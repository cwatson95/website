# QM-12 — Central Potentials & the Hydrogen Atom

Part of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~QM-03` (the time-independent Schrödinger equation),
  `~QM-10` (angular momentum & the spherical harmonics $Y_l^m$ — the angular
  factor of every orbital), `~MA-12` (Laguerre/Legendre special functions),
  `~MA-03` (spherical coordinates). Light contact with `~QM-09` (the same
  series-termination trick quantizes the oscillator).
- **Feeds into:** `~QM-17` (fine structure — relativistic and spin-orbit
  corrections to the levels found here), `~QM-21` (perturbation theory on the
  hydrogen levels), `~QM-13` (multi-electron atoms via the hydrogenic shells).
- **Classical bridge:** `~CM-11` (Kepler / central-force motion — **bridge B4**,
  the $1/r$ potential; the quantum $\langle r\rangle\sim n^2$ and the $-1/n^2$
  energies are the echoes of the classical orbit. CM-11 is not yet built; the
  bridge connects when it lands.)

## Scope
A particle in a **central potential** $V(r)$, then the Coulomb case (hydrogen) in
full — as closed-form formulae *and* a finite-difference solve you can run:

1. **Separation in spherical coordinates.** $\psi(r,\theta,\phi)=R(r)\,Y_l^m(\theta,\phi)$
   splits the TISE into an angular equation (solved once and for all by the
   $Y_l^m$ of `~QM-10`) and a **radial equation** that depends on $V(r)$.
2. **The radial equation & the centrifugal barrier.** With $u=rR$, the radial
   problem becomes a 1-D Schrödinger equation in the **effective potential**
   $V_{\text{eff}}=V(r)+\tfrac{l(l+1)\hbar^2}{2mr^2}$ — the second term is the
   repulsive centrifugal barrier.
3. **The Coulomb problem.** $V=-1/r$ (atomic units) gives the **Bohr spectrum**
   $E_n=-\tfrac1{2n^2}$ Ha $=-13.6/n^2$ eV — depending on $n$ **only**.
4. **Quantum numbers & degeneracy.** $(n,l,m)$ with $l=0..n-1$ and $m=-l..l$;
   the level $E_n$ is $n^2$-fold degenerate.
5. **Radial wavefunctions.** $R_{nl}$ built from the associated Laguerre
   $L_{n-l-1}^{2l+1}$ — normalized, with exactly $n-l-1$ radial nodes; the mean
   radius $\langle r\rangle=\tfrac12[3n^2-l(l+1)]$ ($=\tfrac32 a_0$ for the ground
   state).

**House rule for this module:** the spectrum is obtained **two independent ways
that must agree** — a finite-difference eigensolve of the radial equation, and
the closed-form $E_n$/$R_{nl}$ — and every closed form ($\langle r\rangle$,
normalization, node count, the $n^2$ degeneracy) is checked numerically. Atomic
units $\hbar=m=e=4\pi\varepsilon_0=1$ throughout (so $a_0=1$, energies in
hartrees; $\times$`HARTREE_EV` for eV).

## Operations — `code/hydrogen.py`

| call | meaning | formula |
|------|---------|---------|
| `coulomb_energy(n)` | Bohr level (Ha) | $E_n=-1/(2n^2)$ |
| `coulomb_energy_eV(n)` | Bohr level (eV) | $-13.606/n^2$ |
| `allowed_l(n)` / `m_values(l)` | quantum numbers | $l=0..n{-}1$; $m=-l..l$ |
| `degeneracy(n)` / `count_states(n)` | degeneracy (closed / summed) | $n^2=\sum_{l}(2l{+}1)$ |
| `effective_potential(r, l)` | Coulomb + centrifugal | $-1/r+l(l{+}1)/2r^2$ |
| `radial_solve(l, …)` | finite-difference radial eigensolve | $-\tfrac12u''+V_{\text{eff}}u=Eu$ |
| `generalized_laguerre(k, α, x)` | associated Laguerre | $L_k^{(\alpha)}$ (scipy; α=0 ↔ `~MA-12`) |
| `radial_wavefunction(n, l, r)` | $R_{nl}(r)$ | Griffiths Eq. 4.89 |
| `radial_probability(n, l, r)` | radial density | $r^2|R_{nl}|^2$ |
| `radial_norm(n, l)` | normalization check | $\int|R_{nl}|^2r^2dr=1$ |
| `count_radial_nodes(n, l)` | node count | $=n-l-1$ |
| `expectation_r(n, l)` / `expectation_r_closed(n, l)` | mean radius | $\tfrac12[3n^2-l(l{+}1)]$ |

Constants `HARTREE_EV`, `BOHR_RADIUS` (= 1) are exported too.

## Use
```python
from hydrogen import (coulomb_energy_eV, degeneracy, radial_solve,
                      radial_wavefunction, expectation_r, count_radial_nodes)

coulomb_energy_eV(1)                 # -13.606 eV  (hydrogen ionization energy)
degeneracy(3)                        # 9  = 3^2  (the 3s,3p,3d states)
E, r, u = radial_solve(0, 3)         # finite-difference -> E[0] ~ -0.5 Ha
radial_wavefunction(1, 0, 0.0)       # 2.0   (R_10 = 2 e^{-r}; cusp value at r=0)
count_radial_nodes(3, 1)             # 1     ( = n-l-1 )
expectation_r(1, 0)                  # 1.5   ( <r> = 3/2 a0, not a0 )
```

## Run
```bash
cd code
python3 hydrogen.py          # demo: energy ladder, degeneracy, radial table
python3 test_hydrogen.py     # tests  ->  "All 14 tests passed."
```

## Files
- `notes.md` — separation → radial equation → centrifugal barrier → Coulomb
  spectrum → quantum numbers/degeneracy → $R_{nl}$, nodes, $\langle r\rangle$
- `code/hydrogen.py` — the library (spectrum, radial FD solver, closed-form $R_{nl}$)
- `code/test_hydrogen.py` — 14 checks: Bohr spectrum (FD vs analytic), $n^2$
  degeneracy, normalization, $n-l-1$ nodes, $\langle r\rangle$, MA-12 Laguerre link
- `problems/problems.md` — worked problems (Griffiths 3e, page-verified)
- `refs.md` — verified textbook locations
