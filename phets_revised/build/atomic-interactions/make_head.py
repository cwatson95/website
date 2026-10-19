#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build p1_head.html: the house scaffold (style, site nav, body markup) taken
verbatim from build/coulombs-law/p1_head.html — the most recent phets_revised
head that carries the full 2-D layer's fixes — with only the <title>, the
header comment, the <h1> and the .sub tagline replaced, per PLAYBOOK section 4.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'coulombs-law', 'p1_head.html'))

src = io.open(SRC, encoding='utf-8').read()
i = src.index('<style>')
j = src.index('<script>')
scaffold = src[i:j]

# the only three edits the PLAYBOOK allows in the extracted block
scaffold = scaffold.replace(
    '  <h1>Coulomb&rsquo;s Law</h1>\n',
    '  <h1>Atomic Interactions</h1>\n')
old_sub_a = scaffold.index('<span class="sub" id="sub">')
old_sub_b = scaffold.index('</span>', old_sub_a) + len('</span>')
SUB = ('<span class="sub" id="sub">two atoms on a line and the Lennard-Jones '
       'potential between them: drag them together and apart, watch the well '
       'hold them, and read the force off the slope of the curve</span>')
scaffold = scaffold[:old_sub_a] + SUB + scaffold[old_sub_b:]
# role colours: keep the house semantics, name them for this sim
scaffold = scaffold.replace(
    """    /* role colours: green = the computed force, orange = the reference or a
       warning (the forbidden zone, a clipped arrow), magenta = the live marker,
       cyan = structure (the track, the ruler, the axes). */""",
    """    /* role colours: green = the computed thing (the potential, the total
       force), orange = the reference or analytic curve and every warning (the
       harmonic fit, the literature well, an off-scale arrow), magenta = the
       live marker (the current separation, the moving atom), cyan = structure
       (the axis, the landmarks, the atoms' outlines). */""")
assert '--pos:#b8ec4c' in scaffold and 'site-nav-css' in scaffold
assert scaffold.count('https://cooper-watson.net/') == 7
assert 'Atomic Interactions</h1>' in scaffold

HEAD = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atomic Interactions &mdash; two atoms in a Lennard-Jones well</title>
<!--
  ===================================================================
  atomic-interactions.html — two atoms, the Lennard-Jones potential
  between them, and the motion that potential produces
  ===================================================================

  Remake of PhET Interactive Simulations' Atomic Interactions (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0).  New code; no PhET
  code or assets.  PhET's build 1.2.21 (docs/phets/atomic-interactions_en
  .html) was read only for its model constants and its labels, each cited
  below and on the canvas as "PhET's value".

  Six views.  THE TWO ATOMS is PhET's single screen: a pinned atom on the
  left, a movable one on the right, the pair chosen from PhET's seven
  (neon-neon, argon-argon, oxygen-oxygen, the three mixed pairs and the
  adjustable one), the potential curve with the current separation
  marked, PhET's force arrows (attractive and repulsive separately,
  or their total, or hidden), drag, release and Return Atom.  THE WELL
  draws V(r) and F(r) = -dV/dr on one r axis with the three exact
  landmarks.  THE MOTION releases the atom and shows r(t), the energy
  ledger and the turning points.  SMALL OSCILLATIONS is the harmonic
  limit: omega = sqrt(V''(r_min)/mu), the parabola through the bottom of
  the well, and how fast the real period leaves it.  THE ATOM PAIRS puts
  PhET's seven wells on one axis beside the literature ones and checks
  the combining rules.  THE INTEGRATOR measures the order and the
  boundedness of the three time-steppers.

  WHAT IS EXACT
  -------------
  Everything about the potential is closed form and is asserted to
  machine precision against build/atomic-interactions/derive.py:
    V(r) = 4 eps [ (sigma/r)^12 - (sigma/r)^6 ], zero at r = sigma,
    minimum -eps at r_min = 2^(1/6) sigma;
    F(r) = -dV/dr = (24 eps/r)[ 2(sigma/r)^12 - (sigma/r)^6 ], checked
    against a 60-digit Decimal central difference AND against
    scipy.differentiate.derivative (worst 4.3e-15 of the force scale);
    V''(r) likewise, and V''(r_min) = 72 eps / (2^(1/3) sigma^2) exactly;
    omega = sqrt(V''(r_min)/mu) with mu the reduced mass (the movable
    atom's mass while the other is pinned, m1 m2/(m1+m2) when both move);
    the turning points of a bound orbit in closed form from
    u = (sigma/r)^6, u_in + u_out = 1;
    the period by a regularised Gauss-Legendre quadrature (the sin(th)
    of the substitution cancels exactly against the one inside v), which
    agrees with the integrated motion to 5e-9 and with 2 pi/omega in the
    small-amplitude limit at the rate Landau's anharmonic formula
    predicts, T = T0 (1 + (91/4) a^2/r_min^2).
  Motion is velocity Verlet; its measured order is 2.00 and its energy
  error is bounded (100 periods cost no more than one).  PhET's own
  stepper, semi-implicit Euler, is order 1.00 and also bounded; forward
  Euler is shown beside them and is not.

  WHAT IS MODELLED (PhET's choices, reproduced)
  ---------------------------------------------
  PhET's epsilon/sigma tables, read out of the minified original:
    eps/k_B (K):  Ne-Ne 35.8, Ar-Ar 111.84, O-O 1000, Ne-Ar 59.5,
                  Ne-O 51, Ar-O 85, adjustable 100 (slider 20..450);
    sigma (pm):   308, 376, 200, 343, 306, 340, 350 (slider 75..500);
    van der Waals radii 154 (Ne), 188 (Ar), 152 (O) pm and masses
    20.1797, 39.948, 15.9994 u, from PhET's nitroglycerin element table.
  The atoms are drawn at those radii, as PhET draws them.  PhET's own
  force expressions (48 e' sigma^12/r^13 and 24 e' sigma^6/r^7) are
  reproduced and asserted to be exactly -dV/dr.
  The literature values beside them, and their sources:
    Ne  sigma 278.9 pm, r_min 313.1 pm, eps/k_B 35.7 K
    Ar  sigma 341.8 pm, r_min 383.7 pm, eps/k_B 124.0 K
      — Attard, arXiv:1702.00096 Table I, after van Sciver, Helium
        Cryogenics 2nd ed. (Springer 2012).
    Ar  sigma 343.2 pm, eps/k_B 122.4 K;  O2 sigma 343.3 pm, 113 K
      — Bird, Stewart & Lightfoot, Transport Phenomena 2nd ed. (2007)
        pp. 864-865.
  Argon therefore has two retrieved sets 1.3% apart in eps; that spread
  is the honest uncertainty on an LJ fit, and it is printed.  THE SIM
  USES PhET'S VALUES BY DEFAULT, so that it reproduces PhET; the
  "literature eps, sigma" checkbox swaps in the sourced ones and the
  difference is drawn.  Which set is live is printed on every canvas.
  Finding, stated on the canvas: PhET's sigma is the literature r_min,
  not the literature sigma — 308 against 313.1 for neon and 376 against
  383.7 for argon (2% and 2%), where the literature sigma is 10% away,
  because PhET sets sigma = twice the van der Waals radius and that is a
  radius at the bottom of the well, a factor 2^(1/6) = 1.1225 out.  The
  oxygen pair matches nothing: PhET's own States-of-Matter constants
  carry EPSILON_FOR_DIATOMIC_OXYGEN 113 K (the literature value) and
  SIGMA_FOR_DIATOMIC_OXYGEN 365 pm, while Atomic Interactions uses
  1000 K and 200 pm, which puts r_min inside both drawn atoms.

  NOT MODELLED
  ------------
  Quantum mechanics.  Neon at 25 K has a de Broglie wavelength comparable
  with the well width, so the real dimer's levels are discrete and its
  zero-point energy is a large fraction of eps; nothing here is a bound
  state.  Real pair potentials are not 12-6 (the repulsion is closer to
  exponential and the dispersion series continues past r^-6).  The atoms
  move on a line only, there is no third body, no rotation and no
  temperature.  Oxygen is a diatomic molecule, drawn here as PhET draws
  it, as one sphere.  PhET's sounds, its screen-reader descriptions and
  its zoom buttons on the potential graph are not reproduced.
-->
"""
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(
    HEAD + scaffold + '<script>\n')
print('p1_head.html: %d lines' % len((HEAD + scaffold).splitlines()))
