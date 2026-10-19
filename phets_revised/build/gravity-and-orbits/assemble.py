#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/gravity-and-orbits.html
and extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).

The engine and the shared drawing layers are read from ../keplers-laws/ -- one
source for the three sims of this family (keplers-laws, my-solar-system,
gravity-and-orbits), so they cannot drift: p1_utils.js, p2_engine.js,
p4a_helpers.js, p4b_kit.js.  Sim-specific (here): p1_head.html, p2_ref_go.js,
p2_go.js, p3_state.js, p4_views.js, p5_views.js, p6_boot.js, p7_test.js."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
kl = os.path.normpath(os.path.join(here, '..', 'keplers-laws'))
out_html = os.path.normpath(os.path.join(here, '..', '..', 'gravity-and-orbits.html'))
parts = [(here, 'p1_head.html'), (kl, 'p1_utils.js'), (kl, 'p2_engine.js'), (here, 'p2_ref_go.js'),
         (here, 'p2_go.js'), (here, 'p3_state.js'), (kl, 'p4a_helpers.js'), (kl, 'p4b_kit.js'),
         (here, 'p4_views.js'), (here, 'p5_views.js'), (here, 'p6_boot.js'), (here, 'p7a_shot.js'),
         (here, 'p7_test.js')]
html = ''.join(io.open(os.path.join(d, fn), encoding='utf-8').read() for d, fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('gravity-and-orbits.html: %d lines, %d bytes; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
