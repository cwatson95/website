
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are     *
 *  lines of build/gases-intro/refvals.txt, the printed output of       *
 *  derive.py; REF (p7a_refs.js) is the same numbers, written by        *
 *  derive.py so that none is retyped.  The engine's own invariants     *
 *  are re-asserted here because this file relies on them.              *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,rot:Math.abs(Mx[1])>1e-9,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}
function runFrames(g,frames,dt){ for(let f=0;f<frames;f++) gasStep(g,dt||GAS.DT_FRAME); }
/* the measured wall-hit rate of a fresh box: N disks at T in a width W, run
   for `ps` picoseconds, counting every wall hit */
function measureHits(N,T,Wpm,ps,coll,seed){
  const g=gasMake({seed:seed||7,width:Wpm,collisions:coll!==false,noLid:true});
  gasFill(g,0,N,T);
  const pred=(()=>{ const r=g.species[0].r, a=g.W-2*r, b=g.H-2*r; let s=0;
    for(let i=0;i<g.n;i++) s+=Math.abs(g.vx[i])/a+Math.abs(g.vy[i])/b; return s; })();
  let hits=0, t=0; const frames=Math.round(ps/GAS.DT_FRAME);
  for(let f=0;f<frames;f++){ gasStep(g,GAS.DT_FRAME); hits+=g.stats.frameWallHits; t+=GAS.DT_FRAME; }
  return {g,hits,t,rate:hits/t,sd:Math.sqrt(hits)/t,realised:pred,
          th:hitRateTheory(g,true), id:hitRateTheory(g,false)};
}
/* the configurations the layout sweep and the capture share */
const CONFIGS=[
  ['intro default',{view:'intro'},null],
  ['intro empty',{view:'intro'},w=>{ gasRemoveAll(w.g); }],
  ['intro crowded',{view:'intro',showWatch:true},w=>{ gasInject(w.g,0,300); gasInject(w.g,1,300); for(let f=0;f<40;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['intro lid open',{view:'intro'},w=>{ gasSetLid(w.g,3000); for(let f=0;f<90;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['intro lid blown',{view:'intro',unitP:'kPa'},w=>{ w.g.lid.on=false; for(let f=0;f<12;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['intro narrow',{view:'intro',unitT:'C'},w=>{ gasResize(w.g,GAS.WMIN,true); gasRefresh(w.g); for(let f=0;f<48;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['laws nothing',{view:'laws'},w=>{ for(let f=0;f<48;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['laws hold V heating',{view:'laws',hold:'volume'},w=>{ gasSetHold(w.g,'volume'); for(let f=0;f<72;f++) worldStep(w,Object.assign({},ST,{heat:0.8}),GAS.DT_FRAME); }],
  ['laws hold P V',{view:'laws',hold:'pressureV'},w=>{ gasSetHold(w.g,'pressureV'); for(let f=0;f<72;f++) worldStep(w,Object.assign({},ST,{heat:0.8}),GAS.DT_FRAME); }],
  ['laws hold T',{view:'laws',hold:'temperature'},w=>{ gasSetHold(w.g,'temperature'); gasResize(w.g,7000,true); gasRefresh(w.g); for(let f=0;f<48;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['laws oops',{view:'laws'},w=>{ gasSetHold(w.g,'temperature'); gasRemoveAll(w.g); }],
  ['pv default',{view:'pv'},w=>{ for(let f=0;f<48;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['pv squeezed at T',{view:'pv',hold:'temperature'},w=>{ gasSetHold(w.g,'temperature');
    for(const wd of [9000,8000,7000,6000,5000]){ gasResize(w.g,wd,true); gasRefresh(w.g); for(let f=0;f<24;f++) worldStep(w,ST,GAS.DT_FRAME); } }],
  ['pv empty',{view:'pv'},w=>{ gasRemoveAll(w.g); }],
  ['sweep idle',{view:'sweep'},null],
  ['sweep boyle',{view:'sweep',law:'boyle',sWin:5},w=>{ sweepStart(w,ST); sweepRunAll(w,ST); }],
  ['sweep charles',{view:'sweep',law:'charles',sWin:5},w=>{ sweepStart(w,ST); sweepRunAll(w,ST); }],
  ['sweep gay',{view:'sweep',law:'gay',sWin:5},w=>{ sweepStart(w,ST); sweepRunAll(w,ST); }],
  ['sweep avogadro',{view:'sweep',law:'avo',sWin:5},w=>{ sweepStart(w,ST); sweepRunAll(w,ST); }],
  ['sweep part way',{view:'sweep',law:'gay',sWin:5},w=>{ sweepStart(w,ST); sweepRunAll(w,ST,500); }]
];
function setupConfig(over,fn){
  Object.assign(ST,DEFAULTS,over); DRAG.what=null;
  resetAllWorlds();
  const w=worldOf(ST.view);
  if(fn) fn(w);
  ST.nH=gasCount(w.g,0); ST.nL=gasCount(w.g,1);
  return w;
}

function selfTest(){
  let pass=0,fail=0;
  const verbose=typeof SELFTEST_VERBOSE!=='undefined'&&SELFTEST_VERBOSE;
  const ok=(c,name)=>{ if(c){ pass++; if(verbose) console.log('ok — '+name); } else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T0=Date.now(), TIMES={};
  const stSave=Object.assign({},ST);

  /* ---------- A. PhET's constants, pinned absolutely ---------- */
  eq(GAS.K,8316,'PhET BOLTZMANN = 8316 AMU pm²/(ps² K)');
  rel(GAS.K/REF.kCodata-1,REF.kRelDiff,1e-9,'PhET k is +1.849e-4 over CODATA k_B/u (derive)');
  rel(GAS.P_SCALE,REF.pConv,1e-15,'PRESSURE_CONVERSION_SCALE = 1.66e6 kPa per AMU/(pm ps²) (derive)');
  rel(GAS.KG_PER_AMU*1e33,GAS.P_SCALE,1e-15,'the pressure scale is derived from the AMU, not independent');
  rel(GAS.ATM_PER_KPA,REF.atmPerKpaExact,3e-7,'ATM_PER_KPA is 1/101.325 to PhET’s 6 digits (derive)');
  eq(GAS.H,8750,'container height 8750 pm'); eq(GAS.D,4000,'container depth 4000 pm'); eq(GAS.WALL,75,'wall thickness 75 pm');
  eq(GAS.WMIN+'/'+GAS.WMAX+'/'+GAS.WDEF,'5000/15000/10000','width range 5–15 nm, default 10');
  eq(GAS.HEAVY.m+'/'+GAS.HEAVY.r+'/'+GAS.LIGHT.m+'/'+GAS.LIGHT.r,'28/125/4/87.5','masses and radii (PhET)');
  eq(GAS.HEAT_COOL+'/'+GAS.P_MAX+'/'+GAS.T_MAX,'800/20000/100000','heatCool, maxPressure, maxTemperature');
  close(GAS.ENTRY_Y,REF.entryY,1e-12,'the entry point is H/5 = 1750 pm up the right wall (derive)');
  rel(GAS.DT_FRAME,REF.dtFrame,1e-15,'one frame is 1/24 ps (1 ps = 0.4 s at 60 fps) (derive)');
  rel(GAS.STEP,REF.stepPs,1e-15,'the step button is MODEL_TIME_STEP = 0.2 ps (derive)');
  eq(GAS.PERIODS.join(','),'5,10,20','collision counter periods');
  eq(TABS.length,4,'four views: PhET’s two screens and two house views');
  eq(TABS.map(t=>t[0]).join(','),'intro,laws,pv,sweep','the view keys');
  eq(HOLDS.length,5,'PhET’s five hold-constant choices');

  /* ---------- B. PhET's definitions and the exact laws ---------- */
  rel(gasPressureOf(100,300,REF.V10),REF.P100kPa,1e-15,'P = NkT/V: 100 disks at 300 K in 10 nm = 1183.248 kPa (derive)');
  rel(gasPressureOf(100,300,REF.V10)*GAS.ATM_PER_KPA,REF.P100atm,1e-15,'… = 11.678 atm (derive)');
  rel(gasPressureOf(200,300,REF.V10),REF.P200kPa,1e-15,'doubling N doubles P (derive)');
  rel(gasPressureOf(100,600,REF.V10),REF.P100T600,1e-15,'doubling T doubles P (derive)');
  rel(gasPressureOf(100,300,GAS.WMIN*GAS.H*GAS.D),REF.P100W5,1e-15,'halving V doubles P (derive)');
  rel(gasPressureOf(1000,1000,GAS.WMIN*GAS.H*GAS.D),REF.PmaxCase,1e-14,'1000 at 1000 K in 5 nm: 78,883 kPa, past the lid limit (derive)');
  rel(gasKT2(300),REF.kT2_300,1e-15,'kT₂ = (3/2)kT = 3,742,200 at 300 K (derive)');
  { const g=gasMake({seed:3}); gasFill(g,0,60,437.5);
    rel(gasTemp(g),437.5,1e-12,'T = (2/3)⟨KE⟩/k reproduces the temperature the box was filled at');
    eq(gasTemp(gasMake({seed:4})),null,'an empty box has no temperature'); }
  { /* PhET's pump: every particle enters at (−r, H/5) at √(3kT_i/m), aimed into
       a π/2 fan CENTRED ON π (pointing left into the box).  2000 draws put the
       extremes within FAN/2000 of the ends, which pins the fan's width and its
       centre absolutely rather than merely bounding them. */
    const g=gasMake({seed:77,collisions:false});
    eq(gasInject(g,0,2000,300),GAS.NMAX,'the pump stops at 1000 per species');
    let lo=Infinity, hi=-Infinity, wrongPlace=0;
    for(let i=0;i<g.n;i++){ const a=Math.atan2(g.vy[i],g.vx[i]), th=a<0?a+TAU:a;
      if(th<lo) lo=th; if(th>hi) hi=th;
      if(g.x[i]!==-125||g.y[i]!==REF.entryY) wrongPlace++; }
    eq(wrongPlace,0,'every one of the 1000 entered at (−r, H/5) = (−125, '+REF.entryY+')');
    close(hi-lo,GAS.FAN,4*GAS.FAN/GAS.NMAX,'1000 injections span the whole π/2 fan ('+fmt(hi-lo,4)+' rad)');
    close((hi+lo)/2,PI,4*GAS.FAN/GAS.NMAX,'… centred on π, pointing left into the box');
    close(GAS.FAN,PI/2,1e-15,'the fan is π/2 wide (PhET’s DISPERSION_ANGLE)');
    ok(lo>=PI-GAS.FAN/2-1e-12&&hi<=PI+GAS.FAN/2+1e-12,'… and nothing was aimed outside it');
    /* collisions off: PhET gives every injected particle exactly √(3kT/m) */
    let same=true;
    for(let i=0;i<g.n;i++) if(Math.abs(gasSpeed(g,i)-mbRmsSpeed(28,gasKT2(300)))>1e-9) same=false;
    ok(same,'collisions off: every injected particle is at exactly √(3kT/m) = '+fmt(REF.vRms_heavy,3)+' m/s (derive)');
    rel(gasSpeed(g,0),REF.vRms_heavy,1e-12,'… pinned absolutely, not just to itself'); }
  { /* collisions ON: PhET spreads the injection temperatures (σ = 0.2 T) but
       restores the mean exactly, so a pump stroke does not shift T */
    const g=gasMake({seed:88});
    gasInject(g,0,200,437);
    rel(gasTemp(g),437,1e-13,'collisions on: 200 injected at 437 K leave T at exactly 437 (the Gaussian mean is restored)');
    let spread=0; const v0=mbRmsSpeed(28,gasKT2(437));
    for(let i=0;i<g.n;i++) spread=Math.max(spread,Math.abs(gasSpeed(g,i)/v0-1));
    ok(spread>0.05,'… but the individual speeds ARE spread (worst '+fmt(100*spread,1)+' % from √(3kT/m))');
    const g2=gasMake({seed:88}); gasInject(g2,0,200,437);
    gasInject(g2,0,200,437);
    rel(gasTemp(g2),437,1e-13,'… and a second stroke leaves it there too'); }
  rel(mbMeanSpeed(28,gasKT2(300)),REF.vMean_heavy,1e-14,'heavy ⟨v⟩ = 458.19 m/s (derive, scipy quad)');
  rel(mbMeanSpeed(4,gasKT2(300)),REF.vMean_light,1e-14,'light ⟨v⟩ = 1212.25 m/s (derive)');
  rel(mbRmsSpeed(28,gasKT2(300)),REF.vRms_heavy,1e-14,'the rms speed IS PhET’s injection speed √(3kT/m) (derive)');
  rel(Math.sqrt(gasKT2(300)/(2*PI*28)),REF.vxPlus_heavy,1e-14,'⟨v_x⁺⟩ = √(kT₂/2πm) = 145.846 m/s (derive, scipy quad)');
  rel(mbMeanSpeed(28,gasKT2(300))/PI,REF.vxPlus_heavy,1e-14,'… and it is exactly ⟨v⟩/π (derive)');
  rel(mbMeanSpeed(4,gasKT2(300))/PI,REF.vxPlus_light,1e-14,'… for the light disks too (derive)');
  rel(Math.sqrt(28/4),REF.graham,1e-15,'Graham’s √(m_heavy/m_light) (derive)');
  rel(hdB2(250),REF.b2,1e-14,'B₂ = πσ²/2 (derive)');
  rel(HD_B3_RATIO,REF.b3ratio,1e-15,'B₃/B₂² = 4/3 − √3/π = 0.78200 (derive)');
  rel(hdContact(GAS.WDEF-250,GAS.H-250,250),REF.contactM,1e-12,'the contact measure M, term by term against quadrature (derive)');
  rel(hdZ([100,0],[125,87.5],GAS.WDEF,GAS.H),REF.z100,1e-12,'Z of 100 heavy disks in the 10 nm box (derive)');
  rel(hdZ([50,0],[125,87.5],GAS.WDEF,GAS.H),REF.z50,1e-12,'… of 50 (derive)');
  rel(hdZ([200,0],[125,87.5],GAS.WDEF,GAS.H),REF.z200,1e-12,'… of 200 (derive)');
  ok(hdZ([1,0],[125,87.5],GAS.WDEF,GAS.H)===1,'one disk cannot crowd itself: Z = 1 exactly');
  { /* the engine writes the single-species Z twice — hdZ sums over pairs, hdZ1
       is the closed form for one species — so assert they agree, or a change to
       either is invisible (the identity, not a retyped formula) */
    for(const N of [2,50,100,400]){
      const a=GAS.WDEF-250, b=GAS.H-250;
      rel(hdZ([N,0],[125,87.5],GAS.WDEF,GAS.H),
          1+hdZ1(N,250,a,b)*(1+HD_B3_RATIO*hdB2(250)*N/(a*b)),1e-14,
          'hdZ and hdZ1 agree for '+N+' heavy disks'); } }

  /* ---------- C. the engine invariants this sim relies on ---------- */
  { /* the contact quadratic, at and around its branches.  The overlap test is
       the one with no margin: two disks that already overlap get NO event (they
       pass through, which is what lets the pump inject at one point), and a
       test written with any slack lets a hair-overlapping pair collide. */
    close(pairTime(0,500,0,-100,250),2.5,1e-15,'head-on: (500−250)/100 = 2.5 exactly');
    eq(pairTime(0,300,0,10,250),Infinity,'separating: no event');
    eq(pairTime(0,300,10,0,250),Infinity,'b = 0 (sliding past): no event');
    eq(pairTime(1000,300,-10,0,250),Infinity,'a miss: the discriminant is negative');
    eq(pairTime(0,200,0,-10,250),Infinity,'overlapping and approaching: no event (they pass through, as in PhET)');
    eq(pairTime(0,249.999,0,-10,250),Infinity,'overlapping by a HAIR (c = −0.5 pm²): still no event');
    eq(pairTime(0,250.0001,0,-10,250)<1e-4,true,'… and a hair apart it collides almost at once');
    ok(pairTime(0,250,0,-10,250)===Infinity||pairTime(0,250,0,-10,250)===0,'exactly touching is the boundary'); }
  { /* elastic pair collisions: momentum and energy to rounding, 5000 draws */
    const R=gasRng(4242); let wp=0, we=0;
    for(let q=0;q<5000;q++){
      const mi=1+39*R.next(), mj=1+39*R.next(), ri=60+200*R.next(), rj=60+200*R.next();
      const g=gasMake({seed:1,species:[{m:mi,r:ri},{m:mj,r:rj}]});
      const th=TAU*R.next(), s=ri+rj;
      gasPush(g,0,-5000,4000,300*(R.next()-0.5),300*(R.next()-0.5));
      gasPush(g,1,-5000+s*Math.cos(th),4000+s*Math.sin(th),300*(R.next()-0.5),300*(R.next()-0.5));
      const px0=mi*g.vx[0]+mj*g.vx[1], py0=mi*g.vy[0]+mj*g.vy[1], e0=gasKE(g,0)+gasKE(g,1);
      pairResolve(g,0,1);
      const px1=mi*g.vx[0]+mj*g.vx[1], py1=mi*g.vy[0]+mj*g.vy[1], e1=gasKE(g,0)+gasKE(g,1);
      const sc=Math.abs(px0)+Math.abs(py0)+1e-9;
      wp=Math.max(wp,(Math.abs(px1-px0)+Math.abs(py1-py0))/sc); we=Math.max(we,Math.abs(e1/e0-1));
    }
    ok(wp<1e-14,'5000 random pair collisions conserve momentum ('+wp.toExponential(1)+')');
    ok(we<1e-13,'… and energy ('+we.toExponential(1)+')'); }
  { /* the stationary wall flips one component exactly, and does no work */
    const g=gasMake({seed:5,noLid:true}); gasPush(g,0,-GAS.WDEF+130,4000,-400,250);
    const e0=gasEnergy(g); runFrames(g,24);
    rel(gasEnergy(g),e0,1e-15,'a stationary wall does no work: the energy is unchanged after 1 ps');
    ok(g.stats.wallHits>0,'… and it was struck ('+g.stats.wallHits+' times)'); }
  { /* no overlaps from the dynamics: 300 heavy disks, 3 ps, every pair each frame */
    const g=gasMake({seed:6,noLid:true}); gasFill(g,0,300,300);
    const eta=300*PI*125*125/(GAS.WDEF*GAS.H);
    let worst=Infinity;
    for(let f=0;f<72;f++){ gasStep(g,GAS.DT_FRAME);
      for(let i=0;i<g.n;i++) for(let j=i+1;j<g.n;j++){
        const d=Math.hypot(g.x[i]-g.x[j],g.y[i]-g.y[j])-(gasRad(g,i)+gasRad(g,j));
        if(d<worst) worst=d; } }
    ok(worst>-1e-6,'300 disks at area fraction '+fmt(eta,3)+' never overlap over 3 ps (closest approach '+worst.toExponential(1)+' pm)');
    const led=gasLedger(g); ok(Math.abs(led.resid)<=1e-12*Math.abs(led.E),'… and the energy ledger closes to '+(led.resid/led.E).toExponential(1)+' of the energy'); }

  /* ---------- D. the four laws, as the sweep measures them ---------- */
  for(let i=0;i<REF.boyleW.length;i++)
    rel(gasPressureOf(100,300,REF.boyleW[i]*GAS.H*GAS.D),REF.boyleP[i],1e-14,'Boyle: P at w = '+REF.boyleW[i]+' pm (derive)');
  rel(REF.boyleP[0]*REF.boyleW[0]*GAS.H*GAS.D/1e9,REF.boylePV,1e-14,'Boyle’s invariant P V (derive)');
  for(let i=0;i<REF.charlesT.length;i++)
    rel(100*GAS.K*REF.charlesT[i]/(REF.P100kPa/GAS.P_SCALE)/(GAS.H*GAS.D),REF.charlesW[i],1e-12,'Charles: the width at T = '+REF.charlesT[i]+' K (derive)');
  rel(REF.charlesTmin,150,1e-12,'the container’s 5 nm floor is T = 150 K at this P and N (derive)');
  rel(REF.charlesTmax,450,1e-12,'… and its 15 nm ceiling is 450 K (derive)');
  for(let i=0;i<REF.glT.length;i++)
    rel(gasPressureOf(100,REF.glT[i],REF.V10),REF.glP[i],1e-14,'Gay-Lussac: P at T = '+REF.glT[i]+' K (derive)');
  for(let i=0;i<REF.avN.length;i++)
    rel((REF.P100kPa/GAS.P_SCALE)*REF.V10/(REF.avN[i]*GAS.K),REF.avT[i],1e-12,'Avogadro: T at N = '+REF.avN[i]+' (derive)');
  rel(REF.avN[0]*REF.avT[0],REF.avNT,1e-13,'Avogadro’s invariant N T (derive)');
  /* the isotherms the P-V view draws, asserted off the model function that
     builds them, not off a formula retyped in the test */
  { const V0=GAS.WMIN*GAS.H*GAS.D/1e9, V1=GAS.WMAX*GAS.H*GAS.D/1e9;
    eq(ISO_T.join(','),'150,300,600,1000','the four isotherms the P-V view draws');
    for(let i=0;i<ISO_T.length;i++){
      const iso=pvIsotherm(100,ISO_T[i],V0,V1,2);
      eq(iso.xs.length,3,'three sample points at 5, 10 and 15 nm');
      close(iso.xs[1],GAS.WDEF*GAS.H*GAS.D/1e9,1e-9,'… the middle one is the 10 nm volume');
      for(const j of [0,1,2])
        rel(iso.ys[j],REF.isoP[i][j],1e-14,'the '+ISO_T[i]+' K isotherm at '+(5+5*j)+' nm (derive)');
    }
    const a=pvIsotherm(100,300,V0,V1,2), b2=pvIsotherm(200,300,V0,V1,2);
    for(const j of [0,1,2]) rel(b2.ys[j],2*a.ys[j],1e-14,'doubling N doubles the isotherm everywhere');
    const c2=pvIsotherm(100,600,V0,V1,2);
    for(const j of [0,1,2]) rel(c2.ys[j],2*a.ys[j],1e-14,'… and so does doubling T'); }

  /* ---------- E. the heater, exactly PhET's per-frame factor ---------- */
  { const g=gasMake({seed:8,noLid:true}); gasFill(g,0,80,300); g.heat=1;
    const want=REF.heatStep;
    gasStep(g,GAS.DT_FRAME);
    rel(gasTemp(g),300*want*want,1e-12,'one frame at full heat multiplies T by (1 + 1/800)² (derive)');
    let t=GAS.DT_FRAME; while(gasTemp(g)<1000&&t<200){ gasStep(g,GAS.DT_FRAME); t+=GAS.DT_FRAME; }
    close(t,REF.heatTime300to1000,GAS.DT_FRAME*1.01,'300 K → 1000 K at full heat takes 20.08 ps (derive)');
    g.heat=-1; const T1=gasTemp(g); gasStep(g,GAS.DT_FRAME);
    rel(gasTemp(g),T1*(1-1/800)*(1-1/800),1e-12,'and cooling is the same factor the other way'); }

  /* ---------- F. the wall-hit rate: the one measurement PhET's definitions do not force ---------- */
  { /* collisions OFF: the measured count is the closed-form count of a free
       flight, particle by particle, and the rate is the realised Σ|vx|/a + Σ|vy|/b */
    const g=gasMake({seed:9,noLid:true,collisions:false}); gasFill(g,0,200,300);
    const r=g.species[0].r, a=g.W-2*r, b=g.H-2*r, ps=60, T=ps;
    let want=0;
    for(let i=0;i<g.n;i++){
      for(const [v,p,lo,hi] of [[g.vx[i],g.x[i],g.left+r,-r],[g.vy[i],g.y[i],r,g.H-r]]){
        const L=hi-lo, s=Math.abs(v); if(!(s>0)) continue;
        const d0=v>0?hi-p:p-lo, t1=d0/s;
        if(T>=t1) want+=1+Math.floor((T-t1)*s/L);
      }
    }
    let got=0; const frames=Math.round(ps/GAS.DT_FRAME);
    for(let f=0;f<frames;f++){ gasStep(g,GAS.DT_FRAME); got+=g.stats.frameWallHits; }
    eq(got,want,'collisions off: every wall hit in 60 ps is the closed-form free-flight count');
    const realised=(()=>{ let s=0; for(let i=0;i<g.n;i++) s+=Math.abs(g.vx[i])/a+Math.abs(g.vy[i])/b; return s; })();
    const theory=hitRateTheory(g,false);
    /* Σ|vx| over 2N draws has a relative sd of √(1−2/π)/√((2/π)·2N) = 0.0378 here */
    const sd=Math.sqrt(1-2/PI)/Math.sqrt(2/PI)/Math.sqrt(2*g.n);
    ok(Math.abs(realised/theory-1)<4*sd,'… and 2 n ⟨v⟩/π (a+b) is that realisation’s mean (measured '+fmt(realised,3)+' vs '+fmt(theory,3)+', 4 sd = '+fmt(4*sd,3)+')');
    rel(hitRateTheory(g,true),theory,1e-15,'with collisions off the theory drops its Z: the gas is ideal however big the disks are');
    const gc=gasMake({seed:9,noLid:true}); gasFill(gc,0,200,300); gasRefresh(gc);
    ok(hitRateTheory(gc,true)>hitRateTheory(gc,false)*1.05,'… while the same gas WITH collisions carries a Z of '+fmt(hitRateTheory(gc,true)/hitRateTheory(gc,false),3)); }
  { /* collisions ON: the rate rises by the hard-disk Z, and the measurement
       can tell the two apart.  120 disks for 120 ps counts ~1000 hits, so the
       Poisson error is ~3 % against a Z correction of 15 %. */
    const R=measureHits(120,300,GAS.WDEF,120,true,11);
    rel(R.th/R.id,hdZ([120,0],[125,87.5],GAS.WDEF,GAS.H),1e-15,'theory with Z over theory without IS the hard-disk Z');
    ok(R.hits>600,'120 disks for 120 ps count '+R.hits+' wall hits');
    ok(Math.abs(R.rate-R.th)<3.5*R.sd,'the measured rate '+fmt(R.rate,3)+'/ps matches kinetic theory with Z, '+fmt(R.th,3)+' (3.5 sd = '+fmt(3.5*R.sd,3)+')');
    ok(R.rate-R.id>2*R.sd,'… and is above the Z = 1 value '+fmt(R.id,3)+' by more than 2 sd: the collisions really do crowd the disks against the walls');
    ok(R.th>R.id,'Z > 1 for a gas of finite disks'); }
  { /* light disks are faster, so they strike more often at the same T and N */
    const g=gasMake({seed:12,noLid:true}); gasFill(g,1,100,300); gasRefresh(g);
    const gh=gasMake({seed:12,noLid:true}); gasFill(gh,0,100,300); gasRefresh(gh);
    const ratio=hitRateTheory(g,false)/hitRateTheory(gh,false);
    const geom=(GAS.H-2*87.5+GAS.WDEF-2*87.5)/(GAS.H-250+GAS.WDEF-250)*((GAS.WDEF-250)*(GAS.H-250))/((GAS.WDEF-175)*(GAS.H-175));
    rel(ratio,REF.graham*geom,1e-13,'light over heavy hit rate = Graham’s √7 times the excluded-area factor'); }
  TIMES.F=Date.now();

  /* ---------- G. the sweep: the controller, and the hit rate along it ---------- */
  for(const law of ['boyle','charles','gay','avo']){
    const w=setupConfig({view:'sweep',law,sWin:6},null);
    const S=sweepStart(w,ST); sweepRunAll(w,ST);
    ok(S.done&&S.pts.length===SWEEP_N,law+': the sweep ran to '+SWEEP_N+' points ('+S.pts.length+')');
    if(S.pts.length!==SWEEP_N) continue;
    let worst=0, worstY=0, worstR=0, chi=0;
    for(const p of S.pts){
      worst=Math.max(worst,Math.abs(p.inv/S.pts[0].inv-1));
      worstY=Math.max(worstY,Math.abs(p.y/sweepExactY(S,p.x,w.g)-1));
      const e=Math.sqrt(p.n)/p.t; chi+=(p.rate-p.rateTh)/e; worstR=Math.max(worstR,Math.abs(p.rate/p.rateTh-1));
    }
    ok(worst<1e-6,law+': the invariant '+lawOf(law).inv+' is flat to '+worst.toExponential(1)+' across the sweep');
    /* Charles is the one law whose controller has to SOLVE for the width, and
       PhET rounds that width to five decimals (|Δw| ≤ 5e-6 pm, 1e-9 of a 5 nm
       box, accumulating over the ~200 updates a step takes).  The other three
       only rescale kinetic energies, which is exact. */
    const tolY=law==='charles'?1e-7:1e-9;
    ok(worstY<tolY,law+': every measured point is on the exact line to '+worstY.toExponential(1)
       +(law==='charles'?' (PhET rounds the held-P width to 5 decimals)':''));
    /* the five hit-rate residuals are independent, so their sum is ±√5 sd */
    ok(Math.abs(chi)<3*Math.sqrt(SWEEP_N),law+': the measured hit rates track kinetic theory (Σ residual/σ = '+fmt(chi,2)+', |Σ| < '+fmt(3*Math.sqrt(SWEEP_N),2)+'; worst point '+fmt(100*worstR,1)+' %)');
    ok(S.pts.every(p=>isFinite(p.rate)&&p.rate>0),law+': every swept point measured a rate');
    /* the counting window is what the slider says, not some fraction of it */
    let worstT=0; for(const p of S.pts) worstT=Math.max(worstT,Math.abs(p.t/ST.sWin-1));
    ok(worstT<0.02,law+': every point counted for the '+ST.sWin+' ps the slider asks for (worst '+fmt(100*worstT,1)+' % off)');
  }
  { /* THE SWEEP DOES NOT USE THE PUMP.  PhET's pump puts every new particle at
       one point, (−r, H/5); a wall-hit rate measured before that clump has
       spread is the rate of the clump (it read 38 % low).  Assert directly
       that the sweep's own count-setter leaves the gas spread out: a 600 ×
       600 pm patch around the entry point holds 0.41 % of a uniform gas. */
    const nearEntry=gg=>{ let c=0; for(let i=0;i<gg.n;i++)
      if(Math.abs(gg.x[i]+gg.species[0].r)<300&&Math.abs(gg.y[i]-GAS.ENTRY_Y)<300) c++; return c; };
    /* drive the REAL sweep, not the helper: the difference lives in the call
       site inside sweepApply */
    const w=setupConfig({view:'sweep',law:'avo',sN:100,sWin:2},null);
    const S=sweepStart(w,ST);
    S.i=S.targets.length-1;                      /* the biggest target: 2 × sN */
    sweepApply(w,S);
    eq(gasCount(w.g,0),S.targets[S.i],'the Avogadro sweep took the count to '+S.targets[S.i]);
    const N2=gasCount(w.g,0), want=N2*(600*600)/(GAS.WDEF*GAS.H);
    ok(nearEntry(w.g)<=want+4*Math.sqrt(want)+2,'… spread out, not piled at the entry point ('+nearEntry(w.g)+' within 300 pm of it, uniform would be '+fmt(want,2)+')');
    const g2=gasMake({seed:59,noLid:true}); gasFill(g2,0,100,300);
    gasSetCount(g2,0,200);
    ok(nearEntry(g2)>50,'… whereas PhET’s pump puts all '+nearEntry(g2)+' of them there at once'); }
  { /* THE SETTLE IS LOAD-BEARING.  Boyle's first target halves the width, and
       the Ideal wall's redistribution scales the x positions, which pushes
       disks into each other — tens of overlapping pairs at once.  They pass
       through and separate (the engine's rule), but until they have, the wall
       statistics are of a gas that is not there.  The settle is exactly long
       enough for that transient. */
    const g=gasMake({seed:53,noLid:true}); gasFill(g,0,100,300);
    const over=gg=>{ let c=0; for(let i=0;i<gg.n;i++) for(let j=i+1;j<gg.n;j++)
      if(Math.hypot(gg.x[i]-gg.x[j],gg.y[i]-gg.y[j])<gasRad(gg,i)+gasRad(gg,j)) c++; return c; };
    eq(over(g),0,'the fill starts with no overlapping pairs');
    gasResize(g,GAS.WMIN,true);
    ok(over(g)>0,'halving the width puts '+over(g)+' pairs on top of each other');
    for(let f=0;f<SWEEP_SETTLE;f++) gasStep(g,GAS.DT_FRAME);
    eq(over(g),0,'… and the sweep’s '+SWEEP_SETTLE+'-frame settle ('+fmt(SWEEP_SETTLE*GAS.DT_FRAME,1)+' ps) is enough for every one of them to separate'); }
  { /* Boyle really does squeeze: the narrowest box has the highest pressure */
    const w=setupConfig({view:'sweep',law:'boyle',sWin:5},null);
    const S=sweepStart(w,ST); sweepRunAll(w,ST);
    ok(S.pts[0].P>S.pts[SWEEP_N-1].P*2.9,'Boyle: 5 nm gives ~3× the pressure of 15 nm ('+fmt(S.pts[0].P/S.pts[SWEEP_N-1].P,3)+')');
    ok(S.pts[0].rate>S.pts[SWEEP_N-1].rate,'… and the walls are struck more often in the narrow box');
    let mono=true; for(let i=1;i<SWEEP_N;i++) if(!(S.pts[i].T>0&&Math.abs(S.pts[i].T/S.pts[0].T-1)<1e-9)) mono=false;
    ok(mono,'… while the temperature never moves (the Ideal wall does no work)'); }
  { /* the Ideal wall: no work, and the disks are SPREAD over the new width.
       gasWidthTo only moves the wall; nothing puts a disk back inside, so
       without the redistribution a narrowing leaves particles outside the box
       (drawn outside it, and struck by nothing). */
    const g=gasMake({seed:31,noLid:true}); gasFill(g,0,150,300); gasRefresh(g);
    const T0=gasTemp(g), xs=[]; for(let i=0;i<g.n;i++) xs.push(g.x[i]);
    gasResize(g,GAS.WMIN,true);
    rel(gasTemp(g),T0,1e-15,'the Ideal wall does no work: T unchanged by a 10 → 5 nm resize');
    let outside=0, worstShift=0, rMax=0;
    for(let i=0;i<g.n;i++){ const r=gasRad(g,i); rMax=Math.max(rMax,r);
      if(g.x[i]-r<g.left-1e-9||g.x[i]+r>1e-9) outside++;
      worstShift=Math.max(worstShift,Math.abs(g.x[i]-xs[i]*0.5)); }
    eq(outside,0,'every disk is inside the narrowed box');
    /* x -> x·(w/W) about the RIGHT wall (x = 0), then a clamp that can move a
       disk by at most its own radius off either end */
    ok(worstShift<=rMax+1e-9,'… because every x was scaled by w/W = 0.5 about the right wall, then clamped by at most one radius (worst shift '+fmt(worstShift,1)+' pm, r = '+fmt(rMax,1)+')');
    const g2=gasMake({seed:31,noLid:true}); gasFill(g2,0,150,300);
    gasResize(g2,GAS.WMIN,false);
    let outside2=0; for(let i=0;i<g2.n;i++) if(g2.x[i]-gasRad(g2,i)<g2.left-1e-9) outside2++;
    ok(outside2>0,'… and WITHOUT the redistribution '+outside2+' of them would be left outside it'); }
  { /* PhET's lid: above 20,000 kPa it blows off, unless the gap is already
       1500 pm or wider — then the gas just vents.  The two gaps below are
       ABSOLUTE (1700 and 1200 pm), not written in terms of LID_WIDE: a test
       whose own setup is measured in the constant it is meant to pin moves
       with that constant and sees nothing. */
    close(GAS.LID_WIDE,1500,1e-12,'PhET’s blow-off gap is 1500 pm');
    const g=gasMake({seed:37}); gasFill(g,0,600,900); g.pOn=true; gasRefresh(g);
    ok(g.P>GAS.P_MAX,'600 disks at 900 K in the 10 nm box are past 20,000 kPa ('+fmt(g.P,0)+')');
    ok(g.lid.on===false,'… so the closed lid blew off');
    const g2=gasMake({seed:37}); gasFill(g2,0,600,900);
    gasSetLid(g2,gasMaxLid(g2)-1700); g2.pOn=true;
    close(gasOpening(g2),1700,1e-9,'a gap of exactly 1700 pm, wider than the 1500 blow-off gap');
    gasRefresh(g2);
    ok(g2.lid.on===true,'… and at that gap the lid stays on: the gas vents instead');
    const g3=gasMake({seed:37}); gasFill(g3,0,600,900);
    gasSetLid(g3,gasMaxLid(g3)-1200); g3.pOn=true;
    close(gasOpening(g3),1200,1e-9,'a gap of exactly 1200 pm, narrower than it');
    gasRefresh(g3);
    ok(g3.lid.on===false,'… and at that gap the lid goes'); }
  { /* PhET's gauge refreshes every 0.75 ps, not every frame */
    const g=gasMake({seed:41,noLid:true,noise:false}); gasFill(g,0,100,300); g.pOn=true; gasRefresh(g);
    const p0=g.gaugeP;
    gasSetTemp(g,600);                         /* the true P doubles at once */
    gasStep(g,0.5); ok(g.P>1.9*p0,'the noise-free P follows the temperature at once');
    eq(g.gaugeP,p0,'… but after 0.5 ps the GAUGE has not moved yet');
    gasStep(g,0.3); ok(g.gaugeP>1.9*p0,'… and at 0.8 ps, past PhET’s 0.75 ps refresh, it has');
    let refreshes=0, last=g.gaugeP;
    for(let f=0;f<240;f++){ gasStep(g,GAS.DT_FRAME); if(g.gaugeP!==last){ refreshes++; last=g.gaugeP; } }
    ok(refreshes<=Math.ceil(10/GAS.P_REFRESH)+1,'over 10 ps the gauge refreshed at most '+Math.ceil(10/GAS.P_REFRESH)+' times ('+refreshes+')'); }
  { /* PhET rounds the held-pressure width to FIVE decimals, and the size of
       that rounding is what the sweep's residual measures.  Ask for a width
       that is nowhere near a round number (137 disks going 317 K -> 200 K) and
       the invariant V/T can only stay put to 8e-10 if the rounding really is
       at the fifth decimal; at the first it would move by 8e-6. */
    const g=gasMake({seed:19,noLid:true}); gasFill(g,0,137,317); g.pOn=true; gasRefresh(g);
    const inv0=gasVolume(g)/1e9/gasTemp(g), W0=g.W;
    ok(gasSetHold(g,'pressureV'),'hold P↕V engaged');
    gasSetTemp(g,200); gasRefresh(g);
    const inv1=gasVolume(g)/1e9/gasTemp(g);
    ok(g.W!==W0&&g.W>6000&&g.W<6700,'the controller moved the wall to '+fmt(g.W,5)+' pm');
    ok(Math.abs(g.W*1e5-Math.round(g.W*1e5))<1e-6,'… landing on PhET’s five-decimal grid');
    ok(Math.abs(inv1/inv0-1)<1e-8,'… and V/T is unchanged to '+(Math.abs(inv1/inv0-1)).toExponential(1)+' (five decimals of 6309 pm is 8e-10; one decimal would be 8e-6)'); }
  { /* holding T while particles are REMOVED: PhET rescales what is left back
       to the temperature it had (gasAfterRemove), which is a different branch
       from the empty-box Oops below */
    const g=gasMake({seed:23,noLid:true}); gasFill(g,0,200,437); gasRefresh(g);
    ok(gasSetHold(g,'temperature'),'hold T engaged with 200 disks');
    const T0=gasTemp(g);
    gasRemove(g,0,120);
    eq(gasCount(g,0),80,'120 removed, 80 left');
    rel(gasTemp(g),T0,1e-12,'… and holding T restored the temperature of what is left ('+fmt(gasTemp(g),2)+' K)');
    eq(g.hold,'temperature','… without dropping the hold');
    const g2=gasMake({seed:23,noLid:true}); gasFill(g2,0,200,437); gasRefresh(g2);
    const E0=gasEnergy(g2); gasRemove(g2,0,120);
    ok(Math.abs(gasTemp(g2)-T0)<1e-12||gasCount(g2,0)===80,'… with no hold, removing is just removing');
    ok(gasEnergy(g2)<E0,'… and the energy simply leaves with the particles'); }
  { /* The lone trace marker must not contradict the readout beside it.  A
       fresh view has exactly one trace point, taken at t = 0; erase the gas
       while paused and that point still describes the gas that was there. */
    const w=setupConfig({view:'intro'},null);
    eq(w.trace.length,1,'a fresh view has one trace point');
    ok(w.trace[0][2]>0,'… showing the gauge of the gas it was seeded with');
    gasRemoveAll(w.g); gasRefresh(w.g);
    const c=makeShot(1400,820); drawView(c,1400,820,buildModel());
    eq(w.trace.length,1,'… still one after erasing');
    eq(w.trace[0][2],0,'… but the draw re-seeded it: the gauge point is 0, as the readout says');
    ok(!isFinite(w.trace[0][1]),'… and its temperature is not a number, as the readout’s “—” says'); }
  { /* The hottest isotherm only clips the TOP-RIGHT corner of the P-V box, so
       its label has to hang leftwards from the entry point; hanging rightwards
       it is clamped to the canvas edge and ends up outside its own frame.
       (The label registry clamps to the CANVAS, not to the plot.) */
    setupConfig({view:'pv'},null);
    const c=makeShot(1400,820), M0=buildModel();
    drawView(c,1400,820,M0);
    const G=viewGeo(c,1400,820,M0), b=G.plots[0];
    const want=ISO_T[ISO_T.length-1]+' K';
    const hits=c.ops.filter(o=>o.op==='text'&&o.t===want);
    eq(hits.length,1,'the hottest isotherm ('+want+') is labelled exactly once');
    if(hits.length===1) ok(hits[0].bb[0]>=b.x-1&&hits[0].bb[2]<=b.x1+1,
      '… and its label sits inside the plot frame (['+fmt(hits[0].bb[0],0)+', '+fmt(hits[0].bb[2],0)
      +'] inside ['+fmt(b.x,0)+', '+fmt(b.x1,0)+'])');
    for(const T of ISO_T) ok(c.ops.some(o=>o.op==='text'&&o.t===T+' K'),'the '+T+' K isotherm is labelled');
    /* The entry point moves with the axis: cooling the gas to 290 K raises the
       hottest isotherm's entry to V = 524.9 nm³, a tenth of a nm³ from the
       right edge, and a label hung rightwards from there runs off the plot.
       This is the state the leftward fallback exists for, so pin it here —
       at the default 300 K the label fits either way and pins nothing. */
    const w2=setupConfig({view:'pv'},null);
    gasSetTemp(w2.g,290); gasRefresh(w2.g);
    const c2=makeShot(1400,820), M2=buildModel();
    drawView(c2,1400,820,M2);
    const G2=viewGeo(c2,1400,820,M2), b2=G2.plots[0];
    const h2=c2.ops.filter(o=>o.op==='text'&&o.t===want);
    eq(h2.length,1,'cooled to 290 K, the hottest isotherm is still labelled once');
    if(h2.length===1){
      ok(h2[0].bb[2]<=b2.x1+1,'… and its label is still inside the plot frame (right edge '
        +fmt(h2[0].bb[2],0)+' vs '+fmt(b2.x1,0)+')');
      ok(h2[0].bb[2]>b2.x1-90,'… hard against it, which is what makes this the case that pins the fallback'); } }
  { /* the Oops cases PhET raises */
    const w=setupConfig({view:'laws'},null), g=w.g;
    ok(gasSetHold(g,'temperature'),'hold T is allowed with particles and a closed lid');
    gasRemoveAll(g);
    eq(g.hold,'nothing','erasing while holding T drops the hold'); eq(g.oops,'temperatureEmpty','… and raises PhET’s Oops');
    ok(/Temperature cannot be held constant/.test(GAS_OOPS[g.oops]),'… with PhET’s own wording');
    const w2=setupConfig({view:'laws'},null), g2=w2.g;
    gasSetLid(g2,3000); ok(!gasHoldAllowed(g2,'temperature'),'with the lid open, hold T is refused');
    const w3=setupConfig({view:'laws'},null), g3=w3.g;
    gasSetHold(g3,'pressureV'); g3.heat=1;
    for(let f=0;f<900&&g3.hold==='pressureV';f++) gasStep(g3,GAS.DT_FRAME);
    eq(g3.oops,'pressureLarge','holding P while heating runs the container past 15 nm: Oops');
    eq(g3.hold,'nothing','… and the hold drops to Nothing'); }
  TIMES.G=Date.now();

  /* ---------- H. every configuration: the readout, then the layout at four sizes ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,fn] of CONFIGS){
    setupConfig(over,fn); const M0=buildModel();
    const txt=readoutHTML(M0)+eqbarHTML(M0)+tagHTML(M0)+(INFO[ST.view]||'')+(DERIV[ST.view]||'');
    ok(!/NaN|undefined|Infinity/.test(txt),nm+': readout, eqbar, tag and prose clean');
    ok(txt.indexOf(' K')>=0||txt.indexOf('°C')>=0||M0.N===0,nm+': the readout shows a temperature');
    for(const [W,H] of SIZES){
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(fills.length>=3&&texts.length>=2,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, '+texts.length+' texts)');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
        const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>3&&oy>3){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      /* the house #hint (HTML, bottom: 11px, 11px type) owns the bottom-left
         corner and the canvas capture cannot see it: no canvas text may reach it */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
    }
  }
  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section H');
  TIMES.H=Date.now();

  /* ---------- I. no slider combination produces a non-finite value ---------- */
  { let bad=null;
    for(const view of TABS.map(t=>t[0]))
      for(const nH of [0,1,100,400])
        for(const T of [50,300,1000])
          for(const w2 of [GAS.WMIN,GAS.WDEF,GAS.WMAX]){
            const g=gasMake({seed:13,width:w2}); if(nH) gasFill(g,0,nH,T);
            g.pOn=nH>0; gasRefresh(g);
            const vals=[hitRateTheory(g,true),hitRateTheory(g,false),gasPressureOf(nH,g.T,gasVolume(g)),g.T];
            for(const v of vals) if(v!==null&&!isFinite(v)) bad=view+' N='+nH+' T='+T+' w='+w2+' → '+v;
          }
    ok(!bad,'no view × count × temperature × width gives a non-finite value ('+(bad||'ok')+')'); }
  { /* the sweep survives its extremes (a 2-ps window: this is a crash test,
       not a measurement) */
    let err=null, done=0, oops=null;
    try{ for(const law of ['boyle','charles','gay','avo'])
      for(const sN of [20,400]) for(const sT of [100,600]){
        const w=setupConfig({view:'sweep',law,sN,sT,sWin:2},null);
        sweepStart(w,ST); sweepRunAll(w,ST,2000);
        if(w.sweep.done) done++;
        if(w.g.oops) oops=law+' at N='+sN+' T='+sT+': '+w.g.oops;
        const M=buildModel(); const c=makeShot(1400,820); drawView(c,1400,820,M);
      } }catch(e){ err=e; }
    ok(!err,'every law × 20/400 disks × 100/600 K sweeps and draws'+(err?': '+(err.stack||err):''));
    ok(done===16,'… and all 16 of them ran to the end ('+done+')');
    /* the Charles targets are clamped a hair inside the container's range
       precisely so the controller's toFixed(5) cannot round past the end */
    ok(!oops,'… and not one of them raised an Oops'+(oops?' ('+oops+')':''));
    /* the clamp itself: the extreme Charles targets must ask for a width
       STRICTLY inside the container, so the controller's toFixed(5) has
       somewhere to round to */
    const w2=setupConfig({view:'sweep',law:'charles',sWin:2},null);
    const S2=sweepStart(w2,ST), N2=S2.N0, Pm=S2.P0/GAS.P_SCALE;
    const wOf=T=>N2*GAS.K*T/Pm/(w2.g.H*w2.g.D);
    const wHi=wOf(Math.max.apply(null,S2.targets)), wLo=wOf(Math.min.apply(null,S2.targets));
    ok(wHi<GAS.WMAX&&wLo>GAS.WMIN,'the Charles targets stop a hair inside the container ('
      +fmt(wLo,5)+' … '+fmt(wHi,5)+' pm, inside '+GAS.WMIN+' … '+GAS.WMAX+')');
    ok(GAS.WMAX-wHi<1e-3&&wLo-GAS.WMIN<1e-3,'… but only a hair: the sweep still spans the whole range'); }

  TIMES.E=Date.now();
  console.log('section times, s: '+['F','G','H','E'].map((k,i,a)=>k+' '+((TIMES[k]-(i?TIMES[a[i-1]]:T0))/1000).toFixed(1)).join(', '));

  Object.assign(ST,stSave); resetAllWorlds();
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
