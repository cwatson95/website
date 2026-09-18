"""Tests for RE-04 time dilation, length contraction & simultaneity.

Run directly:   python3 test_sr_effects.py        (-> "All N tests passed.")
Or with pytest: pytest test_sr_effects.py

The checks are property-based and encode the physics, not the implementation:
time_dilation/proper_time and length_contraction/rest_length are exact inverses
with gamma>1; the time-dilation and length-contraction values are cross-checked
against an *inlined* Lorentz boost (the same boost read two ways); leading clocks
lag by beta*L0; relativistic muon survival beats the naive prediction; the
travelling twin returns younger (symmetry only as beta->0); the pole-in-barn
door-shuts are simultaneous in exactly one frame; and the boosted Minkowski axes
scissor toward the light line by equal angles (slopes 1/beta and beta).
"""
import math
import random

from sr_effects import (
    gamma,
    time_dilation, proper_time,
    length_contraction, rest_length,
    leading_clocks_lag,
    muon_fraction,
    twin_ages,
    pole_in_barn,
    boosted_axes,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _rand_beta(rng, hi=0.95):
    return rng.uniform(-hi, hi)


# Inlined Lorentz boost (c = 1) so the cross-checks lean on the definition, not on
# the module under test.  S' moves at +beta x_hat relative to S.
def _boost(ct, x, beta):
    """Forward boost  S -> S':  (ct', x') = (gamma(ct-beta x), gamma(x-beta ct))."""
    g = 1.0 / math.sqrt(1.0 - beta * beta)
    return g * (ct - beta * x), g * (x - beta * ct)


def _iboost(ctp, xp, beta):
    """Inverse boost  S' -> S  (flip beta):  ct = gamma(ct'+beta x')."""
    g = 1.0 / math.sqrt(1.0 - beta * beta)
    return g * (ctp + beta * xp), g * (xp + beta * ctp)


def test_time_dilation_and_proper_time_are_inverse():
    rng = random.Random(0)
    assert _approx(time_dilation(5.0, 0.0), 5.0)         # no motion -> no dilation
    assert _approx(proper_time(5.0, 0.0), 5.0)
    for _ in range(400):
        b = _rand_beta(rng)
        tau = rng.uniform(0.1, 10.0)
        dt = time_dilation(tau, b)                       # coord time for proper tau
        assert _approx(proper_time(dt, b), tau)          # exact inverses
        if abs(b) > 1e-6:
            assert dt > tau                              # gamma>1: moving clocks slow
        # a clock that moves for coordinate time T logs the smaller proper time T/gamma
        T = rng.uniform(0.1, 10.0)
        assert proper_time(T, b) <= T + TOL
        if abs(b) > 1e-6:
            assert proper_time(T, b) < T


def test_length_contraction_and_rest_length_are_inverse():
    rng = random.Random(1)
    assert _approx(length_contraction(2.0, 0.0), 2.0)    # no motion -> no contraction
    for _ in range(400):
        b = _rand_beta(rng)
        L0 = rng.uniform(0.1, 10.0)
        L = length_contraction(L0, b)
        assert _approx(rest_length(L, b), L0)            # exact inverses
        assert L <= L0 + TOL
        if abs(b) > 1e-6:
            assert L < L0                                # moving rods are shorter
        # contraction and dilation use the SAME gamma (one effect, two faces)
        assert _approx(length_contraction(L0, b) * time_dilation(1.0, b), L0)


def test_boost_cross_check_time_and_length():
    """Time dilation and length contraction are ONE boost read two ways."""
    rng = random.Random(2)
    for _ in range(400):
        b = _rand_beta(rng)
        # (a) a clock at rest at x'=0 ticks proper time tau: its two ticks are the
        # events (ct',x') = (0,0) and (tau,0).  Boost back to S:  ct = gamma(ct'+b x').
        tau = rng.uniform(0.1, 5.0)
        ct_S, _ = _iboost(tau, 0.0, b)
        assert _approx(ct_S, time_dilation(tau, b))      # ct = gamma*tau

        # (b) a rod of rest length L0 (ends at x'=0 and x'=L0).  Mark both ends at
        # one instant of S, ct=0; the far end then sits at x = L0/gamma.  Boost that
        # mark forward and it really is the x'=L0 end of the rod.
        L0 = rng.uniform(0.1, 5.0)
        x_far = length_contraction(L0, b)
        ctp, xp = _boost(0.0, x_far, b)
        assert _approx(xp, L0)                           # x' = gamma(x-beta ct) = L0
        if abs(b) > 1e-6:
            # ...but in S' the two end-marks are NOT simultaneous: that disagreement
            # is exactly why the moving observer disputes the contracted length.
            assert abs(ctp) > 1e-7


def test_leading_clocks_lag_sign_and_magnitude():
    rng = random.Random(3)
    assert _approx(leading_clocks_lag(3.0, 0.0), 0.0)    # at rest: stay synchronised
    for _ in range(400):
        b = _rand_beta(rng)
        L0 = rng.uniform(0.1, 10.0)
        lag = leading_clocks_lag(L0, b)
        assert _approx(lag, b * L0)                      # magnitude = beta * L0
        # cross-check via the boost: clocks at rest in S' at x'=0 and x'=L0 both read
        # t'=0.  At one instant of S (ct=0) the far clock sits at x = L0/gamma, and
        # its reading is  t' = gamma(ct - beta x) = -beta*L0:  the leading clock lags.
        x_far = L0 / gamma(b)
        ctp_far, _ = _boost(0.0, x_far, b)
        ctp_near, _ = _boost(0.0, 0.0, b)
        assert _approx(abs(ctp_far - ctp_near), abs(b) * L0)
        if b > 1e-6:                                     # +x motion: front clock behind
            assert ctp_far < ctp_near


def test_muon_relativistic_beats_naive():
    rng = random.Random(4)
    for _ in range(400):
        b = rng.uniform(0.05, 0.999)
        tau0 = rng.uniform(0.5, 5.0)
        # draw a measurable number of naive lifetimes en route (avoid underflow to 0)
        n_naive = rng.uniform(0.2, 25.0)
        dist = n_naive * b * tau0                        # so naive = exp(-n_naive)
        rel, naive = muon_fraction(tau0, b, dist)
        assert 0.0 < naive < rel <= 1.0                  # gamma>1 -> strictly more survive
        # match the closed forms exactly
        g = gamma(b)
        assert _approx(rel, math.exp(-dist / (g * b * tau0)))
        assert _approx(naive, math.exp(-dist / (b * tau0)))
        assert _approx(naive, math.exp(-n_naive))        # sanity on the construction
    # the headline (Rossi-Hall regime): naive predicts ~none, relativity predicts a few %
    rel, naive = muon_fraction(2.2, 0.98, 33.0)
    assert naive < 1e-4 < rel


def test_twin_traveller_is_younger_and_symmetric_only_at_low_beta():
    rng = random.Random(5)
    for _ in range(400):
        b = _rand_beta(rng, 0.999)
        T = rng.uniform(1.0, 100.0)
        home, trav = twin_ages(b, T)
        assert _approx(home, T)                          # home twin ages coord time
        assert _approx(trav, T / gamma(b))               # traveller ages proper time
        assert trav <= home + TOL
        if abs(b) > 1e-6:
            assert trav < home                           # traveller returns younger
    # the age gap vanishes as beta -> 0 (symmetry restored) and grows with beta
    h0, t0 = twin_ages(1e-4, 50.0)
    assert _approx(h0, t0, tol=1e-6)                     # ~equal ages at low speed
    gap = lambda b: twin_ages(b, 50.0)[0] - twin_ages(b, 50.0)[1]
    assert gap(0.3) < gap(0.6) < gap(0.9)                # monotone in beta


def test_pole_in_barn_simultaneity_is_frame_dependent():
    rng = random.Random(6)
    for _ in range(300):
        b = rng.uniform(0.05, 0.95)
        L0 = rng.uniform(1.0, 10.0)
        Lb = rng.uniform(1.0, 10.0)
        d = pole_in_barn(L0, Lb, b)
        assert _approx(d["contracted_pole"], L0 / gamma(b))
        assert d["fits_in_barn_frame"] == (L0 / gamma(b) <= Lb)
        # the two door-shuts are simultaneous in EXACTLY one frame
        zero_barn = abs(d["door_gap_barn"]) <= TOL
        zero_pole = abs(d["door_gap_pole"]) <= TOL
        assert zero_barn and not zero_pole               # 0 in barn, != 0 in pole
        assert zero_barn != zero_pole                    # exactly one frame's "now"
        assert _approx(d["door_gap_pole"], gamma(b) * b * Lb)
    # the classic case: fits in the barn frame, can't in the pole frame
    d = pole_in_barn(10.0, 10.0, 0.6)                     # gamma=1.25 -> pole -> 8
    assert d["fits_in_barn_frame"]                        # 8 <= 10
    assert _approx(d["door_gap_pole"], 1.25 * 0.6 * 10.0)  # 7.5, not simultaneous


def test_boosted_axes_scissor_equally_toward_light_line():
    rng = random.Random(7)
    for _ in range(400):
        b = rng.uniform(0.05, 0.95)
        ct_ax, x_ax = boosted_axes(b)
        assert _approx(ct_ax[0], 1.0) and _approx(ct_ax[1], b)   # ct'-axis dir (1,beta)
        assert _approx(x_ax[0], b) and _approx(x_ax[1], 1.0)     # x'-axis dir (beta,1)
        slope_ctp = ct_ax[0] / ct_ax[1]                  # ct/x, with ct drawn vertical
        slope_xp = x_ax[0] / x_ax[1]
        assert _approx(slope_ctp, 1.0 / b)               # ct'-axis slope 1/beta
        assert _approx(slope_xp, b)                      # x'-axis slope beta
        assert _approx(slope_ctp * slope_xp, 1.0)        # mirror images about ct=x
        # equal tilt: ct'-axis off the (vertical) ct-axis = x'-axis off the
        # (horizontal) x-axis = arctan(beta)
        tilt_ctp = math.atan2(ct_ax[1], ct_ax[0])
        tilt_xp = math.atan2(x_ax[0], x_ax[1])
        assert _approx(tilt_ctp, tilt_xp)
        assert _approx(tilt_ctp, math.atan(b))
        # both close in on, but never cross, the light line (slope 1)
        assert slope_xp < 1.0 < slope_ctp


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
