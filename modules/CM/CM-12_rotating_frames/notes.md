# CM-12 — Non-inertial (Rotating) Frames (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## Acceleration in a rotating frame
Relating the time derivatives in an inertial frame and a frame rotating at **ω**,
the inertial acceleration of a particle is [F §5.3 p.196; MT §10.3 p.391]
$$\mathbf a_{\rm in}=\mathbf a_{\rm rot}+2\,\boldsymbol\omega\times\mathbf v_{\rm rot}
   +\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r)+\dot{\boldsymbol\omega}\times\mathbf r.$$
Solving for the *apparent* (rotating-frame) acceleration, Newton's law picks up
**fictitious forces**:
$$m\,\mathbf a_{\rm rot}=\mathbf F_{\rm real}
   \underbrace{-\,m\,\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r)}_{\text{centrifugal}}
   \underbrace{-\,2m\,\boldsymbol\omega\times\mathbf v_{\rm rot}}_{\text{Coriolis}}
   \underbrace{-\,m\,\dot{\boldsymbol\omega}\times\mathbf r}_{\text{Euler}}.$$

- **Centrifugal** points outward with magnitude ω²ρ (ρ = distance from the axis);
  it is the rotating-frame mirror of the centripetal acceleration of `~CM-10`.
- **Coriolis** is perpendicular to both **ω** and the velocity — it deflects
  moving bodies (trade winds, the Foucault pendulum) without changing their speed.

Code: `centrifugal_acceleration`, `coriolis_acceleration`, `euler_acceleration`,
all built on MA-01's `cross`; the tests verify the outward direction & ω²ρ
magnitude of the centrifugal term and the double perpendicularity of Coriolis.
