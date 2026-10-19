
/* ================================================================== *
 *  the model                                                          *
 *                                                                     *
 *  Everything in this block is EXACT arithmetic on three integers.    *
 *  The element is the proton count, the mass number is protons plus   *
 *  neutrons, the net charge is protons minus electrons, and whether   *
 *  the nucleus is stable is a LOOKUP, not a formula -- which is the    *
 *  one thing about this sim that cannot be derived and has to be       *
 *  measured.  PhET's own numbers are marked PHET.                      *
 * ================================================================== */

const PHET = {
  version: '1.9.3',
  numProtons: 10,          /* the three buckets, read out of BAAModel      */
  numNeutrons: 13,
  numElectrons: 10,
  maxElectrons: 10,        /* ShredConstants.MAX_ELECTRONS                 */
  innerShell: 85,          /* ParticleAtom innerElectronShellRadius        */
  outerShell: 130,         /* ...outerElectronShellRadius                  */
  nucleonRadius: 10,       /* ShredConstants.NUCLEON_RADIUS                */
  electronRadius: 8,       /* ShredConstants.ELECTRON_RADIUS               */
  challengesPerLevel: 5,   /* BAAQueryParameters.challengesPerLevel        */
  pointsFirst: 2,          /* GameModel.POINTS_FIRST_ATTEMPT               */
  pointsSecond: 1,         /* GameModel.POINTS_SECOND_ATTEMPT              */
  numLevels: 4,            /* BAAConstants.NUMBER_OF_GAME_LEVELS           */
};

/* ---- the three rules, and the table ---- */
function elementSymbol(z){ return (z >= 1 && z < SYMBOL.length) ? SYMBOL[z] : '-'; }
function elementName(z){ return (z >= 1 && z < ENAME.length) ? ENAME[z] : ''; }
function massNumber(p, n){ return p + n; }
function netCharge(p, e){ return p - e; }
/* PhET's AtomIdentifier.isStable: the table is indexed by Z and lists the
   NEUTRON numbers, so it is a membership test and nothing more. */
function isStable(p, n){
  const row = (p >= 0 && p < STABLE.length) ? STABLE[p] : undefined;
  return row !== undefined && row.indexOf(n) >= 0;
}
/* PhET's nucleusStableProperty: an atom with no nucleons at all is not called
   unstable.  Keep the two apart -- the label and the jiggle both read this. */
function nucleusStable(p, n){ return (p + n === 0) ? true : isStable(p, n); }
function hasNucleus(p, n){ return p + n > 0; }

/* PhET ships both sign conventions as a preference: signLast is the default
   and is the one chemistry writes (2+, 3-), signFirst is +2, -2. */
function chargeString(q, signFirst){
  if(q === 0) return '0';
  const a = Math.abs(q), s = q < 0 ? '−' : '+';
  return signFirst ? s + a : a + s;
}
function ionWord(q){ return q === 0 ? 'neutral atom' : (q > 0 ? 'positive ion' : 'negative ion'); }

/* ---- the drawn atom: PhET's shell geometry ---- */
/* 10 slots: two on the inner shell at +-r, eight on the outer shell starting
   at pi/8 x 1.2 and stepping 2pi/8.  Read out of ParticleAtom. */
function electronSlots(){
  const out = [{x: PHET.innerShell, y: 0, shell: 0}, {x: -PHET.innerShell, y: 0, shell: 0}];
  let a = PI / 8 * 1.2;
  for(let k = 0; k < 8; k++){
    out.push({x: Math.cos(a) * PHET.outerShell, y: Math.sin(a) * PHET.outerShell, shell: 1});
    a += TAU / 8;
  }
  return out;
}
/* PhET's ElectronCloudView: radius grows linearly from half the inner shell to
   the outer shell over MAX_ELECTRONS, and is exactly zero with no electrons. */
function cloudRadius(e){
  if(e <= 0) return 0;
  const i = 0.5 * PHET.innerShell;
  return i + (PHET.outerShell - i) / PHET.maxElectrons * e;
}
function shellCounts(e){ return [Math.min(e, 2), Math.max(0, Math.min(e, 10) - 2)]; }

/* A deterministic nucleon packing: concentric rings of touching discs, the
   innermost first.  This is NOT PhET's spiral -- it is drawn here, and the
   only thing asserted about it is that no two nucleons overlap and every one
   is inside the drawn nucleus. */
function nucleonLayout(count, r){
  const out = [];
  if(count <= 0) return out;
  if(count === 1){ out.push([0, 0]); return out; }
  if(count === 2){ out.push([-r * 0.86, 0], [r * 0.86, 0]); return out; }
  if(count === 3){
    for(let k = 0; k < 3; k++){
      const a = -PI / 2 + k * TAU / 3;
      out.push([r * 1.02 * Math.cos(a), r * 1.02 * Math.sin(a)]);
    }
    return out;
  }
  if(count === 4){
    for(let k = 0; k < 4; k++){
      const a = PI / 4 + k * TAU / 4;
      out.push([r * 1.12 * Math.cos(a), r * 1.12 * Math.sin(a)]);
    }
    return out;
  }
  out.push([0, 0]);
  let placed = 1, ring = 1;
  while(placed < count){
    const rad = ring * r * 1.78;
    const cap = Math.max(1, Math.floor(TAU * rad / (2 * r * 0.98)));
    const take = Math.min(cap, count - placed);
    const a0 = ring * 1.3;
    for(let k = 0; k < take; k++){
      const a = a0 + k * TAU / take;
      out.push([rad * Math.cos(a), rad * Math.sin(a)]);
    }
    placed += take; ring++;
    if(ring > 40) break;
  }
  return out;
}
/* the radius of the drawn nucleus: PhET grows it with the nucleon count, and
   so does this -- the packing above fills rings of spacing 1.78 r */
function nucleusRadius(count, r){
  if(count <= 1) return r;
  const L = nucleonLayout(count, r);
  let m = 0;
  for(const p of L) m = Math.max(m, Math.sqrt(p[0] * p[0] + p[1] * p[1]));
  return m + r;
}

/* ---- how far from scale the picture is ---- */
/* the ONE length in the file.  PhET's atomic radii are the Clementi
   calculated radii (hydrogen's is the Bohr radius, 53 pm), and a nuclear
   radius is the textbook 1.2 A^(1/3) fm.  The drawing's nucleus-to-atom ratio
   is nucleonRadius / outerShell = 1/13, so the exaggeration is the ratio of
   the two, and it is printed on the canvas for the nuclide on screen. */
const R0_FM = 1.2;
function nuclearRadiusFm(a){ return a > 0 ? R0_FM * Math.pow(a, 1 / 3) : 0; }
function atomRadiusPm(z){ return (z >= 1 && z < ARAD.length) ? ARAD[z] : null; }
function trueNucleusFraction(z, a){
  const R = atomRadiusPm(z);
  return (R == null || !(a > 0)) ? null : nuclearRadiusFm(a) * 1e-15 / (R * 1e-12);
}
function drawnNucleusFraction(){ return PHET.nucleonRadius / PHET.outerShell; }
function nucleusExaggeration(z, a){
  const f = trueNucleusFraction(z, a);
  return f == null ? null : drawnNucleusFraction() / f;
}

/* signed integers, with the MINUS SIGN and not a hyphen: canvas has no
   typography of its own and a hyphen reads as a dash */
function signed(n){ return (n > 0 ? '+' : (n < 0 ? '−' : '')) + Math.abs(n); }

/* ---- measured data ---- */
function isotopesOf(z){
  const d = ISOT[String(z)];
  if(!d) return [];
  const out = [];
  for(const a in d) out.push({A: +a, mass: d[a][0], ab: d[a][1]});
  out.sort((x, y) => x.A - y.A);
  return out;
}
/* PhET flags an isotope that exists only in trace amounts with the sentinel
   abundance 1e-12 (AtomIdentifier.existsInTraceAmounts tests for exactly
   that).  It is a marker, not a measurement, so it never enters a sum. */
const TRACE = 1e-12;
function isTrace(ab){ return ab === TRACE; }
function naturalAbundance(z, a){
  const d = ISOT[String(z)];
  if(!d || !d[String(a)]) return 0;
  const ab = d[String(a)][1];
  return isTrace(ab) ? 0 : ab;
}
function isotopeMass(z, a){
  const d = ISOT[String(z)];
  return (d && d[String(a)]) ? d[String(a)][0] : null;
}
/* sum(abundance x atomic mass) -- the definition of the standard atomic
   weight, evaluated on PhET's own isotope table */
function weightedMass(z){
  let s = 0, w = 0;
  for(const it of isotopesOf(z)){
    if(isTrace(it.ab)) continue;
    s += it.ab * it.mass; w += it.ab;
  }
  return w > 0 ? s : null;
}
function abundanceSum(z){
  let w = 0;
  for(const it of isotopesOf(z)) if(!isTrace(it.ab)) w += it.ab;
  return w;
}
function standardWeight(z){ return (z >= 1 && z < SMASS.length) ? SMASS[z] : null; }

/* CODATA 2022 through scipy.constants, pinned in selfTest against derive.py */
const M_NEUTRON_U = 1.00866491606;
const U_MEV = 931.49410372;
function mH1(){ return isotopeMass(1, 1); }
/* B = [Z m(1H) + N m_n - m(A,Z)] c^2.  The atomic masses carry Z electrons
   each and m(1H) carries one, so the electron masses cancel; what does not
   cancel is the electron BINDING energy, which is eV-scale here and is the
   reason this is quoted to three decimals and not six. */
function bindingMeV(z, a, mass){
  if(mass == null) return null;
  return (z * mH1() + (a - z) * M_NEUTRON_U - mass) * U_MEV;
}
function bindingPerNucleon(z, a){
  const m = isotopeMass(z, a);
  if(m == null || a <= 0) return null;
  return bindingMeV(z, a, m) / a;
}
/* the same quantity from the INDEPENDENT mass excesses, which is how the
   chart view reaches nuclides PhET's own table (Z <= 18) does not carry */
const EXC_BY = (function(){
  const m = {};
  for(const r of DEXC) m[r[0] + ':' + r[1]] = r[2];
  return m;
})();
function massFromExcess(z, a){
  const d = EXC_BY[z + ':' + a];
  return d === undefined ? null : a + d / (U_MEV * 1000);
}
function bindingPerNucleonExc(z, a){
  const m = massFromExcess(z, a);
  if(m == null || a <= 0) return null;
  return bindingMeV(z, a, m) / a;
}

/* ---- the chart of nuclides ---- */
function stableList(){
  const out = [];
  for(let z = 0; z < STABLE.length; z++) for(const n of STABLE[z]) out.push([z, n]);
  return out;
}
function stableCount(){ let c = 0; for(const r of STABLE) c += r.length; return c; }
function elementsWithNoStable(){
  const out = [];
  for(let z = 1; z < STABLE.length; z++) if(STABLE[z].length === 0) out.push(z);
  return out;
}
function heaviestStable(){
  let best = null;
  for(let z = 0; z < STABLE.length; z++) for(const n of STABLE[z])
    if(!best || z + n > best[0] + best[1]) best = [z, n];
  return best;
}
/* the even/odd census -- 140 even-even against 4 odd-odd is the pairing term
   of the semi-empirical mass formula, visible as a bare count */
function parityCensus(){
  const c = {ee: 0, eo: 0, oe: 0, oo: 0, oddOdd: []};
  for(const [z, n] of stableList()){
    const k = (z % 2 === 0 ? 'e' : 'o') + (n % 2 === 0 ? 'e' : 'o');
    c[k]++;
    if(k === 'oo') c.oddOdd.push([z, n]);
  }
  return c;
}

/* ---- the exhaustive census over the buckets ---- */
function bucketCensus(){
  return memo('census', 'fixed', () => {
    let tot = 0, neutral = 0, ions = 0, stable = 0;
    const pn = [];
    for(let p = 0; p <= PHET.numProtons; p++){
      for(let n = 0; n <= PHET.numNeutrons; n++){
        if(p > 0 && isStable(p, n)) pn.push([p, n]);
        for(let e = 0; e <= PHET.numElectrons; e++){
          tot++;
          if(p === e){ if(p + n + e > 0) neutral++; } else ions++;
          if(hasNucleus(p, n) && isStable(p, n)) stable++;
        }
      }
    }
    return {total: tot, neutral: neutral, ions: ions, stableConfigs: stable, stablePN: pn};
  });
}

/* ================================================================== *
 *  the game                                                           *
 * ================================================================== */
/* mulberry32 -- reproduced bit for bit in build/build-an-atom/derive.py, so
   the challenge sets the JS builds are the ones Python asserts. */
function mulberry32(seed){
  let a = seed | 0;
  return function(){
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), a | 1);
    t = (t + Math.imul(t ^ (t >>> 7), t | 61)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/* PhET's four level type lists (ChallengeDescriptorSetFactory) */
const GAME_TYPES = [
  ['schematic-to-element', 'counts-to-element'],
  ['schematic-to-charge', 'schematic-to-mass-number',
   'counts-to-charge', 'counts-to-mass-number'],
  ['schematic-to-symbol-charge', 'schematic-to-symbol-mass-number',
   'schematic-to-symbol-proton-count', 'counts-to-symbol-charge',
   'counts-to-symbol-mass-number'],
  ['schematic-to-symbol-all', 'symbol-to-schematic', 'symbol-to-counts',
   'counts-to-symbol-all'],
];
const SCHEMATIC_TYPES = ['schematic-to-element', 'schematic-to-charge',
  'schematic-to-mass-number', 'schematic-to-symbol-all',
  'schematic-to-symbol-proton-count', 'schematic-to-symbol-charge',
  'schematic-to-symbol-mass-number', 'symbol-to-schematic'];
const CHARGE_TYPES = ['schematic-to-charge', 'counts-to-charge',
  'counts-to-symbol-charge', 'schematic-to-symbol-charge'];
function isSchematicType(t){ return SCHEMATIC_TYPES.indexOf(t) >= 0; }
function isChargeType(t){ return CHARGE_TYPES.indexOf(t) >= 0; }

/* what the question SHOWS and what it ASKS for */
function questionMode(t){
  if(t.indexOf('schematic-to') === 0) return 'schematic';
  if(t.indexOf('counts-to') === 0) return 'counts';
  return 'symbol';
}
function answerFields(t){
  if(t === 'schematic-to-element' || t === 'counts-to-element') return ['element'];
  if(t === 'schematic-to-charge' || t === 'counts-to-charge') return ['charge'];
  if(t === 'schematic-to-mass-number' || t === 'counts-to-mass-number') return ['mass'];
  if(t === 'schematic-to-symbol-charge' || t === 'counts-to-symbol-charge') return ['charge'];
  if(t === 'schematic-to-symbol-mass-number' || t === 'counts-to-symbol-mass-number') return ['mass'];
  if(t === 'schematic-to-symbol-proton-count') return ['protons'];
  if(t === 'schematic-to-symbol-all' || t === 'counts-to-symbol-all') return ['protons', 'mass', 'charge'];
  if(t === 'symbol-to-schematic' || t === 'symbol-to-counts') return ['protons', 'neutrons', 'electrons'];
  throw new Error('unknown challenge type ' + t);
}
function fieldValue(field, atom){
  const p = atom[0], n = atom[1], e = atom[2];
  if(field === 'element' || field === 'protons') return p;
  if(field === 'neutrons') return n;
  if(field === 'electrons') return e;
  if(field === 'mass') return massNumber(p, n);
  if(field === 'charge') return netCharge(p, e);
  throw new Error('unknown answer field ' + field);
}
const FIELD_RANGE = {element: [1, 18], protons: [0, 18], neutrons: [0, 22],
                     electrons: [0, 18], mass: [0, 40], charge: [-10, 10]};
/* A challenge is SOLVABLE when every field it asks for is determined by the
   question and reachable with the answer controls.  Asserted over every seed
   in a sweep, because a generator that can emit an unanswerable puzzle is the
   one bug a game cannot survive. */
function challengeSolvable(t, atom){
  for(const f of answerFields(t)){
    const v = fieldValue(f, atom), r = FIELD_RANGE[f];
    if(!(v >= r[0] && v <= r[1])) return false;
    if(!isFinite(v)) return false;
  }
  return true;
}
function correctAnswer(t, atom){
  const out = {};
  for(const f of answerFields(t)) out[f] = fieldValue(f, atom);
  return out;
}
function answerMatches(t, atom, given){
  for(const f of answerFields(t)) if(given[f] !== fieldValue(f, atom)) return false;
  return true;
}

/* PhET's selection rules: a type is never repeated back to back; a schematic
   challenge draws an atom with Z < 3 so the picture stays readable, every
   other type takes Z >= 4; a charge question asks for a charged atom half the
   time; and an atom is not reused until the pool runs out. */
function makeChallengeSet(level, seed){
  const types = GAME_TYPES[level];
  const remaining = GAME_POOLS[level].map(a => a.slice());
  const used = [];
  const rnd = mulberry32(seed);
  const out = [];
  let prev = null;
  for(let k = 0; k < PHET.challengesPerLevel; k++){
    let i = Math.floor(rnd() * types.length);
    let t = types[i];
    if(prev !== null && t === prev){ i = (i + 1) % types.length; t = types[i]; }
    const lo = isSchematicType(t) ? 0 : 4;
    const hi = isSchematicType(t) ? 3 : 1e9;
    const need = isChargeType(t) ? (rnd() >= 0.5) : false;
    const fits = a => a[0] >= lo && a[0] < hi && (!need || a[0] - a[2] !== 0);
    let ok = remaining.filter(fits);
    if(!ok.length) ok = used.filter(fits);
    if(!ok.length) throw new Error('no atom matches ' + t);
    const a = ok[Math.floor(rnd() * ok.length)];
    const j = remaining.indexOf(a);
    if(j >= 0){ remaining.splice(j, 1); used.push(a); }
    out.push({type: t, atom: a.slice()});
    prev = t;
  }
  return out;
}
function pointsFor(attempt){
  return attempt === 1 ? PHET.pointsFirst : (attempt === 2 ? PHET.pointsSecond : 0);
}
function perfectScore(){ return PHET.challengesPerLevel * PHET.pointsFirst; }
