# SM-06 — Non-equilibrium & Kinetic Theory (notes)

Kinetic theory follows the molecules. In equilibrium it reproduces thermodynamics
from the velocity distribution; out of equilibrium (gradients, collisions) it gives
**transport** — diffusion, viscosity, conduction — and Brownian motion.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria 3e;
**Sch** = Schroeder (image-only). Printed pages.

## 1. The Maxwell–Boltzmann speed distribution
From the Boltzmann factor on kinetic energy, weighted by the $4\pi v^2$ density of
velocity directions [Pa §6.4, p.152]:
$$f(v)=4\pi\Big(\frac{m}{2\pi kT}\Big)^{3/2}v^2\,e^{-mv^2/2kT}.$$
It has three **characteristic speeds**, in a temperature-independent ratio:
$$v_p=\sqrt{\frac{2kT}{m}}<\langle v\rangle=\sqrt{\frac{8kT}{\pi m}}<v_\text{rms}=\sqrt{\frac{3kT}{m}},
  \qquad 1:\sqrt{4/\pi}:\sqrt{3/2}.$$
$v_p$ is the peak of $f$, $\langle v\rangle$ the mean, $v_\text{rms}$ the
root-mean-square. Code: `maxwell_speed_pdf`, `most_probable_speed`, `mean_speed`,
`rms_speed`.

## 2. Equipartition
The mean translational energy is
$$\Big\langle\tfrac12 m v^2\Big\rangle=\tfrac12 m\,v_\text{rms}^2=\tfrac32 kT,$$
i.e. $\tfrac12 kT$ per translational degree of freedom — the same equipartition seen
in `~SM-03`. Code: `mean_kinetic_energy`.

## 3. Collisions: mean free path, collision rate, effusion
With collision cross-section $\sigma=\pi d^2$ the **mean free path** is [Pa §6.4]:
$$\lambda=\frac{1}{\sqrt2\,n\sigma},$$
the $\sqrt2$ from the distribution of *relative* speeds. The collision frequency is
$z=\langle v\rangle/\lambda$, and the **effusion** flux through a small hole is
$\Phi=\tfrac14 n\langle v\rangle$ (the rate molecules strike unit wall area). Code:
`mean_free_path`, `collision_rate`, `effusion_flux`.

## 4. Transport
Between collisions a molecule random-walks a step $\sim\lambda$ at speed
$\sim\langle v\rangle$, giving the kinetic-theory **self-diffusion** coefficient
$$D\simeq\tfrac13\langle v\rangle\lambda$$
(and, by the same argument, viscosity $\eta\sim\tfrac13 nm\langle v\rangle\lambda$
and thermal conductivity). Code: `diffusion_coefficient`.

## 5. Brownian motion and the Einstein relation
A particle suffering random kicks while also feeling drag (mobility $\mu$) obeys
**Einstein's relation** [Pa §15.2, p.587; §15.3, p.593]:
$$D=\mu kT,$$
a **fluctuation–dissipation** theorem linking the diffusion (fluctuation) to the
drag (dissipation) through temperature. Code: `einstein_relation_diffusion`. The
underlying **Boltzmann transport equation** $\partial_t f+\mathbf v\cdot\nabla f
+\mathbf F\cdot\nabla_{\!p}f=(\partial_t f)_\text{coll}$ is the bridge to `~PK-01`.

## Where this goes
- `~PK-01` — the Vlasov/Boltzmann equation and plasma kinetics (the KrF/LoKI code in this repo).
- `~CM-23` — taking velocity moments of the Boltzmann equation yields the fluid (Navier–Stokes) equations.
- `~SM-03` — the fluctuation–dissipation pattern (C = Var(E)/kT², D = µkT) recurs throughout statistical physics.
