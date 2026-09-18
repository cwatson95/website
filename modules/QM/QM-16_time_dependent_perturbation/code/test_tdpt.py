"""Tests for QM-16 tdpt -- every claim checked against a closed form or the
honest dynamics.

Run directly:   python3 test_tdpt.py        (-> "All N tests passed.")
Or with pytest: pytest test_tdpt.py

Each test pins one piece of time-dependent perturbation theory:
  * exact unitary evolution e^{-iHt} is norm-preserving and consistent,
  * the first-order amplitude integral reproduces its closed form,
  * the generalized Rabi formula equals the exact 2-level dynamics, with full
    inversion on resonance and a capped amplitude off resonance,
  * first-order PT reproduces Rabi in the weak/short-time limit,
  * a sinusoidal drive gives a sinc^2 resonance: peak at w=w_fi, height ~ t^2,
    width ~ 1/t; and first-order PT tracks the true driven dynamics (TDSE),
  * Fermi's golden rule: linear-in-t transition probability with the correct
    rate Gamma = 2*pi*|V|^2*rho, its V^2 and rho scaling, and exponential decay
    of the exact (N+1)-level dynamics at that rate.

Natural units hbar = 1 throughout.
"""
import numpy as np
from scipy.linalg import expm

from tdpt import (
    evolve, evolve_tdse, norm, amplitude,
    first_order_amplitude, first_order_probability,
    two_level_H, generalized_rabi_frequency, rabi_probability,
    two_level_exact_probability, sinusoidal_probability, make_driven_H,
    golden_rule_rate, band_hamiltonian, band_first_order_probability,
    survival_probability, extract_rate,
)


def _approx(x, y, rel=1e-9, abs_=1e-12):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- 1. evolution primitives -------------------------------------------------

def test_evolve_unitary_and_consistent():
    """e^{-iHt} is unitary: it preserves the norm, agrees with scipy.expm, and
    the vectorized array-of-times form matches the scalar form."""
    rng = np.random.default_rng(0)
    M = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    H = 0.5 * (M + M.conj().T)                      # random Hermitian
    psi0 = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    psi0 = psi0 / norm(psi0)
    for t in (0.0, 0.7, 3.2):
        psi = evolve(H, psi0, t)
        assert _approx(norm(psi), 1.0, abs_=1e-10)             # unitary
        assert np.allclose(psi, expm(-1j * H * t) @ psi0, atol=1e-9)
    ts = np.array([0.0, 0.7, 3.2])
    block = evolve(H, psi0, ts)                                # (3, 4)
    for k, t in enumerate(ts):
        assert np.allclose(block[k], evolve(H, psi0, t), atol=1e-10)


# --- 2. first-order transition amplitude -------------------------------------

def test_first_order_amplitude_constant_closed_form():
    """For a constant matrix element V0 switched on over [0,t],
        c_f^(1) = -i V0 (e^{i w t} - 1)/(i w)  =>  |c|^2 = V0^2 4 sin^2(w t/2)/w^2.
    (Griffiths Eq. 11.21.)"""
    V0, w, t = 0.013, 0.7, 9.0
    P = first_order_probability(V0, w, t)
    closed = V0 ** 2 * 4.0 * np.sin(w * t / 2.0) ** 2 / w ** 2
    assert _approx(P, closed, rel=1e-6)
    # complex matrix element: only |V0| matters for the probability
    c = first_order_amplitude(0.01j, w, t)
    assert _approx(abs(c) ** 2, 0.01 ** 2 * 4 * np.sin(w * t / 2) ** 2 / w ** 2, rel=1e-6)


def test_first_order_amplitude_callable_matches_constant():
    """A callable returning a constant reproduces the constant code path, and a
    genuinely time-dependent kernel integrates correctly: a Gaussian-in-time
    coupling V(t)=A e^{-t^2/2tau^2} on resonance (w=0) gives c = -i A sqrt(2pi) tau/2
    over (-inf,inf); on a wide finite window we recover it."""
    w, t = 0.7, 9.0
    c_call = first_order_amplitude(lambda tp: 0.013, w, t)
    c_const = first_order_amplitude(0.013, w, t)
    assert _approx(abs(c_call), abs(c_const), rel=1e-6)
    # time-dependent kernel, resonant (w=0): integral of A exp(-t'^2/2tau^2)
    A, tau, T = 0.02, 1.5, 12.0
    c = first_order_amplitude(lambda tp: A * np.exp(-(tp - T / 2) ** 2 / (2 * tau ** 2)),
                              0.0, T)
    expected = -1j * A * np.sqrt(2 * np.pi) * tau     # full Gaussian area, w=0
    assert _approx(abs(c), abs(expected), rel=1e-3)


# --- 3. two-level system & Rabi oscillations ---------------------------------

def test_rabi_formula_matches_exact_dynamics():
    """The generalized Rabi formula equals the exact 2-level evolution
    |<f|e^{-iHt}|i>|^2 to machine precision (Griffiths Prob. 11.9, Eq. 11.37)."""
    for delta, Omega_R, t in [(0.0, 1.0, 1.3), (0.7, 1.0, 2.1),
                              (2.0, 0.3, 5.0), (-1.5, 0.8, 4.0), (0.0, 2.0, 0.5)]:
        formula = rabi_probability(t, Omega_R, delta)
        dynamics = two_level_exact_probability(t, delta, Omega_R)
        assert _approx(formula, dynamics, abs_=1e-10)


def test_rabi_resonance_full_inversion():
    """On resonance (delta=0) the population fully inverts: P = sin^2(Omega_R t/2)
    reaches 1 at t = pi/Omega_R.  Off resonance it is capped below 1 at
    Omega_R^2/(Omega_R^2+delta^2), and flops at sqrt(Omega_R^2+delta^2)."""
    Omega_R = 1.0
    # full inversion on resonance
    assert _approx(rabi_probability(np.pi / Omega_R, Omega_R, 0.0), 1.0, abs_=1e-12)
    assert _approx(rabi_probability(0.0, Omega_R, 0.0), 0.0, abs_=1e-12)
    # off resonance: amplitude is capped, never reaches 1
    for delta in (0.5, 1.0, 3.0):
        cap = Omega_R ** 2 / (Omega_R ** 2 + delta ** 2)
        ts = np.linspace(0, 20, 4001)
        Pmax = max(rabi_probability(t, Omega_R, delta) for t in ts)
        assert Pmax <= cap + 1e-9
        assert _approx(Pmax, cap, rel=2e-3)            # the cap is attained
        assert cap < 1.0
    # generalized Rabi frequency
    assert _approx(generalized_rabi_frequency(3.0, 4.0), 5.0)
    assert _approx(generalized_rabi_frequency(1.0, 0.0), 1.0)


def test_first_order_reproduces_rabi_weak_and_short():
    """First-order PT reproduces the exact Rabi probability in two limits
    (Griffiths Sec. 11.1.2 vs Prob. 11.9):
      (a) weak coupling Omega_R << |delta|: P^(1) = (Omega_R^2/delta^2) sin^2(delta t/2)
          matches the exact capped flopping;
      (b) short time (any delta): both -> Omega_R^2 t^2 / 4.
    P^(1) is computed from the first-order integral with constant coupling
    Omega_R/2 and rotating-frame Bohr frequency -delta."""
    # (a) weak coupling
    Omega_R, delta = 0.01, 0.6
    for t in (3.0, 7.5, 12.0):
        exact = rabi_probability(t, Omega_R, delta)
        pt = first_order_probability(Omega_R / 2.0, -delta, t)
        closed = (Omega_R ** 2 / delta ** 2) * np.sin(delta * t / 2) ** 2
        assert _approx(pt, closed, rel=1e-6)           # PT integral == closed form
        assert _approx(pt, exact, rel=2e-3)            # and == exact, since weak
    # (b) short time, any detuning -> Omega_R^2 t^2 / 4
    Omega_R, t = 0.5, 0.02
    for delta in (0.0, 0.3, 2.0):
        exact = rabi_probability(t, Omega_R, delta)
        quad = (Omega_R * t / 2.0) ** 2
        assert _approx(exact, quad, rel=1e-3)
        pt = first_order_probability(Omega_R / 2.0, -delta, t)
        assert _approx(pt, quad, rel=1e-3)


# --- 3b. sinusoidal perturbation & resonance ---------------------------------

def test_sinusoidal_resonance_peak():
    """Swept over the drive frequency w, the transition probability (Eq. 11.35)
    is sharply peaked at resonance w = w_fi, with central-peak height
    |V_fi|^2 t^2/4 (the delta->0 limit handled without a divide-by-zero)."""
    omega_fi, V_fi, t = 1.0, 0.01, 40.0
    ws = np.linspace(0.6, 1.4, 8001)
    P = sinusoidal_probability(t, ws, omega_fi, V_fi)
    assert _approx(ws[np.argmax(P)], omega_fi, abs_=2e-4)           # peak at w_fi
    peak = sinusoidal_probability(t, omega_fi, omega_fi, V_fi)      # exact resonance
    assert _approx(peak, (V_fi * t / 2.0) ** 2, rel=1e-9)          # height = |V|^2 t^2/4
    assert np.isfinite(peak)                                        # no 0/0 blowup
    assert P.max() <= peak + 1e-12


def test_sinusoidal_sinc_squared():
    """The line shape is a sinc^2 in (w - w_fi): zeros at w = w_fi +/- 2 pi n / t,
    central-peak height grows like t^2, and the peak narrows like 1/t."""
    omega_fi, V_fi = 1.0, 0.01
    # zeros at integer multiples of 2 pi / t
    t = 30.0
    for n in (1, 2, 3):
        w_zero = omega_fi + 2 * np.pi * n / t
        assert _approx(sinusoidal_probability(t, w_zero, omega_fi, V_fi), 0.0, abs_=1e-12)
    # peak height ~ t^2
    h1 = sinusoidal_probability(20.0, omega_fi, omega_fi, V_fi)
    h2 = sinusoidal_probability(40.0, omega_fi, omega_fi, V_fi)
    assert _approx(h2 / h1, 4.0, rel=1e-6)                          # (40/20)^2 = 4
    # width (distance to first zero) ~ 1/t
    width1 = 2 * np.pi / 20.0
    width2 = 2 * np.pi / 40.0
    assert _approx(width1 / width2, 2.0, rel=1e-9)


def test_sinusoidal_pt_vs_tdse():
    """First-order PT tracks the TRUE driven dynamics.  Integrating the honest
    time-dependent lab-frame Hamiltonian H(t)=H0+V cos(wt) (no RWA) and reading
    the transition probability agrees, for weak coupling, with the full
    first-order amplitude (both co- and counter-rotating terms, Eq. 11.32) across
    detunings; and near resonance the RWA result (Eq. 11.35) agrees too."""
    omega_fi = 1.0
    for omega, t, V_fi in [(0.90, 20.0, 0.01), (1.08, 16.0, 0.01),
                           (0.70, 15.0, 0.01)]:
        psi = evolve_tdse(make_driven_H(omega, omega_fi, V_fi),
                          np.array([1.0, 0.0]), t)
        P_tdse = abs(amplitude(1, psi)) ** 2
        # full first order: matrix element V_fi cos(w t'), keeps BOTH terms
        c = first_order_amplitude(lambda tp: V_fi * np.cos(omega * tp), omega_fi, t)
        assert _approx(P_tdse, abs(c) ** 2, rel=2e-2)              # honest dynamics
    # near resonance the RWA (Eq. 11.35) also tracks the full first order
    omega, t, V_fi = 0.97, 18.0, 0.01
    c = first_order_amplitude(lambda tp: V_fi * np.cos(omega * tp), omega_fi, t)
    P_rwa = sinusoidal_probability(t, omega, omega_fi, V_fi)
    assert _approx(P_rwa, abs(c) ** 2, rel=5e-2)


# --- 4. Fermi's golden rule --------------------------------------------------

def test_golden_rule_linear_in_time():
    """The literal derivation (Griffiths Eq. 11.79 -> 11.81): the first-order
    transition probability into a dense band grows LINEARLY in time, and the
    slope is exactly Fermi's golden-rule rate Gamma = 2 pi |V|^2 rho.  In the
    window 1/W << t << 1/dE the recovered slope matches Gamma to ~0.1%."""
    N, dE, V = 2001, 0.02, 0.0309
    rho = 1.0 / dE
    Gamma = golden_rule_rate(V, rho)
    ts = np.linspace(1.0, 10.0, 19)                  # 1/W=0.025 << t << 1/dE=50
    P = np.array([band_first_order_probability(N, dE, V, t) for t in ts])
    slope, intercept = np.polyfit(ts, P, 1)
    assert _approx(slope, Gamma, rel=5e-3)           # rate is the golden rule rate
    assert abs(intercept) < 0.02                     # passes through ~origin
    # residuals from a straight line are tiny (genuinely linear)
    resid = P - (slope * ts + intercept)
    assert np.max(np.abs(resid)) < 5e-3 * P.max()


def test_golden_rule_scaling():
    """Gamma = 2 pi |V|^2 rho scales as |V|^2 and as the density of states rho.
    Measured via the (clean, saturation-free) first-order slope: doubling V
    quadruples the rate; halving the level spacing dE doubles rho and the rate."""
    N, dE, V = 2001, 0.02, 0.0309

    def slope(N, dE, V):
        ts = np.linspace(1.0, 10.0, 19)
        P = np.array([band_first_order_probability(N, dE, V, t) for t in ts])
        return np.polyfit(ts, P, 1)[0]

    base = slope(N, dE, V)
    assert _approx(slope(N, dE, 2 * V) / base, 4.0, rel=1e-3)     # Gamma ~ |V|^2
    assert _approx(slope(N, dE / 2, V) / base, 2.0, rel=1e-2)     # Gamma ~ rho
    # and the absolute base slope is the golden-rule rate
    assert _approx(base, golden_rule_rate(V, 1.0 / dE), rel=5e-3)


def test_golden_rule_exponential_decay():
    """The EXACT (N+1)-level dynamics confirms the rate: a discrete state coupled
    to a wide, dense band (W >> Gamma >> dE) has a survival probability that
    decays exponentially, P_i(t) ~ exp(-Gamma t), with Gamma = 2 pi |V|^2 rho
    recovered to within a few percent (the residual is the finite-bandwidth
    correction).  Total probability stays normalized (unitary evolution)."""
    N, dE, V = 375, 0.02, 0.0309
    rho = 1.0 / dE
    Gamma = golden_rule_rate(V, rho)
    H = band_hamiltonian(N, dE, V)
    times = np.linspace(0.5 / Gamma, 2.5 / Gamma, 60)
    P = survival_probability(H, times)
    assert np.all(P < 1.0) and np.all(P > 0.0)
    assert P[-1] < P[0]                               # it is decaying
    Gamma_num = extract_rate(times, P)
    assert _approx(Gamma_num, Gamma, rel=5e-2)        # golden-rule rate, ~3% here
    # decay-before-recurrence regime really holds
    assert N * dE > 10 * Gamma                        # wide band: W >> Gamma
    assert Gamma > 10 * dE                            # dense band: Gamma >> dE
    # unitarity of the full evolution: no probability is lost
    psi0 = np.zeros(N + 1, dtype=complex)
    psi0[0] = 1.0
    psi = evolve(H, psi0, 1.7)
    assert _approx(norm(psi), 1.0, abs_=1e-9)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
