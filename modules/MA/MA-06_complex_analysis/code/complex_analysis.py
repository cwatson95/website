"""
MA-06  Complex analysis -- analytic functions, Cauchy-Riemann, contour
integration, the Cauchy integral formula, residues and the residue theorem.

Part of the physics topic network (modules/topic_network.txt, module MA-06).
Builds on ~MA-05 (complex numbers); feeds ~QM-19 (propagators / Green's
functions), ~EM-15 (dispersion relations, Kramers-Kronig).

A complex function is f: C -> C, i.e. f(z) with z a Python complex. Contours are
functions gamma(t) -> complex on a parameter interval. The contour integral
   integral_gamma f dz = int_a^b f(gamma(t)) gamma'(t) dt
is evaluated by the trapezoidal rule (spectrally accurate on smooth closed
loops), and residues / winding numbers / the Cauchy formula are built on it.

Pure stdlib (cmath).
"""

import cmath
import math

__all__ = [
    "cauchy_riemann", "complex_derivative", "contour_integral", "circle",
    "winding_number", "residue_at", "cauchy_integral_formula",
]


def cauchy_riemann(f, z, h=1e-6, tol=1e-5):
    """True if f satisfies the Cauchy-Riemann equations at z (=> analytic there):
    with f = u + i v,  u_x = v_y  and  u_y = -v_x."""
    fx_p, fx_m = f(z + h), f(z - h)            # vary the real part
    fy_p, fy_m = f(z + 1j * h), f(z - 1j * h)  # vary the imaginary part
    ux = (fx_p.real - fx_m.real) / (2 * h)
    vx = (fx_p.imag - fx_m.imag) / (2 * h)
    uy = (fy_p.real - fy_m.real) / (2 * h)
    vy = (fy_p.imag - fy_m.imag) / (2 * h)
    return abs(ux - vy) < tol and abs(uy + vx) < tol


def complex_derivative(f, z, h=1e-6):
    """f'(z). For an analytic f the limit is direction-independent, so a real
    step suffices: (f(z+h) - f(z-h)) / 2h."""
    return (f(z + h) - f(z - h)) / (2.0 * h)


def contour_integral(f, gamma, a, b, n=4000):
    """integral over the contour gamma(t), t in [a,b], of f(z) dz
    = int_a^b f(gamma(t)) gamma'(t) dt  (trapezoidal rule)."""
    hh = 1e-7

    def integrand(t):
        gp = (gamma(t + hh) - gamma(t - hh)) / (2.0 * hh)   # gamma'(t)
        return f(gamma(t)) * gp

    dt = (b - a) / n
    total = 0.5 * (integrand(a) + integrand(b))
    for k in range(1, n):
        total += integrand(a + k * dt)
    return total * dt


def circle(z0, r):
    """The positively-oriented circle |z - z0| = r as a contour gamma(t), t in [0, 2pi]."""
    return lambda t: z0 + r * cmath.exp(1j * t)


def winding_number(gamma, z0, a=0.0, b=2.0 * math.pi, n=4000):
    """n(gamma, z0) = (1/2pi i) * contour integral of dz/(z - z0)  (an integer)."""
    val = contour_integral(lambda z: 1.0 / (z - z0), gamma, a, b, n) / (2j * math.pi)
    return val.real          # imaginary part is ~0


def residue_at(f, z0, r=1e-2, n=4000):
    """Residue of f at the isolated singularity z0:
    Res = (1/2pi i) * (integral of f around a small circle |z - z0| = r)."""
    return contour_integral(f, circle(z0, r), 0.0, 2.0 * math.pi, n) / (2j * math.pi)


def cauchy_integral_formula(f, z0, r=0.5, n=4000):
    """Cauchy's integral formula: for f analytic inside the circle |z - z0| = r,
    f(z0) = (1/2pi i) * integral of f(z)/(z - z0) dz."""
    return contour_integral(lambda z: f(z) / (z - z0), circle(z0, r), 0.0, 2.0 * math.pi, n) / (2j * math.pi)


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-06 complex analysis -- demo")
    print("=" * 32)

    print("Cauchy-Riemann (analytic?):")
    print("  f(z)=z^2     :", cauchy_riemann(lambda z: z * z, 1 + 1j))
    print("  f(z)=e^z     :", cauchy_riemann(cmath.exp, 0.3 + 0.7j))
    print("  f(z)=conj(z) :", cauchy_riemann(lambda z: z.conjugate(), 1 + 1j))

    print("\nf'(z): d/dz z^3 at z=2 =", complex_derivative(lambda z: z ** 3, 2 + 0j), " (= 12)")

    unit = circle(0, 1)
    print("\nCauchy integral theorem (analytic -> 0):")
    print("  oint z^2 dz   =", contour_integral(lambda z: z * z, unit, 0, 2 * math.pi), " (~ 0)")
    print("  oint 1/z dz   =", contour_integral(lambda z: 1 / z, unit, 0, 2 * math.pi), " (= 2*pi*i)")

    print("\nwinding number of the unit circle:")
    print("  about 0  =", round(winding_number(unit, 0.0), 6), " (= 1)")
    print("  about 2  =", round(winding_number(unit, 2.0), 6), " (= 0)")

    print("\nresidues:")
    print("  Res 1/(z-1) at 1   =", residue_at(lambda z: 1 / (z - 1), 1 + 0j))
    print("  Res 1/(z^2+1) at i =", residue_at(lambda z: 1 / (z * z + 1), 1j), " (= 1/2i = -0.5i)")

    print("\nCauchy integral formula  f(z0) = (1/2pi i) oint f/(z-z0):")
    print("  f=e^z, z0=0 ->", cauchy_integral_formula(cmath.exp, 0 + 0j), " (= 1)")


if __name__ == "__main__":
    _demo()
