
/* ================================================================== *
 *  state: the beaker (PhET's Concentration screen), the cuvette       *
 *  (its Beer's Law screen), the clock they both run on, the per-view  *
 *  models, and the readout / equation bar / tag                       *
 * ================================================================== */
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c', glass:'#8fb8d4', solid:'#e8843a',
           beam:'#5ac8e0', eye:'#9aa2b4'};
const RO_W=300;
/* the house #hint sits at bottom:11px on top of the last line of a caption anchored at
   H - 12, so every caption here ends HINT_H higher (build/wave-on-a-string/, Known-bad) */
const HINT_H=18;
const FRAME_DT=1/60;             /* a fixed step, so the headless suites are deterministic */

const SOLUTE_LIST=SOLUTES.map(s=>({id:s.id,name:s.name}));
const BLS_LIST=BLSOLS.map(s=>({id:s.id,name:soluteById(s.solute).name}));
const FORM_LIST=[{id:'solid',name:'solid'},{id:'solution',name:'solution'}];
const METER_LIST=[{id:'molar',name:'mol/L'},{id:'percent',name:'%'}];
const BEAKER_UNIT_LIST=[{id:'liters',name:'L'},{id:'milliliters',name:'mL'}];
const MODE_LIST=[{id:'preset',name:'preset'},{id:'variable',name:'variable'}];
const DET_LIST=[{id:'transmittance',name:'transmittance'},{id:'absorbance',name:'absorbance'}];
const ILLUM_LIST=[{id:'E',name:'equal energy'},{id:'A',name:'illuminant A'}];
const LAWX_LIST=[{id:'conc',name:'against c'},{id:'path',name:'against l'}];

const DEFAULTS={view:TABS[0][0],
  /* the Concentration screen */
  solute:'drinkMix', form:'solid',
  shaking:false, dropper:false, faucet:false, drain:false, evap:0,
  running:true, meterUnits:'molar', beakerUnits:'liters',
  showAmount:false, showVolume:false,
  /* the Beer's Law screen */
  blSolution:'drinkMix', blConc:BLSOLS[0].cDefault, cuvette:PHET.CUVETTE_DEFAULT,
  lightOn:true, lightMode:'preset', wavelength:lambdaMaxOf('drinkMix'),
  detector:'transmittance', snap:true,
  /* the analysis views */
  allSpectra:false, lawX:'conc', illum:'E', colourPath:PHET.CUVETTE_DEFAULT};
const ST=Object.assign({},DEFAULTS);

/* the beaker itself is a stepped object, not a slider value: it carries the running mole
   ledger and the shaker's particles in flight.  V0 is remembered so the volume ledger has
   something to close against. */
let BK=makeBeaker(DEFAULTS.solute,0,PHET.VOL_DEFAULT);
const RNG={f:makeRngB(20260922)};
function resetBeaker(){
  BK=makeBeaker(ST.solute,0,PHET.VOL_DEFAULT);
  RNG.f=makeRngB(20260922);
}
function setSoluteId(id){
  ST.solute=id;
  /* PhET empties the solute when the solute changes -- the beaker cannot hold two */
  BK.solute=id; BK.n=0; BK.parts=[];
  resetLedger();
}
function setMoles(n){ BK.n=clamp(n,PHET.SOLUTE_MOL_MIN,PHET.SOLUTE_MOL_MAX); resetLedger(); }
function setVolume(V){ BK.V=clamp(V,PHET.VOL_MIN,PHET.VOL_MAX); resetLedger(); }
/* setting a value by hand is not a transaction the ledger can account for, so the ledger
   is re-based on the state it finds: the residual stays meaningful afterwards */
function resetLedger(){
  BK.n0=BK.n; BK.V0=BK.V;
  BK.led={shaker:0,dropper:0,drained:0,faucet:0,evaporated:0,drainedV:0,dropperV:0,
          flying:MOLE_PER_PARTICLE*BK.parts.length};
}

/* the concentration meter's probe, in BEAKER-LOCAL coordinates: x across the inner width
   (0 at the left wall, 1 at the right), y up from the floor (0 at the floor, 1 at the brim).
   The meter reads only when the tip is in the solution, exactly as PhET's does. */
const PROBE={x:0.78, y:0.18};
const PROBE0={x:0.78, y:0.18};
/* the Beer's Law detector probe, in CUVETTE-LOCAL coordinates: x in cm from the cuvette's
   left face (so it can sit inside the cuvette or past it), y in cm above the beam axis. */
/* x is measured in cm from the cuvette's LEFT face, so the probe can sit inside the
   glass or past it; y in cm above the beam axis */
const DET={x:3.4, y:0};
const DET0={x:3.4, y:0};
const DRAG={what:null, grabW:0, grabX:0};
const PROBE_WALL=0.04;
function probeInSolution(){
  return PROBE.x>=PROBE_WALL && PROBE.x<=1-PROBE_WALL
      && PROBE.y>=0 && PROBE.y<=bkFill(BK) && BK.V>0;
}
/* PhET's ATDetector.isProbeInBeam: the light is on and the probe spans the beam.  The beam
   is 0.45 cm across (PhET's lensDiameter) and the probe's sensor 1 cm, so "spans" is the
   probe's own half-height reaching past both beam edges. */
const BEAM_HALF=0.225, SENSOR_HALF=0.5;
function detectorInBeam(){
  return ST.lightOn && Math.abs(DET.y)+BEAM_HALF<SENSOR_HALF && DET.x>0;
}

/* ---- the clock: PhET's five mechanisms, in PhET's order ----------------------------- */
function stepFrame(){
  if(!ST.running) return false;
  const solidForm=(ST.form==='solid');
  const ctl={faucet:ST.faucet?PHET.FAUCET_FLOW:0,
             drain:ST.drain?PHET.FAUCET_FLOW:0,
             dropper:(!solidForm&&ST.dropper&&BK.n<PHET.SOLUTE_MOL_MAX)?PHET.DROPPER_FLOW:0,
             evap:BK.V>0?ST.evap:0,
             shaking:solidForm&&ST.shaking&&BK.n<PHET.SOLUTE_MOL_MAX};
  const busy=ctl.faucet>0||ctl.drain>0||ctl.dropper>0||ctl.evap>0||ctl.shaking||
             BK.parts.length>0;
  if(!busy) return false;
  bkStep(BK,FRAME_DT,ctl,RNG.f);
  return true;
}
function emptyBeaker(){ BK.n=0; BK.V=0; BK.parts=[]; resetLedger(); }
function fillBeaker(){ BK.V=PHET.VOL_MAX; resetLedger(); }

/* ---- the Beer's Law screen ---------------------------------------------------------- */
function currentBls(){ return blsById(ST.blSolution); }
function presetWavelength(){ return lambdaMaxOf(ST.blSolution); }
function activeWavelength(){
  return ST.lightMode==='preset'?presetWavelength():ST.wavelength;
}
function setBlSolution(id){
  ST.blSolution=id;
  ST.blConc=blsById(id).cDefault;
  /* PhET re-points the light at the new solution's lambda_max whenever the solution
     changes, in BOTH modes for the preset and on switching back to it */
  if(ST.lightMode==='preset') ST.wavelength=lambdaMaxOf(id);
}
function cuvetteWidth(){ return clamp(ST.cuvette,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX); }
/* PhET snaps the cuvette's width to a 0.1 cm interval when a drag ENDS (its
   snapIntervalProperty); zero means no snapping. */
function snapCuvette(w){
  const s=ST.snap?PHET.CUVETTE_SNAP:0;
  if(!(s>0)) return clamp(w,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);
  return clamp(Math.round(w/s)*s,PHET.CUVETTE_MIN,PHET.CUVETTE_MAX);
}

/* ---- the models --------------------------------------------------------------------- */
function beakerModel(){
  const sol=soluteById(BK.solute);
  const cs=sol.cSat;
  const C=bkConc(BK), P=bkPrecip(BK);
  const g=soluteGrams(BK.n,BK.V,cs,sol.molarMass);
  const M={sol, n:BK.n, V:BK.V, C, precip:P, sat:bkSaturated(BK),
           grams:g, percent:percentConcentration(g,BK.V),
           rgb:schemeColor(BK.solute,C), fill:bkFill(BK),
           parts:BK.parts, nParts:particleCount(P),
           led:BK.led, resid:bkLedgerResidual(BK), V0:BK.V0, n0:BK.n0,
           cs, Vsat:saturationVolume(BK.n,cs),
           tSat:timeToSaturate(BK.n,BK.V,cs,ST.evap>0?ST.evap:PHET.EVAPORATION_MAX),
           probeIn:probeInSolution(), empty:!(BK.V>0),
           full:BK.V>=PHET.VOL_MAX-1e-12, stockPct:stockPercent(sol)};
  M.reading=M.probeIn?(ST.meterUnits==='molar'?M.C:M.percent):null;
  M.flying=BK.led.flying;
  return M;
}
function cuvetteModel(){
  const d=currentBls(), sol=soluteById(d.solute);
  const lam=activeWavelength(), l=cuvetteWidth(), c=ST.blConc;
  const eps=epsAt(d.id,lam);
  const A=absorbance(eps,l,c), T=transmittance(A);
  const M={d, sol, lam, l, c, eps, A, T, lamMax:lambdaMaxOf(d.id), epsMax:epsMaxOf(d.id),
           rgb:rampColor(d.id,c), inBeam:detectorInBeam(), on:ST.lightOn,
           mode:ST.lightMode, det:ST.detector,
           wave:waveRGB(lam), atMax:Math.round(lam)===lambdaMaxOf(d.id)};
  M.reading=(M.on&&M.inBeam)?(ST.detector==='absorbance'?A:T):null;
  M.beyondLinear=c>LINEAR_LIMIT;
  M.Amax2=absorbance(M.epsMax,PHET.CUVETTE_MAX,d.cMax);
  return M;
}
function spectrumModel(){
  const d=currentBls(), l=cuvetteWidth(), c=ST.blConc, lam=activeWavelength();
  const t=EPS[d.id];
  const xs=[], eps=[], Aa=[], Tt=[];
  for(let i=0;i<NLAM;i++){
    xs.push(LAM0+i); eps.push(t[i]);
    const A=absorbance(t[i],l,c);
    Aa.push(A); Tt.push(transmittance(A));
  }
  let epsHi=0;
  for(const s of BLSOLS) epsHi=Math.max(epsHi,epsMaxOf(s.id));
  return {d, xs, eps, A:Aa, T:Tt, lam, l, c,
          lamMax:lambdaMaxOf(d.id), epsMax:epsMaxOf(d.id), epsHere:epsAt(d.id,lam),
          Ahere:absorbance(epsAt(d.id,lam),l,c), epsHi,
          all:BLSOLS.map(s=>({id:s.id, name:soluteById(s.solute).name,
                              eps:EPS[s.id], lamMax:lambdaMaxOf(s.id)}))};
}
function lawModel(){
  const d=currentBls(), l=cuvetteWidth(), c=ST.blConc, lam=activeWavelength();
  const eps=epsAt(d.id,lam);
  const N=101, cs=[], Ac=[], Tc=[], ls=[], Al=[], Tl=[];
  for(let i=0;i<=N;i++){
    const cc=d.cMax*i/N, ll=PHET.CUVETTE_MAX*i/N;
    cs.push(cc); Ac.push(absorbance(eps,l,cc)); Tc.push(transmittance(absorbance(eps,l,cc)));
    ls.push(ll); Al.push(absorbance(eps,ll,c)); Tl.push(transmittance(absorbance(eps,ll,c)));
  }
  /* T against A is the same curve for every solution: that is the point of the panel */
  const As=[], Ts=[];
  for(let i=0;i<=120;i++){ const A=4*i/120; As.push(A); Ts.push(transmittance(A)); }
  const A=absorbance(eps,l,c);
  return {d, l, c, lam, eps, A, T:transmittance(A),
          cs, Ac, Tc, ls, Al, Tl, As, Ts,
          Amax:absorbance(eps,PHET.CUVETTE_MAX,d.cMax),
          lines:[0.5,1,2].map(ll=>({l:ll, A:cs.map(cc=>absorbance(eps,ll,cc))})),
          linear:LINEAR_LIMIT, beyond:d.cMax>LINEAR_LIMIT};
}
function ledgerModel(){
  const B=beakerModel();
  /* the evaporation curve: with n held, C = n/V, clamped at Csat */
  const vs=[], cc=[], raw=[];
  for(let i=0;i<=160;i++){
    const V=PHET.VOL_MAX*(1-i/160);
    vs.push(V);
    cc.push(V>0?Math.min(B.cs,B.n/V):NaN);
    raw.push(V>0?B.n/V:NaN);
  }
  return {B, vs, C:cc, raw, Vsat:B.Vsat,
          /* the fifth field is the SHORT key the bar chart writes under its column:
             truncating the sentence gave "the dropper pu" */
          rows:[['the shaker put in', B.led.shaker,'mol', COL.pos, 'shaker'],
                ['the dropper put in', B.led.dropper,'mol', COL.pos, 'dropper'],
                ['the drain took out', -B.led.drained,'mol', COL.ref, 'drain'],
                ['still in the air', B.flying,'mol', COL.live, 'in air']],
          vrows:[['it started with', B.V0,'L', COL.struct, 'start'],
                 ['the faucet put in', B.led.faucet,'L', COL.pos, 'faucet'],
                 ['the dropper put in', B.led.dropperV,'L', COL.pos, 'dropper'],
                 ['the drain took out', -B.led.drainedV,'L', COL.ref, 'drain'],
                 ['evaporation took out', -B.led.evaporated,'L', COL.ref, 'evap']]};
}
function colourModel(){
  const id=SHOW_BEERS?ST.blSolution:ST.solute;
  const usable=hasSpectrum(id)?id:BLSOLS[0].id;
  const d=blsById(usable);
  const l=SHOW_BEERS?cuvetteWidth():ST.colourPath;
  const cHere=SHOW_BEERS?ST.blConc:Math.min(bkConc(BK),d.cMax);
  const N=24, sw=[];
  for(let i=0;i<=N;i++){
    const c=d.cMax*i/N;
    const t=trueRGB(usable,l,c,ST.illum);
    sw.push({c, true_:t.rgb, Ytrue:t.Y, phet:rampColor(usable,c),
             Yphet:relLum(rampColor(usable,c)),
             gap:Math.max(Math.abs(t.rgb[0]-rampColor(usable,c)[0]),
                          Math.abs(t.rgb[1]-rampColor(usable,c)[1]),
                          Math.abs(t.rgb[2]-rampColor(usable,c)[2]))});
  }
  let worst=0, worstC=0;
  for(const s of sw) if(s.gap>worst){ worst=s.gap; worstC=s.c; }
  const here=trueRGB(usable,l,cHere,ST.illum);
  const t=EPS[usable], Ts=[], xs=[], yb=[];
  for(let i=0;i<NLAM;i++){
    xs.push(LAM0+i);
    Ts.push(Math.pow(10,-t[i]*l*cHere));
    yb.push(CIE_Y[i]);
  }
  return {id:usable, name:soluteById(usable).name, d, l, c:cHere, sw, worst, worstC,
          here, phetHere:rampColor(usable,cHere), xs, T:Ts, ybar:yb,
          illum:ST.illum, illumName:ILLUM_LIST.filter(o=>o.id===ST.illum)[0].name,
          white:trueRGB(usable,l,0,ST.illum).rgb};
}
function solutesModel(){
  const rows=SOLUTES.map(s=>{
    const cLit=s.lit.gPerL/s.lit.M;
    return {s, cLit, dC:(s.cSat-cLit)/cLit, dM:(s.molarMass-s.lit.M)/s.lit.M,
            spectrum:hasSpectrum(s.id), lamMax:hasSpectrum(s.id)?lambdaMaxOf(s.id):null,
            epsMax:hasSpectrum(s.id)?epsMaxOf(s.id):null, pct:stockPercent(s)};
  });
  let worst=0;
  for(const r of rows) worst=Math.max(worst,Math.abs(r.dC));
  return {rows, worst, here:ST.solute};
}
function buildModel(){
  const v=ST.view, M={view:v};
  if(v==='beaker') M.B=beakerModel();
  else if(v==='cuvette') M.C=cuvetteModel();
  else if(v==='spectrum') M.S=spectrumModel();
  else if(v==='law') M.L=lawModel();
  else if(v==='ledger') M.G=ledgerModel();
  else if(v==='solutes') M.U=solutesModel();
  else M.K=colourModel();
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
/* scientific notation.  HTML gets real markup; the canvas gets `1.23e-7`, because a
   superscript minus is not in the rasteriser's font (BRIEF: letter subscripts and exotic
   superscripts are tofu, digits are fine). */
function sci(x,nd){
  if(x===null||x===undefined||!isFinite(x)) return '&mdash;';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x)));
  const m=x/Math.pow(10,e);
  return fmt(m,nd===undefined?2:nd)+' &times; 10<sup>'+e+'</sup>';
}
function sciPlain(x,nd){
  if(x===null||x===undefined||!isFinite(x)) return '—';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x)));
  const m=x/Math.pow(10,e);
  return fmt(m,nd===undefined?2:nd)+'e'+e;
}
function volStr(V){
  return ST.beakerUnits==='milliliters'
    ? fmt(V*1000,PHET.DEC_VOLUME===2?0:PHET.DEC_VOLUME)+' mL'
    : fmt(V,PHET.DEC_VOLUME)+' L';
}
function volPlain(V){ return plain(volStr(V)); }
function concStr(C){ return fmt(C,PHET.DEC_CONC)+' mol/L'; }
function molStr(n){ return fmt(n,3)+' mol'; }
/* the Beer's Law screen shows concentration in mM or uM, which is PhET's transform */
function blConcStr(c){
  const d=currentBls();
  return fmt(c*d.scale,PHET.DEC_CONC===3?0:PHET.DEC_CONC)+' '+d.transform;
}
function meterStr(M){
  if(M.reading===null) return '&mdash; <span class="bad">probe is out</span>';
  return ST.meterUnits==='molar'?concStr(M.reading)
                                :fmt(M.reading,PHET.DEC_PERCENT)+' %';
}
function rgbSwatch(v){
  return '<span style="display:inline-block;width:11px;height:11px;border-radius:2px;'
       +'vertical-align:-1px;margin-right:5px;background:'+rgbCss(v)
       +';box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)"></span>';
}

function readoutHTML(M){
  let s='<div class="rname">'+(SHOW_BEERS?'beer&rsquo;s law lab':'concentration')
       +'<small>'+TABS.filter(t=>t[0]===M.view)[0][1]+'</small></div><table>';
  if(M.B){
    const B=M.B;
    s+=hd('the beaker')
      +rrow('solute',B.sol.html)
      +rrow('meter',meterStr(B),B.probeIn?'good':'')
      +rrow('solute amount',molStr(B.n))
      +rrow('solution volume',volStr(B.V)+(B.full?' (full)':''))
      +rrow('concentration',concStr(B.C),'good')
      +rrow('mass percent',fmt(B.percent,PHET.DEC_PERCENT)+' %')
      +rrow('dissolved',fmt(B.grams,1)+' g')
      +rrow('saturated?',B.sat?'<b>Saturated!</b>':'no',B.sat?'bad':'')
      +rrow('solid on the bottom',B.precip>0?fmt(B.precip,3)+' mol':'none',B.precip>0?'bad':'')
      +rrow('solid drawn as',B.nParts+' particles');
    s+=hd('this solute (PhET&rsquo;s values)')
      +rrow('molar mass',fmt(B.sol.molarMass,3)+' g/mol')
      +rrow('saturates at',fmt(B.cs,2)+' mol/L')
      +rrow('stock solution',fmt(B.sol.stock,2)+' mol/L ('+fmt(B.stockPct,1)+' mass %)')
      +rrow('solution colour',rgbSwatch(B.rgb)+rgbCss(B.rgb));
    s+=hd('the mole ledger')
      +rrow('shaker in',fmt(B.led.shaker,4)+' mol','good')
      +rrow('dropper in',fmt(B.led.dropper,4)+' mol','good')
      +rrow('drain out',fmt(B.led.drained,4)+' mol','')
      +rrow('in the air',fmt(B.flying,4)+' mol')
      +rrow('residual',sci(B.resid.n,2)+' mol',Math.abs(B.resid.n)>1e-12?'bad':'good');
  } else if(M.C){
    const C=M.C;
    s+=hd('the cuvette')
      +rrow('solution',C.sol.html)
      +rrow('concentration',blConcStr(C.c),'good')
      +rrow('path length l',fmt(C.l,PHET.DEC_CUVETTE)+' cm')
      +rrow('wavelength &lambda;',fmt(C.lam,PHET.DEC_LAMBDA)+' nm'
            +(C.atMax?' <span class="good">(&lambda;<sub>max</sub>)</span>':''))
      +rrow('molar absorptivity &epsilon;',fmt(C.eps,2)+' L mol<sup>&minus;1</sup> cm<sup>&minus;1</sup>');
    s+=hd('what the detector says')
      +rrow('absorbance A',C.reading===null?'&mdash;':fmt(C.A,PHET.DEC_A),'good')
      +rrow('transmittance T',C.reading===null?'&mdash;':fmt(100*C.T,PHET.DEC_T)+' %')
      +rrow('',C.on?(C.inBeam?'probe is in the beam':'<span class="bad">probe is out of the beam</span>')
                  :'<span class="bad">the light is off</span>')
      +rrow('A = &epsilon;lc',fmt(C.eps,4)+' &times; '+fmt(C.l,2)+' &times; '+sci(C.c,3))
      +rrow('10<sup>&minus;A</sup>',sci(C.T,4));
    s+=hd('this solution')
      +rrow('&lambda;<sub>max</sub>',fmt(C.lamMax,0)+' nm')
      +rrow('&epsilon; at &lambda;<sub>max</sub>',fmt(C.epsMax,2))
      +rrow('range',blConcStr(0)+' &ndash; '+blConcStr(C.d.cMax))
      +rrow('largest A here',fmt(C.Amax2,3)+' (2 cm, full scale)')
      +rrow('cuvette colour',rgbSwatch(C.rgb)+rgbCss(C.rgb))
      +rrow('beyond 10 mM?',C.beyondLinear?'<b>yes</b>':'no',C.beyondLinear?'bad':'');
  } else if(M.S){
    const S=M.S;
    s+=hd('the spectrum')
      +rrow('solution',soluteById(S.d.solute).html)
      +rrow('&lambda;<sub>max</sub>',fmt(S.lamMax,0)+' nm','good')
      +rrow('&epsilon; at &lambda;<sub>max</sub>',fmt(S.epsMax,2))
      +rrow('cursor &lambda;',fmt(S.lam,0)+' nm')
      +rrow('&epsilon; there',fmt(S.epsHere,2))
      +rrow('A there',fmt(S.Ahere,PHET.DEC_A),'good')
      +rrow('T there',fmt(100*transmittance(S.Ahere),PHET.DEC_T)+' %');
    s+=hd('all eight, at their peaks');
    for(const a of S.all)
      s+=rrow(a.name,fmt(a.lamMax,0)+' nm',a.id===S.d.id?'good':'');
  } else if(M.L){
    const L=M.L;
    s+=hd('the law, here')
      +rrow('&epsilon;',fmt(L.eps,4)+' L mol<sup>&minus;1</sup> cm<sup>&minus;1</sup>')
      +rrow('l',fmt(L.l,PHET.DEC_CUVETTE)+' cm')
      +rrow('c',sci(L.c,4)+' mol/L')
      +rrow('A = &epsilon;lc',fmt(L.A,4),'good')
      +rrow('T = 10<sup>&minus;A</sup>',fmt(100*L.T,3)+' %')
      +rrow('&minus;log<sub>10</sub>T',fmt(absorbanceOfT(L.T),4),'good');
    s+=hd('the landmarks')
      +rrow('A = 1','10 % gets through')
      +rrow('A = 2','1 %')
      +rrow('A = 3','0.1 %')
      +rrow('largest A here',fmt(L.Amax,3))
      +rrow('T underflows at','A = 324');
    s+=hd('where the line stops being true')
      +rrow('linear to about',fmt(1000*L.linear,0)+' mM')
      +rrow('this range reaches',blConcStr(L.d.cMax),L.beyond?'bad':'')
      +rrow('',L.beyond?'past it &mdash; the straight line is an extrapolation'
                       :'inside it');
  } else if(M.G){
    const G=M.G, B=G.B;
    s+=hd('the mole ledger')
      +rrow('shaker in',fmt(B.led.shaker,5)+' mol','good')
      +rrow('dropper in',fmt(B.led.dropper,5)+' mol','good')
      +rrow('drain out',fmt(B.led.drained,5)+' mol')
      +rrow('still in the air',fmt(B.flying,5)+' mol')
      +rrow('= in the beaker',fmt(B.n,5)+' mol','good')
      +rrow('residual',sci(B.resid.n,2)+' mol',Math.abs(B.resid.n)>1e-12?'bad':'good');
    s+=hd('the volume ledger')
      +rrow('started with',fmt(B.V0,5)+' L')
      +rrow('faucet in',fmt(B.led.faucet,5)+' L','good')
      +rrow('dropper in',fmt(B.led.dropperV,5)+' L','good')
      +rrow('drain out',fmt(B.led.drainedV,5)+' L')
      +rrow('evaporated',fmt(B.led.evaporated,5)+' L')
      +rrow('= in the beaker',fmt(B.V,5)+' L','good')
      +rrow('residual',sci(B.resid.V,2)+' L',Math.abs(B.resid.V)>1e-12?'bad':'good');
    s+=hd('saturation')
      +rrow('C = n/V',concStr(B.n>0&&B.V>0?B.n/B.V:0))
      +rrow('C<sub>sat</sub>',fmt(B.cs,2)+' mol/L')
      +rrow('saturates below',B.n>0?fmt(B.Vsat,4)+' L':'&mdash;','good')
      +rrow('evaporating gets there in',B.tSat===null?'&mdash;':fmt(B.tSat,2)+' s');
  } else if(M.U){
    const U=M.U;
    s+=hd('PhET&rsquo;s nine solutes');
    for(const r of U.rows)
      s+=rrow(r.s.html,fmt(r.s.cSat,2)+' M',r.s.id===U.here?'good':'');
    s+=hd('against the literature');
    for(const r of U.rows)
      s+=rrow(r.s.formula,fmt(r.cLit,2)+' M ('+fmt(100*r.dC,1)+' %)',
              Math.abs(r.dC)>0.1?'bad':'');
    s+=hd('molar mass')
      +rrow('worst gap, PhET vs source','5.6 &times; 10<sup>&minus;5</sup>','good');
  } else if(M.K){
    const K=M.K;
    s+=hd('the colour')
      +rrow('solution',soluteById(K.id).html)
      +rrow('path length',fmt(K.l,2)+' cm')
      +rrow('concentration',sci(K.c,3)+' mol/L')
      +rrow('illuminant',K.illumName)
      +rrow('true colour',rgbSwatch(K.here.rgb)+rgbCss(K.here.rgb),'good')
      +rrow('PhET&rsquo;s ramp',rgbSwatch(K.phetHere)+rgbCss(K.phetHere))
      +rrow('transmitted light',fmt(100*K.here.Y,PHET.DEC_T)+' %','good')
      +rrow('empty cuvette',rgbSwatch(K.white)+rgbCss(K.white));
    s+=hd('over the whole range')
      +rrow('worst channel gap',fmt(K.worst,0)+' of 255','bad')
      +rrow('at c',sci(K.worstC,3)+' mol/L')
      +rrow('PhET&rsquo;s ramp uses l','never &mdash; it has no path length in it','bad');
  }
  s+='</table><div class="note">'+roNote(M)+'</div>';
  return s;
}
function roNote(M){
  const v=M.view;
  if(v==='beaker') return 'Everything here is a mole count. The meter reads nothing when its '
    +'probe is out of the solution, and it says so rather than inventing a number. Solid '
    +'appears the instant n/V passes C<sub>sat</sub>, with no kinetics &mdash; that is '
    +'PhET&rsquo;s model, and a real solid takes its time.';
  if(v==='cuvette') return 'A = &epsilon;lc and T = 10<sup>&minus;A</sup>, both exact. The '
    +'detector reads only while the light is on and the probe spans the beam, as PhET&rsquo;s '
    +'does. &epsilon; is looked up per nanometre, never interpolated.';
  if(v==='spectrum') return 'These are PhET&rsquo;s own digitised spectra: no literature '
    +'molar absorptivity could be sourced offline here, so nothing is claimed for them '
    +'beyond that they are what the original ships. The preset wavelength is the maximum of '
    +'the curve, found by scanning it.';
  if(v==='law') return 'A is linear in both c and l, so it is the quantity worth plotting; T '
    +'is not, which is why a spectrophotometer reports A. Above about 10 mM a real solution '
    +'stops obeying the law, and every one of PhET&rsquo;s millimolar ranges runs past that.';
  if(v==='ledger') return 'The ledger is the test: what went in minus what came out is what '
    +'is there, to the last bit. The drain is the subtle one &mdash; it takes solution, so '
    +'it carries solute at the DISSOLVED concentration and leaves the solid behind.';
  if(v==='solutes') return 'PhET&rsquo;s molar masses are the literature&rsquo;s to five '
    +'decimal places. Its saturation points are within a per cent for the four whose sources '
    +'quote a room-temperature figure; the rest differ because the source&rsquo;s temperature '
    +'is not 25 &deg;C, and the table says which is which.';
  return 'PhET&rsquo;s colour is an interpolation between fixed stops. The colour beside it '
    +'is worked out: 10<sup>&minus;&epsilon;(&lambda;)lc</sup> at every nanometre, integrated '
    +'against the CIE 1931 observer, adapted so the illuminant itself is white.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='beaker') return E('<span class="hl">C = n/V</span>, &nbsp; capped at C<sub>sat</sub>, '
    +'&nbsp; solid = max(0, n &minus; V C<sub>sat</sub>)',
    'concentration is a ratio, so everything that changes either number changes it &mdash; and '
    +'when the ratio asks for more than the water can hold, the difference falls out as solid');
  if(v==='cuvette') return E('<span class="hl">A = &epsilon; l c</span>, &nbsp; '
    +'<span class="hl2">T = 10<sup>&minus;A</sup></span>',
    'the absorbance adds up along the beam while the transmittance multiplies, which is the '
    +'whole reason the logarithm is there');
  if(v==='spectrum') return E('&epsilon; = &epsilon;(&lambda;), &nbsp; '
    +'<span class="hl">&lambda;<sub>max</sub> = argmax &epsilon;</span>, &nbsp; '
    +'A(&lambda;) = &epsilon;(&lambda;) l c',
    'the law is exact at every wavelength separately; a spectrum is what you get by asking it '
    +'the same question four hundred times');
  if(v==='law') return E('<span class="hl">A = &epsilon;lc</span> &nbsp;&rArr;&nbsp; '
    +'T = 10<sup>&minus;&epsilon;lc</sup>, &nbsp; A = &minus;log<sub>10</sub>T',
    'a straight line through the origin in c and in l, and an exponential in neither &mdash; '
    +'which is why the instrument measures T and reports A');
  if(v==='ledger') return E('<span class="hl">n = in &minus; out</span>, &nbsp; '
    +'V = V<sub>0</sub> + in &minus; out, &nbsp; C = n/V',
    'a simulation of a beaker is a bookkeeping problem before it is a chemistry problem, and '
    +'the residual below is how much of the book does not balance');
  if(v==='solutes') return E('C<sub>sat</sub> = <span class="hl">s/M</span>, &nbsp; '
    +'s in g/L, &nbsp; M in g/mol',
    'a solubility quoted in grams becomes a concentration only through the molar mass, and the '
    +'temperature it was quoted at travels with it');
  return E('<span class="hl">T(&lambda;) = 10<sup>&minus;&epsilon;(&lambda;)lc</sup></span>'
    +' &nbsp;&rArr;&nbsp; X = &int;S(&lambda;)T(&lambda;)x&#772;(&lambda;) d&lambda;',
    'colour is not a property of the solute: it is what is left of the light after the '
    +'solution has taken its share, weighted by an eye');
}
function tagHTML(M){
  const v=M.view, nm=TABS.filter(t=>t[0]===v)[0][1];
  if(M.B||v==='ledger'){
    const B=M.B||M.G.B, bits=[B.sol.name];
    if(B.empty) bits.push('the beaker is empty');
    else { bits.push(volPlain(B.V)); bits.push(fmt(B.C,3)+' mol/L'); }
    if(B.sat) bits.push('saturated');
    if(!ST.running) bits.push('paused');
    return '<b>'+nm+'</b> &mdash; '+bits.join(', ');
  }
  if(M.C) return '<b>'+nm+'</b> &mdash; '+M.C.sol.name+', '+plain(blConcStr(M.C.c))
    +', '+fmt(M.C.l,2)+' cm, '+fmt(M.C.lam,0)+' nm &rarr; A = '+fmt(M.C.A,2);
  if(M.S) return '<b>'+nm+'</b> &mdash; '+soluteById(M.S.d.solute).name
    +', peak at '+fmt(M.S.lamMax,0)+' nm, cursor at '+fmt(M.S.lam,0)+' nm';
  if(M.L) return '<b>'+nm+'</b> &mdash; A = '+fmt(M.L.A,3)+', T = '+fmt(100*M.L.T,2)+' %';
  if(M.U) return '<b>'+nm+'</b> &mdash; nine solutes, PhET&rsquo;s numbers against the sources';
  if(M.K) return '<b>'+nm+'</b> &mdash; '+M.K.name+', '+fmt(M.K.l,2)+' cm, worst gap '
    +fmt(M.K.worst,0)+'/255';
  return '<b>'+nm+'</b>';
}
