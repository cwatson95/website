#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/charges-and-fields.html
and extract _out/run.js (osascript) and _out/run_jsc.js (jsc, which has no
console.log).  Regenerates p7_refs.js from refvals.txt first, so the suite
always asserts against derive.py's latest printed output."""
import io
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
out_html = os.path.abspath(os.path.join(here, '..', '..', 'charges-and-fields.html'))
subprocess.run([sys.executable, os.path.join(here, 'gen_refs.py')], check=True)
parts = ['p1_head.html', 'p1_utils.js', 'p2_physics.js', 'p3_state.js', 'p4_helpers.js', 'p4_views.js',
         'p5_views.js', 'p6_boot.js', 'p7_refs.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %.1f KB; run.js %d lines' % (os.path.basename(out_html), len(html.splitlines()), len(html.encode()) / 1024,
                                                  len(js.splitlines())))
