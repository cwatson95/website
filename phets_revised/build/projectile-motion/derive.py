#!/usr/bin/env python3
"""derive.py — the Python twin and the reference values for projectile-motion.html.

Every number the JS selfTest asserts with a (derive) / (scipy) / (twin) label is
printed here.  Run it and read the output IN FULL (never through head/tail —
Known-bad: a value that never appeared in output you read is a guess):

    python3 derive.py > refvals.txt

What is independent of what:
  * VACUUM: closed forms (exact).  The integrator must reproduce them to
    rounding, because RK4 is exact on a quadratic-in-time trajectory.
  * DRAG, general angle: three routes that share no code —
      (a) the twin of the JS integrator (fixed-rule RK4, bisected events),
      (b) scipy solve_ivp DOP853 at rtol = atol = 1e-13, events polished by
          one Newton step,
      (c) the EXACT hodograph of quadratic drag, 1/u^2 = 1/u0^2 + (k/g)[F(th) - F(phi)],
          F(psi) = sin psi / cos^2 psi + ln tan(pi/4 + psi/2), with t, x, y as
          quadratures in the velocity angle phi (scipy quad) and the landing
          angle from brentq.
  * DRAG, vertical launch: closed forms (tan / tanh / ln cosh).
  * DRAG -> 0: the first-order perturbation dR/dk as a double integral
    (scipy quad), checked against Richardson differences of (b).
  * Air density: NASA Glenn's "Earth Atmosphere Model" (PhET's choice), with
    the ISA / US Standard Atmosphere 1976 printed beside it for comparison.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq, minimize_scalar

DEG = math.pi/180
PI = math.pi

# ---------------------------------------------------------------- PhET's values
G_EARTH = 9.81                     # ProjectileMotionConstants.GRAVITY_ON_EARTH
OBJECTS = [                        # ProjectileObjectType: name, mass kg, diameter m, drag coefficient
    ('cannonball', 17.6, 0.18, 0.47), ('tankShell', 42, 0.15, 0.06), ('golfBall', 0.05, 0.04, 0.25),
    ('baseball', 0.15, 0.07, 0.35), ('football', 0.41, 0.17, 0.05), ('pumpkin', 5, 0.37, 0.6),
    ('human', 70, 0.5, 0.6), ('piano', 400, 2.2, 1.2), ('car', 2000, 2, 0.55)]
CUSTOM = ('custom', 100, 1, 0.47)
SCREEN_OBJ = ('screen', 5, 0.8, 0.47)   # the Vectors and Drag screens' projectile

# ---------------------------------------------------------------- the air
def air_density(alt):
    """NASA GRC Earth Atmosphere Model, troposphere (PhET's calculateAirDensity)."""
    T = 15.04 - 0.00649*alt
    p = 101.29*math.pow((T + 273.1)/288.08, 5.256)
    return p/(0.2869*(T + 273.1))

def isa_density(alt):
    """ISA / US Standard Atmosphere 1976 troposphere, for comparison only."""
    T0, L, p0, R, g0 = 288.15, 0.0065, 101325.0, 287.05287, 9.80665
    T = T0 - L*alt
    return p0*math.pow(T/T0, g0/(R*L))/(R*T)

def drag_k(m, d, cd, rho):
    return rho*cd*(PI*d*d/4)/(2*m)

# ---------------------------------------------------------------- the twin (mirrors p2_physics.js)
H_MAX, C_STEP, N_BIS, DOT = 0.002, 0.005, 60, 0.1

def rk4s(s, h, g, k):
    x, y, vx, vy, w = s
    sp = math.sqrt(vx*vx + vy*vy); kd = k*sp
    a1 = -kd*vx; b1 = -g - kd*vy; p1 = kd*sp*sp
    vx2 = vx + 0.5*h*a1; vy2 = vy + 0.5*h*b1
    sp = math.sqrt(vx2*vx2 + vy2*vy2); kd = k*sp
    a2 = -kd*vx2; b2 = -g - kd*vy2; p2 = kd*sp*sp
    vx3 = vx + 0.5*h*a2; vy3 = vy + 0.5*h*b2
    sp = math.sqrt(vx3*vx3 + vy3*vy3); kd = k*sp
    a3 = -kd*vx3; b3 = -g - kd*vy3; p3 = kd*sp*sp
    vx4 = vx + h*a3; vy4 = vy + h*b3
    sp = math.sqrt(vx4*vx4 + vy4*vy4); kd = k*sp
    a4 = -kd*vx4; b4 = -g - kd*vy4; p4 = kd*sp*sp
    return [x + h/6*(vx + 2*vx2 + 2*vx3 + vx4), y + h/6*(vy + 2*vy2 + 2*vy3 + vy4),
            vx + h/6*(a1 + 2*a2 + 2*a3 + a4), vy + h/6*(b1 + 2*b2 + 2*b3 + b4),
            w + h/6*(p1 + 2*p2 + 2*p3 + p4)]

def flight(h0, thd, v0, g, k, start=None, cliff=False, tEnd=None):
    """Twin of flight() in p2_physics.js: the same steps, the same bisections."""
    if start is not None:
        t = start[0]; s = list(start[1:])
    else:
        th = thd*DEG; t = 0.0; s = [0.0, h0, v0*math.cos(th), v0*math.sin(th), 0.0]
    T = [t]; S = [s[:]]; dots = []; apex = None; land = None; steps = 0
    if abs(t/DOT - round(t/DOT)) < 1e-9: dots.append(0)
    nd = math.floor(t/DOT + 1e-9) + 1
    if (not cliff) and s[1] <= 0 and s[3] <= 0:
        land = (t, s[:])
        return dict(T=T, S=S, dots=dots, apex=apex, land=land, steps=steps)
    while True:
        hh = H_MAX
        if k > 0:
            sp = math.sqrt(s[2]*s[2] + s[3]*s[3])
            if k*sp*hh > C_STEP: hh = C_STEP/(k*sp)
        tD = nd*DOT; hit = False
        if t + hh > tD - 1e-9: hh = tD - t; hit = True
        ns = rk4s(s, hh, g, k); steps += 1
        if s[3] > 0 and ns[3] <= 0:
            lo, hi = 0.0, hh
            for _ in range(N_BIS):
                m = 0.5*(lo + hi)
                if rk4s(s, m, g, k)[3] > 0: lo = m
                else: hi = m
            a = rk4s(s, hi, g, k)
            apex = (t + hi, a)
            T.append(t + hi); S.append(a)
        if land is None and ns[1] <= 0 and (s[1] > 0 or s[3] > 0):
            lo, hi = 0.0, hh
            for _ in range(N_BIS):
                m = 0.5*(lo + hi)
                if rk4s(s, m, g, k)[1] > 0: lo = m
                else: hi = m
            L = rk4s(s, hi, g, k); L[1] = 0.0
            land = (t + hi, L)
            if not cliff:
                T.append(t + hi); S.append(L)
                return dict(T=T, S=S, dots=dots, apex=apex, land=land, steps=steps)
        s = ns
        if hit:
            t = tD; nd += 1
        else:
            t = t + hh
        T.append(t); S.append(s[:])
        if hit: dots.append(len(T) - 1)
        if cliff and hit and t >= tEnd - 1e-9:
            return dict(T=T, S=S, dots=dots, apex=apex, land=land, steps=steps)

def summary(F):
    tL, L = F['land']
    return dict(T=tL, R=L[0], vxL=L[2], vyL=L[3], vL=math.sqrt(L[2]*L[2] + L[3]*L[3]),
                angL=math.atan2(-L[3], L[2])/DEG, W=L[4],
                ta=F['apex'][0] if F['apex'] else None, xa=F['apex'][1][0] if F['apex'] else None,
                H=F['apex'][1][1] if F['apex'] else F['S'][0][1], steps=F['steps'])

def state_at(F, t):
    for i, ti in enumerate(F['T']):
        if abs(ti - t) < 1e-12: return F['S'][i]
    return None

# ---------------------------------------------------------------- scipy reference (independent)
def ref_ivp(h0, thd, v0, g, k, tmax=400):
    th = thd*DEG
    def f(t, s):
        sp = math.hypot(s[2], s[3])
        return [s[2], s[3], -k*sp*s[2], -g - k*sp*s[3], k*sp**3]
    def ground(t, s): return s[1]
    ground.terminal = True; ground.direction = -1
    def apexev(t, s): return s[3]
    apexev.direction = -1
    y0 = [0, h0, v0*math.cos(th), v0*math.sin(th), 0]
    if h0 <= 0 and y0[3] <= 0:
        return dict(T=0.0, R=0.0, vL=v0, angL=None, H=h0, ta=None, xa=None, W=0.0)
    sol = solve_ivp(f, [0, tmax], y0, method='DOP853', rtol=1e-13, atol=1e-13,
                    events=[ground, apexev], dense_output=True)
    tL = sol.t_events[0][0]; sL = sol.y_events[0][0]
    tL2 = tL - sL[1]/sL[3]                       # one Newton step on y(t) = 0
    d = f(tL, sL)
    R = sL[0] + d[0]*(tL2 - tL); vx = sL[2] + d[2]*(tL2 - tL); vy = sL[3] + d[3]*(tL2 - tL)
    out = dict(T=tL2, R=R, vL=math.hypot(vx, vy), angL=math.atan2(-vy, vx)/DEG, W=sL[4] + d[4]*(tL2 - tL))
    if len(sol.t_events[1]):
        ta = sol.t_events[1][0]; sa = sol.y_events[1][0]
        da = f(ta, sa); ta2 = ta - sa[3]/da[3]
        out.update(ta=ta2, xa=sa[0] + sa[2]*(ta2 - ta), H=sa[1] + sa[3]*(ta2 - ta))
    else:
        out.update(ta=None, xa=None, H=h0)
    return out

# ---------------------------------------------------------------- the exact hodograph (independent)
def hodoF(psi):
    c = math.cos(psi)
    return math.sin(psi)/(c*c) + math.log(math.tan(PI/4 + psi/2))

def hodo_u(phi, th, u0, g, k):
    return u0/math.sqrt(1 + k*u0*u0/g*(hodoF(th) - hodoF(phi)))

def hodo_txy(phi, th, v0, h0, g, k):
    u0 = v0*math.cos(th)
    it = quad(lambda p: hodo_u(p, th, u0, g, k)/math.cos(p)**2, phi, th, epsabs=0, epsrel=2e-14, limit=400)[0]/g
    ix = quad(lambda p: hodo_u(p, th, u0, g, k)**2/math.cos(p)**2, phi, th, epsabs=0, epsrel=2e-14, limit=400)[0]/g
    iy = quad(lambda p: hodo_u(p, th, u0, g, k)**2*math.tan(p)/math.cos(p)**2, phi, th, epsabs=0, epsrel=2e-14, limit=400)[0]/g
    return it, ix, h0 + iy

def hodo_landing(h0, thd, v0, g, k):
    th = thd*DEG
    phiL = brentq(lambda p: hodo_txy(p, th, v0, h0, g, k)[2], -PI/2 + 1e-9, min(th, 0.0) - (1e-15 if th <= 0 else 0),
                  xtol=1e-15, rtol=9e-16, maxiter=300)
    t, x, y = hodo_txy(phiL, th, v0, h0, g, k)
    u = hodo_u(phiL, th, v0*math.cos(th), g, k)
    return dict(phiL=phiL/DEG, T=t, R=x, vL=u/math.cos(phiL))

def hodo_apex(h0, thd, v0, g, k):
    th = thd*DEG
    t, x, y = hodo_txy(0.0, th, v0, h0, g, k)
    return dict(ta=t, xa=x, H=y, ua=hodo_u(0.0, th, v0*math.cos(th), g, k))

# ---------------------------------------------------------------- vacuum closed forms
def vacuum(h0, thd, v0, g):
    th = thd*DEG; u = v0*math.cos(th); w = v0*math.sin(th)
    T = 0.0 if (h0 <= 0 and w <= 0) else (w + math.sqrt(w*w + 2*g*h0))/g
    R = u*T; vy = w - g*T
    out = dict(T=T, R=R, vL=math.hypot(u, vy), angL=math.atan2(-vy, u)/DEG)
    if w > 0: out.update(ta=w/g, xa=u*w/g, H=h0 + w*w/(2*g))
    else: out.update(ta=None, xa=None, H=h0)
    return out

# ---------------------------------------------------------------- printing helpers
def P(label, v):
    if v is None: print('%-58s  None' % label)
    elif isinstance(v, (int,)) and not isinstance(v, bool): print('%-58s  %d' % (label, v))
    else: print('%-58s  %.13g' % (label, v))

def main():
    print('=== 0. PhET\'s values (projectile-motion_en.html 1.0.34) ===')
    for nm, m, d, cd in OBJECTS + [CUSTOM, SCREEN_OBJ]:
        print('  %-11s m = %-6g kg  d = %-5g m  Cd = %g' % (nm, m, d, cd))
    print()
    print('=== 1. air density: NASA GRC fit (PhET) vs ISA 1976 ===')
    for alt in [0, 100, 1000, 2500, 5000]:
        P('rho_nasa(%d m)' % alt, air_density(alt))
        P('rho_isa(%d m)' % alt, isa_density(alt))
        P('  nasa/isa - 1 at %d m' % alt, air_density(alt)/isa_density(alt) - 1)
    print()
    rho0 = air_density(0)
    print('=== 2. drag constants and terminal speeds at sea level (g = 9.81) ===')
    for nm, m, d, cd in OBJECTS + [CUSTOM, SCREEN_OBJ]:
        k = drag_k(m, d, cd, rho0)
        P('k[%s] (1/m)' % nm, k)
        P('v_t[%s] = sqrt(2mg/(rho Cd A)) (m/s)' % nm, math.sqrt(2*m*G_EARTH/(rho0*cd*PI*d*d/4)))
    k5000 = drag_k(5, 0.8, 0.47, air_density(5000))
    P('k[screen] at 5000 m', k5000); P('v_t[screen] at 5000 m', math.sqrt(G_EARTH/k5000))
    print()

    print('=== 3. vacuum closed forms ===')
    VAC = [(10, 0, 15, 9.81), (0, 45, 30, 9.81), (15, 80, 30, 20), (0, 80, 18, 9.81), (5, -30, 20, 5),
           (15, 90, 12, 9.81), (7, -90, 4, 9.81), (0, 30, 0, 9.81), (12, 0, 0, 9.81), (0, -20, 10, 9.81), (15, 38.5, 25, 9.81)]
    for c in VAC:
        v = vacuum(*c)
        tag = 'vac h=%g th=%g v0=%g g=%g' % c
        for key in ['T', 'R', 'H', 'ta', 'xa', 'vL', 'angL']: P(tag + ' ' + key, v[key])
    for (h0, v0, g) in [(0, 18, 9.81), (10, 15, 9.81), (15, 30, 5)]:
        s = math.sqrt(v0*v0 + 2*g*h0)
        P('vac optimum angle (deg) h=%g v0=%g g=%g' % (h0, v0, g), math.atan2(v0, s)/DEG)
        P('vac max range h=%g v0=%g g=%g' % (h0, v0, g), v0*s/g)
    print()

    print('=== 4. the twin (JS integrator) vs scipy DOP853 vs the exact hodograph ===')
    CASES = []
    for nm, m, d, cd in OBJECTS:
        k = drag_k(m, d, cd, rho0)
        CASES.append(('intro ' + nm, 10, 0, 15, 9.81, k))
    for nm, m, d, cd in OBJECTS:
        k = drag_k(m, d, cd, rho0)
        CASES.append(('45deg ' + nm, 0, 45, 25, 9.81, k))
    CASES += [
        ('drag default', 0, 80, 18, 9.81, drag_k(5, 0.8, 0.47, rho0)),
        ('drag default 5000 m', 0, 80, 18, 9.81, drag_k(5, 0.8, 0.47, air_density(5000))),
        ('lab custom g=5', 3, 35, 22, 5, drag_k(100, 1, 0.47, rho0)),
        ('lab custom g=20', 3, 35, 22, 20, drag_k(100, 1, 0.47, rho0)),
        ('extreme m=1 d=3 Cd=1 g=20', 15, 60, 30, 20, drag_k(1, 3, 1, rho0)),
        ('down -30 pumpkin', 5, -30, 20, 9.81, drag_k(5, 0.37, 0.6, rho0)),
        ('analysis baseball 45 30', 0, 45, 30, 9.81, drag_k(0.15, 0.07, 0.35, rho0)),
    ]
    worst = 0
    for (tag, h0, thd, v0, g, k) in CASES:
        F = flight(h0, thd, v0, g, k); A = summary(F); B = ref_ivp(h0, thd, v0, g, k)
        for key in ['T', 'R', 'H', 'ta', 'xa', 'vL', 'angL', 'W']:
            P('twin ' + tag + ' ' + key, A[key])
        P('twin ' + tag + ' steps', A['steps'])
        s05 = state_at(F, 0.5)
        if s05 is not None:
            P('twin ' + tag + ' x(0.5 s)', s05[0]); P('twin ' + tag + ' y(0.5 s)', s05[1])
            P('twin ' + tag + ' vx(0.5 s)', s05[2]); P('twin ' + tag + ' vy(0.5 s)', s05[3])
        for key in ['T', 'R', 'H', 'vL', 'angL', 'W']:
            P('scipy ' + tag + ' ' + key, B[key])
        if B['ta'] is not None:
            P('scipy ' + tag + ' ta', B['ta']); P('scipy ' + tag + ' xa', B['xa'])
        e = max(abs(A['R'] - B['R'])/max(abs(B['R']), 1e-12), abs(A['T'] - B['T'])/B['T'], abs(A['H'] - B['H'])/B['H'],
                abs(A['vL'] - B['vL'])/B['vL'])
        worst = max(worst, e)
        P('  twin-vs-scipy worst rel err ' + tag, e)
    P('WORST twin-vs-scipy relative error over section 4', worst)
    print()

    print('=== 5. the exact hodograph (quad + brentq) vs scipy DOP853 ===')
    HCASES = [('drag default', 0, 80, 18, 9.81, drag_k(5, 0.8, 0.47, rho0)),
              ('45deg pumpkin', 0, 45, 25, 9.81, drag_k(5, 0.37, 0.6, rho0)),
              ('45deg baseball', 0, 45, 25, 9.81, drag_k(0.15, 0.07, 0.35, rho0)),
              ('lab custom g=5', 3, 35, 22, 5, drag_k(100, 1, 0.47, rho0)),
              ('down -30 pumpkin', 5, -30, 20, 9.81, drag_k(5, 0.37, 0.6, rho0)),
              ('intro golfBall', 10, 0.0, 15, 9.81, drag_k(0.05, 0.04, 0.25, rho0))]
    hworst = 0
    for (tag, h0, thd, v0, g, k) in HCASES:
        Hl = hodo_landing(h0, thd, v0, g, k); B = ref_ivp(h0, thd, v0, g, k)
        P('hodo ' + tag + ' T', Hl['T']); P('hodo ' + tag + ' R', Hl['R']); P('hodo ' + tag + ' vL', Hl['vL'])
        P('hodo ' + tag + ' landing angle (deg)', -Hl['phiL'])
        e = max(abs(Hl['T'] - B['T'])/B['T'], abs(Hl['R'] - B['R'])/B['R'], abs(Hl['vL'] - B['vL'])/B['vL'])
        if thd > 0:
            Ha = hodo_apex(h0, thd, v0, g, k)
            P('hodo ' + tag + ' ta', Ha['ta']); P('hodo ' + tag + ' xa', Ha['xa']); P('hodo ' + tag + ' H', Ha['H'])
            P('hodo ' + tag + ' u at apex', Ha['ua'])
            e = max(e, abs(Ha['ta'] - B['ta'])/B['ta'], abs(Ha['H'] - B['H'])/B['H'], abs(Ha['xa'] - B['xa'])/B['xa'])
        hworst = max(hworst, e)
        P('  hodograph-vs-scipy worst rel err ' + tag, e)
    P('WORST hodograph-vs-scipy relative error (the reference itself)', hworst)
    # the hodograph at fixed angles along the drag default, for the in-page GL route
    th = 80*DEG; k = drag_k(5, 0.8, 0.47, rho0)
    for phd in [60, 30, 0, -30, -60]:
        t, x, y = hodo_txy(phd*DEG, th, 18, 0, 9.81, k)
        u = hodo_u(phd*DEG, th, 18*math.cos(th), 9.81, k)
        P('hodo drag-default phi=%d t' % phd, t); P('hodo drag-default phi=%d x' % phd, x)
        P('hodo drag-default phi=%d y' % phd, y); P('hodo drag-default phi=%d u' % phd, u)
    print()

    print('=== 6. vertical launches with drag: closed forms ===')
    for (tag, m, d, cd, h0, v0, g) in [('screen obj up 18', 5, 0.8, 0.47, 0, 18, 9.81), ('pumpkin up 30 from 15', 5, 0.37, 0.6, 15, 30, 9.81),
                                        ('human up 20 from 5, g=5', 70, 0.5, 0.6, 5, 20, 5)]:
        k = drag_k(m, d, cd, rho0); vt = math.sqrt(g/k)
        ta = vt/g*math.atan(v0/vt); Hh = h0 + vt*vt/(2*g)*math.log(1 + v0*v0/(vt*vt))
        tf = vt/g*math.acosh(math.exp(g*Hh/(vt*vt))); vL = vt*math.sqrt(1 - math.exp(-2*g*Hh/(vt*vt)))
        P('vertical ' + tag + ' v_t', vt); P('vertical ' + tag + ' t_apex', ta); P('vertical ' + tag + ' H', Hh)
        P('vertical ' + tag + ' T', ta + tf); P('vertical ' + tag + ' v_land', vL)
        F = flight(h0, 90, v0, g, k); A = summary(F)
        P('  twin ' + tag + ' T', A['T']); P('  twin ' + tag + ' H', A['H']); P('  twin ' + tag + ' vL', A['vL'])
        P('  twin-vs-closed rel err T ' + tag, abs(A['T'] - (ta + tf))/(ta + tf))
    # a drop from rest: v(t) = -v_t tanh(g t/v_t), y = h - (v_t^2/g) ln cosh(g t/v_t)
    k = drag_k(5, 0.8, 0.47, rho0); vt = math.sqrt(9.81/k)
    for t in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
        P('drop screen obj v(%g s)' % t, -vt*math.tanh(9.81*t/vt))
        P('drop screen obj fall(%g s)' % t, vt*vt/9.81*math.log(math.cosh(9.81*t/vt)))
    F = flight(0, -90, 0, 9.81, k, cliff=True, tEnd=20.0)
    s20 = state_at(F, 20.0); s1 = state_at(F, 1.0)
    P('  twin drop (cliff) vy(1 s)', s1[3]); P('  twin drop (cliff) y(1 s)', s1[1])
    P('  twin drop (cliff) vy(20 s)', s20[3]); P('  twin drop (cliff) y(20 s)', s20[1])
    P('  twin drop (cliff) |vy(20)|/v_t - 1', abs(s20[3])/vt - 1)
    print()

    print('=== 7. drag -> 0: the first-order range correction dR/dk ===')
    for (h0, thd, v0, g) in [(0, 45, 25, 9.81), (10, 0, 15, 9.81), (15, 60, 20, 9.81)]:
        th = thd*DEG; u = v0*math.cos(th); w = v0*math.sin(th)
        T0 = (w + math.sqrt(w*w + 2*g*h0))/g
        spd = lambda s: math.sqrt(u*u + (w - g*s)**2)
        x1 = -u*quad(lambda s: (T0 - s)*spd(s), 0, T0, epsabs=0, epsrel=2e-14)[0]
        y1 = -quad(lambda s: (T0 - s)*spd(s)*(w - g*s), 0, T0, epsabs=0, epsrel=2e-14)[0]
        dRdk = x1 - u*y1/(w - g*T0)
        P('dR/dk at k=0 (perturbation quad) h=%g th=%g v0=%g' % (h0, thd, v0), dRdk)
        R0 = vacuum(h0, thd, v0, g)['R']
        e1 = 1e-4; e2 = 5e-5
        r1 = (ref_ivp(h0, thd, v0, g, e1)['R'] - R0)/e1; r2 = (ref_ivp(h0, thd, v0, g, e2)['R'] - R0)/e2
        P('  Richardson 2*r(k/2)-r(k) from scipy h=%g th=%g v0=%g' % (h0, thd, v0), 2*r2 - r1)
        P('  twin (R(1e-4)-R0)/1e-4 h=%g th=%g v0=%g' % (h0, thd, v0), (summary(flight(h0, thd, v0, g, 1e-4))['R'] - R0)/1e-4)
        P('  twin (R(1e-5)-R0)/1e-5 h=%g th=%g v0=%g' % (h0, thd, v0), (summary(flight(h0, thd, v0, g, 1e-5))['R'] - R0)/1e-5)
    print()

    print('=== 8. the optimum angle with drag (minimize_scalar on scipy ranges) ===')
    for (tag, h0, v0, g, k) in [('baseball v0=30', 0, 30, 9.81, drag_k(0.15, 0.07, 0.35, rho0)),
                                 ('golfBall v0=30', 0, 30, 9.81, drag_k(0.05, 0.04, 0.25, rho0)),
                                 ('drag default v0=18', 0, 18, 9.81, drag_k(5, 0.8, 0.47, rho0)),
                                 ('pumpkin from 10 v0=15', 10, 15, 9.81, drag_k(5, 0.37, 0.6, rho0))]:
        res = minimize_scalar(lambda a: -ref_ivp(h0, a, v0, g, k)['R'], bounds=(1, 89), method='bounded',
                              options=dict(xatol=1e-7))
        P('optimum ' + tag + ' angle (deg)', res.x); P('optimum ' + tag + ' range', -res.fun)
        s = math.sqrt(v0*v0 + 2*g*h0)
        P('  vacuum optimum ' + tag, math.atan2(v0, s)/DEG)
        # the JS golden section runs on the twin; print the twin range at the scipy optimum
        P('  twin range at that angle ' + tag, summary(flight(h0, res.x, v0, g, k))['R'])
    print()

    print('=== 9. the vacuum envelope (tangency) ===')
    h0, v0, g = 4, 16, 9.81
    for x in [5, 10, 20, 28]:
        tanth = v0*v0/(g*x); thd = math.atan(tanth)/DEG
        y = h0 + x*tanth - g*x*x*(1 + tanth*tanth)/(2*v0*v0)
        P('envelope x=%g: tangent angle (deg)' % x, thd); P('envelope x=%g: y_env' % x, h0 + v0*v0/(2*g) - g*x*x/(2*v0*v0))
        P('envelope x=%g: y(x; tangent angle)' % x, y)
    print()

    print('=== 10. a mid-air change: drag switched off at a node, the rest is a parabola ===')
    k = drag_k(5, 0.8, 0.47, rho0)
    F = flight(0, 80, 18, 9.81, k)
    i = F['dots'][8]; tn = F['T'][i]; sn = F['S'][i]
    P('node t', tn); P('node x', sn[0]); P('node y', sn[1]); P('node vx', sn[2]); P('node vy', sn[3])
    G = flight(0, 0, 0, 9.81, 0.0, start=[tn] + sn)
    A = summary(G)
    tl = (sn[3] + math.sqrt(sn[3]**2 + 2*9.81*sn[1]))/9.81
    P('continuation (vacuum) landing time', A['T']); P('closed form from the node', tn + tl)
    P('continuation range', A['R']); P('closed form range', sn[0] + sn[2]*tl)
    G2 = flight(0, 0, 0, 5.0, k, start=[tn] + sn)
    P('continuation (gravity 5) landing time', summary(G2)['T']); P('continuation (gravity 5) range', summary(G2)['R'])
    print()

    print('=== 12. Gauss-Legendre 10-point (numpy leggauss), for the in-page Newton construction ===')
    xs, ws = np.polynomial.legendre.leggauss(10)
    for i in range(10):
        P('GL10 node %d' % i, float(xs[9 - i])); P('GL10 weight %d' % i, float(ws[9 - i]))
    print()

    print('=== 11. PhET\'s own scheme (25 ms, a evaluated at the previous point) for the drag default ===')
    k = drag_k(5, 0.8, 0.47, rho0); dt = 0.025
    x, y, vx, vy = 0.0, 0.0, 18*math.cos(80*DEG), 18*math.sin(80*DEG); t = 0.0
    def acc(vx, vy):
        sp = math.hypot(vx, vy); return -k*sp*vx, -9.81 - k*sp*vy
    ax, ay = acc(vx, vy)
    while True:
        nx = x + vx*dt + 0.5*ax*dt*dt; ny = y + vy*dt + 0.5*ay*dt*dt
        nvx = vx + ax*dt; nvy = vy + ay*dt
        if ny <= 0:
            tg = (-math.sqrt(vy*vy - 2*ay*y) - vy)/ay
            R = x + vx*tg + 0.5*ax*tg*tg; t += tg
            break
        x, y, vx, vy = nx, ny, nvx, nvy; t += dt; ax, ay = acc(vx, vy)
    B = ref_ivp(0, 80, 18, 9.81, k)
    P('PhET scheme range', R); P('PhET scheme time', t); P('exact range', B['R']); P('exact time', B['T'])
    P('PhET scheme range error (rel)', R/B['R'] - 1)

if __name__ == '__main__':
    main()
