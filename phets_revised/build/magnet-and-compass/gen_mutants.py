#!/usr/bin/env python3
"""gen_mutants.py -- the mutation list for magnet-and-compass.html.

The engine's mutants are the family's, kept in
build/magnets-and-electromagnets/gen_mutants.py: this takes the ones whose text is
actually in THIS page (the electromagnet's are not, the build having stripped it) and
adds the mutants for this page's own controls.  Anything that matches other than exactly
once is reported here rather than left for mutate.py to skip in silence.

    python3 gen_mutants.py
"""
import importlib.util
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY = os.path.join(os.path.dirname(HERE), 'magnets-and-electromagnets')
PAGE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'magnet-and-compass.html')

spec = importlib.util.spec_from_file_location('fam_mut', os.path.join(FAMILY, 'gen_mutants.py'))
fam = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fam)

html = io.open(PAGE, encoding='utf-8').read()
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]

MINE = [  # ---- this page's own controls ----
    ('the H curve is drawn only inside the magnet',
     "      for(const [a0,a1] of [[-C.xr,-MAG_B],[-MAG_B,MAG_B],[MAG_B,C.xr]]){",
     "      for(const [a0,a1] of [[-C.xr,C.xr]]){", 'p'),
    ('the analysis toggles are dimmed where they do nothing',
     "rows.cb_bound.inp.disabled=(v!=='lines'); rows.cb_axisH.inp.disabled=(v!=='axis');",
     "rows.cb_bound.inp.disabled=false; rows.cb_axisH.inp.disabled=false;", 'u'),
    ('the unit chips reach the readout', "function fB(v){ return fmtField(v,ST.units); }",
     "function fB(v){ return fmtField(v,'G'); }", 'u'),
    ("the panel hides the other views' groups", 'for(const g of [gBar,gTools,gShow,gNd]) g.hidden=groups[v].indexOf(g)<0;',
     'for(const g of [gBar,gTools,gShow,gNd]) g.hidden=false;', 'u'),
]

out, dropped, bad = [], [], []
for lab, old, new in fam.P:
    n = js.count(old)
    if n == 0:
        dropped.append(lab)
    elif n == 1:
        out.append([lab, old, new, 'p'])
    else:
        bad.append((lab, n))
for lab, old, new in fam.U:
    n = js.count(old)
    if n == 0:
        dropped.append(lab)
    elif n == 1:
        out.append([lab, old, new, 'u'])
    else:
        bad.append((lab, n))
for lab, old, new, suite in MINE:
    n = js.count(old)
    if n != 1:
        bad.append((lab, n))
    else:
        out.append([lab, old, new, suite])

io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(out, indent=1))
print('mutants.json: %d mutants (%d physics, %d UI)' % (len(out), sum(1 for m in out if m[3] == 'p'), sum(1 for m in out if m[3] == 'u')))
print('   not in this page (the electromagnet is stripped): %d -- %s' % (len(dropped), ', '.join(dropped)))
if bad:
    raise SystemExit('patterns that do not match exactly once: %s' % bad)
