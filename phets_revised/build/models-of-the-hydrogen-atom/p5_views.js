
/* ================================================================== *
 *  views 3-6, the view dispatch, and the scene                        *
 * ================================================================== */

/* ------------------------------------------------------------------ *
 *  view 3 — the standing wave (de Broglie)                            *
 * ------------------------------------------------------------------ */
/* the mismatch when nu wavelengths are wrapped round one turn: the wave has to
   match in VALUE and in SLOPE at the seam, and
   sqrt(sin^2(2 pi nu) + (1 - cos 2 pi nu)^2) = 2|sin(pi nu)|  exactly.
   That closed form is what makes the integers the allowed orbits. */
function closureMismatch(nu){ return 2 * Math.abs(Math.sin(PI * nu)); }
function closureMismatchRaw(nu){
  const dv = Math.sin(TAU * nu) - 0;                 /* value at 2 pi minus at 0 */
  const ds = 1 - Math.cos(TAU * nu);                 /* slope, divided by nu     */
  return Math.sqrt(dv * dv + ds * ds);
}
function waveGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, waveCaption(M),
    'The orbit is allowed when a whole number of electron wavelengths fits round it.');
  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  if(narrowStage(W)){
    const f = stackFit(top, bot, 44, 0.46);
    const side2 = Math.min(f.side, uw - 24);
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(56, a2.y1 + 44, uw - 78, f.bh);
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }
  const side = Math.max(140, Math.min(bot - top, uw * 0.52));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 56, top + 10, Math.max(150, uw - side - 80),
                Math.max(100, bot - top - 30 - AXIS_BOT));
  return {L, a, b, side};
}
function waveCaption(M){
  const st = M.st;
  const nInt = clamp(Math.round(st.nu), 1, NMAX);
  return 'The ring is drawn at ' + (st.showExact ? 'the true radius n²a₀' : 'PhET’s compressed radius')
    + ' for n = ' + nInt + ', and the wave on it has ' + fmt(st.nu, 2) + ' wavelengths. Away from a whole number the '
    + 'wave does not meet itself at the seam, marked in orange: that mismatch is 2|sin πν| exactly, and it is '
    + 'zero only at the integers. The radial and 3-D-height pictures exaggerate the amplitude — the wave is a '
    + 'phase, not a displacement — at 0.24 of the ring radius, and the faint outline behind the live wave is the '
    + 'full amplitude it reaches, drawn so the nodes stay visible while it breathes.';
}
function drawWave(ctx, W, H, M){
  const st = M.st, G = waveGeo(ctx, W, H, M), a = G.a;
  drawCaption(ctx, G.L);
  const nInt = clamp(Math.round(st.nu), 1, NMAX);
  const nu = st.nu;
  ctx.fillStyle = '#0a0d16'; ctx.fillRect(a.x, a.y, a.w, a.h);
  frame(ctx, a, '#242a3a');
  panelTitle(ctx, a, 'the electron wave on the orbit');
  const cx = a.x + a.w / 2, cy = a.y + a.h / 2;
  /* the ladder of orbits, so the chosen one has a context */
  /* the panel is fitted to the ring being DRAWN, not to the n = 6 orbit: on
     the true n^2 ladder n = 2 is a ninth of n = 6 and the wave came out 24 px
     across, which is the one thing this view exists to show.  The rest of the
     ladder is drawn at the same scale and simply runs off the panel, which the
     note below says. */
  const rCur = st.showExact ? trueViewRadius(nInt) : viewRadius(nInt);
  const rmaxUnits = st.showExact ? trueViewRadius(NMAX) : viewRadius(NMAX);
  const sc = (a.w * 0.30) / rCur;
  let offPanel = 0;
  for(let n = 1; n <= NMAX; n++){
    const rr = (st.showExact ? trueViewRadius(n) : viewRadius(n)) * sc;
    if(rr > a.w * 0.49){ offPanel++; continue; }
    ring(ctx, cx, cy, rr, n === nInt ? 'rgba(90,200,224,0.55)' : 'rgba(90,200,224,0.16)', 1, [3, 3]);
  }
  const R = rCur * sc;
  disc(ctx, cx, cy, 5, COL.proton);
  /* the wave itself */
  /* a fraction of the RING, not of the n = 1 radius: on the true ladder the
     n = 1 radius is 1/36 of n = 6 and the wave came out 2 px tall */
  const amp = 0.24 * R;
  const ph = ATOM.angle;
  if(st.dbRep === 'bright'){
    const N = Math.max(48, Math.round(PI * 2 * R / 3) + 1), thick = Math.max(3, 0.06 * R);
    for(let k = 0; k < N; k++){
      const a0 = TAU * k / N, a1 = a0 + TAU / N + 0.002;
      const v = Math.sin(nu * a0) * Math.sin(ph);
      ctx.fillStyle = v >= 0 ? mix('#1b2434', COL.electron, clamp(v, 0, 1))
                             : mix('#1b2434', '#070b18', clamp(-v, 0, 1));
      ctx.beginPath();
      ctx.moveTo(cx + (R - thick) * Math.cos(a0), cy - (R - thick) * Math.sin(a0));
      ctx.lineTo(cx + (R + thick) * Math.cos(a0), cy - (R + thick) * Math.sin(a0));
      ctx.lineTo(cx + (R + thick) * Math.cos(a1), cy - (R + thick) * Math.sin(a1));
      ctx.lineTo(cx + (R - thick) * Math.cos(a1), cy - (R - thick) * Math.sin(a1));
      ctx.closePath(); ctx.fill();
    }
    /* the nodes, where sin(nu*theta) = 0: the brightness itself breathes as
       sin(phase) and a still frame can catch it flat, but the node angles are
       fixed and are what makes it a STANDING wave */
    ctx.strokeStyle = 'rgba(207,212,222,0.45)'; ctx.lineWidth = 1;
    for(let k = 0; k * PI / nu < TAU; k++){
      const th = k * PI / nu;
      ctx.beginPath();
      ctx.moveTo(cx + (R + thick + 1) * Math.cos(th), cy - (R + thick + 1) * Math.sin(th));
      ctx.lineTo(cx + (R + thick + 7) * Math.cos(th), cy - (R + thick + 7) * Math.sin(th));
      ctx.stroke();
    }
  } else if(st.dbRep === 'height'){
    const ys = PHET.db3dYScale;
    ctx.strokeStyle = 'rgba(90,200,224,0.35)'; ctx.lineWidth = 1;
    ctx.beginPath();
    for(let k = 0; k <= 160; k++){
      const t = TAU * k / 160, x = cx + R * Math.cos(t), y = cy - ys * R * Math.sin(t);
      if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.closePath(); ctx.stroke();
    ctx.strokeStyle = COL.electron; ctx.lineWidth = 2;
    ctx.beginPath();
    for(let k = 0; k <= 240; k++){
      const t = TAU * k / 240;
      const x = cx + R * Math.cos(t), y = cy - ys * R * Math.sin(t) - amp * Math.sin(nu * t) * Math.sin(ph);
      if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  } else {
    /* the full-amplitude shape, faint, so the nodes are visible at every phase:
       the live wave breathes as sin(phase) and a still frame can catch it flat */
    for(const [fac, col, lw] of [[1, 'rgba(90,200,224,0.28)', 1], [Math.sin(ph), COL.electron, 2]]){
      ctx.strokeStyle = col; ctx.lineWidth = lw;
      ctx.beginPath();
      for(let k = 0; k <= 240; k++){
        const t = TAU * k / 240, rr = R + amp * Math.sin(nu * t) * fac;
        const x = cx + rr * Math.cos(t), y = cy - rr * Math.sin(t);
        if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  }
  /* the seam: where the wave should have come back to itself */
  const d = closureMismatch(nu);
  /* the seam is drawn at FULL amplitude, which is what the printed mismatch
     measures; at the live phase it shrinks to nothing twice a cycle */
  const seamR0 = R;
  const seamR1 = R + amp * Math.sin(TAU * nu);
  if(d > 1e-9 && st.dbRep === 'radial'){
    ctx.strokeStyle = COL.ref; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(cx + seamR0, cy); ctx.lineTo(cx + seamR1, cy); ctx.stroke();
  }
  /* keep the seam label inside the panel: with the ring fitted to the panel it
     reached the neighbouring plot's rotated axis title, which axes() draws
     outside any registry */
  {
    const stxt = d < 1e-9 ? 'closes' : 'mismatch ' + fmt(d, 3);
    ctx.font = '11px -apple-system, sans-serif';
    const sw = ctx.measureText(stxt).width;
    const scol = d < 1e-9 ? COL.pos : COL.ref;
    if(cx + R + 10 + sw <= a.x1 - 6)
      labelIfClear(ctx, cx + R + 10, cy - 8, stxt, scol, '11px -apple-system, sans-serif', 'left', 'bottom');
    else if(cx - R - 10 - sw >= a.x + 6)
      labelIfClear(ctx, cx - R - 10, cy - 8, stxt, scol, '11px -apple-system, sans-serif', 'right', 'bottom');
    else
      /* neither side fits: put it inside the panel's top-left, or drop it */
      labelIfClear(ctx, a.x + 10, a.y + 6, stxt, scol, '11px -apple-system, sans-serif', 'left', 'top');
  }
  /* one WRAPPED note inside the panel: two fixed lines ran past the frame and
     into the neighbouring plot's tick labels as soon as they grew */
  const wnote = (st.showExact ? 'true radius n²a₀ = ' : 'PhET radius = ') + fmt(rCur, 0)
    + ' units at ' + sigf(sc, 3) + ' px/unit; ν = ' + fmt(nu, 2) + ' wavelengths round the ring'
    + (offPanel ? '; ' + offPanel + ' outer orbit' + (offPanel === 1 ? '' : 's') + ' run off the panel' : '');
  const wLines = wrapText(ctx, wnote, a.w - 20, '11px -apple-system, sans-serif');
  /* on a small panel the note wraps to more lines than the panel is tall and
     climbs off the top of the canvas; the readout carries the same numbers */
  if(wLines.length * 14 < a.h * 0.30){
    LABEL_RECTS.push({x: a.x + 10, y: a.y1 - 10 - wLines.length * 14, w: a.w - 20, h: wLines.length * 14});
    ctx.fillStyle = '#767e92'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
    ctx.font = '11px -apple-system, sans-serif';
    for(let i = 0; i < wLines.length; i++)
      ctx.fillText(wLines[i], a.x + 10, a.y1 - 10 - wLines.length * 14 + i * 14);
  }
  /* the closure curve */
  const b = G.b;
  const NU0 = 0.5, NU1 = 7.2;
  const xs = [], ys = [];
  for(let k = 0; k <= 700; k++){ const v = NU0 + (NU1 - NU0) * k / 700; xs.push(v); ys.push(closureMismatch(v)); }
  axes(ctx, b, NU0, NU1, 0, 2.15, {title: 'how badly the wave misses itself, 2|sin πν|',
    xlab: 'ν, wavelengths round the ring', ylab: 'mismatch', nx: 7, ny: nyFor(b.h),
    xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  polyline(ctx, b, xs, ys, NU0, NU1, 0, 2.15, COL.pos, 1.8);
  for(let n = 1; n <= NMAX; n++){
    const X = b.x + b.w * (n - NU0) / (NU1 - NU0);
    ctx.save(); ctx.strokeStyle = 'rgba(90,200,224,0.35)'; ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(X, b.y); ctx.lineTo(X, b.y1); ctx.stroke(); ctx.restore();
    label(ctx, X, b.y + 4, 'n=' + n, '#6f7789', '10px -apple-system, sans-serif', 'center', 'top');
  }
  const Xm = b.x + b.w * (clamp(nu, NU0, NU1) - NU0) / (NU1 - NU0);
  const Ym = b.y1 - b.h * clamp(d, 0, 2.15) / 2.15;
  ctx.strokeStyle = COL.live; ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.moveTo(Xm, b.y1); ctx.lineTo(Xm, Ym); ctx.stroke();
  disc(ctx, Xm, Ym, 4, COL.live);
  legendAuto(ctx, b, [[COL.pos, 'mismatch 2|sin πν|'], [COL.live, 'where you are'],
                      [COL.struct, 'the allowed orbits']]);
}

/* ------------------------------------------------------------------ *
 *  view 4 — the orbitals (Schrodinger)                                *
 * ------------------------------------------------------------------ */
function orbGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, orbCaption(M),
    'The cloud is ∫|ψ|² dy through the orbital: the dark rings and cones are its nodes.');
  const uw = usableW(W);
  const top = L.top + 24, bot = L.bot - 16;
  if(narrowStage(W)){
    const f = stackFit(top, bot, 46, 0.46);
    const side2 = Math.min(f.side, uw - 24);
    const a2 = box(30 + (uw - 24 - side2) / 2, top, side2, side2);
    const b2 = box(64, a2.y1 + 46, uw - 86, f.bh);
    return {L, a: a2, b: b2, side: side2, narrow: true};
  }
  const side = Math.max(140, Math.min(bot - top, uw * 0.50));
  const a = box(30, top + (bot - top - side) / 2, side, side);
  const b = box(a.x1 + 60, top + 14, Math.max(160, uw - side - 86),
                Math.max(100, bot - top - 40 - AXIS_BOT));
  return {L, a, b, side};
}
function orbCaption(M){
  return 'A slice through the orbital in the x–z plane, with the line of sight along y: every pixel is '
    + '∫|ψ|² dy, which is what a camera pointed at one atom would build up. The wavefunction is the '
    + 'analytic one, R(n,l) times Y(l,m), so the dark rings are the ' + M.nodesR + ' radial node'
    + (M.nodesR === 1 ? '' : 's') + ' at n − l − 1 and the dark cones are the ' + M.nodesA
    + ' angular node' + (M.nodesA === 1 ? '' : 's') + ' at l − |m|. The cloud has no φ dependence, because '
    + '|Y| has none: it is a figure of revolution about z. Radii are in Bohr radii, a₀ = 52.9177 pm.';
}
function drawOrbitals(ctx, W, H, M){
  const st = M.st, G = orbGeo(ctx, W, H, M), a = G.a, n = M.on, l = M.ol, m = M.om;
  drawCaption(ctx, G.L);
  const rmax = cloudExtent(n, l);
  const GRID = 92;
  const cg = cloudGrid(n, l, m, GRID, rmax);
  ctx.fillStyle = '#05070c'; ctx.fillRect(a.x, a.y, a.w, a.h);
  const cell = a.w / GRID;
  for(let j = 0; j < GRID; j++) for(let i = 0; i < GRID; i++){
    const v = cg.mx > 0 ? cg.g[j * GRID + i] / cg.mx : 0;
    if(v < 0.003) continue;
    ctx.fillStyle = mix('#05070c', COL.electron, Math.pow(v, 0.42));
    ctx.fillRect(a.x + i * cell - 0.4, a.y1 - (j + 1) * cell - 0.4, cell + 0.8, cell + 0.8);
  }
  frame(ctx, a, '#242a3a');
  panelTitle(ctx, a, 'the ' + n + 'spdfgh'.charAt(l) + ' orbital, m = ' + m
    + ' — ∫|ψ|² dy');
  /* the axes, in a_0 */
  const cx = a.x + a.w / 2, cy = a.y + a.h / 2, sc = a.w / (2 * rmax);
  ctx.save(); ctx.strokeStyle = 'rgba(207,212,222,0.30)'; ctx.lineWidth = 1; ctx.setLineDash([2, 4]);
  ctx.beginPath(); ctx.moveTo(a.x, cy); ctx.lineTo(a.x1, cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx, a.y); ctx.lineTo(cx, a.y1); ctx.stroke(); ctx.restore();
  label(ctx, a.x1 - 6, cy - 4, 'x', '#aeb6c6', 'italic 12px Georgia, serif', 'right', 'bottom');
  label(ctx, cx + 5, a.y + 4, 'z', '#aeb6c6', 'italic 12px Georgia, serif', 'left', 'top');
  /* the radial nodes, as circles of the right radius */
  if(st.showPhet){
    for(const rn of radialNodeRadii(n, l)){
      if(rn * sc < a.w / 2) ring(ctx, cx, cy, rn * sc, 'rgba(232,132,58,0.55)', 1, [3, 3]);
    }
    for(const th of angularNodeAngles(l, m)){
      const dx = Math.sin(th) * a.w / 2, dz = Math.cos(th) * a.w / 2;
      ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.45)'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
      ctx.beginPath(); ctx.moveTo(cx - dx, cy + dz); ctx.lineTo(cx + dx, cy - dz); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(cx - dx, cy - dz); ctx.lineTo(cx + dx, cy + dz); ctx.stroke();
      ctx.restore();
    }
  }
  /* the note is WRAPPED to the panel: a single label ran 382 px across a
     350 px panel and met the neighbouring plot's tick labels */
  const scaleTxt = 'frame ' + fmt(2 * rmax, 0) + ' a₀ (' + sigf(2 * rmax * A0 * 1e12, 3)
    + ' pm) wide — 99 % of |ψ|² is inside it';
  const sLines = wrapText(ctx, scaleTxt, a.w - 16, '10.5px -apple-system, sans-serif');
  /* on a small panel the note would wrap to more lines than the panel is tall
     and climb into its own title; the readout carries the same numbers */
  if(sLines.length * 13 < a.h * 0.32){
    LABEL_RECTS.push({x: a.x + 8, y: a.y1 - 8 - sLines.length * 13, w: a.w - 16, h: sLines.length * 13});
    ctx.fillStyle = '#8d95a8'; ctx.textAlign = 'left'; ctx.textBaseline = 'top';
    ctx.font = '10.5px -apple-system, sans-serif';
    for(let i = 0; i < sLines.length; i++)
      ctx.fillText(sLines[i], a.x + 8, a.y1 - 8 - sLines.length * 13 + i * 13);
  }
  /* the radial distribution */
  const b = G.b;
  const rs = [], ps = [];
  let pmax = 0;
  for(let k = 0; k <= 600; k++){ const r = rmax * 1.15 * k / 600; const p = radialProb(n, l, r);
    rs.push(r); ps.push(p); if(p > pmax) pmax = p; }
  const yhi = pmax * 1.18 || 1;
  axes(ctx, b, 0, rmax * 1.15, 0, yhi, {title: 'the radial distribution, r²R(r)²',
    xlab: 'r / a₀', ylab: 'probability per a₀', nx: 6, ny: nyFor(b.h),
    xfmt: t => fmt(t, 0), yfmt: t => sigf(t, 2)});
  polyline(ctx, b, rs, ps, 0, rmax * 1.15, 0, yhi, COL.pos, 1.8);
  for(const rn of radialNodeRadii(n, l)){
    const X = b.x + b.w * rn / (rmax * 1.15);
    if(X > b.x && X < b.x1){
      ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.6)'; ctx.setLineDash([3, 3]);
      ctx.beginPath(); ctx.moveTo(X, b.y); ctx.lineTo(X, b.y1); ctx.stroke(); ctx.restore();
    }
  }
  const Xm = b.x + b.w * clamp(M.meanR, 0, rmax * 1.15) / (rmax * 1.15);
  ctx.strokeStyle = COL.live; ctx.lineWidth = 1.5;
  ctx.beginPath(); ctx.moveTo(Xm, b.y); ctx.lineTo(Xm, b.y1); ctx.stroke();
  /* the value goes in the legend, not in a floating label beside the rule:
     legendAuto dodges CURVES, not labels (Known-bad), so the two met */
  legendAuto(ctx, b, [[COL.pos, 'r²R²'], [COL.ref, 'radial nodes'],
                      [COL.live, '⟨r⟩ = ' + fmt(M.meanR, 2) + ' a₀']]);
}
/* the radii where R_nl vanishes (n-l-1 of them), by bisection on a fine scan */
function radialNodeRadii(n, l){
  return memo('rnodes', n + ',' + l, () => {
    /* a node that lands EXACTLY on a sample (R_20 vanishes at exactly r = 2 a_0,
       and 2 is a grid point) makes sign(prev) x sign(v) zero, so a strict
       sign-change test loses it — the same shape as the angular-node counter in
       derive.py, which missed every node at cos theta = 0.  Track the last
       NON-ZERO sign and treat an exact zero as a node in its own right. */
    const out = [], rmax = 40 * n * n, N = 20000;
    let lastSign = 0, lastR = 1e-9;
    for(let k = 1; k <= N; k++){
      const r = rmax * k / N, v = Rnl(n, l, r);
      if(v === 0){ out.push(r); lastSign = 0; lastR = r; continue; }
      const sg = v > 0 ? 1 : -1;
      if(lastSign !== 0 && sg !== lastSign){
        let lo = lastR, hi = r;
        for(let it = 0; it < 80; it++){
          const mid = 0.5 * (lo + hi);
          const vm = Rnl(n, l, mid);
          if(vm === 0){ lo = mid; hi = mid; break; }
          if((vm > 0 ? 1 : -1) === lastSign) lo = mid; else hi = mid;
        }
        out.push(0.5 * (lo + hi));
      }
      lastSign = sg; lastR = r;
    }
    return out;
  });
}
/* the polar angles where P_l^|m|(cos theta) vanishes (l - |m| of them) */
function angularNodeAngles(l, m){
  return memo('anodes', l + ',' + m, () => {
    /* sample at the MIDPOINTS, so cos theta = 0 (a node of every odd l - |m|)
       is never hit exactly, plus the same last-non-zero-sign guard */
    const out = [], N = 4000, am = Math.abs(m);
    let lastSign = 0, lastTh = 1e-7;
    for(let k = 1; k <= N; k++){
      const th = PI * (k - 0.5) / N, v = legendreP(l, am, Math.cos(th));
      if(v === 0){ if(th < PI / 2 + 1e-9) out.push(th); lastSign = 0; lastTh = th; continue; }
      const sg = v > 0 ? 1 : -1;
      if(lastSign !== 0 && sg !== lastSign){
        let lo = lastTh, hi = th;
        for(let it = 0; it < 70; it++){
          const mid = 0.5 * (lo + hi);
          const vm = legendreP(l, am, Math.cos(mid));
          if(vm === 0){ lo = mid; hi = mid; break; }
          if((vm > 0 ? 1 : -1) === lastSign) lo = mid; else hi = mid;
        }
        const t = 0.5 * (lo + hi);
        if(t < PI / 2 + 1e-9) out.push(t);
      }
      lastSign = sg; lastTh = th;
    }
    return out;
  });
}

/* ------------------------------------------------------------------ *
 *  view 5 — the series                                                *
 * ------------------------------------------------------------------ */
const SER_MAX_N = 12;
function seriesLines(which){
  const out = [];
  for(let n1 = 1; n1 <= 5; n1++){
    if(which !== 'all' && +which !== n1) continue;
    for(let n2 = n1 + 1; n2 <= SER_MAX_N; n2++) out.push({n1, n2, lam: lamVac(n1, n2)});
  }
  return out;
}
/* the drawn axis is log10(lambda/nm) — one scale for seven octaves, and the
   compression is printed on the canvas */
function serGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, serCaption(M),
    'Every hydrogen line on one logarithmic wavelength axis, in its own colour.');
  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  const f = stackFit(top, bot, 80, 0.50);
  const hA = f.side;
  const a = box(54, top, uw - 70, hA);
  /* 80 px between the panels, not 58: panel a's x-axis title sits 33 px below
     its frame and panel b's own title 24 px above its own, and at 58 they
     overlapped by 3.6 px at every stage size */
  const b = box(64, a.y1 + 80, uw - 80, f.bh);
  return {L, a, b};
}
function serCaption(M){
  return 'Top: every transition of hydrogen up to n = 12, at its exact vacuum wavelength, on a logarithmic axis '
    + '— the axis is compressed, and a decade is a decade, so the Lyman lines really are that tightly packed. '
    + 'Each line is painted in the colour the eye would see (CIE 1931, sRGB); outside 380–780 nm there is no '
    + 'colour to paint, so ultraviolet is grey and infrared is brown. Bottom: how far this model is from what NIST '
    + 'measured, line by line. The residual is one part in 10⁵ and it is the relativistic correction that a '
    + 'non-relativistic Schrödinger atom cannot have — α²/4 = 1.33 × 10⁻⁵ for the '
    + '1s level, drawn as the orange rule.';
}
function drawSeries(ctx, W, H, M){
  const st = M.st, G = serGeo(ctx, W, H, M), a = G.a, b = G.b;
  drawCaption(ctx, G.L);
  const lines = seriesLines(st.series);
  const lo = Math.log10(80), hi = Math.log10(15000);
  ctx.fillStyle = '#0a0d16'; ctx.fillRect(a.x, a.y, a.w, a.h);
  /* the visible band, in true colour, along the bottom of the panel */
  for(let i = 0; i < 90; i++){
    const lam = 380 + (780 - 380) * (i + 0.5) / 90;
    const X = a.x + a.w * (Math.log10(lam) - lo) / (hi - lo);
    const X2 = a.x + a.w * (Math.log10(380 + (780 - 380) * (i + 1.5) / 90) - lo) / (hi - lo);
    ctx.fillStyle = mix('#0a0d16', lamColour(lam), 0.40);
    ctx.fillRect(X, a.y1 - 9, Math.max(1, X2 - X + 0.6), 9);
  }
  frame(ctx, a, '#242a3a');
  panelTitle(ctx, a, 'every line of hydrogen, 1/λ = Rᴴ(1/n₁² − 1/n₂²)');
  /* decade ticks */
  /* thin the decade labels by MEASURED width: at 560 px '5.0 um' and '7.0 um'
     are 14 px apart and overlap (Known-bad: tick label width follows the tick
     spacing, not a fixed decimal count) */
  let lastLabX = -1e9;
  for(let e = 2; e <= 4; e++) for(const mnt of [1, 2, 3, 5, 7]){
    const v = mnt * Math.pow(10, e);
    if(v < 80 || v > 15000) continue;
    const X = a.x + a.w * (Math.log10(v) - lo) / (hi - lo);
    ctx.strokeStyle = 'rgba(30,38,54,1)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X, a.y); ctx.lineTo(X, a.y1); ctx.stroke();
    const txt = v >= 1000 ? fmt(v / 1000, 1) + ' µm' : fmt(v, 0);
    ctx.font = '10px -apple-system, sans-serif';
    const need = ctx.measureText(plain(txt)).width / 2 + 6;
    if(X - need < lastLabX) continue;
    label(ctx, X, a.y1 + 5, txt, '#6f7789', '10px -apple-system, sans-serif', 'center', 'top');
    lastLabX = X + need;
  }
  label(ctx, a.x + a.w / 2, a.y1 + 21, 'wavelength (nm, log scale)', '#8b93a6',
    '11px -apple-system, sans-serif', 'center', 'top');
  /* the marker first: it is mandatory, so the optional limit and transition
     labels have to dodge IT, not the other way round */
  const rowOf = n1 => a.y + 16 + (n1 - 1) * (a.h - 42) / 5;
  if(st.lam >= 80 && st.lam <= 15000){
    const Xm2 = a.x + a.w * (Math.log10(st.lam) - lo) / (hi - lo);
    ctx.strokeStyle = COL.live; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(Xm2, a.y); ctx.lineTo(Xm2, a.y1); ctx.stroke();
    label(ctx, Xm2 + 4, a.y1 - 13, fmt(st.lam, 0) + ' nm', COL.live,
      '10.5px -apple-system, sans-serif', 'left', 'bottom');
  }
  /* the lines */
  for(const t of lines){
    const X = a.x + a.w * (Math.log10(t.lam) - lo) / (hi - lo);
    if(X < a.x || X > a.x1) continue;
    const y0 = rowOf(t.n1), y1 = a.y1 - 10;
    ctx.strokeStyle = lamColour(t.lam); ctx.lineWidth = t.n2 === t.n1 + 1 ? 2 : 1;
    ctx.globalAlpha = t.n2 === t.n1 + 1 ? 1 : 0.55;
    ctx.beginPath(); ctx.moveTo(X, y0); ctx.lineTo(X, y1); ctx.stroke();
    ctx.globalAlpha = 1;
    if(t.n2 <= t.n1 + 2) labelIfClear(ctx, X, y0 - 2, t.n2 + '→' + t.n1, lamColour(t.lam),
      '9.5px -apple-system, sans-serif', 'center', 'bottom');
  }
  /* series limits and names */
  for(let n1 = 1; n1 <= 5; n1++){
    if(st.series !== 'all' && +st.series !== n1) continue;
    const lim = seriesLimit(n1);
    const X = a.x + a.w * (Math.log10(lim) - lo) / (hi - lo);
    ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.6)'; ctx.setLineDash([4, 3]); ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X, rowOf(n1) + 2); ctx.lineTo(X, a.y1 - 10); ctx.stroke(); ctx.restore();
    /* the Lyman limit sits 2.5 % from the left edge of a seven-octave axis, so a
       right-aligned label there runs 90 px off the canvas.  Pick the side that
       has room and drop the label if neither has. */
    const txt = SERIES_NAME[n1] + ', limit ' + fmt(lim, 1) + ' nm';
    ctx.font = '10px -apple-system, sans-serif';
    const tw = ctx.measureText(plain(txt)).width;
    if(X - 5 - tw >= a.x + 2)
      labelIfClear(ctx, X - 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'right', 'top');
    else if(X + 5 + tw <= a.x1 - 2)
      labelIfClear(ctx, X + 5, rowOf(n1) + 5, txt, COL.ref, '10px -apple-system, sans-serif', 'left', 'top');
  }
  /* the residuals against NIST */
  const xs = [], ys = [], cols = [];
  for(const [inten, ang, n1, n2] of NIST_VAC){
    xs.push(Math.log10(ang / 10)); ys.push((lamVac(n1, n2) - ang / 10) / (ang / 10)); cols.push(COL.pos);
  }
  for(const [inten, ang, n1, n2] of NIST_AIR){
    xs.push(Math.log10(ang / 10)); ys.push((lamAir(n1, n2) - ang / 10) / (ang / 10)); cols.push(COL.ref);
  }
  let ymax = 0;
  for(const v of ys) ymax = Math.max(ymax, Math.abs(v));
  const yhi = Math.max(ymax * 1.25, 1.8e-5);
  /* the units go in the axis TITLE, not on every tick: '0.5x10^-5' is 49 px
     wide and ran into the rotated y-axis label at every stage size */
  axes(ctx, b, lo, hi, 0, yhi, {title: 'this model minus NIST, in parts per 100 000',
    xlab: 'wavelength (nm, log scale)',
    /* a rotated title runs DOWN the screen, so a 150 px one on a 46 px panel
       sticks out 50 px past the frame and lands on the caption */
    ylab: b.h < 120 ? '×10⁻⁵' : '(model − NIST)/NIST, ×10⁻⁵',
    nx: 6, ny: nyFor(b.h), xfmt: t => fmt(Math.pow(10, t), 0), yfmt: t => (t * 1e5).toFixed(1)});
  for(let i = 0; i < xs.length; i++){
    const X = b.x + b.w * (xs[i] - lo) / (hi - lo);
    const Y = b.y1 - b.h * clamp(ys[i], 0, yhi) / yhi;
    if(X < b.x || X > b.x1) continue;
    disc(ctx, X, Y, 3.2, cols[i]);
  }
  const Ya = b.y1 - b.h * (ALPHA * ALPHA / 4) / yhi;
  ctx.save(); ctx.strokeStyle = COL.ref; ctx.lineWidth = 1.4; ctx.setLineDash([5, 4]);
  ctx.beginPath(); ctx.moveTo(b.x, Ya); ctx.lineTo(b.x1, Ya); ctx.stroke(); ctx.restore();
  label(ctx, b.x + 6, Ya - 3, 'α²/4 = 1.331×10⁻⁵, the 1s relativistic shift', COL.ref,
    '10px -apple-system, sans-serif', 'left', 'bottom');
  legendAuto(ctx, b, [[COL.pos, 'NIST vacuum (Lyman)'], [COL.ref, 'NIST air (Edlén 1966)']]);
}

/* ------------------------------------------------------------------ *
 *  view 6 — the rates                                                 *
 * ------------------------------------------------------------------ */
function ratesGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, ratesCaption(M),
    'PhET’s weight table against the Einstein A coefficients of real hydrogen, and the dice checked.');
  const uw = usableW(W);
  const top = L.top + 26, bot = L.bot - 16;
  if(narrowStage(W)){
    /* no room for two columns: the branching bars on top, the ensemble below,
       and the lifetime scatter is dropped (the caption says so) */
    const f2 = stackFit(top, bot, 80, 0.40);
    const a2 = box(58, top, uw - 76, f2.side);
    const b2 = box(58, a2.y1 + 80, uw - 76, f2.bh);
    return {L, a: a2, b: b2, c: null, narrow: true};
  }
  const f = stackFit(top, bot, 80, 0.46);
  const hTop = f.side;
  const wHalf = (uw - 100) / 2;
  const a = box(54, top, wHalf, hTop);
  const c = box(54 + wHalf + 62, top, wHalf - 16, hTop);
  /* 80 px between the rows: a's x-axis title and b's panel title overlapped by
     3.6 px at 54 */
  const b = box(54, a.y1 + 80, uw - 70, f.bh);
  return {L, a, b, c};
}
function ratesCaption(M){
  const st = M.st;
  return 'Left: where an atom in level n = ' + st.fromN + ' actually goes. Green is real hydrogen — the Einstein '
    + 'A coefficients, averaged over l with the statistical weight 2l + 1, from the exact dipole integrals. Orange is '
    + 'PhET’s weight table, normalised. They are not the same model and are not meant to be; PhET’s first '
    + 'column happens to be twice A(np→1s) in units of 10⁸ s⁻¹, to within 1.2 %. Right: how long '
    + 'each state lives, τ = 1/ΣA. The 2s state has no allowed one-photon drop at all, so it is metastable '
    + '— which is exactly the state PhET has to nudge the atom out of. Bottom: ' + st.trials + ' seeded cascades '
    + 'against the distribution they were drawn from; every |z| under 3 is the ensemble agreeing with its own rates.';
}
/* a bar's value: above the bar when there is room, just inside its top when
   the bar reaches the frame, and not at all when the bar is empty or the spot
   is already taken by the legend */
function barLabel(ctx, b, X, f, col){
  if(!(f > 0.005)) return;
  const top = b.y1 - b.h * f;
  const above = top - 3 > b.y + 16;
  const y = above ? top - 3 : top + 13;
  ctx.font = '9.5px -apple-system, sans-serif';
  const w = ctx.measureText(fmt(f, 2)).width;
  for(const r of LEGEND_RECTS){
    if(X + w / 2 < r.x || X - w / 2 > r.x + r.w) continue;
    if(y < r.y || y - 11 > r.y + r.h) continue;
    return;
  }
  labelIfClear(ctx, X, y, fmt(f, 2), col, '9.5px -apple-system, sans-serif', 'center',
    above ? 'bottom' : 'top');
}
function drawRates(ctx, W, H, M){
  const st = M.st, G = ratesGeo(ctx, W, H, M);
  drawCaption(ctx, G.L);
  const a = G.a, b = G.b, c = G.c;
  const nF = st.fromN;
  /* --- branching bars --- */
  const tb = trueBranching(nF);
  const pw = phetLowerDist(nF, Math.min(1, nF - 1));
  const phetMap = {};
  for(const [k, p] of pw) phetMap[k] = p;
  const cats = [];
  for(let np = 1; np < nF; np++) cats.push(np);
  axes(ctx, a, 0.5, nF - 0.5, 0, 1, {title: 'where it goes from n = ' + nF,
    xlab: 'lower level n′', ylab: 'branching fraction', nx: Math.max(2, nF - 1), ny: nyFor(a.h),
    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  /* the bars are fillRects, which legendAuto cannot see (it dodges POLY_SEGS),
     so their outlines go into POLY_SEGS BEFORE the legend is placed; the
     legend still goes down before the bar VALUES, so those can dodge it */
  const bw = Math.min(42, a.w / (nF - 1) * 0.34);
  for(let i = 0; i < cats.length; i++){
    const np = cats[i];
    const X = a.x + a.w * (np - 0.5) / (nF - 1);
    const f1 = tb.frac[i], f2 = phetMap[np] || 0;
    for(const [xx, ff] of [[X - bw - 2, f1], [X + 2, f2]]){
      if(!(ff > 0)) continue;
      POLY_SEGS.push(xx, a.y1 - a.h * ff, xx + bw, a.y1 - a.h * ff);
      POLY_SEGS.push(xx, a.y1 - a.h * ff, xx, a.y1);
      POLY_SEGS.push(xx + bw, a.y1 - a.h * ff, xx + bw, a.y1);
    }
  }
  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);
  for(let i = 0; i < cats.length; i++){
    const np = cats[i];
    const X = a.x + a.w * (np - 0.5) / (nF - 1);
    const f1 = tb.frac[i], f2 = phetMap[np] || 0;
    ctx.fillStyle = COL.pos;
    ctx.fillRect(X - bw - 2, a.y1 - a.h * f1, bw, a.h * f1);
    ctx.fillStyle = COL.ref;
    ctx.fillRect(X + 2, a.y1 - a.h * f2, bw, a.h * f2);
    barLabel(ctx, a, X - bw / 2 - 2, f1, COL.pos);
    barLabel(ctx, a, X + bw / 2 + 2, f2, COL.ref);
  }
  /* --- lifetimes (dropped on a narrow stage) --- */
  if(!c){ drawRatesEnsemble(ctx, M, b, cats, nF); return; }
  const taus = [];
  for(let n = 2; n <= NMAX; n++) for(let l = 0; l < n; l++){
    const g = decayRate(n, l);
    taus.push({n, l, tau: g > 0 ? 1e9 / g : Infinity});
  }
  let metaX = 0;
  const fin = taus.filter(t => isFinite(t.tau));
  const tlo = Math.log10(Math.min.apply(null, fin.map(t => t.tau))) - 0.25;
  const thi = Math.log10(Math.max.apply(null, fin.map(t => t.tau))) + 0.25;
  axes(ctx, c, 1.5, NMAX + 0.5, tlo, thi, {title: 'how long each state lives, τ = 1/ΣA',
    xlab: 'n', ylab: 'lifetime (ns, log scale)', nx: 5, ny: nyFor(c.h),
    xticks: [2, 3, 4, 5, 6], xfmt: t => fmt(t, 0),
    yfmt: t => sigf(Math.pow(10, t), 2)});
  /* the 2s note is MANDATORY and goes down before the scatter and the legend,
     so both have to keep out of its way */
  label(ctx, c.x + 8, c.y + 5, c.w < 330 ? '2s: \u03c4 = \u221e, on the top rule'
    : '2s has no allowed drop: \u03c4 = \u221e, plotted on the top rule',
    COL.ref, '10px -apple-system, sans-serif', 'left', 'top');
  for(const t of taus){
    const X = c.x + c.w * (t.n + (t.l - (t.n - 1) / 2) * 0.13 - 1.5) / (NMAX - 1);
    if(!isFinite(t.tau)){
      /* drawn at the top of the axis, so the legend's "no allowed drop" entry
         names something that is actually on the picture (Known-bad: a legend
         entry for a curve that was not drawn is a false statement) */
      metaX = X;
      disc(ctx, X, c.y + 22, 3.4, COL.ref);
      POLY_SEGS.push(X - 4, c.y + 22, X + 4, c.y + 22);
      continue;
    }
    const Y = c.y1 - c.h * (Math.log10(t.tau) - tlo) / (thi - tlo);
    disc(ctx, X, Y, 3.4, mix(COL.pos, COL.live, t.l / Math.max(1, NMAX - 1)));
    /* a scatter of fills is invisible to legendAuto, which dodges POLY_SEGS;
       record each point as a short segment (never zero length, Known-bad) so
       the legend does not land on the data */
    POLY_SEGS.push(X - 4, Y, X + 4, Y);
    if(t.n <= 3) labelIfClear(ctx, X + 5, Y - 5, t.n + 'spdfgh'.charAt(t.l), '#8b93a6',
      '9.5px -apple-system, sans-serif', 'left', 'bottom');
  }
  /* the scatter goes into POLY_SEGS first so the legend dodges the data, and
     the 2s note goes LAST so it dodges the legend */
  legendAuto(ctx, c, [[COL.pos, 'l = 0'], [COL.live, 'l = n − 1'], [COL.ref, 'no allowed drop']]);
  if(metaX){
    ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.45)'; ctx.lineWidth = 1; ctx.setLineDash([3, 3]);
    ctx.beginPath(); ctx.moveTo(c.x, c.y + 22); ctx.lineTo(c.x1, c.y + 22); ctx.stroke(); ctx.restore();
  }
  drawRatesEnsemble(ctx, M, b, cats, nF);
}
function drawRatesEnsemble(ctx, M, b, cats, nF){
  const st = M.st;
  const rows = M.ens.rows;
  /* auto-range: five channels share 1.0, so a fixed 0-1 axis left the bars in
     the bottom fifth of the panel */
  let yTop = 0.25;
  for(const r of rows) yTop = Math.max(yTop, r.f, r.p);
  yTop = Math.min(1, yTop * 1.35);
  axes(ctx, b, 0.5, Math.max(1.5, nF - 0.5), 0, yTop, {title: st.trials + ' seeded cascades: measured against exact',
    xlab: 'lower level n′', ylab: 'fraction of first hops', nx: Math.max(2, nF - 1), ny: nyFor(b.h),
    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 2)});
  /* the note is mandatory: it goes down before the optional z labels, and at
     the TOP of the panel, where the bars are not */
  label(ctx, b.x + 8, b.y + 5, 'mean hops per cascade ' + fmt(M.ens.mean, 3)
    + (M.ens.stuck ? '; ' + M.ens.stuck + ' of ' + st.trials + ' ended stuck in 2s' : ''),
    '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');
  const bw2 = Math.min(46, b.w / Math.max(1, nF - 1) * 0.3);
  for(const r of rows){
    const X = b.x + b.w * (r.n - 0.5) / Math.max(1, nF - 1);
    const hf = b.h * clamp(r.f / yTop, 0, 1);
    POLY_SEGS.push(X - bw2 / 2, b.y1 - hf, X + bw2 / 2, b.y1 - hf);
    POLY_SEGS.push(X - bw2 / 2, b.y1 - hf, X - bw2 / 2, b.y1);
    POLY_SEGS.push(X + bw2 / 2, b.y1 - hf, X + bw2 / 2, b.y1);
  }
  /* the legend goes down before the z labels, so they dodge it rather than
     landing on it (labelIfClear checks LEGEND_RECTS too) */
  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);
  for(const r of rows){
    const X = b.x + b.w * (r.n - 0.5) / Math.max(1, nF - 1);
    const hf = b.h * clamp(r.f / yTop, 0, 1), hp = b.h * clamp(r.p / yTop, 0, 1);
    ctx.fillStyle = COL.live;
    ctx.fillRect(X - bw2 / 2, b.y1 - hf, bw2, hf);
    const se = Math.sqrt(r.p * (1 - r.p) / st.trials);
    ctx.strokeStyle = COL.ref; ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(X - bw2, b.y1 - hp); ctx.lineTo(X + bw2, b.y1 - hp); ctx.stroke();
    ctx.strokeStyle = 'rgba(232,132,58,0.55)'; ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(X, b.y1 - b.h * clamp((r.p - 2 * se) / yTop, 0, 1));
    ctx.lineTo(X, b.y1 - b.h * clamp((r.p + 2 * se) / yTop, 0, 1)); ctx.stroke();
    const zy = b.y1 - Math.max(hf, hp) - 4;
    labelIfClear(ctx, X, zy > b.y + 22 ? zy : b.y1 - Math.max(hf, hp) + 14,
      'z = ' + fmt(r.z, 2), Math.abs(r.z) < 3 ? COL.pos : COL.ref,
      '10px -apple-system, sans-serif', 'center', zy > b.y + 22 ? 'bottom' : 'top');
  }
}

/* ------------------------------------------------------------------ *
 *  dispatch and the scene                                             *
 * ------------------------------------------------------------------ */
function drawView(ctx, W, H, M){
  POLY_SEGS = []; LEGEND_RECTS = []; LABEL_RECTS = [];
  ctx.fillStyle = '#070b18'; ctx.fillRect(0, 0, W, H);
  if(M.view === 'box') drawBox(ctx, W, H, M);
  else if(M.view === 'levels') drawLevels(ctx, W, H, M);
  else if(M.view === 'wave') drawWave(ctx, W, H, M);
  else if(M.view === 'orbitals') drawOrbitals(ctx, W, H, M);
  else if(M.view === 'series') drawSeries(ctx, W, H, M);
  else drawRates(ctx, W, H, M);
}
function makeScene(canvas){
  const S = {st: ST, W: 1100, H: 712};
  S.model = buildModel;
  S.draw = function(){ const ctx = canvas.getContext('2d'); drawView(ctx, S.W, S.H, buildModel()); };
  /* one frame: the box and the levels views run the atom; the rest are static */
  S.step = function(dtWall){
    if(!ST.running) return false;
    if(ST.view !== 'box' && ST.view !== 'levels' && ST.view !== 'wave') return false;
    const dts = (dtWall || 0) * simFactor(ST);
    if(!(dts > 0)) return false;
    if(ST.view === 'wave'){ ATOM.angle = (ATOM.angle - dts * PHET.bohrOmegaDeg * DEG) % TAU; return true; }
    return atomAdvance(ST, dts) > 0;
  };
  /* dragging: the wavelength marker on the series view, the light in the box */
  S.pointer = function(type, x, y){
    if(type === 'up'){ const had = DRAG.what !== null; DRAG.what = null; return had; }
    const ctx = canvas.getContext('2d'), M = buildModel();
    if(ST.view === 'series'){
      const G = serGeo(ctx, S.W, S.H, M), a = G.a;
      const lo = Math.log10(80), hi = Math.log10(15000);
      if(type === 'down' && x >= a.x && x <= a.x1 && y >= a.y && y <= a.y1){ DRAG.what = 'lam'; }
      if(DRAG.what === 'lam'){
        const f = clamp((x - a.x) / a.w, 0, 1);
        ST.lam = Math.round(clamp(Math.pow(10, lo + (hi - lo) * f), PHET.lamMin, PHET.lamMax));
        return true;
      }
      return false;
    }
    if(ST.view === 'box'){
      const G = boxGeo(ctx, S.W, S.H, M), bb = G.bb;
      if(type === 'down' && x >= bb.x && x <= bb.x1 && y >= bb.y && y <= bb.y1){
        DRAG.what = 'light'; ST.lightOn = !ST.lightOn; return true;
      }
      return false;
    }
    if(ST.view === 'wave'){
      const G = waveGeo(ctx, S.W, S.H, M), b = G.b;
      if(type === 'down' && x >= b.x && x <= b.x1 && y >= b.y && y <= b.y1) DRAG.what = 'nu';
      if(DRAG.what === 'nu'){
        ST.nu = Math.round(clamp(0.5 + (7.2 - 0.5) * (x - b.x) / b.w, 0.5, 7.2) * 20) / 20;
        return true;
      }
      return false;
    }
    return false;
  };
  return S;
}
const DRAG = {what: null};
