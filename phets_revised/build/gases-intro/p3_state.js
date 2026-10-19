
/* ================================================================== *
 *  state: the four views, their worlds, the per-view model, readout,   *
 *  equation bar and tag.  PhET's Gases Intro is the Ideal screen with  *
 *  hasHoldConstantFeature false (Intro) and true (Laws), so `intro`    *
 *  and `laws` are the two screens and `pv` is the Laws screen's own    *
 *  gas seen on the P-V plane — one model, two instruments.             *
 * ================================================================== */
const TABS=[['intro','the box'],['laws','the laws'],['pv','P against V'],['sweep','the four laws']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           heavy:'#6c9cff', light:'#ff6f6f',
           box:'#0d1422', wall:'#5ac8e0', lid:'#7f93b3', heat:'#ff7a3d', cool:'#5fb4ff', text:'#aeb6c6'};
const RO_W=300;
const SEEDS={intro:21, laws:22, sweep:23};
const HOLDS=[{id:'nothing',name:'Nothing'},{id:'volume',name:'Volume (V)'},{id:'temperature',name:'Temperature (T)'},
             {id:'pressureV',name:'Pressure ↕V'},{id:'pressureT',name:'Pressure ↕T'}];
const PUMPS=[{id:'heavy',name:'heavy'},{id:'light',name:'light'}];
const UNITS_T=[{id:'K',name:'K'},{id:'C',name:'°C'}];
const UNITS_P=[{id:'atm',name:'atm'},{id:'kPa',name:'kPa'}];
const PERIODS=GAS.PERIODS.map(p=>({id:p,name:p+' ps'}));
/* the four named laws, each a (hold, swept variable, invariant) triple */
const LAWS=[{id:'boyle',   name:'Boyle',      hold:'temperature', x:'V', y:'P', inv:'P V',   iu:'kPa nm³'},
            {id:'charles', name:'Charles',    hold:'pressureV',   x:'T', y:'V', inv:'V / T', iu:'nm³/K'},
            {id:'gay',     name:'Gay-Lussac', hold:'volume',      x:'T', y:'P', inv:'P / T', iu:'kPa/K'},
            {id:'avo',     name:'Avogadro',   hold:'pressureT',   x:'N', y:'T', inv:'N T',   iu:'K'}];
const FRAME_DT=GAS.DT_FRAME;
/* the isotherms the P-against-V view draws */
const ISO_T=[150,300,600,1000];
/* the wall-hit rate is measured over a rolling window of this many frames */
const HIT_WINDOW=240;
/* the sweep: settle, then count wall hits, at each of five targets */
const SWEEP_SETTLE=48, SWEEP_N=5, SWEEP_BATCH=8;

const DEFAULTS={view:'intro', running:true,
  pump:'heavy', heat:0, unitT:'K', unitP:'atm', noise:true,
  showWidth:true, showWatch:false, showCounter:true, period:10,
  hold:'nothing', nH:100, nL:0,
  law:'boyle', sN:100, sT:300, sWin:20};
const ST=Object.assign({},DEFAULTS);
/* every view here draws the container: the Intro and Laws screens, the P-V
   plane (the Laws gas) and the sweep (the gas being swept) */
const BOXVIEWS={intro:1, laws:1, pv:1, sweep:1};
/* `pv` has no gas of its own: it is the Laws screen's gas on another plot */
function worldKey(view){ return view==='pv'?'laws':view; }

/* ---- the worlds ------------------------------------------------------------ */
const WORLD={};
function pressureOnAfterFill(g){ g.pOn=gasCount(g)>0; gasRefresh(g); }
function makeWorld(view,st){
  const key=worldKey(view);
  const w={view:key, trace:[], hits:[], hitAcc:0, htAcc:0, pump:{h:0, acc:0}, dragW:null, sweep:null};
  const g=w.g=gasMake({seed:SEEDS[key]});
  g.noiseOn=st.noise;
  if(key==='sweep'){ gasFill(g,0,st.sN,st.sT); }
  else { gasFill(g,0,100,GAS.T0); }
  gasLedgerReset(g); pressureOnAfterFill(g);
  traceRecord(w);
  return w;
}
function worldOf(view){ const k=worldKey(view); if(!WORLD[k]) WORLD[k]=makeWorld(k,ST); return WORLD[k]; }
function resetWorld(view){ const k=worldKey(view); WORLD[k]=makeWorld(k,ST); return WORLD[k]; }
function resetAllWorlds(){ for(const k in WORLD) delete WORLD[k]; }

/* the trace every box view shares: t, T, the gauge, the width, the noise-free P */
function traceRecord(w){
  const g=w.g;
  w.trace.push([g.t,g.T===null?NaN:g.T,g.pOn?g.gaugeP:0,g.W,g.pOn?g.P:0]);
  if(w.trace.length>900) w.trace.splice(0,w.trace.length-900);
}
/* the measured wall-hit rate: a rolling window of HIT_WINDOW frames.  This is
   the one falsifiable number on PhET's Intro screen — the Collision Counter —
   so it is measured continuously and compared with kinetic theory. */
function hitRecord(w,dt){
  w.hits.push([dt,w.g.stats.frameWallHits]);
  if(w.hits.length>HIT_WINDOW) w.hits.shift();
}
function hitRateMeasured(w){
  let t=0,c=0; for(const r of w.hits){ t+=r[0]; c+=r[1]; }
  return t>0?{rate:c/t, n:c, t}:null;
}
/* kinetic theory: each species contributes n_k <vx+>_k over the whole
   perimeter its centres can reach, and collisions raise the contact density
   by the hard-disk Z (derive.py section 4b: 6.4234/ps for 100 heavy at 300 K
   in the 10 nm box with Z = 1, 7.2178/ps with Z). */
function hitRateOf(counts,radii,masses,W,Hh,T,useZ){
  if(T===null||!(T>0)||counts[0]+counts[1]===0) return null;
  let s=0;
  for(const k of [0,1]){
    const nk=counts[k]; if(!nk) continue;
    const r=radii[k], a=W-2*r, b=Hh-2*r;
    if(!(a>0&&b>0)) return null;
    s+=nk/(a*b)*Math.sqrt(gasKT2(T)/(2*Math.PI*masses[k]))*2*(a+b);
  }
  return s*(useZ?hdZ(counts,radii,W,Hh):1);
}
/* Z is the crowding the PAIR collisions cause, so a gas with collisions
   switched off is ideal however big its disks are: the flag has to reach the
   theory, or the "with Z" curve would keep claiming a correction that is not
   there (selfTest asserts both branches). */
function hitRateTheory(g,useZ){
  return hitRateOf([gasCount(g,0),gasCount(g,1)],[g.species[0].r,g.species[1].r],
                   [g.species[0].m,g.species[1].m],g.W,g.H,g.T,useZ&&g.collisions!==false);
}

/* the isotherms the P-against-V view draws, as DATA rather than as pixels: a
   number computed inside a draw call cannot be asserted, and a mutation sweep
   says so (projects/simulations/CHANGELOG.md, Known-bad).  V is in nm³. */
function pvIsotherm(N,T,V0,V1,n){
  const xs=[], ys=[];
  for(let i=0;i<=n;i++){ const V=V0+(V1-V0)*i/n; xs.push(V); ys.push(gasPressureOf(N,T,V*1e9)); }
  return {xs,ys};
}

/* ---- the sweep: the four laws, measured off the simulation ------------------ */
function sweepTargets(w,st,P0){
  const g=w.g, N=gasCount(g);
  if(st.law==='boyle')  return [GAS.WMIN,7500,GAS.WDEF,12500,GAS.WMAX];
  if(st.law==='gay')    return [200,300,400,500,600];
  /* Avogadro stops at twice the starting count: past an area fraction of
     about 0.12 the B₃ truncation in Z starts to under-predict the crowding */
  if(st.law==='avo')    return [0.5,0.75,1,1.5,2].map(f=>Math.max(10,Math.round(f*st.sN)));
  /* Charles: T runs over exactly the range whose width fits PhET's container,
     T = P V/(N k), kept a hair inside so the controller's toFixed(5) cannot
     round past the end and raise an Oops */
  const Tlo=P0/GAS.P_SCALE*(GAS.WMIN*g.H*g.D)/(N*GAS.K), Thi=P0/GAS.P_SCALE*(GAS.WMAX*g.H*g.D)/(N*GAS.K);
  return [0,1,2,3,4].map(i=>clamp(Tlo+(Thi-Tlo)*i/4,Tlo*(1+1e-9),Thi*(1-1e-9)));
}
function sweepStart(w,st){
  const g=w.g;
  gasRemoveAll(g); gasSetHold(g,'nothing'); gasResize(g,GAS.WDEF,true);
  gasFill(g,0,st.sN,st.sT); g.pOn=gasCount(g)>0; gasRefresh(g);
  const S={law:st.law, i:0, phase:'apply', frames:0, pts:[], hits:0, ht:0,
           P0:g.P, N0:gasCount(g,0), T0:g.T, W0pm:g.W,
           measure:Math.round(st.sWin/FRAME_DT), done:false};
  S.targets=sweepTargets(w,st,g.P);
  w.sweep=S;
  return S;
}
/* The sweep changes the count with gasFill, not with PhET's pump.  The pump
   puts every new disk at one point (-r, H/5) and it takes tens of ps for a
   batch of fifty to spread out; measuring a wall-hit rate before it has is
   measuring a clump, and it read 38 % low.  gasFill places them uniformly and
   without overlaps, which is the state the kinetic-theory rate assumes.  This
   is a house measurement tool, not one of PhET's screens. */
function sweepSetCount(g,n,T){
  const c=gasCount(g,0);
  if(n>c) gasFill(g,0,n-c,T===null?GAS.T0:T);
  else if(n<c) gasRemove(g,0,c-n);
}
function sweepApply(w,S){
  const g=w.g, v=S.targets[S.i];
  if(S.law==='boyle'){ gasSetHold(g,'temperature'); gasResize(g,v,true); }
  else if(S.law==='gay'){ gasSetHold(g,'volume'); gasSetTemp(g,v); }
  else if(S.law==='charles'){ gasSetHold(g,'pressureV'); gasSetTemp(g,v); }
  else { gasSetHold(g,'pressureT'); sweepSetCount(g,v,g.T); }
  gasRefresh(g);
}
function sweepRecord(w,S){
  const g=w.g, N=gasCount(g), T=g.T, V=gasVolume(g)/1e9, P=g.P;
  const rate=S.ht>0?S.hits/S.ht:null;
  const pt={N,T,V,P,rate,n:S.hits,t:S.ht,
            rateTh:hitRateTheory(g,true), rateId:hitRateTheory(g,false), W:g.W};
  pt.x=S.law==='boyle'?V:(S.law==='avo'?N:T);
  pt.y=S.law==='boyle'?P:(S.law==='charles'?V:(S.law==='gay'?P:T));
  pt.inv=S.law==='boyle'?P*V:(S.law==='charles'?V/T:(S.law==='gay'?P/T:N*T));
  S.pts.push(pt);
}
/* one model frame of the sweep; returns true while it is still running */
function sweepStep(w,st,dt){
  const S=w.sweep; if(!S||S.done) return false;
  if(S.phase==='apply'){ sweepApply(w,S); S.phase='settle'; S.frames=0; S.hits=0; S.ht=0; return true; }
  gasStep(w.g,dt);
  hitRecord(w,dt);
  S.frames++;
  if(S.phase==='settle'){
    if(S.frames>=SWEEP_SETTLE){ S.phase='measure'; S.frames=0; S.hits=0; S.ht=0; }
    return true;
  }
  S.hits+=w.g.stats.frameWallHits; S.ht+=dt;
  if(S.frames>=S.measure){
    sweepRecord(w,S);
    S.i++;
    if(S.i>=S.targets.length){ S.done=true; return false; }
    S.phase='apply';
  }
  return true;
}
/* run a sweep to the end without a frame loop (the tests and the captures) */
function sweepRunAll(w,st,cap){
  let n=0; const lim=cap||60000;
  while(w.sweep&&!w.sweep.done&&n<lim){ sweepStep(w,st,FRAME_DT); n++; }
  return n;
}

/* ---- per-view bookkeeping each frame ---------------------------------------- */
function viewDt(){ return GAS.DT_FRAME; }
function worldStep(w,st,dt){
  const g=w.g;
  if(w.view!=='sweep'&&w.dragW!==null) return false;   /* PhET pauses while the wall is dragged */
  const n0=gasCount(g,0), n1=gasCount(g,1);
  if(w.view==='sweep'&&w.sweep&&!w.sweep.done){
    /* the sweep runs SWEEP_BATCH model frames per animation frame, so 100 ps
       of measurement is a few seconds to watch rather than a minute */
    for(let b=0;b<SWEEP_BATCH;b++) if(!sweepStep(w,st,dt)) break;
  } else {
    g.heat=w.view==='sweep'?0:st.heat;
    gasStep(g,dt);
    hitRecord(w,dt);
  }
  traceRecord(w);
  return gasCount(g,0)!==n0||gasCount(g,1)!==n1;
}

/* ---- the models the readout and the views read ------------------------------- */
function fmtT(T,st){ if(T===null||T===undefined||!isFinite(T)) return '—'; return st.unitT==='C'?sigf(T-273.15,4)+' °C':sigf(T,4)+' K'; }
function fmtP(Pk,st){ if(!isFinite(Pk)) return '—'; return st.unitP==='kPa'?Math.round(Pk)+' kPa':fmt(Pk*GAS.ATM_PER_KPA,1)+' atm'; }
function zJ(e){ return e*GAS.KG_PER_AMU*1e21; }        /* AMU pm²/ps² -> zJ, PhET's AMU */
function holdName(id){ const o=HOLDS.find(h=>h.id===id); return o?o.name:id; }
function lawOf(id){ return LAWS.find(l=>l.id===id)||LAWS[0]; }
function buildModel(){
  const st=ST, view=st.view, w=worldOf(view), g=w.g;
  const N=gasCount(g), nH=gasCount(g,0), nL=gasCount(g,1);
  const M={view,st,w,g,N,nH,nL,T:g.T,P:g.P,gauge:g.gaugeP,Wnm:g.W/1000,t:g.t,oops:g.oops};
  M.kT2=g.T===null?null:gasKT2(g.T);
  M.lidOpen=gasLidOpen(g); M.opening=gasOpening(g);
  M.V=gasVolume(g)/1e9;
  /* the invariant the chosen hold keeps, in the noise-free P */
  const T=g.T;
  M.inv=(!T||!N)?null:g.hold==='volume'?['P / T (Gay-Lussac)',sigf(g.P/T,6)+' kPa/K']
    :g.hold==='temperature'?['P V (Boyle)',sigf(g.P*M.V,6)+' kPa nm³']
    :g.hold==='pressureV'?['V / T (Charles)',sigf(M.V/T,6)+' nm³/K']
    :g.hold==='pressureT'?['N T (Avogadro, at fixed P and V)',sigf(N*T,6)+' K']:null;
  /* the collision counter against kinetic theory */
  M.hit=hitRateMeasured(w);
  M.hitTh=hitRateTheory(g,true); M.hitId=hitRateTheory(g,false);
  M.hitSd=(M.hit&&M.hit.n>0)?Math.sqrt(M.hit.n)/M.hit.t:null;   /* Poisson */
  if(view==='sweep') M.S=w.sweep;
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function readoutHTML(M){
  const st=M.st, g=M.g;
  let s='<div class="rname">gases intro<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  s+=hd('the gas')+rrow('heavy, light',M.nH+', '+M.nL+(gasOutside(g)?' (+'+gasOutside(g)+' escaping)':''))
    +rrow('temperature T',fmtT(M.T,st),'good')
    +rrow('pressure, the gauge',g.pOn?fmtP(M.gauge,st):'0 (no wall hit yet)')
    +rrow('P = NkT/V, no noise',fmtP(M.P,st))
    +rrow('width, volume',fmt(M.Wnm,2)+' nm, '+sigf(M.V,4)+' nm³')
    +rrow('mean KE',M.N?sigf(zJ(gasEnergy(g)/M.N),4)+' zJ':'—');
  if(M.view==='laws'||M.view==='pv'){
    s+=hd('hold constant')+rrow('held',holdName(g.hold),'good')
      +(M.inv?rrow(M.inv[0],M.inv[1],'good'):rrow('nothing held','P, V and T all free'));
  }
  if(M.view==='sweep'){
    const S=M.S, L=lawOf(st.law);
    s+=hd(L.name+'’s law — '+(S?(S.done?'done':'step '+(S.i+1)+' of '+S.targets.length+', '+S.phase):'not started'))
      +rrow('holding',holdName(L.hold))
      +rrow('points measured',S?S.pts.length:0,'good');
    if(S&&S.pts.length){
      const v0=S.pts[0].inv; let worst=0;
      for(const p of S.pts) worst=Math.max(worst,Math.abs(p.inv/v0-1));
      s+=rrow(L.inv+', first point',sigf(v0,7)+' '+L.iu,'good')
        +rrow('worst departure over the sweep',worst.toExponential(1),worst<1e-6?'good':'bad');
    }
  }
  s+=hd('the collision counter (wall hits/ps)');
  if(M.hit&&M.hit.n>0){
    s+=rrow('measured, last '+fmt(M.hit.t,1)+' ps',fmt(M.hit.rate,2)+' ± '+fmt(M.hitSd,2),'good')
      +rrow('kinetic theory, with Z',M.hitTh===null?'—':fmt(M.hitTh,2))
      +rrow('… with Z = 1 (no collisions)',M.hitId===null?'—':fmt(M.hitId,2))
      +rrow('measured / theory',M.hitTh?fmt(M.hit.rate/M.hitTh,3):'—',
            (M.hitTh&&Math.abs(M.hit.rate-M.hitTh)<3*M.hitSd)?'good':'');
  } else s+=rrow('measured','run the clock');
  if(st.showWatch||st.showCounter) s+=hd('tools');
  if(st.showWatch) s+=rrow('stopwatch',fmt(g.watch.t,2)+' ps'+(g.watch.on?' (running)':''));
  if(st.showCounter) s+=rrow('PhET’s counter',g.counter.count+' in '+fmt(g.counter.t,2)+' of '+g.counter.period+' ps');
  s+='</table><div class="note">PhET&rsquo;s definitions: T = (2/3)&lang;KE&rang;/k and P = NkT/V with V = width &times; 8.75 nm &times; 4 nm, so PV = NkT holds <i>by construction</i>. The hit rate is the number on this screen that could come out wrong.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const h=M.g.hold, hl=(x,on)=>on?'<span class="hl">'+x+'</span>':x;
  if(M.view==='intro')
    return E('P V = N k T &nbsp;&middot;&nbsp; T = (2/3)&lang;KE&rang;/k &nbsp;&middot;&nbsp; <span class="hl">wall hits/ps = 2 n Z &lang;v&rang;/&pi; (a + b)</span>',
      'pump, heat and squeeze: the thermometer and the gauge are averages over the disks, and the counter is the one number kinetic theory has to get right');
  if(M.view==='laws')
    return E(hl('P',h==='pressureV'||h==='pressureT')+' '+hl('V',h==='volume')+' = N k '+hl('T',h==='temperature')+' &nbsp;&middot;&nbsp; k = 8316 AMU pm&sup2;/(ps&sup2; K)',
      'hold one of P, V and T and the other two answer — '+(h==='nothing'?'nothing is held yet':holdName(h)+' is held'));
  if(M.view==='pv')
    return E('<span class="hl">P = N k T / V</span> &nbsp;&middot;&nbsp; an isotherm is a hyperbola P &prop; 1/V &nbsp;&middot;&nbsp; V = w &times; 8750 pm &times; 4000 pm',
      'the state is one point on this plane; hold T and it slides along a hyperbola, hold V and it climbs one, hold P and it runs across them');
  const L=lawOf(M.st.law);
  const eqs={boyle:'P V = <span class="rm">const</span> &nbsp;<span class="rm">(T, N fixed)</span>',
             charles:'V / T = <span class="rm">const</span> &nbsp;<span class="rm">(P, N fixed)</span>',
             gay:'P / T = <span class="rm">const</span> &nbsp;<span class="rm">(V, N fixed)</span>',
             avo:'N T = <span class="rm">const</span> &nbsp;<span class="rm">(P, V fixed)</span>'};
  return E('<span class="hl">'+eqs[L.id]+'</span> &nbsp;&middot;&nbsp; measured by holding '+holdName(L.hold)+' and stepping '+L.x,
    'the line is exact because PhET defines P = NkT/V; what the sweep tests is that the controller reaches the state it claims — and the hit rate beside it is not exact at all');
}
function tagHTML(M){
  if(M.view==='intro') return '<b>the box</b> — PhET&rsquo;s Intro screen: no hold-constant panel';
  if(M.view==='laws') return '<b>the laws</b> — PhET&rsquo;s Laws screen'+(M.g.hold!=='nothing'?', holding '+holdName(M.g.hold):'');
  if(M.view==='pv') return '<b>P against V</b> — the Laws screen&rsquo;s gas on the P&ndash;V plane';
  const S=M.S;
  return '<b>the four laws</b> — '+lawOf(M.st.law).name+(S?(S.done?': '+S.pts.length+' points measured':(S.pts.length?': measuring':': running')):': press run');
}
