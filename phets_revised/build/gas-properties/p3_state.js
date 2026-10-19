
/* ================================================================== *
 *  state: the six views, their worlds (one gas each, as PhET keeps    *
 *  one model per screen), the per-view model, readout, eqbar, tag     *
 * ================================================================== */
const TABS=[['ideal','the gas law'],['explore','the moving wall'],['energy','the energy'],
            ['diffusion','diffusion'],['pressure','the pressure'],['equil','equilibrium']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           heavy:'#6c9cff', light:'#ff6f6f', heavyHi:'#b9d0ff', lightHi:'#ffc0bb',
           box:'#0d1422', wall:'#5ac8e0', lid:'#7f93b3', heat:'#ff7a3d', cool:'#5fb4ff', text:'#aeb6c6'};
const RO_W=300;
const SEEDS={ideal:11, explore:12, energy:13, diffusion:14, pressure:15, equil:16};
const HOLDS=[{id:'nothing',name:'Nothing'},{id:'volume',name:'Volume (V)'},{id:'temperature',name:'Temperature (T)'},
             {id:'pressureV',name:'Pressure ↕V'},{id:'pressureT',name:'Pressure ↕T'}];
const PUMPS=[{id:'heavy',name:'heavy'},{id:'light',name:'light'}];
const UNITS_T=[{id:'K',name:'K'},{id:'C',name:'°C'}];
const UNITS_P=[{id:'atm',name:'atm'},{id:'kPa',name:'kPa'}];
const PERIODS=GAS.PERIODS.map(p=>({id:p,name:p+' ps'}));
const INJ=[{id:'match',name:'match container'},{id:'set',name:'set to'}];
const STARTS=[{id:'delta',name:'one speed'},{id:'split',name:'hot heavy, cold light'},{id:'pump',name:'the pump'}];
const ZOOMS=[2000,1500,1000,500,200,100,50];      /* HistogramsModel ZOOM_LEVELS yMax */
const ZOOM_LIST=ZOOMS.map((z,i)=>({id:i,name:'0–'+z}));
const FRAME_DT=GAS.DT_FRAME;

const DEFAULTS={view:'ideal', running:true,
  pump:'heavy', heat:0, unitT:'K', unitP:'atm', noise:true,
  showWidth:true, showWatch:false, showCounter:false, showWallVel:true, period:10, wallU:800,
  hold:'nothing', nH:100, nL:0,
  injMode:'match', injT:300, coll:true, histH:true, histL:true, zoom:5,
  d1n:100, d1m:28, d1r:125, d1T:300, d2n:100, d2m:4, d2r:90, d2T:300,
  dCOM:true, dFlow:true, dScale:true, slow:false, divided:true,
  pN:90, pT:300, pColl:true,
  eN:200, eStart:'delta', eColl:true};
const ST=Object.assign({},DEFAULTS);
const BOXVIEWS={ideal:1, explore:1, energy:1};

/* ---- the worlds ------------------------------------------------------------ */
const WORLD={};
function pressureOnAfterFill(g){ g.pOn=gasCount(g)>0; gasRefresh(g); }
function makeWorld(view,st){
  const w={view, trace:[], hist:[], pump:{h:0, acc:0}, dragW:null};
  if(view==='ideal'||view==='explore'||view==='energy'){
    const g=w.g=gasMake({seed:SEEDS[view], doesWork:view==='explore', wRange:view==='energy'?[GAS.WDEF,GAS.WDEF]:undefined});
    if(view==='energy'){ g.hold='volume'; gasSamplerOn(g); g.collisions=st.coll; g.injectT=st.injMode==='set'?st.injT:null; }
    g.noiseOn=st.noise;
    gasFill(g,0,view==='energy'?150:100,GAS.T0);
    if(view==='energy') gasFill(g,1,150,GAS.T0);
    gasLedgerReset(g); pressureOnAfterFill(g);
    if(view==='energy') for(let k=0;k<24;k++) gasSample(g,FRAME_DT,true);
    w.T0=g.T; w.W0=g.W; w.moving=false; if(view==='explore') g.wallSpeed=st.wallU;
    if(view==='ideal') idealRecord(w);
  } else if(view==='diffusion'){
    const g=w.g=gasMake({width:GAS.DIFF_W, wRange:[GAS.DIFF_W,GAS.DIFF_W], noLid:true, seed:SEEDS.diffusion,
                         species:[{m:st.d1m,r:st.d1r},{m:st.d2m,r:st.d2r}]});
    gasSetDivided(g,st.divided);
    diffScatter(g,st);
    gasFlowOn(g); gasLedgerReset(g);
  } else if(view==='pressure'){
    const g=w.g=gasMake({width:GAS.WDEF, wRange:[GAS.WDEF,GAS.WDEF], noLid:true, virial:true, seed:SEEDS.pressure, collisions:st.pColl});
    gasFill(g,0,st.pN,st.pT);
    pressureOnAfterFill(g); gasLedgerReset(g); gasVirialReset(g); gasImpulseReset(g);
  } else {
    const g=w.g=gasMake({width:GAS.WDEF, wRange:[GAS.WDEF,GAS.WDEF], noLid:true, seed:SEEDS.equil, collisions:st.eColl});
    const n=Math.round(st.eN/2);
    if(st.eStart==='delta'){ gasFill(g,0,n,GAS.T0,true); gasFill(g,1,st.eN-n,GAS.T0,true); }
    else if(st.eStart==='split'){ gasFill(g,0,n,3*GAS.T0,true); gasFill(g,1,st.eN-n,GAS.T0/3,true); }
    else { gasInject(g,0,n,GAS.T0); gasInject(g,1,st.eN-n,GAS.T0); }
    gasLedgerReset(g); pressureOnAfterFill(g);
    equilRecord(w);
  }
  return w;
}
function diffScatter(g,st){
  const half=g.dividerHalf, dx=g.left+g.W/2;
  gasScatter(g,0,st.d1n,st.d1T,g.left,dx-half);
  gasScatter(g,1,st.d2n,st.d2T,dx+half,0);
}
function worldOf(view){ if(!WORLD[view]) WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetWorld(view){ WORLD[view]=makeWorld(view,ST); return WORLD[view]; }
function resetAllWorlds(){ for(const k in WORLD) delete WORLD[k]; }

/* ---- per-view bookkeeping each frame ------------------------------------- */
function viewDt(st){ return st.view==='diffusion'&&st.slow?GAS.DT_SLOW:GAS.DT_FRAME; }
/* the equilibrium view's record: Boltzmann's H over K equal-probability energy
   bins (the relative entropy of the histogram against exp(-e/kT2)), and the two
   species' mean energies in units of the mean */
const EQ_K=12;
function equilH(g){
  const N=gasCount(g); if(N<2) return {H:null,floor:null};
  const kT2=gasEnergy(g)/N, cnt=new Array(EQ_K).fill(0);
  for(let i=0;i<g.n;i++){ if(g.out[i]) continue; const q=1-Math.exp(-gasKE(g,i)/kT2); cnt[Math.min(EQ_K-1,Math.floor(q*EQ_K))]++; }
  let H=0; for(const c of cnt) if(c>0){ const p=c/N; H+=p*Math.log(p*EQ_K); }
  return {H, floor:(EQ_K-1)/(2*N), cnt};
}
function equilRecord(w){
  const g=w.g, N=gasCount(g); if(!N) return;
  const E=gasEnergy(g)/N, h0=gasCount(g,0)?gasEnergy(g,0)/gasCount(g,0)/E:null, h1=gasCount(g,1)?gasEnergy(g,1)/gasCount(g,1)/E:null;
  const Hh=equilH(g);
  w.hist.push([g.t,Hh.H,h0,h1,g.stats.pairHits]);
  if(w.hist.length>2000) w.hist.splice(0,w.hist.length-2000);
}
function worldStep(w,st,dt){
  const g=w.g;
  if(w.view==='ideal'&&w.dragW!==null) return false;          /* PhET pauses the Ideal screen while the wall is dragged */
  g.heat=(w.view==='diffusion'||w.view==='pressure'||w.view==='equil')?0:st.heat;
  const n0=gasCount(g,0), n1=gasCount(g,1), Tb=g.T, Wb=g.W;
  if(w.view==='explore') g.wallSpeed=st.wallU;
  gasStep(g,dt);
  /* the moving wall: each push is measured against the adiabat through the
     state it started from */
  if(w.view==='explore'){
    if(g.u!==0&&!w.moving){ w.moving=true; w.T0=Tb; w.W0=Wb; w.trace=[[Wb,Tb===null?NaN:Tb,g.t-dt]]; }
    else if(g.u===0) w.moving=false;
  }
  if(w.view==='ideal') idealRecord(w);
  if(w.view==='explore'){ w.trace.push([g.W,g.T===null?NaN:g.T,g.t]); if(w.trace.length>4000) w.trace.splice(0,w.trace.length-4000); }
  if(w.view==='diffusion'){ w.hist.push([g.t,gasCOM(g,0),gasCOM(g,1)]); if(w.hist.length>3000) w.hist.splice(0,w.hist.length-3000); }
  if(w.view==='pressure') pressureRecord(w);
  if(w.view==='equil') equilRecord(w);
  return gasCount(g,0)!==n0||gasCount(g,1)!==n1;
}
/* the pressure view's running averages, sampled each frame */
function pressureRecord(w){
  const g=w.g, m=pressureModel(w);
  w.hist.push([g.imp.t,m.Pwall,m.Pgauge,m.Zwall]);
  if(w.hist.length>3000) w.hist.splice(0,w.hist.length-3000);
}

/* ---- the models the readout and the views read ------------------------------ */
function fmtT(T,st){ if(T===null||T===undefined||!isFinite(T)) return '—'; return st.unitT==='C'?sigf(T-273.15,4)+' °C':sigf(T,4)+' K'; }
function fmtP(Pk,st){ if(!isFinite(Pk)) return '—'; return st.unitP==='kPa'?Math.round(Pk)+' kPa':fmt(Pk*GAS.ATM_PER_KPA,1)+' atm'; }
function zJ(e){ return e*GAS.KG_PER_AMU*1e21; }       /* AMU pm^2/ps^2 -> zJ, PhET's AMU */
/* the pressure the walls feel against PhET's gauge (the pressure view) */
function pressureModel(w){
  const g=w.g, N=gasCount(g), E=gasEnergy(g), I=g.imp, t=I.t;
  const S=g.species[0], r=S.r, a=g.W-2*r, b=g.H-2*r;
  const Fx=t>0?(I.L+I.R)/(2*t):0, Fy=t>0?(I.B+I.T)/(2*t):0;          /* mean force on an x-wall, a y-wall */
  const Pwall=Fx/(g.H*g.D)*GAS.P_SCALE;                               /* kPa, per wall area H x D */
  const Pgauge=gasPressureOf(N,gasTemp(g),gasVolume(g));
  let sx=0; for(let i=0;i<g.n;i++) if(!g.out[i]) sx+=gasMass(g,i)*g.vx[i]*g.vx[i];
  const xshare=E>0?sx/E:null;                                         /* Σ m vx² / E: 1 if isotropic */
  const V=gasVirial(g), Zwall=t>0&&E>0?(a*Fx+b*Fy)/(2*E):null;        /* the wall-measured compressibility */
  const Zpair=t>0&&E>0?1+g.vir.pair/t/(2*E):null;
  const eta=N*Math.PI*r*r/(g.W*g.H);
  const z1=g.collisions&&N>1?hdZ1(N,2*r,a,b):0;
  const zTh=1+z1*(1+HD_B3_RATIO*hdB2(2*r)*N/(a*b));
  const kin=1.5*g.W/a;                                                 /* the 3/2 and the excluded strip */
  return {N,E,t,Fx,Fy,Pwall,Pgauge,ratio:Pgauge>0?Pwall/Pgauge:null,Zwall,Zpair,eta,z1,zTh,kin,xshare,
          pred:Pgauge*kin*(Zpair===null?zTh:Zpair),predTh:Pgauge*kin*zTh,vir:V,hits:I.hitsL+I.hitsR+I.hitsB+I.hitsT,
          pairs:g.stats.pairHits};
}
function buildModel(){
  const st=ST, view=st.view, w=worldOf(view), g=w.g;
  const N=gasCount(g), nH=gasCount(g,0), nL=gasCount(g,1);
  const M={view,st,w,g,N,nH,nL,T:g.T,P:g.P,gauge:g.gaugeP,Wnm:g.W/1000,t:g.t,oops:g.oops};
  if(BOXVIEWS[view]){
    M.kT2=g.T===null?null:gasKT2(g.T);
    M.lidOpen=gasLidOpen(g); M.opening=gasOpening(g);
    /* the invariant the chosen hold keeps (noise-free P): Gay-Lussac P/T, Boyle
       PV, Charles V/T, and N T at fixed P and V */
    const Vn=gasVolume(g)/1e9, T=g.T;
    M.inv=(!T||!N)?null:g.hold==='volume'?['P / T (Gay-Lussac)',sigf(g.P/T,5)+' kPa/K']
      :g.hold==='temperature'?['P V (Boyle)',sigf(g.P*Vn,5)+' kPa nm³']
      :g.hold==='pressureV'?['V / T (Charles)',sigf(Vn/T,5)+' nm³/K']
      :g.hold==='pressureT'?['N T (P and V fixed)',sigf(N*T,5)+' K']:null;
  }
  if(view==='explore'){
    M.u=g.u; M.work=g.led.work;
    M.TV=(g.T&&w.T0)?(g.T*g.W)/(w.T0*w.W0):null;
    const cnt=[nH,nL], rad=[g.species[0].r,g.species[1].r];
    M.Tad=(g.T&&w.T0)?w.T0*hdAdiabatRatio(cnt,rad,w.W0,g.W,g.H,64):null;
    const mBar=N?(nH*g.species[0].m+nL*g.species[1].m)/N:null;
    M.c=(M.kT2&&mBar)?gasSound(M.kT2,mBar):null; M.mach=M.c?Math.abs(g.u)/M.c:null;
    M.machLimit=M.c?g.wallSpeed/M.c:null;
  }
  if(view==='energy'){
    const S=g.sampler; M.mean=S?S.mean:[null,null];
    M.mb=[M.kT2?mbMeanSpeed(g.species[0].m,M.kT2):null, M.kT2?mbMeanSpeed(g.species[1].m,M.kT2):null];
  }
  if(view==='diffusion'){
    M.side=gasSideData(g); M.com=[gasCOM(g,0),gasCOM(g,1)]; M.flow=g.flow;
  }
  if(view==='pressure') M.pr=pressureModel(w);
  if(view==='equil'){ M.eh=equilH(g); const last=w.hist[w.hist.length-1]; M.last=last; }
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function readoutHTML(M){
  const st=M.st, g=M.g;
  let s='<div class="rname">gas properties<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(BOXVIEWS[M.view]){
    s+=hd('the gas')+rrow('heavy, light',M.nH+', '+M.nL+(gasOutside(g)?' (+'+gasOutside(g)+' escaping)':''))
      +rrow('temperature T',fmtT(M.T,st),'good')
      +rrow('pressure, the gauge',g.pOn?fmtP(M.gauge,st):'0 (no wall hit yet)')
      +rrow('P = NkT/V, no noise',fmtP(M.P,st))
      +rrow('width, volume',fmt(M.Wnm,2)+' nm, '+sigf(gasVolume(g)/1e9,4)+' nm³')
      +rrow('mean KE',M.N?sigf(zJ(gasEnergy(g)/M.N),4)+' zJ':'—');
    if(M.view==='ideal') s+=hd('hold constant')+rrow('held',HOLDS.find(h=>h.id===g.hold).name,'good')
      +(M.inv?rrow(M.inv[0],M.inv[1],'good'):rrow('nothing held','P, V and T all free'));
    if(M.view==='explore'){
      s+=hd('the wall')+rrow('wall speed u',g.u===0?'still':sigf(Math.abs(g.u),3)+' m/s '+(g.u>0?'in':'out'),g.u!==0?'good':'')
        +rrow('speed limit, as a Mach number',M.machLimit===null?'—':fmt(g.wallSpeed,0)+' m/s = '+fmt(M.machLimit,2)+' c',M.machLimit>1?'bad':'')
        +rrow('work done by the wall',sigf(zJ(M.work),4)+' zJ')
        +rrow('T w / T₀ w₀ (1 for points)',M.TV===null?'—':fmt(M.TV,3))
        +rrow('T / T on the hard-disk adiabat',M.Tad===null?'—':fmt(M.T/M.Tad,3),M.Tad&&M.T/M.Tad>1.02?'bad':'good');
    }
    if(M.view==='energy'){
      s+=hd('average speed (1-ps mean)')+rrow('heavy, measured',M.mean[0]===null?'—':sigf(M.mean[0],4)+' m/s','good')
        +rrow('heavy, Maxwell–Boltzmann',M.mb[0]===null?'—':sigf(M.mb[0],4)+' m/s')
        +rrow('light, measured',M.mean[1]===null?'—':sigf(M.mean[1],4)+' m/s','good')
        +rrow('light, Maxwell–Boltzmann',M.mb[1]===null?'—':sigf(M.mb[1],4)+' m/s')
        +rrow('injection temperature',g.injectT===null?'the container’s':sigf(g.injectT,3)+' K')
        +rrow('particle collisions',g.collisions?'on':'off',g.collisions?'':'bad');
    }
    if(st.showWatch||st.showCounter) s+=hd('tools');
    if(st.showWatch) s+=rrow('stopwatch',fmt(g.watch.t,2)+' ps'+(g.watch.on?' (running)':''));
    if(st.showCounter) s+=rrow('wall collisions',g.counter.count+' in '+fmt(g.counter.t,2)+' of '+g.counter.period+' ps');
    s+='</table><div class="note">PhET&rsquo;s definitions: T = (2/3)&lang;KE&rang;/k and P = NkT/V with V = width &times; 8.75 nm &times; 4 nm. The particles move in two dimensions, so the walls actually receive 3/2 of this pressure &mdash; see <b>the pressure</b>.</div>';
    return s;
  }
  if(M.view==='diffusion'){
    const D=M.side, sp=g.species;
    s+=hd('left of the divider')+rrow('particle 1, particle 2',D[0].n0+', '+D[0].n1)+rrow('average T',fmtT(D[0].T,st));
    s+=hd('right of the divider')+rrow('particle 1, particle 2',D[1].n0+', '+D[1].n1)+rrow('average T',fmtT(D[1].T,st));
    s+=hd('centre of mass (from the middle)')+rrow('particle 1',M.com[0]===null?'—':sigf(M.com[0]/1000,3)+' nm','good')
      +rrow('particle 2',M.com[1]===null?'—':sigf(M.com[1]/1000,3)+' nm','good');
    if(M.flow) s+=hd('particle flow (particles/ps)')+rrow('particle 1 → left, → right',fmt(M.flow.rateL[0],2)+', '+fmt(M.flow.rateR[0],2))
      +rrow('particle 2 → left, → right',fmt(M.flow.rateL[1],2)+', '+fmt(M.flow.rateR[1],2));
    s+=hd('Graham')+rrow('&radic;(m₁/m₂)',fmt(Math.sqrt(sp[0].m/sp[1].m),3));
    s+='</table><div class="note">'+(g.divided?'The divider is in: each species is confined to its own side.':'The divider is out: the flow rates count crossings of the middle line, averaged over 300 frames as PhET does.')+'</div>';
    return s;
  }
  if(M.view==='pressure'){
    const P=M.pr;
    s+=hd(P.N+' heavy disks, '+(g.collisions?'colliding':'collisions off'))
      +rrow('PhET&rsquo;s gauge, NkT/V',fmtP(P.Pgauge,st))
      +rrow('the walls feel (measured)',P.t>0?fmtP(P.Pwall,st):'—','good')
      +rrow('ratio, measured',P.ratio===null?'—':fmt(P.ratio,4),'good')
      +rrow('3/2 &times; W/(W&minus;2r)',fmt(P.kin,4))
      +rrow('&times; Z = 1 + pair virial / 2E',P.Zpair===null?'—':fmt(P.Zpair,4))
      +rrow('&Sigma; m v<sub>x</sub>&sup2; / E now (1 if isotropic)',P.xshare===null?'—':fmt(P.xshare,3),g.collisions?'':'bad');
    s+=hd('Z, the hard-disk law')+rrow('area fraction &eta;',fmt(P.eta,4))
      +rrow('Z, measured at the walls',P.Zwall===null?'—':fmt(P.Zwall,4),'good')
      +rrow('Z, from the collisions',P.Zpair===null?'—':fmt(P.Zpair,4),'good')
      +rrow('Z, B₂ and B₃ theory',fmt(P.zTh,4))
      +rrow('run so far',fmt(P.t,1)+' ps, '+P.hits+' wall hits');
    s+=hd('the virial ledger')+rrow('d(&Sigma;m r·v) &minus; (2KE + wall + pair)',P.vir.scale>0?(P.vir.resid/P.vir.scale).toExponential(1)+' of the terms':'—');
    s+='</table><div class="note">The two Z&rsquo;s differ only by the finite-run boundary term d(&Sigma;m r&middot;v)/2E&middot;t, which shrinks as 1/t.</div>';
    return s;
  }
  /* equilibrium */
  const L=M.last, N=M.N;
  s+=hd(N+' disks, '+(g.collisions?'colliding':'collisions off'))
    +rrow('time',fmt(g.t,2)+' ps')+rrow('collisions per disk',N?fmt(2*g.stats.pairHits/N,1):'—')
    +rrow('Boltzmann&rsquo;s H (relative entropy)',M.eh.H===null?'—':sigf(M.eh.H,3),'good')
    +rrow('its sampling floor (K&minus;1)/2N',M.eh.floor===null?'—':sigf(M.eh.floor,3))
    +rrow('heavy &lang;KE&rang; / &lang;KE&rang;',L&&L[2]!==null?fmt(L[2],3):'—','good')
    +rrow('light &lang;KE&rang; / &lang;KE&rang;',L&&L[3]!==null?fmt(L[3],3):'—','good')
    +rrow('temperature (conserved)',fmtT(g.T,st));
  s+='</table><div class="note">With collisions off nothing relaxes: every disk keeps its speed, walls only turn it.</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='ideal'){
    const h=M.g.hold, hl=(x,on)=>on?'<span class="hl">'+x+'</span>':x;
    return E(hl('P',h==='pressureV'||h==='pressureT')+' '+hl('V',h==='volume')+' = N k '+hl('T',h==='temperature')+' &nbsp;&middot;&nbsp; T = (2/3)&lang;KE&rang;/k &nbsp;&middot;&nbsp; k = 8316 AMU pm&sup2;/(ps&sup2; K)',
      'the ideal gas law, with '+(h==='nothing'?'nothing held':HOLDS.find(x=>x.id===h).name+' held')+' — hold one of P, V, T and the other two answer');
  }
  if(M.view==='explore') return E('v&prime;<sub>x</sub> = 2u &minus; v<sub>x</sub> &nbsp;&middot;&nbsp; dE = &minus;F<sub>x</sub> dW, F<sub>x</sub>(W&minus;2r) = E Z &nbsp;&rArr;&nbsp; <span class="hl">ln '+'T<sub>1</sub>/T<sub>0</sub> = &int; Z dW/(W&minus;2r)</span> &nbsp;(points: T V = const, &gamma; = 2)',
    'each bounce off the moving wall adds 2mu(u − v); pushed slowly the disks warm along their adiabat, pushed faster than sound they are shocked above it');
  if(M.view==='energy') return E('<span class="hl">f(v) = (m v / kT<sub>2</sub>) e<sup>&minus;mv&sup2;/2kT<sub>2</sub></sup></span>, &nbsp; kT<sub>2</sub> = &frac32; kT &nbsp;&middot;&nbsp; &lang;v&rang; = &radic;(&pi;kT<sub>2</sub>/2m) &nbsp;&middot;&nbsp; f(E) = e<sup>&minus;E/kT<sub>2</sub></sup>/kT<sub>2</sub>',
    'the 2-D Maxwell–Boltzmann laws: the same energy law for both species, speeds scaled by 1/√m');
  if(M.view==='diffusion') return E('flux = n &lang;v<sub>x</sub><sup>+</sup>&rang; = n &radic;(kT<sub>2</sub>/2&pi;m) &nbsp;&rArr;&nbsp; <span class="hl">rate &prop; 1/&radic;m</span> &nbsp;(Graham)',
    'take the divider out and each species crosses the middle at a rate set by its density and its mean speed');
  if(M.view==='pressure') return E('F<sub>x</sub> (W&minus;2r) + F<sub>y</sub> (H&minus;2r) = 2E + &Sigma;<sub>collisions</sub> &sigma;|J| &nbsp;&rArr;&nbsp; <span class="hl">P<sub>wall</sub> = &frac32; &middot; W/(W&minus;2r) &middot; Z &middot; NkT/V</span>',
    'the virial theorem: the walls feel the kinetic 2E plus what the collisions carry across the box');
  return E('<span class="hl">H(t) = &Sigma; p<sub>k</sub> ln(p<sub>k</sub>/q<sub>k</sub>) &rarr; 0</span> &nbsp;&middot;&nbsp; q = e<sup>&minus;E/kT<sub>2</sub></sup> &nbsp;&middot;&nbsp; &lang;KE<sub>heavy</sub>&rang; = &lang;KE<sub>light</sub>&rang;',
    'Boltzmann’s H falls as collisions shuffle energy; at equilibrium every disk shares it alike, whatever its mass');
}
function tagHTML(M){
  if(M.view==='ideal') return '<b>the gas law</b> — PhET&rsquo;s Ideal screen'+(M.g.hold!=='nothing'?', holding '+HOLDS.find(h=>h.id===M.g.hold).name:'');
  if(M.view==='explore') return '<b>the moving wall</b> — PhET&rsquo;s Explore screen: the left wall does work';
  if(M.view==='energy') return '<b>the energy</b> — PhET&rsquo;s Energy screen'+(M.g.collisions?'':', collisions off');
  if(M.view==='diffusion') return '<b>diffusion</b> — PhET&rsquo;s Diffusion screen'+(M.g.divided?', divided':', mixing');
  if(M.view==='pressure') return '<b>the pressure</b> — momentum at the walls against PhET&rsquo;s gauge';
  return '<b>equilibrium</b> — from '+STARTS.find(s=>s.id===M.st.eStart).name+' to Maxwell–Boltzmann';
}
