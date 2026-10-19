
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/gas-properties/refvals.txt, the printed output of   *
 *  derive.py, read in full; REF (p7a_refs.js) is the same numbers,     *
 *  written by derive.py so that none is retyped.                       *
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
/* a gas from explicit disks (the reference runs): [m, r, x, y, vx, vy] */
function gasFromList(list,o){
  const g=gasMake(Object.assign({width:GAS.WDEF,seed:1,virial:true},o||{}));
  for(const p of list) gasPush(g,p[0]===28?0:1,p[2],p[3],p[4],p[5]);
  gasLedgerReset(g); gasVirialReset(g); gasImpulseReset(g);
  return g;
}
function runFrames(g,frames,dt){ for(let f=0;f<frames;f++) gasStep(g,dt||GAS.DT_FRAME); }
/* the configurations the layout sweep and the capture share */
const CONFIGS=[
  ['ideal default',{view:'ideal'},null],
  ['ideal empty',{view:'ideal'},w=>{ gasRemoveAll(w.g); }],
  ['ideal crowded',{view:'ideal',showWatch:true,showCounter:true},w=>{ gasInject(w.g,0,300); gasInject(w.g,1,300); runFrames(w.g,6); }],
  ['ideal lid open',{view:'ideal'},w=>{ gasSetLid(w.g,3000); runFrames(w.g,60); }],
  ['ideal lid blown',{view:'ideal',unitP:'kPa'},w=>{ w.g.lid.on=false; runFrames(w.g,12); }],
  ['ideal hold P V',{view:'ideal',hold:'pressureV',heat:0.8},w=>{ gasSetHold(w.g,'pressureV'); for(let f=0;f<48;f++) worldStep(w,Object.assign({},ST,{heat:0.8}),GAS.DT_FRAME); }],
  ['ideal oops',{view:'ideal'},w=>{ gasSetHold(w.g,'temperature'); gasRemoveAll(w.g); }],
  ['ideal narrow wall',{view:'ideal',unitT:'C'},w=>{ gasResize(w.g,GAS.WMIN,true); gasRefresh(w.g); }],
  ['explore default',{view:'explore'},null],
  ['explore squeezed',{view:'explore'},w=>{ w.g.wantW=5000; for(let f=0;f<200;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['explore pulled',{view:'explore'},w=>{ w.g.wantW=15000; for(let f=0;f<200;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['energy default',{view:'energy'},null],
  ['energy no collisions',{view:'energy',coll:false,injMode:'set',injT:600,zoom:2},w=>{ w.g.collisions=false; w.g.injectT=600; gasInject(w.g,0,300); runFrames(w.g,30); }],
  ['energy empty',{view:'energy'},w=>{ gasRemoveAll(w.g); runFrames(w.g,30); }],
  ['diffusion default',{view:'diffusion'},null],
  ['diffusion mixing',{view:'diffusion',divided:false},w=>{ gasSetDivided(w.g,false); for(let f=0;f<240;f++) worldStep(w,Object.assign({},ST,{divided:false}),GAS.DT_FRAME); }],
  ['diffusion empty',{view:'diffusion',d1n:0,d2n:0},null],
  ['diffusion big',{view:'diffusion',d1n:200,d2n:200,d1r:250,d2r:50,d1m:32,d2m:4},null],
  ['pressure default',{view:'pressure'},w=>{ for(let f=0;f<120;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['pressure fresh',{view:'pressure'},null],
  ['pressure no collisions',{view:'pressure',pColl:false,pN:40},w=>{ for(let f=0;f<120;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['pressure dense',{view:'pressure',pN:400,pT:1000},w=>{ for(let f=0;f<48;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['equil delta',{view:'equil'},w=>{ for(let f=0;f<120;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['equil split',{view:'equil',eStart:'split'},w=>{ for(let f=0;f<120;f++) worldStep(w,ST,GAS.DT_FRAME); }],
  ['equil pump fresh',{view:'equil',eStart:'pump',eN:600},null],
  ['equil no collisions',{view:'equil',eColl:false,eN:40},w=>{ for(let f=0;f<60;f++) worldStep(w,ST,GAS.DT_FRAME); }],
];
function setupConfig(over,fn){
  Object.assign(ST,DEFAULTS,over); DRAG.what=null;
  resetAllWorlds();
  const w=worldOf(ST.view);
  if(fn) fn(w);
  if(BOXVIEWS[ST.view]){ ST.nH=gasCount(w.g,0); ST.nL=gasCount(w.g,1); }
  return w;
}

function selfTest(){
  let pass=0,fail=0;
  /* SELFTEST_VERBOSE (never set by the page) prints the passing lines too, so
     the measured numbers behind the statistical assertions can be read */
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
  rel(GAS.P_SCALE,REF.pConv,1e-15,'PRESSURE_CONVERSION_SCALE = KG_PER_AMU·1e36 Pa in kPa (derive)');
  rel(GAS.KG_PER_AMU*1e33,GAS.P_SCALE,1e-15,'the pressure scale is derived from the AMU, not independent');
  rel(GAS.ATM_PER_KPA,REF.atmPerKpaExact,3e-7,'ATM_PER_KPA is 1/101.325 to PhET’s 6 digits (derive)');
  eq(GAS.H,8750,'container height 8750 pm'); eq(GAS.D,4000,'container depth 4000 pm'); eq(GAS.WALL,75,'wall thickness 75 pm');
  eq(GAS.WMIN+'/'+GAS.WMAX+'/'+GAS.WDEF,'5000/15000/10000','width range 5–15 nm, default 10');
  eq(GAS.HEAVY.m+'/'+GAS.HEAVY.r+'/'+GAS.LIGHT.m+'/'+GAS.LIGHT.r,'28/125/4/87.5','masses and radii (PhET)');
  eq(GAS.HEAT_COOL+'/'+GAS.P_MAX+'/'+GAS.T_MAX+'/'+GAS.WALL_SPEED,'800/20000/100000/800','heatCool, maxPressure, maxTemperature, wallSpeedLimit');
  eq(GAS.LID_THICK+'/'+GAS.OPEN_L+'/'+GAS.OPEN_R,'175/1250/2000','lid thickness and opening insets');
  close(GAS.ENTRY_Y,1750,1e-12,'the entry point is H/5 = 1750 pm up the right wall');
  rel(GAS.DT_FRAME,REF.dtFrame,1e-15,'one frame is 1/24 ps (1 ps = 0.4 s at 60 fps)'); close(GAS.DT_SLOW,0.005,1e-15,'slow: 0.3 ps per s');
  eq(GAS.NBIN+'/'+GAS.SBIN+'/'+GAS.EBIN,'19/170/800000','PhET histogram bins');
  eq(GAS.DIFF_W+'/'+GAS.DIVIDER+'/'+GAS.DIFF_NMAX,'16000/100/200','diffusion box, divider, count');
  eq(GAS.PERIODS.join(','),'5,10,20','collision counter periods');
  rel(gasPressureOf(100,300,GAS.WDEF*GAS.H*GAS.D),REF.P100kPa,1e-15,'P = NkT/V: 100 disks at 300 K in 10 nm = 1183.248 kPa (derive)');
  rel(gasPressureOf(100,300,GAS.WDEF*GAS.H*GAS.D)*GAS.ATM_PER_KPA,REF.P100atm,1e-15,'… = 11.678 atm (derive)');
  rel(gasPressureOf(1000,1000,GAS.WMIN*GAS.H*GAS.D),REF.PmaxCase,1e-14,'1000 at 1000 K in 5 nm: 78,883 kPa, past the lid limit (derive)');
  rel(gasKT2(300),REF.kT2_300,1e-15,'kT2 = (3/2)kT = 3,742,200 at 300 K (derive)');
  rel(mbMeanSpeed(28,gasKT2(300)),REF.vMean_heavy,1e-14,'heavy <v> = 458.19 m/s (derive, scipy quad)');
  rel(mbMeanSpeed(4,gasKT2(300)),REF.vMean_light,1e-14,'light <v> = 1212.25 m/s (derive)');
  rel(mbModeSpeed(28,gasKT2(300)),REF.vMode_heavy,1e-14,'heavy most probable speed (derive)');
  rel(mbRmsSpeed(28,gasKT2(300)),REF.vInj_heavy,1e-14,'the rms speed IS PhET’s injection speed sqrt(3kT/m) (derive)');
  rel(zJ(1),REF.zJperUnit,1e-15,'1 AMU pm²/ps² = 1.66e-6 zJ (PhET’s AMU)');

  /* ---------- B. the random stream and PhET's injection, bit for bit ---------- */
  { const R=gasRng(12345); for(let k=0;k<5;k++) eq(R.next(),REF.rng12345[k],'mulberry32(12345) draw '+k+' (derive, bit-exact)'); }
  { const g=gasMake({seed:2024}); eq(gasInject(g,0,6,300),6,'six heavy injected');
    for(let i=0;i<6;i++){ close(g.vx[i],REF.inject2024[i][2],1e-12,'injected vx #'+i+' (derive)'); close(g.vy[i],REF.inject2024[i][3],1e-12,'injected vy #'+i+' (derive)');
      eq(g.x[i],-125,'enters at x = -r'); eq(g.y[i],1750,'at y = H/5'); }
    rel(gasTemp(g),300,1e-14,'the Gaussian temperatures’ mean is restored: T = 300 K exactly');
    let fanOK=true; for(let i=0;i<6;i++){ const th=Math.atan2(g.vy[i],g.vx[i]), a=th<0?th+TAU:th; if(a<0.75*PI-1e-12||a>1.25*PI+1e-12) fanOK=false; }
    ok(fanOK,'every injected direction is inside the pump’s π/2 fan, pointing left');
    const g1=gasMake({seed:5}); gasInject(g1,1,1,450); rel(gasSpeed(g1,0),Math.sqrt(3*GAS.K*450/4),1e-15,'one particle: exactly sqrt(3kT/m), no spread');
    const g2=gasMake({seed:5,collisions:false}); gasInject(g2,0,10,300); let same=true; for(let i=1;i<10;i++) if(Math.abs(gasSpeed(g2,i)-gasSpeed(g2,0))>1e-9) same=false;
    ok(same,'collisions off: every injected particle at the same speed (PhET)');
    const g3=gasMake({seed:9}); gasInject(g3,0,2000,300); eq(gasCount(g3,0),GAS.NMAX,'injection stops at 1000 per species'); }

  /* ---------- C. the collision-time algebra ---------- */
  { const P=REF.pair1;
    rel(pairTime(P.pi[0]-P.pj[0],P.pi[1]-P.pj[1],P.vi[0]-P.vj[0],P.vi[1]-P.vj[1],P.ri+P.rj),P.t,1e-15,'contact time = 5/2 exactly (derive, rational)');
    eq(pairTime(0,300,0,-10,250)===Infinity,false,'head-on approach collides');
    eq(pairTime(0,300,0,10,250),Infinity,'separating: no event'); eq(pairTime(0,200,0,-10,250),Infinity,'overlapping: no event (they pass through, as in PhET)');
    eq(pairTime(0,300,10,0,250),Infinity,'b = 0 (sliding past): no event'); eq(pairTime(1000,300,-10,0,250),Infinity,'miss: discriminant < 0');
    eq(pairTime(0,249.999,0,-10,250),Infinity,'overlapping by a hair (c = −0.5 pm²) and approaching: still no event');
    close(pairTime(0,500,0,-100,250),2.5,1e-15,'head-on: (500-250)/100 = 2.5');
    const g=gasMake({seed:1}); gasPush(g,0,P.pi[0]+P.vi[0]*P.t,P.pi[1]+P.vi[1]*P.t,P.vi[0],P.vi[1]); gasPush(g,1,P.pj[0]+P.vj[0]*P.t,P.pj[1]+P.vj[1]*P.t,P.vj[0],P.vj[1]);
    g.species[1].r=125; const vir=pairResolve(g,0,1);
    close(g.vx[0],P.vi2[0],1e-12,'post-collision vi_x = 1091/5 (derive, rational)'); close(g.vy[0],P.vi2[1],1e-12,'vi_y = -12/5');
    close(g.vx[1],P.vj2[0],1e-12,'vj_x = 863/5'); close(g.vy[1],P.vj2[1],1e-12,'vj_y = 1484/5');
    ok(vir>0,'the pair virial σ|J| is positive'); }
  { /* the grid finds every collision a substep can hold: 20 head-on pairs of heavy
       disks at 3000 m/s each, 300 pm apart (they touch 8.3 fs in), their offsets
       stepped 29 pm across 550 pm, wider than any cell, so some pair straddles every
       cell boundary: all 20 must have bounced after one frame */
    const g=gasMake({seed:1,noLid:true});
    for(let j=0;j<20;j++){ const x1=-9000+29*j, y=300+400*j; gasPush(g,0,x1,y,3000,0); gasPush(g,0,x1+300,y,-3000,0); }
    gasStep(g,GAS.DT_FRAME);
    let bounced=0; for(let j=0;j<20;j++) if(g.vx[2*j]<0&&g.vx[2*j+1]>0&&g.x[2*j]<g.x[2*j+1]) bounced++;
    eq(bounced,20,'every one of 20 fast head-on pairs is found by the grid and bounces'); eq(g.stats.pairHits,20,'exactly 20 collisions'); }
  { /* conservation to rounding over 5000 random collisions, masses 1..40 */
    const R=gasRng(77); let worstP=0, worstE=0, worstT=0;
    for(let q=0;q<5000;q++){
      const g=gasMake({seed:1, species:[{m:1+39*R.next(),r:50+200*R.next()},{m:1+39*R.next(),r:50+200*R.next()}]});
      const s=g.species[0].r+g.species[1].r, th=TAU*R.next();
      gasPush(g,0,0,0,2000*(R.next()-0.5),2000*(R.next()-0.5)); gasPush(g,1,s*Math.cos(th),s*Math.sin(th),2000*(R.next()-0.5),2000*(R.next()-0.5));
      const nx=Math.cos(th), ny=Math.sin(th);
      if((g.vx[0]-g.vx[1])*(-nx)+(g.vy[0]-g.vy[1])*(-ny)>=0) continue;
      const m0=g.species[0].m, m1=g.species[1].m, px=m0*g.vx[0]+m1*g.vx[1], py=m0*g.vy[0]+m1*g.vy[1], E=gasEnergy(g);
      const tan0=(g.vx[0]-g.vx[1])*(-ny)+(g.vy[0]-g.vy[1])*nx;
      pairResolve(g,0,1);
      const px1=m0*g.vx[0]+m1*g.vx[1], py1=m0*g.vy[0]+m1*g.vy[1], P0=Math.hypot(m0*g.vx[0],m0*g.vy[0])+Math.hypot(m1*g.vx[1],m1*g.vy[1]);
      worstP=Math.max(worstP,Math.hypot(px1-px,py1-py)/P0); worstE=Math.max(worstE,Math.abs(gasEnergy(g)-E)/E);
      worstT=Math.max(worstT,Math.abs((g.vx[0]-g.vx[1])*(-ny)+(g.vy[0]-g.vy[1])*nx-tan0)/(Math.abs(tan0)+1));
    }
    ok(worstP<1e-14,'5000 random collisions: momentum conserved to '+worstP.toExponential(2)+' (< 1e-14)');
    ok(worstE<1e-14,'… energy conserved to '+worstE.toExponential(2)+' (< 1e-14)');
    ok(worstT<1e-12,'… the tangential relative velocity unchanged to '+worstT.toExponential(2)); }

  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section A-C');
  TIMES.A=Date.now();
  /* ---------- D. walls, and the brute-force reference runs ---------- */
  { /* one disk against the moving wall: contact time and 2u - v (derive, rational) */
    const g=gasMake({seed:1, doesWork:true, wallSpeed:150}); gasPush(g,0,-9000,4000,-400,0); gasLedgerReset(g);
    g.wantW=10000-150*REF.wallTc*2;
    for(let f=0;f<48;f++) gasStep(g,GAS.DT_FRAME);
    close(g.vx[0],REF.wallVx2,1e-9,'the wall at 150 m/s sends a -400 m/s disk back at 2u - v = 700 (derive)');
    rel(g.led.work,REF.wallWork,1e-12,'and does 2mu(u - v) = 4,620,000 of work (derive)');
    close(gasLedger(g).resid,0,1e-6,'energy ledger: KE = start + work'); }
  { const g=gasFromList(REF.R1init); runFrames(g,600);
    let worst=0; for(let i=0;i<5;i++) for(let q=0;q<4;q++) worst=Math.max(worst,Math.abs([g.x[i],g.y[i],g.vx[i],g.vy[i]][q]-REF.R1final[i][q]));
    ok(worst<1e-5,'R1: five disks, 25 ps, match the brute-force event-driven run to '+worst.toExponential(2)+' (derive)');
    eq(g.stats.pairHits,REF.R1pairs,'R1 pair collisions (derive)'); eq(g.stats.wallHits,REF.R1walls,'R1 wall collisions (derive)');
    eq(gasEnergy(g),REF.R1E,'R1 total KE conserved exactly: 9,101,200');
    const V=gasVirial(g); ok(Math.abs(V.resid)/V.scale<1e-12,'R1 virial ledger closes to '+(Math.abs(V.resid)/V.scale).toExponential(2)+' of its terms');
    rel(g.vir.kin,REF.R1kin,1e-12,'R1 ∫2KE dt (derive)'); rel(g.vir.wall,REF.R1virWall,1e-9,'R1 wall virial Σ r·J (derive)'); rel(g.vir.pair,REF.R1virPair,1e-9,'R1 pair virial Σ σ|J| (derive)');
    eq(g.stats.fastMiss+g.stats.eventCap,0,'R1: no speed-bound or event-cap flags'); }
  { const g=gasFromList(REF.R2init,{doesWork:true,wallSpeed:300}); g.wantW=8500; runFrames(g,600);
    let worst=0; for(let i=0;i<6;i++) for(let q=0;q<4;q++) worst=Math.max(worst,Math.abs([g.x[i],g.y[i],g.vx[i],g.vy[i]][q]-REF.R2final[i][q]));
    ok(worst<1e-5,'R2: the wall pushed in at 300 m/s for 5 ps: match to '+worst.toExponential(2)+' (derive)');
    eq(g.stats.pairHits,REF.R2pairs,'R2 pair collisions (derive)'); eq(g.stats.wallHits,REF.R2walls,'R2 wall collisions (derive)');
    rel(g.led.work,REF.R2work,1e-12,'R2 work done by the wall = 23,040,000 (derive)');
    eq(g.W,8500,'the wall stopped at 8.5 nm');
    close(gasLedger(g).resid/gasEnergy(g),0,1e-14,'R2 energy ledger closes');
    const V=gasVirial(g); ok(Math.abs(V.resid)/V.scale<1e-12,'R2 virial ledger (moving wall) closes to '+(Math.abs(V.resid)/V.scale).toExponential(2)); }
  { const g=gasFromList(REF.R4init); runFrames(g,720);
    let worst=0; for(let i=0;i<12;i++) for(let q=0;q<4;q++) worst=Math.max(worst,Math.abs([g.x[i],g.y[i],g.vx[i],g.vy[i]][q]-REF.R4final[i][q]));
    ok(worst<1e-4,'R4: twelve disks, 30 ps, 11 collisions: match to '+worst.toExponential(2)+' (derive)');
    eq(g.stats.pairHits,REF.R4pairs,'R4 pair collisions (derive)'); eq(g.stats.wallHits,REF.R4walls,'R4 wall collisions (derive)');
    rel(g.vir.pair,REF.R4virPair,1e-8,'R4 pair virial (derive)'); }
  { /* R5: three predictions go stale inside the first substep (a pair event
       stale in its partner, one stale in its owner, a wall event whose disk was
       struck first); each must be skipped, or a disk touching nothing is kicked */
    const g=gasFromList(REF.R5init); runFrames(g,24);
    let worst=0; for(let i=0;i<8;i++) for(let q=0;q<4;q++) worst=Math.max(worst,Math.abs([g.x[i],g.y[i],g.vx[i],g.vy[i]][q]-REF.R5final[i][q]));
    ok(worst<1e-5,'R5: stale predictions, 1 ps: match to '+worst.toExponential(2)+' (derive)');
    eq(g.stats.pairHits,REF.R5pairs,'R5 pair collisions: the three strikes (derive)'); eq(g.stats.wallHits,REF.R5walls,'R5 wall collisions (derive)');
    eq(g.stats.stale,3,'R5: exactly the three stale predictions were popped and skipped'); }
  { const g=gasFromList(REF.R3init,{collisions:false}); runFrames(g,960);
    let worst=0; for(let i=0;i<12;i++) for(let q=0;q<4;q++) worst=Math.max(worst,Math.abs([g.x[i],g.y[i],g.vx[i],g.vy[i]][q]-REF.R3final[i][q]));
    ok(worst<1e-6,'R3: collisions off, 40 ps: match to '+worst.toExponential(2)+' (derive)'); eq(g.stats.wallHits,REF.R3walls,'R3 wall hits (derive)');
    let spd=true; for(let i=0;i<12;i++) if(Math.abs(Math.abs(g.vx[i])-Math.abs(REF.R3init[i][4]))>1e-9) spd=false; ok(spd,'collisions off: every |v_x| is a constant of the motion'); }
  { /* hard disks never overlap: 400 heavy disks at area fraction 0.22, 4 ps, every
       pair checked every frame.  A collision the event search misses (a partner
       left out of a re-prediction, a cell too small) lets two disks slide into
       each other, and PhET's overlap rule then lets them pass through */
    const g=gasMake({seed:31}); gasFill(g,0,400,300);
    let worst=Infinity, bad=0;
    for(let f=0;f<96;f++){ gasStep(g,GAS.DT_FRAME);
      for(let i=0;i<g.n;i++) for(let j=i+1;j<g.n;j++){ const dx=g.x[i]-g.x[j], dy=g.y[i]-g.y[j], d=Math.sqrt(dx*dx+dy*dy)-250; if(d<worst) worst=d; if(d<-1e-6) bad++; } }
    eq(bad,0,'400 disks at area fraction 0.22, 4 ps, every pair every frame: never closer than σ (closest '+worst.toExponential(2)+' pm)');
    ok(g.stats.pairHits>500,'… through '+g.stats.pairHits+' collisions'); }

  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section D');
  TIMES.D=Date.now();
  /* ---------- F. PhET's model: gauge, holds, Oops, lid, heater, wall, samplers ---------- */
  { const g=gasMake({seed:3}); gasInject(g,0,100,300);
    gasStep(g,GAS.DT_FRAME); eq(g.P,0,'the gauge reads 0 until the first wall hit');
    let f=0; while(!g.pOn&&f<200){ gasStep(g,GAS.DT_FRAME); f++; } ok(g.pOn,'then it switches on');
    rel(g.P,gasPressureOf(100,gasTemp(g),gasVolume(g)),1e-15,'and reads NkT/V');
    const g2=gasMake({seed:4}); gasFill(g2,0,100,300); pressureOnAfterFill(g2); g2.noiseOn=false; gasRefresh(g2);
    rel(g2.gaugeP,REF.P100kPa,1e-12,'100 heavy at 300 K, 10 nm: the gauge shows 1183.248 kPa (noise off, derive)');
    g2.noiseOn=true; let dev=0; for(let q=0;q<200;q++){ g2.pAcc=GAS.P_REFRESH; gasUpdate(g2,0,0); dev=Math.max(dev,Math.abs(g2.gaugeP-g2.P)); }
    ok(dev<=REF.noiseMax+1e-9&&dev>REF.noiseMax*0.8,'PhET’s noise law: |gauge − P| ≤ 50(1 − P/20000) = '+REF.noiseMax.toFixed(2)+' kPa (max seen '+dev.toFixed(2)+')');
    g2.hold='pressureV'; g2.pAcc=GAS.P_REFRESH; gasUpdate(g2,0,0); close(g2.gaugeP,g2.P,1e-9,'no noise while P is held'); g2.hold='nothing'; }
  { /* hold P↕V: heat and the wall walks out with P fixed; cool past the limit: Oops */
    const w=setupConfig({view:'ideal'},null), g=w.g;
    ok(gasSetHold(g,'pressureV'),'P↕V allowed with P > 0'); const P0=g.P, W0=g.W, T0g=g.T;
    const s1=Object.assign({},ST,{heat:1});
    for(let f=0;f<48;f++) worldStep(w,s1,GAS.DT_FRAME);
    rel(g.P,P0,1e-5,'P↕V: the pressure stays at '+P0.toFixed(2)+' kPa while heated (the width to 5 decimals)');
    rel(g.W/W0,g.T/T0g,1e-5,'… and V/V₀ = T/T₀ (Charles): '+(g.W/W0).toFixed(5));
    for(let f=0;f<400&&g.hold==='pressureV';f++) worldStep(w,s1,GAS.DT_FRAME);
    eq(g.oops,'pressureLarge','heated past 15 nm: Oops, volume would be too large'); eq(g.hold,'nothing','and the hold drops to Nothing');
    const w2=setupConfig({view:'ideal'},null), g2=w2.g; gasSetHold(g2,'pressureV');
    for(let f=0;f<900&&g2.hold==='pressureV';f++) worldStep(w2,Object.assign({},ST,{heat:-1}),GAS.DT_FRAME);
    eq(g2.oops,'pressureSmall','cooled below 5 nm: Oops, volume would be too small'); }
  { /* hold P↕T: pump in more and the temperature falls with P fixed */
    const w=setupConfig({view:'ideal'},null), g=w.g; gasSetHold(g,'pressureT'); const P0=g.P, N0=gasCount(g), T0g=g.T;
    gasInject(g,0,100); worldStep(w,ST,GAS.DT_FRAME);
    rel(g.P,P0,1e-12,'P↕T: the pressure is held while 100 more are pumped in');
    rel(g.T,T0g*N0/gasCount(g),1e-12,'… and T falls as 1/N: '+g.T.toFixed(3)+' K'); }
  { /* hold T: remove particles and T is restored; the lid and the heater are locked */
    const w=setupConfig({view:'ideal'},null), g=w.g; ok(gasSetHold(g,'temperature'),'T allowed with a closed lid');
    gasInject(g,1,50); for(let f=0;f<24;f++) worldStep(w,ST,GAS.DT_FRAME);
    const T1=g.T; gasRemove(g,1,40); rel(gasTemp(g),T1,1e-12,'hold T: removing 40 light disks leaves T unchanged (every KE rescaled)');
    const e0=gasEnergy(g); worldStep(w,Object.assign({},ST,{heat:1}),GAS.DT_FRAME); rel(gasEnergy(g),e0,1e-12,'hold T: the heater does nothing');
    gasSetLid(g,2000); worldStep(w,ST,GAS.DT_FRAME); eq(g.oops,'temperatureOpen','the lid opened while holding T: Oops'); eq(g.hold,'nothing','… hold released');
    const w2=setupConfig({view:'ideal'},null); gasSetHold(w2.g,'temperature'); gasRemoveAll(w2.g); eq(w2.g.oops,'temperatureEmpty','T held, box emptied: Oops');
    const w3=setupConfig({view:'ideal'},null); gasSetHold(w3.g,'pressureT'); gasRemoveAll(w3.g); eq(w3.g.oops,'pressureEmpty','P held, box emptied: Oops');
    const w4=setupConfig({view:'ideal'},null); gasRemoveAll(w4.g); ok(!gasHoldAllowed(w4.g,'temperature')&&!gasHoldAllowed(w4.g,'pressureV'),'empty: T and P holds disabled');
    const w5=setupConfig({view:'ideal'},null); gasSetLid(w5.g,2000); ok(!gasHoldAllowed(w5.g,'temperature')&&gasHoldAllowed(w5.g,'volume'),'lid open: T disabled, V allowed'); }
  { /* hold V with heating: Gay-Lussac, P/T constant */
    const w=setupConfig({view:'ideal'},null), g=w.g; gasSetHold(g,'volume'); const r0=g.P/g.T;
    for(let f=0;f<24;f++) worldStep(w,Object.assign({},ST,{heat:1}),GAS.DT_FRAME);
    rel(g.P/g.T,r0,1e-12,'hold V: P/T is constant while heating'); ok(g.T>300,'and T rose'); }
  { /* the heater: exactly PhET's per-frame factor, as a rate */
    const g=gasMake({seed:6,collisions:false}); gasFill(g,0,50,300); const e0=gasEnergy(g); g.heat=1;
    runFrames(g,24); rel(gasEnergy(g)/e0,REF.heatKEPerPs,1e-12,'full heat for 1 ps: KE × (1 + 1/800)^48 = 1.0617968 (derive)');
    close(gasLedger(g).resid/gasEnergy(g),0,1e-13,'the heater’s energy is in the ledger');
    const g2=gasMake({seed:6,collisions:false}); gasFill(g2,0,50,300); g2.heat=1; let t=0; while(gasTemp(g2)<1000){ gasStep(g2,GAS.DT_FRAME); t+=GAS.DT_FRAME; }
    ok(Math.abs(t-REF.heatTime)<GAS.DT_FRAME+1e-9,'300 → 1000 K at full heat in '+t.toFixed(3)+' ps (derive '+REF.heatTime.toFixed(3)+')'); }
  { /* the lid: the gap, escaping particles, blowing off, returning */
    const g=gasMake({seed:7}); eq(gasOpening(g),0,'the lid starts closed'); gasSetLid(g,3000);
    close(gasOpenLeft(g),Math.round(-10000-75+3000),1e-12,'opening left edge = left − wall + lid width'); eq(gasOpenRight(),-2000,'opening right edge = −2000 pm');
    gasPush(g,0,-4000,8000,0,500); gasPush(g,0,-9000,8000,0,500); gasLedgerReset(g);
    gasPush(g,0,gasOpenLeft(g)+60,8000,0,500); gasLedgerReset(g);
    runFrames(g,48); eq(g.out[0]+g.out[1],1,'the disk under the gap escapes, the one under the lid bounces');
    eq(g.out[2],0,'a disk with its centre in the gap but its edge under the lid bounces (PhET: the whole disk must fit)');
    eq(gasCount(g),2,'… and N drops by one'); close(gasLedger(g).resid,0,1e-6,'the escape is in the energy ledger');
    gasSetLid(g,0); close(g.lid.width,gasMinLid(),1e-12,'the lid cannot be narrower than 1325 pm');
    const g2=gasMake({seed:8}); gasFill(g2,0,600,300); pressureOnAfterFill(g2); eq(g2.lid.on,true,'600 at 300 K: the lid holds ('+g2.P.toFixed(0)+' kPa)');
    gasSetTemp(g2,10000); gasRefresh(g2); ok(g2.P>GAS.P_MAX,'at 10,000 K the gauge passes 20,000 kPa ('+g2.P.toFixed(0)+')');
    eq(g2.lid.on,false,'past 20,000 kPa the lid blows off'); gasReturnLid(g2); eq(g2.lid.on,true,'and returns');
    const g3=gasMake({seed:8}); gasFill(g3,0,300,300); gasSetLid(g3,GAS.OPEN_L+GAS.WALL); ok(gasOpening(g3)>=GAS.LID_WIDE,'a wide-open lid ('+gasOpening(g3)+' pm)');
    g3.P=GAS.P_MAX+1; gasBlowLid(g3); eq(g3.lid.on,true,'is not blown off when the gap is ≥ 1500 pm (PhET)');
    const g4=gasMake({seed:8}); gasFill(g4,0,200,300); pressureOnAfterFill(g4); g4.heat=1;
    for(let f=0;f<400&&gasCount(g4);f++){ gasSetTemp(g4,Math.min(2e5,gasTemp(g4)*1.5)); gasStep(g4,GAS.DT_FRAME); }
    eq(g4.oops,'maxTemperature','at 10^5 K: Oops, maximum temperature'); eq(gasCount(g4),0,'every particle removed'); }
  { /* evaporative cooling: through the opening leave the fast ones.  The flux-
       weighted energy of a 2-D gas is (3/2)kT2 (a Gamma(3/2) law, variance
       (3/2)(kT2)^2), so the escapees carry 1.5 x the gas's mean energy, measured
       against the mean at the moment each frame's escapes happen */
    const g=gasMake({seed:17,virial:true}); gasFill(g,0,400,300); pressureOnAfterFill(g); gasSetLid(g,0); gasVirialReset(g);
    let S=0, C=0, f=0;
    while(C<120&&f<2400){ const n0=gasCount(g), eb=gasEnergy(g)/n0, e0=g.led.esc; gasStep(g,GAS.DT_FRAME); f++;
      const dn=n0-gasCount(g); if(dn>0){ S+=(g.led.esc-e0)/eb; C+=dn; } }
    /* the lid's widest gap (6.75 nm) is ~20 mean free paths, so this is not
       effusion (3/2, a hole small against the path) but a jet, which carries the
       stagnation enthalpy h0 = kT2 + P/n = 2 kT2 per particle; the escapees must
       land between the two limits (the exact 3/2 is pinned on the wall hits, S6) */
    const ratio=S/C, sd=Math.sqrt(1.5/C);
    ok(ratio>1.5-4*sd&&ratio<2+4*sd,'evaporative cooling: '+C+' escapees carried '+ratio.toFixed(3)+' × the mean energy, between effusion (3/2) and a jet’s enthalpy (2) ± '+(4*sd).toFixed(3));
    ok(Math.abs(ratio-1)>4*sd,'… not the mean itself (the lid is not a random sieve)');
    ok(gasTemp(g)<300,'so the gas left behind cools: '+gasTemp(g).toFixed(2)+' K');
    const Ve=gasVirial(g); ok(Math.abs(Ve.resid)/Ve.scale<1e-12,'the virial ledger closes with '+C+' escapes (each leaves with its r·p and its remaining 2KE)');
    close(gasLedger(g).resid/gasEnergy(g),0,1e-13,'and the energy ledger, escapes included'); }
  { /* the Ideal wall: resizing does no work; x scaled about the right wall */
    const w=setupConfig({view:'ideal'},null), g=w.g; const T1=g.T, x0=g.x[0];
    gasResize(g,7000,true); rel(gasTemp(g),T1,1e-15,'resizing the Ideal box does no work: T unchanged');
    let inside=true; for(let i=0;i<g.n;i++) if(g.x[i]-gasRad(g,i)<g.left-1e-9||g.x[i]+gasRad(g,i)>1e-9) inside=false; ok(inside,'every disk ends inside the new width');
    ok(Math.abs(g.x[0]-Math.max(x0*0.7,g.left+125))<1e-9,'redistribution scales x by 7/10 (PhET)');
    close(gasOpening(g),0,1e-9,'the closed lid follows the wall (still closed)'); }
  { /* the Explore wall: at most 800 m/s, in both directions */
    const w=setupConfig({view:'explore'},null), g=w.g; g.wantW=5000; const W0=g.W;
    worldStep(w,ST,GAS.DT_FRAME); close(W0-g.W,800*GAS.DT_FRAME,1e-9,'one frame moves the wall 800 m/s × 1/24 ps = 33.3 pm');
    close(g.u,800,1e-9,'the wall velocity is +800 (inward)'); ok(g.led.work>=0,'pushing in does non-negative work');
    for(let f=0;f<300;f++) worldStep(w,ST,GAS.DT_FRAME); eq(g.W,5000,'and stops at the requested width'); eq(g.u,0,'at rest');
    ok(g.T>w.T0*1.3,'squeezed 10 → 5 nm the gas has warmed ('+g.T.toFixed(1)+' K)'); }
  { /* the Energy sampler: PhET's 1-ps averages */
    const g=gasMake({seed:10}); gasFill(g,0,200,300); gasFill(g,1,100,300); gasSamplerOn(g);
    runFrames(g,23); eq(g.sampler.published,0,'nothing published before 1 ps');
    runFrames(g,1); eq(g.sampler.published,1,'published after 24 frames = 1 ps');
    const s0=g.sampler.out.s0.reduce((a,b)=>a+b,0), e0=g.sampler.out.e0.reduce((a,b)=>a+b,0);
    ok(s0<=200+1e-9&&s0>190,'the heavy speed bins hold ≤ 200 per frame (the tail past 3230 m/s drops out): '+s0.toFixed(2));
    ok(e0<=200+1e-9&&e0>185,'the heavy KE bins likewise: '+e0.toFixed(2));
    const c=gasBinCounts(g,0,GAS.SBIN,GAS.NBIN,false); eq(c.reduce((a,b)=>a+b,0)<=200,true,'instantaneous counts ≤ N');
    const gb=gasMake({seed:1}); gasPush(gb,0,-5000,4000,169.9999,0); gasPush(gb,0,-3000,4000,170,0); gasPush(gb,0,-1000,4000,0,3229.9);
    const cb=gasBinCounts(gb,0,GAS.SBIN,GAS.NBIN,false); ok(cb[0]===1&&cb[1]===1&&cb[18]===1,'binning is floor(v/170): 169.9999 → 0, 170 → 1, 3229.9 → 18');
    rel(g.sampler.mean[0],gasMeanSpeedOf(g,0),0.2,'the published mean speed is the 1-ps average of the instantaneous one'); }
  { /* diffusion: confinement by the divider, the flow counts, the COM, mass and temperature */
    const w=setupConfig({view:'diffusion'},null), g=w.g;
    eq(gasCount(g,0)+'/'+gasCount(g,1),'100/100','the diffusion defaults: 100 + 100');
    for(let f=0;f<120;f++) worldStep(w,ST,GAS.DT_FRAME);
    let conf=true; for(let i=0;i<g.n;i++){ const r=gasRad(g,i); if(g.sp[i]===0&&g.x[i]+r>g.dividerX-50+1e-6) conf=false; if(g.sp[i]===1&&g.x[i]-r<g.dividerX+50-1e-6) conf=false; }
    ok(conf,'divided: each species stays on its side of the 100-pm divider');
    ok(gasCOM(g,0)<-3000&&gasCOM(g,1)>3000,'the centres of mass sit in their halves');
    const sd=gasSideData(g); eq(sd[0].n0+'/'+sd[0].n1+'/'+sd[1].n0+'/'+sd[1].n1,'100/0/0/100','the Data panel counts');
    gasSetDivided(g,false); const s2=Object.assign({},ST,{divided:false}); for(let f=0;f<600;f++) worldStep(w,s2,GAS.DT_FRAME);
    ok(g.flow.rateL[1]>0&&g.flow.rateR[0]>0,'without the divider both species cross the middle ('+g.flow.rateR[0].toFixed(2)+', '+g.flow.rateL[1].toFixed(2)+' /ps)');
    ok(g.flow.dts.length===GAS.FLOW_WINDOW,'the flow is a running average of 300 frames');
    gasDiffMassTemp(g,1,8,450); let one=true; for(let i=0;i<g.n;i++) if(g.sp[i]===1&&Math.abs(gasSpeed(g,i)-Math.sqrt(3*GAS.K*450/8))>1e-9) one=false;
    ok(one,'a new mass or temperature sets every particle of the species to sqrt(3kT/m) (PhET)');
    gasDiffRestart(g,50,300,70,300); eq(gasCount(g,0)+'/'+gasCount(g,1)+'/'+g.divided,'50/70/true','the divider back: PhET restarts both sides');
    gasDiffCount(g,0,20,300); eq(gasCount(g,0),20,'the count slider removes'); gasDiffCount(g,0,60,300); eq(gasCount(g,0),60,'and adds, in the species’ own half');
    rel(REF.graham,Math.sqrt(28/4),1e-15,'Graham’s ratio √7 (derive)');
    rel(REF.vxplus_heavy,Math.sqrt(gasKT2(300)/(2*PI*28)),1e-14,'<v_x+> = sqrt(kT2/2πm) = 145.85 m/s (derive)'); }
  { const c=makeShot(800,500), b=box(60,60,300,160);
    plotSeries(c,800,500,b,'degenerate','degenerate',[0,1,2],[{ys:[1,1+2.2e-16,1],col:COL.pos}],{refs:[{y:1}]});
    ok(true,'a series flat to the last bit draws (the ticksFor spin is guarded)');
    const r=niceRange(1,1+2.2e-16); ok(r[1]-r[0]>0.09,'niceRange widens a span below rounding to ±5 %');
    const r2=niceRange(2,3); ok(r2[0]===2&&r2[1]===3,'and leaves an honest range alone'); }
  { /* the exact laws used by the views */
    for(let b=0;b<GAS.NBIN;b++){
      const lo=b*GAS.SBIN, hi=lo+GAS.SBIN;
      rel(mbSpeedCdf(hi,28,gasKT2(300))-mbSpeedCdf(lo,28,gasKT2(300)),REF.sbins_heavy[b]||1e-300,1e-10,'heavy speed bin '+b+' probability (derive)');
      rel(mbEnergyCdf((b+1)*GAS.EBIN,gasKT2(300))-mbEnergyCdf(b*GAS.EBIN,gasKT2(300)),REF.ebins[b],1e-10,'KE bin '+b+' probability (derive)');
    }
    rel(1-mbSpeedCdf(19*GAS.SBIN,4,gasKT2(300)),REF.sTail_light,1e-9,'light speeds past the last bin: 0.38 % (derive)');
    close(mcEnergyCdf(0.5,1,2),0.5,1e-15,'N = 2: a uniform split'); close(mcEnergyCdf(0.3,1,60),1-Math.pow(0.7,59),1e-15,'finite-N energy law 1 − (1 − x)^(N−1)');
    rel(hdB2(250),REF.B2heavy,1e-15,'B2 = π σ²/2 (derive)'); rel(HD_B3_RATIO,REF.B3overB2sq,1e-15,'B3/B2² = 4/3 − √3/π (derive, quadrature)');
    rel(hdContact(9750,8500,250),REF.Mbox,1e-14,'the contact measure of the 10 nm box (derive, quadrature)');
    rel(hdZ1(90,250,9750,8500),REF.Z1_90,1e-13,'first-order Z − 1 for 90 heavy (derive)');
    rel(mbSpeedPdf(365.58172820861824,28,gasKT2(300)),28*365.58172820861824/gasKT2(300)*Math.exp(-0.5),1e-14,'the speed pdf at its mode');
    close(mbEnergyPdf(0,gasKT2(300))*gasKT2(300),1,1e-15,'the energy pdf starts at 1/kT2'); }

  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section F');
  TIMES.F=Date.now();
  /* ---------- G. the views' models and readouts ---------- */
  { const w=setupConfig({view:'ideal'},null); const M=buildModel();
    ok(readoutHTML(M).indexOf('11.7 atm')>=0||readoutHTML(M).indexOf('11.6 atm')>=0||readoutHTML(M).indexOf('11.8 atm')>=0,'the gas-law readout prints the gauge near 11.7 atm');
    ok(readoutHTML(M).indexOf('P, V and T all free')>=0,'nothing held: the readout says so');
    gasSetHold(worldOf('ideal').g,'volume'); const M2=buildModel(), pt=worldOf('ideal').g.P/worldOf('ideal').g.T;
    ok(readoutHTML(M2).indexOf(sigf(pt,5)+' kPa/K')>=0,'hold V: the readout prints P/T = '+sigf(pt,5)+' kPa/K off the model');
    worldOf('ideal').g.hold='nothing';
    ST.unitP='kPa'; ok(readoutHTML(buildModel()).indexOf('1183 kPa')>=0,'in kPa: 1183 kPa (P = NkT/V, noise-free row)');
    ST.unitT='C'; ok(readoutHTML(buildModel()).indexOf('26.85 °C')>=0,'in °C: 26.85 °C'); }
  { /* a paused edit moves the state the lone trace marker describes: it re-seeds,
       so the marker never contradicts the readout beside it */
    const w=setupConfig({view:'ideal'},null); const g=w.g, P0=g.gaugeP;
    gasResize(g,GAS.WMIN,true); gasRefresh(g);
    ok(g.gaugeP>1.8*P0,'half the width doubles the gauge ('+g.gaugeP.toFixed(0)+' vs '+P0.toFixed(0)+' kPa)');
    drawView(makeShot(1400,820),1400,820,buildModel());
    eq(w.trace.length,1,'the gas-law trace is still one point');
    close(w.trace[0][2],g.gaugeP,1e-12,'… re-seeded to the state after the paused resize'); }
  { setupConfig({view:'energy'},null); const M=buildModel(); ok(M.mean[0]!==null&&Math.abs(M.mean[0]-REF.vMean_heavy)<40,'the energy view’s heavy mean speed is near MB’s 458 m/s ('+M.mean[0].toFixed(1)+')'); }
  { /* the pressure view, collisions off: the walls feel (3/2)·(Σmvx²/E)·W/(W−2r) of
       the gauge, exactly as t grows (the x share is fixed by the draw; its spread over
       draws is 1/√(N+1) = 0.156 for 40 disks, Dirichlet × uniform angles) */
    const w=setupConfig({view:'pressure',pN:40,pColl:false},null); for(let f=0;f<4800;f++) worldStep(w,ST,GAS.DT_FRAME);
    const P=pressureModel(w), pred=1.5*P.xshare*GAS.WDEF/(GAS.WDEF-250);
    ok(Math.abs(P.Zpair-1)<1e-15,'collisions off: Z from the collisions is exactly 1');
    let bnd=0; for(let i=0;i<w.g.n;i++) bnd+=2*28*Math.abs(w.g.vx[i])/P.t; bnd/=w.g.H*w.g.D/GAS.P_SCALE*P.Pgauge;
    ok(Math.abs(P.ratio-pred)<=bnd,'the walls feel (3/2)(Σmvx²/E)(W/(W−2r)) = '+pred.toFixed(4)+' × the gauge (measured '+P.ratio.toFixed(4)+', one-bounce bound '+bnd.toFixed(4)+')');
    ok(Math.abs(P.xshare-1)<4/Math.sqrt(41),'this draw’s x share '+P.xshare.toFixed(3)+' is within 4 sd of isotropy'); }
  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section G');
  TIMES.G=Date.now();
  /* ---------- H. every configuration: the readout, then the layout at four sizes ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,fn] of CONFIGS){
    setupConfig(over,fn); const M0=buildModel();
    const txt=readoutHTML(M0)+eqbarHTML(M0)+tagHTML(M0);
    ok(!/NaN|undefined|Infinity/.test(txt),nm+': readout, eqbar and tag clean');
    if(BOXVIEWS[ST.view]) ok(txt.indexOf(' K')>=0||txt.indexOf('°C')>=0,nm+': the readout shows a temperature');
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
       corner and the capture cannot see it: no canvas text may reach it */
    const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
    ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
  } }
  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section H');
  TIMES.H=Date.now();
  /* the statistical section runs last: it is the slow one (12 s of the 17) */
  /* ---------- E. the statistical laws, tolerances from the exact ensemble ---------- */
  const Qof=g=>{ const N=gasCount(g), E=gasEnergy(g); let s=0; for(let i=0;i<g.n;i++){ const x=gasKE(g,i)/E; s+=x*x; } return N*s; };
  { /* S1: 60 heavy disks from ONE speed, 40 independent seeds, 6 ps each */
    let qs=0, vs=0; const all=[];
    for(let s=0;s<40;s++){
      const g=gasMake({width:3000,height:3000,wRange:[3000,3000],noLid:true,seed:1000+s});
      gasFill(g,0,60,300,true); if(s===0){ ok(Math.abs(Qof(g)-1)<1e-12,'the start is a spike: every disk at one speed (Q = 1)'); }
      runFrames(g,144);
      qs+=Qof(g); const E=gasEnergy(g); let v=0; for(let i=0;i<g.n;i++){ const x=gasKE(g,i)/E; v+=Math.sqrt(x); all.push(x); } vs+=v/g.n;
    }
    const Qb=qs/40, Vb=vs/40;
    ok(Math.abs(Qb-REF.EQ60)<4*REF.sdQbar,'S1: <E²>/<E>² → 2N/(N+1) = 1.9672: '+Qb.toFixed(4)+' within 4 sd = '+(4*REF.sdQbar).toFixed(4)+' (Dirichlet, derive)');
    ok(Math.abs(Vb-REF.EV60)<4*REF.sdVbar,'S1: mean √(E_i/E) → Γ(3/2)Γ(N)/Γ(N+1/2): '+Vb.toFixed(6)+' vs '+REF.EV60.toFixed(6)+' ± 4 sd (derive)');
    const edges=REF.chiEdges, K=edges.length+1, cnt=new Array(K).fill(0);
    for(const x of all){ let b=0; while(b<edges.length&&x>=edges[b]) b++; cnt[b]++; }
    const Ee=all.length/K; let X2=0; for(const c of cnt) X2+=(c-Ee)*(c-Ee)/Ee;
    ok(X2<REF.chi9999,'S1: chi-square against the exact Beta(1, N-1) law = '+X2.toFixed(2)+' < '+REF.chi9999.toFixed(2)+' (its 99.99% point over the exact ensemble, derive)');
    ok(Qb>1.5,'S1 guard: the spike has relaxed (Q from 1 to '+Qb.toFixed(3)+')'); }
  { /* S2: equipartition from a 6:1 energy split, 30 heavy + 30 light */
    let D=0, D0=0;
    for(let s=0;s<40;s++){
      const g=gasMake({width:3000,height:3000,wRange:[3000,3000],noLid:true,seed:2000+s});
      gasFill(g,0,30,600,true); gasFill(g,1,30,100,true);
      D0+=(gasEnergy(g,0)/30-gasEnergy(g,1)/30)/(gasEnergy(g)/60);
      runFrames(g,144);
      D+=(gasEnergy(g,0)/30-gasEnergy(g,1)/30)/(gasEnergy(g)/60);
    }
    close(D0/40,10/7,1e-12,'S2 starts at (600 - 100)/350 = 1.4286');
    ok(Math.abs(D/40)<4*REF.sdD60/Math.sqrt(40),'S2: heavy and light share the energy alike: D = '+(D/40).toFixed(4)+' within 4 sd = '+(4*REF.sdD60/Math.sqrt(40)).toFixed(4)+' (Beta(N/2, N/2), derive)'); }
  { /* S6: the compressibility of hard disks resolves B3 */
    const g=gasMake({width:GAS.WDEF,seed:31,virial:true,noLid:true});
    gasFill(g,0,90,300); runFrames(g,240);
    gasVirialReset(g); gasImpulseReset(g); const p0=g.stats.pairHits;
    runFrames(g,9600);
    const E=gasEnergy(g), T=400, z=g.vir.pair/T/(2*E), K=g.stats.pairHits-p0;
    const sd=z*Math.sqrt((4/Math.PI)/K);
    const extra=Math.abs(REF.Z2_90-REF.Z1_90)*(0.15+2*250*(10000-250+8750-250)/(Math.PI*(10000-250)*(8750-250)));
    ok(Math.abs(z-REF.Z2_90)<4*sd+extra,'S6: Z - 1 = '+z.toFixed(5)+' against B₂+B₃ theory '+REF.Z2_90.toFixed(5)+' (4 sd + the next term = '+(4*sd+extra).toFixed(5)+', derive)');
    ok(Math.abs(z-REF.Z1_90)>2*sd,'S6: and B₂ alone ('+REF.Z1_90.toFixed(5)+') is excluded at > 2 sd');
    const V=gasVirial(g); ok(Math.abs(V.resid)/V.scale<1e-12,'S6: the virial ledger closes over 400 ps ('+(Math.abs(V.resid)/V.scale).toExponential(2)+')');
    rel(g.vir.kin,2*E*T,1e-12,'the kinetic virial is exactly 2E·t in a closed box');
    /* effusion without draining: every wall hit is flux-weighted, so the energy a
       hit arrives with averages (3/2)kT2 = 1.5 E/N (Gamma(3/2), variance 1.5 (E/N)^2;
       hits by one disk between collisions repeat its energy, so the independent
       count is taken as the 2K collision renewals, not the hits) */
    const hitsAll=g.imp.hitsL+g.imp.hitsR+g.imp.hitsB+g.imp.hitsT, eff=(g.imp.E/hitsAll)/(E/90), sdE=Math.sqrt(1.5/(2*K));
    ok(Math.abs(eff-1.5)<4*sdE,'effusion: '+hitsAll+' wall hits arrive with '+eff.toFixed(4)+' × the mean energy (2-D: 3/2 ± '+(4*sdE).toFixed(4)+')');
    eq(g.stats.eventCap,0,'S6: no event-cap overflow'); }
  { /* S4: collisions off, every bounce is periodic, so the momentum each wall
       receives is a closed form: disk i hits the right wall whenever its
       unfolded coordinate s = (x0 - xlo) + vx t passes L + 2kL (L = W - 2r) */
    const g=gasMake({width:GAS.WDEF,seed:44,virial:true,noLid:true,collisions:false});
    gasFill(g,0,40,300); gasImpulseReset(g);
    const r=125, xlo=-GAS.WDEF+r, L=GAS.WDEF-2*r, T=200;
    const hits=(s0,s1,c)=>{ const lo=Math.min(s0,s1), hi=Math.max(s0,s1); return Math.floor((hi-c)/(2*L))-Math.floor((lo-c)/(2*L)); };
    let JR=0, JL=0, want=0, bound=0;
    for(let i=0;i<g.n;i++){ const s0=g.x[i]-xlo, s1=s0+g.vx[i]*T, J=2*28*Math.abs(g.vx[i]);
      JR+=J*hits(s0,s1,L); JL+=J*hits(s0,s1,0); want+=28*g.vx[i]*g.vx[i]/L; bound+=J/T; }
    runFrames(g,4800);
    rel(g.imp.R,JR,1e-12,'S4: collisions off, the right wall received exactly Σ 2m|vx| × (its closed-form hit count)');
    rel(g.imp.L,JL,1e-12,'S4: the left wall likewise');
    const F=gasWallForce(g);
    ok(Math.abs(F.R-want)<=bound,'S4: so the force → Σ m vx²/(W−2r) = '+want.toFixed(1)+' as t grows (got '+F.R.toFixed(1)+' at 200 ps, one-bounce bound '+bound.toFixed(1)+')'); }
  { /* S7: the adiabat.  Slowly (20 m/s, Mach 0.04) 100 heavy disks squeezed
       10 -> 7 nm land on the HARD-DISK adiabat (derive: 1.0691), not on the
       point law T w = const (1.0111); at PhET's 800 m/s (Mach 1.55) the
       wall drives a shock and the gas ends far above both.  The tolerance is
       4 x the spread over seeds 21-23 at 10 and 20 m/s (0.0060, measured with
       this engine: 1.0740 1.0694 1.0650 / 1.0705 1.0800 1.0657). */
    rel(hdAdiabatRatio([100,0],[125,87.5],10000,7000,GAS.H,256),REF.adHD,1e-9,'the hard-disk adiabat integral, Simpson against scipy quad (derive)');
    rel(Math.log(hdAdiabatRatio([0,0],[0,0],10000,7000,GAS.H,256)),Math.log(10/7),1e-11,'for points it is T·w = const (Simpson, 256 intervals: error bound 1.3e-12)');
    rel(gasSound(gasKT2(300),28),REF.cSound_heavy,1e-15,'the heavy gas’s sound speed √(2kT₂/m) = 517 m/s (derive)');
    const squeeze=(u,seed)=>{ const g=gasMake({seed,doesWork:true,wallSpeed:u,noLid:true}); gasFill(g,0,100,300);
      const T0=gasTemp(g); g.wantW=7000; let f=0; while(g.W!==7000&&f<20000){ gasStep(g,GAS.DT_FRAME); f++; }
      for(let k=0;k<48;k++) gasStep(g,GAS.DT_FRAME); return gasTemp(g)*g.W/(T0*GAS.WDEF); };
    const slow=squeeze(20,22);
    ok(Math.abs(slow-REF.adHDtw)<4*0.006,'S7: a slow push (20 m/s) ends on the hard-disk adiabat: T·w/T₀w₀ = '+slow.toFixed(4)+' vs '+REF.adHDtw.toFixed(4)+' (derive)');
    ok(Math.abs(slow-REF.adPointsTw)>4*0.006,'S7: and not on the point law ('+REF.adPointsTw.toFixed(4)+')');
    const fast=squeeze(800,22);
    ok(fast>2*REF.adHDtw,'S7: at 800 m/s (Mach 1.55) the shock leaves it far above: '+fast.toFixed(3)); }

  TIMES.E=Date.now();
  console.log('section times, s: '+['A','D','F','G','H','E'].map((k,i,a)=>k+' '+((TIMES[k]-(i?TIMES[a[i-1]]:T0))/1000).toFixed(1)).join(', '));

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
