
/* ================================================================== *
 *  selfTest — headless verification.  Every reference is a line of     *
 *  build/greenhouse-effect/refvals.txt (derive.py's output, read in    *
 *  full): (scipy) = CODATA through scipy.constants, (python) = numpy   *
 *  or exact arithmetic in the twin, (PhET) = a constant read out of    *
 *  docs/phets/greenhouse-effect_en.html 1.3.13.                        *
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
  const stSave=Object.assign({},ST), probeSave=PROBE.z;

  /* ---------- A. PhET's constants, read from the minified original ---------- */
  eq(GH.SIGMA,5.670374419e-8,'PhET&rsquo;s Stefan-Boltzmann constant (PhET)');
  eq(GH.S_SUN,343.6,'the sun delivers 343.6 W/m^2 (PhET OUTPUT_ENERGY_RATE)');
  eq(GH.INT_MIN,0.5,'solar intensity from 1/2 (PhET)'); eq(GH.INT_MAX,2,'to 2 suns (PhET)');
  eq(GH.ALB_MEADOW,0.2,'green-meadow albedo 0.2 (PhET)');
  eq(GH.ALB_GLACIER,0.225,'partially-glaciated albedo 0.225 (PhET)');
  eq(GH.ALB_LM,0.3,'the layer model starts at albedo 0.3 (PhET)');
  eq(GH.ALB_MAX,0.9,'the albedo slider stops at 0.9 (PhET)');
  eq(GH.TMIN_NIGHT,245,'Earth-at-night floor 245 K (PhET)');
  eq(GH.TMIN_LM,125,'the layer model"s floor 125 K (PhET)');
  eq(GH.TOP,50000,'the atmosphere is 50 km deep (PhET)');
  eq(GH.N_CONC,12,'twelve sheets on the concentration screens (PhET)');
  eq(GH.N_LM,3,'three on the layer model (PhET)');
  eq(GH.ABS_COEF,0.85,'the 0.85 in PhET"s absorbance fit (PhET)');
  eq(GH.SCALE_H,8400,'and its 8400 m scale height (PhET)');
  eq(GH.ABS_MIN,0.1,'absorbance slider from 0.1 (PhET)');
  eq(GH.SPAN_W,85000,'the sunlight span is 85 km wide (PhET)');
  eq(GH.T_MAX_EXPECTED,309,'PhET"s thermometer expects at most 309 K (PhET)');
  eq(GH.SHOW_ONE_IN,5,'PhET draws one photon in five (PhET)');
  eq(DATES.length,4,'four dates');
  eq(DATES[0].c,0.625,'ice age c = 0.625 (PhET)');
  eq(DATES[1].c,0.7147,'1750 c = 0.7147 (PhET)');
  eq(DATES[2].c,0.7182,'1950 c = 0.7182 (PhET)');
  eq(DATES[3].c,0.7446,'2020 c = 0.7446 (PhET)');
  eq(DATES.map(d=>d.co2).join(),'180,277,311,413','the CO2 values (PhET)');
  eq(DATES.map(d=>d.ch4).join(),'380,694,1116,1889','the CH4 values (PhET)');
  eq(DATES.map(d=>d.n2o).join(),'215,271,288,333','the N2O values (PhET)');
  /* the cloud's two factors cancel exactly */
  close(CLOUD_REFL,ref('CLOUD reflectivity, top value'),1e-15,'the cloud reflects exactly 0.125 (python)');
  close(CLOUD_REFL,0.125,1e-15,'0.125 x 85000/18000 x 18000/85000 = 0.125');
  rel(GH.CLOUD_REFL_TOP,ref('CLOUD reflectivity, top value',1),1e-13,'PhET"s topVisibleLightReflectivity (python)');
  /* PhET's heat capacities */
  rel(K_GROUND,ref('PHET K per J/m2 ground layer',0),1e-13,'the ground warms 32/15 K per J/m^2 (python)');
  rel(K_SHEET,ref('PHET K per J/m2 ground layer',1),1e-13,'a glass sheet 1.5873 K per J/m^2 (python)');
  close(K_GROUND,32/15,1e-15,'and 32/15 exactly');
  rel(stabilityH(520),ref('STABILITY h_max at 520 K, the sim sub-step',0),1e-13,'the Euler stability bound at 520 K (python)');
  ok(FRAME_DT/SUBSTEPS<stabilityH(520),'the sim sub-step is inside that bound');
  eq(FRAME_DT/SUBSTEPS,ref('STABILITY h_max at 520 K, the sim sub-step',1),'the sub-step is 1/240 s');

  /* ---------- B. physics, against CODATA ---------- */
  rel(SIGMA_CODATA,ref('SIGMA scipy, from hck'),1e-13,'sigma from scipy (scipy)');
  rel(SIGMA_CODATA,ref('SIGMA scipy, from hck',1),1e-13,'and from 2 pi^5 k^4/15 h^3 c^2 (scipy)');
  rel(GH.SIGMA,SIGMA_CODATA,1e-9,'PhET rounds it to ten digits');
  close(Math.abs(GH.SIGMA/SIGMA_CODATA-1),ref('PHET_SIGMA rel err',1),1e-13,'by 3.25e-11 (python)');
  eq(SOLAR_CONSTANT,1361,'the 2015 IAU nominal solar irradiance');
  eq(EARTH_ALBEDO,0.3,'the textbook Bond albedo');
  rel(teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4),ref('EARTH S0 albedo F Teff',3),1e-9,
      'Earth"s effective temperature 254.578 K (python)');
  rel((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4,ref('EARTH S0 albedo F Teff',2),1e-13,'from 238.175 W/m^2 (python)');
  close(teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4),255,0.5,'which is the textbook 255 K');
  rel(teff((1-0.306)*SOLAR_CONSTANT/4),ref('EARTH Teff at NASA albedo 0.306',1),1e-9,
      'and 254.03 K at NASA"s 0.306 (python)');
  rel(EARTH_TSURF-teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4),
      ref('EARTH mean surface T, greenhouse warming',1),1e-9,'so 33.4 K of greenhouse warming (python)');
  rel(Math.pow(2,0.25)*teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4),ref('EARTH one black layer'),1e-9,
      'one black sheet over the real Earth would give 302.7 K (python)');

  /* ---------- C. the geometry of the stack ---------- */
  { const alt=layerAltitudes(12);
    eq(alt.length,12,'twelve altitudes');
    rel(alt[0],ref('ALT12 spacing first last',1),1e-13,'the lowest sheet at 3846.15 m (python)');
    rel(alt[11],ref('ALT12 spacing first last',2),1e-13,'the highest at 46153.8 m (python)');
    rel(alt[1]-alt[0],ref('ALT12 spacing first last',0),1e-13,'evenly spaced by 50000/13 (python)');
    const a3=layerAltitudes(3);
    for(let i=0;i<3;i++) rel(a3[i],ref('ALT3',i),1e-13,'the layer model"s sheet '+(i+1)+' (python)');
    const a=concAbsorbance(0.7147,12);
    for(let i=0;i<12;i++) rel(a[i],ref('P1750 absorbance 12 layers',i),1e-11,
      '1750 absorbance at sheet '+(i+1)+' (python)');
    /* the fit is an exponential: neighbouring sheets are in a fixed ratio */
    close(a[1]/a[0],Math.exp(-(alt[1]-alt[0])/GH.SCALE_H),1e-14,'the ratio between sheets is e^(-dz/H)');
    close(concAbsorbance(0,12)[0],0,1e-15,'no gas, no absorbance'); }

  /* ---------- D. the solver, two independent ways ---------- */
  { let worstAgree=0, worstBal=0, nCase=0;
    const rg=makeRng(4242);
    const cases=[];
    for(let n=0;n<=12;n++) for(const av of [0.05,0.1,0.25,0.5,0.75,0.9,1.0])
      cases.push(new Array(n).fill(av));
    for(let k=0;k<40;k++){
      const n=1+Math.floor(rg.next()*12), c=[];
      for(let i=0;i<n;i++) c.push(0.02+0.97*rg.next());
      cases.push(c);
    }
    for(const c of cases){
      const F=274.88, s1=solveClosed(c,F), s2=solveBrute(c,F);
      worstAgree=Math.max(worstAgree,Math.abs(s1.Eg-s2.Eg)/s2.Eg);
      for(let i=0;i<c.length;i++)
        worstAgree=Math.max(worstAgree,Math.abs(s1.J[i]-s2.J[i])/Math.max(s2.J[i],1e-12));
      const r=balanceResiduals(s1);
      worstBal=Math.max(worstBal,r.layer,r.toa,r.ground,r.net);
      nCase++;
    }
    eq(nCase,131,'131 stacks swept');
    ok(worstAgree<1e-11,'the closed form and the dense linear solve agree ('+worstAgree.toExponential(2)+')');
    ok(worstBal<1e-9,'energy balances at every sheet, the ground, the top, and the net flux is constant ('+worstBal.toExponential(2)+' W/m^2)');
    ok(ref('SOLVER agreement, worst balance residual',1)<1e-9,'as it does in the twin (python)'); }
  /* a mutant that breaks the transfer would still balance if only the invariant were checked,
     so the brute-force solve is asserted against ABSOLUTE reference numbers too */
  { const s=solveClosed(concAbsorbance(0.7147,12),(1-GH.ALB_MEADOW)*GH.S_SUN);
    rel(s.Eg,ref('P1750 Eg Tg',0),1e-11,'1750: the ground radiates 438.15 W/m^2 (python)');
    rel(s.Tg,ref('P1750 Eg Tg',1),1e-11,'1750: the surface is 296.484 K (python)');
    for(let i=0;i<=12;i++) rel(s.U[i],ref('P1750 U 13 levels',i),1e-11,
      '1750: the upward flux at level '+i+' (python)');
    for(let i=0;i<12;i++) rel(s.Tlayer[i],ref('P1750 Tlayer 12',i),1e-10,
      '1750: sheet '+(i+1)+' sits at '+fmt(ref('P1750 Tlayer 12',i),2)+' K (python)');
    const b=solveBrute(concAbsorbance(0.7147,12),(1-GH.ALB_MEADOW)*GH.S_SUN);
    rel(b.Tg,ref('P1750 Eg Tg',1),1e-10,'and the dense solve says the same (python)');
    rel(s.Dg,ref('BACK y1750 Dg Eg F escape',0),1e-11,'1750: 163.27 W/m^2 comes back down (python)');
    rel(s.esc,ref('BACK y1750 Dg Eg F escape',3),1e-12,'1750: 62.74 % of the infrared escapes (python)'); }

  /* ---------- E. the ladder and the absorbance law ---------- */
  { const F=(1-GH.ALB_MEADOW)*GH.S_SUN, T=teff(F);
    rel(F,ref('PHET F0 Teff at albedo 0.2 and 343.6',0),1e-13,'F = 274.88 W/m^2 at PhET"s defaults (python)');
    rel(T,ref('PHET F0 Teff at albedo 0.2 and 343.6',1),1e-11,'so a bare rock sits at 263.87 K (python)');
    for(let n=0;n<=12;n++){
      const s=solveClosed(new Array(n).fill(1),F);
      rel(s.Tg,ref('LADDER black layers N=0..12',n),1e-11,'N = '+n+' black sheets (python)');
      rel(s.Tg,Math.pow(n+1,0.25)*T,1e-13,'and (N+1)^(1/4) T_eff at N = '+n);
      close(s.Eg/F,n+1,1e-11,'the outgoing flux is multiplied by exactly '+(n+1));
    }
    let nLaw=0;
    for(const n of [1,2,3,12]) for(const av of [0.1,0.3,0.5,0.7,0.9,1.0]){
      const s=solveClosed(new Array(n).fill(av),F);
      rel(s.Tg,ref('LAW N='+n+' a='+av+' Ts'),1e-11,'the law at N = '+n+', a = '+av+' (python)');
      rel(s.Tg,T*Math.pow(1+n*av/(2-av),0.25),1e-13,'and T_eff[1+Na/(2-a)]^(1/4) there');
      nLaw++;
    }
    eq(nLaw,24,'24 (N, a) pairs checked');
    /* the general law is NOT the black-sheet law: a mutant that drops the (2-a) would pass
       every a = 1 test, so pin a case where they differ by a lot */
    ok(Math.abs(solveClosed(new Array(3).fill(0.5),F).Tg-Math.pow(4,0.25)*T)>40,
       'at a = 1/2 three sheets are nowhere near three black ones');
    for(const n of [0,1,2,3]) for(const av of [0.1,0.5,1.0])
      for(const [inten,alb] of [[1,0.3],[0.5,0],[2,0.9]]){
        const Fl=(1-alb)*GH.S_SUN*inten, s=solveClosed(new Array(n).fill(av),Fl);
        rel(s.Tg,ref('LM n='+n+' a='+av+' i='+inten+' alb='+alb+' Ts'),1e-11,
            'layer model N='+n+' a='+av+' intensity='+inten+' albedo='+alb+' (python)');
        if(n) for(let i=0;i<n;i++) rel(s.Tlayer[i],
          ref('LM n='+n+' a='+av+' i='+inten+' alb='+alb+' Tlayers',i),1e-10,
          '  its sheet '+(i+1)+' (python)');
      }
    /* the reachable extremes, and PhET's floors */
    rel(teff((1-GH.ALB_MAX)*GH.S_SUN*GH.INT_MIN),ref('LM extremes Tmin Tmax',0),1e-10,
        'the coldest the layer model reaches is 131.9 K (python)');
    ok(teff((1-GH.ALB_MAX)*GH.S_SUN*GH.INT_MIN)>GH.TMIN_LM,
       'so PhET"s 125 K floor never binds with the sun on');
    rel(solveClosed(new Array(3).fill(1),(1-GH.ALB_MIN)*GH.S_SUN*GH.INT_MAX).Tg,
        ref('LM extremes Tmin Tmax',1),1e-10,'and the hottest is 469.2 K (python)');
    rel(teff((1-GH.ALB_GLACIER)*GH.S_SUN*(1-CLOUD_REFL)),ref('CONC coldest reachable'),1e-10,
        'the coldest the concentration screens reach is 253.18 K (python)');
    ok(teff((1-GH.ALB_GLACIER)*GH.S_SUN*(1-CLOUD_REFL))>GH.TMIN_NIGHT,
       'so the 245 K night floor binds only with the sun off'); }

  /* ---------- F. PhET's convention against Kirchhoff ---------- */
  for(const av of [0.2,0.5,0.85]){
    const s=solveClosed(new Array(3).fill(av),(1-GH.ALB_MEADOW)*GH.S_SUN);
    rel(s.Tkirch[0]/s.Tlayer[0],ref('KIRCH a='+av+' ratio a^-1/4',0),1e-12,
        'Kirchhoff"s sheet is a^(-1/4) hotter at a = '+av+' (python)');
    rel(s.Tkirch[0]/s.Tlayer[0],Math.pow(av,-0.25),1e-13,'exactly a^(-1/4)');
    /* and the fluxes are untouched: that is the whole point */
    rel(s.J[0],av*(s.U[0]+s.D[1])/2,1e-13,'the emitted flux is a(U+D)/2 either way at a = '+av);
  }
  close(solveClosed(new Array(3).fill(1),274.88).Tkirch[0],
        solveClosed(new Array(3).fill(1),274.88).Tlayer[0],1e-12,
        'at a = 1 the two conventions coincide');

  /* ---------- G. the photon walk ---------- */
  { const r=makeRng(12345);
    for(let i=0;i<6;i++) rel(r.next(),ref('LCG seed 12345 first 6',i),1e-15,
      'the generator"s value '+(i+1)+' matches Python bit for bit (python)');
    const r2=makeRng(1);
    for(let i=0;i<4;i++) rel(r2.next(),ref('LCG seed 1 first 4',i),1e-15,
      'and from seed 1, value '+(i+1)+' (python)'); }
  { const cases=[['N1a1',[1]],['N3a06',[0.6,0.6,0.6]],['N3a1',[1,1,1]],
                 ['grad1750',concAbsorbance(0.7147,12)]];
    for(const [tag,a] of cases){
      const p=escapeMarkov(a), s=solveClosed(a,(1-GH.ALB_MEADOW)*GH.S_SUN);
      rel(p,ref('ESCAPE '+tag+' markov closed',0),1e-11,'the Markov escape chance ['+tag+'] (python)');
      rel(p,s.esc,1e-12,'equals F/sigma Ts^4 ['+tag+']');
      rel(p,1/(1+s.sum),1e-13,'and 1/(1+Sigma) ['+tag+']');
    }
    close(escapeMarkov([]),1,1e-15,'with no sheets every photon escapes');
    close(escapeMarkov([1]),0.5,1e-14,'one black sheet turns back exactly half');
    close(escapeMarkov([1,1,1]),0.25,1e-14,'three black sheets, one in four');
    for(const [tag,a,m] of [['N1a1',[1],200000],['N3a06',[0.6,0.6,0.6],200000],
                            ['grad1750',concAbsorbance(0.7147,12),200000]]){
      const mc=escapeMonteCarlo(a,m,12345);
      rel(mc.p,ref('MC '+tag+' p markov sigma crossings absorbed up',0),1e-12,
          'the Monte Carlo reproduces the twin exactly ['+tag+'] (python)');
      eq(mc.cross,ref('MC '+tag+' p markov sigma crossings absorbed up',3),'same crossings ['+tag+'] (python)');
      eq(mc.absorbed,ref('MC '+tag+' p markov sigma crossings absorbed up',4),'same absorptions ['+tag+'] (python)');
      eq(mc.up,ref('MC '+tag+' p markov sigma crossings absorbed up',5),'same up-emissions ['+tag+'] (python)');
      const pm=escapeMarkov(a), sig=Math.sqrt(pm*(1-pm)/m);
      ok(Math.abs(mc.p-pm)<4*sig,'and lands within 4 sigma of the exact value ['+tag+']');
      ok(Math.abs(mc.up/mc.absorbed-0.5)<4*Math.sqrt(0.25/mc.absorbed),
         'the re-emission is 50/50 ['+tag+']');
    }
    /* a single crossing absorbs with probability exactly a */
    for(const av of [0.2,0.5,0.85]){
      const r=makeRng(777); let hit=0;
      for(let k=0;k<100000;k++) if(r.next()<av) hit++;
      rel(hit/100000,ref('ABS a='+av+' measured sigma',0),1e-12,
          'a single crossing absorbs a fraction a = '+av+' (python)');
      ok(Math.abs(hit/100000-av)<4*ref('ABS a='+av+' measured sigma',1),'within 4 sigma of a = '+av);
    }
    rel(irPhotonRate(296.48445421,245),ref('PHOTONS visible per s at intensity 1, IR at 1750',1),1e-9,
        'PhET emits 56.17 IR photons a second at 1750 (python)');
    close(irPhotonRate(245,245),0,1e-15,'and none at all at the night floor');
    rel(irPhotonRate(309,245),ref('PHOTONS IR at 245 246 and 309 K',2),1e-9,'66.28 at 309 K (python)'); }

  /* ---------- H. PhET's dates ---------- */
  for(const d of DATES){
    const alb=d.glacier?GH.ALB_GLACIER:GH.ALB_MEADOW;
    const s=solveClosed(concAbsorbance(d.c,12),(1-alb)*GH.S_SUN);
    rel(s.Tg,ref('DATE '+d.id+' c alb F Ts a1 a12',3),1e-11,d.name+': the surface is '+
        fmt(ref('DATE '+d.id+' c alb F Ts a1 a12',3),2)+' K (python)');
    rel(alb,ref('DATE '+d.id+' c alb F Ts a1 a12',1),1e-15,d.name+': albedo (PhET)');
    rel(kToC(s.Tg),ref('DATE '+d.id+' Tc Tf',0),1e-10,d.name+': in celsius (python)');
    rel(kToF(s.Tg),ref('DATE '+d.id+' Tc Tf',1),1e-10,d.name+': in fahrenheit (python)');
  }
  { const R=DATES.map(d=>solveClosed(concAbsorbance(d.c,12),
      (1-(d.glacier?GH.ALB_GLACIER:GH.ALB_MEADOW))*GH.S_SUN).Tg);
    close(R[0]-R[1],-6.29,0.02,'PhET"s ice age is 6.29 K below 1750');
    close(R[3]-R[1],1.32,0.02,'and its 2020 is 1.32 K above it');
    close(R[1]-EARTH_TSURF,8.48,0.02,'while its 1750 sits 8.48 K above the real Earth');
    ok(R[0]<R[1]&&R[1]<R[2]&&R[2]<R[3],'the four dates are in order'); }
  for(const c of [0,0.25,0.5,0.75,1]){
    const F=(1-GH.ALB_MEADOW)*GH.S_SUN, a=concAbsorbance(c,12);
    rel(solveClosed(a,F).Tg,ref('CONC c='+c+' Ts Ts_cloud',0),1e-11,'c = '+c+' (python)');
    rel(solveClosed(a,F*(1-CLOUD_REFL)).Tg,ref('CONC c='+c+' Ts Ts_cloud',1),1e-11,
        'c = '+c+' with the cloud (python)');
    rel(a.reduce((s,x)=>s+x/(2-x),0),ref('CONC c='+c+' sumstep escape',0),1e-11,
        'and its Sigma a/(2-a) (python)');
  }
  { const hot=solveClosed(concAbsorbance(1,12),(1-GH.ALB_MEADOW)*GH.S_SUN).Tg;
    rel(hot,ref('HOTTEST reachable, PhET expected max',0),1e-11,'the hottest reachable state (python)');
    close(hot,GH.T_MAX_EXPECTED,0.2,'which is PhET"s own EXPECTED_MAX_TEMPERATURE of 309 K');
    for(const d of DATES){
      const a=concAbsorbance(d.c,12), S=a.reduce((s,x)=>s+x/(2-x),0);
      rel(S,ref('EQUIV '+d.id+' sum aeq',0),1e-11,d.name+': Sigma a/(2-a) (python)');
      const aeq=2*S/(12+S);
      rel(aeq,ref('EQUIV '+d.id+' sum aeq',1),1e-11,d.name+': the equivalent uniform a (python)');
      rel(12*aeq/(2-aeq),S,1e-12,'which reproduces the sum');
    } }

  /* ---------- I. the integrator, against the twin step for step ---------- */
  { const a=concAbsorbance(0.7147,12), F=(1-GH.ALB_MEADOW)*GH.S_SUN;
    const th=makeThermal(12,GH.TMIN_NIGHT);
    eq(th.Tg,GH.TMIN_NIGHT,'the march starts at PhET"s night floor');
    eq(th.T[0],0,'with every sheet at 0 K, as PhET"s constructor leaves them');
    const want=[[1,'MARCH 1750 frame 1 Tg'],[6,'MARCH 1750 frame 6 Tg'],
                [60,'MARCH 1750 frame 60 Tg'],[300,'MARCH 1750 frame 300 Tg'],
                [1800,'MARCH 1750 frame 1800 Tg']];
    let f=0;
    for(const [n,label] of want){
      while(f<n){ marchFrame(th,a,F,GH.TMIN_NIGHT,FRAME_DT,SUBSTEPS); f++; }
      rel(th.Tg,ref(label),1e-9,'frame '+n+' of the march matches the twin (python)');
    }
    rel(th.T[0],ref('MARCH 1750 frame 1800 layer1 layer12',0),1e-8,'and its lowest sheet (python)');
    rel(th.T[11],ref('MARCH 1750 frame 1800 layer1 layer12',1),1e-8,'and its highest (python)');
    const s=solveClosed(a,F);
    close(th.Tg,s.Tg,0.2,'thirty seconds puts the ground within 0.2 K of the exact steady state');
    ok(Math.abs(th.T[11]-s.Tlayer[11])>1,
       'while the coldest sheet is still far from its own — which is why the readout prints both');
    /* run it a long way and it converges */
    for(let k=0;k<12000;k++) marchFrame(th,a,F,GH.TMIN_NIGHT,FRAME_DT,SUBSTEPS);
    rel(th.Tg,s.Tg,1e-6,'and 230 s converges to the closed form');
    for(let i=0;i<12;i++) rel(th.T[i],s.Tlayer[i],1e-4,'as does sheet '+(i+1));
    /* the three-sheet layer model, likewise */
    const th3=makeThermal(3,GH.TMIN_LM), a3=[0.7,0.7,0.7], F3=(1-0.3)*GH.S_SUN;
    for(let k=0;k<30;k++) marchFrame(th3,a3,F3,GH.TMIN_LM,FRAME_DT,SUBSTEPS);
    rel(th3.Tg,ref('MARCH LM3 a0.7 frame 30 Tg T1 T2 T3',0),1e-9,'the layer model march (python)');
    for(let i=0;i<3;i++) rel(th3.T[i],ref('MARCH LM3 a0.7 frame 30 Tg T1 T2 T3',1+i),1e-9,
      '  its sheet '+(i+1)+' (python)');
    /* the floor does bind with the sun off */
    const th0=makeThermal(3,GH.TMIN_LM); th0.Tg=300;
    for(let k=0;k<4000;k++) marchFrame(th0,[0,0,0],0,GH.TMIN_LM,FRAME_DT,SUBSTEPS);
    close(th0.Tg,GH.TMIN_LM,1e-9,'with the sun off the ground falls to the 125 K floor and stops');
    /* the stability clamp: a huge step must not blow up */
    const thB=makeThermal(3,GH.TMIN_LM); marchFrame(thB,[1,1,1],400,GH.TMIN_LM,1.0,1);
    ok(isFinite(thB.Tg)&&thB.Tg<1e4,'a one-second step is sub-divided rather than diverging'); }

  /* ---------- J. temperature units ---------- */
  { for(const K of [245,255,273.15,288,309]){
      close(kToC(K),K-273.15,1e-12,'K to C at '+K);
      close(kToF(K),(K-273.15)*9/5+32,1e-12,'K to F at '+K);
    }
    close(kToF(273.15),32,1e-12,'0 C is 32 F');
    close(kToF(233.15),-40,1e-12,'-40 C is -40 F');
    close(kToC(288),ref('UNITS K=288 C F',1),1e-12,'288 K is 14.85 C (python)');
    close(kToF(288),ref('UNITS K=288 C F',2),1e-12,'and 58.73 F (python)');
    eq(tempIn(300,'K'),300,'tempIn leaves kelvin alone');
    close(tempIn(300,'C'),26.85,1e-12,'and converts to celsius');
    close(tempIn(300,'F'),80.33,1e-12,'and to fahrenheit');
    eq(UNIT_SYM.C,'°C','the celsius symbol is a literal glyph, not an entity');
    /* a temperature DIFFERENCE is not a temperature: 10 K is 10 C but 18 F */
    eq(plain(dK(10,'K',1)),'+10.0 K','10 K difference'); eq(plain(dK(10,'C',1)),'+10.0 K','is 10 C');
    eq(plain(dK(10,'F',1)),'+18.0 °F','and 18 F'); }

  /* ---------- K. the model object the panels are built from ---------- */
  { Object.assign(ST,DEFAULTS); ST.mode='date'; ST.date='y1750'; resetThermal(); settle();
    const M=buildModel();
    rel(M.S.Tsteady,ref('DATE y1750 c alb F Ts a1 a12',3),1e-11,'the model"s 1750 steady state (python)');
    rel(M.S.Tg,M.S.Tsteady,1e-12,'and "jump to equilibrium" lands on it');
    rel(M.S.F,ref('DATE y1750 c alb F Ts a1 a12',2),1e-12,'with F = 274.88 W/m^2 (python)');
    close(M.S.net,0,1e-9,'so the net flux at the top is zero');
    rel(M.S.Utop,M.S.F,1e-12,'and the outgoing infrared equals the absorbed sunlight');
    rel(M.S.probe.U,M.S.Ul[M.S.probe.i],1e-15,'the flux sensor reads the live profile');
    /* and once the model has settled, the live profile IS the exact one — the meter and the
       closed form are the same numbers, which is the whole claim of the view */
    for(let i=0;i<=M.S.a.length;i++){
      close(M.S.Ul[i],M.S.Us[i],1e-8,'settled: the live upward flux at level '+i+' is the exact one');
      close(M.S.Dl[i],M.S.Ds[i],1e-8,'and the downward one');
    }
    /* with the sun off they part company, and the meter follows the MODEL */
    { const sunSave=ST.sun; ST.sun=false; const m0=buildModel();
      close(m0.S.s.Eg,0,1e-12,'the sun off: the steady solve is identically zero');
      rel(m0.S.Ul[0],sbFlux(m0.S.Tg),1e-12,
          'while the ground is still warm and still radiating');
      ok(m0.S.Ul[0]>100,'which is not nothing ('+fmt(m0.S.Ul[0],1)+' W/m^2)');
      rel(m0.S.probe.U,m0.S.Ul[m0.S.probe.i],1e-15,'and the sensor reads that, not the zero');
      ST.sun=sunSave; }
    /* the sensor at the ground and at the top */
    PROBE.z=0; { const m2=buildModel(); rel(m2.S.probe.U,m2.S.s.Eg,1e-12,'at the ground it reads sigma Ts^4');
      close(m2.S.probe.net,m2.S.F,1e-9,'and the net there is F'); }
    PROBE.z=GH.TOP; { const m2=buildModel();
      close(m2.S.probe.D,0,1e-12,'at the top nothing comes down');
      rel(m2.S.probe.U,m2.S.F,1e-12,'and exactly F goes up'); }
    PROBE.z=probeSave;
    /* the ice age switches the ground to the glaciated albedo, by date only */
    ST.date='iceAge'; { const m2=buildModel(); rel(m2.S.albedo,GH.ALB_GLACIER,1e-15,'the ice age is glaciated (PhET)'); }
    ST.mode='value'; ST.conc=0.625;
    { const m2=buildModel(); rel(m2.S.albedo,GH.ALB_MEADOW,1e-15,
        'but the same concentration set by hand is a green meadow (PhET)'); }
    /* the cloud */
    ST.cloud=true; { const m2=buildModel(); rel(m2.S.F,(1-GH.ALB_MEADOW)*GH.S_SUN*(1-CLOUD_REFL),1e-12,
      'the cloud takes 12.5 % of the sunlight before the ground sees it'); }
    ST.cloud=false;
    /* the sun off */
    ST.sun=false; { const m2=buildModel(); close(m2.S.F,0,1e-15,'the sun off means no absorbed flux'); }
    ST.sun=true;
    /* the layer model */
    ST.view='layers'; ST.nLayers=2; ST.absorb=0.5; ST.intensity=1; ST.albedo=0.3;
    resetThermal(); settle();
    { const m2=buildModel();
      rel(m2.S.Tsteady,ref('LM n=2 a=0.5 i=1 alb=0.3 Ts'),1e-11,'two sheets at a = 0.5 (python)');
      /* the intensity and the albedo have to be read OFF the model, not recomputed beside
         it: every other layer-model assertion here builds its own F and would pass with the
         slider disconnected (the drum_head rule — assert off the built model) */
      rel(m2.S.F,(1-0.3)*GH.S_SUN,1e-12,'and the model"s own F at one sun');
      rel(m2.S.A.Sin,GH.S_SUN,1e-12,'with 343.6 W/m^2 arriving');
      eq(m2.S.a.filter(x=>x>0).length,2,'exactly two sheets absorb');
      eq(m2.S.a[2],0,'and the top one is switched off');
      rel(m2.S.Ssteady[0],ref('LM n=2 a=0.5 i=1 alb=0.3 Tlayers',0),1e-10,'its lowest sheet (python)');
      ok(m2.S.Ssteady[2]===null,'the inactive sheet has no temperature at all'); }
    for(const inten of [0.5,2]){
      ST.intensity=inten; resetThermal(); settle();
      const m3=buildModel();
      rel(m3.S.F,(1-0.3)*GH.S_SUN*inten,1e-12,'the solar-intensity slider reaches the model at '+inten+' suns');
      rel(m3.S.A.Sin,GH.S_SUN*inten,1e-12,'and the sunlight arriving at the top');
      rel(m3.S.Tsteady,ref('LM n=2 a=0.5 i='+inten+' alb=0.3 Ts2'),1e-11,
          'so the surface sits at '+fmt(ref('LM n=2 a=0.5 i='+inten+' alb=0.3 Ts2'),3)+' K (python)');
    }
    ST.intensity=1;
    /* the ladder's "equivalent uniform absorbance", off the model */
    ST.view='ladder'; ST.nLayers=3; ST.absorb=0.4;
    { const L=buildModel().L;
      rel(L.aEq,0.4,1e-13,'three sheets all at 0.4 are equivalent to a uniform 0.4');
      ST.absorb=0.9; const L2=buildModel().L;
      rel(L2.aEq,0.9,1e-13,'and three at 0.9 to a uniform 0.9');
      rel(3*L2.aEq/(2-L2.aEq),L2.here.sum,1e-12,'the equivalence is of Sigma a/(2-a)'); }
    Object.assign(ST,stSave); PROBE.z=probeSave; resetThermal(); }

  /* the ladder's marker sits ON the family it is drawn over, which is at PhET's own F,
     while the readout's "stack you have loaded" is the same sheets at the albedo and
     intensity actually set: assert both, and assert they DIFFER when they should */
  { Object.assign(ST,DEFAULTS); ST.view='ladder'; ST.nLayers=2; ST.absorb=0.5;
    ST.albedo=0.3; ST.intensity=1;
    const L=buildModel().L;
    rel(L.hereCurveT,teff((1-GH.ALB_MEADOW)*GH.S_SUN)*Math.pow(1+2*0.5/1.5,0.25),1e-12,
        'the ladder marker lies on the plotted family');
    rel(L.here.Tg,ref('LM n=2 a=0.5 i=1 alb=0.3 Ts'),1e-11,
        'while the readout carries the layer model"s own stack (python)');
    ok(Math.abs(L.hereCurveT-L.here.Tg)>3,'and at albedo 0.3 against 0.2 they differ by 3 K');
    rel(L.earthEqA,2*L.earth.sum/(1+L.earth.sum),1e-13,'the Earth"s equivalent single sheet');
    close(L.earth.sum,Math.pow(EARTH_TSURF/L.earth.T0,4)-1,1e-13,'from (288/254.578)^4 - 1');
    close(L.earthEqA,0.779,0.002,'which is one sheet at a = 0.779');
    Object.assign(ST,stSave); }

  /* ---------- L. the panels build clean, every view x preset x size ---------- */
  const SIZES=[[1400,820],[1180,760],[980,640],[760,520],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  const CONFIGS=[
    {view:'waves'},
    {view:'waves',mode:'date',date:'iceAge',flux:true,sheets:true},
    {view:'waves',mode:'date',date:'y2020',balance:false},
    {view:'waves',conc:0,cloud:true,unit:'K'},
    {view:'waves',conc:1,unit:'F',flux:true},
    {view:'waves',sun:false},
    {view:'photons'},
    {view:'photons',morePhotons:true,mode:'date',date:'y2020'},
    {view:'photons',conc:0,flux:true},
    {view:'layers',nLayers:0},
    {view:'layers',nLayers:3,absorb:1,flux:true,sheets:true},
    {view:'layers',nLayers:1,absorb:0.1,intensity:2,albedo:0.9,unit:'K'},
    {view:'layers',nLayers:2,absorb:0.5,intensity:0.5,albedo:0,kirch:true},
    {view:'ladder'},
    {view:'ladder',unit:'K',nLayers:3,absorb:0.6},
    {view:'record'},
    {view:'record',unit:'F',mode:'date',date:'y2020'}
  ];
  for(const base of CONFIGS){
    Object.assign(ST,DEFAULTS,base);
    resetThermal();
    if(SKY_VIEWS[ST.view]){ settle(); if(ST.view==='photons') for(let k=0;k<120;k++) stepPhotons(atmosphere(),FRAME_DT); }
    const nm=JSON.stringify(base);
    for(const [W,H] of SIZES){
      const c=makeShot(W,H);
      let err=null, M=null;
      try{ M=buildModel(); drawView(c,W,H,M); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      const rects=fills.reduce((a,o)=>a+(o.n||1),0), strokes=c.ops.filter(o=>o.op==='stroke').length;
      ok(rects>=8&&strokes>=6&&texts.length>=6,
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
      /* the readout, the equation bar and the tag, from the same model */
      const ro=readoutHTML(M), eb=eqbarHTML(M), tg=tagHTML(M);
      ok(ro.indexOf('NaN')<0&&ro.indexOf('undefined')<0&&ro.indexOf('Infinity')<0,nm+' readout clean');
      ok(eb.indexOf('NaN')<0&&tg.indexOf('NaN')<0,nm+' equation bar and tag clean');
      ok(ro.length>400,nm+' readout has substance ('+ro.length+' chars)');
    }
  }
  Object.assign(ST,stSave); PROBE.z=probeSave; resetThermal();

  /* ---------- M. the readout prints the numbers it claims to ---------- */
  { Object.assign(ST,DEFAULTS); ST.mode='date'; ST.date='y1750'; ST.unit='K';
    resetThermal(); settle();
    const M=buildModel(), ro=readoutHTML(M);
    ok(ro.indexOf('296.48 K')>=0,'the readout prints 1750"s 296.48 K off the model');
    ok(ro.indexOf('274.88 W/m&sup2;')>=0,'and the 274.88 W/m^2 it absorbs');
    ok(ro.indexOf('277 ppm')>=0,'and PhET"s 277 ppm of CO2');
    ST.unit='C'; ok(readoutHTML(buildModel()).indexOf('23.33 °C')>=0,'in celsius, 23.33 °C');
    ST.unit='F'; ok(readoutHTML(buildModel()).indexOf('74.00 °F')>=0,'in fahrenheit, 74.00 °F');
    Object.assign(ST,stSave); resetThermal(); }

  /* the record view's ice-age connector: the gap IS the whitening of the ground */
  { Object.assign(ST,DEFAULTS); ST.view='record';
    const R=buildModel().R;
    rel(R.iceOnCurve,solveClosed(concAbsorbance(0.625,GH.N_CONC),(1-GH.ALB_MEADOW)*GH.S_SUN).Tg,
        1e-13,'the ice age on the plotted curve is the same c over a green meadow');
    ok(R.iceOnCurve>R.rows[0].Ts,'which is warmer than PhET"s glaciated ice age');
    close(R.iceOnCurve-R.rows[0].Ts,
          teff((1-GH.ALB_MEADOW)*GH.S_SUN)*Math.pow(1+R.rows[0].s.sum,0.25)
          -teff((1-GH.ALB_GLACIER)*GH.S_SUN)*Math.pow(1+R.rows[0].s.sum,0.25),1e-9,
          'by exactly what the albedo 0.2 -> 0.225 is worth');
    Object.assign(ST,stSave); }

  /* ---------- N. canvas prose carries no markup ---------- */
  /* plain() STRIPS tags, so 10<sup>13</sup> reaches the canvas as "1013" — a wrong number,
     not a cosmetic loss — and nothing downstream can see it: the string is well formed and
     the audits only look for entities that survived.  Guard the constants themselves. */
  { const CANVAS_PROSE=[['CAP_WAVES',CAP_WAVES],['CAP_WAVES_S',CAP_WAVES_S],
      ['CAP_PHOTONS',CAP_PHOTONS],['CAP_PHOTONS_S',CAP_PHOTONS_S],
      ['CAP_LAYERS',CAP_LAYERS],['CAP_LAYERS_S',CAP_LAYERS_S],
      ['CAP_LADDER',CAP_LADDER],['CAP_LADDER_S',CAP_LADDER_S],
      ['CAP_RECORD',CAP_RECORD],['CAP_RECORD_S',CAP_RECORD_S]];
    for(const [nm,t] of CANVAS_PROSE){
      ok(!/<su[bp]>/.test(t),nm+' carries no <sub>/<sup>: plain() strips them silently');
      ok(plain(t).indexOf('&')<0,nm+' decodes to literal glyphs');
      ok(plain(t).indexOf('<')<0,nm+' has no tags left after plain()');
    } }

  /* ---------- O. the formatters and the shared helpers ---------- */
  { eq(plain('&sigma;T&sup2; &minus; x'),'σT² − x','plain() decodes the entities this file uses');
    eq(plain('a<sub>1</sub>'),'a1','and strips tags');
    eq(plain('&#955;'),'λ','and numeric entities');
    eq(fmt(296.48445421,2),'296.48','fmt to two places');
    eq(sigf(0.0024963719,3),'0.00250','sigf keeps three figures');
    eq(plain(tstr(296.48445421,'K',2)),'296.48 K','tstr in kelvin');
    eq(plain(tstr(273.15,'C',2)),'0.00 °C','tstr in celsius');
    ok(/^rgb\(\d+,\d+,\d+\)$/.test(mix(COL.sky0,COL.sky1,0.5)),'mix is well formed');
    { const g=toRgb(mix(COL.sky0,COL.sky1,1)); eq(g.join(),toRgb(COL.sky1).join(),'and reaches its end');
      eq(toRgb(shade(COL.pos,0)).join(),toRgb('#070b18').join(),'shade(col,0) is the page background, not the colour');
      eq(toRgb(shade(COL.pos,1)).join(),toRgb(COL.pos).join(),'and shade(col,1) is the colour itself'); }
    /* ticksFor on an inverted range (standard_candle Known-bad) */
    ok(ticksFor(0,12,6).length>=5,'ticksFor gives a full set on a sane range');
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
