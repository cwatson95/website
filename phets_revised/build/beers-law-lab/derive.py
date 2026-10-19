#!/usr/bin/env python3
"""derive.py — the Python twin of beers-law-lab.html / concentration.html.

Re-derives every closed form the sims implement and prints reference values to 17 digits
into refvals.txt, which make_refs.py turns into p7_refs.js.  Nothing in the JS suite is
asserted against a number that is not a line of that file.

What is checked here
--------------------
1.  Beer-Lambert, A = eps * l * c and T = 10^-A, against 50-digit Decimal arithmetic, in
    both directions, including the two extremes (A = 0 and A so large that 10^-A underflows
    a double).
2.  PhET's molar-absorptivity spectra, read out of the minified original by extract_phet.py:
    lambda_max, the quantisation rule eps(lambda) = table[floor(lambda - 380)], and the
    largest absorbance each solution can reach in a 2 cm cuvette.
3.  The Concentration screen's mole ledger: a 900-frame script driving the faucet, the drain,
    the dropper, the evaporator and the shaker, run twice -- once in floats, once in exact
    Fractions -- with the ledger closed both ways.
4.  Saturation: C = min(Csat, n/V), precipitate = max(0, n - V Csat), and the exact volume
    at which evaporating a fixed n first saturates.
5.  PhET's two colour interpolations (the Concentration screen's three-stop scheme and the
    Beer's Law screen's linear ramp), including Color.interpolateRGBA's FLOOR.
6.  The true transmitted colour: XYZ over the CIE 1931 2-degree observer on the SAME 1 nm
    grid the spectra live on, adapted so the illuminant itself renders white, then sRGB.
7.  The literature solubilities and molar masses fetched for the nine solutes, converted to
    molarity, beside PhET's.

Run:  python3 derive.py     (writes refvals.txt; read it in full)
"""
import io
import json
import math
import os
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

HERE = os.path.dirname(os.path.abspath(__file__))
PV = json.load(io.open(os.path.join(HERE, 'phet_values.json'), encoding='utf-8'))
CIE_CSV = os.path.abspath(os.path.join(HERE, '..', 'blackbody-spectrum', 'CIE_xyz_1931_2deg.csv'))

REFS = []
FAILS = []


def ref(label, *vals):
    REFS.append((label, ['%.17g' % v for v in vals]))
    print('%-58s %s' % (label, '  '.join('%.17g' % v for v in vals)))


def check(cond, what):
    if not cond:
        FAILS.append(what)
    print('%-4s %s' % ('ok' if cond else 'FAIL', what))


print('=' * 100)
print('PhET beers-law-lab %s, values read from %s' % (PV['version'], PV['source']))
print('=' * 100)

# ===================================================================== 1. constants
LAM0, LAM1 = PV['MIN_WAVELENGTH'], PV['MAX_WAVELENGTH']
NLAM = LAM1 - LAM0 + 1
check(NLAM == 401, 'the visible band 380..780 nm is 401 one-nanometre samples')
for k in ('BEAKER_VOLUME', 'CUVETTE_SNAP_DEFAULT', 'DROPPER_FLOW', 'FAUCET_FLOW',
          'EVAPORATION_MAX', 'SHAKER_RATE', 'PARTICLES_PER_MOLE', 'PARTICLE_SIZE',
          'WATER_DENSITY', 'MIN_WAVELENGTH', 'MAX_WAVELENGTH'):
    ref('PHET ' + k, PV[k])
ref('PHET SOLUTE_AMOUNT_RANGE min max default', *PV['SOLUTE_AMOUNT_RANGE'])
ref('PHET SOLUTION_VOLUME_RANGE min max default', *PV['SOLUTION_VOLUME_RANGE'])
ref('PHET CUVETTE_WIDTH_RANGE min max default', *PV['CUVETTE_WIDTH_RANGE'])
ref('PHET decimals conc percent molar A T lambda amount cuvette volume',
    PV['DECIMALS_CONC_MOL_PER_L'], PV['DECIMALS_CONC_PERCENT'], PV['DECIMALS_CONC_MOLAR'],
    PV['DECIMALS_ABSORBANCE'], PV['DECIMALS_TRANSMITTANCE'], PV['DECIMALS_WAVELENGTH'],
    PV['DECIMALS_SOLUTE_AMOUNT'], PV['DECIMALS_CUVETTE_WIDTH'], PV['DECIMALS_VOLUME_LITERS'])
ref('PHET WATER_RGB', *PV['WATER_RGB'])
MOLE_PER_PARTICLE = 1.0 / PV['PARTICLES_PER_MOLE']
ref('PHET mole per shaker particle', MOLE_PER_PARTICLE)

SOL = {d['const']: d for d in PV['solutes']}
BLS = {d['const']: d for d in PV['beersLawSolutions']}
EPS = PV['molarAbsorptivity']
ORDER = [d['const'] for d in PV['solutes']]
BL_ORDER = [d['const'] for d in PV['beersLawSolutions']]

# ===================================================================== 2. Beer-Lambert
print('\n--- Beer-Lambert: A = eps l c, T = 10^-A ---')


def absorbance(eps, l, c):
    return eps * l * c


def transmittance(A):
    return math.pow(10.0, -A)


def absorbance_of_T(T):
    # JavaScript's Math.log10(0) is -Infinity; Python's math.log10(0) raises.  The sims run
    # the JS branch, so the twin spells the same limit out rather than throwing.
    return float('inf') if T <= 0 else -math.log10(T)


def eps_at(const, lam):
    """PhET's rule: the table is indexed by floor(lambda - 380); it is NOT interpolated."""
    i = int(math.floor(lam - LAM0))
    if i < 0 or i >= NLAM:
        return None
    return EPS[const][i]


# 50-digit twin
def absorbance_dec(eps, l, c):
    return Decimal(repr(eps)) * Decimal(repr(l)) * Decimal(repr(c))


def transmittance_dec(A):
    return Decimal(10) ** (-A)


worstA, worstT, worstRT, worstProp, bigA = 0.0, 0.0, 0.0, 0.0, 0.0
for const in BL_ORDER:
    d = BLS[const]
    lam = PV['lambdaMax'][const]
    e = eps_at(const, lam)
    for l in (0.5, 1.0, 1.37, 2.0):
        for f in (0.0, 0.25, 0.5, 1.0):
            c = d['cMax'] * f
            A = absorbance(e, l, c)
            bigA = max(bigA, A)
            Ad = absorbance_dec(e, l, c)
            worstA = max(worstA, abs(Decimal(repr(A)) - Ad) / (Ad if Ad else Decimal(1)))
            T = transmittance(A)
            # 10^-A judged on ITS OWN argument: this measures pow, not the product above
            Tsame = transmittance_dec(Decimal(repr(A)))
            worstT = max(worstT, abs(Decimal(repr(T)) - Tsame) / (Tsame if Tsame else Decimal(1)))
            # and end to end, where the error in A is amplified by |dlnT/dA| = ln 10
            Td = transmittance_dec(Ad)
            worstProp = max(worstProp, abs(Decimal(repr(T)) - Td) / (Td if Td else Decimal(1)))
            if T > 0:
                worstRT = max(worstRT, abs(absorbance_of_T(T) - A) / (A if A else 1.0))
check(float(worstA) < 1e-15, 'A = eps l c matches 50-digit Decimal (worst rel %.3e)' % worstA)
check(float(worstT) < 1e-15,
      'T = 10^-A matches 50-digit Decimal on the same A (worst rel %.3e)' % worstT)
check(worstRT < 1e-14, 'and -log10(T) returns A (worst rel %.3e)' % worstRT)
# the end-to-end figure is LARGER on purpose: a relative error d in A becomes ln10 * A * d in
# T, so asserting the round trip to the same tolerance as the product would be asserting
# something false.  The ratio is the check that the amplification is the expected one.
amp = float(worstProp) / (float(worstA) * math.log(10) * bigA)
check(0.2 < amp < 3.0,
      'the end-to-end error in T is the ln10 * A amplification of the error in A '
      '(measured/predicted = %.2f at A up to %.3f)' % (amp, bigA))
ref('BL roundtrip worst rel A T backA propagated', float(worstA), float(worstT), worstRT,
    float(worstProp))

# the two extremes
check(transmittance(0.0) == 1.0, 'A = 0 gives T = 1 exactly')
check(absorbance_of_T(1.0) == 0.0, 'and T = 1 gives A = 0 exactly')
ref('BL T at A 0 1 2 3 10', transmittance(0.0), transmittance(1.0), transmittance(2.0),
    transmittance(3.0), transmittance(10.0))
# where 10^-A underflows a double: the smallest positive normal is ~2.2e-308, denormals to 4.9e-324
A_ZERO = 1.0
while transmittance(A_ZERO) > 0.0:
    A_ZERO += 1.0
check(transmittance(A_ZERO) == 0.0 and transmittance(A_ZERO - 1.0) > 0.0,
      'T underflows to exactly 0 at A = %g and not before' % A_ZERO)
ref('BL A at which T underflows to zero, and T just below', A_ZERO, transmittance(A_ZERO - 1.0))
check(math.isinf(absorbance_of_T(0.0)), 'and -log10(0) is infinite: a detector reading 0 %T '
                                        'cannot be inverted')
# 2.00 absorbance is 1 % transmittance -- the number every spectrophotometer manual quotes
check(abs(transmittance(2.0) - 0.01) < 1e-17, 'A = 2 is exactly 1 % transmittance')
check(abs(transmittance(1.0) - 0.1) < 1e-17, 'A = 1 is exactly 10 % transmittance')

# the largest absorbance each Beer's Law solution can reach
print('\n--- the eight Beer\'s Law solutions ---')
Amax = []
for const in BL_ORDER:
    d = BLS[const]
    lam = PV['lambdaMax'][const]
    e = eps_at(const, lam)
    A2 = absorbance(e, PV['CUVETTE_WIDTH_RANGE'][1], d['cMax'])
    Amax.append(A2)
    print('  %-24s lambda_max %3d nm  eps %10.2f  cmax %8g M  A(2 cm, cmax) = %.6f  T = %.3e'
          % (const, lam, e, d['cMax'], A2, transmittance(A2)))
    ref('BL %s lambdaMax eps cmax cdefault Amax2cm' % const,
        lam, e, d['cMax'], d['cDefault'], A2)
check(min(Amax) > 3.0 and max(Amax) < 4.1,
      'every solution reaches A between 3 and 4.1 at full scale in a 2 cm cuvette')
ref('BL Amax over the eight, min and max', min(Amax), max(Amax))

# the quantisation rule
const = 'POTASSIUM_PERMANGANATE'
check(eps_at(const, 500.0) == eps_at(const, 500.999),
      'eps(lambda) is a STEP function: 500.0 nm and 500.999 nm read the same table cell')
check(eps_at(const, 500.0) != eps_at(const, 501.0), 'and 501 nm reads the next one')
check(eps_at(const, 379.9) is None and eps_at(const, 781.0) is None,
      'outside 380..781 nm the table index runs off the end and PhET has no data at all')
check(eps_at(const, 780.5) == EPS[const][NLAM - 1],
      'but 780.5 nm still reads the last cell: floor() does not stop at the slider')
ref('EPS quantisation KMnO4 at 500 500.999 501',
    eps_at(const, 500.0), eps_at(const, 500.999), eps_at(const, 501.0))

# lambda_max is the FIRST index of the maximum (PhET scans with a strict >)
for const in BL_ORDER:
    arr = EPS[const]
    mx = max(arr)
    first = arr.index(mx)
    ties = [i for i, v in enumerate(arr) if v == mx]
    check(PV['lambdaMax'][const] == LAM0 + first,
          '%s lambda_max is the first maximum (%d ties)' % (const, len(ties)))
ref('EPS lambdaMax in file order', *[PV['lambdaMax'][k] for k in BL_ORDER])
ref('EPS at lambdaMax in file order', *[max(EPS[k]) for k in BL_ORDER])

# ===================================================================== 3. the beaker
print('\n--- the Concentration screen: the mole ledger ---')
VMIN, VMAX = PV['SOLUTION_VOLUME_RANGE'][0], PV['SOLUTION_VOLUME_RANGE'][1]
NMIN, NMAX = PV['SOLUTE_AMOUNT_RANGE'][0], PV['SOLUTE_AMOUNT_RANGE'][1]


def csat(const):
    return SOL[const]['maxConcentration']


def concentration(n, V, cs):
    return min(cs, n / V) if V > 0 else 0.0


def precipitate(n, V, cs):
    return max(0.0, n - V * cs)


def is_saturated(n, V, cs):
    return V > 0 and n / V > cs


def solute_grams(n, V, cs, M):
    return M * max(0.0, n - precipitate(n, V, cs))


def percent_concentration(g, V, rho):
    return 0.0 if V <= 0 else g / (g + V * rho) * 100.0


class Beaker(object):
    """PhET's ConcentrationModel, at the level of moles and litres.  ZERO is the only
    clamp that loses material, and every add/remove returns the amount that ACTUALLY
    moved, which is what lets the ledger close."""

    def __init__(self, const, n, V, one=1.0, zero=0.0):
        self.const, self.n, self.V = const, n, V
        self.one, self.zero = one, zero
        # the four clamps carry the SAME numeric type as the run, or a float 1.0 arriving
        # from min() at the brim turns an exact rational run into a float one halfway through
        cast = (lambda x: Fraction(repr(x))) if isinstance(one, Fraction) else float
        self.vmin, self.vmax = cast(VMIN), cast(VMAX)
        self.nmin, self.nmax = cast(NMIN), cast(NMAX)
        self.frozen = False
        self.pfrozen = zero
        self.inflight = []                      # shaker particles, each 1/200 mol
        self.led = dict(shaker=zero, dropper=zero, drained=zero, faucet=zero,
                        evaporated=zero, drainedV=zero, dropperV=zero, flying=zero)

    def cs(self):
        return self.one * Fraction(repr(csat(self.const))) if isinstance(self.one, Fraction) \
            else csat(self.const)

    def precip(self):
        if self.frozen:
            return self.pfrozen
        z = self.n - self.V * self.cs()
        return z if z > self.zero else self.zero

    def conc(self):
        if not self.V > self.zero:
            return self.zero
        q = self.n / self.V
        cs = self.cs()
        return cs if q > cs else q

    def add_solvent(self, d):
        if d <= self.zero:
            return self.zero
        v0 = self.V
        self.V = min(self.vmax, self.V + d)
        return self.V - v0

    def remove_solvent(self, d):
        if d <= self.zero:
            return self.zero
        v0 = self.V
        self.V = max(self.vmin, self.V - d)
        return v0 - self.V

    def add_solute(self, d):
        if d <= self.zero:
            return self.zero
        n0 = self.n
        self.n = min(self.nmax, self.n + d)
        return self.n - n0

    def remove_solute(self, d):
        if d <= self.zero:
            return self.zero
        n0 = self.n
        self.n = max(self.nmin, self.n - d)
        return n0 - self.n

    def step(self, dt, faucet, drain, dropper, evap, shaking, rng):
        # 1 faucet
        self.led['faucet'] += self.add_solvent(faucet * dt)
        # 2 drain: removes SOLUTION, so it takes solute at the DISSOLVED concentration
        d = drain * dt
        if d > self.zero:
            c = self.conc()
            got = self.remove_solvent(d)
            self.led['drainedV'] += got
            self.led['drained'] += self.remove_solute(c * got)
        # 3 dropper: stock solution.  PhET freezes the precipitate across the volume add
        d = dropper * dt
        if d > self.zero:
            self.frozen, self.pfrozen = True, self.precip()
            got = self.add_solvent(d)
            self.frozen = False
            self.led['dropperV'] += got
            stock = SOL[self.const]['stock']
            stock = Fraction(repr(stock)) if isinstance(self.one, Fraction) else stock
            self.led['dropper'] += self.add_solute(stock * got)
        # 4 evaporate
        self.led['evaporated'] += self.remove_solvent(evap * dt)
        # 5 the shaker's particles fall, and land
        mp = Fraction(1, PV['PARTICLES_PER_MOLE']) if isinstance(self.one, Fraction) \
            else MOLE_PER_PARTICLE
        still = []
        for p in self.inflight:
            p = p - 1
            if p <= 0:
                self.led['shaker'] += self.add_solute(mp)
            else:
                still.append(p)
        self.inflight = still
        # 6 the shaker creates them
        if shaking:
            rate = PV['SHAKER_RATE']
            k = int(round(max(1.0, rate * PV['PARTICLES_PER_MOLE'] * float(dt))))
            for _ in range(k):
                self.inflight.append(6 + (rng() % 5))
        self.led['flying'] = mp * len(self.inflight)
        return self


def run_script(one, zero, steps=900):
    """One deterministic script through every control PhET's step() touches."""
    F = (lambda x: Fraction(repr(x))) if isinstance(one, Fraction) else (lambda x: float(x))
    b = Beaker('DRINK_MIX', zero, F(0.5) * one, one, zero)
    dt = Fraction(1, 60) if isinstance(one, Fraction) else 1.0 / 60.0
    seed = [12345]

    def rng():
        seed[0] = (seed[0] * 1103515245 + 12345) & 0x7fffffff
        return seed[0] >> 16

    for i in range(steps):
        faucet = F(PV['FAUCET_FLOW']) if 60 <= i < 160 else zero
        drain = F(PV['FAUCET_FLOW']) if 500 <= i < 560 else zero
        dropper = F(PV['DROPPER_FLOW']) if 200 <= i < 400 else zero
        evap = F(PV['EVAPORATION_MAX']) if 600 <= i < 690 else zero
        shaking = 700 <= i < 860
        b.step(dt, faucet, drain, dropper, evap, shaking, rng)
    return b


bf = run_script(1.0, 0.0)
bq = run_script(Fraction(1), Fraction(0))

led = bq.led
closes = (bq.n == led['shaker'] + led['dropper'] - led['drained'])
check(closes, 'the mole ledger closes EXACTLY in rationals: '
              'n = shaker + dropper - drained (%s)' % bq.n)
volcloses = (bq.V == Fraction(repr(0.5)) + led['faucet'] + led['dropperV']
             - led['drainedV'] - led['evaporated'])
check(volcloses, 'and the volume ledger: V = 0.5 + faucet + dropper - drain - evaporation')
resid = abs(bf.n - (bf.led['shaker'] + bf.led['dropper'] - bf.led['drained']))
check(resid < 1e-14, 'in doubles it closes to %.3e mol' % resid)
residV = abs(bf.V - (0.5 + bf.led['faucet'] + bf.led['dropperV']
                     - bf.led['drainedV'] - bf.led['evaporated']))
check(residV < 1e-14, 'and the volume to %.3e L' % residV)
drift = max(abs(bf.n - float(bq.n)), abs(bf.V - float(bq.V)))
check(drift < 1e-12, 'the float run tracks the exact one to %.3e over 900 frames' % drift)
ref('LEDGER final n V, exact n V, float residual n V',
    bf.n, bf.V, float(bq.n), float(bq.V), resid, residV)
ref('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',
    bf.led['shaker'], bf.led['dropper'], bf.led['drained'], bf.led['faucet'],
    bf.led['dropperV'], bf.led['drainedV'], bf.led['evaporated'])
print('  final: n = %.17g mol, V = %.17g L, C = %.17g mol/L'
      % (bf.n, bf.V, concentration(bf.n, bf.V, csat('DRINK_MIX'))))

# each shaker particle carries exactly 1/200 mol, so the shaker's total is a multiple of it
k = bq.led['shaker'] / Fraction(1, PV['PARTICLES_PER_MOLE'])
check(k.denominator == 1, 'the shaker total is exactly %s particles of 1/200 mol' % k)
ref('LEDGER shaker particles landed', float(k))

# PhET's shaker makes round(max(1, rate * particlesPerMole * dt)) particles a frame, and
# neither the rounding nor the floor is innocent.  At 60 fps the bracket is 0.6667 and the
# ROUNDING takes it to one grain a frame: 0.30 mol/s against a nominal 0.20.  The floor
# does nothing there -- round(0.6667) is 1 with or without it -- and only starts to bite
# above about 80 frames a second, where it over-delivers further still.  Both are derived
# here rather than asserted, because the first draft of this comment blamed the floor for
# the 60 fps figure and was wrong.
def shaker_per_frame(dt, floor=True):
    x = PV['SHAKER_RATE'] * PV['PARTICLES_PER_MOLE'] * dt
    return int(round(max(1.0, x) if floor else x))


DT = 1.0 / 60.0
bracket = PV['SHAKER_RATE'] * PV['PARTICLES_PER_MOLE'] * DT
per_frame = shaker_per_frame(DT)
delivered = per_frame * MOLE_PER_PARTICLE / DT
check(bracket < 1.0 and per_frame == 1,
      'at 60 fps the bracket is %.6f and one grain a frame comes out of it' % bracket)
check(shaker_per_frame(DT, floor=False) == per_frame,
      'the max(1, ...) floor does NOT do that: rounding 0.667 gives 1 without it')
check(abs(delivered - 0.3) < 1e-12,
      'so the shaker delivers %.4f mol/s at 60 fps, not its nominal %.2f'
      % (delivered, PV['SHAKER_RATE']))
DT120 = 1.0 / 120.0
d120 = shaker_per_frame(DT120) * MOLE_PER_PARTICLE / DT120
check(shaker_per_frame(DT120, floor=False) == 0 and shaker_per_frame(DT120) == 1,
      'above about 80 fps the floor IS what keeps a grain coming: at 120 fps the bracket '
      'rounds to nothing without it')
check(abs(d120 - 0.6) < 1e-12,
      'and the same shaker then delivers %.4f mol/s -- three times its nominal rate' % d120)
check(abs(shaker_per_frame(1.0) * MOLE_PER_PARTICLE / 1.0 - PV['SHAKER_RATE']) < 1e-12,
      'only at a whole-second step, where neither the rounding nor the floor bites, is the '
      'delivered rate the nominal one')
shaken_frames = 860 - 700
check(abs(bf.led['shaker'] - shaken_frames * MOLE_PER_PARTICLE) < 1e-12,
      'and the script\'s %d shaking frames put in exactly %d grains' % (shaken_frames,
                                                                        shaken_frames))
ref('SHAKER bracket perFrame deliveredMolPerS nominal', bracket, per_frame, delivered,
    PV['SHAKER_RATE'])
ref('SHAKER at 120 fps perFrame delivered, and at 1 s',
    shaker_per_frame(DT120), d120, shaker_per_frame(1.0) * MOLE_PER_PARTICLE)

# ---- the drain leaves the precipitate behind ----
print('\n--- saturation ---')
cs = csat('COPPER_SULFATE')
n0, V0 = 2.0, 1.0
check(is_saturated(n0, V0, cs), 'CuSO4 at 2 mol in 1 L is past its 1.38 M saturation')
p0 = precipitate(n0, V0, cs)
c0 = concentration(n0, V0, cs)
check(abs(c0 - cs) < 1e-18, 'so the solution reads exactly Csat')
check(abs(p0 - (n0 - V0 * cs)) < 1e-18, 'and %.17g mol sits on the bottom' % p0)
ref('SAT CuSO4 2mol 1L Csat precip conc', cs, p0, c0)
# draining a saturated beaker removes solute at Csat, not at n/V
b = Beaker('COPPER_SULFATE', n0, V0)
b.step(1.0, 0.0, 0.1, 0.0, 0.0, False, lambda: 0)
check(abs(b.n - (n0 - cs * 0.1)) < 1e-15,
      'draining 0.1 L of a saturated beaker takes Csat*0.1 mol, not (n/V)*0.1')
ref('SAT drained moles at Csat vs naive', n0 - b.n, n0 / V0 * 0.1)
check(n0 - b.n < n0 / V0 * 0.1, 'which is less: the precipitate does not go down the drain')

# ---- evaporation raises the concentration along an exact hyperbola ----
n1, V1 = 0.5, 1.0
csn = csat('NICKEL_II_CHLORIDE')
Vsat = n1 / csn
check(Vsat < V1, 'evaporating 0.5 mol of NiCl2 from 1 L saturates at V = n/Csat')
ref('EVAP NiCl2 n Csat Vsat tsat at 0.25 L/s', n1, csn, Vsat, (V1 - Vsat) / PV['EVAPORATION_MAX'])
worst = 0.0
for j in range(1, 40):
    V = V1 - j * 0.02
    if V <= 0:
        break
    want = min(csn, n1 / V)
    got = concentration(n1, V, csn)
    worst = max(worst, abs(got - want))
check(worst == 0.0, 'C(V) = n/V exactly until it hits Csat, then it is flat')
# the exact curve at four volumes, for the JS to reproduce
ref('EVAP C at V = 1.0 0.5 0.2 0.1 L (n = 0.5 mol NiCl2)',
    concentration(n1, 1.0, csn), concentration(n1, 0.5, csn),
    concentration(n1, 0.2, csn), concentration(n1, 0.1, csn))
# and the precipitate that appears past Vsat
check(precipitate(n1, 0.1, csn) == 0.0 and precipitate(n1, 0.09, csn) > 0.0,
      'nothing precipitates above Vsat = %.6f L and something does below it' % Vsat)
ref('EVAP precipitate at V = 0.09 0.05 0.02 L',
    precipitate(n1, 0.09, csn), precipitate(n1, 0.05, csn), precipitate(n1, 0.02, csn))

# ---- the dropper's mixing law ----
stock = SOL['POTASSIUM_PERMANGANATE']['stock']
b = Beaker('POTASSIUM_PERMANGANATE', 0.0, 0.5)
for _ in range(60):
    b.step(1.0 / 60.0, 0.0, 0.0, PV['DROPPER_FLOW'], 0.0, False, lambda: 0)
dV = PV['DROPPER_FLOW']
# a rate applied 60 times at dt = 1/60 does NOT sum to the rate in binary: the residual
# below is the accumulation, not a model error, and it is pinned rather than hidden
dres = abs(b.V - (0.5 + dV))
check(dres < 2e-14, 'one second of the dropper adds 0.05 L to %.3e (60 roundings)' % dres)
check(abs(b.n - stock * dV) < 2e-14, 'carrying stock * 0.05 mol of solute')
check(abs(b.conc() - stock * dV / (0.5 + dV)) < 2e-14,
      'so the beaker reads c = c_stock dV/(V0+dV) = %.17g mol/L' % b.conc())
ref('DROPPER one-second accumulation residual in V', dres)
ref('DROPPER KMnO4 stock dV n C after 1 s from 0.5 L of water',
    stock, dV, b.n, b.conc())
# filling an EMPTY beaker with stock alone must reach the stock concentration exactly
b = Beaker('POTASSIUM_PERMANGANATE', 0.0, 0.0)
for _ in range(60 * 20):
    b.step(1.0 / 60.0, 0.0, 0.0, PV['DROPPER_FLOW'], 0.0, False, lambda: 0)
check(abs(b.V - 1.0) < 1e-15, 'twenty seconds of the dropper fills the 1 L beaker')
check(abs(b.conc() - stock) < 1e-12,
      'and a beaker of stock alone reads the stock concentration, %.17g' % b.conc())
ref('DROPPER stock-only fill V C', b.V, b.conc())

# ---- grams and mass percent ----
print('\n--- grams, mass percent, and the stock solutions ---')
for const in ORDER:
    d = SOL[const]
    cst = csat(const)
    g = solute_grams(0.5, 0.5, cst, d['molarMass'])
    pc = percent_concentration(g, 0.5, PV['WATER_DENSITY'])
    spc = d['molarMass'] * d['stock'] * 100.0 / (PV['WATER_DENSITY'] + d['molarMass'] * d['stock'])
    ref('MASS %s molarMass stock Csat gramsAt1M percentAt1M stockPercent' % const,
        d['molarMass'], d['stock'], cst, g, pc, spc)
    print('  %-24s M %8.3f  stock %5.2f M (%5.2f mass%%)  Csat %5.2f M' % (const, d['molarMass'],
          d['stock'], spc, cst))
# a 1 molar solution of NaCl in 1 L is 58.443 g in 58.443 + 1000 g of solution
g = solute_grams(1.0, 1.0, csat('SODIUM_CHLORIDE'), SOL['SODIUM_CHLORIDE']['molarMass'])
pc = percent_concentration(g, 1.0, PV['WATER_DENSITY'])
check(abs(pc - 58.443 / (58.443 + 1000.0) * 100.0) < 1e-13,
      '1 M NaCl is %.6f mass %% on PhET\'s definition (solvent mass = V * 1000 g/L)' % pc)
ref('MASS 1M NaCl grams percent', g, pc)
# the precipitate is NOT counted in the grams (PhET's soluteGramsProperty)
g2 = solute_grams(3.0, 1.0, csat('COPPER_SULFATE'), SOL['COPPER_SULFATE']['molarMass'])
check(abs(g2 - csat('COPPER_SULFATE') * SOL['COPPER_SULFATE']['molarMass']) < 1e-12,
      'past saturation only the DISSOLVED solute is weighed (%.4f g of CuSO4)' % g2)
ref('MASS CuSO4 3mol in 1L dissolved grams', g2)

# precipitate particle count: round(200 * moles), floored at one whenever any exists
def particle_count(pm):
    k = int(round(PV['PARTICLES_PER_MOLE'] * pm))
    if k == 0 and pm > 0:
        k = 1
    return k


check(particle_count(0.0) == 0, 'no precipitate, no particles')
check(particle_count(1e-9) == 1, 'a trace of precipitate still draws one particle (PhET)')
check(particle_count(0.5) == 100, 'and half a mole draws 100 of them')
ref('PARTICLES at 0 1e-9 0.0026 0.5 mol',
    particle_count(0.0), particle_count(1e-9), particle_count(0.0026), particle_count(0.5))

# ===================================================================== 5. PhET's colours
print('\n--- PhET\'s two colour interpolations ---')


def lerp_rgb(a, b, t):
    """PhET's Color.interpolateRGBA: linear, then FLOOR (not round) on each channel."""
    return [int(math.floor(a[i] + (b[i] - a[i]) * t)) for i in range(3)]


def scheme_color(const, c):
    """SoluteColorScheme.concentrationToColor, with ConcentrationSolution.createColor's
    c = 0 -> the solvent's own colour in front of it."""
    d = SOL[const]
    if c <= 0:
        return list(PV['WATER_RGB'])
    if c >= d['maxConcentration']:
        return list(d['maxColor'])
    if c <= d['minConcentration']:
        return list(d['minColor'])
    if c <= d['midConcentration']:
        t = (c - d['minConcentration']) / (d['midConcentration'] - d['minConcentration'])
        return lerp_rgb(d['minColor'], d['midColor'], t)
    t = (c - d['midConcentration']) / (d['maxConcentration'] - d['midConcentration'])
    return lerp_rgb(d['midColor'], d['maxColor'], t)


def ramp_color(const, c):
    """BeersLawSolution.fluidColorProperty: water at c = 0, else a straight RGB line from
    colorLo at c = 0+ to colorHi at cMax.  The jump at c = 0 is PhET's, not a bug here."""
    d = BLS[const]
    if not c > 0:
        return list(PV['WATER_RGB'])
    t = (c - d['cMin']) / (d['cMax'] - d['cMin'])
    return lerp_rgb(d['colorLo'], d['colorHi'], min(1.0, max(0.0, t)))


check(scheme_color('DRINK_MIX', 0.0) == PV['WATER_RGB'], 'an empty solution is water-coloured')
check(scheme_color('DRINK_MIX', 5.96) == [255, 0, 0], 'and saturated drink mix is pure red')
half = lerp_rgb([224, 255, 255], [255, 225, 225], 0.5)
check(half == [239, 240, 240],
      'interpolateRGBA FLOORS: halfway from (224,255,255) to (255,225,225) is %s' % half)
ref('COLOR floor midpoint water to drinkmix mid', *half)
for const in ORDER:
    d = SOL[const]
    cs = [0.0, d['midConcentration'] / 2, d['midConcentration'],
          (d['midConcentration'] + d['maxConcentration']) / 2, d['maxConcentration']]
    vals = []
    for c in cs:
        vals += scheme_color(const, c)
    ref('SCHEME %s rgb at 0, mid/2, mid, (mid+sat)/2, sat' % const, *vals)
for const in BL_ORDER:
    d = BLS[const]
    vals = []
    for c in (0.0, 1e-12, d['cMax'] / 2, d['cMax']):
        vals += ramp_color(const, c)
    ref('RAMP %s rgb at 0, 0+, cmax/2, cmax' % const, *vals)
j0 = ramp_color('DRINK_MIX', 0.0)
j1 = ramp_color('DRINK_MIX', 1e-12)
check(j0 != j1, 'PhET\'s Beer\'s Law ramp JUMPS at c = 0: %s -> %s' % (j0, j1))
ref('RAMP jump at zero, water then colorLo', j0[0], j0[1], j0[2], j1[0], j1[1], j1[2])

# ===================================================================== 6. the true colour
print('\n--- the transmitted colour, over the CIE 1931 2-degree observer ---')
rows = [r.split(',') for r in io.open(CIE_CSV, encoding='utf-8').read().splitlines() if r.strip()]
CIE = {}
for r in rows:
    CIE[int(r[0])] = (float(r[1]), float(r[2]), float(r[3]))
XB = [CIE[LAM0 + i][0] for i in range(NLAM)]
YB = [CIE[LAM0 + i][1] for i in range(NLAM)]
ZB = [CIE[LAM0 + i][2] for i in range(NLAM)]
check(len(XB) == NLAM, 'the CIE table covers the same 1 nm grid the spectra do')
ref('CIE first row 380 xbar ybar zbar', XB[0], YB[0], ZB[0])
ref('CIE last row 780 xbar ybar zbar', XB[-1], YB[-1], ZB[-1])
ref('CIE sums over 380..780 x y z', sum(XB), sum(YB), sum(ZB))
# y-bar peaks at 555 nm by construction (V(lambda) = 1 there)
check(YB.index(max(YB)) == 555 - LAM0 and abs(max(YB) - 1.0) < 1e-12,
      'y-bar peaks at exactly 1 at 555 nm, as the CIE defines it')

C2_A = 1.435e-2        # m K, the 1931 second radiation constant the CIE's illuminant A uses
T_A = 2848.0


def illum(kind, lam):
    if kind == 'E':
        return 1.0
    # CIE standard illuminant A, from the CIE's own defining formula
    return 100.0 * (560.0 / lam) ** 5 * (
        math.exp(C2_A * 1e9 / (T_A * 560.0)) - 1.0) / (math.exp(C2_A * 1e9 / (T_A * lam)) - 1.0)


check(abs(illum('A', 560.0) - 100.0) < 1e-10, 'illuminant A is normalised to 100 at 560 nm')
ref('ILLUM A at 380 480 560 660 780',
    illum('A', 380), illum('A', 480), illum('A', 560), illum('A', 660), illum('A', 780))

SRGB_M = ((3.2406, -1.5372, -0.4986),
          (-0.9689, 1.8758, 0.0415),
          (0.0557, -0.2040, 1.0570))


def srgb_gamma(u):
    u = min(1.0, max(0.0, u))
    return 12.92 * u if u <= 0.0031308 else 1.055 * u ** (1.0 / 2.4) - 0.055


def xyz_to_lin(X, Y, Z):
    return [SRGB_M[i][0] * X + SRGB_M[i][1] * Y + SRGB_M[i][2] * Z for i in range(3)]


def transmitted(const, l, c, kind='E'):
    """XYZ of the illuminant seen through the cuvette, and of the illuminant alone.
    One-nanometre sum over 380..780: the SAME grid the spectra are tabulated on, so there
    is no interpolation and no resampling anywhere in this integral."""
    arr = EPS[const]
    X = Y = Z = Xw = Yw = Zw = 0.0
    for i in range(NLAM):
        lam = LAM0 + i
        S = illum(kind, lam)
        T = math.pow(10.0, -arr[i] * l * c)
        X += S * T * XB[i]
        Y += S * T * YB[i]
        Z += S * T * ZB[i]
        Xw += S * XB[i]
        Yw += S * YB[i]
        Zw += S * ZB[i]
    return (X, Y, Z), (Xw, Yw, Zw)


def true_rgb(const, l, c, kind='E'):
    """Adapted so the illuminant itself renders exactly white: each LINEAR sRGB channel is
    divided by the same channel for the illuminant alone (a von Kries adaptation carried
    out in the display's own primaries).  No white-point constant is needed, and pure
    water comes out at exactly rgb(255,255,255)."""
    xyz, w = transmitted(const, l, c, kind)
    lin = xyz_to_lin(*xyz)
    linw = xyz_to_lin(*w)
    v = [max(0.0, lin[i] / linw[i]) for i in range(3)]
    return [int(round(255 * srgb_gamma(u))) for u in v], xyz[1] / w[1]


ref('SRGB gamma at 0.001 0.0031308 0.5 1', srgb_gamma(0.001), srgb_gamma(0.0031308),
    srgb_gamma(0.5), srgb_gamma(1.0))
check(abs(srgb_gamma(0.002) - 12.92 * 0.002) < 1e-15,
      'below 0.0031308 the transfer curve is the linear segment 12.92u')
check(srgb_gamma(-1.0) == 0.0 and abs(srgb_gamma(2.0) - 1.0) < 1e-15,
      'and it clamps out-of-range input, which is the only clamp on that path '
      '(1.055 - 0.055 is 1 - 1.1e-16 in a double, not 1)')

w0, _ = true_rgb('DRINK_MIX', 1.0, 0.0)
check(w0 == [255, 255, 255], 'with no solute the cuvette renders exactly white %s' % w0)
wA, _ = true_rgb('DRINK_MIX', 1.0, 0.0, 'A')
check(wA == [255, 255, 255], 'and so it does under illuminant A: the adaptation is exact')
print('  solution                 c            l     true sRGB        Y/Yw     PhET ramp')
_tr, _pr = {}, {}
for const in BL_ORDER:
    d = BLS[const]
    for f in (0.25, 1.0):
        c = d['cMax'] * f
        rgb, yy = true_rgb(const, 1.0, c)
        pr = ramp_color(const, c)
        print('  %-24s %-11.5g  1 cm  %-16s %.5f  %s' % (const, c, rgb, yy, pr))
        _tr.setdefault(const, []).extend([rgb[0], rgb[1], rgb[2], yy])
        _pr.setdefault(const, []).extend([pr[0], pr[1], pr[2]])

for const in BL_ORDER:
    ref('TRUE %s rgb and Y at cmax/4 and cmax, l = 1 cm' % const, *_tr[const])
    ref('PHETRAMP %s rgb at cmax/4 and cmax' % const, *_pr[const])

# the beam's own colour: a monochromatic stimulus through the same observer, normalised
# to its brightest channel and faded by the eye's response.  Display only -- and pinned,
# because a display-only helper gets no scrutiny from a physics suite by construction
# (Known-bad, standard_candle: a wavelength helper fed the wrong unit painted the whole
# optical band red and looked deliberate).
def wave_rgb(lam):
    i = int(round(lam)) - LAM0
    if i < 0 or i >= NLAM:
        return [0, 0, 0]
    v = xyz_to_lin(XB[i], YB[i], ZB[i])
    lo = min(v)
    if lo < 0:
        v = [u - lo for u in v]
    m = max(v)
    if not (m > 0):
        return [0, 0, 0]
    k = math.sqrt(min(1.0, 4 * YB[i]))
    return [int(round(255 * srgb_gamma(u / m * k))) for u in v]


WAVES = (420, 480, 555, 620, 700)
_wv = []
for lam in WAVES:
    _wv += wave_rgb(lam)
    print('  wave %d nm -> %s' % (lam, wave_rgb(lam)))
ref('WAVE rgb at 420 480 555 620 700', *_wv)
check(max(wave_rgb(555)) == 255, 'the beam at 555 nm is at full brightness')
check(max(wave_rgb(420)) < 120, 'and at 420 nm it is dim, because the eye barely sees it')
check(wave_rgb(300) == [0, 0, 0] and wave_rgb(900) == [0, 0, 0],
      'outside the band there is no beam colour at all')

# the conventional bound past which a real solution stops obeying Beer-Lambert.  It is a
# teaching number, not a measurement, and the file says so wherever it appears.
LINEAR_LIMIT = 0.01
ref('LINEAR LIMIT mol per L', LINEAR_LIMIT)
check(sum(1 for d in BLS.values() if d['cMax'] > LINEAR_LIMIT) == 5,
      'five of the eight Beer\'s Law ranges run past 10 mM')

# the detector's gate: PhET's beam is 0.45 cm across and its sensor 1 cm, so the sensor
# spans the beam while |y| + 0.225 < 0.5
BEAM_HALF, SENSOR_HALF = 0.225, 0.5
ref('DETECTOR beamHalf sensorHalf cutoff', BEAM_HALF, SENSOR_HALF, SENSOR_HALF - BEAM_HALF)
check(0.25 + BEAM_HALF < SENSOR_HALF and 0.30 + BEAM_HALF > SENSOR_HALF,
      'so 0.25 cm off the axis is still in the beam and 0.30 cm is not')

# the physical claim the analysis view makes: the true colour DARKENS, PhET's ramp does not
def rel_lum(rgb):
    """relative luminance of an sRGB triple (IEC 61966-2-1 inverse transfer + the Y row)"""
    def inv(u):
        u /= 255.0
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    return 0.2126 * inv(rgb[0]) + 0.7152 * inv(rgb[1]) + 0.0722 * inv(rgb[2])


const = 'POTASSIUM_PERMANGANATE'
d = BLS[const]
lo_t, lo_y = true_rgb(const, 1.0, d['cMax'] * 0.1)
hi_t, hi_y = true_rgb(const, 1.0, d['cMax'])
lo_p, hi_p = ramp_color(const, d['cMax'] * 0.1), ramp_color(const, d['cMax'])
tr = lo_y / hi_y
pr_ = rel_lum(lo_p) / rel_lum(hi_p)
check(tr > 3.0, 'ten times the KMnO4 darkens the true colour %.2f-fold in luminance' % tr)
check(tr > pr_, 'which is more than PhET\'s ramp darkens (%.2f-fold) -- but only by %.2f, so '
                'luminance is NOT where the two part company' % (pr_, tr / pr_))
ref('DARKEN KMnO4 trueY ratio, phet ramp lum ratio, Y at cmax/10 and cmax',
    tr, pr_, lo_y, hi_y)
# where they DO part company, unambiguously: PhET's ramp is a function of concentration
# alone, so a four-times longer cuvette leaves it untouched, while Beer-Lambert makes the
# transmitted light 10^(-3A) of what it was.
c_mid = d['cMax'] * 0.5
t_thin, y_thin = true_rgb(const, 0.5, c_mid)
t_thick, y_thick = true_rgb(const, 2.0, c_mid)
check(ramp_color(const, c_mid) == ramp_color(const, c_mid),
      'PhET\'s ramp has no path length in it at all')
check(t_thin != t_thick,
      'while a 0.5 cm and a 2 cm cuvette of the same solution look different: %s against %s'
      % (t_thin, t_thick))
# and the size of that difference is the second lesson: BROADBAND luminance does not obey
# Beer-Lambert, because the integral is carried by the shoulders where eps is small.
e_max = eps_at(const, PV['lambdaMax'][const])
mono = math.pow(10.0, -e_max * 2.0 * c_mid) / math.pow(10.0, -e_max * 0.5 * c_mid)
check(y_thick / y_thin > 4.0 * mono,
      'the monochromatic beam at lambda_max is cut to %.4f over that change of path while '
      'the luminance keeps %.4f -- %.1f times as much: an integral over a band is not a '
      'single exponential' % (mono, y_thick / y_thin, (y_thick / y_thin) / mono))
ref('PATHLEN KMnO4 cmax/2 rgb at 0.5 cm and 2 cm, Y each, mono ratio at lambdaMax',
    t_thin[0], t_thin[1], t_thin[2], t_thick[0], t_thick[1], t_thick[2], y_thin, y_thick, mono)

# how far the two disagree, as the largest single-channel gap over each ramp
print('  worst channel gap between PhET\'s ramp and the true colour, over c in [0, cmax]:')
gaps = []
for const in BL_ORDER:
    d = BLS[const]
    worst, wc = 0, 0.0
    for j in range(1, 51):
        c = d['cMax'] * j / 50.0
        t, _y = true_rgb(const, 1.0, c)
        p = ramp_color(const, c)
        g = max(abs(t[i] - p[i]) for i in range(3))
        if g > worst:
            worst, wc = g, c
    gaps.append(worst)
    print('    %-24s %3d of 255 at c = %.6g M' % (const, worst, wc))
    ref('GAP %s worst channel, at c' % const, worst, wc)
check(min(gaps) > 20, 'PhET\'s ramp is nowhere within 20/255 of the true colour '
                      '(smallest worst gap %d)' % min(gaps))
ref('GAP smallest and largest worst-channel gap', min(gaps), max(gaps))

# a five-millimetre path through a SATURATED beaker is essentially opaque
const = 'POTASSIUM_PERMANGANATE'
rgb, yy = true_rgb(const, 0.5, csat(const))
check(yy < 1e-8, 'half a centimetre of saturated KMnO4 transmits %.3e of the light, which '
                 'is black on any display' % yy)
check(rgb == [0, 0, 0], 'and renders as exactly rgb(0,0,0)')
ref('OPAQUE KMnO4 saturated 0.5 cm Y rgb', yy, rgb[0], rgb[1], rgb[2])

# ===================================================================== 7. the literature
print('\n--- PhET\'s data against the literature (Wikipedia chemical infoboxes, fetched) ---')
LIT = {
    # const: (molar mass g/mol, solubility value, unit, temperature text, molarity)
    'DRINK_MIX': (342.297, 2.01, 'g/mL', '20 C', 'sucrose'),
    'COBALT_II_NITRATE': (182.943, 84.03, 'g/100 mL', '0 C', 'anhydrous'),
    'COBALT_CHLORIDE': (129.839, 52.9, 'g/100 mL', '20 C', 'anhydrous'),
    'POTASSIUM_DICHROMATE': (294.182, 15.1, 'g/100 g', 'no temperature given', ''),
    'POTASSIUM_CHROMATE': (194.189, 65.0, 'g/100 mL', 'no temperature given', ''),
    'NICKEL_II_CHLORIDE': (129.5994, 67.5, 'g/100 mL', '25 C', 'anhydrous'),
    'COPPER_SULFATE': (159.60, 201.0, 'g/L', '20 C', 'anhydrous'),
    'POTASSIUM_PERMANGANATE': (158.032, 76.0, 'g/L', '25 C', ''),
    'SODIUM_CHLORIDE': (58.44, 360.0, 'g/L', '25 C', ''),
}
UNIT_TO_GPL = {'g/mL': 1000.0, 'g/100 mL': 10.0, 'g/100 g': 10.0, 'g/L': 1.0}
print('  %-24s %-10s %-10s  %-9s %-9s  %s' % ('solute', 'M PhET', 'M lit', 'Csat PhET',
                                              'Csat lit', 'rel'))
worstM, worstC = 0.0, 0.0
for const in ORDER:
    M_lit, val, unit, temp, note = LIT[const]
    gpl = val * UNIT_TO_GPL[unit]
    c_lit = gpl / M_lit
    c_phet = csat(const)
    dM = abs(SOL[const]['molarMass'] - M_lit) / M_lit
    dC = abs(c_phet - c_lit) / c_lit
    worstM = max(worstM, dM)
    worstC = max(worstC, dC)
    print('  %-24s %-10.4f %-10.4f  %-9.3f %-9.3f  %.1f %%   (%s %s, %s)'
          % (const, SOL[const]['molarMass'], M_lit, c_phet, c_lit, 100 * dC, val, unit, temp))
    ref('LIT %s molarMassLit gPerL cLit relC' % const, M_lit, gpl, c_lit, dC)
check(worstM < 2e-4, 'every molar mass matches the literature to %.1e relative' % worstM)
check(worstC < 0.30, 'and every saturation to %.1f %%, the worst being the two whose only '
                     'quoted temperature is not 25 C' % (100 * worstC))
ref('LIT worst molar-mass and saturation relative gaps', worstM, worstC)
# the ones that land dead on
for const in ('POTASSIUM_CHROMATE', 'POTASSIUM_PERMANGANATE', 'NICKEL_II_CHLORIDE',
              'POTASSIUM_DICHROMATE'):
    M_lit, val, unit, temp, note = LIT[const]
    c_lit = val * UNIT_TO_GPL[unit] / M_lit
    check(abs(csat(const) - c_lit) / c_lit < 0.01,
          '%s saturation is within 1 %% of the literature (%.4f vs %.4f M)'
          % (const, csat(const), c_lit))

# drink mix IS sucrose, by its molar mass
check(abs(SOL['DRINK_MIX']['molarMass'] - 342.297) <= 1.01e-3,
      'PhET\'s "drink mix" has sucrose\'s molar mass to 1 mg/mol (342.296 vs 342.297): it is '
      'modelled as sugar')

# ===================================================================== write refvals
out = io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8')
for label, vals in REFS:
    out.write(label + '\t' + '\t'.join(vals) + '\n')
out.close()
print('\n%d reference lines -> refvals.txt' % len(REFS))
if FAILS:
    print('\n%d CHECK(S) FAILED:' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all checks passed')
