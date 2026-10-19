
/* ================================================================== *
 *  THE ENGINE — the scalar wave equation on PhET's 2-D lattice, its   *
 *  point and plane sources, the screen and the probes, calibrated to  *
 *  physical units.  No DOM.  API: build/wave-interference/ENGINE.md   *
 *  (waves-intro builds on this part).  Twin: derive.py (numpy), which *
 *  repeats every operation below in the same order.                   *
 * ================================================================== */

/* PhET's lattice (wave-interference 2.0.22, read from the minified original):
   151 x 151 cells with a 20-cell pad on every side, so 111 x 111 are visible;
   Courant number C = c dt/dx = 1/2 (PhET's WAVE_SPEED 0.5); the point source at
   column 25 on the middle row 75; 20*111/61 lattice steps per second of wall
   time (half that on slow); the source cell driven at 1.2 x the amplitude
   setting and the plane wave at 0.21 x it.  VISIT is PhET's 1e-3 "has the
   light reached this cell" threshold. */
const LAT={N:151, PAD:20, VIS:111, C:0.5, SRC_I:25, MID:75,
           AMP_CAL:1.2, PLANE_MAG:0.21, EVENT_RATE:20*111/61, VISIT:1e-3};
LAT.C2=LAT.C*LAT.C;
/* Mur's absorbing boundary (G. Mur, IEEE Trans. EMC 23, 377 (1981)), the
   discretisation of the Engquist-Majda one-way equation at C = 1/2:
   MUR1 = (C-1)/(C+1) = -1/3, MUR2A = 2/(C+1) = 4/3, MUR2B = C^2/(2(C+1)) = 1/12.
   Second order on the edges, first order at the four corners.  PhET uses a
   different one-way formula; this one reflects |R| <= 3 % up to 45 degrees
   (derive.py: the exact plane-wave reflection, against 17 % for first order). */
const MUR1=(LAT.C-1)/(LAT.C+1), MUR2A=2/(LAT.C+1), MUR2B=LAT.C2/(2*(LAT.C+1));

function makeLattice(nx,ny,pad){
  const n=nx*ny;
  return {nx,ny,pad:(pad===undefined?LAT.PAD:pad),
          u:new Float64Array(n), up:new Float64Array(n), un:new Float64Array(n),
          vis:new Uint8Array(n), steps:0};
}
function latClear(L){ L.u.fill(0); L.up.fill(0); L.un.fill(0); L.vis.fill(0); L.steps=0; }
function latIndex(L,i,j){ return j*L.nx+i; }
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

/* ---- the three media, in PhET's units (PhET's values, from the scene
   definitions in the minified original): the visible width W, the wave
   speed v, the frequency range, the scale bar, the initial and allowed
   slit and source geometry, and PhET's own fixed time scale (kept only to
   report how far its calibration is from this one). ---- */
const C_NM_FS=299.792458;
const SCENES={
  water:{id:'water',name:'water',W:10,unit:'cm',tunit:'s',v:1.65,fmin:0.25,fmax:1,scaleLen:1,
         slitW0:1.5,slitD0:3,sepMin:1,sepMax:5,slitWMin:0.5,slitWMax:2.5,slitDMin:1,slitDMax:5,
         phetTimeScale:1,what:'water level',fUnit:'Hz',fMul:1},
  sound:{id:'sound',name:'sound',W:500,unit:'cm',tunit:'ms',v:34.3,fmin:0.22,fmax:0.44,scaleLen:50,
         slitW0:90,slitD0:200,sepMin:100,sepMax:400,slitWMin:20,slitWMax:160,slitDMin:40,slitDMax:320,
         phetTimeScale:2.4187847116091334,what:'pressure',fUnit:'Hz',fMul:1000},
  light:{id:'light',name:'light',W:5000,unit:'nm',tunit:'fs',v:C_NM_FS,fmin:C_NM_FS/780,fmax:C_NM_FS/380,scaleLen:500,
         slitW0:500,slitD0:1500,sepMin:500,sepMax:4000,slitWMin:200,slitWMax:1600,slitDMin:400,slitDMax:3200,
         phetTimeScale:1416.5/511.034,what:'electric field',fUnit:'THz',fMul:1000}
};
const SCENE_IDS=['water','sound','light'];
function sceneF0(S){ return 0.5*(S.fmin+S.fmax); }          /* PhET starts every scene mid-range */
function sceneDx(S){ return S.W/LAT.VIS; }
function waveLen(S,f){ return S.v/f; }
function cellsPerWave(S,f){ return S.v/f/sceneDx(S); }
/* the calibration: the physical time per step is solved from the dispersion
   relation so that the wave along a lattice axis has EXACTLY the wavelength
   v/f and the frequency f:  Om = 2 asin(C sin(pi dx/lambda)),  dt = Om/(2 pi f).
   (PhET keeps one dt per medium; see phetLambda.) */
function omegaStep(Nl){ return 2*Math.asin(LAT.C*Math.sin(PI/Nl)); }
function stepDt(S,f){ return omegaStep(cellsPerWave(S,f))/(TAU*f); }
/* what PhET's fixed step makes of frequency f: the lattice wavelength, in the
   medium's length unit, for dt = timeScale/EVENT_RATE along an axis */
function phetLambda(S,f){
  const dt=S.phetTimeScale/LAT.EVENT_RATE, Om=TAU*f*dt;
  const s=Math.sin(Om/2)/LAT.C; if(!(s<=1)) return NaN;
  return TAU/(2*Math.asin(s))*sceneDx(S);
}

/* ---- a run: one lattice, what drives it and what measures it ------------
   mode 'point': one or two in-phase hard sources on column SRC_I, rows MID and
   MID -/+ round(sep/2dx); 'plane': PhET's slits screen — every cell from the
   pad to the barrier column is set to the analytic plane wave, which is an
   exact solution of the lattice equations (the calibration makes it one),
   and the barrier column is a Dirichlet boundary: zero where it is blocked,
   the plane wave in the openings. */
const SCREEN_HIST=180;
function makeRun(sceneId,mode,nSrc,nx){
  const n=nx||LAT.N;
  const R={lat:makeLattice(n,n,LAT.PAD), mode:mode||'point', nSrc:nSrc||1,
           scene:null, f:0, A:8, Om:0, dt:0, Nl:0, phi:0, t:0, n:0,
           src:[true,true], pulse:{on:false,phi:0}, cont:true, sep:0,
           plane:{on:true,m:0,barrier:'one',bcol:LAT.MID,slitW:0,slitD:0},
           watch:{on:false,t:0}, probes:[], trace:[], screen:null};
  runSetScene(R,sceneId||'water');
  return R;
}
function runSetScene(R,sceneId){
  const S=SCENES[sceneId];
  R.scene=sceneId; R.sep=S.slitD0; R.plane.slitW=S.slitW0; R.plane.slitD=S.slitD0;
  R.t=0; R.n=0; R.watch.t=0;                       /* a new medium has its own clock and units */
  runSetFrequency(R,sceneF0(S),true);
  runClear(R);
}
/* keep the phase continuous across a frequency change (it is accumulated per
   step, so nothing jumps); light and plane waves clear, as in PhET */
function runSetFrequency(R,f,quiet){
  const S=SCENES[R.scene];
  R.f=clamp(f,S.fmin,S.fmax); R.Nl=cellsPerWave(S,R.f); R.Om=omegaStep(R.Nl); R.dt=stepDt(S,R.f);
  if(!quiet&&(R.scene==='light'||R.mode==='plane')) runClear(R);
}
function runClear(R){
  latClear(R.lat); R.phi=0; R.pulse.on=false; R.pulse.phi=0; R.plane.m=0; R.trace=[];
  const rows=R.lat.ny-2*R.lat.pad;
  R.screen={rows, buf:new Float64Array(rows*SCREEN_HIST), head:0, count:0};
}
/* PhET's clearRight: when the barrier moves, everything from its new column
   rightward is wiped; the plane wave to its left keeps its progress */
function runClearRight(R,col){
  const L=R.lat, nx=L.nx;
  for(let j=0;j<L.ny;j++) for(let i=Math.max(0,col);i<nx;i++){ const k=j*nx+i; L.u[k]=0; L.up[k]=0; L.un[k]=0; L.vis[k]=0; }
  const rows=L.ny-2*L.pad;
  R.screen={rows, buf:new Float64Array(rows*SCREEN_HIST), head:0, count:0}; R.trace=[];
}
/* the source column: PhET's 25 on the 151 lattice, i.e. 5 cells into the view */
function srcCol(L){ return L.pad+LAT.SRC_I-LAT.PAD; }
/* switching a source on restarts the phase only if no other source is
   running, so two sources always stay in phase (PhET's rule) */
function runSetSource(R,s,on){
  if(on&&!R.src[s]&&!R.src.some((v,q)=>v&&q!==s&&q<R.nSrc)) R.phi=0;
  R.src[s]=on;
}
/* the source rows: PhET's roundSymmetric(sep/2 in cells) either side of MID */
function runSourceRows(R){
  const S=SCENES[R.scene], h=Math.round(R.sep/(2*sceneDx(S)));
  const mid=(R.lat.ny-1)/2;
  return R.nSrc===2?[mid-h,mid+h]:[mid];
}
/* is row j open in the barrier?  cell centres |y - centre| < half-width, in cells */
function slitOpen(R,j){
  const P=R.plane, S=SCENES[R.scene], dx=sceneDx(S), mid=(R.lat.ny-1)/2, y=j-mid;
  if(P.barrier==='none') return true;
  const a=P.slitW/(2*dx);
  if(P.barrier==='one') return Math.abs(y)<a;
  const c=P.slitD/(2*dx);
  return Math.abs(y-c)<a||Math.abs(y+c)<a;
}
/* the slit geometry the lattice actually has: open cells per slit, and the
   distance between the centres of the two open groups, in cells */
function slitCells(R){
  const ny=R.lat.ny, mid=(ny-1)/2; let lo=[], hi=[];
  for(let j=0;j<ny;j++) if(slitOpen(R,j)){ if(j<mid) lo.push(j); else if(j>mid) hi.push(j); else { lo.push(j); hi.push(j); } }
  if(R.plane.barrier!=='two'){ const all=[]; for(let j=0;j<ny;j++) if(slitOpen(R,j)) all.push(j);
    return {n:all.length, a:all.length, d:0, lo:all.length?all[0]:NaN, hi:all.length?all[all.length-1]:NaN}; }
  const cen=g=>g.length?(g[0]+g[g.length-1])/2:NaN;
  return {n:lo.length+hi.length, a:hi.length, d:cen(hi)-cen(lo), lo:lo.length?lo[0]:NaN, hi:hi.length?hi[hi.length-1]:NaN};
}
function runStep(R){
  const L=R.lat;
  latStep(L);
  R.phi+=R.Om;
  if(R.mode==='point') setPointSources(R); else setPlaneWave(R);
  R.t+=R.dt; R.n++;
  if(R.watch.on) R.watch.t+=R.dt;
  recordScreen(R);
  if(R.probes.length){
    const s=[R.t]; for(const p of R.probes) s.push(probeValue(R,p[0],p[1]));
    R.trace.push(s); if(R.trace.length>900) R.trace.shift();
  }
}
function setPointSources(R){
  const L=R.lat, u=L.u, rows=runSourceRows(R), amp=R.A*LAT.AMP_CAL;
  let val=null;
  if(R.cont) val=amp*Math.sin(R.phi);
  else if(R.pulse.on){
    R.pulse.phi+=R.Om;
    if(R.pulse.phi<TAU) val=amp*Math.sin(R.pulse.phi); else { val=0; R.pulse.on=false; }
  }
  if(val===null) return;
  const ci=srcCol(L);
  for(let s=0;s<rows.length;s++) if(R.src[s]) u[rows[s]*L.nx+ci]=val;
}
function firePulse(R){ if(R.cont) return false; R.pulse.on=true; R.pulse.phi=0; return true; }
/* the plane wave, sin(Om m - k x), x in cells from the edge of the pad: its
   front (phase 0) moves at the phase speed Om/k, so the cut is continuous */
function setPlaneWave(R){
  const L=R.lat, P=R.plane, nx=L.nx, ny=L.ny, u=L.u, up=L.up, pad=L.pad;
  const iR=P.barrier==='none'?nx-pad:P.bcol;
  const k=TAU/R.Nl, amp=LAT.PLANE_MAG*R.A;
  const front=P.on?P.m*R.Om/k:-1;
  for(let i=pad;i<=iR;i++){
    const x=i-pad, val=(P.on&&x<=front)?amp*Math.sin(R.Om*P.m-k*x):0;
    for(let j=0;j<ny;j++){
      const q=j*nx+i, v=(i===iR&&P.barrier!=='none'&&!slitOpen(R,j))?0:val;
      u[q]=v; up[q]=v;
    }
  }
  if(P.on) P.m++;
}
/* the screen: PhET's intensity is the mean square of the last-visible column
   over a history window; here the window is the whole number of periods
   nearest 90 steps (PhET's 90), so the mean of sin^2 carries no phase ripple */
function recordScreen(R){
  const Sc=R.screen, L=R.lat, col=L.nx-L.pad-1, rows=Sc.rows;
  const off=Sc.head*rows;
  for(let r=0;r<rows;r++) Sc.buf[off+r]=L.u[(L.pad+r)*L.nx+col];
  Sc.head=(Sc.head+1)%SCREEN_HIST; if(Sc.count<SCREEN_HIST) Sc.count++;
}
function screenWindow(R){
  const P=TAU/R.Om, m=Math.max(1,Math.round(90/P));
  return Math.max(1,Math.min(SCREEN_HIST,Math.round(m*P)));
}
function screenIntensity(R){
  const Sc=R.screen, rows=Sc.rows, w=Math.min(Sc.count,screenWindow(R)), out=new Float64Array(rows);
  if(w<1) return out;
  for(let s=1;s<=w;s++){
    const off=((Sc.head-s+SCREEN_HIST)%SCREEN_HIST)*rows;
    for(let r=0;r<rows;r++){ const v=Sc.buf[off+r]; out[r]+=v*v; }
  }
  for(let r=0;r<rows;r++) out[r]/=w;
  return out;
}
/* model coordinates (x right, y down, both in the medium's unit, 0..W over the
   visible region): cell (i, j) has its centre at ((i-pad+1/2) dx, (j-pad+1/2) dx) */
function cellOfX(R,x){ return R.lat.pad-0.5+x/sceneDx(SCENES[R.scene]); }
function xOfCell(R,i){ return (i-R.lat.pad+0.5)*sceneDx(SCENES[R.scene]); }
function probeValue(R,x,y){
  const L=R.lat, X=cellOfX(R,x), Y=cellOfX(R,y);
  const i0=clamp(Math.floor(X),0,L.nx-2), j0=clamp(Math.floor(Y),0,L.ny-2);
  const fx=clamp(X-i0,0,1), fy=clamp(Y-j0,0,1), u=L.u, k=j0*L.nx+i0;
  return (1-fy)*((1-fx)*u[k]+fx*u[k+1])+fy*((1-fx)*u[k+L.nx]+fx*u[k+L.nx+1]);
}
