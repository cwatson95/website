"""NE-19  The neutron life cycle: the four- and six-factor formulas, k_eff.

Nuclear Science & Engineering trunk, module NE-19 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 10.1-10.6 (printed pp. 322-339).  Pure stdlib.

A reactor is a bookkeeping problem.  Follow one generation of fission neutrons
around the cycle, count what happens to them, and the ratio of the next
generation to this one is k_eff.  S&F define SIX factors:

    eps         fast fission factor -- the bonus from 238U fissioning above 1 MeV
    p           resonance escape probability -- surviving 238U's resonances
    f           thermal utilization -- absorbed by fuel rather than by everything else
    eta         thermal fission factor -- fast neutrons produced per thermal
                absorption in the fuel
    P_NL^f      fast non-leakage
    P_NL^th     thermal non-leakage

and then

    k_inf  = eps p f eta                              (the FOUR-factor formula)
    k_eff  = eps p f eta P_NL^f P_NL^th               (the SIX-factor formula)

WARNING, and the reason this module has a test named after it: S&F's printed
Eqs. (10.16) and (10.17) OMIT eps, and Eq. (10.17) calls the three-factor
product "the four-factor formula".  The book's own Tables 10.5 and 10.8 include
eps -- Table 10.5's water row is 0.888, which is eps*eta*f*p and not eta*f*p
(0.845).  `k_infinity` therefore takes eps and defaults it to 1.0, and
`four_factor_formula_as_printed` reproduces the printed version so the
difference can be seen rather than argued about.

The physics worth carrying away is that the factors PULL AGAINST EACH OTHER.
Adding moderator raises p (fewer resonance captures while slowing down) and
lowers f (more thermal neutrons absorbed by the moderator instead of the fuel).
There is therefore an optimum moderator-to-fuel ratio, and k_inf at that optimum
is BELOW ONE for natural uranium in every moderator except heavy water
[Table 10.5].  That single fact is why enrichment plants exist, and why the only
natural-uranium power reactors are CANDUs and the graphite-moderated designs
that lump their fuel.
"""

import math

__all__ = [
    "K_BOLTZMANN_EV", "ROOM_T_K", "THERMAL_ENERGY_EV", "THERMAL_SPEED_M_S",
    "AVOGADRO", "FUEL_THERMAL_AVERAGED", "FUEL_PROPERTIES",
    "MODERATOR_SLOWING", "MODERATOR_THERMAL", "OPTIMUM_RATIOS",
    "RESONANCE_ROD_CONSTANTS", "XI_SIGMA_S", "LATTICE_TABLE",
    "EPSILON_FIT", "RESONANCE_INTEGRAL_FIT",
    "maxwellian_flux", "most_probable_energy", "mean_thermal_energy",
    "westcott_averaged_cross_section",
    "fast_fission_factor", "resonance_integral_homogeneous",
    "resonance_escape_homogeneous", "resonance_integral_rod",
    "resonance_escape_lattice", "thermal_utilization_homogeneous",
    "thermal_fission_factor", "eta_of_uranium",
    "bessel_i0", "bessel_i1", "bessel_k0", "bessel_k1",
    "lattice_F", "lattice_E", "thermal_utilization_lattice",
    "diffusion_length_squared", "thermal_nonleakage", "fast_nonleakage",
    "geometric_buckling", "k_infinity", "k_effective",
    "four_factor_formula_as_printed", "critical_buckling", "critical_radius_sphere",
    "reactivity", "SIGMA_S_D2O_ERRATA", "L2_GRAPHITE_ERRATA",
]

K_BOLTZMANN_EV = 8.617333e-5        # eV/K
ROOM_T_K = 293.61                   # S&F §10.2: 20.46 C, chosen so kT = 0.0253 eV
THERMAL_ENERGY_EV = 0.02530         # kT at ROOM_T_K; a 2200 m/s neutron
THERMAL_SPEED_M_S = 2200.0
AVOGADRO = 0.602214                 # in 1e24/mol, so N (atoms/b-cm) = rho*Na/A

# --- Table 10.1 (printed p. 323): THERMAL-AVERAGED microscopic cross sections
# (barns) at 20 C, and nu per thermal fission.  These already contain the
# sqrt(pi)/2 Westcott factor -- which is why they differ from Table 10.2.
FUEL_THERMAL_AVERAGED = {
    "232Th": {"sigma_a": 6.503, "sigma_f": None, "nu": None},
    "233U": {"sigma_a": 510.1, "sigma_f": 471.0, "nu": 2.497},
    "234U": {"sigma_a": 89.49, "sigma_f": None, "nu": None},
    "235U": {"sigma_a": 592.6, "sigma_f": 505.9, "nu": 2.437},
    "238U": {"sigma_a": 2.382, "sigma_f": None, "nu": None},
    "239Pu": {"sigma_a": 968.0, "sigma_f": 695.1, "nu": 2.879},
}

# --- Table 10.2 (printed p. 324): cross sections AT 0.0253 eV (2200 m/s),
# ENDF/B-VII.1.  (sigma_a, sigma_gamma, sigma_f, sigma_gamma/sigma_f, nu, eta)
FUEL_PROPERTIES = {
    "232Th": (7.3381, 7.3381, None, None, None, None),
    "233U": (576.60, 45.266, 531.34, 0.08519, 2.4968, 2.301),
    "234U": (100.98, 100.91, 0.06710, None, None, None),
    "235U": (683.68, 98.687, 584.99, 0.14435, 2.4367, 2.085),
    "238U": (2.6835, 2.6835, None, None, None, None),
    "239Pu": (1018.6, 270.73, 747.92, 0.3619, 2.8789, 2.114),
    "240Pu": (287.56, 287.56, None, None, None, None),
    "241Pu": (1376.5, 363.41, 1013.11, 0.3577, 2.9453, 2.151),
}

# --- Table 10.3 (printed p. 327): slowing-down region, for Eq. (10.9).
# heavy water's sigma_sM is printed as 0.509 b -- a duplicate of its own xi.
# Table 10.7's xi*Sigma_s for the same material requires 10.6 b, which is also
# the accepted value.  See refs.md; SIGMA_S_D2O_ERRATA keeps the printed number.
SIGMA_S_D2O_ERRATA = 0.509
MODERATOR_SLOWING = {
    "water": {"xi": 0.920, "sigma_s": 44.8},
    "heavy water": {"xi": 0.509, "sigma_s": 10.6},      # corrected
    "beryllium": {"xi": 0.207, "sigma_s": 6.1},
    "graphite": {"xi": 0.158, "sigma_s": 4.8},
}

# --- Table 10.4 (printed p. 329): thermal properties of pure moderators.
MODERATOR_THERMAL = {
    "H2O": {"rho": 1.00, "sigma_a_mb": 664.4, "Sigma_a": 0.0197,
            "D": 0.16, "L2": 8.12, "L": 2.85, "tau": 27.0},
    "D2O": {"rho": 1.10, "sigma_a_mb": 1.194, "Sigma_a": 3.50e-5,
            "D": 0.87, "L2": 24900.0, "L": 158.0, "tau": 131.0},
    "Be": {"rho": 1.85, "sigma_a_mb": 8.493, "Sigma_a": 9.31e-4,
           "D": 0.50, "L2": 537.0, "L": 23.2, "tau": 102.0},
    "BeO": {"rho": 2.96, "sigma_a_mb": 8.683, "Sigma_a": 5.49e-4,
            "D": 0.47, "L2": 856.0, "L": 29.2, "tau": 100.0},
    "C": {"rho": 1.60, "sigma_a_mb": 3.861, "Sigma_a": 2.74e-4,
          "D": 0.84, "L2": 3070.0, "L": 55.4, "tau": 368.0},
}
L2_GRAPHITE_ERRATA = 3500.0         # Example 10.4 writes this; Table 10.4 says 3070

# --- Table 10.5 (printed p. 334): optimum moderator/fuel for natural uranium.
# (ratio, eps, eta, f, p, k_inf)
OPTIMUM_RATIOS = {
    "H2O": (1.70, 1.051, 1.338, 0.869, 0.727, 0.888),
    "D2O": (291.0, 1.000, 1.338, 0.956, 0.917, 1.173),
    "Be": (191.0, 1.000, 1.338, 0.822, 0.708, 0.779),
    "C": (417.0, 1.000, 1.338, 0.823, 0.709, 0.781),
}

# --- Table 10.6 (printed p. 335): (A, C) for the rod resonance integral.
RESONANCE_ROD_CONSTANTS = {
    "238U metal": (2.8, 38.3), "238UO2": (3.0, 39.6),
    "232Th metal": (3.9, 20.9), "232ThO2": (3.4, 24.5),
}

# --- Table 10.7 (printed p. 335): xi_M * Sigma_sM, cm^-1.
XI_SIGMA_S = {"water": 1.46, "heavy water": 0.178, "beryllium": 0.155,
              "graphite": 0.0608}

# --- Table 10.8 (printed p. 337): the graphite/natural-uranium lattice.
# pitch a (cm) -> (eps, eta, f, p, k_inf)
LATTICE_TABLE = {
    12: (1.027, 1.336, 0.968, 0.742, 0.985),
    14: (1.027, 1.336, 0.955, 0.805, 1.054),
    16: (1.027, 1.336, 0.940, 0.848, 1.093),
    18: (1.027, 1.336, 0.923, 0.878, 1.112),
    19: (1.027, 1.336, 0.915, 0.890, 1.116),
    20: (1.027, 1.336, 0.905, 0.900, 1.118),
    21: (1.027, 1.336, 0.896, 0.909, 1.117),
    22: (1.027, 1.336, 0.886, 0.917, 1.114),
    24: (1.027, 1.336, 0.865, 0.930, 1.103),
    26: (1.027, 1.336, 0.843, 0.940, 1.087),
    28: (1.027, 1.336, 0.820, 0.948, 1.067),
}

# Eq. (10.6) fits: (a, b, c)
EPSILON_FIT = {"homogeneous": (1.0803, 0.03904, 0.08096),
               "rod": (1.1123, 0.03004, 0.1130)}
# Eq. (10.8): (a, c) for the homogeneous effective resonance integral
RESONANCE_INTEGRAL_FIT = {"238U": (2.73, 0.486), "232Th": (8.33, 0.253)}


# --- thermal neutrons  [S&F §10.2] ---------------------------------------

def maxwellian_flux(e_ev, t_k, n=1.0):
    """The Maxwellian FLUX spectrum  [S&F Eq. (10.1)], up to the mass factor:

        phi_M(E, T)  ~  E exp(-E/kT) .

    Note it is linear in E, not sqrt(E).  The neutron DENSITY spectrum is the
    familiar Maxwell-Boltzmann sqrt(E) exp(-E/kT); the flux is that times the
    speed, and v ~ sqrt(E) supplies the extra factor.  The consequence is that
    the flux peaks at kT and averages 2kT, where the density peaks at kT/2 and
    averages (3/2)kT.  Returned in arbitrary units; only shape and moments
    are used here."""
    if e_ev < 0 or t_k <= 0:
        raise ValueError("energy must be non-negative and temperature positive")
    kt = K_BOLTZMANN_EV * t_k
    return n * e_ev * math.exp(-e_ev / kt) / kt ** 2


def most_probable_energy(t_k=ROOM_T_K):
    """E_mp = kT  [S&F §10.2].  0.0253 eV at room temperature -- a 2200 m/s
    neutron, and the energy every thermal cross section is quoted at."""
    if t_k <= 0:
        raise ValueError("temperature must be positive")
    return K_BOLTZMANN_EV * t_k


def mean_thermal_energy(t_k=ROOM_T_K):
    """Ebar = 2kT for this distribution -- NOT (3/2)kT.

    The factor differs from the familiar kinetic-theory 3/2 because the
    Maxwellian FLUX is the density spectrum weighted by speed, which shifts the
    mean upward.  Confusing the two is a 33% error in a reaction rate."""
    return 2.0 * most_probable_energy(t_k)


def westcott_averaged_cross_section(sigma_at_e0, t_k=ROOM_T_K, g=1.0):
    """Thermal-averaged cross section  [S&F Eq. (10.5)]:

        sigma_bar = (sqrt(pi)/2) g(T) sqrt(T0/T) sigma(E0).

    The sqrt(pi)/2 = 0.886 comes from averaging a 1/v cross section over the
    Maxwellian; g(T) is the Westcott non-1/v factor, 1 for light nuclei.

    This is why Tables 10.1 and 10.2 disagree: 10.1 is thermal-AVERAGED and 10.2
    is at 0.0253 eV.  For 235U, 592.6 vs 683.68 b -- and 592.6/683.68 = 0.867,
    close to but not exactly 0.886, because g(T) is not 1 for 235U."""
    if sigma_at_e0 < 0 or t_k <= 0 or g <= 0:
        raise ValueError("cross section, temperature and g must be positive")
    return 0.5 * math.sqrt(math.pi) * g * math.sqrt(ROOM_T_K / t_k) * sigma_at_e0


# --- the six factors -----------------------------------------------------

def fast_fission_factor(n238_over_nm, geometry="homogeneous"):
    """eps  [S&F Eq. (10.6)], fitted to Fig. 10.2 for uranium-water systems:

        eps = a + b sqrt(0.6974 x) - c exp(-0.6974 x),   x = N238/NW.

    Fast fission is almost entirely 238U above its ~1 MeV threshold, so eps is
    near unity and is LARGER in a heterogeneous core (a fast neutron born inside
    a fuel lump meets 238U before it meets any moderator).  Typically 1.02-1.08."""
    if n238_over_nm < 0:
        raise ValueError("the atom ratio cannot be negative")
    if geometry not in EPSILON_FIT:
        raise KeyError("geometry must be one of %s" % sorted(EPSILON_FIT))
    a, b, c = EPSILON_FIT[geometry]
    x = 0.6974 * n238_over_nm
    return a + b * math.sqrt(x) - c * math.exp(-x)


def resonance_integral_homogeneous(sigma_sm, na_per_barn_cm, absorber="238U"):
    """Effective resonance integral I (barns)  [S&F Eq. (10.8)]:

        I = a (Sigma_sM * 1e24 / N_A)^c .

    Note this rises as the absorber is DILUTED: more scattering per absorber
    atom means a neutron crosses each resonance faster and is less likely to be
    caught, so each absorber atom is individually more effective."""
    if absorber not in RESONANCE_INTEGRAL_FIT:
        raise KeyError("no fit for %r; have %s"
                       % (absorber, sorted(RESONANCE_INTEGRAL_FIT)))
    if na_per_barn_cm <= 0 or sigma_sm <= 0:
        raise ValueError("densities and cross sections must be positive")
    a, c = RESONANCE_INTEGRAL_FIT[absorber]
    return a * (sigma_sm / na_per_barn_cm) ** c


def resonance_escape_homogeneous(na_over_nm, moderator="water",
                                 absorber="238U"):
    """p for a homogeneous mixture  [S&F Eq. (10.9)]:

        p = exp[ -(a/xi) (N_A/N_M / sigma_sM)^(1-c) ] .

    Falls as the absorber concentration rises, which is the whole reason a
    natural-uranium core needs a lot of moderator."""
    if moderator not in MODERATOR_SLOWING:
        raise KeyError("no Table 10.3 row for %r" % moderator)
    if na_over_nm <= 0:
        raise ValueError("the atom ratio must be positive")
    a, c = RESONANCE_INTEGRAL_FIT[absorber]
    m = MODERATOR_SLOWING[moderator]
    return math.exp(-(a / m["xi"]) * (na_over_nm / m["sigma_s"]) ** (1.0 - c))


def resonance_integral_rod(radius_cm, density_g_cm3, fuel="238U metal"):
    """I for a cylindrical fuel rod (barns)  [S&F Eq. (10.19)]:

        I = A + C/sqrt(r rho) .

    The 1/sqrt(r rho) is a SURFACE-to-volume statement: resonance capture in a
    lump happens in a thin skin, so a fatter rod has a smaller integral per atom.
    That is the quantitative content of "lumping the fuel helps"."""
    if fuel not in RESONANCE_ROD_CONSTANTS:
        raise KeyError("no Table 10.6 row for %r; have %s"
                       % (fuel, sorted(RESONANCE_ROD_CONSTANTS)))
    if radius_cm <= 0 or density_g_cm3 <= 0:
        raise ValueError("radius and density must be positive")
    a, c = RESONANCE_ROD_CONSTANTS[fuel]
    return a + c / math.sqrt(radius_cm * density_g_cm3)


def resonance_escape_lattice(n_fuel_per_barn_cm, vf_over_vm, i_barns,
                             moderator="graphite"):
    """p for a heterogeneous lattice  [S&F Eq. (10.18)]:

        p = exp[ -N_F (V_F/V_M) I / (xi_M Sigma_sM) ] .

    Lumping raises p from about 0.7 to above 0.9, because neutrons slow down in
    moderator that contains no 238U at all and only those that reach a resonance
    energy near a lump are in danger.  It is the single reason a natural-uranium
    reactor is possible with graphite."""
    if moderator not in XI_SIGMA_S:
        raise KeyError("no Table 10.7 row for %r" % moderator)
    if n_fuel_per_barn_cm <= 0 or vf_over_vm <= 0 or i_barns <= 0:
        raise ValueError("density, volume ratio and resonance integral must be positive")
    return math.exp(-n_fuel_per_barn_cm * vf_over_vm * i_barns
                    / XI_SIGMA_S[moderator])


def thermal_utilization_homogeneous(sigma_a_fuel, sigma_a_nonfuel,
                                    n_nonfuel_over_n_fuel):
    """f for a homogeneous core  [S&F Eq. (10.11)]:

        f = sigma_a^F / [sigma_a^F + sigma_a^NF (N^NF/N^F)] .

    Ranges from ~0 for a very dilute fuel to 1 for a core of pure fuel.  A
    control rod works by lowering f, and nothing else."""
    if sigma_a_fuel <= 0 or sigma_a_nonfuel < 0 or n_nonfuel_over_n_fuel < 0:
        raise ValueError("cross sections and ratios must be non-negative")
    return sigma_a_fuel / (sigma_a_fuel
                           + sigma_a_nonfuel * n_nonfuel_over_n_fuel)


def thermal_fission_factor(nu, sigma_f, sigma_a):
    """eta = nu Sigma_f / Sigma_a  [S&F Eq. (10.12)].

    A property of the FUEL ALONE -- adding or removing moderator, coolant or
    control rods does not change it.  It must exceed 1 for a chain reaction and
    exceed 2 for thermal breeding."""
    if sigma_a <= 0:
        raise ValueError("the absorption cross section must be positive")
    if nu < 0 or sigma_f < 0:
        raise ValueError("nu and sigma_f must be non-negative")
    return nu * sigma_f / sigma_a


def eta_of_uranium(enrichment_atom_fraction, table="thermal averaged"):
    """eta for uranium enriched to a given 235U ATOM fraction, treating the
    remainder as 238U  [S&F Example 10.2].

    Natural uranium (0.7204%) gives 1.338 -- above 1, which is why a reactor is
    possible at all, and far below 2, which is why a thermal breeder is not."""
    if not 0 < enrichment_atom_fraction <= 1:
        raise ValueError("the enrichment must lie in (0, 1]")
    src = FUEL_THERMAL_AVERAGED if table == "thermal averaged" else None
    if src is None:
        u5, u8 = FUEL_PROPERTIES["235U"], FUEL_PROPERTIES["238U"]
        nu, sf, sa5, sa8 = u5[4], u5[2], u5[0], u8[0]
    else:
        nu = src["235U"]["nu"]
        sf = src["235U"]["sigma_f"]
        sa5 = src["235U"]["sigma_a"]
        sa8 = src["238U"]["sigma_a"]
    e = enrichment_atom_fraction
    return nu * sf * e / (sa5 * e + sa8 * (1.0 - e))


# --- the Wigner-Seitz lattice constants  [S&F Eqs. (10.20)-(10.25)] ------

def _poly(coeffs, t):
    out = 0.0
    for c in reversed(coeffs):
        out = out * t + c
    return out


def bessel_i0(x):
    """Modified Bessel I0, Abramowitz & Stegun 9.8.1/9.8.2 (|err| < 2e-7)."""
    ax = abs(x)
    if ax < 3.75:
        t = (x / 3.75) ** 2
        return _poly([1.0, 3.5156229, 3.0899424, 1.2067492, 0.2659732,
                      0.0360768, 0.0045813], t)
    t = 3.75 / ax
    return (math.exp(ax) / math.sqrt(ax)) * _poly(
        [0.39894228, 0.01328592, 0.00225319, -0.00157565, 0.00916281,
         -0.02057706, 0.02635537, -0.01647633, 0.00392377], t)


def bessel_i1(x):
    """Modified Bessel I1, A&S 9.8.3/9.8.4."""
    ax = abs(x)
    if ax < 3.75:
        t = (x / 3.75) ** 2
        ans = ax * _poly([0.5, 0.87890594, 0.51498869, 0.15084934,
                          0.02658733, 0.00301532, 0.00032411], t)
    else:
        t = 3.75 / ax
        ans = (math.exp(ax) / math.sqrt(ax)) * _poly(
            [0.39894228, -0.03988024, -0.00362018, 0.00163801, -0.01031555,
             0.02282967, -0.02895312, 0.01787654, -0.00420059], t)
    return -ans if x < 0 else ans


def bessel_k0(x):
    """Modified Bessel K0, A&S 9.8.5/9.8.6."""
    if x <= 0:
        raise ValueError("K0 requires a positive argument")
    if x <= 2.0:
        t = x * x / 4.0
        return (-math.log(x / 2.0) * bessel_i0(x)
                + _poly([-0.57721566, 0.42278420, 0.23069756, 0.03488590,
                         0.00262698, 0.00010750, 0.0000074], t))
    t = 2.0 / x
    return (math.exp(-x) / math.sqrt(x)) * _poly(
        [1.25331414, -0.07832358, 0.02189568, -0.01062446, 0.00587872,
         -0.00251540, 0.00053208], t)


def bessel_k1(x):
    """Modified Bessel K1, A&S 9.8.7/9.8.8."""
    if x <= 0:
        raise ValueError("K1 requires a positive argument")
    if x <= 2.0:
        t = x * x / 4.0
        return ((math.log(x / 2.0) * bessel_i1(x))
                + (1.0 / x) * _poly([1.0, 0.15443144, -0.67278579, -0.18156897,
                                     -0.01919402, -0.00110404, -0.00004686], t))
    t = 2.0 / x
    return (math.exp(-x) / math.sqrt(x)) * _poly(
        [1.25331414, 0.23498619, -0.03655620, 0.01504268, -0.00780353,
         0.00325614, -0.00068245], t)


def lattice_F(x, series=False):
    """F(x) = x I0(x) / (2 I1(x))  [S&F Eq. (10.22)], or its series Eq. (10.24).

    The fuel-lump self-shielding factor: the interior of a rod is screened by its
    own outer layers, so F > 1 and the lump absorbs less than its volume
    suggests."""
    if x <= 0:
        raise ValueError("x must be positive")
    if series:
        h = x / 2.0
        return 1.0 + 0.5 * h ** 2 - h ** 4 / 12.0 + h ** 6 / 48.0
    return x * bessel_i0(x) / (2.0 * bessel_i1(x))


def lattice_E(y, z, series=False):
    """E(y, z)  [S&F Eq. (10.22)], or its series Eq. (10.25).

    The moderator flux-disadvantage factor.  The series is

        E = 1 + (z^2/2)[ (z^2/(z^2-y^2)) ln(z/y) - 3/4 + y^2/(4z^2) ] ,

    and note the grouping: the z^2/(z^2-y^2) multiplies ONLY the logarithm while
    z^2/2 multiplies the whole bracket.  In the printed two-dimensional layout
    the two leading fractions sit side by side and are easy to read as a single
    z^2/(2(z^2-y^2)) prefactor -- which gives 1.736 instead of 1.031 for S&F's
    own Example 10.9.  `test_the_lattice_series_matches_the_bessel_form` pins the
    correct reading against the exact form."""
    if y <= 0 or z <= 0:
        raise ValueError("y and z must be positive")
    if z <= y:
        raise ValueError("the cell radius must exceed the fuel radius (z > y)")
    if series:
        return 1.0 + 0.5 * z ** 2 * (
            (z ** 2 / (z ** 2 - y ** 2)) * math.log(z / y)
            - 0.75 + y ** 2 / (4.0 * z ** 2))
    num = bessel_i0(y) * bessel_k1(z) + bessel_k0(y) * bessel_i1(z)
    den = bessel_i1(z) * bessel_k1(y) - bessel_k1(z) * bessel_i1(y)
    return ((z ** 2 - y ** 2) / (2.0 * y)) * (num / den)


def thermal_utilization_lattice(sigma_a_mod, sigma_a_fuel, vm_over_vf,
                                r_cm, b_cm, l_fuel_cm, l_mod_cm, series=False):
    """f for a cylindrical-rod lattice by the Wigner-Seitz method
    [S&F Eq. (10.21)]:

        1/f = (Sigma_aM V_M)/(Sigma_aF V_F) F(x) + E(y, z) ,

    with x = r/L_F, y = r/L_M, z = b/L_M and b = a/sqrt(pi) the equivalent
    cylindrical cell radius [Eq. (10.20)].

    Accurate only for r << b.  Modern power lattices are far more tightly packed
    and need transport methods; S&F say so and this docstring repeats it rather
    than letting the formula be used outside its range."""
    if min(sigma_a_mod, sigma_a_fuel, vm_over_vf, r_cm, b_cm,
           l_fuel_cm, l_mod_cm) <= 0:
        raise ValueError("all arguments must be positive")
    x, y, z = r_cm / l_fuel_cm, r_cm / l_mod_cm, b_cm / l_mod_cm
    inv = ((sigma_a_mod * vm_over_vf) / sigma_a_fuel * lattice_F(x, series)
           + lattice_E(y, z, series))
    return 1.0 / inv


def cell_radius(pitch_cm):
    """b = a/sqrt(pi): the cylindrical cell of equal area  [S&F Eq. (10.20)]."""
    if pitch_cm <= 0:
        raise ValueError("the pitch must be positive")
    return pitch_cm / math.sqrt(math.pi)


# --- leakage  [S&F Eqs. (10.13)-(10.15)] ---------------------------------

def diffusion_length_squared(l2_moderator, f):
    """L_T^2 = L_M^2 (1 - f)  [S&F Eq. (10.14)].

    Adding fuel to a moderator soaks up thermal neutrons faster, so they diffuse
    a shorter distance before absorption.  At f = 0.81 in graphite, L^2 falls
    from 3070 to 570 cm2 -- a factor of five, and the reason a fuelled core leaks
    far less than a block of graphite of the same size."""
    if l2_moderator <= 0:
        raise ValueError("the moderator diffusion area must be positive")
    if not 0 <= f < 1:
        raise ValueError("the thermal utilization must lie in [0, 1)")
    return l2_moderator * (1.0 - f)


def thermal_nonleakage(l2, buckling):
    """P_NL^th = 1/(1 + L_T^2 B^2)  [S&F Eq. (10.13)]."""
    if l2 < 0 or buckling < 0:
        raise ValueError("diffusion area and buckling must be non-negative")
    return 1.0 / (1.0 + l2 * buckling)


def fast_nonleakage(buckling, tau):
    """P_NL^f = exp(-B^2 tau_T)  [S&F Eq. (10.15)].

    tau_T is the Fermi age, one sixth of the mean square crow-flight distance
    from birth to thermalisation.  Graphite's 368 cm2 against water's 27 is why
    a graphite core must be metres across and a water core need not be."""
    if buckling < 0 or tau < 0:
        raise ValueError("buckling and Fermi age must be non-negative")
    return math.exp(-buckling * tau)


def geometric_buckling(geometry, **dims):
    """B_g^2 for simple bare geometries  [S&F Table 10.10].

    sphere(R), cylinder(R, H), slab(a), cube(a)."""
    g = geometry.lower()
    if g == "sphere":
        return (math.pi / dims["R"]) ** 2
    if g == "cylinder":
        return (2.405 / dims["R"]) ** 2 + (math.pi / dims["H"]) ** 2
    if g == "slab":
        return (math.pi / dims["a"]) ** 2
    if g == "cube":
        return 3.0 * (math.pi / dims["a"]) ** 2
    raise KeyError("unknown geometry %r" % geometry)


# --- putting it together  [S&F Eqs. (10.16)-(10.17)] ---------------------

def k_infinity(eta, p, f, eps=1.0):
    """The FOUR-factor formula:  k_inf = eps p f eta.

    S&F's Eq. (10.17) prints k_inf = eta p f -- three factors -- and calls it the
    four-factor formula.  The book's own Tables 10.5 and 10.8 include eps: the
    water row of Table 10.5 is 0.888, which is 1.051 x 1.338 x 0.869 x 0.727 and
    not the 0.845 the printed equation gives.  eps defaults to 1 here so a
    fully-enriched or very dilute core (where eps really is 1) reproduces the
    book's examples unchanged."""
    for name, v in (("eta", eta), ("p", p), ("f", f), ("eps", eps)):
        if v < 0:
            raise ValueError("%s cannot be negative" % name)
    if not 0 <= p <= 1 or not 0 <= f <= 1:
        raise ValueError("p and f are probabilities")
    if eps < 1.0:
        raise ValueError("the fast fission factor cannot be below 1: it counts "
                         "fissions ADDED by fast neutrons")
    return eps * p * f * eta


def k_effective(eta, p, f, p_nl_fast, p_nl_thermal, eps=1.0):
    """The SIX-factor formula:  k_eff = eps p f eta P_NL^f P_NL^th
    [S&F Eq. (10.16), with eps restored]."""
    for name, v in (("P_NL^f", p_nl_fast), ("P_NL^th", p_nl_thermal)):
        if not 0 <= v <= 1:
            raise ValueError("%s is a probability" % name)
    return k_infinity(eta, p, f, eps) * p_nl_fast * p_nl_thermal


def four_factor_formula_as_printed(eta, p, f):
    """S&F Eq. (10.17) exactly as printed, WITHOUT eps.

    Kept so the difference can be measured rather than argued about; see
    `test_the_four_factor_formula_is_missing_epsilon`."""
    return eta * p * f


def reactivity(k):
    """rho = (k - 1)/k -- the natural measure of how far from critical."""
    if k <= 0:
        raise ValueError("k must be positive")
    return (k - 1.0) / k


def critical_buckling(k_inf, l2, tau, lo=1e-9, hi=1.0, tol=1e-14):
    """Solve k_inf exp(-B^2 tau)/(1 + L^2 B^2) = 1 for B^2, by bisection
    [S&F Example 10.5, which does it "by trial and error"].

    Refuses a subcritical material: if k_inf <= 1 no finite core is critical, and
    returning a buckling would be meaningless."""
    if k_inf <= 1.0:
        raise ValueError("k_inf = %.4f <= 1: no finite core of this material can "
                         "be critical, however large" % k_inf)
    if l2 < 0 or tau < 0:
        raise ValueError("diffusion area and Fermi age must be non-negative")

    def g(b2):
        return k_inf * math.exp(-b2 * tau) / (1.0 + l2 * b2) - 1.0

    if g(hi) > 0:
        raise ValueError("no root below B^2 = %g" % hi)
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if g(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def critical_radius_sphere(k_inf, l2, tau):
    """R = pi / sqrt(B_c^2) for a bare sphere  [S&F Example 10.5]."""
    return math.pi / math.sqrt(critical_buckling(k_inf, l2, tau))


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-19  the neutron life cycle\n")

    print("  Example 10.1: f for graphite + natural uranium, N_C/N_U = 450")
    abund = {"234U": 0.000055, "235U": 0.007204, "238U": 0.992745}
    sig_u = sum(a * FUEL_THERMAL_AVERAGED[k]["sigma_a"] for k, a in abund.items())
    sig_c = westcott_averaged_cross_section(0.00386)
    print("   Sigma_a^U/N = %.4f b, sigma_a^C(avg) = %.6f b" % (sig_u, sig_c))
    print("   f = %.4f   (book 0.8118)"
          % thermal_utilization_homogeneous(sig_u, sig_c, 450.0))

    print("\n  Example 10.2: eta for 2 atom-% enriched uranium")
    print("   eta = %.3f   (book 1.738)" % eta_of_uranium(0.02))
    print("   natural uranium: eta = %.3f   (Tables 10.5, 10.8 use 1.338/1.336)"
          % eta_of_uranium(0.007204))

    print("\n  Examples 10.3-10.6: a bare 235U/graphite sphere, 1:35 000")
    u5 = FUEL_THERMAL_AVERAGED["235U"]
    eta = thermal_fission_factor(FUEL_PROPERTIES["235U"][4], u5["sigma_f"],
                                 u5["sigma_a"])
    f = thermal_utilization_homogeneous(u5["sigma_a"], 0.00386, 35000.0)
    print("   eta = %.4f, f = %.4f, k_inf = %.4f   (book 2.080, 0.8143, 1.6939)"
          % (eta, f, k_infinity(eta, 1.0, f)))
    l2 = diffusion_length_squared(MODERATOR_THERMAL["C"]["L2"], f)
    tau = MODERATOR_THERMAL["C"]["tau"]
    b2 = geometric_buckling("sphere", R=120.0)
    print("   R = 120 cm: B^2 = %.4e, L^2 = %.1f cm2" % (b2, l2))
    print("   P_NL^f = %.4f, P_NL^th = %.4f   (book 0.7772, 0.7192)"
          % (fast_nonleakage(b2, tau), thermal_nonleakage(l2, b2)))
    r = critical_radius_sphere(k_infinity(eta, 1.0, f), l2, tau)
    print("   critical radius = %.1f cm   (book 126.7)" % r)
    mass = (4 / 3) * math.pi * r ** 3 * 1.60 * (1 / 35000.0) * (235.0 / 12.0)
    print("   235U mass = %.2f kg   (book 7.62)" % (mass / 1000.0))

    print("\n  Examples 10.7-10.8: natural uranium in water, N_W/N_U = 1.70")
    n238 = 0.992745 / 1.70
    print("   eps = %.4f   (book 1.0513)" % fast_fission_factor(n238))
    print("   p   = %.4f   (book 0.7270)"
          % resonance_escape_homogeneous(n238, "water"))

    print("\n  Table 10.5: optimum moderation for NATURAL uranium")
    print("   moderator  (N_M/N_U)opt   eps    eta     f      p     k_inf   3-factor")
    for m, (ratio, e, et, ff, p, k) in OPTIMUM_RATIOS.items():
        print("   %-9s %10.0f %8.3f %6.3f %6.3f %6.3f %7.3f %8.3f"
              % (m, ratio, e, et, ff, p, k_infinity(et, p, ff, e),
                 four_factor_formula_as_printed(et, p, ff)))
    print("   -> only D2O exceeds 1. That is why enrichment plants exist.")

    print("\n  Examples 10.9-10.10: a graphite lattice, 1.25 cm rods, 20 cm pitch")
    b = cell_radius(20.0)
    vm_vf = (20.0 ** 2 - math.pi * 1.25 ** 2) / (math.pi * 1.25 ** 2)
    print("   b = %.4f cm, V_M/V_F = %.3f" % (b, vm_vf))
    print("   F = %.4f, E = %.4f   (book 1.0792, 1.0307)"
          % (lattice_F(1.25 / 1.55), lattice_E(1.25 / 55.4, b / 55.4)))
    fl = thermal_utilization_lattice(0.000274, 0.3208, vm_vf, 1.25, b, 1.55, 55.4)
    print("   f = %.4f   (book 0.9051)" % fl)
    nf = 19.1 * AVOGADRO / 238.0289
    i = resonance_integral_rod(1.25, 19.1)
    pl = resonance_escape_lattice(nf, 1.0 / vm_vf, i)
    print("   N_F = %.5f /b-cm, I = %.4f b, p = %.5f   (book 0.04832, 10.638, 0.90028)"
          % (nf, i, pl))
    print("   k_inf = %.4f   (Table 10.8 at a = 20 cm: 1.118)"
          % k_infinity(1.336, pl, fl, 1.027))
    print("   the homogeneous mixture at the same ratio would have p = %.3f"
          % resonance_escape_homogeneous(0.992745 / (vm_vf * 1.0), "graphite"))


if __name__ == "__main__":
    _demo()
