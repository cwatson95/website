#!/usr/bin/env python3
"""Build p1_head.html from the house scaffold (projects/simulations/build_buoy/p1_head.html):
the two <style> blocks and the body markup are copied VERBATIM; only the <title>, the header
comment, the site-nav hrefs (absolute: ../website/ is dead from docs/phets_revised/), the <h1>,
the .sub tagline and the role-colour comment change.  p1_utils.js is copied unchanged."""
import io, os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p1_head.html')
s = io.open(SRC, encoding='utf-8').read()

TITLE = "Wave interference &mdash; ripples, two sources, slits and the far field"
H1 = "Wave interference"
SUB = ("A remake of PhET&rsquo;s Wave Interference: water, sound and light on PhET&rsquo;s own lattice &mdash; "
       "one source, two sources, one and two slits, and the far-field pattern of an aperture as its Fourier transform")
HEADER = """<!--
  ===================================================================
  wave-interference.html — a remake of PhET's Wave Interference:
  waves on a 2-D lattice from one source, from two, through one or two
  slits, and the far-field pattern of an aperture as its Fourier
  transform; plus the geometry of the path difference and the lattice's
  own dispersion relation
  ===================================================================

  Remake of PhET Interactive Simulations' Wave Interference (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's wave-interference 2.0.22: its
  four screens, their controls, and its model constants.

  Six views.  THE RIPPLE TANK is PhET's Waves screen: one source on a
  151 x 151 lattice (111 x 111 visible) in water, sound or light, with
  frequency and amplitude, continuous or pulse, top or side view (water),
  waves / particles / both (sound), the screen and intensity graph
  (light), the graph of the centre line, the tape measure, the stopwatch
  and the two-probe wave meter.  TWO SOURCES is the Interference screen,
  with the nodal hyperbolae r1 - r2 = (m + 1/2) lambda drawn over the
  lattice.  THE SLITS is the Slits screen: a plane wave, no barrier, one
  slit or two, slit width, separation and a draggable barrier, and the
  screen compared with the Rayleigh-Sommerfeld sum and the Fraunhofer
  formula.  THE FAR FIELD is the Diffraction screen: PhET's ellipse,
  rectangle, circle & square, disorder and a waving figure (PhET's is a
  photograph; this one is drawn), plus a Gaussian and N slits, a
  wavelength slider, the |FFT| pattern and its horizontal cut against the
  closed forms.  PATH DIFFERENCE (analysis): the hyperbolae, their
  asymptotes and the screen, near and far.  THE LATTICE (analysis): the
  dispersion relation, phase and group speeds, the edge reflection and the
  calibration against PhET's fixed time step.

  WHAT IS EXACT HERE
  ------------------
  The lattice is PhET's (5-point leapfrog, C = 1/2, 151 cells, 20-cell
  pad) and its dispersion relation sin^2(w dt/2) = C^2 [sin^2(kx dx/2) +
  sin^2(ky dx/2)] is exact for it; the time step is SOLVED from it at
  every frequency, so the wavelength v/f and the period 1/f are exact
  along the lattice axes (PhET keeps one step per medium and is 0.7 % to
  3.2 % short).  The driven plane wave is an exact lattice solution
  (5e-15 over 20 steps, axis and diagonal).  The engine is pinned against
  a numpy twin that repeats every operation (five scenarios, 150 to 400
  steps, 1e-11).  Mur's second-order boundary: its reflection from the
  plane-wave ansatz (<= 3 % to 45 degrees), checked against a packet
  simulation to 2 %.  Two sources: the nodal hyperbolae, their count
  2 ceil(d/lambda - 1/2), exact and far-field screen positions.  At steady
  state (numpy twin) the lattice's own nodal lines sit 0.85 cells outside
  the hyperbolae on average, 1.4 at worst, all outward, where the
  continuum 1/sqrt(r) formula sits within 0.08: the lattice's anisotropy,
  stated on the view rather than hidden.  The far field: |FFT| of the
  drawn aperture against numpy.fft.fft2 (eight apertures, six bins each)
  and against a direct DFT; the pixel-snapped rectangle against the
  Dirichlet kernel (1e-15); the sampled Gaussian against its continuous
  transform (5e-16); the disc against the Airy pattern [2 J1(v)/v]^2
  (1.2e-3 of the peak for k <= 10); J0, J1, sinc^2 and the N-slit factor
  against scipy.  Every reference is a line of
  build/wave-interference/refvals.txt, the output of derive.py.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  Waves are scalar and linear; the source is a hard (Dirichlet) cell, as
  PhET's is; each 2-D source is a line source, so waves fade as 1/sqrt(r).
  The slits' theory curves use the far-zone form of the 2-D kernels
  (kr >> 1; kr >= 30 at the screen).  The lattice follows the
  Rayleigh-Sommerfeld sum on the screen to 6 % (3 % rms) and misses the
  Fraunhofer formula by 26 % at PhET's default (derive.py).  Sound's air
  parcels are pushed along grad p (xi = grad p / rho omega^2 for one
  frequency), exaggerated to at most 0.3 of their spacing.  Colours:
  water and sound ramps are chosen; light's hue is the CIE 1931 colour of
  the wavelength (desaturated into sRGB), its brightness the field.  The
  disorder aperture is a new design (fixed random offsets, Park-Miller
  seed 20260918), not PhET's table; the waving figure is new art.  The
  clock advances a fixed 1/60 s per frame so the headless suites are
  deterministic.

  NOT MODELLED
  ------------
  PhET's falling water drops (here the source starts at once), the
  animated rotation into the side view (here a switch), its interpolation
  between lattice frames (here the picture changes once per step), its
  temporal mask (a display trick hiding lattice ringing after a source
  stops), sound output ("Play Tone") and light sonification, the
  stopwatch and wave meter as draggable boxes (here: a readout box and a
  fixed chart), and PhET's separate lattice per medium (one lattice per
  view; changing the medium clears it).  Defaults differ in one way: the
  sources and the laser start ON (PhET starts them off, which opens every
  screen blank).

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's values, read from docs/phets/wave-interference_en.html: the
  lattice (151, pad 20, C = 1/2, source column 25), 20 x 111/61 steps per
  second, the amplitude calibration 1.2 and plane-wave factor 0.21, the
  colour scale 2.14, the media (widths 10 cm / 500 cm / 5000 nm, speeds
  1.65 cm/s / 34.3 cm/ms / 299.792458 nm/fs, frequency ranges, scale bars,
  source and slit ranges and defaults, time scales), the 90-step screen
  history, the barrier's range, the diffraction grid (256 over 4/3 mm),
  the aperture ranges and defaults, the lambda0/lambda rescaling and the
  log(0.01|F| + 1) display.  Colour: the CIE 1931 2-degree table (DOI
  10.25039/CIE.DS.xvudnb9b) every 5 nm, read from the file the
  blackbody-spectrum build fetched from the CIE; the sRGB matrix.
  Nothing else is measured.
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
new_roles = ("    /* role colours: green = the computed field and curves (the lattice, the FFT),\n"
             "       orange = the reference (the closed forms, the hyperbolae, PhET's calibration),\n"
             "       magenta = the live marker (the sources, the tools, the operating point),\n"
             "       cyan = structure (the barrier's generator, the bands, the asymptotes). */")
s = s.replace(old_roles, new_roles)
assert 'Buoyancy' not in s and 'buoyancy' not in s.lower()
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(s)
shutil.copyfile(os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p1_utils.js'), os.path.join(HERE, 'p1_utils.js'))
print('p1_head.html: %d lines; p1_utils.js copied' % len(s.splitlines()))
