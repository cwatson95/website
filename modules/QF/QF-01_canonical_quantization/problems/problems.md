# QF-01 — Problems

Work each by hand, then check with `code/field_quantization.py`. Citations in
`../refs.md`; **PS** = Peskin & Schroeder Ch. 2 (scalar) and Ch. 3 (Dirac). Units
$\hbar=c=1$. Throughout, "mode" means one momentum $\mathbf p$ — a single harmonic
oscillator (`~QM-09`), the heart of **bridge B6**.

### P1.  Klein–Gordon dispersion and its limits  *(PS §2.3)*
Each Fourier mode of the free scalar field obeys $\ddot\phi_{\mathbf p}=
-\omega_{\mathbf p}^2\phi_{\mathbf p}$ with $\omega_{\mathbf p}=\sqrt{\mathbf p^2+m^2}$.
Show this is the relativistic $E^2=p^2+m^2$ read as a frequency; that a **massless**
field gives $\omega_{\mathbf p}=|\mathbf p|$ (the light cone); that at $\mathbf p=0$
the frequency is the rest energy $\omega=m$; and that $\omega_{\mathbf p}\to|\mathbf p|$
in the ultrarelativistic limit $|\mathbf p|\gg m$. *Check:* `kg_dispersion([0,1,5], 0.0)`
$=[0,1,5]$; `kg_dispersion(0.0, 2.0)` $=2.0$; `kg_dispersion(1e6, 1.0)` $\approx10^6$.

**Solution.** A single Fourier mode obeys $\ddot\phi_{\mathbf p}=-\omega_{\mathbf p}^2\phi_{\mathbf p}$,
the equation of a harmonic oscillator whose frequency is the energy of one quantum
($E=\hbar\omega$, $\hbar=1$). Squaring the dispersion turns it into the relativistic
energy–momentum relation read as a frequency,
$$\omega_{\mathbf p}^2=\mathbf p^2+m^2\quad\Longleftrightarrow\quad E^2=\mathbf p^2+m^2.$$
Massless $m=0$ gives $\omega_{\mathbf p}=|\mathbf p|$ — the light cone, energy equal to
momentum (`kg_dispersion([0,1,5],0.0)`$=[0,1,5]$). At $\mathbf p=0$, $\omega=\sqrt{0+m^2}=m$,
the rest energy $mc^2$ (`kg_dispersion(0.0,2.0)`$=2.0$). For $|\mathbf p|\gg m$,
$\omega=|\mathbf p|\sqrt{1+m^2/\mathbf p^2}\approx|\mathbf p|(1+m^2/2\mathbf p^2)\to|\mathbf p|$,
so a fast quantum forgets its mass: `kg_dispersion(1e6,1.0)`$\approx10^6$.

### P2.  One mode is an oscillator: the ladder algebra  *(PS §2.3; `~QM-09`)*
From the equal-time commutator $[\phi,\pi]=i\delta^3$, derive the mode relation
$[a_{\mathbf p},a_{\mathbf q}^\dagger]=(2\pi)^3\delta^3(\mathbf p-\mathbf q)$ — one
copy of the oscillator's $[a,a^\dagger]=1$ per mode. Then prove **no finite matrices**
satisfy $[a,a^\dagger]=1$ (hint: take the trace), and say what the truncated $D\times D$
operators give instead. *Check:* `np.diag(commutator(annihilation(6), creation(6))).real`
$=[1,1,1,1,1,-5]$ (identity on the interior, $-(D{-}1)$ in the corner) and
`np.trace(...)` $=0$.

**Solution.** Insert the mode expansion $\phi=\int\!\tfrac{d^3p}{(2\pi)^3}\tfrac{1}{\sqrt{2\omega_{\mathbf p}}}(a_{\mathbf p}e^{i\mathbf p\cdot\mathbf x}+a_{\mathbf p}^\dagger e^{-i\mathbf p\cdot\mathbf x})$
and its conjugate $\pi=\dot\phi$ into $[\phi(\mathbf x),\pi(\mathbf y)]=i\delta^3(\mathbf x-\mathbf y)$;
the delta function is reproduced exactly when the modes obey
$$[a_{\mathbf p},a_{\mathbf q}^\dagger]=(2\pi)^3\delta^3(\mathbf p-\mathbf q),\qquad
[a_{\mathbf p},a_{\mathbf q}]=[a_{\mathbf p}^\dagger,a_{\mathbf q}^\dagger]=0,$$
one independent oscillator $[a,a^\dagger]=1$ per momentum. No finite matrices can satisfy
$[a,a^\dagger]=1$: the trace is cyclic, so $\operatorname{tr}[A,B]=\operatorname{tr}(AB)-\operatorname{tr}(BA)=0$,
yet $\operatorname{tr}\mathbb 1_D=D\neq0$ — a contradiction needing the infinite ladder.
Truncating to $D$ levels drops the rung $a^\dagger|D{-}1\rangle=\sqrt D\,|D\rangle$, dumping the
whole defect into one corner: $[a,a^\dagger]=\operatorname{diag}(1,\dots,1,-(D{-}1))$. For $D=6$
that is `np.diag(commutator(annihilation(6),creation(6))).real`$=[1,1,1,1,1,-5]$ with `np.trace(...)` $=0$.

### P3.  The spectrum $(n+\tfrac12)\hbar\omega$ and the zero-point energy  *(PS §2.3)*
From $H_{\mathbf p}=\omega_{\mathbf p}(a_{\mathbf p}^\dagger a_{\mathbf p}+\tfrac12)$
and a lowest rung $a_{\mathbf p}|0\rangle=0$, deduce the per-mode spectrum
$E_{n_{\mathbf p}}=(n_{\mathbf p}+\tfrac12)\hbar\omega_{\mathbf p}$ with ground (zero-point)
energy $\tfrac12\hbar\omega_{\mathbf p}$ — without solving a differential equation
(the `~QM-09` argument, now per mode). *Check:* `single_mode_spectrum(6, omega=1.0)`
$=[0.5,1.5,2.5,3.5,4.5,5.5]$; for $|\mathbf p|=3,m=4$ ($\omega=5$) `mode_energy(3.0, 4.0, 0)`
$=2.5=\omega/2$ and `mode_energy(3.0, 4.0, 1) - mode_energy(3.0, 4.0, 0)` $=5=\omega$.

**Solution.** With $N=a_{\mathbf p}^\dagger a_{\mathbf p}$ and $[a,a^\dagger]=1$, the commutators
$[N,a^\dagger]=a^\dagger$ and $[N,a]=-a$ make $a^\dagger,a$ step $N$ up and down by one — the
ladder. Positivity $\langle n|N|n\rangle=\lVert a|n\rangle\rVert^2\ge0$ forbids negative
eigenvalues, so lowering must terminate at a floor $a_{\mathbf p}|0\rangle=0$ with $N|0\rangle=0$;
climbing with $a^\dagger$ then gives $n=0,1,2,\dots$ Hence
$$H_{\mathbf p}=\omega_{\mathbf p}\big(N+\tfrac12\big)\ \Longrightarrow\ E_{n}=\big(n+\tfrac12\big)\omega_{\mathbf p}.$$
The floor is not zero: an empty mode still carries the zero-point energy $\tfrac12\omega_{\mathbf p}$.
For $\omega=1$, `single_mode_spectrum(6, omega=1.0)`$=[0.5,1.5,2.5,3.5,4.5,5.5]$; for $|\mathbf p|=3,m=4$
the dispersion gives $\omega=\sqrt{9+16}=5$, so `mode_energy(3.0,4.0,0)`$=\omega/2=2.5$ and one
quantum costs `mode_energy(3.0,4.0,1) - mode_energy(3.0,4.0,0)`$=\omega=5$ — the `~QM-09`
argument, now per mode.

### P4.  The vacuum energy and the ultraviolet divergence  *(PS §2.3)*
Summing the $\tfrac12\hbar\omega_{\mathbf p}$ of every mode gives the vacuum energy
$E_0=\tfrac12\sum_{\mathbf p}\hbar\omega_{\mathbf p}=\tfrac{V}{2}\int\!\frac{d^3p}{(2\pi)^3}\,
\omega_{\mathbf p}$. Show the integrand goes like $p^3\,dp$ at large $p$, so $E_0$
**diverges in the ultraviolet**; with a cutoff $|\mathbf p|\le\Lambda$ argue the
massless energy density scales like $\Lambda^4$, so doubling $\Lambda$ multiplies
$E_0$ by $\approx16$. *Check:* `vacuum_energy(0.0, 1.0)` $=3.0$; the ratios
`vacuum_energy(0.0, 4.0)/vacuum_energy(0.0, 2.0)` and `vacuum_energy(0.0, 8.0)/vacuum_energy(0.0, 4.0)`
are both $>4$ (and approach $16$).

**Solution.** Each mode contributes its zero-point $\tfrac12\omega_{\mathbf p}$; summing over the
continuum and doing the angular integral,
$$E_0=\tfrac12\sum_{\mathbf p}\omega_{\mathbf p}=\frac{V}{2}\!\int\!\frac{d^3p}{(2\pi)^3}\,\omega_{\mathbf p}
=\frac{V}{4\pi^2}\!\int_0^\infty p^2\,\omega_{\mathbf p}\,dp.$$
At large $p$, $\omega_{\mathbf p}\to|\mathbf p|$, so the integrand behaves as $p^2\cdot p\,dp=p^3\,dp$
and the integral **diverges in the ultraviolet**. With a cutoff $|\mathbf p|\le\Lambda$ the massless
energy density is $E_0/V\sim\int_0^\Lambda p^3\,dp\sim\Lambda^4$, so doubling $\Lambda$ multiplies
$E_0$ by $\approx2^4=16$. The discrete box check shows the onset: `vacuum_energy(0.0, 1.0)`$=3.0$
(the six $|\mathbf p|=1$ axis modes, $\tfrac12\cdot6\cdot1$), while the doubling ratios
$379.28/24.41\approx15.5$ and $6290.9/379.28\approx16.6$ both exceed $4$ and climb toward $16$ as
the lattice better samples the integral — the divergence renormalization must tame (`~QF-04`).

### P5.  A massive field and the zero mode  *(PS §2.3)*
Explain why a heavier field has a *larger* zero-point energy at fixed cutoff
($\omega_{\mathbf p}=\sqrt{\mathbf p^2+m^2}$ rises with $m$). Then take a cutoff so
small that only the $\mathbf p=0$ mode survives, and show $E_0=\tfrac12 m$ for a
massive field but $E_0=0$ for a massless one (the photon has no rest energy).
*Check:* `vacuum_energy(2.0, 0.5)` $=1.0=\tfrac12 m$ while `vacuum_energy(0.0, 0.5)`
$=0.0$; and `vacuum_energy(3.0, 4.0) > vacuum_energy(0.0, 4.0)`.

**Solution.** Mode by mode, $\omega_{\mathbf p}=\sqrt{\mathbf p^2+m^2}$ is an increasing function of
$m$, so at fixed cutoff every term of $E_0=\tfrac12\sum_{\mathbf p}\omega_{\mathbf p}$ grows with the
mass and the total rises — `vacuum_energy(3.0, 4.0)`$>$`vacuum_energy(0.0, 4.0)` ($462.4>379.3$).
Now shrink the cutoff below the first nonzero box momentum (here $|\mathbf p|=1$) so only the zero
mode $\mathbf p=0$ survives. Then
$$E_0=\tfrac12\,\omega_{0}=\tfrac12\sqrt{0+m^2}=\tfrac12 m,$$
giving `vacuum_energy(2.0, 0.5)`$=\tfrac12\cdot2=1.0$ for the massive field, but
$\tfrac12\sqrt{0}=0$ for the massless one, `vacuum_energy(0.0, 0.5)`$=0.0$. The single surviving
quantum is just the rest energy $\tfrac12 m$ of the field at rest; a photon ($m=0$) has none.

### P6.  Spin–statistics: why the Dirac field anticommutes  *(PS §3.5; `~QM-14`)*
Quantizing the spin-$\tfrac12$ field with commutators makes $H$ unbounded below; the
fix is **anticommutators** $\{b_{\mathbf p},b_{\mathbf q}^\dagger\}=(2\pi)^3\delta^3(\mathbf p-\mathbf q)$.
Show that this forces $(b^\dagger)^2=0$ — the **Pauli exclusion principle** — so a
fermion mode holds only $0$ or $1$ quantum, unlike a boson mode (which holds any
number). *Check:* with `b = fermion_annihilation()`, `anticommutator(b, b.conj().T)`
$=\mathbb 1_2$ and `b.conj().T @ b.conj().T` $=0$; the fermion number $b^\dagger b$ has
eigenvalues $\{0,1\}$ whereas `np.diag(number(5)).real` $=[0,1,2,3,4]$.

**Solution.** Quantizing the spin-$\tfrac12$ field with commutators makes $H$ unbounded below; the
cure is the equal-time **anticommutator** $\{b_{\mathbf p},b_{\mathbf q}^\dagger\}=(2\pi)^3\delta^3(\mathbf p-\mathbf q)$,
together with $\{b,b\}=\{b^\dagger,b^\dagger\}=0$. The same-mode relation $\{b^\dagger,b^\dagger\}=2(b^\dagger)^2=0$
gives
$$(b^\dagger)^2=0,$$
so a second quantum cannot be created in an occupied mode — the **Pauli exclusion principle**. The
number operator is then idempotent: using $bb^\dagger=1-b^\dagger b$,
$(b^\dagger b)^2=b^\dagger(bb^\dagger)b=b^\dagger(1-b^\dagger b)b=b^\dagger b$, so its eigenvalues are
only $\{0,1\}$. Numerically `anticommutator(b, b.conj().T)`$=\mathbb 1_2$, `b.conj().T @ b.conj().T`$=0$,
and $b^\dagger b$ has spectrum $\{0,1\}$: a fermion mode holds $0$ or $1$ quantum, whereas the boson
number runs unbounded, `np.diag(number(5)).real`$=[0,1,2,3,4]$.

### P7.  Ladder factors and Fock states  *(PS §2.3)*
From the algebra derive $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$,
$a|n\rangle=\sqrt{n}\,|n-1\rangle$, and $a|0\rangle=0$: one $a_{\mathbf p}^\dagger$
on the vacuum creates one particle of momentum $\mathbf p$, and because the
$a^\dagger$ commute the multi-particle states are symmetric (bosons, `~QM-14`).
*Check:* `creation(6) @ e2` $=\sqrt3\,|3\rangle$ (with `e2` the unit vector $|2\rangle$),
`annihilation(6) @ e0` $=0$, and `np.diag(number(6)).real` $=[0,1,2,3,4,5]$.

**Solution.** Since $a^\dagger|n\rangle$ has $N$-eigenvalue $n+1$, write $a^\dagger|n\rangle=c_n|n+1\rangle$
and fix $|c_n|$ from the norm using $aa^\dagger=N+1$:
$$\lVert a^\dagger|n\rangle\rVert^2=\langle n|aa^\dagger|n\rangle=\langle n|(N+1)|n\rangle=n+1,$$
so $a^\dagger|n\rangle=\sqrt{n+1}\,|n+1\rangle$ with the standard phase; likewise
$\lVert a|n\rangle\rVert^2=\langle n|N|n\rangle=n$ gives $a|n\rangle=\sqrt{n}\,|n-1\rangle$, and the
$\sqrt0$ factor kills the floor, $a|0\rangle=0$. Reading the rungs as particles, $a_{\mathbf p}^\dagger|0\rangle$
is one quantum of momentum $\mathbf p$; because the $a_{\mathbf p}^\dagger$ commute,
$a_{\mathbf p}^\dagger a_{\mathbf q}^\dagger|0\rangle=a_{\mathbf q}^\dagger a_{\mathbf p}^\dagger|0\rangle$ —
multi-particle states are symmetric, i.e. **bosons** (`~QM-14`). Hence `creation(6) @ e2`$=\sqrt3\,|3\rangle$
(the $\sqrt3\approx1.732$ in slot $3$), `annihilation(6) @ e0`$=0$, and the occupation runs
`np.diag(number(6)).real`$=[0,1,2,3,4,5]$.
