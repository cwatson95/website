"""
constants.py  —  Constants module (cross-cutting, Thermo level)

Loads the machine-readable constant tables that the Thermo modules share:
  - gas_constants.csv : Moran Table 3.1 "Values of the gas constant R"
                        (printed p.128 / PDF 145), with molecular weights M.
  - constants.csv     : universal/physical constants (R-bar, g, atm, N_A, ...).

The defining relation R = R-bar / M (Moran Eq. 3.25) lets us verify the table
against itself: R * M should equal the universal gas constant for every
substance (see test_constants.py).

Usage:
    import constants as C
    C.gas_constant("Air")            # 0.2870 kJ/kg-K
    C.RBAR                           # 8.314 kJ/kmol-K
    C.constant("Standard atmosphere")  # 101.325
"""
import csv
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DIR = os.path.join(_HERE, os.pardir)

RBAR = 8.314          # universal gas constant, kJ/kmol-K  (Moran Eq. 3.22)


def _load(name):
    with open(os.path.join(_DIR, name)) as f:
        return list(csv.DictReader(f))


GAS = _load("gas_constants.csv")
CONST = _load("constants.csv")


def gas_constant(substance):
    """Specific gas constant R [kJ/kg-K] for a substance name (Table 3.1)."""
    for r in GAS:
        if r["substance"].lower() == substance.lower():
            return float(r["R_kJ_kgK"])
    raise KeyError(f"{substance!r} not in gas_constants.csv; have "
                   f"{[r['substance'] for r in GAS]}")


def molar_mass(substance):
    """Molecular weight M [kg/kmol] for a substance name."""
    for r in GAS:
        if r["substance"].lower() == substance.lower():
            return float(r["M_kg_kmol"])
    raise KeyError(substance)


def constant(name, units=None):
    """First value [float] in constants.csv matching name (and units if given)."""
    for r in CONST:
        if r["name"].lower() == name.lower() and (units is None or r["units"] == units):
            return float(r["value"])
    raise KeyError(f"{name!r} ({units}) not in constants.csv")


def _demo():
    print("Constants module — Moran Table 3.1 (gas constants) + universal constants\n")
    print(f"  R-bar = {RBAR} kJ/kmol-K;  check R*M for each substance:")
    for r in GAS:
        R, M = float(r["R_kJ_kgK"]), float(r["M_kg_kmol"])
        print(f"   {r['substance']:<16} R={R:.4f}  M={M:6.2f}  ->  R*M = {R*M:.3f}")


if __name__ == "__main__":
    _demo()
