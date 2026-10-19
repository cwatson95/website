#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/molecules-and-light.html
and extract _out/run.js for osascript/jsc.  Run make_head.py whenever
p0_top.html or the house scaffold changes, and derive.py + gen_ref.py whenever
the model changes."""
import io, os, sys
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'molecules-and-light.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2a_data.js', 'p2b_fields.js', 'p2_physics.js',
         'p3_state.js', 'p4a_helpers.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js',
         'p7a_ref.js', 'p7_test.js']
html = ''
for fn in parts:
    p = os.path.join(here, fn)
    if not os.path.isfile(p):
        print('MISSING ' + fn)
        sys.exit(2)
    html += io.open(p, encoding='utf-8').read()
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'jsc_run.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines'
      % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')),
         len(js.splitlines())))
