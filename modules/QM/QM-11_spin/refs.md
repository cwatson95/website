# QM-11 — References

Page-level citations **verified by reading the page text** in the PDF (extracted,
not eyeballed off a scan). **Printed** = the number printed on the page; **PDF** =
the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths & Schroeter, *Introduction to Quantum Mechanics*, **3rd ed.** (2018) | `QM_Quantum_Mechanics/QuantumMechanics_Griffiths.pdf` | PDF = printed **+ 0** |
| Bethe & Jackiw, *Intermediate Quantum Mechanics*, 3rd ed. | `QM_Quantum_Mechanics/BetheQM.pdf` | PDF = printed **+ 19** |

> **Offset notes.**
> *Griffiths:* the printed folio equals the viewer page throughout the body (the
> whole QM trunk uses this scan; read printed page `P` with `fitz.open(path)[P-1]`).
> Confirmed for this module at printed pages 212, 214, 215, 216, 218, 219, 220, 221
> (each carries the §/Example/Problem cited below).
> *Bethe:* verified empirically — fitz index 32/33 carry printed folios 14/15, so
> `fitz_index = printed + 18` (PDF viewer page = printed + 19); read printed page
> `P` with `fitz.open(path)[P+18]`. Matches the `~QM-10` offset.

## Topic → location (Griffiths 3e — the primary source)

| Topic (code symbol) | Section | Printed p. |
|---|---|---|
| Spin = intrinsic angular momentum, "a carbon copy of orbital", not a function of position; algebra $[S_i,S_j]=i\hbar\varepsilon_{ijk}S_k$ (Eq. 4.134), $S^2\!\to\!\hbar^2 s(s{+}1)$, $S_z\!\to\!\hbar m$, ladder $S_\pm$ (Eq. 4.135–4.137) (`Sx,Sy,Sz`,`S_squared`,`commutator`) | §4.4 *Spin* | 212 |
| Spin-½: two states $\uparrow,\downarrow$; the spinor $\chi=(a,b)$; spin operators as $2\times2$ matrices via $S_z,S_\pm$ on $\chi_\pm$ (Eq. 4.139–4.143) | §4.4.1 *Spin 1/2* | 214 |
| Pauli matrices $\mathbf S=\tfrac{\hbar}{2}\boldsymbol\sigma$ (Eq. 4.145–4.148); $\sigma_i$ Hermitian; eigenspinors of $S_z$ (Eq. 4.149–4.150); measuring $S_x$ (`sigma_*`,`Sx`,`up_z`,`prob_up_z`) | §4.4.1 | 215 |
| Eigenspinors of $S_x$ (Eq. 4.151); $|c_\pm|^2$ probabilities; Example 4.2 (probabilities of $S_x,S_z$); $\langle S_x\rangle$ (`born_probabilities`,`expectation`) | §4.4.1 | 216 |
| **Problem 4.33** — $S_r=\hat{\mathbf n}\cdot\mathbf S$ along an arbitrary direction; eigenvalues $\pm\hbar/2$; eigenspinor $\chi_+^{(r)}=(\cos\tfrac\theta2,\sin\tfrac\theta2 e^{i\phi})$ (`spin_operator_along`,`spin_eigenstate`) | §4.4.1 (problems) | 218 |
| Magnetic moment $\boldsymbol\mu=\gamma\mathbf S$ (Eq. 4.156), energy $-\boldsymbol\mu\!\cdot\!\mathbf B$ (4.157), **Hamiltonian $H=-\gamma\,\mathbf B\!\cdot\!\mathbf S$ (Eq. 4.158)**; gyromagnetic ratio; Example 4.3 Larmor precession, $\mathbf B=B_0\hat{\mathbf z}$ (`hamiltonian_field`,`propagator`) | §4.4.2 *Electron in a Magnetic Field* | 219 |
| Larmor result: $\langle S_x\rangle=\tfrac\hbar2\sin\alpha\cos\omega t$, $\langle S_y\rangle=-\tfrac\hbar2\sin\alpha\sin\omega t$, $\langle S_z\rangle=\tfrac\hbar2\cos\alpha$; **Larmor frequency $\omega=\gamma B_0$** (Eq. 4.163–4.167); Fig. 4.14 (`spin_expectations`,`larmor_frequency`) | §4.4.2 | 220 |
| **Example 4.4** Stern–Gerlach: force $\nabla(\boldsymbol\mu\!\cdot\!\mathbf B)$; beam splits into $2s+1$ streams — quantization of angular momentum; SG as state preparation/measurement (`born_probabilities`) | §4.4.2 | 221 |

## Topic → location (Bethe & Jackiw — verified extra source)

| Topic | Section | Printed p. |
|---|---|---|
| Spin = angular momentum "which cannot be expressed in terms of the classical position and momentum coordinates"; components can be half-integers since $J_z$ is no longer $-i\,\partial/\partial\phi$; $S^2=s(s{+}1)\mathbb 1$, $S_z=m_s\mathbb 1$ (Eq. 1-31); integer/half-integer forced by the commutators (1-27) **and** Hermiticity; spin is experimentally determined | §1 *Quantum Mechanical Results* | 14 |
| Spin space has $2s+1$ points; the $s=\tfrac12$ eigenvectors; total $\mathbf J=\mathbf L+\mathbf S$ with $[\mathbf L,\mathbf S]=0$ (Eq. 1-33) — the bridge to `~QM-13` | §1 | 15 |

> **Honesty note (per the trunk's citation rule).** Spin is *core* Griffiths and is
> treated from first principles in §4.4: §4.4.1 derives the Pauli matrices, §4.4.2
> the field Hamiltonian and Larmor precession, and Problem 4.33 the
> $\hat{\mathbf n}\cdot\mathbf S$ eigenspinor — every boxed formula in `notes.md`
> sits on a page verified above. The two things Griffiths does **not** print are
> (i) the compact master identity $\sigma_i\sigma_j=\delta_{ij}\mathbb 1+i\varepsilon_{ijk}\sigma_k$
> (it writes the squares and products separately) and (ii) the Rabi formula in the
> rotating-frame form used here — Problem 4.36 (p.222) sets up the *rotating-field*
> two-level problem and asks for the flip probability, and the standard Rabi result
> $P=(\Omega^2/\Omega_R^2)\sin^2(\Omega_R t/2)$ is what the code derives and
> verifies against direct time evolution. For both, **the verification is the
> code** (`test_pauli_product_identity`, `test_rabi_*`). Bethe confirms the same
> spin algebra and the integer/half-integer dichotomy independently.

## Problems (verified, Griffiths 3e)
- **Problem 4.31** — for a general spinor $\chi$, compute
  $\langle S_x\rangle,\langle S_y\rangle,\langle S_z\rangle,\langle S_x^2\rangle,\dots$;
  check the uncertainty relations — printed **p.218**.
- **Problem 4.32** — eigenvalues and eigenspinors of $S_y$; measurement
  probabilities for a general state — printed **p.218**.
- **Problem 4.33** — $S_r=\hat{\mathbf n}\cdot\mathbf S$ along an arbitrary
  direction; eigenvalues $\pm\hbar/2$ and the eigenspinor
  $\chi_+^{(r)}=(\cos\tfrac\theta2,\,\sin\tfrac\theta2 e^{i\phi})$ — printed **p.218**.
- **Problem 4.34** — construct the spin-1 matrices $S_x,S_y,S_z$ (the next rung) —
  printed **p.218**.
- **Problem 4.35** — in Example 4.3 (Larmor), the probabilities of measuring
  $S_x,S_y,S_z$ at time $t$ — printed **p.222**.
- **Problem 4.36** — electron in an *oscillating* magnetic field: build $H(t)$,
  solve the time-dependent Schrödinger equation, find the flip probability (the
  Rabi problem) — printed **p.222**.
- **Problem 4.62** — spin matrices for arbitrary spin $s$, generalizing spin-½ —
  printed **p.240**.

## Further reading (not page-verified here)
- **Sakurai & Napolitano, *Modern QM*** — `QM_Quantum_Mechanics/SakuraiQM.pdf` is an
  **image-only scan (no text layer)**; cite unpinned: Ch. 1 (Stern–Gerlach as the
  opening example) and Ch. 3 (spin, rotations, the $SU(2)$ double cover, and the
  spin-½ rotation $e^{-i\boldsymbol\sigma\cdot\hat{\mathbf n}\,\phi/2}$).
- **Cohen-Tannoudji, *Quantum Mechanics* Vol. I** — `QM_Quantum_Mechanics/QM_Cohen-Tannoudji.pdf`
  is likewise **image-only**; cite unpinned: Ch. IV (the spin-½ two-level system
  and its complements: density matrix, magnetic resonance / Rabi).
- `~QM-10` (this repo) — the angular-momentum algebra and the $l=\tfrac12$ matrix
  representation that **is** spin (imported in the cross-check test).
- `~MA-18` (this repo) — su(2)/SU(2): the Pauli matrices as generators and the
  $SU(2)\to SO(3)$ double cover (imported in the cross-check test).
