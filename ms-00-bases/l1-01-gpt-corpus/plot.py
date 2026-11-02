"""Draw the two curves of the published run into results/curves.svg.

    python3 plot.py

Train and dev on one graph, the whole run from step 0, with the three
landmarks: ln(V), where an honest initialisation starts; the counted bigram,
what the model has to beat; and the bar of check 7, the bigram minus 0.10.
The chosen step is marked. Standard library only, so the figure is rebuilt
from losses.csv on any machine, and GitHub shows the SVG as it is.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(HERE, 'results', 'final')
OUT = os.path.join(HERE, 'results', 'curves.svg')

W, H = 760, 420
X0, Y0, PW, PH = 70, 30, 640, 320          # the plotting area
YMIN, YMAX = 1.5, 5.0
DEV, TRAIN, BIGRAM, LNV, BAR, INK = '#2F4796', '#7F93D1', '#A2452A', '#555B70', '#276240', '#14161F'


def main():
    with open(os.path.join(RUN, 'losses.csv'), newline='') as f:
        rows = [(int(r['step']), float(r['train']), float(r['dev'])) for r in csv.DictReader(f)]
    with open(os.path.join(RUN, 'run.json'), encoding='utf-8') as f:
        run = json.load(f)
    last = rows[-1][0]

    def px(step, loss):
        return (X0 + PW * step / last, Y0 + PH * (YMAX - loss) / (YMAX - YMIN))

    def text(x, y, s, color=INK, anchor='start', size=12):
        return ('<text x="%.1f" y="%.1f" fill="%s" font-family="Menlo, monospace" '
                'font-size="%d" text-anchor="%s">%s</text>' % (x, y, color, size, anchor, s))

    def hline(loss, color, label, dy):
        (xa, y), (xb, _) = px(0, loss), px(last, loss)
        return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                'stroke-dasharray="5 4" stroke-width="1.3"/>' % (xa, y, xb, y, color)
                + text(xb - 4, y + dy, label, color, 'end', 11))

    def curve(index, color, dash):
        pts = ' '.join('%.1f,%.1f' % px(r[0], r[index]) for r in rows)
        return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.2"%s/>'
                % (pts, color, ' stroke-dasharray="4 3"' if dash else ''))

    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
           'role="img" aria-label="Train and dev loss over %d steps">' % (W, H, W, last),
           '<rect width="100%" height="100%" fill="#FFFFFF"/>']
    for loss in (2, 3, 4, 5):
        (xa, y), (xb, _) = px(0, loss), px(last, loss)
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#E2E4EC"/>' % (xa, y, xb, y))
        out.append(text(xa - 8, y + 4, str(loss), LNV, 'end', 11))
    for step in range(0, last + 1, 1000):
        x, y = px(step, YMIN)
        out.append(text(x, y + 18, str(step), LNV, 'middle', 11))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (X0, Y0 + PH, X0 + PW, Y0 + PH, LNV))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (X0, Y0, X0, Y0 + PH, LNV))
    out.append(text(X0 + PW / 2, H - 14, 'training step', LNV, 'middle', 12))
    out.append(text(X0, Y0 - 12, 'loss (nats)', LNV, 'start', 12))
    out.append(hline(run['ln_V'], LNV, 'ln(V) %.4f' % run['ln_V'], -6))
    out.append(hline(run['bigram_dev_loss'], BIGRAM, 'bigram dev %.4f' % run['bigram_dev_loss'], -6))
    bar = run['bigram_dev_loss'] - 0.10
    out.append(hline(bar, BAR, 'check 7 bar %.4f' % bar, 14))
    out.append(curve(1, TRAIN, True))
    out.append(curve(2, DEV, False))
    x, y = px(last, rows[-1][2])
    out.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x, y, DEV))
    out.append(text(x - 8, y + 22, 'chosen: step %d, dev %.4f' % (last, rows[-1][2]), DEV, 'end', 11))
    lx, ly = X0 + 380, Y0 + 110     # below the ln(V) label, above the curves' tail
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2"/>' % (lx, ly, lx + 28, ly, DEV))
    out.append(text(lx + 36, ly + 4, 'dev, 50 fixed batches', DEV, 'start', 11))
    out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" '
               'stroke-dasharray="4 3"/>' % (lx, ly + 18, lx + 28, ly + 18, TRAIN))
    out.append(text(lx + 36, ly + 22, 'train, 50 fixed batches', TRAIN, 'start', 11))
    out.append('</svg>')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print('wrote    %s' % os.path.relpath(OUT, HERE))


if __name__ == '__main__':
    main()
