
/* ================================================================== *
 *  the drawn atom, the buckets, the periodic table, the symbol box    *
 * ================================================================== */
/* PhET's two capture radii, read out of BAAModel: a nucleon dropped within
   100 model units of the centre joins the nucleus, an electron within
   1.1 x the outer shell joins the shells. */
const CAPTURE_NUCLEON = 100;
const CAPTURE_ELECTRON = 1.1 * PHET.outerShell;
/* the model half-width the atom picture is fitted to: the outer shell plus an
   electron, so a full shell is not clipped */
const ATOM_HALF = PHET.outerShell + PHET.electronRadius + 6;

/* layout() reserves 120 px of stage before it gives up on the long caption,
   which is not enough for a view whose panels have MINIMUM heights: the
   clamps then push the lower panel's axis title past the caption.  This is
   layout() with the view's own floor, so a long caption is traded for the
   short one rather than for a collision (Known-bad: wrapped text has no
   fixed height; measure the caption BEFORE laying out the panels). */
function layoutMin(ctx, W, H, full, short, minStage){
  const f = fitCaption(ctx, W, H - HINT_H, full, short, usableW(W), stageTop() + minStage);
  return {top: stageTop(), capY: f.capY, capW: f.capW, txt: f.txt,
          bot: f.capY - 12, W: W, H: H};
}

/* a panel title must fit INSIDE its own panel: the long one is used only when
   it measures narrower than the box, else the short one (Known-bad,
   brachistochrone).  Without it a right-hand panel's title runs out from under
   its own panel and under the floating readout (found by tools/audit.py). */
function panelTitleFit(ctx, b, long, short){
  ctx.font = 'italic 13px Georgia, serif';
  panelTitle(ctx, b, ctx.measureText(plain(long)).width <= b.w ? long : short);
}

/* axes() draws its tick labels, its axis names and its title with raw
   fillText, outside the label registry, so a label placed by labelIfClear
   cannot see them and lands on a tick (Known-bad, brachistochrone: axesR).
   This wrapper draws the same axes and then REGISTERS every piece of text it
   drew, so everything placed afterwards dodges them. */
function axesR(ctx, b, xlo, xhi, ylo, yhi, opt){
  const o = {};
  for(const k in (opt || {})) o[k] = opt[k];
  o.xticks = o.xticks || ticksFor(Math.min(xlo, xhi), Math.max(xlo, xhi), o.nx || 6);
  o.yticks = o.yticks || ticksFor(Math.min(ylo, yhi), Math.max(ylo, yhi), o.ny || 5);
  axes(ctx, b, xlo, xhi, ylo, yhi, o);
  const TF = '10.5px -apple-system, sans-serif';
  for(const t of o.xticks){
    const X = b.x + b.w * (t - xlo) / (xhi - xlo || 1);
    if(X < b.x - 0.5 || X > b.x1 + 0.5) continue;
    LABEL_RECTS.push(labelRect(ctx, X, b.y1 + 5, o.xfmt ? o.xfmt(t) : fmt(t, 2), TF,
                               'center', 'top'));
  }
  for(const t of o.yticks){
    const Y = b.y1 - b.h * (t - ylo) / (yhi - ylo || 1);
    if(Y < b.y - 0.5 || Y > b.y1 + 0.5) continue;
    LABEL_RECTS.push(labelRect(ctx, b.x - 6, Y, o.yfmt ? o.yfmt(t) : fmt(t, 2), TF,
                               'right', 'middle'));
  }
  if(o.xlab) LABEL_RECTS.push(labelRect(ctx, b.x + b.w / 2, b.y1 + 21, o.xlab,
                                        '11px -apple-system, sans-serif', 'center', 'top'));
  if(o.title) LABEL_RECTS.push(labelRect(ctx, b.x, b.y - 9, o.title,
                                         'italic 13px Georgia, serif', 'left', 'bottom'));
  /* the y-axis name is drawn in a ROTATED frame: its screen box is the
     transpose of its text box, centred on the panel's mid-height */
  if(o.ylab){
    const r = labelRect(ctx, 0, 0, o.ylab, '11px -apple-system, sans-serif', 'center', 'bottom');
    LABEL_RECTS.push({x: b.x - 40 - r.h, y: b.y + b.h / 2 - r.w / 2, w: r.h, h: r.w});
  }
}

/* a label/value row that WRAPS instead of overlapping: the value goes on the
   same line when it fits and on its own line when it does not.  A long label
   beside a right-aligned value is the commonest text collision there is. */
function kvRow(ctx, x, y, w, k, v, col){
  const KF = '10.5px -apple-system, sans-serif', VF = '11px -apple-system, sans-serif';
  const vw = labelRect(ctx, x, y, v, VF, 'left', 'top').w;
  const kw = labelRect(ctx, x, y, k, KF, 'left', 'top').w;
  if(kw + vw + 12 <= w){
    label(ctx, x, y, k, COL.faint, KF, 'left', 'top');
    label(ctx, x + w, y, v, col, VF, 'right', 'top');
    return 17;
  }
  /* it does not fit on one line: the KEY wraps to the whole column and the
     value goes underneath it.  Squeezing the key into whatever the value
     leaves is what put "odd-odd" through its own value at 820 px (found by
     tools/audit.py, then by the inline sweep). */
  const lines = wrapText(ctx, k, w, KF);
  for(let i = 0; i < lines.length; i++)
    label(ctx, x, y + i * 13, lines[i], COL.faint, KF, 'left', 'top');
  label(ctx, x + w, y + lines.length * 13, v, col, VF, 'right', 'top');
  return lines.length * 13 + 17;
}

/* a block of annotation lines placed in whichever corner of panel b is clear
   of BOTH the label registry and the given list of solid marks.  Marks drawn
   with fillRect are invisible to labelIfClear, so they have to be handed over
   explicitly (Known-bad: deciding which corner is empty by looking at one
   configuration keeps getting it wrong). */
function annotate(ctx, b, marks, lines){
  const F = '11px -apple-system, sans-serif';
  let w = 0;
  for(const l of lines) w = Math.max(w, labelRect(ctx, 0, 0, l[0], F, 'left', 'top').w);
  const h = lines.length * 14;
  const cands = [[b.x + 6, b.y + 4], [b.x1 - w - 6, b.y + 4],
                 [b.x + 6, b.y1 - h - 4], [b.x1 - w - 6, b.y1 - h - 4]];
  for(const [cx, cy] of cands){
    let hit = false;
    const r = {x: cx, y: cy, w: w, h: h};
    for(const q of marks) if(rectsHit(r, q)){ hit = true; break; }
    if(!hit) for(const q of LABEL_RECTS) if(rectsHit(r, q)){ hit = true; break; }
    if(hit) continue;
    for(let i = 0; i < lines.length; i++)
      label(ctx, cx, cy + i * 14, lines[i][0], lines[i][1], F, 'left', 'top');
    return r;
  }
  return null;               /* every corner is busy: draw nothing rather than lie */
}

/* interleave protons and neutrons evenly over the layout slots, so a nucleus
   looks mixed rather than striped.  Deterministic: slot k is a proton when
   floor((k+1) p / (p+n)) > floor(k p / (p+n)). */
function nucleonTypes(p, n){
  const t = [], tot = p + n;
  if(tot === 0) return t;
  for(let k = 0; k < tot; k++)
    t.push(Math.floor((k + 1) * p / tot) > Math.floor(k * p / tot) ? 'p' : 'n');
  return t;
}
/* jiggle offset for an unstable nucleus: PhET moves it every 0.1 s round a
   five-step cycle of directions and a four-step cycle of amplitudes */
const JIGGLE_ANG = [0.1 * PI, 1.6 * PI, 0.7 * PI, 1.1 * PI, 0.3 * PI];
const JIGGLE_AMP = [0.4, 0.8, 0.2, 0.9];
function jiggleOffset(k){
  const r = JIGGLE_AMP[k % JIGGLE_AMP.length] * 0.5 * PHET.nucleonRadius;
  const a = JIGGLE_ANG[k % JIGGLE_ANG.length];
  return [r * Math.cos(a), r * Math.sin(a)];
}

/* draw the atom centred at (cx, cy) with s px per model unit */
function drawAtomPicture(ctx, cx, cy, s, M, opt){
  const o = opt || {};
  const st = M.st;
  const rNuc = PHET.nucleonRadius * s, rEl = PHET.electronRadius * s;
  if(st.model === 'cloud'){
    const R = M.cloudR * s;
    if(R > 0){
      /* concentric OPAQUE rings premixed against the background: a stack of
         translucent discs composites twice where they overlap and reads as
         banding (Known-bad, the corduroy entry) */
      const NR = 30;
      for(let i = NR; i >= 1; i--){
        const f = i / NR;
        const a = 0.42 * (1 - f) * (1 - f) + 0.03;
        disc(ctx, cx, cy, R * f, mix(COL.bg, COL.electron, a));
      }
      ring(ctx, cx, cy, R, rgba(COL.electron, 0.5), 1);
    }
  } else {
    ring(ctx, cx, cy, PHET.innerShell * s, rgba(COL.str, 0.42), 1, [5, 5]);
    ring(ctx, cx, cy, PHET.outerShell * s, rgba(COL.str, 0.42), 1, [5, 5]);
    const slots = electronSlots();
    for(let k = 0; k < Math.min(M.e, slots.length); k++){
      const sl = slots[k];
      disc(ctx, cx + sl.x * s, cy + sl.y * s, rEl, COL.electron);
      ring(ctx, cx + sl.x * s, cy + sl.y * s, rEl, rgba('#ffffff', 0.35), 1);
    }
  }
  /* the nucleus */
  const tot = M.p + M.n;
  let ox = 0, oy = 0;
  if(o.jiggle && tot > 0 && !M.nucleusStable){
    const j = jiggleOffset(o.jiggle);
    ox = j[0] * s; oy = j[1] * s;
  }
  if(tot > 0){
    const L = nucleonLayout(tot, PHET.nucleonRadius), ty = nucleonTypes(M.p, M.n);
    /* far nucleons first so the near ones overlap them */
    const order = L.map((pt, i) => i).sort((a, b) =>
      (L[b][0] * L[b][0] + L[b][1] * L[b][1]) - (L[a][0] * L[a][0] + L[a][1] * L[a][1]));
    for(const i of order){
      const x = cx + ox + L[i][0] * s, y = cy + oy + L[i][1] * s;
      const c = ty[i] === 'p' ? COL.proton : COL.neutron;
      disc(ctx, x, y, rNuc, c);
      ring(ctx, x, y, rNuc, rgba('#000000', 0.55), 1);
      disc(ctx, x - rNuc * 0.32, y - rNuc * 0.32, rNuc * 0.3, rgba('#ffffff', 0.35));
    }
  }
  return {rNuc: rNuc, rEl: rEl};
}

/* ---- the buckets ---- */
const BUCKET_KINDS = [{k: 'p', name: 'Protons', col: COL.proton, max: PHET.numProtons},
                      {k: 'n', name: 'Neutrons', col: COL.neutron, max: PHET.numNeutrons},
                      {k: 'e', name: 'Electrons', col: COL.electron, max: PHET.numElectrons}];
function bucketBoxes(x0, y, w, h){
  const gap = 10, bw = (w - 2 * gap) / 3;
  return BUCKET_KINDS.map((b, i) => Object.assign({}, b,
    {box: box(x0 + i * (bw + gap), y, bw, h)}));
}
function drawBuckets(ctx, bs, M){
  for(const b of bs){
    const left = b.k === 'p' ? M.leftP : (b.k === 'n' ? M.leftN : M.leftE);
    const r = Math.min(9, Math.max(5, b.box.w / 14));
    ctx.fillStyle = COL.panel; ctx.fillRect(b.box.x, b.box.y, b.box.w, b.box.h);
    frame(ctx, b.box, COL.edge);
    /* the pile: one row of discs, wrapped */
    const perRow = Math.max(1, Math.floor((b.box.w - 12) / (2 * r + 2)));
    for(let i = 0; i < left; i++){
      const rowi = Math.floor(i / perRow), ci = i % perRow;
      const x = b.box.x + 8 + r + ci * (2 * r + 2) + (rowi % 2 ? r : 0);
      const y = b.box.y + b.box.h - 9 - r - rowi * (2 * r - 1);
      if(y < b.box.y + 14) continue;
      disc(ctx, x, y, r, b.col);
      ring(ctx, x, y, r, rgba('#000000', 0.5), 1);
    }
    label(ctx, b.box.x + b.box.w / 2, b.box.y + 4, b.name + ' (' + left + ')',
          left ? COL.text : COL.faint, '11px -apple-system, sans-serif', 'center', 'top');
  }
}
function bucketHit(bs, x, y){
  for(const b of bs){
    const q = b.box;
    if(x >= q.x && x <= q.x1 && y >= q.y && y <= q.y1) return b.k;
  }
  return null;
}

/* ---- the periodic table ---- */
function ptGeo(x0, y0, w, rows){
  const cw = Math.max(6, Math.min(26, (w - 17 * 1) / 18));
  return {x0: x0, y0: y0, cw: cw, ch: cw, gap: 1, rows: rows || 10,
          w: 18 * cw + 17, h: (rows || 10) * cw + ((rows || 10) - 1)};
}
function ptCell(g, z){
  const xy = PTXY[z];
  if(!xy) return null;
  return {x: g.x0 + (xy[0] - 1) * (g.cw + g.gap), y: g.y0 + (xy[1] - 1) * (g.ch + g.gap),
          w: g.cw, h: g.ch};
}
function drawPeriodicTable(ctx, g, M, opt){
  const o = opt || {};
  const hiZ = o.highlight === undefined ? M.p : o.highlight;
  const maxZ = o.maxZ || 118;
  for(let z = 1; z <= maxZ; z++){
    const c = ptCell(g, z);
    if(!c || c.y + c.h > g.y0 + g.h + 1) continue;
    const reach = z <= (o.reach || PHET.numProtons);
    const on = z === hiZ;
    ctx.fillStyle = on ? COL.live : (reach ? mix(COL.bg, COL.str, 0.26) : COL.panel);
    ctx.fillRect(c.x, c.y, c.w, c.h);
    ctx.strokeStyle = on ? '#ffffff' : '#1b2030'; ctx.lineWidth = on ? 1.6 : 1;
    ctx.strokeRect(c.x + 0.5, c.y + 0.5, c.w - 1, c.h - 1);
    if(g.cw >= 13){
      ctx.fillStyle = on ? '#ffffff' : (reach ? COL.text : '#5b6274');
      ctx.font = Math.max(7, Math.round(g.cw * 0.52)) + 'px -apple-system, sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(SYMBOL[z], c.x + c.w / 2, c.y + c.h / 2 + 0.5);
    }
  }
  return g;
}
function ptHit(g, x, y, maxZ){
  for(let z = 1; z <= (maxZ || 118); z++){
    const c = ptCell(g, z);
    if(!c) continue;
    if(x >= c.x && x <= c.x + c.w && y >= c.y && y <= c.y + c.h) return z;
  }
  return null;
}

/* ---- PhET's three display panels ---- */
function factBox(ctx, b, title, value, col){
  ctx.fillStyle = COL.panel; ctx.fillRect(b.x, b.y, b.w, b.h);
  frame(ctx, b, COL.edge);
  label(ctx, b.x + 8, b.y + 5, title, COL.faint, '10px -apple-system, sans-serif', 'left', 'top');
  label(ctx, b.x + b.w / 2, b.y + b.h - 6, value, col || COL.text,
        'italic ' + Math.max(12, Math.min(19, Math.round(b.h * 0.42))) + 'px Georgia, serif',
        'center', 'bottom');
}

/* ================================================================== *
 *  view 1 — the atom (PhET's first screen)                            *
 * ================================================================== */
/* Every rectangle the atom view draws AND the pointer tests is computed here,
   once, by a pure function.  A number computed inside a draw call cannot be
   tested, and a click that recomputes its own geometry drifts away from the
   picture (Known-bad, twice). */
function atomGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, atomCaption(M), atomCaptionShort(M));
  const x0 = 12, w = usableW(W);
  const narrow = narrowStage(W);
  const colW = narrow ? w : Math.max(260, w * 0.56);
  const rightX = x0 + colW + 16, rightW = narrow ? 0 : w - colW - 16;
  const bucketH = 62;
  /* the three labels PhET puts under the atom need a band of their own, or
     the element name lands on a bucket caption at every canvas size */
  const st = M.st;
  const labH = (st.showName ? 21 : 0) + (st.showIon ? 18 : 0) + (st.showStab ? 18 : 0)
             + ((st.showName || st.showIon || st.showStab) ? 10 : 0);
  const picBot = L.bot - bucketH - 14 - labH;
  const picH = Math.max(90, picBot - L.top);
  const s = Math.min(colW / (2 * ATOM_HALF), picH / (2 * ATOM_HALF));
  const G = {L: L, x0: x0, w: w, colW: colW, rightX: rightX, rightW: rightW,
             cx: x0 + colW / 2, cy: L.top + picH / 2, s: s, narrow: narrow,
             bh: 46, gap: 8, labY: L.top + picH + 6,
             buckets: bucketBoxes(x0, L.bot - bucketH, colW, bucketH), pt: null};
  if(!narrow && M.st.showTable){
    const y = L.top + 3 * (G.bh + G.gap) + 6;
    const g = ptGeo(rightX, y + 14, rightW, 10);
    if(g.y0 + g.h < L.bot - 6){ G.pt = g; G.ptLabelY = y; }
  }
  return G;
}
function drawAtomView(ctx, W, H, M){
  const G = atomGeo(ctx, W, H, M);
  const st = M.st;
  drawAtomPicture(ctx, G.cx, G.cy, G.s, M, {jiggle: st.jiggle ? FRAME.jig : 0});
  /* the labels PhET puts under the atom, each behind its own checkbox */
  let ly = G.labY;
  if(st.showName)
    label(ctx, G.cx, ly, M.p ? M.name : 'no element yet', M.p ? COL.pos : COL.faint,
          'italic 16px Georgia, serif', 'center', 'top'), ly += 21;
  if(st.showIon)
    label(ctx, G.cx, ly, (M.hasNuc || M.e) ? M.ion : 'nothing here',
          (!M.hasNuc && !M.e) ? COL.faint : (M.q === 0 ? COL.pos : COL.live),
          '12.5px -apple-system, sans-serif', 'center', 'top'),
    ly += 18;
  if(st.showStab)
    label(ctx, G.cx, ly, M.hasNuc ? (M.stable ? 'stable' : 'unstable') : '',
          M.stable ? COL.pos : COL.ref, '12.5px -apple-system, sans-serif', 'center', 'top');
  /* the held particle rides with the cursor */
  if(DRAG.active && DRAG.type){
    const c = DRAG.type === 'p' ? COL.proton : (DRAG.type === 'n' ? COL.neutron : COL.electron);
    const r = (DRAG.type === 'e' ? PHET.electronRadius : PHET.nucleonRadius) * G.s;
    disc(ctx, DRAG.x, DRAG.y, r, c);
    ring(ctx, DRAG.x, DRAG.y, r, '#ffffff', 1.4);
    ring(ctx, G.cx, G.cy, (DRAG.type === 'e' ? CAPTURE_ELECTRON : CAPTURE_NUCLEON) * G.s,
         rgba(COL.pos, 0.55), 1, [4, 4]);
  }
  drawBuckets(ctx, G.buckets, M);
  if(!G.narrow){
    /* PhET's three display panels, then its periodic table */
    const bh = G.bh, gap = G.gap;
    let y = G.L.top;
    factBox(ctx, box(G.rightX, y, G.rightW, bh), 'ELEMENT NAME',
            M.p ? M.name : '—', M.p ? COL.pos : COL.faint); y += bh + gap;
    const half = (G.rightW - gap) / 2;
    factBox(ctx, box(G.rightX, y, half, bh), 'MASS NUMBER',
            M.hasNuc ? String(M.A) : '—', COL.pos);
    factBox(ctx, box(G.rightX + half + gap, y, half, bh), 'NET CHARGE',
            M.chargeStr, M.q === 0 ? COL.pos : COL.live); y += bh + gap;
    factBox(ctx, box(G.rightX, y, G.rightW, bh), 'NUCLEAR STABILITY',
            M.hasNuc ? (M.stable ? 'Stable' : 'Unstable') : '—',
            M.hasNuc ? (M.stable ? COL.pos : COL.ref) : COL.faint);
    if(G.pt){
      label(ctx, G.rightX, G.ptLabelY, 'periodic table — the ten the buckets reach are lit',
            COL.faint, '10px -apple-system, sans-serif', 'left', 'top');
      drawPeriodicTable(ctx, G.pt, M, {reach: PHET.numProtons});
    }
  }
  drawCaption(ctx, G.L);
}

function atomCaption(M){
  const st = M.st;
  return 'PhET’s first screen. Drag a particle out of a bucket and drop it on the atom, or use the '
    + 'panel’s three counts. The buckets hold ' + PHET.numProtons + ' protons, ' + PHET.numNeutrons
    + ' neutrons and ' + PHET.numElectrons + ' electrons, which are PhET’s own numbers, so the '
    + 'reachable elements stop at neon. Everything under the atom is worked out from the three counts and '
    + 'nothing else: the element is Z = ' + M.p + ', the mass number is ' + M.p + ' + ' + M.n + ' = '
    + M.A + ', the charge is ' + M.p + ' − ' + M.e + ' = ' + signed(M.q) + '. '
    + (M.hasNuc ? ('Whether the nucleus is stable is the one thing that is not arithmetic: ' + M.sym + '-'
      + M.A + ' is ' + (M.stable ? 'in' : 'not in') + ' PhET’s table of ' + M.nStable
      + ' stable nuclides.') : '')
    + (st.model === 'cloud' ? ' The cloud’s radius is PhET’s own linear law, r = 42.5 + 8.75 e '
      + 'model units, so ten electrons put it exactly on the outer shell.'
      : ' The two shells hold 2 and 8, which is PhET’s cartoon and not an orbital calculation.')
    + scaleNote(M);
}
/* the scale distortion, PRINTED, for the nuclide on screen rather than for a
   worked example: house rule, every exaggeration is named on the canvas */
function scaleNote(M){
  const ex = M.hasNuc ? nucleusExaggeration(M.p, M.A) : null;
  if(ex == null) return ' SCALE: with no nucleus there is nothing to be out of scale.';
  return ' SCALE: the nucleus is drawn ' + sigf(ex, 3) + '× too big relative to the shells. '
    + M.sym + '-' + M.A + ' has a nuclear radius of ' + fmt(nuclearRadiusFm(M.A), 2)
    + ' fm inside an atom of ' + fmt(atomRadiusPm(M.p), 0) + ' pm, a ratio of 1 to '
    + fmt(1 / trueNucleusFraction(M.p, M.A), 0) + ', while the drawing’s is 1 to '
    + fmt(1 / drawnNucleusFraction(), 0) + '.';
}
function atomCaptionShort(M){
  return 'Drag protons, neutrons and electrons in. Element = Z, A = Z + N, q = Z − e; '
    + 'stability is a table.';
}

/* ================================================================== *
 *  view 2 — the symbol (PhET's second screen)                         *
 * ================================================================== */
function symbolGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, symbolCaption(M), symbolCaptionShort(M));
  const x0 = 12, w = usableW(W), narrow = narrowStage(W);
  const avail = L.bot - L.top;
  const side = Math.max(120, Math.min(narrow ? w - 20 : w * 0.46, avail - 96));
  return {L: L, x0: x0, w: w, narrow: narrow, side: side,
          bx: x0 + (narrow ? (w - side) / 2 : 6), by: L.top + 10};
}
/* PhET's symbol box: mass number top left, charge top right, atomic number
   bottom left, the symbol itself in the middle. */
function drawSymbolBox(ctx, b, M, big){
  ctx.fillStyle = mix(COL.bg, '#ffffff', 0.06); ctx.fillRect(b.x, b.y, b.w, b.h);
  ctx.strokeStyle = COL.str; ctx.lineWidth = 2;
  ctx.strokeRect(b.x + 1, b.y + 1, b.w - 2, b.h - 2);
  const f = b.w;
  /* the three corner captions only fit on a box wide enough to carry them
     without running into the numbers or the letter (measured, not guessed) */
  const cap = big && b.w >= 230;
  /* the caption sits a full number-height below the number, measured from the
     font actually used: a fixed offset put "mass number" through "12" at
     every stage width over 1000 px */
  const num = Math.round(f * 0.14), capH = cap ? Math.round(num * 1.15) + 4 : 0;
  label(ctx, b.x + b.w / 2, b.y + b.h * 0.60, M.p ? M.sym : '?',
        M.p ? '#ffffff' : COL.faint,
        'italic ' + Math.round(f * 0.32) + 'px Georgia, serif', 'center', 'middle');
  label(ctx, b.x + 9, b.y + 7, M.hasNuc ? String(M.A) : '—', COL.pos,
        num + 'px -apple-system, sans-serif', 'left', 'top');
  label(ctx, b.x + b.w - 9, b.y + 7, M.chargeStr, M.q === 0 ? COL.pos : COL.live,
        num + 'px -apple-system, sans-serif', 'right', 'top');
  label(ctx, b.x + 9, b.y + b.h - 7, M.p ? String(M.p) : '—', COL.proton,
        num + 'px -apple-system, sans-serif', 'left', 'bottom');
  if(cap){
    label(ctx, b.x + 9, b.y + 7 + capH, 'mass number', COL.faint,
          '9.5px -apple-system, sans-serif', 'left', 'top');
    label(ctx, b.x + b.w - 9, b.y + 7 + capH, 'charge', COL.faint,
          '9.5px -apple-system, sans-serif', 'right', 'top');
    label(ctx, b.x + 9, b.y + b.h - 7 - capH, 'atomic number', COL.faint,
          '9.5px -apple-system, sans-serif', 'left', 'bottom');
  }
}
function drawSymbolView(ctx, W, H, M){
  const G = symbolGeo(ctx, W, H, M);
  const st = M.st;
  const b = box(G.bx, G.by, G.side, G.side);
  drawSymbolBox(ctx, b, M, true);
  /* the three counts, each joined to the corner it feeds */
  const rows = [['protons', M.p, COL.proton, 'Z, bottom left — and the element'],
                ['neutrons', M.n, COL.neutron, 'not in the symbol, except through A'],
                ['electrons', M.e, COL.electron, 'only through the charge']];
  if(!G.narrow){
    const rx = G.bx + G.side + 24, rw = Math.max(140, G.x0 + G.w - rx);
    let y = G.by + 4;
    for(const r of rows){
      disc(ctx, rx + 7, y + 8, 6, r[2]);
      label(ctx, rx + 20, y, r[0] + ' = ' + r[1], COL.text,
            '13px -apple-system, sans-serif', 'left', 'top');
      caption(ctx, rx + 20, y + 16, r[3], rw - 24, COL.faint,
              '10.5px -apple-system, sans-serif');
      y += 42;
    }
    y += 6;
    const lines = [['A = Z + N = ' + M.p + ' + ' + M.n + ' = ' + M.A, COL.pos],
                   ['q = Z − e = ' + M.p + ' − ' + M.e + ' = '
                    + signed(M.q), M.q === 0 ? COL.pos : COL.live],
                   [(M.p ? M.name + ' — ' + M.ion : 'no element'),
                    M.p ? COL.text : COL.faint],
                   [M.hasNuc ? (M.stable ? 'stable nucleus' : 'unstable nucleus') : '',
                    M.stable ? COL.pos : COL.ref]];
    for(const l of lines){
      if(!l[0]) continue;
      label(ctx, rx, y, l[0], l[1], 'italic 13px Georgia, serif', 'left', 'top');
      y += 20;
    }
    y += 8;
    label(ctx, rx, y, 'the same atom, drawn', COL.faint,
          '10px -apple-system, sans-serif', 'left', 'top');
    const room = Math.min(rw, G.L.bot - (y + 16));
    if(room > 70){
      const s = room / (2 * ATOM_HALF);
      drawAtomPicture(ctx, rx + room / 2, y + 16 + room / 2, s, M, {jiggle: 0});
    }
  } else {
    /* a narrow stage has no second column, so the four facts go under the box
       as plain lines rather than the view simply drawing a square */
    let y = G.by + G.side + 10;
    const lines = [['protons ' + M.p + ' · neutrons ' + M.n + ' · electrons ' + M.e,
                    COL.text],
                   ['A = Z + N = ' + M.A + ' · q = Z − e = ' + signed(M.q),
                    COL.pos],
                   [(M.p ? M.name + ' — ' + M.ion : 'no element'), M.p ? COL.text : COL.faint],
                   [M.hasNuc ? (M.stable ? 'stable nucleus' : 'unstable nucleus') : '',
                    M.stable ? COL.pos : COL.ref]];
    for(const l of lines){
      if(!l[0] || y + 16 > G.L.bot) continue;
      label(ctx, G.x0, y, l[0], l[1], '11.5px -apple-system, sans-serif', 'left', 'top');
      y += 17;
    }
  }
  drawCaption(ctx, G.L);
}
function symbolCaption(M){
  return 'PhET’s second screen. The nuclear symbol carries the same three integers in fixed places: '
    + 'the mass number A above the atomic number Z on the left, the charge on the right shoulder. '
    + 'Here that is ' + (M.p ? M.sym : '?') + ' with A = ' + M.A + ', Z = ' + M.p + ' and charge '
    + plain(M.chargeStr) + '. Note what the symbol does NOT say: the neutron count appears only as '
    + 'A − Z, and the electron count only through the charge — so '
    + (M.p ? M.sym + '-' + M.A : 'a symbol') + ' and its ion are the same nuclide. '
    + 'The charge is written ' + (M.st.notation === 'first' ? 'sign first (+2)' : 'sign last (2+)')
    + '; PhET ships both conventions as a preference and defaults to sign last, which is what '
    + 'chemistry writes.';
}
function symbolCaptionShort(M){
  return 'Mass number over atomic number, charge on the shoulder — the same three integers.';
}
