
/* ================================================================== *
 *  state: one lattice run per medium (PhET gives each screen its own  *
 *  model), their clock, the per-view model, the readout, the equation *
 *  bar and the tag                                                    *
 * ================================================================== */
const TABS=[['water','water'],['sound','sound'],['light','light'],['media','the three media']];
const MEDIA={water:1, sound:1, light:1};
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c', water0:'#062848', water1:'#bfe8ff', body:'#6b7285'};
const RO_W=300;
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it
   (build/wave-on-a-string/, Known-bad list) */
const HINT_H=18;
/* PhET's MAX_AMPLITUDE_TO_PLOT_ON_RIGHT: the lattice value that maps to full
   colour and to the top of the graph */
const U_FULL=2.14;
const FRAME_DT=1/60;
const DEG=PI/180;
/* each medium's units in SI: water cm and s, sound cm and ms, light nm and fs */
const SI_LEN={water:1e-2, sound:1e-2, light:1e-9};
const SI_TIME={water:1, sound:1e-3, light:1e-15};
const SIDE_LIST=[{id:'top',name:'top view'},{id:'side',name:'side view'}];
const SOUNDVIEW_LIST=[{id:'waves',name:'waves'},{id:'particles',name:'particles'},{id:'both',name:'both'}];
const WAVE_LIST=[{id:'cont',name:'continuous'},{id:'pulse',name:'pulse'}];
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'slow',name:'slow'}];
/* PhET's graph titles and axis labels, one per scene */
const GRAPH_TITLE={water:'water level at centre', sound:'pressure at centre', light:'electric field at centre'};

const DEFAULTS={view:'water',
  f_water:sceneF0(SCENES.water), f_sound:sceneF0(SCENES.sound), f_light:sceneF0(SCENES.light),
  amp_water:8, amp_sound:8, amp_light:8,
  wave:'cont', look:'top', soundView:'waves', tone:false,
  screen:true, inten:false, graph:false, tape:false, watch:false, meter:false,
  speed:'normal', running:true};
const ST=Object.assign({},DEFAULTS);
/* the tools, in fractions of the tank's width, so they survive a change of view */
const TOOLS={tape:[[0.25,0.86],[0.55,0.86]], probes:[[0.45,0.5],[0.7,0.5]]};
const TOOLS0=JSON.parse(JSON.stringify(TOOLS));
const DRAG={what:null};

/* ---- the three runs and their clock ------------------------------------- */
const RUNS={water:makeRun('water','point',1), sound:makeRun('sound','point',1), light:makeRun('light','point',1)};
const CLOCK={acc:0, steps:0};
/* bring one run in line with the panel: frequency (water and sound keep their
   waves, light clears — PhET's LightScene.handlePhaseChanged), amplitude, the
   disturbance type, the probes */
function syncRun(v){
  const R=RUNS[v];
  if(!R) return null;
  const f=ST['f_'+v];
  if(R.f!==f) runSetFrequency(R,f);
  R.A=ST['amp_'+v];
  runSetWave(R,ST.wave==='cont');
  const S=SCENES[v];
  R.probes=ST.meter?TOOLS.probes.map(p=>[p[0]*S.W,p[1]*S.W]):[];
  return R;
}
function curRun(){ return MEDIA[ST.view]?syncRun(ST.view):null; }
function stepsPerSecond(){ return LAT.EVENT_RATE*(ST.speed==='slow'?0.5:1); }
/* one frame of wall time: PhET's event timer, deterministic (FRAME_DT) */
function clockFrame(){
  const R=curRun();
  if(!R||!ST.running) return 0;
  CLOCK.acc+=FRAME_DT;
  const per=1/stepsPerSecond();
  let n=0;
  while(CLOCK.acc>=per&&n<3){ runStep(R); CLOCK.acc-=per; n++; CLOCK.steps++; }
  if(n===3) CLOCK.acc=0;
  return n;
}
function runFor(v,steps){ const R=syncRun(v); for(let k=0;k<steps;k++) runStep(R); return R; }
function resetRuns(){
  for(const v of SCENE_IDS){
    const R=RUNS[v];
    runSetScene(R,v);
    R.A=DEFAULTS['amp_'+v]; R.cont=true; R.src[0]=true; R.src[1]=true;
    R.pulse.on=false; R.pulse.phi=0; R.watch.on=false; R.watch.t=0; R.probes=[]; R.trace=[];
  }
  CLOCK.acc=0; CLOCK.steps=0;
}
/* PhET's enableControlProperties for the tone: the box, the button and the clock */
function toneOn(){ return ST.view==='sound'&&ST.tone&&ST.running&&sourceActive(RUNS.sound); }

/* ---- the models ---------------------------------------------------------- */
function mediumModel(v){
  const R=syncRun(v), S=SCENES[v], dx=sceneDx(S), lam=waveLen(S,R.f);
  const M={R,S,dx,lam,Nl:R.Nl,Om:R.Om,dt:R.dt,T:1/R.f,phetErr:phetLambda(S,R.f)/lam-1,
           steps:R.n,t:R.t,watch:R.watch,active:sourceActive(R),
           mode:R.cont?'continuous':'pulse'};
  if(v==='light'&&(ST.screen||ST.inten)){
    M.I=screenIntensity(R);
    M.Imax=M.I.reduce((a,b)=>Math.max(a,b),0);
    M.bright=screenBright(M.I);
    M.brightMid=M.bright[(M.bright.length-1)/2|0];
    M.brightEnd=M.bright[0];
    if(ST.inten) M.th=screenTheory1(R);
  }
  if(ST.tape){ const a=TOOLS.tape[0], b=TOOLS.tape[1]; M.tapeLen=Math.hypot(b[0]-a[0],b[1]-a[1])*S.W; }
  if(ST.meter) M.probes=TOOLS.probes.map(p=>probeValue(R,p[0]*S.W,p[1]*S.W));
  if(v==='sound') M.tone=Object.assign(toneParams(R),{on:toneOn()});
  return M;
}
function mediaModel(){
  const rows=[];
  for(const id of SCENE_IDS){
    const S=SCENES[id], f=ST['f_'+id];
    rows.push({id, S, f, lam:waveLen(S,f), Nl:cellsPerWave(S,f), dx:sceneDx(S), dt:stepDt(S,f),
               vSI:S.v*SI_LEN[id]/SI_TIME[id], fSI:f/SI_TIME[id], lamSI:waveLen(S,f)*SI_LEN[id],
               m:measureWave(id,f)});
  }
  return {rows};
}
function buildModel(){
  const view=ST.view, M={view};
  if(MEDIA[view]) M.L=mediumModel(view); else M.X=mediaModel();
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
/* scientific notation the canvas can draw (superscript glyphs) and the readout can set
   (<sup>): the house sigf() renders 2.998e8 as "2.998×10^+8", which is not a number anyone
   writes.  Ordinary magnitudes go through sigf unchanged. */
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴',
            '5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function supTxt(n){ return String(n).split('').map(c=>SUPS[c]||'').join(''); }
function sciParts(x,n){
  const e=Math.floor(Math.log10(Math.abs(x)));
  return [sigf(x/Math.pow(10,e),n||4),e];
}
function sciTxt(x,n){
  if(x===0) return '0';
  if(Math.abs(x)>=1e-3&&Math.abs(x)<1e5) return sigf(x,n||4);
  const p=sciParts(x,n); return p[0]+'×10'+supTxt(p[1]);
}
function sciHTML(x,n){
  if(x===0) return '0';
  if(Math.abs(x)>=1e-3&&Math.abs(x)<1e5) return sigf(x,n||4);
  const p=sciParts(x,n); return p[0]+'&times;10<sup>'+p[1]+'</sup>';
}
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function lenU(x,S){ return sigf(x,3)+' '+S.unit; }
function timeU(x,S){ return sigf(x,3)+' '+S.tunit; }
function freqStr(S,f){ return sigf(f*S.fMul,4)+' '+S.fUnit; }
function pct(x,n){ return (x>=0?'+':'&minus;')+sigf(Math.abs(100*x),n||2)+' %'; }
function sourceWord(M){ return M.active?(M.mode==='pulse'?'firing a pulse':'on'):(M.mode==='pulse'?'armed — press to fire':'off'); }
function readoutHTML(M){
  const view=M.view;
  let s='<div class="rname">waves intro<small>'+TABS.find(t=>t[0]===view)[1]+'</small></div><table>';
  if(M.L){
    const L=M.L, S=L.S, R=L.R;
    s+=hd(S.name+', one source')
      +rrow('frequency f',freqStr(S,R.f))
      +rrow('wavelength &lambda; = v/f',lenU(L.lam,S),'good')
      +rrow('speed v',sigf(S.v,4)+' '+S.unit+'/'+S.tunit)
      +rrow('period T = 1/f',timeU(L.T,S))
      +rrow('amplitude',fmt(R.A,1)+' ('+L.mode+')')
      +rrow('the source',sourceWord(L),L.active?'good':'bad');
    s+=hd('on the lattice')
      +rrow('cells per wavelength',sigf(L.Nl,4))
      +rrow('time per step, solved',timeU(L.dt,S))
      +rrow('PhET&rsquo;s fixed step: &lambda; off by',pct(L.phetErr),'bad')
      +rrow('steps, time',L.steps+', '+timeU(L.t,S));
    if(L.bright) s+=hd('the screen')
      +rrow('brightness, centre &amp; edge',fmt(L.brightMid,3)+', '+fmt(L.brightEnd,3))
      +rrow('mean square at the centre',sigf(L.I[(L.I.length-1)/2|0],3));
    if(L.tone) s+=hd('the tone')+rrow('pitch, output level',fmt(L.tone.hz,1)+' Hz, '+fmt(L.tone.level,3))
      +rrow('playing',L.tone.on?'yes':'no',L.tone.on?'good':'');
    if(ST.watch||ST.tape||ST.meter){
      s+=hd('the tools');
      if(ST.watch) s+=rrow('stopwatch',timeU(R.watch.t,S)+(R.watch.on?' running':''));
      if(ST.tape) s+=rrow('tape measure',lenU(L.tapeLen,S),'good');
      if(ST.meter) s+=rrow('wave meter probes',sigf(L.probes[0],3)+', '+sigf(L.probes[1],3));
    }
  } else {
    for(const q of M.X.rows){
      s+=hd(q.S.name)
        +rrow('speed v',sigf(q.S.v,4)+' '+q.S.unit+'/'+q.S.tunit+' = '+sciHTML(q.vSI,4)+' m/s')
        +rrow('frequency f',freqStr(q.S,q.f))
        /* four figures on both, or the difference the row exists to show rounds away */
        +rrow('&lambda; = v/f',sigf(q.lam,4)+' '+q.S.unit,'good')
        +rrow('measured on the lattice',sigf(q.m.lam,4)+' '+q.S.unit+' ('+pct(q.m.err)+')',Math.abs(q.m.err)<0.005?'good':'bad')
        +rrow('cells per wavelength',sigf(q.Nl,4))
        +rrow('envelope, fitted power of r',fmt(q.m.pexp,3));
    }
  }
  s+='</table><div class="note">'+roNote(M)+'</div>';
  return s;
}
function roNote(M){
  const v=M.view;
  if(v==='water') return 'PhET&rsquo;s lattice: 151 &times; 151 cells, 111 &times; 111 of them visible, C = &frac12;. Its time step is solved from the lattice&rsquo;s dispersion relation, so &lambda; and T are exact along the axes; PhET fixes one step per medium instead.';
  if(v==='sound') return 'The same lattice as water, with a ruler 50 times longer and a clock a thousand times faster. Parcel displacement is &xi; = &nabla;p/&rho;&omega;&sup2;, drawn exaggerated.';
  if(v==='light') return 'The same lattice again, in nanometres and femtoseconds. The screen is PhET&rsquo;s: the mean square of the last column, smoothed over three rows, averaged over &plusmn;39, and mapped through PhET&rsquo;s brightness table.';
  return 'The wavelength on each row is measured on the lattice itself — a least-squares fit against the drive at every cell from 30 to 100 cells out, then the slope of the phase.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='water') return E('&part;&sup2;u/&part;t&sup2; = c&sup2;&nabla;&sup2;u &nbsp;&rArr;&nbsp; <span class="hl">&lambda; = v/f</span>, &nbsp; v = 1.65 cm/s',
    'each cell accelerates toward the average of its four neighbours: ripples spread at the speed the water sets, so raising the drip rate crowds the crests');
  if(v==='sound') return E('<span class="hl">&lambda; = v/f</span>, &nbsp; v = 343 m/s &nbsp;&middot;&nbsp; &xi; = &nabla;p/&rho;&omega;&sup2;',
    'the same equation in air: the colour is the pressure, and the parcels crowd where the pressure is high — sound is a wave in the air, not a flow of it');
  if(v==='light') return E('<span class="hl">&lambda; = c/f</span>, &nbsp; c = 3.00&times;10<sup>8</sup> m/s &nbsp;&middot;&nbsp; brightness &prop; &lang;E&sup2;&rang;',
    'the same equation again, at 10<sup>15</sup> Hz: the colour of the wave is its frequency, and what a screen records is the mean square of the field');
  return E('<span class="hl">v = f&lambda;</span> &nbsp;&rArr;&nbsp; log &lambda; = log v &minus; log f',
    'one equation for all three: on a log-log plane a fixed speed is a straight line of slope &minus;1, and the three media are three parallel lines');
}
function tagHTML(M){
  const v=M.view;
  if(M.L) return '<b>'+TABS.find(t=>t[0]===v)[1]+'</b> — '+freqStr(M.L.S,M.L.R.f)+', amplitude '+fmt(M.L.R.A,1)
    +(M.L.active?'':', source off')+(ST.running?'':', paused');
  return '<b>the three media</b> — v = f&lambda;, measured on the lattice';
}
