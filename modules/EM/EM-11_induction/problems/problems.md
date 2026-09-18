# EM-11 — Problems

Work by hand, then check with `code/induction.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages).

### P1.  Faraday EMF in a sinusoidal field  *(Gr §7.2.1, p.312)*
A flat loop of area $A$ lies in a spatially uniform field $\mathbf B(t)=B_0\sin(\omega t)\,\hat{\mathbf z}$
normal to it. Show the flux is $\Phi(t)=B_0A\sin\omega t$ and hence
$$\mathcal{E}=-\frac{d\Phi}{dt}=-B_0A\omega\cos\omega t,$$
so the peak EMF is $B_0A\omega$ and the induced current opposes the field while the
flux is *rising* (Lenz). *Check:* build `B` and `flat_loop_surface`, confirm
`magnetic_flux` gives $B_0A$ at the instant $\sin\omega t=1$, and that
`faraday_emf(flux, t)` matches $-B_0A\omega\cos\omega t$; `lenz_sign(dΦ/dt)` flips
with the sign of $\cos\omega t$.

**Solution.** With $\mathbf B$ uniform and normal to the loop, $d\mathbf a=da\,\hat{\mathbf z}$, so
$$\Phi(t)=\int\mathbf B\cdot d\mathbf a=B_0\sin(\omega t)\!\int_S da=B_0A\sin\omega t.$$
Faraday's law then gives $\mathcal{E}=-\dfrac{d\Phi}{dt}=-B_0A\omega\cos\omega t$, peaking at $|\mathcal{E}|=B_0A\omega$
when $\cos\omega t=\pm1$. While the flux *rises* ($\dot\Phi=B_0A\omega\cos\omega t>0$) Lenz's law forces the
induced current to oppose it, so $\mathcal{E}<0$. Numerically, at $\sin\omega t=1$ the flux equals $B_0A=0.5\times0.01=5\times10^{-3}$
(matching `magnetic_flux`), and at $t=0$ `faraday_emf` returns $-0.5\,$V $=-B_0A\omega$; `lenz_sign` returns $-1$ for $\dot\Phi>0$ and $+1$ for $\dot\Phi<0$, flipping with $\cos\omega t$.

### P2.  Sliding rod on rails  *(Gr §7.1.3, p.305)*
A rod of length $L$ slides at speed $v$ along two rails in a uniform field $B$
perpendicular to the plane of the circuit. From the Lorentz force $q\,\mathbf v\times\mathbf B$
show the motional EMF is $\mathcal{E}=BvL$, and that this equals $-d\Phi/dt$ computed
from the area the rod sweeps (the **flux rule**, p.313). Which way does the induced
current flow? *Check:* `motional_emf(B, v, L)` for $B=0.3$ T, $v=2$ m/s, $L=0.5$ m
returns $0.3$ V.

**Solution.** Each charge in the rod feels $\mathbf f=q\,\mathbf v\times\mathbf B$; with $\mathbf v$, $\mathbf B$ and
the rod mutually perpendicular, $|\mathbf v\times\mathbf B|=vB$ points along the rod. The EMF is the work per
unit charge around the loop,
$$\mathcal{E}=\oint(\mathbf v\times\mathbf B)\cdot d\boldsymbol\ell=vB\,L=BvL.$$
Equivalently, in time $dt$ the rod sweeps area $dA=Lv\,dt$, so $d\Phi=B\,dA=BLv\,dt$ and
$|{-}d\Phi/dt|=BvL$ — the **flux rule** gives the identical answer. By Lenz the induced current circulates
so its own flux opposes the growing $\Phi$ (counter-clockwise if $\mathbf B$ points out of the page and the area is increasing). Numerically $\mathcal{E}=0.3\times2\times0.5=0.3\,$V, as `motional_emf(0.3, 2.0, 0.5)` returns.

### P3.  Self-inductance of a solenoid  *(Gr §7.2.3, p.321)*
A long solenoid has $N$ turns over length $l$ and cross-section $A$. Using
$B=\mu_0(N/l)I$ inside and $\Phi=LI$ for the total flux linkage of all $N$ turns,
derive
$$L=\frac{\mu_0 N^2 A}{l}.$$
Evaluate it for $N=1000$, $A=10^{-4}\,\mathrm{m^2}$, $l=0.2$ m. *Check:*
`solenoid_inductance(1000, 1e-4, 0.2)` $\approx 6.28\times10^{-4}$ H.

**Solution.** Inside the solenoid the field is uniform, $B=\mu_0(N/l)I$, so the flux through *one* turn is
$BA=\mu_0(N/l)IA$. The total flux linkage threads all $N$ turns,
$$\Phi=N\,(BA)=N\cdot\mu_0\frac{N}{l}IA=\frac{\mu_0 N^2 A}{l}\,I.$$
Comparing with $\Phi=LI$ identifies $L=\mu_0 N^2 A/l$. Inserting the numbers,
$$L=\frac{(4\pi\times10^{-7})(1000)^2(10^{-4})}{0.2}=\mu_0\cdot 500=6.28\times10^{-4}\ \text{H},$$
exactly what `solenoid_inductance(1000, 1e-4, 0.2)` returns ($6.2832\times10^{-4}$ H).

### P4.  Energy of the solenoid, two ways  *(Gr §7.2.4, p.328)*
For the solenoid of P3 carrying current $I=3$ A, compute the stored energy *both* as
$$W=\tfrac12 L I^2 \qquad\text{and}\qquad W=\frac{1}{2\mu_0}\int B^2\,d\tau$$
over the interior ($B=\mu_0NI/l$ uniform inside, $\approx 0$ outside), and show the
two agree. *Check:* `energy_in_inductor(L, 3.0)` equals
`magnetic_field_energy_solenoid(1000, 1e-4, 0.2, 3.0)` $\approx 2.83\times10^{-3}$ J
— the same charge-vs-field duality as `~EM-06`.

**Solution.** The inductor picture gives $W=\tfrac12 LI^2=\tfrac12(6.28\times10^{-4})(3)^2=2.83\times10^{-3}\,$J.
The field picture integrates $u=B^2/2\mu_0$ over the interior volume $V=Al$, where $B=\mu_0NI/l$ is uniform:
$$W=\frac{B^2}{2\mu_0}\,Al=\frac{1}{2\mu_0}\Big(\frac{\mu_0 NI}{l}\Big)^2 Al=\tfrac12\,\frac{\mu_0 N^2 A}{l}\,I^2=\tfrac12 LI^2,$$
so the two are algebraically identical — the substitution turns the field integral straight back into $\tfrac12 LI^2$. Numerically both equal $2.8274\times10^{-3}\,$J, confirming `energy_in_inductor(L, 3.0)` $=$ `magnetic_field_energy_solenoid(1000, 1e-4, 0.2, 3.0)`, the magnetic twin of the `~EM-06` charge-vs-field duality.

### P5.  Mutual inductance and reciprocity  *(Gr §7.2.3, p.321)*
Two coaxial solenoids share the cross-section $A$ and length $l$, with $N_1$ and
$N_2$ turns. A current $I_1(t)$ in coil 1 induces $\mathcal{E}_2=-M\,dI_1/dt$ in coil 2.
Show $M=\mu_0 N_1 N_2 A/l$ and argue the **reciprocity** $M_{12}=M_{21}$ — the
mutual inductance is independent of which coil drives. *Check:*
`mutual_inductance_solenoids(N1, N2, A, l)` returns the same value as the call with
$N_1$ and $N_2$ swapped.

**Solution.** Current $I_1$ in coil 1 makes the uniform interior field $B_1=\mu_0(N_1/l)I_1$, which threads
every one of coil 2's $N_2$ turns. The flux linkage of coil 2 is therefore
$$\Phi_2=N_2\,(B_1 A)=\frac{\mu_0 N_1 N_2 A}{l}\,I_1\equiv M\,I_1\;\Longrightarrow\;M=\frac{\mu_0 N_1 N_2 A}{l},$$
and $\mathcal{E}_2=-M\,dI_1/dt$ follows from Faraday's law. The expression is symmetric under $N_1\leftrightarrow N_2$,
so driving coil 2 instead gives the identical $M$: this is **reciprocity** $M_{12}=M_{21}$ (a general theorem, here made explicit). Hence `mutual_inductance_solenoids(N1, N2, A, l)` equals the same call with $N_1,N_2$ swapped (e.g. both give $3.770\times10^{-3}$ H for $N_1{=}2000,N_2{=}3000$).
