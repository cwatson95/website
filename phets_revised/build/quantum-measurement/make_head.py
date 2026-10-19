#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

    python3 make_head.py                      # quantum-measurement (this dir)
    python3 make_head.py <build-dir> <h1> <sub-html>   # a family member

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; -- the CSS, the site-nav block and the body markup.
             Edited: the :root role-colour comment, <h1>, .sub, and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils    : projects/simulations/build_lagr/p1_utils.js, verbatim (every
             Known-bad fix: throwing toRgb, plain() that strips tags and
             decodes numeric entities inside the wide match, Liang-Barsky
             polyline, range-sorting axes, guarded logTicks, recorded legends).
  helpers  : projects/simulations/build_buoy/p4_views.js from its top to the
             first buoyancy-specific helper (the label registry, axesR,
             worldFitUp, stageLayout ...), which build_buoy took from
             build_cycloid unchanged.
The p0_top.html of the target build dir (doctype, <title>, header comment)
is prepended.
"""
import io, os, sys

here = os.path.dirname(os.path.abspath(__file__))
target = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else here
H1 = sys.argv[2] if len(sys.argv) > 2 else 'Quantum measurement'
SUB = sys.argv[3] if len(sys.argv) > 3 else (
    'Coins, photons, spins and the Bloch sphere &mdash; a classical coin has a face before you look, '
    'a quantum one has amplitudes, and the Born rule turns them into odds only when you measure')
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
lagr = os.path.join(root, 'projects', 'simulations', 'build_lagr')

src = io.open(os.path.join(lagr, 'p1_head.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
body = src[i:k]


def sub1(s, old, new):
    assert s.count(old) == 1, (old, s.count(old))
    return s.replace(old, new)


body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""",
            """    /* role colours: green = the computed or measured thing (the counts, the
       outcome +, the state vector), orange = the reference/analytic law (the
       Born rule, the binomial) or a warning, magenta = the live marker (the
       particle in flight, the angle cursor), cyan = structure (apparatus,
       axes, the sphere).  The second outcome (tails, down, H) is violet. */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>%s</h1>' % H1)
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + '<span class="sub" id="sub">%s</span>' % SUB + body[j1:]
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

top = io.open(os.path.join(target, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(target, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

if target == here:
    utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    utils = utils.replace('/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html)                    *',
                          '/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html, via                 *\n *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
    assert 'function polyline(' in utils and 'function legendAuto(' in utils and 'function fitCaption(' in utils
    io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)
    buoy = io.open(os.path.join(root, 'projects', 'simulations', 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
    hcut = buoy.index('/* the fluid: a translucent slab')
    helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function worldFitUp(' in helpers
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)
    print('p1_utils.js: %d lines   p4a_helpers.js: %d lines' % (len(utils.splitlines()), len(helpers.splitlines())))
print('%s/p1_head.html: %d lines' % (os.path.basename(target), len((top + body).splitlines())))
