#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/keplers-laws.html and
extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).

Shared with my-solar-system.html, whose assemble.py reads these from here so the
family has one engine: p1_utils.js, p2_engine.js, p4a_helpers.js, p4b_kit.js."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
out_html = os.path.normpath(os.path.join(here, '..', '..', 'keplers-laws.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_engine.js', 'p2_ref_kl.js', 'p2_kl.js', 'p3_state.js',
         'p4a_helpers.js', 'p4b_kit.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('keplers-laws.html: %d lines, %d bytes; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
