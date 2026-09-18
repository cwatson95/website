"""PK-03  Plasma waves & instabilities -- Langmuir, ion-acoustic, Landau, two-stream.

Physics topic network, module PK-03 (modules/topic_network.txt).
Source: Michel, *Introduction to Laser-Plasma Interactions* (Springer), Chapter 1
(plasma basics & waves) and its Formulary (Appendix A); cited at section level in
refs.md.  Builds on the kinetic/fluid picture of ~PK-01 and the driven-oscillator
language of ~CM-15; the Landau contour belongs to ~MA-06 (complex analysis).

Two scales organize every plasma wave (Michel Sect. 1.2):
    plasma frequency   w_p = sqrt(n q^2 / (eps0 m))     -- the electron clock,
    Debye length       lam_D = sqrt(eps0 kB T/(n q^2)) = v_th / w_p,
with thermal speed v_th = sqrt(kB T/m).  The longitudinal (electrostatic) waves are
roots of the plasma dielectric function eps(k,w) = 0 (Michel Sect. 1.3.1):

  * Langmuir / electron plasma waves (Bohm-Gross):
        w^2 = w_p^2 + 3 k^2 v_th^2 = w_p^2 (1 + 3 k^2 lam_D^2),   ->  w_p as k->0;
  * ion-acoustic waves:
        w = k c_s / sqrt(1 + k^2 lam_D^2),   c_s = sqrt(kB T_e/m_i),  ->  k c_s as
        k lam_D << 1  (the plasma "sound" speed, electron pressure on ion inertia);
  * Landau damping -- collisionless damping from wave-particle resonance at the
    phase velocity v = w/k, gamma ~ -df0/dv|_{w/k}; for a Maxwellian (closed form,
    Michel Sect. 1.3.4 / Formulary A.4)
        gamma/w_p = -sqrt(pi/8) (k lam_D)^{-3} exp(-1/(2(k lam_D)^2) - 3/2) < 0;
  * two-stream instability -- two counter-streaming cold electron beams (+/- v0),
        1 = (w_p^2/2)[1/(w-k v0)^2 + 1/(w+k v0)^2],
    unstable (Im w > 0) for k v0 < w_p, with peak growth w_p/sqrt(8) at
    k v0 = sqrt(3/8) w_p.

Landau damping and the resonance need the *kinetic* (Vlasov) picture of ~PK-01 and
the Landau deformation of the velocity contour of ~MA-06; the fluid dispersions
(Bohm-Gross, ion-acoustic) are their real, weakly-damped roots.
"""

import numpy as np

__all__ = [
    "EPS0", "ELEM_CHARGE", "ELECTRON_MASS", "PROTON_MASS", "K_B",
    "plasma_frequency", "debye_length", "thermal_speed",
    "bohm_gross", "ion_acoustic", "landau_damping_rate", "two_stream_growth_rate",
]

# --- physical constants (CODATA 2018, SI) ------------------------------------
EPS0 = 8.8541878128e-12       # vacuum permittivity  [F/m]
ELEM_CHARGE = 1.602176634e-19  # elementary charge    [C]
ELECTRON_MASS = 9.1093837015e-31  # electron mass     [kg]
PROTON_MASS = 1.67262192369e-27   # proton  mass     [kg]
K_B = 1.380649e-23            # Boltzmann constant   [J/K]


# --- the two fundamental scales (Michel Sect. 1.2.1-1.2.2) -------------------

def plasma_frequency(n, q, m):
    """Plasma (Langmuir) frequency  w_p = sqrt(n q^2 / (eps0 m))  [rad/s].

    The natural oscillation frequency of a charged species of density n, charge q,
    mass m about its neutralizing background -- the cold-plasma cutoff w -> w_p."""
    return np.sqrt(n * q ** 2 / (EPS0 * m))


def debye_length(n, T, q):
    """Debye screening length  lam_D = sqrt(eps0 kB T / (n q^2))  [m].

    The scale over which a charge is shielded; also lam_D = v_th / w_p, the distance
    a thermal particle travels in one plasma period (Michel Sect. 1.2.1)."""
    return np.sqrt(EPS0 * K_B * T / (n * q ** 2))


def thermal_speed(T, m):
    """Thermal speed  v_th = sqrt(kB T / m)  [m/s]  (1-D rms speed, sets c_s and
    the Bohm-Gross pressure term)."""
    return np.sqrt(K_B * T / m)


# --- Langmuir / electron plasma waves: Bohm-Gross (Michel Sect. 1.3.1.4) ------

def bohm_gross(k, n, T, m, q=ELEM_CHARGE):
    """Langmuir-wave dispersion (Bohm-Gross):
        w(k) = sqrt(w_p^2 + 3 k^2 v_th^2),   v_th = sqrt(kB T/m).

    The warm correction 3 k^2 v_th^2 is the 1-D adiabatic (gamma = 3) electron
    pressure; equivalently w^2 = w_p^2 (1 + 3 k^2 lam_D^2).  Cold limit w -> w_p."""
    wp = plasma_frequency(n, q, m)
    vth = thermal_speed(T, m)
    return np.sqrt(wp ** 2 + 3.0 * (k * vth) ** 2)


# --- ion-acoustic waves (Michel Sect. 1.3.1.5) -------------------------------

def ion_acoustic(k, Te, n, mi, q=ELEM_CHARGE):
    """Ion-acoustic dispersion:
        w(k) = k c_s / sqrt(1 + k^2 lam_De^2),   c_s = sqrt(kB Te / mi).

    Electron pressure (via the electron Debye length lam_De) provides the restoring
    force, ion inertia the mass.  Long-wavelength (k lam_De << 1): w ~ k c_s (sound).
    Short-wavelength: w saturates at the ion plasma frequency w_pi = c_s/lam_De."""
    cs = np.sqrt(K_B * Te / mi)
    lam_De = debye_length(n, Te, q)          # electron Debye length
    return k * cs / np.sqrt(1.0 + (k * lam_De) ** 2)


# --- Landau damping (Michel Sect. 1.3.4 / Formulary A.4) ---------------------

def landau_damping_rate(k, n, T, m, q=ELEM_CHARGE):
    """Collisionless Landau damping rate of a Langmuir wave for a Maxwellian (the
    standard weak-damping closed form):
        gamma/w_p = -sqrt(pi/8) (k lam_D)^{-3} exp(-1/(2(k lam_D)^2) - 3/2).

    gamma < 0 (damping): the wave loses energy to particles resonant at the phase
    velocity v = w/k, where -df0/dv > 0 for a Maxwellian.  |gamma| is exponentially
    small for k lam_D << 1 (resonance far on the tail) and grows toward k lam_D ~ 1.
    Requires the kinetic (Vlasov, ~PK-01) picture and the Landau contour (~MA-06)."""
    wp = plasma_frequency(n, q, m)
    kld = k * debye_length(n, T, q)
    return -wp * np.sqrt(np.pi / 8.0) * kld ** (-3) * np.exp(-1.0 / (2.0 * kld ** 2) - 1.5)


# --- two-stream instability (Michel Sect. 1.3.1.3 dielectric framework) ------

def two_stream_growth_rate(k, n, m, v0, q=ELEM_CHARGE):
    """Growth rate Im(w) >= 0 of the cold two-stream instability at wavenumber k.

    Two counter-streaming cold beams (each density n/2, drift +/- v0) give the
    longitudinal dispersion (Michel Sect. 1.3.1.3, applied to two drifting species)
        1 = (w_p^2/2)[1/(w - k v0)^2 + 1/(w + k v0)^2],   w_p^2 = n q^2/(eps0 m),
    which clears to the bi-quadratic
        w^4 - (2a + w_p^2) w^2 + (a^2 - w_p^2 a) = 0,   a = (k v0)^2.
    Solved here numerically with numpy.roots; the most unstable root has
        Im(w) = sqrt( [w_p sqrt(8a + w_p^2) - (2a + w_p^2)] / 2 )   for a < w_p^2,
    and Im(w) = 0 (purely real, stable oscillation) for k v0 >= w_p.  Peak growth
    w_p/sqrt(8) at k v0 = sqrt(3/8) w_p.  k is a scalar (numpy.roots needs scalars)."""
    wp = plasma_frequency(n, q, m)
    a = (k * v0) ** 2
    # bi-quadratic in w: coefficients high -> low degree (w^4 .. w^0)
    coeffs = [1.0, 0.0, -(2.0 * a + wp ** 2), 0.0, a ** 2 - wp ** 2 * a]
    roots = np.roots(coeffs)
    gamma = float(np.max(roots.imag))
    # purely-real (stable) roots carry only numpy.roots round-off: clip it away
    if gamma < 1e-6 * wp:
        return 0.0
    return gamma


# --- demo --------------------------------------------------------------------

def _demo():
    print("PK-03  Plasma waves & instabilities -- demo")
    print("=" * 60)

    n = 1.0e18          # electron density [1/m^3]
    T = 1.0e4           # temperature      [K]  (~0.86 eV)
    e, me, mi = ELEM_CHARGE, ELECTRON_MASS, PROTON_MASS

    wp = plasma_frequency(n, e, me)
    lD = debye_length(n, T, e)
    vth = thermal_speed(T, me)
    print(f"\nplasma: n = {n:.1e} /m^3,  T = {T:.0f} K")
    print(f"  w_p   = {wp:.4e} rad/s")
    print(f"  lam_D = {lD:.4e} m      (= v_th/w_p = {vth/wp:.4e})")
    print(f"  v_th  = {vth:.4e} m/s")

    # 1) Langmuir (Bohm-Gross) & ion-acoustic dispersion samples
    cs = np.sqrt(K_B * T / mi)                 # ion-acoustic sound speed c_s
    print("\n1) dispersion samples (k in units of 1/lam_D):")
    print("   k*lam_D   w_Langmuir/w_p   w_ion-ac/(k c_s)")
    for kld in (0.01, 0.1, 0.3, 0.5):
        k = kld / lD
        wL = bohm_gross(k, n, T, me) / wp
        wIA = ion_acoustic(k, T, n, mi) / (k * cs)
        print(f"   {kld:6.2f}    {wL:10.4f}      {wIA:10.4f}")
    print("   -> Langmuir -> 1 (w_p) as k->0;  ion-acoustic -> 1 (k c_s) as k lam_D->0")

    # 2) Landau damping rate
    print("\n2) Landau damping  gamma/w_p  (Maxwellian, weak-damping form):")
    for kld in (0.2, 0.3, 0.4, 0.5):
        k = kld / lD
        g = landau_damping_rate(k, n, T, me) / wp
        print(f"   k*lam_D = {kld:.2f}:  gamma/w_p = {g:+.4e}   (damping, |gamma| grows with k lam_D)")

    # 3) two-stream instability growth band
    v0 = 5.0 * vth
    print(f"\n3) two-stream instability (beams at +/- v0 = {v0:.2e} m/s):")
    print("   k v0/w_p   gamma/w_p")
    kgrid = np.linspace(1e-3, 1.4, 1500) * wp / v0
    g = np.array([two_stream_growth_rate(k, n, me, v0) for k in kgrid]) / wp
    for target in (0.2, 0.4, 0.6124, 0.9, 1.1):
        j = int(np.argmin(np.abs(kgrid * v0 / wp - target)))
        print(f"   {kgrid[j]*v0/wp:7.4f}    {g[j]:+.4f}")
    jmax = int(np.argmax(g))
    print(f"   peak: gamma/w_p = {g[jmax]:.4f} at k v0/w_p = {kgrid[jmax]*v0/wp:.4f}"
          f"   (theory {1/np.sqrt(8):.4f} at {np.sqrt(3/8):.4f})")
    print(f"   unstable band: k v0 < w_p  (Im w > 0); stable for k v0 > w_p")


if __name__ == "__main__":
    _demo()
