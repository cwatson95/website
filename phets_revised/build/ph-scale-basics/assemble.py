#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/ph-scale-basics.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log).

This build is PhET's Macro screen as its own sim, on the SAME engine as ph-scale: the
chemistry (p2_chem.js), the state and the readout (p3_state.js), and the three shared views
(p4_views.js) come from build/ph-scale/ BY PATH and are never written to here, as do the
reference values derive.py printed (p7_refs.js).  The house utilities (p1_utils.js), the
2-D drawing layer (p4_helpers.js) and the selfTest's recording context (p7_shot.js) come
from build/wave-interference/ the same way.  Every one of those seven has its SHA-256
pinned below, so a change in either directory cannot reach this sim unnoticed.

What differs from ph-scale, and all that differs: this head, the sim's identity
(p2b_id.js: four tabs, and PhET's Basics prints no concentrations), the one extra view
(p5b_views.js, the table of the twelve liquids), the boot (its own controls, captions and
dispatch) and its own suite."""
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')
PS = os.path.join(HERE, '..', 'ph-scale')
OUT = os.path.dirname(os.path.dirname(HERE))               # docs/phets_revised
SHA = {
    'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
    'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc',
    'p7_shot.js': 'e10d16351fd35beecf22f7fb39bc6890019353178034f0336d8aff4c865f8262',
    'p2_chem.js': 'e677c0fc0da963aad57947df61c830e6ed754dd9a5be479ec8dcf674883c001a',
    'p3_state.js': 'da0d4d97c57af26a17e5c84fffb9c04db8d21945975237d49dec08eaf72308a8',
    'p4_views.js': 'a87228305f0b5d1de01c46b8f3739d8864c4ec7a4900a27844545fb66bb5c10e',
    'p7_refs.js': '7a77aff690c1b787234290e3004ae5f27d17ec1e1462702d77f533dff7504e28',
}
PARTS = [(HERE, 'p1_head.html'), (WI, 'p1_utils.js'), (PS, 'p2_chem.js'),
         (HERE, 'p2b_id.js'), (PS, 'p3_state.js'), (WI, 'p4_helpers.js'),
         (PS, 'p4_views.js'), (HERE, 'p5b_views.js'), (HERE, 'p6_boot.js'),
         (PS, 'p7_refs.js'), (WI, 'p7_shot.js'), (HERE, 'p7_test.js')]

html = ''
for d, fn in PARTS:
    body = io.open(os.path.join(d, fn), encoding='utf-8').read()
    if d != HERE:
        got = hashlib.sha256(body.encode('utf-8')).hexdigest()
        assert got == SHA[fn], '%s/%s has changed (%s)' % (os.path.basename(d), fn, got)
    html += body
html += '</script>\n</body>\n</html>\n'
io.open(os.path.join(OUT, 'ph-scale-basics.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
io.open(os.path.join(HERE, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(HERE, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
print('ph-scale-basics.html: %d lines, %.1f KB; run.js: %d lines' %
      (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines())))
