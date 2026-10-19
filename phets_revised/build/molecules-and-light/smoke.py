#!/usr/bin/env python3
"""Scratch: build a physics-only bundle and run it under jsc."""
import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
parts = ['p1_utils.js', 'p2a_data.js', 'p2b_fields.js', 'p2_physics.js']
body = 'var console={log:print};\n'
for fn in parts:
    body += io.open(os.path.join(here, fn), encoding='utf-8').read()
body += io.open(os.path.join(here, 'smoke_tail.js'), encoding='utf-8').read()
p = os.path.join(out, 'smoke.js')
io.open(p, 'w', encoding='utf-8').write(body)
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
r = subprocess.run([JSC, p], capture_output=True, text=True, timeout=600)
sys.stdout.write(r.stdout)
sys.stderr.write(r.stderr)
sys.exit(r.returncode)
