"""NE-21  Neutron diffusion theory: Fick's law, the diffusion equation, criticality.

Nuclear Science & Engineering trunk, module NE-21 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 10.10 (Addendum 1), printed pp. 356-362.  Pure stdlib.

~NE-19 used the buckling B^2 as a given.  This module is where it comes from, and
the derivation is a balance sheet written on a differential volume:

    leakage + absorption = production                      [Eq. (10.57)]

Neutrons random-walk, so on average they drift from where there are many to where
there are few.  Assuming the net current is proportional to the flux gradient --

    J = -D grad(phi)                                       [Eq. (10.58), Fick]

-- turns the balance into a second-order PDE,

    -D grad^2 phi + Sigma_a phi = nu Sigma_f phi + Q       [Eq. (10.64)]

which for the one-speed model rearranges to

    grad^2 phi + (k_inf - 1)/L^2 phi = -Q/D,   L^2 = D/Sigma_a   [Eq. (10.66)]

and splits the subject in two.  With a source Q and no fission it is a FIXED
SOURCE problem, and L is the length scale over which the flux dies away.  With no
source it is a CRITICALITY problem, and it is an EIGENVALUE problem: the equation
has a non-trivial solution only for discrete sizes.  That is the whole content of

    B_mat^2 = (k_inf - 1)/L^2  =  B_g^2                     [Eq. (10.80)]

-- material properties on the left, geometry on the right, and criticality is
where they meet.  Two things follow that ~NE-19 could only assert:

  * The flux SHAPE is fixed by the geometry alone, so the peak-to-average power
    is a pure number (pi/2 for a slab, pi^2/3 for a sphere) with no material in
    it -- and it is why real cores are zoned and reflected.
  * Only the LOWEST eigenvalue is physical.  The higher harmonics go negative
    somewhere inside the core, and a negative neutron density is meaningless.

Fick's law is an approximation, and the module says where it fails rather than
letting it be used there: within a few transport mean free paths of a source, a
boundary, or a strong absorber, the flux is not diffusive at all.
"""

import math

__all__ = [
    "GEOMETRIES", "J0_FIRST_ZERO", "EXTRAPOLATION_COEFFICIENT",
    "fick_current", "diffusion_coefficient", "transport_mfp",
    "diffusion_length", "diffusion_length_squared",
    "plane_source_flux", "point_source_flux", "diffusion_valid",
    "material_buckling", "geometric_buckling", "critical_dimension",
    "critical_flux_profile", "peak_to_average", "extrapolation_distance",
    "extrapolated_dimension", "k_effective_from_buckling",
    "bessel_j0", "bessel_j1", "SLAB_CRITICALITY_ERRATA",
]

J0_FIRST_ZERO = 2.405            # S&F Table 10.10 (exact 2.404826)
EXTRAPOLATION_COEFFICIENT = 0.7104   # d = 0.7104 lambda_tr = 2.1312 D

# S&F Eq. (10.79) prints the criticality condition as B_mat = n pi/a after
# having just discarded every n > 1.  Table 10.10 gives (pi/a)^2.
SLAB_CRITICALITY_ERRATA = "B_mat = n pi / a"

# Table 10.10 (printed p. 362): the bare-core geometries.
GEOMETRIES = ("slab", "parallelepiped", "sphere", "infinite cylinder", "cylinder")


# --- Fick's law and the diffusion length  [S&F §10.10] -------------------

def fick_current(d, dphi_dx):
    """J = -D dphi/dx  [S&F Eq. (10.58)].

    The minus sign is the whole physical content: neutrons flow DOWN the
    gradient.  Fick wrote it for molecules in 1855; Fourier had written the same
    form for heat in 1823, and for the same reason -- both describe a random walk
    seen from far enough away that individual steps do not matter."""
    return -d * dphi_dx


def transport_mfp(sigma_tr):
    """lambda_tr = 1/Sigma_tr, the transport mean free path."""
    if sigma_tr <= 0:
        raise ValueError("the transport cross section must be positive")
    return 1.0 / sigma_tr


def diffusion_coefficient(sigma_tr):
    """D = 1/(3 Sigma_tr) = lambda_tr/3.

    S&F introduce D as an empirical constant of proportionality and never
    evaluate it; this is the standard P1 result, and it is what makes D a LENGTH
    rather than a free parameter."""
    return transport_mfp(sigma_tr) / 3.0


def diffusion_length_squared(d, sigma_a):
    """L^2 = D/Sigma_a  [S&F Eq. (10.66)]."""
    if d <= 0 or sigma_a <= 0:
        raise ValueError("D and Sigma_a must be positive")
    return d / sigma_a


def diffusion_length(d, sigma_a):
    """L = sqrt(D/Sigma_a) -- the length over which a fixed-source flux dies away
    by 1/e, and (as ~NE-19 uses it) one sixth of the mean square crow-flight
    distance from thermalisation to absorption."""
    return math.sqrt(diffusion_length_squared(d, sigma_a))


# --- fixed-source problems  [S&F §10.10.1] -------------------------------

def plane_source_flux(s0, x, d, l):
    """phi(x) = (S0 L / 2D) exp(-|x|/L)  [S&F Eq. (10.72)].

    An infinite plane source emitting S0 neutrons per unit area per unit time
    into a non-multiplying medium.  Pure exponential decay with scale L -- which
    is what L MEANS, before it acquires any interpretation involving random
    walks."""
    if s0 < 0 or d <= 0 or l <= 0:
        raise ValueError("source, D and L must be positive")
    return s0 * l / (2.0 * d) * math.exp(-abs(x) / l)


def point_source_flux(s, r, d, l):
    """phi(r) = S exp(-r/L)/(4 pi D r), for an isotropic point source.

    Beyond S&F, which only does the plane case, and worth having because it is
    the one that appears in shielding: note it is NOT S exp(-mu r)/(4 pi r^2),
    the uncollided form of ~NE-11.  Diffusion counts the SCATTERED population as
    well, so the geometric falloff is 1/r rather than 1/r^2 and the exponent uses
    L rather than the total mean free path."""
    if s < 0 or d <= 0 or l <= 0:
        raise ValueError("source, D and L must be positive")
    if r <= 0:
        raise ValueError("the point-source solution diverges at r = 0")
    return s * math.exp(-r / l) / (4.0 * math.pi * d * r)


def diffusion_valid(distance, sigma_tr, n_mfp=3.0):
    """Is diffusion theory trustworthy this far from a source or boundary?

    Fick's law assumes the flux is nearly linear over a mean free path and that
    the angular distribution is nearly isotropic.  Neither holds within a few
    transport mean free paths of a source, a vacuum boundary, or a strong
    absorber -- exactly where a control rod is.  S&F say this in §10.10.3 and
    then give no criterion; three transport mean free paths is the usual one."""
    if distance < 0:
        raise ValueError("distance cannot be negative")
    return distance >= n_mfp * transport_mfp(sigma_tr)


# --- criticality  [S&F §10.10.2, Table 10.10] ----------------------------

def material_buckling(k_inf, l2):
    """B_mat^2 = (k_inf - 1)/L^2  [S&F Eq. (10.73)].

    Depends only on the material.  It is positive only for k_inf > 1, which is
    the algebraic statement that a subcritical material cannot be made critical
    by any amount of geometry."""
    if l2 <= 0:
        raise ValueError("the diffusion area must be positive")
    return (k_inf - 1.0) / l2


def geometric_buckling(geometry, **dims):
    """B_g^2 for the bare geometries of S&F Table 10.10.

    slab(a); parallelepiped(a, b, c); sphere(R); infinite cylinder(R);
    cylinder(R, H).  Depends only on shape and size."""
    g = geometry.lower()
    try:
        if g == "slab":
            return (math.pi / dims["a"]) ** 2
        if g == "parallelepiped":
            return sum((math.pi / dims[k]) ** 2 for k in ("a", "b", "c"))
        if g == "sphere":
            return (math.pi / dims["R"]) ** 2
        if g == "infinite cylinder":
            return (J0_FIRST_ZERO / dims["R"]) ** 2
        if g == "cylinder":
            return (J0_FIRST_ZERO / dims["R"]) ** 2 + (math.pi / dims["H"]) ** 2
    except KeyError as exc:
        raise KeyError("geometry %r needs dimension %s" % (geometry, exc))
    raise KeyError("unknown geometry %r; have %s" % (geometry, list(GEOMETRIES)))


def critical_dimension(geometry, k_inf, l2, aspect=None):
    """The critical size, from B_g^2 = B_mat^2  [S&F Eq. (10.80)].

    Returns the characteristic dimension: `a` for a slab or cube, `R` for a
    sphere or infinite cylinder, and (R, H) for a finite cylinder with
    H = aspect*R.

    REFUSES k_inf <= 1.  Leakage can only remove neutrons, so no bare assembly
    of a subcritical material is critical at any size -- and the algebra says so
    by making B_mat^2 non-positive while every B_g^2 is strictly positive."""
    if k_inf <= 1.0:
        raise ValueError("k_inf = %.4f <= 1: B_mat^2 is not positive, so no bare "
                         "assembly of this material is critical at any size"
                         % k_inf)
    b2 = material_buckling(k_inf, l2)
    b = math.sqrt(b2)
    g = geometry.lower()
    if g == "slab":
        return math.pi / b
    if g == "parallelepiped":
        return math.pi * math.sqrt(3.0) / b            # a cube
    if g == "sphere":
        return math.pi / b
    if g == "infinite cylinder":
        return J0_FIRST_ZERO / b
    if g == "cylinder":
        if aspect is None:
            # the minimum-volume cylinder: H/R = pi/2.405 * sqrt(2)
            aspect = math.pi / J0_FIRST_ZERO * math.sqrt(2.0)
        r = math.sqrt((J0_FIRST_ZERO ** 2 + (math.pi / aspect) ** 2) / b2)
        return r, aspect * r
    raise KeyError("unknown geometry %r" % geometry)


def bessel_j0(x):
    """Bessel J0, Abramowitz & Stegun 9.4.1/9.4.3 (|err| < 5e-8)."""
    ax = abs(x)
    if ax < 8.0:
        y = x * x
        p = (57568490574.0 + y * (-13362590354.0 + y * (651619640.7 + y * (
            -11214424.18 + y * (77392.33017 + y * -184.9052456)))))
        q = (57568490411.0 + y * (1029532985.0 + y * (9494680.718 + y * (
            59272.64853 + y * (267.8532712 + y)))))
        return p / q
    z = 8.0 / ax
    y = z * z
    xx = ax - 0.785398164
    p = (1.0 + y * (-0.1098628627e-2 + y * (0.2734510407e-4 + y * (
        -0.2073370639e-5 + y * 0.2093887211e-6))))
    q = (-0.1562499995e-1 + y * (0.1430488765e-3 + y * (-0.6911147651e-5 + y * (
        0.7621095161e-6 + y * -0.934935152e-7))))
    return math.sqrt(0.636619772 / ax) * (math.cos(xx) * p - z * math.sin(xx) * q)


def bessel_j1(x):
    """Bessel J1, A&S 9.4.4/9.4.6."""
    ax = abs(x)
    if ax < 8.0:
        y = x * x
        p = x * (72362614232.0 + y * (-7895059235.0 + y * (242396853.1 + y * (
            -2972611.439 + y * (15704.48260 + y * -30.16036606)))))
        q = (144725228442.0 + y * (2300535178.0 + y * (18583304.74 + y * (
            99447.43394 + y * (376.9991397 + y)))))
        return p / q
    z = 8.0 / ax
    y = z * z
    xx = ax - 2.356194491
    p = (1.0 + y * (0.183105e-2 + y * (-0.3516396496e-4 + y * (
        0.2457520174e-5 + y * -0.240337019e-6))))
    q = (0.04687499995 + y * (-0.2002690873e-3 + y * (0.8449199096e-5 + y * (
        -0.88228987e-6 + y * 0.105787412e-6))))
    ans = math.sqrt(0.636619772 / ax) * (math.cos(xx) * p - z * math.sin(xx) * q)
    return -ans if x < 0 else ans


def critical_flux_profile(geometry, position, **dims):
    """The critical flux shape of S&F Table 10.10, normalised to a peak of 1.

    `position` is x for a slab, (x, y, z) for a parallelepiped, r for a sphere or
    infinite cylinder, and (r, z) for a cylinder.  The origin is at the centre.

    The shape contains NO material properties.  Once the geometry is fixed so is
    the power distribution, which is why power peaking is a pure number."""
    g = geometry.lower()
    if g == "slab":
        return math.cos(math.pi * position / dims["a"])
    if g == "parallelepiped":
        x, y, z = position
        return (math.cos(math.pi * x / dims["a"])
                * math.cos(math.pi * y / dims["b"])
                * math.cos(math.pi * z / dims["c"]))
    if g == "sphere":
        r, big_r = position, dims["R"]
        if r == 0:
            return 1.0                     # the removable singularity
        return (big_r / (math.pi * r)) * math.sin(math.pi * r / big_r)
    if g == "infinite cylinder":
        return bessel_j0(J0_FIRST_ZERO * position / dims["R"])
    if g == "cylinder":
        r, z = position
        return (bessel_j0(J0_FIRST_ZERO * r / dims["R"])
                * math.cos(math.pi * z / dims["H"]))
    raise KeyError("unknown geometry %r" % geometry)


def peak_to_average(geometry):
    """Peak-to-average flux (hence power) for a bare critical core.

    A pure number, with no material in it:

        slab            pi/2      = 1.571
        infinite cyl.   2.405/(2 J1(2.405)) = 2.316
        sphere          pi^2/3    = 3.290
        cylinder        the product = 3.639
        cube            (pi/2)^3  = 3.876

    These are why real cores are not bare and not uniform.  A factor of 3.6 in
    power density means the hottest fuel pin limits the whole reactor, so the
    centre gets depleted fuel, the edge gets fresh fuel, and a reflector is added
    to raise the edges (~NE-19 §10.6)."""
    g = geometry.lower()
    if g == "slab":
        return math.pi / 2.0
    if g == "sphere":
        return math.pi ** 2 / 3.0
    if g == "infinite cylinder":
        return J0_FIRST_ZERO / (2.0 * bessel_j1(J0_FIRST_ZERO))
    if g == "cylinder":
        return peak_to_average("infinite cylinder") * peak_to_average("slab")
    if g == "parallelepiped":
        return (math.pi / 2.0) ** 3
    raise KeyError("unknown geometry %r" % geometry)


def extrapolation_distance(d=None, sigma_tr=None):
    """d = 0.7104 lambda_tr = 2.1312 D, the linear-extrapolation distance.

    S&F set it to zero -- "generally very small compared to the size of the
    reactor" -- which is fine for a metre-scale power core and badly wrong for a
    small research assembly.  For graphite (lambda_tr ~ 2.5 cm) it is 1.8 cm; for
    a 20 cm assembly that is 9% of the dimension and ~20% in the buckling."""
    if sigma_tr is not None:
        return EXTRAPOLATION_COEFFICIENT * transport_mfp(sigma_tr)
    if d is not None:
        return 3.0 * EXTRAPOLATION_COEFFICIENT * d
    raise ValueError("give either D or Sigma_tr")


def extrapolated_dimension(physical, d=None, sigma_tr=None, faces=2):
    """The dimension the flux actually vanishes at: a + 2d for a slab."""
    return physical + faces * extrapolation_distance(d, sigma_tr)


def k_effective_from_buckling(k_inf, l2, buckling):
    """k_eff = k_inf/(1 + L^2 B^2), the one-speed non-leakage form.

    Compare ~NE-19's Eq. (10.13): P_NL^th = 1/(1 + L^2 B^2) is exactly this, so
    the thermal non-leakage probability that arrived there as an assertion is
    derived here."""
    if l2 < 0 or buckling < 0:
        raise ValueError("L^2 and B^2 must be non-negative")
    return k_inf / (1.0 + l2 * buckling)


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-21  neutron diffusion theory\n")

    print("  Fick's law and the diffusion length")
    sigma_tr, sigma_a = 0.4, 2.74e-4          # roughly graphite
    d = diffusion_coefficient(sigma_tr)
    l = diffusion_length(d, sigma_a)
    print("   Sigma_tr = %.2f /cm -> lambda_tr = %.2f cm, D = %.3f cm"
          % (sigma_tr, transport_mfp(sigma_tr), d))
    print("   Sigma_a = %.2e /cm  -> L = %.1f cm, L^2 = %.0f cm2  (~NE-19 Table 10.4: 55.4, 3070)"
          % (sigma_a, l, l * l))

    print("\n  the infinite plane source  [Eq. (10.72)]")
    print("   x (cm)   phi/phi(0)   diffusion valid?")
    for x in (0.0, 2.0, 7.5, 55.4, 150.0):
        print("   %6.1f %12.4f   %s"
              % (x, plane_source_flux(1.0, x, d, l) / plane_source_flux(1.0, 0.0, d, l),
                 "yes" if diffusion_valid(x, sigma_tr) else "NO -- within 3 mfp"))

    print("\n  criticality: material meets geometry  [Eq. (10.80)]")
    k_inf, l2 = 1.6939, 570.1                 # ~NE-19's 235U/graphite core
    b2 = material_buckling(k_inf, l2)
    print("   k_inf = %.4f, L^2 = %.1f cm2 -> B_mat^2 = %.4e cm-2" % (k_inf, l2, b2))
    print("   geometry            critical size        volume (m3)   peak/avg")
    r = critical_dimension("sphere", k_inf, l2)
    print("   %-18s R = %6.1f cm %14.2f %10.3f"
          % ("sphere", r, 4 / 3 * math.pi * r ** 3 / 1e6, peak_to_average("sphere")))
    a = critical_dimension("parallelepiped", k_inf, l2)
    print("   %-18s a = %6.1f cm %14.2f %10.3f"
          % ("cube", a, a ** 3 / 1e6, peak_to_average("parallelepiped")))
    rr, hh = critical_dimension("cylinder", k_inf, l2)
    print("   %-18s R = %6.1f, H = %6.1f %5.2f %10.3f"
          % ("cylinder (optimal)", rr, hh, math.pi * rr ** 2 * hh / 1e6,
             peak_to_average("cylinder")))
    print("   -> the sphere is the smallest, as it must be: least surface per volume")

    print("\n  the flux shape has no material in it")
    print("   position     slab      sphere    infinite cylinder")
    for frac in (0.0, 0.25, 0.5, 0.75, 0.95):
        print("   %.2f R    %8.4f %10.4f %14.4f"
              % (frac, critical_flux_profile("slab", frac * 0.5 * 100.0, a=100.0),
                 critical_flux_profile("sphere", frac * 100.0, R=100.0),
                 critical_flux_profile("infinite cylinder", frac * 100.0, R=100.0)))

    print("\n  the extrapolation distance S&F set to zero")
    print("   d = %.3f cm for this medium" % extrapolation_distance(sigma_tr=sigma_tr))
    for size in (20.0, 100.0, 400.0):
        ext = extrapolated_dimension(size, sigma_tr=sigma_tr)
        print("   a slab of %5.1f cm behaves as %6.2f cm: B^2 low by %5.1f%%"
              % (size, ext, 100 * (1 - (size / ext) ** 2)))

    print("\n  and it recovers ~NE-19's thermal non-leakage probability")
    for radius in (120.0, 126.7, 200.0):
        bb = geometric_buckling("sphere", R=radius)
        print("   R = %5.1f cm: L^2B^2 = %.4f, P_NL^th = %.4f, k_eff (1-speed) = %.4f"
              % (radius, l2 * bb, 1 / (1 + l2 * bb),
                 k_effective_from_buckling(k_inf, l2, bb)))


if __name__ == "__main__":
    _demo()
