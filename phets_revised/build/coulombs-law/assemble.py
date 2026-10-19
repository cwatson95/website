#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/coulombs-law.html and
extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).

The inverse-square engine and the shared drawing/test layers are read from
../gravity-force-lab/ — one source for both sims, so they cannot drift:
p1_utils.js, p2_engine.js, p4_helpers.js, p4_lab.js, p7_kit.js, p7_sweep.js.
Sim-specific (here): p1_head.html, p2_cl.js, p3_state.js, p5_views.js,
p6_boot.js, p8_test.js."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
gfl = os.path.normpath(os.path.join(here, '..', 'gravity-force-lab'))
out_html = os.path.normpath(os.path.join(here, '..', '..', 'coulombs-law.html'))
parts = [(here, 'p1_head.html'), (gfl, 'p1_utils.js'), (gfl, 'p2_engine.js'), (here, 'p2_cl.js'), (here, 'p3_state.js'),
         (gfl, 'p4_helpers.js'), (gfl, 'p4_lab.js'), (here, 'p5_views.js'), (here, 'p6_boot.js'),
         (gfl, 'p7_kit.js'), (gfl, 'p7_sweep.js'), (here, 'p8_test.js')]
html = ''.join(io.open(os.path.join(d, fn), encoding='utf-8').read() for d, fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('coulombs-law.html: %d lines, %d bytes; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
