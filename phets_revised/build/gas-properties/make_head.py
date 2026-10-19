#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; (the CSS, the site-nav block, the body markup).
             Edited: the :root role-colour comment, <h1>, .sub, and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils    : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
             layer with every Known-bad fix: throwing toRgb, plain() that strips
             tags and decodes numeric entities inside the wide match,
             Liang-Barsky polyline, range-sorting axes, guarded logTicks,
             recorded legends).
  helpers  : projects/simulations/build_buoy/p4_views.js from its top to the
             first buoyancy-specific helper (its banner: taken from
             build_cycloid/p4_views.js unchanged): worldFitUp, lab/axesR and
             the label registry, stageLayout, marker.
"""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
sims = os.path.join(root, 'projects', 'simulations')
lagr = os.path.join(sims, 'build_lagr')

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
            """    /* role colours: green = the computed thing (the measured histogram, the
       simulated trace), orange = the reference/analytic law (Maxwell-Boltzmann,
       the adiabat, PhET's gauge) or a warning, magenta = the live marker (the
       state now, the handle being dragged), cyan = structure (the box, the
       walls, the axes).  The two species have their own colour slots
       (COL.heavy, COL.light) rather than borrowing a role colour. */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Gas properties</h1>')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + ('<span class="sub" id="sub">Hard disks in a box, collision by collision &mdash; PhET&rsquo;s '
                    'ideal gas law, working wall, energy histograms and diffusion, and where the gauge&rsquo;s '
                    'pressure and the Maxwell&ndash;Boltzmann law come from</span>') + body[j1:]
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

top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
utils = utils.replace('/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html)                    *',
                      '/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html, via                 *\n *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
assert 'function polyline(' in utils and 'function legendAuto(' in utils and 'function plain(' in utils
io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

buoy = io.open(os.path.join(sims, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
hcut = buoy.index('/* the fluid: a translucent slab')
helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                              'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function worldFitUp(' in helpers
io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)
print('p1_head.html: %d lines (scaffold %d from build_lagr); p1_utils.js: %d lines; p4a_helpers.js: %d lines'
      % (len((top + body).splitlines()), len(body.splitlines()), len(utils.splitlines()), len(helpers.splitlines())))
