"""Write samples from the published weights, every one of them, unsorted.

    python3 generate.py            5 samples of 600 characters, seeds 0 to 4

Each sample starts from a blank line and is drawn with its own seed, written
above it, so a third party who runs this file gets the same characters. All
of them are published, in seed order: choosing the best ones would show what
the model can do on a lucky draw, not what it does.
"""
import os
import sys

import torch

from gpt import GPT
from prepare import load
from train import WEIGHTS

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'verne')
OUT = os.path.join(HERE, 'results', 'samples.txt')
COUNT, LENGTH = 5, 600


def main():
    _, _, _, vocab, encode, decode = load(DATA)
    model = GPT(len(vocab))
    model.load_state_dict(torch.load(WEIGHTS, map_location='cpu', weights_only=True))
    model.eval()
    start = torch.tensor([encode('\n')], dtype=torch.long)    # (1, 1)
    blocks = []
    for seed in range(COUNT):
        torch.manual_seed(seed)
        text = decode(model.generate(start, LENGTH)[0].tolist())[1:]
        blocks.append('--- seed %d, %d characters, unsorted\n%s\n' % (seed, LENGTH, text))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(blocks))
    sys.stdout.write('\n'.join(blocks))
    print('wrote    %s' % os.path.relpath(OUT, HERE))


if __name__ == '__main__':
    main()
