#!/usr/bin/env python3
"""derive.py — the Python twin of the density / buoyancy-basics engine.

Re-derives every closed form the two remakes implement and prints reference
values to 12+ significant figures for selfTest to assert.  Nothing here is
copied from the sims: each quantity is computed independently (closed form AND
a brute-force route) so that an assertion against it is a verification rather
than a self-consistency check.

    python3 derive.py > refvals.txt

Sections
  1  the pool, and the free-surface solve (bisection on a monotone G)
  2  Archimedes on a cube: draft, submerged volume, apparent weight, contact
  3  the awkward cases: denser-than-the-fluid, exactly neutral, wider than the pool
  4  the hydrostatic pressure integral on the faces (the force, from where it comes)
  5  PhET's data: materials, screens, block sets, mystery sets
  6  identifiability of the mystery blocks from the numbers the sim prints
"""
import math

try:
    from scipy.optimize import brentq
    HAVE_SCIPY = True
except Exception:                                    # pragma: no cover
    HAVE_SCIPY = False

P = print


def f(x, n=12):
    return ('%.' + str(n) + 'g') % x


# ---------------------------------------------------------------- 1. the pool
# PhET's pool: Bounds3(-0.45, -0.15/0.9/0.4, -0.2, 0.45, 0, 0.2) — read from
# docs/phets/buoyancy-basics_en.html (DensityBuoyancyModel).  y = 0 is ground
# level, the floor is at -POOL_H.
POOL_W = 0.9                     # m, x
POOL_D = 0.4                     # m, z (front to back)
POOL_H = 0.15 / 0.9 / 0.4        # m, PhET's own expression
A_POOL = POOL_W * POOL_D         # m^2, the plan area
V_POOL = A_POOL * POOL_H         # m^3
VF0 = 0.1                        # m^3, PhET's DESIRED_STARTING_POOL_VOLUME
G = 9.8                          # m/s^2, PhET's gEarth (real standard gravity 9.80665)
LITERS = 1000.0                  # litres in a cubic metre

# the pool scale (buoyancy-basics): SCALE_WIDTH 0.15, SCALE_HEIGHT 0.06, depth 0.2
SCALE_W, SCALE_H, SCALE_D = 0.15, 0.06, 0.2
SCALE_V = SCALE_W * SCALE_H * SCALE_D            # 0.0018 m^3 = 1.8 L (PhET's own number)


def clamp(x, lo, hi):
    return lo if x < lo else (hi if x > hi else x)


def side(V):
    """a cube of volume V (PhET: Cube.boundsFromVolume)"""
    return V ** (1.0 / 3.0)


def cube_below(V, yb, yw):
    """the volume of a cube of volume V, bottom at yb, that lies below yw.

    Saturates at V EXACTLY rather than at s^3: s = V^(1/3) is inexact in
    binary, so s*s*s misses V by an ulp and a "fully submerged" fraction comes
    out 1.0000000000000004.
    """
    s = side(V)
    if yw >= yb + s:
        return V
    if yw <= yb:
        return 0.0
    return s * s * (yw - yb)


def block_state(b, yw, rhoF):
    """(V_sub, y_bottom, mode) of one block at a trial free surface yw.

    held   — the user holds it, bottom pinned
    float  — rho_b < rho_f AND the floating draft clears its support
    rest   — sitting on its support (the pool floor, or the pool scale)
    out    — not in the pool at all
    """
    s = side(b['V'])
    if not b.get('inPool', True):
        return 0.0, b.get('yb', 0.0), 'out'
    sup = b.get('support', -POOL_H)
    if b.get('held') is not None:
        yb = max(b['held'], sup)
        return cube_below(b['V'], yb, yw), yb, 'held'
    if b['rho'] < rhoF:
        d = s * b['rho'] / rhoF                       # the floating draft
        yb = yw - d
        if yb >= sup:
            return b['V'] * b['rho'] / rhoF, yb, 'float'
    return cube_below(b['V'], sup, yw), sup, 'rest'


def obstacle_volume(obs, yw):
    """solid furniture in the pool (the pool scale) below yw"""
    tot = 0.0
    for o in obs:
        tot += o['a'] * clamp(yw - o['y0'], 0.0, o['h'])
    return tot


def net_fluid(yw, blocks, obs, rhoF):
    """G(yw) = (pool volume below yw) - (everything solid below yw).

    Non-decreasing in yw whenever the blocked plan area stays below A_POOL.
    """
    tot = A_POOL * max(0.0, yw + POOL_H)
    for b in blocks:
        tot -= block_state(b, yw, rhoF)[0]
    return tot - obstacle_volume(obs, yw)


def pool_level(blocks, obs, rhoF, Vf=VF0, nit=80):
    """the SMALLEST yw with G(yw) >= Vf.

    The infimum matters: a body that spans the whole pool cross-section makes G
    flat, and the fluid surface is then at the bottom of the flat stretch, with
    any surplus above the body's top.
    """
    lo = -POOL_H
    hi = -POOL_H + (Vf + sum(b['V'] for b in blocks) + obstacle_volume(obs, 1e9)) / A_POOL + 1.0
    for _ in range(nit):
        mid = 0.5 * (lo + hi)
        if net_fluid(mid, blocks, obs, rhoF) < Vf:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve(blocks, rhoF, obs=(), Vf=VF0):
    """the whole configuration: the level, then each block's state and forces"""
    obs = list(obs)
    yw = pool_level(blocks, obs, rhoF, Vf)
    out = {'yw': yw, 'blocks': []}
    for b in blocks:
        Vsub, yb, mode = block_state(b, yw, rhoF)
        m = b['rho'] * b['V']
        W = m * G
        Fb = rhoF * G * Vsub
        N = max(0.0, W - Fb) if mode in ('rest',) else 0.0
        hand = (W - Fb) if mode == 'held' else 0.0
        out['blocks'].append({'V': b['V'], 'rho': b['rho'], 's': side(b['V']), 'm': m,
                              'Vsub': Vsub, 'yb': yb, 'mode': mode, 'W': W, 'Fb': Fb,
                              'N': N, 'hand': hand, 'frac': Vsub / b['V']})
    return out


# ------------------------------------------- 2. Archimedes on a cube, closed form
def draft_closed(V, rho, rhoF):
    """a floating cube sinks to d = s rho_b / rho_f  (V_sub = (rho_b/rho_f) V)"""
    return side(V) * rho / rhoF


def submerged_fraction(rho, rhoF):
    return min(1.0, rho / rhoF)


def apparent_weight(V, rho, rhoF, Vsub=None):
    """what a spring scale reads: W - rho_f g V_sub"""
    if Vsub is None:
        Vsub = V
    return rho * V * G - rhoF * G * Vsub


def level_rise_floating(m, rhoF):
    """a FLOATING body raises the level by its own mass / (rho_f A_pool), exactly"""
    return m / (rhoF * A_POOL)


def level_rise_sunk(V):
    """a fully submerged body raises it by its own volume / A_pool, exactly"""
    return V / A_POOL


# ------------------------------------------------------- 4. the pressure integral
def cube_pressure_force(V, yb, yw, rhoF, nsub=4000):
    """the hydrostatic pressure on the six faces of an axis-aligned cube.

    Brute force: p = rho g (yw - y) on every submerged face element, the
    outward normal times the area.  The four side faces must cancel exactly in
    x and z; the top and bottom faces give the net lift.  Gauge pressure (PhET
    ignores air buoyancy - "vacuum assumption" in its model.md).
    """
    s = side(V)
    yt = yb + s
    Fy = 0.0
    Fx = 0.0
    # bottom face (outward normal -y): pushes UP
    if yb < yw:
        Fy += rhoF * G * (yw - yb) * s * s
    # top face (outward normal +y): pushes DOWN
    if yt < yw:
        Fy -= rhoF * G * (yw - yt) * s * s
    # one side face (outward normal +x): pushes in -x
    for k in range(nsub):
        y = yb + s * (k + 0.5) / nsub
        if y < yw:
            Fx -= rhoF * G * (yw - y) * s * (s / nsub)
    return Fx, Fy


def edge_integral_2d(poly, yw, rhoF):
    """the house buoyancy.html per-edge closed form, per unit depth.

    p is linear along a straight edge, so the edge force is p(mid) L exactly;
    the outward normal of a CCW edge (dx, dy) is (dy, -dx)/L and the fluid
    pushes inward, F = -p n L.  Returns (Fx, Fy).
    """
    n = len(poly)
    fx = fy = 0.0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        p = rhoF * G * (yw - 0.5 * (a[1] + b[1]))
        fx += -p * dy
        fy += p * dx
    return fx, fy


def clip_below(poly, w):
    """Sutherland-Hodgman against y <= w"""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ain, bin_ = a[1] <= w, b[1] <= w
        if ain:
            out.append((a[0], a[1]))
        if ain != bin_:
            t = (w - a[1]) / (b[1] - a[1])
            out.append((a[0] + (b[0] - a[0]) * t, w))
    return out


def poly_area(poly):
    s = 0.0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        s += a[0] * b[1] - b[0] * a[1]
    return 0.5 * s


# ------------------------------------------------------------------ 5. PhET data
# every density read out of docs/phets/density_en.html (Material.js), kg/m^3
PHET = {
    'aluminum': 2700, 'brick': 2000, 'ice': 919, 'pvc': 1440, 'styrofoam': 150,
    'wood': 400, 'boatHull': 2700, 'concrete': 3150, 'copper': 8960, 'gold': 19320,
    'platinum': 21450, 'pyrite': 5010, 'sand': 1442, 'silver': 10490, 'steel': 7800,
    'tantalum': 16650, 'apple': 832, 'diamond': 3510, 'glass': 2700, 'human': 950,
    'lead': 11342, 'titanium': 4500, 'air': 1.2, 'gasoline': 680, 'honey': 1440,
    'mercury': 13593, 'oil': 920, 'seawater': 1029, 'water': 1000,
}
# Wikipedia "Density" -> "Densities of various materials", fetched 2026-09-21.
# None where that table has no row for the material at all.
WIKI = {
    'aluminum': 2700, 'brick': None, 'ice': 916.7, 'pvc': 1175, 'styrofoam': 75,
    'wood': 700, 'boatHull': 2700, 'concrete': 2400, 'copper': 8940, 'gold': 19320,
    'platinum': 21450, 'pyrite': None, 'sand': 1600, 'silver': 10500, 'steel': 7850,
    'tantalum': 16600, 'apple': None, 'diamond': 3500, 'glass': 2500, 'human': None,
    'lead': 11340, 'titanium': 4540, 'air': 1.2, 'gasoline': None, 'honey': None,
    'mercury': 13546, 'oil': 920, 'seawater': 1030, 'water': 1000,
}

SIMPLE_MASS = ['styrofoam', 'wood', 'ice', 'pvc', 'brick', 'aluminum']
DENSITY_TABLE = ['wood', 'gasoline', 'apple', 'ice', 'human', 'water', 'glass',
                 'diamond', 'titanium', 'steel', 'copper', 'lead', 'gold']
BUOY_FLUIDS = ['gasoline', 'oil', 'water', 'seawater', 'honey', 'mercury']

# Density's Compare screen (DensityCompareModel): 4 cubes
DENS_CUBES = [
    {'tag': 'B/A/B', 'sameMassVolume': 0.01,    'sameVolumeMass': 8, 'sameDensityVolume': 0.006},
    {'tag': 'A/C/A', 'sameMassVolume': 0.005,   'sameVolumeMass': 6, 'sameDensityVolume': 0.004},
    {'tag': 'C/D/C', 'sameMassVolume': 0.0025,  'sameVolumeMass': 4, 'sameDensityVolume': 0.002},
    {'tag': 'D/B/D', 'sameMassVolume': 0.00125, 'sameVolumeMass': 2, 'sameDensityVolume': 0.001},
]
DENS_SAME_MASS, DENS_SAME_VOL, DENS_SAME_RHO = 5.0, 0.005, 500.0

# Buoyancy: Basics' Compare screen (BuoyancyCompareModel): 2 cubes, brick and wood
BB_CUBES = [
    {'tag': 'A', 'sameMassVolume': 0.002, 'sameVolumeMass': 10, 'sameDensityVolume': 0.005},
    {'tag': 'B', 'sameMassVolume': 0.01,  'sameVolumeMass': 2,  'sameDensityVolume': 0.01},
]
BB_SAME_MASS, BB_SAME_VOL, BB_SAME_RHO = 4.0, 0.005, 400.0

# Density's Mystery screen: ('by volume' V in m^3, or 'by mass' m in kg) + density
MYSTERY = {
    'set 1': [('D', 'V', 0.005,  PHET['water']), ('B', 'V', 0.001, PHET['wood']),
              ('E', 'V', 0.007,  PHET['wood']),  ('C', 'V', 0.001, PHET['gold']),
              ('A', 'V', 0.0055, PHET['diamond'])],
    'set 2': [('D', 'M', 18.0, 4500), ('A', 'M', 18.0, 11340),
              ('E', 'V', 0.005, PHET['copper']), ('C', 'M', 2.7, 2700),
              ('B', 'M', 10.8, 2700)],
    'set 3': [('E', 'M', 6.0, 950), ('B', 'M', 6.0, 1000), ('D', 'M', 2.0, 400),
              ('C', 'M', 23.4, 7800), ('A', 'M', 2.85, 950)],
}


def mystery_blocks(setname):
    out = []
    for tag, kind, val, rho in MYSTERY[setname]:
        V = val if kind == 'V' else val / rho
        out.append({'tag': tag, 'V': V, 'rho': rho, 'm': rho * V})
    return out


def identify(m_disp, V_disp):
    """nearest table density to the density the PRINTED numbers give.

    Returns (name, rho_read, relative error to the winner, relative gap to the
    runner-up).  The sim prints mass to 2 dp in kg and volume to 2 dp in litres,
    so this is exactly what a student can do.
    """
    rho = m_disp / V_disp * LITERS
    d = sorted(((abs(PHET[k] - rho) / PHET[k], k) for k in DENSITY_TABLE))
    return d[0][1], rho, d[0][0], d[1][0]


def r2(x):
    """the sims' 2-dp display, rounding half away from zero like PhET's toFixed"""
    return math.floor(abs(x) * 100 + 0.5) / 100.0 * (1 if x >= 0 else -1)


# ==================================================================== the report
P('# derive.py — density / buoyancy-basics reference values')
P('# every value printed to 12 significant figures; selfTest asserts these')
P('')

P('## 1. the pool (PhET\'s bounds)')
P('POOL_W            %s' % f(POOL_W))
P('POOL_D            %s' % f(POOL_D))
P('POOL_H            %s' % f(POOL_H, 17))
P('A_POOL            %s' % f(A_POOL, 17))
P('V_POOL            %s' % f(V_POOL, 17))
P('VF0               %s' % f(VF0))
P('SCALE_V           %s' % f(SCALE_V, 17))
yw_empty = -POOL_H + VF0 / A_POOL
P('yw_empty          %s   # 100 L in an empty pool' % f(yw_empty, 17))
P('yw_empty_solved   %s   # bisection on G' % f(pool_level([], [], 1000.0), 17))
P('level_per_litre   %s   # m of level per litre displaced' % f(0.001 / A_POOL, 17))
P('')

P('## 2. Archimedes on a cube — the defaults of both sims')
# Density / Buoyancy Basics Intro+Explore: wood 2 kg and aluminium 13.5 kg, in water
for name, mass in (('wood', 2.0), ('aluminum', 13.5)):
    rho = PHET[name]
    V = mass / rho
    s = side(V)
    P('%-9s m %s kg  V %s L  s %s m' % (name, f(mass), f(V * LITERS), f(s, 17)))
one = solve([{'V': V, 'rho': rho}], 1000.0)
# both blocks together, as the two-block mode has them
BA = {'V': 2.0 / PHET['wood'], 'rho': PHET['wood']}
BB = {'V': 13.5 / PHET['aluminum'], 'rho': PHET['aluminum']}
for label, blocks in (('woodOnly', [dict(BA)]), ('alumOnly', [dict(BB)]), ('both', [dict(BA), dict(BB)])):
    r = solve(blocks, 1000.0)
    P('%-9s yw %s' % (label, f(r['yw'], 17)))
    for i, b in enumerate(r['blocks']):
        P('   blk%d mode %-5s Vsub %s L  yb %s  frac %s  W %s N  Fb %s N  N %s N'
          % (i, b['mode'], f(b['Vsub'] * LITERS), f(b['yb'], 17), f(b['frac']),
             f(b['W']), f(b['Fb']), f(b['N'])))
# the floating draft, three ways
V5 = 0.005
d_closed = draft_closed(V5, 400.0, 1000.0)
P('draft_closed      %s   # s rho_b/rho_f, wood 5 L in water' % f(d_closed, 17))
sideV = side(V5)


def net_force(d):
    return 1000.0 * G * sideV * sideV * d - 400.0 * V5 * G


if HAVE_SCIPY:
    P('draft_brentq      %s   (scipy)' % f(brentq(net_force, 0, sideV, xtol=1e-15, rtol=8.9e-16), 17))
P('draft_frac        %s   # d/s = rho_b/rho_f' % f(d_closed / sideV, 17))
P('rise_float_2kg    %s   # m/(rho_f A), a floating 2 kg block' % f(level_rise_floating(2.0, 1000.0), 17))
P('rise_sunk_5L      %s   # V/A, a fully submerged 5 L block' % f(level_rise_sunk(0.005), 17))
P('')

P('## 3. the awkward cases')
# (a) denser than the fluid: rests on the floor, contact force W - Fb
rr = solve([{'V': 0.005, 'rho': PHET['aluminum']}], 1000.0)['blocks'][0]
P('a_rest_mode       %s' % rr['mode'])
P('a_rest_N          %s   N   # (rho_b - rho_f) g V' % f(rr['N'], 17))
P('a_rest_N_closed   %s   N' % f((PHET['aluminum'] - 1000.0) * G * 0.005, 17))
P('a_rest_frac       %s' % f(rr['frac'], 17))
# (b) exactly neutral
nb = solve([{'V': 0.005, 'rho': 1000.0}], 1000.0)['blocks'][0]
P('b_neutral_mode    %s' % nb['mode'])
P('b_neutral_frac    %s' % f(nb['frac'], 17))
P('b_neutral_N       %s   N' % f(nb['N'], 17))
P('b_neutral_app     %s   N   # apparent weight of a neutral block' % f(apparent_weight(0.005, 1000.0, 1000.0), 17))
# held at three depths, fully submerged: the net force does not change
for hy in (-0.30, -0.25, -0.20):
    st = solve([{'V': 0.005, 'rho': 1000.0, 'held': hy}], 1000.0)['blocks'][0]
    P('b_neutral_held %-6s Vsub %s L   hand %s N' % (f(hy, 4), f(st['Vsub'] * LITERS, 17), f(st['hand'], 17)))
# (c) wider than the pool's free surface: a 216 L cube, s = 0.6 m > sqrt(A_POOL)
wide = {'V': 0.216, 'rho': 3000.0}
sw = side(wide['V'])
rw = solve([wide], 1000.0)
P('c_wide_side       %s   m   (footprint %s m2 vs A_POOL %s)' % (f(sw, 17), f(sw * sw, 12), f(A_POOL, 12)))
P('c_wide_yw         %s   # -H + s + Vf/A: all the fluid is ABOVE it' % f(rw['yw'], 17))
P('c_wide_yw_closed  %s' % f(-POOL_H + sw + VF0 / A_POOL, 17))
P('c_wide_frac       %s   # fully submerged' % f(rw['blocks'][0]['frac'], 17))
# a floating wide block instead
rwf = solve([{'V': 0.216, 'rho': 400.0}], 1000.0)
P('c_widefloat_yw    %s' % f(rwf['yw'], 17))
P('c_widefloat_yb    %s   # -H + Vf/A: it floats on ALL the fluid' % f(rwf['blocks'][0]['yb'], 17))
P('c_widefloat_clos  %s' % f(-POOL_H + VF0 / A_POOL, 17))
# monotonicity of G over the whole range, for a two-block configuration
mono_ok = True
prev = -1e18
for k in range(4001):
    y = -POOL_H + k * (POOL_H + 0.8) / 4000.0
    g = net_fluid(y, [dict(BA), dict(BB)], [], 1000.0)
    if g < prev - 1e-15:
        mono_ok = False
    prev = g
P('G_monotone        %s   # over 4001 levels, two blocks' % mono_ok)
P('')

P('## 4. the force, from the pressure on the faces')
# fully submerged aluminium 5 L in water at the solved level
st = solve([{'V': 0.005, 'rho': PHET['aluminum']}], 1000.0)
yw = st['yw']
yb = st['blocks'][0]['yb']
Fx, Fy = cube_pressure_force(0.005, yb, yw, 1000.0)
P('sub_Fy_faces      %s   N   # top + bottom faces' % f(Fy, 17))
P('sub_Fy_archim     %s   N   # rho_f g V_sub' % f(1000.0 * G * 0.005, 17))
P('sub_Fx_oneface    %s   N   # one side face; the opposite one is equal and opposite' % f(Fx, 17))
# partly submerged: a wood cube floating
stf = solve([{'V': 0.005, 'rho': 400.0}], 1000.0)
ywf, ybf = stf['yw'], stf['blocks'][0]['yb']
Fx2, Fy2 = cube_pressure_force(0.005, ybf, ywf, 1000.0)
P('flt_Fy_faces      %s   N' % f(Fy2, 17))
P('flt_Fy_archim     %s   N' % f(1000.0 * G * stf['blocks'][0]['Vsub'], 17))
P('flt_weight        %s   N' % f(400.0 * 0.005 * G, 17))
# the 2-D per-edge closed form on the square cross-section, per unit depth
sq = side(0.005)
poly = [(-sq / 2, ybf), (sq / 2, ybf), (sq / 2, ybf + sq), (-sq / 2, ybf + sq)]
sub = clip_below(poly, ywf)
efx, efy = edge_integral_2d(sub, ywf, 1000.0)
P('edge2d_Fx         %s   N/m' % f(efx, 12))
P('edge2d_Fy         %s   N/m   # = rho g A_sub' % f(efy, 17))
P('edge2d_rhogA      %s   N/m' % f(1000.0 * G * poly_area(sub), 17))
P('')

P('## 5. PhET\'s data')
P('# material           PhET     Wikipedia')
for k in sorted(PHET):
    w = WIKI[k]
    P('%-18s %8s %12s' % (k, PHET[k], '-' if w is None else w))
P('')
P('# Density, Compare screen: same mass %s kg / same volume %s L / same density %s kg/m3'
  % (f(DENS_SAME_MASS), f(DENS_SAME_VOL * LITERS), f(DENS_SAME_RHO)))
for c in DENS_CUBES:
    P('  sameMass  V %6s L -> rho %s' % (f(c['sameMassVolume'] * LITERS), f(DENS_SAME_MASS / c['sameMassVolume'], 12)))
for c in DENS_CUBES:
    P('  sameVol   m %6s kg -> rho %s' % (f(c['sameVolumeMass']), f(c['sameVolumeMass'] / DENS_SAME_VOL, 12)))
for c in DENS_CUBES:
    P('  sameRho   V %6s L -> m %s kg' % (f(c['sameDensityVolume'] * LITERS), f(DENS_SAME_RHO * c['sameDensityVolume'], 12)))
P('# Buoyancy: Basics, Compare screen: same mass %s kg / same volume %s L / same density %s'
  % (f(BB_SAME_MASS), f(BB_SAME_VOL * LITERS), f(BB_SAME_RHO)))
for c in BB_CUBES:
    P('  sameMass  V %6s L -> rho %s   sameVol m %s kg -> rho %s   sameRho V %s L -> m %s kg'
      % (f(c['sameMassVolume'] * LITERS), f(BB_SAME_MASS / c['sameMassVolume'], 12),
         f(c['sameVolumeMass']), f(c['sameVolumeMass'] / BB_SAME_VOL, 12),
         f(c['sameDensityVolume'] * LITERS), f(BB_SAME_RHO * c['sameDensityVolume'], 12)))
P('')

P('## 6. the mystery blocks, and whether the printed numbers identify them')
worst_margin = 1e9
worst_err = 0.0
worst_read = 0.0
for sn in ('set 1', 'set 2', 'set 3'):
    for b in sorted(mystery_blocks(sn), key=lambda z: z['tag']):
        md, Vd = r2(b['m']), r2(b['V'] * LITERS)
        name, rho_read, err, gap = identify(md, Vd)
        P('%-6s %s  m %8s kg (shown %5s)  V %8s L (shown %5s)  rho %s -> %-9s err %s  runner-up %s'
          % (sn, b['tag'], f(b['m'], 8), f(md), f(b['V'] * LITERS, 8), f(Vd),
             f(rho_read, 10), name, f(err, 3), f(gap, 3)))
        worst_margin = min(worst_margin, gap)
        worst_err = max(worst_err, err)
        worst_read = max(worst_read, abs(rho_read - b['rho']) / b['rho'])
P('mystery_worst_err     %s   # worst relative error to the winning material' % f(worst_err, 6))
P('mystery_worst_read    %s   # worst relative error of the READING vs the block\'s own density' % f(worst_read, 6))
P('mystery_worst_gap     %s   # smallest relative gap to the runner-up' % f(worst_margin, 6))
# the random set: every table material at every whole litre 1..10
wm, we, nbad = 1e9, 0.0, 0
for k in DENSITY_TABLE:
    for L in range(1, 11):
        m = PHET[k] * L / LITERS
        name, rho_read, err, gap = identify(r2(m), float(L))
        if name != k:
            nbad += 1
            P('  MISIDENTIFIED %s at %d L -> %s' % (k, L, name))
        wm = min(wm, gap)
        we = max(we, err)
P('random_misidentified  %d   # over 13 materials x 10 litres' % nbad)
P('random_worst_err      %s' % f(we, 6))
P('random_worst_gap      %s' % f(wm, 6))
P('')

P('## 7. Buoyancy: Basics — the six fluids')
for fl in BUOY_FLUIDS:
    rhoF = PHET[fl]
    row = []
    for mat, mass in (('wood', 2.0), ('aluminum', 13.5)):
        V = mass / PHET[mat]
        st = solve([{'V': V, 'rho': PHET[mat]}], rhoF)['blocks'][0]
        row.append('%s %s%% (%s)' % (mat, f(100 * st['frac'], 6), st['mode']))
    P('%-9s rho %6s  %s' % (fl, rhoF, '   '.join(row)))
# the pool scale, and what it reads
obs = [{'a': SCALE_W * SCALE_D, 'y0': -POOL_H + 0.5 * (POOL_H - SCALE_H), 'h': SCALE_H}]
sc_top = obs[0]['y0'] + SCALE_H
st = solve([{'V': 13.5 / PHET['aluminum'], 'rho': PHET['aluminum'], 'support': sc_top}],
           1000.0, obs=obs)
P('scale_top         %s   m  (height fraction 0.5)' % f(sc_top, 17))
P('scale_yw          %s' % f(st['yw'], 17))
P('scale_reads       %s   N   # W - rho_f g V_sub of the aluminium block' % f(st['blocks'][0]['N'], 17))
P('scale_in_air      %s   N   # the same block on the ground scale' % f(13.5 * G, 17))
P('')

P('## 8. PhET\'s slider ranges (read from density_en.html)')
P('minMass 0.1  maxMass 27  minCustomMass 0.5  maxCustomMass 27')
P('minVolumeLiters 1  maxVolumeLiters 10  volume step 0.5 L  mass step 0.1 kg')
P('custom fluid density range %s - %s kg/m3' % (f(0.5 * 1000), f(15 * 1000)))
for mat in SIMPLE_MASS:
    rho = PHET[mat]
    lo = clamp(rho * 1 / LITERS, 0.1, 27)
    hi = clamp(rho * 10 / LITERS, 0.1, 27)
    P('  %-10s rho %6s  mass enabled %s - %s kg' % (mat, rho, f(lo, 8), f(hi, 8)))
P('')

P('## 9. lowering a block through the surface — what a spring scale reads')
# a 5 L brick (2000 kg/m3) held with its BOTTOM at a run of heights, in water,
# with the free surface solved each time (it rises as the block goes in)
for hy in (0.10, -0.05, -0.1388888888888889, -0.20, -0.2554, -0.30, -POOL_H):
    r = solve([{'V': 0.005, 'rho': 2000.0, 'held': hy}], 1000.0)
    bk = r['blocks'][0]
    P('lower yb %-9s yw %s  Vsub %s L  scale %s N' %
      (f(hy, 8), f(r['yw'], 12), f(bk['Vsub'] * LITERS, 12), f(bk['W'] - bk['Fb'], 12)))
P('lower_W           %s   N   # 10 kg' % f(2000.0 * 0.005 * G, 17))
P('lower_Wapp_full   %s   N   # W - rho_f g V once under' % f(apparent_weight(0.005, 2000.0, 1000.0), 17))
P('')

P('## 10. both Compare screens, solved in water')
for label, cubes, mass, vol, rho0 in (
        ('density', DENS_CUBES, DENS_SAME_MASS, DENS_SAME_VOL, DENS_SAME_RHO),
        ('basics', BB_CUBES, BB_SAME_MASS, BB_SAME_VOL, BB_SAME_RHO)):
    for mode in ('sameMass', 'sameVolume', 'sameDensity'):
        bl = []
        for c in cubes:
            if mode == 'sameMass':
                bl.append({'V': c['sameMassVolume'], 'rho': mass / c['sameMassVolume']})
            elif mode == 'sameVolume':
                bl.append({'V': vol, 'rho': c['sameVolumeMass'] / vol})
            else:
                bl.append({'V': c['sameDensityVolume'], 'rho': rho0})
        r = solve(bl, 1000.0)
        P('%-8s %-12s yw %s  %s' % (label, mode, f(r['yw'], 12),
                                    ' '.join('%s:%s' % (b['mode'], f(100 * b['frac'], 6)) for b in r['blocks'])))
P('')

P('## 11. the two side faces of a submerged cube cancel')
st = solve([{'V': 0.005, 'rho': PHET['aluminum']}], 1000.0)
yb = st['blocks'][0]['yb']
yw = st['yw']
sq = side(0.005)
# +x face and -x face, each integrated independently
tot = 0.0
one = 0.0
for sgn in (+1, -1):
    acc = 0.0
    for k in range(4000):
        y = yb + sq * (k + 0.5) / 4000
        if y < yw:
            acc += -sgn * 1000.0 * G * (yw - y) * sq * (sq / 4000)
    tot += acc
    if sgn == +1:
        one = acc
P('side_plus         %s   N' % f(one, 12))
P('side_sum          %s   N   # exactly zero' % f(tot, 3))
P('')
P('## done')
