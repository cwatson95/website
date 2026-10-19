#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/bending-light.html and
extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).
Run make_head.py first whenever p0_top.html or the house scaffold changes."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'bending-light.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_cie.js', 'p2_physics.js', 'p3_state.js',
         'p4a_helpers.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines'
      % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
