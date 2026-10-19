
/* ================================================================== *
 *  selfTest — headless verification.  Values labelled (derive) are    *
 *  lines of build/projectile-sampling-distributions/refvals.txt, the  *
 *  printed output of derive.py, read in full; REF (p7a_refs.js) is    *
 *  the same numbers, written by derive.py so none is retyped.         *
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
   them instead of waited for */
function stubRng(list){
  let i=0;
  return {next(){ return 0.5; }, gauss(){ return i<list.length?list[i++]:0; }};
}
const CONFIGS=[
  ['field default',{view:'field'}],
  ['field n = 2, launcher 6',{view:'field',pN:2,pLau:6,binW:1}],
  ['field n = 40, blocks',{view:'field',pN:40,pLau:3,blocks:true,binW:2}],
  ['field empty',{view:'field',pLau:4},()=>{ fieldClear(curField(ST)); }],
  ['field one sample',{view:'field',pLau:5},()=>{ const F=curField(ST); fieldClear(F); sampleBatch(F,ST.pN,1); }],
  ['field no standard error',{view:'field',showSe:false,pLau:2,zoom:0}],
  ['sizes default',{view:'sizes'}],
  ['sizes launcher 6, 200 samples',{view:'sizes',sLau:6,sM:200,binW:1}],
  ['sizes launcher 5, 20 samples',{view:'sizes',sLau:5,sM:20,binW:0.5}],
  ['sizes no normals',{view:'sizes',sLau:3,showNormal:false}],
  ['parent default',{view:'parent'}],
  ['parent launcher 6, 500',{view:'parent',xLau:6,xN:500,binW:2}],
  ['parent launcher 5, 50',{view:'parent',xLau:5,xN:50,binW:0.5}],
  ['parent empty',{view:'parent'},()=>{ fieldClear(worldOf('parent').F); }],
  ['parent no density',{view:'parent',xLau:4,showDensity:false}],
  ['clt default',{view:'clt'}],
  ['clt launcher 6, 200',{view:'clt',cLau:6,cM:200}],
  ['clt launcher 5, no normals',{view:'clt',cLau:5,cM:100,showNormal:false}],
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

  /* ============ A. PhET's constants, this sim's branch of them ============ */
  rel(PDL.G,REF.G,0,'g is PhET’s 9.81 (derive)');
  rel(PDL.FIELD,REF.FIELD,0,'the field is PhET’s 100 m (derive)');
  eq(JSON.stringify(PDL.BINW),JSON.stringify(REF.BINW),'the bin widths are PhET’s [0.5, 1, 2, 5] for THIS sim (derive)');
  ok(PDL.BINW.indexOf(10)<0,'… and not the data lab’s 10 m');
  rel(PDL.BINW_DEF,REF.BINW_DEFAULT,0,'the default bin width is 0.5 m, not the data lab’s 1 (derive)');
  eq(JSON.stringify(PDL.ZOOM_MAX),JSON.stringify(REF.ZOOM_MAX),'the vertical-scale ladder runs to 250 samples (derive)');
  { /* the auto rung picks the TIGHTEST of PhET's own rungs that holds the
       tallest bin — a ceiling PhET offers, never a number of its own */
    for(const [m,want] of [[0,4],[3,4],[4,6],[6,8],[9,15],[18,25],[22,50],[43,50],[44,75],[200,250],[400,250]])
      eq(autoZoom(m),want,'auto zoom at a tallest bin of '+m+' picks 0–'+want);
    for(const m of [30,60,90,140,190]) ok(PDL.ZOOM_MAX.indexOf(autoZoom(m))>=0,
      'above 20 samples every rung it picks is one of PhET’s ('+autoZoom(m)+')');
    ok(autoZoom(10)>=10*1.15,'and every rung holds the bin it was chosen for');
    /* a bin can never hold more than a full field, which PhET caps at 200, so
       the ladder only has to reach that far — and it does */
    for(let m=0;m<=PDL.MAX_SAMPLES;m+=7) ok(autoZoom(m)>=Math.max(4,m),'auto zoom never crops the tallest bin (at '+m+')');
    ok(autoZoom(PDL.MAX_SAMPLES)>=PDL.MAX_SAMPLES,'and the top rung holds a whole field of '+PDL.MAX_SAMPLES+' samples in one bin'); }
  eq(JSON.stringify(PDL.SIZES),JSON.stringify(REF.SAMPLE_SIZES),'the sample sizes are PhET’s 2, 5, 15, 40 (derive)');
  rel(PDL.MAX_SAMPLES,REF.MAX_SAMPLES,0,'at most 200 samples a field (derive)');
  /* against derive.py, not against itself: the first sweep survived a mutant
     on this ceiling because the assertion read PDL.MAX_PROJ on both sides */
  rel(PDL.MAX_PROJ,REF.MAX_PROJ,0,'and 500 projectiles (derive)');
  rel(PDL.SPEED_MEAN_MIN,20,0,'the speed-mean range floor is 20 m/s here, 15 in the data lab');
  const SAMPVIEW='field', SAMPMODE='mode';
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
  eq(ORIENTS.length,1,'the Sampling screen has ONE orientation (its fields carry validValues:[angle30])');
  rel(ORIENTS[0].ang,REF.MEAN_ANGLE,0,'and it is 30° (derive)');
  eq(ORIENTS[0].h,0,'so nothing here is launched from a height');
  eq(PTYPES.length,1,'and one projectile type, the cannonball');
  rel(PTYPES[0].mult,1,0,'whose speed multiplier is 1');
  for(const k in REF.MECH){
    rel(MECH[k].mean,REF.MECH[k][0],0,'mechanism '+k+': PhET’s mean speed (derive)');
    rel(MECH[k].sd,REF.MECH[k][1],0,'mechanism '+k+': PhET’s speed sd (derive)');
  }
  LAUNCHERS.forEach((l,i)=>{
    rel(l.sdAng,REF.LAUNCH_SD[i],0,'mystery launcher '+(i+1)+': PhET’s angle sd (derive)');
    eq(l.mech,REF.LAUNCH_MECH[i],'mystery launcher '+(i+1)+': PhET’s mechanism (derive)');
  });

  /* ============ B. the random stream ============ */
  { const r=pdlRng(REF.sampSeed);
    /* next() is integer arithmetic all the way, so it is bit-identical across
       the two languages; everything downstream passes through log, cos and
       sqrt, where a libm may differ in the last bit, so those are pinned at
       four ulp rather than at zero */
    for(let i=0;i<6;i++) rel(r.next(),REF.rngStream[i],0,'mulberry32 draw '+i+' is bit-identical to Python (derive)');
    const r2=pdlRng(REF.sampSeed);
    for(let i=0;i<6;i++) rel(r2.gauss(),REF.gaussStream[i],1e-15,'Box–Muller value '+i+' matches Python to 4 ulp (derive)');
    const N=200000, u=new Array(N), r3=pdlRng(11);
    for(let i=0;i<N;i++) u[i]=r3.next();
    close(pdlMean(u),0.5,4/Math.sqrt(12*N),'200k uniforms average 0.5 within 4 se');
    close(Math.pow(pdlSd(u,1),2),1/12,4*(1/12)*Math.sqrt(2/N),'their variance is 1/12 within 4 se');
    const g=new Array(N), r4=pdlRng(11);
    for(let i=0;i<N;i++) g[i]=r4.gauss();
    close(pdlMean(g),0,4/Math.sqrt(N),'200k normals average 0 within 4 se');
    close(Math.pow(pdlSd(g,1),2),1,4*Math.sqrt(2/N),'their variance is 1 within 4 se');
  }
  TIMES.A=Date.now();

  /* ============ C. the trajectory and PhET's launch mechanism ============ */
  REF.rangeCases.forEach(c=>{
    rel(pdlRange(c[0],c[1],c[2]),c[3],1e-15,'the range at v = '+c[0]+', 30° (derive)');
    rel(pdlFlight(c[0],c[1],c[2]),c[4],1e-15,'the flight time there (derive)');
  });
  for(const th of [5,15,30,45,60,75,85]) rel(pdlRange(23,th,0),23*23*Math.sin(2*th*Math.PI/180)/PDL.G,1e-15,
    'h = 0: the range is v² sin2θ/g at θ = '+th+'°');
  for(const [v,th,h] of [[23,30,0],[25,60,0],[23,0,12],[24,-7,12]]){
    const T=pdlFlight(v,th,h);
    rel(v*Math.cos(th*Math.PI/180)*T,pdlRange(v,th,h),1e-14,'x(T) is the range at v='+v+', θ='+th+', h='+h);
    close(pdlHeight(v,th,h,T),0,1e-11*Math.max(1,h),'and the projectile is on the ground at T');
  }
  rel(pdlMaxAngle(23,0),45,1e-13,'from the ground the best angle is 45°');
  ok(pdlMaxAngle(23,12)<45,'from a height it is below 45° (the engine keeps the general form)');
  { /* v* round-trips the range */
    let worst2=0;
    for(const th of [3,12,30,45,60,80]) for(const r of [4,18,37,63,96]){
      const v=pdlVStar(r,th,0); if(v===null) continue;
      worst2=Math.max(worst2,Math.abs(pdlRange(v,th,0)/r-1));
    }
    ok(worst2<1e-13,'v*(r, θ) round-trips the range (worst '+worst2.toExponential(2)+')');
  }
  { /* PhET's re-draw windows, pinned at the values that DECIDE them rather
       than waited for: a stub stream puts the angle exactly where the window
       matters, which is the only way a 10-sigma guard can be tested */
    const cfg=pdlConfig('pressure',5,'angle30','cannonball');
    const a=pdlDraw(stubRng([11,0,0]),cfg);              /* 30 + 11×5 = 85° */
    rel(a.ang,85,1e-12,'an 85° draw is ACCEPTED: PhET’s angle window closes at 90, not lower');
    const b=pdlDraw(stubRng([12.1,0,0]),cfg);            /* 30 + 12.1×5 = 90.5 */
    rel(b.ang,30,1e-12,'a 90.5° draw is re-drawn (the window is open at 90)');
    const c=pdlDraw(stubRng([-6.1,0,0]),cfg);            /* 30 − 30.5 = −0.5 */
    rel(c.ang,30,1e-12,'and a −0.5° draw is re-drawn too');
    const d=pdlDraw(stubRng([-6,0,0]),cfg);              /* exactly 0 */
    rel(d.ang,30,1e-12,'0° itself is re-drawn: PhET’s test is a <= 0, not a < 0');
    /* the speed's own window */
    const e=pdlDraw(stubRng([0,-120,0.5]),cfg);          /* 24 − 24 = 0, then 24 + 0.1 */
    rel(e.v,cfg.meanSpeed+0.5*cfg.sdSpeed,1e-12,'a speed of 0 is re-drawn (PhET’s test is v <= 0)');
    const f=pdlDraw(stubRng([0,2]),cfg);
    rel(f.v,cfg.meanSpeed+2*cfg.sdSpeed,1e-12,'and an ordinary speed is taken as drawn');
    /* the order of the draws is the angle first, then the speed */
    const g=pdlDraw(stubRng([1,2]),cfg);
    rel(g.ang,cfg.meanAng+1*cfg.sdAng,1e-12,'the angle is drawn FIRST from the stream');
    rel(g.v,cfg.meanSpeed+2*cfg.sdSpeed,1e-12,'and the speed second');
  }
  TIMES.B=Date.now();

  /* ============ D. the quadrature and the exact law ============ */
  { let wx=0, ww=0;
    for(let i=0;i<PDL.NGL;i++){ wx=Math.max(wx,Math.abs(GL.x[i]-REF.glX[i])); ww=Math.max(ww,Math.abs(GL.w[i]-REF.glW[i])); }
    ok(wx<1e-14,'the 96 Gauss–Legendre nodes match numpy’s leggauss to '+wx.toExponential(2)+' (derive)');
    ok(ww<1e-13,'and the weights to '+ww.toExponential(2)+' (derive)');
    let s0=0,s2=0;
    for(let i=0;i<PDL.NGL;i++){ s0+=GL.w[i]; s2+=GL.w[i]*GL.x[i]*GL.x[i]; }
    rel(s0,2,1e-14,'Σw = 2'); rel(s2,2/3,1e-13,'Σw x² = 2/3');
    const R1=pdlZRule(-PDL.ZCAP,PDL.ZCAP);
    let tw=0, tz2=0;
    for(let i=0;i<PDL.NGL;i++){ tw+=R1.w[i]; tz2+=R1.w[i]*R1.z[i]*R1.z[i]; }
    rel(tw,1,1e-13,'the ±12 sd normal rule integrates the density to 1');
    rel(tz2,1,1e-12,'and its second moment is 1');
  }
  REF.launcherStats.forEach((o,i)=>{
    const E=pdlExact(cfgMystery(i+1));
    rel(E.mean,o[0],1e-14,'launcher '+(i+1)+': the exact mean landing distance (derive)');
    rel(E.sd,o[1],1e-13,'launcher '+(i+1)+': the exact standard deviation (derive)');
    close(E.mu3,o[2],1e-12*Math.pow(o[1],3),'launcher '+(i+1)+': the third central moment (derive)');
    close(E.mu4,o[3],1e-12*Math.pow(o[1],4),'launcher '+(i+1)+': the fourth (derive)');
    ok(E.varr>0&&isFinite(E.skew)&&isFinite(E.kurt),'launcher '+(i+1)+': variance positive, shape finite');
  });
  REF.generalCases.forEach((c,i)=>{
    /* the screen fixes 30°, where the (0, 90) re-draw window sits six sigma
       out and nothing can see it.  The ENGINE is the general one, and at 60°
       with a 5° spread the window is four sigma out — which is where a test
       of it bites.  The first sweep survived a mutant that moved that window
       to 80° precisely because nothing was evaluated anywhere near it. */
    const cfg={meanSpeed:c[0],sdSpeed:c[1],meanAng:c[2],sdAng:c[3],h:0,raised:false,mult:1};
    const E=pdlExact(cfg);
    rel(E.mean,c[4],1e-14,'general case '+i+' (θ = '+c[2]+'° ± '+c[3]+'°): the exact mean (derive)');
    rel(E.sd,c[5],1e-13,'general case '+i+': the exact sd (derive)');
    const cf=pdlClosed(c[0],c[1],c[2],c[3]);
    rel(cf[0],c[6],1e-14,'general case '+i+': the untruncated closed-form mean (derive)');
    /* the second moment is the one that carries E[cos 4θ]; asserting only the
       first left the closed form's cosine term untested, and the sweep said so */
    rel(cf[1],c[7],1e-14,'general case '+i+': its second moment, which is where E[cos4θ] lives (derive)');
    rel(Math.sqrt(cf[1]-cf[0]*cf[0]),Math.sqrt(c[7]-c[6]*c[6]),1e-12,'general case '+i+': and the sd it implies');
  });
  { /* and the truncation is visible at 60°: six sigma to the window there, so
       the closed form and the quadrature part company by 5e-8 m, not by 0 */
    const c=REF.generalCases[0];
    const cfg={meanSpeed:c[0],sdSpeed:c[1],meanAng:c[2],sdAng:c[3],h:0,raised:false,mult:1};
    const gap=Math.abs(pdlClosed(c[0],c[1],c[2],c[3])[0]-pdlExact(cfg).mean);
    ok(gap>1e-9&&gap<1e-6,'at 60° ± 5° the (0, 90) window really does move the mean, by '+gap.toExponential(2)+' m'); }
  { /* the untruncated closed form stands beside the truncated quadrature, and
       the gap between them is what the re-draws are worth */
    let worst3=0;
    for(let n=1;n<=6;n++){
      const cfg=cfgMystery(n), E=pdlExact(cfg);
      const cf=pdlClosed(cfg.meanSpeed,cfg.sdSpeed,cfg.meanAng,cfg.sdAng);
      worst3=Math.max(worst3,Math.abs(cf[0]-E.mean));
      /* and it factorises exactly: the speed spread lengthens, the angle
         spread shortens */
      const w=cfg.sdAng*Math.PI/180;
      const naive=cfg.meanSpeed*cfg.meanSpeed*Math.sin(2*cfg.meanAng*Math.PI/180)/PDL.G;
      rel(E.mean/naive,(1+Math.pow(cfg.sdSpeed/cfg.meanSpeed,2))*Math.exp(-2*w*w),1e-8,
        'launcher '+n+': the mean is exactly (1 + σ_v²/μ²)·e^{−2σ_θ²} × v²sin2θ/g');
    }
    ok(worst3<1e-7&&worst3>0,'the truncation moves the mean by at most '+worst3.toExponential(2)+' m — measured, not assumed');
  }
  { /* the sampler and the quadrature must agree, which is the one thing that
       ties PhET's mechanism to the law drawn over it */
    /* drawn straight from the sampler, not through fieldBatch: a field stops
       at PhET's 500 projectiles, and a tolerance written for 20000 draws
       against 500 of them is a test that fails on correct code */
    const NB=20000;
    for(const n of [1,6]){
      const cfg=cfgMystery(n), E=pdlExact(cfg), rng=pdlRng(4242+n), xs=new Array(NB);
      for(let k=0;k<NB;k++){ const d=pdlDraw(rng,cfg); xs[k]=pdlRange(d.v,d.ang,cfg.h); }
      const se=E.sd/Math.sqrt(NB);
      ok(Math.abs(pdlMean(xs)-E.mean)<4*se,'launcher '+n+': '+NB+' launches average within 4 σ/√n of the exact mean ('
         +fmt(pdlMean(xs),4)+' vs '+fmt(E.mean,4)+')');
      const sdTol=E.sd*Math.sqrt((E.mu4/Math.pow(E.sd,4)-1)/(4*NB));
      ok(Math.abs(pdlSd(xs,1)-E.sd)<4*sdTol,'launcher '+n+': and their sd within 4 of its own sampling sd');
    }
    { /* and that cap is PhET's own MAX_PROJECTILES_VSM_FIELD_DEFAULT */
      const F=fieldMake(1,cfgMystery(1)); fieldBatch(F,REF.MAX_PROJ+200);
      eq(F.landed.length,REF.MAX_PROJ,'a field stops at PhET’s '+REF.MAX_PROJ+' projectiles (derive)');
      eq(fieldLaunch(F),null,'and refuses one more'); }
    /* the projectile's speed multiplier reaches the SAMPLER, not only the
       quadrature (this sim launches cannonballs, so the test builds the case
       the engine still supports) */
    const cfg2=pdlConfig('spring',ANG_C,'angle30','cannonball');
    const heavy=Object.assign({},cfg2,{mult:1.1});
    const E2=pdlExact(heavy);
    const rngH=pdlRng(77), xh=new Array(NB);
    for(let k=0;k<NB;k++){ const d=pdlDraw(rngH,heavy); xh[k]=pdlRange(d.v,d.ang,heavy.h); }
    ok(Math.abs(pdlMean(xh)-E2.mean)<4*E2.sd/Math.sqrt(NB),
       'a ×1.1 speed multiplier moves the SAMPLED mean to the exact law’s '+fmt(E2.mean,3)+' m ('+fmt(pdlMean(xh),3)+')');
    ok(E2.mean/pdlExact(cfg2).mean>1.2,'… which is 1.1² further than the ×1 one, not the same place');
  }
  TIMES.C=Date.now();

  /* ============ E. the density ============ */
  REF.launcherStats.forEach((o,i)=>{
    const cfg=cfgMystery(i+1);
    /* the VALUE, not only the integral: dropping the truncation normaliser
       moves the density by 1e-9, which an integral asserted at 2e-6 cannot
       see and a value asserted at 1e-12 can (the first sweep survived it) */
    rel(pdlPdf(o[0],cfg),REF.pdfAtMean[i],1e-12,'launcher '+(i+1)+': the density at its own mean (derive)');
    const lo=Math.max(1e-9,o[0]-9*o[1]), hi=o[0]+9*o[1];
    /* ONE pass for both moments: the density costs 8x96 evaluations a point
       now, and calling it twice over the same abscissae was twice the work */
    const [I0,I1]=simp3(x=>pdlPdf(x,cfg),lo,hi,200);
    rel(I0,1,2e-6,'launcher '+(i+1)+': the exact density integrates to 1');
    rel(I1,o[0],2e-6,'launcher '+(i+1)+': and to the exact mean');
    ok(pdlPdf(o[0],cfg)>0,'launcher '+(i+1)+': and is positive at that mean');
  });
  { /* a label that says "1 samples", and a caption promising a green bar the
       first sample cannot have (a spread needs two) */
    Object.assign(ST,DEFAULTS); ST.view='field'; resetAllWorlds();
    const F=curField(ST); fieldClear(F); fireField(ST);
    let g=0; while(F.samples.length<1&&g++<8000) worldStep(ST,1/60);
    eq(F.samples.length,1,'one sample taken');
    const one=fieldCaptionS(buildModel(),'1.00').full;
    ok(/appears with the second/.test(one),'at one sample the caption does not promise a green bar');
    F.firing=true;
    g=0; while(F.samples.length<2&&g++<8000) worldStep(ST,1/60);
    F.firing=false;
    ok(F.samples.length>=2&&/actually measured so far/.test(fieldCaptionS(buildModel(),'1.00').full),
      'and from the second it does');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* and the limit-theorem view's own normals checkbox */
    Object.assign(ST,DEFAULTS); ST.view='clt'; resetAllWorlds();
    const on=cltCaption(buildModel()).full;
    ok(/orange curves are normals/.test(on),'with the normals on, the caption names them');
    ST.showNormal=false;
    const off=cltCaption(buildModel()).full;
    ok(/switched off/.test(off)&&!/orange curves are normals/.test(off),
      'with them off it says so instead of describing curves that are not there');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* a caption that describes a curve the checkbox has switched off says
       something the picture does not: assert BOTH branches */
    Object.assign(ST,DEFAULTS); ST.view='parent'; resetAllWorlds();
    const on=parentCaption(buildModel()).full;
    ok(/the orange curve is not fitted/.test(on),'with the density on, the caption names the curve');
    ST.showDensity=false;
    const off=parentCaption(buildModel()).full;
    ok(/switched off/.test(off)&&!/the orange curve is not fitted/.test(off),
      'with it off the caption says so instead of describing a curve that is not drawn');
    ok(/standard deviation is σ/.test(off),'and σ is still named either way');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the panel count is a measurement, not a taste.  The density at a FIXED
       r integrates a SPIKE in theta — only the angles whose v*(r,theta) lands
       within a few sd of the mean speed contribute — so one 96-node rule rings
       around it wherever a small speed spread meets a large angle spread, which
       is launcher 2 exactly (0.2 m/s beside 5°).  The shipped rule must be
       converged AND the coarse ones must not be, or the constant is free. */
    let wK=0,w1=0,w2=0,whereK='',where1='';
    for(let L=1;L<=6;L++){
      const cfg=cfgMystery(L), M=pdlExact(cfg);
      const lo=Math.max(0,M.mean-4*M.sd), hi=M.mean+4*M.sd, np=L===2?31:9;
      for(let i=0;i<=np;i++){
        const r=lo+(hi-lo)*i/np, ref=pdlPdf(r,cfg,64);
        if(!(ref>0.02/M.sd)) continue;
        const dK=Math.abs(pdlPdf(r,cfg)-ref)/ref;
        const d1=Math.abs(pdlPdf(r,cfg,1)-ref)/ref;
        const d2=Math.abs(pdlPdf(r,cfg,2)-ref)/ref;
        if(dK>wK){ wK=dK; whereK='launcher '+L+' at r = '+fmt(r,1)+' m'; }
        if(d1>w1){ w1=d1; where1='launcher '+L+' at r = '+fmt(r,1)+' m'; }
        if(d2>w2) w2=d2;
      }
    }
    ok(wK<1e-9,'the density is converged in the panel count: worst '+wK.toExponential(1)
      +' against 64 panels ('+whereK+')');
    ok(w1>0.25,'and ONE panel is out by '+fmt(100*w1,0)+' % at '+where1
      +' — the ringing the panels exist to kill');
    ok(w2>0.005,'two panels are still '+fmt(100*w2,2)+' % out, so eight is not a round number');
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
  TIMES.D=Date.now();

  /* ============ F. the statistics, against numpy ============ */
  REF.sampRuns.forEach(R=>{
    const F=fieldMake(REF.sampSeed+R.n,cfgMystery(1));
    sampleBatch(F,R.n,REF.sampCount);
    const M=sampleMeans(F);
    eq(M.length,REF.sampCount,'n = '+R.n+': the reference run holds 200 sample means');
    for(let i=0;i<3;i++) rel(M[i],R.first3[i],1e-15,'n = '+R.n+': sample mean #'+i+' matches Python (derive)');
    rel(pdlMean(M),R.mean,1e-14,'n = '+R.n+': their mean equals numpy’s (derive)');
    rel(pdlSd(M,1),R.sd1,1e-13,'n = '+R.n+': their ddof=1 sd equals numpy’s (derive)');
    rel(pdlSd(M,0),R.sd0,1e-13,'n = '+R.n+': their ddof=0 sd equals numpy’s (derive)');
    rel(pdlMedian(M),R.median,1e-15,'n = '+R.n+': their median equals numpy’s (derive)');
    rel(pdlSd(M,1)/pdlSd(M,0),Math.sqrt(REF.sampCount/(REF.sampCount-1)),1e-14,
      'n = '+R.n+': the two sd conventions differ by exactly √(M/(M−1))');
    /* the standard error is on the readout and was asserted nowhere, which
       the first sweep found by surviving a divide-by-n mutant */
    rel(pdlSe(M),R.se,1e-13,'n = '+R.n+': their standard error equals numpy’s sd/√M (derive)');
    rel(pdlSe(M),pdlSd(M,1)/Math.sqrt(M.length),0,'n = '+R.n+': … which is s/√M, not s/M');
    ok(pdlSe(M)<pdlSd(M,1),'n = '+R.n+': and it is SMALLER than s, by a factor √M');
    const H=pdlHistogram(M,0.5);
    eq(H.lo,R.binLo,'n = '+R.n+': the histogram starts where numpy’s does (derive)');
    eq(JSON.stringify(H.counts),JSON.stringify(R.bins),'n = '+R.n+': and every count matches (derive)');
    let s=0; for(const c of H.counts) s+=c;
    eq(s,REF.sampCount,'n = '+R.n+': the counts add to 200');
    /* a sample mean is the mean of its own sample, and a sample is n launches */
    let worstM=0;
    for(const sm of F.samples) worstM=Math.max(worstM,Math.abs(sm.mean-pdlMean(sm.xs)));
    ok(worstM===0,'n = '+R.n+': every stored mean is the mean of the sample it came from');
    eq(F.samples[0].xs.length,R.n,'n = '+R.n+': and each sample holds n launches');
  });
  /* the estimators' own contracts */
  ok(pdlSd([],1)===null&&pdlSd([5],1)===null,'the n−1 standard deviation is null below two values, as PhET returns null');
  rel(pdlSd([5,7],1),Math.sqrt(2),1e-15,'s of {5, 7} is √2');
  rel(pdlSd([5,7],0),1,1e-15,'and the n convention gives 1');
  rel(pdlSe([5,7]),Math.sqrt(2)/Math.sqrt(2),1e-15,'the standard error of {5, 7} is √2/√2 = 1');
  ok(pdlSe([5])===null,'and it is null where s is');
  rel(pdlMedian([4,1,3,2]),2.5,0,'the median of an even sample is the mean of the middle two');
  eq(pdlBinIndex(46,2),23,'floor(x/w): 46 m at w = 2 is bin 23');
  eq(pdlBinIndex(46-1e-12,2),22,'and a hair below 46 is bin 22 — the left edge belongs to the upper bin');
  eq(JSON.stringify(pdlHistogram([1,1.5,3.5],1).counts),'[2,0,1]','a histogram carries the empty bins between');
  TIMES.E=Date.now();

  /* ============ G. the central limit theorem ============ */
  { const cfg=cfgMystery(1), E=pdlExact(cfg);
    rel(E.mean,REF.clMean,1e-14,'the parent mean μ (derive)');
    rel(E.sd,REF.clSigma,1e-13,'the parent σ (derive)');
    rel(E.skew,REF.clSkew,1e-11,'its skewness (derive)');
    rel(E.kurt,REF.clKurt,1e-10,'its excess kurtosis (derive)');
    const M=REF.clM, rng=pdlRng(90210);
    PDL.SIZES.forEach((n,i)=>{
      const means=new Array(M);
      for(let k=0;k<M;k++){
        let s=0;
        for(let j=0;j<n;j++){ const d=pdlDraw(rng,cfg); s+=pdlRange(d.v,d.ang,cfg.h); }
        means[k]=s/n;
      }
      const se=pdlSd(means,1), want=E.sd/Math.sqrt(n);
      rel(want,REF.clSe[i],1e-13,'n = '+n+': σ/√n is derive.py’s '+fmt(REF.clSe[i],5)+' m');
      const tol=REF.clSeTol[i];
      rel(tol,want*Math.sqrt((E.kurt/n+2)/(4*M)),1e-9,'n = '+n+': the tolerance is σ_n√((κ_n+2)/4M) (derive)');
      ok(Math.abs(se-want)<4*tol,'n = '+n+': '+M+' samples measure SE = '+fmt(se,4)+' m against σ/√n = '
         +fmt(want,4)+' m, inside 4 × '+fmt(tol,4));
      ok(Math.abs(pdlMean(means)-E.mean)<4*want/Math.sqrt(M),
         'n = '+n+': and the sample means are still centred on μ');
      let m3=0; const mm=pdlMean(means);
      for(const x of means){ const d=x-mm; m3+=d*d*d; }
      const sk=m3/M/Math.pow(se,3);
      ok(Math.abs(sk-E.skew/Math.sqrt(n))<5*Math.sqrt(6/M)+0.02,
         'n = '+n+': the sample mean’s skewness is '+fmt(sk,3)+' against skew/√n = '+fmt(E.skew/Math.sqrt(n),3));
    });
    rel((E.sd/Math.sqrt(2))/(E.sd/Math.sqrt(40)),Math.sqrt(20),1e-14,'σ/√2 over σ/√40 is exactly √20');
    /* the width half needs no theorem: it is exact at n = 2, where nothing is
       normal.  Assert var(x̄) = σ²/n directly from the sampler. */
    const K=20000, rng2=pdlRng(4711), ms=new Array(K);
    for(let k=0;k<K;k++){ const a=pdlDraw(rng2,cfg), b=pdlDraw(rng2,cfg);
      ms[k]=0.5*(pdlRange(a.v,a.ang,cfg.h)+pdlRange(b.v,b.ang,cfg.h)); }
    const want2=E.sd/Math.sqrt(2);
    const tol2=want2*Math.sqrt((E.kurt/2+2)/(4*K));
    ok(Math.abs(pdlSd(ms,1)-want2)<4*tol2,'at n = 2 the spread is already σ/√2 = '+fmt(want2,4)
       +' m ('+fmt(pdlSd(ms,1),4)+'), and no central limit theorem is involved');
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
      /* fmt() prints a non-finite as '—', so "no NaN" is vacuous on its own:
         ask for a number only a live model can supply */
      if(ro.indexOf(fmt(M.exact.sd,4)+' m')<0){ bad=cfg[0]+': the readout does not print σ = '+fmt(M.exact.sd,4); break; }
      if(M.view==='field'&&M.mstat.sd1!==null&&ro.indexOf(fmt(M.mstat.sd1,4)+' m')<0){
        bad=cfg[0]+': the readout does not print the measured spread '+fmt(M.mstat.sd1,4); break; }
    }
    ok(!bad,'every view × configuration builds clean panels'+(bad?' ('+bad+')':''));
  }
  { let bad=null;
    for(const v of TABS.map(t=>t[0])) for(let lau=1;lau<=6;lau++) for(const n of PDL.SIZES){
      Object.assign(ST,DEFAULTS);
      ST.view=v; ST.pLau=lau; ST.sLau=lau; ST.xLau=lau; ST.cLau=lau; ST.pN=n; ST.cM=100; ST.sM=20;
      resetAllWorlds();
      const M=buildModel();
      if(!(isFinite(M.exact.mean)&&isFinite(M.exact.sd)&&M.exact.sd>0)){ bad=v+'/'+lau+'/'+n; break; }
    }
    ok(!bad,'every launcher × sample size gives a finite model in every view'+(bad?' ('+bad+')':''));
  }
  TIMES.G=Date.now();
  { const SIZES2=[[1400,820],[1100,712],[820,560],[560,380]];
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
  { /* a caption clause conditioned on the data must be conditioned on the CASE
       making sense too: "visibly not a normal" is false for launcher 5, whose
       parent has skewness 0.028 and excess kurtosis 0.001 */
    const loud=pdlExact(cfgMystery(2)), quiet=pdlExact(cfgMystery(5));
    ok(Math.abs(loud.skew)>0.05,'launcher 2’s parent is visibly skewed ('+fmt(loud.skew,3)+')');
    ok(Math.abs(quiet.skew)<0.05&&Math.abs(quiet.kurt)<0.05,'launcher 5’s is not ('+fmt(quiet.skew,3)+', '+fmt(quiet.kurt,4)+')');
    Object.assign(ST,DEFAULTS); ST.view='parent'; ST.xLau=2; resetAllWorlds();
    ok(/visibly not a normal/.test(parentCaption(buildModel()).full),'and the caption says so for launcher 2');
    Object.assign(ST,DEFAULTS); ST.view='parent'; ST.xLau=5; resetAllWorlds();
    ok(!/visibly not a normal/.test(parentCaption(buildModel()).full),'… and does NOT say so for launcher 5');
    ok(/little for the theorem to do/.test(parentCaption(buildModel()).full),'saying instead what is true there');
    Object.assign(ST,DEFAULTS); resetAllWorlds(); }
  { /* the launcher drag's geometry follows the picture it is drawn in */
    Object.assign(ST,DEFAULTS); ST.view='field'; resetAllWorlds();
    const ctx=makeShot(1200,760);
    drawView(ctx,1200,760,buildModel());
    const S2={W:1200,H:760,measure:()=>ctx,st:ST};
    ok(launcherHit(S2,3,3)===null,'a pointer at the top-left of the stage grabs no launcher');
    const M=buildModel(), ph=fieldCaptionS(M,'1.00');
    const L=labStage(ctx,1200,760,ph.full,ph.short,{histFrac:0.52,fieldWant:fieldWantH(M)});
    const map=fieldMap(L.field,M);
    const g=launcherHit(S2,map.X(0),map.Y(0)-10);
    ok(g&&g.what==='launcher','a pointer on the barrel grabs it');
    ok(launcherHit(S2,map.X(0)+120,map.Y(0)-10)===null,'and one 120 px down the field does not');
    Object.assign(ST,DEFAULTS); ST.view='clt'; resetAllWorlds();
    ok(launcherHit(S2,map.X(0),map.Y(0)-10)===null,'there is no launcher to grab on the limit-theorem view');
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
