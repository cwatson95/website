"""
RE-14  Schwarzschild solution & black holes  --  the horizon, the photon sphere,
the ISCO, and the classic solar-system tests (perihelion precession, light
bending, Shapiro delay, gravitational redshift).

Part of the physics topic network (see modules/topic_network.txt, module RE-14).
Prerequisites: RE-11 (curvature -- IMPORTED here for the metric and its
invariants), RE-13 (Einstein equations), ~CM-11 (central-force motion & the
effective potential -- forward reference; the Newtonian Kepler problem this
generalises).  This is the capstone of the SR/GR line RE-02 .. RE-13.

THE ONE IDEA.  Outside any static, spherically symmetric mass the geometry is
fixed -- uniquely (Birkhoff) -- to the Schwarzschild-Droste metric
        ds^2 = -(1-2M/r) dt^2 + (1-2M/r)^{-1} dr^2 + r^2 dOmega^2     (G=c=1).
Every black-hole phenomenon is one feature of this single line element:
  * r = 2M  is the EVENT HORIZON.  The metric blows up there, but the curvature
    invariant K = 48 M^2/r^6 (RE-11) is FINITE -- it is only the *coordinates*
    that fail, not spacetime.  The genuine singularity is r = 0 (K -> infinity).
  * Orbits follow from ONE effective potential  V(r) = (1-2M/r)(1+L^2/r^2).  The
    GR-only term  -2M L^2/r^3  (absent from Newton/~CM-11) bends bound orbits into
    rosettes -- PERIHELION PRECESSION, 43"/century for Mercury -- and creates two
    radii with no Newtonian analogue: the PHOTON SPHERE r = 3M (light can circle)
    and the ISCO r = 6M (innermost stable circular orbit for matter).
  * A photon climbing out is REDSHIFTED by sqrt((1-2M/r_obs)/(1-2M/r_emit)); the
    shift -> RE-10's weak-field gh/c^2 far away and -> infinity at the horizon.
  * Light grazing the Sun bends by 4M/b = 1.75" -- twice the naive equivalence-
    principle value (RE-10 saw only the time half; here spatial curvature adds the
    rest).

The metric and its curvature invariants are RE-11's; this module imports them and
adds the orbital structure and the four classic tests.  Pure stdlib (math) other
than the RE-11 import.  Geometrized units G = c = 1: a mass M is a *length*
(M_sun = G M_sun/c^2 = 1.477 km), and so is every "time" returned here.
"""

import os
import sys
import math

# --- import RE-11 (curvature: the metric + its invariants) by relative path ---
_RE11 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-11_curvature", "code")
if _RE11 not in sys.path:
    sys.path.insert(0, _RE11)
import curvature  # RE-11: schwarzschild_metric, ricci, kretschmann, riemann, ...

__all__ = [
    # geometry (re-exported / derived from RE-11)
    "schwarzschild_metric", "horizon_radius", "photon_sphere", "isco",
    "lapse", "kretschmann_formula",
    # orbital effective potentials and circular orbits
    "effective_potential", "effective_potential_massless",
    "circular_orbit_radius", "photon_sphere_from_potential", "isco_from_potential",
    # the classic tests
    "perihelion_precession", "light_deflection", "shapiro_delay",
    "gravitational_redshift", "gravitational_redshift_factor",
    # orbit integration (small RK4)
    "apsides_to_L_E", "integrate_orbit", "perihelion_advance",
    # physical constants (geometrized) for the demo / tests
    "GM_SUN", "C_LIGHT", "M_SUN", "R_SUN",
    "A_MERCURY", "E_MERCURY", "T_MERCURY_DAYS", "ARCSEC_PER_RAD",
]

# --- physical constants, in SI, reduced to geometrized (length) units --------
GM_SUN = 1.32712440018e20      # m^3 s^-2  -- IAU solar standard gravitational parameter
C_LIGHT = 2.99792458e8         # m s^-1    -- defined speed of light
M_SUN = GM_SUN / C_LIGHT ** 2  # m         -- the Sun as a length: 1476.6 m = 1.477 km
R_SUN = 6.957e8                # m         -- IAU nominal solar radius
A_MERCURY = 5.790905e10        # m         -- Mercury semi-major axis
E_MERCURY = 0.205630           # --        -- Mercury orbital eccentricity
T_MERCURY_DAYS = 87.9691       # days      -- Mercury orbital period
ARCSEC_PER_RAD = 180.0 / math.pi * 3600.0   # 206264.8...  rad -> arcseconds


# --- the geometry (RE-11) ----------------------------------------------------

def schwarzschild_metric(M=1.0):
    """The Schwarzschild metric g(x) in (t, r, theta, phi), re-exported from RE-11.
    A callable x -> 4x4 matrix.  Vacuum (R_uv = 0) for r > 2M; see RE-11."""
    return curvature.schwarzschild_metric(M)


def lapse(r, M):
    """The metric function f(r) = 1 - 2M/r = -g_tt = 1/g_rr.  Zero at the horizon
    r = 2M (g_tt -> 0, g_rr -> infinity: the coordinate singularity), negative
    inside.  sqrt(f) is the gravitational time-dilation factor for a static clock."""
    return 1.0 - 2.0 * M / r


def horizon_radius(M):
    """Event-horizon (Schwarzschild) radius r_S = 2M.  The metric's coordinate
    singularity; a one-way surface, but curvature is finite there (RE-11)."""
    return 2.0 * M


def photon_sphere(M):
    """Photon-sphere radius r = 3M: the unique circular *null* geodesic, where
    light can orbit.  It is the (unstable) maximum of the massless effective
    potential -- see photon_sphere_from_potential."""
    return 3.0 * M


def isco(M):
    """Innermost stable circular orbit r = 6M for massive particles: inside it no
    stable circular orbit exists and matter must plunge.  The radius at which the
    two circular-orbit roots of V'(r)=0 merge -- see isco_from_potential."""
    return 6.0 * M


def kretschmann_formula(r, M):
    """The Kretschmann invariant in closed form, K = 48 M^2 / r^6 (the value RE-11
    computes from the Riemann tensor).  FINITE at the horizon r = 2M
    (= 3/(4 M^4)); DIVERGENT at r = 0 -- this single scalar separates the
    coordinate horizon from the true curvature singularity."""
    return 48.0 * M * M / r ** 6


# --- orbital effective potentials --------------------------------------------

def effective_potential(r, L, M):
    """Effective potential (per unit rest-mass^2) for a MASSIVE geodesic in the
    equatorial plane:
        V(r) = (1 - 2M/r)(1 + L^2/r^2),     (dr/dtau)^2 = E^2 - V(r),
    with L the specific angular momentum.  Expanding,
        V = 1 - 2M/r + L^2/r^2 - 2M L^2/r^3 :
    the Newtonian -2M/r and centrifugal L^2/r^2 terms PLUS the purely
    relativistic -2M L^2/r^3 that is responsible for precession, the ISCO, and
    the photon sphere (the term absent from the ~CM-11 Kepler problem)."""
    return (1.0 - 2.0 * M / r) * (1.0 + L * L / (r * r))


def effective_potential_massless(r, L, M):
    """Effective potential for a MASSLESS geodesic (light):
        V(r) = (1 - 2M/r) L^2 / r^2 = L^2 (1/r^2 - 2M/r^3),
    with (dr/dlambda)^2 = E^2 - V(r).  Its single maximum, at r = 3M
    independent of L, is the photon sphere (an unstable circular photon orbit)."""
    return (1.0 - 2.0 * M / r) * L * L / (r * r)


def _ternary_extremum(f, lo, hi, find_max=True, iters=200):
    """Golden-free ternary search for the extremum of a unimodal f on [lo, hi]."""
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        better = (f(m1) < f(m2)) if find_max else (f(m1) > f(m2))
        if better:
            lo = m1
        else:
            hi = m2
    return 0.5 * (lo + hi)


def photon_sphere_from_potential(M):
    """Locate the photon sphere NUMERICALLY as the maximum of the massless
    effective potential V(r) = (1-2M/r)/r^2 over r > 2M.  Returns ~3M."""
    return _ternary_extremum(lambda r: effective_potential_massless(r, 1.0, M),
                             2.0001 * M, 30.0 * M, find_max=True)


def _Lsq_circular(r, M):
    """Specific angular momentum^2 of the circular orbit at radius r:
    from V'(r) = 0, L^2 = M r^2 / (r - 3M)  (real & positive only for r > 3M)."""
    return M * r * r / (r - 3.0 * M)


def isco_from_potential(M):
    """Locate the ISCO NUMERICALLY as the minimum of L^2(r) = M r^2/(r-3M) over
    circular orbits r > 3M: the smallest angular momentum that still supports a
    circular orbit marks the innermost stable one.  Returns ~6M."""
    return _ternary_extremum(lambda r: _Lsq_circular(r, M),
                             3.0001 * M, 50.0 * M, find_max=False)


def circular_orbit_radius(L, M, stable=True):
    """Radius of a circular orbit (extremum of V) for specific angular momentum L.
    V'(r)=0 gives  M r^2 - L^2 r + 3 M L^2 = 0, with roots
        r_pm = [L^2 +/- sqrt(L^4 - 12 M^2 L^2)] / (2M).
    The OUTER root (stable, a minimum of V) is returned by default; the inner
    root is the unstable maximum.  Circular orbits exist only for L >= 2*sqrt(3) M;
    at equality the roots merge at r = 6M (the ISCO).  Returns None below that."""
    disc = L * L * (L * L - 12.0 * M * M)
    if disc < 0.0:
        # genuinely no circular orbit -- unless we sit at the marginal ISCO point,
        # where L^2 = 12 M^2 rounds to a negligibly-negative discriminant.
        if disc < -1e-9 * (L * M) ** 2:
            return None
        disc = 0.0
    root = math.sqrt(disc)
    return (L * L + (root if stable else -root)) / (2.0 * M)


# --- classic test 1: perihelion precession -----------------------------------

def perihelion_precession(M, a, e):
    """Relativistic perihelion advance per orbit (radians),
        Delta phi = 6 pi M / (a (1 - e^2)),
    for a bound orbit of semi-major axis a and eccentricity e (a(1-e^2) is the
    semi-latus rectum).  This is the leading post-Newtonian shift produced by the
    -2M L^2/r^3 term in V; for Mercury it accumulates to ~43"/century, the
    anomaly that first confirmed GR.  Newtonian Kepler ellipses (~CM-11) do NOT
    precess: set the GR term to zero and this vanishes."""
    return 6.0 * math.pi * M / (a * (1.0 - e * e))


# --- classic test 2: deflection of light -------------------------------------

def light_deflection(M, b):
    """Deflection angle of a light ray with impact parameter b passing a mass M,
        Delta phi = 4 M / b      (weak field, b >> M).
    For a ray grazing the Sun (b = R_sun) this is 1.75" -- exactly TWICE the
    0.87" that the equivalence principle alone predicts (RE-10): half from
    gravitational time dilation, half from the spatial curvature of this metric."""
    return 4.0 * M / b


# --- classic test 3: Shapiro time delay --------------------------------------

def shapiro_delay(r1, r2, b, M):
    """Excess (one-way) coordinate-time delay of a radar signal travelling between
    radii r1 and r2 past a mass M at impact parameter b (geometrized units, so the
    result is a length = light-travel time):
        Delta t = 2M * ln[ (r1 + sqrt(r1^2-b^2))(r2 + sqrt(r2^2-b^2)) / b^2 ].
    Light slows in the deeper potential, so a round-trip echo arrives LATE; for
    Earth-Venus superior conjunction grazing the Sun this is ~200 microseconds
    round trip (Shapiro 1964).  Divide by c to convert to seconds."""
    s1 = math.sqrt(r1 * r1 - b * b)
    s2 = math.sqrt(r2 * r2 - b * b)
    return 2.0 * M * math.log((r1 + s1) * (r2 + s2) / (b * b))


# --- classic test 4: gravitational redshift ----------------------------------

def gravitational_redshift_factor(r_emit, r_obs, M):
    """The frequency/wavelength ratio 1 + z = lambda_obs/lambda_emit between two
    STATIC observers:
        1 + z = sqrt( (1 - 2M/r_obs) / (1 - 2M/r_emit) ).
    A static clock at r ticks at proper rate sqrt(1-2M/r), so a photon climbing
    OUT (r_emit < r_obs) is stretched: 1+z > 1."""
    return math.sqrt((1.0 - 2.0 * M / r_obs) / (1.0 - 2.0 * M / r_emit))


def gravitational_redshift(r_emit, r_obs, M):
    """Gravitational redshift z = 1+z - 1 = sqrt((1-2M/r_obs)/(1-2M/r_emit)) - 1.
    Two limits:
      * Weak field (both r >> M): z ~= M/r_emit - M/r_obs = Delta Phi/c^2 -- RE-10's
        Pound-Rebka / GPS result gh/c^2 (Newtonian potential difference).
      * Horizon: as r_emit -> 2M, z -> +infinity -- light from the horizon is
        infinitely redshifted, which is why the horizon is (for a distant
        observer) where everything freezes and fades to black."""
    return gravitational_redshift_factor(r_emit, r_obs, M) - 1.0


# --- optional: integrate a precessing orbit with a small RK4 -----------------

def apsides_to_L_E(M, r_peri, r_apo):
    """Specific (L, E) of the bound geodesic whose turning points are r_peri and
    r_apo.  Both are roots of E^2 = V(r), so solving
        (1-2M/r_p)(1+L^2/r_p^2) = (1-2M/r_a)(1+L^2/r_a^2)
    gives L^2, then E^2 = V(r_peri).  (E, L are the conserved energy and angular
    momentum per unit mass used by integrate_orbit.)"""
    fp = 1.0 - 2.0 * M / r_peri
    fa = 1.0 - 2.0 * M / r_apo
    Lsq = (fa - fp) / (fp / r_peri ** 2 - fa / r_apo ** 2)
    Esq = fp * (1.0 + Lsq / r_peri ** 2)
    return math.sqrt(Lsq), math.sqrt(Esq)


def _orbit_rhs(state, L, M):
    """d/dtau of (r, p_r, phi) for an equatorial massive geodesic, where
    p_r = dr/dtau.  From (dr/dtau)^2 = E^2 - V(r): dp_r/dtau = -1/2 V'(r)."""
    r, pr, _phi = state
    dpr = L * L / r ** 3 - M / r ** 2 - 3.0 * M * L * L / r ** 4   # = -1/2 V'(r)
    return (pr, dpr, L / (r * r))


def integrate_orbit(M, r_peri, r_apo, dtau=0.5, n_steps=200000):
    """Integrate a bound equatorial orbit with classic RK4, starting at perihelion
    (r = r_peri, p_r = 0, phi = 0).  Returns the trajectory as a list of
    (tau, r, phi).  (L, E) come from apsides_to_L_E.  Stops after n_steps or once
    a second perihelion is reached (one full radial period)."""
    L, _E = apsides_to_L_E(M, r_peri, r_apo)
    state = (r_peri, 0.0, 0.0)
    traj = [(0.0, state[0], state[2])]
    tau = 0.0
    seen_apo = False
    for _ in range(n_steps):
        r, pr, phi = state
        k1 = _orbit_rhs(state, L, M)
        s2 = tuple(state[i] + 0.5 * dtau * k1[i] for i in range(3))
        k2 = _orbit_rhs(s2, L, M)
        s3 = tuple(state[i] + 0.5 * dtau * k2[i] for i in range(3))
        k3 = _orbit_rhs(s3, L, M)
        s4 = tuple(state[i] + dtau * k3[i] for i in range(3))
        k4 = _orbit_rhs(s4, L, M)
        new = tuple(state[i] + (dtau / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
                    for i in range(3))
        tau += dtau
        # detect apoapsis (p_r: + -> -) then the next periapsis (p_r: - -> +)
        if state[1] > 0.0 >= new[1]:
            seen_apo = True
        if seen_apo and state[1] < 0.0 <= new[1]:
            # linear-interpolate phi to the p_r = 0 crossing (the perihelion)
            frac = -state[1] / (new[1] - state[1])
            phi_peri = state[2] + frac * (new[2] - state[2])
            traj.append((tau, new[0], phi_peri))
            return traj
        state = new
        traj.append((tau, state[0], state[2]))
    return traj


def perihelion_advance(M, r_peri, r_apo, dtau=0.25, n_steps=400000):
    """Numerically integrated perihelion advance per radial period (radians):
    integrate from one perihelion to the next and subtract 2*pi.  A direct test of
    the closed-form perihelion_precession, with no weak-field approximation."""
    traj = integrate_orbit(M, r_peri, r_apo, dtau=dtau, n_steps=n_steps)
    phi_next_peri = traj[-1][2]
    return phi_next_peri - 2.0 * math.pi


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-14  Schwarzschild solution & black holes -- demo   (geometrized G=c=1)")
    print("=" * 74)

    print("\nCharacteristic radii (units of M):")
    print("  horizon r_S = %.0f M   photon sphere = %.0f M   ISCO = %.0f M"
          % (horizon_radius(1.0), photon_sphere(1.0), isco(1.0)))
    print("  located from the effective potentials:  photon sphere -> %.4f M, "
          "ISCO -> %.4f M" % (photon_sphere_from_potential(1.0), isco_from_potential(1.0)))

    print("\nHorizon is a COORDINATE singularity, r=0 is REAL (RE-11 invariant):")
    sch = schwarzschild_metric(1.0)
    for r in (10.0, 6.0, 3.0):
        K = curvature.kretschmann(sch, [0.0, r, 1.2, 0.7])
        print("  r=%4.1f M:  Ricci~0 (vacuum),  K = %.4e  (48/r^6 = %.4e)"
              % (r, K, kretschmann_formula(r, 1.0)))
    print("  at the horizon r=2M the curvature is finite: K = 48/(2M)^6 = %.4f / M^4"
          % kretschmann_formula(2.0, 1.0))

    print("\nClassic test 1 -- Mercury's perihelion precession:")
    dphi_orbit = perihelion_precession(M_SUN, A_MERCURY, E_MERCURY)
    orbits_per_century = 100.0 * 365.25 / T_MERCURY_DAYS
    arcsec_century = dphi_orbit * orbits_per_century * ARCSEC_PER_RAD
    print("  Delta phi = 6 pi M/(a(1-e^2)) = %.4e rad/orbit  ->  %.2f \"/century"
          % (dphi_orbit, arcsec_century))
    print("  (observed anomalous precession: ~43 \"/century)")

    print("\nClassic test 2 -- deflection of starlight grazing the Sun:")
    defl = light_deflection(M_SUN, R_SUN)
    print("  Delta phi = 4M/b = %.3e rad = %.3f \"   (Eddington 1919: 1.75 \")"
          % (defl, defl * ARCSEC_PER_RAD))

    print("\nClassic test 3 -- Shapiro radar echo delay (Earth-Venus past the Sun):")
    r_earth, r_venus = 1.496e11, 1.082e11
    dt_oneway = shapiro_delay(r_earth, r_venus, R_SUN, M_SUN)   # geometrized = metres
    roundtrip_us = 2.0 * dt_oneway / C_LIGHT * 1e6
    print("  round-trip excess delay ~ %.0f microseconds   (Shapiro 1964/68: ~200 us)"
          % roundtrip_us)

    print("\nClassic test 4 -- gravitational redshift:")
    z_sun = gravitational_redshift(R_SUN, 1.0e30, M_SUN)        # Sun surface -> infinity
    print("  Sun surface -> infinity:  z = %.3e  (~M_sun/R_sun = %.3e)"
          % (z_sun, M_SUN / R_SUN))
    print("  near the horizon, r_emit -> 2M:  z(2.0001M) = %.1f  ->  diverges"
          % gravitational_redshift(2.0001, 1.0e9, 1.0))

    print("\nIntegrated precessing orbit (RK4), r_peri=50M, r_apo=90M:")
    num = perihelion_advance(1.0, 50.0, 90.0)
    a = 0.5 * (50.0 + 90.0)
    e = (90.0 - 50.0) / (90.0 + 50.0)
    formula = perihelion_precession(1.0, a, e)
    print("  RK4 advance = %.4f rad/orbit   vs   6 pi M/(a(1-e^2)) = %.4f rad/orbit"
          % (num, formula))


if __name__ == "__main__":
    _demo()
