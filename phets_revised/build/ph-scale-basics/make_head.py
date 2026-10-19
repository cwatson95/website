#!/usr/bin/env python3
"""Write p1_head.html: this sim's own <head>, header comment, <h1> and tagline, followed by
build/ph-scale/p1_head.html's <style> ... <body> block VERBATIM.

The scaffold is extracted rather than retyped (PLAYBOOK 4), and the extraction is cut on
'<style>' and on the end of the body markup, so the two builds cannot drift apart in the
palette, the site nav or the stage layout.  Only the title, the h1 and the .sub line are
edited, which is exactly what the PLAYBOOK allows."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, '..', 'ph-scale', 'p1_head.html'), encoding='utf-8').read()
tail = src[src.index('<style>'):]

OLD_H1 = '  <h1>pH scale</h1>'
NEW_H1 = '  <h1>pH scale: basics</h1>'
assert tail.count(OLD_H1) == 1
tail = tail.replace(OLD_H1, NEW_H1)

i = tail.index('<span class="sub" id="sub">')
j = tail.index('</span>', i) + len('</span>')
NEW_SUB = ('<span class="sub" id="sub">A remake of PhET&rsquo;s pH Scale: Basics &mdash; '
           'PhET&rsquo;s Macro screen on its own: pour out one of twelve everyday liquids, '
           'dip the meter, add water, and see how little the number moves &mdash; because '
           'what dilutes is C = [H<sub>3</sub>O<sup>+</sup>] &minus; [OH<sup>&minus;</sup>], '
           'not the pH</span>')
tail = tail[:i] + NEW_SUB + tail[j:]

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>pH Scale: Basics &mdash; one beaker, twelve liquids, and the exact dilution law</title>
<!--
  ===================================================================
  ph-scale-basics.html — a remake of PhET's pH Scale: Basics: PhET's
  Macro screen as its own sim, with the dilution law done exactly
  ===================================================================

  Remake of PhET Interactive Simulations' pH Scale: Basics (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's ph-scale-basics 1.7.5, whose
  ONE screen is the Macro screen of pH Scale: pick one of twelve
  everyday liquids, pour it from the dropper, dip the pH meter, run the
  tap to dilute it, open the drain.  PhET's Basics sim shows a pH and a
  volume and nothing else — no concentrations, no moles, no particle
  counts — and this remake keeps that in the beaker view.

  THE SAME ENGINE AS ph-scale.html.  The chemistry, the beaker's state
  and clock, the readout and three of the four views are the very same
  part files, taken by path and pinned by SHA-256 in
  build/ph-scale-basics/assemble.py: build/ph-scale/p2_chem.js,
  p3_state.js, p4_views.js and p7_refs.js.  What differs is this head,
  the sim's identity (four tabs, and no concentrations in the beaker
  readout), one extra view, the control panel and the test suite.  The
  full sim's other three screens — the particle picture, the
  concentration graph and My Solution — are simply absent, which is
  PhET's own difference between the two sims.

  Four views.  THE BEAKER is PhET's Macro screen.  THE LIQUIDS is this
  file's own: PhET's twelve as a table, with the measured range where
  one could be sourced and what a full beaker of water does to each.
  DILUTION and THE SCALE are the two analysis views ph-scale carries,
  unchanged.

  WHAT IS EXACT HERE
  ------------------
  The chemistry, as exact arithmetic, with Kw = 1.000e-14 mol^2/L^2
  (pKw = 14.000) — the conventional value at 25 C, and the one PhET's
  hard-coded 14 encodes.  Neutral is therefore pH 7.000 exactly.

      [H3O+] = 10^-pH,   [OH-] = Kw/[H3O+],   n = cV,   N = n N_A

  with N_A the exact SI 2019 value 6.02214076e23.  Every concentration
  is asserted against 50-digit `decimal` evaluation in
  build/ph-scale/derive.py over the whole scale INCLUDING its ends.
  [OH-] is written as a division on purpose: PhET's spelling
  10^-(14-pH) is out by up to 2.1e-15 because pH - 14 is inexact in a
  double whenever pH < 7, while the division is out by 2.1e-16 and
  keeps [H3O+][OH-] = Kw to a rounding.

  DILUTION is where a sloppy model shows, so it is done properly.  What
  dilutes is not the pH and not either ion but the NET STRONG ACID

      C = [H3O+] - [OH-] = -2 sqrt(Kw) sinh( ln10 (pH - 7) ),

  a difference of ANALYTICAL concentrations — the spectator ions cancel
  out of the charge balance — whose moles are therefore conserved on
  mixing.  Water carries C = 0 exactly.  So mixing V1 of pH1 with V2 of
  pH2 is

      C = (C1 V1 + C2 V2)/(V1 + V2),  then re-solve [H3O+] - Kw/[H3O+] = C,
      pH = 7 - asinh( C / (2 sqrt(Kw)) ) / ln10.

  That re-solve is the water autoionisation PhET's rule leaves out.  It
  is implemented twice (the asinh closed form and the stable branch of
  the quadratic root) and asserted against a Decimal mole ledger plus a
  scipy brentq root of the charge balance.  The stable branch is
  load-bearing: the textbook root (C + sqrt(C^2 + 4Kw))/2 is out by
  3.6e-5 at pH 13, 8.0e-4 at pH 14 and 11 % at pH 15, all of which
  PhET's range reaches, and derive.py asserts it is STILL that bad so
  the branch cannot be deleted.  Two structural facts fall out and are
  asserted: diluting f-fold divides C by exactly f, and C is an ODD
  function about pH 7, so pH 2 and pH 12 are exactly as strong as each
  other and equal volumes of them are exactly neutral.

  WHAT IS PhET'S RULE, AND WHERE IT DIFFERS
  -----------------------------------------
  PhET mixes the MAJORITY ion linearly and takes a log (doc/model.md
  and PHModel.computePH), never re-solving, so water's own
  autoionisation is counted on the majority side and ignored on the
  minority side.  Both laws are implemented and a chip switches between
  them.  Over everything this beaker can reach (pH -1..15,
  0.015..1.2 L of liquid in 1.2 L) the two never differ by more than
  0.0948 pH, at pH 4.91 with 0.015 L in the beaker; at PhET's own
  liquids the worst is 0.0815 pH (chicken soup, 0.1 L in 1.2 L).  It is
  a small error and a real one, it vanishes undiluted and at infinite
  dilution, and it is an odd function about pH 7.  Volume-averaging the
  pH — the mistake the dilution view exists to rule out — is wrong by
  up to 4.42 pH.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  Every liquid is treated as a STRONG acid or base of the stated pH:
  fully dissociated, with a spectator counter-ion and no buffering.
  That is PhET's model too, and for blood it is a fiction — blood is a
  bicarbonate buffer and diluting it does not move its pH the way this
  shows.  The sim says so on the canvas.  Temperature is fixed: pKw is
  14.000 and does not move.  Activity coefficients are ignored, which
  is why battery acid can be called pH 1 at all.  The solute colour is
  PhET's own law (water colour to the colour-stop colour over the first
  quarter of the mixture, then to the stock colour), reimplemented from
  its arithmetic.  The clock runs at a fixed 1/60 s per frame so the
  headless suites are deterministic, and the dropper and faucets run at
  PhET's rates (0.05 and 0.25 L/s).

  NOT MODELLED
  ------------
  Weak acids and bases, buffers, ionic strength and activity, carbonate
  equilibria, temperature, mixing kinetics, and any solute chemistry at
  all: two liquids mixed here interact only through H3O+ and OH-.  Also
  absent, being PhET's interface rather than its physics: the sounds,
  the voicing and alt-text layers, the artwork and the combo box.  Two
  things differ from PhET's: the dropper starts loaded with orange juice
  rather than water, so the beaker shows something the moment it opens,
  and the beaker starts autofilled with PhET's 0.5 L.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's values, read from docs/phets/ph-scale-basics_en.html (1.7.5)
  and its shared PH_SCALE code: the twelve liquids' names, pH values and
  colours (battery acid 1, blood 7.4, chicken soup 5.8, coffee 5, drain
  cleaner 13, hand soap 10, milk 6.5, orange juice 3.5, soda pop 2.5,
  spit 7.4, vomit 2, water 7); the beaker's 1.2 L and its 0.015 L
  minimum; the pH range -1 to 15 and its two decimal places; the
  dropper's 0.05 L/s, the faucets' 0.25 L/s and the autofill's 0.5 L at
  0.45 L/s; water at 55 mol/L; the colour law's 0.25 stop.  Chemistry:
  Kw = 1e-14 at 25 C by convention, N_A = 6.02214076e23 (SI 2019,
  exact).  Measured pH ranges, four of the twelve, quoted to their
  sources' own precision: BLOOD 7.37-7.43 (Merck Manual Professional,
  "Acid-Base Regulation", J. L. Lewis III: "a pH of 7.43 to 7.37");
  ORANGE JUICE 3.30-4.19 and MILK 6.40-6.80 and CHICKEN BROTH 5.80
  (FDA, "Approximate pH of Foods and Food Products").  PhET's value
  lies inside every one of those four.  No measured range could be
  sourced here for the other eight, and the canvas says which is which
  rather than inventing one.  Every reference value the suite asserts
  is a line of build/ph-scale/refvals.txt, the output of derive.py.
-->
'''

io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(HEAD + tail)
print('p1_head.html: %d lines (%d of them the extracted scaffold)'
      % (len((HEAD + tail).splitlines()), len(tail.splitlines())))
