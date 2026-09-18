# RE-06 — Problems

Work them by hand, then check with `code/rel_dynamics.py`. Sources in `../refs.md`.

### P1. Kinetic energy n times the rest energy  *(Griffiths 4e, Prob. 12.30, p.537)*
A particle's kinetic energy equals `n` times its rest energy. Find its speed.
*Answer:* `γ = n+1`, so `v = c√(1 − 1/(n+1)²)`. For `n=1`: `v = √3/2 c ≈ 0.866c`.
*Check:* solve `kinetic_energy(1, [v,0,0]) = 1` ⇒ `v ≈ 0.866`.

**Solution.** Kinetic energy is $T=(\gamma-1)m$, and "$T=n$ times the rest energy $m$" means
$(\gamma-1)m=nm$, hence
$$\gamma=n+1\quad\Longrightarrow\quad v=c\sqrt{1-\frac{1}{\gamma^2}}=c\sqrt{1-\frac{1}{(n+1)^2}} .$$
For $n=1$ the kinetic energy equals the rest energy, so $\gamma=2$ and
$v=\sqrt{1-\tfrac14}=\sqrt3/2\approx0.866\,c$. (As $n\to\infty$, $\gamma\to\infty$ but $v\to c$:
more kinetic energy buys ever less speed.) Solving `kinetic_energy(1, [v,0,0]) = 1` indeed
returns $v\approx0.866$, with $\gamma=2$.

### P2. The mass shell  *(Griffiths 4e, §12.2.2, p.535)*
Show `E² − |𝐩|²c² = m²c⁴` for any speed, and that a massless particle has `E=|𝐩|c`.
*Check:* for any `(m,v)`, `energy(m,v)² − Σ momentum(m,v)² = m²`; and
`interval2(photon_four_momentum(E, n̂)) = 0`.

**Solution.** With $E=\gamma m$ and $\mathbf p=\gamma m\mathbf v$,
$$E^2-|\mathbf p|^2=\gamma^2m^2-\gamma^2m^2|\mathbf v|^2=\gamma^2m^2\big(1-|\mathbf v|^2\big)=m^2,$$
since $\gamma^2(1-|\mathbf v|^2)=1$ at every speed; restoring units, $E^2-|\mathbf p|^2c^2=m^2c^4$.
This is just $p\cdot p=-m^2$ in mostly-plus signs. Taking $m\to0$ at fixed $E$ forces
$|\mathbf p|=E$: a massless particle is **null** ($p\cdot p=0$) and moves at $c$. Hence
`energy(m,v)² − Σ momentum(m,v)²`$=m^2$ for any $(m,v)$, and
`interval2(photon_four_momentum(E, n̂))`$=0$.

### P3. Invariant mass of a system  *(Griffiths 4e, Prob. 12.31, p.537)*
Two photons of energy `E` fly off back-to-back. What is the invariant mass of the
pair? Could a single photon have done this?
*Answer:* `M = 2E ≠ 0` — a massive system from massless parts; a single photon has
`M=0`, so a lone photon can't decay to mass (4-momentum forbids it).
*Check:* `system_invariant_mass([photon_four_momentum(E,[1,0,0]), photon_four_momentum(E,[-1,0,0])]) = 2E`.

**Solution.** Each photon carries a null 4-momentum $p_{1,2}=(E,\pm E,0,0)$, so the pair's
total is
$$P^\mu=p_1^\mu+p_2^\mu=(2E,\ 0,0,0),\qquad M=\sqrt{-P\cdot P}=\sqrt{(2E)^2}=2E\neq0 .$$
The 3-momenta cancel while the energies add, so the *system* is massive ($M=2E$) though each
part is massless — mass belongs to the total 4-momentum, not to individual particles. A single
photon instead has $P\cdot P=-E^2+E^2=0$, so $M=0$, and it can never decay into massive
products: 4-momentum conservation cannot turn one null vector into a timelike one. Thus
`system_invariant_mass([photon_four_momentum(E,[1,0,0]), photon_four_momentum(E,[-1,0,0])])`$=2E$.

### P4. Inelastic collision gets heavier  *(notes §5)*
Two lumps of clay, each mass `m` at `±0.8c`, collide and stick. Find the rest mass
of the blob.
*Answer:* `M = 2γm = 2(1.667)m = 3.33m > 2m` — the kinetic energy became mass.
*Check:* `inelastic_stick(1, [0.8,0,0], 1, [-0.8,0,0])` → `(3.333, [0,0,0])`.

**Solution.** At $\beta=0.8$, $\gamma=1/\sqrt{1-0.64}=1/0.6=5/3$. The lumps carry opposite
momenta, so the total 4-momentum is purely temporal:
$$P^\mu=(\gamma m+\gamma m,\ \gamma m v-\gamma m v,0,0)=(2\gamma m,\,0,0,0).$$
With no net 3-momentum the blob is born at rest, and its rest mass is the system invariant mass
$$M=\sqrt{-P\cdot P}=2\gamma m=2\cdot\tfrac53\cdot1=\tfrac{10}{3}\approx3.33>2m .$$
The lost kinetic energy $2(\gamma-1)m$ did not disappear — it became rest mass ($E=mc^2$).
This is `inelastic_stick(1, [0.8,0,0], 1, [-0.8,0,0])`→`(3.333, [0,0,0])`.

### P5. The antiproton threshold  *(Griffiths 4e, §12.2.3, p.537)*
In `p + p → p + p + p + p̄` (a proton beam on a stationary proton target), find the
minimum beam kinetic energy.
*Answer:* `T = 6m_p c² ≈ 5.6 GeV` (the 1955 Bevatron discovery energy).
*Check:* `threshold_kinetic_energy(1, 1, 4) = 6` (in units `m_p=1`).

**Solution.** The invariant $s=-P\cdot P$ is frame-independent. In the lab (beam energy $E_b$,
momentum $p_b$, on a target $m_p$ at rest), using $E_b^2-p_b^2=m_p^2$,
$$s=(E_b+m_p)^2-p_b^2=2E_bm_p+2m_p^2 .$$
At threshold the four final particles ($M=4m_p$) sit at rest in the centre-of-momentum frame,
so $s=M^2=16m_p^2$. Equating,
$$2E_bm_p+2m_p^2=16m_p^2\ \Rightarrow\ E_b=7m_p\ \Rightarrow\ T=E_b-m_p=6m_p .$$
The beam needs $6m_pc^2\approx5.6$ GeV of kinetic energy — the 1955 Bevatron antiproton
threshold. So `threshold_kinetic_energy(1, 1, 4)`$=6$.

### P6. Pion decay & Compton  *(Griffiths 4e, Prob. 12.34, p.541; §12.2)*
(a) A neutral pion at rest decays to two photons; show each has energy `m_π c²/2`.
(b) A photon backscatters (`θ=π`) off an electron; find the wavelength shift.
*Answers:* (a) `E_γ = m_π/2` each, opposite directions. (b) `Δλ = 2ℏ/m_e c` (two
Compton wavelengths) — the maximum possible shift.
*Check:* `compton_shift(math.pi, 1.0) = 2.0`; `compton_shift(0,1)=0`.

**Solution.** (a) The pion at rest has $P^\mu=(m_\pi,\mathbf 0)$. Momentum conservation sends
the two photons back-to-back with $|\mathbf p_1|=|\mathbf p_2|$, and since each is null,
$E_i=|\mathbf p_i|$; energy conservation $E_1+E_2=m_\pi$ with $E_1=E_2$ then gives
$$E_\gamma=\frac{m_\pi}{2}\quad\text{each, in opposite directions.}$$
(b) Compton scattering shifts the wavelength by $\Delta\lambda=\dfrac{\hbar}{m_ec}(1-\cos\theta)$;
on backscatter $\theta=\pi$,
$$\Delta\lambda=\frac{\hbar}{m_ec}(1-\cos\pi)=\frac{2\hbar}{m_ec},$$
two Compton wavelengths — the maximum possible shift, versus zero in the forward direction.
In natural units this is `compton_shift(math.pi, 1.0)`$=2.0$ against `compton_shift(0,1)`$=0$.
