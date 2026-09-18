# MA-01 — Problems

Work them by hand, then check with `code/vector_algebra.py`. Sources in `../refs.md`.

### P1.  BAC–CAB by components  *(Griffiths 4e, Prob. 1.5, p.8)*
Prove a×(b×c) = b(a·c) − c(a·b) by writing out one component with the ε–δ
identity εᵢⱼₖεᵢₗₘ = δⱼₗδₖₘ − δⱼₘδₖₗ.
*Check:* `vector_algebra._demo()` proves it symbolically with SymPy.

**Solution.** Write the $i$-th component with the Levi-Civita symbol, using $(\mathbf a\times\mathbf b)_i=\varepsilon_{ijk}a_jb_k$ twice:
$$[\mathbf a\times(\mathbf b\times\mathbf c)]_i=\varepsilon_{ijk}a_j(\mathbf b\times\mathbf c)_k=\varepsilon_{ijk}\varepsilon_{klm}\,a_j b_l c_m.$$
Cycle the first symbol, $\varepsilon_{ijk}=\varepsilon_{kij}$, so $\varepsilon_{kij}\varepsilon_{klm}=\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl}$ (the ε–δ identity with shared index $k$). Then
$$[\mathbf a\times(\mathbf b\times\mathbf c)]_i=(\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl})a_j b_l c_m=b_i\,(a_jc_j)-c_i\,(a_jb_j)=b_i(\mathbf a\cdot\mathbf c)-c_i(\mathbf a\cdot\mathbf b).$$
Since this holds for every $i$, $\mathbf a\times(\mathbf b\times\mathbf c)=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b)$ — exactly the BAC–CAB identity `vector_algebra._demo()` confirms symbolically.

### P2.  Angle between body diagonals of a cube  *(Griffiths 4e, Prob. 1.3, p.7)*
Find the angle between two body diagonals of a cube.
*Answer:* arccos(1/3) ≈ 70.53°.
*Check:* `angle((1,1,1), (-1,1,1))` (place the cube corner at the origin).
*(Don't confuse with Griffiths Example 1.2, p.6, which does the* face *diagonals → 60°.)*

**Solution.** With a unit cube cornered at the origin, two body diagonals point along $\mathbf a=(1,1,1)$ and $\mathbf b=(-1,1,1)$. Their dot product and magnitudes are
$$\mathbf a\cdot\mathbf b=-1+1+1=1,\qquad |\mathbf a|=|\mathbf b|=\sqrt3.$$
Hence $\cos\theta=\dfrac{\mathbf a\cdot\mathbf b}{|\mathbf a||\mathbf b|}=\dfrac{1}{\sqrt3\cdot\sqrt3}=\dfrac13$, so
$$\theta=\arccos\tfrac13=70.5288^\circ.$$
This is exactly the value `angle((1,1,1), (-1,1,1))` returns (≈ $70.5288^\circ$), which uses the numerically stable $\operatorname{atan2}(|\mathbf a\times\mathbf b|,\mathbf a\cdot\mathbf b)$ form.

### P3.  Volume & coplanarity
Given a = (1,0,0), b = (1,1,0), c = (1,1,1): find the parallelepiped volume, then
decide whether (2,1,0) lies in the plane of a and b.
*Answer:* `box_volume(a,b,c) = 1`; `are_coplanar((1,0,0),(1,1,0),(2,1,0)) → True`.

**Solution.** The signed volume is the scalar triple product $\mathbf a\cdot(\mathbf b\times\mathbf c)=\det[\mathbf a\ \mathbf b\ \mathbf c]$:
$$\det\begin{pmatrix}1&0&0\\1&1&0\\1&1&1\end{pmatrix}=1\,(1\cdot1-0\cdot1)=1,$$
so the parallelepiped volume is $|1|=1$. For coplanarity of $(1,0,0),(1,1,0),(2,1,0)$, all three vectors have zero $z$-component, so they lie in the $z=0$ plane and their triple product vanishes:
$$\det\begin{pmatrix}1&0&0\\1&1&0\\2&1&0\end{pmatrix}=0.$$
Thus `box_volume(a,b,c)` $=1$ and `are_coplanar(...)` $\to$ `True`, matching the stated answers.

### P4.  Area of a triangle in space
The triangle with vertices P, Q, R has area ½|PQ × PR|. Compute it for
P=(0,0,0), Q=(1,2,0), R=(0,3,4).
*Check:* `0.5 * norm(cross((1,2,0),(0,3,4)))`.

**Solution.** The edge vectors from $P$ are $\overrightarrow{PQ}=(1,2,0)$ and $\overrightarrow{PR}=(0,3,4)$. Their cross product is
$$\overrightarrow{PQ}\times\overrightarrow{PR}=\begin{vmatrix}\hat x&\hat y&\hat z\\1&2&0\\0&3&4\end{vmatrix}=(2\cdot4-0\cdot3,\ 0\cdot0-1\cdot4,\ 1\cdot3-2\cdot0)=(8,-4,3).$$
Its magnitude is $|(8,-4,3)|=\sqrt{64+16+9}=\sqrt{89}$, so the triangle area is
$$\tfrac12|\overrightarrow{PQ}\times\overrightarrow{PR}|=\tfrac12\sqrt{89}=4.71699.$$
This matches `0.5 * norm(cross((1,2,0),(0,3,4)))` ≈ $4.71699$.

### P5.  A trajectory (bridge to CM-01 / CM-09)
For the helix r(t) = (cos t, sin t, t) with v = r′, w = v′:
1. Show the speed |v| is constant. *(= √2)*
2. Show the specific angular momentum ℓ(t) = r×v is **not** constant (no central
   force), and compute dℓ/dt = r×w.
*Check:* build `speed = norm(v)`, `l = cross(r, v)` as functions and sample them;
compare `[l(t+h)-l(t)]/h` against `cross(r, w)(t)`.

**Solution.** Differentiating, $\mathbf v=\mathbf r'=(-\sin t,\cos t,1)$ and $\mathbf w=\mathbf v'=(-\cos t,-\sin t,0)$. The speed is
$$|\mathbf v|=\sqrt{\sin^2 t+\cos^2 t+1}=\sqrt2,$$
constant. The specific angular momentum is
$$\boldsymbol\ell=\mathbf r\times\mathbf v=(\sin t-t\cos t,\ -(t\sin t+\cos t),\ \cos^2 t+\sin^2 t)=(\sin t-t\cos t,\ -t\sin t-\cos t,\ 1).$$
Its $x,y$ components vary with $t$, so $\boldsymbol\ell$ is not constant; differentiating (or using $\dot{\boldsymbol\ell}=\mathbf r\times\mathbf w$ since $\mathbf v\times\mathbf v=0$) gives
$$\frac{d\boldsymbol\ell}{dt}=\mathbf r\times\mathbf w=(t\sin t,\ -t\cos t,\ 0).$$
At $t=0.7$ both the finite difference and $\mathbf r\times\mathbf w$ give $(0.45095,-0.53539,0)$, confirming $\dot{\boldsymbol\ell}=\mathbf r\times\mathbf w\neq\mathbf 0$ (the helix feels a non-central force), exactly as the sampled `cross(r, w)` check shows.
