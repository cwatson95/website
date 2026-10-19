#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/circuit-construction-kit-dc-virtual-lab.html
and extract _out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log).
Run make_head.py first whenever p0_top.html or the house scaffold changes, and
derive.py whenever the presets or the references change (it writes
p2_presets.js and p7_refs.js)."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'circuit-construction-kit-dc-virtual-lab.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_presets.js', 'p2_circuit.js', 'p3_state.js', 'p4a_helpers.js',
         'p4_lab.js', 'p5_views.js', 'p6_boot.js', 'p7_refs.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
assert 'fetch(' not in html and 'XMLHttpRequest' not in html
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines' % (os.path.basename(sim), len(html.splitlines()),
                                                   len(html.encode('utf-8')), len(js.splitlines())))
