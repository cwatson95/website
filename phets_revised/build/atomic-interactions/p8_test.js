
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/atomic-interactions/refvals.txt, the printed output *
 *  of derive.py (scipy.constants CODATA 2022, 60- and 90-digit        *
 *  Decimal finite differences, scipy.differentiate), read in full.    *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),
    name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now();
  const stSave=Object.assign({},ST);
  function withState(over,fn){
    Object.assign(ST,DEFAULTS,over); simReset();
    try{ return fn(); } finally{ Object.assign(ST,stSave); simReset(); }
  }

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,
       'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  close(DEG*90,Math.PI/2,1e-15,'DEG converts degrees INTO radians (90° = π/2)');

  /* ---------- A. the constants, against absolute numbers ---------- */
  eq(KBOLTZ,1.380649e-23,'k_B, exact since the 2019 SI');
  eq(MU_KG,1.66053906892e-27,'m_u (CODATA 2022)');
  eq(QE,1.602176634e-19,'e, exact since the 2019 SI');
  rel(K_TO_E,8314.4626094101,1e-13,'K_TO_E = k_B/m_u (derive)');
  rel(E_TO_MEV,1.0364269667161e-5,1e-12,'E_TO_MEV (derive)');
  rel(E_TO_ZJ,1.66053906892e-6,1e-15,'E_TO_ZJ (derive)');
  rel(F_TO_PN,0.00166053906892,1e-15,'F_TO_PN (derive)');
  rel(SIXRT2,1.12246204830937,1e-14,'2^(1/6) (derive)');
  rel(CBRT2,1.25992104989487,1e-14,'2^(1/3) (derive)');
  rel(72/CBRT2,57.1464378708552,1e-13,'72/2^(1/3) (derive)');

  /* ---------- B. PhET's tables, exactly as the original carries them ---------- */
  eq(ATOM.Ne.r,154,"PhET's neon van der Waals radius");
  eq(ATOM.Ar.r,188,"PhET's argon van der Waals radius");
  eq(ATOM.O.r,152,"PhET's oxygen van der Waals radius");
  eq(ATOM.X.r,175,"PhET's ADJUSTABLE_ATTRACTION_DEFAULT_RADIUS");
  eq(ATOM.Ne.m,20.1797,"PhET's neon mass"); eq(ATOM.Ar.m,39.948,"PhET's argon mass");
  eq(ATOM.O.m,15.9994,"PhET's oxygen mass"); eq(ATOM.X.m,25,"PhET's adjustable mass");
  eq(PHET_MIN_SIGMA,75,'PhET MIN_SIGMA'); eq(PHET_MAX_SIGMA,500,'PhET MAX_SIGMA');
  eq(PHET_MIN_EPSILON,20,'PhET MIN_EPSILON'); eq(PHET_MAX_EPSILON,450,'PhET MAX_EPSILON');
  eq(PHET_ADJ_SIGMA,350,"PhET's adjustable default diameter, 2 x 175 pm");
  eq(PHET_ADJ_EPSILON,100,"PhET's adjustable default interaction strength");
  eq(PHET_SOM.epsO2,113,"PhET's own EPSILON_FOR_DIATOMIC_OXYGEN");
  eq(PHET_SOM.sigO2,365,"PhET's own SIGMA_FOR_DIATOMIC_OXYGEN");
  eq(PHET_CRIT.Ar,151,"PhET's argon critical point"); eq(PHET_CRIT.Ne,45,"PhET's neon critical point");
  eq(PHET_CRIT.O,155,"PhET's O2 critical point"); eq(PHET_TRIPLE.Ar,75,"PhET's argon triple point");
  eq(PAIRS.length,7,'PhET offers seven pairs');
  eq(PAIR_BY_KEY.NeNe.eps,35.8,"PhET's neon-neon eps/k_B");
  eq(PAIR_BY_KEY.ArAr.eps,111.84,"PhET's argon-argon eps/k_B");
  eq(PAIR_BY_KEY.OO.eps,1000,"PhET's oxygen-oxygen eps/k_B");
  eq(PAIR_BY_KEY.NeAr.eps,59.5,"PhET's neon-argon eps/k_B");
  eq(PAIR_BY_KEY.NeO.eps,51,"PhET's neon-oxygen eps/k_B");
  eq(PAIR_BY_KEY.ArO.eps,85,"PhET's argon-oxygen eps/k_B");
  eq(PAIR_BY_KEY.NeNe.sig,308,"PhET's neon-neon sigma");
  eq(PAIR_BY_KEY.ArAr.sig,376,"PhET's argon-argon sigma");
  eq(PAIR_BY_KEY.OO.sig,200,"PhET's oxygen-oxygen sigma");
  eq(PAIR_BY_KEY.NeAr.sig,343,"PhET's neon-argon sigma");
  eq(PAIR_BY_KEY.NeO.sig,306,"PhET's neon-oxygen sigma = r(Ne) + r(O)");
  eq(PAIR_BY_KEY.ArO.sig,340,"PhET's argon-oxygen sigma = r(Ar) + r(O)");
  /* the literature, with its sources */
  eq(LIT.Ne.sig,278.9,'literature neon sigma (van Sciver table)');
  eq(LIT.Ne.eps,35.7,'literature neon eps/k_B');
  eq(LIT.Ne.rmin,313.1,'literature neon r_min, as the table prints it');
  eq(LIT.Ar.sig,341.8,'literature argon sigma'); eq(LIT.Ar.eps,124.0,'literature argon eps/k_B');
  eq(LIT.Ar.rmin,383.7,'literature argon r_min');
  eq(LIT.O.sig,343.3,'literature O2 sigma (Bird Stewart Lightfoot)');
  eq(LIT.O.eps,113,'literature O2 eps/k_B');
  eq(LIT_ALT.Ar.eps,122.4,"argon's second retrieved eps/k_B (BSL)");
  rel(LIT.Ar.eps/LIT_ALT.Ar.eps-1,0.013071895424836555,1e-13,
      'the two argon sources differ by 1.31% in eps — the honest uncertainty');

  /* ---------- C. the potential ---------- */
  const SIG=308, EPSK=35.8, EPS=EPSK*K_TO_E;
  rel(EPS,297657.76141688,1e-13,'neon eps in u (pm/ps)^2 (derive)');
  rel(EPS*E_TO_MEV,3.085005307848,1e-12,'neon eps in meV (derive)');
  rel(EPS*E_TO_ZJ,0.494272342,1e-9,'neon eps in zJ (derive)');
  eq(ljV(SIG,SIG,EPS),0,'V(sigma) = 0 exactly');
  rel(rMin(SIG),345.71831087929,1e-13,'r_min = 2^(1/6) sigma (derive)');
  rel(ljV(rMin(SIG),SIG,EPS)/EPS,-1,1e-15,'V(r_min) = -eps exactly');
  /* the pinned values, off the model function, at fixed multiples of sigma */
  const VPINS=[[0.9,1975292.3121214,134003.61453585],[0.95,583699.32656441,57151.790983946],
               [1.0,0,23194.111279238],[1.2,-265202.73300213,-2137.4275622946],
               [1.5,-95350.673552868,-1119.1437321604],[2.0,-18312.928680921,-175.54136954501],
               [3.0,-1630.9983634043,-10.576350526214]];
  VPINS.forEach(([f,v,fF])=>{
    rel(ljV(f*SIG,SIG,EPS),v,1e-12,'V at r/sigma = '+f+' (derive)');
    rel(ljF(f*SIG,SIG,EPS),fF,1e-12,'F at r/sigma = '+f+' (derive)');
  });
  /* argon, so no pin depends on one pair */
  rel(ljV(0.95*376,376,111.84*K_TO_E),1823489.7397476,1e-12,'argon V at 0.95 sigma (derive)');
  rel(ljF(1.5*376,376,111.84*K_TO_E),-2863.9331080979,1e-12,'argon F at 1.5 sigma (derive)');
  rel(ljV(rMin(376),376,111.84*K_TO_E),-929889.49823643,1e-13,'argon V(r_min) = -eps (derive)');
  /* a pure scaling identity: V/eps depends on r/sigma alone */
  rel(ljV(1.37*777,777,5)/5,ljV(1.37*SIG,SIG,EPS)/EPS,1e-13,
      'V/eps is a function of r/sigma only');

  /* ---------- D. the force is exactly minus the derivative ---------- */
  eq(ljF(SIG,SIG,EPS),24*EPS/SIG*(2-1),'F(sigma) = 24 eps/sigma');
  close(ljF(rMin(SIG),SIG,EPS)/(24*EPS/rMin(SIG)),0,1e-15,'F(r_min) = 0 (derive: -1.11e-16 of the scale)');
  [0.85,0.95,1.0,1.12,1.4,2.0,3.5].forEach(f=>{
    const r=f*SIG, scale=24*EPS/r;
    rel(ljF(r,SIG,EPS)/scale,numForce(r,SIG,EPS)/scale,3e-9,
        'F = -dV/dr by Richardson difference at r/sigma = '+f);
  });
  /* PhET's own two halves, which must difference to the same thing */
  [0.95,1.122462048309373,1.5].forEach(f=>{
    const r=f*SIG;
    close(ljRepulsive(r,SIG,EPS)-ljAttractive(r,SIG,EPS)-ljF(r,SIG,EPS),0,
          1e-9*Math.abs(24*EPS/r),"PhET's 48 e sig^12/r^13 minus 24 e sig^6/r^7 IS -dV/dr at r/sigma = "+f);
  });
  rel(ljRepulsive(SIG,SIG,EPS),48*EPS/SIG,1e-14,'the repulsive half at r = sigma is 48 eps/sigma');
  rel(ljAttractive(SIG,SIG,EPS),24*EPS/SIG,1e-14,'the attractive half at r = sigma is 24 eps/sigma');
  /* the sign convention: positive pushes the movable atom out */
  ok(ljF(0.98*SIG,SIG,EPS)>0&&ljF(1.4*SIG,SIG,EPS)<0,
     'F > 0 inside sigma (repulsive), F < 0 outside r_min (attractive)');
  rel(ljF(1.2*SIG,SIG,EPS)*F_TO_PN,-3.5492819741767,1e-12,'F at 1.2 sigma in pN (derive)');
  rel(4*EPS/SIG*F_TO_PN,6.4191213246753,1e-12,'the force scale 4 eps/sigma in pN (derive)');

  /* ---------- E. the curvature and the small-oscillation spring ---------- */
  [0.85,0.95,1.0,1.12,1.4,2.0,3.5].forEach(f=>{
    const r=f*SIG;
    rel(ljVpp(r,SIG,EPS),numVpp(r,SIG,EPS),2e-7,"V'' by Richardson difference at r/sigma = "+f);
  });
  rel(ljVpp(rMin(SIG),SIG,EPS),179.31017846167,1e-12,"V''(r_min) (derive)");
  rel(ljK(SIG,EPS),179.31017846167,1e-12,"ljK = 72 eps/(2^(1/3) sigma^2) (derive)");
  rel(ljK(SIG,EPS),ljVpp(rMin(SIG),SIG,EPS),1e-14,'the closed form and the general one agree');
  /* the inflection of V: where the pull is strongest */
  const RF=SIG*Math.pow(26/7,1/6);
  rel(Math.pow(26/7,1/6),1.24445506025981,1e-14,'(26/7)^(1/6) (derive)');
  rel(RF,383.29215856002,1e-12,'r_F for neon (derive)');
  close(ljVpp(RF,SIG,EPS),0,1e-11,"V''(r_F) = 0 (derive: 5.4e-14)");
  rel(ljF(RF,SIG,EPS),-2315.9602899217,1e-12,'F(r_F), the deepest pull (derive)');
  rel(ljF(RF,SIG,EPS)*F_TO_PN,-3.8457425434822,1e-12,'F(r_F) in pN (derive)');
  { /* and it really is the minimum: no sample beats it */
    let worst=0, rW=0;
    for(let i=0;i<=4000;i++){ const r=SIG*(1.0+2.4*i/4000), f=ljF(r,SIG,EPS);
      if(f<worst){ worst=f; rW=r; } }
    close(rW,RF,0.3,'a 4001-point scan puts the deepest pull at r_F');
  }
  /* omega, and the reduced mass that sets it */
  rel(ljOmega(SIG,EPS,ATOM.Ne.m),2.9808842928973,1e-12,'omega, left atom pinned (derive)');
  rel(ljPeriod(SIG,EPS,ATOM.Ne.m),2.1078259636413,1e-12,'T = 2 pi/omega, pinned (derive)');
  rel(ljOmega(SIG,EPS,ATOM.Ne.m)*1e12,2980884292897.3,1e-12,'omega in rad/s (derive)');
  rel(ljPeriod(SIG,EPS,ATOM.Ne.m/2),1.4904580324518,1e-12,'T with both atoms free (derive)');
  rel(ljPeriod(SIG,EPS,ATOM.Ne.m)/ljPeriod(SIG,EPS,ATOM.Ne.m/2),Math.SQRT2,1e-14,
      'freeing a LIKE partner shortens the period by exactly sqrt(2)');
  eq(effMass(ATOM.Ne.m,ATOM.Ar.m,true),ATOM.Ar.m,'pinned: mu is the movable atom');
  rel(effMass(ATOM.Ne.m,ATOM.Ar.m,false),13.407109462028314,1e-14,'free: mu = m1 m2/(m1+m2) (derive)');
  rel(ljPeriod(376,111.84*K_TO_E,ATOM.Ar.m),2.0483538387693,1e-12,'argon T pinned (derive)');
  rel(ljPeriod(350,100*K_TO_E,25),1.595167315406,1e-12,'the adjustable pair T pinned (derive)');
  rel(ljK(350,100*K_TO_E),387.87095586792,1e-12,'the adjustable pair spring (derive)');

  /* ---------- F. the turning points are exact ---------- */
  [-0.999,-0.99,-0.9,-0.5,-0.2,-0.05,-0.01].forEach(f=>{
    const E=f*EPS, tp=turningPoints(E,SIG,EPS);
    const uIn=Math.pow(SIG/tp.rIn,6), uOut=Math.pow(SIG/tp.rOut,6);
    rel(uIn+uOut,1,1e-13,'u_in + u_out = 1 at E/eps = '+f);
    rel(ljV(tp.rIn,SIG,EPS),E,1e-11,'V(r_in) = E at E/eps = '+f);
    rel(ljV(tp.rOut,SIG,EPS),E,1e-11,'V(r_out) = E at E/eps = '+f);
    ok(tp.rIn<rMin(SIG)&&tp.rOut>rMin(SIG),'the minimum lies between them at E/eps = '+f);
  });
  { const tp=turningPoints(-0.5*EPS,SIG,EPS);
    rel(tp.rIn,316.236698879,1e-10,'r_in at E = -eps/2 (derive)');
    rel(tp.rOut,424.232721428,1e-10,'r_out at E = -eps/2 (derive)'); }
  ok(!isFinite(turningPoints(0,SIG,EPS).rOut),'E = 0 has no outer turning point');
  ok(!isFinite(turningPoints(0.3*EPS,SIG,EPS).rOut),'E > 0 is unbound');
  eq(turningPoints(-1.4*EPS,SIG,EPS),null,'E < -eps is below the floor of the well');
  rel(turningPoints(-EPS,SIG,EPS).rIn,rMin(SIG),1e-12,'at E = -eps the two turning points meet at r_min');

  /* ---------- G. the period, by three routes ---------- */
  const MU=ATOM.Ne.m;
  /* NOTE: these are the REGULARISED quadrature's values.  The first version of
     this list was copied from an earlier run of derive.py that still used the
     naive E - V(r) integrand, and three of the seven then disagreed with the
     JS by 1e-11..1e-9 — the pins were stale, not the code. */
  const TPINS=[[-0.999,2.10915909198],[-0.99,2.12125708],[-0.9,2.25308369421],
               [-0.5,3.27484251461],[-0.2,5.90660985954],[-0.05,14.5995112689],
               [-0.01,42.2479150864]];
  TPINS.forEach(([f,T])=>{
    rel(periodQuad(f*EPS,SIG,EPS,MU),T,1e-11,'the period at E/eps = '+f+' (derive)');
  });
  /* the quadrature has converged at the panel count the sim uses */
  [-0.9,-0.5,-0.05].forEach(f=>{
    rel(periodQuad(f*EPS,SIG,EPS,MU,96),periodQuad(f*EPS,SIG,EPS,MU,400),1e-12,
        'periodQuad has converged by n = 96 at E/eps = '+f);
  });
  /* the regularisation is load-bearing: the naive integrand is WORSE, and by how much */
  { const E=ljV(rMin(SIG)+0.002,SIG,EPS);
    const a=periodQuad(E,SIG,EPS,MU), b=periodQuadNaive(E,SIG,EPS,MU);
    ok(Math.abs(b-a)/a>1e-5,'the naive E - V(r) integrand is visibly wrong at a = 0.002 pm ['
       +(Math.abs(b-a)/a).toExponential(2)+']');
    const E2=ljV(rMin(SIG)+8,SIG,EPS);
    rel(periodQuadNaive(E2,SIG,EPS,MU),periodQuad(E2,SIG,EPS,MU),1e-8,
        '...and agrees with it at a = 7.4 pm, so the difference really is cancellation'); }
  /* the integrated motion reproduces the quadrature */
  [1,10,40].forEach(A=>{
    const r0=rMin(SIG)+A, E=ljV(r0,SIG,EPS);
    const Tq=periodQuad(E,SIG,EPS,MU);
    rel(periodFromMotion(r0,SIG,EPS,MU,Tq/8000,60000),Tq,5e-7,
        'velocity Verlet reproduces the quadrature period at A = '+A+' pm');
  });
  /* the small-amplitude limit, and Landau's RATE of approach to it */
  eq(ANHARM_C,91/4,"Landau's coefficient for the LJ well is 91/4");
  const TH=ljPeriod(SIG,EPS,MU);
  [0.03125,0.125,0.5,2].forEach(A=>{
    const E=ljV(rMin(SIG)+A,SIG,EPS), tp=turningPoints(E,SIG,EPS);
    const a=0.5*(tp.rOut-tp.rIn);
    const meas=periodQuad(E,SIG,EPS,MU)/TH-1, pred=ANHARM_C*a*a/(rMin(SIG)*rMin(SIG));
    rel(meas,pred,A<1?2e-5:3e-4,'T(a)/T0 - 1 follows (91/4) a^2/r_min^2 at A = '+A+' pm');
  });
  { /* halving the amplitude quarters the excess: the rate, not the destination */
    const ex=A=>periodQuad(ljV(rMin(SIG)+A,SIG,EPS),SIG,EPS,MU)/TH-1;
    rel(ex(0.25)/ex(0.125),4,3e-3,'halving the amplitude quarters the period excess');
    rel(ex(0.125)/ex(0.0625),4,2e-3,'...and closer in, closer to four');
    ok(ex(0.0625)>0&&ex(2)>ex(0.0625),'the anharmonic shift is positive and grows'); }
  rel(periodQuad(ljV(rMin(SIG)+1,SIG,EPS),SIG,EPS,MU),2.10821924822,1e-11,
      'the period at A = 1 pm (derive)');
  withState({view:'small',amp:1},()=>{
    /* off the BUILT model, which is what the readout and the panel print —
       a test that re-types the formula tests nothing (drum_head Known-bad) */
    const S=buildModel().SM;
    rel(S.aNow,0.9900768681,1e-9,'smallModel amplitude a at A = 1 pm (derive)');
    rel(S.Tnow,2.10821924822,1e-10,'smallModel period at A = 1 pm (derive)');
    rel(S.predNow,ANHARM_C*S.aNow*S.aNow/(rMin(SIG)*rMin(SIG)),1e-14,
        'and the prediction it draws is (91/4) a^2/r_min^2');
    rel(S.Tnow/ljPeriod(SIG,EPS,MU)-1,S.predNow,1e-5,'which the measurement follows');
    ok(S.as.length>20&&S.ex.length===S.as.length&&S.pred.length===S.as.length,
       'and the swept curve has a prediction for every measured point');
    ok(S.as.every(isFinite)&&S.ex.every(isFinite)&&S.pred.every(isFinite),
       'all of them finite');
  });
  rel(periodQuad(ljV(rMin(SIG)+10,SIG,EPS),SIG,EPS,MU),2.1414520080684,2e-10,
      'the period at A = 10 pm (derive)');

  /* ---------- H. the integrators ---------- */
  const R0=rMin(SIG)+10, TP=periodQuad(ljV(R0,SIG,EPS),SIG,EPS,MU);
  const EXPECT={verlet:[8.11049e-7,2.02765e-7,5.06914e-8,1.26728e-8,3.16821e-9],
                symplectic:[1.67796e-4,8.36969e-5,4.17993e-5,2.08872e-5,1.04405e-5],
                forward:[1.92566e-3,9.456e-4,4.68262e-4,2.33081e-4,1.1627e-4]};
  const ORD={verlet:1.99999,symplectic:1.00161,forward:1.01245};
  ['verlet','symplectic','forward'].forEach(k=>{
    const es=DT_LIST.map(dt=>energyExcursion(R0,0,SIG,EPS,MU,dt,Math.round(TP/dt),k).worst);
    es.forEach((v,i)=>rel(v,EXPECT[k][i],2e-4,k+' energy excursion at dt = '+DT_LIST[i]+' (derive)'));
    const p=Math.log(es[0]/es[es.length-1])/Math.log(DT_LIST[0]/DT_LIST[DT_LIST.length-1]);
    rel(p,ORD[k],1e-3,k+' measured order (derive)');
  });
  { const es=DT_LIST.map(dt=>energyExcursion(R0,0,SIG,EPS,MU,dt,Math.round(TP/dt),'verlet').worst);
    for(let i=0;i<es.length-1;i++) rel(es[i]/es[i+1],4,1e-3,'Verlet: halving dt quarters the error ('+i+')'); }
  /* boundedness: the symplectic pair do not grow, forward Euler does */
  { const n1=Math.round(TP/1e-3), n20=Math.round(20*TP/1e-3);
    ['verlet','symplectic'].forEach(k=>{
      const a=energyExcursion(R0,0,SIG,EPS,MU,1e-3,n1,k).worst;
      const b=energyExcursion(R0,0,SIG,EPS,MU,1e-3,n20,k).worst;
      /* 1e-5, not 0: the two runs are not the same number of steps (each is
         round(n x T/dt) for a different n), so the sampled maximum of a
         bounded oscillation differs in the seventh digit. */
      rel(b/a,1,1e-5,k+' is symplectic: 20 periods cost no more than one'); });
    const a=energyExcursion(R0,0,SIG,EPS,MU,1e-3,n1,'forward').worst;
    const b=energyExcursion(R0,0,SIG,EPS,MU,1e-3,n20,'forward').worst;
    ok(b/a>20,'forward Euler is not: 20 periods cost '+fmt(b/a,1)+' times as much');
    rel(b,0.011237178,2e-4,'forward Euler after 20 periods (derive)');
    rel(energyExcursion(R0,0,SIG,EPS,MU,1e-3,n20,'verlet').worst,5.0691432e-8,2e-4,
        'velocity Verlet after 20 periods (derive)'); }
  /* a whole trajectory pinned, not just a summary */
  { const s=ljState(R0,0,SIG,EPS,MU);
    for(let i=0;i<1000;i++) stepVerlet(s,SIG,EPS,MU,1e-3);
    rel(s.r,337.64191225235,1e-9,'r after 1000 Verlet steps of 1 fs (derive)');
    rel(s.v,-6.6712289406425,1e-8,'v after 1000 Verlet steps (derive)');
    rel(ljV(R0,SIG,EPS),-290297.08444232,1e-12,'E(0) of that run (derive)');
    rel(s.t,1,1e-12,'the clock reads 1.000 ps'); }
  /* the steppers are distinguishable: identical code would be an equivalent mutant */
  { const a=ljState(R0,0,SIG,EPS,MU), b=ljState(R0,0,SIG,EPS,MU), c=ljState(R0,0,SIG,EPS,MU);
    for(let i=0;i<200;i++){ stepVerlet(a,SIG,EPS,MU,4e-3); stepSymplecticEuler(b,SIG,EPS,MU,4e-3);
      stepForwardEuler(c,SIG,EPS,MU,4e-3); }
    ok(Math.abs(a.r-b.r)>1e-3&&Math.abs(a.r-c.r)>1e-3&&Math.abs(b.r-c.r)>1e-3,
       'the three steppers really are three different schemes'); }

  { /* the step ceiling is applied, not merely computed */
    const a=energyExcursion(R0,0,SIG,EPS,MU,1e-3,4*MAX_STEPS,'verlet');
    ok(isFinite(a.worst)&&Math.abs(a.s.t-MAX_STEPS*1e-3)<1e-3,
       'a step count past the ceiling is clamped to it, not run ('+fmt(a.s.t,0)+' ps)');
    const b=energyExcursion(R0,0,SIG,EPS,MU,1e-3,Infinity,'verlet');
    eq(b.s.t,0,'and an infinite one runs nothing at all');
    /* and the integrator view survives a pair with no bound orbit at r_min+10 */
    withState({view:'steppers',pair:'Adj'},()=>{
      setAdjSig(ST,500); setAdjEps(ST,20);
      let M=null; try{ M=buildModel(); }catch(e){ M=null; }
      ok(M&&isFinite(M.IT.T)&&M.IT.drift.verlet.ds.length>0,
         'the integrator view builds for every adjustable setting');
    }); }

  /* ---------- I. escape ---------- */
  rel(escapeSpeed(R0,SIG,EPS,MU),169.62075114575,1e-11,'the escape speed at r_min + 10 pm (derive)');
  eq(escapeSpeed(0.9*SIG,SIG,EPS,MU),0,'inside sigma V > 0: nothing to escape from');
  { const s=ljState(R0,1.02*escapeSpeed(R0,SIG,EPS,MU),SIG,EPS,MU);
    const E=ljEnergy(s,SIG,EPS,MU);
    rel(E/EPS,0.039400962217962,1e-9,'E at 1.02 of the escape speed (derive)');
    for(let i=0;i<20000;i++) stepVerlet(s,SIG,EPS,MU,1e-3);
    rel(s.r,1262.4307898947,1e-6,'r after 20 ps of escape (derive)');
    rel(s.v,34.456637770434,1e-6,'v after 20 ps (derive)');
    ok(s.v>Math.sqrt(2*E/MU),'and it is still slowing toward its speed at infinity'); }
  { const s=ljState(R0,0.98*escapeSpeed(R0,SIG,EPS,MU),SIG,EPS,MU);
    ok(ljEnergy(s,SIG,EPS,MU)<0,'just below the escape speed the pair stays bound');
    const tp=turningPoints(ljEnergy(s,SIG,EPS,MU),SIG,EPS);
    rel(ljEnergy(s,SIG,EPS,MU)/EPS,-0.038620745144339261,1e-9,
        'E at 0.98 of the escape speed (derive)');
    rel(tp.rOut,666.36891572402988,1e-8,'...and the outer turning point is 666 pm (derive)');
    ok(tp.rOut>1.9*rMin(SIG),'which is nearly twice r_min: the well is very shallow there'); }

  /* ---------- J. PhET against the literature ---------- */
  LIT_RMIN_TABLE.forEach(([nm,s,rm])=>{
    close(rm/s,SIXRT2,4e-4,'the source table’s own r_min/sigma is 2^(1/6) for '+nm);
  });
  rel(PAIR_BY_KEY.NeNe.sig/LIT.Ne.rmin-1,-0.016288725646758317,1e-13,
      "PhET's neon sigma is the literature r_min to 1.6% (derive)");
  rel(PAIR_BY_KEY.NeNe.sig/LIT.Ne.sig-1,0.10433847257081408,1e-13,
      "...and is 10.4% from the literature sigma (derive)");
  rel(PAIR_BY_KEY.ArAr.sig/LIT.Ar.rmin-1,-0.020067761271826967,1e-13,
      "PhET's argon sigma is the literature r_min to 2.0% (derive)");
  rel(PAIR_BY_KEY.ArAr.sig/LIT.Ar.sig-1,0.10005851375073149,1e-13,
      "...and is 10.0% from the literature sigma (derive)");
  ok(Math.abs(PAIR_BY_KEY.OO.sig/LIT.O.sig-1)>0.4&&Math.abs(PAIR_BY_KEY.OO.eps/LIT.O.eps-1)>7,
     "PhET's oxygen pair matches neither the literature sigma nor its eps");
  ok(Math.abs(PHET_SOM.epsO2/LIT.O.eps-1)<1e-12,
     "...while PhET's OWN States-of-Matter constant for O2 IS the literature 113 K");
  { const lb=lorentzBerthelot(PAIR_BY_KEY.NeNe,PAIR_BY_KEY.ArAr);
    rel(lb.sig,342,1e-12,'Lorentz on PhET’s like pairs gives 342 pm for Ne-Ar');
    rel(lb.eps,63.276156646876082,1e-13,'Berthelot gives 63.2762 K (derive)');
    close(PAIR_BY_KEY.NeAr.sig,lb.sig,1.5,"PhET's Ne-Ar sigma follows the Lorentz rule");
    rel(PAIR_BY_KEY.NeAr.eps/lb.eps-1,-0.059677402152434778,1e-12,
        "...but its eps is 5.97% below Berthelot's (derive)");
    const lbO=lorentzBerthelot(PAIR_BY_KEY.NeNe,PAIR_BY_KEY.OO);
    ok(Math.abs(PAIR_BY_KEY.NeO.sig/lbO.sig-1)>0.15,
       "and the oxygen rows cannot follow it: PhET uses r(Ne)+r(O), not the sigma mean"); }
  /* the literature mixed pairs the sim actually builds */
  { const p=pairParams('NeAr',true,{sig:350,eps:100});
    rel(p.sig,310.35,1e-12,'literature Ne-Ar sigma by Lorentz (derive)');
    rel(p.eps,66.53420173028024,1e-10,'literature Ne-Ar eps by Berthelot (derive)'); }
  { const p=pairParams('Adj',true,{sig:265,eps:230});
    eq(p.sig,265,'the adjustable pair ignores the literature switch (sigma)');
    eq(p.eps,230,'...and its epsilon'); }
  /* corresponding states, computed rather than remembered */
  { const R=pairsModel(DEFAULTS);
    rel(R.cs[0].ratio,1.2605042016806722,1e-14,'kT_c/eps for neon, from PhET T_c and the literature eps (derive)');
    rel(R.csMean,1.2833091843645823,1e-13,'the mean kT_c/eps (derive)');
    rel(R.csSpread,0.11995509914592721,1e-13,'and its spread (derive)');
    ok(R.csSpread<0.2,'the three cluster: that IS the law of corresponding states'); }

  /* ---------- J2. the drawn r window, and every other constant that used
     to be asserted against ITSELF ----------------------------------------
     The mutation sweep walked R_LO_FAC from 0.72 to 0.50 and the whole suite
     stayed green, because every assertion that touched the window was written
     as `R_LO_FAC * sigma` — in terms of the very constant under test.  A test
     that re-derives the thing it is testing tests nothing (drum_head
     Known-bad).  The mutant is NOT equivalent: it moves the inward end of a
     drag from 221.76 pm to 154.00 pm for neon, where the wall the atom is
     pushed against goes from 177 eps to 16128 eps.  It is invisible only to
     the PICTURE, for the reason asserted at the end of this block. */
  const WIN=[['NeNe',308,221.75999999999999,985.60000000000002],
             ['ArAr',376,270.71999999999997,1203.2],
             ['OO',200,144,640],
             ['NeAr',343,246.95999999999998,1097.6000000000001],
             ['NeO',306,220.31999999999999,979.20000000000005],
             ['ArO',340,244.79999999999998,1088],
             ['Adj',350,252,1120]];
  WIN.forEach(([key,sg,lo,hi])=>{
    withState({pair:key},()=>{
      const P=pairInfo(ST);
      eq(P.sig,sg,key+': sigma is '+sg+' pm');
      rel(P.rLo,lo,1e-14,key+': the drawn window floor is '+lo+' pm (derive)');
      rel(P.rHi,hi,1e-14,key+': and its ceiling is '+hi+' pm (derive)');
      /* the drag lands exactly on each end — pinned absolutely, not as a
         product of the constant that decides where the end is */
      setSep(ST,1);   rel(ST.r,lo,1e-12,key+': an inward drag stops exactly on the floor');
      setSep(ST,1e9); rel(ST.r,hi,1e-12,key+': and an outward one exactly on the ceiling');
    });
  });
  /* the floor is where it is for the WALL it puts the atom against: steep
     enough to read as a wall, finite enough to plot.  That is the only reason
     0.72 is 0.72, so it is what gets pinned. */
  rel(ljV(0.72*SIG,SIG,EPS)/EPS,177.38412001633412,1e-12,
      'V at the window floor is 177.384 eps (derive)');
  rel(ljV(0.50*SIG,SIG,EPS)/EPS,16128,1e-12,
      '...and 16128 eps at half a sigma, 91 times deeper (derive)');
  /* what is DRAWN spans exactly the window */
  withState({view:'atoms'},()=>{
    const M=buildModel(), P=M.P, C=M.C, n=C.xs.length;
    eq(n,261,'the two-atoms curve is sampled at 261 points');
    rel(C.xs[0],P.rLo,1e-15,'its first sample is the window floor');
    rel(C.xs[n-1],P.rHi,1e-15,'and its last is the ceiling');
    rel(C.xs[0],221.75999999999999,1e-14,'in picometres, 221.76 (derive)');
    rel(C.xs[n-1],985.60000000000002,1e-14,'and 985.6 (derive)');
    rel(C.xs[1]-C.xs[0],(P.rHi-P.rLo)/260,1e-12,'evenly spaced across it');
    rel(C.ys[0],ljV(P.rLo,P.sig,P.eps)/P.eps,1e-15,'with V evaluated at each sample');
  });
  { /* THE INVARIANCE, asserted deliberately rather than left as a blind spot:
       the box runs to V/eps = 2.4, which the curve reaches at r = 0.943016
       sigma, so every sample below that is clipped away by polyline and the
       window FLOOR moves no pixel.  Measured in _out/probe_window.py: with the
       floor at 0.50 sigma, six of the eight captured views hash identically
       and the two two-atoms views differ only in sample placement.  The floor
       is a DRAG contract, not a drawing contract — which is why no picture
       check could have caught the mutant and why the pins above are on the
       drag. */
    const u=(4+Math.sqrt(16+4*4*2.4))/8, rc=Math.pow(u,-1/6);
    rel(u,1.4219544457292888,1e-14,'u at the top of the plot box (derive)');
    rel(rc,0.94301598124699082,1e-14,'the curve leaves the box at 0.943016 sigma (derive)');
    rel(ljV(rc*SIG,SIG,EPS)/EPS,2.4,1e-12,'where V/eps is exactly the box ceiling');
    ok(R_LO_FAC<rc,'the window floor lies inside the clipped region, so it draws nothing');
    ok(0.50<rc,'and so does the mutant floor, which is why the picture cannot tell them apart'); }
  /* and the floor is reachable ONLY by dragging: no slider setting goes near it */
  WIN.forEach(([key,sg,lo,hi])=>{
    withState({view:'motion',pair:key},()=>{
      let least=Infinity;
      for(let q=-20;q<=120;q+=2){ ST.rel=q; releaseAtom(ST); least=Math.min(least,ST.r); }
      ok(least>lo+40,key+': no release setting comes within 40 pm of the floor ('
         +fmt(least,1)+' vs '+fmt(lo,1)+')');
    });
  });
  /* The same shape, everywhere else it could hide: a constant that appears in
     its own assertion needs one ABSOLUTE pin as well, or its mutant is free. */
  eq(MAX_STEPS,6e5,"the integrator's step ceiling is 600000");
  ok(MAX_STEPS>20*periodQuad(ljV(rMin(500),500,20*K_TO_E),500,20*K_TO_E,25)/1e-3,
     'which is above the longest run any view asks for');
  eq(PS_PER_SEC,2,'the clock runs 2 ps of model time per second');
  eq(SLOW_FACTOR,0.35,"and PhET's slow switch takes it to 0.35 of that");
  eq(DT_INT,1.5e-3,'the integrator substeps at 1.5 fs');
  ok(DT_INT<0.02*ljPeriod(200,1000*K_TO_E,ATOM.O.m),
     'which is under 2% of the shortest period the pairs reach');
  eq(TRAIL_MAX,900,'the trail keeps at most 900 samples');
  eq(R_LO_FAC,0.72,'the window runs from 0.72 sigma');
  eq(R_HI_FAC,3.2,'to 3.2 sigma');

  /* ---------- K. the state machine ---------- */
  withState({},()=>{
    rel(ST.r,rMin(308),1e-12,'the sim opens with the atom at r_min');
    eq(ST.forces,'hidden',"and with the forces hidden, as PhET's model does");
    eq(ST.pair,'NeNe',"and on PhET's default pair");
    setPair(ST,'ArAr'); rel(ST.r,rMin(376),1e-12,'changing the pair returns the atom to the new r_min');
    setSep(ST,500); eq(ST.v,0,'dragging stops the atom');
    returnAtom(ST); rel(ST.r,rMin(376),1e-12,'Return Atom puts it back');
    ok(!ST.running,'...and stops the clock');
    setSep(ST,1e6); rel(ST.r,1203.2,1e-12,'the drag is clamped outward, at 1203.2 pm (derive)');
    setSep(ST,1); rel(ST.r,270.71999999999997,1e-12,'and inward, at 270.72 pm (derive)');
    setAdjSig(ST,333); eq(ST.adjSig,335,"the diameter slider snaps to PhET's 5 pm");
    setAdjSig(ST,9); eq(ST.adjSig,PHET_MIN_SIGMA,"and clamps at PhET's MIN_SIGMA");
    setAdjSig(ST,9999); eq(ST.adjSig,PHET_MAX_SIGMA,'and at MAX_SIGMA');
    setAdjEps(ST,333); eq(ST.adjEps,335,'the strength slider snaps to 5 K');
    setAdjEps(ST,1); eq(ST.adjEps,PHET_MIN_EPSILON,'and clamps at MIN_EPSILON');
    setAdjEps(ST,9999); eq(ST.adjEps,PHET_MAX_EPSILON,'and at MAX_EPSILON');
    ST.pair='Adj'; setAdjSig(ST,420); rel(ST.r,rMin(420),1e-12,
      'moving the diameter while the adjustable pair is live returns the atom to the new minimum');
    setPinned(ST,false);
    rel(pairInfo(ST).mu,12.5,1e-12,'unpinning halves the effective mass of a like pair');
  });
  withState({pair:'NeAr'},()=>{
    const P=pairInfo(ST);
    eq(P.mu,ATOM.Ar.m,'pinned neon-argon: the argon moves, so mu is 39.948 u');
    setPinned(ST,false);
    rel(pairInfo(ST).mu,13.407109462028314,1e-14,'free neon-argon: mu = m1m2/(m1+m2) (derive)');
  });
  withState({},()=>{
    ST.rel=10; ST.v0f=0; releaseAtom(ST);
    rel(ST.r,rMin(308)+10,1e-12,'release puts it 10 pm outside the minimum');
    eq(ST.v,0,'at rest'); ok(ST.running,'and running');
    ST.v0f=1; releaseAtom(ST);
    rel(ST.v,escapeSpeed(ST.r,pairInfo(ST).sig,pairInfo(ST).eps,pairInfo(ST).mu),1e-12,
        'launch speed 1.0 is exactly the escape speed');
    close(liveModel(ST).E,0,1e-6*pairInfo(ST).eps,'...so E = 0');
    ok(!liveModel(ST).bound,'and the pair is unbound');
  });

  /* ---------- L. the frame loop moves the atom ---------- */
  { const S=makeScene({getContext:()=>makeShot(1100,700)});
    withState({},()=>{
      ST.rel=10; ST.v0f=0; releaseAtom(ST);
      const r0=ST.r, E0=liveModel(ST).E;
      for(let i=0;i<30;i++) S.step();
      ok(Math.abs(ST.r-r0)>0.5,'thirty frames move the atom measurably');
      ok(ST.t>0,'and advance the clock');
      rel(liveModel(ST).E,E0,1e-6,'while the energy holds to a part in 10^6');
      ok(TRAIL.length===30,'and every frame is recorded once');
      ST.running=false;
      const rr=ST.r; for(let i=0;i<10;i++) S.step();
      eq(ST.r,rr,'paused, the frame loop does not move it');
    });
    withState({},()=>{
      /* the trail cap bites, and at the number it claims: an uncapped trail is
         an unbounded array behind a view that only ever shows a few periods */
      ST.rel=10; ST.v0f=0; releaseAtom(ST);
      for(let i=0;i<TRAIL_MAX-1;i++) S.step();
      eq(TRAIL.length,TRAIL_MAX-1,'the trail grows one sample a frame');
      for(let i=0;i<60;i++) S.step();
      eq(TRAIL.length,TRAIL_MAX,'and stops growing at exactly 900');
      ok(TRAIL[TRAIL.length-1][0]>TRAIL[0][0],'keeping the most recent samples');
    });
    withState({},()=>{
      ST.rel=10; ST.v0f=0; releaseAtom(ST); ST.slow=true;
      for(let i=0;i<20;i++) S.step();
      const tSlow=ST.t;
      ST.rel=10; releaseAtom(ST); ST.slow=false;
      for(let i=0;i<20;i++) S.step();
      rel(tSlow/ST.t,SLOW_FACTOR,1e-9,'the slow switch really slows the clock');
    });
    withState({pair:'NeNe'},()=>{
      /* the integrated period matches the quadrature through the REAL loop */
      ST.rel=1; ST.v0f=0; releaseAtom(ST);
      const T=liveModel(ST).period;
      let prev2=null,prev1=null; const hits=[];
      for(let i=0;i<4000&&hits.length<2;i++){
        S.step();
        if(prev2!==null&&prev1>prev2&&prev1>=ST.r) hits.push(ST.t);
        prev2=prev1; prev1=ST.r;
      }
      ok(hits.length===2,'the frame loop completes two oscillations');
      if(hits.length===2) rel(hits[1]-hits[0],T,0.02,
        'and their spacing is the quadrature period to 2% at one frame of resolution');
    });
  }

  /* ---------- M. every panel builds clean, every view x pair x toggle ---------- */
  { let bad=null;
    for(const p of PAIRS) for(const lit of [false,true]) for(const pin of [false,true])
      for(const f of ['hidden','total','components']) for(const v of TABS.map(t=>t[0])){
        withState({view:v,pair:p.key,lit,pinned:pin,forces:f},()=>{
          if(bad) return;
          let M; try{ M=buildModel(); }catch(e){ bad=v+'/'+p.key+': '+e; return; }
          const html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M)+(INFO[v]||'');
          if(/NaN|undefined|Infinity/.test(html)) bad=v+'/'+p.key+'/'+f+(lit?'/lit':'')+': '+
            html.slice(Math.max(0,html.search(/NaN|undefined|Infinity/)-40),html.search(/NaN|undefined|Infinity/)+40);
          if(!/\d/.test(html)) bad=v+'/'+p.key+': no numbers at all';
        });
        if(bad) break;
      }
    ok(!bad,'every view x pair x literature x pinned x forces builds clean ('+(bad||'ok')+')');
  }
  { /* the readout names a number no other row can supply, so containment is not vacuous */
    withState({view:'well',pair:'NeNe'},()=>{
      const s=readoutHTML(buildModel());
      ok(s.indexOf('345.718')>=0,'the readout prints neon’s r_min to six figures');
      ok(s.indexOf('383.29')>=0,'and the separation of strongest pull'); });
    withState({view:'small',pair:'ArAr'},()=>{
      const s=readoutHTML(buildModel());
      ok(s.indexOf('2.04835')>=0,'the small-oscillation readout prints argon’s period'); });
  }
  { /* no slider combination produces a non-finite model */
    let bad=null;
    for(let i=0;i<=8&&!bad;i++) for(let j=0;j<=8&&!bad;j++){
      const sg=PHET_MIN_SIGMA+(PHET_MAX_SIGMA-PHET_MIN_SIGMA)*i/8;
      const ep=PHET_MIN_EPSILON+(PHET_MAX_EPSILON-PHET_MIN_EPSILON)*j/8;
      withState({view:'small',pair:'Adj'},()=>{
        setAdjSig(ST,sg); setAdjEps(ST,ep);
        for(const A of [0.05,1,10,60]){
          ST.amp=A;
          const M=buildModel();
          const vals=[M.P.k,M.P.omega,M.P.period,M.SM.aNow,M.SM.Tnow,M.SM.predNow];
          if(vals.some(v=>!isFinite(v))) bad='sigma '+sg+' eps '+ep+' A '+A;
        }
      });
    }
    ok(!bad,'no adjustable slider pair makes a non-finite model ('+(bad||'ok')+')');
  }
  { /* nor any release offset or launch speed */
    let bad=null;
    for(let i=0;i<=10&&!bad;i++) for(let j=0;j<=6&&!bad;j++){
      withState({view:'motion'},()=>{
        ST.rel=-20+140*i/10; ST.v0f=1.4*j/6; releaseAtom(ST);
        const M=buildModel();
        if(![M.L.E,M.L.K,M.L.V,M.L.vEsc].every(isFinite)) bad='rel '+ST.rel+' v0f '+ST.v0f;
        if(M.L.bound&&!isFinite(M.L.period)) bad='bound but no period at rel '+ST.rel;
      });
    }
    ok(!bad,'no release setting makes a non-finite model ('+(bad||'ok')+')');
  }

  /* ---------- N. the drag ---------- */
  { const S=makeScene({getContext:()=>makeShot(1100,700)});
    /* the scene's own W and H, not a pair of literals: the band height, and
       therefore the drawn atom radius and therefore the axis origin, depend on
       the stage height, so a geometry built at a different H maps r elsewhere */
    S.W=1100; S.H=700;
    withState({view:'atoms'},()=>{
      const ctx=makeShot(S.W,S.H), M=buildModel(), G=atomsGeom(ctx,S.W,S.H,M);
      const X=G.X(ST.r);
      ok(S.pointer('down',X,G.band.cy),'the movable atom grabs at its centre');
      eq(DRAG.what,'atom','and it is the atom');
      S.pointer('move',X+40,G.band.cy);
      rel(ST.r,G.wx(X+40),1e-9,'and follows the pointer exactly');
      S.pointer('up',0,0); eq(DRAG.what,null,'and lets go');
      ok(!S.pointer('down',G.X(0),G.band.cy)||DRAG.what===null,
         'the PINNED atom does not grab');
      S.pointer('up',0,0);
      ok(!S.pointer('down',G.band.x+4,G.band.y+3),'empty stage grabs nothing');
      S.pointer('up',0,0);
      /* dragging past the ends clamps rather than escaping */
      S.pointer('down',G.X(ST.r),G.band.cy); S.pointer('move',G.b.x1+900,G.band.cy);
      rel(ST.r,985.60000000000002,1e-12,'dragged far right it stops at 985.6 pm (derive)');
      S.pointer('up',0,0);
      /* the drag stops the clock, as PhET's setMotionPaused does */
      ST.running=true; S.pointer('down',G.X(ST.r),G.band.cy);
      ok(!ST.running,'grabbing the atom pauses the motion, as PhET does');
      S.pointer('up',0,0);
    });
    ['well','motion','small','pairs','steppers'].forEach(v=>{
      withState({view:v},()=>{ ok(!S.pointer('down',400,300),'the '+v+' view ignores the pointer');
        S.pointer('up',0,0); });
    });
  }

  { /* a sparse view must SAY why it is sparse, not merely be sparse */
    withState({view:'motion'},()=>{
      const c=makeShot(1100,700); drawView(c,1100,700,buildModel());
      const t=c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' | ');
      ok(t.indexOf('press release')>=0,'a fresh motion view says how to start it');
      ok(t.indexOf('nothing released yet')>=0,'and its ledger says why it is empty');
    });
    withState({view:'motion',r:400,v:400},()=>{
      const c=makeShot(1100,700); drawView(c,1100,700,buildModel());
      const t=c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' | ');
      /* the LEGEND entry, not the word: the caption legitimately explains what
         turning points are even when this orbit has none */
      ok(t.indexOf('turning points (exact)')<0,'an unbound release names no turning points in its legend');
      ok(t.indexOf('this orbit (closed)')<0,'...and no closed orbit in the phase portrait');
      ok(t.indexOf('unbound')>=0,'and says the pair is unbound');
    }); }

  /* ---------- O. layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['atoms default',{view:'atoms'},8],
    ['atoms total',{view:'atoms',forces:'total'},8],
    ['atoms components',{view:'atoms',forces:'components'},8],
    ['atoms close',{view:'atoms',forces:'components',r:270},8],
    ['atoms far',{view:'atoms',forces:'total',r:900},8],
    ['atoms argon',{view:'atoms',pair:'ArAr',forces:'total'},8],
    ['atoms oxygen',{view:'atoms',pair:'OO',r:224.5},8],
    ['atoms adjustable',{view:'atoms',pair:'Adj',forces:'components',r:392.9},8],
    ['atoms free',{view:'atoms',pinned:false},8],
    ['atoms literature',{view:'atoms',lit:true,forces:'total'},8],
    ['well default',{view:'well'},5],
    ['well components',{view:'well',forces:'components'},5],
    ['well oxygen',{view:'well',pair:'OO'},5],
    ['well adjustable small',{view:'well',pair:'Adj',adjSig:75,adjEps:20,r:100},5],
    ['well adjustable big',{view:'well',pair:'Adj',adjSig:500,adjEps:450,r:560},5],
    /* an untouched motion view legitimately draws the background, one marker
       and two sentences saying nothing has been released: floor what it emits,
       and assert the sentences separately below (pulsar Known-bad) */
    ['motion fresh',{view:'motion'},2],
    ['motion argon',{view:'motion',pair:'ArAr'},2],
    ['motion unbound',{view:'motion',r:400,v:400},4],
    ['motion free',{view:'motion',pinned:false},2],
    /* the small-oscillation view is nearly all strokes: two curves, a rule and
       four markers, so its fill floor is what it emits, not what a filled view
       emits (pascals_triangle Known-bad) */
    ['small default',{view:'small'},3],
    ['small tiny',{view:'small',amp:0.05},3],
    ['small wide',{view:'small',amp:60},3],
    ['small oxygen',{view:'small',pair:'OO',amp:5},3],
    ['small free lit',{view:'small',pinned:false,lit:true,pair:'ArAr'},3],
    ['pairs default',{view:'pairs'},8],
    ['pairs no overlay',{view:'pairs',showLit:false},8],
    /* on a narrow stage this view drops its dt panel and draws one: the floor
       is the background plus the three curve-end dots */
    ['steppers default',{view:'steppers'},4],
    ['steppers argon',{view:'steppers',pair:'ArAr'},4],
    ['steppers adjustable',{view:'steppers',pair:'Adj',adjSig:200,adjEps:300},4],
  ];
  layoutSweep(ok,withState,CONFIGS,SIZES);

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
