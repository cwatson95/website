
/* ================================================================== *
 *  views C-F: what responds, the normal modes, the statistics,        *
 *  the atmosphere -- then the dispatch and the scene                  *
 * ================================================================== */

/* ---------------------------------------------------------------- *
 *  C. what responds -- PhET's table beside the real one              *
 * ---------------------------------------------------------------- */
/* The real answer for one molecule at one of PhET's four wavelengths.
   Everything but the visible column is computed from the tables in this
   file; the two visible entries are QUOTED and marked so on the canvas. */
const VISIBLE_ABSORBERS = {
  NO2: ['absorbs, 400-650 nm', 'QUOTED: NO₂ is brown because it absorbs right across the visible'],
  O3: ['absorbs weakly', 'QUOTED: the Chappuis band; PhET’s own model notes say O₃ absorbs weakly in the visible'],
};
function realCell(mol, band) {
  const R = realAnswer(mol, band);
  if (band === 'microwave') {
    if (!R.rot) return {txt: 'no dipole: no rotational spectrum at all', kind: '', ok: true};
    return {txt: 'has a rotational spectrum, but not at 1.5 GHz', kind: 'rotate', ok: false,
            note: 'the lowest lines are 22.2 GHz (H₂O) and 115.3 GHz (CO)'};
  }
  if (band === 'infrared') {
    if (!R.irActive) return {txt: 'no infrared-active mode', kind: '', ok: true};
    const b0 = Math.min.apply(null, R.bands), b1 = Math.max.apply(null, R.bands);
    return {txt: R.nActive + ' IR-active mode' + (R.nActive > 1 ? 's' : '') + ', at '
            + (b1 - b0 < 0.5 ? fmt(b0, 0) : fmt(b0, 0) + '–' + fmt(b1, 0)) + ' cm⁻¹',
            kind: 'vibrate', ok: false,
            note: 'PhET’s 850 nm photon is 11765 cm⁻¹, ' + fmt(11764.7 / Math.max.apply(null, R.bands), 1)
                  + '× the highest of them'};
  }
  if (band === 'visible') {
    const q = VISIBLE_ABSORBERS[mol];
    if (q) return {txt: q[0], kind: 'glow', ok: mol === 'NO2', quoted: q[1]};
    return {txt: 'transparent', kind: '', ok: true};
  }
  return {txt: 'dissociates: 12.40 eV is above its ' + fmt(D0_EV[mol], 2) + ' eV bond',
          kind: 'break', ok: PHET_TABLE[mol].ultraviolet === 'break',
          note: 'by a factor of ' + fmt(12.39841984332 / D0_EV[mol], 1) + ', so the fragments leave with '
                + fmt(12.39841984332 - D0_EV[mol], 1) + ' eV of kinetic and internal energy between them'};
}
function gridCell(ctx, W, H, x, y, w, h, txt, col, on) {
  ctx.fillStyle = rgba(col, on ? 0.34 : 0.16);
  ctx.fillRect(x, y, w, h);
  ctx.strokeStyle = on ? COL.live : rgba(col, 0.55);
  ctx.lineWidth = on ? 1.8 : 1;
  ctx.strokeRect(Math.round(x) + 0.5, Math.round(y) + 0.5, Math.round(w), Math.round(h));
  const ls = wrapText(ctx, txt, w - 8, SMALL);
  ctx.fillStyle = shade(col, 1);
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < Math.min(ls.length, Math.floor((h - 4) / 12)); i++)
    ctx.fillText(ls[i], x + w / 2, y + h / 2 + (i - (Math.min(ls.length, Math.floor((h - 4) / 12)) - 1) / 2) * 12);
}
function drawGrid(ctx, W, H, b, title, cellFn) {
  const cols = BANDS, rows = MOLORDER;
  const lw = 46, hh = 22;
  const cw = (b.w - lw) / cols.length, ch = (b.h - hh) / rows.length;
  lab(ctx, W, H, b.x, b.y - 9, title, COL.text, TITLE_FONT, 'left', 'bottom');
  for (let c = 0; c < cols.length; c++)
    lab(ctx, W, H, b.x + lw + cw * (c + 0.5), b.y + hh - 4, BANDNAME[cols[c]],
        shade(BANDCOL[cols[c]], 1), SMALL, 'center', 'bottom');
  for (let r = 0; r < rows.length; r++) {
    lab(ctx, W, H, b.x + lw - 5, b.y + hh + ch * (r + 0.5), rows[r],
        rows[r] === ST.mol ? COL.live : COL.dim, SMALL, 'right', 'middle');
    for (let c = 0; c < cols.length; c++) {
      const cell = cellFn(rows[r], cols[c]);
      gridCell(ctx, W, H, b.x + lw + cw * c + 1, b.y + hh + ch * r + 1, cw - 2, ch - 2,
               cell.txt, RESPCOL[cell.kind] !== undefined ? RESPCOL[cell.kind] : COL.dim,
               rows[r] === ST.mol && cols[c] === ST.band);
    }
  }
}
function drawTable(ctx, W, H, M) {
  const nDis = MOLORDER.reduce((s, m) => s + BANDS.reduce(
    (t, b2) => t + ((PHET_TABLE[m][b2] !== '') !== (realCell(m, b2).kind !== '') ? 1 : 0), 0), 0);
  const capFull = 'Left: PhET&rsquo;s table exactly as its code registers it &mdash; eight molecules, four bands, '
    + 'thirteen responses. Right: what really happens to a photon of that wavelength, computed from the dipole '
    + 'moment and the mode shapes in this file, except the two visible cells, which are quoted. The two tables '
    + 'disagree in ' + nDis + ' of the 32 cells, and every disagreement has the same cause: PhET&rsquo;s four '
    + 'photons stand for their bands rather than sitting on any real line.';
  const capShort = 'PhET&rsquo;s response table beside the real one; ' + nDis + ' of 32 cells disagree.';
  const L = stage(ctx, W, H, capFull, capShort, 1, 0.24, 1);
  const b = L.main;
  const gap = 34;
  if (L.narrow) {
    const hh = (b.h - gap) / 2;
    drawGrid(ctx, W, H, box(b.x, b.y + 14, b.w, hh - 14), 'PhET’s table', (m, bd) =>
      ({txt: RESPNAME[PHET_TABLE[m][bd]], kind: PHET_TABLE[m][bd]}));
    drawGrid(ctx, W, H, box(b.x, b.y + hh + gap, b.w, hh - 14), 'the real molecule', realCell);
  } else {
    const gw = (b.w - gap) / 2;
    drawGrid(ctx, W, H, box(b.x, b.y + 14, gw, b.h - 14), 'PhET’s table, read from its code', (m, bd) =>
      ({txt: RESPNAME[PHET_TABLE[m][bd]], kind: PHET_TABLE[m][bd]}));
    drawGrid(ctx, W, H, box(b.x + gw + gap, b.y + 14, gw, b.h - 14),
             'the real molecule, at PhET’s four wavelengths', realCell);
  }
  if (L.bottom.length) {
    const s = L.bottom[0];
    frame(ctx, s, COL.edge);
    const R = M.real, cell = realCell(M.mol, M.band);
    const txt = [
      MOLNAME[M.mol] + ' at ' + BANDNAME[M.band] + ': PhET says it ' + RESPNAME[M.resp] + '.',
      'Really: ' + cell.txt + (cell.note ? ' — ' + cell.note : '') + (cell.quoted ? ' [' + cell.quoted + ']' : ''),
      'Where PhET gets it exactly right: its microwave column is the permanent-dipole column '
      + '(CO, H₂O, NO₂, O₃ — the four with μ ≠ 0), and its infrared column is the '
      + 'infrared-active column (all but N₂ and O₂, which have no dipole to change).',
      'Where it does not: at 100 nm every one of these molecules dissociates, including the two PhET leaves '
      + 'transparent; and ozone really does absorb visible light, which PhET’s own model notes say.'];
    let y = s.y + 8;
    for (let i = 0; i < txt.length; i++) {
      const nl = wrapText(ctx, txt[i], s.w - 20, SMALL).length;
      if (y + nl * 14 > s.y1 - 4) break;          /* draw what fits, never past the box */
      y += caption(ctx, s.x + 10, y, txt[i], s.w - 20,
                   i === 2 ? COL.pos : (i === 3 ? COL.ref : COL.text), SMALL) + 2;
    }
  }
  drawCaption(ctx, L);
}

/* ---------------------------------------------------------------- *
 *  D. the normal modes                                               *
 * ---------------------------------------------------------------- */
function modeGeom(mol) {
  return memo('mg' + mol, mol, () => geomXY(mol));
}
function drawModes(ctx, W, H, M) {
  const m = M.mode, g = modeGeom(M.mol);
  const exactTxt = MOLSHAPE[M.mol] === 'diatomic'
    ? 'the one mode&rsquo;s shape is (1, &minus;m&#8321;/m&#8322;) exactly, from momentum alone'
    : M.mol === 'CO2'
      ? 'all three shapes are exact: (1, 0, &minus;1) for the symmetric stretch, with the carbon at rest, and '
        + '(1, &minus;2m<sub>O</sub>/m<sub>C</sub>, 1) for the other two'
      : MOLSHAPE[M.mol] === 'bent'
        ? 'the B&#8322; antisymmetric stretch is exact (cot(&theta;/2) from zero angular momentum); the two A&#8321; '
          + 'shapes need a force field and are model'
        : 'the shapes come from the fitted field and are model; the degeneracies (1, 2, 3, 3) are not';
  const capFull = 'The vibrations, diagonalised here from a valence force field fitted to the measured wavenumbers, '
    + 'and animated at their true displacement ratios. For ' + M.mol + ', ' + plain(exactTxt) + '. A mode absorbs '
    + 'infrared only if it changes the dipole moment: the grey ones below change nothing, exactly, and no amount of '
    + 'infrared will excite them.';
  const capShort = 'The normal modes, at their true displacement ratios; grey = no dipole change, so no infrared.';
  const L = stage(ctx, W, H, capFull, capShort, 2, 0.34, 1);
  const b = L.main;
  frame(ctx, b, COL.edge);
  /* the molecule gets the box BELOW the two header lines and ABOVE the
     footnote: a 560-px stage put an atom label inside the header otherwise */
  const hdr = b.h > 200 ? 46 : 26, ftr = b.h > 200 ? 16 : 2;
  const bb = box(b.x, b.y + hdr, b.w, Math.max(40, b.h - hdr - ftr));
  /* The molecules are built in the x-y plane, and the house camera is z-up,
     so a face-on view would need phi = pi/2, where its `right` vector is
     degenerate.  Map the molecular plane onto the WORLD x-z plane instead
     (x, y, z)_mol -> (x, z, y)_world; then phi = 0 looks straight at it and
     a drag still orbits normally.  (Known-bad: a default camera pointed
     along the thing the view exists to show.) */
  const w3 = p => [p[0], p[2], p[1]];
  let R = 0;
  for (const p of g.X) R = Math.max(R, Math.hypot(p[0], p[1], p[2]));
  R = Math.max(R, 0.45);
  /* frame the molecule to a fixed fraction of the box: the projected
     half-width of a point at radius R is f R / dist, so dist follows from
     the fraction wanted.  A divisor tuned at one canvas size scales wrongly
     at another (Known-bad, bloch_sphere). */
  const want = 0.30 * Math.min(bb.w, bb.h) * clamp(ST.zoom, 0.4, 3);
  const fpx0 = (bb.h / 2) / Math.tan(0.78 / 2);
  const dist = Math.max(1.6 * R, fpx0 * R / want);
  const C = boxCamera(bb, ST.camTheta, ST.camPhi, dist, [0, 0, 0]);
  const amp = 0.30 * Math.sin(M.phase);
  const pts = g.X.map((p, i) => [p[0] + m.d[i][0] * amp, p[1] + m.d[i][1] * amp, p[2] + m.d[i][2] * amp]);
  const bl = bondsOf(M.mol);
  for (const [i, j] of bl)
    seg3(ctx, C, w3(pts[i]), w3(pts[j]), COL.bond, Math.max(1.5, 0.05 * Math.min(bb.w, bb.h)), null, true);
  /* atoms back to front */
  const order = pts.map((p, i) => i).sort((a, c) => {
    const qa = C.P(w3(pts[a])), qc = C.P(w3(pts[c]));
    return (qc ? qc.z : 0) - (qa ? qa.z : 0);
  });
  const fpx = C.B.f;
  const arrows = [];
  for (const i of order) {
    const q = C.P(w3(pts[i]));
    if (!q) continue;
    const el = g.sym[i];
    /* ATOM_R is a fraction of ONE drawn bond, so the world radius is that
       fraction times this molecule's bond length -- not a bare constant */
    /* 0.78 of the CPK radius, so an INWARD-pointing eigenvector arrow still
       clears the sphere it starts in (at some phases every arrow points in) */
    const rr = Math.max(3, 0.78 * ATOM_R[el] * GEOM[M.mol].r * fpx / q.z);
    dot(ctx, q.x, q.y, rr, shade(ELCOL[el], 0.86), shade(ELCOL[el], 1), 1.3);
    if (rr > 9) {
      ctx.fillStyle = '#0b0e16';
      ctx.font = 'bold ' + Math.round(Math.min(16, rr * 0.9)) + 'px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(el, q.x, q.y);
    }
    /* the displacement arrow: the eigenvector itself, from the atom's CURRENT
       position, drawn after every sphere so it is not buried in one */
    const L2 = 0.34 * GEOM[M.mol].r;
    const tip = [pts[i][0] + m.d[i][0] * L2, pts[i][1] + m.d[i][1] * L2, pts[i][2] + m.d[i][2] * L2];
    const q1 = C.P(w3(tip));
    if (q1 && Math.hypot(q1.x - q.x, q1.y - q.y) > 4) arrows.push([q, q1, rr]);
  }
  for (const [q0, q1, rr] of arrows) {
    if (q1.x < bb.x || q1.x > bb.x1 || q1.y < bb.y || q1.y > bb.y1) continue;
    const a = Math.atan2(q1.y - q0.y, q1.x - q0.x);
    const sx = q0.x + Math.cos(a) * rr * 0.85, sy = q0.y + Math.sin(a) * rr * 0.85;
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.lineTo(q1.x, q1.y);
    ctx.strokeStyle = m.active ? COL.pos : COL.off;
    ctx.lineWidth = 2.2;
    ctx.stroke();
    const hl = 9;
    ctx.beginPath();
    ctx.moveTo(q1.x, q1.y);
    ctx.lineTo(q1.x - hl * Math.cos(a - 0.4), q1.y - hl * Math.sin(a - 0.4));
    ctx.lineTo(q1.x - hl * Math.cos(a + 0.4), q1.y - hl * Math.sin(a + 0.4));
    ctx.closePath();
    ctx.fillStyle = m.active ? COL.pos : COL.off;
    ctx.fill();
  }
  lab(ctx, W, H, b.x + 10, b.y + 8, MOLNAME[M.mol] + ' · ' + fmt(m.nu, 0) + ' cm⁻¹ · '
      + sigf(m.um, 3) + ' µm · ' + m.sym + (m.mult > 1 ? ' (×' + m.mult + ')' : ''),
      COL.text, TITLE_FONT, 'left', 'top');
  lab(ctx, W, H, b.x + 10, b.y + 26, m.active
      ? 'infrared-active: the dipole moves, |∂μ/∂Q| = ' + sigf(m.dmu, 3)
      : 'infrared-INACTIVE: ∂μ/∂Q is exactly zero, whatever the charges are',
      m.active ? COL.pos : COL.off, SMALL, 'left', 'top');
  if (b.h > 200) lab(ctx, W, H, b.x1 - 10, b.y1 - 6,
      b.w > 620 ? 'arrows are the eigenvector; the atoms swing at ±' + fmt(0.30, 2)
                  + ' Å of it, exaggerated — a real amplitude is under 0.1 Å'
                : 'arrows are the eigenvector; swing exaggerated ×4',
      COL.dim, SMALL, 'right', 'bottom');
  /* bottom 1: this molecule's fundamentals on a wavenumber axis */
  if (L.bottom.length >= 1) {
    const s = L.bottom[0];
    const nus = M.modes.map(o => o.nu);
    const hi = Math.max(4000, Math.max.apply(null, nus) * 1.12);
    axesR(ctx, s, 0, hi, 0, 1, {title: titleFor(s, 'the measured fundamentals of ' + M.mol, M.mol + ' fundamentals'),
                                xlab: 'wavenumber (cm⁻¹)', ny: 2, yfmt: () => ''});
    const seen = [];
    for (const o of M.modes) {
      if (seen.some(v => Math.abs(v - o.nu) < 0.5)) continue;
      seen.push(o.nu);
      const x = s.x + s.w * o.nu / hi;
      ctx.strokeStyle = o.active ? COL.pos : COL.off;
      ctx.lineWidth = o === m ? 3 : 1.8;
      ctx.beginPath();
      ctx.moveTo(x, s.y + 18);
      ctx.lineTo(x, s.y1 - 6);
      ctx.stroke();
      lab(ctx, W, H, x, s.y + 3, plain(o.sym),
          o === m ? COL.live : (o.active ? COL.pos : COL.off), SMALL, 'center', 'top');
    }
    const px = s.x + s.w * PHOTON.infrared.nubar / hi;
    if (px <= s.x1) {
      ctx.strokeStyle = COL.ref;
      ctx.lineWidth = 2;
      ctx.setLineDash([5, 3]);
      ctx.beginPath();
      ctx.moveTo(px, s.y);
      ctx.lineTo(px, s.y1);
      ctx.stroke();
      ctx.setLineDash([]);
    } else {
      lab(ctx, W, H, s.x1, s.y - 9,
          s.w > 380 ? 'PhET’s infrared photon is off this axis, at 11765 cm⁻¹'
                    : 'PhET’s photon: 11765 cm⁻¹, off this axis',
          COL.ref, SMALL, 'right', 'bottom');
    }
  }
  /* bottom 2: what symmetry fixes, against the numerical eigenvector */
  if (L.bottom.length >= 2) {
    const s = L.bottom[1];
    frame(ctx, s, COL.edge);
    lab(ctx, W, H, s.x, s.y - 9, titleFor(s, 'the shape symmetry fixes, against the eigenvector', 'exact vs computed'),
        COL.text, TITLE_FONT, 'left', 'bottom');
    const rows = exactRows(M.mol);
    let y = s.y + 8;
    for (const [a, c] of rows) {
      const nl = wrapText(ctx, a + '  ' + c, s.w - 20, SMALL).length;
      if (y + nl * 14 > s.y1 - 4) break;      /* draw what fits, never past the box */
      y += caption(ctx, s.x + 10, y, a + '  ' + c, s.w - 20, COL.text, SMALL) + 2;
    }
  }
  drawCaption(ctx, L);
}
/* the exact statements this file can make about the current molecule's mode
   shapes, each with the numerical eigenvector's value beside it */
function exactRows(mol) {
  const T = modeTable(mol), out = [];
  if (MOLSHAPE[mol] === 'diatomic') {
    const g = geomXY(mol);
    const r = -MASS[g.sym[0]] / MASS[g.sym[1]];
    out.push(['d₂/d₁ = −m₁/m₂ =', fmt(r, 6) + '  (exact, from zero momentum)']);
    out.push(['force constant k =', fmt(diatomicK(mol), 2) + ' N/m, from the measured ' + VIB[mol][0][0] + ' cm⁻¹']);
    return out;
  }
  if (mol === 'CO2') {
    const ex = 2 * MASS.O / MASS.C;
    const symM = T.filter(o => Math.abs(o.d[1][0]) < 1e-7 && Math.abs(o.d[0][0]) > 0.5)[0];
    const asy = T.filter(o => Math.abs(o.d[1][0]) > 0.1)[0];
    const bnd = T.filter(o => Math.abs(o.d[0][1]) > 0.1)[0];
    out.push(['symmetric stretch: the carbon moves', fmt(Math.abs(symM.d[1][0]), 1) + ' — exactly zero, by symmetry']);
    out.push(['antisymmetric stretch ratio', fmt(asy.d[1][0] / asy.d[0][0], 6)
              + '  vs exact −2m_O/m_C = ' + fmt(-ex, 6)]);
    out.push(['bend ratio', fmt(bnd.d[1][1] / bnd.d[0][1], 6) + '  vs the same exact ' + fmt(-ex, 6)]);
    out.push(['PhET draws the bend at ratio', fmt(40 / CO2_SB, 4) + ' — which is what its oxygen mass of '
              + PHET_ATOM.O.m + ' (carbon’s) gives']);
    return out;
  }
  if (MOLSHAPE[mol] === 'bent') {
    const ex = bentB2Exact(mol);
    const got = T.filter(o => Math.abs(o.d[1][1]) < 1e-7 && Math.abs(o.d[1][0]) > 1e-3)[0];
    let err = 0;
    if (got) {
      const sg = Math.sign(got.d[0][0]);
      for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++) err = Math.max(err, Math.abs(sg * got.d[i][k] - ex[i][k]));
    }
    out.push(['B₂ antisymmetric stretch: v/u = cot(θ/2) =',
              fmt(1 / Math.tan(GEOM[mol].ang * Math.PI / 360), 9) + '  (exact, from zero angular momentum)']);
    out.push(['the computed eigenvector differs by', err.toExponential(2) + '  — machine precision']);
    out.push(['the two A₁ shapes', 'need a force field; the fit sets the stretch-bend constant to the smallest '
              + 'value that reproduces all three measured wavenumbers, and the shapes are MODEL']);
    return out;
  }
  out.push(['degeneracies, in descending wavenumber', T.filter((o, i) => i === 0 || Math.abs(T[i - 1].nu - o.nu) > 0.5)
            .map(o => o.mult).join(', ') + '  — which are the symmetry species T₂, A₁, E, T₂']);
  out.push(['A₁ and E change no dipole:', 'the four bond vectors of a tetrahedron sum to zero and stay summed to '
            + 'zero under both, so |∂μ/∂Q| is exactly 0']);
  out.push(['the shapes themselves', 'come from the fitted field and are MODEL']);
  return out;
}

/* ---------------------------------------------------------------- *
 *  E. the statistics                                                 *
 * ---------------------------------------------------------------- */
function drawStats(ctx, W, H, M) {
  const t = M.stat;
  const capFull = 'PhET&rsquo;s absorption is not a rule, it is three coin flips: every photon that reaches a free '
    + 'molecule is absorbed with probability exactly one half, the molecule then holds it for a time uniform on '
    + '1.1&ndash;1.3 s, and re-emits it in a direction uniform on the circle. Those three claims are measured here '
    + 'over ' + t.n + ' draws of a seeded generator, against the standard error each of them is entitled to &mdash; '
    + 'not against a tolerance chosen to pass. The orange trace is a generator deliberately biased to 0.52, which '
    + 'the same test rejects.';
  const capShort = 'PhET&rsquo;s three random rules, measured against their own standard errors.';
  const L = stage(ctx, W, H, capFull, capShort, 2, 0.36, 1);
  const b = L.main;
  const lo = Math.max(10, t.xs[0]), hi = t.n;
  axesR(ctx, b, Math.log10(lo), Math.log10(hi), 0.4, 0.6,
        {title: titleFor(b, 'the absorbed fraction, as the sample grows', 'absorbed fraction'),
         xlab: 'photons tried', ylab: 'absorbed fraction',
         xticks: logTicks(lo, hi).map(v => Math.log10(v)),
         xfmt: v => sigf(Math.pow(10, v), 2), ny: 5});
  const lx = t.xs.map(v => Math.log10(v));
  polyline(ctx, b, lx, t.lo, Math.log10(lo), Math.log10(hi), 0.4, 0.6, rgba(COL.struct, 0.8), 1, [4, 3]);
  polyline(ctx, b, lx, t.hi, Math.log10(lo), Math.log10(hi), 0.4, 0.6, rgba(COL.struct, 0.8), 1, [4, 3]);
  polyline(ctx, b, [Math.log10(lo), Math.log10(hi)], [0.5, 0.5], Math.log10(lo), Math.log10(hi), 0.4, 0.6, COL.ref, 1.4);
  polyline(ctx, b, lx, t.ys, Math.log10(lo), Math.log10(hi), 0.4, 0.6, COL.pos, 1.8);
  /* the biased generator, for contrast */
  const rngB = mulberry32(ST.statSeed);
  const bx = [], by = [];
  let acc = 0;
  const step = Math.max(1, Math.floor(t.n / 400));
  for (let i = 1; i <= t.n; i++) {
    if (rngB() < 0.52) acc++;
    if (i % step === 0 || i === t.n) { bx.push(Math.log10(i)); by.push(acc / i); }
  }
  polyline(ctx, b, bx, by, Math.log10(lo), Math.log10(hi), 0.4, 0.6, COL.ref, 1.4, [6, 3]);
  marker(ctx, b, Math.log10(lo), Math.log10(hi), 0.4, 0.6, Math.log10(t.n), t.f, COL.live);
  legendAuto(ctx, b, [[COL.pos, 'the sim’s generator'], [COL.ref, 'p = 0.52, deliberately biased'],
                      [COL.struct, '±2σ of a fair coin']]);
  lab(ctx, W, H, b.x + 8, b.y1 - 8,
      b.w > 620
        ? 'measured ' + fmt(t.f, 5) + ' over ' + t.n + ', a 4σ band of ±' + sigf(4 * t.seP, 3)
          + ' — ' + (t.pass ? 'inside' : 'OUTSIDE') + '; the biased one reads ' + fmt(t.bias, 5)
          + ' and is ' + (t.biasCaught ? 'rejected' : 'NOT rejected')
        : fmt(t.f, 5) + ' ± ' + sigf(4 * t.seP, 2) + (t.pass ? ' inside' : ' OUTSIDE'),
      t.pass && t.biasCaught ? COL.pos : COL.ref, SMALL, 'left', 'bottom');
  /* bottom 1: the hold-time histogram */
  if (L.bottom.length >= 1) {
    const s = L.bottom[0];
    const nb = 20, bins = new Array(nb).fill(0);
    const rng = mulberry32(ST.statSeed + 1);
    for (let i = 0; i < t.n; i++) {
      const hv = PHET.HOLD_MIN + rng() * (PHET.HOLD_MAX - PHET.HOLD_MIN);
      bins[Math.min(nb - 1, Math.floor((hv - PHET.HOLD_MIN) / (PHET.HOLD_MAX - PHET.HOLD_MIN) * nb))]++;
    }
    const exp = t.n / nb, top = Math.max(exp * 1.4, Math.max.apply(null, bins) * 1.12);
    axesR(ctx, s, PHET.HOLD_MIN, PHET.HOLD_MAX, 0, top,
          {title: titleFor(s, 'how long the molecule holds the photon', 'hold time'),
           xlab: 'hold time (s)', ny: 3, yfmt: v => sigf(v, 2)});
    for (let i = 0; i < nb; i++) {
      const x0 = s.x + s.w * i / nb, wdt = s.w / nb;
      const hgt = s.h * bins[i] / top;
      ctx.fillStyle = rgba(COL.pos, 0.5);
      ctx.fillRect(x0 + 1, s.y1 - hgt, wdt - 2, hgt);
    }
    polyline(ctx, s, [PHET.HOLD_MIN, PHET.HOLD_MAX], [exp, exp], PHET.HOLD_MIN, PHET.HOLD_MAX, 0, top, COL.ref, 1.6);
    lab(ctx, W, H, s.x + 6, s.y + 6, 'mean ' + fmt(t.hold.mean, 5) + ' s vs 1.2 exactly; s.d. '
        + fmt(t.hold.sd, 5) + ' vs 0.2/√12 = ' + fmt(0.2 / Math.sqrt(12), 5), COL.text, SMALL, 'left', 'top');
  }
  /* bottom 2: the emission-direction rose */
  if (L.bottom.length >= 2) {
    const s = L.bottom[1];
    frame(ctx, s, COL.edge);
    lab(ctx, W, H, s.x, s.y - 9, titleFor(s, 'which way the photon comes back out', 'emission direction'),
        COL.text, TITLE_FONT, 'left', 'bottom');
    const cx = s.x + s.w / 2, cy = s.y + s.h / 2 + 4;
    const R0 = Math.min(s.w, s.h) * 0.30, exp = t.n / t.dir.bins.length;
    let mx = 0;
    for (const v of t.dir.bins) mx = Math.max(mx, v);
    for (let i = 0; i < t.dir.bins.length; i++) {
      const a0 = i / t.dir.bins.length * TAU, a1 = (i + 1) / t.dir.bins.length * TAU;
      const rr = R0 * 0.35 + R0 * 0.65 * t.dir.bins[i] / (mx || 1);
      const N = 8, pts = [[cx, cy]];
      for (let k = 0; k <= N; k++) {
        const a = a0 + (a1 - a0) * k / N;
        pts.push([cx + rr * Math.cos(a), cy - rr * Math.sin(a)]);
      }
      ctx.beginPath();
      ctx.moveTo(pts[0][0], pts[0][1]);
      for (const p of pts) ctx.lineTo(p[0], p[1]);
      ctx.closePath();
      ctx.fillStyle = rgba(COL.pos, 0.45);
      ctx.fill();
      ctx.strokeStyle = rgba(COL.pos, 0.8);
      ctx.lineWidth = 1;
      ctx.stroke();
    }
    /* the uniform circle, in reference orange */
    const ru = R0 * 0.35 + R0 * 0.65 * exp / (mx || 1), N = 64, cp = [];
    for (let k = 0; k <= N; k++) cp.push([cx + ru * Math.cos(k / N * TAU), cy - ru * Math.sin(k / N * TAU)]);
    ctx.beginPath();
    ctx.moveTo(cp[0][0], cp[0][1]);
    for (const p of cp) ctx.lineTo(p[0], p[1]);
    ctx.strokeStyle = COL.ref;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    lab(ctx, W, H, s.x + 6, s.y1 - 6, 'χ² = ' + fmt(t.dir.chi2, 2) + ' on 11 d.f.; the 99.9 % point is 31.26',
        t.dir.chi2 < 31.2641336202 ? COL.pos : COL.ref, SMALL, 'left', 'bottom');
    lab(ctx, W, H, s.x1 - 6, s.y1 - 6, '⟨cos⟩ ' + fmt(t.dir.cos, 4) + '  ⟨sin⟩ ' + fmt(t.dir.sin, 4),
        COL.text, SMALL, 'right', 'bottom');
  }
  drawCaption(ctx, L);
}

/* ---------------------------------------------------------------- *
 *  F. the atmosphere                                                 *
 * ---------------------------------------------------------------- */
const AIRCOL = {CO2: '#e8843a', H2O: '#5ac8e0', CH4: '#b8ec4c', O3: '#cd35c4',
                N2: '#3a4154', O2: '#3a4154'};
function drawAir(ctx, W, H, M) {
  const a = M.air;
  const capFull = 'Earth&rsquo;s surface radiates a Planck spectrum at about ' + fmt(a.T, 0) + ' K, drawn here per unit '
    + 'wavenumber, which is where infrared spectroscopy is done. Every vertical line is a measured infrared-active '
    + 'fundamental of a gas the air carries &mdash; positions only, never strengths, because this file computes no '
    + 'cross-sections. Carbon dioxide&rsquo;s bend sits at 667 cm&#8315;&#185;, almost exactly on the peak. The shaded '
    + 'band is the 8&ndash;13 &micro;m window, ' + fmt(100 * a.wfrac, 1) + ' % of the emission, and it is a window '
    + 'because no strong fundamental of the major gases lands in it.';
  const capShort = 'Earth at ' + fmt(a.T, 0) + ' K, the bands that cover it, and the window that is left.';
  const L = stage(ctx, W, H, capFull, capShort, 1, 0.3, 1);
  const b = L.main;
  const lo = 200, hi = 2600;
  let top = 0;
  for (const v of a.ys) top = Math.max(top, v);
  top *= 1.18;
  axesR(ctx, b, lo, hi, 0, top,
        {title: titleFor(b, 'the 288 K surface, and the bands that absorb it', 'Planck and the bands'),
         xlab: 'wavenumber (cm⁻¹)', ylab: 'B (W m⁻² sr⁻¹ / cm⁻¹)',
         ny: 5, yfmt: v => sigf(v, 2)});
  /* the window */
  if (ST.showWindow) {
    const x0 = b.x + b.w * (1e4 / WINDOW_UM[1] - lo) / (hi - lo);
    const x1 = b.x + b.w * (1e4 / WINDOW_UM[0] - lo) / (hi - lo);
    ctx.fillStyle = rgba(COL.struct, 0.10);
    ctx.fillRect(Math.max(b.x, x0), b.y, Math.min(b.x1, x1) - Math.max(b.x, x0), b.h);
    lab(ctx, W, H, (Math.max(b.x, x0) + Math.min(b.x1, x1)) / 2, b.y + 6,
        'the 8–13 µm window', COL.struct, SMALL, 'center', 'top');
  }
  polyline(ctx, b, a.xs, a.ys, lo, hi, 0, top, COL.pos, 2);
  /* the bands */
  let ai = 0;
  for (const ln of a.lines) {
    if (ln.nu < lo || ln.nu > hi) continue;
    const x = b.x + b.w * (ln.nu - lo) / (hi - lo);
    const c = AIRCOL[ln.mol] || COL.dim;
    ctx.strokeStyle = c;
    ctx.lineWidth = ln.mol === 'CO2' ? 2.2 : 1.5;
    ctx.beginPath();
    ctx.moveTo(x, b.y1);
    ctx.lineTo(x, b.y + b.h * 0.14);
    ctx.stroke();
    lab(ctx, W, H, x, b.y + b.h * 0.14 - 3 - 13 * (ai++ % 2), ln.mol, c, SMALL, 'center', 'bottom');
  }
  const pk = b.x + b.w * (a.peak - lo) / (hi - lo);
  ctx.strokeStyle = COL.ref;
  ctx.lineWidth = 1.3;
  ctx.setLineDash([5, 3]);
  ctx.beginPath();
  ctx.moveTo(pk, b.y);
  ctx.lineTo(pk, b.y1);
  ctx.stroke();
  ctx.setLineDash([]);
  lab(ctx, W, H, pk + 5, b.y + 20, 'peak ' + fmt(a.peak, 0) + ' cm⁻¹ = ' + fmt(a.peakUm, 1) + ' µm',
      COL.ref, SMALL, 'left', 'top');
  lab(ctx, W, H, b.x1 - 6, b.y + 6,
      'π∫B dν̃ = ' + sigf(a.tot, 6) + ' W/m², against σT⁴ = ' + sigf(a.sb, 6),
      COL.dim, SMALL, 'right', 'top');
  { const off = a.lines.filter(l => l.nu > hi).length;
    if (off && b.w > 700) lab(ctx, W, H, b.x1 - 6, b.y + 20,
        off + ' more bands sit off the right of this axis (the O–H and C–H stretches, 3019–3756) '
        + '— far above anything a 288 K surface emits',
        COL.dim, SMALL, 'right', 'top'); }
  /* bottom: the composition */
  if (L.bottom.length) {
    const s = L.bottom[0];
    const roomy = s.h >= 96;
    axesR(ctx, s, -4, 2, 0, 1, {title: titleFor(s, 'what the air is made of, and which of it absorbs infrared',
                                                'air, by volume'),
                                ny: 2, yfmt: () => '',
                                xticks: roomy ? [-4, -3, -2, -1, 0, 1, 2] : [],
                                xfmt: v => sigf(Math.pow(10, v), 2)});
    if (roomy) lab(ctx, W, H, s.x + s.w / 2, s.y1 + 21, 'per cent by volume (log)', '#8b93a6',
                   '11px -apple-system, sans-serif', 'center', 'top');
    const rh = (s.h - 8) / AIR.length;
    for (let i = 0; i < AIR.length; i++) {
      const [nm, pc, why, act2] = AIR[i];
      const x0 = s.x, x1 = s.x + s.w * (Math.log10(pc) + 4) / 6;
      const y = s.y + 4 + rh * i;
      ctx.fillStyle = rgba(act2 ? COL.pos : COL.off, 0.55);
      ctx.fillRect(x0, y + 1, Math.max(2, clamp(x1, s.x, s.x1) - x0), rh - 2);
      const txt = plain(nm) + '  ' + (pc >= 0.01 ? fmt(pc, 3) : sigf(pc, 3)) + ' %'
        + (roomy && s.w > 430 ? '  ·  ' + plain(why) : '');
      lab(ctx, W, H, x0 + 5, y + rh / 2, txt, act2 ? COL.pos : COL.dim, SMALL, 'left', 'middle');
    }
    const inert = AIR.filter(r => !r[3]).reduce((t, r) => t + r[1], 0);
    const actv = AIR.filter(r => r[3]).reduce((t, r) => t + r[1], 0);
    /* the summary goes above the panel only when it clears the main panel's
       own axis title; otherwise the caption already carries the numbers */
    if (s.y - 21 > b.y1 + 34)
      lab(ctx, W, H, s.x1 - 6, s.y - 9, fmt(inert, 3) + ' % absorbs nothing; '
          + fmt(actv, 4) + ' % does all of it', COL.ref, SMALL, 'right', 'bottom');
  }
  drawCaption(ctx, L);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx, W, H, M) {
  LABELS = []; POLY_SEGS = []; LEGEND_RECTS = []; PICKS = [];
  ctx.fillStyle = '#070b18';
  ctx.fillRect(0, 0, W, H);
  const v = M.view;
  if (v === 'chamber') drawChamber(ctx, W, H, M);
  else if (v === 'spectrum') drawSpectrum(ctx, W, H, M);
  else if (v === 'table') drawTable(ctx, W, H, M);
  else if (v === 'modes') drawModes(ctx, W, H, M);
  else if (v === 'stats') drawStats(ctx, W, H, M);
  else drawAir(ctx, W, H, M);
}
/* the helper block already declares DRAG; extend it rather than shadow it */
DRAG.lx = 0; DRAG.ly = 0; DRAG.moved = 0;
function makeScene(canvas) {
  const S = {st: ST, W: 1100, H: 712, onView: null};
  S.model = buildModel;
  S.draw = function () { drawView(canvas.getContext('2d'), S.W, S.H, buildModel()); };
  S.step = function (dt) { return sceneStep(dt); };
  S.resetCam = function () {
    ST.camTheta = DEFAULTS.camTheta; ST.camPhi = DEFAULTS.camPhi; ST.zoom = 1;
  };
  S.wheel = function (dy) {
    if (ST.view !== 'modes') return false;
    ST.zoom = clamp(ST.zoom * (dy > 0 ? 0.93 : 1.075), 0.4, 3);
    return true;
  };
  S.pointer = function (type, x, y) {
    if (type === 'down') {
      DRAG.lx = x; DRAG.ly = y; DRAG.moved = 0;
      DRAG.what = ST.view === 'modes' ? 'orbit' : null;
      return DRAG.what !== null;
    }
    if (type === 'move') {
      if (!DRAG.what) return false;
      const dx = x - DRAG.lx, dy = y - DRAG.ly;
      DRAG.lx = x; DRAG.ly = y;
      DRAG.moved += Math.abs(dx) + Math.abs(dy);
      ST.camTheta -= dx * 0.0075;
      ST.camPhi = clamp(ST.camPhi + dy * 0.006, -1.45, 1.45);
      return true;
    }
    const had = DRAG.what !== null;
    DRAG.what = null;
    return had;
  };
  return S;
}
