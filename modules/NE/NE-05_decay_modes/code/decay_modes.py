"""NE-05  Radioactive decay modes and their energetics.

Nuclear Science & Engineering trunk, module NE-05 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 5.1-5.4 (printed pp. 97-111).  Pure stdlib; measured masses from
../../data_tables/B1_atomic_masses.csv and measured emission energies from
../../data_tables/D1_decay_radiation.csv (Appendices B and D).

Every decay Q-value is a difference of *atomic* masses, but the electron
bookkeeping differs by mode -- and this is the whole content of the module:

    alpha       Q = M(P) - M(D) - M(4He)          electrons cancel
    beta-minus  Q = M(P) - M(D)                   electrons cancel exactly
    beta-plus   Q = M(P) - M(D) - 2 m_e           TWO electron masses
    EC          Q = M(P) - M(D)                   same form as beta-minus
    IT/gamma    Q = E*                            no change of nuclide

The 2 m_e c^2 = 1.022 MeV penalty on beta-plus is not bookkeeping pedantry: it
means a parent with 0 < Q_EC < 1.022 MeV can *only* decay by electron capture,
which is why light proton-rich nuclides positron-emit and heavy ones capture.

Alpha decay is two-body, so the alpha comes out with a sharp energy set by
momentum conservation, E_alpha = Q A_D/(A_D + 4).  Beta decay is three-body --
the neutrino takes a share -- so the electron emerges with a *spectrum* whose
endpoint is Q.  That distinction is why alpha spectroscopy identifies nuclides
and beta spectroscopy does not (~NE-15).
"""

import csv
import os

__all__ = [
    "M_N_U", "M_H_U", "M_E_U", "U_MEV", "TWO_ME_MEV",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "q_alpha", "alpha_kinetic_energy", "daughter_recoil_energy",
    "q_beta_minus", "q_beta_plus", "q_electron_capture",
    "q_isomeric_transition", "q_neutron_emission", "q_proton_emission",
    "allowed_decay_modes", "dominant_decay_mode",
    "beta_endpoint", "daughter_of",
    "load_decay_radiation", "measured_emissions",
]

M_N_U = 1.0086649156
M_H_U = 1.0078250321
M_E_U = 5.48579909e-4
U_MEV = 931.494043
TWO_ME_MEV = 2.0 * M_E_U * U_MEV        # 1.02200 MeV, the beta-plus penalty

_MASSES = None
_RADIATION = None


def _data_path(name):
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, os.pardir, os.pardir, "data_tables", name))


def load_atomic_masses(path=None):
    """{(Z, A): atomic_mass_u} from the extracted Appendix B.  Cached."""
    global _MASSES
    if _MASSES is not None and path is None:
        return _MASSES
    table = {}
    with open(path or _data_path("B1_atomic_masses.csv"), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[(int(row["Z"]), int(row["A"]))] = float(row["atomic_mass_u"])
    if path is None:
        _MASSES = table
    return table


def atomic_mass(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


def daughter_of(A, Z, mode):
    """(A, Z) of the daughter for a given decay mode."""
    m = mode.lower()
    if m in ("alpha", "a"):
        return A - 4, Z - 2
    if m in ("beta-", "beta_minus", "b-"):
        return A, Z + 1
    if m in ("beta+", "beta_plus", "b+", "ec", "electron_capture"):
        return A, Z - 1
    if m in ("it", "gamma", "isomeric"):
        return A, Z
    if m in ("n", "neutron"):
        return A - 1, Z
    if m in ("p", "proton"):
        return A - 1, Z - 1
    raise ValueError("unknown decay mode %r" % (mode,))


# --- alpha decay  [S&F Eqs. (5.6)-(5.12), printed pp. 103-105] --------------

def q_alpha(A, Z, table=None, excitation=0.0):
    """Q_alpha = [M(P) - M(D) - M(4He)] c^2 in MeV  [Eq. (5.7)].

    The two surplus electrons of the daughter ion and the two the alpha picks up
    cancel, so atomic masses may be used directly; the neglected electron
    binding energies are tens of eV against MeV."""
    Ad, Zd = daughter_of(A, Z, "alpha")
    q = (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table)
         - atomic_mass(4, 2, table)) * U_MEV
    return q - excitation


def alpha_kinetic_energy(A, Z, table=None, excitation=0.0):
    """Kinetic energy of the emitted alpha  [Eq. (5.11)]:

        E_alpha = Q_alpha * M_D / (M_D + M_alpha) ~ Q_alpha * A_D/(A_D + 4).

    Two-body decay from rest gives a single sharp energy -- the reason alpha
    spectra are line spectra."""
    Ad, Zd = daughter_of(A, Z, "alpha")
    q = q_alpha(A, Z, table, excitation)
    MD = atomic_mass(Ad, Zd, table)
    Ma = atomic_mass(4, 2, table)
    return q * MD / (MD + Ma)


def daughter_recoil_energy(A, Z, table=None, excitation=0.0):
    """Recoil energy of the daughter  [Eq. (5.12)]: E_D = Q - E_alpha."""
    return q_alpha(A, Z, table, excitation) - alpha_kinetic_energy(A, Z, table, excitation)


# --- beta decay  [S&F Eqs. (5.13)-(5.23), printed pp. 105-110] -------------

def q_beta_minus(A, Z, table=None, excitation=0.0):
    """Q_beta- = [M(P) - M(D)] c^2  [Eq. (5.14)], D having Z+1.

    The daughter ion has one *surplus* electron, and the emitted beta supplies
    it, so atomic masses cancel exactly with no correction."""
    Ad, Zd = daughter_of(A, Z, "beta-")
    q = (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table)) * U_MEV
    return q - excitation


def q_beta_plus(A, Z, table=None, excitation=0.0):
    """Q_beta+ = [M(P) - M(D)] c^2 - 2 m_e c^2  [Eq. (5.18)], D having Z-1.

    Two electron masses: one for the emitted positron, one for the electron the
    daughter must shed to become neutral.  2 m_e c^2 = 1.022 MeV, so positron
    emission is energetically forbidden unless the atomic mass difference
    exceeds that."""
    Ad, Zd = daughter_of(A, Z, "beta+")
    q = (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table)) * U_MEV
    return q - TWO_ME_MEV - excitation


def q_electron_capture(A, Z, table=None, excitation=0.0):
    """Q_EC = [M(P) - M(D)] c^2  [Eq. (5.22)], D having Z-1.

    Same form as beta-minus: the captured electron was already part of the
    parent atom, so nothing extra is needed.  Electron binding energy (keV in
    heavy atoms) is neglected."""
    Ad, Zd = daughter_of(A, Z, "ec")
    q = (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table)) * U_MEV
    return q - excitation


def beta_endpoint(A, Z, mode="beta-", table=None, excitation=0.0):
    """Maximum beta kinetic energy  [Eq. (5.16)]: (E_beta)_max = Q.

    Beta decay is a three-body process, so the electron shares the energy with
    an antineutrino and emerges with a continuous spectrum from 0 up to Q."""
    if mode.startswith("beta-") or mode in ("b-", "beta_minus"):
        return q_beta_minus(A, Z, table, excitation)
    return q_beta_plus(A, Z, table, excitation)


# --- other modes  [S&F §§5.4.1, 5.4.6-5.4.8] --------------------------------

def q_isomeric_transition(excitation_mev):
    """Gamma decay / isomeric transition: Q is just the excitation energy.

    No nuclide changes; the nucleus drops to a lower state and emits a photon
    (or ejects an orbital electron -- internal conversion, §5.4.8)."""
    if excitation_mev < 0:
        raise ValueError("excitation energy must be non-negative")
    return excitation_mev


def q_neutron_emission(A, Z, table=None):
    """Q_n = [M(P) - M(D) - m_n] c^2, the negative of the neutron separation
    energy.  Positive only for very neutron-rich nuclides -- the delayed-neutron
    precursors that make reactors controllable (~NE-20)."""
    Ad, Zd = daughter_of(A, Z, "n")
    return (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table) - M_N_U) * U_MEV


def q_proton_emission(A, Z, table=None):
    """Q_p = [M(P) - M(D) - M(1H)] c^2, using the neutral-atom substitution."""
    Ad, Zd = daughter_of(A, Z, "p")
    return (atomic_mass(A, Z, table) - atomic_mass(Ad, Zd, table) - M_H_U) * U_MEV


# --- which modes are open ----------------------------------------------------

_MODES = ("alpha", "beta-", "beta+", "ec", "n", "p")


def allowed_decay_modes(A, Z, table=None, tol=0.0):
    """{mode: Q} for every mode with Q > tol and a tabulated daughter.

    Energetics only: a positive Q says a mode is *permitted*, not that it is
    observed.  Alpha decay in particular is suppressed by the Coulomb barrier
    for tens of orders of magnitude when Q is small (~NE-03 P8)."""
    t = load_atomic_masses() if table is None else table
    out = {}
    for mode in _MODES:
        Ad, Zd = daughter_of(A, Z, mode)
        if Ad < 1 or Zd < 0 or Zd > Ad or not has_nuclide(Ad, Zd, t):
            continue
        q = {
            "alpha": q_alpha, "beta-": q_beta_minus, "beta+": q_beta_plus,
            "ec": q_electron_capture, "n": q_neutron_emission, "p": q_proton_emission,
        }[mode](A, Z, t)
        if q > tol:
            out[mode] = q
    return out


def dominant_decay_mode(A, Z, table=None):
    """The open mode with the largest Q, or None if the nuclide is stable
    against all of them.  A crude rule -- real branching depends on barriers and
    selection rules -- but it gets the direction right across the chart."""
    modes = allowed_decay_modes(A, Z, table)
    if not modes:
        return None
    # electron capture and beta-plus compete for the same transition; report the
    # one that is actually accessible
    if "beta+" in modes and "ec" in modes:
        modes.pop("ec" if modes["beta+"] > 0 else "beta+")
    return max(modes.items(), key=lambda kv: kv[1])[0]


# --- measured emissions, from the extracted Appendix D ----------------------

def load_decay_radiation(path=None):
    """[{nuclide, half_life, group, freq_pct, E_avg_keV, E_max_keV, E_keV}, ...]
    from the extracted Appendix D.  Cached."""
    global _RADIATION
    if _RADIATION is not None and path is None:
        return _RADIATION
    rows = []
    with open(path or _data_path("D1_decay_radiation.csv"), newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if path is None:
        _RADIATION = rows
    return rows


def measured_emissions(nuclide, group=None):
    """Appendix D rows for a nuclide, e.g. measured_emissions('60Co', 'gamma_xray')."""
    rows = [r for r in load_decay_radiation() if r["nuclide"] == nuclide]
    if group:
        rows = [r for r in rows if r["group"] == group]
    return rows


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-05  decay modes and their energetics\n")

    print("  alpha decay: two-body, so the alpha energy is sharp")
    print("   parent    Q_alpha    E_alpha    E_recoil   E_a/Q")
    for A, Z, name in [(238, 92, "238U"), (226, 88, "226Ra"), (222, 86, "222Rn"),
                       (210, 84, "210Po"), (241, 95, "241Am")]:
        q = q_alpha(A, Z, t)
        ea = alpha_kinetic_energy(A, Z, t)
        ed = daughter_recoil_energy(A, Z, t)
        print("   %-8s %8.4f  %8.4f  %8.4f   %.4f" % (name, q, ea, ed, ea / q))

    print("\n  the three beta modes for one parent, and their electron corrections")
    for A, Z, name in [(22, 11, "22Na"), (40, 19, "40K"), (64, 29, "64Cu"),
                       (7, 4, "7Be"), (137, 55, "137Cs")]:
        parts = []
        for lab, fn in (("b-", q_beta_minus), ("b+", q_beta_plus), ("EC", q_electron_capture)):
            Ad, Zd = daughter_of(A, Z, {"b-": "beta-", "b+": "beta+", "EC": "ec"}[lab])
            if has_nuclide(Ad, Zd, t):
                parts.append("%s %+7.3f" % (lab, fn(A, Z, t)))
        print("   %-8s %s" % (name, "   ".join(parts)))

    print("\n  EC without beta-plus: when 0 < Q_EC < 1.022 MeV only capture is open")
    for A, Z, name in [(7, 4, "7Be"), (55, 26, "55Fe"), (51, 24, "51Cr"), (125, 53, "125I")]:
        if has_nuclide(A, Z - 1, t):
            print("   %-8s Q_EC = %+7.4f   Q_b+ = %+7.4f   %s"
                  % (name, q_electron_capture(A, Z, t), q_beta_plus(A, Z, t),
                     "EC only" if q_beta_plus(A, Z, t) < 0 < q_electron_capture(A, Z, t)
                     else "both open"))

    print("\n  predicted dominant mode vs Appendix D observation")
    for A, Z, name in [(3, 1, "3H"), (14, 6, "14C"), (60, 27, "60Co"), (137, 55, "137Cs"),
                       (131, 53, "131I"), (238, 92, "238U"), (226, 88, "226Ra")]:
        mode = dominant_decay_mode(A, Z, t)
        groups = sorted({r["group"] for r in measured_emissions(name)})
        print("   %-8s predicted %-6s   Appendix D groups: %s"
              % (name, mode, ", ".join(groups) if groups else "(not tabulated)"))

    print("\n  computed endpoints against Appendix D measured maxima")
    for A, Z, name in [(3, 1, "3H"), (14, 6, "14C"), (32, 15, "32P"), (90, 38, "90Sr")]:
        rows = measured_emissions(name, "beta")
        if rows:
            emax = max(float(r["E_max_keV"]) for r in rows if r["E_max_keV"])
            print("   %-8s Q_beta- = %8.2f keV    Appendix D E_max = %8.2f keV"
                  % (name, q_beta_minus(A, Z, t) * 1000, emax))


if __name__ == "__main__":
    _demo()
