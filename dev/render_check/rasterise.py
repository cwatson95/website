#!/usr/bin/env python3
"""rasterise.py — turn record_frames.js display lists into PNGs.

There is no headless browser on this machine, so this implements exactly the
context subset synthwave.js uses: solid/gradient fillRect (linear + radial
gradients), and batched moveTo/lineTo/stroke. Painter's order is preserved via
zorder.

Usage: python3 rasterise.py out/frame_*.json
With more than one frame it also prints the mean |pixel diff| between
consecutive frames — a nonzero value is the undulation/scroll check.
"""
import json
import re
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Rectangle

DPI = 100
HA = {'left': 'left', 'start': 'left', 'center': 'center',
      'right': 'right', 'end': 'right'}
VA = {'top': 'top', 'hanging': 'top', 'middle': 'center',
      'alphabetic': 'baseline', 'bottom': 'bottom'}


def parse_color(s):
    s = s.strip()
    if s.startswith('#'):
        return (int(s[1:3], 16) / 255, int(s[3:5], 16) / 255,
                int(s[5:7], 16) / 255, 1.0)
    m = re.match(r'rgba?\(([^)]*)\)', s)
    parts = [float(p) for p in m.group(1).split(',')]
    r, g, b = [p / 255 for p in parts[:3]]
    a = parts[3] if len(parts) == 4 else 1.0
    return (r, g, b, a)


def grad_rgba(stops, u):
    offs = np.array([s[0] for s in stops], float)
    cols = np.array([parse_color(s[1]) for s in stops], float)
    out = np.empty(u.shape + (4,))
    for c in range(4):
        out[..., c] = np.interp(u, offs, cols[:, c])
    return out


def grad_image(gobj, x, y, rw, rh):
    kind, coords, stops = gobj['__grad'], gobj['coords'], gobj['stops']
    n = 256
    yy, xx = np.meshgrid(np.linspace(y, y + rh, n),
                         np.linspace(x, x + rw, n), indexing='ij')
    if kind == 'linear':
        x0, y0, x1, y1 = coords
        dx, dy = x1 - x0, y1 - y0
        l2 = dx * dx + dy * dy or 1.0
        u = ((xx - x0) * dx + (yy - y0) * dy) / l2
    else:
        x0, y0, r0, x1, y1, r1 = coords
        u = (np.hypot(xx - x1, yy - y1) - r0) / max(r1 - r0, 1e-9)
    return grad_rgba(stops, np.clip(u, 0, 1))


def render(path):
    d = json.load(open(path))
    w, h = d['w'], d['h']
    fig = plt.figure(figsize=(w / DPI, h / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis('off')

    z = 1
    fill_solid, fill_grad = (0, 0, 0, 1), None
    stroke, lw = (0, 0, 0, 1), 1.0
    segs, cur, arcs = [], None, []
    font_px, talign, tbase = 11.0, 'start', 'alphabetic'

    for op in d['ops']:
        name = op[0]
        if name == 'fillStyle':
            v = op[1]
            if isinstance(v, dict):
                fill_grad, fill_solid = v, None
            else:
                fill_solid, fill_grad = parse_color(v), None
        elif name == 'strokeStyle':
            stroke = parse_color(op[1])
        elif name == 'lineWidth':
            lw = op[1]
        elif name == 'font':
            m = re.search(r'([\d.]+)px', op[1])
            font_px = float(m.group(1)) if m else 11.0
        elif name == 'textAlign':
            talign = op[1]
        elif name == 'textBaseline':
            tbase = op[1]
        elif name == 'beginPath':
            segs, cur, arcs = [], None, []
        elif name == 'moveTo':
            cur = (op[1], op[2])
        elif name == 'lineTo':
            if cur is not None:
                segs.append([cur, (op[1], op[2])])
            cur = (op[1], op[2])
        elif name == 'arc':
            arcs.append((op[1], op[2], op[3]))
        elif name == 'fill':
            for (cx, cy, r) in arcs:
                ax.add_patch(Circle((cx, cy), r, facecolor=fill_solid,
                                    edgecolor='none', zorder=z))
                z += 1
        elif name == 'fillText':
            ax.text(op[2], op[3], op[1], color=fill_solid,
                    fontsize=font_px * 72 / DPI, ha=HA.get(talign, 'left'),
                    va=VA.get(tbase, 'baseline'), zorder=z)
            z += 1
        elif name == 'stroke':
            if segs:
                ax.add_collection(LineCollection(
                    segs, colors=[stroke], linewidths=lw * 72 / DPI,
                    zorder=z, capstyle='butt'))
                z += 1
            for (cx, cy, r) in arcs:
                ax.add_patch(Circle((cx, cy), r, facecolor='none',
                                    edgecolor=stroke,
                                    linewidth=lw * 72 / DPI, zorder=z))
                z += 1
        elif name == 'fillRect':
            x, y, rw, rh = op[1:5]
            if fill_grad is None:
                ax.add_patch(Rectangle((x, y), rw, rh, facecolor=fill_solid,
                                       edgecolor='none', zorder=z))
            else:
                ax.imshow(grad_image(fill_grad, x, y, rw, rh),
                          extent=(x, x + rw, y + rh, y), zorder=z,
                          interpolation='bilinear', origin='upper')
            z += 1

    out = path.rsplit('.json', 1)[0] + '.png'
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(out)
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pngs = [render(p) for p in sys.argv[1:]]
    if len(pngs) > 1:
        import matplotlib.image as mpimg
        imgs = [mpimg.imread(p) for p in pngs]
        for a, b, pa, pb in zip(imgs, imgs[1:], pngs, pngs[1:]):
            diff = float(np.abs(a[..., :3] - b[..., :3]).mean() * 255)
            print(f'mean|diff| {pa} -> {pb}: {diff:.2f}/255')


if __name__ == '__main__':
    main()
