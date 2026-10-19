
/* ================================================================== *
 *  THE ENGINE — the scalar wave equation on PhET's 2-D lattice, one   *
 *  hard point source, and the calibration to physical units.  No DOM. *
 * ================================================================== */
/* PROVENANCE.  The lattice core here — makeLattice / latStep / murEdge / murCorner,
   latOmega / latK / latPhaseSpeed / latGroupSpeed / murReflection, and the idea of
   SOLVING the time step from the lattice's own dispersion relation — is copied from
   build/wave-interference/p2_engine.js (SHA-256 393cdd8f1d6067a960b7c85726876c78ee
   fa604ba6e7802f243dfab630b1dc66), whose API is that build's ENGINE.md and whose
   proof is its derive.py.  Two things are different here, and both are re-derived
   from scratch in build/sound-waves/derive.py:
     (1) the lattice is 231 x 231 with PhET's 20-cell pad (191 visible) rather than
         PhET's 151 / 111, because on PhET's own lattice this sim's top frequency,
         1000 Hz, has only 3.81 cells per wavelength and PhET's fixed time step
         makes its wavelength 12.8 % short (derive.py, section C);
     (2) the run layer is new: SI units, PhET's Sound Waves geometry, the air
         density on the drive, and no plane wave, no barrier and no screen (Sound
         Waves has none of those, so they are not carried over).
   derive.py ALSO falsifies the stencil independently, by putting an exact lattice
   plane wave through it (residual 5e-15), so nothing here rests only on the copy. */
const LAT={N:231, PAD:20, VIS:191, C:0.5, SRC_OFF:34, AMP_CAL:1.2, VISIT:1e-3};
LAT.C2=LAT.C*LAT.C;
LAT.MID=(LAT.N-1)/2;                      /* 115: the middle row, at exactly y = W/2 */
LAT.SRC_I=LAT.PAD+LAT.SRC_OFF;            /* 54: PhET's speaker, 1.81 m into the 10 m box */
/* Mur's absorbing boundary (G. Mur, IEEE Trans. EMC 23, 377 (1981)), the
   discretisation of the Engquist-Majda one-way equation at C = 1/2:
   MUR1 = (C-1)/(C+1) = -1/3, MUR2A = 2/(C+1) = 4/3, MUR2B = C^2/(2(C+1)) = 1/12. */
const MUR1=(LAT.C-1)/(LAT.C+1), MUR2A=2/(LAT.C+1), MUR2B=LAT.C2/(2*(LAT.C+1));

function makeLattice(nx,ny,pad){
  const n=nx*ny;
  return {nx,ny,pad:(pad===undefined?LAT.PAD:pad),
          u:new Float64Array(n), up:new Float64Array(n), un:new Float64Array(n),
          vis:new Uint8Array(n), steps:0};
}
function latClear(L){ L.u.fill(0); L.up.fill(0); L.un.fill(0); L.vis.fill(0); L.steps=0; }
function latIndex(L,i,j){ return j*L.nx+i; }
/* a read that is ZERO off the lattice — the image source and the second speaker both
   read cells that can lie outside it, and there is no field out there */
function latAt(L,i,j){
  if(i<0||j<0||i>=L.nx||j>=L.ny) return 0;
  return L.u[j*L.nx+i];
}
/* one leapfrog step of u_tt = c^2 lap u on the 5-point stencil:
   u^{n+1} = 2u^n - u^{n-1} + C^2 (u_E + u_W + u_N + u_S - 4u^n)            */
function latStep(L){
  const nx=L.nx, ny=L.ny, u=L.u, up=L.up, un=L.un, vis=L.vis, C2=LAT.C2, V=LAT.VISIT;
  for(let j=1;j<ny-1;j++){
    const r=j*nx;
    for(let i=1;i<nx-1;i++){
      const k=r+i, c=u[k];
      const v=2*c-up[k]+C2*(u[k+1]+u[k-1]+u[k+nx]+u[k-nx]-4*c);
      un[k]=v;
      if(v>V||v<-V) vis[k]=1;
    }
  }
  /* the edges: left and right on rows 1..ny-2 (tangent = y, stride nx), then
     top and bottom on columns 1..nx-2 (tangent = x, stride 1) */
  for(let j=1;j<ny-1;j++){
    const r=j*nx;
    murEdge(un,u,up,r,r+1,nx);
    murEdge(un,u,up,r+nx-1,r+nx-2,nx);
  }
  const b=(ny-1)*nx, b1=(ny-2)*nx;
  for(let i=1;i<nx-1;i++){
    murEdge(un,u,up,i,nx+i,1);
    murEdge(un,u,up,b+i,b1+i,1);
  }
  murCorner(un,u,0,1); murCorner(un,u,nx-1,nx-2); murCorner(un,u,b,b+1); murCorner(un,u,b+nx-1,b+nx-2);
  L.up=u; L.u=un; L.un=up; L.steps++;
}
/* e = the edge cell, i = its inner neighbour, s = the stride along the edge */
function murEdge(un,u,up,e,i,s){
  un[e]=-up[i]+MUR1*(un[i]+up[e])+MUR2A*(u[e]+u[i])
        +MUR2B*(u[e+s]-2*u[e]+u[e-s]+u[i+s]-2*u[i]+u[i-s]);
}
function murCorner(un,u,c,a){ un[c]=u[a]+MUR1*(un[a]-u[c]); }

/* ---- the lattice's dispersion relation (exact for this scheme) ----------
   A mode u ~ exp(i(kx i + ky j - Om n)) solves the update iff
        sin^2(Om/2) = C^2 [ sin^2(kx/2) + sin^2(ky/2) ],
   with Om in radians per step and k in radians per cell.  Stable iff
   2C^2 <= 1 (C <= 1/sqrt 2); PhET's C = 1/2 is inside that. */
function latOmega(kx,ky){
  const s=Math.sin(kx/2), t=Math.sin(ky/2);
  return 2*Math.asin(LAT.C*Math.sqrt(s*s+t*t));
}
/* the wavenumber along direction th that carries the per-step frequency Om:
   bisection on the monotone branch k in (0, pi/max|cos|,|sin|) */
function latK(Om,th){
  const c=Math.cos(th), s=Math.sin(th), want=Math.sin(Om/2);
  let lo=0, hi=PI/Math.max(Math.abs(c),Math.abs(s));
  if(!(latOmega(hi*c,hi*s)>=Om)) return NaN;
  for(let it=0;it<200&&hi-lo>1e-15*hi;it++){
    const m=0.5*(lo+hi), g=LAT.C*Math.sqrt(Math.pow(Math.sin(m*c/2),2)+Math.pow(Math.sin(m*s/2),2));
    if(g<want) lo=m; else hi=m;
  }
  return 0.5*(lo+hi);
}
/* phase and group speed in cells per step; the continuum value is C */
function latPhaseSpeed(k,th){ return latOmega(k*Math.cos(th),k*Math.sin(th))/k; }
function latGroupSpeed(k,th){
  const kx=k*Math.cos(th), ky=k*Math.sin(th), Om=latOmega(kx,ky);
  return LAT.C2*Math.hypot(Math.sin(kx),Math.sin(ky))/Math.sin(Om);
}
/* the exact reflection off the Mur edge for a plane wave (kx, ky) arriving at
   the right-hand edge: a(x) = e^{ikx} + R e^{-ikx}, z = e^{-i Om} per step.
   order 1 or 2.  Complex arithmetic spelled out; returns |R|. */
function murReflection(kx,ky,order){
  const Om=latOmega(kx,ky);
  const zr=Math.cos(Om), zi=-Math.sin(Om);
  const cm=(ar,ai,br,bi)=>[ar*br-ai*bi, ar*bi+ai*br];
  const cd=(ar,ai,br,bi)=>{ const d=br*br+bi*bi; return [(ar*br+ai*bi)/d,(ai*br-ar*bi)/d]; };
  const ekr=Math.cos(kx), eki=Math.sin(kx);                 /* e^{ik}  */
  let P, Q;
  if(order===1){                                           /* a(0)(z+A1) = a(-1)(1+A1 z) */
    P=[zr+MUR1, zi]; Q=[1+MUR1*zr, MUR1*zi];
  } else {                                                 /* a(0)(z - A1/z - B) = a(-1)(-1/z + A1 z + B) */
    const B=MUR2A-MUR2B*(2-2*Math.cos(ky));
    const iz=cd(1,0,zr,zi);
    P=[zr-MUR1*iz[0]-B, zi-MUR1*iz[1]];
    Q=[-iz[0]+MUR1*zr+B, -iz[1]+MUR1*zi];
  }
  /* R = (e^{-ik} Q - P) / (P - e^{ik} Q) */
  const a=cm(ekr,-eki,Q[0],Q[1]), bq=cm(ekr,eki,Q[0],Q[1]);
  const R=cd(a[0]-P[0],a[1]-P[1],P[0]-bq[0],P[1]-bq[1]);
  return Math.hypot(R[0],R[1]);
}

/* ---- the air, in SI.  PhET's model unit is 1 cm (its ruler is 500 model units
   long and reads 0 to 5 m) and its frequency property is per millisecond (its
   slider label is round(1000 f) Hz), so PhET's 1000-unit wave area is 10 m, its
   34.3 cm/ms is 343 m/s and its 0.1-1 frequency range is 100-1000 Hz.  Every
   number below is PhET's, read from the minified original. ---- */
const AIR={W:10, unit:'m', v:343, fmin:100, fmax:1000, f0:550, scaleLen:1,
           ampMax:10, amp0:5, phetVis:111, phetN:151,
           phetTimeScale:0.004837569423218267,   /* s of model time per s of wall time */
           phetEventRate:20*111/61, phetMaxSoundDist:85, phetListenerLambdaK:36};
function sceneDx(){ return AIR.W/LAT.VIS; }
function waveLen(f){ return AIR.v/f; }
function cellsPerWave(f){ return AIR.v/f/sceneDx(); }
/* the calibration: the physical time per step is solved from the dispersion
   relation so that a wave along a lattice axis has EXACTLY the wavelength v/f
   and the period 1/f:  Om = 2 asin(C sin(pi dx/lambda)),  dt = Om/(2 pi f).
   (PhET keeps one dt for the whole sim; see phetLambda.) */
function omegaStep(Nl){ return 2*Math.asin(LAT.C*Math.sin(PI/Nl)); }
function stepDt(f){ return omegaStep(cellsPerWave(f))/(TAU*f); }
/* what PhET's one fixed step makes of frequency f, on PhET's own 111-cell view */
function phetLambda(f){
  const dt=AIR.phetTimeScale/AIR.phetEventRate, Om=TAU*f*dt;
  const s=Math.sin(Om/2)/LAT.C; if(!(s<=1)) return NaN;
  return TAU/(2*Math.asin(s))*(AIR.W/AIR.phetVis);
}

/* ---- a run: one lattice with ONE hard point source on the middle row ------
   Every picture this sim draws is a shifted or mirrored READ of this one field,
   which is what PhET does: its second speaker is the same lattice read at a
   shifted row, and its reflecting wall is the same lattice read at the mirror
   point.  That is exact, because the wave equation is linear and mirroring is
   an isometry, so u at the mirror of P IS the field of the image source at P
   (derive.py, section F). */
function makeRun(f,n){
  const N=n||LAT.N;
  const R={lat:makeLattice(N,N,LAT.PAD), f:0, Om:0, dt:0, Nl:0, phi:0, t:0, n:0,
           A:AIR.amp0, on:true, cont:true, pressure:1, srcOff:LAT.SRC_OFF,
           pulse:{on:false,phi:0}, val:0};
  runSetFrequency(R,f||AIR.f0,true);
  runClear(R);
  return R;
}
function srcCol(R){ return R.lat.pad+R.srcOff; }
function srcRow(R){ return (R.lat.ny-1)/2; }
/* keep the phase continuous across a frequency change (it is accumulated per
   step, so nothing jumps) */
function runSetFrequency(R,f,quiet){
  R.f=clamp(f,AIR.fmin,AIR.fmax); R.Nl=cellsPerWave(R.f); R.Om=omegaStep(R.Nl); R.dt=stepDt(R.f);
  return R.f;
}
function runClear(R){
  latClear(R.lat); R.phi=0; R.t=0; R.n=0; R.val=0;
  R.pulse.on=false; R.pulse.phi=0;
}
/* PhET's button.  Continuous: it switches the source on and off, and switching
   it on restarts the phase (PhET's resetPhase).  Pulse: it fires one period and
   is dead until that pulse finishes. */
function setSource(R,on){ if(on&&!R.on) R.phi=0; R.on=on; }
function firePulse(R){ if(R.cont||R.pulse.on) return false; R.pulse.on=true; R.pulse.phi=0; return true; }
function pressSource(R){
  if(R.cont){ setSource(R,!R.on); return true; }
  return firePulse(R);
}
function sourceActive(R){ return R.cont?R.on:R.pulse.on; }
/* changing the sound mode stops everything, as PhET's soundModeProperty link does:
   coming back to continuous leaves the speaker waiting for its button */
function setWaveMode(R,cont){
  if(R.cont===cont) return false;
  R.cont=cont; R.pulse.on=false; R.pulse.phi=0; R.on=false;
  return true;
}
/* the drive: 1.2 x the amplitude (PhET's AMPLITUDE_CALIBRATION_SCALE), scaled by
   the air density in the box (PhET scales its source by pressureProperty too) */
function sourceValue(R){
  const amp=R.A*LAT.AMP_CAL*R.pressure;
  if(R.cont) return R.on?amp*Math.sin(R.phi):null;
  if(R.pulse.on){
    R.pulse.phi+=R.Om;
    if(R.pulse.phi<TAU) return amp*Math.sin(R.pulse.phi);
    R.pulse.on=false;
  }
  return null;
}
function runStep(R){
  const L=R.lat;
  latStep(L);
  R.phi+=R.Om;
  const v=sourceValue(R);
  if(v!==null){ L.u[srcRow(R)*L.nx+srcCol(R)]=v; R.val=v; } else R.val=0;
  R.t+=R.dt; R.n++;
}
/* model coordinates (x right, y down, metres, 0..W over the visible region):
   cell (i, j) has its centre at ((i-pad+1/2) dx, (j-pad+1/2) dx) */
function cellOfX(R,x){ return R.lat.pad-0.5+x/sceneDx(); }
function xOfCell(R,i){ return (i-R.lat.pad+0.5)*sceneDx(); }
function srcXY(R){ return [xOfCell(R,srcCol(R)), xOfCell(R,srcRow(R))]; }
/* bilinear read of the lattice at LATTICE coordinates; zero off the lattice */
function latBilinear(L,X,Y){
  if(!(X>=0&&Y>=0&&X<=L.nx-1&&Y<=L.ny-1)) return 0;
  const i0=Math.min(Math.floor(X),L.nx-2), j0=Math.min(Math.floor(Y),L.ny-2);
  const fx=X-i0, fy=Y-j0, u=L.u, k=j0*L.nx+i0;
  return (1-fy)*((1-fx)*u[k]+fx*u[k+1])+fy*((1-fx)*u[k+L.nx]+fx*u[k+L.nx+1]);
}
