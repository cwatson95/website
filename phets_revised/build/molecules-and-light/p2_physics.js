
/* ================================================================== *
 *  physics                                                            *
 *  1  exact photon arithmetic                                         *
 *  2  the seeded generator                                            *
 *  3  geometry, the valence force field, the Hessian, Jacobi          *
 *  4  normal modes and the infrared selection rule                    *
 *  5  PhET's chamber, stepped by PhET's own rules                     *
 *  6  Planck                                                          *
 * ================================================================== */

/* ---- 1. photons.  E = hc/lambda, and hc is exact. ---- */
function photonOf(lam_m) {
  return {lam: lam_m, nu: LIGHT_C / lam_m, E_J: HC_JM / lam_m,
          E_eV: HC_JM / lam_m / ELEM_Q, nubar: 1 / (lam_m * 100)};
}
/* the same energy by the identity the file prints, as a second route */
function eVfromNm(lam_nm) { return HC_EV_NM / lam_nm; }
function nubarToEv(nubar_cm) { return nubar_cm * 100 * HC_JM / ELEM_Q; }
function nubarToUm(nubar_cm) { return 1e4 / nubar_cm; }
/* which of PhET's own spectrum bands a wavelength falls in (null = none) */
function bandOf(lam_m) {
  for (const [name, hi, lo] of PHET_BANDS) if (lam_m >= lo && lam_m <= hi) return name;
  return null;
}
const PHOTON = {};
for (const b of BANDS) PHOTON[b] = photonOf(PHET.lam[b]);

/* ---- 2. the seeded generator (mulberry32: 32-bit throughout, so the
   Python twin reproduces it bit for bit with masked arithmetic) ---- */
function mulberry32(seed) {
  let a = seed | 0;
  return function () {
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* ---- 3. geometry and the valence force field ---- */
/* equilibrium Cartesians in angstrom, centre of mass at the origin, the
   molecule in the x-y plane with the symmetry axis along y */
function geomXY(mol) {
  const g = GEOM[mol], r = g.r;
  let sym, X;
  if (mol === 'CO' || mol === 'N2' || mol === 'O2' || mol === 'NO') {
    sym = {CO: ['C', 'O'], N2: ['N', 'N'], O2: ['O', 'O'], NO: ['N', 'O']}[mol];
    X = [[-r / 2, 0, 0], [r / 2, 0, 0]];
  } else if (mol === 'CO2') {
    sym = ['O', 'C', 'O'];
    X = [[-r, 0, 0], [0, 0, 0], [r, 0, 0]];
  } else if (mol === 'CH4') {
    sym = ['C', 'H', 'H', 'H', 'H'];
    const d = r / Math.sqrt(3);
    X = [[0, 0, 0], [d, d, d], [d, -d, -d], [-d, d, -d], [-d, -d, d]];
  } else {
    const cen = {H2O: 'O', O3: 'O', NO2: 'N'}[mol];
    const out = {H2O: 'H', O3: 'O', NO2: 'O'}[mol];
    sym = [out, cen, out];
    const half = g.ang * Math.PI / 360;
    X = [[-r * Math.sin(half), -r * Math.cos(half), 0], [0, 0, 0],
         [r * Math.sin(half), -r * Math.cos(half), 0]];
  }
  const m = sym.map(a => MASS[a]);
  const M = m.reduce((s, v) => s + v, 0);
  const c = [0, 1, 2].map(k => X.reduce((s, p, i) => s + m[i] * p[k], 0) / M);
  return {sym, X: X.map(p => [p[0] - c[0], p[1] - c[1], p[2] - c[2]]), m};
}
function bondsOf(mol) {
  return {CO: [[0, 1]], N2: [[0, 1]], O2: [[0, 1]], NO: [[0, 1]],
          CO2: [[1, 0], [1, 2]], H2O: [[1, 0], [1, 2]], O3: [[1, 0], [1, 2]],
          NO2: [[1, 0], [1, 2]],
          CH4: [[0, 1], [0, 2], [0, 3], [0, 4]]}[mol];
}
function anglesOf(mol) {
  if (mol === 'CO2' || mol === 'H2O' || mol === 'O3' || mol === 'NO2') return [[0, 1, 2]];
  if (mol === 'CH4') {
    const out = [];
    for (let i = 1; i <= 4; i++) for (let j = i + 1; j <= 4; j++) out.push([i, 0, j]);
    return out;
  }
  return [];
}
const vlen = (a, b) => Math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2);
/* the valence force field, energy in aJ.  f = [f_r, f_rr, f_th, f_rth,
   f_thth, f_thth2]; lengths in angstrom, so f is in aJ/A^2 = mdyn/A. */
function potentialV(mol, X, f) {
  const g = GEOM[mol], re = g.r;
  const [f_r, f_rr, f_th, f_rth, f_thth, f_thth2] = f;
  const bl = bondsOf(mol), dr = bl.map(([i, j]) => vlen(X[i], X[j]) - re);
  let V = 0;
  for (const d of dr) V += 0.5 * f_r * d * d;
  for (let a = 0; a < dr.length; a++) for (let b = a + 1; b < dr.length; b++) V += f_rr * dr[a] * dr[b];
  const ang = anglesOf(mol);
  if (!ang.length) return V;
  const linear = Math.abs(g.ang - 180) < 1e-9;
  const da = [];
  for (const [i, j, k] of ang) {
    const u = [X[i][0] - X[j][0], X[i][1] - X[j][1], X[i][2] - X[j][2]];
    const w = [X[k][0] - X[j][0], X[k][1] - X[j][1], X[k][2] - X[j][2]];
    const lu = Math.sqrt(u[0] * u[0] + u[1] * u[1] + u[2] * u[2]);
    const lw = Math.sqrt(w[0] * w[0] + w[1] * w[1] + w[2] * w[2]);
    let ct = (u[0] * w[0] + u[1] * w[1] + u[2] * w[2]) / (lu * lw);
    ct = ct > 1 ? 1 : (ct < -1 ? -1 : ct);
    if (linear) {
      /* a LINEAR molecule's bend: (pi - theta)^2 = 2(1 + cos theta) to
         leading order, and 1 + cos theta is smooth in the Cartesians where
         arccos is not.  This IS the harmonic bend coordinate. */
      V += 0.5 * f_th * re * re * 2 * (1 + ct);
    } else da.push(Math.acos(ct) - g.ang * Math.PI / 180);
  }
  if (linear) return V;
  for (const d of da) V += 0.5 * f_th * re * re * d * d;
  if (da.length === 1) { V += f_rth * re * (dr[0] + dr[1]) * da[0]; return V; }
  for (let a = 0; a < ang.length; a++) {
    for (let b = a + 1; b < ang.length; b++) {
      const share = (ang[a][0] === ang[b][0] || ang[a][0] === ang[b][2] ||
                     ang[a][2] === ang[b][0] || ang[a][2] === ang[b][2]);
      V += (share ? f_thth : f_thth2) * re * re * da[a] * da[b];
    }
  }
  for (let a = 0; a < ang.length; a++) {
    for (let k = 0; k < bl.length; k++) {
      if (bl[k][1] === ang[a][0] || bl[k][1] === ang[a][2]) V += f_rth * re * dr[k] * da[a];
    }
  }
  return V;
}
function hessianOf(mol, f, h) {
  h = h || 2e-4;
  const {sym, X} = geomXY(mol), n = sym.length * 3;
  const flat = [];
  for (const p of X) flat.push(p[0], p[1], p[2]);
  const V = v => {
    const P = [];
    for (let i = 0; i < v.length; i += 3) P.push([v[i], v[i + 1], v[i + 2]]);
    return potentialV(mol, P, f);
  };
  const H = [];
  for (let i = 0; i < n; i++) H.push(new Array(n).fill(0));
  for (let a = 0; a < n; a++) {
    for (let b = a; b < n; b++) {
      const v1 = flat.slice(), v2 = flat.slice(), v3 = flat.slice(), v4 = flat.slice();
      v1[a] += h; v1[b] += h;
      v2[a] += h; v2[b] -= h;
      v3[a] -= h; v3[b] += h;
      v4[a] -= h; v4[b] -= h;
      H[a][b] = H[b][a] = (V(v1) - V(v2) - V(v3) + V(v4)) / (4 * h * h);
    }
  }
  return {sym, X, H};
}
/* the mass-weighted rigid motions: three translations and the rotations that
   are not identically zero.  Orthonormalised by Gram-Schmidt. */
function eckartBasis(sym, X) {
  const sq = sym.map(a => Math.sqrt(MASS[a])), n = sym.length;
  const raw = [];
  for (let al = 0; al < 3; al++) {
    const v = new Array(3 * n).fill(0);
    for (let i = 0; i < n; i++) v[3 * i + al] = sq[i];
    raw.push(v);
  }
  for (let al = 0; al < 3; al++) {
    const e = [0, 0, 0]; e[al] = 1;
    const v = new Array(3 * n).fill(0);
    for (let i = 0; i < n; i++) {
      const c = [e[1] * X[i][2] - e[2] * X[i][1], e[2] * X[i][0] - e[0] * X[i][2],
                 e[0] * X[i][1] - e[1] * X[i][0]];
      for (let k = 0; k < 3; k++) v[3 * i + k] = c[k] * sq[i];
    }
    raw.push(v);
  }
  const B = [];
  for (let v of raw) {
    v = v.slice();
    for (const u of B) {
      let d = 0; for (let k = 0; k < v.length; k++) d += u[k] * v[k];
      for (let k = 0; k < v.length; k++) v[k] -= d * u[k];
    }
    let nn = 0; for (const x of v) nn += x * x;
    nn = Math.sqrt(nn);
    if (nn > 1e-8) B.push(v.map(x => x / nn));
  }
  return B;
}
/* cyclic Jacobi for a symmetric matrix; returns eigenvalues and the columns
   of the eigenvector matrix */
function jacobiEig(Ain) {
  const n = Ain.length;
  const A = Ain.map(r => r.slice());
  const Vv = [];
  for (let i = 0; i < n; i++) { Vv.push(new Array(n).fill(0)); Vv[i][i] = 1; }
  for (let sweep = 0; sweep < 100; sweep++) {
    let off = 0;
    for (let p = 0; p < n; p++) for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
    if (off < 1e-30) break;
    for (let p = 0; p < n; p++) {
      for (let q = p + 1; q < n; q++) {
        if (Math.abs(A[p][q]) < 1e-18) continue;
        const theta = (A[q][q] - A[p][p]) / (2 * A[p][q]);
        const t = Math.sign(theta || 1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
        const c = 1 / Math.sqrt(t * t + 1), s = t * c;
        for (let k = 0; k < n; k++) {
          const akp = A[k][p], akq = A[k][q];
          A[k][p] = c * akp - s * akq; A[k][q] = s * akp + c * akq;
        }
        for (let k = 0; k < n; k++) {
          const apk = A[p][k], aqk = A[q][k];
          A[p][k] = c * apk - s * aqk; A[q][k] = s * apk + c * aqk;
        }
        for (let k = 0; k < n; k++) {
          const vkp = Vv[k][p], vkq = Vv[k][q];
          Vv[k][p] = c * vkp - s * vkq; Vv[k][q] = s * vkp + c * vkq;
        }
      }
    }
  }
  return {val: A.map((r, i) => r[i]), vec: Vv};
}
/* an eigenvalue of the mass-weighted Hessian, in aJ/(A^2 u), as cm-1 */
const CONV_S2 = 1e-18 / (1e-20 * U_KG);
function eigToWavenumber(lam) {
  return lam <= 0 ? -Math.sqrt(-lam * CONV_S2) / (2 * Math.PI * C_CM)
                  : Math.sqrt(lam * CONV_S2) / (2 * Math.PI * C_CM);
}

/* ---- 4. normal modes ---- */
/* A degenerate pair has no preferred basis.  Rotating it so one member lies
   wholly in the drawing plane is a CHOICE, and the pair's own invariants --
   its two wavenumbers -- are untouched by it. */
function deplanePair(a, b) {
  const k = a.reduce((best, _, i) => (Math.abs(a[i][2]) + Math.abs(b[i][2]) >
                                      Math.abs(a[best][2]) + Math.abs(b[best][2]) ? i : best), 0);
  const za = a[k][2], zb = b[k][2];
  const c1 = a.map((p, i) => [zb * p[0] - za * b[i][0], zb * p[1] - za * b[i][1], zb * p[2] - za * b[i][2]]);
  const c2 = a.map((p, i) => [za * p[0] + zb * b[i][0], za * p[1] + zb * b[i][1], za * p[2] + zb * b[i][2]]);
  const mx = v => Math.max.apply(null, v.map(p => Math.max(Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2]))));
  if (mx(c1) < 1e-12 || mx(c2) < 1e-12) return null;
  return [c1.map(p => p.map(x => x / mx(c1))), c2.map(p => p.map(x => x / mx(c2)))];
}
const MODE_CACHE = {};
function normalModes(mol) {
  if (MODE_CACHE[mol]) return MODE_CACHE[mol];
  let out;
  if (MOLSHAPE[mol] === 'diatomic') {
    /* symmetry and momentum alone: (1, -m1/m2), exactly */
    const {sym} = geomXY(mol);
    const m1 = MASS[sym[0]], m2 = MASS[sym[1]];
    let d = [[1, 0, 0], [-m1 / m2, 0, 0]];
    const mx = Math.max(1, Math.abs(m1 / m2));
    d = d.map(p => p.map(x => x / mx));
    out = [{nu: VIB[mol][0][0], d, exact: true}];
  } else {
    const f = FIELDS[mol];
    const {sym, X, H} = hessianOf(mol, f);
    const n = sym.length;
    const w = [];
    for (let i = 0; i < n; i++) for (let k = 0; k < 3; k++) w.push(1 / Math.sqrt(MASS[sym[i]]));
    const N = 3 * n;
    let Hw = [];
    for (let i = 0; i < N; i++) {
      const row = new Array(N);
      for (let j = 0; j < N; j++) row[j] = 0.5 * (H[i][j] + H[j][i]) * w[i] * w[j];
      Hw.push(row);
    }
    /* Eckart projection: a finite-difference Hessian is only translationally
       and rotationally invariant to O(h^2), and the residual leaks into the
       eigenvectors as a spurious drift and spin.  Project the rigid motions
       out and every mode conserves momentum to machine precision. */
    const B = eckartBasis(sym, X);
    const P = [];
    for (let i = 0; i < N; i++) {
      const row = new Array(N).fill(0);
      row[i] = 1;
      for (const u of B) for (let j = 0; j < N; j++) row[j] -= u[i] * u[j];
      P.push(row);
    }
    const mul = (A, Bm) => A.map(r => {
      const o = new Array(N).fill(0);
      for (let k = 0; k < N; k++) { const v = r[k]; if (v) for (let j = 0; j < N; j++) o[j] += v * Bm[k][j]; }
      return o;
    });
    Hw = mul(mul(P, Hw), P);
    for (let i = 0; i < N; i++) for (let j = i + 1; j < N; j++) {
      const a = 0.5 * (Hw[i][j] + Hw[j][i]); Hw[i][j] = Hw[j][i] = a;
    }
    const {val, vec} = jacobiEig(Hw);
    const idx = val.map((v, i) => i).sort((a, b) => val[b] - val[a]).slice(0, N - B.length);
    out = idx.map(k => {
      const d = [];
      for (let i = 0; i < n; i++) d.push([vec[3 * i][k] * w[3 * i], vec[3 * i + 1][k] * w[3 * i + 1],
                                          vec[3 * i + 2][k] * w[3 * i + 2]]);
      let mx = 0;
      for (const p of d) mx = Math.max(mx, Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2]));
      return {nu: eigToWavenumber(val[k]), d: d.map(p => p.map(x => x / mx)), exact: false};
    });
    for (let i = 0; i < out.length - 1; i++) {
      if (Math.abs(out[i].nu - out[i + 1].nu) > 0.5) continue;
      const pair = deplanePair(out[i].d, out[i + 1].d);
      if (pair) { out[i].d = pair[0]; out[i + 1].d = pair[1]; }
    }
  }
  /* the degeneracy, which IS the symmetry species, and the selection rule */
  for (const m of out) {
    m.mult = out.filter(o => Math.abs(o.nu - m.nu) < 0.5).length;
    m.dmu = dmuDq(mol, m.d, 1);
    m.dmu2 = dmuDq(mol, m.d, 2.7);
    m.active = m.dmu > 1e-9;
    const v = VIB[mol].filter(r => Math.abs(r[0] - m.nu) < 0.6)[0];
    m.sym = v ? v[1] : '?';
    m.what = v ? v[2] : '';
  }
  MODE_CACHE[mol] = out;
  return out;
}
/* |d mu / dQ| for rigid point charges.  Every zero below must be independent
   of the charge magnitude -- `scale` is what selfTest varies to prove it. */
function dmuDq(mol, d, scale) {
  const q = CHARGE[mol];
  let x = 0, y = 0, z = 0;
  for (let i = 0; i < d.length; i++) { x += q[i] * d[i][0]; y += q[i] * d[i][1]; z += q[i] * d[i][2]; }
  return scale * Math.sqrt(x * x + y * y + z * z);
}
/* the inversion character, for the centrosymmetric molecules.  A mode that
   maps to +itself under i cannot change a dipole, because i sends every
   component of mu to -mu.  Independent of the charge model above. */
const INV_PERM = {N2: [1, 0], O2: [1, 0], CO2: [2, 1, 0]};
function inversionChi(mol, d) {
  const perm = INV_PERM[mol];
  if (!perm) return 0;
  const dp = d.map(() => [0, 0, 0]);
  for (let i = 0; i < d.length; i++) for (let k = 0; k < 3; k++) dp[perm[i]][k] = -d[i][k];
  let same = 0, opp = 0;
  for (let i = 0; i < d.length; i++) for (let k = 0; k < 3; k++) {
    same = Math.max(same, Math.abs(dp[i][k] - d[i][k]));
    opp = Math.max(opp, Math.abs(dp[i][k] + d[i][k]));
  }
  if (same < 1e-7) return +1;
  if (opp < 1e-7) return -1;
  return 0;
}
/* the exact B2 antisymmetric-stretch shape of a bent XY2, from the bond
   angle and the masses alone: zero linear and zero angular momentum force
   v1 = u1 cot(theta/2) and u_X = -2 m_Y u1 / m_X, with v_X = 0. */
function bentB2Exact(mol) {
  const {sym} = geomXY(mol);
  const mY = MASS[sym[0]], mX = MASS[sym[1]];
  const cot = 1 / Math.tan(GEOM[mol].ang * Math.PI / 360);
  let d = [[1, cot, 0], [-2 * mY / mX, 0, 0], [1, -cot, 0]];
  let mx = 0;
  for (const p of d) mx = Math.max(mx, Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2]));
  return d.map(p => p.map(x => x / mx));
}
/* the exact linear-XY2 shapes */
function linearExact(mol, which) {
  const {sym} = geomXY(mol);
  const ratio = 2 * MASS[sym[0]] / MASS[sym[1]];
  let d;
  if (which === 'sym') d = [[1, 0, 0], [0, 0, 0], [-1, 0, 0]];
  else if (which === 'asym') d = [[1, 0, 0], [-ratio, 0, 0], [1, 0, 0]];
  else d = [[0, 1, 0], [0, -ratio, 0], [0, 1, 0]];
  let mx = 0;
  for (const p of d) mx = Math.max(mx, Math.abs(p[0]), Math.abs(p[1]), Math.abs(p[2]));
  return d.map(p => p.map(x => x / mx));
}
/* the diatomic force constant, from the measured fundamental */
function diatomicK(mol) {
  const {sym} = geomXY(mol);
  const mu = MASS[sym[0]] * MASS[sym[1]] / (MASS[sym[0]] + MASS[sym[1]]) * U_KG;
  const nub = VIB[mol][0][0];
  return (2 * Math.PI * C_CM * nub) ** 2 * mu;
}
/* B_e from the geometry, an independent route to a tabulated number */
function BeFromGeometry(mol) {
  const {sym} = geomXY(mol);
  const mu = MASS[sym[0]] * MASS[sym[1]] / (MASS[sym[0]] + MASS[sym[1]]) * U_KG;
  const I = mu * Math.pow(DIATOMIC[mol].re * 1e-10, 2);
  return PLANCK_H / (8 * Math.PI * Math.PI * C_CM * I);
}
/* the photodissociation threshold from a QUOTED bond energy */
function threshNm(mol) { return HC_EV_NM / D0_EV[mol]; }

/* ---- 5. PhET's chamber ---- */
function newChamber(seed, mol, band) {
  const ch = {rng: mulberry32(seed), mol, band, photons: [], t: 0,
              state: 'idle', hold: 0, hyst: 0, vibPhase: 0, rot: 0, rotDir: 1,
              frags: null, glow: 0, emitTimer: Infinity, source: false,
              fired: 0, absorbed: 0, passed: 0, reemitted: 0, broke: 0,
              lastEvent: '', busyTime: 0, liveTime: 0, holds: []};
  ch.resonanceRight = ch.rng() < 0.5;    /* PhET picks one resonance structure */
  return ch;
}
function chamberReset(ch, seed) {
  const mol = ch.mol, band = ch.band;
  const n = newChamber(seed === undefined ? 12345 : seed, mol, band);
  for (const k in n) ch[k] = n[k];
  return ch;
}
function chamberFire(ch, over) {
  ch.photons.push({x: PHET.EMITTER_X + PHET.PHOTON_SPEED * (over || 0), y: 0,
                   vx: PHET.PHOTON_SPEED, vy: 0, band: ch.band, pass: false});
  ch.fired++;
}
function chamberSetSource(ch, on) {
  ch.source = on;
  if (on) { if (ch.emitTimer === Infinity) ch.emitTimer = 0; }
  else ch.emitTimer = Infinity;
}
/* PhET's queryAbsorbPhoton, rule for rule.  The pass-through list is what
   makes the FIRST failed trial final, so each photon gets exactly one. */
function chamberQuery(ch, p) {
  if (ch.state === 'broken') return false;
  if (ch.hyst > 0) return false;
  if (Math.hypot(p.x, p.y) >= PHET.ABSORB_RADIUS) return false;
  if (p.pass) return false;
  const strat = PHET_TABLE[ch.mol][p.band];
  const busy = ch.state !== 'idle';
  if (!strat || busy) { p.pass = true; ch.passed++; return false; }
  if (ch.rng() < PHET.P_ABSORB) {
    ch.absorbed++;
    ch.hold = PHET.HOLD_MIN + ch.rng() * (PHET.HOLD_MAX - PHET.HOLD_MIN);
    ch.holds.push(ch.hold);
    if (strat === 'rotate') { ch.state = 'rot'; ch.rotDir = ch.rng() < 0.5 ? -1 : 1; }
    else if (strat === 'vibrate') ch.state = 'vib';
    else if (strat === 'glow') ch.state = 'glow';
    else if (strat === 'break') { ch.state = 'break'; ch.hold = 0; }
    ch.lastEvent = strat;
    return true;
  }
  p.pass = true; ch.passed++; return false;
}
function chamberBreak(ch) {
  const prod = PHET_BREAK[ch.mol];
  if (!prod) { ch.state = 'idle'; return; }
  /* PhET's break-apart: the heavy fragment leaves at 990 and the light one
     at 0.67 x 3000 in the opposite direction, at an angle it draws from the
     same generator (pi/4 or pi/2 plus a quarter turn of random). */
  const base = ch.resonanceRight ? Math.PI / 4 : Math.PI / 2;
  const e = base + ch.rng() * Math.PI / 4;
  const G = PHET_GEOM[ch.mol].atoms;
  const side = ch.resonanceRight ? 1 : -1;
  const cx = (G[0][1] + G[1][1] * side) / 2, cy = (G[0][2] + G[1][2]) / 2;
  ch.frags = [{mol: prod[0], x: cx, y: cy, vx: PHET.FRAG_A * Math.cos(e), vy: PHET.FRAG_A * Math.sin(e), rot: 0},
              {mol: prod[1], x: -side * G[1][1], y: G[1][2],
               vx: -PHET.FRAG_B * Math.cos(e), vy: -PHET.FRAG_B * Math.sin(e), rot: 0}];
  ch.state = 'broken';
  ch.broke++;
}
function chamberStep(ch, dtRaw, slow) {
  if (dtRaw > PHET.DT_CEILING) return false;     /* PhET discards a long frame whole */
  const dt = slow ? dtRaw * PHET.SLOW_FACTOR : dtRaw;
  ch.t += dt;
  ch.liveTime += dt;
  if (ch.state !== 'idle' && ch.state !== 'broken') ch.busyTime += dt;
  /* photons: query, then move (PhET's order) */
  const keep = [];
  for (const p of ch.photons) {
    if (chamberQuery(ch, p)) continue;           /* absorbed: the photon is gone */
    p.x += p.vx * dt; p.y += p.vy * dt;
    if (p.x < 2200 && p.x > PHET.EMITTER_X - 200 && Math.abs(p.y) < 1400) keep.push(p);
  }
  ch.photons = keep;
  /* the emission timer */
  if (ch.emitTimer !== Infinity) {
    ch.emitTimer -= dt;
    if (ch.emitTimer <= 0) { chamberFire(ch, Math.abs(ch.emitTimer)); ch.emitTimer = PHET.EMIT_PERIOD; }
  }
  /* the molecule */
  if (ch.hyst > 0) ch.hyst -= dt;
  if (ch.state === 'break') chamberBreak(ch);
  else if (ch.state === 'broken') {
    for (const f of ch.frags) { f.x += f.vx * dt; f.y += f.vy * dt; f.rot += dt * 2; }
  } else if (ch.state !== 'idle') {
    if (ch.state === 'vib') ch.vibPhase += PHET.VIB_HZ * dt * 2 * Math.PI;
    if (ch.state === 'rot') ch.rot = (ch.rot + PHET.ROT_HZ * dt * 2 * Math.PI * ch.rotDir) % (2 * Math.PI);
    ch.hold -= dt;
    if (ch.hold <= 0) {
      /* re-emission: the same wavelength, a direction uniform on the circle */
      const a = ch.rng() * 2 * Math.PI;
      /* an ORDINARY photon, at the molecule's own position: nothing marks it
         to pass through, and the only thing that stops the molecule swallowing
         it again on the very next frame is the hysteresis set below -- which
         is exactly how PhET does it */
      ch.photons.push({x: 0, y: 0, vx: PHET.PHOTON_SPEED * Math.cos(a),
                       vy: PHET.PHOTON_SPEED * Math.sin(a), band: ch.band, pass: false});
      ch.reemitted++;
      ch.state = 'idle'; ch.vibPhase = 0; ch.hyst = PHET.HYSTERESIS;
      ch.lastEvent = 'emit';
    }
  }
  return true;
}
/* the long-run statistics, run without any drawing: N photons fired one at a
   time at a molecule that is always free, which isolates the 1/2 */
function ensembleAbsorb(seed, n, p) {
  const rng = mulberry32(seed);
  let k = 0;
  for (let i = 0; i < n; i++) if (rng() < p) k++;
  return k;
}
function ensembleHold(seed, n) {
  const rng = mulberry32(seed);
  let s = 0, s2 = 0;
  for (let i = 0; i < n; i++) {
    const h = PHET.HOLD_MIN + rng() * (PHET.HOLD_MAX - PHET.HOLD_MIN);
    s += h; s2 += h * h;
  }
  return {mean: s / n, sd: Math.sqrt(s2 / n - (s / n) * (s / n))};
}
function ensembleDirection(seed, n, nbin) {
  const rng = mulberry32(seed);
  const bins = new Array(nbin || 12).fill(0);
  let c = 0, s = 0;
  for (let i = 0; i < n; i++) {
    const a = rng() * 2 * Math.PI;
    c += Math.cos(a); s += Math.sin(a);
    bins[Math.min(bins.length - 1, Math.floor(a / (2 * Math.PI) * bins.length))]++;
  }
  const e = n / bins.length;
  let chi2 = 0;
  for (const b of bins) chi2 += (b - e) * (b - e) / e;
  return {cos: c / n, sin: s / n, bins, chi2};
}
/* the duty cycle a renewal argument predicts for the continuous source */
function dutyCycle() {
  const busy = 0.5 * (PHET.HOLD_MIN + PHET.HOLD_MAX) + PHET.HYSTERESIS;
  /* assume the phase of the periodic source decorrelates from the busy
     period: the wait to the next photon is then U(0, T), mean T/2, and a
     further (1/p - 1) whole periods go to failed trials.  It does NOT
     decorrelate -- the measured duty is 6 % higher -- and the file says so. */
  const wait = PHET.EMIT_PERIOD / 2 + (1 / PHET.P_ABSORB - 1) * PHET.EMIT_PERIOD;
  const cycle = wait + busy;
  return {busy, wait, cycle, duty: 0.5 * (PHET.HOLD_MIN + PHET.HOLD_MAX) / cycle, rate: 1 / cycle};
}

/* ---- 6. Planck ---- */
/* spectral radiance per unit wavenumber, W m-2 sr-1 / cm-1 */
function planckNubar(nubar_cm, T) {
  const nu = nubar_cm * C_CM;
  const x = PLANCK_H * nu / (BOLTZ_K * T);
  if (!(x > 0) || x > 700) return 0;
  return 2 * PLANCK_H * nu * nu * nu / (LIGHT_C * LIGHT_C) / (Math.expm1(x)) * C_CM;
}
/* the peak of B_nubar: x = hc nubar/kT solves 3(1 - e^-x) = x */
function wienXWavenumber() {
  let lo = 1, hi = 6;
  const g = x => 3 * (1 - Math.exp(-x)) - x;
  for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (g(lo) * g(m) <= 0) hi = m; else lo = m; }
  return (lo + hi) / 2;
}
function planckPeakCm(T) { return wienXWavenumber() * BOLTZ_K * T / (PLANCK_H * C_CM); }
/* pi * int B dnubar over [lo, hi], by the trapezium rule on n panels */
function planckBand(lo, hi, T, n) {
  n = n || 4000;
  const h = (hi - lo) / n;
  let s = 0.5 * (planckNubar(lo, T) + planckNubar(hi, T));
  for (let i = 1; i < n; i++) s += planckNubar(lo + i * h, T);
  return Math.PI * s * h;
}
