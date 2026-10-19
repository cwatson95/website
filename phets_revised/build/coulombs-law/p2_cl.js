
/* ================================================================== *
 *  electrostatics: CODATA's k and e, PhET's two tracks, and the       *
 *  comparison with gravity                                            *
 * ================================================================== */
const EPS0=8.8541878188e-12;       /* F/m, CODATA 2022 (scipy.constants 1.18, derive.py) */
const K_E=1/(4*PI*EPS0);           /* N m^2 C^-2: 8.987551786170797e9 */
const E_CH=1.602176634e-19;        /* C, exact since the 2019 SI */
const G_N=6.6743e-11;              /* m^3 kg^-1 s^-2, CODATA 2022 — for the gravity comparison */
const M_E=9.1093837139e-31, M_P=1.67262192595e-27;   /* kg, CODATA 2022 */
const A0=5.29177210544e-11;        /* m, the Bohr radius, CODATA 2022 */
const K_PHET=8987551e3, E_PHET=1.6021766208e-19;     /* PhET's values (ISLCConstants) */
const Q_MAX=10;                    /* PhET's charge range: +-10 uC (macro), +-10 e (atomic), whole units */

/* PhET's two tracks.  macro: charges 6.75 mm in radius on a 1-mm grid within
   +-5 cm, 1 mm between surfaces asked for — but 6.75 + 6.75 + 1 mm sums to
   14.4999... mm in floating point and snaps DOWN, so the closest centres sit
   14 mm apart with a 0.5-mm gap (PhET's own arithmetic, reproduced).  atomic:
   0.95 pm on a 1-pm grid within +-50 pm, 0.1 pm between surfaces.  Display
   units: centimetres and picometres; charge units: microcoulombs and e. */
const TRACKS={
  macro:{q:0.001, perM:1000, iL:-50, iR:50, sep:0.001, C:K_E, R:0.00675,
         unit:'cm', uPerM:100, qUnit:'µC', qSI:1e-6, places:3},
  atomic:{q:1e-12, perM:1e12, iL:-50, iR:50, sep:1e-13, C:K_E, R:9.5e-13,
         unit:'pm', uPerM:1e12, qUnit:'e', qSI:E_CH, places:9},
};
function chargeSteps(T){ return minSteps(T,T.R,T.R); }

/* ---- electricity and gravity ---------------------------------------------
   Both laws fall as 1/r^2, so their ratio for a given pair of particles is the
   same at every distance: k e^2 / (G m_e m_p) for the hydrogen atom's pair. */
function ratioEG(m1,m2){ return K_E*E_CH*E_CH/(G_N*m1*m2); }
/* the equal masses that would pull as hard as two charges push or pull: from
   G m^2 / r^2 = |k q1 q2| / r^2 — independent of r, for the same reason */
function equalMass(q1,q2){ return Math.sqrt(Math.abs(K_E*q1*q2)/G_N); }
