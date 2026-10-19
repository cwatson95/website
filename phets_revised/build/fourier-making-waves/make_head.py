#!/usr/bin/env python3
"""Build p1_head.html, p1_utils.js and p4_helpers.js by EXTRACTION from the
house sims (PLAYBOOK section 4: the aesthetic is extracted, not restyled).

  scaffold : projects/simulations/build_lagr/p1_head.html, from <style> to
             'use strict'; -- the CSS, the site-nav block and the body markup.
             Edited: the :root role-colour comment, <h1>, .sub and the seven
             site-nav hrefs (absolute; the relative ../website/ links are dead
             from docs/phets_revised/).  Everything else byte-identical.
  utils    : build/wave-interference/p1_utils.js, verbatim (the shared layer
             with every Known-bad fix: throwing toRgb, plain() that strips tags
             and decodes numeric entities inside the wide match, Liang-Barsky
             polyline, range-sorting axes, guarded logTicks, recorded legends).
  helpers  : build/wave-interference/p4_helpers.js, verbatim (the world map,
             the label registry, axesR, stageLayout).
Both copies are checked against wave-interference's SHA-256 on every run, in
both directions, so neither can drift.
"""
import hashlib
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
LAGR = os.path.join(ROOT, 'projects', 'simulations', 'build_lagr')
WI = os.path.join(HERE, '..', 'wave-interference')
PINS = {'p1_utils.js': 'bff73f3eb6aa92c4485808f7b5ee4f8da0973353ecb44c137ec945ac4741ae96',
        'p4_helpers.js': '863bca754db41b8237306153edf4dba8dd4f9a97af41a96443d7d960a315c7dc'}

TAGLINE = ('A remake of PhET&rsquo;s Fourier: Making Waves &mdash; eleven harmonics you set by hand, '
           'the classic waveforms and the closed forms behind them, the ringing at a jump that never '
           'goes away, a matching game, and a wave packet beside its own spectrum')


def sha(p):
    return hashlib.sha256(io.open(p, encoding='utf-8').read().encode('utf-8')).hexdigest()


def sub1(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


src = io.open(os.path.join(LAGR, 'p1_head.html'), encoding='utf-8').read()
i = src.index('<style>')
k = src.index("<script>\n'use strict';\n") + len("<script>\n'use strict';\n")
body = src[i:k]

body = sub1(body, """    /* role colours: green = the computed orbit or curve, orange = a reference
       value, a warning or the unstable branch, magenta = the live particle or
       spacecraft, cyan = structure (the primaries, the frame, the axes). */""",
            """    /* role colours: green = the computed thing (the sum of the series, the
       partial sum, the discrete packet), orange = the reference/analytic curve
       (the waveform the series converges to, the continuous packet, the exact
       envelope) or a warning, magenta = the live marker (the selected harmonic,
       the caliper, the Gibbs peak), cyan = structure (axes, the zero line, the
       component stems).  The eleven harmonics themselves use the house NEON
       ramp, which is a scale, not a role. */""")
body = sub1(body, '<h1>Lagrange points</h1>', '<h1>Fourier: making waves</h1>')
j0 = body.index('<span class="sub" id="sub">')
j1 = body.index('</span>', j0) + len('</span>')
body = body[:j0] + '<span class="sub" id="sub">' + TAGLINE + '</span>' + body[j1:]
NAV = [('../website/index.html', 'https://cooper-watson.net/index.html'),
       ('../website/about.html', 'https://cooper-watson.net/about.html'),
       ('../website/teaching.html', 'https://cooper-watson.net/teaching.html'),
       ('../modules/teaching_modules.html', 'https://cooper-watson.net/modules/teaching_modules.html'),
       ('../website/simulations.html', 'https://cooper-watson.net/simulations.html'),
       ('../website/research.html', 'https://cooper-watson.net/research.html'),
       ('../website/cv.html', 'https://cooper-watson.net/cv.html')]
for old, new in NAV:
    body = sub1(body, 'href="%s"' % old, 'href="%s"' % new)
assert 'href="../' not in body and 'aria-current="page"' in body

top = io.open(os.path.join(HERE, 'p0_top.html'), encoding='utf-8').read()
io.open(os.path.join(HERE, 'p1_head.html'), 'w', encoding='utf-8').write(top + body)

for fn, want in PINS.items():
    theirs = os.path.join(WI, fn)
    assert sha(theirs) == want, '%s changed upstream (%s)' % (fn, sha(theirs))
    io.open(os.path.join(HERE, fn), 'w', encoding='utf-8').write(
        io.open(theirs, encoding='utf-8').read())
    assert sha(os.path.join(HERE, fn)) == want

print('p1_head.html: %d lines (scaffold %d from build_lagr); p1_utils.js and p4_helpers.js '
      'copied verbatim from build/wave-interference (SHA pinned)'
      % (len((top + body).splitlines()), len(body.splitlines())))
