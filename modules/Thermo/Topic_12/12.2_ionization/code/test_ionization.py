"""test_ionization.py — checks for Module 12.2.  Run: python3 test_ionization.py
(A) Moran Ch.14 equilibrium-constant pieces against Examples 14.1, 14.2 (book numbers).
(B) Saha extension [~PK, NOT Moran]: physical-consistency + literature de Broglie value."""
import math
from ionization import (delta_nu, equilibrium_constant_from_composition, gibbs_of_reaction,
                        lnK_from_gibbs, K_from_gibbs, log10K_from_gibbs, log10K_inverse,
                        equilibrium_constant_CO_oxidation, dissociation_extent_CO2,
                        thermal_debroglie_wavelength, quantum_concentration, saha_rhs,
                        saha_ionization_fraction, saha_electron_density)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# ===== (A) MORAN: equilibrium constant (Ch.14) =====
# stoichiometry exponent dnu for CO + 1/2 O2 -> CO2 : 1 - (1 + 1/2) = -1/2
chk("dnu CO oxidation", delta_nu([1], [1, 0.5]), -0.5)

# Example 14.1 -- K for CO + 1/2 O2 <-> CO2
r298 = equilibrium_constant_CO_oxidation(298)
chk("Ex14.1 dG0 @298K", r298["dG0"], -257253.0, 60.0)        # book -257,253 kJ/kmol
chk("Ex14.1 lnK @298K", r298["lnK"], 103.83, 0.02)           # book 103.83
chk("Ex14.1 log10K @298K", r298["log10K"], 45.093, 0.02)     # book 45.093
r2000 = equilibrium_constant_CO_oxidation(2000)
chk("Ex14.1 dG0 @2000K", r2000["dG0"], -110453.0, 60.0)      # book -110,453 kJ/kmol
chk("Ex14.1 lnK @2000K", r2000["lnK"], 6.643, 0.01)          # book 6.643
chk("Ex14.1 log10K @2000K", r2000["log10K"], 2.885, 0.01)    # book 2.885
# Table A-27 tabulates the INVERSE reaction CO2 -> CO + 1/2 O2: log10 K* = -log10 K
chk("Ex14.1 log10K* (inverse)", log10K_inverse(r2000["log10K"]), -2.885, 0.01)

# generic Gibbs/K helpers round-trip
dG = gibbs_of_reaction([(1, -393520.0, 213.69)],
                       [(1, -110530.0, 197.54), (0.5, 0.0, 205.03)], 298.0)
chk("gibbs_of_reaction == Ex14.1", dG, -257253.0, 60.0)
chk("K from gibbs", K_from_gibbs(dG, 298.0), math.exp(103.83), math.exp(103.83) * 1e-2)
chk("log10K consistency", log10K_from_gibbs(dG, 298.0), lnK_from_gibbs(dG, 298.0) / math.log(10), 1e-9)

# Example 14.2 -- CO2 dissociation extent at 2500 K (K = 0.0363 for CO2 -> CO + 1/2 O2)
chk("Ex14.2 z @1 atm", dissociation_extent_CO2(0.0363, 1.0), 0.129, 1e-3)       # book 0.129
chk("Ex14.2 z @10 atm", dissociation_extent_CO2(0.0363, 10.0), 0.062, 2e-3)     # book 0.062
# Example 14.4 -- inert N2 (1.88 kmol) at 1 atm raises dissociation: z = 0.175
chk("Ex14.4 z with 1.88 N2", dissociation_extent_CO2(0.0363, 1.0, n_inert=1.88), 0.175, 2e-3)
# resulting mole fractions reproduce Ex 14.2(a): yCO=0.121, yO2=0.061, yCO2=0.818
z = dissociation_extent_CO2(0.0363, 1.0)
nt = (2.0 + z) / 2.0
chk("Ex14.2 yCO", (z) / nt, 0.121, 2e-3)
chk("Ex14.2 yO2", (z / 2.0) / nt, 0.061, 2e-3)
chk("Ex14.2 yCO2", (1.0 - z) / nt, 0.818, 2e-3)
# K recovered from those equilibrium mole fractions (Eq. 14.32) matches input K
Krec = equilibrium_constant_from_composition(
    [(z / nt, 1.0), ((z / 2.0) / nt, 0.5)], [((1.0 - z) / nt, 1.0)], 1.0)
chk("Eq14.32 K round trip", Krec, 0.0363, 5e-4)

# ===== (B) SAHA extension [~PK, NOT Moran]: consistency + literature value =====
chk("e- de Broglie @300K (nm)", thermal_debroglie_wavelength(300.0) * 1e9, 4.30, 0.02)  # lit ~4.30 nm
chk("n_Q = 1/lambda^3", quantum_concentration(300.0),
    thermal_debroglie_wavelength(300.0) ** -3, 1e15)
# Saha RHS rises with T (Boltzmann + quantum-concentration factors)
assert saha_rhs(12000.0, 13.6) > saha_rhs(6000.0, 13.6) > 0.0;  _n += 1
# ionization fraction is bounded and monotonic in T and in density
xa = saha_ionization_fraction(10000.0, 1.0e23, 13.6)
assert 0.0 < xa < 1.0;  _n += 1
assert saha_ionization_fraction(20000.0, 1.0e23, 13.6) > xa;  _n += 1   # hotter -> more ionized
assert saha_ionization_fraction(10000.0, 1.0e25, 13.6) < xa;  _n += 1   # denser -> less ionized
# limits: x -> 1 as T huge, x -> 0 as T small
chk("Saha x -> 1 (very hot)", saha_ionization_fraction(1.0e6, 1.0e20, 13.6), 1.0, 1e-3)
assert saha_ionization_fraction(2000.0, 1.0e23, 13.6) < 1e-6;  _n += 1
# n_e = x * n_total
chk("Saha n_e = x n", saha_electron_density(10000.0, 1.0e23, 13.6), xa * 1.0e23, 1.0)

print(f"All {_n} tests passed.")
