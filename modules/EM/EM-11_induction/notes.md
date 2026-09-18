# EM-11 — Electromagnetic Induction (notes)

Induction is the response of circuits and fields to a **changing magnetic flux**.
The central law is **Faraday's**; everything here is built from the magnetic flux
Φ = ∫**B**·d**a** (the `~MA-02` surface integral of the `~EM-08` field **B**) and the
single constant μ₀ = `MU0`.

Citation key (full details + PDF pages in `refs.md`): **Gr** = Griffiths 4e. Page
numbers are the *printed* book pages. The EMF is written $\mathcal{E}$.

## 1. Faraday's law and Lenz
A changing flux through a loop drives an electromotive force (Gr §7.2.1, p.312):
$$\mathcal{E}=-\frac{d\Phi}{dt},\qquad \Phi=\int\mathbf B\cdot d\mathbf a .$$
The minus sign is **Lenz's law**: the induced current flows so that *its own* flux
opposes the change that produced it — nature resists the change in flux. Code:
`magnetic_flux` (= MA-02 `surface_flux`) for Φ, `faraday_emf` for −dΦ/dt by a
central difference in $t$, and `lenz_sign` for the sense. The worked demo takes
$\Phi(t)=B_0A\sin\omega t$ and recovers $\mathcal{E}=-B_0A\omega\cos\omega t$.

## 2. The induced electric field
When the flux changes because **B** itself varies in time, the EMF is carried by a
real **electric field that is not electrostatic** (Gr §7.2.2, Eq. 7.18, p.317):
$$\nabla\times\mathbf E=-\frac{\partial\mathbf B}{\partial t}
  \qquad\Longleftrightarrow\qquad \oint\mathbf E\cdot d\mathbf l=-\frac{d\Phi}{dt}.$$
Unlike the `~EM-01` field, this **E** has nonzero curl and is **not** the gradient
of a potential; it wraps around the changing **B** exactly as a magnetostatic **B**
wraps a current. This one equation is later promoted, unchanged, to one of
Maxwell's four (`~EM-13`).

## 3. Motional EMF
The flux can also change because the circuit **moves**. Then the driving force is
the magnetic part of the Lorentz force, $q\,\mathbf v\times\mathbf B$, acting on the
charges in the moving conductor (Gr §7.1.3, p.305). For a rod of length $L$ sliding
at speed $v$ with **v**, **B**, and the rod mutually perpendicular,
$$\mathcal{E}=\int(\mathbf v\times\mathbf B)\cdot d\mathbf l = B\,v\,L .$$
Code: `motional_emf(B, v, length)`. Griffiths shows this equals $-d\Phi/dt$ computed
from the area the rod sweeps out — the **flux rule** (p.313): motional and
induced-**E** EMFs, physically distinct mechanisms, obey the *same* $\mathcal{E}=-d\Phi/dt$.

## 4. Inductance
Flux linkage is proportional to the current that makes it (Gr §7.2.3,
Eq. 7.27–7.28, p.321):
$$\Phi = L\,I\qquad(\text{self}),\qquad \Phi_2 = M\,I_1\qquad(\text{mutual}).$$
For a long solenoid ($N$ turns, length $l$, cross-section $A$), $B=\mu_0 N I/l$
inside gives $L=\mu_0 N^2 A/l$; two coaxial solenoids share $M=\mu_0 N_1 N_2 A/l$.
A key result is **reciprocity**, $M_{12}=M_{21}$ — the mutual inductance is the same
whichever coil drives. Code: `solenoid_inductance`, `mutual_inductance_solenoids`.

## 5. Energy in the magnetic field
The work done against the back-EMF while building the current up to $I$ is stored,
and reads two ways (Gr §7.2.4, Eq. 7.34–7.35, p.328):
$$W=\tfrac12 L I^2=\frac{1}{2\mu_0}\int B^2\,d\tau ,\qquad u=\frac{B^2}{2\mu_0}.$$
Either bookkeeping — energy "in the inductor" ($\tfrac12 LI^2$) or "in the field"
at density $u=B^2/2\mu_0$ — gives the same number; for a solenoid the code checks
this to machine precision (`energy_in_inductor` vs `magnetic_field_energy_solenoid`,
with `magnetic_energy_density` returning the field $u(x,y,z)$). It is the exact
magnetic twin of the `~EM-06` charge-vs-field energy duality ($\tfrac12 CV^2$ vs
$\tfrac{\varepsilon_0}{2}\!\int E^2$).

## Where this goes
- `~EM-12` puts this `L` (with `C` and `R`) in a loop driven by an AC source:
  complex impedance and resonance $\omega_0=1/\sqrt{LC}$.
- `~EM-13` adds Maxwell's displacement current to Ampère's law; together with the
  induced-**E** law $\nabla\times\mathbf E=-\partial\mathbf B/\partial t$ from §2, the
  set closes into the four Maxwell equations and predicts light.
