#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; (the CSS, the site-nav block, the body markup).
             Edited: the :root role-colour comment, <h1>, .sub, and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils    : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
             layer with every Known-bad fix: throwing toRgb, plain() that
             strips tags and decodes numeric entities inside the wide match,
             Liang-Barsky polyline, range-sorting axes, guarded logTicks,
             recorded legends).
  helpers  : projects/simulations/build_buoy/p4_views.js from its top to the
             first buoyancy-specific helper: worldFitUp, lab/axesR and the
             label registry, stageLayout, marker.

Usage:  python3 make_head.py [<stem>]     (default: this directory's stem)
The sibling build (projectile-sampling-distributions) passes its own stem and
takes its own p0_top.html and subtitle from the TITLES table below.
"""
import io
import os
import sys

TITLES = {
    'projectile-data-lab': (
        'Projectile data lab',
        'Launchers that scatter &mdash; PhET&rsquo;s variability, sources, measures and sampling '
        'screens, with the exact distribution of the landing distance and the central limit '
        'theorem derived rather than drawn'),
    'projectile-sampling-distributions': (
        'Projectile sampling distributions',
        'One launcher, many samples &mdash; PhET&rsquo;s sampling screen, the distribution of the '
        'sample mean at n = 2, 5, 15 and 40, and why its width is &sigma;/&radic;n'),
}
ROLES = """    /* role colours: green = the computed thing (the simulated histogram, the
       measured mean and standard deviation), orange = the exact law derived
       from PhET's mechanism (the density, sigma/sqrt(n), PhET's own
       delta-method spread) or a warning, magenta = the live marker (the
       projectile in flight, the handle being dragged, the sample mean),
       cyan = structure (the field, the launcher, the axes).  The six mystery
       launchers have their own colour slots (COL.lau) rather than borrowing
       a role colour. */"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    stem = sys.argv[1] if len(sys.argv) > 1 else os.path.basename(here)
    root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
    sims = os.path.join(root, 'projects', 'simulations')
    lagr = os.path.join(sims, 'build_lagr')
    dest = os.path.join(os.path.dirname(here), stem)

    src = io.open(os.path.join(lagr, 'p1_head.html'), encoding='utf-8').read()
    i = src.index('<style>')
    k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
    body = src[i:k]

    def sub1(s, old, new):
        assert s.count(old) == 1, (old[:60], s.count(old))
        return s.replace(old, new)

    body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""", ROLES)
    title, sub = TITLES[stem]
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>%s</h1>' % title)
    j0 = body.index('<span class="sub" id="sub">')
    j1 = body.index('</span>', j0) + len('</span>')
    body = body[:j0] + '<span class="sub" id="sub">' + sub + '</span>' + body[j1:]
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

    utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    utils = utils.replace(
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html)                    *',
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html, via                *\n'
        ' *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
    assert 'function polyline(' in utils and 'function legendAuto(' in utils and 'function plain(' in utils
    io.open(os.path.join(dest, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    buoy = io.open(os.path.join(sims, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
    hcut = buoy.index('/* the fluid: a translucent slab')
    helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function worldFitUp(' in helpers
    io.open(os.path.join(dest, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)
    print('%s: p1_head.html %d lines (scaffold %d from build_lagr); p1_utils.js %d; p4a_helpers.js %d'
          % (stem, len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
