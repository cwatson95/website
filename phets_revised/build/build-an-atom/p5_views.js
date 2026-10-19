
/* ================================================================== *
 *  view 3 — the game (PhET's third screen)                            *
 * ================================================================== */
const LEVEL_BLURB = [
  'find the element, from a drawing or from the counts',
  'find the mass number or the charge',
  'fill in one box of the symbol',
  'fill in the whole symbol, or build the atom from one',
];
const PROMPT = {
  'schematic-to-element': 'Find the element:',
  'counts-to-element': 'Find the element:',
  'schematic-to-charge': 'What is the total charge?',
  'counts-to-charge': 'What is the total charge?',
  'schematic-to-mass-number': 'What is the mass number?',
  'counts-to-mass-number': 'What is the mass number?',
  'schematic-to-symbol-charge': 'Fill in the charge:',
  'counts-to-symbol-charge': 'Fill in the charge:',
  'schematic-to-symbol-mass-number': 'Fill in the mass number:',
  'counts-to-symbol-mass-number': 'Fill in the mass number:',
  'schematic-to-symbol-proton-count': 'Fill in the atomic number:',
  'schematic-to-symbol-all': 'Fill in the whole symbol:',
  'counts-to-symbol-all': 'Fill in the whole symbol:',
  'symbol-to-schematic': 'Build this atom:',
  'symbol-to-counts': 'How many of each?',
};
const FIELD_NAME = {element: 'element', protons: 'protons', neutrons: 'neutrons',
                    electrons: 'electrons', mass: 'mass number', charge: 'charge'};
/* All the game's hit rectangles come out of gameGeo, which draws nothing, so
   a click and the picture cannot disagree. */
function gameGeo(ctx, W, H, M){
  const L = layout(ctx, W, H, gameCaption(M), gameCaptionShort(M));
  const x0 = 12, w = usableW(W), narrow = narrowStage(W);
  const G = {L: L, x0: x0, w: w, narrow: narrow, cards: null, pt: null};
  if(GAME.phase === 'idle'){
    /* two columns whatever the width: four cards stacked do not fit a 380 px
       stage, and a card that overflows lands on the caption */
    const cols = 2, rows = Math.ceil(PHET.numLevels / cols), gap = 12;
    const cw = (w - (cols - 1) * gap) / cols;
    const chh = Math.min(96, Math.max(46, (L.bot - L.top - 30 - (rows - 1) * gap) / rows));
    G.cards = [];
    for(let i = 0; i < PHET.numLevels; i++)
      G.cards.push(box(x0 + (i % cols) * (cw + gap),
                       L.top + 24 + Math.floor(i / cols) * (chh + gap), cw, chh));
    return G;
  }
  const c = gameCurrent();
  if(!c) return G;
  const top = L.top + 26;
  const half = narrow ? w : (w - 16) / 2;
  const fields = answerFields(c.type);
  G.top = top; G.half = half;
  /* on a narrow stage the answer block sits UNDER the question, so the
     question box has to give up exactly the height the answer needs -- a
     fixed question height pushed "set them in the panel" onto the caption at
     560 x 380, which the inline sweep missed because it swept the game in its
     idle phase only (Known-bad: a sweep at default settings is not a sweep) */
  const ansH = fields.length * 24 + 46;
  /* the question box is sized by what it CONTAINS: a list of three counts in a
     400 px square is a view that reads as empty */
  const qWant = {counts: 150, symbol: 260, schematic: 340}[questionMode(c.type)];
  G.qb = box(x0, top + 22, half, narrow
    ? Math.max(70, L.bot - top - 22 - ansH)
    : Math.max(90, Math.min(qWant, L.bot - top - 46)));
  G.ax = narrow ? x0 : x0 + half + 16;
  G.aw = half;
  G.ay0 = (narrow ? G.qb.y1 + 12 : top) + 16;
  /* what the ANSWER is drawn as: the periodic table for an element, a symbol
     box for anything that fills one in, a drawn atom for symbol-to-schematic,
     otherwise the bare fields.  Matching PhET's own screens, and it is what
     fills a view that was two-thirds empty. */
  G.ansKind = 'fields';
  if(fields.length === 1 && fields[0] === 'element'){
    G.ansKind = 'element';
    const g = ptGeo(G.ax, G.ay0, Math.min(G.aw, 18 * 22), 10);
    /* the table needs room for its own ten rows AND the line under it */
    if(g.y0 + g.h + 20 < L.bot - 4) G.pt = g;
  } else if(c.type.indexOf('symbol') >= 0 && c.type !== 'symbol-to-counts'
            && c.type !== 'symbol-to-schematic'){
    G.ansKind = 'symbol';
    const side = Math.min(G.aw - 8, L.bot - G.ay0 - 8, 230);
    if(side >= 110) G.ansBox = box(G.ax, G.ay0, side, side); else G.ansKind = 'fields';
  } else if(c.type === 'symbol-to-schematic'){
    G.ansKind = 'schematic';
    const side = Math.min(G.aw - 8, L.bot - G.ay0 - 8, 300);
    if(side >= 110) G.ansBox = box(G.ax, G.ay0, side, side); else G.ansKind = 'fields';
  }
  return G;
}
function drawLevelCards(ctx, G, M){
  const cards = G.cards;
  label(ctx, G.x0, G.L.top, 'Choose your level', COL.text,
        'italic 15px Georgia, serif', 'left', 'top');
  for(let i = 0; i < cards.length; i++){
    const b = cards[i];
    const on = ST.level === i + 1;
    ctx.fillStyle = on ? mix(COL.bg, COL.live, 0.22) : COL.panel;
    ctx.fillRect(b.x, b.y, b.w, b.h);
    frame(ctx, b, on ? COL.live : COL.edge);
    label(ctx, b.x + 12, b.y + 9, 'Level ' + (i + 1), on ? '#ffffff' : COL.text,
          'italic 15px Georgia, serif', 'left', 'top');
    caption(ctx, b.x + 12, b.y + 30, LEVEL_BLURB[i], b.w - 24, COL.faint,
            '11px -apple-system, sans-serif');
    label(ctx, b.x + b.w - 12, b.y + 9, 'best ' + GAME.best[i] + '/' + perfectScore(),
          GAME.best[i] === perfectScore() ? COL.pos : COL.faint,
          '11px -apple-system, sans-serif', 'right', 'top');
  }
  /* the fifteen challenge types, by level: the level screen was two thirds
     empty, and the type names are the clearest statement of what the game
     actually asks */
  const last = cards[cards.length - 1];
  let y = last.y1 + 22;
  if(y + 60 < G.L.bot){
    label(ctx, G.x0, y - 16, 'the fifteen challenge types — the name says what the question '
      + 'shows and what it asks for', COL.faint,
      '10.5px -apple-system, sans-serif', 'left', 'top');
    for(let i = 0; i < PHET.numLevels && y + 16 < G.L.bot; i++){
      label(ctx, G.x0, y, 'level ' + (i + 1), COL.dim,
            '11px -apple-system, sans-serif', 'left', 'top');
      y += caption(ctx, G.x0 + 54, y, GAME_TYPES[i].join('   ·   '),
                   Math.max(200, G.w - 60), COL.text, '11px -apple-system, sans-serif') + 6;
    }
    y += 4;
    if(y + 30 < G.L.bot){
      label(ctx, G.x0, y, 'the atoms come from PhET’s own pools: '
        + GAME_POOLS[0].length + ' for levels 1 and 2, ' + GAME_POOLS[2].length
        + ' for levels 3 and 4, and the schematic types take only Z < 3', COL.faint,
        '10.5px -apple-system, sans-serif', 'left', 'top');
    }
  }
  return cards;
}
function drawQuestion(ctx, b, c, M){
  /* the atom the question is ABOUT, shown the way the type says */
  const mode = questionMode(c.type);
  const QM = buildModel(Object.assign({}, M.st, {p: c.atom[0], n: c.atom[1], e: c.atom[2]}));
  if(mode === 'schematic'){
    const s = Math.min(b.w, b.h) / (2 * ATOM_HALF);
    drawAtomPicture(ctx, b.x + b.w / 2, b.y + b.h / 2, s, QM, {jiggle: 0});
  } else if(mode === 'counts'){
    const rows = [['Protons:', c.atom[0], COL.proton], ['Neutrons:', c.atom[1], COL.neutron],
                  ['Electrons:', c.atom[2], COL.electron]];
    const y0 = b.y + Math.max(0, (b.h - 3 * 30) / 2);
    for(let i = 0; i < 3; i++){
      disc(ctx, b.x + 14, y0 + i * 30 + 10, 7, rows[i][2]);
      label(ctx, b.x + 30, y0 + i * 30, rows[i][0], COL.dim,
            '13px -apple-system, sans-serif', 'left', 'top');
      label(ctx, b.x + 128, y0 + i * 30, String(rows[i][1]), COL.text,
            '15px -apple-system, sans-serif', 'left', 'top');
    }
  } else {
    const side = Math.min(b.w - 20, b.h - 20, 150);
    drawSymbolBox(ctx, box(b.x + (b.w - side) / 2, b.y + (b.h - side) / 2, side, side), QM, false);
  }
}
function drawGameView(ctx, W, H, M){
  const G = gameGeo(ctx, W, H, M);
  if(GAME.phase === 'idle'){
    drawLevelCards(ctx, G, M);
    drawCaption(ctx, G.L);
    return;
  }
  if(GAME.phase === 'done'){
    const bw = Math.min(360, G.w);
    const bh = Math.max(120, Math.min(170, G.L.bot - G.L.top - 24));
    const b = box(G.x0 + (G.w - bw) / 2, G.L.top + 12, bw, bh);
    ctx.fillStyle = COL.panel; ctx.fillRect(b.x, b.y, b.w, b.h);
    frame(ctx, b, GAME.score === perfectScore() ? COL.pos : COL.edge);
    label(ctx, b.x + b.w / 2, b.y + 12, 'Level ' + GAME.level + ' finished', COL.text,
          'italic 17px Georgia, serif', 'center', 'top');
    label(ctx, b.x + b.w / 2, b.y + 42, GAME.score + ' out of ' + perfectScore(),
          GAME.score === perfectScore() ? COL.pos : COL.ref,
          'italic 28px Georgia, serif', 'center', 'top');
    for(let i = 0; i < GAME.history.length; i++){
      const a = GAME.history[i];
      const x = b.x + b.w / 2 + (i - (GAME.history.length - 1) / 2) * 20, y = b.y + 88;
      disc(ctx, x, y, 7, a === 1 ? COL.pos : (a === 2 ? COL.ref : '#5b3040'));
      ring(ctx, x, y, 7, COL.edge, 1);
      label(ctx, x, y, a === 1 ? '2' : (a === 2 ? '1' : '0'), '#0b1206',
            '9px -apple-system, sans-serif', 'center', 'middle');
    }
    label(ctx, b.x + b.w / 2, b.y + 106,
          GAME.history.map(a => a === 1 ? '2' : (a === 2 ? '1' : '0')).join(' + ')
          + ' = ' + GAME.score, COL.dim, '12px -apple-system, sans-serif', 'center', 'top');
    label(ctx, b.x + b.w / 2, b.y + bh - 8, 'seed ' + GAME.seed
          + ' — the same seed replays it exactly',
          COL.faint, '10.5px -apple-system, sans-serif', 'center', 'bottom');
    drawCaption(ctx, G.L);
    return;
  }
  const c = gameCurrent();
  /* progress dots */
  for(let i = 0; i < PHET.challengesPerLevel; i++){
    const x = G.x0 + 8 + i * 18, y = G.L.top + 6;
    const done = i < GAME.history.length;
    const col = !done ? COL.panel : (GAME.history[i] === 1 ? COL.pos
      : (GAME.history[i] === 2 ? COL.ref : '#5b3040'));
    disc(ctx, x, y, 6, col);
    ring(ctx, x, y, 6, i === GAME.idx ? '#ffffff' : COL.edge, i === GAME.idx ? 1.6 : 1);
  }
  label(ctx, G.x0 + 8 + PHET.challengesPerLevel * 18 + 10, G.L.top,
        'level ' + GAME.level + ' · score ' + GAME.score + '/' + perfectScore()
        + ' · attempt ' + GAME.attempt, COL.dim,
        '11.5px -apple-system, sans-serif', 'left', 'top');
  const top = G.top, qb = G.qb;
  label(ctx, G.x0, top, PROMPT[c.type] || '?', COL.text,
        'italic 15px Georgia, serif', 'left', 'top');
  ctx.fillStyle = COL.panel; ctx.fillRect(qb.x, qb.y, qb.w, qb.h);
  frame(ctx, qb, COL.edge);
  drawQuestion(ctx, qb, c, M);
  /* the answer side */
  const ax = G.ax, aw = G.aw;
  let ay = G.ay0 - 16;
  label(ctx, ax, ay, 'your answer', COL.faint, '10px -apple-system, sans-serif', 'left', 'top');
  ay = G.ay0;
  const fields = answerFields(c.type);
  if(G.ansKind === 'element' && G.pt){
    drawPeriodicTable(ctx, G.pt, M, {highlight: GAME.given.element, reach: 18, maxZ: 118});
    ay = G.pt.y0 + G.pt.h + 6;
    label(ctx, ax, ay, 'click a cell — chosen: '
      + (GAME.given.element ? SYMBOL[GAME.given.element] + ', '
        + ENAME[GAME.given.element] : 'none'), COL.live,
      '11.5px -apple-system, sans-serif', 'left', 'top');
    ay += 18;
  } else if(G.ansKind === 'symbol'){
    /* PhET's own answer control: the symbol box with the asked-for slots
       carrying YOUR numbers and the rest taken from the question */
    drawSymbolBox(ctx, G.ansBox, answerSymbolModel(c, M), true);
    ay = G.ansBox.y1 + 8;
    label(ctx, ax, ay, answerFields(c.type).map(f => FIELD_NAME[f]).join(', ')
      + ' come from the panel', COL.faint,
      '10.5px -apple-system, sans-serif', 'left', 'top');
    ay += 18;
  } else if(G.ansKind === 'schematic'){
    const s = Math.min(G.ansBox.w, G.ansBox.h) / (2 * ATOM_HALF);
    const AM = buildModel(Object.assign({}, M.st, {p: GAME.given.protons,
      n: GAME.given.neutrons, e: GAME.given.electrons}));
    drawAtomPicture(ctx, G.ansBox.x + G.ansBox.w / 2, G.ansBox.y + G.ansBox.h / 2, s, AM,
                    {jiggle: 0});
    ay = G.ansBox.y1 + 8;
    label(ctx, ax, ay, 'protons ' + GAME.given.protons + ' · neutrons '
      + GAME.given.neutrons + ' · electrons ' + GAME.given.electrons, COL.live,
      '11.5px -apple-system, sans-serif', 'left', 'top');
    ay += 18;
  } else {
    for(const f of fields){
      const v = GAME.given[f];
      label(ctx, ax, ay, f === 'element' ? 'element' : FIELD_NAME[f], COL.faint,
            '10.5px -apple-system, sans-serif', 'left', 'top');
      label(ctx, ax + 92, ay - 2, f === 'charge'
        ? chargeString(v, M.st.notation === 'first')
        : (f === 'element' ? (v >= 1 ? SYMBOL[v] : '—') : String(v)),
        COL.live, 'italic 16px Georgia, serif', 'left', 'top');
      ay += 24;
    }
    ay += 4;
    if(ay + 14 < G.L.bot){
      label(ctx, ax, ay, 'set them in the panel, then check', COL.faint,
            '10.5px -apple-system, sans-serif', 'left', 'top');
      ay += 18;
    }
  }
  /* feedback */
  const fb = {ask: ['', COL.dim], wrong: ['not right — one more try, worth 1 point', COL.ref],
              right: ['right, ' + pointsFor(GAME.history[GAME.history.length - 1])
                      + ' point' + (GAME.history[GAME.history.length - 1] === 1 ? 's' : ''), COL.pos],
              shown: ['the answer was ' + answerText(c), COL.ref]}[GAME.phase];
  if(fb && fb[0] && ay + 22 < G.L.bot)
    ay += 6 + caption(ctx, ax, ay + 6, fb[0], aw, fb[1], 'italic 14px Georgia, serif');
  /* the level's five challenges, by type, with what each one scored: the
     lower half of a 820 px stage was empty, and this is the clearest
     statement of what the level is asking */
  {
    /* below BOTH columns: the answer side can run lower than the question box,
       and a list started under the question alone collides with it */
    let ly = Math.max(G.qb.y1, ay) + 18;
    const lw = Math.min(300, G.half - 60);
    if(!G.narrow && ly + 22 + GAME.set.length * 15 < G.L.bot){
      label(ctx, G.x0, ly, 'this level, challenge by challenge', COL.faint,
            '10.5px -apple-system, sans-serif', 'left', 'top');
      ly += 16;
      for(let i = 0; i < GAME.set.length; i++){
        const done = i < GAME.history.length;
        const got = done ? pointsFor(GAME.history[i]) : null;
        label(ctx, G.x0, ly, (i + 1) + '.', i === GAME.idx ? COL.text : COL.faint,
              '11px -apple-system, sans-serif', 'left', 'top');
        label(ctx, G.x0 + 18, ly, GAME.set[i].type,
              i === GAME.idx ? COL.live : (done ? COL.dim : COL.faint),
              '11px -apple-system, sans-serif', 'left', 'top');
        label(ctx, G.x0 + lw, ly, done ? got + (got === 1 ? ' point' : ' points')
              : (i === GAME.idx ? 'now' : ''),
              done ? (got === 2 ? COL.pos : (got === 1 ? COL.ref : '#a85068')) : COL.faint,
              '11px -apple-system, sans-serif', 'left', 'top');
        ly += 15;
      }
    }
  }
  drawCaption(ctx, G.L);
}
/* the symbol box the answer side shows: the slots the challenge ASKS for carry
   the player's numbers, the rest are the question's own.  A light object, not
   a full model — drawSymbolBox reads only these five fields. */
function answerSymbolModel(c, M){
  const fields = answerFields(c.type);
  const has = f => fields.indexOf(f) >= 0;
  const p = has('protons') ? GAME.given.protons : c.atom[0];
  const A = has('mass') ? GAME.given.mass : c.atom[0] + c.atom[1];
  const q = has('charge') ? GAME.given.charge : c.atom[0] - c.atom[2];
  return {p: p, A: A, q: q, sym: elementSymbol(p), hasNuc: true,
          chargeStr: chargeString(q, M.st.notation === 'first')};
}
function answerText(c){
  const a = correctAnswer(c.type, c.atom);
  const parts = [];
  for(const f in a){
    if(f === 'element') parts.push(ENAME[a[f]] + ' (' + SYMBOL[a[f]] + ')');
    else if(f === 'charge') parts.push('charge ' + chargeString(a[f], false));
    else parts.push(FIELD_NAME[f] + ' ' + a[f]);
  }
  return parts.join(', ');
}
function gameCaption(M){
  if(GAME.phase === 'idle')
    return 'PhET’s third screen. Four levels, ' + PHET.challengesPerLevel + ' challenges each, '
      + PHET.pointsFirst + ' points for a right answer first time and ' + PHET.pointsSecond
      + ' for a right answer second time — ' + perfectScore() + ' for a perfect level. The '
      + 'challenges come from PhET’s own four pools of atoms (32 for levels 1 and 2, 60 for '
      + 'levels 3 and 4) and its own type lists, under its own rules: a type is never posed twice '
      + 'in a row, a challenge that DRAWS the atom uses Z < 3 so the picture stays readable, every '
      + 'other type uses Z ≥ 4, and a charge question asks for a charged atom about half the '
      + 'time. The generator here is seeded, so a level replays exactly; selfTest walks 16 000 '
      + 'generated levels and checks that every challenge is answerable.';
  const c = gameCurrent();
  if(!c)
    return 'Level ' + GAME.level + ' is over: ' + GAME.score + ' of a possible ' + perfectScore()
      + ', from ' + GAME.history.map(a => a === 1 ? '2' : (a === 2 ? '1' : '0')).join(' + ')
      + '. The five challenges were ' + GAME.set.map(s => s.type).join(', ') + '. '
      + 'The seed was ' + GAME.seed + ' — the control’s seed mixed with the level '
      + 'number, so the same settings replay this level exactly and the four levels of one '
      + 'seed are four independent runs.';
  const t = c.type;
  return 'Level ' + GAME.level + ', challenge ' + Math.min(GAME.idx + 1, PHET.challengesPerLevel)
    + ' of ' + PHET.challengesPerLevel + ', type "' + t + '" — the name says what the question '
    + 'shows and what it asks for. Score so far ' + GAME.score + ' of a possible ' + perfectScore()
    + '. This is attempt ' + GAME.attempt + ', worth ' + pointsFor(GAME.attempt) + '. '
    + 'The seed is ' + GAME.seed + ': the same seed and level give the same five challenges in the '
    + 'same order, which is what makes the game testable at all.';
}
function gameCaptionShort(M){
  return 'Four levels of five challenges, 2 points first try and 1 second — PhET’s scoring, '
    + 'from a seeded generator.';
}

/* ================================================================== *
 *  view 4 — the counting                                              *
 * ================================================================== */
function countGeo(ctx, W, H, M){
  const L = layoutMin(ctx, W, H, countCaption(M), countCaptionShort(M),
                      16 + 11 * 10 + 34 + 12);
  const x0 = 12, w = usableW(W), narrow = narrowStage(W);
  const gridW = narrow ? w : Math.max(220, w * 0.72);
  return {L: L, x0: x0, w: w, narrow: narrow, gridW: gridW,
          rightX: x0 + gridW + 18, rightW: w - gridW - 18};
}
function drawCountView(ctx, W, H, M){
  const G = countGeo(ctx, W, H, M);
  const st = M.st;
  const NP = PHET.numProtons, NN = PHET.numNeutrons;
  const availH = G.L.bot - G.L.top - 34;
  const cw = Math.max(10, Math.min((G.gridW - 34) / (NN + 1), availH / (NP + 1)));
  const gx = G.x0 + 30, gy = G.L.top + 16;
  panelTitleFit(ctx, box(gx, gy, (NN + 1) * cw, (NP + 1) * cw),
                'every nucleus the buckets can make', 'the buckets\u2019 nuclides');
  for(let p = 0; p <= NP; p++){
    for(let n = 0; n <= NN; n++){
      const x = gx + n * cw, y = gy + (NP - p) * cw;
      const stb = p > 0 && isStable(p, n);
      let col;
      if(st.countMode === 'stability') col = (p + n === 0) ? COL.panel
        : (stb ? mix(COL.bg, COL.pos, 0.85) : mix(COL.bg, COL.ref, 0.22));
      else if(st.countMode === 'element') col = p === 0 ? COL.panel
        : shade(neonCss(p / NP), 0.85);
      else col = (p + n === 0) ? COL.panel : shade(neonCss((p + n) / (NP + NN)), 0.9);
      ctx.fillStyle = col; ctx.fillRect(x, y, cw - 1, cw - 1);
      if(cw >= 17 && p > 0){
        ctx.fillStyle = stb && st.countMode === 'stability' ? '#0b1206' : '#cfd4de';
        ctx.font = Math.max(7, Math.round(cw * 0.34)) + 'px -apple-system, sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(String(p + n), x + cw / 2, y + cw / 2);
      }
    }
  }
  /* the one you have built */
  if(M.p <= NP && M.n <= NN){
    const x = gx + M.n * cw, y = gy + (NP - M.p) * cw;
    ctx.strokeStyle = COL.live; ctx.lineWidth = 2.2;
    ctx.strokeRect(x - 1, y - 1, cw + 1, cw + 1);
  }
  /* axes by hand: the cells are the units */
  for(let p = 0; p <= NP; p += 1){
    if(cw < 14 && p % 2) continue;
    label(ctx, gx - 5, gy + (NP - p) * cw + cw / 2, String(p), COL.faint,
          '9.5px -apple-system, sans-serif', 'right', 'middle');
  }
  for(let n = 0; n <= NN; n += 1){
    if(cw < 14 && n % 2) continue;
    label(ctx, gx + n * cw + cw / 2, gy + (NP + 1) * cw + 3, String(n), COL.faint,
          '9.5px -apple-system, sans-serif', 'center', 'top');
  }
  label(ctx, gx + (NN + 1) * cw / 2, gy + (NP + 1) * cw + 16, 'neutrons N', COL.dim,
        '10.5px -apple-system, sans-serif', 'center', 'top');
  label(ctx, gx - 20, gy + (NP + 1) * cw / 2, 'Z', COL.dim,
        '10.5px -apple-system, sans-serif', 'center', 'middle');
  /* the charge strip and the census */
  if(!G.narrow){
    let y = G.L.top + 16;
    const rw = G.rightW;
    panelTitleFit(ctx, box(G.rightX, y, rw, 10), 'charge, for Z = ' + M.p, 'charge');
    y += 8;
    const sw = Math.max(8, Math.min(24, rw / (PHET.numElectrons + 1)));
    for(let e = 0; e <= PHET.numElectrons; e++){
      const q = M.p - e;
      const x = G.rightX + e * sw;
      const col = q === 0 ? COL.pos : (q > 0 ? COL.proton : COL.electron);
      ctx.fillStyle = e === M.e ? col : shade(col, 0.45);
      ctx.fillRect(x, y, sw - 2, 20);
      if(sw >= 14)
        label(ctx, x + (sw - 2) / 2, y + 10, String(q), e === M.e ? '#0b1206' : COL.text,
              '9.5px -apple-system, sans-serif', 'center', 'middle');
    }
    y += 24 + caption(ctx, G.rightX, y + 24, 'electrons 0 … ' + PHET.numElectrons
      + ' — one of them, e = Z, is neutral', rw, COL.faint,
      '10px -apple-system, sans-serif') + 8;
    const C = M.census, P = M.parity;
    const rows = [
      ['configurations (p, n, e)', String(C.total), COL.text],
      ['of them neutral', String(C.neutral), COL.pos],
      ['of them ions', String(C.ions), COL.live],
      ['with a stable nucleus', String(C.stableConfigs), COL.pos],
      ['distinct stable nuclides here', String(C.stablePN.length), COL.pos],
      ['stable nuclides with Z ≤ 10, anywhere', String(C.stablePN.length), COL.str],
      ['elements reachable', '10, H to Ne', COL.text],
      ['odd-odd stable nuclides, ALL of them', String(P.oddOdd.length) + ': '
        + P.oddOdd.map(r => SYMBOL[r[0]] + '-' + (r[0] + r[1])).join(', '), COL.ref],
    ];
    for(const r of rows){
      if(y + 16 > G.L.bot) break;
      y += kvRow(ctx, G.rightX, y, rw, r[0], r[1], r[2]);
    }
  }
  drawCaption(ctx, G.L);
}
function countCaption(M){
  const C = M.census, P = M.parity;
  return 'The whole space the buckets can reach: ' + PHET.numProtons + ' protons by '
    + PHET.numNeutrons + ' neutrons by ' + PHET.numElectrons + ' electrons is '
    + C.total + ' configurations, and selfTest checks the element, the mass number, the charge and '
    + 'the stability of every single one against an independently written expression. '
    + C.neutral + ' of them are neutral, ' + C.ions + ' are ions, and ' + C.stableConfigs
    + ' have a stable nucleus — which is ' + C.stablePN.length + ' distinct stable nuclides '
    + 'times the ' + (PHET.numElectrons + 1) + ' electron counts, because stability does not care '
    + 'about electrons. Those ' + C.stablePN.length + ' are EVERY stable nuclide with Z ≤ 10 '
    + 'that exists; the 13-neutron bucket is one more than neon-22 needs. Note the four odd-odd '
    + 'cells (' + P.oddOdd.map(r => SYMBOL[r[0]] + '-' + (r[0] + r[1])).join(', ') + '): they are '
    + 'the only four odd-odd stable nuclides in the whole chart, and all four are in this corner.';
}
function countCaptionShort(M){
  return 'All ' + M.census.total + ' bucket configurations, coloured by ' + M.st.countMode + '.';
}

/* ================================================================== *
 *  view 5 — the chart of nuclides                                     *
 * ================================================================== */
const MAGIC = [2, 8, 20, 28, 50, 82, 126];
/* legendBox's own sizing rule, repeated here so the caller can choose the
   corner itself; the placement tries each corner against the drawn marks */
function chartLegendPlace(ctx, b, items, marks){
  ctx.font = '10.5px -apple-system, sans-serif';
  let w = 0;
  for(const it of items) w = Math.max(w, ctx.measureText(plain(it[1])).width);
  const bw = w + 26, bh = items.length * 15 + 8;
  if(bw > b.w - 16 || bh > b.h - 16) return null;
  const cands = [[b.x1 - bw - 8, b.y1 - bh - 8], [b.x + 8, b.y + 8],
                 [b.x1 - bw - 8, b.y + 8], [b.x + 8, b.y1 - bh - 8]];
  for(const [cx, cy] of cands){
    const r = {x: cx, y: cy, w: bw, h: bh};
    let hit = false;
    for(const q of marks) if(rectsHit(r, q)){ hit = true; break; }
    if(!hit) for(const q of LABEL_RECTS) if(rectsHit(r, q)){ hit = true; break; }
    if(!hit) return legendBox(ctx, cx, cy, items);
  }
  return null;
}
let CHART_LEGEND = null;
let CHART_MARKS = [];
/* PhET's table against the independent one.  Both lists are emitted by
   derive.py and pinned in selfTest, so the labels on this view cannot drift
   away from the tables they describe. */
const PHET_ONLY = [[32, 44]];
const NUBASE_ONLY = [[24, 26], [30, 40], [52, 71], [54, 70], [54, 80], [56, 76],
                     [58, 80], [58, 84], [74, 109], [82, 122]];
function chartGeo(ctx, W, H, M){
  const L = layoutMin(ctx, W, H, chartCaption(M), chartCaptionShort(M), 16 + 90 + AXIS_BOT + 12);
  const x0 = 12, w = usableW(W), narrow = narrowStage(W);
  const mainW = narrow ? w : Math.max(240, w * 0.66);
  const b = box(x0 + 42, L.top + 16, mainW - 54, Math.max(90, L.bot - L.top - 16 - AXIS_BOT));
  return {L: L, x0: x0, w: w, narrow: narrow, b: b,
          rightX: x0 + mainW + 16, rightW: w - mainW - 16};
}
function drawChartView(ctx, W, H, M){
  const G = chartGeo(ctx, W, H, M);
  const st = M.st;
  const Zmax = st.chartZmax, Nmax = Math.round(Zmax * 1.62) + 4;
  const b = G.b;
  panelTitleFit(ctx, b, 'the stable nuclides, N against Z', 'stable nuclides');
  axesR(ctx, b, 0, Nmax, 0, Zmax, {nx: 7, ny: 6, xlab: 'neutron number N', ylab: 'proton number Z',
       xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 0)});
  const X = n => b.x + b.w * n / Nmax, Y = z => b.y1 - b.h * z / Zmax;
  const cw = Math.max(1.4, Math.min(b.w / Nmax, b.h / Zmax));
  if(st.chartMagic){
    for(const m of MAGIC){
      if(m <= Zmax){
        ctx.strokeStyle = rgba(COL.str, 0.22); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(b.x, Y(m)); ctx.lineTo(b.x1, Y(m)); ctx.stroke();
      }
      if(m <= Nmax){
        ctx.strokeStyle = rgba(COL.str, 0.22); ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(X(m), b.y); ctx.lineTo(X(m), b.y1); ctx.stroke();
      }
    }
  }
  /* N = Z, clipped to the box by polyline's data-space clip */
  polyline(ctx, b, [0, Nmax], [0, Nmax], 0, Nmax, 0, Zmax, rgba(COL.ref, 0.75), 1.2, [5, 4]);
  CHART_MARKS = [];
  for(const [z, n] of stableList()){
    if(z > Zmax || n > Nmax) continue;
    ctx.fillStyle = mix(COL.bg, COL.pos, 0.92);
    ctx.fillRect(X(n) - cw / 2, Y(z) - cw / 2, cw, cw);
    /* recorded so selfTest can assert the legend sits on nothing: a display
       check has to measure the thing it claims to check (Known-bad) */
    CHART_MARKS.push({x: X(n) - cw / 2, y: Y(z) - cw / 2, w: cw, h: cw});
  }
  if(st.chartCompare){
    for(const [z, n] of NUBASE_ONLY){
      if(z > Zmax || n > Nmax) continue;
      ctx.fillStyle = COL.ref;
      ctx.fillRect(X(n) - cw / 2 - 1, Y(z) - cw / 2 - 1, cw + 2, cw + 2);
    }
    for(const [z, n] of PHET_ONLY){
      if(z > Zmax || n > Nmax) continue;
      ring(ctx, X(n), Y(z), Math.max(3, cw), COL.live, 1.6);
    }
  }
  /* the two empty rows, the heaviest, and the box the buckets reach: the
     RULES first, the labels for them after the legend, so labelIfClear can
     dodge it */
  for(const z of M.noStable){
    if(z > Zmax) continue;
    ctx.strokeStyle = rgba(COL.live, 0.8); ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(b.x, Y(z)); ctx.lineTo(b.x1, Y(z)); ctx.stroke();
  }
  const hz = M.heaviest[0], hn = M.heaviest[1];
  if(hz <= Zmax && hn <= Nmax) ring(ctx, X(hn), Y(hz), Math.max(4, cw + 2), COL.pos, 1.6);
  ctx.strokeStyle = COL.live; ctx.lineWidth = 1.2;
  ctx.strokeRect(X(0), Y(PHET.numProtons), X(PHET.numNeutrons) - X(0),
                 Y(0) - Y(PHET.numProtons));
  /* the current nuclide */
  if(M.hasNuc && M.p <= Zmax && M.n <= Nmax)
    ring(ctx, X(M.n), Y(M.p), Math.max(4, cw + 3), COL.live, 1.8);
  const items = [[mix(COL.bg, COL.pos, 0.92), 'PhET’s table (' + M.nStable + ')'],
                 [rgba(COL.ref, 0.9), 'N = Z']];
  /* a legend entry for something that was NOT drawn is a false statement
     about the picture (Known-bad): at Z up to 12 none of the eleven disputed
     nuclides is on the chart, so neither entry belongs there.  Count what is
     inside the range and name only that. */
  const nOnly = NUBASE_ONLY.filter(r => r[0] <= Zmax && r[1] <= Nmax).length;
  const pOnly = PHET_ONLY.filter(r => r[0] <= Zmax && r[1] <= Nmax).length;
  let nMagic = 0;
  for(const m of MAGIC) if(m <= Zmax || m <= Nmax) nMagic++;
  if(st.chartMagic && nMagic) items.push([rgba(COL.str, 0.6),
    'magic numbers (' + nMagic + ' of ' + MAGIC.length + ' in range)']);
  if(st.chartCompare && nOnly) items.push([COL.ref, 'stable only in NUBASE (' + nOnly + ')']);
  if(st.chartCompare && pOnly) items.push([COL.live, 'stable only in PhET (' + pOnly + ')']);
  /* legendAuto dodges polylines and labels only, and the nuclides are
     fillRects, so it put the legend over the top of the band (found in the
     PNG).  Place it in the first corner no DRAWN square touches -- bottom
     right first, because low Z with high N is empty for every setting -- and
     drop it when every corner is busy rather than draw a lying one
     (Known-bad).  selfTest re-measures this over the whole Z-range slider. */
  CHART_LEGEND = chartLegendPlace(ctx, b, items, CHART_MARKS);
  /* now the labels, which can dodge the legend because it is in LEGEND_RECTS */
  for(const z of M.noStable){
    if(z > Zmax) continue;
    labelIfClear(ctx, b.x1 - 4, Y(z) - 3, SYMBOL[z] + ' \u2014 no stable isotope', COL.live,
                 '10px -apple-system, sans-serif', 'right', 'bottom');
  }
  if(hz <= Zmax && hn <= Nmax)
    labelIfClear(ctx, X(hn) - 6, Y(hz) - 6, SYMBOL[hz] + '-' + (hz + hn) + ', the heaviest',
                 COL.pos, '10px -apple-system, sans-serif', 'right', 'bottom');
  labelIfClear(ctx, X(PHET.numNeutrons) + 5, Y(PHET.numProtons / 2), 'the buckets reach here',
               COL.live, '10px -apple-system, sans-serif', 'left', 'middle');
  /* the N/Z drift panel */
  if(!G.narrow && G.rightW > 130){
    const rb = box(G.rightX + 34, G.L.top + 16, G.rightW - 44,
                   Math.max(80, (G.L.bot - G.L.top - 16 - AXIS_BOT)));
    panelTitleFit(ctx, rb, 'N/Z along the valley', 'N/Z');
    axesR(ctx, rb, 0, Zmax, 0.9, 1.65, {nx: 4, ny: nyFor(rb.h), xlab: 'Z', ylab: 'N / Z',
         xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 2)});
    const zs = [], rs = [];
    for(let z = 1; z <= Zmax; z++){
      const row = STABLE[z] || [];
      if(!row.length) continue;
      let s = 0;
      for(const n of row) s += n / z;
      zs.push(z); rs.push(s / row.length);
    }
    polyline(ctx, rb, zs, rs, 0, Zmax, 0.9, 1.65, COL.pos, 1.6);
    polyline(ctx, rb, [0, Zmax], [1, 1], 0, Zmax, 0.9, 1.65, rgba(COL.ref, 0.8), 1.2, [5, 4]);
    labelIfClear(ctx, rb.x + 6, rb.y1 - 6, 'N = Z', COL.ref,
                 '10px -apple-system, sans-serif', 'left', 'bottom');
  }
  drawCaption(ctx, G.L);
}
function chartCaption(M){
  const hz = M.heaviest[0];
  return 'Stability is the one thing in this sim that is not arithmetic, and this is what it is '
    + 'instead: a table. PhET’s stableElementTable holds ' + M.nStable + ' nuclides, Z = 1 to '
    + hz + '. Drawn beside it is an independent one — NUBASE half-lives with NIST isotopic '
    + 'compositions, criterion "occurs in nature and has never been seen to decay" — which '
    + 'holds 253. The two agree on 243. PhET alone counts germanium-76, whose double-beta half-life '
    + 'of 1.9×10²¹ yr has actually been measured; the other alone counts ten '
    + '(Cr-50, Zn-70, Te-123, Xe-124, Xe-134, Ba-132, Ce-138, Ce-142, W-183, Pb-204) whose '
    + 'predicted decay has never been seen. Below Z = 24 they are IDENTICAL, so nothing this sim '
    + 'can build is in dispute. Both stop at lead: bismuth-209 is in neither, because its alpha '
    + 'decay was measured in 2003 at 2.0×10¹⁹ yr. Technetium and promethium have no '
    + 'stable isotope at all, which is why the chart has two empty rows. The dashed line is N = Z; '
    + 'the band leaves it above about Z = 20 and reaches N/Z = ' + fmt(M.heaviest[1] / hz, 3)
    + ' at lead-208, because Coulomb repulsion grows as Z² while the nuclear force saturates.';
}
function chartCaptionShort(M){
  return M.nStable + ' stable nuclides in PhET’s table against 253 in an independent one; '
    + 'they agree on 243.';
}

/* ================================================================== *
 *  view 6 — mass and binding                                          *
 * ================================================================== */
function massGeo(ctx, W, H, M){
  const gap = 30, MASS_ROW0 = 14;
  /* the two panels need 2 x AXIS_BOT, the mass row, the gap and 56 px each;
     ask layoutMin for that much stage before it keeps the long caption */
  const L = layoutMin(ctx, W, H, massCaption(M), massCaptionShort(M),
                      2 * AXIS_BOT + MASS_ROW0 + gap + 2 * 56 + 20);
  const x0 = 12, w = usableW(W);
  const top = L.top + 16;
  /* the upper panel needs AXIS_BOT for its ticks PLUS a row for the atomic
     masses under the bars, or the two collide at every canvas size */
  const MASS_ROW = 14;
  const h = L.bot - top;
  const topH = Math.max(56, (h - gap - 2 * AXIS_BOT - MASS_ROW) * 0.42);
  const botH = Math.max(56, h - gap - 2 * AXIS_BOT - MASS_ROW - topH);
  return {L: L, x0: x0, w: w, massRow: MASS_ROW,
          a: box(x0 + 46, top, w - 58, topH),
          b: box(x0 + 46, top + topH + AXIS_BOT + MASS_ROW + gap, w - 58, botH)};
}
function drawMassView(ctx, W, H, M){
  const G = massGeo(ctx, W, H, M);
  const st = M.st;
  /* --- the isotopes of this element --- */
  const iso = isotopesOf(M.p).filter(it => !isTrace(it.ab) || !st.showAbund);
  const all = isotopesOf(M.p);
  const a = G.a;
  if(!all.length){
    panelTitleFit(ctx, a, 'isotopes of ' + (M.p ? M.name : 'nothing'), 'isotopes');
    caption(ctx, a.x, a.y + 8, M.p
      ? ('PhET’s isotope table stops at argon (Z = 18), so there is no measured mass or '
         + 'abundance here for ' + M.name + ' — the sim says so rather than guessing.')
      : 'No protons, so no element and no isotopes.', a.w, COL.faint);
  } else {
    const As = all.map(it => it.A);
    const lo = Math.min.apply(null, As) - 1, hi = Math.max.apply(null, As) + 1;
    panelTitleFit(ctx, a, 'the isotopes of ' + M.name + ', by mass number A',
                  'isotopes of ' + M.name + ', by A');
    axesR(ctx, a, lo, hi, 0, 100, {xticks: intTicks(lo, hi), ny: nyFor(a.h),
         ylab: 'abundance / %',
         xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 0)});
    const bw = Math.max(6, Math.min(34, a.w / (hi - lo) * 0.55));
    var bars = [];
    for(const it of all){
      const x = a.x + a.w * (it.A - lo) / (hi - lo);
      const pct = isTrace(it.ab) ? 0 : it.ab * 100;
      const hgt = a.h * pct / 100;
      const on = it.A === M.A;
      ctx.fillStyle = on ? COL.live : mix(COL.bg, COL.pos, 0.85);
      ctx.fillRect(x - bw / 2, a.y1 - hgt, bw, Math.max(hgt, 1));
      bars.push({x: x - bw / 2, y: a.y1 - hgt, w: bw, h: Math.max(hgt, 1)});
      if(isTrace(it.ab)){
        label(ctx, x, a.y1 - 4, 'traces', COL.ref, '9.5px -apple-system, sans-serif',
              'center', 'bottom');
      } else if(bw >= 12){
        labelIfClear(ctx, x, a.y1 - hgt - 3, fmt(pct, pct < 1 ? 3 : 2) + '%',
                     on ? COL.live : COL.dim, '9.5px -apple-system, sans-serif',
                     'center', 'bottom');
      }
      labelIfClear(ctx, x, a.y1 + 20, sigf(it.mass, 9) + ' u', COL.faint,
                   '9px -apple-system, sans-serif', 'center', 'top');
    }
    /* the mean, and PhET's published standard weight.  The bars are fillRects
       and the label registry has never seen them, so the annotation has to be
       given their rectangles or it lands on the tallest bar (found in the
       PNG). */
    if(M.weighted != null){
      annotate(ctx, a, bars, [
        ['Σ ab × m = ' + fmt(M.weighted, 6) + ' u', COL.pos],
        ['standard atomic weight ' + fmt(M.standard, 6) + ' u  (gap '
         + sigf(Math.abs(M.weighted - M.standard) / M.standard, 2) + ')', COL.ref]]);
    }
  }
  /* --- binding energy per nucleon --- */
  const b = G.b;
  const pts = memo('bind', st.bindAll ? 'all' : 'low', () => {
    const xs = [], ys = [];
    for(const r of DEXC){
      const z = r[0], A = r[1];
      if(!isStable(z, A - z)) continue;
      if(!st.bindAll && z > 18) continue;
      const v = bindingPerNucleonExc(z, A);
      if(v == null) continue;
      xs.push(A); ys.push(v);
    }
    /* sorted by A so the polyline is a curve and not a scribble */
    const idx = xs.map((_, i) => i).sort((p, q) => xs[p] - xs[q]);
    return {xs: idx.map(i => xs[i]), ys: idx.map(i => ys[i])};
  });
  const Amax = st.bindAll ? 212 : 42;
  panelTitleFit(ctx, b, 'binding energy per nucleon, from the measured masses',
                'binding energy per nucleon');
  axesR(ctx, b, 0, Amax, 0, 9.4, {nx: 6, ny: nyFor(b.h), xlab: 'mass number A',
       ylab: 'B / A  (MeV)', xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  polyline(ctx, b, pts.xs, pts.ys, 0, Amax, 0, 9.4, mix(COL.bg, COL.pos, 0.85), 1.4);
  for(let i = 0; i < pts.xs.length; i++){
    const x = b.x + b.w * pts.xs[i] / Amax, y = b.y1 - b.h * pts.ys[i] / 9.4;
    if(x < b.x || x > b.x1 || y < b.y || y > b.y1) continue;
    disc(ctx, x, y, 1.7, mix(COL.bg, COL.pos, 0.9));
  }
  /* Ni-62, the real maximum */
  const nix = b.x + b.w * 62 / Amax, niy = b.y1 - b.h * bindingPerNucleonExc(28, 62) / 9.4;
  if(62 <= Amax){
    ring(ctx, nix, niy, 4, COL.ref, 1.6);
    labelIfClear(ctx, nix + 6, niy - 4, 'Ni-62, '
      + fmt(bindingPerNucleonExc(28, 62), 3) + ' MeV — the maximum', COL.ref,
      '10px -apple-system, sans-serif', 'left', 'bottom');
  }
  if(M.BperA != null && M.A <= Amax){
    const x = b.x + b.w * M.A / Amax, y = b.y1 - b.h * M.BperA / 9.4;
    ring(ctx, x, y, 5, COL.live, 1.8);
    labelIfClear(ctx, x, y + 7, M.sym + '-' + M.A + ', ' + fmt(M.BperA, 3), COL.live,
                 '10px -apple-system, sans-serif', 'center', 'top');
  }
  drawCaption(ctx, G.L);
}
function massCaption(M){
  const s = 'Measured data, and what it buys. The bars are PhET’s own isotope table (Z ≤ 18, '
    + 'from AME/NIST): the natural abundance of each isotope with its atomic mass printed under it. '
    + 'Their mean, Σ (abundance × mass), IS the standard atomic weight '
    + (M.weighted != null ? ('— ' + fmt(M.weighted, 6) + ' u here against PhET’s published '
      + fmt(M.standard, 6) + '. ') : '— for the elements that have one. ')
    + 'The worst gap over all eighteen is 1.4×10⁻⁴ relative, at lithium, and that is '
    + 'not an error in either: lithium’s isotopic composition varies between natural sources by '
    + 'enough that IUPAC gives it an interval rather than a number. PhET’s masses agree with '
    + 'the independent NUBASE mass excesses to 1.6×10⁻⁶ u and its abundances with NIST '
    + 'to 3.2×10⁻³ percentage points. '
    + 'The curve below is the binding energy per nucleon of every stable nuclide, computed from the '
    + 'measured masses by B = [Z m(¹H) + N mₙ − m(A, Z)] c² — no mass '
    + 'formula, no fit. It peaks at nickel-62 ('
    + fmt(bindingPerNucleonExc(28, 62), 4) + ' MeV per nucleon, just above iron-56 at '
    + fmt(bindingPerNucleonExc(26, 56), 4) + '), which is why fusion releases energy below it and '
    + 'fission above. The masses for it come from the INDEPENDENT NUBASE mass excesses, because '
    + 'PhET’s own table stops at argon.';
  return s;
}
function massCaptionShort(M){
  return 'Measured isotope masses and abundances, their mean (the atomic weight), and the binding '
    + 'energy they imply.';
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx, W, H, M){
  POLY_SEGS = []; LEGEND_RECTS = []; LABEL_RECTS = [];
  ctx.fillStyle = COL.bg; ctx.fillRect(0, 0, W, H);
  const v = M.view;
  if(v === 'atom') drawAtomView(ctx, W, H, M);
  else if(v === 'symbol') drawSymbolView(ctx, W, H, M);
  else if(v === 'game') drawGameView(ctx, W, H, M);
  else if(v === 'counting') drawCountView(ctx, W, H, M);
  else if(v === 'chart') drawChartView(ctx, W, H, M);
  else drawMassView(ctx, W, H, M);
}

function makeScene(canvas){
  const S = {st: ST, W: 1400, H: 820};
  S.model = () => buildModel(ST);
  /* the context is fetched INSIDE the draw, never cached at boot: a harness
     that swaps in a fresh recorder per frame would otherwise record nothing
     (Known-bad, polyhedra.html) */
  S.draw = function(){
    const ctx = canvas.getContext('2d');
    drawView(ctx, S.W, S.H, buildModel(ST));
  };
  /* the only animation in the file: the unstable-nucleus jiggle, and only on
     the two views that draw a live atom */
  S.step = function(){
    if(!ST.jiggle) return false;
    if(ST.view !== 'atom') return false;
    if(nucleusStable(ST.p, ST.n)) return false;
    FRAME.jig++;
    return true;
  };
  /* ---- the pointer ---- */
  S.pointer = function(type, x, y){
    const ctx = canvas.getContext('2d');
    if(ST.view === 'atom') return atomPointer(ctx, S, type, x, y);
    if(ST.view === 'game') return gamePointer(ctx, S, type, x, y);
    if(type === 'up'){ const had = DRAG.active; dragClear(); return had; }
    return false;
  };
  return S;
}
function dragClear(){ DRAG.active = false; DRAG.type = null; DRAG.from = null; }
function addToAtom(k){
  if(k === 'p' && ST.p < PHET.numProtons) ST.p++;
  else if(k === 'n' && ST.n < PHET.numNeutrons) ST.n++;
  else if(k === 'e' && ST.e < PHET.numElectrons) ST.e++;
}
function takeFromAtom(k){
  if(k === 'p' && ST.p > 0){ ST.p--; return true; }
  if(k === 'n' && ST.n > 0){ ST.n--; return true; }
  if(k === 'e' && ST.e > 0){ ST.e--; return true; }
  return false;
}
function atomPointer(ctx, S, type, x, y){
  const M = buildModel(ST), G = atomGeo(ctx, S.W, S.H, M);
  if(type === 'down'){
    const k = bucketHit(G.buckets, x, y);
    if(k){
      const left = k === 'p' ? M.leftP : (k === 'n' ? M.leftN : M.leftE);
      if(left <= 0) return false;
      DRAG.active = true; DRAG.type = k; DRAG.from = 'bucket'; DRAG.x = x; DRAG.y = y;
      return true;
    }
    /* inside the atom: pull the outermost particle of whatever you grabbed */
    const dx = (x - G.cx) / G.s, dy = (y - G.cy) / G.s, r = Math.sqrt(dx * dx + dy * dy);
    const rn = nucleusRadius(M.p + M.n, PHET.nucleonRadius);
    if(M.p + M.n > 0 && r <= rn + 2){
      const k2 = M.n > 0 ? 'n' : 'p';
      if(takeFromAtom(k2)){
        DRAG.active = true; DRAG.type = k2; DRAG.from = 'atom'; DRAG.x = x; DRAG.y = y;
        return true;
      }
    }
    if(M.e > 0 && r <= CAPTURE_ELECTRON && r > rn){
      if(takeFromAtom('e')){
        DRAG.active = true; DRAG.type = 'e'; DRAG.from = 'atom'; DRAG.x = x; DRAG.y = y;
        return true;
      }
    }
    /* clicking a periodic-table cell sets the proton count, with the neutrons
       of the most common isotope and a neutral electron count */
    if(G.pt){
      const z = ptHit(G.pt, x, y, PHET.numProtons);
      if(z){ setNuclide(z, MOSTN[z], z); return true; }
    }
    return false;
  }
  if(type === 'move'){
    if(!DRAG.active) return false;
    DRAG.x = x; DRAG.y = y; return true;
  }
  if(type === 'up'){
    if(!DRAG.active) return false;
    const dx = (x - G.cx) / G.s, dy = (y - G.cy) / G.s, r = Math.sqrt(dx * dx + dy * dy);
    const cap = DRAG.type === 'e' ? CAPTURE_ELECTRON : CAPTURE_NUCLEON;
    if(r <= cap) addToAtom(DRAG.type);
    dragClear();
    return true;
  }
  return false;
}
function setNuclide(p, n, e){
  ST.p = clamp(p | 0, 0, PHET.numProtons);
  ST.n = clamp(n | 0, 0, PHET.numNeutrons);
  ST.e = clamp(e | 0, 0, PHET.numElectrons);
}
function gamePointer(ctx, S, type, x, y){
  if(type !== 'down') return false;
  const G = gameGeo(ctx, S.W, S.H, buildModel(ST));
  if(GAME.phase === 'idle' && G.cards){
    for(let i = 0; i < G.cards.length; i++){
      const b = G.cards[i];
      if(x >= b.x && x <= b.x1 && y >= b.y && y <= b.y1){
        ST.level = i + 1; gameStart(ST); return true;
      }
    }
    return false;
  }
  if(GAME.phase === 'ask' && G.pt){
    const z = ptHit(G.pt, x, y, 118);
    if(z){ GAME.given.element = z; return true; }
  }
  return false;
}
