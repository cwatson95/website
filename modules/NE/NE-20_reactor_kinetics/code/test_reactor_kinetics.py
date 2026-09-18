"""NE-20 tests -- reactor kinetics against Shultis & Faw §§10.7-10.9 and
Addenda 2-3, Table 10.9, Examples 10.11-10.12, and Chapter 10 problems 24-30.

Run:  python3 test_reactor_kinetics.py
"""

import math

from reactor_kinetics import (
    DELAYED_GROUPS, BETA, SIGMA_A_XE135_B, GAMMA_I, GAMMA_X, LAMBDA_I, LAMBDA_X,
    GAMMA_PM149, SIGMA_A_SM149_B, LAMBDA_PM,
    beta_total, relative_yields, decay_constants, mean_precursor_lifetime,
    mean_precursor_half_life, reactivity, keff_from_reactivity, dollars,
    keff_from_dollars, pcm, prompt_generation_time, effective_generation_time,
    simple_period, small_insertion_period, prompt_critical_period,
    inhour, asymptotic_period, one_group_omegas, step_response,
    prompt_jump_factor, solve_point_kinetics,
    poison_reactivity, iodine_xenon_equilibrium, xenon_transient,
    xenon_reactivity, time_to_poison, promethium_samarium_equilibrium,
    samarium_transient, temperature_coefficient, is_self_regulating,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- delayed neutrons ----------------------------------------------------

def test_table_10_9_sums_and_the_plutonium_problem():
    """Table 10.9's six groups sum to the printed totals for all three nuclides,
    and the relative yields sum to 1.

    The consequence S&F draw is operational: beta falls from 0.0065 for 235U to
    0.0021 for 239Pu, so as plutonium builds in over a fuel cycle the SAME delta-k
    is worth three times as many dollars, and the reactor becomes markedly more
    responsive to reactivity changes near end of life."""
    for nuc, printed in BETA.items():
        assert _rel(beta_total(nuc), printed, 2e-2), \
            "%s: %.5f vs %.4f" % (nuc, beta_total(nuc), printed)
        assert _rel(sum(relative_yields(nuc)), 1.0, 1e-12)
        assert len(DELAYED_GROUPS[nuc]) == 6
    assert beta_total("235U") > beta_total("233U") > beta_total("239Pu")
    assert _rel(beta_total("235U") / beta_total("239Pu"), 3.1, 0.05)
    # a 300 pcm insertion is 0.46$ in fresh fuel and 1.4$ -- prompt critical --
    # in pure plutonium
    assert dollars(300e-5, "235U") < 0.5
    assert dollars(300e-5, "239Pu") > 1.0


def test_the_mean_precursor_lifetime_is_the_control_time_scale():
    """tau = sum a_i/lambda_i = 12.95 s for 235U (S&F quote 12.8 s from an
    average 8.8 s half-life; the six groups give 8.98 s).

    This is the number that makes reactors possible: it is FIVE ORDERS OF
    MAGNITUDE longer than the ~1e-4 s prompt cycle, and it is what the effective
    generation time is dominated by."""
    tau = mean_precursor_lifetime()
    assert _rel(tau, 12.95, 5e-3), "%.3f s" % tau
    assert _rel(tau, 12.8, 0.02)                      # the printed value
    assert _rel(mean_precursor_half_life(), 8.98, 5e-3)
    assert _rel(mean_precursor_half_life(), 8.8, 0.03)
    # the longest-lived group dominates the tail, not the mean
    a, lam = relative_yields(), decay_constants()
    contributions = [ai / li for ai, li in zip(a, lam)]
    assert contributions.index(max(contributions)) == 1   # group 2, 22.7 s
    assert _rel(max(contributions) / tau, 0.55, 0.05)
    # the effective generation time is beta*tau, not l0
    l_eff = effective_generation_time(1e-4)
    assert _rel(l_eff, 1e-4 + 0.0065 * tau, 1e-9)
    assert _rel(l_eff / prompt_generation_time(1e-4), 843.0, 0.02)


def test_why_a_prompt_only_reactor_would_be_uncontrollable():
    """S&F Eqs. (10.29) and (10.34), the comparison the whole subject rests on.
    Same reactor, same delta_k = 0.001, two models."""
    t_prompt = simple_period(0.001, 1e-4)
    assert _approx(t_prompt, 0.1)
    assert _rel(math.exp(1.0 / t_prompt), 22026.0, 1e-3)      # ~20 000 in 1 s
    # with delayed neutrons: T = beta*tau/delta_k
    t_delayed = 0.0065 * mean_precursor_lifetime() / 0.001
    assert _rel(t_delayed, 84.2, 5e-3), "%.2f s" % t_delayed
    assert _rel(t_delayed, 83.0, 0.02)                        # S&F's 83 s
    assert _rel(math.exp(1.0 / t_delayed), 1.012, 2e-3)
    assert t_delayed / t_prompt > 800
    try:
        simple_period(0.0, 1e-4)
    except ValueError:
        pass
    else:
        raise AssertionError("a critical reactor has no finite period")


# --- reactivity units and the worked examples ----------------------------

def test_reproduces_examples_10_11_and_10_12():
    """S&F Ex. 10.11: 0.1$ into a critical reactor gives k_eff = 1.00065.
    Ex. 10.12: 10 W to 10 kW then takes 884 s.

    (Example 10.12 refers to "the reactor of Example 10.7" twice. Example 10.7 is
    the fast-fission-factor calculation of §10.4; the 0.1$ insertion and the
    delta_k = 0.00065 it quotes are Example 10.11's.)"""
    k = keff_from_dollars(0.1)
    assert _rel(k, 1.00065, 1e-5), "%.6f" % k
    assert _rel(k - 1.0, 0.00065, 1e-3)
    assert _rel(dollars(reactivity(k)), 0.1, 1e-9)
    t = small_insertion_period(0.1)
    assert _rel(t, 129.5, 5e-3), "%.2f s" % t
    assert _rel(t, 128.0, 0.02)                       # the printed value
    elapsed = t * math.log(10000.0 / 10.0)
    assert _rel(elapsed, 894.6, 5e-3), "%.1f s" % elapsed
    assert _rel(elapsed, 884.0, 0.02)
    # reactivity unit round trips
    for kk in (0.999, 1.0, 1.002):
        assert _rel(keff_from_reactivity(reactivity(kk)), kk, 1e-12)
    assert _rel(pcm(0.00065), 65.0, 1e-9)
    try:
        keff_from_dollars(200.0)
    except ValueError:
        pass
    else:
        raise AssertionError("beta k($) >= 1 should be refused")


def test_the_small_insertion_formula_is_already_32_percent_high_at_0_1_dollars():
    """S&F use T = beta*tau/delta_k at 0.1$ (Example 10.12) and get 128 s. The
    exact inhour equation gives 98 s.

    The approximation replaces sum a_i/(lambda_i + omega) by sum a_i/lambda_i,
    which needs omega << lambda_min = 0.0124 s^-1, i.e. T >> 80 s. At 0.1$ the
    true period is 98 s -- barely above that floor -- so the approximation is
    already at the edge of its validity where the book applies it. It is not an
    erratum; it is an approximation whose error is worth knowing."""
    exact = asymptotic_period(0.1, 1e-4)
    approx = small_insertion_period(0.1)
    assert _rel(exact, 98.1, 5e-3), "%.2f s" % exact
    assert _rel(approx / exact, 1.32, 0.02)
    # the error shrinks as the insertion does, as it must
    errs = [abs(small_insertion_period(k) / asymptotic_period(k, 1e-4) - 1.0)
            for k in (0.001, 0.01, 0.1, 0.3)]
    assert errs == sorted(errs)
    assert errs[0] < 0.01 and errs[-1] > 0.5
    # and the inhour function is the definition it is measured against
    for k in (0.05, 0.2, 0.8):
        w = 1.0 / asymptotic_period(k, 1e-4)
        assert _rel(inhour(w, 1e-4), k, 1e-6)


def test_the_prompt_critical_cliff():
    """At k($) = 1 the prompt neutrons alone sustain the chain and the period
    stops being set by precursor decay and starts being set by the ~1e-4 s
    prompt lifetime. The period falls by three orders of magnitude across a
    factor of ten in reactivity."""
    periods = [asymptotic_period(k, 1e-4) for k in (0.1, 0.5, 0.9, 1.5, 5.0)]
    assert periods == sorted(periods, reverse=True)
    assert _rel(periods[0] / periods[-1], 2.55e4, 0.05)
    assert asymptotic_period(0.9, 1e-4) > 0.4
    assert asymptotic_period(1.5, 1e-4) < 0.05
    # above prompt critical the period IS proportional to the prompt lifetime
    for l0 in (1e-4, 1e-3):
        assert _rel(prompt_critical_period(2.0, l0), (l0 / 0.0065) / 1.0, 1e-12)
    assert _rel(asymptotic_period(5.0, 1e-4) / asymptotic_period(5.0, 2e-4),
                0.5, 0.05)
    # ...and below it, it is nearly independent of the prompt lifetime
    assert _rel(asymptotic_period(0.1, 1e-4) / asymptotic_period(0.1, 1e-3),
                1.0, 0.02)
    for bad in ((0.5, 1e-4), (1.0, 1e-4)):
        try:
            prompt_critical_period(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be refused" % (bad,))


def test_the_period_formula_refuses_to_cross_prompt_critical():
    """The dangerous failure mode: Eq. (10.33) does not blow up at 1$, it just
    keeps returning a comfortable-looking number. At 1.5$ it would report 8.6 s
    where the truth is 0.03 s -- a 280-fold error in the direction of 'there is
    plenty of time'."""
    would_be = mean_precursor_lifetime() / 1.5
    truth = asymptotic_period(1.5, 1e-4)
    assert _rel(would_be / truth, 287.0, 0.05), "%.1f" % (would_be / truth)
    for k in (0.5, 1.0, 1.5, -2.0):
        try:
            small_insertion_period(k)
        except ValueError as exc:
            assert "prompt" in str(exc) or "exceeds" in str(exc)
        else:
            raise AssertionError("k($) = %g should be refused" % k)
    small_insertion_period(0.3)             # the stated boundary is allowed
    small_insertion_period(-0.2)


def test_shutdown_cannot_beat_the_longest_lived_precursor():
    """However much negative reactivity is inserted, the power cannot fall faster
    than the decay of the 55.7 s precursor group -- about -80 s per e-fold
    [S&F §10.7.4].

    This is why decay-heat removal is not optional, and it is the physics behind
    every loss-of-cooling accident: you can stop the chain reaction in
    milliseconds and you still cannot stop the heat."""
    floor = -55.7 / math.log(2.0)
    assert _rel(floor, -80.4, 1e-3)
    periods = [asymptotic_period(k, 1e-4) for k in (-1.0, -5.0, -20.0, -100.0, -1e4)]
    for p in periods:
        assert p < 0
        assert p <= floor + 1e-6, "%.2f s beats the precursor floor" % p
    # and it converges to the floor from below
    assert _rel(periods[-1], floor, 1e-3)
    assert periods[0] < periods[-1]                # -83.5 s is slower than -80.4
    # a scram to 0.01% of full power takes minutes, not seconds
    assert -periods[-1] * math.log(1e4) > 600.0


# --- the point kinetics equations ----------------------------------------

def test_point_kinetics_integrates_to_the_right_asymptote():
    """The G-group equations (10.86) integrated by RK4. Three checks: a zero
    insertion stays flat (the initial precursor equilibrium is right), a positive
    insertion approaches the inhour asymptotic period, and the prompt jump
    appears on the way."""
    sol = solve_point_kinetics(lambda t: 0.0, 1e-4, 20.0, dt=1e-3)
    assert _rel(sol[-1][1], 1.0, 1e-6), "%.6f" % sol[-1][1]

    rho = 0.1 * BETA["235U"]
    sol = solve_point_kinetics(lambda t: rho, 1e-4, 200.0, dt=5e-4)
    ts = [t for t, _ in sol]
    ns = [n for _, n in sol]
    # asymptotic slope over the last 50 s
    i0 = min(range(len(ts)), key=lambda i: abs(ts[i] - 150.0))
    t_num = (ts[-1] - ts[i0]) / math.log(ns[-1] / ns[i0])
    assert _rel(t_num, asymptotic_period(0.1, 1e-4), 0.02), "%.2f s" % t_num
    # the prompt jump: within a second the level is already up by ~1/(1-k$)
    i1 = min(range(len(ts)), key=lambda i: abs(ts[i] - 1.0))
    assert 1.05 < ns[i1] < 1.20
    assert ns[i1] > 1.0


def test_the_one_group_step_response_and_the_prompt_jump():
    """S&F Addendum 3, Eqs. (10.96)-(10.108). The response is a fast prompt jump
    by 1/(1 - k($)) followed by a slow exponential.

    For a NEGATIVE insertion the same factor is a prompt DROP: a -1$ scram cuts
    the power in half within a fraction of a second and then decays with the
    precursors, which is exactly the shape Fig. 10.8 shows."""
    for k in (0.1, 0.25, 0.5):
        w1, w2 = one_group_omegas(k, 1e-4)
        assert w1 > 0 > w2
        assert abs(w2) > 100 * abs(w1)              # w2 is the prompt root
        # after the prompt root has died but before the slow one has moved
        n = step_response(0.5, k, 1e-4)
        assert _rel(n, prompt_jump_factor(k), 0.15), \
            "k=%g: %.4f vs %.4f" % (k, n, prompt_jump_factor(k))
    # negative: a prompt drop
    assert _rel(prompt_jump_factor(-1.0), 0.5, 1e-12)
    n = step_response(0.5, -1.0, 1e-4)
    assert 0.4 < n < 0.6
    # both roots negative for a negative insertion
    w1, w2 = one_group_omegas(-1.0, 1e-4)
    assert w1 < 0 and w2 < 0
    # the jump diverges exactly at 1$
    assert prompt_jump_factor(0.99) > 90
    try:
        prompt_jump_factor(1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("the prompt jump at 1$ should be refused")
    assert _approx(step_response(0.0, 0.2, 1e-4), 1.0, 1e-6)


# --- xenon ---------------------------------------------------------------

def test_xenon_saturates_and_iodine_does_not():
    """S&F Eqs. (10.50)-(10.51). 135I grows linearly with flux without limit;
    135Xe saturates above phi ~ lambda_X/sigma_a^X = 7.8e12 cm-2 s-1, because
    above that it is burned out as fast as it is made.

    That asymmetry is the entire cause of the post-shutdown xenon peak: a
    high-power reactor sits on a reservoir of iodine far larger than its xenon,
    and after a scram the reservoir decays into xenon with no flux to burn it."""
    sat = LAMBDA_X / (SIGMA_A_XE135_B * 1e-24)
    assert _rel(sat, 7.78e12, 1e-2), "%.3e" % sat
    fluxes = [1e12, 1e13, 1e14, 1e15]
    iod = [iodine_xenon_equilibrium(p)[0] for p in fluxes]
    xen = [iodine_xenon_equilibrium(p)[1] for p in fluxes]
    # iodine is exactly linear
    for a, b in zip(iod, iod[1:]):
        assert _rel(b / a, 10.0, 1e-9)
    # xenon saturates: a hundredfold flux increase buys 1.8x
    assert _rel(xen[-1] / xen[1], 1.76, 0.02)
    # and it approaches its own ceiling, (gamma_I + gamma_X)/sigma_a^X
    ceiling = (GAMMA_I + GAMMA_X) / (SIGMA_A_XE135_B * 1e-24)
    assert _rel(ceiling, 2.370e16, 1e-3), "%.4e" % ceiling
    assert xen[-1] < ceiling and _rel(xen[-1] / ceiling, 0.992, 1e-2)
    # at 1e14 the iodine reservoir is 10x the xenon
    i14, x14 = iodine_xenon_equilibrium(1e14)
    assert _rel(i14 / x14, 9.56, 0.02), "%.2f" % (i14 / x14)
    # equilibrium xenon reactivity in an operating LWR: a few percent
    rho = poison_reactivity(SIGMA_A_XE135_B, x14)
    assert -0.05 < rho < -0.02, "%.4f" % rho
    try:
        iodine_xenon_equilibrium(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative flux should be refused")


def test_the_post_shutdown_xenon_peak_and_the_poison_window():
    """After a scram from 1e14 cm-2 s-1 the xenon reactivity keeps GROWING for
    about 11 hours, peaking at 4.5x its operating value, and does not fall back
    below that value for well over a day.

    That is the poison shutdown time S&F give as 15-25 hours, and it is why an
    operator under production pressure to restart quickly is in a race: the
    time-to-poison here is 2.5 hours with 10% override available, and once past
    it the reactor cannot be restarted at all until the peak has passed."""
    r0 = xenon_reactivity(0.0, 0.0, 1e14)
    curve = [(h, xenon_reactivity(h * 3600.0, 0.0, 1e14)) for h in range(0, 49)]
    peak_h, peak = min(curve, key=lambda p: p[1])
    assert 9 <= peak_h <= 12, "peak at %d h" % peak_h
    assert _rel(peak / r0, 4.53, 0.02), "%.3f" % (peak / r0)
    # monotone up to the peak, monotone down after
    up = [v for h, v in curve if h <= peak_h]
    assert up == sorted(up, reverse=True)
    down = [v for h, v in curve if h >= peak_h]
    assert down == sorted(down)
    # it does not return to the operating level for over a day
    back = [h for h, v in curve if h > peak_h and v > r0]
    assert back and back[0] > 30, "returns at %d h" % (back[0] if back else -1)
    # the time-to-poison
    tp = time_to_poison(1e14, 0.10)
    assert tp is not None and _rel(tp / 3600.0, 2.5, 0.05), "%.2f h" % (tp / 3600)
    # with more override there is more time; with enough, never
    assert time_to_poison(1e14, 0.14) > tp
    assert time_to_poison(1e14, 0.20) is None
    # a low-power reactor does not poison out at all
    assert time_to_poison(1e12, 0.05) is None
    try:
        time_to_poison(1e14, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero available reactivity should be refused")


def test_xenon_transient_is_consistent_with_its_own_equilibrium():
    """Eqs. (10.48)-(10.49) must reproduce Eqs. (10.50)-(10.51) at t = 0 when
    started from equilibrium, and must stay there."""
    for phi in (1e13, 1e14):
        i0, x0 = iodine_xenon_equilibrium(phi)
        for t in (0.0, 3600.0, 1e5):
            i, x = xenon_transient(t, phi, flux_before=phi)
            assert _rel(i, i0, 1e-6) and _rel(x, x0, 1e-6)
    # starting from zero, it climbs to equilibrium -- but slowly: the iodine
    # time constant is 1/lambda_I = 9.6 h, so full equilibrium takes ~2 days
    i0, x0 = iodine_xenon_equilibrium(1e14)
    i, x = xenon_transient(2e5, 1e14, i0=0.0, x0=0.0)
    assert _rel(i, i0, 5e-3) and _rel(x, x0, 5e-3)
    i, x = xenon_transient(5e5, 1e14, i0=0.0, x0=0.0)
    assert _rel(i, i0, 1e-6) and _rel(x, x0, 1e-6)
    # a restart burns the xenon down BELOW equilibrium, because the iodine that
    # would replenish it has already decayed
    _, x_peak = xenon_transient(11 * 3600.0, 0.0, flux_before=1e14)
    _, x_after = xenon_transient(6 * 3600.0, 1e14, i0=0.0, x0=x_peak)
    assert x_after < x0, "%.4e vs %.4e" % (x_after, x0)
    try:
        xenon_transient(1.0, 1e14)
    except ValueError:
        pass
    else:
        raise AssertionError("missing initial conditions should be refused")


# --- samarium ------------------------------------------------------------

def test_samarium_equilibrium_is_independent_of_flux():
    """S&F §10.9.2: S0/Sigma_f = gamma_P/sigma_a^S, with no flux in it. Every
    reactor ends up with the same equilibrium samarium poisoning whatever its
    power, because production and the only loss channel are both proportional to
    the flux.

    And unlike xenon, the post-shutdown buildup is PERMANENT: 149Sm is stable and
    nothing burns it until the reactor restarts. (S&F's closing sentence attributes
    this to 149Pm being stable; 149Pm has a 53 h half-life, and the decay chain
    printed three paragraphs earlier says so.)"""
    s = [promethium_samarium_equilibrium(p)[1] for p in (1e12, 1e13, 1e14, 1e15)]
    for v in s[1:]:
        assert _rel(v, s[0], 1e-12)
    assert _rel(s[0], GAMMA_PM149 / (SIGMA_A_SM149_B * 1e-24), 1e-12)
    # promethium, by contrast, is linear in flux
    p = [promethium_samarium_equilibrium(f)[0] for f in (1e13, 1e14)]
    assert _rel(p[1] / p[0], 10.0, 1e-12)
    # 149Pm is NOT stable -- 53 h
    assert _rel(math.log(2.0) / LAMBDA_PM / 3600.0, 53.0, 1e-9)
    assert LAMBDA_PM > 0
    # after shutdown samarium grows and never falls
    s0 = promethium_samarium_equilibrium(1e14)[1]
    curve = [samarium_transient(h * 3600.0, 0.0, 1e14)[1] for h in (0, 24, 100, 500)]
    assert curve == sorted(curve)
    assert curve[-1] > curve[0]
    assert _rel(curve[-1], s0 + promethium_samarium_equilibrium(1e14)[0], 1e-3)
    # and the buildup is far worse from a high-flux reactor
    hi = samarium_transient(200 * 3600.0, 0.0, 1e14)[1]
    lo = samarium_transient(200 * 3600.0, 0.0, 1e13)[1]
    assert hi > lo
    # samarium's equilibrium poisoning is small beside xenon's
    assert abs(poison_reactivity(SIGMA_A_SM149_B, s0)) < abs(
        poison_reactivity(SIGMA_A_XE135_B, iodine_xenon_equilibrium(1e14)[1]))


# --- feedback ------------------------------------------------------------

def test_a_reactor_is_safe_only_if_its_temperature_coefficient_is_negative():
    """S&F §10.8.2. The dominant negative term is Doppler broadening of 238U's
    resonances -- p falls within milliseconds of the fuel heating -- and it acts
    faster than any control system.

    A positive coefficient is not merely undesirable; it is a positive feedback
    loop, and it is what made RBMK-1000 unstable at low power."""
    alpha = temperature_coefficient(-0.004, 0.0, 900.0, 300.0)
    assert _rel(alpha, -6.667e-6, 1e-3)
    assert is_self_regulating(alpha)
    assert not is_self_regulating(+1e-6)
    assert not is_self_regulating(0.0)
    # a 500 K excursion in a reactor with this coefficient removes half a dollar
    assert _rel(dollars(alpha * 500.0), -0.513, 0.02)
    try:
        temperature_coefficient(0.0, 0.0, 300.0, 300.0)
    except ValueError:
        pass
    else:
        raise AssertionError("equal temperatures should be refused")


def test_poison_reactivity_scales_as_the_book_says():
    """Eq. (10.45): rho_p ~ -0.6 sigma_a^p N_p/Sigma_f, with 0.6 = (eta/nu)f for
    a typical 2.5%-enriched LWR (eta ~ 1.8, nu = 2.43, f ~ 0.8)."""
    assert _rel((1.8 / 2.43) * 0.8, 0.593, 1e-2)
    assert _rel(poison_reactivity(1.0, 1e24), -0.6, 1e-9)
    assert _rel(poison_reactivity(2.0, 1e24), 2 * poison_reactivity(1.0, 1e24), 1e-12)
    assert poison_reactivity(0.0, 1e24) == 0.0
    # 135Xe's cross section is 66x samarium's and 54 000x the 50 b rule of thumb
    assert _rel(SIGMA_A_XE135_B / SIGMA_A_SM149_B, 65.9, 0.02)
    assert _rel(SIGMA_A_XE135_B / 50.0, 54000.0, 0.01)
    try:
        poison_reactivity(-1.0, 1e24)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative cross section should be refused")


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
