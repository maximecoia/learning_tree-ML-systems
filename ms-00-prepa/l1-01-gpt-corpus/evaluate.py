"""Measure the published weights: dev loss on every window, against the landmarks.

    python3 evaluate.py            dev, ln(V) and the bigram, into results/eval.json
    python3 evaluate.py --test     the test loss, once, into results/test.json

Dev is measured on every full window of the split, none sampled, the way
check 7 of verifier.py measures it. The test split is read only with --test,
and only once: the script refuses a second look while results/test.json
exists. Every look at test to choose a setting turns it, slowly and
invisibly, into a second dev set.
"""
import datetime
import json
import math
import os
import sys

import torch

from gpt import BLOCK_SIZE, GPT
from prepare import load
from train import WEIGHTS, bigram_dev_loss, count_parameters

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'verne')
RESULTS = os.path.join(HERE, 'results')


@torch.no_grad()
def window_loss(model, ids):
    """Mean next-token loss over every full window of ids, none sampled."""
    n = (len(ids) - 1) // BLOCK_SIZE
    x = ids[:n * BLOCK_SIZE].view(n, BLOCK_SIZE)
    y = ids[1:n * BLOCK_SIZE + 1].view(n, BLOCK_SIZE)
    model.eval()
    total = 0.0
    for i in range(0, n, 256):
        total += model(x[i:i + 256], y[i:i + 256])[1].item() * len(x[i:i + 256])
    return total / n, n


def main():
    test = '--test' in sys.argv[1:]
    train_data, dev_data, test_data, vocab, _, _ = load(DATA)
    V = len(vocab)
    model = GPT(V)
    model.load_state_dict(torch.load(WEIGHTS, map_location='cpu', weights_only=True))
    os.makedirs(RESULTS, exist_ok=True)

    if test:
        target = os.path.join(RESULTS, 'test.json')
        if os.path.exists(target):
            raise SystemExit('REFUSED  results/test.json exists: the test split '
                             'has been looked at already, and is looked at once')
        loss, windows = window_loss(model, test_data)
        report = {'test_loss': loss, 'windows': windows,
                  'bigram_test_loss': bigram_dev_loss(train_data, test_data, V),
                  'measured_at': datetime.datetime.now().isoformat(timespec='seconds')}
        print('test     %.4f on %d windows   bigram %.4f'
              % (loss, windows, report['bigram_test_loss']))
    else:
        target = os.path.join(RESULTS, 'eval.json')
        loss, windows = window_loss(model, dev_data)
        total, no_tables = count_parameters(model)
        report = {'dev_loss': loss, 'windows': windows, 'ln_V': math.log(V),
                  'bigram_dev_loss': bigram_dev_loss(train_data, dev_data, V),
                  'parameters': {'all': total, 'without_embedding_tables': no_tables}}
        print('dev      %.4f on %d windows   ln(V) %.4f   bigram %.4f'
              % (loss, windows, report['ln_V'], report['bigram_dev_loss']))
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print('wrote    %s' % os.path.relpath(target, HERE))


if __name__ == '__main__':
    main()
