#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/calculus-grapher.html and
extract _out/run.js (for osascript / jsc).  Run make_head.py after changing
p0_top.html and make_refs.py after re-running derive.py.

p1_utils.js, p4_helpers.js and p7_shot.js are COPIES of
build/fourier-making-waves's, taken verbatim; their SHA-256 is checked here in
both directions so neither side can drift."""
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FMW = os.path.join(HERE, '..', 'fourier-making-waves')
OUT = os.path.dirname(os.path.dirname(HERE))                    # docs/phets_revised
PINS = {'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
        'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc',
        'p7_shot.js': 'e10d16351fd35beecf22f7fb39bc6890019353178034f0336d8aff4c865f8262'}
PARTS = ['p1_head.html', 'p1_utils.js', 'p2_calculus.js', 'p3_state.js', 'p4_helpers.js',
         'p4_views.js', 'p5_views.js', 'p6_boot.js', 'p7_refs.js', 'p7_shot.js', 'p7_test.js']


def sha(p):
    return hashlib.sha256(io.open(p, encoding='utf-8').read().encode('utf-8')).hexdigest()


for fn, want in PINS.items():
    assert sha(os.path.join(HERE, fn)) == want, '%s has been edited here' % fn
    assert sha(os.path.join(FMW, fn)) == want, 'build/fourier-making-waves/%s changed upstream' % fn

html = ''.join(io.open(os.path.join(HERE, fn), encoding='utf-8').read() for fn in PARTS)
html += '</script>\n</body>\n</html>\n'
sim = os.path.join(OUT, 'calculus-grapher.html')
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
io.open(os.path.join(HERE, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
print('calculus-grapher.html: %d lines, %.1f KB; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines())))
