"""PK-04  Atomic & molecular kinetics -- rate equations, excimer chemistry, EEDF.

Physics topic network, module PK-04 (modules/topic_network.txt).  Cross-links
~QO-03 (emission & laser physics), ~SM-06 (kinetic theory, <sigma v>) and
~PK-01 (the EEDF from the kinetic equation).

Sources (chapter/section level -- see ../refs.md):
  * Rhodes (ed.), *Excimer Lasers* (Topics in Applied Physics 30) -- the KrF
    reference: rare-gas-halide formation, the 248 nm B->X band, kinetics.
  * Michel, *Introduction to Laser-Plasma Interactions* -- atomic rates, the
    electron energy distribution function (EEDF), ionization (Saha).
  * The Maxwellian <sigma v> averaging is the kinetic-theory module ~SM-06.

This module is a teaching distillation of the user's own research code, the KrF
excimer-laser plasma-kinetics simulator in
    projects/Kinetic_Modeling/KrF_and_LoKI/KrF Code/factored-pyfiles/phantom11/
There a 0-D state vector u in R^26 packs LOG-transformed densities (n_e, kT, 23
species: Kr+, He*, Kr*, KrF*, Kr2*, Kr**, F-, F, F2, ...) plus a photon integral,
and  run_sim -> build_rhs_u -> rhs_u  integrates dn_i/dt = production - loss with
a stiff BDF/LSODA solver.  Electron-impact rate coefficients there are NOT
Maxwellian: they are k = <sigma v> averaged over a non-Maxwellian EEDF tabulated
by LoKI (LisbOn KInetics Monte Carlo) at E/N = CHOW_EN_TD_DEFAULT = 51 Td
(phantom11/loki_tables.py).  Here we use the Maxwellian average analytically so
the threshold -> Arrhenius story is transparent.

The excimer cartoon below uses the three dominant KrF* channels of phantom11:
  r25  Kr* + F2 -> KrF* + F          harpooning, K25 = 8.1e-10 cm^3/s  (Johnson & Hunter 1980)
  r31  KrF* -> Kr + F + h*nu (248 nm) radiative decay, tau_eff = 25 ns (coupled B+C state)
  r32  KrF* + F2 -> (quench) + ...    F2 collisional quenching, K32 = 3.0e-10 cm^3/s
plus an electron-impact pump  e + Kr -> Kr* + e  driven by a Gaussian discharge
pulse.  (phantom11 adds the ion channel Kr+ + F- + M -> KrF* + M and 20+ more.)
"""

import numpy as np
from scipy.integrate import quad, solve_ivp

__all__ = [
    # physical constants
    "K_B_J", "K_B_EV", "M_E", "E_CHARGE", "H_PLANCK", "C_LIGHT",
    # EEDF & rate coefficients
    "maxwell_energy_pdf", "rate_coefficient_maxwellian",
    "rate_coefficient_step_closed_form", "arrhenius",
    # ionization equilibrium
    "saha_ratio", "saha_ionization_fraction",
    # excimer 0-D kinetics
    "default_krf_params", "excimer_rhs", "simulate_krf", "photon_energy_eV",
]

# --- physical constants (SI, with eV companions) -----------------------------
K_B_J = 1.380649e-23        # Boltzmann constant [J/K]
K_B_EV = 8.617333262e-5     # Boltzmann constant [eV/K]
M_E = 9.1093837015e-31      # electron mass [kg]
E_CHARGE = 1.602176634e-19  # elementary charge [C]  (also J per eV)
H_PLANCK = 6.62607015e-34   # Planck constant [J s]
C_LIGHT = 2.99792458e8      # speed of light [m/s]


# =============================================================================
# 1.  The EEDF and the rate coefficient  k = <sigma v>
# =============================================================================

def maxwell_energy_pdf(E_eV, T):
    """Maxwellian electron energy distribution function (EEDF) F(E), per eV.

        F(E) = 2 sqrt(E/pi) (kT)^{-3/2} exp(-E/kT),   normalized  int F dE = 1,
    with mean energy <E> = (3/2) kT.  E in eV, T in K; returns 1/eV.  Real
    swarm solvers (LoKI) replace this with a non-Maxwellian F(E) (~PK-01)."""
    kT = K_B_EV * T                       # electron temperature in eV
    E = np.asarray(E_eV, dtype=float)
    out = 2.0 * np.sqrt(np.maximum(E, 0.0) / np.pi) * kT ** -1.5 * np.exp(-E / kT)
    return out


def rate_coefficient_maxwellian(T, sigma0, E_threshold, m=M_E):
    """Rate coefficient k = <sigma v> for a STEP (threshold) cross-section

        sigma(E) = sigma0  for E >= E_threshold,   else 0,

    averaged over a Maxwellian EEDF.  Done as the energy integral

        k = int_{Eth}^inf sigma0 * v(E) * F(E) dE,   v = sqrt(2E/m),

    which is the textbook  k = sqrt(8/(pi m)) (kT)^{-3/2} int sigma E e^{-E/kT} dE.
    T in K, sigma0 in m^2, E_threshold in eV, m in kg.  Returns m^3/s (>0, and
    increasing with T).  This is the Maxwellian counterpart of the LoKI EEDF
    average used in phantom11 (loki_tables.py)."""
    kT_J = K_B_J * T                      # thermal energy [J]
    Eth_J = E_threshold * E_CHARGE        # threshold [J]

    def integrand(E_J):                   # sigma0 * v(E) * F(E),  all in SI
        v = np.sqrt(2.0 * E_J / m)
        F = 2.0 * np.sqrt(E_J / np.pi) * kT_J ** -1.5 * np.exp(-E_J / kT_J)
        return sigma0 * v * F

    # the integrand decays as e^{-E/kT}; Eth + 60 kT is far into the tail
    val, _ = quad(integrand, Eth_J, Eth_J + 60.0 * kT_J, limit=200)
    return val


def rate_coefficient_step_closed_form(T, sigma0, E_threshold, m=M_E):
    """Closed form of the Maxwellian average of a step cross-section:

        k(T) = sigma0 <v> (1 + Eth/kT) exp(-Eth/kT),   <v> = sqrt(8kT/pi m).

    For Eth >> kT this is Arrhenius-like, k ~ exp(-Eth/kT): the threshold acts
    as an activation energy.  Used to validate `rate_coefficient_maxwellian`."""
    kT = K_B_J * T
    Eth = E_threshold * E_CHARGE
    v_bar = np.sqrt(8.0 * kT / (np.pi * m))
    return sigma0 * v_bar * (1.0 + Eth / kT) * np.exp(-Eth / kT)


def arrhenius(T, A, Ea):
    """Arrhenius rate law  k(T) = A exp(-Ea/kT).  T in K, Ea in eV, A in the
    units of the returned k.  The Maxwellian threshold average above reduces to
    this form, with the activation energy Ea set by the cross-section threshold."""
    return A * np.exp(-Ea / (K_B_EV * T))


# =============================================================================
# 2.  Ionization equilibrium -- detailed balance & the Saha equation
# =============================================================================

def saha_ratio(T, E_ion, g_i=1.0, g_0=1.0):
    """Saha ionization ratio (detailed balance of  A <-> A+ + e):

        n_e n_i / n_0 = (2 g_i/g_0)(2 pi m_e kT / h^2)^{3/2} exp(-E_ion/kT).

    The factor 2 is the electron spin degeneracy; (2 pi m_e kT/h^2)^{3/2} is the
    quantum concentration (inverse thermal-de-Broglie volume).  T in K, E_ion in
    eV; returns a number density [m^-3].  Increases steeply with T."""
    kT_J = K_B_J * T
    quantum_conc = (2.0 * np.pi * M_E * kT_J / H_PLANCK ** 2) ** 1.5
    return 2.0 * (g_i / g_0) * quantum_conc * np.exp(-E_ion / (K_B_EV * T))


def saha_ionization_fraction(T, n_total, E_ion, g_i=1.0, g_0=1.0):
    """Ionization fraction x = n_i/n_total from the Saha equation, assuming a
    single ionization stage with n_e = n_i and n_0 = n_total - n_i.  Solving

        x^2/(1 - x) = S/n_total,   S = saha_ratio(T, E_ion, ...),

    gives  x = (-R + sqrt(R^2 + 4R))/2  with R = S/n_total.  x -> 0 as T -> 0
    and x -> 1 as T -> inf; monotonically increasing in T."""
    S = saha_ratio(T, E_ion, g_i, g_0)
    R = S / n_total
    return 0.5 * (-R + np.sqrt(R * R + 4.0 * R))


# =============================================================================
# 3.  A 0-D KrF* excimer rate-equation system (the heart of phantom11)
# =============================================================================
#
# Species (number densities, m^-3):   y = [Kr, Krs, F2, F, KrFs, photons]
#   Kr   ground-state krypton            F2   molecular fluorine
#   Krs  excited Kr*                     F    atomic fluorine
#   KrFs the KrF* excimer                photons  cumulative 248 nm photons
#
# Reactions (production - loss):
#   R1 pump      Kr + e -> Kr* + e            r1 = k_pump * pulse(t) * Kr
#   R2 harpoon   Kr* + F2 -> KrF* + F         r2 = k_harpoon * Krs * F2   (r25)
#   R3 radiative KrF* -> Kr + F + h*nu(248)   r3 = A_rad * KrFs           (r31)
#   R4 quench    KrF* + F2 -> Kr + F + F2     r4 = k_quench * KrFs * F2   (r32)
#
# Conserved by construction (closed reactions):
#   Kr nuclei: Kr + Krs + KrFs            = const
#   F  nuclei: 2 F2 + F + KrFs            = const

def default_krf_params():
    """Authentic-scale parameters for the KrF* cartoon (cf. phantom11/reactions.py
    and config.py).  Rate coefficients in SI; 1 cm^3/s = 1e-6 m^3/s."""
    return dict(
        k_pump=2.0e6,        # effective e-impact pump frequency [1/s] (k_exc * n_e)
        k_harpoon=8.1e-16,   # r25  Kr* + F2 -> KrF* + F   (8.1e-10 cm^3/s)
        A_rad=1.0 / 25e-9,   # r31  KrF* -> Kr + F + hv     (tau_eff = 25 ns)
        k_quench=3.0e-16,    # r32  KrF* + F2 quenching     (3.0e-10 cm^3/s)
        t0=4.0e-8,           # pump-pulse centre [s]
        tau_p=1.5e-8,        # pump-pulse 1/e half-width [s]
        Kr0=1.0e24,          # initial Kr density [m^-3]
        F2_0=2.0e23,         # initial F2 density [m^-3]
    )


def _pump_pulse(t, t0, tau_p):
    """Gaussian discharge/e-beam pump shape (dimensionless, peak 1).  In the real
    simulator this current pulse also sets n_e and the reduced field E/N that
    indexes the LoKI EEDF tables (CHOW_EN_TD_DEFAULT = 51 Td)."""
    return np.exp(-((t - t0) / tau_p) ** 2)


def excimer_rhs(t, y, p):
    """Right-hand side dy/dt of the 0-D KrF* system; mirrors phantom11's
    rhs_u(t, u) = production - loss (but in linear, not log-packed, densities).
    y = [Kr, Krs, F2, F, KrFs, photons]; p a params dict."""
    Kr, Krs, F2, F, KrFs, _photons = y
    r1 = p["k_pump"] * _pump_pulse(t, p["t0"], p["tau_p"]) * Kr   # e-impact pump
    r2 = p["k_harpoon"] * Krs * F2                                # harpoon -> KrF*
    r3 = p["A_rad"] * KrFs                                        # radiative (248 nm)
    r4 = p["k_quench"] * KrFs * F2                                # F2 quench
    dKr = -r1 + r3 + r4
    dKrs = r1 - r2
    dF2 = -r2
    dF = r2 + r3 + r4
    dKrFs = r2 - r3 - r4
    dphotons = r3                                                 # spontaneous 248 nm
    return [dKr, dKrs, dF2, dF, dKrFs, dphotons]


def simulate_krf(params=None, t_end=2.0e-7, n_points=400):
    """Integrate the 0-D KrF* excimer kinetics with scipy.integrate.solve_ivp
    (stiff LSODA, as in phantom11/sim_0d.py).  Returns a dict of time series:
    't', 'Kr', 'Krs', 'F2', 'F', 'KrFs', 'photons', plus the conserved nuclei
    inventories 'kr_nuclei', 'f_nuclei', and the peak KrF* value/time.

    KrF* rises to a peak (formation outrunning decay during the pump) then decays
    away; the heavy-particle (atom) inventories are conserved to solver tolerance."""
    p = default_krf_params() if params is None else dict(params)
    y0 = [p["Kr0"], 0.0, p["F2_0"], 0.0, 0.0, 0.0]   # Kr, Krs, F2, F, KrFs, photons
    t_eval = np.linspace(0.0, t_end, n_points)
    sol = solve_ivp(excimer_rhs, (0.0, t_end), y0, args=(p,), method="LSODA",
                    t_eval=t_eval, rtol=1e-10, atol=1e4)
    if not sol.success:
        raise RuntimeError("solve_ivp failed: " + sol.message)
    Kr, Krs, F2, F, KrFs, photons = sol.y
    ipk = int(np.argmax(KrFs))
    return dict(
        t=sol.t, Kr=Kr, Krs=Krs, F2=F2, F=F, KrFs=KrFs, photons=photons,
        kr_nuclei=Kr + Krs + KrFs,            # conserved
        f_nuclei=2.0 * F2 + F + KrFs,         # conserved
        peak_KrFs=float(KrFs[ipk]), peak_time=float(sol.t[ipk]),
    )


def photon_energy_eV(wavelength_nm=248.0):
    """Photon energy E = h c / lambda in eV.  For the KrF* B->X band at 248 nm
    this is ~5.0 eV (phantom11/config.py uses Ehnu = 4.999 eV).  Because the
    lower (Kr + F) state is repulsive, KrF* has no ground-state reabsorption ->
    automatic population inversion and 248 nm laser gain (~QO-03)."""
    lam = wavelength_nm * 1e-9
    return H_PLANCK * C_LIGHT / lam / E_CHARGE


# =============================================================================
# demo
# =============================================================================

def _demo():
    print("PK-04  Atomic & molecular kinetics -- demo")
    print("=" * 52)

    # 1) rate coefficient vs T for an electron-impact threshold process
    #    (e.g. e + Kr -> Kr* + e, excitation threshold ~9.9 eV)
    print("\n1) Maxwellian rate coefficient k = <sigma v> for a step")
    print("   cross-section (sigma0 = 1e-20 m^2, threshold = 9.9 eV):")
    print("     T [K]     kT [eV]    k [m^3/s]   (rises with T)")
    sigma0, Eth = 1.0e-20, 9.9
    for T in (1.0e4, 2.0e4, 3.0e4, 5.0e4):
        k = rate_coefficient_maxwellian(T, sigma0, Eth)
        print(f"   {T:8.0f}   {K_B_EV*T:7.3f}    {k:.3e}")

    # 2) Saha ionization fraction vs T (krypton, E_ion = 14.0 eV, 1e24 /m^3)
    print("\n2) Saha ionization fraction (Kr, E_ion = 14.0 eV, n = 1e24 /m^3):")
    print("     T [K]     x = n_i/n_tot   (rises with T)")
    for T in (1.0e4, 1.5e4, 2.0e4, 3.0e4):
        x = saha_ionization_fraction(T, 1.0e24, 14.0)
        print(f"   {T:8.0f}      {x:.4e}")

    # 3) the 0-D KrF* excimer pulse
    print("\n3) 0-D KrF* excimer kinetics (harpoon + radiative + F2 quench):")
    res = simulate_krf()
    print(f"   KrF* peak  = {res['peak_KrFs']:.3e} m^-3  at t = {res['peak_time']*1e9:.1f} ns")
    print(f"   KrF* end   = {res['KrFs'][-1]:.3e} m^-3  (decayed away after the pump)")
    kr0, krN = res["kr_nuclei"][0], res["kr_nuclei"][-1]
    f0, fN = res["f_nuclei"][0], res["f_nuclei"][-1]
    print(f"   Kr nuclei  conserved: {kr0:.6e} -> {krN:.6e}  (rel dev {abs(krN/kr0-1):.1e})")
    print(f"   F  nuclei  conserved: {f0:.6e} -> {fN:.6e}  (rel dev {abs(fN/f0-1):.1e})")
    print(f"   photons emitted (248 nm): {res['photons'][-1]:.3e} m^-3")
    print(f"   248 nm photon energy = {photon_energy_eV(248.0):.3f} eV  (KrF* B->X, ~QO-03)")


if __name__ == "__main__":
    _demo()
