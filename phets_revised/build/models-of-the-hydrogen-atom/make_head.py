#!/usr/bin/env python3
"""Write p1_head.html: the doctype, the header comment, the <style> block
(taken wholesale from build/blackbody-spectrum/p1_head.html, with only the
:root accents, the <h1>, the .sub tagline and the <title> changed), the
site-nav block, the body scaffold and the opening <script>."""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "blackbody-spectrum", "p1_head.html")
src = io.open(SRC, encoding="utf-8").read()

# everything from <style> to the end of the file is the shared scaffold
i = src.index("<style>")
scaffold = src[i:]

HEADCOMMENT = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Models of the hydrogen atom &mdash; billiard ball to Schr&ouml;dinger, and the spectrum that decides between them</title>
<!--
  ===================================================================
  models-of-the-hydrogen-atom.html — a remake of PhET's Models of the
  Hydrogen Atom: shine light into a box of hydrogen and see which of
  six historical models can reproduce what comes back out
  ===================================================================

  Remake of PhET Interactive Simulations' Models of the Hydrogen Atom
  (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0).  New
  code; no PhET code or assets.  Built against PhET's
  models-of-the-hydrogen-atom 1.0.9: both of its screens, all six of its
  atomic models, its Experiment-vs-Model switch, its white/monochromatic
  light source, its spectrometer, its electron-energy-level diagram, its
  three de Broglie representations and its (n,l,m) quantum numbers —
  and its model constants, read out of the minified original.

  Six views.  THE BOX is PhET's Spectra screen: a 475-unit box with the
  light source below it, photons flying up at PhET's 300 units/s, one
  every 0.0792 s, and the chosen atom in the middle.  Billiard Ball
  bounces photons off a hard sphere; Plum Pudding swallows one and
  re-emits it at 150 nm after half an oscillation; Classical Solar
  System spirals in and destroys the atom in 0.67 s; Bohr, de Broglie
  and Schrodinger absorb on a transition wavelength and fall back down.
  THE LEVELS is PhET's Energy Levels screen: the electron on its level,
  the transition squiggle, the (n,l) grid for Schrodinger — drawn on
  PhET's compressed axis and on the true one, side by side.  THE
  STANDING WAVE is de Broglie's three PhET representations (radial
  distance, 3-D height, brightness) with the n*lambda = 2*pi*r
  construction that picks the radii out.  THE ORBITALS is Schrodinger:
  |psi(n,l,m)|^2 from the analytic wavefunctions, its radial and
  angular nodes, and the radial distribution.  THE SERIES puts every
  transition on one compressed wavelength axis in its true colour.  THE
  RATES compares PhET's transition-strength table with the Einstein A
  coefficients of real hydrogen and checks the seeded cascade against
  the distribution it is drawn from.

  WHAT IS EXACT HERE
  ------------------
  Everything about the atom itself.  E_n = -R_H hc/n^2 and every
  transition wavelength from CODATA 2022 (scipy.constants), with the
  electron-proton reduced mass; r_n = n^2 a_0; v_n = alpha c / n.  The
  de Broglie condition n*lambda_dB = 2*pi*r_n is an identity, and holds
  to 5.2e-12 here, which is how consistent CODATA's separately rounded
  a_0 and alpha are.  The hydrogen wavefunctions are the analytic ones:
  the radial functions as exact polynomial coefficients (pinned against
  scipy.special.genlaguerre to 4e-17), the angular parts from the
  associated Legendre functions (pinned against scipy.special.sph_harm_y
  to 2e-16), normalisation, <r>, <r^2>, <1/r>, the n-l-1 radial nodes
  and the l-m angular nodes all asserted.  The drawn cloud is the
  column density of that |psi|^2, integrated along the line of sight and
  pinned against scipy quad.  The Einstein A coefficients come from the
  dipole radial integrals evaluated in closed form (a polynomial times
  exp(-sr), term by term) and agree with scipy quad to 2e-13;
  A(2p->1s) = 6.2683e8 /s, tau(2p) = 1.5953 ns.  The stochastic parts
  run on a seeded mulberry32 whose stream is reproduced bit-for-bit in
  Python, and the cascade ensembles are asserted against the exact
  distributions they are drawn from (|z| < 3).

  WHAT IS MODELLED / CHOSEN
  -------------------------
  The dynamics in the box are PhET's model, not physics: PhET's photon
  speed and firing rate, its 0.75 s and 1.0 s waits before an atom may
  absorb or emit, its flat 0.5 chance of spontaneous emission per step,
  its uniform choice of lower n for Bohr, its transition-strength table
  for Schrodinger, its 0.4 white-light bias toward the n=1 absorption
  lines, its 150 nm plum-pudding line, its classical spiral (radius
  falling 220 units/s, angular speed x1.008 a step).  None of those are
  rates of real hydrogen and the file says so on the canvas.  PhET's
  drawn orbit radii (15, 44, 81, 124, 174, 233) are compressed, not
  n^2, and so are its energy-diagram heights (0.025, 0.6, 0.73, 0.81,
  0.86, 0.9 of the axis) — both are drawn here beside the true ones.
  The wavelength axis of the series view is compressed the way PhET's
  spectrometer is, and the compression is printed on it.  Photon and
  electron sizes are PhET's, wildly out of scale with a_0.

  NOT MODELLED
  ------------
  No fine structure, no Lamb shift, no hyperfine structure, no
  relativistic corrections: the residual against NIST's measured lines
  (1.1e-5 on Lyman) IS that missing physics, and it is close to
  alpha^2/4 = 1.33e-5, the 1s relativistic shift.  No stimulated-
  emission bookkeeping beyond PhET's, no line widths, no Doppler or
  pressure broadening, no multi-electron atoms, no ionisation above
  n = 6 (PhET's ceiling), no magnetic field (m is degenerate here).
  PhET's alpha-particle screen does not exist in build 1.0.9 and is not
  reproduced.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  Constants: scipy.constants (CODATA 2022) — R_inf, a_0, alpha, the
  Hartree, m_e/m_p.  Measured lines: NIST, Handbook of Basic Atomic
  Spectroscopic Data, "Strong Lines of Hydrogen (H I)",
  physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable2.htm
  (fetched 2026-09-21) — all 8 vacuum rows and all 22 air rows, used
  verbatim; the vacuum-to-air conversion is Edlen 1966 (Metrologia 2,
  71).  The CIE 1931 2-degree colour-matching table (5 nm, DOI
  10.25039/CIE.DS.xvudnb9b, ISO/CIE 11664-1:2019) and the IEC 61966-2-1
  sRGB matrix give the line colours.  PhET's values are read from the
  minified build 1.0.9 in docs/phets/ and are labelled PhET's
  throughout.  The Python twin is build/models-of-the-hydrogen-atom/
  derive.py and every reference number is a line of its refvals.txt.
-->
"""

out = HEADCOMMENT + scaffold

# --- :root accents: this sim's role colours -----------------------------
old_roles = """    /* role colours: green = the computed curve (Planck's law, the area under it),
       orange = the reference (Wien's locus, the saved curves, the classical laws),
       magenta = the live marker (the thermometer thumb, the Graph Values point),
       cyan = structure (the axes, the band edges, the thermometer). */
    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;"""
new_roles = """    /* role colours: green = the computed thing (the exact quantum answer — the
       levels, |psi|^2, the Einstein rates, the emitted line), orange = the
       reference or the warning (PhET's own model values, the classical laws,
       the measured NIST line), magenta = the live marker (the electron, the
       chosen wavelength, the state the atom is in), cyan = structure (the box,
       the orbits, the axes). */
    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;"""
assert out.count(old_roles) == 1
out = out.replace(old_roles, new_roles)

# --- h1 and tagline -----------------------------------------------------
old_h1 = "  <h1>Blackbody spectrum</h1>"
assert out.count(old_h1) == 1
out = out.replace(old_h1, "  <h1>Models of the hydrogen atom</h1>")

old_sub = re.search(r'  <span class="sub" id="sub">.*?</span>\n', out, flags=re.S).group(0)
new_sub = ('  <span class="sub" id="sub">A remake of PhET&rsquo;s Models of the Hydrogen Atom: '
           'shine light into a box of hydrogen and see which of six models &mdash; billiard ball, plum pudding, '
           'solar system, Bohr, de Broglie, Schr&ouml;dinger &mdash; gives back the spectrum you measure</span>\n')
out = out.replace(old_sub, new_sub)

io.open(os.path.join(HERE, "p1_head.html"), "w", encoding="utf-8").write(out)
print("%d lines" % len(out.splitlines()))

# --- p1_utils.js: the shared utilities, verbatim ------------------------
U = io.open(os.path.join(HERE, "..", "blackbody-spectrum", "p1_utils.js"), encoding="utf-8").read()
for name in ["toRgb", "mix", "rgba", "shade", "neon", "neonCss", "function h(", "fmt", "sigf",
             "plain", "wrapText", "caption", "box", "frame", "ticksFor", "logTicks", "axes",
             "polyline", "legendBox", "legendAuto", "capFit", "fitCaption", "intTicks"]:
    assert name in U, "scaffold lost " + name
io.open(os.path.join(HERE, "p1_utils.js"), "w", encoding="utf-8").write(U)
print("utils: %d lines" % len(U.splitlines()))

# --- p2_cie.js: the CIE table, verbatim ---------------------------------
CIE = io.open(os.path.join(HERE, "..", "blackbody-spectrum", "p2_cie.js"), encoding="utf-8").read()
assert CIE.count("const CIE1931=[") == 1 and CIE.count("[830,") == 1
io.open(os.path.join(HERE, "p2_cie.js"), "w", encoding="utf-8").write(CIE)
print("cie: %d lines" % len(CIE.splitlines()))
