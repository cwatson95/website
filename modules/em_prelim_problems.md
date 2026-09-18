# EM Prelim Notes — Transcribed Problems

Transcribed page-by-page from the scanned handwritten notebook `em_prelim_notes.pdf`
(115 pages, no text layer) on 2026-07-02. 56 entries in notebook order; the
*(pp. N–M)* citation on each heading gives the PDF page numbers.

**Conventions.** $\mathfrak{r}$ (Fraktur r) stands for the notebook's Griffiths
script-r separation vector, $\vec{\mathfrak{r}} = \vec{r}-\vec{r}\,'$, $\mathfrak{r}=|\vec{r}-\vec{r}\,'|$
(KaTeX has no lowercase script glyph). The notes' $\forall$-like symbol for volume is
kept as written. Bracketed italic lines describe the hand diagrams. *[sic: …]* marks
slips present in the notebook itself, transcribed as written. Entries tagged
*[reference notes, not a worked problem]* are formula/summary sheets, not worked problems.

**Duplicate scans in the PDF:** pp. 26/27 are the same sheet scanned twice, p. 29 is a
faint pencil duplicate of p. 30, and p. 112 duplicates p. 111 (different orientation).

### P1. E of Wire *(p. 1)*

Electric field at a point a height $z$ above the midpoint of a straight wire of length $2L$ (linear charge density $\lambda$) lying along $\hat{x}$; the Coulomb integral is set up and reduced to its vertical component.

**Solution.**

*[Diagram: field point at height $z$ above the midpoint of a wire of length $2L$ along $\hat{x}$; $\theta$ is the angle at the field point between the vertical and the separation vector $\mathfrak{r}$ to a source point on the wire. A small side triangle identifies the legs: $r \to z$ (vertical), $r' \to x$ (horizontal), hypotenuse $\mathfrak{r}$.]*

$$
\mathfrak{r} = \sqrt{z^2+x^2} \qquad \vec{\mathfrak{r}} = z\,\hat{z} - x\,\hat{x}
$$

$$
\vec{E} = \frac{1}{4\pi\epsilon_0}\int \frac{\rho(\vec{\mathfrak{r}})\,\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,d\tau
$$

$$
\rho\,d\tau \to \lambda\,dx'
$$

Horizontal components cancel.

$$
\vec{E} = \frac{1}{4\pi\epsilon_0}\int_{-L}^{L} \frac{\lambda\, z\,\hat{z}}{\left(z^2+x^2\right)^{3/2}}\,dx'
$$

*[The page ends here with the integral left unevaluated.]*

### P2. [Untitled — E on the Axis of a Charged Ring] *(p. 2)*

Electric field at a point a height $z$ above the center of a circular loop of radius $r$ carrying uniform line charge $\lambda$.

**Solution.**

*[Diagram: point P above the center of a circular loop; $z$ runs from P down to the center, $\mathfrak{r}$ slants from P to the rim, with angle $\theta$ between them at P.]*

$$
\vec{E} = \frac{1}{4\pi\epsilon_0}\int \frac{\lambda\,\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,dl'
$$

Horizontal components cancel so then

$$
\vec{E} = \frac{\lambda}{4\pi\epsilon_0}\int \frac{\cos\theta}{z^2+r^2}\,dl
$$

*[Side triangle: legs $z$ and $r$, hypotenuse $\mathfrak{r}$, giving $\cos\theta = \dfrac{z}{\mathfrak{r}}$.]*

$$
\int dl = C = 2\pi r
$$

$$
\vec{E} = \frac{\lambda}{4\pi\epsilon_0}\,\frac{2\pi r\, z}{\left(z^2+r^2\right)^{3/2}}\,\hat{z}
$$

### P3. B of Wire *(p. 3)*

Magnetic field at point P a height $z$ above the midpoint of a straight wire of length $2L$ along $\hat{x}$ carrying current $I$, by the Biot–Savart law.

**Solution.**

*[Diagram: wire from $-L$ to $L$ along $\hat{x}$ carrying current $I$; point P above the midpoint, with $\vec{r}$ vertical to P, $\vec{r}\,'$ along the wire, $\mathfrak{r}$ from source point to P, angle $\theta$ at P.]*

$$
\vec{B} = \frac{\mu_0 I}{4\pi}\int \frac{d\vec{l}\times\hat{\mathfrak{r}}}{\mathfrak{r}^2}
$$

$$
\vec{r} = z\,\hat{z} \qquad \vec{r}\,' = x'\,\hat{x} \qquad \vec{\mathfrak{r}} = \vec{r}-\vec{r}\,' = z\,\hat{z}-x'\,\hat{x}
$$

$$
d\vec{l} = dx'\,\hat{x} \qquad \hat{\mathfrak{r}} = \frac{\vec{\mathfrak{r}}}{\mathfrak{r}} \qquad \mathfrak{r}^2 = x^2+z^2
$$

$$
d\vec{l}\times\vec{\mathfrak{r}} = \left(dx'\,\hat{x}\right)\times\left(z\,\hat{z}-x'\,\hat{x}\right)
$$

Horizontal components cancel; $\hat{x}\times\hat{x} = 0$

$$
d\vec{l}\times\vec{\mathfrak{r}} = z\,dx'\left(\hat{x}\times\hat{z}\right) = z\,dx'\left(-\hat{y}\right)
$$

$$
\vec{B} = -\frac{\mu_0 I}{4\pi}\int_{-L}^{L}\frac{z\,dx'}{\left(x^2+z^2\right)^{3/2}}\;\hat{y}
$$

### P4. B of Square Loop *(p. 4)*

Magnetic field at a point a height $z$ above the center of a square loop of side $2L$ carrying current $I$, assembled from the finite-wire result of the previous page.

**Solution.**

*[Diagrams: (i) square loop of side $2L$ with apex point P above its center — $s$ runs from P to the midpoint of one side, $\mathfrak{r}$ from P to a point on that side; (ii) triangle with vertical $s$, horizontal $x$, hypotenuse $\mathfrak{r}$, angle $\theta$; (iii) triangle with vertical $z$, horizontal $L$, hypotenuse $s$, angle $\psi$. A corner sketch is scribbled out.]*

$$
\mathfrak{r}^2 = s^2+x^2 \qquad \cos\theta = \frac{s}{\mathfrak{r}} \qquad \sin\psi = \frac{L}{s}
$$

$$
\left|\vec{B}_{\text{side}}\right| = -\frac{\mu_0 I}{4\pi}\int_{-L}^{L}\frac{z\,dx'}{\left(x^2+z^2\right)^{3/2}}\;\hat{y}
$$

where for this problem $z \to s$ and all horizontal components cancel. For all four sides multiply by $4\sin\psi$ so then

$$
\vec{B}_{\text{tot}} = -\frac{\mu_0 I}{\pi}\int_{-L}^{L}\frac{s\,dx'}{\left(x^2+s^2\right)^{3/2}}\,\frac{L}{s}\;\hat{z}
$$

$$
\vec{B}_{\text{tot}} = -\frac{\mu_0 I L}{\pi}\int_{-L}^{L}\frac{dx'}{\left(x^2+s^2\right)^{3/2}}\;\hat{z}
$$

### P5. Charge Conservation *(p. 5)*

Derives the continuity equation by taking the divergence of the Ampère–Maxwell law.

**Solution.**

$$
\nabla\times\vec{B} = \mu_0\vec{J} + \mu_0\epsilon_0\frac{\partial\vec{E}}{\partial t}
$$

$$
\underbrace{\nabla\cdot\left(\nabla\times\vec{B}\right)}_{\text{zero}} = \mu_0\left(\nabla\cdot\vec{J}\right) + \mu_0\epsilon_0\frac{\partial}{\partial t}\left(\nabla\cdot\vec{E}\right)
$$

$$
0 = \left(\nabla\cdot\vec{J}\right)\mu_0 + \mu_0\epsilon_0\frac{\partial}{\partial t}\left(\nabla\cdot\vec{E}\right)
$$

$$
\nabla\cdot\vec{J} = -\epsilon_0\frac{\partial}{\partial t}\left(\frac{\rho}{\epsilon_0}\right)
$$

$$
\nabla\cdot\vec{J} = -\frac{\partial\rho}{\partial t}
$$

*[The last line is boxed.]*

### P6. Poynting Theorem *(pp. 6–7)*

Derives Poynting's theorem — the energy balance $dW/dt$ for the electromagnetic field — starting from the work done by the Lorentz force on a charge distribution, and the local statement $\partial u/\partial t = -\nabla\cdot\vec{S}$ when no work is done.

**Solution.**

$$
\vec{F}\cdot d\vec{l} = q\left(\vec{E}+\vec{v}\times\vec{B}\right)\cdot\vec{v}\,dt = q\vec{E}\cdot\vec{v}\,dt
$$

where $q \to \rho\,d\tau$

$$
\vec{F}\cdot d\vec{l} = q\vec{E}\cdot\vec{v}\,dt \;\to\; \vec{E}\cdot\rho\vec{v}\,dt\,d\tau
$$

where $\rho\vec{v} \to \vec{J}$

$$
\vec{F}\cdot d\vec{l} = \vec{E}\cdot\vec{J}\,d\tau\,dt
$$

where $dW = \vec{F}\cdot d\vec{l}$, so

$$
\frac{dW}{dt} = \int_V \left(\vec{E}\cdot\vec{J}\right)d\tau
$$

$$
\vec{E}\cdot\vec{J} = \frac{1}{\mu_0}\,\vec{E}\cdot\left(\nabla\times\vec{B}\right) - \epsilon_0\,\vec{E}\cdot\frac{\partial\vec{E}}{\partial t}
$$

prod. rule 6 *[margin note: "pg 23 Camb 2.53"]*

$$
\nabla\cdot\left(\vec{E}\times\vec{B}\right) = \vec{B}\cdot\left(\nabla\times\vec{E}\right) - \vec{E}\cdot\left(\nabla\times\vec{B}\right)
$$

Faraday's law

$$
\nabla\times\vec{E} = -\frac{\partial\vec{B}}{\partial t}
$$

$$
\vec{E}\cdot\left(\nabla\times\vec{B}\right) = -\vec{B}\cdot\frac{\partial\vec{B}}{\partial t} - \nabla\cdot\left(\vec{E}\times\vec{B}\right)
$$

where

$$
\vec{B}\cdot\frac{\partial\vec{B}}{\partial t} = \frac{1}{2}\frac{\partial}{\partial t}\left(B^2\right) \qquad \vec{E}\cdot\frac{\partial\vec{E}}{\partial t} = \frac{1}{2}\frac{\partial}{\partial t}\left(E^2\right)
$$

so

$$
\vec{E}\cdot\vec{J} = -\frac{1}{2}\frac{\partial}{\partial t}\left(\epsilon_0 E^2 + \frac{1}{\mu_0}B^2\right) - \frac{1}{\mu_0}\nabla\cdot\left(\vec{E}\times\vec{B}\right)
$$

$$
\frac{dW}{dt} = -\frac{d}{dt}\int_V \frac{1}{2}\left(\epsilon_0 E^2 + \frac{1}{\mu_0}B^2\right)d\tau - \frac{1}{\mu_0}\oint_{SA}\left(\vec{E}\times\vec{B}\right)\cdot d\vec{a}
$$

*[The line above is boxed.]*

$$
\vec{S} \equiv \frac{1}{\mu_0}\left(\vec{E}\times\vec{B}\right)
$$

$$
\frac{dW}{dt} = -\frac{d}{dt}\int_V u\,d\tau - \oint_S \vec{S}\cdot d\vec{a}
$$

*[The line above is boxed.]*

if no work is done

$$
\int \frac{\partial u}{\partial t}\,d\tau = -\oint \vec{S}\cdot d\vec{a} = -\int\left(\nabla\cdot\vec{S}\right)d\tau
$$

$$
\frac{\partial u}{\partial t} = -\nabla\cdot\vec{S}
$$

### P7. [Untitled — Line Charge above a Grounded Plane (Method of Images)] *(pp. 8–9)*

An infinite line charge $\lambda$ at height $z_0$ above the grounded plane $z=0$ ($V=0$): the field of a wire from Gauss's law, its logarithmic potential, and the total potential above the plane by the method of images.

**Solution.**

*[Diagram: $\hat{z}$ axis vertical; a line charge $\lambda$ drawn horizontally through the axis at height $z_0$; below it the $x$–$y$ plane marked $V=0$, with axes $\hat{y}$ (right) and $\hat{x}$ (toward viewer).]*

$$
\oint\vec{E}\cdot d\vec{a} = \frac{Q_{\text{enc}}}{\epsilon_0} \;\to\; E\left(2\pi R L\right) = \frac{\lambda L}{\epsilon_0}
$$

$$
\vec{E} = \frac{\lambda}{2\pi\epsilon_0 R}
$$

$$
V = -\int\vec{E}\cdot d\vec{l} = -\int_a^{s} \frac{\lambda}{2\pi\epsilon_0\, r}\,dr
$$

$$
V = -\frac{\lambda}{2\pi\epsilon_0}\left(\ln(s)-\ln(a)\right) = \frac{\lambda}{2\pi\epsilon_0}\ln\left(\frac{a}{s}\right)
$$

using method of images

$$
V = \frac{\lambda}{2\pi\epsilon_0}\ln\left(\frac{a}{\mathfrak{r}}\right)
$$

so

$$
V_1 = \frac{\lambda}{2\pi\epsilon_0}\,\ln\left[\frac{a}{\left(x^2+y^2+\left(z-z_0\right)^2\right)^{1/2}}\right]
$$

*[sic: for an infinite line the distance should involve only the coordinates transverse to the wire; the notes fold in the full $x^2+y^2$, defining $s^2 = x^2+y^2$ below.]*

$$
V_2 = \frac{\lambda'}{2\pi\epsilon_0}\,\ln\left[\frac{a}{\left(x^2+y^2+\left(z+z_0\right)^2\right)^{1/2}}\right]
$$

$$
V_{\text{tot}} = \frac{\lambda}{2\pi\epsilon_0}\left\{\ln\left[\frac{a}{\left(s^2+\left(z-z_0\right)^2\right)^{1/2}}\right] - \ln\left[\frac{a}{\left(s^2+\left(z+z_0\right)^2\right)^{1/2}}\right]\right\} \qquad \left(s^2 = x^2+y^2\right)
$$

@ $V=0$

$$
\therefore\; V_{\text{tot}} = \frac{\lambda}{4\pi\epsilon_0}\,\ln\left[\frac{s^2+\left(z-z_0\right)^2}{s^2+\left(z+z_0\right)^2}\right]
$$

*[The line above is boxed. sic: the ratio is inverted relative to the preceding line, which combines to $\ln\!\big[(s^2+(z+z_0)^2)/(s^2+(z-z_0)^2)\big]$.]*

### P8. B of Loop & Rotating Spherical Shell *(p. 10)*

On-axis magnetic field of a circular current loop of radius $R$ by Biot–Savart, then — treating a rotating charged spherical shell (radius $R$, surface density $\sigma$, angular velocity $\omega$) as a stack of loops — the field at its center.

**Solution.**

*[Diagram: point P at the apex, dashed height $z$ down to the center of a circle of radius $R$, slant $\mathfrak{r}$ from P to the rim.]*

$$
\vec{B} = \frac{\mu_0}{4\pi}\int\frac{d\vec{I}\times\hat{\mathfrak{r}}}{\mathfrak{r}^2} \qquad \vec{\mathfrak{r}} = z\,\hat{z}-R\,\hat{r} \qquad \mathfrak{r}^2 = R^2+z^2
$$

$$
dl\times\vec{\mathfrak{r}} = R\,d\phi\,\hat{\phi}\times\left(z\,\hat{z}-R\,\hat{r}\right)
$$

due to symmetry $\hat{\phi}\times\hat{z} = \hat{r}$, $\hat{\phi}\times\left(-\hat{r}\right) = \hat{z}$; $\hat{r}$, $\hat{\phi}$ components cancel, leaving

$$
d\vec{l}\times\vec{\mathfrak{r}} = R^2\,d\phi\,\hat{z} \qquad \frac{\hat{\mathfrak{r}}}{\mathfrak{r}^2} = \frac{\vec{\mathfrak{r}}}{\mathfrak{r}^3} \qquad d\vec{I} = I\,d\vec{l}
$$

$$
\vec{B} = \frac{\mu_0 I}{4\pi}\int\frac{R^2\,d\phi}{\left(R^2+z^2\right)^{3/2}}\;\hat{z} \qquad \text{let } R \equiv R'
$$

for 3D shell $\to$ $\vec{K} = \sigma\vec{v}$ where $\vec{v} = R'\omega$

$$
R' \to R\sin\theta \qquad z \to R\cos\theta \qquad \&\quad I \equiv R'\sigma\omega
$$

$$
I \to \sigma R\sin\theta\,\omega \qquad d\vec{l} = R\,d\theta \qquad d\vec{I} = \sigma R^2\sin\theta\,\omega\,d\theta
$$

$$
\vec{B} = \frac{\mu_0}{2}\int\frac{R^2\sin^2\theta\;dI}{\left(R^2\left(\sin^2\theta+\cos^2\theta\right)\right)^{3/2}}\;\hat{z} = \frac{\mu_0 R\sigma\omega}{2}\int\sin^3\theta\,d\theta\;\hat{z}
$$

*[The page ends here with the $\sin^3\theta$ integral unevaluated.]*

### P9. B outside Spinning Solid Sphere *(pp. 11–14)*

A uniformly charged solid sphere (radius $R$, total charge $Q$, density $\rho$) spins at angular velocity $\omega$: the vector potential is built by superposing spinning-shell dipole contributions split at the field radius $r$, and then $\vec{B} = \nabla\times\vec{A}$ is evaluated in spherical coordinates.

**Solution.**

$$
\vec{A}_{\text{dip}} \approx \frac{\mu_0}{4\pi r^2}\left(\vec{m}\times\hat{r}\right) \qquad \sigma \equiv \rho\,dr' \qquad V = \frac{4}{3}\pi R^3 \qquad \rho = \frac{Q}{V}
$$

$$
\vec{K} = \sigma\vec{v} = \sigma\omega r'\,\hat{z} \;\to\; d\vec{J} = \rho\omega r'\,dr'\,\hat{z}
$$

*[sic: $\vec{K}$ and $d\vec{J}$ circulate along $\hat{\phi}$; the $\hat{z}$ written here is the axis that reappears in $d\vec{m}\parallel\hat{z}$.]*

$$
d\vec{m} = V\,d\vec{J} = \frac{4}{3}\pi R^3 \rho\omega r'\,dr'\,\hat{z}
$$

$$
\hat{z}\times\hat{r} = \hat{\phi}
$$

however for spherical

$$
d\phi\,\hat{\phi} \to \sin\theta\,d\phi\,\hat{\phi}
$$

$$
\vec{A} \approx \frac{\mu_0}{4\pi r^2}\int \frac{4}{3}\pi R^3\rho\omega r'\,dr'\,\sin\theta\;\hat{\phi}
$$

$$
\vec{A} \approx \frac{\mu_0\rho\omega\sin\theta}{3}\int\frac{R^3\, r'\,dr'}{r^2}\;\hat{\phi}
$$

$$
\vec{A} = \frac{\mu_0\rho\omega\sin\theta}{3}\int_0^{r}\frac{R_<^3\, r'\,dr'}{r^2}\;\hat{\phi} \;+\; \frac{\mu_0\rho\omega\sin\theta}{3}\int_r^{R}\frac{R_>^3\, r'\,dr'}{r^2}\;\hat{\phi} \qquad \left(\text{let } R_< \equiv r',\; R_> \equiv r\right)
$$

$$
\vec{A} = \frac{\mu_0\rho\omega\sin\theta}{3}\left[\int_0^{r}\frac{r'^4}{r^2}\,dr' + \int_r^{R} r\,r'\,dr'\right]\hat{\phi}
$$

$$
\to \frac{\mu_0\rho\omega\sin\theta}{3}\left[\frac{r^5}{5r^2} + \frac{r}{2}\left(R^2-r^2\right)\right]\hat{\phi}
$$

$$
\to \frac{\mu_0\rho\omega\sin\theta}{3}\left[\frac{r^3}{5} + \frac{R^2 r}{2} - \frac{r^3}{2}\right]\hat{\phi}
$$

$$
\to \frac{\mu_0\rho\omega r\sin\theta}{3}\left[\frac{r^2}{5} - \frac{r^2}{2} + \frac{R^2}{2}\right]\hat{\phi}
$$

$$
\to \frac{\mu_0\rho\omega r\sin\theta}{2}\left[\frac{R^2}{3} - \frac{r^2}{5}\right]\hat{\phi}
$$

$$
\vec{A} = \frac{\mu_0\rho\omega r\sin\theta}{2}\left[\frac{R^2}{3} - \frac{r^2}{5}\right]\hat{\phi}
$$

*[The line above is boxed.]*

$$
\vec{B} = \nabla\times\vec{A} = \begin{vmatrix} \dfrac{\hat{r}}{r^2\sin\theta} & \dfrac{\hat{\theta}}{r\sin\theta} & \dfrac{\hat{\phi}}{r} \\ \partial_r & \partial_\theta & \partial_\phi \\ 0 & 0 & rA_\phi\sin\theta \end{vmatrix}
$$

$$
\vec{B} = \frac{\hat{r}}{r^2\sin\theta}\,\partial_\theta\left(rA_\phi\sin\theta\right) - \frac{\hat{\theta}}{r\sin\theta}\,\partial_r\left(rA_\phi\sin\theta\right)
$$

$$
= \frac{1}{r^2\sin\theta}\,\partial_\theta\left[\frac{\mu_0\rho\omega r^2\sin^2\theta}{2}\left(\frac{R^2}{3}-\frac{r^2}{5}\right)\right]\hat{r} - \frac{1}{r\sin\theta}\,\partial_r\left[\frac{\mu_0\rho\omega r^2\sin^2\theta}{2}\left(\frac{R^2}{3}-\frac{r^2}{5}\right)\right]\hat{\theta}
$$

$$
= \frac{2\sin\theta\cos\theta}{\sin\theta}\,\frac{\mu_0\rho\omega}{2}\left(\frac{R^2}{3}-\frac{r^2}{5}\right)\hat{r} - \frac{1}{r\sin\theta}\,\frac{\mu_0\rho\omega\sin^2\theta}{2}\,\partial_r\left(\frac{r^2 R^2}{3}-\frac{r^4}{5}\right)\hat{\theta}
$$

$$
\vec{B} = \mu_0\rho\omega\cos\theta\left(\frac{R^2}{3}-\frac{r^2}{5}\right)\hat{r} - \frac{\mu_0\rho\omega\sin\theta}{2r}\left(\frac{2rR^2}{3}-\frac{4r^3}{5}\right)\hat{\theta}
$$

$$
\vec{B} = \mu_0\rho\omega\left[\left(\frac{R^2}{3}-\frac{r^2}{5}\right)\cos\theta\,\hat{r} - \left(\frac{R^2}{3}-\frac{2r^2}{5}\right)\sin\theta\,\hat{\theta}\right]
$$

$$
\rho = \frac{Q}{\frac{4}{3}\pi R^3}
$$

$$
\vec{B}_{\text{out}} = \frac{\mu_0\,\omega\, Q}{4\pi R}\left[\left(1-\frac{3r^2}{5R^2}\right)\cos\theta\,\hat{r} - \left(1-\frac{6r^2}{5R^2}\right)\sin\theta\,\hat{\theta}\right]
$$

*[The line above is boxed. sic: despite the title and the "out" subscript, this is the interior field ($r \le R$) — it follows from the $r' < r$ / $r' > r$ shell split above.]*

### P10. Metal Sphere with Linear Dielectric (Ex 4.5) *(pp. 15–16)*

A metal sphere of radius $a$ carrying free charge $Q$ is surrounded by a linear dielectric shell (permittivity $\varepsilon$, susceptibility $\chi_e$) out to radius $b$: find $\vec{D}$, $\vec{E}$, the potential at the origin, and the bound charges. *[The margin tag "Ex 4.5" is struck through; pages carry corner marks 1/2, 2/2.]*

**Solution.**

*[Diagram: concentric circles — inner sphere of radius $a$ with charge $Q$, dielectric shell out to radius $b$.]*

$$
\oint_{SA}\vec{D}\cdot d\vec{a} = Q_{f,\text{enc}} \qquad SA = 4\pi r^2 \qquad Q_{f,\text{enc}} = Q
$$

$$
\vec{D} = \frac{Q}{4\pi r^2}\,\hat{r} \qquad (r>a)
$$

Inside metal sphere $\vec{E} = \vec{P} = \vec{D} = 0$

$$
\vec{E} = \begin{cases} \dfrac{Q}{4\pi\varepsilon r^2}\,\hat{r} & a<r<b \\[2ex] \dfrac{Q}{4\pi\epsilon_0 r^2}\,\hat{r} & r>b \end{cases}
$$

$$
V = -\int_\infty^0 \vec{E}\cdot d\vec{l} = -\int_\infty^b E_{\text{out}}\,dr - \int_b^a E_{\text{mat}}\,dr - \int_a^0 E_{\text{in}}\,dr
$$

$$
V = \frac{-Q}{4\pi}\left[\int_\infty^b \frac{1}{\epsilon_0 r^2}\,dr + \int_b^a \frac{1}{\varepsilon r^2}\,dr\right]
$$

*[Underbraces mark the two integrals as $-\frac{1}{\epsilon_0}\left(\frac{1}{b}-\frac{1}{\infty}\right)$ and $-\frac{1}{\varepsilon}\left(\frac{1}{a}-\frac{1}{b}\right)$.]*

$$
V_{\text{org}} = \frac{Q}{4\pi}\left[\frac{1}{\epsilon_0 b} + \frac{1}{\varepsilon a} - \frac{1}{\varepsilon b}\right]
$$

*[The line above is boxed.]*

$$
\vec{P} = \epsilon_0\chi_e\vec{E} = \epsilon_0\chi_e\,\frac{Q}{4\pi\varepsilon r^2}\;\hat{r}
$$

$$
\rho_b = -\vec{\nabla}\cdot\vec{P} = 0
$$

while

$$
\sigma_b = \vec{P}\cdot\hat{n} = \begin{cases} \dfrac{\epsilon_0\chi_e Q}{4\pi\varepsilon b^2} & \text{outer surface} \\[2ex] \dfrac{-\epsilon_0\chi_e Q}{4\pi\varepsilon a^2} & \text{inner surface} \end{cases}
$$

### P11. Spherical Conductor w/ Linear Dielectric (Prob 4.26) *(pp. 17–18)*

Energy of the configuration: a spherical conductor of inner radius $a$ with charge $Q$, surrounded out to radius $b$ by linear dielectric material $\chi_e$; computes $W = \frac{1}{2}\int\vec{D}\cdot\vec{E}\,d\tau$.

**Solution.**

Inner radius $a$ w/ charge $Q$. Outer radius $b$ w/ linear dielectric material $\chi_e$.

*[Diagram: sphere of radius $a$ carrying $Q$, surrounded by a dielectric layer out to radius $b$.]*

$$
\vec{D} = \frac{Q}{4\pi r^2}\,\hat{r} \qquad (r>a)
$$

$$
\vec{E} = \begin{cases} \dfrac{Q}{4\pi\varepsilon r^2}\,\hat{r} & (a<r<b) \\[2ex] \dfrac{Q}{4\pi\epsilon_0 r^2}\,\hat{r} & (r>b) \end{cases}
$$

$$
u = \frac{1}{2}\left(\vec{D}\cdot\vec{E} + \vec{B}\cdot\vec{H}\right) \qquad W = \int u\,d\tau
$$

*[The $\vec{B}\cdot\vec{H}$ term is struck through with a 0 above it.]*

$$
W = \frac{1}{2}\int\vec{D}\cdot\vec{E}\,d\tau = \frac{1}{2}\left[\int_a^b \left(\vec{D}\cdot\vec{E}\right)d\tau + \int_b^\infty \left(\vec{D}\cdot\vec{E}\right)d\tau\right]
$$

$$
= \frac{1}{2}\frac{Q^2}{\left(4\pi\right)^2}\left[\int_a^b \frac{1}{\varepsilon r^4}\,d\tau + \int_b^\infty \frac{1}{\epsilon_0 r^4}\,d\tau\right]
$$

$$
\int_0^{2\pi}d\phi \int_0^{\pi}\sin\theta\,d\theta = 4\pi
$$

$$
W = \frac{4\pi}{2}\frac{Q^2}{\left(4\pi\right)^2}\left[\frac{1}{\varepsilon}\int_a^b \frac{r^2}{r^4}\,dr + \frac{1}{\epsilon_0}\int_b^\infty \frac{r^2}{r^4}\,dr\right]
$$

$$
\varepsilon_r = 1+\chi_e \qquad \epsilon_0\,\varepsilon_r = \varepsilon
$$

$$
W = \frac{Q^2}{8\pi\epsilon_0}\left\{\frac{1}{\left(1+\chi_e\right)}\int_a^b r^{-2}\,dr + \int_b^\infty r^{-2}\,dr\right\}
$$

*[Underbraces mark the integrals as $-r^{-1}\big|_a^b$ and $-r^{-1}\big|_b^\infty$.]*

$$
W = \frac{Q^2}{8\pi\epsilon_0}\left[\frac{\left(\frac{1}{a}-\frac{1}{b}\right)}{\left(1+\chi_e\right)} + \frac{1}{b}\right]
$$

$$
W = \frac{Q^2}{8\pi\epsilon_0\left(1+\chi_e\right)}\left[\frac{1}{a} + \frac{\chi_e}{b}\right]
$$

*[The line above is boxed.]*

### P12. Loop Inductance (Prob 7.22) *(p. 19)*

A small loop of radius $a$ sits on the axis of a large loop of radius $b$, a height $z$ above it: the flux through the little loop from current $I$ in the big loop, and the mutual-inductance reciprocity $M_{12}=M_{21}$ checked via the little loop's dipole field.

**Solution.**

*[Diagram: small loop of radius $a$ at height $z$ above a coaxial large loop of radius $b$; side triangle with legs $z$, $b$ and hypotenuse $\mathfrak{r}$.]*

$$
\vec{B} = \frac{\mu_0 I}{4\pi}\int\frac{d\vec{l}\times\hat{\mathfrak{r}}}{\mathfrak{r}^2}
$$

$$
dl = b\,d\phi\,\hat{\phi} \qquad \vec{\mathfrak{r}} = z\,\hat{z}-b\,\hat{r} \qquad \mathfrak{r}^2 = b^2+z^2 \qquad dl\times\vec{\mathfrak{r}} = b^2\,d\phi\,\hat{z}
$$

$$
\vec{B} = \frac{\mu_0 I}{4\pi}\int\frac{b^2\,d\phi\,\hat{z}}{\left(b^2+z^2\right)^{3/2}}
$$

$$
\vec{B} = \frac{\mu_0 I}{2}\,\frac{b^2}{\left(b^2+z^2\right)^{3/2}}\;\hat{z}
$$

$$
\Phi = \int\vec{B}\cdot d\vec{a} = B\,\pi a^2 = \frac{\mu_0 I \pi a^2 b^2}{2\left(b^2+z^2\right)^{3/2}} = \Phi_a
$$

*[The flux result is boxed.]*

$$
\Phi_1 = M_{12} I_2 \qquad \Phi_2 = M_{21} I_1
$$

$$
M_{12} = M_{21}
$$

$$
\vec{B}_b = \vec{B}_{\text{dip}} \qquad \left|\vec{m}_a\right| = I\pi a^2
$$

where $r = \sqrt{b^2+z^2}$, $\sin\theta = \dfrac{b}{r}$ — gives same flux.

### P13. ||-Plate Cap. w/ 2 Linear Dielectric (Problem 4.18) *(pp. 20–21)*

A parallel-plate capacitor with plate charge $\pm\sigma$ is filled by two linear dielectric slabs, each of thickness $a$: slab 1 ($\varepsilon_1 = 2\epsilon_0$) against the positive plate, slab 2 ($\varepsilon_2 = \frac{3}{2}\epsilon_0$) below it. Find $D$, $E$, $P$, the potential difference, the bound charges, and re-check the fields from all the surface charges.

**Solution.**

*[Diagram: 3-D sketch of the stack — hatched top plate at $+\sigma$, slab 1 then slab 2 (thicknesses $a$ and $a$), bottom plate at $-\sigma$; $\hat{z}$ drawn pointing downward.]*

$$
\varepsilon_1 = 2\epsilon_0 \qquad \varepsilon_2 = \frac{3}{2}\epsilon_0
$$

$$
\oint\vec{D}\cdot da = Q_{f,\text{enc}} \qquad DA = \sigma A
$$

$$
D = \sigma \qquad \hat{z}
$$

*[The line above is boxed.]*

$$
\vec{D} = \varepsilon\vec{E} \;\to\; \vec{E} = \frac{\sigma}{\varepsilon_1}\;\;\text{slab 1} \qquad \vec{E} = \frac{\sigma}{\varepsilon_2}\;\;\text{slab 2}
$$

$$
E_1 = \frac{\sigma}{2\epsilon_0} \qquad E_2 = \frac{2\sigma}{3\epsilon_0} \qquad \hat{z}
$$

*[The line above is boxed.]*

$$
\vec{P} = \epsilon_0\chi_e\vec{E} \qquad \varepsilon_r = 1+\chi_e = \frac{\varepsilon}{\epsilon_0} \qquad \varepsilon_r - 1 = \chi_e
$$

$$
\vec{P} = \epsilon_0\left(\varepsilon_r-1\right)\vec{E}
$$

$$
P_1 = \epsilon_0\left(2-1\right)E_1 = \frac{\epsilon_0\,\sigma}{2\epsilon_0} \qquad\qquad P_1 = \frac{\sigma}{2}
$$

$$
P_2 = \epsilon_0\left(\frac{3}{2}-1\right)E_2 = \frac{\epsilon_0}{2}\,\frac{2\sigma}{3\epsilon_0} \qquad\qquad P_2 = \frac{\sigma}{3}
$$

*[The $P_1 = \sigma/2$ and $P_2 = \sigma/3$ results are boxed.]*

$$
V = E_1 a + E_2 a = \frac{\sigma a}{2\epsilon_0} + \frac{2\sigma a}{3\epsilon_0}
$$

$$
V = \frac{\sigma a}{\epsilon_0}\left(\frac{1}{2}+\frac{2}{3}\right) = \frac{\sigma a}{\epsilon_0}\left(\frac{3+4}{6}\right) = \frac{7\sigma a}{6\epsilon_0}
$$

$$
V = \frac{7\sigma a}{6\epsilon_0}
$$

*[The line above is boxed.]*

$$
\rho_b = 0
$$

*[Diagram: the stack redrawn with the surface charges circled at each boundary — $+\sigma$ (top plate), $-\sigma/2$ and $+\sigma/2$ (top and bottom faces of slab 1), $-\sigma/3$ and $+\sigma/3$ (top and bottom faces of slab 2), $-\sigma$ (bottom plate).]*

(slab 1)

$$
\sum_{\sigma\,\text{above}} = \sigma - \frac{\sigma}{2}
$$

$$
\sum_{\sigma\,\text{below}} = \frac{\sigma}{2} - \frac{\sigma}{3} + \frac{\sigma}{3} - \sigma = -\frac{\sigma}{2}
$$

$$
\to\; E_1 = \frac{\sigma}{2\epsilon_0}
$$

similarly for slab 2

$$
\text{above: } \sigma - \frac{\sigma}{3} = \frac{2\sigma}{3} \qquad \text{below: } \frac{\sigma}{3} - \sigma = -\frac{2\sigma}{3}
$$

$$
E_2 = \frac{2\sigma}{3\epsilon_0} \;\checkmark
$$

### P14. Multipole Expansion *(pp. 22–23)*

Potential of a physical dipole: charges $+q$ and $-q$ separated by a distance $d$, evaluated at a field point a distance $r$ from the center at angle $\theta$ from the dipole axis. First the far-field ($r \gg d$) binomial expansion giving the dipole potential, then the full Legendre-series expansion giving the odd multipoles (dipole, quadrupole $\to 0$, octopole). (The page carries a struck-through problem tag, apparently "Prob 3.3…", before the title.)

**Solution.**

*[Diagram: $+q$ above $-q$ separated by $d$; field point at the end of $\vec{r}$ drawn from the dipole center at angle $\theta$ from the axis, with separation vectors $\mathfrak{r}_+$ from $+q$ and $\mathfrak{r}_-$ from $-q$.]*

$$
V(\vec{r}) = \frac{1}{4\pi\epsilon_0}\left(\frac{q}{\mathfrak{r}_+} - \frac{q}{\mathfrak{r}_-}\right)
$$

$$
\mathfrak{r}_\pm^2 = r^2 + \left(\frac{d}{2}\right)^2 \mp rd\cos\theta = r^2\left(1 \mp \frac{d}{r}\cos\theta + \frac{d^2}{4r^2}\right)
$$

For $r \gg d$ the 3rd term is negligible.

$$
\frac{1}{\mathfrak{r}_\pm} \approx \frac{1}{r}\left(1 \mp \frac{d}{r}\cos\theta\right)^{-1/2} \approx \frac{1}{r}\left(1 \pm \frac{d}{2r}\cos\theta\right)
$$

$$
\frac{1}{\mathfrak{r}_+} - \frac{1}{\mathfrak{r}_-} \approx \frac{d}{r^2}\cos\theta \;\longrightarrow\; V(\vec{r}) \approx \frac{1}{4\pi\epsilon_0}\,\frac{dq\cos\theta}{r^2}
$$

*[Dashed rule; the general expansion follows.]*

$$
\frac{1}{\mathfrak{r}} = \frac{1}{r}\sum_{n=0}^{\infty}\left(\frac{r'}{r}\right)^n P_n(\cos\alpha)
$$

choosing $\mathfrak{r} \to \mathfrak{r}_+$, $\;r' \to \frac{d}{2}$, $\;\alpha \to \theta$

$$
\frac{1}{\mathfrak{r}_+} = \frac{1}{r}\sum_{n=0}^{\infty}\left(\frac{d}{2r}\right)^n P_n(\cos\theta)
$$

$\mathfrak{r}_-$: $\;\theta \to \theta + 180 \;\longrightarrow\; \cos\theta \to -\cos\theta$

$$
\frac{1}{\mathfrak{r}_-} = \frac{1}{r}\sum_{n=0}^{\infty}\left(\frac{d}{2r}\right)^n P_n(-\cos\theta)
$$

$$
P_n(-x) = (-1)^n P_n(x)
$$

$$
V = \frac{1}{4\pi\epsilon_0}\, q\left(\frac{1}{\mathfrak{r}_+} - \frac{1}{\mathfrak{r}_-}\right)
= \frac{1}{4\pi\epsilon_0}\, q\,\frac{1}{r}\sum_{n=0}^{\infty}\left(\frac{d}{2r}\right)^n \left[P_n(\cos\theta) - P_n(-\cos\theta)\right]
$$

$$
= \frac{2q}{4\pi\epsilon_0 r}\sum_{n=1,3,5,\ldots}\left(\frac{d}{2r}\right)^n P_n(\cos\theta)
$$

dipole ($n=1$) $\longrightarrow$

$$
V_{dip} = \frac{2q}{4\pi\epsilon_0 r}\,\frac{d}{2r}\,P_1(\cos\theta) = \frac{qd\cos\theta}{4\pi\epsilon_0 r^2}
$$

Quadrupole ($n=2$) $\longrightarrow$ zero. Octopole ($n=3$):

$$
V_{oct} = \frac{2q}{4\pi\epsilon_0}\,\frac{1}{r}\left(\frac{d}{2r}\right)^3 P_3(\cos\theta), \qquad P_3(x) = \frac{5x^3 - 3x}{2}
$$

$$
V_{oct} = \frac{2q}{4\pi\epsilon_0}\,\frac{1}{r}\,\frac{d^3}{8r^3}\left(\frac{5\cos^3\theta - 3\cos\theta}{2}\right)
$$

$$
V_{oct} = \frac{qd^3}{4\pi\epsilon_0}\,\frac{1}{8r^4}\left(5\cos^3\theta - 3\cos\theta\right)
$$

### P15. Reflection & Transmission @ Oblique Incidence *(pp. 24–28)*

A monochromatic plane wave in medium 1 strikes the interface with medium 2 at incidence angle $\theta_I$, with the polarization in the plane of incidence. Phase matching at the boundary gives the three laws of geometrical optics; the four electromagnetic boundary conditions then give the Fresnel equations for $\tilde{E}_{0_R}$ and $\tilde{E}_{0_T}$. Four-page entry marked 1/4–4/4. *[pp. 26 and 27 are duplicate scans of the same sheet (3/4).]*

**Solution.**

$$
\vec{E}_I(\vec{r},t) = \tilde{E}_{0_I}\, e^{i(\vec{k}_I\cdot\vec{r} - \omega t)}, \qquad
\vec{B}_I(\vec{r},t) = \frac{1}{v_1}\left(\hat{k}_I \times \vec{E}_I\right)
$$

similarly for $\vec{E}_R$, $\vec{B}_R$, $\vec{E}_T$, $\vec{B}_T$.

*[Diagram: hatched interface with normal along $\hat{z}$, $\hat{x}$ along the surface; $\vec{k}_I$ incident at $\theta_I$, $\vec{k}_R$ reflected at $\theta_R$, $\vec{k}_T$ transmitted.]*

$$
k_I v_1 = k_R v_1 = k_T v_2 = \omega
$$

$$
k_I = k_R = \frac{v_2}{v_1}\,k_T = \frac{n_1}{n_2}\,k_T
$$

$$
(\;)\,e^{i(\vec{k}_I\cdot\vec{r} - \omega t)} + (\;)\,e^{i(\vec{k}_R\cdot\vec{r} - \omega t)} = (\;)\,e^{i(\vec{k}_T\cdot\vec{r} - \omega t)} \qquad (z=0)
$$

$$
\vec{k}_I\cdot\vec{r} = \vec{k}_R\cdot\vec{r} = \vec{k}_T\cdot\vec{r} \qquad (z=0)
$$

$$
x(k_I)_x + y(k_I)_y = x(k_R)_x + y(k_R)_y = x(k_T)_x + y(k_T)_y
$$

if $x=0$:

$$
(k_I)_y = (k_R)_y = (k_T)_y
$$

if $y=0$:

$$
(k_I)_x = (k_R)_x = (k_T)_x
$$

where $\vec{k}$ lies in the x-z plane, so $(k_I)_y = 0$ (1st Law — plane of incidence). So

$$
k_I\sin\theta_I = k_R\sin\theta_R = k_T\sin\theta_T
$$

$$
\theta_I = \theta_R
$$

(2nd Law — "angle of refraction") *[sic: $\theta_I = \theta_R$ is the law of reflection]*

$$
k_I\sin\theta_I = k_T\sin\theta_T \qquad \text{where } k_I = \frac{n_1}{n_2}k_T
$$

so

$$
\frac{\sin\theta_T}{\sin\theta_I} = \frac{n_1}{n_2} \qquad \text{(3rd Law — Snell's)}
$$

B.C.'s:

$$
\text{(i)}\quad \epsilon_1\left(\vec{E}_{0_I} + \vec{E}_{0_R}\right)_z = \epsilon_2\left(\vec{E}_{0_T}\right)_z
$$

$$
\text{(ii)}\quad \left(\vec{B}_{0_I} + \vec{B}_{0_R}\right)_z = \left(\vec{B}_{0_T}\right)_z
$$

$$
\text{(iii)}\quad \left(\vec{E}_{0_I} + \vec{E}_{0_R}\right)_{x,y} = \left(\vec{E}_{0_T}\right)_{x,y}
$$

$$
\text{(iv)}\quad \frac{1}{\mu_1}\left(\vec{B}_{0_I} + \vec{B}_{0_R}\right)_{x,y} = \frac{1}{\mu_2}\left(\vec{B}_{0_T}\right)_{x,y}
$$

*[Diagram: media ① and ② separated by the hatched interface; $\vec{E}_I$, $\vec{E}_R$, $\vec{E}_T$ drawn in the plane of incidence with $\vec{B}$'s perpendicular to their $\vec{k}$'s; angles $\theta_I$, $\theta_R$, $\theta_T$ measured from the z-axis.]*

$$
\text{(i)}\quad \epsilon_1\left(-\tilde{E}_{0_I}\sin\theta_I + \tilde{E}_{0_R}\sin\theta_R\right) = \epsilon_2\left(-\tilde{E}_{0_T}\sin\theta_T\right) \qquad (1)
$$

$\vec{B} = \frac{1}{v_1}(\hat{k}\times\vec{E})$; (ii) does nothing ($B_z = 0$).

$$
\text{(iii)}\quad \tilde{E}_{0_I}\cos\theta_I + \tilde{E}_{0_R}\cos\theta_R = \tilde{E}_{0_T}\cos\theta_T \qquad (2)
$$

$$
\text{(iv)}\quad \frac{1}{\mu_1}\left(\tilde{B}_{0_I} + \tilde{B}_{0_R}\right)_{x,y} = \frac{1}{\mu_2}\left(\tilde{B}_{0_T}\right)_{x,y}
$$

$$
\vec{B}_0 = \frac{1}{v_1}\left(\hat{k}\times\vec{E}_0\right)
$$

$$
\frac{1}{\mu_1 v_1}\left(\tilde{E}_{0_I} - \tilde{E}_{0_R}\right) = \frac{1}{\mu_2 v_2}\,\tilde{E}_{0_T} \qquad (3)
$$

$$
\longrightarrow\quad \tilde{E}_{0_I} - \tilde{E}_{0_R} = \frac{\mu_1 v_1}{\mu_2 v_2}\,\tilde{E}_{0_T}
$$

let

$$
\beta \equiv \frac{\mu_1 v_1}{\mu_2 v_2} = \frac{\mu_1 n_2}{\mu_2 n_1}, \qquad
\tilde{E}_{0_I} - \tilde{E}_{0_R} = \beta\,\tilde{E}_{0_T} \qquad (4)
$$

$\theta_I = \theta_R$, so

$$
(2) \longrightarrow\quad \tilde{E}_{0_I} + \tilde{E}_{0_R} = \frac{\cos\theta_T}{\cos\theta_I}\,\tilde{E}_{0_T}
$$

let $\alpha \equiv \dfrac{\cos\theta_T}{\cos\theta_I}$, so

$$
\tilde{E}_{0_I} + \tilde{E}_{0_R} = \alpha\,\tilde{E}_{0_T} \qquad (5)
$$

$(4)+(5) \longrightarrow$

$$
2\tilde{E}_{0_I} = (\alpha + \beta)\,\tilde{E}_{0_T} \qquad (6)
$$

$(5)-(4) \longrightarrow$

$$
2\tilde{E}_{0_R} = (\alpha - \beta)\,\tilde{E}_{0_T}
\quad\longrightarrow\quad
\frac{2\tilde{E}_{0_R}}{\alpha - \beta} = \tilde{E}_{0_T}
$$

$$
(6) \longrightarrow\quad \tilde{E}_{0_I} = \left(\frac{\alpha+\beta}{\alpha-\beta}\right)\tilde{E}_{0_R}
$$

(the 2's cancel), so

$$
\tilde{E}_{0_T} = \left(\frac{2}{\alpha+\beta}\right)\tilde{E}_{0_I}
$$

$$
\tilde{E}_{0_R} = \left(\frac{\alpha-\beta}{\alpha+\beta}\right)\tilde{E}_{0_I}
$$

(both boxed) — Fresnel's equations.

### P16. Ex 5.1 Cyclotron Motion *(pp. 29–30)*

Griffiths Ex 5.1: a charge $Q$ moves counterclockwise with speed $v$ around a circle of radius $R$ in the uniform field $\vec{B} = -B\hat{z}$; the magnetic force supplies the centripetal acceleration, giving the cyclotron momentum formula. *[p. 29 is a faint pencil-scan duplicate of the same sheet as p. 30.]*

**Solution.**

$$
\vec{B} = -B\hat{z}
$$

$Q$ moves counterclockwise w/ speed $v$ @ radius $R$.

$$
F_{mag} = QvB = ma, \qquad a = \frac{v^2}{R}
$$

$$
QvB = m\frac{v^2}{R} \;\longrightarrow\; p = QBR
$$

$$
QBR = mv \;\longrightarrow\; p = mv
$$

*[Diagram: circular orbit of radius $R$ in the x–y plane, with the charge $Q$ on the circle carrying tangential $\vec{v}$ and inward $\vec{F}$, axes $x$, $y$, $z$ drawn. Beside it: a helix wound along the field direction, with arrows $B$ along the axis and $v_{\parallel}$ parallel to it — the trajectory when the particle also has a velocity component along $\vec{B}$.]*

### P17. B-field on Atomic Orbits *(pp. 31–32)*

Effect of a magnetic field on an electron's circular atomic orbit (radius $R$, speed $v$): the orbit is treated as a current loop with orbital dipole moment $\vec{m}$; switching on $\vec{B}$ adds the force $-e(\vec{v}\times\vec{B})$, speeding the electron to $v'$ at fixed $R$, and the resulting $\Delta\vec{m}$ is opposite to $\vec{B}$ (diamagnetism).

**Solution.**

$$
T = \frac{2\pi R}{v} \qquad \text{(Period)}
$$

$$
I = \frac{-e}{T} = \frac{-ev}{2\pi R}
$$

Orbital dipole moment ($I\pi R^2$):

$$
\vec{m} = \frac{-ev}{2\pi R}\,\pi R^2 = -\frac{1}{2}\,evR\,\hat{z}
$$

$$
\vec{F} = m\vec{a}
$$

$$
\frac{1}{4\pi\epsilon_0}\frac{e^2}{R^2} = m_e\,\frac{v^2}{R}
$$

w/ additional force $-e\left(\vec{v}\times\vec{B}\right)$:

$$
\frac{1}{4\pi\epsilon_0}\frac{e^2}{R^2} + ev'B = m_e\,\frac{v'^2}{R} \qquad (v' > v)
$$

$$
ev'B = \frac{m_e}{R}\left(v'^2 - v^2\right) = \frac{m_e}{R}(v'+v)(v'-v)
$$

assuming $\Delta v = v' - v$ is small,

$$
\Delta v = \frac{eRB}{2m_e}
$$

$$
\Delta\vec{m} = -\frac{1}{2}\,e(\Delta v)R\,\hat{z} = -\frac{e^2R^2}{4m_e}\,\vec{B}
$$

### P18. Boundary-Condition Reference Notes *(pp. 33–35)*

*[reference notes, not a worked problem]*

Summaries of the boundary conditions (and asymptotic conditions) used to fix the coefficients in the classic separation-of-variables sphere problems — electrostatic potential $V$ for charged/dielectric/conducting spheres, magnetic scalar potential $W$ for magnetized and permeable spheres, and the ansatz for a conducting sphere with an insulating dielectric shell.

**Solution.**

**Charge Density of Shell** (conditions listed (ii) then (i) on the page):

$$
\text{(ii)}\quad \frac{\partial V_{in}}{\partial r}\bigg|_R - \frac{\partial V_{out}}{\partial r}\bigg|_R = \frac{\sigma_0(\theta)}{\epsilon_0}
$$

$$
\text{(i)}\quad V_{out}\big|_R = V_{in}\big|_R
$$

**Dielectric Sphere in $\vec{E}$-field:**

$$
\text{(i)}\quad V_{in}\big|_R = V_{out}\big|_R
$$

$$
\text{(ii)}\quad \varepsilon\,\frac{\partial V_{in}}{\partial r}\bigg|_{r=R} = \epsilon_0\,\frac{\partial V_{out}}{\partial r}\bigg|_R
$$

$$
\text{(iii)}\quad V_{out} \longrightarrow -E_0\, r\cos\theta \qquad (r \gg R)
$$

**Uncharged Sphere in E-field:**

$$
\text{(i)}\quad V_{in}\big|_R = V_{out}\big|_R
$$

$$
\text{(ii)}\quad -\epsilon_0\,\frac{\partial V}{\partial r}\bigg|_R = \sigma(\theta)
$$

$$
\text{(iii)}\quad V_{out} \longrightarrow -E_0\, r\cos\theta \qquad (r \gg R)
$$

**Uniform $\vec{M}$ sphere:**

$$
\text{(i)}\quad W_{in}\big|_R = W_{out}\big|_R
$$

$$
\text{(ii)}\quad \frac{\partial W_{in}}{\partial r}\bigg|_R - \frac{\partial W_{out}}{\partial r}\bigg|_R = M^{\perp} = M\,\hat{z}\cdot\hat{r} = M\cos\theta
$$

**Uniform $\vec{M}$ in B-field** (the conditions are those of a linear permeable sphere in a uniform $B_0$):

$$
\text{(i)}\quad W_{in}\big|_R = W_{out}\big|_R
$$

$$
\text{(ii)}\quad \mu\,\frac{\partial W_{in}}{\partial r}\bigg|_R - \mu_0\,\frac{\partial W_{out}}{\partial r}\bigg|_R = 0
$$

$$
\text{(iii)}\quad W_{out} \longrightarrow -\frac{1}{\mu_0}B_0\, r\cos\theta \qquad (r \gg R)
$$

**Uncharged Cond. Sphere w/ insulating shell in $E_0$-field:**

$$
V_{out} = -E_0\, r\cos\theta + \sum_{\ell}\frac{B_\ell}{r^{\ell+1}}\,P_\ell(\cos\theta)
$$

$$
V_{int} = \sum_{\ell}\left(A_\ell\, r^\ell + \frac{\bar{B}_\ell}{r^{\ell+1}}\right)P_\ell(\cos\theta)
$$

$$
V_{in} = 0
$$

$$
V_{out} = V_{int} \qquad (r=b)
$$

$$
\varepsilon\,\frac{\partial V_{int}}{\partial r}\bigg|_b = \epsilon_0\,\frac{\partial V_{out}}{\partial r}\bigg|_b
\qquad\qquad
V_{int}\big|_a = 0
$$

### P19. Ex 2.7 Potential of Spherical Shell w/ Uniform Surface Charge *(p. 36)*

Potential inside and outside a spherical shell of radius $R$ carrying total charge $q$ uniformly on its surface, found by integrating $-\int \vec{E}\cdot d\vec{l}$ in from infinity.

**Solution.**

If the shell has a total charge $q$ it can be treated as a point on the origin (from $r \geq R$).

$$
\vec{E}_{out} = \frac{1}{4\pi\epsilon_0}\frac{q}{r^2}\,\hat{r}
$$

*[Diagram: sphere of radius $R$ with a field point P outside on a radial ray.]*

Due to symmetry

$$
\vec{E}_{in} = 0
$$

$$
V_{out} = -\int_{\infty}^{r}\vec{E}\cdot d\vec{l} = -\frac{1}{4\pi\epsilon_0}\,q\int_{\infty}^{r}\frac{1}{r'^2}\,dr'
$$

$$
= +\frac{q}{4\pi\epsilon_0}\,\frac{1}{r'}\bigg|_{\infty}^{r} = \frac{q}{4\pi\epsilon_0}\,\frac{1}{r}
$$

$$
V_{out} = \frac{1}{4\pi\epsilon_0}\frac{q}{r}
$$

(boxed) *[Small sketch: the $1/r$ fall-off of $V$ outside the shell, axis labeled $r$, marked "$R \to \infty$".]*

$$
V_{in}(r) = -\frac{1}{4\pi\epsilon_0}\int_{\infty}^{R}\frac{q}{r'^2}\,dr' - \int_{R}^{r} 0 = \frac{1}{4\pi\epsilon_0}\,\frac{q}{r'}\bigg|_{\infty}^{R}
$$

$$
\nabla V = 0
$$

$$
V_{in} = \frac{1}{4\pi\epsilon_0}\frac{q}{R}
$$

(boxed)

### P20. Ex 4.8 Point Charge Above Linear Dielectric *(pp. 37–39)*

Given: the region $z<0$ is filled with a uniform linear dielectric of susceptibility $\chi_e$. Solve: calculate the force on a point charge $q$ situated a distance $d$ above the origin — via the bound surface charge $\sigma_b$ at $z=0$ and the method of images.

**Solution.**

*[Diagram: 3-D sketch of the dielectric half-space $z<0$ with axes $x$, $y$, $z$; the charge $q$ sits on the $\hat{z}$-axis a height $d$ above the origin, with angle $\theta$ to a surface point; annotation with an arrow to the interface: "$q(\text{surface}) = -q$ @ $z=0$, so attractive".]*

$$
\sigma_b = \vec{P}\cdot\hat{n} = P_z = \epsilon_0\chi_e E_z
$$

*[Diagram: right triangle with vertical leg $d$, horizontal leg $r$, hypotenuse $\sqrt{r^2+d^2} = \mathfrak{r}$, angle $\theta$ at the top]* — so when $d = \mathfrak{r}\cos\theta$,

$$
-\frac{1}{4\pi\epsilon_0}\frac{q\cos\theta}{(r^2+d^2)} = -\frac{1}{4\pi\epsilon_0}\frac{qd}{(r^2+d^2)^{3/2}}
$$

z-component of the field of the bound charge is $-\sigma_b/2\epsilon_0$ (pg 90 footnote).

$$
\sigma_b = \epsilon_0\chi_e\left(-\frac{1}{4\pi\epsilon_0}\frac{qd}{\left(r^2+d^2\right)^{3/2}} - \frac{\sigma_b}{2\epsilon_0}\right)
$$

then

$$
\sigma_b = -\frac{1}{2\pi}\left(\frac{\chi_e}{\chi_e+2}\right)\frac{qd}{\left(r^2+d^2\right)^{3/2}}
$$

ignoring $\left(\frac{\chi_e}{\chi_e+2}\right)$ this is the same as the induced charge on an infinite conducting plane.

Total bound charge

$$
q_b = -\left(\frac{\chi_e}{\chi_e+2}\right)q
$$

(boxed). By direct integration

$$
\vec{E} = \frac{1}{4\pi\epsilon_0}\int \frac{\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,\sigma_b\, da
$$

Method of images: replace the dielectric by a single point charge $q_b$ at image position $(0,0,-d)$:

$$
V = \frac{1}{4\pi\epsilon_0}\left(\frac{q}{\sqrt{x^2+y^2+(z-d)^2}} + \frac{q_b}{\sqrt{x^2+y^2+(z+d)^2}}\right)
\qquad \text{for } z>0
$$

A charge $q+q_b$ at $(0,0,d)$ yields the potential *[preceding words struck out; this is the potential in the region $z<0$]*

$$
V = \frac{1}{4\pi\epsilon_0}\,\frac{q+q_b}{\sqrt{x^2+y^2+(z-d)^2}}
$$

Using the two potentials, constitute a function that satisfies Poisson's equation with a point charge $q$ at $(0,0,d)$, which goes to zero at infinity, which is continuous at the boundary $z=0$, and whose normal derivative exhibits the discontinuity appropriate to the surface charge $\sigma_b$ at $z=0$:

$$
-\epsilon_0\left(\frac{\partial V}{\partial z}\bigg|_{z=0^+} - \frac{\partial V}{\partial z}\bigg|_{z=0^-}\right)
= -\frac{1}{2\pi}\left(\frac{\chi_e}{\chi_e+2}\right)\frac{qd}{\left(x^2+y^2+d^2\right)^{3/2}}
$$

The force on $q$ is

$$
\vec{F} = \frac{1}{4\pi\epsilon_0}\,\frac{qq_b}{(2d)^2}\,\hat{z}
= -\frac{1}{4\pi\epsilon_0}\left(\frac{\chi_e}{\chi_e+2}\right)\frac{q^2}{4d^2}\,\hat{z}
$$

*[Top of p. 39 carries a struck-through false start of the next problem's title ("Uniform Current Over a Wire"), taken up on p. 40.]*

### P21. Ex 5.4(a) Uniform Current Over a Wire *(pp. 40–41)*

Griffiths Ex 5.4: (a) a current $I$ is uniformly distributed over a wire of circular cross section with radius $a$ — find the volume current density $J$; (b) the current density in the wire is proportional to the distance from the axis, $J = ks$ — find the total current. The entry closes by deriving the continuity equation from the divergence theorem.

**Solution.**

Find: volume current density $J$.

$$
J = \frac{I}{\pi a^2}
$$

b) Current density in the wire is proportional:

$$
J = ks
$$

Solution:

$$
\vec{J} = \frac{d\vec{I}}{da_\perp}, \qquad da_\perp = s\,ds\,d\phi
$$

$$
I = \int J\,da_\perp = \iint (ks)(s\,ds\,d\phi)
$$

$$
I = 2\pi k \int_0^a s^2\,ds = \frac{2\pi k a^3}{3}
$$

$$
I = \int_S J\,da_\perp = \int_S \vec{J}\cdot d\vec{a}
$$

Then by the divergence theorem,

$$
\oint_S \vec{J}\cdot d\vec{a} = \int_{\forall}\left(\nabla\cdot\vec{J}\right)d\tau
$$

$$
\int_{\forall}\left(\nabla\cdot\vec{J}\right)d\tau = -\frac{d}{dt}\int_{\forall}\rho\,d\tau = -\int_{\forall}\left(\frac{\partial\rho}{\partial t}\right)d\tau
$$

giving the boxed continuity equation

$$
\nabla\cdot\vec{J} = -\frac{\partial\rho}{\partial t}
$$

$$
q \sim \lambda\,dl \sim \sigma\,da \sim \rho\,d\tau
$$

### P22. Prob 4.12 Potential of Uniform Polarized Sphere *(p. 42)*

Griffiths Prob 4.12: compute the potential of a uniformly polarized sphere (radius $R$, uniform $\vec{P}$) directly from $V = \frac{1}{4\pi\epsilon_0}\int \vec{P}\cdot\hat{\mathfrak{r}}/\mathfrak{r}^2\,d\tau'$, by recognizing the integral as the field of a uniformly charged sphere.

**Solution.**

$$
V = \frac{1}{4\pi\epsilon_0}\int \frac{\vec{P}\cdot\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,d\tau'
$$

$$
\rightarrow\; \frac{\vec{P}}{4\pi\epsilon_0}\cdot\int \frac{\vec{\mathfrak{r}}}{\mathfrak{r}^3}\,d\tau, \qquad \vec{E} = \frac{1}{4\pi\epsilon_0}\int \frac{\rho\,\vec{\mathfrak{r}}}{\mathfrak{r}^3}\,d\tau'
$$

$$
V = \vec{P}\cdot\frac{\vec{E}_{ucs}}{\rho}
$$

($\vec{E}_{ucs}$ = $\vec{E}$ of the uniform charged sphere.)

$$
\vec{E}_{out} = \frac{1}{4\pi\epsilon_0}\frac{q}{r^2}\hat{r} \qquad \text{where } q = \rho\forall
$$

$$
\vec{E}_{out} = \frac{1}{4\pi\epsilon_0}\,\frac{\frac{4}{3}\pi R^3\rho}{r^2}\,\hat{r}
$$

$$
\vec{E}_{in} = \frac{1}{4\pi\epsilon_0}\,\frac{\frac{4}{3}\pi R^3\rho}{R^3}\,\vec{r}
$$

Boxed results:

$$
V_{in} = \vec{P}\cdot\frac{1}{3\epsilon_0}\vec{r} = \frac{P r\cos\theta}{3\epsilon_0}
$$

$$
V_{out} = \vec{P}\cdot\frac{R^3\,\hat{r}}{3\epsilon_0 r^2} = \frac{R^3 P\cos\theta}{3\epsilon_0 r^2}
$$

### P23. B Field of Perfect Dipole *(pp. 43–44)*

Compute the magnetic field of a perfect (point) magnetic dipole $m$ at the origin, directed along $\hat{z}$, from its vector potential by taking the curl in spherical coordinates.

*[Diagram: x, y, z axes with dipole moment $m$ along $\hat{z}$ at the origin; a field point at $(r,\theta,\phi)$.]*

**Solution.**

$$
\vec{A}_{dip}(\vec{r}) = \frac{\mu_0}{4\pi}\frac{m\sin\theta}{r^2}\hat{\phi}
$$

$$
\vec{B}_{dip}(\vec{r}) = \nabla\times\vec{A}
$$

curl in spherical

$$
\nabla\times\vec{A} = \frac{1}{r\sin\theta}\left[\partial_\theta\left(\sin\theta\,A_\phi\right) - \partial_\phi A_\theta\right]\hat{r} + \frac{1}{r}\left[\frac{1}{\sin\theta}\,\partial_\phi A_r - \partial_r\left(r A_\phi\right)\right]\hat{\theta} + \frac{1}{r}\left(\frac{\partial}{\partial r}\left(r A_\theta\right) - \partial_\theta A_r\right)\hat{\phi}
$$

(the $\partial_\phi A_\theta$ and $\partial_\phi A_r$ terms are marked zero and the whole $\hat{\phi}$ term is struck out, since only $A_\phi$ is nonzero)

$$
\nabla\times\vec{A} = \frac{1}{r\sin\theta}\left(\partial_\theta\left(\sin\theta\,A_\phi\right)\right)\hat{r} - \frac{1}{r}\,\partial_r\left(r A_\phi\right)\hat{\theta}
$$

$$
\partial_\theta\left(\sin\theta\,A_\phi\right) = \frac{\mu_0}{4\pi}\frac{m}{r^2}\,2\sin\theta\cos\theta
$$

$$
\partial_r\left(r A_\phi\right) = \frac{\mu_0}{4\pi}\,m\sin\theta\,\partial_r\left(r^{-1}\right) \;\rightarrow\; \frac{\mu_0}{4\pi}\,m\sin\theta\left(-\frac{1}{r^2}\right)
$$

$$
\nabla\times\vec{A} = \frac{\mu_0}{4\pi}\frac{m}{r^3}\left[2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right]
$$

Boxed:

$$
\vec{B}_{dip} = \frac{\mu_0 m}{4\pi r^3}\left[2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right]
$$

### P24. Ex 4.2 Uniformly Polarized Sphere *(p. 45)*

Griffiths Ex 4.2: the field of a uniformly polarized sphere of radius $R$, obtained from the bound surface charge $\sigma_b = P\cos\theta$ by reusing the $\sigma = k\cos\theta$ boundary-value result; inside the field is $-\vec{P}/3\epsilon_0$, outside it is a perfect dipole.

**Solution.**

$$
\sigma_b = \vec{P}\cdot\hat{n} = P\cos\theta
$$

$$
V_{in} = \frac{k}{3\epsilon_0}\,r\cos\theta \;\Longrightarrow\; \frac{P r\cos\theta}{3\epsilon_0}
$$

$$
V_{out} = \frac{k R^3}{3\epsilon_0 r^2} \;\longrightarrow\; \frac{P}{3\epsilon_0}\frac{R^3}{r^2}\cos\theta
$$

$$
z = r\cos\theta
$$

$$
\vec{E}_{in} = -\nabla V = -\nabla\frac{P z}{3\epsilon_0}\,\hat{z} = -\frac{\vec{P}}{3\epsilon_0}
$$

Outside can be treated as perfect dipole

$$
V = \frac{1}{4\pi\epsilon_0}\frac{\vec{p}\cdot\hat{r}}{r^2} \qquad r \geq R
$$

$$
\vec{p} = \vec{P}\,d\tau'
$$

which agrees since $\vec{p} = \frac{4}{3}\pi R^3\vec{P}$

$$
V = \frac{4\pi R^3}{3\cdot 4\pi\epsilon_0}\frac{\vec{P}\cdot\hat{r}}{r^2} = \frac{P R^3\cos\theta}{3\epsilon_0 r^2}
$$

### P25. Ex 2.3 Uniform Charged Sphere *(p. 46)*

Solve: $\vec{E}$ outside a uniformly charged sphere of charge $q$ with radius $R$, by Gauss's law; then rewritten in terms of $\rho$, together with the interior field.

*[Diagram: sphere of radius R inside a larger concentric dashed spherical Gaussian surface of radius r, labeled "Pill Box".]*

**Solution.**

Gaussian surface @ $(r > R)$:

$$
\oint_S \vec{E}\cdot d\vec{a} = \frac{1}{\epsilon_0}Q_{enc}, \qquad Q_{enc} = q
$$

$$
\int_S \vec{E}\cdot da = \int \left|\vec{E}\right| da = \left|\vec{E}\right| 4\pi r^2
$$

Boxed:

$$
\vec{E}_{out} = \frac{1}{4\pi\epsilon_0}\frac{q}{r^2}\hat{r}
$$

$$
\rho = \frac{q}{\forall}
$$

$$
E_{out} = \frac{1}{4\pi\epsilon_0}\,\frac{\frac{4}{3}\pi R^3\rho}{r^2}\,\hat{r}
$$

$$
\vec{E}_{out} = \frac{\rho R^3}{3\epsilon_0 r^2}\hat{r}, \qquad \vec{E}_{in} = \frac{\rho}{3\epsilon_0}\vec{r}
$$

### P26. Magnetostatics *(p. 47)*

*[reference notes, not a worked problem]*

Opening reference sheet for the magnetostatics section: the magnetic and electric forces on a charge, the Lorentz force law, the statement that magnetic forces do no work, and the line-current form of the magnetic force.

*[Diagram: B field circling a wire carrying current I upward; two antiparallel currents I with the field lines between them bulging apart; two parallel currents I bowing toward each other with force F.]*

**Solution.**

$$
\vec{F}_{mag} = Q\left(\vec{v}\times\vec{B}\right), \qquad \vec{F}_E = Q\vec{E}
$$

Lorentz Force Law

$$
\vec{F} = Q\left[\vec{E} + \left(\vec{v}\times\vec{B}\right)\right]
$$

magnetic forces do no work

$$
dW_{mag} = \vec{F}_{mag}\cdot d\vec{l} = Q\left(\vec{v}\times\vec{B}\right)\cdot\vec{v}\,dt = 0
$$

Currents:

$$
\vec{I} = \lambda\vec{v}
$$

$$
\vec{F}_{mag} = \int\left(\vec{v}\times\vec{B}\right)dq = \int\left(\vec{v}\times\vec{B}\right)\lambda\,dl = \int\left(\vec{I}\times\vec{B}\right)dl
$$

$$
\vec{F}_{mag} = \int I\left(d\vec{l}\times\vec{B}\right)
$$

### P27. Ex 2.4 Cylindrically Charged Density *(p. 48)*

Griffiths Ex 2.4: a long cylinder carries charge density proportional to the distance from the axis, $\rho = ks$; find $\vec{E}$ inside using a Gaussian cylinder of radius $s$ and length $\ell$.

*[Diagram: cylinder of length $\ell$ about the $\hat{z}$ axis, with $s$ the radial distance from the axis.]*

**Solution.**

$$
\oint_S \vec{E}\cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0}, \qquad A_{cylinder} = 2\pi s\ell, \qquad d\tau = s'\,ds'\,d\phi\,dz
$$

$$
Q_{enc} = \int \rho\,d\tau = \int_0^{2\pi} d\phi \int_0^{\ell} dz \int_0^s k s'^2\,ds'
$$

$$
Q_{enc} = 2\pi k\ell \int_0^s s'^2\,ds' = 2\pi k\ell\,\frac{s^3}{3}
$$

$$
\oint_S \left|\vec{E}\right| da = \frac{Q_{enc}}{\epsilon_0}
$$

$$
\left|\vec{E}\right| 2\pi s\ell = \frac{1}{\epsilon_0}\frac{2}{3}\pi k\ell s^3
$$

Boxed:

$$
\vec{E}_{in} = \frac{k s^2}{3\epsilon_0}\hat{s}
$$

### P28. Ex 2.5 Rectangular Pill Box *(p. 49)*

Griffiths Ex 2.5: an infinite plane carries uniform surface charge $\sigma$; find $\vec{E}$ using a rectangular Gaussian pillbox of face area $A$ straddling the plane.

*[Diagram: infinite plane with a rectangular pillbox of face area A straddling it; $\vec{E}$ points up above the plane and down below.]*

**Solution.**

$$
\oint \vec{E}\cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0}, \qquad Q_{enc} = \sigma A
$$

$$
\oint \vec{E}\cdot da = \int \left|\vec{E}\right| da = 2A\left|\vec{E}\right|
$$

$$
\oint \vec{E}\cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0} \;\Rightarrow\; 2A\left|\vec{E}\right| = \frac{\sigma A}{\epsilon_0}
$$

Boxed:

$$
\vec{E} = \frac{\sigma}{2\epsilon_0}\hat{n}
$$

### P29. Ex 4.4 Wire with Rubber Dielectric *(p. 50)*

Griffiths Ex 4.4: a uniform line charge $\lambda$ with rubber insulation up to $r = a$; find $\vec{D}$ from the free charge using a Gaussian cylinder of radius $s$ and length $L$, then $\vec{E}$ outside the rubber.

*[Diagram: wire carrying line charge $\lambda$ along the axis of a dielectric cylinder of radius a, with a coaxial Gaussian cylinder of radius s and length L inside it.]*

**Solution.**

$$
\oint \vec{D}\cdot d\vec{a} = Q_{f\,enc}, \qquad \vec{D} \equiv \epsilon_0\vec{E} + \vec{P}
$$

$$
A_{cyl} = 2\pi r h, \qquad A_{gaus} = 2\pi s L
$$

$$
\oint \vec{D}\cdot d\vec{a} \;\longrightarrow\; D\left(2\pi s L\right), \qquad Q_{f\,enc} \;\longrightarrow\; \lambda L
$$

$$
D\,2\pi s L = \lambda L
$$

Boxed:

$$
\vec{D} = \frac{\lambda}{2\pi s}\hat{s}
$$

for $s > a$, $\vec{P} = 0$, and $\vec{D} \equiv \epsilon_0\vec{E} + \vec{P}$ with the $\vec{P}$ term marked zero, so boxed:

$$
\vec{E}_{out} = \frac{\lambda}{2\pi\epsilon_0 s}\hat{s} \qquad (s > a)
$$

### P30. Ex 7.2 *(p. 51)*

Griffiths Ex 7.2: the radial current between two coaxial cylinders (inner radius $a$, outer radius $b$, length $L$) separated by material of conductivity $\sigma$, starting from the line-charge field $\vec{E} = \lambda/(2\pi\epsilon_0 s)\,\hat{s}$; relate $I$ to the potential difference $V$.

*[Diagram: coaxial cylinders of inner radius a and outer radius b, length L.]*

**Solution.**

$$
\vec{E} = \frac{\lambda}{2\pi\epsilon_0 s}\hat{s}
$$

$$
I = \int \vec{J}\cdot d\vec{a} = \sigma\int \vec{E}\cdot d\vec{a} = \frac{\lambda\sigma}{2\pi\epsilon_0 s}\left(2\pi s L\right)
$$

$$
I = \frac{\lambda\sigma L}{\epsilon_0}
$$

$$
V = -\int_b^a \vec{E}\cdot d\vec{l} = \frac{\lambda}{2\pi\epsilon_0}\ln\left(\frac{b}{a}\right)
$$

$$
I = \frac{2\pi\sigma L}{\ln\left(\frac{b}{a}\right)}\,V
$$

### P31. Uniform Line Charge / Solenoid / Magnetized Cylinder and Sphere *(pp. 52–54)*

*[reference notes, not a worked problem]*

Quick-reference results: Gauss's law for a uniform line charge and inside a uniformly charged sphere; the on-axis solenoid integral with the $z = a\cot\theta$ substitution; nested and single solenoids; and the uniformly magnetized cylinder and sphere.

**Solution.**

Uniform line charge. *[Diagram: short cylinder of length $\ell$ enclosing a line charge $\lambda$.]*

$$
\oint \vec{E}\cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0}
$$

$$
\vec{E}\cdot 2\pi s L = \frac{\lambda L}{\epsilon_0}
$$

$$
\vec{E} = \frac{\lambda}{2\pi s\epsilon_0}\hat{s}
$$

Unif. Charged [sphere]. *[Diagram: sphere.]*

$$
\oint \vec{E}\cdot d\vec{a} = \frac{Q_{enc}}{\epsilon_0} = \frac{1}{\epsilon_0}\int \rho\,d\tau
$$

$$
\vec{E}\cdot 4\pi r^2 = \frac{\frac{4}{3}\pi R^3\rho}{\epsilon_0}
$$

*[sic: for the interior field the enclosed charge should be $\frac{4}{3}\pi r^3\rho$; the boxed result below corresponds to $r^3$]*

$$
\vec{E} = \frac{1}{3\epsilon_0}\rho r\,\hat{r}
$$

On-axis solenoid field. *[Diagram: cylinder of radius a with a circumferential current loop; right triangle with legs a and z, hypotenuse r, giving $z = a\cot\theta$.]*

$$
B = \frac{\mu_0 n I}{2}\int \frac{a^2}{\left(a^2 + z^2\right)^{3/2}}\,dz, \qquad dz = -\frac{a}{\sin^2\theta}\,d\theta
$$

Nested solenoids. *[Diagram: two coaxial solenoid windings drawn with oppositely directed winding arrows.]*

$$
B_{mid} = \mu_0 I n_2\,\hat{z}, \qquad B_{out} = 0
$$

$$
B_{in} = \mu_0 I\left(n_2 - n_1\right)\hat{z}
$$

Solenoid:

$$
B_{in} = \mu_0 n I\,\hat{z}, \qquad B_{out} = 0
$$

Cylinder. *[Diagram: cylinder with $\vec{M}$ along its axis.]*

$$
\vec{J}_b = \nabla\times M = 0, \qquad \vec{K}_b = M\times\hat{n} = M\hat{\phi}
$$

$$
B_{out} = 0, \qquad B = \mu_0 K_b = \mu_0 M
$$

$$
\vec{B} = \mu_0\vec{M}
$$

Magnetized Cylinder: Long $\rightarrow$ Solenoid; Short $\rightarrow$ Dipole.

Magnetized Sphere:

$$
\vec{B} = \frac{2}{3}\mu_0 M, \qquad \vec{m} = \frac{4}{3}\pi R^3\vec{M}
$$

### P32. Energy in Magnetic Fields *(pp. 55–56)*

Derivation of the energy stored in an inductor and in the magnetic field: from $dW/dt = -\mathcal{E}I$ to $W = \frac{1}{2}LI^2$, then rewriting via the vector potential and product rule 6 to $W = \frac{1}{2\mu_0}\int B^2\,d\tau$; the back of the page collects the electric and magnetic energy formulas side by side.

**Solution.**

$$
\frac{dW}{dt} = -\mathcal{E}I = LI\frac{dI}{dt}
$$

Boxed:

$$
W = \frac{1}{2}LI^2
$$

$$
\Phi = \int \vec{B}\cdot d\vec{a} = \int \left(\nabla\times\vec{A}\right)\cdot d\vec{a} = \oint \vec{A}\cdot d\vec{l}
$$

$$
LI = \oint \vec{A}\cdot d\vec{l}
$$

$$
W = \frac{1}{2}I\oint \vec{A}\cdot d\vec{l} = \frac{1}{2}\oint \left(\vec{A}\cdot\vec{I}\right)dl
$$

$$
W = \frac{1}{2}\int_{\forall}\left(\vec{A}\cdot\vec{J}\right)d\tau \qquad \left(\nabla\times\vec{B} = \mu_0\vec{J}\right)
$$

$$
W = \frac{1}{2\mu_0}\int \vec{A}\cdot\left(\nabla\times\vec{B}\right)d\tau
$$

product rule 6

$$
\nabla\cdot\left(\vec{A}\times\vec{B}\right) = \vec{B}\cdot\left(\nabla\times\vec{A}\right) - \vec{A}\cdot\left(\nabla\times\vec{B}\right)
$$

$$
\vec{A}\cdot\left(\nabla\times\vec{B}\right) \;\rightarrow\; \vec{B}\cdot\vec{B} - \nabla\cdot\left(\vec{A}\times\vec{B}\right)
$$

$$
W = \frac{1}{2\mu_0}\int_{All} B^2\,d\tau
$$

more on back:

$$
W_{elec} = \frac{1}{2}\int \left(V\rho\right)d\tau = \frac{\epsilon_0}{2}\int E^2\,d\tau
$$

$$
W_{mag} = \frac{1}{2}\int \left(\vec{A}\cdot\vec{J}\right)d\tau = \frac{1}{2\mu_0}\int B^2\,d\tau
$$

### P33. Ex 3.8 Uncharged Metal Sphere in Uniform E-field *(pp. 57–59)*

Griffiths Ex 3.8: an uncharged metal sphere of radius $R$ is placed in a uniform field $\vec{E} = E_0\hat{z}$; find the potential outside by separation of variables in Legendre polynomials, then the induced surface charge density.

*[Diagram: sphere of radius R; uniform field lines along $\hat{z}$ bending near the sphere, with induced + charge drawn on the top surface and − on the bottom, regions labeled $E_-$ and $E_+$; axes $\hat{z}$, $\hat{y}$.]*

**Solution.**

By symmetry x-y plane potential is zero, $V = 0$.

at large $z$

$$
V \rightarrow -E_0 z + C
$$

from xy-plane $V = 0$, so $C = 0$.

at $z = 0$, with $z = r\cos\theta$:

① $V = 0$ $(r = R)$

② $V \rightarrow -E_0 r\cos\theta$ $(r \gg R)$

1st case:

$$
V(r,\theta) = \sum_{\ell=0}^{\infty}\left(A_\ell r^\ell + \frac{B_\ell}{r^{\ell+1}}\right)P_\ell(\cos\theta)
$$

① at $z = 0$ focuses on the radial factor *[underbrace beneath $\left(A_\ell r^\ell + B_\ell/r^{\ell+1}\right)$]* so that $V = 0$ at $r = R$:

$$
A_\ell R^\ell + \frac{B_\ell}{R^{\ell+1}} = 0
$$

$$
B_\ell = -A_\ell R^{2\ell+1}
$$

$$
V(r,\theta) = \sum_{\ell=0}^{\infty} A_\ell\left(r^\ell - \frac{R^{2\ell+1}}{r^{\ell+1}}\right)P_\ell(\cos\theta)
$$

Condition ② for $r \gg R$: second term disappears, so that where $\left(V \approx -E_0 r\cos\theta\right)$

$$
V(r,\theta) \rightarrow \sum_{\ell=0}^{\infty} A_\ell r^\ell P_\ell(\cos\theta) = -E_0 r\cos\theta
$$

$$
A_0 r^0 P_0 + A_1 r P_1(\cos\theta) + A_2 r^2 P_2(\cos\theta) = -E_0 r\cos\theta
$$

Matching term by term ($\ell$ | LHS = RHS): for $\ell = 0$, $A_0 = 0$; for $\ell = 1$, $A_1 r\cos\theta = -E_0 r\cos\theta$; for $\ell = 2$, $A_2 r^2 P_2(\cos\theta) = 0$.

$$
A_1 r\cos\theta = -E_0 r\cos\theta
$$

$$
A_1 = -E_0 \qquad \text{so} \qquad \ell = 1
$$

Boxed:

$$
V(r,\theta) = -E_0\left(r - \frac{R^3}{r^2}\right)\cos\theta
$$

first-component: external field; 2nd-component: induced charge.

Induced Charge density

$$
\sigma(\theta) = -\epsilon_0\left.\frac{\partial V}{\partial r}\right|_{r=R}
$$

$$
-\frac{\partial V}{\partial r} = +E_0\left(1 + \frac{2R^3}{r^3}\right)\cos\theta
$$

$$
\sigma(\theta) = -\epsilon_0\left.\frac{\partial V}{\partial r}\right|_{r=R} = 3E_0\epsilon_0\cos\theta
$$

Boxed:

$$
\sigma(\theta) = 3E_0\epsilon_0\cos\theta
$$

### P34. Ex 3.9 Charge Density on Spherical Shell *(pp. 60–61)*

Find the potential inside and outside a spherical shell of radius $R$ carrying surface charge $\sigma_0(\theta) = k\cos\theta$, by separation of variables and the two boundary conditions at $r = R$. *[The header first reads "Ex 4.7 Homogeneous Linear Dielectric sphere in E-field", struck through and overwritten with this title; that dielectric problem is worked on pp. 62–65.]*

**Solution.**

General solutions inside and outside:

$$
V_{in} = \sum A_\ell r^\ell P_\ell(\cos\theta)
$$

$$
V_{out} = \sum \frac{B_\ell}{r^{\ell+1}} P_\ell(\cos\theta)
$$

*[Margin notes: $\nabla\cdot\vec{E} = \rho/\epsilon_0$; $E_\parallel$ continuous; $\vec{E} = -\nabla V$.]*

(ii) The derivative jump at the shell:

$$
\left.\frac{\partial V_{out}}{\partial r}\right|_R - \left.\frac{\partial V_{in}}{\partial r}\right|_R = -\frac{1}{\epsilon_0}\sigma_0(\theta)
$$

$$
\sum -\frac{(\ell+1)B_\ell}{R^{\ell+2}} P_\ell(\cos\theta) - \sum \ell A_\ell R^{\ell-1} P_\ell(\cos\theta) = -\frac{\sigma_0(\theta)}{\epsilon_0}
$$

(i) Continuity of the potential:

$$
V_{out}\big|_R = V_{in}\big|_R
$$

$$
\sum A_\ell R^\ell P_\ell(\cos\theta) = \sum \frac{B_\ell}{R^{\ell+1}} P_\ell(\cos\theta)
$$

Matching coefficients (the notes tag this line $\ell \neq 1$) *[sic: this match holds for every $\ell$, including $\ell = 1$]*:

$$
A_\ell R^\ell = \frac{B_\ell}{R^{\ell+1}} \;\to\; B_\ell = A_\ell R^{2\ell+1}
$$

Substituting into (ii):

$$
\sum -(\ell+1) A_\ell \frac{R^{2\ell+1}}{R^{\ell+2}} P_\ell(\cos\theta) - \ell A_\ell R^{\ell-1} P_\ell(\cos\theta) = -\frac{\sigma_0(\theta)}{\epsilon_0}
$$

$$
\sum_{\ell=0}^{\infty} (2\ell+1) A_\ell R^{\ell-1} P_\ell(\cos\theta) = \frac{\sigma_0(\theta)}{\epsilon_0}
$$

since $\sigma_0(\theta) \equiv k\cos\theta$:

($\ell = 1$)

$$
3A_1 \cos\theta = \frac{k\cos\theta}{\epsilon_0} \;\to\; A_1 = \frac{k}{3\epsilon_0}
$$

($\ell \neq 1$) $\to A_\ell \to$ zero. With $B_1 = A_1 R^3$, the boxed results:

$$
\boxed{V_{in} = \frac{k}{3\epsilon_0}\, r\cos\theta \qquad V_{out} = \frac{k}{3\epsilon_0}\frac{R^3\cos\theta}{r^2}}
$$

### P35. Ex 4.7 Homogeneous Linear Dielectric Sphere in E₀-Field *(pp. 62–65)*

A homogeneous linear dielectric sphere of radius $R$ (permittivity $\epsilon$, $\epsilon_r = \epsilon/\epsilon_0$) sits in an otherwise uniform field $\vec{E}_0$; find the potential everywhere and the field inside, by separation of variables with the dielectric boundary conditions.

**Solution.**

*[Diagram: vertical field lines labeled $E_0$ threading and bending around a sphere; short arrows inside the sphere indicate the uniform interior field.]*

Boundary conditions:

(i) $V_{in}\big|_{r=R} = V_{out}\big|_{r=R}$, (ii) $\epsilon \dfrac{\partial V_{in}}{\partial r}\Big|_{r=R} = \epsilon_0 \dfrac{\partial V_{out}}{\partial r}\Big|_{r=R}$, (iii) $V_{out} \to -E_0 r\cos\theta \quad (r \gg R)$.

$$
V_{in} = \sum_{\ell=0}^{\infty} A_\ell r^\ell P_\ell(\cos\theta)
$$

$$
V_{out} = -E_0 r\cos\theta + \sum_{\ell=0}^{\infty} \frac{B_\ell}{r^{\ell+1}} P_\ell(\cos\theta)
$$

(i):

$$
\sum_{\ell=0}^{\infty} A_\ell R^\ell P_\ell(\cos\theta) = -E_0 R\cos\theta + \sum_{\ell=0}^{\infty} \frac{B_\ell}{R^{\ell+1}} P_\ell(\cos\theta)
$$

let $\ell = 1$ (the $\cos\theta$'s cancel):

$$
A_1 R = -E_0 R + \frac{B_1}{R^2}
$$

($\ell \neq 1$):

$$
A_\ell R^\ell = \frac{B_\ell}{R^{\ell+1}}
$$

*[Margin: $\epsilon_r = \epsilon/\epsilon_0$.]*

(ii):

$$
\left.\frac{\partial V_{in}}{\partial r}\right|_{r=R} = \sum_{\ell=0}^{\infty} A_\ell\, \ell\, r^{\ell-1} P_\ell(\cos\theta)\bigg|_{r=R}
$$

$$
\left.\frac{\partial V_{out}}{\partial r}\right|_{r=R} = -E_0\cos\theta - \sum_{\ell=0}^{\infty} (\ell+1)\frac{B_\ell}{R^{\ell+2}} P_\ell(\cos\theta)
$$

$$
\epsilon \left.\frac{\partial V_{in}}{\partial r}\right|_{r=R} = \epsilon_0 \left.\frac{\partial V_{out}}{\partial r}\right|_{r=R}
$$

$$
\epsilon_r \sum_{\ell=0}^{\infty} \ell A_\ell R^{\ell-1} P_\ell(\cos\theta) = -E_0\cos\theta - \sum_{\ell=0}^{\infty} \frac{(\ell+1) B_\ell}{R^{\ell+2}} P_\ell(\cos\theta)
$$

($\ell = 1$), cancelling $\cos\theta$:

$$
\epsilon_r A_1 = -E_0 - \frac{2B_1}{R^3}
$$

($\ell \neq 1$), cancelling $P_\ell$:

$$
\epsilon_r \ell A_\ell R^{\ell-1} = -(\ell+1)\frac{B_\ell}{R^{\ell+2}}
$$

*[Margin bracket: $\ell = 0 \to B_\ell = 0$, $A_0 = 0$; $\ell \to \infty$: $A_\ell \to 0$, $B_\ell \to 0$.]*

where, from (i), $A_1 R = -E_0 R + \dfrac{B_1}{R^2}$, i.e. (cancelling one $R$ and correcting the exponent)

$$
\left(A_1 + E_0\right) = \frac{B_1}{R^3}
$$

$$
\epsilon_r A_1 = -E_0 - 2\left(A_1 + E_0\right)
$$

$$
\epsilon_r A_1 + 2A_1 = -3E_0
$$

$$
A_1\left(\epsilon_r + 2\right) = -3E_0
$$

$$
\boxed{A_1 = \frac{-3E_0}{2+\epsilon_r}}
$$

Returning to $\epsilon_r A_1 = -E_0 - 2B_1/R^3$ with this $A_1$ *[a false start beside it is scribbled out]*:

$$
\frac{-3E_0}{2+\epsilon_r}\,\epsilon_r = -E_0 - \frac{2B_1}{R^3}
$$

$$
\frac{3E_0\,\epsilon_r}{2+\epsilon_r} - E_0 = \frac{2B_1}{R^3}
$$

$$
E_0\left(\frac{3\epsilon_r}{2+\epsilon_r} - 1\right)\frac{R^3}{2} = B_1
$$

$$
E_0\left(\frac{3\epsilon_r - (2+\epsilon_r)}{2+\epsilon_r}\right)\frac{R^3}{2} = B_1
$$

$$
\frac{E_0 R^3}{2}\left(\frac{2\epsilon_r - 2}{\epsilon_r + 2}\right) = B_1
$$

cancelling the 2's:

$$
\boxed{B_1 = E_0 R^3 \left(\frac{\epsilon_r - 1}{\epsilon_r + 2}\right)}
$$

$$
\boxed{V_{in} = \frac{-3E_0}{2+\epsilon_r}\, r\cos\theta = -\frac{3E_0}{2+\epsilon_r}\, z}
$$

$\vec{E} = -\vec{\nabla}\vec{V}$:

$$
\boxed{\vec{E}_{in} = \frac{3E_0}{2+\epsilon_r}}
$$

### P36. Prob 4.23 *(p. 66)*

Find the field inside a sphere of linear dielectric (susceptibility $\chi_e$) in an otherwise uniform field $\vec{E}_0$ by successive approximations: each polarization produces a uniform field $-\vec{P}/3\epsilon_0$ inside the sphere, which repolarizes the material, and the series is summed. *[Title line mostly hidden under a folded page corner; only "4.23" is clearly legible.]*

**Solution.**

$$
\vec{P} = \epsilon_0 \chi_e \vec{E}
$$

$$
\vec{E}_1 = -\frac{1}{3\epsilon_0}\vec{P}_0 = -\frac{\chi_e}{3}\vec{E}_0
$$

$$
\vec{P}_1 = \epsilon_0 \chi_e \vec{E}_1 = -\epsilon_0 \frac{\chi_e^{\,2}}{3}\vec{E}_0
$$

$$
\vec{E}_2 = -\frac{1}{3\epsilon_0}\vec{P}_1 = \frac{\chi_e^{\,2}}{9}\vec{E}_0
$$

$$
\vec{E} = \vec{E}_0 + \vec{E}_1 + \vec{E}_2 + \dots = \sum_{n=0}^{\infty} \left(-\frac{\chi_e}{3}\right)^{n} \vec{E}_0
$$

where

$$
\sum_{n=0}^{\infty} x^n = \frac{1}{1-x}
$$

$$
\vec{E} = \frac{\vec{E}_0}{\left(1 + \dfrac{\chi_e}{3}\right)}
$$

### P37. Ex 6.1 Uniformly Magnetized Sphere *(p. 67)*

Find $\vec{B}$ of a uniformly magnetized sphere ($\vec{M}$ along $\hat{z}$, radius $R$) from its bound currents, using the equivalence to a spinning charged spherical shell.

**Solution.**

*[Diagram: sphere with a $\hat{z}$ axis and magnetization $\vec{M}$ inside.]*

$$
\vec{J}_b = \nabla\times\vec{M} = 0
$$

$$
\vec{K}_b = \vec{M}\times\hat{n} = M\sin\theta\,\hat{\phi}
$$

identical to spinning spherical shell

$$
\vec{K} = \sigma\vec{v} = \sigma\omega R \sin\theta\,\hat{\phi}, \qquad \sigma R \vec{\omega} \equiv \vec{M}
$$

where

$$
\vec{B} = \frac{2}{3}\mu_0\, \sigma R \vec{\omega}
$$

so then

$$
\boxed{\vec{B}_{in} = \frac{2}{3}\mu_0 \vec{M}} \qquad \boxed{\vec{B}_{out} = \vec{B}_{dipole}}
$$

$$
\vec{m} = V\vec{M} = \boxed{\frac{4}{3}\pi R^3 \vec{M} = \vec{m}}
$$

### P38. 6.15 Uniformly Magnetized Sphere *(pp. 68–69)*

The uniformly magnetized sphere ($\vec{M} = M\hat{z}$) again, now by separation of variables for the magnetic scalar potential $W$: since there is no free current, $\vec{H} = -\nabla W$, with the jump in $\partial W/\partial r$ set by $M_\perp$.

**Solution.**

$$
\nabla\times\vec{H} = \vec{J}_f + \frac{\partial \vec{D}}{\partial t}
$$

(the $\partial\vec{D}/\partial t$ term is crossed out — zero here), and

$$
\vec{B} = -\mu_0\nabla\phi_m, \qquad \phi_m \equiv W
$$

*[Margin: $\vec{B} = \mu_0(\vec{H}+\vec{M})$; $\vec{B} = \mu\vec{H}$.]*

$$
W_{in} = \sum A_\ell r^\ell P_\ell(\cos\theta), \qquad W_{out} = \sum \frac{B_\ell}{r^{\ell+1}} P_\ell(\cos\theta)
$$

(i)

$$
W_{in}\big|_R = W_{out}\big|_R
$$

(ii)

$$
-\left.\frac{\partial W_{out}}{\partial r}\right|_R + \left.\frac{\partial W_{in}}{\partial r}\right|_R = M_\perp = M\,\hat{z}\cdot\hat{r} = M\cos\theta
$$

(i), cancelling $P_\ell(\cos\theta)$ on both sides:

$$
A_\ell R^\ell = \frac{B_\ell}{R^{\ell+1}} \;\to\; B_\ell = A_\ell R^{2\ell+1}
$$

(ii):

$$
\frac{B_\ell(\ell+1)}{R^{\ell+2}} P_\ell(\cos\theta) + A_\ell\, \ell\, R^{\ell-1} P_\ell(\cos\theta) = M\cos\theta
$$

$$
A_\ell \frac{R^{2\ell+1}}{R^{\ell+2}}(\ell+1) P_\ell(\cos\theta) + A_\ell\, \ell\, R^{\ell-1} P_\ell(\cos\theta) = M\cos\theta
$$

$\ell \neq 1$:

$$
A_\ell \left[ R^{\ell-1}(2\ell+1) P_\ell(\cos\theta) \right] = 0 \;\to\; A_\ell = 0
$$

$\ell = 1$ (the $\cos\theta$'s cancel, $R^0 = 1$):

$$
A_1 R^0 (2)\cos\theta + A_1 R^0 \cos\theta = M\cos\theta
$$

$$
2A_1 + A_1 = M \qquad A_1 = \frac{M}{3}
$$

$$
W_{in} = \frac{M}{3} r\cos\theta = \frac{M}{3} z
$$

$$
\vec{H}_{in} = -\nabla W_{in} = -\frac{M}{3}\hat{z}
$$

*[Margin: $\vec{B} \approx \mu_0\vec{H}$; $\vec{B} = -\mu_0\nabla\phi_m$; $\mu_0\vec{H} = -\mu_0\nabla W$; $\vec{H}_{in} \approx -\nabla W_{in}$.]*

$$
\vec{B} = \mu_0\left(\vec{H} + \vec{M}\right) = \mu_0\left(-\frac{1}{3}M + M\right)\hat{z} = \frac{2}{3}\mu_0\vec{M}
$$

$$
\boxed{\vec{B}_{in} = \frac{2}{3}\mu_0 M \hat{z}}
$$

### P39. 6.18 Uniformly Magnetized Sphere in B₀ *(pp. 70–74)*

A sphere of linear magnetic material (permeability $\mu$, susceptibility $\chi_m$; the header calls it "uniformly magnetized") in an otherwise uniform field $\vec{B}_0 = B_0\hat{z}$: find the new field inside. Solved first as a boundary-value problem for the magnetic scalar potential $W$, then re-derived by successive approximation of the magnetization.

**Solution.**

$$
\vec{B} = -\mu_0\nabla\phi_m, \qquad \phi_m \equiv W, \qquad \vec{H}_{in} \approx -\nabla W_{in}
$$

$$
V_{in} = \sum A_\ell r^\ell P_\ell(\cos\theta) \qquad V_{out} = \sum \frac{B_\ell}{r^{\ell+1}} P_\ell(\cos\theta)
$$

b.c.s:

(i)

$$
W_{in}\big|_R = W_{out}\big|_R
$$

(ii)

$$
\mu \left.\frac{\partial W_{in}}{\partial r}\right|_R = \mu_0 \left.\frac{\partial W_{out}}{\partial r}\right|_R
$$

(iii) for $r \gg R$:

$$
\vec{B} \to B_0\hat{z}\,, \qquad \vec{H} \approx \frac{1}{\mu_0}\vec{B} = \frac{B_0}{\mu_0}\hat{z}
$$

*[Margin: $H \approx -\nabla W$, so $W \approx -\int \vec{B}\, dz$.]*

$$
W_{out} \to -\frac{1}{\mu_0} B_0\, r\cos\theta
$$

$$
W_{out} = -\frac{1}{\mu_0} B_0\, r\cos\theta + \sum \frac{B_\ell}{r^{\ell+1}} P_\ell(\cos\theta)
$$

(i):

$$
\sum A_\ell R^\ell P_\ell(\cos\theta) = -\frac{1}{\mu_0} B_0 R \cos\theta + \sum \frac{B_\ell}{R^{\ell+1}} P_\ell(\cos\theta)
$$

($\ell \neq 1$), cancelling $P_\ell$:

$$
A_\ell R^\ell = \frac{B_\ell}{R^{\ell+1}}
$$

$$
A_\ell R^{2\ell+1} = B_\ell \qquad (1)
$$

($\ell = 1$), cancelling $\cos\theta$, then multiplying through by $R^2$:

$$
A_1 R = -\frac{1}{\mu_0} B_0 R + \frac{B_1}{R^2}
$$

$$
A_1 R^3 = -\frac{1}{\mu_0} B_0 R^3 + B_1 \qquad (2)
$$

(ii):

$$
\mu\left(A_\ell\, \ell\, R^{\ell-1} P_\ell(\cos\theta)\right) - \mu_0\left[-\frac{1}{\mu_0} B_0 \cos\theta - \frac{(\ell+1) B_\ell}{R^{\ell+2}} P_\ell(\cos\theta)\right] = 0
$$

($\ell \neq 1$):

$$
\mu A_\ell\, \ell\, R^{\ell-1} P_\ell + \mu_0 \left[\frac{(\ell+1) B_\ell}{R^{\ell+2}} P_\ell\right] = 0
$$

using (1):

$$
\mu A_\ell\, \ell\, R^{\ell-1} + \mu_0 \frac{(\ell+1)}{R^{\ell+2}} A_\ell R^{2\ell+1} = 0
$$

*[a line is scribbled out]*

$$
A_\ell \left[\mu\, \ell\, R^{\ell-1} + \mu_0 (\ell+1) R^{\ell-1}\right] = 0
$$

$$
A_\ell = 0
$$

(ii) ($\ell = 1$), cancelling $\cos\theta$:

$$
\mu A_1 \cos\theta + \mu_0 \left[\frac{1}{\mu_0} B_0 \cos\theta + \frac{(1+1) B_1}{R^3}\cos\theta\right] = 0
$$

$$
\mu A_1 + B_0 + \mu_0 \frac{2 B_1}{R^3} = 0 \qquad (3)
$$

From (2):

$$
B_1 = A_1 R^3 + \frac{B_0}{\mu_0} R^3 \;\to\; B_1 = R^3\left(A_1 + \frac{B_0}{\mu_0}\right)
$$

(2) $\to$ (3):

$$
\mu A_1 + B_0 + \frac{2\mu_0}{R^3} R^3 \left(A_1 + \frac{B_0}{\mu_0}\right) = 0
$$

$$
\mu A_1 + B_0 + 2\mu_0 A_1 + 2 B_0 = 0
$$

$$
A_1 \left(\mu + 2\mu_0\right) + 3 B_0 = 0
$$

$$
A_1 = \frac{-3}{\mu + 2\mu_0} B_0
$$

$$
W_{in} = \left(\frac{-3}{\mu + 2\mu_0}\right) B_0\, r\cos\theta = \frac{-3}{\mu+2\mu_0} B_0\, z
$$

$$
\vec{H}_{in} \approx -\nabla W_{in} \;\to\; \frac{+3}{\mu+2\mu_0} B_0 \hat{z}
$$

$$
\vec{B} = \mu\vec{H} \;\to\; \frac{3\mu}{\mu + 2\mu_0} B_0 \hat{z}
$$

With $\mu_0\mu_r = \mu$ and $\mu_r = 1 + \chi_m$ *[a scratched-out expression between]*, i.e. $\mu = \mu_0(1+\chi_m)$:

$$
\vec{B} = \frac{3\mu_0\left(1+\chi_m\right)}{\mu_0\left(1+\chi_m\right) + 2\mu_0} B_0 \hat{z}
$$

cancelling the $\mu_0$'s:

$$
\boxed{\vec{B} = \frac{1+\chi_m}{\left(1+\dfrac{\chi_m}{3}\right)} B_0 \hat{z}}
$$

Second method (below a dividing line): successive magnetization.

$$
\vec{M} = \chi_m \vec{H}\,, \qquad \vec{M}_0 = \chi_m \vec{H}_0
$$

*[Margin: $\dfrac{\vec{B}}{\mu_0\mu_r} = \vec{H}$; $\vec{H} = \dfrac{\vec{B}}{\mu_0(1+\chi_m)}$.]*

$$
\vec{M}_0 = \frac{\chi_m}{\mu_0\left(1+\chi_m\right)} \vec{B}_0\,, \qquad K \equiv \frac{\chi_m}{1+\chi_m}
$$

$$
\vec{B}_1 \equiv \vec{B}_{in} = \frac{2}{3}\mu_0 \vec{M}_0 = \frac{2}{3}\frac{\chi_m}{1+\chi_m}\vec{B}_0 = \frac{2}{3} K \vec{B}_0
$$

$\vec{B}_1 = \frac{2}{3} K \vec{B}_0$, which magnetizes an additional amt.

$$
\vec{B}_2 = \frac{2}{3}\mu_0 \vec{M}_1 = \frac{2}{3} K \vec{B}_1 = \left(\frac{2K}{3}\right)^2 \vec{B}_0
$$

$$
\vec{B} = \vec{B}_0 + \vec{B}_1 + \vec{B}_2 + \dots
$$

$$
\vec{B} = \vec{B}_0 + \left(\frac{2}{3}K\right)\vec{B}_0 + \left(\frac{2K}{3}\right)^2 \vec{B}_0
$$

$$
\sum_{n=0}^{\infty} x^n = \frac{1}{1-x} \qquad \text{where } x \equiv \frac{2}{3}K
$$

$$
\vec{B} = \frac{\vec{B}_0}{1 - \frac{2}{3}K} = \frac{\vec{B}_0}{1 - \frac{2}{3}\left(\frac{\chi_m}{1+\chi_m}\right)}
$$

$$
\boxed{\vec{B} = \left(\frac{1+\chi_m}{1+\dfrac{\chi_m}{3}}\right)\vec{B}_0} \qquad \left(\vec{B}_0 = B_0\hat{z}\right)
$$

### P40. Prob 4.5 Torque on Perfect Dipoles *(p. 75)*

Two perfect dipoles a distance $r$ apart: $\vec{p}_1$ points perpendicular to the line joining them, $\vec{p}_2$ points along that line. Find the torque on $\vec{p}_2$ due to $\vec{p}_1$, and the torque on $\vec{p}_1$ due to $\vec{p}_2$.

**Solution.**

*[Diagram: $\vec{p}_1$ pointing up at the left; $\vec{p}_2$ a distance $r$ to the right, pointing along the line joining them.]*

$$
\vec{E}_{dip} = \frac{p}{4\pi\epsilon_0 r^3}\left(2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)
$$

Field of $\vec{p}_1$ @ $\vec{p}_2$: $\theta_{p_2} = \dfrac{\pi}{2}$. *[Small diagram: $\vec{p}_1$ pointing up, the field point a distance $r$ along the horizontal, angle $\pi/2$ marked.]*

$$
\vec{E}_1 = \frac{p_1}{4\pi\epsilon_0 r^3}\left(2\cos\left(\frac{\pi}{2}\right)\hat{r} + \sin\left(\frac{\pi}{2}\right)\hat{\theta}\right)
$$

(the first term vanishes)

$$
\vec{E}_1 = \frac{p_1}{4\pi\epsilon_0}\frac{1}{r^3}\,\hat{\theta}
$$

Torque on $\vec{p}_2$:

$$
\vec{N}_2 = \vec{p}_2 \times \vec{E}_1 = p_2 E_1 \sin(90) = p_2 E_1
$$

$$
\vec{N}_2 = \frac{p_1 p_2}{4\pi\epsilon_0 r^3} \quad \text{into the page}
$$

Field of $\vec{p}_2$ @ $\vec{p}_1$ $\left(\theta = \pi\right)$: *[Small diagram: the angle from $\vec{p}_2$'s axis back to $\vec{p}_1$ is $\pi$.]*

$$
\vec{E}_2 = \frac{p_2}{4\pi\epsilon_0 r^3}\left(-2\hat{r}\right)
$$

$$
\vec{N}_1 = \frac{2 p_1 p_2}{4\pi\epsilon_0 r^3}
$$

### P41. P 4.6 Dipole Method of Images *(p. 76)*

A perfect dipole $\vec{p}$ sits a height $z$ above an infinite grounded conducting plane, tilted an angle $\theta$ from the perpendicular; find the torque on $\vec{p}$ by replacing the plane with an image dipole a distance $2z$ away.

**Solution.**

*[Diagram: dipole $\vec{p}$ at angle $\theta$ a height $z$ above a hatched grounded plane; an arrow points to the image construction, with the mirrored image dipole (its $+$ and $-$ ends marked) below the plane.]*

*[Diagram: image dipole $\vec{p}_i$ a distance $r \equiv 2z$ below the real dipole $\vec{p}$; each makes angle $\theta$ with the line joining them.]*

$$
\vec{E}_{dip} = \frac{p}{4\pi\epsilon_0 \left(r^3\right)}\left(2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)
$$

$$
\vec{p} = p\left(\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)
$$

$$
\vec{N} = \vec{p}\times\vec{E}_i = \frac{p^2}{4\pi\epsilon_0 (2z)^3}\left[\left(\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)\times\left(2\cos\theta\,\hat{r} + \sin\theta\,\hat{\theta}\right)\right]
$$

$$
\vec{N} = \frac{p^2 \sin\theta\cos\theta}{4\pi\epsilon_0 \left(2z\right)^3}\left(-\hat{\phi}\right) \quad \text{out of page}
$$

$$
\sin\theta\cos\theta = \frac{1}{2}\sin 2\theta
$$

$$
\boxed{N = \frac{p^2 \sin 2\theta}{4\pi\epsilon_0\, 16 z^3} \quad \text{out of page}}
$$

$0 < \theta < \dfrac{\pi}{2}$: C.C.W. $\qquad \dfrac{\pi}{2} \to \pi$: C.W.

### P42. Prob 3.28 Multipole Expansion of Loop *(pp. 77–78)*

Compute the dipole moment of the surface charge $\sigma = K\cos\theta$ on a sphere of radius $R$ (the shell of Ex 3.9) and the resulting dipole potential. *[Header: a struck-out word is overwritten with "loop", and the title trails "w/" plus a cursive symbol read as $z$; the notes call the distribution a "loop" throughout, but the object worked is the spherical shell.]*

**Solution.**

$$
\vec{p} \equiv \int \vec{r}\,' \rho(\vec{r}\,')\, d\tau' \qquad \vec{p} = q\vec{d}
$$

$\vec{E}$ of loop is $\hat{z}$ due to symmetry, so

$$
\vec{p} = p\hat{z}
$$

$$
p = \int z \rho\, d\tau \qquad p = \int z \sigma\, da
$$

*[Margin: $\rho \sim K\cos\theta$; $z = R\cos\theta$; $da = R^2 \sin\theta\, d\theta\, d\phi$.]*

$$
p = \int_0^{\pi} R\cos\theta\, K\cos\theta\, R^2 \sin\theta\, d\theta \int_0^{2\pi} d\phi
$$

$$
p = 2\pi R^3 K \int_0^{\pi} \cos^2\theta \sin\theta\, d\theta
$$

$$
u \equiv \cos\theta \qquad du = -\sin\theta\, d\theta
$$

$$
\int_0^{\pi} \cos^2\theta \sin\theta\, d\theta = -\int u^2\, du \;\to\; -\frac{u^3}{3}
$$

$$
\to\; -\frac{\cos^3\theta}{3}\Bigg|_0^{\pi} = \frac{-(-1)^3}{3} + \frac{1}{3} = \frac{2}{3}
$$

$$
p = \frac{4}{3}\pi R^3 K \qquad \boxed{\vec{p} = \frac{4\pi R^3 K}{3}\,\hat{z}}
$$

$$
V_{dip} = \frac{1}{4\pi\epsilon_0} \frac{\vec{p}\cdot\hat{r}}{r^2}
$$

Cancelling the $4\pi$'s:

$$
V_{dip} = \frac{1}{4\pi\epsilon_0}\frac{4\pi R^3}{3}\frac{K\cos\theta}{r^2} = \boxed{\frac{K R^3 \cos\theta}{3\epsilon_0 r^2}} = V_{dip}
$$

*[The final label is squeezed against the page edge; it matches the exact $V_{out}$ found in Ex 3.9.]*

### P43. Prob 7.8 *(p. 79)*

A square loop of side $a$ sits a distance $s$ above a long straight wire carrying current $I$. (a) Find the flux of $\vec{B}$ through the loop; (b) find the EMF $\mathcal{E}$ generated by pulling the loop directly away from the wire; (c) find $\mathcal{E}$ if the loop instead moves to the right at speed $v$.

*[Diagram: square loop of side $a$, its bottom edge a distance $s$ above a long horizontal wire carrying current $I$ to the right.]*

**Solution.**

$$
\vec{B} = \frac{\mu_0 I}{2\pi s}\,\hat{\phi}
\qquad
\Phi = \int \vec{B}\cdot d\vec{a}
$$

a)

$$
\Phi = \frac{\mu_0 I}{2\pi}\int_{s}^{s+a}\frac{1}{s}\,a\,ds = \frac{\mu_0 I a}{2\pi}\ln\left(\frac{s+a}{s}\right)
$$

b)

$$
\mathcal{E} = -\frac{d\Phi}{dt} = -\frac{\mu_0 I a}{2\pi}\left(\frac{ds}{dt}\frac{1}{s+a} - \frac{1}{s}\frac{ds}{dt}\right)
$$

$$
\frac{ds}{dt} = v
$$

$$
\mathcal{E} = -\frac{\mu_0 I a v}{2\pi}\left(\frac{\cancel{s}-(\cancel{s}+a)}{s(s+a)}\right) = \frac{\mu_0 I a^2 v}{2\pi s(s+a)}
$$

counterclockwise

c)

$$
\mathcal{E} = 0 \qquad \Phi = \text{constant}
$$

### P44. Proof: $\mathcal{E} = -\frac{d\Phi}{dt}$ *(p. 80)*

Proof of the flux rule for motional EMF: for a loop moving through a magnetic field, the EMF equals minus the rate of change of the flux. Here $\vec{v}$ is the loop's velocity, $\vec{u}$ the charge velocity along the wire, and $\vec{w} = \vec{v}+\vec{u}$ the total charge velocity.

**Solution.**

$$
d\Phi = \Phi(t+dt) - \Phi(t) = \Phi_{\text{ribbon}} = \int_{\text{ribbon}}\vec{B}\cdot d\vec{a}
$$

$$
\vec{w} = \vec{v} + \vec{u}
$$

$$
d\vec{a} = \left(\vec{v}\times d\vec{l}\,\right)dt
$$

$$
\frac{d\Phi}{dt} = \oint \vec{B}\cdot\left(\vec{v}\times d\vec{l}\,\right)
\qquad \left(\vec{u} \text{ is } \parallel \text{ to } d\vec{l}\,\right)
$$

so

$$
\frac{d\Phi}{dt} = \oint \vec{B}\cdot\left(\vec{w}\times d\vec{l}\,\right)
$$

Scalar triple-product can be rewritten

$$
\vec{B}\cdot\left(\vec{w}\times d\vec{l}\,\right) = -\left(\vec{w}\times\vec{B}\right)\cdot d\vec{l}
$$

$$
\frac{d\Phi}{dt} = -\oint \underbrace{\left(\vec{w}\times\vec{B}\right)}_{(\equiv\,\vec{f}_{\text{mag}})}\cdot\,d\vec{l} = -\oint \vec{f}_{\text{mag}}\cdot d\vec{l}
$$

$$
\boxed{\,\mathcal{E} = -\frac{d\Phi}{dt}\,}
$$

### P45. Electric Dipole Radiation *(pp. 81–84)*

Derivation of the potentials, radiation-zone fields, and radiated power of an oscillating electric dipole: charges $\pm q(t) = \pm q_0\cos(\omega t)$ separated by $d$ on the $z$-axis, so $\vec{p}(t) = p_0\cos(\omega t)\,\hat{z}$ with $p_0 \equiv q_0 d$, carried through the three standard approximations ($d\ll r$, $d\ll c/\omega$, $r\gg c/\omega$) to $\langle\vec{S}\rangle$ and $\langle P\rangle$.

**Solution.**

$$
\vec{p}(t) = p_0\cos(\omega t)\,\hat{z} \qquad q(t) = q_0\cos(\omega t) \qquad p_0 \equiv q_0 d
$$

$$
V_{\text{ret}} = \frac{1}{4\pi\epsilon_0}\left\{\frac{q_0\cos[\omega(t-\mathfrak{r}_+/c)]}{\mathfrak{r}_+} - \frac{q_0\cos[\omega(t-\mathfrak{r}_-/c)]}{\mathfrak{r}_-}\right\}
$$

$$
\mathfrak{r}_\pm = \sqrt{r^2 \mp rd\cos\theta + \left(\frac{d}{2}\right)^2}
$$

approx. 1: $d \ll r$

$$
\mathfrak{r}_\pm \approx r\left(1 \mp \frac{d}{2r}\cos\theta\right)
$$

$$
\frac{1}{\mathfrak{r}_\pm} \approx \frac{1}{r}\left(1 \pm \frac{d}{2r}\cos\theta\right)
\tag{1}
$$

$$
\begin{aligned}
\cos[\omega(t-\mathfrak{r}_\pm/c)] &\approx \cos\left[\omega(t-r/c) \pm \frac{\omega d}{2c}\cos\theta\right] \\
&= \cos[\omega(t-r/c)]\cos\left(\frac{\omega d}{2c}\cos\theta\right) \mp \sin[\omega(t-r/c)]\sin\left(\frac{\omega d}{2c}\cos\theta\right)
\end{aligned}
$$

approx 2: $d \ll \frac{c}{\omega}$, with $\lambda = \frac{2\pi c}{\omega}$, $\to\ d \ll \frac{\lambda}{2\pi}$

$$
\cos[\omega(t-\mathfrak{r}_\pm/c)] \approx \cos[\omega(t-r/c)] \mp \frac{\omega d}{2c}\cos\theta\,\sin[\omega(t-r/c)]
\tag{2}
$$

(1), (2) $\to V_{\text{ret}}$:

$$
V = \frac{p_0\cos\theta}{4\pi\epsilon_0\, r}\left\{-\frac{\omega}{c}\sin[\omega(t-r/c)] + \frac{1}{r}\cos[\omega(t-r/c)]\right\}
$$

approx 3: $\left(r \gg \frac{c}{\omega}\right)$, $r \gg \lambda$

$$
\boxed{\,V = -\frac{p_0\omega}{4\pi\epsilon_0 c}\left(\frac{\cos\theta}{r}\right)\sin[\omega(t-r/c)]\,}
$$

$$
\vec{I}(t) = \frac{dq}{dt}\,\hat{z} = -q_0\omega\sin(\omega t)\,\hat{z}
$$

$$
\vec{A}(\vec{r},t) = \frac{\mu_0}{4\pi}\int_{-d/2}^{d/2}\frac{-q_0\omega\sin[\omega(t-\mathfrak{r}/c)]}{\mathfrak{r}}\,\hat{z}\,dz
\qquad \text{(margin: } p_0 = q_0 d\text{)}
$$

$$
\boxed{\,\vec{A} = -\frac{\mu_0 p_0 \omega}{4\pi r}\sin[\omega(t-r/c)]\,\hat{z}\,}
$$

$$
\nabla V = \frac{\partial V}{\partial r}\hat{r} + \frac{1}{r}\frac{\partial V}{\partial\theta}\hat{\theta} \approx \frac{p_0\omega^2}{4\pi\epsilon_0 c^2}\left(\frac{\cos\theta}{r}\right)\cos[\omega(t-r/c)]\,\hat{r}
$$

$$
\frac{\partial\vec{A}}{\partial t} = -\frac{\mu_0 p_0\omega^2}{4\pi r}\cos[\omega(t-r/c)]\left(\cos\theta\,\hat{r} - \sin\theta\,\hat{\theta}\right)
$$

$$
\boxed{\,\vec{E} = -\nabla V - \frac{\partial\vec{A}}{\partial t} = -\frac{\mu_0 p_0\omega^2}{4\pi}\left(\frac{\sin\theta}{r}\right)\cos[\omega(t-r/c)]\,\hat{\theta}\,}
$$

$$
\nabla\times\vec{A} = \frac{1}{r}\left[\frac{\partial}{\partial r}\left(rA_\theta\right) - \frac{\partial A_r}{\partial\theta}\right]\hat{\phi}
= -\frac{\mu_0 p_0\omega}{4\pi r}\left\{\frac{\omega}{c}\sin\theta\cos[\omega(t-r/c)] + \frac{\sin\theta}{r}\sin[\omega(t-r/c)]\right\}\hat{\phi}
$$

$$
\boxed{\,\vec{B} = \nabla\times\vec{A} = -\frac{\mu_0 p_0\omega^2}{4\pi c}\left(\frac{\sin\theta}{r}\right)\cos[\omega(t-r/c)]\,\hat{\phi}\,}
$$

$$
\vec{S} = \frac{1}{\mu_0}\left(\vec{E}\times\vec{B}\right) = \frac{\mu_0}{c}\left\{\frac{p_0\omega^2}{4\pi}\frac{\sin\theta}{r}\cos[\omega(t-r/c)]\right\}^2\hat{r}
$$

$$
\langle\vec{S}\rangle = \left(\frac{\mu_0 p_0^2\omega^4}{32\pi^2 c}\right)\frac{\sin^2\theta}{r^2}\,\hat{r}
$$

$$
\langle P\rangle = \int\langle\vec{S}\rangle\cdot d\vec{a} = \frac{\mu_0 p_0^2\omega^4}{32\pi^2 c}\int\frac{\sin^2\theta}{r^2}\,r^2\sin\theta\,d\theta\,d\phi
$$

$$
\langle P\rangle = \frac{\mu_0 p_0^2\omega^4}{12\pi c}
$$

### P46. Magnetic Dipole Radiation *(pp. 85–88)*

The same program for an oscillating magnetic dipole: a wire loop of radius $b$ in the $xy$-plane carrying $I(t) = I_0\cos(\omega t)$, so $\vec{m}(t) = \pi b^2 I(t)\,\hat{z} = m_0\cos(\omega t)\,\hat{z}$; the vector potential is expanded through the three approximations, then the radiation fields, $\langle\vec{S}\rangle$, $\langle P\rangle$, and the ratio $P_{\text{mag}}/P_{\text{ele}}$.

*[Diagram: circular loop of radius $b$ in the $xy$-plane; field point at $\vec{r}$ (polar angle $\theta$ from $\hat{z}$, drawn above the $x$-axis, i.e. in the $xz$-plane); source element $d\vec{l}\,'$ on the loop at azimuth $\phi'$, separation $\mathfrak{r}$ to the field point; $\psi$ is the angle between $\vec{r}$ and $\vec{b}$.]*

**Solution.**

$$
I(t) = I_0\cos(\omega t)
$$

$$
\vec{m}(t) = \pi b^2\, I(t)\,\hat{z} = m_0\cos(\omega t)\,\hat{z} \qquad m_0 \equiv \pi b^2 I_0
$$

$$
\vec{A}(\vec{r},t) = \frac{\mu_0}{4\pi}\int\frac{I_0\cos[\omega(t-\mathfrak{r}/c)]}{\mathfrak{r}}\,d\vec{l}\,'
$$

$\vec{r}$ is above $\hat{x}$ so $\vec{A} = A\,\hat{y}$ ($x$-axis cancels)

$$
\vec{A}(\vec{r},t) = \frac{\mu_0 I_0 b}{4\pi}\,\hat{y}\int_0^{2\pi}\frac{\cos[\omega(t-\mathfrak{r}/c)]}{\mathfrak{r}}\cos\phi'\,d\phi'
\tag{1}
$$

law of cosines

$$
\mathfrak{r} = \sqrt{r^2 + b^2 - 2rb\cos\psi}
$$

$$
\vec{r} = r\sin\theta\,\hat{x} + r\cos\theta\,\hat{z}
$$

$$
\vec{b} = b\cos\phi'\,\hat{x} + b\sin\phi'\,\hat{y}
$$

$$
\vec{r}\cdot\vec{b} = rb\cos\psi = rb\sin\theta\cos\phi'
$$

$$
\mathfrak{r} = \sqrt{r^2 + b^2 - 2rb\sin\theta\cos\phi'}
$$

approx 1: $b \ll r$

$$
\mathfrak{r} \approx r\left(1 - \frac{b}{r}\sin\theta\cos\phi'\right)
$$

$$
\frac{1}{\mathfrak{r}} \approx \frac{1}{r}\left(1 + \frac{b}{r}\sin\theta\cos\phi'\right)
\tag{2}
$$

$$
\begin{aligned}
\cos[\omega(t-\mathfrak{r}/c)] &\approx \cos\left[\omega(t-r/c) + \frac{\omega b}{c}\sin\theta\cos\phi'\right] \\
&= \cos[\omega(t-r/c)]\cos\left(\frac{\omega b}{c}\sin\theta\cos\phi'\right) - \sin[\omega(t-r/c)]\sin\left(\frac{\omega b}{c}\sin\theta\cos\phi'\right)
\end{aligned}
$$

approx 2: $b \ll \frac{c}{\omega}$

$$
\cos[\omega(t-\mathfrak{r}/c)] \approx \cos[\omega(t-r/c)] - \frac{\omega b}{c}\sin\theta\cos\phi'\,\sin[\omega(t-r/c)]
\tag{3}
$$

(2), (3) $\to$ (1) to the 1st order

$$
\vec{A}(\vec{r},t) \approx \frac{\mu_0 I_0 b}{4\pi r}\,\hat{y}\int_0^{2\pi}\left\{\cos[\omega(t-r/c)] + b\sin\theta\cos\phi'\left(\frac{1}{r}\cos[\omega(t-r/c)] - \frac{\omega}{c}\sin[\omega(t-r/c)]\right)\right\}\cos\phi'\,d\phi'
$$

1st term $\to 0$

$$
\int_0^{2\pi}\cos\phi'\,d\phi' = 0
$$

2nd term

$$
\int_0^{2\pi}\cos^2\phi'\,d\phi' = \pi
$$

$$
\vec{A} = \frac{\mu_0 m_0}{4\pi}\left(\frac{\sin\theta}{r}\right)\left\{\frac{1}{r}\cos[\omega(t-r/c)] - \frac{\omega}{c}\sin[\omega(t-r/c)]\right\}\hat{\phi}
$$

Static ($\omega = 0$) gives mag. dipole

$$
\vec{A} = \frac{\mu_0}{4\pi}\frac{m_0\sin\theta}{r^2}\,\hat{\phi}
$$

approx. 3: $\left(r \gg \frac{c}{\omega}\right) \;\to\; \frac{\omega}{c} \gg \frac{1}{r}$

$$
\boxed{\,\vec{A} = -\frac{\mu_0 m_0 \omega}{4\pi c}\left(\frac{\sin\theta}{r}\right)\sin[\omega(t-r/c)]\,\hat{\phi}\,}
$$

$$
\boxed{\,\vec{E} = -\frac{\partial\vec{A}}{\partial t} = \frac{\mu_0 m_0\omega^2}{4\pi c}\left(\frac{\sin\theta}{r}\right)\cos[\omega(t-r/c)]\,\hat{\phi}\,}
$$

$$
\boxed{\,\vec{B} = \nabla\times\vec{A} = -\frac{\mu_0 m_0\omega^2}{4\pi c^2}\left(\frac{\sin\theta}{r}\right)\cos[\omega(t-r/c)]\,\hat{\theta}\,}
$$

$$
\vec{S} = \frac{1}{\mu_0}\left(\vec{E}\times\vec{B}\right) = \frac{\mu_0}{c}\left\{\frac{m_0\omega^2}{4\pi c}\left(\frac{\sin\theta}{r}\right)\cos[\omega(t-r/c)]\right\}^2\hat{r}
$$

$$
\langle\vec{S}\rangle = \left(\frac{\mu_0 m_0^2\omega^4}{32\pi^2 c^3}\right)\frac{\sin^2\theta}{r^2}\,\hat{r}
$$

$$
\langle P\rangle = \frac{\mu_0 m_0^2\omega^4}{12\pi c^3}
$$

$$
\frac{P_{\text{mag}}}{P_{\text{ele}}} = \left(\frac{m_0}{p_0 c}\right)^2
\qquad
m_0 = \pi b^2 I_0,\quad p_0 = q_0 d,\quad I_0 = q_0\omega,\quad d = \pi b
$$

$$
\frac{P_{\text{mag}}}{P_{\text{ele}}} = \left(\frac{\omega b}{c}\right)^2
$$

### P47. Prob 5.28 — Coulomb Gauge *(pp. 89–91)*

For the magnetostatic vector potential $\vec{A}(\vec{r}) = \frac{\mu_0}{4\pi}\int \frac{\vec{J}(\vec{r}\,')}{\mathfrak{r}}\,d\tau'$, show the three Coulomb-gauge properties: $\nabla\cdot\vec{A}=0$, $\nabla\times\vec{A}=\vec{B}$, and $\nabla^2\vec{A} = -\mu_0\vec{J}$, where $\vec{B}$ is the Biot–Savart field.

**Solution.**

$$
\vec{A}(\vec{r}) = \frac{\mu_0}{4\pi}\int\frac{\vec{J}(\vec{r}\,')}{\mathfrak{r}}\,d\tau'
$$

$$
\nabla\cdot\vec{A} = 0 \qquad \nabla\times\vec{A} = \vec{B} \qquad \nabla^2\vec{A} = -\mu_0\vec{J}
\qquad\text{with}\qquad
\vec{B}(\vec{r}) = \frac{\mu_0}{4\pi}\int\frac{\vec{J}(\vec{r}\,')\times\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,d\tau'
$$

$$
\nabla\cdot\vec{A} = \frac{\mu_0}{4\pi}\int\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau'
$$

$$
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = \cancel{\frac{1}{\mathfrak{r}}\left(\nabla\cdot\vec{J}\right)} + \vec{J}\cdot\nabla\left(\frac{1}{\mathfrak{r}}\right)
$$

$$
\nabla\left(\frac{1}{\mathfrak{r}}\right) = -\nabla'\,\frac{1}{\mathfrak{r}}
\qquad \vec{\mathfrak{r}} = \vec{r} - \vec{r}\,'
$$

$$
\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = \cancel{\frac{1}{\mathfrak{r}}\left(\nabla'\cdot\vec{J}\right)} + \vec{J}\cdot\nabla'\left(\frac{1}{\mathfrak{r}}\right)
$$

$$
\nabla'\cdot\vec{J} = 0 \qquad \text{(magnetostatics)}
$$

$$
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = -\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)
$$

$$
\nabla\cdot\vec{A} = -\frac{\mu_0}{4\pi}\int\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau'
\;\xrightarrow{\text{div. theorem}}\;
-\frac{\mu_0}{4\pi}\oint\frac{\vec{J}}{\mathfrak{r}}\cdot d\vec{a}\,'
$$

where $\vec{J} = 0$ on surface $\therefore\ \nabla\cdot\vec{A} = 0$

$$
\nabla\times\vec{A} = \frac{\mu_0}{4\pi}\int\nabla\times\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau'
= \frac{\mu_0}{4\pi}\int\left[\cancel{\frac{1}{\mathfrak{r}}\left(\nabla\times\vec{J}\right)} - \vec{J}\times\nabla\left(\frac{1}{\mathfrak{r}}\right)\right]d\tau'
$$

$$
\vec{J} \neq f(\vec{r})
$$

$$
\nabla\left(\frac{1}{\mathfrak{r}}\right) = -\frac{\vec{\mathfrak{r}}}{\mathfrak{r}^3} = -\frac{\hat{\mathfrak{r}}}{\mathfrak{r}^2}
$$

$$
\nabla\times\vec{A} = \frac{\mu_0}{4\pi}\int\frac{\vec{J}\times\hat{\mathfrak{r}}}{\mathfrak{r}^2}\,d\tau' = \vec{B}
$$

$$
\nabla^2\vec{A} = \frac{\mu_0}{4\pi}\int\nabla^2\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau'
$$

$$
\nabla^2 f = \nabla\cdot\left(\nabla f\right) \qquad \text{where } \nabla\cdot\vec{J} = 0
$$

so $\nabla^2\vec{J} = 0$, so then

$$
\nabla^2\left(\frac{\vec{J}}{\mathfrak{r}}\right) = \vec{J}\;\nabla^2\left(\frac{1}{\mathfrak{r}}\right)
\qquad\text{margin: } \nabla\left(\frac{1}{\mathfrak{r}}\right) = -\frac{\hat{\mathfrak{r}}}{\mathfrak{r}^2},\quad \nabla\cdot\left(\frac{\vec{\mathfrak{r}}}{\mathfrak{r}^3}\right) = 4\pi\,\delta(\vec{\mathfrak{r}})
$$

so

$$
\nabla^2\left(\frac{1}{\mathfrak{r}}\right) = -4\pi\,\delta(\vec{\mathfrak{r}})
$$

$$
\nabla^2\vec{A} = -\frac{\mu_0}{4\pi}\int\vec{J}(\vec{r}\,')\;4\pi\,\delta(\vec{\mathfrak{r}})\,d\tau'
\qquad \delta(\vec{\mathfrak{r}}) = \delta(\vec{r}-\vec{r}\,')
$$

thus

$$
\boxed{\,\nabla^2\vec{A} = -\mu_0\,\vec{J}(\vec{r})\,}
$$

### P48. Prob 10.10 — Lorenz Gauge *(pp. 92–94)*

Show that the retarded potentials satisfy the Lorenz gauge condition $\nabla\cdot\vec{A} = -\mu_0\epsilon_0\,\partial V/\partial t$. The work turns on relating $\nabla\cdot\vec{J}$ and $\nabla'\cdot\vec{J}$ for the retarded current $\vec{J}(\vec{r}\,',t_r)$, whose dependence on $\vec{r}$ and $\vec{r}\,'$ also enters through $t_r = t-\mathfrak{r}/c$.

**Solution.**

$$
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = \frac{1}{\mathfrak{r}}\left(\nabla\cdot\vec{J}\right) + \vec{J}\cdot\nabla\left(\frac{1}{\mathfrak{r}}\right)
$$

$$
\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = \frac{1}{\mathfrak{r}}\left(\nabla'\cdot\vec{J}\right) + \vec{J}\cdot\left(\nabla'\,\frac{1}{\mathfrak{r}}\right)
$$

$$
\nabla\left(\frac{1}{\mathfrak{r}}\right) = -\nabla'\left(\frac{1}{\mathfrak{r}}\right)
\qquad \vec{\mathfrak{r}} = \vec{r}-\vec{r}\,'
$$

$$
\begin{aligned}
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) &= \frac{1}{\mathfrak{r}}\left(\nabla\cdot\vec{J}\right) - \vec{J}\cdot\nabla'\left(\frac{1}{\mathfrak{r}}\right) \\
&= \frac{1}{\mathfrak{r}}\left(\nabla\cdot\vec{J}\right) + \frac{1}{\mathfrak{r}}\left(\nabla'\cdot\vec{J}\right) - \nabla'\cdot\frac{\vec{J}}{\mathfrak{r}}
\end{aligned}
$$

$$
\nabla\cdot\vec{J} = \partial_i J_i = \partial_{t_r}\,\frac{\partial t_r}{\partial x^i}\,J_i
$$

$$
\frac{\partial t_r}{\partial x^i} = -\frac{1}{c}\frac{\partial\mathfrak{r}}{\partial x^i} = -\frac{1}{c}\nabla\mathfrak{r}
$$

$$
\nabla\cdot\vec{J} = -\frac{1}{c}\,\partial_{t_r}\vec{J}\cdot\left(\nabla\mathfrak{r}\right) = -\frac{1}{c}\frac{\partial\vec{J}}{\partial t_r}\cdot\left(\nabla\mathfrak{r}\right)
$$

Similarly

$$
\nabla'\cdot\vec{J} = -\frac{\partial\rho}{\partial t} - \frac{1}{c}\frac{\partial\vec{J}}{\partial t_r}\cdot\left(\nabla'\mathfrak{r}\right)
\qquad\left(\nabla'\cdot\vec{J}(\vec{r}\,') = -\frac{\partial\rho}{\partial t}\right)
$$

$$
\begin{aligned}
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) &= \frac{1}{\mathfrak{r}}\left(\nabla\cdot\vec{J}\right) + \frac{1}{\mathfrak{r}}\left(\nabla'\cdot\vec{J}\right) - \nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) \\
&= \frac{1}{\mathfrak{r}}\left[\cancel{-\frac{1}{c}\frac{\partial\vec{J}}{\partial t_r}\cdot\left(\nabla\mathfrak{r}\right)} - \frac{\partial\rho}{\partial t} + \cancel{\frac{1}{c}\frac{\partial\vec{J}}{\partial t_r}\cdot\left(\nabla\mathfrak{r}\right)}\right] - \nabla'\cdot\frac{\vec{J}}{\mathfrak{r}}
\end{aligned}
$$

$$
\nabla\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right) = -\frac{1}{\mathfrak{r}}\frac{\partial\rho}{\partial t} - \nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)
$$

$$
\vec{A}(\vec{r}) = \frac{\mu_0}{4\pi}\int\frac{\vec{J}(\vec{r}\,')}{\mathfrak{r}}\,d\tau'
$$

$$
\nabla\cdot\vec{A}(\vec{r}) = \frac{\mu_0}{4\pi}\int\left(\nabla\cdot\frac{\vec{J}}{\mathfrak{r}}\right)d\tau'
$$

$$
\begin{aligned}
\nabla\cdot\vec{A} &= \frac{\mu_0}{4\pi}\left[\frac{\partial}{\partial t}\int-\frac{\rho}{\mathfrak{r}}\,d\tau \;-\; \int\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau\right] \\
&= -\frac{\mu_0}{4\pi}\left[\frac{\partial}{\partial t}\int\frac{\rho}{\mathfrak{r}}\,d\tau \;+\; \int\nabla'\cdot\left(\frac{\vec{J}}{\mathfrak{r}}\right)d\tau\right]
\end{aligned}
$$

$$
\nabla\cdot\vec{A} = -\mu_0\epsilon_0\,\frac{\partial}{\partial t}\left[\frac{1}{4\pi\epsilon_0}\int\frac{\rho}{\mathfrak{r}}\,d\tau\right] - \cancel{\frac{\mu_0}{4\pi}\oint\frac{\vec{J}}{\mathfrak{r}}\cdot d\vec{a}}
\qquad\text{(div. theorem; where } \vec{J} = 0 \text{ on surface)}
$$

$$
\boxed{\,\nabla\cdot\vec{A} = -\mu_0\epsilon_0\,\frac{\partial V}{\partial t}\,}
$$

### P49. Ex 2.6 — Two Infinite Planes *(p. 95)*

Two infinite parallel planes carry equal but opposite uniform charge densities $\pm\sigma$; find $\vec{E}$ on the left, middle, and right. The page argues entirely by superposition diagrams (field directions of each sheet in the three regions); no formulas are written.

**Solution.**

2 infinite planes (parallel) equal but opposite uniform charge densities $\pm\sigma$. Find: $\vec{E}$ on the left, middle, right.

*[Diagram: two parallel rectangular sheets drawn side by side, labeled $+\sigma$ and $-\sigma$.]*

*[Diagram: the planes as two vertical lines ($+\sigma$ left, $-\sigma$ right) dividing space into three regions. Top row, the $+$ sheet's field $E_+$: points left in the left region, right in the middle region, right in the right region (always away from $+\sigma$). Bottom row, the $-$ sheet's field $E_-$: points right in the left region, right in the middle region, left in the right region (always toward $-\sigma$). Outside the pair the two arrows oppose; between the planes they point the same way.]*

*[Diagram: between the two planes, arrows labeled $\vec{E}$ pointing from $+\sigma$ toward $-\sigma$ — the total field.]*

so

*[Diagram: the gap again, planes labeled $\sigma_+$ and $\sigma_-$, with the two contributions $E_+$ and $E_-$ drawn parallel, both pointing from $\sigma_+$ to $\sigma_-$.]*

where if so, then by attraction

*[Diagram: at the $\sigma_+$ plane, $E_+$ points away to the left while $E_-$ points right, toward the $-$ plane; at the $\sigma_-$ plane, $E_+$ points right (away from $+\sigma$) while $E_-$ points left, into it — each sheet sits in the other's field, pulling the sheets together.]*

& Newton Law (3rd) *[crossed-out word, illegible]*

### P50. Spherical Laplace (Legendre, Rodrigues) *(pp. 96–97)*

*[reference notes, not a worked problem]*

General solution of Laplace's equation in spherical coordinates with azimuthal symmetry (margin label "3D Potential"): separation of variables $V = R(r)\Theta(\theta)$, the radial and angular equations with separation constant $\ell(\ell+1)$, Legendre polynomials via the Rodrigues formula, and the general series for $V(r,\theta)$.

**Solution.**

$$
d\vec{l} = dr\,\hat{r} + r\,d\theta\,\hat{\theta} + r\sin\theta\,d\phi\,\hat{\phi}
$$

$$
d\tau = r^2\sin\theta\,dr\,d\theta\,d\phi
$$

$$
\frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial V}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial V}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2 V}{\partial\phi^2} = 0
$$

Azimuthal symmetry (ind. of $\phi$)

$$
\frac{\partial}{\partial r}\left(r^2\frac{\partial V}{\partial r}\right) + \frac{1}{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial V}{\partial\theta}\right) = 0
$$

Set $V(r,\theta) = R(r)\,\Theta(\theta)$, then divide by $R(r)\,\Theta(\theta)$

$$
\frac{1}{R}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \frac{1}{\Theta\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) = 0
$$

for convenience

$$
\frac{1}{R}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) = \ell(\ell+1)
\qquad
\frac{1}{\Theta\sin\theta}\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) = -\ell(\ell+1)
$$

$$
\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) = \ell(\ell+1)\,R
$$

$$
R(r) = A\,r^\ell + \frac{B}{r^{\ell+1}}
$$

$$
\frac{d}{d\theta}\left(\sin\theta\frac{d\Theta}{d\theta}\right) = -\ell(\ell+1)\sin\theta\,\Theta
$$

Legendre Polynomials

$$
\Theta(\theta) = P_\ell(\cos\theta)
$$

Rodrigues formula

$$
P_\ell(x) = \frac{1}{2^\ell\,\ell!}\left(\frac{d}{dx}\right)^{\ell}\left(x^2-1\right)^{\ell}
$$

$$
P_0(x) = 1 \qquad P_1(x) = x \qquad P_2(x) = \frac{3x^2-1}{2} \qquad P_3 = \frac{5x^3-3x}{2} \qquad P_4 = \frac{35x^4-30x^2+3}{8} \quad \text{etc.}\ldots
$$

$$
V(r,\theta) = \sum_{\ell=0}^{\infty}\left(A_\ell\,r^\ell + \frac{B_\ell}{r^{\ell+1}}\right)P_\ell(\cos\theta)
$$

### P51. Infinite Pipe 2D *(pp. 98–100)*

Laplace's equation is solved for the potential inside an infinitely long rectangular pipe (axis along $z$) of cross-section $-b \le x \le b$, $0 \le y \le a$: the walls $y=0$ and $y=a$ are grounded, and the two side walls at $x=\pm b$ are held at constant potential $V_0$.

**Solution.**

*[Diagram: a rectangular pipe extending to infinity along $z$ (jagged ends); the faces $y=0$ and $y=a$ are marked $V=0$, the side faces at $x=-b$ and $x=+b$ are marked $V_0$.]*

$$
V(x,0) = V(x,a) = 0, \qquad V(\pm b, y) = V_0
$$

$$
\{x \mid x \in \pm b\}, \qquad \{y \mid y \in 0, a\}
$$

$$
\nabla^2 V = 0 \;\rightarrow\; \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} = 0
$$

$$
\frac{1}{X}\frac{d^2 X}{dx^2} + \frac{1}{Y}\frac{d^2 Y}{dy^2} = 0
$$

Again *[a crossed-out symbol]* has trivial solutions so

$$
X \sim f\!\left(e^{\pm kx}\right) \qquad Y \sim f(\sin + \cos)
$$

$X$ is symmetric, $\{x \mid x \in \pm b\}$:

$$
e^{kx} + e^{-kx} = 2\cosh(kx)
$$

$$
V(x,y) = \cosh(kx)\left(C\sin ky + D\cos ky\right)
$$

$$
V(x,0) = 0 = \cosh(kx)\left(C\sin(0) + D\cos(0)\right)
$$

so $D \to 0$.

$$
V(x,y) = C\cosh(kx)\sin(ky)
$$

$$
ka = n\pi \;\rightarrow\; k = \frac{n\pi}{a}
$$

$$
V(x,y) = \sum_{n=1}^{\infty} C_n \cosh\!\left(\frac{n\pi x}{a}\right)\sin\!\left(\frac{n\pi y}{a}\right)
$$

$$
V(b,y) = \sum_{n=1}^{\infty} C_n \cosh\!\left(\frac{n\pi b}{a}\right)\sin\!\left(\frac{n\pi y}{a}\right) = V_0
$$

$$
\sum_{n=1}^{\infty} C_n \int_0^{a} \cosh\!\left(\frac{n\pi b}{a}\right)\sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{n'\pi y}{a}\right)dy = V_0 \int_0^{a} \sin\!\left(\frac{n'\pi y}{a}\right)dy
$$

$$
\sum_{n=1}^{\infty} C_n \cosh\!\left(\frac{n\pi b}{a}\right)\underbrace{\sin\!\left(\frac{n\pi y}{a}\right)}_{f(y)} = V_0
$$

$$
C_n = \frac{2V_0}{a\cosh\!\left(\frac{n\pi b}{a}\right)}\int_0^{a}\sin\!\left(\frac{n\pi y}{a}\right)dy, \qquad \int_0^{a}\sin\!\left(\frac{n\pi y}{a}\right)dy = \frac{2a}{n\pi}\ \text{ if } n \text{ is odd}
$$

$$
C_n = \frac{4V_0}{n\pi}\,\frac{1}{\cosh\!\left(\frac{n\pi b}{a}\right)}
$$

$$
V(x,y) = \frac{4V_0}{\pi}\sum_{n=1,3,5\ldots}\frac{1}{n}\,\frac{\cosh\!\left(\frac{n\pi x}{a}\right)}{\cosh\!\left(\frac{n\pi b}{a}\right)}\,\sin\!\left(\frac{n\pi y}{a}\right)
$$

### P52. Inf. Rect. Pipe 3D *(pp. 101–103)*

Laplace's equation is solved in the semi-infinite rectangular pipe $\{x \mid x\in[0,\infty]\}$, $\{y \mid y\in[0,a]\}$, $\{z \mid z\in[0,b]\}$: the four long walls are grounded, $V \to 0$ as $x \to \infty$, and the end face at $x=0$ is held at a prescribed potential $V_0(y,z)$.

**Solution.**

$$
V(x,0,z) = V(x,a,z) = 0, \qquad V(x,y,0) = V(x,y,b) = 0
$$

$$
V \to 0: \; V(\infty,y,z), \qquad V(0,y,z) = V_0(y,z)
$$

*[Diagram: semi-infinite rectangular duct along $+x$ with jagged open far end; height $a$ along $y$, depth $b$ along $z$; the $x=0$ face carries $V_0(y,z)$, the bottom face is marked $V=0$, and $V\to0$ toward the far end.]*

Laplace eq.

$$
\nabla^2 V = 0, \qquad \frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} + \frac{\partial^2 V}{\partial z^2} = 0
$$

$$
V(x,y,z) = X(x)\,Y(y)\,Z(z)
$$

$$
\frac{d^2X}{dx^2}\,YZ + \frac{d^2Y}{dy^2}\,XZ + XY\,\frac{d^2Z}{dz^2} = 0
$$

$y$ & $z$ have set boundaries $a$, $b$ so sin & cos:

$$
\frac{1}{Y}\frac{d^2Y}{dy^2} = -k^2 \qquad \frac{1}{Z}\frac{d^2Z}{dz^2} = -\ell^2
$$

$$
\frac{1}{X}\frac{d^2X}{dx^2} = k^2+\ell^2
$$

$$
X(x) = A\,e^{\sqrt{k^2+\ell^2}\,x} + B\,e^{-\sqrt{k^2+\ell^2}\,x}
$$

$$
Y(y) = C\sin(ky) + D\cos(ky)
$$

$$
Z(z) = E\sin(\ell z) + F\cos(\ell z)
$$

$$
V(y=0) \rightarrow D = 0, \qquad V(z=0) \rightarrow F = 0, \qquad V(x\to\infty) \rightarrow A = 0
$$

let $BCE \equiv C$:

$$
V = C\,e^{-\sqrt{k^2+\ell^2}\,x}\sin(ky)\sin(\ell z)
$$

$$
ka = n\pi \;\rightarrow\; k = \frac{n\pi}{a}, \qquad \ell = \frac{m\pi}{b}
$$

$$
V = \sum_{n,m=1}^{\infty} C_{nm}\, e^{-\pi\sqrt{\left(\frac{n}{a}\right)^2+\left(\frac{m}{b}\right)^2}\,x}\,\sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{m\pi z}{b}\right)
$$

$$
V(x=0) = V_0(y,z) = \sum_{n,m=1}^{\infty} C_{nm}\,\sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{m\pi z}{b}\right)
$$

$$
\sum\sum C_{nm}\int_0^{a} \sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{n'\pi y}{a}\right)dy\int_0^{b} \sin\!\left(\frac{m\pi z}{b}\right)\sin\!\left(\frac{m'\pi z}{b}\right)dz = \int_0^{a} \sin\!\left(\frac{n\pi y}{a}\right)dy\int_0^{b} \sin\!\left(\frac{m\pi z}{b}\right)dz\; V_0
$$

Fourier's trick:

$$
C_{nm} = \frac{2}{a}\,\frac{2}{b}\int_0^{a}\!\!\int_0^{b} V_0\,\sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{m\pi z}{b}\right)dy\,dz
$$

$$
C_{nm} = \frac{16\,V_0}{nm\,\pi^2} \quad \text{if } n,m \text{ are odd}
$$

(General form noted alongside, "fourier's trick":

$$
C_{nm} = \frac{2}{L_y}\,\frac{2}{L_z}\int_0^{L_y} dy\, f_y(n') \int_0^{L_z} dz\, f_z(m')\, V_0
$$

)

$$
V(x,y,z) = \frac{16V_0}{\pi^2}\sum_{n,m=1,3,5\ldots}^{\infty} e^{-\pi\sqrt{\left(\frac{n}{a}\right)^2+\left(\frac{m}{b}\right)^2}\,x}\,\sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{m\pi z}{b}\right)\frac{1}{nm}
$$

### P53. Ex 3.2 — Sep. of Variables *(pp. 104–107)*

The semi-infinite slot: two grounded semi-infinite plates at $y=0$ and $y=a$ run from $x=0$ to $x\to\infty$, closed at $x=0$ by a strip held at $V_0(y)$, with $V \to 0$ as $x \to \infty$; $V(x,y)$ is found by separation of variables, and the coefficients are then evaluated for constant $V_0$.

**Solution.**

*[Diagram: two semi-infinite grounded plates ($V=0$) parallel to the $x$–$z$ plane at $y=0$ and $y=a$, jagged at large $x$; the strip $V_0(y)$ at $x=0$ closes the slot; axes $x$, $y$, $z$ drawn.]*

$$
V(x,0) = V(x,a) = 0
$$

$$
V(0,y) = V_0(y), \qquad V \to 0 \ \text{ as } \ x \to \infty
$$

① Laplace's 2D eq.

$$
\frac{\partial^2 V}{\partial x^2} + \frac{\partial^2 V}{\partial y^2} = 0
$$

②

$$
V(x,y) = X(x)\,Y(y)
$$

② → ①

$$
\frac{d^2X}{dx^2}\,Y + X\,\frac{d^2Y}{dy^2} = 0
$$

$$
\frac{1}{X}\frac{d^2X}{dx^2} + \frac{1}{Y}\frac{d^2Y}{dy^2} = 0, \qquad k^2 - k^2 = 0
$$

with the first term marked $\equiv k^2$ and the second $-k^2$:

$$
X(x) = A\,e^{kx} + B\,e^{-kx} \qquad Y(y) = C\sin(ky) + D\cos(ky)
$$

$$
V(x,y) = \left(A\,e^{kx}+B\,e^{-kx}\right)\left(C\sin(ky)+D\cos(ky)\right)
$$

$$
V(\infty,y) = \left(A\,e^{\infty} + \frac{B}{e^{\infty}}\right)Y(y) = 0
$$

So $A$ must go to zero. $A=0$.

$$
X(x) = B\,e^{-kx}
$$

$$
V(x,0) = B\,e^{-kx}\left(C\sin(0)+D\cos(0)\right) = 0
$$

so $D \to 0$.

$$
V(x,y) = BC\, e^{-kx}\sin(ky) \qquad \text{let } BC \equiv B
$$

$$
V(x,a) = 0 = B\, e^{-kx}\sin(ka)
$$

$\sin(ka) = 0$ when $ka = n\pi$ so

$$
k = \frac{n\pi}{a}
$$

$$
V(x,y) = \sum_{n=1}^{\infty} e^{-\frac{n\pi x}{a}}\sin\!\left(\frac{n\pi y}{a}\right)B_n
$$

$$
V(0,y) \rightarrow \sum_{n=1}^{\infty} B_n \sin\!\left(\frac{n\pi y}{a}\right) = V_0(y)
$$

integrate over $y$-axis with additional $f(n')$:

$$
\sum_{n=1}^{\infty} B_n \int_0^{a} \sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{n'\pi y}{a}\right)dy = \int_0^{a} V_0(y)\,\sin\!\left(\frac{n'\pi y}{a}\right)dy
$$

$$
\int_0^{a} \sin\!\left(\frac{n\pi y}{a}\right)\sin\!\left(\frac{n'\pi y}{a}\right)dy = \begin{cases} 0 & n'\neq n \\[2pt] \dfrac{a}{2} & n = n' \end{cases}
$$

$$
B_n\,\frac{a}{2} = \int_0^{a} V_0(y)\,\sin\!\left(\frac{n\pi y}{a}\right)dy
$$

$$
B_n = \frac{2V_0}{a}\int_0^{a} \sin\!\left(\frac{n\pi y}{a}\right)dy = \frac{2V_0}{n\pi}\left(1-\cos n\pi\right)
$$

$$
B_n = 0 \ \text{ if } n = \text{even}
$$

so

$$
B_n = \frac{4V_0}{n\pi} \quad \text{for odd } n
$$

$$
V(x,y) = \frac{4V_0}{\pi}\sum_{n=1,3,5}^{\infty}\frac{1}{n}\, e^{-\frac{n\pi x}{a}}\sin\!\left(\frac{n\pi y}{a}\right)
$$

### P54. Spherical Coordinates → Multipole Expansion *(p. 108)*

*[reference notes, not a worked problem]*

The spherical-harmonic expansion of $1/|\vec{x}-\vec{x}\,'|$ and the resulting multipole form of the potential of a charge density $\rho(\vec{x}\,')$, evaluated outside the sphere enclosing the charge ($r_< = r'$, $r_> = r$).

**Solution.**

$$
\frac{1}{|\vec{x}-\vec{x}\,'|} = 4\pi\sum_{\ell=0}^{\infty}\sum_{m=-\ell}^{\ell}\frac{1}{2\ell+1}\,\frac{r_<^{\ell}}{r_>^{\ell+1}}\,Y^*_{\ell m}(\theta',\phi')\,Y_{\ell m}(\theta,\phi)
$$

$$
\Phi(\vec{x}) = \frac{1}{4\pi\epsilon_0}\int \frac{\rho(\vec{x}\,')}{|\vec{x}-\vec{x}\,'|}\,d^3x'
$$

for outside the sphere $r_< = r'$, $r_> = r$:

$$
\Phi(\vec{x}) = \frac{1}{\epsilon_0}\sum_{\ell,m}\frac{1}{2\ell+1}\int \frac{r'^{\ell}}{r^{\ell+1}}\,Y^*_{\ell m}(\theta',\phi')\,\rho(\vec{x}\,')\,Y_{\ell m}(\theta,\phi)\,d^3x'
$$

### P55. Eigenfunction Expansions for Green functions *(pp. 109–110)*

*[reference notes, not a worked problem]*

The eigenfunction expansion of the Green function of the operator $\nabla^2 + f(\vec{x}) + \lambda$ is derived, then specialized to $f=0$, $\lambda=0$ with the free-space wave-equation continuum $\psi_{\vec{k}}$ (giving the Fourier representation of $1/|\vec{x}-\vec{x}\,'|$) and to the Dirichlet modes of a rectangular box $x\in(0,a)$, $y\in(0,b)$, $z\in(0,c)$.

**Solution.**

$$
\nabla^2\psi_n(\vec{x}) + \left(f(\vec{x})+\lambda_n\right)\psi_n(\vec{x}) = 0
$$

$$
\int_V \psi^*_m(\vec{x})\,\psi_n(\vec{x})\,d^3x = \delta_{mn}
$$

$$
\nabla^2 G(\vec{x},\vec{x}\,') + \left[f(\vec{x})+\lambda\right]G(\vec{x},\vec{x}\,') = -4\pi\,\delta(\vec{x}-\vec{x}\,')
$$

$$
G(\vec{x},\vec{x}\,') = \sum_n a_n(\vec{x}\,')\,\psi_n(\vec{x})
$$

$$
\sum_m a_m(\vec{x}\,')\left(\lambda-\lambda_m\right)\psi_m(\vec{x}) = -4\pi\,\delta(\vec{x}-\vec{x}\,')
$$

$\times\ \psi^*_n(\vec{x})$ (both sides) & int $\int_V$ — orthogonality simplifies LHS

$$
\rightarrow\; a_n(\vec{x}\,') = 4\pi\,\frac{\psi^*_n(\vec{x}\,')}{\lambda_n-\lambda}
$$

so

$$
G(\vec{x},\vec{x}\,') = 4\pi\sum_n \frac{\psi^*_n(\vec{x}\,')\,\psi_n(\vec{x})}{\lambda_n-\lambda}
$$

let $f(\vec{x})=0$, $\lambda=0$ $\rightarrow$ wave eq. over all space:

$$
\left(\nabla^2+k^2\right)\psi_{\vec{k}}(\vec{x}) = 0
$$

$$
\psi_{\vec{k}}(\vec{x}) = \frac{1}{(2\pi)^{3/2}}\,e^{i\vec{k}\cdot\vec{x}}
$$

normalization δ-fun:

$$
\int \psi^*_{\vec{k}'}(\vec{x})\,\psi_{\vec{k}}(\vec{x})\,d^3x = \delta\!\left(\vec{k}-\vec{k}'\right)
$$

$$
\frac{1}{|\vec{x}-\vec{x}\,'|} = \frac{1}{2\pi^2}\int d^3k\,\frac{e^{i\vec{k}\cdot(\vec{x}-\vec{x}\,')}}{k^2}
$$

For Cartesian box $\{x\in(0,a);\ y\in(0,b);\ z\in(0,c)\}$:

$$
\left(\nabla^2 + k^2_{lmn}\right)\psi_{lmn}(x,y,z) = 0
$$

$$
\psi_{lmn}(x,y,z) = \sqrt{\frac{8}{abc}}\,\sin\!\left(\frac{l\pi x}{a}\right)\sin\!\left(\frac{m\pi y}{b}\right)\sin\!\left(\frac{n\pi z}{c}\right)
$$

$$
k^2_{lmn} = \pi^2\left(\frac{l^2}{a^2}+\frac{m^2}{b^2}+\frac{n^2}{c^2}\right)
$$

$$
G(\vec{x},\vec{x}\,') = \frac{32}{\pi abc}\sum_{l,m,n=1}^{\infty}\frac{\sin\!\left(\frac{l\pi x}{a}\right)\sin\!\left(\frac{l\pi x'}{a}\right)\sin\!\left(\frac{m\pi y}{b}\right)\sin\!\left(\frac{m\pi y'}{b}\right)\sin\!\left(\frac{n\pi z}{c}\right)\sin\!\left(\frac{n\pi z'}{c}\right)}{\frac{l^2}{a^2}+\frac{m^2}{b^2}+\frac{n^2}{c^2}}
$$

more on pg 129 *(a textbook page reference)*.

### P56. Cylindrical Green's Functions *(pp. 111–115)*

The free-space Green function is expanded in cylindrical coordinates $(\rho,\phi,z)$: the $\delta$-functions are written in Fourier form, the radial equation is solved with modified Bessel functions $I_m$, $K_m$ normalized through the Wronskian/slope-discontinuity condition, the resulting expansion of $1/|\vec{x}-\vec{x}\,'|$ is used to obtain (and check) the $K_0$ addition theorem, and the $k\to0$ limit gives the 2-D logarithmic expansion.

*[p. 112 is a second scan of the same "1/4" page as p. 111; the entry's pages are corner-marked 1/4–4/4.]*

**Solution.**

$$
\nabla^2 G(\vec{x},\vec{x}\,') = -\frac{4\pi}{\rho}\,\delta(\rho-\rho')\,\delta(\phi-\phi')\,\delta(z-z')
$$

$$
\delta(z-z') = \frac{1}{2\pi}\int_{-\infty}^{\infty} dk\, e^{ik(z-z')} = \frac{1}{\pi}\int_0^{\infty} dk\,\cos\!\left[k(z-z')\right]
$$

$$
\delta(\phi-\phi') = \frac{1}{2\pi}\sum_{m=-\infty}^{\infty} e^{im(\phi-\phi')}
$$

$$
G(\vec{x},\vec{x}\,') = \frac{1}{2\pi^2}\sum_{m=-\infty}^{\infty}\int_0^{\infty} dk\, e^{im(\phi-\phi')}\cos\!\left[k(z-z')\right] g_m(k,\rho,\rho')
$$

$$
\frac{1}{\rho}\frac{d}{d\rho}\!\left(\rho\,\frac{dg_m}{d\rho}\right) - \left(k^2+\frac{m^2}{\rho^2}\right)g_m = -\frac{4\pi}{\rho}\,\delta(\rho-\rho')
$$

Linear combinations of modified Bessel functions $I_m(k\rho)$, $K_m(k\rho)$: $\psi_1(k\rho)$ satisfies $\rho<\rho'$; $\psi_2(k\rho)$ lin. ind., satisf. $\rho>\rho'$.

$$
g_m(k,\rho,\rho') = \psi_1(k\rho_<)\,\psi_2(k\rho_>)
$$

Normalize wrt. discontinuity by δ-function:

$$
\left.\frac{dg_m}{d\rho}\right|_{+} - \left.\frac{dg_m}{d\rho}\right|_{-} = -\frac{4\pi}{\rho'}
$$

$$
\left.\frac{dg_m}{d\rho}\right|_{+} - \left.\frac{dg_m}{d\rho}\right|_{-} = k\left(\psi_1\psi_2' - \psi_2\psi_1'\right) = k\,W\!\left[\psi_1,\psi_2\right]
$$

Sturm–Liouville type (radial Green function), so then

$$
W\!\left[\psi_1(x),\psi_2(x)\right] = -\frac{4\pi}{x}
$$

$g_m$ must be finite at $\rho=0$; vanish $\rho\to\infty$, so

$$
\psi_1(k\rho) = A\,I_m(k\rho) \qquad \psi_2(k\rho) = K_m(k\rho)
$$

choosing $A = 4\pi$:

$$
W\!\left[I_m(x),K_m(x)\right] = -\frac{1}{x}
$$

$$
\frac{1}{|\vec{x}-\vec{x}\,'|} = \frac{2}{\pi}\sum_{m=-\infty}^{\infty}\int_0^{\infty} dk\, e^{im(\phi-\phi')}\cos\!\left[k(z-z')\right] I_m(k\rho_<)\,K_m(k\rho_>)
$$

in purely real terms

$$
\frac{1}{|\vec{x}-\vec{x}\,'|} = \frac{4}{\pi}\int_0^{\infty} dk\,\cos\!\left[k(z-z')\right]\left\{\frac{1}{2}\,I_0(k\rho_<)K_0(k\rho_>) + \sum_{m=1}^{\infty}\cos\!\left[m(\phi-\phi')\right] I_m(k\rho_<)\,K_m(k\rho_>)\right\} \tag{1}
$$

(the braced quantity is labelled $\beta$). If $\vec{x}\,' \to 0$ only $m=0$ survives:

$$
\frac{1}{\sqrt{\rho^2+z^2}} = \frac{2}{\pi}\int_0^{\infty}\cos(kz)\,K_0(k\rho)\,dk \tag{2}
$$

(margin note: comparable to $1/|\vec{x}|$). let

$$
\rho^2 \rightarrow R^2 = \rho^2+\rho'^2-2\rho\rho'\cos(\phi-\phi'), \qquad R = \sqrt{\rho^2+\rho'^2-2\rho\rho'\cos(\phi-\phi')}
$$

eval. (1) @ $z'=0$; RHS of (1) $\equiv$ (2) RHS:

$$
K_0\!\left(k\sqrt{\rho^2+\rho'^2-2\rho\rho'\cos(\phi-\phi')}\right) = I_0(k\rho_<)K_0(k\rho_>) + 2\sum_{m=1}^{\infty}\cos\!\left[m(\phi-\phi')\right] I_m(k\rho_<)\,K_m(k\rho_>)
$$

checking — the common factor $\frac{2}{\pi}\int_0^{\infty} dk\,\cos(kz)$ is struck from both sides:

$$
2\,\cancel{\frac{4}{\pi}}\int_0^{\infty}dk\,\cancel{\cos(kz)}\,\{\beta\} = \cancel{\frac{2}{\pi}}\int_0^{\infty}\cancel{\cos kz}\; K_0(k\rho)\,dk
$$

$$
K_0\!\left[k(\rho=R)\right] = 2\beta \quad \checkmark
$$

take $k\to0$ (the addition theorem is rewritten at the top of the last page):

$$
\lim_{k\to0} K_0(k\rho) \Rightarrow \ln\!\left(\frac{1}{R^2}\right)\bigg|_{\rho=R}
$$

$$
\lim_{k\to0} I_0(k\rho_<) \rightarrow 2
$$

*[sic: as literal limits $I_0 \to 1$ and $K_0(x) \sim \ln(2/x)-\gamma$; the factors of 2 in these two lines are bookkeeping, distributed so that the final expansion below comes out correctly]*

$$
\lim_{k\to0} K_m(k\rho_>) \rightarrow \left(\frac{1}{\rho_>}\right)^{m} \qquad \lim_{k\to0} K_0(k\rho_>) = \ln\!\left(\frac{1}{\rho_>}\right)
$$

$$
\lim_{k\to0} I_m(k\rho_<) \rightarrow \frac{1}{m}\left(\rho_<\right)^{m}
$$

$$
\ln\!\left(\frac{1}{\rho^2+\rho'^2-2\rho\rho'\cos(\phi-\phi')}\right) = 2\ln\!\left(\frac{1}{\rho_>}\right) + 2\sum_{m=1}^{\infty}\frac{1}{m}\left(\frac{\rho_<}{\rho_>}\right)^{m}\cos\!\left[m(\phi-\phi')\right]
$$

look at problem 2.17
