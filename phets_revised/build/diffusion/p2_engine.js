/* ================================================================== *
 *  the gas engine                                                  *
 *  Taken UNCHANGED from build/gas-properties/p2_engine.js         *
 *  (the finished gas-properties remake).  Do not edit here.          *
 * ================================================================== */

/* ================================================================== *
 *  THE GAS ENGINE — particles, collisions, walls, heating, the lid,   *
 *  the hold-constant logic and the statistics.  No DOM, no view       *
 *  state: gases-intro and diffusion are built on this part unchanged. *
 *  API and invariants: build/gas-properties/ENGINE.md.                *
 * ================================================================== */

/* PhET's values, read from docs/phets/gas-properties_en.html (1.1.10):
   GasPropertiesConstants, GasPropertiesQueryParameters, BaseContainer,
   IdealGasLawContainer, PressureModel, TemperatureModel, HistogramsModel,
   CollisionCounter, DiffusionContainer, DiffusionSettings, TimeTransform. */
const GAS={
  K:8316,                    /* BOLTZMANN, AMU pm^2 ps^-2 K^-1 (CODATA: 8314.46) */
  KG_PER_AMU:1.66e-27,
  ATM_PER_KPA:0.00986923,
  P_SCALE:1.66e6,            /* kPa per AMU/(pm ps^2) = KG_PER_AMU*1e33 */
  H:8750, D:4000, WALL:75,   /* container height, depth, wall thickness, pm */
  WMIN:5000, WMAX:15000, WDEF:10000,
  HEAVY:{m:28,r:125}, LIGHT:{m:4,r:87.5},
  NMAX:1000,                 /* per species (Ideal, Explore, Energy) */
  DT_FRAME:2.5/60,           /* ps per frame at 60 fps: 1 ps = 0.4 s (TimeTransform NORMAL) */
  DT_SLOW:0.3/60,            /* TimeTransform SLOW (Diffusion) */
  STEP:0.2,                  /* MODEL_TIME_STEP, the step button, ps */
  HEAT_COOL:800,             /* heatCool: speeds scale by 1 + a/800 per 60-fps frame */
  P_MAX:2e4,                 /* maxPressure, kPa: the lid blows off above this */
  T_MAX:1e5,                 /* maxTemperature, K */
  WALL_SPEED:800,            /* wallSpeedLimit, pm/ps (Explore) */
  LID_THICK:175, OPEN_L:1250, OPEN_R:2000, LID_WIDE:1500,
  ENTRY_Y:8750/5,            /* particleEntryPosition = (0, H/5); a particle enters at x = -r */
  FAN:Math.PI/2,             /* the pump's dispersion angle */
  T0:300,                    /* defaultInitialTemperature, K */
  P_REFRESH:0.75,            /* PressureModel REFRESH_PERIOD, ps */
  PERIODS:[5,10,20],         /* CollisionCounter SAMPLE_PERIODS, ps (default 10) */
  NBIN:19, SBIN:170, EBIN:8e5, SAMPLE:1,   /* HistogramsModel; 1-ps averaging */
  MAXTIME:999.99,            /* the stopwatch's range, ps */
  DIFF_W:16000, DIVIDER:100, /* DiffusionContainer */
  DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,
  FLOW_WINDOW:300            /* ParticleFlowRateModel: running average of 300 samples */
};

/* ---- the random stream: mulberry32 (bit-exact twin in derive.py) ---------- */
function gasRng(seed){
  let a=seed>>>0;
  const R={
    next(){
      a=(a+0x6D2B79F5)>>>0;
      let t=Math.imul(a^(a>>>15),a|1);
      t=((t+Math.imul(t^(t>>>7),t|61))>>>0)^t;
      return ((t^(t>>>14))>>>0)/4294967296;
    },
    /* Box-Muller, one pair of draws per value (no caching: a draw count that
       does not depend on history keeps the stream reproducible) */
    gauss(){ const u1=1-R.next(), u2=R.next(); return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2); }
  };
  return R;
}

/* ---- the 2-D Maxwell-Boltzmann laws, in PhET's units ------------------------
   PhET defines T by <KE> = (3/2) k T although the particles move in two
   dimensions, so the energy per quadratic degree of freedom is kT2/2 with
   kT2 = (3/2) k T.  Speed pdf (m v/kT2) exp(-m v^2/2kT2); energy pdf
   exp(-e/kT2)/kT2 (two dof: an exponential). */
function gasKT2(T){ return 1.5*GAS.K*T; }
function mbSpeedPdf(v,m,kT2){ return v<0?0:m*v/kT2*Math.exp(-m*v*v/(2*kT2)); }
function mbSpeedCdf(v,m,kT2){ return v<=0?0:-Math.expm1(-m*v*v/(2*kT2)); }
function mbEnergyPdf(e,kT2){ return e<0?0:Math.exp(-e/kT2)/kT2; }
function mbEnergyCdf(e,kT2){ return e<=0?0:-Math.expm1(-e/kT2); }
function mbMeanSpeed(m,kT2){ return Math.sqrt(Math.PI*kT2/(2*m)); }
function mbModeSpeed(m,kT2){ return Math.sqrt(kT2/m); }
function mbRmsSpeed(m,kT2){ return Math.sqrt(2*kT2/m); }
/* the finite-N law in a closed box: energy fractions uniform on the simplex,
   so one disk's energy e of a total E has F(e) = 1 - (1 - e/E)^(N-1) */
function mcEnergyCdf(e,E,N){ if(e<=0) return 0; if(e>=E) return 1; return -Math.expm1((N-1)*Math.log1p(-e/E)); }
/* hard disks: the second virial coefficient, B3/B2^2, the contact measure of a
   circle of radius s over an a x b rectangle of centres, and the first-order
   compressibility excess of N equal disks in that rectangle */
function hdB2(s){ return Math.PI*s*s/2; }
const HD_B3_RATIO=4/3-Math.sqrt(3)/Math.PI;
function hdContact(a,b,s){ return 2*Math.PI*s*a*b-4*s*s*(a+b)+2*s*s*s; }
function hdZ1(N,s,a,b){ return (N-1)*s*hdContact(a,b,s)/(4*(a*b)*(a*b)); }
/* Z of the gas in a W x H box: every like and unlike pair at first order (the
   per-pair virial sigma kT2 M/(ab)^2 over 2E), times the bulk B3 factor when
   there is one species (derive.py section 7) */
function hdZ(counts,radii,W,H){
  const N=counts[0]+counts[1]; if(N<2) return 1;
  let S=0;
  for(let i=0;i<2;i++) for(let j=i;j<2;j++){
    const np=i===j?counts[i]*(counts[i]-1)/2:counts[i]*counts[j];
    if(np<=0) continue;
    const s=radii[i]+radii[j], a=W-s, b=H-s;
    S+=np*s*hdContact(a,b,s)/((a*b)*(a*b));
  }
  let z=S/(2*N);
  if(counts[0]===0||counts[1]===0){ const k=counts[0]?0:1, s=2*radii[k], a=W-s, b=H-s; z*=1+HD_B3_RATIO*hdB2(s)*N/(a*b); }
  return 1+z;
}
/* the quasi-static adiabat of hard disks (derive.py section 9): pushed slowly
   the gas stays in equilibrium, dE = -F_x dW with F_x (W - 2r) = E Z(W), so
   ln(T1/T0) = int_{W1}^{W0} Z dW/(W - 2r) (composite Simpson, n intervals).
   For points (r = 0, Z = 1) it is T W = const; for a mixture r is the
   number-weighted mean radius. */
function hdAdiabatRatio(counts,radii,W0,W1,H,n){
  n=n||256; if(n%2) n++;
  const N=counts[0]+counts[1], rb=N?(counts[0]*radii[0]+counts[1]*radii[1])/N:0;
  const f=W=>hdZ(counts,radii,W,H)/(W-2*rb), hstep=(W0-W1)/n;
  if(hstep===0) return 1;
  let s=f(W1)+f(W0);
  for(let k=1;k<n;k++) s+=(k%2?4:2)*f(W1+k*hstep);
  return Math.exp(s*hstep/3);
}
/* the speed of sound in the 2-D gas: c^2 = gamma P/rho = 2 kT2/<m> */
function gasSound(kT2,mMean){ return Math.sqrt(2*kT2/mMean); }

/* ---- the gas -------------------------------------------------------------- */
function gasMake(o){
  o=o||{};
  const W=o.width||GAS.WDEF;
  const g={
    /* particles, structure of arrays (grown on demand) */
    cap:0, n:0, x:null, y:null, vx:null, vy:null, sp:null, out:null, id:null, lt:null, st:null, px:null,
    nextId:1,
    species:(o.species||[{m:GAS.HEAVY.m,r:GAS.HEAVY.r},{m:GAS.LIGHT.m,r:GAS.LIGHT.r}]).map(s=>({m:s.m,r:s.r})),
    /* the container: x in [left, 0], y in [0, H]; PhET's origin is the bottom-right corner */
    W, H:o.height||GAS.H, D:o.depth||GAS.D, left:-W,
    wRange:o.wRange||[GAS.WMIN,GAS.WMAX],
    wantW:W, u:0, doesWork:!!o.doesWork, wallSpeed:o.wallSpeed||GAS.WALL_SPEED,
    lid:o.noLid?null:{on:true,width:0}, divided:!!o.divided, dividerX:-W/2, dividerHalf:GAS.DIVIDER/2,
    collisions:o.collisions!==false,
    heat:0, hold:'nothing', holdP:null, injectT:null,
    t:0, rng:gasRng(o.seed===undefined?1:o.seed), noise:gasRng(((o.seed===undefined?1:o.seed)^0x5bd1e995)>>>0),
    noiseOn:o.noise!==false,
    /* the model quantities PhET displays */
    T:null, P:0, gaugeP:0, pOn:false, pAcc:0, oops:null,
    /* the energy ledger: E == E0 + work + heatQ + inj - rem - esc + setT */
    led:{E0:0, work:0, heatQ:0, inj:0, rem:0, esc:0, setT:0},
    /* the virial ledger (closed boxes): G1 - G0 == kin + wall + pair + heat */
    vir:{on:!!o.virial, G0:0, kin:0, wall:0, pair:0, heat:0, esc:0},
    /* wall impulses (the pressure the walls feel), per wall, since resetImpulse */
    imp:{L:0, R:0, B:0, T:0, t:0, hitsL:0, hitsR:0, hitsB:0, hitsT:0, E:0},
    /* counters */
    stats:{pairHits:0, wallHits:0, frameWallHits:0, events:0, stale:0, eventCap:0, fastMiss:0, substeps:0},
    counter:{on:false, count:0, t:0, period:10},
    watch:{on:false, t:0},
    /* PhET's 1-ps sampler for the Energy screen (HistogramsModel + AverageSpeedModel) */
    sampler:null,
    /* the particle-flow counters for the Diffusion screen */
    flow:null,
    /* work arrays for the substep */
    _cellHead:null, _cellNext:null
  };
  if(g.lid) g.lid.width=gasMaxLid(g);
  if(o.virial) g.vir.on=true;
  return g;
}
function gasGrow(g,need){
  if(need<=g.cap) return;
  let c=Math.max(64,g.cap);
  while(c<need) c*=2;
  const F=a=>{ const b=new Float64Array(c); if(a) b.set(a.subarray(0,g.n)); return b; };
  const I=a=>{ const b=new Int32Array(c); if(a) b.set(a.subarray(0,g.n)); return b; };
  g.x=F(g.x); g.y=F(g.y); g.vx=F(g.vx); g.vy=F(g.vy); g.lt=F(g.lt); g.px=F(g.px);
  g.sp=I(g.sp); g.out=I(g.out); g.id=I(g.id); g.st=I(g.st);
  g.cap=c; g._cellNext=new Int32Array(c); g._cellOf=new Int32Array(c);
}
function gasPush(g,k,x,y,vx,vy){
  gasGrow(g,g.n+1);
  const i=g.n++;
  g.x[i]=x; g.y[i]=y; g.vx[i]=vx; g.vy[i]=vy; g.sp[i]=k; g.out[i]=0; g.id[i]=g.nextId++; g.lt[i]=0; g.st[i]=0; g.px[i]=x;
  return i;
}
/* swap-remove: order changes, but every loop in this file is order-free
   except the event heap, which is rebuilt each substep */
function gasKill(g,i){
  const j=--g.n;
  if(i!==j){ g.x[i]=g.x[j]; g.y[i]=g.y[j]; g.vx[i]=g.vx[j]; g.vy[i]=g.vy[j]; g.sp[i]=g.sp[j]; g.out[i]=g.out[j];
    g.id[i]=g.id[j]; g.lt[i]=g.lt[j]; g.st[i]=g.st[j]; g.px[i]=g.px[j]; }
}
function gasMass(g,i){ return g.species[g.sp[i]].m; }
function gasRad(g,i){ return g.species[g.sp[i]].r; }
function gasKE(g,i){ const m=g.species[g.sp[i]].m; return 0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]); }

/* ---- counts, energy, temperature, pressure -------------------------------- */
function gasCount(g,k){ let c=0; for(let i=0;i<g.n;i++) if(!g.out[i]&&(k===undefined||g.sp[i]===k)) c++; return c; }
function gasOutside(g){ let c=0; for(let i=0;i<g.n;i++) if(g.out[i]) c++; return c; }
function gasEnergy(g,k){ let e=0; for(let i=0;i<g.n;i++) if(!g.out[i]&&(k===undefined||g.sp[i]===k)) e+=gasKE(g,i); return e; }
/* PhET's temperature: T = (2/3)<KE>/k over the particles in the container */
function gasTemp(g,k){ const n=gasCount(g,k); return n?(2/3)*gasEnergy(g,k)/n/GAS.K:null; }
function gasVolume(g){ return g.W*g.H*g.D; }
/* PhET's pressure: P = N k T / V, in kPa (no noise) */
function gasPressureOf(N,T,V){ return N*GAS.K*(T||0)/V*GAS.P_SCALE; }
function gasLedger(g){
  const L=g.led, E=gasEnergy(g);
  return {E, pred:L.E0+L.work+L.heatQ+L.inj-L.rem-L.esc+L.setT, resid:E-(L.E0+L.work+L.heatQ+L.inj-L.rem-L.esc+L.setT)};
}
function gasLedgerReset(g){
  const L=g.led; L.E0=gasEnergy(g); L.work=0; L.heatQ=0; L.inj=0; L.rem=0; L.esc=0; L.setT=0;
}
function gasG(g){ let G=0; for(let i=0;i<g.n;i++) if(!g.out[i]){ const m=gasMass(g,i); G+=m*(g.x[i]*g.vx[i]+g.y[i]*g.vy[i]); } return G; }
function gasVirialReset(g){ const V=g.vir; V.on=true; V.G0=gasG(g); V.kin=0; V.wall=0; V.pair=0; V.heat=0; V.esc=0; }
function gasVirial(g){
  const V=g.vir, G1=gasG(g), rhs=V.kin+V.wall+V.pair+V.heat+V.esc;
  return {dG:G1-V.G0, rhs, resid:(G1-V.G0)-rhs, scale:Math.abs(V.kin)+Math.abs(V.wall)+Math.abs(V.pair)+Math.abs(V.heat)+Math.abs(V.esc)};
}
function gasImpulseReset(g){ const I=g.imp; I.L=0; I.R=0; I.B=0; I.T=0; I.t=0; I.hitsL=0; I.hitsR=0; I.hitsB=0; I.hitsT=0; I.E=0; }

/* ---- the container: width, lid, divider ------------------------------------ */
function gasMaxLid(g){ return g.W-GAS.OPEN_R+GAS.WALL; }
function gasMinLid(){ return GAS.OPEN_L+GAS.WALL; }
function gasOpenLeft(g){
  if(!g.lid) return 0;
  return g.lid.on?Math.round(g.left-GAS.WALL+g.lid.width):g.left+GAS.OPEN_L;
}
function gasOpenRight(){ return -GAS.OPEN_R; }
function gasLidOpen(g){ return !!g.lid&&(!g.lid.on||g.lid.width<gasMaxLid(g)); }
function gasOpening(g){ return gasLidOpen(g)?Math.max(0,gasOpenRight()-gasOpenLeft(g)):0; }
function gasSetLid(g,w){ if(!g.lid||!g.lid.on) return; g.lid.width=Math.min(gasMaxLid(g),Math.max(gasMinLid(),w)); }
function gasBlowLid(g){ if(g.lid&&(!gasLidOpen(g)||gasOpening(g)<GAS.LID_WIDE)) g.lid.on=false; }
function gasReturnLid(g){ if(g.lid){ g.lid.on=true; g.lid.width=gasMaxLid(g); } }
/* the width changes; with the lid on, the opening keeps its size (PhET setWidth) */
function gasWidthTo(g,w){
  if(w===g.W) return;
  const open=g.lid&&g.lid.on?gasOpenRight()-gasOpenLeft(g):0;
  g.W=w; g.left=-w;
  if(g.lid&&g.lid.on) g.lid.width=Math.max(gasMaxLid(g)-open,gasMinLid());
}
/* the Ideal screen's resize: the wall does no work; afterwards every particle's
   x is scaled about the right wall (PhET redistributeParticles), and any that
   the scaling leaves overlapping the new left wall is set against it */
function gasResize(g,w,redistribute){
  w=Math.min(g.wRange[1],Math.max(g.wRange[0],w));
  const ratio=w/g.W;
  gasWidthTo(g,w); g.wantW=w;
  if(redistribute) for(let i=0;i<g.n;i++) if(!g.out[i]){
    g.x[i]*=ratio;
    const r=gasRad(g,i); if(g.x[i]-r<g.left) g.x[i]=g.left+r; if(g.x[i]+r>0) g.x[i]=-r;
  }
  return w;
}
function gasSetDivided(g,on){ g.divided=!!on; g.dividerX=g.left+g.W/2; }
/* the x-range a particle's CENTRE may occupy: the left wall (which may move),
   the right wall, and the divider for the two diffusion species */
function gasXlo(g,k){ return (g.divided&&k===1)?g.dividerX+g.dividerHalf:null; }   /* null = the moving left wall */
function gasXhi(g,k){ return (g.divided&&k===0)?g.dividerX-g.dividerHalf:0; }

/* ---- adding and removing particles ----------------------------------------- */
/* PhET's addParticles: n particles of species k at (-r, H/5), every one at a
   speed sqrt(3kT_i/m) aimed into the pump's pi/2 fan pointing left.  With
   collisions on and n > 1 the T_i are Gaussian about T (sd 0.2T) with the
   mean restored exactly, so the container's temperature is not disturbed. */
function gasInjectT(g){
  if(g.injectT!==null) return g.injectT;
  const T=gasTemp(g); return T===null?GAS.T0:T;
}
function gasInject(g,k,n,T){
  const have=gasCount(g,k);
  n=Math.max(0,Math.min(n,GAS.NMAX-have));
  if(n<=0) return 0;
  if(T===undefined) T=gasInjectT(g);
  let Ts;
  if(n!==1&&g.collisions){
    Ts=[]; let s=0;
    for(let q=0;q<n;q++){ const v=T+0.2*T*g.rng.gauss(); Ts.push(v); s+=v; }
    const sh=T-s/n; for(let q=0;q<n;q++) Ts[q]=Math.max(0,Ts[q]+sh);
  } else { Ts=[]; for(let q=0;q<n;q++) Ts.push(T); }
  const S=g.species[k];
  for(let q=0;q<n;q++){
    const th=Math.PI-GAS.FAN/2+g.rng.next()*GAS.FAN, v=Math.sqrt(3*GAS.K*Ts[q]/S.m);
    const i=gasPush(g,k,-S.r,GAS.ENTRY_Y,v*Math.cos(th),v*Math.sin(th));
    g.led.inj+=gasKE(g,i);
  }
  return n;
}
/* uniform, non-overlapping placement (rejection; gives up after 200 tries and
   places the disk anyway) with 2-D Maxwell-Boltzmann velocities rescaled so the
   batch's mean KE is exactly (3/2)kT, or all at one speed (delta = true).  Not
   a PhET path: the house views open with a gas already in the box. */
function gasFill(g,k,n,T,delta,region){
  const S=g.species[k], R=g.rng, first=g.n;
  const x0=(region?region[0]:g.left)+S.r, x1=(region?region[1]:0)-S.r, y0=S.r, y1=g.H-S.r;
  for(let q=0;q<n;q++){
    let px=0,py=0;
    for(let tries=0;tries<200;tries++){
      px=x0+R.next()*(x1-x0); py=y0+R.next()*(y1-y0);
      let clash=false;
      for(let j=0;j<g.n&&!clash;j++) if(!g.out[j]){ const dx=px-g.x[j], dy=py-g.y[j], s=S.r+gasRad(g,j); if(dx*dx+dy*dy<s*s) clash=true; }
      if(!clash) break;
    }
    const kT2=gasKT2(T), sp=delta?mbRmsSpeed(S.m,kT2):Math.sqrt(-2*kT2/S.m*Math.log(1-R.next())), th=2*Math.PI*R.next();
    gasPush(g,k,px,py,sp*Math.cos(th),sp*Math.sin(th));
  }
  if(n>0){
    let e=0; for(let i=first;i<g.n;i++) e+=gasKE(g,i);
    const want=n*1.5*GAS.K*T, f=e>0?Math.sqrt(want/e):0;
    for(let i=first;i<g.n;i++){ g.vx[i]*=f; g.vy[i]*=f; g.led.inj+=gasKE(g,i); }
  }
  return n;
}
/* PhET's diffusion placement: uniform in the region, NO overlap rejection,
   every particle at sqrt(3kT/m) in a uniformly random direction */
function gasScatter(g,k,n,T,x0,x1){
  const S=g.species[k], R=g.rng, v=Math.sqrt(3*GAS.K*T/S.m);
  for(let q=0;q<n;q++){
    const px=(x0+S.r)+R.next()*((x1-S.r)-(x0+S.r)), py=S.r+R.next()*(g.H-2*S.r), th=2*Math.PI*R.next();
    const i=gasPush(g,k,px,py,v*Math.cos(th),v*Math.sin(th));
    g.led.inj+=gasKE(g,i);
  }
  return n;
}
/* remove the n most recently added particles of species k (PhET removeLastParticles) */
function gasRemove(g,k,n){
  const Tbefore=gasTemp(g);
  let removed=0;
  while(removed<n){
    let best=-1;
    for(let i=0;i<g.n;i++) if(!g.out[i]&&g.sp[i]===k&&(best<0||g.id[i]>g.id[best])) best=i;
    if(best<0) break;
    g.led.rem+=gasKE(g,best); gasKill(g,best); removed++;
  }
  if(removed) gasAfterRemove(g,Tbefore);
  return removed;
}
function gasRemoveAll(g){
  for(let i=g.n-1;i>=0;i--){ if(!g.out[i]) g.led.rem+=gasKE(g,i); gasKill(g,i); }
  gasAfterRemove(g,null);
}
function gasSetCount(g,k,n){ const c=gasCount(g,k); if(n>c) return gasInject(g,k,n-c); if(n<c) return -gasRemove(g,k,c-n); return 0; }
/* PhET: N -> 0 while holding T or P is an Oops; N falling while holding T
   restores T by rescaling every particle's energy */
function gasAfterRemove(g,Tbefore){
  const N=gasCount(g);
  if(N===0){
    if(g.hold==='temperature'){ g.hold='nothing'; g.oops='temperatureEmpty'; }
    else if(g.hold==='pressureV'||g.hold==='pressureT'){ g.hold='nothing'; g.oops='pressureEmpty'; }
    g.pOn=false; g.P=0; g.gaugeP=0; g.T=null;
  } else if(g.hold==='temperature'&&Tbefore!==null) gasSetTemp(g,Tbefore);
}
/* PhET setTemperature: every particle's KE is scaled by (3/2)kT/<KE> */
function gasSetTemp(g,T){
  const N=gasCount(g); if(!N) return;
  const E=gasEnergy(g), f=1.5*T*GAS.K/(E/N), s=Math.sqrt(f);
  for(let i=0;i<g.n;i++) if(!g.out[i]){ g.vx[i]*=s; g.vy[i]*=s; }
  g.led.setT+=gasEnergy(g)-E;
}

/* ---- the event heap (one substep) ------------------------------------------ */
const EVH={t:new Float64Array(1024), i:new Int32Array(1024), j:new Int32Array(1024), k:new Int32Array(1024),
           si:new Int32Array(1024), sj:new Int32Array(1024), n:0};
function evGrow(){
  const c=EVH.t.length*2, cp=(A,T)=>{ const b=new T(c); b.set(A); return b; };
  EVH.t=cp(EVH.t,Float64Array); EVH.i=cp(EVH.i,Int32Array); EVH.j=cp(EVH.j,Int32Array); EVH.k=cp(EVH.k,Int32Array);
  EVH.si=cp(EVH.si,Int32Array); EVH.sj=cp(EVH.sj,Int32Array);
}
function evSwap(a,b){
  let v=EVH.t[a]; EVH.t[a]=EVH.t[b]; EVH.t[b]=v;
  v=EVH.i[a]; EVH.i[a]=EVH.i[b]; EVH.i[b]=v; v=EVH.j[a]; EVH.j[a]=EVH.j[b]; EVH.j[b]=v;
  v=EVH.k[a]; EVH.k[a]=EVH.k[b]; EVH.k[b]=v; v=EVH.si[a]; EVH.si[a]=EVH.si[b]; EVH.si[b]=v;
  v=EVH.sj[a]; EVH.sj[a]=EVH.sj[b]; EVH.sj[b]=v;
}
function evPush(t,i,j,k,si,sj){
  if(EVH.n>=EVH.t.length) evGrow();
  let c=EVH.n++;
  EVH.t[c]=t; EVH.i[c]=i; EVH.j[c]=j; EVH.k[c]=k; EVH.si[c]=si; EVH.sj[c]=sj;
  while(c>0){ const p=(c-1)>>1; if(EVH.t[p]<=EVH.t[c]) break; evSwap(p,c); c=p; }
}
function evPop(){
  const last=--EVH.n;
  if(last>0){ evSwap(0,last); let c=0;
    for(;;){ const l=2*c+1, r=l+1; let m=c;
      if(l<last&&EVH.t[l]<EVH.t[m]) m=l; if(r<last&&EVH.t[r]<EVH.t[m]) m=r;
      if(m===c) break; evSwap(c,m); c=m; } }
  return last;                       /* the popped event sits at index `last` */
}

/* event kinds */
const EV_PAIR=0, EV_LEFT=1, EV_RIGHT=2, EV_BOT=3, EV_TOP=4, EV_ESC=5;

/* ---- the collision-time algebra (derivation: derive.py section 2) --------------
   Two disks at relative position dp, relative velocity dv, touching at |dp| = s:
   |dp + t dv|^2 = s^2 is a quadratic a t^2 + 2 b t + c = 0 with a = dv.dv,
   b = dp.dv, c = dp.dp - s^2.  They collide only if apart (c > 0) and
   approaching (b < 0), at the EARLIER root, which in the cancellation-free form
   is t = c / (-b + sqrt(b^2 - a c)).  Overlapping pairs (c < 0) get no event:
   they pass through each other, as in PhET, until they separate. */
function pairTime(dpx,dpy,dvx,dvy,s){
  const c=dpx*dpx+dpy*dpy-s*s;
  if(c<0) return Infinity;
  const b=dpx*dvx+dpy*dvy;
  if(b>=0) return Infinity;
  const a=dvx*dvx+dvy*dvy, d=b*b-a*c;
  if(d<0) return Infinity;
  return c/(-b+Math.sqrt(d));
}
/* the elastic impulse along the line of centres: exact momentum and energy
   conservation (derive.py checks it in rational arithmetic); returns the
   impulse delivered to i along n */
function pairResolve(g,i,j){
  const mi=gasMass(g,i), mj=gasMass(g,j);
  const dx=g.x[i]-g.x[j], dy=g.y[i]-g.y[j], d=Math.sqrt(dx*dx+dy*dy);
  const nx=dx/d, ny=dy/d;
  const gn=(g.vx[i]-g.vx[j])*nx+(g.vy[i]-g.vy[j])*ny;          /* < 0: approaching */
  const M=mi+mj, ci=2*mj/M*gn, cj=2*mi/M*gn;
  g.vx[i]-=ci*nx; g.vy[i]-=ci*ny; g.vx[j]+=cj*nx; g.vy[j]+=cj*ny;
  return -mi*ci*d;                   /* (r_i - r_j).J_i = |dp| |J| : the pair virial */
}

/* ---- one substep of length h: every event in time order -------------------- */
/* push i's next wall event and its pair events with every neighbour, from
   time t0 to the substep's end h.  `half` (the substep's opening prediction,
   t0 = 0) pushes each pair once, from its lower index; after an event, i is
   paired with everyone.  One routine for both, so a rule lives in one place. */
function gasPredict(g,i,t0,h,L0,u,G,half){
  const k=g.sp[i], S=g.species[k], r=S.r, x=g.x[i], y=g.y[i], vx=g.vx[i], vy=g.vy[i], si=g.st[i];
  /* the left bound: the moving left wall, or the divider for species 1 */
  const xlo=gasXlo(g,k);
  if(xlo===null){
    const xw=L0+u*t0;
    if(vx<u){ let dt=(xw+r-x)/(vx-u); if(dt<0) dt=0; if(t0+dt<=h) evPush(t0+dt,i,-1,EV_LEFT,si,0); }
  } else if(vx<0){ let dt=(xlo+r-x)/vx; if(dt<0) dt=0; if(t0+dt<=h) evPush(t0+dt,i,-1,EV_LEFT,si,0); }
  const xhi=gasXhi(g,k);
  if(vx>0){ let dt=(xhi-r-x)/vx; if(dt<0) dt=0; if(t0+dt<=h) evPush(t0+dt,i,-1,EV_RIGHT,si,0); }
  if(vy<0){ let dt=(r-y)/vy; if(dt<0) dt=0; if(t0+dt<=h) evPush(t0+dt,i,-1,EV_BOT,si,0); }
  if(vy>0){ let dt=(g.H-r-y)/vy; if(dt<0) dt=0;
    if(t0+dt<=h){
      /* through the opening (entirely inside it, lid open) the particle leaves */
      let kind=EV_TOP;
      if(g.lid&&gasLidOpen(g)){ const xc=x+vx*dt; if(xc-r>gasOpenLeft(g)&&xc+r<gasOpenRight()) kind=EV_ESC; }
      evPush(t0+dt,i,-1,kind,si,0);
    } }
  if(!g.collisions||!G) return;
  /* pairs with every disk in the 3x3 block of cells around i */
  /* the cell i was REGISTERED in at the substep's start: a partner that can
     still be reached started within C of i's start, i.e. in an adjacent cell */
  const ci=g._cellOf[i], cx=ci%G.nx, cy=(ci-cx)/G.nx;
  for(let yy=cy-1;yy<=cy+1;yy++){ if(yy<0||yy>=G.ny) continue;
    for(let xx=cx-1;xx<=cx+1;xx++){ if(xx<0||xx>=G.nx) continue;
      for(let j=g._cellHead[yy*G.nx+xx];j>=0;j=g._cellNext[j]){
        if((half?j<=i:j===i)||g.out[j]) continue;
        const ax=g.x[j]+g.vx[j]*(t0-g.lt[j]), ay=g.y[j]+g.vy[j]*(t0-g.lt[j]);
        const dt=pairTime(x-ax,y-ay,vx-g.vx[j],vy-g.vy[j],r+gasRad(g,j));
        if(t0+dt<=h) evPush(t0+dt,i,j,EV_PAIR,si,g.st[j]);
      } } }
}
function gasSubstep(g,h,wantLeft){
  const N=g.n, L0=g.left;
  g.stats.substeps++;
  /* 1. the heater: PhET scales every speed by 1 + a/800 once per 60-fps frame;
        here the same factor is applied as a rate, (1 + a/800)^(h/DT_FRAME) */
  if(g.heat!==0&&g.hold!=='temperature'&&g.hold!=='pressureT'){
    const s=Math.pow(1+g.heat/GAS.HEAT_COOL,h/GAS.DT_FRAME);
    let e0=0,e1=0,vr=0;
    for(let i=0;i<N;i++) if(!g.out[i]){
      const m=gasMass(g,i); e0+=0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]);
      vr+=m*(g.x[i]*g.vx[i]+g.y[i]*g.vy[i]);
      g.vx[i]*=s; g.vy[i]*=s; e1+=0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]); }
    g.led.heatQ+=e1-e0; if(g.vir.on) g.vir.heat+=(s-1)*vr;
  }
  /* 2. the left wall moves linearly across the substep */
  const u=(wantLeft===undefined?0:(wantLeft-L0)/h);
  /* 3. the grid: any pair that can touch within h starts in adjacent cells.
        v_b bounds every speed during the substep (a binary collision cannot
        leave a disk more than twice the largest kinetic energy) */
  let keMax=0, smax=0, mmin=Infinity, nin=0;
  for(let i=0;i<N;i++){ if(g.out[i]) continue; nin++; const e=gasKE(g,i); if(e>keMax) keMax=e; }
  for(const S of g.species){ if(2*S.r>smax) smax=2*S.r; if(S.m<mmin) mmin=S.m; }
  const vb=Math.sqrt(4*keMax/mmin)+Math.abs(u);
  let G=null;
  if(g.collisions&&nin>1){
    const C=Math.max(smax+2*vb*h,1), x0=Math.min(L0,wantLeft===undefined?L0:wantLeft)-smax, y0=-smax;
    const nx=Math.max(1,Math.ceil((smax-x0)/C)+1), ny=Math.max(1,Math.ceil((g.H+2*smax)/C)+1);
    const nc=nx*ny;
    if(!g._cellHead||g._cellHead.length<nc) g._cellHead=new Int32Array(Math.max(nc,64));
    g._cellHead.fill(-1,0,nc);
    for(let i=0;i<N;i++){ if(g.out[i]) continue;
      const cx=Math.min(nx-1,Math.max(0,Math.floor((g.x[i]-x0)/C))), cy=Math.min(ny-1,Math.max(0,Math.floor((g.y[i]-y0)/C)));
      const c=cy*nx+cx; g._cellNext[i]=g._cellHead[c]; g._cellHead[c]=i; g._cellOf[i]=c; }
    G={C,x0,y0,nx,ny,vb};
  }
  if(g.vir.on){ let e2=0; for(let i=0;i<N;i++) if(!g.out[i]) e2+=2*gasKE(g,i); g.vir.kin+=e2*h; }
  /* 4. predict every particle's first events; pairs once each (j > i) */
  EVH.n=0;
  for(let i=0;i<N;i++){ g.lt[i]=0; }
  for(let i=0;i<N;i++){ if(g.out[i]) continue; gasPredict(g,i,0,h,L0,u,G,true); }
  /* 5. events in time order */
  const cap=64*nin+1000; let nev=0;
  while(EVH.n>0){
    const e=evPop(), t=EVH.t[e];
    if(t>h) break;
    const i=EVH.i[e], j=EVH.j[e], kind=EVH.k[e];
    /* stale: a disk has had an event since this one was predicted (its stamp
       moved on), or has left through the lid */
    if(g.st[i]!==EVH.si[e]||g.out[i]){ g.stats.stale++; continue; }
    if(kind===EV_PAIR&&(g.st[j]!==EVH.sj[e]||g.out[j])){ g.stats.stale++; continue; }
    if(++nev>cap){ g.stats.eventCap++; break; }
    /* advance the particle(s) to the event time */
    g.x[i]+=g.vx[i]*(t-g.lt[i]); g.y[i]+=g.vy[i]*(t-g.lt[i]); g.lt[i]=t;
    const m=gasMass(g,i);
    if(kind===EV_PAIR){
      g.x[j]+=g.vx[j]*(t-g.lt[j]); g.y[j]+=g.vy[j]*(t-g.lt[j]); g.lt[j]=t;
      const vir=pairResolve(g,i,j);
      if(g.vir.on) g.vir.pair+=vir;
      g.stats.pairHits++; g.st[i]++; g.st[j]++;
      if(G&&(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]>G.vb*G.vb||g.vx[j]*g.vx[j]+g.vy[j]*g.vy[j]>G.vb*G.vb)) g.stats.fastMiss++;
      gasPredict(g,i,t,h,L0,u,G); gasPredict(g,j,t,h,L0,u,G);
      continue;
    }
    if(kind===EV_ESC){
      /* leaves through the opening: out of the container, no more collisions */
      const e0=0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]);
      if(g.vir.on){ g.vir.esc-=m*(g.x[i]*g.vx[i]+g.y[i]*g.vy[i]); g.vir.kin-=2*e0*(h-t); }
      g.led.esc+=e0; g.out[i]=1; g.st[i]++;
      continue;
    }
    let Jx=0,Jy=0;
    const eHit=0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]);
    if(kind===EV_LEFT){
      const moving=gasXlo(g,g.sp[i])===null, uu=moving?u:0;
      const vx0=g.vx[i], vx1=2*uu-vx0;               /* elastic: the wall is infinitely heavy */
      g.vx[i]=vx1; Jx=m*(vx1-vx0);
      if(uu!==0){ const dE=0.5*m*(vx1*vx1-vx0*vx0); g.led.work+=dE; if(g.vir.on) g.vir.kin+=2*dE*(h-t); }
      if(moving){ g.imp.L+=Jx; g.imp.hitsL++; g.imp.E+=eHit; g.stats.wallHits++; g.stats.frameWallHits++; }
    } else if(kind===EV_RIGHT){
      Jx=-2*m*g.vx[i]; g.vx[i]=-g.vx[i];
      if(gasXhi(g,g.sp[i])===0){ g.imp.R-=Jx; g.imp.hitsR++; g.imp.E+=eHit; g.stats.wallHits++; g.stats.frameWallHits++; }
    } else if(kind===EV_BOT){
      Jy=-2*m*g.vy[i]; g.vy[i]=-g.vy[i]; g.imp.B+=Jy; g.imp.hitsB++; g.imp.E+=eHit; g.stats.wallHits++; g.stats.frameWallHits++;
    } else {
      Jy=-2*m*g.vy[i]; g.vy[i]=-g.vy[i]; g.imp.T-=Jy; g.imp.hitsT++; g.imp.E+=eHit; g.stats.wallHits++; g.stats.frameWallHits++;
    }
    if(g.vir.on) g.vir.wall+=g.x[i]*Jx+g.y[i]*Jy;
    g.st[i]++;
    gasPredict(g,i,t,h,L0,u,G);
  }
  g.stats.events+=nev;
  /* 6. everyone to the end of the substep; the kinetic virial of the substep */
  for(let i=0;i<N;i++){
    const dt=h-g.lt[i];
    g.x[i]+=g.vx[i]*dt; g.y[i]+=g.vy[i]*dt; g.lt[i]=0;
  }
  if(wantLeft!==undefined) gasWidthTo(g,-wantLeft);
  g.u=u;
  g.imp.t+=h;
  EVH.n=0;
}
/* ---- one frame: substeps, then PhET's per-step bookkeeping ------------------- */
/* the number of substeps keeps the grid's cells at most ~2 diameters: a cell
   is s_max + 2 v_b h wide, and the event order inside a substep is exact
   whatever h is, so this is a speed knob, not an accuracy one */
function gasSubsteps(g,dt){
  let keMax=0, smax=0, mmin=Infinity;
  for(let i=0;i<g.n;i++) if(!g.out[i]){ const e=gasKE(g,i); if(e>keMax) keMax=e; }
  for(const S of g.species){ if(2*S.r>smax) smax=2*S.r; if(S.m<mmin) mmin=S.m; }
  if(!(keMax>0)||!(smax>0)) return 1;
  const vb=Math.sqrt(4*keMax/mmin)+(g.doesWork?g.wallSpeed:0);
  return Math.max(1,Math.min(64,Math.ceil(2*vb*dt/smax)));
}
function gasStep(g,dt){
  if(!(dt>0)) return;
  for(let i=0;i<g.n;i++) g.px[i]=g.x[i];
  const n=gasSubsteps(g,dt), h=dt/n;
  g.stats.frameWallHits=0;
  let moved=false;
  for(let s=0;s<n;s++){
    let wantLeft;
    if(g.doesWork&&g.wantW!==g.W){
      /* Explore: the wall heads for the width the user asked for at no more
         than PhET's wallSpeedLimit, in either direction */
      const d=g.wantW-g.W, lim=g.wallSpeed*h;
      wantLeft=-(Math.abs(d)<=lim?g.wantW:g.W+(d>0?lim:-lim));
      moved=true;
    }
    gasSubstep(g,h,wantLeft);
  }
  if(!moved) g.u=0;
  g.t+=dt;
  /* escaped particles float off; they are dropped far outside the box */
  for(let i=g.n-1;i>=0;i--) if(g.out[i]&&(g.y[i]>g.H+30000||g.y[i]<-30000||g.x[i]>30000||g.x[i]<g.left-30000)) gasKill(g,i);
  if(g.counter.on){ g.counter.count+=g.stats.frameWallHits; g.counter.t+=dt;
    if(g.counter.t>=g.counter.period){ g.counter.on=false; g.counter.t=g.counter.period; } }
  if(g.watch.on){ g.watch.t=Math.min(GAS.MAXTIME,g.watch.t+dt); if(g.watch.t>=GAS.MAXTIME) g.watch.on=false; }
  gasUpdate(g,dt,g.stats.frameWallHits);
  if(g.sampler) gasSample(g,dt,true);
  if(g.flow&&!g.divided) gasFlowStep(g,dt);
}
/* PhET's updateModel: compensateForHoldConstant, the temperature, the pressure
   (enabled after the first wall hit; the gauge refreshes every 0.75 ps with
   noise), the lid blowing off, the maximum temperature */
function gasUpdate(g,dt,hits){
  const N=gasCount(g);
  if(g.hold==='pressureV'&&N>0&&g.P>0){
    const T=gasTemp(g), Pm=g.P/GAS.P_SCALE;
    let w=+(N*GAS.K*T/Pm/(g.H*g.D)).toFixed(5);
    if(w<g.wRange[0]||w>g.wRange[1]){
      g.oops=w>g.wRange[1]?'pressureLarge':'pressureSmall'; g.hold='nothing';
      w=Math.min(g.wRange[1],Math.max(g.wRange[0],w));
    }
    gasResize(g,w,true);
  } else if(g.hold==='pressureT'&&N>0&&g.P>0){
    gasSetTemp(g,(g.P/GAS.P_SCALE)*gasVolume(g)/(N*GAS.K));
  }
  g.T=gasTemp(g);
  if(N===0){ g.pOn=false; g.P=0; g.gaugeP=0; }
  else if(!g.pOn&&hits>0) g.pOn=true;
  if(g.pOn){
    g.P=gasPressureOf(N,g.T,gasVolume(g));
    g.pAcc+=dt;
    if(g.pAcc>=GAS.P_REFRESH){
      let e=0;
      if(g.noiseOn&&g.hold!=='pressureV'&&g.hold!=='pressureT'){
        const pn=Math.min(50,Math.max(0,50*(1-g.P/GAS.P_MAX))), sn=Math.min(1,Math.max(0,((g.T||0)-5)/45));
        e=pn*sn*g.noise.next();
        if(e<g.P) e*=g.noise.next()<0.5?-1:1;
      }
      g.gaugeP=g.P+e; g.pAcc=0;
    }
    if(g.P>GAS.P_MAX) gasBlowLid(g);
  }
  if(g.T!==null&&g.T>=GAS.T_MAX){
    if(g.hold!=='nothing'&&g.hold!=='volume') g.hold='nothing';
    gasRemoveAll(g); gasReturnLid(g); g.oops='maxTemperature'; g.T=null;
  }
  if(g.hold==='temperature'&&gasLidOpen(g)){ g.hold='nothing'; g.oops='temperatureOpen'; }
}
/* the model refreshed without time passing (a paused resize, a count change):
   PhET's updateWhenPaused, which also refreshes the gauge */
function gasRefresh(g){ g.pAcc=GAS.P_REFRESH; gasUpdate(g,0,0); }
/* the hold-constant modes a user may choose right now (PhET HoldConstantPanel):
   T needs particles and a closed lid; P needs a non-zero pressure */
function gasHoldAllowed(g,mode){
  if(mode==='temperature') return gasCount(g)>0&&!gasLidOpen(g);
  if(mode==='pressureV'||mode==='pressureT') return g.P>0;
  return true;
}
function gasSetHold(g,mode){ if(!gasHoldAllowed(g,mode)) return false; g.hold=mode; return true; }
/* the Oops texts (PhET's strings, <br> dropped) */
const GAS_OOPS={
  maxTemperature:'Oops! Maximum temperature reached.',
  pressureEmpty:'Oops! Pressure cannot be held constant when the container is empty.',
  pressureLarge:'Oops! Pressure cannot be held constant. Volume would be too large.',
  pressureSmall:'Oops! Pressure cannot be held constant. Volume would be too small.',
  temperatureEmpty:'Oops! Temperature cannot be held constant when the container is empty.',
  temperatureOpen:'Oops! Temperature cannot be held constant when the container is open.'
};

/* ---- statistics --------------------------------------------------------------- */
function gasSpeed(g,i){ return Math.sqrt(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]); }
/* counts in nb bins of width w (PhET HistogramsModel: floor(v/w); values past
   the last bin are not counted) */
function gasBinCounts(g,k,w,nb,energy){
  const out=new Array(nb).fill(0);
  for(let i=0;i<g.n;i++){ if(g.out[i]||g.sp[i]!==k) continue;
    const v=energy?gasKE(g,i):gasSpeed(g,i), b=Math.floor(v/w);
    if(b>=0&&b<nb) out[b]++; }
  return out;
}
function gasMeanSpeedOf(g,k){ let s=0,c=0; for(let i=0;i<g.n;i++) if(!g.out[i]&&g.sp[i]===k){ s+=gasSpeed(g,i); c++; } return c?s/c:null; }
/* PhET's Energy-screen sampler: every frame adds the bin counts and the mean
   speeds; every 1 ps (or at once when paused) the averages are published */
function gasSamplerOn(g){
  const z=()=>new Array(GAS.NBIN).fill(0);
  g.sampler={dt:0, n:0, acc:{s0:z(),s1:z(),e0:z(),e1:z()}, spd:[0,0],
             out:{s0:z(),s1:z(),e0:z(),e1:z()}, mean:[null,null], published:0};
  return g.sampler;
}
function gasSample(g,dt,playing){
  const S=g.sampler; if(!S) return;
  S.dt+=dt; S.n++;
  for(const k of [0,1]){
    const sc=gasBinCounts(g,k,GAS.SBIN,GAS.NBIN,false), ec=gasBinCounts(g,k,GAS.EBIN,GAS.NBIN,true);
    const A=S.acc['s'+k], B=S.acc['e'+k];
    for(let b=0;b<GAS.NBIN;b++){ A[b]+=sc[b]; B[b]+=ec[b]; }
    const ms=gasMeanSpeedOf(g,k); S.spd[k]+=ms===null?0:ms;
  }
  if(S.dt>=GAS.SAMPLE-1e-9||!playing){
    for(const key of ['s0','s1','e0','e1']) S.out[key]=S.acc[key].map(v=>v/S.n);
    for(const k of [0,1]) S.mean[k]=gasCount(g,k)?S.spd[k]/S.n:null;
    for(const key of ['s0','s1','e0','e1']) S.acc[key].fill(0);
    S.spd=[0,0]; S.n=0; S.dt=0; S.published++;
  }
}
/* the centre of mass of species k: x offset from the container's centre, pm */
function gasCOM(g,k){
  let sm=0,sx=0;
  for(let i=0;i<g.n;i++) if(!g.out[i]&&g.sp[i]===k){ const m=gasMass(g,i); sm+=m; sx+=m*g.x[i]; }
  return sm>0?sx/sm-(g.left+g.W/2):null;
}
/* Diffusion's Data: per side of the divider line, the counts of each species
   and the average temperature (2/3)<KE>/k */
function gasSideData(g){
  const res=[{n0:0,n1:0,e:0,T:null},{n0:0,n1:0,e:0,T:null}];
  for(let i=0;i<g.n;i++){ if(g.out[i]) continue;
    const s=g.x[i]<g.dividerX?0:1; if(g.sp[i]===0) res[s].n0++; else res[s].n1++; res[s].e+=gasKE(g,i); }
  for(const r of res){ const n=r.n0+r.n1; r.T=n?(2/3)*r.e/n/GAS.K:null; }
  return res;
}
/* Diffusion's particle flow: crossings of the divider line this frame (from x
   at the frame's start to x at its end), a running window of 300 frames */
function gasFlowOn(g){ g.flow={L:[[],[]], R:[[],[]], dts:[], rateL:[0,0], rateR:[0,0]}; return g.flow; }
function gasFlowStep(g,dt){
  const F=g.flow, cL=[0,0], cR=[0,0];
  for(let i=0;i<g.n;i++){ if(g.out[i]) continue; const k=g.sp[i];
    if(g.px[i]>=g.dividerX&&g.x[i]<g.dividerX) cL[k]++; else if(g.px[i]<=g.dividerX&&g.x[i]>g.dividerX) cR[k]++; }
  F.dts.push(dt); for(const k of [0,1]){ F.L[k].push(cL[k]); F.R[k].push(cR[k]); }
  if(F.dts.length>GAS.FLOW_WINDOW){ F.dts.shift(); for(const k of [0,1]){ F.L[k].shift(); F.R[k].shift(); } }
  const T=F.dts.reduce((a,b)=>a+b,0);
  for(const k of [0,1]){ F.rateL[k]=F.L[k].reduce((a,b)=>a+b,0)/T; F.rateR[k]=F.R[k].reduce((a,b)=>a+b,0)/T; }
}
/* the pressure the walls feel: momentum delivered per unit time to each wall
   (a 2-D force per unit length is this over the wall's length) */
function gasWallForce(g){
  const I=g.imp, t=I.t||1;
  return {L:I.L/t, R:I.R/t, B:I.B/t, T:I.T/t, t:I.t, hits:I.hitsL+I.hitsR+I.hitsB+I.hitsT};
}

/* ---- Diffusion's settings (PhET DiffusionParticleSystem) --------------------- */
/* the half a species is born in: particle 1 left of the divider, particle 2 right */
function gasDiffRegion(g,k){ const mid=g.left+g.W/2; return k===0?[g.left,mid-g.dividerHalf]:[mid+g.dividerHalf,0]; }
/* a new mass or starting temperature sets EVERY particle of the species to
   sqrt(3kT/m), keeping its direction (PhET setMassAndTemperature) */
function gasDiffMassTemp(g,k,m,T){
  g.species[k].m=m;
  const v=Math.sqrt(3*GAS.K*T/m);
  for(let i=0;i<g.n;i++) if(g.sp[i]===k&&!g.out[i]){
    const s=gasSpeed(g,i); if(s>0){ g.vx[i]*=v/s; g.vy[i]*=v/s; } else { g.vx[i]=v; g.vy[i]=0; } }
}
/* a new radius; paused, every particle of the species is set back inside the
   x-range it may occupy (PhET clamps into the left half for particle 1 even
   with the divider out; here the range is the one the divider allows) */
function gasDiffRadius(g,k,r,playing){
  g.species[k].r=r;
  if(playing) return;
  const lo=gasXlo(g,k), xlo=lo===null?g.left:lo, xhi=gasXhi(g,k);
  for(let i=0;i<g.n;i++) if(g.sp[i]===k&&!g.out[i]){
    if(g.x[i]-r<xlo) g.x[i]=xlo+r; else if(g.x[i]+r>xhi) g.x[i]=xhi-r;
    if(g.y[i]-r<0) g.y[i]=r; else if(g.y[i]+r>g.H) g.y[i]=g.H-r; }
}
/* a new count: added in the species' own half; removing resets the rest to
   sqrt(3kT/m), as PhET does */
function gasDiffCount(g,k,n,T){
  const c=gasCount(g,k);
  if(n>c){ const R=gasDiffRegion(g,k); gasScatter(g,k,n-c,T,R[0],R[1]); }
  else if(n<c){ gasRemove(g,k,c-n); gasDiffMassTemp(g,k,g.species[k].m,T); }
}
/* the divider back in: PhET restarts, every particle regenerated on its side */
function gasDiffRestart(g,n0,T0,n1,T1){
  gasRemoveAll(g); gasSetDivided(g,true);
  const R0=gasDiffRegion(g,0), R1=gasDiffRegion(g,1);
  gasScatter(g,0,n0,T0,R0[0],R0[1]); gasScatter(g,1,n1,T1,R1[0],R1[1]);
  if(g.flow) gasFlowOn(g);
}
