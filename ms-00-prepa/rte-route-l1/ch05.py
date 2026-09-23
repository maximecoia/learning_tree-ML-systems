"""Chapter 5, my answer: the GPT of chapter 4 is finally made to learn.

    python3 ch05.py     # from this file's own directory

It needs `torch`, `tiktoken` and `numpy`, plus `ch02.py` and `ch04.py`
beside it. It also needs the book's corpus, which is not published, so
this file is published to be read rather than run.

The chapter's own script trains GPT-2 124M for ten epochs and then downloads
OpenAI's weights. Both are out of reach for a file meant to be run on the spot,
so the demo below keeps the chapter's pipeline and shrinks only the model: two
layers, ninety-six dimensions, a few dozen steps. The loss still falls from
log(vocab_size) the way the chapter says it should, and the checkpoint is still
saved, reloaded and resumed.

`load_weights_into_gpt` is written out in full because it is the chapter's
point -- an architecture compatible enough with GPT-2 to accept its
parameters -- but it is not executed here: it would download half a gigabyte.

Importing `ch02` prints one line of its own, `torch.Size([8, 4, 256])`. That
file has no `if __name__ == "__main__"` guard, because the fiche's listing has
none either and the two are kept identical.
"""

import math
import tempfile

from pathlib import Path

import numpy as np
import tiktoken
import torch

# Chapter 2 built the loaders, chapter 4 the model. This file adds what turns
# one into the other: a loss, a loop, and a way to save the result.
from ch02 import create_dataloader_v1, find_corpus
from ch04 import GPTModel, generate_text_simple


def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")

    if torch.backends.mps.is_available():
        major, minor = map(int, torch.__version__.split(".")[:2])

        if (major, minor) >= (2, 9):
            return torch.device("mps")

    return torch.device("cpu")


def text_to_token_ids(text, tokenizer):
    encoded = tokenizer.encode(text, allowed_special={"<|endoftext|>"})

    # unsqueeze(0) adds the batch axis the model expects.
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)

    return encoded_tensor


def token_ids_to_text(token_ids, tokenizer):
    flat = token_ids.squeeze(0)

    return tokenizer.decode(flat.tolist())


def calc_loss_batch(input_batch, target_batch, model, device):
    """One scalar, on which the whole network's gradient will depend.

    `cross_entropy` wants one row per prediction, so the batch and token axes
    are folded together: [B, T, V] becomes [B*T, V], and [B, T] becomes [B*T].
    """
    input_batch = input_batch.to(device)
    target_batch = target_batch.to(device)

    logits = model(input_batch)

    loss = torch.nn.functional.cross_entropy(
        logits.flatten(0, 1), target_batch.flatten()
    )

    return loss


def calc_loss_loader(data_loader, model, device, num_batches=None):
    """The average loss over a loader, or over its first `num_batches`.

    Re-reading the whole set every few steps would cost more than the training
    itself, so evaluation settles for an estimate.
    """
    total_loss = 0.0

    if len(data_loader) == 0:
        return float("nan")

    if num_batches is None:
        num_batches = len(data_loader)

    else:
        num_batches = min(num_batches, len(data_loader))

    for i, (input_batch, target_batch) in enumerate(data_loader):
        if i >= num_batches:
            break

        loss = calc_loss_batch(input_batch, target_batch, model, device)

        total_loss += loss.item()

    return total_loss / num_batches


def evaluate_model(model, train_loader, val_loader, device, eval_iter):
    """eval() silences dropout, no_grad() stops the graph. Both are needed."""
    model.eval()

    with torch.no_grad():
        train_loss = calc_loss_loader(
            train_loader, model, device, num_batches=eval_iter
        )

        val_loss = calc_loss_loader(
            val_loader, model, device, num_batches=eval_iter
        )

    model.train()

    return train_loss, val_loss


def generate_and_print_sample(model, tokenizer, device, start_context):
    """The loss says the predictions improve; this says whether it reads."""
    model.eval()

    # The model itself says how many positions its table can index.
    context_size = model.pos_emb.weight.shape[0]

    encoded = text_to_token_ids(start_context, tokenizer).to(device)

    with torch.no_grad():
        token_ids = generate_text_simple(
            model=model,
            idx=encoded,
            max_new_tokens=50,
            context_size=context_size,
        )

    decoded_text = token_ids_to_text(token_ids, tokenizer)

    print(decoded_text.replace("\n", " "))

    model.train()


def train_model_simple(
    model,
    train_loader,
    val_loader,
    optimizer,
    device,
    num_epochs,
    eval_freq,
    eval_iter,
    start_context,
    tokenizer,
):
    train_losses = []
    val_losses = []
    track_tokens_seen = []

    tokens_seen = 0

    # -1 so the very first step lands on 0, and is therefore evaluated: it
    # gives a reference point taken before any weight has moved far.
    global_step = -1

    for epoch in range(num_epochs):
        model.train()

        for input_batch, target_batch in train_loader:
            # PyTorch accumulates gradients; without this line the previous
            # batch's would be added to this one's.
            optimizer.zero_grad()

            loss = calc_loss_batch(input_batch, target_batch, model, device)

            loss.backward()

            optimizer.step()

            tokens_seen += input_batch.numel()

            global_step += 1

            if global_step % eval_freq == 0:
                train_loss, val_loss = evaluate_model(
                    model, train_loader, val_loader, device, eval_iter
                )

                train_losses.append(train_loss)
                val_losses.append(val_loss)
                track_tokens_seen.append(tokens_seen)

                print(
                    f"Ep {epoch + 1} "
                    f"(Step {global_step:06d}): "
                    f"Train loss {train_loss:.3f}, "
                    f"Val loss {val_loss:.3f}"
                )

        generate_and_print_sample(model, tokenizer, device, start_context)

    return train_losses, val_losses, track_tokens_seen


def generate(
    model,
    idx,
    max_new_tokens,
    context_size,
    temperature=0.0,
    top_k=None,
    eos_id=None,
):
    """Decoding, which changes how a token is picked and never the weights."""
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -context_size:]

        with torch.no_grad():
            logits = model(idx_cond)

        # Only the last position predicts the next token.
        logits = logits[:, -1, :]

        if top_k is not None:
            top_logits, _ = torch.topk(logits, top_k)

            # The smallest of the k best becomes the threshold.
            min_val = top_logits[:, -1]

            # Below it, -inf: exp(-inf) is 0, so softmax gives those tokens
            # exactly no chance of being drawn.
            logits = torch.where(
                logits < min_val.unsqueeze(-1),
                torch.tensor(float("-inf"), device=logits.device),
                logits,
            )

        if temperature > 0.0:
            # Dividing by less than 1 deepens the gaps, by more than 1
            # flattens them. The model has not changed either way.
            logits = logits / temperature

            # Subtracting the maximum leaves softmax unchanged and keeps the
            # exponentials small.
            logits = logits - logits.max(dim=-1, keepdim=True).values

            probs = torch.softmax(logits, dim=-1)

            idx_next = torch.multinomial(probs, num_samples=1)

        else:
            # temperature = 0 means, in this API, no sampling at all.
            idx_next = torch.argmax(logits, dim=-1, keepdim=True)

        if eos_id is not None:
            if torch.all(idx_next == eos_id):
                break

        idx = torch.cat((idx, idx_next), dim=1)

    return idx


def assign(left, right):
    """`left` only says what shape is expected; checking it here turns a wrong
    architecture into an immediate error rather than a silent mismatch."""
    if left.shape != right.shape:
        raise ValueError(
            f"Shape mismatch. Left: {left.shape}, Right: {right.shape}"
        )

    return torch.nn.Parameter(torch.tensor(right))


def load_weights_into_gpt(gpt, params):
    """Fill this architecture with OpenAI's parameters.

    Written out because it is the chapter's point, and not run here: the
    checkpoint is half a gigabyte away. Two conventions have to be bridged.
    GPT-2 keeps Q, K and V in one `c_attn` matrix where we have three layers,
    and it stores its weights transposed with respect to `nn.Linear`.
    """

    gpt.pos_emb.weight = assign(gpt.pos_emb.weight, params["wpe"])
    gpt.tok_emb.weight = assign(gpt.tok_emb.weight, params["wte"])

    for b in range(len(params["blocks"])):
        q_w, k_w, v_w = np.split(
            params["blocks"][b]["attn"]["c_attn"]["w"], 3, axis=-1
        )

        gpt.trf_blocks[b].att.W_query.weight = assign(
            gpt.trf_blocks[b].att.W_query.weight, q_w.T
        )
        gpt.trf_blocks[b].att.W_key.weight = assign(
            gpt.trf_blocks[b].att.W_key.weight, k_w.T
        )
        gpt.trf_blocks[b].att.W_value.weight = assign(
            gpt.trf_blocks[b].att.W_value.weight, v_w.T
        )

        # Biases are one-dimensional, so they need no transpose.
        q_b, k_b, v_b = np.split(
            params["blocks"][b]["attn"]["c_attn"]["b"], 3, axis=-1
        )

        gpt.trf_blocks[b].att.W_query.bias = assign(
            gpt.trf_blocks[b].att.W_query.bias, q_b
        )
        gpt.trf_blocks[b].att.W_key.bias = assign(
            gpt.trf_blocks[b].att.W_key.bias, k_b
        )
        gpt.trf_blocks[b].att.W_value.bias = assign(
            gpt.trf_blocks[b].att.W_value.bias, v_b
        )

        gpt.trf_blocks[b].att.out_proj.weight = assign(
            gpt.trf_blocks[b].att.out_proj.weight,
            params["blocks"][b]["attn"]["c_proj"]["w"].T,
        )
        gpt.trf_blocks[b].att.out_proj.bias = assign(
            gpt.trf_blocks[b].att.out_proj.bias,
            params["blocks"][b]["attn"]["c_proj"]["b"],
        )

        gpt.trf_blocks[b].ff.layers[0].weight = assign(
            gpt.trf_blocks[b].ff.layers[0].weight,
            params["blocks"][b]["mlp"]["c_fc"]["w"].T,
        )
        gpt.trf_blocks[b].ff.layers[0].bias = assign(
            gpt.trf_blocks[b].ff.layers[0].bias,
            params["blocks"][b]["mlp"]["c_fc"]["b"],
        )

        gpt.trf_blocks[b].ff.layers[2].weight = assign(
            gpt.trf_blocks[b].ff.layers[2].weight,
            params["blocks"][b]["mlp"]["c_proj"]["w"].T,
        )
        gpt.trf_blocks[b].ff.layers[2].bias = assign(
            gpt.trf_blocks[b].ff.layers[2].bias,
            params["blocks"][b]["mlp"]["c_proj"]["b"],
        )

        gpt.trf_blocks[b].norm1.scale = assign(
            gpt.trf_blocks[b].norm1.scale, params["blocks"][b]["ln_1"]["g"]
        )
        gpt.trf_blocks[b].norm1.shift = assign(
            gpt.trf_blocks[b].norm1.shift, params["blocks"][b]["ln_1"]["b"]
        )
        gpt.trf_blocks[b].norm2.scale = assign(
            gpt.trf_blocks[b].norm2.scale, params["blocks"][b]["ln_2"]["g"]
        )
        gpt.trf_blocks[b].norm2.shift = assign(
            gpt.trf_blocks[b].norm2.shift, params["blocks"][b]["ln_2"]["b"]
        )

    gpt.final_norm.scale = assign(gpt.final_norm.scale, params["g"])
    gpt.final_norm.shift = assign(gpt.final_norm.shift, params["b"])

    # GPT-2 reuses its embedding table as the output matrix: weight tying.
    gpt.out_head.weight = assign(gpt.out_head.weight, params["wte"])


# Small enough to train in seconds, and still the chapter's pipeline. Only
# vocab_size has to stay honest: the corpus is tokenised with GPT-2's BPE.
CONFIG_DEMO = {
    "vocab_size": 50257,
    "context_length": 64,
    "emb_dim": 96,
    "n_heads": 4,
    "n_layers": 2,
    "drop_rate": 0.1,
    "qkv_bias": False,
}


if __name__ == "__main__":
    device = get_device()
    tokenizer = tiktoken.get_encoding("gpt2")

    text_data = find_corpus().read_text(encoding="utf-8")

    split_idx = int(0.90 * len(text_data))
    train_data, val_data = text_data[:split_idx], text_data[split_idx:]

    torch.manual_seed(123)

    commun = dict(
        batch_size=2,
        max_length=CONFIG_DEMO["context_length"],
        stride=CONFIG_DEMO["context_length"],
        num_workers=0,
    )
    train_loader = create_dataloader_v1(
        train_data, drop_last=True, shuffle=True, **commun
    )
    val_loader = create_dataloader_v1(
        val_data, drop_last=False, shuffle=False, **commun
    )

    model = GPTModel(CONFIG_DEMO).to(device)

    with torch.no_grad():
        depart = calc_loss_loader(train_loader, model, device)

    attendu = math.log(CONFIG_DEMO["vocab_size"])
    print(f"device                    {device}")
    print(f"batches train / val       {len(train_loader)} / {len(val_loader)}")
    print(f"loss avant entraînement   {depart:.3f}")
    print(f"log(vocab_size)           {attendu:.3f}   <- le repère du hasard")

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=0.0004, weight_decay=0.1
    )

    print("\nentraînement")
    train_losses, val_losses, _ = train_model_simple(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        optimizer=optimizer,
        device=device,
        num_epochs=2,
        eval_freq=20,
        eval_iter=5,
        start_context="Every effort moves you",
        tokenizer=tokenizer,
    )
    print(
        f"\nla loss est passée de {train_losses[0]:.3f} "
        f"à {train_losses[-1]:.3f}"
    )

    print("\ndécoder autrement, à modèle inchangé")
    depart_ids = text_to_token_ids("Every effort moves you", tokenizer)
    for nom, kwargs in (
        ("greedy           ", {}),
        ("temperature 1.4  ", {"temperature": 1.4}),
        ("+ top_k 25       ", {"temperature": 1.4, "top_k": 25}),
    ):
        torch.manual_seed(123)
        sortie = generate(
            model=model,
            idx=depart_ids.to(device),
            max_new_tokens=12,
            context_size=CONFIG_DEMO["context_length"],
            **kwargs,
        )
        texte = token_ids_to_text(sortie, tokenizer).replace("\n", " ")
        print(f"    {nom} {texte}")

    print("\ncheckpoint : sauver, recharger, reprendre")
    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "model_and_optimizer.pth"
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
            },
            chemin,
        )

        checkpoint = torch.load(chemin, map_location=device, weights_only=True)

        repris = GPTModel(CONFIG_DEMO)
        repris.load_state_dict(checkpoint["model_state_dict"])
        repris.to(device)

        neuf = torch.optim.AdamW(
            repris.parameters(), lr=0.0004, weight_decay=0.1
        )
        neuf.load_state_dict(checkpoint["optimizer_state_dict"])
        repris.train()

        # Comparer deux passages du loader mesurerait le dropout et le
        # mélange, pas la fidélité du rechargement : une première version
        # annonçait un écart de 9e-02 qui ne disait rien. Les deux modèles
        # sont donc jugés en eval(), sur le même tenseur, logit par logit.
        lot = next(iter(train_loader))[0].to(device)
        model.eval()
        repris.eval()

        with torch.no_grad():
            ecart = (model(lot) - repris(lot)).abs().max().item()

        print(f"    écart maximal des logits {ecart:.2e}")
        print(f"    identiques               {ecart == 0.0}")

        # Et le contrôle sait-il voir une différence ? On bouge un poids que
        # chaque position traverse. Un premier essai déplaçait l'embedding du
        # token 0, absent de ce lot : le sabotage ne touchait pas ce que la
        # mesure regarde, et se taisait donc à tort.
        with torch.no_grad():
            repris.final_norm.shift[0] += 1.0
            temoin = (model(lot) - repris(lot)).abs().max().item()

        print(f"    après un poids déplacé   {temoin:.2e}")
        assert ecart == 0.0 and temoin > 0.0
