#!/usr/bin/env python3
"""Capture the display list at three stage sizes, audit each, and rasterise the
default size.  Run after assemble.py.  Writes _out/display_<W>x<H>.json,
_out/audit_<W>x<H>.txt and _out/png/view_*.png.  Never pipes osascript
through head/tail (the Known-bad stale-display.json trap)."""
import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
tools = os.path.abspath(os.path.join(here, '..', '..', '..', '..', 'projects', 'simulations', 'tools'))
run = io.open(os.path.join(out, 'run.js'), encoding='utf-8').read()
rec = io.open(os.path.join(tools, 'recorder.js'), encoding='utf-8').read()
tail = io.open(os.path.join(here, 'capture_tail_gas-properties.js'), encoding='utf-8').read()
bad = 0
for (W, H) in [(1400, 820), (1100, 700), (560, 380)]:
    js = 'var CAP_W=%d, CAP_H=%d;\n' % (W, H) + run + '\n' + rec + '\n' + tail
    p = os.path.join(out, 'cap_run_%dx%d.js' % (W, H))
    io.open(p, 'w', encoding='utf-8').write(js)
    dj = os.path.join(out, 'display.json')
    if os.path.exists(dj):
        os.remove(dj)
    r = subprocess.run(['osascript', '-l', 'JavaScript', p], cwd=out, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or not os.path.exists(dj):
        print('capture %dx%d FAILED' % (W, H), r.stderr[-400:])
        sys.exit(1)
    dst = os.path.join(out, 'display_%dx%d.json' % (W, H))
    os.replace(dj, dst)
    a = subprocess.run([sys.executable, os.path.join(tools, 'audit.py'), dst], capture_output=True, text=True)
    io.open(os.path.join(out, 'audit_%dx%d.txt' % (W, H)), 'w').write(a.stdout)
    last = a.stdout.strip().splitlines()[-1] if a.stdout.strip() else '?'
    print('%dx%d: %s' % (W, H, last))
    for line in a.stdout.splitlines():
        if line.startswith('!!') or 'OFF' in line or 'HIT' in line or 'ENTITY' in line:
            print('   ' + line)
    if a.returncode != 0:
        bad += 1
os.makedirs(os.path.join(out, 'png'), exist_ok=True)
subprocess.run([sys.executable, os.path.join(tools, 'raster.py'), os.path.join(out, 'display_1400x820.json'), os.path.join(out, 'png')],
               capture_output=True, text=True)
os.makedirs(os.path.join(out, 'png_small'), exist_ok=True)
subprocess.run([sys.executable, os.path.join(tools, 'raster.py'), os.path.join(out, 'display_560x380.json'), os.path.join(out, 'png_small')],
               capture_output=True, text=True)
print('rasterised 1400x820 -> _out/png, 560x380 -> _out/png_small')
sys.exit(1 if bad else 0)
