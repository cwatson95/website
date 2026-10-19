
/* ================================================================== *
 *  the live stage: PhET's two Rutherford scenes and its plum pudding  *
 * ================================================================== */
/* the model box is 255 x 255 in PhET's units with y UP (its gun sits at the
   minimum y and fires along +y).  mapBox returns the screen transform. */
function mapBox(x0, y0, side){
  const s = side / PHET.boxW;
  return {
    s: s, x0: x0, y0: y0, side: side,
    X: mx => x0 + side / 2 + mx * s,
    Y: my => y0 + side / 2 - my * s,
  };
}
/* the square stage: a box, a census strip under it, the caption under that */
function liveGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, liveCaption(M), liveCaptionShort(M));
  const avoid = W > 880 ? RO_W + 26 : 10;
  const areaX = 12, areaW = Math.max(180, W - 24 - avoid);
  /* the gun sits BELOW the box, because PhET's gun fires from the minimum y
     of the model bounds, so the square has to give up a band for it -- the
     first version drew the gun label into the census strip and the caption at
     every size under 900 px */
  const gunH = 22;
  const stripH = (L.bot - L.top) > 360 ? 70 : 0;
  const side = Math.max(120, Math.min(areaW, L.bot - L.top - gunH - (stripH ? stripH + 30 : 0)));
  const bx = areaX + (areaW - side) / 2;
  const g = mapBox(bx, L.top, side);
  const strip = stripH ? box(bx, L.top + side + gunH + 26, side, stripH - 26) : null;
  return {L: L, g: g, strip: strip, side: side, gunH: gunH};
}

/* --- the drawn atom --------------------------------------------------- *
 *  Nucleons on a sunflower (Vogel) spiral: r = c sqrt(k), theta = k x the
 *  golden angle.  Deterministic, needs no table, and packs at constant
 *  density -- PhET builds its nucleus in rings instead, which is the same
 *  idea with a hand-written ring rule.                                     */
const GOLDEN_ANGLE = PI * (3 - Math.sqrt(5));
function nucleonLayout(nP, nN){
  const n = nP + nN, out = [];
  for(let k = 0; k < n; k++){
    const r = Math.sqrt(k + 0.5), a = k * GOLDEN_ANGLE;
    /* alternate the species along the spiral so neither ends up in a shell */
    out.push({x: r * Math.cos(a), y: r * Math.sin(a), p: (k % 2 === 0) === (nP >= nN)});
  }
  /* exactly nP protons: walk the list and fix the count */
  let want = nP, have = 0;
  for(const q of out) if(q.p) have++;
  for(let i = 0; i < out.length && have !== want; i++){
    if(have > want && out[i].p){ out[i].p = false; have--; }
    else if(have < want && !out[i].p){ out[i].p = true; have++; }
  }
  return out;
}
/* clip a world-space polyline to the model box, in DATA space: a canvas
   ctx.clip() would fix the browser and NOT the display-list audit, which
   records clip() as a no-op (Known-bad).  Liang-Barsky, crossings kept. */
function strokeBoxed(ctx, g, pts){
  const B = PHET.boxW / 2;
  ctx.beginPath();
  let started = false;
  for(let i = 0; i + 3 < pts.length; i += 2){
    const X0 = pts[i], Y0 = pts[i + 1], X1 = pts[i + 2], Y1 = pts[i + 3];
    if(!isFinite(X0) || !isFinite(Y0) || !isFinite(X1) || !isFinite(Y1)){ started = false; continue; }
    let t0 = 0, t1 = 1, out = false;
    const dx = X1 - X0, dy = Y1 - Y0;
    const P = [-dx, dx, -dy, dy], Q = [X0 + B, B - X0, Y0 + B, B - Y0];
    for(let k = 0; k < 4 && !out; k++){
      if(P[k] === 0){ if(Q[k] < 0) out = true; continue; }
      const t = Q[k] / P[k];
      if(P[k] < 0){ if(t > t1) out = true; else if(t > t0) t0 = t; }
      else { if(t < t0) out = true; else if(t < t1) t1 = t; }
    }
    if(out || t0 > t1){ started = false; continue; }
    if(t0 > 0) started = false;
    if(!started){ ctx.moveTo(g.X(X0 + t0 * dx), g.Y(Y0 + t0 * dy)); started = true; }
    ctx.lineTo(g.X(X0 + t1 * dx), g.Y(Y0 + t1 * dy));
    if(t1 < 1) started = false;
  }
  ctx.stroke();
}
function drawNucleus(ctx, g, ax, ay, nP, nN, rPix){
  /* below about 8 px the nucleons are sub-pixel and average to mud: draw the
     nucleus as what it is at that scale, a point with a ring round it */
  if(rPix < 8){
    disc(ctx, g.X(ax), g.Y(ay), Math.max(1.6, rPix * 0.55), COL.proton);
    ring(ctx, g.X(ax), g.Y(ay), Math.max(2.6, rPix), rgba(COL.proton, 0.5), 1);
    return;
  }
  const lay = nucleonLayout(nP, nN);
  const span = Math.sqrt(lay.length) + 1;
  const sc = rPix / span;
  const cx = g.X(ax), cy = g.Y(ay);
  for(const q of lay) disc(ctx, cx + q.x * sc, cy + q.y * sc,
                           Math.max(1, sc * 0.95), q.p ? COL.proton : COL.neutron);
}
/* the gun lives in the band under the box; its label goes beside it and is
   DROPPED if there is no room, rather than stacking on the strip below */
/* one place, because the labels of the analytic overlay have to keep clear
   of the nucleus and a second copy of this expression would drift from it
   (Known-bad: the drum's group velocity, written out three times) */
function nucleusPix(view, halfPix){
  return view === 'foil' ? Math.max(3, halfPix * 0.16) : Math.max(8, halfPix * 0.085);
}
function drawGun(ctx, g, on){
  const x = g.X(0), y = g.Y(-PHET.boxW / 2);
  ctx.fillStyle = on ? shade(COL.live, 0.8) : '#2a2f3d';
  ctx.fillRect(x - 12, y + 3, 24, 15);
  ctx.fillStyle = '#1e222c'; ctx.fillRect(x - 4, y - 2, 8, 6);
  labelIfClear(ctx, x + 17, y + 4, on ? 'the gun, firing' : 'the gun, off',
    COL.dim, '10px -apple-system, sans-serif', 'left', 'top');
}
function drawParticles(ctx, g, M){
  const st = M.st;
  if(st.traces){
    ctx.save(); ctx.strokeStyle = rgba(COL.live, 0.34); ctx.lineWidth = 1;
    for(const p of RUN.ps){
      if(p.trail.length < 4) continue;
      strokeBoxed(ctx, g, p.trail);
    }
    ctx.restore();
  }
  /* everything is clipped to the box: a particle thrown back down the beam
     line leaves through the bottom and was being drawn over the gun and the
     census strip (Known-bad: everything inside a plot box gets clipped) */
  const B = PHET.boxW / 2;
  for(const p of RUN.ps){
    if(Math.abs(p.x) > B || Math.abs(p.y) > B) continue;
    alphaGlyph(ctx, g.X(p.x), g.Y(p.y), clamp(g.s * 1.5, 1.8, 3.4));
  }
}
/* an alpha particle: two protons and two neutrons, PhET's own composition,
   drawn as a four-lobed cluster in the live-marker colour */
function alphaGlyph(ctx, x, y, r){
  disc(ctx, x, y, r * 1.55, rgba(COL.live, 0.9));
  disc(ctx, x - r * 0.45, y - r * 0.45, r * 0.62, '#f2a8ea');
  disc(ctx, x + r * 0.5, y + r * 0.4, r * 0.62, rgba('#ffffff', 0.55));
}

/* --- views 1 and 2: the nuclear and atomic scenes --------------------- */
function drawLive(ctx, W, H, M){
  const G = liveGeo(ctx, W, H, M), g = G.g, st = M.st;
  const bb = box(g.x0, g.y0, G.side, G.side);
  ctx.fillStyle = '#080c16'; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  frame(ctx, bb, '#242a3a');
  /* the atoms */
  for(const a of M.atoms){
    const half = a.L / 2 * g.s;
    /* PhET tracks a particle only inside a box of the atom's own width, and
       it rotates that box to the particle's direction.  Drawn unrotated. */
    ctx.save(); ctx.strokeStyle = rgba(COL.str, 0.22); ctx.lineWidth = 1;
    ctx.setLineDash([3, 4]);
    ctx.strokeRect(g.X(a.x) - half, g.Y(a.y) - half, 2 * half, 2 * half);
    ctx.restore();
    if(M.view === 'foil'){
      ctx.fillStyle = rgba(COL.str, 0.07);
      ctx.beginPath(); ctx.arc(g.X(a.x), g.Y(a.y), half * 0.92, 0, TAU); ctx.fill();
      ring(ctx, g.X(a.x), g.Y(a.y), half * 0.92, rgba(COL.str, 0.3), 1, [2, 3]);
    }
    drawNucleus(ctx, g, a.x, a.y, st.protons, st.neutrons, nucleusPix(M.view, half));
  }
  drawGun(ctx, g, st.gunOn);
  /* the closed form over the most deflected particle in flight */
  if(st.showClosed) drawClosedOver(ctx, g, M);
  drawParticles(ctx, g, M);
  /* scale bar */
  const mPerU = (M.view === 'foil' ? PHET.atomicScaleM : PHET.nuclearScaleM) / PHET.boxW;
  scaleBar(ctx, bb, g, mPerU, M.view === 'foil' ? 'atomic scale' : 'nuclear scale',
           'PhET’s caption');
  if(G.strip) censusStrip(ctx, G.strip, M);
  drawCaption(ctx, G.L);
  return G;
}
function scaleBar(ctx, bb, g, mPerU, name, src){
  const u = PHET.boxW / 4, px = u * g.s;
  const x = bb.x + 12, y = bb.y1 - 16;
  ctx.save(); ctx.strokeStyle = COL.str; ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + px, y);
  ctx.moveTo(x, y - 4); ctx.lineTo(x, y + 4);
  ctx.moveTo(x + px, y - 4); ctx.lineTo(x + px, y + 4);
  ctx.stroke(); ctx.restore();
  label(ctx, x, y - 6, sigf(u * mPerU, 2) + ' m · ' + name + (src ? ' (' + src + ')' : ''),
        COL.dim, '10px -apple-system, sans-serif', 'left', 'bottom');
}
/* the analytic hyperbola of whichever particle is turning the most: drawn
   from the conic, not from the integrated path, so the two can be compared */
function drawClosedOver(ctx, g, M){
  let best = null;
  for(const p of RUN.ps) if(p.ai >= 0 && (!best || p.b0 < best.b0)) best = p;
  if(!best) return;
  const a = M.atoms[best.ai];
  const pts = conicPath(best.b, best.D, PHET.boxW * 0.95, 200);
  const world = [];
  for(let i = 0; i < pts.length; i += 2){
    world.push(a.x + best.ix * pts[i] + best.jx * pts[i + 1],
               a.y + best.iy * pts[i] + best.jy * pts[i + 1]);
  }
  ctx.save(); ctx.strokeStyle = rgba(COL.ref, 0.75); ctx.lineWidth = 1.3;
  ctx.setLineDash([5, 4]);
  strokeBoxed(ctx, g, world);
  ctx.restore();
  /* and its impact parameter, as the perpendicular from the nucleus to the
     incoming asymptote */
  const bx = a.x + best.ix * best.b, by = a.y + best.iy * best.b;
  ctx.save(); ctx.strokeStyle = COL.live; ctx.lineWidth = 1.6; ctx.beginPath();
  ctx.moveTo(g.X(a.x), g.Y(a.y)); ctx.lineTo(g.X(bx), g.Y(by)); ctx.stroke(); ctx.restore();
  /* both labels keep clear of the drawn nucleus: put b beyond the far end of
     its own segment and theta above the nucleus, not on top of it */
  const rN = nucleusPix(M.view, a.L / 2 * g.s);
  const lx = g.X(bx) + best.ix * 7, ly = g.Y(by) - best.iy * 7;
  if(Math.hypot(lx - g.X(a.x), ly - g.Y(a.y)) > rN + 4)
    labelIfClear(ctx, lx, ly, 'b = ' + fmt(best.b, 1), COL.live,
      '10.5px -apple-system, sans-serif', best.ix >= 0 ? 'left' : 'right', 'middle');
  labelIfClear(ctx, g.X(a.x), g.Y(a.y) - rN - 5,
    'θ = ' + fmt(thetaOfB(best.b, best.D) * 180 / PI, 1) + '°',
    COL.ref, '10.5px -apple-system, sans-serif', 'center', 'bottom');
}
/* how the particles that have left the frame were deflected */
function censusStrip(ctx, b, M){
  const h = RUN.hist;
  let tot = 0, mx = 0;
  for(let i = 0; i < NHIST; i++){ tot += h[i]; mx = Math.max(mx, h[i]); }
  panelTitle(ctx, b, 'where they went — ' + fmt(tot, 0) + ' particles off the frame');
  frame(ctx, b, '#242a3a');
  if(tot < 1){
    label(ctx, b.x + b.w / 2, b.y + b.h / 2, 'nothing has left the frame yet',
      COL.dim, '11px -apple-system, sans-serif', 'center', 'middle');
    return;
  }
  for(let i = 0; i < NHIST; i++){
    if(!h[i]) continue;
    const x0 = b.x + b.w * i / NHIST, w = b.w / NHIST - 1;
    const hh = b.h * Math.sqrt(h[i] / mx);
    ctx.fillStyle = i * 180 / NHIST >= 90 ? COL.pos : rgba(COL.str, 0.75);
    ctx.fillRect(x0, b.y1 - hh, Math.max(1, w), hh);
  }
  for(const d of [0, 45, 90, 135, 180]){
    const x = b.x + b.w * d / 180;
    label(ctx, x, b.y1 + 3, fmt(d, 0) + '°', COL.faint,
      '10px -apple-system, sans-serif', d === 0 ? 'left' : (d === 180 ? 'right' : 'center'), 'top');
  }
  label(ctx, b.x + b.w - 4, b.y + 4, 'bar height ∝N · green is past 90°',
    COL.faint, '10px -apple-system, sans-serif', 'right', 'top');
}

/* --- view 3: the plum pudding ---------------------------------------- */
function puddingGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, puddCaption(M), puddCaptionShort(M));
  const avoid = W > 880 ? RO_W + 26 : 10;
  const areaX = 12, areaW = Math.max(180, W - 24 - avoid);
  const gunH = 22;
  const stripH = (L.bot - L.top) > 380 ? 92 : 0;
  const side = Math.max(120, Math.min(areaW, L.bot - L.top - gunH - (stripH ? stripH + 30 : 0)));
  const bx = areaX + (areaW - side) / 2;
  return {L: L, g: mapBox(bx, L.top, side), side: side, gunH: gunH,
          strip: stripH ? box(bx, L.top + side + gunH + 28, side, stripH - 28) : null};
}
function drawPudding(ctx, W, H, M){
  const G = puddingGeo(ctx, W, H, M), g = G.g, st = M.st;
  const bb = box(g.x0, g.y0, G.side, G.side);
  ctx.fillStyle = '#080c16'; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  frame(ctx, bb, '#242a3a');
  /* the pudding: a ball of positive charge with the electrons in it */
  const R = (PHET.boxW / 2) * g.s, cx = g.X(0), cy = g.Y(0);
  /* a canvas gradient records as an object, not a colour string, so the
     display-list audit cannot read it and the rasteriser paints it its
     unparseable-colour magenta -- the whole atom came out solid magenta in
     the first capture.  A flat premixed fill is what the capture can see. */
  ctx.fillStyle = mix(COL.bg, COL.proton, 0.16);
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.fill();
  ring(ctx, cx, cy, R, rgba(COL.proton, 0.55), 1.2);
  const rng = mulberry32(31337);
  const ne = Math.min(st.protons, 96);
  for(let i = 0; i < ne; i++){
    const rr = R * Math.sqrt(rng()) * 0.94, aa = rng() * TAU;
    disc(ctx, cx + rr * Math.cos(aa), cy + rr * Math.sin(aa), Math.max(1.6, R * 0.017), COL.electron);
  }
  labelIfClear(ctx, cx, cy - R - 6, 'Thomson’s atom: ' + fmt(st.protons, 0)
    + ' electrons in a ball of +' + fmt(st.protons, 0) + 'e', COL.dim,
    '11px -apple-system, sans-serif', 'center', 'bottom');
  drawGun(ctx, g, st.gunOn);
  drawParticles(ctx, g, M);
  /* PhET draws no scale on its plum-pudding screen, so this bar must NOT
     claim its caption: the ball here is one real gold atom across. */
  scaleBar(ctx, bb, g, GOLD.rAtom * 2 / PHET.boxW, 'the ball is one gold atom, 2 R');
  if(G.strip) decadeStrip(ctx, G.strip, M);
  drawCaption(ctx, G.L);
  return G;
}
/* the whole argument on one logarithmic angle axis: what Thomson's atom can
   do, what a foil of them can do, and where Rutherford's angles live */
function decadeStrip(ctx, b, M){
  const G = M.gold, st = M.st;
  const lo = Math.log10(Math.max(1e-9, G.thMax / 30)), hi = Math.log10(PI);
  const X = t => b.x + b.w * (Math.log10(Math.max(1e-12, t)) - lo) / (hi - lo);
  panelTitle(ctx, b, 'every deflection on one logarithmic axis, radians');
  frame(ctx, b, '#242a3a');
  ctx.save(); ctx.strokeStyle = '#181d29'; ctx.lineWidth = 1;
  for(let e = Math.ceil(lo); e <= Math.floor(hi); e++){
    const x = X(Math.pow(10, e));
    ctx.beginPath(); ctx.moveTo(x, b.y); ctx.lineTo(x, b.y1); ctx.stroke();
  }
  ctx.restore();
  for(let e = Math.ceil(lo); e <= Math.floor(hi); e++)
    label(ctx, X(Math.pow(10, e)), b.y1 + 3, '10' + supStr(e), COL.faint,
      '10px -apple-system, sans-serif', 'center', 'top');
  const marks = [
    [G.thMax, COL.ref, 'Thomson, one atom (D/2R)', 1],
    [G.thRms, COL.ref, fmt(st.foilNm, 0) + ' nm of Thomson atoms, θrms', 2],
    [electronMaxDeflection(), COL.dim, 'one free electron', 3],
    [thetaOfB(GOLD.rAtom, G.D), COL.pos, 'Rutherford at b = R(atom)', 1],
    [PI / 2, COL.live, '90°', 2],
    [PI * 0.995, COL.live, 'straight back', 3],
  ];
  for(const [t, c, nm, lane] of marks){
    const x = clamp(X(t), b.x, b.x1);
    ctx.save(); ctx.strokeStyle = c; ctx.lineWidth = 1.6;
    ctx.beginPath(); ctx.moveTo(x, b.y + 3); ctx.lineTo(x, b.y1 - 3); ctx.stroke(); ctx.restore();
    const ly = b.y + 5 + (lane - 1) * 13;
    sideLabel(ctx, b, x, ly, nm, c);
  }
}
