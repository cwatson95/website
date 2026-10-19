
/* ================================================================== *
 *  the engine: one PRNG, the binomial, the qubit algebra, and PhET's  *
 *  four experiments (coins, photons, Stern-Gerlach, Bloch sphere).    *
 *  Shared by quantum-measurement.html and quantum-coin-toss.html.     *
 * ================================================================== */
const DEG=Math.PI/180;          /* multiply degrees by DEG to get radians (90*DEG = pi/2, asserted) */

/* ---- the PRNG: mulberry32.  Every random draw in the file comes from one of
   these, and build/quantum-measurement/derive.py mirrors it with explicit
   32-bit arithmetic, so a seeded count is pinned exactly, not statistically.
   The state is plain data ({s}) so a scene can be saved, copied and reset. */
function rngMake(seed){ return {s:seed|0}; }
function rngNext(R){
  R.s=(R.s+0x6D2B79F5)|0;
  let t=Math.imul(R.s^(R.s>>>15),1|R.s);
  t=(t+Math.imul(t^(t>>>7),61|t))^t;
  return ((t^(t>>>14))>>>0)/4294967296;
}

/* ---- the binomial.  ln n! from a 0..30 table of summed logs, Stirling with
   four correction terms above (truncation < 1/(1188 n^9) < 1e-16 there);
   derive.py checks it against math.lgamma and the pmf against scipy. */
const LNF=(function(){ const t=[0]; let s=0; for(let i=1;i<=30;i++){ s+=Math.log(i); t.push(s); } return t; })();
function lnFactStirling(x){
  return x*Math.log(x)-x+0.5*Math.log(2*Math.PI*x)+1/(12*x)-1/(360*x*x*x)+1/(1260*Math.pow(x,5))-1/(1680*Math.pow(x,7));
}
function lnFact(n){ return n<=30?LNF[n]:lnFactStirling(n); }
function binomPmf(N,k,p){
  if(k<0||k>N) return 0;
  if(p<=0) return k===0?1:0;
  if(p>=1) return k===N?1:0;
  return Math.exp(lnFact(N)-lnFact(k)-lnFact(N-k)+k*Math.log(p)+(N-k)*Math.log1p(-p));
}
function binomSD(N,p){ return Math.sqrt(N*p*(1-p)); }
/* chi-square of observed counts against M x pmf: merge k = 0..N left to right
   until a bin expects at least 5; a short tail joins the last bin (derive.py
   does exactly this, in this order) */
function chi2Binned(obs,N,p,M){
  const bins=[]; let co=0, ce=0;
  for(let k=0;k<=N;k++){ co+=obs[k]||0; ce+=M*binomPmf(N,k,p); if(ce>=5){ bins.push([co,ce]); co=0; ce=0; } }
  if((ce>0||co>0)&&bins.length){ bins[bins.length-1][0]+=co; bins[bins.length-1][1]+=ce; }
  let chi=0; for(const [o,e] of bins) chi+=(o-e)*(o-e)/e;
  return {chi,dof:bins.length-1,bins};
}
/* one set of N coins: k = number of u < p (heads, up), exactly as a coin set draws */
function coinCount(R,N,p){ let k=0; for(let i=0;i<N;i++) if(rngNext(R)<p) k++; return k; }
/* M sets of N coins from one seed: the histogram, the sample mean and the
   unbiased sample variance, and the binned chi-square */
function repeatsRun(seed,N,p,M){
  const R=rngMake(seed), obs=new Float64Array(N+1), ks=new Int32Array(M);
  let sum=0;
  for(let j=0;j<M;j++){ const k=coinCount(R,N,p); ks[j]=k; obs[k]++; sum+=k; }
  const mean=sum/M; let ss=0; for(let j=0;j<M;j++) ss+=(ks[j]-mean)*(ks[j]-mean);
  const c=chi2Binned(obs,N,p,M);
  return {N,p,M,seed,obs,ks,mean,v:M>1?ss/(M-1):0,chi:c.chi,dof:c.dof};
}

/* ---- the qubit: 2x2 complex matrices and kets as flat real arrays
   (taken from bloch_sphere.html, which checks the arithmetic by hand first)
   A 2x2 is [a.re,a.im, b.re,b.im, c.re,c.im, d.re,d.im] for [[a,b],[c,d]];
   a ket is [a.re,a.im, b.re,b.im]. */
const M_I=[1,0, 0,0, 0,0, 1,0], M_SX=[0,0, 1,0, 1,0, 0,0], M_SY=[0,0, 0,-1, 0,1, 0,0], M_SZ=[1,0, 0,0, 0,0, -1,0];
const PAULI=[M_SX,M_SY,M_SZ];
function mAdd(A,B){ const o=new Array(8); for(let i=0;i<8;i++) o[i]=A[i]+B[i]; return o; }
function mScale(A,s){ const o=new Array(8); for(let i=0;i<8;i++) o[i]=A[i]*s; return o; }
function mScaleC(A,x,y){ const o=new Array(8); for(let i=0;i<8;i+=2){ o[i]=A[i]*x-A[i+1]*y; o[i+1]=A[i]*y+A[i+1]*x; } return o; }
function mMul(A,B){
  const o=new Array(8);
  for(let r=0;r<2;r++) for(let c=0;c<2;c++){
    let re=0,im=0;
    for(let k=0;k<2;k++){ const ar=A[4*r+2*k], ai=A[4*r+2*k+1], br=B[4*k+2*c], bi=B[4*k+2*c+1]; re+=ar*br-ai*bi; im+=ar*bi+ai*br; }
    o[4*r+2*c]=re; o[4*r+2*c+1]=im;
  }
  return o;
}
function mDag(A){ return [A[0],-A[1],A[4],-A[5],A[2],-A[3],A[6],-A[7]]; }
function mMaxAbsDiff(A,B){ let m=0; for(let i=0;i<A.length;i++) m=Math.max(m,Math.abs(A[i]-B[i])); return m; }
/* |psi> = cos(th/2)|0> + e^{i ph} sin(th/2)|1>: the HALF angle is why
   orthogonal states are antipodal on the sphere */
function ketOf(th,ph){ const c=Math.cos(th/2), s=Math.sin(th/2); return [c,0,s*Math.cos(ph),s*Math.sin(ph)]; }
function ketNorm(k){ return Math.sqrt(k[0]*k[0]+k[1]*k[1]+k[2]*k[2]+k[3]*k[3]); }
function braket(a,b){ return [a[0]*b[0]+a[1]*b[1]+a[2]*b[2]+a[3]*b[3], a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2]]; }
function mApply(A,k){
  const o=new Array(4);
  for(let r=0;r<2;r++){ let re=0,im=0;
    for(let c=0;c<2;c++){ const ar=A[4*r+2*c], ai=A[4*r+2*c+1], kr=k[2*c], ki=k[2*c+1]; re+=ar*kr-ai*ki; im+=ar*ki+ai*kr; }
    o[2*r]=re; o[2*r+1]=im; }
  return o;
}
/* r_i = <psi|sigma_i|psi> */
function blochOfKet(k){ const o=[0,0,0]; for(let i=0;i<3;i++) o[i]=braket(k,mApply(PAULI[i],k))[0]; return o; }
function blochOfAngles(th,ph){ return [Math.sin(th)*Math.cos(ph),Math.sin(th)*Math.sin(ph),Math.cos(th)]; }
function anglesOfBloch(r){
  const n=Math.hypot(r[0],r[1],r[2]);
  let ph=Math.atan2(r[1],r[0]); if(ph<0) ph+=2*Math.PI;
  return {th:Math.acos(clamp(n>0?r[2]/n:1,-1,1)),ph,len:n};
}
function dot3v(a,b){ return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]; }
/* THE BORN RULE: P(up along n) = Tr(rho P_n) = (1 + r.n)/2 = cos^2(Theta/2) */
function bornP(r,n){ return 0.5*(1+dot3v(r,n)); }
/* the one measurement primitive every spin view calls: one draw, u < P(up)
   is up, and the state collapses onto +n or -n (PhET's rule, both screens) */
function measureAlong(R,r,n){
  const up=rngNext(R)<bornP(r,n);
  return {up, r:up?[n[0],n[1],n[2]]:[-n[0],-n[1],-n[2]]};
}
/* U(n,a) = exp(-i a n.sigma/2) turns the Bloch vector by a about n */
function unitary(n,a){
  let m=mScale(M_I,Math.cos(a/2)); const s=-Math.sin(a/2);
  for(let i=0;i<3;i++) m=mAdd(m,mScaleC(PAULI[i],0,s*n[i]));
  return m;
}
/* Rodrigues: r turned by a about the unit axis n */
function rotate3(r,n,a){
  const c=Math.cos(a), s=Math.sin(a), d=dot3v(n,r);
  const cr=[n[1]*r[2]-n[2]*r[1], n[2]*r[0]-n[0]*r[2], n[0]*r[1]-n[1]*r[0]];
  return [r[0]*c+cr[0]*s+n[0]*d*(1-c), r[1]*c+cr[1]*s+n[1]*d*(1-c), r[2]*c+cr[2]*s+n[2]*d*(1-c)];
}
/* the three measurement bases: |up_n>, |down_n> (standard kets; |up_y> =
   (|0> + i|1>)/sqrt2 is the state at azimuth pi/2, the sphere's +Y) */
const BASIS={Z:{up:[1,0,0,0],dn:[0,0,1,0],n:[0,0,1]},
             X:{up:[Math.SQRT1_2,0,Math.SQRT1_2,0],dn:[Math.SQRT1_2,0,-Math.SQRT1_2,0],n:[1,0,0]},
             Y:{up:[Math.SQRT1_2,0,0,Math.SQRT1_2],dn:[Math.SQRT1_2,0,0,-Math.SQRT1_2],n:[0,1,0]}};
function wrap2(x){ x=x%2; return x<0?x+2:x; }
/* the state written in basis b: |psi> = e^{i g pi}(a|up> + c e^{i chi pi}|down>),
   a, c >= 0; chi and g in units of pi, in [0, 2) */
function ketInBasis(k,b){
  const B=BASIS[b], au=braket(B.up,k), ad=braket(B.dn,k);
  const a=Math.hypot(au[0],au[1]), c=Math.hypot(ad[0],ad[1]);
  const gu=Math.atan2(au[1],au[0])/Math.PI, gd=Math.atan2(ad[1],ad[0])/Math.PI;
  const g=a>1e-12?gu:gd;
  const chi=(a>1e-12&&c>1e-12)?wrap2(gd-gu):0;
  return {a,c,chi,g:wrap2(g)};
}
/* ... and the equation rebuilt into a ket, for the round trip */
function ketFromBasis(E,b){
  const B=BASIS[b], cg=Math.cos(Math.PI*E.g), sg=Math.sin(Math.PI*E.g);
  const cx=Math.cos(Math.PI*(E.g+E.chi)), sx=Math.sin(Math.PI*(E.g+E.chi));
  const o=[0,0,0,0];
  for(let i=0;i<2;i++){
    const ur=B.up[2*i], ui=B.up[2*i+1], dr=B.dn[2*i], di=B.dn[2*i+1];
    o[2*i]=E.a*(ur*cg-ui*sg)+E.c*(dr*cx-di*sx);
    o[2*i+1]=E.a*(ur*sg+ui*cg)+E.c*(dr*sx+di*cx);
  }
  return o;
}

/* ================================================================== *
 *  THE COINS (PhET's Coins screen)                                    *
 * ================================================================== */
const FLIP_T=1.0;               /* s: a flip or a repreparation takes 1 s (PhET's value) */
const COIN_NS=[10,100,10000];   /* identical coins (PhET's value) */
const BIAS_STEP=0.05;           /* the bias sliders snap to 0.05 (PhET's value) */
const HIST_KEEP=48;             /* the single coin's strip of recent outcomes (house) */
/* k/20 is correctly rounded where k x 0.05 is not (7 x 0.05 = 0.35000000000000003) */
function snapBias(p){ const n=Math.round(1/BIAS_STEP); return clamp(Math.round(p*n)/n,0,1); }
/* states: 'preparing' (flipping / being reprepared), 'ready' (a quantum coin
   nobody has looked at: no face exists yet), 'hidden' (a face exists, under the
   cup), 'revealed' */
function makeCoin(n){ return {n, state:'revealed', t:0, then:null, vals:new Uint8Array(10000), kUp:0, hist:[], nObs:0, nUp:0}; }
function makeCoinScene(type,seed){
  const q=type==='quantum';
  const sc={type, quantum:q, p:0.5, init:q?'up':'heads', preparing:true, startsHidden:false,
            single:makeCoin(1), set:makeCoin(100), R:rngMake(seed), seed};
  return sc;
}
/* the quantum coin's state follows its bias (PhET): 1 is up, 0 down, else a superposition */
function quantumInit(p){ return p>=1?'up':(p<=0?'down':'superposition'); }
function coinFace1(sc){ return (sc.init==='heads'||sc.init==='up'||sc.init==='superposition')?1:0; }
/* the draw: u < p is heads / up, exactly as PhET's seeded sets decide */
function coinDraw(sc,c){
  let k=0; for(let i=0;i<c.n;i++){ const v=rngNext(sc.R)<sc.p?1:0; c.vals[i]=v; k+=v; }
  c.kUp=k;
}
function coinPrepare(sc,c,reveal){ c.state='preparing'; c.t=0; c.then=reveal?'reveal':null; }
/* the end of a flip: a classical coin now HAS a face (under the cup); a quantum
   coin is ready, with no face until it is observed */
function coinPrepareNow(sc,c){ if(sc.quantum) c.state='ready'; else { coinDraw(sc,c); c.state='hidden'; } }
function coinReveal(sc,c){
  if(c.state==='preparing') return false;
  if(c.state==='ready') coinDraw(sc,c);         /* the collapse: the face is drawn now */
  const was=c.state; c.state='revealed';
  if(was!=='revealed'){ c.nObs+=c.n; c.nUp+=c.kUp;
    if(c.n===1){ c.hist.push(c.vals[0]); if(c.hist.length>HIST_KEEP) c.hist.shift(); } }
  return true;
}
function coinHide(sc,c){ if(c.state==='revealed'){ c.state='hidden'; return true; } return false; }
/* PhET's reveal/hide (observe/hide) button */
function coinToggle(sc,c){ if(c.state==='revealed') return coinHide(sc,c); return coinReveal(sc,c); }
function coinStep(sc,c,dt){
  if(c.state!=='preparing') return false;
  c.t+=dt;
  if(c.t>=FLIP_T){ c.t=FLIP_T; coinPrepareNow(sc,c); if(c.then==='reveal') coinReveal(sc,c); c.then=null; }
  return true;
}
/* the arrow: the prepared coins go to be measured.  Classical coins arrive
   showing the prepared face (hidden if the preference says so); quantum coins
   arrive ready, faceless (PhET's setMeasurementValuesImmediate) */
function sceneStart(sc){
  sc.preparing=false;
  for(const c of [sc.single,sc.set]){
    const v=coinFace1(sc);
    for(let i=0;i<c.n;i++) c.vals[i]=v;
    c.kUp=v*c.n; c.t=0; c.then=null; c.hist=[]; c.nObs=0; c.nUp=0;
    c.state=sc.quantum?'ready':(sc.startsHidden?'hidden':'revealed');
  }
}
function sceneNewCoin(sc){ sc.preparing=true; for(const c of [sc.single,sc.set]){ c.state='revealed'; c.t=0; c.then=null; } }
function setCoinCount(sc,N){ if(sc.preparing&&COIN_NS.indexOf(N)>=0) sc.set.n=N; }
function sceneAnimating(sc){ return !sc.preparing&&(sc.single.state==='preparing'||sc.set.state==='preparing'); }

/* ================================================================== *
 *  THE PHOTONS (PhET's Photons screen)                                *
 * ================================================================== */
/* PhET's values: model units (PhET's metres), seconds */
const PH={X0:-0.15, V:0.3, BEAM_W:0.04, PBS:0.035, MX:0.11, DV:0.2, DH:-0.09, AP:0.07, ABS:0.05,
          RATE_MAX:200, SLOW:0.4, CAP:999, AVG_T:1, AVG_S:0.5, STEP_DT:2/60, CUSTOM_STEP:5};
const PRESET_ANG={vertical:90, horizontal:0, fortyFive:45};
/* the beam splitter reflects (to the V detector) with probability sin^2(theta),
   theta measured from horizontal: Malus's law with the analyser at 0 and 90 deg */
function pV(angDeg){ const s=Math.sin(angDeg*DEG); return s*s; }
function expectP(angDeg){ return pV(angDeg)-(1-pV(angDeg)); }   /* V = +1, H = -1: -cos 2 theta */
/* the one decision every photon makes, classical (at the splitter) or quantum
   (at the detectors): one draw, u < sin^2 theta is V */
function photonDecide(R,angDeg){ return rngNext(R)<pV(angDeg)?'V':'H'; }
/* the path: along the beam at height y0 to the splitter's diagonal (x = y0),
   then up to y = 0.2 (V), or on to the mirror x + y = 0.11 and down to
   y = -0.09 (H).  Both arms are 0.2 - y0 long, so every photon arrives
   (0.2 - X0)/v = 1.1667 s after it left x = X0, whatever its height. */
function photonLegs(y0){ return {d1:y0-PH.X0, arm:PH.DV-y0, dArr:PH.DV-PH.X0}; }
function photonPos(ph,d,route){
  const y0=ph.y0, L=photonLegs(y0);
  if(d<=L.d1) return [PH.X0+d,y0];
  const e=d-L.d1;
  if(route==='V') return [y0,y0+e];
  const toMirror=PH.MX-2*y0;
  if(e<=toMirror) return [y0+e,y0];
  return [PH.MX-y0,y0-(e-toMirror)];
}
/* PhET's averaging counter: count events, sample every 0.5 s, and report the
   count over the most recent samples covering at least the averaging period */
function makeAvg(total,sample){ return {total,sample,cur:0,tsl:0,hist:[],value:0}; }
function avgCount(A){ A.cur++; }
function avgStep(A,dt){
  A.tsl+=dt;
  if(A.tsl>=A.sample){
    A.hist.push([A.tsl,A.cur]);
    let e=0,t=0,i=0;
    for(let n=A.hist.length-1;n>=0;n--){ e+=A.hist[n][0]; t+=A.hist[n][1]; i++; if(e>=A.total) break; }
    A.value=e>0?Math.round(t/e*1e12)/1e12:0;
    A.hist.splice(0,A.hist.length-i);
    A.cur=0; A.tsl=0;
  }
}
function avgReset(A){ A.cur=0; A.tsl=0; A.hist=[]; A.value=0; }
function makePhotonScene(mode,seed){
  return {mode, R:rngMake(seed), seed, t:0, photons:[], nV:0, nH:0, acc:0,
          avgV:makeAvg(PH.AVG_T,PH.AVG_S), avgH:makeAvg(PH.AVG_T,PH.AVG_S), lastFrame:null};
}
function photonAngle(st){ return st.phPreset==='custom'?st.phCustom:(st.phPreset==='unpolarized'?null:PRESET_ANG[st.phPreset]); }
/* one photon from the laser (PhET's emitAPhoton): a height across the 0.04
   beam, a start up to one frame's travel ahead, an angle (random for the
   unpolarized source) */
function photonEmit(sc,st,dtFrame){
  const y0=PH.BEAM_W/2*(1-2*rngNext(sc.R));
  const ahead=(dtFrame||0)*rngNext(sc.R)*PH.V;
  const a0=photonAngle(st);
  const ang=a0===null?360*rngNext(sc.R):a0;
  sc.photons.push({t0:sc.t-ahead/PH.V, y0, ang, route:null});
}
function photonClear(sc){ sc.photons=[]; }
function photonCounts(sc){ sc.nV=0; sc.nH=0; avgReset(sc.avgV); avgReset(sc.avgH); }
/* advance the scene by dt: emit (many-photon mode, PhET's fractional
   accumulator), decide at the splitter (classical) or at the detectors
   (quantum), count, and retire photons 0.05 past the detector line */
function photonAdvance(sc,st,dt){
  if(!(dt>0)) return;
  if(sc.mode==='many'){
    const n=st.phRate*dt, nf=Math.floor(n);
    for(let i=0;i<nf;i++) photonEmit(sc,st,dt);
    sc.acc+=n-nf;
    while(sc.acc>=1){ photonEmit(sc,st,dt); sc.acc-=1; }
  }
  sc.t+=dt;
  const keep=[];
  for(const ph of sc.photons){
    const d=PH.V*(sc.t-ph.t0), L=photonLegs(ph.y0);
    if(st.phBehavior==='classical'&&ph.route===null&&d>=L.d1) ph.route=photonDecide(sc.R,ph.ang);
    if(d>=L.dArr&&!ph.counted){
      if(ph.route===null) ph.route=photonDecide(sc.R,ph.ang);      /* quantum: the collapse, at the detector */
      ph.counted=true;
      if(ph.route==='V'){ sc.nV=Math.min(sc.nV+1,PH.CAP); avgCount(sc.avgV); } else { sc.nH=Math.min(sc.nH+1,PH.CAP); avgCount(sc.avgH); }
    }
    if(d<L.dArr+PH.ABS) keep.push(ph);
  }
  sc.photons=keep;
  avgStep(sc.avgV,dt); avgStep(sc.avgH,dt);
}
/* a seeded batch through photonDecide: the V count of n photons */
function photonBatch(seed,angDeg,n){ const R=rngMake(seed); let v=0; for(let i=0;i<n;i++) if(photonDecide(R,angDeg)==='V') v++; return v; }
function photonBatchUnpol(seed,n){ const R=rngMake(seed); let v=0; for(let i=0;i<n;i++){ const a=360*rngNext(R); if(photonDecide(R,a)==='V') v++; } return v; }

/* ================================================================== *
 *  THE SPINS (PhET's Spin screen: Stern-Gerlach)                      *
 * ================================================================== */
const AXV={z:[0,0,1], x:[1,0,0]};
/* PhET's six experiments and its custom layout: magnet 1, then the magnet on
   magnet 1's UP beam, then the one on its DOWN beam (PhET's value) */
const SG_EXPS=[{id:'e1',name:'1 [SGz]',axes:['z']},{id:'e2',name:'2 [SGx]',axes:['x']},
               {id:'e3',name:'3 [SGz, SGx]',axes:['z','x','x']},{id:'e4',name:'4 [SGz, SGz]',axes:['z','z','z']},
               {id:'e5',name:'5 [SGx, SGz]',axes:['x','z','z']},{id:'e6',name:'6 [SGx, SGx]',axes:['x','x','x']},
               {id:'custom',name:'custom',axes:['x','z','z']}];
const SG_RATE=300;              /* particles a second per unit amount: PhET's 5 x amount per 60-Hz frame */
const SG_MAXP=1250, SG_MAXP1=50;/* PhET's caps on particles in flight (continuous, single) */
const SG_AVG_T=3;               /* the magnets' counters average over 3 s in 0.5-s samples (PhET's value) */
const SG_SPEED=1.5;             /* apparatus units per second (the remake's layout) */
/* the custom source state, EXACTLY: theta = 2 arccos|alpha| so that
   P(up_z) = cos^2(theta/2) = |alpha|^2.  (PhET uses theta = pi(1 - |alpha|^2).) */
function customTheta(a2){ return 2*Math.acos(Math.sqrt(clamp(a2,0,1))); }
function phetCustomTheta(a2){ return Math.PI*(1-a2); }
const SG_SOURCES={'+Z':[0,0,1],'+X':[1,0,0],'-Z':[0,0,-1]};
function sgSource(st){ if(st.sgExp==='custom'){ const t=customTheta(st.sgA2); return [Math.sin(t),0,Math.cos(t)]; } return SG_SOURCES[st.sgSrc].slice(); }
function sgAxes(st){
  const e=SG_EXPS.find(x=>x.id===st.sgExp);
  if(e.id==='custom') return [st.sgC1,st.sgC2,st.sgC2];
  return e.axes.slice();
}
/* one particle through the apparatus: PhET's measureParticle at each magnet */
function sgRun(R,r0,axes){
  const m1=measureAlong(R,r0,AXV[axes[0]]);
  if(axes.length===1) return {up1:m1.up, r1:m1.r, up2:null, r2:null};
  const n2=m1.up?AXV[axes[1]]:AXV[axes[2]];
  const m2=measureAlong(R,m1.r,n2);
  return {up1:m1.up, r1:m1.r, up2:m2.up, r2:m2.r};
}
/* products of projections: [P(up,up), P(up,down), P(down,up), P(down,down)] */
function sgProbs(r0,axes){
  const n1=AXV[axes[0]], p1=bornP(r0,n1);
  if(axes.length===1) return [p1,1-p1];
  const pu=bornP(n1,AXV[axes[1]]), pd=bornP([-n1[0],-n1[1],-n1[2]],AXV[axes[2]]);
  return [p1*pu,p1*(1-pu),(1-p1)*pd,(1-p1)*(1-pd)];
}
function sgBatch(seed,r0,axes,n){
  const R=rngMake(seed), c=[0,0,0,0];
  for(let i=0;i<n;i++){ const o=sgRun(R,r0,axes); if(axes.length===1) c[o.up1?0:1]++; else c[(o.up1?0:2)+(o.up2?0:1)]++; }
  return c;
}
/* the apparatus layout (the remake's): source exit at x = 0, magnet 1 from 1
   to 2 (the particle is measured at its middle and bends to an exit), the
   second stage from 3 to 4 at y = +-0.62, the counters at x = 5 */
const SGL={S1:[1,2], S2:[3,4], Y2:0.62, EXIT:0.16, END:5.05};
function sgWaypoints(p){
  const pts=[[0,p.jy]], y=p.jy;
  pts.push([1.5,y]);
  if(p.up1===null) return pts;
  const s1=p.up1?1:-1;
  pts.push([2,s1*SGL.EXIT+y*0.5]);
  if(!p.two){ pts.push([SGL.END,s1*SGL.Y2]); return pts; }
  pts.push([3,s1*SGL.Y2+y*0.5]); pts.push([3.5,s1*SGL.Y2+y*0.5]);
  if(p.up2===null) return pts;
  const s2=p.up2?1:-1;
  pts.push([4,s1*SGL.Y2+s2*SGL.EXIT]); pts.push([SGL.END,s1*SGL.Y2+s2*SGL.EXIT*2.2]);
  return pts;
}
function polyAt(pts,d){
  for(let i=1;i<pts.length;i++){
    const a=pts[i-1], b=pts[i], L=Math.hypot(b[0]-a[0],b[1]-a[1]);
    if(d<=L||i===pts.length-1){ const f=L>0?Math.min(1,Math.max(0,d/L)):0; return [a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f]; }
    d-=L;
  }
  return pts[pts.length-1].slice();
}
function polyLen(pts){ let s=0; for(let i=1;i<pts.length;i++) s+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]); return s; }
function makeSgScene(seed){
  return {R:rngMake(seed), seed, t:0, parts:[], acc:0, last:null,
          c:[{up:makeAvg(SG_AVG_T,0.5),dn:makeAvg(SG_AVG_T,0.5),nU:0,nD:0},
             {up:makeAvg(SG_AVG_T,0.5),dn:makeAvg(SG_AVG_T,0.5),nU:0,nD:0},
             {up:makeAvg(SG_AVG_T,0.5),dn:makeAvg(SG_AVG_T,0.5),nU:0,nD:0}]};
}
function sgResetCounts(sc){ for(const c of sc.c){ avgReset(c.up); avgReset(c.dn); c.nU=0; c.nD=0; } }
function sgClear(sc){ sc.parts=[]; sc.last=null; }
function sgBlock(st){ return (st.sgMode==='continuous'&&sgAxes(st).length>1)?st.sgBlock:'none'; }
function sgShoot(sc,st){
  const two=sgAxes(st).length>1, cap=st.sgMode==='single'?SG_MAXP1:SG_MAXP;
  if(sc.parts.length>=cap) return false;
  const p={t0:sc.t, r0:sgSource(st), jy:0.05*(2*rngNext(sc.R)-1), up1:null, up2:null, r1:null, r2:null, two, dead:false};
  sc.parts.push(p); if(st.sgMode==='single') sc.last=p;
  return true;
}
/* advance: measure at each magnet's middle, stop blocked particles at the
   blocker on magnet 1's exit, count, and retire particles at the end of their
   path (a single particle rests there 1.5 s so it can be read) */
const SG_BLOCK_D=2.35;          /* path length at which the blocker catches a particle (x = 2.30) */
function sgCount(sc,k,up){ if(up){ sc.c[k].nU++; avgCount(sc.c[k].up); } else { sc.c[k].nD++; avgCount(sc.c[k].dn); } }
function sgAdvance(sc,st,dt){
  if(!(dt>0)) return;
  const axes=sgAxes(st), block=sgBlock(st), hold=st.sgMode==='single'?1.5:0.05;
  if(st.sgMode==='continuous'){
    const n=SG_RATE*st.sgAmount*dt, nf=Math.floor(n);
    for(let i=0;i<nf;i++) sgShoot(sc,st);
    sc.acc+=n-nf; while(sc.acc>=1){ sgShoot(sc,st); sc.acc-=1; }
  }
  sc.t+=dt;
  const keep=[];
  for(const p of sc.parts){
    const d=SG_SPEED*(sc.t-p.t0);
    if(p.up1===null&&d>=1.5){ const m=measureAlong(sc.R,p.r0,AXV[axes[0]]); p.up1=m.up; p.r1=m.r; sgCount(sc,0,m.up); }
    if(p.up1!==null&&block!=='none'&&(block==='up')===p.up1&&d>=SG_BLOCK_D) p.dead=true;
    if(p.two&&!p.dead&&p.up1!==null&&p.up2===null&&d>=polyLen(sgWaypoints(p))){
      const k=p.up1?1:2, m=measureAlong(sc.R,p.r1,AXV[axes[k]]); p.up2=m.up; p.r2=m.r; sgCount(sc,k,m.up); }
    const done=p.up1!==null&&(!p.two||p.up2!==null)&&d>=polyLen(sgWaypoints(p))+hold;
    if(!p.dead&&!done) keep.push(p);
  }
  sc.parts=keep;
  for(const c of sc.c){ avgStep(c.up,dt); avgStep(c.dn,dt); }
}

/* ================================================================== *
 *  THE BLOCH SPHERE (PhET's Bloch Sphere screen)                      *
 * ================================================================== */
const BL={STEP:Math.PI/12, DELAY:0.75, DELAY_MAX:1, NS_PER_S:0.25, ATOMS:10};   /* PhET's values */
/* The field: PhET's strength s in [-1, 1] turns the state once per ns at
   |s| = 1.  The remake makes it an electron in B = s B0 along +z:
   f = (gamma_e/2pi) B, and B0 is the field that gives 1 GHz.  CODATA 2022
   gamma_e/2pi = 28 024.951 3861 MHz/T (bloch_sphere.html; = |g_e| mu_B/h). */
const GAMMA_E_MHZ_T=28024.9513861, G_E=-2.00231930436092, MUB_HZ_T=13996244917.1;
const B0_T=1e3/GAMMA_E_MHZ_T;   /* tesla: 1000 MHz / (MHz/T) */
/* the azimuth advances by w t with w = 2 pi s per ns: counterclockwise about
   +z for s > 0, the electron's sense (and PhET's).  EXACT: a rotation of the
   prepared vector, never an integrated one */
function larmorAngle(s,tauNs){ return 2*Math.PI*s*tauNs; }
function precess(r0,s,tauNs){ return rotate3(r0,[0,0,1],larmorAngle(s,tauNs)); }
/* the same thing on the ket: U = exp(-i w t sigma_z / 2) */
function precessU(s,tauNs){ return unitary([0,0,1],larmorAngle(s,tauNs)); }
const BL_PRESETS={'+X':[Math.PI/2,0],'-X':[Math.PI/2,Math.PI],'+Y':[Math.PI/2,Math.PI/2],'-Y':[Math.PI/2,3*Math.PI/2],
                  '+Z':[0,0],'-Z':[Math.PI,0]};
function makeBlochScene(seed){ return {R:rngMake(seed), seed, phase:'prepared', tau:0, r:[], up:0, dn:0, lastUp:null}; }
function blochPrep(st){ return blochOfAngles(st.bTheta,st.bPhi); }
function blochNAtoms(st){ return st.bAtoms===10?10:1; }
function blochReprepare(sc,st){ const r0=blochPrep(st); sc.r=[]; for(let i=0;i<BL.ATOMS;i++) sc.r.push(r0.slice()); sc.tau=0; sc.phase='prepared'; sc.lastUp=null; }
function blochResetCounts(sc){ sc.up=0; sc.dn=0; }
function blochObserve(sc,st){
  const n=BASIS[st.bAxis].n, na=blochNAtoms(st);
  let u=0;
  for(let i=0;i<na;i++){ const m=measureAlong(sc.R,sc.r[i],n); sc.r[i]=m.r; if(m.up) u++; }
  sc.up+=u; sc.dn+=na-u; sc.lastUp=u; sc.phase='observed';
}
/* PhET's single button: Observe (no field) or Start (field on), then Reprepare */
function blochButton(sc,st){
  if(sc.phase==='observed'){ blochReprepare(sc,st); return 'reprepared'; }
  if(sc.phase==='timing') return 'busy';
  if(st.bField){ sc.phase='timing'; sc.tau=0; return 'timing'; }
  blochObserve(sc,st); return 'observed';
}
function blochAdvance(sc,st,dtWall){
  if(sc.phase!=='timing'||!(dtWall>0)) return false;
  sc.tau=Math.min(sc.tau+dtWall*BL.NS_PER_S,st.bDelay);
  const r0=blochPrep(st), s=st.bField?st.bStrength:0;
  for(let i=0;i<BL.ATOMS;i++) sc.r[i]=precess(r0,s,sc.tau);
  if(sc.tau>=st.bDelay) blochObserve(sc,st);
  return true;
}
/* what the measurement will see: P(up along n) at the moment of observation */
function blochPUp(st){
  const r=st.bField?precess(blochPrep(st),st.bStrength,st.bDelay):blochPrep(st);
  return bornP(r,BASIS[st.bAxis].n);
}

/* ================================================================== *
 *  THE BORN RULE view: the half-angle, and measurement in sequence    *
 * ================================================================== */
function bornSpin(ThDeg){ const c=Math.cos(ThDeg*DEG/2); return c*c; }      /* cos^2(Theta/2) */
function bornPhoton(thDeg){ const c=Math.cos(thDeg*DEG); return c*c; }     /* cos^2(theta): Malus */
/* a chain of N magnets from +z to -z in equal steps: every stage passes its
   up beam with cos^2(pi/2N), so T(N) = cos^(2N)(pi/2N) -> 1 as N -> infinity */
function chainT(N){ return Math.pow(Math.cos(Math.PI/(2*N)),2*N); }
function middleSpin(alDeg){ const s=Math.sin(alDeg*DEG); return s*s/4; }       /* z -> alpha -> -z */
function middlePhoton(alDeg){ const s=Math.sin(2*alDeg*DEG); return s*s/4; }   /* H -> alpha -> V */
function chainMC(seed,N,n){
  const R=rngMake(seed); let ok=0;
  for(let i=0;i<n;i++){
    let r=[0,0,1], alive=true;
    for(let k=1;k<=N;k++){ const a=Math.PI*k/N, m=measureAlong(R,r,[Math.sin(a),0,Math.cos(a)]); if(m.up) r=m.r; else { alive=false; break; } }
    if(alive) ok++;
  }
  return ok;
}
function middleSpinMC(seed,alDeg,n){
  const R=rngMake(seed), a=alDeg*DEG, nn=[Math.sin(a),0,Math.cos(a)]; let ok=0;
  for(let i=0;i<n;i++){ const m=measureAlong(R,[0,0,1],nn); if(m.up){ const m2=measureAlong(R,m.r,[0,0,1]); if(!m2.up) ok++; } }
  return ok;
}
function middlePhotonMC(seed,alDeg,n){
  const R=rngMake(seed); let ok=0;
  /* through a polariser at alpha: pass with cos^2(alpha) (the H component of
     the analyser frame is the photon's own V at 90 - alpha); then V passes sin^2 */
  for(let i=0;i<n;i++) if(photonDecide(R,90-alDeg)==='V'&&photonDecide(R,alDeg)==='V') ok++;
  return ok;
}
function bornSpinMC(seed,ThDeg,n){ const R=rngMake(seed), t=ThDeg*DEG, r=[Math.sin(t),0,Math.cos(t)]; let up=0; for(let i=0;i<n;i++) if(measureAlong(R,r,[0,0,1]).up) up++; return up; }
function bornPhotonMC(seed,thDeg,n){ return n-photonBatch(seed,thDeg,n); }   /* the H (transmitted) count */
