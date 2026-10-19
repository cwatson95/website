#!/usr/bin/env python3
"""make_head.py -- build p1_head.html, p1_utils.js and p4a_helpers.js by
EXTRACTION from the house sims (PLAYBOOK section 4: the aesthetic is extracted,
not restyled).  Run it again whenever the house scaffold changes.

  scaffold   projects/simulations/build_lagr/p1_head.html, from <style> to
             "'use strict';" -- the CSS, the injected site-nav block and the
             body markup.  Edited: the <title>, the header comment, the <h1>,
             the .sub tagline, the :root role-colour comment and the seven
             site-nav hrefs (absolute: the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else is byte-identical.
  utils      projects/simulations/build_lagr/p1_utils.js, verbatim: the shared
             layer carrying every Known-bad fix (toRgb throws, plain() strips
             tags and decodes numeric entities inside the wide match, axes()
             sorts its range, polyline() clips in data space by Liang-Barsky,
             logTicks guards non-positive bounds, legends record their boxes).
  helpers    projects/simulations/build_lagr/p4_views.js, its generic 2-D block
             (worldFitUp ... marker), plus worldFill/worldPoly/arrowW from
             build_buoy/p4_views.js, which lagrange dropped.  The 3-D camera
             block is NOT taken: neither sim has a 3-D view and code no view
             calls is dead code a mutation sweep can only report as survivors.

Both sims of this family use the same p1_utils.js and p4a_helpers.js;
my-solar-system's assemble.py reads them from here.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
SIMS = os.path.join(ROOT, 'projects', 'simulations')
LAGR = os.path.join(SIMS, 'build_lagr')
BUOY = os.path.join(SIMS, 'build_buoy')

TITLE = ('<title>Kepler&rsquo;s laws &mdash; the ellipse and its foci, equal areas in equal times, '
         'and T&sup2; against a&sup3;</title>')

COMMENT = """<!--
  ===================================================================
  keplers-laws.html — Kepler's three laws on one orbit: the ellipse
  with the star at a focus, equal areas in equal times, and the
  period against the semi-major axis
  ===================================================================

  Remake of PhET Interactive Simulations' Kepler's Laws (University of
  Colorado Boulder, phet.colorado.edu, CC-BY 4.0).  New code; no PhET
  code or assets.  PhET's four screens are the first four views here.

  THE FIRST LAW: drag the planet, or the tip of its velocity arrow,
  and the orbit follows — the ellipse with the star at one focus, the
  empty focus, the string d₁ + d₂ = 2a, the axes, the semiaxes a and
  b, the focal distance c and e = c/a.  Choose one of PhET's target
  orbits (Mercury to Jupiter) and match it, or put the planet on it.
  THE SECOND LAW: the orbit cut into 2–6 sectors that take equal
  times, which fill as the planet sweeps them, with PhET's swept-area
  bars under the orbit and the areas and times printed on it.  THE
  THIRD LAW: T^p against a^q with PhET's power chips — only a³ and T²
  give a straight line through the origin — and a log–log view on
  which every orbit about the same star lies on one line of slope 3/2,
  with the five planets on it.  ALL LAWS: the three together.
  KEPLER'S EQUATION (an analysis view, not a PhET screen): where the
  motion in time comes from — the auxiliary circle, the mean, eccentric
  and true anomalies, M = E − e sin E solved by Newton in front of you,
  and the three anomalies plotted over one period.

  WHAT IS EXACT
  -------------
  Everything about the orbit.  The elements come from the state vector
  in closed form (vis-viva for a, the eccentricity vector for e and the
  periapsis direction, the sign of x v_y − y v_x for the sense of
  travel); the position in time comes from Kepler's equation solved by
  Newton safeguarded with the bracket [M − e, M + e] to 1e-15 in the
  step, which build/keplers-laws/derive.py checks against scipy's
  brentq (worst 8.9e-16 over 120 cases) and against solve_ivp at rtol
  1e-13 integrating the equations of motion (the Kepler position stays
  within 8e-12 a over 2.3 periods).  The sector areas are πab/N
  exactly; derive.py re-derives each by Gauss–Legendre quadrature of
  ½r²dν (worst 1.3e-15) and the suite re-derives them again in the
  browser.  T = 2π√(a³/GM), asserted against both.  No numerical
  integration is used anywhere in the sim itself.

  WHAT IS MODELLED
  ----------------
  PhET's model: a test body about a FIXED star, so the planet's own
  mass does not enter (for a real planet μ = G(M+m), which moves the
  Earth's period by 1.5 parts in a million).  PhET's rules are kept:
  the speed is capped at 0.99 of the escape speed and the orbit is
  flagged as escaping from 0.9801 of it; an orbit whose periapsis is
  inside the star crashes; a flagged orbit is drawn dashed and the
  clock will not run on it (PhET disables play the same way).

  WHAT IS NOT MODELLED
  --------------------
  Nothing perturbs the orbit: no other planet, no oblateness, no
  relativity (Mercury's 43″/century is 5e-8 of a revolution and would
  be invisible), no radiation pressure.  PhET's sounds, its metronome,
  its screen-reader descriptions and its PhET-iO target orbits are not
  here.  Orbits are drawn in the plane, as PhET draws them.

  MEASURED NUMBERS, AND WHERE THEY COME FROM
  ------------------------------------------
  AU = 149,597,870.7 km (IAU 2012 Resolution B2, exact by definition);
  the Julian year = 365.25 d = 31,557,600 s (exact by definition);
  GM_sun = 1.32712440042e20 m³ s⁻² (Wikipedia, "Standard gravitational
  parameter" — the value projects/simulations/lagrange_points.html
  already carries).  Those three give K = GM_sun yr²/AU³ =
  39.4769264 AU³ yr⁻² per solar mass, and 1 AU/yr = 4.740470464 km/s.
  PhET's own values are read out of docs/phets/keplers-laws_en.html
  (1.2.12) and named as PhET's on the page: G = 4.4567 AU (km/s)² per
  10²⁸ kg, our Sun = 200 × 10²⁸ kg, star mass 0.5–2 suns snapping to 1
  within 5 %, the planet at (2, 0) AU moving 17.2358 km/s, 2–6 period
  divisions, e shown as 0 below 0.01, the star's radius
  max(0.03, 0.023 M^(1/3)) AU, and the target orbits' (e, a).

  WHERE PhET AND THIS FILE DIFFER, DELIBERATELY (all measured in
  derive.py, and stated in the physics column)
  -----------------------------------------------------------------
  * PhET's μ = 4.45669 M is 0.24 % away from its own year: a circular
    orbit at 1 AU reads 29.855 km/s where 2π AU in its 1.000-year
    period is 29.785 km/s.  Here GM_sun, the AU and the year are the
    measured ones, so the two agree: 29.7847 km/s.
  * PhET's clock advances the mean anomaly 6.3/T rad per year, not
    2π/T, so one revolution reads 0.99733 T on its stopwatch.  Here
    the clock is exact.
  * PhET stops Newton's iteration once a step falls below 0.01 rad,
    which leaves the planet up to 2.4e-5 AU (3,559 km) from where
    Kepler puts it on the default orbit — invisible, but not exact.
    Here the step is driven to 1e-15.
-->"""

SUB = ('<span class="sub" id="sub">One planet, one star, and the three laws it obeys &mdash; the ellipse '
       'with the star at a focus, the equal areas swept in equal times, and T&sup2; &prop; a&sup3; &mdash; '
       'every orbit solved in closed form from Kepler&rsquo;s equation</span>')

ROLES = """    /* role colours: green = the computed orbit and its quantities, orange =
       the reference (a target orbit, the exact law) or a warning, magenta =
       the live planet and the swept sector, cyan = structure (the star, the
       axes, the frame). */"""

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


def build_head(title, comment, h1, sub, roles, out_path):
    src = io.open(os.path.join(LAGR, 'p1_head.html'), encoding='utf-8').read()
    i = src.index('<!doctype html>')
    k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
    head = src[i:k]
    t0 = head.index('<title>')
    t1 = head.index('-->', t0) + 3
    head = head[:t0] + title + '\n' + comment + head[t1:]
    h0 = head.index('<header>\n  <h1>')
    h1e = head.index('<nav id="tabs"></nav>')
    head = head[:h0] + '<header>\n  <h1>' + h1 + '</h1>\n  ' + sub + '\n  ' + head[h1e:]
    head = sub1(head, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""", roles)
    for old, new in NAV:
        head = sub1(head, 'href="%s"' % old, 'href="%s"' % new)
    assert 'href="../' not in head and 'aria-current="page"' in head
    assert head.count('<canvas id="scene">') == 1 and '<div id="hint"></div>' in head
    io.open(out_path, 'w', encoding='utf-8').write(head)
    return head


def main():
    head = build_head(TITLE, COMMENT, 'Kepler&rsquo;s laws', SUB, ROLES, os.path.join(HERE, 'p1_head.html'))

    utils = io.open(os.path.join(LAGR, 'p1_utils.js'), encoding='utf-8').read()
    utils = sub1(utils, ' *  small utilities  (extracted from sbs_sims.html)                    *',
                 ' *  small utilities  (sbs_sims.html via build_lagr/p1_utils.js, verbatim) *')
    for fn in ('function toRgb(', 'function plain(', 'function axes(', 'function polyline(', 'function logTicks(',
               'function legendBox(', 'function legendAuto(', 'function fitCaption(', 'function sigf('):
        assert fn in utils, fn
    io.open(os.path.join(HERE, 'p1_utils.js'), 'w', encoding='utf-8').write(utils)

    lagr = io.open(os.path.join(LAGR, 'p4_views.js'), encoding='utf-8').read()
    cut = lagr.index('/* ---- 3-vector helpers')
    helpers = lagr[:cut]
    helpers = sub1(helpers, ' *  — extracted from build_buoy/p4_views.js; the camera block from     *\n'
                            ' *  pulsar.html (v3, makeCamera, camBasis, project)                    *',
                   ' *  — build_lagr/p4_views.js (lineage build_buoy, build_cycloid), its   *\n'
                   ' *  generic block only; worldFill/worldPoly/arrowW from build_buoy      *')
    buoy = io.open(os.path.join(BUOY, 'p4_views.js'), encoding='utf-8').read()
    extra = []
    for fn in ('function worldFill(', 'function worldPoly(', 'function arrowW('):
        a = buoy.index(fn)
        a = buoy.rindex('\n', 0, a) + 1
        # take any comment line directly above the function
        if buoy[:a].rstrip().endswith('*/'):
            a = buoy.rindex('/*', 0, a)
        b = buoy.index('\n}\n', a) + 3
        extra.append(buoy[a:b])
    helpers += ''.join(extra)
    for fn in ('function worldFitUp(', 'function worldPath(', 'function clipToWin(', 'function legendR(',
               'function stageLayout(', 'function axesR(', 'function lab(', 'function arrowW(',
               'function worldPoly(', 'function diamond(', 'function marker('):
        assert fn in helpers, fn
    assert 'makeCamera' not in helpers and 'const v3=' not in helpers
    io.open(os.path.join(HERE, 'p4a_helpers.js'), 'w', encoding='utf-8').write(helpers)

    print('p1_head.html: %d lines   p1_utils.js: %d lines   p4a_helpers.js: %d lines'
          % (len(head.splitlines()), len(utils.splitlines()), len(helpers.splitlines())))


if __name__ == '__main__':
    main()
