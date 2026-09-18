# MA-03 — Coordinate Systems (notes)

Citation keys (full details + PDF pages in `refs.md`): **B** = Boas 3e ·
**Gr** = Griffiths 4e. Pages are the *printed* book pages.

## 1. The three systems
$$\text{cylindrical: }x=\rho\cos\phi,\;y=\rho\sin\phi,\;z=z;$$
$$\text{spherical: }x=r\sin\theta\cos\phi,\;y=r\sin\theta\sin\phi,\;z=r\cos\theta,$$
with θ the polar angle from +z and φ the azimuth [B §5.4 pp.260–261; Gr §1.4.1
p.38 (spherical), §1.4.2 p.43 (cylindrical)]. Inverses use `atan2` for the
correct quadrant. Code: `cart_to_cyl/cyl_to_cart`, `cart_to_sph/sph_to_cart`.

## 2. Orthonormal basis vectors
Unlike **x̂ŷẑ**, the curvilinear unit vectors *depend on position*:
$$\hat{\mathbf e}_r=(s_\theta c_\phi,\,s_\theta s_\phi,\,c_\theta),\quad
  \hat{\mathbf e}_\theta=(c_\theta c_\phi,\,c_\theta s_\phi,\,-s_\theta),\quad
  \hat{\mathbf e}_\phi=(-s_\phi,\,c_\phi,\,0)$$
(s,c = sin,cos). They are orthonormal and right-handed: **ê_r×ê_θ = ê_φ** [Gr
§1.4.1 p.38]. Code: `sph_basis`, `cyl_basis`; the tests confirm |ê_i|=1,
ê_i·ê_j=δ_ij, and the cross-product handedness via MA-01.

A vector's components transform by projection onto this basis:
v_r = **v**·**ê_r**, etc. Code: `vector_to_spherical`/`vector_from_spherical`.

## 3. Scale factors
A small coordinate change dq_i moves you a physical distance h_i dq_i. For our
orthogonal systems [B Ch.10 §8 p.521, "scale factors" pp.522, 524]:
$$\text{cyl: }(h_\rho,h_\phi,h_z)=(1,\rho,1),\qquad
  \text{sph: }(h_r,h_\theta,h_\phi)=(1,r,r\sin\theta).$$
They carry all the geometry: arc length ds² = Σ(h_i dq_i)², and the operators of
`~MA-02` get h-factors in curvilinear form [B Ch.10 §9 p.525]. Code:
`cyl_scale_factors`, `sph_scale_factors`.

## 4. The volume element (Jacobian)
The volume element is the product of the scale factors [B §5.4 *Jacobians* p.258]:
$$dV=h_1h_2h_3\,dq_1dq_2dq_3:\quad
  \text{cyl }=\rho\,d\rho\,d\phi\,dz,\qquad
  \text{sph }=r^2\sin\theta\,dr\,d\theta\,d\phi.$$
Code: `cyl_jacobian` (= ρ), `sph_jacobian` (= r² sinθ); the test checks
J = h₁h₂h₃. This factor is why central-potential and spherically-symmetric
integrals (`~QM-12`, `~EM-04`) are done in spherical coordinates.
