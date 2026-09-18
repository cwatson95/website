"""Tests for MA-15 Dirac delta & distributions. Pure stdlib.

Run:  python3 test_dirac_delta.py     ->  "All N tests passed."
"""
import math

from dirac_delta import (
    gaussian_delta, lorentzian_delta, box_delta, sinc_delta,
    heaviside, simpson, sift, delta_compose_rhs, delta_compose_integral,
    delta_prime_sift, fourier_delta_kernel,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


PHI = lambda x: math.cos(x) + 0.5 * x * x          # phi'(x) = -sin x + x


def test_nascent_normalization():
    # each nascent delta integrates to 1 (resolved windows)
    assert _approx(sift(lambda x: 1.0, 0.0, "gaussian", 0.1), 1.0, tol=1e-6)
    assert _approx(sift(lambda x: 1.0, 0.0, "box", 0.2), 1.0, tol=1e-12)
    # lorentzian has heavy tails -> only ~1 once the window is wide; looser tol
    assert _approx(sift(lambda x: 1.0, 0.0, "lorentzian", 0.1), 1.0, tol=2e-3)


def test_sift_converges_to_phi():
    # gaussian and box sift to phi(x0) as a -> 0
    for x0 in (0.0, 1.2, -0.8):
        target = PHI(x0)
        for kind in ("gaussian", "box"):
            errs = [abs(sift(PHI, x0, kind, a) - target) for a in (0.2, 0.05, 0.01)]
            assert errs[-1] < errs[0]                 # converging
            assert errs[-1] < 1e-3                    # and small


def test_sift_normalization_independent_of_a():
    for a in (0.3, 0.1, 0.03):
        assert _approx(sift(lambda x: 1.0, 0.0, "gaussian", a), 1.0, tol=1e-6)
        assert _approx(sift(lambda x: 1.0, 0.0, "box", a), 1.0, tol=1e-9)


def test_delta_composition():
    # delta(x^2 - c^2): roots +-c, |g'|=2c -> [phi(c)+phi(-c)]/(2c)
    c = 1.5
    g = lambda x: x * x - c * c
    gp = lambda x: 2 * x
    rhs = delta_compose_rhs(PHI, [c, -c], gp)
    vals = [delta_compose_integral(PHI, g, a, -4.0, 4.0) for a in (0.05, 0.01, 0.004)]
    assert abs(vals[-1] - rhs) < abs(vals[0] - rhs)   # converging to the closed form
    assert abs(vals[-1] - rhs) < 5e-3
    # a linear g(x)=2x-1 has one root 0.5, |g'|=2 -> phi(0.5)/2
    g2 = lambda x: 2 * x - 1
    rhs2 = delta_compose_rhs(PHI, [0.5], lambda x: 2.0)
    assert abs(delta_compose_integral(PHI, g2, 0.004, -3, 3) - rhs2) < 5e-3


def test_delta_prime_gives_minus_phi_prime():
    # int delta'(x) phi(x) dx = -phi'(0)
    for phi, dphi0 in [(PHI, (-math.sin(0) + 0.0)),         # phi'(0)=0
                       (lambda x: math.exp(-x), -1.0),       # psi'(0)=-1
                       (lambda x: math.sin(2 * x), 2.0)]:    # 2cos(0)=2
        vals = [delta_prime_sift(phi, a) for a in (0.2, 0.05, 0.02)]
        assert abs(vals[-1] - (-dphi0)) < 1e-3


def test_heaviside_derivative_is_delta():
    # <H', phi> = -<H, phi'> = -int_0^inf phi' = phi(0)  for decaying phi
    for phi, p0 in [(lambda x: math.exp(-x * x), 1.0),
                    (lambda x: math.exp(-abs(x)) * math.cos(x), 1.0)]:
        ibp = -simpson(lambda x: (phi(x + 1e-5) - phi(x - 1e-5)) / 2e-5, 0.0, 30.0, 20000)
        assert _approx(ibp, p0, tol=1e-3)
    # sanity on the step itself
    assert heaviside(-1) == 0.0 and heaviside(1) == 1.0 and heaviside(0) == 0.5


def test_fourier_kernel_sifts():
    # sin(Kx)/(pi x) -> delta(x): integral against a DECAYING phi -> phi(0) as K
    # grows. (The growing 0.5 x^2 part of PHI is not integrable against the sinc,
    # so use psi = e^{-x^2} cos x, psi(0)=1.)
    psi = lambda x: math.exp(-x * x) * math.cos(x)
    target = psi(0.0)
    errs = []
    for K in (20.0, 60.0, 150.0):
        val = simpson(lambda x: fourier_delta_kernel(x, K) * psi(x), -15.0, 15.0, 30000)
        errs.append(abs(val - target))
    assert errs[-1] < errs[0]            # converging as the cutoff grows
    assert errs[-1] < 3e-3


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
