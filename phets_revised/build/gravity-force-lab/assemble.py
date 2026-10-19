#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/gravity-force-lab.html and
extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).

Shared with coulombs-law.html (its assemble.py reads these from here, so the
engine has one source): p1_utils.js, p2_engine.js, p4_helpers.js, p4_lab.js,
p7_kit.js, p7_sweep.js.  Sim-specific: p1_head.html, p2_gfl.js, p3_state.js,
p5_views.js, p6_boot.js, p8_test.js."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out_html = os.path.normpath(os.path.join(here, '..', '..', 'gravity-force-lab.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_engine.js', 'p2_gfl.js', 'p3_state.js', 'p4_helpers.js',
         'p4_lab.js', 'p5_views.js', 'p6_boot.js', 'p7_kit.js', 'p7_sweep.js', 'p8_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('gravity-force-lab.html: %d lines, %d bytes; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
