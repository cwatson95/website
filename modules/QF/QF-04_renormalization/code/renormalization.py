"""QF-04  Renormalization & the renormalization group.

Physics topic network, module QF-04 (modules/topic_network.txt).
Source: Peskin & Schroeder, *An Introduction to Quantum Field Theory*
(Ch. 7 the running electric charge; Ch. 10 the systematics of renormalization;
Ch. 12 the renormalization group).  Builds on ~QF-02 (the loop integrals that
diverge) and ~QF-03 (the QED coupling); the fixed-point / critical-exponent story
is the same renormalization group as ~SM-05 (Ising criticality, Wilson-Fisher).

Loop corrections in QFT are UV-divergent.  One **regularizes** them (a momentum
cutoff Lambda, or dimensional regularization) and then **renormalizes**: the bare
couplings absorb the cutoff so that physical (renormalized) quantities are finite.
The price is that the renormalized coupling depends on the sliding scale mu at
which it is defined.  How it slides is the **beta function**

    beta(g) = mu d g / d mu ,

and its solution g(mu) is the **running coupling**.  Two headline cases:

  * QED:  beta(alpha) = +2 alpha^2 / 3pi > 0, so the closed form
        alpha(Q) = alpha(mu) / [1 - (alpha(mu)/3pi) ln(Q^2/mu^2)]
    GROWS with energy (alpha(0) ~ 1/137 -> alpha(M_Z) ~ 1/128) and hits a
    **Landau pole** where the denominator vanishes (astronomically high in QED).
  * phi^4:  beta(lambda) = +3 lambda^2 / 16pi^2 > 0 -- same sign, "triviality."

The opposite sign (non-abelian gauge theory, QCD: beta < 0) gives **asymptotic
freedom** -- the coupling shrinks at high energy.  A zero beta(g*) = 0 is a
**fixed point**; the sign of beta'(g*) sets its stability, and those linearized
eigenvalues are exactly the critical exponents of statistical mechanics (~SM-05).

Conventions: energies/scales in GeV; alpha = e^2/4pi is the fine-structure
constant; mu, Q, Q0 are renormalization / probe scales.  Self-contained
(numpy + scipy only).
"""

import numpy as np
from scipy.integrate import solve_ivp

__all__ = [
    # constants
    "ALPHA0", "M_E", "M_Z", "M_MU", "M_TAU", "SM_FERMIONS",
    # QED running & Landau pole
    "beta_qed", "qed_running_alpha", "qed_landau_pole", "qed_alpha_sm",
    # phi^4
    "beta_phi4", "phi4_running", "phi4_landau_pole",
    # asymptotic freedom (QCD, the beta < 0 contrast)
    "beta_qcd", "qcd_running_alpha",
    # fixed points (the bridge to ~SM-05)
    "beta_toy", "fixed_point",
]

# --- physical constants (GeV) ------------------------------------------------

ALPHA0 = 1.0 / 137.036          # fine-structure constant at low energy, alpha(0)
M_E = 0.000510999              # electron mass [GeV]
M_MU = 0.1056584               # muon mass [GeV]
M_TAU = 1.77686                # tau mass [GeV]
M_Z = 91.1876                  # Z-boson mass [GeV] (the standard high-scale probe)

# Charged Standard-Model fermions below M_Z as (name, mass[GeV], |charge|, N_colour).
# Light-quark "masses" are EFFECTIVE hadronic-threshold scales (~0.3 GeV), not the
# tiny current masses: the genuine low-energy hadronic vacuum polarization is
# data-driven (the R-ratio), and ~0.3 GeV is the standard back-of-envelope stand-in
# (Peskin Ch. 7).  With this content the one-loop threshold sum reproduces the
# measured alpha(M_Z)^-1 ~ 128.
SM_FERMIONS = [
    ("e",   M_E,    1.0,     1),
    ("mu",  M_MU,   1.0,     1),
    ("tau", M_TAU,  1.0,     1),
    ("u",   0.30,   2.0 / 3, 3),
    ("d",   0.30,   1.0 / 3, 3),
    ("s",   0.50,   1.0 / 3, 3),
    ("c",   1.27,   2.0 / 3, 3),
    ("b",   4.18,   1.0 / 3, 3),
]


# --- QED: beta function, running coupling, Landau pole -----------------------

def beta_qed(alpha, sum_q2=1.0):
    """One-loop QED beta function  beta(alpha) = mu d alpha/d mu = (2/3pi) S alpha^2.

    S = sum_q2 = sum_f Q_f^2 N_c^f over the charged fermions in the loop (S = 1 for
    the electron alone).  Positive -> alpha GROWS toward the UV (Peskin Ch. 7, 12).
    """
    return (2.0 / (3.0 * np.pi)) * sum_q2 * alpha ** 2


def qed_running_alpha(Q, alpha0=ALPHA0, Q0=M_E, sum_q2=1.0):
    """One-loop QED running coupling (closed form, Peskin Ch. 7 eq. for alpha(q^2)):

        alpha(Q) = alpha0 / [ 1 - (alpha0/3pi) S ln(Q^2/Q0^2) ],   S = sum_q2.

    alpha0 = alpha(Q0).  With the default S = 1 this is the electron-only result;
    alpha increases with Q and diverges at the Landau pole (denominator -> 0).
    """
    # ln(Q^2/Q0^2) = 2 ln(Q/Q0); the split form avoids float overflow when Q is
    # near the (astronomically high) Landau scale.
    denom = 1.0 - (alpha0 / (3.0 * np.pi)) * sum_q2 * 2.0 * np.log(Q / Q0)
    return alpha0 / denom


def qed_landau_pole(alpha0=ALPHA0, Q0=M_E, sum_q2=1.0):
    """Scale where one-loop alpha(Q) diverges (denominator -> 0):

        Q_Landau = Q0 exp( 3pi / (2 alpha0 S) ),   S = sum_q2.

    For electron-only QED this is ~10^277 GeV, far above the Planck scale
    (~10^19 GeV): the QED Landau pole is unphysically high, signalling only that
    perturbative QED cannot be the whole story at such energies (Peskin Ch. 12).
    """
    return Q0 * np.exp(3.0 * np.pi / (2.0 * alpha0 * sum_q2))


def qed_alpha_sm(Q, alpha0=ALPHA0, fermions=SM_FERMIONS):
    """alpha(Q) including ALL charged SM fermions, via the one-loop threshold sum

        1/alpha(Q) = 1/alpha0 - (1/3pi) sum_f Q_f^2 N_c^f ln(Q^2/m_f^2),

    each fermion contributing only above its threshold (m_f < Q).  Run from the
    Thomson limit alpha0 = alpha(0) ~ 1/137 up to Q = M_Z this returns
    alpha(M_Z)^-1 ~ 128, the measured value (Peskin Ch. 7).
    """
    inv = 1.0 / alpha0
    for _name, m, q, nc in fermions:
        if Q > m:
            inv -= (1.0 / (3.0 * np.pi)) * (q ** 2) * nc * 2.0 * np.log(Q / m)
    return 1.0 / inv


# --- phi^4: beta function, running coupling, triviality pole -----------------

def beta_phi4(lam):
    """One-loop phi^4 beta function  beta(lambda) = 3 lambda^2 / 16pi^2 > 0
    (Peskin Ch. 10, 12).  Same sign as QED: lambda grows toward the UV."""
    return 3.0 * lam ** 2 / (16.0 * np.pi ** 2)


def phi4_running(lam0, mu0, mu):
    """Running phi^4 coupling, obtained by NUMERICALLY integrating

        d lambda / d ln(mu) = beta_phi4(lambda) = 3 lambda^2 / 16pi^2

    from mu0 to mu (scipy solve_ivp).  Equivalent closed form
        1/lambda(mu) = 1/lam0 - (3/16pi^2) ln(mu/mu0).
    """
    s0, s1 = np.log(mu0), np.log(mu)
    sol = solve_ivp(lambda _s, y: beta_phi4(y[0]), (s0, s1), [lam0],
                    rtol=1e-10, atol=1e-12, dense_output=True)
    return float(sol.y[0, -1])


def phi4_landau_pole(lam0, mu0):
    """Triviality (Landau) scale where the phi^4 closed form diverges:

        mu_pole = mu0 exp( 16pi^2 / (3 lam0) ).

    Above it the one-loop coupling is infinite; demanding a finite continuum limit
    forces lam0 -> 0 ("triviality" of phi^4, Peskin Ch. 12)."""
    return mu0 * np.exp(16.0 * np.pi ** 2 / (3.0 * lam0))


# --- QCD: the beta < 0 contrast (asymptotic freedom) -------------------------

def beta_qcd(alpha_s, nf=5):
    """One-loop QCD beta function  beta(alpha_s) = -(b0/2pi) alpha_s^2,
    b0 = 11 - (2/3) nf  (SU(3): 11/3 C_A - 4/3 T_F nf with C_A=3, T_F=1/2).

    NEGATIVE for nf < 16.5 -> alpha_s SHRINKS toward the UV: **asymptotic freedom**
    (Peskin Ch. 16, 17).  Opposite sign to QED/phi^4."""
    b0 = 11.0 - (2.0 / 3.0) * nf
    return -(b0 / (2.0 * np.pi)) * alpha_s ** 2


def qcd_running_alpha(Q, alpha_s0=0.1181, Q0=M_Z, nf=5):
    """One-loop QCD running coupling (closed form):

        1/alpha_s(Q) = 1/alpha_s0 + (b0/4pi) ln(Q^2/Q0^2),   b0 = 11 - (2/3) nf.

    alpha_s0 = alpha_s(Q0) (default alpha_s(M_Z) ~ 0.118).  Because b0 > 0 the
    coupling DECREASES as Q grows -- asymptotic freedom (Peskin Ch. 16, 17)."""
    b0 = 11.0 - (2.0 / 3.0) * nf
    inv = 1.0 / alpha_s0 + (b0 / (4.0 * np.pi)) * 2.0 * np.log(Q / Q0)
    return 1.0 / inv


# --- fixed points: the bridge to critical phenomena (~SM-05) -----------------

def beta_toy(g, a, b):
    """Toy beta function  beta(g) = a g^2 - b g^3  with two zeros g = 0 and
    g* = a/b (a,b > 0).  A minimal model of a non-trivial fixed point."""
    return a * g ** 2 - b * g ** 3


def fixed_point(a, b):
    """Non-trivial fixed point of beta(g) = a g^2 - b g^3 and its stability.

    Zeros: g = 0 (Gaussian/free) and  g* = a/b.  The slope there is
        beta'(g*) = 2 a g* - 3 b g*^2 = -a^2/b  < 0  (for a,b > 0),
    so g* is **UV-attractive** (couplings flow INTO g* as mu -> infinity); the
    origin, with beta ~ a g^2 > 0, is UV-repulsive / IR-attractive.  The linearized
    slope beta'(g*) is the analogue of the RG eigenvalue that fixes the critical
    exponents of statistical mechanics (Wilson-Fisher, Peskin Ch. 12-13; ~SM-05).

    Returns a dict: g_star, beta_prime, uv_attractive (bool), stability (str).
    """
    g_star = a / b
    beta_prime = 2.0 * a * g_star - 3.0 * b * g_star ** 2     # = -a^2/b
    uv_attractive = beta_prime < 0.0
    return {
        "g_star": g_star,
        "beta_prime": beta_prime,
        "uv_attractive": uv_attractive,
        "stability": "UV-attractive" if uv_attractive else "UV-repulsive",
    }


# --- demo --------------------------------------------------------------------

def _demo():
    print("QF-04  Renormalization & the renormalization group -- demo")
    print("=" * 60)

    # 1) QED running coupling: alpha grows with energy (electron-only closed form)
    print("\n1) QED running coupling alpha(Q) -- electron-only closed form:")
    for Q, label in [(M_E, "m_e"), (1.0, "1 GeV"), (M_Z, "M_Z"), (1.0e3, "1 TeV")]:
        a = qed_running_alpha(Q)
        print(f"   alpha({label:>5}) = {a:.6e}  = 1/{1.0 / a:7.2f}")
    print("   -> alpha increases monotonically with Q (beta_qed > 0).")

    # 2) alpha(M_Z) from alpha(0): electron-only vs the full SM fermion content
    a_e = qed_running_alpha(M_Z)
    a_sm = qed_alpha_sm(M_Z)
    print("\n2) alpha(M_Z) from alpha(0) = 1/%.3f :" % (1.0 / ALPHA0))
    print(f"   electron loop only      : 1/{1.0 / a_e:6.2f}")
    print(f"   all charged SM fermions : 1/{1.0 / a_sm:6.2f}   (measured ~ 1/128)")

    # 3) the QED Landau pole
    QL = qed_landau_pole()
    print("\n3) QED Landau pole (denominator -> 0):")
    print(f"   Q_Landau = {QL:.3e} GeV  ~ 10^{np.log10(QL):.0f} GeV")
    print(f"   (Planck scale ~ 1e19 GeV) -> unphysically high; QED is incomplete first.")

    # 4) phi^4 running: same-sign beta, integrated numerically, triviality scale
    lam0, mu0, mu = 1.0, 1.0, 1.0e10
    lam = phi4_running(lam0, mu0, mu)
    lam_closed = 1.0 / (1.0 / lam0 - 3.0 / (16.0 * np.pi ** 2) * np.log(mu / mu0))
    print("\n4) phi^4 coupling (beta = 3 lambda^2/16pi^2 > 0), lambda0 = %.1f at mu0 = %.0f GeV:" % (lam0, mu0))
    print(f"   integrated lambda({mu:.0e} GeV) = {lam:.6f}   (closed form {lam_closed:.6f})")
    print(f"   triviality (Landau) scale       = {phi4_landau_pole(lam0, mu0):.3e} GeV")

    # 5) the beta < 0 contrast: QCD asymptotic freedom
    print("\n5) QCD (non-abelian, beta < 0): asymptotic freedom, alpha_s(M_Z) = 0.1181:")
    for Q, label in [(2.0, "2 GeV"), (M_Z, "M_Z"), (1.0e3, "1 TeV")]:
        print(f"   alpha_s({label:>5}) = {qcd_running_alpha(Q):.4f}")
    print(f"   beta_qcd(0.118) = {beta_qcd(0.1181):+.5f} < 0  -> coupling shrinks at high Q.")

    # 6) toy fixed point and the bridge to critical phenomena (~SM-05)
    a, b = 2.0, 4.0
    fp = fixed_point(a, b)
    print("\n6) toy beta(g) = a g^2 - b g^3,  a = %.1f, b = %.1f :" % (a, b))
    print(f"   g* = a/b = {fp['g_star']:.4f};  beta'(g*) = {fp['beta_prime']:+.4f}  ({fp['stability']})")
    print("   beta'(g*) is the linearized RG eigenvalue -> critical exponents (~SM-05).")


if __name__ == "__main__":
    _demo()
