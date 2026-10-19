#!/usr/bin/env python3
"""Scratch: run _out/dbg.js against the assembled sim under jsc."""
import io, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
body = io.open(os.path.join(out, 'jsc_run.js'), encoding='utf-8').read()
i = body.rindex('/* ============================== entry')
body = body[:i]
body += io.open(os.path.join(out, 'dbg.js'), encoding='utf-8').read()
p = os.path.join(out, 'dbg_run.js')
io.open(p, 'w', encoding='utf-8').write(body)
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
r = subprocess.run([JSC, p], capture_output=True, text=True, timeout=600)
sys.stdout.write(r.stdout)
sys.stderr.write(r.stderr)
sys.exit(r.returncode)
