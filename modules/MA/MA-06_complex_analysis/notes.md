# MA-06 — Complex Analysis (notes)

Citation keys (details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are the *printed* book pages. (Butkov is image-only and
cited at chapter level in `refs.md`, without page numbers.)

## 1. Analytic functions & Cauchy–Riemann
f = u(x,y) + i v(x,y) is **analytic** at z if f′(z) exists in a neighbourhood —
equivalently u, v satisfy the **Cauchy–Riemann** equations [B §14.2 p.667 (C–R
stated p.669)]:
$$\frac{\partial u}{\partial x}=\frac{\partial v}{\partial y},\qquad
  \frac{\partial u}{\partial y}=-\frac{\partial v}{\partial x}.$$
Then f′ is the same in every direction, so a real step computes it. Code:
`cauchy_riemann`, `complex_derivative`. (z² and eᶻ pass; z̄ and Re z fail.)

## 2. Contour integrals & Cauchy's theorem
For a contour γ(t),
$$\int_\gamma f\,dz=\int_a^b f(\gamma(t))\,\gamma'(t)\,dt.$$
**Cauchy's integral theorem** [B §14.3 p.674]: if f is analytic on
and inside a closed contour, ∮f dz = 0. The canonical exception is ∮ dz/z = 2πi
around the origin (1/z is not analytic at 0). Code: `contour_integral`.

## 3. Cauchy's integral formula
For f analytic inside the loop around z₀ [B §14.3 Thm VI p.675 (eq. 3.9 p.676)]:
$$f(z_0)=\frac{1}{2\pi i}\oint\frac{f(z)}{z-z_0}\,dz.$$
A function's interior values are fixed by its boundary values — the analytic
analogue of the mean-value property. Code: `cauchy_integral_formula`.

## 4. Residues & the residue theorem
Near an isolated singularity f has a Laurent series [B §14.4 p.678]
Σ aₙ(z−z₀)ⁿ; the **residue** is a₋₁. The **residue theorem** [B §14.5 p.682
(eq. 5.2 p.683)]:
$$\oint_\gamma f\,dz=2\pi i\sum(\text{residues enclosed}).$$
A residue is itself a small-circle integral, Res = (1/2πi)∮ f dz. The **winding
number** (1/2πi)∮ dz/(z−z₀) counts how many times γ encircles z₀. Code:
`residue_at`, `winding_number`; the test verifies ∮ = 2πi·Σres.

## Where this goes
Residues evaluate real integrals and sums that have no elementary antiderivative,
and they are the backbone of propagators and Green's functions in `~QM-19`; the
analytic structure of response functions gives the Kramers–Kronig relations in
`~EM-15`.
