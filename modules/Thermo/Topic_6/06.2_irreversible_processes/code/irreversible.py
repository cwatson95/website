"""
irreversible.py  —  Module 6.2 (Irreversible Processes & Entropy Production)

A process is IRREVERSIBLE if the system and surroundings cannot both be restored to
their initial states (Moran 8e Sec. 5.3.1).  Every actual process is irreversible.
Whenever an irreversibility is present, ENTROPY IS PRODUCED within the system.  The
closed-system ENTROPY BALANCE (Sec. 6.7) accounts for it:

    S2 - S1 = integral_1^2 (dQ/T)_b + sigma                 (Eq. 6.24)
    [entropy change] = [entropy transfer] + [entropy production]

The second law requires (Eq. 6.26):

    sigma > 0   internal irreversibilities present
    sigma = 0   no internal irreversibilities (internally reversible)
    sigma < 0   IMPOSSIBLE

The ENTROPY CHANGE  S2 - S1  may be positive, negative, or zero (Eq. 6.27).  On a time-
rate basis the closed-system entropy rate balance is  dS/dt = sum(Qdot_j/Tj) + sigmadot
(Eq. 6.28).  For an ISOLATED system the entropy transfer vanishes, giving the INCREASE
OF ENTROPY PRINCIPLE (Eq. 6.30):

    DeltaS_isol = DeltaS_system + DeltaS_surr = sigma_isol >= 0

so processes proceed only in the direction that increases the total entropy of system +
surroundings.

Units: S,s [kJ/K, kJ/kg.K]; sigma [kJ/K]; Qdot [kW]; T [K or degR]; c [kJ/kg.K].
Citations: Moran 8e (PDF = printed + 18).  Worked Examples 6.2 (irreversible water,
sigma/m=4.9961 kJ/kg.K), 6.4 (gearbox, sigmadot=4e-3 kW/K), 6.5 (quenched bar, sigma=0.0864 Btu/degR).
"""
import math


# the eight common irreversibilities (Moran Sec. 5.3.1, p.249)
IRREVERSIBILITIES = [
    "Heat transfer through a finite temperature difference",
    "Unrestrained expansion of a gas or liquid to a lower pressure",
    "Spontaneous chemical reaction",
    "Spontaneous mixing of matter at different compositions or states",
    "Friction -- sliding friction and friction in the flow of fluids",
    "Electric current flow through a resistance",
    "Magnetization or polarization with hysteresis",
    "Inelastic deformation",
]


def entropy_production(dS, entropy_transfer):
    """Entropy production from the closed-system entropy balance, solved for sigma:
    sigma = (S2 - S1) - integral(dQ/T)_b.  [Moran Eq. 6.24, Sec. 6.7, p.305]"""
    return dS - entropy_transfer


def sigma_adiabatic(s2, s1):
    """Specific entropy production of an ADIABATIC process (entropy transfer = 0):
    sigma/m = s2 - s1.  [Moran Eq. 6.24 with Q=0, Sec. 6.7; Ex. 6.2, p.308]"""
    return s2 - s1


def entropy_production_rate(Qdot, Tb):
    """Steady-state entropy production rate for a system exchanging heat only at a single
    boundary temperature Tb (dS/dt = 0):  sigmadot = -Qdot/Tb.
    [Moran Eq. 6.28, Sec. 6.7.4; Ex. 6.4, p.311]"""
    return -Qdot / Tb


def sigma_isolated(dS_system, dS_surr):
    """Increase-of-entropy principle: total entropy produced in an isolated system =
    sum of the entropy changes of system and surroundings:
    sigma_isol = DeltaS_system + DeltaS_surr  (>= 0).  [Moran Eq. 6.30b, Sec. 6.8.1, p.313]"""
    return dS_system + dS_surr


def entropy_change_incompressible(m, c, T2, T1):
    """Entropy change of an incompressible substance with constant specific heat:
    DeltaS = m c ln(T2/T1).  T absolute.  [Moran Eq. 6.13, Sec. 6.4, p.298]"""
    return m * c * math.log(T2 / T1)


def is_possible(sigma, tol=1e-9):
    """Second-law feasibility test: a process is possible iff sigma >= 0.
    [Moran Eq. 6.26, Sec. 6.7, p.307]"""
    return sigma >= -tol


def classify_process(sigma, tol=1e-9):
    """Classify a process by its entropy production sigma (Eq. 6.26):
    sigma < 0 -> 'impossible'; sigma == 0 -> 'reversible'; sigma > 0 -> 'irreversible'.
    [Moran Eq. 6.26, Sec. 6.7, p.307]"""
    if sigma < -tol:
        return "impossible"
    if abs(sigma) <= tol:
        return "reversible"
    return "irreversible"


def _demo():
    print("Module 6.2 -- Irreversible Processes & Entropy Production  (sigma >= 0)\n")
    print("  The 8 common irreversibilities (M Sec. 5.3.1):")
    for i, s in enumerate(IRREVERSIBILITIES, 1):
        print("    %d. %s" % (i, s))
    # Example 6.2: water, adiabatic paddle-wheel stir, sat liquid -> sat vapor at 150 C.
    s1, s2 = 1.8418, 6.8379
    u1, u2 = 631.68, 2559.5
    W = -(u2 - u1)                          # energy balance, Q=0: W = -(u2-u1)
    sig = sigma_adiabatic(s2, s1)           # entropy transfer = 0
    print("\n  Ex 6.2 water (adiabatic, irreversible): W/m = %.2f kJ/kg  [book -1927.82]" % W)
    print("                                          sigma/m = %.4f kJ/kg.K [book 4.9961]" % sig)
    print("    same end states as the int.-rev. Ex 6.1 (sigma=0) -> sigma is NOT a property")
    # Example 6.4: gearbox at steady state, Q=-1.2 kW.
    print("\n  Ex 6.4 gearbox: sigmadot(Tb=300K) = %.1e kW/K [book 4.0e-3];"
          " sigmadot(Tf=293K) = %.1e [book 4.1e-3]"
          % (entropy_production_rate(-1.2, 300.0), entropy_production_rate(-1.2, 293.0)))
    # Example 6.5: quench 0.8-lb metal bar (1900 R) in 20 lb water (530 R).
    Tf = 535.0
    sig5 = (entropy_change_incompressible(20.0, 1.0, Tf, 530.0)
            + entropy_change_incompressible(0.8, 0.1, Tf, 1900.0))
    print("\n  Ex 6.5 quench: sigma = %.4f Btu/degR  [book 0.0864]  -> increase principle (>0)" % sig5)
    print("  feasibility: classify(-1e-3)=%s, classify(0)=%s, classify(2.0)=%s"
          % (classify_process(-1e-3), classify_process(0.0), classify_process(2.0)))


if __name__ == "__main__":
    _demo()
