# SM-02 — Problems

Work by hand, then check with `code/laws_of_thermodynamics.py`. Citations in
`../refs.md`; **Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  Temperature of an ideal gas from entropy  *(Pa §1.2, p.3)*
Given S(U) = (3/2)Nk ln U + const, use 1/T = (∂S/∂U) to show U = (3/2)NkT
(equipartition). *Check:* `temperature_from_entropy(lambda U: 1.5*N*K_B*log(U), U)`
returns T with (3/2)NkT = U.

*Answer:* $1/T=\tfrac32 Nk/U\Rightarrow U=\tfrac32 NkT$ — temperature is the reciprocal slope of $S(U)$.

**Solution.** At fixed $V,N$, differentiate $S(U)=\tfrac32 Nk\ln U+\text{const}$:
$$\frac1T=\left(\frac{\partial S}{\partial U}\right)_{V,N}=\frac{d}{dU}\Big[\tfrac32 Nk\ln U\Big]=\frac{3Nk}{2U}.$$
Inverting gives $U=\tfrac32 NkT$ — exactly equipartition, $\tfrac12 kT$ for each of the three
translational degrees of freedom. Temperature is therefore not assumed but *emerges* as the
reciprocal slope of the entropy. For $N=1$ at $U=3\times10^{-21}\,$J this returns
$T=2U/(3k)=144.86$ K with $\tfrac32 kT=U$, matching
`temperature_from_entropy(lambda U: 1.5*N*K_B*log(U), U)`.

### P2.  Legendre transforms  *(Sch Ch.5, image-only)*
Starting from U(S,V), construct H, F, G and identify the natural variables of each.
Show G = H − TS = F + PV. *Check:* `gibbs_free_energy(U,T,S,P,V)` equals both
`enthalpy(U,P,V) − T*S` and `helmholtz_free_energy(U,T,S) + P*V`.

*Answer:* $H=U+PV\,(S,P)$; $F=U-TS\,(T,V)$; $G=U-TS+PV\,(T,P)$; and $G=H-TS=F+PV$.

**Solution.** The first law $dU=T\,dS-P\,dV$ makes $(S,V)$ the natural variables of $U$. Each
Legendre transform adds a conjugate product to swap one variable for the other:
$$\begin{aligned} H&=U+PV, & dH&=T\,dS+V\,dP &&(S,P),\\ F&=U-TS, & dF&=-S\,dT-P\,dV &&(T,V),\\ G&=U-TS+PV, & dG&=-S\,dT+V\,dP &&(T,P). \end{aligned}$$
Reading off the constructions, $G=(U+PV)-TS=H-TS$ and $G=(U-TS)+PV=F+PV$. Numerically at
$(U,T,S,P,V)=(100,300,0.2,10^5,10^{-3})$: $H=200$, $F=40$, $G=140$, with
$H-TS=200-60=140=F+PV=40+100$ — so `gibbs_free_energy(U,T,S,P,V)` equals both
`enthalpy(U,P,V) − T*S` and `helmholtz_free_energy(U,T,S) + P*V`.

### P3.  A Maxwell relation  *(Sch Ch.5, image-only)*
From dF = −S dT − P dV derive (∂S/∂V)_T = (∂P/∂T)_V, and verify both equal Nk/V for
the ideal gas (S = Nk(ln V + (3/2)ln T), P = NkT/V). *Check:*
`maxwell_relation_residual(S_TV, P_TV, T, V)` ≈ 0.

*Answer:* equality of $F$'s mixed second derivatives gives $(\partial S/\partial V)_T=(\partial P/\partial T)_V$; both equal $Nk/V$.

**Solution.** From $dF=-S\,dT-P\,dV$ the first derivatives are $S=-(\partial F/\partial T)_V$ and
$P=-(\partial F/\partial V)_T$. Because mixed second partials of $F$ commute,
$\partial^2F/\partial V\,\partial T=\partial^2F/\partial T\,\partial V$, so
$$\left(\frac{\partial S}{\partial V}\right)_T=-\frac{\partial^2F}{\partial V\,\partial T}=-\frac{\partial^2F}{\partial T\,\partial V}=\left(\frac{\partial P}{\partial T}\right)_V.$$
For the ideal gas $S=Nk\big(\ln V+\tfrac32\ln T\big)$ gives $(\partial S/\partial V)_T=Nk/V$, and
$P=NkT/V$ gives $(\partial P/\partial T)_V=Nk/V$ — identical. The two sides agree to a relative
residual $\sim3\times10^{-5}$, so `maxwell_relation_residual(S_TV, P_TV, T, V)` $\approx 0$.

### P4.  Carnot efficiency and COP  *(Sch Ch.4, image-only)*
Show η_Carnot = 1 − Tc/Th, and that the same cycle run backwards has refrigerator
COP = Tc/(Th−Tc) and heat-pump COP = 1 + COP_fridge. *Check:* `carnot_efficiency(300,600)`
= 0.5; `carnot_cop_heat_pump(270,300)` = 1 + `carnot_cop_refrigerator(270,300)`.

*Answer:* $\eta=1-T_c/T_h$; refrigerator $\text{COP}=T_c/(T_h-T_c)$; heat pump $T_h/(T_h-T_c)=1+\text{COP}_{\text{fridge}}$.

**Solution.** A reversible cycle returns to its initial state, so its total entropy change is zero
and the heats obey $Q_h/T_h=Q_c/T_c$, i.e. $Q_c/Q_h=T_c/T_h$. With energy conservation
$W=Q_h-Q_c$, the efficiency is
$$\eta=\frac{W}{Q_h}=1-\frac{Q_c}{Q_h}=1-\frac{T_c}{T_h}.$$
Run in reverse as a refrigerator, $\text{COP}=Q_c/W=(T_c/T_h)/(1-T_c/T_h)=T_c/(T_h-T_c)$; as a heat
pump it delivers $Q_h$, so $Q_h/W=T_h/(T_h-T_c)=1+T_c/(T_h-T_c)=1+\text{COP}_{\text{fridge}}$. Thus
`carnot_efficiency(300,600)` $=1-\tfrac{300}{600}=0.5$ and `carnot_cop_heat_pump(270,300)`
$=\tfrac{300}{30}=10=1+9=$ `1 + carnot_cop_refrigerator(270,300)`.

### P5.  The second law in a heat flow  *(Pa §1.3, p.6)*
A quantity of heat Q passes from a hot reservoir T_h to a cold one T_c. Show the
total entropy change is Q(1/T_c − 1/T_h) > 0, and that it → 0 in the reversible limit
T_h → T_c. *Check:* `total_entropy_change_heat_flow(10, 500, 300) > 0` and decreases
as the reservoirs approach the same temperature.

*Answer:* $\Delta S_{\text{total}}=Q\big(1/T_c-1/T_h\big)>0$ for $T_h>T_c$, and $\to0$ as $T_h\to T_c$.

**Solution.** Take both reservoirs large enough that their temperatures hold fixed, so each
entropy change is $\Delta S=Q_{\text{in}}/T$. The hot reservoir loses $Q$ and the cold one gains it:
$$\Delta S_{\text{total}}=-\frac{Q}{T_h}+\frac{Q}{T_c}=Q\left(\frac1{T_c}-\frac1{T_h}\right)=Q\,\frac{T_h-T_c}{T_hT_c}.$$
For $T_h>T_c$ the numerator is positive, so $\Delta S_{\text{total}}>0$: heat flows hot$\to$cold
spontaneously, never the reverse — the second law. As $T_h\to T_c$ the gap $T_h-T_c\to0$ and the
transfer becomes reversible, $\Delta S\to0$. Hence `total_entropy_change_heat_flow(10, 500, 300)`
$=10\big(\tfrac1{300}-\tfrac1{500}\big)\approx1.33\times10^{-2}$ J/K $>0$, shrinking toward zero as
the reservoir temperatures converge.
