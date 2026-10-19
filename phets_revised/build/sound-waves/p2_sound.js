
/* ================================================================== *
 *  SOUND WAVES' own layer on the lattice: the wall as an image        *
 *  source, the second speaker as a shifted read, the air parcels, the *
 *  steady-state measurement of the wavelength, the gas itself, and    *
 *  the tone.  No DOM.  Twin: derive.py, which repeats every operation *
 *  below in the same order (refvals.txt).                             *
 * ================================================================== */

/* PhET maps a lattice value of +2 to full white and -1.5 to (almost) black; this
   sim uses a symmetric +/-2, because a compression and a rarefaction of the same
   size ARE the same size.  It is PhET's MAX-amplitude-to-plot in all but the
   asymmetry (read from the minified original, SoundWaveCanvasNode.paintCanvas). */
const U_FULL=2.0;

/* ---- the wall ------------------------------------------------------------
   PhET's reflector crosses the BOTTOM edge of the wave area at wallPositionX
   and leans back at wallAngle, so it is the line through A = (xw, W) with the
   direction dhat = (cos th, -sin th) -- y runs down, as on the lattice.  Its
   normal is nhat = (sin th, cos th), and PhET's own test for "the sound is on
   this side", x < xw - (y - W)/tan(th), is exactly (P - A).nhat < 0.
   PhET's ranges: xw in [W/3, 2W/3] (default W/3), th in [0.1 pi, 0.5 pi]
   (default pi/4). */
const WALLR={xmin:AIR.W/3, xmax:2*AIR.W/3, x0:AIR.W/3,
             amin:0.1*PI, amax:0.5*PI, a0:0.25*PI};
function wallGeom(xw,th){
  return {xw, th, ax:xw, ay:AIR.W,
          dxh:Math.cos(th), dyh:-Math.sin(th), nxh:Math.sin(th), nyh:Math.cos(th)};
}
/* the signed distance to the wall: negative on the side the sound is on */
function wallSide(G,x,y){ return (x-G.ax)*G.nxh+(y-G.ay)*G.nyh; }
function wallMirror(G,x,y){ const s=2*wallSide(G,x,y); return [x-s*G.nxh, y-s*G.nyh]; }
function wallFoot(G,x,y){ const t=(x-G.ax)*G.dxh+(y-G.ay)*G.dyh; return [G.ax+t*G.dxh, G.ay+t*G.dyh]; }
/* where the ray from S to P bounces: the straight line from the IMAGE of S to P
   crosses the wall there, and there the angle of incidence equals the angle of
   reflection and |SQ| + |QP| = |S'P| is the shortest path (derive.py, F) */
function wallBounce(G,sx,sy,px,py){
  const I=wallMirror(G,sx,sy);
  const den=(px-I[0])*G.nxh+(py-I[1])*G.nyh;
  if(!(Math.abs(den)>1e-13)) return null;
  const t=((G.ax-I[0])*G.nxh+(G.ay-I[1])*G.nyh)/den;
  if(!(t>0&&t<1)) return null;
  return [I[0]+t*(px-I[0]), I[1]+t*(py-I[1])];
}
/* the angle a direction makes with the wall's normal, in [0, pi/2] */
function angleToNormal(G,vx,vy){
  const L=Math.hypot(vx,vy);
  if(!(L>0)) return NaN;
  return Math.acos(Math.min(1,Math.abs((vx*G.nxh+vy*G.nyh)/L)));
}

/* ---- the composed picture ------------------------------------------------
   Every view draws the SAME lattice field:
     'one'  read straight,
     'two'  read at two shifts in y -- a source on lattice row r contributes
            u(i, j - (r - mid)), so the second speaker costs nothing,
     'wall' read twice, direct and mirrored, and nothing behind the wall.
   Both are exact superpositions: the equation is linear, and mirroring is an
   isometry, so u at the mirror of P IS the field of the image source at P.
   The grid is allocated once per run and OVERWRITTEN in place, so a caller must
   use it before building the next model. */
function fieldGrid(R,mode,rows,G){
  const L=R.lat, V=LAT.VIS, pad=L.pad, nx=L.nx, ny=L.ny, u=L.u, mid=srcRow(R), dx=sceneDx();
  if(!R.grid) R.grid={v:new Float64Array(V*V), mask:new Uint8Array(V*V), nfront:0};
  const g=R.grid, v=g.v, mk=g.mask;
  let nfront=0;
  if(mode==='two'){
    const s0=rows[0]-mid, s1=rows[1]-mid;
    for(let j=0;j<V;j++){
      const J=pad+j, q=j*V, j0=J-s0, j1=J-s1;
      const r0=(j0>=0&&j0<ny)?j0*nx:-1, r1=(j1>=0&&j1<ny)?j1*nx:-1;
      for(let i=0;i<V;i++){
        const I=pad+i;
        v[q+i]=(r0>=0?u[r0+I]:0)+(r1>=0?u[r1+I]:0); mk[q+i]=1;
      }
    }
    nfront=V*V;
  } else if(mode==='wall'){
    /* the mirror is affine, so s and the mirrored indices march along a row */
    const sI=dx*G.nxh, sJ=dx*G.nyh;
    const kx=2*G.nxh/dx, ky=2*G.nyh/dx;
    for(let j=0;j<V;j++){
      const J=pad+j, q=j*V;
      let s=(0.5*dx-G.ax)*G.nxh+((j+0.5)*dx-G.ay)*G.nyh;      /* the cell centre at i = 0 */
      for(let i=0;i<V;i++,s+=sI){
        const I=pad+i;
        if(s>=0){ v[q+i]=0; mk[q+i]=0; continue; }
        const Ip=Math.round(I-kx*s), Jp=Math.round(J-ky*s);
        v[q+i]=u[J*nx+I]+latAt(L,Ip,Jp); mk[q+i]=1; nfront++;
      }
    }
  } else {
    for(let j=0;j<V;j++){
      const r=(pad+j)*nx+pad, q=j*V;
      for(let i=0;i<V;i++){ v[q+i]=u[r+i]; mk[q+i]=1; }
    }
    nfront=V*V;
  }
  g.nfront=nfront;
  return g;
}
/* the same composition at an arbitrary model point, bilinear (what the listener
   and the probes read) */
function fieldAtModel(R,mode,rows,G,x,y){
  const L=R.lat, mid=srcRow(R), X=cellOfX(R,x), Y=cellOfX(R,y);
  if(mode==='two') return latBilinear(L,X,Y-(rows[0]-mid))+latBilinear(L,X,Y-(rows[1]-mid));
  if(mode==='wall') return wallSide(G,x,y)>=0?0:mirrorSum(R,G,x,y);
  return latBilinear(L,X,Y);
}
/* the direct wave plus its image, WITHOUT the mask: this is the field the image
   construction really defines, and it is even about the wall, which is why
   du/dn vanishes there.  What the sim draws is this, cut off behind the wall. */
function mirrorSum(R,G,x,y){
  const L=R.lat, m=wallMirror(G,x,y);
  return latBilinear(L,cellOfX(R,x),cellOfX(R,y))+latBilinear(L,cellOfX(R,m[0]),cellOfX(R,m[1]));
}
/* the model positions of the speakers a view shows: one on the middle row, or
   two on the rows nearest the y positions asked for */
function rowOfY(R,y){ return clamp(Math.round(cellOfX(R,y)),R.lat.pad+1,R.lat.ny-R.lat.pad-2); }
function yOfRow(R,j){ return xOfCell(R,j); }

/* ---- the air parcels -----------------------------------------------------
   Sound in a gas is longitudinal: rho d2xi/dt2 = -grad p, so at one frequency
   xi = grad p / (rho omega^2) and the parcels crowd where the pressure is high.
   Drawn exaggerated: the scale makes a wave at full contrast push a parcel 0.45
   of the parcel spacing, well short of the spacing that would make rows cross
   (Known-bad: a displacement larger than the spacing destroys the bunching it
   is meant to show). */
const PARC_N=20, PARC_PUSH=0.45;
function parcelPositions(R,g){
  const V=LAT.VIS, k=TAU/R.Nl, KD=PARC_PUSH*(V/PARC_N)/(k*U_FULL), out=[];
  for(let a=0;a<=PARC_N;a++) for(let b=0;b<=PARC_N;b++){
    const i=clamp(Math.round(a*V/PARC_N),1,V-2), j=clamp(Math.round(b*V/PARC_N),1,V-2), q=j*V+i;
    if(!g.mask[q]){ out.push([i,j,0]); continue; }
    const gx=(g.mask[q+1]&&g.mask[q-1])?(g.v[q+1]-g.v[q-1])/2:0;
    const gy=(g.mask[q+V]&&g.mask[q-V])?(g.v[q+V]-g.v[q-V])/2:0;
    out.push([i+KD*gx, j+KD*gy, 1]);
  }
  return out;
}

/* ---- the gas -------------------------------------------------------------
   c = sqrt(gamma p / rho) = sqrt(gamma R T / M): p and rho both scale with how
   much gas is in the box at fixed temperature, so the SPEED does not move at
   all as the air is removed.  What falls is the amplitude: a cone of fixed
   velocity radiates p = rho c u, so the pressure amplitude goes as rho and the
   intensity I = p^2/(rho c) goes as rho too -- both are 20 log10(rho/rho0) dB.
   That is also what PhET does, in one line: it multiplies the source cell by
   its pressure property. */
const GAS={gamma:1.4,            /* a diatomic ideal gas */
           R:8.314462618,        /* J/mol/K, exact since the 2019 SI redefinition */
           M:28.9647e-3,         /* kg/mol, standard dry air */
           T0:293.15,            /* 20.00 C */
           kB:1.380649e-23,      /* J/K, exact */
           d:3.7e-10,            /* m, the kinetic-theory collision diameter of air */
           pAtm:101325};         /* Pa, exact */
function soundSpeedIdeal(T){ return Math.sqrt(GAS.gamma*GAS.R*T/GAS.M); }
function tempForSpeed(v){ return v*v*GAS.M/(GAS.gamma*GAS.R); }
function airDensity(frac,T){ return frac*GAS.pAtm*GAS.M/(GAS.R*(T===undefined?GAS.T0:T)); }
function meanFreePath(frac,T){
  const TT=(T===undefined?GAS.T0:T);
  return GAS.kB*TT/(Math.SQRT2*PI*GAS.d*GAS.d*frac*GAS.pAtm);
}
function knudsen(frac,f,T){ return meanFreePath(frac,T)/waveLen(f); }
function dbOf(r){ return r>0?20*Math.log10(r):-Infinity; }

/* ---- the steady state along the axis -------------------------------------
   A fresh run at frequency f on a shorter tank of the SAME cells (MEAS.N cells,
   the source MEAS.SRC cells in), so that the measurement is about the lattice's
   calibration and not about the box this sim draws.  After MEAS.N0 steps the
   front has crossed the tank about 1.3 times; MEAS.PER whole periods are then
   recorded along the source's row, and at every cell the record is fitted by
   least squares to

        u(n) = a sin(phi_n) + b cos(phi_n) + c + d (n - nbar)

   against the drive's own phase, so the amplitude is hypot(a, b) and the phase
   atan2(b, a).  The constant and the drift absorb the wake of the switch-on,
   which in two dimensions dies only as 1/(omega t).  lambda is 2 pi over the
   slope of the unwrapped phase across cells MEAS.R0..MEAS.R1; the envelope's
   power is the slope of log amplitude against log r over the same cells. */
const MEAS={N:181, SRC:5, N0:470, PER:2, R0:30, R1:120, A:8};
const MEAS_CACHE=[];
function measureWave(f){
  const key=f.toFixed(6);
  for(const e of MEAS_CACHE) if(e.key===key) return e.val;
  const val=measureCompute(f);
  MEAS_CACHE.unshift({key,val});
  if(MEAS_CACHE.length>12) MEAS_CACHE.pop();
  return val;
}
/* Gaussian elimination with partial pivoting on the 4 x 4 normal equations */
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
/* unwrap a sequence of angles: each step brought into (-pi, pi] by whole turns.
   Lifted out so BOTH branches can be tested -- the wave here travels outward, so
   its phase only ever falls and only the first branch is reached (Known-bad: a
   branch no test reaches is covered by nothing). */
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
function measureCompute(f){
  const R=makeRun(f,MEAS.N);
  R.srcOff=MEAS.SRC; R.A=MEAS.A;
  runClear(R);
  for(let s=0;s<MEAS.N0;s++) runStep(R);
  const L=R.lat, ci=srcCol(R), nc=L.nx-L.pad-ci, mid=srcRow(R), off=mid*L.nx+ci;
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
  return {f, M, nc, amp, ph:un, snap, Nl:R.Nl, lamCells, pexp,
          afit:sa/(MEAS.R1-MEAS.R0+1), lam:lamCells*sceneDx(), lam0:waveLen(f),
          err:lamCells/R.Nl-1, dt:R.dt, steps:R.n};
}

/* ---- the nodal lines of two sources --------------------------------------
   Two in-phase sources a distance d apart are quiet where |r1 - r2| =
   (m + 1/2) lambda, which is a hyperbola with the sources as its foci.  With
   the origin at their midpoint and the sources on the y axis at +/- d/2,

        y^2/a^2 - x^2/(c^2 - a^2) = 1,   a = (m + 1/2) lambda / 2,  c = d/2,

   and it exists only while a < c, so there are as many nodal lines each side as
   there are m with (m + 1/2) lambda < d.  Far away the branch runs at
   sin(theta) = (m + 1/2) lambda / d from the axis -- the two-slit condition. */
function nodeOrders(d,lam){
  const out=[];
  for(let m=0;(m+0.5)*lam<d;m++) out.push(m);
  return out;
}
function nodeY(m,lam,d,x){          /* the height of the m-th branch at distance x */
  const a=(m+0.5)*lam/2, c=d/2, t=c*c-a*a;
  if(!(t>0)) return NaN;
  return a*Math.sqrt(1+x*x/t);
}
function nodeX(m,lam,d,y){          /* and its distance at height y */
  const a=(m+0.5)*lam/2, c=d/2, t=y*y/(a*a)-1;
  if(!(t>0)||a>=c) return NaN;
  return Math.sqrt((c*c-a*a)*t);
}
function nodeFarAngle(m,lam,d){
  const s=(m+0.5)*lam/d;
  return s<=1?Math.asin(s):NaN;
}
/* the same nodal line with the LATTICE's own wavenumber, which is longer off
   the axes: solving |k(th1) r1 - k(th2) r2| = (2m+1) pi instead of using one
   lambda moves the line out by a couple of cells, which is exactly where the
   lattice really puts it (derive.py, section E). */
function latKofDir(Om,dx0,dy0){ return latK(Om,Math.atan2(Math.abs(dy0),Math.abs(dx0)))/sceneDx(); }
function nodePhase(Om,d,x,y){
  const ax=x, ay1=y-d/2, ay2=y+d/2;
  const r1=Math.hypot(ax,ay1), r2=Math.hypot(ax,ay2);
  return Math.abs(latKofDir(Om,ax,ay1)*r1-latKofDir(Om,ax,ay2)*r2);
}
function nodeYLattice(m,Om,d,x,y0){
  let lo=0.25*y0, hi=3*y0, want=(2*m+1)*PI;
  if(!(nodePhase(Om,d,x,lo)<want)) return NaN;
  for(let it=0;it<90;it++){
    const mid=0.5*(lo+hi);
    if(nodePhase(Om,d,x,mid)<want) lo=mid; else hi=mid;
  }
  return 0.5*(lo+hi);
}

/* ---- the listener --------------------------------------------------------
   A rolling window of the composed field at the listener, one period long, so
   the amplitude is sqrt(2 <u^2>).  PhET instead computes A |cos(pi dr / lambda)|
   with lambda = 36/f in MODEL UNITS -- 4.96 % longer than v/f, a hand-tuned
   constant; both are printed so the difference is visible. */
function makeProbe(n){ return {buf:new Float64Array(Math.max(4,n)), head:0, count:0, n:Math.max(4,n), mode:''}; }
function probeResize(P,n){
  n=Math.max(4,Math.min(4000,Math.round(n)));
  if(P.n===n) return P;
  P.buf=new Float64Array(n); P.n=n; P.head=0; P.count=0;
  return P;
}
function probePush(P,v){ P.buf[P.head]=v; P.head=(P.head+1)%P.n; if(P.count<P.n) P.count++; }
function probeAmp(P){
  if(P.count<1) return 0;
  let s=0;
  for(let i=0;i<P.count;i++) s+=P.buf[i]*P.buf[i];
  return Math.sqrt(2*s/P.count);
}
/* the textbook two-source law: amplitudes A1, A2 arriving with a phase
   difference dphi give sqrt(A1^2 + A2^2 + 2 A1 A2 cos dphi) */
function twoSourceAmp(a1,a2,dphi){ return Math.sqrt(a1*a1+a2*a2+2*a1*a2*Math.cos(dphi)); }
function phetListenerFactor(A,dr,f){ return A*Math.abs(Math.cos(PI*dr/(AIR.phetListenerLambdaK/f*100))); }

/* ---- the tone ------------------------------------------------------------
   A sine at the frequency on the slider, played from a buffer of whole cycles
   so that it loops seamlessly and the suite can check the samples.  The output
   level runs linearly from 0 to 0.3 over the amplitude range (the level PhET's
   sound scene uses in Waves Intro); with the listener selected it follows the
   pressure amplitude the lattice actually holds at the listener instead.  PhET's
   own Sound Waves multiplies its oscillator by A |cos(pi dr / (36/f))| — a
   hand-tuned wavelength, which the analysis prints beside the real one. */
const TONE_SR=44100, TONE_SECONDS=0.5, TONE_MAX=0.3;
function toneLevel(mode,A,listenAmp){
  if(mode==='listener') return TONE_MAX*clamp(listenAmp/U_FULL,0,1);
  return TONE_MAX*clamp(A/AIR.ampMax,0,1);
}
function toneBuffer(hz,level,sr){
  const m=Math.max(1,Math.round(hz*TONE_SECONDS)), L=Math.round(m*sr/hz), data=new Float32Array(L);
  for(let i=0;i<L;i++) data[i]=level*Math.sin(TAU*m*i/L);
  return {data, m, L, hz:m*sr/L};
}
