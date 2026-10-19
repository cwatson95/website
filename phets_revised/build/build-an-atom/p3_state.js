
/* ================================================================== *
 *  state, the model the views read, and the three text bars           *
 * ================================================================== */
const TABS = [['atom', 'the atom'], ['symbol', 'the symbol'], ['game', 'the game'],
              ['counting', 'the counting'], ['chart', 'chart of nuclides'],
              ['mass', 'mass and binding']];

const COL = {
  pos: '#b8ec4c',      /* green   — the computed thing, and "stable"      */
  ref: '#e8843a',      /* orange  — the reference value, and "unstable"   */
  live: '#cd35c4',     /* magenta — the nuclide you built, the held one   */
  str: '#5ac8e0',      /* cyan    — shells, axes, the table grid          */
  dim: '#8b93a6', text: '#cfd4de', faint: '#6f7789', bg: '#070b18',
  proton: '#e8843a', neutron: '#8b93a6', electron: '#5ac8e0',
  panel: '#10131b', edge: '#242a3a',
};
const RO_W = 300;                       /* the floating readout's footprint */

const MODELS = [{id: 'orbits', name: 'orbits'}, {id: 'cloud', name: 'cloud'}];
const NOTATIONS = [{id: 'last', name: '2+ (sign last)'}, {id: 'first', name: '+2 (sign first)'}];
const COUNT_MODES = [{id: 'stability', name: 'stable or not'},
                     {id: 'element', name: 'which element'},
                     {id: 'mass', name: 'mass number'}];

const DEFAULTS = {
  view: 'atom',
  /* PhET opens with an EMPTY atom; an empty atom draws an empty picture, so
     this file opens on carbon-12 (neutral, stable) and keeps PhET's start one
     button away.  Known-bad: a default that makes a view draw nothing. */
  p: 6, n: 6, e: 6,
  model: 'orbits',
  showName: true,
  showIon: true,
  showStab: true,
  showTable: true,
  notation: 'last',        /* PhET's chargeNotation default is signLast */
  jiggle: false,           /* PhET jiggles an unstable nucleus; off by default
                              here so every view is a still picture           */
  /* the counting view */
  countMode: 'stability',
  eSel: 6,
  /* the chart view */
  chartZmax: 84,
  chartCompare: true,
  chartMagic: true,
  /* mass and binding */
  bindAll: true,
  showAbund: true,
  /* the game */
  level: 1,
  gseed: 20260922,
};
const ST = Object.assign({}, DEFAULTS);

const MEMO = {};
function memo(name, key, fn){
  const e = MEMO[name];
  if(e && e.key === key) return e.val;
  const val = fn();
  MEMO[name] = {key: key, val: val};
  return val;
}

/* ---- the game's run state, which is not a control ---- */
const GAME = {phase: 'idle', level: 1, seed: 0, set: [], idx: 0, attempt: 1,
              score: 0, given: {}, history: [], best: [0, 0, 0, 0]};
function gameReset(st){
  GAME.phase = 'idle'; GAME.level = st.level; GAME.seed = st.gseed;
  GAME.set = []; GAME.idx = 0; GAME.attempt = 1; GAME.score = 0;
  GAME.given = {}; GAME.history = [];
}
/* the seed a level actually runs on: the control's seed mixed with the level
   number, so the four levels of one seed are four independent runs rather
   than four readings of the same random stream.  Kept as a function, and
   stored in GAME.seed, so the mixing is observable state and not something
   buried in an argument (the mutation sweep found the argument version
   untestable). */
function levelSeed(gseed, level){ return (gseed + level * 7919) | 0; }
function gameStart(st){
  GAME.level = st.level;
  GAME.seed = levelSeed(st.gseed, st.level);
  GAME.set = makeChallengeSet(st.level - 1, GAME.seed);
  GAME.idx = 0; GAME.attempt = 1; GAME.score = 0; GAME.history = [];
  GAME.phase = 'ask';
  gameClearAnswer();
}
function gameCurrent(){
  return (GAME.phase === 'idle' || GAME.idx >= GAME.set.length) ? null : GAME.set[GAME.idx];
}
function gameClearAnswer(){
  const c = gameCurrent();
  GAME.given = {};
  if(!c) return;
  /* a blank answer starts at the bottom of each field's range, except the
     charge, whose natural blank is zero and not -10 */
  for(const f of answerFields(c.type))
    GAME.given[f] = (f === 'charge') ? 0 : FIELD_RANGE[f][0];
}
function gameCheck(){
  const c = gameCurrent();
  if(!c || GAME.phase !== 'ask') return null;
  if(answerMatches(c.type, c.atom, GAME.given)){
    GAME.score += pointsFor(GAME.attempt);
    GAME.history.push(GAME.attempt);
    GAME.phase = 'right';
    return true;
  }
  if(GAME.attempt === 1){ GAME.attempt = 2; GAME.phase = 'wrong'; return false; }
  GAME.history.push(0);
  GAME.phase = 'shown';
  return false;
}
function gameRetry(){ if(GAME.phase === 'wrong') GAME.phase = 'ask'; }
function gameNext(){
  if(GAME.phase !== 'right' && GAME.phase !== 'shown') return;
  GAME.idx++;
  GAME.attempt = 1;
  if(GAME.idx >= GAME.set.length){
    GAME.phase = 'done';
    const li = GAME.level - 1;
    if(GAME.score > GAME.best[li]) GAME.best[li] = GAME.score;
  } else { GAME.phase = 'ask'; gameClearAnswer(); }
}

/* ---- the particle being dragged, if any ---- */
const DRAG = {type: null, x: 0, y: 0, from: null, active: false};
/* the frame counter the unstable-nucleus jiggle reads.  It is the ONLY
   animated quantity in the file, and it advances only while the jiggle
   checkbox is on and the nucleus is unstable. */
const FRAME = {jig: 0};

/* ================================================================== *
 *  the model                                                          *
 * ================================================================== */
function buildModel(st){
  st = st || ST;
  const p = st.p | 0, n = st.n | 0, e = st.e | 0;
  const A = massNumber(p, n), q = netCharge(p, e);
  const stable = isStable(p, n), nuc = hasNucleus(p, n);
  const sym = elementSymbol(p), name = elementName(p);
  const M = {
    view: st.view,
    p: p, n: n, e: e, A: A, q: q,
    sym: sym, name: name,
    hasNuc: nuc,
    stable: stable,
    nucleusStable: nucleusStable(p, n),
    ion: ionWord(q),
    chargeStr: chargeString(q, st.notation === 'first'),
    shells: shellCounts(e),
    cloudR: cloudRadius(e),
    leftP: PHET.numProtons - p, leftN: PHET.numNeutrons - n, leftE: PHET.numElectrons - e,
    mass: isotopeMass(p, A),
    abundance: naturalAbundance(p, A),
    trace: (function(){ const d = ISOT[String(p)]; return !!(d && d[String(A)] && isTrace(d[String(A)][1])); })(),
    weighted: weightedMass(p),
    standard: standardWeight(p),
    BperA: bindingPerNucleon(p, A),
    B: (isotopeMass(p, A) == null) ? null : bindingMeV(p, A, isotopeMass(p, A)),
    census: bucketCensus(),
    parity: memo('parity', 'fixed', parityCensus),
    heaviest: memo('heaviest', 'fixed', heaviestStable),
    nStable: memo('nstable', 'fixed', stableCount),
    noStable: memo('nostable', 'fixed', elementsWithNoStable),
    st: st,
  };
  return M;
}

/* ---- the floating readout ---- */
function hd(t){ return '<tr><td class="hd" colspan="2">' + t + '</td></tr>'; }
function row(k, v, cls){
  return '<tr><td>' + k + '</td><td class="v' + (cls ? ' ' + cls : '') + '">' + v + '</td></tr>';
}
function nuclideName(M){
  if(!M.hasNuc) return 'no nucleus yet';
  if(M.p === 0) return M.n + ' neutron' + (M.n === 1 ? '' : 's') + ', no protons';
  return M.name + '&ndash;' + M.A;
}
function readoutHTML(M){
  const st = M.st;
  let s = '<div class="rname">' + nuclideName(M)
        + '<small>' + (M.hasNuc ? (M.p === 0 ? 'not an element &mdash; an element needs a proton'
                                             : M.sym + ', ' + M.ion) : 'drag particles in')
        + '</small></div><table>';
  s += hd('the counts');
  s += row('protons', M.p + ' <span style="color:' + COL.proton + '">&#9679;</span>');
  s += row('neutrons', M.n + ' <span style="color:' + COL.neutron + '">&#9679;</span>');
  s += row('electrons', M.e + ' <span style="color:' + COL.electron + '">&#9679;</span>');
  s += hd('what follows from them');
  s += row('element', M.p ? M.name + ' (' + M.sym + ')' : '&mdash;');
  s += row('mass number A', M.hasNuc ? String(M.A) : '&mdash;');
  s += row('net charge', M.chargeStr, M.q === 0 ? 'good' : '');
  s += row('neutral or ion', M.hasNuc || M.e ? M.ion : '&mdash;');
  s += row('nucleus', M.hasNuc ? (M.stable ? 'stable' : 'unstable') : '&mdash;',
           M.hasNuc ? (M.stable ? 'good' : 'bad') : '');
  if(M.p >= 1 && M.p <= 18){
    s += hd('measured, for this nuclide');
    s += row('atomic mass', M.mass == null ? 'not in the table'
             : sigf(M.mass, 10) + ' u');
    s += row('natural abundance', M.mass == null ? '&mdash;'
             : (M.trace ? 'traces only' : (M.abundance > 0 ? fmt(100 * M.abundance, 4) + ' %'
                                                           : 'none')));
    s += row('binding energy / A', M.BperA == null ? '&mdash;' : fmt(M.BperA, 3) + ' MeV');
    s += row('standard weight', M.standard == null ? '&mdash;' : fmt(M.standard, 6) + ' u');
  }
  if(st.view === 'game'){
    s += hd('the game');
    s += row('level', String(GAME.level) + ' of ' + PHET.numLevels);
    s += row('challenge', GAME.phase === 'idle' ? 'not started'
             : Math.min(GAME.idx + 1, PHET.challengesPerLevel) + ' of ' + PHET.challengesPerLevel);
    s += row('score', GAME.score + ' / ' + perfectScore(),
             GAME.score === perfectScore() ? 'good' : '');
    s += row('attempt', GAME.phase === 'idle' ? '&mdash;' : String(GAME.attempt));
    s += row('best on this level', String(GAME.best[GAME.level - 1]));
  }
  s += '</table>';
  if(st.view === 'chart' || st.view === 'counting'){
    s += '<div class="note"><b>' + M.nStable + '</b> nuclides are in PhET&rsquo;s stability '
      + 'table, the heaviest ' + elementSymbol(M.heaviest[0]) + '&ndash;'
      + (M.heaviest[0] + M.heaviest[1]) + '. Technetium and promethium have none at all.</div>';
  } else if(st.view === 'mass'){
    s += '<div class="note">Atomic masses and abundances are <b>measured</b>. '
      + 'The standard atomic weight is their mean, &Sigma;&thinsp;(abundance &times; mass).</div>';
  } else {
    s += '<div class="note">The element is the <b>proton count</b> and nothing else. '
      + 'Neutrons change the isotope, electrons the charge.</div>';
  }
  s += '<div class="legend">'
    + '<span><i style="background:' + COL.proton + '"></i>proton</span>'
    + '<span><i style="background:' + COL.neutron + '"></i>neutron</span>'
    + '<span><i style="background:' + COL.electron + '"></i>electron</span></div>';
  return s;
}

/* ---- the equation bar: one equation per view ---- */
const EQ = {
  atom: ['<span class="lhs">Z</span> = protons &nbsp;&nbsp; '
    + '<span class="lhs">A</span> = Z + N &nbsp;&nbsp; '
    + '<span class="lhs">q</span> = Z &minus; e',
    'the element is the proton count; the mass number adds the neutrons; the charge is '
    + 'the protons the electrons do not cancel'],
  symbol: ['<sup>A</sup><sub>Z</sub>X<sup>q</sup>',
    'the nuclear symbol writes all three: mass number above atomic number, charge on the shoulder'],
  game: ['score = 2 &times; (right first time) + 1 &times; (right second time)',
    'five challenges a level, ten points for a perfect run &mdash; PhET&rsquo;s own scoring'],
  counting: ['(Z, N, e) &rarr; (element, A, q, stable?)',
    'the first three are arithmetic; the fourth is a table lookup'],
  chart: ['stable = (N &isin; T[Z])',
    'there is no formula here: T is a measured table of 244 nuclides'],
  mass: ['B = [Z&thinsp;m(<sup>1</sup>H) + N&thinsp;m<sub>n</sub> &minus; m(A, Z)]&thinsp;c&sup2;',
    'the mass a nucleus is missing is the energy holding it together'],
};
function eqbarHTML(M){
  const e = EQ[M.st.view] || EQ.atom;
  return e[0] + '<span class="sm">' + e[1] + '</span>';
}

/* ---- the top-left stage tag ---- */
function tagHTML(M){
  const st = M.st;
  if(st.view === 'atom')
    return '<b>' + (M.hasNuc ? M.sym + '-' + M.A : 'empty') + '</b> &nbsp; '
      + (M.p ? M.name : 'no element') + ' &nbsp; ' + M.ion + ' &nbsp; '
      + (M.hasNuc ? (M.stable ? 'stable' : 'unstable') : '');
  if(st.view === 'symbol')
    return '<b>' + (M.p ? M.sym : '?') + '</b> &nbsp; A = ' + M.A + ' &nbsp; Z = ' + M.p
      + ' &nbsp; charge ' + M.chargeStr;
  if(st.view === 'game')
    return '<b>level ' + GAME.level + '</b> &nbsp; ' + (GAME.phase === 'idle'
      ? 'press start' : 'challenge ' + Math.min(GAME.idx + 1, PHET.challengesPerLevel)
        + ' &nbsp; score ' + GAME.score);
  if(st.view === 'counting')
    return '<b>' + M.census.total + '</b> configurations &nbsp; '
      + M.census.stablePN.length + ' stable nuclides inside the buckets';
  if(st.view === 'chart')
    return '<b>' + M.nStable + '</b> stable nuclides &nbsp; Z = 1 to '
      + M.heaviest[0] + ' &nbsp; heaviest ' + elementSymbol(M.heaviest[0]) + '-'
      + (M.heaviest[0] + M.heaviest[1]);
  return '<b>' + (M.p >= 1 && M.p <= 18 ? M.name : 'no isotope data') + '</b> &nbsp; '
    + (M.weighted == null ? '' : 'mean mass ' + fmt(M.weighted, 5) + ' u');
}
