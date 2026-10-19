#!/usr/bin/env python3
"""Build p1_head.html from the house scaffold (projects/simulations/build_buoy/p1_head.html):
the two <style> blocks and the body markup are copied VERBATIM; only the <title>, the header
comment, the site-nav hrefs (absolute: ../website/ is dead from docs/phets_revised/), the <h1>,
the .sub tagline and the role-colour comment change.  Same recipe as
build/waves-intro/make_head.py, against the same source file."""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p1_head.html')
s = io.open(SRC, encoding='utf-8').read()

TITLE = "Greenhouse Effect &mdash; the layer model, solved exactly"
H1 = "Greenhouse effect"
SUB = ("A remake of PhET&rsquo;s Greenhouse Effect: sunlight in, infrared out, and a stack of "
       "absorbing layers in between &mdash; with the steady state solved in closed form, "
       "T<sub>s</sub> = T<sub>eff</sub>[1 + &Sigma; a/(2&minus;a)]<sup>1/4</sup>")
HEADER = """<!--
  ===================================================================
  greenhouse-effect.html — a remake of PhET's Greenhouse Effect: the
  waves, the photons and the layer model, on one exactly-solvable
  radiative-equilibrium engine
  ===================================================================

  Remake of PhET Interactive Simulations' Greenhouse Effect (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's greenhouse-effect 1.3.13, whose
  three screens (Waves, Photons, Layer Model) all run on one "layers
  model": a stack of sheets that pass sunlight and absorb infrared.
  Its constants were read out of the minified original in
  docs/phets/greenhouse-effect_en.html and are cited as PhET's values
  wherever they appear.

  Five views.  THE WAVES and THE PHOTONS are PhET's first two screens:
  the same 12-layer atmosphere, greenhouse-gas concentration set either
  by a slider or by a date (ice age, 1750, 1950, 2020), a cloud, a
  surface albedo that turns glacial at the ice age, the thermometer in
  K / °C / °F, the energy-balance meter at the top of the atmosphere
  and the flux meter — drawn once as waves whose brightness is the
  actual transmitted flux, and once as individual photons absorbed and
  re-emitted by a seeded random number generator.  THE LAYERS is PhET's
  Layer Model screen: 0 to 3 explicit sheets, their absorbance, the
  solar intensity from 1/2 to 2 suns, the surface albedo, and each
  sheet's own temperature.  THE LADDER and THE RECORD are this file's
  own analysis: the law the whole sim obeys, drawn; and PhET's four
  dates against the real climate record, with the line between physics
  and fit drawn explicitly.

  WHAT IS EXACT HERE
  ------------------
  The whole model.  For N sheets of infrared absorbance a_i over a
  ground of albedo alpha under an absorbed solar flux F, each sheet
  conserving energy makes the NET upward flux the same at every level,
  so U_i = U_{i-1} - F a_i/(2 - a_i), and with U_N = F at the top,

      sigma T_s^4 = F [ 1 + sum_i a_i/(2 - a_i) ].

  That is derived in build/greenhouse-effect/derive.py, implemented
  twice in this file (the recursion above, and a dense Gaussian solve
  of the full 13-unknown flux system that never uses the invariant),
  and asserted against a forward-Euler march of PhET's own layer ODE.
  Energy balance is asserted at every sheet, at the ground and at the
  top of the atmosphere to 1e-9 W/m^2, and the net flux is asserted
  constant with altitude.  For a_i = 1 it collapses to the textbook
  T_s = (N+1)^(1/4) T_eff, which is asserted at every N from 0 to 12.
  The Stefan-Boltzmann constant is asserted against scipy's CODATA
  value AND against 2 pi^5 k^4 / 15 h^3 c^2 built from CODATA h, c, k;
  the Earth's effective temperature, 254.578 K, comes from the 2015 IAU
  nominal solar irradiance 1361 W/m^2 and a Bond albedo of 0.30.
  The photon picture is tied to the flux solution exactly: the chance
  that an infrared photon leaving the ground escapes to space, under
  "absorbed with probability a_i, then re-emitted up or down with
  probability 1/2", is F/sigma T_s^4 — proved here as a Markov chain,
  as the closed form, and by a seeded Monte Carlo (the sim and derive.py
  share one 32-bit generator whose stream is pinned bit for bit).
  One more exact statement, about PhET's own convention: PhET's sheet
  absorbs a fraction a but emits a FULL blackbody sigma T^4 in each
  direction, which is not Kirchhoff's law.  It makes no difference at
  all to the fluxes or to the surface temperature — the emitted flux
  per direction is a(U+D)/2 either way — and changes every sheet's
  reported temperature by exactly a^(-1/4).  Both are printed.

  WHAT IS PhET'S FIT, NOT PHYSICS
  -------------------------------
  Everything that turns a greenhouse-gas concentration into an
  absorbance.  PhET's concentration screens use twelve sheets at
  i x 50000/13 m with

      a_i = 0.85 c exp(-altitude/8400 m),

  and map its four dates to c = 0.625 (ice age), 0.7147 (1750),
  0.7182 (1950), 0.7446 (2020).  Those five numbers, the sun's
  343.6 W/m^2, the albedos 0.2 / 0.225 / 0.3, the cloud's 12.5 %, and
  the CO2 / CH4 / N2O values printed beside each date are PhET's,
  quoted as PhET's and not adjusted.  They are a teaching fit, not a
  radiative-transfer calculation: no line strengths, no bands, no
  overlap, no water vapour, no lapse rate.  What comes OUT of them is
  this file's exact solve, and the answer is worth stating plainly —
  PhET's 1750 surface temperature is 296.48 K (23.3 °C), about 8.5 K
  above the real Earth's 288 K, while the DIFFERENCES between its dates
  are good: the ice age is 6.29 K colder than 1750 (the Last Glacial
  Maximum was about 6 K colder) and 2020 is 1.32 K warmer than 1750
  (the observed figure is about 1.2 K).  PhET tuned the changes, not
  the absolute level.  The independent check that this really is PhET's
  model: the hottest state its concentration screens can reach is
  309.13 K by this solve, and PhET hard-codes 309 as its thermometer's
  EXPECTED_MAX_TEMPERATURE.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  The temperature is integrated with PhET's own heat capacities (a
  sheet's response is 85000/(85000 x 3e-7 x rho x c_p) K per J/m^2:
  exactly 32/15 for the ground, 1.5873 for a glass sheet), from PhET's
  own starting state (the ground at its 245 K night floor, every sheet
  at 0 K), in four forward-Euler sub-steps of a 1/60 s frame — which is
  well inside the ODE's stability bound of h < 0.0198 s at 520 K, and
  the sim clamps against that bound.  It settles in about 30 s of model
  time; the exact steady state is printed alongside the live value, and
  a button jumps to it.  The waves are drawn, not solved: their
  brightness is the model's own transmitted flux at that height, which
  is more honest than PhET's decorative per-layer attenuators and is
  labelled on the canvas.  The flux meter and its draggable sensor
  likewise read the LIVE model, and the meter draws the exact steady
  profile beside it: settled, the two coincide to 1e-8 W/m^2 (asserted);
  with the sun switched off they part company and the meter follows the
  model.  The photons ARE simulated, with PhET's own
  rules (created at the ground at sigma T^4/7.8 per second, one in five
  drawn unless "more photons"; absorbed with probability a_i on
  crossing a sheet; re-emitted after a fixed hold, up or down at even
  odds), but as in PhET they are a display: the energy that sets the
  temperature is the flux model, not the photon count, and the sim says
  so.  The altitude axis is compressed by a factor printed on the
  canvas.  The clock advances a fixed 1/60 s per frame so the headless
  suites are deterministic.

  NOT MODELLED
  ------------
  Everything that is not radiation: no convection, no lapse rate, no
  latent heat, no water vapour feedback, no ocean, no clouds beyond
  PhET's one 12.5 % reflector, no day and night, no latitude, no
  spectral detail whatever — a real atmosphere's infrared opacity is a
  forest of lines, and "absorbance a" stands in for all of it.  The
  Earth in this model is a single point with one temperature.  Also
  absent from this remake, being PhET's interface rather than its
  physics: the sounds, the voicing and alt-text layers, the animated
  glacier and cloud artwork, the flux meter as a box you drag around
  (its SENSOR is draggable here; the panel is fixed beside the window),
  PhET's "pause / step / speed" trio (here: a time checkbox, one step
  and a jump-to-equilibrium button), and its per-layer wave
  attenuators.  Two things differ from PhET's: the sun starts SHINING,
  so a view shows something the moment it opens (PhET's "start
  sunlight" button is a "cold start" button here), and the twelve
  sheets of the concentration screens are DRAWN, faintly, with an
  opacity that follows each sheet's absorbance -- PhET keeps them
  invisible on those screens, and the captions here point at them.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's values, read from docs/phets/greenhouse-effect_en.html
  (1.3.13): the sun's 343.6 W/m^2 and its 0.5-2 x range; the albedos
  0.2 (green meadow), 0.225 (partially glaciated) and 0.3 (layer
  model), the slider's 0-0.9; the 50 km top of atmosphere and the
  sheet spacing 50000/(N+1); 12 sheets on the concentration screens
  and 3 on the layer model, absorbance 0.1-1; a_i = 0.85 c
  exp(-z/8400); the four dates' concentrations and their CO2 (180, 277,
  311, 413 ppm), CH4 (380, 694, 1116, 1889 ppb) and N2O (215, 271, 288,
  333 ppb); the cloud's 12.5 % (0.125 x 85000/18000 x 18000/85000
  exactly); the 245 K night floor and the 125 K layer-model floor;
  sigma = 5.670374419e-8; the densities and heat capacities 1250/1250
  (earth) and 2500/840 (glass) with the 3e-7 volume coefficient; the
  photon rules and rates; and the thermometer's 309 K expected maximum.
  Physics, from scipy's CODATA: sigma = 5.670374419184e-8 W/m^2/K^4,
  h, c, k.  Cited scalars: the 2015 IAU nominal total solar irradiance
  1361 W/m^2, Earth's Bond albedo 0.30 (NASA's fact sheet gives 0.306,
  which moves T_eff by 0.55 K), the conventional global mean surface
  temperature 288 K, the Last Glacial Maximum about 6 K below
  pre-industrial, and about 1.2 K of observed warming since 1750.
  Nothing else is measured, and nothing was taken from PhET's code or
  assets.
-->"""

NAV_OLD = ['../website/index.html', '../website/about.html', '../website/teaching.html',
           '../modules/teaching_modules.html', '../website/simulations.html',
           '../website/research.html', '../website/cv.html']
NAV_NEW = ['https://cooper-watson.net/index.html', 'https://cooper-watson.net/about.html',
           'https://cooper-watson.net/teaching.html',
           'https://cooper-watson.net/modules/teaching_modules.html',
           'https://cooper-watson.net/simulations.html', 'https://cooper-watson.net/research.html',
           'https://cooper-watson.net/cv.html']

i0 = s.index('<title>')
i1 = s.index('</title>') + len('</title>')
s = s[:i0] + '<title>' + TITLE + '</title>' + s[i1:]
c0 = s.index('<!--')
c1 = s.index('-->', c0) + 3
assert c0 < s.index('<style>')
s = s[:c0] + HEADER + s[c1:]
for a, b in zip(NAV_OLD, NAV_NEW):
    assert s.count('href="%s"' % a) == 1, a
    s = s.replace('href="%s"' % a, 'href="%s"' % b)
assert s.count('<h1>Buoyancy</h1>') == 1
s = s.replace('<h1>Buoyancy</h1>', '<h1>' + H1 + '</h1>')
m = re.search(r'<span class="sub" id="sub">.*?</span>', s)
s = s[:m.start()] + '<span class="sub" id="sub">' + SUB + '</span>' + s[m.end():]
old_roles = s[s.index('    /* role colours:'):s.index('*/', s.index('    /* role colours:')) + 2]
new_roles = ("    /* role colours: green = the computed thing (the surface temperature and the\n"
             "       flux solution), orange = the reference (the bare effective temperature, the\n"
             "       closed form, the real Earth), magenta = the live marker (the concentration\n"
             "       or date you have set, the thermometer's reading), cyan = structure (the\n"
             "       sheets, the altitude axis, the sunbeam). */")
s = s.replace(old_roles, new_roles)
assert 'Buoyancy' not in s and 'buoyancy' not in s.lower()
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(s)
print('p1_head.html: %d lines' % len(s.splitlines()))
