"""
QM-11  Spin & two-level systems -- intrinsic angular momentum with no r x p
realization: the Pauli matrices, the spin-1/2 operators S = (hbar/2) sigma, the
eigenstates of n.S, Larmor precession in a magnetic field, and the driven
two-level (Rabi) flop.

Part of the physics topic network (see modules/topic_network.txt, module QM-11).
Spin is the HALF-INTEGER representation that ~QM-10 (angular momentum) builds from
the algebra alone but cannot give a wavefunction Y_l^m: the same commutators
[S_i,S_j] = i hbar eps_ijk S_k, now with s = 1/2, dim 2.  The 2x2 generators are
the su(2) Pauli matrices of ~MA-18.  Measurement of S_z is the Stern-Gerlach
experiment (~QM-06).  Feeds ~QM-13 (addition of angular momenta) and ~QM-17
(spin-orbit / fine structure).  Classical lineage: bridge B3 (CM-09 -> QM-10/11).

The story, each a function group below:
  1. Pauli matrices    -- sigma_i sigma_j = delta_ij I + i eps_ijk sigma_k, which
                          packs sigma^2=I, {sigma_i,sigma_j}=2 delta_ij I, and
                          [sigma_i,sigma_j]=2 i eps_ijk sigma_k all in one line.
  2. Spin operators    -- S_i = (hbar/2) sigma_i; [S_i,S_j]=i hbar eps_ijk S_k,
                          S^2 = (3/4) hbar^2 I = hbar^2 s(s+1) I with s=1/2.
  3. n.S eigenstates   -- chi_+(theta,phi) = (cos(theta/2), sin(theta/2)e^{i phi}):
                          <n.S> = +hbar/2, and |<up_z|chi>|^2 = cos^2(theta/2).
  4. Larmor precession -- H = -gamma B.S.  For B = B0 z-hat, <S_x>,<S_y> rotate at
                          omega = gamma B0 while <S_z> is constant (the spin cone).
  5. Rabi flop          -- a driven two-level system: P_flip = (Omega^2/Omega_R^2)
                          sin^2(Omega_R t/2), Omega_R = sqrt(Omega^2 + Delta^2).

UNITS: natural units  hbar = 1  by default (set HBAR below).  The hbar factors are
carried symbolically, so S = (hbar/2) sigma, S^2 = (3/4) hbar^2 I, the propagator
exp(-i H t / hbar), and the Larmor frequency omega = gamma B0 all read off
literally; restore SI with HBAR = 1.054571817e-34.

Reference: Griffiths & Schroeter, Introduction to QM, 3rd ed., Sec. 4.4 (Spin,
p.212), 4.4.1 (Spin 1/2 / Pauli matrices, p.214-216), Prob. 4.33 (n.S eigenspinor,
p.218), 4.4.2 (electron in a magnetic field / Larmor, p.219-221), Prob. 4.36
(driven two-level, p.222).  See ../refs.md for page-verified citations.
"""

import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

__all__ = [
    "HBAR",
    # Pauli / identity
    "I2", "sigma_x", "sigma_y", "sigma_z", "sigma", "levi_civita",
    "commutator", "anticommutator",
    # spin-1/2 operators
    "Sx", "Sy", "Sz", "S", "S_squared", "S_VALUE",
    # states, directions, measurement
    "n_hat", "spin_operator_along", "spin_eigenstate", "up_z", "down_z",
    "expectation", "prob_up_z", "born_probabilities",
    # dynamics
    "hamiltonian_field", "larmor_frequency", "propagator", "evolve",
    "spin_expectations", "schrodinger_solve",
    # driven two-level
    "rabi_hamiltonian", "rabi_frequency", "rabi_probability",
    # rotations (su(2) double cover)
    "rotation",
]

HBAR = 1.0   # natural units; restore SI by setting HBAR = 1.054571817e-34
S_VALUE = 0.5  # the spin quantum number s for this module (spin-1/2)

# --- 1. Pauli matrices -------------------------------------------------------

I2 = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
sigma = (sigma_x, sigma_y, sigma_z)   # indexed 0,1,2 <-> x,y,z


def levi_civita(i, j, k):
    """Totally antisymmetric Levi-Civita symbol eps_ijk on indices in {0,1,2}.
    +1 for an even permutation of (0,1,2), -1 for odd, 0 if any index repeats."""
    return (i - j) * (j - k) * (k - i) / 2.0


def commutator(A, B):
    """[A, B] = A B - B A."""
    return A @ B - B @ A


def anticommutator(A, B):
    """{A, B} = A B + B A."""
    return A @ B + B @ A


# --- 2. spin-1/2 operators  S_i = (hbar/2) sigma_i ---------------------------

Sx = 0.5 * HBAR * sigma_x
Sy = 0.5 * HBAR * sigma_y
Sz = 0.5 * HBAR * sigma_z
S = (Sx, Sy, Sz)


def S_squared():
    """The Casimir S^2 = S_x^2 + S_y^2 + S_z^2.  For spin-1/2 it equals
    (3/4) hbar^2 I = hbar^2 s(s+1) I with s = 1/2 (Griffiths 3e Eq. 4.135,
    p.212 -- the same spectrum the ~QM-10 ladder forces, now at half-integer s)."""
    return Sx @ Sx + Sy @ Sy + Sz @ Sz


# --- 3. directions, n.S eigenstates, measurement -----------------------------

def n_hat(theta, phi):
    """Unit vector in spherical coordinates:
    n = (sin theta cos phi, sin theta sin phi, cos theta).  theta is the polar
    angle from +z, phi the azimuth (Griffiths 3e Prob. 4.33, p.218)."""
    return np.array([np.sin(theta) * np.cos(phi),
                     np.sin(theta) * np.sin(phi),
                     np.cos(theta)])


def spin_operator_along(theta, phi):
    """The spin component along n-hat(theta, phi):  n . S = (hbar/2)(n . sigma) =

        (hbar/2) [[ cos t        , sin t e^{-i p} ],
                  [ sin t e^{i p}, -cos t         ]].

    Its eigenvalues are +-hbar/2 for every direction (Griffiths 3e Prob. 4.33)."""
    n = n_hat(theta, phi)
    return 0.5 * HBAR * (n[0] * sigma_x + n[1] * sigma_y + n[2] * sigma_z)


def spin_eigenstate(theta, phi, sign=+1):
    """Eigenspinor of n . S with eigenvalue sign*hbar/2 (Griffiths 3e Prob. 4.33,
    p.218).  For the + state (spin "up" along n-hat):

        chi_+ = ( cos(theta/2),  sin(theta/2) e^{i phi} )^T,

    and chi_- (spin down along n-hat) is the orthogonal partner

        chi_- = ( sin(theta/2),  -cos(theta/2) e^{i phi} )^T.

    Setting theta=phi=0 recovers up_z = (1,0); theta=pi recovers down_z.  These
    are the half-integer analogue of ~QM-10's Y_l^m -- but there is no spatial
    wavefunction, only this 2-spinor (that is what 'intrinsic' means)."""
    c, s = np.cos(theta / 2.0), np.sin(theta / 2.0)
    e = np.exp(1j * phi)
    if sign > 0:
        return np.array([c, s * e], dtype=complex)
    return np.array([s, -c * e], dtype=complex)


up_z = spin_eigenstate(0.0, 0.0, +1)     # (1, 0): spin up along z
down_z = spin_eigenstate(np.pi, 0.0, +1)  # (0, 1) up to phase: spin down along z


def expectation(op, state):
    """Expectation value <state| op |state> for a (normalized) spinor.  Returns a
    real float (the tiny imaginary part of a Hermitian expectation is dropped
    after an assertion that it is negligible)."""
    val = np.vdot(state, op @ state)
    assert abs(val.imag) < 1e-9, "non-real expectation of a Hermitian operator"
    return val.real


def prob_up_z(state):
    """Born-rule probability of measuring S_z = +hbar/2 (spin up along z):
    |<up_z|state>|^2 (Griffiths 3e p.215).  For state = chi_+(theta,phi) this is
    cos^2(theta/2) -- verified in the tests."""
    return abs(np.vdot(up_z, state)) ** 2


def born_probabilities(op, state):
    """Generalized statistical interpretation (~QM-06): the probabilities of the
    outcomes of measuring the observable `op` on `state`, as a dict
    {eigenvalue: probability}.  For op = S_z this is the Stern-Gerlach split into
    2s+1 = 2 beams (Griffiths 3e Example 4.4, p.221)."""
    w, V = np.linalg.eigh(op)
    out = {}
    for k in range(len(w)):
        p = abs(np.vdot(V[:, k], state)) ** 2
        out[round(float(w[k]), 12)] = out.get(round(float(w[k]), 12), 0.0) + p
    return out


# --- 4. dynamics: spin in a magnetic field, Larmor precession ----------------

def hamiltonian_field(gamma, B):
    """Hamiltonian of a spin magnetic moment in a field B (a 3-vector):

        H = -mu . B = -gamma B . S        (Griffiths 3e Eq. 4.158, p.219)

    mu = gamma S is the magnetic dipole moment, gamma the gyromagnetic ratio."""
    B = np.asarray(B, dtype=float)
    return -gamma * (B[0] * Sx + B[1] * Sy + B[2] * Sz)


def larmor_frequency(gamma, B0):
    """Larmor precession frequency omega = gamma B0 (Griffiths 3e p.220).  It is
    the level splitting Delta E = hbar omega = gamma B0 hbar of H = -gamma B0 S_z,
    and is independent of hbar."""
    return gamma * B0


def propagator(H, t):
    """Time-evolution operator U(t) = exp(-i H t / hbar) for a time-independent H
    (Griffiths 3e Eq. 4.162, p.219)."""
    return expm(-1j * H * t / HBAR)


def evolve(H, state, t):
    """Evolve a spinor: |chi(t)> = U(t) |chi(0)> = exp(-i H t / hbar)|chi(0)>."""
    return propagator(H, t) @ state


def spin_expectations(H, state, t):
    """(<S_x>, <S_y>, <S_z>) at time t for a state evolving under H.  Used to
    exhibit Larmor precession: with H = -gamma B0 S_z and an initial spinor tilted
    at angle alpha to z, <S_x> and <S_y> rotate at omega = gamma B0 while <S_z>
    stays put (Griffiths 3e Eq. 4.163-4.167, p.220)."""
    chi = evolve(H, state, t)
    return (expectation(Sx, chi), expectation(Sy, chi), expectation(Sz, chi))


def schrodinger_solve(H, state, t, n=400):
    """Integrate the time-dependent Schrodinger equation
        i hbar d|chi>/dt = H |chi>
    from 0 to t with scipy.solve_ivp (real/imag split), returning |chi(t)>.  An
    independent dynamical check on `evolve` (which uses the matrix exponential)."""
    H = np.asarray(H, dtype=complex)

    def rhs(_t, y):
        chi = y[:2] + 1j * y[2:]
        dchi = (-1j / HBAR) * (H @ chi)
        return np.concatenate([dchi.real, dchi.imag])

    y0 = np.concatenate([np.asarray(state).real, np.asarray(state).imag])
    sol = solve_ivp(rhs, (0.0, t), y0, t_eval=[t], rtol=1e-10, atol=1e-12,
                    max_step=t / n)
    yf = sol.y[:, -1]
    return yf[:2] + 1j * yf[2:]


# --- 5. driven two-level (Rabi) ---------------------------------------------

def rabi_hamiltonian(Omega, Delta):
    """Rotating-frame Hamiltonian of a two-level system driven near resonance:

        H = (hbar/2) (Delta sigma_z + Omega sigma_x)
          = Delta S_z + Omega S_x,

    with Rabi coupling Omega (drive strength) and detuning Delta (drive minus
    transition frequency).  This is the standard rotating-wave form of Griffiths
    3e Prob. 4.36 (electron in an oscillating field, p.222)."""
    return Delta * Sz + Omega * Sx


def rabi_frequency(Omega, Delta):
    """Generalized Rabi frequency  Omega_R = sqrt(Omega^2 + Delta^2): the rate at
    which population oscillates between the two levels when driven off resonance."""
    return np.sqrt(Omega ** 2 + Delta ** 2)


def rabi_probability(t, Omega, Delta):
    """Rabi formula: probability that a system started in the lower level is found
    in the upper level at time t,

        P(t) = (Omega^2 / Omega_R^2) sin^2(Omega_R t / 2),  Omega_R = sqrt(Om^2+De^2).

    On resonance (Delta=0) the amplitude is 1 -- complete inversion every
    t = pi/Omega; off resonance it saturates at Omega^2/Omega_R^2 < 1."""
    OmR = rabi_frequency(Omega, Delta)
    return (Omega ** 2 / OmR ** 2) * np.sin(OmR * t / 2.0) ** 2


# --- rotations: the su(2) double cover ---------------------------------------

def rotation(theta, n=(0.0, 0.0, 1.0)):
    """Spin-1/2 rotation operator by angle theta about axis n-hat:

        R_n(theta) = exp(-i theta (n . sigma) / 2).

    The hallmark of spin-1/2: R(2 pi) = -I (a 360 deg rotation flips the SIGN of
    the spinor), and only R(4 pi) = +I.  This is the 2-to-1 cover SU(2) -> SO(3)
    of ~MA-18 -- a spinor needs 720 deg to return to itself."""
    n = np.asarray(n, dtype=float)
    n = n / np.linalg.norm(n)
    n_dot_sigma = n[0] * sigma_x + n[1] * sigma_y + n[2] * sigma_z
    return expm(-1j * theta * n_dot_sigma / 2.0)


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=4, suppress=True)
    print("QM-11 Spin & two-level systems  (hbar = %.3g)\n" % HBAR)

    print("Pauli algebra  sigma_i sigma_j = delta_ij I + i eps_ijk sigma_k:")
    print("  sigma_x sigma_y =\n", sigma_x @ sigma_y, " (= i sigma_z)")
    print("  [Sx,Sy] = i hbar Sz ?",
          np.allclose(commutator(Sx, Sy), 1j * HBAR * Sz))
    print("  S^2 = 3/4 hbar^2 I ?",
          np.allclose(S_squared(), 0.75 * HBAR ** 2 * I2),
          " (s(s+1)=%.3f)" % (S_VALUE * (S_VALUE + 1)))

    print("\nEigenstate of n.S at theta=60deg, phi=40deg:")
    th, ph = np.deg2rad(60), np.deg2rad(40)
    chi = spin_eigenstate(th, ph)
    print("  chi_+ =", chi)
    print("  <n.S> = %.4f hbar  (expect +0.5)"
          % (expectation(spin_operator_along(th, ph), chi) / HBAR))
    print("  P(up_z) = %.4f   cos^2(theta/2) = %.4f"
          % (prob_up_z(chi), np.cos(th / 2) ** 2))
    print("  <S> / hbar =", np.array([expectation(o, chi) for o in S]) / HBAR,
          " (= n/2)")

    print("\nLarmor precession  H = -gamma B0 S_z,  gamma=2, B0=3  =>  omega=6:")
    gamma, B0, alpha = 2.0, 3.0, np.deg2rad(50)
    H = hamiltonian_field(gamma, [0, 0, B0])
    chi0 = spin_eigenstate(alpha, 0.0)
    for t in (0.0, 0.25, 0.5):
        sx, sy, sz = spin_expectations(H, chi0, t)
        print("  t=%.2f:  <Sx>=%+.4f <Sy>=%+.4f <Sz>=%+.4f" % (t, sx, sy, sz))
    print("  omega = gamma*B0 = %.3f ; <Sz> constant = (hbar/2)cos(alpha) = %.4f"
          % (larmor_frequency(gamma, B0), 0.5 * HBAR * np.cos(alpha)))

    print("\nRabi flop  (resonant Omega=1, Delta=0): full inversion at t=pi")
    for t in (0.0, np.pi / 2, np.pi):
        print("  t=%.3f:  P_up = %.4f" % (t, rabi_probability(t, 1.0, 0.0)))
    print("  detuned (Omega=1, Delta=1): max P = Om^2/Om_R^2 = %.4f"
          % (1.0 / rabi_frequency(1.0, 1.0) ** 2))

    print("\nSpin-1/2 double cover:  R_z(2pi) = -I ?  R_z(4pi) = +I ?")
    print("  ", np.allclose(rotation(2 * np.pi), -I2),
          " ", np.allclose(rotation(4 * np.pi), I2))


if __name__ == "__main__":
    _demo()
