# PK-03 — References

| Book | File | Notes |
|---|---|---|
| Michel, *Introduction to Laser-Plasma Interactions* (Springer) | `PK_Plasma_Kinetic_Theory/Laser_plasma_pierre_michel.pdf` | primary source; cited at **section level** |
| Rhodes (ed.), *Excimer Lasers* (Topics in Applied Physics) | `PK_Plasma_Kinetic_Theory/Excimer_Lasers_Topics_Rhodes.pdf` | same shelf; not used for this module (excimer/laser kinetics → `~PK-04`) |

> **Granularity.** Section numbers/titles below are read from the PDF's own
> bookmarks/table of contents (verified against the outline), so they are real and
> stable. **Printed↔PDF page offsets were not checked, so citations are given by
> section, not page** — open the PDF and use the bookmark tree to navigate
> (cf. `~SM-06/refs.md`, which does verify page numbers for Pathria). The Formulary
> (Appendix A) collects the closed-form dispersion and damping relations used in the
> code.

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| Debye length & screening (`debye_length`) | M | §1.2.1 *The Plasma State; Debye Length and Screening* |
| plasma frequency (`plasma_frequency`) | M | §1.2.2 *The Plasma Frequency* |
| Maxwellian distribution, thermal speed (`thermal_speed`) | M | §1.2.3 *Equilibrium (Maxwellian) Velocity Distributions in Plasmas* |
| Vlasov vs. fluid description (the dielectric function's origin) | M | §1.2.4 *Kinetic (Vlasov) and Fluid Descriptions of Plasmas* (→ `~PK-01`) |
| longitudinal-wave dielectric framework; two-stream susceptibility (`two_stream_growth_rate`) | M | §1.3.1.3 *Longitudinal (Plasma) Waves: General Description* |
| Langmuir / Bohm–Gross (`bohm_gross`) | M | §1.3.1.4 *Electron Plasma Waves (EPWs)* |
| ion-acoustic waves (`ion_acoustic`) | M | §1.3.1.5 *Ion Acoustic Waves (IAWs)* |
| kinetic dispersion; the Landau contour | M | §1.3.3 *Kinetic Description of Plasma Waves* |
| Landau damping closed form (`landau_damping_rate`) | M | §1.3.4 *Landau Damping* |
| general theory of instability growth rates | M | Ch. 6 *Introduction to Three-Wave Instabilities* (esp. §6.4 *Temporal Growth Rate*) |
| formulary: EPWs, IAWs, plasma dispersion function, Landau damping | M | Appendix A *Formulary* — §A.1 *Plasma Parameters*, §A.2.2 *EPWs*, §A.2.3 *IAWs*, §A.3 *Plasma Dispersion Function*, §A.4 *Landau Damping* |

> **On the two-stream instability.** Michel's Ch. 1 develops the longitudinal
> dielectric/susceptibility form ε(k,ω)=0 (§1.3.1.3); the **cold counter-streaming
> two-stream** dispersion `1 = ½ω_p²[1/(ω−kv₀)²+1/(ω+kv₀)²]` is the standard
> textbook archetype obtained by inserting two cold drifting populations into that
> same susceptibility, with the growth-rate machinery of Ch. 6. (Michel's later
> chapters treat the laser-driven three-wave instabilities — SBS, SRS, TPD — rather
> than the cold beam-plasma mode.)

## See also
- `~PK-01` (the Vlasov equation and f₀(v) behind the dielectric function — Michel §1.2.4) and `~PK-02` (the fluid moments that reproduce Bohm–Gross / ion-acoustic without kinetic damping).
- `~MA-06` (complex analysis — the Landau contour is a residue/analytic-continuation calculation) and `~CM-15` / `~CM-25` / `~EM-15` (the oscillator and dispersive-wave language).
- Michel Ch. 1 + Formulary A (rigorous, laser-plasma framing). The classic cold two-stream derivation is standard in Chen, Nicholson, or Krall–Trivelpiece.
