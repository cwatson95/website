"""QO-04  Open quantum systems -- master equations & decoherence.

Physics topic network, module QO-04 (modules/topic_network.txt).
Source: Scully & Zubairy, *Quantum Optics* (Cambridge, 1997): the density matrix
of a two-level atom (Sect. 5.3), Weisskopf-Wigner spontaneous emission (Sect. 6.3),
the quantum theory of damping / master-equation & quantum-jump picture (Ch. 8),
and the driven-damped atom / optical Bloch equations of resonance fluorescence
(Ch. 10).  Builds on ~QM-20 (the density operator, Tr rho = 1, the von Neumann
equation ihbar rho-dot = [H, rho]); ~QO-02 (the two-level atom & Rabi frequency);
~QO-03 (the spontaneous-emission rate gamma).

A CLOSED system evolves unitarily (von Neumann), conserving the spectrum of rho,
so a pure state stays pure.  An OPEN system -- coupled to a vacuum / reservoir it
cannot track -- loses purity IRREVERSIBLY.  The Markovian generator is the
**Lindblad (GKSL) master equation**

    rho-dot = -(i/hbar)[H, rho]
              + sum_k ( L_k rho L_k^dag - 1/2 { L_k^dag L_k, rho } ),

with **collapse (jump) operators** L_k.  It is completely positive and
trace-preserving (CPTP): Tr rho = 1, rho = rho^dag and rho >= 0 hold for all time.

For a two-level atom (basis |e>, |g>) spontaneous emission is the single jump
operator  L = sqrt(gamma) sigma^-,  sigma^- = |g><e|.  It gives

    rho_ee(t) = rho_ee(0) e^{-gamma t}        (population: T1 = 1/gamma)
    rho_eg(t) = rho_eg(0) e^{-(gamma/2) t}    (coherence decays at HALF the rate)

so the coherence (T2) time is 2 T1.  Adding **pure dephasing**
L_phi = sqrt(gamma_phi/2) sigma_z (elastic collisions, Sect. 5.3.3) damps the
coherence further, giving the textbook relation

    1/T2 = 1/(2 T1) + 1/T_phi .

Driving the atom (Rabi frequency Omega, detuning Delta) and letting it relax gives
the **optical Bloch equations**, whose steady state is the saturated population

    rho_ee^ss = (Omega^2/4) / (Delta^2 + gamma^2/4 + Omega^2/2)   ->  1/2  as Omega -> inf.

Units hbar = 1 throughout (pass hbar=... to override).  numpy/scipy only;
self-contained (no sibling imports).
"""

import numpy as np
from scipy.integrate import solve_ivp

__all__ = [
    # constants / two-level operators
    "HBAR", "I2", "sigma_x", "sigma_y", "sigma_z",
    "sigma_minus", "sigma_plus", "ket_e", "ket_g", "proj_e",
    # density-matrix helpers
    "density_matrix", "populations", "excited_population", "coherence",
    "is_hermitian", "is_positive_semidefinite", "is_density_matrix",
    # the master equation
    "commutator", "anticommutator", "lindblad_rhs", "evolve_lindblad",
    # the driven-damped two-level model
    "two_level_hamiltonian", "spontaneous_emission_op", "dephasing_op",
    "steady_state_excited_population",
]

HBAR = 1.0  # natural units; pass hbar=... to the master-equation routines for SI

# --- two-level atom operators, basis ordering (|e>, |g>) = (excited, ground) ---
# index 0 = |e> (excited), index 1 = |g> (ground), so rho[0,0] is the population
# that DECAYS under spontaneous emission and rho[0,1] is the optical coherence.
I2          = np.eye(2, dtype=complex)
sigma_x     = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y     = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z     = np.array([[1, 0], [0, -1]], dtype=complex)   # |e><e| - |g><g|
sigma_minus = np.array([[0, 0], [1, 0]], dtype=complex)    # |g><e|  (lowering)
sigma_plus  = np.array([[0, 1], [0, 0]], dtype=complex)    # |e><g|  (raising)
ket_e       = np.array([1, 0], dtype=complex)
ket_g       = np.array([0, 1], dtype=complex)
proj_e      = np.array([[1, 0], [0, 0]], dtype=complex)    # |e><e| = sigma^+ sigma^-

_TOL = 1e-9


# --- density-matrix helpers (a slim, self-contained restatement of ~QM-20) ----

def density_matrix(psi):
    """Pure-state density operator rho = |psi><psi| (psi normalized first).

    The diagonal entries rho_ii are POPULATIONS (probabilities), the off-diagonal
    rho_ij are COHERENCES; rho is Hermitian, unit-trace and positive (~QM-20)."""
    psi = np.asarray(psi, dtype=complex).reshape(-1)
    nrm = np.sqrt(np.vdot(psi, psi).real)
    if nrm < _TOL:
        raise ValueError("cannot normalize a zero vector")
    psi = psi / nrm
    return np.outer(psi, psi.conj())


def populations(rho):
    """The diagonal of rho as a real array -- the level populations (probabilities
    of finding the atom in each basis state).  They sum to Tr rho = 1."""
    return np.real(np.diag(np.asarray(rho, dtype=complex)))


def excited_population(rho):
    """Excited-state population rho_ee = rho[0,0] (real).  Decays as e^{-gamma t}
    under spontaneous emission -- the T1 observable."""
    return float(np.real(np.asarray(rho, dtype=complex)[0, 0]))


def coherence(rho):
    """The optical coherence rho_eg = rho[0,1] (complex).  Its magnitude decays as
    e^{-(gamma/2) t} under spontaneous emission (and faster with dephasing) -- the
    T2 observable; off-diagonal collapse to 0 IS decoherence."""
    return complex(np.asarray(rho, dtype=complex)[0, 1])


def is_hermitian(A, tol=_TOL):
    """True iff A = A^dag (so its eigenvalues -- the populations -- are real)."""
    A = np.asarray(A, dtype=complex)
    return A.ndim == 2 and A.shape[0] == A.shape[1] and \
        np.allclose(A, A.conj().T, atol=tol)


def is_positive_semidefinite(A, tol=_TOL):
    """True iff A is Hermitian with every eigenvalue >= -tol -- i.e. the
    populations are genuine probabilities (>= 0).  Preserved by Lindblad flow."""
    if not is_hermitian(A, tol):
        return False
    w = np.linalg.eigvalsh(np.asarray(A, dtype=complex)).real
    return bool(np.all(w >= -tol))


def is_density_matrix(A, tol=_TOL):
    """True iff A is a legitimate state: Hermitian, unit trace, positive
    semidefinite.  The Lindblad equation keeps every rho(t) in this set (CPTP)."""
    A = np.asarray(A, dtype=complex)
    return is_hermitian(A, tol) and abs(np.trace(A) - 1.0) <= tol \
        and is_positive_semidefinite(A, tol)


# --- the Lindblad master equation --------------------------------------------

def commutator(A, B):
    """[A, B] = A B - B A  (the unitary/Hamiltonian part of the dynamics)."""
    A = np.asarray(A, dtype=complex)
    B = np.asarray(B, dtype=complex)
    return A @ B - B @ A


def anticommutator(A, B):
    """{A, B} = A B + B A  (appears in the Lindblad 'no-jump' decay term)."""
    A = np.asarray(A, dtype=complex)
    B = np.asarray(B, dtype=complex)
    return A @ B + B @ A


def lindblad_rhs(rho, H, collapse_ops, hbar=HBAR):
    """Right-hand side rho-dot of the Lindblad (GKSL) master equation:

        rho-dot = -(i/hbar)[H, rho]
                  + sum_k ( L_k rho L_k^dag - 1/2 { L_k^dag L_k, rho } )

    `H` is the (Hermitian) Hamiltonian and `collapse_ops` a list of jump operators
    L_k (e.g. sqrt(gamma) sigma^- for spontaneous emission).  The first term is the
    von Neumann (closed-system) flow of ~QM-20; each dissipator
    D[L_k]rho = L_k rho L_k^dag - 1/2{L_k^dag L_k, rho} adds irreversible decay.

    The generator is trace-preserving (Tr rho-dot = 0) and Hermiticity-preserving,
    and the full flow is completely positive -- the CPTP property (Scully & Zubairy
    Ch. 8).  Returns the 2x2 (in general d x d) complex matrix rho-dot."""
    rho = np.asarray(rho, dtype=complex)
    H = np.asarray(H, dtype=complex)
    drho = (-1j / hbar) * commutator(H, rho)
    for L in collapse_ops:
        L = np.asarray(L, dtype=complex)
        Ldag = L.conj().T
        LdagL = Ldag @ L
        drho = drho + L @ rho @ Ldag - 0.5 * anticommutator(LdagL, rho)
    return drho


def _rho_to_y(rho):
    """Flatten a d x d complex density matrix to a real ODE vector.

    rho -> length-d^2 COMPLEX vector (its row-major ravel; the '4-vector' for a
    2x2 atom) -> split into real and imaginary parts for scipy's real-valued
    integrator: a real vector of length 2 d^2 (length 8 for a qubit)."""
    flat = np.asarray(rho, dtype=complex).ravel()
    return np.concatenate([flat.real, flat.imag])


def _y_to_rho(y, d):
    """Inverse of `_rho_to_y`: real 2 d^2-vector -> d x d complex matrix."""
    n = d * d
    flat = y[:n] + 1j * y[n:]
    return flat.reshape(d, d)


def evolve_lindblad(rho0, H, collapse_ops, times, hbar=HBAR):
    """Integrate the Lindblad master equation from rho0 over the array `times`.

    The density matrix is vectorized (rho -> a length-d^2 complex vector, stored as
    2 d^2 reals) and handed to `scipy.integrate.solve_ivp` (RK45, tight tolerances).
    Returns an array of shape (len(times), d, d): rho at each requested time.

    Because the generator is CPTP, every returned rho(t) is a valid state --
    Tr rho = 1, Hermitian, positive semidefinite -- which the tests verify."""
    rho0 = np.asarray(rho0, dtype=complex)
    d = rho0.shape[0]
    times = np.asarray(times, dtype=float)
    H = np.asarray(H, dtype=complex)
    Ls = [np.asarray(L, dtype=complex) for L in collapse_ops]

    def rhs(_t, y):
        return _rho_to_y(lindblad_rhs(_y_to_rho(y, d), H, Ls, hbar))

    sol = solve_ivp(rhs, (times[0], times[-1]), _rho_to_y(rho0),
                    t_eval=times, method="RK45", rtol=1e-9, atol=1e-12)
    if not sol.success:
        raise RuntimeError("solve_ivp failed: " + sol.message)
    return np.stack([_y_to_rho(sol.y[:, i], d) for i in range(sol.y.shape[1])])


# --- the driven-damped two-level atom (optical Bloch, Scully & Zubairy Ch. 10) -

def two_level_hamiltonian(omega_rabi, detuning=0.0, hbar=HBAR):
    """Rotating-frame two-level Hamiltonian (rotating-wave approximation):

        H = hbar*Delta |e><e| + (hbar*Omega/2) sigma_x ,

    Omega = `omega_rabi` the Rabi frequency, Delta = `detuning` = omega_laser
    minus omega_atom.  The sigma_x term is the coherent drive that builds up
    coherence; Delta is the laser-atom mismatch (~QO-02)."""
    return hbar * detuning * proj_e + 0.5 * hbar * omega_rabi * sigma_x


def spontaneous_emission_op(gamma):
    """Spontaneous-emission collapse operator  L = sqrt(gamma) sigma^- ,
    sigma^- = |g><e|.  gamma is the Einstein-A / Weisskopf-Wigner decay rate
    (~QO-03); it gives rho_ee ~ e^{-gamma t} (T1 = 1/gamma) and coherence
    ~ e^{-(gamma/2) t}."""
    return np.sqrt(gamma) * sigma_minus


def dephasing_op(gamma_phi):
    """Pure-dephasing collapse operator  L_phi = sqrt(gamma_phi/2) sigma_z .

    Models elastic, population-conserving phase-scrambling collisions
    (Scully & Zubairy Sect. 5.3.3).  It damps ONLY the coherence, at rate
    gamma_phi = 1/T_phi, so combined with emission  1/T2 = 1/(2 T1) + 1/T_phi."""
    return np.sqrt(gamma_phi / 2.0) * sigma_z


def steady_state_excited_population(omega_rabi, gamma, detuning=0.0):
    """Optical-Bloch steady-state excited population (Scully & Zubairy Ch. 10):

        rho_ee^ss = (Omega^2/4) / (Delta^2 + gamma^2/4 + Omega^2/2).

    On resonance (Delta = 0) this is Omega^2 / (gamma^2 + 2 Omega^2), rising from 0
    to the saturation value 1/2 as Omega -> infinity (you cannot invert a two-level
    atom with a classical field)."""
    return (omega_rabi ** 2 / 4.0) / (
        detuning ** 2 + gamma ** 2 / 4.0 + omega_rabi ** 2 / 2.0)


# --- helper: extract a decay rate from a simulated signal --------------------

def _fit_rate(times, signal):
    """Decay rate from a (noiseless) exponential signal: -slope of log(signal),
    fitted where the signal is well above round-off.  Used by the demo/tests to
    READ the decay rate back out of the simulation."""
    times = np.asarray(times, dtype=float)
    signal = np.asarray(signal, dtype=float)
    mask = signal > 1e-7 * np.max(signal)
    slope = np.polyfit(times[mask], np.log(signal[mask]), 1)[0]
    return float(-slope)


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QO-04  Open quantum systems -- master equations & decoherence")
    print("=" * 62)

    gamma = 1.0                      # spontaneous-emission rate (sets the time unit)
    T1 = 1.0 / gamma

    # 1) Spontaneous emission: start in |+> = (|e>+|g>)/sqrt2 so we see BOTH the
    #    population decay (rate gamma) and the coherence decay (rate gamma/2).
    psi_plus = (ket_e + ket_g) / np.sqrt(2.0)
    rho0 = density_matrix(psi_plus)
    t = np.linspace(0.0, 6.0 * T1, 400)
    L_spont = spontaneous_emission_op(gamma)
    rhos = evolve_lindblad(rho0, np.zeros((2, 2)), [L_spont], t)

    pe = np.array([excited_population(r) for r in rhos])
    coh = np.array([abs(coherence(r)) for r in rhos])
    traces = np.array([np.real(np.trace(r)) for r in rhos])
    min_eig = min(np.linalg.eigvalsh(r).min().real for r in rhos)

    g_fit = _fit_rate(t, pe)              # should be gamma
    g2_fit = _fit_rate(t, coh)            # should be gamma/2
    print("\n1) Spontaneous emission (start |+>, H = 0, L = sqrt(gamma) sigma^-):")
    print(f"   population rho_ee:  fitted rate = {g_fit:.4f}   (input gamma   = {gamma:.4f})  -> T1 = {1/g_fit:.3f}")
    print(f"   coherence |rho_eg|: fitted rate = {g2_fit:.4f}   (gamma/2        = {gamma/2:.4f})  -> T2 = {1/g2_fit:.3f} = 2 T1")
    print(f"   closed forms: rho_ee(t)=e^-gt, max|sim-form| = "
          f"{np.max(np.abs(pe - 0.5*np.exp(-gamma*t))):.2e}")
    print(f"   trace conserved: max|Tr rho - 1| = {np.max(np.abs(traces-1)):.2e}; "
          f"min eigenvalue over run = {min_eig:+.2e} (>= 0)")
    print(f"   final state (t={t[-1]:.0f}/gamma): rho_ee = {pe[-1]:.4f} -> "
          f"decays to the GROUND state |g><g|")

    # 2) Pure dephasing adds to give T2:  1/T2 = 1/(2 T1) + 1/T_phi
    gamma_phi = 0.8
    rhos2 = evolve_lindblad(rho0, np.zeros((2, 2)),
                            [L_spont, dephasing_op(gamma_phi)], t)
    coh2 = np.array([abs(coherence(r)) for r in rhos2])
    rate_T2 = _fit_rate(t, coh2)
    print("\n2) Add pure dephasing L_phi = sqrt(gamma_phi/2) sigma_z, "
          f"gamma_phi = {gamma_phi}:")
    print(f"   coherence decay rate 1/T2 = {rate_T2:.4f}")
    print(f"   prediction 1/(2 T1) + 1/T_phi = {gamma/2:.4f} + {gamma_phi:.4f} "
          f"= {gamma/2 + gamma_phi:.4f}")

    # 3) Driven + damped: optical Bloch steady state vs the analytic formula.
    print("\n3) Driven + damped two-level atom (optical Bloch steady state):")
    ts = np.linspace(0.0, 40.0 * T1, 800)
    for Omega, Delta in [(2.0, 0.0), (2.0, 1.5), (8.0, 0.0)]:
        H = two_level_hamiltonian(Omega, Delta)
        traj = evolve_lindblad(density_matrix(ket_g), H, [L_spont], ts)
        sim = excited_population(traj[-1])
        ana = steady_state_excited_population(Omega, gamma, Delta)
        print(f"   Omega={Omega:4.1f}, Delta={Delta:4.1f}:  rho_ee^ss(sim) = "
              f"{sim:.4f}   formula = {ana:.4f}   |diff| = {abs(sim-ana):.1e}")
    print(f"   saturation: Omega->inf gives rho_ee^ss -> "
          f"{steady_state_excited_population(1e6, gamma):.4f} (= 1/2; cannot invert)")


if __name__ == "__main__":
    _demo()
