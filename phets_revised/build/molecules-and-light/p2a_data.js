
/* ================================================================== *
 *  data tables                                                        *
 *                                                                     *
 *  PHET.*   read out of docs/phets/molecules-and-light_en.html,       *
 *           build 1.5.33, and its doc/model.md.  Cited as PhET's.     *
 *  VIB      NIST CCCBDB "Experimental Vibrational Frequencies"        *
 *           (cccbdb.nist.gov/exp2x.asp), retrieved 2026-09-22, to     *
 *           the precision CCCBDB prints, with CCCBDB's reference.     *
 *  GEOM     NIST CCCBDB "Experimental Geometries"                     *
 *           (cccbdb.nist.gov/expgeom2x.asp); the diatomics' r_e from  *
 *           the NIST WebBook, Constants of Diatomic Molecules.        *
 *  DIPOLE   NIST CCCBDB "Experimental Dipole Moments"                 *
 *           (cccbdb.nist.gov/diplistx.asp).                           *
 *  MASS     NIST Atomic Weights and Isotopic Compositions, principal  *
 *           isotope.                                                  *
 *  D0_EV    QUOTED, Active Thermochemical Tables / NIST-JANAF; NOT    *
 *           re-derived here, and labelled QUOTED wherever it is used. *
 * ================================================================== */

/* the 2019 SI defining constants -- h, c and e are EXACT, so hc and hc/e
   below are exact rational numbers and carry no uncertainty at all */
const PLANCK_H = 6.62607015e-34;        /* J s, exact by definition */
const LIGHT_C = 299792458;              /* m/s, exact by definition */
const ELEM_Q = 1.602176634e-19;         /* C,   exact by definition */
const BOLTZ_K = 1.380649e-23;           /* J/K, exact by definition */
const U_KG = 1.66053906892e-27;         /* atomic mass constant, CODATA 2022 */
const HC_JM = PLANCK_H * LIGHT_C;
const HC_EV_NM = PLANCK_H * LIGHT_C / ELEM_Q * 1e9;
const C_CM = LIGHT_C * 100;

/* ---------------- PhET's model constants ---------------- */
const PHET = {
  lam: {microwave: 0.2, infrared: 850e-9, visible: 580e-9, ultraviolet: 100e-9},
  P_ABSORB: 0.5,          /* PhotonAbsorptionStrategy: nextDouble() < 0.5 */
  HOLD_MIN: 1.1,          /* photonHoldCountdownTime = 1.1 + rand*(1.3-1.1) */
  HOLD_MAX: 1.3,
  HYSTERESIS: 0.2,        /* absorptionHysteresisCountdownTime after an emission */
  ABSORB_RADIUS: 100,     /* queryAbsorbPhoton: distance to the COG < 100 */
  PHOTON_SPEED: 3000,     /* PhotonAbsorptionModel.PHOTON_VELOCITY */
  EMITTER_X: -1350,       /* the emission position */
  EMIT_PERIOD: 0.8,       /* setPhotonEmissionPeriod when the source is on */
  VIB_HZ: 5.0,            /* advanceVibration(5 * dt * 2pi) */
  ROT_HZ: 1.1,            /* rotate(1.1 * dt * 2pi) */
  SLOW_FACTOR: 0.5,       /* TimeSpeed.SLOW halves dt */
  DT_CEILING: 0.2,        /* step(): a dt over 0.2 s is discarded whole */
  FRAG_A: 990,            /* the heavy fragment's speed */
  FRAG_B: 0.67 * 3000,    /* the light fragment's speed */
  PASS_LIST: 10,          /* the pass-through list is capped at ten photons */
};
const BANDS = ['microwave', 'infrared', 'visible', 'ultraviolet'];
const BANDNAME = {microwave: 'Microwave', infrared: 'Infrared',
                  visible: 'Visible', ultraviolet: 'Ultraviolet'};

/* PhET's Light Spectrum Diagram, from its own accessibility descriptions:
   [name, long-wavelength edge, short-wavelength edge] in metres */
const PHET_BANDS = [['radio', 1e4, 5e-1], ['microwave', 1e-1, 1e-3],
                    ['infrared', 1e-3, 7e-7], ['visible', 7e-7, 4e-7],
                    ['ultraviolet', 4e-7, 1e-8], ['x-ray', 1e-8, 5e-11],
                    ['gamma ray', 5e-11, 1e-12]];

/* PhET's response table, read from its setPhotonAbsorptionStrategy calls.
   '' means no strategy is registered, so the photon passes through. */
const PHET_TABLE = {
  CO:  {microwave: 'rotate', infrared: 'vibrate', visible: '', ultraviolet: ''},
  N2:  {microwave: '', infrared: '', visible: '', ultraviolet: ''},
  O2:  {microwave: '', infrared: '', visible: '', ultraviolet: ''},
  CO2: {microwave: '', infrared: 'vibrate', visible: '', ultraviolet: ''},
  CH4: {microwave: '', infrared: 'vibrate', visible: '', ultraviolet: ''},
  H2O: {microwave: 'rotate', infrared: 'vibrate', visible: '', ultraviolet: ''},
  NO2: {microwave: 'rotate', infrared: 'vibrate', visible: 'glow', ultraviolet: 'break'},
  O3:  {microwave: 'rotate', infrared: 'vibrate', visible: '', ultraviolet: 'break'},
};
/* PhET's own control-panel labels (inventory.json, MOLECULES_AND_LIGHT) */
const MOLORDER = ['CO', 'N2', 'O2', 'CO2', 'CH4', 'H2O', 'NO2', 'O3'];
const MOLNAME = {CO: 'Carbon Monoxide', N2: 'Nitrogen', O2: 'Oxygen',
                 CO2: 'Carbon Dioxide', CH4: 'Methane', H2O: 'Water',
                 NO2: 'Nitrogen Dioxide', O3: 'Ozone',
                 NO: 'Nitric Oxide', O: 'Oxygen atom'};
const MOLSHAPE = {CO: 'diatomic', N2: 'diatomic', O2: 'diatomic', NO: 'diatomic',
                  CO2: 'linear', CH4: 'tetrahedral', H2O: 'bent',
                  NO2: 'bent', O3: 'bent', O: 'atom'};
/* PhET's break-apart products */
const PHET_BREAK = {NO2: ['NO', 'O'], O3: ['O2', 'O']};

/* PhET's atom table (radius in its model units, mass in u).  NOTE the oxygen
   mass: PhET's Atom.oxygen() carries 12.011, which is CARBON's -- a
   copy-paste in its source.  It is kept here only where PhET's own drawing
   depends on it (the CO2 bend amplitude), and never used as physics. */
const PHET_ATOM = {C: {r: 77, m: 12.011}, H: {r: 37, m: 1},
                   N: {r: 75, m: 14.00674}, O: {r: 73, m: 12.011}};

/* PhET's drawing geometry, model units, y UP.  Every offset below is read
   out of the molecule classes' initializeAtomOffsets(); the vibration
   amplitudes come from their setVibration(). */
const PH_D2R = Math.PI / 180;
const CH4_A = 0.9 * Math.PI, CH4_HC = 155 * Math.cos(CH4_A), CH4_JC = 155 * Math.sin(CH4_A);
const CH4_W = Math.PI / 4, CH4_XC = 30 * Math.cos(CH4_W), CH4_YC = 30 * Math.sin(CH4_W);
const H2O_A = 109 * PH_D2R, H2O_AB = 130 * Math.cos(H2O_A / 2), H2O_LB = 130 * Math.sin(H2O_A / 2);
const H2O_M = PHET_ATOM.O.m + 2 * PHET_ATOM.H.m;
const H2O_OY = H2O_AB * (2 * PHET_ATOM.H.m / H2O_M), H2O_HY = -(H2O_AB - H2O_OY);
const NO2_A = 120 * PH_D2R, NO2_YB = 180 * Math.cos(NO2_A / 2);
const NO2_M = PHET_ATOM.N.m + 2 * PHET_ATOM.O.m;
const NO2_NY = NO2_YB * (2 * PHET_ATOM.O.m / NO2_M), NO2_OY = -(NO2_YB - NO2_NY);
const NO2_OX = 180 * Math.sin(NO2_A / 2);
const O3_A = 120 * PH_D2R, O3_IB = 180 * Math.cos(O3_A / 2), O3_QB = 360 * Math.sin(O3_A / 2);
const O3_CY = (2 / 3) * O3_IB, O3_OY = -O3_CY / 2, O3_OX = O3_QB / 2;
const CO2_SB = 40 * PHET_ATOM.C.m / (2 * PHET_ATOM.O.m);   /* = 20 with PhET's masses */

/* atoms: [element, x, y]; bonds: [i, j, order] */
const PHET_GEOM = {
  CO:  {atoms: [['C', -85, 0], ['O', 85, 0]], bonds: [[0, 1, 3]]},
  N2:  {atoms: [['N', -85, 0], ['N', 85, 0]], bonds: [[0, 1, 3]]},
  O2:  {atoms: [['O', -85, 0], ['O', 85, 0]], bonds: [[0, 1, 2]]},
  NO:  {atoms: [['N', -85, 0], ['O', 85, 0]], bonds: [[0, 1, 2]]},
  O:   {atoms: [['O', 0, 0]], bonds: []},
  CO2: {atoms: [['C', 0, 0], ['O', 170, 0], ['O', -170, 0]], bonds: [[0, 1, 2], [0, 2, 2]]},
  H2O: {atoms: [['O', 0, H2O_OY], ['H', H2O_LB, H2O_HY], ['H', -H2O_LB, H2O_HY]],
        bonds: [[0, 1, 1], [0, 2, 1]]},
  CH4: {atoms: [['C', 0, 0], ['H', 0, 155], ['H', CH4_HC, -CH4_JC],
                ['H', -CH4_HC, 30 - CH4_JC], ['H', 30, -125]],
        bonds: [[0, 1, 1], [0, 2, 1], [0, 3, 1], [0, 4, 1]]},
  NO2: {atoms: [['N', 0, NO2_NY], ['O', NO2_OX, NO2_OY], ['O', -NO2_OX, NO2_OY]],
        bonds: [[0, 1, 2], [0, 2, 1]]},
  O3:  {atoms: [['O', 0, O3_CY], ['O', O3_OX, O3_OY], ['O', -O3_OX, O3_OY]],
        bonds: [[0, 1, 2], [0, 2, 1]]},
};
/* PhET's own vibration: the offset each atom takes at phase q.  Returns an
   array of [dx, dy] in PhET's model units.  This is PhET's animation, not a
   normal mode, and the file says so wherever it is drawn. */
function phetVibration(mol, q) {
  const t = Math.sin(q);
  if (mol === 'CO') return [[20 * t, 0], [-20 * t, 0]];
  if (mol === 'CO2') return [[0, 40 * t], [0, -CO2_SB * t], [0, -CO2_SB * t]];
  if (mol === 'H2O') return [[0, -3 * t], [18 * t, 18 * t], [-18 * t, 18 * t]];
  if (mol === 'NO2') return [[0, -30 * t], [15 * t, 15 * t], [-15 * t, 15 * t]];
  if (mol === 'O3') return [[0, 30 * t], [-15 * t, -15 * t], [15 * t, -15 * t]];
  if (mol === 'CH4') {
    const s = 1.5 * t, a = Math.abs(s);
    const h1 = [s * CH4_XC, -a * CH4_YC];
    const h2 = [s * CH4_XC, -s * CH4_YC];
    const h3 = [-s * CH4_XC, -s * CH4_YC];
    const h4 = [s * CH4_XC, a * CH4_YC];
    const k = -PHET_ATOM.H.m / PHET_ATOM.C.m;
    const G = PHET_GEOM.CH4.atoms;
    const sx = (G[1][1] + h1[0]) + (G[2][1] + h2[0]) + (G[3][1] + h3[0]) + (G[4][1] + h4[0]);
    const sy = (G[1][2] + h1[1]) + (G[2][2] + h2[1]) + (G[3][2] + h3[1]) + (G[4][2] + h4[1]);
    return [[k * sx, k * sy], h1, h2, h3, h4];
  }
  return PHET_GEOM[mol].atoms.map(() => [0, 0]);
}

/* ---------------- the measured spectroscopy ---------------- */
/* [wavenumber cm-1, symmetry species, description, degeneracy] */
const VIB = {
  CO:  [[2143, '&Sigma;', 'stretch', 1]],
  N2:  [[2330, '&Sigma;g', 'stretch', 1]],
  O2:  [[1556, '&Sigma;g', 'stretch', 1]],
  NO:  [[1876, '&Sigma;', 'stretch', 1]],
  CO2: [[1333, '&Sigma;g', 'symmetric stretch', 1], [667, '&Pi;u', 'bend', 2],
        [2349, '&Sigma;u', 'antisymmetric stretch', 1]],
  H2O: [[3657, 'A1', 'symmetric stretch', 1], [1595, 'A1', 'bend', 1],
        [3756, 'B2', 'antisymmetric stretch', 1]],
  O3:  [[1110, 'A1', 'symmetric stretch', 1], [705, 'A1', 'bend', 1],
        [1042, 'B2', 'antisymmetric stretch', 1]],
  NO2: [[1318, 'A1', 'symmetric stretch', 1], [750, 'A1', 'bend', 1],
        [1618, 'B2', 'antisymmetric stretch', 1]],
  CH4: [[2917, 'A1', 'symmetric stretch', 1], [1534, 'E', 'deformation', 2],
        [3019, 'T2', 'degenerate stretch', 3], [1306, 'T2', 'degenerate deformation', 3]],
};
const VIB_REF = {CO: '1979HUB/HER', N2: '2007Iri:389', O2: '1979HUB/HER', NO: '2007Iri:389',
                 CO2: '1945Herzberg', H2O: 'Shimanouchi', O3: '1966Herzberg',
                 NO2: 'Shimanouchi', CH4: 'Shimanouchi / 1982 intensities'};
/* r in angstrom, ang in degrees (null for a diatomic) */
const GEOM = {
  CO:  {r: 1.128323, ang: null, ref: 'WebBook r_e (Huber &amp; Herzberg)'},
  N2:  {r: 1.097685, ang: null, ref: 'WebBook r_e (Huber &amp; Herzberg)'},
  O2:  {r: 1.20752, ang: null, ref: 'WebBook r_e (Huber &amp; Herzberg)'},
  NO:  {r: 1.15077, ang: null, ref: 'WebBook r_e (Huber &amp; Herzberg)'},
  CO2: {r: 1.162, ang: 180.0, ref: 'CCCBDB 1966Herzberg'},
  H2O: {r: 0.958, ang: 104.4776, ref: 'CCCBDB 1979Hoy/Bun:1'},
  O3:  {r: 1.278, ang: 116.8, ref: 'CCCBDB 1966Herzberg'},
  NO2: {r: 1.193, ang: 134.1, ref: 'CCCBDB 1966Herzberg'},
  CH4: {r: 1.087, ang: 109.471, ref: 'CCCBDB 1979Hir:213'},
};
const DIPOLE = {CO: 0.112, N2: 0.0, O2: 0.0, NO: 0.159, CO2: 0.0,
                H2O: 1.857, O3: 0.530, NO2: 0.316, CH4: 0.0};
/* NIST Atomic Weights and Isotopic Compositions, principal isotope */
const MASS = {H: 1.00782503223, C: 12.0, N: 14.00307400443, O: 15.99491461957};
/* Huber & Herzberg's Dunham constants; a value in SQUARE BRACKETS in that
   table belongs to the stated vibrational level, not to the equilibrium
   geometry -- O2's "Be" is B_0, which is what derive.py proves from r_e. */
const DIATOMIC = {
  CO: {we: 2169.81358, wexe: 13.28831, Bprint: 1.93128087, ae: 0.01750441, re: 1.128323, bracketed: false},
  N2: {we: 2358.57, wexe: 14.324, Bprint: 1.998241, ae: 0.017318, re: 1.097685, bracketed: false},
  O2: {we: 1580.193, wexe: 11.981, Bprint: 1.4376766, ae: 0.01593, re: 1.20752, bracketed: true},
};
/* bond dissociation energies at 0 K, eV.  QUOTED (Active Thermochemical
   Tables / NIST-JANAF); NOT re-derived here, and said so on the canvas. */
const D0_EV = {O2: 5.1156, O3: 1.0520, NO2: 3.1163, N2: 9.7538,
               CO: 11.1088, H2O: 5.1102, CH4: 4.4800, CO2: 5.4533};
const D0_CHANNEL = {O2: 'O + O', O3: 'O&#8322; + O', NO2: 'NO + O', N2: 'N + N',
                    CO: 'C + O', H2O: 'H + OH', CH4: 'CH&#8323; + H', CO2: 'CO + O'};
/* fixed point charges, in units of e.  The MAGNITUDE is arbitrary -- every
   selection-rule zero below must be independent of it, and selfTest checks
   exactly that by rescaling them. */
const CHARGE = {CO: [0.5, -0.5], NO: [0.5, -0.5], N2: [0, 0], O2: [0, 0],
                CO2: [-0.5, 1.0, -0.5], H2O: [0.4, -0.8, 0.4],
                O3: [-0.25, 0.5, -0.25], NO2: [-0.4, 0.8, -0.4],
                CH4: [-0.4, 0.1, 0.1, 0.1, 0.1]};

/* CPK-style element colours for a dark ground, as molecule_shapes.html and
   amino_acids.html use them.  Cosmetic: nothing is computed from them. */
const ELCOL = {H: '#e8e8ee', C: '#aab2c0', N: '#5f86ff', O: '#ff5a5a'};
const ATOM_R = {H: 0.15, C: 0.24, N: 0.23, O: 0.22};

/* Earth's dry-air composition by volume, NASA Earth Fact Sheet, except the
   CO2 mixing ratio, which is NOAA GML's global monthly mean for June 2026
   (427.62 ppm) -- a figure that page itself calls preliminary. */
const AIR = [['N&#8322;', 78.084, 'no dipole, no IR-active mode', false],
             ['O&#8322;', 20.946, 'no dipole, no IR-active mode', false],
             ['Ar', 0.934, 'monatomic: nothing to vibrate', false],
             ['CO&#8322;', 427.62e-4, 'bend 667, stretch 2349 cm&#8315;&#185;', true],
             ['Ne', 18.18e-4, 'monatomic', false],
             ['He', 5.24e-4, 'monatomic', false],
             ['CH&#8324;', 1.94e-4, 'two IR-active modes, 1306 and 3019 cm&#8315;&#185;', true]];
const CO2_PPM = 427.62;
const T_EARTH = 288;      /* the conventional global mean surface temperature */
/* the atmospheric window, in micrometres -- a conventional range, not a
   measurement, and the picture shows why it is drawn where it is */
const WINDOW_UM = [8, 13];
/* two transitions quoted rather than derived, and labelled so on the canvas */
const QUOTED_LINES = [
  ['CO J = 1 &larr; 0', 115.2712018e9, 'the 2.6 mm line radio astronomy maps'],
  ['H&#8322;O 6&#8321;&#8326;&ndash;5&#8322;&#8323;', 22.23508e9, 'the 1.35 cm water line'],
];
