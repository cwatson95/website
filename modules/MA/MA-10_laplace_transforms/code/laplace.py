"""
MA-10  Laplace & integral transforms -- the Laplace transform, its operational
rules (linearity, first-shift, derivative), the convolution theorem, and the
use of transforms to turn linear constant-coefficient ODE initial-value
problems into algebra (Boas Ch.8, sections 8-10).

Part of the physics topic network (modules/topic_network.txt, module MA-10).
Pairs with ~MA-09 (Fourier transforms), feeds ~CM-15 (driven oscillator and
transient response), ~EM-12 (AC transients), and the causal Green's function of
~MA-14.

Pure Python (math/cmath), dependency-free. The forward transform is evaluated by
composite-Simpson quadrature; ODEs are solved the way Boas Section 9 does it --
transform, do algebra in s, then invert through the standard table by partial
fractions over the quadratic characteristic polynomial s^2 + p s + q. A
self-contained RK4 integrator in the tests cross-checks the closed forms.
"""

import cmath
import math

__all__ = [
    "laplace_numeric", "convolve",
    "F_const", "F_exp", "F_pow", "F_cos", "F_sin",
    "invert_quadratic", "solve_ivp_laplace", "rk4",
]


# --- forward transform (quadrature) ------------------------------------------

def laplace_numeric(f, s, T=None, N=20000):
    """Forward Laplace transform  F(s) = int_0^inf f(t) e^{-st} dt  by composite
    Simpson's rule. Needs Re(s) > 0 for convergence; the upper limit defaults to
    where e^{-Re(s) T} is already negligible. Returns a complex number (the
    imaginary part is ~0 for real-valued f and real s)."""
    sr = s.real if isinstance(s, complex) else float(s)
    if sr <= 0:
        raise ValueError("need Re(s) > 0 for the integral to converge")
    if T is None:
        T = 32.0 / sr                      # e^{-32} ~ 1e-14
    if N % 2:
        N += 1
    h = T / N
    total = 0.0 + 0.0j
    for k in range(N + 1):
        t = k * h
        w = 1.0 if k in (0, N) else (4.0 if k % 2 else 2.0)
        total += w * f(t) * cmath.exp(-s * t)
    return total * h / 3.0


# --- a few entries of the standard table  (the inverse pairs) ----------------
# F(s) for the common time functions, used to check laplace_numeric and to
# invert by inspection.  See Boas Table of Laplace Transforms, p.469.

def F_const(s):            return 1.0 / s                     # 1            <-> 1/s
def F_exp(a, s):           return 1.0 / (s - a)               # e^{at}       <-> 1/(s-a)
def F_pow(n, s):           return math.factorial(n) / s ** (n + 1)   # t^n   <-> n!/s^{n+1}
def F_cos(w, s):           return s / (s * s + w * w)         # cos wt       <-> s/(s^2+w^2)
def F_sin(w, s):           return w / (s * s + w * w)         # sin wt       <-> w/(s^2+w^2)


# --- convolution -------------------------------------------------------------

def convolve(f, g, t, N=2000):
    """Causal convolution  (f*g)(t) = int_0^t f(tau) g(t-tau) dtau  by Simpson.
    The convolution theorem says its transform is the product F(s) G(s)."""
    if t == 0.0:
        return 0.0
    if N % 2:
        N += 1
    h = t / N
    tot = 0.0
    for k in range(N + 1):
        tau = k * h
        w = 1.0 if k in (0, N) else (4.0 if k % 2 else 2.0)
        tot += w * f(tau) * g(t - tau)
    return tot * h / 3.0


# --- inversion by partial fractions over a quadratic -------------------------

def invert_quadratic(b1, b0, p, q):
    """Inverse transform of the rational function  (b1 s + b0) / (s^2 + p s + q).
    Returns the time function y(t) as a callable. This is the engine behind
    solving y'' + p y' + q y = 0: the three cases are the over/critically/under-
    damped responses (Boas Section 9). Roots of s^2+ps+q set the case."""
    disc = p * p - 4.0 * q
    if disc > 1e-14:                                    # real, distinct roots
        rt = math.sqrt(disc)
        r1, r2 = (-p + rt) / 2.0, (-p - rt) / 2.0
        A = (b1 * r1 + b0) / (r1 - r2)                  # partial fractions
        B = (b1 * r2 + b0) / (r2 - r1)
        return lambda t: A * math.exp(r1 * t) + B * math.exp(r2 * t)
    if disc < -1e-14:                                   # complex pair -> oscillation
        alpha = -p / 2.0
        beta = math.sqrt(-disc) / 2.0
        C = b1
        D = (b0 + b1 * alpha) / beta
        return lambda t: math.exp(alpha * t) * (C * math.cos(beta * t) + D * math.sin(beta * t))
    r = -p / 2.0                                        # repeated root
    return lambda t: (b1 + (b1 * r + b0) * t) * math.exp(r * t)


def solve_ivp_laplace(p, q, y0, v0, F0=0.0):
    """Solve  y'' + p y' + q y = F0  (constant forcing) with y(0)=y0, y'(0)=v0
    by the Laplace method:  (s^2+ps+q) Y(s) = (s+p) y0 + v0 + F0/s.
    Returns y(t). The constant forcing contributes the steady state y_p = F0/q;
    the rest is the homogeneous response with shifted initial conditions."""
    if abs(q) < 1e-300:
        raise ValueError("q = 0 puts a pole at the origin; not handled here")
    yp = F0 / q                                         # particular (steady state)
    Y0, V0 = y0 - yp, v0                                # homogeneous initial data
    homog = invert_quadratic(Y0, p * Y0 + V0, p, q)     # N(s) = (s+p)Y0 + V0
    return lambda t: yp + homog(t)


# --- independent check: RK4 on the same ODE ----------------------------------

def rk4(p, q, y0, v0, F0, t, n=4000):
    """Classic RK4 for y'' + p y' + q y = F0, returning y(t). Used in the tests
    as an independent check on the closed-form Laplace solution."""
    if t == 0.0:
        return y0
    h = t / n
    y, v = y0, v0
    acc = lambda yy, vv: F0 - p * vv - q * yy
    for _ in range(n):
        k1y, k1v = v, acc(y, v)
        k2y, k2v = v + 0.5 * h * k1v, acc(y + 0.5 * h * k1y, v + 0.5 * h * k1v)
        k3y, k3v = v + 0.5 * h * k2v, acc(y + 0.5 * h * k2y, v + 0.5 * h * k2v)
        k4y, k4v = v + h * k3v, acc(y + h * k3y, v + h * k3v)
        y += h / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y)
        v += h / 6.0 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return y


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-10 Laplace transforms -- demo")
    print("=" * 34)

    print("\nforward transform vs the table (s = 2):")
    s = 2.0
    rows = [
        ("1",        laplace_numeric(lambda t: 1.0, s),            F_const(s)),
        ("e^{-t}",   laplace_numeric(lambda t: math.exp(-t), s),   F_exp(-1.0, s)),
        ("t^2",      laplace_numeric(lambda t: t * t, s),          F_pow(2, s)),
        ("cos 3t",   laplace_numeric(lambda t: math.cos(3 * t), s), F_cos(3.0, s)),
    ]
    for name, num, exact in rows:
        print(f"  L[{name:7s}] = {num.real: .6f}   table = {exact: .6f}")

    print("\nconvolution theorem  (f=e^{-t}, g=e^{-2t}):")
    t = 1.3
    lhs = convolve(lambda u: math.exp(-u), lambda u: math.exp(-2 * u), t)
    closed = math.exp(-t) - math.exp(-2 * t)             # (f*g)(t) = e^{-t} - e^{-2t}
    print(f"  (f*g)({t}) = {lhs:.6f}   closed form = {closed:.6f}")

    print("\nIVP by Laplace vs RK4  --  y'' + 0.5 y' + 4 y = 0,  y(0)=1, y'(0)=0:")
    y = solve_ivp_laplace(0.5, 4.0, 1.0, 0.0)
    for tt in (0.5, 1.0, 2.0, 3.0):
        print(f"  t={tt}:  Laplace {y(tt): .6f}   RK4 {rk4(0.5, 4.0, 1.0, 0.0, 0.0, tt): .6f}")

    print("\nstep response  --  y'' + 0.5 y' + 4 y = 3,  y(0)=0, y'(0)=0  (steady state 3/4):")
    ystep = solve_ivp_laplace(0.5, 4.0, 0.0, 0.0, F0=3.0)
    print(f"  y(10) = {ystep(10.0):.4f}  (-> 0.75)")


if __name__ == "__main__":
    _demo()
