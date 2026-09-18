# CM-13 — Rigid-Body Dynamics

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-09`,
**`~MA-04`** (the eigensolver). **Feeds:** `~CM-14` (Euler's equations).

## Scope
The **moment-of-inertia tensor** I_ij and its diagonalization into **principal
moments** (eigenvalues) and **principal axes** (eigenvectors). This is the
headline MA-04 consumer: I is real symmetric, so `eig_symmetric` *is* the
principal-axis transformation. Also L = Iω and the rotational kinetic energy.

## Operations — `code/rigid_body.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `inertia_tensor(masses, positions)` | I_ij = Σm(r²δ_ij − r_i r_j) | Fowles §9.1 p.361 |
| `principal_axes(I)` | principal moments & axes (via MA-04) | Fowles §9.2 p.371 |
| `moment_about_axis(I, axis)` | n·I·n | Fowles §9.1 p.361 |
| `angular_momentum(I, omega)` | L = Iω | Fowles §9.1 p.361 |
| `rotational_kinetic_energy(I, omega)` | ½ω·Iω | Fowles §9.1 p.361 |
| `parallel_axis(I_cm, M, d)` | parallel-axis shift | Fowles §9.1 p.361 |

## Use
```python
from rigid_body import inertia_tensor, principal_axes, angular_momentum
I = inertia_tensor([1]*4, [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)])   # -> diag(2,2,4)
moments, axes = principal_axes(I)                                 # eigenvalues, eigenvectors
angular_momentum(I, (0,0,3))                                      # (0,0,12), L || omega here
```

## Run
```bash
cd code
python3 rigid_body.py        # demo (inertia tensor, principal moments, L=I omega)
python3 test_rigid_body.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/rigid_body.py` · `code/test_rigid_body.py` · `problems/problems.md`
