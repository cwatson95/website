#!/usr/bin/env python3
"""Build p1_head.html from the house scaffold (projects/simulations/build_buoy/p1_head.html):
the two <style> blocks and the body markup are copied VERBATIM; only the <title>, the header
comment, the site-nav hrefs (absolute: ../website/ is dead from docs/phets_revised/), the <h1>,
the .sub tagline and the role-colour comment change.  Same recipe as
build/wave-interference/make_head.py, against the same source file."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p1_head.html')
s = io.open(SRC, encoding='utf-8').read()

TITLE = "Waves Intro &mdash; water, sound and light on one lattice"
H1 = "Waves intro"
SUB = ("A remake of PhET&rsquo;s Waves Intro: one source in a ripple tank of water, of air, of light &mdash; "
       "PhET&rsquo;s own lattice with three rulers and three clocks, and v = f&lambda; measured on it")
HEADER = """<!--
  ===================================================================
  waves-intro.html — a remake of PhET's Waves Intro: one wave source
  in water, in sound and in light, on PhET's own 2-D lattice, plus the
  law that ties the three together, v = f lambda, measured on the
  lattice itself
  ===================================================================

  Remake of PhET Interactive Simulations' Waves Intro (University of
  Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's waves-intro 1.1.24, whose model
  note reads "This simulation is a subset of the Wave Interference
  simulation, which shows one scene per screen": its three screens,
  their controls, and its model constants, read from the minified
  original in docs/phets/waves-intro_en.html.

  Four views.  WATER, SOUND and LIGHT are PhET's three screens: one
  hard source five cells in from the left edge of a 151 x 151 lattice
  (111 x 111 visible), with frequency and amplitude, PhET's green
  button (continuous: it switches the source on and off; pulse: it
  fires one period and pops back up), the graph of the centre line, the
  tape measure, the stopwatch and the two-probe wave meter, normal and
  slow speed, pause, one step and clear.  Water adds PhET's top and
  side views, sound its air parcels (waves / particles / both) and
  PhET's tone, light the screen at the right-hand edge, drawn through
  PhET's own brightness pipeline.  THE THREE MEDIA (analysis) is this
  file's own: the law v = f lambda as three parallel lines on a log-log
  plane, one per medium, and underneath, for each medium, the steady
  state along the axis of the tank with the wavelength MEASURED on the
  lattice by least squares and compared with v/f.

  WHAT IS EXACT HERE
  ------------------
  The engine is the one built and pinned for wave-interference.html
  (build/wave-interference/p2_engine.js, unchanged, API in its
  ENGINE.md): PhET's lattice (5-point leapfrog, C = 1/2, 151 cells,
  20-cell pad, the source cell driven at 1.2 x the amplitude), Mur's
  second-order absorbing edge, and a time step SOLVED at every
  frequency from the lattice's own dispersion relation
  sin^2(w dt/2) = C^2 [sin^2(kx dx/2) + sin^2(ky dx/2)], so that the
  wavelength v/f and the period 1/f are exact along the lattice axes
  (PhET keeps one step per medium, which makes its wavelengths 0.7 % to
  3.2 % short).  That engine's own proof — the dispersion relation, the
  calibration of all three media, Mur's reflection, and a numpy twin
  that repeats every operation — is not re-derived here: the lines this
  file needs are read from build/wave-interference/refvals.txt, and
  this build's own numpy twin reproduces that file's tank and pulse
  scenarios to 1e-13 before adding its own (sound at 0.2937 per ms,
  light, a source switched off and on again, the light screen).
  New and exact here: PhET's light screen as Waves Intro draws it (a
  3-row smoothing, a +/-39-row box average, and PhET's piecewise-linear
  brightness table, all read from the original); PhET's tone mapping
  (1000 f Hz at output level 0.3 A/10) and a looped tone buffer of
  whole cycles; and the steady-state measurement — a least-squares fit
  against the drive's own phase at every cell of the axis, the
  wavelength from the slope of the phase.  Every reference value is a
  line of build/waves-intro/refvals.txt, the output of derive.py.

  WHAT IS MEASURED, AND WHAT THE MEASUREMENT FINDS
  ------------------------------------------------
  Fitted over cells 30 to 100 from the source, the lattice's own
  wavelength agrees with v/f to 0.03 % (light), 0.08 % (water) and
  0.15 % (sound) at PhET's default frequencies, and the envelope falls
  as 1/sqrt(r) (fitted exponent -0.47 to -0.54).  At water's lowest
  frequency, 0.25 Hz, the tank is only 1.4 wavelengths long and the
  reading is 1.6 % short: about a third of that is the 2-D near field
  (the phase of the Hankel function H0(kr), scipy: 0.46 %) and the rest
  is the tank's edges — on a 401-cell lattice, with the same source,
  the same screen and the same fit, the reading returns to 0.49 %.
  Likewise the light screen's profile departs from the 1/r law of a
  point source by up to 9 %: a ripple of about one wavelength's period
  left by waves the edges reflect (rms 2.0 % on PhET's 151 cells,
  1.5 % on 401, 0.75 % on 601) on a smooth tilt of about 6 % that is
  the square lattice's own anisotropy.  PhET's +/-39-row screen average
  smooths the ripple away.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  Waves are scalar and linear; the source is a hard (Dirichlet) cell,
  as PhET's is, so each 2-D source is a line source and its waves fade
  as 1/sqrt(r).  PhET drives its source with -sin and this engine with
  +sin: the same solution with the first half-period the other way up.
  Sound's air parcels are pushed along grad p (xi = grad p / rho
  omega^2 for one frequency), exaggerated: the scaling makes a wave at
  PhET's full colour move a parcel 0.3 of the parcel spacing, and
  beside the source, where the field is stronger than full colour, the
  push reaches 0.39 of it (derive.py) — still far short of the spacing
  that would make the rows cross.  PhET instead gives each parcel a
  spring, a damper and a random jitter.  Colours: the water and sound
  ramps are chosen; light's hue is the CIE 1931 colour of the
  wavelength (desaturated into sRGB), its brightness the field.  The clock advances a fixed
  1/60 s per frame so the headless suites are deterministic.  The tone
  is computed here as samples and played from a looped buffer, not from
  an OscillatorNode, so that the suite can check it.

  NOT MODELLED
  ------------
  PhET's falling water drops (here the source starts at once, and the
  frequency and amplitude take effect at once rather than when the next
  drop lands), the animated rotation into the side view (here a
  switch), its interpolation between lattice frames, its temporal mask
  (a display trick that hides lattice ringing after a source stops),
  the light screen's sheared perspective (here a plain strip), its
  "Sound Effect" sonification of light, the water-drop sounds, and the
  stopwatch and wave meter as draggable boxes (here: a readout box and
  a fixed chart).  Two defaults differ from PhET's, both so that a view
  shows something the moment it opens: the source starts ON (PhET opens
  every screen blank, waiting for the button) and the light screen
  starts SHOWN.  One control is PhET's Wave Interference rather than
  PhET's Waves Intro: the intensity graph, which Waves Intro builds
  with showIntensityCheckbox:false and therefore can never show.  It is
  off by default here and labelled on the page.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's values, read from docs/phets/waves-intro_en.html (1.1.24): the
  lattice (151 cells, pad 20, C = 1/2, the source column 25 and row 75),
  20 x 111/61 lattice steps per second of wall time, the amplitude
  calibration 1.2, the colour scale 2.14, the amplitude range 0 to 10
  and its initial 8, the three media (widths 10 cm / 500 cm / 5000 nm,
  speeds 1.65 cm/s / 34.3 cm/ms / 299.792458 nm/fs, frequency ranges,
  scale bars, time scales, the frequency starting mid-range), the
  90-step intensity history and its 3-row smoothing, the light screen's
  +/-39-row window and its piecewise-linear brightness table, and the
  tone's 1000 f Hz and 0.3 A/10.  Colour: the CIE 1931 2-degree table
  (DOI 10.25039/CIE.DS.xvudnb9b) every 5 nm, from the file the
  blackbody-spectrum build fetched from the CIE; the sRGB matrix.
  Nothing else is measured, and nothing was taken from PhET's code or
  assets.
-->"""

NAV_OLD = ['../website/index.html', '../website/about.html', '../website/teaching.html',
           '../modules/teaching_modules.html', '../website/simulations.html',
           '../website/research.html', '../website/cv.html']
NAV_NEW = ['https://cooper-watson.net/index.html', 'https://cooper-watson.net/about.html',
           'https://cooper-watson.net/teaching.html', 'https://cooper-watson.net/modules/teaching_modules.html',
           'https://cooper-watson.net/simulations.html', 'https://cooper-watson.net/research.html',
           'https://cooper-watson.net/cv.html']

i0 = s.index('<title>'); i1 = s.index('</title>') + len('</title>')
s = s[:i0] + '<title>' + TITLE + '</title>' + s[i1:]
c0 = s.index('<!--'); c1 = s.index('-->', c0) + 3
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
new_roles = ("    /* role colours: green = the computed thing (the lattice's field and the\n"
             "       wavelength measured on it), orange = the reference (v = f lambda, the\n"
             "       1/sqrt(r) envelope, the 1/r screen, PhET's own calibration), magenta = the\n"
             "       live marker (the source, its button, the tools), cyan = structure (the\n"
             "       generator, the fit window, each medium's frequency range). */")
s = s.replace(old_roles, new_roles)
assert 'Buoyancy' not in s and 'buoyancy' not in s.lower()
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(s)
print('p1_head.html: %d lines' % len(s.splitlines()))
