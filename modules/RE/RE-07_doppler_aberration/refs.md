# RE-07 — References

Page-level citations **verified by reading the page text** in the PDFs under
`books/library/` (via PyMuPDF, not inferred from a table of contents).
**Printed** = the number on the page; **PDF** = the page index in the viewer.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

## Topic → location (verified)

| Topic (code symbol) | Source | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|---|
| Relativistic Doppler from the 4-vector `k=(ω,𝐤)` (`four_wavevector`, `transform_wavevector`) | Zee | §III.3 *Minkowski and the Geometry of Spacetime*, **"The relativistic Doppler shift"** | 185 | 208 |
| Angular Doppler `ω' = γω(1 + β cosθ)`, blue/redshift limits (`doppler_general`, `doppler_longitudinal`) | Zee | §III.3, **Eq. (9)** + the `θ≈0`/`θ≈π` discussion | 185–186 | 208–209 |
| Transverse factor = time dilation `1/√(1−u²)` (`doppler_transverse`) | Zee | §III.3, remark after Eq. (9) ("…due to time dilation") | 186 | 209 |
| Aberration = transform of `k_x', k_y'` (`aberration`) | Zee | §III.3, the `k'_x=(k_x+uω)/√(1−u²)`, `k'_y=k_y` lines | 185 | 208 |
| Worked SR method (events, primed/unprimed frames) | Zee | §III.4 *Special Relativity Applied* | 195 | 218 |
| Aberration of starlight (named, historical — Michelson–Morley context) | Griffiths | §12.1 *The Special Theory of Relativity* | 505 | 523 |

**Verification notes (honest scope).**
- Zee printed **185** literally carries the section header *"The relativistic Doppler
  shift"* and derives it from `k = (ω, 𝐤)` with `ω² = 𝐤²`, demanding the phase
  `k'x' = kx` so that `k` transforms as a 4-vector — i.e. **exactly this module's
  construction**. The displayed result is `ω' = ω(1 + u cosθ)/√(1−u²)` (Eq. 9), with
  blueshift `√((1+u)/(1−u))` at `θ≈0` and redshift `√((1−u)/(1+u))` at `θ≈π`. Zee's
  `+u` sign convention is the mirror of RE-03's `+β` boost (`u = −β`); the physics
  and the longitudinal limits are identical. The same page's `k'_x, k'_y` lines are
  the aberration transformation.
- Griffiths 4e printed **505** (PDF 523) is the **Michelson–Morley** discussion; the
  phrase *"the aberration of starlight"* appears there as a historical observation
  (with a footnote to Resnick), **not** as a derivation of `cosθ' = (cosθ−β)/(1−β cosθ)`.
  Cited only for the *phenomenon's name and history*. Griffiths 4e Ch. 12 has **no**
  page that prints the word "Doppler" (its only "Doppler" pages are in Ch. 11 on
  Liénard/Larmor radiation), so **Zee is the verified primary** for the Doppler and
  aberration formulae here.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. 2 (special relativity:
  Doppler & aberration) — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 2 (special relativity) —
  `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so no page numbers are
  cited — same policy as Butkov in the MA trunk and d'Inverno/Weinberg in RE-03.)*
- Terrell, *Phys. Rev.* **116**, 1041 (1959) and Penrose, *Proc. Camb. Phil. Soc.*
  **55**, 137 (1959) — the "invisibility of length contraction" / apparent rotation
  (the §6 note). Cited by name only; not in the local library.
