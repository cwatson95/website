#!/usr/bin/env python3
"""derive.py -- the Python twin of gravity-and-orbits.html.

Re-derives every number the sim asserts, from PhET's own data (read out of
docs/phets/gravity-and-orbits_en.html, 1.6.28) and from the measured values of
the Sun, the Earth, the Moon and the ISS, and prints them to 15+ digits.

Nothing here is quoted from memory: PhET's constants are grepped out of its
published build (see PHET below, each with the minified name it carries), and
the measured values come from the NASA planetary fact sheets and NASA's ISS
facts-and-figures page, each at the precision that page prints.

What is checked, in order:
  1. the four systems, on both screens, after PhET's centre-of-momentum shift
  2. the circular-orbit condition v = sqrt(GM/r) and Kepler's third law
  3. the exact Kepler solution (brentq on E - e sin E = M) against solve_ivp
  4. the sim's own PEFRL stepping against BOTH of those
  5. energy, angular momentum and momentum over long runs
  6. gravity off: exactly straight lines at constant speed
  7. the order of the integrator (PEFRL vs PhET's as-shipped step)
  8. what PhET's Model screen does to the physics on purpose

Run: python3 derive.py            (writes refvals.txt; gen_tables.py reads it)
"""
import io
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

OUT = []


def P(s=''):
    OUT.append(s)
    print(s)


# =====================================================================
#  PhET's values, read out of docs/phets/gravity-and-orbits_en.html
# =====================================================================
# Every entry names the minified identifier it was read from, so the grep can
# be repeated.  GravityAndOrbitsConstants (bp): EARTH_MASS:59724e20,
# SPACE_STATION_MASS:419725.  PhysicalConstants (Yg):
# GRAVITATIONAL_CONSTANT:667408e-16.  SceneFactory (KI): ZI=1.989e30 (sun),
# LI=7346e19 (moon).  GravityAndOrbitsClock (um): SECONDS_PER_DAY 86400,
# DEFAULT_DT 36e3.
PHET = dict(
    G=667408e-16,                 # 6.67408e-11, CODATA 2014
    SUN_MASS=1.989e30,            # ZI
    EARTH_MASS=59724e20,          # bp.EARTH_MASS
    MOON_MASS=7346e19,            # LI
    STATION_MASS=419725,          # bp.SPACE_STATION_MASS
    SUN_RADIUS=6957e5,            # 6.957e8 m
    EARTH_RADIUS=6371e3,
    MOON_RADIUS=1727400,          # PhET's figure; the measured mean is 1737.4 km
    STATION_RADIUS=45.5,
    EARTH_X=147098074e3,          # m from the sun
    EARTH_VY=30300,               # m/s
    MOON_Y=3633e5,                # 3.633e8 m from the earth
    MOON_VX=-1082,                # m/s
    STATION_X=6718045.5,          # m from the earth's centre
    STATION_VY=7706,              # m/s
    STATION_ROT=5484,             # s
    MOON_ROT=27.322 * 24 * 3600,  # s (PhET writes 27.322 d)
    SECONDS_PER_DAY=86400,
    DEFAULT_DT=36e3,
    SUBSTEP_FRAC=0.13125,         # GravityAndOrbitsPhysicsEngine.stepModel
    SPEED_STEPS=(1, 4, 7),        # slow / normal / fast substeps a frame
    STAGE_W=987.5, STAGE_H=772.5,  # GravityAndOrbitsSceneView.STAGE_SIZE
    VIEW_SCALE=1.5e-9,            # view units per metre, times the scene zoom
    ZOOM_MIN=0.5, ZOOM_MAX=1.3,   # GravityAndOrbitsConstants.ZOOM_RANGE
    MOON_BOOST=10200,             # ModelState.getTwoBodyForce, adjustMoonOrbit
    MODEL_SUN_R=50, MODEL_PLANET_R=800, MODEL_MOON_R=800,
    MODEL_MOON_VX=21, MODEL_MOON_Y_R=1.7,
    MODEL_PM_R=15, MODEL_SAT_PLANET_R=0.8, MODEL_SAT_R=2e4,
    PEFRL=(0.1786178958448091, -0.2123418310626054, -0.0662645826698185),
)

# ---- the measured values, each at the precision its source prints -----------
# NASA planetary fact sheets (nssdc.gsfc.nasa.gov/planetary/factsheet/), and
# NASA's ISS "Facts and Figures" page for the station.
MEAS = dict(
    SUN_MASS=1988400e24,        # sunfact:  1,988,400 x 10^24 kg
    SUN_RADIUS=695700e3,        # sunfact:  695,700 km (volumetric mean)
    SUN_GM=132712e6 * 1e9,      # sunfact:  132,712 x 10^6 km^3/s^2
    EARTH_MASS=5.9722e24,       # earthfact
    EARTH_RADIUS=6371.000e3,    # earthfact: volumetric mean radius
    EARTH_EQ_RADIUS=6378.137e3,
    EARTH_GM=0.39860e6 * 1e9,   # earthfact: 0.39860 x 10^6 km^3/s^2
    EARTH_A=149.598e9,          # earthfact: 149.598 x 10^6 km
    EARTH_PERI=147.095e9,       # earthfact: 147.095 x 10^6 km
    EARTH_VMAX=30.29e3,         # earthfact: max orbital velocity km/s
    EARTH_ECC=0.0167,
    MOON_MASS=7.346e22,         # moonfact
    MOON_RADIUS=1737.4e3,       # moonfact: volumetric mean radius
    MOON_PERI=363300e3,         # moonfact: perigee
    MOON_A=384400e3,
    MOON_VMAX=1.082e3,          # moonfact: max orbital velocity
    MOON_ROT=655.720 * 3600,    # moonfact: sidereal rotation period, hours
    STATION_MASS=419725,        # NASA ISS facts: 925,335 lb (419,725 kg)
    STATION_TRUSS=94.0,         # NASA ISS facts: 310 ft (94 m)
)

G = PHET['G']
DAY = PHET['SECONDS_PER_DAY']


# =====================================================================
#  the four systems, on the two screens
# =====================================================================
def body(name, kind, m, r, x, y, vx, vy, rot=None):
    return dict(name=name, kind=kind, m=float(m), r=float(r), x=float(x), y=float(y),
                vx=float(vx), vy=float(vy), rot=rot, fixed=False)


def base_scene(sid):
    """PhET's SceneFactory configs, before any Model-screen exaggeration."""
    if sid == 'starPlanet':
        bs = [body('Our Sun', 'star', PHET['SUN_MASS'], PHET['SUN_RADIUS'], 0, 0, 0, 0),
              body('Earth', 'planet', PHET['EARTH_MASS'], PHET['EARTH_RADIUS'],
                   PHET['EARTH_X'], 0, 0, PHET['EARTH_VY'])]
        return dict(id=sid, bodies=bs, zoom=1.25, dt=PHET['DEFAULT_DT'],
                    grid=PHET['EARTH_X'] / 2, pair=(0, 1))
    if sid == 'starPlanetMoon':
        bs = [body('Our Sun', 'star', PHET['SUN_MASS'], PHET['SUN_RADIUS'], 0, 0, 0, 0),
              body('Earth', 'planet', PHET['EARTH_MASS'], PHET['EARTH_RADIUS'],
                   PHET['EARTH_X'], 0, 0, PHET['EARTH_VY']),
              body('Our Moon', 'moon', PHET['MOON_MASS'], PHET['MOON_RADIUS'],
                   PHET['EARTH_X'], PHET['MOON_Y'], PHET['MOON_VX'], PHET['EARTH_VY'])]
        return dict(id=sid, bodies=bs, zoom=1.25, dt=PHET['DEFAULT_DT'],
                    grid=PHET['EARTH_X'] / 2, pair=(0, 1))
    if sid == 'planetMoon':
        # PhET puts this pair in its own centre-of-momentum frame by hand
        vp = -PHET['MOON_VX'] * PHET['MOON_MASS'] / (PHET['EARTH_MASS'] + PHET['MOON_MASS'])
        vm = vp + PHET['MOON_VX']
        bs = [body('Earth', 'planet', PHET['EARTH_MASS'], PHET['EARTH_RADIUS'],
                   PHET['EARTH_X'], 0, vp, 0),
              body('Our Moon', 'moon', PHET['MOON_MASS'], PHET['MOON_RADIUS'],
                   PHET['EARTH_X'], PHET['MOON_Y'], vm, 0)]
        return dict(id=sid, bodies=bs, zoom=400, dt=PHET['DEFAULT_DT'] / 3,
                    grid=PHET['MOON_Y'] / 2, pair=(0, 1), centre=(PHET['EARTH_X'], 0.0))
    if sid == 'planetSatellite':
        bs = [body('Earth', 'planet', PHET['EARTH_MASS'], PHET['EARTH_RADIUS'], 0, 0, 0, 0),
              body('Space Station', 'satellite', PHET['STATION_MASS'], PHET['STATION_RADIUS'],
                   PHET['STATION_X'], 0, 0, PHET['STATION_VY'], rot=PHET['STATION_ROT'])]
        return dict(id=sid, bodies=bs, zoom=21600, dt=9e-4 * PHET['DEFAULT_DT'],
                    grid=PHET['STATION_X'], pair=(0, 1))
    raise ValueError(sid)


def centre(sc):
    """ModeConfig.center(): subtract the centre-of-momentum velocity."""
    M = sum(b['m'] for b in sc['bodies'])
    px = sum(b['m'] * b['vx'] for b in sc['bodies'])
    py = sum(b['m'] * b['vy'] for b in sc['bodies'])
    for b in sc['bodies']:
        b['vx'] -= px / M
        b['vy'] -= py / M
    return sc


def scene(screen, sid):
    """A scene of either screen, exactly as PhET builds it."""
    sc = base_scene(sid)
    sc['screen'] = screen
    sc['boost'] = 1.0
    bs = sc['bodies']
    if screen == 'model':
        if sid == 'starPlanet':
            bs[0]['r'] *= PHET['MODEL_SUN_R']
            bs[1]['r'] *= PHET['MODEL_PLANET_R']
            bs[0]['fixed'] = True
        elif sid == 'starPlanetMoon':
            bs[0]['r'] *= PHET['MODEL_SUN_R']
            bs[1]['r'] *= PHET['MODEL_PLANET_R']
            bs[2]['r'] *= PHET['MODEL_MOON_R']
            bs[2]['vx'] *= PHET['MODEL_MOON_VX']
            bs[2]['y'] = bs[1]['x'] * 0 + bs[1]['y'] + PHET['MODEL_MOON_Y_R'] * bs[1]['r']
            bs[0]['fixed'] = True
            sc['boost'] = PHET['MOON_BOOST']
        elif sid == 'planetMoon':
            bs[0]['r'] *= PHET['MODEL_PM_R']
            bs[1]['r'] *= PHET['MODEL_PM_R']
            bs[1]['rot'] = PHET['MOON_ROT']
        elif sid == 'planetSatellite':
            bs[0]['r'] *= PHET['MODEL_SAT_PLANET_R']
            bs[1]['r'] *= PHET['MODEL_SAT_R']
    return centre(sc)


SCENES = ['starPlanet', 'starPlanetMoon', 'planetMoon', 'planetSatellite']
SCREENS = ['model', 'scale']


# =====================================================================
#  the engine: PEFRL on the state, with PhET's two Model-screen cheats
# =====================================================================
def st_of(sc):
    bs = sc['bodies']
    return dict(n=len(bs),
                m=np.array([b['m'] for b in bs]), x=np.array([b['x'] for b in bs]),
                y=np.array([b['y'] for b in bs]), vx=np.array([b['vx'] for b in bs]),
                vy=np.array([b['vy'] for b in bs]),
                fix=np.array([1.0 if b['fixed'] else 0.0 for b in bs]),
                kind=[b['kind'] for b in bs], boost=sc['boost'])


def st_copy(S):
    T = dict(S)
    for k in ('m', 'x', 'y', 'vx', 'vy', 'fix'):
        T[k] = S[k].copy()
    return T


def accel(S):
    """The acceleration on every body.  PhET's Model Sun-Planet-Moon scene
    multiplies the pull of the PLANET on the MOON by 10200 and does NOT apply
    the reaction, so Newton's third law is deliberately broken there."""
    n = S['n']
    ax = np.zeros(n)
    ay = np.zeros(n)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dx = S['x'][j] - S['x'][i]
            dy = S['y'][j] - S['y'][i]
            r2 = dx * dx + dy * dy
            r = math.sqrt(r2)
            k = 1.0
            if S['boost'] != 1.0 and S['kind'][i] == 'moon' and S['kind'][j] == 'planet':
                k = S['boost']
            f = k * G * S['m'][j] / (r2 * r)
            ax[i] += f * dx
            ay[i] += f * dy
    return ax, ay


def drift(S, c):
    free = 1.0 - S['fix']
    S['x'] += c * S['vx'] * free
    S['y'] += c * S['vy'] * free


def kick(S, c):
    ax, ay = accel(S)
    free = 1.0 - S['fix']
    S['vx'] += c * ax * free
    S['vy'] += c * ay * free


XI, LAM, CHI = PHET['PEFRL']


def pefrl(S, h):
    drift(S, XI * h)
    kick(S, (1 - 2 * LAM) * h / 2)
    drift(S, CHI * h)
    kick(S, LAM * h)
    drift(S, (1 - 2 * (CHI + XI)) * h)
    kick(S, LAM * h)
    drift(S, CHI * h)
    kick(S, (1 - 2 * LAM) * h / 2)
    drift(S, XI * h)


def phet_step(S, h):
    """PhET's step AS SHIPPED: the same composition, but the acceleration is
    evaluated once and reused by all four kicks -- which makes it first order."""
    ax, ay = accel(S)
    free = 1.0 - S['fix']

    def k(c):
        S['vx'] += c * ax * free
        S['vy'] += c * ay * free
    drift(S, XI * h)
    k((1 - 2 * LAM) * h / 2)
    drift(S, CHI * h)
    k(LAM * h)
    drift(S, (1 - 2 * (CHI + XI)) * h)
    k(LAM * h)
    drift(S, CHI * h)
    k((1 - 2 * LAM) * h / 2)
    drift(S, XI * h)


ETA = 0.02


def step_limit(S):
    tau = math.inf
    for i in range(S['n']):
        for j in range(i + 1, S['n']):
            dx = S['x'][j] - S['x'][i]
            dy = S['y'][j] - S['y'][i]
            r = math.hypot(dx, dy)
            k = S['boost'] if (S['boost'] != 1.0 and 'moon' in (S['kind'][i], S['kind'][j])
                               and 'planet' in (S['kind'][i], S['kind'][j])) else 1.0
            tff = math.sqrt(r ** 3 / (k * G * (S['m'][i] + S['m'][j])))
            tau = min(tau, tff)
            dv = math.hypot(S['vx'][j] - S['vx'][i], S['vy'][j] - S['vy'][i])
            if dv > 0:
                tau = min(tau, r / dv)
    return ETA * tau if math.isfinite(tau) else math.inf


def advance(S, dt, gravity=True, stepfn=None):
    if not gravity:                       # PhET's getNextCoastingState: pure drift
        drift(S, dt)
        return 1
    lim = step_limit(S)
    n = max(1, int(math.ceil(abs(dt) / lim)))
    h = dt / n
    fn = stepfn or pefrl
    for _ in range(n):
        fn(S, h)
    return n


def energy(S):
    K = float(np.sum(0.5 * S['m'] * (S['vx'] ** 2 + S['vy'] ** 2)))
    U = 0.0
    for i in range(S['n']):
        for j in range(i + 1, S['n']):
            U -= G * S['m'][i] * S['m'][j] / math.hypot(S['x'][j] - S['x'][i], S['y'][j] - S['y'][i])
    return K + U, K, U


def angular(S):
    return float(np.sum(S['m'] * (S['x'] * S['vy'] - S['y'] * S['vx'])))


def momentum(S):
    return float(np.sum(S['m'] * S['vx'])), float(np.sum(S['m'] * S['vy']))


def com(S):
    M = float(np.sum(S['m']))
    return (float(np.sum(S['m'] * S['x'])) / M, float(np.sum(S['m'] * S['y'])) / M,
            float(np.sum(S['m'] * S['vx'])) / M, float(np.sum(S['m'] * S['vy'])) / M, M)


def frame_dt(sc, speed=1):
    """PhET's frame: 0.13125 x the scene's dt, taken 1/4/7 times."""
    return PHET['SUBSTEP_FRAC'] * sc['dt'] * PHET['SPEED_STEPS'][speed]


# =====================================================================
#  the exact answers
# =====================================================================
def conic(x, y, vx, vy, mu):
    """Elements from a state vector: vis-viva for a, the eccentricity vector
    for e and the periapsis direction, sign(h) for the sense of travel."""
    r = math.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    h = x * vy - y * vx
    en = 0.5 * v2 - mu / r
    ex = ((v2 - mu / r) * x - rv * vx) / mu
    ey = ((v2 - mu / r) * y - rv * vy) / mu
    e = math.hypot(ex, ey)
    d = 1 if h >= 0 else -1
    w = math.atan2(ey, ex) if e > 1e-12 else math.atan2(y, x)
    nu0 = math.atan2(d * (y * math.cos(w) - x * math.sin(w)), x * math.cos(w) + y * math.sin(w))
    out = dict(mu=mu, r=r, v=math.sqrt(v2), h=h, dir=d, energy=en, e=e, w=w, nu0=nu0,
               p=h * h / mu, vesc=math.sqrt(2 * mu / r))
    if en < 0:
        a = -mu / (2 * en)
        out.update(kind='ellipse', a=a, b=a * math.sqrt(max(0.0, 1 - e * e)),
                   n=math.sqrt(mu / a ** 3), T=2 * math.pi * math.sqrt(a ** 3 / mu),
                   q=a * (1 - e), Q=a * (1 + e))
        E0 = 2 * math.atan2(math.sqrt(1 - e) * math.sin(nu0 / 2), math.sqrt(1 + e) * math.cos(nu0 / 2))
        out['E0'] = E0
        out['M0'] = E0 - e * math.sin(E0)
    else:
        out.update(kind='hyperbola' if en > 0 else 'parabola', a=-mu / (2 * en) if en else math.inf,
                   T=math.inf, q=h * h / mu / (1 + e), Q=math.inf)
    return out


def kepler_E(M, e):
    """E - e sin E = M, by brentq on the bracket [M - e, M + e]."""
    turns = round(M / (2 * math.pi))
    Mr = M - 2 * math.pi * turns
    if e == 0:
        return Mr + 2 * math.pi * turns
    f = lambda E: E - e * math.sin(E) - Mr
    E = brentq(f, Mr - e - 1e-12, Mr + e + 1e-12, xtol=1e-15, rtol=8.9e-16, maxiter=200)
    return E + 2 * math.pi * turns


def state_on(el, t):
    """The state on the conic a time t after the state it was built from."""
    w, d = el['w'], el['dir']
    Px, Py = math.cos(w), math.sin(w)
    Qx, Qy = -d * math.sin(w), d * math.cos(w)
    M = el['M0'] + el['n'] * t
    E = kepler_E(M, el['e'])
    cE, sE = math.cos(E), math.sin(E)
    r = el['a'] * (1 - el['e'] * cE)
    X = el['a'] * (cE - el['e'])
    Y = el['b'] * sE
    VX = -el['n'] * el['a'] * el['a'] * sE / r
    VY = el['n'] * el['a'] * el['b'] * cE / r
    return (X * Px + Y * Qx, X * Py + Y * Qy, VX * Px + VY * Qx, VX * Py + VY * Qy)


def two_body_ref(sc):
    """The closed-form answer for a scene of two bodies.  A FIXED star makes it
    a one-body problem about mu = G M; two free bodies reduce to the relative
    orbit about mu = G(m1+m2) with the centre of mass drifting in a line."""
    bs = sc['bodies']
    if len(bs) != 2:
        return None
    a, b = bs
    if a['fixed'] and not b['fixed']:
        mu = G * a['m']
        el = conic(b['x'] - a['x'], b['y'] - a['y'], b['vx'], b['vy'], mu)
        return dict(kind='fixed', mu=mu, el=el, cx=a['x'], cy=a['y'])
    mu = G * (a['m'] + b['m'])
    el = conic(b['x'] - a['x'], b['y'] - a['y'], b['vx'] - a['vx'], b['vy'] - a['vy'], mu)
    cx, cy, cvx, cvy, M = com(st_of(sc))
    return dict(kind='free', mu=mu, el=el, cx=cx, cy=cy, cvx=cvx, cvy=cvy,
                f1=b['m'] / M, f2=a['m'] / M)


def two_body_at(ref, t):
    """Where both bodies are at time t, exactly."""
    x, y, vx, vy = state_on(ref['el'], t)
    if ref['kind'] == 'fixed':
        return (ref['cx'], ref['cy'], 0.0, 0.0, ref['cx'] + x, ref['cy'] + y, vx, vy)
    cx = ref['cx'] + ref['cvx'] * t
    cy = ref['cy'] + ref['cvy'] * t
    return (cx - ref['f1'] * x, cy - ref['f1'] * y, ref['cvx'] - ref['f1'] * vx, ref['cvy'] - ref['f1'] * vy,
            cx + ref['f2'] * x, cy + ref['f2'] * y, ref['cvx'] + ref['f2'] * vx, ref['cvy'] + ref['f2'] * vy)


def rhs(t, u, S):
    n = S['n']
    x, y, vx, vy = u[:n], u[n:2 * n], u[2 * n:3 * n], u[3 * n:]
    T = dict(S)
    T['x'], T['y'], T['vx'], T['vy'] = x, y, vx, vy
    ax, ay = accel(T)
    free = 1.0 - S['fix']
    return np.concatenate([vx * free, vy * free, ax * free, ay * free])


def ivp(S, T, rtol=1e-13, atol=1.0):
    u0 = np.concatenate([S['x'], S['y'], S['vx'], S['vy']])
    s = solve_ivp(rhs, (0, T), u0, args=(S,), method='DOP853', rtol=rtol, atol=atol,
                  dense_output=True)
    assert s.success, s.message
    return s


# =====================================================================
#  1. the systems
# =====================================================================
REF = {}
P('# gravity-and-orbits derive.py -- run python3 derive.py')
P()
P('# PhET constants, read out of docs/phets/gravity-and-orbits_en.html (1.6.28)')
for k in ('G', 'SUN_MASS', 'EARTH_MASS', 'MOON_MASS', 'STATION_MASS', 'SUN_RADIUS',
          'EARTH_RADIUS', 'MOON_RADIUS', 'STATION_RADIUS', 'EARTH_X', 'EARTH_VY',
          'MOON_Y', 'MOON_VX', 'STATION_X', 'STATION_VY'):
    P('  %-16s %s' % (k, repr(PHET[k])))
P()
P('# PhET against the measurement (each measured value at its source\'s own precision)')
CMP = []
for label, pk, mk, unit, src in [
        ('Sun mass', 'SUN_MASS', 'SUN_MASS', 'kg', 'NASA sunfact'),
        ('Sun radius', 'SUN_RADIUS', 'SUN_RADIUS', 'm', 'NASA sunfact (volumetric mean)'),
        ('Earth mass', 'EARTH_MASS', 'EARTH_MASS', 'kg', 'NASA earthfact'),
        ('Earth radius', 'EARTH_RADIUS', 'EARTH_RADIUS', 'm', 'NASA earthfact (volumetric mean)'),
        ('Moon mass', 'MOON_MASS', 'MOON_MASS', 'kg', 'NASA moonfact'),
        ('Moon radius', 'MOON_RADIUS', 'MOON_RADIUS', 'm', 'NASA moonfact (volumetric mean)'),
        ('ISS mass', 'STATION_MASS', 'STATION_MASS', 'kg', 'NASA ISS facts and figures'),
        ('Earth perihelion', 'EARTH_X', 'EARTH_PERI', 'm', 'NASA earthfact'),
        ('Earth max speed', 'EARTH_VY', 'EARTH_VMAX', 'm/s', 'NASA earthfact'),
        ('Moon perigee', 'MOON_Y', 'MOON_PERI', 'm', 'NASA moonfact'),
        ('Moon max speed', 'MOON_VX', 'MOON_VMAX', 'm/s', 'NASA moonfact'),
]:
    pv = abs(PHET[pk])
    mv = MEAS[mk]
    rel = (pv - mv) / mv
    CMP.append(dict(label=label, phet=pv, meas=mv, rel=rel, unit=unit, src=src))
    P('  %-18s PhET %-16.7g  measured %-16.7g  %+8.4f %%   [%s]' % (label, pv, mv, 100 * rel, src))
P('  G: PhET 6.67408e-11 (CODATA 2014); CODATA 2018 is 6.67430e-11, %+.4f %% away'
  % (100 * (PHET['G'] - 6.6743e-11) / 6.6743e-11))
REF['cmp'] = CMP
REF['phet'] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in PHET.items()}
REF['meas'] = MEAS

P()
P('# the four systems on both screens, after PhET\'s centre-of-momentum shift')
REF['scenes'] = {}
for screen in SCREENS:
    for sid in SCENES:
        sc = scene(screen, sid)
        S = st_of(sc)
        E, K, U = energy(S)
        L = angular(S)
        px, py = momentum(S)
        cx, cy, cvx, cvy, M = com(S)
        key = screen + '/' + sid
        REF['scenes'][key] = dict(
            n=S['n'], m=[b['m'] for b in sc['bodies']], r=[b['r'] for b in sc['bodies']],
            x=[b['x'] for b in sc['bodies']], y=[b['y'] for b in sc['bodies']],
            vx=[b['vx'] for b in sc['bodies']], vy=[b['vy'] for b in sc['bodies']],
            fix=[bool(b['fixed']) for b in sc['bodies']], boost=sc['boost'],
            E=E, K=K, U=U, L=L, px=px, py=py, comx=cx, comy=cy,
            lim=step_limit(S), dt=sc['dt'], zoom=sc['zoom'], grid=sc['grid'],
            frame=frame_dt(sc, 1))
        P('  %-24s n=%d  E=%+.12e  L=%+.12e  |p|=%.3e  step limit %.4g s  frame %.4g s'
          % (key, S['n'], E, L, math.hypot(px, py), step_limit(S), frame_dt(sc, 1)))

# =====================================================================
#  2. the circular-orbit condition and Kepler's third law
# =====================================================================
P()
P('# the circular-orbit condition v = sqrt(GM/r), and T = 2 pi sqrt(r^3/GM)')
CIRC = {}
for sid, mk, rk, vk in [('starPlanet', 'SUN_MASS', 'EARTH_X', 'EARTH_VY'),
                        ('planetMoon', 'EARTH_MASS', 'MOON_Y', 'MOON_VX'),
                        ('planetSatellite', 'EARTH_MASS', 'STATION_X', 'STATION_VY')]:
    Mc = PHET[mk]
    r = PHET[rk]
    v = abs(PHET[vk])
    vc = math.sqrt(G * Mc / r)
    Tc = 2 * math.pi * math.sqrt(r ** 3 / (G * Mc))
    # the same period the long way: integrate the circular orbit and time the return
    CIRC[sid] = dict(M=Mc, r=r, v=v, vc=vc, ratio=v / vc, T=Tc, Tdays=Tc / DAY,
                     vesc=math.sqrt(2) * vc)
    P('  %-16s r = %.9e m   v_c = %.9f m/s   PhET starts at %.1f m/s (%.6f of v_c)'
      % (sid, r, vc, v, v / vc))
    P('  %-16s T_circ = %.9e s = %.9f d   v_esc = %.6f m/s'
      % ('', Tc, Tc / DAY, math.sqrt(2) * vc))
# the third law as a ratio: T^2/a^3 must be 4 pi^2 / GM for every orbit about the same M
P('  T^2/a^3 for a circular orbit about the Sun   = %.15e s^2/m^3 (4 pi^2/GM = %.15e)'
  % (CIRC['starPlanet']['T'] ** 2 / CIRC['starPlanet']['r'] ** 3,
     4 * math.pi ** 2 / (G * PHET['SUN_MASS'])))
P('  T^2/a^3 for a circular orbit about the Earth = %.15e s^2/m^3 (4 pi^2/GM = %.15e)'
  % (CIRC['planetMoon']['T'] ** 2 / CIRC['planetMoon']['r'] ** 3,
     4 * math.pi ** 2 / (G * PHET['EARTH_MASS'])))
REF['circ'] = CIRC

# the third law across the two Earth satellites: the moon and the station
rm, rs = CIRC['planetMoon'], CIRC['planetSatellite']
P('  moon vs station about the Earth: (T_m/T_s)^2 = %.12f, (r_m/r_s)^3 = %.12f'
  % ((rm['T'] / rs['T']) ** 2, (rm['r'] / rs['r']) ** 3))
REF['third'] = dict(T2=(rm['T'] / rs['T']) ** 2, a3=(rm['r'] / rs['r']) ** 3)

# =====================================================================
#  3-4. the exact orbit, solve_ivp, and the sim's own stepping
# =====================================================================
P()
P('# the two-body scenes: elements from the state vector, and the exact orbit')
REF['two'] = {}
for screen in SCREENS:
    for sid in ('starPlanet', 'planetMoon', 'planetSatellite'):
        sc = scene(screen, sid)
        ref = two_body_ref(sc)
        el = ref['el']
        key = screen + '/' + sid
        REF['two'][key] = dict(kind=ref['kind'], mu=ref['mu'], a=el['a'], e=el['e'], T=el['T'],
                               q=el['q'], Q=el['Q'], w=el['w'], dir=el['dir'],
                               Tdays=el['T'] / DAY, energy=el['energy'], vesc=el['vesc'],
                               conic=el['kind'])
        P('  %-24s %-6s mu=%.9e  a=%.9e m  e=%.12f  T=%.9f d  q=%.6e  Q=%.6e'
          % (key, ref['kind'], ref['mu'], el['a'], el['e'], el['T'] / DAY, el['q'], el['Q']))

P()
P('# the sim\'s own stepping against the exact Kepler solution AND against solve_ivp')
REF['runs'] = {}
for screen in SCREENS:
    for sid in SCENES:
        sc = scene(screen, sid)
        S = st_of(sc)
        ref = two_body_ref(sc)
        dt = frame_dt(sc, 1)
        nf = 400
        sv = ivp(st_of(sc), nf * dt)
        worstK = 0.0
        worstI = 0.0
        nsub = 0
        for f in range(nf):
            nsub = advance(S, dt)
        t = nf * dt
        u = sv.sol(t)
        n = S['n']
        for i in range(n):
            worstI = max(worstI, math.hypot(S['x'][i] - u[i], S['y'][i] - u[n + i]))
        if ref is not None:
            ex = two_body_at(ref, t)
            worstK = max(math.hypot(S['x'][0] - ex[0], S['y'][0] - ex[1]),
                         math.hypot(S['x'][1] - ex[4], S['y'][1] - ex[5]))
        key = screen + '/' + sid
        scale = max(abs(sc['bodies'][1]['x'] - sc['bodies'][0]['x']),
                    abs(sc['bodies'][1]['y'] - sc['bodies'][0]['y']), 1.0)
        REF['runs'][key] = dict(frames=nf, dt=dt, t=t, nsub=nsub,
                                x=[float(v) for v in S['x']], y=[float(v) for v in S['y']],
                                vx=[float(v) for v in S['vx']], vy=[float(v) for v in S['vy']],
                                dev_ivp=worstI, dev_kepler=worstK if ref else None,
                                rel_ivp=worstI / scale,
                                rel_kepler=(worstK / scale) if ref else None)
        P('  %-24s %4d frames (%.6g s, %.4f d): vs solve_ivp %.4e m (%.2e of r), vs Kepler %s'
          % (key, nf, t, t / DAY, worstI, worstI / scale,
             ('%.4e m (%.2e of r)' % (worstK, worstK / scale)) if ref else 'n/a (3 bodies)'))

# =====================================================================
#  5. conservation over long runs
# =====================================================================
P()
P('# energy, angular momentum and momentum over 4000 frames')
REF['cons'] = {}
for screen in SCREENS:
    for sid in SCENES:
        sc = scene(screen, sid)
        S = st_of(sc)
        E0, _, _ = energy(S)
        L0 = angular(S)
        p0 = momentum(S)
        pscale = float(np.sum(S['m'] * np.hypot(S['vx'], S['vy']))) or 1.0
        dt = frame_dt(sc, 1)
        dE = dL = dP = 0.0
        for f in range(4000):
            advance(S, dt)
            E, _, _ = energy(S)
            L = angular(S)
            p = momentum(S)
            dE = max(dE, abs(E - E0) / abs(E0))
            dL = max(dL, abs(L - L0) / max(1e-300, abs(L0)))
            dP = max(dP, math.hypot(p[0] - p0[0], p[1] - p0[1]) / pscale)
        key = screen + '/' + sid
        REF['cons'][key] = dict(frames=4000, t=4000 * dt, dE=dE, dL=dL, dP=dP,
                                xend=[float(v) for v in S['x']], yend=[float(v) for v in S['y']])
        P('  %-24s over %10.4f d: |dE/E| <= %.3e   |dL/L| <= %.3e   |dp|/p <= %.3e'
          % (key, 4000 * dt / DAY, dE, dL, dP))
P('  (the Model screen nails the star down and boosts the moon-planet pull, so its')
P('   momentum and energy are NOT conserved -- that is PhET\'s model, not an error here)')

# =====================================================================
#  6. gravity off
# =====================================================================
P()
P('# gravity off: PhET\'s getNextCoastingState is a pure drift -- straight lines, constant speed')
REF['coast'] = {}
for screen in SCREENS:
    for sid in SCENES:
        sc = scene(screen, sid)
        S = st_of(sc)
        v0 = [math.hypot(S['vx'][i], S['vy'][i]) for i in range(S['n'])]
        x0, y0 = S['x'].copy(), S['y'].copy()
        vx0, vy0 = S['vx'].copy(), S['vy'].copy()
        dt = frame_dt(sc, 1)
        # one frame is EXACTLY x + vx dt, bit for bit: a drift and nothing else
        T1 = st_copy(S)
        advance(T1, dt, gravity=False)
        exact1 = all(T1['x'][i] == x0[i] + vx0[i] * dt and T1['y'][i] == y0[i] + vy0[i] * dt
                     for i in range(S['n']) if not S['fix'][i])
        worst_line = 0.0
        worst_speed = 0.0
        travel = 1.0
        for f in range(1, 601):
            advance(S, dt, gravity=False)
            t = f * dt
            for i in range(S['n']):
                if S['fix'][i]:
                    continue
                # the residual perpendicular to v0: a straight line has none
                ux, uy = vx0[i] / v0[i], vy0[i] / v0[i]
                dx, dy = S['x'][i] - x0[i], S['y'][i] - y0[i]
                worst_line = max(worst_line, abs(dx * uy - dy * ux))
                travel = max(travel, math.hypot(dx, dy))
                worst_speed = max(worst_speed, abs(math.hypot(S['vx'][i], S['vy'][i]) - v0[i]))
        key = screen + '/' + sid
        REF['coast'][key] = dict(frames=600, dev=worst_line, rel=worst_line / travel,
                                 dspeed=worst_speed, exact1=bool(exact1), travel=travel,
                                 xend=[float(v) for v in S['x']], yend=[float(v) for v in S['y']])
        P('  %-24s 600 frames: one frame is exactly a drift: %s; off the straight line by <= %.3e m '
          '(%.2e of the %.4e m travelled); |v| changes by %.3e m/s'
          % (key, 'yes' if exact1 else 'NO', worst_line, worst_line / travel, travel, worst_speed))

# =====================================================================
#  7. the order of the two integrators
# =====================================================================
P()
P('# the order of the integrator, measured by halving the step (to scale, star and planet)')
# The step counts have to stay coarse enough that the error is well above the
# ROUNDOFF FLOOR: positions are ~1.5e11 m, so one ulp is 3e-5 m and a run of N
# steps random-walks about sqrt(N) ulps.  At N = 1600 over 40 days PEFRL's own
# truncation error is 3e-3 m, which IS that floor, and the measured ratio falls
# to 1.2 on perfectly correct code.  N = 20..160 keeps every error above 1 m.
sc = scene('scale', 'starPlanet')
T = 40 * 86400.0


def run_fixed(N, fn):
    S = st_of(sc)
    h = T / N
    for _ in range(N):
        fn(S, h)
    return S


REFS = run_fixed(25600, pefrl)
ORD = {}
for nm, fn in (('pefrl', pefrl), ('phet', phet_step)):
    errs = []
    for N in (20, 40, 80, 160):
        S = run_fixed(N, fn)
        d = max(max(abs(S['x'][i] - REFS['x'][i]), abs(S['y'][i] - REFS['y'][i]))
                for i in range(S['n']))
        errs.append((N, d))
    ratios = [errs[i][1] / errs[i + 1][1] for i in range(len(errs) - 1)]
    order = sum(math.log2(r) for r in ratios) / len(ratios)
    ORD[nm] = dict(errs=errs, ratios=ratios, order=order)
    P('  %-6s %s   ratios %s -> order %.3f'
      % (nm, '  '.join('N=%-5d err %.4e' % e for e in errs),
         ' '.join('%.2f' % r for r in ratios), order))
P('  PEFRL is fourth order (16 per halving); PhET\'s as-shipped step is first (2 per halving).')
P('  At PhET\'s own substep the difference is invisible over a frame, and both are drawn here.')
REF['orders'] = ORD


def order_time(S):
    """The time the sim's own order sweep runs over: a ninth of the CLOSEST pair's reference
    period.  A fixed 40 days is more than a whole (boosted) lunar orbit on the Model screen,
    where PhET's first-order step then saturates at the size of the system and the measured
    order collapses to 0.58 -- a number about the saturation, not about the method."""
    T = math.inf
    for i in range(S['n']):
        for j in range(i + 1, S['n']):
            r = math.hypot(S['x'][j] - S['x'][i], S['y'][j] - S['y'][i])
            k = S['boost'] if (S['boost'] != 1.0 and 'moon' in (S['kind'][i], S['kind'][j])
                               and 'planet' in (S['kind'][i], S['kind'][j])) else 1.0
            T = min(T, 2 * math.pi * math.sqrt(r ** 3 / (k * G * (S['m'][i] + S['m'][j]))))
    return T / 9


P()
P('# the sim runs the same sweep on whatever system is on the bench, over T_ref/9')
OT = {}
for screen in SCREENS:
    for sid in SCENES:
        OT[screen + '/' + sid] = order_time(st_of(scene(screen, sid)))
ORD2 = {}
for key in ('scale/starPlanet', 'model/starPlanetMoon'):
    screen, sid = key.split('/')
    sc2 = scene(screen, sid)
    T2 = OT[key]

    def run2(N, fn, sc2=sc2, T2=T2):
        S = st_of(sc2)
        h = T2 / N
        for _ in range(N):
            fn(S, h)
        return S
    R2 = run2(25600, pefrl)
    row = {}
    for nm, fn in (('pefrl', pefrl), ('phet', phet_step)):
        errs = []
        for N in (20, 40, 80, 160):
            S = run2(N, fn)
            d = max(max(abs(S['x'][i] - R2['x'][i]), abs(S['y'][i] - R2['y'][i])) for i in range(S['n']))
            errs.append((N, d))
        ratios = [errs[i][1] / errs[i + 1][1] for i in range(len(errs) - 1)]
        row[nm] = dict(errs=errs, order=sum(math.log2(r) for r in ratios) / len(ratios))
    ORD2[key] = dict(T=T2, **row)
    P('  %-24s T = %.6f d   PEFRL order %.3f   PhET order %.3f'
      % (key, T2 / DAY, row['pefrl']['order'], row['phet']['order']))
for k, v in sorted(OT.items()):
    P('  order-sweep time for %-24s %.6f d' % (k, v / DAY))
REF['order_times'] = OT
REF['orders2'] = ORD2

# PhET's shipped step over its own frames, for the comparison panel
sc = scene('scale', 'starPlanet')          # re-bound: the blocks above walk every scene
S = st_of(sc)
Sp = st_of(sc)
dt = frame_dt(sc, 1)
E0, _, _ = energy(S)
for f in range(600):
    advance(S, dt)
    advance(Sp, dt, stepfn=phet_step)
Ep, _, _ = energy(Sp)
Eo, _, _ = energy(S)
dev = max(math.hypot(Sp['x'][i] - S['x'][i], Sp['y'][i] - S['y'][i]) for i in range(S['n']))
P('  after 600 frames (%.3f d): ours |dE/E| = %.3e, PhET\'s %.3e, the two runs differ by %.4e m'
  % (600 * dt / DAY, abs(Eo - E0) / abs(E0), abs(Ep - E0) / abs(E0), dev))
REF['shadow'] = dict(frames=600, t=600 * dt, dE_ours=abs(Eo - E0) / abs(E0),
                     dE_phet=abs(Ep - E0) / abs(E0), dev=dev)

# =====================================================================
#  8. what PhET's Model screen does on purpose
# =====================================================================
P()
P('# PhET\'s Model screen, measured')
mm = scene('model', 'starPlanetMoon')
ts = scene('scale', 'starPlanetMoon')
mo, pl = mm['bodies'][2], mm['bodies'][1]
rm_model = math.hypot(mo['x'] - pl['x'], mo['y'] - pl['y'])
rm_scale = math.hypot(ts['bodies'][2]['x'] - ts['bodies'][1]['x'],
                      ts['bodies'][2]['y'] - ts['bodies'][1]['y'])
vrel_model = math.hypot(mo['vx'] - pl['vx'], mo['vy'] - pl['vy'])
vc_plain = math.sqrt(G * PHET['EARTH_MASS'] / rm_model)
vc_boost = math.sqrt(PHET['MOON_BOOST'] * G * PHET['EARTH_MASS'] / rm_model)
P('  the drawn moon sits %.6e m from the planet, %.6f x its real %.6e m'
  % (rm_model, rm_model / rm_scale, rm_scale))
P('  its speed relative to the planet is %.4f m/s, %.4f x the real %.1f m/s'
  % (vrel_model, vrel_model / abs(PHET['MOON_VX']), abs(PHET['MOON_VX'])))
P('  a circular orbit there needs %.4f m/s with the plain pull, %.4f m/s with PhET\'s x%d boost'
  % (vc_plain, vc_boost, PHET['MOON_BOOST']))
P('  so the boost that would make it exactly circular is %.1f; PhET uses %d'
  % ((vrel_model / vc_plain) ** 2, PHET['MOON_BOOST']))
REF['modelmoon'] = dict(r=rm_model, r_true=rm_scale, rratio=rm_model / rm_scale,
                        v=vrel_model, vratio=vrel_model / abs(PHET['MOON_VX']),
                        vc_plain=vc_plain, vc_boost=vc_boost,
                        boost_for_circle=(vrel_model / vc_plain) ** 2,
                        boost=PHET['MOON_BOOST'])
# the third law is broken there: measure the momentum drift over a run
S = st_of(mm)
p0 = momentum(S)
pscale = float(np.sum(S['m'] * np.hypot(S['vx'], S['vy'])))
dt = frame_dt(mm, 1)
for f in range(600):
    advance(S, dt)
p1 = momentum(S)
P('  over 600 frames the Model Sun-Planet-Moon momentum moves by %.4e of p (the boost is one-sided)'
  % (math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / pscale))
REF['modelmoon']['dP600'] = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / pscale

P()
P('# the drawn sizes: what PhET\'s exaggerations amount to')
SZ = {}
for sid in SCENES:
    ms = scene('model', sid)
    ss = scene('scale', sid)
    row = []
    for i, b in enumerate(ms['bodies']):
        row.append(dict(name=b['name'], model=b['r'], scale=ss['bodies'][i]['r'],
                        factor=b['r'] / ss['bodies'][i]['r']))
    SZ[sid] = row
    P('  %-18s %s' % (sid, ', '.join('%s x%.6g' % (r['name'], r['factor']) for r in row)))
# and how many pixels a true-size body gets on the To Scale screen
P()
P('# to scale: how big the bodies really are at PhET\'s own zoom (987.5 x 772.5 stage)')
PX = {}
for sid in SCENES:
    ss = scene('scale', sid)
    s_view = PHET['VIEW_SCALE'] * ss['zoom']          # view units per metre at zoom level 1
    row = [dict(name=b['name'], px=2 * b['r'] * s_view) for b in ss['bodies']]
    PX[sid] = row
    P('  %-18s %s' % (sid, ', '.join('%s %.4g px across' % (r['name'], r['px']) for r in row)))
REF['sizes'] = SZ
REF['px'] = PX

# =====================================================================
#  the view window PhET uses, so the sim frames the same thing
# =====================================================================
P()
P('# the view window: half-height = STAGE_H / (2 x 1.5e-9 x zoom x level)')
VW = {}
for sid in SCENES:
    ss = scene('scale', sid)
    half = PHET['STAGE_H'] / (2 * PHET['VIEW_SCALE'] * ss['zoom'])
    VW[sid] = half
    P('  %-18s zoom %-8g half-height %.9e m = %.4f Earth radii' % (sid, ss['zoom'], half, half / PHET['EARTH_RADIUS']))
REF['window'] = VW

# =====================================================================
#  a brute-force cross-check of the Kepler solver
# =====================================================================
P()
P('# the Kepler solver against a brute-force inversion (bisection on 1e6 samples)')
worst = 0.0
for e in (0.0, 0.0167, 0.1, 0.5, 0.9, 0.99):
    for Mi in range(0, 13):
        M = Mi * math.pi / 6
        E = kepler_E(M, e)
        worst = max(worst, abs(E - e * math.sin(E) - M))
P('  worst residual |E - e sin E - M| over 78 cases = %.3e' % worst)
REF['kepler_resid'] = worst

# the period the long way: integrate until the body comes back to periapsis
P()
P('# the period of each two-body scene, measured from the integration (to scale)')
PER = {}
for sid in ('starPlanet', 'planetMoon', 'planetSatellite'):
    sc = scene('scale', sid)
    ref = two_body_ref(sc)
    el = ref['el']
    S = st_of(sc)
    dt = frame_dt(sc, 1)
    # the separation's angle about the centre of mass, unwrapped, to one full turn
    a, b = 0, 1
    th0 = math.atan2(S['y'][b] - S['y'][a], S['x'][b] - S['x'][a])
    tot = 0.0
    t = 0.0
    prev = th0
    hit = None
    while t < 3 * el['T']:
        advance(S, dt)
        t += dt
        th = math.atan2(S['y'][b] - S['y'][a], S['x'][b] - S['x'][a])
        d = th - prev
        while d > math.pi:
            d -= 2 * math.pi
        while d < -math.pi:
            d += 2 * math.pi
        tot += d
        prev = th
        if abs(tot) >= 2 * math.pi:
            # linear interpolation back to exactly one turn
            hit = t - dt * (abs(tot) - 2 * math.pi) / abs(d)
            break
    PER[sid] = dict(T_exact=el['T'], T_measured=hit, rel=abs(hit - el['T']) / el['T'])
    P('  %-18s Kepler T = %.9f d, measured from the run %.9f d, %.3e apart'
      % (sid, el['T'] / DAY, hit / DAY, abs(hit - el['T']) / el['T']))
REF['periods'] = PER


# =====================================================================
#  9. the circular-orbit view: what a different start speed does
# =====================================================================
P()
P('# start the Earth at f x the circular speed, everything else the same')
SWEEP = []
mu0 = G * PHET['SUN_MASS']
r0 = PHET['EARTH_X']
vc0 = math.sqrt(mu0 / r0)
for f in (0.4, 0.7, 1.0, 1.15, 1.3, math.sqrt(2), 1.5):
    el = conic(r0, 0.0, 0.0, f * vc0, mu0)
    row = dict(f=f, v=f * vc0, kind=el['kind'], e=el['e'], a=el['a'],
               T=el.get('T'), q=el['q'], Q=el.get('Q'), energy=el['energy'])
    SWEEP.append(row)
    P('  v = %.4f v_c = %10.3f m/s -> %-9s e = %.9f  a = %14.7e m  T = %s  q = %.6e'
      % (f, f * vc0, el['kind'], el['e'], el['a'],
         ('%.4f d' % (el['T'] / DAY)) if el['kind'] == 'ellipse' else 'infinite', el['q']))
P('  at f = 1 exactly: e = %.3e (a circle), a - r = %.3e m' % (SWEEP[2]['e'], SWEEP[2]['a'] - r0))
P('  at f = sqrt(2) exactly: the specific energy is %.6e (parabolic escape)'
  % conic(r0, 0.0, 0.0, math.sqrt(2) * vc0, mu0)['energy'])
REF['sweep'] = SWEEP

P()
P('# the mass sliders: PhET runs each one from half to double the body\'s own mass')
MASS = {}
for lab2, fac in (('half', 0.5), ('default', 1.0), ('double', 2.0)):
    sc = scene('scale', 'starPlanet')
    sc['bodies'][0]['m'] *= fac
    sc = centre(sc)
    ref = two_body_ref(sc)
    el = ref['el']
    MASS[lab2] = dict(fac=fac, m=sc['bodies'][0]['m'], mu=ref['mu'], a=el['a'], e=el['e'],
                      T=el['T'], Tdays=el['T'] / DAY, kind=el['kind'], vesc=el['vesc'])
    P('  star x%-8s mu = %.9e  %-9s a = %.9e m  e = %.9f  T = %s'
      % (lab2, ref['mu'], el['kind'], el['a'], el['e'],
         ('%.6f d' % (el['T'] / DAY)) if el['kind'] == 'ellipse' else 'infinite (unbound)'))
P('  halving the star leaves the Earth at %.6f of the escape speed there'
  % (PHET['EARTH_VY'] / math.sqrt(2 * G * 0.5 * PHET['SUN_MASS'] / PHET['EARTH_X'])))
REF['mass'] = MASS

P()
P('# PhET\'s orbits against the measured ones')
# the real Earth orbit from the fact sheet's own perihelion and max speed
mu_meas = MEAS['SUN_GM'] + MEAS['EARTH_GM']
el_meas = conic(MEAS['EARTH_PERI'], 0.0, 0.0, MEAS['EARTH_VMAX'], mu_meas)
P('  Earth year: PhET\'s numbers give %.6f d; the fact sheet\'s own perihelion and max speed give'
  % REF['two']['scale/starPlanet']['Tdays'])
P('              %.6f d; the fact sheet\'s sidereal orbit period is 365.256 d' % (el_meas['T'] / DAY))
mu_moon = G * (MEAS['EARTH_MASS'] + MEAS['MOON_MASS'])
el_moon = conic(MEAS['MOON_PERI'], 0.0, 0.0, MEAS['MOON_VMAX'], mu_moon)
P('  Moon month: PhET\'s numbers give %.6f d; perigee + max speed give %.6f d; the fact sheet\'s'
  % (REF['two']['scale/planetMoon']['Tdays'], el_moon['T'] / DAY))
P('              sidereal orbit period is 27.3217 d')
P('  ISS: PhET\'s orbit is %.4f min at %.3f km altitude; NASA says the real one is "about 90 minutes"'
  % (REF['two']['scale/planetSatellite']['T'] * DAY / 60 if False else
     REF['two']['scale/planetSatellite']['Tdays'] * 24 * 60,
     (PHET['STATION_X'] - PHET['EARTH_RADIUS']) / 1e3))
REF['vsmeas'] = dict(earth_phet=REF['two']['scale/starPlanet']['Tdays'],
                     earth_factsheet=el_meas['T'] / DAY, earth_sidereal=365.256,
                     moon_phet=REF['two']['scale/planetMoon']['Tdays'],
                     moon_factsheet=el_moon['T'] / DAY, moon_sidereal=27.3217,
                     iss_min=REF['two']['scale/planetSatellite']['Tdays'] * 1440,
                     iss_alt_km=(PHET['STATION_X'] - PHET['EARTH_RADIUS']) / 1e3)

P()
P('REFJSON ' + json.dumps(REF, sort_keys=True))

here = os.path.dirname(os.path.abspath(__file__))
io.open(os.path.join(here, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
sys.stderr.write('wrote refvals.txt (%d lines)\n' % len(OUT))
