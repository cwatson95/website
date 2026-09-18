"""
RE-16  Gravitational waves  --  linearized gravity, the transverse-traceless
gauge and its two polarizations, the effect on a ring of free test particles,
the quadrupole formula, and the binary-inspiral chirp.

Part of the physics topic network (see modules/topic_network.txt, module RE-16).
Prerequisites: RE-11 (curvature: the linearized Riemann tensor is the tidal field
a wave carries), RE-13 (the Einstein field equations being linearized here), RE-05
(eta and the Minkowski inner product).  This is the wave sector of the RE/GR trunk.

THE ONE IDEA.  Write the metric as a small ripple on flat space, g = eta + h with
|h| << 1, and feed it into Einstein's equation.  In the Lorenz (harmonic) gauge
the trace-reversed perturbation  hbar_{mu nu} = h_{mu nu} - 1/2 eta_{mu nu} h
obeys the ORDINARY WAVE EQUATION
        box hbar_{mu nu} = -16 pi T_{mu nu},        box = -d_t^2 + del^2 ,
so in vacuum (box hbar = 0) gravity propagates as a wave AT THE SPEED OF LIGHT.
The residual gauge freedom strips it down to the transverse-traceless (TT) gauge:
just TWO physical polarizations, h_+ and h_x.  A wave passing through a ring of
free particles stretches one transverse axis while squeezing the other -- and does
so AREA-PRESERVINGLY (the perturbation is traceless).  Waves are SOURCED by the
QUADRUPOLE moment: conservation of mass kills the monopole and conservation of
momentum kills the dipole, so a *spherically symmetric* source is gravitationally
silent.  For a binary the inspiral CHIRPS, and the rate fixes the chirp mass M_c.

Conventions (whole RE trunk): geometrized units  G = c = 1; mostly-plus metric
eta = diag(-1, +1, +1, +1); weak field  g = eta + h,  |h| << 1.  Greek indices
run 0..3 with x^0 = t, (x^1, x^2, x^3) = (x, y, z).  Waves propagate along +z.
Pure stdlib (math only); 4-vectors / tensors are nested Python lists.
"""

import math

__all__ = [
    "ETA", "POL_PLUS", "POL_CROSS", "polarization_tensors",
    "tt_wave", "is_transverse_traceless",
    "dispersion_omega", "wave_equation_residual",
    "unit_ring", "ring_response", "polygon_area", "area_change",
    "chirp_mass", "orbital_frequency", "gw_frequency",
    "reduced_quadrupole", "quadrupole_luminosity", "chirp_rate",
    "CHIRP_RATE_CONST",
]

# Minkowski metric, mostly plus (RE-05). Reference only -- h below is the
# perturbation g - eta, not the full metric.
ETA = [[-1.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.0, 0.0],
       [0.0, 0.0, 1.0, 0.0],
       [0.0, 0.0, 0.0, 1.0]]

# The two TT polarization basis tensors, in the transverse (x, y) plane of a
# +z wave (3x3 spatial blocks). e_+ stretches x while squeezing y; e_x is e_+
# rotated by 45 deg. They are trace-free and trace-orthogonal: sum_ij e_+ e_x = 0.
POL_PLUS = [[1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 0.0]]
POL_CROSS = [[0.0, 1.0, 0.0],
             [1.0, 0.0, 0.0],
             [0.0, 0.0, 0.0]]


def polarization_tensors():
    """Return (e_+, e_x), the two TT polarization basis tensors (3x3 spatial)
    for a wave along z.  Trace-free and orthogonal under the Frobenius product
    sum_{ij} A_{ij} B_{ij}; each has squared norm 2."""
    return [row[:] for row in POL_PLUS], [row[:] for row in POL_CROSS]


# --- the plane gravitational wave (transverse-traceless gauge) ----------------

def tt_wave(h_plus, h_cross, omega, t, z):
    """TT metric perturbation h_{mu nu} (4x4) of a plane wave of angular
    frequency `omega` propagating along +z, evaluated at time `t`, position `z`.

    The wave is null (k^2 = 0), so the phase is  omega*(t - z)  and only the
    transverse (x, y) block is populated:
        h_xx = -h_yy = h_+ cos(omega(t - z)),
        h_xy =  h_yx = h_x cos(omega(t - z)),
    every other component (the time row/column and the z row/column) is zero.
    That structure -- spatial-trace zero and transverse to the propagation
    direction -- is exactly the transverse-traceless gauge."""
    phase = omega * (t - z)
    c = math.cos(phase)
    hp = h_plus * c
    hx = h_cross * c
    h = [[0.0] * 4 for _ in range(4)]
    h[1][1] = hp        # xx
    h[2][2] = -hp       # yy = -xx  (traceless)
    h[1][2] = hx        # xy
    h[2][1] = hx        # yx = xy   (symmetric)
    return h


def is_transverse_traceless(h, axis=3, tol=1e-9):
    """True iff the 4x4 perturbation `h` is in the transverse-traceless gauge for
    a wave along spatial `axis` (default z = index 3):

      * spatial trace  h_11 + h_22 + h_33 = 0          (traceless),
      * the propagation-axis row & column vanish        (transverse: nothing
        along the direction of travel),
      * the time row & column vanish                    (TT gauge: purely spatial,
        h_{0 mu} = 0, so a single particle at rest feels no force).
    """
    spatial_trace = h[1][1] + h[2][2] + h[3][3]
    if abs(spatial_trace) > tol:
        return False
    for mu in range(4):
        if abs(h[axis][mu]) > tol or abs(h[mu][axis]) > tol:
            return False          # transverse to the propagation axis
        if abs(h[0][mu]) > tol or abs(h[mu][0]) > tol:
            return False          # purely spatial (TT gauge)
    return True


# --- the wave equation: gravity travels at c ----------------------------------

def dispersion_omega(k):
    """The vacuum dispersion relation  omega = |k|: gravitational waves are null,
    so their phase speed omega/|k| equals 1 = c.  `k` may be a wavenumber
    (scalar) or a wave 3-vector (sequence); returns its magnitude."""
    try:
        return math.sqrt(sum(ki * ki for ki in k))
    except TypeError:
        return abs(k)


def wave_equation_residual(h_plus, h_cross, omega, k, t=0.0, z=0.0):
    """Residual of the vacuum wave equation  box h = (-d_t^2 + d_z^2) h  for the
    plane wave  h_{mu nu}(t, z) = eps_{mu nu} cos(omega t - k z)  propagating
    along z (eps the +/x polarization pattern).  Acting on this field,
        box h_{mu nu} = (omega^2 - k^2) h_{mu nu},
    so the returned max_{mu nu} |box h_{mu nu}| VANISHES exactly when
    omega^2 = k^2, i.e. omega = dispersion_omega(k) -- the wave moves at c -- and
    is nonzero for any other (omega, k).  (Default sample point t = z = 0, where
    cos = 1, so the residual cleanly reports the coefficient.)"""
    coeff = omega * omega - k * k
    c = math.cos(omega * t - k * z)
    eps = [[0.0] * 4 for _ in range(4)]
    eps[1][1] = h_plus
    eps[2][2] = -h_plus
    eps[1][2] = h_cross
    eps[2][1] = h_cross
    return max(abs(coeff * eps[i][j] * c) for i in range(4) for j in range(4))


# --- effect on matter: a ring of free test particles --------------------------

def unit_ring(n=256):
    """`n` points evenly spaced on the unit circle in the transverse (x, y)
    plane -- a ring of free test particles to watch a wave deform."""
    return [(math.cos(2.0 * math.pi * i / n), math.sin(2.0 * math.pi * i / n))
            for i in range(n)]


def ring_response(h_plus, h_cross, phase, ring_points):
    """Displace each test particle by the geodesic-deviation shift
        delta xi^i = 1/2 h^i_j xi^j ,
    with the TT perturbation evaluated at the given `phase` (the argument of the
    cosine; phase = 0 is maximum +/x amplitude).  In the (x, y) plane
        delta xi_x = 1/2 cos(phase) (h_+ xi_x + h_x xi_y),
        delta xi_y = 1/2 cos(phase) (h_x xi_x - h_+ xi_y).
    Returns the list of displaced (x, y) points.  h_+ stretches x while squeezing
    y (principal axes = coordinate axes); h_x is the same pattern rotated 45 deg
    (principal axes = the diagonals)."""
    c = 0.5 * math.cos(phase)
    out = []
    for (xi_x, xi_y) in ring_points:
        dx = c * (h_plus * xi_x + h_cross * xi_y)
        dy = c * (h_cross * xi_x - h_plus * xi_y)
        out.append((xi_x + dx, xi_y + dy))
    return out


def polygon_area(points):
    """Signed area enclosed by a closed polygon (shoelace formula)."""
    n = len(points)
    a = 0.0
    for i in range(n):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return 0.5 * a


def area_change(h_plus, h_cross, phase, n=256):
    """Fractional area change  (A' - A)/A  of a ring of free particles deformed by
    the wave at `phase`, measured geometrically (shoelace).  Because the TT
    perturbation is TRACELESS, the linear-order change 1/2 tr(h) vanishes and the
    area is preserved to first order; the exact residual is second order,
        area_change = -1/4 (h_+^2 + h_x^2) cos^2(phase) = O(h^2) ~ 0.
    (A linear map scales every area by its determinant, so this ratio is exact
    and independent of n.)  This is the hallmark of a quadrupolar, spin-2 wave:
    it shears space without compressing it."""
    ring = unit_ring(n)
    a0 = polygon_area(ring)
    a1 = polygon_area(ring_response(h_plus, h_cross, phase, ring))
    return (a1 - a0) / a0


# --- generation: the quadrupole formula & the inspiral chirp -------------------

def chirp_mass(m1, m2):
    """Chirp mass  M_c = (m1 m2)^(3/5) / (m1 + m2)^(1/5).  This single combination
    -- not the individual masses -- governs the leading inspiral waveform; it is
    what LIGO reads off the chirp rate.  Symmetric in m1, m2; for equal masses
    m1 = m2 = m it is  m / 2^(1/5)."""
    return (m1 * m2) ** 0.6 / (m1 + m2) ** 0.2


def orbital_frequency(m1, m2, r):
    """Newtonian (Kepler) orbital frequency of a circular binary of total mass
    M = m1 + m2 and separation r:  f_orb = (1/2pi) sqrt(M / r^3)  (G = 1).
    Equivalently omega_orb^2 = M / r^3 -- Kepler's third law."""
    return math.sqrt((m1 + m2) / r ** 3) / (2.0 * math.pi)


def gw_frequency(m1, m2, r):
    """Gravitational-wave frequency of a circular binary:  f_GW = 2 f_orb,
    because the mass quadrupole returns to its original shape TWICE per orbit (it
    is invariant under a half-turn).  Thus
        f_GW = (1/pi) sqrt((m1 + m2) / r^3) = 2 * orbital_frequency(m1, m2, r)."""
    return math.sqrt((m1 + m2) / r ** 3) / math.pi


def reduced_quadrupole(points):
    """Trace-free (reduced) mass quadrupole moment
        Qbar_ij = sum_a m_a (x_i x_j - 1/3 delta_ij r^2)
    of point masses, each given as (m, x, y, z).  Returns a 3x3 matrix.  Only this
    trace-free part radiates: the monopole (total mass) and dipole (center of
    mass / momentum) are conserved and produce NO waves, so a spherically
    symmetric distribution has Qbar = 0 and is gravitationally silent."""
    Q = [[0.0] * 3 for _ in range(3)]
    for (m, x, y, z) in points:
        pos = (x, y, z)
        r2 = x * x + y * y + z * z
        for i in range(3):
            for j in range(3):
                Q[i][j] += m * (pos[i] * pos[j] - (r2 / 3.0 if i == j else 0.0))
    return Q


def quadrupole_luminosity(Q3dot):
    """Einstein quadrupole luminosity (power radiated as gravitational waves):
        P = (1/5) <  d^3 Qbar_ij/dt^3  d^3 Qbar^ij/dt^3  >
          = (1/5) sum_{ij} (Q3dot_ij)^2     (G = c = 1),
    where Q3dot is the third time derivative of the TRACE-FREE quadrupole moment
    (a 3x3 matrix).  A spherically symmetric source has Qbar = 0 at all times, so
    every derivative -- and hence P -- vanishes: no monopole or dipole radiation."""
    return 0.2 * sum(Q3dot[i][j] ** 2 for i in range(3) for j in range(3))


# df_GW/dt = (96/5) pi^(8/3) M_c^(5/3) f_GW^(11/3)  (quadrupole order, G = c = 1).
CHIRP_RATE_CONST = (96.0 / 5.0) * math.pi ** (8.0 / 3.0)


def chirp_rate(f, Mc):
    """Rate of increase of the GW frequency of an inspiralling binary,
        df/dt = (96/5) pi^(8/3) M_c^(5/3) f^(11/3)   (G = c = 1),
    obtained by equating the quadrupole luminosity to the orbital energy loss.
    The strong powers  f^(11/3) and M_c^(5/3)  are the 'chirp': measuring df/dt
    and f directly yields the chirp mass M_c.  CHIRP_RATE_CONST = (96/5) pi^(8/3)."""
    return CHIRP_RATE_CONST * Mc ** (5.0 / 3.0) * f ** (11.0 / 3.0)


# --- demo ---------------------------------------------------------------------

def _demo():
    print("RE-16  Gravitational waves -- demo   (G = c = 1, eta = diag(-1,+1,+1,+1))")
    print("=" * 72)

    print("\nTT plane wave along +z (h_+ = 0.1, h_x = 0.05, omega = 1) at t = z = 0:")
    h = tt_wave(0.1, 0.05, 1.0, 0.0, 0.0)
    for row in h:
        print("   ", ["% .3f" % v for v in row])
    print("  transverse-traceless?", is_transverse_traceless(h),
          "  spatial trace =", round(h[1][1] + h[2][2] + h[3][3], 12))

    print("\nwaves travel at c:  box h = 0  iff  omega = |k|:")
    for omega in (1.0, 1.3):
        r = wave_equation_residual(0.1, 0.05, omega, 1.0)
        print("    omega=%.2f, k=1.00 -> max|box h| = %.4f   %s"
              % (omega, r, "(on-shell, wave at c)" if r < 1e-12 else "(off-shell)"))

    print("\na ring of free particles: h_+ stretches x / squeezes y; area preserved:")
    ring = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]
    disp = ring_response(0.2, 0.0, 0.0, ring)
    print("    (1,0) ->", tuple(round(v, 3) for v in disp[0]),
          "   (0,1) ->", tuple(round(v, 3) for v in disp[1]))
    print("    fractional area change = %.3e   (O(h^2): traceless => area-preserving)"
          % area_change(0.2, 0.0, 0.0))
    print("    pure h_x shears the diagonals: (1,0) ->",
          tuple(round(v, 3) for v in ring_response(0.0, 0.2, 0.0, ring)[0]))

    print("\nno monopole/dipole: a spherically symmetric source is silent:")
    octahedron = [(2.0, 1.7, 0, 0), (2.0, -1.7, 0, 0), (2.0, 0, 1.7, 0),
                  (2.0, 0, -1.7, 0), (2.0, 0, 0, 1.7), (2.0, 0, 0, -1.7)]
    Q = reduced_quadrupole(octahedron)
    qmax = max(abs(Q[i][j]) for i in range(3) for j in range(3))
    print("    symmetric octahedron: max|Qbar_ij| = %.2e -> luminosity = %.2e (silent)"
          % (qmax, quadrupole_luminosity(Q)))
    aspherical = [(1.0, 2.0, 0.0, 0.0), (1.0, -2.0, 0.0, 0.0)]   # a bar along x
    print("    a bar along x:        max|Qbar_ij| = %.3f  (radiates)"
          % max(abs(v) for row in reduced_quadrupole(aspherical) for v in row))

    print("\nbinary inspiral -- the chirp (GW150914-like 36 + 29 solar masses):")
    m1, m2 = 36.0, 29.0
    Mc = chirp_mass(m1, m2)
    print("    chirp mass M_c = %.2f Msun   (equal-mass check: chirp_mass(30,30)=%.3f, 30/2^.2=%.3f)"
          % (Mc, chirp_mass(30.0, 30.0), 30.0 / 2.0 ** 0.2))
    r = 50.0
    print("    at r = %.0f:  f_orb = %.5f,  f_GW = %.5f = 2 f_orb,  df/dt = %.3e"
          % (r, orbital_frequency(m1, m2, r), gw_frequency(m1, m2, r),
             chirp_rate(gw_frequency(m1, m2, r), Mc)))


if __name__ == "__main__":
    _demo()
