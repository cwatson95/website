
/* ================================================================== *
 *  selfTest — headless verification (runs when there is no document)  *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T={ok,eq,close,rel}, T0=Date.now();
  const stSave=Object.assign({},ST);
  /* the memo is NOT cleared: every memo key carries all of its inputs (the
     functions are pure), and clearing it made the layout sweep recompute
     2.5 M seeded draws per binomial drawing (18 s under osascript) */
  function fresh(over){ Object.assign(ST,DEFAULTS,over||{}); resetScenes(); resetCam(); }
  function withState(over,fn){ fresh(over); try{ return fn(); } finally{ fresh(stSave); } }

  engineTests(T);

  /* ---------- A. PhET's values ---------- */
  eq(FLIP_T,1,'a flip takes 1 s (PhET\'s value)'); eq(COIN_NS.join(','),'10,100,10000','10, 100 or 10 000 identical coins (PhET\'s value)'); eq(BIAS_STEP,0.05,'bias steps of 0.05 (PhET\'s value)');
  ok(PH.X0===-0.15&&PH.V===0.3&&PH.BEAM_W===0.04&&PH.PBS===0.035&&PH.MX===0.11&&PH.DV===0.2&&PH.DH===-0.09,'the photon bench: laser -0.15, 0.3/s, beam 0.04, splitter 0.07, mirror 0.11, detectors 0.2 and -0.09 (PhET\'s values)');
  ok(PH.AP===0.07&&PH.ABS===0.05&&PH.RATE_MAX===200&&PH.SLOW===0.4&&PH.CAP===999&&PH.AVG_T===1&&PH.AVG_S===0.5&&PH.CUSTOM_STEP===5,'aperture 1.75 x beam, absorber 0.05, 200/s, slow x0.4, cap 999, 1-s average in 0.5-s samples, 5-deg custom steps (PhET\'s values)');
  close(PH.STEP_DT,2/60,1e-17,'the step button advances 2/60 s (PhET\'s value)');
  ok(PRESET_ANG.vertical===90&&PRESET_ANG.horizontal===0&&PRESET_ANG.fortyFive===45,'presets V 90, H 0, 45 (PhET\'s values)');
  eq(SG_EXPS.map(e=>e.axes.join('')).join('|'),'z|x|zxx|zzz|xzz|xxx|xzz','the six experiments and the custom layout (PhET\'s values)');
  ok(SG_RATE===5*60&&SG_MAXP===1250&&SG_MAXP1===50&&SG_AVG_T===3,'5 x amount per 60-Hz frame, 1250 and 50 in flight, a 3-s average (PhET\'s values)');
  ok(BL.STEP===Math.PI/12&&BL.DELAY===0.75&&BL.DELAY_MAX===1&&BL.NS_PER_S===0.25&&BL.ATOMS===10,'15-deg steps, delay 0.75 of 0-1 ns, 0.25 ns per second, ten atoms (PhET\'s values)');
  ok(DEFAULTS.coinScene==='classical'&&DEFAULTS.phMode==='single'&&DEFAULTS.phPreset==='fortyFive'&&DEFAULTS.phCustom===45&&DEFAULTS.phBehavior==='classical','PhET\'s starts: classical coins, single photons at 45 deg, classical behaviour');
  ok(DEFAULTS.sgExp==='e1'&&DEFAULTS.sgMode==='single'&&DEFAULTS.sgSrc==='+Z'&&DEFAULTS.sgA2===1&&DEFAULTS.sgAmount===0.1&&DEFAULTS.sgBlock==='up'&&DEFAULTS.sgC1==='x'&&DEFAULTS.sgC2==='z','PhET\'s spin start: experiment 1, +Z, single, |alpha|^2 = 1, amount 0.1, block up, custom [x, z]');
  ok(DEFAULTS.bPreset==='+X'&&DEFAULTS.bTheta===Math.PI/2&&DEFAULTS.bPhi===0&&DEFAULTS.bAxis==='Z'&&DEFAULTS.bAtoms===1&&!DEFAULTS.bField&&DEFAULTS.bStrength===1,'PhET\'s Bloch start: +X, measured along z, one atom, no field (strength 1)');
  { const c=makeCoinScene('quantum',1); eq(c.p,0.5,'the quantum coin starts at bias 0.5'); eq(quantumInit(c.p),'superposition','so in a superposition (PhET)'); }

  /* ---------- B. photons ---------- */
  for(const [a,p,e] of [[0,0,-1],[30,0.24999999999999994,-0.5000000000000002],[45,0.4999999999999999,-2.220446049250313e-16],[60,0.7499999999999999,0.4999999999999998],
                        [90,1,1],[17.5,0.0904239778555041,-0.8191520442889919],[72.5,0.909576022144496,0.8191520442889919]]){
    close(pV(a),p,2e-16,'P(V) = sin^2 at '+a+' deg (derive)'); close(expectP(a),e,4e-16,'<P> = -cos 2 theta at '+a+' deg (derive)'); }
  for(const [y0,d1,arm] of [[-0.02,0.13,0.22],[-0.013,0.13699999999999998,0.21300000000000002],[0,0.15,0.2],[0.007,0.157,0.193],[0.02,0.16999999999999998,0.18000000000000002]]){
    const L=photonLegs(y0); close(L.d1,d1,1e-16,'to the splitter at y0 = '+y0+' (derive)'); close(L.arm,arm,1e-16,'the arm beyond it (derive)');
    close(L.d1+L.arm,0.35,1e-15,'splitter + arm = 0.35 at every height');
    const v=photonPos({y0},L.dArr,'V'), hh=photonPos({y0},L.dArr,'H'), mir=photonPos({y0},L.d1+PH.MX-2*y0,'H');
    close(v[1],PH.DV,1e-15,'the V arm ends on the V detector line'); close(hh[1],PH.DH,1e-15,'the H arm ends on the H detector line'); close(mir[0]+mir[1],PH.MX,1e-15,'the H arm turns on the mirror x + y = 0.11'); }
  rel(photonLegs(0.013).dArr/PH.V,1.1666666666666667,1e-15,'every photon arrives 1.167 s after leaving the laser (derive)');
  eq(photonBatch(99,30,5000),1236,'5000 photons at 30 deg: 1236 V (derive)'); ok(Math.abs(1236-1250)<4*Math.sqrt(5000*0.25*0.75),'within 4 sigma of 1250');
  eq(photonBatchUnpol(17,5000),2536,'5000 unpolarized photons: 2536 V (derive)'); ok(Math.abs(2536-2500)<4*35.35533905932738,'within 4 sigma of half (derive)');
  { const A=makeAvg(1,0.5); for(let f=1;f<=300;f++){ if(f%3===0) avgCount(A); avgStep(A,1/60); } eq(A.value,20.322580645161,'the averaging counter: 20 counts/s in 1/60-s frames reads 20.3226 (derive)'); }
  /* the live bench: one photon at a time, both behaviours, the same draws */
  const runPhotons=(beh,n)=>withState({view:'photons',phBehavior:beh,phPreset:'custom',phCustom:30},()=>{
    const ps=PHOT.single; let nf=0;
    for(let i=0;i<n;i++){ photonEmit(ps,ST,0); while(ps.photons.length&&nf<1e6){ photonAdvance(ps,ST,0.05); nf++; } }
    return {nV:ps.nV,nH:ps.nH,t:ps.t}; });
  { const a=runPhotons('classical',400), b=runPhotons('quantum',400);
    eq(a.nV+a.nH,400,'400 photons, 400 detections (classical)'); eq(b.nV+b.nH,400,'and 400 (quantum): every photon is counted exactly once');
    eq(a.nV,b.nV,'which-path at the splitter and collapse at the detector give the SAME seeded counts: one splitter cannot tell them apart');
    ok(Math.abs(a.nV-100)<4*Math.sqrt(400*0.25*0.75),'and the V count is sin^2(30) of 400 within 4 sigma ('+a.nV+')'); }
  /* WHEN the choice is made: a classical photon has a path as soon as it is past
     the splitter (0.5 s); a quantum one only at the detectors.  The counts cannot
     see this (one photon at a time, the same draws), so it is asserted directly. */
  withState({view:'photons',phBehavior:'classical'},()=>{ const ps=PHOT.single; photonEmit(ps,ST,0);
    const t1=photonLegs(ps.photons[0].y0).d1/PH.V;          /* 0.43-0.57 s across the beam's width */
    photonAdvance(ps,ST,t1-0.01); eq(ps.photons[0].route,null,'classical: no path just before the splitter');
    photonAdvance(ps,ST,0.02); ok(ps.photons[0].route!==null,'classical: the path is chosen AT the splitter'); });
  withState({view:'photons',phBehavior:'quantum'},()=>{ const ps=PHOT.single; photonEmit(ps,ST,0); photonAdvance(ps,ST,1.1); eq(ps.photons[0].route,null,'quantum: still on both paths at 1.1 s');
    photonAdvance(ps,ST,0.1); ok(ps.photons[0].route!==null&&ps.nV+ps.nH===1,'quantum: it collapses at the detectors (1.167 s), and is counted'); });
  withState({view:'photons',phMode:'single'},()=>{ const ps=PHOT.single; photonEmit(ps,ST,0); photonAdvance(ps,ST,1.16); eq(ps.nV+ps.nH,0,'at 1.16 s the photon has not arrived');
    photonAdvance(ps,ST,0.01); eq(ps.nV+ps.nH,1,'at 1.17 s it has (1.1667 s)'); photonAdvance(ps,ST,0.2); eq(ps.photons.length,0,'and it is gone 0.05 past the detector line');
    ps.nV=998; photonEmit(ps,ST,0); ST.phPreset='vertical'; ps.photons[0].ang=90; photonAdvance(ps,ST,1.3); photonEmit(ps,ST,0); ps.photons[0].ang=90; photonAdvance(ps,ST,1.3); eq(ps.nV,999,'single-photon counts stop at 999 (PhET)'); });
  withState({view:'photons',phMode:'many',phRate:60},()=>{ const ps=PHOT.many; for(let f=0;f<600;f++) photonAdvance(ps,ST,1/60);
    /* every photon is counted before it is retired, so emitted = counted + not yet counted */
    const emitted=ps.nV+ps.nH+ps.photons.filter(p=>!p.counted).length;
    ok(Math.abs(emitted-600)<=1,'60 photons/s for 10 s: '+emitted+' emitted (PhET\'s fractional accumulator)');
    ok(ps.avgV.value>0&&ps.avgH.value>0,'both detectors have a rate'); close((ps.avgV.value)/(ps.avgV.value+ps.avgH.value),0.5,0.2,'at 45 deg the rates are near half and half'); });
  withState({view:'photons',phMode:'single'},()=>{ PHOT.single.nV=5; ST.phPreset='horizontal'; photonAfterAngle(); eq(PHOT.single.nV,0,'a new polarization clears the single-photon counts (PhET)'); });

  /* ---------- C. Stern-Gerlach ---------- */
  const SRC={'+Z':[0,0,1],'+X':[1,0,0],'-Z':[0,0,-1]}; { const t=customTheta(0.3); SRC.c03=[Math.sin(t),0,Math.cos(t)]; }
  const PR={'e1':{'+Z':[1,0],'+X':[0.5000000000000001,0.4999999999999999],'-Z':[3.749399456654644e-33,1],'c03':[0.29999999999999993,0.7000000000000001]},
    'e2':{'+Z':[0.5,0.5],'+X':[0.9999999999999998,2.220446049250313e-16],'-Z':[0.5,0.5],'c03':[0.9582575694955839,0.04174243050441606]},
    'e3':{'+Z':[0.5,0.5,0,0],'+X':[0.25000000000000006,0.25000000000000006,0.24999999999999994,0.24999999999999994],'-Z':[0,0,0.5,0.5],'c03':[0.14999999999999997,0.14999999999999997,0.35000000000000003,0.35000000000000003]},
    'e4':{'+Z':[1,0,0,0],'+X':[0.5000000000000001,0,0,0.4999999999999999],'-Z':[0,0,0,1],'c03':[0.29999999999999993,0,0,0.7000000000000001]},
    'e5':{'+Z':[0.25,0.25,0.25,0.25],'+X':[0.4999999999999999,0.4999999999999999,0,0],'-Z':[0.25,0.25,0.24999999999999994,0.24999999999999994],'c03':[0.47912878474779197,0.47912878474779197,0.020871215252208006,0.020871215252208006]},
    'e6':{'+Z':[0.5,0,0,0.5],'+X':[0.9999999999999998,0,0,0],'-Z':[0.5,0,0,0.4999999999999999],'c03':[0.9582575694955839,0,0,0.04174243050441601]}};
  for(const e of SG_EXPS){ const key=e.id==='custom'?'e5':e.id;           /* PhET's custom layout [x, z, z] is experiment 5's */
    for(const s of Object.keys(SRC)){ const got=sgProbs(SRC[s],e.axes), want=PR[key][s]; let w=0; for(let i=0;i<want.length;i++) w=Math.max(w,Math.abs(got[i]-want[i]));
      ok(w<1e-12&&got.length===want.length,'experiment '+e.id+', source '+s+': the joint probabilities are the products of projections, against numpy projectors ('+w.toExponential(1)+', derive)'); } }
  { /* the same thing twice in JS: explicit 2x2 projectors on the ket */
    const Pn=(n,sg)=>mScale(mAdd(M_I,mScale(mAdd(mAdd(mScale(M_SX,n[0]),mScale(M_SY,n[1])),mScale(M_SZ,n[2])),sg)),0.5);
    let w=0;
    for(const e of SG_EXPS) if(e.axes.length===3) for(const s of Object.keys(SRC)){
      const r=SRC[s], th=Math.acos(clamp(r[2],-1,1)), ph=Math.atan2(r[1],r[0]), k=ketOf(th,ph), got=sgProbs(r,e.axes);
      let i=0; for(const s1 of [1,-1]) for(const s2 of [1,-1]){ const k1=mApply(Pn(AXV[e.axes[0]],s1),k), k2=mApply(Pn(AXV[s1>0?e.axes[1]:e.axes[2]],s2),k1);
        w=Math.max(w,Math.abs(ketNorm(k2)*ketNorm(k2)-got[i])); i++; } }
    ok(w<1e-14,'products of projections = ||P2 P1 psi||^2 from explicit projector matrices, all two-stage cases ('+w.toExponential(1)+')'); }
  { /* beyond PhET, which links its second-stage magnets: DIFFERENT ones, so the
       routing of the up and down beams is pinned by something (derive) */
    const g1=sgProbs([1,0,0],['z','x','z']), w1=[0.25000000000000006,0.25000000000000006,0,0.4999999999999999];
    ok(g1.every((v,i)=>Math.abs(v-w1[i])<1e-12),'[z, x, z] from +X: the up beam to x, the down beam to z (numpy projectors, derive)');
    const g2=sgProbs(SRC.c03,['z','x','z']), w2=[0.14999999999999997,0.14999999999999997,0,0.7000000000000001];
    ok(g2.every((v,i)=>Math.abs(v-w2[i])<1e-12),'[z, x, z] from |alpha|^2 = 0.3 (derive)');
    eq(sgBatch(35,[1,0,0],['z','x','z'],10000).join(','),'2589,2532,0,4879','[z, x, z]: the seeded counts (derive)'); }
  rel(customTheta(0.3),1.9823131728623846,1e-14,'custom |alpha|^2 = 0.3: theta = 2 arccos|alpha| (derive)');
  rel(bornP(SRC.c03,[0,0,1]),0.3,1e-13,'and P(up_z) IS |alpha|^2 = 0.3 (derive: 0.29999999999999993)');
  close(SRC.c03[0],0.916515138991168,1e-14,'its Bloch x (derive)'); close(SRC.c03[2],-0.4000000000000001,1e-14,'its Bloch z (derive)');
  rel((1+Math.cos(phetCustomTheta(0.75)))/2,0.8535533905932737,1e-14,'PhET\'s theta = pi(1 - |alpha|^2) would give 0.854 at |alpha|^2 = 0.75 (derive)');
  ok(Math.abs((1+Math.cos(phetCustomTheta(0.75)))/2-0.75)>0.1,'which disagrees with its own |alpha|^2 by 0.10 (the remake\'s does not)');
  for(const a2 of [0,0.5,1]) close((1+Math.cos(phetCustomTheta(a2)))/2,a2,1e-15,'except at |alpha|^2 = '+a2);
  for(const [lab,seed,r,axes,n,want] of [['exp 3 (z, x) from +X',31,[1,0,0],['z','x','x'],10000,[2558,2517,2473,2452]],['exp 5 (x, z) from +Z',32,[0,0,1],['x','z','z'],10000,[2500,2553,2522,2425]],
      ['exp 1 from |alpha|^2 = 0.3',33,SRC.c03,['z'],10000,[2947,7053,0,0]],['exp 4 (z, z) from -Z',34,[0,0,-1],['z','z','z'],4000,[0,0,0,4000]]]){
    const got=sgBatch(seed,r,axes,n); eq(got.join(','),want.join(','),lab+': the seeded counts (derive)');
    const pr=sgProbs(r,axes); let okk=true; for(let i=0;i<pr.length;i++) if(Math.abs(got[i]-n*pr[i])>4*Math.sqrt(n*pr[i]*(1-pr[i]))+1e-9) okk=false; ok(okk,lab+': every count within 4 sigma of n x the product'); }
  withState({view:'spins',sgExp:'e3'},()=>{ sgShoot(SGS,ST); for(let i=0;i<200;i++) sgAdvance(SGS,ST,0.05);
    eq(SGS.c[0].nU+SGS.c[0].nD,1,'one particle through experiment 3: measured once by magnet 1'); eq(SGS.c[1].nU+SGS.c[1].nD+SGS.c[2].nU+SGS.c[2].nD,1,'and once in the second stage');
    eq(SGS.c[0].nU,1,'a +Z source always goes up in SGz'); eq(SGS.parts.length,0,'and the particle retires after its hold'); });
  withState({view:'spins',sgExp:'e4',sgMode:'continuous',sgBlock:'up',sgAmount:0.5},()=>{ ST.sgSrc='+X'; for(let i=0;i<600;i++) sgAdvance(SGS,ST,1/60);
    eq(SGS.c[1].nU+SGS.c[1].nD,0,'blocking magnet 1\'s up beam: nothing reaches the upper magnet'); ok(SGS.c[2].nU+SGS.c[2].nD>50,'while the lower one counts ('+(SGS.c[2].nU+SGS.c[2].nD)+')');
    eq(SGS.c[2].nU,0,'and a z-down atom in a second z magnet always goes down (experiment 4)');
    const shot=SGS.c[0].nU+SGS.c[0].nD; ok(Math.abs(shot-1350)<=3,'300 x 0.5 = 150 particles a second: '+shot+' measured by magnet 1 in 10 s, less the 1-s transit (1350)'); });
  withState({view:'spins',sgExp:'e4',sgMode:'continuous',sgBlock:'down',sgAmount:0.5,sgSrc:'+X'},()=>{ for(let i=0;i<600;i++) sgAdvance(SGS,ST,1/60);
    eq(SGS.c[2].nU+SGS.c[2].nD,0,'blocking the down beam starves the lower magnet'); ok(SGS.c[1].nU>50&&SGS.c[1].nD===0,'and the upper one passes every z-up atom up'); });
  withState({view:'spins',sgExp:'e4',sgMode:'single'},()=>eq(sgBlock(ST),'none','no blocker with single particles (PhET)'));

  /* ---------- D. the Bloch sphere ---------- */
  { let wr=0, wn=0;
    for(let a=0;a<=12;a++) for(let b=0;b<=12;b++){ const th=Math.PI*a/12, ph=2*Math.PI*b/12, k=ketOf(th,ph), r=blochOfKet(k), w=blochOfAngles(th,ph);
      wn=Math.max(wn,Math.abs(ketNorm(k)-1)); wr=Math.max(wr,Math.abs(r[0]-w[0]),Math.abs(r[1]-w[1]),Math.abs(r[2]-w[2]));
      if(a>0&&a<12){ const g=anglesOfBloch(r); wr=Math.max(wr,Math.abs(g.th-th),Math.abs(Math.cos(g.ph)-Math.cos(ph)),Math.abs(Math.sin(g.ph)-Math.sin(ph))); } }
    ok(wn<1e-15,'every ket is normalised'); ok(wr<1e-13,'ket -> Bloch vector -> angles -> ket round-trips over 169 states ('+wr.toExponential(1)+')'); }
  for(const [th,ph,s,tau,rw,U,pu] of [[Math.PI/2,0,1,0.75,[-2.220446049250313e-16,-1,2.220446049250313e-16],[-0.7071067811865475,-0.7071067811865476,-0.7071067811865475,0.7071067811865476],[0.4999999999999999,0,0.5000000000000001]],
      [1.1,0.4,0.6,0.4,[-0.2948256681362459,0.841028170774136,0.4535961214255772],[0.7289686274214116,-0.6845471059286887,0.7289686274214116,0.6845471059286887],[0.35258716593187706,0.920514085387068,0.7267980607127886]],
      [2.3,5.1,-0.35,0.9,[-0.7455439686800587,0.015506586739676085,-0.6662760212798239],[0.5490228179981317,0.8358073613682703,0.5490228179981317,-0.8358073613682703],[0.12722801565997066,0.507753293369838,0.16686198936008806]]]){
    const tag='precession th='+fmt(th,2)+' s='+s+' t='+tau+' ns: ';
    const r=precess(blochOfAngles(th,ph),s,tau), Um=precessU(s,tau), kr=blochOfKet(mApply(Um,ketOf(th,ph)));
    ok(Math.max(Math.abs(r[0]-rw[0]),Math.abs(r[1]-rw[1]),Math.abs(r[2]-rw[2]))<1e-12,tag+'the exact rotation = scipy expm on the ket (derive)');
    ok(Math.max(Math.abs(kr[0]-rw[0]),Math.abs(kr[1]-rw[1]),Math.abs(kr[2]-rw[2]))<1e-12,tag+'and U(t) on the ket gives the same vector');
    ok(Math.abs(Um[0]-U[0])<1e-12&&Math.abs(Um[1]-U[1])<1e-12&&Math.abs(Um[6]-U[2])<1e-12&&Math.abs(Um[7]-U[3])<1e-12&&Math.abs(Um[2])+Math.abs(Um[3])+Math.abs(Um[4])+Math.abs(Um[5])<1e-15,tag+'U = diag(e^-iwt/2, e^+iwt/2) (derive)');
    ['X','Y','Z'].forEach((b,i)=>close(bornP(r,BASIS[b].n),pu[i],1e-12,tag+'P(up along '+b+') (derive)'));
  }
  { /* brute force: RK4 on i d psi/dt = (w/2) sigma_z psi, against the rotation */
    const s=0.6, tau=0.4, w=2*Math.PI*s, n=4000, dt=tau/n; let k=ketOf(1.1,0.4);
    const f=q=>[ w/2*q[1], -w/2*q[0], -w/2*q[3], w/2*q[2] ];   /* d/dt of [a.re,a.im,b.re,b.im] with H = (w/2) diag(1,-1) */
    for(let i=0;i<n;i++){ const k1=f(k), k2=f(k.map((v,j)=>v+dt/2*k1[j])), k3=f(k.map((v,j)=>v+dt/2*k2[j])), k4=f(k.map((v,j)=>v+dt*k3[j])); k=k.map((v,j)=>v+dt*(k1[j]+2*k2[j]+2*k3[j]+k4[j])/6); }
    const a=blochOfKet(k), b=precess(blochOfAngles(1.1,0.4),s,tau);
    ok(Math.max(Math.abs(a[0]-b[0]),Math.abs(a[1]-b[1]),Math.abs(a[2]-b[2]))<1e-10,'integrating the Schrodinger equation (RK4, 4000 steps) lands on the exact rotation'); }
  { const r=precess([1,0,0],1,0.75); close(r[1],-1,1e-15,'+X after the default 0.75 ns at s = +1 is -Y: the electron turns counterclockwise about +z (derive)');
    const wrong=rotate3([1,0,0],[0,0,1],-larmorAngle(1,0.75)); ok(wrong[1]>0.99,'the opposite sense would give +Y, so the sign is pinned, not vacuous');
    const p=precess([1,0,0],1,1); close(p[0],1,1e-14,'one nanosecond at |s| = 1 is exactly one turn'); }
  rel(B0_T*1e3,35.68248830204882,1e-14,'B0 = 1 GHz / (gamma_e/2pi) = 35.68 mT (derive)');
  rel(Math.abs(G_E)*MUB_HZ_T/1e6,GAMMA_E_MHZ_T,2e-12,'CODATA gamma_e/2pi = |g_e| mu_B/h to 1e-12 (derive: 9.7e-13)');
  withState({view:'bloch',bField:true,bStrength:-0.5},()=>{ const m=blochModel(ST,CAM); rel(m.BmT,-0.5*35.68248830204882,1e-14,'B = s B0 in mT off the model');
    rel(m.fGHz,0.5,1e-15,'f = |s| GHz: B0 is what makes an electron turn once per ns'); rel(GAMMA_E_MHZ_T*Math.abs(m.BmT)/1e6,0.5,1e-12,'and gamma_e B/2pi in GHz agrees (the constant is pinned, not invisible)'); });
  for(const [th,ph,rows] of [[1.1,2.3,{Z:[0.8525245220595057,0.5226872289306592,0.7321127382227185,0],X:[0.450671668736216,0.8926897820623435,1.6906378340728947,0.20945472481417213],Y:[0.912298737675348,0.40952535115175254,1.7076455639701331,0.08699909392895268]}],
      [Math.PI/2,0,{Z:[0.7071067811865476,0.7071067811865475,0,0],X:[1,0,0,0],Y:[0.7071067811865475,0.7071067811865475,0.49999999999999994,-0.25]}],
      [0.4,4,{Z:[0.9800665778412416,0.19866933079506122,1.2732395447351625,0],X:[0.6105158411960611,0.7920040452224129,0.09857312472015847,-0.05571490660007095],Y:[0.5938380363458273,0.8045846049912537,1.9141752131999483,0.04941798187459157]}]]){
    for(const b of ['Z','X','Y']){ const E=ketInBasis(ketOf(th,ph),b), w=rows[b];
      ok(Math.abs(E.a-w[0])<1e-12&&Math.abs(E.c-w[1])<1e-12&&(w[1]<1e-12||Math.abs(wrap2(E.chi-w[2]+1)-1)<1e-12),'the state ('+fmt(th,2)+', '+fmt(ph,2)+') in the '+b+' basis: amplitudes and relative phase (derive)');
      const k2=ketFromBasis(E,b), k=ketOf(th,ph); ok(Math.max(Math.abs(k2[0]-k[0]),Math.abs(k2[1]-k[1]),Math.abs(k2[2]-k[2]),Math.abs(k2[3]-k[3]))<1e-13,'and the written equation rebuilds the ket, global phase included'); } }
  { const E=ketInBasis(ketOf(Math.PI/2,0),'Y'); close(E.chi,0.5,1e-12,'+X in the Y basis: relative phase 0.5 pi (derive)');
    const bad=blochOfKet(ketFromBasis({a:Math.SQRT1_2,c:Math.SQRT1_2,chi:1.5,g:0},'Y')); close(bad[0],-1,1e-12,'PhET\'s printed 1.5 pi rebuilds -X, not +X (derive)'); }
  withState({view:'bloch'},()=>{ const n0=BLO.R.s; eq(blochButton(BLO,ST),'observed','no field: observe measures at once'); ok(BLO.R.s!==n0,'with one draw');
    eq(BLO.up+BLO.dn,1,'one atom counted'); eq(blochButton(BLO,ST),'reprepared','the same button then reprepares (PhET)'); eq(BLO.r[0].join(','),blochPrep(ST).join(','),'back to the prepared state');
    ST.bField=true; blochReprepare(BLO,ST); eq(blochButton(BLO,ST),'timing','with the field it starts a timed run'); eq(blochButton(BLO,ST),'busy','and the button is busy meanwhile');
    blochAdvance(BLO,ST,2.9); eq(BLO.phase,'timing','2.9 s of wall time is 0.725 ns: still timing');
    blochAdvance(BLO,ST,0.2); eq(BLO.phase,'observed','at 0.75 ns it is observed'); close(BLO.tau,0.75,1e-15,'exactly at the delay, never past it');
    ST.bAxis='Y'; blochReprepare(BLO,ST); blochResetCounts(BLO); for(let i=0;i<50;i++){ blochButton(BLO,ST); blochAdvance(BLO,ST,4); blochButton(BLO,ST); }
    eq(BLO.up,0,'+X, field on, 0.75 ns, measured along y: ALWAYS down (derive: P = 0)'); eq(BLO.dn,50,'fifty of fifty');
    close(blochPUp(ST),0,1e-15,'P(up along y) = 0 off the model'); ST.bAxis='X'; close(blochPUp(ST),0.5,1e-15,'and along x, a half'); });
  withState({view:'bloch',bTheta:1.1,bPhi:0.4,bField:true,bStrength:0.6,bDelay:0.4,bAxis:'X',bAtoms:10},()=>{ BLO.R=rngMake(42); blochResetCounts(BLO);
    for(let i=0;i<1000;i++){ blochReprepare(BLO,ST); blochButton(BLO,ST); blochAdvance(BLO,ST,1.6); }
    eq(BLO.up,3545,'1000 rounds of ten atoms along x after 0.4 ns at s = 0.6: 3545 up (derive)'); eq(BLO.up+BLO.dn,10000,'ten atoms each time');
    rel(blochPUp(ST),0.35258716593187706,1e-12,'P(up along x) at the measurement (derive)'); ok(Math.abs(3545-3525.87)<4*Math.sqrt(10000*0.3526*0.6474),'the count within 4 sigma'); });
  { const cam={theta:CAM_HOME.theta,phi:CAM_HOME.phi}; for(const [v,n] of [[[1,0,0],'x'],[[0,1,0],'y'],[[0,0,1],'z']]) ok(projLen(cam,v)>=0.6,'the home camera sees the '+n+' axis at '+fmt(projLen(cam,v),2)+' of its length (Known-bad: a camera looking along the state)');
    const B=camBasis3(cam.theta,cam.phi); ok(B.right[1]>0.5&&B.right[0]<-0.3,'x comes toward the viewer on the left, y points right (the textbook view)'); }

  /* ---------- E. the Born rule view ---------- */
  for(const [N,T2] of [[1,3.749399456654644e-33],[2,0.25000000000000006],[3,0.42187500000000017],[4,0.5307900429449552],[8,0.733133440547323],[10,0.7805460697811408],[30,0.9210100677078636],[100,0.9756269141438981],[1000,0.9975356394195499]])
    close(chainT(N),T2,1e-13,'the chain of '+N+' magnets passes cos^(2N)(pi/2N) (derive)');
  rel((1-chainT(100))/(1-chainT(1000)),9.890227124007366,1e-9,'the approach to 1 is O(1/N): ratio 9.89 (derive)');
  rel((1-chainT(1000))*4000/(Math.PI*Math.PI),0.998767723730881,1e-9,'with the coefficient pi^2/4N (derive)');
  for(const [a,s1,p1] of [[30,0.062499999999999986,0.18749999999999997],[45,0.12499999999999997,0.25],[60,0.18749999999999997,0.18750000000000003],[90,0.25,3.749399456654644e-33],[120,0.18750000000000003,0.1874999999999999]]){
    close(middleSpin(a),s1,1e-15,'a middle magnet at '+a+': 1/4 sin^2 alpha (derive)'); close(middlePhoton(a),p1,1e-15,'a middle polariser: 1/4 sin^2 2alpha (derive)'); }
  close(bornSpin(60),0.7500000000000001,1e-15,'cos^2(Theta/2) at 60 (derive)'); close(bornPhoton(60),0.2500000000000001,1e-15,'cos^2(theta) at 60 (derive)');
  eq(chainMC(51,8,5000),3682,'a chain of 8: 3682 of 5000 (derive)'); eq(chainMC(55,1,3000),0,'one magnet straight to -z passes none (derive)');
  eq(middleSpinMC(52,60,5000),955,'the middle magnet at 60: 955 (derive)'); eq(middlePhotonMC(53,60,5000),928,'the middle polariser at 60: 928 (derive)');
  eq(bornSpinMC(61,60,2000),1467,'spins at 60: 1467 up of 2000 (derive)'); eq(bornPhotonMC(62,60,2000),478,'photons at 60: 478 H of 2000 (derive)');
  withState({view:'born'},()=>{ const m=bornModel(ST);
    eq(m.pts.map(p=>Math.round(p.spin*2000)).join(','),'2000,1968,1883,1703,1489,1284,978,733,502,278,139,35,0','the view\'s spin points (derive)');
    eq(m.pts.filter(p=>p.photon!==null).map(p=>Math.round(p.photon*2000)).join(','),'2000,1856,1512,998,488,127,0','its photon points (derive)');
    rel(m.fit.chi,8.389107309239947,1e-9,'its chi-square (derive)'); eq(m.fit.dof,16,'on 16 points (derive)'); ok(m.fit.chi<39.25235479076848,'below the 99.9 % point (scipy)'); ok(m.fit.exact,'and the certain points are exact');
    const want=[0,0.244,0.4305,0.534,0.658,0.7285,0.819,0.8365,0.9015,0.928,0.9505,0.965]; ok(m.chain.every((p,i)=>Math.abs(p.T-want[i])<1e-15),'the chain view\'s points (derive)'); });

  /* ---------- F. the binomial view ---------- */
  for(const [N,s] of [[10,0.14491376746189438],[100,0.0458257569495584],[1000,0.014491376746189439],[10000,0.00458257569495584]]) rel(Math.sqrt(0.3*0.7/N),s,1e-15,'sd(k/N) at N = '+N+', p = 0.3 (derive)');
  withState({view:'binom',binN:100,binP:0.3,binM:1000,binSeed:71},()=>{ const m=binomModel(ST); eq(m.r.mean,29.951,'the view\'s default-style run: 1000 sets of 100 at 0.3 (derive)'); eq(m.r.dof,23,'23 dof (derive)');
    let s=0; for(let i=0;i<m.win.nb;i++) s+=m.hObs[i]; close(s+m.outside/m.M,1,1e-12,'the histogram accounts for every set');
    /* a sample sd from M sets scatters by about 1/sqrt(2(M-1)) in relative terms: 4 of those */
    ok(m.spread.every(p=>p.sd>0&&Math.abs(Math.log(p.sd/p.law))<4/Math.sqrt(2*(p.M-1))),'the measured spreads sit on sqrt(p(1-p)/N) within 4/sqrt(2(M-1)) at every N ('+m.spread.map(p=>fmt(p.sd/p.law,3)).join(', ')+')');
    eq(m.spread.map(p=>p.M).join(','),'200,200,200,100','200 sets per point, 100 at N = 10 000 (1e6 draws)');
    ok(Math.abs(m.run[RUN_LEN-1]-0.3)<4*Math.sqrt(0.21/RUN_LEN),'the long run ends within 4 sigma of p'); });
  withState({view:'binom',binN:10000,binP:0.5,binM:5000},()=>{ const m=binomModel(ST); eq(m.M,200,'N = 10 000 caps the sets at 200'); ok(m.capped,'and says so'); ok(m.win.w>1,'and bins the histogram'); });
  { const w=binWindow(10000,0.35); eq([w.lo,w.hi,w.w,w.nb].join(','),'3260,3740,13,37','the N = 10 000 window: +-5 sd around Np in 13-count bars, 37 of them (at most ~40)');
    const w2=binWindow(10,1); eq([w2.lo,w2.hi,w2.w].join(','),'8,10,1','p = 1: a window round the certain k = N'); }
  withState({view:'binom',binP:0},()=>{ const m=binomModel(ST); eq(m.r.mean,0,'p = 0: every set has no heads'); eq(m.sd,0,'and no spread'); });

  /* ---------- G. the models and the readouts ---------- */
  const PRESETS={coins:[{},{coinScene:'quantum'},{_start:1},{coinScene:'quantum',_start:1},{_start:1,_flip:1},{coinScene:'quantum',_start:1,_obs:1},{_start:1,_n:10000,_flip:1},{coinScene:'quantum',_n:10000,_start:1,_obs:1},{_start:1,_p:0},{coinScene:'quantum',_p:1,_start:1,_obs:1}],
    photons:[{},{phMode:'many'},{phPreset:'unpolarized'},{phBehavior:'quantum',_ph:30},{phMode:'many',phRate:200,_ph:120},{phPreset:'custom',phCustom:0,_ph:40}],
    spins:[{},{sgExp:'e3',_sg:120},{sgExp:'custom',sgA2:0.3},{sgMode:'continuous',sgExp:'e5',_sg:300},{sgMode:'continuous',sgExp:'e4',sgBlock:'down',_sg:300},{sgExp:'e6',_sg:40}],
    bloch:[{},{bField:true},{bAtoms:10},{bField:true,bAxis:'Y',_obs:1},{bTheta:0,bPhi:0,bBasis:'X',bGlobal:true},{bAtoms:10,bField:true,bStrength:-1,bDelay:1,_obs:1},{bAtoms:10,_obs:1}],
    born:[{},{bornTh:0,bornAlpha:0,bornN:1},{bornTh:180,bornAlpha:180,bornN:64,bornShots:100}],
    binom:[{},{binN:10},{binN:10000,binP:0.35},{binP:1},{binP:0.05,binN:100,binM:5000}]};
  function applyPreset(v,over){
    const clean={view:v}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    fresh(clean);
    if(v==='coins'){ const sc=COINS[ST.coinScene]; if(over._p!==undefined) sc.p=over._p; if(over._n) setCoinCount(sc,over._n);
      if(over._start) sceneStart(sc); if(over._flip){ coinPrepare(sc,sc.single,true); coinPrepare(sc,sc.set,true); coinStep(sc,sc.single,1); coinStep(sc,sc.set,1); }
      if(over._obs){ coinReveal(sc,sc.single); coinReveal(sc,sc.set); } }
    if(v==='photons'&&over._ph){ const ps=PHOT[ST.phMode]; for(let i=0;i<over._ph;i++){ if(ST.phMode==='single'&&i%6===0) photonEmit(ps,ST,0); photonAdvance(ps,ST,1/30); } }
    if(v==='spins'&&over._sg){ for(let i=0;i<over._sg;i++){ if(ST.sgMode==='single'&&i%20===0) sgShoot(SGS,ST); sgAdvance(SGS,ST,1/30); } }
    if(v==='bloch'&&over._obs){ blochButton(BLO,ST); blochAdvance(BLO,ST,5); }
  }
  for(const [v] of TABS) for(const over of PRESETS[v]){
    applyPreset(v,over); const M=buildModel(), html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(!/NaN|undefined|Infinity/.test(html),'panels clean for '+v+' '+JSON.stringify(over));
    { const nz=negZeroIn(html); ok(!nz,'no negative zero in the panels for '+v+' '+JSON.stringify(over)+(nz?': '+nz:'')); }
  }
  applyPreset('photons',{phPreset:'custom',phCustom:30}); ok(readoutHTML(buildModel()).indexOf('0.2500')>=0,'the photon readout prints P(V) = 0.2500 at 30 deg off the model');
  applyPreset('bloch',{bField:true,bAxis:'Y'}); ok(readoutHTML(buildModel()).indexOf('0.0000')>=0,'the Bloch readout prints P(up along y) = 0.0000 for +X after 0.75 ns');
  applyPreset('spins',{sgExp:'custom',sgA2:0.75}); ok(readoutHTML(buildModel()).indexOf('0.854')>=0,'the custom spin readout prints PhET\'s 0.854 beside the exact 0.750');
  applyPreset('coins',{coinScene:'quantum'}); ok(readoutHTML(buildModel()).indexOf('0.707')>=0,'the quantum coin readout prints alpha = 0.707 at bias 0.5');
  fresh(stSave);

  /* ---------- H. the pointer ---------- */
  { const shot=makeShot(1100,712), S=makeScene({getContext:()=>shot});
    withState({view:'coins'},()=>{ const sc=COINS.classical; ok(!S.pointer('down',400,300),'while preparing the coins cannot be clicked'); sceneStart(sc);
      const G=coinsLayout(shot,S.W,S.H,buildModel()).G; ok(S.pointer('down',G.single.cx,G.single.cy),'clicking the single coin'); eq(sc.single.state,'hidden','hides it');
      S.pointer('up',0,0); S.pointer('down',G.single.cx,G.single.cy); eq(sc.single.state,'revealed','and again reveals it');
      S.pointer('up',0,0); ok(S.pointer('down',G.C.x+G.C.w/2,G.C.y+G.C.h/2),'clicking the set'); eq(sc.set.state,'hidden','hides the set'); S.pointer('up',0,0);
      ok(!S.pointer('down',G.A.x+10,G.A.y+10),'the prepared coin is not a button'); });
    withState({view:'photons'},()=>{ const G=photonsGeo(shot,S.W,S.H,photonsCaption(buildModel())), map=G.map;
      ok(S.pointer('down',map.X(-0.18),map.Y(0)),'clicking the laser'); eq(PHOT.single.photons.length,1,'emits one photon'); S.pointer('up',0,0);
      const D=G.dial; ok(S.pointer('down',D.cx+D.r*Math.cos(20*DEG),D.cy-D.r*Math.sin(20*DEG)),'grabbing the dial'); eq(ST.phPreset,'custom','switches to a custom angle'); eq(ST.phCustom,20,'of 20 deg (5-deg steps)');
      eq(PHOT.single.photons.length,0,'and, as PhET does, clears the bench');
      S.pointer('move',D.cx+D.r*Math.cos(62*DEG),D.cy-D.r*Math.sin(62*DEG)); eq(ST.phCustom,60,'dragging to 62 deg sets 60');
      S.pointer('move',D.cx-D.r*Math.cos(35*DEG),D.cy-D.r*Math.sin(35*DEG)); eq(ST.phCustom,35,'across the left (145 deg) it folds into PhET\'s 0..90 as 35');
      S.pointer('up',0,0); eq(DRAG.what,null,'released'); });
    withState({view:'spins',sgExp:'custom'},()=>{ const G=spinsGeo(shot,S.W,S.H,spinsCaption(buildModel())), D=G.disc, map=G.map;
      ok(S.pointer('down',D.cx+D.r*Math.sin(Math.PI/2),D.cy-D.r*Math.cos(Math.PI/2)),'grabbing the prepared spin'); close(ST.sgA2,0.5,1e-15,'pointing along x sets |alpha|^2 = 1/2 exactly');
      S.pointer('move',D.cx,D.cy+D.r); close(ST.sgA2,0,1e-15,'pointing down sets 0'); S.pointer('up',0,0);
      const c1=ST.sgC1, mg=sgMagnetBoxes(map,spinsModel(ST),ST)[0].b; ok(S.pointer('down',mg.x+mg.w/2,mg.y+mg.h/2),'clicking magnet 1'); ok(ST.sgC1!==c1,'turns it'); S.pointer('up',0,0);
      ST.sgExp='e1'; ok(S.pointer('down',map.X(-0.5),map.Y(0)),'clicking the source'); eq(SGS.parts.length,1,'shoots a particle'); S.pointer('up',0,0); });
    withState({view:'bloch'},()=>{ ok(S.pointer('down',400,300),'grab the Bloch view'); const t0=CAM.theta, p0=CAM.phi; S.pointer('move',460,300); ok(CAM.theta!==t0&&CAM.phi===p0,'a horizontal drag turns theta only');
      S.pointer('move',460,340); ok(CAM.phi!==p0,'a vertical one turns phi'); S.pointer('up',0,0); resetCam(); eq(CAM.theta,CAM_HOME.theta,'and r goes home'); });
    withState({view:'born'},()=>{ const G=bornLayout(shot,S.W,S.H,buildModel()).G; ok(S.pointer('down',G.A.x+G.A.w/2,G.A.y+G.A.h/2),'grabbing the half-angle panel'); eq(ST.bornTh,90,'sets Theta = 90');
      S.pointer('move',G.A.x+G.A.w/6,G.A.y+10); eq(ST.bornTh,30,'dragging sets 30'); S.pointer('up',0,0);
      S.pointer('down',G.C.x+G.C.w,G.C.y+5); eq(ST.bornN,64,'the chain panel sets N'); S.pointer('up',0,0); });
    withState({view:'binom'},()=>ok(!S.pointer('down',400,300),'the binomial view ignores the pointer'));
  }

  /* ---------- I. the layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const FLOOR={coins:2,photons:4,spins:3,bloch:4,born:4,binom:4};      /* the sparsest configuration's own count */
  /* legendAuto draws NO legend when every spot is crossed (house rule: better
     none than a lying one), so a legend can vanish silently: at the two large
     sizes every legend must find its spot (the photon beam's lost its own) */
  const legendAuto0=legendAuto; let legLost=[];
  legendAuto=function(ctx,b,items){ const r=legendAuto0(ctx,b,items); if(r===null) legLost.push(items.map(i=>i[1]).join(', ')); return r; };
  for(const [v] of TABS) for(const over of PRESETS[v]) for(const [W,H] of SIZES){
    applyPreset(v,over); legLost=[];
    layoutCheck(T,v+' '+JSON.stringify(over),(c,w,hh)=>drawView(c,w,hh,buildModel()),W,H,FLOOR[v]);
    if(W>=1100) ok(!legLost.length,v+' '+JSON.stringify(over)+' '+W+'x'+H+' every legend is drawn'+(legLost.length?' (lost: '+legLost[0]+')':''));
  }
  legendAuto=legendAuto0;
  /* the hint reservation is load-bearing: without it, bottom captions sit in the hint's corner */
  { applyPreset('coins',{}); const c=makeShot(1400,820); drawView(c,1400,820,buildModel()); const last=c.ops.filter(o=>o.op==='text').reduce((a,o)=>Math.max(a,o.bb[3]),0);
    ok(last<=820-HINT_H,'the lowest canvas text ends '+fmt(820-last,0)+' px above the bottom, clear of the 18-px hint band'); }
  /* the Malus legend names only what is drawn (it listed the measured point in the beam and unpolarized views, looked at) */
  { const legOf=over=>{ applyPreset('photons',over); const c=makeShot(1400,820); drawView(c,1400,820,buildModel()); return c.ops.filter(o=>o.op==='text').map(o=>o.t).join('|'); };
    const a=legOf({}), b=legOf({_ph:40}), cc=legOf({phMode:'many',_ph:120}), d=legOf({phPreset:'unpolarized',phMode:'many',_ph:120});
    const has=(s,t)=>('|'+s+'|').indexOf('|'+t+'|')>=0;
    ok([a,b,cc,d].every(s=>has(s,'P(V) = sin²θ')),'the Malus legend is drawn in all four states (a longer entry once pushed it off its only free spot, and legendAuto then draws none)');
    ok(a.indexOf('measured V')<0&&has(b,'measured V fraction ± 1σ')&&has(cc,'measured V fraction')&&d.indexOf('measured V')<0,
       'and it lists the measured point only where it is drawn: not before a count, ± 1σ for counts, without sigma for a beam\'s rates, never unpolarized'); }
  /* the Bloch fringe legend names the measured point exactly when it is drawn (field on and off) */
  { const legB=over=>{ applyPreset('bloch',over); const c=makeShot(1400,820); drawView(c,1400,820,buildModel()); return c.ops.filter(o=>o.op==='text').map(o=>o.t).join('|'); };
    const has=(s,t)=>('|'+s+'|').indexOf('|'+t+'|')>=0, M1='measured here ± 1σ';
    const f0=legB({bField:true}), f1=legB({bField:true,_obs:1}), n0=legB({}), n1=legB({bAtoms:10,_obs:1});
    ok(has(f0,'the law, for this field')&&!has(f0,M1)&&has(f1,M1)&&has(n0,'no field: flat')&&!has(n0,M1)&&has(n1,M1)&&has(n1,'no field: flat'),
       'the Bloch fringe legend is drawn, and names the measured point exactly when it is drawn, with the field on and off'); }
  /* a caption names only panels that are drawn (the Bloch caption named its fringe panel where 820 x 520 skips it, looked at) */
  { const NAMES={coins:/histogram counts|Orange:/,bloch:/panel below/,born:/Below:|the chain/,binom:/Below:|one long run/};
    const LAY={coins:coinsLayout,bloch:blochLayout,born:bornLayout,binom:binomLayout};
    let bad=null, n=0; const off={};
    for(const v in LAY) for(const over of PRESETS[v]) for(const [W,H] of SIZES.concat([[700,450],[900,560]])){
      applyPreset(v,over); const L=LAY[v](makeShot(W,H),W,H,buildModel()); n++;
      if(L.G.panelOff){ off[v]=(off[v]||0)+1; if(NAMES[v].test(L.G.fit.txt)&&!bad) bad=v+' '+W+'x'+H+': "'+L.G.fit.txt.slice(0,60)+'"'; }
      else if(!NAMES[v].test(L.Cap.full)&&!bad) bad=v+' '+W+'x'+H+': the panel is drawn but the full caption does not name it'; }
    ok(!bad&&Object.keys(LAY).every(v=>off[v]>0),'every caption names only the panels that are drawn ('+n+' layouts; optional panel off in '+JSON.stringify(off)+(bad?'; '+bad:'')+')'); }
  /* the stage dials clear every beam band (after magnet 2 sat on the upper magnet's up beam, looked at) */
  { const segD=(px0,py0,ax,ay,bx,by)=>{ const vx=bx-ax, vy=by-ay, L2=vx*vx+vy*vy, t=L2>0?clamp(((px0-ax)*vx+(py0-ay)*vy)/L2,0,1):0; return Math.hypot(px0-ax-t*vx,py0-ay-t*vy); };
    let worst=Infinity, where='', n=0;
    for(const e of SG_EXPS.map(x=>x.id)) for(const [W,H] of SIZES){
      applyPreset('spins',{sgExp:e}); const M=buildModel(), m=M.S, G=spinsGeo(makeShot(W,H),W,H,spinsCaption(M)), map=G.map, half=Math.max(2,0.07*map.s)/2;
      const paths=[]; for(const u1 of [true,false]){ if(!m.two) paths.push(sgWaypoints({jy:0,up1:u1,two:false,up2:null}));
        else for(const u2 of [true,false]) paths.push(sgWaypoints({jy:0,up1:u1,two:true,up2:u2})); }
      for(const d of sgDials(map,m)){ n++; for(const P of paths) for(let i=1;i<P.length;i++){
        const g=segD(d.x,d.y,map.X(P[i-1][0]),map.Y(P[i-1][1]),map.X(P[i][0]),map.Y(P[i][1]))-d.r-half;
        if(g<worst){ worst=g; where=e+' '+W+'x'+H+' '+d.label; } } } }
    ok(worst>=3,'all '+n+' stage dials (7 experiments x 4 sizes) clear every beam band by '+fmt(worst,1)+' px or more (tightest: '+where+')'); }
  fresh(stSave);
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
