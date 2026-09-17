/* teaching_network.js — the Teaching Network page.
 *
 * An empty void: sparse specks of light glimmering in the darkness; each
 * topic a small black orb outlined by a thin halo of white light. Travel
 * node to node along the edges of projects/modules/topic_network.txt
 * (prerequisite chains, ~cross-links, and the KEY BRIDGES backbone).
 *
 * The DATA block below is baked by dev/build_network.py (the page must work
 * over file://, so nothing is fetched). The drawing/interaction core is
 * DOM-free so dev/render_check/record_teaching.js can verify it headlessly;
 * only boot() at the bottom touches the DOM.
 *
 * Deep links, both ways with the modules browser: teaching.html#<id> glides
 * to that orb on load (and the URL follows your travel), and the panel's
 * "open module" link goes to ../modules/teaching_modules.html#<id>, whose
 * hash routing shows that module; every module there links back here.
 * dev/render_check/links_harness.js drives this without a browser.
 */
(function (global) {
  'use strict';

  /* === AUTO-GENERATED NETWORK DATA (dev/build_network.py) -- DO NOT EDIT === */
  var DATA = {"nodes":[["MA","22 \u00b7 CM 25 \u00b7 EM 18 \u00b7 QM 22 \u00b7 RE 17 \u00b7 SM 6 \u00b7 PK 4 \u00b7 QO 6 \u00b7 QF 5 \u00b7 ST 18","MA",1,0,99.7,-576.3,1],["MA-01","Vectors & vector algebra -- dot/cross/triple products","MA",0,0,97.6,-621.2,1],["MA-02","Vector calculus -- grad, div, curl, Laplacian; Gauss & Stokes theorems","MA",0,0,143.0,-612.3,1],["MA-03","Coordinate systems -- Cartesian/cylindrical/spherical, curvilinear, Jacobians","MA",0,0,158.4,-566.0,1],["MA-04","Linear algebra -- vector spaces, matrices, eigenvalues/vectors, diagonalization","MA",0,0,137.1,-521.7,1],["MA-05","Complex numbers & functions -- Euler form, branch cuts","MA",0,0,91.7,-501.8,1],["MA-06","Complex analysis -- analyticity, contour integration, residues","MA",0,0,50.2,-529.4,1],["MA-07","Ordinary differential equations -- linear systems, series solutions","MA",0,0,31.2,-577.5,1],["MA-08","Partial differential equations -- wave/heat/Laplace, separation of variables","MA",0,0,38.4,-630.4,1],["MA-09","Fourier series & transforms -- spectral methods, momentum space","MA",0,0,71.1,-674.1,1],["MA-10","Laplace & integral transforms","MA",0,0,123.8,-687.7,1],["MA-11","Sturm-Liouville theory -- orthogonal functions, completeness, eigenfunction expansions","MA",0,0,175.8,-669.0,1],["MA-12","Special functions -- Legendre, spherical harmonics, Bessel, Hermite, Laguerre","MA",0,0,212.9,-627.2,1],["MA-13","Calculus of variations -- Euler-Lagrange, functionals, constraints","MA",0,0,225.8,-573.2,1],["MA-14","Green's functions -- propagators, source & boundary-value problems","MA",0,0,217.7,-518.5,1],["MA-15","Dirac delta & distributions","MA",0,0,191.2,-471.8,1],["MA-16","Tensor analysis & index notation -- covariant/contravariant, the metric","MA",0,0,154.3,-437.1,1],["MA-17","Differential geometry -- manifolds, forms, connections, curvature","MA",0,1,14.7,-447.3,1],["MA-18","Group theory & symmetry -- discrete & Lie groups, representations","MA",0,0,-16.6,-485.7,1],["MA-19","Probability & statistics -- distributions, moments, error analysis","MA",0,0,-41.5,-530.5,1],["MA-20","Numerical methods -- quadrature, ODE/PDE integrators, linear algebra","MA",0,0,-52.5,-581.4,1],["MA-21","Dimensional analysis & asymptotics -- scaling, perturbation series","MA",0,0,-47.4,-632.5,1],["MA-22","Topology & dynamical systems -- Hatcher; Chicone; category theory","MA",0,1,-31.9,-679.7,1],["CM","Classical Mechanics","CM",1,0,-293.0,-471.1,1],["CM-01","Kinematics -- position/velocity/acceleration, projectile, 1D/2D/3D","CM",0,0,-297.9,-513.4,1],["CM-02","Equation of motion / Newton's laws -- F=ma, free-body analysis","CM",0,0,-251.6,-510.5,1],["CM-03","Reference frames -- inertial; lab frame vs centre-of-mass frame; Galilean","CM",0,0,-223.9,-472.3,1],["CM-04","Work & energy -- kinetic energy, work-energy theorem","CM",0,0,-220.7,-424.0,1],["CM-05","Conservative forces & potential energy -- energy conservation, stability","CM",0,0,-256.7,-392.7,1],["CM-06","Linear momentum & conservation -- impulse, systems of particles","CM",0,0,-305.9,-401.5,1],["CM-07","Centre of mass -- CM motion, reduced mass","CM",0,0,-347.3,-432.0,1],["CM-08","Collisions & scattering -- elastic/inelastic, lab vs CM frame, cross-sections, Rutherford","CM",0,0,-363.5,-481.4,1],["CM-09","Angular momentum & torque -- conservation for particles & systems","CM",0,0,-348.9,-532.9,1],["CM-10","Centripetal & circular motion -- radial/tangential acceleration","CM",0,0,-306.8,-568.7,1],["CM-11","Central-force motion -- effective potential, orbits, Kepler's laws, two-body problem","CM",0,0,-253.6,-580.5,1],["CM-12","Non-inertial frames -- rotating frames, centrifugal & Coriolis forces","CM",0,0,-203.0,-561.2,1],["CM-13","Rigid-body dynamics -- moment-of-inertia tensor, principal axes & moments","CM",0,0,-166.4,-521.0,1],["CM-14","Euler's equations -- tops, gyroscopes, free precession","CM",0,0,-147.6,-470.7,1],["CM-15","Oscillations -- SHM, damped, driven/forced, resonance, Q-factor","CM",0,0,-148.9,-419.8,1],["CM-16","Coupled oscillations & normal modes -- eigenvalue problem, normal coordinates","CM",0,0,-273.0,-317.2,1],["CM-17","Lagrangian mechanics -- generalized coordinates, constraints, Euler-Lagrange","CM",0,0,-322.5,-324.2,1],["CM-18","Symmetries & Noether's theorem -- cyclic coordinates -> conservation laws","CM",0,0,-370.9,-343.4,1],["CM-19","Hamiltonian mechanics -- Legendre transform, phase space, Hamilton's equations","CM",0,0,-409.9,-379.7,1],["CM-20","Poisson brackets & canonical transformations -- generating functions, Liouville","CM",0,0,-436.5,-426.7,1],["CM-21","Hamilton-Jacobi theory & action-angle variables","CM",0,0,-446.6,-479.7,1],["CM-22","Continuum mechanics & the CONTINUITY EQUATION -- mass conservation, stress/strain","CM",0,0,-439.3,-533.1,1],["CM-23","Fluid dynamics -- Euler & Navier-Stokes, Bernoulli, vorticity","CM",0,0,-414.5,-580.5,1],["CM-24","Nonlinear dynamics & chaos -- phase portraits, bifurcations, attractors","CM",0,0,-379.0,-619.5,1],["CM-25","Waves in continuous media -- strings, sound, dispersion","CM",0,0,-337.0,-648.2,1],["EM","Electricity & Magnetism","EM",1,0,-685.8,209.2,1],["EM-01","Electrostatics -- Coulomb's law, electric field, superposition","EM",0,0,-729.8,210.9,1],["EM-02","Gauss's law -- flux, symmetry, fields of charge distributions","EM",0,0,-716.2,163.8,1],["EM-03","Electric potential -- voltage, Poisson & Laplace equations","EM",0,0,-672.7,140.0,1],["EM-04","Boundary-value problems -- separation of variables, method of images, uniqueness","EM",0,0,-634.4,169.9,1],["EM-05","Multipole expansion -- monopole/dipole/quadrupole","EM",0,0,-628.9,220.5,1],["EM-06","Conductors & capacitance -- electrostatic energy","EM",0,0,-649.4,267.8,1],["EM-07","Dielectrics & polarization -- bound charge, D field, susceptibility","EM",0,0,-691.6,296.8,1],["EM-08","Magnetostatics -- Biot-Savart & Ampere's laws, Lorentz force","EM",0,0,-743.3,289.7,1],["EM-09","Magnetic vector potential -- gauge freedom","EM",0,0,-783.5,254.3,1],["EM-10","Magnetic materials & magnetization -- H field, ferromagnetism","EM",0,0,-798.5,201.8,1],["EM-11","Electromagnetic induction -- Faraday's & Lenz's laws, inductance","EM",0,0,-786.2,148.7,1],["EM-12","AC circuits & driven RLC -- impedance, resonance","EM",0,0,-754.9,105.2,1],["EM-13","Maxwell's equations -- displacement current, integral & differential forms","EM",0,0,-713.1,76.0,1],["EM-14","EM conservation laws -- Poynting vector, field energy & momentum, stress tensor","EM",0,0,-569.7,121.0,1],["EM-15","Electromagnetic waves -- vacuum & media, polarization, reflection/refraction, dispersion","EM",0,0,-551.6,167.1,1],["EM-16","Waveguides, cavities & transmission lines","EM",0,0,-547.5,217.7,1],["EM-17","Radiation -- retarded potentials, Lienard-Wiechert, dipole & Larmor radiation","EM",0,0,-555.7,268.0,1],["EM-18","Relativistic electrodynamics -- field tensor F^{mu nu}, covariant Maxwell","EM",0,0,-578.0,312.2,1],["QM","Quantum Mechanics","QM",1,0,99.7,994.6,1],["QM-01","Origins -- blackbody, photoelectric effect, Bohr model, de Broglie waves","QM",0,0,72.3,1034.7,1],["QM-02","Wavefunction & Born rule -- probability density, normalization","QM",0,0,26.2,1026.3,1],["QM-03","Schrodinger equation -- time-dependent & time-independent","QM",0,0,35.9,978.1,1],["QM-04","Probability current & continuity -- conservation of probability","QM",0,0,72.1,943.3,1],["QM-05","Formalism -- Hilbert space, Dirac bra-ket, operators, observables, commutators","QM",0,0,122.6,941.6,1],["QM-06","Measurement postulates -- eigenvalues, collapse, expectation values","QM",0,0,157.0,977.8,1],["QM-07","Uncertainty principle -- non-commuting observables, Ehrenfest's theorem","QM",0,0,160.4,1028.2,1],["QM-08","One-dimensional problems -- wells, step & barrier, tunnelling","QM",0,0,133.1,1071.8,1],["QM-09","Harmonic oscillator -- analytic (Hermite) & algebraic (ladder operators)","QM",0,0,92.1,1102.1,1],["QM-10","Angular momentum -- operators, ladder, spherical harmonics","QM",0,0,45.5,1115.7,1],["QM-11","Spin & two-level systems -- Pauli matrices, Stern-Gerlach","QM",0,0,-38.2,976.8,1],["QM-12","Central potentials & the hydrogen atom -- radial equation, degeneracy","QM",0,0,-18.6,930.4,1],["QM-13","Addition of angular momenta -- Clebsch-Gordan coefficients","QM",0,0,18.4,892.7,1],["QM-14","Identical particles -- symmetrization, bosons/fermions, Pauli exclusion","QM",0,0,66.9,868.8,1],["QM-15","Approximations I -- time-independent perturbation, variational method, WKB","QM",0,0,121.4,864.2,1],["QM-16","Approximations II -- time-dependent perturbation, Fermi's golden rule","QM",0,0,172.2,884.0,1],["QM-17","Fine structure, Zeeman & hyperfine -- spin-orbit, relativistic corrections","QM",0,0,213.6,919.6,1],["QM-18","Scattering theory -- partial waves, Born approximation, phase shifts","QM",0,0,237.4,968.0,1],["QM-19","Propagators & path integrals -- Green's functions, Feynman integral","QM",0,0,242.0,1021.4,1],["QM-20","Density matrix & open systems -- mixed states, decoherence","QM",0,0,228.4,1073.1,1],["QM-21","Entanglement & foundations -- EPR, Bell inequalities","QM",0,0,201.1,1117.5,1],["QM-22","Relativistic QM -- Klein-Gordon & Dirac equations","QM",0,0,162.8,1150.0,1],["RE","Relativity","RE",1,0,-580.5,-183.6,1],["RE-01","Galilean relativity & its failure -- Michelson-Morley, the ether","RE",0,0,-624.4,-192.0,1],["RE-02","Postulates of special relativity -- constancy of c","RE",0,0,-596.0,-230.4,1],["RE-03","Lorentz transformations -- boosts, relativistic velocity addition","RE",0,0,-547.0,-219.4,1],["RE-04","Time dilation, length contraction & simultaneity","RE",0,0,-529.4,-171.8,1],["RE-05","Minkowski spacetime -- 4-vectors, invariant interval, light cones","RE",0,0,-544.6,-123.8,1],["RE-06","Relativistic dynamics -- 4-momentum, E=mc^2, relativistic collisions","RE",0,0,-586.1,-96.3,1],["RE-07","Relativistic Doppler effect & aberration","RE",0,0,-636.2,-106.2,1],["RE-08","Covariant formulation -- tensors in SR, index gymnastics","RE",0,0,-673.0,-144.7,1],["RE-09","Tensor calculus on manifolds -- metric, covariant derivative, Christoffel symbols","RE",0,0,-683.1,-199.1,1],["RE-10","Equivalence principle -- gravitation as geometry","RE",0,0,-664.1,-252.0,1],["RE-11","Curvature -- Riemann & Ricci tensors, geodesic deviation","RE",0,0,-620.2,-287.8,1],["RE-12","Geodesics & the variational principle -- particle & light paths","RE",0,0,-565.1,-298.0,1],["RE-13","Einstein field equations -- stress-energy tensor, Newtonian limit","RE",0,0,-512.8,-278.4,1],["RE-14","Schwarzschild solution & black holes -- orbits, horizons, classic tests","RE",0,0,-474.8,-237.6,1],["RE-15","Cosmology -- FLRW metric, Friedmann equations, expansion","RE",0,0,-458.0,-185.5,1],["RE-16","Gravitational waves -- linearized gravity, detection","RE",0,0,-458.7,-132.6,1],["RE-17","Exact solutions & numerical relativity -- Stephani; Baumgarte-Shapiro","RE",0,1,-475.6,-84.8,1],["SM","Statistical Mechanics & Thermodynamics","SM",1,0,779.9,-183.6,1],["SM-01","Probability foundations & ensembles","SM",0,0,825.5,-201.3,1],["SM-02","Laws of thermodynamics -- entropy, thermodynamic potentials","SM",0,0,832.6,-151.8,1],["SM-03","Classical stat mech -- micro/canonical/grand ensembles, partition functions","SM",0,0,793.6,-118.4,1],["SM-04","Quantum statistics -- Bose-Einstein & Fermi-Dirac gases","SM",0,0,742.3,-123.9,1],["SM-05","Phase transitions & critical phenomena -- Ising, mean field, RG","SM",0,0,709.9,-163.2,1],["SM-06","Non-equilibrium & kinetic theory -- Boltzmann equation, transport","SM",0,0,701.8,-211.9,1],["QO","Quantum & Nonlinear Optics","QO",1,0,779.9,601.9,1],["QO-01","Classical & quantized light -- modes, coherent states","QO",0,0,817.4,633.4,1],["QO-02","Atom-field interaction -- Rabi oscillations, Jaynes-Cummings model","QO",0,0,778.4,664.2,1],["QO-03","Emission & coherence -- spontaneous/stimulated emission, laser physics","QO",0,0,730.1,644.5,1],["QO-04","Open quantum systems -- master equations, decoherence","QO",0,0,712.7,595.5,1],["QO-05","Squeezing & nonclassical light -- entangled photons","QO",0,0,731.0,547.7,1],["QO-06","Nonlinear optics -- chi^(2)/chi^(3), parametric, Brillouin (SBS) & Raman scattering","QO",0,0,772.6,520.4,1],["PK","Plasma & Kinetic Theory","PK",1,0,885.1,209.2,1],["PK-01","Kinetic description -- distribution functions, Vlasov & Boltzmann","PK",0,0,931.7,199.3,1],["PK-02","Fluid / MHD description -- moments, continuity & momentum equations","PK",0,0,929.7,248.9,1],["PK-03","Plasma waves & instabilities -- Langmuir, ion-acoustic, Landau damping","PK",0,0,887.2,276.4,1],["PK-04","Atomic & molecular kinetics -- rate equations, excimer chemistry, EEDF/swarm","PK",0,0,838.6,267.9,1],["QF","Quantum Field Theory","QF",1,0,492.4,889.4,1],["QF-01","Canonical field quantization -- scalar/Dirac/EM fields, 2nd quantization","QF",0,0,495.6,937.7,1],["QF-02","Interactions & Feynman diagrams -- perturbation theory, S-matrix","QF",0,0,446.3,928.7,1],["QF-03","Gauge theories -- QED, gauge invariance","QF",0,0,428.8,880.8,1],["QF-04","Renormalization & the renormalization group","QF",0,0,450.6,834.5,1],["QF-05","QFT in curved spacetime -- Hawking & Unruh effects","QF",0,0,495.1,812.9,1],["ST","Probability Theory","ST",1,0,492.4,-471.1,1],["ST-01","Sample spaces & the axioms of probability -- set algebra, inclusion-exclusion","ST",0,0,530.3,-495.9,1],["ST-02","Counting techniques -- permutations, combinations, multinomial","ST",0,0,541.7,-449.9,1],["ST-03","Conditional probability & independence -- multiplication rule","ST",0,0,502.0,-420.2,1],["ST-04","Bayes' theorem -- total probability, posterior updating","ST",0,0,454.6,-436.4,1],["ST-05","Discrete random variables & expectation -- pmf/cdf, E[X], variance, moments","ST",0,0,436.7,-484.5,1],["ST-06","Moment-generating functions -- M(t)=E[e^{tX}], uniqueness","ST",0,0,447.3,-534.7,1],["ST-07","The binomial distribution -- Bernoulli trials, n p, n p (1-p)","ST",0,0,489.5,-563.9,1],["ST-08","Geometric & negative binomial distributions -- discrete waiting times","ST",0,0,542.8,-560.2,1],["ST-09","The Poisson distribution -- law of rare events, Poisson process","ST",0,0,586.4,-526.5,1],["ST-10","Continuous random variables -- pdf/cdf, percentiles, uniform","ST",0,0,604.5,-473.3,1],["ST-11","Exponential, gamma & chi-square distributions -- the gamma function","ST",0,0,592.0,-417.5,1],["ST-12","The normal distribution -- Gaussian, standardization, Gaussian integral","ST",0,0,553.4,-374.8,1],["ST-13","Joint distributions of two random variables -- marginals, independence","ST",0,0,500.2,-354.4,1],["ST-14","Correlation & conditional distributions -- covariance, regression to the mean","ST",0,0,444.5,-360.7,1],["ST-15","The bivariate normal distribution -- joint Gaussian, conditionals are Gaussian","ST",0,0,398.6,-391.1,1],["ST-16","Transformations of random variables -- cdf & Jacobian methods, convolution","ST",0,0,365.3,-433.4,1],["ST-17","The MGF technique & normal sampling distributions -- chi-square, t, F","ST",0,0,355.3,-485.4,1],["ST-18","The central limit theorem & approximations -- normal approx, continuity correction","ST",0,0,363.3,-535.2,1],["CMx","Condensed Matter","CMx",1,0,-580.5,601.9,0],["QC","Quantum Chemistry","QC",1,0,-293.0,889.4,0]],"edges":[[23,24,1],[24,25,0],[24,2,2],[25,26,0],[26,27,0],[26,92,2],[27,28,0],[28,29,0],[29,30,0],[29,97,2],[30,31,0],[30,34,2],[31,32,0],[31,86,2],[32,33,0],[32,36,3],[32,78,2],[33,34,0],[34,35,0],[34,80,3],[34,105,2],[35,36,0],[36,37,0],[36,67,3],[36,4,2],[36,17,3],[36,78,3],[37,38,0],[38,39,3],[38,61,2],[38,7,2],[38,77,2],[39,40,0],[39,64,3],[39,4,2],[39,9,3],[39,77,3],[40,41,0],[40,44,3],[40,13,3],[40,87,2],[41,42,0],[41,18,3],[41,131,3],[42,43,0],[43,44,0],[43,73,3],[44,45,0],[44,83,2],[44,87,3],[44,103,2],[45,46,0],[45,62,3],[45,63,2],[45,125,2],[45,72,2],[46,47,0],[46,124,3],[46,125,3],[46,126,2],[46,115,2],[47,48,0],[47,22,2],[48,64,2],[48,8,2],[153,56,2],[49,50,1],[50,51,0],[51,52,0],[51,2,2],[52,53,0],[52,8,2],[53,54,0],[53,8,2],[54,55,0],[54,12,2],[55,56,0],[56,57,0],[57,58,0],[58,59,0],[58,131,2],[59,60,0],[60,61,0],[61,62,0],[62,63,3],[63,64,0],[63,72,3],[63,104,2],[64,65,0],[64,9,2],[64,76,3],[64,117,2],[65,66,0],[66,67,0],[66,6,2],[66,14,2],[67,16,2],[67,99,2],[67,100,3],[0,1,1],[1,2,0],[2,3,0],[3,4,0],[3,150,2],[4,5,0],[4,73,2],[4,148,2],[4,149,2],[5,6,0],[6,7,0],[6,87,2],[7,8,0],[8,9,0],[8,71,2],[9,10,0],[9,76,2],[9,150,2],[10,11,0],[10,140,2],[11,12,0],[12,13,0],[12,77,2],[12,78,2],[12,80,2],[12,145,2],[13,14,0],[13,103,2],[14,15,0],[14,87,2],[15,16,0],[15,144,2],[16,17,3],[16,96,2],[16,99,2],[17,18,0],[17,100,2],[17,102,2],[18,19,0],[18,131,2],[19,20,0],[19,110,2],[19,112,3],[19,135,2],[20,21,0],[20,124,2],[21,22,0],[21,83,2],[123,124,1],[124,125,0],[124,115,3],[124,152,2],[125,126,0],[125,72,3],[125,115,3],[126,127,0],[127,119,2],[127,143,2],[128,129,1],[129,130,0],[129,77,3],[129,87,2],[129,90,2],[130,131,0],[131,132,0],[132,133,0],[132,114,2],[133,104,2],[68,69,1],[69,70,0],[70,71,0],[70,135,2],[71,72,0],[72,73,0],[73,74,0],[74,75,0],[74,139,2],[75,76,0],[75,146,2],[76,77,0],[77,78,0],[78,79,3],[79,80,0],[79,81,3],[80,81,0],[80,105,3],[81,82,0],[82,83,0],[82,113,2],[83,84,0],[84,85,0],[84,119,2],[85,86,0],[86,87,0],[87,88,0],[87,103,3],[88,89,0],[88,120,2],[89,90,0],[89,121,2],[90,97,2],[116,117,1],[117,118,0],[117,143,2],[118,119,0],[119,120,0],[120,121,0],[121,122,0],[91,92,1],[92,93,0],[93,94,0],[94,95,0],[95,96,0],[96,97,0],[97,98,0],[98,99,0],[99,100,0],[100,101,0],[100,104,3],[101,102,0],[102,103,0],[103,104,0],[104,105,0],[105,106,0],[106,107,0],[107,108,0],[109,110,1],[110,111,0],[110,112,3],[110,136,2],[110,139,2],[110,146,2],[110,152,3],[111,112,0],[112,113,0],[112,115,3],[112,140,2],[113,114,0],[114,115,0],[115,145,2],[134,135,1],[135,136,0],[136,137,0],[136,141,2],[137,138,0],[138,139,0],[139,140,0],[139,146,3],[140,141,0],[140,151,2],[141,142,0],[142,143,0],[143,144,0],[144,145,0],[145,146,0],[146,147,0],[146,152,3],[147,148,0],[148,149,0],[149,150,0],[150,151,0],[151,152,0]],"trunks":{"MA":"22 \u00b7 CM 25 \u00b7 EM 18 \u00b7 QM 22 \u00b7 RE 17 \u00b7 SM 6 \u00b7 PK 4 \u00b7 QO 6 \u00b7 QF 5 \u00b7 ST 18","CM":"Classical Mechanics","EM":"Electricity & Magnetism","QM":"Quantum Mechanics","RE":"Relativity","SM":"Statistical Mechanics & Thermodynamics","QO":"Quantum & Nonlinear Optics","PK":"Plasma & Kinetic Theory","QF":"Quantum Field Theory","ST":"Probability Theory","CMx":"Condensed Matter","QC":"Quantum Chemistry"}};
  /* === END AUTO-GENERATED === */

  var EK_CHAIN = 0, EK_HUB = 1, EK_CROSS = 2, EK_BRIDGE = 3;

  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function clamp01(v) { return clamp(v, 0, 1); }
  function easeInOut(p) {
    return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
  }

  /* ---------- state ---------- */

  function createState(w, h, seed) {
    var st = { w: w, h: h };
    st.nodes = DATA.nodes.map(function (n) {
      return { id: n[0], label: n[1], trunk: n[2], hub: n[3] === 1,
               adv: n[4] === 1, mod: n[7] === 1,
               x: n[5], y: n[6], r: n[3] === 1 ? 13 : 6.5 };
    });
    st.edges = DATA.edges;
    st.trunks = DATA.trunks;
    st.byId = {};
    st.adj = [];
    var i;
    for (i = 0; i < st.nodes.length; i++) {
      st.byId[st.nodes[i].id] = i;
      st.adj.push([]);
    }
    for (i = 0; i < st.edges.length; i++) {
      var e = st.edges[i];
      st.adj[e[0]].push({ j: e[1], k: e[2] });
      st.adj[e[1]].push({ j: e[0], k: e[2] });
    }

    var rng = mulberry32(((seed || 1) ^ 0x51ED2701) >>> 0);
    st.specks = [];
    for (i = 0; i < 170; i++) {
      var ang = rng() * 6.2832, rad = 1900 * Math.sqrt(rng());
      st.specks.push({
        x: Math.cos(ang) * rad, y: Math.sin(ang) * rad,
        f: [0.25, 0.5, 0.8][i % 3],           // parallax depth layer
        s: 0.7 + 1.7 * Math.pow(rng(), 2),    // star params match the homepage
        base: 0.28 + 0.6 * rng(),
        sp: 0.25 + 0.5 * rng(),
        ph: 6.2832 * rng(),
        fl: rng() < 0.06
      });
    }

    st.cam = { x: 0, y: 0, z: 0.3 };
    st.glide = null;
    st.current = -1;
    st.hover = -1;
    fitView(st);
    return st;
  }

  function bounds(st) {
    var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (var i = 0; i < st.nodes.length; i++) {
      var n = st.nodes[i];
      if (n.x < x0) x0 = n.x;
      if (n.x > x1) x1 = n.x;
      if (n.y < y0) y0 = n.y;
      if (n.y > y1) y1 = n.y;
    }
    return [x0, y0, x1, y1];
  }

  function fitParams(st) {
    var b = bounds(st), pad = 170;
    var z = Math.min(st.w / (b[2] - b[0] + 2 * pad), st.h / (b[3] - b[1] + 2 * pad));
    return { x: (b[0] + b[2]) / 2, y: (b[1] + b[3]) / 2, z: clamp(z, 0.12, 0.6) };
  }

  function fitView(st) {
    var p = fitParams(st);
    st.cam.x = p.x; st.cam.y = p.y; st.cam.z = p.z;
    st.glide = null;
  }

  function glideTo(st, x, y, z, t, dur) {
    var c = cameraAt(st, t);
    st.glide = { x0: c.x, y0: c.y, z0: c.z, x1: x, y1: y, z1: z, t0: t, dur: dur };
  }

  function travelTo(st, i, t, instant) {
    st.current = i;
    var n = st.nodes[i];
    var z1 = n.hub ? 0.85 : Math.max(1.7, Math.min(cameraAt(st, t).z, 2.6));
    if (instant) {
      st.cam.x = n.x; st.cam.y = n.y; st.cam.z = z1;
      st.glide = null;
    } else {
      glideTo(st, n.x, n.y, z1, t, 1.15);
    }
  }

  function cameraAt(st, t) {
    var g = st.glide;
    if (!g) return st.cam;
    var p = clamp01((t - g.t0) / g.dur);
    var e = easeInOut(p);
    var c = { x: g.x0 + (g.x1 - g.x0) * e,
              y: g.y0 + (g.y1 - g.y0) * e,
              z: g.z0 + (g.z1 - g.z0) * e };
    if (p >= 1) {
      st.cam = c;
      st.glide = null;
    }
    return c;
  }

  function screenToWorld(st, cam, sx, sy) {
    return [cam.x + (sx - st.w / 2) / cam.z, cam.y + (sy - st.h / 2) / cam.z];
  }

  function pick(st, t, sx, sy) {
    var cam = cameraAt(st, t);
    var best = -1, bd = 1e9;
    for (var i = 0; i < st.nodes.length; i++) {
      var n = st.nodes[i];
      var nx = st.w / 2 + (n.x - cam.x) * cam.z;
      var ny = st.h / 2 + (n.y - cam.y) * cam.z;
      var lim = Math.max(11, n.r * cam.z + 7);
      var dx = nx - sx, dy = ny - sy;
      var d = Math.sqrt(dx * dx + dy * dy);
      if (d < lim && d < bd) { bd = d; best = i; }
    }
    return best;
  }

  /* ---------- deep links (DOM-free) ---------- */

  var MODULES_PAGE = '../modules/teaching_modules.html';

  // teaching.html#<id> -> node index, or -1 (empty, unknown, or garbage)
  function nodeFromHash(st, hash) {
    var id = String(hash || '').replace(/^#/, '');
    try { id = decodeURIComponent(id); } catch (e) { /* keep it raw */ }
    id = id.replace(/^\s+|\s+$/g, '');
    if (!id || !Object.prototype.hasOwnProperty.call(st.byId, id)) return -1;
    return st.byId[id];
  }

  // the node's page in the modules browser, '' when none exists yet
  function moduleHref(n) {
    return n && n.mod ? MODULES_PAGE + '#' + encodeURIComponent(n.id) : '';
  }

  /* ---------- drawing ---------- */

  function drawFrame(ctx, st, t) {
    var w = st.w, h = st.h;
    var cam = cameraAt(st, t);
    var i, n, a;

    var bg = ctx.createLinearGradient(0, 0, 0, h);
    bg.addColorStop(0, '#070b18');            // the other pages' dark blue
    bg.addColorStop(0.7, '#04060c');
    bg.addColorStop(1, '#04060c');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);

    // stars glimmering in the void, same twinkle as the homepage
    for (i = 0; i < st.specks.length; i++) {
      var S = st.specks[i];
      var px = w / 2 + (S.x - cam.x) * cam.z * S.f;
      var py = h / 2 + (S.y - cam.y) * cam.z * S.f;
      if (px < -6 || px > w + 6 || py < -6 || py > h + 6) continue;
      a = S.base * (0.55 + 0.45 * Math.sin(S.sp * t + S.ph));
      if (a < 0.04) continue;
      ctx.fillStyle = 'rgba(159,216,255,' + a.toFixed(3) + ')';
      ctx.fillRect(px - S.s / 2, py - S.s / 2, S.s, S.s);
      if (S.fl) {                             // faint cross flare, a few stars
        ctx.fillStyle = 'rgba(159,216,255,' + (a * 0.3).toFixed(3) + ')';
        ctx.fillRect(px - 3 * S.s, py - 0.5, 6 * S.s, 1);
        ctx.fillRect(px - 0.5, py - 3 * S.s, 1, 6 * S.s);
      }
    }

    // node screen positions
    var P = new Array(st.nodes.length);
    for (i = 0; i < st.nodes.length; i++) {
      n = st.nodes[i];
      P[i] = [w / 2 + (n.x - cam.x) * cam.z, h / 2 + (n.y - cam.y) * cam.z];
    }
    function onscreen(p, m) {
      return p[0] > -m && p[0] < w + m && p[1] > -m && p[1] < h + m;
    }

    // edges, faint threads; bridges slightly brighter
    var zr = clamp01((cam.z - 0.2) / 0.8);
    var EDGE_A = [0.02 + 0.05 * zr, 0.03 + 0.05 * zr,
                  0.02 + 0.035 * zr, 0.05 + 0.06 * zr];
    for (var k = 0; k < 4; k++) {
      if (k === EK_CHAIN && cam.z < 0.45) continue;
      ctx.strokeStyle = 'rgba(198,212,240,' + EDGE_A[k].toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (i = 0; i < st.edges.length; i++) {
        var e = st.edges[i];
        if (e[2] !== k) continue;
        var pa = P[e[0]], pb = P[e[1]];
        if (!onscreen(pa, 90) && !onscreen(pb, 90)) continue;
        ctx.moveTo(pa[0], pa[1]);
        ctx.lineTo(pb[0], pb[1]);
      }
      ctx.stroke();
    }

    // the current node's own links, lifted out of the murk
    if (st.current >= 0) {
      var ad = st.adj[st.current];
      for (var q = 0; q < 2; q++) {          // pass 0: normal, 1: bridges
        ctx.strokeStyle = q ? 'rgba(214,226,248,0.30)' : 'rgba(214,226,248,0.16)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (i = 0; i < ad.length; i++) {
          if ((ad[i].k === EK_BRIDGE) !== !!q) continue;
          ctx.moveTo(P[st.current][0], P[st.current][1]);
          ctx.lineTo(P[ad[i].j][0], P[ad[i].j][1]);
        }
        ctx.stroke();
      }
    }

    // nodes: black orbs, thin white halos
    for (i = 0; i < st.nodes.length; i++) {
      n = st.nodes[i];
      var p = P[i];
      if (!onscreen(p, 60)) continue;
      var sr = n.r * cam.z;
      var lit = i === st.current || i === st.hover;

      if (sr < 2.2) {                        // too far: the topic is a speck
        ctx.fillStyle = 'rgba(220,231,252,' + (lit ? 0.9 : 0.42) + ')';
        ctx.fillRect(p[0] - 0.8, p[1] - 0.8, 1.6, 1.6);
        continue;
      }

      var glowA = 0.09 + (n.hub ? 0.03 : 0) + (lit ? 0.12 : 0);
      var g = ctx.createRadialGradient(p[0], p[1], sr * 0.8, p[0], p[1], sr * 2.6);
      g.addColorStop(0, 'rgba(208,224,255,' + glowA.toFixed(3) + ')');
      g.addColorStop(1, 'rgba(208,224,255,0)');
      ctx.fillStyle = g;
      ctx.fillRect(p[0] - sr * 2.6, p[1] - sr * 2.6, sr * 5.2, sr * 5.2);

      ctx.fillStyle = '#000000';             // the black orb
      ctx.beginPath();
      ctx.arc(p[0], p[1], sr, 0, 6.2832);
      ctx.fill();

      var ringA = n.hub ? 0.62 : 0.5;        // the thin halo of white light
      if (i === st.hover) ringA = 0.88;
      if (i === st.current) ringA = 0.82 + 0.14 * Math.sin(2.4 * t);
      ctx.strokeStyle = 'rgba(235,242,255,' + ringA.toFixed(3) + ')';
      ctx.lineWidth = i === st.current ? 1.6 : 1.25;
      ctx.beginPath();
      ctx.arc(p[0], p[1], sr, 0, 6.2832);
      ctx.stroke();

      if (i === st.current) {                // "you are here": faint outer ring
        ctx.strokeStyle = 'rgba(235,242,255,' +
          (0.2 + 0.08 * Math.sin(2.4 * t)).toFixed(3) + ')';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(p[0], p[1], sr * 1.65 + 2, 0, 6.2832);
        ctx.stroke();
      }
    }

    // labels
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    for (i = 0; i < st.nodes.length; i++) {
      n = st.nodes[i];
      var pp = P[i];
      if (!onscreen(pp, 40)) continue;
      var srr = n.r * cam.z;
      var isLit = i === st.current || i === st.hover;
      if (n.hub) {
        if (srr < 2.0) continue;
        a = isLit ? 0.9 : 0.42;
        ctx.font = '600 12px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif';
        ctx.fillStyle = 'rgba(222,233,252,' + a.toFixed(3) + ')';
        ctx.fillText(cam.z < 0.55 ? n.id : n.label, pp[0], pp[1] + srr + 7);
      } else {
        if (!isLit && (cam.z < 0.85 || srr < 2.6)) continue;
        a = isLit ? 0.9 : 0.3;
        ctx.font = '500 10.5px -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif';
        ctx.fillStyle = 'rgba(214,228,248,' + a.toFixed(3) + ')';
        ctx.fillText(n.id, pp[0], pp[1] + srr + 6);
      }
    }
  }

  global.TeachingNetwork = {
    createState: createState,
    drawFrame: drawFrame,
    fitView: fitView,
    fitParams: fitParams,
    cameraAt: cameraAt,
    travelTo: travelTo,
    glideTo: glideTo,
    pick: pick,
    screenToWorld: screenToWorld,
    nodeFromHash: nodeFromHash,
    moduleHref: moduleHref
  };

  /* ---------- browser boot (skipped under deno / render_check) ---------- */

  if (!global.document || !global.requestAnimationFrame) return;

  function boot() {
    var cv = global.document.getElementById('net');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d');
    var doc = global.document;
    var elTitle = doc.getElementById('net-title');
    var elSub = doc.getElementById('net-sub');
    var elLinks = doc.getElementById('net-links');
    var elMod = doc.getElementById('net-module');

    var reduced = false;
    try {
      reduced = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
    } catch (e) { /* keep animating */ }

    var st = null, dpr = 1, raf = 0, last = null, acc = 0;
    function tNow() { return acc / 1000; }

    function resize() {
      dpr = Math.min(global.devicePixelRatio || 1, 2);
      var w = global.innerWidth, h = global.innerHeight;
      cv.width = Math.round(w * dpr);
      cv.height = Math.round(h * dpr);
      cv.style.width = w + 'px';
      cv.style.height = h + 'px';
      if (!st) {
        st = createState(w, h, 20260812);
      } else {
        st.w = w; st.h = h;
      }
      if (reduced) renderOnce();
    }

    function renderOnce() {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      drawFrame(ctx, st, tNow());
    }

    function frame(ms) {
      if (last !== null) acc += Math.min(ms - last, 100);
      last = ms;
      renderOnce();
      raf = global.requestAnimationFrame(frame);
    }

    function updatePanel() {
      if (!elTitle) return;
      elLinks.textContent = '';
      if (elMod) {                             // the way out: this orb's page
        var cur = st.current >= 0 ? st.nodes[st.current] : null;
        var href = moduleHref(cur);
        if (href) {
          elMod.href = href;
          elMod.textContent = cur.hub ? 'browse the ' + cur.id + ' modules'
                                      : 'open module ' + cur.id;
          elMod.hidden = false;
        } else {
          elMod.removeAttribute('href');
          elMod.hidden = true;
        }
      }
      var mk = function (label, title, cls, onclick) {
        var b = doc.createElement('button');
        b.type = 'button';
        b.textContent = label;
        if (title) b.title = title;
        if (cls) b.className = cls;
        b.addEventListener('click', onclick);
        elLinks.appendChild(b);
      };
      if (st.current < 0) {
        elTitle.textContent = 'The Teaching Network';
        elSub.textContent = 'click an orb · every topic links onward';
        for (var i = 0; i < st.nodes.length; i++) {
          if (!st.nodes[i].hub) continue;
          (function (ix) {
            mk(st.nodes[ix].id, st.nodes[ix].label, '', function () { go(ix); });
          })(i);
        }
        return;
      }
      var n = st.nodes[st.current];
      elTitle.textContent = n.label;
      elSub.textContent = n.hub
        ? n.id + ' · trunk'
        : n.id + ' · ' + (st.trunks[n.trunk] || n.trunk) + (n.adv ? ' · advanced' : '');
      var ad = st.adj[st.current].slice();
      ad.sort(function (a, b) { return b.k - a.k; });   // bridges first
      for (var j = 0; j < ad.length; j++) {
        (function (ix, kk) {
          var o = st.nodes[ix];
          mk(o.id, o.label, kk === EK_BRIDGE ? 'bridge' : '', function () { go(ix); });
        })(ad[j].j, ad[j].k);
      }
    }

    function go(i) {
      travelTo(st, i, tNow(), reduced);
      updatePanel();
      setHash(st.nodes[i].id);
      if (reduced) renderOnce();
    }

    function fitAll() {                        // the whole sky, no current orb
      var p = fitParams(st);
      st.current = -1;
      if (reduced) {
        st.cam = { x: p.x, y: p.y, z: p.z };
        renderOnce();
      } else {
        glideTo(st, p.x, p.y, p.z, tNow(), 1.2);
      }
      updatePanel();
      setHash('');
    }

    // keep the URL in step with travel (replaceState: Back still leaves the page)
    function setHash(id) {
      var loc = global.location;
      if (!loc) return;
      var want = id ? '#' + encodeURIComponent(id) : '';
      if ((loc.hash || '') === want) return;
      try {
        global.history.replaceState(null, '', want || (loc.pathname + loc.search));
      } catch (e) {
        try { loc.replace(want || '#'); } catch (e2) { /* leave the URL alone */ }
      }
    }

    /* pointer: click travels, drag pans */
    var down = null, moved = false;
    cv.addEventListener('pointerdown', function (ev) {
      var c = cameraAt(st, tNow());
      st.cam = { x: c.x, y: c.y, z: c.z };
      st.glide = null;
      down = { sx: ev.clientX, sy: ev.clientY, cx: c.x, cy: c.y };
      moved = false;
      cv.setPointerCapture(ev.pointerId);
    });
    cv.addEventListener('pointermove', function (ev) {
      if (down) {
        var dx = ev.clientX - down.sx, dy = ev.clientY - down.sy;
        if (Math.abs(dx) + Math.abs(dy) > 5) moved = true;
        if (moved) {
          st.cam.x = down.cx - dx / st.cam.z;
          st.cam.y = down.cy - dy / st.cam.z;
          if (reduced) renderOnce();
        }
        return;
      }
      var hov = pick(st, tNow(), ev.clientX, ev.clientY);
      if (hov !== st.hover) {
        st.hover = hov;
        cv.style.cursor = hov >= 0 ? 'pointer' : '';
        if (reduced) renderOnce();
      }
    });
    cv.addEventListener('pointerup', function (ev) {
      if (down && !moved) {
        var i = pick(st, tNow(), ev.clientX, ev.clientY);
        if (i >= 0) go(i);
      }
      down = null;
    });
    cv.addEventListener('pointercancel', function () { down = null; });

    cv.addEventListener('wheel', function (ev) {
      ev.preventDefault();
      var c = cameraAt(st, tNow());
      st.glide = null;
      var anchor = screenToWorld(st, c, ev.clientX, ev.clientY);
      var z2 = clamp(c.z * Math.exp(-ev.deltaY * 0.0016), 0.12, 4.5);
      st.cam = {
        x: anchor[0] - (ev.clientX - st.w / 2) / z2,
        y: anchor[1] - (ev.clientY - st.h / 2) / z2,
        z: z2
      };
      if (reduced) renderOnce();
    }, { passive: false });

    cv.addEventListener('dblclick', function (ev) {
      if (pick(st, tNow(), ev.clientX, ev.clientY) >= 0) return;
      fitAll();
    });

    resize();
    updatePanel();

    // arriving by deep link (teaching.html#CM-22, e.g. from a module's
    // "open in the Teaching Network"): glide there from the whole sky
    var h0 = nodeFromHash(st, global.location && global.location.hash);
    if (h0 >= 0) go(h0);
    global.addEventListener('hashchange', function () {
      var i = nodeFromHash(st, global.location.hash);
      if (i >= 0) {
        if (i !== st.current) go(i);
      } else if (!global.location.hash && st.current >= 0) {
        fitAll();
      }
    });
    if (reduced) {
      renderOnce();
    } else {
      raf = global.requestAnimationFrame(frame);
    }
    global.addEventListener('resize', resize);
    doc.addEventListener('visibilitychange', function () {
      if (reduced) return;
      if (doc.hidden) {
        global.cancelAnimationFrame(raf);
        last = null;
      } else {
        raf = global.requestAnimationFrame(frame);
      }
    });
  }

  if (global.document.readyState === 'loading') {
    global.document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : globalThis);
