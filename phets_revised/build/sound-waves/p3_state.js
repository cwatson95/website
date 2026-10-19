
/* ================================================================== *
 *  state: the one lattice run every view shares, its clock, the       *
 *  per-view model, the readout, the equation bar and the tag          *
 * ================================================================== */
const TABS=[['intro','the speaker'],['measure','the bench'],['two','two speakers'],
            ['wall','the wall'],['air','thin air'],['law','wavelength and speed']];
/* which of PhET's five screens each view is */
const SCREEN_OF={intro:'Intro', measure:'Measure', two:'Two Sources', wall:'Reflection', air:'Air Pressure', law:''};
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c', body:'#6b7285',
           air0:'#05070c', air1:'#eef1f7', wall:'#8a94ab'};
const RO_W=300;
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it
   (build/wave-on-a-string/, Known-bad list) */
const HINT_H=18;
const FRAME_DT=1/60;
const DEG=PI/180;
const LOOK_LIST=[{id:'waves',name:'pressure'},{id:'particles',name:'air parcels'},{id:'both',name:'both'}];
const MODE_LIST=[{id:'cont',name:'continuous'},{id:'pulse',name:'pulse'}];
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'slow',name:'slow'}];
const TONE_LIST=[{id:'speaker',name:'at the speaker'},{id:'listener',name:'at the listener'}];
/* the frequencies the analysis view measures, plus whatever the slider is on */
const LAW_FS=[100,325,550,775,1000];

const DEFAULTS={view:'intro', f:AIR.f0, amp:AIR.amp0, wave:'cont', pressure:1,
  wallX:WALLR.x0, wallAng:WALLR.a0, spk2y:2*AIR.W/3,
  look:'waves', graph:false, ruler:false, watch:false, listener:true,
  nodes:true, image:true, tone:false, toneMode:'speaker',
  speed:'normal', running:true};
const ST=Object.assign({},DEFAULTS);
/* the tools, in metres (model coordinates), so they survive a change of view */
const TOOLS={ruler:[1.2,8.6], listener:[5.0,5.0]};
const TOOLS0=JSON.parse(JSON.stringify(TOOLS));
const DRAG={what:null};
const RULER_LEN=5;                      /* PhET's ruler is 5 m long */

/* ---- the run, its probe and its clock ----------------------------------- */
const RUN=makeRun(AIR.f0);
const PROBE=makeProbe(64);
const CLOCK={acc:0, steps:0, watch:0, watchOn:false};

function viewMode(v){ return v==='two'?'two':(v==='wall'?'wall':'one'); }
function speakerYs(){ return ST.view==='two'?[AIR.W/3,ST.spk2y]:[AIR.W/2]; }
function speakerRows(){ return speakerYs().map(y=>rowOfY(RUN,y)); }
function curWall(){ return wallGeom(ST.wallX,ST.wallAng); }
/* bring the run in line with the panel */
function syncRun(){
  if(RUN.f!==ST.f) runSetFrequency(RUN,ST.f);
  RUN.A=ST.amp;
  RUN.pressure=(ST.view==='air')?ST.pressure:1;
  setWaveMode(RUN,ST.wave==='cont');
  probeResize(PROBE,Math.max(8,Math.round(TAU/RUN.Om)));
  return RUN;
}
function stepsPerSecond(){ return AIR.phetTimeScale/RUN.dt*(ST.speed==='slow'?0.5:1); }
/* one lattice step, then the listener's ring buffer gets the composed field.  The
   buffer is emptied whenever the composition changes, so a view never reports an
   amplitude that is partly another view's picture. */
function stepOnce(){
  runStep(RUN);
  const rows=speakerRows(), G=curWall(), mode=viewMode(ST.view);
  if(PROBE.mode!==mode){ PROBE.mode=mode; PROBE.head=0; PROBE.count=0; }
  probePush(PROBE,fieldAtModel(RUN,mode,rows,G,TOOLS.listener[0],TOOLS.listener[1]));
  if(CLOCK.watchOn) CLOCK.watch+=RUN.dt;
  CLOCK.steps++;
}
/* one frame of wall time, deterministic (FRAME_DT) so the headless suites repeat */
function clockFrame(){
  if(!ST.running) return 0;
  syncRun();
  CLOCK.acc+=FRAME_DT;
  const per=1/stepsPerSecond();
  let n=0;
  while(CLOCK.acc>=per&&n<3){ stepOnce(); CLOCK.acc-=per; n++; }
  if(n===3) CLOCK.acc=0;
  return n;
}
function runFor(steps){ syncRun(); for(let k=0;k<steps;k++) stepOnce(); return RUN; }
function resetAll(){
  const v=ST.view;
  Object.assign(ST,DEFAULTS); ST.view=v;
  TOOLS.ruler=TOOLS0.ruler.slice(); TOOLS.listener=TOOLS0.listener.slice();
  RUN.A=DEFAULTS.amp; RUN.pressure=1; RUN.cont=true; RUN.on=true; RUN.srcOff=LAT.SRC_OFF;
  runSetFrequency(RUN,DEFAULTS.f); runClear(RUN);
  probeResize(PROBE,Math.max(8,Math.round(TAU/RUN.Om))); PROBE.head=0; PROBE.count=0;
  CLOCK.acc=0; CLOCK.steps=0; CLOCK.watch=0; CLOCK.watchOn=false;
}

/* ---- the models ---------------------------------------------------------- */
function baseModel(){
  const R=syncRun(), mode=viewMode(ST.view), rows=speakerRows(), G=curWall();
  const M={view:ST.view, R, mode, rows, G, screen:SCREEN_OF[ST.view],
           lam:waveLen(R.f), T:1/R.f, Nl:R.Nl, dt:R.dt, dx:sceneDx(),
           phetErr:phetLambda(R.f)/waveLen(R.f)-1, steps:R.n, t:R.t,
           active:sourceActive(R), pulsing:R.pulse.on,
           speakers:speakerYs().map((y,i)=>[xOfCell(R,srcCol(R)),yOfRow(R,rows[i])]),
           sps:stepsPerSecond(), watch:CLOCK.watch, watchOn:CLOCK.watchOn};
  M.g=fieldGrid(R,mode,rows,G);
  M.parcels=(ST.look!=='waves')?parcelPositions(R,M.g):null;
  /* the listener: the composed field there now, and its amplitude over one period */
  const lx=TOOLS.listener[0], ly=TOOLS.listener[1];
  const L={x:lx, y:ly, u:fieldAtModel(R,mode,rows,G,lx,ly), amp:probeAmp(PROBE),
           r:M.speakers.map(s=>Math.hypot(lx-s[0],ly-s[1]))};
  L.dr=L.r.length>1?L.r[0]-L.r[1]:0;
  L.dPhase=TAU*L.dr/M.lam;
  L.inFront=(mode!=='wall')||wallSide(G,lx,ly)<0;
  M.listener=L;
  M.tone={hz:R.f, level:toneLevel(ST.toneMode,R.A,L.amp), on:false};
  if(ST.ruler) M.ruler={x0:TOOLS.ruler[0], y:TOOLS.ruler[1], len:RULER_LEN,
                        lamPerM:M.lam, ticks:Math.round(RULER_LEN/M.lam*100)/100};
  if(mode==='two'){
    const d=Math.abs(M.speakers[0][1]-M.speakers[1][1]);
    M.two={d, dOverLam:d/M.lam, orders:nodeOrders(d,M.lam),
           ym:0.5*(M.speakers[0][1]+M.speakers[1][1]), xs:M.speakers[0][0]};
    M.two.far=M.two.orders.map(m=>nodeFarAngle(m,M.lam,d));
  }
  if(mode==='wall'){
    const s=M.speakers[0], im=wallMirror(G,s[0],s[1]);
    const lp=(L.inFront)?wallBounce(G,s[0],s[1],lx,ly):null;
    const W2={image:im, dSS:Math.hypot(im[0]-s[0],im[1]-s[1]), bounce:lp,
              foot:wallFoot(G,s[0],s[1]), dist:Math.abs(wallSide(G,s[0],s[1])),
              angDeg:ST.wallAng/DEG, front:M.g.nfront/(LAT.VIS*LAT.VIS)};
    if(lp){
      W2.aIn=angleToNormal(G,lp[0]-s[0],lp[1]-s[1]);
      W2.aOut=angleToNormal(G,lx-lp[0],ly-lp[1]);
      W2.direct=Math.hypot(lx-s[0],ly-s[1]);
      W2.path=Math.hypot(lp[0]-s[0],lp[1]-s[1])+Math.hypot(lx-lp[0],ly-lp[1]);
      W2.image_r=Math.hypot(lx-im[0],ly-im[1]);
      W2.dr=W2.path-W2.direct;
      W2.dOverLam=W2.dr/M.lam;
    }
    M.wall=W2;
  }
  if(ST.view==='air'){
    const p=ST.pressure;
    M.air={frac:p, rho:airDensity(p), rho0:airDensity(1), v:soundSpeedIdeal(GAS.T0),
           db:dbOf(p), mfp:meanFreePath(Math.max(p,1e-12)), Kn:knudsen(Math.max(p,1e-12),R.f),
           T:GAS.T0, TforV:tempForSpeed(AIR.v)};
  }
  return M;
}
/* the analysis view measures the lattice, which costs a few hundred lattice
   steps per frequency: at most ONE uncached frequency is measured per model, so
   the view fills in over a second or two instead of freezing */
function lawModel(){
  const want=LAW_FS.slice();
  if(want.indexOf(ST.f)<0) want.push(ST.f);
  const rows=[]; let pending=0, did=false;
  for(const f of want){
    const key=f.toFixed(6);
    let hit=null;
    for(const e of MEAS_CACHE) if(e.key===key) hit=e.val;
    if(!hit&&!did){ hit=measureWave(f); did=true; }
    if(!hit){ pending++; rows.push({f, m:null}); continue; }
    rows.push({f, m:hit});
  }
  return {rows, pending, live:ST.f};
}
/* the lattice's own dispersion, as a curve over the slider: phase speed, group
   speed and the wavelength along the diagonal against the one along the axis */
function dispRows(){
  const out=[];
  for(let q=0;q<=40;q++){
    const f=AIR.fmin+(AIR.fmax-AIR.fmin)*q/40, Nl=cellsPerWave(f), Om=omegaStep(Nl);
    const ka=latK(Om,0), kd=latK(Om,PI/4);
    out.push({f, Nl, vp:latPhaseSpeed(ka,0)/LAT.C, vg:latGroupSpeed(ka,0)/LAT.C,
              aniso:(TAU/kd)/(TAU/ka)-1, phet:phetLambda(f)/waveLen(f)-1});
  }
  return out;
}
function buildModel(){
  const M=baseModel();
  if(ST.view==='law'){ M.X=lawModel(); M.disp=dispRows(); }
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function lenM(x){ return sigf(x,3)+' m'; }
function msU(x){ return sigf(x*1000,3)+' ms'; }
function pct(x,n){ return (x>=0?'+':'&minus;')+sigf(Math.abs(100*x),n||2)+' %'; }
function degU(a){ return sigf(a/DEG,3)+'&deg;'; }
function sourceWord(M){
  if(ST.wave==='pulse') return M.pulsing?'firing a pulse':'armed &mdash; press to fire';
  return M.active?'on':'off';
}
function readoutHTML(M){
  let s='<div class="rname">sound waves<small>'+TABS.find(t=>t[0]===M.view)[1]
    +(M.screen?' &middot; PhET&rsquo;s '+M.screen:'')+'</small></div><table>';
  s+=hd('the speaker')
    +rrow('frequency f',sigf(M.R.f,4)+' Hz')
    +rrow('wavelength &lambda; = v/f',lenM(M.lam),'good')
    +rrow('speed of sound v',sigf(AIR.v,4)+' m/s')
    +rrow('period T = 1/f',msU(M.T))
    +rrow('amplitude',fmt(M.R.A,1)+' ('+(ST.wave==='cont'?'continuous':'pulse')+')')
    +rrow('the source',sourceWord(M),M.active?'good':'bad');
  s+=hd('on the lattice')
    +rrow('cells per wavelength',sigf(M.Nl,4))
    +rrow('time per step, solved',sigf(M.dt*1e6,4)+' &micro;s')
    +rrow('PhET&rsquo;s one step: &lambda; off by',pct(M.phetErr),'bad')
    +rrow('steps, time',M.steps+', '+msU(M.t));
  if(M.view==='two'&&M.two) s+=hd('two speakers')
    +rrow('separation d',lenM(M.two.d))
    +rrow('d / &lambda;',sigf(M.two.dOverLam,4))
    +rrow('quiet lines each side',M.two.orders.length)
    +rrow('first one at',M.two.far.length?degU(M.two.far[0]):'&mdash;');
  if(M.view==='wall'&&M.wall) s+=hd('the wall')
    +rrow('position, angle',lenM(ST.wallX)+', '+degU(ST.wallAng))
    +rrow('the speaker&rsquo;s image at',lenM(M.wall.image[0])+', '+lenM(M.wall.image[1]),'good')
    +rrow('speaker to its image',lenM(M.wall.dSS))
    +rrow('in front of the wall',sigf(100*M.wall.front,3)+' % of the box')
    +(M.wall.bounce?rrow('incidence, reflection',degU(M.wall.aIn)+', '+degU(M.wall.aOut),'good'):'')
    +(M.wall.bounce?rrow('extra path, &Delta;/&lambda;',lenM(M.wall.dr)+', '+sigf(M.wall.dOverLam,3)):'');
  if(M.view==='air'&&M.air) s+=hd('the air in the box')
    +rrow('density',sigf(M.air.frac,3)+' atm = '+sigf(M.air.rho,3)+' kg/m&sup3;')
    +rrow('sound speed &radic;(&gamma;RT/M)',sigf(M.air.v,5)+' m/s','good')
    +rrow('loudness against full air',(M.air.frac>0?sigf(M.air.db,3)+' dB':'silent'),M.air.frac>0?'':'bad')
    +rrow('mean free path',M.air.frac>0?sigf(M.air.mfp,3)+' m':'&infin;')
    +rrow('mean free path / &lambda;',M.air.frac>0?sciHTML(M.air.Kn,3):'&infin;');
  if(ST.listener){
    const L=M.listener;
    s+=hd('the listener')
      +rrow('at',lenM(L.x)+', '+lenM(L.y))
      +rrow('pressure now',sigf(L.u,3))
      +rrow('amplitude over one period',sigf(L.amp,3),L.amp>0.05?'good':'')
      +(M.mode==='two'?rrow('r&#8321; &minus; r&#8322;, &Delta;/&lambda;',lenM(L.dr)+', '+sigf(L.dr/M.lam,3)):'')
      +(M.mode==='wall'&&!L.inFront?rrow('behind the wall','no sound','bad'):'');
  }
  if(ST.ruler||ST.watch) s+=hd('the tools')
    +(ST.ruler?rrow('ruler, wavelengths on it',sigf(RULER_LEN,2)+' m, '+sigf(RULER_LEN/M.lam,3)):'')
    +(ST.watch?rrow('stopwatch',msU(CLOCK.watch)+(CLOCK.watchOn?' running':'')):'');
  if(M.view==='law'&&M.X){
    const done=M.X.rows.filter(r=>r.m);
    s+=hd('measured on the lattice');
    for(const r of done.slice(0,6))
      s+=rrow(sigf(r.f,4)+' Hz &lambda;',sigf(r.m.lam,5)+' m ('+pct(r.m.err,2)+')',
              Math.abs(r.m.err)<0.005?'good':'bad');
    if(M.X.pending) s+=rrow('still measuring',M.X.pending+' more');
  }
  s+='</table><div class="note">'+roNote(M)+'</div>';
  return s;
}
function roNote(M){
  const v=M.view;
  if(v==='intro') return 'One cell of a 231 &times; 231 lattice is driven up and down; every other cell accelerates toward the average of its four neighbours. The colour is the pressure &mdash; white is a compression, black a rarefaction &mdash; and &plusmn;2 in lattice units is full contrast (PhET&rsquo;s scale).';
  if(v==='measure') return 'Measure &lambda; with the ruler, crest to crest, and T with the stopwatch on the listener&rsquo;s trace. Their product is the speed of sound, and it is the same number at every frequency because the speed belongs to the air.';
  if(v==='two') return 'Both speakers are the SAME lattice field read at two different rows, which is exactly PhET&rsquo;s trick and is exact because the equation is linear. The quiet lines are hyperbolae with the speakers as foci.';
  if(v==='wall') return 'The wall is an image source: the field behind a rigid wall is the mirror of the field in front of it, so the reflected wave is the wave of a second speaker at the speaker&rsquo;s mirror image. Nothing is drawn behind the wall.';
  if(v==='air') return 'Removing the air scales the source with the density. The SPEED does not move: c = &radic;(&gamma;p/&rho;) and p and &rho; fall together at fixed temperature. What falls is the loudness, 20 log&#8321;&#8320;(&rho;/&rho;&#8320;) decibels.';
  return 'The wavelength on each row is measured on the lattice itself &mdash; a least-squares fit against the drive&rsquo;s own phase at every cell of the axis, then the slope of the phase &mdash; not computed from v/f.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='intro') return E('&part;&sup2;p/&part;t&sup2; = v&sup2;&nabla;&sup2;p &nbsp;&rArr;&nbsp; <span class="hl">&lambda; = v/f</span>, &nbsp; v = 343 m/s',
    'the air sets the speed, so a higher note can only mean a shorter wave &mdash; the crests crowd together as you raise the frequency');
  if(v==='measure') return E('<span class="hl">v = f&lambda;</span> &nbsp;&middot;&nbsp; T = 1/f',
    'lay the ruler across the crests to read &lambda;, time one swing of the listener&rsquo;s trace to read T, and multiply: 343 m/s at every setting');
  if(v==='two') return E('|r&#8321; &minus; r&#8322;| = <span class="hl">(m + &frac12;)&lambda;</span> &nbsp;&rArr;&nbsp; quiet &nbsp;&middot;&nbsp; d sin&theta; = (m + &frac12;)&lambda;',
    'the quiet places are where the two paths differ by half a wavelength, an odd number of times &mdash; hyperbolae with the speakers as foci');
  if(v==='wall') return E('<span class="hl">&theta;<sub>in</sub> = &theta;<sub>out</sub></span> &nbsp;&hArr;&nbsp; p(P) = p(P) + p(P&prime;), &nbsp; &part;p/&part;n = 0 on the wall',
    'a rigid wall is a mirror: reflect the speaker in it and the reflected sound is the sound of that image, which is why the two angles are equal');
  if(v==='air') return E('<span class="hl">c = &radic;(&gamma;p/&rho;) = &radic;(&gamma;RT/M)</span> &nbsp;&middot;&nbsp; p<sub>amp</sub> &prop; &rho;',
    'take the air away and the sound gets quieter, not slower: pressure and density fall together, and their ratio is what sets the speed');
  return E('<span class="hl">&lambda; = v/f</span> &nbsp;&rArr;&nbsp; log &lambda; = log v &minus; log f',
    'one law across the slider: on log scales a fixed speed is a straight line of slope &minus;1, and the green dots are the lattice measured, not the formula');
}
function tagHTML(M){
  return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b> &mdash; '+sigf(M.R.f,4)+' Hz, &lambda; = '+lenM(M.lam)
    +', amplitude '+fmt(M.R.A,1)+(M.active?'':', source off')+(ST.running?'':', paused')
    +(M.view==='air'&&ST.pressure<1?', air '+sigf(ST.pressure,2)+' atm':'');
}
/* scientific notation the canvas can draw and the readout can set */
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴',
            '5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function supTxt(n){ return String(n).split('').map(c=>SUPS[c]||'').join(''); }
function sciParts(x,n){
  const e=Math.floor(Math.log10(Math.abs(x)));
  return [sigf(x/Math.pow(10,e),n||4),e];
}
function sciTxt(x,n){
  if(x===0) return '0';
  if(!isFinite(x)) return '∞';
  if(Math.abs(x)>=1e-3&&Math.abs(x)<1e5) return sigf(x,n||4);
  const p=sciParts(x,n); return p[0]+'×10'+supTxt(p[1]);
}
function sciHTML(x,n){
  if(x===0) return '0';
  if(!isFinite(x)) return '&infin;';
  if(Math.abs(x)>=1e-3&&Math.abs(x)<1e5) return sigf(x,n||4);
  const p=sciParts(x,n); return p[0]+'&times;10<sup>'+p[1]+'</sup>';
}
function pow10(e){ return '10'+supTxt(Math.round(e)); }
