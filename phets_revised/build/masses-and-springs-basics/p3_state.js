
/* ================================================================== *
 *  state, the live springs, the per-view model, readout, eqbar, tag   *
 * ================================================================== */
const TABS=[['str','the stretch'],['bnc','the bounce'],['lab','the lab'],
            ['per','the period law'],['dmp','the damping'],['eng','the energy']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', ke:'#b8ec4c', pel:'#5ac8e0', pgr:'#cd35c4',
           th:'#e8843a', tot:'#e4e8f0', coil:'#9aa4bb', mass1:'#b8ec4c', mass2:'#5ac8e0'};
const RO_W=300;
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'slow',name:'slow motion'}];
const BODY_LIST=BODIES.map(b=>({id:b.id,name:b.name}));
const HMAX=1400;                 /* history points kept per spring */
const HWIN=6.0;                  /* the longest window the strips show */
const CROSS_V=1e-3;              /* m/s: below this the spring has stopped moving */

/* PhET's own defaults: spring constant 6 N/m on both springs, 100 g on the lab's
   adjustable mass, Earth, playing, normal speed, the lines and tools as PhET
   leaves them.  The damping is PhET's per-SCREEN value (the Stretch screen sets
   0.7, Bounce and Lab 0): switching views restores it, as switching PhET's
   screens does, and the slider then moves it inside the parent sim's 0-0.7. */
const DEFAULTS={view:'str', k1:KDEF, k2:KDEF, kl:KDEF,
                mass1:'m250', mass2:'m50', labMass:'adj', massG:MASS_G_DEF,
                body:'earth', gCustom:GDEF, damping:B_STRETCH,
                running:true, speed:'normal', reveal:false,
                natLine:true, restLine:true, movLine:false, movY:0.62,
                ruler:false, rulerX:0.40, rulerY:1.44, stopwatch:false, trace:true,
                zeta:0.25, bExt:1.0, kA:KDEF, mAg:MASS_G_DEF};
const ST=Object.assign({},DEFAULTS);
const VIEW_DAMPING={str:B_STRETCH, bnc:B_BOUNCE, lab:B_LAB};

/* ---- the live springs ---------------------------------------------
   slot 0 and 1 are the two-spring screens, slot 2 is the lab.  y is the
   spring's extension below its unstretched length (m), v its rate; the
   equilibrium mg/k is recomputed from the current settings every step, so
   moving gravity or the spring constant moves the hanging point under the
   mass exactly as PhET's re-linked equilibrium does. */
function newSlot(){ return {y:0,v:0,hist:[],ht:[],cross:[],tAttach:0,last:null}; }
const LIVE={t:0, sw:0, swOn:false, slot:[newSlot(),newSlot(),newSlot()]};
function slotReset(i,t){ const s=LIVE.slot[i]; s.y=0; s.v=0; s.hist=[]; s.ht=[]; s.cross=[]; s.tAttach=t===undefined?LIVE.t:t; s.last=null; }
function liveReset(){ LIVE.t=0; LIVE.sw=0; LIVE.swOn=false; for(let i=0;i<3;i++) slotReset(i,0); }

function gOf(st){ const b=bodyById(st.body); return b.g===null?st.gCustom:b.g; }
function labMassKg(st){ const r=rackById(LAB_RACK,st.labMass); return r.m===null?st.massG/1000:r.m; }
/* the springs the current view runs: index into LIVE.slot, world x, k, mass */
function springsOf(st){
  if(st.view==='lab'||st.view==='eng'){
    const r=rackById(LAB_RACK,st.labMass);
    return [{i:2,x:SPRING_X,k:st.kl,m:labMassKg(st),myst:!!r.myst,name:r.name,label:'spring'}];
  }
  const a=rackById(RACK,st.mass1), b=rackById(RACK,st.mass2);
  return [{i:0,x:LEFT_SPRING_X,k:st.k1,m:a.m,myst:!!a.myst,name:a.name,label:'spring 1'},
          {i:1,x:RIGHT_SPRING_X,k:st.k2,m:b.m,myst:!!b.myst,name:b.name,label:'spring 2'}];
}
function liveViews(v){ return v==='str'||v==='bnc'||v==='lab'||v==='eng'; }

/* one step of one spring, by the exact propagator, with the equilibrium
   crossings recorded through the same bisection selfTest measures with */
function stepSlot(sp,g,b,dt){
  const S=LIVE.slot[sp.i];
  if(!(sp.m>0)||!(dt>0)) return;
  const ye=yEq(sp.m,sp.k,g), u0=S.y-ye, v0=S.v;
  const r=prop(sp.m,sp.k,b,u0,v0,dt);
  const u1=r[0];
  /* a crossing counts only while the spring is still visibly moving: at 1 mm/s
     the swing is sub-pixel, and the sign changes of a dying exponential would
     otherwise go on filling the trace for ever (PhET has the same threshold) */
  if(u0!==0&&u1!==0&&(u0<0)!==(u1<0)&&Math.abs(v0)>CROSS_V){
    const tc=zeroBetween(sp.m,sp.k,b,u0,v0,0,dt);
    if(isFinite(tc)){ S.cross.push(LIVE.t+tc); if(S.cross.length>8) S.cross.shift(); }
  }
  S.y=u1+ye; S.v=r[1];
}
function pushHist(sp){
  const S=LIVE.slot[sp.i];
  S.hist.push(S.y); S.ht.push(LIVE.t);
  if(S.hist.length>HMAX){ S.hist.shift(); S.ht.shift(); }
}
function advance(st,dts){
  const g=gOf(st), b=st.damping, sps=springsOf(st);
  for(const sp of sps){ if(DRAG.what===null||DRAG.sp!==sp.i) stepSlot(sp,g,b,dts); }
  LIVE.t+=dts;
  if(LIVE.swOn) LIVE.sw+=dts;
  for(const sp of sps) pushHist(sp);
}
/* the period the trace has measured: two crossings apart */
function tracedPeriod(i){
  const c=LIVE.slot[i].cross;
  return c.length>=3?c[c.length-1]-c[c.length-3]:NaN;
}

/* ---- the per-view model ------------------------------------------- */
function springModel(st,sp,g,b){
  const S=LIVE.slot[sp.i], m=sp.m, k=sp.k;
  const o={i:sp.i,x:sp.x,k:k,m:m,myst:sp.myst,name:sp.name,label:sp.label,on:m>0};
  o.ye=m>0?yEq(m,k,g):0;
  o.y=S.y; o.v=S.v; o.u=S.y-o.ye;
  o.bottom=CEILING_Y-L0-S.y;                 /* the free end of the spring, world y */
  /* the flag is about the BLOCK: that is what a reader sees crossing the floor */
  o.floorBust=m>0?(o.bottom-HOOK_C-massHeight(m)<FLOOR_Y):(o.bottom<FLOOR_Y);
  if(m>0){
    o.w0=omega0(m,k); o.T0=period0(m,k); o.gam=gammaOf(m,b); o.zeta=zetaOf(m,k,b);
    o.bc=bCrit(m,k); o.wd=omegaD(m,k,b); o.Td=periodD(m,k,b); o.ld=logDec(m,k,b); o.Q=qFactor(m,k,b);
    o.ybot=swingBottom(m,k,g);
    o.KE=keOf(m,S.v); o.PEe=peElastic(k,S.y); o.PEg=peGrav(m,g,S.y,o.ybot);
    o.E=energyU(m,k,o.u,S.v); o.off=gravOffset(m,k,g);
    o.E0=energyU(m,k,-o.ye,0);               /* released from the unstretched end */
    o.Eth=Math.max(0,o.E0-o.E);
    o.Tmeas=tracedPeriod(sp.i);
    o.hist=S.hist; o.ht=S.ht; o.cross=S.cross;
    o.mInfer=g>0?mFromStretch(k,o.ye,g):NaN;
  }
  return o;
}
function buildModel(){
  const st=ST, g=gOf(st), body=bodyById(st.body), b=st.damping;
  const M={st,view:st.view,g,body,b,t:LIVE.t,sw:LIVE.sw,swOn:LIVE.swOn,
           gReal:body.real,springs:springsOf(st).map(sp=>springModel(st,sp,g,b))};
  M.mysteryG=(st.body==='planetX'&&!st.reveal);
  M.anyMyst=M.springs.some(s=>s.myst&&!st.reveal);
  /* the analysis views, built lazily: the sweeps are the expensive part and
     three of six views never look at them */
  let _per=null,_dmp=null,_eng=null;
  Object.defineProperty(M,'per',{get(){ return _per||(_per=perModel(st,b)); }});
  Object.defineProperty(M,'dmp',{get(){ return _dmp||(_dmp=dmpModel(st)); }});
  Object.defineProperty(M,'eng',{get(){ return _eng||(_eng=engModel(st,g,b)); }});
  return M;
}
/* the period law: T(m) at four spring constants, with the period measured from
   the drawn motion at a handful of masses */
function perModel(st,b){
  const ks=[3,6,9,12], ms=[], curves=[];
  for(let i=0;i<=60;i++) ms.push((MASS_G_MIN+(MASS_G_MAX-MASS_G_MIN)*i/60)/1000);
  for(const k of ks) curves.push({k,T:ms.map(m=>period0(m,k))});
  const mk=st.mAg/1000, k=st.kA;
  const pts=[];
  for(const gm of [60,110,170,230,290]){
    const m=gm/1000;
    pts.push({m,T:measurePeriod(m,k,0,0.05),T0:period0(m,k)});
  }
  const zs=[]; for(let i=0;i<=80;i++) zs.push(i/80*0.999);
  return {ks,ms,curves,pts,m:mk,k,T0:period0(mk,k),Td:periodD(mk,k,b),zeta:zetaOf(mk,k,b),
          zs,stretch:zs.map(z=>1/Math.sqrt(1-z*z)),
          planets:BODIES.filter(x=>x.g!==null).map(x=>({name:x.name,g:x.g,ye:yEq(mk,k,x.g),T:period0(mk,k)})),
          zMaxPhet:BMAX/bCrit(MASS_G_MIN/1000,KMIN)};
}
/* the three regimes, at the current k and m, with b run past PhET's range */
function dmpModel(st){
  const m=st.mAg/1000, k=st.kA, bc=bCrit(m,k), u0=0.05;
  const T0=period0(m,k), tmax=3.2*T0, n=260, ts=[];
  for(let i=0;i<=n;i++) ts.push(tmax*i/n);
  const zlist=[{z:st.zeta,lab:'ζ = '+fmt(st.zeta,2),col:COL.pos},
               {z:1,lab:'ζ = 1 critical',col:COL.ref},
               {z:1.8,lab:'ζ = 1.8 over',col:COL.struct}];
  const curves=zlist.map(o=>({z:o.z,lab:o.lab,col:o.col,b:o.z*bc,
                              u:ts.map(t=>prop(m,k,o.z*bc,u0,0,t)[0])}));
  const gamZ=st.zeta*bc/(2*m);
  const env=ts.map(t=>u0*Math.exp(-gamZ*t));
  /* successive peaks of the underdamped curve, for the logarithmic decrement */
  const Td=periodD(m,k,st.zeta*bc), peaks=[];
  if(isFinite(Td)) for(let n2=0;n2<6;n2++){
    const t=n2*Td; peaks.push({n:n2,t,u:prop(m,k,st.zeta*bc,u0,0,t)[0]});
  }
  return {m,k,bc,u0,ts,curves,env,Td,T0,peaks,ld:logDec(m,k,st.zeta*bc),
          bPhet:BMAX,bcMin:bCrit(MASS_G_MIN/1000,KMIN),bcMax:bCrit(MASS_G_MAX/1000,KMAX),
          zMax:BMAX/bCrit(MASS_G_MIN/1000,KMIN),reach:st.zeta*bc<=BMAX+1e-12};
}
/* the energy ledger of the lab spring over three periods from its release */
function engModel(st,g,b){
  const m=labMassKg(st), k=st.kl, ye=yEq(m,k,g), T0=period0(m,k);
  const n=240, tmax=3*T0, ts=[], KE=[], PEe=[], PEg=[], TH=[], TOT=[];
  const E0=energyU(m,k,-ye,0), off=gravOffset(m,k,g), ybot=swingBottom(m,k,g);
  for(let i=0;i<=n;i++){
    const t=tmax*i/n, r=prop(m,k,b,-ye,0,t), y=r[0]+ye;
    ts.push(t); KE.push(keOf(m,r[1])); PEe.push(peElastic(k,y)); PEg.push(peGrav(m,g,y,ybot));
    const th=E0-energyU(m,k,r[0],r[1]); TH.push(th);
    TOT.push(keOf(m,r[1])+peElastic(k,y)+peGrav(m,g,y,ybot)+th);
  }
  return {m,k,g,b,ye,ybot,T0,ts,KE,PEe,PEg,TH,TOT,E0,off,base:E0+off,
          Etot:E0+off,drift:Math.max.apply(null,TOT.map(x=>Math.abs(x-(E0+off))))};
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function cmv(x,n){ return sigf(100*x,n||4)+' cm'; }
function gName(st){ const b=bodyById(st.body); return b.id==='custom'?'custom':b.name; }
function gShown(M){ return M.mysteryG?'?':fmt(M.g,1)+' m/s<sup>2</sup>'; }
function massShown(M,s){ return !s.on?'&mdash;':(s.myst&&!M.st.reveal?'?':fmt(1000*s.m,0)+' g'); }

function springRows(M,s){
  const st=M.st;
  let out=hd(s.label+' &mdash; k = '+fmt(s.k,0)+' N/m');
  out+=rrow('mass',massShown(M,s));
  if(!s.on) return out+rrow('nothing hangs on it','spring at its natural length');
  out+=rrow('resting extension m g / k',cmv(s.ye),'good');
  out+=rrow('extension now',cmv(s.y)+(s.floorBust?' (past the floor)':''),s.floorBust?'bad':'');
  out+=rrow('speed',sigf(Math.abs(s.v),3)+' m/s');
  out+=rrow('period 2&pi;&radic;(m/k)',sigf(s.T0,4)+' s','good');
  if(M.b>0) out+=rrow('damped period, &zeta; = '+fmt(s.zeta,3),isFinite(s.Td)?sigf(s.Td,4)+' s':'no oscillation');
  if(isFinite(s.Tmeas)) out+=rrow('period measured from the trace',sigf(s.Tmeas,4)+' s',Math.abs(s.Tmeas-(M.b>0?s.Td:s.T0))<1e-6?'good':'');
  if(s.myst&&!st.reveal) out+=rrow('unlabelled mass','solve m = k y / g');
  if(st.body==='planetX'&&!st.reveal) out+=rrow('unknown gravity','solve g = k y / m');
  return out;
}
function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">masses and springs<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(liveViews(M.view)&&M.view!=='eng'){
    s+=hd('gravity &mdash; '+gName(st))+rrow('g',gShown(M),'good');
    if(M.gReal!==null&&!M.mysteryG) s+=rrow('the real surface value',fmt(M.gReal,2)+' m/s<sup>2</sup> ('+(M.g>M.gReal?'&minus;':'+')+fmt(Math.abs(M.gReal-M.g),2)+')');
    if(st.body==='planetX'&&st.reveal) s+=rrow('Planet X','PhET&rsquo;s invented 14.2 m/s<sup>2</sup>');
    for(const sp of M.springs) s+=springRows(M,sp);
    s+=hd('the clock')+rrow('t',fmt(M.t,2)+' s'+(st.running?'':' (paused)'))
      +(st.speed==='slow'?rrow('slow motion','&times;1/8 (PhET)'):'');
    if(st.stopwatch) s+=rrow('stopwatch',fmt(M.sw,2)+' s'+(M.swOn?' (running)':''));
    if(st.movLine) s+=rrow('movable line',fmt(100*st.movY,1)+' cm above the floor');
  }
  else if(M.view==='per'){
    const P=M.per;
    s+=hd('the spring')+rrow('k',fmt(P.k,0)+' N/m')+rrow('m',fmt(1000*P.m,0)+' g')
      +rrow('T = 2&pi;&radic;(m/k)',sigf(P.T0,5)+' s','good')
      +rrow('damped T<sub>d</sub>, &zeta; = '+fmt(P.zeta,3),isFinite(P.Td)?sigf(P.Td,5)+' s':'no oscillation')
      +rrow('T<sub>d</sub>/T',isFinite(P.Td)?sigf(P.Td/P.T0,5):'&mdash;');
    s+=hd('measured from the motion');
    for(const p of P.pts) s+=rrow(fmt(1000*p.m,0)+' g: zeros two apart',sigf(p.T,6)+' s',Math.abs(p.T-p.T0)<1e-9?'good':'bad');
    s+=hd('gravity moves the hanging point, not the period');
    for(const pl of P.planets) s+=rrow(pl.name+', g = '+fmt(pl.g,1),cmv(pl.ye,4)+', T = '+sigf(pl.T,4)+' s');
  }
  else if(M.view==='dmp'){
    const D=M.dmp;
    s+=hd('the spring')+rrow('k, m',fmt(D.k,0)+' N/m, '+fmt(1000*D.m,0)+' g')
      +rrow('undamped period',sigf(D.T0,5)+' s')
      +rrow('critical damping 2&radic;(km)',sigf(D.bc,5)+' N s/m','good');
    s+=hd('the damping drawn')+rrow('&zeta;',fmt(st.zeta,3))
      +rrow('b = &zeta; &times; 2&radic;(km)',sigf(st.zeta*D.bc,4)+' N s/m',D.reach?'good':'bad')
      +rrow('within PhET&rsquo;s 0&ndash;0.7?',D.reach?'yes':'no &mdash; beyond its slider','')
      +rrow('damped period',isFinite(D.Td)?sigf(D.Td,5)+' s':'none')
      +rrow('log decrement &gamma;T<sub>d</sub>',isFinite(D.ld)?sigf(D.ld,5):'&mdash;')
      +rrow('amplitude kept per period',isFinite(D.ld)?sigf(Math.exp(-D.ld),4):'&mdash;');
    s+=hd('what the sim can reach')
      +rrow('2&radic;(km) over its box',sigf(D.bcMin,6)+' &ndash; '+sigf(D.bcMax,5)+' N s/m')
      +rrow('its damping tops out at',fmt(BMAX,1)+' N s/m')
      +rrow('so &zeta; never exceeds',sigf(D.zMax,6),'good')
      +rrow('every reachable state is','underdamped');
  }
  else{
    const E=M.eng, sp=M.springs[0];
    s+=hd('the run drawn')+rrow('m, k, g',fmt(1000*E.m,0)+' g, '+fmt(E.k,0)+' N/m, '+fmt(E.g,1)+' m/s<sup>2</sup>')
      +rrow('released from the unstretched end','y = 0, v = 0')
      +rrow('resting extension m g / k',cmv(E.ye),'good')
      +rrow('so it swings between','0 and '+cmv(2*E.ye))
      +rrow('starting energy &frac12;k(mg/k)<sup>2</sup>',sigf(E.E0,5)+' J','good')
      +rrow('the gravitational zero','the bottom of the swing, '+cmv(E.ybot)+' down');
    s+=hd('the ledger')+rrow('damping b',fmt(E.b,2)+' N s/m')
      +rrow('KE + PE<sub>elastic</sub> + PE<sub>gravity</sub> + E<sub>thermal</sub>',sigf(E.Etot,6)+' J','good')
      +rrow('&hellip; drift over three periods',sigf(E.drift,2)+' J',E.drift<1e-12?'good':'bad')
      +rrow('the constant 3(mg)<sup>2</sup>/2k',sigf(E.off,5)+' J');
    if(sp&&sp.on) s+=hd('the live spring')+rrow('KE',sigf(sp.KE,4)+' J')+rrow('PE elastic',sigf(sp.PEe,4)+' J')
      +rrow('PE gravity',sigf(sp.PEg,4)+' J')+rrow('thermal so far',sigf(sp.Eth,4)+' J');
  }
  s+='</table><div class="note">PhET&rsquo;s values (spring 3&ndash;12 N/m, masses 50&ndash;300 g, Moon 1.6, Earth 9.8, Planet X 14.2, '
    +'Jupiter 24.8 m/s<sup>2</sup>, damping 0&ndash;0.7 N s/m) are read from its build 1.0.28; the real surface gravities are 1.62, 9.81 and '
    +'24.79. Everything else is exact and pinned in selfTest to derive.py.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='str') return E('<span class="hl">F = &minus;k y</span> &nbsp;&rArr;&nbsp; <span class="hl">y<sub>eq</sub> = m g / k</span>',
    'the spring pulls back in proportion to its stretch, so it stops where the pull equals the weight: twice the mass is twice the stretch, twice the stiffness is half');
  if(M.view==='bnc') return E('<span class="hl">m &#375; + b &#7823; + k y = m g</span> &nbsp;&middot;&nbsp; y = y<sub>eq</sub> + u, &nbsp; <span class="hl">m &uuml; + b &#361; + k u = 0</span>',
    'gravity only moves the resting point; about it the motion is the plain harmonic oscillator, so letting go from the unstretched end swings exactly 2mg/k');
  if(M.view==='lab') return E('<span class="hl">T = 2&pi;&radic;(m/k)</span> &nbsp;&middot;&nbsp; y<sub>eq</sub> = m g / k',
    'the period holds the mass and the spring and nothing else: the same spring beats the same time on the Moon, on Jupiter and on Planet X');
  if(M.view==='per') return E('<span class="hl">T<sub>d</sub> = 2&pi;/&radic;(k/m &minus; (b/2m)<sup>2</sup>) = T/&radic;(1 &minus; &zeta;<sup>2</sup>)</span>',
    'damping lengthens the period, and only at second order: at PhET&rsquo;s stiffest and heaviest it is 1.7 % longer, at its softest and lightest 2.34 times');
  if(M.view==='dmp') return E('<span class="hl">&zeta; = b/(2&radic;(km))</span> &nbsp;&middot;&nbsp; <span class="rm">&zeta; &lt; 1 oscillates, &zeta; = 1 critical, &zeta; &gt; 1 crawls back</span>',
    'the whole behaviour of a damped spring is one number; PhET&rsquo;s own ranges keep it below 0.904, so nothing it can draw is critically damped');
  return E('<span class="hl">E = &frac12;mv<sup>2</sup> + &frac12;ku<sup>2</sup></span> &nbsp;&middot;&nbsp; <span class="hl">dE/dt = &minus;b v<sup>2</sup></span> &nbsp;&middot;&nbsp; KE + PE<sub>el</sub> + PE<sub>gr</sub> = E &minus; (mg)<sup>2</sup>/2k',
    'the damper is the only leak, and it takes energy at bv&sup2;: with none, the three stores add to a constant for ever');
}
function tagHTML(M){
  const st=M.st;
  const mm=M.springs.map(s=>s.on?(s.myst&&!st.reveal?'?':fmt(1000*s.m,0)+' g'):'empty').join(' / ');
  if(M.view==='str') return '<b>the stretch</b> &mdash; '+mm+' on k = '+fmt(st.k1,0)+' / '+fmt(st.k2,0)+' N/m, '+gName(st)+', damping '+fmt(M.b,2);
  if(M.view==='bnc') return '<b>the bounce</b> &mdash; '+mm+', damping '+fmt(M.b,2)+' N s/m'+(st.running?'':', paused')+(st.speed==='slow'?', slow motion':'');
  if(M.view==='lab') return '<b>the lab</b> &mdash; '+mm+' on k = '+fmt(st.kl,0)+' N/m, '+gName(st)+(M.mysteryG?' (g hidden)':'');
  if(M.view==='per') return '<b>the period law</b> &mdash; T = 2&pi;&radic;(m/k), measured against the closed form';
  if(M.view==='dmp') return '<b>the damping</b> &mdash; &zeta; = '+fmt(st.zeta,2)+(M.dmp.reach?' (inside PhET&rsquo;s range)':' (beyond PhET&rsquo;s range)');
  return '<b>the energy</b> &mdash; three periods from the unstretched end, damping '+fmt(M.b,2);
}
