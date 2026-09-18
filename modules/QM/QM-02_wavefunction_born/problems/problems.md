# QM-02 — Problems

Work them by hand, then check with `code/wavefunction.py`. Sources in `../refs.md`.
Setup for the `Check:` calls:
```python
import numpy as np, math
from wavefunction import *
x   = np.linspace(-18, 22, 4001)
psi = gaussian_packet(x, x0=2.0, sigma=1.0, k0=5.0)   # x0=2, sigma=1, k0=5, hbar=1
```

### P1.  Normalize a wavefunction  *(Griffiths 3e, Prob. 1.4, p.30)*
A state arrives un-normalized, $\Psi_{\text{raw}}(x)=C\,f(x)$. Born's rule needs
$\int|\Psi|^2dx=1$; find the rescaling and confirm the density now integrates to 1.
*Answer:* divide by $\sqrt{\int|\Psi_{\text{raw}}|^2dx}$; then $\int|\Psi|^2dx=1$.
*Check:*
```python
raw = 7.3*np.exp(-(x-1)**2/2)*np.exp(0.4j*x)
total_probability(normalize(raw, x), x)      # -> 1.0
```
(`test_normalize_makes_unit_integral`.)

**Solution.** Linearity of the Schrödinger equation means $A\Psi_{\text{raw}}$ is a state for any constant $A$; Born's rule fixes $|A|$. Demand
$$\int|A\Psi_{\text{raw}}|^2dx=|A|^2\!\int|\Psi_{\text{raw}}|^2dx=1\ \Rightarrow\ |A|=\Big(\!\int|\Psi_{\text{raw}}|^2dx\Big)^{-1/2}.$$
So the normalized state is $\Psi=\Psi_{\text{raw}}/\sqrt{\int|\Psi_{\text{raw}}|^2dx}$ (the overall phase of $A$ is physically irrelevant and left free). By construction $\int|\Psi|^2dx=\int|\Psi_{\text{raw}}|^2dx\big/\int|\Psi_{\text{raw}}|^2dx=1$. This is exactly what `normalize` does — divide by $\sqrt{\int|\Psi_{\text{raw}}|^2dx}$ — so `total_probability(normalize(raw, x), x)` returns $1.0$.

### P2.  Probability is the area under $|\Psi|^2$  *(Griffiths §1.3.2, Eq.1.16, p.26)*
For the Gaussian above, what is the probability of finding the particle between
$x=1$ and $x=3$ (i.e. within one $\sigma$ of the centre $x_0=2$)? And over the whole
line?
*Answer:* $P(1\le x\le 3)=\operatorname{erf}(1/\sqrt2)\approx0.6827$; $P(-\infty,\infty)=1$.
*Check:* `prob_between(psi, x, 1, 3)` ≈ 0.6827; `prob_between(psi, x, x[0], x[-1])` ≈ 1.0.
(`test_prob_symmetric_interval_is_erf`, `test_prob_over_whole_line_is_one`.)

**Solution.** The Born density is the normal density $|\Psi|^2=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-(x-x_0)^2/2\sigma^2}$ with $x_0=2,\ \sigma=1$. The interval $[1,3]$ is exactly $x_0\pm\sigma$, so substituting $u=(x-x_0)/\sigma$,
$$P(1\le x\le3)=\int_{1}^{3}|\Psi|^2dx=\frac{1}{\sqrt{2\pi}}\int_{-1}^{1}e^{-u^2/2}\,du=\operatorname{erf}\!\Big(\tfrac{1}{\sqrt2}\Big)\approx0.6827,$$
using $\frac{1}{\sqrt{2\pi}}\int_{-a}^{a}e^{-u^2/2}du=\operatorname{erf}(a/\sqrt2)$. Over the whole line the integral is the normalization, $=1$. These match `prob_between(psi, x, 1, 3)` $\approx0.68269$ and `prob_between(psi, x, x[0], x[-1])` $\approx1.0$.

### P3.  The "$1\sigma$, $2\sigma$, $3\sigma$" rule
Show that for *any* Gaussian state the probability of lying within $L$ standard
deviations of the mean is $\operatorname{erf}(L/\sqrt2)$, independent of
$x_0,\sigma$. Evaluate for $L=1,2,3$.
*Answer:* $0.6827,\ 0.9545,\ 0.9973$ (the familiar 68–95–99.7%).
*Check:*
```python
for L in (1,2,3):
    print(prob_between(psi, x, 2-L, 2+L), math.erf(L/math.sqrt(2)))
```
(`test_prob_symmetric_interval_is_erf`.)

**Solution.** For *any* mean $x_0$ and width $\sigma$, the substitution $u=(x-x_0)/\sigma$ removes both parameters:
$$P(|x-x_0|<L\sigma)=\int_{x_0-L\sigma}^{x_0+L\sigma}\frac{e^{-(x-x_0)^2/2\sigma^2}}{\sqrt{2\pi}\,\sigma}\,dx=\frac{1}{\sqrt{2\pi}}\int_{-L}^{L}e^{-u^2/2}\,du=\operatorname{erf}\!\Big(\tfrac{L}{\sqrt2}\Big),$$
a pure number depending only on $L$. Evaluating: $\operatorname{erf}(1/\sqrt2)=0.6827$, $\operatorname{erf}(2/\sqrt2)=0.9545$, $\operatorname{erf}(3/\sqrt2)=0.9973$ — the familiar 68–95–99.7% rule. The loop prints these alongside `math.erf(L/math.sqrt(2))`, agreeing to grid accuracy.

### P4.  Expectation values and the spread  *(Griffiths 3e, Prob. 1.5, p.30)*
For $\Psi\propto e^{-(x-x_0)^2/4\sigma^2}e^{ik_0x}$, compute $\langle x\rangle$,
$\langle x^2\rangle$ and the standard deviation $\sigma_x$ from the Born density.
*Answer:* $\langle x\rangle=x_0=2$, $\langle x^2\rangle=x_0^2+\sigma^2=5$,
$\sigma_x=\sigma=1$.
*Check:* `expectation_x(psi, x)` ≈ 2; `expectation_x2(psi, x)` ≈ 5; `sigma_x(psi, x)` ≈ 1.
(`test_expectation_x`, `test_expectation_x2`, `test_sigma_x`.)

**Solution.** The phase $e^{ik_0x}$ cancels in $|\Psi|^2=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-(x-x_0)^2/2\sigma^2}$, a normal density of mean $x_0$ and variance $\sigma^2$. Its first moment is the mean,
$$\langle x\rangle=\int x\,|\Psi|^2dx=x_0=2.$$
By the variance theorem $\sigma_x^2=\langle x^2\rangle-\langle x\rangle^2=\sigma^2$, so $\langle x^2\rangle=x_0^2+\sigma^2=4+1=5$ and $\sigma_x=\sqrt{5-4}=\sigma=1$. These reproduce `expectation_x(psi, x)` $\approx2$, `expectation_x2(psi, x)` $\approx5$, `sigma_x(psi, x)` $\approx1$.

### P5.  Momentum lives in the phase  *(Griffiths §1.5, Eqs.1.33–1.35, p.33)*
The factor $e^{ik_0x}$ contributes no probability density ($|e^{ik_0x}|=1$) yet sets
the momentum. Using $\hat p=-i\hbar\,\partial_x$, find $\langle p\rangle$ and
$\sigma_p$.
*Answer:* $\langle p\rangle=\hbar k_0=5$ (with $\hbar=1$); $\sigma_p=\hbar/2\sigma=0.5$.
*Check:* `expectation_p(psi, x)` ≈ 5 (finite diff.); `expectation_p_fft(psi, x)` = 5
(exact, via momentum space); `sigma_p(psi, x)` ≈ 0.5.
(`test_expectation_p_finite_difference`, `test_expectation_p_fft_is_exact`, `test_sigma_p`.)

**Solution.** Write $\Psi=g(x)\,e^{ik_0x}$ with $g$ the real Gaussian envelope. Then $\hat p\Psi=-i\hbar\,\partial_x\Psi=(\hbar k_0\,g-i\hbar\,g')\,e^{ik_0x}$, so
$$\Psi^*\hat p\,\Psi=\hbar k_0\,g^2-i\hbar\,g\,g'.$$
Integrating: $\int g^2dx=1$ gives $\hbar k_0$, while $\int g g'dx=\tfrac12\int(g^2)'dx=0$ (boundary terms vanish), so $\langle p\rangle=\hbar k_0=5$. For the spread, $\langle p^2\rangle=\hbar^2\!\int|\partial_x\Psi|^2dx=\hbar^2\!\big(k_0^2+\tfrac{1}{4\sigma^2}\big)$, hence $\sigma_p^2=\hbar^2/4\sigma^2$ and $\sigma_p=\hbar/2\sigma=0.5$. This matches `expectation_p_fft(psi, x)` $=5.0$ (the finite-difference `expectation_p` $\approx4.998$) and `sigma_p(psi, x)` $\approx0.499$.

### P6.  The minimum-uncertainty state  *(preview of ~QM-07)*
Form the product $\sigma_x\sigma_p$ for the Gaussian and compare it to the
Heisenberg bound $\hbar/2$.
*Answer:* $\sigma_x\sigma_p=\sigma\cdot\dfrac{\hbar}{2\sigma}=\dfrac{\hbar}{2}$ —
the Gaussian *saturates* the bound (no state is more localized in both $x$ and $p$).
*Check:* `sigma_x(psi, x)*sigma_p(psi, x)` ≈ 0.5 = ℏ/2.
(`test_minimum_uncertainty_product`.)

**Solution.** Combine the two closed forms from P4 and P5, $\sigma_x=\sigma$ and $\sigma_p=\hbar/2\sigma$:
$$\sigma_x\,\sigma_p=\sigma\cdot\frac{\hbar}{2\sigma}=\frac{\hbar}{2}.$$
The $\sigma$ cancels, so *every* Gaussian — no matter how wide or narrow — has the same product $\hbar/2$, the exact floor of the Heisenberg inequality $\sigma_x\sigma_p\ge\hbar/2$ (`~QM-07`). Squeezing the packet in $x$ (small $\sigma$) inflates $\sigma_p=\hbar/2\sigma$ in lockstep. Numerically `sigma_x(psi, x)*sigma_p(psi, x)` $\approx0.4994\approx\hbar/2=0.5$ (the tiny shortfall is finite-difference/grid error).

### P7.  Move to momentum space  *(Griffiths §3.4, p.134; ~MA-09)*
The momentum-space wavefunction is the Fourier transform
$\Phi(p)=(2\pi\hbar)^{-1/2}\!\int\Psi e^{-ipx/\hbar}dx$. Show $|\Phi(p)|^2$ is a
Gaussian centred at $p_0=\hbar k_0$ with width $\sigma_p=\hbar/2\sigma$, and that
$\int|\Phi|^2dp=1$ (Plancherel).
*Answer:* $|\Phi(p)|^2=\dfrac{1}{\sqrt{2\pi}\,\sigma_p}e^{-(p-\hbar k_0)^2/2\sigma_p^2}$;
$\int|\Phi|^2dp=1$.
*Check:*
```python
p, phi = momentum_space(psi, x)
p[np.argmax(np.abs(phi)**2)]                 # -> ~5.0  (peak at p = hbar*k0)
np.trapz(np.abs(phi)**2, p)                  # -> ~1.0  (Plancherel)
```
(`test_momentum_space_is_normalized`, `test_momentum_space_density_matches_closed_form_gaussian`.)

**Solution.** Insert $\Psi=(2\pi\sigma^2)^{-1/4}e^{-(x-x_0)^2/4\sigma^2}e^{ik_0x}$ into $\Phi(p)=(2\pi\hbar)^{-1/2}\!\int\Psi\,e^{-ipx/\hbar}dx$. Collecting exponentials, the integral is the Fourier transform of a Gaussian at wavenumber $q=p/\hbar-k_0$, which (completing the square) gives $\Phi(p)\propto\exp\!\big[-\sigma^2(p/\hbar-k_0)^2\big]=\exp\!\big[-\sigma^2(p-\hbar k_0)^2/\hbar^2\big]$. Therefore
$$|\Phi(p)|^2\propto\exp\!\Big[-\frac{(p-\hbar k_0)^2}{2\sigma_p^2}\Big],\qquad \frac{1}{2\sigma_p^2}=\frac{2\sigma^2}{\hbar^2}\ \Rightarrow\ \sigma_p=\frac{\hbar}{2\sigma},$$
a Gaussian centred at $p_0=\hbar k_0=5$ with width $\hbar/2\sigma$. Plancherel's theorem makes $\int|\Phi|^2dp=\int|\Psi|^2dx=1$. The code confirms the peak at `p[argmax|phi|^2]` $\approx5.0$ and `np.trapz(|phi|^2, p)` $\approx1.0$.

### P8.  Normalization survives time evolution  *(Griffiths §1.4, p.30; Prob. 2.21, p.80)*
A free Gaussian ($V=0$) spreads as it evolves. Show numerically that
$\int|\Psi(x,t)|^2dx$ stays 1 while $\sigma_x$ grows as
$\sigma_x(t)=\sigma_0\sqrt{1+\big(\hbar t/2m\sigma_0^2\big)^2}$.
*Answer:* the norm is conserved (the Schrödinger equation preserves it); the width
follows the spreading law above.
*Check:*
```python
xx = np.linspace(-40, 60, 8001); p0 = gaussian_packet(xx, 0.0, 1.0, 4.0)
pt = free_propagate(p0, xx, t=2.0)           # m=1, hbar=1
total_probability(pt, xx)                    # -> 1.0
sigma_x(pt, xx), 1.0*math.sqrt(1+(2/2)**2)   # -> (1.414..., 1.414...)
```
(`test_free_evolution_preserves_normalization`, `test_free_evolution_spreading_law`.)

**Solution.** Free evolution acts in momentum space as a pure phase: $\widetilde\Psi(k,t)=e^{-i\hbar k^2 t/2m}\,\widetilde\Psi(k,0)$. Since $|e^{-i\hbar k^2t/2m}|=1$, every mode keeps its modulus, so by Plancherel
$$\int|\Psi(x,t)|^2dx=\int|\widetilde\Psi(k,t)|^2\,dk=\int|\widetilde\Psi(k,0)|^2\,dk=1$$
for all $t$ — normalization is conserved. The phase does, however, dephase the modes and broaden the packet: a Gaussian spreads as $\sigma_x(t)=\sigma_0\sqrt{1+(\hbar t/2m\sigma_0^2)^2}$. At $t=2,\ m=\hbar=\sigma_0=1$ this is $\sqrt{1+1}=\sqrt2\approx1.4142$, matching `total_probability(pt, xx)` $\approx1.0$ and `sigma_x(pt, xx)` $\approx1.41421$.

### P9.  Ehrenfest: the centre moves classically  *(Griffiths 3e, Prob. 1.7, p.34)*
Ehrenfest's theorem says expectation values obey the classical laws. For the free
packet, where is the centre $\langle x\rangle(t)$ at time $t$, and how fast does it
move?
*Answer:* $\langle x\rangle(t)=x_0+\dfrac{\langle p\rangle}{m}t=x_0+\dfrac{\hbar k_0}{m}t$
— it drifts at the (group) velocity $\hbar k_0/m$, while $\langle p\rangle$ stays
constant ($V=0$, no force).
*Check:* `expectation_x(free_propagate(p0, xx, 1.0), xx)` ≈ `0 + 4*1` = 4;
`expectation_p_fft(free_propagate(p0, xx, 1.0), xx)` ≈ 4 (unchanged).
(`test_free_evolution_group_velocity`, `test_free_evolution_conserves_momentum`.)

**Solution.** Ehrenfest's theorem gives $\frac{d}{dt}\langle x\rangle=\frac{\langle p\rangle}{m}$ and $\frac{d}{dt}\langle p\rangle=\langle-\partial_xV\rangle$. With $V=0$ there is no force, so $\langle p\rangle=\hbar k_0$ stays constant; integrating the first equation,
$$\langle x\rangle(t)=x_0+\frac{\langle p\rangle}{m}\,t=x_0+\frac{\hbar k_0}{m}\,t,$$
i.e. the centroid drifts at the group velocity $\hbar k_0/m$. For $x_0=0,\ k_0=4,\ m=\hbar=1$, at $t=1$ this is $\langle x\rangle=0+4\cdot1=4$, while $\langle p\rangle=\hbar k_0=4$ is unchanged. These match `expectation_x(free_propagate(p0, xx, 1.0), xx)` $\approx4.0$ and `expectation_p_fft(...)` $\approx4.0$.
