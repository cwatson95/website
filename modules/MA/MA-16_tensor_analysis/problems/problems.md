# MA-16 — Problems

Work by hand, then check with `code/tensors.py`. Citations in `../refs.md`.

### P1.  Summation convention  *(Boas 3e §3, p.502)*
Rewrite, then evaluate with the convention: tr(AB)=A_ij B_ji, the matrix–vector
product (Ax)_i=A_ij x_j, and δ_ij a_j = a_i. Why must a repeated (summed) index
appear exactly twice? *Check:* `matvec`.

**Solution.** Each index appearing twice is summed; an index appearing once is *free* and labels a component of the result:
$$(A\mathbf x)_i=\sum_j A_{ij}x_j=A_{ij}x_j,\qquad \operatorname{tr}(AB)=(AB)_{ii}=A_{ij}B_{ji},\qquad \delta_{ij}a_j=a_i,$$
the last because $\delta_{ij}$ is nonzero only at $j=i$, so it *renames* the summed index. A summed index must appear **exactly twice**: it stands for a single contraction (one $\sum$), and the free indices must balance on both sides; a third occurrence would leave the contraction ambiguous and the object would no longer transform as a tensor. `matvec(A, x)` computes exactly $A_{ij}x_j$ — $j$ summed, $i$ free.

### P2.  Cross product and curl from ε  *(Boas 3e §5, p.508)*
Show (a×b)_i = ε_{ijk} a_j b_k and confirm it equals the elementary determinant
formula. *Check:* `cross_via_levi_civita([1,2,3], [4,5,6])` → [−3, 6, −3].

**Solution.** With the totally antisymmetric symbol ($\varepsilon_{123}=+1$), expand the contraction one free index at a time:
$$(a\times b)_1=\varepsilon_{1jk}a_jb_k=\varepsilon_{123}a_2b_3+\varepsilon_{132}a_3b_2=a_2b_3-a_3b_2,$$
and cyclically $(a\times b)_2=a_3b_1-a_1b_3$, $(a\times b)_3=a_1b_2-a_2b_1$ — precisely the cofactor rows of the determinant $\det\!\begin{pmatrix}\hat e_1&\hat e_2&\hat e_3\\ a_1&a_2&a_3\\ b_1&b_2&b_3\end{pmatrix}$. For $a=(1,2,3),\,b=(4,5,6)$: $2\cdot6-3\cdot5=-3$, $3\cdot4-1\cdot6=6$, $1\cdot5-2\cdot4=-3$, giving $[-3,6,-3]$ — exactly `cross_via_levi_civita([1,2,3], [4,5,6])`.

### P3.  The ε–δ identity ⇒ BAC–CAB  *(Boas 3e §5, p.508)*
Prove Σ_i ε_{ijk}ε_{ilm}=δ_{jl}δ_{km}−δ_{jm}δ_{kl}, then use it to derive
a×(b×c)=b(a·c)−c(a·b). *Check:* `eps_delta_identity_holds()`.

**Solution.** The sum $\sum_i\varepsilon_{ijk}\varepsilon_{ilm}$ is nonzero only when $\{j,k\}=\{l,m\}$ with $j\ne k$. If $(l,m)=(j,k)$ the two symbols are equal, product $+1\Rightarrow\delta_{jl}\delta_{km}$; if $(l,m)=(k,j)$ they have opposite sign, product $-1\Rightarrow-\delta_{jm}\delta_{kl}$. Hence $\sum_i\varepsilon_{ijk}\varepsilon_{ilm}=\delta_{jl}\delta_{km}-\delta_{jm}\delta_{kl}$. Apply it to the double cross product, using the cyclic relabel $\varepsilon_{ijk}=\varepsilon_{kij}$:
$$[a\times(b\times c)]_i=\varepsilon_{ijk}a_j\,\varepsilon_{klm}b_lc_m=(\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl})\,a_jb_lc_m=b_i(a_jc_j)-c_i(a_jb_j),$$
i.e. $a\times(b\times c)=b\,(a\cdot c)-c\,(a\cdot b)$ — the BAC–CAB rule. `eps_delta_identity_holds()` verifies the identity over all $j,k,l,m$ and returns `True`.

### P4.  Determinant as an antisymmetric contraction  *(Boas 3e §5, p.508)*
Write det A = ε_{i₁…iₙ}A_{1i₁}…A_{niₙ} and evaluate a 3×3 by hand; confirm the
inverse via adj/det. *Check:* `det_levi_civita`, `inverse`.

**Solution.** The Levi-Civita definition antisymmetrizes the column index:
$$\det A=\varepsilon_{ijk}A_{1i}A_{2j}A_{3k}=\sum_\sigma\operatorname{sgn}(\sigma)\,A_{1\sigma_1}A_{2\sigma_2}A_{3\sigma_3}.$$
For $A=\begin{pmatrix}2&1&0\\1&3&1\\0&1&2\end{pmatrix}$, expanding along row 1, $\det A=2(3\cdot2-1\cdot1)-1(1\cdot2-1\cdot0)+0=2(5)-2=8.$ The inverse follows from Cramer, $A^{-1}=\operatorname{adj}(A)/\det A=C^{\mathsf T}/\det A$ with $C_{ij}=(-1)^{i+j}M_{ij}$; e.g. $(A^{-1})_{11}=C_{11}/8=5/8=0.625$. `det_levi_civita(A)` returns $8.0$ and `inverse(A)` returns $[[0.625,-0.25,0.125],[-0.25,0.5,-0.25],[0.125,-0.25,0.625]]$, matching adj/det.

### P5.  The metric of curvilinear coordinates  *(Boas 3e §8 p.521; §10 p.529)*
From x=r cosθ, y=r sinθ compute g_ij=(JᵀJ)_ij=diag(1,r²), giving ds²=dr²+r²dθ².
Repeat for spherical → diag(1,r²,r²sin²θ). *Check:* `metric_from_map(polar, [r,θ])`.

**Solution.** The Cartesian embedding $x(r,\theta)=(r\cos\theta,\,r\sin\theta)$ has Jacobian $J_{ki}=\partial x^k/\partial q^i$,
$$J=\begin{pmatrix}\cos\theta & -r\sin\theta\\ \sin\theta & r\cos\theta\end{pmatrix},\qquad g=J^{\mathsf T}J.$$
Then $g_{rr}=\cos^2\theta+\sin^2\theta=1$, $g_{\theta\theta}=r^2\sin^2\theta+r^2\cos^2\theta=r^2$, $g_{r\theta}=-r\sin\theta\cos\theta+r\sin\theta\cos\theta=0$, so $g=\operatorname{diag}(1,r^2)$ and $ds^2=dr^2+r^2d\theta^2$. The identical computation for $x(r,\theta,\phi)$ gives $g=\operatorname{diag}(1,r^2,r^2\sin^2\theta)$. `metric_from_map(_polar, [2,0.7])` returns $[[1,0],[0,4]]$ ($r^2=4$), matching.

### P6.  Covariant invariance of length  *(Boas 3e §10, p.529)*
Show that for a contravariant vector vⁱ the scalar g_ij vⁱvʲ is the same in polar
and Cartesian coordinates (the metric "undoes" the coordinate stretch). *Check:*
`inner(g, v, v)` equals the Cartesian Σ(Vᵏ)² with V=Jv.

**Solution.** The contravariant components transform with the Jacobian, $V^k=(Jv)^k=\dfrac{\partial x^k}{\partial q^i}v^i$. The Cartesian metric is $\delta_{kl}$, so
$$|V|^2=\sum_k (V^k)^2=\delta_{kl}\frac{\partial x^k}{\partial q^i}\frac{\partial x^l}{\partial q^j}v^iv^j=\Big(\sum_k\frac{\partial x^k}{\partial q^i}\frac{\partial x^k}{\partial q^j}\Big)v^iv^j=g_{ij}v^iv^j,$$
since the bracket is exactly the induced metric $g_{ij}=(J^{\mathsf T}J)_{ij}$. The metric's $r^2$ precisely undoes the coordinate stretch in $V$. Numerically at $(r,\theta)=(2,0.7)$ with $v=(0.3,0.25)$, `inner(g, v, v)` $=g_{ij}v^iv^j=0.340000$ equals $\sum_k(V^k)^2=0.340000$ with $V=Jv$ — matching `inner`.
