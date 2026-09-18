# EM-12 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed in Ch. 7 against the page text (PDF p.321 carries printed
"303"). The induction physics this module drives (`~EM-11`) lives in the same §7.1–7.2.

**Citation caveat (read this).** AC steady-state circuit theory — complex impedance, the
driven series RLC, resonance and Q — is **not** a numbered section in Griffiths. He
develops it in the **Chapter 7 problems**, building on the EMF and inductance of §7.1–7.2.
So the table below cites only the *underlying* physics Griffiths treats in numbered
sections (EMF §7.1.2 p303, inductance §7.2.3 p321), and the impedance/resonance method is
referenced as the standard complex-exponential technique (`~MA-05`/`~MA-06`; Boas
Ch. 2 §16) plus the `~CM-15` driven-oscillator analogy. **No Griffiths page or equation
number is invented for impedance, Z_C, or resonance** — those rows are marked "—".

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| EMF driving current, V = IR (`impedance_resistor`) | §7.1.2 *Electromotive Force* | 303 | 321 |
| self-inductance, Φ = LI, EMF = −L dI/dt (`impedance_inductor`) | §7.2.3 *Inductance* (Eq. 7.27–7.28) | 321 | 339 |
| energy stored in L and C (½LI², ½CV²) | §7.2.4 *Energy in Magnetic Fields* (Eq. 7.34) | 328 | 346 |
| capacitive reactance Z_C = 1/(iωC) (`impedance_capacitor`) | complex method — Boas Ch. 2 §16; `~MA-05` | — | — |
| series/parallel impedance, Z = R + i(ωL − 1/ωC) (`series_rlc_impedance`, `impedance_series`, `impedance_parallel`) | Gr Ch. 7 *problems*; complex method (`~MA-05`/`~MA-06`) | — | — |
| resonance ω₀ = 1/√(LC), Q, bandwidth (`resonant_frequency`, `quality_factor`, `bandwidth`) | not a numbered Gr section; `~CM-15` driven-oscillator resonance | — | — |
| amplitude / phase / average power (`current_amplitude`, `current_phase`, `average_power`) | phasor Ohm's law; ⟨P⟩ on R — `~CM-15` | — | — |

## See also
- `~EM-11` (electromagnetic induction) — the EMF and inductance this module drives; the
  same Gr §7.1–7.2.
- `~CM-15` (oscillations — damped, driven, resonance, Q): the **mechanical twin**. The
  series RLC is its term-for-term re-labelling (**KEY BRIDGE B6**), so every resonance/Q
  result is shared; the worked source is the classical oscillations chapter (Marion &
  Thornton; Fowles & Cassiday).
- `~MA-05` / `~MA-06` (complex numbers & analysis) — the e^{iωt} phasor method that turns
  the loop ODE into V = IZ.
- **Boas, *Mathematical Methods in the Physical Sciences*, 3rd ed., Ch. 2 §16 "AC
  circuits"** — the worked complex-impedance treatment used here; the method reference in
  place of a Griffiths section.
- `~EM-16` for transmission-line (characteristic) impedance and cavity Q; `~EM-15` for the
  wave impedance η = √(μ/ε).
- Higher level: Jackson, *Classical Electrodynamics* 3e (impedance and quasistatics appear
  in the circuits/waveguide material); Schwinger, *Classical Electrodynamics*
  (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
