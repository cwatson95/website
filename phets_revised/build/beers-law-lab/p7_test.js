
/* ================================================================== *
 *  selfTest -- headless verification.  Every reference is a line of   *
 *  build/beers-law-lab/refvals.txt (derive.py's output, read in       *
 *  full):  (python) = 50-digit decimal / exact-rational arithmetic in *
 *  the twin,  (PhET) = a constant read out of the minified original.  *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),
    name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  function R(label,i){
    const v=REF[label];
    if(!v) throw new Error('no reference line "'+label+'"');
    return v[i||0];
  }
  const stSave=Object.assign({},ST), bkSave=BK;
  const pxS=PROBE.x, pyS=PROBE.y, dxS=DET.x, dyS=DET.y;
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;

  /* ---------- A. PhET's constants, read out of the minified original ---------- */
  eq(PHET.BEAKER_VOLUME,R('PHET BEAKER_VOLUME'),'the beaker holds 1 L (PhET)');
  eq(PHET.VOL_MAX,R('PHET SOLUTION_VOLUME_RANGE min max default',1),'and the volume stops there (PhET)');
  eq(PHET.VOL_DEFAULT,R('PHET SOLUTION_VOLUME_RANGE min max default',2),'starting at 0.5 L (PhET)');
  eq(PHET.SOLUTE_MOL_MAX,R('PHET SOLUTE_AMOUNT_RANGE min max default',1),'7 mol of solute at most (PhET)');
  eq(PHET.CUVETTE_MIN,R('PHET CUVETTE_WIDTH_RANGE min max default',0),'the cuvette starts at 0.5 cm (PhET)');
  eq(PHET.CUVETTE_MAX,R('PHET CUVETTE_WIDTH_RANGE min max default',1),'and reaches 2 cm (PhET)');
  eq(PHET.CUVETTE_DEFAULT,R('PHET CUVETTE_WIDTH_RANGE min max default',2),'defaulting to 1 cm (PhET)');
  eq(PHET.CUVETTE_SNAP,R('PHET CUVETTE_SNAP_DEFAULT'),'snapping to 0.1 cm (PhET)');
  eq(PHET.DROPPER_FLOW,R('PHET DROPPER_FLOW'),'the dropper runs at 0.05 L/s (PhET)');
  eq(PHET.FAUCET_FLOW,R('PHET FAUCET_FLOW'),'the faucets at 0.25 L/s (PhET)');
  eq(PHET.EVAPORATION_MAX,R('PHET EVAPORATION_MAX'),'the evaporator to 0.25 L/s (PhET)');
  eq(PHET.SHAKER_RATE,R('PHET SHAKER_RATE'),'the shaker at 0.2 mol/s nominal (PhET)');
  eq(PHET.PARTICLES_PER_MOLE,R('PHET PARTICLES_PER_MOLE'),'200 particles per mole (PhET)');
  eq(PHET.WATER_DENSITY,R('PHET WATER_DENSITY'),'water is 1000 g/L (PhET)');
  eq(LAM0,R('PHET MIN_WAVELENGTH'),'the band starts at 380 nm (PhET)');
  eq(LAM1,R('PHET MAX_WAVELENGTH'),'and ends at 780 nm (PhET)');
  eq(NLAM,401,'so the spectra are 401 samples');
  eq(MOLE_PER_PARTICLE,R('PHET mole per shaker particle'),'each grain is 1/200 mol (PhET)');
  eq(WATER_RGB.join(),[R('PHET WATER_RGB',0),R('PHET WATER_RGB',1),R('PHET WATER_RGB',2)].join(),
     'water is rgb(224,255,255) (PhET)');
  { const d=['DEC_CONC','DEC_PERCENT','DEC_MOLAR','DEC_A','DEC_T','DEC_LAMBDA','DEC_AMOUNT',
             'DEC_CUVETTE','DEC_VOLUME'].map(k=>PHET[k]);
    const w=[]; for(let i=0;i<9;i++) w.push(R('PHET decimals conc percent molar A T lambda amount cuvette volume',i));
    eq(d.join(),w.join(),'every decimal-place count is PhET\'s (PhET)'); }
  eq(SOLUTES.length,9,'nine solutes (PhET)');
  eq(BLSOLS.length,8,'and eight Beer\'s Law solutions -- sodium chloride is colourless (PhET)');
  eq(soluteById('nonsense').id,SOLUTES[0].id,'an unknown solute id falls back rather than throwing');
  eq(blsById('sodiumChloride').id,BLSOLS[0].id,'and so does a solution that has no spectrum');
  ok(!hasSpectrum('sodiumChloride'),'sodium chloride has no spectrum at all');
  for(let i=0;i<SOLUTES.length;i++){
    const c=SOLUTE_CONST[i], s=SOLUTES[i];
    close(s.molarMass,R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',0),
          1e-12,c+' molar mass (PhET)');
    close(s.stock,R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',1),
          1e-12,c+' stock concentration (PhET)');
    close(s.cSat,R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',2),
          1e-12,c+' saturation (PhET)');
    close(stockPercent(s),R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',5),
          1e-12,c+' stock mass percent (python)');
  }

  /* ---------- B. Beer-Lambert ---------- */
  eq(absorbance(3,2,5),30,'A = eps l c is a plain product');
  eq(transmittance(0),1,'A = 0 gives T = 1 exactly (python)');
  eq(absorbanceOfT(1),0,'and T = 1 gives A = 0 exactly (python)');
  close(transmittance(1),R('BL T at A 0 1 2 3 10',1),1e-18,'A = 1 is exactly 10 % (python)');
  close(transmittance(2),R('BL T at A 0 1 2 3 10',2),1e-18,'A = 2 is exactly 1 % (python)');
  close(transmittance(3),R('BL T at A 0 1 2 3 10',3),1e-19,'A = 3 is a thousandth (python)');
  close(transmittance(10),R('BL T at A 0 1 2 3 10',4),1e-26,'and A = 10 is 1e-10 (python)');
  { const az=R('BL A at which T underflows to zero, and T just below',0);
    eq(transmittance(az),0,'T underflows to exactly 0 at A = '+az+' (python)');
    ok(transmittance(az-1)>0,'and not before');
    close(transmittance(az-1),R('BL A at which T underflows to zero, and T just below',1),
          1e-330,'the last positive value is a denormal (python)');
    ok(!isFinite(absorbanceOfT(0)),'a reading of exactly 0 % T inverts to an infinite absorbance');
    ok(absorbanceOfT(0)>0,'and it is +Infinity, not -Infinity'); }
  /* the round trip, over every solution the file carries */
  { let wa=0, wt=0, wr=0;
    for(let i=0;i<BLSOLS.length;i++){
      const d=BLSOLS[i], lm=lambdaMaxOf(d.id), e=epsAt(d.id,lm);
      for(const l of [0.5,1,1.37,2]) for(const f of [0,0.25,0.5,1]){
        const c=d.cMax*f, A=absorbance(e,l,c), Tv=transmittance(A);
        wa=Math.max(wa,Math.abs(A-e*l*c));
        wt=Math.max(wt,Math.abs(Tv-Math.pow(10,-A)));
        if(Tv>0&&A>0) wr=Math.max(wr,Math.abs(absorbanceOfT(Tv)-A)/A);
      }
    }
    eq(wa,0,'A is the product, evaluated once');
    eq(wt,0,'and T the power, evaluated once');
    ok(wr<=R('BL roundtrip worst rel A T backA propagated',2)*4,
       'the round trip -log10(10^-A) = A holds to '+wr.toExponential(2)
       +', against the twin\'s '+R('BL roundtrip worst rel A T backA propagated',2)+' (python)'); }
  /* the eight solutions, against the twin */
  for(let i=0;i<BLSOLS.length;i++){
    const c=BLS_CONST[i], d=BLSOLS[i], lbl='BL '+c+' lambdaMax eps cmax cdefault Amax2cm';
    eq(lambdaMaxOf(d.id),R(lbl,0),c+' lambda_max is '+R(lbl,0)+' nm (python)');
    close(epsMaxOf(d.id),R(lbl,1),1e-12,c+' eps at the peak (PhET)');
    close(d.cMax,R(lbl,2),1e-18,c+' concentration range (PhET)');
    close(d.cDefault,R(lbl,3),1e-18,c+' default concentration (PhET)');
    close(absorbance(epsMaxOf(d.id),PHET.CUVETTE_MAX,d.cMax),R(lbl,4),1e-12,
          c+' largest absorbance in a 2 cm cuvette (python)');
  }
  { const got=BLSOLS.map(d=>lambdaMaxOf(d.id)).join();
    const want=[]; for(let i=0;i<8;i++) want.push(R('EPS lambdaMax in file order',i));
    eq(got,want.join(),'every lambda_max matches the twin (python)'); }
  ok(lambdaMaxOf('copperSulfate')===LAM1,
     'copper sulfate peaks at the LAST sample: its band is in the infrared and PhET\'s table stops at the eye');
  /* eps is a lookup, not an interpolation */
  eq(epsAt('potassiumPermanganate',500),R('EPS quantisation KMnO4 at 500 500.999 501',0),
     'eps at 500 nm (PhET)');
  eq(epsAt('potassiumPermanganate',500.999),R('EPS quantisation KMnO4 at 500 500.999 501',1),
     'and at 500.999 nm -- the same cell (python)');
  eq(epsAt('potassiumPermanganate',501),R('EPS quantisation KMnO4 at 500 500.999 501',2),
     'while 501 nm reads the next one (python)');
  ok(epsAt('potassiumPermanganate',500)!==epsAt('potassiumPermanganate',501),
     'so the step is real and not a coincidence of equal values');
  eq(epsAt('potassiumPermanganate',379.9),null,'below 380 nm PhET has no data');
  eq(epsAt('potassiumPermanganate',781),null,'and above 780 nm neither');
  eq(epsAt('drinkMix',780.5),EPS.drinkMix[NLAM-1],'780.5 nm still reads the last cell (python)');
  eq(epsAt('sodiumChloride',500),null,'a solute with no spectrum returns null, not zero');
  /* two cuvettes: T multiplies, A adds -- the reason the instrument reports A */
  { const e=epsMaxOf('drinkMix'), c=0.1;
    const A1=absorbance(e,1,c), A2=absorbance(e,1,c);
    close(transmittance(A1)*transmittance(A2),transmittance(absorbance(e,2,c)),1e-15,
          'two 1 cm cuvettes transmit T squared, which is one 2 cm cuvette');
    close(A1+A2,absorbance(e,2,c),1e-15,'and their absorbances add'); }

  /* ---------- C. the beaker: the mole ledger ---------- */
  /* PhET's shaker arithmetic: round(max(1, rate * 200 * dt)) grains a frame */
  close(PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*FRAME_DT,
        R('SHAKER bracket perFrame deliveredMolPerS nominal',0),1e-15,
        'the shaker\'s per-frame bracket is 0.667 at 60 fps (python)');
  eq(shakerPerFrame(FRAME_DT),R('SHAKER bracket perFrame deliveredMolPerS nominal',1),
     'so one grain a frame comes out of it (python)');
  close(shakerPerFrame(FRAME_DT)*MOLE_PER_PARTICLE/FRAME_DT,
        R('SHAKER bracket perFrame deliveredMolPerS nominal',2),1e-12,
        'and the shaker delivers 0.30 mol/s at 60 fps, not its nominal 0.20 (python)');
  ok(R('SHAKER bracket perFrame deliveredMolPerS nominal',2)
     >R('SHAKER bracket perFrame deliveredMolPerS nominal',3),
     'which is MORE than PhET\'s own maxDispensingRate');
  /* which half of PhET's expression does it, at which frame rate: the ROUNDING at 60 fps
     (0.667 rounds to 1 with or without the floor), the FLOOR above about 80 */
  eq(shakerPerFrame(1/120),R('SHAKER at 120 fps perFrame delivered, and at 1 s',0),
     'at 120 fps the max(1, ...) floor is what keeps a grain coming (python)');
  close(shakerPerFrame(1/120)*MOLE_PER_PARTICLE*120,
        R('SHAKER at 120 fps perFrame delivered, and at 1 s',1),1e-12,
        'and the same shaker then delivers 0.60 mol/s (python)');
  close(shakerPerFrame(1)*MOLE_PER_PARTICLE,
        R('SHAKER at 120 fps perFrame delivered, and at 1 s',2),1e-12,
        'only at a whole-second step is the delivered rate the nominal one (python)');
  eq(shakerPerFrame(1),Math.round(PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE),
     'where neither the rounding nor the floor bites');
  /* the 900-frame script, the same one derive.py runs */
  function scriptRun(){
    const B=makeBeaker('drinkMix',0,0.5);
    const rng=makeRngB(4242);
    for(let i=0;i<900;i++){
      bkStep(B,FRAME_DT,{faucet:(i>=60&&i<160)?PHET.FAUCET_FLOW:0,
                         drain:(i>=500&&i<560)?PHET.FAUCET_FLOW:0,
                         dropper:(i>=200&&i<400)?PHET.DROPPER_FLOW:0,
                         evap:(i>=600&&i<690)?PHET.EVAPORATION_MAX:0,
                         shaking:(i>=700&&i<860)},rng);
    }
    return B;
  }
  { const B=scriptRun();
    const r=bkLedgerResidual(B);
    eq(r.n,0,'the mole ledger closes to the last bit over 900 frames');
    eq(r.V,0,'and so does the volume ledger');
    close(B.V,R('LEDGER final n V, exact n V, float residual n V',1),1e-15,
          'the final volume matches the twin exactly (python)');
    close(B.led.faucet,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',3),
          1e-15,'the faucet put in what the twin says (python)');
    close(B.led.dropperV,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',4),
          1e-15,'and the dropper (python)');
    close(B.led.drainedV,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',5),
          1e-15,'the drain took out what the twin says (python)');
    close(B.led.evaporated,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',6),
          1e-15,'and the evaporator (python)');
    close(B.led.dropper,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',1),
          1e-15,'the dropper\'s moles match the twin (python)');
    close(B.led.drained,R('LEDGER shaker dropper drained faucet dropperV drainedV evaporated',2),
          1e-15,'and the drain\'s (python)');
    /* the shaker's total is dispensed deterministically even though the FLIGHT is not:
       160 shaking frames, one grain each, 1/200 mol each */
    close(B.led.shaker+B.led.flying,R('LEDGER shaker particles landed')*MOLE_PER_PARTICLE,
          1e-12,'the shaker dispensed exactly 160 grains of 1/200 mol (python)');
    ok(B.led.shaker>0,'and most of them have landed by the end of the script');
    /* let the rest land, and the beaker must reach the twin's mole count exactly */
    let guard=0;
    while(B.parts.length&&guard++<3000)
      bkStep(B,FRAME_DT,{faucet:0,drain:0,dropper:0,evap:0,shaking:false},makeRngB(1));
    ok(guard<3000,'every grain lands in finite time ('+guard+' frames)');
    eq(B.led.flying,0,'and nothing is left in the air');
    close(B.n,R('LEDGER final n V, exact n V, float residual n V',0),1e-12,
          'the beaker then holds exactly the twin\'s 1.14375 mol (python)');
    close(B.n,R('LEDGER final n V, exact n V, float residual n V',2),1e-12,
          'which is also the exact-rational answer (python)');
    eq(bkLedgerResidual(B).n,0,'and the ledger still closes'); }
  /* the clamps hold, and the ledger closes THROUGH them */
  { const B=makeBeaker('drinkMix',6.9,0.98);
    const rng=makeRngB(7);
    for(let i=0;i<400;i++)
      bkStep(B,FRAME_DT,{faucet:PHET.FAUCET_FLOW,drain:0,dropper:PHET.DROPPER_FLOW,
                         evap:0,shaking:true},rng);
    ok(B.V<=PHET.VOL_MAX+1e-15,'the beaker never overfills');
    ok(B.n<=PHET.SOLUTE_MOL_MAX+1e-15,'and never passes PhET\'s 7 mol ceiling');
    close(B.n,PHET.SOLUTE_MOL_MAX,1e-12,'it sits exactly on it');
    close(bkLedgerResidual(B).n,0,1e-15,'and the ledger closes through both clamps');
    close(bkLedgerResidual(B).V,0,1e-15,'in volume too'); }
  /* saturation */
  { const cs=soluteById('copperSulfate').cSat;
    close(cs,R('SAT CuSO4 2mol 1L Csat precip conc',0),1e-15,'CuSO4 saturates at 1.38 M (PhET)');
    const B=makeBeaker('copperSulfate',2,1);
    ok(bkSaturated(B),'2 mol in 1 L of it is past saturation');
    close(bkPrecip(B),R('SAT CuSO4 2mol 1L Csat precip conc',1),1e-15,
          'so 0.62 mol is solid (python)');
    close(bkConc(B),R('SAT CuSO4 2mol 1L Csat precip conc',2),1e-15,
          'and the solution reads exactly Csat (python)');
    /* draining a saturated beaker takes solute at Csat, not at n/V */
    const B2=makeBeaker('copperSulfate',2,1);
    bkStep(B2,1,{faucet:0,drain:0.1,dropper:0,evap:0,shaking:false},makeRngB(1));
    close(2-B2.n,R('SAT drained moles at Csat vs naive',0),1e-14,
          'draining 0.1 L takes Csat x 0.1 mol (python)');
    ok(2-B2.n<R('SAT drained moles at Csat vs naive',1),
       'which is LESS than (n/V) x 0.1: the precipitate does not go down the drain');
    ok(!bkSaturated(makeBeaker('copperSulfate',1,1)),'1 mol in 1 L is not saturated');
    eq(bkPrecip(makeBeaker('copperSulfate',1,1)),0,'and nothing is solid');
    ok(!bkSaturated(makeBeaker('copperSulfate',2,0)),'an EMPTY beaker is not "saturated"');
    eq(bkConc(makeBeaker('copperSulfate',2,0)),0,'and reads zero rather than dividing by zero');
    /* the clamps only differ from no clamp at all when they BITE, so drain a beaker that
       holds less than the drain is asking for */
    const B4=makeBeaker('drinkMix',0.3,0.05);
    const c4=bkConc(B4);
    bkStep(B4,1,{faucet:0,drain:0.4,dropper:0,evap:0,shaking:false},makeRngB(1));
    eq(B4.V,0,'draining 0.4 L from a beaker holding 0.05 L empties it and stops');
    ok(B4.V>=0,'it does not go negative');
    close(B4.led.drainedV,0.05,1e-15,'and the ledger records the 0.05 L that MOVED, '
          +'not the 0.4 L that was asked for');
    close(0.3-B4.n,c4*0.05,1e-15,'so the solute it carried away is C times the volume '
          +'that actually left');
    close(bkLedgerResidual(B4).n,0,1e-15,'with the mole ledger closed through the clamp');
    close(bkLedgerResidual(B4).V,0,1e-15,'and the volume ledger');
    const B5=makeBeaker('drinkMix',0.3,0.05);
    bkStep(B5,1,{faucet:0,drain:0,dropper:0,evap:0.4,shaking:false},makeRngB(1));
    eq(B5.V,0,'evaporating more than is there empties it and stops');
    close(B5.n,0.3,1e-15,'leaving every mole of solute behind');
    close(B5.led.evaporated,0.05,1e-15,'and recording only what evaporated'); }
  /* evaporation follows C = n/V exactly to the saturation volume, then stops */
  { const cs=soluteById('nickelIIChloride').cSat;
    close(saturationVolume(0.5,cs),R('EVAP NiCl2 n Csat Vsat tsat at 0.25 L/s',2),1e-15,
          'Vsat = n/Csat (python)');
    close(timeToSaturate(0.5,1,cs,PHET.EVAPORATION_MAX),
          R('EVAP NiCl2 n Csat Vsat tsat at 0.25 L/s',3),1e-12,
          'and the evaporator takes 3.616 s to get there (python)');
    eq(timeToSaturate(0.5,0.05,cs,PHET.EVAPORATION_MAX),null,
       'below Vsat there is no time to saturation to report');
    const Vs=[1,0.5,0.2,0.1];
    for(let i=0;i<4;i++)
      close(bkConc(makeBeaker('nickelIIChloride',0.5,Vs[i])),
            R('EVAP C at V = 1.0 0.5 0.2 0.1 L (n = 0.5 mol NiCl2)',i),1e-15,
            'C at V = '+Vs[i]+' L is n/V exactly (python)');
    const Vp=[0.09,0.05,0.02];
    for(let i=0;i<3;i++)
      close(bkPrecip(makeBeaker('nickelIIChloride',0.5,Vp[i])),
            R('EVAP precipitate at V = 0.09 0.05 0.02 L',i),1e-15,
            'and the solid at V = '+Vp[i]+' L (python)');
    eq(bkPrecip(makeBeaker('nickelIIChloride',0.5,0.1)),0,'nothing is solid just above Vsat');
    ok(bkPrecip(makeBeaker('nickelIIChloride',0.5,0.09))>0,'and something is just below it');
    /* evaporating really does walk that curve */
    const B=makeBeaker('nickelIIChloride',0.5,1);
    for(let i=0;i<60;i++) bkStep(B,FRAME_DT,{faucet:0,drain:0,dropper:0,
                                             evap:PHET.EVAPORATION_MAX,shaking:false},makeRngB(1));
    close(B.n,0.5,1e-15,'a second of evaporating removes no solute at all');
    close(B.V,1-PHET.EVAPORATION_MAX,2e-14,'and exactly 0.25 L of solvent');
    close(bkConc(B),0.5/B.V,1e-15,'so the concentration is n/V on the nose'); }
  /* the dropper's mixing law */
  { const stock=soluteById('potassiumPermanganate').stock;
    const B=makeBeaker('potassiumPermanganate',0,0.5);
    for(let i=0;i<60;i++) bkStep(B,FRAME_DT,{faucet:0,drain:0,dropper:PHET.DROPPER_FLOW,
                                             evap:0,shaking:false},makeRngB(1));
    close(B.V-0.5,PHET.DROPPER_FLOW,2e-14,'a second of the dropper adds 0.05 L (python)');
    close(B.n,R('DROPPER KMnO4 stock dV n C after 1 s from 0.5 L of water',2),2e-14,
          'carrying stock x 0.05 mol (python)');
    close(bkConc(B),R('DROPPER KMnO4 stock dV n C after 1 s from 0.5 L of water',3),2e-14,
          'so the beaker reads c_stock dV/(V0+dV) (python)');
    const B2=makeBeaker('potassiumPermanganate',0,0);
    for(let i=0;i<60*20;i++) bkStep(B2,FRAME_DT,{faucet:0,drain:0,dropper:PHET.DROPPER_FLOW,
                                                 evap:0,shaking:false},makeRngB(1));
    close(B2.V,R('DROPPER stock-only fill V C',0),1e-15,'twenty seconds fills the beaker (python)');
    close(bkConc(B2),R('DROPPER stock-only fill V C',1),1e-12,
          'and a beaker of stock alone reads the stock concentration (python)');
    close(bkConc(B2),stock,1e-12,'which is PhET\'s 0.4 mol/L');
    /* every one of PhET's stock solutions is BELOW its own saturation point, so the
       dropper can never saturate a beaker by itself and a drop into a saturated one
       DISSOLVES solid.  Both halves are asserted, because the second follows from the
       first and neither is obvious. */
    for(const s2 of SOLUTES)
      ok(s2.stock<s2.cSat,s2.id+'\'s stock solution is below its own saturation point (PhET)');
    /* 0.8 L, not the brim: at V = 1 L addSolvent returns zero and the dropper does
       nothing at all, so the test would be asserting about a step that never happened */
    const B3=makeBeaker('copperSulfate',1.6,0.8);
    const p0=bkPrecip(B3);
    bkStep(B3,FRAME_DT,{faucet:0,drain:0,dropper:PHET.DROPPER_FLOW,evap:0,shaking:false},
           makeRngB(1));
    ok(bkPrecip(B3)<p0,'so a drop of stock into a saturated beaker DISSOLVES solid');
    ok(B3.V<PHET.VOL_MAX,'with room in the beaker for the drop to go in');
    close(bkPrecip(B3),B3.n-B3.V*soluteById('copperSulfate').cSat,1e-15,
          'and the solid left is the end state, computed once: PhET\'s '
          +'updatePrecipitateAmount flag guards a transient this file does not have');
    close(bkLedgerResidual(B3).n,0,1e-15,'with the ledger still closed'); }
  /* grams and mass percent */
  { const nacl=soluteById('sodiumChloride');
    close(soluteGrams(1,1,nacl.cSat,nacl.molarMass),R('MASS 1M NaCl grams percent',0),1e-12,
          '1 M NaCl in 1 L is 58.443 g (python)');
    close(percentConcentration(soluteGrams(1,1,nacl.cSat,nacl.molarMass),1),
          R('MASS 1M NaCl grams percent',1),1e-12,'which is 5.52 mass percent (python)');
    const cu=soluteById('copperSulfate');
    close(soluteGrams(3,1,cu.cSat,cu.molarMass),R('MASS CuSO4 3mol in 1L dissolved grams'),1e-11,
          'past saturation only the DISSOLVED solute is weighed (python)');
    eq(percentConcentration(10,0),0,'an empty beaker is 0 mass percent, not a division by zero');
    for(let i=0;i<SOLUTES.length;i++){
      const s=SOLUTES[i], c=SOLUTE_CONST[i];
      close(soluteGrams(0.5,0.5,s.cSat,s.molarMass),
            R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',3),1e-11,
            c+' grams at 1 M (python)');
      close(percentConcentration(soluteGrams(0.5,0.5,s.cSat,s.molarMass),0.5),
            R('MASS '+c+' molarMass stock Csat gramsAt1M percentAt1M stockPercent',4),1e-11,
            c+' mass percent at 1 M (python)');
    } }
  /* the drawn grain count */
  { const w=[0,1e-9,0.0026,0.5];
    for(let i=0;i<4;i++)
      eq(particleCount(w[i]),R('PARTICLES at 0 1e-9 0.0026 0.5 mol',i),
         'the solid at '+w[i]+' mol draws that many grains (python)');
    eq(particleCount(0),0,'no solid, no grains');
    ok(particleCount(1e-12)===1,'but a trace still draws one, as PhET\'s does'); }

  /* ---------- D. PhET's two colour laws ---------- */
  { const m=lerpRGBfloor([224,255,255],[255,225,225],0.5);
    eq(m.join(),[R('COLOR floor midpoint water to drinkmix mid',0),
                 R('COLOR floor midpoint water to drinkmix mid',1),
                 R('COLOR floor midpoint water to drinkmix mid',2)].join(),
       'Color.interpolateRGBA FLOORS: the midpoint is (239,240,240), not (240,240,240) (python)');
    ok(m[0]===239,'which is one less than a rounding would give'); }
  for(let i=0;i<SOLUTES.length;i++){
    const s=SOLUTES[i], c=SOLUTE_CONST[i];
    const cs=[0,s.cMid/2,s.cMid,(s.cMid+s.cSat)/2,s.cSat];
    const got=[]; cs.forEach(x=>{ got.push.apply(got,schemeColor(s.id,x)); });
    const want=[]; for(let k=0;k<15;k++)
      want.push(R('SCHEME '+c+' rgb at 0, mid/2, mid, (mid+sat)/2, sat',k));
    eq(got.join(),want.join(),c+' three-stop colour scheme (python)');
  }
  for(let i=0;i<BLSOLS.length;i++){
    const d=BLSOLS[i], c=BLS_CONST[i];
    const got=[]; [0,1e-12,d.cMax/2,d.cMax].forEach(x=>{ got.push.apply(got,rampColor(d.id,x)); });
    const want=[]; for(let k=0;k<12;k++) want.push(R('RAMP '+c+' rgb at 0, 0+, cmax/2, cmax',k));
    eq(got.join(),want.join(),c+' two-stop Beer\'s Law ramp (python)');
  }
  /* ConcentrationSolution.createColor shows the SOLVENT at c = 0, and SoluteColorScheme
     would return minColor there anyway.  For PhET's nine that is the same colour, so the
     branch is redundant -- which is a fact about PhET's data, not about the code, and is
     asserted as one: add a solute whose minColor is not water and it starts to matter. */
  { for(const s2 of SOLUTES){
      eq(s2.minRGB.join(),WATER_RGB.join(),s2.id+"'s minColor is the water colour (PhET)");
      eq(s2.cMin,0,s2.id+"'s low stop is at zero concentration (PhET)");
    }
    eq(schemeColor('drinkMix',0).join(),WATER_RGB.join(),'an empty solution is water-coloured');
    eq(schemeColor('drinkMix',99).join(),'255,0,0','and past saturation it stops changing');
    eq(rampColor('drinkMix',0).join(),
       [R('RAMP jump at zero, water then colorLo',0),R('RAMP jump at zero, water then colorLo',1),
        R('RAMP jump at zero, water then colorLo',2)].join(),'the ramp is water at exactly 0 (python)');
    eq(rampColor('drinkMix',1e-12).join(),
       [R('RAMP jump at zero, water then colorLo',3),R('RAMP jump at zero, water then colorLo',4),
        R('RAMP jump at zero, water then colorLo',5)].join(),'and jumps to its low stop above it (python)');
    ok(rampColor('drinkMix',0).join()!==rampColor('drinkMix',1e-12).join(),
       'so the ramp has a genuine step at c = 0, which is PhET\'s');
    eq(rampColor('drinkMix',99).join(),'255,0,0','and it clamps at the top'); }

  /* ---------- E. the colour the solution really transmits ---------- */
  close(CIE_X[0],R('CIE first row 380 xbar ybar zbar',0),1e-15,'the CIE table starts at 380 nm (CIE)');
  close(CIE_Y[NLAM-1],R('CIE last row 780 xbar ybar zbar',1),1e-18,'and ends at 780 nm (CIE)');
  { let sx=0,sy=0,sz=0;
    for(let i=0;i<NLAM;i++){ sx+=CIE_X[i]; sy+=CIE_Y[i]; sz+=CIE_Z[i]; }
    rel(sx,R('CIE sums over 380..780 x y z',0),1e-12,'x-bar sums to the twin\'s value (python)');
    rel(sy,R('CIE sums over 380..780 x y z',1),1e-12,'y-bar too (python)');
    rel(sz,R('CIE sums over 380..780 x y z',2),1e-12,'and z-bar (python)');
    let k=0; for(let i=0;i<NLAM;i++) if(CIE_Y[i]>CIE_Y[k]) k=i;
    eq(LAM0+k,555,'y-bar peaks at 555 nm, as the CIE defines it');
    close(CIE_Y[k],1,1e-12,'at exactly 1'); }
  /* the transfer curve, including its LINEAR segment, which every colour the suite
     checks is either far above or exactly at zero */
  { const us=[0.001,0.0031308,0.5,1];
    for(let i=0;i<4;i++)
      rel(srgbGamma(us[i]),R('SRGB gamma at 0.001 0.0031308 0.5 1',i),1e-12,
          'srgbGamma('+us[i]+') (python)');
    eq(srgbGamma(-1),0,'and it clamps a negative channel to black, which is the ONLY '
       +'clamp on that path');
    close(srgbGamma(2),1,1e-15,'and an over-bright one to white (1.055 - 0.055 is a rounding short of 1)');
    ok(Math.abs(srgbGamma(0.002)-12.92*0.002)<1e-15,
       'below the knee it is the linear segment, 12.92u'); }
  close(illumAt('E',500),1,0,'illuminant E is flat by definition');
  close(illumAt('A',560),100,1e-9,'illuminant A is normalised to 100 at 560 nm (CIE)');
  { const lams=[380,480,560,660,780];
    for(let i=0;i<5;i++)
      rel(illumAt('A',lams[i]),R('ILLUM A at 380 480 560 660 780',i),1e-12,
          'illuminant A at '+lams[i]+' nm (python)'); }
  { const w=trueRGB('drinkMix',1,0,'E');
    eq(w.rgb.join(),'255,255,255','an empty cuvette renders exactly white under E');
    close(w.Y,1,1e-15,'and transmits all of the light');
    const wA=trueRGB('drinkMix',1,0,'A');
    eq(wA.rgb.join(),'255,255,255','and under illuminant A too: the adaptation is exact');
    eq(trueRGB('sodiumChloride',1,1,'E'),null,'a solute with no spectrum has no computed colour'); }
  for(let i=0;i<BLSOLS.length;i++){
    const d=BLSOLS[i], c=BLS_CONST[i];
    const lbl='TRUE '+c+' rgb and Y at cmax/4 and cmax, l = 1 cm';
    const a=trueRGB(d.id,1,d.cMax*0.25,'E'), b=trueRGB(d.id,1,d.cMax,'E');
    eq(a.rgb.join(),[R(lbl,0),R(lbl,1),R(lbl,2)].join(),c+' true colour at a quarter scale (python)');
    rel(a.Y,R(lbl,3),1e-11,c+' transmitted luminance there (python)');
    eq(b.rgb.join(),[R(lbl,4),R(lbl,5),R(lbl,6)].join(),c+' true colour at full scale (python)');
    rel(b.Y,R(lbl,7),1e-11,c+' transmitted luminance there (python)');
    ok(b.Y<a.Y,c+': four times the concentration transmits less light');
    const pr='PHETRAMP '+c+' rgb at cmax/4 and cmax';
    eq(rampColor(d.id,d.cMax*0.25).join(),[R(pr,0),R(pr,1),R(pr,2)].join(),
       c+' PhET ramp at a quarter scale (python)');
  }
  /* the two do not agree anywhere, and the gap is measured rather than asserted */
  { let smallest=1e9;
    for(let i=0;i<BLSOLS.length;i++){
      const d=BLSOLS[i], c=BLS_CONST[i];
      let worst=0, wc=0;
      for(let j=1;j<=50;j++){
        const cc=d.cMax*j/50, t=trueRGB(d.id,1,cc,'E').rgb, p=rampColor(d.id,cc);
        const g=Math.max(Math.abs(t[0]-p[0]),Math.abs(t[1]-p[1]),Math.abs(t[2]-p[2]));
        if(g>worst){ worst=g; wc=cc; }
      }
      eq(worst,R('GAP '+c+' worst channel, at c',0),c+' worst channel gap is '+worst+'/255 (python)');
      close(wc,R('GAP '+c+' worst channel, at c',1),1e-15,'at the twin\'s concentration (python)');
      smallest=Math.min(smallest,worst);
    }
    eq(smallest,R('GAP smallest and largest worst-channel gap',0),
       'the SMALLEST worst-channel gap over the eight is '+smallest+'/255 (python)');
    ok(smallest>20,'so PhET\'s ramp is nowhere close to the transmitted colour'); }
  /* PhET's ramp has no path length in it; the real colour does */
  { const d=blsById('potassiumPermanganate'), c=d.cMax/2;
    eq(rampColor(d.id,c).join(),rampColor(d.id,c).join(),'PhET\'s ramp cannot see the cuvette width');
    const lbl='PATHLEN KMnO4 cmax/2 rgb at 0.5 cm and 2 cm, Y each, mono ratio at lambdaMax';
    const thin=trueRGB(d.id,0.5,c,'E'), thick=trueRGB(d.id,2,c,'E');
    eq(thin.rgb.join(),[R(lbl,0),R(lbl,1),R(lbl,2)].join(),'0.5 cm of it (python)');
    eq(thick.rgb.join(),[R(lbl,3),R(lbl,4),R(lbl,5)].join(),'and 2 cm of it (python)');
    ok(thin.rgb.join()!==thick.rgb.join(),'which are different colours, as they must be');
    rel(thin.Y,R(lbl,6),1e-11,'the thin one\'s luminance (python)');
    rel(thick.Y,R(lbl,7),1e-11,'and the thick one\'s (python)');
    /* the monochromatic beam falls far faster than the luminance: an integral over a band
       is not a single exponential, and that is the point the view makes */
    const mono=transmittance(absorbance(epsMaxOf(d.id),2,c))
              /transmittance(absorbance(epsMaxOf(d.id),0.5,c));
    rel(mono,R(lbl,8),1e-12,'the beam at lambda_max is cut to 6.3 % over that change (python)');
    ok(thick.Y/thin.Y>4*mono,'while the luminance keeps '+fmt(thick.Y/thin.Y,4)
       +' -- far more, because the shoulders carry the integral'); }
  /* and a saturated beaker is simply black */
  { const lbl='OPAQUE KMnO4 saturated 0.5 cm Y rgb';
    const t=trueRGB('potassiumPermanganate',0.5,soluteById('potassiumPermanganate').cSat,'E');
    rel(t.Y,R(lbl,0),1e-9,'saturated KMnO4 through 5 mm transmits 3.2e-10 of the light (python)');
    eq(t.rgb.join(),'0,0,0','and renders as exactly black'); }
  /* the darkening comparison the view prints */
  { const lbl='DARKEN KMnO4 trueY ratio, phet ramp lum ratio, Y at cmax/10 and cmax';
    const d=blsById('potassiumPermanganate');
    const lo=trueRGB(d.id,1,d.cMax*0.1,'E'), hi=trueRGB(d.id,1,d.cMax,'E');
    rel(lo.Y/hi.Y,R(lbl,0),1e-11,'the true colour darkens 3.20-fold over a decade of c (python)');
    rel(relLum(rampColor(d.id,d.cMax*0.1))/relLum(rampColor(d.id,d.cMax)),R(lbl,1),1e-11,
        'and PhET\'s ramp 2.64-fold (python)');
    ok(lo.Y/hi.Y>relLum(rampColor(d.id,d.cMax*0.1))/relLum(rampColor(d.id,d.cMax)),
       'so the true colour does darken more -- but only by 1.2, so luminance is not the story'); }
  /* the display-only wavelength colour, pinned per wavelength: a helper nothing asserts
     is a helper a unit mistake can paint the whole band red in (Known-bad) */
  { const WV=[420,480,555,620,700], got=[];
    for(const w of WV) got.push.apply(got,waveRGB(w));
    const want=[]; for(let i=0;i<15;i++) want.push(R('WAVE rgb at 420 480 555 620 700',i));
    eq(got.join(),want.join(),'the beam colour at 420, 480, 555, 620 and 700 nm (python)');
    eq(waveRGB(300).join(),'0,0,0','below the band there is no colour at all');
    eq(waveRGB(900).join(),'0,0,0','and above it neither');
    const g=waveRGB(555);
    ok(g[1]>=g[0]&&g[1]>=g[2],'555 nm is green');
    eq(Math.max(g[0],g[1],g[2]),255,'and at full brightness, being where the eye peaks');
    const v=waveRGB(420);
    ok(Math.max(v[0],v[1],v[2])<120,'420 nm is dim, because the eye barely sees it'); }
  /* the bound past which the straight line is an extrapolation */
  { close(LINEAR_LIMIT,R('LINEAR LIMIT mol per L'),1e-18,
          'Beer-Lambert is drawn as linear to 10 mM (a teaching bound, not a measurement)');
    let past=0;
    for(const d of BLSOLS) if(d.cMax>LINEAR_LIMIT) past++;
    eq(past,5,'five of the eight ranges run past it');
    Object.assign(ST,DEFAULTS); ST.blSolution='drinkMix'; ST.blConc=0.02;
    ok(cuvetteModel().beyondLinear,'20 mM is past it');
    ST.blConc=0.005;
    ok(!cuvetteModel().beyondLinear,'and 5 mM is not');
    Object.assign(ST,DEFAULTS); }

  /* ---------- F. PhET's data against the literature ---------- */
  { let worstM=0, worstC=0;
    for(let i=0;i<SOLUTES.length;i++){
      const s=SOLUTES[i], c=SOLUTE_CONST[i], lbl='LIT '+c+' molarMassLit gPerL cLit relC';
      close(s.lit.M,R(lbl,0),1e-12,c+' literature molar mass (source)');
      close(s.lit.gPerL,R(lbl,1),1e-9,c+' solubility in g/L (source)');
      const cLit=s.lit.gPerL/s.lit.M;
      rel(cLit,R(lbl,2),1e-12,c+' converted to mol/L (python)');
      rel(Math.abs(s.cSat-cLit)/cLit,Math.abs(R(lbl,3)),1e-9,c+' relative gap (python)');
      worstM=Math.max(worstM,Math.abs(s.molarMass-s.lit.M)/s.lit.M);
      worstC=Math.max(worstC,Math.abs(s.cSat-cLit)/cLit);
    }
    rel(worstM,R('LIT worst molar-mass and saturation relative gaps',0),1e-9,
        'the worst molar-mass gap over the nine is 5.6e-5 (python)');
    rel(worstC,R('LIT worst molar-mass and saturation relative gaps',1),1e-9,
        'and the worst saturation gap 22.8 %, which is the 0 C source (python)');
    ok(worstM<2e-4,'so every molar mass is the literature\'s');
    for(const id of ['potassiumChromate','potassiumPermanganate','nickelIIChloride',
                     'potassiumDichromate']){
      const s=soluteById(id), cLit=s.lit.gPerL/s.lit.M;
      ok(Math.abs(s.cSat-cLit)/cLit<0.01,
         id+'\'s saturation is within 1 % of a source quoted near room temperature');
    }
    ok(Math.abs(soluteById('drinkMix').molarMass-342.297)<=1.01e-3,
       'PhET\'s drink mix carries sucrose\'s molar mass: it is sugar'); }

  /* ---------- G. the panels build clean for every view and every preset ---------- */
  { Object.assign(ST,DEFAULTS);
    let bad='';
    for(const [v] of TABS){
      for(const s of SOLUTES){
        for(const blsId of (SHOW_BEERS?[BLSOLS[0].id,BLSOLS[7].id]:[BLSOLS[0].id])){
          for(const units of ['molar','percent']){
            ST.view=v; ST.solute=s.id; ST.blSolution=blsId; ST.meterUnits=units;
            BK=makeBeaker(s.id,1.2,0.4);
            ST.blConc=blsById(blsId).cDefault; ST.wavelength=lambdaMaxOf(blsId);
            const M=buildModel();
            const ro=readoutHTML(M), eb=eqbarHTML(M), tg=tagHTML(M);
            for(const [nm,txt] of [['readout',ro],['eqbar',eb],['tag',tg]]){
              if(/NaN|undefined|Infinity/.test(txt)&&!bad) bad=v+'/'+s.id+' '+nm;
            }
            if(ro.length<400&&!bad) bad=v+'/'+s.id+' readout too short';
          }
        }
      }
    }
    ok(!bad,'every view x solute x solution x unit builds clean panels'+(bad?' ('+bad+')':''));
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }
  /* no slider combination makes a non-finite model */
  { let bad='';
    Object.assign(ST,DEFAULTS);
    for(const n of [0,0.001,3.5,7]) for(const V of [0,0.001,0.5,1])
      for(const l of [PHET.CUVETTE_MIN,1,PHET.CUVETTE_MAX])
        for(const lam of [LAM0,500,LAM1]){
          BK=makeBeaker('copperSulfate',n,V);
          ST.solute='copperSulfate'; ST.cuvette=l; ST.lightMode='variable'; ST.wavelength=lam;
          for(const [v] of TABS){
            ST.view=v;
            const M=buildModel();
            /* the model's SCALARS must all be finite.  Drawing arrays are exempt on
               purpose: the ledger view's uncapped n/V curve carries NaN where V = 0, which
               is how polyline() is told to leave a gap, and that gap has its own assertion
               below rather than a blanket exemption here. */
            const walk=(o,path)=>{
              if(o===null||o===undefined) return;
              if(typeof o==='number'){ if(!isFinite(o)&&!bad) bad=v+' '+path+' n='+n+' V='+V; return; }
              if(Array.isArray(o)) return;
              if(typeof o==='object') for(const k in o) walk(o[k],path+'.'+k);
            };
            walk(M,'');
          }
        }
    ok(!bad,'no combination of the sliders makes a non-finite model'+(bad?' ('+bad+')':''));
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }
  /* the one deliberate gap: the uncapped n/V curve has no value at V = 0 */
  { ST.view='ledger'; BK=makeBeaker('drinkMix',0.5,0.6);
    const G=ledgerModel();
    let gaps=0, bad2='';
    const cs=soluteById('drinkMix').cSat;
    let capped=0;
    for(let i=0;i<G.vs.length;i++){
      if(G.vs[i]>0){
        if(!isFinite(G.C[i])||!isFinite(G.raw[i])) bad2='finite V with a gap at '+G.vs[i];
        /* the drawn curve IS the meter's reading: capped at Csat, with the uncapped n/V
           beside it.  Only the cap tells the two apart, so assert it. */
        if(Math.abs(G.C[i]-Math.min(cs,G.raw[i]))>1e-15) bad2='uncapped C at V = '+G.vs[i];
        if(G.C[i]>cs+1e-15) bad2='C past Csat at V = '+G.vs[i];
        if(G.raw[i]>cs+1e-9) capped++;
      }
      else { gaps++; if(isFinite(G.raw[i])) bad2='V = 0 with a value'; }
    }
    ok(capped>0,'the two branches part company somewhere on the drawn curve ('
       +capped+' samples past Csat)');
    eq(gaps,1,'the evaporation curve has exactly one sample at V = 0');
    ok(!bad2,'and that is the only place either branch is non-finite'+(bad2?' ('+bad2+')':''));
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }

  /* ---------- H. the canvas: nothing off it, nothing on top of anything ---------- */
  { const SIZES=[[1400,820],[1100,700],[900,560],[700,470],[560,380]];
    let off=0, hit=0, ent='', firstOff='', firstHit='';
    for(const [W,H] of SIZES){
      for(const [v] of TABS){
        ST.view=v;
        BK=makeBeaker(ST.solute,1.4,0.6);
        const rc=makeShot(W,H);
        drawView(rc,W,H,buildModel());
        const texts=rc.ops.filter(o=>o.op==='text');
        for(const t of texts){
          if(entRe.test(t.t)){ if(!ent) ent=v+' "'+t.t+'"'; }
          if(/NaN|undefined|Infinity/.test(t.t)){ if(!ent) ent=v+' NaN "'+t.t+'"'; }
          if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){
            off++; if(!firstOff) firstOff=v+' '+W+'x'+H+' "'+t.t+'"'; }
        }
        for(let i=0;i<texts.length;i++) for(let j=i+1;j<texts.length;j++){
          const a=texts[i].bb, b=texts[j].bb;
          if(a[0]<b[2]-0.5&&a[2]>b[0]+0.5&&a[1]<b[3]-0.5&&a[3]>b[1]+0.5){
            hit++; if(!firstHit) firstHit=v+' '+W+'x'+H+' "'+texts[i].t+'" / "'+texts[j].t+'"'; }
        }
      }
    }
    ok(!ent,'no entity, tag, NaN or undefined reaches a canvas text op'+(ent?' ('+ent+')':''));
    ok(off===0,off+' text boxes off the canvas'+(firstOff?' (first: '+firstOff+')':''));
    ok(hit===0,hit+' text collisions'+(firstHit?' (first: '+firstHit+')':''));
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }
  /* every view draws something, and the bottom-left corner stays clear of the HTML hint */
  { let thin='';
    for(const [v] of TABS){
      ST.view=v;
      BK=makeBeaker(ST.solute,1.4,0.6);
      const rc=makeShot(1400,820);
      drawView(rc,1400,820,buildModel());
      if(rc.ops.length<40&&!thin) thin=v+' ('+rc.ops.length+' ops)';
      for(const o of rc.ops) if(o.op==='text'&&o.bb[3]>820-HINT_H&&o.bb[0]<420&&!thin)
        thin=v+' writes into the hint\'s corner: "'+o.t+'"';
    }
    ok(!thin,'every view draws a picture and keeps the hint\'s corner clear'+(thin?' ('+thin+')':''));
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }

  /* ---------- I. the readout prints the numbers it computed ---------- */
  { Object.assign(ST,DEFAULTS);
    ST.view='beaker'; ST.solute='copperSulfate';
    BK=makeBeaker('copperSulfate',2,1);
    const ro=readoutHTML(buildModel());
    ok(ro.indexOf('Saturated!')>=0,'a saturated beaker says so in the readout');
    ok(ro.indexOf(fmt(bkPrecip(BK),3))>=0,'and prints the moles of solid it computed');
    ok(ro.indexOf(fmt(bkConc(BK),PHET.DEC_CONC))>=0,'and the concentration');
    PROBE.y=1.2;
    ok(readoutHTML(buildModel()).indexOf('probe is out')>=0,
       'lifted out of the solution the meter says so rather than printing a number');
    PROBE.y=PROBE0.y;
    if(SHOW_BEERS){
      ST.view='cuvette'; ST.blSolution='potassiumPermanganate'; ST.blConc=4e-4;
      ST.cuvette=1.5; ST.lightMode='preset'; ST.lightOn=true; DET.x=DET0.x; DET.y=0;
      const M=cuvetteModel();
      const r2=readoutHTML(buildModel());
      ok(r2.indexOf(fmt(M.A,PHET.DEC_A))>=0,'the cuvette readout prints the absorbance it computed');
      ok(r2.indexOf(fmt(100*M.T,PHET.DEC_T))>=0,'and the transmittance');
      ST.lightOn=false;
      ok(readoutHTML(buildModel()).indexOf('the light is off')>=0,'with the light off it says so');
      ST.lightOn=true; DET.y=2;
      ok(readoutHTML(buildModel()).indexOf('out of the beam')>=0,
         'and with the probe out of the beam it says that instead');
      DET.y=0;
    }
    Object.assign(ST,DEFAULTS); PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; DET.x=DET0.x; DET.y=DET0.y;
    BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }
  /* the detector's own gate */
  if(SHOW_BEERS){
    ST.lightOn=true; DET.x=3.4; DET.y=0;
    ok(detectorInBeam(),'the probe on the axis is in the beam');
    close(BEAM_HALF,R('DETECTOR beamHalf sensorHalf cutoff',0),1e-18,
          'PhET\'s beam is 0.45 cm across (PhET lensDiameter)');
    close(SENSOR_HALF,R('DETECTOR beamHalf sensorHalf cutoff',1),1e-18,
          'and its sensor 1 cm (PhET sensorDiameter)');
    /* 0.25 and 0.30 cm straddle the cutoff; 0.4 does not distinguish the two halves */
    DET.y=0.25; ok(detectorInBeam(),'a quarter of a millimetre off the axis is still in it');
    DET.y=0.30; ok(!detectorInBeam(),'three tenths is not');
    DET.y=0.4;
    ok(!detectorInBeam(),'lifted 4 mm it is not: the sensor no longer spans the beam');
    DET.y=0; ST.lightOn=false;
    ok(!detectorInBeam(),'and with the light off nothing is in any beam');
    ST.lightOn=true; DET.x=-0.2;
    ok(!detectorInBeam(),'nor behind the source');
    DET.x=DET0.x; DET.y=DET0.y;
    /* the cuvette's snap */
    ST.snap=true;
    close(snapCuvette(1.234),1.2,1e-12,'the cuvette snaps to 0.1 cm (PhET cuvetteSnapInterval)');
    close(snapCuvette(1.26),1.3,1e-12,'rounding to the nearest tenth');
    close(snapCuvette(9),PHET.CUVETTE_MAX,1e-12,'and clamps at 2 cm');
    close(snapCuvette(0.01),PHET.CUVETTE_MIN,1e-12,'and at 0.5 cm');
    ST.snap=false;
    close(snapCuvette(1.234),1.234,1e-12,'with snapping off the width is left alone');
    ST.snap=DEFAULTS.snap;
    /* the preset wavelength tracks the solution */
    setBlSolution('potassiumPermanganate');
    eq(activeWavelength(),lambdaMaxOf('potassiumPermanganate'),
       'the preset light sits at the solution\'s own lambda_max');
    eq(ST.blConc,blsById('potassiumPermanganate').cDefault,
       'and the concentration resets to that solution\'s default (PhET)');
    ST.lightMode='variable'; ST.wavelength=400;
    eq(activeWavelength(),400,'in variable mode the wavelength is whatever it is set to');
    setBlSolution('drinkMix');
    eq(activeWavelength(),400,'and changing the solution does not move it');
    ST.lightMode='preset';
    eq(activeWavelength(),lambdaMaxOf('drinkMix'),'switching back returns it to the peak');
    Object.assign(ST,DEFAULTS);
  }
  /* changing the solute empties the beaker, as PhET's does */
  { BK=makeBeaker('drinkMix',3,0.8);
    setSoluteId('copperSulfate');
    eq(BK.n,0,'changing the solute empties the solute (PhET)');
    close(BK.V,0.8,1e-15,'but leaves the water');
    eq(BK.solute,'copperSulfate','and the beaker knows which solute it now holds');
    Object.assign(ST,DEFAULTS); BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT); }

  /* ---------- J. the canvas prose and the shared helpers ---------- */
  { const PROSE=[['CAP_BEAKER',CAP_BEAKER],['CAP_BEAKER_S',CAP_BEAKER_S],
                 ['CAP_LEDGER',CAP_LEDGER],['CAP_LEDGER_S',CAP_LEDGER_S],
                 ['CAP_COLOUR',CAP_COLOUR],['CAP_COLOUR_S',CAP_COLOUR_S]].concat(
      typeof CAP_CUVETTE==='undefined'?[]:[['CAP_CUVETTE',CAP_CUVETTE],['CAP_CUVETTE_S',CAP_CUVETTE_S],
        ['CAP_SPEC',CAP_SPEC],['CAP_SPEC_S',CAP_SPEC_S],['CAP_LAW',CAP_LAW],['CAP_LAW_S',CAP_LAW_S]]).concat(
      typeof CAP_SOLUTES==='undefined'?[]:[['CAP_SOLUTES',CAP_SOLUTES],['CAP_SOLUTES_S',CAP_SOLUTES_S]]);
    for(const [nm,t] of PROSE){
      ok(!/<su[bp]>/.test(t),nm+' carries no <sub>/<sup>: plain() strips them silently');
      ok(plain(t).indexOf('&')<0,nm+' decodes to literal glyphs');
      ok(plain(t).indexOf('<')<0,nm+' has no tags left after plain()');
      ok(t.length>80,nm+' says something'); } }
  { for(const [k] of TABS){
      ok((INFO[k]||'').length>300,'INFO['+k+'] is a paragraph');
      ok((DERIV[k]||'').length>200,'DERIV['+k+'] carries its derivation'); } }
  { eq(plain('&radic;K<sub>w</sub> &minus; x'),'√Kw − x','plain() decodes and strips');
    eq(plain('&#955;'),'λ','and numeric entities');
    eq(fmt(4.58236,2),'4.58','fmt to two places');
    eq(sciPlain(1.5848931924611141e-6,3),'1.585e-6','sciPlain for the canvas');
    eq(sciPlain(0),'0','and zero');
    eq(sciPlain(null),'—','and a missing value');
    eq(sci(null),'&mdash;','sci for the readout');
    ok(/^rgb\(\d+,\d+,\d+\)$/.test(mix(COL.pos,COL.ref,0.5)),'mix is well formed');
    eq(toRgb(shade(COL.pos,0)).join(),toRgb('#070b18').join(),'shade(col,0) is the page background');
    eq(rgbCss([1,2,3]),'rgb(1,2,3)','rgbCss');
    ok(ticksFor(0,780,6).length>=5,'ticksFor gives a full set on a sane range');
    eq(logTicks(0,10).length,0,'logTicks refuses a non-positive bound rather than looping'); }
  /* the house 2-D layer's own fixes, asserted so they cannot rot out from under this file */
  { const rc=makeShot(400,300), b=box(50,50,300,200);
    POLY_SEGS=[];
    polyline(rc,b,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4,'polyline clips a segment whose BOTH ends are outside the box');
    close(POLY_SEGS[0],b.x,0.5,'and interpolates the crossing to the left edge');
    close(POLY_SEGS[2],b.x1,0.5,'and to the right edge'); }

  Object.assign(ST,stSave); BK=bkSave;
  PROBE.x=pxS; PROBE.y=pyS; DET.x=dxS; DET.y=dyS;
  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
