#!/usr/bin/env python3
"""Concatenate the part files into docs/phets_revised/molecule-shapes-basics.html
and extract _out/run.js.

Molecule Shapes: Basics is the same engine as molecule-shapes.html, trimmed to
its screens and controls.  The engine parts (the model, the state, the renderer,
the two PhET screens, the table and the relaxation, the boot, the suite) are
COPIED HERE from ../molecule-shapes at build time and checked byte for byte, so
this directory is self-contained once built and cannot drift from its sibling.
What differs lives here: p0_top.html (the header), p3v_variant.js (no lone
pairs, four views, PhET's five Basics molecules), and the squeeze view, which
Basics does not carry, is simply left out of the parts list.

Run make_head.py (in ../molecule-shapes, with the argument `basics`) first
whenever p0_top.html or the house scaffold changes, and gen_ref.py basics
whenever derive.py's output changes."""
import filecmp, io, os, shutil

here = os.path.dirname(os.path.abspath(__file__))
full = os.path.abspath(os.path.join(here, '..', 'molecule-shapes'))
out = os.path.join(here, '_out')
os.makedirs(out, exist_ok=True)
sim = os.path.abspath(os.path.join(here, '..', '..', 'molecule-shapes-basics.html'))

SHARED = ['p1_utils.js', 'p2_physics.js', 'p3_state.js', 'p4a_helpers.js', 'p4_views.js',
          'p5_table.js', 'p5c_relax.js', 'p6_boot.js', 'p7_test.js']
for fn in SHARED:
    shutil.copyfile(os.path.join(full, fn), os.path.join(here, fn))
    assert filecmp.cmp(os.path.join(full, fn), os.path.join(here, fn), shallow=False), fn
OWN = ['p1_head.html', 'p3v_variant.js', 'p7a_ref.js']
for fn in OWN:
    assert os.path.isfile(os.path.join(here, fn)), 'missing %s (run make_head.py basics / gen_ref.py basics)' % fn

parts = ['p1_head.html', 'p1_utils.js', 'p2_physics.js', 'p3v_variant.js', 'p3_state.js', 'p4a_helpers.js',
         'p4_views.js', 'p5_table.js', 'p5c_relax.js', 'p6_boot.js', 'p7a_ref.js', 'p7_test.js']
html = ''.join(io.open(os.path.join(here, fn), encoding='utf-8').read() for fn in parts)
html += '</script>\n</body>\n</html>\n'
io.open(sim, 'w', encoding='utf-8').write(html)
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]
io.open(os.path.join(out, 'run.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(out, 'run_jsc.js'), 'w', encoding='utf-8').write('var console={log:print};\n' + js)
assert 'function drawSqueeze(' not in html, 'the squeeze view is not part of Basics'
print('%s: %d lines, %d bytes; run.js: %d lines (%d shared parts, byte-identical to ../molecule-shapes)'
      % (os.path.basename(sim), len(html.splitlines()), len(html.encode('utf-8')), len(js.splitlines()), len(SHARED)))
