"""
QM-18  Scattering theory -- the scattering amplitude f(theta), the cross-sections
it produces, partial-wave analysis with phase shifts, the optical theorem, and
the Born approximation, as closed-form objects you can evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-18).
Builds on ~QM-10 (the Legendre P_l / partial-wave machinery; its assoc_legendre
comes from ~MA-12, whose `legendre` this module imports for P_l(cos theta)) and
~QM-15 (the Born approximation is first-order perturbation theory).  It is the
quantum face of ~CM-08 (classical collisions, cross-sections, Rutherford): the
Born/Coulomb amplitude reproduces the SAME Rutherford dsigma/dOmega that CM-08
derives classically (Griffiths Example 10.6).

The story, each a function group below:
  1. Kinematics         -- the momentum transfer q = 2k sin(theta/2).
  2. Phase shifts       -- delta_l for a hard sphere (Dirichlet BC at r=a) and a
                           spherical square well (match log-derivatives at r=a).
  3. Partial waves      -- f(theta) = (1/k) sum (2l+1) e^{i d_l} sin d_l P_l(cos),
                           dsigma/dOmega = |f|^2, sigma = (4pi/k^2) sum (2l+1) sin^2 d_l.
  4. Optical theorem    -- sigma_tot = (4pi/k) Im f(0), an identity between the two.
  5. Born approximation -- f = -(m/2 pi hbar^2) int e^{i q.r} V d^3r, weak V;
                           the Yukawa potential gives f = -2 m beta/(hbar^2(mu^2+q^2)),
                           whose screened mu->0 limit is Rutherford 1/sin^4(theta/2).

UNITS: hbar = 2m = 1 (so 2m/hbar^2 = 1 and the energy is E = k^2).  In this
convention an attractive square well of depth V0 has interior wavenumber
k_in = sqrt(k^2 + V0), and the Born Yukawa amplitude is f = -beta/(mu^2 + q^2).
The Born functions keep the mass m and hbar as explicit (default m=1/2, hbar=1)
arguments so SI numbers can be restored by passing them.

scipy.special supplies the spherical Bessel functions j_l = spherical_jn and
n_l = spherical_yn (Griffiths' Neumann convention, n_0 = -cos x / x); ~MA-12
supplies the Legendre polynomials P_l.  See ../refs.md for page-verified
citations (Griffiths & Schroeter, Intro to QM, 3rd ed., Chapter 10).
"""

import math
import os
import sys

import numpy as np
from scipy.special import spherical_jn, spherical_yn
from scipy.integrate import quad

# ~MA-12 (Legendre polynomials) by relative path -- the same cross-link ~QM-10
# uses for assoc_legendre.  P_l(cos theta) is the angular building block of the
# partial-wave sum (Griffiths Eq. 10.25, p.486).  Once a shared `physkit`
# package exists this becomes `from physkit.special_functions import legendre`.
_HERE = os.path.dirname(os.path.abspath(__file__))
_MA12 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-12_special_functions", "code"))
if _MA12 not in sys.path:
    sys.path.insert(0, _MA12)

from special_functions import legendre as _ma12_legendre  # noqa: E402

__all__ = [
    # kinematics
    "momentum_transfer",
    # special-function helpers
    "P_l", "spherical_j", "spherical_n",
    # phase shifts
    "hard_sphere_phase_shift", "square_well_phase_shift",
    "phase_shifts_hard_sphere", "phase_shifts_square_well",
    # partial-wave amplitude & cross sections
    "partial_wave_amplitude", "differential_cross_section",
    "partial_cross_section", "total_cross_section",
    # optical theorem
    "optical_theorem_sigma",
    # Born approximation
    "born_amplitude_yukawa", "born_amplitude_radial", "rutherford_cross_section",
]


# --- 1. kinematics -----------------------------------------------------------

def momentum_transfer(theta, k):
    """Magnitude of the momentum transfer  q = |k0 - k| = 2 k sin(theta/2).

    k0 (incident) and k (scattered) both have length k; theta is the angle
    between them, so the chord length is 2 k sin(theta/2) (Griffiths Eq. 10.89,
    p.500).  q = 0 forward (theta=0), q = 2k backward (theta=pi).  This single
    variable carries all the angle dependence of the Born amplitude for a
    spherically symmetric potential."""
    return 2.0 * k * np.sin(np.asarray(theta, dtype=float) / 2.0)


# --- 2. special-function helpers --------------------------------------------

def P_l(l, x):
    """Legendre polynomial P_l(x), vectorized over x, via ~MA-12's `legendre`.
    These are the angular eigenfunctions of ~QM-10 (P_l(cos theta) is Y_l^0 up
    to normalization); orthogonality of the P_l is what collapses the partial-
    wave sum for the total cross-section (Griffiths Eq. 4.34 used at Eq. 10.27)."""
    f = np.vectorize(lambda t: _ma12_legendre(int(l), float(t)))
    return f(np.asarray(x, dtype=float))


def spherical_j(l, x):
    """Spherical Bessel function j_l(x) (regular at the origin)."""
    return spherical_jn(int(l), x)


def spherical_n(l, x):
    """Spherical Neumann function n_l(x) (Griffiths' convention, n_0 = -cos x/x;
    == scipy.special.spherical_yn).  Irregular at the origin, allowed in the
    exterior region r > a where the wave function need not be finite at r=0."""
    return spherical_yn(int(l), x)


# --- 3. phase shifts ---------------------------------------------------------

def hard_sphere_phase_shift(l, k, a):
    """Partial-wave phase shift for a hard sphere of radius a (V = +infinity for
    r < a, 0 outside), Griffiths Example 10.3 / Problem 10.6.

    The exterior radial function cos(d_l) j_l(kr) - sin(d_l) n_l(kr) must vanish
    at r = a (Dirichlet boundary), giving

        tan d_l = j_l(ka) / n_l(ka).

    With the standard (Griffiths/scipy) Neumann sign n_0 = -cos x/x this returns
    the physical s-wave result d_0 = -ka (the hard core simply pushes the wave
    out by a).  Some texts write d_l = -arctan(j_l/n_l); that is the same number
    under the opposite sign convention for n_l.  Only sin^2 d_l (hence sigma) and
    the relative phases in f(theta) are observable -- d_l itself is defined mod pi.
    """
    x = k * a
    return np.arctan(spherical_j(l, x) / spherical_n(l, x))


def square_well_phase_shift(l, k, a, V0):
    """Partial-wave phase shift for a spherical square well of radius a and depth
    V0 (attractive: V = -V0 for r < a, 0 outside; pass V0 > 0).  Griffiths
    §10.2.2 strategy: match the interior solution j_l(k_in r) -- regular at the
    origin -- to the exterior cos(d_l) j_l(kr) - sin(d_l) n_l(kr) by requiring the
    logarithmic derivative R'/R to be continuous at r = a.

    With hbar = 2m = 1 the interior wavenumber is k_in = sqrt(k^2 + V0).  Writing
    the dimensionless interior log-derivative  L = (k_in a) j_l'(k_in a)/j_l(k_in a),
    continuity of R'/R at a gives

        tan d_l = [ L j_l(ka) - (ka) j_l'(ka) ] / [ L n_l(ka) - (ka) n_l'(ka) ].

    Two checks built into the tests: V0 -> 0 gives d_l -> 0 (no potential, no
    scattering); the s-wave matches the closed form d_0 = -ka + arctan((k/k_in)
    tan(k_in a)); and L -> infinity (Dirichlet) recovers the hard sphere above.
    """
    k_in = math.sqrt(k * k + V0)
    x, xin = k * a, k_in * a
    jin = spherical_jn(int(l), xin)
    jin_p = spherical_jn(int(l), xin, derivative=True)
    L = xin * jin_p / jin
    jl = spherical_jn(int(l), x)
    jl_p = spherical_jn(int(l), x, derivative=True)
    nl = spherical_yn(int(l), x)
    nl_p = spherical_yn(int(l), x, derivative=True)
    num = L * jl - x * jl_p
    den = L * nl - x * nl_p
    return math.atan2(num, den)


def phase_shifts_hard_sphere(k, a, lmax):
    """Array [d_0, d_1, ..., d_lmax] of hard-sphere phase shifts."""
    return np.array([hard_sphere_phase_shift(l, k, a) for l in range(lmax + 1)])


def phase_shifts_square_well(k, a, V0, lmax):
    """Array [d_0, ..., d_lmax] of square-well phase shifts."""
    return np.array([square_well_phase_shift(l, k, a, V0) for l in range(lmax + 1)])


# --- 4. partial-wave amplitude and cross-sections ----------------------------

def partial_wave_amplitude(theta, k, deltas):
    """Scattering amplitude from the partial-wave (phase-shift) expansion
    (Griffiths Eq. 10.47, p.491):

        f(theta) = (1/k) sum_l (2l+1) e^{i d_l} sin(d_l) P_l(cos theta).

    `deltas` is the sequence [d_0, d_1, ...]; the sum runs over the supplied
    partial waves.  Returns a complex amplitude (array if theta is an array).
    dsigma/dOmega = |f|^2 (Griffiths Eq. 10.14)."""
    theta = np.asarray(theta, dtype=float)
    cos_t = np.cos(theta)
    f = np.zeros_like(cos_t, dtype=complex)
    for l, d in enumerate(deltas):
        f = f + (2 * l + 1) * np.exp(1j * d) * np.sin(d) * P_l(l, cos_t)
    return f / k


def differential_cross_section(theta, k, deltas):
    """Differential cross-section dsigma/dOmega = |f(theta)|^2 (Griffiths Eq.
    10.14, p.481), with f from the partial-wave sum."""
    f = partial_wave_amplitude(theta, k, deltas)
    return np.abs(f) ** 2


def partial_cross_section(l, k, delta_l):
    """The contribution of a single partial wave to the total cross-section,
    sigma_l = (4pi/k^2)(2l+1) sin^2(d_l).  Bounded above by 4pi(2l+1)/k^2 (the
    unitarity bound, saturated at d_l = pi/2 -- a resonance)."""
    return 4.0 * math.pi / k ** 2 * (2 * l + 1) * math.sin(delta_l) ** 2


def total_cross_section(k, deltas):
    """Total cross-section from the phase shifts (Griffiths Eq. 10.48, p.491):

        sigma = (4pi/k^2) sum_l (2l+1) sin^2(d_l).

    The cross-terms drop out by orthogonality of the P_l, so the total is a sum
    of independent partial-wave contributions."""
    return sum(partial_cross_section(l, k, d) for l, d in enumerate(deltas))


# --- 5. optical theorem ------------------------------------------------------

def optical_theorem_sigma(k, deltas):
    """Total cross-section via the OPTICAL THEOREM (Griffiths Problem 10.19,
    p.504):

        sigma_tot = (4pi/k) Im f(0).

    At theta = 0 every P_l(1) = 1, so Im f(0) = (1/k) sum (2l+1) sin^2 d_l, and
    (4pi/k) Im f(0) reproduces total_cross_section EXACTLY.  Returned separately
    so the test can confirm the two formulas agree (a statement of probability
    conservation: forward interference removes from the beam exactly what is
    scattered into all angles)."""
    f0 = partial_wave_amplitude(0.0, k, deltas)
    return 4.0 * math.pi / k * np.imag(f0)


# --- 6. Born approximation ---------------------------------------------------

def born_amplitude_yukawa(theta, k, beta, mu, m=0.5, hbar=1.0):
    """First Born amplitude for the Yukawa (screened-Coulomb) potential
    V(r) = beta e^{-mu r} / r  (Griffiths Example 10.5, Eq. 10.91, p.500):

        f(theta) = - (2 m beta / hbar^2) / (mu^2 + q^2),    q = 2k sin(theta/2).

    Defaults m=1/2, hbar=1 (the hbar=2m=1 units of this module), for which
    f = -beta/(mu^2+q^2).  mu is the inverse screening length: mu>0 keeps f finite
    in the forward direction (f(0) = -2m beta/(hbar^2 mu^2)), while mu->0 (the bare
    Coulomb limit) makes f(0) diverge -- the long range of 1/r."""
    q = momentum_transfer(theta, k)
    return -(2.0 * m * beta / hbar ** 2) / (mu ** 2 + q ** 2)


def born_amplitude_radial(theta, k, V_func, m=0.5, hbar=1.0, r_max=np.inf):
    """First Born amplitude for ANY spherically symmetric V(r), by the reduced
    radial integral (Griffiths Eq. 10.88, p.500):

        f(theta) = -(2m/hbar^2 q) int_0^inf r V(r) sin(q r) dr,   q = 2k sin(theta/2)

    which is the angular reduction of the 3-D Born formula
    f = -(m/2 pi hbar^2) int e^{i q.r} V(r) d^3r (Griffiths Eq. 10.79, p.499).
    Evaluated numerically (scipy.integrate.quad).  Used in the tests to confirm
    that this integral reproduces born_amplitude_yukawa in closed form.  In the
    forward limit q -> 0, sin(qr)/q -> r, so f(0) = -(2m/hbar^2) int r^2 V dr."""
    q = float(momentum_transfer(theta, k))
    pref = -2.0 * m / hbar ** 2
    if q == 0.0:
        I, _ = quad(lambda r: r * r * V_func(r), 0.0, r_max)
        return pref * I
    I, _ = quad(lambda r: r * V_func(r) * math.sin(q * r), 0.0, r_max)
    return pref * I / q


def rutherford_cross_section(theta, k, beta, m=0.5, hbar=1.0):
    """Rutherford differential cross-section, the bare-Coulomb (mu->0) limit of
    Yukawa (Griffiths Example 10.6, Eq. 10.93, p.501):

        dsigma/dOmega = (2 m beta / hbar^2)^2 / (2k sin(theta/2))^4
                      = (2 m beta / hbar^2)^2 / q^4.

    With hbar=2m=1 and E=k^2 this is beta^2/(16 E^2 sin^4(theta/2)).  beta =
    q1 q2 / 4 pi eps0 is the Coulomb strength.  This is identical to the CLASSICAL
    result derived in ~CM-08 -- the famous robustness of Rutherford's formula
    (classical mechanics, the Born approximation and QED all agree)."""
    q = momentum_transfer(theta, k)
    return (2.0 * m * beta / hbar ** 2) ** 2 / q ** 4


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-18 Scattering -- amplitude, phase shifts, optical theorem, Born\n")

    a = 1.0
    print("Hard sphere (radius a=1), low-energy limit ka -> 0:")
    for ka in (0.3, 0.1, 0.03):
        k = ka / a
        ds = phase_shifts_hard_sphere(k, a, lmax=6)
        sig = total_cross_section(k, ds)
        print("  ka=%.2f: d_0=%+.4f (-ka=%+.4f),  sigma=%.4f,  sigma/(pi a^2)=%.4f"
              % (ka, ds[0], -ka, sig, sig / (math.pi * a ** 2)))
    print("  -> sigma -> 4 pi a^2 = %.4f : FOUR times the classical shadow pi a^2."
          % (4 * math.pi * a ** 2))

    print("\nSpherical square well (a=1, depth V0=4), k=1.5:")
    k, V0 = 1.5, 4.0
    ds = phase_shifts_square_well(k, a, V0, lmax=6)
    print("  phase shifts d_l =", np.array2string(ds, precision=3))
    sig = total_cross_section(k, ds)
    sig_opt = optical_theorem_sigma(k, ds)
    print("  sigma (sum sin^2) = %.5f" % sig)
    print("  sigma (4pi/k Im f(0)) = %.5f   <- optical theorem agrees" % sig_opt)

    print("\nBorn approximation, Yukawa V = beta e^{-mu r}/r (beta=1, mu=0.7), k=2:")
    k, beta, mu = 2.0, 1.0, 0.7
    for th in (0.3, math.pi / 2, math.pi):
        f = born_amplitude_yukawa(th, k, beta, mu)
        print("  theta=%4.0f deg: f=%+.5f  |f|^2=%.5f"
              % (math.degrees(th), f, abs(f) ** 2))
    print("  forward-peaked: |f| largest at theta=0.")
    print("  screened mu->0 -> Rutherford dsigma/dOmega ~ 1/sin^4(theta/2):")
    for th in (math.pi / 6, math.pi / 2):
        print("    theta=%4.0f deg: dsigma/dOmega=%.5f, *sin^4(th/2)=%.5f (const)"
              % (math.degrees(th), rutherford_cross_section(th, k, beta),
                 rutherford_cross_section(th, k, beta) * math.sin(th / 2) ** 4))


if __name__ == "__main__":
    _demo()
