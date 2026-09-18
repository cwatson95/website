# CM-16 — Problems

Work by hand, then check with `code/normal_modes.py`. Citations in `../refs.md`.

### P1.  Two coupled masses  *(Fowles 7e §11.3, p.472)*
For two equal masses joined by three identical springs (K = [[2k,−k],[−k,2k]]),
find the normal frequencies √(k/m) and √(3k/m) and their mode shapes (in-phase,
out-of-phase). *Check:* `normal_modes([[2,-1],[-1,2]], [1,1])`.
*Answer:* $\omega=\sqrt{k/m}=1$ for the in-phase mode $(1,1)/\sqrt2$ and $\omega=\sqrt{3k/m}=\sqrt3$ for the out-of-phase mode $(1,-1)/\sqrt2$.

**Solution.** With $M=mI$ the problem $K\mathbf v=\omega^2 m\mathbf v$ is the ordinary eigenproblem of $K=k[[2,-1],[-1,2]]$. The characteristic equation is
$$\det(K-\lambda I)=(2k-\lambda)^2-k^2=0\ \Rightarrow\ \lambda=k,\,3k,$$
so $\omega=\sqrt{k/m}$ and $\sqrt{3k/m}$. For $\lambda=k$: $(2k-k)v_1=kv_2\Rightarrow v_1=v_2$, the in-phase mode $(1,1)/\sqrt2$ (the middle spring never stretches — lower $\omega$). For $\lambda=3k$: $v_2=-v_1$, the out-of-phase mode $(1,-1)/\sqrt2$ (middle spring maximally stretched — higher $\omega$). With $k=m=1$, `normal_modes([[2,-1],[-1,2]],[1,1])` returns frequencies $[1.0,1.7321]$ and exactly these shapes.

### P2.  The generalized eigenproblem  *(Marion & Thornton 5e §12.6, p.483)*
Show every mode satisfies K**v** = ω²M**v**. *Check:* verify the relation
component-by-component for unequal masses.
*Answer:* substituting $\mathbf x=\mathbf v\,e^{i\omega t}$ into $M\ddot{\mathbf x}=-K\mathbf x$ gives $K\mathbf v=\omega^2 M\mathbf v$.

**Solution.** The small-oscillation equations are $M\ddot{\mathbf x}=-K\mathbf x$. A normal mode oscillates rigidly, $\mathbf x=\mathbf v\,e^{i\omega t}$, so $\ddot{\mathbf x}=-\omega^2\mathbf x$ and
$$-\omega^2 M\mathbf v=-K\mathbf v\quad\Longleftrightarrow\quad K\mathbf v=\omega^2 M\mathbf v,$$
a generalized (mass-weighted) eigenproblem. The code reduces it to the symmetric eigenproblem of $A=M^{-1/2}KM^{-1/2}$ and maps the eigenvectors back via $\mathbf v=M^{-1/2}\mathbf u$, so each returned $(\omega,\mathbf v)$ satisfies the relation by construction. Component-by-component $(K\mathbf v)_i=\omega^2 M_i v_i$, which the test verifies for $K=[[3,-1],[-1,2]]$, $M=[2,1]$ to $10^{-7}$.

### P3.  Mass-orthonormality  *(Fowles 7e §11.3, p.472)*
Show distinct normal modes are orthogonal in the mass inner product vₐᵀMv_b = δ_ab.
*Check:* `mode_inner_product(M, modes[a], modes[b])`.
*Answer:* $\mathbf v_a^{\top} M\,\mathbf v_b=\delta_{ab}$ — the modes are orthonormal in the mass metric.

**Solution.** The reduced matrix $A=M^{-1/2}KM^{-1/2}$ is real symmetric, so its eigenvectors can be chosen orthonormal, $\mathbf u_a^{\top}\mathbf u_b=\delta_{ab}$. The physical modes are $\mathbf v=M^{-1/2}\mathbf u$, hence
$$\mathbf v_a^{\top} M\,\mathbf v_b=(M^{-1/2}\mathbf u_a)^{\top} M\,(M^{-1/2}\mathbf u_b)=\mathbf u_a^{\top}\,M^{-1/2}MM^{-1/2}\,\mathbf u_b=\mathbf u_a^{\top}\mathbf u_b=\delta_{ab}.$$
So distinct modes are orthogonal and each is normalized in the mass inner product (physically, the modes simultaneously diagonalize the kinetic and potential energies). `mode_inner_product(M, modes[a], modes[b])` then returns $\delta_{ab}$ to $10^{-7}$ for the 3-mass $K=[[3,-1,0],[-1,2,-1],[0,-1,3]]$, $M=[1,2,1]$.

### P4.  Three-mass chain  *(Fowles 7e §11.3, p.472)*
For a fixed–fixed chain of three equal masses & springs show ω_j² = (2k/m)(1 −
cos(jπ/4)), j = 1,2,3. *Check:* `normal_modes` of the 3×3 tridiagonal K.
*Answer:* $\omega_j=\sqrt{(2k/m)(1-\cos(j\pi/4))}=\{0.7654,\,1.4142,\,1.8478\}\sqrt{k/m}$ for $j=1,2,3$.

**Solution.** The fixed–fixed chain has $K=k[[2,-1,0],[-1,2,-1],[0,-1,2]]$, $M=mI$. With walls at $n=0,4$ the modes are standing waves $v^{(j)}_n=\sin(nj\pi/4)$; acting with the tridiagonal $K$ on a sine multiplies it by the discrete-Laplacian eigenvalue $2-2\cos(j\pi/4)$, so
$$\omega_j^2=\frac{k}{m}\big(2-2\cos(j\pi/4)\big)=\frac{2k}{m}\big(1-\cos(j\pi/4)\big),\qquad j=1,2,3.$$
Numerically $\omega_j^2=\{0.586,\,2,\,3.414\}\,k/m$, i.e. $\omega_j=\{0.7654,1.4142,1.8478\}\sqrt{k/m}$ — exactly what `normal_modes` of the $3\times3$ tridiagonal $K$ returns ($k=m=1$).

### P5.  Normal coordinates decouple  *(Marion & Thornton 5e §12.6, p.483)*
Explain how transforming to normal coordinates turns the coupled equations into
independent simple oscillators (`~CM-15`), each a single Fourier tone (`~MA-09`).
*Answer:* in normal coordinates $q_j$ the system becomes $\ddot q_j+\omega_j^2 q_j=0$ — independent oscillators, each a single tone.

**Solution.** Collect the mass-orthonormal modes as the columns of $P$, so that $P^{\top}MP=I$ and $P^{\top}KP=\operatorname{diag}(\omega_j^2)$. Define normal coordinates $\mathbf q=P^{-1}\mathbf x$, i.e. $\mathbf x=\sum_j q_j\mathbf v_j$. Substituting into $M\ddot{\mathbf x}=-K\mathbf x$ and left-multiplying by $P^{\top}$,
$$\ddot{\mathbf q}+\operatorname{diag}(\omega_j^2)\,\mathbf q=0\quad\Longrightarrow\quad \ddot q_j+\omega_j^2 q_j=0\ \ (\text{each }j).$$
The coupling is gone: each $q_j(t)=C_j\cos(\omega_j t+\varphi_j)$ is an independent `~CM-15` oscillator — a single Fourier tone (`~MA-09`) — and a general motion is the superposition $\mathbf x(t)=\sum_j q_j(t)\,\mathbf v_j$. The $P$ whose columns diagonalize both $T$ and $U$ is exactly the mass-orthonormal set returned by `normal_modes` ($P^{\top}MP=I$ via `mode_inner_product`).
