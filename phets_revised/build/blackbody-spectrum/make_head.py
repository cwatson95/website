#!/usr/bin/env python3
"""Build p1_head.html from the house scaffold (projects/simulations/build_buoy/p1_head.html):
the two <style> blocks and the body markup are copied VERBATIM; only the <title>, the header
comment, the site-nav hrefs (absolute, since ../website/ is dead from docs/phets_revised/),
the <h1> and the .sub tagline change.  Re-run after editing HEADER below."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p1_head.html')
s = io.open(SRC, encoding='utf-8').read()

TITLE = "Blackbody spectrum &mdash; Planck&rsquo;s law, Wien&rsquo;s peak, the Stefan&ndash;Boltzmann area and the colour of heat"
H1 = "Blackbody spectrum"
SUB = ("A remake of PhET&rsquo;s Blackbody Spectrum: slide the temperature and watch Planck&rsquo;s curve move &mdash; "
       "its peak (Wien), its area (Stefan&ndash;Boltzmann), the colour it glows, and where the classical laws fail")
HEADER = """<!--
  ===================================================================
  blackbody-spectrum.html — a remake of PhET's Blackbody Spectrum:
  the spectral power density of a blackbody against wavelength
  (Planck's law), where it peaks (Wien), how much it radiates in all
  (Stefan-Boltzmann), what colour it glows, and where the classical
  laws that came before Planck break
  ===================================================================

  Remake of PhET Interactive Simulations' Blackbody Spectrum (University
  of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET
  code or assets.  Built against PhET's blackbody-spectrum 1.0.26: its
  one screen, every control on it, and its model constants.

  Five views.  THE SPECTRUM is PhET's screen: a thermometer from 200 K to
  11000 K that snaps to 50 K, with PhET's four presets (Earth, Light
  Bulb, Sun, Sirius A); the curve of spectral power density M_lambda =
  pi B_lambda against wavelength on axes that zoom x2 in wavelength
  (0.75 to 48 um) and x5 in power (1.024e-5 to 2500 MW/m^2/um); the
  visible band; the Graph Values marker, dragged along the curve and
  sent back to the peak whenever the temperature changes, as PhET's is;
  the band labels (X-ray, ultraviolet, visible, infrared); the
  intensity, the shaded area sigma T^4; two saved curves; and the glowing
  star with PhET's B, G, R photometer.  THE STAR: the colour of the
  body two ways — PhET's photometer (three samples of the curve) against
  true CIE 1931 colorimetry (the curve integrated against the eye's
  colour-matching functions); the photometer reads the Sun as a cyan
  white and a 3000 K filament as deep orange, colorimetry reads them
  warm white and pale orange.  THE PEAK: Wien's law — the family of
  curves on log-log axes threaded by the locus of peaks (slope -5), and
  every curve collapsing onto one universal shape when scaled by its own
  peak.  THE TOTAL: the Stefan-Boltzmann law, sigma T^4 against T
  (slope 4), and where the power goes band by band.  THE LIMITS: the
  Rayleigh-Jeans law (classical, and infinite in total) and Wien's
  approximation against Planck's law, and the ratio of each to it.

  WHAT IS EXACT HERE
  ------------------
  Planck's law in SI with the exact 2019 defining constants h, c, k;
  sigma, b, c1 = 2 pi h c^2, c2 = hc/k and the frequency-peak constant
  are derived from them and equal scipy.constants (CODATA 2022) to the
  last digit.  The Wien roots x5 = 4.965114231744276 and x3 =
  2.821439372122079 by Newton (checked against Lambert W and 50-digit
  decimal Newton).  Every M_lambda pinned against 50-digit decimal
  arithmetic.  The band fractions by two series — a Bernoulli head
  series whose coefficients come from power-series division, and the
  exponential tail series — joined at x = 2 and pinned against scipy
  quad and exact rationals.  The total pinned against scipy quad and a
  composite Gauss-Legendre rule in ln lambda.  Chromaticities are sums
  over the CIE's own colour-matching table.  Twin:
  build/blackbody-spectrum/derive.py; every reference number is a line
  of build/blackbody-spectrum/refvals.txt.

  WHAT IS MODELLED / CHOSEN
  -------------------------
  The star's colour is PhET's model, reproduced exactly: each channel is
  the curve sampled at 650, 550 and 450 nm, normalised to the brightest
  of the three and dimmed by min(1, 0.02 sqrt(T/K - 798)) (PhET's
  values: 798 K is the Draper point); the halo's radius is 5 + 47.5 r px
  and its opacity 0.3 r, r = 0.02 sqrt(T/K - 798) (PhET's values).  The
  CIE colour is exact colorimetry clipped into the sRGB gamut and
  normalised to its brightest channel; its glow brightness is
  log-compressed, 1 + log10(L/L(6500 K))/12 (display only).  The
  rainbow band fades at its ends by sqrt(min(1, 4 ybar)) (display only).

  NOT MODELLED
  ------------
  Real bodies are not black: no emissivity, no absorption lines (the
  Sun's spectrum is not a Planck curve), no atmosphere.  The presets
  are PhET's round numbers, not measurements.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  h, c, k: the SI (exact).  The CIE 1931 2-degree colour-matching
  functions: the CIE's own table, CIE_xyz_1931_2deg.csv (1 nm, 360-830
  nm, DOI 10.25039/CIE.DS.xvudnb9b, ISO/CIE 11664-1:2019), every fifth
  row embedded verbatim by derive.py; the CIE's Illuminant A table
  (CIE_std_illum_A_1nm.csv) checks the chain: a Planck body at
  2855.496 K reproduces it to its printed precision (4.8e-6) and its
  chromaticity to 4e-8.  sRGB: the IEC 61966-2-1 matrix and transfer
  curve.  683 lm/W: the SI definition of the candela.  PhET's values
  (read from the minified original): the range 200-11000 K and its 50 K
  snap; the presets Earth 250 K, Light Bulb 3000 K, Sun 5800 K,
  Sirius A 9950 K; the zoom ladders; the band edges 10 nm, 380 nm,
  780 nm and 100 um; two saved curves; the photometer.  PhET's own
  constants differ from CODATA by +4.0e-5 (c1), -4.8e-6 (c2), -2.5e-7
  (sigma) and +3.6e-7 (b); this file uses CODATA throughout.
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
# the :root role-colour comment is the one accent block a sim edits
old_roles = s[s.index('    /* role colours:'):s.index('*/', s.index('    /* role colours:')) + 2]
new_roles = ("    /* role colours: green = the computed curve (Planck's law, the area under it),\n"
             "       orange = the reference (Wien's locus, the saved curves, the classical laws),\n"
             "       magenta = the live marker (the thermometer thumb, the Graph Values point),\n"
             "       cyan = structure (the axes, the band edges, the thermometer). */")
s = s.replace(old_roles, new_roles)
assert 'Buoyancy' not in s and 'buoyancy' not in s.lower().replace('buoyancy-', '')
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(s)
print('p1_head.html: %d lines' % len(s.splitlines()))
