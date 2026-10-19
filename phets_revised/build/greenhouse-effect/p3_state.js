
/* ================================================================== *
 *  state: two atmospheres (PhET's twelve-sheet concentration model    *
 *  and its three-sheet layer model), their thermal clocks, the photon *
 *  population, the per-view model, the readout, the equation bar and  *
 *  the tag                                                            *
 * ================================================================== */
const TABS=[['waves','the waves'],['photons','the photons'],['layers','the layers'],
            ['ladder','the ladder'],['record','the record']];
const SKY_VIEWS={waves:1, photons:1, layers:1};
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c',
           sun:'#f6d365', ir:'#e8583a', sky0:'#050a18', sky1:'#0d1b33',
           ground:'#2f6b34', glacier:'#cfe3ef', cloud:'#9fb0c4', sheet:'#5ac8e0'};
const RO_W=300;
/* the house #hint sits at bottom:11px on top of the last line of a caption anchored at
   H - 12, so every caption here ends HINT_H higher (build/wave-on-a-string/, Known-bad) */
const HINT_H=18;

const MODE_LIST=[{id:'value',name:'by concentration'},{id:'date',name:'by date'}];
const UNIT_LIST=[{id:'K',name:'kelvin'},{id:'C',name:'celsius'},{id:'F',name:'fahrenheit'}];
const DATE_LIST=DATES.map(d=>({id:d.id,name:d.name}));

const DEFAULTS={view:'waves',
  mode:'value', conc:0.5, date:'y1750', cloud:false, unit:'C',
  nLayers:1, absorb:1.0, intensity:1.0, albedo:GH.ALB_LM,
  balance:true, flux:false, sheets:true, morePhotons:false,
  sun:true, running:true, kirch:false};
const ST=Object.assign({},DEFAULTS);

/* PhET's flux-meter sensor, draggable up and down the window */
const PROBE={z:20000};
const PROBE0={z:20000};
const DRAG={what:null};

/* the two thermal states, one per PhET screen family */
const TH={conc:makeThermal(GH.N_CONC,GH.TMIN_NIGHT), lm:makeThermal(GH.N_LM,GH.TMIN_LM)};
/* the photon population (the concentration screens and the layer model share the drawing) */
const PH={list:[], rng:makeRng(20260921), acc:{vis:0,ir:0}, nVis:0, nIr:0,
          emitted:0, escaped:0, returned:0, crossings:0, absorbed:0, up:0};
const PHOTON_SPEED=9000;                 /* GreenhouseEffectConstants.SPEED_OF_LIGHT, m/s */
const PHOTON_SEED=20260921;

function resetPhotons(){
  PH.list.length=0; PH.rng.seed(PHOTON_SEED);
  PH.acc.vis=0; PH.acc.ir=0; PH.nVis=0; PH.nIr=0;
  PH.emitted=0; PH.escaped=0; PH.returned=0; PH.crossings=0; PH.absorbed=0; PH.up=0;
}
function resetThermal(){
  TH.conc=makeThermal(GH.N_CONC,GH.TMIN_NIGHT); TH.lm=makeThermal(GH.N_LM,GH.TMIN_LM);
  resetPhotons();
}

/* ---- which atmosphere is on show, and what drives it --------------------- */
function currentDate(){ return DATES.find(d=>d.id===ST.date)||DATES[1]; }
function concNow(){ return ST.mode==='date'?currentDate().c:ST.conc; }
/* PhET switches the ground to its glaciated albedo only for the ice age BY DATE */
function concAlbedo(){ return (ST.mode==='date'&&currentDate().glacier)?GH.ALB_GLACIER:GH.ALB_MEADOW; }
function cloudOn(){ return ST.mode==='date'?true:ST.cloud; }
/* PhET forces the cloud on in by-date mode only as a control-enabling rule; the cloud itself
   is only in the model when the user has asked for it, which here is the checkbox alone. */
/* the number of sheets is a COUNT: the slider's step is 1, but a headless harness can put
   1.5 in it, and new Array(1.5) is a RangeError rather than a rounding error */
function nSheets(){ return Math.max(0,Math.min(GH.N_LM,Math.round(ST.nLayers))); }
function atmosphere(){
  if(ST.view==='layers'){
    const alt=layerAltitudes(GH.N_LM), a=[], nA=nSheets();
    for(let i=0;i<GH.N_LM;i++) a.push(i<nA?ST.absorb:0);
    const F=ST.sun?(1-ST.albedo)*GH.S_SUN*ST.intensity:0;
    return {kind:'lm', a, alt, F, albedo:ST.albedo, floor:GH.TMIN_LM, th:TH.lm,
            n:GH.N_LM, nActive:nA, hold:GH.PHOTON_HOLD_LM,
            Sin:ST.sun?GH.S_SUN*ST.intensity:0, cloud:false};
  }
  const c=concNow(), alb=concAlbedo(), a=concAbsorbance(c,GH.N_CONC);
  const S=ST.sun?GH.S_SUN:0;
  const Safter=S*(ST.cloud?1-CLOUD_REFL:1);
  return {kind:'conc', a, alt:layerAltitudes(GH.N_CONC), F:(1-alb)*Safter, albedo:alb,
          floor:GH.TMIN_NIGHT, th:TH.conc, n:GH.N_CONC, nActive:GH.N_CONC,
          hold:GH.PHOTON_HOLD_CONC, conc:c, Sin:S, Safter, cloud:ST.cloud};
}
/* an atmosphere with the sheets that are actually absorbing, for the solver: an inactive
   layer-model sheet (a = 0) is transparent and radiates nothing, so it simply is not there */
function activeAbs(A){ return A.a.filter(x=>x>0); }

/* ---- the clock ---------------------------------------------------------- */
function stepFrame(){
  if(!ST.running||!SKY_VIEWS[ST.view]) return false;
  const A=atmosphere();
  marchFrame(A.th,A.a,A.F,ST.sun?A.floor:A.floor,FRAME_DT,SUBSTEPS);
  if(ST.view==='photons') stepPhotons(A,FRAME_DT);
  return true;
}
function settle(){
  const A=atmosphere(), s=solveClosed(activeAbs(A),A.F);
  if(!ST.sun){ A.th.Tg=A.floor; A.th.T=A.th.T.map(()=>0); return; }
  A.th.Tg=Math.max(s.Tg,A.floor);
  let k=0;
  A.th.T=A.a.map(x=>x>0?s.Tlayer[k++]:0);
}

/* ---- the photons (PhET's own rules; a display, not the energy model) ----- */
function stepPhotons(A,dt){
  const R=PH.rng, half=GH.SPAN_W/2;
  /* sunlight: PhET creates 10 x intensity per second and draws one in five */
  const visRate=ST.sun?GH.VIS_RATE*(A.kind==='lm'?ST.intensity:1):0;
  PH.acc.vis+=visRate*dt;
  while(PH.acc.vis>=1){
    PH.acc.vis-=1;
    PH.list.push({x:(R.next()-0.5)*GH.SPAN_W, y:GH.TOP, vx:0, vy:-PHOTON_SPEED,
                  ir:false, hold:0, show:(PH.nVis%GH.SHOW_ONE_IN)===0});
    PH.nVis++;
  }
  /* infrared from the ground: PhET's sigma T^4 / 7.8 per second, one in five drawn */
  const irRate=irPhotonRate(A.th.Tg,A.floor);
  PH.acc.ir+=irRate*dt;
  while(PH.acc.ir>=1){
    PH.acc.ir-=1;
    const ang=(R.next()-0.5)*PI/8;
    PH.list.push({x:(R.next()-0.5)*GH.SPAN_W, y:0,
                  vx:PHOTON_SPEED*Math.sin(ang), vy:PHOTON_SPEED*Math.cos(ang),
                  ir:true, hold:0, show:(PH.nIr%GH.SHOW_ONE_IN)===0});
    PH.nIr++; PH.emitted++;
  }
  const keep=[];
  for(const p of PH.list){
    if(p.hold>0){                                   /* held inside a sheet */
      p.hold-=dt;
      if(p.hold<=0){
        /* PhET re-emits up or down at even odds; the lateral jump is its own decoration */
        const up=R.next()<0.5;
        PH.absorbed++; if(up) PH.up++;
        const ang=(R.next()-0.5)*PI/4;
        p.vy=(up?1:-1)*PHOTON_SPEED*Math.cos(ang);
        p.vx=PHOTON_SPEED*Math.sin(ang);
      }
      keep.push(p); continue;
    }
    const y0=p.y;
    p.x+=p.vx*dt; p.y+=p.vy*dt;
    if(p.x>GH.SPAN_W/2) p.x-=GH.SPAN_W;
    if(p.x<-GH.SPAN_W/2) p.x+=GH.SPAN_W;
    if(!p.ir){
      if(A.cloud&&y0>GH.CLOUD_Y&&p.y<=GH.CLOUD_Y&&Math.abs(p.x-GH.CLOUD_X)<GH.CLOUD_W/2
         &&R.next()<CLOUD_REFL*GH.SPAN_W/GH.CLOUD_W){ p.vy=-p.vy; keep.push(p); continue; }
      if(p.y<=0){
        if(R.next()<A.albedo){ p.y=0; p.vy=-p.vy; keep.push(p); }   /* reflected */
        continue;                                                   /* else absorbed */
      }
      if(p.y<GH.TOP+1||p.vy<0) keep.push(p);
      continue;
    }
    /* infrared: a sheet crossed is a chance to be absorbed */
    let gone=false;
    for(let i=0;i<A.a.length;i++){
      const z=A.alt[i];
      if(A.a[i]<=0) continue;
      if((y0<z&&p.y>=z)||(y0>z&&p.y<=z)){
        PH.crossings++;
        if(R.next()<=A.a[i]){ p.y=z; p.hold=A.hold; p.vx=0; p.vy=0; }
        break;
      }
    }
    if(p.y>=GH.TOP&&p.vy>0){ PH.escaped++; gone=true; }
    if(p.y<0){ PH.returned++; gone=true; }
    if(!gone) keep.push(p);
  }
  PH.list=keep.slice(0,1400);
}

/* a big, cached Monte Carlo of the same walk, so the panel can put a measured escape
   fraction beside the exact one (the live population is far too small and far too
   transient to be a statistic) */
const MC_CACHE={};
function mcFor(a,m,seed){
  const key=a.map(x=>x.toFixed(6)).join(',')+'|'+m+'|'+seed;
  if(!MC_CACHE[key]) MC_CACHE[key]=escapeMonteCarlo(a,m,seed);
  return MC_CACHE[key];
}

/* ---- the models --------------------------------------------------------- */
function skyModel(){
  const A=atmosphere(), aa=activeAbs(A), s=solveClosed(aa,A.F);
  const live=fluxesNow(A.th,A.a);
  const M={A, s, live, a:A.a, alt:A.alt, F:A.F, albedo:A.albedo,
           Tg:A.th.Tg, Tlayer:A.th.T.slice(), Tsteady:s.Tg, t:A.th.t,
           Teff:teff(A.F), esc:s.esc, sum:s.sum,
           net:A.F-live.U[A.a.length]+live.D[A.a.length],
           Utop:live.U[A.a.length], Dg:live.D[0],
           res:balanceResiduals(s),
           warming:s.Tg-teff(A.F)};
  /* the steady-state profile on the full sheet list (inactive sheets keep a null) */
  let k=0;
  M.Ssteady=A.a.map(x=>x>0?s.Tlayer[k++]:null);
  k=0;
  M.Skirch=A.a.map(x=>x>0?s.Tkirch[k++]:null);
  /* two flux profiles over the same levels: the LIVE one (what the sheets are radiating
     right now, which is what the meter and its sensor read, as PhET's do) and the exact
     steady one (the reference the panel draws beside it).  They coincide to machine
     precision once the model has settled, which selfTest asserts. */
  M.Ul=live.U.slice(); M.Dl=live.D.slice();
  M.Us=[]; M.Ds=[];
  { let j=0;
    M.Us.push(s.U[0]); M.Ds.push(s.D[0]);
    for(let i=0;i<A.a.length;i++){ if(A.a[i]>0) j++; M.Us.push(s.U[j]); M.Ds.push(s.D[j]); } }
  /* the flux-meter sensor: the exact fluxes at the altitude the probe sits at.  The profiles
     are piecewise constant between sheets, so the index is the number of sheets below it. */
  { let i=0;
    while(i<A.alt.length&&PROBE.z>=A.alt[i]) i++;
    const Safter=A.Safter===undefined?A.Sin:A.Safter;
    const visDown=(A.cloud&&PROBE.z>GH.CLOUD_Y)?A.Sin:Safter;
    M.probe={z:PROBE.z, i, U:M.Ul[i], D:M.Dl[i], net:M.Ul[i]-M.Dl[i],
             Us:M.Us[i], Ds:M.Ds[i], visDown, visUp:Safter*A.albedo}; }
  if(ST.view==='photons'){
    M.mc=mcFor(aa,20000,12345);
    M.pExact=escapeMarkov(aa);
    M.photons=PH.list.filter(p=>ST.morePhotons||p.show);
    M.counts={emitted:PH.emitted, escaped:PH.escaped, returned:PH.returned,
              crossings:PH.crossings, absorbed:PH.absorbed, up:PH.up,
              live:PH.list.length, drawn:M.photons.length};
    M.irRate=irPhotonRate(A.th.Tg,A.floor);
  }
  return M;
}
function ladderModel(){
  const F=(1-GH.ALB_MEADOW)*GH.S_SUN, T0=teff(F);
  const black=[];
  for(let n=0;n<=12;n++) black.push({n, T:solveClosed(new Array(n).fill(1),F).Tg,
                                        law:Math.pow(n+1,0.25)*T0});
  const curves=[];
  for(const n of [1,2,3,12]){
    const pts=[];
    for(let k=0;k<=100;k++){
      const a=k/100;
      pts.push([a,solveClosed(new Array(n).fill(a),F).Tg]);
    }
    curves.push({n,pts});
  }
  /* "the stack you have loaded" is the LAYER MODEL's, not whatever atmosphere() would
     hand back for this view: the ladder's two sliders are the layer model's two sliders,
     and reading the concentration stack here made the absorbance slider do nothing. */
  const aa=new Array(nSheets()).fill(ST.absorb);
  const Fl=(1-ST.albedo)*GH.S_SUN*ST.intensity;
  const here=solveClosed(aa,Fl);
  /* the equivalent uniform absorbance of whatever stack is loaded: the a with the same sum */
  const nEq=Math.max(aa.length,1);
  const aEq=aa.length?2*here.sum/(nEq+here.sum):0;
  /* what the real atmosphere is worth in these terms: sigma Ts^4 / F = 1 + Sigma, so the
     Earth's own Sigma is (288/254.578)^4 - 1, which one sheet reaches at a = 2S/(1+S) */
  const eT0=teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4);
  const eSum=Math.pow(EARTH_TSURF/eT0,4)-1;
  /* the marker belongs ON the plotted family, which is drawn at PhET's own F (albedo 0.2,
     one sun); `here` is the same stack at whatever albedo and intensity the layer model is
     set to, and the readout prints that one.  Two different questions, two numbers. */
  const hereCurveT=solveClosed(aa,F).Tg;
  return {F, T0, black, curves, here, hereCurveT, nHere:aa.length, aEq,
          earth:{T0:eT0, Ts:EARTH_TSURF, sum:eSum},
          earthEqA:2*eSum/(1+eSum),
          n:aa.length, a:ST.absorb};
}
function recordModel(){
  const rows=DATES.map(d=>{
    const alb=d.glacier?GH.ALB_GLACIER:GH.ALB_MEADOW;
    const F=(1-alb)*GH.S_SUN, a=concAbsorbance(d.c,GH.N_CONC);
    const s=solveClosed(a,F);
    return {d, alb, F, a, s, Ts:s.Tg};
  });
  const curve=[];
  for(let k=0;k<=120;k++){
    const c=k/120;
    curve.push([c,solveClosed(concAbsorbance(c,GH.N_CONC),(1-GH.ALB_MEADOW)*GH.S_SUN).Tg]);
  }
  const curveCloud=[];
  for(let k=0;k<=120;k++){
    const c=k/120;
    curveCloud.push([c,solveClosed(concAbsorbance(c,GH.N_CONC),
                                   (1-GH.ALB_MEADOW)*GH.S_SUN*(1-CLOUD_REFL)).Tg]);
  }
  const base=rows[1].Ts;
  /* what the ice age WOULD be on the plotted curve, i.e. over a green meadow: the gap is
     the whitening of the ground, and the view draws it as a connector rather than giving
     the point a second colour the legend would have to reuse */
  const iceOnCurve=solveClosed(concAbsorbance(rows[0].d.c,GH.N_CONC),
                               (1-GH.ALB_MEADOW)*GH.S_SUN).Tg;
  return {rows, curve, curveCloud, iceOnCurve,
          dIce:rows[0].Ts-base, d2020:rows[3].Ts-base,
          hottest:solveClosed(concAbsorbance(1,GH.N_CONC),(1-GH.ALB_MEADOW)*GH.S_SUN).Tg,
          coldest:teff((1-GH.ALB_GLACIER)*GH.S_SUN*(1-CLOUD_REFL)),
          earthTs:EARTH_TSURF, earthTeff:teff((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4),
          here:concNow()};
}
function buildModel(){
  const view=ST.view, M={view, unit:ST.unit};
  if(SKY_VIEWS[view]) M.S=skyModel();
  else if(view==='ladder') M.L=ladderModel();
  else M.R=recordModel();
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function tstr(K,unit,nd){
  if(!isFinite(K)) return '—';
  return fmt(tempIn(K,unit),nd===undefined?2:nd)+' '+UNIT_SYM[unit];
}
function signed(x,nd){ return (x>=-Math.pow(10,-(nd||2))/2?'+':'&minus;')+fmt(Math.abs(x),nd===undefined?2:nd); }
function dK(x,unit,nd){
  /* a temperature DIFFERENCE: kelvin and celsius are the same size, fahrenheit is 9/5 */
  const v=unit==='F'?x*9/5:x;
  return (v>=0?'+':'&minus;')+fmt(Math.abs(v),nd===undefined?2:nd)+' '+(unit==='F'?'°F':'K');
}
function wm2(x,nd){ return fmt(x,nd===undefined?2:nd)+' W/m&sup2;'; }
function readoutHTML(M){
  const u=M.unit;
  let s='<div class="rname">greenhouse effect<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.S){
    const S=M.S;
    s+=hd(S.A.kind==='lm'?'the layer model':'the atmosphere')
      +rrow('surface temperature',tstr(S.Tg,u),'good')
      +rrow('steady state, exact',tstr(S.Tsteady,u))
      +rrow('bare rock T<sub>eff</sub>',tstr(S.Teff,u))
      +rrow('greenhouse warming',dK(S.Tsteady-S.Teff,u),'good');
    s+=hd('energy, per square metre')
      +rrow('sunlight reaching the top',wm2(S.A.Sin))
      +(S.A.cloud?rrow('reflected by the cloud',wm2(S.A.Sin*CLOUD_REFL),'bad'):'')
      +rrow('reflected by the ground',wm2(S.A.Safter!==undefined?S.A.Safter*S.albedo:S.A.Sin*S.albedo),'bad')
      +rrow('absorbed, F',wm2(S.F),'good')
      +rrow('leaving the top now',wm2(S.Utop))
      +rrow('net in &minus; out',wm2(S.net),Math.abs(S.net)<0.5?'good':'bad')
      +rrow('back radiation at the ground',wm2(S.Dg))
      +rrow('escape chance of an IR photon',fmt(100*S.esc,2)+' %');
    if(S.A.kind==='conc'){
      const c=S.A.conc;
      s+=hd('greenhouse gas')
        +rrow('concentration c',fmt(c,4)+(ST.mode==='date'?' ('+currentDate().name+')':''))
        +rrow('lowest sheet a<sub>1</sub>',fmt(S.a[0],4))
        +rrow('&Sigma; a/(2&minus;a)',fmt(S.sum,5),'good')
        +rrow('surface albedo',fmt(S.albedo,3));
      if(ST.mode==='date'){ const d=currentDate();
        s+=rrow('CO<sub>2</sub>',d.co2+' ppm')+rrow('CH<sub>4</sub>',d.ch4+' ppb')
          +rrow('N<sub>2</sub>O',d.n2o+' ppb'); }
    } else {
      s+=hd('the sheets')
        +rrow('absorbing sheets',S.A.nActive+' of '+GH.N_LM)
        +rrow('absorbance a',fmt(ST.absorb,3))
        +rrow('&Sigma; a/(2&minus;a)',fmt(S.sum,5),'good')
        +rrow('solar intensity',fmt(100*ST.intensity,0)+' % of our sun')
        +rrow('surface albedo',fmt(ST.albedo,3));
      for(let i=S.a.length-1;i>=0;i--) if(S.a[i]>0)
        s+=rrow('sheet '+(i+1)+' at '+fmt(S.alt[i]/1000,1)+' km',
                tstr(ST.kirch?S.Skirch[i]:S.Ssteady[i],u));
    }
    if(M.view==='photons'&&S.mc){
      s+=hd('the photon walk')
        +rrow('escape chance, exact',fmt(100*S.pExact,3)+' %','good')
        +rrow('measured, '+S.mc.m+' walks',fmt(100*S.mc.p,3)+' %')
        +rrow('re-emitted upward',fmt(100*S.mc.up/Math.max(S.mc.absorbed,1),2)+' %')
        +rrow('photons alive, drawn',S.counts.live+', '+S.counts.drawn)
        +rrow('IR photons per second',fmt(S.irRate,1));
    }
    s+=hd('the flux sensor, drag it')
      +rrow('altitude',fmt(S.probe.z/1000,2)+' km')
      +rrow('infrared up',wm2(S.probe.U),'good')
      +rrow('infrared down',wm2(S.probe.D))
      +rrow('net infrared up',wm2(S.probe.net))
      +rrow('up at the steady state',wm2(S.probe.Us))
      +rrow('sunlight down',wm2(S.probe.visDown));
    s+=hd('the solve')
      +rrow('worst sheet residual',S.res.layer.toExponential(1)+' W/m&sup2;','good')
      +rrow('top of atmosphere',S.res.toa.toExponential(1)+' W/m&sup2;','good')
      +rrow('net flux constant to',S.res.net.toExponential(1)+' W/m&sup2;','good');
  } else if(M.L){
    const L=M.L;
    s+=hd('the law')
      +rrow('bare rock T<sub>eff</sub>',tstr(L.T0,u))
      +rrow('N = 1 black sheet',tstr(L.black[1].T,u))
      +rrow('N = 2',tstr(L.black[2].T,u))
      +rrow('N = 3',tstr(L.black[3].T,u))
      +rrow('N = 12',tstr(L.black[12].T,u));
    s+=hd('the stack you have loaded')
      +rrow('absorbing sheets',L.nHere)
      +rrow('&Sigma; a/(2&minus;a)',fmt(L.here.sum,5),'good')
      +rrow('surface temperature',tstr(L.here.Tg,u),'good')
      +rrow('equivalent uniform a',fmt(L.aEq,4));
    s+=hd('the real Earth')
      +rrow('S<sub>0</sub>/4, albedo 0.30',wm2((1-EARTH_ALBEDO)*SOLAR_CONSTANT/4))
      +rrow('T<sub>eff</sub>',tstr(L.earth.T0,u))
      +rrow('observed surface',tstr(L.earth.Ts,u))
      +rrow('one black sheet would give',tstr(Math.pow(2,0.25)*L.earth.T0,u),'bad');
  } else {
    const R=M.R;
    s+=hd('PhET&rsquo;s four dates');
    for(const r of R.rows) s+=rrow(r.d.name+' (c = '+fmt(r.d.c,4)+')',tstr(r.Ts,u),
                                   r.d.id===ST.date&&ST.mode==='date'?'good':'');
    s+=hd('the differences')
      +rrow('ice age &minus; 1750',dK(R.dIce,u),'bad')
      +rrow('2020 &minus; 1750',dK(R.d2020,u),'good')
      +rrow('observed LGM anomaly','&minus;6 K')
      +rrow('observed 1750&ndash;2020','+1.2 K');
    s+=hd('against the real Earth')
      +rrow('PhET&rsquo;s 1750 surface',tstr(R.rows[1].Ts,u))
      +rrow('the real Earth',tstr(R.earthTs,u))
      +rrow('offset',dK(R.rows[1].Ts-R.earthTs,u),'bad')
      +rrow('hottest reachable',tstr(R.hottest,u))
      +rrow('PhET&rsquo;s thermometer maximum',tstr(GH.T_MAX_EXPECTED,u));
  }
  s+='</table><div class="note">'+roNote(M)+'</div>';
  return s;
}
function roNote(M){
  const v=M.view;
  if(v==='waves') return 'The waves are drawn, not solved: the brightness of each band is the flux the exact solve carries at that height. PhET&rsquo;s twelve sheets sit at multiples of 50/13 km with a = 0.85 c e<sup>&minus;z/8400&nbsp;m</sup> &mdash; PhET&rsquo;s fit, not a radiative-transfer calculation.';
  if(v==='photons') return 'The photons ARE simulated, with PhET&rsquo;s rules and a seeded generator &mdash; but as in PhET they are a display: the temperature comes from the flux model, not from the photon count. The escape chance they measure is the flux ratio F/&sigma;T<sub>s</sub><sup>4</sup>.';
  if(v==='layers') return 'PhET&rsquo;s Layer Model screen. A sheet absorbs a fraction a of the infrared crossing it and radiates a full &sigma;T<sup>4</sup> each way &mdash; PhET&rsquo;s convention, not Kirchhoff&rsquo;s law. It changes no flux at all; it changes every sheet temperature by exactly a<sup>&minus;1/4</sup>, which the tick box shows.';
  if(v==='ladder') return 'Every screen of this sim obeys one line: &sigma;T<sub>s</sub><sup>4</sup> = F[1 + &Sigma; a<sub>i</sub>/(2&minus;a<sub>i</sub>)]. Fully absorbing sheets make it (N+1), and the famous fourth root follows.';
  return 'The concentrations, the 0.85 and the 8400 m are PhET&rsquo;s fit. The temperatures are this file&rsquo;s exact solve of them. PhET tuned the DIFFERENCES between its dates, not the absolute level.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='waves') return E('<span class="hl">&sigma;T<sub>s</sub><sup>4</sup> = F[1 + &Sigma;<sub>i</sub> a<sub>i</sub>/(2 &minus; a<sub>i</sub>)]</span>, &nbsp; F = (1 &minus; &alpha;)S',
    'sunlight goes straight through the greenhouse gas and warms the ground; the infrared the ground sends back does not, and every sheet that catches it sends half of it down again');
  if(v==='photons') return E('P(escape) = <span class="hl">F / &sigma;T<sub>s</sub><sup>4</sup></span> = 1 / [1 + &Sigma;<sub>i</sub> a<sub>i</sub>/(2 &minus; a<sub>i</sub>)]',
    'one photon at a time: absorbed with probability a on crossing a sheet, then sent up or down at even odds &mdash; the chance it ever reaches space is exactly the flux ratio');
  if(v==='layers') return E('2&sigma;T<sub>i</sub><sup>4</sup> = a<sub>i</sub>(U<sub>i&minus;1</sub> + D<sub>i</sub>) &nbsp;&rArr;&nbsp; <span class="hl">U<sub>i</sub> = U<sub>i&minus;1</sub> &minus; F&thinsp;a<sub>i</sub>/(2 &minus; a<sub>i</sub>)</span>',
    'each sheet absorbs what crosses it and radiates the same amount away, half up and half down, so the net upward flux is the same at every height and only the upward flux steps down');
  if(v==='ladder') return E('<span class="hl">T<sub>s</sub> = T<sub>eff</sub>[1 + N a/(2 &minus; a)]<sup>1/4</sup></span> &nbsp;&rarr;&nbsp; <span class="hl2">T<sub>eff</sub>(N+1)<sup>1/4</sup></span> at a = 1',
    'the whole model in one line: a stack of black sheets multiplies the outgoing flux by N + 1, and the fourth root is why ten sheets are not ten times hotter');
  return E('a<sub>i</sub> = <span class="hl2">0.85</span>&thinsp;c&thinsp;e<sup>&minus;z<sub>i</sub>/8400 m</sup>, &nbsp; c = 0.625 / 0.7147 / 0.7182 / 0.7446 &nbsp;&rarr;&nbsp; <span class="hl">T<sub>s</sub></span>',
    'PhET&rsquo;s fit on the left, this file&rsquo;s exact solve on the right &mdash; the numbers in the middle are a teaching choice, and the page says so');
}
function tagHTML(M){
  const v=M.view, nm=TABS.find(t=>t[0]===v)[1];
  if(M.S){
    const S=M.S;
    let bits=[];
    if(S.A.kind==='conc') bits.push(ST.mode==='date'?currentDate().name:'c = '+fmt(S.A.conc,3));
    else bits.push(S.A.nActive+' sheet'+(S.A.nActive===1?'':'s')+', a = '+fmt(ST.absorb,2));
    bits.push('surface '+tstr(S.Tg,M.unit,1));
    if(!ST.sun) bits.push('the sun is off');
    else if(Math.abs(S.Tg-S.Tsteady)>0.05) bits.push('still settling');
    else bits.push('in balance');
    if(!ST.running) bits.push('paused');
    return '<b>'+nm+'</b> &mdash; '+bits.join(', ');
  }
  if(M.L) return '<b>'+nm+'</b> &mdash; T<sub>s</sub> = T<sub>eff</sub>[1 + &Sigma; a/(2&minus;a)]<sup>1/4</sup>, exact';
  return '<b>'+nm+'</b> &mdash; PhET&rsquo;s fit, solved exactly';
}
