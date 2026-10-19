#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js, p2_cie.js and p4a_helpers.js by EXTRACTION
from the house sims (PLAYBOOK section 4: the aesthetic is extracted, not
restyled).

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
  cie       : docs/phets_revised/build/blackbody-spectrum/p2_cie.js (the CIE
              1931 2-degree table, written from the CIE's own data file) plus
              the sRGB conversion block lifted out of blackbody-spectrum.html.
  helpers   : projects/simulations/build_buoy/p4_views.js from its top through
              matColour() -- the 2-D/world drawing layer (worldFitUp, worldPoly,
              seg, circleW, dot, arrowW, the label registry, axesR, stageLayout).

  python3 make_head.py
"""
import io
import os

TITLE = 'Bending light'
SUB = ('PhET&rsquo;s three screens &mdash; a laser on a boundary, the same picture as a wave, and a '
       'prism &mdash; with Snell&rsquo;s law, the Fresnel equations and the dispersion model solved '
       'exactly, and the rainbow they add up to')
ROLE = """    /* role colours: green = the computed thing (the transmitted ray's
       angle, the reflected fraction, the traced path), orange = the
       reference or analytic value (Brewster, the critical angle, the
       closed-form deviation) or a warning, magenta = the live marker (the
       laser, the cursor on a plot), cyan = structure (the normal, the
       boundary, the prism faces, the axes).  Light itself is drawn in its
       own spectral colour, from the CIE 1931 observer. */"""
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
    bb = os.path.join(root, 'docs', 'phets_revised', 'build', 'blackbody-spectrum')

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

    # --- the CIE table (from the CIE's own file, via blackbody-spectrum) and
    #     the sRGB block that goes with it
    cie = io.open(os.path.join(bb, 'p2_cie.js'), encoding='utf-8').read()
    assert 'const CIE1931=[' in cie and cie.count('[830,') == 1
    bbh = io.open(os.path.join(root, 'docs', 'phets_revised', 'blackbody-spectrum.html'),
                  encoding='utf-8').read()
    a = bbh.index('/* sRGB (IEC 61966-2-1) primaries, D65')
    b = bbh.rindex('/*', a, bbh.index('function bbLinear('))
    srgb = bbh[a:b]
    c = bbh.rindex('/*', 0, bbh.index('function cmfAt('))
    d = bbh.index('function hexOfBytes(')
    mono = bbh[c:d]
    for name in ('function srgbGamma(', 'function xyzToLin('):
        assert name in srgb, name
    for name in ('function cmfAt(', 'function monoLinear(', 'function monoLevel(',
                 'function cssOfLinear('):
        assert name in mono, name
    head = ('/* ================================================================== *\n'
            ' *  colour: the CIE 1931 2-degree observer and the sRGB transform      *\n'
            ' *  — the table and the conversions are lifted unchanged from          *\n'
            ' *  docs/phets_revised/blackbody-spectrum (which wrote the table from  *\n'
            ' *  the CIE\'s own data file; nothing here is re-typed)                 *\n'
            ' * ================================================================== */\n')
    body_cie = (head + cie[cie.index('/* CIE 1931'):] + '\nconst CIE_STEP=5;'
                + '   /* nm between the embedded rows */\n' + srgb + mono)
    io.open(os.path.join(here, 'p2_cie.js'), 'w', encoding='utf-8').write(body_cie)

    bsrc = io.open(os.path.join(buoy, 'p4_views.js'), encoding='utf-8').read()
    hcut = bsrc.index('function matColour(')
    hcut = bsrc.rindex('\n', 0, hcut) + 1
    helpers = bsrc[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    for name in ('function axesR(', 'function lab(', 'function worldFitUp(', 'function worldPoly(',
                 'function stageLayout(', 'function arrowW(', 'function seg(', 'function dot('):
        assert name in helpers, name
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    print('p1_head.html %d lines (scaffold %d), p1_utils.js %d, p2_cie.js %d, p4a_helpers.js %d'
          % (len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(body_cie.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
