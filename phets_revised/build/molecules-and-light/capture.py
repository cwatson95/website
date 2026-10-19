#!/usr/bin/env python3
"""Display-list capture: run.js + tools/recorder.js + the capture tail, under
osascript, writing _out/display.json; then audit.py and raster.py."""
import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
TOOLS = os.path.join(root, 'projects', 'simulations', 'tools')
body = io.open(os.path.join(out, 'run.js'), encoding='utf-8').read()
body += '\n' + io.open(os.path.join(TOOLS, 'recorder.js'), encoding='utf-8').read()
body += '\n' + io.open(os.path.join(here, 'capture_tail_molecules-and-light.js'), encoding='utf-8').read()
p = os.path.join(out, 'cap_run.js')
io.open(p, 'w', encoding='utf-8').write(body)
# never pipe osascript through head: a closed pipe kills it before it writes
# display.json and the next audit silently reads a STALE file (Known-bad)
r = subprocess.run(['osascript', '-l', 'JavaScript', p], capture_output=True, text=True,
                   timeout=1800, cwd=out)
io.open(os.path.join(out, 'cap.log'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
sys.stdout.write(r.stdout[-3000:])
sys.stderr.write(r.stderr[-3000:])
if r.returncode:
    sys.exit(r.returncode)
dj = os.path.join(out, 'display.json')
print('--- audit ---')
a = subprocess.run([sys.executable, os.path.join(TOOLS, 'audit.py'), dj], capture_output=True, text=True)
sys.stdout.write(a.stdout)
sys.stderr.write(a.stderr)
print('--- raster ---')
b = subprocess.run([sys.executable, os.path.join(TOOLS, 'raster.py'), dj, out], capture_output=True, text=True)
sys.stdout.write(b.stdout[-2000:])
sys.stderr.write(b.stderr[-2000:])
