
/* ================================================================== *
 *  state: PhET's four screens as four scene views (each with its own   *
 *  cannon, projectiles, target, clock), two analysis views, the per-   *
 *  view model, the readout, the equation bar and the tag               *
 * ================================================================== */
const TABS=[['intro','the launch'],['vectors','the vectors'],['drag','the drag'],['lab','the lab'],
            ['env','the envelope'],['hodo','the hodograph']];
const SCENE_VIEWS=['intro','vectors','drag','lab'];
function isScene(v){ return SCENE_VIEWS.indexOf(v)>=0; }
const PFX={intro:'i_',vectors:'v_',drag:'d_',lab:'l_',env:'a_',hodo:'a_'};
/* role colours: green = the computed path and velocity, orange = the vacuum
   reference and the target, magenta = the live marker and the derived-
   secondary (acceleration, the energy the air takes), cyan = structure (the
   cannon, the ground, the probe), white = force, gold = the tape and stars */
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', force:'#e9e9f0',
           tape:'#d9b44a', star:'#e8c24a', ground:'#0c1422', groundLine:'#35566b', edge:'#242a3a',
           cannon:'#39404f', cannon2:'#566077', sky:'#070b18'};
const RO_W=300, FRAME_DT=1/60;
const ANALYSIS_OBJS=OBJECTS.map(o=>({id:o.id,name:o.name})).concat([{id:'sphere',name:'the 5-kg sphere'}]);

/* PhET's per-screen defaults (Intro: pumpkin, 10 m, 0 deg, 15 m/s, no air;
   Vectors and Drag: the 5-kg, 0.8-m, C_d 0.47 sphere with air, 0 m, 80 deg,
   18 m/s; Lab: cannonball, no air, 0 m, 80 deg, 18 m/s).  Two departures,
   both so a view shows its subject at load: the Vectors view starts with
   velocity and acceleration on and strobes them along the shot, and the
   analysis views start on a baseball at 30 m/s with the air on. */
const DEFAULTS={
  view:'intro', zoom:1, speed:'normal', running:true, tape:false, probe:false, vacRef:true,
  i_obj:'pumpkin', i_air:false, i_h:10, i_th:0, i_v0:15, i_tgt:TARGET_X0,
  i_vt:false, i_vc:false, i_at:false, i_ac:false,
  v_m:5, v_d:0.8, v_air:true, v_h:0, v_th:80, v_v0:18, v_tgt:TARGET_X0,
  v_mode:'total', v_vel:true, v_acc:true, v_frc:false, v_strobe:true,
  d_cd:0.47, d_d:0.8, d_m:5, d_alt:0, d_h:0, d_th:80, d_v0:18, d_tgt:TARGET_X0,
  d_mode:'total', d_vel:false, d_frc:false,
  l_obj:'cannonball', l_m:17.6, l_d:0.18, l_cd:0.47, l_g:G_EARTH, l_alt:0, l_air:false,
  l_h:0, l_th:80, l_v0:18, l_tgt:TARGET_X0,
  a_obj:'baseball', a_air:true, a_alt:0, a_g:G_EARTH, a_h:0, a_th:45, a_v0:30, e_vac:true, o_cliff:true,
};
const ST=Object.assign({},DEFAULTS);
const ZOOM=[0.25,2];                               /* PhET's MIN_ZOOM, MAX_ZOOM */

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---- what each view fires -------------------------------------------------------- */
function projOf(v,st){
  st=st||ST;
  if(v==='intro'){ const o=objById(st.i_obj); return {o,m:o.m,d:o.d,cd:o.cd}; }
  if(v==='vectors') return {o:SCREEN_OBJ,m:st.v_m,d:st.v_d,cd:SCREEN_OBJ.cd};
  if(v==='drag') return {o:SCREEN_OBJ,m:st.d_m,d:st.d_d,cd:st.d_cd};
  if(v==='lab'){ const o=objById(st.l_obj); return {o,m:st.l_m,d:st.l_d,cd:st.l_cd}; }
  const o=objById(st.a_obj); return {o,m:o.m,d:o.d,cd:o.cd};
}
function envOf(v,st){
  st=st||ST;
  const P=projOf(v,st), an=(v==='env'||v==='hodo');
  const air=v==='intro'?st.i_air:(v==='vectors'?st.v_air:(v==='drag'?true:(v==='lab'?st.l_air:st.a_air)));
  const alt=v==='drag'?st.d_alt:(v==='lab'?st.l_alt:(an?st.a_alt:0));
  const g=v==='lab'?st.l_g:(an?st.a_g:G_EARTH);
  const rho=airDensity(alt);
  return {g,rho,air:!!air,alt,k:air?dragK(P.m,P.d,P.cd,rho):0};
}
function launchOf(v,st){ st=st||ST; const p=PFX[v]; return {h:st[p+'h'],th:st[p+'th'],v0:st[p+'v0']}; }
function launchKey(v,st){
  const L=launchOf(v,st), P=projOf(v,st), E=envOf(v,st);
  return [P.o.id,P.m,P.d,P.cd,L.h,L.th,L.v0,E.g,E.k].join('|');
}
function predicted(v){ return memo('pred_'+v,launchKey(v,ST),()=>flight(launchOf(v,ST),envOf(v,ST))); }

/* ---- the scenes: each PhET screen keeps its own clock, paths, tape and probe ---- */
const SCN={};
function scnReset(v){ SCN[v]={t:0,trajs:[],score:null,tape:{x0:0,y0:0,x1:10,y1:0},probe:{x:8,y:4},nextId:1}; }
SCENE_VIEWS.forEach(scnReset);
function flyingCount(v){ let n=0; for(const tr of SCN[v].trajs) for(const p of tr.projs) if(!p.landed) n++; return n; }
/* fire: PhET's rules — at most three in the air; a shot identical to the last
   path (same object, mass, size, C_d, height, angle, speed, gravity and air)
   joins that path instead of making a new one; five paths are kept */
function fire(v){
  if(!isScene(v)) return false;
  const sc=SCN[v];
  if(flyingCount(v)>=MAX_FLYING) return false;
  const key=launchKey(v,ST), last=sc.trajs[sc.trajs.length-1];
  if(last&&!last.changed&&last.key===key){ last.projs.push({t0:sc.t,landed:false}); return true; }
  sc.trajs.push({id:sc.nextId++,key,F:predicted(v),L:launchOf(v,ST),E:envOf(v,ST),P:projOf(v,ST),
                 projs:[{t0:sc.t,landed:false}],changed:false});
  while(sc.trajs.length>MAX_TRAJ) sc.trajs.shift();
  return true;
}
function erase(v){ if(!isScene(v)) return; SCN[v].trajs=[]; SCN[v].score=null; }
/* advance the clock; a landing scores against the target and, as in PhET,
   only the most recent landed projectile of each path stays on the ground */
function advance(v,dt){
  const sc=SCN[v], was=flyingCount(v);
  sc.t+=dt;
  const tgt=ST[PFX[v]+'tgt'];
  for(const tr of sc.trajs){
    for(const p of tr.projs) if(!p.landed&&sc.t-p.t0>=tr.F.T){
      p.landed=true; p.tl=sc.t;
      sc.score={stars:starsFor(tr.F.R,tgt),x:tr.F.R,tgt,t:sc.t};
    }
    const landed=tr.projs.filter(p=>p.landed);
    if(landed.length>1){ let keep=landed[0]; for(const p of landed) if(p.tl>keep.tl||(p.tl===keep.tl&&p.t0>keep.t0)) keep=p;
      tr.projs=tr.projs.filter(p=>!p.landed||p===keep); }
  }
  return was>0;
}
/* air, altitude or gravity changed: every projectile still in the air flies on
   from its last node in the new conditions.  The furthest one keeps its path
   (the path bends where it is); the others behind it split off onto paths of
   their own, as in PhET's updateTrajectoriesWithMovingProjectiles. */
function retarget(v){
  if(!isScene(v)) return 0;
  const sc=SCN[v], E=envOf(v,ST), add=[]; let n=0;
  for(const tr of sc.trajs){
    const fly=tr.projs.filter(p=>!p.landed);
    if(!fly.length) continue;
    let lead=tr.projs[0]; for(const p of tr.projs) if(p.t0<lead.t0) lead=p;
    const conts=fly.map(p=>continueFlight(tr.F,sc.t-p.t0,E));
    fly.forEach((p,i)=>{
      n++;
      if(!lead.landed&&p===lead){ tr.F=conts[i]; tr.E=E; tr.changed=true; }
      else { add.push({id:sc.nextId++,key:tr.key,F:conts[i],L:tr.L,E,P:tr.P,projs:[p],changed:true});
             tr.projs.splice(tr.projs.indexOf(p),1); }
    });
  }
  for(const a of add) sc.trajs.push(a);
  while(sc.trajs.length>MAX_TRAJ) sc.trajs.shift();
  return n;
}
/* how far along its path a trajectory has been drawn: to its furthest projectile */
function shownUntil(tr,t){
  let a=0; for(const p of tr.projs) a=Math.max(a,t-p.t0);
  return Math.min(a,tr.F.T);
}
/* the data probe: the nearest READABLE point — a 0.1-s dot, the apex or the
   landing — already reached, within the sensing radius; the newest path wins
   (PhET's Tracer).  PhET senses within 0.2 m of model space whatever the zoom;
   here the radius is 0.45 m at zoom 1 and scales with it, so it stays about
   12 px on screen at every zoom (0.225 m at the closest, zoom 2). */
function probeRadius(){ return 0.45/ST.zoom; }
function probeRead(v){
  const sc=SCN[v], pr=sc.probe, r=probeRadius();
  for(let j=sc.trajs.length-1;j>=0;j--){
    const tr=sc.trajs[j], F=tr.F, lim=shownUntil(tr,sc.t)+1e-12;
    let best=null, bd=Infinity;
    const idx=F.dots.slice(); if(F.apexI>=0) idx.push(F.apexI); if(F.landI>=0) idx.push(F.landI);
    for(const i of idx){
      if(F.t[i]>lim) continue;
      const d=Math.hypot(F.x[i]-pr.x,F.y[i]-pr.y);
      if(d<=r&&(d<bd-1e-12||(Math.abs(d-bd)<=1e-12&&best&&F.t[i]>best.t))){ bd=d; best={t:F.t[i],x:F.x[i],y:F.y[i],apex:i===F.apexI,land:i===F.landI,j,d}; }
    }
    if(best) return best;
  }
  return null;
}
function tapeLength(v){ const T=SCN[v].tape; return Math.hypot(T.x1-T.x0,T.y1-T.y0); }
/* the energy ledger: max |v^2/2 + g y + w - e0| over the nodes (J/kg) */
function ledgerResidual(F){
  const e0=0.5*(F.vx[0]*F.vx[0]+F.vy[0]*F.vy[0])+F.g*F.y[0]+F.w[0];
  let worst=0;
  for(let i=0;i<F.t.length;i++){ const e=0.5*(F.vx[i]*F.vx[i]+F.vy[i]*F.vy[i])+F.g*F.y[i]+F.w[i]; worst=Math.max(worst,Math.abs(e-e0)); }
  return {e0,worst};
}

/* ---- the analysis views: the envelope and the hodograph ---------------------------- */
function analysisKey(st){ return [st.a_obj,st.a_air,st.a_alt,st.a_g,st.a_h,st.a_v0].join('|'); }
const FAN_STEP=7.5, R_STEP=2;
function envModel(st){
  const L=launchOf('env',st), E=envOf('env',st), P=projOf('env',st);
  const base=memo('env',analysisKey(st),()=>{
    const fan=[], ths=[], Rs=[], Rv=[];
    for(let a=0;a<=90+1e-9;a+=FAN_STEP) fan.push({th:a,F:E.k>0?flight({h:L.h,th:a,v0:L.v0},E):null});
    for(let a=0;a<=90+1e-9;a+=R_STEP){ ths.push(a); Rs.push(rangeAt(L,E,a)); Rv.push(vacuum(L.h,a,L.v0,E.g).R); }
    const opt=optimumAngle(L,E);
    return {fan,ths,Rs,Rv,opt,vopt:vacuumOptimum(L.h,L.v0,E.g),best:E.k>0?flight({h:L.h,th:opt.th,v0:L.v0},E):null};
  });
  const cur=memo('envcur',analysisKey(st)+'|'+st.a_th,()=>({F:E.k>0?flight(L,E):null,V:vacuum(L.h,L.th,L.v0,E.g)}));
  const Rcur=E.k>0?cur.F.R:cur.V.R;
  return Object.assign({L,E,P,cur,Rcur,Hmax:L.h+L.v0*L.v0/(2*E.g),vt:terminalSpeed(E.g,E.k)},base);
}
function hodoModel(st){
  const L=launchOf('hodo',st), E=envOf('hodo',st), P=projOf('hodo',st);
  return memo('hodo',analysisKey(st)+'|'+st.a_th+'|'+st.o_cliff,()=>{
    /* fly on past the ground only as far as it shows something: to 3 v_t/g past
       the landing when v_t is reachable (3 v_t/g <= 25 s), else a little way */
    const F=flight(L,E), vt=terminalSpeed(E.g,E.k), reach=isFinite(vt)&&3*vt/E.g<=25;
    const tEnd=Math.ceil(Math.min(40,reach?F.T+3*vt/E.g:1.5*F.T+0.5)/DOT-1e-9)*DOT;
    const C=st.o_cliff?flight(L,E,{cliff:true,tEnd}):null;
    const th=L.th*DEG, u0=L.v0*Math.cos(th), ex=[];
    if(Math.abs(L.th)<89.9&&L.v0>0){
      const n=240, lo=-89.6*DEG;
      for(let i=0;i<=n;i++){ const phi=th+(lo-th)*i/n, u=hodoU(phi,th,u0,E.g,E.k); ex.push([u,u*Math.tan(phi)]); }
    } else ex.push([0,L.v0*Math.sin(th)],[0,isFinite(vt)?-vt:-L.v0-E.g*1.5*F.T]);
    const HL=(E.k>0&&Math.abs(L.th)<89.9&&L.v0>0&&F.T>0&&F.angL<89.5)?hodoLanding(L,E):null;
    return {L,E,P,F,C,vt,reach,tEnd,ex,HL,led:ledgerResidual(C||F),ua:F.apex?F.vx[F.apexI]:null};
  });
}

function buildModel(){
  const st=ST, v=st.view, M={view:v,st};
  if(isScene(v)){
    const sc=SCN[v];
    M.L=launchOf(v,st); M.E=envOf(v,st); M.P=projOf(v,st);
    M.pred=predicted(v); M.vac=vacuum(M.L.h,M.L.th,M.L.v0,M.E.g); M.vt=terminalSpeed(M.E.g,M.E.k);
    M.sc=sc; M.t=sc.t; M.flying=flyingCount(v); M.tgt=st[PFX[v]+'tgt'];
    M.probe=st.probe?probeRead(v):null; M.tape=st.tape?tapeLength(v):null;
  }
  else if(v==='env') M.Env=envModel(st);
  else M.Hodo=hodoModel(st);
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function fm(x,n){ return sigf(x,n||4)+' m'; }
function starText(n){ return n>0?'&#9733;'.repeat(n)+' ('+n+(n===1?' star':' stars')+')':'missed'; }
function objLine(P){ return sigf(P.m,4)+' kg &middot; '+sigf(P.d,3)+' m &middot; C<sub>d</sub> '+fmt(P.cd,2); }
function airLine(E){ return E.air?'&rho; '+sigf(E.rho,4)+' kg/m&sup3; at '+fmt(E.alt,0)+' m':'off (&rho; = 0)'; }
function readoutHTML(M){
  const st=ST, name=TABS.find(t=>t[0]===M.view)[1];
  let s='<div class="rname">projectile motion<small>'+name+'</small></div><table>';
  if(isScene(M.view)){
    const L=M.L, E=M.E, P=M.P, F=M.pred, V=M.vac;
    s+=hd((M.view==='intro'||M.view==='lab')?P.o.name:'the projectile')+rrow('mass, diameter, drag',objLine(P))
      +rrow('air',airLine(E));
    if(E.air) s+=rrow('terminal speed &radic;(2mg/&rho;C<sub>d</sub>A)',sigf(M.vt,4)+' m/s');
    if(M.view==='lab') s+=rrow('gravity',sigf(E.g,4)+' m/s&sup2;');
    s+=hd('this shot: '+fmt(L.h,1)+' m, '+fmt(L.th,0)+'&deg;, '+fmt(L.v0,1)+' m/s')
      +rrow('range',fm(F.R),'good')+rrow('highest point',fm(F.H)+(F.apex?' at '+fm(F.apex.x):' (launched level or down)'))
      +rrow('time of flight',sigf(F.T,4)+' s')+rrow('lands at',F.vL>0?sigf(F.vL,4)+' m/s, '+fmt(F.angL,1)+'&deg; down':'rest');
    if(E.air) s+=rrow('in vacuum instead',fm(V.R)+', '+sigf(V.T,4)+' s','bad')
                 +rrow('taken by the air',sigf(F.W,4)+' J/kg = '+sigf(F.W*P.m,4)+' J');
    const sc=M.sc;
    s+=hd('fired')+rrow('in the air, paths',M.flying+' of '+MAX_FLYING+', '+sc.trajs.length+' of '+MAX_TRAJ)
      +rrow('target at '+fmt(M.tgt,1)+' m',sc.score?starText(sc.score.stars)+(sc.score.stars?'':' by '+fm(Math.abs(sc.score.x-sc.score.tgt)-TARGET_W/2)):'no shot yet',sc.score&&sc.score.stars?'good':'');
    if(st.probe) s+=hd('data probe')+(M.probe?rrow('time',sigf(M.probe.t,4)+' s'+(M.probe.apex?' (apex)':(M.probe.land?' (landing)':'')))
        +rrow('range',fm(M.probe.x))+rrow('height',fm(M.probe.y)):rrow('reading','not on a dot, the apex or a landing'));
    if(st.tape) s+=hd('tape measure')+rrow('length',fm(M.tape));
  }
  else if(M.view==='env'){
    const Q=M.Env, L=Q.L, E=Q.E;
    s+=hd(Q.P.o.name)+rrow('mass, diameter, drag',objLine(Q.P))+rrow('air',airLine(E))
      +rrow('launch',fmt(L.v0,1)+' m/s from '+fmt(L.h,1)+' m, g '+sigf(E.g,4));
    s+=hd('the best angle')+rrow(E.air?'with the air (golden section)':'this shot',fmt(Q.opt.th,2)+'&deg; &rarr; '+fm(Q.opt.R),'good')
      +rrow('vacuum: tan &theta;* = v<sub>0</sub>/&radic;(v<sub>0</sub>&sup2;+2gh)',fmt(Q.vopt.th,2)+'&deg; &rarr; '+fm(Q.vopt.R),'bad');
    if(E.air&&Q.vopt.R>0) s+=rrow('the air costs',fmt(100*(1-Q.opt.R/Q.vopt.R),1)+' % of the reach');
    s+=hd('at '+fmt(L.th,0)+'&deg;')+rrow(E.air?'range with the air':'range',fm(Q.Rcur),'good');
    if(E.air) s+=rrow('range in vacuum',fm(Q.cur.V.R));
    s+=hd('the vacuum envelope')+rrow('top, h + v<sub>0</sub>&sup2;/2g',fm(Q.Hmax))+rrow('reach on the ground',fm(Q.vopt.R));
  }
  else {
    const Q=M.Hodo, L=Q.L, E=Q.E, F=Q.F, th=L.th*DEG;
    s+=hd(Q.P.o.name)+rrow('mass, diameter, drag',objLine(Q.P))+rrow('air',airLine(E))
      +rrow('launch',fmt(L.h,1)+' m, '+fmt(L.th,0)+'&deg;, '+fmt(L.v0,1)+' m/s');
    s+=hd('velocity (v<sub>x</sub>, v<sub>y</sub>)')+rrow('at launch','('+sigf(L.v0*Math.cos(th),3)+', '+sigf(L.v0*Math.sin(th),3)+') m/s')
      +rrow('at the apex',Q.ua!==null?'('+sigf(Q.ua,4)+', 0) m/s':'no apex')
      +rrow('at landing','('+sigf(F.vx[F.landI],4)+', '+sigf(F.vy[F.landI],4)+') m/s')
      +rrow('landing speed',sigf(F.vL,4)+' m/s, '+fmt(F.angL,1)+'&deg; down','good')
      +rrow('terminal (0, &minus;v<sub>t</sub>)',isFinite(Q.vt)?'(0, &minus;'+sigf(Q.vt,4)+') m/s':'none in vacuum','bad');
    if(Q.HL) s+=hd('the exact hodograph route')+rrow('range: RK4',fm(F.R))+rrow('range: hodograph',fm(Q.HL.R),'good')
      +rrow('they differ by',sigf(Math.abs(Q.HL.R-F.R)/F.R,2)+' of it');
    s+=hd('energy per kilogram')+rrow('&frac12;v<sub>0</sub>&sup2; + gh',sigf(Q.led.e0,4)+' J/kg')
      +rrow('taken by the air by landing',sigf(F.W,4)+' J/kg ('+fmt(100*F.W/Q.led.e0,1)+' %)')
      +rrow('ledger &frac12;v&sup2;+gy+w &minus; e<sub>0</sub>, worst',sigf(Q.led.worst,2)+' J/kg','good');
  }
  s+='</table><div class="note">PhET&rsquo;s projectiles and air model; every computed number here is pinned in selfTest to build/projectile-motion/derive.py (scipy DOP853, the exact hodograph, the closed forms).</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='intro') return E('x = v<sub>0</sub> cos &theta; t, &nbsp; y = h + v<sub>0</sub> sin &theta; t &minus; &frac12;g t&sup2; &nbsp;&rArr;&nbsp; <span class="hl">R = v<sub>0</sub> cos &theta; (v<sub>0</sub> sin &theta; + &radic;(v<sub>0</sub>&sup2; sin&sup2;&theta; + 2gh)) / g</span>',
    'without air the path is a parabola and every number about it is closed form; the mass never appears');
  if(M.view==='vectors') return E('m <b>a</b> = m <b>g</b> + <b>F</b><sub>d</sub>, &nbsp; <span class="hl"><b>F</b><sub>d</sub> = &minus;&frac12; &rho; C<sub>d</sub> A |<b>v</b>| <b>v</b></span> &nbsp;&rArr;&nbsp; a<sub>x</sub> = &minus;k|v|v<sub>x</sub>, &nbsp; a<sub>y</sub> = &minus;g &minus; k|v|v<sub>y</sub>',
    'gravity never changes; the drag always points back along the velocity and grows as its square, so it tilts the acceleration against the motion');
  if(M.view==='drag') return E('<span class="hl">v<sub>t</sub> = &radic;(2mg / &rho; C<sub>d</sub> A)</span> &nbsp;&middot;&nbsp; &rho; = p / (0.2869 (T + 273.1)), &nbsp; T = 15.04 &minus; 0.00649 h, &nbsp; p = 101.29 [(T + 273.1)/288.08]<sup>5.256</sup>',
    'the drag equals the weight at the terminal speed; thinner air at altitude raises it and the shot flies further');
  if(M.view==='lab') return E('x&Prime; = &minus;k |v| x&prime;, &nbsp; y&Prime; = &minus;g &minus; k |v| y&prime;, &nbsp; <span class="hl">k = &rho; C<sub>d</sub> A / 2m</span>',
    'the mass enters only through k: in vacuum a piano and a golf ball fly the same path');
  if(M.view==='env') return E('<span class="hl">y = h + v<sub>0</sub>&sup2;/2g &minus; g x&sup2;/2v<sub>0</sub>&sup2;</span> &nbsp;&middot;&nbsp; tan &theta;* = v<sub>0</sub> / &radic;(v<sub>0</sub>&sup2; + 2gh), &nbsp; R* = v<sub>0</sub> &radic;(v<sub>0</sub>&sup2; + 2gh) / g',
    'no vacuum shot at this speed crosses this parabola, and every shot steeper than the best angle touches it; the air pulls the best angle below 45&deg;');
  return E('<span class="hl">1/u&sup2; = 1/u<sub>0</sub>&sup2; + (k/g) [F(&theta;) &minus; F(&phi;)]</span>, &nbsp; F(&psi;) = sin &psi; / cos&sup2;&psi; + ln tan(&pi;/4 + &psi;/2), &nbsp; u = v cos &phi;',
    'the velocity turns down while its horizontal part decays; the curve ends at (0, &minus;v<sub>t</sub>), where the drag holds the weight');
}
function tagHTML(M){
  const st=ST;
  if(isScene(M.view)){ const L=M.L;
    return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b> — '+(M.view==='intro'||M.view==='lab'?M.P.o.name:'the sphere')+', '
      +fmt(L.h,1)+' m, '+fmt(L.th,0)+'&deg;, '+fmt(L.v0,1)+' m/s'+(M.E.air?', air on':', no air'); }
  const P=projOf(M.view,st);
  return '<b>'+TABS.find(t=>t[0]===M.view)[1]+'</b> — '+P.o.name+', '+fmt(st.a_v0,1)+' m/s'+(M.view==='hodo'?' at '+fmt(st.a_th,0)+'&deg;':'')+(st.a_air?', air on':', no air');
}
