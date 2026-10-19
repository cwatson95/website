#!/usr/bin/env python3
"""Display-list capture -> audit -> rasterise, all inside _out/.

    python3 capture.py            capture both sizes, audit, rasterise
    python3 capture.py --no-png   capture and audit only

The capture runs under osascript with _out/ as its working directory (the tail
writes display.json and display_narrow.json there).  Output goes to
_out/cap.log -- never through head/tail, which kills osascript before it
writes (Known-bad)."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_out')
TOOLS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', 'projects', 'simulations', 'tools'))
STEM = 'circuit-construction-kit-dc-virtual-lab'


def main():
    run = io.open(os.path.join(OUT, 'run.js'), encoding='utf-8').read()
    rec = io.open(os.path.join(TOOLS, 'recorder.js'), encoding='utf-8').read()
    tail = io.open(os.path.join(HERE, 'capture_tail_%s.js' % STEM), encoding='utf-8').read()
    io.open(os.path.join(OUT, 'cap_run.js'), 'w', encoding='utf-8').write(run + '\n' + rec + '\n' + tail)
    for f in ('display.json', 'display_narrow.json'):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)                      # never audit a stale file
    r = subprocess.run(['osascript', '-l', 'JavaScript', 'cap_run.js'], cwd=OUT, capture_output=True, text=True, timeout=1800)
    io.open(os.path.join(OUT, 'cap.log'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
    print('capture exit', r.returncode, '-- log in _out/cap.log')
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-3000:])
        sys.exit(1)
    for f in ('display.json', 'display_narrow.json'):
        print('==== audit', f)
        a = subprocess.run([sys.executable, os.path.join(TOOLS, 'audit.py'), f], cwd=OUT, capture_output=True, text=True)
        print(a.stdout + a.stderr)
    if '--no-png' not in sys.argv:
        for f, d in (('display.json', 'png'), ('display_narrow.json', 'png_narrow')):
            os.makedirs(os.path.join(OUT, d), exist_ok=True)
            p = subprocess.run([sys.executable, os.path.join(TOOLS, 'raster.py'), f, d], cwd=OUT, capture_output=True, text=True)
            print('raster', f, 'exit', p.returncode, (p.stdout + p.stderr)[-600:])


if __name__ == '__main__':
    main()
