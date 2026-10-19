#!/usr/bin/env python3
"""Where may the head/tail join sit?  Run the selfTest (jsc) with X_JOIN moved, to measure the window
inside which the choice is an EQUIVALENT mutant (both branches accurate) rather than assume it."""
import io, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc'
src = io.open(os.path.join(HERE, '_out', 'run_jsc.js'), encoding='utf-8').read()
old = 'const X_JOIN=2, BERN_N=40;'
assert src.count(old) == 1
for xj in ['0.005', '0.01', '0.02', '0.05', '0.5', '4', '5', '5.5', '6', '6.5', '7']:
    tmp = os.path.join(HERE, '_out', '_join.js')
    io.open(tmp, 'w', encoding='utf-8').write(src.replace(old, 'const X_JOIN=%s, BERN_N=40;' % xj))
    r = subprocess.run([JSC, tmp], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    fails = [l for l in out if l.startswith('FAIL')]
    summ = [l for l in out if 'passed' in l]
    print('X_JOIN=%-6s exit %d  %s  %s' % (xj, r.returncode, summ[-1] if summ else '?', (fails[0][:110] if fails else '')))
os.remove(os.path.join(HERE, '_out', '_join.js'))
