"""NE-15  Radiation detectors: gas-filled, scintillation, semiconductor.

Nuclear Science & Engineering trunk, module NE-15 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 8.1-8.5 (printed pp. 221-259).  Pure stdlib; Tables 8.1 and 8.2 are
transcribed below.

Every detector does the same three things (S&F's chapter opening): absorb the
radiation, turn the absorbed energy into an observable, and measure the
observable.  ~NE-12 and ~NE-14 supplied the first step -- a detector must stop
the particle to see it, and the ranges and mean free paths there set how big and
how dense it has to be.  This module is about the second and third.

The organising quantity is the NUMBER OF INFORMATION CARRIERS produced per
event.  Everything about a detector's energy resolution follows from it, because
the carrier count fluctuates statistically and that fluctuation is irreducible:

    N = E / w          w = energy per carrier (Table 8.2 for semiconductors)
    sigma_N = sqrt(F N)                       F = Fano factor
    FWHM/E = 2.355 sqrt(F/N)

So resolution improves as 1/sqrt(N), and the whole history of detector
development is a race to make w small.  A gas ion chamber spends ~30 eV per ion
pair, NaI(Tl) needs ~100 eV per collected photoelectron, and germanium needs
2.98 eV.  That single ratio -- 2.98 against ~100 -- is why a germanium spectrum
resolves lines a sodium-iodide spectrum smears into one bump, and it is the
reason to put up with liquid nitrogen.
"""

import math

__all__ = [
    "SEMICONDUCTORS", "SCINTILLATORS_INORGANIC", "SCINTILLATORS_ORGANIC",
    "GAS_W_VALUES", "FANO_FACTORS", "ANTHRACENE_RELATIVE_TO_NAI",
    "FWHM_PER_SIGMA",
    "carriers_produced", "carrier_sigma", "intrinsic_resolution_fraction",
    "intrinsic_resolution_percent", "fwhm_energy",
    "gas_multiplication", "townsend_series_terms",
    "scintillator_photoelectrons", "photopeak_resolution_percent",
    "compare_resolution",
]

FWHM_PER_SIGMA = 2.355          # Gaussian FWHM = 2.355 sigma  [S&F §8.6.2]

# S&F Table 8.2 (printed p. 244): Z, density g/cm3, band gap eV, w in eV per
# electron-hole pair.
SEMICONDUCTORS = {
    "Si":     {"Z": 14,       "density": 2.33, "band_gap_eV": 1.12, "w_eV": 3.61},
    "Ge":     {"Z": 32,       "density": 5.33, "band_gap_eV": 0.72, "w_eV": 2.98},
    "GaAs":   {"Z": (31, 33), "density": 5.32, "band_gap_eV": 1.42, "w_eV": 4.2},
    "CdTe":   {"Z": (48, 52), "density": 6.06, "band_gap_eV": 1.52, "w_eV": 4.43},
    "CdZnTe": {"Z": (48, 30, 52), "density": 6.0, "band_gap_eV": 1.60, "w_eV": 5.0},
    "HgI2":   {"Z": (80, 53), "density": 6.4,  "band_gap_eV": 2.13, "w_eV": 4.3},
}

# S&F Table 8.1 (printed p. 238): inorganic scintillators.
# wavelength nm, decay time ns (tuple where multi-component), photons per MeV,
# response relative to NaI(Tl).
SCINTILLATORS_INORGANIC = {
    "NaI(Tl)":   {"nm": 415, "decay_ns": (230,),      "photons_per_MeV": 38000, "rel": 1.00},
    "CsI(Na)":   {"nm": 420, "decay_ns": (680, 3340), "photons_per_MeV": 39000, "rel": 1.10},
    "CsI(Tl)":   {"nm": 540, "decay_ns": (460, 4180), "photons_per_MeV": 65000, "rel": 0.49},
    "LiI(Eu)":   {"nm": 470, "decay_ns": (1400,),     "photons_per_MeV": 11000, "rel": 0.23},
    "BGO":       {"nm": 480, "decay_ns": (300,),      "photons_per_MeV": 8200,  "rel": 0.13},
    "CaF2(Eu)":  {"nm": 435, "decay_ns": (900,),      "photons_per_MeV": 24000, "rel": 0.50},
    "GSO(Ce)":   {"nm": 440, "decay_ns": (56, 400),   "photons_per_MeV": 9000,  "rel": 0.20},
    "YAP(Ce)":   {"nm": 370, "decay_ns": (27,),       "photons_per_MeV": 18000, "rel": 0.45},
    "YAG(Ce)":   {"nm": 550, "decay_ns": (88, 302),   "photons_per_MeV": 17000, "rel": 0.50},
    "LSO(Ce)":   {"nm": 420, "decay_ns": (47,),       "photons_per_MeV": 25000, "rel": 0.75},
    "LaCl3(Ce)": {"nm": 350, "decay_ns": (28,),       "photons_per_MeV": 49000, "rel": 0.80},
    "LaBr3(Ce)": {"nm": 380, "decay_ns": (16,),       "photons_per_MeV": 63000, "rel": 1.30},
}

# S&F Table 8.1, organic: light yield as a PERCENTAGE of anthracene.
SCINTILLATORS_ORGANIC = {
    "Anthracene":   {"nm": 447, "decay_ns": 30.0,  "rel_anthracene_pct": 100, "form": "crystal"},
    "Stilbene":     {"nm": 410, "decay_ns": 4.5,   "rel_anthracene_pct": 50,  "form": "crystal"},
    "BC-400":       {"nm": 423, "decay_ns": 2.4,   "rel_anthracene_pct": 65,  "form": "plastic"},
    "EJ-204":       {"nm": 408, "decay_ns": 1.8,   "rel_anthracene_pct": 68,  "form": "plastic"},
    "EJ-232":       {"nm": 370, "decay_ns": 1.4,   "rel_anthracene_pct": 55,  "form": "plastic"},
    "EJ-240":       {"nm": 435, "decay_ns": 285.0, "rel_anthracene_pct": 41,  "form": "plastic"},
    "EJ-252":       {"nm": 423, "decay_ns": 2.4,   "rel_anthracene_pct": 46,  "form": "plastic"},
    "EJ-301":       {"nm": 425, "decay_ns": 3.2,   "rel_anthracene_pct": 78,  "form": "liquid"},
    "EJ-305":       {"nm": 425, "decay_ns": 2.7,   "rel_anthracene_pct": 80,  "form": "liquid"},
    "EJ-331":       {"nm": 424, "decay_ns": 3.6,   "rel_anthracene_pct": 68,  "form": "liquid"},
    "EJ-339":       {"nm": 425, "decay_ns": 3.7,   "rel_anthracene_pct": 65,  "form": "liquid"},
}

# S&F Table 8.1 footnote: NaI(Tl)'s light yield is 2.3x anthracene's.
ANTHRACENE_RELATIVE_TO_NAI = 1.0 / 2.3

# Gas W-values, eV per ion pair.  BEYOND S&F -- §8.1 describes ion-pair creation
# but tabulates no W-values, and resolution cannot be computed without them.
# Standard values (ICRU Report 31); see refs.md.
GAS_W_VALUES = {"air": 33.97, "Ar": 26.4, "He": 41.3, "Xe": 21.9,
                "CH4": 27.3, "P10": 26.0}

# Fano factors.  ALSO BEYOND S&F, which does not mention the Fano factor at all
# -- but carrier statistics are sub-Poisson and using sqrt(N) instead of
# sqrt(F N) overestimates the width of a germanium photopeak by a factor of ~8.
# Standard values; see refs.md.
FANO_FACTORS = {"Si": 0.115, "Ge": 0.13, "gas": 0.20, "scintillator": 1.0}


# --- carrier statistics: where resolution comes from ----------------------

def carriers_produced(e_mev, w_ev):
    """N = E/w: information carriers (ion pairs, electron-hole pairs,
    photoelectrons) produced by depositing e_mev with a carrier cost of w_ev.

    This is the number everything else depends on.  A 1 MeV event makes ~336 000
    electron-hole pairs in germanium and ~30 000 ion pairs in argon."""
    if e_mev <= 0 or w_ev <= 0:
        raise ValueError("energy and w-value must be positive")
    return e_mev * 1.0e6 / w_ev


def carrier_sigma(n_carriers, fano=1.0):
    """sigma_N = sqrt(F N).

    F = 1 recovers Poisson.  Real semiconductors have F ~ 0.1: the carriers are
    NOT independent, because the total energy is fixed and every quantum spent
    on one excitation is unavailable to another.  That correlation SUPPRESSES the
    variance, and ignoring it overestimates a germanium peak width threefold."""
    if n_carriers < 0 or fano <= 0:
        raise ValueError("carrier count must be non-negative and F positive")
    return math.sqrt(fano * n_carriers)


def intrinsic_resolution_fraction(e_mev, w_ev, fano=1.0):
    """FWHM/E from carrier statistics alone: 2.355 sqrt(F/N).

    A LOWER BOUND, not a prediction.  Real resolution also carries incomplete
    charge collection, electronic noise and (for scintillators) photocathode and
    light-collection statistics, all of which add in quadrature."""
    n = carriers_produced(e_mev, w_ev)
    return FWHM_PER_SIGMA * carrier_sigma(n, fano) / n


def intrinsic_resolution_percent(e_mev, w_ev, fano=1.0):
    """The same, as a percentage -- the units resolution is always quoted in."""
    return 100.0 * intrinsic_resolution_fraction(e_mev, w_ev, fano)


def fwhm_energy(e_mev, w_ev, fano=1.0):
    """Absolute FWHM in MeV, i.e. the peak width you would measure."""
    return e_mev * intrinsic_resolution_fraction(e_mev, w_ev, fano)


# --- gas multiplication  [S&F Eqs. (8.6)-(8.7), printed p. 232] ----------

def townsend_series_terms(f, delta, n_terms):
    """The first n terms of S&F Eq. (8.6):

        M = f + delta f^2 + delta^2 f^3 + ... = sum_i delta^(i-1) f^i .

    f is the multiplication per avalanche and delta the probability that an
    avalanche triggers a further one (via UV photons or ion feedback).

    Evaluated as f*(delta f)^(i-1) rather than delta^(i-1) * f^i.  The two are
    algebraically identical, but the printed form overflows for large f and
    modest term counts (f = 100 at 200 terms is 100^200), while the factored
    form is bounded whenever the series converges at all -- which is exactly the
    regime the function is used in."""
    if f <= 0 or delta < 0 or n_terms < 1:
        raise ValueError("f must be positive, delta non-negative, n_terms >= 1")
    ratio = delta * f
    return [f * ratio ** (i - 1) for i in range(1, n_terms + 1)]


def gas_multiplication(f, delta):
    """Total gas multiplication  [S&F Eq. (8.7)]:  M = f/(1 - delta f).

    The geometric series of Eq. (8.6), summed.  It converges only for
    delta*f < 1; at delta*f = 1 the avalanche becomes self-sustaining and the
    detector has left proportional operation for the Geiger-Mueller regime,
    where the output no longer depends on the deposited energy at all.

    That divergence is not a mathematical artefact -- it IS the transition
    between the two detector types."""
    if f <= 0 or delta < 0:
        raise ValueError("f must be positive and delta non-negative")
    if delta * f >= 1.0:
        raise ValueError("delta*f = %.4f >= 1: the series diverges and the "
                         "avalanche is self-sustaining -- this is the "
                         "Geiger-Mueller regime, not proportional operation"
                         % (delta * f))
    return f / (1.0 - delta * f)


# --- scintillators: photons are not the carriers that count --------------

def scintillator_photoelectrons(e_mev, scintillator, light_collection=0.7,
                                quantum_efficiency=0.25):
    """Photoelectrons reaching the first dynode of a PMT.

    The chain is lossy and every step costs resolution, because the SMALLEST
    number along it is the one that governs the statistics:

        photons produced (Table 8.1) -> collected -> converted at the photocathode

    NaI(Tl) makes 38 000 photons/MeV but delivers only ~6 600 photoelectrons at
    typical efficiencies -- a w of ~150 eV per usable carrier, fifty times
    germanium's.  That, not the light yield, is why NaI resolves poorly."""
    if scintillator not in SCINTILLATORS_INORGANIC:
        raise KeyError("no Table 8.1 entry for %r" % scintillator)
    if not (0 < light_collection <= 1) or not (0 < quantum_efficiency <= 1):
        raise ValueError("efficiencies must lie in (0, 1]")
    photons = SCINTILLATORS_INORGANIC[scintillator]["photons_per_MeV"] * e_mev
    return photons * light_collection * quantum_efficiency


def photopeak_resolution_percent(e_mev, scintillator, light_collection=0.7,
                                 quantum_efficiency=0.25):
    """Statistical resolution of a scintillator, from the PHOTOELECTRON count.

    Uses F = 1: scintillator carrier statistics are essentially Poisson, with no
    Fano suppression, because the photoelectron count is set by an independent
    cascade of lossy steps rather than by a fixed energy budget."""
    npe = scintillator_photoelectrons(e_mev, scintillator, light_collection,
                                      quantum_efficiency)
    return 100.0 * FWHM_PER_SIGMA / math.sqrt(npe)


def compare_resolution(e_mev=0.6617):
    """Intrinsic resolution of the main detector families at one energy,
    defaulting to 137Cs's 662 keV line (~NE-12).

    Returns [(label, w_eV_effective, N, FWHM %)] sorted best first."""
    rows = []
    for m in ("Ge", "Si", "CdTe"):
        w = SEMICONDUCTORS[m]["w_eV"]
        f = FANO_FACTORS.get(m, 0.13)
        rows.append(("%s semiconductor" % m, w, carriers_produced(e_mev, w),
                     intrinsic_resolution_percent(e_mev, w, f)))
    for g in ("Ar", "air"):
        w = GAS_W_VALUES[g]
        rows.append(("%s gas" % g, w, carriers_produced(e_mev, w),
                     intrinsic_resolution_percent(e_mev, w, FANO_FACTORS["gas"])))
    for s in ("NaI(Tl)", "LaBr3(Ce)", "BGO"):
        npe = scintillator_photoelectrons(e_mev, s)
        rows.append(("%s scintillator" % s, e_mev * 1e6 / npe, npe,
                     photopeak_resolution_percent(e_mev, s)))
    return sorted(rows, key=lambda r: r[3])


# --- demo --------------------------------------------------------------------

def _demo():
    print("NE-15  radiation detectors\n")

    print("  resolution comes from the CARRIER COUNT, and nothing else")
    print("   detector                    w (eV)    carriers    FWHM at 662 keV")
    for lab, w, n, r in compare_resolution():
        print("   %-26s %7.1f %11.0f %12.2f%%" % (lab, w, n, r))
    print("   -> germanium wins by ~30x on resolution because w is ~50x smaller.")

    print("\n  Table 8.2: the semiconductor trade-off")
    print("   material    Z      band gap    w (eV/pair)   carriers/MeV   FWHM at 1 MeV")
    for m, d in SEMICONDUCTORS.items():
        z = d["Z"] if isinstance(d["Z"], int) else d["Z"][0]
        n = carriers_produced(1.0, d["w_eV"])
        print("   %-10s %-6s %8.2f %12.2f %14.0f %12.3f%%"
              % (m, z, d["band_gap_eV"], d["w_eV"], n,
                 intrinsic_resolution_percent(1.0, d["w_eV"], 0.13)))
    print("   -> small band gap means small w means good resolution -- but also")
    print("      more thermal noise, which is why Ge must be cooled and CdTe need not.")

    print("\n  Table 8.1: scintillators, and what actually reaches the PMT")
    print("   scintillator   photons/MeV   decay (ns)   photoelectrons   FWHM at 662 keV")
    for s in ("NaI(Tl)", "CsI(Tl)", "LaBr3(Ce)", "BGO", "LSO(Ce)"):
        d = SCINTILLATORS_INORGANIC[s]
        print("   %-14s %11d %12s %14.0f %12.2f%%"
              % (s, d["photons_per_MeV"], "/".join(str(x) for x in d["decay_ns"]),
                 scintillator_photoelectrons(0.6617, s),
                 photopeak_resolution_percent(0.6617, s)))
    print("   -> CsI(Tl) makes the most light but is slow; LaBr3 is bright AND fast.")

    print("\n  gas multiplication  [Eqs. (8.6)-(8.7)]")
    print("   f      delta    M = f/(1-delta f)   regime")
    for f, d in ((10.0, 0.0), (10.0, 0.02), (10.0, 0.05), (10.0, 0.09), (10.0, 0.099)):
        try:
            m = "%18.1f" % gas_multiplication(f, d)
            reg = "proportional"
        except ValueError:
            m, reg = "%18s" % "diverges", "Geiger-Mueller"
        print("   %-6.1f %-8.3f %s   %s" % (f, d, m, reg))
    print("   at delta*f = 1 the avalanche self-sustains: proportionality is lost.")

    print("\n  why the Fano factor cannot be ignored")
    for m in ("Ge", "Si"):
        w, f = SEMICONDUCTORS[m]["w_eV"], FANO_FACTORS[m]
        poisson = intrinsic_resolution_percent(0.6617, w, 1.0)
        real = intrinsic_resolution_percent(0.6617, w, f)
        print("   %-4s F = %.3f:  Poisson would give %.3f%%, actual %.3f%%  (x%.1f too wide)"
              % (m, f, poisson, real, poisson / real))


if __name__ == "__main__":
    _demo()
