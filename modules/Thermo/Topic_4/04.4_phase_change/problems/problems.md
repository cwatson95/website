# 4.4 — Problems

Check with `code/phase_change.py`. Citations in `../refs.md`. `x` is dimensionless (0–1).

### P1.  Specific volume from quality  *(Moran 8e Eq. 3.2, p.108)*
Water at 100 °C has `vf = 1.0435×10⁻³` and `vg = 1.673 m³/kg`. Find `v` at `x = 0.9`.
*Answer:* `v = vf + x(vg−vf) = 1.506 m³/kg`. *Check:*
`mixture_property(1.0435e-3, 1.673, 0.9)` ≈ 1.506.

### P2.  Quality from a measured property  *(Moran 8e §3.5.2, p.108)*
A mixture has `v = 1.506 m³/kg` between `vf = 1.0435×10⁻³` and `vg = 1.673`. Find `x`.
*Answer:* `x = (v−vf)/(vg−vf) = 0.9`. (Same inversion works for `u`, `h`, `s`.)
*Check:* `quality_from_property(1.506, 1.0435e-3, 1.673)` ≈ 0.9.

### P3.  Liquid occupies almost no volume (HW 3.16)  *(Moran 8e §3.3, p.152)*
A 1 m³ rigid tank holds CO₂ at `x = 0.70` with `vf = 0.9827×10⁻³`, `vg = 1.756×10⁻²
m³/kg`. Find the total mass, the masses of liquid and vapor, and the % of the volume
the liquid occupies.
*Answer:* `v = 0.01259 m³/kg`, `m = 1/0.01259 = 79.4 kg`; `m_vap = 0.7m = 55.6 kg`,
`m_liq = 0.3m = 23.8 kg`; `V_liq = m_liq·vf = 0.0234 m³ → 2.34 %`. Despite being 30 %
of the *mass*, the liquid is ~2 % of the *volume* (`vg ≫ vf`). *Check:*
`liquid_volume_fraction(0.7, 0.9827e-3, 1.756e-2)` ≈ 0.0234.

### P4.  Latent heat  *(Moran 8e §3.5.2)*
Find the latent heat of vaporization of water at 100 °C given `hf = 419.04`,
`hg = 2676.1 kJ/kg`. What happens to `hfg` as pressure approaches the critical point?
*Answer:* `hfg = hg − hf = 2257 kJ/kg`; `hfg → 0` at the critical point (liquid and
vapor become indistinguishable). *Check:* `latent_heat(419.04, 2676.1)` ≈ 2257.
