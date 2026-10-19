#!/usr/bin/env python3
"""make_head.py -- p1_head.html for my-solar-system.html, built by the same
extraction as its sibling: build_head() lives in ../keplers-laws/make_head.py and
cuts the scaffold (CSS, the injected site nav, the body markup) out of
projects/simulations/build_lagr/p1_head.html.  Only the title, the header
comment, the h1, the .sub line and the :root role-colour comment differ.

p1_utils.js, p2_engine.js, p4a_helpers.js and p4b_kit.js are NOT copied here:
assemble.py reads them from ../keplers-laws/, so the family has one engine.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KL = os.path.normpath(os.path.join(HERE, '..', 'keplers-laws'))
sys.path.insert(0, KL)
from make_head import build_head          # noqa: E402

TITLE = ('<title>My solar system &mdash; two to four bodies under gravity, and the orbits they make</title>')

COMMENT = """<!--
  ===================================================================
  my-solar-system.html — gravity with two, three and four bodies:
  drag them, weigh them, throw them, and watch what Newton's law
  does with what you built
  ===================================================================

  Remake of PhET Interactive Simulations' My Solar System (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0).  New code; no
  PhET code or assets.  PhET's two screens are the first two views.

  TWO BODIES: PhET's Intro screen — a star and a planet whose masses
  you set and whose positions and velocities you drag, with the paths,
  the centre of mass, the velocity and gravity arrows, a grid and a
  measuring tape.  THE LAB: PhET's Lab screen — one to four bodies and
  its eleven orbital systems (Sun and planet, a moon, a comet, trojan
  asteroids, ellipses, "hyperbolic", the slingshots, a binary, the four
  star ballet, the double double), the values table, and the same
  controls.  THE EXACT ORBIT (an analysis view, not a PhET screen): two
  bodies are the one case that has a closed-form answer, so the
  integrated path is drawn against Kepler's — the relative orbit about
  μ = G(m₁+m₂), the two similar ellipses about the centre of mass, and
  the error between numerical and exact as it grows.  CONSERVATION
  (also not a PhET screen): energy, momentum and angular momentum along
  the run, the same system integrated by PhET's own shipped step beside
  it, and the order of both methods measured by halving the step.

  WHAT IS EXACT
  -------------
  Two-body runs, against Kepler's equation: the sim's own integration
  tracks the closed-form solution to 1e-9 AU over 120 frames, and
  build/my-solar-system/derive.py checks both against scipy's solve_ivp
  (DOP853, rtol 1e-12).  Momentum and angular momentum are conserved to
  rounding by construction (every kick is an equal and opposite pair,
  every drift leaves r × v alone): measured |Δp|/p ≤ 7e-15 and |ΔL/L| ≤
  1.3e-14 over 2,000 frames.  Energy is not a conserved quantity of the
  scheme, only a nearly conserved one: measured |ΔE/E| ≤ 6.1e-10 over
  the same run.  The four-star ballet is an exact homographic solution
  and is asserted as one: the square stays square to 2e-14 of a side
  and the whole configuration returns to its start after 0.2870 model
  units to 1e-11 AU.

  WHAT IS MODELLED
  ----------------
  Newton's law of gravitation, point masses, in the plane, with no
  softening.  The integrator is PEFRL (Omelyan, Mryglod & Folk 2002),
  fourth order, four force evaluations a step, substepped so that no
  step exceeds 0.02 of the shortest pairwise crossing or free-fall
  time.  A collision merges the pair: mass, momentum and the centre of
  mass are all conserved (PhET instead keeps the heavier body's mass
  and hands it the lighter one's momentum, which conserves momentum but
  loses the mass — the difference is stated in the readout).

  WHAT IS NOT MODELLED
  --------------------
  No relativity, no tides, no radiation pressure, no third dimension.
  Bodies are points for the force and discs only for drawing and for
  deciding when they touch.  Three bodies and more are chaotic, so a
  long run is one possible history, not the history: the sim says so on
  the canvas, and the conservation view is there to show how much of
  the drift is the method and how much is the physics.

  MEASURED NUMBERS, AND WHERE THEY COME FROM
  ------------------------------------------
  Everything dimensional is PhET's own, read out of
  docs/phets/my-solar-system_en.html (1.3.16) and named as PhET's:
  G = 4.4567 AU (km/s)² per 10²⁸ kg, the mass unit 10²⁸ kg, the mass
  slider 0.1–300, the body radius max(0.03, 0.023 m^(1/3)) AU, the
  engine time scale 0.05 per second with 4,000/N substeps, the zoom
  levels 25–125 view units per AU, the 20-AU path cap, and the eleven
  orbital systems' masses, positions and velocities.  The conversions
  to years and true km/s use AU = 149,597,870.7 km (IAU 2012), the
  Julian year and G = 6.6743e-11 (CODATA, PhET's own figure).

  WHAT THIS FILE MEASURED ABOUT PhET (derive.py; stated on the page)
  -----------------------------------------------------------------
  * PhET's integrator is named PEFRL and carries its three
    coefficients, but as shipped it evaluates the acceleration ONCE per
    step and reuses it for all four kicks.  That composition is exactly
    x + v h + ½a h², v + a h: first order, not fourth.  Measured by
    halving the step: error ratios 1.9, 2.0, 2.0 (order 0.97) against
    16.0, 16.0, 16.6 (order 4.02) for the real thing.  Its own substep
    is small enough to hide it — 3.7e-6 of the energy in the first
    second of running.
  * PhET's G = 4.4567 is 0.107 % below the 4.4615 that CODATA's G gives
    in these units, and PhET solves its time unit from its own G, so
    its "km/s" is 1.000538 true km/s.  Kept, so the presets move as
    PhET's do; the readout gives both.
  * PhET's "Hyperbolic" orbital system is not hyperbolic.  Its three
    test bodies fly past the star at 0.878, 0.929 and 0.995 of the
    escape speed, on ellipses of e = 0.954, 0.926 and 0.990 that come
    back after 12.6, 32.5 and 1,791 years.
-->"""

SUB = ('<span class="sub" id="sub">Two, three or four bodies pulling on each other &mdash; PhET&rsquo;s '
       'orbital systems with their paths, vectors and centre of mass, the two-body case against its exact '
       'Kepler solution, and what the integrator does to the conserved quantities</span>')

ROLES = """    /* role colours: green = the computed path and the conserved quantities, orange =
       the exact (Kepler) solution or a warning, magenta = the live body or marker,
       cyan = structure (the grid, the frame, the centre of mass). */"""


def main():
    head = build_head(TITLE, COMMENT, 'My solar system', SUB, ROLES, os.path.join(HERE, 'p1_head.html'))
    print('p1_head.html: %d lines' % len(head.splitlines()))


if __name__ == '__main__':
    main()
