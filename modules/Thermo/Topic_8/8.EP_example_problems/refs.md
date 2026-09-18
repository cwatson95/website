# 8.EP — References

Examples read page-by-page from the PDF. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| 4.5 | Calculating Compressor Power | 190–191 | 208–209 |
| 4.7 | Evaluating Performance of a Power Plant Condenser | 197–198 | 215–216 |
| 4.8 | Cooling Computer Components | 198–199 | 216–217 |
| 6.14 | Evaluating Isentropic Compressor Efficiency | 338–339 | 356–357 |
| 10.1 | Analyzing an Ideal Vapor-Compression Refrigeration Cycle | 614–615 | 632–633 |
| 10.2 | Considering the Effect of Irreversible Heat Transfer on Performance | 616–617 | 634–635 |
| 10.3 | Analyzing an Actual Vapor-Compression Refrigeration Cycle | 618–619 | 636–637 |
| 10.4 | Analyzing an Actual Vapor-Compression Heat Pump Cycle | 630–632 | 648–650 |

## Equations used
Mass flow `ṁ = AV/v` (Eq. 4.4b, §4.2.1, p.172; ideal-gas form per Ex 4.5); steady CV
energy balance (Eq. 4.20a, §4.5.1, p.181) with the compressor (§4.8.1, p.190),
single-stream condenser (Ex 4.7(b), p.198), and two-stream exchanger (Eq. 4.18;
Ex 4.7(a), p.197) reductions; isentropic compressor efficiency (Eq. 6.48, §6.12.3,
p.338); vapor-compression relations (Eqs. 10.1, 10.3–10.10, pp.611–630);
`1 ton = 211 kJ/min` (per Ex 10.1, p.615). Canonical implementations in module `8.EQ`.

Property values embedded in the examples are the ones the book quotes from its
Tables A-2/A-3 (water), A-9 (R-22), A-10/A-11/A-12 (R-134a), and A-22 (air).

## See also
`8.EQ` (the equations these use), `8.HP` (homework problems), and the concept modules
`08.1`–`08.4` (each anchors its own demo on a subset of these Examples).
