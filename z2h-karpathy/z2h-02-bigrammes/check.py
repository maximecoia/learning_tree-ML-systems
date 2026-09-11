import torch
import matplotlib

print("torch     ", torch.__version__)
print("matplotlib", matplotlib.__version__)
print("noms      ", len(open('names.txt').read().splitlines()))
