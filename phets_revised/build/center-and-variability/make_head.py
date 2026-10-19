#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4a_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; (the CSS, the site-nav block, the body markup).
             Edited: the :root role-colour comment, <h1>, .sub, and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils    : projects/simulations/build_lagr/p1_utils.js, verbatim.
  helpers  : projects/simulations/build_buoy/p4_views.js from its top to the
             first buoyancy-specific helper.

This is the same recipe the projectile-data-lab and
projectile-sampling-distributions remakes used; the two files it produces are
byte-identical to theirs, which is asserted below so a drift in either source
is noticed here rather than in the picture.

Usage:  python3 make_head.py
"""
import io
import os

STEM = 'center-and-variability'
TITLE = 'Center and variability'
SUB = ('Soccer balls on a number line &mdash; PhET&rsquo;s median, mean-and-median and '
       'variability screens, with every statistic computed exactly and its convention named')
ROLES = """    /* role colours: green = the data and the statistic computed from it,
       orange = the exact population value the kicker's own weights imply (or
       a warning), magenta = the live marker (the ball being dragged, the
       prediction pointer, the interval tool), cyan = structure (the field,
       the number line, the axes).  The five measures each own a colour slot
       (COL.med, COL.mean, COL.iqr, COL.rng, COL.mad) rather than borrowing a
       role colour, and the four kickers own COL.kick. */"""


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
    sims = os.path.join(root, 'projects', 'simulations')
    lagr = os.path.join(sims, 'build_lagr')
    sib = os.path.join(os.path.dirname(here), 'projectile-sampling-distributions')

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
    body = sub1(body, '<h1>Lagrange points</h1>', '<h1>%s</h1>' % TITLE)
    j0 = body.index('<span class="sub" id="sub">')
    j1 = body.index('</span>', j0) + len('</span>')
    body = body[:j0] + '<span class="sub" id="sub">' + SUB + '</span>' + body[j1:]
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

    # The shared 2-D layer has DRIFTED (Known-bad list: no single sim carries
    # all of its fixes).  build_lagr's legendAuto avoids the CURVES only; the
    # sibling remakes carry the later fix that also avoids the LABELS, which is
    # the one this sim needs (its conventions view puts value labels beside
    # every bar).  So the source here is the sibling's file, and the drift is
    # asserted to be exactly that one block rather than assumed.
    utils_lagr = io.open(os.path.join(lagr, 'p1_utils.js'), encoding='utf-8').read()
    utils = io.open(os.path.join(sib, 'p1_utils.js'), encoding='utf-8').read()
    LABEL_FIX = """      hit=true;
    }
    /* a corner clear of the CURVES can still be full of their LABELS: the bar
       chart's value labels sit where no bar is, which is exactly where this
       used to put the legend.  A legend is a label like any other. */
    for(let i=0;i<LABELS.length&&!hit;i++){
      const L=LABELS[i];
      if(L[2]<=cx||L[0]>=cx+bw||L[3]<=cy||L[1]>=cy+bh) continue;
"""
    assert LABEL_FIX in utils and LABEL_FIX not in utils_lagr
    assert utils.replace(LABEL_FIX, '') == utils_lagr.replace(
        '/*  small utilities  (extracted from sbs_sims.html)                    *',
        '/*  small utilities  (extracted from sbs_sims.html)                    *'
    ).replace(
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html)                    *',
        '/* ================================================================== *\n'
        ' *  small utilities  (extracted from sbs_sims.html, via                *\n'
        ' *  build_lagr/p1_utils.js, verbatim)                                  *', 1), \
        'p1_utils.js differs from build_lagr by more than the legendAuto label fix'
    assert 'function polyline(' in utils and 'function legendAuto(' in utils and 'function plain(' in utils
    assert 'function axes(' in utils and 'function ticksFor(' in utils
    io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    buoy = io.open(os.path.join(sims, 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
    hcut = buoy.index('/* the fluid: a translucent slab')
    helpers = buoy[:hcut].replace('extracted from build_cycloid/p4_views.js, unchanged',
                                  'from build_cycloid via build_buoy/p4_views.js, unchanged', 1)
    assert 'function axesR(' in helpers and 'function lab(' in helpers and 'function worldFitUp(' in helpers
    assert 'function stageLayout(' in helpers and 'function titleFor(' in helpers
    io.open(os.path.join(here, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    # the two shared files must match the sibling remakes byte for byte
    for fn in ['p1_utils.js', 'p4a_helpers.js']:
        a = io.open(os.path.join(here, fn), encoding='utf-8').read()
        b = io.open(os.path.join(sib, fn), encoding='utf-8').read()
        assert a == b, '%s drifted from the sibling remake' % fn
    print('%s: p1_head.html %d lines (scaffold %d from build_lagr); '
          'p1_utils.js %d; p4a_helpers.js %d; both match the sibling remakes'
          % (STEM, len((top + body).splitlines()), len(body.splitlines()),
             len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
