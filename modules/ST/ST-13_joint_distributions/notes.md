# ST-13 — Joint Distributions of Two Random Variables (notes)

A single random variable $X$ carries a pmf or pdf $f(x)$ that assigns probability
to its values (`~ST-05`, `~ST-10`). Most real questions involve **two** quantities
measured on the same experiment — height *and* weight, a particle's energy *and*
its angle, today's return *and* tomorrow's. A **joint distribution** assigns
probability to the *pair* $(X,Y)$, and from it we recover each variable alone
(**marginals**), test whether they carry independent information (**independence**),
and average any function of the two (**expectation**). The discrete theory (STAT
414 **L17**) and the continuous theory (**L20**) are the *same statements* with
$\sum\leftrightarrow\int$; these notes run them in two columns and tie every result
to a function in `code/joint_distributions.py`.

Citation key (full details + granularity in `refs.md`): **PSU L17/L20** = Penn
State STAT 414 Lessons 17 and 20; **HTZ** = Hogg, Tanis & Zimmerman, *Probability
and Statistical Inference*, cited at **chapter level**. Code symbols are written
in `monospace`.

## 1. The joint pmf and the joint pdf

For two **discrete** random variables the **joint probability mass function** is
[PSU L17]
$$f(x,y)=P(X=x\ \text{and}\ Y=y),\qquad f(x,y)\ge 0,\qquad
\sum_{x}\sum_{y}f(x,y)=1 .$$
We store it as a matrix `P` with `P[i,j]` $=f(x_i,y_j)$ — rows index $X$, columns
index $Y$. Validity (nonnegativity and total mass one) is `joint_pmf_is_valid(P)`.
The probability of any event $A\subseteq\{(x,y)\}$ is the sum of $f$ over the cells
in $A$.

For two **continuous** random variables the **joint probability density function**
$f(x,y)$ assigns probability by *volume under the surface* [PSU L20]:
$$f(x,y)\ge 0,\qquad \iint_{\mathbb R^2} f(x,y)\,dx\,dy=1,\qquad
P\big((X,Y)\in A\big)=\iint_{A} f(x,y)\,dx\,dy .$$
Validity is `joint_pdf_is_valid(f, ax,bx,ay,by)`, which checks $f\ge0$ on a grid and
$\iint f=1$ via the midpoint rule `_integrate2d`. If only the *shape* of a density
is known, the **normalizing constant** is
$$c=\Big(\iint \text{shape}(x,y)\,dx\,dy\Big)^{-1}\quad\Rightarrow\quad
\int\!\!\int c\,\text{shape}=1,$$
computed by `normalize_joint_pdf`. (For `shape`$=xy$ on the unit square,
$\iint xy=\tfrac14$, so $c=4$: the density is $4xy$.)

**Running examples.** Discrete: $f(x,y)=\dfrac{x+y}{32}$ on $x\in\{1,2\}$,
$y\in\{1,2,3,4\}$ — the cell sums of $x+y$ total $32$, so $f$ is a valid pmf.
Continuous: $f=4xy$ and $f=x+y$ on the unit square $0<x<1,\,0<y<1$ (both integrate
to $1$). These four densities recur throughout.

## 2. Marginal distributions — summing/integrating a variable out

To recover the distribution of $X$ **alone**, collapse the other variable. The
**marginal pmf / pdf** of $X$ is [PSU L17, L20]
$$\underbrace{f_X(x)=\sum_{y} f(x,y)}_{\text{discrete}}
\qquad\Longleftrightarrow\qquad
\underbrace{f_X(x)=\int_{-\infty}^{\infty} f(x,y)\,dy}_{\text{continuous}},$$
and symmetrically $f_Y(y)=\sum_x f(x,y)=\int f(x,y)\,dx$. The name is literal: in a
table you write the row/column totals in the **margins**. Code: `marginal_x(P)`
sums over columns (axis 1), `marginal_y(P)` over rows (axis 0); `marginal_pdf_x`
and `marginal_pdf_y` do the corresponding 1-D integrals with `_integrate`.

A marginal is itself a genuine one-variable distribution — it sums/integrates to
$1$ — so all of `~ST-05`/`~ST-10` applies to it. For the running examples:
$$f_X(x)=\tfrac{x+y\text{ summed}}{32}=\frac{14}{32},\frac{18}{32}\ \ (x=1,2);
\qquad f_Y(y)=\frac{3+2y}{32}\ \ (y=1,2,3,4),$$
and continuously $f=4xy\Rightarrow f_X(x)=\int_0^1 4xy\,dy=2x$, while
$f=x+y\Rightarrow f_X(x)=\int_0^1 (x+y)\,dy=x+\tfrac12$. Each integrates to $1$ over
$[0,1]$, as the tests confirm.

## 3. Independence: the joint *factors*

$X$ and $Y$ are **independent** when knowing one tells you nothing about the other.
For events this is $P(A\cap B)=P(A)P(B)$ (`~ST-03`); for random variables it becomes
the **factorization of the joint** [PSU L17, L20]:
$$\boxed{\,X\perp Y\quad\Longleftrightarrow\quad f(x,y)=f_X(x)\,f_Y(y)
\ \text{ for every }(x,y).\,}$$
It must hold *everywhere*; a single cell where $f(x,y)\ne f_X(x)f_Y(y)$ destroys
independence. Code: `independent_rv_check(P)` compares `P` to the **outer product**
$\texttt{np.outer}(f_X,f_Y)$; `independent_pdf_check` tests the factorization on a
grid of points.

- **Running discrete example is dependent.** $f(1,1)=\tfrac{2}{32}$ but
  $f_X(1)f_Y(1)=\tfrac{14}{32}\cdot\tfrac{5}{32}=\tfrac{70}{1024}\ne\tfrac{64}{1024}$.
  A joint pmf factors iff it can be written $g(x)h(y)$; $x+y$ cannot.
- **$f=4xy$ is independent:** $4xy=(2x)(2y)=f_X(x)f_Y(y)$. **$f=x+y$ is not:**
  $x+y\ne(x+\tfrac12)(y+\tfrac12)$ in general (they happen to agree at the centre
  $(\tfrac12,\tfrac12)$, which is why the check must sample several points).
- A handy generator: any **outer product** of two valid 1-D pmfs is automatically
  a valid, independent joint pmf — e.g. $\texttt{np.outer}([.4,.6],[.5,.5])$, which
  `independent_rv_check` returns `True` and whose marginals are $[.4,.6]$, $[.5,.5]$.

A useful **support test**: if the support of $f$ is not a rectangle
$\{x:f_X>0\}\times\{y:f_Y>0\}$ — e.g. the triangle $0<x<y<1$ — then $X,Y$ **cannot**
be independent, because the factored form has rectangular support.

## 4. Expectation of $g(X,Y)$ — the bivariate LOTUS

The **Law of the Unconscious Statistician** extends to two variables: to average a
function $g(X,Y)$ you weight $g$ by the joint and sum/integrate [PSU L17, L20]:
$$E[g(X,Y)]=\sum_{x}\sum_{y} g(x,y)\,f(x,y)
\qquad\Longleftrightarrow\qquad
E[g(X,Y)]=\iint g(x,y)\,f(x,y)\,dx\,dy .$$
Code: `expectation_joint(g, xv, yv, P)` and `expectation_joint_continuous(g, f, …)`.
Special cases recover everything one needs downstream:

- **Means / single-variable moments.** $g=x$ gives $E[X]$, and because
  $\sum_y f(x,y)=f_X(x)$ this equals the marginal mean $\sum_x x\,f_X(x)$ of
  `~ST-05` — joint LOTUS and the marginal agree (verified in the tests). For the
  running pmf $E[X]=\tfrac{50}{32}$, $E[Y]=\tfrac{90}{32}$, $E[XY]=\tfrac{140}{32}$.
- **Linearity, always.** With $g=x+y$,
  $$E[X+Y]=\sum_{x,y}(x+y)f(x,y)=\sum_{x,y}x\,f+\sum_{x,y}y\,f=E[X]+E[Y],$$
  which holds **whether or not** $X,Y$ are independent — no factorization used. The
  tests assert this in both columns.
- **Products and the independence multiplication rule.** With $g=xy$,
  $E[XY]=\sum_{x,y}xy\,f(x,y)$. **If $X\perp Y$** the joint factors and the double
  sum splits:
  $$E[XY]=\Big(\sum_x x f_X(x)\Big)\Big(\sum_y y f_Y(y)\Big)=E[X]\,E[Y].$$
  For the independent $f=4xy$: $E[X]=E[Y]=\tfrac23$ and $E[XY]=\tfrac49=E[X]E[Y]$
  (tests, $\texttt{tol}=10^{-3}$). The **gap** $E[XY]-E[X]E[Y]$ is the
  **covariance** — zero here, but $\approx-0.0195$ for the dependent pmf — which is
  the subject of `~ST-14`.

## 5. Joint and marginal cumulative distribution functions

The **joint cdf** accumulates probability over the quadrant below and to the left
of $(x,y)$ [PSU L17, L20]:
$$F(x,y)=P(X\le x,\,Y\le y)=\sum_{x_i\le x}\ \sum_{y_j\le y} f(x_i,y_j)
\quad\Longleftrightarrow\quad
F(x,y)=\int_{-\infty}^{x}\!\!\int_{-\infty}^{y} f(u,v)\,dv\,du .$$
Code: `joint_cdf(P, xv, yv, x, y)` and `joint_cdf_continuous(f, ax, ay, x, y)`. It
is **nondecreasing in each argument**, runs from $0$ (below all support) to $1$ (the
upper-right corner $F(+\infty,+\infty)=1$), and — the key consistency — gives back a
**marginal cdf** in the limit:
$$F_X(x)=F(x,+\infty)=P(X\le x),\qquad F_Y(y)=F(+\infty,y).$$
`marginal_cdf_x(P, xv, x)` computes $F_X$ as the cumulative sum of `marginal_x`, and
the tests check it equals `joint_cdf` evaluated at the largest $y$. In the
continuous case the density is recovered by differentiation,
$f(x,y)=\partial^2 F/\partial x\,\partial y$; e.g. $f=4xy$ has
$F(x,y)=x^2y^2$ on the unit square, so $F(\tfrac12,\tfrac12)=\tfrac1{16}=0.0625$ and
$F(1,1)=1$ (verified). For $f=x+y$, $F(\tfrac12,\tfrac12)=\tfrac18=0.125$.

## 6. Numerical integration of the continuous case

Because the continuous identities are integrals, the module ships a **midpoint
integrator** rather than relying on SciPy. `_integrate(f,a,b,n)` is the 1-D rule
$\int_a^b f\approx h\sum_{i} f\!\big(a+(i+\tfrac12)h\big)$, $h=(b-a)/n$; it powers
the marginals. `_integrate2d(f, ax,bx,ay,by)` is its tensor product on a meshgrid,
$$\iint f\,dx\,dy\;\approx\; h_x h_y\sum_{i}\sum_{j}
f\!\big(a_x+(i+\tfrac12)h_x,\ a_y+(j+\tfrac12)h_y\big),$$
used for normalization, LOTUS, and the joint cdf. The midpoint rule is **exact for
bilinear integrands** (products of linear factors), so $\iint 4xy$ and $\iint(x+y)$
come out exactly $1$; for the quadratic integrands of $E[X]$ and $E[XY]$ the
$n=400$ grid is accurate to $\sim10^{-4}$, comfortably inside the $10^{-3}$ test
tolerances. This is the same `_integrate` idiom as `~SM-06`.

## Where this goes

- `~ST-05` (a single discrete random variable) and `~ST-10`/`~ST-12` (continuous
  RVs) — *what each marginal is*; this module is their two-variable lift, and joint
  LOTUS reduces to the marginal mean when $g$ depends on one variable.
- `~ST-14` (covariance, correlation, **conditional** distributions) — the direct
  sequel: $\mathrm{Cov}(X,Y)=E[XY]-E[X]E[Y]$ is exactly the §4 gap, and conditional
  pmfs/pdfs are $f(x\mid y)=f(x,y)/f_Y(y)$ built from this module's joint and
  marginals.
- `~ST-15` (the bivariate normal) — the canonical continuous joint density, whose
  marginals and conditionals are all Gaussian.
- `~ST-06` (mgf) — the joint mgf $M(s,t)=E[e^{sX+tY}]$ **factors**,
  $M(s,t)=M_X(s)M_Y(t)$, iff $X\perp Y$: the §3 test in transform space; `~ST-16`
  (transformations of two RVs) uses independence + the convolution of marginals to
  get the distribution of $X+Y$.
- `~SM-01` (statistical-mechanical multiplicity) — independence of subsystems is
  the same product rule $\Omega_{12}=\Omega_1\Omega_2$ / $f=f_Xf_Y$ that turns
  multiplication of probabilities into addition of entropies.
