#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; -- the CSS, the site-nav block and the body markup.
             Edited: the :root role-colour comment, <h1>, .sub, and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils    : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
             layer with every Known-bad fix: throwing toRgb, plain() that strips
             tags and decodes numeric entities inside the wide match,
             Liang-Barsky polyline, range-sorting axes, guarded logTicks,
             recorded legends).
  helpers  : projects/simulations/build_buoy/p4_views.js from its top to the
             first buoyancy-specific helper (the label registry lab(), axesR,
             stageLayout, dot, seg ...), then the 3-D camera block of
             build_lagr/p4_views.js (v3, makeCamera, camBasis, project,
             boxCamera, poly3, seg3 -- pulsar.html's, unchanged).

Usage: python3 make_head.py [basics]   (the basics variant writes into
build/molecule-shapes-basics/ with its own p0_top.html, h1 and tagline)
"""
import io, os, sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
SIM = os.path.join(root, 'projects', 'simulations')
basics = len(sys.argv) > 1 and sys.argv[1] == 'basics'
dest = os.path.join(here, '..', 'molecule-shapes-basics') if basics else here

src = io.open(os.path.join(SIM, 'build_lagr', 'p1_head.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
body = src[i:k]


def sub1(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""",
            """    /* role colours: green = the computed thing (the relaxed shape's angles,
       the model's curves), orange = the reference (the ideal angle, the
       measured molecule) or a warning, magenta = the live marker (the pair
       being dragged, the current rho), cyan = structure (the lone pairs, the
       frames, the axes). */""")
if basics:
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Molecule shapes: basics</h1>')
    tagline = ('Two to six bonds round a central atom, pushing each other apart on a sphere until they settle into '
               'one of five shapes &mdash; linear, trigonal planar, tetrahedral, trigonal bipyramidal, octahedral &mdash; '
               'and five real molecules that have them')
else:
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Molecule shapes</h1>')
    tagline = ('Bonds and lone pairs round a central atom repel on a sphere and settle into their VSEPR shape '
               '&mdash; the AXE table, the measured molecules beside the model, and how far a lone pair bends a bond angle')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + '<span class="sub" id="sub">' + tagline + '</span>' + body[j1:]
NAV = [('../website/index.html', 'https://cooper-watson.net/index.html'),
       ('../website/about.html', 'https://cooper-watson.net/about.html'),
       ('../website/teaching.html', 'https://cooper-watson.net/teaching.html'),
       ('../modules/teaching_modules.html', 'https://cooper-watson.net/modules/teaching_modules.html'),
       ('../website/simulations.html', 'https://cooper-watson.net/simulations.html'),
       ('../website/research.html', 'https://cooper-watson.net/research.html'),
       ('../website/cv.html', 'https://cooper-watson.net/cv.html')]
for old, new in NAV:
    body = sub1(body, 'href="%s"' % old, 'href="%s"' % new)
assert 'href="../' not in body
assert 'aria-current="page"' in body

top = io.open(os.path.join(dest, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(dest, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

utils = io.open(os.path.join(SIM, 'build_lagr', 'p1_utils.js'), encoding='utf-8').read()
utils = utils.replace('/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html)                    *',
                      '/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html, via                 *\n *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
assert 'function plain(' in utils and 'function polyline(' in utils and 'function legendAuto(' in utils
io.open(os.path.join(dest, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

buoy = io.open(os.path.join(SIM, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
hcut = buoy.index('/* the fluid: a translucent slab')
helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                              'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function stageLayout(' in helpers
lagr = io.open(os.path.join(SIM, 'build_lagr', 'p4_views.js'), encoding='utf-8').read()
c0 = lagr.index('/* ---- 3-vector helpers, orbit camera, perspective projection')
c1 = lagr.index('function seg3(')
c1 = lagr.index('\n', c1) + 1
cam = lagr[c0:c1]
assert 'function makeCamera(' in cam and 'function camBasis(' in cam and 'function project(' in cam and 'function poly3(' in cam
helpers = helpers + '\n/* ---- the 3-D block, from build_lagr/p4_views.js ---- */\n' + cam
io.open(os.path.join(dest, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)
print('p1_head.html: %d lines   p1_utils.js: %d lines   p4a_helpers.js: %d lines (camera block %d)  -> %s'
      % (len((top + body).splitlines()), len(utils.splitlines()), len(helpers.splitlines()), len(cam.splitlines()), os.path.basename(os.path.abspath(dest))))
