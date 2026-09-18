# ST-13 — Problems

Work each by hand, then check with `code/joint_distributions.py`. Citations in
`../refs.md`; **PSU L17** = STAT 414 Lesson 17 (two discrete RVs), **L20** =
Lesson 20 (two continuous RVs). Two running examples recur: the discrete table
$f(x,y)=\tfrac{x+y}{32}$ on $x\in\{1,2\},\,y\in\{1,2,3,4\}$, and the continuous
densities $f=4xy$ (independent) and $f=x+y$ (dependent) on the unit square.

In code: `xv, yv = [1,2], [1,2,3,4]` and
`P = np.array([[x+y for y in yv] for x in xv], float)/32`.

### P1.  A valid joint pmf and its marginals  *(PSU L17; `~ST-05`)*
Verify $f(x,y)=\tfrac{x+y}{32}$ is a valid joint pmf: $f\ge0$ and the $2\times4$
cell values $x+y$ sum to $32$. Then compute the marginals by summing out the other
variable, $f_X(x)=\sum_y f(x,y)$ and $f_Y(y)=\sum_x f(x,y)=\tfrac{3+2y}{32}$, and
confirm each is itself a one-variable pmf (sums to $1$).
*Check:* `joint_pmf_is_valid(P)` $=$ `True`; `marginal_x(P)` $=[0.4375,\,0.5625]$
$=[\tfrac{14}{32},\tfrac{18}{32}]$; `marginal_y(P)` $=[0.15625,0.21875,0.28125,0.34375]$
and `marginal_y(P).sum()` $=1.0$.

**Solution.** Nonnegativity is immediate: $x,y\ge1$, so $f=(x+y)/32>0$ on every
cell. For the total mass, sum the numerators $x+y$ over the $2\times4$ grid — row
$x{=}1$ gives $2{+}3{+}4{+}5=14$ and row $x{=}2$ gives $3{+}4{+}5{+}6=18$ — so
$$\sum_{x,y}f(x,y)=\frac{14+18}{32}=\frac{32}{32}=1,$$
a valid pmf. Summing out $y$ collapses each row to its total, $f_X(1)=\tfrac{14}{32}$,
$f_X(2)=\tfrac{18}{32}$; summing out $x$ gives
$f_Y(y)=\tfrac{(1+y)+(2+y)}{32}=\tfrac{3+2y}{32}$, i.e.
$\tfrac5{32},\tfrac7{32},\tfrac9{32},\tfrac{11}{32}$, totalling $\tfrac{32}{32}=1$ —
each marginal is itself a pmf. This is `marginal_x(P)` $=[0.4375,0.5625]$ and
`marginal_y(P)` $=[0.15625,0.21875,0.28125,0.34375]$ with `marginal_y(P).sum()` $=1.0$.

### P2.  Are they independent?  *(PSU L17)*
Test $f(x,y)=f_X(x)\,f_Y(y)$. Show it fails at $(1,1)$:
$f(1,1)=\tfrac{2}{32}=0.0625$ but $f_X(1)\,f_Y(1)=\tfrac{14}{32}\cdot\tfrac{5}{32}
=0.06836$. Conclude $X,Y$ are **dependent** (a sum $x+y$ never factors as
$g(x)h(y)$). Contrast with the **outer-product** table
$P_i=\big[\begin{smallmatrix}.2&.2\\.3&.3\end{smallmatrix}\big]
=\mathrm{outer}([.4,.6],[.5,.5])$, which *does* factor.
*Check:* `independent_rv_check(P)` $=$ `False`;
`independent_rv_check(np.outer([0.4,0.6],[0.5,0.5]))` $=$ `True`.

**Solution.** Factorization must hold at *every* cell, so a single failure settles
it. At $(1,1)$,
$$f(1,1)=\frac{2}{32}=0.0625,\qquad f_X(1)\,f_Y(1)=\frac{14}{32}\cdot\frac{5}{32}=\frac{70}{1024}=0.06836,$$
which differ, so $X,Y$ are **dependent**. The structural reason: a pmf factors iff it
can be written $g(x)h(y)$, and a *sum* $x+y$ admits no such split (only products
separate into a function of $x$ times a function of $y$). By contrast the
outer-product table is a product by construction, so it factors with marginals
$[.4,.6],[.5,.5]$. Hence `independent_rv_check(P)` $=$ `False` while
`independent_rv_check(np.outer([0.4,0.6],[0.5,0.5]))` $=$ `True`.

### P3.  Bivariate LOTUS: means, $E[XY]$, and linearity  *(PSU L17; `~ST-14`)*
Using $E[g(X,Y)]=\sum_{x,y}g(x,y)f(x,y)$, compute $E[X]=\tfrac{50}{32}$,
$E[Y]=\tfrac{90}{32}$, $E[XY]=\tfrac{140}{32}$. Verify **linearity**
$E[X+Y]=E[X]+E[Y]$ (it needs no independence), and that the gap
$E[XY]-E[X]E[Y]=-\tfrac{5}{256}$ is nonzero — the covariance of `~ST-14`.
*Check:* `expectation_joint(lambda x,y:x, xv,yv,P)` $=1.5625$;
`...:y...` $=2.8125$; `...:x*y...` $=4.375$;
`expectation_joint(lambda x,y:x+y,...)` $=4.375\stackrel{?}{=}1.5625+2.8125=4.375$;
$E[XY]-E[X]E[Y]=-0.01953$.

**Solution.** Bivariate LOTUS weights $g$ by the joint. With the P1 marginals,
$E[X]=\sum_x x f_X(x)=1\cdot\tfrac{14}{32}+2\cdot\tfrac{18}{32}=\tfrac{50}{32}$ and
$E[Y]=\sum_y y f_Y(y)=\tfrac{5+14+27+44}{32}=\tfrac{90}{32}$; the cross moment needs
the full table,
$$E[XY]=\frac1{32}\sum_{x,y}xy(x+y)=\frac{40+100}{32}=\frac{140}{32}=4.375.$$
Linearity uses no independence — splitting the sum,
$E[X+Y]=E[X]+E[Y]=\tfrac{50+90}{32}=\tfrac{140}{32}=4.375$ (numerically equal to
$E[XY]$ here, but by a different route). The *product* rule fails, though:
$E[XY]-E[X]E[Y]=4.375-\tfrac{50}{32}\cdot\tfrac{90}{32}=-\tfrac{5}{256}=-0.01953$, the
covariance of `~ST-14`. These match `expectation_joint` $=1.5625,2.8125,4.375$ and the
gap $-0.01953$.

### P4.  Joint and marginal cdfs  *(PSU L17)*
Compute $F(x,y)=\sum_{x_i\le x,\,y_j\le y}f(x_i,y_j)$. Show
$F(1,2)=f(1,1)+f(1,2)=\tfrac{5}{32}$, the corner $F(2,4)=1$, and that pushing
$y\to\max$ recovers the **marginal cdf** $F_X(1)=F(1,4)=f_X(1)=\tfrac{14}{32}$.
Argue $F$ is nondecreasing in each argument.
*Check:* `joint_cdf(P,xv,yv,1,2)` $=0.15625$; `joint_cdf(P,xv,yv,2,4)` $=1.0$;
`joint_cdf(P,xv,yv,1,4)` $=$ `marginal_cdf_x(P,xv,1)` $=0.4375$.

**Solution.** The joint cdf accumulates all mass in the lower-left quadrant of
$(x,y)$. At $(1,2)$ only cells $(1,1),(1,2)$ qualify,
$$F(1,2)=f(1,1)+f(1,2)=\frac{2}{32}+\frac{3}{32}=\frac{5}{32}=0.15625,$$
and at the top-right corner every cell is included, so $F(2,4)=\sum_{x,y}f=1$. Pushing
$y$ to its maximum keeps only the $X\le x$ restriction, recovering the marginal cdf:
$F(1,4)=\sum_y f(1,y)=f_X(1)=\tfrac{14}{32}=0.4375$. Since each added cell contributes
$f\ge0$, $F$ only rises as $x$ or $y$ grows — nondecreasing in each argument. These
reproduce `joint_cdf(P,xv,yv,1,2)` $=0.15625$, `joint_cdf(P,xv,yv,2,4)` $=1.0$, and
`joint_cdf(P,xv,yv,1,4)` $=$ `marginal_cdf_x(P,xv,1)` $=0.4375$.

### P5.  Normalizing a continuous joint density  *(PSU L20)*
A density has the *shape* $f\propto xy$ on the unit square. Find the constant $c$
with $\iint c\,xy\,dx\,dy=1$: since $\iint_0^1 xy\,dx\,dy=\tfrac14$, $c=4$, so
$f=4xy$. Confirm it is a valid pdf ($f\ge0$, integral $1$).
*Check:* `normalize_joint_pdf(lambda x,y:x*y, 0,1,0,1)` $\approx4.0$;
`joint_pdf_is_valid(lambda x,y:4*x*y, 0,1,0,1)` $=$ `True`.

**Solution.** The shape $xy$ separates over the unit square, so
$$\iint_0^1 xy\,dx\,dy=\Big(\int_0^1 x\,dx\Big)\Big(\int_0^1 y\,dy\Big)=\frac12\cdot\frac12=\frac14.$$
A density must integrate to $1$, which forces $c=\big(\tfrac14\big)^{-1}=4$ and
$f(x,y)=4xy$. It is nonnegative on the square and $\iint 4xy=4\cdot\tfrac14=1$, so it is
a valid pdf. Numerically `normalize_joint_pdf(lambda x,y:x*y, 0,1,0,1)` $\approx4.0$ and
`joint_pdf_is_valid(lambda x,y:4*x*y, 0,1,0,1)` $=$ `True`.

### P6.  Continuous marginals and independence  *(PSU L20)*
For $f=4xy$ integrate out $y$: $f_X(x)=\int_0^1 4xy\,dy=2x$, similarly $f_Y(y)=2y$,
and note $4xy=(2x)(2y)$ — **independent**. For $f=x+y$:
$f_X(x)=\int_0^1(x+y)\,dy=x+\tfrac12$, which gives $f_X(x)f_Y(y)=(x+\tfrac12)(y+\tfrac12)
\ne x+y$ — **dependent** (they coincide only at the centre, so the check must
sample several points).
*Check:* `marginal_pdf_x(lambda x,y:4*x*y, 0.5, 0,1)` $=1.0$ $(=2\cdot0.5)$;
`marginal_pdf_x(lambda x,y:x+y, 0.3, 0,1)` $=0.8$ $(=0.3+\tfrac12)$;
`independent_pdf_check(...4*x*y...)` $=$ `True`, `independent_pdf_check(...x+y...)` $=$ `False`.

**Solution.** Integrate the other variable out. For $f=4xy$,
$$f_X(x)=\int_0^1 4xy\,dy=4x\cdot\tfrac12=2x,\qquad f_Y(y)=2y,$$
and since $(2x)(2y)=4xy=f$, the joint factors — $X\perp Y$. For $f=x+y$,
$f_X(x)=\int_0^1(x+y)\,dy=x+\tfrac12$ and $f_Y(y)=y+\tfrac12$, whose product
$(x+\tfrac12)(y+\tfrac12)=xy+\tfrac{x+y}{2}+\tfrac14$ is **not** $x+y$ (they coincide
only where $xy+\tfrac14=\tfrac{x+y}2$, e.g. the centre), so $X,Y$ are **dependent**.
Hence `marginal_pdf_x(...4*x*y..., 0.5)` $=1.0=2(0.5)$,
`marginal_pdf_x(...x+y..., 0.3)` $=0.8=0.3+\tfrac12$, and `independent_pdf_check` returns
`True` for $4xy$ and `False` for $x+y$.

### P7.  Continuous LOTUS, the product rule, and the joint cdf  *(PSU L20; `~ST-14`)*
For $f=x+y$ compute $E[X]=\iint x(x+y)\,dx\,dy=\tfrac{7}{12}$ and
$E[XY]=\iint xy(x+y)=\tfrac13$. For the **independent** $f=4xy$ show the product
rule $E[XY]=E[X]E[Y]=\tfrac23\cdot\tfrac23=\tfrac49$. Finally get the joint cdf of
$f=4xy$, $F(x,y)=\iint_0^{x,y}4uv=x^2y^2$, so $F(\tfrac12,\tfrac12)=\tfrac1{16}$ and
$F(1,1)=1$.
*Check:* `expectation_joint_continuous(lambda x,y:x, lambda x,y:x+y, 0,1,0,1)`
$\approx0.5833\,(=\tfrac{7}{12})$; `...x*y...` $\approx0.3333\,(=\tfrac13)$; for
$4xy$ `expectation_joint_continuous(lambda x,y:x*y,...)` $\approx0.4444=\tfrac49$;
`joint_cdf_continuous(lambda x,y:4*x*y, 0,0, 0.5,0.5)` $\approx0.0625$,
`...,1,1)` $\approx1.0$.

**Solution.** For $f=x+y$, continuous LOTUS gives
$$E[X]=\iint_0^1 x(x+y)\,dx\,dy=\int_0^1 x^2dx+\Big(\int_0^1 x\,dx\Big)\Big(\int_0^1 y\,dy\Big)=\tfrac13+\tfrac14=\tfrac7{12},$$
and $E[XY]=\iint xy(x+y)=(\tfrac13)(\tfrac12)+(\tfrac12)(\tfrac13)=\tfrac13$. For the
**independent** $f=4xy$ the integrals separate,
$E[X]=E[Y]=4\cdot\tfrac13\cdot\tfrac12=\tfrac23$ and
$E[XY]=4(\tfrac13)(\tfrac13)=\tfrac49=E[X]E[Y]$ — the product rule, here exact. Its cdf
is the running integral $F(x,y)=\int_0^x\!\int_0^y 4uv\,dv\,du=x^2y^2$, so
$F(\tfrac12,\tfrac12)=\tfrac1{16}$ and $F(1,1)=1$. These match
`expectation_joint_continuous` $\approx0.5833,0.3333,0.4444$ and `joint_cdf_continuous`
$\approx0.0625,1.0$.

### P8.  Non-rectangular support forces dependence  *(PSU L20)*
Let $f(x,y)=2$ on the triangle $0<x<y<1$ (area $\tfrac12$, so it integrates to $1$).
Because the support is **not a rectangle**, $X,Y$ **cannot** be independent. Verify
by marginalizing: $f_X(x)=\int_x^1 2\,dy=2(1-x)$ and $f_Y(y)=\int_0^y 2\,dx=2y$,
whose product $4y(1-x)\ne2$. (The diagonal makes the 2-D midpoint integral of the
indicator slightly inexact, but the marginals — 1-D integrals at fixed $x$ or $y$ —
are clean.)
*Check:* with `f = lambda x,y: 2.0*(np.asarray(x) < np.asarray(y))`,
`marginal_pdf_x(f, 0.25, 0,1)` $=1.5=2(1-0.25)$;
`marginal_pdf_y(f, 0.6, 0,1)` $=1.2=2\cdot0.6$;
`independent_pdf_check(f, 0,1,0,1)` $=$ `False`.

**Solution.** The mass $f=2$ sits on the triangle $0<x<y<1$ of area $\tfrac12$, so
$\iint f=2\cdot\tfrac12=1$. Independence would require a *rectangular* support (the
factored form $f_Xf_Y$ is positive on a product set), but the constraint $x<y$ couples
the variables, so they cannot be independent. The marginals confirm it:
$$f_X(x)=\int_x^1 2\,dy=2(1-x),\qquad f_Y(y)=\int_0^y 2\,dx=2y,$$
whose product $4y(1-x)$ is not the constant $2$. Hence
`marginal_pdf_x(f, 0.25, 0,1)` $=1.5=2(1-0.25)$,
`marginal_pdf_y(f, 0.6, 0,1)` $=1.2=2\cdot0.6$, and
`independent_pdf_check(f, 0,1,0,1)` $=$ `False`.
