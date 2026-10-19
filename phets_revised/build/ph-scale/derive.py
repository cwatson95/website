#!/usr/bin/env python3
"""derive.py — the Python twin for ph-scale.html and ph-scale-basics.html.

Re-derives every number the two sims assert and prints them at full double precision into
refvals.txt, which p7_refs.js carries verbatim.  Nothing here is quoted from memory: PhET's
constants were read out of docs/phets/ph-scale_en.html 1.7.6 and are marked (PhET); the
chemistry is exact arithmetic, cross-checked against 50-digit `decimal` evaluation.

WHAT IS PROVED HERE
-------------------
1.  The two concentrations.  [H3O+] = 10^-pH and [OH-] = 10^-(14-pH) = Kw/[H3O+], with
    Kw = 1.000e-14 exactly (pKw = 14.000, the conventional 25 C value, and the one PhET's
    hard-coded `14` encodes).  Both are checked against `decimal` at 50 digits over the whole
    scale including its ends, and the identity [H3O+][OH-] = Kw is checked in doubles.

2.  Molecule counts.  n = c V mol, N = n N_A.  N_A is the exact SI 2019 value
    6.02214076e23 mol^-1; PhET uses 6.023e23, which is 1.30e-4 high, and both are printed.

3.  THE NET STRONG ACID, and why it is the thing that dilutes.  Write
        C(pH) = [H3O+] - [OH-] = 10^-pH - 10^(pH-14).
    C is the analytical excess of strong acid over strong base: it is a difference of
    ANALYTICAL concentrations (the spectator ions cancel in the charge balance), so on mixing
    it is conserved and simply volume-averages, which neither the pH nor either ion does.
    Water has C = 0 exactly.  Two exact rewrites, both used by the sims:
        C(pH)  = -2 sqrt(Kw) sinh( ln10 (pH - 7) )
        pH(C)  = 7 - asinh( C / (2 sqrt(Kw)) ) / ln10
    The naive difference 10^-pH - 10^(pH-14) cancels catastrophically near pH 7 and the naive
    quadratic root (C + sqrt(C^2 + 4Kw))/2 cancels catastrophically for C < 0 (every base);
    the digit loss of both is MEASURED here against the 50-digit value, so the stable forms
    cannot be quietly deleted.

4.  THE MIXING LAW, exactly.  Mixing V1 of pH1 with V2 of pH2 conserves moles of net strong
    acid, so
        C = (C1 V1 + C2 V2) / (V1 + V2),   then re-solve  [H3O+] - Kw/[H3O+] = C.
    Diluting with water (C2 = 0) is therefore C -> C V1/(V1+V2): the NET acid dilutes
    linearly, and the pH follows through the asinh.  This is compared against
      (a) PhET's own rule (model.md and PHModel.computePH): mix the MAJORITY ion linearly and
          take a log, using the branch pH < 7 for acids and 14 + log for bases, with water
          contributing 1e-7 of that ion.  PhET's rule ignores water's autoionisation on the
          minority side, so it is wrong by up to 0.1 pH unit in the dilute limit, and it is
          the difference the sims draw.
      (b) volume-averaging the pH, which is wrong by up to several pH units and is the
          mistake the view exists to rule out.
    Every case is also checked against an independent brute-force root of the full charge
    balance (scipy.optimize.brentq on h - Kw/h - C).

5.  PhET's drawing rules, reimplemented from the original's arithmetic and cited as PhET's:
    the solute colour law (dilutedColor -> colorStopColor at ratio 0.25 -> stockColor), and
    the particle counts (50 dots per 1e-7 mol/L inside pH 6..8, a linear ramp to 3000 at the
    ends of the pH range outside it, floor 5).

6.  The twelve liquids: PhET's pH values, their concentrations, their moles and molecules in
    a full 1.2 L beaker, and the measured ranges that could be sourced.
"""
import io
import math
import os
from decimal import Decimal, getcontext

from scipy import optimize

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
CHECKS = []


def emit(label, *vals):
    """One reference line: a label and its values at FULL double precision.

    '%.17g' round-trips a double exactly, so the JavaScript twin is pinned bit for bit."""
    OUT.append(label + '\t' + '\t'.join('%.17g' % v for v in vals))


def check(name, cond, detail=''):
    CHECKS.append((name, bool(cond), detail))
    print('%-6s %s%s' % ('ok' if cond else 'FAIL', name, ('   ' + detail) if detail else ''))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ======================================================================== #
#  0.  Constants                                                            #
# ======================================================================== #
# Kw = 1.000e-14 exactly: the conventional value at 25 C, and the one PhET's hard-coded 14
# encodes (PHModel.ts writes 14 - pH and 14 + log10 everywhere).  pKw is therefore 14.000
# exactly here and neutral water is pH 7.000 exactly.  The real pKw at 25 C is slightly
# below 14 and it moves with temperature; none of that is modelled, and the sims say so.
PKW = 14.0
KW = 1e-14
SQRTKW = 1e-7
LN10 = math.log(10.0)

NA_SI = 6.02214076e23          # exact, SI 2019 definition of the mole
NA_PHET = 6.023e23             # PhET's value, doc/model.md and PHModel.computeParticleCount

emit('KW pKw sqrtKw ln10', KW, PKW, SQRTKW, LN10)
emit('NA si phet rel', NA_SI, NA_PHET, rel(NA_PHET, NA_SI))
check('Kw = 10^-pKw', abs(KW - 10.0 ** -PKW) < 1e-30)
check('sqrt(Kw) = 1e-7', abs(SQRTKW - math.sqrt(KW)) < 1e-22)
check("PhET's N_A is 1.43e-4 high", 1.4e-4 < rel(NA_PHET, NA_SI) < 1.5e-4,
      'rel %.4e' % rel(NA_PHET, NA_SI))

# --- PhET's constants, read from docs/phets/ph-scale_en.html 1.7.6 --------------------- #
PHET = dict(
    BEAKER_VOLUME=1.2,          # PHScaleConstants.BEAKER_VOLUME, L
    MIN_SOLUTION_VOLUME=0.015,  # PHScaleConstants.MIN_SOLUTION_VOLUME, L
    PH_MIN=-1.0, PH_MAX=15.0, PH_DEFAULT=7.0,   # PHScaleConstants.PH_RANGE
    PH_DECIMALS=2,              # PHScaleConstants.PH_METER_DECIMAL_PLACES
    VOL_DECIMALS=2,             # PHScaleConstants.VOLUME_DECIMAL_PLACES
    MY_VOL_MIN=0.01, MY_VOL_DEFAULT=0.5,        # MySolution's totalVolumeProperty
    DROPPER_FLOW=0.05,          # Dropper maxFlowRate, L/s
    FAUCET_FLOW=0.25,           # Faucet maxFlowRate, L/s (water and drain)
    AUTOFILL_VOLUME=0.5,        # PHModel autofillVolume, L
    AUTOFILL_FLOW=0.45,         # startAutofill flowRate, L/s
    WATER_CONC=55.0,            # Water.concentration, mol/L
    WATER_PH=7.0,               # Water.pH
    LOG_EXP_MIN=-16.0, LOG_EXP_MAX=2.0,         # LOGARITHMIC_EXPONENT_RANGE
    LIN_EXP_MIN=-14.0, LIN_EXP_MAX=1.0,         # LINEAR_EXPONENT_RANGE
    LIN_MANTISSA_MAX=8.0,       # LINEAR_MANTISSA_RANGE
    DOTS_AT_PH7=50.0,           # ParticlesNode: round(50 * c / 1e-7)
    DOTS_REF_CONC=1e-7,
    DOTS_MIN=5.0,               # Math.max(5, ...)
    DOTS_MAX=3000.0,            # the ramp's top at the ends of PH_RANGE
    DOTS_PH_LO=6.0, DOTS_PH_HI=8.0,             # the window where the true counts are used
    COLOR_STOP_RATIO=0.25,      # Solute's default colorStopRatio
)
for k in sorted(PHET):
    emit('PHET ' + k, PHET[k])

# PhET's twelve solutes: name, pH, stock colour, colour-stop colour (None = no stop).
# Read verbatim from the Solute.BATTERY_ACID ... Solute.WATER block of the minified original.
SOLUTES = [
    ('Battery Acid',  1.0,  (255, 255, 0),   (255, 224, 204)),
    ('Blood',         7.4,  (211, 79, 68),   (255, 207, 204)),
    ('Chicken Soup',  5.8,  (255, 240, 104), (255, 250, 204)),
    ('Coffee',        5.0,  (164, 99, 7),    (255, 240, 204)),
    ('Drain Cleaner', 13.0, (255, 255, 0),   (255, 255, 204)),
    ('Hand Soap',     10.0, (224, 141, 242), (232, 204, 255)),
    ('Milk',          6.5,  (250, 250, 250), None),
    ('Orange Juice',  3.5,  (255, 180, 0),   (255, 242, 204)),
    ('Soda Pop',      2.5,  (204, 255, 102), (238, 255, 204)),
    ('Spit',          7.4,  (202, 240, 239), None),
    ('Vomit',         2.0,  (255, 171, 120), (255, 224, 204)),
    ('Water',         7.0,  (224, 255, 255), None),
]
WATER_RGB = (224, 255, 255)     # PHScaleColors.WATER, and Solute's default dilutedColor
emit('SOLUTE pH values', *[s[1] for s in SOLUTES])
check('twelve solutes', len(SOLUTES) == 12)
check('PhET water is pH 7 and its own colour',
      SOLUTES[11][1] == PHET['WATER_PH'] and SOLUTES[11][2] == WATER_RGB)


# ======================================================================== #
#  1.  The two concentrations, against 50-digit decimal                     #
# ======================================================================== #
def conc_h3o(ph):
    return math.pow(10.0, -ph)


def conc_oh(ph):
    """Kw / [H3O+], NOT 10^(pH-14).

    The two are the same on paper and not in doubles: pH - 14 is inexact whenever pH < 7
    (5.8 - 14 needs one bit more than a double carries), so PhET's spelling
    10^-(14 - pH) is out by up to 1.7e-15 relative while the division is out by half an
    ulp and makes the identity [H3O+][OH-] = Kw hold to a rounding.  Measured below."""
    return KW / math.pow(10.0, -ph)


def conc_oh_phet(ph):
    """PhET's spelling: pHToConcentrationH3O(14 - pH) = 10^-(14 - pH)."""
    return math.pow(10.0, -(PKW - ph))


def conc_h3o_exact(ph):
    """50-digit truth at the EXACT double value of ph — Decimal(ph), never Decimal(repr(ph)),
    which is a different number and makes a correct formula look wrong by 1e-12."""
    return Decimal(10) ** Decimal(-ph)


def conc_oh_exact(ph):
    """The mathematical truth 10^(pH-14) at the exact double value of ph."""
    return Decimal(10) ** (Decimal(ph) - Decimal(14))


PH_GRID = [-1.0, -0.5, 0.0, 1.0, 2.0, 2.5, 3.5, 5.0, 5.8, 6.0, 6.5, 6.9, 6.99, 7.0,
           7.01, 7.1, 7.4, 8.0, 10.0, 11.5, 13.0, 14.0, 14.5, 15.0]
worst_h, worst_o, worst_id, worst_phet_oh = 0.0, 0.0, 0.0, 0.0
for ph in PH_GRID:
    h, o = conc_h3o(ph), conc_oh(ph)
    he, oe = float(conc_h3o_exact(ph)), float(conc_oh_exact(ph))
    worst_h = max(worst_h, rel(h, he))
    worst_o = max(worst_o, rel(o, oe))
    worst_id = max(worst_id, rel(h * o, KW))
    worst_phet_oh = max(worst_phet_oh, rel(conc_oh_phet(ph), oe))
emit('CONC worst rel err h3o oh, identity h*o=Kw, PhET spelling of OH',
     worst_h, worst_o, worst_id, worst_phet_oh)
check('[H3O+] = 10^-pH to 1e-15 of the 50-digit value over the whole scale',
      worst_h < 1e-15, 'worst %.3e' % worst_h)
check('[OH-] = Kw/[H3O+] to 3e-16 likewise', worst_o < 3e-16, 'worst %.3e' % worst_o)
check('and [H3O+][OH-] = Kw in doubles to 3e-16', worst_id < 3e-16, 'worst %.3e' % worst_id)
check('while PhET\'s 10^-(14-pH) is five times worse (the pH-14 subtraction)',
      worst_phet_oh > 5 * worst_o, 'PhET %.3e vs %.3e' % (worst_phet_oh, worst_o))
# the ends of PhET's range, printed in full so the JS twin can be pinned bit for bit
for ph in (-1.0, 0.0, 1.0, 7.0, 13.0, 14.0, 15.0):
    emit('CONC at pH %g' % ph, conc_h3o(ph), conc_oh(ph))
# two exponents that are NOT round numbers, so a mutated 14 cannot hide behind a round answer
emit('CONC at pH 5.8 7.4 2.5', conc_h3o(5.8), conc_oh(5.8), conc_h3o(7.4), conc_oh(7.4),
     conc_h3o(2.5), conc_oh(2.5))

# moles and molecules
emit('COUNT pH7 1.2L moles molecules si phet',
     conc_h3o(7.0) * 1.2, conc_h3o(7.0) * 1.2 * NA_SI, conc_h3o(7.0) * 1.2 * NA_PHET)
emit('COUNT water 55 molar in 1.2L', PHET['WATER_CONC'] * 1.2,
     PHET['WATER_CONC'] * 1.2 * NA_SI)
emit('COUNT drain cleaner pH13 0.5L OH molecules', conc_oh(13.0) * 0.5 * NA_SI)
check('a 1.2 L beaker of neutral water holds 7.2e16 hydronium ions',
      abs(conc_h3o(7.0) * 1.2 * NA_SI - 7.2265689e16) < 1e10,
      '%.6e' % (conc_h3o(7.0) * 1.2 * NA_SI))


# ======================================================================== #
#  2.  The net strong acid, and the two stable rewrites                     #
# ======================================================================== #
def net_naive(ph):
    """[H3O+] - [OH-] as written: catastrophic cancellation near pH 7."""
    return conc_h3o(ph) - conc_oh(ph)


def net_stable(ph):
    """The same quantity as -2 sqrt(Kw) sinh(ln10 (pH - 7)) — exact everywhere."""
    return -2.0 * SQRTKW * math.sinh(LN10 * (ph - 0.5 * PKW))


def net_exact(ph):
    return conc_h3o_exact(ph) - conc_oh_exact(ph)


def ph_of_net_asinh(c):
    """pH(C) in closed form.  asinh is stable for every sign and magnitude of C."""
    return 0.5 * PKW - math.asinh(c / (2.0 * SQRTKW)) / LN10


def h_of_net_stable(c):
    """[H3O+] from C, on the branch of the quadratic root that does not cancel."""
    r = math.sqrt(c * c + 4.0 * KW)
    return 0.5 * (c + r) if c >= 0.0 else 2.0 * KW / (r - c)


def h_of_net_naive(c):
    """The textbook root, which loses every digit for C < 0."""
    return 0.5 * (c + math.sqrt(c * c + 4.0 * KW))


def ph_of_net(c):
    return -math.log10(h_of_net_stable(c))


def h_of_net_brute(c):
    """An independent route: root of h - Kw/h - C by bisection, no formula reused."""
    lo, hi = 1e-20, 1e2
    return optimize.brentq(lambda h: h - KW / h - c, lo, hi, xtol=1e-300, rtol=8.9e-16)


worst_stable, worst_naive = 0.0, 0.0
for ph in PH_GRID + [6.999, 7.001, 6.9999, 7.0001, 6.999999, 7.000001]:
    ce = net_exact(ph)
    worst_stable = max(worst_stable, rel(net_stable(ph), float(ce)))
    if abs(float(ce)) > 1e-300:
        worst_naive = max(worst_naive, rel(net_naive(ph), float(ce)))
emit('NET worst rel err stable naive', worst_stable, worst_naive)
check('C = -2 sqrt(Kw) sinh(ln10 (pH-7)) matches the 50-digit difference to 1e-14',
      worst_stable < 1e-14, 'worst %.3e' % worst_stable)
check('and the naive difference is a thousand times worse near neutral',
      worst_naive > 1000 * worst_stable, 'naive %.3e vs %.3e' % (worst_naive, worst_stable))
# where exactly the naive difference dies: the relative error grows as 1/(7 - pH), because
# the absolute error of a difference of two numbers of size 1e-7 is fixed at ~1e-23 while
# the answer itself vanishes.  The sims never evaluate C closer than 0.01 pH to neutral --
# the twelve solutes are fixed values and the My Solution slider steps by 0.01 -- so this is
# a guard rather than a hot path, and the file says so.
for ph in (6.999999, 6.9999, 6.999, 6.99, 6.9):
    e = rel(net_naive(ph), float(net_exact(ph)))
    emit('NET naive rel err at pH %.6f' % ph, e)
    print('       naive C(pH=%s) rel err %.3e' % (ph, e))

worst_rt, worst_brute, worst_naive_h = 0.0, 0.0, 0.0
for ph in PH_GRID:
    c = net_stable(ph)
    worst_rt = max(worst_rt, abs(ph_of_net_asinh(c) - ph), abs(ph_of_net(c) - ph))
    worst_brute = max(worst_brute, rel(h_of_net_stable(c), h_of_net_brute(c)))
    worst_naive_h = max(worst_naive_h, rel(h_of_net_naive(c), conc_h3o(ph)))
emit('NET roundtrip worst, brute agreement, naive root worst',
     worst_rt, worst_brute, worst_naive_h)
check('pH -> C -> pH round-trips to 1e-12 over the whole scale, both routes',
      worst_rt < 1e-12, 'worst %.3e' % worst_rt)
check('the stable root agrees with brentq on h - Kw/h = C to 1e-12',
      worst_brute < 1e-12, 'worst %.3e' % worst_brute)
check('the naive quadratic root loses its digits for bases (>1e-3 somewhere)',
      worst_naive_h > 1e-3, 'worst %.3e' % worst_naive_h)
for ph in (13.0, 14.0, 15.0):
    c = net_stable(ph)
    e = rel(h_of_net_naive(c), conc_h3o(ph))
    emit('NET naive root rel err at pH %g' % ph, e)
    print('       naive root rel err at pH %g: %.3e' % (ph, e))
emit('NET C at pH 1 7 13 14', net_stable(1.0), net_stable(7.0), net_stable(13.0),
     net_stable(14.0))
check('C is exactly zero at pH 7', net_stable(7.0) == 0.0)
check('C is positive for acids and negative for bases',
      net_stable(3.0) > 0 > net_stable(11.0))


# ======================================================================== #
#  3.  The mixing law                                                       #
# ======================================================================== #
def mix_net(ph1, v1, ph2, v2):
    """The net strong acid of the mixture: moles of C, per litre of the total."""
    vt = v1 + v2
    return None if vt <= 0.0 else (net_stable(ph1) * v1 + net_stable(ph2) * v2) / vt


def mix_exact(ph1, v1, ph2, v2):
    """Conserve moles of NET strong acid, then re-solve the charge balance with Kw.

    The two degenerate cases are exact rather than round-tripped, as PhET's are: adding
    nothing leaves the stock pH, and a beaker of water alone is pH 7."""
    vt = v1 + v2
    if vt <= 0.0:
        return None
    if v2 == 0.0:
        return ph1
    if v1 == 0.0:
        return ph2
    return ph_of_net(mix_net(ph1, v1, ph2, v2))


def mix_exact_brute(ph1, v1, ph2, v2):
    """The same, through the independent root finder and a mole ledger done in Decimal."""
    vt = Decimal(repr(v1)) + Decimal(repr(v2))
    if vt <= 0:
        return None
    moles = net_exact(ph1) * Decimal(repr(v1)) + net_exact(ph2) * Decimal(repr(v2))
    c = float(moles / vt)
    return -math.log10(h_of_net_brute(c))


def mix_phet(ph1, v1, v2):
    """PhET's own rule (doc/model.md, PHModel.computePH), reimplemented from its arithmetic."""
    vt = v1 + v2
    if vt == 0.0:
        return None
    if v2 == 0.0:
        return ph1
    if v1 == 0.0:
        return PHET['WATER_PH']
    if ph1 < 7.0:
        return -math.log10((math.pow(10.0, -ph1) * v1
                            + math.pow(10.0, -PHET['WATER_PH']) * v2) / vt)
    return PKW + math.log10((math.pow(10.0, ph1 - PKW) * v1
                             + math.pow(10.0, PHET['WATER_PH'] - PKW) * v2) / vt)


def mix_average(ph1, v1, ph2, v2):
    """Volume-averaging the pH — the mistake the dilution view exists to rule out."""
    vt = v1 + v2
    return None if vt == 0 else (ph1 * v1 + ph2 * v2) / vt


CASES = [(ph, v1, 1.2 - v1) for ph in (1.0, 2.5, 5.0, 5.8, 6.5, 7.0, 7.4, 10.0, 13.0)
         for v1 in (0.1, 0.3, 0.6, 1.0, 1.2)]
worst_mix, worst_dPhet, worst_dAvg = 0.0, 0.0, 0.0
arg_phet, arg_avg = None, None
for ph, v1, v2 in CASES:
    a = mix_exact(ph, v1, PHET['WATER_PH'], v2)
    b = mix_exact_brute(ph, v1, PHET['WATER_PH'], v2)
    p = mix_phet(ph, v1, v2)
    m = mix_average(ph, v1, PHET['WATER_PH'], v2)
    worst_mix = max(worst_mix, abs(a - b))
    if abs(a - p) > worst_dPhet:
        worst_dPhet, arg_phet = abs(a - p), (ph, v1, v2, a, p)
    if abs(a - m) > worst_dAvg:
        worst_dAvg, arg_avg = abs(a - m), (ph, v1, v2, a, m)
emit('MIX exact vs brute worst', worst_mix)
check('the exact mixing law agrees with the Decimal ledger + brentq to 1e-12',
      worst_mix < 1e-12, 'worst %.3e' % worst_mix)
emit('MIX worst |exact - PhET| over the beaker, and where',
     worst_dPhet, arg_phet[0], arg_phet[1], arg_phet[2], arg_phet[3], arg_phet[4])
emit('MIX worst |exact - averaged pH|, and where',
     worst_dAvg, arg_avg[0], arg_avg[1], arg_avg[2], arg_avg[3], arg_avg[4])
print('       worst |exact - PhET|   = %.6f pH  at pH %.1f, %.2f L in %.2f L'
      % (worst_dPhet, arg_phet[0], arg_phet[1], arg_phet[1] + arg_phet[2]))
print('       worst |exact - avg pH| = %.6f pH  at pH %.1f, %.2f L in %.2f L'
      % (worst_dAvg, arg_avg[0], arg_avg[1], arg_avg[1] + arg_avg[2]))
check('PhET\'s rule differs from the exact one by more than 0.01 pH somewhere reachable',
      worst_dPhet > 0.01)
check('and averaging the pH is wrong by more than a whole pH unit', worst_dAvg > 1.0)

# a named case each way, printed in full for the JS suite
for ph, v1, v2 in [(1.0, 0.1, 1.1), (5.0, 0.1, 1.1), (6.5, 0.1, 1.1), (7.4, 0.1, 1.1),
                   (10.0, 0.1, 1.1), (13.0, 0.1, 1.1), (5.8, 0.6, 0.6), (2.5, 0.3, 0.9)]:
    emit('MIX pH %g, %g L + %g L water: exact phet avg' % (ph, v1, v2),
         mix_exact(ph, v1, PHET['WATER_PH'], v2), mix_phet(ph, v1, v2),
         mix_average(ph, v1, PHET['WATER_PH'], v2))

# the undiluted and the pure-water limits, where PhET and the exact law must agree exactly
check('with no water added both laws return the stock pH exactly',
      all(mix_exact(ph, 0.5, 7.0, 0.0) == ph and mix_phet(ph, 0.5, 0.0) == ph
          for ph in (1.0, 5.0, 7.0, 10.0, 13.0)))
check('with no solute both return 7 exactly',
      mix_exact(3.0, 0.0, 7.0, 1.0) == 7.0 and mix_phet(3.0, 0.0, 1.0) == 7.0)

# THE LAW ITSELF: diluting with water scales the net acid by the volume ratio.
# Asserted on C directly — going out through the pH and back is a different measurement,
# and a far coarser one (below).
worst_scale = 0.0
for ph in (1.0, 3.5, 6.9, 7.1, 10.0, 13.0):
    for f in (2.0, 10.0, 1000.0, 1e6):
        v1, v2 = 1.0, f - 1.0
        worst_scale = max(worst_scale, rel(mix_net(ph, v1, 7.0, v2), net_stable(ph) / f))
emit('MIX net acid scales as V0/V, worst rel err', worst_scale)
check('diluting f-fold divides the net strong acid by exactly f',
      worst_scale < 1e-14, 'worst %.3e' % worst_scale)

# ... and the price of carrying the STATE as a pH instead of as a C.  Near neutral the pH
# is 7 - eps with eps tiny, and a double holds 7 - eps to an absolute 8.9e-16, so eps
# itself keeps only the digits that are left: a 1e6-fold dilution of pH 6.9 recovers its
# own net acid to 4e-9, not to 1e-16.  The sims therefore keep (V_solute, V_water) and
# re-derive the pH, never the other way round.
worst_rt_scale, worst_rt_1000 = 0.0, 0.0
for ph in (1.0, 3.5, 6.9, 7.1, 10.0, 13.0):
    for f, bucket in ((1000.0, 'k'), (1e6, 'M')):
        v1, v2 = 1.0, f - 1.0
        e = rel(net_stable(mix_exact(ph, v1, 7.0, v2)), net_stable(ph) / f)
        if bucket == 'M':
            worst_rt_scale = max(worst_rt_scale, e)
        else:
            worst_rt_1000 = max(worst_rt_1000, e)
emit('MIX pH round-trip loss at 1e6-fold and 1e3-fold dilution',
     worst_rt_scale, worst_rt_1000)
check('and a round trip through a stored pH costs eight digits at 1e6-fold dilution',
      worst_rt_scale > 1e-10 > worst_rt_1000,
      '1e6-fold %.3e, 1e3-fold %.3e' % (worst_rt_scale, worst_rt_1000))

# the dilute limit: infinite dilution is pH 7 from either side, and PhET's rule is NOT
emit('MIX infinite dilution exact phet at pH 1 and 13',
     mix_exact(1.0, 1e-12, 7.0, 1.0), mix_phet(1.0, 1e-12, 1.0),
     mix_exact(13.0, 1e-12, 7.0, 1.0), mix_phet(13.0, 1e-12, 1.0))

# the worst the two laws can differ anywhere a user can actually reach: PhET's pH range
# crossed with a beaker from its 0.015 L minimum to its 1.2 L brim
gw, garg = 0.0, None
for i in range(0, 1601):
    ph = -1.0 + i * 0.01
    for j in range(1, 80):
        v1 = 0.015 * j
        if v1 > 1.2:
            break
        d = abs(mix_exact(ph, v1, 7.0, 1.2 - v1) - mix_phet(ph, v1, 1.2 - v1))
        if d > gw:
            gw, garg = d, (ph, v1)
emit('MIX worst difference anywhere in the beaker, pH, V_solute', gw, garg[0], garg[1])
print('       worst |exact - PhET| anywhere reachable: %.6f pH at pH %.2f, %.3f L in 1.2 L'
      % (gw, garg[0], garg[1]))
check('the two laws never differ by more than a tenth of a pH unit in this beaker',
      0.05 < gw < 0.12, '%.6f' % gw)

# a sweep over stock pH at a fixed dilution, for the difference panel
SWEEP = []
for i in range(0, 141):
    ph = i * 0.1
    SWEEP.append((ph, mix_exact(ph, 0.1, 7.0, 1.1) - mix_phet(ph, 0.1, 1.1)))
best = max(SWEEP, key=lambda t: abs(t[1]))
emit('SWEEP 0.1L in 1.2L: worst pH and difference', best[0], best[1])
print('       0.1 L in 1.2 L: |exact - PhET| peaks at pH %.1f, %.5f pH units'
      % (best[0], best[1]))
emit('SWEEP 0.1L in 1.2L at pH 5 6 6.5 8 9',
     mix_exact(5.0, 0.1, 7.0, 1.1) - mix_phet(5.0, 0.1, 1.1),
     mix_exact(6.0, 0.1, 7.0, 1.1) - mix_phet(6.0, 0.1, 1.1),
     mix_exact(6.5, 0.1, 7.0, 1.1) - mix_phet(6.5, 0.1, 1.1),
     mix_exact(8.0, 0.1, 7.0, 1.1) - mix_phet(8.0, 0.1, 1.1),
     mix_exact(9.0, 0.1, 7.0, 1.1) - mix_phet(9.0, 0.1, 1.1))

# C(pH) is ODD about pH 7, because sinh is odd: 10^-pH - 10^(pH-14) changes sign and not
# magnitude under pH -> 14 - pH.  So pH 2 and pH 12 are EXACTLY as strong as each other and
# neutralise completely, which is the opposite of the "the acid is stronger" instinct and is
# worth pinning.  PhET's branch rule is symmetric under the same reflection, so the
# difference between the two laws is an ODD function of pH about 7 -- which is what the
# dilution view's difference panel draws.
worst_odd, worst_odd_phet = 0.0, 0.0
for ph in [x * 0.25 for x in range(-4, 61)]:
    worst_odd = max(worst_odd, rel(net_stable(PKW - ph), -net_stable(ph)))
    if 0.0 < ph < 14.0:
        a = mix_exact(ph, 0.1, 7.0, 1.1) - mix_phet(ph, 0.1, 1.1)
        b = mix_exact(PKW - ph, 0.1, 7.0, 1.1) - mix_phet(PKW - ph, 0.1, 1.1)
        worst_odd_phet = max(worst_odd_phet, abs(a + b))
emit('SYMMETRY C odd about pH 7, PhET-vs-exact difference odd too',
     worst_odd, worst_odd_phet)
check('C(14 - pH) = -C(pH) exactly (sinh is odd)', worst_odd < 1e-14,
      'worst %.3e' % worst_odd)
check('so the exact-minus-PhET difference is odd about pH 7 too',
      worst_odd_phet < 1e-12, 'worst %.3e' % worst_odd_phet)

# mixing two SOLUTIONS (not just water): an acid and a base neutralise, which PhET's
# single-solute model never does and the exact law handles without a special case
emit('MIX acid+base 0.5L pH2+pH12, pH2+pH11, pH1+pH13',
     mix_exact(2.0, 0.5, 12.0, 0.5), mix_exact(2.0, 0.5, 11.0, 0.5),
     mix_exact(1.0, 0.5, 13.0, 0.5))
check('equal volumes of pH 2 and pH 12 are EXACTLY neutral, not acidic',
      abs(mix_exact(2.0, 0.5, 12.0, 0.5) - 7.0) < 1e-12,
      '%.9f' % mix_exact(2.0, 0.5, 12.0, 0.5))
check('but pH 2 with pH 11 stays acidic: the acid is ten times the stronger',
      2.3 < mix_exact(2.0, 0.5, 11.0, 0.5) < 2.4,
      '%.6f' % mix_exact(2.0, 0.5, 11.0, 0.5))


# ======================================================================== #
#  4.  PhET's drawing rules                                                 #
# ======================================================================== #
def solute_color(stock, stop, ratio):
    """PhET's Solute.computeColor, reimplemented from its arithmetic.

    ratio = V_solute / V_total.  With a colour stop the ramp is diluted->stop over
    [0, 0.25] and stop->stock over [0.25, 1]; without one it is diluted->stock over [0,1]."""
    r = PHET['COLOR_STOP_RATIO']

    def lerp(a, b, t):
        return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    if stop is None:
        return lerp(WATER_RGB, stock, ratio)
    if ratio > r:
        return lerp(stop, stock, (ratio - r) / (1.0 - r))
    return lerp(WATER_RGB, stop, ratio / r)


emit('COLOR coffee at 0 0.25 1',
     *(list(solute_color((164, 99, 7), (255, 240, 204), 0.0))
       + list(solute_color((164, 99, 7), (255, 240, 204), 0.25))
       + list(solute_color((164, 99, 7), (255, 240, 204), 1.0))))
# 0.5 is the one ratio at which lerp(water, stock, r) and lerp(stock, water, r) agree, so
# a no-stop colour tested only there is tested by nothing (the mutation sweep proved it)
emit('COLOR milk (no stop) at 0.25 0.5 0.75',
     *(list(solute_color((250, 250, 250), None, 0.25))
       + list(solute_color((250, 250, 250), None, 0.5))
       + list(solute_color((250, 250, 250), None, 0.75))))
check('an undiluted solute is its stock colour',
      solute_color((164, 99, 7), (255, 240, 204), 1.0) == (164.0, 99.0, 7.0))
check('and a vanishing one is water', solute_color((164, 99, 7), (255, 240, 204), 0.0)
      == tuple(float(x) for x in WATER_RGB))


def dots(ph, which):
    """PhET's ParticlesNode.update, reimplemented from its arithmetic.

    Inside pH 6..8 the two counts are the true concentrations at 50 dots per 1e-7 mol/L
    (floored at 5).  Outside it the majority saturates and the minority ramps linearly to
    3000 at the ends of PH_RANGE, which is a drawing rule and not a concentration."""
    def raw_h(p):
        return PHET['DOTS_AT_PH7'] * conc_h3o(p) / PHET['DOTS_REF_CONC']

    def raw_o(p):
        return PHET['DOTS_AT_PH7'] * conc_oh(p) / PHET['DOTS_REF_CONC']
    lo, hi = PHET['DOTS_PH_LO'], PHET['DOTS_PH_HI']
    if lo <= ph <= hi:
        h, o = max(PHET['DOTS_MIN'], raw_h(ph)), max(PHET['DOTS_MIN'], raw_o(ph))
    else:
        slope = (PHET['DOTS_MAX'] - raw_o(hi)) / (PHET['PH_MAX'] - hi)
        if ph > hi:
            s = ph - hi
            h, o = max(PHET['DOTS_MIN'], raw_h(hi) - s), raw_o(hi) + s * slope
        else:
            s = lo - ph
            h, o = raw_h(lo) + s * slope, max(PHET['DOTS_MIN'], raw_o(lo) - s)
    r = (lambda x: math.floor(x + 0.5))
    return r(h), r(o)


emit('DOTS at pH 7 6 8 1 13 15 -1',
     *[float(v) for p in (7.0, 6.0, 8.0, 1.0, 13.0, 15.0, -1.0) for v in dots(p, None)])
check('fifty dots each at pH 7 (PhET)', dots(7.0, None) == (50, 50))
check('at pH 6 that is 500 hydronium and 5 hydroxide (PhET floors the minority at 5)',
      dots(6.0, None) == (500, 5), str(dots(6.0, None)))
check('at pH 15 the hydroxide count reaches PhET\'s 3000', dots(15.0, None)[1] == 3000,
      str(dots(15.0, None)))
check('the true ratio at pH 13 is 1e12 : 1 while the drawn ratio is only',
      dots(13.0, None)[1] / dots(13.0, None)[0] < 1e4,
      '%.1f : 1 drawn, %.3e : 1 true' % (dots(13.0, None)[1] / dots(13.0, None)[0],
                                         conc_oh(13.0) / conc_h3o(13.0)))
emit('DOTS drawn vs true ratio at pH 13',
     dots(13.0, None)[1] / float(dots(13.0, None)[0]), conc_oh(13.0) / conc_h3o(13.0))


# ======================================================================== #
#  5.  The twelve liquids                                                   #
# ======================================================================== #
print('\n  PhET\'s twelve liquids, and what the chemistry makes of them')
print('  %-14s %6s  %12s  %12s  %14s' % ('liquid', 'pH', '[H3O+] M', '[OH-] M', 'H3O+ in 1.2 L'))
for nm, ph, _st, _cs in SOLUTES:
    print('  %-14s %6.2f  %12.4e  %12.4e  %14.4e'
          % (nm, ph, conc_h3o(ph), conc_oh(ph), conc_h3o(ph) * 1.2 * NA_SI))
emit('LIQUID h3o', *[conc_h3o(s[1]) for s in SOLUTES])
emit('LIQUID oh', *[conc_oh(s[1]) for s in SOLUTES])
emit('LIQUID molecules h3o in 1.2 L', *[conc_h3o(s[1]) * 1.2 * NA_SI for s in SOLUTES])

# --- the measured ranges that could be sourced -------------------------------------- #
# Four of the twelve.  Everything else in PhET's list carries PhET's value alone and the
# sims say so on the canvas rather than inventing a range for it.
MEASURED = [
    ('Blood', 7.37, 7.43,
     'Merck Manual Professional, "Acid-Base Regulation" (J. L. Lewis III): '
     '"typically 37 to 43 nEq/L ... with a pH of 7.43 to 7.37"'),
    ('Orange Juice', 3.30, 4.19,
     'FDA, "Approximate pH of Foods and Food Products", row "Orange Juice, California" '
     '(the Florida row is 3.30-4.15)'),
    ('Milk', 6.40, 6.80, 'FDA, same table, row "Milk, cow"'),
    ('Chicken Soup', 5.80, 5.80, 'FDA, same table, row "Chicken Broth, rts." (one value)'),
]
emit('MEASURED blood oj milk soup lo hi',
     *[v for m in MEASURED for v in (m[1], m[2])])
for nm, lo, hi, _s in MEASURED:
    ph = dict((s[0], s[1]) for s in SOLUTES)[nm]
    inside = lo - 1e-12 <= ph <= hi + 1e-12
    check('PhET\'s %s (pH %.2f) lies inside its sourced range %.2f-%.2f'
          % (nm, ph, lo, hi), inside)
check('four of the twelve liquids have a sourced measured range', len(MEASURED) == 4)

# the flow arithmetic: PhET's autofill and its faucets
emit('FLOW autofill seconds, dropper seconds to fill, faucet seconds to fill',
     PHET['AUTOFILL_VOLUME'] / PHET['AUTOFILL_FLOW'],
     PHET['BEAKER_VOLUME'] / PHET['DROPPER_FLOW'],
     PHET['BEAKER_VOLUME'] / PHET['FAUCET_FLOW'])
check('PhET\'s autofill of 0.5 L at 0.45 L/s takes 1.111 s',
      abs(PHET['AUTOFILL_VOLUME'] / PHET['AUTOFILL_FLOW'] - 1.1111111111111112) < 1e-15)

# the graph axes
emit('GRAPH log decades, linear top',
     PHET['LOG_EXP_MAX'] - PHET['LOG_EXP_MIN'],
     PHET['LIN_MANTISSA_MAX'] * math.pow(10.0, PHET['LIN_EXP_MAX']))
check('PhET\'s logarithmic graph spans 18 decades',
      PHET['LOG_EXP_MAX'] - PHET['LOG_EXP_MIN'] == 18.0)

# ======================================================================== #
#  6.  Write refvals.txt                                                    #
# ======================================================================== #
io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
bad = [n for n, okc, _ in CHECKS if not okc]
print('\n%d checks, %d failed' % (len(CHECKS), len(bad)))
for n in bad:
    print('   FAILED:', n)
print('refvals.txt: %d reference lines' % len(OUT))
raise SystemExit(1 if bad else 0)
