
/* ================================================================== *
 *  state, the per-view model, readout, equation bar, tag              *
 * ================================================================== */
const TABS=[['harm','the harmonics'],['conv','the convergence'],['spec','the spectrum'],
            ['game','the wave game'],['pack','the wave packet'],['pair','the transform pair']];
const COL={sum:'#b8ec4c', ideal:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', warn:'#e8843a', guess:'#b8ec4c', target:'#cd35c4',
           env:'#e8843a', cont:'#e8843a', zero:'#39405a'};
const RO_W=300;
const SERIES_LIST=[{id:'sin',name:'sines'},{id:'cos',name:'cosines'}];
const WPDOM_LIST=[{id:'space',name:'space (k, x)'},{id:'time',name:'time (&omega;, t)'}];
/* the eleven harmonic colours: the house NEON ramp, which is a scale, not a role */
function harmCol(n){ return neonCss((n-1)/(NMAX-1)); }
/* the transform-pair view's own component-spacing slider: this file's, not
   PhET's four fixed values, so the copies can be watched walking out */
const PAIR_K1_MIN=0.4, PAIR_K1_MAX=TAU;

const DEFAULTS={view:'harm', preset:'sinusoid', series:'sin', domain:'space', N:11, sel:1,
                t:0, running:false, showHarm:true, showInf:false, caliper:false, calX:0,
                convM:6, convPre:'square',
                level:1, seed:1, showAns:false,
                wpK0:WP_K0_DEF, wpSk:WP_SK_DEF, wpSp:3, wpEnv:true, wpWid:true, wpDom:'space',
                pairK1:PI, pairSk:WP_SK_DEF};
/* the eleven amplitudes live beside ST, because Object.assign would alias the
   array and a reset would then write through to the defaults.  There are TWO
   sets, as in PhET: the Discrete screens' series and the game's guess.  One
   shared array would mean starting the game wiped the waveform you had built
   (and it did, until the UI drive caught it). */
const ST=Object.assign({},DEFAULTS);
const AMPS=new Array(NMAX).fill(0);
const GUESS=new Array(NMAX).fill(0);
function ampArray(){ return ST.view==='game'?GUESS:AMPS; }
function setAmps(a){ for(let i=0;i<NMAX;i++) AMPS[i]=i<a.length?a[i]:0; }
function setGuess(a){ for(let i=0;i<NMAX;i++) GUESS[i]=i<a.length?a[i]:0; }
function setCurrent(a){ if(ST.view==='game') setGuess(a); else setAmps(a); }
function ampsNow(){ return ampArray().slice(); }
/* PhET: choosing a waveform fills the amplitudes from its closed form, and
   editing one by hand turns the waveform into "custom" */
function applyPreset(){
  if(ST.preset==='custom') return;
  setAmps(presetAmps(ST.preset,ST.series,ST.N));
}
function resetAll(){
  const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v; applyPreset(); GAME.reset();
}

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---- the harmonics view: the drawn curves ------------------------- */
/* PhET plots x over one to five wavelengths; this file fixes the window at
   two periods of the fundamental, which is PhET's default zoom. */
function xWindow(domain){
  if(domain==='time') return [-TPER,TPER];
  return [-LWAVE,LWAVE];
}
function xUnits(domain){ return domain==='time'?'ms':'m'; }
/* every drawn curve goes through phaseAt, never phaseOf: the abscissa of the
   time domain is t, and handing it to phaseOf as x draws a flat line */
function curveSum(amps,series,domain,t,N,ns){
  const [a,b]=xWindow(domain), xs=[], ys=[];
  for(let j=0;j<=ns;j++){ const s=a+(b-a)*j/ns; xs.push(s); ys.push(seriesSum(amps,phaseAt(domain,s,t),series,N)); }
  return {xs,ys};
}
function curveHarmonic(amps,n,series,domain,t,ns){
  const [a,b]=xWindow(domain), xs=[], ys=[];
  for(let j=0;j<=ns;j++){ const s=a+(b-a)*j/ns; xs.push(s); ys.push(amps[n-1]*trigOf(series,n*phaseAt(domain,s,t))); }
  return {xs,ys};
}
function curveIdeal(name,series,domain,t,ns){
  const [a,b]=xWindow(domain), xs=[], ys=[];
  for(let j=0;j<=ns;j++){ const s=a+(b-a)*j/ns; xs.push(s); ys.push(idealWave(name,series,phaseAt(domain,s,t))); }
  return {xs,ys};
}
/* the y range PhET uses: it steps through fixed descriptions, the widest being
   +-5 for the sum.  This file fits the drawn data and rounds up to a nice
   number, and prints the number on the canvas. */
function yFit(ys,floor){
  let m=floor===undefined?0.5:floor;
  for(let i=0;i<ys.length;i++) if(isFinite(ys[i])) m=Math.max(m,Math.abs(ys[i]));
  const t=ticksFor(0,m*1.08,3);
  return Math.max(m*1.08,t[t.length-1]);
}
/* the caliper: PhET's wavelength/period tool.  Its width is the selected
   harmonic's own wavelength L/n (or period T/n), so placing it on the curve
   measures that harmonic. */
function caliperWidth(domain,n){ return (domain==='time'?TPER:LWAVE)/n; }

/* ---- the convergence view ----------------------------------------- */
const CONV_MS=[1,2,3,4,6,8,12,20,32,50,80,128];
function convModel(st){
  return memo('conv',[st.convPre,st.series,st.convM].join('|'),()=>{
    const name=st.convPre, series=(name==='sawtooth')?'sin':st.series;   /* PhET: a sawtooth needs sines */
    const M=st.convM;                                     /* harmonics kept, n = 1..M */
    const A=presetAmps(name,series,M);
    /* the partial sum over one period of the phase */
    const ns=2400, us=[], sm=[], id=[];
    for(let j=0;j<=ns;j++){ const u=-PI+TAU*j/ns; us.push(u); sm.push(seriesSum(A,u,series,M)); id.push(idealWave(name,series,u)); }
    /* the measured peak of the partial sum, next to the jump, and the closed
       form for the square wave written in its odd-harmonic count */
    const win=peakWindow(name);
    const pk=peakOf(u=>seriesSum(A,u,series,M),win[0],win[1],6000);
    const closed=(name==='square'&&series==='sin')?squarePeakClosed(oddCount(M)):null;
    /* the overshoot curve: the peak of the M-term square partial sum vs M */
    const ms=[], pks=[];
    for(let m=1;m<=64;m++){ ms.push(m); pks.push(squarePeakClosed(m).val); }
    /* the rms error against the complete waveform, for every order */
    const Ns=[], errs=[];
    for(let n=1;n<=128;n++){ Ns.push(n); errs.push(truncationRms(name,series,n)); }
    const jump=(name==='square')?2:(name==='sawtooth'?2:0);
    return {name,series,M,A,us,sm,id,pk,closed,ms,pks,Ns,errs,jump,odd:oddCount(M),
            rms:truncationRms(name,series,M), msTotal:idealMeanSquare(name),
            captured:0.5*A.reduce((s,a)=>s+a*a,0)};
  });
}

/* ---- the spectrum view -------------------------------------------- */
const SPEC_NS=256;                    /* samples of one period: a power of two for the FFT */
function specModel(st,amps){
  return memo('spec',[amps.join(','),st.series,st.N].join('|'),()=>{
    const y=sampleSeries(amps,st.series,SPEC_NS,st.N);
    const back=analyseFFT(y,NMAX,st.series);
    const direct=analyseDirect(y,NMAX,st.series);
    let dFFT=0,dDir=0;
    for(let n=0;n<NMAX;n++){
      const a=n<st.N?amps[n]:0;
      dFFT=Math.max(dFFT,Math.abs(back[n]-a));
      dDir=Math.max(dDir,Math.abs(back[n]-direct[n]));
    }
    const P=[]; let tot=0;
    for(let n=0;n<st.N;n++){ const p=0.5*amps[n]*amps[n]; P.push(p); tot+=p; }
    const cum=[]; let c=0;
    for(let n=0;n<P.length;n++){ c+=P[n]; cum.push(tot>0?c/tot:0); }
    return {y,back,direct,dFFT,dDir,P,cum,tot,
            msNum:meanSquareNumeric(amps,st.series,SPEC_NS,st.N),
            msPar:parseval(amps,st.N), rms:Math.sqrt(tot)};
  });
}

/* ---- the wave game ------------------------------------------------ */
function gameSeedOf(level,seed){ return seed*7919+level*104729; }
const GAME={level:1, seed:1, answer:new Array(NMAX).fill(0), score:0, tries:0, solved:false,
  reset(){ this.level=ST.level; this.seed=ST.seed; this.score=0; this.tries=0; this.solved=false;
           this.answer=gameAmplitudes(this.level,gameSeedOf(this.level,this.seed));
           setGuess(new Array(NMAX).fill(0)); ST.showAns=false; },
  fresh(){ this.seed++; ST.seed=this.seed; this.solved=false; ST.showAns=false;
           this.answer=gameAmplitudes(this.level,gameSeedOf(this.level,this.seed));
           setGuess(new Array(NMAX).fill(0)); },
  check(){ this.tries++;
           if(gameMatches(GUESS,this.answer)){ if(!this.solved) this.score++; this.solved=true; return true; }
           return false; },
  show(){ setGuess(this.answer.slice()); this.solved=true; ST.showAns=true; }
};

/* ---- the wave packet ---------------------------------------------- */
function wpModel(st){
  return memo('wp',[st.wpK0,st.wpSk,st.wpSp,st.wpDom].join('|'),()=>{
    const k1=WP_SPACINGS[st.wpSp], k0=st.wpK0, sk=st.wpSk, sx=1/sk;
    const comps=wpComponents(k1,k0,sk);
    const cont=k1===0;
    const [xa,xb]=[-2,2];                     /* PhET's default x window, m or ms */
    const ns=NPTS, xs=[], sum=[], env=[], cs=[];
    for(let j=0;j<=ns;j++){
      const x=xa+(xb-xa)*j/ns; xs.push(x);
      if(cont){ sum.push(wpContinuous(x,k0,sk,'cos')); env.push(wpEnvelopeContinuous(x,sk)); }
      else {                                  /* one pass: the cosine and sine sums give both */
        let sc=0,ss=0;
        for(let i=0;i<comps.length;i++){ const c=comps[i]; sc+=c.a*Math.cos(c.k*x); ss+=c.a*Math.sin(c.k*x); }
        sum.push(sc); env.push(Math.sqrt(sc*sc+ss*ss));
      }
      cs.push(wpContinuous(x,k0,sk,'cos'));
    }
    /* how far the drawn sum is from the exact continuous packet: over the whole
       drawn window (where a copy at a multiple of lambda1 shows up at full
       height) and inside one period (where only the Gaussian tail is left) */
    const lam1=k1>0?TAU/k1:Infinity;
    let dev=0, devP=0, copies=0;
    for(let j=0;j<=ns;j++){
      const d=Math.abs(sum[j]-cs[j]);
      dev=Math.max(dev,d);
      if(Math.abs(xs[j])<=Math.min(lam1/2,xb)) devP=Math.max(devP,d);
    }
    if(isFinite(lam1)) copies=2*Math.floor(xb/lam1);
    let amax=0; for(const c of comps) amax=Math.max(amax,c.a);
    let asum=0; for(const c of comps) asum+=c.a;
    const peakA=wpAmp(k0,k0,sk);
    return {k1,k0,sk,sx,comps,cont,xs,sum,env,cs,dev,devP,copies,amax,asum,
            n:wpComponentCount(k1), lam1,
            tail:wpTailBound(k0,sk), peakA, peakPlot:cont?peakA:peakA*k1,
            width:2*sx, kwidth:2*sk};
  });
}

/* ---- the transform pair ------------------------------------------- */
function pairModel(st){
  return memo('pair',[st.pairK1,st.wpK0,st.pairSk].join('|'),()=>{
    const k1=st.pairK1, k0=st.wpK0, sk=st.pairSk, sx=1/sk, lam1=TAU/k1;
    const comps=wpComponents(k1,k0,sk);
    const W=3, ns=900, xs=[], dis=[], con=[];
    for(let j=0;j<=ns;j++){ const x=-W+2*W*j/ns; xs.push(x);
      dis.push(wpDiscrete(x,comps,'cos')); con.push(wpContinuous(x,k0,sk,'cos')); }
    let devW=0, devP=0;
    for(let j=0;j<=ns;j++){
      const d=Math.abs(dis[j]-con[j]);
      devW=Math.max(devW,d);
      if(Math.abs(xs[j])<=Math.min(lam1/2,W)) devP=Math.max(devP,d);
    }
    /* the same measurement across the whole slider, for the error curve */
    const K1LO=PAIR_K1_MIN, K1HI=PAIR_K1_MAX, NK=28, NXE=161;
    const k1s=[], errW=[], errP=[];
    for(let i=0;i<=NK;i++){
      const kk=K1LO*Math.pow(K1HI/K1LO,i/NK);
      const cc=wpComponents(kk,k0,sk), lm=TAU/kk;
      let ew=0, ep=0;
      for(let j=0;j<=NXE;j++){
        const x=-W+2*W*j/NXE, d=Math.abs(wpDiscrete(x,cc,'cos')-wpContinuous(x,k0,sk,'cos'));
        ew=Math.max(ew,d);
        if(Math.abs(x)<=Math.min(lm/2,W)) ep=Math.max(ep,d);
      }
      k1s.push(kk); errW.push(ew); errP.push(ep);
    }
    /* the uncertainty hyperbola */
    const sks=[], sxs=[];
    for(let i=0;i<=120;i++){ const s=WP_SK_MIN+(WP_SK_MAX-WP_SK_MIN)*i/120; sks.push(s); sxs.push(1/s); }
    return {k1,k0,sk,sx,lam1,comps,W,xs,dis,con,devW,devP,k1s,errW,errP,sks,sxs,
            n:wpComponentCount(k1), tail:wpTailBound(k0,sk), prod:sk*sx};
  });
}

/* ---- the model ---------------------------------------------------- */
/* a SNAPSHOT of the state, so a readout rendered later cannot read
   whatever state ran last */
function buildModel(){
  const st=Object.assign({},ST), view=st.view, amps=ampsNow();
  const M={view,st,amps};
  if(view==='harm'){
    M.sum=curveSum(amps,st.series,st.domain,st.t,st.N,NPTS);
    M.harms=[]; for(let n=1;n<=st.N;n++) M.harms.push(curveHarmonic(amps,n,st.series,st.domain,st.t,NPTS));
    M.ideal=(st.showInf&&hasIdeal(st.preset))?curveIdeal(st.preset,st.series,st.domain,st.t,NPTS):null;
    M.yMax=yFit(M.sum.ys,1);
    M.par=parseval(amps,st.N);
    M.msNum=meanSquareNumeric(amps,st.series,512,st.N);
    M.nz=nonZeroCount(amps.slice(0,st.N));
    M.calW=caliperWidth(st.domain,st.sel);
    M.lamSel=LWAVE/st.sel; M.perSel=TPER/st.sel; M.fSel=F1*st.sel;
    M.kSel=K1*st.sel; M.wSel=W1*st.sel;
  }
  else if(view==='conv') M.C=convModel(st);
  else if(view==='spec') M.S=specModel(st,amps);
  else if(view==='game'){
    M.ans=GAME.answer.slice(); M.score=GAME.score; M.tries=GAME.tries; M.solved=GAME.solved;
    M.target=curveSum(M.ans,'sin','space',0,NMAX,NPTS);
    M.guess=curveSum(amps,'sin','space',0,NMAX,NPTS);
    M.yMax=yFit(M.target.ys.concat(M.guess.ys),1);
    M.nzAns=nonZeroCount(M.ans); M.nzGuess=nonZeroCount(amps);
    M.ctrl=GAME_CONTROLS[GAME.level-1];
    let e=0; for(let i=0;i<NMAX;i++) e=Math.max(e,Math.abs(amps[i]-M.ans[i]));
    M.worst=e; M.match=gameMatches(amps,M.ans);
    /* how far the guess is from the answer, as an rms over a period: Parseval
       again, on the DIFFERENCE of the two series */
    const d=[]; for(let i=0;i<NMAX;i++) d.push(amps[i]-M.ans[i]);
    M.rmsErr=Math.sqrt(parseval(d,NMAX));
  }
  else if(view==='pack') M.P=wpModel(st);
  else M.T=pairModel(st);
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function pct(x,n){ return sigf(100*x,n||3)+' %'; }
function presetName(id){ const p=PRESETS.find(o=>o.id===id); return p?p.name:id; }
function domName(id){ const d=DOMAINS.find(o=>o.id===id); return d?d.name:id; }

function harmonicRows(M){
  const st=M.st, n=st.sel;
  let s=hd('harmonic '+n+' of '+st.N);
  s+=rrow('amplitude A<sub>'+n+'</sub>',fmt(M.amps[n-1],2));
  if(st.domain==='time'){
    s+=rrow('period T<sub>'+n+'</sub> = T/'+n,sigf(M.perSel,4)+' ms')
      +rrow('frequency f<sub>'+n+'</sub> = '+n+'f<sub>1</sub>',sigf(M.fSel,4)+' Hz')
      +rrow('&omega;<sub>'+n+'</sub> = 2&pi;/T<sub>'+n+'</sub>',sigf(M.wSel,4)+' rad/ms');
  } else {
    s+=rrow('wavelength &lambda;<sub>'+n+'</sub> = L/'+n,sigf(M.lamSel,4)+' m')
      +rrow('k<sub>'+n+'</sub> = 2&pi;/&lambda;<sub>'+n+'</sub>',sigf(M.kSel,4)+' rad/m');
    if(st.domain==='both') s+=rrow('speed &lambda;<sub>n</sub>f<sub>n</sub> = L/T',sigf(LWAVE/TPER,3)+' m/ms');
  }
  return s;
}

function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">making waves<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='harm'){
    s+=hd('the series')+rrow('waveform',presetName(st.preset)+', '+(st.series==='sin'?'sines':'cosines'))
      +rrow('harmonics kept',st.N+' of '+NMAX+' ('+M.nz+' non-zero)')
      +rrow('function of',domName(st.domain))
      +(st.domain!=='space'?rrow('t',fmt(st.t,3)+' ms'+(st.running?' (running)':'')):'')
      +rrow('largest |F|',sigf(M.yMax,3)+' (axis)');
    s+=harmonicRows(M);
    s+=hd('Parseval')+rrow('&frac12; &Sigma; A<sub>n</sub>&sup2;',sigf(M.par,6),'good')
      +rrow('&lang;F&sup2;&rang; measured',sigf(M.msNum,6))
      +rrow('difference',M.par>0?sigf(Math.abs(M.par-M.msNum)/M.par,2):'0',Math.abs(M.par-M.msNum)<1e-12?'good':'bad')
      +rrow('rms of F',sigf(Math.sqrt(M.par),4));
    if(st.caliper) s+=hd('the caliper')+rrow(st.domain==='time'?'width = T/'+st.sel:'width = L/'+st.sel,sigf(M.calW,4)+' '+xUnits(st.domain))
      +rrow('left edge at',sigf(st.calX,3)+' '+xUnits(st.domain));
  }
  else if(M.view==='conv'){
    const C=M.C;
    s+=hd('the waveform')+rrow('converging to',presetName(C.name)+', '+(C.series==='sin'?'sines':'cosines'))
      +rrow('harmonics kept M',String(C.M)+(C.name==='square'||C.name==='triangle'?' ('+C.odd+' odd)':''))
      +rrow('&lang;f&sup2;&rang; complete',sigf(C.msTotal,6))
      +rrow('&frac12;&Sigma;A&sup2; captured',sigf(C.captured,6))
      +rrow('rms error, f less S<sub>M</sub>',sigf(C.rms,5),'good');
    s+=hd('the overshoot');
    if(C.jump>0){
      s+=rrow('peak of S<sub>M</sub> (measured)',sigf(C.pk.val,7))
        +(C.closed?rrow('&hellip; closed form',sigf(C.closed.val,7),Math.abs(C.pk.val-C.closed.val)<2e-7?'good':'bad'):'')
        +rrow('overshoot / jump',pct((C.pk.val-1)/C.jump,4))
        +rrow('limit M &rarr; &infin;',pct(GIBBS_FRACTION,5),'bad')
        +rrow('peak position u',sigf(C.pk.u,5)+' rad')
        +(C.closed?rrow('&hellip; = &pi;/2M<sub>odd</sub>',sigf(C.closed.u,5)+' rad'):'');
    } else s+=rrow('jump','none: the waveform is continuous')+rrow('max |S<sub>M</sub>|',sigf(C.pk.val,6),'good');
    s+='</table><div class="note">A truncated series rings at every jump, and the ears do not shrink: '
      +'they narrow. The overshoot tends to <b>'+sigf(100*GIBBS_FRACTION,6)+' %</b> of the jump &mdash; the '
      +'Wilbraham&ndash;Gibbs constant, (1/&pi;)Si(&pi;) &minus; &frac12;.</div>';
    return s+'';
  }
  else if(M.view==='spec'){
    const S=M.S;
    s+=hd('Parseval')+rrow('&frac12; &Sigma; A<sub>n</sub>&sup2;',sigf(S.msPar,8),'good')
      +rrow('&lang;F&sup2;&rang; from '+SPEC_NS+' samples',sigf(S.msNum,8))
      +rrow('difference',sigf(Math.abs(S.msPar-S.msNum),2),Math.abs(S.msPar-S.msNum)<1e-12?'good':'bad')
      +rrow('rms of F',sigf(S.rms,5));
    s+=hd('analysis &rarr; synthesis')+rrow('max |A<sub>n</sub> &minus; recovered|',sigf(S.dFFT,2),S.dFFT<1e-12?'good':'bad')
      +rrow('FFT &minus; direct DFT',sigf(S.dDir,2),S.dDir<1e-12?'good':'bad')
      +rrow('samples, radix-2',String(SPEC_NS));
    s+=hd('the power')+rrow('total &frac12;&Sigma;A&sup2;',sigf(S.tot,6))
      +rrow('largest single harmonic',S.tot>0?pct(Math.max.apply(null,S.P)/S.tot,3):'&mdash;')
      +rrow('harmonics for 99 %',String(S.cum.findIndex(c=>c>=0.99)+1||'&mdash;'));
  }
  else if(M.view==='game'){
    s+=hd('level '+GAME.level+' of '+N_LEVELS)
      +rrow('harmonics in the answer',String(M.nzAns)+(GAME.level===N_LEVELS?' (5 or more)':''))
      +rrow('amplitude controls',String(M.ctrl))
      +rrow('non-zero in your guess',String(M.nzGuess))
      +rrow('score',String(M.score)+' of '+M.tries+' tries');
    s+=hd('how close')+rrow('worst |guess &minus; answer|',sigf(M.worst,3),M.match?'good':'bad')
      +rrow('rms difference',sigf(M.rmsErr,4),M.match?'good':'')
      +rrow('matched',M.match?'yes &mdash; exactly':'not yet',M.match?'good':'bad');
    s+='</table><div class="note">PhET counts a guess right only when <b>every</b> amplitude matches exactly, '
      +'so the rms difference is a guide, not the test. Amplitudes here move in steps of '+fmt(G_STEP,1)+', as in PhET.</div>';
    return s;
  }
  else if(M.view==='pack'){
    const P=M.P, sp=P.k1>0?'k<sub>1</sub>':'continuous';
    const ku=st.wpDom==='time'?'rad/ms':'rad/m', xu=st.wpDom==='time'?'ms':'m';
    s+=hd('the packet')+rrow('centre k<sub>0</sub>',sigf(P.k0,4)+' '+ku)
      +rrow('&hellip; in units of &pi;',sigf(P.k0/PI,4)+' &pi;')
      +rrow('width &sigma;<sub>k</sub>',sigf(P.sk,4)+' '+ku)
      +rrow('&sigma;<sub>x</sub> = 1/&sigma;<sub>k</sub>',sigf(P.sx,4)+' '+xu,'good')
      +rrow('&sigma;<sub>x</sub>&sigma;<sub>k</sub>',fmt(P.sx*P.sk,12),'good');
    s+=hd('the components')+rrow('spacing',P.k1>0?sigf(P.k1,4)+' '+ku:'0 (continuous)')
      +rrow('how many',P.cont?'&infin;':String(P.n))
      +rrow('&lambda;<sub>1</sub> = 2&pi;/k<sub>1</sub>',P.cont?'&infin;':sigf(P.lam1,4)+' '+xu)
      +rrow('tallest A(k<sub>n</sub>)k<sub>1</sub>',P.cont?'&mdash;':sigf(P.amax,4))
      +rrow('&Sigma; A(k<sub>n</sub>)k<sub>1</sub>',P.cont?'1 (exactly)':sigf(P.asum,6),Math.abs(P.asum-1)<2e-4||P.cont?'good':'bad');
    s+=hd('against the exact packet')+rrow('copies inside the window',P.cont?'none':String(P.copies))
      +rrow('max difference, whole window',sigf(P.dev,2),P.copies>0?'bad':'good')
      +rrow('&hellip; inside one period',sigf(P.devP,2),P.devP<=P.tail*1.05?'good':'bad')
      +rrow('Gaussian tail bound',sigf(P.tail,2))
      +rrow('envelope width at 1/&radic;e',sigf(P.width,4)+' '+xu);
  }
  else {
    const T=M.T;
    s+=hd('the pair')+rrow('centre k<sub>0</sub>',sigf(T.k0,4)+' rad/m')
      +rrow('&sigma;<sub>k</sub>',sigf(T.sk,4)+' rad/m')+rrow('&sigma;<sub>x</sub> = 1/&sigma;<sub>k</sub>',sigf(T.sx,4)+' m')
      +rrow('product',fmt(T.prod,12),Math.abs(T.prod-1)<1e-12?'good':'bad');
    s+=hd('the spacing')+rrow('k<sub>1</sub>',sigf(T.k1,4)+' rad/m')
      +rrow('&lambda;<sub>1</sub> = 2&pi;/k<sub>1</sub>',sigf(T.lam1,4)+' m')
      +rrow('components below 24&pi;',String(T.n))
      +rrow('copies inside &plusmn;3 m',String(2*Math.floor(3/T.lam1)));
    s+=hd('discrete vs continuous')+rrow('max |diff| on &plusmn;3 m',sigf(T.devW,3),T.devW<1e-3?'good':'bad')
      +rrow('&hellip; inside one period',sigf(T.devP,2),T.devP<=T.tail*1.05?'good':'bad')
      +rrow('Gaussian tail bound',sigf(T.tail,2));
    s+='</table><div class="note">By Poisson summation the discrete sum is <b>exactly</b> the continuous '
      +'packet repeated every &lambda;<sub>1</sub>. Narrow the spacing and the copies walk off to infinity; '
      +'what is left inside one period is only the Gaussian tail below k = 0 and above 24&pi;.</div>';
    return s;
  }
  s+='</table><div class="note">PhET&rsquo;s values (11 harmonics, amplitudes to &plusmn;1.5 in steps of '
    +fmt(A_STEP,2)+', f<sub>1</sub> = 440 Hz, L = 1 m, T = 1000/440 ms) are read out of its build 1.1.5. '
    +'Everything else is exact and pinned in selfTest to build/fourier-making-waves/derive.py.</div>';
  return s;
}

function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const st=M.st;
  if(M.view==='harm'){
    const tr=st.series==='sin'?'sin':'cos';
    const arg=st.domain==='time'?'2&pi;n t/T':(st.domain==='both'?'2&pi;n (x/L &minus; t/T)':'2&pi;n x/L');
    return E('<span class="hl">F = &Sigma;<sub>n=1</sub><sup>'+st.N+'</sup> A<sub>n</sub> '+tr+'('+arg+')</span>'
      +' &nbsp;&middot;&nbsp; &lambda;<sub>n</sub> = L/n, &nbsp; T<sub>n</sub> = T/n, &nbsp; f<sub>n</sub> = n f<sub>1</sub>',
      'eleven sines (or cosines) whose wavelengths are L, L/2, L/3 &hellip; ; set their amplitudes and this is their sum');
  }
  if(M.view==='conv') return E('<span class="hl">max S<sub>M</sub> &minus; 1 &rarr; (1/&pi;)Si(&pi;) &minus; &frac12; = 0.0894899</span>'
    +' &nbsp;&times; the jump &nbsp;&middot;&nbsp; at u = &pi;/2M',
    'the ringing at a jump does not die away as more terms are added &mdash; it narrows, and keeps the same height');
  if(M.view==='spec') return E('<span class="hl">&lang;F&sup2;&rang; = &frac12; &Sigma;<sub>n</sub> A<sub>n</sub>&sup2;</span>'
    +' &nbsp;&middot;&nbsp; A<sub>n</sub> = (2/N<sub>s</sub>) &Sigma;<sub>j</sub> F(u<sub>j</sub>) sin(n u<sub>j</sub>)',
    'Parseval: the power in the waveform is the power in its harmonics, added up &mdash; and the amplitudes come back out of the waveform');
  if(M.view==='game') return E('<span class="hl">F(x) = &Sigma;<sub>n=1</sub><sup>11</sup> A<sub>n</sub> sin(2&pi;n x/L)</span>'
    +' &nbsp;&middot;&nbsp; <span class="rm">find the A<sub>n</sub></span>',
    'the magenta curve is somebody else&rsquo;s amplitudes; a guess counts only when every one of the eleven matches exactly');
  if(M.view==='pack') return E('<span class="hl">F(x) = &Sigma;<sub>n</sub> A(k<sub>n</sub>) k<sub>1</sub> cos(k<sub>n</sub>x)</span>'
    +' &nbsp;&middot;&nbsp; A(k) = e<sup>&minus;(k&minus;k<sub>0</sub>)&sup2;/2&sigma;<sub>k</sub>&sup2;</sup> / &sigma;<sub>k</sub>&radic;(2&pi;)',
    'a bundle of cosines whose wave numbers are spread about k&#8320; &mdash; the narrower the spread, the longer the packet');
  return E('<span class="hl">&#8747; A(k) cos(kx) dk = e<sup>&minus;&sigma;<sub>k</sub>&sup2;x&sup2;/2</sup> cos(k<sub>0</sub>x)</span>'
    +' &nbsp;&middot;&nbsp; <span class="hl2">&sigma;<sub>x</sub>&sigma;<sub>k</sub> = 1</span>',
    'a Gaussian in k is a Gaussian in x, and the two widths are exactly reciprocal: you cannot narrow both');
}

function tagHTML(M){
  const st=M.st;
  if(M.view==='harm') return '<b>the harmonics</b> &mdash; '+presetName(st.preset)+', '+(st.series==='sin'?'sines':'cosines')
    +', '+st.N+' term'+(st.N===1?'':'s')+', '+domName(st.domain)+(st.running&&st.domain==='both'?', running':'');
  if(M.view==='conv') return '<b>the convergence</b> &mdash; '+presetName(M.C.name)+', '+M.C.M+' term'+(M.C.M===1?'':'s');
  if(M.view==='spec') return '<b>the spectrum</b> &mdash; '+presetName(st.preset)+', '+st.N+' harmonics, Parseval both ways';
  if(M.view==='game') return '<b>the wave game</b> &mdash; level '+GAME.level+', '+M.nzAns+' harmonics to find'
    +(M.match?' &mdash; matched':'');
  if(M.view==='pack') return '<b>the wave packet</b> &mdash; '+(M.P.cont?'continuous':M.P.n+' components, spacing '+sigf(M.P.k1,3))
    +', &sigma;<sub>k</sub> = '+sigf(M.P.sk,3);
  return '<b>the transform pair</b> &mdash; k<sub>1</sub> = '+sigf(M.T.k1,3)+' rad/m, &lambda;<sub>1</sub> = '+sigf(M.T.lam1,3)+' m';
}
