# CM-13 — Problems

Work by hand, then check with `code/rigid_body.py`. Citations in `../refs.md`.

### P1.  Inertia tensor of point masses  *(Fowles 7e §9.1, p.361)*
For four equal masses at (±a,0,0) and (0,±a,0) compute I and show it is
diag(2,2,4)ma². *Check:* `inertia_tensor([m]*4, pts)`.
*Answer:* $I=\mathrm{diag}(2,2,4)\,ma^2$; the off-diagonals vanish because each mass sits on an axis.

**Solution.** Use $I_{ij}=\sum_\alpha m_\alpha\big(r_\alpha^2\delta_{ij}-r_{\alpha,i}r_{\alpha,j}\big)$ with all $m_\alpha=m$ and $r_\alpha^2=a^2$. The two masses on the $x$-axis, $(\pm a,0,0)$, add $0$ to $I_{xx}$ (since $r^2-x^2=0$) and $ma^2$ each to $I_{yy}$ and $I_{zz}$; the two on the $y$-axis add $ma^2$ each to $I_{xx}$ and $I_{zz}$ and $0$ to $I_{yy}$. Every off-diagonal $I_{xy}=-\sum m\,xy$ etc. vanishes because each mass has a zero coordinate. Summing,
$$I=ma^2\begin{pmatrix}2&0&0\\0&2&0\\0&0&4\end{pmatrix}=\mathrm{diag}(2,2,4)\,ma^2.$$
`inertia_tensor([1]*4, pts)` returns exactly $\mathrm{diag}(2,2,4)$ for $m=a=1$.

### P2.  Principal axes by diagonalization  *(Fowles 7e §9.2, p.371; Marion & Thornton 5e §11.5, p.424)*
Show the principal moments are the eigenvalues of I and the principal axes its
orthonormal eigenvectors. *Check:* `principal_axes(I)` (reuses MA-04).
*Answer:* principal moments $=$ eigenvalues of $I$; principal axes $=$ its orthonormal eigenvectors (real and orthogonal because $I$ is symmetric).

**Solution.** A principal axis is a direction $\hat{\mathbf e}$ along which $\mathbf L=I\hat{\mathbf e}$ is parallel to $\hat{\mathbf e}$, i.e.
$$I\hat{\mathbf e}=I_k\,\hat{\mathbf e},$$
which is exactly the eigenvalue equation: the principal moments $I_k$ are the eigenvalues and the principal axes the eigenvectors. Since $I_{ij}=I_{ji}$ is real symmetric, the spectral theorem guarantees real eigenvalues and an orthonormal eigenbasis, so $I=Q\,\mathrm{diag}(I_1,I_2,I_3)\,Q^{\mathsf T}$ with $Q$ orthogonal. `principal_axes(I)` (MA-04's `eig_symmetric`) returns moments $[2,2,4]$ and axes that the test confirms satisfy $\hat{\mathbf e}_i\cdot\hat{\mathbf e}_j=\delta_{ij}$.

### P3.  Moment about an axis  *(Fowles 7e §9.1, p.361)*
Show I_n = **n**·I**n** for a unit axis **n**, and that for the body of P1 the
moment about ẑ is 4ma². *Check:* `moment_about_axis(I, (0,0,1))`.
*Answer:* $I_n=\mathbf n\cdot I\,\mathbf n$; for $\hat{\mathbf z}$ it equals $I_{zz}=4ma^2$ ($=4$ for $m=a=1$).

**Solution.** The scalar moment about an axis through the origin along unit $\mathbf n$ is $I_n=\sum_\alpha m_\alpha d_\alpha^2$, with $d_\alpha$ the perpendicular distance of mass $\alpha$ from the axis: $d_\alpha^2=r_\alpha^2-(\mathbf n\cdot\mathbf r_\alpha)^2$. Then, using $\mathbf n\cdot\mathbf n=1$,
$$I_n=\sum_\alpha m_\alpha\big[r_\alpha^2(\mathbf n\cdot\mathbf n)-(\mathbf n\cdot\mathbf r_\alpha)^2\big]=\mathbf n\cdot\Big[\sum_\alpha m_\alpha\big(r_\alpha^2\,\mathbb 1-\mathbf r_\alpha\mathbf r_\alpha^{\mathsf T}\big)\Big]\mathbf n=\mathbf n\cdot I\,\mathbf n.$$
For $\mathbf n=\hat{\mathbf z}$ this picks out $I_{zz}=4ma^2$. Accordingly `moment_about_axis(I,(0,0,1))` $=4$, while `(1,0,0)` gives $I_{xx}=2$ (the routine normalizes non-unit axes first).

### P4.  L is parallel to ω only along a principal axis  *(Marion & Thornton 5e §11.3, p.415)*
Show **L** = I**ω** is parallel to **ω** iff **ω** is a principal axis (an
eigenvector). *Check:* `angular_momentum(I, v)` = λ**v** for each principal v.
*Answer:* $\mathbf L\parallel\boldsymbol\omega\iff I\boldsymbol\omega=\lambda\boldsymbol\omega\iff\boldsymbol\omega$ is an eigenvector (principal axis), with $\lambda$ the principal moment.

**Solution.** "$\mathbf L=I\boldsymbol\omega$ parallel to $\boldsymbol\omega$" means $\mathbf L=\lambda\boldsymbol\omega$ for some scalar $\lambda$, i.e.
$$I\boldsymbol\omega=\lambda\boldsymbol\omega,$$
precisely the statement that $\boldsymbol\omega$ is an eigenvector of $I$ — a principal axis — with eigenvalue the principal moment $\lambda$. If $\boldsymbol\omega$ is not an eigenvector, $I\boldsymbol\omega$ points in another direction and $\mathbf L$ wobbles around $\boldsymbol\omega$. For each principal axis $\mathbf v$, `angular_momentum(I, v)` $=I\mathbf v=\lambda\mathbf v$; e.g. $\boldsymbol\omega=(0,0,3)$ along the principal $\hat{\mathbf z}$ gives $\mathbf L=(0,0,12)=4\boldsymbol\omega$, parallel.

### P5.  Principal moments are rotation-invariant
Rotate the whole body and show the eigenvalues of I do not change — they are
intrinsic. *Check:* re-`principal_axes` after rotating the positions.
*Answer:* under a body rotation $R$, $I\to RIR^{\mathsf T}$; an orthogonal similarity preserves eigenvalues, so the principal moments are unchanged (only the axes rotate).

**Solution.** Rotating the body by orthogonal $R$ sends every position $\mathbf r\to R\mathbf r$. Each term transforms as $m\big(r^2\mathbb 1-\mathbf r\mathbf r^{\mathsf T}\big)\to m\big(r^2\mathbb 1-R\mathbf r\mathbf r^{\mathsf T}R^{\mathsf T}\big)=R\,m\big(r^2\mathbb 1-\mathbf r\mathbf r^{\mathsf T}\big)R^{\mathsf T}$, using $|R\mathbf r|=|\mathbf r|$ and $R\,\mathbb 1\,R^{\mathsf T}=\mathbb 1$, so
$$I\ \longrightarrow\ R\,I\,R^{\mathsf T}.$$
An orthogonal similarity preserves the spectrum: if $I\hat{\mathbf e}=\lambda\hat{\mathbf e}$ then $(RIR^{\mathsf T})(R\hat{\mathbf e})=\lambda(R\hat{\mathbf e})$. Hence the principal moments $\{I_1,I_2,I_3\}$ are unchanged — only the axes rotate with the body. Re-running `principal_axes` after rotating the positions returns the same moments (the test matches them to $10^{-7}$).
