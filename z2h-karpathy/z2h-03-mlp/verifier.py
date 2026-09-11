"""Acceptance test for the MLP. Three checks, one command."""
import torch
from mlp import load, dataset, split, train, evaluate

SEED = 1


def verdict(name, ok, detail):
    print('%-36s %-5s  %s' % (name, 'OK' if ok else 'ECART', detail))
    return ok


words = load()
X, Y = dataset(words)
(Xtr, Ytr), (Xdev, Ydev), _ = split(words)

all_ok = True

# 1. the dataset every number on this page assumes
all_ok &= verdict('1. dataset, shape and dtype',
                  tuple(X.shape) == (228146, 3) and X.dtype == torch.int64
                  and Y.shape[0] == 228146,
                  'expected (228146, 3) int64   got %s %s' % (tuple(X.shape), X.dtype))

# 2. the final model: its size, and where its dev loss lands
torch.manual_seed(SEED)
plain = train(Xtr, Ytr)
size = sum(p.nelement() for p in plain)
dev = evaluate(plain, Xdev, Ydev)
all_ok &= verdict('2. 11897 params, dev in [2.14, 2.20]',
                  size == 11897 and 2.14 <= dev <= 2.20,
                  'expected 11897 and the range   got %d and %.4f' % (size, dev))

# 3. weight decay earns more than the noise floor of 0.03
torch.manual_seed(SEED)
decayed = train(Xtr, Ytr, weight_decay=1e-4)
gain = dev - evaluate(decayed, Xdev, Ydev)
all_ok &= verdict('3. weight_decay 1e-4 gains >= 0.02',
                  gain >= 0.02,
                  'expected >= 0.02              got %.4f' % gain)

print('ALL OK' if all_ok else 'SOMETHING IS OFF')
