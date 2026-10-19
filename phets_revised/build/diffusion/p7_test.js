
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are     *
 *  lines of build/diffusion/refvals.txt, the printed output of         *
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
function runW(w,frames,dt){ for(let f=0;f<frames;f++) worldStep(w,ST,dt||GAS.DT_FRAME); }
/* the configurations the layout sweep and the capture share */
const CONFIGS=[
  ['box divided',{view:'box'},null],
  ['box mixing',{view:'box'},w=>{ removeDivider(w,ST); runW(w,240); }],
  ['box empty',{view:'box',d1n:0,d2n:0},w=>{ resetWorld(); }],
  ['box identical',{view:'box',preset:'same',d1m:28,d1r:125,d2m:28,d2r:125},w=>{ resetWorld(); removeDivider(worldOf(),ST); runW(worldOf(),240); }],
  ['box big and small',{view:'box',preset:'size',d1r:250,d2r:50},w=>{ resetWorld(); removeDivider(worldOf(),ST); runW(worldOf(),120); }],
  ['box lifting',{view:'box'},w=>{ w.divLift=0.6; }],
  ['mixing divided',{view:'mixing'},null],
  ['mixing early',{view:'mixing'},w=>{ removeDivider(w,ST); runW(w,120); }],
  ['mixing late',{view:'mixing'},w=>{ removeDivider(w,ST); runW(w,1200); }],
  ['mixing no collisions',{view:'mixing'},w=>{ w.g.collisions=false; removeDivider(w,ST); runW(w,960); }],
  ['flow divided',{view:'flow'},null],
  ['flow running',{view:'flow'},w=>{ removeDivider(w,ST); runW(w,360); }],
  ['flow heavy only',{view:'flow',d2n:0},w=>{ resetWorld(); removeDivider(worldOf(),ST); runW(worldOf(),360); }],
  ['speeds fresh',{view:'speeds'},null],
  ['speeds relaxed',{view:'speeds'},w=>{ removeDivider(w,ST); runW(w,720); }],
  ['speeds hot and cold',{view:'speeds',preset:'hot',d1T:500,d2T:100,d2m:28,d2r:125},w=>{ resetWorld(); removeDivider(worldOf(),ST); runW(worldOf(),720); }],
  ['speeds one species',{view:'speeds',d2n:0},w=>{ resetWorld(); runW(worldOf(),240); }],
  ['box slow',{view:'box',slow:true,unitT:'C'},w=>{ removeDivider(w,ST); runW(w,240,GAS.DT_SLOW); }]
];
function setupConfig(over,fn){
  Object.assign(ST,DEFAULTS,over); DRAG.what=null;
  resetAllWorlds();
  const w=worldOf();
  if(fn) fn(w);
  return worldOf();
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
  rel(GAS.P_SCALE,REF.pConv,1e-15,'PRESSURE_CONVERSION_SCALE (derive)');
  rel(GAS.ATM_PER_KPA,REF.atmPerKpaExact,3e-7,'ATM_PER_KPA is 1/101.325 to PhET’s 6 digits (derive)');
  eq(GAS.DIFF_W,16000,'the Diffusion container is 16 nm wide (widthRange 16e3,16e3,16e3)');
  eq(GAS.H+'/'+GAS.D,'8750/4000','… 8.75 nm tall and 4 nm deep');
  rel(GAS.DIVIDER,REF.divider,1e-15,'the divider is 100 pm thick (derive)');
  eq(GAS.DIFF_NMAX+'/'+GAS.DIFF_DN,'200/10','number of particles: 0–200 in tens');
  eq(GAS.DIFF_M.join('-'),'4-32','mass 4–32 AMU');
  eq(GAS.DIFF_R.join('-')+'/'+GAS.DIFF_RSTEP,'50-250/5','radius 50–250 pm in fives');
  eq(GAS.DIFF_T.join('-')+'/'+GAS.DIFF_TSTEP,'50-500/50','initial temperature 50–500 K in fifties');
  eq(GAS.FLOW_WINDOW,300,'the flow rate is a 300-frame running average');
  rel(GAS.DT_FRAME,REF.dtFrame,1e-15,'one frame is 1/24 ps (derive)');
  rel(GAS.DT_SLOW,REF.dtSlow,1e-15,'PhET’s slow speed is 0.3 ps a second (derive)');
  rel(GAS.STEP,REF.stepPs,1e-15,'the step button is MODEL_TIME_STEP = 0.2 ps (derive)');
  { const w=setupConfig({view:'box'},null); const t0=w.g.t;
    worldStep(w,ST,GAS.STEP);
    close(w.g.t-t0,REF.stepPs,1e-12,'… and one press really advances the model by it'); }
  /* PhET's Diffusion screen has no gauge, so the pressure is inert here — but
     P = NkT/V is the shared engine's definition and this suite re-asserts the
     engine, so it is pinned rather than left to drift */
  rel(gasVolume(worldOf().g),REF.Vbox,1e-15,'V = 16 nm × 8.75 nm × 4 nm (derive)');
  rel(gasPressureOf(200,300,REF.Vbox),REF.pBox200,1e-14,'P = NkT/V for 200 disks at 300 K in it: 1479.1 kPa (derive)');
  rel(gasPressureOf(100,300,REF.Vbox),REF.pBox100,1e-14,'… and half that for 100 (derive)');
  eq(TABS.length,4,'four views'); eq(TABS.map(t=>t[0]).join(','),'box,mixing,flow,speeds','the view keys');
  eq(worldKey('mixing'),'box','all four views share one gas: PhET’s Diffusion is one screen');

  /* ---------- B. the engine invariants this sim relies on ---------- */
  { /* the contact quadratic, at and around its branches.  The overlap test is
       the one with no margin, and this sim leans on it hardest: PhET's
       placement drops particles without rejection, so overlapping pairs are
       normal here and MUST get no event (they pass through until they
       separate).  A test written with any slack lets a hair-overlapping pair
       collide instead. */
    close(pairTime(0,500,0,-100,250),2.5,1e-15,'head-on: (500−250)/100 = 2.5 exactly');
    eq(pairTime(0,300,0,10,250),Infinity,'separating: no event');
    eq(pairTime(0,300,10,0,250),Infinity,'b = 0 (sliding past): no event');
    eq(pairTime(1000,300,-10,0,250),Infinity,'a miss: the discriminant is negative');
    eq(pairTime(0,200,0,-10,250),Infinity,'overlapping and approaching: no event');
    eq(pairTime(0,249.999,0,-10,250),Infinity,'overlapping by a HAIR (c = −0.5 pm²): still no event');
    eq(pairTime(0,250.0001,0,-10,250)<1e-4,true,'… and a hair apart it collides almost at once'); }
  { const R=gasRng(777); let wp=0, we=0;
    for(let q=0;q<5000;q++){
      const mi=4+28*R.next(), mj=4+28*R.next(), ri=50+200*R.next(), rj=50+200*R.next();
      const g=gasMake({seed:1,species:[{m:mi,r:ri},{m:mj,r:rj}]});
      const th=TAU*R.next(), s=ri+rj;
      gasPush(g,0,-8000,4000,300*(R.next()-0.5),300*(R.next()-0.5));
      gasPush(g,1,-8000+s*Math.cos(th),4000+s*Math.sin(th),300*(R.next()-0.5),300*(R.next()-0.5));
      const px0=mi*g.vx[0]+mj*g.vx[1], py0=mi*g.vy[0]+mj*g.vy[1], e0=gasKE(g,0)+gasKE(g,1);
      pairResolve(g,0,1);
      const px1=mi*g.vx[0]+mj*g.vx[1], py1=mi*g.vy[0]+mj*g.vy[1], e1=gasKE(g,0)+gasKE(g,1);
      /* the scale is the momentum carried, not its (possibly cancelling) sum */
      const sc=mi*(Math.abs(g.vx[0])+Math.abs(g.vy[0]))+mj*(Math.abs(g.vx[1])+Math.abs(g.vy[1]));
      wp=Math.max(wp,(Math.abs(px1-px0)+Math.abs(py1-py0))/sc); we=Math.max(we,Math.abs(e1/e0-1));
    }
    ok(wp<1e-15,'5000 random pair collisions conserve momentum ('+wp.toExponential(1)+' of the momentum carried)');
    ok(we<1e-13,'… and energy ('+we.toExponential(1)+')'); }
  { /* No overlaps from the dynamics.  PhET's own placement DOES overlap (it
       scatters without rejection), and the engine's rule is that overlapping
       disks pass through each other until they separate — so this has to be
       started from a non-overlapping fill, or it would be testing the rule
       rather than the dynamics.  200 of each at 125 pm is an area fraction of
       0.14, denser than anything the sliders reach at those radii. */
    const g=gasMake({width:GAS.DIFF_W,wRange:[GAS.DIFF_W,GAS.DIFF_W],noLid:true,seed:41,
                     species:[{m:28,r:125},{m:4,r:125}]});
    gasFill(g,0,200,300); gasFill(g,1,200,300); gasLedgerReset(g);
    const eta=gasCount(g)*PI*125*125/(g.W*g.H);
    let worst=Infinity;
    for(let f=0;f<48;f++){ gasStep(g,GAS.DT_FRAME);
      for(let i=0;i<g.n;i++) for(let j=i+1;j<g.n;j++){
        const d=Math.hypot(g.x[i]-g.x[j],g.y[i]-g.y[j])-(gasRad(g,i)+gasRad(g,j));
        if(d<worst) worst=d; } }
    ok(worst>-1e-6,'400 disks (area fraction '+fmt(eta,3)+') never overlap over 2 ps (closest approach '+worst.toExponential(1)+' pm)');
    const led=gasLedger(g); ok(Math.abs(led.resid)<=1e-12*Math.abs(led.E),'… and the energy ledger closes to '+(led.resid/led.E).toExponential(1)+' of the energy');
    rel(gasTemp(g),(2/3)*gasEnergy(g)/gasCount(g)/GAS.K,1e-15,'T is exactly (2/3)⟨KE⟩/k'); }
  { /* … and the documented opposite: PhET's placement overlaps at the densest
       slider setting, and those disks pass through each other rather than
       exploding.  The energy must not move. */
    const w=setupConfig({view:'box',d1n:200,d1r:250,d2n:200,d2r:250},null);
    const g=w.g;
    let over=0;
    for(let i=0;i<g.n;i++) for(let j=i+1;j<g.n;j++)
      if(Math.hypot(g.x[i]-g.x[j],g.y[i]-g.y[j])<gasRad(g,i)+gasRad(g,j)) over++;
    ok(over>0,'PhET’s placement (no rejection) starts 200+200 disks of 250 pm with '+over+' overlapping pairs');
    const E0=gasEnergy(g); runW(w,48);
    rel(gasEnergy(g),E0,1e-12,'… and they pass through each other: the energy is untouched');
    ok(isFinite(gasTemp(g)),'… and the temperature stays finite'); }
  { /* the divider really confines: nothing crosses while it is in */
    const w=setupConfig({view:'box'},null), g=w.g, mid=g.dividerX;
    runW(w,480);
    let bad=0;
    for(let i=0;i<g.n;i++){ if(g.out[i]) continue;
      if(g.sp[i]===0&&g.x[i]>mid) bad++; if(g.sp[i]===1&&g.x[i]<mid) bad++; }
    eq(bad,0,'with the divider in, 20 ps leaves every particle on its own side');
    eq(g.flow.dts.length,0,'… and the flow counter does not run'); }

  /* ---------- C. the centre of mass, exactly ---------- */
  { const w=setupConfig({view:'box'},null), g=w.g;
    close(REF.com1,-(GAS.DIFF_W+GAS.DIVIDER)/4,1e-9,'derive: the start is −(W + d)/4 = −4025 pm');
    close(REF.com2,+(GAS.DIFF_W+GAS.DIVIDER)/4,1e-9,'… and +4025 for particle 2 (derive)');
    /* 24 independent draws, so the mean of the measurements is 24× tighter */
    let s0=0,s1=0; const K=24;
    for(let q=0;q<K;q++){
      const g2=gasMake({width:GAS.DIFF_W,wRange:[GAS.DIFF_W,GAS.DIFF_W],noLid:true,seed:100+q,
                        species:[{m:28,r:125},{m:4,r:90}]});
      gasSetDivided(g2,true); diffScatter(g2,ST);
      s0+=gasCOM(g2,0); s1+=gasCOM(g2,1);
    }
    const sd0=REF.comSd1/Math.sqrt(K), sd1=REF.comSd2/Math.sqrt(K);
    ok(Math.abs(s0/K-REF.com1)<4*sd0,'24 fresh boxes put particle 1’s COM at '+fmt(s0/K,1)+' pm, against −4025 (4 sd = '+fmt(4*sd0,1)+')');
    ok(Math.abs(s1/K-REF.com2)<4*sd1,'… and particle 2’s at '+fmt(s1/K,1)+' pm, against +4025 (4 sd = '+fmt(4*sd1,1)+')');
    /* the radius cancels: the same claim at both ends of PhET's range */
    for(const r of [50,250]){
      let s=0; const K2=24;
      for(let q=0;q<K2;q++){
        const g2=gasMake({width:GAS.DIFF_W,wRange:[GAS.DIFF_W,GAS.DIFF_W],noLid:true,seed:200+q,
                          species:[{m:28,r},{m:4,r:90}]});
        gasSetDivided(g2,true); gasScatter(g2,0,100,300,g2.left,g2.left+g2.W/2-g2.dividerHalf);
        s+=gasCOM(g2,0);
      }
      const L=(GAS.DIFF_W/2-GAS.DIVIDER/2)-2*r, sd=L/Math.sqrt(12*100)/Math.sqrt(K2);
      ok(Math.abs(s/K2-REF.com1)<4*sd,'at r = '+r+' pm the COM is still −4025 ('+fmt(s/K2,1)+', 4 sd = '+fmt(4*sd,1)+'): the radius cancels');
    } }

  /* ---------- D. the exact laws ---------- */
  rel(vxPlus(28,300),REF.vxPlus1,1e-14,'⟨v_x⁺⟩ = √(kT₂/2πm) = 145.846 m/s for 28 AMU (derive, scipy quad)');
  rel(vxPlus(4,300),REF.vxPlus2,1e-14,'… 385.872 m/s for 4 AMU (derive)');
  rel(mbMeanSpeed(28,gasKT2(300))/PI,REF.vxPlus1,1e-14,'… and it is exactly ⟨v⟩/π (derive)');
  rel(mbMeanSpeed(28,gasKT2(300)),REF.vbar1,1e-14,'⟨v⟩ = 458.189 m/s (derive)');
  rel(mbRmsSpeed(28,gasKT2(300)),REF.vDelta1,1e-14,'PhET starts every particle at √(3kT/m) = the rms speed (derive)');
  rel(mbModeSpeed(28,gasKT2(300)),REF.mode1,1e-14,'the most probable speed √(kT₂/m) = 365.58 m/s for 28 AMU (derive)');
  rel(mbModeSpeed(4,gasKT2(300)),REF.mode2,1e-14,'… 967.24 m/s for 4 AMU (derive)');
  ok(mbModeSpeed(28,gasKT2(300))<mbMeanSpeed(28,gasKT2(300))&&mbMeanSpeed(28,gasKT2(300))<mbRmsSpeed(28,gasKT2(300)),
     'mode < mean < rms, as Maxwell–Boltzmann demands (1 : √(π/2) : √2)');
  rel(mbMeanSpeed(28,gasKT2(300))/mbModeSpeed(28,gasKT2(300)),Math.sqrt(PI/2),1e-14,'… ⟨v⟩/v_mode = √(π/2) exactly');
  rel(mbMeanSpeed(28,gasKT2(300))/mbRmsSpeed(28,gasKT2(300)),REF.meanSpeedDrop,1e-14,'⟨v⟩/rms = √(π/4) = 0.886227 (derive)');
  rel(mbMeanSpeed(4,gasKT2(300))/mbRmsSpeed(4,gasKT2(300)),REF.meanSpeedDrop,1e-14,'… the same for any mass (derive)');
  rel(vxPlus(4,300)/vxPlus(28,300),REF.graham,1e-14,'Graham’s √(m₁/m₂) = 2.6458 IS the ratio of the one-sided fluxes (derive)');
  /* off the BUILT MODEL, not off a formula retyped in the test (Known-bad:
     a test that re-derives the thing it is testing tests nothing) */
  { const w=setupConfig({view:'flow'},null);
    rel(buildModel().graham,REF.graham,1e-14,'… and the readout’s Graham number is that (derive)');
    gasDiffMassTemp(w.g,1,7,300);
    rel(buildModel().graham,Math.sqrt(28/7),1e-14,'… it follows the mass sliders (28 over 7 gives 2)'); }
  { /* the common temperature two species must reach is the NUMBER-weighted
       mean, which only differs from the plain mean when the counts differ */
    const w=setupConfig({view:'speeds',d1n:100,d1T:500,d2n:50,d2m:28,d2r:125,d2T:100},null);
    const M=buildModel();
    close(M.Tmix,(100*500+50*100)/150,1e-9,'100 at 500 K with 50 at 100 K must end at 366.67 K, not 300');
    ok(Math.abs(M.Tmix-300)>60,'… so the plain mean would be wrong by '+fmt(M.Tmix-300,1)+' K here');
    rel(gasTemp(w.g),M.Tmix,1e-12,'… and the whole gas is already at it (energy is conserved)');
    removeDivider(w,ST); runW(w,2400);
    rel(gasTemp(w.g),M.Tmix,1e-9,'… and stays there');
    ok(Math.abs(gasTemp(w.g,0)-M.Tmix)<0.1*M.Tmix,'… with both species arriving at it ('+fmt(gasTemp(w.g,0),0)+' K)'); }
  { const w=setupConfig({view:'box'},null), g=w.g;
    rel(flowTheory(g,0,100),REF.flow1,1e-13,'100 heavy on the left cross at 1.852/ps (derive)');
    rel(flowTheory(g,1,100),REF.flow2,1e-13,'100 light cross at 4.878/ps (derive)');
    rel(flowTheory(g,0,100),100*vxPlus(28,300)/(g.W/2-125),1e-15,'the height cancels: rate = N⟨v_x⁺⟩/(W/2 − r)');
    rel(tauEffusion(g,0),REF.tauFree1,1e-13,'τ (effusion) = (W − 2r)/4⟨v_x⁺⟩ = 27.0 ps (derive)');
    rel(tauEffusion(g,1),REF.tauFree2,1e-13,'… 10.25 ps for the light gas (derive)');
    rel(vRel(g,0,0),Math.sqrt(2)*mbMeanSpeed(28,gasKT2(300)),1e-14,'like pairs: ⟨v_rel⟩ = √2 ⟨v⟩ (derive)');
    rel(vRel(g,0,1),Math.sqrt(PI*gasKT2(300)/(2*(28*4/32))),1e-14,'unlike pairs: √(πkT₂/2μ) with the reduced mass');
    rel(zRate(g,0),REF.z1,1e-12,'a heavy disk suffers '+fmt(REF.z1,4)+' collisions/ps (derive)');
    rel(zRate(g,1),REF.z2,1e-12,'a light one '+fmt(REF.z2,4)+' (derive)');
    rel(mfp(g,0),REF.mfp1,1e-12,'its mean free path is '+fmt(REF.mfp1,1)+' pm (derive)');
    rel(pairRateTheory(g),REF.pairRate,1e-12,'the box holds '+fmt(REF.pairRate,2)+' pair collisions/ps (derive)');
    rel(dEstimate(g,0),REF.Dest1,1e-12,'D ≈ ⟨v⟩λ/2 (derive)');
    rel(tauDiffusive(g,0),REF.tauD1,1e-12,'τ_D = W²/π²D = '+fmt(REF.tauD1,1)+' ps (derive)');
    rel(g.W/mfp(g,0),REF.boxInMfp1,1e-12,'the box is 11.0 mean free paths across (derive)');
    /* the exact ratio the two limits must have for point particles */
    rel(tauDiffusive(g,0)/((g.W)/(4*vxPlus(28,300))),8*g.W/(PI*PI*PI*mfp(g,0)),1e-12,'τ_D/τ = 8W/π³λ exactly (derive)'); }
  /* the tail bins are ~1e-14, so the tolerance carries an absolute floor: at
     that size the last digits are the two libraries' expm1, not the physics
     (derive.py writes the bins with the same two expm1 calls this does) */
  for(let b=0;b<REF.mbBins1.length;b++)
    close(mbBinCounts(1,28,300)[b],REF.mbBins1[b],Math.max(1e-12*Math.abs(REF.mbBins1[b]),1e-16),
          'the 2-D MB probability in bin '+b+' (derive)');
  { let s=0; for(const v of mbBinCounts(1,28,300)) s+=v;
    rel(s,REF.mbCover1,1e-12,'the 20 bins cover the whole distribution for 28 AMU (derive)'); }
  TIMES.D=Date.now();

  /* ---------- E. the measurements ---------- */
  { /* the collisionless imbalance is exact kinematics: the sim must reproduce
       derive.py's 4-million-trajectory curve to its Monte-Carlo error */
    const w=setupConfig({view:'mixing',d2n:0},null);
    w.g.collisions=false; removeDivider(w,ST);
    const want=REF.ballT.map(()=>0), got=[];
    let f=0;
    for(let q=0;q<REF.ballT.length;q++){
      const target=Math.round(REF.ballT[q]/GAS.DT_FRAME);
      while(f<target){ worldStep(w,ST,GAS.DT_FRAME); f++; }
      const side=gasSideData(w.g); got.push(imbalance(w.g,side,0));
    }
    /* 100 particles, so the sampling sd of ΔN/N is 1/√100 = 0.10 */
    let worst=0; for(let q=0;q<got.length;q++) worst=Math.max(worst,Math.abs(got[q]-REF.ballDN[q]));
    ok(worst<0.34,'collisions off: ΔN/N follows derive.py’s exact ballistic curve at 5, 10, 20, 40 and 80 ps (worst '+fmt(worst,3)+', 3.4 sd on 100 particles)');
    ok(got[1]<Math.exp(-REF.ballT[1]/REF.tauFree1)+0.20,'… and it leads the effusion model early on, as the exact curve does'); }
  { /* the measured crossing rate against n ⟨vx+⟩ (H − 2r) */
    const w=setupConfig({view:'flow'},null);
    removeDivider(w,ST);
    runW(w,720);                                   /* 30 ps */
    const g=w.g, M=buildModel();
    /* the 300-frame average is over the last 12.5 ps; compare with the theory
       built from the side counts averaged over the same stretch is overkill —
       the counts move slowly, so the instantaneous theory is within a few % */
    let chi=0, nTot=0;
    for(const k of [0,1]) for(const dir of [0,1]){
      const meas=dir?g.flow.rateR[k]:g.flow.rateL[k], th=M.flowTh[k][dir?0:1];
      const n=meas*(g.flow.dts.reduce((a,b)=>a+b,0));
      nTot+=n;
      if(th>0&&n>4) chi+=(meas-th)/(th/Math.sqrt(n));
    }
    ok(nTot>40,'30 ps of mixing counted '+fmt(nTot,0)+' crossings');
    ok(Math.abs(chi)<3*2,'the four measured crossing rates track n⟨v_x⁺⟩(H−2r) (Σ residual/σ = '+fmt(chi,2)+')');
    ok(g.flow.rateR[1]>g.flow.rateL[1]*0.2,'the light gas is crossing both ways by now'); }
  { /* Graham: the light gas leads out of the gate */
    const w=setupConfig({view:'flow'},null);
    removeDivider(w,ST); runW(w,48);              /* 2 ps: still one-way */
    const g=w.g, r1=g.flow.rateR[0], r2=g.flow.rateL[1];
    ok(r1>0&&r2>0,'both species have crossed within 2 ps');
    const want=REF.graham*(g.W/2-g.species[0].r)/(g.W/2-g.species[1].r);
    const n1=r1*2, n2=r2*2, sd=want*Math.sqrt(1/Math.max(1,n1)+1/Math.max(1,n2));
    ok(Math.abs(r2/r1-want)<4*sd,'the light gas crosses '+fmt(r2/r1,2)+'× as fast, against Graham’s '+fmt(want,2)+' (4 sd = '+fmt(4*sd,2)+')'); }
  { /* the pair-collision rate against the mixture's collision frequency */
    const w=setupConfig({view:'flow'},null);
    removeDivider(w,ST); runW(w,240); w.pairs=[]; w.lastPairs=w.g.stats.pairHits;
    runW(w,240);                                   /* a full 10-ps window */
    const P=pairRateMeasured(w), th=pairRateTheory(w.g);
    ok(P.n>400,'10 ps of the default box counts '+P.n+' pair collisions');
    ok(Math.abs(P.rate-th)<0.12*th,'the measured '+fmt(P.rate,1)+'/ps is within 12 % of Σⱼ nⱼ(rᵢ+rⱼ)⟨v_rel⟩ = '+fmt(th,1)+'/ps'); }
  { /* PhET's spike relaxes, and the mean speed falls by exactly √(π/4) */
    const w=setupConfig({view:'speeds'},null);
    const g=w.g;
    for(const k of [0,1]){
      const v0=gasMeanSpeedOf(g,k);
      rel(v0,mbRmsSpeed(g.species[k].m,gasKT2(300)),1e-12,'species '+(k+1)+' starts at one speed, √(3kT/m)');
    }
    const E0=gasEnergy(g);
    removeDivider(w,ST); runW(w,960);              /* 40 ps, tens of collisions each */
    rel(gasEnergy(g),E0,1e-12,'the energy never changed');
    for(const k of [0,1]){
      const v=gasMeanSpeedOf(g,k), want=mbMeanSpeed(g.species[k].m,gasKT2(gasTemp(g,k)));
      ok(Math.abs(v/want-1)<0.05,'species '+(k+1)+'’s mean speed relaxed to ⟨v⟩ = √(πkT₂/2m) ('+fmt(v,1)+' vs '+fmt(want,1)+')');
      ok(v<mbRmsSpeed(g.species[k].m,gasKT2(gasTemp(g,k)))*0.95,'… i.e. it FELL from the rms, as √(π/4) = 0.886 demands');
    } }
  { /* two species started at different temperatures reach the number-weighted mean */
    const w=setupConfig({view:'speeds',preset:'hot',d1T:500,d2T:100,d2m:28,d2r:125},null);
    const g=w.g;
    rel(gasTemp(g,0),500,1e-12,'particle 1 starts at 500 K'); rel(gasTemp(g,1),100,1e-12,'particle 2 at 100 K');
    const want=REF.tCommon500_100;
    removeDivider(w,ST); runW(w,2400);             /* 100 ps */
    ok(Math.abs(gasTemp(g,0)-want)<0.08*want,'after 100 ps particle 1 is at '+fmt(gasTemp(g,0),1)+' K, against the common '+fmt(want,0)+' K');
    ok(Math.abs(gasTemp(g,1)-want)<0.08*want,'… and particle 2 at '+fmt(gasTemp(g,1),1)+' K');
    rel(gasTemp(g),want,1e-9,'… while the whole gas was always at the number-weighted mean (energy is conserved)'); }
  { /* the profile's binning, in ABSOLUTE numbers: a test written in terms of
       NPROF moves with it and sees nothing */
    eq(NPROF,32,'the concentration profile has 32 bins');
    const g=gasMake({width:GAS.DIFF_W,wRange:[GAS.DIFF_W,GAS.DIFF_W],noLid:true,seed:71,
                     species:[{m:28,r:125},{m:4,r:90}]});
    close(g.W/32,500,1e-9,'… 500 pm each across the 16 nm box');
    gasPush(g,0,g.left+0.5*g.W+1,4000,10,10);      /* just right of the middle */
    gasPush(g,1,g.left+250,4000,10,10);            /* in the second bin */
    const pr=profile(g);
    eq(pr[0].length,32,'profile() returns 32 bins per species');
    eq(pr[0][16],1,'a particle a hair right of the middle lands in bin 16 of 32');
    eq(pr[1][0],1,'… and one 250 pm from the left wall in bin 0');
    let tot=0; for(const v of pr[0].concat(pr[1])) tot+=v;
    eq(tot,2,'… and nothing is counted twice or dropped'); }
  { /* the profile: two blocks become one flat line */
    const w=setupConfig({view:'mixing'},null);
    const p0=profile(w.g);
    let leftOnly=true; for(let q=NPROF/2;q<NPROF;q++) if(p0[0][q]>0) leftOnly=false;
    ok(leftOnly,'divided: particle 1 is entirely in the left half of the profile');
    removeDivider(w,ST); runW(w,2400);
    const p1=profile(w.g), mean=gasCount(w.g,0)/NPROF;
    let chi2=0; for(let q=0;q<NPROF;q++) chi2+=(p1[0][q]-mean)*(p1[0][q]-mean)/mean;
    ok(chi2<2*NPROF,'after 100 ps the profile is flat to a χ² of '+fmt(chi2,1)+' on '+(NPROF-1)+' degrees of freedom'); }
  TIMES.E=Date.now();

  /* ---------- F. the controls behave as PhET's do ---------- */
  { const w=setupConfig({view:'box'},null), g=w.g;
    gasDiffMassTemp(g,0,16,300);
    eq(g.species[0].m,16,'a new mass takes effect at once');
    let one=true; for(let i=0;i<g.n;i++) if(g.sp[i]===0&&Math.abs(gasSpeed(g,i)-Math.sqrt(3*GAS.K*300/16))>1e-9) one=false;
    ok(one,'… and re-speeds every particle of that species to √(3kT/m), as PhET does');
    gasDiffCount(g,1,50,300); eq(gasCount(g,1),50,'the count slider removes down to 50');
    gasDiffCount(g,1,120,300); eq(gasCount(g,1),120,'… and adds back to 120');
    let inHalf=true; for(let i=0;i<g.n;i++) if(g.sp[i]===1&&!g.out[i]&&g.x[i]<g.dividerX) inHalf=false;
    ok(inHalf,'… adding puts them in the species’ own half');
    gasDiffRadius(g,1,250,false); eq(g.species[1].r,250,'the radius slider');
    let inside=true; for(let i=0;i<g.n;i++) if(g.sp[i]===1&&!g.out[i]&&(g.x[i]+250>0||g.y[i]-250<0)) inside=false;
    ok(inside,'… and while paused every particle is put back inside the walls');
    resetDivider(w,ST);
    eq(g.divided,true,'reset divider puts it back');
    eq(gasCount(g,0)+'/'+gasCount(g,1),ST.d1n+'/'+ST.d2n,'… and regenerates both species at their slider counts (PhET restarts)');
    eq(g.t,0,'… from t = 0'); }
  { const w=setupConfig({view:'box'},null);
    removeDivider(w,ST);
    eq(w.g.divided,false,'remove divider takes it out'); eq(ST.divided,false,'… and the panel follows');
    eq(w.g.flow.dts.length,0,'… restarting the flow counter');
    runW(w,10); ok(w.g.flow.dts.length===10,'… which then runs a sample a frame'); }

  /* ---------- G. every configuration: the readout, then the layout ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,fn] of CONFIGS){
    setupConfig(over,fn); const M0=buildModel();
    const txt=readoutHTML(M0)+eqbarHTML(M0)+tagHTML(M0)+(INFO[ST.view]||'')+(DERIV[ST.view]||'');
    ok(!/NaN|undefined|Infinity/.test(txt),nm+': readout, eqbar, tag and prose clean');
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
         corner and the canvas capture cannot see it */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
    }
  }
  if(fail>0) throw new Error(fail+' self-test failure(s), stopped after section G');
  TIMES.G=Date.now();

  /* ---------- H. no slider combination gives a non-finite value ---------- */
  { let bad=null, err=null;
    try{
      for(const n of [0,10,200]) for(const m of [4,32]) for(const r of [50,250]) for(const T of [50,500]){
        const w=setupConfig({view:'flow',d1n:n,d1m:m,d1r:r,d1T:T,d2n:n,d2m:36-m,d2r:300-r,d2T:550-T},null);
        removeDivider(w,ST); runW(w,6);
        const M=buildModel();
        const vals=[M.tauEff[0],M.tauEff[1],M.tauDif[0],M.tauDif[1],M.mfp[0],M.mfp[1],M.pairTh,
                    M.flowTh[0][0],M.flowTh[0][1],M.flowTh[1][0],M.flowTh[1][1],M.Tmix,M.graham];
        for(const v of vals) if(v!==null&&!isFinite(v)) bad='n='+n+' m='+m+' r='+r+' T='+T+' → '+v;
        const c=makeShot(1400,820); drawView(c,1400,820,M);
      }
    }catch(e){ err=e; }
    ok(!err,'every count × mass × radius × temperature corner runs and draws'+(err?': '+(err.stack||err):''));
    ok(!bad,'… with no non-finite value ('+(bad||'ok')+')'); }
  TIMES.H=Date.now();

  console.log('section times, s: '+['D','E','G','H'].map((k,i,a)=>k+' '+((TIMES[k]-(i?TIMES[a[i-1]]:T0))/1000).toFixed(1)).join(', '));
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
