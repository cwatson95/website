# CM-15 — Oscillations (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## Simple harmonic motion
A linear restoring force gives x″ + ω₀²x = 0 with solution x = A cos(ω₀t + φ)
[F §3.2 p.84]. Any system near a potential minimum looks like this with
ω₀ = √(U″/m) (`~CM-05`).

## Damping
Adding linear damping, x″ + 2γx′ + ω₀²x = 0 [F §3.4 p.96; MT §3.5 p.108]:
- **underdamped** (γ < ω₀): oscillates at ω_d = √(ω₀²−γ²) inside a decaying
  envelope e^{−γt} (code `damped_frequency`, `underdamped_solution`);
- **critically damped** (γ = ω₀) and **overdamped** (γ > ω₀): no oscillation.

The quality factor Q = ω₀/(2γ) counts the oscillations before the amplitude falls
by e^{−π}.

## Driven oscillator and resonance
With a sinusoidal drive F₀cos(ω_d t), the transient dies and a steady state
remains at the drive frequency with amplitude [F §3.6 p.113; MT §3.6 p.117]
$$A(\omega)=\frac{F_0}{\sqrt{(\omega_0^2-\omega^2)^2+(2\gamma\omega)^2}},$$
peaking (amplitude **resonance**) at ω = √(ω₀²−2γ²). Code: `driven_amplitude`,
`resonance_frequency`, `quality_factor`. The test integrates past the transient and
recovers A(ω) to ~1%. The identical mathematics is the driven RLC circuit
(`~EM-12`), and decomposing a many-body oscillation into independent driven modes
is `~CM-16`.
