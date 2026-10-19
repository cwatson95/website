#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/quantum-measurement.html
and extract _out/run.js (osascript) and _out/run_jsc.js (jsc, which has no
console.log).  Run make_head.py first whenever p0_top.html or the house
scaffold changes.  The engine and the shared views (SHARED) are also read by
build/quantum-coin-toss/assemble.py, so the two files cannot drift."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'quantum-measurement.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_engine.js', 'p4a_helpers.js', 'p4c_common.js', 'p4b_3d.js',
         'p3_state.js', 'p4_coins.js', 'p4_photons.js', 'p5_spins.js', 'p5_bloch.js', 'p5_born.js',
         'p5_binom.js', 'p5_scene.js', 'p6_boot.js', 'p7a_lib.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines' % (os.path.basename(sim), len(html.splitlines()),
                                                    len(html.encode('utf-8')), len(js.splitlines())))
