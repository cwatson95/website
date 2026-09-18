"""NE-20  Reactor kinetics: point kinetics, delayed neutrons, feedback, xenon.

Nuclear Science & Engineering trunk, module NE-20 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 10.7-10.9 and Addenda 2-3 (§§10.11-10.12), printed pp. 339-365.
Pure stdlib.

~NE-19 asked whether a reactor is critical.  This module asks what happens when
it is not, and the answer rests on one number: for 235U only

    beta = 0.0065

of the fission neutrons are DELAYED, appearing seconds to minutes after the
fission that made their precursor.  Without them a reactor would be
uncontrollable -- a 0.1% increase in k_eff with a 1e-4 s cycle multiplies the
population 20 000-fold in one second [Eq. (10.29)].  With them, the same
insertion gives a 128 s period and a 1.2% rise [Eq. (10.34)].

Everything else follows from that, and so does the danger.  Because delayed
neutrons carry the whole margin, the interesting scale for reactivity is beta
itself, which is why reactivity is measured in DOLLARS: k($) = rho/beta.  Below
1$ the chain needs its delayed neutrons and the reactor is controllable; at 1$ it
is PROMPT CRITICAL, sustained on prompt neutrons alone, and the period collapses
from ~100 s to ~1 ms.  That cliff is the single most important fact in reactor
safety, and the module refuses to apply the small-insertion period formula
across it.

Two further consequences appear here:

  * FEEDBACK.  Temperature changes k_eff, mostly through Doppler broadening of
    238U's resonances (p falls) and moderator expansion (f falls).  A reactor
    whose net temperature coefficient is negative is self-regulating; one whose
    coefficient is positive is not, which is what the module's `is_self_regulating`
    is about.
  * XENON.  135Xe has the largest thermal absorption cross section of any nuclide
    (2.7e6 b) and is a fission product whose parent 135I outlives it. So after a
    shutdown the poison keeps GROWING for ~11 hours, and a reactor that cannot
    override it is locked out for 15-25 hours.
"""

import math

__all__ = [
    "DELAYED_GROUPS", "BETA", "SIGMA_A_XE135_B", "GAMMA_I", "GAMMA_X",
    "LAMBDA_I", "LAMBDA_X", "GAMMA_PM149", "SIGMA_A_SM149_B", "LAMBDA_PM",
    "beta_total", "relative_yields", "decay_constants",
    "mean_precursor_lifetime", "mean_precursor_half_life",
    "reactivity", "keff_from_reactivity", "dollars", "keff_from_dollars",
    "pcm", "prompt_generation_time", "effective_generation_time",
    "simple_period", "small_insertion_period", "prompt_critical_period",
    "inhour", "asymptotic_period", "one_group_omegas", "step_response",
    "prompt_jump_factor", "solve_point_kinetics",
    "poison_reactivity", "iodine_xenon_equilibrium", "xenon_transient",
    "xenon_reactivity", "time_to_poison",
    "promethium_samarium_equilibrium", "samarium_transient",
    "temperature_coefficient", "is_self_regulating",
    "EXAMPLE_10_12_CROSSREF_ERRATA", "SM149_STABILITY_ERRATA",
]

# --- Table 10.9 (printed p. 341): six delayed-neutron groups, Keepin [1965].
# nuclide -> [(half-life s, yield fraction beta_i), ...]
DELAYED_GROUPS = {
    "235U": [(55.7, 0.00021), (22.7, 0.00142), (6.22, 0.00127),
             (2.30, 0.00257), (0.610, 0.00075), (0.230, 0.00027)],
    "233U": [(55.0, 0.00022), (20.6, 0.00078), (5.00, 0.00066),
             (2.13, 0.00072), (0.615, 0.00013), (0.277, 0.00009)],
    "239Pu": [(54.3, 0.00007), (23.0, 0.00063), (5.60, 0.00044),
              (2.13, 0.00068), (0.618, 0.00018), (0.257, 0.00009)],
}
BETA = {"235U": 0.0065, "233U": 0.0026, "239Pu": 0.0021}   # the printed totals

# --- §10.9: fission-product poisons (printed pp. 351-356)
SIGMA_A_XE135_B = 2.7e6         # the largest thermal cross section known
GAMMA_I = 0.061                 # 135I yield from 235U, including 135Te
GAMMA_X = 0.003                 # direct 135Xe yield
LAMBDA_I = 2.9e-5               # s^-1  (135I, 6.7 h)
LAMBDA_X = 2.1e-5               # s^-1  (135Xe, 9.2 h)
GAMMA_PM149 = 0.0113            # 149Pm yield, including 149Nd
SIGMA_A_SM149_B = 41000.0       # 149Sm thermal absorption (S&F do not print it)
LAMBDA_PM = math.log(2.0) / (53.0 * 3600.0)     # 149Pm, 53 h

# --- printed slips kept for the tests (see refs.md)
EXAMPLE_10_12_CROSSREF_ERRATA = "Example 10.7"   # should be Example 10.11
SM149_STABILITY_ERRATA = "149Pm is stable"       # 149Pm has a 53 h half-life


# --- delayed-neutron bookkeeping  [S&F Table 10.9] -----------------------

def _groups(nuclide):
    if nuclide not in DELAYED_GROUPS:
        raise KeyError("no Table 10.9 data for %r; have %s"
                       % (nuclide, sorted(DELAYED_GROUPS)))
    return DELAYED_GROUPS[nuclide]


def beta_total(nuclide="235U"):
    """Total delayed-neutron fraction, summed over the six groups."""
    return sum(b for _, b in _groups(nuclide))


def relative_yields(nuclide="235U"):
    """a_i = beta_i/beta, which sum to 1  [S&F Eq. (10.87)]."""
    b = beta_total(nuclide)
    return [bi / b for _, bi in _groups(nuclide)]


def decay_constants(nuclide="235U"):
    """lambda_i = ln2/T_i for each precursor group."""
    return [math.log(2.0) / t for t, _ in _groups(nuclide)]


def mean_precursor_lifetime(nuclide="235U"):
    """tau = sum a_i/lambda_i  [S&F §10.7.4], about 12.9 s for 235U.

    S&F quote 12.8 s from an average half-life of 8.8 s; the six groups of
    Table 10.9 give 12.95 s and 8.98 s.  This is the quantity that sets the
    period for small reactivity insertions, and the reason it is SECONDS rather
    than the 1e-4 s of a prompt cycle is the whole of reactor control."""
    return sum(a / lam for a, lam in zip(relative_yields(nuclide),
                                         decay_constants(nuclide)))


def mean_precursor_half_life(nuclide="235U"):
    """The half-life corresponding to `mean_precursor_lifetime`."""
    return mean_precursor_lifetime(nuclide) * math.log(2.0)


# --- reactivity units  [S&F §10.7.3, Eq. (10.30)] ------------------------

def reactivity(keff):
    """rho = (k-1)/k  [S&F Eq. (10.30)]."""
    if keff <= 0:
        raise ValueError("k_eff must be positive")
    return (keff - 1.0) / keff


def keff_from_reactivity(rho):
    """The inverse of `reactivity`."""
    if rho >= 1.0:
        raise ValueError("rho >= 1 corresponds to infinite k_eff")
    return 1.0 / (1.0 - rho)


def dollars(rho, nuclide="235U", beta=None):
    """k($) = rho/beta  [S&F §10.7.3].

    Dollars are the only reactivity unit that shows the prompt-critical cliff
    directly: 1$ is exactly the point at which the prompt neutrons alone sustain
    the chain."""
    b = BETA[nuclide] if beta is None else beta
    return rho / b


def keff_from_dollars(k_dollars, nuclide="235U", beta=None):
    """k_eff for a given reactivity in dollars  [S&F Example 10.11]:

        k_eff = 1/(1 - beta k($)) .
    """
    b = BETA[nuclide] if beta is None else beta
    if b * k_dollars >= 1.0:
        raise ValueError("beta k($) >= 1 is unphysical")
    return 1.0 / (1.0 - b * k_dollars)


def pcm(rho):
    """Reactivity in pcm, 1 pcm = 1e-5 delta-k/k  [S&F §10.7.3]."""
    return rho * 1e5


# --- generation times: two different quantities, one symbol --------------

def prompt_generation_time(l0, keff=1.0):
    """l = l0/k_eff  [S&F Eq. (10.83)] -- the PROMPT neutron generation time,
    of order 1e-4 s in a thermal reactor.

    This is the l of the point kinetics equations (10.84)-(10.87) and of the
    inhour equation (10.39)."""
    if l0 <= 0 or keff <= 0:
        raise ValueError("lifetime and k_eff must be positive")
    return l0 / keff


def effective_generation_time(l0, nuclide="235U", beta=None):
    """l = l0 + beta*tau  [S&F Eq. (10.31)] -- the EFFECTIVE generation time
    averaged over prompt and delayed neutrons, about 0.084 s for 235U.

    NOTE THE COLLISION.  S&F write both this and `prompt_generation_time` as
    "l", and the two differ by a factor of ~800.  Eq. (10.42) is only correct
    with THIS one; Eqs. (10.39) and (10.84)-(10.87), which surround it, use the
    other.  The module gives them different names on purpose."""
    b = BETA[nuclide] if beta is None else beta
    return l0 + b * mean_precursor_lifetime(nuclide)


# --- periods  [S&F Eqs. (10.33), (10.36), (10.42)] -----------------------

def simple_period(delta_k, l0):
    """T = l0/delta_k  [S&F Eq. (10.28)] -- the PROMPT-ONLY model, kept only to
    show how wrong it is.

    For delta_k = 0.001 and l0 = 1e-4 s it gives a 0.1 s period, i.e. e^10 in one
    second.  Reactors are controllable only because this model is false."""
    if delta_k == 0:
        raise ValueError("a critical reactor has an infinite period")
    if l0 <= 0:
        raise ValueError("the prompt lifetime must be positive")
    return l0 / delta_k


def small_insertion_period(k_dollars, nuclide="235U", max_dollars=0.3):
    """Asymptotic period for a small insertion  [S&F Eqs. (10.33), (10.42)]:

        T = tau/k($) ,

    i.e. the mean precursor lifetime divided by the reactivity in dollars.
    Equivalently beta*tau/delta_k, which is how S&F write Eq. (10.33).

    REFUSES beyond `max_dollars`.  The approximation assumes |rho| << beta, and
    it fails catastrophically rather than gracefully: at 1$ the true period
    collapses by three orders of magnitude to the prompt-critical branch, and
    this formula would still be reporting a leisurely 13 s."""
    if k_dollars == 0:
        raise ValueError("zero reactivity gives an infinite period")
    if abs(k_dollars) > max_dollars:
        raise ValueError(
            "|k($)| = %.3f exceeds %.2f$: Eq. (10.33) assumes |rho| << beta and "
            "breaks down before prompt critical, where the period collapses "
            "from ~100 s to ~1 ms. Use asymptotic_period()."
            % (abs(k_dollars), max_dollars))
    return mean_precursor_lifetime(nuclide) / k_dollars


def prompt_critical_period(k_dollars, l0, nuclide="235U", beta=None):
    """T = (l0/beta)/(k($) - 1)  [S&F Eq. (10.36)], valid for k($) >> 1.

    Now the period is proportional to the PROMPT lifetime, which is why it is
    milliseconds. This is the branch that destroyed SL-1 and Chernobyl-4."""
    b = BETA[nuclide] if beta is None else beta
    if k_dollars <= 1.0:
        raise ValueError("Eq. (10.36) applies only above prompt critical "
                         "(k($) > 1); below it the delayed neutrons dominate")
    return (l0 / b) / (k_dollars - 1.0)


# --- the inhour equation  [S&F Eq. (10.39)] ------------------------------

def inhour(omega, l0, nuclide="235U", keff=1.0):
    """The inhour function: omega[l/beta + sum a_i/(lambda_i + omega)], whose
    value is the reactivity in dollars  [S&F Eq. (10.39)].

    Solving it for omega given k($) gives the exact asymptotic period, with no
    small-reactivity assumption."""
    lam = decay_constants(nuclide)
    a = relative_yields(nuclide)
    b = beta_total(nuclide)
    l = prompt_generation_time(l0, keff)
    s = sum(ai / (li + omega) for ai, li in zip(a, lam))
    return omega * (l / b + s)


def asymptotic_period(k_dollars, l0, nuclide="235U", tol=1e-14):
    """The exact asymptotic period T = 1/omega_0 from the inhour equation.

    omega_0 is the largest root, positive for k($) > 0 and negative below.  For
    negative insertions it is bounded below by the longest-lived precursor: no
    matter how much negative reactivity is inserted, the power cannot fall faster
    than -80 s per e-fold, which is why decay-heat removal is not optional."""
    if k_dollars == 0:
        raise ValueError("zero reactivity gives an infinite period")
    lam = sorted(decay_constants(nuclide))
    if k_dollars > 0:
        lo, hi = 1e-12, 1.0
        while inhour(hi, l0, nuclide) < k_dollars:
            hi *= 2.0
            if hi > 1e12:
                raise ValueError("no root found")
    else:
        # omega_0 lies in (-lambda_min, 0)
        lo, hi = -lam[0] * (1 - 1e-12), -1e-12
    while hi - lo > tol * max(1.0, abs(hi)):
        mid = 0.5 * (lo + hi)
        if inhour(mid, l0, nuclide) < k_dollars:
            lo = mid
        else:
            hi = mid
    return 1.0 / (0.5 * (lo + hi))


def one_group_omegas(k_dollars, l0, nuclide="235U", beta=None):
    """The two roots of the one-group inhour equation  [S&F Eq. (10.96)].

    Returns (omega_1, omega_2) with omega_1 > omega_2.  omega_2 is the fast,
    always-negative prompt root that produces the PROMPT JUMP; omega_1 is the
    slow asymptotic one."""
    b = BETA[nuclide] if beta is None else beta
    lam = math.log(2.0) / (mean_precursor_half_life(nuclide))
    l = l0
    c = lam + (b / l) * (1.0 - k_dollars)
    disc = c * c + 4.0 * k_dollars * lam * b / l
    if disc < 0:
        raise ValueError("complex roots: the one-group model has failed")
    r = math.sqrt(disc)
    return 0.5 * (-c + r), 0.5 * (-c - r)


def step_response(t, k_dollars, l0, n0=1.0, nuclide="235U", beta=None):
    """n(t) after a step insertion, one-group  [S&F Eq. (10.105)].

    The shape is a fast PROMPT JUMP followed by an exponential.  For a positive
    insertion the jump is upward by 1/(1-k($)); for a negative one it is a prompt
    DROP by the same factor."""
    if t < 0:
        raise ValueError("t must be non-negative")
    b = BETA[nuclide] if beta is None else beta
    w1, w2 = one_group_omegas(k_dollars, l0, nuclide, b)
    a1 = (b * k_dollars / l0 - w2) / (w1 - w2)
    a2 = (w1 - b * k_dollars / l0) / (w1 - w2)
    return n0 * (a1 * math.exp(w1 * t) + a2 * math.exp(w2 * t))


def prompt_jump_factor(k_dollars):
    """The prompt jump: n jumps by 1/(1 - k($)) before the slow branch takes over
    [S&F Eq. (10.108)].

    Reads as an instantaneous multiplication because it happens on the prompt
    time scale, ~l0/beta = 0.06 s.  It diverges at exactly 1$, which is the
    mathematical signature of prompt criticality."""
    if k_dollars >= 1.0:
        raise ValueError("the prompt jump diverges at 1$: above prompt critical "
                         "there is no jump-then-drift, only a prompt excursion")
    return 1.0 / (1.0 - k_dollars)


def solve_point_kinetics(rho_of_t, l0, t_end, dt=1e-3, n0=1.0,
                         nuclide="235U", source=0.0):
    """Integrate the G-group point kinetics equations  [S&F Eqs. (10.86)] by RK4.

        dn/dt   = (rho - beta)/l * n + sum lambda_i C_i + S
        dC_i/dt = beta_i/l * n - lambda_i C_i

    `rho_of_t` is a callable.  Returns [(t, n), ...].  Started from the exact
    equilibrium C_i = beta_i n0/(l lambda_i), so a zero insertion is a flat line
    -- which is the first thing the test checks."""
    lam = decay_constants(nuclide)
    betas = [b for _, b in _groups(nuclide)]
    b = beta_total(nuclide)
    c = [bi * n0 / (l0 * li) for bi, li in zip(betas, lam)]
    y = [n0] + c

    def deriv(t, y):
        n = y[0]
        rho = rho_of_t(t)
        dn = (rho - b) / l0 * n + sum(li * ci for li, ci in zip(lam, y[1:])) + source
        return [dn] + [bi / l0 * n - li * ci
                       for bi, li, ci in zip(betas, lam, y[1:])]

    out = [(0.0, n0)]
    t = 0.0
    n_steps = int(round(t_end / dt))
    for _ in range(n_steps):
        k1 = deriv(t, y)
        k2 = deriv(t + dt / 2, [yi + dt / 2 * ki for yi, ki in zip(y, k1)])
        k3 = deriv(t + dt / 2, [yi + dt / 2 * ki for yi, ki in zip(y, k2)])
        k4 = deriv(t + dt, [yi + dt * ki for yi, ki in zip(y, k3)])
        y = [yi + dt / 6 * (a + 2 * bb + 2 * cc + d)
             for yi, a, bb, cc, d in zip(y, k1, k2, k3, k4)]
        t += dt
        out.append((t, y[0]))
    return out


# --- fission-product poisons  [S&F §10.9] --------------------------------

def poison_reactivity(sigma_a_barns, n_over_sigma_f, ratio=0.6):
    """rho_p = -(Sigma_f/Sigma_a) sigma_a^p N_p/Sigma_f  [S&F Eqs. (10.44)-(10.45)].

    S&F evaluate Sigma_f/Sigma_a ~ 0.6 for a typical LWR (eta ~ 1.8, nu = 2.43,
    f ~ 0.8, so (eta/nu)f = 0.59).  `n_over_sigma_f` is N_p/Sigma_f in cm^2 --
    exactly what the xenon and samarium solutions return."""
    if sigma_a_barns < 0:
        raise ValueError("cross section must be non-negative")
    return -ratio * sigma_a_barns * 1e-24 * n_over_sigma_f


def iodine_xenon_equilibrium(flux):
    """Equilibrium (I/Sigma_f, X/Sigma_f) in cm^2  [S&F Eqs. (10.50)-(10.51)]:

        I0/Sigma_f = gamma_I phi / lambda_I
        X0/Sigma_f = (gamma_I + gamma_X) phi / (lambda_X + sigma_a^X phi)

    The asymmetry is the whole of xenon dynamics.  135I grows LINEARLY with flux
    for ever; 135Xe SATURATES, because above phi ~ lambda_X/sigma_a^X = 8e8 the
    xenon is burned out as fast as it appears.  So a high-power reactor sits on a
    large reservoir of 135I that is not yet xenon -- and after a scram that
    reservoir decays into xenon with nothing burning it."""
    if flux < 0:
        raise ValueError("flux must be non-negative")
    i = GAMMA_I * flux / LAMBDA_I
    x = ((GAMMA_I + GAMMA_X) * flux
         / (LAMBDA_X + SIGMA_A_XE135_B * 1e-24 * flux))
    return i, x


def xenon_transient(t, flux, i0=None, x0=None, flux_before=None):
    """(I/Sigma_f, X/Sigma_f) at time t  [S&F Eqs. (10.48)-(10.49)].

    `flux_before` sets the initial condition to the equilibrium at that flux,
    which is the shutdown case (flux=0) and the restart case."""
    if t < 0 or flux < 0:
        raise ValueError("t and flux must be non-negative")
    if flux_before is not None:
        i0, x0 = iodine_xenon_equilibrium(flux_before)
    if i0 is None or x0 is None:
        raise ValueError("initial conditions or flux_before must be given")
    lx = LAMBDA_X + SIGMA_A_XE135_B * 1e-24 * flux
    i = i0 * math.exp(-LAMBDA_I * t) + (GAMMA_I * flux / LAMBDA_I) * (
        1 - math.exp(-LAMBDA_I * t))
    x = (x0 * math.exp(-lx * t)
         + ((GAMMA_I + GAMMA_X) * flux / lx) * (1 - math.exp(-lx * t)))
    denom = LAMBDA_X - LAMBDA_I + SIGMA_A_XE135_B * 1e-24 * flux
    if abs(denom) > 1e-30:
        x += ((LAMBDA_I * i0 - GAMMA_I * flux) / denom
              * (math.exp(-LAMBDA_I * t) - math.exp(-lx * t)))
    return i, x


def xenon_reactivity(t, flux, flux_before, ratio=0.6):
    """Negative reactivity from 135Xe at time t after a flux change."""
    _, x = xenon_transient(t, flux, flux_before=flux_before)
    return poison_reactivity(SIGMA_A_XE135_B, x, ratio)


def time_to_poison(flux_before, available_reactivity, ratio=0.6,
                   t_max=200000.0, dt=10.0):
    """Time after shutdown at which the xenon reactivity exceeds the control
    system's available positive reactivity  [S&F §10.9.1].

    Returns None if the reactor never poisons out.  S&F: the interval during
    which restart is impossible -- the poison shutdown time -- is typically
    15-25 hours, and the time-to-poison is often only tens of minutes."""
    if available_reactivity <= 0:
        raise ValueError("available reactivity must be positive")
    t = 0.0
    while t <= t_max:
        if abs(xenon_reactivity(t, 0.0, flux_before, ratio)) > available_reactivity:
            return t
        t += dt
    return None


def promethium_samarium_equilibrium(flux, sigma_a_sm=SIGMA_A_SM149_B):
    """Equilibrium (P/Sigma_f, S/Sigma_f)  [S&F Eqs. (10.52)-(10.53)].

    S0/Sigma_f = gamma_P/sigma_a^S -- INDEPENDENT OF FLUX.  Every reactor
    therefore ends up with the same equilibrium samarium poisoning, whatever its
    power.  That is a genuinely surprising result and it follows in one line:
    production is proportional to flux and the only loss is burnup, also
    proportional to flux."""
    if flux < 0:
        raise ValueError("flux must be non-negative")
    p = GAMMA_PM149 * flux / LAMBDA_PM
    s = GAMMA_PM149 / (sigma_a_sm * 1e-24)
    return p, s


def samarium_transient(t, flux, flux_before, sigma_a_sm=SIGMA_A_SM149_B):
    """(P/Sigma_f, S/Sigma_f) at time t  [S&F Eqs. (10.54)-(10.55)].

    Unlike xenon, the post-shutdown samarium buildup is PERMANENT: 149Sm is
    stable and there is no flux to burn it, so it stays until the reactor
    restarts.  (S&F's closing sentence of §10.9.2 says this happens "since 149Pm
    is stable" -- 149Pm has a 53 h half-life; it is 149Sm that is stable.)"""
    if t < 0 or flux < 0:
        raise ValueError("t and flux must be non-negative")
    p0, s0 = promethium_samarium_equilibrium(flux_before, sigma_a_sm)
    burn = sigma_a_sm * 1e-24 * flux
    p = p0 * math.exp(-LAMBDA_PM * t) + (GAMMA_PM149 * flux / LAMBDA_PM) * (
        1 - math.exp(-LAMBDA_PM * t))
    if burn > 0:
        s = s0 * math.exp(-burn * t) + (GAMMA_PM149 * flux / burn) * (
            1 - math.exp(-burn * t))
        denom = burn - LAMBDA_PM
        if abs(denom) > 1e-30:
            s += ((LAMBDA_PM * p0 - GAMMA_PM149 * flux) / denom
                  * (math.exp(-LAMBDA_PM * t) - math.exp(-burn * t)))
    else:
        # shutdown: samarium only accumulates, from the decaying promethium
        s = s0 + p0 * (1 - math.exp(-LAMBDA_PM * t))
    return p, s


# --- temperature feedback  [S&F §10.8] -----------------------------------

def temperature_coefficient(rho_hot, rho_cold, t_hot, t_cold):
    """alpha_T = d(rho)/dT, in reactivity per kelvin  [S&F §10.8.2]."""
    if t_hot == t_cold:
        raise ValueError("the two temperatures must differ")
    return (rho_hot - rho_cold) / (t_hot - t_cold)


def is_self_regulating(alpha_t):
    """A reactor is self-regulating only if its net temperature coefficient is
    negative  [S&F §10.8.2].

    The dominant negative term is the Doppler broadening of 238U's resonances
    (p falls as the fuel heats, within milliseconds); the dominant positive risk
    is a positive void coefficient, which is what made RBMK-1000 unstable at low
    power.  Note the sign convention: alpha_T < 0 means heating removes
    reactivity."""
    return alpha_t < 0


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-20  reactor kinetics\n")

    print("  why delayed neutrons matter  [Eqs. (10.29), (10.34)]")
    print("   prompt-only model, dk = 0.001, l0 = 1e-4 s:")
    print("     period %.4f s -> after 1 s, n/n0 = %.0f"
          % (simple_period(0.001, 1e-4), math.exp(1 / simple_period(0.001, 1e-4))))
    print("   with delayed neutrons (tau = %.2f s):" % mean_precursor_lifetime())
    t = 0.0065 * mean_precursor_lifetime() / 0.001
    print("     period %.1f s -> after 1 s, n/n0 = %.4f" % (t, math.exp(1 / t)))

    print("\n  Table 10.9: the delayed fraction shrinks as plutonium builds in")
    for nuc in ("235U", "233U", "239Pu"):
        print("   %-6s beta = %.5f (printed %.4f), tau = %.2f s, mean T1/2 = %.2f s"
              % (nuc, beta_total(nuc), BETA[nuc], mean_precursor_lifetime(nuc),
                 mean_precursor_half_life(nuc)))

    print("\n  Examples 10.11-10.12: a 0.1$ insertion")
    k = keff_from_dollars(0.1)
    print("   k_eff = %.5f   (book 1.00065),  delta-k = %.5f" % (k, k - 1))
    print("   period = %.1f s   (book 128 s)" % small_insertion_period(0.1))
    print("   exact inhour period = %.1f s" % asymptotic_period(0.1, 1e-4))
    print("   10 W -> 10 kW takes %.0f s = %.1f min"
          % (small_insertion_period(0.1) * math.log(1000),
             small_insertion_period(0.1) * math.log(1000) / 60))

    print("\n  the prompt-critical cliff")
    print("   k($)     asymptotic period      prompt jump")
    for kd in (0.05, 0.1, 0.25, 0.5, 0.9, 0.99, 1.5, 2.0):
        try:
            pj = "%8.2f" % prompt_jump_factor(kd)
        except ValueError:
            pj = "  diverged"
        print("   %5.2f %18.4f s %s" % (kd, asymptotic_period(kd, 1e-4), pj))
    print("   -> the period falls %.0fx between 0.9$ and 1.5$"
          % (asymptotic_period(0.9, 1e-4) / asymptotic_period(1.5, 1e-4)))
    try:
        small_insertion_period(1.5)
    except ValueError as exc:
        print("   small_insertion_period(1.5$) refused: %s..." % str(exc)[:58])

    print("\n  shutdown: the -80 s floor")
    for kd in (-1.0, -5.0, -20.0, -100.0):
        print("   %7.1f$ inserted -> asymptotic period %.1f s"
              % (kd, asymptotic_period(kd, 1e-4)))
    print("   the longest-lived precursor (T1/2 = 55.7 s) sets the floor: %.1f s"
          % (-55.7 / math.log(2.0)))

    print("\n  xenon  [Eqs. (10.50)-(10.51)]")
    print("   flux (/cm2/s)   I/Sigma_f      X/Sigma_f     rho_Xe")
    for phi in (1e12, 1e13, 1e14, 1e15):
        i, x = iodine_xenon_equilibrium(phi)
        print("   %-14.0e %12.4e %12.4e %10.4f"
              % (phi, i, x, poison_reactivity(SIGMA_A_XE135_B, x)))
    print("   -> 135Xe saturates above phi ~ %.2e; 135I never does"
          % (LAMBDA_X / (SIGMA_A_XE135_B * 1e-24)))

    print("\n  after a scram from 1e14 /cm2/s, xenon keeps growing:")
    for hours in (0, 2, 4, 8, 11, 15, 24, 48):
        r = xenon_reactivity(hours * 3600.0, 0.0, 1e14)
        print("   %5.1f h   rho_Xe = %8.4f  (%.2fx equilibrium)"
              % (hours, r, r / xenon_reactivity(0.0, 0.0, 1e14)))
    tp = time_to_poison(1e14, 0.10)
    print("   with 0.10 of override available, time-to-poison = %.0f s = %.1f h"
          % (tp, tp / 3600))

    print("\n  samarium: equilibrium is the same at every power  [Eq. (10.53)]")
    for phi in (1e13, 1e14, 1e15):
        _, s = promethium_samarium_equilibrium(phi)
        print("   phi = %-8.0e  S/Sigma_f = %.4e  rho_Sm = %.5f"
              % (phi, s, poison_reactivity(SIGMA_A_SM149_B, s)))


if __name__ == "__main__":
    _demo()
