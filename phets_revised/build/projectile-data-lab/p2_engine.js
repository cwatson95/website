
/* ================================================================== *
 *  the engine: PhET's constants, its launch mechanism, the exact      *
 *  distribution of the landing distance, and the statistics.          *
 *  Every constant below is read from the minified original            *
 *  docs/phets/projectile-data-lab_en.html and cited as PhET's value;  *
 *  everything derived is pinned in selfTest to derive.py.             *
 * ================================================================== */
const PDL={
  G:9.81,                 /* PDLConstants.FREEFALL_ACCELERATION      */
  FIELD:100,              /* PDLConstants.MAX_FIELD_DISTANCE, metres */
  RAISED_H:12,            /* PDLConstants.RAISED_LAUNCHER_HEIGHT     */
  ANG_SD:[0.2,5],         /* ANGLE_STANDARD_DEVIATION_RANGE, degrees */
  LAUNCH_GAP:0.7,         /* MINIMUM_TIME_BETWEEN_LAUNCHES, seconds  */
  MAX_PROJ:500,           /* MAX_PROJECTILES_VSM_FIELD_DEFAULT       */
  MAX_SAMPLES:200,        /* the maxSamples query parameter          */
  SAMPLE_TIME:{2:0.75,5:2,15:5,40:9}, /* SamplingField.totalSampleTime */
  N_FIELDS:6,             /* six fields on the VSM screens           */
  SIZES:[2,5,15,40],      /* the Sampling screen's sample sizes      */
  BINW:[0.5,1,2,5,10],    /* selectedBinWidthProperty validValues    */
  NBINS:[10,20,50,100,200], /* selectedTotalBinsProperty validValues */
  INTERVAL:[40,60],       /* IntervalTool edge1, edge2 defaults      */
  ZCAP:12,                /* beyond 12 sd a normal density is <1e-32 */
  TIME_SPEED_FAST:6,      /* PDLConstants.TIME_SPEED_FAST            */
  NGL:96,                 /* Gauss-Legendre nodes (derive.py's rule) */
  /* panels for the density's theta integral.  The MOMENTS are a product rule
     over a smooth integrand and one panel is exact to 1e-15, but the density
     at a FIXED r is not: only the angles whose v*(r,theta) lands within a few
     sd of the mean speed contribute, so a small speed spread beside a large
     angle spread makes the integrand a narrow spike that one 96-node rule
     rings around (29 % on mystery launcher 2, 292 % raised).  Eight panels
     take every case tested to 0.000 % against a 64-panel reference, and
     selfTest asserts that convergence rather than assuming it. */
  NPANEL:8
};
/* LauncherMechanism(tandem, speedMean, speedStandardDeviation) */
const MECH={spring:{id:'spring',name:'spring',mean:23,sd:0.5},
            pressure:{id:'pressure',name:'pressure',mean:24,sd:0.2},
            explosion:{id:'explosion',name:'explosion',mean:25,sd:1.2},
            custom:{id:'custom',name:'custom',mean:24,sd:0.5}};
const MECH_LIST=[MECH.spring,MECH.pressure,MECH.explosion];
/* ProjectileType(tandem, speedMultiplier) */
const PTYPES=[{id:'cannonball',name:'cannonball',mult:1},
              {id:'pumpkin',name:'pumpkin',mult:1.1},
              {id:'piano',name:'piano',mult:0.9}];
/* launcherOrientation: the mean launch angle, and the launch height */
const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:0},
               {id:'angle45',name:'45°',ang:45,h:0},
               {id:'angle60',name:'60°',ang:60,h:0},
               {id:'angle0Raised',name:'0° raised',ang:0,h:PDL.RAISED_H}];
/* the six mystery launchers: Range.getCenter(), max, min, min+length/4, min, max */
const ANG_C=0.5*(PDL.ANG_SD[0]+PDL.ANG_SD[1]);
const ANG_Q=PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])/4;
const LAUNCHERS=[{n:1,mech:'spring',sdAng:ANG_C},{n:2,mech:'pressure',sdAng:PDL.ANG_SD[1]},
                 {n:3,mech:'explosion',sdAng:PDL.ANG_SD[0]},{n:4,mech:'spring',sdAng:ANG_Q},
                 {n:5,mech:'pressure',sdAng:PDL.ANG_SD[0]},{n:6,mech:'explosion',sdAng:PDL.ANG_SD[1]}];

/* ---- the random stream: mulberry32 + Box-Muller (bit-exact twin in
   derive.py).  One pair of uniforms per normal, never cached: a draw count
   that does not depend on history is what keeps the stream reproducible. */
function pdlRng(seed){
  let a=seed>>>0;
  const R={
    next(){
      a=(a+0x6D2B79F5)>>>0;
      let t=Math.imul(a^(a>>>15),a|1);
      t=((t+Math.imul(t^(t>>>7),t|61))>>>0)^t;
      return ((t^(t>>>14))>>>0)/4294967296;
    },
    gauss(){ const u1=1-R.next(), u2=R.next(); return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2); }
  };
  return R;
}

/* ---- the trajectory --------------------------------------------------------
   y(t) = h + v sinθ t − g t²/2 = 0  ⇒  t = [v s + √(v²s² + 2gh)]/g,
   x(t) = v cosθ t  ⇒  R = (v cosθ/g)(v s + √(v²s² + 2gh)).  PhET's two
   closed forms; derive.py re-derives them and checks both against the root
   of y(t) = 0 and against a marched trajectory. */
function pdlRange(v,thDeg,h){
  const th=thDeg*Math.PI/180, s=Math.sin(th);
  return v*Math.cos(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*h));
}
/* the same range, multiplied through by the conjugate.  For a DOWNWARD launch
   (sin θ < 0) PhET's form adds two nearly equal numbers of opposite sign and
   loses digits — at v = 10⁶ m/s from 12 m it loses the answer entirely —
   whereas 2gh/(√(v²s²+2gh) − v s) is a quotient of positives and cannot.
   The two agree to 1e-15 over everything the sliders reach; PhET's form is the
   one the sim and derive.py evaluate, so that the bit-level pins hold. */
function pdlRangeStable(v,thDeg,h){
  const th=thDeg*Math.PI/180, s=Math.sin(th), Q=Math.sqrt(v*v*s*s+2*PDL.G*h);
  if(h===0) return s<=0?0:v*Math.cos(th)/PDL.G*2*v*s;
  return v*Math.cos(th)/PDL.G*(2*PDL.G*h)/(Q-v*s);
}
function pdlFlight(v,thDeg,h){
  const s=Math.sin(thDeg*Math.PI/180), a=v*s/PDL.G;
  return a+Math.sqrt(a*a+2*h/PDL.G);
}
function pdlHeight(v,thDeg,h,t){ return h+v*Math.sin(thDeg*Math.PI/180)*t-0.5*PDL.G*t*t; }
/* ∂R/∂v at fixed θ — positive for every v, so R is monotone in the speed */
function pdlDRdv(v,thDeg,h){
  const th=thDeg*Math.PI/180, s=Math.sin(th), c=Math.cos(th);
  const Q=Math.sqrt(v*v*s*s+2*PDL.G*h);
  return c/PDL.G*(2*v*s+(2*v*v*s*s+2*PDL.G*h)/Q);
}
/* the angle of maximum range from a height: cos 2θ* = gh/(v² + gh) */
function pdlMaxAngle(v,h){ return 0.5*Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }
/* the speed that lands at r from angle θ.  R(v) rises monotonically but from
   a height a DOWNWARD launch saturates: as v grows the path straightens and
   the range tends to h/tan|θ|, so beyond that no speed reaches r and the
   answer is null rather than a Newton step that divides by nothing. */
function pdlVStar(r,thDeg,h){
  const th=thDeg*Math.PI/180, s=Math.sin(th), c=Math.cos(th);
  if(!(c>1e-9)||!(r>0)) return null;
  if(h===0) return s<=0?null:Math.sqrt(r*PDL.G/Math.sin(2*th));
  if(s<0&&r>=h*c/(-s)) return null;
  let v=s>1e-4?Math.sqrt(r*PDL.G/Math.sin(2*th)):r*Math.sqrt(PDL.G/(2*h))/c;
  for(let i=0;i<120;i++){
    const d=pdlDRdv(v,thDeg,h);
    if(!(d>1e-12)) return null;
    const step=(pdlRange(v,thDeg,h)-r)/d;
    v=Math.max(1e-9,v-step);
    if(Math.abs(step)<1e-15*Math.max(1,v)) break;
  }
  return Math.abs(pdlRange(v,thDeg,h)-r)<1e-9*Math.max(1,r)?v:null;
}

/* ---- PhET's angle stabiliser -----------------------------------------------
   standardDeviationAngle = linear(1, 0, sdMin, sdMax, stability): the slider
   runs the other way round, stability 1 giving the TIGHTEST launcher. */
function pdlSdOfStab(stab){ return PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])*(1-stab); }
function pdlStabOfSd(sd){ return 1-(sd-PDL.ANG_SD[0])/(PDL.ANG_SD[1]-PDL.ANG_SD[0]); }

/* ---- one launch, exactly PhET's createProjectile ---------------------------
   the angle first (re-drawn up to 100 times while it is outside (0°, 90°),
   and not re-drawn at all on the raised launcher, which PhET exempts), then
   the speed (re-drawn while it is ≤ 0).  Both are therefore truncated
   normals; section 4 of derive.py measures how much that truncation moves
   the answer (5.5e-8 m at worst). */
function pdlDraw(rng,cfg){
  let a=cfg.meanAng+rng.gauss()*cfg.sdAng;
  if(!cfg.raised){ let k=0; while(k<100&&(a<=0||a>=90)){ a=cfg.meanAng+rng.gauss()*cfg.sdAng; k++; } }
  const mu=cfg.meanSpeed*cfg.mult;
  let v=mu+rng.gauss()*cfg.sdSpeed;
  while(v<=0) v=mu+rng.gauss()*cfg.sdSpeed;
  return {v,ang:a};
}
function pdlConfig(mechId,sdAng,orientId,typeId,speedMean,speedSd){
  const M=MECH[mechId], O=ORIENTS.find(o=>o.id===orientId)||ORIENTS[0];
  const T=PTYPES.find(t=>t.id===typeId)||PTYPES[0];
  return {mech:mechId, sdAng, meanAng:O.ang, h:O.h, raised:O.h>0,
          mult:T.mult, meanSpeed:speedMean===undefined?M.mean:speedMean,
          sdSpeed:speedSd===undefined?M.sd:speedSd, orient:O.id, type:T.id};
}

/* ================================================================== *
 *  the exact distribution                                             *
 * ================================================================== */
/* Gauss-Legendre nodes and weights on [-1,1] by Newton on P_n (the standard
   three-term recurrence).  Computed here rather than pasted: selfTest asserts
   them against numpy's leggauss(96), which is a stronger check than a table
   of literals could be. */
function pdlGauleg(n,seed){
  const sd=seed===undefined?0.75:seed;
  const x=new Array(n), w=new Array(n), m=(n+1)>>1;
  for(let i=0;i<m;i++){
    let z=Math.cos(Math.PI*(i+sd)/(n+0.5)), pp=1, z1;
    for(let it=0;it<100;it++){
      let p1=1, p2=0;
      for(let j=0;j<n;j++){ const p3=p2; p2=p1; p1=((2*j+1)*z*p2-j*p3)/(j+1); }
      pp=n*(z*p1-p2)/(z*z-1);
      z1=z; z=z1-p1/pp;
      if(Math.abs(z-z1)<=1e-16) break;
    }
    x[i]=-z; x[n-1-i]=z;
    w[i]=2/((1-z*z)*pp*pp); w[n-1-i]=w[i];
  }
  return {x,w};
}
const GL=pdlGauleg(PDL.NGL);
const NORM=1/Math.sqrt(2*Math.PI);
function pdlPhi(z){ return NORM*Math.exp(-0.5*z*z); }
/* nodes z and weights carrying φ(z) dz over [a,b]; Σw = Φ(b) − Φ(a) */
function pdlZRule(a,b){
  const n=PDL.NGL, z=new Array(n), w=new Array(n);
  for(let i=0;i<n;i++){ z[i]=0.5*(b-a)*GL.x[i]+0.5*(a+b); w[i]=0.5*(b-a)*GL.w[i]*pdlPhi(z[i]); }
  return {z,w};
}
/* the z-interval of N(mu, sd) truncated to (lo, hi), capped at 12 sd */
function pdlZRange(mu,sd,lo,hi){
  return [lo===null?-PDL.ZCAP:Math.max(-PDL.ZCAP,(lo-mu)/sd),
          hi===null? PDL.ZCAP:Math.min( PDL.ZCAP,(hi-mu)/sd)];
}
/* the moments of the landing distance, over the SAME 96×96 product rule
   derive.py uses.  TWO passes: the mean first, then the central moments about
   it.  Assembling mu3 from the raw moments cancels five to seven digits
   (m3 ~ 2e5 against mu3 ~ 0.02) and the two languages round that cancellation
   differently — with the second pass they agree to 1e-15, and selfTest pins
   the difference between the two forms so the shortcut cannot come back. */
function pdlMomentGrid(cfg){
  const mu=cfg.meanSpeed*cfg.mult, sv=cfg.sdSpeed;
  const rv=pdlZRule.apply(null,pdlZRange(mu,sv,0,null));
  const rt=cfg.raised?pdlZRule(-PDL.ZCAP,PDL.ZCAP):pdlZRule.apply(null,pdlZRange(cfg.meanAng,cfg.sdAng,0,90));
  let wsum=0;
  for(let i=0;i<PDL.NGL;i++) for(let j=0;j<PDL.NGL;j++) wsum+=rv.w[i]*rt.w[j];
  const R=new Array(PDL.NGL*PDL.NGL), P=new Array(PDL.NGL*PDL.NGL);
  for(let j=0;j<PDL.NGL;j++){
    const th=(cfg.meanAng+cfg.sdAng*rt.z[j])*Math.PI/180, s=Math.sin(th), c=Math.cos(th);
    for(let i=0;i<PDL.NGL;i++){
      const v=mu+sv*rv.z[i], k=j*PDL.NGL+i;
      R[k]=v*c/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*cfg.h));
      P[k]=rv.w[i]*rt.w[j]/wsum;
    }
  }
  return {R,P};
}
function pdlMoments(cfg){
  const {R,P}=pdlMomentGrid(cfg), N=R.length;
  const m=[0,0,0,0];
  for(let k=0;k<N;k++){ let q=R[k]; m[0]+=P[k]*q; q*=R[k]; m[1]+=P[k]*q; q*=R[k]; m[2]+=P[k]*q; q*=R[k]; m[3]+=P[k]*q; }
  const mean=m[0];
  let c2=0,c3=0,c4=0;
  for(let k=0;k<N;k++){ const d=R[k]-mean, d2=d*d; c2+=P[k]*d2; c3+=P[k]*d2*d; c4+=P[k]*d2*d2; }
  return {m1:m[0],m2:m[1],m3:m[2],m4:m[3],mean,varr:c2,sd:Math.sqrt(c2),mu3:c3,mu4:c4};
}
/* the same central moments assembled from the RAW ones — kept only so
   selfTest can measure the cancellation it suffers (it is not used to draw
   or report anything) */
function pdlMomentsRaw(cfg){
  const M=pdlMoments(cfg), m1=M.m1;
  return {varr:M.m2-m1*m1, mu3:M.m3-3*m1*M.m2+2*m1*m1*m1,
          mu4:M.m4-4*m1*M.m3+6*m1*m1*M.m2-3*Math.pow(m1,4)};
}
/* memoised on the configuration: the readout, the captions and the drawing
   all ask for the same moments many times a frame, and the rule is 9216
   evaluations (about 7 ms for six configurations) */
const EXACT_CACHE={};
function pdlCfgKey(cfg){
  return [cfg.meanSpeed,cfg.sdSpeed,cfg.mult,cfg.meanAng,cfg.sdAng,cfg.h,cfg.raised?1:0].join('/');
}
function pdlExact(cfg){
  const k=pdlCfgKey(cfg);
  if(EXACT_CACHE[k]) return EXACT_CACHE[k];
  const M=pdlMoments(cfg);
  M.skew=M.mu3/Math.pow(M.sd,3); M.kurt=M.mu4/Math.pow(M.sd,4)-3;
  EXACT_CACHE[k]=M;
  return M;
}
/* the UNtruncated model in closed form, h = 0 only: R = v² sin2θ/g, and both
   E[v^2k] and E[sin^k 2θ] are exact for a normal —
   E[e^{iaθ}] = e^{iam − a²w²/2} gives every sine moment. */
function pdlClosed(mu,s,mDeg,wDeg){
  const m=mDeg*Math.PI/180, w=wDeg*Math.PI/180, g=PDL.G;
  const C=a=>Math.cos(a*m)*Math.exp(-0.5*a*a*w*w);
  const S=a=>Math.sin(a*m)*Math.exp(-0.5*a*a*w*w);
  const v2=mu*mu+s*s;
  const v4=Math.pow(mu,4)+6*mu*mu*s*s+3*Math.pow(s,4);
  const v6=Math.pow(mu,6)+15*Math.pow(mu,4)*s*s+45*mu*mu*Math.pow(s,4)+15*Math.pow(s,6);
  const v8=Math.pow(mu,8)+28*Math.pow(mu,6)*s*s+210*Math.pow(mu,4)*Math.pow(s,4)
          +420*mu*mu*Math.pow(s,6)+105*Math.pow(s,8);
  const s1=S(2), s2=0.5*(1-C(4)), s3=0.25*(3*S(2)-S(6)), s4=0.125*(3-4*C(4)+C(8));
  return [v2*s1/g, v4*s2/(g*g), v6*s3/(g*g*g), v8*s4/Math.pow(g,4)];
}
/* PhET's own spread estimate — SampleSizeThumbnailNode.calculateRangeStdDev,
   which is the first-order (delta-method) propagation through v² sin2θ/g and
   is what sets the Sampling thumbnails' x-range. */
function pdlDeltaSd(v,sdv,thDeg,sdthDeg){
  const s=thDeg*Math.PI/180, r=sdthDeg*Math.PI/180;
  const a=2*v/PDL.G*Math.sin(2*s), b=2*v*v/PDL.G*Math.cos(2*s);
  return Math.sqrt(a*a*sdv*sdv+b*b*r*r);
}
/* the exact density: f(r) = ∫ f_θ(θ) f_v(v*(r,θ))/|∂R/∂v| dθ over the
   accepted angles, on the same rule */
function pdlPdf(r,cfg,panels){
  const K=panels||PDL.NPANEL;
  const mu=cfg.meanSpeed*cfg.mult, sv=cfg.sdSpeed;
  const zr=cfg.raised?[-PDL.ZCAP,PDL.ZCAP]:pdlZRange(cfg.meanAng,cfg.sdAng,0,90);
  const rv=pdlZRule.apply(null,pdlZRange(mu,sv,0,null));
  let vw=0;
  for(let i=0;i<PDL.NGL;i++) vw+=rv.w[i];
  let tot=0, tw=0;
  for(let k=0;k<K;k++){
    const a=zr[0]+(zr[1]-zr[0])*k/K, b=zr[0]+(zr[1]-zr[0])*(k+1)/K;
    for(let j=0;j<PDL.NGL;j++){
      const z=0.5*(b-a)*GL.x[j]+0.5*(a+b), w=0.5*(b-a)*GL.w[j]*pdlPhi(z);
      tw+=w;
      const th=cfg.meanAng+cfg.sdAng*z, vs=pdlVStar(r,th,cfg.h);
      if(vs===null||!(vs>0)) continue;
      const zz=(vs-mu)/sv;
      tot+=w*(NORM*Math.exp(-0.5*zz*zz)/sv)/pdlDRdv(vs,th,cfg.h);
    }
  }
  return tot/(tw*vw);
}
/* the drawn curve is the same 201 points every frame while the launcher and
   the axis hold still, and it costs 8x96 integrand evaluations a point */
const PDF_CACHE={};
function pdlPdfCurve(cfg,lo,hi,n){
  const k=pdlCfgKey(cfg)+'/'+lo+'/'+hi+'/'+n;
  if(PDF_CACHE[k]) return PDF_CACHE[k];
  const xs=[], ys=[];
  for(let i=0;i<=n;i++){ const x=lo+(hi-lo)*i/n; xs.push(x); ys.push(pdlPdf(x,cfg)); }
  PDF_CACHE[k]={xs,ys};
  return PDF_CACHE[k];
}

/* ================================================================== *
 *  the statistics — PhET's conventions, pinned against numpy          *
 * ================================================================== */
/* PhET bins by Math.floor(x/w)*w, so a bin is [k w, (k+1) w) */
function pdlBinIndex(x,w){ return Math.floor(x/w); }
function pdlHistogram(xs,w){
  if(!xs.length) return {lo:0,counts:[],max:0,w};
  let lo=Infinity, hi=-Infinity;
  for(const x of xs){ const k=pdlBinIndex(x,w); if(k<lo) lo=k; if(k>hi) hi=k; }
  const counts=new Array(hi-lo+1).fill(0);
  for(const x of xs) counts[pdlBinIndex(x,w)-lo]++;
  let mx=0; for(const c of counts) if(c>mx) mx=c;
  return {lo,counts,max:mx,w};
}
function pdlMean(xs){ if(!xs.length) return null; let s=0; for(const x of xs) s+=x; return s/xs.length; }
/* PhET's getStandardDeviationDistance: Σ(x−x̄)²/(n−1), null below two
   projectiles.  ddof = 0 is offered beside it because the difference between
   the two conventions is exactly what a statistics sim is about. */
function pdlSd(xs,ddof){
  const d=ddof===undefined?1:ddof, n=xs.length;
  if(n<=d) return null;
  const m=pdlMean(xs);
  let s=0; for(const x of xs){ const e=x-m; s+=e*e; }
  return Math.sqrt(s/(n-d));
}
function pdlSe(xs){ const s=pdlSd(xs,1); return s===null?null:s/Math.sqrt(xs.length); }
function pdlMedian(xs){
  const n=xs.length; if(!n) return null;
  const a=xs.slice().sort((p,q)=>p-q);
  return n%2?a[(n-1)/2]:0.5*(a[n/2-1]+a[n/2]);
}
/* the interval tool: PhET counts x >= lo && x <= hi, both ends closed */
function pdlFraction(xs,lo,hi){
  if(!xs.length) return 0;
  const a=Math.min(lo,hi), b=Math.max(lo,hi);
  let k=0; for(const x of xs) if(x>=a&&x<=b) k++;
  return k/xs.length;
}
/* the probability the exact law puts in [a,b] — Simpson on the density */
function pdlProbIn(cfg,a,b,n){
  const N=(n||200)*2, dx=(b-a)/N;
  let s=0;
  for(let i=0;i<=N;i++){ const c=(i===0||i===N)?1:(i%2?4:2); s+=c*pdlPdf(a+i*dx,cfg); }
  return s*dx/3;
}

/* ================================================================== *
 *  a field: PhET's Field — one launcher, its projectiles, its stats   *
 * ================================================================== */
function fieldMake(seed,cfg){
  return {rng:pdlRng(seed),seed,cfg,landed:[],air:[],t:0,sinceLaunch:PDL.LAUNCH_GAP,
          n:0,samples:[],sampleN:0,firing:false,pending:0,size:0,lau:0,
          launched:0,tSample:0};
}
function fieldLaunch(F){
  if(F.landed.length+F.air.length>=PDL.MAX_PROJ) return null;
  const d=pdlDraw(F.rng,F.cfg);
  const p={v:d.v,ang:d.ang,x:pdlRange(d.v,d.ang,F.cfg.h),T:pdlFlight(d.v,d.ang,F.cfg.h),
           t:0,id:++F.n,type:F.cfg.type,sample:F.sampleN};
  F.air.push(p); F.sinceLaunch=0;
  return p;
}
function fieldStep(F,dt){
  F.t+=dt; F.sinceLaunch+=dt;
  let landedAny=false;
  for(let i=F.air.length-1;i>=0;i--){
    const p=F.air[i]; p.t+=dt;
    if(p.t>=p.T){ p.t=p.T; F.air.splice(i,1); F.landed.push(p); landedAny=true; }
  }
  return landedAny;
}
function fieldXs(F){ return F.landed.map(p=>p.x); }
function fieldClear(F){ F.landed.length=0; F.air.length=0; F.t=0; F.n=0;
  F.sinceLaunch=PDL.LAUNCH_GAP; F.rng=pdlRng(F.seed); F.samples.length=0; F.sampleN=0;
  F.firing=false; F.pending=0; F.launched=0; F.tSample=0; }
/* launch n at once and land them immediately (PhET's autoGenerateData) */
function fieldBatch(F,n){
  for(let k=0;k<n;k++){
    if(F.landed.length+F.air.length>=PDL.MAX_PROJ) break;
    const d=pdlDraw(F.rng,F.cfg);
    F.landed.push({v:d.v,ang:d.ang,x:pdlRange(d.v,d.ang,F.cfg.h),
                   T:pdlFlight(d.v,d.ang,F.cfg.h),t:pdlFlight(d.v,d.ang,F.cfg.h),
                   id:++F.n,type:F.cfg.type,sample:F.sampleN});
  }
}
/* starting a sample is ONE operation in ONE place: it was written twice — in
   fireField and again where continuous sampling rolls into the next one — and
   two guards on one path make each other's mutant invisible (Known-bad).  The
   field the sample will fill is emptied here and nowhere else. */
function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; F.tSample=0; }
/* the interval between the launches of one sample: PhET spreads them evenly
   over totalSampleTime rather than waiting for each to land */
function sampleStep(size){ return (PDL.SAMPLE_TIME[size]||2)/size; }
/* the Sampling screen: one sample is `size` launches, and its MEAN is the
   datum that goes into the histogram (PhET's SamplingField.getHistogramData) */
function sampleBatch(F,size,count){
  const out=[];
  for(let k=0;k<count&&F.samples.length<PDL.MAX_SAMPLES;k++){
    const xs=[], ps=[];
    for(let i=0;i<size;i++){
      const d=pdlDraw(F.rng,F.cfg), T=pdlFlight(d.v,d.ang,F.cfg.h);
      const p={v:d.v,ang:d.ang,x:pdlRange(d.v,d.ang,F.cfg.h),T,t:T,id:++F.n,
               type:F.cfg.type,sample:F.sampleN+1};
      xs.push(p.x); ps.push(p);
    }
    F.sampleN++;
    F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs)});
    /* the field shows the LAST sample, which is the one whose mean just
       joined the histogram — a field strip with nothing on it is a view that
       draws nothing */
    F.landed=ps; F.size=size;
    out.push(F.samples[F.samples.length-1]);
  }
  return out;
}
function sampleMeans(F){ return F.samples.map(s=>s.mean); }
