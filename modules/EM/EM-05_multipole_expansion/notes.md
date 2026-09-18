# EM-05 — Multipole Expansion (notes)

The **multipole expansion** answers a practical question: what does the potential of a
complicated but *localized* charge cloud look like from far away? The answer is a tidy
series whose successive terms — monopole, dipole, quadrupole — fall off ever faster with
distance, so that one or two of them suffice in the far field. Everything is built on the
exact potential of `~EM-03` and checked against it as $r$ grows.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page numbers
are the *printed* book pages. As in `~EM-01`, a charge is a pair $(q,\mathbf r')$; **r'**
locates the source, $\mathbf r = r\,\hat{\mathbf r}$ the (distant) field point, and
$\alpha$ the angle between them, so the separation is $\eta=|\mathbf r-\mathbf r'|$ and
$k\equiv 1/4\pi\varepsilon_0$.

## 1. The expansion in powers of 1/r
Start from the exact potential of a set of charges (Gr §3.4.1, p.151),
$V(\mathbf r)=k\sum_a q_a/\eta_a$. Write the separation with the law of cosines,
$\eta=r\sqrt{1+(r'/r)^2-2(r'/r)\cos\alpha}$, and expand $1/\eta$ in powers of the small ratio
$r'/r$. The coefficients are exactly the **Legendre polynomials** `~MA-12`:
$$\frac{1}{\eta}=\frac1r\sum_{n=0}^{\infty}\Big(\frac{r'}{r}\Big)^{n}P_n(\cos\alpha),
\qquad P_0=1,\ P_1=\cos\alpha,\ P_2=\tfrac12(3\cos^2\alpha-1).$$
Inserting this gives the **multipole expansion** (Gr Eq. 3.95, §3.4.1, p.151):
$$V(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\sum_{n=0}^{\infty}\frac{1}{r^{\,n+1}}
\int (r')^{n}P_n(\cos\alpha)\,\rho(\mathbf r')\,d\tau' ,$$
or, for point charges,
$V=k\sum_n r^{-(n+1)}\sum_a q_a (r'_a)^{n}P_n(\cos\alpha_a)$. The $n$-th term carries
$1/r^{n+1}$: monopole $1/r$, dipole $1/r^2$, quadrupole $1/r^3$. Because each step costs
another factor $r'/r\lesssim\text{size}/r$, truncating after the $\ell$-th term leaves a
relative error of order $(\text{size}/r)^{\ell+1}$ — **adding one term cuts the error by
another power of $(\text{size}/r)$.** Code: `multipole_potential(charges, lmax)` evaluates
this sum through $n=\texttt{lmax}$ (with `_legendre` for $P_0,P_1,P_2$) and converges to
the exact `~EM-03` `potential_point_charges` as $r$ grows.

## 2. The monopole and dipole terms
The first two terms are the workhorses (Gr §3.4.2, p.154). The $n=0$ term is the
**monopole**:
$$V_{\text{mono}}=\frac{1}{4\pi\varepsilon_0}\frac{Q}{r},
\qquad Q=\int\rho\,d\tau'=\sum_a q_a ,$$
the potential of the total charge gathered at the origin (`monopole_moment`). When $Q\neq0$
it dominates and the cloud looks like a point charge — the `~EM-01` far-field limit. The
$n=1$ term is the **dipole**. Using $P_1(\cos\alpha)=\cos\alpha$ and
$r'\cos\alpha=\mathbf r'\cdot\hat{\mathbf r}$,
$$V_{\text{dip}}(\mathbf r)=\frac{1}{4\pi\varepsilon_0}\frac{1}{r^{2}}\int r'\cos\alpha\,
\rho\,d\tau'=\frac{1}{4\pi\varepsilon_0}\frac{\mathbf p\cdot\hat{\mathbf r}}{r^{2}},
\qquad
\mathbf p=\int\mathbf r'\,\rho(\mathbf r')\,d\tau'=\sum_a q_a\mathbf r'_a ,$$
the **dipole moment** **p** (Gr Eq. 3.98) and pure-dipole potential (Gr Eq. 3.99). Code:
`dipole_moment` builds **p**; `dipole_potential(p)` returns
$V_{\text{dip}}=k\,\mathbf p\cdot\hat{\mathbf r}/r^2$ (stored as $\mathbf p\cdot\mathbf r/r^3$).
For a neutral pair $\pm q$ separated by **d** (from $-q$ to $+q$), $\mathbf p=q\mathbf d$,
pointing from the negative to the positive charge.

## 3. Origin of coordinates
The moments depend on where you put the origin — but not all equally (Gr §3.4.3, p.157).
Shift every source by a constant **a**, $\mathbf r'\to\mathbf r'-\mathbf a$. The dipole
moment becomes
$$\mathbf p\to\sum_a q_a(\mathbf r'_a-\mathbf a)=\mathbf p-Q\,\mathbf a .$$
So **p is independent of the origin precisely when the total charge $Q=0$**; for a neutral
object the dipole moment is an intrinsic property. If $Q\neq0$ the monopole term dominates
anyway, and the (origin-dependent) **p** is merely the leading correction. The same logic
cascades upward: the *lowest non-vanishing* moment is always origin-independent, the higher
ones are not. Code: `test_dipole_moment_origin_independent_when_neutral` shifts a neutral
pair by $(0.3,0.2,0.5)$ and recovers the same **p**.

## 4. The field of a dipole
Differentiate $V_{\text{dip}}=k\,\mathbf p\cdot\hat{\mathbf r}/r^{2}$ to get the field
(Gr §3.4.4, p.158). With **p** $=p\,\hat{\mathbf z}$, so $V_{\text{dip}}=k\,p\cos\theta/r^2$,
the gradient $\mathbf E=-\nabla V$ gives (Gr Eq. 3.103)
$$\mathbf E_{\text{dip}}=\frac{p}{4\pi\varepsilon_0 r^{3}}
\big(2\cos\theta\,\hat{\mathbf r}+\sin\theta\,\hat{\boldsymbol\theta}\big),$$
or, coordinate-free (Gr Eq. 3.104),
$$\boxed{\;\mathbf E_{\text{dip}}=\frac{1}{4\pi\varepsilon_0 r^{3}}
\big[\,3(\mathbf p\cdot\hat{\mathbf r})\,\hat{\mathbf r}-\mathbf p\,\big].\;}$$
The field falls as $1/r^{3}$ with a fixed angular shape. On the **axis**
($\theta=0$, $\hat{\mathbf r}\parallel\mathbf p$) it is $\mathbf E=2k\,p/r^{3}$ along **p**;
on the **perpendicular bisector** ($\theta=90^\circ$, $\hat{\mathbf r}\perp\mathbf p$) it is
$\mathbf E=-k\,p/r^{3}$, antiparallel to **p** and half as strong — the **2 : 1
axis-to-bisector ratio**. Code: `dipole_field(p)` returns this `E(x,y,z)`;
`test_dipole_field_axis_and_bisector` checks both limits.

The bracket $[\,3(\mathbf p\cdot\hat{\mathbf r})\hat{\mathbf r}-\mathbf p\,]$ is a
**structural template, not a one-off**: the *magnetic* dipole field of `~EM-09` has the
identical form with $\mathbf p\to\mathbf m$ and $1/4\pi\varepsilon_0\to\mu_0/4\pi$, because
both far fields descend from the same $\hat{\mathbf r}/r^2$ angular structure
($\mathbf p\cdot\hat{\mathbf r}/r^2$ here, $\mathbf m\times\hat{\mathbf r}/r^2$ there). The
quadrupole term ($n=2$, `quadrupole_moment`) continues the pattern through the traceless
tensor $Q_{ij}=\sum_a q_a(3r_ir_j-r^2\delta_{ij})$, dominant only when **both** $Q$ and **p**
vanish — e.g. the linear $+q,-2q,+q$ array of `test_quadrupole_of_linear_quadrupole`, for
which $Q_{zz}=4qa^{2}$ and $Q_{xx}=Q_{yy}=-2qa^{2}$.

## Where this goes
- `~EM-09` repeats the entire construction for the vector potential **A**: the magnetic
  dipole $\mathbf A_{\text{dip}}=(\mu_0/4\pi)\,\mathbf m\times\hat{\mathbf r}/r^2$ and its
  field reuse this section's $3(\cdot)\hat{\mathbf r}-(\cdot)$ structure (Gr Eq. 5.85).
- `~EM-07` defines the macroscopic polarization **P** as dipole moment **per unit volume** —
  the dipole term, integrated over a dielectric.
- `~MA-12` supplies the Legendre $P_n$ (and, with the azimuthal angle, the spherical
  harmonics) that make the expansion exact term by term.
- Far away, every neutral cloud is a dipole — which is why the dipole field is the default
  building block for radiation `~EM-17` and for intermolecular forces.
