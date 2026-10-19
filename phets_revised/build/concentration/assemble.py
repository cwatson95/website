#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/concentration.html.

PhET ships Concentration as the Concentration screen of Beer's Law Lab on its own, so this
sim is the same engine trimmed to that screen.  Every part but two comes from
build/beers-law-lab/ BY PATH and is never written to here -- the data, the chemistry, the
state, the beaker, the ledger and colour views, the solutes view, boot and the suite are
literally the same bytes, and `SHOW_BEERS` (set in this directory's p2b_id.js) is what
switches the cuvette off.  Only p1_head.html (this sim's own header and tagline) and
p2b_id.js (its identity and its four tabs) are local.

The three house files come from build/wave-interference/ and are SHA-pinned.  The shared
parts are not pinned: they are this family's own, both sims are built together, and a
divergence would show up as a red suite on the next assemble rather than as a silent drift.
"""
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BLL = os.path.join(HERE, '..', 'beers-law-lab')
WI = os.path.join(HERE, '..', 'wave-interference')
OUT = os.path.dirname(os.path.dirname(HERE))               # docs/phets_revised
WI_SHA = {
    'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
    'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc',
    'p7_shot.js': 'e10d16351fd35beecf22f7fb39bc6890019353178034f0336d8aff4c865f8262',
}
PARTS = [(HERE, 'p1_head.html'), (WI, 'p1_utils.js'), (BLL, 'p2_data.js'),
         (BLL, 'p2_chem.js'), (HERE, 'p2b_id.js'), (BLL, 'p3_state.js'),
         (WI, 'p4_helpers.js'), (BLL, 'p4_views.js'), (BLL, 'p5_views.js'),
         (BLL, 'p5c_solutes.js'), (BLL, 'p6_boot.js'), (BLL, 'p7_refs.js'),
         (WI, 'p7_shot.js'), (BLL, 'p7_test.js')]

html = ''
for d, fn in PARTS:
    body = io.open(os.path.join(d, fn), encoding='utf-8').read()
    if d == WI:
        got = hashlib.sha256(body.encode('utf-8')).hexdigest()
        assert got == WI_SHA[fn], 'build/wave-interference/%s has changed (%s)' % (fn, got)
    html += body
html += '</script>\n</body>\n</html>\n'
io.open(os.path.join(OUT, 'concentration.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
io.open(os.path.join(HERE, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(HERE, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
# the UI drive is the same harness, guarded by SHOW_BEERS; verify_one.py insists on the
# name ui_drive_<stem>.js, so it is COPIED rather than shared by path, and the copy is
# rewritten here every time so the two cannot drift apart unnoticed
src = io.open(os.path.join(BLL, 'ui_drive_beers-law-lab.js'), encoding='utf-8').read()
io.open(os.path.join(HERE, 'ui_drive_concentration.js'), 'w', encoding='utf-8').write(src)
print('concentration.html: %d lines, %.1f KB; run.js: %d lines; ui drive copied (%d lines)' %
      (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines()),
       len(src.splitlines())))
