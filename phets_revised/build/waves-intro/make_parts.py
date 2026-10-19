#!/usr/bin/env python3
"""Extract, BY NAME and unchanged, the blocks this sim reuses from the wave-interference build
(the same recipe as its own make_ext.py used on diffraction.html).  Nothing is retyped, and
nothing in build/wave-interference/ is touched.

  p2_parts.js  <- p2_ext.js    : SRGB_M, srgbGamma          (the house sRGB transfer)
                  p2_optics.js : cieAt, specLinear, specCss (wavelength -> sRGB, CIE 1931)
  p4_draw.js   <- p4_views.js  : the lattice drawing this sim shares with wave-interference —
                  the colour classes and the field, the sound parcels, the tape, the probes and
                  the wave meter's chart.

The rest of the drawing (the wave generator and its button, the side view, PhET's light screen,
the graph titles, the layouts and the analysis view) is this sim's own and lives in p4_views.js.
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')


def blocks(fn, names):
    src = io.open(os.path.join(WI, fn), encoding='utf-8').read()
    out = []
    for start in names:
        assert src.count(start) == 1, '%s: %r appears %d times' % (fn, start, src.count(start))
        i = src.index(start)
        first = src[i:].split('\n', 1)[0].rstrip()
        if first.endswith('{'):
            j = src.index('\n}\n', i) + 3
        elif first.startswith('const ') and '[' in first and not first.endswith(';'):
            j = src.index('];\n', i) + 3
        else:
            j = src.index('\n', i) + 1
        out.append(src[i:j])
    return ''.join(out)


P2 = ('\n/* ================================================================== *\n'
      ' *  the colour of a wavelength, extracted BY NAME and unchanged from   *\n'
      ' *  build/wave-interference/p2_ext.js (the sRGB matrix and transfer,   *\n'
      ' *  themselves extracted there from projects/simulations/diffraction   *\n'
      ' *  .html) and p2_optics.js (the CIE 1931 table -> linear sRGB,        *\n'
      ' *  desaturated into gamut).  make_parts.py; nothing retyped.          *\n'
      ' * ================================================================== */\n')
P2 += blocks('p2_ext.js', ['const SRGB_M=', 'function srgbGamma('])
P2 += blocks('p2_optics.js', ['function cieAt(', 'function specLinear(', 'function specCss('])
for nm in ['srgbGamma', 'cieAt', 'specLinear', 'specCss']:
    assert ('function ' + nm + '(') in P2, nm
assert 'const SRGB_M=' in P2
io.open(os.path.join(HERE, 'p2_parts.js'), 'w', encoding='utf-8').write(P2)

P4 = ('\n/* ================================================================== *\n'
      ' *  the lattice drawing shared with wave-interference: extracted BY    *\n'
      ' *  NAME and unchanged from build/wave-interference/p4_views.js —      *\n'
      ' *  the 49 colour classes and the field (one fill per class, runs      *\n'
      ' *  merged, pixel-snapped), the positions of PhET\'s 21 x 21 air        *\n'
      ' *  parcels, the tape measure and the probes.  make_parts.py; nothing  *\n'
      ' *  retyped.  Their dependencies (COL, U_FULL, TOOLS, lenU) are        *\n'
      ' *  defined in p3_state.js, with the same names and meanings.          *\n'
      ' * ================================================================== */\n')
# drawParcels and drawMeter are NOT taken: this sim draws its marked parcel in cyan (magenta is
# already the source, its button, the tape and the probes) and its wave meter over 2.5 periods of
# the frequency on show rather than of the medium's slowest.  Both are in p4_views.js, credited.
P4 += blocks('p4_views.js', ['const NLEV=49, HALF=24;', 'function levelOf(', 'const LEVEL_CACHE={};',
                            'function levelCols(', 'function drawField(', 'function parcelPositions(',
                            'function cellX(', 'function drawTape(', 'function drawProbes('])
for nm in ['levelOf', 'levelCols', 'drawField', 'parcelPositions', 'cellX', 'drawTape', 'drawProbes']:
    assert ('function ' + nm + '(') in P4, nm
assert 'const NLEV=49' in P4 and 'const LEVEL_CACHE={};' in P4
# the blocks must be whole: every brace balanced
for nm, txt in [('p2_parts.js', P2), ('p4_draw.js', P4)]:
    assert txt.count('{') == txt.count('}'), nm + ': unbalanced braces'
io.open(os.path.join(HERE, 'p4_draw.js'), 'w', encoding='utf-8').write(P4)
print('p2_parts.js: %d lines; p4_draw.js: %d lines' % (len(P2.splitlines()), len(P4.splitlines())))
