"""
QM-17  Fine structure, Zeeman & hyperfine -- the corrections to the hydrogen
spectrum, as closed-form formulae you can evaluate and check against the measured
splittings (the n=2 fine-structure interval, the Lande g-factors, the 21 cm line).

Part of the physics topic network (see modules/topic_network.txt, module QM-17).
This is the showcase application of ~QM-15 (time-independent perturbation theory):
every result here is a first-order shift  E^1 = <psi_0| H' |psi_0>  of the Bohr
levels of ~QM-12 (hydrogen).  The pieces use:
  - ~QM-11 (spin: the electron's S, gyromagnetic factor g_e ~= 2),
  - ~QM-13 (addition of angular momenta: J = L + S forces the good quantum
    numbers n, l, s, j, m_j; F = I + S does the same for hyperfine),
  - ~QM-10 (the L*S operator is built from j(j+1)-l(l+1)-s(s+1)).

The hierarchy (Griffiths 3e Table 7.1, p.378), each a function group below:
  1. The scale          -- the fine-structure constant alpha = e^2/(4 pi eps0 hbar c)
                           ~= 1/137.036.  Fine structure is O(alpha^2) below Bohr.
  2. Fine structure     -- relativistic kinetic correction (Eq.7.58) + spin-orbit
                           coupling (Eq.7.67) + Darwin term (l=0); their sum is the
                           (n,j)-only fine-structure formula (Eq.7.68/7.69), which
                           splits the l-degeneracy but preserves the j-degeneracy.
  3. Zeeman effect      -- a level in an external field B.  Weak field: the Lande
                           g-factor g_J and E = mu_B g_J B m_j (Eq.7.79).  Strong
                           field (Paschen-Back): E = mu_B B (m_l + 2 m_s) (Eq.7.83).
  4. Hyperfine          -- the proton's magnetic moment splits the ground state into
                           triplet/singlet (spin-spin coupling); the gap is the
                           famous 21 cm / 1420 MHz line (Eq.7.94-7.99).

UNITS.  Energies are returned in eV, frequencies in Hz, lengths in m -- the point
of this module is to land on real measured numbers (CODATA / NIST), exactly like
~QM-01.  The two purely-algebraic angular-momentum quantities, <L*S> and <S_p*S_e>,
are returned in units of hbar^2 (their hbar carried by the keyword `hbar`, default
1.0); the Lande g-factor and the L*S bracket are dimensionless quantum-number
formulae.  CODATA-2018 SI constants are used throughout; reference values suffixed
`_ref` are used ONLY to check the rederivations in test_fine_structure.py.

Reference: Griffiths & Schroeter, Introduction to QM, 3rd ed., Chapter 7:
Sec.7.3 Fine Structure (p.378; 7.3.1 relativistic p.380, 7.3.2 spin-orbit p.384),
Sec.7.4 Zeeman (p.389; weak 7.4.1 p.390, strong 7.4.2 p.393),
Sec.7.5 Hyperfine / 21 cm line (p.398).  See ../refs.md for page-verified cites.
"""

import math

__all__ = [
    # constants (CODATA 2018, SI)
    "h", "hbar", "c", "k_B", "e", "m_e", "m_p", "eps0", "mu0",
    "a0", "Ry_eV", "g_e", "g_p",
    # reference values (used only to check the code)
    "alpha_ref", "mu_B_ref", "f_21cm_ref", "lambda_21cm_ref",
    # 1. scale
    "fine_structure_constant", "electron_rest_energy_eV", "rydberg_energy_eV",
    "bohr_energy_eV",
    # 2. fine structure
    "relativistic_correction_eV", "LS_coupling", "spin_orbit_correction_eV",
    "darwin_correction_eV", "fine_structure_correction_eV", "hydrogen_energy_eV",
    # 3. Zeeman
    "lande_g_factor", "bohr_magneton", "bohr_magneton_eV_per_T",
    "zeeman_weak_field_eV", "zeeman_strong_field_eV",
    # 4. hyperfine
    "spin_spin_coupling", "hyperfine_splitting_eV", "hyperfine_frequency",
    "hyperfine_wavelength",
]

# --- physical constants, CODATA 2018 (SI) ------------------------------------
h     = 6.62607015e-34       # Planck constant            [J s]   (exact)
hbar  = 1.054571817e-34      # reduced Planck constant    [J s]
c     = 2.99792458e8         # speed of light             [m/s]   (exact)
k_B   = 1.380649e-23         # Boltzmann constant         [J/K]   (exact)
e     = 1.602176634e-19      # elementary charge          [C]     (exact)
m_e   = 9.1093837015e-31     # electron mass              [kg]
m_p   = 1.67262192369e-27    # proton mass                [kg]
eps0  = 8.8541878128e-12     # vacuum permittivity        [F/m]
mu0   = 1.25663706212e-6     # vacuum permeability        [N/A^2]
a0    = 5.29177210903e-11    # Bohr radius                [m]
Ry_eV = 13.605693122994      # Rydberg energy             [eV]
g_e   = 2.00231930436        # electron spin g-factor (~2; the "extra 2" is Dirac)
g_p   = 5.5856946893         # proton g-factor (composite: 3 quarks, hence != 2)
# reference values (CHECK ONLY -- never used to produce an answer)
alpha_ref       = 7.2973525693e-3     # fine-structure constant (= 1/137.035999...)
mu_B_ref        = 9.2740100783e-24    # Bohr magneton           [J/T]
f_21cm_ref      = 1420.405751768e6    # H ground-state hyperfine freq [Hz]
lambda_21cm_ref = 0.21106114         # ... and its wavelength  [m] (~21 cm)


# --- 1. the scale: the fine-structure constant -------------------------------

def fine_structure_constant():
    """The fine-structure constant  alpha = e^2 / (4 pi eps0 hbar c)  ~= 1/137.036
    (Griffiths 3e Eq.7.44, p.378).  Dimensionless: it is the ratio of the
    electron's Coulomb energy at one Bohr radius to its rest energy scale, and it
    sets the size of every correction in this module -- fine structure is O(alpha^2)
    below the Bohr levels, hyperfine another ~m_e/m_p smaller."""
    return e ** 2 / (4.0 * math.pi * eps0 * hbar * c)


def electron_rest_energy_eV():
    """Electron rest energy  m_e c^2  in eV (~511 keV).  The Bohr energy is
    E_n = -(1/2) alpha^2 (m c^2) / n^2, so Ry = (1/2) alpha^2 m c^2 -- the lever by
    which alpha^2 turns 13.6 eV into the ~1e-4 eV fine structure."""
    return m_e * c ** 2 / e


def rydberg_energy_eV():
    """Rydberg energy  Ry = (1/2) alpha^2 m_e c^2  [eV]  -- REDERIVED from alpha and
    the rest energy (the ~QM-01 house rule: derive, don't quote).  ~13.6057 eV,
    matching CODATA Ry_eV to ~1e-7.  Deriving it from the same alpha and m c^2 used
    by the corrections makes the whole constant set self-consistent, so the
    fine-structure decomposition below is exact to machine precision."""
    return 0.5 * fine_structure_constant() ** 2 * electron_rest_energy_eV()


def bohr_energy_eV(n, Z=1):
    """Unperturbed Bohr level  E_n = -Ry Z^2 / n^2  [eV]  (the ~QM-12 baseline that
    everything here perturbs), with Ry rederived from alpha (rydberg_energy_eV).
    E_1(H) = -13.606 eV."""
    return -rydberg_energy_eV() * Z ** 2 / n ** 2


# --- 2. fine structure -------------------------------------------------------

def relativistic_correction_eV(n, l, Z=1):
    """First-order RELATIVISTIC kinetic-energy correction (Griffiths 3e Eq.7.58,
    p.381).  H'_rel = -p^4/(8 m^3 c^2) is the next term in T = sqrt(p^2c^2+m^2c^4)
    - mc^2; its expectation value in |n l m> is

        E^1_rel = -(E_n^2 / (2 m c^2)) [ 4n/(l+1/2) - 3 ].

    Depends on n and l (not j); always lowers the level.  O(alpha^2) below E_n."""
    En = bohr_energy_eV(n, Z)
    return -(En ** 2 / (2.0 * electron_rest_energy_eV())) * (4.0 * n / (l + 0.5) - 3.0)


def LS_coupling(j, l, s=0.5, hbar=1.0):
    """The spin-orbit operator's eigenvalue

        <L*S> = (hbar^2/2) [ j(j+1) - l(l+1) - s(s+1) ]

    on a state of definite total j (Griffiths 3e Eq.7.65, p.386).  Because L and S
    are not separately conserved, the good states diagonalize J=L+S (~QM-13); then
    2 L*S = J^2 - L^2 - S^2.  Returned in units of hbar^2 (set `hbar` for SI).
    Check: for p (l=1,s=1/2), p_1/2 gives -hbar^2 and p_3/2 gives +hbar^2/2, and
    the (2j+1)-weighted average over the two j's is zero (the center-of-gravity
    rule)."""
    return 0.5 * hbar ** 2 * (j * (j + 1.0) - l * (l + 1.0) - s * (s + 1.0))


def spin_orbit_correction_eV(n, l, j, Z=1):
    """First-order SPIN-ORBIT correction (Griffiths 3e Eq.7.67, p.386):

        E^1_so = (E_n^2 / (m c^2)) * n[j(j+1)-l(l+1)-3/4] / [l(l+1/2)(l+1)].

    The electron's spin moment sits in the magnetic field of the (apparently)
    orbiting proton; the Thomas-precession 1/2 is already included.  Vanishes for
    l=0 (no orbital motion -> no internal field).  Raises j=l+1/2, lowers j=l-1/2;
    same O(alpha^2) size as the relativistic term."""
    if l == 0:
        return 0.0                       # no orbital angular momentum, no coupling
    En = bohr_energy_eV(n, Z)
    num = n * (j * (j + 1.0) - l * (l + 1.0) - 0.75)
    den = l * (l + 0.5) * (l + 1.0)
    return (En ** 2 / electron_rest_energy_eV()) * num / den


def darwin_correction_eV(n, l, Z=1):
    """The DARWIN term, nonzero only for l=0 s-states (the electron's
    'Zitterbewegung' smears the point Coulomb interaction over ~a Compton
    wavelength).  Griffiths does not derive it in Sec.7.3 -- it is a relic of the
    Dirac equation (~QM-22) -- but it is exactly what restores the fine-structure
    formula at l=0, where spin-orbit vanishes:

        E^1_Darwin = 2 n E_n^2 / (m c^2)   (l = 0),     0   (l != 0).

    With it, E_rel + E_so + E_Darwin equals the (n,j)-only formula below for EVERY
    state (verified to machine precision in the tests)."""
    if l != 0:
        return 0.0
    En = bohr_energy_eV(n, Z)
    return 2.0 * n * En ** 2 / electron_rest_energy_eV()


def fine_structure_correction_eV(n, j, Z=1):
    """The complete first-order FINE-STRUCTURE shift, which (remarkably, given the
    different mechanisms) depends only on n and j:

        E^1_fs = -(Ry Z^2/n^2) (Z alpha)^2/n^2 [ n/(j+1/2) - 3/4 ]

    (Griffiths 3e Eq.7.68/7.69, p.386).  At Z=1 this is the headline form
    -(13.6 eV/n^2)(alpha^2/n^2)[n/(j+1/2) - 3/4].  It breaks the l-degeneracy of
    the Bohr spectrum (s,p,d at fixed n,j coincide; different j split) but leaves
    the j-degeneracy intact (Griffiths Fig.7.8, p.387)."""
    alpha = fine_structure_constant()
    En = bohr_energy_eV(n, Z)            # = -Ry Z^2/n^2 (negative)
    return En * ((Z * alpha) ** 2 / n ** 2) * (n / (j + 0.5) - 0.75)


def hydrogen_energy_eV(n, j, Z=1):
    """The hydrogen level including fine structure (Griffiths 3e Eq.7.69, p.386):

        E_nj = -(Ry Z^2/n^2) [ 1 + (Z alpha)^2/n^2 ( n/(j+1/2) - 3/4 ) ].

    = Bohr energy + fine-structure correction.  This is the 'grand result' for the
    gross+fine spectrum of hydrogen."""
    return bohr_energy_eV(n, Z) + fine_structure_correction_eV(n, j, Z)


# --- 3. the Zeeman effect ----------------------------------------------------

def lande_g_factor(j, l, s=0.5):
    """The Lande g-factor (Griffiths 3e Eq.7.78, p.390):

        g_J = 1 + [ j(j+1) + s(s+1) - l(l+1) ] / [ 2 j(j+1) ].

    It interpolates between the orbital value 1 (s=0 -> g=1) and the spin value
    g_e~=2 (l=0 -> g=2) because only the projection of S on the conserved J=L+S
    survives the precession (Fig.7.9).  Examples: 2S_1/2 -> 2, 2P_1/2 -> 2/3,
    2P_3/2 -> 4/3, 2D_5/2 -> 6/5."""
    return 1.0 + (j * (j + 1.0) + s * (s + 1.0) - l * (l + 1.0)) / (2.0 * j * (j + 1.0))


def bohr_magneton():
    """Bohr magneton  mu_B = e hbar / (2 m_e)  [J/T] (~9.274e-24).  The natural
    unit of atomic magnetic moment; sets the Zeeman energy scale mu_B*B."""
    return e * hbar / (2.0 * m_e)


def bohr_magneton_eV_per_T():
    """Bohr magneton in eV/T (~5.788e-5): a 1 tesla field shifts levels by tens of
    micro-eV, comparable to the n=2 fine-structure interval -> the weak/strong
    crossover happens around ~1 T in hydrogen."""
    return bohr_magneton() / e


def zeeman_weak_field_eV(j, l, m_j, B, s=0.5):
    """WEAK-field Zeeman shift (B << internal spin-orbit field; fine structure
    dominates).  The good states are |n l j m_j>; first-order PT gives (Griffiths
    3e Eq.7.79, p.391)

        E^1_Z = mu_B g_J B m_j .

    Each fine-structure level fans into its 2j+1 equally spaced m_j sublevels, with
    spacing set by the Lande g_J -- the anomalous Zeeman effect.  Returns eV."""
    return bohr_magneton_eV_per_T() * lande_g_factor(j, l, s) * B * m_j


def zeeman_strong_field_eV(m_l, m_s, B):
    """STRONG-field (Paschen-Back) Zeeman shift (B >> internal field; the field
    decouples L and S, so m_l and m_s are separately good).  Griffiths 3e Eq.7.83,
    p.393:

        E^1_Z = mu_B B (m_l + 2 m_s)

    (the 2 is the Dirac spin g-factor, as Griffiths writes it; the measured anomaly
    g_e = 2.0023 is a QED effect, ~QM-22).  Returns eV.  Levels with the same
    m_l + 2 m_s coincide -- e.g. (m_l=+1, m_s=-1/2) and (m_l=-1, m_s=+1/2) -- and
    fine structure is then the small perturbation that resolves them."""
    return bohr_magneton_eV_per_T() * B * (m_l + 2.0 * m_s)


# --- 4. hyperfine splitting & the 21 cm line ---------------------------------

def spin_spin_coupling(F, s1=0.5, s2=0.5, hbar=1.0):
    """The spin-spin operator's eigenvalue, the hyperfine analogue of L*S:

        <S1*S2> = (hbar^2/2) [ F(F+1) - s1(s1+1) - s2(s2+1) ],   F = total spin

    (Griffiths 3e Eq.7.96, p.398).  For the H ground state (electron + proton, both
    spin 1/2): the triplet F=1 gives +hbar^2/4, the singlet F=0 gives -3hbar^2/4,
    so the splitting is hbar^2 -- the gap that becomes the 21 cm line.  Returned in
    units of hbar^2 (the F=I+S coupling is ~QM-13 applied to two spins)."""
    return 0.5 * hbar ** 2 * (F * (F + 1.0) - s1 * (s1 + 1.0) - s2 * (s2 + 1.0))


def hyperfine_splitting_eV():
    """Ground-state HYPERFINE energy gap (triplet minus singlet), the spin-spin
    coupling of the electron and proton magnetic moments (Griffiths 3e Eq.7.97,
    p.399):

        Delta E = 4 g_p hbar^4 / (3 m_p m_e^2 c^2 a0^4) .

    ~5.88 micro-eV -- about m_e/m_p (~1/2000) below fine structure, exactly the
    last rung of Table 7.1.  Returns eV."""
    dE_J = 4.0 * g_p * hbar ** 4 / (3.0 * m_p * m_e ** 2 * c ** 2 * a0 ** 4)
    return dE_J / e


def hyperfine_frequency():
    """Frequency of the ground-state hyperfine (spin-flip) photon  f = Delta E / h
    (Griffiths 3e Eq.7.98, p.399).  ~1420 MHz."""
    return hyperfine_splitting_eV() * e / h


def hyperfine_wavelength():
    """Wavelength of the hyperfine line  lambda = c / f  (Griffiths 3e Eq.7.99,
    p.399).  ~0.21 m = 21 cm -- the '21-centimeter line', one of the most pervasive
    radio signals in the universe (it maps neutral hydrogen across the galaxy)."""
    return c / hyperfine_frequency()


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-17  Fine structure, Zeeman & hyperfine -- the hydrogen spectrum, corrected\n")
    alpha = fine_structure_constant()
    print("1. Scale:")
    print("   alpha = %.10f   (1/alpha = %.4f)" % (alpha, 1.0 / alpha))
    print("   electron rest energy  m c^2 = %.1f keV" % (electron_rest_energy_eV() / 1e3))

    print("\n2. Fine structure (= relativistic + spin-orbit [+ Darwin at l=0]):")
    print("   state      E_rel       E_so        E_Dar       sum         E_fs(n,j)")
    for (n, l, j, name) in [(2, 0, 0.5, "2S_1/2"), (2, 1, 0.5, "2P_1/2"),
                            (2, 1, 1.5, "2P_3/2")]:
        er = relativistic_correction_eV(n, l)
        es = spin_orbit_correction_eV(n, l, j)
        ed = darwin_correction_eV(n, l)
        print("   %-7s % .3e  % .3e  % .3e  % .3e  % .3e eV"
              % (name, er, es, ed, er + es + ed, fine_structure_correction_eV(n, j)))
    split = fine_structure_correction_eV(2, 1.5) - fine_structure_correction_eV(2, 0.5)
    print("   n=2 splitting 2P_3/2 - 2P_1/2 = %.3e eV = %.2f GHz"
          % (split, split * e / h / 1e9))
    print("   (l-degeneracy broken, j-degeneracy kept: 2S_1/2 == 2P_1/2)")

    print("\n3. Zeeman effect:")
    print("   mu_B = %.4e J/T = %.4e eV/T" % (bohr_magneton(), bohr_magneton_eV_per_T()))
    for (j, l, name) in [(0.5, 0, "2S_1/2"), (0.5, 1, "2P_1/2"), (1.5, 1, "2P_3/2")]:
        print("   Lande g(%s) = %.4f" % (name, lande_g_factor(j, l)))
    print("   weak  field ground state, B=1 T: dE = +/- %.3e eV"
          % zeeman_weak_field_eV(0.5, 0, +0.5, 1.0))
    print("   strong field (Paschen-Back) m_l=0,m_s=+1/2, B=1 T: dE = %.3e eV"
          % zeeman_strong_field_eV(0, +0.5, 1.0))

    print("\n4. Hyperfine -- the 21 cm line:")
    print("   ground-state gap Delta E = %.4f micro-eV" % (hyperfine_splitting_eV() * 1e6))
    print("   frequency  = %.3f MHz   (measured 1420.406 MHz)"
          % (hyperfine_frequency() / 1e6))
    print("   wavelength = %.2f cm    (the famous 21 cm line)"
          % (hyperfine_wavelength() * 100.0))


if __name__ == "__main__":
    _demo()
