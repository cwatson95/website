#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive.py -- the Python twin of molecules-and-light.html.

Re-derives every model quantity the sim prints and writes reference values to
10+ digits for selfTest() to assert.  Nothing here is copied from the JS; the
JS is written against THESE numbers.  Run:

    python3 derive.py          # prints refvals.txt and writes refvals.json

Sections
  1  exact photon arithmetic from the 2019 SI defining constants
  2  PhET's model constants, read out of docs/phets/molecules-and-light_en.html
  3  the measured spectroscopy (NIST CCCBDB / WebBook), verbatim
  4  normal modes: symmetry-exact shapes, and an independent numerical
     diagonalisation of the mass-weighted Cartesian Hessian of a valence
     force field fitted to the measured fundamentals
  5  the infrared selection rule two ways (fixed point charges; the inversion
     character) and the exact zeros
  6  the seeded generator and the ensemble statistics of PhET's stochastic
     rules, with binomial / uniform tolerances
  7  the chamber kinematics and the duty cycle
  8  Planck at 288 K, the atmospheric window, the composition
"""
import io
import json
import math
import os

import numpy as np
from scipy import constants as sc
from scipy import optimize, stats

OUT = {}
LINES = []


def say(s=''):
    LINES.append(s)
    print(s)


def put(key, val, note=''):
    OUT[key] = val
    if isinstance(val, float):
        say('%-42s %.12g   %s' % (key, val, note))
    else:
        say('%-42s %s   %s' % (key, val, note))


# ===================================================================== #
# 1. exact photon arithmetic                                            #
# ===================================================================== #
# The 2019 SI fixes h, c and e exactly; hc and hc/e are therefore exact
# rational numbers and carry no uncertainty at all.
H = 6.62607015e-34          # J s, exact by definition
C = 299792458.0             # m/s, exact by definition
QE = 1.602176634e-19        # C, exact by definition
KB = 1.380649e-23           # J/K, exact by definition
HC = H * C                  # J m
HC_EV_NM = H * C / QE * 1e9  # eV nm
assert sc.h == H and sc.c == C and sc.e == QE and sc.k == KB, 'scipy CODATA disagrees'
U_KG = sc.physical_constants['atomic mass constant'][0]
C_CM = C * 100.0            # cm/s

say('=' * 72)
say('1.  exact photon arithmetic  (2019 SI defining constants)')
say('=' * 72)
put('HC_Jm', HC, 'h*c, exact')
put('HC_eV_nm', HC_EV_NM, 'h*c/e in eV nm, exact')
put('U_KG', U_KG, 'atomic mass constant, CODATA via scipy')

# PhET's five wavelengths, in metres, read from WavelengthConstants
PHET_LAMBDA = {'microwave': 0.2, 'infrared': 850e-9, 'visible': 580e-9,
               'ultraviolet': 100e-9, 'sunlight': 400e-9}


def photon(lam_m):
    """Every derived quantity of one photon, from lambda alone."""
    return dict(lam_m=lam_m,
                nu_Hz=C / lam_m,
                E_J=HC / lam_m,
                E_eV=HC / lam_m / QE,
                nubar_cm=1.0 / (lam_m * 100.0))


PH = {k: photon(v) for k, v in PHET_LAMBDA.items()}
for k in ['microwave', 'infrared', 'visible', 'ultraviolet', 'sunlight']:
    p = PH[k]
    say('  %-12s lambda %.6g m   nu %.12g Hz   E %.12g eV   nubar %.12g cm-1'
        % (k, p['lam_m'], p['nu_Hz'], p['E_eV'], p['nubar_cm']))
OUT['photons'] = PH
# The identity the file prints: E[eV] = 1239.841984332002 / lambda[nm]
for k, p in PH.items():
    assert abs(p['E_eV'] - HC_EV_NM / (p['lam_m'] * 1e9)) < 1e-15 * p['E_eV']

# ===================================================================== #
# 2. PhET's model constants                                             #
# ===================================================================== #
say()
say('=' * 72)
say("2.  PhET's constants, read out of its build 1.5.33")
say('=' * 72)
PHET = dict(
    P_ABSORB=0.5,                 # PhotonAbsorptionStrategy: probability 0.5
    HOLD_MIN=1.1, HOLD_MAX=1.3,   # 1.1 + rand*(1.3-1.1)
    HYSTERESIS=0.2,               # absorptionHysteresisCountdownTime after emit
    ABSORB_RADIUS=100.0,          # queryAbsorbPhoton: distance < 100
    PHOTON_SPEED=3000.0,          # PhotonAbsorptionModel.PHOTON_VELOCITY
    EMITTER_X=-1350.0,            # emission position
    EMIT_PERIOD=0.8,              # setPhotonEmissionPeriod(true -> 0.8)
    VIB_HZ=5.0,                   # advanceVibration(5*dt*2pi)
    ROT_HZ=1.1,                   # rotate(1.1*dt*2pi)
    SLOW_FACTOR=0.5,              # timeSpeed SLOW -> dt *= 0.5
    DT_CEILING=0.2,               # step(): dt > 0.2 is discarded
    FRAG_SPEED_A=990.0,           # NO -> 990, O2 -> 990
    FRAG_SPEED_B=0.67 * 3000.0,   # O -> 0.67 * 3000
    PASS_LIST=10,                 # passThroughPhotonList cap
)
for k in sorted(PHET):
    put('PHET.' + k, float(PHET[k]))

# PhET's atom table (Atom.js): colour, radius (model units), mass (u).
# NOTE PhET carries oxygen's mass as 12.011 -- carbon's.  That is a
# copy-paste in its source and this file reproduces it only where PhET's
# own drawing depends on it.
PHET_ATOM = {'C': dict(col='gray', r=77, m=12.011),
             'H': dict(col='white', r=37, m=1),
             'N': dict(col='blue', r=75, m=14.00674),
             'O': dict(col='rgb(255,85,0)', r=73, m=12.011)}
put('PHET.oxygen_mass', PHET_ATOM['O']['m'], "PhET's value; the real 16-O is 15.9949")

# PhET's CO2 bend: C moves +40 sin, each O moves -sB sin with
# sB = 40 * m_C / (2 m_O).  With PhET's oxygen mass that is exactly 20.
sB_phet = 40.0 * PHET_ATOM['C']['m'] / (2 * PHET_ATOM['O']['m'])
put('PHET.CO2_bend_sB', sB_phet, '= 40 m_C/(2 m_O) with PhET masses')
M_O_REAL = 15.99491461957
M_C_REAL = 12.0
M_H_REAL = 1.00782503223
M_N_REAL = 14.00307400443
sB_real = 40.0 * M_C_REAL / (2 * M_O_REAL)
put('PHET.CO2_bend_sB_realmass', sB_real, 'the same rule with real 16-O')
put('PHET.CO2_bend_ratio', 40.0 / sB_phet, "PhET's drawn |C|/|O| displacement ratio")
put('CO2_bend_ratio_true', 2 * M_O_REAL / M_C_REAL, 'the true ratio 2 m_O/m_C')

# PhET's Light Spectrum Diagram band edges, taken from its own accessibility
# descriptions (a11y.spectrumWindowLabelledSpectrum*WavelengthDescription).
# Wavelengths in metres, long end first.
PHET_BANDS = [('radio', 1e4, 5e-1), ('microwave', 1e-1, 1e-3),
              ('infrared', 1e-3, 7e-7), ('visible', 7e-7, 4e-7),
              ('ultraviolet', 4e-7, 1e-8), ('x-ray', 1e-8, 5e-11),
              ('gamma ray', 5e-11, 1e-12)]
OUT['PHET_BANDS'] = PHET_BANDS


def band_of(lam, bands=PHET_BANDS):
    for name, hi, lo in bands:
        if lo <= lam <= hi:
            return name
    return None


say()
say("  PhET's four sources placed on PhET's own band table:")
for k in ['microwave', 'infrared', 'visible', 'ultraviolet']:
    say('    %-12s %-10s -> %s' % (k, '%.4g m' % PHET_LAMBDA[k], band_of(PHET_LAMBDA[k])))
# The microwave photon at 0.2 m falls in the GAP between PhET's radio band
# (which stops at 0.5 m) and its microwave band (which starts at 0.1 m).
put('PHET.microwave_in_own_band', band_of(0.2) is None and 'NO (falls in the 0.5-0.1 m gap)' or 'yes')
put('PHET.ir_in_own_band', band_of(850e-9) or 'none')
put('PHET.uv_in_own_band', band_of(100e-9) or 'none')

# PhET's response table, read from the setPhotonAbsorptionStrategy calls.
# '' = no strategy = the photon passes through.
PHET_TABLE = {
    'CO':  {'microwave': 'rotate', 'infrared': 'vibrate', 'visible': '', 'ultraviolet': ''},
    'N2':  {'microwave': '', 'infrared': '', 'visible': '', 'ultraviolet': ''},
    'O2':  {'microwave': '', 'infrared': '', 'visible': '', 'ultraviolet': ''},
    'CO2': {'microwave': '', 'infrared': 'vibrate', 'visible': '', 'ultraviolet': ''},
    'CH4': {'microwave': '', 'infrared': 'vibrate', 'visible': '', 'ultraviolet': ''},
    'H2O': {'microwave': 'rotate', 'infrared': 'vibrate', 'visible': '', 'ultraviolet': ''},
    'NO2': {'microwave': 'rotate', 'infrared': 'vibrate', 'visible': 'glow', 'ultraviolet': 'break'},
    'O3':  {'microwave': 'rotate', 'infrared': 'vibrate', 'visible': '', 'ultraviolet': 'break'},
}
OUT['PHET_TABLE'] = PHET_TABLE
put('PHET.table_responses', sum(1 for m in PHET_TABLE for b in PHET_TABLE[m] if PHET_TABLE[m][b]),
    'non-empty cells out of 32')

# ===================================================================== #
# 3. the measured spectroscopy                                          #
# ===================================================================== #
say()
say('=' * 72)
say('3.  measured spectroscopy -- NIST, retrieved 2026-09-22')
say('=' * 72)
# Fundamental vibrational wavenumbers, cm-1, NIST CCCBDB "Experimental
# Vibrational Frequencies" (cccbdb.nist.gov/exp2x.asp), to the precision
# CCCBDB prints, with CCCBDB's own reference code.  Mode labels follow the
# spectroscopic convention (nu1 symmetric stretch, nu2 bend, nu3
# antisymmetric stretch), which for CO2 and NO2 renumbers CCCBDB's rows.
VIB = {
    'CO':  [(2143, 'sigma', 'stretch')],
    'N2':  [(2330, 'sigma-g', 'stretch')],
    'O2':  [(1556, 'sigma-g', 'stretch')],
    'NO':  [(1876, 'sigma', 'stretch')],
    'CO2': [(1333, 'sigma-g', 'symmetric stretch'), (667, 'pi-u', 'bend'),
            (2349, 'sigma-u', 'antisymmetric stretch')],
    'H2O': [(3657, 'A1', 'symmetric stretch'), (1595, 'A1', 'bend'),
            (3756, 'B2', 'antisymmetric stretch')],
    'O3':  [(1110, 'A1', 'symmetric stretch'), (705, 'A1', 'bend'),
            (1042, 'B2', 'antisymmetric stretch')],
    'NO2': [(1318, 'A1', 'symmetric stretch'), (750, 'A1', 'bend'),
            (1618, 'B2', 'antisymmetric stretch')],
    'CH4': [(2917, 'A1', 'symmetric stretch'), (1534, 'E', 'deformation'),
            (3019, 'T2', 'degenerate stretch'), (1306, 'T2', 'degenerate deformation')],
}
OUT['VIB'] = VIB
# Experimental geometry, NIST CCCBDB "Experimental Geometries"
# (cccbdb.nist.gov/expgeom2x.asp).  r in angstrom, angle in degrees.
GEOM = {
    'CO':  dict(r=1.128323, ang=None, ref='NIST WebBook, Huber & Herzberg 1979 (r_e)'),
    'N2':  dict(r=1.097685, ang=None, ref='NIST WebBook, Huber & Herzberg 1979 (r_e)'),
    'O2':  dict(r=1.20752, ang=None, ref='NIST WebBook, Huber & Herzberg 1979 (r_e)'),
    'NO':  dict(r=1.15077, ang=None, ref='NIST WebBook, Huber & Herzberg 1979 (r_e)'),
    'CO2': dict(r=1.162, ang=180.0, ref='CCCBDB, 1966Herzberg'),
    'H2O': dict(r=0.958, ang=104.4776, ref='CCCBDB, 1979Hoy/Bun:1'),
    'O3':  dict(r=1.278, ang=116.8, ref='CCCBDB, 1966Herzberg'),
    'NO2': dict(r=1.193, ang=134.1, ref='CCCBDB, 1966Herzberg'),
    'CH4': dict(r=1.087, ang=109.471, ref='CCCBDB, 1979Hir:213 / 1974sve/kov'),
}
OUT['GEOM'] = GEOM
# Experimental dipole moments, debye, CCCBDB "Experimental Dipole Moments"
DIPOLE = {'CO': 0.112, 'N2': 0.0, 'O2': 0.0, 'NO': 0.159, 'CO2': 0.0,
          'H2O': 1.857, 'O3': 0.530, 'NO2': 0.316, 'CH4': 0.0}
OUT['DIPOLE'] = DIPOLE
# Diatomic constants, NIST WebBook "Constants of Diatomic Molecules"
# NOTE the bracket convention.  Huber & Herzberg put SQUARE BRACKETS round a
# rotational constant that belongs to the stated vibrational level rather than
# to the equilibrium geometry, and the WebBook reproduces them: O2's row reads
# Be = [1.4376766], which is B_0, not B_e.  Taking it as B_e disagrees with
# the same row's r_e by 0.55 %, which is what caught it -- and B_e computed
# from r_e minus alpha_e/2 reproduces the bracketed number to 6 digits, which
# is what settled it.  'bracketed' marks the rows where that applies.
DIATOMIC = {
    'CO': dict(we=2169.81358, wexe=13.28831, Be=1.93128087, ae=0.01750441, re=1.128323,
               bracketed=False),
    'N2': dict(we=2358.57, wexe=14.324, Be=1.998241, ae=0.017318, re=1.097685,
               bracketed=False),
    'O2': dict(we=1580.193, wexe=11.981, Be=1.4376766, ae=0.01593, re=1.20752,
               bracketed=True),
}
OUT['DIATOMIC'] = DIATOMIC
MASS = {'H': M_H_REAL, 'C': M_C_REAL, 'N': M_N_REAL, 'O': M_O_REAL}
OUT['MASS'] = MASS

say('  fundamental wavenumbers (cm-1) and the wavelengths they sit at:')
for m in ['CO', 'N2', 'O2', 'CO2', 'H2O', 'CH4', 'NO2', 'O3']:
    parts = ['%d cm-1 = %.4g um (%s)' % (v, 1e4 / v, s) for v, s, _ in VIB[m]]
    say('    %-4s %s' % (m, '; '.join(parts)))

# The diatomic fundamental from the Dunham constants: nu = we - 2 wexe.
for m, d in DIATOMIC.items():
    fund = d['we'] - 2 * d['wexe']
    put('fundamental_from_Dunham.' + m, fund,
        'we - 2 wexe; CCCBDB prints %d' % VIB[m][0][0])
    assert abs(fund - VIB[m][0][0]) < 4.0

# B_e from r_e and the reduced mass -- an independent route to a tabulated
# number, which validates the mass table and the unit chain in one check.
HBAR = H / (2 * math.pi)


def Be_from_geometry(m1, m2, re_ang):
    mu = m1 * m2 / (m1 + m2) * U_KG
    I = mu * (re_ang * 1e-10) ** 2
    return H / (8 * math.pi ** 2 * C_CM * I)     # cm-1


for m, (a1, a2) in [('CO', ('C', 'O')), ('N2', ('N', 'N')), ('O2', ('O', 'O'))]:
    d = DIATOMIC[m]
    b = Be_from_geometry(MASS[a1], MASS[a2], d['re'])
    d['Be_true'] = b
    d['B0'] = b - d['ae'] / 2
    as_Be = abs(b - d['Be']) / d['Be']
    as_B0 = abs(d['B0'] - d['Be']) / d['Be']
    put('Be_from_geometry.' + m, b, 'printed %.7f%s' % (d['Be'], ' [B_0]' if d['bracketed'] else ''))
    put('Be_rel_if_read_as_Be.' + m, as_Be)
    put('Be_rel_if_read_as_B0.' + m, as_B0)
    if d['bracketed']:
        # The discriminating statement is the RATIO, not an absolute bound:
        # r_e is printed to 6 figures here, so 4e-6 of the residual is the
        # table's own rounding, and the rest is the next Dunham term.
        assert as_B0 < 3e-5 and as_Be > 100 * as_B0, (m, as_Be, as_B0)
    else:
        assert as_Be < 1e-6 and as_B0 > 100 * as_Be, (m, as_Be, as_B0)
    put('bracket_reading_better_by.' + m, (as_Be / as_B0) if d['bracketed'] else (as_B0 / as_Be),
        'the factor that decides which column it is')

# The CO J = 1 <- 0 pure rotational line: 2 B_0 with B_0 = B_e - alpha_e/2.
B0_CO = DIATOMIC['CO']['Be'] - DIATOMIC['CO']['ae'] / 2
put('CO_B0_cm', B0_CO, 'B_e - alpha_e/2')
put('CO_J10_cm', 2 * B0_CO)
put('CO_J10_GHz', 2 * B0_CO * C_CM / 1e9, 'the 115.271 GHz line astronomers use')
put('CO_J10_mm', 1e4 / (2 * B0_CO) / 1e3, 'mm')
# the observed rest frequency, quoted (CO(1-0), 115.2712018 GHz)
put('CO_J10_GHz_observed', 115.2712018, 'QUOTED (radio-astronomy rest frequency)')
put('CO_J10_rel_err', abs(2 * B0_CO * C_CM / 1e9 - 115.2712018) / 115.2712018,
    'the residual is the centrifugal distortion -4 D_0, not an error')

# Bond dissociation energies at 0 K, eV.  QUOTED (Active Thermochemical
# Tables / NIST-JANAF values); NOT re-derived here.
D0_EV = {'O2': 5.1156, 'O3': 1.0520, 'NO2': 3.1163, 'N2': 9.7538,
         'CO': 11.1088, 'H2O': 5.1102, 'CH4': 4.4800, 'CO2': 5.4533}
D0_NOTE = {'O2': 'O + O', 'O3': 'O2 + O', 'NO2': 'NO + O', 'N2': 'N + N',
           'CO': 'C + O', 'H2O': 'H + OH', 'CH4': 'CH3 + H', 'CO2': 'CO + O'}
OUT['D0_EV'] = D0_EV
OUT['D0_NOTE'] = D0_NOTE
say()
say('  photodissociation thresholds lambda = hc/D0  (D0 QUOTED, ATcT):')
THRESH = {}
for m, d in sorted(D0_EV.items()):
    lam_nm = HC_EV_NM / d
    THRESH[m] = lam_nm
    say('    %-4s D0 = %7.4f eV (%-8s)  ->  %8.2f nm' % (m, d, D0_NOTE[m], lam_nm))
OUT['THRESH_NM'] = THRESH
put('thresh_NO2_nm', THRESH['NO2'], 'NO2 + hv -> NO + O')
put('thresh_O3_nm', THRESH['O3'], 'O3 + hv -> O2 + O, ground-state channel')
put('thresh_O2_nm', THRESH['O2'])
# PhET's UV photon is more energetic than EVERY one of these thresholds.
put('phet_uv_eV', PH['ultraviolet']['E_eV'])
put('phet_uv_above_all_D0', bool(all(PH['ultraviolet']['E_eV'] > d for d in D0_EV.values())))
put('phet_uv_over_CO', PH['ultraviolet']['E_eV'] / D0_EV['CO'], 'x the strongest bond here')
put('phet_ir_eV', PH['infrared']['E_eV'])
put('CO2_bend_eV', 667 * 100 * HC / QE, 'the 15 um band, in eV')
put('phet_ir_over_CO2bend', PH['infrared']['E_eV'] / (667 * 100 * HC / QE),
    "PhET's IR photon over the CO2 bend quantum")
put('phet_micro_eV', PH['microwave']['E_eV'])
put('phet_micro_over_CO_J10', PH['microwave']['E_eV'] / (2 * B0_CO * 100 * HC / QE),
    "PhET's microwave photon over CO's J=1<-0 quantum")

# ===================================================================== #
# 4. normal modes                                                       #
# ===================================================================== #
say()
say('=' * 72)
say('4.  normal modes')
say('=' * 72)
# Units: length angstrom, mass u, energy aJ = 1e-18 J.  Force constants then
# come out in aJ/A^2 = mdyn/A = 100 N/m.
CONV = 1e-18 / (1e-20 * U_KG)          # (aJ / (A^2 u))  ->  s^-2
put('CONV_s2', CONV, 'aJ/(A^2 u) -> s^-2')


def wavenumber(lam_eig):
    """eigenvalue of the mass-weighted Hessian (aJ/(A^2 u)) -> cm-1"""
    if lam_eig <= 0:
        return -math.sqrt(-lam_eig * CONV) / (2 * math.pi * C_CM)
    return math.sqrt(lam_eig * CONV) / (2 * math.pi * C_CM)


def geom_xy(name):
    """Equilibrium Cartesians (angstrom) in the molecular plane, centre of
    mass at the origin.  Returns (symbols, positions Nx3)."""
    g = GEOM[name]
    r, ang = g['r'], g['ang']
    if name in ('CO', 'N2', 'O2', 'NO'):
        s = {'CO': ['C', 'O'], 'N2': ['N', 'N'], 'O2': ['O', 'O'], 'NO': ['N', 'O']}[name]
        p = np.array([[-r / 2, 0, 0], [r / 2, 0, 0]], float)
    elif name == 'CO2':
        s = ['O', 'C', 'O']
        p = np.array([[-r, 0, 0], [0, 0, 0], [r, 0, 0]], float)
    elif name == 'CH4':
        s = ['C', 'H', 'H', 'H', 'H']
        d = r / math.sqrt(3.0)
        p = np.array([[0, 0, 0], [d, d, d], [d, -d, -d], [-d, d, -d], [-d, -d, d]], float)
    else:                                   # bent XY2: H2O, O3, NO2
        cen = {'H2O': 'O', 'O3': 'O', 'NO2': 'N'}[name]
        out = {'H2O': 'H', 'O3': 'O', 'NO2': 'O'}[name]
        s = [out, cen, out]
        half = math.radians(ang) / 2
        p = np.array([[-r * math.sin(half), -r * math.cos(half), 0],
                      [0, 0, 0],
                      [r * math.sin(half), -r * math.cos(half), 0]], float)
    m = np.array([MASS[a] for a in s])
    p = p - (m[:, None] * p).sum(0) / m.sum()
    return s, p


def bonds_of(name):
    return {'CO': [(0, 1)], 'N2': [(0, 1)], 'O2': [(0, 1)], 'NO': [(0, 1)],
            'CO2': [(1, 0), (1, 2)], 'H2O': [(1, 0), (1, 2)],
            'O3': [(1, 0), (1, 2)], 'NO2': [(1, 0), (1, 2)],
            'CH4': [(0, 1), (0, 2), (0, 3), (0, 4)]}[name]


def angles_of(name):
    """(i, j, k) triples with j the vertex."""
    if name in ('CO2', 'H2O', 'O3', 'NO2'):
        return [(0, 1, 2)]
    if name == 'CH4':
        return [(i, 0, j) for i in range(1, 5) for j in range(i + 1, 5)]
    return []


def potential(name, X, f):
    """Valence force field, energy in aJ.  The constants, in order, are
        f_r    bond stretch
        f_rr   stretch-stretch interaction
        f_th   bend (in the coordinate r_e * delta theta)
        f_rth  stretch-bend interaction (bent triatomics)
        f_thth bend-bend interaction, angles sharing a bond (CH4)
        f_thth2 bend-bend interaction, opposite angle pairs (CH4)
    """
    g = GEOM[name]
    re = g['r']
    f_r, f_rr, f_th, f_rth, f_thth, f_thth2 = (list(f) + [0.0] * 6)[:6]
    dr = np.array([np.linalg.norm(X[j] - X[i]) - re for (i, j) in bonds_of(name)])
    V = 0.5 * f_r * float(dr @ dr)
    nb = len(dr)
    for a in range(nb):
        for b in range(a + 1, nb):
            V += f_rr * dr[a] * dr[b]
    ang = angles_of(name)
    if not ang:
        return V
    linear = abs(g['ang'] - 180.0) < 1e-9
    da = []
    for (i, j, k) in ang:
        u = X[i] - X[j]
        w = X[k] - X[j]
        cth = float(u @ w) / (np.linalg.norm(u) * np.linalg.norm(w))
        cth = min(1.0, max(-1.0, cth))
        if linear:
            # A linear molecule's bend: (pi - theta)^2 = 2(1 + cos theta) to
            # leading order, and 1 + cos theta is smooth in the Cartesians
            # where arccos is not.  This IS the harmonic bend coordinate.
            V += 0.5 * f_th * re * re * 2.0 * (1.0 + cth)
        else:
            da.append(math.acos(cth) - math.radians(g['ang']))
    if linear:
        return V
    da = np.array(da)
    V += 0.5 * f_th * re * re * float(da @ da)
    if len(da) == 1:
        # bent XY2: the two bonds are equivalent, so one stretch-bend constant
        V += f_rth * re * (dr[0] + dr[1]) * da[0]
        return V
    # CH4: angle pairs either share a bond or do not
    bl = bonds_of(name)
    for a in range(len(ang)):
        for b in range(a + 1, len(ang)):
            sa, sb = {ang[a][0], ang[a][2]}, {ang[b][0], ang[b][2]}
            V += (f_thth if sa & sb else f_thth2) * re * re * da[a] * da[b]
    for a in range(len(ang)):
        for (i, j) in bl:
            if j in (ang[a][0], ang[a][2]):
                V += f_rth * re * dr[bl.index((i, j))] * da[a]
    return V


def hessian(name, f, h=2e-4):
    s, X0 = geom_xy(name)
    n = len(s) * 3
    Hm = np.zeros((n, n))
    flat = X0.reshape(-1).copy()

    def V(v):
        return potential(name, v.reshape(-1, 3), f)

    for a in range(n):
        for b in range(a, n):
            vpp = flat.copy(); vpp[a] += h; vpp[b] += h
            vpm = flat.copy(); vpm[a] += h; vpm[b] -= h
            vmp = flat.copy(); vmp[a] -= h; vmp[b] += h
            vmm = flat.copy(); vmm[a] -= h; vmm[b] -= h
            Hm[a, b] = Hm[b, a] = (V(vpp) - V(vpm) - V(vmp) + V(vmm)) / (4 * h * h)
    return s, X0, Hm


def eckart_basis(s, X0):
    """The six (or five) mass-weighted vectors that span the rigid motions:
    three translations and three rotations about the centre of mass, each
    written in the mass-weighted coordinates the Hessian is diagonalised in.
    Returned orthonormal; a linear molecule drops one automatically because
    its rotation about the axis is the zero vector."""
    m = np.array([MASS[a] for a in s])
    sq = np.sqrt(m)
    cols = []
    for al in range(3):
        v = np.zeros((len(s), 3))
        v[:, al] = sq
        cols.append(v.reshape(-1))
    for al in range(3):
        e = np.zeros(3)
        e[al] = 1.0
        v = np.cross(np.tile(e, (len(s), 1)), X0) * sq[:, None]
        cols.append(v.reshape(-1))
    B = []
    for v in cols:
        for u in B:
            v = v - u * float(u @ v)
        n = float(np.linalg.norm(v))
        if n > 1e-8:
            B.append(v / n)
    return np.array(B)


def modes(name, f):
    """Mass-weighted diagonalisation.  Returns (wavenumbers cm-1, Cartesian
    displacement vectors Nx3, sorted descending in frequency, with the
    translations and rotations dropped)."""
    s, X0, Hm = hessian(name, f)
    m = np.array([MASS[a] for a in s])
    w = np.repeat(1.0 / np.sqrt(m), 3)
    Hw = Hm * np.outer(w, w)
    Hw = 0.5 * (Hw + Hw.T)
    # Eckart projection.  A finite-difference Hessian is only translationally
    # and rotationally invariant to O(h^2), and the residual leaks into the
    # eigenvectors as a spurious drift and spin (2e-8 in water before this was
    # put in).  Projecting the rigid motions out of H makes them exact null
    # vectors, so every remaining eigenvector is orthogonal to them and every
    # mode conserves linear and angular momentum to machine precision.
    B = eckart_basis(s, X0)
    P = np.eye(len(Hw)) - B.T @ B
    Hw = P @ Hw @ P
    Hw = 0.5 * (Hw + Hw.T)
    lam, vec = np.linalg.eigh(Hw)
    nat = len(s)
    nvib = 3 * nat - len(B)
    order = np.argsort(lam)[::-1][:nvib]
    out_nu, out_d = [], []
    for k in order:
        out_nu.append(wavenumber(lam[k]))
        d = (vec[:, k] * w).reshape(-1, 3)      # back to Cartesian displacement
        d = d / np.abs(d).max()
        out_d.append(d)
    return np.array(out_nu), np.array(out_d), s, X0


def distinct(nu, tol=0.5):
    """Collapse a degenerate set to its distinct frequencies, with the
    multiplicity of each -- the multiplicities ARE the symmetry species."""
    out = []
    for v in sorted(nu, reverse=True):
        if out and abs(out[-1][0] - v) < tol:
            out[-1][1] += 1
        else:
            out.append([float(v), 1])
    return out


def fit_field(name, target, x0, free, pen_idx=(), pen_w=5e-5):
    """Least-squares the valence constants onto the measured fundamentals.
    `free` names which slots of the six-constant field are varied.  Where the
    frequencies alone do not determine the field (a bent triatomic has three
    measured numbers and four symmetry constants), `pen_idx` carries a small
    penalty, so the solution returned is the one of SMALLEST stretch-bend
    interaction that still reproduces all three measurements -- a stated
    choice, not an accident of the optimiser's starting point."""
    tgt = np.array(sorted(target, reverse=True), float)

    def expand(p):
        f = [0.0] * 6
        for k, i in enumerate(free):
            f[i] = p[k]
        return f

    def resid(p):
        nu, _, _, _ = modes(name, expand(p))
        got = np.array([v for v, _ in distinct(nu)])
        n = min(len(got), len(tgt))
        r = (got[:n] - tgt[:n]) / tgt[:n]
        if len(got) < len(tgt):
            r = np.concatenate([r, np.ones(len(tgt) - len(got))])
        extra = np.array([pen_w * p[free.index(i)] for i in pen_idx])
        return np.concatenate([r, extra]) if len(extra) else r
    sol = optimize.least_squares(resid, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
    return expand(sol.x), sol, len(tgt)


FIELDS, MODES = {}, {}
say()
# slots: 0 f_r, 1 f_rr, 2 f_th, 3 f_rth, 4 f_thth, 5 f_thth2
FITJOBS = [
    # linear XY2: three constants, three frequencies, exactly determined
    ('CO2', [1333, 667, 2349], [15.0, 1.0, 0.6], (0, 1, 2), ()),
    # bent XY2: four symmetry constants, three frequencies -- f_rth is the
    # free one and is driven to the smallest magnitude that still fits
    ('H2O', [3657, 1595, 3756], [8.0, -0.1, 0.7, 0.0], (0, 1, 2, 3), (3,)),
    ('O3', [1110, 705, 1042], [5.0, 0.7, 1.6, 0.0], (0, 1, 2, 3), (3,)),
    ('NO2', [1318, 750, 1618], [10.0, 2.0, 1.2, 0.0], (0, 1, 2, 3), (3,)),
    # tetrahedral XY4: five constants, four frequencies
    ('CH4', [2917, 1534, 3019, 1306], [5.0, 0.05, 0.5, 0.0, -0.01, 0.0],
     (0, 1, 2, 3, 4, 5), (3,)),
]
FNAMES = ['f_r', 'f_rr', 'f_th', 'f_rth', 'f_thth', 'f_thth2']
for name, ntarget, x0, free, pen in FITJOBS:
    f, sol, ntgt = fit_field(name, ntarget, x0, free, pen)
    nu, d, s, X0 = modes(name, f)
    FIELDS[name] = f
    MODES[name] = dict(nu=nu.tolist(), d=d.tolist(), sym=s, X0=X0.tolist(),
                       distinct=distinct(nu))
    worst = float(np.max(np.abs(sol.fun[:ntgt])))
    say('  %-4s fitted [%s] aJ/A^2'
        % (name, ', '.join('%s %.5f' % (FNAMES[i], f[i]) for i in free)))
    say('       computed %s  vs measured %s  (worst rel %.2e)'
        % ([round(v, 1) for v, _ in distinct(nu)], sorted(ntarget, reverse=True), worst))
    put('fit_worst_rel.' + name, worst)
    assert worst < 2e-7, (name, sol.fun)   # 2e-7 of 1000 cm-1 is 2e-4 cm-1
OUT['FIELDS'] = FIELDS
# the multiplicities recover the symmetry species without any group theory
put('CH4_multiplicities', [m for _, m in MODES['CH4']['distinct']],
    'T2(3), A1(1), E(2), T2(3) in descending frequency')
assert [m for _, m in MODES['CH4']['distinct']] == [3, 1, 2, 3]
put('CO2_multiplicities', [m for _, m in MODES['CO2']['distinct']],
    'sigma-u(1), sigma-g(1), pi-u(2)')
assert [m for _, m in MODES['CO2']['distinct']] == [1, 1, 2]

# ---- the symmetry-exact mode shapes, derived independently ---------- #
say()
say('  the shapes symmetry alone fixes, against the numerical eigenvectors:')

# (a) diatomic: (1, -m1/m2) from zero linear momentum, exactly.
for name in ['CO', 'N2', 'O2', 'NO']:
    s, X0 = geom_xy(name)
    m1, m2 = MASS[s[0]], MASS[s[1]]
    exact = np.array([1.0, -m1 / m2])
    exact = exact / np.abs(exact).max()
    put('diatomic_ratio.' + name, float(-m1 / m2), 'd2/d1 = -m1/m2')
    # the force constant from the measured fundamental
    mu = m1 * m2 / (m1 + m2)
    nub = VIB[name][0][0]
    k = (2 * math.pi * C_CM * nub) ** 2 * mu * U_KG      # N/m
    put('k_Nm.' + name, k, 'from nu = (1/2pi c) sqrt(k/mu)')

# (b) linear symmetric XY2 (CO2): (1, 0, -1) and (1, -2 m_Y/m_X, 1), exact.
# The bend is a degenerate pair, and eigh returns an arbitrary rotation of it
# in the y-z plane; rotate it so one member lies wholly in the drawing plane.
# (A degenerate pair has no preferred basis -- CHOOSING one is legitimate, and
# the pair's own invariants, the two wavenumbers, are untouched by it.)
def deplane(name):
    d = np.array(MODES[name]['d'])
    nu = MODES[name]['nu']
    for i in range(len(d) - 1):
        if abs(nu[i] - nu[i + 1]) > 0.5:
            continue
        a, b = d[i], d[i + 1]
        za, zb = a[:, 2], b[:, 2]
        k = int(np.argmax(np.abs(za) + np.abs(zb)))
        new = zb[k] * a - za[k] * b
        oth = za[k] * a + zb[k] * b
        if np.abs(new).max() < 1e-12 or np.abs(oth).max() < 1e-12:
            continue
        d[i] = new / np.abs(new).max()
        d[i + 1] = oth / np.abs(oth).max()
    MODES[name]['d'] = d.tolist()
    return d


deplane('CO2')
ratio_lin = 2 * MASS['O'] / MASS['C']
put('CO2_asym_ratio', -ratio_lin, 'central-atom displacement / outer, EXACT')
nu_c, d_c = MODES['CO2']['nu'], np.array(MODES['CO2']['d'])
for i, d in enumerate(d_c):
    say('    CO2 mode %d  %.1f cm-1   d = %s' % (i, nu_c[i], np.round(d, 4).tolist()))


def pick_mode(name, pred):
    for i, d in enumerate(np.array(MODES[name]['d'])):
        if pred(d):
            return i, d
    raise AssertionError('no mode matched for ' + name)


axial = lambda d: np.abs(d[:, 1:]).max() < 1e-7
i_sym, d_sym = pick_mode('CO2', lambda d: axial(d) and abs(d[1][0]) < 1e-8)
i_asy, d_asy = pick_mode('CO2', lambda d: axial(d) and abs(d[1][0]) > 0.1)
i_bnd, d_bnd = pick_mode('CO2', lambda d: abs(d[0][1]) > 0.1 and abs(d[0][2]) < 1e-7)
MODES['CO2']['idx'] = dict(nu1=i_sym, nu2=i_bnd, nu3=i_asy)
put('CO2_nu1_computed', float(nu_c[i_sym]), 'symmetric stretch, C at rest')
put('CO2_nu2_computed', float(nu_c[i_bnd]), 'bend')
put('CO2_nu3_computed', float(nu_c[i_asy]), 'antisymmetric stretch')
put('CO2_nu1_C_rest', float(abs(d_sym[1]).max()), 'the central atom really does not move')
assert abs(d_sym[1]).max() < 1e-8
put('CO2_nu1_shape_err', float(abs(abs(d_sym[0][0]) - abs(d_sym[2][0]))), 'the two O move equally')
r_asy = d_asy[1][0] / d_asy[0][0]
r_bnd = d_bnd[1][1] / d_bnd[0][1]
put('CO2_nu3_ratio_numeric', float(r_asy), 'vs exact %.12g' % (-ratio_lin))
put('CO2_nu2_ratio_numeric', float(r_bnd), 'vs exact %.12g' % (-ratio_lin))
assert abs(r_asy + ratio_lin) < 1e-7 and abs(r_bnd + ratio_lin) < 1e-7

# (c) bent XY2: the B2 antisymmetric stretch's shape is fixed by the bond
#     angle and the masses alone.  With the C2 axis along y and the outer
#     atoms at (+-s, y_Y), zero linear and zero angular momentum give
#         v1 = u1 cot(theta/2),   u_X = -2 m_Y u1 / m_X,   v_X = 0.
BENT_B2 = {}
for name in ['H2O', 'O3', 'NO2']:
    s, X0 = geom_xy(name)
    mY, mX = MASS[s[0]], MASS[s[1]]
    half = math.radians(GEOM[name]['ang']) / 2
    cot = 1.0 / math.tan(half)
    # the exact eigenvector, before normalisation:  atom0 (-u,+v? ) --
    # take u1 = 1 for the LEFT atom; then u2 = u1, v2 = -v1.
    ex = np.array([[1.0, cot, 0.0], [-2 * mY / mX, 0.0, 0.0], [1.0, -cot, 0.0]])
    ex = ex / np.abs(ex).max()
    BENT_B2[name] = ex.tolist()
    # find it numerically: the B2 mode is the one whose central atom moves
    # only in x (the C2 axis is y)
    got = None
    for i, d in enumerate(np.array(MODES[name]['d'])):
        if abs(d[1][1]) < 1e-7 and abs(d[1][0]) > 1e-3:
            got = (i, d)
    assert got is not None, name
    i_b2, d_b2 = got
    d_b2 = d_b2 * np.sign(d_b2[0][0])
    err = float(np.abs(d_b2 / np.abs(d_b2).max() - ex).max())
    put('B2_exact_vs_numeric.' + name, err, 'nu3 = %.1f cm-1, cot(theta/2) = %.9f'
        % (MODES[name]['nu'][i_b2], cot))
    assert err < 1e-6, (name, err)
    MODES[name]['i_b2'] = i_b2
OUT['BENT_B2'] = BENT_B2
OUT['MODES'] = {k: dict(nu=v['nu'], d=np.array(v['d']).tolist(), sym=v['sym'],
                        X0=v['X0'], i_b2=v.get('i_b2', -1)) for k, v in MODES.items()}

# every mode must conserve linear momentum and, in the plane, angular momentum
say()
for name in MODES:
    s, X0 = geom_xy(name)
    m = np.array([MASS[a] for a in s])
    worstP, worstL = 0.0, 0.0
    for d in np.array(MODES[name]['d']):
        worstP = max(worstP, float(np.abs((m[:, None] * d).sum(0)).max()))
        L = float(np.abs(np.cross(X0, m[:, None] * d).sum(0)).max())
        worstL = max(worstL, L)
    put('mode_momentum.' + name, worstP, 'sum m_i d_i')
    put('mode_angmom.' + name, worstL, 'sum m_i r_i x d_i')
    assert worstP < 1e-9 and worstL < 1e-7, (name, worstP, worstL)

# ===================================================================== #
# 5. the infrared selection rule                                        #
# ===================================================================== #
say()
say('=' * 72)
say('5.  the infrared selection rule, two ways')
say('=' * 72)
# (a) fixed point charges.  q on the outer atoms, -(sum) on the centre;
#     the magnitude is arbitrary because a zero must not depend on it.
CHARGE = {'CO': [0.5, -0.5], 'NO': [0.5, -0.5], 'N2': [0.0, 0.0], 'O2': [0.0, 0.0],
          'CO2': [-0.5, 1.0, -0.5], 'H2O': [0.4, -0.8, 0.4],
          'O3': [-0.25, 0.5, -0.25], 'NO2': [-0.4, 0.8, -0.4],
          'CH4': [-0.4, 0.1, 0.1, 0.1, 0.1]}
OUT['CHARGE'] = CHARGE


def dmu_dQ(name, d, q=None):
    """|d mu / dQ| for a rigid-charge model: sum_i q_i d_i."""
    qq = np.array(q if q is not None else CHARGE[name], float)
    return float(np.linalg.norm((qq[:, None] * d).sum(0)))


IRACT = {}
for name in ['CO', 'N2', 'O2', 'NO', 'CO2', 'H2O', 'O3', 'NO2', 'CH4']:
    if name in MODES:
        ds, nus = np.array(MODES[name]['d']), MODES[name]['nu']
    else:
        s, X0 = geom_xy(name)
        m1, m2 = MASS[s[0]], MASS[s[1]]
        v = np.array([[1.0, 0, 0], [-m1 / m2, 0, 0]])
        ds, nus = np.array([v / np.abs(v).max()]), [float(VIB[name][0][0])]
    rows = []
    for i, d in enumerate(ds):
        a = dmu_dQ(name, d)
        b = dmu_dQ(name, d, [2.7 * x for x in CHARGE[name]])   # a different q
        rows.append(dict(nu=float(nus[i]), dmu=a, dmu_scaled=b, active=bool(a > 1e-9)))
    IRACT[name] = rows
    say('  %-4s ' % name + '  '.join('%.0f cm-1 %s (|dmu/dQ| %.3e)'
                                     % (r['nu'], 'IR-ACTIVE' if r['active'] else 'inactive', r['dmu'])
                                     for r in rows))
OUT['IRACT'] = IRACT
# the zeros must be EXACT and independent of the charge magnitude
zeros = [(n, r) for n in IRACT for r in IRACT[n] if not r['active']]
put('n_inactive_modes', len(zeros))
put('worst_inactive_dmu', max(r['dmu'] for _, r in zeros))
put('worst_inactive_dmu_scaled', max(r['dmu_scaled'] for _, r in zeros))
assert max(r['dmu'] for _, r in zeros) < 1e-12
put('n_active_modes', sum(1 for n in IRACT for r in IRACT[n] if r['active']))
put('weakest_active_dmu', min(r['dmu'] for n in IRACT for r in IRACT[n] if r['active']))

# (b) the inversion character, for the centrosymmetric molecules.  A mode
#     that maps to +itself under i cannot change a dipole, because i sends
#     every component of mu to -mu.  This is the real selection rule and it
#     is a completely independent computation from (a).
say()
INV = {'N2': [1, 0], 'O2': [1, 0], 'CO2': [2, 1, 0]}   # atom permutation under i


def inversion_character(name, d):
    perm = INV[name]
    dp = np.zeros_like(d)
    for i in range(len(d)):
        dp[perm[i]] = -d[i]
    if np.abs(dp - d).max() < 1e-7:
        return +1
    if np.abs(dp + d).max() < 1e-7:
        return -1
    return 0


for name in ['N2', 'O2', 'CO2']:
    if name in MODES:
        ds, nus = np.array(MODES[name]['d']), MODES[name]['nu']
    else:
        s, X0 = geom_xy(name)
        v = np.array([[1.0, 0, 0], [-1.0, 0, 0]])
        ds, nus = np.array([v]), [float(VIB[name][0][0])]
    for i, d in enumerate(ds):
        chi = inversion_character(name, d)
        act = IRACT[name][i]['active']
        say('    %-4s %6.0f cm-1   chi(i) = %+d (%s)   point-charge says %s'
            % (name, nus[i], chi, 'gerade' if chi > 0 else ('ungerade' if chi < 0 else 'mixed'),
               'ACTIVE' if act else 'inactive'))
        if chi != 0:
            assert (chi < 0) == act, (name, i, chi, act)
put('inversion_agrees_with_charges', True, 'every centrosymmetric mode, both ways')

# how many of PhET's eight molecules have an IR-active fundamental at all
ir_any = {n: any(r['active'] for r in IRACT[n]) for n in
          ['CO', 'N2', 'O2', 'CO2', 'CH4', 'H2O', 'NO2', 'O3']}
put('n_IR_active_molecules', sum(ir_any.values()), 'of 8; the two that are not: '
    + ', '.join(n for n in ir_any if not ir_any[n]))
# a permanent dipole is what allows a pure rotational (microwave) spectrum
rot_any = {n: DIPOLE[n] > 0 for n in ['CO', 'N2', 'O2', 'CO2', 'CH4', 'H2O', 'NO2', 'O3']}
put('n_microwave_active', sum(rot_any.values()), 'molecules with mu != 0: '
    + ', '.join(n for n in rot_any if rot_any[n]))
# PhET gives a microwave response to exactly the molecules with mu != 0
phet_rot = {n: PHET_TABLE[n]['microwave'] == 'rotate' for n in rot_any}
put('phet_microwave_matches_dipole', phet_rot == rot_any,
    "PhET's microwave column IS the permanent-dipole column")
# PhET's infrared column against real IR activity
phet_ir = {n: PHET_TABLE[n]['infrared'] == 'vibrate' for n in ir_any}
put('phet_infrared_matches_activity', phet_ir == ir_any,
    "PhET's infrared column IS the IR-active column")
OUT['IR_ANY'] = ir_any
OUT['ROT_ANY'] = rot_any

# ===================================================================== #
# 6. the seeded generator and PhET's stochastic rules                   #
# ===================================================================== #
say()
say('=' * 72)
say("6.  the seeded generator and PhET's stochastic rules")
say('=' * 72)
M32 = 0xFFFFFFFF


class Mulberry32(object):
    """Bit-for-bit the generator the JS carries (32-bit ops throughout, so
    Math.imul and >>> map exactly onto masked Python arithmetic)."""

    def __init__(self, seed):
        self.a = seed & M32

    def next(self):
        self.a = (self.a + 0x6D2B79F5) & M32
        a = self.a
        t = ((a ^ (a >> 15)) * (1 | a)) & M32
        t = (t ^ ((t + (((t ^ (t >> 7)) * (61 | t)) & M32)) & M32)) & M32
        return ((t ^ (t >> 14)) & M32) / 4294967296.0


R = Mulberry32(20260922)
first = [R.next() for _ in range(6)]
put('mulberry_seed', 20260922)
for i, v in enumerate(first):
    put('mulberry_first[%d]' % i, v)
OUT['mulberry_first'] = first

N_STAT = 20000
R = Mulberry32(20260922)
u = np.array([R.next() for _ in range(N_STAT)])
put('mulberry_mean', float(u.mean()), 'exactly reproducible in the JS')
put('mulberry_var', float(u.var(ddof=0)))
put('mulberry_min', float(u.min()))
put('mulberry_max', float(u.max()))
OUT['N_STAT'] = N_STAT
OUT['mulberry_mean'] = float(u.mean())
OUT['mulberry_var'] = float(u.var(ddof=0))

# the expected values PhET's rules imply, and the tolerances a run of N
# draws is entitled to
put('E_hold_s', 0.5 * (PHET['HOLD_MIN'] + PHET['HOLD_MAX']))
put('sd_hold_s', (PHET['HOLD_MAX'] - PHET['HOLD_MIN']) / math.sqrt(12.0))
se_p = math.sqrt(0.25 / N_STAT)
put('se_absorbed_fraction', se_p, 'binomial standard error at p = 1/2, N = %d' % N_STAT)
put('tol_absorbed_fraction', 4 * se_p, 'the 4-sigma band selfTest uses')
put('two_sided_p_at_4sigma', float(2 * stats.norm.sf(4)), 'how often an honest run fails')
se_hold = ((PHET['HOLD_MAX'] - PHET['HOLD_MIN']) / math.sqrt(12.0)) / math.sqrt(N_STAT)
put('se_hold_mean', se_hold)
put('tol_hold_mean', 4 * se_hold)
se_dir = 1.0 / math.sqrt(2.0 * N_STAT)
put('se_emission_cos', se_dir, 'sd of mean cos over N uniform directions')
put('tol_emission_cos', 4 * se_dir)

# the measured statistics of the actual draws, which the JS must reproduce
# to machine precision because the generator is the same
R = Mulberry32(77003)
nabs = sum(1 for _ in range(N_STAT) if R.next() < PHET['P_ABSORB'])
put('absorbed_count', nabs, 'seed 77003, N = %d' % N_STAT)
put('absorbed_fraction', nabs / N_STAT)
assert abs(nabs / N_STAT - 0.5) < 4 * se_p
R = Mulberry32(77004)
holds = np.array([PHET['HOLD_MIN'] + R.next() * (PHET['HOLD_MAX'] - PHET['HOLD_MIN'])
                  for _ in range(N_STAT)])
put('hold_mean', float(holds.mean()))
put('hold_sd', float(holds.std(ddof=0)))
assert abs(holds.mean() - 1.2) < 4 * se_hold
R = Mulberry32(77005)
ang = np.array([R.next() * 2 * math.pi for _ in range(N_STAT)])
put('emission_mean_cos', float(np.cos(ang).mean()))
put('emission_mean_sin', float(np.sin(ang).mean()))
assert abs(np.cos(ang).mean()) < 4 * se_dir and abs(np.sin(ang).mean()) < 4 * se_dir
# a chi-square over 12 sectors, to catch a generator with structure
cnt = np.histogram(ang, bins=12, range=(0, 2 * math.pi))[0]
chi2 = float(((cnt - N_STAT / 12.0) ** 2 / (N_STAT / 12.0)).sum())
put('emission_chi2_12', chi2, 'df 11; 99.9%% point is %.3f' % stats.chi2.ppf(0.999, 11))
put('emission_chi2_crit', float(stats.chi2.ppf(0.999, 11)))
assert chi2 < stats.chi2.ppf(0.999, 11)
R = Mulberry32(77006)
ncw = sum(1 for _ in range(N_STAT) if R.next() < 0.5)
put('clockwise_fraction', ncw / N_STAT)
# a deliberately biased generator MUST fail the same test
R = Mulberry32(77003)
nbad = sum(1 for _ in range(N_STAT) if R.next() < 0.52)
put('biased_fraction', nbad / N_STAT, 'p = 0.52 instead of 0.5')
put('biased_is_caught', abs(nbad / N_STAT - 0.5) > 4 * se_p)
assert abs(nbad / N_STAT - 0.5) > 4 * se_p
OUT['stat'] = dict(absorbed_count=nabs, absorbed_fraction=nabs / N_STAT,
                   hold_mean=float(holds.mean()), hold_sd=float(holds.std(ddof=0)),
                   emission_mean_cos=float(np.cos(ang).mean()),
                   emission_mean_sin=float(np.sin(ang).mean()),
                   emission_chi2=chi2, clockwise_fraction=ncw / N_STAT,
                   biased_fraction=nbad / N_STAT)

# ===================================================================== #
# 7. chamber kinematics and the duty cycle                              #
# ===================================================================== #
say()
say('=' * 72)
say('7.  chamber kinematics')
say('=' * 72)
t_fly = abs(PHET['EMITTER_X']) / PHET['PHOTON_SPEED']
put('flight_time_s', t_fly, 'emitter to the molecule at 3000 units/s')
put('crossing_time_s', 2 * PHET['ABSORB_RADIUS'] / PHET['PHOTON_SPEED'],
    'time inside the 100-unit absorption sphere')
put('frames_inside_at_60Hz', 2 * PHET['ABSORB_RADIUS'] / PHET['PHOTON_SPEED'] * 60.0)
# PhET marks a photon for pass-through on its FIRST failed trial, so each
# photon gets EXACTLY ONE trial however many frames it spends inside.
put('trials_per_photon', 1, 'the pass-through list makes the first failure final')
put('p_absorb_per_photon', PHET['P_ABSORB'], 'therefore exactly 1/2')
# the busy fraction: while the molecule holds a photon it absorbs nothing,
# and for 0.2 s after it emits one it still absorbs nothing.
busy = 0.5 * (PHET['HOLD_MIN'] + PHET['HOLD_MAX']) + PHET['HYSTERESIS']
put('mean_busy_s', busy, 'mean hold + hysteresis')
put('photons_per_busy_period', busy / PHET['EMIT_PERIOD'], 'at the 0.8 s emission period')
# A renewal estimate.  Assume the phase of the periodic source decorrelates
# from the busy period: the wait to the next photon is then U(0, T), mean
# T/2, and a further (1/p - 1) whole periods are lost to failed trials.
naive_wait = PHET['EMIT_PERIOD'] / 2 + (1 / PHET['P_ABSORB'] - 1) * PHET['EMIT_PERIOD']
naive_cycle = naive_wait + busy
put('renewal_wait_s', naive_wait, 'T/2 + (1/p - 1) T, decorrelated phase')
put('renewal_cycle_s', naive_cycle)
put('renewal_duty', 0.5 * (PHET['HOLD_MIN'] + PHET['HOLD_MAX']) / naive_cycle,
    'hold time / cycle, on that assumption')


# ...and the same thing SIMULATED, by PhET's own rules, with the generator the
# JS carries.  The two do not agree, and the reason is the assumption: the
# busy period is nearly deterministic (the hold's spread is 0.058 s on 1.4)
# and the source is exactly periodic, so the phase does NOT decorrelate.
def chamber_run(seed, mol, band, nsteps, dt=1.0 / 60.0):
    rng = Mulberry32(seed)
    rng.next()                       # the resonance-structure draw the JS makes
    photons, t = [], 0.0
    state, hold, hyst, emit = 'idle', 0.0, 0.0, 0.0
    fired = absorbed = passed = reemit = 0
    busy_t = 0.0
    for _step in range(nsteps):
        t += dt
        if state not in ('idle', 'broken'):
            busy_t += dt
        keep = []
        for p in photons:
            got = False
            if (state != 'broken' and hyst <= 0 and not p['pass']
                    and math.hypot(p['x'], p['y']) < PHET['ABSORB_RADIUS']):
                strat = PHET_TABLE[mol][band]
                if not strat or state != 'idle':
                    p['pass'] = True
                    passed += 1
                elif rng.next() < PHET['P_ABSORB']:
                    absorbed += 1
                    hold = PHET['HOLD_MIN'] + rng.next() * (PHET['HOLD_MAX'] - PHET['HOLD_MIN'])
                    state = {'rotate': 'rot', 'vibrate': 'vib', 'glow': 'glow',
                             'break': 'break'}[strat]
                    if strat == 'rotate':
                        rng.next()                     # the rotation sense
                    if strat == 'break':
                        hold = 0.0
                    got = True
                else:
                    p['pass'] = True
                    passed += 1
            if got:
                continue
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            if PHET['EMITTER_X'] - 200 < p['x'] < 2200 and abs(p['y']) < 1400:
                keep.append(p)
        photons = keep
        emit -= dt
        if emit <= 0:
            photons.append(dict(x=PHET['EMITTER_X'] + PHET['PHOTON_SPEED'] * abs(emit),
                                y=0.0, vx=PHET['PHOTON_SPEED'], vy=0.0, **{'pass': False}))
            fired += 1
            emit = PHET['EMIT_PERIOD']
        if hyst > 0:
            hyst -= dt
        if state == 'break':
            state = 'broken'
        elif state not in ('idle', 'broken'):
            hold -= dt
            if hold <= 0:
                a = rng.next() * 2 * math.pi
                photons.append(dict(x=0.0, y=0.0, vx=PHET['PHOTON_SPEED'] * math.cos(a),
                                    vy=PHET['PHOTON_SPEED'] * math.sin(a), **{'pass': True}))
                reemit += 1
                state, hyst = 'idle', PHET['HYSTERESIS']
    return dict(fired=fired, absorbed=absorbed, passed=passed, reemit=reemit,
                duty=busy_t / t, t=t)


run = chamber_run(4242, 'CO2', 'infrared', 3600)
put('sim_fired', run['fired'], 'CO2 in infrared, seed 4242, 60 s at 1/60 s')
put('sim_absorbed', run['absorbed'])
put('sim_passed', run['passed'])
put('sim_reemit', run['reemit'])
put('sim_duty', run['duty'], 'measured fraction of the time the molecule is excited')
put('sim_absorbed_fraction', run['absorbed'] / (run['absorbed'] + run['passed']),
    'well below 1/2, because a busy molecule refuses every photon')
# A 60 s run is only ~28 cycles, so its duty is noisy.  Run longer and sweep
# the seed to separate the sampling spread from a real systematic difference.
run6 = chamber_run(4242, 'CO2', 'infrared', 36000)
put('sim600_fired', run6['fired'], 'the same run to 600 s')
put('sim600_absorbed', run6['absorbed'])
put('sim600_passed', run6['passed'])
put('sim600_reemit', run6['reemit'])
put('sim600_duty', run6['duty'])
duties = [chamber_run(s, 'CO2', 'infrared', 72000)['duty'] for s in (11, 4242, 90210, 777, 31337)]
mean_duty = sum(duties) / len(duties)
put('sim1200_duty_sweep', [round(d, 4) for d in duties], 'five seeds, 1200 s each')
put('sim1200_duty_mean', mean_duty)
put('sim1200_duty_spread', max(duties) - min(duties))
put('renewal_over_measured', OUT['renewal_duty'] / mean_duty,
    'the renewal estimate is LOW by this factor, and the gap survives the '
    'seed spread -- the source is exactly periodic and the busy time nearly '
    'deterministic, so the phase does not decorrelate')
assert max(duties) - min(duties) < 0.03
assert OUT['renewal_duty'] < min(duties)     # the estimate is low for EVERY seed
OUT['kin'] = dict(t_fly=t_fly, busy=busy, renewal_cycle=naive_cycle, run=run,
                  run600=run6, duties=duties, mean_duty=mean_duty)

# ===================================================================== #
# 8. Planck at 288 K, the window, the composition                       #
# ===================================================================== #
say()
say('=' * 72)
say('8.  the atmosphere')
say('=' * 72)
T_EARTH = 288.0     # the conventional global mean surface temperature


def planck_nubar(nubar_cm, T):
    """spectral radiance per unit wavenumber, W m-2 sr-1 / cm-1"""
    nu = nubar_cm * C_CM                      # s^-1 (cm-1 * cm/s)
    B = 2 * H * nu ** 3 / C ** 2 / (math.exp(H * nu / (KB * T)) - 1.0)
    return B * C_CM                            # per cm-1


put('planck_288_at_667', planck_nubar(667.0, T_EARTH), 'W m-2 sr-1 /cm-1, the CO2 bend')
put('planck_288_at_1000', planck_nubar(1000.0, T_EARTH), 'the middle of the window')
# Wien's displacement for the wavenumber form: x = hc nubar / kT solves
# 3(1-e^-x) = x, x = 2.8214393721...
xw = optimize.brentq(lambda x: 3 * (1 - math.exp(-x)) - x, 1e-6, 10, xtol=1e-15)
put('wien_x_wavenumber', xw, 'root of 3(1-e^-x) = x')
nub_peak = xw * KB * T_EARTH / (H * C_CM)
put('planck_peak_cm', nub_peak, 'peak of B_nubar at 288 K')
put('planck_peak_um', 1e4 / nub_peak)
# Stefan-Boltzmann as a check that the Planck function is normalised right
grid = np.linspace(1.0, 6000.0, 400001)
tot = float(np.trapezoid(np.array([planck_nubar(x, T_EARTH) for x in grid]), grid)) * math.pi
put('integrated_emittance', tot, 'pi * int B dnubar')
put('sigma_T4', sc.sigma * T_EARTH ** 4)
put('planck_integral_rel_err', abs(tot - sc.sigma * T_EARTH ** 4) / (sc.sigma * T_EARTH ** 4))
assert abs(tot - sc.sigma * T_EARTH ** 4) / (sc.sigma * T_EARTH ** 4) < 2e-4
# the fraction of the 288 K emission inside the 8-13 um window
w_lo, w_hi = 1e4 / 13.0, 1e4 / 8.0           # cm-1
g2 = np.linspace(w_lo, w_hi, 20001)
inwin = float(np.trapezoid(np.array([planck_nubar(x, T_EARTH) for x in g2]), g2)) * math.pi
put('window_lo_cm', w_lo)
put('window_hi_cm', w_hi)
put('window_fraction', inwin / tot, 'of the 288 K emission that lies in 8-13 um')

# composition, NASA Earth Fact Sheet (by volume, dry air) + NOAA GML for CO2
COMP = [('N2', 78.084, 'no dipole, no IR-active mode'),
        ('O2', 20.946, 'no dipole, no IR-active mode'),
        ('Ar', 0.934, 'monatomic: no vibration at all'),
        ('CO2', 427.62e-4, 'bend at 667 cm-1, stretch at 2349'),
        ('Ne', 18.18e-4, 'monatomic'),
        ('He', 5.24e-4, 'monatomic'),
        ('CH4', 1.94e-4, 'two IR-active modes, 1306 and 3019 cm-1')]
OUT['COMP'] = COMP
inert = sum(p for n, p, _ in COMP if n in ('N2', 'O2', 'Ar', 'Ne', 'He'))
active = sum(p for n, p, _ in COMP if n in ('CO2', 'CH4'))
put('dry_air_transparent_pct', inert, 'N2 + O2 + Ar + Ne + He, per cent by volume')
put('dry_air_IRactive_pct', active, 'CO2 + CH4, per cent by volume')
put('CO2_ppm', 427.62, 'NOAA GML global monthly mean, June 2026 (preliminary)')

# ===================================================================== #
say()
say('=' * 72)
say('done.  %d reference values.' % len(OUT))
here = os.path.dirname(os.path.abspath(__file__))
io.open(os.path.join(here, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(LINES) + '\n')


def jsonable(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    return o


io.open(os.path.join(here, 'refvals.json'), 'w', encoding='utf-8').write(
    json.dumps(jsonable(OUT), indent=1, sort_keys=True))
print('wrote refvals.txt and refvals.json')
