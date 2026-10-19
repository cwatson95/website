#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/waves-intro.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log).

Five parts come from build/wave-interference/ BY PATH and are never written to: the house
utilities and 2-D drawing layer, the CIE table its derive.py wrote, the selfTest's recording
context, and — the point of the exercise — p2_engine.js, the lattice engine whose API is that
build's ENGINE.md and whose proof is its derive.py.  Their SHA-256s are pinned below, so that a
change over there cannot reach this sim unnoticed."""
import hashlib, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')
OUT = os.path.dirname(os.path.dirname(HERE))                # docs/phets_revised
WI_SHA = {
    'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
    'p2_cie.js': '6b6b7be2dc4d487ffc202775a8f2c0d4c9708e7ee06855c232a7e643a31cbc2d',
    'p2_engine.js': '393cdd8f1d6067a960b7c85726876c78eefa604ba6e7802f243dfab630b1dc66',
    'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc',
    'p7_shot.js': 'e10d16351fd35beecf22f7fb39bc6890019353178034f0336d8aff4c865f8262',
}
PARTS = [(HERE, 'p1_head.html'), (WI, 'p1_utils.js'), (WI, 'p2_cie.js'), (HERE, 'p2_parts.js'),
         (WI, 'p2_engine.js'), (HERE, 'p2_intro.js'), (HERE, 'p3_state.js'), (WI, 'p4_helpers.js'),
         (HERE, 'p4_draw.js'), (HERE, 'p4_views.js'), (HERE, 'p6_boot.js'), (HERE, 'p7_refs.js'),
         (WI, 'p7_shot.js'), (HERE, 'p7_test.js')]

html = ''
for d, fn in PARTS:
    body = io.open(os.path.join(d, fn), encoding='utf-8').read()
    if d == WI:
        got = hashlib.sha256(body.encode('utf-8')).hexdigest()
        assert got == WI_SHA[fn], 'build/wave-interference/%s has changed (%s)' % (fn, got)
    html += body
html += '</script>\n</body>\n</html>\n'
io.open(os.path.join(OUT, 'waves-intro.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
io.open(os.path.join(HERE, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(HERE, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('waves-intro.html: %d lines, %.1f KB; run.js: %d lines' %
      (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines())))
