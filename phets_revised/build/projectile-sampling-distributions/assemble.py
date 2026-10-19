#!/usr/bin/env python3
"""Concatenate the part files into
docs/phets_revised/projectile-sampling-distributions.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc: no console.log).
Run make_head.py, make_engine.py and make_views.py first whenever p0_top.html,
the house scaffold or the data lab's engine/picture layer changes, and
derive.py whenever a reference value changes (it writes p7a_refs.js)."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'projectile-sampling-distributions.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_engine.js', 'p3_state.js', 'p4a_helpers.js',
         'p4b_shared.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js', 'p7a_refs.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines'
      % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')),
         len(js.splitlines())))
