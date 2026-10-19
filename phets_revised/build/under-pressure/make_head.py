#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold  : projects/simulations/build_lagr/p1_head.html, from <style> to
              'use strict'; -- the CSS, the site-nav block and the body markup.
              Edited: the :root role-colour comment, <h1>, .sub and the seven
              site-nav hrefs (absolute -- the relative ../website/ links are
              dead from docs/phets_revised/).  Everything else is byte-identical.
  utils     : projects/simulations/build_lagr/p1_utils.js, verbatim.
  helpers   : docs/phets_revised/build/buoyancy-basics/p4a_helpers.js, verbatim
              -- the 2-D/world drawing layer INCLUDING fluidRect() and
              forceArrow(), which the house buoyancy work wrote for pools.

  python3 make_head.py
"""
import io
import os

TITLE = 'Under Pressure'
SUB = ('PhET&rsquo;s four pools &mdash; square, trapezoid, chamber and mystery &mdash; with '
       'p = p<sub>atm</sub> + &rho;gh solved exactly and the units taken from their definitions')
ROLE = """    /* role colours: green = the computed quantity (the gauge pressure, the
       level, the force on the base), orange = the reference/analytic value
       (the air pressure, the weight of fluid, the exact law) or a warning,
       magenta = the live marker (the gauge being dragged, the loaded piston),
       cyan = structure (the pool walls, the free surface, the frames). */"""
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
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
    lagr = os.path.join(root, 'projects', 'simulations', 'build_lagr')
    buoy = os.path.join(root, 'docs', 'phets_revised', 'build', 'buoyancy-basics')

    src = io.open(os.path.join(lagr, 'p1_head.html'), encoding='utf-8').read()
    i = src.index('<style>')
    k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
    body = src[i:k]

    body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""", ROLE)
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>%s</h1>' % TITLE)
    j0 = body.index('<span class="sub" id="sub">')
    j1 = body.index('</span>', j0) + len('</span>')
    body = body[:j0] + '<span class="sub" id="sub">' + SUB + '</span>' + body[j1:]
    for old, new in NAV:
        body = sub1(body, 'href="%s"' % old, 'href="%s"' % new)
    assert 'href="../' not in body
    assert 'aria-current="page"' in body
    for need in ('id="scene"', 'id="panel"', 'id="tabs"', 'id="readout"', 'id="eqbar"',
                 'id="tag"', 'id="hint"', 'id="errbox"'):
        assert need in body, need

    top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
    io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

    utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    for name in ('function toRgb(', 'function plain(', 'function polyline(', 'function axes(',
                 'function legendAuto(', 'function ticksFor(', 'function caption(',
                 'function fitCaption(', 'function box(', 'function frame('):
        assert name in utils, name
    # the Known-bad fixes this file depends on, each checked individually
    assert '[a-zA-Z' in utils, 'plain(): the entity regex must be wide (Known-bad)'
    assert 'replace(/<\\/?[a-zA-Z][^>]*>/g' in utils, 'plain(): must strip tags (Known-bad)'
    assert 'String.fromCodePoint' in utils, 'plain(): numeric entities decoded INSIDE the wide match (Known-bad)'
    assert 'Liang-Barsky' in utils, 'polyline(): Liang-Barsky clip (Known-bad)'
    assert 'ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi)' in utils, 'axes(): sorts its range (Known-bad)'
    assert 'if(!(lo>0)||!(hi>0)' in utils, 'logTicks(): guarded against a non-positive bound (Known-bad)'
    io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    helpers = io.open(os.path.join(buoy, 'p4a_helpers.js'), encoding='utf-8').read()
    for name in ('function axesR(', 'function lab(', 'function worldFitUp(', 'function fluidRect(',
                 'function forceArrow(', 'function worldPoly(', 'function stageLayout(',
                 'function seg(', 'function arrowW(', 'function dot('):
        assert name in helpers, name
    helpers = helpers.replace('from build_cycloid via build_buoy/p4_views.js, unchanged',
                              'from build_cycloid via build_buoy and buoyancy-basics, unchanged', 1)
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    print('under-pressure: p1_head.html %d lines (scaffold %d), p1_utils.js %d, p4a_helpers.js %d'
          % (len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
