
/* ================================================================== *
 *  state, the three clocks (the live string, the reflection demo, the *
 *  standing-wave run), the per-view model, readout, eqbar, tag        *
 * ================================================================== */
const TABS=[['str','the string'],['xt','the space-time'],['refl','the reflections'],
            ['stand','the standing waves'],['disp','the dispersion']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', chain:'#9a7fd1', dn:'#5ac8e0', text:'#aeb6c6', bead2:'#5c7a22'};
const RO_W=300;
const MODE_LIST=[{id:'manual',name:'manual'},{id:'osc',name:'oscillate'},{id:'pulse',name:'pulse'}];
const END_LIST=[{id:'fixed',name:'fixed end'},{id:'loose',name:'loose end'},{id:'none',name:'no end'}];
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'slow',name:'slow motion'}];
const ENDS=['fixed','loose','none'];

/* PhET's defaults (manual, fixed end, amplitude 0.75 cm, 1.5 Hz, 0.5 s, damping
   0.2, full tension, playing, normal speed, every tool hidden).  Tool positions
   are world cm: the rulers' zero marks, the reference line's height (PhET's
   1.45 cm), the stopwatch's top-left corner. */
const DEFAULTS={view:'str', mode:'manual', end:'fixed', amp:0.75, freq:1.5, pw:0.5, damping:0.2, tension:TMAX,
                running:true, speed:'normal', rulers:false, stopwatch:false, refline:false, alpha:1,
                rhX:0, rhY:-1.95, rvX:-2.55, rvY:-2.5, refY:REF_Y0, swX:0.3, swY:2.62};
const ST=Object.assign({},DEFAULTS);
const HMAX=240;                 /* the space-time view keeps this many lattice levels: two round trips, so a stripe tilts ~7 degrees */

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function simFactor(st){ return st.speed==='slow'?SLOW:1; }

/* ---- the live string (views 1 and 2) -----------------------------------------
   acc = sim time since the current level; t = the sim time of the current level;
   phase = the oscillator's phase at the current level; wr/wrPrev = the wrench now
   and at the start of this frame (the lattice steps inside a frame see it
   interpolated, as PhET's ticks do); sw = the stopwatch. */
const LIVE={lat:makeLat(NSEG), acc:0, t:0, phase:0, pulseOn:false, pulseT0:0, wr:0, wrPrev:0,
            sw:0, swOn:false, arrows:true, hist:[], histT:[]};
function liveRestart(){
  latClear(LIVE.lat); LIVE.acc=0; LIVE.t=0; LIVE.phase=0; LIVE.pulseOn=false; LIVE.pulseT0=0;
  LIVE.wr=0; LIVE.wrPrev=0; LIVE.hist=[]; LIVE.histT=[];
}
/* the left end at the next lattice time tn; frac = how far through this frame tn falls */
function liveDriver(st,dt,tn,frac){
  if(st.mode==='osc'){ LIVE.phase=(LIVE.phase+TAU*st.freq*dt)%TAU; return st.amp*Math.sin(LIVE.phase); }
  if(st.mode==='pulse'){
    if(!LIVE.pulseOn) return 0;
    const u=(tn-LIVE.pulseT0)/st.pw;
    if(u>=1) LIVE.pulseOn=false;
    return st.amp*tri(u);
  }
  return LIVE.wrPrev+(LIVE.wr-LIVE.wrPrev)*frac;
}
function liveStepOnce(st,frac){
  const dt=dtOf(st.tension), tn=LIVE.t+dt;
  const yl=liveDriver(st,dt,tn,frac===undefined?1:frac);
  latStep(LIVE.lat,1,betaOf(st.damping),st.end,yl);
  LIVE.t=tn;
  LIVE.hist.push(Float64Array.from(LIVE.lat.cur)); LIVE.histT.push(tn);
  if(LIVE.hist.length>HMAX){ LIVE.hist.shift(); LIVE.histT.shift(); }
}
/* a whole number of steps with a guard: 60 frames of 1/60 s leave acc at
   0.019999... < 0.02 and the clock would fall a step behind (Known-bad) */
const STEP_TOL=1e-9;
/* advance the live string by dtSim seconds of simulated time */
function liveAdvance(st,dtSim){
  const dt=dtOf(st.tension), t0=LIVE.t+LIVE.acc;
  LIVE.acc+=dtSim;
  let n=0;
  while(LIVE.acc>=dt*(1-STEP_TOL)){
    LIVE.acc-=dt;
    liveStepOnce(st,dtSim>0?clamp((LIVE.t+dt-t0)/dtSim,0,1):1);
    n++;
  }
  LIVE.wrPrev=LIVE.wr;
  if(LIVE.swOn) LIVE.sw+=dtSim;
  return n;
}
/* the step button: exactly one lattice step, whatever the frame clock says */
function liveStepButton(st){ LIVE.acc=0; liveStepOnce(st,1); LIVE.wrPrev=LIVE.wr; if(LIVE.swOn) LIVE.sw+=dtOf(st.tension); }
function sendPulse(st){
  if(st.mode!=='pulse'||LIVE.pulseOn) return false;
  LIVE.pulseOn=true; LIVE.pulseT0=LIVE.t+LIVE.acc; return true;
}
/* the drawn string: interior beads between the last two levels (PhET's yDraw),
   bead 0 where the driver is NOW */
function liveLeftNow(st){
  if(st.mode==='osc') return st.amp*Math.sin(LIVE.phase+TAU*st.freq*LIVE.acc);
  if(st.mode==='pulse') return LIVE.pulseOn?st.amp*tri((LIVE.t+LIVE.acc-LIVE.pulseT0)/st.pw):0;
  return LIVE.wr;
}
function liveDraw(st){
  const L=LIVE.lat, dt=dtOf(st.tension), s=clamp(LIVE.acc/dt,0,1), y=new Float64Array(NSEG+1);
  for(let i=1;i<=NSEG;i++) y[i]=L.prev[i]+(L.cur[i]-L.prev[i])*s;
  y[0]=liveLeftNow(st);
  if(st.end==='fixed') y[NSEG]=0;
  return y;
}

/* ---- the reflection demo (view 3): one pulse, three ends, undamped, whole steps ---- */
const REFL={key:'', lats:null, n:0, acc:0};
function reflKey(st){ return [st.amp,st.pw,st.tension].join('|'); }
function reflLoop(st){ return 2*NSEG+Math.ceil(st.pw/dtOf(st.tension))+14; }
function reflReset(st){ REFL.lats={fixed:makeLat(NSEG),loose:makeLat(NSEG),none:makeLat(NSEG)}; REFL.n=0; REFL.acc=0; REFL.key=reflKey(st); }
function reflStep(st){
  if(REFL.key!==reflKey(st)) reflReset(st);
  if(REFL.n>=reflLoop(st)) reflReset(st);
  REFL.n++;
  const yl=st.amp*tri(REFL.n*dtOf(st.tension)/st.pw);
  for(const e of ENDS) latStep(REFL.lats[e],1,0,e,yl);
}
function reflAdvance(st,dtSim){
  if(REFL.key!==reflKey(st)) reflReset(st);
  const dt=dtOf(st.tension); REFL.acc+=dtSim; let n=0;
  while(REFL.acc>=dt*(1-STEP_TOL)){ REFL.acc-=dt; reflStep(st); n++; }
  return n;
}
/* the whole demo run once, for the numbers: the reflection each end returns
   (the extreme of y_30 on the way back over the extreme on the way in) and the
   largest departure from d'Alembert anywhere, any step */
function reflSummary(st){
  return memo('reflsum',reflKey(st),()=>{
    const v=speedOf(st.tension), dt=dtOf(st.tension), nL=reflLoop(st), out={};
    const tIn=(30*DX)/v+st.pw, tBack=(2*LSTR-30*DX)/v;
    for(const e of ENDS){
      const L=makeLat(NSEG); let dev=0, inc=0, back=0;
      for(let n=1;n<=nL;n++){
        latStep(L,1,0,e,st.amp*tri(n*dt/st.pw));
        for(let i=0;i<=NSEG;i++) dev=Math.max(dev,Math.abs(L.cur[i]-imageSeries(e,st.amp,st.pw,v,n*dt,i*DX)));
        const y=L.cur[30], t=n*dt;
        if(t<=tIn&&Math.abs(y)>Math.abs(inc)) inc=y;
        if(t>tBack&&t<=tBack+st.pw+dt&&Math.abs(y)>Math.abs(back)) back=y;
      }
      out[e]={dev,inc,back,r:Math.abs(inc)>0?back/inc:NaN};
    }
    return out;
  });
}

/* ---- the standing-wave run (view 4): the oscillator from rest ---- */
const STAND={key:'', lat:null, n:0, acc:0, phase:0};
function standKey(st){ return [st.freq,st.amp,st.damping,st.tension,st.end].join('|'); }
function standReset(st){ STAND.lat=makeLat(NSEG); STAND.n=0; STAND.acc=0; STAND.phase=0; STAND.key=standKey(st); }
function standStep(st){
  if(STAND.key!==standKey(st)) standReset(st);
  const dt=dtOf(st.tension);
  STAND.phase=(STAND.phase+TAU*st.freq*dt)%TAU;
  latStep(STAND.lat,1,betaOf(st.damping),st.end,st.amp*Math.sin(STAND.phase));
  STAND.n++;
}
function standAdvance(st,dtSim){
  if(STAND.key!==standKey(st)) standReset(st);
  const dt=dtOf(st.tension); STAND.acc+=dtSim; let n=0;
  while(STAND.acc>=dt*(1-STEP_TOL)){ STAND.acc-=dt; standStep(st); n++; }
  return n;
}
function standDraw(st){
  const L=STAND.lat, s=clamp(STAND.acc/dtOf(st.tension),0,1), y=new Float64Array(NSEG+1);
  for(let i=0;i<=NSEG;i++) y[i]=L.prev[i]+(L.cur[i]-L.prev[i])*s;
  return y;
}
/* the response curve: the largest steady amplitude anywhere on the string, over A */
const FGRID_N=420, FLO=0.01;
function responseCurve(st){
  return memo('resp',[st.damping,st.tension,st.end].join('|'),()=>{
    const b=betaOf(st.damping), fn=resonances(st.end,st.tension,FMAX);
    const fs=[]; for(let k=0;k<=FGRID_N;k++) fs.push(FLO+(FMAX-FLO)*k/FGRID_N);
    for(const f of fn) fs.push(f);
    fs.sort((a,c)=>a-c);
    const gb=[], g0=[];
    for(const f of fs){
      gb.push(steadyMax(steadyClosed(f,1,b,st.tension,st.end)));
      const onRes=fn.some(x=>Math.abs(x-f)<1e-12);
      g0.push(onRes?NaN:steadyMax(steadyClosed(f,1,0,st.tension,st.end)));
    }
    return {fs,gb,g0,fn,b};
  });
}

/* ---- the dispersion view ---- */
function dispModel(st){
  return memo('disp',[st.alpha,st.damping,st.tension,st.amp,st.pw,st.freq].join('|'),()=>{
    const a=st.alpha, b0=betaOf(st.damping), ba=a*b0;   /* the same PHYSICAL damping at any a */
    const K=[], om=[], omPhet=[], chain=[], cont=[], vp=[], vg=[], vgChain=[];
    for(let k=0;k<=240;k++){
      const kap=Math.PI*k/240; K.push(kap);
      om.push(omegaNorm(kap,a,ba)); omPhet.push(omegaNorm(kap,1,b0)); chain.push(chainOmegaNorm(kap)); cont.push(kap);
      vp.push(kap>0?vpOverV(kap,a,ba):NaN); vg.push(vgOverV(kap,a,ba)); vgChain.push(chainVgOverV(kap));
    }
    const v=speedOf(st.tension), xcen=0.72*LSTR;
    /* the pulses run UNDAMPED, so that only the dispersion changes their shape */
    const P=longPulse(a,0,st.amp,st.pw,st.tension,xcen);
    const Pc=longPulse(0.05,0,st.amp,st.pw,st.tension,xcen);   /* the bead chain (a -> 0, converged to O(a^2)) */
    const ex=t=>{ const y=[]; for(let i=0;i<=NSEG;i++) y.push(st.amp*tri((t-i*DX/v)/st.pw)); return y; };
    const exP=ex(P.t), exC=ex(Pc.t);
    let dev=0, devC=0; for(let i=0;i<=NSEG;i++){ dev=Math.max(dev,Math.abs(P.y[i]-exP[i])); devC=Math.max(devC,Math.abs(Pc.y[i]-exC[i])); }
    /* the oscillator's wave on each dispersion relation: k from omega */
    const thOsc=TAU*st.freq*a*DX/v;                          /* omega dt at this a */
    const sArg=Math.sin(thOsc/2)/a;
    const kOsc=(b0===0&&sArg<=1)?2*Math.asin(sArg):NaN;      /* undamped inverse; with damping solved below */
    return {a,b0,ba,K,om,omPhet,chain,cont,vp,vg,vgChain,P,Pc,exP,exC,dev,devC,v,xcen,
            kOsc:isFinite(kOsc)?kOsc:kapFromOmega(TAU*st.freq*DX/v,a,ba),
            wOsc:TAU*st.freq*DX/v, zone:Math.PI/DX, fChain:v/(Math.PI*DX), fLat:v/(2*a*DX),
            cut:cutoffKap(ba)};
  });
}
/* invert omega dx/v = theta(kap)/a for kap (bisection on the monotone branch) */
function kapFromOmega(wn,a,b){
  let lo=cutoffKap(b), hi=Math.PI;
  if(!(omegaNorm(hi,a,b)>=wn)) return NaN;
  for(let k=0;k<80;k++){ const m=(lo+hi)/2; if(omegaNorm(m,a,b)<wn) lo=m; else hi=m; }
  return (lo+hi)/2;
}

/* ---- the model ---- */
/* the model carries a SNAPSHOT of the state, so a readout rendered later
   cannot read whatever state ran last */
function buildModel(){
  const st=Object.assign({},ST), view=st.view, v=speedOf(st.tension), dt=dtOf(st.tension), b=betaOf(st.damping);
  const M={view,st,v,dt,b,T:st.tension,running:st.running};
  if(view==='str'||view==='xt'){
    M.y=liveDraw(st); M.t=LIVE.t+LIVE.acc; M.steps=LIVE.lat.steps; M.sw=LIVE.sw; M.swOn=LIVE.swOn;
    let mx=0, at=0; for(let i=0;i<=NSEG;i++) if(Math.abs(M.y[i])>mx){ mx=Math.abs(M.y[i]); at=i; }
    M.maxAbs=mx; M.maxAt=at; M.offScale=mx>YHALF;
    M.left=M.y[0]; M.right=M.y[NSEG]; M.pulseOn=LIVE.pulseOn;
    M.lambda=st.freq>0?v/st.freq:Infinity; M.rNone=noEndReflection(st.freq>0?st.freq:1.5,b,st.tension);
    M.phaseNow=LIVE.phase+TAU*st.freq*LIVE.acc;
    if(view==='xt'){ M.hist=LIVE.hist; M.histT=LIVE.histT;
      let hm=mx; for(const r of LIVE.hist) for(let i=0;i<r.length;i++) hm=Math.max(hm,Math.abs(r[i])); M.hmax=hm; }
  }
  if(view==='refl'){
    if(REFL.key!==reflKey(st)) reflReset(st);
    M.n=REFL.n; M.tR=REFL.n*dt; M.loop=reflLoop(st); M.lats=REFL.lats; M.sum=reflSummary(st);
  }
  if(view==='stand'){
    if(STAND.key!==standKey(st)) standReset(st);
    M.S=steadyClosed(st.freq,st.amp,b,st.tension,st.end); M.Smax=steadyMax(M.S);
    M.env=M.S.Y.map(cabs); M.y=standDraw(st); M.n=STAND.n;
    let mx=0; for(let i=0;i<=NSEG;i++) mx=Math.max(mx,Math.abs(M.y[i])); M.latMax=mx;
    M.resp=responseCurve(st); M.fn=M.resp.fn; M.lambda=st.freq>0?v/st.freq:Infinity;
    M.transient=Math.pow(keepPerStep(b),STAND.n);
    let near=null; for(let k=0;k<M.fn.length;k++) if(near===null||Math.abs(M.fn[k]-st.freq)<Math.abs(M.fn[near]-st.freq)) near=k;
    M.near=near; M.rNone=noEndReflection(st.freq,b,st.tension);
    M.nodes=nodesOf(M.env,M.Smax);
  }
  if(view==='disp') M.D=dispModel(st);
  return M;
}
/* nodes: interior local minima of the envelope below 15 % of its maximum, and the fixed end */
function nodesOf(env,mx){
  const out=[];
  for(let i=1;i<NSEG;i++) if(env[i]<=env[i-1]&&env[i]<=env[i+1]&&env[i]<0.15*mx) out.push(i);
  if(env[NSEG]<1e-12*Math.max(mx,1e-300)) out.push(NSEG);
  return out;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
const YHALF=2.7;                /* the string view shows y in [-2.7, 2.7] cm */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function cm(x,n){ return sigf(x,n||3)+' cm'; }
function modeName(m){ return MODE_LIST.find(o=>o.id===m).name; }
function endName(e){ return END_LIST.find(o=>o.id===e).name; }
function endRows(M){
  const st=M.st;
  if(st.end==='fixed') return rrow('fixed end','reflects inverted, r = &minus;1');
  if(st.end==='loose') return rrow('loose end','reflects upright, r = +1')+rrow('&hellip; about','x = '+fmt(LLOOSE,4)+' cm (bead 59&frac12;)');
  return rrow('no end','absorbs: exact at zero damping')+rrow('&hellip; leaks at '+(st.freq>0?fmt(st.freq,2):'1.50')+' Hz','|r| = '+sigf(M.rNone,2),M.rNone>0.02?'bad':'good');
}
function stringRows(M){
  const st=M.st;
  return hd('the string')+rrow('tension T (relative)',fmt(st.tension,3))
    +rrow('wave speed v',fmt(M.v,3)+' cm/s','good')+rrow('lattice step &Delta;t = &Delta;x/v',sigf(M.dt*1000,3)+' ms ('+sigf(1/M.dt,3)+' per s)')
    +rrow('61 beads, 1.25 mm apart',fmt(LSTR,1)+' cm, crossed in '+sigf(LSTR/M.v,3)+' s');
}
function dampRows(M){
  return hd('damping '+fmt(M.st.damping,2))+rrow('&beta; per step',sigf(M.b,3))
    +rrow('kept per bead, e<sup>&minus;atanh &beta;</sup>',sigf(keepPerStep(M.b),4))
    +rrow('decay length &Delta;x/atanh &beta;',isFinite(decayLength(M.b))?cm(decayLength(M.b)):'none');
}
function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">wave on a string<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='str'||M.view==='xt'){
    s+=stringRows(M);
    s+=hd('the wave: '+modeName(st.mode));
    if(st.mode==='manual') s+=rrow('wrench height',cm(M.left,3));
    else if(st.mode==='osc') s+=rrow('frequency, period',fmt(st.freq,2)+' Hz, '+(st.freq>0?sigf(1/st.freq,3)+' s':'&infin;'))+rrow('wavelength &lambda; = v/f',isFinite(M.lambda)?cm(M.lambda):'&infin;','good')+rrow('amplitude',cm(st.amp,3));
    else s+=rrow('pulse width w, length v&middot;w',fmt(st.pw,2)+' s, '+cm(M.v*st.pw))+rrow('height',cm(st.amp,3))+rrow('generator',M.pulseOn?'sending':'ready');
    s+=dampRows(M);
    s+=hd('the far end')+endRows(M);
    if(M.view==='str') s+=hd('now')+rrow('t, lattice steps',fmt(M.t,2)+' s, '+M.steps)+rrow('largest |y|',cm(M.maxAbs,3)+' (bead '+M.maxAt+')',M.offScale?'bad':'')
      +(st.stopwatch?rrow('stopwatch',fmt(M.sw,2)+' s'+(M.swOn?' (running)':'')):'');
    else s+=hd('the record')+rrow('levels kept',(M.hist?M.hist.length:0)+' of '+HMAX)+rrow('spanning',M.hist&&M.hist.length>1?fmt(M.histT[M.histT.length-1]-M.histT[0],2)+' s':'&mdash;');
  }
  else if(M.view==='refl'){
    const R=M.sum;
    s+=stringRows(M)+hd('the pulse')+rrow('height A, width w',cm(st.amp,3)+', '+fmt(st.pw,2)+' s')+rrow('step n of the loop',M.n+' / '+M.loop);
    for(const e of ENDS){
      const r=R[e];
      s+=hd(endName(e))+rrow('reflected / incident (bead 30)',isFinite(r.r)?fmt(r.r,3):'&mdash;',e==='none'?'':'good')
        +rrow('max |lattice &minus; d&rsquo;Alembert|',sigf(r.dev,2)+' cm',r.dev<1e-12?'good':'bad');
    }
  }
  else if(M.view==='stand'){
    s+=stringRows(M)+hd('the oscillator')+rrow('frequency f',fmt(st.freq,3)+' Hz')+rrow('wavelength v/f',isFinite(M.lambda)?cm(M.lambda):'&infin;');
    if(M.near!==null){ const n=M.near+1, fn=M.fn[M.near];
      s+=rrow(st.end==='fixed'?'nearest f<sub>'+n+'</sub> = '+n+'v/2L':'nearest f<sub>'+n+'</sub> = '+(2*n-1)+'v/4L&prime;',fmt(fn,4)+' Hz'); }
    else s+=rrow('resonances','none: nothing comes back');
    s+=hd('the steady state (exact)')+rrow('largest amplitude / A',sigf(M.Smax/Math.max(st.amp,1e-300),4),'good')
      +rrow('largest amplitude',cm(M.Smax,4))+rrow('nodes on the string',String(M.nodes.length));
    s+=hd('the lattice run')+rrow('steps from rest',String(M.n))+rrow('its largest |y| now',cm(M.latMax,4))
      +rrow('transient left, (e<sup>&minus;atanh &beta;</sup>)<sup>n</sup>',M.b>0?sigf(M.transient,2):'never decays',M.b>0&&M.transient<1e-3?'good':'bad');
    if(st.end==='none') s+=rrow('the absorber leaks |r|',sigf(M.rNone,2));
  }
  else {
    const D=M.D;
    s+=hd('the lattice')+rrow('Courant number &alpha; = v&Delta;t/&Delta;x',fmt(D.a,2)+(D.a===1?' (PhET)':''))+rrow('wave speed v',fmt(D.v,3)+' cm/s')
      +rrow('zone edge k = &pi;/&Delta;x',sigf(D.zone,3)+' rad/cm')+rrow('lattice Nyquist f = v/2&alpha;&Delta;x',sigf(D.fLat,3)+' Hz')
      +rrow('bead chain tops out at v/&pi;&Delta;x',sigf(D.fChain,3)+' Hz');
    s+=hd('the oscillator, '+fmt(st.freq,2)+' Hz')+rrow('k&Delta;x on the lattice',isFinite(D.kOsc)?sigf(D.kOsc,4)+' rad':'overdamped')
      +rrow('phase speed / v',isFinite(D.kOsc)?sigf(vpOverV(D.kOsc,D.a,D.ba),5):'&mdash;')+rrow('group speed / v',isFinite(D.kOsc)?sigf(vgOverV(D.kOsc,D.a,D.ba),5):'&mdash;');
    s+=hd('the pulse after 5.4 cm, undamped')+rrow('max |lattice &minus; exact| (&alpha; = '+fmt(D.a,2)+')',sigf(D.dev,2)+' cm',D.dev<1e-12?'good':'bad')
      +rrow('bead chain (&alpha; &rarr; 0)',sigf(D.devC,2)+' cm','bad')+rrow('damping &beta; per step at this &alpha;',sigf(D.ba,3));
  }
  s+='</table><div class="note">PhET&rsquo;s lattice steps at &alpha; = v&Delta;t/&Delta;x = 1 exactly: the tension sets the clock, never the stencil. '
    +'PhET&rsquo;s values (61 beads, 0.125 cm, 50 steps/s, &beta; = 0.1 &times; damping) are from its build 1.2.4; everything else is exact and pinned in selfTest to derive.py.</div>';
  return s;
}

function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='str') return E('<span class="hl">(1+&beta;) y<sub>i</sub><sup>n+1</sup> = y<sub>i+1</sub><sup>n</sup> + y<sub>i&minus;1</sub><sup>n</sup> &minus; (1&minus;&beta;) y<sub>i</sub><sup>n&minus;1</sup></span> &nbsp;&middot;&nbsp; &alpha; = v&Delta;t/&Delta;x = 1, &nbsp; v = v<sub>max</sub>&radic;(T/T<sub>max</sub>)',
    'each bead goes to the sum of its neighbours&rsquo; positions less its own previous one: at &alpha; = 1 that moves every wave exactly one bead per step');
  if(M.view==='xt') return E('<span class="hl">y(x, t) = f(x &minus; vt) + g(x + vt)</span> &nbsp;&middot;&nbsp; y<sub>i</sub><sup>n</sup> = F(n &minus; i) + G(n + i) <span class="rm">on the lattice, exactly</span>',
    'd&rsquo;Alembert: any motion of the string is two shapes sliding in opposite directions at v — the stripes of the space-time picture');
  if(M.view==='refl') return E('<span class="hl">y = f(t &minus; x/v) &mp; f(t &minus; (2L &minus; x)/v)</span> &nbsp;&middot;&nbsp; <span class="rm">fixed: &minus;, &nbsp; loose: + about L&prime; = 59&frac12; &Delta;x, &nbsp; no end: no image</span>',
    'the end is a mirror: a fixed end holds y = 0, so the image pulse must arrive upside down; a loose end holds the slope at zero, so it arrives upright');
  if(M.view==='stand') return E('<span class="hl">f<sub>n</sub> = n v/2L</span> <span class="rm">(fixed)</span>, &nbsp; <span class="hl">(2n&minus;1) v/4L&prime;</span> <span class="rm">(loose)</span> &nbsp;&middot;&nbsp; Y<sub>i+1</sub> + Y<sub>i&minus;1</sub> = 2(cos &theta; + i&beta; sin &theta;) Y<sub>i</sub>',
    'the driven end reflects too, so waves that fit a whole number of round trips pile up: the peak grows as 1/(N&beta;) when the damping goes');
  return E('<span class="hl">(1+&beta;) z&sup2; &minus; 2(1 &minus; 2&alpha;&sup2; sin&sup2;(k&Delta;x/2)) z + (1&minus;&beta;) = 0</span> &nbsp;&middot;&nbsp; &alpha; = 1, &beta; = 0 <span class="rm">&rArr;</span> &omega; = vk &nbsp;&middot;&nbsp; <span class="rm">bead chain:</span> &omega; = (2v/&Delta;x) sin(k&Delta;x/2)',
    'at &alpha; = 1 the time step exactly cancels the chain&rsquo;s dispersion: PhET&rsquo;s beads carry a continuous string, not a chain of beads');
}
function tagHTML(M){
  const st=M.st;
  if(M.view==='str') return '<b>the string</b> — '+modeName(st.mode)+', '+endName(st.end)+(st.running?'':', paused')+(st.speed==='slow'?', slow motion':'');
  if(M.view==='xt') return '<b>the space-time</b> — the last '+HMAX+' lattice steps of the string, time running up';
  if(M.view==='refl') return '<b>the reflections</b> — one pulse, three ends, no damping';
  if(M.view==='stand') return '<b>the standing waves</b> — '+fmt(st.freq,3)+' Hz, '+endName(st.end);
  return '<b>the dispersion</b> — &alpha; = '+fmt(st.alpha,2)+(st.alpha===1?' (PhET)':'');
}
