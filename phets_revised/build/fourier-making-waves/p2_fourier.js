
/* ================================================================== *
 *  the mathematics.  PhET's constants are marked "PhET's value" and   *
 *  every one of them is READ OUT of docs/phets/fourier-making-waves_  *
 *  en.html by build/fourier-making-waves/derive.py, which also        *
 *  re-derives every closed form below from the waveform it belongs    *
 *  to.  Nothing here is a coefficient typed from memory.              *
 * ================================================================== */

/* ---- PhET's values (build 1.1.5) ---------------------------------- */
const NMAX=11;                 /* MAX_HARMONICS */
const AMAX=1.5;                /* MAX_AMPLITUDE */
const A_STEP=0.05;             /* DISCRETE_AMPLITUDE_STEP */
const G_STEP=0.1;              /* WAVE_GAME_AMPLITUDE_STEP */
const N_LEVELS=5;              /* NUMBER_OF_GAME_LEVELS */
const F1=440;                  /* fundamentalFrequency, Hz */
const LWAVE=1;                 /* fundamentalWavelength, m */
const TPER=1000/F1;            /* fundamentalPeriod, ms */
const K1=TAU/LWAVE;            /* rad/m */
const W1=TAU/TPER;             /* rad/ms */
const NPTS=1000;               /* MAX_POINTS_PER_DATA_SET */

/* the wave-packet screen */
const WP_KMAX=24*PI;           /* waveNumberRange 0 .. 24 pi */
const WP_K0_MIN=9*PI, WP_K0_MAX=15*PI, WP_K0_DEF=12*PI;
const WP_SK_MIN=PI, WP_SK_MAX=4*PI, WP_SK_DEF=3*PI;
const WP_SPACINGS=[0,PI/4,PI/2,PI];      /* 0 = continuous */

/* ---- the presets -------------------------------------------------- *
 * Every one is the textbook Fourier series of a waveform, and derive.py
 * integrates that waveform against sin n u and cos n u to get these back
 * to 2.5e-13 -- including the coefficients of the WRONG parity, which
 * come back zero.  The wave packet is PhET's hard-coded table, which is
 * exp(-(n-c)^2/2 sigma^2) with c = (N+1)/2 and sigma = N/5 to PhET's own
 * printed precision (see the header for its single typo).             */
const PRESETS=[{id:'sinusoid',name:'sinusoid'},{id:'triangle',name:'triangle'},
               {id:'square',name:'square'},{id:'sawtooth',name:'sawtooth'},
               {id:'wavePacket',name:'wave packet'},{id:'custom',name:'custom'}];

function presetAmps(name,series,N){
  const out=[];
  for(let n=1;n<=N;n++){
    if(name==='sinusoid') out.push(n===1?1:0);
    else if(name==='triangle') out.push(n%2===0?0:(series==='sin'
      ? Math.pow(-1,(n-1)/2)*8/(n*n*PI*PI) : 8/(n*n*PI*PI)));
    else if(name==='square') out.push(n%2===0?0:(series==='sin'
      ? 4/(n*PI) : Math.pow(-1,(n-1)/2)*4/(n*PI)));
    else if(name==='sawtooth') out.push(Math.pow(-1,n-1)*2/(n*PI));
    else if(name==='wavePacket'){ const c=(N+1)/2, s=N/5;
      out.push(Math.exp(-(n-c)*(n-c)/(2*s*s))); }
    else out.push(0);
  }
  while(out.length<NMAX) out.push(0);
  return out;
}
/* PhET: a sawtooth cannot be built out of cosines, because it is odd. */
function presetAllowsCos(name){ return name!=='sawtooth'; }

/* the waveform the infinite series converges to, as a function of the
   phase u.  PhET draws these as its "Infinite Harmonics" curve. */
function wrapPi(u){ let v=(u+PI)%TAU; if(v<0) v+=TAU; return v-PI; }
function idealWave(name,series,u){
  const s=Math.sin(u), c=Math.cos(u);
  if(name==='sinusoid') return series==='sin'?s:c;
  if(name==='square')   return series==='sin'?(s>=0?1:-1):(c>=0?1:-1);
  if(name==='triangle') return (2/PI)*Math.asin(clamp(series==='sin'?s:c,-1,1));
  if(name==='sawtooth') return wrapPi(u)/PI;
  return NaN;                                   /* wave packet and custom have none */
}
function hasIdeal(name){ return name==='sinusoid'||name==='square'||name==='triangle'||name==='sawtooth'; }
/* the exact mean square of the complete waveform, <f^2> over a period.
   square: (8/pi^2) sum_odd n^-2 = 1;  triangle: (32/pi^4) sum_odd n^-4 = 1/3;
   sawtooth: (2/pi^2) sum n^-2 = 1/3;  sinusoid: 1/2. */
function idealMeanSquare(name){
  if(name==='sinusoid') return 0.5;
  if(name==='square') return 1;
  if(name==='triangle'||name==='sawtooth') return 1/3;
  return NaN;
}

/* ---- the series --------------------------------------------------- *
 * PhET's three domains are one function of one phase:
 *   space          u = 2 pi x / L
 *   time           u = 2 pi t / T
 *   space & time   u = 2 pi (x/L - t/T)
 * so a harmonic is always A_n sin(n u) or A_n cos(n u).                */
const DOMAINS=[{id:'space',name:'space (x)'},{id:'time',name:'time (t)'},
               {id:'both',name:'space & time'}];
function phaseOf(domain,x,t){
  if(domain==='time') return W1*t;
  if(domain==='both') return K1*x-W1*t;
  return K1*x;
}
/* the phase at abscissa s of the axis the view DRAWS.  In the time domain that
   abscissa is t, not x, and passing it as x is a bug that draws a flat line:
   phaseOf('time', s, t) ignores s entirely.  Found by looking at the PNG. */
function phaseAt(domain,s,t){ return domain==='time'?phaseOf(domain,0,s):phaseOf(domain,s,t); }
function trigOf(series,a){ return series==='sin'?Math.sin(a):Math.cos(a); }
function harmonicValue(A,n,u,series){ return A*trigOf(series,n*u); }
function seriesSum(amps,u,series,N){
  const M=N===undefined?amps.length:N;
  let s=0;
  for(let n=1;n<=M;n++){ const a=amps[n-1]; if(a!==0) s+=a*trigOf(series,n*u); }
  return s;
}
/* Parseval: the mean square of the sum over one period is (1/2) sum A_n^2,
   whatever the amplitudes and whichever series -- because sin n u and
   cos n u are orthogonal with mean square 1/2.  Asserted against
   quadrature of the square of the sum, both in derive.py and in JS. */
function parseval(amps,N){
  const M=N===undefined?amps.length:N;
  let s=0; for(let n=1;n<=M;n++) s+=amps[n-1]*amps[n-1];
  return 0.5*s;
}
/* the same thing the hard way: the mean of f^2 by the trapezium rule on
   a grid of ns points.  Exact for a trigonometric polynomial once
   ns > 2 * (the highest harmonic present), which is why selfTest asserts
   it agrees with parseval() to 1e-14 and NOT merely to a tolerance. */
function meanSquareNumeric(amps,series,ns,N){
  let s=0;
  for(let j=0;j<ns;j++){ const v=seriesSum(amps,TAU*j/ns,series,N); s+=v*v; }
  return s/ns;
}

/* ---- truncation --------------------------------------------------- *
 * ||f - S_N||^2 = <f^2> - (1/2) sum_{n<=N} A_n^2.  Exact, and far better
 * than summing the tail: the square wave's tail converges like 1/N.    */
function truncationRms(name,series,N){
  const A=presetAmps(name,series,N);
  let s=0; for(let n=1;n<=N;n++) s+=A[n-1]*A[n-1];
  return Math.sqrt(Math.max(0,idealMeanSquare(name)-0.5*s));
}

/* ---- Gibbs -------------------------------------------------------- *
 * S_M'(u) = (8/2pi) sin(2 M u)/sin u for the M-term square wave, so the
 * first maximum is at u = pi/(2M) exactly, and there
 *   S_M = sum_{m=1..M} 4/(pi(2m-1)) sin((2m-1) pi / 2M)
 * which is the Riemann sum of (2/pi) int_0^pi sinc, i.e. (2/pi) Si(pi).  */
const GIBBS_PEAK=1.1789797444721672;        /* (2/pi) Si(pi)  (derive, scipy.special.sici) */
const GIBBS_FRACTION=0.08948987223608362;   /* (peak - 1) / 2: the Wilbraham-Gibbs constant */
function squarePeakClosed(M){
  const u=PI/(2*M); let s=0;
  for(let m=1;m<=M;m++) s+=4/(PI*(2*m-1))*Math.sin((2*m-1)*u);
  return {u,val:s};
}
/* keeping harmonics 1..N of a square or triangle keeps ceil(N/2) ODD ones,
   and it is the odd count the Gibbs closed form is written in */
function oddCount(N){ return Math.ceil(N/2); }
/* where to look for the overshoot: next to the jump, not over the whole half
   period.  A square wave's partial sum is symmetric about u = pi/2 (only odd
   harmonics survive u -> pi - u), so a global scan finds the MIRROR of the
   first ear as often as the ear, with the same height and the wrong position. */
function peakWindow(name){
  if(name==='square') return [1e-9,PI/2];
  if(name==='sawtooth') return [PI/2,PI-1e-9];
  return [0,PI];                               /* continuous: the plain maximum */
}
/* the measured peak: a grid scan then one parabola refinement.  This is
   the only quantity in the file read off a curve, and selfTest bounds its
   grid error against the closed form above. */
function peakOf(fn,uLo,uHi,ns){
  let bi=0,bv=-Infinity;
  const us=[],vs=[];
  for(let j=0;j<=ns;j++){ const u=uLo+(uHi-uLo)*j/ns, v=fn(u); us.push(u); vs.push(v);
    if(v>bv){ bv=v; bi=j; } }
  if(bi<=0||bi>=ns) return {u:us[bi],val:vs[bi]};
  const y0=vs[bi-1],y1=vs[bi],y2=vs[bi+1], den=y0-2*y1+y2;
  const d=den!==0?0.5*(y0-y2)/den:0;
  const du=(uHi-uLo)/ns;
  return {u:us[bi]+d*du, val:y1-0.25*(y0-y2)*d};
}

/* ---- analysis: the amplitudes come back out ----------------------- *
 * A_n = (2/ns) sum_j f(u_j) sin(n u_j) -- the discrete projection, exact
 * for a trigonometric polynomial of degree < ns/2.  Implemented twice:
 * a direct O(N ns) sum and a radix-2 FFT, asserted equal to 1e-14.      */
function analyseDirect(y,N,series){
  const ns=y.length, out=[];
  for(let n=1;n<=N;n++){
    let s=0;
    for(let j=0;j<ns;j++) s+=y[j]*trigOf(series,n*TAU*j/ns);
    out.push(2*s/ns);
  }
  return out;
}
/* in-place radix-2 Cooley-Tukey, decimation in time.  n must be a power
   of two; fftRadix2 throws otherwise rather than returning nonsense. */
function fftRadix2(re,im){
  const n=re.length;
  if(n!==im.length||n<2||(n&(n-1))!==0) throw new Error('fftRadix2: length must be a power of two');
  for(let i=1,j=0;i<n;i++){
    let bit=n>>1;
    for(;j&bit;bit>>=1) j^=bit;
    j^=bit;
    if(i<j){ let t=re[i]; re[i]=re[j]; re[j]=t; t=im[i]; im[i]=im[j]; im[j]=t; }
  }
  for(let len=2;len<=n;len<<=1){
    const ang=-TAU/len, wr=Math.cos(ang), wi=Math.sin(ang);
    for(let i=0;i<n;i+=len){
      let cr=1,ci=0;
      for(let k=0;k<len/2;k++){
        const ur=re[i+k], ui=im[i+k];
        const vr=re[i+k+len/2]*cr-im[i+k+len/2]*ci;
        const vi=re[i+k+len/2]*ci+im[i+k+len/2]*cr;
        re[i+k]=ur+vr; im[i+k]=ui+vi;
        re[i+k+len/2]=ur-vr; im[i+k+len/2]=ui-vi;
        const nr=cr*wr-ci*wi; ci=cr*wi+ci*wr; cr=nr;
      }
    }
  }
}
function analyseFFT(y,N,series){
  const ns=y.length, re=Array.from(y), im=new Array(ns).fill(0);
  fftRadix2(re,im);
  const out=[];
  for(let n=1;n<=N;n++) out.push(series==='sin'?-2*im[n]/ns:2*re[n]/ns);
  return out;
}
/* sample one period of a series, for the analysis to chew on */
function sampleSeries(amps,series,ns,N){
  const y=new Array(ns);
  for(let j=0;j<ns;j++) y[j]=seriesSum(amps,TAU*j/ns,series,N);
  return y;
}

/* ---- the wave packet ---------------------------------------------- *
 * A(k) = exp(-(k-k0)^2 / 2 sigma_k^2) / (sigma_k sqrt(2 pi))           *
 * F(x) = int A(k) cos(k x) dk = exp(-sigma_k^2 x^2 / 2) cos(k0 x)      *
 * so sigma_x sigma_k = 1 exactly and the envelope is 1/sqrt(e) at      *
 * x = sigma_x.  PhET's discrete packet sums A(n k1) k1 cos(n k1 x) for *
 * n k1 <= 24 pi, which by Poisson summation is the continuous packet   *
 * repeated every lambda1 = 2 pi / k1, less a Gaussian tail.            */
function wpAmp(k,k0,sk){ return Math.exp(-(k-k0)*(k-k0)/(2*sk*sk))/(sk*Math.sqrt(TAU)); }
function wpComponentCount(k1){ return k1>0?Math.floor(WP_KMAX/k1)+1:Infinity; }
function wpComponents(k1,k0,sk){
  const out=[];
  if(!(k1>0)) return out;
  const n=wpComponentCount(k1);
  for(let j=0;j<n;j++){ const k=j*k1; out.push({k,a:wpAmp(k,k0,sk)*k1,n:j}); }
  return out;
}
function wpContinuous(x,k0,sk,series){
  const e=Math.exp(-sk*sk*x*x/2);
  return e*trigOf(series,k0*x);
}
function wpDiscrete(x,comps,series){
  let s=0;
  for(let i=0;i<comps.length;i++) s+=comps[i].a*trigOf(series,comps[i].k*x);
  return s;
}
/* the envelope: the magnitude of the analytic signal, sqrt(cos-sum^2 +
   sin-sum^2).  For the continuous packet that is exp(-x^2/2 sigma_x^2)
   exactly; PhET builds the discrete one the same way. */
function wpEnvelopeDiscrete(x,comps){
  const c=wpDiscrete(x,comps,'cos'), s=wpDiscrete(x,comps,'sin');
  return Math.sqrt(c*c+s*s);
}
function wpEnvelopeContinuous(x,sk){ return Math.exp(-sk*sk*x*x/2); }
/* Poisson: sum over ALL n in Z of k1 A(n k1) trig(n k1 x) equals the sum
   of copies of the continuous packet at x - m lambda1.  mCopies copies
   either side is enough once they are Gaussian-small. */
function wpPeriodised(x,k1,k0,sk,series,mCopies){
  const lam=TAU/k1, mm=mCopies===undefined?6:mCopies;
  let s=0;
  for(let m=-mm;m<=mm;m++) s+=wpContinuous(x-m*lam,k0,sk,series);
  return s;
}
/* the two-sided discrete sum, which is what Poisson's identity is about:
   PhET keeps only n >= 0 and n k1 <= 24 pi, and the difference is the
   Gaussian tail below k = 0 and above k = 24 pi. */
function wpDiscreteTwoSided(x,k1,k0,sk,series,nExtra){
  const nx=nExtra===undefined?Math.ceil(12*sk/k1)+2:nExtra;
  const n1=wpComponentCount(k1);
  let s=0;
  for(let j=-nx;j<n1+nx;j++){
    const k=j*k1;
    s+=wpAmp(k,k0,sk)*k1*trigOf(series,k*x);
  }
  return s;
}
/* erfc, Numerical Recipes' Chebyshev form: |error| < 1.2e-7 relative,
   which is ample for a bound that is itself 3e-5.  Used ONLY for the
   printed truncation bound. */
function erfcApprox(x){
  const z=Math.abs(x), t=1/(1+z/2);
  const ans=t*Math.exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+
    t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+
    t*(-0.82215223+t*0.17087277)))))))));
  return x>=0?ans:2-ans;
}
function wpTailBound(k0,sk){
  return 0.5*erfcApprox(k0/(sk*Math.SQRT2))+0.5*erfcApprox((WP_KMAX-k0)/(sk*Math.SQRT2));
}

/* ---- the wave game ------------------------------------------------ *
 * PhET: level n asks for n non-zero harmonics out of eleven (level 5 for
 * a random 5..11); each non-zero amplitude is a multiple of 0.1 in
 * [-1.5, 1.5], zero excluded; a challenge that repeats the previous
 * answer is redrawn, up to ten times.  A guess is right when every
 * amplitude matches exactly.                                          */
const GAME_CONTROLS=[2,3,5,6,NMAX];         /* PhET's defaultNumberOfAmplitudeControls */
/* a small deterministic generator, so a challenge can be reproduced from
   its seed and selfTest can pin one */
function makeRng(seed){
  let s=(seed>>>0)||1;
  return function(){ s^=s<<13; s>>>=0; s^=s>>>17; s^=s<<5; s>>>=0; return s/4294967296; };
}
function gameHarmonicCount(level,rnd){
  return level<N_LEVELS?level:5+Math.floor(rnd()*(NMAX-5+1));
}
function gameAmplitudes(level,seed){
  const rnd=makeRng(seed), amps=new Array(NMAX).fill(0);
  const pool=[]; for(let i=0;i<NMAX;i++) pool.push(i);
  const want=gameHarmonicCount(level,rnd);
  for(let c=0;c<want;c++){
    const i=Math.floor(rnd()*pool.length), slot=pool[i];
    pool.splice(i,1);
    /* PhET: uniform in [-1.5, 0), snapped to the 0.1 step, never zero,
       then a random sign */
    let a=-AMAX*rnd();
    a=Math.round(a/G_STEP)*G_STEP;
    if(a===0) a=-G_STEP;
    if(rnd()<0.5) a=-a;
    amps[slot]=+a.toFixed(10);
  }
  return amps;
}
function gameMatches(guess,answer){
  for(let i=0;i<NMAX;i++) if(Math.abs(guess[i]-answer[i])>0) return false;
  return true;
}
function nonZeroCount(amps){ let c=0; for(let i=0;i<amps.length;i++) if(amps[i]!==0) c++; return c; }

/* snap an amplitude to PhET's step and range */
function snapAmp(a,step){ return clamp(Math.round(a/step)*step,-AMAX,AMAX); }
