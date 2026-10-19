#!/usr/bin/env python3
"""Extract, BY NAME and unchanged, the house special functions and sRGB helpers from
projects/simulations/diffraction.html into p2_ext.js: J_SPLIT, besselAsym, besselJ0, besselJ1
(power series below x = 17, Hankel asymptotic above), sinc2, airyI, SRGB_M, srgbGamma.
The colour-matching functions are NOT taken (the Wyman-Sloan-Shirley fit is wrong past 700 nm,
blackbody-spectrum Known-bad); p2_cie.js carries the CIE table instead.  Nothing retyped."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'projects', 'simulations', 'diffraction.html')
src = io.open(SRC, encoding='utf-8').read()


def block(start):
    i = src.index(start)
    first = src[i:].split('\n', 1)[0].rstrip()
    if first.endswith('{'):
        j = src.index('\n}\n', i) + 3
    elif first.startswith('const ') and '[' in first and not first.endswith(';'):
        j = src.index('];\n', i) + 3              # a multi-line array literal
    else:
        j = src.index('\n', i) + 1
    return src[i:j]


parts = [block('const J_SPLIT='), block('function besselAsym('), block('function besselJ0('),
         block('function besselJ1('), block('function sinc2('), block('function gratingFactor('),
         block('function airyI('),
         block('const SRGB_M='), block('function srgbGamma(')]
out = ('\n/* ================================================================== *\n'
       ' *  special functions and sRGB, extracted by name and unchanged from   *\n'
       ' *  projects/simulations/diffraction.html (make_ext.py): Bessel J0/J1  *\n'
       ' *  (series below 17, Hankel asymptotic above), sinc^2 and the Airy   *\n'
       ' *  pattern with their small-argument series, the sRGB matrix and     *\n'
       ' *  transfer curve.  Asserted here against scipy (refvals.txt).        *\n'
       ' * ================================================================== */\n')
out += ''.join(parts)
for nm in ['besselAsym', 'besselJ0', 'besselJ1', 'sinc2', 'gratingFactor', 'airyI', 'srgbGamma']:
    assert ('function ' + nm + '(') in out, nm
assert 'const SRGB_M=' in out and 'const J_SPLIT=' in out
io.open(os.path.join(HERE, 'p2_ext.js'), 'w', encoding='utf-8').write(out)
print('p2_ext.js: %d lines' % len(out.splitlines()))
print(out)
