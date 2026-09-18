"""QO-03  Emission & coherence -- Einstein A/B, laser threshold, g^(2)(0).

Physics topic network, module QO-03 (modules/topic_network.txt).
Source: Scully & Zubairy, *Quantum Optics* (Cambridge, 1997) -- the black-body /
Planck / Einstein introduction (Ch. 1), the physical picture of stimulated
emission and absorption (Sect. 5.6), the Weisskopf-Wigner spontaneous-emission
rate (Sect. 6.3), semiclassical and quantum laser theory (Sect. 5.5, Ch. 11),
and the first/second-order coherence functions (Ch. 4, Sects. 4.2-4.4).
Bridges ~QM-16 (time-dependent perturbation: the emission/absorption rate) and
~PK-04 (excimer/laser kinetics: the photon side of KrF* chemistry); neighbour
~QO-02 (atom-field interaction, Rabi/Jaynes-Cummings).

Three threads, each a self-contained closed form:

1. Einstein A & B coefficients.  In thermal equilibrium an atom with levels
   1 (lower) and 2 (upper) exchanges photons with a radiation field of spectral
   energy density rho(nu) by three processes: spontaneous emission (rate A21),
   stimulated emission (B21 rho) and absorption (B12 rho).  Detailed balance
   against the Boltzmann populations forces rho(nu) to be the *Planck* spectrum
   only if the Einstein relations hold:
       A21/B21 = 8 pi h nu^3 / c^3 ,     g1 B12 = g2 B21 .
   The ratio of stimulated to spontaneous emission in equilibrium is then
       B21 rho / A21 = 1 / (exp(h nu / kB T) - 1) ,
   tiny at optical frequencies & room T (why lasers need an inversion, not heat).

2. Laser threshold.  The single-mode rate equations for inversion N and photon
   number n,  Ndot = R - gamma N - G N n ,  ndot = G N n - kappa n , have a sharp
   *threshold* pump R_th = gamma kappa / G: below it n = 0 and N rises with pump;
   above it the gain *clamps* the inversion at N_th = kappa/G and the extra pump
   converts to photons, n = (R - R_th)/kappa.

3. Coherence.  The normalized second-order correlation at zero delay,
   g2(0) = <n(n-1)>/<n>^2, classifies light: thermal/chaotic = 2 (bunching),
   coherent/laser = 1 (Poissonian), and a single-photon Fock state = 0
   (antibunching, g2_fock(n) = 1 - 1/n).
"""

import numpy as np

__all__ = [
    "H_PLANCK", "C_LIGHT", "K_B",
    "einstein_A_over_B", "planck_spectral_energy_density",
    "boltzmann_population_ratio", "detailed_balance_energy_density",
    "stimulated_to_spontaneous",
    "laser_threshold", "laser_steady_state", "laser_rate_rhs",
    "g2_thermal", "g2_coherent", "g2_fock", "g2_from_distribution",
]

# --- SI constants (defined locally; module is self-contained) -----------------
H_PLANCK = 6.62607015e-34     # Planck constant [J s]
C_LIGHT = 2.99792458e8        # speed of light [m/s]
K_B = 1.380649e-23            # Boltzmann constant [J/K]


# --- Einstein coefficients, detailed balance, Planck (S&Z Ch. 1, 5.6, 6.3) ----

def einstein_A_over_B(nu):
    """Einstein ratio  A21/B21 = 8 pi h nu^3 / c^3  [J s / m^3].

    Fixed entirely by detailed balance against the Planck spectrum; it is the
    spectral energy density at which stimulated and spontaneous emission are
    equal (S&Z, Quantum Optics, Ch. 1 / Sect. 6.3)."""
    nu = np.asarray(nu, dtype=float)
    return 8.0 * np.pi * H_PLANCK * nu ** 3 / C_LIGHT ** 3


def planck_spectral_energy_density(nu, T):
    """Planck spectral energy density per unit frequency
        rho(nu, T) = (8 pi h nu^3 / c^3) / (exp(h nu / kB T) - 1)   [J s / m^3].

    `np.expm1` keeps the Rayleigh-Jeans limit (h nu << kB T) accurate
    (S&Z Ch. 1, black-body radiation)."""
    nu = np.asarray(nu, dtype=float)
    x = H_PLANCK * nu / (K_B * T)
    return einstein_A_over_B(nu) / np.expm1(x)


def boltzmann_population_ratio(nu, T, g_lower=1.0, g_upper=1.0):
    """Thermal population ratio of the upper to the lower level
        N2/N1 = (g2/g1) exp(-h nu / kB T)   (Boltzmann; ~SM-03).

    Always < g2/g1 at positive T -- no thermal *inversion* (S&Z Sect. 5.6)."""
    nu = np.asarray(nu, dtype=float)
    return (g_upper / g_lower) * np.exp(-H_PLANCK * nu / (K_B * T))


def detailed_balance_energy_density(nu, T, g_lower=1.0, g_upper=1.0, A21=1.0):
    """Spectral energy density forced by *detailed balance* of the three Einstein
    processes against the thermal populations:

        N1 B12 rho = N2 (A21 + B21 rho)   =>   rho = A21 / (B12 N1/N2 - B21),

    with the Einstein relations B21 = A21 / (8 pi h nu^3/c^3) and
    g1 B12 = g2 B21 imposed.  The result is *independent* of A21 and the g's and
    equals `planck_spectral_energy_density` exactly -- that closure is Einstein's
    1917 argument (S&Z Ch. 1).  Returned here as an explicit check, not a shortcut."""
    nu = np.asarray(nu, dtype=float)
    AB = einstein_A_over_B(nu)                       # = 8 pi h nu^3 / c^3
    B21 = A21 / AB
    B12 = (g_upper / g_lower) * B21                  # g1 B12 = g2 B21
    N1_over_N2 = 1.0 / boltzmann_population_ratio(nu, T, g_lower, g_upper)
    return A21 / (B12 * N1_over_N2 - B21)


def stimulated_to_spontaneous(nu, T):
    """Ratio of stimulated to spontaneous emission in thermal equilibrium
        B21 rho / A21 = rho / (A21/B21) = 1 / (exp(h nu / kB T) - 1).

    ~1e-84 for a 248 nm (KrF) photon at 300 K -- spontaneous emission utterly
    dominates in equilibrium, so a laser needs a population *inversion* and a
    cavity, not a hot black body (S&Z Sect. 5.6)."""
    nu = np.asarray(nu, dtype=float)
    x = H_PLANCK * nu / (K_B * T)
    return 1.0 / np.expm1(x)


# --- single-mode laser rate equations & threshold (S&Z Sect. 5.5, Ch. 11) -----

def laser_threshold(gain=1.0, kappa=1.0, gamma=1.0):
    """Threshold pump rate  R_th = gamma * kappa / gain.

    Where round-trip gain first balances cavity loss; the inversion needed to
    lase is N_th = kappa/gain (S&Z Sect. 11.2, the threshold condition d = c)."""
    return gamma * kappa / gain


def laser_rate_rhs(state, pump, gain=1.0, kappa=1.0, gamma=1.0):
    """Single-mode laser rate equations  (S&Z Sect. 5.5):
        d N / dt = pump - gamma * N - gain * N * n      (inversion)
        d n / dt = gain * N * n - kappa * n             (cavity photons)
    `state = (N, n)`; returns (Ndot, ndot).  `laser_steady_state` zeroes both."""
    N, n = state
    Ndot = pump - gamma * N - gain * N * n
    ndot = gain * N * n - kappa * n
    return Ndot, ndot


def laser_steady_state(pump, gain=1.0, kappa=1.0, gamma=1.0):
    """Steady state (Ndot = ndot = 0) of the single-mode laser rate equations.

    Returns the tuple ``(inversion N, photon number n)``:

      * below threshold (pump <= R_th):  n = 0,  N = pump/gamma  (rises with pump);
      * above threshold (pump >  R_th):  N = kappa/gain (gain *clamps* the
        inversion) and n = (pump - R_th)/kappa  (the extra pump becomes photons).

    R_th = gamma kappa / gain = `laser_threshold(...)`.  The clamped inversion +
    the linear photon turn-on are the two hallmark laser results (S&Z Ch. 11)."""
    R_th = laser_threshold(gain, kappa, gamma)
    if pump <= R_th:
        return pump / gamma, 0.0
    N = kappa / gain                                  # gain clamping
    n = (pump - R_th) / kappa
    return N, n


# --- coherence: second-order correlation g2(0) (S&Z Ch. 4, Sects. 4.2-4.4) ----

def g2_thermal():
    """g2(0) = 2 for thermal / chaotic light (photon *bunching*).

    Bose-Einstein statistics give <n(n-1)> = 2<n>^2 (S&Z Sect. 4.4,
    Hanbury-Brown-Twiss)."""
    return 2.0


def g2_coherent():
    """g2(0) = 1 for ideal coherent (laser) light -- Poissonian, photons
    statistically independent (S&Z Sect. 4.4)."""
    return 1.0


def g2_fock(n):
    """g2(0) = 1 - 1/n for a number (Fock) state |n>; = 0 for n = 1, the perfect
    *antibunching* of a single-photon source (S&Z Sect. 4.4.4, sub-Poissonian).

    g2 < 1 has no classical description -- a nonclassicality witness (~QO-05)."""
    if n < 1:
        raise ValueError("g2_fock requires n >= 1 (a state with photons to detect)")
    return 1.0 - 1.0 / n


def g2_from_distribution(p_n):
    """Second-order correlation at zero delay from a photon-number distribution
        g2(0) = <n(n-1)> / <n>^2 ,
    with p_n[k] = P(n = k).  Reproduces 2 (thermal), 1 (Poisson/coherent),
    1 - 1/n0 (Fock) -- the operational definition (S&Z Sect. 4.5)."""
    p = np.asarray(p_n, dtype=float)
    p = p / p.sum()                                   # normalize defensively
    n = np.arange(p.size)
    mean = np.sum(n * p)
    mean_nn1 = np.sum(n * (n - 1) * p)
    return float(mean_nn1 / mean ** 2)


# --- demo ---------------------------------------------------------------------

def _demo():
    print("QO-03  Emission & coherence -- demo")
    print("=" * 52)

    # 1) Einstein A/B and the stimulated/spontaneous ratio
    lam = 248e-9                       # KrF excimer line (~PK-04)
    nu = C_LIGHT / lam
    print("\n1) Einstein coefficients at lambda = 248 nm (nu = %.3e Hz):" % nu)
    print("   A21/B21 = 8 pi h nu^3 / c^3 = %.3e J s / m^3" % einstein_A_over_B(nu))
    print("   detailed balance reproduces Planck: rho_db/rho_Planck = %.6f"
          % (detailed_balance_energy_density(nu, 300.0, 1.0, 3.0, A21=7.5e6)
             / planck_spectral_energy_density(nu, 300.0)))
    print("   stimulated/spontaneous = 1/(e^{h nu/kT}-1):")
    print("      at  T =   300 K (optical):  %.3e   (spontaneous wins -> need inversion)"
          % stimulated_to_spontaneous(nu, 300.0))
    nu_rf = 1.0e9                      # 1 GHz, microwave
    print("      at nu = 1 GHz, 300 K     :  %.3e   (stimulated wins -> maser regime)"
          % stimulated_to_spontaneous(nu_rf, 300.0))

    # 2) laser threshold: photon number vs pump
    g, k, gam = 1.0, 1.0, 1.0
    Rth = laser_threshold(g, k, gam)
    print("\n2) single-mode laser (gain=%.0f, kappa=%.0f, gamma=%.0f): R_th = %.2f"
          % (g, k, gam, Rth))
    print("   pump R   inversion N   photons n")
    for R in (0.0, 0.5, 1.0, 2.0, 5.0):
        N, n = laser_steady_state(R, g, k, gam)
        flag = "  (below)" if R < Rth else ("  (THRESHOLD)" if R == Rth else "  (above: N clamped)")
        print("   %5.2f      %7.3f      %7.3f%s" % (R, N, n, flag))

    # 3) the three g2(0) values
    print("\n3) second-order coherence g2(0):")
    print("   thermal / chaotic : %.3f   (bunching)" % g2_thermal())
    print("   coherent / laser  : %.3f   (Poissonian)" % g2_coherent())
    print("   single photon n=1 : %.3f   (antibunching)" % g2_fock(1))
    print("   Fock n=2          : %.3f   (sub-Poissonian, 1 - 1/n)" % g2_fock(2))


if __name__ == "__main__":
    _demo()
