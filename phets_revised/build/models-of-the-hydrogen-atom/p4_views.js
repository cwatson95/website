
/* ================================================================== *
 *  drawing helpers, and views 1-2 (the box, the levels)              *
 * ================================================================== */
/* the floating readout covers the top right of the stage (about 300 x 550),
   and the HTML #hint owns the bottom-left corner (bottom:11px, 11px type), so
   every view keeps canvas text out of both (Known-bad, twice). */
const HINT_W = 340, HINT_H = 27;
function usableW(W){ return Math.max(320, W - RO_W - 34); }

/* lay the stage out from the BOTTOM up: measure the caption first, give the
   picture whatever is left (Known-bad: wrapped text has no fixed height).
   The HTML #hint is drawn at bottom:11px in 11 px type and the canvas capture
   cannot see it, so the caption's LAST line has to clear it: HINT_H of extra
   bottom margin, asserted in selfTest (Known-bad, wave-on-a-string). */
function layout(ctx, W, H, full, short){
  /* a narrow stage has to keep 300 px for the picture, or the long caption
     eats the stack and the bottom panel's axis title lands on it */
  /* the caption is capped at the USABLE width, which is the part of the stage
     the floating readout does not cover; at the full stage width it ran under
     the readout at every size below 1400 px */
  const f = fitCaption(ctx, W, H - HINT_H, full, short, usableW(W),
                       stageTop() + (narrowStage(W) ? 300 : 120));
  return {top: stageTop(), capY: f.capY, capW: f.capW, txt: f.txt,
          bot: f.capY - 12, W, H};
}
/* a stage narrower than this cannot carry two panels side by side (the
   floating readout already owns 300 px of it) — every two-panel view stacks
   instead (Known-bad: two-column layouts collapse below ~430 px of column) */
function narrowStage(W){ return usableW(W) < 430; }
/* axes() puts tick labels at +5 and the x-axis title at +21 below the
   frame, in 11 px type: 38 px of clearance under every plot box. */
const AXIS_BOT = 38;
/* how many y ticks a panel of this height can label without the labels
   touching: a 10.5 px label is ~12 px tall, so five ticks need 60 px of frame
   (Known-bad: tick label size follows the tick SPACING) */
function nyFor(h){ return h < 90 ? 2 : (h < 140 ? 3 : 5); }
function drawCaption(ctx, L){
  const lines = wrapText(ctx, L.txt, L.capW, '11.5px -apple-system, sans-serif');
  LABEL_RECTS.push({x: 18, y: L.capY, w: L.capW, h: lines.length * 14});
  caption(ctx, 18, L.capY, L.txt, L.capW, '#767e92');
}
/* two stacked panels that ALWAYS leave AXIS_BOT under the lower one: the
   square shrinks until the plot below it fits, rather than the plot's height
   being clamped and its x-axis title pushed onto the caption */
function stackFit(top, bot, gap, share){
  let side = Math.max(90, Math.min((bot - top) * (share || 0.46), bot - top));
  let bh = bot - AXIS_BOT - (top + side + gap);
  if(bh < 72){ side = Math.max(70, side - (72 - bh)); bh = bot - AXIS_BOT - (top + side + gap); }
  return {side, bh: Math.max(46, bh)};
}
function panelTitle(ctx, b, t){
  LABEL_RECTS.push(labelRect(ctx, b.x, b.y - 9, t, 'italic 13px Georgia, serif', 'left', 'bottom'));
  ctx.textAlign = 'left'; ctx.textBaseline = 'bottom'; ctx.fillStyle = '#aeb6c6';
  ctx.font = 'italic 13px Georgia, serif';
  ctx.fillText(plain(t), b.x, b.y - 9);
}
/* every label this file draws records its rectangle; labelIfClear() then
   refuses to draw one that would land on an existing rectangle, so a crowded
   picture DROPS labels instead of stacking them.  Cleared per draw. */
let LABEL_RECTS = [];
function labelRect(ctx, x, y, t, font, align, base){
  ctx.font = font || '11px -apple-system, sans-serif';
  const w = ctx.measureText(plain(t)).width;
  const mm = /([\d.]+)px/.exec(ctx.font), fs = mm ? parseFloat(mm[1]) : 10, fh = fs * 1.15;
  const lx = align === 'center' ? x - w / 2 : (align === 'right' ? x - w : x);
  const ly = base === 'top' ? y : (base === 'middle' ? y - fh / 2
    : (base === 'bottom' ? y - fh : y - fh * 0.8));
  return {x: lx, y: ly, w, h: fh};
}
/* half a pixel, which is tools/audit.py's threshold.  A 2 px tolerance passed
   the inline sweep and failed the audit on the same picture (Known-bad), and a
   2 px graze is visible antialiased smear on canvas. */
function rectsHit(a, b){
  return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > 0.5
      && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > 0.5;
}
function label(ctx, x, y, t, col, font, align, base){
  LABEL_RECTS.push(labelRect(ctx, x, y, t, font, align, base));
  ctx.fillStyle = col || '#8b93a6';
  ctx.font = font || '11px -apple-system, sans-serif';
  ctx.textAlign = align || 'left'; ctx.textBaseline = base || 'top';
  ctx.fillText(plain(t), x, y);
}
function labelIfClear(ctx, x, y, t, col, font, align, base){
  const r = labelRect(ctx, x, y, t, font, align, base);
  for(const q of LABEL_RECTS) if(rectsHit(r, q)) return false;
  /* the shared legendBox() draws its own text and records it in LEGEND_RECTS,
     not in the label registry — check both, or a dodging label lands on a
     legend (a z score did exactly that at 820x520) */
  for(const q of LEGEND_RECTS) if(rectsHit(r, q)) return false;
  label(ctx, x, y, t, col, font, align, base);
  return true;
}
function disc(ctx, x, y, r, col){
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
}
function ring(ctx, x, y, r, col, lw, dash){
  ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = lw || 1;
  if(dash) ctx.setLineDash(dash);
  ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); ctx.restore();
}
/* a photon: a small coloured disc with four spokes, PhET-ish but new code */
function photonGlyph(ctx, x, y, r, col){
  ctx.save();
  ctx.strokeStyle = col; ctx.lineWidth = 1.4;
  for(let k = 0; k < 4; k++){
    const a = k * PI / 4 + PI / 8;
    ctx.beginPath();
    ctx.moveTo(x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55);
    ctx.lineTo(x + Math.cos(a) * r * 1.5, y + Math.sin(a) * r * 1.5);
    ctx.stroke();
  }
  disc(ctx, x, y, r * 0.75, col);
  ctx.restore();
}

/* ------------------------------------------------------------------ *
 *  view 1 — the box (PhET's Spectra screen)                           *
 * ------------------------------------------------------------------ */
function boxGeo(ctx, W, H, M){
  const st = M.st;
  const L = layout(ctx, W, H, boxCaption(M), boxCaptionShort(M));
  const gunH = 48;
  const availW = usableW(W) - 40;
  /* the light source is a FILL, so neither the audit nor the inline sweep can
     see it land on the spectrometer's title; the title's row is reserved here.
     If the box would then be under 130 px the spectrometer is DROPPED rather
     than the box clamped at a floor it has no room for (Known-bad: a Math.max
     floor does not make a panel fit, it pushes the neighbour off the frame). */
  let spH = st.showSpectro ? Math.min(124, Math.max(56, (L.bot - L.top) * 0.24)) : 0;
  let availH = (spH ? L.bot - spH - 34 : L.bot) - L.top - gunH - 20;
  let dropped = false;
  if(spH && availH < 105){ spH = 0; dropped = true; availH = L.bot - L.top - gunH - 20; }
  const spB = box(20, L.bot - spH, W - 40, spH);
  const side = Math.max(80, Math.min(availH, availW));
  const cx = 20 + availW / 2 + 10, cy = L.top + 10 + side / 2;
  const bb = box(cx - side / 2, cy - side / 2, side, side);
  return {L, spB, bb, cx, cy, side, s: side / PHET.boxSide, gunH, spH, dropped};
}
function boxCaption(M){
  const st = M.st;
  let s = 'PhET&rsquo;s zoomed-in box is 475 model units across. The photon is 15 units wide and travels 300 units a '
    + 'second, the source fires one every 0.0792 s, and the drawn orbits are PhET&rsquo;s compressed ladder '
    + '15, 44, 81, 124, 174, 233 &mdash; every one of those is PhET&rsquo;s value and none is to scale: a real n = 6 '
    + 'orbit is 36 times n = 1, not 15.5 times, and a photon has no size at all.'
    + (st.showExact ? ' The faint green rings are where n&sup2;a&#8320; would put the orbits.' : '');
  if(st.model === 'classical') s += ' The spiral is PhET&rsquo;s: the radius falls 220 units a second and the '
    + 'angular speed is multiplied by 1.008 every frame, so the atom dies in 0.67 s.';
  else if(st.model === 'pudding') s += ' Plum pudding emits one wavelength only, 150 nm, which PhET chose; a real '
    + 'oscillator would emit at its own frequency.';
  else if(st.model === 'billiard') s += ' A hard sphere can only scatter: nothing here ever changes colour.';
  else if(M.quantum) s += ' Absorption needs the photon&rsquo;s wavelength to be exactly one of PhET&rsquo;s '
    + 'fifteen integers, and PhET makes the atom wait 0.75 s before it will absorb and 1 s before it will emit.';
  return s;
}
function boxCaptionShort(M){
  return 'PhET&rsquo;s box, 475 units across; the photon size, speed and the orbit radii are PhET&rsquo;s and are '
    + 'not to scale. On a stage this small the spectrometer is dropped and the box keeps the room.';
}

function drawBox(ctx, W, H, M){
  const st = M.st, G = boxGeo(ctx, W, H, M), bb = G.bb, s = G.s;
  drawCaption(ctx, G.L);
  /* the spectrometer's title is mandatory, so it goes down before the gun
     label, which is the one that has to move out of the way */
  if(G.spH) drawSpectrometer(ctx, G.spB, M);
  const X = u => G.cx + u * s, Y = v => G.cy - v * s;
  /* the box */
  ctx.fillStyle = '#0a0d16'; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  frame(ctx, bb, '#2a3242');
  /* the beam and the light source */
  const gy = bb.y1 + 8, gh = G.gunH - 12;
  const beamCol = !st.lightOn ? '#1a1f2b'
    : (st.light === 'white' ? 'rgba(235,238,246,0.10)' : rgba(lamColour(st.lam), 0.16));
  ctx.fillStyle = beamCol; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  const gw = Math.min(120, bb.w * 0.32);
  ctx.fillStyle = st.lightOn ? (st.light === 'white' ? '#e9ecf4' : lamColour(st.lam)) : '#3a4050';
  ctx.fillRect(G.cx - gw / 2, gy, gw, gh);
  frame(ctx, box(G.cx - gw / 2, gy, gw, gh), '#4a5164');
  labelIfClear(ctx, G.cx + gw / 2 + 9, gy + gh / 2, st.lightOn
    ? (st.light === 'white' ? 'white light' : fmt(st.lam, 0) + ' nm, ' + bandOf(st.lam))
    : 'light source off', '#8b93a6', '11px -apple-system, sans-serif', 'left', 'middle');
  /* the model name and year go down BEFORE the atom, so the Experiment's "?"
     has something to dodge */
  label(ctx, bb.x + 10, bb.y + 8, M.name + (MODEL_LIST.filter(o => o.id === st.model)[0].year
    ? '  ' + MODEL_LIST.filter(o => o.id === st.model)[0].year : ''),
    '#cfd4de', 'italic 15px Georgia, serif', 'left', 'top');
  /* the claim is 55 characters: below 280 px of box it is three times as wide
     as the thing it labels, and the control panel carries it anyway */
  if(bb.w >= 280) labelIfClear(ctx, bb.x + 10, bb.y + 28, MODEL_CLAIM[st.model], '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');
  /* the atom */
  ctx.save();
  ctx.beginPath(); ctx.rect(bb.x, bb.y, bb.w, bb.h); ctx.clip();
  drawAtomInBox(ctx, M, G, X, Y);
  for(const p of M.photons){
    const col = lamColour(p.lam);
    photonGlyph(ctx, X(p.x), Y(p.y), Math.max(3, PHET.photonRadius * s * 0.5), col);
  }
  ctx.restore();
}
const MODEL_CLAIM = {
  billiard: 'a hard sphere: light bounces, nothing is absorbed',
  pudding: 'an electron in a ball of positive jelly: one line, at 150 nm (PhET)',
  classical: 'a charge in orbit radiates: the atom collapses in 0.67 s',
  bohr: 'only certain orbits, and light on the gaps between them',
  debroglie: 'the orbits are standing waves of the electron',
  schrodinger: 'a probability cloud with quantum numbers n, l, m',
  experiment: 'a real box of hydrogen: you see only what comes out',
};
/* PhET draws a fat proton; at 8 x 1.6 view units it covered its own n = 1
   orbit (15 units) completely.  7 units across is still generous and leaves
   the ground-state orbit visible. */
function protonR(s){ return Math.max(3, 7 * s); }
/* PhET draws a fat proton; at 8 x 1.6 view units it covered its own n = 1
   orbit (15 units) completely.  7 units across is still generous and leaves
   the ground-state orbit visible. */
function protonR(s){ return Math.max(3, 7 * s); }
function drawAtomInBox(ctx, M, G, X, Y){
  const st = M.st, s = G.s;
  const px = X(0), py = Y(0);
  if(st.model === 'billiard'){
    const r = PHET.billiardR * s;
    disc(ctx, px, py, r, COL.ball);
    disc(ctx, px - r * 0.3, py - r * 0.3, r * 0.34, '#ff8d15');
    return;
  }
  if(st.model === 'pudding'){
    const r = PHET.puddingR * s;
    disc(ctx, px, py, r, 'rgba(176,107,224,0.30)');
    ring(ctx, px, py, r, COL.pudding, 1.4);
    const [ex, ey] = electronXY(st);
    disc(ctx, X(ex), Y(ey), Math.max(3, PHET.electronRadius * s), COL.electron);
    return;
  }
  if(st.model === 'classical'){
    disc(ctx, px, py, protonR(s), COL.proton);
    if(!M.dead){
      const [ex, ey] = electronXY(st);
      /* the path it has already run down, integrated BACKWARDS through the
         exact inverse of the forward step (r += dr, a += w dt, w /= spin).
         Running it forwards from r_0 with today's angular speed drew an arc of
         something that never happened. */
      ctx.strokeStyle = rgba(COL.struct, 0.35); ctx.lineWidth = 1;
      ctx.beginPath();
      let br = ATOM.cls.r, ba = ATOM.cls.a, bw = ATOM.cls.w;
      for(let k = 0; k <= ATOM.ticks; k++){
        const xx = X(br * Math.cos(ba)), yy = Y(br * Math.sin(ba));
        if(k === 0) ctx.moveTo(xx, yy); else ctx.lineTo(xx, yy);
        bw /= PHET.classicalSpin;
        br += PHET.classicalDrdt * DT_TICK;
        ba += bw * DT_TICK;
        if(br > PHET.classicalR0) break;
      }
      ctx.stroke();
      disc(ctx, X(ex), Y(ey), Math.max(3, PHET.electronRadius * s), COL.electron);
    } else {
      label(ctx, px, py + 18 * s + 6, 'the atom has collapsed', COL.ref,
        '12px -apple-system, sans-serif', 'center', 'top');
    }
    return;
  }
  /* the quantum models */
  if(st.model === 'experiment'){
    disc(ctx, px, py, protonR(s), COL.proton);
    /* above the proton if there is room, below it if the model name is there */
    if(!labelIfClear(ctx, px, py - 26, '?', '#cfd4de', 'bold 34px -apple-system, sans-serif', 'center', 'middle'))
      labelIfClear(ctx, px, py + 26, '?', '#cfd4de', 'bold 34px -apple-system, sans-serif', 'center', 'middle');
    return;
  }
  /* the orbits */
  for(let n = 1; n <= NMAX; n++){
    ring(ctx, px, py, viewRadius(n) * s, n === M.n ? rgba(COL.struct, 0.8) : 'rgba(90,200,224,0.22)',
      n === M.n ? 1.4 : 1, [3, 3]);
  }
  if(st.showExact) for(let n = 1; n <= NMAX; n++){
    const rr = trueViewRadius(n) * s;
    if(rr < G.side / 2) ring(ctx, px, py, rr, 'rgba(184,236,76,0.34)', 1, [1, 4]);
  }
  disc(ctx, px, py, protonR(s), COL.proton);
  if(st.model === 'debroglie') drawDeBroglieRing(ctx, M, px, py, viewRadius(M.n) * s, s);
  else if(st.model === 'schrodinger') drawCloudSmall(ctx, M, px, py, G.side);
  else {
    const [ex, ey] = electronXY(st);
    disc(ctx, X(ex), Y(ey), Math.max(3, PHET.electronRadius * s), COL.electron);
  }
}
/* de Broglie's three PhET representations, drawn on a ring of radius R px */
function drawDeBroglieRing(ctx, M, px, py, R, s){
  const st = M.st, n = M.n;
  if(st.dbRep === 'radial'){
    ctx.strokeStyle = COL.electron; ctx.lineWidth = 2;
    ctx.beginPath();
    const amp = 0.45 * viewRadius(1) * s;
    for(let k = 0; k <= 200; k++){
      const a = TAU * k / 200, rr = R + amp * dbAmplitude(n, a);
      const x = px + rr * Math.cos(a), y = py - rr * Math.sin(a);
      if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.closePath(); ctx.stroke();
    return;
  }
  if(st.dbRep === 'bright'){
    const thick = Math.max(2, PHET.dbRingThick * s);
    const N = Math.max(24, Math.round(PI * 2 * R / 3) + 1);
    for(let k = 0; k < N; k++){
      const a0 = TAU * k / N, a1 = a0 + TAU / N + 0.002;
      const amp = dbAmplitude(n, a0);
      /* pre-mixed against the page so abutting quads can be drawn OPAQUE
         (Known-bad: an overlap under globalAlpha composites twice) */
      const col = amp >= 0 ? mix('#1b2434', COL.electron, clamp(amp, 0, 1))
                           : mix('#1b2434', '#070b18', clamp(-amp, 0, 1));
      ctx.fillStyle = col;
      ctx.beginPath();
      ctx.moveTo(px + (R - thick) * Math.cos(a0), py - (R - thick) * Math.sin(a0));
      ctx.lineTo(px + (R + thick) * Math.cos(a0), py - (R + thick) * Math.sin(a0));
      ctx.lineTo(px + (R + thick) * Math.cos(a1), py - (R + thick) * Math.sin(a1));
      ctx.lineTo(px + (R - thick) * Math.cos(a1), py - (R - thick) * Math.sin(a1));
      ctx.closePath(); ctx.fill();
    }
    return;
  }
  /* 3-D height: the ring seen at PhET's 0.35 y-squash, the amplitude lifted */
  const ys = PHET.db3dYScale, hgt = 0.42 * viewRadius(1) * s;
  ctx.strokeStyle = 'rgba(90,200,224,0.35)'; ctx.lineWidth = 1;
  ctx.beginPath();
  for(let k = 0; k <= 160; k++){
    const a = TAU * k / 160;
    const x = px + R * Math.cos(a), y = py - ys * R * Math.sin(a);
    if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.closePath(); ctx.stroke();
  ctx.strokeStyle = COL.electron; ctx.lineWidth = 2;
  ctx.beginPath();
  for(let k = 0; k <= 200; k++){
    const a = TAU * k / 200;
    const x = px + R * Math.cos(a), y = py - ys * R * Math.sin(a) - hgt * dbAmplitude(n, a);
    if(k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.closePath(); ctx.stroke();
}
/* the Schrodinger cloud, small, inside the box */
function drawCloudSmall(ctx, M, px, py, side){
  const n = M.n, l = M.l, m = M.m;
  const G = 44, rmax = cloudExtent(n, l);
  const cg = cloudGrid(n, l, m, G, rmax);
  /* the cloud has to GROW with n, or it contradicts the orbit ladder drawn
     behind it: <r> is put on PhET's drawn radius for this n and the rest of
     the cloud follows that scale */
  const pxPerA0 = viewRadius(n) * (side / PHET.boxSide) / meanR(n, l);
  const half = Math.min(side * 0.47, rmax * pxPerA0);
  const cell = 2 * half / G;
  for(let j = 0; j < G; j++) for(let i = 0; i < G; i++){
    const v = cg.mx > 0 ? cg.g[j * G + i] / cg.mx : 0;
    if(v < 0.004) continue;
    ctx.fillStyle = mix('#0a0d16', COL.electron, Math.pow(v, 0.45));
    ctx.fillRect(px - half + i * cell - 0.4, py - half + j * cell - 0.4, cell + 0.8, cell + 0.8);
  }
}

/* the spectrometer: PhET's three segments (UV compressed, visible true, IR
   compressed) with the compression printed on the axis */
const UV_MAP = [[94, 94], [95, 95], [97, 97], [103, 100], [122, 105], [150, 112]];
const IR_MAP = [[1094, 1094], [1282, 1282], [1876, 1650], [2626, 2200], [4052, 3000], [7460, 4000]];
function segPos(lam){
  /* returns [segment, fraction 0..1] — PhET's own mapping, read from its
     SpectrometerChartSegment */
  if(lam < 380){
    let v = lam;
    for(const [a, b] of UV_MAP) if(a === lam) v = b;
    return [0, (v - 93) / (113 - 93)];
  }
  if(lam <= 780) return [1, (lam - 380) / (780 - 380)];
  let v = lam;
  for(const [a, b] of IR_MAP) if(a === lam) v = b;
  return [2, (v - 900) / (4200 - 900)];
}
function drawSpectrometer(ctx, b, M){
  const st = M.st;
  const gap = 10;
  const wTot = b.w - 2 * gap;
  const ws = [wTot * 0.42, wTot * 0.22, wTot * 0.36];
  const xs = [b.x, b.x + ws[0] + gap, b.x + ws[0] + ws[1] + 2 * gap];
  const axisY = b.y1 - 26;
  const names = ['UV (compressed)', 'visible (true scale)', 'IR (compressed)'];
  let maxC = 1;
  for(const k in M.counts) maxC = Math.max(maxC, M.counts[k]);
  for(let s = 0; s < 3; s++){
    ctx.fillStyle = s === 1 ? '#151a26' : '#12151f';
    ctx.fillRect(xs[s], b.y, ws[s], axisY - b.y + 4);
    if(s === 1){
      for(let i = 0; i < 40; i++){
        const lam = 380 + (780 - 380) * (i + 0.5) / 40;
        ctx.fillStyle = mix('#12151f', lamColour(lam), 0.30);
        ctx.fillRect(xs[s] + ws[s] * i / 40, axisY, ws[s] / 40 + 0.6, 4);
      }
    } else {
      ctx.fillStyle = s === 0 ? '#3c4150' : '#463c36';
      ctx.fillRect(xs[s], axisY, ws[s], 4);
    }
    label(ctx, xs[s] + ws[s] / 2, axisY + 8, names[s], '#6f7789',
      '10px -apple-system, sans-serif', 'center', 'top');
  }
  /* every line PhET's model can make, as a faint tick; the counts as bars */
  const all = PHET_LAMS.concat([PHET.puddingLam]);
  for(const lam of all){
    const [s, f] = segPos(lam);
    const x = xs[s] + clamp(f, 0, 1) * ws[s];
    ctx.strokeStyle = 'rgba(140,150,170,0.30)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x, axisY); ctx.lineTo(x, axisY - 5); ctx.stroke();
    const c = M.counts[lam] || 0;
    if(c > 0){
      const hgt = (axisY - b.y - 6) * (st.logCount ? Math.log10(1 + c) / Math.log10(1 + maxC)
                                                   : c / maxC);
      ctx.fillStyle = lamColour(lam);
      ctx.fillRect(x - 2.5, axisY - hgt, 5, hgt);
      if(c === maxC) labelIfClear(ctx, x, axisY - hgt - 12, lam + ' nm', lamColour(lam),
        '10px -apple-system, sans-serif', 'center', 'top');
    }
  }
  label(ctx, b.x, b.y - 13, b.w < 620
    ? 'spectrometer' + (st.logCount ? ', log counts' : '') + ': ' + M.emitted + ' photons'
    : 'spectrometer &mdash; photons emitted per wavelength'
      + (st.logCount ? ' (log counts)' : '') + '; ' + M.emitted + ' so far',
    '#aeb6c6', 'italic 12.5px Georgia, serif', 'left', 'bottom');
}

/* ------------------------------------------------------------------ *
 *  view 2 — the levels (PhET's Energy Levels screen)                  *
 * ------------------------------------------------------------------ */
function levelsGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, levelsCaption(M), 'PhET compresses the level ladder so n = 2 to 6 are visible; the true spacing is beside it.');
  const top = L.top + 26, bot = L.bot - 24;
  const uw = usableW(W);
  if(narrowStage(W)){
    /* no room for the live box as well as the two ladders: the box is the one
       the first view already shows, so it goes */
    const pw2 = Math.max(90, (uw - 70) / 2);
    const a2 = box(56, top, pw2, bot - top);
    const b2 = box(a2.x1 + 44, top, pw2, bot - top);
    return {L, a: a2, b: b2, c: null, side: 0, narrow: true};
  }
  const pw = Math.max(120, (uw - 60) * 0.42);
  const a = box(56, top, pw, bot - top);
  const bx = box(a.x1 + 54, top, pw, bot - top);
  const side = Math.max(90, Math.min(bot - top, W - bx.x1 - 40));
  const c = box(Math.min(W - side - 20, bx.x1 + 28), bot - side, side, side);
  return {L, a, b: bx, c, side};
}
function levelsCaption(M){
  return 'Left: the ladder as PhET draws it &mdash; its level heights are 0.025, 0.6, 0.73, 0.81, 0.86 and 0.9 of '
    + 'the axis, chosen so that n = 2 to 6 are far enough apart to click on. Middle: the same six levels at their true '
    + 'energies, &minus;13.598287 eV / n&sup2;, where n = 2 to 6 crowd into the top quarter and everything above n = 6 '
    + 'piles onto the ionisation line. Right: the atom that is making the transitions, in the same box as the first '
    + 'view. The squiggle is the photon that just went in or out, drawn in its own colour.';
}
function drawLevels(ctx, W, H, M){
  const st = M.st, G = levelsGeo(ctx, W, H, M);
  drawCaption(ctx, G.L);
  drawLadder(ctx, G.a, M, false);
  drawLadder(ctx, G.b, M, true);
  if(!G.c) return;
  /* the live box */
  const bb = G.c;
  ctx.fillStyle = '#0a0d16'; ctx.fillRect(bb.x, bb.y, bb.w, bb.h);
  frame(ctx, bb, '#2a3242');
  const s = bb.w / PHET.boxSide, cx = bb.x + bb.w / 2, cy = bb.y + bb.h / 2;
  ctx.save(); ctx.beginPath(); ctx.rect(bb.x, bb.y, bb.w, bb.h); ctx.clip();
  drawAtomInBox(ctx, M, {cx, cy, s, side: bb.w}, u => cx + u * s, v => cy - v * s);
  for(const p of M.photons) photonGlyph(ctx, cx + p.x * s, cy - p.y * s,
    Math.max(2.5, PHET.photonRadius * s * 0.5), lamColour(p.lam));
  ctx.restore();
  panelTitle(ctx, bb, 'the atom');
}
function drawLadder(ctx, b, M, trueAxis){
  const st = M.st;
  ctx.fillStyle = '#0a0d16'; ctx.fillRect(b.x, b.y, b.w, b.h);
  frame(ctx, b, '#242a3a');
  /* a 26-character title does not fit a 130 px panel, and the two ran into
     each other at 560x380 */
  panelTitle(ctx, b, b.w < 200 ? (trueAxis ? 'true' : 'PhET&rsquo;s')
                               : (trueAxis ? 'the true ladder' : 'PhET&rsquo;s ladder (compressed)'));
  /* the Schrodinger diagram carries an "l = 0 1 2 ..." legend along the
     bottom, which is exactly where n = 1 lands on PhET's compressed axis */
  const foot = (st.model === 'schrodinger') ? 28 : 16;
  const yOf = n => trueAxis ? b.y1 - foot - (b.h - 24 - foot) * (1 - 1 / (n * n))
                            : b.y1 - foot - (b.h - 24 - foot) * PHET.levelY[n - 1];
  /* the energy axis */
  ctx.strokeStyle = '#3a4152'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(b.x + 26, b.y1 - 12); ctx.lineTo(b.x + 26, b.y + 12); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(b.x + 26, b.y + 12); ctx.lineTo(b.x + 22, b.y + 20);
  ctx.lineTo(b.x + 30, b.y + 20); ctx.closePath(); ctx.fillStyle = '#3a4152'; ctx.fill();
  ctx.save(); ctx.translate(b.x + 13, b.y + b.h / 2); ctx.rotate(-PI / 2);
  ctx.fillStyle = '#8b93a6'; ctx.font = '11px -apple-system, sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
  ctx.fillText('energy', 0, 0);          /* rotated: not registered, see labelRect */
  ctx.restore();
  const x0 = b.x + 36, x1 = b.x1 - 14;
  let lastLabY = -1e9, labelled = 0;
  const schro = (st.model === 'schrodinger');
  const lw = schro ? Math.min(26, (x1 - x0 - 30) / NMAX) : (x1 - x0 - 34);
  for(let n = 1; n <= NMAX; n++){
    const y = yOf(n);
    ctx.strokeStyle = n === M.n && st.model !== 'experiment' ? COL.pos : '#7f8798';
    ctx.lineWidth = n === M.n && st.model !== 'experiment' ? 2 : 1;
    if(schro){
      for(let l = 0; l < n; l++){
        ctx.beginPath();
        ctx.moveTo(x0 + l * (lw + 4), y); ctx.lineTo(x0 + l * (lw + 4) + lw, y); ctx.stroke();
      }
    } else {
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x0 + lw, y); ctx.stroke();
    }
  }
  /* The labels go down in ONE pass through labelIfClear, occupied level first
     so that it wins the space.  Nothing is exempt: exempting the electron's own
     level put "n=6" on top of "n=5" on the true ladder of the Experiment model,
     which has no visible electron at all. */
  const labOrder = [];
  if(st.model !== 'experiment') labOrder.push(M.n);
  for(let n = 1; n <= NMAX; n++) if(labOrder.indexOf(n) < 0) labOrder.push(n);
  for(const n of labOrder){
    const y = yOf(n);
    const live = (n === M.n && st.model !== 'experiment');
    if(labelIfClear(ctx, x1 + 1, y, 'n=' + n, live ? COL.pos : '#6f7789',
        '10.5px -apple-system, sans-serif', 'right', 'middle')){
      lastLabY = y; labelled++;
    }
    /* below 150 px of panel there is no room between the energy axis and the
       level lines for a value, and it lands on the rotated axis title */
    if(trueAxis && b.w >= 150) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');
  }
  if(labelled < NMAX) labelIfClear(ctx, x0, b.y + 30,
    (NMAX - labelled) + (NMAX - labelled === 1 ? ' level' : ' levels') + ' too close to label',
    '#6f7789', '10px -apple-system, sans-serif', 'left', 'top');
  /* the ionisation line */
  const yInf = trueAxis ? b.y1 - foot - (b.h - 24 - foot) : b.y + 16;
  ctx.save(); ctx.strokeStyle = 'rgba(232,132,58,0.55)'; ctx.lineWidth = 1; ctx.setLineDash([4, 3]);
  ctx.beginPath(); ctx.moveTo(x0 - 6, yInf); ctx.lineTo(x1, yInf); ctx.stroke(); ctx.restore();
  label(ctx, x0 - 6, yInf - 3, 'ionised, E = 0', COL.ref, '10px -apple-system, sans-serif', 'left', 'bottom');
  if(schro){
    /* the spaced-out form is 90 px wide and ran past a 130 px panel */
    label(ctx, x0, b.y1 - 12, b.w < 200 ? 'l = 0 to 5' : 'l = 0   1   2   3   4   5', '#6f7789',
      '10px -apple-system, sans-serif', 'left', 'top');
  }
  /* the electron */
  if(st.model === 'experiment'){
    label(ctx, b.x + b.w / 2, b.y + b.h / 2, '?', '#cfd4de',
      'bold 54px -apple-system, sans-serif', 'center', 'middle');
    return;
  }
  const ex = schro ? x0 + M.l * (lw + 4) + lw / 2 : x0 + lw / 2;
  disc(ctx, ex, yOf(M.n) - 6, 4.5, COL.live);
  /* the squiggle for the last transition */
  const sq = M.squiggle;
  if(sq && sq.age < 1.6){
    const y1 = yOf(sq.from.n), y2 = yOf(sq.to.n);
    const xx = schro ? x0 + sq.to.l * (lw + 4) + lw / 2 : x0 + lw / 2;
    const x2 = schro ? x0 + sq.from.l * (lw + 4) + lw / 2 : x0 + lw / 2;
    ctx.save();
    ctx.strokeStyle = lamColour(sq.lam); ctx.lineWidth = 1.6;
    ctx.beginPath();
    const N = 40, amp = 5;
    for(let k = 0; k <= N; k++){
      const t = k / N, yy = y1 + (y2 - y1) * t, xb = x2 + (xx - x2) * t;
      const x = xb + 26 + amp * Math.sin(t * 9 * PI);
      if(k === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy);
    }
    ctx.stroke(); ctx.restore();
    label(ctx, x2 + 40, (y1 + y2) / 2, sq.lam + ' nm', lamColour(sq.lam),
      '10px -apple-system, sans-serif', 'left', 'middle');
  }
}
