#!/usr/bin/env python3
"""derive.py — the Python twin of coulombs-law.html.

Re-derives every number the sim's selfTest pins:

  * k = 1/(4 pi eps0) from CODATA 2022 eps0, and e (exact since 2019), via
    scipy.constants; PhET's own k and e for the parity notes
  * PhET's two tracks: macro (charges 6.75 mm in radius, a 1-mm grid, a 1-mm
    gap, +-5 cm) and atomic (0.95 pm, a 1-pm grid, a 0.1-pm gap, +-50 pm) —
    including the floating-point rounding that gives the macro screen a
    closest centre distance of 14 mm, not 15
  * the forces at the defaults and the extremes, signs included, and PhET's
    decimal (3 places macro, 9 atomic) and scientific readouts
  * the inverse-square samples and the charge-product contours
  * electricity against gravity: k e^2 / (G m_e m_p) and friends, the forces
    at the Bohr radius, and the mass two spheres would need to pull as hard
    as the macro charges push or pull

Printed to 13 significant digits into refvals.txt; read it in full.
"""
import math
import scipy
import scipy.constants as C

P = lambda *a: print(*a)
def g13(x): return '%.13g' % x

P('scipy', scipy.__version__)
EPS0 = C.epsilon_0
K = 1 / (4 * math.pi * EPS0)
E = C.e
G = C.G
ME, MP = C.m_e, C.m_p
A0 = C.physical_constants['Bohr radius'][0]
P('eps0', g13(EPS0), '| k = 1/(4 pi eps0)', repr(K), '| e', repr(E), '| G', g13(G))
P('m_e', repr(ME), '| m_p', repr(MP), '| Bohr radius', repr(A0))
K_PHET, E_PHET = 8987551e3, 1.6021766208e-19
P('k / k_PhET - 1', g13(K / K_PHET - 1), '| e / e_PhET - 1', g13(E / E_PHET - 1))

def sym_round(y):
    return int(math.copysign(math.floor(abs(y) + 0.5), y))

TRACKS = {
    'macro': dict(q=0.001, perM=1000, iL=-50, iR=50, sep=0.001, R=0.00675),
    'atomic': dict(q=1e-12, perM=1e12, iL=-50, iR=50, sep=1e-13, R=9.5e-13),
}
for nm, T in TRACKS.items():
    s = T['R'] + T['R'] + T['sep']
    n = sym_round(s / T['q'])
    P(nm, 'r1 + r2 + sep', repr(s), 'sum/q', repr(s / T['q']), '-> n', n, '| closest centres', g13(n / T['perM']),
      'm | gap', g13(n / T['perM'] - 2 * T['R']), 'm')

def force_on(q1, q2, x1, x2, on):
    d = x1 - x2 if on == 1 else x2 - x1
    return K * q1 * q2 * d / (abs(d) * d * d)
def dec_group(x, places):
    s = '%.*f' % (places, x)
    i = s.index('.')
    out = s[:i + 4]
    j = i + 4
    while j < len(s):
        out += ' ' + s[j:j + 3]
        j += 3
    return out
def sci(x):
    man, ex = ('%.2e' % x).split('e')
    return man + (' x 10^' + str(int(ex)) if int(ex) != 0 else '')

P('\n# macro scale: q in microcoulombs, x in the 1-mm grid')
UC = 1e-6
for (q1, q2, i1, i2) in [(-4, 8, -10, 20), (10, 10, -7, 7), (1, -1, -50, 50), (5, 5, -10, 20), (-10, 10, -7, 7)]:
    x1, x2 = i1 / 1000, i2 / 1000
    F1 = force_on(q1 * UC, q2 * UC, x1, x2, 1)
    F2 = force_on(q1 * UC, q2 * UC, x1, x2, 2)
    Fm = abs(K * q1 * UC * q2 * UC) / ((i2 - i1) / 1000) ** 2
    P('macro q1 %+d uC at %d mm, q2 %+d uC at %d mm: F on q1' % (q1, i1, q2, i2), g13(F1), 'F on q2', g13(F2),
      '| |F|', g13(Fm), '| decimal3', repr(dec_group(Fm, 3)), '| sci', sci(Fm))
P('macro k q1 q2 at the defaults', g13(K * -4e-6 * 8e-6))
P('macro PhET readout at the defaults (k_PhET)', g13(abs(K_PHET * -4e-6 * 8e-6) / 0.03 ** 2))

P('\n# atomic scale: q in e, x in the 1-pm grid')
for (q1, q2, i1, i2) in [(-2, 4, -20, 20), (10, 10, -1, 1), (1, -1, -50, 50), (3, 3, -20, 20), (-10, 10, -1, 1)]:
    x1, x2 = i1 / 1e12, i2 / 1e12
    F1 = force_on(q1 * E, q2 * E, x1, x2, 1)
    F2 = force_on(q1 * E, q2 * E, x1, x2, 2)
    Fm = abs(K * q1 * E * q2 * E) / ((i2 - i1) / 1e12) ** 2
    P('atomic q1 %+d e at %d pm, q2 %+d e at %d pm: F on q1' % (q1, i1, q2, i2), g13(F1), 'F on q2', g13(F2),
      '| |F|', g13(Fm), '| decimal9', repr(dec_group(Fm, 9)), '| sci', sci(Fm))
P('atomic k q1 q2 at the defaults', g13(K * -2 * E * 4 * E))
P('atomic PhET readout at the defaults (k_PhET, e_PhET)', g13(abs(K_PHET * -2 * E_PHET * 4 * E_PHET) / 4e-11 ** 2))

P('\n# the inverse square at the defaults')
for nm, (q1, q2, r, rT, dmin, rTrack) in {'macro': (-4 * UC, 8 * UC, 0.03, 0.0135, 0.014, 0.1),
                                           'atomic': (-2 * E, 4 * E, 4e-11, 1.9e-12, 2e-12, 1e-10)}.items():
    Fr = lambda x: abs(K * q1 * q2) / x ** 2
    P(nm, 'F(dmin)', g13(Fr(dmin)), 'F(rTrack)', g13(Fr(rTrack)), 'F(2r)', g13(Fr(2 * r)), '|k q1 q2|', g13(abs(K * q1 * q2)),
      'lo', g13(0.5 * rT), 'hi', g13(2 * rTrack), 'F3r2 at dmin', g13(Fr(r) * r ** 3 / dmin))

P('\n# the charge product at the defaults: contour levels in 1-2-5 steps')
for nm, (u, r) in {'macro': (UC, 0.03), 'atomic': (E, 4e-11)}.items():
    k = K * u * u / r ** 2          # newtons per (display unit of charge)^2
    Flo, Fhi = k * 1, k * 100
    lv = []
    for e in range(math.floor(math.log10(Flo)), math.ceil(math.log10(Fhi)) + 1):
        for c in (1, 2, 5):
            F = c * 10.0 ** e
            if Flo * 1.0001 < F < Fhi * 0.9999:
                lv.append(F)
    P(nm, 'k per unit^2', g13(k), '| levels', len(lv), 'first', g13(lv[0]), 'last', g13(lv[-1]))

P('\n# electricity and gravity')
ke2 = K * E * E
P('k e^2', g13(ke2))
P('ratio e-p  k e^2/(G m_e m_p)', g13(ke2 / (G * ME * MP)))
P('ratio p-p  k e^2/(G m_p^2)', g13(ke2 / (G * MP * MP)))
P('ratio e-e  k e^2/(G m_e^2)', g13(ke2 / (G * ME * ME)))
P('Coulomb e-p at the Bohr radius', g13(ke2 / A0 ** 2), '| gravity e-p there', g13(G * ME * MP / A0 ** 2))
m_eq = math.sqrt(abs(K * -4e-6 * 8e-6) / G)
V = 4 / 3 * math.pi * 0.00675 ** 3
P('macro defaults: two equal masses pulling as hard, at any distance', g13(m_eq), 'kg | as 6.75-mm spheres, density', g13(m_eq / V))
m_eq1 = math.sqrt(K * 1e-12 / G)
P('per microcoulomb: sqrt(k/G) x 1e-6 C', g13(m_eq1), 'kg')
P('the atomic defaults at r = 40 pm: |F|', g13(abs(K * -2 * E * 4 * E) / 4e-11 ** 2))
