# QO-02 — Atom–Field Interaction — Rabi Oscillations & Jaynes–Cummings (notes)

One two-level atom, one mode of light. Drive the atom with a **classical** field
and its excited-state population *flops* coherently — **Rabi oscillations**. Drive
it with the **quantized** field and the same coupling produces the
**Jaynes–Cummings model**: dressed states, a vacuum Rabi splitting set by a single
photon, and — over a coherent field — the **collapse and revival** of the
inversion, a phenomenon with no classical-field counterpart. The atom is the
two-level system / qubit of `~QM-11`; the dipole drive is the time-dependent
perturbation of `~QM-16`; the photon states are those of `~QO-01`.

Citation key (full details + verified sections in `refs.md`): **SZ** = Scully &
Zubairy, *Quantum Optics* — semiclassical Rabi in Ch. 5 (§5.2), the
Jaynes–Cummings model in Ch. 6 (§6.1–6.2). Sections checked against the book's own
table of contents. The code uses $\hbar=1$.

## 1. The two-level atom
Keep only two atomic levels, ground $|g\rangle$ and excited $|e\rangle$ split by
$\hbar\omega_a$. The dynamics live in the **same algebra as spin-$\tfrac12$**
(`~QM-11`), with $|e\rangle\leftrightarrow\,\uparrow$:
$$\sigma_z=|e\rangle\langle e|-|g\rangle\langle g|,\qquad
\sigma^+=|e\rangle\langle g|,\qquad \sigma^-=|g\rangle\langle e|,\qquad
H_A=\tfrac12\hbar\omega_a\,\sigma_z.$$
$\sigma^\pm=\tfrac12(\sigma_x\pm i\sigma_y)$ raise/lower the atom, and
$\sigma^+\sigma^-=|e\rangle\langle e|$ is the excited-state projector. Code:
`sigma_z`, `sigma_plus`, `sigma_minus`.

## 2. The dipole drive and the rotating-wave approximation
A classical field $E(t)=E_0\cos\omega_L t$ couples through the dipole
$-\mathbf d\!\cdot\!\mathbf E$ (`~QM-16`); with $\mathbf d=d_{eg}(\sigma^++\sigma^-)$
and **Rabi coupling** $\Omega=d_{eg}E_0/\hbar$,
$$H_\text{int}=\hbar\,\Omega\cos(\omega_L t)\,(\sigma^++\sigma^-).$$
In the interaction picture $\sigma^\pm$ rotate as $e^{\pm i\omega_a t}$, so each
$\cos\omega_L t$ splits into a **co-rotating** part $\propto e^{\pm i(\omega_a-\omega_L)t}$
and a **counter-rotating** part $\propto e^{\pm i(\omega_a+\omega_L)t}$. The
**rotating-wave approximation (RWA)** drops the fast counter-rotating terms
(valid for $\Omega,|\delta|\ll\omega_a$, near resonance); what they leave behind is
the small Bloch–Siegert shift (SZ §5.2.3, *Beyond the RWA*). In the frame rotating
at $\omega_L$ the survivor is the time-independent
$$H_\text{RWA}=\tfrac12\hbar\big(\delta\,\sigma_z+\Omega\,\sigma_x\big),\qquad
\delta=\omega_a-\omega_L,\quad \sigma_x=\sigma^++\sigma^-,$$
the driven two-level Hamiltonian (cf. the Larmor/Rabi $H$ of `~QM-11`). Code:
`two_level_hamiltonian`.

## 3. Semiclassical Rabi oscillations
$H_\text{RWA}$ has eigenvalues $\pm\tfrac12\hbar\Omega_R$. Starting in $|g\rangle$,
the probability of finding the atom **excited** is the **Rabi formula**
$$\boxed{\;P_e(t)=\frac{\Omega^2}{\Omega_R^2}\,\sin^2\!\Big(\frac{\Omega_R t}{2}\Big),
\qquad \Omega_R=\sqrt{\Omega^2+\delta^2}\;}$$
with the **generalized Rabi frequency** $\Omega_R$. **On resonance** ($\delta=0$)
this is $P_e=\sin^2(\Omega t/2)$: a complete inversion ($P_e=1$) at $\Omega t=\pi$
(a "$\pi$-pulse"), and a full **return** to $P_e=0$ at $\Omega t=2\pi$. **Off
resonance** the flop is faster (rate $\Omega_R$) but never completes — it saturates
at the reduced amplitude $P_e^{\max}=\Omega^2/(\Omega^2+\delta^2)<1$.
Code: `rabi_excited_population`, `generalized_rabi`; the closed form is checked
against genuine evolution of $|g\rangle$ under `two_level_hamiltonian`. (The
weak-field, short-time limit $P_e\simeq\tfrac14\Omega^2 t^2$ is the
time-dependent-perturbation result of `~QM-16`, before the population saturates.)

## 4. Quantizing the field — the Jaynes–Cummings model
Replace the classical field by one quantized mode, $E\to$ operators with photon
ladder $a,a^\dagger$ (`~QO-01`). The dipole coupling, in the RWA, becomes the
**Jaynes–Cummings Hamiltonian** (SZ §6.1–6.2)
$$\boxed{\;H=\hbar\omega_c\,a^\dagger a+\tfrac12\hbar\omega_a\,\sigma_z
+\hbar g\big(a\,\sigma^++a^\dagger\sigma^-\big)\;}$$
where $a\sigma^+$ absorbs a photon **and** excites the atom while $a^\dagger\sigma^-$
emits **and** de-excites. Hence the **excitation number**
$\hat N=a^\dagger a+|e\rangle\langle e|$ is conserved, $[H,\hat N]=0$, and $H$ is
**block-diagonal** in the two-dimensional manifolds $\{|e,n\rangle,|g,n+1\rangle\}$
(both have $n+1$ excitations). Code: `jcm_hamiltonian`.

## 5. Dressed states and the vacuum Rabi splitting
In the basis $(|e,n\rangle,\,|g,n+1\rangle)$ each block is
$$H_n=\hbar\begin{pmatrix}\omega_c n+\tfrac12\omega_a & g\sqrt{n+1}\\
g\sqrt{n+1} & \omega_c(n+1)-\tfrac12\omega_a\end{pmatrix},$$
the off-diagonal $g\sqrt{n+1}$ coming from $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$.
Diagonalizing gives the **dressed states** with energies
$$\boxed{\;E_{n,\pm}=\hbar\omega_c\!\Big(n+\tfrac12\Big)
\pm\tfrac12\hbar\sqrt{\delta^2+4g^2(n+1)}\;},\qquad \delta=\omega_a-\omega_c,$$
the eigenvalues of `jcm_hamiltonian`'s $n$-th block (`dressed_energies`, verified
against `eigh`). Measuring the atomic energy from its ground state instead
($H_A=\hbar\omega_a\sigma^+\sigma^-$, a global $+\tfrac12\hbar\omega_a$) lets one
write the *same* doublet with $\delta'=\omega_c-\omega_a$ as
$$E_{n,\pm}=\hbar\omega_c(n+1)-\tfrac12\hbar\delta'\pm
\tfrac12\hbar\sqrt{\delta'^2+4g^2(n+1)} ,$$
identical up to the unobservable constant. The **splitting** is convention-free,
$E_{n,+}-E_{n,-}=\hbar\sqrt{\delta^2+4g^2(n+1)}$, which on resonance is
$2\hbar g\sqrt{n+1}$. For the lowest rung $n=0$ this is the **vacuum Rabi
splitting** $\Delta E_\text{vac}=2\hbar g$ — a *single* quantum, indeed the vacuum
field, lifts the degeneracy of $|e,0\rangle$ and $|g,1\rangle$, the cavity-QED
signature of strong coupling. Code: `dressed_energies`, `vacuum_rabi_splitting`.

## 6. Collapse and revival of the inversion
Put the atom in $|e\rangle$ over a **coherent** field $|\alpha\rangle$ (mean photon
number $\bar n=|\alpha|^2$, Poissonian $P_n=e^{-\bar n}\bar n^{\,n}/n!$). On
resonance each Fock component $|e,n\rangle$ flops to $|g,n+1\rangle$ at its own
frequency $2g\sqrt{n+1}$, so the **inversion** is a Poisson-weighted sum
$$\boxed{\;\langle\sigma_z\rangle(t)=\sum_{n=0}^{\infty}P_n\cos\!\big(2g\sqrt{n+1}\,t\big)\;}$$
These tones **dephase** — the inversion **collapses** to zero — then **rephase**,
producing partial **revivals**:
$$t_\text{collapse}\sim\frac{\sqrt2}{g}\ \ (\text{independent of }\bar n),\qquad
t_\text{revival}\sim\frac{2\pi\sqrt{\bar n}}{g}\ \ (\text{recurring at }k\,t_\text{revival}).$$
The revival is the fingerprint of field **quantization**: a classical field (a
single Rabi frequency) would flop forever without collapsing. Code: `jcm_inversion`
(exact eigenbasis evolution), `resonant_inversion_series` (the sum above, an
independent check that matches to $\sim10^{-14}$), `collapse_time`, `revival_time`.

## Where this goes
- `~QO-01` — the quantized modes and coherent states $|\alpha\rangle$ that this
  module drives the atom with.
- `~QO-03` — spontaneous & stimulated emission and laser physics: the JCM with the
  field mode now *lossy*, and the gain medium of the KrF/excimer laser.
- `~QO-04` — open quantum systems / master equations: add atomic decay $\Gamma$ and
  cavity loss $\kappa$ to the Rabi flop, giving damped Rabi and the
  strong-coupling condition $g\gg\Gamma,\kappa$ behind the vacuum Rabi splitting.
- `~QM-11` — the two-level/spin algebra ($\sigma_z,\sigma^\pm$) reused here.
- `~QM-16` — time-dependent perturbation theory: the weak-drive limit of the Rabi
  formula, on the way to Fermi's golden rule.
