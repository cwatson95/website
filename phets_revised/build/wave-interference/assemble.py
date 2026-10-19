#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/wave-interference.html and extract
_out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log)."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
outdir = os.path.dirname(os.path.dirname(here))            # docs/phets_revised
parts = ['p1_head.html', 'p1_utils.js', 'p2_cie.js', 'p2_ext.js', 'p2_engine.js', 'p2_optics.js',
         'p3_state.js', 'p4_helpers.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js',
         'p7_refs.js', 'p7_shot.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(os.path.join(outdir, 'wave-interference.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('wave-interference.html: %d lines, %.1f KB; run.js: %d lines' %
      (len(html.splitlines()), len(html.encode('utf-8')) / 1024, len(js.splitlines())))
