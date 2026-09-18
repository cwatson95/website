# QM-14 — Identical Particles

Indistinguishability and its consequences, in the **QUANTUM MECHANICS** trunk
(see `modules/topic_network.txt`). Identical quantum particles cannot be labelled,
and that one fact — promoted to the **symmetrization postulate** — produces the
boson/fermion split, the Pauli exclusion principle, the Slater determinant, the
"exchange force," and ultimately the periodic table.

- **Prerequisites:** `~QM-05` (states as vectors, operators — the exchange
  operator $P_{12}$ is one of these), `~QM-06` (measurement / expectation
  values). Helpful: `~QM-09` (the harmonic-oscillator orbitals used for the
  exchange force) and `~QM-11` (spin, for the singlet/triplet capstone).
- **Feeds into:** `~SM-04` (Bose–Einstein & Fermi–Dirac statistics — *not yet
  built; the bridge connects when it lands*) and `~QM-12` (multi-electron atoms /
  the periodic table).

## Scope
Indistinguishability and the **symmetrization postulate**; **bosons** (symmetric
under exchange, $P_{12}\Psi=+\Psi$) versus **fermions** (antisymmetric,
$P_{12}\Psi=-\Psi$); the **Pauli exclusion principle** as a corollary of
antisymmetry; the **Slater determinant** for $N$ fermions; **exchange forces**
(why fermions effectively repel and bosons bunch, via the $\mp2|\langle
x\rangle_{ab}|^2$ term); and a word on **spin, the helium atom and the periodic
table**. *(Griffiths 3e, Ch. 5.)*

**House rule for this module:** nothing about symmetry is asserted — it is
*verified numerically*. The boson state is checked to be a $+1$ eigenstate of the
exchange operator and the fermion state a $-1$ eigenstate; Pauli is checked as a
literal zero vector; the Slater determinant is checked antisymmetric under *any*
pair swap, vanishing on a repeated orbital, and normalized to $\sqrt{N!}$; and
the exchange force is checked against **two** independent closed forms (Griffiths
Problems 5.6 and 5.7).

## Operations — `code/identical.py`

| call | meaning | formula |
|------|---------|---------|
| `tensor(a, b, ...)` | product state | $\|a\rangle\otimes\|b\rangle\otimes\cdots$ |
| `swap_operator(d)` | exchange operator $P_{12}$ on $\mathbb C^d\otimes\mathbb C^d$ | $P_{12}\|i\rangle\|j\rangle=\|j\rangle\|i\rangle$, $P_{12}^2=\mathbb 1$ |
| `apply_pair_swap(state,d,N,p,q)` | swap particles $p,q$ in an $N$-particle state | exchange two tensor slots |
| `symmetrize(a, b)` | **boson** pair | $(\|a\rangle\|b\rangle+\|b\rangle\|a\rangle)/\mathcal N$ |
| `antisymmetrize(a, b)` | **fermion** pair | $(\|a\rangle\|b\rangle-\|b\rangle\|a\rangle)/\mathcal N$; $=0$ if $a=b$ (Pauli) |
| `slater_determinant(orbitals)` | $N$-fermion antisym. state | $\tfrac1{\sqrt{N!}}\sum_\sigma\mathrm{sgn}(\sigma)\,\bigotimes_k\|\phi_{\sigma(k)}\rangle$ |
| `well_state(n, x, L)` / `ho_state(n, x)` | 1-D orbitals | infinite well / harmonic oscillator |
| `position_moments(a, b, x)` | matrix elements | $\langle x\rangle_a,\langle x^2\rangle_a,\langle x\rangle_{ab}=\int x\,\psi_a^*\psi_b$ |
| `exchange_dx2(a, b, x)` | exchange force | $\langle(\Delta x)^2\rangle_\pm=\langle(\Delta x)^2\rangle_{\rm dist}\mp2\|\langle x\rangle_{ab}\|^2$ |
| `singlet()` / `triplet()` | two-spin states | antisym. singlet / sym. triplet |
| `spin_up` / `spin_down` / `levi_civita_sign` / `norm` | helpers | — |

A single-particle state is a vector in $\mathbb C^d$; an $N$-particle state lives
in $(\mathbb C^d)^{\otimes N}=\mathbb C^{d^N}$ with particle $k$ in tensor slot
$k$. **Natural units** for the oscillator ($\hbar=m=\omega=1$, so $\langle
x^2\rangle_n=n+\tfrac12$); the well uses width $L$ (default $1$).

## Use
```python
import numpy as np
from identical import (symmetrize, antisymmetrize, swap_operator,
                       slater_determinant, well_state, exchange_dx2, norm)

a, b = np.array([1.,0.,0.]), np.array([0.,1.,0.])
P = swap_operator(3)
np.allclose(P @ symmetrize(a, b),  symmetrize(a, b))    # True: boson  P=+1
np.allclose(P @ antisymmetrize(a, b), -antisymmetrize(a, b))  # True: fermion P=-1
norm(antisymmetrize(a, a))                              # 0.0  (Pauli exclusion)

# N=3 fermions: a Slater determinant, antisymmetric and normalized
e = np.eye(3); Psi = slater_determinant([e[0], e[1], e[2]])

# exchange force: fermions sit farther apart than bosons (infinite well n=1,2)
x = np.linspace(0, 1, 4001)
r = exchange_dx2(well_state(1, x), well_state(2, x), x)
r["boson"] < r["distinguishable"] < r["fermion"]       # True
```

## Cross-links
- `~QM-05` (formalism) — the exchange operator $P_{12}$ is a Hermitian/unitary
  operator; its $\pm1$ eigenspaces are the symmetric/antisymmetric subspaces.
- `~QM-06` (measurement) — the $\pm1$ exchange parity is a conserved observable.
- `~QM-09` (oscillator), `~QM-11` (spin) — supply the orbitals and the
  singlet/triplet states used here (built locally to avoid a race on
  concurrently-written siblings — no sibling code is imported).
- `~SM-04` (quantum statistics) — Bose–Einstein vs Fermi–Dirac gases follow from
  the boson/fermion occupation rule established here. **Not yet built**; the
  bridge connects when it lands.
- `~QM-12` (central potentials / multi-electron atoms) — the Slater determinant +
  Pauli give the Aufbau principle and the periodic table.

## Run
```bash
cd code
python3 identical.py          # demo: P_12 eigenvalues, Pauli, Slater, exchange force
python3 test_identical.py     # tests  ->  "All 21 tests passed."
```

## Files
- `notes.md` — derivations: indistinguishability, symmetrization, Pauli, the
  Slater determinant, the exchange-force calculation, spin & the periodic table
- `code/identical.py` — the library (numpy; symmetrizers, Slater determinant,
  exchange force, spin helpers)
- `code/test_identical.py` — 21 checks against closed forms (symmetry eigenvalues,
  $\sqrt{N!}$ normalization, Griffiths Problems 5.6 & 5.7)
- `problems/problems.md` — worked problems (Griffiths 3e), each with a code *Check:*
- `refs.md` — verified textbook locations
