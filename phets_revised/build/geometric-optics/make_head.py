#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold  : projects/simulations/build_lagr/p1_head.html, from <style> to
              'use strict'; -- the CSS, the site-nav block and the body markup.
              Edited: the :root role-colour comment, <h1>, .sub and the seven
              site-nav hrefs (absolute -- the relative ../website/ links are
              dead from docs/phets_revised/).  Everything else byte-identical.
  utils     : projects/simulations/build_lagr/p1_utils.js, verbatim (the shared
              layer carrying every Known-bad fix: a throwing toRgb, a plain()
              that strips tags and decodes numeric entities inside the wide
              match, Liang-Barsky polyline clipping, range-sorting axes,
              guarded log ticks, recorded legends).
  helpers   : projects/simulations/build_buoy/p4_views.js from its top through
              matColour() -- the 2-D/world drawing layer (worldFitUp, worldPoly,
              seg, circleW, dot, arrowW, the label registry, axesR, stageLayout).

  python3 make_head.py
"""
import io
import os

TITLE = 'Geometric optics'
SUB = ('PhET&rsquo;s two screens &mdash; an object in front of a lens or a mirror &mdash; with the '
       'thin-optic equation solved exactly, every ray traced to agree with it, and the place where '
       'that model stops being true')
ROLE = """    /* role colours: green = the computed thing (the image, the traced ray,
       the focal length that follows from n and R), orange = the reference or
       analytic value (the paraxial focus, PhET's own construction) or a
       warning, magenta = the live marker (the object being dragged, the
       cursor on a plot), cyan = structure (the optic, the axis, the frames). */"""
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
    buoy = os.path.join(root, 'projects', 'simulations', 'build_buoy')

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

    top = io.open(os.path.join(here, 'p0_top.html'), encoding='utf-8').read()
    io.open(os.path.join(here, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

    utils = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    utils = utils.replace(
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html)                    *',
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html, via                *\n'
        ' *  build_lagr/p1_utils.js, verbatim)                                  *', 1)
    for name in ('function toRgb(', 'function plain(', 'function polyline(', 'function axes(',
                 'function legendAuto('):
        assert name in utils, name
    io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    bsrc = io.open(os.path.join(buoy, 'p4_views.js'), encoding='utf-8').read()
    hcut = bsrc.index('function matColour(')
    hcut = bsrc.rindex('\n', 0, hcut) + 1
    helpers = bsrc[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    for name in ('function axesR(', 'function lab(', 'function worldFitUp(', 'function worldPoly(',
                 'function stageLayout(', 'function arrowW(', 'function seg(', 'function dot('):
        assert name in helpers, name
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    print('p1_head.html %d lines (scaffold %d), p1_utils.js %d, p4a_helpers.js %d'
          % (len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
