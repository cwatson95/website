# MA-05 — Problems

Work by hand, then check with `code/complex_numbers.py`. Citations in `../refs.md`.

### P1.  Euler and the famous identity  *(Boas 3e §9, p.61)*
From e^{iθ}=cosθ+i sinθ, evaluate e^{iπ}, e^{iπ/2}, e^{2πi}, and confirm
e^{iπ}+1=0. *Check:* `euler(math.pi)`, `euler(math.pi/2)`.

**Solution.** Substitute each angle into Euler's formula $e^{i\theta}=\cos\theta+i\sin\theta$:
$$e^{i\pi}=\cos\pi+i\sin\pi=-1+0i=-1,\qquad e^{i\pi/2}=\cos\tfrac\pi2+i\sin\tfrac\pi2=0+i=i,$$
$$e^{2\pi i}=\cos 2\pi+i\sin 2\pi=1.$$
Hence $e^{i\pi}+1=-1+1=0$ — Euler's identity. (`euler(math.pi)` returns $-1$ up to a
$10^{-16}$ floating-point imaginary part, since $\sin\pi$ is not exactly $0$ numerically.)

### P2.  A De Moivre identity  *(Boas 3e §10, p.64)*
Use De Moivre with n=2 to derive cos2θ = cos²θ − sin²θ and sin2θ = 2 sinθ cosθ.
*Check:* compare `de_moivre(theta, 2)` to `euler(theta)**2`.

**Solution.** De Moivre's theorem gives $(\cos\theta+i\sin\theta)^2=\cos 2\theta+i\sin 2\theta$.
Expand the left side directly:
$$(\cos\theta+i\sin\theta)^2=\cos^2\theta+2i\sin\theta\cos\theta+i^2\sin^2\theta
=(\cos^2\theta-\sin^2\theta)+i\,(2\sin\theta\cos\theta).$$
Equating real and imaginary parts with $\cos 2\theta+i\sin 2\theta$:
$$\cos 2\theta=\cos^2\theta-\sin^2\theta,\qquad \sin 2\theta=2\sin\theta\cos\theta.$$
This is exactly why `de_moivre(theta, 2)` equals `euler(theta)**2`.

### P3.  The nth roots of unity  *(Boas 3e §10, p.64)*
Find the cube roots of 1 and the fourth roots of 1; show each set sums to zero
and lies on the unit circle. *Check:* `roots_of_unity(3)`, `roots_of_unity(4)`;
`sum(roots_of_unity(n))` ≈ 0.

**Solution.** Writing $1=e^{2\pi i k}$, the $n$th roots are $\omega_k=e^{2\pi i k/n}$,
$k=0,\dots,n-1$ — equally spaced on the unit circle ($|\omega_k|=1$). For $n=3$:
$$1,\quad e^{2\pi i/3}=-\tfrac12+\tfrac{\sqrt3}{2}i,\quad e^{4\pi i/3}=-\tfrac12-\tfrac{\sqrt3}{2}i.$$
For $n=4$: $\;1,\;i,\;-1,\;-i$. Each set sums to zero because it is a finite geometric
series: $\sum_{k=0}^{n-1}\omega_k=\dfrac{\omega^{\,n}-1}{\omega-1}=0$ (with $\omega=e^{2\pi i/n}$,
since $\omega^n=1$ and $\omega\ne1$ for $n\ge2$). Matches `sum(roots_of_unity(n))` ≈ 0.

### P4.  Roots of a general complex number  *(Boas 3e §10, p.64)*
Find all three cube roots of 8i and verify each, cubed, returns 8i.
*Check:* `nth_roots(complex(0,8), 3)`; each `w**3` ≈ 8i.

**Solution.** Put $8i$ in polar form: $8i=8\,e^{i\pi/2}$. Its cube roots are
$$w_k=8^{1/3}\,e^{i(\pi/2+2\pi k)/3}=2\,e^{i(\pi/6+2\pi k/3)},\qquad k=0,1,2,$$
i.e.
$$w_0=2e^{i\pi/6}=\sqrt3+i,\quad w_1=2e^{i5\pi/6}=-\sqrt3+i,\quad w_2=2e^{i3\pi/2}=-2i.$$
Cubing any one restores the modulus $2^3=8$ and triples the argument back to $\pi/2$
(mod $2\pi$), so $w_k^3=8i$. These are the values `nth_roots(complex(0,8), 3)` returns.

### P5.  The branch cut of √  *(Boas 3e §13, p.72)*
Compute the principal √(−1) = i. Then evaluate √ just above and just below the
negative real axis and observe the sign flip in the imaginary part — the
discontinuity across the cut. *Check:* `principal_sqrt(complex(-1, +1e-9))` vs
`principal_sqrt(complex(-1, -1e-9))`.

**Solution.** The principal square root uses the principal argument $\arg z\in(-\pi,\pi]$:
$\sqrt z=\sqrt{|z|}\,e^{i\arg z/2}$. For $z=-1$, $\arg z=\pi$, so
$$\sqrt{-1}=\sqrt1\,e^{i\pi/2}=i.$$
Approaching the negative real axis from **above** ($z=-1+i\varepsilon$), $\arg z\to\pi^-$,
giving $\sqrt z\to e^{i\pi/2}=i$; from **below** ($z=-1-i\varepsilon$), $\arg z\to-\pi^+$,
giving $\sqrt z\to e^{-i\pi/2}=-i$. The imaginary part jumps $+i\to-i$ across the cut —
the $2\pi$ ambiguity of $\arg$ halved to a sign by $\sqrt{\ }$. (`principal_sqrt` returns
$\approx +i$ and $\approx -i$ for the two cases.)
