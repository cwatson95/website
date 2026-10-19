#!/usr/bin/env python3
"""A fast FIRST pass of the mutation sweep, for iterating only.

Identical in logic to projects/simulations/tools/mutate.py — same mutants.json, same
exactly-once pattern rule, same caught-is-a-non-zero-exit rule — but it runs the physics
suite under jsc, which is about fourteen times faster than osascript and is the house's
iterating loop (Known-bad: "jsc has no console.log ... osascript remains the final pass").
UI mutants need ObjC.import and are left to the real tool.

    python3 sweep_jsc.py [label substring ...]

The authoritative sweep is still tools/mutate.py on a copy inside _out/; this only finds the
survivors sooner.  It proves the runner can see a failure before trusting any green."""
import io, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, '_out')
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
SIM = os.path.join(OUTD, 'sim_for_mutants.html')
TMP = os.path.join(OUTD, '_mutant_jsc.js')


def extract(path):
    s = io.open(path, encoding='utf-8').read()
    return s.split('<script>', 1)[1].rsplit('</script>', 1)[0]


def run(js):
    io.open(TMP, 'w', encoding='utf-8').write('var console={log:print};\n' + js)
    p = subprocess.run([JSC, TMP], capture_output=True, text=True, timeout=1800)
    return p.returncode, p.stdout + p.stderr


base = extract(SIM)
want = sys.argv[1:]
mutants = [m for m in json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
           if m[3] == 'p' and (not want or any(w in m[0] for w in want))]

rc, out = run(base)
print('BASELINE physics:', out.strip().splitlines()[-1] if out.strip() else '(silent)', flush=True)
if rc != 0:
    print('baseline is RED — fix that before mutating anything')
    sys.exit(1)
# prove the runner can see a failure before trusting a single green line
rc_bad, _ = run(base.replace('const U_FULL=2.14;', 'const U_FULL=2.05;'))
assert rc_bad != 0, 'the runner cannot see a failing suite: a green sweep would mean nothing'
print('runner check: a hand-broken constant exits %d, so caught-vs-survived is meaningful' % rc_bad, flush=True)

caught, survived, skipped, t0 = 0, [], [], time.time()
for label, old, new, suite in mutants:
    n = base.count(old)
    if n != 1:
        skipped.append((label, n))
        print('SKIP    %-44s (pattern appears %d times)' % (label, n), flush=True)
        continue
    rc, _ = run(base.replace(old, new))
    if rc != 0:
        caught += 1
        print('caught    %s' % label, flush=True)
    else:
        survived.append(label)
        print('SURVIVED  *** %s ***' % label, flush=True)
try:
    os.remove(TMP)
except OSError:
    pass
print('\n%d caught, %d survived, %d skipped  (%.0f s)' % (caught, len(survived), len(skipped), time.time() - t0))
for s in survived:
    print('   SURVIVOR:', s)
for s, n in skipped:
    print('   SKIPPED :', s, '(count %d)' % n)
sys.exit(0 if not survived and not skipped else 3)
