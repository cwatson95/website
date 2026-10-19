#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/molecule-polarity.html and
extract _out/run.js for osascript.  Run make_head.py whenever p0_top.html or the
house scaffold changes, and derive.py + gen_ref.py whenever the model changes."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'molecule-polarity.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2a_data.js', 'p2_physics.js', 'p3_state.js',
         'p4a_helpers.js', 'p4_views.js', 'p5_views.js', 'p6_boot.js', 'p7a_ref.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
print('%s: %d lines, %d bytes; run.js: %d lines'
      % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
