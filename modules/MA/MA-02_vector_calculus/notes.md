# MA-02 — Vector Calculus (notes)

Citation keys (full details + PDF pages in `refs.md`): **B** = Boas 3e ·
**Gr** = Griffiths 4e. Page numbers are the *printed* book pages.

A **scalar field** assigns a number to each point, f(x,y,z); a **vector field**
assigns a vector, **F**(x,y,z). The operator ∇ = (∂/∂x, ∂/∂y, ∂/∂z) acts three ways.

## 1. Gradient
$$\nabla f=\Big(\frac{\partial f}{\partial x},\frac{\partial f}{\partial y},\frac{\partial f}{\partial z}\Big).$$
Points in the direction of steepest increase; its component along **û** is the
**directional derivative** D_û f = ∇f·**û** [B §6 p.290; Gr §1.2.2–1.2.3 p.13].
Code: `gradient(f)`, `directional_derivative(f, u)`.

## 2. Divergence and curl
$$\nabla\cdot\mathbf F=\frac{\partial F_x}{\partial x}+\frac{\partial F_y}{\partial y}+\frac{\partial F_z}{\partial z},
\qquad
\nabla\times\mathbf F=\Big(\partial_yF_z-\partial_zF_y,\ \partial_zF_x-\partial_xF_z,\ \partial_xF_y-\partial_yF_x\Big).$$
Divergence = net outflow per unit volume (a source density); curl = circulation
per unit area (a rotation density) [B §7 p.296; Gr §1.2.4 p.17, §1.2.5 p.18].
Code: `divergence(F)`, `curl(F)`.

## 3. Laplacian and the second-derivative identities
$$\nabla^2 f=\nabla\cdot\nabla f=\partial_x^2 f+\partial_y^2 f+\partial_z^2 f.$$
[B §7 p.297; Gr §1.2.7 p.23.] Two identities always hold (Gr §1.2.7):
$$\nabla\times(\nabla f)=\mathbf 0,\qquad \nabla\cdot(\nabla\times\mathbf F)=0.$$
Code: `laplacian(f)`; the identities are checked in the demo and tests.

## 4. Line integrals & conservative fields
The work / circulation integral is ∫_C **F**·d**l**. When **F** = ∇f it is
path-independent — the **fundamental theorem for gradients** [Gr §1.3.3 p.29]:
$$\int_{\mathbf a}^{\mathbf b}\nabla f\cdot d\mathbf l=f(\mathbf b)-f(\mathbf a).$$
[B §8 Line Integrals p.299.] Code: `line_integral(F, path, a, b)`.

## 5. The integral theorems
**Divergence (Gauss) theorem** [B §10 p.314; Gr §1.3.4 p.31, named p.32]:
$$\oint_{\partial V}\mathbf F\cdot d\mathbf S=\int_V(\nabla\cdot\mathbf F)\,dV.$$
**Stokes' theorem** [B §11 p.324; Gr §1.3.5 p.34]:
$$\oint_{\partial S}\mathbf F\cdot d\mathbf l=\int_S(\nabla\times\mathbf F)\cdot d\mathbf S.$$
**Green's theorem** is the planar special case of both [B §9 p.309].
Code checks: `line_integral` of (−y,x,0) round the unit circle = 2π = (curl_z)(πr²)
[Stokes]; `surface_flux` of **r** through the unit sphere = 4π = ∫div **r** dV [Gauss].

## Where this goes
These operators are the language of field physics: Gauss's law and the
continuity equation `~CM-22`/`~EM-13` are statements about divergence; Faraday
and Ampère are about curl; Laplace's & Poisson's equations `~EM-03` are about ∇².
Curvilinear-coordinate versions of all four are `~MA-03`.
