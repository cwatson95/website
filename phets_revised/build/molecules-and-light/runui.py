#!/usr/bin/env python3
"""Build _out/ui_run.js (run.js + the UI drive) and run it under osascript."""
import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
body = io.open(os.path.join(out, 'run.js'), encoding='utf-8').read()
body += '\n' + io.open(os.path.join(here, 'ui_drive_molecules-and-light.js'), encoding='utf-8').read()
p = os.path.join(out, 'ui_run.js')
io.open(p, 'w', encoding='utf-8').write(body)
r = subprocess.run(['osascript', '-l', 'JavaScript', p], capture_output=True, text=True, timeout=1800)
sys.stdout.write(r.stdout)
sys.stderr.write(r.stderr)
print('exit', r.returncode)
sys.exit(r.returncode)
