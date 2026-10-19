#!/usr/bin/env python3
"""make_head.py -- p1_head.html for gravity-and-orbits.html, built by the same
extraction as its siblings: build_head() lives in ../keplers-laws/make_head.py
and cuts the scaffold (CSS, the injected site nav, the body markup) out of
projects/simulations/build_lagr/p1_head.html.  Only the title, the header
comment, the h1, the .sub line and the :root role-colour comment differ.

p1_utils.js, p2_engine.js, p4a_helpers.js and p4b_kit.js are NOT copied here:
assemble.py reads them from ../keplers-laws/, so this family of three sims
(keplers-laws, my-solar-system, gravity-and-orbits) has one engine.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KL = os.path.normpath(os.path.join(HERE, '..', 'keplers-laws'))
sys.path.insert(0, KL)
from make_head import build_head          # noqa: E402

TITLE = ('<title>Gravity and orbits &mdash; the Sun, the Earth, the Moon and the space station, '
         'drawn to scale and drawn so you can see them</title>')

COMMENT = """<!--
  ===================================================================
  gravity-and-orbits.html — one law, four systems: switch gravity
  off and everything flies straight; switch it on and the Earth
  comes back round
  ===================================================================

  Remake of PhET Interactive Simulations' Gravity and Orbits
  (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0).
  New code; no PhET code or assets.  PhET's two screens are the
  first two views here.

  THE MODEL: PhET's Model screen — the four systems (Sun and Planet,
  Sun Planet and Moon, Planet and Moon, Planet and Space Station)
  with the bodies drawn at PhET's own exaggerated sizes so they can
  be seen, the gravity switch, the mass sliders, the velocity and
  gravity-force arrows, the path, the grid, the measuring tape, the
  mass readout and the clock in Earth days.  TO SCALE: PhET's To
  Scale screen — the same four systems with every radius true, which
  is the point: at PhET's own zoom the Earth is a third of a pixel
  across beside a four-pixel Sun, and the space station is 10⁻⁵ of a
  pixel.  THE CIRCULAR ORBIT (an analysis view, not a PhET screen):
  where v = √(GM/r) comes from, what a slower or faster start does
  to the conic, the circular speed against radius with all four real
  orbits on it, and T² ∝ a³.  THE EXACT ORBIT (also not a PhET
  screen): the closed-form Kepler solution drawn against what the
  integrator actually did, with the error between them.  WHAT IS
  CONSERVED: energy, angular momentum and momentum along the run —
  exactly on the To Scale screen, and NOT on the Model screen,
  because PhET bends the physics there on purpose and this view
  measures by how much.

  WHAT IS EXACT
  -------------
  * The circular-orbit condition v = √(GM/r) and its period
    T = 2π√(r³/GM): asserted to 1e-12 against
    build/gravity-and-orbits/derive.py.
  * Kepler's third law: T²/a³ = 4π²/GM, the same number for the Moon
    and the space station about the Earth to 1e-13.
  * Every two-body run tracks the closed-form Kepler solution —
    elements from the state vector, then E − e sin E = M solved by
    Newton safeguarded on [M − e, M + e] to 1e-15 in the step, which
    derive.py checks against scipy's brentq and against solve_ivp
    (DOP853, rtol 1e-13) integrating the equations of motion.
  * Gravity off is a pure drift, so the bodies move in exactly
    straight lines at exactly constant speed: asserted at 0 (not
    "small") over 600 frames of every system.
  * Momentum and angular momentum are conserved to rounding by
    construction on the To Scale screen (every kick is an equal and
    opposite pair, every drift leaves r × v alone).

  WHAT IS MODELLED
  ----------------
  Newton's law of gravitation, point masses, in the plane, with no
  softening.  The integrator is PEFRL (Omelyan, Mryglod & Folk 2002)
  — PhET's own choice, and its three coefficients are PhET's — fourth
  order, four force evaluations a step, substepped so that no step
  exceeds 0.02 of the shortest pairwise crossing or free-fall time.
  PhET's two deliberate distortions of the Model screen are kept,
  because they ARE its model, and both are printed on the canvas:
  the star is nailed down, and in Sun-Planet-Moon the pull of the
  planet on the moon is multiplied by 10,200 (one-sidedly, so
  Newton's third law does not hold there) to keep the moon — moved
  out to 1.7 exaggerated planet radii — in orbit.

  WHAT IS NOT MODELLED
  --------------------
  No relativity, no tides, no oblateness, no atmospheric drag (the
  real ISS loses altitude to it continuously and is reboosted; this
  one does not), no radiation pressure, no third dimension.  Bodies
  are points for the force and discs only for drawing.  PhET's sounds, its
  screen-reader descriptions, its rewind button and its PhET-iO
  instrumentation are not here.

  MEASURED NUMBERS, AND WHERE THEY COME FROM
  ------------------------------------------
  Two columns, both on the page.  PhET's are read out of
  docs/phets/gravity-and-orbits_en.html (1.6.28) and named as
  PhET's: G = 6.67408e-11 (CODATA 2014), Sun 1.989e30 kg and
  6.957e8 m, Earth 5.9724e24 kg and 6.371e6 m at 1.47098074e11 m
  moving 30,300 m/s, Moon 7.346e22 kg and 1.7274e6 m at 3.633e8 m
  moving 1,082 m/s, Space Station 419,725 kg and 45.5 m at
  6,718,045.5 m moving 7,706 m/s, the clock's 86,400 s day and
  36,000 s base step, the 0.13125 substep and the 1/4/7 speeds, the
  987.5 × 772.5 stage at 1.5e-9 view units per metre, the 0.5–1.3
  zoom range, the half-to-double mass sliders, and every
  exaggeration factor of the Model screen.
  The measured column is the NASA planetary fact sheets
  (nssdc.gsfc.nasa.gov/planetary/factsheet/) for the Sun, Earth and
  Moon and NASA's ISS "Facts and Figures" for the station, each
  quoted at the precision that page prints.  The sim RUNS on PhET's
  numbers, so its systems move as PhET's do; the measured column is
  beside them and the differences are printed.

  WHAT THIS FILE MEASURED ABOUT PhET (derive.py; stated on the page)
  -----------------------------------------------------------------
  * PhET's Moon radius is 1,727.4 km.  The measured volumetric mean
    radius is 1,737.4 km (NASA moonfact) — 0.58 % apart, and the
    shape of a transposed digit.  Every other radius it ships is the
    fact-sheet value to the digits the fact sheet prints.
  * Its Sun is 1.989e30 kg against the measured 1.9884e30 (+0.03 %),
    its Earth 5.9724e24 against 5.9722e24 (+0.003 %), its Moon and
    its 419,725-kg station exact.
  * PhET's space station is at 347.0 km altitude moving 7,706 m/s,
    which is 1.0004 of the circular speed there — a very slightly
    elliptical orbit of period 91.4 min.  The real ISS is nearer
    420 km.
  * Its integrator is named PEFRL and carries its three
    coefficients, but as shipped it evaluates the acceleration ONCE
    a step and reuses it for all four kicks, which is first order,
    not fourth.  Both are run here, and the order of each is
    measured by halving the step.
-->"""

SUB = ('<span class="sub" id="sub">Four systems and one inverse-square law &mdash; PhET&rsquo;s Sun, Earth, '
       'Moon and space station, drawn big enough to see and then drawn true, with the circular-orbit '
       'condition, the exact Kepler solution and the conserved quantities measured against them</span>')

ROLES = """    /* role colours: green = the computed orbit and the conserved quantities,
       orange = the exact (Kepler) solution, a reference or a warning, magenta =
       the live body or marker, cyan = structure (the grid, the frame, the
       centre of mass). */"""


def main():
    head = build_head(TITLE, COMMENT, 'Gravity and orbits', SUB, ROLES, os.path.join(HERE, 'p1_head.html'))

    # makeShot() -- the display-list stub selfTest's layout sweep draws into -- is extracted
    # from ../my-solar-system/p7_test.js rather than retyped (PLAYBOOK section 4: the
    # framework is extracted, not rewritten).  It carries the rotate() tracking that a
    # rotated y-axis title needs, and the clip recording the stage-clip tests read.
    import io
    mss = os.path.normpath(os.path.join(HERE, '..', 'my-solar-system'))
    src = io.open(os.path.join(mss, 'p7_test.js'), encoding='utf-8').read()
    i = src.index('function makeShot(')
    k = src.index('\n}\n', src.index('return ctx;', i)) + 3
    banner = ('\n/* ================================================================== *\n'
              ' *  makeShot() -- the display-list stub the layout sweep draws into.    *\n'
              ' *  Extracted verbatim from build/my-solar-system/p7_test.js by         *\n'
              ' *  make_head.py, so the two sims measure layout the same way.  It      *\n'
              ' *  tracks rotate() (axes() draws its y title in a rotated frame) and    *\n'
              ' *  records clip() (the stage clip is a thing the tests check).          *\n'
              ' * ================================================================== */\n')
    shot = banner + src[i:k]
    for fn in ('function makeShot(', 'rotate(r)', 'clip()', 'fillText(t, x, y)'):
        assert fn in shot, fn
    io.open(os.path.join(HERE, 'p7a_shot.js'), 'w', encoding='utf-8').write(shot)
    print('p1_head.html: %d lines   p7a_shot.js: %d lines'
          % (len(head.splitlines()), len(shot.splitlines())))


if __name__ == '__main__':
    main()
