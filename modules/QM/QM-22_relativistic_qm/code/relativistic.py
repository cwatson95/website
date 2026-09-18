"""
QM-22  Relativistic quantum mechanics -- the Klein-Gordon and Dirac equations,
built and *verified* as explicit matrix / operator identities.

Part of the physics topic network (see modules/topic_network.txt, module QM-22).
This is where QM is made compatible with special relativity.  Its home module for
the energy-momentum relation, ~RE-06 (relativistic dynamics, 4-momentum, E=mc^2),
was skipped in the RE trunk (it waits on ~CM-06), so the relation E^2 = p^2 c^2 +
m^2 c^4 is stated inline here.  Forward links: ~QF-01 (second quantization, which
reinterprets the negative-energy solutions as antiparticles and cures the
probability problem), ~QM-11 (spin -- which here EMERGES from the Dirac equation),
~QM-17 (fine structure = the non-relativistic expansion of the Dirac equation),
and ~MA-18 (the Clifford / gamma-matrix algebra; cross-checked in the tests).

UNITS: natural units  hbar = c = 1  (documented; HBAR, C below).  In these units
energy, momentum and mass share one unit and the energy-momentum relation reads
E^2 = p^2 + m^2.  Restore SI by reinserting hbar and c (noted at each formula).

METRIC: g = diag(+1, -1, -1, -1)  ("mostly minus" / West-coast).  A 4-vector is
a^mu = (a^0, a^1, a^2, a^3) = (a^0, vec a); its covariant form is
a_mu = g_{mu nu} a^nu = (a^0, -vec a); and a.b = a_mu b^mu = a^0 b^0 - vec a . vec b.
On-shell 4-momentum p^mu = (E, vec p) obeys p.p = E^2 - |vec p|^2 = m^2.

The story, each a function group below:
  0. Conventions     -- metric, Minkowski dot, the Pauli matrices (built locally).
  1. Gamma matrices  -- Dirac (standard) representation, 4x4 from Pauli blocks;
                        the Clifford algebra {gamma^mu, gamma^nu} = 2 g^{mu nu} I_4.
  2. Klein-Gordon    -- quantize E^2 = p^2 + m^2: (box + m^2) phi = 0; a plane wave
                        solves it IFF E^2 = p^2 + m^2 (both signs -> negative energy).
  3. Dirac           -- (i gamma^mu d_mu - m) psi = 0; p-slash, det = (p^2-m^2)^2,
                        the factorization (p-slash - m)(p-slash + m) = (p^2-m^2) I
                        ["Dirac^2 = Klein-Gordon"], and the 4 plane-wave spinors.
  4. Non-rel. limit  -- the block reduction -> Pauli equation with g = 2 and the
                        leading energy E ~ m + p^2/2m.

numpy supplies the linear algebra.  Every claim is checked numerically against a
closed form in test_relativistic.py (the verification is the code -- Griffiths is
non-relativistic and barely mentions these equations; see ../refs.md).
"""

import numpy as np

__all__ = [
    "HBAR", "C", "I2", "I4",
    # conventions
    "metric", "metric_vector", "minkowski_dot", "lower_index", "pauli",
    "commutator", "anticommutator", "dagger", "sigma_dot",
    # gamma matrices
    "dirac_gamma", "gamma5", "clifford",
    # Klein-Gordon
    "kg_energy", "plane_wave", "box_fd", "kg_operator_fd", "kg_eigenvalue",
    # Dirac
    "four_momentum", "p_slash", "dirac_matrix", "dirac_determinant",
    "dirac_squared", "u_spinor", "v_spinor", "dirac_solutions",
    # non-relativistic limit
    "nonrel_energy", "energy_expansion",
    "ladder_operators", "kinetic_momentum_operators",
    "sigma_dot_pi_squared", "dirac_g_factor",
]

HBAR = 1.0   # natural units; restore SI with hbar = 1.054571817e-34 J s
C = 1.0      # natural units; restore SI with c   = 2.99792458e8   m/s

I2 = np.eye(2, dtype=complex)
I4 = np.eye(4, dtype=complex)


# --- 0. conventions ----------------------------------------------------------

def metric():
    """The Minkowski metric tensor g_{mu nu} = diag(+1, -1, -1, -1) as a 4x4 array
    (mostly-minus signature).  g^{mu nu} has the same entries (g is its own
    inverse: g g = I_4), so raising and lowering an index is the same operation."""
    return np.diag([1.0, -1.0, -1.0, -1.0])


def metric_vector():
    """The diagonal of g as a length-4 array (1, -1, -1, -1) -- convenient for
    lowering an index componentwise."""
    return np.array([1.0, -1.0, -1.0, -1.0])


def minkowski_dot(a, b):
    """The Lorentz-invariant scalar product  a.b = a_mu b^mu = a^0 b^0 - vec a . vec b
    for two contravariant 4-vectors a^mu, b^mu.  For p^mu = (E, vec p) this gives
    p.p = E^2 - |vec p|^2, which equals m^2 on shell."""
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


def lower_index(p_up):
    """Lower a contravariant 4-vector index: p_mu = g_{mu nu} p^nu = (E, -vec p)."""
    p_up = np.asarray(p_up, dtype=complex)
    return metric_vector() * p_up


def pauli(i):
    """The Pauli matrix sigma_i (i = 1, 2, 3); pauli(0) returns the 2x2 identity.
    Built locally (numpy) so this module is self-contained; the tests cross-check
    pauli(1..3) against ~MA-18's group-theory pauli().  They obey sigma_i^2 = I,
    {sigma_i, sigma_j} = 2 delta_ij I and [sigma_i, sigma_j] = 2 i eps_ijk sigma_k
    -- the spin-1/2 (su(2)) algebra that the Dirac gammas are assembled from."""
    if i == 0:
        return I2.copy()
    if i == 1:
        return np.array([[0, 1], [1, 0]], dtype=complex)
    if i == 2:
        return np.array([[0, -1j], [1j, 0]], dtype=complex)
    if i == 3:
        return np.array([[1, 0], [0, -1]], dtype=complex)
    raise ValueError("Pauli index must be 0, 1, 2 or 3")


def commutator(A, B):
    """[A, B] = A B - B A."""
    return A @ B - B @ A


def anticommutator(A, B):
    """{A, B} = A B + B A  (the bracket that defines the Clifford algebra)."""
    return A @ B + B @ A


def dagger(A):
    """Hermitian conjugate (adjoint)  A^dagger = conj(A)^T."""
    return np.asarray(A, dtype=complex).conj().T


def sigma_dot(v3):
    """The 2x2 matrix  sigma . v = sigma_x v_x + sigma_y v_y + sigma_z v_z  for a
    3-vector v.  Key identity (verified in the tests):
        (sigma.a)(sigma.b) = (a.b) I + i sigma.(a x b).
    With a = b = vec pi (the kinetic momentum) the cross term produces the spin
    magnetic moment with g = 2 -- see sigma_dot_pi_squared / dirac_g_factor."""
    v3 = np.asarray(v3, dtype=complex)
    return v3[0] * pauli(1) + v3[1] * pauli(2) + v3[2] * pauli(3)


# --- 1. gamma matrices (Dirac / standard representation) ---------------------

def dirac_gamma(mu):
    """The Dirac gamma matrix gamma^mu (mu = 0,1,2,3), 4x4, in the Dirac/standard
    representation built from 2x2 Pauli blocks:

        gamma^0 = [[ I, 0 ], [ 0, -I ]],     gamma^i = [[ 0, sigma_i ],
                                                        [ -sigma_i, 0 ]].

    They satisfy the Clifford algebra {gamma^mu, gamma^nu} = 2 g^{mu nu} I_4, so
    gamma^0 squares to +I and each gamma^i squares to -I.  (gamma^0)^dagger =
    gamma^0 (Hermitian); (gamma^i)^dagger = -gamma^i (anti-Hermitian); and in
    general gamma^{mu dagger} = gamma^0 gamma^mu gamma^0."""
    Z = np.zeros((2, 2), dtype=complex)
    if mu == 0:
        return np.block([[I2, Z], [Z, -I2]])
    if mu in (1, 2, 3):
        s = pauli(mu)
        return np.block([[Z, s], [-s, Z]])
    raise ValueError("gamma index must be 0, 1, 2 or 3")


def gamma5():
    """The chirality matrix  gamma^5 = i gamma^0 gamma^1 gamma^2 gamma^3.  In the
    Dirac representation gamma^5 = [[0, I], [I, 0]].  It obeys (gamma^5)^2 = I_4,
    (gamma^5)^dagger = gamma^5, and {gamma^5, gamma^mu} = 0 for every mu (it
    anticommutes with all four gammas) -- the algebraic root of chirality / the
    left/right projectors (1 +- gamma^5)/2 used in ~QF-01."""
    return 1j * dirac_gamma(0) @ dirac_gamma(1) @ dirac_gamma(2) @ dirac_gamma(3)


def clifford(mu, nu):
    """The Clifford anticommutator  {gamma^mu, gamma^nu}.  Should equal
    2 g^{mu nu} I_4 for every (mu, nu) -- diagonal (2I_4 for 00, -2I_4 for 11/22/33)
    and zero off-diagonal.  Verified for all 16 pairs in the tests."""
    return anticommutator(dirac_gamma(mu), dirac_gamma(nu))


# --- 2. Klein-Gordon equation ------------------------------------------------

def kg_energy(p3, m, sign=+1):
    """On-shell energy from the relativistic energy-momentum relation
    E^2 = p^2 + m^2  (= p^2 c^2 + m^2 c^4 in SI):  E = sign * sqrt(|p|^2 + m^2).
    BOTH signs solve the Klein-Gordon equation -- sign = -1 is the notorious
    negative-energy root that motivates field theory (~QF-01)."""
    p3 = np.asarray(p3, dtype=float)
    return sign * np.sqrt(float(p3 @ p3) + m * m)


def plane_wave(p4, x4):
    """The scalar plane wave  phi(x) = exp(-i p.x) = exp(-i (E t - vec p . vec x)),
    p.x being the Minkowski product.  Substituting it into (box + m^2) phi = 0 is
    the dispersion test below."""
    p4 = np.asarray(p4, dtype=complex)
    x4 = np.asarray(x4, dtype=complex)
    return np.exp(-1j * minkowski_dot(p4, x4))


def box_fd(field, x4, h=1e-3):
    """Apply the d'Alembertian  box = d_mu d^mu = d_t^2 - nabla^2  to a scalar
    field(x4) at the spacetime point x4, by central second finite differences in
    each of t, x, y, z (mu=0 enters with +, the three spatial mu with -, exactly
    the metric signature).  A genuine numerical operator -- the KG test feeds it a
    plane wave and checks the result against the closed-form eigenvalue."""
    x4 = np.asarray(x4, dtype=float)
    total = 0.0 + 0.0j
    f0 = field(x4)
    for mu in range(4):
        step = np.zeros(4)
        step[mu] = h
        second = (field(x4 + step) - 2.0 * f0 + field(x4 - step)) / h**2
        total += (1.0 if mu == 0 else -1.0) * second
    return total


def kg_eigenvalue(p4, m):
    """Closed form for (box + m^2) acting on exp(-i p.x):  since box phi = -p.p phi,
        (box + m^2) phi = -(p.p - m^2) phi = -(E^2 - |vec p|^2 - m^2) phi.
    Returns the scalar -(p.p - m^2); it vanishes exactly on shell (p.p = m^2)."""
    p4 = np.asarray(p4, dtype=complex)
    return -(minkowski_dot(p4, p4) - m * m)


def kg_operator_fd(p4, m, x4, h=1e-3):
    """(box + m^2) phi  for the plane wave phi = exp(-i p.x), evaluated numerically
    at x4.  Equals kg_eigenvalue(p4, m) * phi(x4) (checked off-shell) and vanishes
    when p4 is on shell (checked for both energy signs)."""
    val = box_fd(lambda y: plane_wave(p4, y), x4, h)
    return val + m * m * plane_wave(p4, x4)


# --- 3. Dirac equation -------------------------------------------------------

def four_momentum(p3, m, sign=+1):
    """Assemble the on-shell 4-momentum p^mu = (E, vec p) with E = sign*sqrt(p^2+m^2)."""
    p3 = np.asarray(p3, dtype=float)
    return np.array([kg_energy(p3, m, sign), p3[0], p3[1], p3[2]], dtype=complex)


def p_slash(p4):
    """Feynman slash  p-slash = gamma^mu p_mu = gamma^0 E - vec gamma . vec p  (the
    index on p is lowered).  In the Dirac representation
        p-slash = [[ E I, -sigma.p ], [ sigma.p, -E I ]].
    Its square is p-slash^2 = (p.p) I_4 (a direct consequence of the Clifford
    algebra), which is what lets the Dirac operator 'square-root' Klein-Gordon."""
    p4 = np.asarray(p4, dtype=complex)
    p_low = lower_index(p4)
    return sum(dirac_gamma(mu) * p_low[mu] for mu in range(4))


def dirac_matrix(p4, m):
    """The momentum-space Dirac operator  (p-slash - m I_4).  A plane-wave spinor
    psi = u(p) e^{-i p.x} solves (i gamma^mu d_mu - m) psi = 0  iff  (p-slash - m) u = 0."""
    return p_slash(p4) - m * I4


def dirac_determinant(p4, m):
    """det(p-slash - m I_4).  The closed form is (p.p - m^2)^2: the operator is
    singular -- and hence has nontrivial spinor solutions -- exactly on shell
    (p.p = m^2, i.e. E^2 = |vec p|^2 + m^2).  Returns the numpy determinant; the
    test compares it to (p.p - m^2)^2."""
    return np.linalg.det(dirac_matrix(p4, m))


def dirac_squared(p4, m):
    """The product (p-slash - m)(p-slash + m).  Using p-slash^2 = (p.p) I this is
    (p.p - m^2) I_4 -- the Klein-Gordon operator.  This is the precise sense in
    which 'Dirac^2 = Klein-Gordon': every solution of the (first-order) Dirac
    equation automatically solves the (second-order) Klein-Gordon equation."""
    ps = p_slash(p4)
    return (ps - m * I4) @ (ps + m * I4)


def u_spinor(p3, m, s):
    """Positive-energy plane-wave spinor u^(s)(p), s = 0 (spin up) or 1 (down),
    with E = +sqrt(p^2+m^2).  Dirac-rep construction (normalization N = sqrt(E+m)):
        u = N [ xi ; (sigma.p / (E+m)) xi ],   xi = (1,0) or (0,1).
    Solves (p-slash - m) u = 0 and is normalized to u^dagger u = 2E, u-bar u = 2m."""
    p3 = np.asarray(p3, dtype=float)
    E = kg_energy(p3, m, +1)
    xi = np.array([1, 0], dtype=complex) if s == 0 else np.array([0, 1], dtype=complex)
    N = np.sqrt(E + m)
    lower = (sigma_dot(p3) @ xi) / (E + m)
    return N * np.concatenate([xi, lower])


def v_spinor(p3, m, s):
    """Negative-energy / antiparticle plane-wave spinor v^(s)(p), s = 0 or 1.  The
    full solution is psi = v(p) e^{+i p.x} (positive frequency reversed), and v
    solves (p-slash + m) v = 0.  Dirac-rep construction:
        v = N [ (sigma.p / (E+m)) chi ; chi ],   N = sqrt(E+m),  chi = (1,0) or (0,1).
    Normalized to v^dagger v = 2E, v-bar v = -2m (the minus sign is the hallmark of
    the antiparticle sector)."""
    p3 = np.asarray(p3, dtype=float)
    E = kg_energy(p3, m, +1)
    chi = np.array([1, 0], dtype=complex) if s == 0 else np.array([0, 1], dtype=complex)
    N = np.sqrt(E + m)
    upper = (sigma_dot(p3) @ chi) / (E + m)
    return N * np.concatenate([upper, chi])


def dirac_solutions(p3, m):
    """The 4 independent plane-wave spinors for momentum vec p:
    (u0, u1) two positive-energy [solve (p-slash - m)u = 0] and (v0, v1) two
    negative-energy/antiparticle [solve (p-slash + m)v = 0].  Returned as a dict."""
    return {"u0": u_spinor(p3, m, 0), "u1": u_spinor(p3, m, 1),
            "v0": v_spinor(p3, m, 0), "v1": v_spinor(p3, m, 1)}


# --- 4. non-relativistic limit: Pauli equation, g = 2 ------------------------

def nonrel_energy(p3, m):
    """Kinetic energy above the rest mass, E - m = sqrt(p^2+m^2) - m.  For |p|<<m
    this -> p^2/2m, the Schroedinger kinetic energy; the next term -p^4/8m^3 is the
    leading relativistic correction that opens hydrogen's fine structure (~QM-17)."""
    return kg_energy(p3, m, +1) - m


def energy_expansion(p3, m, order=2):
    """Low-momentum expansion of E = sqrt(p^2+m^2):
        E = m + p^2/2m - p^4/8m^3 + ...   (order counts terms past the rest mass m).
    order=0 -> m;  order=1 -> m + p^2/2m;  order=2 -> m + p^2/2m - p^4/8m^3."""
    p3 = np.asarray(p3, dtype=float)
    p2 = float(p3 @ p3)
    terms = [m]
    if order >= 1:
        terms.append(p2 / (2.0 * m))
    if order >= 2:
        terms.append(-(p2**2) / (8.0 * m**3))
    return float(sum(terms))


def ladder_operators(N):
    """Truncated harmonic-oscillator annihilation/creation operators a, a^dagger on
    an N-level basis:  a|n> = sqrt(n)|n-1>.  [a, a^dagger] = I on the interior, with
    the usual truncation artifact in the top level (cf. ~QM-05).  Used to realize
    kinetic-momentum operators with the magnetic commutator [pi_x, pi_y] = i q B."""
    a = np.diag(np.sqrt(np.arange(1, N, dtype=float)), 1).astype(complex)
    return a, dagger(a)


def kinetic_momentum_operators(N, q, B):
    """Kinetic momentum vec pi = vec p - q vec A for a uniform field B = B z-hat,
    represented on an N-level basis so that the gauge-invariant magnetic commutator
        [pi_x, pi_y] = i q B   (and pi_z = 0)
    holds exactly on the interior.  This commutator is the entire physical input;
    everything about g = 2 follows from it via the (sigma.pi)^2 identity below."""
    a, ad = ladder_operators(N)
    s = np.sqrt(q * B / 2.0)
    pix = s * (a + ad)
    piy = -1j * s * (a - ad)
    piz = np.zeros((N, N), dtype=complex)
    return pix, piy, piz


def sigma_dot_pi_squared(N, q, B):
    """(sigma . vec pi)^2 on (spin) x (orbital), with vec pi from
    kinetic_momentum_operators.  By the identity (sigma.a)(sigma.b) = a.b + i
    sigma.(a x b) with a = b = vec pi,
        (sigma.pi)^2 = pi^2 I + i sigma.(pi x pi) = pi^2 I - q sigma.B,
    because (pi x pi)_z = [pi_x, pi_y] = i q B.  The spin term -q sigma.B has TWICE
    the coefficient a g=1 moment would give -- that factor of 2 IS the Dirac g=2."""
    pix, piy, piz = kinetic_momentum_operators(N, q, B)
    sx, sy, sz = pauli(1), pauli(2), pauli(3)
    sdotpi = np.kron(sx, pix) + np.kron(sy, piy) + np.kron(sz, piz)
    return sdotpi @ sdotpi


def dirac_g_factor(N=8, q=1.0, B=0.7, m=1.0):
    """Extract the spin g-factor from the non-relativistic reduction of the Dirac
    equation.  The Pauli Hamiltonian's kinetic term is (sigma.pi)^2/2m; subtract the
    orbital part pi^2/2m and what remains is the spin Zeeman term

        H_spin = (1/2m)[(sigma.pi)^2 - pi^2 I] = -(q B / 2m) sigma_z
               = -(q/2m) g S_z B    with   S_z = sigma_z/2   ==>   g = 2.

    Returns (g, residual): g read off a representative interior matrix element, and
    residual = max|(sigma.pi)^2 - pi^2 I - (-q B sigma_z)| over the interior block
    (the last orbital level is dropped -- that is where [pi_x,pi_y] picks up the
    oscillator truncation artifact)."""
    pix, piy, piz = kinetic_momentum_operators(N, q, B)
    D = sigma_dot_pi_squared(N, q, B)
    pi2 = pix @ pix + piy @ piy + piz @ piz
    O = np.kron(I2, pi2)                       # orbital part, spin-blind
    extra = D - O                             # should be -q B sigma_z (x) I
    target = np.kron(-q * B * pauli(3), np.eye(N, dtype=complex))

    # interior = orbital levels 0 .. N-2 in both spin sectors (drop top rung)
    idx = [spin * N + o for spin in (0, 1) for o in range(N - 1)]
    sub = np.ix_(idx, idx)
    residual = np.max(np.abs(extra[sub] - target[sub]))

    # g from the spin term  H_spin = -(q/2m) g S_z B, at interior entry (0,0):
    # spin_term[0,0] = -(q B/2m) * sigma_z[0,0] = -(q B/2m);  S_z[0,0] = +1/2.
    spin_term = extra / (2.0 * m)
    Sz00 = 0.5                                 # (sigma_z/2)[0,0] on orbital level 0
    g = -spin_term[0, 0].real / ((q / (2.0 * m)) * B * Sz00)
    return g, residual


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=3, suppress=True)
    print("QM-22  Relativistic QM -- Klein-Gordon & Dirac (hbar = c = 1)\n")

    print("Gamma matrices (Dirac rep), Clifford algebra {g^mu,g^nu}=2 g^{mu nu} I:")
    for mu in range(4):
        for nu in range(4):
            expect = 2.0 * metric()[mu, nu]
            ok = np.allclose(clifford(mu, nu), expect * I4)
            if mu == nu:
                print(f"  (g^{mu})^2 = {'+' if expect>0 else '-'}I : {ok}", end="   ")
        print()
    print("  {g^5,g^mu}=0 for all mu:",
          all(np.allclose(anticommutator(gamma5(), dirac_gamma(mu)), 0) for mu in range(4)),
          " (g^5)^2=I:", np.allclose(gamma5() @ gamma5(), I4))

    print("\nKlein-Gordon: plane wave exp(-i p.x), m=1, vec p=(0.3,0.4,0):")
    m, p3, x4 = 1.0, [0.3, 0.4, 0.0], [0.11, 0.22, 0.33, 0.44]
    for sign in (+1, -1):
        p4 = four_momentum(p3, m, sign)
        res = kg_operator_fd(p4, m, x4)
        print(f"  E = {p4[0].real:+.4f}:  (box+m^2)phi = {abs(res):.2e}  (-> 0, solves KG)")
    print("  ==> both E = +/- sqrt(p^2+m^2) solve KG: negative-energy solutions.")

    print("\nDirac: det(p-slash - m) = (p.p - m^2)^2, and Dirac^2 = Klein-Gordon:")
    p4 = four_momentum(p3, m, +1)
    print(f"  det(p-slash - m) on shell = {abs(dirac_determinant(p4, m)):.2e}  (-> 0)")
    print("  (p-slash-m)(p-slash+m) = (p.p-m^2)I = 0 on shell:",
          np.allclose(dirac_squared(p4, m), 0))
    sols = dirac_solutions(p3, m)
    ok_u = all(np.allclose(dirac_matrix(p4, m) @ sols[k], 0) for k in ("u0", "u1"))
    ok_v = all(np.allclose((p_slash(p4) + m * I4) @ sols[k], 0) for k in ("v0", "v1"))
    print(f"  u0,u1 solve (p-slash-m)u=0: {ok_u};  v0,v1 solve (p-slash+m)v=0: {ok_v}")
    u0 = sols["u0"]
    print(f"  normalization: u-bar u = {(dagger(u0) @ dirac_gamma(0) @ u0).real:.3f}"
          f"  (= 2m = {2*m}),  u^dag u = {(dagger(u0) @ u0).real:.3f} (= 2E = {2*p4[0].real:.3f})")

    print("\nNon-relativistic limit:")
    print(f"  E - m = {nonrel_energy([0.01,0,0],1.0):.3e}  vs  p^2/2m = {0.01**2/2:.3e}")
    g, resid = dirac_g_factor()
    print(f"  spin g-factor from (sigma.pi)^2 reduction:  g = {g:.6f}"
          f"   (identity residual {resid:.1e})")
    print("  ==> spin and g=2 EMERGE from the Dirac equation (no input by hand).")


if __name__ == "__main__":
    _demo()
