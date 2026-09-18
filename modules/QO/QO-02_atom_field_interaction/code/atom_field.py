"""QO-02  Atom-field interaction -- Rabi oscillations & the Jaynes-Cummings model.

Physics topic network, module QO-02 (modules/topic_network.txt), trunk QO
(Quantum & Nonlinear Optics).  Source: Scully & Zubairy, *Quantum Optics*
(Cambridge, 1997).  The SEMICLASSICAL two-level atom and Rabi flopping are their
Ch. 5 (Sect. 5.2, with 5.2.3 "Beyond the rotating-wave approximation"); the fully
QUANTIZED Jaynes-Cummings model -- dressed states, vacuum Rabi splitting, and the
collapse-and-revival of the atomic inversion -- is their Ch. 6 (Sect. 6.1-6.2).

Builds on ~QM-11 (the two-level system / Pauli operators sigma_z, sigma^+,
sigma^-) and ~QM-16 (time-dependent perturbation: the dipole drive -d.E); the
photon-number states |n> and the coherent state |alpha> are those of ~QO-01.

Three layers, each a function group below:

  1. Two-level atom        sigma_z = |e><e| - |g><g|,  sigma^+ = |e><g| (raises
                           g -> e),  sigma^- = |g><e| (lowers e -> g): exactly the
                           spin-1/2 / qubit algebra of ~QM-11, with |e> <-> up.

  2. Semiclassical Rabi    a CLASSICAL field E_0 cos(w_L t) drives the dipole; in
                           the rotating-wave approximation the excited-state
                           probability of an atom started in |g> is
                              P_e(t) = (Om^2 / Om_R^2) sin^2(Om_R t / 2),
                           with generalized Rabi frequency Om_R = sqrt(Om^2 + d^2),
                           Rabi coupling Om = d_eg E_0 / hbar, and detuning
                           d = w_a - w_L.  ON RESONANCE (d=0): P_e = sin^2(Om t/2)
                           -- complete inversion at Om t = pi (a "pi-pulse"), back
                           to 0 at Om t = 2 pi.  OFF resonance the flop never
                           finishes, saturating at Om^2/(Om^2 + d^2) < 1.

  3. Jaynes-Cummings model quantize the single field mode:
                              H = w_c a^dag a + (1/2) w_a sigma_z
                                    + g (a sigma^+ + a^dag sigma^-).
                           The interaction is already rotating-wave: a sigma^+
                           absorbs a photon AND excites the atom; a^dag sigma^-
                           emits AND de-excites.  The excitation number
                           a^dag a + |e><e| is therefore conserved, so H breaks
                           into 2x2 blocks {|e,n>, |g,n+1>}.  Diagonalizing a block
                           gives the DRESSED states with energies
                              E_{n,±} = w_c(n + 1/2) ± (1/2) sqrt(d^2 + 4 g^2(n+1)),
                           d = w_a - w_c, a splitting 2 g sqrt(n+1); for n=0 this is
                           the VACUUM RABI SPLITTING 2g (a single quantum -- even the
                           vacuum -- lifts the {|e,0>,|g,1>} degeneracy).  An atom in
                           |e> over a COHERENT field |alpha> shows the inversion
                           <sigma_z>(t) COLLAPSE (t_c ~ sqrt2/g) and then partially
                           REVIVE (t_r ~ 2 pi sqrt(nbar)/g) -- a hallmark of field
                           quantization with no semiclassical counterpart.

UNITS: hbar = 1 throughout (set HBAR below); every angular frequency is an energy
and every time is 1/energy.  Restore SI by carrying HBAR = 1.054571817e-34.
"""

import numpy as np
from scipy.linalg import expm

__all__ = [
    "HBAR",
    # 1. two-level atom (~QM-11)
    "I2", "sigma_z", "sigma_plus", "sigma_minus", "ket_e", "ket_g",
    # 2. semiclassical Rabi oscillations (S&Z Ch. 5)
    "generalized_rabi", "rabi_excited_population", "two_level_hamiltonian",
    # 3. field operators and states (~QO-01)
    "annihilation", "number_operator", "coherent_state",
    # Jaynes-Cummings model (S&Z Ch. 6)
    "jcm_hamiltonian", "dressed_energies", "vacuum_rabi_splitting",
    "jcm_inversion", "resonant_inversion_series", "collapse_time", "revival_time",
]

HBAR = 1.0  # natural units; restore SI with HBAR = 1.054571817e-34


# --- 1. the two-level atom (Pauli operators of ~QM-11) -----------------------
# Basis order (|e>, |g>) = ((1,0), (0,1)): excited first, like spin "up".

I2 = np.eye(2, dtype=complex)
sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)       # |e><e| - |g><g|
sigma_plus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)     # |e><g|  (raise)
sigma_minus = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=complex)    # |g><e|  (lower)
ket_e = np.array([1.0, 0.0], dtype=complex)                        # excited
ket_g = np.array([0.0, 1.0], dtype=complex)                        # ground


# --- 2. semiclassical Rabi oscillations (Scully-Zubairy Sect. 5.2) -----------

def generalized_rabi(Omega, detuning):
    """Generalized Rabi frequency  Om_R = sqrt(Om^2 + d^2): the rate at which a
    driven two-level atom flops between its levels, faster the further off
    resonance.  On resonance (d=0) it reduces to the bare Rabi coupling Om."""
    return np.sqrt(Omega ** 2 + detuning ** 2)


def rabi_excited_population(t, Omega, detuning=0.0):
    """Rabi formula -- probability that an atom started in the ground state |g> is
    found excited at time t under a classical drive (rotating-wave approximation):

        P_e(t) = (Om^2 / Om_R^2) sin^2(Om_R t / 2),   Om_R = sqrt(Om^2 + d^2),

    with Rabi coupling Om and detuning d = w_a - w_L (Scully-Zubairy Sect. 5.2).
    ON RESONANCE (d=0) this is sin^2(Om t/2): a full inversion (P_e=1) at Om t=pi
    and a return to P_e=0 at Om t=2 pi.  OFF resonance the maximum transfer is the
    saturated amplitude  Om^2 / (Om^2 + d^2) < 1.  Accepts scalar or array t."""
    t = np.asarray(t, dtype=float)
    OmR = generalized_rabi(Omega, detuning)
    if OmR == 0.0:                       # no drive and no detuning: nothing happens
        out = np.zeros_like(t)
    else:
        out = (Omega ** 2 / OmR ** 2) * np.sin(OmR * t / 2.0) ** 2
    return out if out.ndim else float(out)


def two_level_hamiltonian(Omega, detuning):
    """Rotating-frame two-level Hamiltonian in the rotating-wave approximation,

        H = (1/2)(d sigma_z + Om sigma_x),   sigma_x = sigma^+ + sigma^-,

    with Rabi coupling Om and detuning d.  Its eigenvalues are ±Om_R/2; evolving
    |g> with exp(-iHt) and projecting on |e> reproduces `rabi_excited_population`
    exactly (the dynamical check of the closed form).  Scully-Zubairy Sect. 5.2."""
    sigma_x = sigma_plus + sigma_minus
    return 0.5 * (detuning * sigma_z + Omega * sigma_x)


# --- 3a. single-mode field operators and states (~QO-01) ---------------------

def annihilation(N):
    """Truncated bosonic annihilation operator a on an N-level Fock space:
    a|n> = sqrt(n)|n-1> for n = 0..N-1 (so a|0> = 0).  The creation operator is
    a^dag = a.conj().T and the number operator a^dag a = diag(0,1,...,N-1).
    Truncation only matters for states with appreciable weight near |N-1>."""
    return np.diag(np.sqrt(np.arange(1, N)), 1).astype(complex)


def number_operator(N):
    """Photon-number operator  n_hat = a^dag a = diag(0, 1, ..., N-1)."""
    return np.diag(np.arange(N)).astype(complex)


def coherent_state(alpha, N):
    """Truncated, renormalized coherent state (~QO-01)

        |alpha> = e^{-|alpha|^2/2} sum_n alpha^n / sqrt(n!) |n>,

    the eigenstate of a with eigenvalue alpha.  Its photon statistics are
    Poissonian, P_n = e^{-nbar} nbar^n / n!, with mean nbar = |alpha|^2.  Built by
    the stable recursion c_n = c_{n-1} alpha / sqrt(n) and renormalized so the
    truncated vector has unit norm (negligible for N >> nbar)."""
    c = np.zeros(N, dtype=complex)
    c[0] = np.exp(-0.5 * abs(alpha) ** 2)
    for n in range(1, N):
        c[n] = c[n - 1] * alpha / np.sqrt(n)
    return c / np.linalg.norm(c)


# --- 3b. the Jaynes-Cummings model (Scully-Zubairy Ch. 6) --------------------

def jcm_hamiltonian(omega_c, omega_a, g, N):
    """Jaynes-Cummings Hamiltonian on (2-level atom) (x) (N-level field), hbar=1:

        H = w_c a^dag a + (1/2) w_a sigma_z + g (a sigma^+ + a^dag sigma^-),

    assembled as numpy kron of the 2x2 atom and N x N field operators in
    atom (x) field order, so the basis index of |atom, n> is atom*N + n.  The
    rotating-wave interaction conserves the excitation number a^dag a + |e><e|,
    so H is block-diagonal in the doublets {|e,n>, |g,n+1>} (Scully-Zubairy
    Sect. 6.1-6.2)."""
    a = annihilation(N)
    adag = a.conj().T
    IN = np.eye(N, dtype=complex)
    H = (omega_c * np.kron(I2, adag @ a)
         + 0.5 * omega_a * np.kron(sigma_z, IN)
         + g * (np.kron(sigma_plus, a) + np.kron(sigma_minus, adag)))
    return H


def dressed_energies(n, detuning, g, omega_c):
    """The two DRESSED-STATE energies of the {|e,n>, |g,n+1>} doublet, i.e. the
    eigenvalues of the n-th 2x2 block of `jcm_hamiltonian`:

        E_{n,±} = w_c (n + 1/2) ± (1/2) sqrt(d^2 + 4 g^2 (n+1)),   d = w_a - w_c.

    The gap E_{n,+} - E_{n,-} = sqrt(d^2 + 4 g^2 (n+1)) becomes 2 g sqrt(n+1) on
    resonance (d=0); at n=0 that is the VACUUM RABI SPLITTING 2g.  (Measuring the
    atom from its ground state, H_atom = w_a sigma^+ sigma^-, adds the global
    constant +w_a/2 and lets one write the same levels as
    w_c(n+1) - d'/2 ± (1/2) sqrt(d'^2 + 4 g^2 (n+1)) with d' = w_c - w_a; the
    splitting, and hence the physics, is identical.)  Returns (E_minus, E_plus)."""
    half_gap = 0.5 * np.sqrt(detuning ** 2 + 4.0 * g ** 2 * (n + 1))
    center = omega_c * (n + 0.5)
    return center - half_gap, center + half_gap


def vacuum_rabi_splitting(g):
    """Vacuum Rabi splitting 2g: the n=0 resonant dressed gap
    E_{0,+} - E_{0,-} = 2 g sqrt(0+1) = 2g.  Even a single quantum -- the
    one-photon manifold over the vacuum -- splits the degenerate |e,0>, |g,1>
    pair, the cavity-QED signature of strong atom-field coupling (S&Z Ch. 6)."""
    return 2.0 * g


def jcm_inversion(times, omega_c, omega_a, g, alpha, N):
    """Atomic inversion <sigma_z>(t) for the atom prepared EXCITED over a coherent
    field, |psi(0)> = |e> (x) |alpha>, evolving under the JCM.  H is diagonalized
    once with eigh and the state is propagated in its (exact, unitary) energy
    eigenbasis.  ON RESONANCE (w_a = w_c) the inversion COLLAPSES on a timescale
    ~sqrt2/g as the n-photon Rabi frequencies 2 g sqrt(n+1) dephase, then partially
    REVIVES near t_r ~ 2 pi sqrt(nbar)/g when they rephase (Scully-Zubairy Ch. 6).
    Returns <sigma_z>(t) for each t (scalar if `times` is scalar)."""
    times = np.atleast_1d(np.asarray(times, dtype=float))
    H = jcm_hamiltonian(omega_c, omega_a, g, N)
    w, V = np.linalg.eigh(H)
    psi0 = np.kron(ket_e, coherent_state(alpha, N))
    Sz = np.kron(sigma_z, np.eye(N, dtype=complex))
    c0 = V.conj().T @ psi0                       # initial amplitudes in eigenbasis
    out = np.empty(times.shape, dtype=float)
    for i, t in enumerate(times):
        psit = V @ (np.exp(-1j * w * t / HBAR) * c0)
        out[i] = np.real(np.vdot(psit, Sz @ psit))
    return out if out.size > 1 else float(out[0])


def resonant_inversion_series(times, g, alpha, N):
    """Closed-form atomic inversion ON RESONANCE for |psi(0)> = |e> (x) |alpha>,

        W(t) = sum_n P_n cos(2 g sqrt(n+1) t),   P_n = |<n|alpha>|^2,

    each Fock component |e,n> Rabi-flopping to |g,n+1> at frequency 2 g sqrt(n+1),
    weighted by the Poissonian photon distribution P_n.  Independent cross-check of
    `jcm_inversion` at w_a = w_c (Scully-Zubairy Ch. 6).  Uses the SAME truncated,
    renormalized |alpha> as the numerical evolution."""
    times = np.atleast_1d(np.asarray(times, dtype=float))
    Pn = np.abs(coherent_state(alpha, N)) ** 2
    freqs = 2.0 * g * np.sqrt(np.arange(N) + 1)
    W = (Pn[None, :] * np.cos(np.outer(times, freqs))).sum(axis=1)
    return W if W.size > 1 else float(W[0])


def collapse_time(g):
    """Gaussian collapse time of the inversion envelope, t_c ~ sqrt(2)/g, set by
    the spread of the n-photon Rabi frequencies over the Poisson width of |alpha>;
    to leading order it is INDEPENDENT of the mean photon number nbar
    (Scully-Zubairy Ch. 6)."""
    return np.sqrt(2.0) / g


def revival_time(g, nbar):
    """First revival time t_r ~ 2 pi sqrt(nbar)/g, when adjacent n-photon Rabi
    frequencies 2 g sqrt(n+1) rephase (their spacing ~ g/sqrt(nbar) times t_r
    equals 2 pi).  Revivals recur at integer multiples k t_r (S&Z Ch. 6)."""
    return 2.0 * np.pi * np.sqrt(nbar) / g


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QO-02  Atom-field interaction: Rabi & Jaynes-Cummings  (hbar = %.3g)" % HBAR)
    print("=" * 70)

    # 1. two-level algebra (~QM-11)
    print("\n1) Two-level atom (~QM-11):  sigma^+ |g> = |e| ?",
          np.allclose(sigma_plus @ ket_g, ket_e),
          "  [sigma^+,sigma^-] = sigma_z ?",
          np.allclose(sigma_plus @ sigma_minus - sigma_minus @ sigma_plus, sigma_z))

    # 2. semiclassical Rabi: resonant return and detuned saturation
    Om = 1.0
    print("\n2) Semiclassical Rabi, RESONANT (Om=1, d=0):  P_e = sin^2(Om t/2)")
    for t in (0.0, np.pi / 2, np.pi, 2 * np.pi):
        print("     Om t = %5.3f :  P_e = %.4f" % (Om * t, rabi_excited_population(t, Om, 0.0)))
    print("     -> full inversion at Om t = pi, RETURN to 0 at Om t = 2 pi")
    d = 1.5
    print("   detuned (Om=1, d=1.5):  Om_R = sqrt(Om^2+d^2) = %.4f ;"
          "  max P_e = Om^2/Om_R^2 = %.4f"
          % (generalized_rabi(Om, d), Om ** 2 / generalized_rabi(Om, d) ** 2))

    # 3. Jaynes-Cummings dressed states and the vacuum Rabi splitting 2g
    g = 1.0
    print("\n3) Jaynes-Cummings dressed states (resonant w_c=w_a=5, g=1):")
    for n in range(3):
        Em, Ep = dressed_energies(n, 0.0, g, 5.0)
        print("     n=%d:  E_- = %7.4f  E_+ = %7.4f   gap = %.4f = 2 g sqrt(n+1)"
              % (n, Em, Ep, Ep - Em))
    print("   VACUUM RABI SPLITTING (n=0):  2g = %.4f" % vacuum_rabi_splitting(g))

    # 4. collapse and revival of the inversion over a coherent field
    alpha = 4.0
    nbar = abs(alpha) ** 2
    N = 60
    tc, tr = collapse_time(g), revival_time(g, nbar)
    print("\n4) Collapse & revival,  |e> (x) |alpha=%.0f>  (nbar=%.0f, g=1):" % (alpha, nbar))
    print("     collapse time  t_c ~ sqrt2/g       = %.3f" % tc)
    print("     revival  time  t_r ~ 2 pi sqrt(nbar)/g = %.3f" % tr)
    samples = [0.0, tr / 2.0, tr]
    Wnum = jcm_inversion(samples, 5.0, 5.0, g, alpha, N)
    labels = ["t=0 (excited)", "t=t_r/2 (collapsed)", "t=t_r (revived)"]
    for lab, t, W in zip(labels, samples, np.atleast_1d(Wnum)):
        print("     %-20s t=%6.3f :  <sigma_z> = %+.4f" % (lab, t, W))
    Wser = resonant_inversion_series(samples, g, alpha, N)
    print("     numeric vs sum_n P_n cos(2g sqrt(n+1) t): max diff = %.2e"
          % np.max(np.abs(np.atleast_1d(Wnum) - np.atleast_1d(Wser))))


if __name__ == "__main__":
    _demo()
