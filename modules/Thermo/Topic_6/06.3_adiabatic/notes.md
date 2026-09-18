# 6.3 — Adiabatic & Isentropic Processes (notes)

Citations: **M** = Moran 8e; *printed* pages (PDF = printed + 18; `refs.md`).

## 1. Adiabatic vs. isentropic
**Adiabatic** means no heat transfer, `Q = 0`. From the entropy balance an adiabatic
closed system has `ΔS = σ ≥ 0`: entropy can still *rise* if irreversibilities are present.
An adiabatic process that is **also internally reversible** has `σ = 0`, hence `ΔS = 0` —
a constant-entropy = **isentropic** process [M §6.6, p.302]. (So *isentropic* ⇒ adiabatic
+ internally reversible; an actual adiabatic device, e.g. a real turbine, is *not*
isentropic because σ > 0.)

## 2. Ideal-gas entropy change (the parent relations)
For an ideal gas [M §6.5, p.300–301]:
$$s_2-s_1=s^\circ(T_2)-s^\circ(T_1)-R\ln\tfrac{p_2}{p_1}\;(6.20a),\qquad
s_2-s_1=c_p\ln\tfrac{T_2}{T_1}-R\ln\tfrac{p_2}{p_1}\;(6.22,\ \text{const }c_p).$$

## 3. Isentropic ideal-gas relations (set s₂ = s₁)
**Air tables** (relative pressure `p_r`, relative volume `v_r`) [M §6.11.2, p.327–328]:
$$\frac{p_2}{p_1}=\frac{p_r(T_2)}{p_r(T_1)}\;(6.41),\qquad \frac{v_2}{v_1}=\frac{v_r(T_2)}{v_r(T_1)}\;(6.42)\quad(\text{air only}).$$
**Constant specific-heat ratio `k`** (the *cold-air-standard*), with `c_p=kR/(k-1)`,
`c_v=R/(k-1)` (Eq. 3.47) [M §6.11.2, p.328]:
$$\frac{T_2}{T_1}=\Big(\frac{p_2}{p_1}\Big)^{\!\frac{k-1}{k}}\!(6.43),\quad
\frac{T_2}{T_1}=\Big(\frac{v_1}{v_2}\Big)^{\!k-1}\!(6.44),\quad
\frac{p_2}{p_1}=\Big(\frac{v_1}{v_2}\Big)^{\!k}\!\iff\! pv^{k}=\text{const}\;(6.45).$$
So `pv^k = const` is exactly the constant-`k` isentropic of an ideal gas (the polytropic
process with `n = k`).

## 4. Isentropic efficiency (the bridge to real devices)
A real **adiabatic** device is compared to an isentropic one between the *same inlet state
and same exit pressure* [M §6.12, p.333–335]:
$$\eta_t=\frac{h_1-h_2}{h_1-h_{2s}}\;(6.46),\qquad
\eta_{\text{nozzle}}=\frac{V_2^2/2}{(V_2^2/2)_s}\;(6.47).$$
Because σ ≥ 0 forces `s₂ ≥ s₁`, state 2s (the isentropic exit) bounds the best output;
typical `η_t ≈ 0.7–0.9`, nozzle `η ≥ 0.95`.

**Adiabatic + internally reversible = isentropic.** *Check (M Ex 6.9, air, 1 atm/540 °R →
1160 °R):* `p₂ = p₁·p_r2/p_r1 = 1·21.18/1.3860 = 15.28 atm` (tables); with `k = 1.39`,
`p₂ = (1160/540)^{1.39/0.39} = 15.26 atm` (Eq. 6.43). *Check (M Ex 6.12, air turbine):*
`(Ẇ/ṁ)_s = h₁−h₂s = 390.88−285.27 = 105.6`, so `η_t = 74/105.6 = 0.70`.

## Bridge
The σ = 0 condition is module `6.1`; the σ ≥ 0 inequality that makes real adiabatic devices
fall short of isentropic is module `6.2`. These isentropic relations and efficiencies size
every turbine, compressor, nozzle, and pump in Topics 7–9.
