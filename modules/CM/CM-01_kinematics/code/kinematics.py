"""
CM-01  Kinematics -- position, velocity, acceleration of a particle.

Part of the physics topic network (modules/topic_network.txt, module CM-01).
Builds directly on ~MA-01 (vector algebra): a trajectory is a vector-valued
FUNCTION r(t); from it we get v(t)=r'(t), a(t)=r''(t), the speed, the
tangential/normal split of the acceleration, the curvature, and the plane-polar
decomposition -- every result is itself a function of t, and we reuse MA-01's
dot/cross/norm/unit straight on those functions.

Feeds ~CM-09 (angular momentum L=r x p, torque), ~CM-10 (centripetal motion),
~CM-11 (central-force orbits).

NOTE: MA-01's vector_algebra is imported by relative path for now; once the
shared `physkit` package exists this line becomes
    from physkit.vector_algebra import dot, cross, norm, unit
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-01_vector_algebra", "code"))
if _MA01 not in sys.path:
    sys.path.insert(0, _MA01)

from vector_algebra import dot, cross, norm, unit  # noqa: E402

__all__ = [
    "derivative", "velocity", "acceleration", "speed", "tangent",
    "tangential_acceleration", "normal_acceleration",
    "curvature", "radius_of_curvature",
    "uniform_acceleration", "projectile", "time_of_flight", "range_", "max_height",
    "polar_position", "polar_acceleration_components",
]


# --- differentiation of vector-valued functions ------------------------------

def derivative(f, h=1e-6):
    """Numerical time-derivative of a vector function f(t)->R^3 (central diff)."""
    def fp(t):
        a, b = f(t + h), f(t - h)
        return tuple((a[i] - b[i]) / (2.0 * h) for i in range(3))
    return fp


def velocity(r, h=1e-6):
    """v(t) = r'(t)   (a vector function)."""
    return derivative(r, h)


def acceleration(r, h=1e-4):
    """a(t) = r''(t)  via the central second difference  (a vector function)."""
    def a(t):
        p, q, m = r(t + h), r(t), r(t - h)
        return tuple((p[i] - 2.0 * q[i] + m[i]) / (h * h) for i in range(3))
    return a


def speed(r, h=1e-6):
    """|v(t)|   (a scalar function).  Reuses MA-01 norm on the velocity function."""
    return norm(velocity(r, h))


def tangent(r, h=1e-6):
    """Unit tangent  T(t) = v/|v|   (a vector function)."""
    return unit(velocity(r, h))


# --- the tangential / normal split  (uses MA-01 dot & cross) ------------------

def tangential_acceleration(r, h=1e-4):
    """Scalar a_T = (a . v)/|v| = d|v|/dt   (a scalar function)."""
    v, a = velocity(r), acceleration(r, h)

    def a_T(t):
        vt = v(t)
        return dot(a(t), vt) / norm(vt)
    return a_T


def normal_acceleration(r, h=1e-4):
    """Scalar a_N = |v x a|/|v| = v^2/R   (a scalar function)."""
    v, a = velocity(r), acceleration(r, h)

    def a_N(t):
        vt = v(t)
        return norm(cross(vt, a(t))) / norm(vt)
    return a_N


def curvature(r, h=1e-4):
    """kappa(t) = |v x a| / |v|^3   (a scalar function)."""
    v, a = velocity(r), acceleration(r, h)

    def k(t):
        vt = v(t)
        return norm(cross(vt, a(t))) / norm(vt) ** 3
    return k


def radius_of_curvature(r, h=1e-4):
    """R(t) = 1/kappa(t)   (a scalar function)."""
    k = curvature(r, h)
    return lambda t: 1.0 / k(t)


# --- constant acceleration & projectiles -------------------------------------

def uniform_acceleration(r0, v0, a):
    """Constant-acceleration trajectory  r(t) = r0 + v0 t + 1/2 a t^2  (vector func)."""
    return lambda t: tuple(r0[i] + v0[i] * t + 0.5 * a[i] * t * t for i in range(3))


def projectile(speed0, angle, g=9.81, r0=(0.0, 0.0, 0.0)):
    """Projectile launched in the x-z plane at `angle` (radians) above +x, with
    gravity along -z.  Returns r(t) (a vector function); x is horizontal, z up."""
    v0 = (speed0 * math.cos(angle), 0.0, speed0 * math.sin(angle))
    return uniform_acceleration(r0, v0, (0.0, 0.0, -g))


def time_of_flight(speed0, angle, g=9.81):
    """Time to return to launch height on level ground:  2 v0 sin(theta)/g."""
    return 2.0 * speed0 * math.sin(angle) / g


def range_(speed0, angle, g=9.81):
    """Horizontal range on level ground:  v0^2 sin(2 theta)/g."""
    return speed0 ** 2 * math.sin(2.0 * angle) / g


def max_height(speed0, angle, g=9.81):
    """Peak height above launch:  (v0 sin theta)^2 / (2 g)."""
    return (speed0 * math.sin(angle)) ** 2 / (2.0 * g)


# --- plane-polar kinematics --------------------------------------------------

def polar_position(rho, theta):
    """Planar trajectory from polar scalar functions rho(t), theta(t):
       r(t) = (rho cos theta, rho sin theta, 0)   (a vector function)."""
    return lambda t: (rho(t) * math.cos(theta(t)), rho(t) * math.sin(theta(t)), 0.0)


def _d(f, h=1e-6):     # scalar first derivative
    return lambda t: (f(t + h) - f(t - h)) / (2.0 * h)


def _dd(f, h=1e-4):    # scalar second derivative
    return lambda t: (f(t + h) - 2.0 * f(t) + f(t - h)) / (h * h)


def polar_acceleration_components(rho, theta, h=1e-4):
    """Radial & transverse acceleration of planar polar motion, as scalar funcs:

        a_r     = rho'' - rho (theta')^2          (the -rho*omega^2 is centripetal)
        a_theta = rho theta'' + 2 rho' theta'     (the 2 rho' theta' is Coriolis)

    Returns the pair (a_r, a_theta)."""
    rd, rdd = _d(rho), _dd(rho, h)
    td, tdd = _d(theta), _dd(theta, h)
    a_r = lambda t: rdd(t) - rho(t) * td(t) ** 2
    a_theta = lambda t: rho(t) * tdd(t) + 2.0 * rd(t) * td(t)
    return a_r, a_theta


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-01 kinematics -- demo")
    print("=" * 32)

    v0, ang = 20.0, math.radians(40.0)
    r = projectile(v0, ang)
    a = acceleration(r)
    print("projectile  v0=20 m/s  angle=40 deg:")
    print(f"  range   = {range_(v0, ang):.3f} m")
    print(f"  apex    = {max_height(v0, ang):.3f} m   t_flight = {time_of_flight(v0, ang):.3f} s")
    print(f"  a(0.37) ~ {tuple(round(c, 3) for c in a(0.37))} m/s^2  (expect ~ (0, 0, -9.81))")

    R, w = 2.0, 3.0
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    sp, kap = speed(circ), curvature(circ)
    aN, aT = normal_acceleration(circ), tangential_acceleration(circ)
    t = 0.6
    print("\nuniform circular motion  R=2, omega=3:")
    print(f"  speed        = {sp(t):.4f}   (R*omega   = {R * w})")
    print(f"  curvature    = {kap(t):.4f}   (1/R       = {1 / R})")
    print(f"  a_normal     = {aN(t):.4f}   (v^2/R     = {(R * w) ** 2 / R})")
    print(f"  a_tangential = {aT(t):.2e}  (~0, constant speed)")

    a_r, a_th = polar_acceleration_components(lambda t: R, lambda t: w * t)
    print(f"  polar a_r    = {a_r(t):.4f}   (-R*omega^2 = {-R * w * w})")
    print(f"  polar a_th   = {a_th(t):.2e}  (~0, no Coriolis)")


if __name__ == "__main__":
    _demo()
