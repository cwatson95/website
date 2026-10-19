
/* ================================================================== *
 *  state, the three lattice runs and their clock, the per-view model, *
 *  readout, equation bar, tag                                         *
 * ================================================================== */
const TABS=[['tank','the ripple tank'],['two','two sources'],['slits','the slits'],
            ['far','the far field'],['path','path difference'],['lattice','the lattice']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c', water0:'#062848', water1:'#bfe8ff', barrier:'#8f9bb3'};
const RO_W=300;
/* the house #hint sits at bottom:11px, on top of the last line of a caption
   anchored at H - 12: every caption here ends HINT_H higher, clear of it
   (wave-on-a-string; neither the capture nor the audit can see it, because
   the hint is HTML, not canvas) */
const HINT_H=18;
const LATTICE_VIEWS={tank:1, two:1, slits:1};
const SCENE_LIST=SCENE_IDS.map(id=>({id,name:SCENES[id].name}));
const BARRIER_LIST=[{id:'none',name:'no barrier'},{id:'one',name:'one slit'},{id:'two',name:'two slits'}];
const SOUNDVIEW_LIST=[{id:'waves',name:'waves'},{id:'particles',name:'particles'},{id:'both',name:'both'}];
const SIDE_LIST=[{id:'top',name:'top view'},{id:'side',name:'side view'}];
const WAVE_LIST=[{id:'cont',name:'continuous'},{id:'pulse',name:'pulse'}];
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'slow',name:'slow'}];
const FARMODE_LIST=[{id:'phet',name:'PhET’s log brightness'},{id:'lin',name:'intensity |F|²'}];
const AP_LIST=APERTURES.map(a=>({id:a.id,name:a.name}));
/* the colour scale: PhET's MAX_AMPLITUDE_TO_PLOT_ON_RIGHT, the lattice value
   that maps to the brightest colour and the top of the charts */
const U_FULL=2.14;
const FRAME_DT=1/60;

const DEFAULTS={view:'tank', scene:'water',
  f_water:sceneF0(SCENES.water), f_sound:sceneF0(SCENES.sound), f_light:sceneF0(SCENES.light),
  amp_tank:8, amp_two:10, amp_slits:10, wave:'cont', look:'top', soundView:'waves',
  screen:true, inten:true, graph:false, tape:false, watch:false, meter:false,
  speed:'normal', running:true, src1:true, src2:true, planeOn:true, nodal:true, theory:true,
  sep_water:3, sep_sound:200, sep_light:1500, barrier:'one', bcol:LAT.MID,
  slitW_water:1.5, slitW_sound:90, slitW_light:500, slitD_water:3, slitD_sound:200, slitD_light:1500,
  laser:true, lam:DIF.LAM0, ap:'ellipse', farMode:'phet',
  ellD:0.1, ellE:0, recW:0.1, recH:0.1, csD:0.05, csW:0.05, disD:0.05, disP:0.1, disL:0,
  figH:0.1, figR:0, gauSx:0.03, gauSy:0.03, sltN:2, sltW:0.03, sltD:0.1,
  pd:3.2, pL:12, hyp:true, asym:true, latTh:30};
const ST=Object.assign({},DEFAULTS);
/* the barrier drags within the visible region less a tenth at each side (PhET's) */
const BCOL_MIN=Math.ceil(LAT.PAD+LAT.VIS/10), BCOL_MAX=Math.floor(LAT.PAD+LAT.VIS*9/10);
/* the tools, in fractions of the visible width (so they survive a change of medium) */
const TOOLS={tape:[[0.25,0.86],[0.55,0.86]], probes:[[0.45,0.5],[0.7,0.5]]};
const TOOLS0=JSON.parse(JSON.stringify(TOOLS));
const DRAG={what:null,off:[0,0]};

function stKey(base){ return base+'_'+ST.scene; }
function stF(){ return ST['f_'+ST.scene]; }
function ampKey(v){ return 'amp_'+v; }

/* ---- the three lattice runs and their clock ------------------------------ */
const RUNS={tank:makeRun('water','point',1), two:makeRun('water','point',2), slits:makeRun('water','plane',1)};
const CLOCK={acc:0, steps:0};
/* bring a run in line with the panel: medium (clears), frequency (keeps the
   waves unless light or plane), amplitude, sources, barrier, tools */
function syncRun(v){
  const R=RUNS[v]; if(!R) return null;
  if(R.scene!==ST.scene){ runSetScene(R,ST.scene); }
  if(R.f!==stF()) runSetFrequency(R,stF());
  R.A=ST[ampKey(v)];
  R.cont=(ST.wave==='cont');
  const S=SCENES[R.scene];
  if(v==='two'){ R.sep=ST[stKey('sep')];
    if(R.src[0]!==ST.src1) runSetSource(R,0,ST.src1);
    if(R.src[1]!==ST.src2) runSetSource(R,1,ST.src2); }
  if(v==='slits'){
    const P=R.plane, w=ST[stKey('slitW')], d=ST[stKey('slitD')];
    if(P.barrier!==ST.barrier||P.slitW!==w||P.slitD!==d){
      P.barrier=ST.barrier; P.bcol=ST.bcol; P.slitW=w; P.slitD=d; runClear(R); }
    else if(P.bcol!==ST.bcol){ P.bcol=ST.bcol; runClearRight(R,P.bcol); }
    if(P.on!==ST.planeOn){ P.on=ST.planeOn; runClear(R); }
  }
  R.probes=ST.meter?TOOLS.probes.map(p=>[p[0]*S.W,p[1]*S.W]):[];
  return R;
}
function curRun(){ return LATTICE_VIEWS[ST.view]?syncRun(ST.view):null; }
function stepsPerSecond(){ return LAT.EVENT_RATE*(ST.speed==='slow'?0.5:1); }
/* one frame of wall time: PhET's event timer, deterministic (FRAME_DT) */
function clockFrame(){
  const R=curRun(); if(!R||!ST.running) return 0;
  CLOCK.acc+=FRAME_DT; const per=1/stepsPerSecond(); let n=0;
  while(CLOCK.acc>=per&&n<3){ runStep(R); CLOCK.acc-=per; n++; CLOCK.steps++; }
  if(n===3) CLOCK.acc=0;
  return n;
}
function runFor(v,steps){ const R=syncRun(v); for(let k=0;k<steps;k++) runStep(R); return R; }
function resetRuns(){ for(const v in RUNS){ const R=RUNS[v]; runSetScene(R,ST.scene); R.watch.on=false; R.watch.t=0; } CLOCK.acc=0; }

/* ---- the far field: a render + FFT only when a parameter moves; the eight
   most recent results are kept, so flipping between apertures is free ---- */
const FAR_CACHE=[];
/* the aperture sliders' ranges, one table for the panel and the tests (PhET's values
   for its five apertures, mm and degrees; the Gaussian and the slits are this file's) */
const SLIDER_RANGE={ellD:[0.04,0.4],ellE:[0,0.99],recW:[0.04,0.4],recH:[0.04,0.4],csD:[0.04,0.15],csW:[0.04,0.15],
  disD:[0.01,0.1],disP:[0.05,0.2],disL:[0,4],figH:[0.04,0.4],figR:[0,360],gauSx:[0.01,0.08],gauSy:[0.01,0.08],
  sltN:[1,5],sltW:[0.01,0.1],sltD:[0.04,0.2]};
/* only the chosen aperture's own parameters: a hidden slider cannot trigger a transform */
const AP_KEYS={ellipse:['ellD','ellE'],rect:['recW','recH'],cs:['csD','csW'],disorder:['disD','disP','disL'],
               figure:['figH','figR'],gauss:['gauSx','gauSy'],slits:['sltN','sltW','sltD']};
function farParams(){ const P={ap:ST.ap}; for(const k of AP_KEYS[ST.ap]) P[k]=ST[k]; return P; }
function farModel(){
  const P=farParams(), key=JSON.stringify(P)+'|'+ST.lam;
  for(const e of FAR_CACHE) if(e.key===key) return e.val;
  const val=farCompute(P);
  FAR_CACHE.unshift({key,val}); if(FAR_CACHE.length>8) FAR_CACHE.pop();
  return val;
}
function farCompute(P){
  const rend=renderAperture(P,ST.lam), D=diffract(rend.t), n=DIF.N, h=n/2;
  const cut=[], ana=[], ks=[];
  for(let k=-h;k<h;k++){ const m=D.mag[h*n+k+h]; ks.push(k); cut.push(D.dc>0?(m/D.dc)*(m/D.dc):0);
    const a=fraunhoferCut(P,ST.lam,k*DIF.SIN_PER_BIN,rend); ana.push(a===null?NaN:a); }
  return {P,rend,D,ks,cut,ana,hasAna:!isNaN(ana[h+1]),zero:firstZero(P,ST.lam,rend),s:rend.s,
          open:rend.t.reduce((a,b)=>a+b,0)};
}
/* sin(theta) of the first dark fringe along the cut, where a closed form gives one:
   the disc j11 lambda/(pi D), the snapped rectangle lambda/w, N slits lambda/(N d), one slit lambda/a */
function firstZero(P,lam,rend){
  const lm=lam*1e-6;
  if(P.ap==='ellipse') return J11*lm/(PI*P.ellD);
  if(P.ap==='rect') return lm/(2*rend.iw*DIF.PX/rend.s);
  if(P.ap==='slits'){ const n=Math.round(P.sltN); return n>1?lm/(n*P.sltD):lm/P.sltW; }
  return null;
}

/* ---- the models ---------------------------------------------------------- */
function latModel(v){
  const R=syncRun(v), S=SCENES[R.scene], dx=sceneDx(S), lam=waveLen(S,R.f);
  const M={R,S,dx,lam,Nl:R.Nl,Om:R.Om,dt:R.dt,T:1/R.f,phetErr:phetLambda(S,R.f)/lam-1,
           steps:R.n,t:R.t,watch:R.watch};
  if(v==='two'){ const rs=runSourceRows(R); M.dEff=(rs[1]-rs[0])*dx; M.nodal=nodalCount(M.dEff/lam); }
  if(v==='slits'){ M.g=slitCells(R); M.X=(R.lat.nx-R.lat.pad-1-R.plane.bcol)*dx;
    M.aEff=M.g.a*dx; M.dEff=M.g.d*dx; M.fresnel=(R.plane.barrier==='two'?M.dEff:M.aEff)*(R.plane.barrier==='two'?M.dEff:M.aEff)/(lam*M.X); }
  if((ST.screen||ST.inten)&&R.scene==='light'){ M.I=screenIntensity(R); M.Imax=M.I.reduce((a,b)=>Math.max(a,b),0);
    M.th=(ST.theory&&(v==='two'||v==='slits'))?screenTheory(R):null; }
  if(ST.tape){ const a=TOOLS.tape[0], b=TOOLS.tape[1]; M.tapeLen=Math.hypot(b[0]-a[0],b[1]-a[1])*S.W; }
  if(ST.meter) M.probes=TOOLS.probes.map(p=>probeValue(R,p[0]*S.W,p[1]*S.W));
  return M;
}
function pathModel(){
  const d=ST.pd, L=ST.pL, lam=1, k=TAU;
  const mins=[];
  for(let m=0;(m+0.5)<d;m++){ const D=(m+0.5)*lam; mins.push({m,D,y:hyperY(d,D,L),yf:farY(d,D,L)}); }
  return {d,L,lam,k,n:nodalCount(d),mins,fraun:d*d/lam,I0:twoSourceI(L,0,d,k)};
}
function latticeModel(){
  const S=SCENES[ST.scene], f=stF(), Nl=cellsPerWave(S,f), Om=omegaStep(Nl), k=TAU/Nl, th=ST.latTh*DEG;
  const kth=latK(Om,th);
  return {S,f,Nl,Om,k,th,vp0:latPhaseSpeed(k,0)/LAT.C,vg0:latGroupSpeed(k,0)/LAT.C,
          vpd:latPhaseSpeed(latK(Om,PI/4),PI/4)/LAT.C,vgd:latGroupSpeed(latK(Om,PI/4),PI/4)/LAT.C,
          vpth:Om/kth/LAT.C,lamDiag:(TAU/latK(Om,PI/4))/Nl,
          R1:[0,30,45,60].map(a=>murReflection(k*Math.cos(a*DEG),k*Math.sin(a*DEG),1)),
          R2:[0,30,45,60].map(a=>murReflection(k*Math.cos(a*DEG),k*Math.sin(a*DEG),2)),
          phetErr:phetLambda(S,f)/waveLen(S,f)-1, dt:stepDt(S,f)};
}
function buildModel(){
  const view=ST.view, M={view};
  if(LATTICE_VIEWS[view]) M.L=latModel(view);
  if(view==='far') M.F=farModel();
  if(view==='path') M.P=pathModel();
  if(view==='lattice') M.K=latticeModel();
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
const DEG=PI/180;
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function lenU(x,S){ return sigf(x,3)+' '+S.unit; }
function timeU(x,S){ return sigf(x,3)+' '+S.tunit; }
function freqStr(S,f){ return sigf(f*S.fMul,4)+' '+S.fUnit; }
function pct(x){ return (x>=0?'+':'&minus;')+sigf(Math.abs(100*x),2)+' %'; }
function readoutHTML(M){
  const view=M.view;
  let s='<div class="rname">wave interference<small>'+TABS.find(t=>t[0]===view)[1]+'</small></div><table>';
  if(M.L){
    const L=M.L, S=L.S, R=L.R;
    s+=hd(S.name+(R.mode==='plane'?', a plane wave':(R.nSrc===2?', two sources':', one source')))
      +rrow('frequency f',freqStr(S,R.f))+rrow('wavelength &lambda; = v/f',lenU(L.lam,S),'good')
      +rrow('speed v',sigf(S.v,4)+' '+S.unit+'/'+S.tunit)+rrow('period 1/f',timeU(L.T,S))
      +rrow('amplitude',fmt(R.A,1)+(R.mode==='plane'?'':(R.cont?' (continuous)':' (pulse)')));
    s+=hd('on the lattice')+rrow('cells per wavelength',sigf(L.Nl,4))+rrow('time per step, solved',timeU(L.dt,S))
      +rrow('PhET&rsquo;s fixed step: &lambda; off by',pct(L.phetErr),'bad')
      +rrow('steps, time',L.steps+', '+timeU(L.t,S));
    if(view==='two') s+=hd('the sources')+rrow('separation on the lattice',lenU(L.dEff,S)+' ('+fmt(L.dEff/L.lam,2)+' &lambda;)')
      +rrow('nodal lines, 2&lceil;d/&lambda; &minus; &frac12;&rceil;',String(L.nodal),'good');
    if(view==='slits'){
      const P=R.plane;
      s+=hd('the barrier')+rrow('barrier',BARRIER_LIST.find(b=>b.id===P.barrier).name+', '+lenU(xOfCell(R,P.bcol),S));
      if(P.barrier!=='none') s+=rrow('slit width on the lattice',lenU(L.aEff,S)+' ('+L.g.a+' cells)')
        +(P.barrier==='two'?rrow('slit separation on the lattice',lenU(L.dEff,S)):'')
        +rrow('to the screen, L',lenU(L.X,S))+rrow((P.barrier==='two'?'d':'a')+'&sup2;/&lambda;L (far field &#8810; 1)',sigf(L.fresnel,3),L.fresnel<0.3?'good':'bad');
    }
    if(L.I&&M.L.Imax>0) s+=hd('the screen')+rrow('peak intensity (arb.)',sigf(L.Imax,3));
    if(ST.watch) s+=rrow('stopwatch',timeU(R.watch.t,S)+(R.watch.on?' running':''));
    if(ST.tape) s+=rrow('tape measure',lenU(L.tapeLen,S),'good');
    if(ST.meter) s+=rrow('wave meter probes',sigf(L.probes[0],3)+', '+sigf(L.probes[1],3));
  }
  else if(view==='far'){
    const F=M.F, P=F.P;
    s+=hd(APERTURES.find(a=>a.id===P.ap).name+(APERTURES.find(a=>a.id===P.ap).phet?'':' (not in PhET)'))
      +rrow('wavelength',fmt(ST.lam,1)+' nm')+rrow('open area',sigf(F.open*DIF.PX*DIF.PX/(F.s*F.s),3)+' mm&sup2;')
      +rrow('the picture spans',' &plusmn;'+sigf(Math.asin(128*DIF.SIN_PER_BIN)/DEG,3)+'&deg;');
    if(F.zero!==null&&F.zero<1) s+=rrow(P.ap==='ellipse'?'first dark ring 1.22 &lambda;/D':(P.ap==='rect'?'first zero &lambda;/w':(Math.round(P.sltN)>1?'first zero &lambda;/Nd':'first zero &lambda;/a')),sigf(Math.asin(F.zero)/DEG,3)+'&deg;','good');
    s+=hd('the transform')+rrow('grid','256 &times; 256, '+sigf(DIF.PX*1000,3)+' &micro;m')+rrow('aperture drawn &times;&lambda;<sub>0</sub>/&lambda;',sigf(F.s,4))
      +rrow('laser',ST.laser?'on':'off',ST.laser?'good':'bad');
  }
  else if(view==='path'){
    const P=M.P;
    s+=hd('two sources, in wavelengths')+rrow('separation d',fmt(P.d,2)+' &lambda;')+rrow('screen at L',fmt(P.L,1)+' &lambda;')
      +rrow('nodal lines',String(P.n),'good')+rrow('Fraunhofer distance d&sup2;/&lambda;',sigf(P.fraun,3)+' &lambda;',P.L>P.fraun?'good':'bad');
    for(const q of P.mins.slice(0,3)) s+=rrow('minimum m = '+q.m+': exact, far field',sigf(q.y,4)+', '+sigf(q.yf,4)+' &lambda;');
  }
  else {
    const K=M.K;
    s+=hd('the scheme')+rrow('Courant number C = c&Delta;t/&Delta;x','1/2 (stable to 1/&radic;2)')+rrow('medium, f',K.S.name+', '+freqStr(K.S,K.f))
      +rrow('cells per wavelength',sigf(K.Nl,4))+rrow('&omega;&Delta;t per step',sigf(K.Om,4));
    s+=hd('speeds / c')+rrow('phase, along an axis',sigf(K.vp0,5))+rrow('phase, diagonal',sigf(K.vpd,5))
      +rrow('phase, at &theta; = '+fmt(ST.latTh,0)+'&deg;',sigf(K.vpth,5),'good')
      +rrow('group, axis / diagonal',sigf(K.vg0,4)+' / '+sigf(K.vgd,4))+rrow('&lambda; diagonal / &lambda; axis',sigf(K.lamDiag,5));
    s+=hd('the edges, |R| at 0, 30, 45, 60&deg;')+rrow('Mur 2nd order (here)',K.R2.map(r=>sigf(100*r,2)).join(', ')+' %','good')
      +rrow('Mur 1st order',K.R1.map(r=>sigf(100*r,2)).join(', ')+' %','bad');
    s+=hd('calibration')+rrow('time per step',timeU(K.dt,K.S))+rrow('PhET&rsquo;s step: &lambda; off by',pct(K.phetErr),'bad');
  }
  s+='</table><div class="note">'+roNote(view)+'</div>';
  return s;
}
function roNote(view){
  if(LATTICE_VIEWS[view]) return 'The lattice is PhET&rsquo;s: 151 &times; 151 cells, 111 &times; 111 visible, C = &frac12;. Its time step is solved from the dispersion relation, so &lambda; and f are exact along the axes; PhET fixes one step per medium.';
  if(view==='far') return 'The pattern is |FFT| of the aperture (256 &times; 256 over 4/3 mm, PhET&rsquo;s grid), checked against a direct DFT; the orange curve is the closed form.';
  if(view==='path') return 'Pure geometry: each source a 2-D cylindrical wave e<sup>ikr</sup>/&radic;r. Nodal lines are hyperbolae with the sources as foci.';
  return 'Everything on this view is the lattice&rsquo;s dispersion relation, pinned against derive.py.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='tank') return E('&part;&sup2;u/&part;t&sup2; = c&sup2;&nabla;&sup2;u &nbsp;&rArr;&nbsp; <span class="hl">u<sup>n+1</sup> = 2u<sup>n</sup> &minus; u<sup>n&minus;1</sup> + C&sup2;(u<sub>E</sub> + u<sub>W</sub> + u<sub>N</sub> + u<sub>S</sub> &minus; 4u<sup>n</sup>)</span>, &nbsp;C = &frac12; &nbsp;&middot;&nbsp; v = f&lambda;',
    'the wave equation on PhET&rsquo;s lattice: each cell moves toward the average of its four neighbours; ripples spread at v = f&lambda;');
  if(v==='two') return E('r<sub>1</sub> &minus; r<sub>2</sub> = (m + &frac12;)&lambda; &nbsp;&rArr;&nbsp; <span class="hl">d sin &theta; = (m + &frac12;)&lambda;</span> <span class="rm">far away</span>',
    'where the two waves arrive half a wavelength apart they cancel: the nodal lines are hyperbolae, and far away they are straight');
  if(v==='slits') return E('<span class="hl">d sin &theta; = m&lambda;</span> <span class="rm">bright</span>, &nbsp; a sin &theta; = m&lambda; <span class="rm">dark (single slit)</span> &nbsp;&middot;&nbsp; I &prop; sinc&sup2;(&pi;a sin&theta;/&lambda;) cos&sup2;(&pi;d sin&theta;/&lambda;)',
    'Huygens: every open cell of the barrier is a new source; the far-field formula needs L &#8811; d&sup2;/&lambda;, and PhET&rsquo;s light screen is closer than that');
  if(v==='far') return E('<span class="hl">I(&theta;) &prop; |&#8748; t(x,y) e<sup>&minus;ik sin&theta; &middot; r</sup> dx dy|&sup2;</span> &nbsp;&middot;&nbsp; <span class="rm">disc:</span> [2J<sub>1</sub>(v)/v]&sup2;, v = &pi;D sin&theta;/&lambda;',
    'far from the aperture the pattern is the Fourier transform of the aperture: small holes spread light wide, and the pattern rotates with the aperture');
  if(v==='path') return E('r<sub>1</sub> &minus; r<sub>2</sub> = &Delta;: &nbsp; <span class="hl">y&sup2;/a&sup2; &minus; x&sup2;/b&sup2; = 1</span>, &nbsp; a = &Delta;/2, &nbsp; b&sup2; = d&sup2;/4 &minus; a&sup2; &nbsp;&rArr;&nbsp; sin &theta;<sub>&infin;</sub> = &Delta;/d',
    'every line of constant path difference is a hyperbola with the sources as its foci; its asymptote is the far-field direction d sin&theta; = &Delta;');
  return E('<span class="hl">sin&sup2;(&omega;&Delta;t/2) = C&sup2;[sin&sup2;(k<sub>x</sub>&Delta;x/2) + sin&sup2;(k<sub>y</sub>&Delta;x/2)]</span> &nbsp;&middot;&nbsp; stable iff C &le; 1/&radic;2',
    'the lattice&rsquo;s own dispersion relation: short waves lag, and the lag depends on direction — this is what calibrates every length and time in the sim');
}
function tagHTML(M){
  const v=M.view;
  if(M.L){ const R=M.L.R; return '<b>'+TABS.find(t=>t[0]===v)[1]+'</b> — '+SCENES[R.scene].name+', '+freqStr(SCENES[R.scene],R.f)+(ST.running?'':', paused'); }
  if(v==='far') return '<b>the far field</b> — '+APERTURES.find(a=>a.id===ST.ap).name+', '+fmt(ST.lam,0)+' nm'+(ST.laser?'':', laser off');
  if(v==='path') return '<b>path difference</b> — d = '+fmt(ST.pd,2)+' &lambda;, L = '+fmt(ST.pL,1)+' &lambda;';
  return '<b>the lattice</b> — '+SCENES[ST.scene].name+', '+freqStr(SCENES[ST.scene],stF());
}
