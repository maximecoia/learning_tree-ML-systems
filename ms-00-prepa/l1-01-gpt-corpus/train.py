"""Train the GPT of gpt.py on the prepared corpus.

    python3 train.py configs/smoke.json     a 50-step run that proves the pipeline
    python3 train.py configs/final.json     the published run, writes gpt.pt

The config holds the training choices; the architecture lives in gpt.py.
Outputs land in results/<name>/: losses.csv (step, train, dev) and run.json
(seed, hyperparameters, parameter counts, duration and hardware). Only a
config with "save_weights": true writes gpt.pt beside gpt.py, where
verifier.py and evaluate.py read it, so a smoke run never overwrites the
published weights.
"""
import csv
import json
import math
import os
import platform
import sys
import time

import torch

import gpt
from gpt import BLOCK_SIZE, GPT, SEED
from prepare import load

HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = os.path.join(HERE, 'gpt.pt')


def batch(data, batch_size, block_size, generator=None):
    """(x, y), each (batch_size, block_size): random windows, y shifted by one."""
    i = torch.randint(len(data) - block_size - 1, (batch_size,), generator=generator)
    x = torch.stack([data[j:j + block_size] for j in i])
    y = torch.stack([data[j + 1:j + 1 + block_size] for j in i])
    return x, y


def bigram_dev_loss(train_data, dev_data, vocab_size):
    """Dev loss of a counted bigram, add-one smoothed: the number to beat."""
    counts = torch.ones(vocab_size, vocab_size)
    counts.index_put_((train_data[:-1], train_data[1:]),
                      torch.ones(len(train_data) - 1), accumulate=True)
    logp = (counts / counts.sum(1, keepdim=True)).log()
    return -logp[dev_data[:-1], dev_data[1:]].mean().item()


def count_parameters(model):
    """(all, without the two embedding tables)."""
    total = sum(p.numel() for p in model.parameters())
    tables = (model.token_embedding.weight.numel()
              + model.position_embedding.weight.numel())
    return total, total - tables


@torch.no_grad()
def estimate(model, data, batches, batch_size, generator_seed):
    """Mean loss over the same batches at every call, so two evals compare."""
    g = torch.Generator().manual_seed(generator_seed)
    model.eval()
    losses = [model(*batch(data, batch_size, BLOCK_SIZE, g))[1].item()
              for _ in range(batches)]
    model.train()
    return sum(losses) / len(losses)


def train(config, data_dir):
    """Train one model with the given config. Returns (model, rows, run)."""
    torch.manual_seed(SEED)
    train_data, dev_data, _, vocab, _, _ = load(data_dir)   # test stays unread
    V = len(vocab)
    model = GPT(V)
    opt = torch.optim.AdamW(model.parameters(), lr=config['lr'])
    g = torch.Generator().manual_seed(SEED)
    bigram = bigram_dev_loss(train_data, dev_data, V)
    print('ln(V)    %.4f   bigram dev %.4f' % (math.log(V), bigram))

    rows = []
    start = time.perf_counter()
    for step in range(config['steps'] + 1):
        if step % config['eval_every'] == 0 or step == config['steps']:
            tr = estimate(model, train_data, config['eval_batches'], config['batch_size'], 1)
            dv = estimate(model, dev_data, config['eval_batches'], config['batch_size'], 2)
            rows.append((step, tr, dv))
            print('step %5d   train %.4f   dev %.4f' % (step, tr, dv))
        if step == config['steps']:
            break
        x, y = batch(train_data, config['batch_size'], BLOCK_SIZE, g)
        _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    elapsed = time.perf_counter() - start

    total, no_tables = count_parameters(model)
    run = {
        'config': config,
        'data_dir': os.path.relpath(os.path.abspath(data_dir), HERE),
        'seed': SEED,
        'architecture': {'block_size': BLOCK_SIZE, 'n_emb': gpt.N_EMB,
                         'n_head': gpt.N_HEAD, 'n_layer': gpt.N_LAYER,
                         'dropout': gpt.DROPOUT, 'vocab_size': V},
        'parameters': {'all': total, 'without_embedding_tables': no_tables},
        'ln_V': math.log(V),
        'bigram_dev_loss': bigram,
        'seconds': round(elapsed, 1),
        'hardware': {'machine': platform.machine(),
                     'processor': platform.processor() or 'cpu',
                     'system': platform.system(), 'device': 'cpu'},
        'versions': {'python': platform.python_version(), 'torch': torch.__version__},
    }
    print('params   %d all, %d without the embedding tables' % (total, no_tables))
    print('time     %.0f s on %s, %s, torch %s'
          % (elapsed, run['hardware']['machine'], run['hardware']['processor'],
             torch.__version__))
    return model, rows, run


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding='utf-8') as f:
        config = json.load(f)
    model, rows, run = train(config, os.path.join(HERE, config['data_dir']))
    out = os.path.join(HERE, 'results', config['name'])
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'losses.csv'), 'w', newline='') as f:
        csv.writer(f).writerows([('step', 'train', 'dev'), *rows])
    with open(os.path.join(out, 'run.json'), 'w', encoding='utf-8') as f:
        json.dump(run, f, indent=2)
        f.write('\n')
    if config.get('save_weights'):
        torch.save(model.state_dict(), WEIGHTS)
        print('wrote    gpt.pt')
    print('wrote    %s' % os.path.relpath(out, HERE))


if __name__ == '__main__':
    main()
