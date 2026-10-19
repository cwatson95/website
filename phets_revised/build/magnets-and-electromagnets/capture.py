#!/usr/bin/env python3
"""capture.py -- display-list capture -> audit -> PNGs, for one stem of the family.

    python3 capture.py [stem] [W H]

Concatenates _out/run.js + tools/recorder.js + capture_tail_<stem>.js, runs it under
osascript (redirected to a log file, never a pipe: a closed pipe kills osascript before
it writes the JSON, and the audit then reads a stale file), then runs tools/audit.py and
tools/raster.py over the result.
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(BUILD, '..', '..', '..'))
TOOLS = os.path.join(ROOT, 'projects', 'simulations', 'tools')
stem = sys.argv[1] if len(sys.argv) > 1 else 'magnets-and-electromagnets'
W, H = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1400, 820)
sdir = os.path.join(BUILD, stem)
out = os.path.join(sdir, '_out')
tag = '' if (W, H) == (1400, 820) else '_%dx%d' % (W, H)
os.makedirs(os.path.join(out, 'png' + tag), exist_ok=True)

js = ('const CAP_W=%d, CAP_H=%d, CAP_FILE=%r;\n' % (W, H, os.path.join(out, 'display%s.json' % tag))
      + io.open(os.path.join(out, 'run.js'), encoding='utf-8').read()
      + io.open(os.path.join(TOOLS, 'recorder.js'), encoding='utf-8').read()
      + io.open(os.path.join(sdir, 'capture_tail_%s.js' % stem), encoding='utf-8').read())
cap = os.path.join(out, 'cap_run%s.js' % tag)
io.open(cap, 'w', encoding='utf-8').write(js)
log = os.path.join(out, 'cap%s.log' % tag)
with io.open(log, 'w', encoding='utf-8') as f:
    r = subprocess.run(['osascript', '-l', 'JavaScript', cap], stdout=f, stderr=subprocess.STDOUT)
print(io.open(log, encoding='utf-8').read()[-800:])
if r.returncode != 0:
    raise SystemExit('capture failed (exit %d), see %s' % (r.returncode, log))
dj = os.path.join(out, 'display%s.json' % tag)
subprocess.run([sys.executable, os.path.join(TOOLS, 'audit.py'), dj])
subprocess.run([sys.executable, os.path.join(TOOLS, 'raster.py'), dj, os.path.join(out, 'png' + tag)])
