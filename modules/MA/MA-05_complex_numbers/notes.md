# MA-05 — Complex Numbers (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages.

## 1. The complex plane and polar form
z = x + iy is a point (x, y). Its **modulus** |z| = √(x²+y²) and **argument**
arg z = atan2(y, x) give the polar form [B §3 p.47, §4 p.49]:
$$z=r(\cos\theta+i\sin\theta),\qquad r=|z|,\ \theta=\arg z.$$
Code: `modulus`, `argument`, `to_polar`, `from_polar`. The **conjugate**
z̄ = x − iy satisfies z z̄ = |z|².

## 2. Euler's formula
$$e^{i\theta}=\cos\theta+i\sin\theta$$
[B §9 p.61] — the single most useful identity here. So z = r e^{iθ}, and the
unit circle is θ ↦ e^{iθ}. Special case e^{iπ}+1 = 0. Code: `euler`.

## 3. De Moivre, powers and roots
Multiplying multiplies moduli and adds arguments, so powers are easy [B §10 p.64]:
$$(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta\quad(\textbf{De Moivre}),
\qquad z^n=r^n e^{in\theta}.$$
Going backwards, every nonzero z has exactly **n distinct nth roots**, equally
spaced by 2π/n on a circle of radius r^{1/n}:
$$z^{1/n}=r^{1/n}\,e^{i(\theta+2\pi k)/n},\quad k=0,\dots,n-1.$$
The nth **roots of unity** (z=1) are e^{2πik/n}; they sum to zero for n ≥ 2.
Code: `de_moivre`, `power`, `nth_roots`, `roots_of_unity`.

## 4. The principal branch of √ and log
Because arg is multivalued (θ + 2πk all give the same point), √ and log need a
choice. Taking the **principal value** arg ∈ (−π, π] [B §11 exp p.67, §13 log p.72]:
$$\sqrt z=\sqrt r\,e^{i\theta/2},\qquad \operatorname{Log}z=\ln|z|+i\arg z.$$
This is single-valued except across the **negative real axis**, where arg jumps
by 2π — the *branch cut*. (Boas calls this the "principal value"; the word
"branch" is the complex-analysis term you'll meet in `~MA-06`.) Code:
`principal_sqrt`, `principal_log`; the test samples just above/below the cut to
show the sign flip.

## Where this goes
e^{iωt} turns oscillations and AC steady state into algebra (`~CM-15`, `~EM-12`);
complex amplitudes carry phase in waves and quantum states (`~QM-02`); and the
characteristic polynomial can hand you complex eigenvalues (`~MA-04`,
`eigvals_2x2` of a rotation = ±i).
