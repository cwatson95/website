"""
open_systems.py  —  Module 1.1 (Open Systems / Control Volumes)

Control-volume (open-system) mass and energy rate balances, plus the standard
one-inlet/one-outlet steady-flow device idealizations, following

    Moran, Shapiro, Boettner & Bailey, *Fundamentals of Engineering
    Thermodynamics*, 8th ed., Chapter 4 ("Control Volume Analysis Using
    Energy").  Section titles cited in the docstrings; exact equation numbers
    and verified page numbers are in ../refs.md and ../notes.md.

Everything is plain functions over SI quantities so the pieces compose:

    h, u   specific enthalpy / internal energy   [kJ/kg]
    V      velocity                              [m/s]
    z      elevation                             [m]
    v      specific volume                       [m^3/kg]
    mdot   mass flow rate                        [kg/s]
    Qdot   heat transfer rate                    [kW]
    Wdot   power (shaft/CV work rate)            [kW]

Unit bookkeeping: kinetic (V^2/2) and potential (g z) energies come out in
J/kg, so they are divided by 1000 to add to enthalpy in kJ/kg.  A stream then
carries mdot * psi in kJ/s = kW, matching Qdot and Wdot.

A throwaway demo (steam turbine + nozzle + throttle, using the real
steam_tables/ CSVs through steam_lookup.py) runs under `python3 open_systems.py`.
"""
from __future__ import annotations
import math
from collections import namedtuple

G = 9.81  # standard gravity [m/s^2]

# A flowing stream crossing the control surface.  V, z default to 0 (the common
# "kinetic and potential energy changes negligible" modeling assumption).
Stream = namedtuple("Stream", ["mdot", "h", "V", "z"])
Stream.__new__.__defaults__ = (0.0, 0.0)   # defaults for (V, z)


# --------------------------------------------------------------- flow energy
def flow_energy(h, V=0.0, z=0.0):
    """Specific flow energy psi = h + V^2/2 + g z  [kJ/kg].

    This is the per-unit-mass energy carried across a control surface by flowing
    matter: internal energy + flow work (together = enthalpy h) plus kinetic and
    potential energy.  [Moran 8e, "Conservation of Energy for a Control Volume".]
    """
    return h + (0.5 * V * V + G * z) / 1000.0


def stream_energy(s: Stream):
    """Energy transport rate carried by a stream, mdot * psi  [kW]."""
    return s.mdot * flow_energy(s.h, s.V, s.z)


# --------------------------------------------------------------- mass balance
def mass_flow_rate(A, V, v):
    """One-dimensional mass flow rate  mdot = A V / v  [kg/s].

    A cross-sectional area [m^2], V normal velocity [m/s], v specific volume
    [m^3/kg].  Equivalent to rho A V.  [Moran 8e Eq. 4.4b, "Conservation of Mass
    for a Control Volume".]
    """
    return A * V / v


def mass_rate_residual(inlets, outlets):
    """Mass rate balance residual  dm_cv/dt = sum(mdot_in) - sum(mdot_out)  [kg/s].

    Zero at steady state.  [Moran 8e, "Conservation of Mass for a Control Volume".]
    """
    return sum(s.mdot for s in inlets) - sum(s.mdot for s in outlets)


def is_steady_mass(inlets, outlets, tol=1e-9):
    """True if the mass rate balance closes (steady-state continuity)."""
    return abs(mass_rate_residual(inlets, outlets)) <= tol


# ------------------------------------------------------------- energy balance
def energy_rate_residual(Qdot, Wdot, inlets, outlets):
    """Control-volume energy rate balance residual  [kW]:

        dE_cv/dt = Qdot - Wdot + sum(mdot*psi)_in - sum(mdot*psi)_out .

    Zero at steady state.  Sign convention (Moran): Qdot > 0 INTO the CV,
    Wdot > 0 done BY the CV (e.g. a turbine).  [Moran 8e Eq. 4.15, "Conservation
    of Energy for a Control Volume".]
    """
    return (Qdot - Wdot
            + sum(stream_energy(s) for s in inlets)
            - sum(stream_energy(s) for s in outlets))


# ----------------------------------------- steady one-in/one-out shaft devices
def shaft_power(inlet: Stream, outlet: Stream, Qdot=0.0):
    """Steady 1-in/1-out shaft power  Wdot_cv = Qdot + mdot_in*psi_in - mdot_out*psi_out
    [kW].  Positive => work OUT of the CV (turbine); negative => work IN
    (compressor/pump).  Continuity (inlet.mdot == outlet.mdot) is the caller's
    responsibility.  [Moran 8e, "Analyzing Control Volumes at Steady State".]
    """
    return Qdot + stream_energy(inlet) - stream_energy(outlet)


def turbine_power(inlet: Stream, outlet: Stream, Qdot=0.0):
    """Turbine power output  [kW] (>0 for a real turbine).  Often Qdot ~ 0.
    [Moran 8e, "Turbines".]"""
    return shaft_power(inlet, outlet, Qdot)


def compressor_power(inlet: Stream, outlet: Stream, Qdot=0.0):
    """Compressor/pump power INPUT magnitude  [kW] (>0).  This is -Wdot_cv.
    [Moran 8e, "Compressors and Pumps".]"""
    return -shaft_power(inlet, outlet, Qdot)


# ------------------------------------------------- devices with no shaft work
def nozzle_exit_velocity(h_in, h_out, V_in=0.0):
    """Exit velocity of an adiabatic nozzle  [m/s].

    Model: Wdot = 0, Qdot ~ 0, dpe ~ 0, so h_in + V_in^2/2 = h_out + V_out^2/2,
    giving  V_out = sqrt(V_in^2 + 2*1000*(h_in - h_out))  (the 1000 converts the
    kJ/kg enthalpy drop to J/kg).  [Moran 8e Eq. 4.21, "Nozzles and Diffusers".]
    """
    return math.sqrt(V_in * V_in + 2.0 * 1000.0 * (h_in - h_out))


def diffuser_exit_enthalpy(h_in, V_in, V_out=0.0):
    """Exit enthalpy of an adiabatic diffuser  [kJ/kg]:
    h_out = h_in + (V_in^2 - V_out^2)/2000.  [Moran 8e, "Nozzles and Diffusers".]"""
    return h_in + (V_in * V_in - V_out * V_out) / 2000.0


def throttle_exit_enthalpy(h_in):
    """Throttling process is isenthalpic: h_out = h_in.

    Model: Wdot = 0, Qdot ~ 0, dke ~ 0, dpe ~ 0.  Pressure drops at constant
    enthalpy (a key idealization for expansion valves and the throttling
    calorimeter).  [Moran 8e Eq. 4.22, "Throttling Devices".]
    """
    return h_in


# ------------------------------------------------- multi-stream steady devices
def mixing_exit_enthalpy(inlets):
    """Adiabatic mixing-chamber exit enthalpy  [kJ/kg]:
    h_out = sum(mdot*h) / sum(mdot)   (Qdot = Wdot = 0, dke = dpe = 0).
    [Moran 8e, "Heat Exchangers" / direct-contact mixing.]"""
    M = sum(s.mdot for s in inlets)
    if M == 0:
        raise ValueError("total inlet mass flow is zero")
    return sum(s.mdot * s.h for s in inlets) / M


def heat_exchanger_flow_ratio(h_hot_in, h_hot_out, h_cold_in, h_cold_out):
    """Closed (no-mixing) heat exchanger flow-rate ratio  mdot_cold / mdot_hot.

    From the overall energy balance with Qdot = Wdot = 0 (control volume around
    BOTH streams):  mdot_hot (h_hot_in - h_hot_out) = mdot_cold (h_cold_out -
    h_cold_in).  [Moran 8e, "Heat Exchangers".]
    """
    return (h_hot_in - h_hot_out) / (h_cold_out - h_cold_in)


# ------------------------------------------------------------------- demo ----
def _demo():
    import steam_lookup as st

    print("Module 1.1 — Open systems: worked examples using steam_tables/\n")

    # (1) Steam turbine: 60 bar / 400 C  ->  0.10 bar, quality x2 = 0.90
    h1 = st.h_superheated(60.0, 400.0)          # from A-4
    h2 = st.h_two_phase(0.10, 0.90)             # hf + x*hfg from A-3
    sin = Stream(mdot=1.0, h=h1)
    sout = Stream(mdot=1.0, h=h2)
    w = turbine_power(sin, sout)                # kW per (kg/s)
    print(f"(1) Turbine  h1={h1:.1f}  h2={h2:.1f} kJ/kg  ->  Wdot/mdot = {w:.1f} kJ/kg")
    print(f"    energy balance closes: residual = {energy_rate_residual(0.0, w, [sin], [sout]):.2e} kW")

    # with kinetic energy (V1=10, V2=90 m/s)
    sin_k = Stream(1.0, h1, V=10.0)
    sout_k = Stream(1.0, h2, V=90.0)
    print(f"    including ke (10->90 m/s): Wdot/mdot = {turbine_power(sin_k, sout_k):.1f} kJ/kg")

    # (2) Nozzle: drop 80 kJ/kg of enthalpy from rest
    Vout = nozzle_exit_velocity(h_in=3000.0, h_out=2920.0, V_in=10.0)
    print(f"(2) Nozzle  dh=80 kJ/kg, V_in=10 m/s  ->  V_out = {Vout:.1f} m/s")

    # (3) Throttle: pressure drops at constant h (R-134a-like value)
    print(f"(3) Throttle  h_out = h_in = {throttle_exit_enthalpy(271.0):.1f} kJ/kg (isenthalpic)")

    # (4) Mass flow rate
    print(f"(4) mdot = A V / v, A=0.1 m^2, V=20 m/s, v=0.2 m^3/kg  ->  "
          f"{mass_flow_rate(0.1, 20.0, 0.2):.1f} kg/s")


if __name__ == "__main__":
    _demo()
