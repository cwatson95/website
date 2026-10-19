#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/energy-forms-and-changes.html and
extract _out/run.js (osascript) and _out/run_jsc.js (jsc, which has no console.log).
Also writes _out/energy-forms-and-changes.html, the COPY the mutation sweep runs on
(tools/mutate.py writes its scratch _mutant.js beside the html it is given, so an
in-place sweep would share docs/phets_revised/_mutant.js with every parallel job).
Run make_head.py first whenever p0_top.html or the house scaffold changes, and
derive.py > refvals.txt; gen_refs.py whenever derive.py changes."""
import io, os
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'energy-forms-and-changes.html'))
parts = ['p1_head.html', 'p1_utils.js', 'p2_consts.js', 'p2_bench.js', 'p2_systems.js', 'p2_equil.js',
         'p3_state.js', 'p4a_helpers.js', 'p4_bench.js', 'p4_systems.js', 'p5_views.js', 'p6_boot.js',
         'p7a_refs.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
io.open(os.path.join(out, 'energy-forms-and-changes.html'), 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
print('%s: %d lines, %d bytes; run.js: %d lines' % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines())))
