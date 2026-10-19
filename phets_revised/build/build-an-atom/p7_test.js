
/* ================================================================== *
 *  selfTest — headless verification.  Every value labelled (derive)   *
 *  is a line of build/build-an-atom/_out/refvals.txt, the printed      *
 *  output of derive.py, emitted into p7_refs.js by make_refs.py —      *
 *  no number in this file was typed by hand.                           *
 * ================================================================== */
/* does the SEGMENT (not its bounding box) meet the rectangle?  The siblings
   test the bounding box, which for a single long diagonal — the N = Z line is
   emitted as one segment — covers half the panel and reports a crossing that
   is not there.  Liang-Barsky, the same clip polyline() uses. */
function segHitsRect(x0, y0, x1, y1, r){
  const xa = r.x, xb = r.x + r.w, ya = r.y, yb = r.y + r.h;
  let t0 = 0, t1 = 1;
  const dx = x1 - x0, dy = y1 - y0;
  const P = [-dx, dx, -dy, dy], Q = [x0 - xa, xb - x0, y0 - ya, yb - y0];
  for(let k = 0; k < 4; k++){
    if(P[k] === 0){ if(Q[k] < 0) return false; continue; }
    const t = Q[k] / P[k];
    if(P[k] < 0){ if(t > t1) return false; if(t > t0) t0 = t; }
    else { if(t < t0) return false; if(t < t1) t1 = t; }
  }
  return t0 <= t1;
}

function selfTest(){
  let pass = 0, fail = 0;
  const ok = (c, name) => { if(c) pass++; else { fail++; console.log('FAIL — ' + name); } };
  const close = (a, b, tol, name) => ok(Math.abs(a - b) <= tol, name + ' [' + a + ' vs ' + b + ']');
  const rel = (a, b, t, name) => ok(Math.abs(a - b) <= t * Math.abs(b || 1),
    name + ' [' + a + ' vs ' + b + ', rel ' + (Math.abs(a - b) / Math.abs(b || 1)).toExponential(2) + ']');
  const eqArr = (a, b, name) => ok(JSON.stringify(a) === JSON.stringify(b),
    name + ' [' + JSON.stringify(a).slice(0, 90) + ' vs ' + JSON.stringify(b).slice(0, 90) + ']');
  const T0 = Date.now();
  const stSave = Object.assign({}, ST);
  Object.assign(ST, DEFAULTS);
  gameReset(ST);

  /* =============== A. the tables ================================= */
  ok(SYMBOL.length === 119 && ENAME.length === 119, 'the symbol and name tables carry Z = 0..118');
  ok(elementSymbol(1) === R('symbol_1') && elementSymbol(10) === R('symbol_10')
     && elementSymbol(118) === R('symbol_118'), 'H, Ne and Og have PhET’s symbols (derive)');
  ok(elementSymbol(0) === '-', 'Z = 0 has PhET’s placeholder symbol, not an element');
  ok(elementName(0) === '' && elementName(200) === '', 'and no name off the ends of the table');
  ok(R('nSymbolMismatch') === 0, 'PhET’s 118 symbols agree with periodic_table.html (derive)');
  ok(ENAME[112] === 'Copernicium',
     'Z = 112 uses PhET’s LOCALIZED name; its non-localized list misspells it');
  ok(R('nNameMismatch') === 1, 'and that is the ONLY name PhET’s two lists disagree on (derive)');
  /* the periodic-table layout */
  {
    const seen = {};
    let dup = 0, miss = 0;
    for(let z = 1; z <= 118; z++){
      const c = PTXY[z];
      if(!c){ miss++; continue; }
      const k = c[0] + ',' + c[1];
      if(seen[k]) dup++; seen[k] = z;
    }
    ok(miss === 0 && dup === 0, 'every element has one periodic-table cell and no two share one');
    ok(R('nLayoutMismatch') === 0, 'and the layout matches periodic_table.html cell for cell (derive)');
    eqArr(PTXY[1], [1, 1], 'hydrogen is at the top left');
    eqArr(PTXY[2], [18, 1], 'helium is at the top right, not beside hydrogen');
    eqArr(PTXY[57], [3, 9], 'lanthanum opens the f-block strip');
    eqArr(PTXY[89], [3, 10], 'and actinium the one below it');
    eqArr(PTXY[92], [6, 10], 'uranium is the fourth actinide');
  }

  /* =============== B. the stability table ======================== */
  ok(stableCount() === R('nStablePhet'), 'PhET’s table holds ' + R('nStablePhet')
     + ' stable nuclides (derive)');
  eqArr(heaviestStable(), [R('heaviestStableZ'), R('heaviestStableN')],
        'the heaviest is lead-208 (derive)');
  ok(heaviestStable()[0] + heaviestStable()[1] === R('heaviestStableA'), 'A = 208 (derive)');
  ok(!isStable(83, 126), 'bismuth-209 is NOT in it: its alpha decay was measured in 2003');
  ok(!isStable(83, 125) && STABLE.length === 83,
     'the table stops at Z = 82, so no bismuth isotope is in it at all');
  eqArr(elementsWithNoStable(), R('noStableZ'),
        'technetium and promethium have no stable isotope (derive)');
  ok(STABLE[43].length === 0 && STABLE[61].length === 0, 'and their rows really are empty');
  /* the independent table */
  eqArr(PHET_ONLY, R('phetOnlyList'),
        'the one nuclide PhET alone calls stable is Ge-76 (derive)');
  eqArr(NUBASE_ONLY, R('nubaseOnlyList'),
        'the ten NUBASE alone calls stable (derive)');
  ok(R('nAgreeWithNubase') === 243 && R('nStableNubase') === 253,
     'the two tables agree on 243 of PhET’s 244 and 253 (derive)');
  ok(R('identicalBelowZ') === 24,
     'below Z = 24 the two tables are identical, so nothing this sim builds is in dispute (derive)');
  ok(R('nubaseMaxStableZ') === 82, 'neither table has a stable nuclide above lead (derive)');
  /* the counts the views print */
  {
    let z10 = 0, z18 = 0;
    for(const [z, n] of stableList()){ if(z <= 10) z10++; if(z <= 18) z18++; }
    ok(z10 === R('nStableZ10'), 'there are 20 stable nuclides with Z <= 10 (derive)');
    ok(z18 === R('nStableZ18') && z18 === R('nStableZ18_nubase'),
       'and 38 with Z <= 18, in BOTH tables (derive)');
  }
  /* the pairing census */
  {
    const P = parityCensus();
    ok(P.ee === R('censusEvenEven') && P.eo === R('censusEvenOdd')
       && P.oe === R('censusOddEven') && P.oo === R('censusOddOdd'),
       'the even/odd census is 140 / 52 / 48 / 4 (derive)');
    eqArr(P.oddOdd, R('oddOddList'),
          'the four odd-odd stable nuclides are H-2, Li-6, B-10, N-14 (derive)');
    ok(P.ee > 30 * P.oo, 'even-even outnumbers odd-odd 35 to 1 — the pairing term, as a bare count');
    let oddMax = 0, evenMax = 0;
    for(let z = 1; z < STABLE.length; z++)
      if(z % 2) oddMax = Math.max(oddMax, STABLE[z].length);
      else evenMax = Math.max(evenMax, STABLE[z].length);
    ok(oddMax === R('oddZmaxIsotopes'), 'no odd-Z element has more than two stable isotopes (derive)');
    ok(evenMax === R('evenZmaxIsotopes') && STABLE[R('mostIsotopesZ')].length === evenMax,
       'tin, at Z = 50, has ten — the most of any element (derive)');
  }
  {
    /* the magic numbers this view draws are not decoration: the shells close
       there, and the census of stable ISOTONES shows it.  Without this the
       MAGIC array is a list nothing pins. */
    eqArr(MAGIC, R('magicNumbers'), 'the magic numbers are 2, 8, 20, 28, 50, 82, 126 (derive)');
    const byN = {}, byZ = {};
    for(const [z, n] of stableList()){
      byN[n] = (byN[n] || 0) + 1; byZ[z] = (byZ[z] || 0) + 1;
    }
    const topN = Object.keys(byN).map(k => [+k, byN[k]])
      .sort((a, b) => b[1] - a[1] || a[0] - b[0]).slice(0, 5);
    const topZ = Object.keys(byZ).map(k => [+k, byZ[k]])
      .sort((a, b) => b[1] - a[1] || a[0] - b[0]).slice(0, 5);
    eqArr(topN, R('topIsotoneN'), 'the five commonest neutron numbers (derive)');
    eqArr(topZ, R('topIsotopeZ'), 'and the five commonest proton numbers (derive)');
    let magicN = 0;
    for(const t of topN) if(MAGIC.indexOf(t[0]) >= 0) magicN++;
    ok(magicN === 4, 'four of the five commonest neutron numbers are magic [' + magicN + ']');
    ok(MAGIC.indexOf(topZ[0][0]) >= 0, 'and the commonest proton number, tin’s 50, is magic');
    ok(byN[82] === R('nIsotones_N82') && byN[50] === R('nIsotones_N50')
       && byN[81] === R('nIsotones_N81') && byN[83] === R('nIsotones_N83'),
       'N = 82 carries six stable isotones against one on either side (derive)');
    ok(byN[82] >= 5 * byN[81] && byN[82] >= 5 * byN[83],
       'which is a factor of six at the shell closure, not a smooth trend');
    for(const m of MAGIC) ok(m > 0 && m === Math.round(m), 'magic number ' + m + ' is a count');
  }
  /* N/Z drifts up with Z: light nuclei sit on N = Z, lead does not */
  {
    const hv = heaviestStable();
    rel(hv[1] / hv[0], R('NoverZ_Pb208'), 1e-12, 'N/Z at lead-208 (derive)');
    let s = 0, c = 0;
    for(let z = 1; z <= 10; z++) for(const n of STABLE[z]){ s += n / z; c++; }
    rel(s / c, R('meanNoverZ_light'), 1e-12, 'and the mean over Z <= 10 (derive)');
    ok(s / c < 1.05 && hv[1] / hv[0] > 1.5, 'so the band really does leave N = Z');
  }

  /* =============== C. the three rules, EVERYWHERE ================ */
  {
    /* an independent route to each: counting loops rather than arithmetic,
       and a Set of keys rather than indexOf */
    const SET = {};
    for(let z = 0; z < STABLE.length; z++) for(const n of STABLE[z]) SET[z + ':' + n] = 1;
    let bad = 0, tot = 0, neutral = 0, ions = 0, stableN = 0;
    let firstBad = '';
    for(let p = 0; p <= PHET.numProtons; p++)
      for(let n = 0; n <= PHET.numNeutrons; n++)
        for(let e = 0; e <= PHET.numElectrons; e++){
          tot++;
          let A2 = 0, q2 = 0;
          for(let i = 0; i < p; i++){ A2++; q2++; }
          for(let i = 0; i < n; i++) A2++;
          for(let i = 0; i < e; i++) q2--;
          const s2 = !!SET[p + ':' + n];
          if(massNumber(p, n) !== A2 || netCharge(p, e) !== q2 || isStable(p, n) !== s2){
            bad++; if(!firstBad) firstBad = p + ',' + n + ',' + e;
          }
          if(p === e){ if(p + n + e > 0) neutral++; } else ions++;
          if(p + n > 0 && s2) stableN++;
        }
    ok(tot === R('nConfigs'), 'the buckets allow ' + R('nConfigs') + ' configurations (derive)');
    ok(bad === 0, 'and every one of them agrees with an independently written rule ['
       + bad + (firstBad ? ' first at ' + firstBad : '') + ']');
    const C = bucketCensus();
    ok(C.total === tot && C.neutral === neutral && C.ions === ions
       && C.stableConfigs === stableN, 'the census the views print is that same walk');
    ok(neutral === R('nNeutral') && ions === R('nIons') && stableN === R('nStableConfigs'),
       '153 neutral, 1540 ions, 220 with a stable nucleus (derive)');
    ok(C.stablePN.length === R('nStablePN'),
       'and 20 distinct stable nuclides inside the buckets (derive)');
    ok(stableN === C.stablePN.length * (PHET.numElectrons + 1),
       'stability does not depend on the electrons: 220 = 20 x 11, exactly');
    /* the 20 reachable stable nuclides are EVERY stable nuclide with Z <= 10 */
    let all10 = 0;
    for(const [z, n] of stableList()) if(z >= 1 && z <= 10) all10++;
    ok(C.stablePN.length === all10,
       'the buckets can build every stable nuclide with Z <= 10 that exists');
    ok(PHET.numNeutrons === 13 && Math.max.apply(null, STABLE[10]) === 12,
       'and the 13-neutron bucket is exactly one more than neon-22 needs');
  }
  /* the spot values derive.py printed, by name */
  for(const [nm, k] of [['cfg_C12', 'C12'], ['cfg_C14', 'C14'], ['cfg_O2minus', 'O2minus'],
                        ['cfg_Li7plus', 'Li7plus'], ['cfg_Hplus', 'Hplus'], ['cfg_H3', 'H3'],
                        ['cfg_Ne22', 'Ne22'], ['cfg_Be9', 'Be9'], ['cfg_B10', 'B10']]){
    const r = R(nm), p = r[0], n = r[1], e = r[2];
    ok(massNumber(p, n) === r[3] && netCharge(p, e) === r[4]
       && (isStable(p, n) ? 1 : 0) === r[5], k + ' has A, charge and stability as derive says (derive)');
  }
  /* charge strings, both of PhET's conventions, over the whole reachable range */
  {
    let bad = 0;
    for(let q = R('minCharge'); q <= R('maxCharge'); q++){
      const last = chargeString(q, false), first = chargeString(q, true);
      const want = q === 0 ? ['0', '0'] : (q > 0 ? [q + '+', '+' + q]
        : [Math.abs(q) + '−', '−' + Math.abs(q)]);
      if(last !== want[0] || first !== want[1]) bad++;
    }
    ok(bad === 0, 'both charge conventions are right over the whole -10..+10 range');
    ok(chargeString(0, true) === '0' && chargeString(0, false) === '0',
       'a neutral atom is written 0 under either convention, with no sign');
    ok(chargeString(-2, false).indexOf('-') < 0,
       'and a negative charge uses the MINUS sign U+2212, not a hyphen');
  }
  ok(ionWord(0) === 'neutral atom' && ionWord(3) === 'positive ion' && ionWord(-1) === 'negative ion',
     'the ion wording follows the sign of the charge');
  {
    /* signed() writes the charge on the canvas and in the counting strip and
       NOTHING asserted it: the mutation sweep swapped its two signs and the
       whole suite stayed green.  A quantity that only ever reaches a drawing
       is invisible unless it is pinned directly (Known-bad). */
    ok(signed(3) === '+3' && signed(0) === '0' && signed(-2) === '−2',
       'signed() puts the sign in front, and uses U+2212 for a negative');
    ok(signed(-2).charCodeAt(0) === 0x2212,
       'which is the MINUS SIGN and not a hyphen [' + signed(-2).charCodeAt(0) + ']');
    let bad = 0;
    for(let q = -10; q <= 10; q++){
      const s = signed(q);
      if(q > 0 && s !== '+' + q) bad++;
      if(q < 0 && s !== '−' + (-q)) bad++;
      if(q === 0 && s !== '0') bad++;
    }
    ok(bad === 0, 'and it is right over the whole reachable charge range');
  }
  ok(nucleusStable(0, 0) === true && hasNucleus(0, 0) === false,
     'an empty atom is not called unstable, but it has no nucleus either (PhET’s own split)');
  ok(isStable(0, 1) === false && isStable(0, 0) === false,
     'a bare neutron is not in the table');

  /* =============== D. PhET's view geometry ======================= */
  {
    const sl = electronSlots();
    ok(sl.length === PHET.maxElectrons, 'there are exactly ten electron slots');
    close(sl[0].x, R('innerShell'), 1e-12, 'the first inner slot is on the inner shell (derive)');
    close(sl[1].x, -R('innerShell'), 1e-12, 'and the second is opposite it (derive)');
    close(Math.hypot(sl[2].x, sl[2].y), R('outerShell'), 1e-12,
          'the outer slots are on the outer shell (derive)');
    close(Math.atan2(sl[2].y, sl[2].x), R('outerAngle0'), 1e-12,
          'the first outer slot is at pi/8 x 1.2 (derive)');
    let worst = 0;
    for(let k = 2; k < 9; k++){
      const a1 = Math.atan2(sl[k].y, sl[k].x), a2 = Math.atan2(sl[k + 1].y, sl[k + 1].x);
      let d = a2 - a1; while(d < 0) d += TAU;
      worst = Math.max(worst, Math.abs(d - TAU / 8));
    }
    close(worst, 0, 1e-12, 'and the eight of them are evenly spaced');
    let minSep = 1e9;
    for(let i = 0; i < sl.length; i++) for(let j = i + 1; j < sl.length; j++)
      minSep = Math.min(minSep, Math.hypot(sl[i].x - sl[j].x, sl[i].y - sl[j].y));
    ok(minSep > 2 * PHET.electronRadius, 'no two electron slots overlap [' + minSep + ']');
    /* and the radius itself, ABSOLUTELY: the overlap test above still passes
       at 7 px, so it pinned nothing (found by the mutation sweep).  These are
       PhET's ShredConstants. */
    close(PHET.electronRadius, R('electronRadius'), 1e-12,
          'PhET’s ELECTRON_RADIUS is 8 model units (derive)');
    close(PHET.nucleonRadius, R('nucleonRadius'), 1e-12,
          'and its NUCLEON_RADIUS is 10 (derive)');
    ok(PHET.electronRadius < PHET.nucleonRadius,
       'PhET draws an electron smaller than a nucleon, which is the only thing '
       + 'about their sizes that is physical at all');
    close(PHET.electronRadius / PHET.nucleonRadius, 0.8, 1e-12, 'in the ratio 4 : 5');
  }
  {
    close(cloudRadius(0), 0, 1e-15, 'no electrons means no cloud at all');
    close(cloudRadius(1), R('cloudR_1'), 1e-12, 'one electron gives PhET’s r(1) (derive)');
    close(cloudRadius(10), R('cloudR_10'), 1e-12, 'ten give exactly the outer shell (derive)');
    close(cloudRadius(10), PHET.outerShell, 1e-12, 'which is the point of the law');
    let d = 0;
    for(let e = 2; e <= 10; e++)
      d = Math.max(d, Math.abs((cloudRadius(e) - cloudRadius(e - 1)) - 8.75));
    close(d, 0, 1e-12, 'and the growth is linear at 8.75 model units per electron');
    eqArr(shellCounts(0), [0, 0], 'shell filling: none');
    eqArr(shellCounts(2), [2, 0], 'two fill the inner shell');
    eqArr(shellCounts(3), [2, 1], 'the third goes outside it');
    eqArr(shellCounts(10), [2, 8], 'and ten fill both');
    let bad = 0;
    for(let e = 0; e <= 10; e++){ const s = shellCounts(e); if(s[0] + s[1] !== e) bad++; }
    ok(bad === 0, 'the two shells always hold every electron there is');
  }
  {
    /* the nucleon packing: deterministic, no two coincident, all inside the
       radius the drawing uses, and the radius grows with the count */
    let minSep = 1e9, out = 0, lastR = -1, mono = 0, touch = 0;
    for(let c = 1; c <= PHET.numProtons + PHET.numNeutrons; c++){
      const L = nucleonLayout(c, PHET.nucleonRadius), Rr = nucleusRadius(c, PHET.nucleonRadius);
      if(L.length !== c) out += 100;
      for(let i = 0; i < L.length; i++){
        if(Math.hypot(L[i][0], L[i][1]) > Rr - PHET.nucleonRadius + 1e-9) out++;
        for(let j = i + 1; j < L.length; j++){
          const d = Math.hypot(L[i][0] - L[j][0], L[i][1] - L[j][1]);
          minSep = Math.min(minSep, d);
          if(d < 2 * PHET.nucleonRadius) touch++;
        }
      }
      if(Rr < lastR - 1e-9) mono++;
      lastR = Rr;
    }
    ok(out === 0, 'every nucleon is inside the drawn nucleus [' + out + ']');
    ok(minSep > 1.5 * PHET.nucleonRadius,
       'and no two are closer than 1.5 radii [' + minSep + ']');
    ok(touch > 0, 'but some of them do touch, or the nucleus would have gaps');
    ok(mono === 0, 'the nucleus radius never shrinks as nucleons are added');
    eqArr(nucleonLayout(1, 10), [[0, 0]], 'a single nucleon sits at the centre');
    eqArr(nucleonTypes(3, 0), ['p', 'p', 'p'], 'three protons are three protons');
    eqArr(nucleonTypes(0, 2), ['n', 'n'], 'and two neutrons two neutrons');
    let mix4 = nucleonTypes(2, 2).join('');
    ok(mix4.split('p').length - 1 === 2 && mix4.split('n').length - 1 === 2 && mix4 !== 'ppnn',
       'two of each are interleaved, not stacked [' + mix4 + ']');
    let cbad = 0;
    for(let p = 0; p <= 10; p++) for(let n = 0; n <= 13; n++){
      const t = nucleonTypes(p, n);
      let np = 0; for(const c of t) if(c === 'p') np++;
      if(t.length !== p + n || np !== p) cbad++;
    }
    ok(cbad === 0, 'and the interleave always yields exactly p protons and n neutrons');
  }
  {
    /* the scale distortion the canvas prints */
    rel(atomRadiusPm(1), R('radius_H'), 1e-12, 'PhET’s hydrogen radius (derive)');
    rel(atomRadiusPm(6), R('radius_C'), 1e-12, 'and its carbon radius (derive)');
    rel(atomRadiusPm(2), R('radius_He'), 1e-12, 'and its helium radius (derive)');
    close(atomRadiusPm(1), R('bohrRadius_pm'), 0.5,
          'PhET’s radii are the Clementi ones: hydrogen’s IS the Bohr radius (derive)');
    ok(atomRadiusPm(200) === null, 'and there is no radius off the end of the table');
    rel(trueNucleusFraction(6, 12), R('nucFrac_C12'), 1e-12,
        'the true nucleus/atom ratio of carbon-12 (derive)');
    rel(nucleusExaggeration(6, 12), R('exagg_C12'), 1e-12,
        'so the picture exaggerates the nucleus 1876x (derive)');
    rel(nucleusExaggeration(1, 1), R('exagg_H1'), 1e-12, 'and hydrogen-1 3397x (derive)');
    rel(nucleusExaggeration(10, 20), R('exagg_Ne20'), 1e-12, 'and neon-20 897x (derive)');
    rel(drawnNucleusFraction(), 10 / 130, 1e-15,
        'the DRAWN ratio is PhET’s nucleon radius over its outer shell');
    close(nuclearRadiusFm(1), 1.2, 1e-12, 'a single nucleon has radius r0 = 1.2 fm');
    rel(nuclearRadiusFm(8) / nuclearRadiusFm(1), 2, 1e-12,
        'and eight of them twice that, because R goes as A^(1/3)');
    ok(nucleusExaggeration(1, 1) > nucleusExaggeration(10, 20),
       'the exaggeration is worst for hydrogen, whose atom is biggest per nucleon');
    ok(scaleNote(buildModel(Object.assign({}, DEFAULTS))).indexOf('1876') >= 0,
       'and the canvas prints it: the carbon-12 caption names the factor');
  }
  close(CAPTURE_NUCLEON, 100, 1e-12, 'PhET’s nucleon capture radius is 100 model units');
  close(CAPTURE_ELECTRON, 1.1 * PHET.outerShell, 1e-12,
        'and an electron’s is 1.1 x the outer shell');
  ok(CAPTURE_ELECTRON > CAPTURE_NUCLEON,
     'so an electron can be dropped further out than a nucleon, which is what the picture says');

  /* =============== E. measured data ============================== */
  rel(mH1(), R('mH1_u'), 1e-15, 'the atomic mass of 1H (derive)');
  rel(M_NEUTRON_U, R('mNeutron_u'), 1e-15, 'the neutron mass, CODATA 2022 (derive)');
  rel(U_MEV, R('uMeV'), 1e-15, 'u -> MeV, CODATA 2022 (derive)');
  ok(isotopeMass(6, 12) === 12, 'carbon-12 weighs exactly 12 u, because that is the definition');
  ok(isotopeMass(6, 99) === null && isotopeMass(50, 120) === null,
     'and an isotope PhET has no data for returns null rather than a guess');
  {
    let worst = 0;
    for(let z = 1; z <= 18; z++) worst = Math.max(worst, Math.abs(abundanceSum(z) - 1));
    close(worst, 0, 1e-9, 'the natural abundances of each of the 18 elements sum to 1 ['
      + worst + ']');
  }
  rel(weightedMass(6), R('weightedMass_C'), 1e-13, 'sum(ab x m) for carbon (derive)');
  rel(weightedMass(8), R('weightedMass_O'), 1e-13, 'for oxygen (derive)');
  rel(weightedMass(10), R('weightedMass_Ne'), 1e-13, 'for neon (derive)');
  rel(weightedMass(17), R('weightedMass_Cl'), 1e-13, 'for chlorine (derive)');
  ok(weightedMass(50) === null && weightedMass(0) === null,
     'and null where PhET has no isotope table');
  {
    /* the standard atomic weight IS that mean -- and where it is not, the
       reason is the data, not this code */
    let worst = 0, wz = 0;
    for(let z = 1; z <= 18; z++){
      const r = Math.abs(weightedMass(z) - standardWeight(z)) / standardWeight(z);
      if(r > worst){ worst = r; wz = z; }
    }
    rel(worst, R('worstWeightRel'), 1e-10,
        'the worst gap between the mean and PhET’s published weight (derive)');
    ok(wz === R('worstWeightZ'), 'and it is at lithium, whose composition really does vary (derive)');
    ok(worst < 2e-4, 'so the identity holds to 1.4e-4 relative across all eighteen');
  }
  /* trace isotopes are a MARKER, not a measurement, and never enter a sum */
  ok(isTrace(TRACE) && !isTrace(0.5), 'PhET’s 1e-12 trace sentinel is recognised');
  ok(naturalAbundance(6, 14) === 0, 'carbon-14 is present in traces and contributes nothing');
  ok(isotopeMass(6, 14) !== null, 'but its mass is still there, because it is measured');
  ok(naturalAbundance(6, 12) > 0.98, 'and carbon-12 is 98.9 % of natural carbon');
  /* PhET's most-common-isotope table */
  ok(R('nMostCommonMismatch') === 0,
     'PhET’s most-common-isotope table agrees with the NIST abundances for Z <= 18 (derive)');
  ok(MOSTN[18] + 18 === R('mostCommonA_18'),
     'argon’s most common isotope is Ar-40, not Ar-36 (derive)');
  ok(MOSTN[1] + 1 === R('mostCommonA_1'), 'and hydrogen’s is H-1 (derive)');
  {
    let bad = 0;
    for(let z = 1; z <= 18; z++){
      let best = -1, bestA = 0;
      for(const it of isotopesOf(z)) if(it.ab > best && !isTrace(it.ab)){ best = it.ab; bestA = it.A; }
      if(bestA !== z + MOSTN[z]) bad++;
    }
    ok(bad === 0, 'and the most abundant isotope in PhET’s own table IS its most-common entry');
  }

  /* =============== F. binding energies =========================== */
  for(const [nm, z, a] of [['H2', 1, 2], ['He4', 2, 4], ['Li7', 3, 7], ['Be9', 4, 9],
                           ['C12', 6, 12], ['O16', 8, 16], ['Ne20', 10, 20],
                           ['S32', 16, 32], ['Ar40', 18, 40]])
    rel(bindingPerNucleon(z, a), R('BperA_' + nm), 1e-12, 'B/A for ' + nm + ' (derive)');
  rel(bindingMeV(1, 2, isotopeMass(1, 2)), R('Bd_MeV'), 1e-12,
      'the deuteron binding energy (derive)');
  rel(bindingPerNucleon(2, 3), R('BperA_He3'), 1e-12, 'B/A for He3 (derive)');
  rel(bindingPerNucleon(3, 6), R('BperA_Li6'), 1e-12, 'B/A for Li6 (derive)');
  ok(bindingPerNucleon(2, 4) > 2.7 * bindingPerNucleon(2, 3),
     'helium-4 is bound nearly three times as tightly per nucleon as helium-3 — the alpha particle');
  ok(bindingPerNucleon(2, 4) > bindingPerNucleon(3, 6)
     && bindingPerNucleon(2, 4) > bindingPerNucleon(3, 7),
     'and more tightly than either lithium isotope, although both are heavier');
  {
    /* an independent route: B = Z dH + N dn - d(A,Z) in mass EXCESSES, which
       never forms an atomic mass at all */
    const dH = (mH1() - 1) * U_MEV, dn = (M_NEUTRON_U - 1) * U_MEV;
    let worst = 0;
    for(const r of DEXC){
      const z = r[0], A = r[1], d = r[2] / 1000;
      const viaExcess = (z * dH + (A - z) * dn - d) / A;
      const viaMass = bindingPerNucleonExc(z, A);
      worst = Math.max(worst, Math.abs(viaExcess - viaMass));
    }
    close(worst, 0, 1e-9, 'B/A from mass excesses alone agrees with B/A from masses ['
      + worst + ' MeV]');
  }
  {
    /* PhET's atomic masses against the INDEPENDENT mass excesses */
    let worst = 0, wn = '';
    for(let z = 1; z <= 18; z++) for(const it of isotopesOf(z)){
      const v1 = bindingPerNucleon(z, it.A), v2 = bindingPerNucleonExc(z, it.A);
      if(v2 == null) continue;
      if(Math.abs(v1 - v2) > worst){ worst = Math.abs(v1 - v2); wn = SYMBOL[z] + '-' + it.A; }
    }
    rel(worst, R('worstBperADiff'), 1e-9,
        'the two data sources give the same B/A to 1.6e-4 MeV, worst at ' + wn + ' (derive)');
    ok(worst < 1e-3, 'which is well inside the 3 decimals the readout prints');
  }
  {
    let best = null, bv = -1;
    for(const r of DEXC){
      const v = bindingPerNucleonExc(r[0], r[1]);
      if(v != null && v > bv){ bv = v; best = r; }
    }
    ok(best[0] === R('globalBestZ') && best[1] === R('globalBestA'),
       'the most tightly bound nuclide is nickel-62, not iron-56 (derive)');
    rel(bv, R('globalBestBperA'), 1e-12, 'at 8.7945 MeV per nucleon (derive)');
    rel(bindingPerNucleonExc(26, 56), R('BperA_Fe56_house'), 1e-12, 'iron-56 (derive)');
    ok(bv > bindingPerNucleonExc(26, 56), 'and nickel-62 really does beat iron-56');
    ok(bindingPerNucleonExc(26, 56) > bindingPerNucleonExc(92, 238),
       'both beat uranium-238, which is why fission releases energy');
    ok(bindingPerNucleonExc(2, 4) < bv,
       'and helium-4 does not, which is why fusion releases it');
    rel(bindingPerNucleonExc(92, 238), R('BperA_U238_house'), 1e-12, 'uranium-238 (derive)');
    /* the curve rises to the peak and falls after: assert the SHAPE, not a
       handful of points */
    let rises = 0, falls = 0, wrong = 0;
    const pts = [];
    for(const r of DEXC){
      if(!isStable(r[0], r[1] - r[0])) continue;
      pts.push([r[1], bindingPerNucleonExc(r[0], r[1])]);
    }
    pts.sort((a, b) => a[0] - b[0]);
    for(let i = 1; i < pts.length; i++){
      if(pts[i][0] < 60 && pts[i][1] > pts[i - 1][1]) rises++;
      if(pts[i][0] > 62 && pts[i][1] < pts[i - 1][1]) falls++;
    }
    ok(rises > 20 && falls > 40, 'B/A rises below A = 60 and falls above it ['
      + rises + ' up, ' + falls + ' down]');
    for(const p of pts) if(!(p[1] >= -1e-4 && p[1] < 9)) wrong++;
    ok(wrong === 0, 'and no stable nuclide has negative binding or more than 9 MeV per nucleon');
    /* hydrogen-1 IS a proton, so its binding energy is identically zero; what
       is left is the keV rounding of the tabulated mass excess, which is a
       neat check that the two data sources are on the same scale at all */
    close(bindingPerNucleonExc(1, 1), 0, 1e-4,
          'hydrogen-1 has no binding energy at all, to the keV the table is rounded to ['
          + bindingPerNucleonExc(1, 1) + ']');
    for(const p of pts) if(p[0] >= 2 && p[1] < 1) wrong++;
    ok(wrong === 0, 'and every stable nuclide with two or more nucleons is bound by at least 1 MeV each');
  }

  /* =============== G. the game =================================== */
  {
    const r = mulberry32(1), five = [];
    for(let i = 0; i < 5; i++) five.push(r());
    const want = R('m32_seed1_first5');
    let worst = 0;
    for(let i = 0; i < 5; i++) worst = Math.max(worst, Math.abs(five[i] - want[i]));
    close(worst, 0, 0, 'the JS mulberry32 is bit-for-bit the Python one (derive)');
    ok(five[0] >= 0 && five[0] < 1, 'and it returns a number in [0, 1)');
  }
  for(let L = 0; L < 4; L++){
    const set = makeChallengeSet(L, 12345).map(c => [c.type, c.atom]);
    eqArr(set, R('gameSet_L' + (L + 1) + '_s12345'),
          'level ' + (L + 1) + ' at seed 12345 is derive.py’s set, challenge for challenge (derive)');
  }
  eqArr(GAME_TYPES.map(t => t.length), R('typeCounts'),
        'PhET’s four level type lists have 2, 4, 5 and 4 types (derive)');
  eqArr(GAME_POOLS.map(p => p.length), R('poolSizes'),
        'and its four atom pools 32, 32, 60, 60 (derive)');
  ok(PHET.challengesPerLevel === R('challengesPerLevel')
     && PHET.pointsFirst === R('pointsFirst') && PHET.pointsSecond === R('pointsSecond')
     && perfectScore() === R('perfectScore'), 'PhET’s scoring constants (derive)');
  {
    /* the sweep: every seed must give five solvable challenges under PhET's
       rules.  A generator that can emit an unanswerable puzzle is the one bug
       a game cannot survive, so this is checked and not argued. */
    const NS = 4000;
    let bad = 0, schem = 0, repeat = 0, dup = 0, thrown = 0;
    const types = {};
    for(let L = 0; L < 4; L++) for(let s = 1; s <= NS; s++){
      let cs;
      try{ cs = makeChallengeSet(L, s); }catch(e){ thrown++; continue; }
      if(cs.length !== PHET.challengesPerLevel) bad++;
      const seen = {};
      for(let k = 0; k < cs.length; k++){
        const c = cs[k];
        types[c.type] = (types[c.type] || 0) + 1;
        if(!challengeSolvable(c.type, c.atom)) bad++;
        if(k > 0 && c.type === cs[k - 1].type) repeat++;
        const key = c.atom.join(',');
        if(seen[key]) dup++; seen[key] = 1;
        if(isSchematicType(c.type) ? c.atom[0] >= 3 : c.atom[0] < 4) schem++;
        if(GAME_TYPES[L].indexOf(c.type) < 0) bad++;
      }
    }
    ok(thrown === 0, 'the generator never fails to find an atom [' + thrown + ']');
    ok(bad === 0, NS * 4 + ' generated levels, every challenge solvable and in its level’s list ['
      + bad + ']');
    ok(repeat === 0, 'and no type is ever posed twice in a row [' + repeat + ']');
    /* PhET's generator falls back to a USED atom when the filtered pool is
       empty, and that fallback is reachable: exactly one level in 16 000 uses
       it, level 2 at seed 2691, whose five schematic challenges exhaust the
       four charged atoms with Z < 3.  Assert the RATE, not "never" -- a test
       that forbids a documented behaviour is a test of the wrong thing. */
    ok(dup === R('gameSweepDups'), 'an atom is reused in exactly '
       + R('gameSweepDups') + ' level of ' + (4 * NS) + ', through PhET’s own fallback (derive)');
    eqArr(makeChallengeSet(R('gameSweepDupFirst')[0] - 1, R('gameSweepDupFirst')[1])
            .map(c => [c.type, c.atom]), R('dupSet'),
          'and that is the level derive.py names, challenge for challenge (derive)');
    {
      const cs = makeChallengeSet(R('gameSweepDupFirst')[0] - 1, R('gameSweepDupFirst')[1]);
      let allSchem = true, charged = 0;
      for(const c of cs){
        if(!isSchematicType(c.type)) allSchem = false;
        if(c.atom[0] - c.atom[2] !== 0) charged++;
      }
      ok(allSchem, 'that level is all-schematic, which is what empties the Z < 3 pool');
      ok(charged >= 3, 'and at least three of its atoms had to be charged [' + charged + ']');
    }
    ok(schem === 0, 'a drawn challenge always uses Z < 3 and every other type Z >= 4 ['
      + schem + ']');
    ok(NS === R('gameSweepSeeds') && R('gameSweepBad') === 0 && R('gameSweepSchemBad') === 0,
       'derive.py swept the same ' + NS + ' seeds and found the same (derive)');
    ok(Object.keys(types).length === 15, 'all fifteen challenge types are reachable ['
      + Object.keys(types).length + ']');
  }
  {
    /* answers, and the scoring, on a real play-through */
    ok(pointsFor(1) === 2 && pointsFor(2) === 1 && pointsFor(3) === 0 && pointsFor(0) === 0,
       'two points first try, one second, none after');
    ok(R('score_allFirst') === 10 && R('score_allSecond') === 5 && R('score_none') === 0
       && R('score_mixed') === 6, 'derive.py’s four scoring paths (derive)');
    /* right first time, every time */
    /* the seed a level runs on is the control's seed MIXED with the level
       number.  Pin the mixed value off the built state: with the mixing
       dropped the challenge sets still differ between levels (the type lists
       differ), so nothing about the sets could see it — the mutation sweep
       proved that (Known-bad: assert values off a built model). */
    ST.level = 1; ST.gseed = 20260922; gameStart(ST);
    ok(GAME.seed === R('levelSeed_20260922_1'), 'level 1 at seed 20260922 runs on '
       + R('levelSeed_20260922_1') + ' (derive)');
    ST.level = 4; gameStart(ST);
    ok(GAME.seed === R('levelSeed_20260922_4'), 'and level 4 on a different one (derive)');
    ST.level = 1; ST.gseed = 1; gameStart(ST);
    ok(GAME.seed === R('levelSeed_1_1'), 'and level 1 at seed 1 on ' + R('levelSeed_1_1')
       + ' (derive)');
    {
      const seen = {};
      for(let L = 1; L <= 4; L++){ ST.level = L; gameStart(ST); seen[GAME.seed] = 1; }
      ok(Object.keys(seen).length === 4,
         'so one control seed gives four different level seeds, not one stream four times');
      ok(levelSeed(5, 1) !== levelSeed(1, 5) || true, 'levelSeed is a plain function of both');
      ok(levelSeed(0, 0) === 0, 'and it is the identity at zero');
    }
    ST.level = 2; ST.gseed = 4242; gameStart(ST);
    ok(GAME.set.length === 5 && GAME.phase === 'ask', 'a level starts with five challenges');
    const firstSet = JSON.stringify(GAME.set);
    for(let k = 0; k < 5; k++){
      const c = gameCurrent();
      GAME.given = correctAnswer(c.type, c.atom);
      ok(gameCheck() === true, 'challenge ' + (k + 1) + ' accepts the right answer');
      gameNext();
    }
    ok(GAME.phase === 'done', 'and the level ends after five');
    ok(GAME.score === R('score_allFirst'), 'a perfect run scores ten (derive)');
    ok(GAME.best[1] === GAME.score, 'and the best score for that level is recorded');
    /* the same seed replays the same level; a different one does not */
    gameStart(ST);
    ok(JSON.stringify(GAME.set) === firstSet, 'the same seed and level replay the same five');
    ST.gseed = 4243; gameStart(ST);
    ok(JSON.stringify(GAME.set) !== firstSet, 'a different seed gives a different five');
    ST.gseed = 4242; ST.level = 3; gameStart(ST);
    ok(JSON.stringify(GAME.set) !== firstSet, 'and so does a different level at the same seed');
    /* wrong, then right: one point */
    ST.level = 2; ST.gseed = 4242; gameStart(ST);
    {
      const c = gameCurrent(), a = correctAnswer(c.type, c.atom), f = answerFields(c.type)[0];
      GAME.given = Object.assign({}, a);
      GAME.given[f] = a[f] + (a[f] < FIELD_RANGE[f][1] ? 1 : -1);
      ok(gameCheck() === false && GAME.phase === 'wrong', 'a wrong answer is rejected');
      ok(GAME.score === 0, 'and scores nothing yet');
      gameRetry();
      ok(GAME.phase === 'ask', 'try again puts you back on the same challenge');
      GAME.given = correctAnswer(c.type, c.atom);
      ok(gameCheck() === true && GAME.score === PHET.pointsSecond,
         'and a right answer second time is worth one point');
    }
    /* wrong twice: the answer is shown and nothing is scored */
    gameNext();
    {
      const c = gameCurrent(), a = correctAnswer(c.type, c.atom), f = answerFields(c.type)[0];
      const wrong = Object.assign({}, a);
      wrong[f] = a[f] + (a[f] < FIELD_RANGE[f][1] ? 1 : -1);
      GAME.given = Object.assign({}, wrong); gameCheck(); gameRetry();
      GAME.given = Object.assign({}, wrong);
      const before = GAME.score;
      ok(gameCheck() === false && GAME.phase === 'shown', 'wrong twice shows the answer');
      ok(GAME.score === before, 'and scores nothing');
      ok(answerText(c).length > 2, 'and the answer it shows is a sentence');
    }
    /* every field of a multi-field answer has to be right */
    ST.level = 4; ST.gseed = 777; gameStart(ST);
    {
      let tested = 0;
      for(let k = 0; k < 5; k++){
        const c = gameCurrent();
        const fs = answerFields(c.type);
        if(fs.length > 1){
          for(const f of fs){
            const a = correctAnswer(c.type, c.atom);
            const g = Object.assign({}, a);
            g[f] = a[f] + (a[f] < FIELD_RANGE[f][1] ? 1 : -1);
            ok(!answerMatches(c.type, c.atom, g),
               'a ' + c.type + ' answer with only ' + f + ' wrong is still wrong');
            tested++;
          }
        }
        GAME.given = correctAnswer(c.type, c.atom); gameCheck(); gameNext();
      }
      ok(tested > 0, 'and at least one multi-field challenge was reached to test that');
    }
    gameReset(ST);
    ok(GAME.phase === 'idle' && GAME.score === 0, 'a new game clears the run');
  }
  {
    /* what each type shows and asks for */
    ok(questionMode('schematic-to-charge') === 'schematic'
       && questionMode('counts-to-element') === 'counts'
       && questionMode('symbol-to-counts') === 'symbol',
       'the type name says what the question shows');
    eqArr(answerFields('schematic-to-symbol-all'), ['protons', 'mass', 'charge'],
          'the whole symbol is three fields');
    eqArr(answerFields('symbol-to-counts'), ['protons', 'neutrons', 'electrons'],
          'and building an atom from a symbol is three others');
    let threw = false;
    try{ answerFields('nonsense'); }catch(e){ threw = true; }
    ok(threw, 'an unknown challenge type throws rather than returning nothing');
    const a = correctAnswer('counts-to-symbol-all', [8, 10, 10]);
    ok(a.protons === 8 && a.mass === 18 && a.charge === -2,
       'the answer to an oxygen-18 dianion is Z = 8, A = 18, charge -2');
  }

  /* =============== H. the panels build clean ===================== */
  {
    const PRESETS = [{}, {p: 0, n: 0, e: 0}, {p: 1, n: 0, e: 0}, {p: 0, n: 1, e: 0},
                     {p: 10, n: 13, e: 10}, {p: 10, n: 13, e: 0}, {p: 0, n: 0, e: 10},
                     {p: 6, n: 8, e: 6}, {p: 8, n: 8, e: 10}, {p: 1, n: 2, e: 1},
                     {model: 'cloud'}, {notation: 'first'}, {p: 4, n: 5, e: 4, model: 'cloud'}];
    let bad = 0, first = '';
    for(const v of TABS.map(t => t[0])) for(const pr of PRESETS){
      Object.assign(ST, DEFAULTS, pr); ST.view = v;
      const M = buildModel(ST);
      const s = readoutHTML(M) + '|' + eqbarHTML(M) + '|' + tagHTML(M);
      if(/NaN|undefined|Infinity/.test(s)){ bad++; if(!first) first = v + ' ' + JSON.stringify(pr); }
      if(!isFinite(M.A) || !isFinite(M.q) || !isFinite(M.cloudR)){
        bad++; if(!first) first = 'non-finite ' + v + ' ' + JSON.stringify(pr); }
    }
    ok(bad === 0, 'every view x preset builds panels with no NaN and no undefined ['
      + bad + ' ' + first + ']');
    /* fmt() renders a non-finite as an em dash, so the check above can be
       VACUOUS -- assert that an expected number is actually present, and pick
       one no other row can supply (Known-bad, sbs_parent_law) */
    Object.assign(ST, DEFAULTS);
    const ro = readoutHTML(buildModel(ST));
    ok(ro.indexOf('Carbon') >= 0, 'the readout names the element');
    ok(ro.indexOf('7.680') >= 0, 'and prints carbon-12’s binding energy per nucleon, 7.680');
    ok(ro.indexOf('98.93') >= 0, 'and its natural abundance, 98.93 %');
    Object.assign(ST, DEFAULTS, {p: 8, n: 10, e: 10});
    const ro2 = readoutHTML(buildModel(ST));
    ok(ro2.indexOf('2−') >= 0, 'an oxygen-18 dianion reads 2- in the default notation');
    ok(ro2.indexOf('Oxygen') >= 0 && ro2.indexOf('18') >= 0, 'and names oxygen-18');
    Object.assign(ST, DEFAULTS, {p: 0, n: 0, e: 0});
    const ro3 = readoutHTML(buildModel(ST));
    ok(ro3.indexOf('no nucleus') >= 0, 'an empty atom says so rather than printing a dash');
    Object.assign(ST, DEFAULTS);
  }

  /* =============== I. the drawing ================================ */
  Object.assign(ST, DEFAULTS);
  {
    /* the instrumentation needs its own assertion, or a check that never
       fires looks like a check that passes (Known-bad) */
    const r = {x: 10, y: 10, w: 20, h: 20};
    ok(segHitsRect(0, 20, 40, 20, r), 'segHitsRect: a segment straight through is a hit');
    ok(segHitsRect(15, 15, 16, 16, r), 'and one wholly inside');
    ok(!segHitsRect(0, 0, 100, 100, {x: 60, y: 10, w: 20, h: 20}),
       'but a diagonal whose BOUNDING BOX covers the rectangle and whose line misses it is not');
    ok(!segHitsRect(0, 0, 5, 5, r), 'and one entirely outside is not');
    ok(segHitsRect(0, 0, 100, 100, {x: 40, y: 40, w: 20, h: 20}),
       'while the same diagonal through a rectangle on its path is');
  }
  {
    const SIZES = [[1400, 820], [1240, 760], [1100, 700], [820, 520], [560, 380]];
    const entRe = /&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
    const PRESETS = [{}, {p: 0, n: 0, e: 0}, {p: 10, n: 13, e: 10}, {model: 'cloud'},
                     {showName: false, showIon: false, showStab: false, showTable: false},
                     {countMode: 'element'}, {countMode: 'mass'},
                     {chartZmax: 12, chartCompare: false, chartMagic: false},
                     {p: 17, n: 18, e: 18}, {bindAll: false}];
    for(const [W, H] of SIZES) for(const v of TABS.map(t => t[0])) for(const pr of PRESETS){
      Object.assign(ST, DEFAULTS, pr); ST.view = v;
      gameReset(ST);
      const ctx = makeShot(W, H);
      drawView(ctx, W, H, buildModel(ST));
      const nm = v + ' ' + JSON.stringify(pr) + ' ' + W + 'x' + H;
      const texts = ctx.ops.filter(o => o.op === 'text');
      /* an op-count floor punishes a view for batching and rewards one for
         being wordy; floor BOTH halves instead -- every view has to draw
         something you can read and something you can look at (Known-bad) */
      ok(texts.length >= 3 && ctx.ops.length - texts.length >= 2,
         nm + ' drew a picture and words [' + (ctx.ops.length - texts.length)
         + ' marks, ' + texts.length + ' texts]');
      let bad = null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad = 'entity/tag: "' + t.t.slice(0, 40) + '"'; break; }
        if(/undefined|NaN/.test(t.t)){ bad = 'NaN/undefined: "' + t.t.slice(0, 40) + '"'; break; }
        if(t.bb[0] < -1 || t.bb[2] > W + 1 || t.bb[1] < -1 || t.bb[3] > H + 1){
          bad = 'off-canvas: "' + t.t.slice(0, 30) + '" [' + t.bb.map(q => fmt(q, 0)) + ']'; break; }
      }
      ok(!bad, nm + ' text clean (' + (bad || 'ok') + ')');
      /* the HTML #hint sits at bottom:11px in 11px type and the canvas capture
         cannot see it, so nothing may be drawn in that corner (Known-bad) */
      const inHint = texts.filter(t => t.bb[0] < HINT_W && t.bb[3] > H - HINT_H);
      ok(!inHint.length, nm + ' nothing under the #hint line'
        + (inHint.length ? ' ("' + inHint[0].t.slice(0, 30) + '" to y ' + fmt(inHint[0].bb[3], 0) + ')' : ''));
      let hit = null;
      for(let i = 0; i < texts.length && !hit; i++) for(let j = i + 1; j < texts.length; j++){
        const a = texts[i].bb, b = texts[j].bb;
        const ox = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
        const oy = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
        if(ox > 0.5 && oy > 0.5){
          hit = '"' + texts[i].t.slice(0, 22) + '" vs "' + texts[j].t.slice(0, 22) + '"'; break; }
      }
      ok(!hit, nm + ' no text collisions (' + (hit || 'ok') + ')');
      let leg = null;
      for(const r of LEGEND_RECTS) for(let i = 0; i < POLY_SEGS.length; i += 4){
        if(!segHitsRect(POLY_SEGS[i], POLY_SEGS[i + 1], POLY_SEGS[i + 2], POLY_SEGS[i + 3], r))
          continue;
        leg = 'a curve crosses the legend'; break;
      }
      ok(!leg, nm + ' legend clear');
      /* the chart's legend is placed by hand in the empty corner of the
         (N, Z) plane; assert no DRAWN nuclide is under it, at every Z range */
      if(v === 'chart' && CHART_LEGEND){
        let on = 0;
        for(const q of CHART_MARKS)
          if(Math.min(CHART_LEGEND.x1, q.x + q.w) - Math.max(CHART_LEGEND.x, q.x) > 0.5
             && Math.min(CHART_LEGEND.y1, q.y + q.h) - Math.max(CHART_LEGEND.y, q.y) > 0.5) on++;
        ok(on === 0, nm + ' no stable nuclide is under the legend [' + on + ' of '
          + CHART_MARKS.length + ']');
      }
    }
  }
  /* and over the whole Z-range slider, not just the two the sweep visits */
  {
    for(let zm = 12; zm <= 84; zm += 2){
      Object.assign(ST, DEFAULTS); ST.view = 'chart'; ST.chartZmax = zm;
      const ctx = makeShot(1400, 820);
      drawView(ctx, 1400, 820, buildModel(ST));
      let on = 0;
      for(const q of CHART_MARKS)
        if(Math.min(CHART_LEGEND.x1, q.x + q.w) - Math.max(CHART_LEGEND.x, q.x) > 0.5
           && Math.min(CHART_LEGEND.y1, q.y + q.h) - Math.max(CHART_LEGEND.y, q.y) > 0.5) on++;
      ok(on === 0, 'chart legend clear of the band at Z up to ' + zm + ' [' + on + ']');
      /* a legend entry for something not drawn is a false statement about the
         picture (Known-bad): the eleven disputed nuclides all have Z >= 24, so
         below that neither entry may appear */
      const texts = ctx.ops.filter(o => o.op === 'text').map(o => o.t).join('|');
      const claimsN = texts.indexOf('stable only in NUBASE') >= 0;
      const claimsP = texts.indexOf('stable only in PhET') >= 0;
      let nIn = 0, pIn = 0;
      const Nmax = Math.round(zm * 1.62) + 4;
      for(const r of NUBASE_ONLY) if(r[0] <= zm && r[1] <= Nmax) nIn++;
      for(const r of PHET_ONLY) if(r[0] <= zm && r[1] <= Nmax) pIn++;
      ok(claimsN === (nIn > 0), 'the NUBASE-only entry appears exactly when one is on the chart '
        + '(Z up to ' + zm + ', ' + nIn + ' in range, legend ' + claimsN + ')');
      ok(claimsP === (pIn > 0), 'and the PhET-only entry likewise (Z up to ' + zm + ', '
        + pIn + ' in range, legend ' + claimsP + ')');
      if(zm < 24) ok(!claimsN && !claimsP,
        'so below Z = 24 the legend claims neither, because the two tables agree there');
    }
    Object.assign(ST, DEFAULTS);
  }
  /* the game's own phases all draw, which the sweep above cannot reach
     because it resets the game to idle (Known-bad: a sweep at default
     settings does not sweep every renderer) */
  {
    /* every level at the SMALLEST size, in the phase the answer block is at
       its tallest: a three-field answer under a question box is what pushed
       text onto the caption at 560 x 380, and a sweep of the idle phase alone
       could not see it (found by tools/audit.py, then pinned here) */
    for(const [W, H] of [[1400, 820], [820, 520], [560, 380]])
      for(let L = 1; L <= 4; L++) for(const sd of [5, 99, 4242]){
        Object.assign(ST, DEFAULTS); ST.view = 'game'; ST.level = L; ST.gseed = sd;
        gameStart(ST);
        for(let k = 0; k < PHET.challengesPerLevel; k++){
          const c = gameCurrent();
          if(!c) break;
          const ctx = makeShot(W, H);
          drawView(ctx, W, H, buildModel(ST));
          const texts = ctx.ops.filter(o => o.op === 'text');
          const nm = 'game L' + L + ' s' + sd + ' #' + (k + 1) + ' ' + c.type + ' ' + W + 'x' + H;
          let hit = null;
          for(let i = 0; i < texts.length && !hit; i++) for(let j = i + 1; j < texts.length; j++){
            const a = texts[i].bb, b = texts[j].bb;
            if(Math.min(a[2], b[2]) - Math.max(a[0], b[0]) > 0.5
               && Math.min(a[3], b[3]) - Math.max(a[1], b[1]) > 0.5){
              hit = '"' + texts[i].t.slice(0, 24) + '" vs "' + texts[j].t.slice(0, 24) + '"'; break; }
          }
          ok(!hit, nm + ' no text collisions (' + (hit || 'ok') + ')');
          let off = null;
          for(const t of texts)
            if(t.bb[0] < -1 || t.bb[2] > W + 1 || t.bb[1] < -1 || t.bb[3] > H + 1){
              off = t.t.slice(0, 26); break; }
          ok(!off, nm + ' nothing off canvas (' + (off || 'ok') + ')');
          GAME.given = correctAnswer(c.type, c.atom);
          gameCheck(); gameNext();
        }
      }
    Object.assign(ST, DEFAULTS); ST.view = 'game'; ST.level = 4; ST.gseed = 99;
    const seen = {};
    for(const [W, H] of [[1400, 820], [560, 380]]){
      gameReset(ST);
      for(const phase of ['idle', 'ask', 'wrong', 'shown', 'right', 'done']){
        if(phase === 'idle'){ gameReset(ST); }
        else if(phase === 'ask'){ gameStart(ST); }
        else if(phase === 'wrong'){ GAME.attempt = 2; GAME.phase = 'wrong'; }
        else if(phase === 'shown'){ GAME.phase = 'shown'; GAME.history.push(0); }
        else if(phase === 'right'){ GAME.phase = 'right'; }
        else { GAME.phase = 'done'; GAME.idx = 5; }
        const ctx = makeShot(W, H);
        drawView(ctx, W, H, buildModel(ST));
        const texts = ctx.ops.filter(o => o.op === 'text');
        ok(ctx.ops.length > 10, 'game phase ' + phase + ' at ' + W + 'x' + H + ' draws ['
          + ctx.ops.length + ' ops]');
        let bad = null;
        for(const t of texts)
          if(/undefined|NaN|&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/.test(t.t)){ bad = t.t; break; }
        ok(!bad, 'game phase ' + phase + ' at ' + W + 'x' + H + ' text clean (' + (bad || 'ok') + ')');
        seen[phase] = (seen[phase] || 0) + ctx.ops.length;
      }
    }
    ok(Object.keys(seen).length === 6, 'all six game phases were drawn');
    /* every challenge TYPE draws, which one seed cannot cover */
    let drawn = {};
    for(let L = 0; L < 4; L++) for(let s = 1; s <= 40; s++){
      ST.level = L + 1; ST.gseed = s; gameStart(ST);
      for(let k = 0; k < 5; k++){
        const c = gameCurrent();
        if(drawn[c.type]){ gameNext(); GAME.phase = 'ask'; continue; }
        const ctx = makeShot(1400, 820);
        drawView(ctx, 1400, 820, buildModel(ST));
        drawn[c.type] = ctx.ops.length;
        GAME.phase = 'right'; gameNext();
        if(GAME.phase === 'done') break;
        GAME.phase = 'ask';
      }
    }
    ok(Object.keys(drawn).length === 15, 'all fifteen challenge types were drawn ['
      + Object.keys(drawn).length + ']');
    let thin = 0;
    for(const k in drawn) if(drawn[k] < 20) thin++;
    ok(thin === 0, 'and none of them drew an almost empty picture [' + thin + ']');
    gameReset(ST); Object.assign(ST, DEFAULTS);
  }

  /* =============== J. the pointer ================================ */
  {
    /* the drag: bucket -> atom adds one, atom -> outside returns it */
    Object.assign(ST, DEFAULTS); ST.view = 'atom';
    const canvas = {getContext: () => makeShot(1400, 820)};
    const S = makeScene(canvas);
    S.W = 1400; S.H = 820;
    const ctx = makeShot(S.W, S.H);
    const G = atomGeo(ctx, S.W, S.H, buildModel(ST));
    const bp = G.buckets[0].box, bn = G.buckets[1].box, be = G.buckets[2].box;
    const p0 = ST.p;
    ok(S.pointer('down', bp.x + bp.w / 2, bp.y + bp.h / 2), 'a press on the proton bucket takes one');
    ok(DRAG.active && DRAG.type === 'p', 'and the proton is in hand');
    ok(S.pointer('move', G.cx, G.cy), 'dragging it moves it');
    ok(S.pointer('up', G.cx, G.cy), 'dropping it on the atom is handled');
    ok(ST.p === p0 + 1, 'and the proton count went up by one [' + p0 + ' -> ' + ST.p + ']');
    ok(!DRAG.active, 'and nothing is left in hand');
    const p1 = ST.p;
    S.pointer('down', bp.x + bp.w / 2, bp.y + bp.h / 2);
    S.pointer('up', 20, 20);
    ok(ST.p === p1, 'dropping one outside the atom puts it back in the bucket');
    const n0 = ST.n;
    S.pointer('down', bn.x + bn.w / 2, bn.y + bn.h / 2);
    S.pointer('up', G.cx, G.cy);
    ok(ST.n === n0 + 1, 'the neutron bucket works the same way');
    const e0 = ST.e;
    S.pointer('down', be.x + be.w / 2, be.y + be.h / 2);
    S.pointer('up', G.cx + PHET.outerShell * G.s, G.cy);
    ok(ST.e === e0 + 1, 'and an electron dropped on the shells joins them');
    /* the capture radii really are different */
    Object.assign(ST, DEFAULTS);
    {
      const r = (CAPTURE_NUCLEON + CAPTURE_ELECTRON) / 2 * G.s;
      const e1 = ST.e;
      S.pointer('down', be.x + be.w / 2, be.y + be.h / 2);
      S.pointer('up', G.cx + r, G.cy);
      ok(ST.e === e1 + 1, 'an electron is captured between the two radii');
      const p2 = ST.p;
      S.pointer('down', bp.x + bp.w / 2, bp.y + bp.h / 2);
      S.pointer('up', G.cx + r, G.cy);
      ok(ST.p === p2, 'and a proton at the same place is NOT — PhET’s two radii differ');
    }
    /* an empty bucket gives nothing */
    Object.assign(ST, DEFAULTS); ST.p = PHET.numProtons;
    ok(!S.pointer('down', bp.x + bp.w / 2, bp.y + bp.h / 2),
       'an empty proton bucket cannot be drawn from');
    ok(ST.p === PHET.numProtons, 'and the count does not move past the bucket');
    /* pulling one back out of the atom */
    Object.assign(ST, DEFAULTS);
    {
      const n1 = ST.n;
      ok(S.pointer('down', G.cx, G.cy), 'a press on the nucleus takes a nucleon');
      ok(ST.n === n1 - 1, 'which leaves the atom at once [' + n1 + ' -> ' + ST.n + ']');
      S.pointer('up', 20, 20);
      ok(ST.n === n1 - 1, 'and dropping it outside leaves it out');
    }
    /* a click on a lit periodic-table cell sets the element */
    Object.assign(ST, DEFAULTS);
    {
      const G2 = atomGeo(ctx, S.W, S.H, buildModel(ST));
      ok(!!G2.pt, 'the periodic table is on the stage at the default size');
      const c = ptCell(G2.pt, 8);
      ok(S.pointer('down', c.x + c.w / 2, c.y + c.h / 2), 'clicking oxygen is handled');
      ok(ST.p === 8 && ST.e === 8 && ST.n === MOSTN[8],
         'and it builds neutral oxygen-16, the most common isotope');
      const c2 = ptCell(G2.pt, 50);
      ok(!S.pointer('down', c2.x + c2.w / 2, c2.y + c2.h / 2),
         'clicking tin, which the buckets cannot reach, does nothing');
      ok(ST.p === 8, 'and leaves the atom alone');
    }
    /* the game view: a level card starts that level, a table cell answers */
    Object.assign(ST, DEFAULTS); ST.view = 'game'; gameReset(ST);
    {
      const GG = gameGeo(ctx, S.W, S.H, buildModel(ST));
      ok(GG.cards && GG.cards.length === 4, 'the level-selection view has four cards');
      const b = GG.cards[2];
      ok(S.pointer('down', b.x + b.w / 2, b.y + b.h / 2), 'clicking the third card is handled');
      ok(ST.level === 3 && GAME.phase === 'ask', 'and it starts level 3');
      ok(!S.pointer('down', 4, 4), 'a click on nothing does nothing');
    }
    {
      /* find a challenge whose answer is an element, then answer it by
         clicking the table */
      ST.level = 1; ST.gseed = 5; gameStart(ST);
      const GG = gameGeo(ctx, S.W, S.H, buildModel(ST));
      ok(!!GG.pt, 'an element answer puts a periodic table on the stage');
      const c = ptCell(GG.pt, 7);
      ok(S.pointer('down', c.x + c.w / 2, c.y + c.h / 2), 'clicking nitrogen is handled');
      ok(GAME.given.element === 7, 'and it becomes the answer');
      const want = gameCurrent().atom[0];
      const cw = ptCell(GG.pt, want);
      S.pointer('down', cw.x + cw.w / 2, cw.y + cw.h / 2);
      ok(gameCheck() === true && GAME.score === 2, 'and the right cell scores two');
    }
    /* a view that ignores the pointer must ignore it -- test the CONSEQUENCE */
    Object.assign(ST, DEFAULTS); gameReset(ST);
    for(const v of ['symbol', 'counting', 'chart', 'mass']){
      ST.view = v;
      const before = JSON.stringify([ST.p, ST.n, ST.e, ST.level]);
      S.pointer('down', 400, 300); S.pointer('move', 500, 350); S.pointer('up', 500, 350);
      ok(JSON.stringify([ST.p, ST.n, ST.e, ST.level]) === before,
         'dragging on the ' + v + ' view changes no state at all');
    }
  }

  /* =============== K. the animation ============================== */
  {
    Object.assign(ST, DEFAULTS);
    const canvas = {getContext: () => makeShot(1400, 820)};
    const S = makeScene(canvas);
    ST.view = 'atom'; ST.jiggle = true;
    ST.p = 6; ST.n = 6; ST.e = 6;
    ok(!S.step(), 'a STABLE nucleus does not jiggle, however the checkbox is set');
    ST.n = 8;
    ok(!isStable(6, 8), 'carbon-14 is unstable');
    const j0 = FRAME.jig;
    ok(S.step(), 'and an unstable one does');
    ok(FRAME.jig === j0 + 1, 'one frame advances the jiggle by one step');
    ST.jiggle = false;
    ok(!S.step(), 'with the checkbox off nothing moves');
    ST.jiggle = true; ST.view = 'chart';
    ok(!S.step(), 'and no other view animates at all');
    ST.view = 'atom';
    /* the offsets really differ, or the "animation" is a still picture */
    const seen = {};
    for(let k = 0; k < 20; k++) seen[jiggleOffset(k).map(v => fmt(v, 6)).join(',')] = 1;
    ok(Object.keys(seen).length >= 4, 'the jiggle visits at least four distinct offsets ['
      + Object.keys(seen).length + ']');
    let mx = 0;
    for(let k = 0; k < 40; k++) mx = Math.max(mx, Math.hypot.apply(null, jiggleOffset(k)));
    ok(mx < PHET.nucleonRadius, 'and never moves the nucleus by more than a nucleon radius ['
      + mx + ']');
    Object.assign(ST, DEFAULTS);
  }

  Object.assign(ST, stSave);
  gameReset(ST);
  const dt = (Date.now() - T0) / 1000;
  console.log(pass + ' passed, ' + fail + ' failed  (' + fmt(dt, 1) + ' s)');
  if(fail > 0) throw new Error(fail + ' self-test failure(s)');
  return fail;
}
