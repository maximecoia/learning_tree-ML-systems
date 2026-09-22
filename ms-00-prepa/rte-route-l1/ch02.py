"""Chapter 2, my answer: the sliding window, the dataloader, the two embeddings.

    cd pratique/raschka && ../../.venv/bin/python3 mes-reponses/ch02.py

The corpus belongs to the book and is not versioned here, so it is resolved
from this file's location rather than from the working directory.
"""

from pathlib import Path

import tiktoken
import torch

from torch.utils.data import Dataset, DataLoader

# `__file__` exists in a .py but not in every notebook, and this answer is
# also meant to be pasted into one.
try:
    HERE = Path(__file__).resolve().parent
except NameError:
    HERE = Path.cwd().resolve()


def find_corpus(name="the-verdict.txt"):
    """Walk up until the book's chapter 2 directory comes into reach.

    This file is read from `mes-reponses/` and, as a blank-file exercise, from
    `mes-reponses/blanc/`. A fixed number of `.parent` hops is wrong in one of
    the two, and it fails on a path instead of on a concept.
    """
    relative = Path("ch02") / "01_main-chapter-code" / name
    for directory in [HERE, *HERE.parents]:
        candidate = directory / relative
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"corpus not found: {relative}")


CORPUS = find_corpus()


class GPTDatasetV1(Dataset):

    def __init__(self, txt, tokenizer, max_length, stride):
        self.input_ids = []
        self.target_ids = []

        # Convert the complete text into token IDs
        token_ids = tokenizer.encode(txt, allowed_special={"<|endoftext|>"})

        # Create input/target sequences
        for i in range(0, len(token_ids) - max_length, stride):
            input_chunk = token_ids[i : i + max_length]

            target_chunk = token_ids[i + 1 : i + max_length + 1]

            # `dtype=torch.long`: these numbers are indices, not values. An
            # Embedding layer uses them to pick a row from its table, and it
            # wants 64-bit integers. PyTorch would infer that from a list of
            # Python ints anyway; writing it keeps the distinction visible.
            self.input_ids.append(torch.tensor(input_chunk, dtype=torch.long))

            self.target_ids.append(
                torch.tensor(target_chunk, dtype=torch.long)
            )

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return (self.input_ids[idx], self.target_ids[idx])


def create_dataloader_v1(
    txt,
    batch_size=4,
    max_length=256,
    stride=128,
    shuffle=True,
    drop_last=True,
    num_workers=0,
):
    tokenizer = tiktoken.get_encoding("gpt2")

    dataset = GPTDatasetV1(txt, tokenizer, max_length, stride)

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        drop_last=drop_last,
        num_workers=num_workers,
    )

    return dataloader


if __name__ == "__main__":
    with open(CORPUS, "r", encoding="utf-8") as f:
        raw_text = f.read()

    vocab_size = 50257
    output_dim = 256
    context_length = 1024

    token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

    pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)

    batch_size = 8
    max_length = 4

    dataloader = create_dataloader_v1(
        raw_text,
        batch_size=batch_size,
        max_length=max_length,
        stride=max_length,
    )

    for batch in dataloader:
        x, y = batch

        token_embeddings = token_embedding_layer(x)

        # `device=x.device`: the positions are born wherever the data lives.
        # Everything is on the CPU today, so this changes nothing; the day `x`
        # moves to a GPU, it is what keeps the addition below legal.
        positions = torch.arange(max_length, device=x.device)

        pos_embeddings = pos_embedding_layer(positions)

        input_embeddings = token_embeddings + pos_embeddings

        break

    print(input_embeddings.shape)
