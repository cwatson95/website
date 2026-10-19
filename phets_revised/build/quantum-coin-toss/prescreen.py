#!/usr/bin/env python3
"""Pre-screen this sim's physics mutants under jsc (about 0.3 s each) before
the official osascript sweep with tools/mutate.py.  Writes nothing but its log."""
import io, json, os, subprocess
here = os.path.dirname(os.path.abspath(__file__))
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
base = io.open(os.path.join(here, '_out', 'run_jsc.js'), encoding='utf-8').read()
muts = json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))
tmp = os.path.join(here, '_out', '_prescreen.js')
surv = []
for lab, old, new, kind in muts:
    if kind != 'p':
        continue
    assert base.count(old) == 1, lab
    io.open(tmp, 'w', encoding='utf-8').write(base.replace(old, new))
    r = subprocess.run([JSC, tmp], capture_output=True, text=True, timeout=600)
    caught = r.returncode != 0
    print(('caught   ' if caught else 'SURVIVED ') + lab, flush=True)
    if not caught:
        surv.append(lab)
os.remove(tmp)
print('\n%d survivors: %s' % (len(surv), surv))
