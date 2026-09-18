# RE-03 — Problems

Work them by hand, then check with `code/lorentz.py`. Sources in `../refs.md`.

### P1. Invert the boost  *(Griffiths 4e, Prob. 12.12, p.523)*
Solve the Lorentz transformation Eqs. 12.18 for `(ct, x)` in terms of `(ct', x')`.
Show the inverse is the same transformation with `β → −β`.
*Check:* `inverse(boost(0.6))` equals `boost(-0.6)`, and `compose(inverse(L), L)`
is the identity.

**Solution.** The boost is $ct'=\gamma(ct-\beta x)$, $x'=\gamma(x-\beta ct)$. Solve for the
unprimed pair (eliminate, then use $\gamma^2(1-\beta^2)=1$):
$$ct=\gamma(ct'+\beta x'),\qquad x=\gamma(x'+\beta ct').$$
This is the *same* transformation with $\beta\to-\beta$ — physically obvious, since S moves
at $-\beta$ relative to S′. In matrix form $\Lambda(\beta)=\begin{pmatrix}\gamma&-\gamma\beta\\-\gamma\beta&\gamma\end{pmatrix}$
has $\det=\gamma^2(1-\beta^2)=1$, and its inverse just flips the off-diagonal sign:
$\Lambda(\beta)^{-1}=\Lambda(-\beta)$. Hence `inverse(boost(0.6))` equals `boost(-0.6)`, and
`compose(inverse(L), L)` is the identity.

### P2. Velocities don't add  *(Griffiths 4e, Ex. 12.6 / Prob. 12.14, p.523)*
Two ships approach you head-on, each at `0.9c` in your frame. How fast does one
move in the other's frame?
*Answer:* `(0.9+0.9)/(1+0.81) = 1.8/1.81 = 0.9945c`, not `1.8c`.
*Check:* `velocity_add(0.9, 0.9) → 0.99447…`. Confirm `velocity_add(0.9, 1.0) = 1.0`.

**Solution.** Boost into one ship's rest frame; the other's velocity composes by
$$w=\frac{u+v}{1+uv/c^2}=\frac{0.9c+0.9c}{1+(0.9)(0.9)}=\frac{1.8c}{1.81}=0.9945\,c,$$
not $1.8c$ — the gap closes at $1.8c$ as a coordinate rate in *your* frame, but neither ship
measures the other above $c$. The cap is automatic because $\tanh$ (hence the rule)
saturates at $1$: feeding in a light ray, `velocity_add(0.9, 1.0)`$=(0.9+1)/(1+0.9)=1$ — light
stays at light speed in every frame. So `velocity_add(0.9, 0.9)`$=0.99447$.

### P3. Rapidity is the additive angle  *(Griffiths 4e, Prob. 12.19, p.528)*
A Lorentz boost is a "rotation through an imaginary angle." Show that three
collinear boosts `β₁, β₂, β₃` compose to a single boost whose rapidity is
`φ₁+φ₂+φ₃`.
*Check:* `compose(boost(b1), boost(b2), boost(b3))` equals `boost(β)` with
`β = beta_from_rapidity(rapidity(b1)+rapidity(b2)+rapidity(b3))`.

**Solution.** In the $(ct,x)$ plane a boost is a hyperbolic rotation
$\Lambda(\phi)=\begin{pmatrix}\cosh\phi&-\sinh\phi\\-\sinh\phi&\cosh\phi\end{pmatrix}$ with
$\phi=\operatorname{artanh}\beta$. Rotations about the same axis add their angles,
$\Lambda(\phi_1)\Lambda(\phi_2)\Lambda(\phi_3)=\Lambda(\phi_1+\phi_2+\phi_3)$, exactly like
ordinary rotations. So three collinear boosts make a single boost of rapidity
$\phi_1+\phi_2+\phi_3$, i.e.
$$\beta=\tanh(\phi_1+\phi_2+\phi_3).$$
For $\beta_i=(0.4,0.5,0.6)$ the rapidities sum to $1.6661$ and $\beta=\tanh(1.6661)=0.9310$.
Thus `compose(boost(b1), boost(b2), boost(b3))` equals
`boost(beta_from_rapidity(rapidity(b1)+rapidity(b2)+rapidity(b3)))` — velocities don't add,
rapidities do.

### P4. The Galilean limit  *(Griffiths 4e, Prob. 12.18a, p.527)*
Write the boost matrix for `β = 10⁻⁴` and show it differs from the Galilean
transformation `[[1,0],[−β,1]]` (in `(ct,x)`) only at order `β²`.
*Check:* compare `boost(1e-4)` with the Galilean matrix; the `γ−1 ≈ ½β² = 5×10⁻⁹`
corrections sit on the diagonal.

**Solution.** The boost $\begin{pmatrix}\gamma&-\gamma\beta\\-\gamma\beta&\gamma\end{pmatrix}$
sits against the Galilean $\begin{pmatrix}1&0\\-\beta&1\end{pmatrix}$ in $(ct,x)$. For
$\beta=10^{-4}$, $\gamma=(1-10^{-8})^{-1/2}=1+\tfrac12\beta^2+\cdots$, so the diagonal entries
exceed the Galilean $1$ by
$$\gamma-1\approx\tfrac12\beta^2=5\times10^{-9},$$
the corrections the Check locates on the diagonal. The space-row entry
$-\gamma\beta=-\beta(1+\tfrac12\beta^2+\cdots)$ reproduces the Galilean $-\beta$ to relative
order $\beta^2$, so $x'=\gamma(x-\beta ct)$ matches $x'=x-\beta ct$ to that order. The one
genuinely new entry is the $-\gamma\beta$ in the *time* row — the $-\beta x$
(relativity-of-simultaneity) term that $t'=t$ drops — and it too vanishes as $\beta\to0$.
So `boost(1e-4)` has diagonal $1.000000005$ and collapses to the Galilean map in the
$c\to\infty$ limit.

### P5. The interval is invariant  *(Griffiths 4e, Prob. 12.20, p.529)*
Event A = `(0, 0, 0, 0)`, event B = `(ct, x, 0, 0)` with `ct = 5`, `x = 3`. Compute
`s²` between them, then boost by an arbitrary `β` and recompute.
*Answer:* `s² = −25 + 9 = −16` (timelike) in every frame.
*Check:* `interval2([5,3,0,0])` and `interval2(apply(general_boost((0.4,-0.2,0.5)), [5,3,0,0]))`
agree; `classify([5,3,0,0]) → "timelike"`.

**Solution.** With $\eta=\mathrm{diag}(-1,1,1,1)$ the squared interval between
$A=(0,0,0,0)$ and $B=(5,3,0,0)$ is
$$s^2=-(ct)^2+x^2=-(5)^2+(3)^2=-25+9=-16<0,$$
so the separation is **timelike**. Every Lorentz transformation obeys
$\Lambda^{\mathsf T}\eta\Lambda=\eta$, hence leaves $s^2=x^{\mathsf T}\eta x$ unchanged for
all events: boosting $B$ by any $\boldsymbol\beta$ returns the same $-16$. Concretely
`interval2([5,3,0,0])`$=-16$ equals
`interval2(apply(general_boost((0.4,-0.2,0.5)), [5,3,0,0]))`, and `classify([5,3,0,0])` is
`"timelike"`.

### P6. Light stays light  *(Zee III.2; conceptual)*
A photon moves along `(t, t, 0, 0)` (speed 1). Boost to a frame moving at any
`β` and show the photon's measured 3-speed is still 1.
*Check:* `out = apply(boost(0.8), [1,1,0,0]); out[1]/out[0]` → 1.0, and
`classify(out) → "null"`. This is the postulate the whole module is built to honour.

**Solution.** The photon worldline $(t,t,0,0)$ has 3-speed $x/t=1$ and is null,
$s^2=-t^2+t^2=0$. Boost at $\beta=0.8$ ($\gamma=1/\sqrt{1-0.64}=5/3$):
$$\begin{pmatrix}ct'\\x'\end{pmatrix}=\gamma\begin{pmatrix}1&-\beta\\-\beta&1\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix}=\tfrac53\begin{pmatrix}1-0.8\\1-0.8\end{pmatrix}=\begin{pmatrix}1/3\\1/3\end{pmatrix},$$
so the new 3-speed is $x'/t'=1$ again — both components shrink by the same Doppler factor,
leaving the ratio fixed. Thus `apply(boost(0.8), [1,1,0,0])`$=[\tfrac13,\tfrac13,0,0]$ gives
`out[1]/out[0]`$=1.0$ and `classify(out)` is `"null"`: light moves at $c$ in every frame,
the postulate the module is built to honour.
