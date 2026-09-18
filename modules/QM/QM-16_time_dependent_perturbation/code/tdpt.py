"""
QM-16  Time-dependent perturbation theory, Rabi oscillations & Fermi's golden
rule  --  transitions between quantum states, as formulae and dynamics you can
evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-16).
Builds on ~QM-15 (the time-INDEPENDENT counterpart: perturbing the energy
levels) and ~QM-05/~QM-06 (states, observables, the Born rule that turns
|c_f(t)|^2 into a measured transition probability); ~QM-11 supplies the two-level
/ spin language.  Points forward to ~QM-17 (selection rules) and bridges to
~QO-03 (laser physics / stimulated emission), which is not yet built.

The chapter (Griffiths 3e Ch. 11 "Quantum Dynamics"), as four function groups:

  1. Evolution primitives.  Exact unitary evolution e^{-iHt} for a time-
     INDEPENDENT H (eigendecomposition), and an honest integrator for the
     time-DEPENDENT Schrodinger equation  i d|psi>/dt = H(t)|psi>.
     (evolve, evolve_tdse)

  2. First-order transition amplitude (the master formula, Griffiths Sec. 11.1.2):
         c_f^(1)(t) = -(i/hbar) integral_{t0}^{t} <f|H'(t')|i> e^{i w_fi t'} dt'
     and P_{i->f} = |c_f^(1)|^2.  Works for any matrix element (constant or a
     function of time).
     (first_order_amplitude, first_order_probability)

  3. Two-level system & Rabi oscillations (Griffiths Sec. 11.1, Prob. 11.9).
     The EXACT generalized Rabi formula
         P = (W_R^2 / (W_R^2 + d^2)) sin^2( sqrt(W_R^2 + d^2) t / 2 )
     (W_R = Rabi frequency, d = detuning), recovered from the exact 2x2
     evolution; full inversion on resonance (d=0); first-order PT reproduces it
     in the weak/short-time limit.  Sinusoidal driving gives the resonance
     line shape (Griffiths Sec. 11.1.3, Eq. 11.35): a sinc^2 in (w - w_fi),
     peak ~ t^2, width ~ 1/t.
     (two_level_H, generalized_rabi_frequency, rabi_probability,
      sinusoidal_probability, make_driven_H)

  4. Fermi's golden rule (Griffiths Sec. 11.4).  A discrete state coupled to a
     dense band of N final states with density of states rho decays
     exponentially with the golden-rule rate
         Gamma = (2 pi / hbar) |<f|H'|i>|^2 rho(E_f).
     (golden_rule_rate, band_hamiltonian, survival_probability,
      instantaneous_rate, extract_rate)

Natural units:  hbar = 1  throughout (energies are angular frequencies and rates;
times are 1/energy).  All operators are numpy complex arrays; states are complex
column vectors.  Convention for transitions: i = initial, f = final.
"""

import numpy as np
from scipy.integrate import quad, solve_ivp

__all__ = [
    "HBAR",
    # 1. evolution primitives
    "evolve", "evolve_tdse", "norm", "amplitude",
    # 2. first-order amplitude
    "first_order_amplitude", "first_order_probability",
    # 3. two-level / Rabi / sinusoidal
    "two_level_H", "generalized_rabi_frequency", "rabi_probability",
    "two_level_exact_probability", "sinusoidal_probability", "make_driven_H",
    # 4. Fermi's golden rule
    "golden_rule_rate", "band_hamiltonian", "band_first_order_probability",
    "survival_probability", "instantaneous_rate", "extract_rate",
]

HBAR = 1.0  # natural units

_TOL = 1e-12


# --- 1. evolution primitives -------------------------------------------------

def amplitude(f, psi):
    """Transition amplitude <f|psi>.  `f` may be a state vector or a basis index
    (an integer, meaning the f-th computational basis ket)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    if np.isscalar(f) or (isinstance(f, (int, np.integer))):
        return psi[int(f)]
    f = np.asarray(f, dtype=complex).reshape(-1)
    return np.vdot(f, psi)


def norm(psi):
    """The norm sqrt(<psi|psi>) of a state (should stay 1 under unitary evolution)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    return float(np.sqrt(np.vdot(psi, psi).real))


def evolve(H, psi0, t):
    """Exact unitary evolution of |psi0> for time t under a TIME-INDEPENDENT
    Hamiltonian H:  |psi(t)> = e^{-i H t / hbar} |psi0>   (hbar = 1).

    Computed by diagonalizing the Hermitian H once (spectral theorem, ~QM-05),
    so it is exact to machine precision and cheap to repeat over many t.  `t` may
    be a scalar (returns one state) or an array (returns an array of states,
    shape (len(t), dim)).  This is the rotating-frame engine for the two-level
    Rabi problem and the (N+1)-level golden-rule band."""
    H = np.asarray(H, dtype=complex)
    psi0 = np.asarray(psi0, dtype=complex).reshape(-1)
    w, V = np.linalg.eigh(H)               # H = V diag(w) V^dagger
    c0 = V.conj().T @ psi0                 # components in the energy eigenbasis
    if np.isscalar(t):
        return V @ (np.exp(-1j * w * t) * c0)
    t = np.asarray(t, dtype=float)
    phases = np.exp(-1j * np.outer(t, w))  # (len(t), dim)
    return (phases * c0) @ V.T             # (len(t), dim)


def evolve_tdse(H_of_t, psi0, t, rtol=1e-10, atol=1e-12):
    """Honest numerical integration of the time-dependent Schrodinger equation

        i hbar d|psi>/dt = H(t) |psi>            (hbar = 1)

    for a TIME-DEPENDENT Hamiltonian `H_of_t(t)` (a callable returning a square
    complex matrix).  Returns |psi(t)>.  Used to validate first-order
    perturbation theory against the true dynamics of a driven system -- no RWA,
    no weak-coupling assumption (Griffiths Sec. 11.1: Eqs. 11.14-11.17 are the
    exact 2-level equations; here we integrate the operator form directly)."""
    psi0 = np.asarray(psi0, dtype=complex).reshape(-1)

    def rhs(tt, y):
        return -1j * (np.asarray(H_of_t(tt), dtype=complex) @ y)

    sol = solve_ivp(rhs, [0.0, float(t)], psi0, rtol=rtol, atol=atol,
                    method="DOP853")
    return sol.y[:, -1]


# --- 2. first-order transition amplitude (the master formula) ----------------

def first_order_amplitude(matrix_element, omega_fi, t, t0=0.0):
    """First-order transition amplitude (Griffiths 3e Sec. 11.1.2, Eq. 11.21):

        c_f^(1)(t) = -(i/hbar) integral_{t0}^{t} <f|H'(t')|i> e^{i w_fi t'} dt'

    with hbar = 1.  `matrix_element` is <f|H'(t')|i>: either a constant (number)
    or a callable t' -> complex.  `omega_fi = (E_f - E_i)/hbar` is the transition
    (Bohr) frequency.  The integral is done numerically (real and imaginary parts
    separately) so it is exact for any time profile -- a delta kick, a switch-on,
    or a sinusoid.  Returns the complex amplitude c_f^(1)(t); square it (or call
    first_order_probability) for the transition probability."""
    if callable(matrix_element):
        f = matrix_element
    else:
        me = complex(matrix_element)
        f = lambda tp: me

    re = quad(lambda tp: (f(tp) * np.exp(1j * omega_fi * tp)).real,
              t0, t, limit=400)[0]
    im = quad(lambda tp: (f(tp) * np.exp(1j * omega_fi * tp)).imag,
              t0, t, limit=400)[0]
    return -1j * (re + 1j * im) / HBAR


def first_order_probability(matrix_element, omega_fi, t, t0=0.0):
    """First-order transition probability  P_{i->f}(t) = |c_f^(1)(t)|^2
    (Griffiths 3e Sec. 11.1.2).  Valid while P << 1 (else higher orders, or the
    exact treatment, are needed)."""
    return abs(first_order_amplitude(matrix_element, omega_fi, t, t0)) ** 2


# --- 3. two-level system, Rabi oscillations, sinusoidal resonance ------------

def two_level_H(delta, Omega_R):
    """Rotating-frame Hamiltonian of a driven two-level system (hbar = 1):

        H = (1/2) [[ delta ,  Omega_R ],
                   [ Omega_R, -delta  ]]
          = (Omega_R/2) sigma_x + (delta/2) sigma_z

    `delta = omega - omega_fi` is the detuning of the drive from resonance and
    `Omega_R` is the Rabi frequency (proportional to the drive amplitude times
    the dipole matrix element).  The initial state |i> = (1,0) is the lower level
    in the rotating frame; |f> = (0,1) is the upper one.  Diagonalizing this
    time-INDEPENDENT matrix and evolving with `evolve` reproduces the exact Rabi
    oscillation (Griffiths Sec. 11.1; the rotating-wave approximation of
    Prob. 11.9 is what makes the driven problem time-independent here)."""
    return 0.5 * np.array([[delta, Omega_R],
                           [Omega_R, -delta]], dtype=complex)


def generalized_rabi_frequency(Omega_R, delta):
    """Generalized (flopping) Rabi frequency  Omega = sqrt(Omega_R^2 + delta^2)
    (Griffiths Prob. 11.9, Eq. 11.37).  The population flops at this frequency;
    on resonance (delta=0) it equals the bare Rabi frequency Omega_R."""
    return np.hypot(Omega_R, delta)


def rabi_probability(t, Omega_R, delta):
    """EXACT two-level transition probability -- the generalized Rabi formula:

        P_{i->f}(t) = (Omega_R^2 / (Omega_R^2 + delta^2))
                       * sin^2( sqrt(Omega_R^2 + delta^2) * t / 2 )

    (Griffiths 3e Prob. 11.9, Eq. 11.37; this is the closed form of evolving
    `two_level_H`).  Key features, all checked in the tests:
      * On resonance (delta = 0):  P = sin^2(Omega_R t / 2)  -> reaches 1, a
        complete population inversion at t = pi/Omega_R.
      * Off resonance: the amplitude is capped at Omega_R^2/(Omega_R^2+delta^2)
        < 1, and the flopping speeds up to sqrt(Omega_R^2+delta^2).
      * It never exceeds 1 (unlike the first-order PT estimate)."""
    Omega = generalized_rabi_frequency(Omega_R, delta)
    if Omega < _TOL:                    # no coupling and no detuning: no transition
        return 0.0
    return (Omega_R ** 2 / Omega ** 2) * np.sin(Omega * t / 2.0) ** 2


def two_level_exact_probability(t, delta, Omega_R, init=0, final=1):
    """Exact two-level transition probability from the *dynamics*: evolve
    `two_level_H` for time t and read |<final|psi(t)>|^2.  Equals
    `rabi_probability` to machine precision -- the function exists so the test
    suite can confirm the closed form against the actual time evolution."""
    psi0 = np.zeros(2, dtype=complex)
    psi0[init] = 1.0
    psi = evolve(two_level_H(delta, Omega_R), psi0, t)
    return abs(amplitude(final, psi)) ** 2


def sinusoidal_probability(t, omega, omega_fi, V_fi):
    """Transition probability under a sinusoidal perturbation H'(t)=V cos(w t),
    to first order and in the rotating-wave (near-resonance) approximation
    (Griffiths 3e Sec. 11.1.3, Eq. 11.35; hbar = 1):

        P_{i->f}(t) = |V_fi|^2  sin^2[(w_fi - w) t / 2] / (w_fi - w)^2

    where V_fi = <f|V|i> is the (amplitude of the) matrix element and
    w_fi = (E_f - E_i)/hbar.  As a function of the drive frequency w this is a
    sinc^2 line shape centred on resonance w = w_fi, with central-peak height
    |V_fi|^2 t^2 / 4 (the delta -> 0 limit handled below) and first zeros at
    w = w_fi +/- 2 pi / t -- the peak grows like t^2 and narrows like 1/t."""
    d = omega_fi - omega
    d = np.asarray(d, dtype=float)
    small = np.abs(d) < _TOL
    # safe evaluation: replace tiny denominators, then patch with the limit
    d_safe = np.where(small, 1.0, d)
    P = np.abs(V_fi) ** 2 * np.sin(d_safe * t / 2.0) ** 2 / d_safe ** 2
    P = np.where(small, (np.abs(V_fi) * t / 2.0) ** 2, P)
    return P if P.ndim else float(P)


def make_driven_H(omega, omega_fi, V_fi, E_i=0.0):
    """Build the *lab-frame*, time-DEPENDENT two-level Hamiltonian for a
    sinusoidal drive (to feed `evolve_tdse`):

        H(t) = [[E_i,            V_fi cos(w t)        ],
                [V_fi cos(w t),  E_i + w_fi           ]]

    so the bare levels are split by w_fi = (E_f - E_i)/hbar and the off-diagonal
    coupling is the full cosine (BOTH the co- and counter-rotating terms -- no
    RWA).  Integrating this with `evolve_tdse` is the honest dynamics that
    first-order PT (Eq. 11.32) and the RWA formula (Eq. 11.35) approximate."""
    H0 = np.diag([E_i, E_i + omega_fi]).astype(complex)
    off = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    def H_of_t(t):
        return H0 + V_fi * np.cos(omega * t) * off

    return H_of_t


# --- 4. Fermi's golden rule --------------------------------------------------

def golden_rule_rate(V, rho):
    """Fermi's golden rule transition rate (Griffiths 3e Sec. 11.4, Eq. 11.81):

        Gamma = (2 pi / hbar) |<f|H'|i>|^2 rho(E_f)            (hbar = 1)

    `V` is the (constant) coupling matrix element <f|H'|i>; `rho` is the density
    of final states at the resonant energy E_f = E_i.  This is the rate at which
    the initial state empties into a continuum; the survival probability decays
    as exp(-Gamma t)."""
    return 2.0 * np.pi * np.abs(V) ** 2 * rho / HBAR


def band_hamiltonian(N, level_spacing, V, E_init=0.0):
    """Wigner-Weisskopf 'star' model of a discrete state coupled to a band
    (Griffiths 3e Sec. 11.4): one initial state |i> at energy E_init, coupled
    with constant strength V to N final states |f_k> whose energies are evenly
    spaced by `level_spacing` (dE) and centred on E_init,

        E_k = (k - (N-1)/2) dE,   k = 0..N-1,

    with the final states NOT coupled to each other.  Returns the
    (N+1) x (N+1) Hermitian Hamiltonian; index 0 is the initial state.  The
    density of final states is rho = 1/dE, the bandwidth is W = N dE, and the
    recurrence (Poincare) time is 2 pi / dE.  In the wide-band, dense-band
    regime (W >> Gamma >> dE) the initial state decays exponentially at the
    golden-rule rate Gamma = 2 pi V^2 / dE = 2 pi V^2 rho."""
    M = N + 1
    H = np.zeros((M, M), dtype=complex)
    H[0, 0] = E_init
    E_k = (np.arange(N) - (N - 1) / 2.0) * level_spacing + E_init
    H[0, 1:] = V
    H[1:, 0] = np.conj(V)
    H[1:, 1:] = np.diag(E_k)
    return H


def band_first_order_probability(N, level_spacing, V, t, E_init=0.0):
    """Total FIRST-ORDER transition probability out of |i> into the whole band,

        P_band^(1)(t) = sum_k |c_k^(1)(t)|^2
                      = sum_k |V|^2 * 4 sin^2(E_k t / 2) / E_k^2 ,

    i.e. the integral of the single-state result (Griffiths Eq. 11.35 with
    omega=0, a constant switched-on coupling) over all final states
    (Griffiths Eq. 11.79).  This is the literal derivation of the golden rule:
    in the regime  1/W << t << 1/dE  the sinc^2 around resonance is well sampled
    and fully contained in the band, so the sum becomes linear in t,

        P_band^(1)(t)  ->  Gamma t ,   Gamma = 2 pi |V|^2 rho = 2 pi |V|^2 / dE

    (Eq. 11.81).  The constant slope IS Fermi's golden-rule rate; first order
    has no saturation, so the linearity (and hence the rate) is clean over a wide
    window even though P itself eventually exceeds 1 (the usual PT breakdown)."""
    E_k = (np.arange(N) - (N - 1) / 2.0) * level_spacing
    d = E_k                                  # E_k - E_init relative to resonance
    small = np.abs(d) < _TOL
    d_safe = np.where(small, 1.0, d)
    P = np.abs(V) ** 2 * 4.0 * np.sin(d_safe * t / 2.0) ** 2 / d_safe ** 2
    P = np.where(small, (np.abs(V) * t) ** 2, P)   # resonant level: |V|^2 t^2
    return float(np.sum(P))


def survival_probability(H, times, init=0):
    """Survival probability of the initial state under a time-independent H:

        P_i(t) = |<i| e^{-i H t} |i>|^2

    `times` is an array; returns the array of P_i(t).  For the band Hamiltonian
    this is the population that has NOT yet decayed into the continuum; in the
    golden-rule regime it follows exp(-Gamma t) (Griffiths Sec. 11.4)."""
    H = np.asarray(H, dtype=complex)
    times = np.atleast_1d(np.asarray(times, dtype=float))
    psi0 = np.zeros(H.shape[0], dtype=complex)
    psi0[init] = 1.0
    states = evolve(H, psi0, times)           # (len(times), dim)
    return np.abs(states[:, init]) ** 2


def instantaneous_rate(times, P):
    """Instantaneous decay rate  -d(ln P)/dt  as a function of time.  In the
    golden-rule regime this plateaus at Gamma (exponential decay); at very short
    times it ramps up from 0 (the quadratic Zeno onset) and at long times it
    wobbles as discreteness/recurrences set in."""
    times = np.asarray(times, dtype=float)
    P = np.asarray(P, dtype=float)
    return -np.gradient(np.log(P), times)


def extract_rate(times, P):
    """Robust single estimate of the exponential decay constant Gamma from a
    survival curve P(t): the median of the instantaneous rate -d(ln P)/dt over
    the central half of the time window (so the short-time onset and any
    long-time recurrence are trimmed off).  Compare to golden_rule_rate()."""
    r = instantaneous_rate(times, P)
    n = len(r)
    lo, hi = n // 4, max(n // 4 + 1, 3 * n // 4)
    return float(np.median(r[lo:hi]))


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-16  Time-dependent perturbation theory, Rabi & Fermi's golden rule")
    print("=" * 70)
    print("(natural units, hbar = 1)\n")

    # --- two-level Rabi -----------------------------------------------------
    print("[1] Two-level system -- Rabi oscillations (exact 2x2 evolution)")
    Omega_R = 1.0
    print("    On resonance (delta=0): full inversion at t = pi/Omega_R")
    t_inv = np.pi / Omega_R
    print("      P(t=pi/Omega_R) = %.6f   (exact dynamics: %.6f)"
          % (rabi_probability(t_inv, Omega_R, 0.0),
             two_level_exact_probability(t_inv, 0.0, Omega_R)))
    for delta in (0.0, 1.0, 3.0):
        cap = Omega_R ** 2 / (Omega_R ** 2 + delta ** 2)
        print("      detuning delta=%.1f : amplitude capped at %.4f" % (delta, cap))

    # --- first-order PT reproduces the weak/short limit ---------------------
    print("\n[2] First-order PT reproduces Rabi in the weak-coupling limit")
    Omega_R, delta, t = 0.02, 0.5, 8.0
    exact = rabi_probability(t, Omega_R, delta)
    pt = first_order_probability(Omega_R / 2.0, -delta, t)   # rotating frame
    print("    Omega_R=%.2f << |delta|=%.2f, t=%.1f :  exact=%.3e  first-order=%.3e"
          % (Omega_R, delta, t, exact, pt))

    # --- sinusoidal resonance -----------------------------------------------
    print("\n[3] Sinusoidal perturbation -- resonance line shape (Eq. 11.35)")
    omega_fi, V_fi, t = 1.0, 0.01, 40.0
    ws = np.linspace(0.7, 1.3, 4001)
    P = sinusoidal_probability(t, ws, omega_fi, V_fi)
    print("    peak at w = %.4f  (w_fi = %.2f),  height = %.3e  (|V_fi|^2 t^2/4 = %.3e)"
          % (ws[np.argmax(P)], omega_fi, P.max(), (V_fi * t / 2) ** 2))
    print("    first zeros expected at w_fi +/- 2pi/t = 1 +/- %.4f" % (2 * np.pi / t))

    # --- Fermi's golden rule ------------------------------------------------
    print("\n[4] Fermi's golden rule -- discrete state decaying into a band")
    N, dE, V = 375, 0.02, 0.0309
    rho = 1.0 / dE
    Gamma = golden_rule_rate(V, rho)
    H = band_hamiltonian(N, dE, V)
    times = np.linspace(0.5 / Gamma, 2.5 / Gamma, 60)
    P = survival_probability(H, times)
    Gamma_num = extract_rate(times, P)
    print("    N=%d states, spacing dE=%.3f -> rho=%.1f, coupling V=%.4f"
          % (N, dE, rho, V))
    print("    Gamma (golden rule, 2*pi*V^2*rho) = %.4f" % Gamma)
    print("    Gamma (numerical decay rate)      = %.4f   (ratio %.3f)"
          % (Gamma_num, Gamma_num / Gamma))
    print("    bandwidth W=%.1f >> Gamma >> dE=%.3f ;  recurrence time = %.0f"
          % (N * dE, dE, 2 * np.pi / dE))


if __name__ == "__main__":
    _demo()
