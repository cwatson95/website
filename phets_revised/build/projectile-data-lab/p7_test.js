
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/projectile-data-lab/refvals.txt, the printed output *
 *  of derive.py, read in full; REF (p7a_refs.js) is the same numbers, *
 *  written by derive.py so that none is retyped.                      *
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
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
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
/* Simpson on a function, for the density integrals */
/* the 0th, 1st and 2nd moments of f from ONE sampling of it */
function simp3(f,a,b,n){
  const h=(b-a)/n, out=[0,0,0];
  for(let i=0;i<=n;i++){
    const x=a+i*h, c=(i===0||i===n)?1:(i%2?4:2), y=f(x)*c;
    out[0]+=y; out[1]+=y*x; out[2]+=y*x*x;
  }
  return out.map(s=>s*h/3);
}
function simp(f,a,b,n){
  const N=2*Math.max(1,Math.round(n/2)), dx=(b-a)/N;
  let s=f(a)+f(b);
  for(let i=1;i<N;i++) s+=(i%2?4:2)*f(a+i*dx);
  return s*dx/3;
}
/* a deterministic stand-in for the random stream: gauss() walks a fixed list,
   so PhET's re-draw windows can be pinned at the exact values that decide
   them rather than waited for (a 10-sigma guard is otherwise untestable) */
function stubRng(list){
  let i=0;
  return {next(){ return 0.5; }, gauss(){ return i<list.length?list[i++]:0; }};
}
/* the configurations the layout sweep and the capture share */
const CONFIGS=[
  ['field default',{view:'field'}],
  ['field launcher 6, bars',{view:'field',fld:3,lau:6,blocks:false,binW:2}],
  ['field empty',{view:'field',fld:5},w=>{ fieldClear(worldOf('field').fields[4]); }],
  ['field one shot',{view:'field',fld:6},w=>{ const F=worldOf('field').fields[5]; fieldClear(F); fieldBatch(F,1); }],
  ['field angle flags, 200 shots',{view:'field',fld:2,showAng:true,binStrat:'totalBins',nBins:50},
    w=>{ const F=worldOf('field').fields[1]; fieldBatch(F,160); }],
  ['sources spring 45°',{view:'sources',orient:'angle45',mech:'spring',stab:0.2}],
  ['sources explosion raised',{view:'sources',orient:'angle0Raised',mech:'explosion',stab:0.9,ptype:'piano'}],
  ['sources pumpkin 60°',{view:'sources',orient:'angle60',ptype:'pumpkin',mech:'pressure'}],
  ['measures default',{view:'measures'}],
  ['measures values + wide interval',{view:'measures',showValues:true,e1:5,e2:95,mLau:6}],
  ['measures custom, empty',{view:'measures',mSrc:'custom'},w=>{ fieldClear(worldOf('measures').F); }],
  ['measures one shot',{view:'measures'},w=>{ const F=worldOf('measures').F; fieldClear(F); fieldBatch(F,1); }],
  ['sampling n = 2',{view:'sampling',pN:2,pLau:3}],
  ['sampling n = 40',{view:'sampling',pN:40,pLau:6}],
  ['sampling no standard error',{view:'sampling',pN:15,showSe:false}],
  ['exact launcher 2',{view:'exact',xLau:2}],
  ['exact raised, no delta',{view:'exact',xLau:5,xOrient:'angle0Raised',showDelta:false}],
  ['exact 50 launches',{view:'exact',xLau:3,xN:50}],
  ['exact no density',{view:'exact',xLau:6,showDensity:false}],
  ['clt default',{view:'clt'}],
  ['clt launcher 6, no normals',{view:'clt',cLau:6,cM:200,showNormal:false}],
];
function applyConfig(cfg){
  Object.assign(ST,DEFAULTS);
  Object.assign(ST,cfg[1]);
  resetAllWorlds();
  if(cfg[2]) cfg[2]();
}

function selfTest(){
  let pass=0, fail=0;
  const T0=Date.now(), TIMES={};
  const ok=(c,n)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+n); } };
  const close=(a,b,t,n)=>ok(Math.abs(a-b)<=t,n+'  ('+a+' vs '+b+', |d| '+Math.abs(a-b).toExponential(2)+' > '+t+')');
  const rel=(a,b,t,n)=>ok(Math.abs(a-b)<=t*Math.max(1e-300,Math.abs(b)),
    n+'  ('+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.max(1e-300,Math.abs(b))).toExponential(2)+' > '+t+')');
  const eq=(a,b,n)=>ok(a===b,n+'  ('+a+' vs '+b+')');
  const stSave=Object.assign({},ST);

  /* ============ A. PhET's own constants ============ */
  rel(PDL.G,REF.G,0,'g is PhET’s 9.81 (derive)');
  rel(PDL.FIELD,REF.FIELD,0,'the field is PhET’s 100 m (derive)');
  rel(PDL.RAISED_H,REF.RAISED_H,0,'the raised launcher is PhET’s 12 m (derive)');
  rel(ANG_C,REF.angSdCentre,0,'launcher 1’s angle sd is the range centre, 2.6° (derive)');
  rel(ANG_Q,REF.angSdQuarter,0,'launcher 4’s is min + length/4, 1.4° (derive)');
  eq(JSON.stringify(PDL.SIZES),JSON.stringify(REF.SAMPLE_SIZES),'the sample sizes are PhET’s 2, 5, 15, 40 (derive)');
  eq(JSON.stringify(PTYPES.map(t=>t.mult)),JSON.stringify(REF.TYPE_MULT),'the projectile multipliers are PhET’s 1, 1.1, 0.9 (derive)');
  for(const k in REF.MECH){
    rel(MECH[k].mean,REF.MECH[k][0],0,'mechanism '+k+': PhET’s mean speed (derive)');
    rel(MECH[k].sd,REF.MECH[k][1],0,'mechanism '+k+': PhET’s speed sd (derive)');
  }
  LAUNCHERS.forEach((l,i)=>{
    rel(l.sdAng,REF.LAUNCH_SD[i],0,'mystery launcher '+(i+1)+': PhET’s angle sd (derive)');
    eq(l.mech,REF.LAUNCH_MECH[i],'mystery launcher '+(i+1)+': PhET’s mechanism (derive)');
  });
  [0,0.25,0.5,0.75,1].forEach((s,i)=>rel(pdlSdOfStab(s),REF.sdStab[i],1e-15,'the stabiliser at '+s+' gives PhET’s angle sd (derive)'));
  for(const s of [0,0.13,0.5,0.87,1]) close(pdlStabOfSd(pdlSdOfStab(s)),s,1e-13,'the stabiliser inverts at '+s);
  ok(pdlSdOfStab(1)<pdlSdOfStab(0),'stability 1 is the TIGHTEST launcher, not the loosest (PhET’s map runs backwards)');
  rel(PDL.LAUNCH_GAP,REF.LAUNCH_GAP,0,'continuous fire waits PhET’s MINIMUM_TIME_BETWEEN_LAUNCHES (derive)');
  rel(PDL.MAX_PROJ,REF.MAX_PROJ,0,'a field holds PhET’s 500 projectiles (derive)');
  rel(PDL.MAX_SAMPLES,REF.MAX_SAMPLES,0,'and 200 samples (derive)');
  eq(JSON.stringify(PDL.NBINS),JSON.stringify(REF.NBINS),'the total-bins choices are PhET’s (derive)');
  { /* the gap is what the model does, not only what the constant says */
    Object.assign(ST,DEFAULTS); ST.view='field'; ST.mode='continuous'; resetAllWorlds();
    const F=curField(ST); fieldClear(F); fireField(ST);
    const NF=Math.round(3*PDL.LAUNCH_GAP*60);          /* 126 frames = 2.1 s */
    for(let k=0;k<NF;k++) worldStep(ST,1/60);
    eq(F.n,3,'continuous fire launches 3 projectiles in '+NF+' frames (one at once, then one every '+PDL.LAUNCH_GAP+' s)');
    worldStep(ST,1/60);
    eq(F.n,4,'and the fourth on the very next frame — which is what pins the gap at '+PDL.LAUNCH_GAP+' s');
    F.firing=false;
    /* and the field stops at PhET's ceiling */
    fieldClear(F); fieldBatch(F,PDL.MAX_PROJ+200);
    eq(F.landed.length,PDL.MAX_PROJ,'a field stops at PhET’s '+PDL.MAX_PROJ+' projectiles');
    eq(fieldLaunch(F),null,'and refuses one more');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  const SAMPVIEW='sampling', SAMPMODE='pMode';
  { /* PhET's SamplingField.totalSampleTime: a sample of n is spread evenly
       over it, and the launches overlap rather than queueing */
    for(const n of PDL.SIZES) rel(PDL.SAMPLE_TIME[n],REF.SAMPLE_TIME[''+n],0,
      'a sample of '+n+' takes PhET’s '+REF.SAMPLE_TIME[''+n]+' s (derive)');
    for(const n of PDL.SIZES) rel(sampleStep(n),PDL.SAMPLE_TIME[n]/n,0,
      'so its launches are '+fmt(PDL.SAMPLE_TIME[n]/n,4)+' s apart at n = '+n);
    ok(sampleStep(40)<sampleStep(2),'a bigger sample fires FASTER, not slower (9 s for 40, 0.75 for 2)');
    /* and the model really does that */
    Object.assign(ST,DEFAULTS); ST.view=SAMPVIEW; ST.running=true; resetAllWorlds();
    const F=curField(ST); fieldClear(F); fireField(ST);
    const step=sampleStep(F.size);
    let atHalf=0;
    for(let k=0;k<Math.round(F.size*step*60/2);k++) worldStep(ST,1/60);
    atHalf=F.n;
    ok(Math.abs(atHalf-F.size/2)<=1,'half way through a sample about half its '+F.size+' launches are away ('+atHalf+')');
    for(let k=0;k<4000&&F.samples.length===0;k++) worldStep(ST,1/60);
    eq(F.samples.length,1,'and the sample completes when the last of them lands');
    eq(F.samples[0].xs.length,F.size,'with exactly n landing distances in it');
    ok(F.t<PDL.SAMPLE_TIME[F.size]+6,'inside '+fmt(PDL.SAMPLE_TIME[F.size],2)+' s + one flight ('+fmt(F.t,2)+' s)');
    F.firing=false;
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the second sample of a continuous run is paced by sampleStart's clock
       rewind and by nothing else: every other route into a sample comes
       through fieldClear, which zeroes the same clock, so a test that starts
       from a cleared field cannot see it (Known-bad: two guards on one path
       make each other's mutant equivalent — this is the second pair in this
       file, one level out from the first). */
    Object.assign(ST,DEFAULTS); ST.view=SAMPVIEW; ST.running=true; ST[SAMPMODE]='continuous';
    resetAllWorlds();
    const F=curField(ST); fieldClear(F); fireField(ST);
    let guard=0;
    while(F.samples.length<1&&guard++<8000) worldStep(ST,1/60);
    eq(F.samples.length,1,'the first sample of a continuous run completes');
    ok(F.firing===true,'and the next one starts by itself');
    const n0=F.n, half=Math.round(PDL.SAMPLE_TIME[F.size]*60/2);
    for(let k=0;k<half;k++) worldStep(ST,1/60);
    const made=F.n-n0;
    ok(Math.abs(made-F.size/2)<=1,'the SECOND sample is paced too — '+made+' of its '+F.size
      +' away half way through its '+PDL.SAMPLE_TIME[F.size]+' s, not all of them at once');
    ok(F.samples.length===1,'… and it has not completed yet');
    F.firing=false;
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the total-bins strategy: the width is exactly 100/n, and the bins then
       tile the field with no remainder */
    for(const n of PDL.NBINS){
      const w=binWidthOf({binStrat:'totalBins',nBins:n,binW:1});
      rel(w,PDL.FIELD/n,0,'total bins = '+n+' gives a width of exactly 100/'+n);
      rel(PDL.FIELD/w,n,1e-12,'… and '+n+' of them tile the 100 m field exactly');
    }
    rel(binWidthOf({binStrat:'binWidth',nBins:10,binW:2.5}),2.5,0,'the bin-width strategy takes the width as given'); }

  /* ============ B. the random stream ============ */
  { const r=pdlRng(REF.sampleSeed);
    /* next() is integer arithmetic all the way, so it is bit-identical across
       the two languages and the tolerance is zero.  Everything downstream
       passes through log, cos and sqrt, where a libm may differ in the last
       bit between JavaScriptCore and CPython — those are pinned at 1e-15,
       which is four ulp, not at zero. */
    for(let i=0;i<6;i++) rel(r.next(),REF.rngStream[i],0,'mulberry32 draw '+i+' is bit-identical to Python (derive)');
    const r2=pdlRng(REF.sampleSeed);
    for(let i=0;i<6;i++) rel(r2.gauss(),REF.gaussStream[i],1e-15,'Box–Muller value '+i+' matches Python to 4 ulp (derive)');
    /* the same seed repeats; a different seed does not */
    const a=pdlRng(5), b=pdlRng(5), c=pdlRng(6);
    let same=true, diff=false;
    for(let i=0;i<20;i++){ const x=a.next(); if(x!==b.next()) same=false; if(x!==c.next()) diff=true; }
    ok(same,'the same seed gives the same stream');
    ok(diff,'a different seed gives a different one');
    /* the stream's own quality, with tolerances from the sampling variance */
    const N=200000, u=new Array(N); const r3=pdlRng(7);
    for(let i=0;i<N;i++) u[i]=r3.next();
    const mu=pdlMean(u), sd=pdlSd(u,1);
    close(mu,0.5,4/Math.sqrt(12*N),'200k uniforms average 0.5 within 4 se ('+fmt(mu,6)+')');
    close(sd*sd,1/12,4*(1/12)*Math.sqrt(2/N),'their variance is 1/12 within 4 se ('+fmt(sd*sd,6)+')');
    let lo=0, hi=0; for(const x of u){ if(x<0||x>=1) lo++; if(x<0.5) hi++; }
    eq(lo,0,'every draw is in [0, 1)');
    close(hi/N,0.5,4*0.5/Math.sqrt(N),'half of them are below 0.5');
    const g=new Array(N); const r4=pdlRng(7);
    for(let i=0;i<N;i++) g[i]=r4.gauss();
    const gm=pdlMean(g), gs=pdlSd(g,1);
    close(gm,0,4/Math.sqrt(N),'200k normals average 0 within 4 se ('+fmt(gm,5)+')');
    close(gs*gs,1,4*Math.sqrt(2/N),'their variance is 1 within 4 se ('+fmt(gs*gs,6)+')');
    let m3=0,m4=0; for(const x of g){ const d=x-gm; m3+=d*d*d; m4+=d*d*d*d; }
    close(m3/N/Math.pow(gs,3),0,4*Math.sqrt(6/N),'their skewness is 0 within 4 se');
    close(m4/N/Math.pow(gs,4)-3,0,4*Math.sqrt(24/N),'their excess kurtosis is 0 within 4 se');
  }
  TIMES.A=Date.now();

  /* ============ C. the trajectory ============ */
  REF.rangeCases.forEach(c=>{
    rel(pdlRange(c[0],c[1],c[2]),c[3],1e-15,'the range at v='+c[0]+', θ='+c[1]+'°, h='+c[2]+' m (derive)');
    rel(pdlFlight(c[0],c[1],c[2]),c[4],1e-15,'the flight time there (derive)');
  });
  for(const [v,th,h] of [[23,30,0],[24,45,0],[25,60,0],[23,0,12],[24,-7,12],[20,80,0],[18,12,12]]){
    const T=pdlFlight(v,th,h);
    rel(v*Math.cos(th*Math.PI/180)*T,pdlRange(v,th,h),1e-14,'x(T) = the range at v='+v+', θ='+th+', h='+h);
    close(pdlHeight(v,th,h,T),0,1e-11*Math.max(1,h),'the projectile is on the ground at T there');
    ok(pdlHeight(v,th,h,T*0.5)>0||th<0,'and above it half way there');
  }
  for(const th of [5,15,30,45,60,75,85]) rel(pdlRange(23,th,0),23*23*Math.sin(2*th*Math.PI/180)/PDL.G,1e-15,
    'h = 0: the range is v² sin2θ/g at θ = '+th+'°');
  /* the SHAPE of the formula, not only its value: a 0° launch from a height
     is v√(2h/g), and a 90° launch lands where it started */
  rel(pdlRange(20,0,12),20*Math.sqrt(2*12/PDL.G),1e-15,'a flat launch from 12 m carries v√(2h/g)');
  close(pdlRange(20,90,0),0,1e-13,'a vertical launch lands on the launcher');
  REF.maxAngle.forEach(c=>rel(pdlMaxAngle(c[0],c[1]),c[2],1e-14,'the maximum-range angle at v='+c[0]+', h='+c[1]+' (derive)'));
  rel(pdlMaxAngle(23,0),45,1e-13,'from the ground the best angle is 45°');
  ok(pdlMaxAngle(23,12)<45,'from a height it is BELOW 45° ('+fmt(pdlMaxAngle(23,12),3)+'°)');
  { const th=pdlMaxAngle(23,12), r0=pdlRange(23,th,12);
    ok(pdlRange(23,th-0.4,12)<r0&&pdlRange(23,th+0.4,12)<r0,'and the range really peaks there');
    /* the derivative, against a central difference */
    for(const [v,th2,h] of [[23,30,0],[25,12,12],[19,55,0]]){
      const e=1e-5, num=(pdlRange(v+e,th2,h)-pdlRange(v-e,th2,h))/(2*e);
      rel(pdlDRdv(v,th2,h),num,1e-8,'∂x/∂v against a central difference at v='+v+', θ='+th2+', h='+h);
    }
    /* PhET's two delta-method coefficients ARE the partials of its own range
       at h = 0, and the second of them vanishes at 45° — which is the whole
       reason its estimate is high there rather than low */
    for(const [v,th2] of [[23,30],[24,45],[25,60],[22,12]]){
      const e=1e-5, rad=Math.PI/180, x0=pdlRange(v,th2,0);
      /* a central difference of two numbers of size x0 has a roundoff floor of
         about eps·x0/(2h); at 45° the answer is exactly 0 and a RELATIVE
         tolerance there would be asserting the floor, not the derivative */
      const dth=(pdlRange(v,th2+e,0)-pdlRange(v,th2-e,0))/(2*e*rad);
      const wth=2*v*v/PDL.G*Math.cos(2*th2*rad);
      close(dth,wth,Math.max(1e-8*Math.abs(wth),4e-15*x0/(2*e*rad)),'∂x/∂θ is PhET’s 2v²cos2θ/g at θ = '+th2+'°');
      const dv=(pdlRange(v+e,th2,0)-pdlRange(v-e,th2,0))/(2*e);
      const wv=2*v/PDL.G*Math.sin(2*th2*rad);
      close(dv,wv,Math.max(1e-8*Math.abs(wv),4e-15*x0/(2*e)),'∂x/∂v is PhET’s 2v sin2θ/g at θ = '+th2+'°');
    }
    close(2*24*24/PDL.G*Math.cos(2*45*Math.PI/180),0,1e-14,'and at 45° the angle coefficient is exactly zero');
    ok(Math.abs((pdlRange(24,45+1e-4,0)-pdlRange(24,45-1e-4,0))/(2e-4*Math.PI/180))<1e-6,
       '… which the range itself confirms: 45° is its stationary point');
    /* ∂x/∂v > 0 everywhere, which is what makes v*(r, θ) unique */
    let mono=true;
    for(const h of [0,12]) for(let th2=h?-40:1;th2<89;th2+=3.7) for(let v=1;v<40;v+=1.3) if(!(pdlDRdv(v,th2,h)>0)) mono=false;
    ok(mono,'∂x/∂v is positive over the whole slider space, so the speed that reaches r is unique');
  }
  /* v* round-trips the range, on both the flat and the raised launcher */
  { let worst=0;
    for(const h of [0,12]) for(const th of (h?[-20,-6,0,7,25]:[3,12,30,45,60,80])) for(const r of [4,18,37,63,96]){
      const v=pdlVStar(r,th,h);
      if(v===null) continue;
      worst=Math.max(worst,Math.abs(pdlRange(v,th,h)/r-1));
    }
    ok(worst<1e-12,'v*(r, θ) round-trips the range everywhere it exists (worst '+worst.toExponential(2)+')');
    /* downward from a height the range saturates at h/tan|θ| — v* must refuse
       past it rather than iterate into a vanishing derivative */
    const lim=12/Math.tan(20*Math.PI/180);
    ok(pdlVStar(lim*0.98,-20,12)!==null,'v* exists just below the h/tan|θ| ceiling ('+fmt(lim,3)+' m)');
    ok(pdlVStar(lim*1.02,-20,12)===null,'and refuses just above it');
    ok(pdlRange(2000,-20,12)<lim&&pdlRange(2000,-20,12)>0.99*lim,
       'because a 20° downward launch approaches it from below as v grows (2000 m/s gives '+fmt(pdlRange(2000,-20,12),3)+' m)');
    /* the two algebraic forms of the range: equal everywhere the sliders
       reach, and only the stable one survives the cancellation past them */
    { let worst=0;
      for(const h of [0,12]) for(let th=h?-50:1;th<89;th+=2.3) for(let v=5;v<40;v+=1.1)
        worst=Math.max(worst,Math.abs(pdlRangeStable(v,th,h)-pdlRange(v,th,h))/Math.max(1e-9,pdlRange(v,th,h)));
      ok(worst<1e-13,'the conjugate form of the range agrees with PhET’s over the whole slider space (worst '+worst.toExponential(2)+')');
      rel(pdlRangeStable(1e9,-20,12),lim,1e-14,'and at 10⁹ m/s it still gives h/tan|θ| to 1e-14');
      ok(Math.abs(pdlRange(1e9,-20,12)/lim-1)>1e-3,'where PhET’s form is 3.9 % out, the cancellation having eaten it ('+fmt(pdlRange(1e9,-20,12),4)+' m)');
      /* and the error grows as v², which is what identifies it as cancellation
         rather than a wrong formula */
      const e7=Math.abs(pdlRange(1e7,-20,12)/lim-1), e8=Math.abs(pdlRange(1e8,-20,12)/lim-1);
      ok(e8/e7>8&&e8/e7<40,'the error grows about 100-fold per decade of v, as a lost-digits error must ('+fmt(e8/e7,1)+'×)');
    }
    ok(pdlVStar(30,-20,0)===null,'and on flat ground a downward launch reaches nothing at all');
  }
  { /* PhET's two re-draw windows, pinned at the values that DECIDE them.
       Both sit six standard deviations out or more at every launcher the sim
       offers, so waiting for a draw to reach one is not a test; a stub stream
       puts the draw exactly there. */
    const cfg=pdlConfig('pressure',5,'angle30','cannonball');
    rel(pdlDraw(stubRng([11,0,0]),cfg).ang,85,1e-12,'an 85° draw is ACCEPTED: PhET’s angle window closes at 90, not lower');
    rel(pdlDraw(stubRng([12.1,0,0]),cfg).ang,30,1e-12,'a 90.5° draw is re-drawn');
    rel(pdlDraw(stubRng([-6.1,0,0]),cfg).ang,30,1e-12,'and a −0.5° draw is re-drawn');
    rel(pdlDraw(stubRng([-6,0,0]),cfg).ang,30,1e-12,'0° itself is re-drawn: PhET’s test is a <= 0, not a < 0');
    rel(pdlDraw(stubRng([12,0,0]),cfg).ang,30,1e-12,'and 90° itself is re-drawn: the test is a >= 90');
    /* the RAISED launcher is exempt — PhET skips the re-draw there entirely */
    const raised=pdlConfig('spring',ANG_C,'angle0Raised','cannonball');
    rel(pdlDraw(stubRng([-8,0]),raised).ang,-8*ANG_C,1e-12,
      'the raised launcher keeps a '+fmt(-8*ANG_C,1)+'° draw: PhET exempts it from the window');
    ok(pdlRange(23,-8*ANG_C,PDL.RAISED_H)>0,'… and such a shot still lands down the field');
    /* the speed's own window */
    rel(pdlDraw(stubRng([0,-120,0.5]),cfg).v,cfg.meanSpeed+0.5*cfg.sdSpeed,1e-12,
      'a speed of 0 is re-drawn (PhET’s test is v <= 0)');
    rel(pdlDraw(stubRng([0,2]),cfg).v,cfg.meanSpeed+2*cfg.sdSpeed,1e-12,'and an ordinary speed is taken as drawn');
    /* the order of the draws: the angle first, then the speed */
    const g=pdlDraw(stubRng([1,2]),cfg);
    rel(g.ang,cfg.meanAng+1*cfg.sdAng,1e-12,'the angle is drawn FIRST from the stream');
    rel(g.v,cfg.meanSpeed+2*cfg.sdSpeed,1e-12,'and the speed second');
    /* the projectile's speed multiplier reaches the SAMPLER, not only the
       quadrature — the one thing that ties PhET's mechanism to the law */
    for(const t of PTYPES){
      const c2=pdlConfig('spring',ANG_C,'angle30',t.id);
      rel(pdlDraw(stubRng([0,0]),c2).v,MECH.spring.mean*t.mult,1e-12,
        'a '+t.name+' is launched at ×'+t.mult+' the mechanism’s mean speed');
    }
    const NB=20000;
    for(const t of ['cannonball','pumpkin','piano']){
      const c2=pdlConfig('spring',ANG_C,'angle30',t), E2=pdlExact(c2);
      const rng=pdlRng(4242), xs=new Array(NB);
      for(let k=0;k<NB;k++){ const d=pdlDraw(rng,c2); xs[k]=pdlRange(d.v,d.ang,c2.h); }
      ok(Math.abs(pdlMean(xs)-E2.mean)<4*E2.sd/Math.sqrt(NB),
        'and '+NB+' sampled '+t+'s average the exact law’s '+fmt(E2.mean,3)+' m ('+fmt(pdlMean(xs),3)+')');
    } }
  TIMES.B=Date.now();

  /* ============ D. the quadrature and the exact law ============ */
  { let wx=0, ww=0;
    for(let i=0;i<PDL.NGL;i++){ wx=Math.max(wx,Math.abs(GL.x[i]-REF.glX[i])); ww=Math.max(ww,Math.abs(GL.w[i]-REF.glW[i])); }
    ok(wx<1e-14,'the 96 Gauss–Legendre nodes match numpy’s leggauss to '+wx.toExponential(2)+' (derive)');
    ok(ww<1e-13,'and the weights to '+ww.toExponential(2)+' (derive)');
    let s0=0,s2=0,s10=0;
    for(let i=0;i<PDL.NGL;i++){ s0+=GL.w[i]; s2+=GL.w[i]*GL.x[i]*GL.x[i]; s10+=GL.w[i]*Math.pow(GL.x[i],10); }
    rel(s0,2,1e-14,'Σw = 2 exactly');
    rel(s2,2/3,1e-13,'Σw x² = 2/3');
    rel(s10,2/11,1e-12,'Σw x¹⁰ = 2/11 (the rule is exact to degree 191)');
    /* Newton's starting guess: 0.75 and 0.5 land on the SAME roots (the
       mutation sweep reports that mutant as a survivor, and it is right —
       this is the measurement that says so), while 0.25 does not, so the
       seed is not free either */
    const g75=pdlGauleg(PDL.NGL), g50=pdlGauleg(PDL.NGL,0.5), g25=pdlGauleg(PDL.NGL,0.25);
    let d50=0, d25=0;
    for(let i=0;i<PDL.NGL;i++){ d50=Math.max(d50,Math.abs(g75.x[i]-g50.x[i]));
      d25=Math.max(d25,Math.abs(g75.x[i]-g25.x[i])); }
    ok(d50===0,'the 0.75 and 0.50 Newton seeds converge to bit-identical nodes');
    ok(d25>1,'while 0.25 converges somewhere else entirely ('+d25.toExponential(2)+') — the seed is not free');
    let d0=0; for(let i=0;i<PDL.NGL;i++) d0=Math.max(d0,Math.abs(GL.x[i]-g75.x[i]));
    ok(d0===0,'and the table the sim uses is the 0.75 one');
    /* the normal weights: over ±12 sd they must sum to one */
    const R1=pdlZRule(-PDL.ZCAP,PDL.ZCAP);
    let tw=0, tz=0, tz2=0;
    for(let i=0;i<PDL.NGL;i++){ tw+=R1.w[i]; tz+=R1.w[i]*R1.z[i]; tz2+=R1.w[i]*R1.z[i]*R1.z[i]; }
    rel(tw,1,1e-13,'the ±12 sd normal rule integrates the density to 1');
    close(tz,0,1e-13,'its first moment is 0');
    rel(tz2,1,1e-12,'and its second is 1');
    /* a half-line: the two halves must add back up */
    const A=pdlZRule(-PDL.ZCAP,0), B=pdlZRule(0,PDL.ZCAP);
    let wa=0, wb=0; for(let i=0;i<PDL.NGL;i++){ wa+=A.w[i]; wb+=B.w[i]; }
    rel(wa+wb,1,1e-13,'the two half-line rules add to 1');
    rel(wa,0.5,1e-13,'each holds half the density');
  }
  REF.exactCases.forEach((c,i)=>{
    const cfg={meanSpeed:c[0],sdSpeed:c[1],meanAng:c[2],sdAng:c[3],h:c[4],raised:!!c[5],mult:1};
    const E=pdlExact(cfg);
    rel(E.mean,c[6],1e-14,'case '+i+': the exact mean landing distance (derive)');
    rel(E.sd,c[7],1e-13,'case '+i+': the exact standard deviation (derive)');
    /* μ₃ is a sum of terms of order σ³ that cancels to as little as σ³/40,
       so its natural tolerance is absolute in σ³, not relative in μ₃ */
    close(E.mu3,c[8],1e-12*Math.pow(c[7],3),'case '+i+': the exact third central moment (derive)');
    close(E.mu4,c[9],1e-12*Math.pow(c[7],4),'case '+i+': the exact fourth central moment (derive)');
    ok(E.varr>0&&isFinite(E.skew)&&isFinite(E.kurt),'case '+i+': variance positive, skew and kurtosis finite');
  });
  /* the closed form of the UNtruncated model, and what the truncation costs */
  { let ci=0, worst=0, anyReal=false;
    REF.exactCases.forEach(c=>{
      if(c[5]) return;
      const cf=pdlClosed(c[0],c[1],c[2],c[3]);
      for(let k=0;k<4;k++) rel(cf[k],REF.closedCases[ci][k],1e-14,'closed form '+ci+', moment '+(k+1)+' (derive)');
      const d=Math.abs(cf[0]-c[6]);
      worst=Math.max(worst,d);
      if(c[3]>=5&&d>1e-9) anyReal=true;
      ci++;
    });
    rel(worst,REF.truncGap,1e-6,'the worst truncation shift of the mean is derive.py’s '+REF.truncGap.toExponential(2)+' m');
    ok(anyReal,'the 5° launchers really are truncated (the shift is not identically zero, so this measures something)');
    ok(worst<1e-6,'and it is below a micrometre, which is what "negligible" means here');
  }
  /* the two-pass central moments: the raw-moment form loses digits, and this
     pins the choice rather than leaving it to taste */
  { const cfg=cfgMystery(5), E=pdlExact(cfg), Rw=pdlMomentsRaw(cfg);
    ok(Math.abs(Rw.mu3/E.mu3-1)>1e-9,'assembling μ₃ from the raw moments loses '+
       (Math.abs(Rw.mu3/E.mu3-1)).toExponential(1)+' of it (m₃ ≈ 2e5 against μ₃ ≈ 0.02)');
    rel(Rw.varr,E.varr,1e-9,'the variance survives the same cancellation (it only loses three digits)');
  }
  /* 30° and 60° are the SAME distribution of distance: sin2θ is symmetric
     about 45° and so is the 0–90° truncation */
  { const a=pdlExact(cfgMystery(1,'angle30')), b=pdlExact(cfgMystery(1,'angle60'));
    rel(a.mean,b.mean,1e-14,'a launcher at 30° and at 60° have the same mean distance');
    rel(a.sd,b.sd,1e-12,'… and the same standard deviation');
    ok(Math.abs(pdlFlight(23,30,0)/pdlFlight(23,60,0)-1)>0.4,'… while their flight times differ by 73 %');
  }
  REF.orientStats.forEach((o,i)=>{
    const E=pdlExact(cfgMystery(1,ORIENTS[i].id));
    rel(E.mean,o[0],1e-14,'launcher 1 at '+ORIENTS[i].name+': the exact mean (derive)');
    rel(E.sd,o[1],1e-12,'launcher 1 at '+ORIENTS[i].name+': the exact sd (derive)');
  });
  REF.typeStats.forEach((o,i)=>{
    const E=pdlExact(pdlConfig('spring',ANG_C,'angle30',PTYPES[i].id));
    rel(E.mean,o[0],1e-14,'launcher 1 with a '+PTYPES[i].name+': the exact mean (derive)');
    rel(E.sd,o[1],1e-12,'… and its sd (derive)');
  });
  { /* the projectile scales the speed, so the mean distance scales as the
       square of the multiplier and the sd scales with it */
    const a=pdlExact(pdlConfig('spring',ANG_C,'angle30','cannonball'));
    const b=pdlExact(pdlConfig('spring',ANG_C,'angle30','pumpkin'));
    rel(b.mean/a.mean,1.1*1.1,2e-3,'a pumpkin flies 1.1² further (the speed sd does not scale, so it is not exact)');
    ok(b.sd>a.sd,'and lands with a wider spread');
  }
  REF.launcherStats30.forEach((o,i)=>{
    const E=pdlExact(cfgMystery(i+1));
    rel(E.mean,o[0],1e-14,'mystery launcher '+(i+1)+' at 30°: the exact mean (derive)');
    rel(E.sd,o[1],1e-12,'mystery launcher '+(i+1)+' at 30°: the exact sd (derive)');
  });
  /* PhET's own delta method: pinned, and one-sided against the exact sd */
  { let di=0, low=0;
    REF.exactCases.forEach(c=>{
      if(c[5]) return;
      const d=pdlDeltaSd(c[0],c[1],c[2],c[3]);
      rel(d,REF.deltaSd[di],1e-14,'PhET’s delta-method sd, case '+di+' (derive)');
      rel(REF.naiveMean[di],c[0]*c[0]*Math.sin(2*c[2]*Math.PI/180)/PDL.G,1e-14,'the no-jitter mean, case '+di+' (derive)');
      if(d<c[7]) low++;
      di++;
    });
    /* four of the five are low; the 45° one is high by 5e-6, because cos2θ = 0
       there kills the angle term and only the speed term survives.  The
       measured statement, not the tidy one. */
    eq(low,di-1,'PhET’s delta method is BELOW the exact sd in four of the five flat cases');
    { const c45=REF.exactCases.filter(c=>!c[5])[3];
      ok(pdlDeltaSd(c45[0],c45[1],c45[2],c45[3])>c45[7],'and ABOVE it at 45°, where cos2θ = 0 leaves only the speed term');
      ok(pdlDeltaSd(c45[0],c45[1],c45[2],c45[3])/c45[7]-1<1e-4,'… by 5e-6, which is why the sign is worth stating rather than the size'); }
    let wors=0;
    REF.exactCases.filter(c=>!c[5]).forEach((c,k)=>{ wors=Math.max(wors,Math.abs(REF.deltaSd[k]/c[7]-1)); });
    ok(wors<0.01&&wors>0.005,'the delta method is never more than 1 % out, and is 0.68 % out at its worst');
    /* the exact mean divided by the no-jitter one factorises: the SPEED
       spread lengthens it (E[v²] = μ² + σ²) and the ANGLE spread shortens it
       (E[sin2θ] = sin2μ·e^{−2σ²}).  Neither wins everywhere, and asserting
       "jitter shortens the range" would have been false for two launchers. */
    let shorter=0, longer=0, worstFac=0;
    for(let n=1;n<=6;n++) for(const o of ['angle30','angle45','angle60']){
      const cfg=cfgMystery(n,o), mu=cfg.meanSpeed, w=cfg.sdAng*Math.PI/180;
      const naive=mu*mu*Math.sin(2*cfg.meanAng*Math.PI/180)/PDL.G;
      const fac=(1+Math.pow(cfg.sdSpeed/mu,2))*Math.exp(-2*w*w);
      worstFac=Math.max(worstFac,Math.abs(pdlExact(cfg).mean/naive/fac-1));
      if(pdlExact(cfg).mean<naive) shorter++; else longer++;
    }
    ok(worstFac<1e-8,'the exact mean is exactly (1 + σ_v²/μ_v²)·e^{−2σ_θ²} × the no-jitter one, at all 18 settings (worst '+worstFac.toExponential(2)+')');
    eq(shorter,12,'twelve of the eighteen are SHORTER than the no-jitter value');
    eq(longer,6,'and six are LONGER — launchers 3 and 5, whose speed spread beats their angle spread');
    for(const n of [3,5]){ const cfg=cfgMystery(n), mu=cfg.meanSpeed, w=cfg.sdAng*Math.PI/180;
      ok(Math.pow(cfg.sdSpeed/mu,2)>2*w*w,'launcher '+n+': σ_v²/μ² beats 2σ_θ², which is why it lands long'); }
  }
  TIMES.C=Date.now();

  /* ============ E. the density ============ */
  REF.exactCases.forEach((c,i)=>{
    const cfg={meanSpeed:c[0],sdSpeed:c[1],meanAng:c[2],sdAng:c[3],h:c[4],raised:!!c[5],mult:1};
    rel(pdlPdf(c[6],cfg),REF.pdfAtMean[i],1e-12,'the density at the mean, case '+i+' (derive)');
    const lo=Math.max(1e-9,c[6]-9*c[7]), hi=c[6]+9*c[7];
    /* ONE pass for all three moments: the density costs 8x96 evaluations a
       point now, and calling it three times over the same abscissae was three
       times the work for nothing */
    const [I0,I1,I2]=simp3(x=>pdlPdf(x,cfg),lo,hi,200);
    rel(I0,1,2e-6,'case '+i+': the density integrates to 1');
    rel(I1,c[6],2e-6,'case '+i+': and to the exact mean');
    rel(I2,c[7]*c[7]+c[6]*c[6],2e-6,'case '+i+': and to the exact second moment');
    ok(pdlPdf(c[6],cfg)>0&&pdlPdf(c[6]+14*c[7],cfg)<pdlPdf(c[6],cfg)*1e-6,'case '+i+': it is positive at the mean and dead 14 sd out');
  });
  { /* a legend ROW for a curve that is switched off is the caption fault in
       legend form: draw it both ways and read the canvas back */
    const drawn=(st)=>{ Object.assign(ST,DEFAULTS,st); resetAllWorlds();
      const c=makeShot(1200,760); drawView(c,1200,760,buildModel());
      return c.ops.filter(o=>o.op==='text').map(o=>plain(o.t)); };
    const withD=drawn({view:'exact'}), noD=drawn({view:'exact',showDensity:false});
    ok(withD.indexOf('the exact density')>=0,'the exact view legends its density when it draws it');
    ok(noD.indexOf('the exact density')<0,'and drops the row when the checkbox is off');
    ok(noD.indexOf('300 launches')>=0,'while the launches row stays');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* and the same for the exact view's own density checkbox */
    Object.assign(ST,DEFAULTS); ST.view='exact'; resetAllWorlds();
    const on=exactCaption(buildModel()).full;
    ok(/orange curve is not a fit/.test(on),'with the density on, the exact view names the curve');
    ST.showDensity=false;
    const off=exactCaption(buildModel()).full;
    ok(/switched off/.test(off)&&!/orange curve is not a fit/.test(off),
      'with it off it says the bars stand on their own');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* a caption that describes curves the checkbox has switched off is the
       raised-panel fault again, in the view that teaches the theorem */
    Object.assign(ST,DEFAULTS); ST.view='clt'; resetAllWorlds();
    const on=cltCaption(buildModel()).full;
    ok(/orange curves are normals/.test(on),'with the normals on, the caption names them');
    ST.showNormal=false;
    const off=cltCaption(buildModel()).full;
    ok(/switched off/.test(off)&&!/orange curves are normals/.test(off),
      'with them off it says so instead of describing curves that are not there');
    ok(/7\.684|[0-9]\.[0-9]{3} m from the exact law/.test(off),'and still names σ, which the panels below measure against');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the panel count is a measurement, not a taste.  The density at a FIXED
       r integrates a SPIKE in theta — only the angles whose v*(r,theta) lands
       within a few sd of the mean speed contribute — so one 96-node rule rings
       around it wherever a small speed spread meets a large angle spread. The
       shipped rule must be converged AND one panel must not be, or the constant
       is free and a mutant on it is equivalent. */
    const PCASES=[['mystery 2',cfgMystery(2),31],['mystery 1',cfgMystery(1),9],
      ['mystery 6',cfgMystery(6),9],['pressure 5° raised',pdlConfig('pressure',5,'angle0Raised','cannonball'),31],
      ['pressure 5° at 60°',pdlConfig('pressure',5,'angle60','cannonball'),9]];
    let wK=0,w1=0,w4=0,whereK='',where1='';
    for(const [nm,cfg,np] of PCASES){
      const M=pdlExact(cfg), lo=Math.max(0,M.mean-4*M.sd), hi=M.mean+4*M.sd;
      for(let i=0;i<=np;i++){
        const r=lo+(hi-lo)*i/np, ref=pdlPdf(r,cfg,64);
        if(!(ref>0.02/M.sd)) continue;
        const dK=Math.abs(pdlPdf(r,cfg)-ref)/ref;
        const d1=Math.abs(pdlPdf(r,cfg,1)-ref)/ref;
        const d4=Math.abs(pdlPdf(r,cfg,4)-ref)/ref;
        if(dK>wK){ wK=dK; whereK=nm+' at r = '+fmt(r,1)+' m'; }
        if(d1>w1){ w1=d1; where1=nm+' at r = '+fmt(r,1)+' m'; }
        if(d4>w4) w4=d4;
      }
    }
    ok(wK<1e-6,'the density is converged in the panel count: worst '+wK.toExponential(1)
      +' against 64 panels ('+whereK+'), against 4.3e-3 for the single rule');
    ok(w1>0.25,'and ONE panel is out by '+fmt(100*w1,0)+' % at '+where1
      +' — the ringing the panels exist to kill');
    ok(w4>0.05,'four panels are still '+fmt(100*w4,1)+' % out, so eight is not a round number');
    /* the drawn curve comes from a cache: it must be the same numbers */
    const cq=cfgMystery(4), Mq=pdlExact(cq), lq=Mq.mean-3*Mq.sd, hq=Mq.mean+3*Mq.sd;
    const C1=pdlPdfCurve(cq,lq,hq,20), C2=pdlPdfCurve(cq,lq,hq,20);
    ok(C1===C2,'the drawn density curve is cached, not recomputed every frame');
    let cw=0;
    for(let i=0;i<=20;i++) cw=Math.max(cw,Math.abs(C1.ys[i]-pdlPdf(lq+(hq-lq)*i/20,cq)));
    rel(cw,0,1e-18,'and the cached curve IS the density (worst '+cw.toExponential(1)+')');
    const C3=pdlPdfCurve(cfgMystery(6),lq,hq,20);
    ok(Math.abs(C3.ys[10]-C1.ys[10])>1e-4,'a different launcher gets a different curve out of it'); }
  { /* the density divides by BOTH acceptance probabilities.  At every launcher
       PhET ships, mu_v/sigma_v is 20 or more, so the speed one is 1 to machine
       precision and a mutant that drops it is equivalent — which is the sweep
       saying the code carries meaning the tests do not.  Pin the contract
       where it bites instead: a configuration the ENGINE supports in which one
       launch in 44 would be drawn at a negative speed. */
    const wsum=r=>{ let s2=0; for(let i=0;i<PDL.NGL;i++) s2+=r.w[i]; return s2; };
    rel(wsum(pdlZRule.apply(null,pdlZRange(23,0.5,0,null))),1,1e-14,
      'at PhET’s launchers the speed truncation is unreachable: its acceptance is 1');
    const vw2=wsum(pdlZRule.apply(null,pdlZRange(2,1,0,null)));
    ok(vw2>0.976&&vw2<0.978,'at 2 ± 1 m/s it is 0.977 — and there the divisor is doing something ('+fmt(vw2,4)+')');
    const cfgT={meanSpeed:2,sdSpeed:1,meanAng:30,sdAng:0.2,h:0,raised:false,mult:1};
    const ET=pdlExact(cfgT);
    const I1=simp(r=>r*pdlPdf(r,cfgT),0,ET.mean+9*ET.sd,2000);
    rel(I1,ET.mean,3e-3,'and with it the density’s first moment is still the exact mean ('
      +fmt(I1,4)+' vs '+fmt(ET.mean,4)+'; r·f goes as √r at the origin, so Simpson stalls at 2.3e-5 however fine the grid)');
    ok(Math.abs(I1/vw2-ET.mean)/ET.mean>0.02,'… while dropping the divisor would put it 2 % out'); }
  { const cfg=cfgMystery(1);
    rel(pdlProbIn(cfg,40,60,100),REF.pIn4060,1e-7,'P(40 ≤ x ≤ 60) for launcher 1 (derive)');
    rel(pdlProbIn(cfg,0,200,200),1,1e-6,'and the whole line carries probability 1');
    /* the density is NOT the normal the delta method would draw: its skewness
       is real, and this is the assertion that says so */
    const E=pdlExact(cfg);
    const pl2=pdlProbIn(cfg,E.mean-3*E.sd,E.mean,100), pr=pdlProbIn(cfg,E.mean,E.mean+3*E.sd,100);
    ok(pl2<pr,'the density is left-skewed about its mean, as μ₃ = '+fmt(E.mu3,3)+' says');
    ok(Math.abs(pl2-pr)>1e-4,'… by more than rounding ('+(pr-pl2).toExponential(2)+')');
  }
  TIMES.D=Date.now();

  /* ============ F. the statistics, against numpy ============ */
  { const cfg=cfgMystery(1);
    const F=fieldMake(REF.sampleSeed,cfg);
    fieldBatch(F,REF.sampleN);
    const X=fieldXs(F);
    eq(X.length,REF.sampleN,'the reference field holds 500 landed projectiles');
    for(let i=0;i<5;i++) rel(X[i],REF.sampleFirst5[i],1e-15,'landing distance #'+i+' matches Python to 4 ulp (derive)');
    rel(X[X.length-1],REF.sampleLast,1e-15,'and so does #499 (derive)');
    rel(pdlMean(X),REF.sMean,1e-14,'the mean equals numpy’s (derive)');
    rel(pdlMedian(X),REF.sMedian,1e-15,'the median equals numpy’s (derive)');
    rel(pdlSd(X,1),REF.sSd1,1e-13,'the n−1 standard deviation equals numpy’s ddof=1 (derive)');
    rel(pdlSd(X,0),REF.sSd0,1e-13,'the n standard deviation equals numpy’s ddof=0 (derive)');
    rel(pdlSe(X),REF.sSe,1e-13,'the standard error equals numpy’s s/√n (derive)');
    rel(pdlSd(X,1)/pdlSd(X,0),Math.sqrt(500/499),1e-14,'the two conventions differ by exactly √(n/(n−1))');
    rel(Math.min.apply(null,X),REF.sMin,1e-14,'the smallest (derive)');
    rel(Math.max.apply(null,X),REF.sMax,1e-14,'the largest (derive)');
    /* the sample is a draw from the exact law, and its mean must sit within
       the standard error the law itself predicts */
    const E=pdlExact(cfg);
    ok(Math.abs(pdlMean(X)-E.mean)<4*E.sd/Math.sqrt(500),
       '500 launches average within 4 σ/√n of the exact mean ('+fmt(pdlMean(X),4)+' vs '+fmt(E.mean,4)+')');
    const sdTol=E.sd*Math.sqrt((E.mu4/Math.pow(E.sd,4)-1)/(4*500));
    ok(Math.abs(pdlSd(X,1)-E.sd)<4*sdTol,'and their standard deviation within 4 of its own sampling sd ('+fmt(sdTol,4)+' m)');
    /* every bin width, against numpy's histogram on the same data */
    for(const w of PDL.BINW){
      const Hh=pdlHistogram(X,w), R2=REF.binCounts[''+w];
      eq(Hh.lo,R2[0],'bin width '+w+': the first bin index equals numpy’s (derive)');
      eq(JSON.stringify(Hh.counts),JSON.stringify(R2[1]),'bin width '+w+': every count equals numpy’s (derive)');
      let s=0; for(const c of Hh.counts) s+=c;
      eq(s,X.length,'bin width '+w+': the counts add to 500');
    }
    eq(pdlFraction(X,40,60),REF.sFrac4060,'the interval tool’s fraction equals numpy’s, exactly (it is a count) (derive)');
    /* the binning RULE, at the edges where it is decided */
    eq(pdlBinIndex(46,2),23,'floor(x/w): 46 m at w = 2 is bin 23');
    eq(pdlBinIndex(46-1e-12,2),22,'and a hair below 46 is bin 22 — the left edge belongs to the upper bin');
    eq(pdlBinIndex(0,0.5),0,'0 is bin 0');
    eq(pdlHistogram([1,1.5,3.5],1).lo,1,'a histogram starts at the lowest occupied bin');
    eq(JSON.stringify(pdlHistogram([1,1.5,3.5],1).counts),'[2,0,1]','… and carries the empty bins between');
    eq(pdlHistogram([1,1.999999,2,3.5],1).counts[1],1,'a value on a bin edge goes to the bin above it');
  }
  /* the estimators' own contracts */
  ok(pdlSd([],1)===null&&pdlSd([5],1)===null,'the n−1 standard deviation is null below two values, as PhET returns null');
  ok(pdlSd([5,7],1)!==null,'… and defined at two');
  rel(pdlSd([5,7],1),Math.sqrt(2),1e-15,'s of {5, 7} is √2');
  rel(pdlSd([5,7],0),1,1e-15,'and the n convention gives 1');
  rel(pdlMedian([3,1,2]),2,0,'the median of an odd sample is the middle value');
  /* the median reads symmetric positions out of the sorted array, so it does
     not care which way the sort ran — the mutation sweep reports the reversed
     comparator as a survivor, and this is why (Known-bad: when a property is
     invariant, assert the invariance rather than leaving a blind spot) */
  { const a=[5,1,9,3,7,2], b=a.slice().reverse();
    rel(pdlMedian(a),pdlMedian(b),0,'the median is the same whichever order the input arrives in');
    rel(pdlMedian([1,2,3,4]),pdlMedian([4,3,2,1]),0,'… for an even sample as well as an odd one'); }
  rel(pdlMedian([4,1,3,2]),2.5,0,'and of an even one the mean of the middle two');
  ok(pdlMedian([])===null&&pdlMean([])===null,'both are null on no data');
  { const a=[1,2,3]; pdlMedian(a); eq(JSON.stringify(a),'[1,2,3]','the median does not sort the caller’s array in place'); }
  eq(pdlFraction([1,2,3,4],2,3),0.5,'the interval counts both ends closed');
  eq(pdlFraction([1,2,3,4],2.0001,2.9999),0,'… and moving the edges a hair inwards drops BOTH');
  eq(pdlFraction([2],2,2),1,'a zero-width interval still catches a value sitting on it');
  eq(pdlFraction([1,2,3,4],3,2),0.5,'… and the edges may be given either way round');
  eq(pdlFraction([],0,1),0,'no data is no fraction, not a division by zero');
  { /* the sampling run, against numpy */
    const F=fieldMake(REF.sampSeed,cfgMystery(1));
    sampleBatch(F,REF.sampSize,REF.sampN);
    const MS=sampleMeans(F);
    eq(MS.length,REF.sampN,'the reference sampling run holds 200 sample means');
    for(let i=0;i<3;i++) rel(MS[i],REF.sampFirst3[i],1e-15,'sample mean #'+i+' equals Python’s (derive)');
    rel(pdlMean(MS),REF.sampMean,1e-14,'the mean of the sample means equals numpy’s (derive)');
    rel(pdlSd(MS,1),REF.sampSd,1e-13,'their standard deviation equals numpy’s (derive)');
    rel(pdlMedian(MS),REF.sampMedian,1e-15,'their median equals numpy’s (derive)');
    const Hh=pdlHistogram(MS,0.5);
    eq(Hh.lo,REF.sampBins[0],'their histogram starts where numpy’s does (derive)');
    eq(JSON.stringify(Hh.counts),JSON.stringify(REF.sampBins[1]),'and every count matches (derive)');
    /* a sample mean really is the mean of its own sample */
    let worst=0;
    for(const s of F.samples) worst=Math.max(worst,Math.abs(s.mean-pdlMean(s.xs)));
    ok(worst===0,'every stored sample mean is the mean of the sample it came from');
    eq(F.samples[0].xs.length,REF.sampSize,'and each sample holds n launches');
  }
  TIMES.E=Date.now();

  /* ============ G. the central limit theorem ============ */
  { const cfg=cfgMystery(1), E=pdlExact(cfg);
    rel(E.mean,REF.clMean,1e-14,'the parent mean μ (derive)');
    rel(E.sd,REF.clSigma,1e-13,'the parent σ (derive)');
    rel(E.skew,REF.clSkew,1e-11,'its skewness (derive)');
    rel(E.kurt,REF.clKurt,1e-10,'its excess kurtosis (derive)');
    const M=REF.clM, rng=pdlRng(31337);
    PDL.SIZES.forEach((n,i)=>{
      const means=new Array(M);
      for(let k=0;k<M;k++){
        let s=0;
        for(let j=0;j<n;j++){ const d=pdlDraw(rng,cfg); s+=pdlRange(d.v,d.ang,cfg.h); }
        means[k]=s/n;
      }
      const se=pdlSd(means,1), want=E.sd/Math.sqrt(n);
      rel(want,REF.clSe[i],1e-13,'n = '+n+': σ/√n is derive.py’s '+fmt(REF.clSe[i],5)+' m');
      /* the tolerance is the sampling sd of a standard error measured over M
         samples, σ_n√((κ_n+2)/4M) — computed, not chosen */
      const tol=REF.clSeTol[i];
      rel(tol,want*Math.sqrt((E.kurt/n+2)/(4*M)),1e-9,'n = '+n+': the tolerance is that formula (derive)');
      ok(Math.abs(se-want)<4*tol,'n = '+n+': '+M+' samples measure SE = '+fmt(se,4)+' m against σ/√n = '
         +fmt(want,4)+' m, inside 4 × '+fmt(tol,4));
      ok(Math.abs(pdlMean(means)-E.mean)<4*want/Math.sqrt(M),
         'n = '+n+': and the sample means are still centred on μ (averaging biases nothing)');
      /* the OTHER half of the theorem: the skewness falls as 1/√n */
      let m3=0; const mm=pdlMean(means);
      for(const x of means){ const d=x-mm; m3+=d*d*d; }
      const sk=m3/M/Math.pow(se,3), wantSk=E.skew/Math.sqrt(n);
      ok(Math.abs(sk-wantSk)<5*Math.sqrt(6/M)+0.02,'n = '+n+': the sample mean’s skewness is '+fmt(sk,3)
         +' against skew/√n = '+fmt(wantSk,3));
    });
    /* the 1/√n law itself, as a ratio that cannot be faked by a scale factor */
    const r1=E.sd/Math.sqrt(2), r2=E.sd/Math.sqrt(40);
    rel(r1/r2,Math.sqrt(20),1e-14,'σ/√2 over σ/√40 is exactly √20');
  }
  TIMES.F=Date.now();

  /* ============ H. the panels and the drawing ============ */
  { let bad=null;
    for(const cfg of CONFIGS){
      applyConfig(cfg);
      const M=buildModel();
      const ro=readoutHTML(M), eb=eqbarHTML(M), tg=tagHTML(M);
      for(const [nm,s] of [['readout',ro],['eqbar',eb],['tag',tg],['info',INFO[ST.view]],['deriv',DERIV[ST.view]]]){
        if(!s||!s.length){ bad=cfg[0]+': '+nm+' is empty'; break; }
        if(/NaN|undefined|Infinity/.test(s)){ bad=cfg[0]+': '+nm+' contains NaN/undefined/Infinity'; break; }
      }
      if(bad) break;
      /* the formatter renders a non-finite as '—', so "no NaN" is vacuous on
         its own: assert a number only a live model can supply (Known-bad) */
      if(ro.indexOf(fmt(M.exact.mean,3)+' m')<0){ bad=cfg[0]+': the readout does not print the exact mean '+fmt(M.exact.mean,3); break; }
      if(M.view==='sampling'){
        if(M.mstat.sd1!==null&&ro.indexOf(fmt(M.mstat.sd1,4)+' m')<0){ bad=cfg[0]+': the readout does not print the sd of the sample means '+fmt(M.mstat.sd1,4); break; }
      } else if(M.stat&&M.stat.n>1&&ro.indexOf(fmt(M.stat.sd1,4)+' m')<0){ bad=cfg[0]+': the readout does not print s = '+fmt(M.stat.sd1,4); break; }
    }
    ok(!bad,'every view × configuration builds clean panels'+(bad?' ('+bad+')':''));
  }
  { /* every slider and chip setting, for a finite model */
    let bad=null;
    for(const v of TABS.map(t=>t[0])){
      for(const lau of [1,2,3,4,5,6]) for(const o of ORIENTS) for(const stab of [0,0.5,1]){
        Object.assign(ST,DEFAULTS);
        ST.view=v; ST.lau=lau; ST.mLau=lau; ST.pLau=lau; ST.xLau=lau; ST.cLau=lau;
        ST.orient=o.id; ST.xOrient=o.id; ST.stab=stab; ST.cM=100;
        resetAllWorlds();
        const M=buildModel();
        if(!(isFinite(M.exact.mean)&&isFinite(M.exact.sd)&&M.exact.sd>0)){ bad=v+'/'+lau+'/'+o.id+'/'+stab; break; }
        if(M.stat&&!(M.stat.n===0||isFinite(M.stat.mean))){ bad=v+'/'+lau+' stat'; break; }
      }
      if(bad) break;
    }
    ok(!bad,'every launcher × orientation × stability gives a finite model in every view'+(bad?' ('+bad+')':''));
  }
  TIMES.G=Date.now();
  { /* the layout sweep: text on the canvas, no collisions, nothing under the
       #hint, no legend crossed by a data curve */
    const SIZES2=[[1400,820],[1100,712],[820,560],[560,380]];
    let textBad=null, hintBad=null, collide=null, legBad=null, blank=null;
    const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
    for(const cfg of CONFIGS){
      applyConfig(cfg);
      for(const [W,H] of SIZES2){
        const ctx=makeShot(W,H);
        drawView(ctx,W,H,buildModel());
        const texts=ctx.ops.filter(o=>o.op==='text');
        if(ctx.ops.length<20&&!blank) blank=cfg[0]+' '+W+'x'+H+' drew only '+ctx.ops.length+' ops';
        for(const t of texts){
          if(entRe.test(t.t)&&!textBad) textBad=cfg[0]+' '+W+'x'+H+': entity/tag "'+t.t.slice(0,32)+'"';
          if(/NaN|undefined/.test(t.t)&&!textBad) textBad=cfg[0]+' '+W+'x'+H+': "'+t.t.slice(0,32)+'"';
          if((t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1)&&!textBad)
            textBad=cfg[0]+' '+W+'x'+H+': off canvas "'+t.t.slice(0,28)+'" ['+t.bb.map(v=>fmt(v,0))+']';
          /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left */
          if(t.bb[0]<340&&t.bb[3]>H-27&&!hintBad) hintBad=cfg[0]+' '+W+'x'+H+': "'+t.t.slice(0,28)+'" under the #hint';
        }
        for(let i=0;i<texts.length&&!collide;i++) for(let j=i+1;j<texts.length;j++){
          const a=texts[i].bb,b=texts[j].bb;
          const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
          if(ox>0.5&&oy>0.5){ collide=cfg[0]+' '+W+'x'+H+': "'+texts[i].t.slice(0,20)+'" vs "'+texts[j].t.slice(0,20)+'"'; break; }
        }
        for(const r of LEGEND_RECTS){ for(let i=0;i<POLY_SEGS.length&&!legBad;i+=4){
          const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
          if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
          legBad=cfg[0]+' '+W+'x'+H+': a data curve runs through a legend';
        } }
      }
    }
    ok(!textBad,'the layout sweep finds clean, on-canvas text'+(textBad?' ('+textBad+')':''));
    ok(!hintBad,'nothing is drawn under the #hint line'+(hintBad?' ('+hintBad+')':''));
    ok(!collide,'no two text boxes overlap'+(collide?' ('+collide+')':''));
    ok(!legBad,'no legend has a data curve through it'+(legBad?' ('+legBad+')':''));
    ok(!blank,'every view draws something at every size'+(blank?' ('+blank+')':''));
  }
  { /* the exact-law view's bins follow sigma, because it does not show the
       bin chips and a control a view hides must not still decide its picture */
    for(const [x,want] of [[0.37,0.5],[0.4,0.5],[0.8,1],[1.2,1],[1.6,2],[3.9,5],[8,10],[0.09,0.1]])
      rel(niceStep(x),want,1e-12,'niceStep('+x+') is '+want);
    for(const lau of [1,3,5]) for(const o of ['angle30','angle0Raised']){
      Object.assign(ST,DEFAULTS); ST.view='exact'; ST.xLau=lau; ST.xOrient=o; ST.binW=10; resetAllWorlds();
      const M=buildModel();
      rel(M.binW,niceStep(M.exact.sd/4),0,'launcher '+lau+' '+o+': the exact view bins at σ/4 ('+fmt(M.binW,3)+' m), not at the chips’ 10 m');
      ok(M.hist.counts.length>=6,'… so its density has at least six bars to show a shape ('+M.hist.counts.length+')');
    }
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the raised orientation has no v²sin2θ/g and no delta method, and the
       two comparison panels must SAY so rather than draw an empty axis */
    Object.assign(ST,DEFAULTS); ST.view='exact'; ST.xOrient='angle0Raised'; resetAllWorlds();
    const M=buildModel();
    ok(M.naive===null&&M.delta===null,'the raised launcher has neither shortcut');
    const ctx=makeShot(1400,820);
    drawView(ctx,1400,820,M);
    const txt=ctx.ops.filter(o=>o.op==='text').map(o=>o.t).join(' ');
    ok(/neither applies/.test(txt),'and the panels say why they are empty');
    ok(LEGEND_RECTS.length<=1,'with no legend left floating over an empty axis ('+LEGEND_RECTS.length+')');
    Object.assign(ST,DEFAULTS); ST.view='exact'; resetAllWorlds();
    const ctx2=makeShot(1400,820);
    drawView(ctx2,1400,820,buildModel());
    ok(!/neither applies/.test(ctx2.ops.filter(o=>o.op==='text').map(o=>o.t).join(' ')),
       '… and a ground orientation draws the bars instead');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the histogram really carries the data: the bars' total area is n */
    applyConfig(['field default',{view:'field'}]);
    const M=buildModel();
    let total=0; for(const c of M.hist.counts) total+=c;
    eq(total,M.stat.n,'the drawn histogram accounts for every landed projectile');
    /* and the field and the histogram share one x axis, which is the point */
    const ctx=makeShot(1200,760);
    const G=drawView(ctx,1200,760,M);
    ok(Math.abs(G.map.X(0)-G.hm.px(0))<1e-9&&Math.abs(G.map.X(100)-G.hm.px(100))<1e-9,
       'the field and the histogram share the same x mapping, so a bar sits under the shots that made it');
  }
  { /* the interval tool's geometry follows its own numbers */
    Object.assign(ST,DEFAULTS); ST.view='measures'; ST.e1=20; ST.e2=70; resetAllWorlds();
    const M=buildModel();
    const ctx=makeShot(1200,760);
    drawView(ctx,1200,760,M);
    const S2={W:1200,H:760,measure:()=>ctx,st:ST};
    const hit=intervalHit(S2,0,0);
    ok(hit===null,'a pointer at the top-left of the stage grabs no interval edge');
    const ph=measCaption(M,'1.00'), L=labStage(ctx,1200,760,ph.full,ph.short,{histFrac:0.46});
    const x1=L.hist.x+L.hist.w*ST.e1/PDL.FIELD;
    const g=intervalHit(S2,x1,L.hist.y+10);
    ok(g&&g.what==='e1','a pointer on the left edge grabs it');
    const g2=intervalHit(S2,L.hist.x+L.hist.w*ST.e2/PDL.FIELD,L.hist.y+10);
    ok(g2&&g2.what==='e2','a pointer on the right edge grabs that one');
    const g3=intervalHit(S2,L.hist.x+L.hist.w*45/PDL.FIELD,L.hist.y+10);
    ok(g3&&g3.what==='mid','and one in the middle grabs the whole window');
  }
  TIMES.H=Date.now();

  console.log('section times, s: '+['A','B','C','D','E','F','G','H'].map((k,i,a)=>
    k+' '+((TIMES[k]-(i?TIMES[a[i-1]]:T0))/1000).toFixed(1)).join(', '));
  Object.assign(ST,stSave); resetAllWorlds();
  console.log(pass+' passed, '+fail+' failed  ('+fmt((Date.now()-T0)/1000,1)+' s)');
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
