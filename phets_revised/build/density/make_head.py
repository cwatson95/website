#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK §4: the aesthetic is extracted, not restyled).

  scaffold  : projects/simulations/build_lagr/p1_head.html, from <style> to
              'use strict'; — the CSS, the site-nav block and the body markup.
              Edited: the :root role-colour comment, <h1>, .sub and the seven
              site-nav hrefs (absolute — the relative ../website/ links are dead
              from docs/phets_revised/).  Everything else is byte-identical.
  utils     : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
              layer carrying every Known-bad fix: a throwing toRgb, a plain()
              that strips tags and decodes numeric entities inside the wide
              match, Liang-Barsky polyline clipping, range-sorting axes,
              guarded log ticks, recorded legends).
  helpers   : projects/simulations/build_buoy/p4_views.js from its top through
              matColour() — the 2-D/world drawing layer INCLUDING fluidRect()
              and forceArrow(), which the house buoyancy sim wrote for exactly
              this job.

  python3 make_head.py <stem>      (stem: density | buoyancy-basics)
"""
import io
import os
import sys

HEAD = {
    'density': (
        'Density',
        'PhET&rsquo;s three screens &mdash; a block in a pool, sets matched in mass, volume or '
        'density, and five mystery blocks &mdash; with Archimedes&rsquo; principle solved exactly',
    ),
    'buoyancy-basics': (
        'Buoyancy: Basics',
        'PhET&rsquo;s two screens &mdash; blocks of every material in six fluids, on the scales and '
        'on the pool floor &mdash; with the upthrust taken from the pressure on the faces',
    ),
}
ROLE = {
    'density': """    /* role colours: green = the computed quantity (the density, the submerged
       volume, the upthrust), orange = the reference/analytic value (the
       handbook density, the exact law) or a warning, magenta = the live marker
       (the block being adjusted, the cursor on a plot), cyan = structure (the
       pool, the waterline, the frames). */""",
    'buoyancy-basics': """    /* role colours: green = the computed quantity (the buoyant force, the
       submerged fraction), orange = the reference/analytic value (the weight,
       the handbook density) or a warning, magenta = the live marker (the block
       being adjusted, the contact force), cyan = structure (the fluid, the
       waterline, the scales, the frames). */""",
}
NAV = [('../website/index.html', 'https://cooper-watson.net/index.html'),
       ('../website/about.html', 'https://cooper-watson.net/about.html'),
       ('../website/teaching.html', 'https://cooper-watson.net/teaching.html'),
       ('../modules/teaching_modules.html', 'https://cooper-watson.net/modules/teaching_modules.html'),
       ('../website/simulations.html', 'https://cooper-watson.net/simulations.html'),
       ('../website/research.html', 'https://cooper-watson.net/research.html'),
       ('../website/cv.html', 'https://cooper-watson.net/cv.html')]


def sub1(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


def main():
    stem = sys.argv[1] if len(sys.argv) > 1 else 'density'
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(here) != stem:
        here = os.path.join(os.path.dirname(here), stem)
    root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
    lagr = os.path.join(root, 'projects', 'simulations', 'build_lagr')
    buoy = os.path.join(root, 'projects', 'simulations', 'build_buoy')

    src = io.open(os.path.join(lagr, 'p1_head.html'), encoding='utf-8').read()
    i = src.index('<style>')
    k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
    body = src[i:k]

    body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""", ROLE[stem])
    title, sub = HEAD[stem]
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>%s</h1>' % title)
    j0 = body.index('<span class="sub" id="sub">')
    j1 = body.index('</span>', j0) + len('</span>')
    body = body[:j0] + '<span class="sub" id="sub">' + sub + '</span>' + body[j1:]
    for old, new in NAV:
        body = sub1(body, 'href="%s"' % old, 'href="%s"' % new)
    assert 'href="../' not in body
    assert 'aria-current="page"' in body

    top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
    io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

    utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    utils = utils.replace(
        '/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html)                    *',
        '/* ================================================================== *\n *  small utilities  (extracted from sbs_sims.html, via                 *\n *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
    for name in ('function toRgb(', 'function plain(', 'function polyline(', 'function axes(', 'function legendAuto('):
        assert name in utils, name
    io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    bsrc = io.open(os.path.join(buoy, 'p4_views.js'), encoding='utf-8').read()
    hcut = bsrc.index('function matColour(')          # this sim has its own matColor
    hcut = bsrc.rindex('\n', 0, hcut) + 1
    helpers = bsrc[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    for name in ('function axesR(', 'function lab(', 'function worldFitUp(', 'function fluidRect(',
                 'function forceArrow(', 'function worldPoly(', 'function stageLayout('):
        assert name in helpers, name
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    print('%s: p1_head.html %d lines (scaffold %d), p1_utils.js %d, p4a_helpers.js %d'
          % (stem, len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
