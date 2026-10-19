
/* ================================================================== *
 *  the model: PhET's bead lattice, exactly.  Every constant marked    *
 *  "PhET's value" was read out of wave-on-a-string_en.html 1.2.4      *
 *  (docs/phets/) and agrees with its doc/model.md.                    *
 * ================================================================== */
const NSEG=60;                 /* PhET's value: 61 beads, indices 0..60 */
const DX=10/80;                /* PhET's value: 10 model units apart at 80 per cm = 0.125 cm */
const LSTR=NSEG*DX;            /* 7.5 cm from bead 0 to bead 60 */
const LLOOSE=(NSEG-0.5)*DX;    /* the loose end reflects about bead 59.5 (y60 copies y59) */
const TMAX=0.8;                /* PhET's value: its tension slider tops out (and starts) at 0.8 */
const TMIN=TMAX/25;            /* 0.032: where v = sqrt(T) reaches PhET's slowest speed */
const VMAX=50*DX;              /* PhET's value: 50 lattice steps a second at full tension = 6.25 cm/s */
const BPD=0.1;                 /* PhET's value: beta = (0.2 x damping)/2 per step */
const SLOW=0.25;               /* PhET's value: slow motion */
const AMAX=1.3;                /* PhET's value: amplitude slider and the wrench's travel, cm */
const FMAX=3;                  /* PhET's value: frequency slider, Hz */
const WMIN=0.2, WMAX=1;        /* PhET's value: pulse width slider, s */
const REF_Y0=1.45;             /* PhET's value: the reference line starts 1.45 cm above the string */
const RULER_H=10, RULER_V=5;   /* PhET's value: the rulers are 10 cm and 5 cm long */

/* v = v_max sqrt(T / T_max): the physical law, over PhET's own speed range */
function speedOf(T){ return VMAX*Math.sqrt(T/TMAX); }
/* the lattice step: alpha = v dt/dx = 1, so the tension sets the clock, not the stencil */
function dtOf(T){ return DX/speedOf(T); }
function betaOf(d){ return BPD*d; }
/* PhET's own map, kept for the record (header, readout): steps per second linear
   in sqrt(T) from sqrt(0.2) -> 0.2 to sqrt(0.8) -> 1, times 50 */
function phetRate(T){ const s=Math.sqrt(T); return 50*(0.2+(1-0.2)*(s-Math.sqrt(0.2))/(Math.sqrt(0.8)-Math.sqrt(0.2))); }
/* the amplitude a travelling wave keeps per step (= per bead): sqrt((1-b)/(1+b)) = exp(-atanh b) */
function keepPerStep(b){ return Math.sqrt((1-b)/(1+b)); }
function decayLength(b){ return b>0?DX/Math.atanh(b):Infinity; }

/* the pulse generator: a triangle of height A lasting w (PhET's shape) */
function tri(u){ return (u>=0&&u<=1)?1-Math.abs(2*u-1):0; }

/* ---- the lattice ---------------------------------------------------------
   (1+b) y_i^{n+1} = (b-1) y_i^{n-1} + 2(1-a^2) y_i^n + a^2 (y_{i+1}^n + y_{i-1}^n)
   ends: fixed y_N = 0; loose y_N = y_{N-1}; none y_N^{n+1} = y_{N-1}^n.  PhET
   re-asserts the end on the current level before each update (it matters only
   the step after the end type is switched) and sets it on the new one after. */
function makeLat(n){ return {n,prev:new Float64Array(n+1),cur:new Float64Array(n+1),nxt:new Float64Array(n+1),steps:0}; }
function latClear(L){ L.prev.fill(0); L.cur.fill(0); L.nxt.fill(0); L.steps=0; }
function latStep(L,a,b,end,yl){
  const n=L.n, P=L.prev, C=L.cur, X=L.nxt;
  if(end==='fixed') C[n]=0; else if(end==='loose') C[n]=C[n-1]; else C[n]=P[n-1];
  const a2=a*a, c=2*(1-a2), inv=1/(1+b);
  for(let i=1;i<n;i++) X[i]=inv*((b-1)*P[i]+c*C[i]+a2*(C[i+1]+C[i-1]));
  X[0]=yl;
  if(end==='fixed') X[n]=0; else if(end==='loose') X[n]=X[n-1]; else X[n]=C[n-1];
  L.prev=C; L.cur=X; L.nxt=P; L.steps++;
}

/* ---- d'Alembert with images: the lattice at a = 1, b = 0 IS this, sampled ----
   A pulse f(t) fed in at x = 0 travels right; the fixed end sends it back
   inverted, the loose end upright (about L' = 59.5 dx), and the driven left
   end sends every returning wave back inverted.  Returns the incident and the
   reflected parts separately so the view can draw both. */
function imageParts(end,A,w,v,t,x){
  const f=tau=>A*tri(tau/w);
  if(end==='none') return {inc:f(t-x/v),ref:0};
  const Lr=end==='fixed'?LSTR:LLOOSE, sr=end==='fixed'?-1:1;
  if(x>Lr) x=2*Lr-x;                         /* the ring bead copies its neighbour */
  let inc=0, ref=0, rt=1;
  for(let m=0;m<100000;m++){
    const t1=t-(2*m*Lr+x)/v;
    if(t1<=0) break;
    inc+=rt*f(t1); ref+=rt*sr*f(t-(2*(m+1)*Lr-x)/v);
    rt*=-sr;
  }
  return {inc,ref};
}
function imageSeries(end,A,w,v,t,x){ const p=imageParts(end,A,w,v,t,x); return p.inc+p.ref; }

/* ---- the lattice dispersion relation ----------------------------------------
   y ~ z^n e^{i k x}:  (1+b) z^2 - 2(1 - 2a^2 sin^2(k dx/2)) z + (1-b) = 0,
   |z| = sqrt((1-b)/(1+b)) and cos(omega dt) = (1 - 2a^2 sin^2(k dx/2))/sqrt(1-b^2).
   kap = k dx (rad per bead); theta = omega dt (rad per step); omega dx/v = theta/a. */
function thetaOf(kap,a,b){
  const s=Math.sin(kap/2), c=(1-2*a*a*s*s)/Math.sqrt(1-b*b);
  return Math.acos(clamp(c,-1,1));
}
function omegaNorm(kap,a,b){ return thetaOf(kap,a,b)/a; }          /* omega dx / v */
function vpOverV(kap,a,b){ return omegaNorm(kap,a,b)/kap; }
/* d theta/d kap from differentiating cos(theta) = c(kap)/sqrt(1-b^2):
   v_g/v = a sin(kap) / (sqrt(1-b^2) sin(theta)); NaN where theta is pinned (overdamped) */
function vgOverV(kap,a,b){
  const th=thetaOf(kap,a,b), s=Math.sin(th);
  if(!(s>1e-12)) return NaN;
  return a*Math.sin(kap)/(Math.sqrt(1-b*b)*s);
}
/* a real bead-and-spring chain (continuous time): omega = (2v/dx) sin(k dx/2) — the a -> 0 limit */
function chainOmegaNorm(kap){ return 2*Math.sin(kap/2); }
function chainVgOverV(kap){ return Math.cos(kap/2); }
/* long waves are overdamped below k dx = asin(b) (a = 1) */
function cutoffKap(b){ return Math.asin(Math.min(1,b)); }

/* ---- small complex arithmetic ([re, im]) ---- */
const cadd=(a,b)=>[a[0]+b[0],a[1]+b[1]];
const csub=(a,b)=>[a[0]-b[0],a[1]-b[1]];
const cmul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]];
const cdiv=(a,b)=>{ const d=b[0]*b[0]+b[1]*b[1]; return [(a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d]; };
const cabs=a=>Math.hypot(a[0],a[1]);
/* principal square root without cancellation (re from im when re < 0) */
function csqrt(a){
  const r=cabs(a); if(r===0) return [0,0];
  if(a[0]>=0){ const re=Math.sqrt((r+a[0])/2); return [re,a[1]/(2*re)]; }
  const t=Math.sqrt((r-a[0])/2), im=a[1]<0?-t:t; return [a[1]/(2*im),im];
}

/* ---- the driven steady state --------------------------------------------------
   The oscillator makes y_0^n = A sin(phi_n), phi_n = n theta, theta = 2 pi f dt.
   Then y_i^n = Im(Y_i e^{i phi_n}) with Y_{i+1} + Y_{i-1} = 2C Y_i,
   C = cos(theta) + i b sin(theta)   [from (1+b) z + (1-b)/z, z = e^{i theta}].
   Route 1 (closed form): Y_i = p lam^i + q lam^{N-i}, lam the root of
   lam^2 - 2C lam + 1 = 0 inside the unit circle, p and q from Y_0 = A and the end.
   Route 2: the same tridiagonal system solved directly (Thomas).                  */
function steadyTheta(f,T){ return TAU*f*dtOf(T); }
function steadyClosed(f,A,b,T,end,n){
  n=n||NSEG;
  const th=steadyTheta(f,T);
  if(!(th>1e-12)) return dcProfile(A,end,n);
  const C=[Math.cos(th),b*Math.sin(th)], z=[Math.cos(th),Math.sin(th)];
  let lam=csub(C,csqrt(csub(cmul(C,C),[1,0])));
  if(cabs(lam)>1) lam=cdiv([1,0],lam);
  const pw=[[1,0]]; for(let i=1;i<=n;i++) pw.push(cmul(pw[i-1],lam));
  const r0=[[1,0],pw[n]];
  let r1;
  if(end==='fixed') r1=[pw[n],[1,0]];
  else if(end==='loose') r1=[csub(pw[n],pw[n-1]),csub([1,0],pw[1])];
  else r1=[csub(cmul(z,pw[n]),pw[n-1]),csub(z,pw[1])];
  const det=csub(cmul(r0[0],r1[1]),cmul(r0[1],r1[0]));
  const p=cdiv(cmul([A,0],r1[1]),det), q=cdiv(cmul([-A,0],r1[0]),det);
  const Y=[]; for(let i=0;i<=n;i++) Y.push(cadd(cmul(p,pw[i]),cmul(q,pw[n-i])));
  return {Y,lam,p,q,z,th,dc:false};
}
function dcProfile(A,end,n){
  const Y=[]; for(let i=0;i<=n;i++) Y.push([end==='fixed'?A*(n-i)/n:A,0]);
  return {Y,lam:[1,0],p:[A,0],q:[0,0],z:[1,0],th:0,dc:true};
}
function steadyThomas(f,A,b,T,end,n){
  n=n||NSEG;
  const th=steadyTheta(f,T);
  if(!(th>1e-12)) return dcProfile(A,end,n).Y;
  const C=[Math.cos(th),b*Math.sin(th)], z=[Math.cos(th),Math.sin(th)];
  const cp=new Array(n+1), dp=new Array(n+1);
  cp[0]=[0,0]; dp[0]=[A,0];                                   /* row 0: Y_0 = A */
  for(let i=1;i<=n;i++){
    let ai, bi, ci=[0,0];
    if(i<n){ ai=[1,0]; bi=[-2*C[0],-2*C[1]]; ci=[1,0]; }
    else if(end==='fixed'){ ai=[0,0]; bi=[1,0]; }
    else if(end==='loose'){ ai=[-1,0]; bi=[1,0]; }
    else { ai=[-1,0]; bi=z; }
    const m=csub(bi,cmul(ai,cp[i-1]));
    cp[i]=cdiv(ci,m); dp[i]=cdiv(csub([0,0],cmul(ai,dp[i-1])),m);
  }
  const Y=new Array(n+1); Y[n]=dp[n];
  for(let i=n-1;i>=0;i--) Y[i]=csub(dp[i],cmul(cp[i],Y[i+1]));
  return Y;
}
function steadyMax(S){ let m=0; for(const y of S.Y) m=Math.max(m,cabs(y)); return m; }
/* the undamped resonances: fixed f_n = n v/(2L), loose f_n = (2n-1) v/(4L'), none: none */
function resonances(end,T,fmax){
  const v=speedOf(T), out=[];
  if(end==='fixed') for(let n=1;n*v/(2*LSTR)<=fmax;n++) out.push(n*v/(2*LSTR));
  else if(end==='loose') for(let n=1;(2*n-1)*v/(4*LLOOSE)<=fmax;n++) out.push((2*n-1)*v/(4*LLOOSE));
  return out;
}
/* what the no-end absorber sends back at bead N: q/(p lam^N) = (z lam - 1)/(lam (lam - z)),
   zero at b = 0 (lam = e^{-i theta}); about b/(2 sin theta) for small b */
function noEndReflection(f,b,T){
  const th=steadyTheta(f,T); if(!(th>1e-12)) return 1;
  const C=[Math.cos(th),b*Math.sin(th)], z=[Math.cos(th),Math.sin(th)];
  let lam=csub(C,csqrt(csub(cmul(C,C),[1,0])));
  if(cabs(lam)>1) lam=cdiv([1,0],lam);
  return cabs(cdiv(csub(cmul(z,lam),[1,0]),cmul(lam,csub(lam,z))));
}

/* ---- a triangle pulse on a LONG lattice at Courant number a (the dispersion view) ----
   driven at bead 0 from t = 0, run until the exact pulse centre reaches xcen;
   160 beads: at a <= 1 nothing on the lattice outruns the front (v_g <= v). */
const LONG_N=160;
function longPulse(a,b,A,w,T,xcen){
  const v=speedOf(T), dt=a*DX/v, tstop=xcen/v+w/2;
  const ns=Math.floor(tstop/dt+1e-9), L=makeLat(LONG_N);
  for(let k=1;k<=ns;k++) latStep(L,a,b,'none',A*tri(k*dt/w));
  return {y:Array.from(L.cur),t:ns*dt,steps:ns,dt};
}
