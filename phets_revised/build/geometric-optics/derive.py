#!/usr/bin/env python3
"""The Python twin of docs/phets_revised/geometric-optics.html.

Re-derives every closed form the sim implements and prints reference values to
17 significant figures for selfTest() to assert against.  Nothing here is
copied from the JavaScript: the formulas are written from the definitions, and
anything computed cleverly is cross-checked against a brute-force route
(a bisection, a quadrature, or an independent implementation).

Conventions used throughout (the same ones the page states):

    x runs to the RIGHT, the optic sits at x = 0, the object is always at
    x < 0, and y is measured from the optical axis, positive up.

    d_o = -x_object  > 0                      object distance
    f   > 0 converging (convex lens, concave mirror)
        < 0 diverging  (concave lens, convex mirror)
    d_i > 0 real image, < 0 virtual image.  A lens puts a real image at
        x = +d_i, a mirror at x = -d_i (PhET's `sign` = +1 / -1).
    m   = -d_i/d_o  (negative => inverted)
    R   > 0 convex optic, < 0 concave optic (PhET's sign convention)

Run:  python3 derive.py > refvals.txt
"""
import math
import sys

try:
    import numpy as np
    from scipy.optimize import brentq, minimize_scalar
    HAVE_SCIPY = True
except Exception:                                    # pragma: no cover
    HAVE_SCIPY = False

G = lambda x: repr(float(x))                          # 17 sig figs, round-trip


def head(t):
    print('\n' + '=' * 72)
    print(t)
    print('=' * 72)


# ============================================================================
#  PhET's own constants, read out of docs/phets/geometric-optics_en.html
#  (build 1.3.16).  Every one of these is quoted in the page as "PhET's value".
# ============================================================================
PHET = dict(
    f_lens=(40.0, 120.0, 80.0),        # fRangeLens      min, max, default  (cm)
    roc_lens=(40.0, 120.0, 80.0),      # rocRangeLens
    ior_lens=(1.2, 1.8, 1.5),          # iorRangeLens
    d_lens=(60.0, 120.0, 80.0),        # dRangeLens
    f_mirror=(75.0, 150.0, 90.0),      # fRangeMirror
    roc_mirror=(150.0, 300.0, 180.0),  # rocRangeMirror
    d_mirror=(60.0, 120.0, 80.0),      # dRangeMirror
    ior_direct_lens=1.5,               # new Xg(1.5,1.5,1.5)
    ior_mirror=2.0,                    # Vm = new Xg(2,2,2)
    flat_f=1e5,                        # flat mirror focal length, cm
    flat_R=2e5,                        # flat mirror radius, cm
    min_object_to_optic=40.0,          # GOConstants.MIN_DISTANCE_FROM_OBJECT_TO_OPTIC
    min_optic_to_screen=60.0,          # ...MIN_DISTANCE_FROM_OPTIC_TO_PROJECTION_SCREEN
    max_object_off_axis=100.0,         # ...MAX_DISTANCE_FROM_OBJECT_TO_OPTICAL_AXIS
    framed_object_lens=(-170.0, 27.0),
    framed_object_mirror=(-150.0, 72.5),
    arrow1_lens=(-160.0, 60.0), arrow2_lens=(-125.0, 30.0),
    arrow1_mirror=(-150.0, 60.0), arrow2_mirror=(-165.0, 30.0),
    light1=(-170.0, 20.0), light2=(-124.0, -20.0),
    second_point_offset=-56.5,         # SecondPoint.VERTICAL_OFFSET_RANGE.min
    screen_x=200.0, screen_height=123.0,
    many_fan_deg=120.0,                # LightRays: Tm = toRadians(120)
    arrow_max=80.0,                    # ArrowObject.MAX_MAGNITUDE
    ruler_h=260.0, ruler_v=160.0,
)


# ============================================================================
#  1.  The thin-lens / mirror equation, exactly
# ============================================================================
def image_distance(f, do):
    """1/d_o + 1/d_i = 1/f  solved for d_i.  d_o = f is the singular case."""
    if do == f:
        return math.inf
    return f * do / (do - f)


def magnification(f, do):
    di = image_distance(f, do)
    if do == 0:
        return 1.0
    if math.isinf(di):
        return math.copysign(math.inf, -di / 1.0) if di > 0 else math.inf
    return -di / do


def image_point(kind, f, do, yo):
    """(x, y) of the image.  kind = 'lens' -> sign +1, 'mirror' -> sign -1."""
    sign = 1.0 if kind == 'lens' else -1.0
    di = image_distance(f, do)
    m = -di / do
    return (sign * di, m * yo)


def residual(f, do, di):
    """The defining equation's residual, 1/d_o + 1/d_i - 1/f."""
    return 1.0 / do + 1.0 / di - 1.0 / f


# ============================================================================
#  2.  Ray transfer through an ideal thin optic
#
#  A ray leaving the object point (-d_o, y_o) and crossing the optic plane at
#  height h has incoming transverse slope u = (h - y_o)/d_o.  The ideal thin
#  optic turns it into u' = u - h/f, where u' is measured along the OUTGOING
#  direction of travel (+x for a lens, -x for a mirror).  That one line is the
#  whole of paraxial ray optics, and it never blows up -- not even at d_o = f,
#  where the image is at infinity.
# ============================================================================
def out_slope(f, do, yo, h):
    return (h - yo) / do - h / f


def bend(u, h, f):
    """The whole of paraxial ray optics, in one line."""
    return u - h / f


def ray_y_at(f, do, yo, h, s):
    """Height of the OUTGOING ray at signed path length s from the optic
    (s < 0 is the backward extension, which is where a virtual image lives)."""
    return h + out_slope(f, do, yo, h) * s


def ray_target(kind, f, do, yo, h):
    """Where the outgoing ray is aimed: the point it passes through (real) or
    appears to come from (virtual).  Computed from the image point, i.e. by the
    OTHER route, so the two can be asserted against each other."""
    xi, yi = image_point(kind, f, do, yo)
    return (xi, yi)


def ray_out_point(kind, f, do, yo, h, s):
    """The outgoing ray at path length s from the optic, from the slope law."""
    sign = 1.0 if kind == 'lens' else -1.0
    u = out_slope(f, do, yo, h)
    return (sign * s, h + u * s)


def ray_from_image(kind, f, do, yo, h, s):
    """The same outgoing ray, built instead by aiming at the image point."""
    sign = 1.0 if kind == 'lens' else -1.0
    xi, yi = image_point(kind, f, do, yo)
    di = image_distance(f, do)
    # direction from (0,h) to the image, reversed when the image is virtual
    dx, dy = xi - 0.0, yi - h
    if di < 0:                       # virtual: the ray diverges FROM the image
        dx, dy = -dx, -dy
    L = math.hypot(dx, dy)
    dx, dy = dx / L, dy / L
    # travel a horizontal distance s
    t = s / abs(dx)
    return (sign * s, h + dy * t * (1.0 if dx * sign > 0 else -1.0))


# ----- the three principal rays, and where they meet ------------------------
def principal_rays(kind, f, do, yo):
    """Returns three (h, u') pairs: the parallel ray, the chief ray through the
    centre, and the ray through the near focal point."""
    rays = []
    h1 = yo                                   # parallel to the axis
    rays.append((h1, out_slope(f, do, yo, h1)))
    h2 = 0.0                                  # through the centre, undeviated
    rays.append((h2, out_slope(f, do, yo, h2)))
    # through the front focal point F at x = -f: the ray from (-d_o, y_o) that
    # crosses y = 0 at x = -f.  Its height at the optic is
    #     h = y_o * (1 - d_o/(d_o - f)) ... derive directly:
    # parameterise x from -d_o; the ray hits y = 0 at x = -f, so the slope is
    # (0 - y_o)/(-f + d_o) and h = y_o + slope*d_o.
    if do != f:
        slope = -yo / (do - f)
        h3 = yo + slope * do
        rays.append((h3, out_slope(f, do, yo, h3)))
    return rays


def ray_cross(kind, r1, r2):
    """Intersection of two outgoing rays, in (x, y) with the outgoing sense
    already folded in."""
    sign = 1.0 if kind == 'lens' else -1.0
    (h1, u1), (h2, u2) = r1, r2
    if u1 == u2:
        return (math.inf, math.inf)
    s = (h2 - h1) / (u1 - u2)                 # path length from the optic
    return (sign * s, h1 + u1 * s)


# ============================================================================
#  3.  The lens maker's equation, and PhET's use of it
# ============================================================================
def f_thin(n, R1, R2):
    """1/f = (n-1)(1/R1 - 1/R2), the thin-lens maker's equation."""
    i1 = 0.0 if (R1 == 0 or math.isinf(R1)) else 1.0 / R1
    i2 = 0.0 if (R2 == 0 or math.isinf(R2)) else 1.0 / R2
    return 1.0 / ((n - 1.0) * (i1 - i2))


def f_thick(n, R1, R2, t):
    """The thick form, which carries the (n-1)t/(n R1 R2) term."""
    i1 = 0.0 if (R1 == 0 or math.isinf(R1)) else 1.0 / R1
    i2 = 0.0 if (R2 == 0 or math.isinf(R2)) else 1.0 / R2
    return 1.0 / ((n - 1.0) * (i1 - i2 + (n - 1.0) * t * i1 * i2 / n))


def bfd(n, R1, R2, t):
    """Back focal distance, from the rear vertex."""
    f = f_thick(n, R1, R2, t)
    i1 = 0.0 if (R1 == 0 or math.isinf(R1)) else 1.0 / R1
    return f * (1.0 - (n - 1.0) * t * i1 / n)


def phet_f_of_R(R, n):
    """PhET's symmetric optic: R1 = +R, R2 = -R, so |f| = |R| / (2(n-1))."""
    return abs(R) / (2.0 * (n - 1.0))


# ============================================================================
#  4.  PhET's guides -- a construction PhET invented, reproduced exactly
#
#      fulcrum   = optic + (0, s*D/2),  s = +1 top, -1 bottom
#      incident  = angle(object - fulcrum)
#      r         = D / (4 f)                       (f SIGNED)
#      convex :  transmitted = incident + pi - s * 2*atan(r)
#      concave:  transmitted = incident + pi - s * (atan(3r) - atan(r))
# ============================================================================
def guide_angles(surface, f, D, obj, s):
    fx, fy = 0.0, s * D / 2.0
    inc = math.atan2(obj[1] - fy, obj[0] - fx)
    r = D / (4.0 * f)
    if surface == 'convex':
        corr = -s * (2.0 * math.atan(r))
    else:
        corr = -s * (math.atan(3.0 * r) - math.atan(r))
    return inc, inc + math.pi + corr, r


def guide_deviation(surface, f, D, s):
    """The angle the guide turns a ray through, measured from the straight-on
    continuation.  Independent of where the object is -- which is exactly what
    makes the guides an approximation."""
    r = D / (4.0 * f)
    if surface == 'convex':
        return -s * 2.0 * math.atan(r)
    return -s * (math.atan(3.0 * r) - math.atan(r))


def guide_cross(surface, f, D, obj):
    """Where PhET's two transmitted guides cross -- its approximation to the
    image point."""
    pts = []
    for s in (1, -1):
        fy = s * D / 2.0
        inc, out, r = guide_angles(surface, f, D, obj, s)
        pts.append((fy, math.cos(out), math.sin(out)))
    (y1, c1, s1), (y2, c2, s2) = pts
    # y = y1 + (s1/c1) x  and  y = y2 + (s2/c2) x
    m1, m2 = s1 / c1, s2 / c2
    if m1 == m2:
        return (math.inf, math.inf)
    x = (y2 - y1) / (m1 - m2)
    return (x, y1 + m1 * x)


def slope_cross(f, D, do, yo):
    """The same pair of rays, but bent by the thin-optic SLOPE law instead of
    by a fixed rotation.  Exact for every object, which is the point."""
    out = []
    for s in (1, -1):
        h = s * D / 2.0
        out.append((h, out_slope(f, do, yo, h)))
    (h1, u1), (h2, u2) = out
    if u1 == u2:
        return (math.inf, math.inf)
    x = (h2 - h1) / (u1 - u2)
    return (x, h1 + u1 * x)


def true_deviation(f, do, yo, s, D):
    """The angle an IDEAL thin optic turns the ray that strikes it at the
    guide's own fulcrum height h = s*D/2."""
    h = s * D / 2.0
    u = (h - yo) / do
    up = u - h / f
    return math.atan(up) - math.atan(u)


# ============================================================================
#  5.  PhET's light spot on the projection screen (Lens screen)
#
#  The spot is bounded by the two rays that graze the rim of the lens and head
#  for the image point; where they cross the screen plane sets its extent.
# ============================================================================
def spot_edge(screen_x, rim_y, img):
    """The optic is at x = 0 (PhET fixes it there), so the rim's x never
    appears; carrying it would be generality no test can reach."""
    n = 1e7 if img[0] == 0 else screen_x / img[0]
    return rim_y + (img[1] - rim_y) * n


def light_spot(screen_x, D, f, do, yo):
    img = image_point('lens', f, do, yo)
    yt = spot_edge(screen_x, D / 2.0, img)
    yb = spot_edge(screen_x, -D / 2.0, img)
    return (0.5 * (yt + yb), abs(yt - yb))


def spot_diameter_closed(screen_x, D, f, do):
    """Closed form: the cone from the rim to the image, extended to the screen.
    |diameter| = D * |screen_x - d_i| / d_i   for a lens image at x = d_i."""
    di = image_distance(f, do)
    return D * abs(screen_x - di) / abs(di)


# ============================================================================
#  6.  Exact ray tracing through a REAL spherical lens -- where the thin-lens
#      model runs out.  Vector Snell, sphere intersection in closed form, and
#      a second route (Newton on the sag) to check it.
# ============================================================================
def sag(R, h):
    """z of a spherical surface at height h, vertex at z = 0, sign(R) as usual."""
    if math.isinf(R) or R == 0:
        return 0.0
    d = R * R - h * h
    if d < 0:
        return float('nan')
    return h * h / (R * (1.0 + math.sqrt(d) / abs(R)))


def hit_sphere(p, d, z0, R, semi):
    """Closed-form intersection of the ray p + t d with the sphere of radius R
    whose vertex is at (0, z0).  Returns the (y, z) hit or None."""
    if math.isinf(R) or R == 0:
        if abs(d[1]) < 1e-15:
            return None
        t = (z0 - p[1]) / d[1]
        if t <= 1e-12:
            return None
        q = (p[0] + t * d[0], z0)
        return q if abs(q[0]) <= semi else None
    cz = z0 + R                                  # centre of curvature
    oy, oz = p[0] - 0.0, p[1] - cz
    b = 2.0 * (oy * d[0] + oz * d[1])
    c = oy * oy + oz * oz - R * R
    disc = b * b - 4.0 * c                       # |d| = 1
    if disc < 0:
        return None
    sq = math.sqrt(disc)
    ts = sorted([(-b - sq) / 2.0, (-b + sq) / 2.0])
    best = None
    for t in ts:
        if t <= 1e-12:
            continue
        q = (p[0] + t * d[0], p[1] + t * d[1])
        if abs(q[0]) > semi:
            continue
        # the physical vertex-side branch: |z - z0| must be the small root
        if abs(q[1] - z0) > abs(R):
            continue
        if best is None:
            best = q
    return best


def hit_sphere_newton(p, d, z0, R, semi):
    """The same intersection by Newton on the sag -- the independent route."""
    if math.isinf(R) or R == 0:
        return hit_sphere(p, d, z0, R, semi)
    if abs(d[1]) < 1e-15:
        return None
    t = (z0 - p[1]) / d[1]
    for _ in range(80):
        y = p[0] + t * d[0]
        z = p[1] + t * d[1]
        if abs(y) >= abs(R):
            return None
        s = sag(R, y)
        if not math.isfinite(s):
            return None
        err = z - (z0 + s)
        disc = 1.0 - y * y / (R * R)
        if disc <= 0:
            return None
        dsdy = y / (R * math.sqrt(disc))
        den = d[1] - dsdy * d[0]
        if abs(den) < 1e-15:
            return None
        dt = -err / den
        t += dt
        if abs(dt) < 1e-14:
            break
    if t <= 1e-12:
        return None
    q = (p[0] + t * d[0], p[1] + t * d[1])
    return q if abs(q[0]) <= semi else None


def sphere_normal(y, R):
    if math.isinf(R) or R == 0:
        return (0.0, -1.0)
    disc = 1.0 - y * y / (R * R)
    if disc <= 0:
        return (0.0, -1.0)
    dsdy = y / (R * math.sqrt(disc))
    n = (-dsdy, 1.0)
    L = math.hypot(*n)
    return (n[0] / L, n[1] / L)


def refract(d, nrm, n1, n2):
    L = math.hypot(*d)
    dx, dy = d[0] / L, d[1] / L
    nx, ny = nrm
    ci = -(nx * dx + ny * dy)
    if ci < 0:
        nx, ny, ci = -nx, -ny, -ci
    eta = n1 / n2
    k = 1.0 - eta * eta * (1.0 - ci * ci)
    if k < 0:
        return None
    fscale = eta * ci - math.sqrt(k)
    return (eta * dx + fscale * nx, eta * dy + fscale * ny)


def trace_lens(p0, d0, n, R1, R2, t, semi, newton=False):
    """Trace one ray through a biconvex/biconcave glass lens whose FRONT vertex
    is at z = 0 and rear vertex at z = t.  Returns the hit list and the exit
    ray, or None if the ray is blocked."""
    hit = hit_sphere_newton if newton else hit_sphere
    L = math.hypot(*d0)
    d = (d0[0] / L, d0[1] / L)
    p = p0
    pts = [p]
    q = hit(p, d, 0.0, R1, semi)
    if q is None:
        return None
    dd = refract(d, sphere_normal(q[0], R1), 1.0, n)
    if dd is None:
        return None
    pts.append(q)
    p, d = q, dd
    q = hit(p, d, t, R2, semi)
    if q is None:
        return None
    dd = refract(d, sphere_normal(q[0], R2), n, 1.0)
    if dd is None:
        return None
    pts.append(q)
    return dict(pts=pts, p=q, d=dd)


def axis_crossing(p, d):
    if abs(d[0]) < 1e-15:
        return math.inf
    return p[1] + (-p[0] / d[0]) * d[1]


def lsa(h, n, R1, R2, t, semi):
    """Longitudinal spherical aberration at ray height h: the axis crossing of
    a ray entering parallel to the axis at height h, minus the paraxial back
    focal point.  Both measured from the REAR vertex (z = t)."""
    r = trace_lens((h, -1000.0), (0.0, 1.0), n, R1, R2, t, semi)
    if r is None:
        return float('nan')
    z = axis_crossing(r['p'], r['d'])
    return (z - t) - bfd(n, R1, R2, t)


def blur_radius(h, n, R1, R2, t, semi):
    """Transverse height of the marginal ray at the PARAXIAL focal plane."""
    r = trace_lens((h, -1000.0), (0.0, 1.0), n, R1, R2, t, semi)
    if r is None:
        return float('nan')
    zf = t + bfd(n, R1, R2, t)
    s = (zf - r['p'][1]) / r['d'][1]
    return r['p'][0] + s * r['d'][0]


# ============================================================================
#  the run
# ============================================================================
def main():
    head('0.  PhET constants read out of the minified original (build 1.3.16)')
    for k in sorted(PHET):
        print('  %-24s %s' % (k, PHET[k]))

    # ------------------------------------------------------------------ 1 ---
    head('1.  the thin-lens / mirror equation, and every regime of it')
    cases = [
        ('converging lens, object beyond 2F  (real, minified)', 'lens', 80.0, 170.0, 27.0),
        ('converging lens, object at 2F      (real, m = -1)', 'lens', 80.0, 160.0, 27.0),
        ('converging lens, F < d_o < 2F      (real, magnified)', 'lens', 80.0, 120.0, 27.0),
        ('converging lens, object AT F       (image at infinity)', 'lens', 80.0, 80.0, 27.0),
        ('converging lens, object inside F   (virtual, upright)', 'lens', 80.0, 50.0, 27.0),
        ('diverging lens                     (always virtual)', 'lens', -80.0, 170.0, 27.0),
        ('diverging lens, object inside |f|', 'lens', -80.0, 50.0, 27.0),
        ('concave mirror, object beyond 2F', 'mirror', 90.0, 200.0, 40.0),
        ('concave mirror, object inside F', 'mirror', 90.0, 60.0, 40.0),
        ('convex mirror', 'mirror', -90.0, 150.0, 40.0),
        ('flat mirror  (PhET: f = 1e5 cm)', 'mirror', 1e5, 150.0, 40.0),
    ]
    refs = {}
    for name, kind, f, do, yo in cases:
        di = image_distance(f, do)
        m = -di / do if math.isfinite(di) else float('-inf')
        xi, yi = image_point(kind, f, do, yo) if math.isfinite(di) else (math.inf, math.inf)
        res = residual(f, do, di) if math.isfinite(di) else 0.0
        print('  %-52s f=%8.4f d_o=%7.3f' % (name, f, do))
        print('      d_i = %s' % G(di))
        print('      m   = %s' % G(m))
        print('      img = (%s, %s)' % (G(xi), G(yi)))
        print('      residual 1/d_o + 1/d_i - 1/f = %s' % G(res))
        refs[name] = (di, m, xi, yi)

    print('\n  Newton\'s form:  x x\' = f^2  with x = d_o - f, x\' = d_i - f')
    worst = 0.0
    for f in (80.0, -80.0, 90.0, -90.0, 41.5):
        for do in (40.0, 55.0, 79.0, 81.0, 123.0, 170.0, 400.0):
            di = image_distance(f, do)
            if not math.isfinite(di):
                continue
            worst = max(worst, abs((do - f) * (di - f) - f * f) / (f * f))
    print('      worst relative departure over 35 (f, d_o) pairs: %s' % G(worst))

    print('\n  the d_o = f limit is a pole, not a value:')
    for e in (1e-3, 1e-6, 1e-9):
        print('      d_o = f + %-7g  ->  d_i = %s' % (e, G(image_distance(80.0, 80.0 + e))))
        print('      d_o = f - %-7g  ->  d_i = %s' % (e, G(image_distance(80.0, 80.0 - e))))

    print('\n  real <-> virtual crossover for a converging lens: d_i changes sign at d_o = f')
    print('      d_i(f=80, d_o=80.000001) = %s' % G(image_distance(80.0, 80.000001)))
    print('      d_i(f=80, d_o=79.999999) = %s' % G(image_distance(80.0, 79.999999)))

    if HAVE_SCIPY:
        # the same d_i, found by root-finding the defining equation instead
        def solve(f, do):
            g = lambda di: 1.0 / do + 1.0 / di - 1.0 / f
            lo, hi = (1e-6, 1e9) if do > f else (-1e9, -1e-6)
            return brentq(g, lo, hi, xtol=1e-14, rtol=1e-15, maxiter=400)
        w = 0.0
        for f in (80.0, 90.0, 41.5):
            for do in (45.0, 79.0, 81.0, 170.0, 350.0):
                w = max(w, abs(solve(f, do) - image_distance(f, do)) / abs(image_distance(f, do)))
        print('\n  (scipy) brentq on 1/d_o + 1/d_i - 1/f vs the closed form,')
        print('      worst relative difference over 15 pairs: %s' % G(w))

    # ------------------------------------------------------------------ 2 ---
    head('2.  ray tracing AGREES with the equation, to machine precision')
    print('  For every (kind, f, d_o, y_o) and every ray height h, the outgoing')
    print('  ray built from the slope law u\' = u - h/f must pass through the')
    print('  image point the thin-lens equation gives.  Residual = |y_ray(x_img)')
    print('  - y_img| / (|y_img| + 1).')
    print('  The outgoing ray is at height h + u\' s after a signed path length s,')
    print('  and the image sits at s = d_i (negative s = the backward extension,')
    print('  which is exactly where a virtual image lives).  So the claim is')
    print('      h + (u - h/f) d_i  ==  m y_o     for EVERY h.')
    worst = 0.0
    worst_at = None
    nconf = 0
    for kind, fs in (('lens', (80.0, -80.0, 40.0, 120.0)), ('mirror', (90.0, -90.0, 75.0, 150.0))):
        for f in fs:
            for do in (41.0, 60.0, 79.5, 100.0, 170.0, 300.0):
                for yo in (-60.0, -12.0, 0.0, 27.0, 95.0):
                    di = image_distance(f, do)
                    if not math.isfinite(di) or abs(di) > 1e6:
                        continue
                    yi = -di / do * yo
                    for h in (-40.0, -13.0, 0.0, 7.5, 40.0):
                        y = ray_y_at(f, do, yo, h, di)
                        r = abs(y - yi) / (abs(yi) + 1.0)
                        nconf += 1
                        if r > worst:
                            worst, worst_at = r, (kind, f, do, yo, h)
    print('      worst residual over %d configurations: %s' % (nconf, G(worst)))
    print('      at %s' % (worst_at,))
    print('  (the residual is set by the lever arm: at f = 80, d_o = 79.5 the')
    print('   image is 12 720 cm away, so 1e-16 of slope is 1e-12 of height)')

    print('\n  the three PRINCIPAL rays meet at the image point, pairwise:')
    worst = 0.0
    for kind in ('lens', 'mirror'):
        for f in (80.0, -80.0, 90.0, -90.0):
            for do in (41.0, 60.0, 100.0, 170.0, 300.0):
                for yo in (-95.0, 27.0, 60.0):
                    di = image_distance(f, do)
                    if not math.isfinite(di) or abs(di) > 1e6:
                        continue
                    xi, yi = image_point(kind, f, do, yo)
                    rr = principal_rays(kind, f, do, yo)
                    for i in range(len(rr)):
                        for j in range(i + 1, len(rr)):
                            X, Y = ray_cross(kind, rr[i], rr[j])
                            if not math.isfinite(X):
                                continue
                            e = (abs(X - xi) + abs(Y - yi)) / (abs(xi) + abs(yi) + 1.0)
                            worst = max(worst, e)
    print('      worst relative departure over 360 configurations: %s' % G(worst))

    print('\n  a worked case, printed for the suite to pin:')
    kind, f, do, yo = 'lens', 80.0, 170.0, 27.0
    xi, yi = image_point(kind, f, do, yo)
    print('      lens f = 80, object (-170, 27):  image = (%s, %s)' % (G(xi), G(yi)))
    for (h, u) in principal_rays(kind, f, do, yo):
        print('      h = %-22s u\' = %s' % (G(h), G(u)))
    kind, f, do, yo = 'mirror', 90.0, 150.0, 72.5
    xi, yi = image_point(kind, f, do, yo)
    print('      concave mirror f = 90, object (-150, 72.5):  image = (%s, %s)' % (G(xi), G(yi)))
    for (h, u) in principal_rays(kind, f, do, yo):
        print('      h = %-22s u\' = %s' % (G(h), G(u)))

    print('\n  the parallel ray really does cross the axis at the BACK focal point:')
    for f in (80.0, -80.0, 40.0, 120.0):
        for h in (27.0, -95.0):
            u = bend(0.0, h, f)             # an object at infinity: u = 0 exactly
            print('      f = %+7.2f  parallel ray at h = %+6.1f crosses the axis at s = %s'
                  % (f, h, G(-h / u)))

    print('\n  a ray through the CENTRE is undeviated (h = 0 kills the h/f term):')
    for f in (80.0, -80.0, 1e5):
        print('      f = %+10.2f   u\' - u = %s' % (f, G(out_slope(f, 170.0, 27.0, 0.0) - (0.0 - 27.0) / 170.0)))

    # ------------------------------------------------------------------ 3 ---
    head('3.  the lens maker\'s equation, and PhET\'s use of it')
    print('  PhET makes both surfaces the same radius: R1 = +R, R2 = -R, so')
    print('      1/f = (n-1)(1/R - 1/(-R)) = 2(n-1)/R   =>   f = R / (2(n-1)).')
    print('  Its code computes the MAGNITUDES that way and puts the sign on from')
    print('  the surface type; its doc/model.md prints f = R/(2(1-n)), which is')
    print('  the same equation with the sign convention of the OTHER surface.')
    worst = 0.0
    for n in (1.2, 1.35, 1.5, 1.65, 1.8):
        for R in (40.0, 55.0, 80.0, 120.0):
            a = f_thin(n, R, -R)
            b = phet_f_of_R(R, n)
            worst = max(worst, abs(a - b) / b)
            print('      n = %.2f  R = %6.1f  ->  f_thin = %-22s  R/(2(n-1)) = %s'
                  % (n, R, G(a), G(b)))
    print('      worst relative difference: %s' % G(worst))
    print('\n  PhET\'s "direct" lens model fixes n = 1.5, so R = 2f(n-1) = f exactly:')
    for f in (40.0, 80.0, 120.0):
        print('      f = %6.1f  ->  R = %s' % (f, G(2.0 * f * (1.5 - 1.0))))
    print('\n  PhET models a MIRROR as a lens of index 2, so f = R/(2(2-1)) = R/2:')
    for R in (150.0, 180.0, 300.0):
        print('      R = %6.1f  ->  f = %s   (paraxial mirror: R/2 = %s)'
              % (R, G(phet_f_of_R(R, 2.0)), G(R / 2.0)))
    print('\n  flat mirror, PhET\'s stand-in:  f = %s cm, R = %s cm' % (G(PHET['flat_f']), G(PHET['flat_R'])))
    print('      an object at d_o = 150 then images at d_i = %s' % G(image_distance(PHET['flat_f'], 150.0)))
    print('      m = %s  (the true flat mirror gives exactly -150 and +1)'
          % G(-image_distance(PHET['flat_f'], 150.0) / 150.0))
    print('      so PhET\'s stand-in is wrong by %s cm in d_i and %s in m'
          % (G(abs(image_distance(PHET['flat_f'], 150.0) + 150.0)),
             G(abs(-image_distance(PHET['flat_f'], 150.0) / 150.0 - 1.0))))

    print('\n  the general (unequal-radii) form reduces to the symmetric one:')
    print('      1/f = (n-1)(1/R1 - 1/R2):  plano-convex R2 = inf')
    for n, R1 in ((1.5, 80.0), (1.5, 40.0)):
        print('      n = %.2f R1 = %5.1f R2 = inf ->  f = %s  ( = R1/(n-1) )'
              % (n, R1, G(f_thin(n, R1, float('inf')))))

    # ------------------------------------------------------------------ 4 ---
    head('4.  PhET\'s guides -- what they are, and what they approximate')
    f, D = 80.0, 80.0
    obj = (-170.0, 27.0)
    for s, nm in ((1, 'top'), (-1, 'bottom')):
        inc, out, r = guide_angles('convex', f, D, obj, s)
        print('  convex, %-6s fulcrum (0, %+6.1f):  r = D/4f = %s' % (nm, s * D / 2, G(r)))
        print('      incident angle  = %s rad' % G(inc))
        print('      transmitted     = %s rad' % G(out))
        print('      internal turn   = %s rad = %s deg'
              % (G(guide_deviation('convex', f, D, s)), G(math.degrees(guide_deviation('convex', f, D, s)))))
    for s, nm in ((1, 'top'), (-1, 'bottom')):
        inc, out, r = guide_angles('concave', -f, D, obj, s)
        print('  concave, %-5s r = %s  internal turn = %s rad'
              % (nm, G(D / (4.0 * -f)), G(guide_deviation('concave', -f, D, s))))

    print('\n  PhET\'s two branches differ by EXACTLY 3 atan(r) - atan(3r) = 8r^3/... :')
    for r in (0.01, 0.05, 0.25, 0.5):
        d = 3.0 * math.atan(r) - math.atan(3.0 * r)
        print('      r = %-6g  3atan(r)-atan(3r) = %-24s  8r^3 = %-24s ratio = %s'
              % (r, G(d), G(8.0 * r ** 3), G(d / (8.0 * r ** 3))))

    print('\n  the guide is EXACT in the paraxial limit and approximate outside it.')
    print('  Compare the guide\'s fixed turn with the turn an ideal thin optic')
    print('  gives the ray that strikes it at the same height h = D/2:')
    for D in (5.0, 20.0, 80.0, 120.0):
        gd = guide_deviation('convex', 80.0, D, 1)
        td = true_deviation(80.0, 170.0, 27.0, 1, D)
        print('      D = %6.1f  guide = %-23s  ideal = %-23s  diff = %s'
              % (D, G(gd), G(td), G(gd - td)))
    print('  the difference is O(D^3) in the limit; halving D at fixed object:')
    prev = None
    for D in (10.0, 5.0, 2.5, 1.25):
        d = guide_deviation('convex', 80.0, D, 1) - true_deviation(80.0, 170.0, 27.0, 1, D)
        if prev is not None:
            print('      D = %7.4f  diff = %-24s  ratio to previous = %s' % (D, G(d), G(prev / d)))
        else:
            print('      D = %7.4f  diff = %s' % (D, G(d)))
        prev = d
    print('  (a ratio of 8 per halving is a cubic; the guide and the true ray')
    print('   agree through O(D^2) and part company at O(D^3))')

    print('\n  where the PAIR of guides points: the two transmitted rays cross,')
    print('  and that crossing is PhET\'s approximation to the image point.')
    for D in (5.0, 20.0, 80.0, 120.0):
        X, Y = guide_cross('convex', 80.0, D, (-170.0, 27.0))
        xi, yi = image_point('lens', 80.0, 170.0, 27.0)
        print('      D = %6.1f  guides cross at (%s, %s)' % (D, G(X), G(Y)))
        print('                 the image is at   (%s, %s)   miss %s %%'
              % (G(xi), G(yi), G(100.0 * math.hypot(X - xi, Y - yi) / math.hypot(xi, yi))))
    print('\n  shrinking D alone does NOT make them exact -- the miss sticks at')
    print('  4.5 %, because PhET rotates the ray by a fixed ANGLE where a thin')
    print('  optic changes its SLOPE, and tan(a + da) = tan a + da(1 + tan^2 a):')
    print('  the surviving error is the u^2 of the ray\'s own inclination.')
    for D in (80.0, 20.0, 5.0, 1.0, 0.25):
        X, Y = guide_cross('convex', 80.0, D, (-170.0, 27.0))
        xi, yi = image_point('lens', 80.0, 170.0, 27.0)
        print('      D = %7.3f  cross x = %-22s  miss %s cm (%s %%)'
              % (D, G(X), G(math.hypot(X - xi, Y - yi)),
                 G(100.0 * math.hypot(X - xi, Y - yi) / math.hypot(xi, yi))))
    print('  shrinking the OBJECT\'S inclination as well does:  (D, y_o) = e(80, 27)')
    prev = None
    for e in (1.0, 0.5, 0.25, 0.125, 0.0625):
        X, Y = guide_cross('convex', 80.0, 80.0 * e, (-170.0, 27.0 * e))
        xi, yi = image_point('lens', 80.0, 170.0, 27.0 * e)
        miss = abs(X - xi)
        if prev is None:
            print('      e = %7.4f   |x_cross - d_i| = %s cm' % (e, G(miss)))
        else:
            print('      e = %7.4f   |x_cross - d_i| = %-22s  ratio %s' % (e, G(miss), G(prev / miss)))
        prev = miss
    print('      (a ratio of 4 per halving: the miss is O(e^2) = O(u^2), so the')
    print('       guides ARE the thin-optic construction to second order)')
    print('\n  the SLOPE version of the same construction (u\' = u - h/f at the')
    print('  fulcrum heights) is exact for every object, by construction:')
    w = 0.0
    for do in (41.0, 170.0, 600.0):
        for yo in (-95.0, 0.0, 27.0, 95.0):
            for D in (60.0, 80.0, 120.0):
                X, Y = slope_cross(80.0, D, do, yo)
                xi, yi = image_point('lens', 80.0, do, yo)
                w = max(w, math.hypot(X - xi, Y - yi) / (math.hypot(xi, yi) + 1.0))
    print('      worst relative miss over 36 configurations: %s' % G(w))

    # ------------------------------------------------------------------ 5 ---
    head('5.  the light spot on PhET\'s projection screen')
    D, f, do, yo, sx = 80.0, 80.0, 170.0, 20.0, 200.0
    c, dia = light_spot(sx, D, f, do, yo)
    print('  lens D = 80, f = 80, source (-170, 20), screen at x = 200')
    print('      image      = (%s, %s)' % (G(image_point('lens', f, do, yo)[0]), G(image_point('lens', f, do, yo)[1])))
    print('      spot centre y = %s' % G(c))
    print('      spot diameter = %s' % G(dia))
    print('      closed form D|x_s - d_i|/d_i = %s' % G(spot_diameter_closed(sx, D, f, do)))
    print('      difference = %s' % G(abs(dia - spot_diameter_closed(sx, D, f, do))))
    print('  the spot collapses to a point when the screen is AT the image:')
    di = image_distance(f, do)
    for dx in (40.0, 4.0, 0.4, 0.04):
        print('      screen at d_i + %-6g  ->  diameter = %s' % (dx, G(light_spot(di + dx, D, f, do, yo)[1])))
    print('  and it grows linearly with the screen\'s distance past the image:')
    print('      slope d(diameter)/d(x_screen) = %s  (exact: D/d_i = %s)'
          % (G((light_spot(di + 20.0, D, f, do, yo)[1] - light_spot(di + 10.0, D, f, do, yo)[1]) / 10.0),
             G(D / di)))

    # ------------------------------------------------------------------ 6 ---
    head('6.  where the thin-lens model fails: a REAL spherical lens')
    n = PHET['ior_direct_lens']
    R = PHET['roc_lens'][2]                      # 80 cm, PhET's default
    D = PHET['d_lens'][2]                        # 80 cm, PhET's default
    a = D / 2.0
    s = R - math.sqrt(R * R - a * a)
    t_edge = 2.0
    t = 2.0 * s + t_edge
    print('  Take PhET\'s own default lens at face value: n = %.1f, R = %.0f cm,' % (n, R))
    print('  diameter %.0f cm.  As a real biconvex glass lens that is' % D)
    print('      sag per surface        = %s cm' % G(s))
    print('      centre thickness       = %s cm  (edge thickness %.1f cm, chosen)' % (G(t), t_edge))
    print('      f/number f/D           = %s     -- an f/1 lens' % G(phet_f_of_R(R, n) / D))
    print('      thin-lens f            = %s cm' % G(f_thin(n, R, -R)))
    print('      thick-lens f           = %s cm' % G(f_thick(n, R, -R, t)))
    print('      back focal distance    = %s cm (from the rear vertex)' % G(bfd(n, R, -R, t)))

    print('\n  exact trace of parallel rays: the axis crossing walks IN as h grows')
    hs = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 24.0, 32.0, 38.0, 39.5]
    for hh in hs:
        z = lsa(hh, n, R, -R, t, a)
        print('      h = %6.2f cm  LSA = %-24s cm   blur y = %s cm'
              % (hh, G(z), G(blur_radius(hh, n, R, -R, t, a))))
    print('\n  the paraxial limit: LSA -> 0 as h -> 0, quadratically')
    prev = None
    for hh in (4.0, 2.0, 1.0, 0.5, 0.25):
        z = lsa(hh, n, R, -R, t, a)
        if prev is not None:
            print('      h = %6.3f  LSA = %-24s  ratio to previous = %s' % (hh, G(z), G(prev / z)))
        else:
            print('      h = %6.3f  LSA = %s' % (hh, G(z)))
        prev = z
    print('      (a ratio of 4 per halving is h^2 -- third-order aberration)')
    c_h2 = lsa(0.25, n, R, -R, t, a) / 0.25 ** 2
    print('      LSA / h^2 -> %s cm^-1' % G(c_h2))

    print('\n  the two intersection routes agree (closed form vs Newton on the sag):')
    w = 0.0
    for hh in (0.5, 4.0, 16.0, 32.0, 39.0):
        r1 = trace_lens((hh, -1000.0), (0.0, 1.0), n, R, -R, t, a, newton=False)
        r2 = trace_lens((hh, -1000.0), (0.0, 1.0), n, R, -R, t, a, newton=True)
        w = max(w, abs(axis_crossing(r1['p'], r1['d']) - axis_crossing(r2['p'], r2['d'])))
    print('      worst |z_focus difference| over five heights: %s cm' % G(w))

    print('\n  the marginal focus, the paraxial focus, and the blur:')
    zmarg = lsa(a * 0.98, n, R, -R, t, a)
    print('      marginal (h = 0.98 a = %.2f cm) LSA = %s cm' % (a * 0.98, G(zmarg)))
    print('      that is %s %% of the focal length' % G(100.0 * abs(zmarg) / f_thick(n, R, -R, t)))
    print('      blur radius at the paraxial focus = %s cm' % G(abs(blur_radius(a * 0.98, n, R, -R, t, a))))
    if HAVE_SCIPY:
        def rms_at(z):
            tot, cnt = 0.0, 0
            for i in range(1, 41):
                hh = a * 0.985 * i / 40.0
                r = trace_lens((hh, -1000.0), (0.0, 1.0), n, R, -R, t, a)
                if r is None:
                    continue
                ss = (z - r['p'][1]) / r['d'][1]
                y = r['p'][0] + ss * r['d'][0]
                tot += hh * y * y                # area weight
                cnt += hh
            return math.sqrt(tot / cnt)
        z0 = t + bfd(n, R, -R, t)
        res = minimize_scalar(rms_at, bounds=(z0 - 60.0, z0 + 10.0), method='bounded',
                              options=dict(xatol=1e-10))
        print('      (scipy) circle of least confusion at z = %s cm, i.e. %s cm'
              % (G(res.x), G(res.x - z0)))
        print('      (scipy) inside the paraxial focus; rms spot there = %s cm' % G(res.fun))
        print('      (scipy) rms spot at the paraxial focus            = %s cm' % G(rms_at(z0)))

    print('\n  a SLOW lens is nearly paraxial -- the same lens stopped to D = 8 cm:')
    a2 = 4.0
    print('      LSA at the rim (h = %.2f) = %s cm  ( %s %% of f )'
          % (a2 * 0.98, G(lsa(a2 * 0.98, n, R, -R, t, a)),
             G(100.0 * abs(lsa(a2 * 0.98, n, R, -R, t, a)) / f_thick(n, R, -R, t))))

    print('\n  a real CONCAVE MIRROR has spherical aberration too, and its exact')
    print('  marginal focus is a closed form: a ray parallel at height h strikes')
    print('  the sphere and crosses the axis at  z = R - R/(2 cos(asin(h/R))),')
    print('  measured from the centre of curvature; from the vertex that is')
    print('  |f| = R/2 only in the limit h -> 0.')
    Rm = PHET['roc_mirror'][2]
    for hh in (1.0, 10.0, 30.0, 40.0, 59.0):
        th = math.asin(hh / Rm)
        zf = Rm - Rm / (2.0 * math.cos(th))      # from the vertex, toward the centre
        print('      h = %5.1f  focus at %s cm from the vertex  (paraxial %s)'
              % (hh, G(zf), G(Rm / 2.0)))
    print('      the caustic cusp (h -> 0) is at R/2 = %s cm' % G(Rm / 2.0))
    print('      at the rim h = 60 the focus is %s cm short of it'
          % G(Rm / 2.0 - (Rm - Rm / (2.0 * math.cos(math.asin(60.0 / Rm))))))
    # cross-check the closed form by exact vector reflection.  Put the vertex at
    # z = 0 with the light running in +z and the centre of curvature at z = -Rm,
    # so the rim of a concave mirror is NEARER the source than its vertex.
    def mirror_focus_trace(h, Rm):
        th = math.asin(h / Rm)
        zhit = -Rm * (1.0 - math.cos(th))        # negative: in front of the vertex
        nx, ny = math.sin(th), math.cos(th)      # unit normal, from the centre out
        dx, dy = 0.0, 1.0
        dot = dx * nx + dy * ny
        rx, ry = dx - 2 * dot * nx, dy - 2 * dot * ny
        if rx == 0:
            return math.inf
        t = -h / rx
        return -(zhit + t * ry)                  # distance IN FRONT of the vertex
    w = 0.0
    for hh in (1.0, 10.0, 30.0, 40.0, 59.0):
        th = math.asin(hh / Rm)
        w = max(w, abs(mirror_focus_trace(hh, Rm) - (Rm - Rm / (2.0 * math.cos(th)))))
    print('      closed form vs exact vector reflection, worst difference: %s cm' % G(w))
    print('      and the rim ray at h = 60 exactly: %s cm' % G(mirror_focus_trace(60.0, Rm)))

    # ------------------------------------------------------------------ 7 ---
    head('7.  PhET\'s "many" rays: how many, and how wide')
    print('  PhET: n = 20 * (floor(d_o / 300) + 1) rays over a %.0f-degree fan.' % PHET['many_fan_deg'])
    for do in (41.0, 170.0, 299.0, 300.0, 601.0, 1200.0):
        nray = 20 * (int(do // 300) + 1)
        print('      d_o = %7.1f  ->  %3d rays, spacing %s deg'
              % (do, nray, G(PHET['many_fan_deg'] / (nray - 1))))
    print('\n  how many of them hit an aperture of diameter D at distance d_o:')
    for D, do in ((80.0, 170.0), (80.0, 41.0), (60.0, 300.0), (120.0, 170.0)):
        nray = 20 * (int(do // 300) + 1)
        half = math.radians(PHET['many_fan_deg']) / 2.0
        step = 2.0 * half / (nray - 1)
        cnt = 0
        for i in range(nray):
            ang = half - i * step
            # a ray from (-d_o, 0) at this angle crosses x = 0 at y = d_o tan(ang)
            if abs(math.tan(ang) * do) <= D / 2.0:
                cnt += 1
        print('      D = %5.1f d_o = %6.1f  ->  %d of %d rays reach the optic' % (D, do, cnt, nray))

    # ------------------------------------------------------------------ 8 ---
    head('8.  the drawn optic is not the modelled optic (PhET\'s own note)')
    print('  PhET draws its lens with a "hollywooded" sag  a = (D/2)^2 / (2(|R|+100))')
    print('  instead of the true sag  |R| - sqrt(R^2 - (D/2)^2).  At its defaults:')
    for R, D in ((80.0, 80.0), (40.0, 120.0), (120.0, 60.0)):
        aH = 0.5 * (D / 2.0) ** 2 / (abs(R) + 100.0)
        aT = abs(R) - math.sqrt(R * R - (D / 2.0) ** 2) if abs(R) > D / 2.0 else float('nan')
        print('      R = %5.1f D = %5.1f   drawn half-thickness = %-22s  true sag = %s'
              % (R, D, G(aH), G(aT)))
    print('  Its MIRROR shape uses the true sag  |R| - sqrt(R^2 - (D/2)^2):')
    for R, D in ((180.0, 80.0), (150.0, 120.0)):
        print('      R = %5.1f D = %5.1f   sag = %s' % (R, D, G(abs(R) - math.sqrt(R * R - (D / 2.0) ** 2))))

    head('9.  a small table the suite pins directly')
    print('  lens f = 80 cm (PhET default), object at PhET\'s framed position (-170, 27):')
    for f in (80.0, -80.0):
        di = image_distance(f, 170.0)
        print('      f = %+6.1f  d_i = %-22s  m = %-22s  %s'
              % (f, G(di), G(-di / 170.0), 'real' if di > 0 else 'virtual'))
    print('  mirror f = 90 cm (PhET default), object at (-150, 72.5):')
    for f in (90.0, -90.0):
        di = image_distance(f, 150.0)
        print('      f = %+6.1f  d_i = %-22s  m = %-22s  %s'
              % (f, G(di), G(-di / 150.0), 'real' if di > 0 else 'virtual'))
    print('  the four PhET slider corners, converging lens, object at -170:')
    for f in (40.0, 120.0):
        for do in (40.0, 170.0):
            di = image_distance(f, do)
            print('      f = %5.1f d_o = %5.1f  d_i = %-22s  m = %s' % (f, do, G(di), G(-di / do)))


if __name__ == '__main__':
    main()
