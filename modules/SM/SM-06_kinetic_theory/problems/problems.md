# SM-06 — Problems

Work by hand, then check with `code/kinetic_theory.py`. Citations in `../refs.md`;
**Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  The three characteristic speeds  *(Pa §6.4, p.152)*
From f(v) = 4π(m/2πkT)^{3/2} v² e^{−mv²/2kT}, find v_p (peak), ⟨v⟩ (mean), and
v_rms, and show their ratio is 1 : √(4/π) : √(3/2), independent of T. *Check:*
`most_probable_speed`, `mean_speed`, `rms_speed` for N₂ at 300 K give 422, 476,
517 m/s.

*Answer:* $v_p=\sqrt{2kT/m}$, $\langle v\rangle=\sqrt{8kT/\pi m}$, $v_\text{rms}=\sqrt{3kT/m}$;
ratio $1:\sqrt{4/\pi}:\sqrt{3/2}$, independent of $T$.

**Solution.** Set $\alpha=\tfrac{m}{2kT}$, so $f(v)=4\pi(\alpha/\pi)^{3/2}v^2e^{-\alpha v^2}$. The
peak satisfies $\frac{d}{dv}\big(v^2e^{-\alpha v^2}\big)=0$, i.e. $2v=2\alpha v^3$, giving
$$v_p=\frac{1}{\sqrt\alpha}=\sqrt{\frac{2kT}{m}}.$$
The mean and mean-square use $\int_0^\infty v^3e^{-\alpha v^2}\,dv=\tfrac{1}{2\alpha^2}$ and
$\int_0^\infty v^4e^{-\alpha v^2}\,dv=\tfrac{3}{8}\sqrt\pi\,\alpha^{-5/2}$:
$$\langle v\rangle=\sqrt{\frac{8kT}{\pi m}},\qquad
v_\text{rms}=\sqrt{\langle v^2\rangle}=\sqrt{\frac{3kT}{m}}.$$
Dividing all three by $v_p$ gives $1:\sqrt{4/\pi}:\sqrt{3/2}$, with $kT/m$ cancelling so the ratio
is $T$-independent. For N$_2$ ($m=4.652\times10^{-26}$ kg) at $300$ K they evaluate to
$422,\,476,\,517$ m/s, matching `most_probable_speed`, `mean_speed`, `rms_speed`.

### P2.  Normalization and moments  *(Pa §6.4, p.152)*
Show ∫₀^∞ f(v) dv = 1 and ∫ v² f dv = 3kT/m, hence ⟨½mv²⟩ = (3/2)kT (equipartition).
*Check:* numerically integrate `maxwell_speed_pdf`; the moments match the closed forms
and `mean_kinetic_energy(T)`.

*Answer:* $\int_0^\infty f\,dv=1$ and $\langle v^2\rangle=3kT/m$, so
$\langle\tfrac12 mv^2\rangle=\tfrac32 kT$ (equipartition).

**Solution.** With $\alpha=\tfrac{m}{2kT}$ the prefactor is $4\pi(\alpha/\pi)^{3/2}$, and the
Gaussian moments are $\int_0^\infty v^2e^{-\alpha v^2}\,dv=\tfrac{\sqrt\pi}{4}\alpha^{-3/2}$ and
$\int_0^\infty v^4e^{-\alpha v^2}\,dv=\tfrac{3\sqrt\pi}{8}\alpha^{-5/2}$. Normalization is then
$$\int_0^\infty f\,dv=4\pi\Big(\frac{\alpha}{\pi}\Big)^{3/2}\frac{\sqrt\pi}{4}\alpha^{-3/2}=1,$$
and the second moment is
$$\langle v^2\rangle=4\pi\Big(\frac{\alpha}{\pi}\Big)^{3/2}\frac{3\sqrt\pi}{8}\alpha^{-5/2}
=\frac{3}{2\alpha}=\frac{3kT}{m}.$$
Hence $\langle\tfrac12 mv^2\rangle=\tfrac12 m\cdot\tfrac{3kT}{m}=\tfrac32 kT$ — equipartition,
$\tfrac12 kT$ per translational degree of freedom. Numerically integrating `maxwell_speed_pdf`
reproduces $\int f\,dv=1$, $\langle v^2\rangle=3kT/m$, and $\tfrac12 m\langle v^2\rangle=$
`mean_kinetic_energy(T)` $=6.21\times10^{-21}$ J at $300$ K.

### P3.  Mean free path and collision rate  *(Pa §6.4, p.152)*
Derive λ = 1/(√2 nσ) with σ = πd², and z = ⟨v⟩/λ. Estimate λ for air at 1 atm.
*Check:* `mean_free_path(n, 3.7e-10)` ≈ 67 nm at 1 atm; `collision_rate` = ⟨v⟩/λ.

*Answer:* $\lambda=1/(\sqrt2\,n\sigma)$ with $\sigma=\pi d^2$, and $z=\langle v\rangle/\lambda$;
for air at $1$ atm, $300$ K, $\lambda\approx67$ nm.

**Solution.** Model the molecule as a disk of cross-section $\sigma=\pi d^2$ (two centres collide
when their separation reaches $d$). In time $t$ it sweeps a volume $\sigma\langle v_\text{rel}\rangle t$
and strikes $n\sigma\langle v_\text{rel}\rangle t$ partners, so
$$\lambda=\frac{\text{distance travelled}}{\text{collisions}}
=\frac{\langle v\rangle t}{n\sigma\langle v_\text{rel}\rangle t}.$$
Averaging two independent Maxwellians gives $\langle v_\text{rel}\rangle=\sqrt2\,\langle v\rangle$, so
$\lambda=1/(\sqrt2\,n\sigma)$ and the collision frequency $z=\langle v\rangle/\lambda
=\sqrt2\,n\sigma\langle v\rangle$. At $1$ atm and $300$ K, $n=P/kT\approx2.45\times10^{25}\,\text{m}^{-3}$
and $\sigma=\pi(3.7\times10^{-10})^2$:
$$\lambda\approx67\ \text{nm},\qquad z\approx7.1\times10^{9}\ \text{s}^{-1}.$$
These reproduce `mean_free_path(n, 3.7e-10)` $\approx67$ nm and `collision_rate` $=\langle v\rangle/\lambda$.

### P4.  Effusion  *(Pa §6.4, p.152)*
Show the rate at which molecules pass through a small hole is Φ = ¼ n⟨v⟩, and explain
why lighter gases effuse faster (Graham's law). *Check:* `effusion_flux(n, m, T)` =
¼ n `mean_speed(m,T)`.

*Answer:* $\Phi=\tfrac14 n\langle v\rangle$; since $\langle v\rangle\propto m^{-1/2}$, lighter gases
effuse faster ($\Phi\propto1/\sqrt m$, Graham's law).

**Solution.** Place the hole at $x=0$; only molecules with $v_x>0$ escape, so the flux is
$$\Phi=n\int_0^\infty v_x\,g(v_x)\,dv_x,\qquad
g(v_x)=\sqrt{\frac{m}{2\pi kT}}\,e^{-mv_x^2/2kT},$$
with $g$ the one-dimensional Maxwellian. The integral is $\int_0^\infty v_x g\,dv_x=\sqrt{kT/2\pi m}$,
and since $\langle v\rangle=\sqrt{8kT/\pi m}$ this equals $\tfrac14\langle v\rangle$, giving
$$\Phi=\tfrac14 n\langle v\rangle.$$
Because $\langle v\rangle\propto m^{-1/2}$, at fixed $n,T$ the effusion rate scales as $1/\sqrt m$: a
lighter gas effuses faster, with rate ratio $\sqrt{m_2/m_1}$ (Graham's law). This is exactly
`effusion_flux(n, m, T)` $=\tfrac14 n\,$`mean_speed(m, T)`.

### P5.  The Einstein relation  *(Pa §15.2, p.587)*
For a Brownian particle with mobility µ, argue D = µkT, balancing diffusion against
drag. *Check:* `einstein_relation_diffusion(mu, T)` = µkT and scales linearly with
both µ and T.

*Answer:* $D=\mu kT$ — a fluctuation-dissipation relation, linear in $\mu$ and $T$.

**Solution.** Hold the Brownian particles in equilibrium under a weak force $F=-dU/dx$. Two currents
balance: a drift current $j_\text{drift}=n\mu F$ (mobility $\mu$ set by the drift speed $v=\mu F$)
and Fick diffusion $j_\text{diff}=-D\,dn/dx$. Zero net flux requires
$$n\mu F-D\frac{dn}{dx}=0.$$
Equilibrium also fixes the barometric law $n\propto e^{-U/kT}$, so
$\frac{dn}{dx}=-\frac{1}{kT}\frac{dU}{dx}\,n=\frac{F}{kT}n$. Substituting,
$$n\mu F-D\frac{F}{kT}n=0\quad\Rightarrow\quad D=\mu kT.$$
Diffusion (fluctuation) is tied to mobility (the response to drag) through $T$ — a
fluctuation-dissipation theorem. Thus `einstein_relation_diffusion(mu, T)` $=\mu kT$ is linear in
both $\mu$ and $T$ (doubling $T$ doubles $D$); at $\mu=10^{11}$ s/kg, $T=300$ K it returns
$4.14\times10^{-10}\,\text{m}^2/\text{s}$.
