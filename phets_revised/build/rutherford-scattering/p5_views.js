
/* ================================================================== *
 *  views 4-6: the closed form, the cross section, and real gold       *
 * ================================================================== */

/* --- view 4: the hyperbola -------------------------------------------- */
function hyperGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, hyperCaption(M), hyperCaptionShort(M));
  const avoid = W > 880 ? RO_W + 26 : 10;
  const areaX = 12, areaW = Math.max(180, W - 24 - avoid);
  const stripH = (L.bot - L.top) > 360 ? 142 : 0;
  const side = Math.max(120, Math.min(areaW, L.bot - L.top - (stripH ? stripH + 8 : 0)));
  const bx = areaX + (areaW - side) / 2;
  const fam = bFamily(M);
  /* frame the DEFLECTION, not the widest orbit: scaling from b_max put the
     nucleus and every large-angle orbit inside a tenth of the picture */
  const Rw = Math.max(3 * M.D, 1.3 * M.bSel, 1.15 * fam[fam.length - 1], 40);
  return {L: L, side: side, bx: bx, Rw: Rw,
          g: {s: side / (2 * Rw), Rw: Rw,
              X: mx => bx + side / 2 + mx * side / (2 * Rw),
              Y: my => L.top + side / 2 - my * side / (2 * Rw)},
          strip: stripH ? box(bx + 46, L.top + side + 26, side - 58, stripH - AXIS_BOT - 18) : null};
}
function bFamily(M){
  const n = Math.max(1, Math.round(M.st.nPaths)), out = [];
  const lo = Math.log(M.D * 0.15), hi = Math.log(M.D * 3);
  for(let i = 0; i < n; i++) out.push(Math.exp(lo + (hi - lo) * (n === 1 ? 0.5 : i / (n - 1))));
  return out;
}
function drawHyper(ctx, W, H, M){
  const G = hyperGeo(ctx, W, H, M), g = G.g, st = M.st, D = M.D;
  const bb = box(G.bx, G.L.top, G.side, G.side);
  ctx.fillStyle = '#080c16'; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  frame(ctx, bb, '#242a3a');
  const cx = g.X(0), cy = g.Y(0);
  /* the family */
  /* both sides.  A beam is not one-sided, and drawing only +b left three
     quarters of the frame empty and the picture reading as a spray out of the
     nucleus rather than a beam passing it (the same failure as drawing each
     conic in its own frame -- Known-bad, differential_scattering). */
  for(const b of bFamily(M)){
    const pts = conicPath(b, D, g.Rw * 2.4, 260);
    strokeModel(ctx, g, bb, pts, rgba(COL.ref, 0.30), 1);
    const mir = [];
    for(let i = 0; i < pts.length; i += 2) mir.push(-pts[i], pts[i + 1]);
    strokeModel(ctx, g, bb, mir, rgba(COL.ref, 0.30), 1);
  }
  /* r_min of the selected orbit */
  const bSel = Math.max(1e-6, M.bSel);
  ring(ctx, cx, cy, rminOfB(bSel, D) * g.s, rgba(COL.str, 0.5), 1, [2, 3]);
  /* the asymptotes */
  if(st.showAsym){
    const thS = thetaOfB(bSel, D), phiI = PI - thS, far = g.Rw * 3;
    aline(ctx, g, bb, bSel, -far, bSel, 0.02 * far, rgba(COL.str, 0.55), [6, 4]);
    /* the outgoing asymptote: take a far point of the conic and drop the
       component along the outgoing direction.  Deriving the foot from a sign
       convention instead put it on the wrong side of the nucleus. */
    const dx = Math.sin(phiI), dy = -Math.cos(phiI);
    const rf = rOfPhi(phiI * (1 - 1e-7), bSel, D);
    const fx = rf * Math.sin(phiI * (1 - 1e-7)), fy = -rf * Math.cos(phiI * (1 - 1e-7));
    const dot = fx * dx + fy * dy;
    const ox = fx - dot * dx, oy = fy - dot * dy;
    aline(ctx, g, bb, ox - dx * far * 0.02, oy - dy * far * 0.02, ox + dx * far, oy + dy * far,
          rgba(COL.str, 0.55), [6, 4]);
    /* the impact parameter itself, offset below the nucleus so its label does
       not land on the nucleus glyph */
    const bY = -Math.min(g.Rw * 0.22, rminOfB(bSel, D) * 0.55);
    aline(ctx, g, bb, 0, bY, bSel, bY, COL.live, null, 1.8);
    aline(ctx, g, bb, 0, 0, 0, bY, rgba(COL.live, 0.4), [2, 3], 1);
    labelIfClear(ctx, (cx + g.X(bSel)) / 2, g.Y(bY) - 4, 'b = ' + fmt(bSel, 1), COL.live,
      'italic 12px Georgia, serif', 'center', 'bottom');
  }
  /* the selected closed form, then the integrated path over it */
  const sel = conicPath(bSel, D, g.Rw * 2.4, 520);
  strokeModel(ctx, g, bb, sel, COL.ref, 2.2);
  if(st.showInt){
    const io = hyperCheck(M);
    const pts = [];
    for(let i = 0; i < io.pts.length; i += 2) pts.push(io.pts[i] * D, io.pts[i + 1] * D);
    strokeModel(ctx, g, bb, pts, COL.pos, 1.6, [5, 4]);
  }
  /* the closest approach */
  const phiMin = phiInfOf(bSel, D) / 2, rm = rminOfB(bSel, D);
  const mx = g.X(rm * Math.sin(phiMin)), my = g.Y(-rm * Math.cos(phiMin));
  if(mx > bb.x && mx < bb.x1 && my > bb.y && my < bb.y1){
    disc(ctx, mx, my, 3.4, COL.live);
    if(!labelIfClear(ctx, mx + 7, my - 4, 'r min = ' + fmt(rm, 1), COL.live,
        '10.5px -apple-system, sans-serif', 'left', 'bottom'))
      labelIfClear(ctx, mx - 7, my - 4, 'r min = ' + fmt(rm, 1), COL.live,
        '10.5px -apple-system, sans-serif', 'right', 'bottom');
  }
  drawNucleus(ctx, g, 0, 0, st.protons, st.neutrons, Math.max(5, D * g.s * 0.22));
  labelIfClear(ctx, cx + 9, cy + 11, 'D = ' + fmt(D, 2), COL.str,
    '10.5px -apple-system, sans-serif', 'left', 'top');
  legendAuto(ctx, bb, [[COL.ref, 'the closed form'], [COL.pos, 'RK4 on Newton’s equations'],
                       [COL.str, 'asymptotes, r min'], [COL.live, 'b, closest approach']]);
  if(G.strip) deflectionPanel(ctx, G.strip, M);
  drawCaption(ctx, G.L);
  return G;
}
/* Everything in this view is drawn through polyline(), whose clipping is in
   DATA space -- a ctx.clip() fixes the browser and not the display-list audit,
   which records clip() as a no-op (Known-bad).  polyline's own mapping of
   [-Rw, Rw] onto a square box is the same map as g.X / g.Y, exactly.  The
   first version drew the whole family unclipped and the orbits ran across the
   caption and off the stage. */
function strokeModel(ctx, g, bb, pts, col, lw, dash){
  if(pts.length < 4) return;
  const xs = [], ys = [];
  for(let i = 0; i < pts.length; i += 2){ xs.push(pts[i]); ys.push(pts[i + 1]); }
  polyline(ctx, bb, xs, ys, -g.Rw, g.Rw, -g.Rw, g.Rw, col, lw || 1, dash);
}
function aline(ctx, g, bb, x0, y0, x1, y1, col, dash, lw){
  polyline(ctx, bb, [x0, x1], [y0, y1], -g.Rw, g.Rw, -g.Rw, g.Rw, col, lw || 1.2, dash);
}
/* theta(b): the closed form and the quadrature that has never been told it */
function deflectionPanel(ctx, b, M){
  const D = M.D;
  const lo = Math.log10(D * 0.04), hi = Math.log10(D * 20);
  const xs = [], ys = [];
  for(let i = 0; i <= 160; i++){
    const bb = Math.pow(10, lo + (hi - lo) * i / 160);
    xs.push(Math.log10(bb)); ys.push(thetaOfB(bb, D) * 180 / PI);
  }
  panelTitle(ctx, b, 'θ(b) = 2 atan(D/2b), and the deflection integral that never heard of it');
  axes(ctx, b, lo, hi, 0, 180, {yticks: b.h < 70 ? [90, 180] : [45, 90, 135, 180], nx: 5,
    xfmt: t => sigf(Math.pow(10, t), 2), yfmt: t => fmt(t, 0) + '°',
    xlab: 'impact parameter b, model units (log)', ylab: 'deflection θ'});
  polyline(ctx, b, xs, ys, lo, hi, 0, 180, COL.ref, 2);
  /* the independent route: the deflection integral for U/E = D/r */
  for(let i = 0; i <= 11; i++){
    const bb = Math.pow(10, lo + (hi - lo) * i / 11);
    const th = thetaQuad(bb, r => D / r, 12) * 180 / PI;
    const x = b.x + b.w * (Math.log10(bb) - lo) / (hi - lo);
    const y = b.y1 - b.h * clamp(th, 0, 180) / 180;
    ring(ctx, x, y, 3.2, COL.pos, 1.4);
  }
  const xs2 = Math.log10(Math.max(1e-9, M.bSel));
  if(xs2 > lo && xs2 < hi){
    const x = b.x + b.w * (xs2 - lo) / (hi - lo);
    ctx.save(); ctx.strokeStyle = COL.live; ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(x, b.y); ctx.lineTo(x, b.y1); ctx.stroke(); ctx.restore();
  }
  legendAuto(ctx, b, [[COL.ref, 'closed form'], [COL.pos, 'quadrature'], [COL.live, 'b on the left']]);
}

/* --- view 5: the cross section ---------------------------------------- */
function sigmaGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, sigCaption(M), sigCaptionShort(M));
  const avoid = W > 880 ? RO_W + 26 : 10;
  const x0 = 54, wAll = Math.max(160, W - x0 - 18 - avoid);
  if(narrowStage(W)){
    /* the upper panel's x-axis title ends 33 px below its frame and the lower
       panel's title starts 24 px above its own, so 64 px of gap is the
       minimum -- at 30 they overlapped by 3 px at 560x380 */
    const f = stackFit(L.top, L.bot, 44, 0.44);
    return {L: L, a: box(x0, L.top + 14, wAll, f.side - AXIS_BOT),
            c: box(x0, L.top + 14 + f.side + 26, wAll, f.bh), stacked: true};
  }
  const gap = 66, pw = (wAll - gap) / 2;
  const hh = L.bot - L.top - AXIS_BOT - 14;
  return {L: L, a: box(x0, L.top + 14, pw, hh), c: box(x0 + pw + gap, L.top + 14, pw, hh),
          stacked: false};
}
function drawSigma(ctx, W, H, M){
  const G = sigmaGeo(ctx, W, H, M), st = M.st;
  const B = beamSample(st), D = B.D;
  const thMin = thetaOfB(st.bMax, D);
  const xlo = Math.log10(thMin * 180 / PI * 0.8), xhi = Math.log10(180);
  /* ---- panel A: dsigma/dOmega ---- */
  const dsLo = Math.log10(dsdoOf(PI, D) * 0.5), dsHi = Math.log10(dsdoOf(thMin * 0.9, D) * 2);
  const a = G.a;
  panelTitle(ctx, a, 'dσ/dΩ, three ways');
  axes(ctx, a, xlo, xhi, dsLo, dsHi, {yticks: ticksNoFloor(dsLo, dsHi, nyFor(a.h)), nx: 4,
    xfmt: t => sigf(Math.pow(10, t), 2) + '°', yfmt: t => '10' + supStr(Math.round(t)),
    xlab: 'scattering angle (log)',
    ylab: G.stacked ? 'dσ/dΩ (log)' : 'dσ/dΩ, model units²/sr (log)'});
  const xs = [], ys = [];
  for(let i = 0; i <= 220; i++){
    const th = Math.pow(10, xlo + (xhi - xlo) * i / 220) * PI / 180;
    xs.push(Math.log10(th * 180 / PI)); ys.push(Math.log10(dsdoOf(th, D)));
  }
  polyline(ctx, a, xs, ys, xlo, xhi, dsLo, dsHi, COL.ref, 2.2);
  if(st.showJac){
    for(let i = 0; i <= 10; i++){
      const th = Math.pow(10, xlo + (xhi - xlo) * (i + 0.5) / 11) * PI / 180;
      const v = dsdoNumeric(th, D);
      if(!isFinite(v) || v <= 0) continue;
      const x = a.x + a.w * (Math.log10(th * 180 / PI) - xlo) / (xhi - xlo);
      const y = a.y1 - a.h * (Math.log10(v) - dsLo) / (dsHi - dsLo);
      if(y < a.y || y > a.y1) continue;
      ring(ctx, x, y, 3.4, COL.pos, 1.5);
    }
  }
  if(st.showSample){
    for(const bn of B.bins){
      if(!bn.n) continue;
      const mid = Math.sqrt(bn.lo * bn.hi) * 180 / PI;
      const x = a.x + a.w * (Math.log10(mid) - xlo) / (xhi - xlo);
      const y = a.y1 - a.h * (Math.log10(bn.dens) - dsLo) / (dsHi - dsLo);
      if(x < a.x || x > a.x1 || y < a.y || y > a.y1) continue;
      const yUp = a.y1 - a.h * (Math.log10(bn.dens * (1 + bn.sigma)) - dsLo) / (dsHi - dsLo);
      const yDn = a.y1 - a.h * (Math.log10(bn.dens * Math.max(1e-6, 1 - bn.sigma)) - dsLo) / (dsHi - dsLo);
      ctx.save(); ctx.strokeStyle = COL.live; ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.moveTo(x, Math.max(a.y, yUp)); ctx.lineTo(x, Math.min(a.y1, yDn));
      ctx.stroke(); ctx.restore();
      disc(ctx, x, y, 2.6, COL.live);
    }
  }
  legendAuto(ctx, a, [[COL.ref, '(D/4)²/sin⁴(θ/2)'],
                      [COL.pos, '(b/sinθ)|db/dθ|'],
                      [COL.live, fmt(st.nSample, 0) + ' sampled, ±1/√N']]);
  /* ---- panel C: the cumulative ---- */
  const c = G.c;
  const cLo = Math.log10(Math.max(1e-6, sigmaBeyond(PI * 0.999, D) / (PI * st.bMax * st.bMax) * 0.5));
  panelTitle(ctx, c, 'the fraction of the beam turned past θ');
  axes(ctx, c, xlo, xhi, cLo, 0.15, {yticks: ticksNoFloor(cLo, 0.15, nyFor(c.h)), nx: 4,
    xfmt: t => sigf(Math.pow(10, t), 2) + '°', yfmt: t => '10' + supStr(Math.round(t)),
    xlab: 'scattering angle (log)',
    ylab: G.stacked ? 'fraction (log)' : 'fraction beyond θ (log)'});
  const xs2 = [], ys2 = [], xs3 = [], ys3 = [];
  for(let i = 0; i <= 200; i++){
    const th = Math.pow(10, xlo + (xhi - xlo) * i / 200) * PI / 180;
    const ex = sigmaBeyond(Math.min(th, PI * 0.9999), D) / (PI * st.bMax * st.bMax);
    xs2.push(Math.log10(th * 180 / PI)); ys2.push(Math.log10(Math.max(1e-30, Math.min(1, ex))));
  }
  polyline(ctx, c, xs2, ys2, xlo, xhi, cLo, 0.15, COL.ref, 2.2);
  if(st.showSample){
    for(let i = 0; i <= 18; i++){
      const th = Math.pow(10, xlo + (xhi - xlo) * i / 18) * PI / 180;
      const f = fractionBeyond(B.th, th);
      if(f <= 0) continue;
      xs3.push(Math.log10(th * 180 / PI)); ys3.push(Math.log10(f));
    }
    for(let i = 0; i < xs3.length; i++){
      const x = c.x + c.w * (xs3[i] - xlo) / (xhi - xlo);
      const y = c.y1 - c.h * (ys3[i] - cLo) / (0.15 - cLo);
      if(x < c.x || x > c.x1 || y < c.y || y > c.y1) continue;
      disc(ctx, x, y, 2.6, COL.live);
    }
  }
  legendAuto(ctx, c, [[COL.ref, 'π b(θ)² / π bmax²'],
                      [COL.live, 'the seeded beam']]);
  drawCaption(ctx, G.L);
  return G;
}

/* --- view 6: gold, for real ------------------------------------------- */
function goldGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, goldCaption(M), goldCaptionShort(M));
  const avoid = W > 880 ? RO_W + 26 : 10;
  const x0 = 58, wAll = Math.max(160, W - x0 - 18 - avoid);
  /* the ruler needs seven 15 px label rows and the bar under them, and not a
     pixel more: give the rest to the plot */
  const f = stackFit(L.top + 4, L.bot, 44, 0.30);
  const rh = clamp(f.side - 30, 80, 150);
  return {L: L, ruler: box(x0, L.top + 20, wAll, rh),
          plot: box(x0, L.top + 24 + rh + 40, wAll,
                    Math.max(60, L.bot - AXIS_BOT - (L.top + 24 + rh + 40)))};
}
function drawGold(ctx, W, H, M){
  const G = goldGeo(ctx, W, H, M), st = M.st, g = M.gold;
  /* ---- the ruler: every length in the problem on one log axis ---- */
  const b = G.ruler;
  const lo = Math.log10(0.5 * FM), hi = Math.log10(1e-8);
  const X = r => b.x + b.w * (Math.log10(r) - lo) / (hi - lo);
  panelTitle(ctx, b, 'the lengths, on one logarithmic ruler');
  frame(ctx, b, '#242a3a');
  ctx.save(); ctx.strokeStyle = '#181d29'; ctx.lineWidth = 1;
  for(let e = Math.ceil(lo); e <= Math.floor(hi); e++){
    const x = X(Math.pow(10, e));
    ctx.beginPath(); ctx.moveTo(x, b.y); ctx.lineTo(x, b.y1); ctx.stroke();
  }
  ctx.restore();
  for(let e = Math.ceil(lo); e <= Math.floor(hi); e++)
    label(ctx, X(Math.pow(10, e)), b.y1 + 3, '10' + supStr(e) + ' m', COL.faint,
      '10px -apple-system, sans-serif', 'center', 'top');
  const items = [
    [g.Ralpha, COL.neutron, 'alpha radius', 0],
    [g.Rnuc, COL.str, 'gold nucleus, 1.2 A⅓ fm', 1],
    [g.Rnuc + g.Ralpha, COL.str, 'touching', 2],
    [g.a, COL.ref, 'a = D/2 = b at 90°', 3],
    [g.D, COL.ref, 'D, head-on closest approach', 4],
    [g.rminA, COL.pos, 'r min at b = a', 5],
    [PHET.nuclearScaleM, COL.dim, 'PhET’s nuclear-scale caption', 6],
    [GOLD.rAtom, COL.live, 'gold atom, 1.44 Å', 0],
    [g.spacing, COL.live, 'atom spacing n⁻⅓', 1],
    [PHET.atomicScaleM, COL.dim, 'PhET’s atomic-scale caption', 2],
  ];
  /* ten labels need ten rows, not four: with four they landed on each other
     and sideLabel dropped half of them.  A leader joins each label to its own
     rule, because at this density the nearest rule is not the right one. */
  const lanes = Math.max(2, Math.min(7, Math.floor((b.h - 26) / 15)));
  for(const [r, c, nm, lane] of items){
    if(!(r > 0)) continue;
    const x = clamp(X(r), b.x, b.x1);
    ctx.save(); ctx.strokeStyle = c; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(x, b.y + 2); ctx.lineTo(x, b.y1 - 2); ctx.stroke(); ctx.restore();
    const ly = b.y + 5 + (lane % lanes) * 15;
    sideLabel(ctx, b, x, ly, nm, c);
  }
  /* the gap that makes Rutherford's law exact here */
  ctx.save(); ctx.strokeStyle = rgba(COL.pos, 0.6); ctx.lineWidth = 6;
  ctx.beginPath(); ctx.moveTo(X(g.Rnuc + g.Ralpha), b.y1 - 9); ctx.lineTo(X(g.D), b.y1 - 9);
  ctx.stroke(); ctx.restore();
  labelIfClear(ctx, (X(g.Rnuc + g.Ralpha) + X(g.D)) / 2, b.y1 - 12,
    'never touches: pure Coulomb up to ' + fmt(g.Etouch / MEV, 1) + ' MeV',
    COL.pos, '10px -apple-system, sans-serif', 'center', 'bottom');

  /* ---- the plot: what each model says a foil does ---- */
  const c = G.plot;
  const xlo = Math.log10(0.3), xhi = Math.log10(180);
  const ylo = -40, yhi = 0.4;
  panelTitle(ctx, c, 'fraction of the beam turned past θ by ' + fmt(st.foilNm, 0)
    + ' nm of gold — the two models');
  axes(ctx, c, xlo, xhi, ylo, yhi, {yticks: ticksNoFloor(ylo, yhi, nyFor(c.h)), nx: 4,
    xfmt: t => sigf(Math.pow(10, t), 2) + '°', yfmt: t => '10' + supStr(Math.round(t)),
    xlab: 'scattering angle (log)', ylab: 'fraction beyond θ (log)'});
  const xr = [], yr = [], xt = [], yt = [];
  for(let i = 0; i <= 220; i++){
    const th = Math.pow(10, xlo + (xhi - xlo) * i / 220) * PI / 180;
    xr.push(Math.log10(th * 180 / PI));
    yr.push(Math.log10(Math.max(1e-99, Math.min(1, g.nt * sigmaBeyond(Math.min(th, PI * 0.9999), g.D)))));
    xt.push(Math.log10(th * 180 / PI));
    yt.push(thomsonLog10P(th, g.th2));
  }
  polyline(ctx, c, xr, yr, xlo, xhi, ylo, yhi, COL.ref, 2.2);
  polyline(ctx, c, xt, yt, xlo, xhi, ylo, yhi, COL.pos, 2.2);
  const x90 = c.x + c.w * (Math.log10(90) - xlo) / (xhi - xlo);
  ctx.save(); ctx.strokeStyle = rgba(COL.live, 0.7); ctx.lineWidth = 1.2; ctx.setLineDash([4, 4]);
  ctx.beginPath(); ctx.moveTo(x90, c.y); ctx.lineTo(x90, c.y1); ctx.stroke(); ctx.restore();
  legendAuto(ctx, c, [[COL.ref, 'Rutherford: 1 in ' + sigf(1 / g.f90, 3) + ' past 90°'],
                      [COL.pos, 'Thomson: 10' + supStr(Math.round(g.log10P)) + ' past 90°']]);
  /* where the Thomson curve crosses the bottom of the box: -theta^2/<th2>/ln10
     = ylo, so theta = sqrt(-ylo ln10 <theta^2>) */
  const thCut = Math.sqrt(-ylo * Math.LN10 * g.th2) * 180 / PI;
  const xcut = c.x + c.w * (Math.log10(thCut) - xlo) / (xhi - xlo);
  if(xcut > c.x && xcut < c.x1)
    labelIfClear(ctx, xcut + 5, c.y1 - 5, 'Thomson falls off the bottom at '
      + fmt(thCut, 2) + '°', COL.pos, '10px -apple-system, sans-serif', 'left', 'bottom');
  drawCaption(ctx, G.L);
  return G;
}

/* ------------------------------------------------------------------ *
 *  captions -- every scale distortion is printed on the canvas         *
 * ------------------------------------------------------------------ */
function liveCaption(M){
  const st = M.st;
  if(M.view === 'nucleus')
    return 'PhET’s nuclear-scale scene, reproduced in its own model units: the box is 255 units across and the '
      + 'head-on distance of closest approach is D = ' + fmt(M.D, 2) + ' units, one eighth of the box. '
      + 'Nothing here is to scale — PhET’s caption calls this box 1.5×10⁻¹³ m, in which a real '
      + 'gold nucleus would be ' + fmt(2 * M.gold.Rnuc / PHET.nuclearScaleM * 100, 1)
      + '% of the width and D would be ' + fmt(M.gold.D / PHET.nuclearScaleM * 100, 1) + '%, against the drawn 12.5%. '
      + 'The neutron slider changes the drawn nucleus and nothing else. A particle is put on the hyperbola whose '
      + 'ASYMPTOTE is parallel to its direction, so its own direction steps by at most ' + deg(M.kinkMax)
      + ' as it is picked up at the frame edge \u2014 PhET does the same, and that step is the price of taking the '
      + 'potential to be zero outside the tracked box. Traces are ' + (st.traces ? 'on' : 'off') + '.';
  return 'PhET’s atomic-scale scene: five atoms in a 255-unit box, each tracked inside a square of side 30 '
    + '(dashed), each with its own D = ' + fmt(M.D, 3) + ' — again exactly one eighth of ITS box, which is why the '
    + 'picture looks the same at both zooms although the two captions are 4000× apart and the geometry is only '
    + fmt(PHET.boxW / PHET.atomW, 1) + '×. A real gold atom is '
    + sigf(M.gold.ratio, 3) + ' nuclear diameters across; draw that honestly and the nucleus is invisible.';
}
function liveCaptionShort(M){
  return 'PhET’s ' + (M.view === 'nucleus' ? 'nuclear' : 'atomic') + '-scale scene in its own model units. '
    + 'D = ' + fmt(M.D, 2) + ' units = L/8. Not to scale; see the readout.';
}
function puddCaption(M){
  const g = M.gold, st = M.st;
  return 'Thomson’s atom: the positive charge spread through a ball the size of the whole atom. PhET’s '
    + 'plum-pudding screen has no scattering model at all — the particles go straight through — and that is '
    + 'the right answer. A uniform ball of +' + fmt(st.protons, 0) + 'e of radius ' + sigf(GOLD.rAtom, 3)
    + ' m turns a ' + fmt(st.EMeV, 2) + ' MeV alpha by at most D/2R = ' + sigf(g.thMax, 3) + ' rad = '
    + fmt(g.thMax * 180 / PI * 3600, 1) + ' arcsec, whatever the impact parameter. The deflection drawn here is '
    + (st.exagg === 1 ? 'the true one' : 'exaggerated ×' + fmt(st.exagg, 0))
    + '; at ×1 the sideways shift across the whole box is '
    + sigf(g.thMax * PHET.boxW, 2) + ' of a model unit, well under a pixel.';
}
function puddCaptionShort(M){
  return 'Thomson’s atom turns an alpha by at most ' + sigf(M.gold.thMax, 3)
    + ' rad. Drawn ×' + fmt(M.st.exagg, 0) + '.';
}
function hyperCaption(M){
  const io = hyperCheck(M), bInt = hyperB(M);
  return 'One nucleus and a family of impact parameters, drawn from the closed form r = b²/[b sinφ + '
    + '(D/2)(cosφ − 1)]. The selected orbit carries an RK4 integration of Newton’s equations over it '
    + '(green, dashed): started on the conic at 12 D, it conserves energy to ' + sigf(io.dE, 2)
    + ' and angular momentum to ' + sigf(io.dL, 2) + ', and its final direction differs from 2 atan(D/2b) by '
    + sigf(Math.abs(io.theta - thetaOfB(bInt, M.D)), 2) + ' rad — a truncation that falls as 1/r², not an error. '
    + (bInt !== M.bSel ? 'Below b = 0.02 D the orbit is a hairpin with a near-cusp at its turning point, which no '
      + 'fixed-step integrator can cross: the green overlay is drawn at b = ' + fmt(bInt, 2)
      + ' (θ = ' + deg(thetaOfB(bInt, M.D)) + ') instead, and the b = 0 case is checked in selfTest against the '
      + 'closed parametric solution of the radial problem. ' : '')
    + 'The incoming asymptotes are drawn PARALLEL because a beam is parallel: conic sections are usually written '
    + 'with periapsis on an axis, and a family drawn that way fans out from the target and reads as emission '
    + 'rather than scattering. Only ' + deg(M.turnSel) + ' of the ' + deg(M.thSel)
    + ' is delivered inside a box of ±' + fmt(PHET.boxW / 2, 0) + ' units; the rest is out past the frame.';
}
function hyperCaptionShort(M){
  return 'The closed-form hyperbola (orange) with an RK4 integration of Newton’s equations over it (green).';
}
function sigCaption(M){
  const st = M.st, B = beamSample(st);
  return fmt(st.nSample, 0) + ' particles with impact parameter uniform on a disc of radius ' + fmt(st.bMax, 0)
    + ' model units, from a seeded mulberry32 whose stream is reproduced bit for bit in Python. Binned in SOLID '
    + 'ANGLE and divided by the beam area, they land on (D/4)²/sin⁴(θ/2) — which is drawn here as '
    + 'the closed form and, independently, as the Jacobian (b/sinθ)|db/dθ| taken by differencing θ(b). '
    + 'No angle below ' + fmt(thetaOfB(st.bMax, B.D) * 180 / PI, 2) + '° can appear: that is the angle at '
    + 'b = bmax. Error bars are 1/√N per bin, which is the sampling law, not a fit.';
}
function sigCaptionShort(M){
  return 'The 1/sin⁴(θ/2) law three ways: closed form, Jacobian, and ' + fmt(M.st.nSample, 0)
    + ' seeded particles.';
}
function goldCaption(M){
  const g = M.gold, st = M.st;
  return 'The same problem in metres. A ' + fmt(st.EMeV, 2) + ' MeV alpha on Z = ' + fmt(st.protons, 0)
    + ' has D = ' + fmt(g.D / FM, 1) + ' fm, and the gold nucleus plus the alpha is only '
    + fmt((g.Rnuc + g.Ralpha) / FM, 1) + ' fm across — so even head-on the two never touch, the field is pure '
    + 'Coulomb, and the 1/sin⁴ law is exact. That stops at ' + fmt(g.Etouch / MEV, 1)
    + ' MeV. Below: what a ' + fmt(st.foilNm, 0) + ' nm gold leaf (' + fmt(g.deep, 0)
    + ' atoms deep) does to a beam under each model. Rutherford sends 1 in ' + sigf(1 / g.f90, 3)
    + ' past 90°; Thomson’s multiple scattering (θrms = ' + fmt(g.thRms * 180 / PI, 3)
    + '°) sends 10' + supStr(Math.round(g.log10P)) + ', so its curve leaves the bottom of the plot and never '
    + 'comes back. That factor is the discovery of the nucleus.';
}
function goldCaptionShort(M){
  return 'Alpha on gold in metres: D = ' + fmt(M.gold.D / FM, 1) + ' fm against a nucleus of '
    + fmt(M.gold.Rnuc / FM, 1) + ' fm, so the two never touch.';
}

/* ------------------------------------------------------------------ *
 *  dispatch and the scene                                             *
 * ------------------------------------------------------------------ */
function drawView(ctx, W, H, M){
  POLY_SEGS = []; LEGEND_RECTS = []; LABEL_RECTS = [];
  ctx.fillStyle = COL.bg; ctx.fillRect(0, 0, W, H);
  if(M.view === 'nucleus' || M.view === 'foil') drawLive(ctx, W, H, M);
  else if(M.view === 'pudding') drawPudding(ctx, W, H, M);
  else if(M.view === 'hyperbola') drawHyper(ctx, W, H, M);
  else if(M.view === 'sigma') drawSigma(ctx, W, H, M);
  else drawGold(ctx, W, H, M);
}
const DRAG = {what: null};
function makeScene(canvas){
  const S = {st: ST, W: 1400, H: 820};
  S.model = buildModel;
  S.draw = function(){ const ctx = canvas.getContext('2d'); drawView(ctx, S.W, S.H, buildModel()); };
  S.step = function(dtWall){
    if(!ST.running || !liveView(ST.view)) return false;
    return engineAdvance(ST, dtWall || 0) > 0;
  };
  /* the pointer: clicking a live stage works the gun, dragging the hyperbola
     view sets the impact parameter.  No wheel handler exists, because no view
     reads a zoom -- a no-op handler nothing calls is dead code (Known-bad). */
  S.pointer = function(type, x, y){
    if(type === 'up'){ const had = DRAG.what !== null; DRAG.what = null; return had; }
    const ctx = canvas.getContext('2d'), M = buildModel();
    if(liveView(ST.view)){
      const G = ST.view === 'pudding' ? puddingGeo(ctx, S.W, S.H, M) : liveGeo(ctx, S.W, S.H, M);
      const g = G.g;
      if(type === 'down' && x >= g.x0 && x <= g.x0 + G.side && y >= g.y0 && y <= g.y0 + G.side){
        DRAG.what = 'gun'; ST.gunOn = !ST.gunOn; return true;
      }
      return false;
    }
    if(ST.view === 'hyperbola'){
      const G = hyperGeo(ctx, S.W, S.H, M), g = G.g;
      if(type === 'down' && x >= G.bx && x <= G.bx + G.side && y >= G.L.top && y <= G.L.top + G.side)
        DRAG.what = 'b';
      if(DRAG.what === 'b'){
        const mx = (x - (G.bx + G.side / 2)) / g.s;
        ST.bModel = clamp(Math.abs(mx), 0, 200);
        return true;
      }
      return false;
    }
    return false;
  };
  return S;
}
