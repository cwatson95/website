# QO-04 — References

Citations are anchored at **section / chapter level** (number + exact title), the
granularity the assignment asks for. The book has a real text layer, so the anchor
pages were **verified by extracting the page text**; **printed** = the folio on the
page, **PDF** = the page in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Scully & Zubairy, *Quantum Optics* (Cambridge Univ. Press, 1997) | `QO_Quantum_Optics/QuantumOptics.ZubairyMuhammadSuhail.pdf` | PDF = printed **+ 20** |

> **Offset note (verified).** The printed↔PDF offset is **+20**, confirmed by
> reading the page body at four anchors: PDF p.180 opens "*160 · Atom–field
> interaction — semiclassical theory … §5.3*"; PDF p.226 carries "*206 … 6.3
> Weisskopf–Wigner theory of spontaneous emission*"; PDF p.268 is "*CHAPTER 8
> Quantum theory of damping*" (printed 248); PDF p.311 is "*CHAPTER 10 Resonance
> fluorescence*" (printed 291); and §8.1 "*General reservoir theory*" (printed 249)
> sits alone on PDF p.269. **Granularity:** the chapter/section *heading* pages
> below were each read directly; the finer sub-section pages are taken from the
> book's printed **Contents** listing and inherit the same verified +20 offset
> (they were not each re-read). No page number here is invented.

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Density matrix of a two-level atom; populations & coherences; equation of motion (`density_matrix`, `populations`, `coherence`, `excited_population`) | **§5.3** *Density matrix for a two-level atom* (§5.3.1 *Equation of motion for the density matrix*, §5.3.2 *Two-level atom*) | 160–162 | 180–182 |
| Elastic, population-conserving collisions = **pure dephasing** (`dephasing_op`, the $T_\phi$ / $T_2$ term) | **§5.3.3** *Inclusion of elastic collisions between atoms* | 163 | 183 |
| Bloch-vector picture of $\rho$ (the optical Bloch geometry behind Ch. 10) | **§5.B** *Vector model of the density matrix* | 183 | 203 |
| **Spontaneous emission rate $\gamma$** (Einstein $A$); the $T_1$ process (`spontaneous_emission_op`) | **§6.3** *Weisskopf–Wigner theory of spontaneous emission between two atomic levels* | 206 | 226 |
| **Master equation / quantum theory of damping**; reservoir theory; CPTP generator (`lindblad_rhs`, `evolve_lindblad`, `is_density_matrix`) | **Ch. 8** *Quantum theory of damping — density operator and wave function approach*; **§8.1** *General reservoir theory*; **§8.2** *Atomic decay by … reservoirs* | 248–251 | 268–271 |
| Squeezed-vacuum reservoir (which quadrature decoheres; `~QO-05`) | **§8.2.2** *Squeezed vacuum reservoir* | 253 | 273 |
| **Quantum-jump / collapse-operator** ("quantum jump") unravelling; Monte-Carlo wavefunction | **§8.5** *The 'quantum jump' approach to damping* (§8.5.2 *The wave function Monte Carlo approach*) | 260–263 | 280–283 |
| **Driven–damped two-level atom / optical Bloch equations**; steady state & saturation (`two_level_hamiltonian`, `steady_state_excited_population`) | **Ch. 10** *Resonance fluorescence*; **§10.C** *Equations of motion … of the density matrix in the bare-state basis* | 291, 320 | 311, 340 |

## Honesty notes (per the trunk's citation rule)
1. **Section-level by design.** Scully & Zubairy develop the master equation as
   *reservoir theory* (Ch. 8) rather than writing the modern Lindblad/GKSL line in
   one boxed equation; the explicit $\sum_k(L_k\rho L_k^\dagger-\tfrac12\{L_k^\dagger L_k,\rho\})$
   form used in `lindblad_rhs` is the standard GKSL generator equivalent to their
   damped density-matrix equations, and **the verification is the code** (trace,
   Hermiticity, positivity, and the decay rates are all checked numerically in
   `test_open_systems.py`).
2. **"$T_1$/$T_2$" naming.** The $T_1$ (energy) and $T_2$ (transverse) times are
   standard magnetic-resonance / quantum-optics nomenclature; SZ obtain the same
   rates ($\gamma$ for the population in §6.3, $\gamma/2$ + collisional dephasing
   for the coherence in §5.3) without always using the $T_1/T_2$ labels.
3. **Heading pages read; sub-section pages from the Contents.** See the offset note
   above — the four chapter/section headings were confirmed by reading the page;
   the sub-section folios come from the printed Contents at the verified +20 offset.

## See also
- `~QM-20` (the density operator and its **closed-system** von Neumann evolution
  $i\hbar\dot\rho=[H,\rho]$ — QO-04 is its irreversible, CPTP generalization, where
  the decoherence QM-20 only *names* becomes a dynamical law).
- `~QO-02` (two-level atom, Rabi frequency $\Omega$ — the coherent drive of the
  optical Bloch equations) and `~QO-03` (the spontaneous-emission rate $\gamma$ and
  why a two-level atom cannot be inverted — the saturation of P6).
- `~QO-05` (squeezed / nonclassical light — squeezed-vacuum reservoirs, SZ §8.2.2,
  decohere one quadrature faster than the other).
- Scully & Zubairy Ch. 8 (master equation, rigorous) and Ch. 10 (resonance
  fluorescence / optical Bloch); §5.3 (the two-level density matrix, gentle entry).
