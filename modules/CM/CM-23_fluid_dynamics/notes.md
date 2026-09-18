# CM-23 — Fluid Dynamics (notes)

Citation key (details + PDF pages in `refs.md`): **B** = Boas 3e.

## The velocity field
A flow is described by a velocity field **v**(x); its integral curves are
**streamlines** [B §6.10 p.314]. Two scalars built from the derivatives of **v**
characterize it locally:
- **divergence** ∇·v — the net rate of outflow per unit volume; **v** is
  **incompressible** when ∇·v = 0 [B §6.10 p.316] (`is_incompressible`);
- **vorticity** ω = ∇×v — twice the local angular velocity of a fluid element; a
  flow is **irrotational** when ∇×v = 0 (`vorticity`, `is_irrotational`).

Rigid rotation **v** = **Ω**×**r** has ω = 2**Ω** (constant) and is incompressible;
a potential flow **v** = ∇φ is irrotational by construction (curl of a gradient,
`~MA-02`); a radial source **v** = **r** is irrotational but compressible (∇·v = 3).

## The Euler equation and Bernoulli
A fluid element obeys Newton's law (the **Euler equation**)
$$\rho\frac{D\mathbf v}{Dt}=-\nabla p+\rho\mathbf g,$$
with the material derivative of `~CM-22`. For steady, incompressible, irrotational
flow this integrates along a streamline to **Bernoulli's equation**:
$$\tfrac12 v^2+\frac{p}{\rho}+gz=\text{const}.$$
Faster flow ⇒ lower pressure — lift, the Venturi effect, the curveball. Code:
`bernoulli_constant`.

*(Caveat: the ClassicalMechanics shelf has no dedicated fluid-dynamics text, so
the operators are cited to Boas's vector analysis; the Euler equation and
Bernoulli's relation are standard results stated here without a shelf page —
see `refs.md`.)*
