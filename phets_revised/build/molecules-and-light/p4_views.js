
/* ================================================================== *
 *  views A and B: the chamber, the spectrum                           *
 * ================================================================== */
/* the house #hint (HTML, bottom:11px, 11px type) sits on the last line of a
   caption anchored at H - 12: every caption here ends HINT_H higher, clear of
   it (lineage: build/wave-on-a-string via build/molecule-polarity) */
const HINT_H = 18;
const SMALL = '10.5px -apple-system, sans-serif';
/* stageLayout floors the main box at 80 px; on a short stage that floor
   pushes the main panel over the bottom row and the text collides.  When
   the floor bites, lay the stage out again with NO bottom row -- one
   honest panel beats two overlapping ones. */
function stage(ctx, W, H, capFull, capShort, nB, frac, nBn) {
  const L = stageLayout(ctx, W, H - HINT_H, capFull, capShort, nB, frac, nBn);
  if (L.bottom.length && L.main.h <= 82)
    return stageLayout(ctx, W, H - HINT_H, capShort, capShort, 0, frac, 0);
  return L;
}
const TITLE_FONT = 'italic 13px Georgia, serif';
let PICKS = [];                 /* draggable targets of the last draw */

/* PhET's model units -> pixels, equal scale on both axes (the molecule is a
   SHAPE, so its two axes must share a scale -- the Known-bad rule) */
const CHAMBER_X = 1620, CHAMBER_Y = 560;
function chamberMap(b) {
  const XLO = -CHAMBER_X, XHI = CHAMBER_X;
  const s = Math.min(b.w / (XHI - XLO), b.h / (2 * CHAMBER_Y));
  return {s, cx: b.x + b.w / 2, cy: b.y + b.h / 2,
          X: x => b.x + b.w / 2 + x * s, Y: y => b.y + b.h / 2 - y * s};
}
/* one molecule, drawn from PhET's offsets with the given per-atom shift */
function drawMolecule(ctx, map, mol, off, rot, cx, cy, glow, alpha) {
  const G = PHET_GEOM[mol];
  if (!G) return;
  const ca = Math.cos(rot || 0), sa = Math.sin(rot || 0);
  const pos = G.atoms.map((a, i) => {
    const dx = (off && off[i]) ? off[i][0] : 0, dy = (off && off[i]) ? off[i][1] : 0;
    const x = a[1] + dx, y = a[2] + dy;
    return [(cx || 0) + x * ca - y * sa, (cy || 0) + x * sa + y * ca, a[0]];
  });
  ctx.globalAlpha = alpha === undefined ? 1 : alpha;
  if (glow > 0) {
    let mx = 0;
    for (const p of pos) mx = Math.max(mx, Math.hypot(p[0] - (cx || 0), p[1] - (cy || 0)));
    const r = (mx + 110) * map.s;
    ctx.fillStyle = rgba(COL.glow, 0.10 + 0.20 * glow);
    ctx.beginPath();
    ctx.arc(map.X(cx || 0), map.Y(cy || 0), r, 0, TAU);
    ctx.fill();
  }
  for (const [i, j, order] of G.bonds) {
    const a = pos[i], c = pos[j];
    const nx = -(c[1] - a[1]), ny = c[0] - a[0];
    const L = Math.hypot(nx, ny) || 1;
    const sep = 20;
    for (let k = 0; k < order; k++) {
      const t = (k - (order - 1) / 2) * sep;
      ctx.beginPath();
      ctx.moveTo(map.X(a[0] + nx / L * t), map.Y(a[1] + ny / L * t));
      ctx.lineTo(map.X(c[0] + nx / L * t), map.Y(c[1] + ny / L * t));
      ctx.strokeStyle = COL.bond;
      ctx.lineWidth = Math.max(1.2, 9 * map.s);
      ctx.stroke();
    }
  }
  for (const p of pos) {
    const el = p[2], r = PHET_ATOM[el].r * map.s;
    ctx.beginPath();
    ctx.arc(map.X(p[0]), map.Y(p[1]), Math.max(2.5, r), 0, TAU);
    ctx.fillStyle = shade(ELCOL[el], 0.86);
    ctx.fill();
    ctx.strokeStyle = shade(ELCOL[el], 1);
    ctx.lineWidth = 1.2;
    ctx.stroke();
    if (r > 9) {
      ctx.fillStyle = '#0b0e16';
      ctx.font = 'bold ' + Math.round(Math.min(15, r * 0.95)) + 'px -apple-system, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(el, map.X(p[0]), map.Y(p[1]));
    }
  }
  ctx.globalAlpha = 1;
}
/* the light source: a lamp body and a cone, drawn as explicit polygons in
   device coordinates (the display-list recorder has no ellipse, and a scaled
   arc does not survive restore()) */
function drawLamp(ctx, map, on, col) {
  const x0 = map.X(PHET.EMITTER_X - 210), x1 = map.X(PHET.EMITTER_X + 40);
  const yc = map.Y(0), hh = Math.max(10, 150 * map.s);
  ctx.fillStyle = on ? shade(col, 0.5) : '#161b26';
  ctx.strokeStyle = on ? col : '#2a2f3d';
  ctx.lineWidth = 1.4;
  ctx.beginPath();
  ctx.moveTo(x0, yc - hh * 0.62);
  ctx.lineTo(x1 - hh * 0.5, yc - hh * 0.62);
  ctx.lineTo(x1, yc - hh);
  ctx.lineTo(x1, yc + hh);
  ctx.lineTo(x1 - hh * 0.5, yc + hh * 0.62);
  ctx.lineTo(x0, yc + hh * 0.62);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  if (on) {
    ctx.fillStyle = rgba(col, 0.07);
    ctx.beginPath();
    ctx.moveTo(x1, yc - hh * 0.55);
    ctx.lineTo(map.X(CHAMBER_X - 20), yc - hh * 0.8);
    ctx.lineTo(map.X(CHAMBER_X - 20), yc + hh * 0.8);
    ctx.lineTo(x1, yc + hh * 0.55);
    ctx.closePath();
    ctx.fill();
  }
}
function drawChamber(ctx, W, H, M) {
  const capFull = 'PhET&rsquo;s screen, remade. The source fires photons of one wavelength to the right; the '
    + 'molecule sits at the origin and every photon inside ' + PHET.ABSORB_RADIUS + ' model units of it gets exactly '
    + 'one absorption trial, at probability one half. Both axes share a scale &mdash; the molecule is a shape, so '
    + 'nothing here is exaggerated. The strip underneath is the molecule&rsquo;s state against time.';
  const capShort = 'PhET&rsquo;s screen: one absorption trial per photon at p = &frac12;. Equal scale on both axes.';
  const L = stage(ctx, W, H, capFull, capShort, 1, 0.26, 1);
  const b = L.main;
  const map = chamberMap(b);
  /* frame the MODEL window, at its own aspect, rather than the whole stage
     box: the frame then means something -- it is the observation window */
  const win = box(map.X(-CHAMBER_X), map.Y(CHAMBER_Y),
                  2 * CHAMBER_X * map.s, 2 * CHAMBER_Y * map.s);
  frame(ctx, win, COL.edge);
  const col = BANDCOL[M.band];
  drawLamp(ctx, map, ST.source, col);
  /* the absorption radius */
  if (ST.showRadius) {
    ctx.beginPath();
    ctx.arc(map.X(0), map.Y(0), PHET.ABSORB_RADIUS * map.s, 0, TAU);
    ctx.strokeStyle = rgba(COL.struct, 0.55);
    ctx.lineWidth = 1;
    ctx.setLineDash([4, 4]);
    ctx.stroke();
    ctx.setLineDash([]);
    lab(ctx, W, H, map.X(0), map.Y(0) - PHET.ABSORB_RADIUS * map.s - 6,
        'absorption radius ' + PHET.ABSORB_RADIUS, COL.struct, SMALL, 'center', 'bottom');
  }
  /* the photons */
  for (const p of CH.photons) {
    const x = map.X(p.x), y = map.Y(p.y);
    if (x < win.x || x > win.x1 || y < win.y || y > win.y1) continue;
    const tl = 0.012;
    ctx.beginPath();
    ctx.moveTo(map.X(p.x - p.vx * tl), map.Y(p.y - p.vy * tl));
    ctx.lineTo(x, y);
    ctx.strokeStyle = rgba(col, p.pass ? 0.35 : 0.75);
    ctx.lineWidth = 2;
    ctx.stroke();
    dot(ctx, x, y, 3.6, p.pass ? shade(col, 0.55) : col, null, 0);
  }
  /* the molecule, or its pieces */
  let gone = 0;
  if (CH.state === 'broken' && CH.frags) {
    for (const f of CH.frags) {
      if (Math.abs(f.x) > CHAMBER_X + 200 || Math.abs(f.y) > CHAMBER_Y + 200) { gone++; continue; }
      drawMolecule(ctx, map, f.mol, null, f.rot, f.x, f.y, 0, 0.9);
    }
    if (gone) lab(ctx, W, H, map.X(0), map.Y(260),
        gone === CH.frags.length
          ? 'the pieces have left the window — press "reset molecule" to put it back'
          : gone + ' piece has left the window',
        COL.ref, SMALL, 'center', 'middle');
  } else {
    const kind = ST.anim;
    let off = null;
    if (CH.state === 'vib') off = drawOffsets(M.mol, kind, CH.vibPhase, 55);
    drawMolecule(ctx, map, M.mol, off, CH.rot, 0, 0,
                 CH.state === 'glow' ? 1 : 0, 1);
  }
  /* what PhET says is happening */
  const say = CH.state === 'broken' ? 'broken apart'
    : CH.state === 'idle' ? (M.resp ? 'waiting for a photon' : 'transparent to this band')
    : RESPNAME[M.resp];
  lab(ctx, W, H, win.x + 10, win.y + 8,
      MOLNAME[M.mol] + ' · ' + BANDNAME[M.band] + ' → ' + say,
      M.resp ? COL.pos : COL.dim, TITLE_FONT, 'left', 'top');
  if (CH.state === 'vib') {
    lab(ctx, W, H, win.x + 10, win.y + 26,
        ST.anim === 'phet' ? 'PhET’s own animation (hand-picked offsets, not a normal mode)'
                           : 'the derived normal mode, at its true displacement ratios',
        ST.anim === 'phet' ? COL.ref : COL.pos, SMALL, 'left', 'top');
  }
  /* a scale bar, in PhET's model units */
  const sbl = 500 * map.s;
  ctx.strokeStyle = COL.dim;
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(win.x1 - 20 - sbl, win.y1 - 16);
  ctx.lineTo(win.x1 - 20, win.y1 - 16);
  ctx.stroke();
  lab(ctx, W, H, win.x1 - 20 - sbl / 2, win.y1 - 20, '500 PhET model units', COL.dim, SMALL, 'center', 'bottom');
  /* the state strip */
  if (L.bottom.length) {
    const s = L.bottom[0];
    const t1 = Math.max(6, CH.t), t0 = Math.max(0, t1 - 24);
    axesR(ctx, s, t0, t1, 0, 1, {title: titleFor(s, 'the molecule’s state against time', 'state vs time'),
                                 xlab: 'time (s)', ny: 2, yfmt: () => ''});
    let n = 0;
    for (let i = 1; i < STATE_HIST.length; i++) {
      const [ta, sa] = STATE_HIST[i - 1], tb = STATE_HIST[i][0];
      if (tb < t0 || sa === 'idle') continue;
      const xa = s.x + s.w * (Math.max(ta, t0) - t0) / (t1 - t0);
      const xb = s.x + s.w * (Math.min(tb, t1) - t0) / (t1 - t0);
      ctx.fillStyle = sa === 'broken' ? RESPCOL.break : RESPCOL[M.resp] || COL.pos;
      ctx.fillRect(xa, s.y + 20, Math.max(1, xb - xa), s.h - 26);
      n++;
    }
    lab(ctx, W, H, s.x + 6, s.y + 3,
        n ? (CH.state === 'broken' ? 'in pieces since ' + fmt(CH.t, 1) + ' s'
                                   : 'excited ' + fmt(100 * M.chDuty, 1) + ' % of the run so far')
          : 'never excited yet',
        n ? COL.pos : COL.dim, SMALL, 'left', 'top');
    lab(ctx, W, H, s.x1 - 6, s.y + 3,
        CH.absorbed + ' absorbed / ' + (CH.absorbed + CH.passed) + ' tried = '
        + fmt(M.chFrac, 3) + '  (a free molecule takes exactly ½)',
        COL.dim, SMALL, 'right', 'top');
  }
  drawCaption(ctx, L);
}


/* ---------------------------------------------------------------- *
 *  B. the spectrum -- PhET's Light Spectrum Diagram, and the real    *
 *     transitions of these molecules on the same axis                *
 * ---------------------------------------------------------------- */
/* every real transition this file can place, as [wavelength m, molecule,
   label, kind].  kind: 'vib' | 'rot' | 'diss' | 'elec' */
function realLines() {
  return memo('lines', 'all', () => {
    const out = [];
    for (const mol of MOLORDER) {
      for (const m of modeTable(mol)) {
        if (out.some(o => o.mol === mol && o.kind === 'vib' && Math.abs(o.nu - m.nu) < 0.5)) continue;
        out.push({lam: 1e-2 / m.nu, mol, nu: m.nu, kind: 'vib', active: m.active,
                  lab: fmt(m.nu, 0) + ' cm⁻¹ ' + m.sym});
      }
      if (D0_EV[mol] !== undefined)
        out.push({lam: threshNm(mol) * 1e-9, mol, kind: 'diss',
                  lab: 'breaks below ' + fmt(threshNm(mol), 0) + ' nm', active: true});
    }
    /* the pure rotational lines this file can actually place */
    const B0 = DIATOMIC.CO.Bprint - DIATOMIC.CO.ae / 2;   /* the tabulated B_e */
    out.push({lam: 1e-2 / (2 * B0), mol: 'CO', kind: 'rot', active: true,
              lab: 'J = 1 ← 0 at ' + fmt(2 * B0 * C_CM / 1e9, 3) + ' GHz'});
    out.push({lam: LIGHT_C / QUOTED_LINES[1][1], mol: 'H2O', kind: 'rot', active: true,
              lab: 'the 22.235 GHz line (quoted)'});
    /* NO2 is brown: it absorbs right across the visible */
    out.push({lam: 450e-9, mol: 'NO2', kind: 'elec', active: true,
              lab: 'visible band, 400–650 nm (why NO₂ is brown)'});
    return out;
  });
}
function logX(b, lam, lo, hi) {
  return b.x + b.w * (Math.log10(lam) - Math.log10(lo)) / (Math.log10(hi) - Math.log10(lo));
}
function drawBandStrip(ctx, b, lo, hi, W, H) {
  for (const [name, bhi, blo] of PHET_BANDS) {
    const xa = logX(b, Math.min(bhi, hi), lo, hi), xb = logX(b, Math.max(blo, lo), lo, hi);
    const x0 = Math.max(b.x, Math.min(xa, xb)), x1 = Math.min(b.x1, Math.max(xa, xb));
    if (x1 <= x0 + 0.5) continue;
    const c = BANDCOL[name] || COL.struct;
    ctx.fillStyle = rgba(c, 0.16);
    ctx.fillRect(x0, b.y, x1 - x0, b.h);
    ctx.strokeStyle = rgba(c, 0.5);
    ctx.lineWidth = 1;
    ctx.strokeRect(Math.round(x0) + 0.5, Math.round(b.y) + 0.5, Math.round(x1 - x0), Math.round(b.h));
    if (x1 - x0 > 34) lab(ctx, W, H, (x0 + x1) / 2, b.y + b.h / 2, name, shade(c, 1), SMALL, 'center', 'middle');
  }
}
function drawSpectrum(ctx, W, H, M) {
  const capFull = 'The top strip is PhET&rsquo;s own Light Spectrum Diagram, with the band edges its accessibility '
    + 'text states, and the four wavelengths its light source can actually emit. The two panels below are zooms, on the '
    + 'same logarithmic wavelength axis, carrying every measured transition of these molecules. The gap between the two '
    + 'is the whole point: PhET&rsquo;s &ldquo;infrared&rdquo; photon is at 850 nm, and the vibrations it stands for are '
    + 'at 2.7&ndash;15 &micro;m &mdash; a factor of ' + fmt(M.real.nearest ? 1e4 / M.real.nearest / 0.85 : 0, 0)
    + ' away for this molecule.';
  const capShort = 'PhET&rsquo;s band diagram and its four photons, against the measured transitions of these molecules.';
  const L = stage(ctx, W, H, capFull, capShort, 2, 0.52, 1);
  const b = L.main, LO = 1e-12, HI = 1e4;
  const strip = box(b.x, b.y + 14, b.w, Math.min(52, b.h * 0.3));
  drawBandStrip(ctx, strip, LO, HI, W, H);
  /* the decade axis */
  ctx.strokeStyle = '#181d29';
  ctx.lineWidth = 1;
  for (let e = -12; e <= 4; e += 2) {
    const x = logX(b, Math.pow(10, e), LO, HI);
    ctx.beginPath();
    ctx.moveTo(x, strip.y + strip.h);
    ctx.lineTo(x, strip.y + strip.h + 5);
    ctx.stroke();
    lab(ctx, W, H, x, strip.y + strip.h + 7, '10' + supDigits(e) + ' m', '#6f7789', SMALL, 'center', 'top');
  }
  lab(ctx, W, H, b.x, b.y, 'PhET’s Light Spectrum Diagram — its own band edges', COL.ref, TITLE_FONT, 'left', 'top');
  lab(ctx, W, H, b.x1, strip.y + strip.h + 7, 'longer wavelength ←', COL.dim, SMALL, 'right', 'top');
  /* PhET's four photons */
  let iy = 0;
  for (const bd of BANDS) {
    const lam = PHET.lam[bd], x = logX(b, lam, LO, HI);
    const y0 = strip.y + strip.h + 24, y1 = y0 + 22 + (iy % 2) * 18;
    ctx.beginPath();
    ctx.moveTo(x, strip.y);
    ctx.lineTo(x, y1);
    ctx.strokeStyle = bd === M.band ? COL.live : rgba(BANDCOL[bd], 0.8);
    ctx.lineWidth = bd === M.band ? 2.2 : 1.3;
    ctx.stroke();
    dot(ctx, x, strip.y + strip.h / 2, bd === M.band ? 5 : 3.6, BANDCOL[bd], '#0b0e16', 1);
    lab(ctx, W, H, x, y1 + 2, BANDNAME[bd] + '  ' + eFmt(PHOTON[bd].E_eV, 3) + ' eV',
        bd === M.band ? COL.live : shade(BANDCOL[bd], 1), SMALL, 'center', 'top');
    iy++;
  }
  const inBand = bandOf(PHET.lam.microwave);
  lab(ctx, W, H, b.x, strip.y + strip.h + 100,
      b.w > 700
        ? 'PhET’s microwave photon is at 0.2 m, which falls in the gap between its own radio band (down to 0.5 m) '
          + 'and its microwave band (from 0.1 m): ' + (inBand ? 'in ' + inBand : 'in neither')
        : 'PhET’s 0.2 m photon is in ' + (inBand ? inBand : 'neither of its own bands'),
      COL.ref, SMALL, 'left', 'top');
  /* the two zooms */
  if (L.bottom.length >= 1) drawZoom(ctx, W, H, M, L.bottom[0], 6e-7, 3e-1,
                                     'the infrared and microwave: where the vibrations and rotations really are',
                                     'infrared and microwave');
  if (L.bottom.length >= 2) drawZoom(ctx, W, H, M, L.bottom[1], 8e-8, 8e-7,
                                     'the visible and ultraviolet: the electronic bands and the bond energies',
                                     'visible and ultraviolet');
  /* one legend for both zooms, in the main panel's empty middle -- and only
     when it fits clear of everything above it; otherwise the caption names
     the colours (Known-bad: a legend laid over a label is worse than none) */
  { const items = [[COL.pos, 'measured IR-active fundamental'], [COL.off, 'inactive: Raman only, never infrared'],
                   [COL.struct, 'pure rotational line'], [COL.ref, 'dissociation threshold (quoted bond energy)'],
                   [COL.glow, 'electronic absorption band']];
    const legY = strip.y + strip.h + 124;
    if (legY + 90 < b.y1 && b.w > 520) legendBox(ctx, b.x, legY, items);
    else {
      /* no room for a box: a one-line colour key instead, each phrase in its
         own colour, rather than a legend laid over something else */
      let x = b.x;
      ctx.font = SMALL;
      for (const [c, t] of items) {
        const wdt = ctx.measureText(t).width + 26;
        if (x + wdt > b.x1) break;
        ctx.fillStyle = c;
        ctx.fillRect(x, strip.y + strip.h + 122, 10, 7);
        lab(ctx, W, H, x + 15, strip.y + strip.h + 119, t, shade(c, 1), SMALL, 'left', 'top');
        x += wdt;
      }
    }
  }
  drawCaption(ctx, L);
}
function supDigits(e) {
  const S = {'-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
             5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹'};
  return String(e).split('').map(c => S[c] || c).join('');
}
function drawZoom(ctx, W, H, M, b, lo, hi, title, shortTitle) {
  frame(ctx, b, COL.edge);
  const GUT = 40;                      /* the row labels get their own gutter */
  drawBandStrip(ctx, box(b.x + GUT, b.y, b.w - GUT, 13), lo, hi, W, H);
  lab(ctx, W, H, b.x, b.y - 9, titleFor(b, title, shortTitle), COL.text, TITLE_FONT, 'left', 'bottom');
  const bz = box(b.x + GUT, b.y, b.w - GUT, b.h);
  for (let e = Math.ceil(Math.log10(lo)); e <= Math.floor(Math.log10(hi)); e++) {
    const x = logX(bz, Math.pow(10, e), lo, hi);
    ctx.strokeStyle = '#181d29';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x, b.y + 13);
    ctx.lineTo(x, b.y1);
    ctx.stroke();
    const um = Math.pow(10, e) * 1e6;
    lab(ctx, W, H, x, b.y1 + 3,
        um >= 1000 ? fmt(um / 1000, 0) + ' mm' : (um >= 1 ? fmt(um, 0) + ' µm' : fmt(um * 1000, 0) + ' nm'),
        '#6f7789', SMALL, 'center', 'top');
  }
  const rows = MOLORDER;
  const rh = (b.h - 20) / rows.length;
  const lines = realLines();
  for (let r = 0; r < rows.length; r++) {
    const mol = rows[r], y = b.y + 16 + rh * (r + 0.5);
    const on = mol === M.mol;
    lab(ctx, W, H, b.x + 4, y, mol, on ? COL.live : COL.dim, SMALL, 'left', 'middle');
    for (const ln of lines) {
      if (ln.mol !== mol) continue;
      if (ln.lam < lo || ln.lam > hi) continue;
      const x = logX(bz, ln.lam, lo, hi);
      const c = ln.kind === 'vib' ? (ln.active ? COL.pos : COL.off)
        : ln.kind === 'rot' ? COL.struct : ln.kind === 'diss' ? COL.ref : COL.glow;
      ctx.strokeStyle = c;
      ctx.lineWidth = ln.kind === 'vib' && !ln.active ? 1 : 1.8;
      ctx.beginPath();
      ctx.moveTo(x, y - rh * 0.34);
      ctx.lineTo(x, y + rh * 0.34);
      if (ln.kind === 'diss') ctx.setLineDash([3, 3]);
      ctx.stroke();
      ctx.setLineDash([]);
    }
  }
  /* PhET's photons that fall in this window */
  for (const bd of BANDS) {
    const lam = PHET.lam[bd];
    if (lam < lo || lam > hi) continue;
    const x = logX(bz, lam, lo, hi);
    ctx.strokeStyle = bd === M.band ? COL.live : rgba(BANDCOL[bd], 0.9);
    ctx.lineWidth = bd === M.band ? 2.4 : 1.6;
    ctx.setLineDash([6, 3]);
    ctx.beginPath();
    ctx.moveTo(x, b.y + 13);
    ctx.lineTo(x, b.y1);
    ctx.stroke();
    ctx.setLineDash([]);
    lab(ctx, W, H, x, b.y1 + 17, 'PhET’s ' + bd,
        bd === M.band ? COL.live : shade(BANDCOL[bd], 1), SMALL, 'center', 'top');
  }
  
}
