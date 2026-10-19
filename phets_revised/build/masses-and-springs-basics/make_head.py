#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold  : projects/simulations/build_lagr/p1_head.html, from <style> to
              'use strict'; — the CSS, the site-nav block and the body markup.
              Edited: the :root role-colour comment, <h1>, .sub, and the seven
              site-nav hrefs (absolute: the relative ../website/ links are dead
              from docs/phets_revised/).  Everything else is byte-identical.
  utils     : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
              layer with every Known-bad fix: throwing toRgb, plain() that
              strips tags and decodes numeric entities inside the wide match,
              Liang-Barsky polyline, range-sorting axes, guarded logTicks,
              recorded legends).
  helpers   : projects/simulations/build_buoy/p4_views.js up to its first
              buoyancy-specific helper — axesR, lab, legendAuto, worldFitUp.
"""
import io, os

here = os.path.dirname(os.path.abspath(__file__))
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
            """    /* role colours: green = the computed thing (the springs, the motion, the
       measured period), orange = the reference/analytic value (mg/k, 2 pi
       sqrt(m/k), the closed form) or a warning, magenta = the live marker (the
       hanging mass, the clock hand, the current setting), cyan = structure
       (the ceiling, the rulers, the frames, the lines). */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Masses and springs</h1>')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + ('<span class="sub" id="sub">Hang a mass on a spring and it stretches by mg/k; let go and it bounces at '
                    '2&pi;&radic;(m/k) whatever the gravity &mdash; PhET&rsquo;s three screens, with the damped oscillator '
                    'in closed form, its three regimes and its energy</span>') + body[j1:]
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
for need in ('function toRgb(', 'function plain(', 'function polyline(', 'function axes(',
             'function caption(', 'function wrapText(', 'function fmt(', 'function sigf(',
             'function ticksFor(', 'const clamp=', 'function legendAuto(', 'function h(tag'):
    assert need in utils, need
io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

buoy = io.open(os.path.join(root, 'projects', 'simulations', 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
hcut = buoy.index('/* the fluid: a translucent slab')
helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                              'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
for need in ('function axesR(', 'function lab(', 'function worldFitUp('):
    assert need in helpers, need
io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

print('p1_head.html: %d lines (scaffold %d from build_lagr)' % (len((top + body).splitlines()), len(body.splitlines())))
print('p1_utils.js: %d lines   p4a_helpers.js: %d lines' % (len(utils.splitlines()), len(helpers.splitlines())))
