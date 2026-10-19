
/* ================================================================== *
 *  the physics: PhET's constants, the N-sheet grey atmosphere solved  *
 *  in closed form AND by a dense linear solve, PhET's own layer ODE,  *
 *  and the photon random walk with a bit-exact seeded generator.      *
 *  Every number here is derived in build/greenhouse-effect/derive.py. *
 * ================================================================== */

/* plain() can only decode the entities ENTS carries, and an unknown one reaches the canvas
   VERBATIM (Known-bad list, buoyancy.html / wave_fronts.html).  The shared table has no thin
   space, and this sim writes "F a/(2-a)" with one in every caption, so extend the table here
   rather than editing the shared helper — and assert the extension in selfTest. */
ENTS['&thinsp;']=' '; ENTS['&ensp;']=' '; ENTS['&emsp;']=' ';
ENTS['&sup1;']='¹'; ENTS['&frac14;']='¼'; ENTS['&frac34;']='¾';
ENTS['&part;']='∂'; ENTS['&nabla;']='∇'; ENTS['&sum;']='∑'; ENTS['&lang;']='⟨'; ENTS['&rang;']='⟩';

/* --- PhET's constants, read from docs/phets/greenhouse-effect_en.html 1.3.13 --- */
const GH={
  SIGMA:5.670374419e-8,        /* GreenhouseEffectConstants.STEFAN_BOLTZMANN_CONSTANT */
  S_SUN:343.6,                 /* SunEnergySource.OUTPUT_ENERGY_RATE, W/m^2 */
  INT_MIN:0.5, INT_MAX:2.0,    /* proportionateOutputRateProperty range */
  ALB_MEADOW:0.2,              /* GroundLayer.GREEN_MEADOW_ALBEDO */
  ALB_GLACIER:0.225,           /* GroundLayer.PARTIALLY_GLACIATED_LAND_ALBEDO */
  ALB_LM:0.3,                  /* LayerModelModel initialAlbedo */
  ALB_MIN:0, ALB_MAX:0.9,      /* GroundLayer albedoProperty range */
  TMIN_NIGHT:245,              /* GroundLayer.MINIMUM_EARTH_AT_NIGHT_TEMPERATURE */
  TMIN_LM:125,                 /* the layer-model screen's ground floor */
  TOP:50000,                   /* LayersModel.HEIGHT_OF_ATMOSPHERE, m */
  N_CONC:12, N_LM:3,           /* sheets on the concentration screens / the layer model */
  ABS_COEF:0.85, SCALE_H:8400, /* a_i = 0.85 c exp(-z/8400) */
  ABS_MIN:0.1, ABS_MAX:1,      /* layersInfraredAbsorbanceProperty range */
  SPAN_W:85000,                /* SUNLIGHT_SPAN width, m (height 1) */
  CLOUD_W:18000, CLOUD_H:4000, CLOUD_Y:20000, CLOUD_X:-16000,
  CLOUD_REFL_TOP:0.125*85000/18000,   /* topVisibleLightReflectivity */
  RHO_EARTH:1250, CP_EARTH:1250,
  RHO_GLASS:2500, CP_GLASS:840,
  VOL_COEF:3e-7,               /* mass = SPAN_W * 1 * 3e-7 * density */
  T_MAX_EXPECTED:309,          /* GreenhouseEffectObservationWindow.EXPECTED_MAX_TEMPERATURE */
  PHOTON_HOLD_CONC:1.0,        /* photonAbsorptionTime on the concentration screens */
  PHOTON_HOLD_LM:0.25,         /* and on the layer model */
  IR_RATE_DIV:7.8,             /* sigma T^4 / 390 * 5 * 10 = sigma T^4 / 7.8 per second */
  VIS_RATE:10,                 /* visible photons per second at intensity 1 */
  SHOW_ONE_IN:5                /* PhET draws one photon in five unless "more photons" */
};
/* the cloud reflects energy * topVisibleLightReflectivity * (cloudWidth/spanWidth): the two
   factors cancel to exactly 0.125 of the incoming sunlight */
const CLOUD_REFL=GH.CLOUD_REFL_TOP*GH.CLOUD_W/GH.SPAN_W;
/* PhET's thermal response, K per (J/m^2) absorbed: area / (mass * specific heat) */
const K_GROUND=GH.SPAN_W/(GH.SPAN_W*GH.VOL_COEF*GH.RHO_EARTH*GH.CP_EARTH);
const K_SHEET =GH.SPAN_W/(GH.SPAN_W*GH.VOL_COEF*GH.RHO_GLASS*GH.CP_GLASS);

/* physics, from CODATA (scipy) — the sim asserts PhET's rounded sigma against this one */
const SIGMA_CODATA=5.670374419184e-8;
const SOLAR_CONSTANT=1361;     /* 2015 IAU nominal total solar irradiance, W/m^2 */
const EARTH_ALBEDO=0.30;       /* the textbook Bond albedo; NASA's fact sheet gives 0.306 */
const EARTH_TSURF=288;         /* the conventional global mean surface temperature, K */

/* PhET's four dates: concentration, then the mixing ratios its panel prints */
const DATES=[
  {id:'iceAge',name:'ice age',  c:0.625,  co2:180, ch4:380,  n2o:215, glacier:true},
  {id:'y1750', name:'1750',     c:0.7147, co2:277, ch4:694,  n2o:271, glacier:false},
  {id:'y1950', name:'1950',     c:0.7182, co2:311, ch4:1116, n2o:288, glacier:false},
  {id:'y2020', name:'2020',     c:0.7446, co2:413, ch4:1889, n2o:333, glacier:false}
];

function teff(F){ return Math.pow(Math.max(F,0)/GH.SIGMA,0.25); }
function sbFlux(T){ return GH.SIGMA*T*T*T*T; }
function kToC(K){ return K-273.15; }
function kToF(K){ return (K-273.15)*9/5+32; }
function tempIn(K,unit){ return unit==='C'?kToC(K):(unit==='F'?kToF(K):K); }
const UNIT_SYM={K:'K',C:'°C',F:'°F'};

/* PhET: spacing = 50000/(n+1), sheet i at spacing*(i+1) */
function layerAltitudes(n){
  const out=[], sp=GH.TOP/(n+1);
  for(let i=0;i<n;i++) out.push(sp*(i+1));
  return out;
}
/* ConcentrationModel: energyAbsorptionProportion = 0.85 * concentration * exp(-z/8400) */
function concAbsorbance(c,n){
  const N=(n===undefined)?GH.N_CONC:n;
  return layerAltitudes(N).map(z=>GH.ABS_COEF*c*Math.exp(-z/GH.SCALE_H));
}

/* ------------------------------------------------------------------ *
 *  the closed form.  Each sheet conserves energy, so the net upward
 *  flux U_i - D_i is the same at every level and equals F at the top;
 *  substituting D_i = U_i - F into the transfer and balance equations
 *  gives U_i = U_{i-1} - F a_i/(2-a_i), whence
 *      sigma T_s^4 = F [ 1 + sum_i a_i/(2-a_i) ].
 *  (derive.py carries the derivation and the brute-force check.)
 * ------------------------------------------------------------------ */
function solveClosed(a,F){
  const n=a.length, step=new Array(n);
  let sum=0;
  for(let i=0;i<n;i++){ step[i]=a[i]/(2-a[i]); sum+=step[i]; }
  const Eg=F*(1+sum);
  const U=new Array(n+1), D=new Array(n+1), J=new Array(n);
  U[0]=Eg;
  for(let i=0;i<n;i++) U[i+1]=U[i]-F*step[i];
  for(let i=0;i<=n;i++) D[i]=U[i]-F;
  for(let i=0;i<n;i++) J[i]=a[i]*(U[i]+D[i+1])/2;
  return {a,F,Eg,U,D,J,sum,
          Tg:teff(Eg),
          Tlayer:J.map(teff),                                   /* PhET's convention */
          Tkirch:J.map((j,i)=>a[i]>0?teff(j/a[i]):0),            /* emissivity = absorptivity */
          esc:Eg>0?F/Eg:1,
          Dg:D[0], Utop:U[n]};
}

/* Gaussian elimination with partial pivoting — used only by the independent solver below
   and by selfTest, never in a draw path. */
function gaussSolve(M,b){
  const n=b.length, A=M.map((r,i)=>r.slice().concat([b[i]]));
  for(let k=0;k<n;k++){
    let p=k;
    for(let i=k+1;i<n;i++) if(Math.abs(A[i][k])>Math.abs(A[p][k])) p=i;
    const t=A[k]; A[k]=A[p]; A[p]=t;
    if(Math.abs(A[k][k])<1e-300) throw new Error('gaussSolve: singular');
    for(let i=k+1;i<n;i++){
      const f=A[i][k]/A[k][k];
      for(let j=k;j<=n;j++) A[i][j]-=f*A[k][j];
    }
  }
  const x=new Array(n);
  for(let i=n-1;i>=0;i--){
    let s=A[i][n];
    for(let j=i+1;j<n;j++) s-=A[i][j]*x[j];
    x[i]=s/A[i][i];
  }
  return x;
}
/* The SAME steady state, solved as a dense linear system in (Eg, J_1..J_N) straight from the
   transfer and balance equations, without ever using the net-flux invariant.  Two independent
   routes to one answer — the PLAYBOOK's rule for anything implemented cleverly. */
function solveBrute(a,F){
  const n=a.length;
  const U=[], D=[];
  for(let i=0;i<=n;i++){ U.push(new Array(n+1).fill(0)); D.push(new Array(n+1).fill(0)); }
  U[0][0]=1;
  for(let i=0;i<n;i++){
    for(let j=0;j<=n;j++) U[i+1][j]=(1-a[i])*U[i][j];
    U[i+1][1+i]+=1;
  }
  for(let i=n-1;i>=0;i--){
    for(let j=0;j<=n;j++) D[i][j]=(1-a[i])*D[i+1][j];
    D[i][1+i]+=1;
  }
  const M=[], rhs=[];
  const r0=new Array(n+1).fill(0);
  for(let j=0;j<=n;j++) r0[j]=-D[0][j];
  r0[0]+=1;
  M.push(r0); rhs.push(F);                                    /* Eg - D_0 = F */
  for(let i=0;i<n;i++){
    const r=new Array(n+1).fill(0);
    for(let j=0;j<=n;j++) r[j]=-a[i]*(U[i][j]+D[i+1][j]);
    r[1+i]+=2;
    M.push(r); rhs.push(0);                                   /* 2 J_i = a_i (U_{i-1}+D_i) */
  }
  const x=gaussSolve(M,rhs);
  const Uv=U.map(row=>row.reduce((s,c,j)=>s+c*x[j],0));
  const Dv=D.map(row=>row.reduce((s,c,j)=>s+c*x[j],0));
  return {Eg:x[0],J:x.slice(1),U:Uv,D:Dv,Tg:teff(x[0]),Tlayer:x.slice(1).map(teff)};
}
/* the residuals the suite asserts: every sheet, the ground, the top, and the net flux */
function balanceResiduals(s){
  const a=s.a, n=a.length;
  let lay=0, net=0;
  for(let i=0;i<n;i++) lay=Math.max(lay,Math.abs(a[i]*(s.U[i]+s.D[i+1])-2*s.J[i]));
  for(let i=0;i<=n;i++) net=Math.max(net,Math.abs(s.U[i]-s.D[i]-s.F));
  return {layer:lay, toa:Math.abs(s.U[n]-s.F), ground:Math.abs(s.Eg-s.F-s.D[0]), net};
}

/* ------------------------------------------------------------------ *
 *  PhET's own layer ODE, marched forward.  A sheet's linearised rate
 *  is 8 K_SHEET sigma T^3, so forward Euler needs h < 2/(8 K sigma
 *  T^3) — 0.0198 s at 520 K.  SUBSTEPS keeps the sim's step inside it
 *  and stepModel CLAMPS against the bound rather than trusting it.
 * ------------------------------------------------------------------ */
const FRAME_DT=1/60, SUBSTEPS=4;
function stabilityH(Tmax){ return 2/(8*K_SHEET*GH.SIGMA*Tmax*Tmax*Tmax); }
/* PhET's starting state: the ground at ITS OWN floor (245 K on the concentration screens,
   125 K on the layer model) and every sheet at the 0 K its constructor leaves it at */
function makeThermal(n,T0){ return {Tg:T0, T:new Array(n).fill(0), t:0}; }
/* the instantaneous fluxes for a given set of temperatures (NOT the steady state) */
function fluxesNow(th,a){
  const n=a.length, U=new Array(n+1), D=new Array(n+1);
  const Jg=sbFlux(th.Tg), J=th.T.map(sbFlux);
  U[0]=Jg;
  for(let i=0;i<n;i++) U[i+1]=(1-a[i])*U[i]+J[i];
  D[n]=0;
  for(let i=n-1;i>=0;i--) D[i]=(1-a[i])*D[i+1]+J[i];
  return {U,D,Jg,J};
}
function marchFrame(th,a,F,Tfloor,dt,nsub){
  const n=a.length, h=(dt===undefined?FRAME_DT:dt)/(nsub===undefined?SUBSTEPS:nsub);
  const m=(nsub===undefined?SUBSTEPS:nsub);
  const hmax=stabilityH(Math.max(300,th.Tg+120));
  const steps=h>hmax?Math.ceil(m*h/hmax):m;                   /* clamp against the bound */
  const hh=(dt===undefined?FRAME_DT:dt)/steps;
  for(let k=0;k<steps;k++){
    const f=fluxesNow(th,a);
    let Tg=th.Tg+K_GROUND*(F+f.D[0]-f.Jg)*hh;
    if(Tg<Tfloor) Tg=Tfloor;
    const T=new Array(n);
    for(let i=0;i<n;i++){
      let Ti=th.T[i]+K_SHEET*(a[i]*(f.U[i]+f.D[i+1])-2*f.J[i])*hh;
      if(Ti<0) Ti=0;
      T[i]=Ti;
    }
    th.Tg=Tg; th.T=T;
  }
  th.t+=(dt===undefined?FRAME_DT:dt);
  return th;
}

/* ------------------------------------------------------------------ *
 *  the photon picture
 * ------------------------------------------------------------------ */
/* A 32-bit linear congruential generator.  Every product stays below 2^53, so JavaScript's
   doubles carry it exactly and derive.py's Python twin produces the IDENTICAL stream — which
   is what lets the suite pin the Monte Carlo against the Markov chain. */
function makeRng(seed){
  let s=((seed|0)>>>0)%4294967296;
  return {next(){ s=(1664525*s+1013904223)%4294967296; return s/4294967296; },
          seed(v){ s=((v|0)>>>0)%4294967296; },
          state(){ return s; }};
}
/* The chance that an IR photon leaving the ground upward escapes to space, under "absorbed
   with probability a_i on crossing sheet i, then re-emitted up or down at even odds".
   p_i = escape from moving up about to cross sheet i; q_i = the same moving down.
   p_{n+1} = 1 (space), q_0 = 0 (the ground absorbs all infrared). */
function escapeMarkov(a){
  const n=a.length;
  if(n===0) return 1;
  const N=2*n, M=[], b=new Array(N).fill(0);
  for(let i=0;i<N;i++) M.push(new Array(N).fill(0));
  const pi=i=>i-1, qi=i=>n+i-1;
  for(let i=1;i<=n;i++){
    /* cGo = pass through (1-a) OR be absorbed and sent on the same way (a/2);
       cBack = be absorbed and sent back the other way (a/2). */
    const ai=a[i-1], cGo=(1-ai)+ai/2, cBack=ai/2;
    M[pi(i)][pi(i)]=1;
    if(i+1<=n) M[pi(i)][pi(i+1)]-=cGo; else b[pi(i)]+=cGo;    /* above the top sheet: space */
    if(i-1>=1) M[pi(i)][qi(i-1)]-=cBack;                      /* q_0 = 0: the ground absorbs */
    M[qi(i)][qi(i)]=1;
    if(i-1>=1) M[qi(i)][qi(i-1)]-=cGo;
    if(i+1<=n) M[qi(i)][pi(i+1)]-=cBack; else b[qi(i)]+=cBack;
  }
  return gaussSolve(M,b)[pi(1)];
}
/* the same walk, simulated with the seeded generator — returns the measured statistics */
function escapeMonteCarlo(a,m,seed){
  const n=a.length, r=makeRng(seed===undefined?12345:seed);
  let esc=0, cross=0, absorbed=0, up=0;
  for(let k=0;k<m;k++){
    let i=1, d=1;
    for(;;){
      if(i>n){ esc++; break; }
      if(i<1) break;
      cross++;
      if(r.next()<a[i-1]){
        absorbed++;
        if(r.next()<0.5){ d=1; up++; } else d=-1;
        i+=d;
      } else i+=d;
    }
  }
  return {p:esc/m, esc, cross, absorbed, up, m};
}
/* PhET's photon production rates (a display layer: the temperature comes from the fluxes) */
function irPhotonRate(T,Tfloor){ return T>Tfloor?sbFlux(T)/GH.IR_RATE_DIV:0; }
