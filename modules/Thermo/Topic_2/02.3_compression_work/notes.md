# 2.3 — Compression Work (notes)

This is module `2.2`'s integral with the limits reversed. Nothing new is
derived; what changes is the **sign**, and with it the engineering question.
Expansion asks how much work a gas will give you. Compression asks how much you
must pay — and, because the answer depends on the path, how to pay less. That
question is the whole design brief of a compressor (`8.1`) and of the intake
stroke of every cycle in Topic 9.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18). Units: $p$ in kPa, $V$ in m³, $W$ in kJ.

## 1. The same integral, and why the sign takes care of itself

The moving-boundary work is defined once [M Eq. 2.17, §2.2.3, p.48]:
$$W=\int_{V_1}^{V_2} p\,dV .$$
Nothing in it distinguishes compression from expansion. For a compression
$V_2<V_1$, so the integration runs from a larger limit to a smaller one and,
since $p>0$ throughout,
$$\boxed{\;W=\int_{V_1}^{V_2}p\,dV<0\quad (V_2<V_1)\;}$$
The negative sign is *produced by the limits*, not imposed by a convention on
top of them. Under the work-out-positive convention a negative $W$ means energy
flowed **into** the system, which is exactly what happened: the surroundings did
work on the gas.

The practically useful quantity is therefore the magnitude, the **work input**
$$W_{\text{in}}=-W=\int_{V_2}^{V_1}p\,dV>0,$$
`work_input`. `compression_work` returns the signed $W$ for the energy balance;
`work_input` returns what the motor must supply. Keeping both, under names that
cannot be confused, is deliberate — a sign error here propagates straight into
$\Delta U=Q-W$ and silently doubles the apparent heat transfer.

`compression_work` rejects $V_2>V_1$, mirroring `2.2`'s rejection of $V_2<V_1$.

## 2. The polytropic forms

Identical to `2.2`, since they are the same integral [M Example 2.1, pp.50–51]:
$$W=\frac{p_2V_2-p_1V_1}{1-n}\quad(n\neq1),
\qquad W=p_1V_1\ln\frac{V_2}{V_1}\quad(n=1),$$
with $p_2=p_1(V_1/V_2)^{n}$ — `polytropic_compression`. For a compression
$V_2/V_1<1$, so the logarithm is negative and the $n=1$ form returns $W<0$
automatically, again without a special case.

## 3. The exponent is the price, and this is why

Compressing 1 m³ of gas at 1 bar down to 0.5 m³ — a 2:1 reduction — along four
polytropic paths:

| $n$ | path | $p_2$ (kPa) | work input (kJ) |
|---|---|---|---|
| 1.0 | isothermal (perfectly cooled) | 200.0 | 69.31 |
| 1.2 | partly cooled | 229.7 | 74.35 |
| 1.3 | partly cooled | 246.2 | 77.05 |
| 1.4 | adiabatic (uncooled, air) | 263.9 | 79.88 |

The work input rises monotonically with $n$, and the mechanism is visible in the
$p_2$ column. Squeezing a gas does work on it; unless that energy is removed as
heat, it raises the internal energy and hence the temperature, and a hotter gas
at the same volume is at a **higher pressure**. The path therefore rides higher
on the $p$–$V$ diagram at every intermediate volume, enclosing more area — and
the area is the bill.

The two ends of the family are the two idealisations that matter:

- $n=1$ (**isothermal**) — all the heat of compression is removed as fast as it
  appears. Cheapest, and unattainable, because perfect cooling needs infinite
  time or infinite surface.
- $n=k$ (**adiabatic**, $k=1.4$ for air) — none of it is removed. Dearest, and
  the realistic limit for a fast machine, since a compression stroke lasting
  milliseconds has no time to shed heat.

Real compressors land between the two and are pushed toward the cheaper end by
**intercooling**: split the compression into stages and cool the gas back down
between them, so each stage starts low on the diagram instead of continuing up
the adiabatic. Module `8.1` costs this out for an actual machine; `9.5` shows
the same argument shaping the gas-turbine back work ratio.

## 4. Where the compression work goes

Applying the closed-system energy balance (`1.2`, `3.2`) to an **adiabatic**
compression, $Q=0$, so
$$\Delta U = Q - W = -W = W_{\text{in}}>0 .$$
Every joule supplied is stored as internal energy, and for an ideal gas
$\Delta U=mc_v\Delta T$ — the gas gets hot in direct proportion to the work
done on it. That is the physical content of `6.3`'s isentropic relation
$T_2/T_1=(p_2/p_1)^{(k-1)/k}$, and the reason `8.1`'s `fig2` can plot a
compressor's exit temperature as a measure of its inefficiency.

In an **isothermal** compression, by contrast, $\Delta U=0$ for an ideal gas, so
$Q=W<0$: every joule supplied leaves again as heat, and the gas ends as cool as
it began. The work has not been stored at all — it has been passed through.

## 5. Consistency checks in the code

`test_compression_work.py` pins: the negative sign for $V_2<V_1$; the
`work_input` magnitude; the polytropic closed form against the numerical
quadrature; the rejection of $V_2>V_1$; the monotone ordering of the table in §3
across $n=1.0,1.2,1.3,1.4$; and agreement with `2.2`'s expansion result run
backwards, since compressing 0.2→0.1 m³ must cost exactly what expanding
0.1→0.2 m³ returned along the same path.

## Where this goes

- `2.2` — the same integral for $V_2>V_1$, and M's worked Example 2.1.
- `1.2` / `1.5` — the general polytropic machinery and path-dependence.
- `6.3` — the isentropic ($n=k$) relations, and what an adiabatic compression
  does to the temperature.
- `8.1` — a real compressor: isentropic efficiency, the power actually drawn,
  and the exit temperature that inefficiency leaves behind.
- `9.2`–`9.5` — the compression strokes of the Otto, Diesel, dual and Brayton
  cycles, and the back work ratio that decides how much of the turbine's output
  survives.
