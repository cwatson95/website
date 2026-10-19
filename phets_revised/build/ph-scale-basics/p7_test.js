
/* ================================================================== *
 *  selfTest — headless verification.  Every reference is a line of     *
 *  build/ph-scale/refvals.txt (derive.py's output, read in full):      *
 *  (python) = 50-digit decimal or exact arithmetic in the twin,        *
 *  (scipy)  = a brentq root of the charge balance,                     *
 *  (PhET)   = a constant read out of the minified original 1.7.5.      *
 *  The chemistry is the same engine as ph-scale.html, so it is         *
 *  asserted here too: this file has to stand on its own.               *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),
    name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  function ref(label,i){
    const v=REF[label];
    if(!v) throw new Error('no reference line "'+label+'"');
    return v[i||0];
  }
  const stSave=Object.assign({},ST), pxSave=PROBE.x, pySave=PROBE.y;
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;

  /* ---------- A. this build IS the Basics sim ---------- */
  eq(SIMID,'ph-scale-basics','the file knows which sim it is');
  eq(SIM_VER,'1.7.5','and which version of the original it was built against (PhET)');
  eq(TABS.length,4,'four views: PhET"s one screen and three analyses');
  eq(TABS.map(t=>t[0]).join(),'beaker,liquids,dilution,scale','in that order');
  eq(SHOW_CONC,false,'PhET"s Basics prints no concentrations, and neither does this readout');
  { Object.assign(ST,DEFAULTS);
    const ro=readoutHTML(buildModel());
    ok(ro.indexOf('mol/L')<0,'the beaker readout carries no concentration');
    ok(ro.indexOf('molecules')<0,'no molecule count');
    ok(ro.indexOf('moles')<0,'and no moles');
    ok(ro.indexOf('pH')>=0&&ro.indexOf('total volume')>=0,'a pH and a volume, as PhET does');
    ok(ro.indexOf('exact, re-solved')>=0&&ro.indexOf('PhET&rsquo;s rule')>=0,
       'and both dilution laws, which is this remake"s own addition');
    ST.view='scale';
    const rs=readoutHTML(buildModel());
    ok(rs.indexOf('mol/L')>=0||rs.indexOf('&times; 10<sup>')>=0,
       'while the scale view DOES print them, because they are its subject');
    Object.assign(ST,stSave); }

  /* ---------- B. PhET's constants, read from the minified original ---------- */
  eq(PHET.BEAKER_VOLUME,1.2,'the beaker holds 1.2 L (PhET BEAKER_VOLUME)');
  eq(PHET.MIN_SOLUTION_VOLUME,0.015,'and at least 0.015 L (PhET)');
  eq(PHET.PH_MIN,-1,'the pH range starts at -1 (PhET PH_RANGE)');
  eq(PHET.PH_MAX,15,'and ends at 15 (PhET)');
  eq(PHET.PH_DECIMALS,2,'the meter prints two decimals (PhET)');
  eq(PHET.DROPPER_FLOW,0.05,'the dropper runs at 0.05 L/s (PhET)');
  eq(PHET.FAUCET_FLOW,0.25,'the faucets at 0.25 L/s (PhET)');
  eq(PHET.AUTOFILL_VOLUME,0.5,'autofill puts in 0.5 L (PhET)');
  eq(PHET.AUTOFILL_FLOW,0.45,'at 0.45 L/s (PhET)');
  eq(PHET.WATER_CONC,55,'water is 55 mol/L (PhET Water.concentration)');
  eq(PHET.WATER_PH,7,'and pH 7 (PhET Water.pH)');
  eq(PHET.COLOR_STOP_RATIO,0.25,'the colour stop sits at a quarter (PhET)');
  eq(NA_PHET,6.023e23,'PhET"s Avogadro number is 6.023e23 (PhET)');
  eq(SOLUTES.length,12,'twelve liquids (PhET)');
  eq(SOLUTES.map(s=>s.pH).join(),REF['SOLUTE pH values'].join(),
     'and their pH values are PhET"s (python)');
  eq(soluteById('drainCleaner').pH,13,'drain cleaner is pH 13 (PhET)');
  eq(soluteById('batteryAcid').pH,1,'battery acid pH 1 (PhET)');
  eq(soluteById('chickenSoup').pH,5.8,'chicken soup pH 5.8 (PhET)');
  eq(soluteById('water').stock.join(),WATER_RGB.join(),'and water is PhET"s own colour (PhET)');
  { const got=[], want=REF['MEASURED blood oj milk soup lo hi'];
    for(const id of ['blood','orangeJuice','milk','chickenSoup']){
      const s=soluteById(id); got.push(s.range[0],s.range[1]);
      ok(s.pH>=s.range[0]-1e-12&&s.pH<=s.range[1]+1e-12,
         'PhET"s '+s.name+' lies inside its sourced measured range'); }
    eq(got.join(),want.join(),'the four sourced ranges match derive.py (python)');
    eq(SOLUTES.filter(s=>s.range).length,4,'and only four of the twelve carry one');
    for(const s of SOLUTES) ok(!s.range||!!s.src,'a range without a source would be an invention: '+s.name); }
  close(PHET.AUTOFILL_VOLUME/PHET.AUTOFILL_FLOW,
        ref('FLOW autofill seconds, dropper seconds to fill, faucet seconds to fill'),1e-15,
        'autofill takes 1.111 s (python)');

  /* ---------- C. the two concentrations ---------- */
  eq(KW,1e-14,'Kw is 1e-14 at 25 C by convention');
  eq(PKW,14,'so pKw is 14.000 exactly, and neutral is pH 7.000');
  eq(NA,6.02214076e23,'N_A is the exact SI 2019 value');
  for(const [lbl,ph] of [['CONC at pH -1',-1],['CONC at pH 0',0],['CONC at pH 1',1],
                         ['CONC at pH 7',7],['CONC at pH 13',13],['CONC at pH 14',14],
                         ['CONC at pH 15',15]]){
    rel(concH3O(ph),ref(lbl),1e-15,'[H3O+] at pH '+ph+' (python)');
    rel(concOH(ph),ref(lbl,1),1e-15,'[OH-] at pH '+ph+' (python)');
  }
  rel(concH3O(5.8),ref('CONC at pH 5.8 7.4 2.5'),1e-15,'[H3O+] at pH 5.8, not a round exponent (python)');
  rel(concOH(5.8),ref('CONC at pH 5.8 7.4 2.5',1),1e-15,'[OH-] at pH 5.8 (python)');
  { let worst=0, worstPhet=0;
    for(let i=0;i<=320;i++){ const ph=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/320;
      worst=Math.max(worst,Math.abs(concH3O(ph)*concOH(ph)-KW)/KW);
      worstPhet=Math.max(worstPhet,Math.abs(concOHPhet(ph)-concOH(ph))/concOH(ph)); }
    ok(worst<3e-16,'[H3O+][OH-] = Kw to 3e-16 over the whole scale ['+worst.toExponential(2)+']');
    ok(worstPhet>5*3e-16,'and PhET"s 10^-(14-pH) spelling is measurably worse ['
       +worstPhet.toExponential(2)+'] — the reason concOH divides');
    rel(worstPhet,ref('CONC worst rel err h3o oh, identity h*o=Kw, PhET spelling of OH',3),
        0.35,'the size of that gap (python)'); }
  for(let i=0;i<SOLUTES.length;i++){
    rel(concH3O(SOLUTES[i].pH),REF['LIQUID h3o'][i],1e-15,SOLUTES[i].name+' [H3O+] (python)');
    rel(concOH(SOLUTES[i].pH),REF['LIQUID oh'][i],1e-15,SOLUTES[i].name+' [OH-] (python)');
    rel(moleculesOf(concH3O(SOLUTES[i].pH),PHET.BEAKER_VOLUME),
        REF['LIQUID molecules h3o in 1.2 L'][i],1e-14,SOLUTES[i].name+' H3O+ per beaker (python)');
  }
  rel(moleculesOf(concH3O(7),1.2),ref('COUNT pH7 1.2L moles molecules si phet',1),1e-14,
      'a neutral beaker holds 7.23e16 hydronium ions (python)');

  /* ---------- C2. what this build carries but never draws ----------
     The chemistry file is the SAME one ph-scale uses, so this build contains PhET's
     particle rule, its graph ranges and the other two inverses whether or not a view of
     its own shows them.  Code that ships is code that gets asserted: without this block a
     mutation sweep finds seventeen live mutants inside a file that calls itself verified,
     and every one of them is real — the constants are in the bundle a reader downloads. */
  { const d=REF['DOTS at pH 7 6 8 1 13 15 -1'], phs=[7,6,8,1,13,15,-1];
    for(let i=0;i<phs.length;i++){
      const c=dotCounts(phs[i]);
      eq(c.h,d[2*i],'dots of H3O+ at pH '+phs[i]+' (PhET rule, python)');
      eq(c.o,d[2*i+1],'dots of OH- at pH '+phs[i]+' (PhET rule, python)'); }
    eq(dotCounts(7).h,50,'fifty dots each at neutral (PhET)');
    eq(dotCounts(6).o,5,'and the minority is floored at five (PhET)');
    eq(dotCounts(15).o,3000,'the ramp reaches PhET"s 3000 at pH 15 (PhET)');
    const c13=dotCounts(13);
    rel(c13.o/c13.h,ref('DOTS drawn vs true ratio at pH 13'),1e-12,
        'and the drawn ratio at pH 13 is 457.2 : 1 (python)');
    rel(concOH(13)/concH3O(13),ref('DOTS drawn vs true ratio at pH 13',1),1e-12,
        'against a true 1e12 : 1 (python)'); }
  eq(PHET.LOG_EXP_MIN,-16,'the log graph would start at 1e-16 (PhET)');
  eq(PHET.LOG_EXP_MAX,2,'and end at 1e2 (PhET)');
  close(PHET.LOG_EXP_MAX-PHET.LOG_EXP_MIN,ref('GRAPH log decades, linear top'),1e-12,
        'eighteen decades (python)');
  eq(PHET.LIN_MANTISSA_MAX,8,'with a mantissa to 8 (PhET)');
  eq(PHET.LIN_EXP_MIN,-14,'and an exponent from -14 (PhET)');
  eq(PHET.MY_VOL_MIN,0.01,'My Solution would go down to 0.01 L (PhET)');
  eq(PHET.MY_VOL_DEFAULT,0.5,'and start at 0.5 L (PhET)');
  eq(soluteById('nonsense').id,'orangeJuice','an unknown id falls back rather than throwing');
  { let worst=0;
    for(let i=0;i<=160;i++){ const ph=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/160;
      worst=Math.max(worst,Math.abs(phFromH3O(concH3O(ph))-ph),
                           Math.abs(phFromOH(concOH(ph))-ph)); }
    ok(worst<1e-12,'pH -> concentration -> pH round-trips both ways ['+worst.toExponential(2)+']'); }
  eq(phFromH3O(0),null,'a zero concentration has no pH, and says so rather than -Infinity');
  eq(phFromH3O(null),null,'and neither does a missing one');
  rel(molesOf(concH3O(7),1.2),ref('COUNT pH7 1.2L moles molecules si phet'),1e-15,
      'moles of H3O+ in 1.2 L of neutral water (python)');
  rel(molesOf(PHET.WATER_CONC,1.2),ref('COUNT water 55 molar in 1.2L'),1e-15,
      'and 66 moles of water around them (python)');
  rel(moleculesOf(concH3O(7),1.2,NA_PHET),ref('COUNT pH7 1.2L moles molecules si phet',2),1e-14,
      'PhET"s N_A gives a different last four digits (python)');

  /* ---------- D. the net strong acid, and the two stable branches ---------- */
  { const c=REF['NET C at pH 1 7 13 14'];
    rel(netAcid(1),c[0],1e-15,'C at pH 1 (python)');
    eq(netAcid(7),0,'C is exactly zero at pH 7');
    rel(netAcid(13),c[2],1e-15,'C at pH 13 (python)');
    ok(netAcid(3)>0&&netAcid(11)<0,'positive for an acid, negative for a base'); }
  { const bad=Math.abs(netAcidNaive(6.999999)-netAcid(6.999999))/Math.abs(netAcid(6.999999));
    rel(bad,ref('NET naive rel err at pH 6.999999'),0.5,
        'the plain difference loses 11 digits at pH 6.999999 (python)');
    ok(bad>1e-12,'which is a thousand times the sinh form"s own error');
    ok(Math.abs(netAcidNaive(6.99)-netAcid(6.99))/Math.abs(netAcid(6.99))<1e-14,
       'at 0.01 from neutral it is still fine'); }
  { let worst=0;
    for(let i=0;i<=140;i++){ const ph=i*0.1;
      worst=Math.max(worst,Math.abs(netAcid(PKW-ph)+netAcid(ph))/Math.max(1e-300,Math.abs(netAcid(ph)))); }
    ok(worst<1e-14,'C(14-pH) = -C(pH) exactly ['+worst.toExponential(2)+']'); }
  { let worst=0, worstRt=0;
    for(let i=0;i<=160;i++){ const ph=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/160;
      const c=netAcid(ph);
      worst=Math.max(worst,Math.abs(phFromNet(c)-phFromNetAsinh(c)));
      worstRt=Math.max(worstRt,Math.abs(phFromNet(c)-ph)); }
    ok(worst<1e-11,'the quadratic root and the asinh closed form agree ['+worst.toExponential(2)+']');
    ok(worstRt<1e-12,'and pH -> C -> pH round-trips ['+worstRt.toExponential(2)+']'); }
  for(const [ph,lbl] of [[13,'NET naive root rel err at pH 13'],
                         [14,'NET naive root rel err at pH 14'],
                         [15,'NET naive root rel err at pH 15']]){
    const c=netAcid(ph), bad=Math.abs(h3oFromNetNaive(c)-concH3O(ph))/concH3O(ph);
    rel(bad,ref(lbl),0.02,'the textbook quadratic root is out by '+ref(lbl).toExponential(1)
        +' at pH '+ph+' (python)');
    rel(h3oFromNet(c),concH3O(ph),1e-12,'while the rationalised branch is exact at pH '+ph);
  }
  ok(Math.abs(h3oFromNetNaive(netAcid(15))-concH3O(15))/concH3O(15)>0.1,
     'the naive root is STILL 11 % wrong at pH 15, so this branch cannot be deleted');
  { let worst=0;
    for(let i=0;i<=160;i++){ const ph=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/160;
      const c=netAcid(ph), h=h3oFromNet(c);
      worst=Math.max(worst,Math.abs(h-KW/h-c)/Math.max(Math.abs(c),SQRTKW)); }
    ok(worst<1e-11,'and every root satisfies h - Kw/h = C ['+worst.toExponential(2)+']'); }

  /* ---------- E. the mixing laws ---------- */
  for(const [ph,lbl] of [[1,'MIX pH 1, 0.1 L + 1.1 L water: exact phet avg'],
                         [5,'MIX pH 5, 0.1 L + 1.1 L water: exact phet avg'],
                         [6.5,'MIX pH 6.5, 0.1 L + 1.1 L water: exact phet avg'],
                         [7.4,'MIX pH 7.4, 0.1 L + 1.1 L water: exact phet avg'],
                         [10,'MIX pH 10, 0.1 L + 1.1 L water: exact phet avg'],
                         [13,'MIX pH 13, 0.1 L + 1.1 L water: exact phet avg']]){
    rel(mixExact(ph,0.1,PHET.WATER_PH,1.1),ref(lbl),1e-12,
        'pH '+ph+' diluted twelvefold, exact (python + scipy)');
    rel(mixPhet(ph,0.1,1.1),ref(lbl,1),1e-12,'the same by PhET"s rule (python)');
    rel(mixAverage(ph,0.1,PHET.WATER_PH,1.1),ref(lbl,2),1e-12,'and by averaging the pH (python)');
  }
  for(const ph of [1,5,7,10,13]){
    eq(mixExact(ph,0.5,PHET.WATER_PH,0),ph,'no water added leaves pH '+ph+' exactly');
    eq(mixPhet(ph,0.5,0),ph,'and so does PhET"s rule');
  }
  eq(mixExact(3,0,PHET.WATER_PH,1),7,'no solute is pH 7 exactly');
  eq(mixExact(3,0,PHET.WATER_PH,0),null,'an empty beaker has no pH at all');
  { let worst=0;
    for(const ph of [1,3.5,6.9,7.1,10,13]) for(const f of [2,10,1000,1e6]){
      const got=mixNet(ph,1,PHET.WATER_PH,f-1), want=netAcid(ph)/f;
      worst=Math.max(worst,Math.abs(got-want)/Math.abs(want)); }
    ok(worst<1e-14,'diluting f-fold divides C by exactly f ['+worst.toExponential(2)+']'); }
  { let worst=0, argPh=0, argV=0;
    for(let i=0;i<=320;i++){ const ph=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/320;
      for(let j=1;j<=80;j++){ const v1=0.015*j; if(v1>PHET.BEAKER_VOLUME) break;
        const d=Math.abs(mixExact(ph,v1,PHET.WATER_PH,PHET.BEAKER_VOLUME-v1)
                        -mixPhet(ph,v1,PHET.BEAKER_VOLUME-v1));
        if(d>worst){ worst=d; argPh=ph; argV=v1; } } }
    rel(worst,ref('MIX worst difference anywhere in the beaker, pH, V_solute'),0.02,
        'the two laws never differ by more than 0.0948 pH in this beaker (python)');
    ok(worst>0.05&&worst<0.12,'which is small, real, and worth drawing ['+fmt(worst,5)+' pH]');
    close(argV,0.015,1e-9,'and it happens at the thinnest solution the beaker allows'); }
  { let worst=0;
    for(const ph of [1,2.5,5,5.8,6.5,7,7.4,10,13]) for(const v1 of [0.1,0.3,0.6,1.0,1.2])
      worst=Math.max(worst,Math.abs(mixExact(ph,v1,PHET.WATER_PH,1.2-v1)
                                   -mixAverage(ph,v1,PHET.WATER_PH,1.2-v1)));
    rel(worst,REF['MIX worst |exact - averaged pH|, and where'][0],1e-12,
        'averaging the pH is wrong by 4.42 units at worst (python)');
    ok(worst>1.0,'a different order of wrong from PhET"s rule'); }
  { let worst=0;
    for(let i=1;i<140;i++){ const ph=i*0.1;
      const a=mixExact(ph,0.1,PHET.WATER_PH,1.1)-mixPhet(ph,0.1,1.1);
      const b=mixExact(PKW-ph,0.1,PHET.WATER_PH,1.1)-mixPhet(PKW-ph,0.1,1.1);
      worst=Math.max(worst,Math.abs(a+b)); }
    ok(worst<1e-12,'exact minus PhET is odd about pH 7 ['+worst.toExponential(2)+']'); }
  { close(mixExact(2,0.5,12,0.5),7,1e-12,'equal volumes of pH 2 and pH 12 are exactly neutral (python)');
    rel(mixExact(2,0.5,11,0.5),REF['MIX acid+base 0.5L pH2+pH12, pH2+pH11, pH1+pH13'][1],1e-12,
        'pH 2 with pH 11 stays acidic at 2.3468 (python)'); }
  /* the one number the liquids table is built on */
  close(Math.log10(12),1.0791812460476249,1e-12,'a twelvefold dilution is 1.079 pH, well away from neutral');
  /* NOT a 17-digit constant typed from the head — that one was wrong in its fourth digit
     and the suite caught it (Known-bad: a reference value you computed in your head is
     not a reference value).  What the prose claims is what the sim PRINTS, so that is
     what is asserted, alongside the two independent implementations agreeing. */
  { const v=mixExact(3.5,0.1,PHET.WATER_PH,1.1);
    eq(phPlain(v),'4.58','orange juice poured to 0.1 L and filled to the brim reads 4.58');
    rel(v,phFromNetAsinh(mixNet(3.5,0.1,PHET.WATER_PH,1.1)),1e-12,
        'by the asinh closed form as well as by the quadratic root');
    close(v-3.5,Math.log10(12),0.001,
          'and it is log10(12) above the stock pH, because 3.5 is far from neutral'); }

  /* ---------- F. PhET's colour law ---------- */
  { const c=REF['COLOR coffee at 0 0.25 1'], cf=soluteById('coffee');
    for(const [r,i] of [[0,0],[0.25,3],[1,6]]){
      const g=soluteRGB(cf,r);
      for(let k=0;k<3;k++) close(g[k],c[i+k],1e-9,'coffee colour at r = '+r+', channel '+k+' (python)'); }
    /* at r = 0.5 lerp(water, stock, r) and lerp(stock, water, r) AGREE, so a no-stop
       colour tested only there is tested by nothing (the ph-scale sweep proved it) */
    const mr=REF['COLOR milk (no stop) at 0.25 0.5 0.75'];
    [0.25,0.5,0.75].forEach((r,i)=>{
      const mk=soluteRGB(soluteById('milk'),r);
      for(let k=0;k<3;k++) close(mk[k],mr[3*i+k],1e-9,
        'milk has no colour stop, r = '+r+', channel '+k+' (python)'); });
    eq(rgbCss(soluteRGB(cf,1)),'rgb(164,99,7)','an undiluted solute is its stock colour');
    eq(rgbCss(soluteRGB(cf,0)),rgbCss(WATER_RGB),'and a vanishing one is water'); }

  /* ---------- G. the beaker, as a machine ---------- */
  { Object.assign(ST,DEFAULTS);
    eq(vTotal(),PHET.AUTOFILL_VOLUME,'the beaker starts with PhET"s autofill volume');
    eq(soluteRatio(),1,'all of it the liquid');
    let worst=0;
    for(let i=0;i<=24;i++) for(let j=0;j<=24;j++){
      setSolute(i*0.05); setWater(j*0.05);
      worst=Math.max(worst,vTotal()-PHET.BEAKER_VOLUME);
      ok(ST.vSolute>=-1e-12&&ST.vWater>=-1e-12,'no negative volume at ('+i+','+j+')'); }
    ok(worst<=1e-12,'no slider pair puts more than 1.2 L in the beaker ['+worst.toExponential(2)+']');
    setSolute(1.2); eq(ST.vWater,0,'filling with liquid empties the water');
    setWater(1.2); eq(ST.vSolute,0,'and the other way round');
    Object.assign(ST,DEFAULTS); ST.vSolute=0.3; ST.vWater=0.6; ST.drain=true; ST.running=true;
    const before=beakerPH(), rBefore=soluteRatio();
    for(let k=0;k<30;k++) stepFrame();
    close(beakerPH(),before,1e-12,'draining does not change the pH: it removes solution, not solute');
    close(soluteRatio(),rBefore,1e-12,'and leaves the mixture"s ratio alone');
    ok(vTotal()<0.9,'while emptying it ['+fmt(vTotal(),3)+' L]');
    Object.assign(ST,DEFAULTS); emptyBeaker(); ST.pourSolute=true; ST.running=true;
    for(let k=0;k<60;k++) stepFrame();
    close(ST.vSolute,PHET.DROPPER_FLOW,1e-12,'one second of the dropper is 0.05 L (PhET)');
    ST.pourWater=true;
    for(let k=0;k<60;k++) stepFrame();
    close(ST.vWater,PHET.FAUCET_FLOW,1e-12,'one second of the faucet is 0.25 L (PhET)');
    for(let k=0;k<6000;k++) stepFrame();
    close(vTotal(),PHET.BEAKER_VOLUME,1e-12,'and both stop at the brim');
    ok(stepFrame()===false,'after which the frame reports that nothing moved');
    ST.running=false; const held=vTotal();
    ST.pourWater=true; for(let k=0;k<60;k++) stepFrame();
    eq(vTotal(),held,'and a paused clock pours nothing');
    Object.assign(ST,DEFAULTS); emptyBeaker(); ST.running=true; ST.drain=true;
    for(let k=0;k<6000;k++) stepFrame();
    eq(vTotal(),0,'an empty beaker drains to exactly nothing, never below');
    eq(beakerPH(),null,'and an empty beaker has no pH');
    autofill(); eq(vTotal(),PHET.AUTOFILL_VOLUME,'autofill puts PhET"s 0.5 L back');
    eq(ST.vWater,0,'of the LIQUID alone, not of water'); }
  { Object.assign(ST,DEFAULTS); PROBE.x=0.62; PROBE.y=0.16;
    ok(probeInLiquid(),'the probe starts in the liquid');
    PROBE.y=0.9; ok(!probeInLiquid(),'lifted above the surface it reads nothing');
    PROBE.y=0.16; PROBE.x=-0.1; ok(!probeInLiquid(),'and outside the wall it reads nothing');
    PROBE.x=0.10; ok(probeInLiquid(),'a tenth of the way in is still in the liquid');
    PROBE.x=PROBE_WALL*0.5; ok(!probeInLiquid(),'half the wall margin in is not');
    PROBE.x=0.62; emptyBeaker(); ok(!probeInLiquid(),'nor in an empty beaker');
    autofill(); ok(probeInLiquid(),'and it reads again when the beaker is refilled'); }
  { Object.assign(ST,DEFAULTS); ST.solute='chickenSoup'; ST.vSolute=0.1; ST.vWater=1.1;
    ST.law='exact';
    const e=beakerIons();
    rel(e.ph,mixExact(5.8,0.1,PHET.WATER_PH,1.1),1e-15,'the model uses the exact law when asked');
    rel(e.h*e.o,KW,3e-16,'and its two ions still multiply to Kw');
    rel(e.h,h3oFromNet(e.c),1e-15,'because both come from C, not from the printed pH');
    { let bad=0, n=0;
      const sv=Object.assign({},ST);
      for(const sol of SOLUTES) for(let i=1;i<=80;i++){
        const v1=0.015*i; if(v1>PHET.BEAKER_VOLUME) break;
        for(const v2 of [0,0.05,0.2,0.6,PHET.BEAKER_VOLUME-v1]){
          if(v2<0||v1+v2>PHET.BEAKER_VOLUME+1e-12) continue;
          ST.solute=sol.id; ST.vSolute=v1; ST.vWater=v2; ST.law='exact';
          const io2=beakerIons(); if(!io2) continue;
          n++; if(io2.o!==KW/io2.h) bad++;
        } }
      Object.assign(ST,sv);
      ok(bad===0&&n>4000,'the hydroxide is Kw over the solved hydronium, bit for bit, at all '
         +n+' reachable states ('+bad+' bad)'); }
    ST.law='phet';
    const p=beakerIons();
    rel(p.ph,mixPhet(5.8,0.1,1.1),1e-15,'and PhET"s rule when asked for that');
    ok(Math.abs(e.ph-p.ph)>0.05,'the two differ by more than a twentieth of a unit here');
    ST.law='exact'; }
  { eq(phClass(7),'neutral','pH 7 is neutral');
    eq(phClass(7.004),'neutral','and so is anything the meter prints as 7.00 (PhET rounding)');
    eq(phClass(7.006),'basic','while 7.01 is basic');
    eq(phClass(6.994),'acidic','and 6.99 acidic');
    eq(phClass(null),'empty','an empty beaker is neither'); }
  { /* the dilution view's envelope IS derive.py's headline number */
    Object.assign(ST,DEFAULTS); ST.view='dilution';
    const D=buildModel().D;
    close(D.fReach,80,1e-12,'the envelope sweeps every dilution the beaker can hold, 80-fold');
    rel(D.worst,ref('MIX worst difference anywhere in the beaker, pH, V_solute'),0.02,
        'and its peak is the 0.0948 pH derive.py measured (python)');
    close(D.worstPh,ref('MIX worst difference anywhere in the beaker, pH, V_solute',1),0.12,
          'at the stock pH derive.py found, 4.91 (python)');
    close(D.hereDiff,0,1e-15,'and the undiluted beaker sits at exactly zero');
    Object.assign(ST,stSave); }

  /* ---------- H. every view builds clean, at four sizes ---------- */
  const SIZES=[[1400,820],[1100,700],[820,560],[560,380]];
  const CONFIGS=[
    {view:'beaker'},
    {view:'beaker',solute:'drainCleaner',vSolute:0.1,vWater:1.1},
    {view:'beaker',solute:'batteryAcid',vSolute:1.2,vWater:0},
    {view:'beaker',solute:'water',vSolute:0.02,vWater:0},
    {view:'beaker',vSolute:0,vWater:0},
    {view:'beaker',vSolute:0,vWater:0.6},
    {view:'beaker',law:'phet',solute:'coffee',vSolute:0.05,vWater:1.15},
    {view:'beaker',pourSolute:true,pourWater:true,drain:true},
    {view:'liquids'},
    {view:'liquids',solute:'drainCleaner'},
    {view:'liquids',solute:'blood'},
    {view:'dilution'},
    {view:'dilution',solute:'drainCleaner'},
    {view:'dilution',solute:'milk',vSolute:0.015,vWater:1.185},
    {view:'dilution',solute:'water'},
    {view:'dilution',vSolute:0,vWater:0},
    {view:'scale'},
    {view:'scale',solute:'blood'}
  ];
  for(const base of CONFIGS){
    Object.assign(ST,DEFAULTS,base);
    PROBE.x=PROBE0.x; PROBE.y=PROBE0.y;
    const nm=JSON.stringify(base);
    for(const [W,H] of SIZES){
      const c=makeShot(W,H);
      let err=null, M=null;
      try{ M=buildModel(); drawView(c,W,H,M); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      const rects=fills.reduce((a,o)=>a+(o.n||1),0), strokes=c.ops.filter(o=>o.op==='stroke').length;
      /* a floor on what the ops CARRY, not on how many there are (Known-bad: an op-count
         floor punishes a view for batching) */
      ok(rects+strokes>=12&&texts.length>=5,
         nm+' '+W+'x'+H+' draws substance ('+rects+' rects, '+strokes+' strokes, '+texts.length+' texts)');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){
          bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const A2=texts[i2].bb,B2=texts[j2].bb;
        const ox=Math.min(A2[2],B2[2])-Math.max(A2[0],B2[0]);
        const oy=Math.min(A2[3],B2[3])-Math.max(A2[1],B2[1]);
        if(ox>0.5&&oy>0.5){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      /* the house #hint is HTML at bottom:11px and the canvas capture cannot see it
         (build/wave-on-a-string/, Known-bad): keep the corner clear */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' nothing under the #hint line'+
         (inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||
           Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
      const ro=readoutHTML(M), eb=eqbarFor(M), tg=tagHTML(M);
      ok(ro.indexOf('NaN')<0&&ro.indexOf('undefined')<0&&ro.indexOf('Infinity')<0,nm+' readout clean');
      ok(eb.indexOf('NaN')<0&&tg.indexOf('NaN')<0&&tg.indexOf('undefined')<0,
         nm+' equation bar and tag clean');
      ok(ro.length>300,nm+' readout has substance ('+ro.length+' chars)');
    }
  }
  Object.assign(ST,stSave); PROBE.x=pxSave; PROBE.y=pySave;

  /* ---------- I. the liquids table prints what it computed ---------- */
  { Object.assign(ST,DEFAULTS); ST.view='liquids';
    const c=makeShot(1400,820);
    drawView(c,1400,820,buildModel());
    const tx=c.ops.filter(o=>o.op==='text').map(o=>o.t);
    for(const s of SOLUTES) ok(tx.indexOf(s.name)>=0,'the table lists '+s.name);
    ok(tx.indexOf('4.58')>=0,'and prints orange juice"s diluted pH, 4.58');
    /* CHICKEN SOUP, not orange juice, pins the two columns: it is the liquid at which the
       two laws part company (6.73 against 6.65), so an orange-juice-only check passes on a
       table whose PhET column has been replaced by the exact one, and on one whose
       dilution has been changed under the exact column alone.  Both survived a spot check
       until this line. */
    ok(tx.indexOf('6.73')>=0,'chicken soup diluted twelvefold, exactly: 6.73');
    ok(tx.indexOf('6.65')>=0,'and by PhET"s rule: 6.65 — the two columns really differ');
    ok(tx.indexOf('7.37–7.43')>=0,'and blood"s sourced range');
    ok(tx.filter(t=>t==='not sourced').length===8,
       'and says "not sourced" for exactly the eight that are not');
    /* the rows are emitted in order, so their order in the display list IS the sort */
    ok(tx.indexOf('battery acid')<tx.indexOf('water')
       &&tx.indexOf('water')<tx.indexOf('drain cleaner'),
       'and the twelve are sorted by pH, acid first');
    Object.assign(ST,stSave); }

  /* ---------- J. the canvas prose and the shared helpers ---------- */
  { const CANVAS_PROSE=[['CAP_BEAKER',CAP_BEAKER],['CAP_BEAKER_S',CAP_BEAKER_S],
      ['CAP_LIQ',CAP_LIQ],['CAP_LIQ_S',CAP_LIQ_S],
      ['CAP_DIL',CAP_DIL],['CAP_DIL_S',CAP_DIL_S],
      ['CAP_SCALE',CAP_SCALE],['CAP_SCALE_S',CAP_SCALE_S]];
    for(const [nm,t] of CANVAS_PROSE){
      ok(!/<su[bp]>/.test(t),nm+' carries no <sub>/<sup>: plain() strips them silently');
      ok(plain(t).indexOf('&')<0,nm+' decodes to literal glyphs');
      ok(plain(t).indexOf('<')<0,nm+' has no tags left after plain()'); } }
  { for(const [k] of TABS){ ok((INFO[k]||'').length>300,'INFO['+k+'] is a paragraph');
      ok((DERIV[k]||'').length>200,'DERIV['+k+'] carries its derivation'); } }
  { eq(plain('&radic;K<sub>w</sub> &minus; x'),'√Kw − x','plain() decodes and strips');
    eq(plain('&#955;'),'λ','and numeric entities');
    eq(fmt(4.58236,2),'4.58','fmt to two places');
    eq(sciPlain(1.5848931924611141e-6,3),'1.585e-6','sciPlain for the canvas');
    eq(phPlain(null),'—','phPlain on an empty beaker');
    eq(volStr(0.5),'0.50 L','volumes carry PhET"s two places');
    ok(/^rgb\(\d+,\d+,\d+\)$/.test(mix(COL.h3o,COL.oh,0.5)),'mix is well formed');
    eq(toRgb(shade(COL.pos,0)).join(),toRgb('#070b18').join(),'shade(col,0) is the page background');
    ok(ticksFor(0,14,6).length>=5,'ticksFor gives a full set on a sane range');
    eq(logTicks(0,10).length,0,'logTicks refuses a non-positive bound rather than looping'); }

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
