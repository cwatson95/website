# ST-16 — Transformations of Random Variables

Module of the **PROBABILITY THEORY** trunk (a module-by-module replica of Penn
State's STAT 414; see `modules/ST/list_ST.txt`). Covers **STAT 414 Lessons 22–24**:
Functions of One Random Variable (L22), Transformations of Two Random Variables
(L23), and Several Independent Random Variables (L24). Given a random variable $X$
with known density $f_X$ and a function $Y=g(X)$, what is the density $f_Y$? This
module answers it three ways.

- **Prerequisites:** `~ST-10` (continuous random variables — pdf/cdf, the uniform
  distribution), `~ST-11` (exponential, gamma & chi-square — the gamma function
  $\Gamma$), `~ST-13` (joint distributions of two variables — joint/marginal pdfs),
  `~MA-03` (coordinate systems & **Jacobians** — the determinant that rescales the
  joint density), `~MA-09` (Fourier transforms & the **convolution** theorem — the
  analytic engine behind sums of independent variables).
- **Cross-links:** `~ST-17` (the **MGF technique** — convolution $\leftrightarrow$
  *products* of moment-generating functions; chi-square / $t$ / $F$ sampling laws,
  whose first member $\chi^2_1=Z^2$ is derived here), `~ST-06` (mgfs), `~ST-12`
  (the normal distribution — standardized here, squared into $\chi^2_1$), `~ST-18`
  (the central limit theorem — the limiting transform of a sum), `~SM-06`
  (Maxwell speed distribution — a physics change-of-variables from velocity to
  speed), `~MA-19` (probability & statistics foundations).

## Scope

Three tools turn the law of $X$ into the law of $Y=g(X)$.

1. **The cdf (distribution-function) method.** Always works: build the cdf of $Y$
   by integrating $f_X$ over the event $\{x:g(x)\le y\}$,
   $F_Y(y)=P(g(X)\le y)$, then differentiate, $f_Y=F_Y'$. Code: `cdf_of_Y`,
   `pdf_of_Y_cdf_method`. Worked: $X\sim U(0,1),\,Y=X^2\Rightarrow F_Y=\sqrt y$.

2. **The change-of-variables formula** for a one-to-one (monotone) $g$, the
   differentiated cdf method:
   $$f_Y(y)=f_X\!\big(g^{-1}(y)\big)\,\Big|\tfrac{dx}{dy}\Big|.$$
   The factor $|dx/dy|$ is the local stretch of the transform. Code:
   `change_of_variables_1d`. Worked: $Y=-\ln X/\lambda$ on $U(0,1)$ gives
   $\mathrm{Exp}(\lambda)$ (inverse-transform sampling).

3. **The 2-D Jacobian transformation** (L23): for $(U,V)=T(X,Y)$ one-to-one,
   $$f_{UV}(u,v)=f_{XY}\!\big(x(u,v),y(u,v)\big)\,\big|J\big|,\qquad
   J=\det\frac{\partial(x,y)}{\partial(u,v)}\quad(\text{Jacobian, see ~MA-03}).$$
   Code: `jacobian_det_2d`, `jacobian_transform_2d`.

**Sums of independent variables** (L23–L24) are the transform $Z=X+Y$, whose
density is the **convolution**
$$f_{X+Y}(z)=\int_{-\infty}^{\infty} f_X(t)\,f_Y(z-t)\,dt,$$
the probabilistic mirror of the Fourier convolution theorem (`~MA-09`; the same
sum becomes a *product* of mgfs in `~ST-17`). Code: `convolution`. Two canonical
results: $U(0,1)+U(0,1)$ is **triangular**, and a sum of $n$ i.i.d.
$\mathrm{Exp}(\lambda)$ is **Gamma$(n,\lambda)$** (Erlang). Finally the
**probability integral transform** $F_X(X)\sim U(0,1)$ — the change-of-variable
identity in disguise, the basis of random-number generation (`probability_integral_transform_pdf`).

## Operations — `code/transformations.py`

| call | meaning | reference |
|------|---------|-----------|
| `uniform_pdf(x,a,b)` | $U(a,b)$ density $1/(b-a)$ on $[a,b]$ | PSU L10 |
| `exp_pdf(x,rate)` / `exp_cdf(x,rate)` | $\mathrm{Exp}(\lambda)$: $\lambda e^{-\lambda x}$, $1-e^{-\lambda x}$ | PSU L15; `~ST-11` |
| `exp_quantile(u,rate)` | $F^{-1}(u)=-\ln(1-u)/\lambda$ | PSU L22 |
| `gamma_pdf(x,k,rate)` | $\dfrac{\lambda^k}{\Gamma(k)}x^{k-1}e^{-\lambda x}$ | PSU L15; `~ST-11` |
| `triangular_pdf(z)` | $z$ on $[0,1]$, $2-z$ on $[1,2]$ (sum of two $U(0,1)$) | PSU L23 |
| `normal_pdf(x,mu,sigma)` / `normal_cdf(x,mu,sigma)` | $\phi$, $\Phi=\tfrac12(1+\mathrm{erf}(\cdot))$ | PSU L16; `~ST-12` |
| `cdf_of_Y(fX,g,y,x_lo,x_hi)` | $F_Y(y)=\int_{\{g(x)\le y\}}f_X\,dx$ (cdf method) | PSU L22 |
| `pdf_of_Y_cdf_method(fX,g,y,...)` | $f_Y=\dfrac{d}{dy}F_Y$ (differentiated cdf method) | PSU L22 |
| `change_of_variables_1d(fX,ginv,dxdy,y)` | $f_Y(y)=f_X(g^{-1}(y))\,\lvert dx/dy\rvert$ | PSU L22 |
| `jacobian_det_2d(inv_map,u,v)` | $J=x_uy_v-x_vy_u$ of $(u,v)\!\to\!(x,y)$ | PSU L23; `~MA-03` |
| `jacobian_transform_2d(fXY,inv_map,u,v)` | $f_{UV}=f_{XY}(x,y)\,\lvert J\rvert$ | PSU L23 |
| `convolution(fX,fY,z,t_lo,t_hi)` | $f_{X+Y}(z)=\int f_X(t)f_Y(z-t)\,dt$ | PSU L23; `~MA-09` |
| `sum_two_uniforms_pdf(z)` | closed form: $U(0,1)^{*2}=$ triangular | PSU L23 |
| `sum_n_exponentials_pdf(z,n,rate)` | closed form: $\mathrm{Exp}^{*n}=$ Gamma$(n,\lambda)$ | PSU L24 |
| `probability_integral_transform_pdf(fX,Finv,u)` | $f_X(F^{-1}(u))\,\lvert dF^{-1}/du\rvert\equiv1$ | PSU L22 |

## Use
```python
import math
from transformations import (cdf_of_Y, change_of_variables_1d, convolution,
                             jacobian_transform_2d, jacobian_det_2d,
                             uniform_pdf, exp_pdf, gamma_pdf, triangular_pdf,
                             probability_integral_transform_pdf, exp_quantile)

# cdf method: X~U(0,1), Y=X^2 -> F_Y(y)=sqrt(y)
cdf_of_Y(uniform_pdf, lambda x: x*x, 0.25, 0.0, 1.0)            # 0.5  = sqrt(0.25)

# change of variables: Y = -ln(X)/rate on U(0,1) -> Exp(rate)
change_of_variables_1d(uniform_pdf, lambda y: math.exp(-1.5*y),
                       lambda y: -1.5*math.exp(-1.5*y), 1.0)    # 0.3347 = Exp(1.5)

# sum of two uniforms is triangular; sum of two exponentials is Gamma(2)
convolution(uniform_pdf, uniform_pdf, 1.0, 0.0, 1.0)           # 1.0   (triangular peak)
convolution(exp_pdf, exp_pdf, 2.0, 0.0, 2.0)                   # 0.2707 = Gamma(2,1) at 2

# 2-D Jacobian: X,Y~Exp(1); U=X+Y, V=X/(X+Y); inverse x=uv, y=u(1-v), |J|=u
fXY = lambda x, y: float(exp_pdf(x,1.0))*float(exp_pdf(y,1.0))
inv = lambda u, v: (u*v, u*(1-v))
jacobian_transform_2d(fXY, inv, 1.5, 0.3)                      # 0.3347 = 1.5 e^-1.5

# probability integral transform: F_X(X) ~ Uniform(0,1)
probability_integral_transform_pdf(lambda x: exp_pdf(x,2.0),
                                   lambda u: exp_quantile(u,2.0), 0.5)   # 1.0
```

## Run
```bash
cd code
python3 transformations.py        # demo: cdf method, change of vars, convolution, Jacobian, PIT
python3 test_transformations.py   # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — the cdf method → change-of-variables formula → 2-D Jacobian →
  convolution; the triangular and gamma sums; the probability integral transform;
  the bridge to mgfs (`~ST-17`)
- `code/transformations.py`, `code/test_transformations.py` (numpy + stdlib only, self-contained)
- `problems/problems.md` — worked problems (STAT 414 L22–24; cross-checks to the code)
- `refs.md` — citation table (STAT 414 OER primarily; Hogg–Tanis–Zimmerman, Wackerly, Ross at chapter level)
