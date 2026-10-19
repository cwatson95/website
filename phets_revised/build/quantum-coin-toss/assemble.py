#!/usr/bin/env python3
"""Concatenate docs/phets_revised/quantum-coin-toss.html from this sim's own
parts and the engine it shares with quantum-measurement.html, READ FROM
build/quantum-measurement/ so the two files cannot drift (the same code, trimmed
to PhET's Coins screen); extract _out/run.js (osascript) and _out/run_jsc.js
(jsc).  The head comes from ../quantum-measurement/make_head.py:
    python3 ../quantum-measurement/make_head.py . "Quantum coin toss" "<sub html>"
"""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
qm = os.path.join(here, '..', 'quantum-measurement')
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'quantum-coin-toss.html'))
parts = [(here, 'p1_head.html'), (qm, 'p1_utils.js'), (qm, 'p2_engine.js'), (qm, 'p4a_helpers.js'), (qm, 'p4c_common.js'),
         (here, 'p3_state.js'), (qm, 'p4_coins.js'), (qm, 'p5_binom.js'), (here, 'p5_mix.js'), (here, 'p5_scene.js'),
         (here, 'p6_boot.js'), (qm, 'p7a_lib.js'), (here, 'p7_test.js')]
html = ''.join(io.open(os.path.join(d, fn), encoding='utf-8').read() for d, fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines' % (os.path.basename(sim), len(html.splitlines()),
                                                    len(html.encode('utf-8')), len(js.splitlines())))
