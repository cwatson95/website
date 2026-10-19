
/* ================================================================== *
 *  WAVES INTRO's own layer on the wave-interference engine: PhET's    *
 *  wave-generator button, PhET's light screen, the steady-state       *
 *  measurement of the wavelength along the axis, and PhET's tone.     *
 *  No DOM.  Twin: derive.py, which repeats every operation below in   *
 *  the same order (refvals.txt).                                      *
 * ================================================================== */

/* ---- PhET's green button (WaveGeneratorNode + Scene.handleButton1Toggled) ----
   Continuous: the button switches the source on and off, and switching it on
   restarts the phase (PhET's resetPhase; the engine's runSetSource does it
   because no other source is running).  Pulse: the button fires one period and
   is dead until that pulse finishes, when PhET's pulseFiringProperty link pops
   it back up.  Changing the disturbance type stops everything (PhET's
   disturbanceTypeProperty link) — in pulse mode the source cell stays armed so
   that a pulse can be written into it. */
function sourceActive(R){ return R.cont?R.src[0]:R.pulse.on; }
function pressSource(R){
  if(R.cont){ runSetSource(R,0,!R.src[0]); return true; }
  if(R.pulse.on) return false;
  return firePulse(R);
}
function runSetWave(R,cont){
  if(R.cont===cont) return false;
  R.cont=cont; R.pulse.on=false; R.pulse.phi=0; R.src[0]=!cont;
  return true;
}

/* ---- PhET's light screen, as Waves Intro 1.1.24 draws it --------------------
   The screen shows the mean square of the lattice's last visible column over a
   history window (the engine's screenIntensity: the whole number of periods
   nearest PhET's 90 steps).  PhET then smooths it over three rows
   (IntensitySample.getIntensityValues), averages each row over the rows within
   +/-(SCREEN_AVG - 1) of it (LightScreenNode, lightScreenAveragingWindowSize
   40 in Waves Intro against 3 in Wave Interference), and maps the result to
   brightness through its piecewise-linear table (piecewiseLinearBrightness
   true).  Every number here is PhET's, read from the minified original. */
const SCREEN_AVG=40;
const PHET_BRIGHT=[0,0, 0.002237089269640335,0.4, 0.008937089269640335,0.5, 0.05372277438413573,0.64,
                   0.13422634397144692,0.74, 0.2096934692889395,0.8, 1,1];
function phetBrightness(u){
  const T=PHET_BRIGHT;
  let b;
  if(u<=T[0]) b=T[1];
  else if(u>=T[T.length-2]) b=T[T.length-1];
  else { let i=0; while(u>T[i+2]) i+=2;
    b=T[i+1]+(T[i+3]-T[i+1])*(u-T[i])/(T[i+2]-T[i]); }
  return clamp(b,0,1);
}
function smooth3(I){
  const n=I.length, out=new Float64Array(n);
  out[0]=(I[0]+I[1])/2; out[n-1]=(I[n-1]+I[n-2])/2;
  for(let r=1;r<n-1;r++) out[r]=(I[r-1]+I[r]+I[r+1])/3;
  return out;
}
function screenAverage(I,a){
  const n=I.length, out=new Float64Array(n);
  for(let r=0;r<n;r++){
    let s=I[r], c=1;
    for(let d=1;d<a;d++){
      if(r+d<n){ s+=I[r+d]; c++; }
      if(r-d>=0){ s+=I[r-d]; c++; }
    }
    out[r]=s/c;
  }
  return out;
}
function screenBright(I){
  const sm=screenAverage(smooth3(I),SCREEN_AVG), out=new Float64Array(sm.length);
  for(let r=0;r<sm.length;r++) out[r]=phetBrightness(sm[r]);
  return out;
}
/* what one source ought to put on the screen: a hard source radiates the same
   way in every direction, so in two dimensions the time-averaged intensity
   falls as 1/r.  Normalised to its peak, like the measured profile. */
function screenTheory1(R){
  const L=R.lat, S=SCENES[R.scene], dx=sceneDx(S), mid=(L.ny-1)/2, col=L.nx-L.pad-1, rows=L.ny-2*L.pad;
  const X=(col-srcCol(L))*dx, out=new Float64Array(rows);
  let mx=0;
  for(let r=0;r<rows;r++){ const y=(L.pad+r-mid)*dx; out[r]=1/Math.hypot(X,y); if(out[r]>mx) mx=out[r]; }
  for(let r=0;r<rows;r++) out[r]/=mx;
  return out;
}

/* ---- the steady state along the axis ---------------------------------------
   A fresh run of one medium at frequency f with the source on from the first
   step.  After MEAS.N0 steps the front has crossed the tank twice; MEAS.PER
   whole periods are then recorded along the centre row, and at every cell the
   record is fitted by least squares to

        u(n) = a sin(phi_n) + b cos(phi_n) + c + d (n - nbar)

   against the drive's own phase phi_n, so that the amplitude is hypot(a, b)
   and the phase atan2(b, a).  The constant and the drift are there to absorb
   the wake of the switch-on, which in two dimensions decays only as 1/(omega t).
   The wavelength is the slope of the unwrapped phase over cells MEAS.R0 to
   MEAS.R1 from the source, and the envelope's power is the slope of log
   amplitude against log r over the same cells (1/sqrt(r) in two dimensions).
   Amplitude MEAS.A: the scheme is linear, so the wavelength does not depend on
   it and the drawn snapshot is simply scaled. */
const MEAS={N0:400, PER:2, R0:30, R1:100, A:8};
const MEAS_CACHE=[];
function measureWave(sceneId,f){
  const key=sceneId+'|'+f;
  for(const e of MEAS_CACHE) if(e.key===key) return e.val;
  const val=measureCompute(sceneId,f);
  MEAS_CACHE.unshift({key,val});
  if(MEAS_CACHE.length>9) MEAS_CACHE.pop();
  return val;
}
/* Gaussian elimination with partial pivoting on the 4 x 4 normal equations
   (the same order as derive.py's, so the two agree to rounding) */
function solve4(Nm,rhs){
  const A=[];
  for(let i=0;i<4;i++) A.push([Nm[i][0],Nm[i][1],Nm[i][2],Nm[i][3],rhs[i]]);
  for(let col=0;col<4;col++){
    let piv=col;
    for(let r=col+1;r<4;r++) if(Math.abs(A[r][col])>Math.abs(A[piv][col])) piv=r;
    if(piv!==col){ const t=A[col]; A[col]=A[piv]; A[piv]=t; }
    for(let r=col+1;r<4;r++){
      const fct=A[r][col]/A[col][col];
      for(let c=col;c<5;c++) A[r][c]-=fct*A[col][c];
    }
  }
  const x=[0,0,0,0];
  for(let r=3;r>=0;r--){
    let s=A[r][4];
    for(let c=r+1;c<4;c++) s-=A[r][c]*x[c];
    x[r]=s/A[r][r];
  }
  return x;
}
/* unwrap a sequence of angles: each step is brought into (-pi, pi] by whole turns.  Lifted out
   of the measurement so that BOTH branches can be tested: the wave here travels outward, so its
   phase only ever falls and only the first branch is reached — a mutant on the second survived
   a sweep while it sat inline (Known-bad: a quantity that only one code path reaches is covered
   by nothing, however many assertions surround it). */
function unwrapPhase(ph){
  const n=ph.length, out=new Float64Array(n);
  out[0]=ph[0];
  for(let c=1;c<n;c++){
    let d=ph[c]-ph[c-1];
    while(d>PI) d-=TAU;
    while(d<-PI) d+=TAU;
    out[c]=out[c-1]+d;
  }
  return out;
}
function lineSlope(xs,ys,i0,i1){
  let n=0, sx=0, sy=0;
  for(let i=i0;i<=i1;i++){ n++; sx+=xs[i]; sy+=ys[i]; }
  const xb=sx/n, yb=sy/n;
  let num=0, den=0;
  for(let i=i0;i<=i1;i++){ num+=(xs[i]-xb)*(ys[i]-yb); den+=(xs[i]-xb)*(xs[i]-xb); }
  return num/den;
}
function measureCompute(sceneId,f){
  const R=makeRun(sceneId,'point',1);
  runSetFrequency(R,f,true);
  R.A=MEAS.A;
  for(let s=0;s<MEAS.N0;s++) runStep(R);
  const L=R.lat, ci=srcCol(L), nc=L.nx-L.pad-ci, mid=(L.ny-1)/2, off=mid*L.nx+ci;
  const M=Math.ceil(MEAS.PER*TAU/R.Om);
  const Nm=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], rhs=[];
  for(let i=0;i<4;i++) rhs.push(new Float64Array(nc));
  for(let q=0;q<M;q++){
    runStep(R);
    const u=R.lat.u, tq=q-(M-1)/2, b=[Math.sin(R.phi),Math.cos(R.phi),1,tq];
    for(let i=0;i<4;i++){
      for(let j=0;j<4;j++) Nm[i][j]+=b[i]*b[j];
      const bi=b[i], ri=rhs[i];
      for(let c=0;c<nc;c++) ri[c]+=bi*u[off+c];
    }
  }
  const amp=new Float64Array(nc), ph=new Float64Array(nc), rs=new Float64Array(nc),
        la=new Float64Array(nc), lr=new Float64Array(nc), snap=new Float64Array(nc);
  for(let c=0;c<nc;c++){
    const x=solve4(Nm,[rhs[0][c],rhs[1][c],rhs[2][c],rhs[3][c]]);
    amp[c]=Math.hypot(x[0],x[1]); ph[c]=Math.atan2(x[1],x[0]);
    rs[c]=c; lr[c]=Math.log(c); la[c]=Math.log(amp[c]); snap[c]=R.lat.u[off+c];
  }
  const un=unwrapPhase(ph);
  const lamCells=TAU/(-lineSlope(rs,un,MEAS.R0,MEAS.R1)), pexp=lineSlope(lr,la,MEAS.R0,MEAS.R1);
  let sa=0;
  for(let c=MEAS.R0;c<=MEAS.R1;c++) sa+=amp[c]*Math.sqrt(c);
  const S=SCENES[sceneId];
  return {scene:sceneId, f, M, nc, amp, ph, un, snap, Nl:R.Nl, lamCells, pexp,
          afit:sa/(MEAS.R1-MEAS.R0+1), lam:lamCells*sceneDx(S), lam0:waveLen(S,f),
          err:lamCells/R.Nl-1, dx:sceneDx(S), dt:R.dt, steps:R.n};
}

/* ---- PhET's tone (SineWaveGenerator) ---------------------------------------
   PhET plays a sine at 1000 x the sound scene's frequency (which is per
   millisecond, so 220-440 Hz) at an output level that runs linearly from 0 to
   0.3 over the amplitude range 0 to 10, and only while the tone is switched on,
   the source button is down and the clock is running.  The samples are computed
   here rather than taken from an OscillatorNode, so the suite can check them:
   the buffer holds a whole number of cycles and therefore loops seamlessly, at
   a frequency within one part in 10^4 of the one asked for. */
const TONE_SR=44100, TONE_SECONDS=0.5;
function toneParams(R){ return {hz:1000*R.f, level:0.3*R.A/10}; }
function toneBuffer(hz,level,sr){
  const m=Math.max(1,Math.round(hz*TONE_SECONDS)), L=Math.round(m*sr/hz), data=new Float32Array(L);
  for(let i=0;i<L;i++) data[i]=level*Math.sin(TAU*m*i/L);
  return {data, m, L, hz:m*sr/L};
}
