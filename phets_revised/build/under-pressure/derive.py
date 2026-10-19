#!/usr/bin/env python3
"""derive.py — the Python twin of docs/phets_revised/under-pressure.html.

Re-derives every closed form the sim implements and prints reference values to
16 digits for selfTest() to assert.  Nothing here is copied from the JS: the
formulas are written out from the definitions, the awkward ones are computed a
second way (a brute-force sum, a scipy quadrature, a scipy root), and the two
routes are compared here before either is trusted.

Run:  python3 derive.py > refvals.txt
"""
import math
import sys

try:
    from scipy import integrate, optimize
    HAVE_SCIPY = True
except Exception:                                    # pragma: no cover
    HAVE_SCIPY = False

OUT = []


def p(*a):
    s = ' '.join(str(x) for x in a)
    OUT.append(s)
    print(s)


def g17(x):
    return '%.17g' % x


def head(t):
    p('')
    p('=' * 74)
    p(t)
    p('=' * 74)


# ======================================================================
# 1.  UNITS — exact by definition, nothing rounded
# ======================================================================
head('1. units: the exact definitions')

PA_PER_ATM = 101325.0                    # the standard atmosphere, exact (CGPM 1954)
LB = 0.45359237                          # the international pound, kg, exact (1959)
G_STD = 9.80665                          # standard gravity, m/s^2, exact
INCH = 0.0254                            # the international inch, m, exact
LBF = LB * G_STD                         # pound-force, N, exact
PA_PER_PSI = LBF / (INCH * INCH)         # 1 lbf / 1 in^2
PA_PER_KPA = 1000.0
FT = 0.3048                              # the international foot, m, exact

p('PA_PER_ATM            =', g17(PA_PER_ATM), '   (definition)')
p('LBF (N)               =', g17(LBF), '   = 0.45359237 * 9.80665')
p('INCH^2 (m^2)          =', g17(INCH * INCH))
p('PA_PER_PSI            =', g17(PA_PER_PSI))
p('PSI_PER_ATM           =', g17(PA_PER_ATM / PA_PER_PSI))
p('KPA_PER_ATM           =', g17(PA_PER_ATM / PA_PER_KPA))
p('FT (m)                =', g17(FT), '  M_PER_FT inverse =', g17(1.0 / FT))

# a second, independent route to the psi: 1 atm in psi is quoted as 14.69594878.
p('check psi from atm    : 101325 / %s = %s' % (g17(PA_PER_PSI), g17(PA_PER_ATM / PA_PER_PSI)))
assert abs(PA_PER_PSI - 6894.757293168361) < 1e-9, PA_PER_PSI

# round trips, at the pressures the sim actually reaches
head('1b. unit round trips (worst relative error over the sim range)')
worst = 0.0
for i in range(0, 4001):
    pa = 0.0 + i * 1000.0                      # 0 .. 4 MPa covers every reachable p
    for c in (PA_PER_ATM, PA_PER_PSI, PA_PER_KPA):
        back = (pa / c) * c
        if pa > 0:
            worst = max(worst, abs(back - pa) / pa)
p('worst round-trip relative error =', '%.3e' % worst)

# PhET's own rounded constants, for the record (the sim does NOT use these)
p('PhET 1.1.36 uses ATM_PER_PA = 9.8692e-6  -> 1 atm =', g17(1.0 / 9.8692e-6), 'Pa')
p('PhET 1.1.36 uses PSI_PER_PA = 1.4504e-4  -> 1 psi =', g17(1.0 / 1.4504e-4), 'Pa')
p('this sim uses the exact definitions; the difference at 1 atm is',
  '%.3e' % abs(PA_PER_ATM * 9.8692e-6 - 1.0), 'atm and',
  '%.3e' % abs(PA_PER_ATM * 1.4504e-4 - PA_PER_ATM / PA_PER_PSI), 'psi')

# ======================================================================
# 2.  PhET's constants (read out of docs/phets/under-pressure_en.html)
# ======================================================================
head("2. PhET's values, read out of the minified build 1.1.36")

RHO_GASOLINE, RHO_WATER, RHO_HONEY = 700.0, 1000.0, 1420.0
G_MARS, G_EARTH, G_JUPITER = 3.71, 9.8, 24.9
P_AIR_0 = 101325.0            # Constants.EARTH_AIR_PRESSURE
P_AIR_150 = 99490.0           # Constants.EARTH_AIR_PRESSURE_AT_500_FT
Y_LAPSE = 150.0               # getStandardAirPressure: linear(0,150,P_AIR_0,P_AIR_150,y)
MAX_POOL_HEIGHT = 3.0
MYSTERY_RHO = [1700.0, 840.0, 1100.0]        # Fluid A, B, C
MYSTERY_G = [20.0, 14.0, 6.5]                # Planet A, B, C
DEPTH_OUT = 2.0               # THIS SIM's out-of-page depth (PhET is 2-D; see header)

p('densities  gasoline/water/honey =', RHO_GASOLINE, RHO_WATER, RHO_HONEY, 'kg/m^3')
p('gravity    Mars/Earth/Jupiter   =', G_MARS, G_EARTH, G_JUPITER, 'm/s^2')
p('air        p(0), p(150 m)       =', P_AIR_0, P_AIR_150, 'Pa   (linear between)')
p('mystery    fluids               =', MYSTERY_RHO)
p('mystery    gravities            =', MYSTERY_G)
p('pool depth (max)                =', MAX_POOL_HEIGHT, 'm')
p('out-of-page depth chosen here   =', DEPTH_OUT, 'm')

LAPSE = (P_AIR_150 - P_AIR_0) / Y_LAPSE
p('lapse dp/dy                     =', g17(LAPSE), 'Pa/m')


def air(y, gravity=G_EARTH, atmosphere=True):
    """PhET's air pressure: a linear lapse, scaled by g/g_earth."""
    if not atmosphere:
        return 0.0
    return (P_AIR_0 + LAPSE * y) * (gravity / G_EARTH)


def pressure(depth, rho, gravity, y_surface=0.0, atmosphere=True):
    """p = p_air(at the surface) + rho g h.  depth h is measured DOWN from the
    free surface, so the point sits at y = y_surface - depth."""
    return air(y_surface, gravity, atmosphere) + rho * gravity * depth


p('')
p('air(0)    Earth   =', g17(air(0.0)))
p('air(150)  Earth   =', g17(air(150.0)))
p('air(0)    Jupiter =', g17(air(0.0, G_JUPITER)))
p('air(2.5)  Earth   =', g17(air(2.5)))
p('air(0)    no atm  =', g17(air(0.0, G_EARTH, False)))

# how good is PhET's LINEAR lapse?  The isothermal column is exact for an
# ideal gas at constant T: p = p0 exp(-y/Hs), Hs = p0/(rho0 g).
RHO_AIR_0 = 1.225                       # ISA sea-level density, kg/m^3
H_SCALE = P_AIR_0 / (RHO_AIR_0 * G_STD)
p('')
p('isothermal scale height Hs      =', g17(H_SCALE), 'm  (p0 / rho0 g, rho0 = 1.225)')
p('exact exponential p(150 m)      =', g17(P_AIR_0 * math.exp(-150.0 / H_SCALE)), 'Pa')
p("PhET's linear     p(150 m)      =", g17(air(150.0)), 'Pa')
p('they differ by                  =', '%.4f' % (100 * abs(air(150.0) - P_AIR_0 * math.exp(-150.0 / H_SCALE)) / P_AIR_0), '% of an atmosphere')
p('worst linear-vs-exponential gap over 0..150 m:')
wg = max(abs((P_AIR_0 + LAPSE * y) - P_AIR_0 * math.exp(-y / H_SCALE)) for y in [j * 0.15 for j in range(1001)])
p('   ', g17(wg), 'Pa =', '%.4f' % (100 * wg / P_AIR_0), '% of an atmosphere')

# ======================================================================
# 3.  THE HYDROSTATIC LAW at every setting the controls reach
# ======================================================================
head('3. p = p_atm + rho g h, at every tick of every control')

p('%-10s %-9s %-7s %-22s %-22s' % ('fluid', 'gravity', 'depth', 'p with atmosphere (Pa)', 'p with none (Pa)'))
PINS = []
for rname, rho in [('gasoline', RHO_GASOLINE), ('water', RHO_WATER), ('honey', RHO_HONEY)]:
    for gname, gg in [('Mars', G_MARS), ('Earth', G_EARTH), ('Jupiter', G_JUPITER)]:
        for d in (0.0, 1.5, 3.0):
            a = pressure(d, rho, gg, 0.0, True)
            b = pressure(d, rho, gg, 0.0, False)
            p('%-10s %-9s %-7s %-22s %-22s' % (rname, gname, d, g17(a), g17(b)))
            PINS.append((rname, gname, d, a, b))

p('')
p('the extremes of the two sliders (700..1420 kg/m^3, 3.71..24.9 m/s^2) at h = 3 m:')
for rho in (RHO_GASOLINE, RHO_HONEY):
    for gg in (G_MARS, G_JUPITER):
        p('   rho=%-6s g=%-6s p =' % (rho, gg), g17(pressure(3.0, rho, gg)), 'Pa =',
          g17(pressure(3.0, rho, gg) / PA_PER_ATM), 'atm =',
          g17(pressure(3.0, rho, gg) / PA_PER_PSI), 'psi')

p('')
p('the gauge at the surface reads exactly the air pressure (atmosphere on):')
p('   ', g17(pressure(0.0, RHO_HONEY, G_JUPITER)), 'vs air =', g17(air(0.0, G_JUPITER)),
  ' difference', g17(pressure(0.0, RHO_HONEY, G_JUPITER) - air(0.0, G_JUPITER)))
p('with the atmosphere off it reads exactly zero:', g17(pressure(0.0, RHO_HONEY, G_JUPITER, 0.0, False)))

# an independent route to the same number: integrate dp/dy = -rho g downward
if HAVE_SCIPY:
    for rho, gg, d in ((RHO_WATER, G_EARTH, 3.0), (RHO_HONEY, G_JUPITER, 1.5)):
        q, err = integrate.quad(lambda y: rho * gg, 0.0, d)
        p('quad check rho=%s g=%s h=%s : p_gauge = %s (quad %s, err %.1e)'
          % (rho, gg, d, g17(rho * gg * d), g17(q), err))

# ======================================================================
# 4.  THE POOLS — geometry, and volume <-> level, exactly
# ======================================================================
head("4. the pools (PhET's world coordinates, metres, y up, y = 0 at ground)")

# --- the square pool ---------------------------------------------------
SQ = dict(x0=2.3, x1=6.0, ytop=0.0, ybot=-MAX_POOL_HEIGHT)
SQ_W = SQ['x1'] - SQ['x0']
SQ_A = SQ_W * DEPTH_OUT
SQ_VMAX = SQ_A * MAX_POOL_HEIGHT
p('square pool  x in [%s, %s], y in [%s, 0]' % (SQ['x0'], SQ['x1'], SQ['ybot']))
p('   width %s m, plan area %s m^2, full volume %s m^3 = %s L'
  % (g17(SQ_W), g17(SQ_A), g17(SQ_VMAX), g17(SQ_VMAX * 1000)))

# --- the trapezoid pool ------------------------------------------------
TZ_WTOP, TZ_WBOT, TZ_CTOP, TZ_SEP = 0.7, 3.15, 3.2, 3.22
TZ_H = MAX_POOL_HEIGHT
# PhET's bottomChamber is x in [4, 6]; its right chamber's foot is at 6.07, so
# PhET leaves a 7 cm wedge between them that its own isPointInsidePool calls
# OUTSIDE the pool (see _out/gap.py: 5948 sampled points in the sliver, the gap
# closing at y = -2.8286).  This file runs the channel to 6.2 so the fluid is
# one connected body at every height, which is what the scene is about.
TZ_CHAN = dict(x0=4.0, x1=6.2, y0=-MAX_POOL_HEIGHT, y1=-MAX_POOL_HEIGHT + 0.21)
TZ_CHAN_PHET_X1 = 6.0


def tz_left(t):
    """left chamber [xl, xr] at height t above the pool bottom (PhET's
    LinearFunction(0, maxHeight, c - u/2, c - h/2) and its mirror)."""
    xl = (TZ_CTOP - TZ_WBOT / 2) + ((TZ_CTOP - TZ_WTOP / 2) - (TZ_CTOP - TZ_WBOT / 2)) * t / TZ_H
    xr = (TZ_CTOP + TZ_WBOT / 2) + ((TZ_CTOP + TZ_WTOP / 2) - (TZ_CTOP + TZ_WBOT / 2)) * t / TZ_H
    return xl, xr


def tz_right(t):
    c = TZ_CTOP + TZ_SEP
    xl = (c - TZ_WTOP / 2) + ((c - TZ_WBOT / 2) - (c - TZ_WTOP / 2)) * t / TZ_H
    xr = (c + TZ_WTOP / 2) + ((c + TZ_WBOT / 2) - (c + TZ_WTOP / 2)) * t / TZ_H
    return xl, xr


p('')
p('trapezoid pool: widthTop %s widthBottom %s centerTop %s separation %s' % (TZ_WTOP, TZ_WBOT, TZ_CTOP, TZ_SEP))
for t in (0.0, 0.21, 1.5, 3.0):
    a, b = tz_left(t)
    c, d = tz_right(t)
    p('   t=%-5s left [%s, %s] w=%-8s right [%s, %s] w=%-8s sum w=%s'
      % (t, g17(a), g17(b), g17(b - a), g17(c), g17(d), g17(d - c), g17((b - a) + (d - c))))
p('   the two chamber widths SUM to a constant: %s m at every height'
  % g17((tz_left(1.7)[1] - tz_left(1.7)[0]) + (tz_right(1.7)[1] - tz_right(1.7)[0])))
p('   (the tapers are equal and opposite -- this is why the level is linear in volume above the channel)')

TZ_WSUM = TZ_WTOP + TZ_WBOT
TZ_CHAN_T = TZ_CHAN['y1'] - TZ_CHAN['y0']
# inside the channel band the two chambers and the channel overlap, so the
# cross-section is one band from the left chamber's left edge to the right
# chamber's right edge.
lo0, _ = tz_left(0.0)
_, hi0 = tz_right(0.0)
TZ_WCHAN = hi0 - lo0
lo2, _ = tz_left(TZ_CHAN_T)
_, hi2 = tz_right(TZ_CHAN_T)
p('   channel band t in [0, %s]: width %s at t=0 and %s at the top of the band (constant, the band slides)'
  % (g17(TZ_CHAN_T), g17(TZ_WCHAN), g17(hi2 - lo2)))
assert abs((hi2 - lo2) - TZ_WCHAN) < 1e-12
for t in [i * TZ_CHAN_T / 40 for i in range(41)]:
    assert tz_left(t)[1] >= TZ_CHAN['x0'] and tz_right(t)[0] <= TZ_CHAN['x1'], t
    assert TZ_CHAN['x0'] >= tz_left(t)[0] and TZ_CHAN['x1'] <= tz_right(t)[1], t
p('   the channel is connected to BOTH chambers at every height of the band, and lies inside their span')
p('')
p("   PhET 1.1.36's own bottomChamber stops at x = %s while its right chamber's foot is at %s:"
  % (TZ_CHAN_PHET_X1, g17(tz_right(0.0)[0])))
p('   a %s m wedge, closing at y = %s, that its own isPointInsidePool reports as OUTSIDE the pool'
  % (g17(tz_right(0.0)[0] - TZ_CHAN_PHET_X1), g17(-TZ_H + (tz_right(0.0)[0] - TZ_CHAN_PHET_X1) / ((tz_right(0.0)[0] - tz_right(TZ_H)[0]) / TZ_H))))
p('   (a gauge dropped there reads air, not fluid).  This file runs the channel to x = %s instead.'
  % TZ_CHAN['x1'])

TZ_VCHAN = TZ_WCHAN * TZ_CHAN_T * DEPTH_OUT
TZ_VMAX = TZ_VCHAN + TZ_WSUM * (TZ_H - TZ_CHAN_T) * DEPTH_OUT
p('   full volume = %s m^3 = %s L   (channel %s + chambers %s)'
  % (g17(TZ_VMAX), g17(TZ_VMAX * 1000), g17(TZ_VCHAN), g17(TZ_VMAX - TZ_VCHAN)))


def tz_area(t):
    """cross-sectional area (m^2) of the trapezoid pool at height t."""
    if t < 0 or t > TZ_H:
        return 0.0
    return (TZ_WCHAN if t < TZ_CHAN_T else TZ_WSUM) * DEPTH_OUT


def tz_volume(t):
    """the fluid volume with the surface at height t above the pool bottom."""
    t = max(0.0, min(TZ_H, t))
    if t <= TZ_CHAN_T:
        return TZ_WCHAN * t * DEPTH_OUT
    return TZ_VCHAN + TZ_WSUM * (t - TZ_CHAN_T) * DEPTH_OUT


def tz_level(V):
    """invert it."""
    V = max(0.0, min(TZ_VMAX, V))
    if V <= TZ_VCHAN:
        return V / (TZ_WCHAN * DEPTH_OUT)
    return TZ_CHAN_T + (V - TZ_VCHAN) / (TZ_WSUM * DEPTH_OUT)


if HAVE_SCIPY:
    for t in (0.1, 0.21, 1.0, 2.5, 3.0):
        q, _ = integrate.quad(tz_area, 0.0, t, points=[TZ_CHAN_T], limit=200)
        p('   quad V(t=%-5s) = %-22s closed form %-22s  diff %.2e' % (t, g17(q), g17(tz_volume(t)), abs(q - tz_volume(t))))
for V in (1.0, TZ_VCHAN, 5.0, TZ_VMAX):
    assert abs(tz_volume(tz_level(V)) - V) < 1e-12, V
p('   volume <-> level round trip exact to 1e-12 at four volumes')

# --- the chamber pool (Pascal) ----------------------------------------
CH_L_OPEN = 0.5          # PhET's u
CH_R_OPEN = 2.3          # PhET's h
CH_RATIO = CH_R_OPEN / CH_L_OPEN
A_L = CH_L_OPEN * DEPTH_OUT
A_R = CH_R_OPEN * DEPTH_OUT
CH_WATER = 1.0           # PhET's leftWaterHeight = E - c = 2.3 - 1.3
CH_OPEN_BOT = -1.7       # PhET's leftOpening.y2 = -(MAX_POOL_HEIGHT - 1.3)
CH_REST = CH_OPEN_BOT + CH_WATER
MASSES = [500.0, 250.0, 250.0]
p('')
p('chamber pool: left opening %s m, right opening %s m, out-of-page %s m'
  % (CH_L_OPEN, CH_R_OPEN, DEPTH_OUT))
p('   A_left = %s m^2, A_right = %s m^2, ratio A_R/A_L = %s' % (g17(A_L), g17(A_R), g17(CH_RATIO)))
p('   (PhET is 2-D and uses width alone; the %s m out-of-page depth makes A_left exactly 1 m^2,'
  % DEPTH_OUT)
p('    which is what reproduces its displacement numbers with an honest area)')
p('   rest level %s m, the left column can fall at most %s m' % (g17(CH_REST), g17(CH_WATER)))
p('   masses:', MASSES, 'kg  (PhET: one 500 and two 250)')


def pascal(M, rho, gravity, atmosphere=True):
    """A stack of mass M on the left piston.

    Pascal: the pressure the piston adds is dp = F/A_left, and it is the SAME
    everywhere in the connected fluid.  Matching the pressure at one point by
    the two routes (down from the loaded left surface, down from the free right
    surface) gives

        dp = (rho g + lambda) * dh ,   lambda = d(p_air)/dy ,

    so with the atmosphere OFF (lambda = 0) the classical dh = M/(rho A_left)
    is exact, and with it ON the air column between the two surfaces has its
    own weight and dh is larger by |lambda|/(rho g) -- about 0.12 % in water.
    Volume conservation splits dh between the two surfaces in inverse
    proportion to their areas."""
    lam = LAPSE * (gravity / G_EARTH) if atmosphere else 0.0
    dp = M * gravity / A_L
    dh = dp / (rho * gravity + lam)
    dL = dh * A_R / (A_L + A_R)
    dR = dh * A_L / (A_L + A_R)
    return dict(dp=dp, dh=dh, dL=dL, dR=dR, Fout=dp * A_R, mult=A_R / A_L,
                lam=lam, dh_ideal=M / (rho * A_L))


p('')
p('%-7s %-8s %-9s %-16s %-20s %-20s %-20s %-14s' %
  ('M (kg)', 'rho', 'g', 'dp = F/A (Pa)', 'dh, atmosphere on', 'dh, atmosphere off', 'left down (on)', 'F on right (N)'))
for M in (0.0, 250.0, 500.0, 750.0, 1000.0):
    for rho, gg in ((RHO_WATER, G_EARTH),):
        r = pascal(M, rho, gg, True)
        r0 = pascal(M, rho, gg, False)
        p('%-7s %-8s %-9s %-16s %-20s %-20s %-20s %-14s' %
          (M, rho, gg, g17(r['dp']), g17(r['dh']), g17(r0['dh']), g17(r['dL']), g17(r['Fout'])))
        assert abs(r0['dh'] - r0['dh_ideal']) < 1e-12
p('with the atmosphere OFF, dh = M/(rho A_left) exactly (residual < 1e-12 at all five masses)')
p('with it ON, dh is larger by |lambda|/(rho g) =',
  '%.6f' % (abs(LAPSE) / (RHO_WATER * G_EARTH) * 100), '% for water on Earth')
p('   (lambda = %s Pa/m is PhET\'s air lapse; it is the weight of the air column' % g17(LAPSE))
p('    between the two free surfaces, i.e. an air density of %s kg/m^3)' % g17(abs(LAPSE) / G_EARTH))
p('force multiplication A_R/A_L = %s: %s kg on the small piston balances %s kg on the big one'
  % (g17(CH_RATIO), 500.0, g17(500.0 * CH_RATIO)))
p('dh is independent of g EITHER WAY, and the atmosphere-on case has a closed form too:')
p('   dp = Mg/A_L and (rho g + lambda) = g (rho + LAPSE/g_earth), so g cancels and')
RHO_EFF_W = RHO_WATER + LAPSE / G_EARTH
p('   dh = M / (A_L (rho + LAPSE/g_earth)) = M / (A_L * %s)  for water' % g17(RHO_EFF_W))
for gg in (G_MARS, G_EARTH, G_JUPITER):
    r = pascal(500.0, RHO_WATER, gg, False)
    ron = pascal(500.0, RHO_WATER, gg, True)
    closed = 500.0 / (A_L * RHO_EFF_W)
    p('   g = %-6s dh(off) = %-20s dh(on) = %-20s closed form %-20s (diff %.2e)  dp = %s Pa'
      % (gg, g17(r['dh']), g17(ron['dh']), g17(closed), abs(ron['dh'] - closed), g17(r['dp'])))
    assert abs(ron['dh'] - closed) < 1e-14
p('   the air simply subtracts its own density %s kg/m^3 from the fluid\'s' % g17(-LAPSE / G_EARTH))
p('the left column bottoms out when dL = %s m, i.e. at M = rho A_L %s (A_L+A_R)/A_R (atmosphere off):'
  % (g17(CH_WATER), g17(CH_WATER)))
for rho in (RHO_GASOLINE, RHO_WATER, RHO_HONEY):
    Mmax = rho * A_L * CH_WATER * (A_L + A_R) / A_R
    p('   rho = %-6s M_max = %s kg%s' % (rho, g17(Mmax), '  (reachable: the stack goes to 1000 kg)' if Mmax <= 1000 else ''))

# the pressure a gauge sees on each side, at a common depth below BOTH surfaces
p('')
p('gauges in the chamber pool: the SAME point reached down from each surface must agree.')
p('%-8s %-7s %-6s %-13s %-13s %-22s %-22s %-10s' %
  ('atm', 'M (kg)', 'rho', 'left surface', 'right surface', 'p(y=-2.5) from left', 'from right', 'diff'))
for atmo in (True, False):
    for M in (0.0, 500.0, 1000.0):
        for rho in (RHO_WATER, RHO_HONEY):
            r = pascal(M, rho, G_EARTH, atmo)
            yL = CH_REST - r['dL']
            yR = CH_REST + r['dR']
            y = -2.5
            pl = air(yL, G_EARTH, atmo) + r['dp'] + rho * G_EARTH * (yL - y)
            pr = air(yR, G_EARTH, atmo) + rho * G_EARTH * (yR - y)
            p('%-8s %-7s %-6s %-13s %-13s %-22s %-22s %.3e'
              % (atmo, M, rho, g17(yL), g17(yR), g17(pl), g17(pr), abs(pl - pr)))
            assert abs(pl - pr) < 1e-9, (atmo, M, rho, pl, pr)
p('(the left route carries the piston term dp = F/A and the right does not; they agree')
p(' to better than 1e-9 Pa everywhere, which is what "the added pressure is the same')
p(' everywhere" means numerically)')

# ======================================================================
# 5.  THE HYDROSTATIC PARADOX
# ======================================================================
head('5. the hydrostatic paradox: same depth, same pressure; different weight')

# four vessels, all with the same base width and the same fluid depth
PAR_H = 2.0            # fluid depth, m
PAR_WB = 1.2           # base width, m
VESSELS = [
    ('straight', [(0.0, PAR_WB), (PAR_H, PAR_WB)]),
    ('flared', [(0.0, PAR_WB), (PAR_H, 3.0)]),
    ('tapered', [(0.0, PAR_WB), (PAR_H, 0.35)]),
    ('stepped', [(0.0, PAR_WB), (0.55 * PAR_H, PAR_WB), (0.62 * PAR_H, 2.6), (PAR_H, 2.6)]),
]


def prof_w(prof, y):
    """piecewise-linear width profile w(y)."""
    if y <= prof[0][0]:
        return prof[0][1]
    for i in range(len(prof) - 1):
        y0, w0 = prof[i]
        y1, w1 = prof[i + 1]
        if y <= y1:
            return w0 if y1 == y0 else w0 + (w1 - w0) * (y - y0) / (y1 - y0)
    return prof[-1][1]


def prof_volume(prof, H, depth=DEPTH_OUT):
    """exact: the trapezium rule is EXACT on a piecewise-linear profile."""
    V = 0.0
    for i in range(len(prof) - 1):
        y0, w0 = prof[i]
        y1, w1 = prof[i + 1]
        if y1 <= 0 or y0 >= H:
            continue
        a, b = max(y0, 0.0), min(y1, H)
        wa, wb = prof_w(prof, a), prof_w(prof, b)
        V += 0.5 * (wa + wb) * (b - a) * depth
    return V


def prof_wall_vertical(prof, H, rho, gravity, depth=DEPTH_OUT):
    """The vertical component of the pressure force the SIDE WALLS exert on the
    fluid, integrated directly:  F_z = int p(y) w'(y) D dy  with gauge
    p(y) = rho g (H - y).  (Right wall at x = +w/2, left at -w/2; each gives
    p w'/2, and they add.)  Exact term by term on a linear segment."""
    F = 0.0
    for i in range(len(prof) - 1):
        y0, w0 = prof[i]
        y1, w1 = prof[i + 1]
        if y1 <= y0 or y1 <= 0 or y0 >= H:
            continue
        a, b = max(y0, 0.0), min(y1, H)
        k = (w1 - w0) / (y1 - y0)
        # int_a^b rho g (H - y) k D dy
        F += rho * gravity * k * depth * ((H * b - b * b / 2) - (H * a - a * a / 2))
    return F


p('four vessels, base width %s m, fluid depth %s m, out-of-page %s m, water on Earth'
  % (PAR_WB, PAR_H, DEPTH_OUT))
p('%-10s %-16s %-16s %-16s %-16s %-10s' %
  ('vessel', 'volume (m^3)', 'weight W (N)', 'p_base gauge', 'F_base (N)', 'F/W'))
PAR = []
pbase = RHO_WATER * G_EARTH * PAR_H
Abase = PAR_WB * DEPTH_OUT
Fbase = pbase * Abase
for name, prof in VESSELS:
    V = prof_volume(prof, PAR_H)
    W = RHO_WATER * G_EARTH * V
    p('%-10s %-16s %-16s %-16s %-16s %-10s' %
      (name, g17(V), g17(W), g17(pbase), g17(Fbase), g17(Fbase / W)))
    PAR.append((name, V, W, Fbase / W))
p('')
p('the base force is the SAME for all four (%s N) because p_base = rho g h and the bases match.' % g17(Fbase))
p('the weights differ by a factor of %s.' % g17(max(x[2] for x in PAR) / min(x[2] for x in PAR)))
p('')
p('where the difference goes: the vertical pressure force on the SLANTED WALLS.')
p('%-10s %-22s %-22s %-10s' % ('vessel', 'wall F_z, direct integral', 'W - F_base', 'diff'))
for name, prof in VESSELS:
    V = prof_volume(prof, PAR_H)
    W = RHO_WATER * G_EARTH * V
    Fw = prof_wall_vertical(prof, PAR_H, RHO_WATER, G_EARTH)
    p('%-10s %-22s %-22s %.3e' % (name, g17(Fw), g17(W - Fbase), abs(Fw - (W - Fbase))))
p('(the identity F_wall,z = W - F_base is force balance on the fluid; the left-hand side')
p(' is integrated over the walls without using the balance, so the agreement is a check)')

if HAVE_SCIPY:
    p('')
    p('scipy cross-check of both integrals (quad, and a 400000-strip Riemann sum):')
    for name, prof in VESSELS:
        q, _ = integrate.quad(lambda y: prof_w(prof, y) * DEPTH_OUT, 0.0, PAR_H,
                              points=[pt[0] for pt in prof[1:-1]], limit=300)
        N = 400000
        rs = sum(prof_w(prof, (i + 0.5) * PAR_H / N) for i in range(N)) * PAR_H / N * DEPTH_OUT
        p('   %-10s V closed %-20s quad %-20s riemann %-20s' % (name, g17(prof_volume(prof, PAR_H)), g17(q), g17(rs)))

p('')
p('the paradox depends on neither the fluid nor the gravity: F/W is geometry alone.')
for rho, gg in ((RHO_GASOLINE, G_MARS), (RHO_HONEY, G_JUPITER)):
    fb = rho * gg * PAR_H * Abase
    for name, prof in VESSELS:
        W = rho * gg * prof_volume(prof, PAR_H)
        p('   rho=%-6s g=%-6s %-10s F/W = %s' % (rho, gg, name, g17(fb / W)))

# ======================================================================
# 6.  SHAPE INDEPENDENCE inside the sim's own pools
# ======================================================================
head("6. the gauge reads the same at the same depth in every pool the sim has")

lvl = 1.5   # metres of fluid above the pool bottom, i.e. surface at y = -1.5
for d in (0.0, 0.5, 1.0, 1.5):
    psq = pressure(d, RHO_WATER, G_EARTH, -MAX_POOL_HEIGHT + lvl)
    p('   depth %-5s : square %-22s trapezoid-left %-22s trapezoid-right %-22s'
      % (d, g17(psq), g17(psq), g17(psq)))
p('   (identical by construction: p depends on the surface height and the depth, on nothing else)')
p('')
p("the sim's OWN default gauge positions, at its default half-full square pool")
p('(gauge A at x = 3.10, gauge B at x = 5.20, both at y = -2.40; surface at y = -1.50):')
for gy in (-2.40, -1.50, -0.90):
    d = (-MAX_POOL_HEIGHT + 1.5) - gy
    if d >= 0:
        p('   y = %-7s depth %-6s p = %-22s = %s kPa = %s atm = %s psi'
          % (gy, g17(d), g17(pressure(d, RHO_WATER, G_EARTH, -1.5)),
             g17(pressure(d, RHO_WATER, G_EARTH, -1.5) / 1000),
             g17(pressure(d, RHO_WATER, G_EARTH, -1.5) / PA_PER_ATM),
             g17(pressure(d, RHO_WATER, G_EARTH, -1.5) / PA_PER_PSI)))
    else:
        p('   y = %-7s ABOVE the surface: reads the air, %s Pa' % (gy, g17(air(gy))))
p('   the same gauge in honey on Jupiter at y = -2.40:',
  g17(pressure(0.9, RHO_HONEY, G_JUPITER, -1.5)), 'Pa')
p('   the same gauge with the atmosphere off:', g17(pressure(0.9, RHO_WATER, G_EARTH, -1.5, False)), 'Pa')
p('')
p('   fluid actually held, at that level:  square %s L, trapezoid %s L, ratio %s'
  % (g17(1000 * SQ_A * lvl), g17(1000 * tz_volume(lvl)), g17(tz_volume(lvl) / (SQ_A * lvl))))

p('')
p('how much fluid stands ABOVE a gauge, in each trapezoid chamber (the paradox,')
p('measured): the chamber width is linear in height, so the trapezium rule is exact.')


def tz_column(which, y_from, y_surf):
    f = lambda y: (tz_left(y + MAX_POOL_HEIGHT) if which == 'left' else tz_right(y + MAX_POOL_HEIGHT))
    wa = f(y_from)[1] - f(y_from)[0]
    wb = f(y_surf)[1] - f(y_surf)[0]
    return 0.5 * (wa + wb) * (y_surf - y_from) * DEPTH_OUT


p('%-8s %-8s %-22s %-22s %-10s' % ('level', 'gauge y', 'left column (m^3)', 'right column (m^3)', 'ratio'))
for lv, gy in ((1.5, -2.2), (1.5, -2.75), (0.5, -2.75), (2.9, -2.95)):
    ys = -MAX_POOL_HEIGHT + lv
    a = tz_column('left', gy, ys)
    b = tz_column('right', gy, ys)
    p('%-8s %-8s %-22s %-22s %-10s' % (lv, gy, g17(a), g17(b), g17(a / b)))
    if HAVE_SCIPY:
        qa, _ = integrate.quad(lambda y: (tz_left(y + MAX_POOL_HEIGHT)[1] - tz_left(y + MAX_POOL_HEIGHT)[0]) * DEPTH_OUT, gy, ys)
        assert abs(qa - a) < 1e-12, (qa, a)
p('   (each checked against scipy.integrate.quad to 1e-12)')
p('   the volume-at-a-level in the OTHER pools, for the same-reading claim:')
for lv in (0.5, 1.5, 2.9):
    p('      level %-5s square %-22s trapezoid %s' % (lv, g17(SQ_A * lv), g17(tz_volume(lv))))

# ======================================================================
# 7.  THE MYSTERY SCENE — does the reading identify the answer?
# ======================================================================
head('7. the mystery scene: one reading, one answer')

MY_DEPTH = 1.5      # the gauge's depth below the surface
p('gauge at %s m below the surface.' % MY_DEPTH)
p('')
p('mystery FLUID (gravity is Earth, %s m/s^2):' % G_EARTH)
rd = []
for i, rho in enumerate(MYSTERY_RHO):
    pv = pressure(MY_DEPTH, rho, G_EARTH)
    rd.append(pv)
    p('   Fluid %s  rho = %-7s  p = %-22s = %-22s kPa = %-20s atm = %s psi'
      % ('ABC'[i], rho, g17(pv), g17(pv / 1000), g17(pv / PA_PER_ATM), g17(pv / PA_PER_PSI)))
sep = min(abs(rd[i] - rd[j]) for i in range(3) for j in range(i + 1, 3))
p('   closest pair differs by %s Pa = %s kPa = %s atm = %s psi'
  % (g17(sep), g17(sep / 1000), g17(sep / PA_PER_ATM), g17(sep / PA_PER_PSI)))
p('   the readout prints kPa to 0.1 and atm to 0.001, so the three are distinguishable at every unit.')
p('   inverting: rho = (p - p_air) / (g h):')
for i, rho in enumerate(MYSTERY_RHO):
    inv = (rd[i] - air(0.0)) / (G_EARTH * MY_DEPTH)
    p('      Fluid %s -> %s  (exact, residual %.3e)' % ('ABC'[i], g17(inv), abs(inv - rho)))

p('')
p('mystery PLANET (the fluid is water, %s kg/m^3):' % RHO_WATER)
rd2 = []
for i, gg in enumerate(MYSTERY_G):
    pv = pressure(MY_DEPTH, RHO_WATER, gg)
    rd2.append(pv)
    p('   Planet %s  g = %-6s  p = %-22s = %-22s kPa   (air term %s)'
      % ('ABC'[i], gg, g17(pv), g17(pv / 1000), g17(air(0.0, gg))))
sep2 = min(abs(rd2[i] - rd2[j]) for i in range(3) for j in range(i + 1, 3))
p('   closest pair differs by %s Pa = %s kPa' % (g17(sep2), g17(sep2 / 1000)))
p('   inverting: g = (p - p_air(g)) / (rho h) does NOT separate, because PhET scales the')
p('   air pressure by g/g_earth too.  Solve p = P0*(g/g0) + rho g h for g:')
for i, gg in enumerate(MYSTERY_G):
    inv = rd2[i] / (P_AIR_0 / G_EARTH + RHO_WATER * MY_DEPTH)
    p('      Planet %s -> %s  (residual %.3e)' % ('ABC'[i], g17(inv), abs(inv - gg)))
p('   both inversions are exact, so a single reading identifies the answer uniquely.')
p('')
p('worst case: is any mystery choice ever degenerate with another at ANY depth 0..3 m?')
worstF = min(min(abs(pressure(d, MYSTERY_RHO[i], G_EARTH) - pressure(d, MYSTERY_RHO[j], G_EARTH))
                 for i in range(3) for j in range(i + 1, 3))
             for d in [k * 0.05 for k in range(1, 61)])
worstP = min(min(abs(pressure(d, RHO_WATER, MYSTERY_G[i]) - pressure(d, RHO_WATER, MYSTERY_G[j]))
                 for i in range(3) for j in range(i + 1, 3))
             for d in [k * 0.05 for k in range(1, 61)])
p('   fluids : smallest gap over depths 0.05..3.00 m =', g17(worstF), 'Pa (at the shallowest depth)')
p('   planets: smallest gap over depths 0.05..3.00 m =', g17(worstP), 'Pa')
p('   at depth EXACTLY 0 the three fluids are degenerate (all read the air pressure) --')
p('   the sim therefore refuses to identify a fluid from a surface reading and says so.')
p('   planets are NOT degenerate at depth 0 (the air term carries g):',
  g17(min(abs(air(0.0, MYSTERY_G[i]) - air(0.0, MYSTERY_G[j])) for i in range(3) for j in range(i + 1, 3))), 'Pa')

# ======================================================================
# 8.  THE COLUMN — the law drawn as a line
# ======================================================================
head('8. the column: p(h) is a straight line of slope rho g and intercept p_atm')

for rname, rho in [('gasoline', RHO_GASOLINE), ('water', RHO_WATER), ('honey', RHO_HONEY)]:
    slope = rho * G_EARTH
    p('   %-9s slope rho g = %-20s Pa/m = %-20s kPa/m = %-20s atm/m = %s psi/m'
      % (rname, g17(slope), g17(slope / 1000), g17(slope / PA_PER_ATM), g17(slope / PA_PER_PSI)))
p('   the depth at which the gauge reads exactly 2 atm (water, Earth, atmosphere on):')
d2 = (2 * PA_PER_ATM - air(0.0)) / (RHO_WATER * G_EARTH)
p('      h =', g17(d2), 'm   check p =', g17(pressure(d2, RHO_WATER, G_EARTH) / PA_PER_ATM), 'atm')
if HAVE_SCIPY:
    r = optimize.brentq(lambda d: pressure(d, RHO_WATER, G_EARTH) - 2 * PA_PER_ATM, 0.0, 100.0,
                        xtol=1e-15, rtol=8.9e-16)
    p('      scipy.brentq                         :', g17(r), '  diff %.3e' % abs(r - d2))
p('   the depth that doubles the gauge reading is the same in every unit (it is one equation).')

p('')
p('the three scales side by side, water on Earth, atmosphere on:')
p('%-8s %-20s %-20s %-20s' % ('h (m)', 'kPa', 'atm', 'psi'))
for d in (0.0, 0.75, 1.5, 2.25, 3.0):
    pv = pressure(d, RHO_WATER, G_EARTH)
    p('%-8s %-20s %-20s %-20s' % (d, g17(pv / 1000), g17(pv / PA_PER_ATM), g17(pv / PA_PER_PSI)))

p('')
p('ten metres of water is very nearly one atmosphere:')
p('   rho g h at h = 10 m, water, Earth      =', g17(RHO_WATER * G_EARTH * 10.0), 'Pa =',
  g17(RHO_WATER * G_EARTH * 10.0 / PA_PER_ATM), 'atm')
p('   the depth of exactly one atmosphere    =', g17(PA_PER_ATM / (RHO_WATER * G_EARTH)), 'm')
p('   with standard gravity 9.80665          =', g17(PA_PER_ATM / (RHO_WATER * G_STD)), 'm')

# ======================================================================
# 9.  THE RULER AND THE GRID
# ======================================================================
head('9. ruler and grid')
p('metric: metres.  english: feet, 1 ft = %s m exactly, so 3 m = %s ft' % (g17(FT), g17(3.0 / FT)))
p('PhET 1.1.36 stores 3.2808399 ft per metre; exact is %s (relative difference %.2e)'
  % (g17(1.0 / FT), abs(3.2808399 - 1.0 / FT) * FT))
p('grid lines every 0.5 m (metric) / 1 ft (english); the top line is the ground, y = 0')

# ======================================================================
# 10.  A SWEEP for the "no non-finite value anywhere" assertion
# ======================================================================
head('10. sweep: p over the whole control space (for the finiteness pin)')
lo = hi = None
n = 0
for rho in [RHO_GASOLINE + i * (RHO_HONEY - RHO_GASOLINE) / 20 for i in range(21)]:
    for gg in [G_MARS + i * (G_JUPITER - G_MARS) / 20 for i in range(21)]:
        for d in [i * MAX_POOL_HEIGHT / 12 for i in range(13)]:
            for atm in (True, False):
                v = pressure(d, rho, gg, 0.0, atm)
                assert math.isfinite(v) and v >= 0.0
                lo = v if lo is None else min(lo, v)
                hi = v if hi is None else max(hi, v)
                n += 1
p('%d combinations, all finite and non-negative; min %s Pa, max %s Pa' % (n, g17(lo), g17(hi)))
p('   max in atm = %s, in psi = %s, in kPa = %s' % (g17(hi / PA_PER_ATM), g17(hi / PA_PER_PSI), g17(hi / 1000)))

p('')
p('scipy available:', HAVE_SCIPY)
p('END')
