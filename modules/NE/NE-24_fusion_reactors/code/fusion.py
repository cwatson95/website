"""NE-24  Fusion reactors: the Lawson criterion, the triple product, MCF and ICF.

Nuclear Science & Engineering trunk, module NE-24 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 12.1-12.4 (printed pp. 429-455).  Pure stdlib.

~NE-10 showed that fusion releases more energy per nucleon than fission.  This
module is about why that has not yet been useful, and the answer is three
compounding difficulties, each of which the chapter quantifies:

  1. YOU MUST MAKE A PLASMA.  The Saha equation says a hydrogen gas is 95%
     ionised only above ~13 000 K, and at room temperature the ionised fraction
     is ~1e-111.  There is no gentle approach to a plasma.

  2. IT RADIATES FASTER THAN IT BURNS, UNTIL IT DOESN'T.  Bremsstrahlung goes as
     n^2 sqrt(T) while fusion power goes as n^2 <sigma v>, and <sigma v> rises
     far more steeply.  They cross at the IGNITION TEMPERATURE -- 3e7 K for D-T
     and 5e8 K for D-D, a factor of seventeen that is the whole reason every
     experiment burns tritium.

  3. YOU MUST HOLD IT LONG ENOUGH.  Lawson's argument gives n tau_E >= 12kT/(E_c
     <sigma v>), and the modern figure of merit is the TRIPLE PRODUCT n tau_E T,
     which is nearly independent of density and only weakly dependent on
     temperature -- so it measures the confinement scheme and not the operating
     point.

The module supplies the one thing S&F only draw as a figure: a usable <sigma v>.
Fig. 12.1 is a graph, and every number in §§12.2-12.3 depends on reading it.  The
fits here reproduce the book's own Fig. 12.2 ignition temperatures to 4% (D-T)
and 12% (D-D), which is the check that they are the same curves.
"""

import math

__all__ = [
    "K_B_EV", "K_B_J", "M_E", "H_PLANCK", "MEV_TO_J",
    "HYDROGEN_IONIZATION_EV", "HYDROGEN_IONIZATION_PRINTED",
    "REACTIONS", "BREMSSTRAHLUNG_COEFF", "ITER",
    "saha_ionization_fraction", "sigma_v_dt", "sigma_v_dd",
    "fusion_power_density", "bremsstrahlung_power_density",
    "ignition_temperature", "gain_factor", "breakeven_alpha_fraction",
    "energy_confinement_time", "lawson_n_tau", "triple_product",
    "optimal_temperature",
    "icf_confinement_time", "icf_burn_fraction", "areal_density_for_burn",
]

K_B_EV = 8.617333e-5            # eV/K
K_B_J = 1.380649e-23
M_E = 9.109384e-31
H_PLANCK = 6.626070e-34
MEV_TO_J = 1.602177e-13
EV_TO_J = 1.602177e-19

# S&F §12.1.1 prints I = 13.06 eV for the hydrogen isotopes.  The accepted value
# is 13.598 eV -- a transposed digit.  The book's own worked example (95%
# ionised at 13 150 K) reproduces only with 13.06, so the example is internally
# consistent with the wrong constant.  See refs.md.
HYDROGEN_IONIZATION_EV = 13.598
HYDROGEN_IONIZATION_PRINTED = 13.06

# S&F Eqs. (12.2)-(12.3): Q values and the charged/neutral split, MeV.
REACTIONS = {
    "D-T": {"q_mev": 17.6, "charged_mev": 3.5, "neutral_mev": 14.1,
            "identical": False,
            "products": "4He (3.5 MeV) + n (14.1 MeV)"},
    "D-D(n)": {"q_mev": 3.27, "charged_mev": 0.82, "neutral_mev": 2.45,
               "identical": True, "products": "3He (0.82 MeV) + n (2.45 MeV)"},
    "D-D(p)": {"q_mev": 4.03, "charged_mev": 4.03, "neutral_mev": 0.0,
               "identical": True, "products": "1H (3.02 MeV) + 3H (1.01 MeV)"},
}
# footnote 4: the branch-averaged charged energy for D-D
DD_CHARGED_MEV = (4.03 + 0.82) / 2.0

BREMSSTRAHLUNG_COEFF = 1.42e-34     # S&F Eq. (12.6), W cm^3 K^-1/2

# §12.2.6 and Table 12.x, as printed
ITER = {"mass_tonnes": 23000, "site": "Cadarache, France",
        "agreed": 2005, "construction_began": 2013,
        "initial_cost_billion_usd": 6, "produces_electricity": False}


# --- making a plasma  [S&F Eq. (12.1)] -----------------------------------

def saha_ionization_fraction(t_k, n_per_m3, ionization_ev=None):
    """Solve the Saha equation  [S&F Eq. (12.1)] for the ionised fraction:

        f^2/(1-f) = (1/n)(2 pi m_e k T/h^2)^{3/2} exp(-I/kT) .

    The point of the equation is how abruptly it switches.  At S&F's example
    conditions (n = 2e21 m^-3, 13 150 K) a hydrogen gas is 95% ionised; at room
    temperature the same gas is ionised at the 1e-111 level.  There is no gentle
    approach to a plasma -- you are either in one or nowhere near one."""
    i_ev = HYDROGEN_IONIZATION_EV if ionization_ev is None else ionization_ev
    if t_k <= 0 or n_per_m3 <= 0 or i_ev <= 0:
        raise ValueError("temperature, density and ionization energy must be positive")
    kt = K_B_J * t_k
    rhs = ((1.0 / n_per_m3) * (2.0 * math.pi * M_E * kt / H_PLANCK ** 2) ** 1.5
           * math.exp(-i_ev * EV_TO_J / kt))
    # f^2 + rhs f - rhs = 0
    return 0.5 * (-rhs + math.sqrt(rhs * rhs + 4.0 * rhs))


# --- reactivity  [the curves behind S&F Fig. 12.1] -----------------------

def sigma_v_dt(kt_kev):
    """<sigma v> for D-T, cm^3/s, from the standard log-Gaussian fit

        <sigma v> = 9.10e-16 exp(-0.572 |ln(T/64.2)|^2.13) .

    S&F give Fig. 12.1 and no formula, so every number in §§12.2-12.3 depends on
    reading a graph.  This fit peaks at 64 keV, which is where the D-T cross
    section peaks, and it reproduces the book's own Fig. 12.2 ignition
    temperature to 4%.

    Valid roughly 1-200 keV; refuses outside, because the fit is a fit."""
    if not 0.5 <= kt_kev <= 200.0:
        raise ValueError("the D-T fit is valid for about 0.5-200 keV, not %g"
                         % kt_kev)
    return 9.10e-16 * math.exp(-0.572 * abs(math.log(kt_kev / 64.2)) ** 2.13)


def sigma_v_dd(kt_kev):
    """<sigma v> for D-D, both branches summed, cm^3/s, from the Gamow-form fit

        <sigma v> = 2.72e-14 T^{-2/3} exp(-18.76 T^{-1/3}) .

    ACCURATE ONLY BELOW ~25 keV.  The Gamow form assumes the rate is set by
    barrier penetration alone, which fails once the cross section turns over; at
    100 keV it is about a factor of two low.  It is allowed up to 100 keV because
    D-D IGNITION itself lies at ~45 keV -- outside the trustworthy range, which
    is itself worth knowing -- and refused beyond, where it is simply wrong.

    Because the fit is LOW in that region it understates the D-D fusion power,
    so the ignition temperature it returns is an OVER-estimate of the easy case:
    the real D-D ignition is no harder than this, and no easier than D-T's."""
    if not 0.5 <= kt_kev <= 100.0:
        raise ValueError("the D-D Gamow fit is offered over 0.5-100 keV and is "
                         "trustworthy only below ~25 keV; asked for %g keV"
                         % kt_kev)
    return 2.72e-14 * kt_kev ** (-2.0 / 3.0) * math.exp(-18.76 * kt_kev ** (-1.0 / 3.0))


def fusion_power_density(n_per_cm3, kt_kev, reaction="D-T"):
    """W/cm^3  [S&F Eq. (12.5)], for an equimolar D-T or a pure D plasma.

    For D-T, n1 = n2 = n/2 so the rate is n^2<sigma v>/4.  For D-D the two
    reactants are identical, so the rate is n^2<sigma v>/2 -- the factor of 1/2
    that S&F's footnote 1 exists to warn about, and which is easy to lose."""
    if n_per_cm3 < 0:
        raise ValueError("density cannot be negative")
    if reaction == "D-T":
        return 0.25 * n_per_cm3 ** 2 * sigma_v_dt(kt_kev) * 17.6 * MEV_TO_J
    if reaction == "D-D":
        q = 0.5 * (REACTIONS["D-D(n)"]["q_mev"] + REACTIONS["D-D(p)"]["q_mev"])
        return 0.5 * n_per_cm3 ** 2 * sigma_v_dd(kt_kev) * q * MEV_TO_J
    raise KeyError("reaction must be 'D-T' or 'D-D'")


def bremsstrahlung_power_density(n_per_cm3, kt_kev, z=1.0):
    """W/cm^3  [S&F Eq. (12.6)]: 1.42e-34 Z^2 n_i n_e sqrt(T), T in KELVIN.

    Note the Z^2: a percent of tungsten sputtered off the wall radiates like
    5000 hydrogens, which is why plasma-facing materials are a first-order
    physics problem and not an engineering detail.

    (S&F print the units as 'W cm^-3 s^-1'. A watt is already a joule per
    second; the quantity is a power density, W cm^-3.)"""
    if n_per_cm3 < 0 or kt_kev <= 0:
        raise ValueError("density must be non-negative and temperature positive")
    t_k = kt_kev * 1e3 / K_B_EV
    return BREMSSTRAHLUNG_COEFF * z * z * n_per_cm3 ** 2 * math.sqrt(t_k)


def ignition_temperature(reaction="D-T", z=1.0, lo=0.6, hi=None):
    """The critical ignition temperature, keV: where fusion power equals
    bremsstrahlung loss  [S&F §12.2, Fig. 12.2].

    Density cancels -- both terms go as n^2 -- so it is a property of the fuel
    alone.  D-T ignites at 3.1e7 K and D-D at 5.3e8 K, a factor of seventeen.
    That gap is why every serious experiment burns tritium despite tritium being
    radioactive, scarce and impossible to stockpile."""
    hi = (150.0 if reaction == "D-T" else 99.0) if hi is None else hi
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if fusion_power_density(1.0, mid, reaction) < bremsstrahlung_power_density(1.0, mid, z):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# --- the gain factor  [S&F Eq. (12.7)] -----------------------------------

def gain_factor(eta_heat=0.7, f_recirc=0.25, eta_elect=0.35, f_charged=0.2):
    """Q = Pfus/Pheat = 1/(eta_heat f_recirc eta_elect (1 - f_c))
    [S&F Eq. (12.7)].

    With S&F's own assumptions this gives Q ~ 20, and that is the number that
    matters: a fusion POWER PLANT needs about twenty, not one.  Q = 1 is
    "scientific break-even", which sounds like the goal and is not -- it is the
    point at which the plasma produces as much energy as was put into it, before
    any of the losses in making electricity and putting it back."""
    for name, v in (("eta_heat", eta_heat), ("f_recirc", f_recirc),
                    ("eta_elect", eta_elect)):
        if not 0 < v <= 1:
            raise ValueError("%s must lie in (0, 1]" % name)
    if not 0 <= f_charged < 1:
        raise ValueError("the charged-product fraction must lie in [0, 1)")
    return 1.0 / (eta_heat * f_recirc * eta_elect * (1.0 - f_charged))


def breakeven_alpha_fraction(reaction="D-T"):
    """E_charged/Q_fus -- the fraction of the fusion energy that stays in the
    plasma and can heat it.

    For D-T it is 3.5/17.6 = 0.20, so at Q = 1 the alphas supply a fifth of the
    heating.  IGNITION -- Q infinite -- needs the alphas to supply all of it,
    which is a fivefold further step and not a marginal one."""
    if reaction == "D-T":
        r = REACTIONS["D-T"]
        return r["charged_mev"] / r["q_mev"]
    if reaction == "D-D":
        q = 0.5 * (REACTIONS["D-D(n)"]["q_mev"] + REACTIONS["D-D(p)"]["q_mev"])
        return DD_CHARGED_MEV / q
    raise KeyError("reaction must be 'D-T' or 'D-D'")


# --- Lawson  [S&F Eqs. (12.8)-(12.14)] -----------------------------------

def energy_confinement_time(n_per_cm3, kt_kev, p_loss_w_per_cm3):
    """tau_E = 3nkT/P_loss  [S&F Eq. (12.8)].

    Note the 3, not 3/2: the plasma holds (3/2)kT per ion AND per electron, and
    n_e = n.  Dropping the electrons halves the answer."""
    if p_loss_w_per_cm3 <= 0:
        raise ValueError("the loss power must be positive")
    return 3.0 * n_per_cm3 * kt_kev * 1e3 * EV_TO_J / p_loss_w_per_cm3


def lawson_n_tau(kt_kev, reaction="D-T"):
    """n tau_E, s/cm^3  [S&F Eq. (12.10)]:

        D-T:  12 kT/(E_c <sigma v>)      (n1 = n2 = n/2)
        D-D:   6 kT/(E_c <sigma v>)      (identical reactants)

    The two prefactors differ because of the identical-particle factor, and
    getting them the wrong way round is the classic error here."""
    if reaction == "D-T":
        e_c = REACTIONS["D-T"]["charged_mev"]
        return 12.0 * kt_kev * 1e-3 / (e_c * sigma_v_dt(kt_kev))
    if reaction == "D-D":
        return 6.0 * kt_kev * 1e-3 / (DD_CHARGED_MEV * sigma_v_dd(kt_kev))
    raise KeyError("reaction must be 'D-T' or 'D-D'")


def triple_product(kt_kev, reaction="D-T"):
    """n tau_E T, keV s/cm^3  [S&F Eq. (12.11)] -- the modern figure of merit.

    It is nearly independent of density and only weakly dependent on temperature
    [Eq. (12.13)], so it measures the CONFINEMENT SCHEME rather than the
    operating point.  Its minimum for D-T is about 2e15 keV s cm^-3
    [Eq. (12.14)], and finding that minimum is what tells a designer what
    temperature to run at."""
    return lawson_n_tau(kt_kev, reaction) * kt_kev


def optimal_temperature(reaction="D-T", lo=1.0, hi=None, n=4000):
    """The temperature minimising the triple product -- i.e. the easiest place to
    build a reactor.  For D-T it is about 25 keV."""
    hi = (150.0 if reaction == "D-T" else 24.0) if hi is None else hi
    best, best_t = None, None
    for i in range(n):
        t = lo + (hi - lo) * i / (n - 1)
        try:
            v = triple_product(t, reaction)
        except ValueError:
            continue
        if best is None or v < best:
            best, best_t = v, t
    return best_t, best


# --- inertial confinement  [S&F §12.3, Eq. (12.15)] ----------------------

def icf_confinement_time(radius_cm, kt_kev, mass_amu=2.5):
    """tau_E = R/v with v the ion sound speed sqrt(kT/m)  [S&F Eq. (12.15)].

    For a millimetre pellet at 10 keV this is ~1e-9 s, which is why ICF must
    reach densities a thousand times solid: the Lawson product is bought with n,
    not tau."""
    if radius_cm <= 0 or kt_kev <= 0:
        raise ValueError("radius and temperature must be positive")
    m = mass_amu * 1.660539e-27
    v = math.sqrt(kt_kev * 1e3 * EV_TO_J / m)     # cm/s after conversion below
    return radius_cm / (v * 100.0)


def areal_density_for_burn(burn_fraction, hb_g_per_cm2=6.0):
    """rho R needed for a given burn fraction, g/cm^2, from the standard

        phi = rho R/(rho R + H_B),   H_B ~ 6 g/cm^2 for D-T at 20-40 keV.

    Beyond S&F, which says only that "in practice, only a small portion of the
    pellet fuel actually fuses".  A third of the fuel needs rho R = 3 g/cm^2 --
    against ~0.2 g/cm^2 for a solid-density millimetre pellet, hence the factor
    of a thousand in compression."""
    if not 0 < burn_fraction < 1:
        raise ValueError("the burn fraction must lie in (0, 1)")
    return hb_g_per_cm2 * burn_fraction / (1.0 - burn_fraction)


def icf_burn_fraction(rho_r_g_per_cm2, hb_g_per_cm2=6.0):
    """The inverse of `areal_density_for_burn`."""
    if rho_r_g_per_cm2 < 0:
        raise ValueError("areal density cannot be negative")
    return rho_r_g_per_cm2 / (rho_r_g_per_cm2 + hb_g_per_cm2)


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-24  fusion reactors\n")

    print("  1. you must make a plasma  [Eq. (12.1)]")
    print("   T (K)      ionised fraction (n = 2e21 m^-3)")
    for t in (293.0, 5000.0, 10000.0, 13150.0, 20000.0, 1e5):
        print("   %-10.4g %.4g" % (t, saha_ionization_fraction(t, 2e21)))
    print("   S&F's example uses I = 13.06 eV and gets 95%% at 13 150 K:")
    print("     with 13.06 eV -> %.4f ; with the true 13.598 eV -> %.4f"
          % (saha_ionization_fraction(13150.0, 2e21, 13.06),
             saha_ionization_fraction(13150.0, 2e21)))

    print("\n  2. it radiates faster than it burns, until it doesn't")
    print("   kT (keV)   <sv> D-T      <sv> D-D      P_fus/P_brems (D-T)")
    for t in (1.0, 2.0, 5.0, 10.0, 20.0):
        print("   %-10.1f %.4e %.4e %10.3f"
              % (t, sigma_v_dt(t), sigma_v_dd(t),
                 fusion_power_density(1e15, t) / bremsstrahlung_power_density(1e15, t)))
    for r in ("D-T", "D-D"):
        ti = ignition_temperature(r)
        print("   %s ignition: %.2f keV = %.2e K  (S&F Fig. 12.2: %s)"
              % (r, ti, ti * 1e3 / K_B_EV, "3e7 K" if r == "D-T" else "6e8 K"))
    print("   -> a factor of %.0f in temperature. That is why everyone burns tritium."
          % (ignition_temperature("D-D") / ignition_temperature("D-T")))

    print("\n  3. you must hold it long enough  [Eqs. (12.10), (12.11)]")
    print("   kT (keV)   n tau (s/cm3)   n tau T (keV s/cm3)")
    for t in (2.0, 5.0, 10.0, 20.0, 25.0):
        print("   %-10.1f %.4e %14.4e" % (t, lawson_n_tau(t), triple_product(t)))
    t_opt, v_opt = optimal_temperature()
    print("   optimum for D-T: %.1f keV, triple product %.3e keV s cm^-3"
          % (t_opt, v_opt))
    print("   (S&F Eq. (12.14) quotes > 2e15 keV s cm^-3)")
    print("   D-D at 10 keV needs %.0fx the n tau of D-T"
          % (lawson_n_tau(10.0, "D-D") / lawson_n_tau(10.0, "D-T")))

    print("\n  the gain factor  [Eq. (12.7)]")
    print("   alphas carry %.0f%% of D-T's energy, so Q = 1 means the plasma"
          % (100 * breakeven_alpha_fraction()))
    print("   self-heats only a fifth of the way.")
    print("   f_recirc  eta_elect   Q needed")
    for fr, ee in ((0.25, 0.35), (0.25, 0.45), (0.10, 0.35), (0.50, 0.35)):
        print("   %8.2f %10.2f %10.1f" % (fr, ee, gain_factor(0.7, fr, ee)))
    print("   -> a POWER PLANT needs Q ~ 20, not Q = 1.")

    print("\n  inertial confinement  [Eq. (12.15)]")
    print("   a 1 mm pellet at 10 keV is confined for %.3e s"
          % icf_confinement_time(0.05, 10.0))
    print("   burn fraction   needed rho R (g/cm2)")
    for phi in (0.01, 0.1, 0.3, 0.5):
        print("   %13.2f %18.2f" % (phi, areal_density_for_burn(phi)))
    print("   a solid-density 1 mm D-T pellet has rho R ~ 0.02 g/cm2, so it")
    print("   must be compressed a thousandfold to burn a third of itself.")


if __name__ == "__main__":
    _demo()
