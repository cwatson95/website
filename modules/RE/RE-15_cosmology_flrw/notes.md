# RE-15 — Cosmology: the FLRW universe (notes)

Conventions: geometrized units $G = c = 1$; mostly-plus signature $(-,+,+,+)$;
comoving coordinates $x = (t, r, \theta, \phi)$ with $t$ cosmic (proper) time of a
comoving observer. Overdot is $d/dt$. The Einstein tensor and curvature are those
of **RE-11** (`curvature.einstein_tensor`), which this module imports.

## 1. The cosmological principle ⇒ the FLRW metric
The founding assumption of cosmology is that, on large scales, the universe is
**homogeneous** (the same at every point) and **isotropic** (the same in every
direction) about every point. This is not a small symmetry: it forces the spatial
slices to be **maximally symmetric** 3-spaces — exactly the constant-curvature
spaces of RE-11 §6, $R_{ijkl} = \tfrac{k}{a^2}(g_{ik}g_{jl}-g_{il}g_{jk})$ — of which
there are only three, labelled by a sign $k$:
$$ds^2 = -dt^2 + a(t)^2\!\left[\frac{dr^2}{1-k r^2} + r^2\big(d\theta^2 + \sin^2\theta\, d\phi^2\big)\right],$$
the **Friedmann–Lemaître–Robertson–Walker (FLRW)** metric (`flrw_metric`). Here
$k=+1$ is the closed 3-sphere $S^3$, $k=0$ flat $\mathbb{R}^3$, $k=-1$ the open
hyperbolic $H^3$; $a(t)$ is the **scale factor**, the single dynamical degree of
freedom that survives the symmetry. The whole problem of cosmology is to find one
function, $a(t)$. (Zee §VI.2; Dodelson Eq. 2.4 gives the flat case $g_{\mu\nu}=
\mathrm{diag}(-1,a^2,a^2,a^2)$.)

## 2. The scale factor, the Hubble rate, and redshift
Comoving coordinates are carried along by the expansion: a galaxy at fixed comoving
$r$ has physical distance $a(t)\,r$, growing with $a$. The fractional expansion rate
is the **Hubble rate**
$$H \equiv \frac{\dot a}{a}\qquad(\texttt{hubble}),$$
whose present value $H_0$ sets the size ($\sim 1/H_0$) and age ($\sim 1/H_0$) of the
universe. A wavelength comoving with the expansion is stretched by the same factor
as $a$, so light emitted at $a_{\rm emit}$ and observed at $a_{\rm obs}$ is redshifted:
$$1+z = \frac{a_{\rm obs}}{a_{\rm emit}}\qquad(\texttt{redshift}),$$
and with the standard normalisation $a_0=1$ today, $a_{\rm emit}=1/(1+z)$. This is a
**cosmological** redshift — the stretching of space itself — not a kinematic Doppler
shift, though it reduces to Hubble's law $cz\simeq H_0 d$ for small $z$. (Dodelson
§2.2.)

## 3. The Friedmann equations (FLRW into the Einstein equations)
Feed the FLRW metric into the Einstein equations $G_{\mu\nu}+\Lambda g_{\mu\nu} =
8\pi T_{\mu\nu}$ (RE-11/RE-13) with a perfect-fluid source $T^{\mu}{}_{\nu} =
\mathrm{diag}(-\rho,p,p,p)$. Isotropy leaves only two independent components. The
**time–time** component gives the **first Friedmann equation**
$$\boxed{\;\Big(\frac{\dot a}{a}\Big)^2 = \frac{8\pi}{3}\rho - \frac{k}{a^2} + \frac{\Lambda}{3}\;}\qquad(\texttt{friedmann\_1\_residual}),$$
a *constraint* (no $\ddot a$); the trace/space part gives the **second Friedmann
(acceleration) equation**
$$\boxed{\;\frac{\ddot a}{a} = -\frac{4\pi}{3}\big(\rho+3p\big) + \frac{\Lambda}{3}\;}\qquad(\texttt{friedmann\_2\_residual}).$$
The headline of this module makes the first one *literal*: for the FLRW metric the
Einstein tensor’s time–time component is
$$G_{00} = 3\!\left[\Big(\frac{\dot a}{a}\Big)^2 + \frac{k}{a^2}\right] = \frac{3(\dot a^2 + k)}{a^2},$$
so $G_{00}=8\pi T_{00}=8\pi\rho$ *is* the first Friedmann equation. `G00_from_flrw`
builds the metric, hands it to RE-11’s finite-difference `einstein_tensor`, and
recovers this — the coefficient $\boxed{+3}$ is confirmed numerically (de Sitter
$G_{00}\to 3H^2$; matter $G_{00}\to 3(\tfrac{2}{3t})^2$) to $\sim1\%$. Two sign
lessons: (i) pressure **gravitates** ($\rho+3p$, not $\rho$, sources deceleration),
so a radiation universe decelerates harder than a matter one; (ii) only $\rho+3p<0$
— a sufficiently negative pressure, or $\Lambda>0$ — can give $\ddot a>0$, cosmic
**acceleration**. (Dodelson §2.1.3, Eqs. 2.30, 2.38–2.39; Zee §VIII.1.)

## 4. Critical density, $\Omega$, and the flat/open/closed trichotomy
Solve the first Friedmann equation (with $\Lambda=0$) for the density that makes a
universe spatially **flat** ($k=0$):
$$\rho_c = \frac{3H^2}{8\pi}\qquad(\texttt{critical\_density}),$$
the **critical density**. Normalising the actual density to it defines the **density
parameter**
$$\Omega \equiv \frac{\rho}{\rho_c} = \frac{8\pi\rho}{3H^2}\qquad(\texttt{omega}).$$
Dividing Friedmann I by $H^2$ rewrites it as an exact identity among fractions,
$$1 = \Omega + \Omega_\Lambda + \Omega_k,\qquad \Omega_k \equiv -\frac{k}{a^2H^2},$$
so the **geometry is read straight off the total density**: with $\Lambda=0$,
$$\Omega_{\rm tot}>1 \iff k=+1\ (\text{closed, recollapses}),\quad
  \Omega_{\rm tot}=1 \iff k=0\ (\text{flat}),\quad
  \Omega_{\rm tot}<1 \iff k=-1\ (\text{open, expands forever}).$$
`test_omega_trichotomy_matches_curvature_sign` checks the sign of $\Omega-1$ equals
the sign of $k$ on-shell. (Dodelson Eq. 2.39–2.40 defines $\rho_{cr}=3H_0^2/8\pi G$.)

## 5. The three eras
A single perfect fluid with equation of state $p = w\rho$ has, in a flat universe,
$\rho\propto a^{-3(1+w)}$ (§6) and hence a **power-law** scale factor $a\propto
t^{2/(3(1+w))}$ from Friedmann I. The three epochs that built our universe:

| era | $w$ | $p$ | $\rho(a)$ | $a(t)$ |
|---|---|---|---|---|
| **radiation** | $1/3$ | $\rho/3$ | $a^{-4}$ | $t^{1/2}$ |
| **matter** (dust) | $0$ | $0$ | $a^{-3}$ | $t^{2/3}$ |
| **dark energy / $\Lambda$** | $-1$ | $-\rho$ | const $=\Lambda/8\pi$ | $e^{Ht}$ (de Sitter) |

Radiation dilutes fastest (one extra factor of $a$ from redshift on top of volume
$a^{-3}$), so the early universe is radiation-dominated; matter overtakes it, then a
constant $\Lambda$ inevitably wins at late times and the expansion turns
**exponential** ($H=\sqrt{\Lambda/3}$ constant, $\ddot a>0$). `test_three_eras…`
verifies each era satisfies **both** Friedmann residuals; $F_2=0$ is the nontrivial
check — it pins the exponent to exactly $2/(3(1+w))$.

## 6. Conservation: the fluid equation
The four Einstein equations are not independent: the contracted Bianchi identity
$\nabla_\mu G^{\mu\nu}=0$ (RE-11 §3) forces $\nabla_\mu T^{\mu\nu}=0$, whose $\nu=0$
component in FLRW is the **fluid (continuity) equation**
$$\boxed{\;\dot\rho = -3\frac{\dot a}{a}\,(\rho+p)\;}\qquad(\texttt{fluid\_equation\_residual}).$$
It is exactly $\dot E = -p\,dV$ for a comoving volume $V\propto a^3$: the energy in a
patch falls both because volume grows ($-3H\rho$) and because pressure does work as it
expands ($-3Hp$). For $p=w\rho$ it integrates to $\rho\propto a^{-3(1+w)}$, giving the
$\rho(a)$ scalings of §5 — matter $a^{-3}$ (rest mass conserved, just diluted),
radiation $a^{-4}$ (diluted *and* redshifted), $\Lambda$ constant (vacuum energy does
$-p\,dV$ work that exactly refills itself). Because it follows from the two Friedmann
equations, the fluid equation is a *consistency* relation — and a numerically exact
one here: `test_fluid_equation…` gives residual $0$ to machine precision for matter
and radiation. This closes the system: {Friedmann I, fluid equation, $p=w\rho$} ⇒
$a(t)$ and $\rho(t)$, the entire smooth history of the universe.
