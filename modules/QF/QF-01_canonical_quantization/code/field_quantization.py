"""QF-01  Canonical field quantization -- a free field is infinitely many oscillators.

Physics topic network, module QF-01 (modules/topic_network.txt) -- KEY BRIDGE B6:
    ~CM-15 (classical SHM) -> ~CM-16 (normal modes) -> ~QM-09 (quantum SHO) ->
    QF-01 (a free quantum field = one harmonic oscillator per momentum mode).
Builds on ~QM-22 (the Klein-Gordon / Dirac equations being quantized) and
~QM-09 (the single oscillator and its a, a+ algebra).  ~QM-19 (path integrals)
is the alternative quantization route.

Source: Peskin & Schroeder, *An Introduction to Quantum Field Theory*:
  * Ch. 2, esp. Sect. 2.2 (classical field theory: the canonical momentum
    pi = dL/d(d0 phi) and the equal-time commutator) and Sect. 2.3 (the
    Klein-Gordon field as harmonic oscillators: a_p, a_p+, the Hamiltonian,
    the vacuum/zero-point energy and its ultraviolet divergence);
  * Ch. 3, Sect. 3.5 (quantization of the Dirac field with ANTIcommutators --
    the spin-statistics connection and the Pauli exclusion principle).
Cross-citable: Zee, *QFT in a Nutshell* (Part I); Weinberg, *The Quantum Theory
of Fields, Vol. 1* (Ch. 5).

------------------------------------------------------------------------------
The physics, in one screen
------------------------------------------------------------------------------
A free real scalar field has Lagrangian density (NATURAL UNITS hbar = c = 1)

    L = (1/2)(d_mu phi)(d^mu phi) - (1/2) m^2 phi^2 .

Its canonical momentum is  pi = dL/d(d0 phi) = phi-dot, and quantization promotes
the classical Poisson bracket to the equal-time commutator (cf. ~QM-05, the
[x,p]=i hbar of a single particle, B7)

    [phi(x), pi(y)] = i hbar delta^3(x - y) .

Fourier-expanding the field, every momentum mode p decouples into an independent
harmonic oscillator with frequency given by the Klein-Gordon DISPERSION RELATION

    omega_p = sqrt(p^2 c^2 + m^2 c^4) / hbar   --(hbar=c=1)-->   sqrt(p^2 + m^2),

massless m=0 giving omega_p = |p| (the light cone).  The field is then

    phi(x) = INT d^3p/(2pi)^3 (1/sqrt(2 omega_p)) ( a_p e^{ip.x} + a_p+ e^{-ip.x} ),
    [a_p, a_q+] = (2pi)^3 delta^3(p - q),

the continuum version of the single oscillator's [a, a+] = 1.  The Hamiltonian

    H = INT d^3p/(2pi)^3  omega_p ( a_p+ a_p + (1/2)[a_p, a_p+] )

is a sum of oscillators: mode p carries energy E = (n_p + 1/2) hbar omega_p.
Stacking quanta with a_p+ on the vacuum |0> (a_p|0>=0) builds multi-particle Fock
states -- this is SECOND QUANTIZATION.  The leftover (1/2) per mode sums to the
VACUUM (zero-point) ENERGY  E_0 = (1/2) SUM_p hbar omega_p, which diverges in the
ultraviolet and is regularized here by a momentum cutoff over discrete box modes
(it grows ~ cutoff^4, motivating renormalization, ~QF-04).

Spin-1/2 (Dirac) fields force ANTIcommutators {b, b+} = ... instead (spin-statistics);
b+^2 = 0 is the Pauli exclusion principle (~QM-14).  This file demonstrates that
with a single fermionic mode too.
"""

import numpy as np

__all__ = [
    "kg_dispersion",
    "annihilation", "creation", "number",
    "commutator", "anticommutator",
    "single_mode_spectrum", "mode_energy",
    "field_modes", "vacuum_energy",
    "fermion_annihilation",
]


# =============================================================================
# 1. The Klein-Gordon dispersion relation  (Peskin Sect. 2.3)
# =============================================================================

def kg_dispersion(p, m):
    """Klein-Gordon dispersion  omega_p = sqrt(p^2 + m^2)  (natural units hbar=c=1).

    `p` is the momentum MAGNITUDE |p| (a scalar, or an array of magnitudes); `m`
    is the field mass.  Massless m=0 gives omega_p = |p| (the photon/light cone);
    at p=0 it gives omega = m (the rest energy m c^2).  In SI units this is
    omega_p = sqrt(p^2 c^2 + m^2 c^4)/hbar.  Source: Peskin Eq. (2.25) region."""
    p = np.asarray(p, dtype=float)
    out = np.sqrt(p * p + float(m) ** 2)
    return float(out) if out.ndim == 0 else out


# =============================================================================
# 2. The single mode IS a harmonic oscillator  (B6; ladder ops from ~QM-09)
# =============================================================================
# Each momentum mode of the field is one quantum oscillator.  We realise its
# ladder operators a, a+ as matrices in the truncated number basis {|0>,...,|D-1>},
# exactly as in ~QM-09: a|n> = sqrt(n)|n-1>, a+|n> = sqrt(n+1)|n+1>.  These are
# the field's particle ANNIHILATION / CREATION operators for that mode.

def annihilation(D):
    """Annihilation operator a (D x D, truncated number basis): a|n> = sqrt(n)|n-1>.
    One nonzero superdiagonal sqrt(1), sqrt(2), ..., sqrt(D-1).  In QFT a = a_p
    removes one quantum (particle) from mode p."""
    a = np.zeros((D, D), dtype=complex)
    for n in range(1, D):
        a[n - 1, n] = np.sqrt(n)
    return a


def creation(D):
    """Creation operator a+ = a^dagger (D x D): a+|n> = sqrt(n+1)|n+1>.  Hermitian
    conjugate of `annihilation`; a_p+ adds one particle of momentum p (Peskin
    Sect. 2.3)."""
    return annihilation(D).conj().T


def number(D):
    """Number operator  N = a+ a = diag(0, 1, 2, ..., D-1).  Counts the quanta
    (particles) in the mode; its eigenvalue n_p is the occupation number."""
    return creation(D) @ annihilation(D)


def commutator(A, B):
    """Commutator [A, B] = A B - B A.

    For bosonic ladder operators the exact relation is [a, a+] = 1, but NO finite
    matrices satisfy it (tr[A,B] = 0 always, while tr(I) = D).  Truncation dumps
    the whole defect in one corner: [a, a+] = diag(1, ..., 1, -(D-1)).  The
    interior is the identity -- that is the [a_p, a_q+] = (2pi)^3 delta(p-q) of the
    field, one oscillator at a time."""
    return A @ B - B @ A


def anticommutator(A, B):
    """Anticommutator {A, B} = A B + B A.  The Dirac (spin-1/2) field is quantized
    with these instead of commutators (spin-statistics; Peskin Sect. 3.5)."""
    return A @ B + B @ A


def single_mode_spectrum(D, omega=1.0):
    """Eigenvalues of one mode's Hamiltonian  H = omega (N + 1/2), sorted ascending.
    Returns omega*(n + 1/2) for n = 0..D-1 -- the oscillator spectrum (B6), the
    energy of n quanta in a mode of frequency omega.  GENUINELY diagonalised (a
    cross-check, not read off)."""
    H = omega * (number(D) + 0.5 * np.eye(D))
    return np.sort(np.linalg.eigvalsh(H))


def mode_energy(p, m, n):
    """Energy of n quanta in the field mode of momentum |p| = `p`, mass `m`:

        E = (n + 1/2) hbar omega_p,   omega_p = sqrt(p^2 + m^2).

    n=0 gives the per-mode ZERO-POINT energy (1/2) omega_p; raising n by 1 adds one
    particle of energy omega_p.  Accepts scalars or arrays."""
    w = kg_dispersion(p, m)
    n = np.asarray(n, dtype=float)
    out = (n + 0.5) * w
    return float(out) if np.ndim(out) == 0 else out


# =============================================================================
# 3. The vacuum (zero-point) energy and its ultraviolet divergence
# =============================================================================
# E_0 = (1/2) SUM_p hbar omega_p over the field modes.  In a cubic box of side L
# the momenta are quantized, p = (2 pi / L) n with n in Z^3; we sum the modes with
# |p| <= cutoff.  With the default box L = 2 pi the modes are the integer lattice
# points, so the cutoff is just a radius in units of the mode spacing.  E_0 is
# FINITE for any finite cutoff but GROWS ~ cutoff^4 -- the UV divergence that
# motivates normal-ordering and renormalization (~QF-04).

def field_modes(cutoff, box_L=2.0 * np.pi):
    """Momentum magnitudes |p| of a cubic-box scalar field with |p| <= `cutoff`.

    Momenta are p = (2 pi / L) n, n in Z^3 (box side L = `box_L`); returns the
    sorted array of |p| for every lattice mode inside the cutoff sphere (including
    the zero mode p = 0).  With L = 2 pi the spacing is 1, so the modes are the
    integer-lattice points |n| <= cutoff."""
    dp = 2.0 * np.pi / box_L
    n_max = int(np.floor(cutoff / dp + 1e-9))
    rng = np.arange(-n_max, n_max + 1)
    nx, ny, nz = np.meshgrid(rng, rng, rng, indexing="ij")
    mag = dp * np.sqrt(nx * nx + ny * ny + nz * nz).ravel()
    mag = mag[mag <= cutoff + 1e-9]
    return np.sort(mag)


def vacuum_energy(masses_or_modes, cutoff, mass=0.0, box_L=2.0 * np.pi):
    """Regularized vacuum energy  E_0 = (1/2) SUM_p omega_p  (Peskin Sect. 2.3).

    `masses_or_modes`:
      * a SCALAR -> the mass m of one scalar field; the box modes are generated
        internally (cubic lattice, |p| <= `cutoff`) and E_0 = (1/2) sum sqrt(p^2+m^2).
      * an ARRAY -> an explicit list of mode magnitudes |p|; those with |p| <= cutoff
        are summed as (1/2) sum sqrt(p^2 + mass^2) using the `mass` keyword.

    Finite for any finite cutoff, but grows ~ cutoff^4 (the UV divergence): the
    half-quantum (1/2) hbar omega_p of every mode, summed over the infinitely many
    modes of the field.  Normal-ordering drops it; with boundary conditions its
    cutoff-independent remainder is the Casimir energy (~QF-04)."""
    arr = np.asarray(masses_or_modes, dtype=float)
    if arr.ndim == 0:
        mags = field_modes(cutoff, box_L)
        omega = kg_dispersion(mags, float(arr))
    else:
        mags = arr[arr <= cutoff + 1e-12]
        omega = kg_dispersion(mags, mass)
    return 0.5 * float(np.sum(omega))


# =============================================================================
# 4. Spin-statistics: the Dirac field needs ANTIcommutators
# =============================================================================
# A single fermionic mode lives in a 2-d Fock space {|0>, |1>} (empty / filled):
# the operator b lowers, b+ raises, and {b, b+} = 1, b+^2 = 0 (you cannot put two
# identical fermions in one mode -- the Pauli exclusion principle, ~QM-14).

def fermion_annihilation():
    """Single-mode fermion annihilation operator b (2 x 2): b|1>=|0>, b|0>=0.

    Its conjugate b+ = b.conj().T satisfies the canonical ANTIcommutator
    {b, b+} = 1 and b+^2 = 0 (Pauli exclusion).  This is the spin-1/2 analogue of
    `annihilation`; the Dirac field is built from these (Peskin Sect. 3.5)."""
    return np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("QF-01  Canonical field quantization  (hbar = c = 1)")
    print("=" * 60)

    # 1) Klein-Gordon dispersion: massless vs massive
    p = np.array([0.0, 0.5, 1.0, 2.0, 5.0])
    print("\n1) Klein-Gordon dispersion  omega_p = sqrt(p^2 + m^2)")
    print("   |p|          :", p)
    print("   massless m=0 : omega =", np.round(kg_dispersion(p, 0.0), 4),
          " (= |p|, the light cone)")
    print("   massive  m=1 : omega =", np.round(kg_dispersion(p, 1.0), 4),
          " (omega >= m; -> |p| at large p)")

    # 2) each mode is an oscillator: spectrum (n+1/2) omega  (B6)
    D = 8
    print("\n2) One field mode = one oscillator (~QM-09), spectrum (n+1/2) omega")
    print("   N = a+a diag :", np.round(np.diag(number(D)).real, 3))
    print("   spectrum w=1 :", np.round(single_mode_spectrum(D, omega=1.0), 3),
          " <- E_n = (n+1/2) omega")
    comm = commutator(annihilation(D), creation(D))
    print("   [a,a+] diag  :", np.round(np.diag(comm).real, 3),
          " (interior = 1 = [a_p,a_q+]; corner is truncation)")
    w_massive = kg_dispersion(1.0, 1.0)
    print("   mode |p|=1,m=1: omega=%.4f, E(n=0..2)=" % w_massive,
          np.round([mode_energy(1.0, 1.0, n) for n in range(3)], 4),
          " (E_0 = omega/2 is the zero-point energy)")

    # 3) vacuum energy diverges with the cutoff (UV)  ~ cutoff^4
    print("\n3) Vacuum energy  E_0 = (1/2) SUM_p omega_p  over box modes |p| <= cutoff")
    print("   massless field (m=0):")
    prev = None
    for Lam in (1.0, 2.0, 4.0, 8.0):
        E0 = vacuum_energy(0.0, Lam)
        nmodes = len(field_modes(Lam))
        ratio = "" if prev is None else "   (x %5.1f vs previous)" % (E0 / prev)
        print("     cutoff = %4.1f : %6d modes,  E_0 = %12.3f%s" % (Lam, nmodes, E0, ratio))
        prev = E0
    print("   -> finite for finite cutoff, but grows ~cutoff^4: the UV divergence")
    print("      tamed by normal-ordering / renormalization (~QF-04).")
    print("   massive m=2, cutoff=4: E_0 = %.3f  >  massless %.3f  (mass adds energy)"
          % (vacuum_energy(2.0, 4.0), vacuum_energy(0.0, 4.0)))

    # 4) spin-statistics: a fermion mode anticommutes (Pauli)
    b = fermion_annihilation()
    bd = b.conj().T
    print("\n4) Dirac/spin-1/2: ANTIcommutators (spin-statistics, ~QF-03)")
    print("   {b, b+} =\n", np.round(anticommutator(b, bd).real, 3), " (= identity)")
    print("   b+ b+ =", np.round((bd @ bd).real, 3).tolist(),
          " (= 0: Pauli exclusion -- no two fermions in one mode)")


if __name__ == "__main__":
    _demo()
