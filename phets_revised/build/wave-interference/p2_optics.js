
/* ================================================================== *
 *  the colour of a wavelength: CIE 1931 (p2_cie.js, the CIE's own     *
 *  table every 5 nm) -> linear sRGB, desaturated into gamut toward    *
 *  white and normalised to its brightest channel (hue, not luminance) *
 * ================================================================== */
function cieAt(nm){
  const T=CIE1931, x=clamp((nm-T[0][0])/5,0,T.length-1), i=Math.min(T.length-2,Math.floor(x)), f=x-i;
  return [T[i][1]+(T[i+1][1]-T[i][1])*f, T[i][2]+(T[i+1][2]-T[i][2])*f, T[i][3]+(T[i+1][3]-T[i][3])*f];
}
function specLinear(nm){
  const c=cieAt(nm);
  if(c[0]+c[1]+c[2]<1e-9) return [0,0,0];
  let r=SRGB_M[0][0]*c[0]+SRGB_M[0][1]*c[1]+SRGB_M[0][2]*c[2];
  let g=SRGB_M[1][0]*c[0]+SRGB_M[1][1]*c[1]+SRGB_M[1][2]*c[2];
  let b=SRGB_M[2][0]*c[0]+SRGB_M[2][1]*c[1]+SRGB_M[2][2]*c[2];
  const lo=Math.min(r,g,b); if(lo<0){ r-=lo; g-=lo; b-=lo; }
  const hi=Math.max(r,g,b,1e-12);
  return [r/hi,g/hi,b/hi];
}
/* intensity applied in LINEAR light, then gamma-encoded (diffraction.html's rule) */
function specCss(nm,I){
  const c=specLinear(nm), t=clamp(I,0,1);
  return 'rgb('+Math.round(255*srgbGamma(c[0]*t))+','+Math.round(255*srgbGamma(c[1]*t))+','+Math.round(255*srgbGamma(c[2]*t))+')';
}

/* ================================================================== *
 *  the far field: PhET's Diffraction screen                           *
 *  A 256 x 256 aperture spans 4/3 mm (PhET's DIFFRACTION_MATRIX_      *
 *  DIMENSION and DIFFRACTION_APERTURE_WIDTH), so a pixel is 1/192 mm. *
 *  The pattern is |FFT| of the aperture, shifted to the centre.  To   *
 *  keep the picture's angular scale fixed as the wavelength changes,  *
 *  PhET redraws the aperture magnified by s = lambda0/lambda (lambda0  *
 *  = 511.03 nm, the harmonic mean of 380 and 780 nm); then one FFT bin *
 *  is  sin(theta) = lambda0 / (N px) = 3.8328e-4  at every wavelength. *
 * ================================================================== */
const DIF={N:256, WIDTH:4/3, LAM0:2/(1/780+1/380), Q:4, LAMMIN:380, LAMMAX:780, SLIT_H:0.3, FIG_SEED:20260918};
/* the first zero of J1 (scipy.special.jn_zeros(1,1)); selfTest asserts J1 vanishes there */
const J11=3.8317059702075125;
DIF.PX=DIF.WIDTH/DIF.N;
DIF.SIN_PER_BIN=DIF.LAM0*1e-6/(DIF.N*DIF.PX);
const APERTURES=[
  {id:'ellipse',name:'ellipse',phet:true},{id:'rect',name:'rectangle',phet:true},
  {id:'cs',name:'circle & square',phet:true},{id:'disorder',name:'disorder',phet:true},
  {id:'figure',name:'a waving figure',phet:true},{id:'gauss',name:'Gaussian',phet:false},
  {id:'slits',name:'slits',phet:false}];
function difScale(lam){ return DIF.LAM0/lam; }
/* the disorder lattice: 4 x 4 circles; each is pushed off its site by
   (level/4) x 0.3 spacing x a fixed random vector in the unit disc (Park-Miller
   minimal-standard generator, seed 20260918 — integer arithmetic, so the
   python twin reproduces it exactly).  A new design: PhET's own table of
   offsets is not used. */
const DISORDER_V=(function(){
  let x=DIF.FIG_SEED%2147483647; const out=[];
  const nxt=()=>{ x=(48271*x)%2147483647; return x/2147483647; };
  for(let q=0;q<16;q++){ const a=TAU*nxt(), r=Math.sqrt(nxt()); out.push([r*Math.cos(a),r*Math.sin(a)]); }
  return out;
})();
/* the waving figure, in units of its height (y down, centred): a head and
   six capsules — new art standing in for PhET's photograph */
const FIGURE={head:[0,-0.38,0.12],
  caps:[[0,-0.25,0,0.1,0.055],[0,0.1,-0.12,0.47,0.035],[0,0.1,0.12,0.47,0.035],
        [0,-0.17,-0.2,0.05,0.03],[0,-0.17,0.17,-0.3,0.03],[0.17,-0.3,0.22,-0.47,0.03]]};
function segDist2(px,py,ax,ay,bx,by){
  const dx=bx-ax, dy=by-ay, L2=dx*dx+dy*dy;
  let t=L2>0?((px-ax)*dx+(py-ay)*dy)/L2:0; t=t<0?0:(t>1?1:t);
  const ex=ax+t*dx-px, ey=ay+t*dy-py; return ex*ex+ey*ey;
}
/* the aperture as geometry, in mm, magnified by s: inside(x, y) and a bounding
   box; the Gaussian is a transmission profile instead (grey, sampled at
   pixel centres) and the rectangle is snapped to whole pixels, as PhET's is */
/* the ellipse's semi-axes: D/2 and D/2 sqrt(1 - e^2), magnified by s (one formula for
   the renderer and the drawing both) */
function ellipseAxes(P,s){ const rx=s*P.ellD/2; return [rx,rx*Math.sqrt(1-P.ellE*P.ellE)]; }
function apertureShape(P,s){
  const id=P.ap;
  if(id==='ellipse'){
    const ax=ellipseAxes(P,s), rx=ax[0], ry=ax[1];
    return {bb:[-rx,rx,-ry,ry], inside:(x,y)=>(x/rx)*(x/rx)+(y/ry)*(y/ry)<1};
  }
  if(id==='cs'){
    const c=26*DIF.PX*s, r=s*P.csD/2, h=s*P.csW/2;
    return {bb:[-c-Math.max(r,h),c+Math.max(r,h),-c-Math.max(r,h),c+Math.max(r,h)],
            inside:(x,y)=>((x+c)*(x+c)+(y+c)*(y+c)<r*r)||(Math.abs(x-c)<h&&Math.abs(y-c)<h)};
  }
  if(id==='disorder'){
    const p=P.disP, r=s*P.disD/2, f=P.disL/4*0.3*p, cen=[];
    for(let a=0;a<4;a++) for(let b=0;b<4;b++){ const v=DISORDER_V[4*a+b];
      cen.push([s*((a-1.5)*p+f*v[0]), s*((b-1.5)*p+f*v[1])]); }
    let m=0; for(const c of cen) m=Math.max(m,Math.abs(c[0])+r,Math.abs(c[1])+r);
    return {bb:[-m,m,-m,m], inside:(x,y)=>{ for(const c of cen){ const dx=x-c[0], dy=y-c[1]; if(dx*dx+dy*dy<r*r) return true; } return false; }};
  }
  if(id==='figure'){
    const H=s*P.figH, rot=P.figR*PI/180, co=Math.cos(rot), si=Math.sin(rot), hd=FIGURE.head;
    return {bb:[-0.6*H,0.6*H,-0.6*H,0.6*H], inside:(x,y)=>{
      const u=(x*co+y*si)/H, v=(-x*si+y*co)/H;
      if((u-hd[0])*(u-hd[0])+(v-hd[1])*(v-hd[1])<hd[2]*hd[2]) return true;
      for(const c of FIGURE.caps) if(segDist2(u,v,c[0],c[1],c[2],c[3])<c[4]*c[4]) return true;
      return false; }};
  }
  if(id==='slits'){
    const n=Math.round(P.sltN), a=s*P.sltW/2, d=s*P.sltD, hh=s*DIF.SLIT_H/2, x0=-(n-1)/2*d;
    return {bb:[x0-a,-x0+a,-hh,hh], inside:(x,y)=>{
      if(Math.abs(y)>=hh) return false;
      for(let q=0;q<n;q++) if(Math.abs(x-(x0+q*d))<a) return true;
      return false; }};
  }
  return null;
}
/* render the aperture into an N x N transmission map (row j, column i; the
   aperture's centre sits on the corner between pixels 127 and 128, as in
   PhET's canvas).  Shapes are covered by Q x Q sub-samples per pixel. */
function renderAperture(P,lam){
  const N=DIF.N, px=DIF.PX, s=difScale(lam), t=new Float64Array(N*N), h=N/2;
  if(P.ap==='rect'){
    const iw=Math.round(P.recW*s/(2*px)), ih=Math.round(P.recH*s/(2*px));
    for(let j=h-ih;j<h+ih;j++) for(let i=h-iw;i<h+iw;i++) if(i>=0&&i<N&&j>=0&&j<N) t[j*N+i]=1;
    return {t,s,iw,ih};
  }
  if(P.ap==='gauss'){
    const sx=s*P.gauSx, sy=s*P.gauSy;
    for(let j=0;j<N;j++){ const y=(j-h+0.5)*px;
      for(let i=0;i<N;i++){ const x=(i-h+0.5)*px;
        t[j*N+i]=Math.exp(-(x*x/(2*sx*sx)+y*y/(2*sy*sy))); } }
    return {t,s};
  }
  const G=apertureShape(P,s), Q=DIF.Q;
  const i0=Math.max(0,Math.floor(G.bb[0]/px+h)-1), i1=Math.min(N-1,Math.ceil(G.bb[1]/px+h)+1);
  const j0=Math.max(0,Math.floor(G.bb[2]/px+h)-1), j1=Math.min(N-1,Math.ceil(G.bb[3]/px+h)+1);
  for(let j=j0;j<=j1;j++) for(let i=i0;i<=i1;i++){
    let c=0;
    for(let qy=0;qy<Q;qy++){ const y=(j-h+(qy+0.5)/Q)*px;
      for(let qx=0;qx<Q;qx++){ const x=(i-h+(qx+0.5)/Q)*px; if(G.inside(x,y)) c++; } }
    t[j*N+i]=c/(Q*Q);
  }
  return {t,s};
}
/* ---- the FFT: radix-2 decimation in time with a twiddle table (the
   structure of fourier.html's, tabled rather than recurred) ---- */
const FFT_TABLES={};
function fftTables(n){
  if(FFT_TABLES[n]) return FFT_TABLES[n];
  const bits=Math.round(Math.log2(n)), rev=new Uint32Array(n), c=new Float64Array(n/2), s=new Float64Array(n/2);
  for(let i=0;i<n;i++){ let r=0; for(let b=0;b<bits;b++) if(i&(1<<b)) r|=1<<(bits-1-b); rev[i]=r; }
  for(let k=0;k<n/2;k++){ c[k]=Math.cos(-TAU*k/n); s[k]=Math.sin(-TAU*k/n); }
  return FFT_TABLES[n]={rev,c,s};
}
function fftInPlace(re,im){
  const n=re.length, T=fftTables(n);
  for(let i=0;i<n;i++){ const r=T.rev[i]; if(r>i){ let t=re[i]; re[i]=re[r]; re[r]=t; t=im[i]; im[i]=im[r]; im[r]=t; } }
  for(let len=2;len<=n;len<<=1){
    const half=len>>1, step=n/len;
    for(let i=0;i<n;i+=len) for(let k=0;k<half;k++){
      const wr=T.c[k*step], wi=T.s[k*step], a=i+k, b=a+half;
      const vr=re[b]*wr-im[b]*wi, vi=re[b]*wi+im[b]*wr;
      re[b]=re[a]-vr; im[b]=im[a]-vi; re[a]+=vr; im[a]+=vi;
    }
  }
}
function fft2(re,im,n){
  const rr=new Float64Array(n), ri=new Float64Array(n);
  for(let j=0;j<n;j++){ for(let i=0;i<n;i++){ rr[i]=re[j*n+i]; ri[i]=im[j*n+i]; }
    fftInPlace(rr,ri); for(let i=0;i<n;i++){ re[j*n+i]=rr[i]; im[j*n+i]=ri[i]; } }
  for(let i=0;i<n;i++){ for(let j=0;j<n;j++){ rr[j]=re[j*n+i]; ri[j]=im[j*n+i]; }
    fftInPlace(rr,ri); for(let j=0;j<n;j++){ re[j*n+i]=rr[j]; im[j*n+i]=ri[j]; } }
}
/* the O(N^2)-per-bin direct sum, for the cross-check */
function dft2At(t,n,k1,k2){
  let sr=0, si=0;
  for(let j=0;j<n;j++) for(let i=0;i<n;i++){ const v=t[j*n+i]; if(v===0) continue;
    const a=-TAU*((k1*i+k2*j)%n)/n; sr+=v*Math.cos(a); si+=v*Math.sin(a); }
  return [sr,si];
}
/* the pattern: |F| shifted so bin (0,0) sits at pixel (128,128); PhET's
   display value log(0.01|F| + 1)/log(0.01 max + 1); the intensity |F|^2/max^2 */
function diffract(t){
  const n=DIF.N, re=Float64Array.from(t), im=new Float64Array(n*n), mag=new Float64Array(n*n), h=n/2;
  fft2(re,im,n);
  let mx=0;
  for(let j=0;j<n;j++) for(let i=0;i<n;i++){
    const v=Math.sqrt(re[j*n+i]*re[j*n+i]+im[j*n+i]*im[j*n+i]);
    mag[((j+h)%n)*n+(i+h)%n]=v; if(v>mx) mx=v; }
  return {mag,max:mx,dc:mag[h*n+h]};
}
function phetDisplay(m,max){ return max>0?Math.log(0.01*m+1)/Math.log(0.01*max+1):0; }
/* the analytic far field along the horizontal cut (ky = 0), I/I0 at sin(theta),
   for the apertures that have one; null for the rest */
function fraunhoferCut(P,lam,sinT,rendered){
  const lm=lam*1e-6;
  if(P.ap==='ellipse') return airyI(PI*P.ellD*sinT/lm);
  if(P.ap==='rect'){ const w=rendered?2*rendered.iw*DIF.PX/rendered.s:P.recW; return sinc2(PI*w*sinT/lm); }
  if(P.ap==='gauss'){ const q=TAU*P.gauSx*sinT/lm; return Math.exp(-q*q); }
  if(P.ap==='slits') return sinc2(PI*P.sltW*sinT/lm)*gratingFactor(PI*P.sltD*sinT/lm,Math.round(P.sltN));
  return null;
}
/* the exact discrete answer for the pixel-snapped rectangle: a box of M ones
   transforms to the Dirichlet kernel sin(pi k M/N)/sin(pi k/N) */
function dirichlet(k,M,N){
  if(k%N===0) return M;
  return Math.sin(PI*k*M/N)/Math.sin(PI*k/N);
}

/* ================================================================== *
 *  two sources: the geometry of the path difference                   *
 *  Sources at (0, -d/2) and (0, +d/2); a point (x, y) has r1, r2 and   *
 *  path difference r1 - r2 = Delta.  Delta = const is a hyperbola with *
 *  foci at the sources: y^2/a^2 - x^2/b^2 = 1, a = Delta/2,            *
 *  b^2 = d^2/4 - a^2, asymptotic to sin(theta) = Delta/d.  The nodal   *
 *  lines are Delta = (m + 1/2) lambda with |Delta| < d.                *
 * ================================================================== */
function nodalCount(dOverLam){ return 2*Math.max(0,Math.ceil(dOverLam-0.5)); }
function hyperY(d,Del,L){ const a=Del/2, b2=d*d/4-a*a; return a*Math.sqrt(1+L*L/b2); }
function farY(d,Del,L){ const a=Del/2; return L*a/Math.sqrt(d*d/4-a*a); }
/* each source a 2-D cylindrical wave e^{ikr}/sqrt(r) (the far form of the 2-D
   Green's function, kr >> 1): the time-averaged intensity at (x, y) */
function twoSourceI(x,y,d,k){
  const r1=Math.hypot(x,y+d/2), r2=Math.hypot(x,y-d/2);
  return 1/r1+1/r2+2*Math.cos(k*(r1-r2))/Math.sqrt(r1*r2);
}
/* the interference factor: I divided by the two waves' own intensities,
   1 + 2 cos k(r1 - r2) sqrt(r1 r2)/(r1 + r2), in [0, 2] */
function fringeFactor(x,y,d,k){ const r1=Math.hypot(x,y+d/2), r2=Math.hypot(x,y-d/2); return twoSourceI(x,y,d,k)/(1/r1+1/r2); }
/* Fraunhofer: cos^2(pi d sin(theta)/lambda), theta seen from the midpoint */
function twoSourceFar(x,y,d,k){ const c=Math.cos(k*d*y/(2*Math.hypot(x,y))); return c*c; }

/* ---- the theory curves for the lattice's own screen ------------------
   Slits: the 2-D Rayleigh-Sommerfeld integral for Dirichlet data on the
   barrier column (exactly what the lattice imposes), in its far-zone form
   E(P) ~ sum over open cells of (X/r) e^{ikr}/sqrt(r), X the barrier-to-screen
   distance; and the Fraunhofer sinc^2 cos^2 seen from the barrier's centre.
   Two sources: twoSourceI at the screen.  All normalised to their peak. */
function screenTheory(R){
  const S=SCENES[R.scene], dx=sceneDx(S), L=R.lat, mid=(L.ny-1)/2, col=L.nx-L.pad-1;
  const rows=L.ny-2*L.pad, k=TAU/waveLen(S,R.f), exact=new Float64Array(rows), far=new Float64Array(rows);
  if(R.mode==='plane'){
    if(R.plane.barrier==='none') { exact.fill(1); far.fill(1); return {exact,far}; }
    const X=(col-R.plane.bcol)*dx, open=[];
    for(let j=0;j<L.ny;j++) if(slitOpen(R,j)) open.push((j-mid)*dx);
    const g=slitCells(R), a=g.a*dx, dd=g.d*dx;
    for(let r=0;r<rows;r++){
      const ys=(L.pad+r-mid)*dx; let er=0, ei=0;
      for(const yj of open){ const rr=Math.hypot(X,ys-yj), w=X/(rr*Math.sqrt(rr)); er+=w*Math.cos(k*rr); ei+=w*Math.sin(k*rr); }
      exact[r]=er*er+ei*ei;
      const sn=ys/Math.hypot(X,ys);
      far[r]=sinc2(k*a*sn/2)*(R.plane.barrier==='two'?Math.pow(Math.cos(k*dd*sn/2),2):1);
    }
  } else {
    const rs=runSourceRows(R), X=(col-srcCol(L))*dx;
    if(rs.length===2&&R.src[0]&&R.src[1]){
      const d=(rs[1]-rs[0])*dx;
      for(let r=0;r<rows;r++){ const ys=(L.pad+r-mid)*dx; exact[r]=twoSourceI(X,ys,d,k); far[r]=twoSourceFar(X,ys,d,k); }
    } else {
      const on=rs.filter((_,q)=>R.src[q]), y0=on.length?(on[0]-mid)*dx:0;
      for(let r=0;r<rows;r++){ const ys=(L.pad+r-mid)*dx, rr=Math.hypot(X,ys-y0); exact[r]=on.length?1/rr:0; far[r]=on.length?1:0; }
    }
  }
  const nm=a=>{ let m=0; for(const v of a) m=Math.max(m,v); if(m>0) for(let q=0;q<a.length;q++) a[q]/=m; };
  nm(exact); nm(far);
  return {exact,far};
}
