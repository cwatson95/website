"""Tests for RE-07 relativistic Doppler effect & aberration.

Run directly:   python3 test_doppler_aberration.py     (-> "All N tests passed.")
Or with pytest: pytest test_doppler_aberration.py

The checks are property-based and physical: the longitudinal/transverse limits,
the blueshift/redshift signs, the aberration fixed points and beaming direction,
and -- the headline cross-check -- that a SINGLE Lorentz boost of the null
4-wavevector reproduces BOTH the Doppler factor (its frequency) and the aberration
formula (its direction) exactly, while keeping the ray null.
"""
import math
import random

from doppler_aberration import (
    gamma, bondi_k,
    doppler_longitudinal, doppler_general, doppler_transverse,
    aberration,
    four_wavevector, transform_wavevector, wavevector_frequency, wavevector_angle,
    headlight_halfangle,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _mink2(k):
    """Minkowski square k.k = -k0^2 + k1^2 + k2^2 + k3^2 (mostly plus). 0 if null."""
    return -k[0] ** 2 + k[1] ** 2 + k[2] ** 2 + k[3] ** 2


# --- Doppler: longitudinal ----------------------------------------------------

def test_longitudinal_rest_redshift_and_bondi():
    assert _approx(doppler_longitudinal(0.0), 1.0)              # no motion, no shift
    rng = random.Random(0)
    for _ in range(400):
        b = rng.uniform(1e-3, 0.999)
        assert doppler_longitudinal(b) < 1.0                   # receding -> redshift
        assert doppler_longitudinal(-b) > 1.0                  # approaching -> blueshift
        assert _approx(doppler_longitudinal(b) * bondi_k(b), 1.0)        # = 1/bondi_k
        assert _approx(doppler_longitudinal(b) * doppler_longitudinal(-b), 1.0)  # reciprocal
        # explicit closed form
        assert _approx(doppler_longitudinal(b), math.sqrt((1.0 - b) / (1.0 + b)))


# --- Doppler: transverse (pure time dilation) ---------------------------------

def test_transverse_is_time_dilation():
    rng = random.Random(1)
    for _ in range(400):
        b = rng.uniform(-0.999, 0.999)
        assert _approx(doppler_transverse(b), 1.0 / gamma(b))           # = 1/gamma
        assert _approx(doppler_transverse(b), doppler_general(b, math.pi / 2))
        if abs(b) > 1e-6:
            assert doppler_transverse(b) < 1.0                          # always a redshift


# --- Doppler: general angular formula and its limits --------------------------

def test_general_limits_match_longitudinal():
    rng = random.Random(2)
    for _ in range(400):
        b = rng.uniform(-0.99, 0.99)
        # theta = 0 -> blueshift sqrt((1+b)/(1-b));  theta = pi -> redshift sqrt((1-b)/(1+b))
        assert _approx(doppler_general(b, 0.0), math.sqrt((1.0 + b) / (1.0 - b)))
        assert _approx(doppler_general(b, math.pi), math.sqrt((1.0 - b) / (1.0 + b)))
        # consistency with the longitudinal factor (recede = theta = pi)
        assert _approx(doppler_general(b, math.pi), doppler_longitudinal(b))
        assert _approx(doppler_general(b, 0.0), 1.0 / doppler_longitudinal(b))
        # transverse slice
        assert _approx(doppler_general(b, math.pi / 2), doppler_transverse(b))
        # blueshift in the forward half, redshift in the backward half (beta > 0)
        if b > 1e-3:
            assert doppler_general(b, math.radians(30)) > 1.0
            assert doppler_general(b, math.radians(150)) < 1.0


# --- aberration: identity at rest, fixed points -------------------------------

def test_aberration_identity_and_fixed_points():
    rng = random.Random(3)
    for _ in range(400):
        th = rng.uniform(0.0, math.pi)
        assert _approx(aberration(th, 0.0), th)                # beta = 0: no aberration
    for _ in range(200):
        b = rng.uniform(-0.99, 0.99)
        assert _approx(aberration(0.0, b), 0.0)                # forward ray stays forward
        assert _approx(aberration(math.pi, b), math.pi)        # backward ray stays backward


# --- aberration: beaming direction --------------------------------------------

def test_aberration_beaming_direction():
    rng = random.Random(4)
    for _ in range(400):
        th = rng.uniform(1e-3, math.pi - 1e-3)
        b = rng.uniform(1e-3, 0.99)
        # +beta boost swings a ray towards theta = pi (apparent source motion in S');
        # the -beta boost (rest-frame -> lab) is the forward "headlight" beaming.
        assert aberration(th, b) > th
        assert aberration(th, -b) < th
        # the two boosts undo each other on the direction
        assert _approx(aberration(aberration(th, b), -b), th)


# --- the headline cross-check: k' = Lambda k gives Doppler AND aberration ------

def test_wavevector_encodes_doppler_and_aberration():
    """A single Lorentz boost of the null 4-wavevector reproduces, EXACTLY,
    doppler_general (from omega/omega') and aberration (from the new direction),
    and keeps k null."""
    rng = random.Random(5)
    for _ in range(600):
        b = rng.uniform(-0.95, 0.95)
        th = rng.uniform(0.0, math.pi)
        om = rng.uniform(0.5, 5.0)
        k = four_wavevector(om, th)
        assert _approx(_mink2(k), 0.0)                         # source ray is null
        kp = transform_wavevector(b, k)
        assert _approx(_mink2(kp), 0.0)                        # boosted ray still null
        # DOPPLER: the frequency ratio across the boost is the Doppler factor.
        omega, omega_p = wavevector_frequency(k), wavevector_frequency(kp)
        assert _approx(doppler_general(b, th), omega / omega_p)
        # ABERRATION: the emergent propagation direction obeys the aberration law.
        assert _approx(wavevector_angle(kp), aberration(th, b))


def test_four_wavevector_is_null():
    rng = random.Random(6)
    for _ in range(300):
        om = rng.uniform(0.1, 10.0)
        th = rng.uniform(0.0, math.pi)
        assert _approx(_mink2(four_wavevector(om, th)), 0.0)
        assert _approx(wavevector_angle(four_wavevector(om, th)), th)


# --- the headlight / beaming cone ---------------------------------------------

def test_headlight_halfangle_and_beaming():
    assert _approx(headlight_halfangle(0.0), math.pi / 2)      # isotropic at rest
    prev = math.pi / 2
    for b in (0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999):
        hc = headlight_halfangle(b)
        assert hc < prev                                       # cone tightens with beta
        assert _approx(hc, aberration(math.pi / 2, -b))        # = aberrated 90deg ray
        assert _approx(math.cos(hc), b)                        # cos(theta_c) = beta
        prev = hc
    assert headlight_halfangle(0.999999) < 1e-2                # -> 0 as beta -> 1


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
