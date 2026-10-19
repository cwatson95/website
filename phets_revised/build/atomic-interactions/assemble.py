#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/atomic-interactions.html
and extract _out/run.js (osascript) and _out/run_jsc.js (jsc has no console.log).

p1_utils.js, p4_helpers.js, p7_kit.js and p7_sweep.js are copies of
build/gravity-force-lab/'s, taken verbatim so this build is self-contained;
everything else is this sim's.
"""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out_html = os.path.normpath(os.path.join(here, '..', '..', 'atomic-interactions.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_lj.js', 'p3_state.js', 'p4_helpers.js',
         'p4_draw.js', 'p5_views.js', 'p6_boot.js', 'p7_kit.js', 'p7_sweep.js',
         'p8_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(out_html, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
os.makedirs(os.path.join(here, '_out'), exist_ok=True)
io.open(os.path.join(here, '_out', 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(here, '_out', 'run_jsc.js'), 'w', encoding='utf-8').write(
    'var console={log:print};\n' + js)
print('atomic-interactions.html: %d lines, %d bytes; run.js: %d lines'
      % (len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
