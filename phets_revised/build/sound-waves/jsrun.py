#!/usr/bin/env python3
"""Run the assembled script with a tail appended, under jsc (fast) or osascript.

    python3 jsrun.py <tail.js> [jsc|osa] [nosuite]

jsc runs the physics suite many times faster than osascript and is the right loop for
iterating; osascript is the final pass (and the only one the UI harness can use: it needs
ObjC.import).  Writes _out/<tail stem>_run.js next to run.js."""
import io
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '_out')
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
tail = sys.argv[1] if len(sys.argv) > 1 else ''
engine = sys.argv[2] if len(sys.argv) > 2 else 'jsc'
body = io.open(os.path.join(OUTD, 'run.js'), encoding='utf-8').read()
if 'nosuite' in sys.argv[3:]:
    assert body.count('\n  selfTest();\n') == 1
    body = body.replace('\n  selfTest();\n', '\n  /* suite skipped for this run */\n')
extra = ''
if tail:
    extra = io.open(tail if os.path.isabs(tail) else os.path.join(HERE, tail), encoding='utf-8').read()
stem = os.path.splitext(os.path.basename(tail))[0] if tail else 'plain'
path = os.path.join(OUTD, stem + '_run.js')
io.open(path, 'w', encoding='utf-8').write(
    ('var console={log:print};\n' if engine == 'jsc' else '') + body + '\n' + extra)
t0 = time.time()
cmd = [JSC, path] if engine == 'jsc' else ['osascript', '-l', 'JavaScript', path]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
sys.stdout.write(r.stdout)
sys.stderr.write(r.stderr)
print('[%s exit %d, %.1f s]' % (engine, r.returncode, time.time() - t0))
sys.exit(r.returncode)
