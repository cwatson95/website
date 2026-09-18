# EM-05 — Problems

Work by hand, then check with `code/multipole.py`. Citations in `../refs.md`;
**Gr** = Griffiths 4e (printed pages). A charge is a pair $(q,\mathbf r')$ and moments are
taken about the origin unless stated otherwise.

### P1.  The physical dipole — moment and far-field potential  *(Gr §3.4.2, p.154)*
Place $+q$ at $+\tfrac{a}{2}\hat{\mathbf z}$ and $-q$ at $-\tfrac{a}{2}\hat{\mathbf z}$.
Show the system is neutral ($Q=0$) and has dipole moment $\mathbf p=qa\,\hat{\mathbf z}$,
pointing from the $-$ charge to the $+$ charge. Hence show the far field reduces to
$$V_{\text{dip}}(r,\theta)=\frac{1}{4\pi\varepsilon_0}\frac{qa\cos\theta}{r^{2}},$$
and that this captures the exact two-charge potential once $r\gg a$. *Check:*
`monopole_moment` returns $0$ and `dipole_moment` returns $(0,0,qa)$; `dipole_potential(p)`
and `multipole_potential(dip, lmax=1)` both track `potential_point_charges` (~EM-03) to a
fraction of a percent at $r=100a$.

**Solution.** The two charges sum to $Q=q+(-q)=0$, so the cloud is neutral. The dipole
moment (Gr Eq. 3.98) is $\mathbf p=\sum_a q_a\mathbf r'_a=q(\tfrac a2\hat{\mathbf z})+(-q)(-\tfrac a2\hat{\mathbf z})=qa\,\hat{\mathbf z}$,
pointing from $-q$ to $+q$. With $Q=0$ the monopole term drops and the $n=1$ term leads;
using $P_1(\cos\alpha)=\cos\alpha$ and $\mathbf p\cdot\hat{\mathbf r}=qa\cos\theta$,
$$V_{\text{dip}}=\frac{1}{4\pi\varepsilon_0}\frac{\mathbf p\cdot\hat{\mathbf r}}{r^{2}}
=\frac{1}{4\pi\varepsilon_0}\frac{qa\cos\theta}{r^{2}}.$$
For $q=10^{-9},\,a=0.01$ this is $\mathbf p=(0,0,10^{-11})$ C·m. On the axis at $r=100a$ the
dipole term gives $V=8.9876\times10^{-2}$ V against the exact $8.9878\times10^{-2}$ V —
agreement to $2\times10^{-5}$, matching `monopole_moment`$=0$, `dipole_moment`$=(0,0,qa)$, and
`multipole_potential(dip,1)`$\approx$`potential_point_charges`.

### P2.  How many terms? — convergence of the truncated series  *(Gr §3.4.1, p.151)*
For the same dipole, argue that the monopole term ($n=0$) gives $V\approx0$ (neutral), so
the leading contribution is the $1/r^{2}$ dipole term. Show the truncation error after the
$\ell$-th term scales as $(a/r)^{\ell+1}$, and estimate how far out (in units of $a$) the
dipole approximation is good to $1\%$. *Check:* at $r=30a$, compare `multipole_potential(dip, 0)`
(monopole only) and `multipole_potential(dip, 1)` (+dipole) against `potential_point_charges`;
the dipole-order error is below $1\%$ and strictly smaller than the monopole-order error.

**Solution.** Since $Q=0$, the $n=0$ term is $V_{\text{mono}}=kQ/r=0$ — it captures none of
the potential, so its relative error is exactly $100\%$. Each added term costs another factor
$r'/r\lesssim a/r$, so truncating after the $\ell$-th term leaves a relative error
$\sim(a/r)^{\ell+1}$. For the dipole ($\ell=1$) that is $(a/r)^{2}$; setting $(a/r)^{2}\lesssim0.01$
gives $r\gtrsim10a$. At $r=30a$ the measured monopole error is $1.0$ and the dipole-order error
is $2.78\times10^{-4}$ ($0.028\%$) — strictly smaller and far under $1\%$. (The symmetric pair's
even moments vanish, so the leading omitted term is the octupole and the error falls as
$(a/2r)^{2}=2.78\times10^{-4}$ at $r=30a$, exactly the value `multipole_potential` prints.)

### P3.  Origin of coordinates — when is p intrinsic?  *(Gr §3.4.3, p.157)*
Translate every source by a constant **a**, $\mathbf r'\to\mathbf r'-\mathbf a$, and prove
$$\mathbf p\to\mathbf p-Q\,\mathbf a,$$
so **p** is independent of the origin exactly when $Q=0$. Verify it concretely on a neutral
pair, then take a *like-charge* pair $(+q,+q)$ and show its dipole moment **does** shift
when the origin moves. *Check:* `dipole_moment` is invariant under a translation for the
neutral pair but not for the like-charge pair; `monopole_moment` is the obstruction $Q$ in
$\mathbf p-Q\mathbf a$.

**Solution.** Under $\mathbf r'\to\mathbf r'-\mathbf a$,
$$\mathbf p\to\sum_a q_a(\mathbf r'_a-\mathbf a)=\sum_a q_a\mathbf r'_a-\Big(\sum_a q_a\Big)\mathbf a
=\mathbf p-Q\,\mathbf a.$$
The shift $-Q\mathbf a$ vanishes iff $Q=0$. For the neutral pair $Q=0$, and translating by
$\mathbf a=(0.3,0.2,0.5)$ leaves $\mathbf p=(0,0,10^{-11})$ unchanged. For the like pair
$(+q,+q)$, $Q=2q=2\times10^{-9}\neq0$, so $\mathbf p$ moves from $\mathbf 0$ to
$-Q\mathbf a=(-6\times10^{-10},-4\times10^{-10},-10^{-9})$. This is exactly what the code shows:
`dipole_moment` is invariant for the neutral pair but shifts by $-$`monopole_moment`$\cdot\mathbf a$
for the like pair.

### P4.  The dipole field and its 2 : 1 structure  *(Gr §3.4.4, p.158)*
From $\mathbf E_{\text{dip}}=\dfrac{1}{4\pi\varepsilon_0 r^{3}}\big[3(\mathbf p\cdot\hat{\mathbf r})\hat{\mathbf r}-\mathbf p\big]$
with $\mathbf p=p\,\hat{\mathbf z}$, show that on the **axis** ($\hat{\mathbf r}\parallel\mathbf p$)
the field is $\mathbf E=2kp/r^{3}$ along **p**, while on the **perpendicular bisector**
($\hat{\mathbf r}\perp\mathbf p$) it is $\mathbf E=-kp/r^{3}$, antiparallel and half as
strong — the 2 : 1 ratio, with $k=1/4\pi\varepsilon_0$. Where does **E** point purely
radially, and where purely transversely? *Check:* `dipole_field(p)` evaluated on the
$z$-axis returns $E_z=2kp/r^{3}$, and on the $x$-axis returns $E_z=-kp/r^{3}$.

**Solution.** Write $\mathbf p=p\,\hat{\mathbf z}$, so $\mathbf p\cdot\hat{\mathbf r}=p\cos\theta$.
On the **axis** $\hat{\mathbf r}=\hat{\mathbf z}$ ($\theta=0$):
$$\mathbf E=\frac{k}{r^{3}}\big[3p\,\hat{\mathbf z}-p\,\hat{\mathbf z}\big]=\frac{2kp}{r^{3}}\hat{\mathbf z},$$
purely radial and along $\mathbf p$. On the **perpendicular bisector** $\hat{\mathbf r}\perp\mathbf p$
($\theta=90^\circ$, $\mathbf p\cdot\hat{\mathbf r}=0$):
$\mathbf E=\dfrac{k}{r^{3}}[\,0-p\,\hat{\mathbf z}\,]=-\dfrac{kp}{r^{3}}\hat{\mathbf z}$, antiparallel and
half as strong — the $2:1$ ratio. With $p=10^{-11},\,r=0.1$, `dipole_field(p)` returns
$E_z=179.75=2kp/r^{3}$ on the $z$-axis and $E_z=-89.876=-kp/r^{3}$ on the $x$-axis. $\mathbf E$ is
purely radial on the axis ($\mathbf E\parallel\hat{\mathbf r}$) and purely transverse on the
bisector ($\mathbf E\perp\hat{\mathbf r}$).

### P5.  The linear quadrupole  *(Gr §3.4.1, p.151)*
Put $+q,\,-2q,\,+q$ at $z=+a,\,0,\,-a$. Show both the monopole ($Q=0$) and the dipole
($\mathbf p=0$) vanish, so the **quadrupole** is the leading term and the potential falls as
$1/r^{3}$. Compute the traceless tensor $Q_{ij}=\sum_a q_a(3r_ir_j-r^{2}\delta_{ij})$ and
show $Q_{zz}=4qa^{2}$ with $Q_{xx}=Q_{yy}=-2qa^{2}$ (traceless: $Q_{xx}=Q_{yy}=-\tfrac12 Q_{zz}$).
*Check:* `monopole_moment` and `dipole_moment` both return zero, while `quadrupole_moment`
gives $Q[2][2]=4qa^{2}$ and $Q[0][0]=-2qa^{2}$.

**Solution.** Monopole: $Q=q-2q+q=0$. Dipole: $\mathbf p=q(a\hat{\mathbf z})-2q(\mathbf 0)+q(-a\hat{\mathbf z})=\mathbf 0$.
Both vanish, so the $n=2$ quadrupole leads and $V\sim1/r^{3}$. The charges sit on the $z$-axis, so
$x_a=y_a=0$ and $r_a^{2}=z_a^{2}$. Then
$$Q_{zz}=\sum_a q_a(3z_a^{2}-z_a^{2})=2\sum_a q_a z_a^{2}=2\big[q\,a^{2}+0+q\,a^{2}\big]=4qa^{2},$$
while $Q_{xx}=Q_{yy}=\sum_a q_a(0-z_a^{2})=-2qa^{2}=-\tfrac12 Q_{zz}$ (traceless). With
$q=10^{-9},\,a=0.01$: $Q_{zz}=4\times10^{-13}$ and $Q_{xx}=Q_{yy}=-2\times10^{-13}$, matching
`monopole_moment`$=$`dipole_moment`$=0$ and `quadrupole_moment` $Q[2][2]=4qa^{2}$, $Q[0][0]=-2qa^{2}$.
