#!/usr/bin/env python3
"""Write p1_head.html for beers-law-lab.html and concentration.html.

The scaffold -- the whole <style> block, the injected site-nav stylesheet, the site header
and the body markup -- is EXTRACTED from build/ph-scale/p1_head.html rather than retyped
(PLAYBOOK section 4), and its SHA-256 is pinned so a change over there cannot arrive here
unnoticed.  Only the <title>, the header comment, the <h1>, the .sub tagline and the
:root accent block are this sim's own.

    python3 make_head.py            -> p1_head.html  (the full sim)
    python3 make_head.py basics     -> ../concentration/p1_head.html
"""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'ph-scale', 'p1_head.html')
SRC_SHA = 'd29777bb08c6f9bd3f4a230aacc5fca9a9a2fb4be4506bc2c2a28d72771ca9ae'

src = io.open(SRC, encoding='utf-8').read()
got = hashlib.sha256(src.encode('utf-8')).hexdigest()
if len(sys.argv) > 2 and sys.argv[2] == '--sha':
    print(got)
    raise SystemExit(0)
assert got == SRC_SHA, 'build/ph-scale/p1_head.html has changed (%s) -- re-check the ' \
                       'scaffold before re-pinning' % got

i = src.index('<style>')
j = src.index('<header>\n  <h1>')
SCAFFOLD_STYLE = src[i:j]                       # both <style> blocks + the site-nav header
k = src.index('<div id="wrap">')
SCAFFOLD_BODY = src[k:]                         # stage, readout, panel, eqbar, <script>

# the one thing in the extracted CSS that is this sim's: the role-colour block
OLD_ROOT = """    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;"""
NEW_ROOT = """    --pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --beam:#5ac8e0; --solid:#e8843a;"""
OLD_NOTE = """    /* role colours: green = the computed thing (the exact pH and the hydronium it
       comes from), orange = the reference (PhET's own rule, the measured ranges),
       magenta = the live marker (where the beaker is now), cyan = structure (the
       glass, the axes, the hydroxide). */"""
NEW_NOTE = """    /* role colours: green = the computed thing (the absorbance, the concentration
       this file works out), orange = the reference (PhET's own colour ramp, the
       literature solubilities, the solid on the bottom), magenta = the live marker
       (the wavelength cursor, the beaker's present state), cyan = structure (the
       glass, the cuvette, the axes, the beam). */"""
assert SCAFFOLD_STYLE.count(OLD_ROOT) == 1 and SCAFFOLD_STYLE.count(OLD_NOTE) == 1
SCAFFOLD_STYLE = SCAFFOLD_STYLE.replace(OLD_ROOT, NEW_ROOT).replace(OLD_NOTE, NEW_NOTE)

BASICS = len(sys.argv) > 1 and sys.argv[1] == 'basics'

COMMON = """
  WHAT IS EXACT HERE
  ------------------
  The chemistry is arithmetic, and it is done as arithmetic.

      A = eps l c,   T = 10^-A,   C = n/V,   n = cV

  Beer-Lambert is PhET's own model (doc/model.md: "A = abC", "T = 10^-A") and it
  is implemented with no approximation at all: derive.py asserts A against
  50-digit `decimal` evaluation over every solution x four path lengths x four
  concentrations (worst 2.7e-16 relative), T against the same (4.7e-16), and the
  round trip -log10(T) = A (1.4e-16).  The end-to-end error in T is LARGER, at
  1.2e-15, and that is not a defect: a relative error d in A becomes ln10 * A * d
  in T, so the suite asserts the amplification is the expected one rather than
  pretending it is not there.  Both extremes are pinned too: A = 0 gives T = 1
  exactly, A = 1 and A = 2 give exactly 10 % and 1 %, and 10^-A underflows a
  double to exactly zero at A = 324 -- past which the detector's reading cannot
  be inverted at all, since -log10(0) is infinite.

  The beaker is a MOLE LEDGER, and it closes.  Volume and moles are moved by
  PhET's five mechanisms in PhET's own order (faucet, drain, dropper,
  evaporation, shaker), each returning the amount that actually moved, so

      n_final  = shaker + dropper - drained          (exactly)
      V_final  = V_0 + faucet + dropper - drain - evaporation

  derive.py runs a 900-frame script through every one of them TWICE, once in
  doubles and once in exact `fractions.Fraction`, and both ledgers close --
  the rational one identically, the double one to 0.0 mol and 0.0 L, with the
  two runs agreeing to 4.4e-15 over the whole script.  The drain is the
  interesting one: it removes SOLUTION, so it carries solute away at the
  DISSOLVED concentration min(Csat, n/V) and leaves the precipitate behind.

  Saturation is exact: C = min(Csat, n/V), precipitate = max(0, n - V Csat),
  and evaporating a fixed n raises C along the exact hyperbola n/V until
  V = n/Csat, after which C is pinned at Csat and the rest falls out as solid.
  That saturation volume, and the time to reach it at PhET's 0.25 L/s, are
  closed forms the suite asserts against derive.py.

  Each shaker particle carries exactly 1/200 mol (PhET's particlesPerMole), so
  the shaker's contribution to the ledger is an exact multiple of 0.005 mol,
  and the particles you watch fall are the moles: they are added when they land,
  as PhET's are, not when they are released.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's, read out of the minified original by build/beers-law-lab/
  extract_phet.py and written into the file by make_data.py -- not one of them
  typed by hand: the nine solutes (molar mass, stock concentration, saturation
  point, and all three colour stops), the eight Beer's Law solutions (range,
  default, display transform and two-stop ramp), the eight molar-absorptivity
  spectra at one value per nanometre from 380 to 780 nm, the beaker's 1 L, the
  0-7 mol and 0-1 L ranges, the 0.5-2 cm cuvette and its 0.1 cm snap, the flow
  rates (dropper 0.05 L/s, faucets 0.25 L/s, evaporator 0.25 L/s, shaker
  0.2 mol/s), 200 particles per mole, water at 1000 g/L and rgb(224,255,255),
  and every decimal-place count the readouts use.

  Literature, fetched 2026-09-22 from the Wikipedia chemical infoboxes and
  quoted to their own printed precision, converted to molarity on the stated
  assumption that a litre of water makes a litre of solution: sucrose 342.297
  g/mol and 2.01 g/mL (20 C); Co(NO3)2 182.943 and 84.03 g/100 mL (0 C);
  CoCl2 129.839 and 52.9 g/100 mL (20 C); K2Cr2O7 294.182 and 15.1 g/100 g (no
  temperature given); K2CrO4 194.189 and 65.0 g/100 mL (no temperature given);
  NiCl2 129.5994 and 67.5 g/100 mL (25 C); CuSO4 159.60 and 201 g/L (20 C);
  KMnO4 158.032 and 76 g/L (25 C); NaCl 58.44 and 360 g/L (25 C).  PhET's molar
  masses match to 5.6e-5 relative and its saturation points to 0.0-0.6 % for
  the four quoted near room temperature (K2CrO4, KMnO4, NiCl2, K2Cr2O7); the
  worst gap is cobalt(II) nitrate at 23 %, whose only usable infobox figure is
  at 0 C.  PhET's "drink mix" has sucrose's molar mass to a milligram per mole.

  NO molar-absorptivity literature value could be sourced offline here.  Three
  sources were tried and all three carry only qualitative colour: Wikipedia's
  "Molar attenuation coefficient" (no numerical example for any substance),
  "Metal aquo complex" (a colour column, no wavelengths and no coefficients) and
  "Permanganate" (a spectrum figure, no printed lambda_max and no epsilon).  The
  spectra therefore stand as PhET's own digitised data, are labelled as such on
  the canvas and in the panel, and no literature comparison is invented for
  them.  "Still unverified" is the honest answer for those eight curves.

  The CIE 1931 2-degree colour-matching functions are the CIE's own table
  (DOI 10.25039/CIE.DS.xvudnb9b, ISO/CIE 11664-1:2019), at one row per
  nanometre -- the same grid the spectra are on, so the colour integral
  interpolates and resamples nothing.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  Displaced volume is ignored, as PhET ignores it: dissolving solute does not
  change the solution's volume here, which is why a mass percent can be taken
  with the solvent mass as V x 1000 g/L.  The solute is a single species with
  one saturation point and no temperature, no ionic strength, no activity and
  no common-ion effect: PhET's model, and the sim says so.  The clock runs at a
  fixed 1/60 s per frame so the headless suites are deterministic, and the
  shaker's particle scatter comes from a seeded generator for the same reason.
  PhET's own model.md disagrees with PhET's own code in two places, and the
  CODE is what is implemented here: the doc writes the concentration clamp
  against stockSolutionConcentration where ConcentrationSolution clamps against
  the SATURATED concentration, and it writes the precipitate as a difference of
  concentrations where the code takes a difference of moles.

  NOT MODELLED
  ------------
  Temperature, activity coefficients, ionic strength, common-ion and
  complex-formation effects, dissolution kinetics (solid appears and vanishes
  instantly at the saturation point), scattering and reflection at the cuvette
  faces, stray light, the detector's own noise and dynamic range, and
  chemical deviations from Beer-Lambert at high concentration -- a real
  solution stops being linear above roughly 0.01 M, which every one of PhET's
  Beer's Law ranges except the three micromolar ones runs past.  The sim draws
  that boundary and names it rather than pretending it is not there.  Also
  absent, being PhET's interface rather than its chemistry: the sounds, the
  voicing and alt-text layers, the artwork, the combo boxes, the draggable
  ruler, and the drag-the-shaker-to-shake gesture (a checkbox does it here).
"""

FULL_COMMENT = """<!--
  ===================================================================
  beers-law-lab.html -- a remake of PhET's Beer's Law Lab: make a
  solution in a beaker, then shine a light through it and measure what
  comes out
  ===================================================================

  Remake of PhET Interactive Simulations' Beer's Law Lab (University of
  Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's beers-law-lab 1.8.7, whose two
  screens are Concentration (a shaker and a dropper of one of nine
  solutes into a 1 L beaker, with a faucet, a drain, an evaporator, a
  concentration meter, and a saturation point where solid appears) and
  Beer's Law (a monochromatic source through a cuvette of adjustable
  width into a detector reading absorbance or transmittance, with the
  wavelength either at the solution's lambda_max or set by hand).

  Six views.  THE BEAKER is PhET's Concentration screen and THE CUVETTE
  is its Beer's Law screen.  THE SPECTRUM, THE LAW, THE LEDGER and TRUE
  COLOUR are this file's own analysis: PhET's eight absorption spectra
  with the beam on them, the straight line A = eps l c against the
  exponential T = 10^-A it implies, the beaker's mole ledger drawn as a
  ledger, and the colour the solution really transmits worked out over
  the CIE 1931 observer and laid beside PhET's interpolated ramp.
%s-->""" % COMMON

BASICS_COMMENT = """<!--
  ===================================================================
  concentration.html -- a remake of PhET's Concentration: make a
  solution in a beaker and watch what the number on the meter does
  ===================================================================

  Remake of PhET Interactive Simulations' Concentration (University of
  Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's concentration 1.8.6, which is
  the Concentration screen of Beer's Law Lab shipped on its own: a
  shaker and a dropper of one of nine solutes into a 1 L beaker, with a
  faucet, a drain, an evaporator, a concentration meter reading mol/L
  or mass percent, and a saturation point where solid appears.

  It runs on the same engine as beers-law-lab.html in this directory,
  trimmed to that one screen.  Four views.  THE BEAKER is PhET's
  screen.  THE LEDGER, THE SOLUTES and TRUE COLOUR are this file's own
  analysis: the mole ledger drawn as a ledger with the saturation
  ceiling on it, the nine solutes' molar masses and solubilities
  against the literature, and the colour the solution really transmits
  worked out over the CIE 1931 observer and laid beside PhET's
  interpolated ramp.
%s-->""" % COMMON

if BASICS:
    title = 'Concentration &mdash; the beaker, the mole ledger and the saturation point'
    h1 = 'concentration'
    sub = ('A remake of PhET&rsquo;s Concentration: nine solutes, a dropper, a faucet, a drain '
           'and an evaporator into one litre &mdash; and the ledger C = n/V that ties them '
           'together, with the solid that appears when it runs out of room')
    comment = BASICS_COMMENT
    out = os.path.join(HERE, '..', 'concentration', 'p1_head.html')
else:
    title = 'Beer&rsquo;s Law Lab &mdash; the beaker, the cuvette and A = &epsilon;lc'
    h1 = 'beer&rsquo;s law lab'
    sub = ('A remake of PhET&rsquo;s Beer&rsquo;s Law Lab: make the solution, then measure it '
           '&mdash; A = &epsilon;lc exactly, T = 10<sup>&minus;A</sup> exactly, and the colour '
           'the cuvette really transmits worked out over the CIE observer')
    comment = FULL_COMMENT
    out = os.path.join(HERE, 'p1_head.html')

head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%s</title>\n%s\n%s<header>\n  <h1>%s</h1>\n'
        '  <span class="sub" id="sub">%s</span>\n  <nav id="tabs"></nav>\n</header>\n%s'
        % (title, comment, SCAFFOLD_STYLE, h1, sub, SCAFFOLD_BODY))
io.open(out, 'w', encoding='utf-8').write(head)
print('%s: %d lines, %.1f KB' % (os.path.relpath(out, HERE), len(head.splitlines()),
                                 len(head.encode()) / 1024))
