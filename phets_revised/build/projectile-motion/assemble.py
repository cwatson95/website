#!/usr/bin/env python3
"""Concatenate the part files into ../../projectile-motion.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log)."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out_html = os.path.abspath(os.path.join(here, '..', '..', 'projectile-motion.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_physics.js', 'p3_state.js', 'p4_views.js',
         'p5_views.js', 'p6_boot.js', 'p7a_refs.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
# a copy beside the harness scratch, so tools/mutate.py writes its _mutant.js
# into _out/ and not into the shared docs/phets_revised/ directory
io.open(os.path.join(here, '_out', 'projectile-motion.html'), 'w', encoding='utf-8').write(html)
print('%s: %d lines, %d bytes; run.js: %d lines' % (out_html, len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
