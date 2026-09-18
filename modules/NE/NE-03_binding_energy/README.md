# NE-03 — Binding energy and separation energies

Third module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§4.1–4.3** (printed pp. 80–88) of Shultis &
Faw, 3rd ed.: the mass defect, binding energy from atomic masses, the $B/A$
curve, and nucleon separation energies.

Where `~NE-02` built a *model* of nuclear binding, this module **measures** it,
using the 2931 atomic masses of `../data_tables/B1_atomic_masses.csv`.

- **Prerequisites:** `~NE-02` (the liquid drop model these numbers test),
  `~NE-01` (the eV-vs-MeV scale separation that lets electron binding be
  dropped), `~RE-06` ($E=mc^{2}$ and rest-mass bookkeeping).
- **Cross-links:** `~NE-04` (Q-values are the same mass differences applied to
  general reactions), `~NE-05` ($Q_\alpha=-S_\alpha$; beta energetics from
  atomic masses), `~NE-09` (the $B/A$ step from uranium to the fission peak *is*
  the 200 MeV), `~NE-10` (the same curve climbed from below; the iron/nickel
  peak ends stellar fusion), `~NE-13` ($S_n$ is the energy released on neutron
  capture, hence the compound nucleus excitation).

## Scope
A nucleus weighs less than its parts, and the deficit is the binding energy.
Appendix B holds **atomic** masses, so the working form adds $Z$ electrons to
both sides — $Z$ protons become $Z$ hydrogen atoms, the electron binding
energies cancel to one part in $10^{6}$, and
$$BE=\big[ZM({}^{1}\mathrm{H})+(A-Z)m_n-M(A,Z)\big]c^{2},\qquad c^{2}=931.494\ \text{MeV/u}.$$
Uranium's mass defect is 1.93 u — 0.8% of the atom, against $1.4\times10^{-8}$ u
for atomic binding. $BE/A$ peaks at **⁶²Ni, 8.7945 MeV/nucleon** (not ⁵⁶Fe, which
is 0.004 MeV lower), so both fusion and fission release energy. The marginal
quantity is more informative than the average: the **separation energy**
$$S_n(A,Z)=BE(A,Z)-BE(A-1,Z)$$
staggers by 3–4 MeV between even and odd $N$ (pairing, measured with no model in
between) and falls off a cliff just past a magic number (shell closure).
$S_\alpha$ goes negative above $A\approx150$, which is where alpha decay becomes
energetically allowed.

## Operations — `code/binding_energy.py`

| call | meaning | reference |
|------|---------|-----------|
| `load_atomic_masses()`, `atomic_mass(A, Z)`, `has_nuclide(A, Z)` | `{(Z,A): M}` from Appendix B | App. B |
| `atomic_to_nuclear_mass(A, Z)` | $m = M - Zm_e$ (electron binding dropped) | Eq. (4.8) |
| `mass_defect_u(A, Z)` | $ZM(^1\mathrm{H})+(A-Z)m_n-M$ | Eq. (4.10) |
| `mass_excess_mev(A, Z)` | $(M-A)c^{2}$ | §4.1.1 |
| `binding_energy(A, Z)` | $BE$ in MeV from measured masses | **Eq. (4.12)** |
| `binding_energy_per_nucleon(A, Z)` | $BE/A$ | §4.1.3 |
| `binding_energy_curve(z_tolerance)` | $(A,Z,BE/A)$ for every nuclide | §4.1.3 |
| `most_bound_nuclide()` | the top of the curve — ⁶²Ni | §4.1.3 |
| `neutron_separation_energy(A, Z)` | $S_n=BE(A,Z)-BE(A{-}1,Z)$ | Eqs. (4.13)–(4.14) |
| `proton_separation_energy(A, Z)` | $S_p=BE(A,Z)-BE(A{-}1,Z{-}1)$ | Eq. (4.15) |
| `two_neutron_separation_energy(A, Z)` | $S_{2n}$ — pairing cancelled, shells visible | §4.3 |
| `alpha_separation_energy(A, Z)` | $S_\alpha$; $Q_\alpha=-S_\alpha$ | §4.3 |
| `pairing_stagger(A, Z)` | $S_n(A,Z)-S_n(A{+}1,Z)$, the odd–even alternation | §4.3 |
| `electron_binding_fraction(A, Z, ev)` | how safe dropping the electron term is | §4.1.1 |

## Use
```python
from binding_energy import (binding_energy, binding_energy_per_nucleon,
                            neutron_separation_energy, alpha_separation_energy,
                            most_bound_nuclide)

binding_energy(56, 26)                  # 492.254 MeV
binding_energy_per_nucleon(235, 92)     # 7.5909 MeV/nucleon
most_bound_nuclide()                    # (62, 28, 8.7945) -- 62Ni, not 56Fe
neutron_separation_energy(16, 8)        # 15.664 MeV  (S&F Example 4.3)
neutron_separation_energy(17, 8)        #  4.143 MeV  -- one neutron later
alpha_separation_energy(238, 92)        # -4.270 MeV  => Q_alpha = +4.270 MeV
```

## Run
```bash
cd code
python3 binding_energy.py        # demo: defects, the curve, S_n systematics, S_alpha
python3 test_binding_energy.py   # tests  ->  "All 18 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv`.

## Files
- `notes.md` — atomic vs nuclear masses → binding energy from Eq. (4.12) → the
  $B/A$ curve and why its peak is ⁶²Ni → separation energies → what they expose
  (pairing, shell closures, alpha instability), with a "Where this goes" map.
- `code/binding_energy.py`, `code/test_binding_energy.py` (stdlib only). Tests
  check the book's Example 4.3, standard binding energies, both formulations of
  $S_n$ agreeing, the odd–even stagger, the shell drop at $N=82$ and $N=126$, and
  the sign change of $S_\alpha$.
- `problems/problems.md` — 8 worked problems (S&F Ch. 4 problems 2, 3/6, 4, 7, 8,
  10 plus two added) with numeric `*Check:*` lines.
- `figures/` — the measured $B/A$ curve, the $S_n$ sawtooth across four isotope
  chains, $S_{2n}$ showing the shell drops, and $S_\alpha$ changing sign.
- `refs.md` — page-verified citations, plus the neutron-mass inconsistency
  between Table A.1 and Appendix B.
