"""NE-23  The nuclear fuel cycle: enrichment & SWU, burnup, spent fuel, waste.

Nuclear Science & Engineering trunk, module NE-23 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 11.7-11.8 (printed pp. 410-424).  Pure stdlib.

~NE-22 ran the reactor.  This module follows the material: 150 tonnes of natural
uranium a year in at one end, 26 tonnes of spent fuel out at the other, and a
waste problem measured in hundreds of thousands of years.

Three quantitative things carry the chapter, and only the first is in S&F.

  * THE MASS BALANCE.  Table 11.7 is a complete annual flowsheet for a 1000
    MW(e) PWR, and it closes: enrichment product plus tails equals feed to the
    kilogram, and the 873 kg of fission products it reports corresponds to 277
    full-power days, against the 274 days its own 75% capacity factor implies.

  * SEPARATIVE WORK.  S&F describe five enrichment technologies and never write
    down the quantity they are all measured in.  The separative work unit follows
    from one value function,

        V(x) = (2x - 1) ln[x/(1-x)] ,

    and Table 11.7's own numbers give 116 tSWU/y -- squarely in the industry
    range for a 1000 MW(e) PWR.  It also exposes the optimum tails assay, which
    is an economic choice and not a physical constant.

  * THE ATOM-PERCENT TRAP.  Natural uranium is 0.7204 ATOM-% 235U and 0.711
    WEIGHT-% 235U, and enrichment arithmetic uses weight fractions throughout.
    Using 0.7204 in a cascade calculation is a 1.8% error in the feed
    requirement, which is millions of dollars a year on one reactor -- and
    Table 11.7 is consistent to 0.13% with the weight fraction and not with the
    atom fraction, which is how one can tell.

Table 11.8's spent-fuel composition then closes exactly as a heavy-atom balance,
and shows that 43% of the fissions in a discharged LWR fuel assembly came from
plutonium that was not there when the fuel was loaded.
"""

import math

__all__ = [
    "U235_ATOM_PERCENT", "U235_WEIGHT_FRACTION", "M_U235", "M_U238",
    "ANNUAL_FLOWS", "SPENT_FUEL_ATOM_PERCENT", "NEW_FUEL_ATOM_PERCENT",
    "WASTE_CLASSES", "LONG_LIVED_FISSION_PRODUCTS", "ENRICHMENT_TECHNOLOGIES",
    "atom_to_weight_fraction", "weight_to_atom_fraction",
    "value_function", "separative_work", "feed_per_product",
    "tails_per_product", "swu_per_product", "optimal_tails_assay",
    "cascade_balance", "burnup_from_fissioned_fraction",
    "fission_energy_from_mass", "plutonium_fission_fraction",
    "fission_product_activity_fraction", "years_to_ore_activity",
    "natural_uranium_per_year", "lifetime_uranium",
]

# --- natural uranium: the two percentages that are not the same -------------
U235_ATOM_PERCENT = 0.7204          # S&F §11.7, and Appendix A.4
U234_ATOM_PERCENT = 0.0055
M_U234, M_U235, M_U238 = 234.0409, 235.0439, 238.0508


def atom_to_weight_fraction(atom_fraction, m_light=M_U235, m_heavy=M_U238):
    """Convert an isotopic ATOM fraction to a WEIGHT fraction.

    For natural uranium: 0.7204 atom-% is 0.711 weight-%.  Every enrichment
    calculation in the industry -- feed, product, tails, SWU -- uses WEIGHT
    fractions, and substituting the atom percent is a systematic 1.8% error in
    the feed requirement."""
    if not 0 <= atom_fraction <= 1:
        raise ValueError("atom fraction must lie in [0, 1]")
    return (atom_fraction * m_light
            / (atom_fraction * m_light + (1 - atom_fraction) * m_heavy))


def weight_to_atom_fraction(weight_fraction, m_light=M_U235, m_heavy=M_U238):
    """The inverse of `atom_to_weight_fraction`."""
    if not 0 <= weight_fraction <= 1:
        raise ValueError("weight fraction must lie in [0, 1]")
    return (weight_fraction / m_light
            / (weight_fraction / m_light + (1 - weight_fraction) / m_heavy))


U235_WEIGHT_FRACTION = atom_to_weight_fraction(U235_ATOM_PERCENT / 100.0)


# --- Table 11.7 (printed p. 411): annual flows for a 1000 MW(e) PWR ---------
# kg, at a 0.75 capacity factor and 0.2% tails.
ANNUAL_FLOWS = {
    "U in U3O8 (mining/milling)": 150047.0,
    "U in UF6 (conversion)": 149297.0,
    "235U (enrichment product)": 821.0,
    "238U (enrichment product)": 27249.0,
    "U tails at 0.2%": 121227.0,
    "235U discharged": 220.0,
    "U discharged": 25858.0,
    "fissile Pu discharged": 178.0,
    "total Pu discharged": 246.0,
    "U + Pu discharged": 26104.0,
    "fission products": 873.0,
}
CAPACITY_FACTOR = 0.75
TAILS_ASSAY = 0.002

# --- Table 11.8 (printed p. 417): LWR fuel before and after, atom-% ---------
NEW_FUEL_ATOM_PERCENT = {"238U": 96.7, "235U": 3.3}
SPENT_FUEL_ATOM_PERCENT = {
    "238U": 94.3, "235U": 0.81, "236U": 0.51,
    "239Pu": 0.52, "240Pu": 0.21, "241Pu": 0.10, "242Pu": 0.05,
    "fission products": 3.5,
}

# --- §11.7.4: the fission products that outlive a human lifetime ------------
# nuclide -> half-life in years
LONG_LIVED_FISSION_PRODUCTS = {
    "90Sr": 29.1, "137Cs": 30.2, "99Tc": 0.21e6, "79Se": 1.1e6,
    "93Zr": 1.5e6, "135Cs": 2.3e6, "129I": 16e6,
}

# --- §11.7.3: the waste classes ---------------------------------------------
WASTE_CLASSES = {
    "HLW": "fission products separated in reprocessing; in the once-through "
           "cycle, spent fuel itself",
    "TRU": "plutonium and higher actinides above 100 nCi/g, chiefly from "
           "reprocessing",
    "mill tailings": "low activity, large volume; the concern is radon",
    "LLW": "under 100 nCi/g of actinides and low enough activity that handling "
           "needs no shielding",
    "ILW": "everything else; needs shielding but is not HLW",
}

# --- §11.7.2: the five enrichment technologies ------------------------------
ENRICHMENT_TECHNOLOGIES = {
    "gaseous diffusion": {"basis": "lighter molecules strike a porous membrane "
                                   "more often", "stages": "hundreds",
                          "energy": "very high", "status": "largely retired"},
    "gas centrifuge": {"basis": "centrifugal separation by molecular mass",
                       "stages": "cascades", "energy": "a few percent of "
                       "diffusion", "status": "dominant"},
    "aerodynamic": {"basis": "curved nozzle or vortex tube",
                    "stages": "cascades", "energy": "high",
                    "status": "demonstrated, uneconomic"},
    "electromagnetic": {"basis": "magnetic deflection of accelerated ions",
                        "stages": "one", "energy": "very high",
                        "status": "Manhattan Project; now only for medical "
                        "isotopes"},
    "laser (AVLIS/SILEX)": {"basis": "the 49 ueV isotope shift in an electronic "
                            "level", "stages": "one or few",
                            "energy": "low in principle",
                            "status": "under development"},
}


# --- enrichment and separative work  [beyond S&F §11.7.2] -------------------

def value_function(x):
    """V(x) = (2x - 1) ln[x/(1-x)], the separative-work value function.

    S&F describe five enrichment technologies and never state the quantity that
    measures them.  V is dimensionless, symmetric about x = 1/2 where it
    vanishes, and rises steeply toward both extremes -- which is the statement
    that separating a nearly pure stream is expensive whichever end you are at."""
    if not 0 < x < 1:
        raise ValueError("an assay must lie strictly in (0, 1)")
    return (2.0 * x - 1.0) * math.log(x / (1.0 - x))


def feed_per_product(x_f, x_p, x_t):
    """F/P = (x_p - x_t)/(x_f - x_t), from the mass and 235U balances.

    REFUSES a cascade that cannot exist: the tails must be leaner than the feed
    and the product richer, or the two balance equations have no positive
    solution."""
    if not 0 < x_t < x_f < x_p < 1:
        raise ValueError("need 0 < x_t < x_f < x_p < 1; got tails %.5f, feed "
                         "%.5f, product %.5f. A cascade cannot enrich below its "
                         "feed or leave tails richer than its feed."
                         % (x_t, x_f, x_p))
    return (x_p - x_t) / (x_f - x_t)


def tails_per_product(x_f, x_p, x_t):
    """T/P = (x_p - x_f)/(x_f - x_t)."""
    return feed_per_product(x_f, x_p, x_t) - 1.0


def separative_work(product_kg, x_f, x_p, x_t):
    """Separative work, kg-SWU, for a given mass of product.

        SWU = P V(x_p) + T V(x_t) - F V(x_f)

    This is the quantity enrichment is sold in, and it is not energy: it is a
    measure of how much the isotopic mixture has been un-mixed.  A 1000 MW(e)
    PWR needs about 116 tSWU a year."""
    if product_kg < 0:
        raise ValueError("product mass cannot be negative")
    f = feed_per_product(x_f, x_p, x_t) * product_kg
    t = tails_per_product(x_f, x_p, x_t) * product_kg
    return (product_kg * value_function(x_p) + t * value_function(x_t)
            - f * value_function(x_f))


def swu_per_product(x_f, x_p, x_t):
    """Separative work per kilogram of product."""
    return separative_work(1.0, x_f, x_p, x_t)


def optimal_tails_assay(x_f, x_p, feed_cost_per_kg, swu_cost,
                        lo=1e-4, hi=None, n=20000):
    """The tails assay minimising total cost, given a uranium price and a SWU
    price.  Beyond S&F entirely.

    The tails assay is an ECONOMIC choice, not a physical constant.  Leaner
    tails need less uranium and more separative work; richer tails the reverse.
    When uranium is cheap relative to enrichment, plants run richer tails and
    throw more 235U away -- which is why the "0.2%" of Table 11.7 is a
    convention of its era and not a law."""
    if feed_cost_per_kg <= 0 or swu_cost <= 0:
        raise ValueError("prices must be positive")
    hi = x_f * 0.98 if hi is None else hi
    best, best_x = None, None
    for i in range(1, n):
        x_t = lo + (hi - lo) * i / n
        cost = (feed_per_product(x_f, x_p, x_t) * feed_cost_per_kg
                + swu_per_product(x_f, x_p, x_t) * swu_cost)
        if best is None or cost < best:
            best, best_x = cost, x_t
    return best_x, best


def cascade_balance(feed_kg, x_f, x_p, x_t):
    """(product kg, tails kg), from the two balance equations."""
    ratio = feed_per_product(x_f, x_p, x_t)
    p = feed_kg / ratio
    return p, feed_kg - p


# --- burnup and spent fuel  [S&F Table 11.8] --------------------------------

def burnup_from_fissioned_fraction(atom_percent_fissioned, m_fuel=235.0):
    """Burnup in GWd per tonne of heavy metal, from the fraction of heavy atoms
    that fissioned.

    3.5% -- Table 11.8's fission-product entry -- gives 33.3 GWd/tU, which is
    Table 11.2's printed discharge burnup.  Two tables six chapters apart, and
    they agree to 1%."""
    if not 0 <= atom_percent_fissioned <= 100:
        raise ValueError("the fissioned fraction must be a percentage")
    kg_per_tonne = 10.0 * atom_percent_fissioned         # kg fissioned per tonne
    return fission_energy_from_mass(kg_per_tonne, m_fuel) / 1e3


def fission_energy_from_mass(kg_fissioned, m_fuel=235.0, mev_per_fission=200.0):
    """Energy released, MWd, by fissioning a given mass of heavy metal."""
    if kg_fissioned < 0:
        raise ValueError("mass cannot be negative")
    fissions = kg_fissioned * 1e3 / m_fuel * 6.022e23
    joules = fissions * mev_per_fission * 1.602e-13
    return joules / 86400.0 / 1e6


def plutonium_fission_fraction(new=None, spent=None):
    """What fraction of the fissions in a discharged fuel assembly came from
    plutonium, from Table 11.8's heavy-atom balance.

    The accounting closes exactly:
      235U consumed 2.49 = 0.51 captured to 236U + 1.98 fissioned
      238U consumed 2.40 = 0.88 Pu remaining + 1.52 Pu fissioned
      total fissions 1.98 + 1.52 = 3.50 = the printed fission-product entry.

    So 43% of the energy came from an element that was not in the fuel when it
    was loaded -- which is what S&F's §11.1 means by "almost half the power" at
    end of life, and the reason a reactor's reactivity does not simply decay."""
    new = NEW_FUEL_ATOM_PERCENT if new is None else new
    spent = SPENT_FUEL_ATOM_PERCENT if spent is None else spent
    u5_burned = new["235U"] - spent["235U"]
    u5_fissioned = u5_burned - spent.get("236U", 0.0)
    pu_left = sum(v for k, v in spent.items() if k.endswith("Pu"))
    u8_burned = new["238U"] - spent["238U"]
    pu_fissioned = u8_burned - pu_left
    total = u5_fissioned + pu_fissioned
    if total <= 0:
        raise ValueError("no net fissions in this balance")
    return pu_fissioned / total


# --- waste  [S&F §11.7.4] ---------------------------------------------------

def fission_product_activity_fraction(years, half_life_y=30.0):
    """Fraction of the initial fission-product activity remaining.

    S&F's estimate: after 1000 years, exp[-(1000 ln2)/30] = 1e-10, "an activity
    less than the ore from which the uranium was extracted".  The long-term
    activity is set almost entirely by 137Cs (30.2 y) and 90Sr (29.1 y) -- the
    other five long-lived fission products have million-year half-lives and are
    therefore effectively stable and effectively inert."""
    if years < 0 or half_life_y <= 0:
        raise ValueError("time and half-life must be positive")
    return math.exp(-years * math.log(2.0) / half_life_y)


def years_to_ore_activity(target=1e-10, half_life_y=30.0):
    """Years for the fission-product activity to fall by `target`.

    ~1000 years for 1e-10.  The actinides are the other problem entirely: 239Pu's
    24 000-year half-life needs isolation for several hundred thousand years,
    which is why reprocessing -- separating the actinides back into fuel --
    changes the disposal problem by a factor of a few hundred in time."""
    if not 0 < target < 1:
        raise ValueError("the target must lie in (0, 1)")
    return -math.log(target) * half_life_y / math.log(2.0)


def natural_uranium_per_year(x_f=None, x_p=0.03, x_t=TAILS_ASSAY,
                             product_kg=28070.0):
    """Natural uranium needed per year, kg, for a given annual fuel loading."""
    x_f = U235_WEIGHT_FRACTION if x_f is None else x_f
    return feed_per_product(x_f, x_p, x_t) * product_kg


def lifetime_uranium(annual_kg, years=30.0):
    """Lifetime natural-uranium requirement, tonnes."""
    return annual_kg * years / 1e3


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-23  the nuclear fuel cycle\n")

    print("  the two percentages that are not the same")
    print("   natural uranium: %.4f atom-%%  ->  %.4f weight-%%"
          % (U235_ATOM_PERCENT, 100 * U235_WEIGHT_FRACTION))
    print("   enrichment arithmetic uses WEIGHT fractions throughout")
    a = feed_per_product(U235_WEIGHT_FRACTION, 0.03, 0.002)
    b = feed_per_product(U235_ATOM_PERCENT / 100, 0.03, 0.002)
    print("   feed per kg product: %.4f (weight) vs %.4f (atom) -- %.1f%% apart"
          % (a, b, 100 * (a / b - 1)))

    print("\n  Table 11.7 checks against itself")
    f = ANNUAL_FLOWS["U in UF6 (conversion)"]
    p = ANNUAL_FLOWS["235U (enrichment product)"] + ANNUAL_FLOWS["238U (enrichment product)"]
    t = ANNUAL_FLOWS["U tails at 0.2%"]
    x_p = ANNUAL_FLOWS["235U (enrichment product)"] / p
    print("   product %.0f + tails %.0f = %.0f, feed %.0f  (difference %.0f kg)"
          % (p, t, p + t, f, f - p - t))
    print("   product assay %.4f%%; feed assay implied %.4f%% (natural is %.4f wt-%%)"
          % (100 * x_p, 100 * (p * x_p + t * 0.002) / f, 100 * U235_WEIGHT_FRACTION))
    print("   F/P = %.3f measured, %.3f from the balance equations"
          % (f / p, feed_per_product(U235_WEIGHT_FRACTION, x_p, 0.002)))

    print("\n  separative work -- the quantity S&F never name")
    swu = separative_work(p, U235_WEIGHT_FRACTION, x_p, 0.002)
    print("   %.0f kg-SWU/y = %.1f tSWU/y for this reactor" % (swu, swu / 1e3))
    print("   %.3f SWU per kg of product" % (swu / p))
    print("   assay   V(x)")
    for x in (0.002, 0.00711, 0.03, 0.05, 0.20, 0.90, 0.99):
        print("   %6.3f %8.4f" % (x, value_function(x)))
    print("   -> V vanishes at x = 0.5 and diverges at both ends: purity is")
    print("      expensive whichever end of the mixture you want.")

    print("\n  the tails assay is an economic choice, not a constant")
    print("   U price   SWU price   optimal tails   feed/product   SWU/kg")
    for u, s in ((50.0, 100.0), (100.0, 100.0), (250.0, 100.0), (100.0, 50.0)):
        xt, cost = optimal_tails_assay(U235_WEIGHT_FRACTION, 0.045, u, s)
        print("   $%-8.0f $%-10.0f %10.4f%% %13.2f %8.2f"
              % (u, s, 100 * xt, feed_per_product(U235_WEIGHT_FRACTION, 0.045, xt),
                 swu_per_product(U235_WEIGHT_FRACTION, 0.045, xt)))
    print("   -> dear uranium buys leaner tails; dear enrichment buys richer.")

    print("\n  Table 11.8: where the energy actually came from")
    print("   235U consumed %.2f = %.2f -> 236U + %.2f fissioned"
          % (NEW_FUEL_ATOM_PERCENT["235U"] - SPENT_FUEL_ATOM_PERCENT["235U"],
             SPENT_FUEL_ATOM_PERCENT["236U"],
             NEW_FUEL_ATOM_PERCENT["235U"] - SPENT_FUEL_ATOM_PERCENT["235U"]
             - SPENT_FUEL_ATOM_PERCENT["236U"]))
    pu_left = sum(v for k, v in SPENT_FUEL_ATOM_PERCENT.items() if k.endswith("Pu"))
    u8 = NEW_FUEL_ATOM_PERCENT["238U"] - SPENT_FUEL_ATOM_PERCENT["238U"]
    print("   238U consumed %.2f = %.2f Pu left + %.2f Pu fissioned"
          % (u8, pu_left, u8 - pu_left))
    print("   total fissions %.2f, printed fission products %.2f"
          % (1.98 + (u8 - pu_left), SPENT_FUEL_ATOM_PERCENT["fission products"]))
    print("   plutonium's share of the energy: %.0f%%"
          % (100 * plutonium_fission_fraction()))
    print("   burnup from 3.5%% fissioned: %.1f GWd/tU  (Table 11.2 prints 33)"
          % burnup_from_fissioned_fraction(3.5))

    print("\n  waste: two problems on two timescales  [§11.7.4]")
    print("   years    fission-product activity")
    for y in (1, 30, 100, 300, 1000):
        print("   %6d %20.3e" % (y, fission_product_activity_fraction(y)))
    print("   -> below ore activity in %.0f years" % years_to_ore_activity())
    print("   but 239Pu's 24 000-y half-life needs several hundred thousand,")
    print("   which is the whole argument for separating the actinides.")
    print("   long-lived fission products (>25 y):")
    for k, v in sorted(LONG_LIVED_FISSION_PRODUCTS.items(), key=lambda kv: kv[1]):
        print("     %-6s %10.3g y%s" % (k, v, "  <- sets the 1000-y number"
                                        if v < 100 else "  (effectively stable)"))


if __name__ == "__main__":
    _demo()
