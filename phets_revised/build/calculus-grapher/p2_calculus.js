
/* ================================================================== *
 *  the model: PhET's grid and curve shapes, and an EXACT discrete     *
 *  calculus on top of them                                            *
 *                                                                     *
 *  Every constant in this block is PhET's, read out of its build 1.1.1 *
 *  by build/calculus-grapher/derive.py (see refvals.txt); selfTest     *
 *  asserts each against REF, so none of them can drift.               *
 * ================================================================== */
const XMIN=0, XMAX=10;                 /* PhET: CURVE_X_RANGE */
const NPTS=1251;                       /* PhET: numberOfPoints */
const XLEN=XMAX-XMIN;
const DX=XLEN/(NPTS-1);
const TYPICAL_Y=0.1*XLEN;              /* PhET: TYPICAL_Y */
const SMOOTH_SIGMA=0.005*XLEN;         /* PhET: smoothingStandardDeviation */
const EDGE_SLOPE=0.04*XLEN;            /* PhET: edgeSlopeFactor */
const MAX_TILT=25;                     /* PhET: maxTilt */
const W_MIN=0.1*XLEN, W_MAX=0.5*XLEN, W_DEF=0.2*XLEN;   /* PhET: CURVE_MANIPULATION_WIDTH_RANGE */
const Y_MIN=-2, Y_MAX=2;               /* PhET: CURVE_MANIPULATION_Y_RANGE */
const SLOPE_MAX=8;                     /* PhET: SLOPE_OF_TANGENT_MODEL_RANGE */
const AREA_MAX=0.8*XLEN*TYPICAL_Y;     /* PhET: NET_SIGNED_AREA_MODEL_RANGE */
const MAX_UNDO=20;                     /* PhET: MAX_UNDO */
const FREEFORM_W=XLEN/40;              /* PhET: the hill a single freeform click lays down */
const BLEND_EPS=1e-8;                  /* PhET: below this weight the saved value is kept */
const SMOOTH_W=0.999;                  /* PhET: above this weight the point becomes smooth */
const REGION_ZERO=0.001;               /* PhET: isRegionZero's tolerance */

const XG=new Float64Array(NPTS);
for(let i=0;i<NPTS;i++) XG[i]=XMIN+i*DX;
const XMID=new Float64Array(NPTS-1);            /* the cell centres, where f' lives */
for(let i=0;i<NPTS-1;i++) XMID[i]=XG[i]+DX/2;

/* ------------------------------------------------------------------ *
 *  the discrete calculus
 *
 *  f is stored at the NODES and drawn as the polyline through them, so
 *  the curve the sim shows IS the piecewise-linear interpolant.  Its
 *  exact derivative is constant on each cell and its exact integral is
 *  the cumulative trapezium, and those two operators are inverse to
 *  each other in floating point:
 *
 *      integCells(deriv(f))[i] = f[i] - f[0]                (exactly)
 *      deriv(integCells(g))[i] = g[i]                       (exactly)
 *      deriv(integ(f))[i]      = (f[i] + f[i+1])/2          (exactly)
 *
 *  The third line is the fundamental theorem on this grid: differentiating
 *  the integral returns f AT THE CELL MIDPOINT, and for a straight segment
 *  the midpoint value is exactly the mean of the two ends.  Nothing is
 *  approximated; selfTest asserts all three to 2e-12 over random curves.
 *
 *  PhET instead puts f' on the NODES as the mean of the two one-sided
 *  slopes.  That is a perfectly good teaching choice and differs by
 *  O(dx^2 f''), but it is not the inverse of its own trapezium integral:
 *  phetDeriv(integ(f))[i] is exactly (f[i-1] + 2 f[i] + f[i+1])/4, the
 *  [1,2,1]/4 smoothing of f.  phetDeriv is kept here so THE GRID view can
 *  show that identity rather than assert it from memory.
 * ------------------------------------------------------------------ */
function derivOf(f,n,dx){
  n=n||f.length; dx=dx===undefined?DX:dx;
  const d=new Float64Array(n-1);
  for(let i=0;i<n-1;i++) d[i]=(f[i+1]-f[i])/dx;
  return d;
}
function integOf(f,n,dx){
  n=n||f.length; dx=dx===undefined?DX:dx;
  const F=new Float64Array(n);
  for(let i=1;i<n;i++) F[i]=F[i-1]+0.5*(f[i]+f[i-1])*dx;
  return F;
}
function integCells(g,dx){
  dx=dx===undefined?DX:dx;
  const F=new Float64Array(g.length+1);
  for(let i=1;i<=g.length;i++) F[i]=F[i-1]+g[i-1]*dx;
  return F;
}
function deriv2Of(f,n,dx){
  n=n||f.length; dx=dx===undefined?DX:dx;
  const d=derivOf(f,n,dx), o=new Float64Array(n);
  for(let i=1;i<n-1;i++) o[i]=(d[i]-d[i-1])/dx;
  o[0]=o[1]; o[n-1]=o[n-2];
  return o;
}
function phetDeriv(f,n,dx){
  n=n||f.length; dx=dx===undefined?DX:dx;
  const o=new Float64Array(n);
  for(let i=1;i<n-1;i++) o[i]=0.5*((f[i]-f[i-1])/dx+(f[i+1]-f[i])/dx);
  o[0]=(f[1]-f[0])/dx; o[n-1]=(f[n-1]-f[n-2])/dx;
  return o;
}

/* ------------------------------------------------------------------ *
 *  PhET's eight curve-manipulation modes
 *  hill      exp(-((x-x0)/(w/2sqrt2))^2)           a Gaussian of sd w/4
 *  triangle  y - sign(dy) (TYPICAL_Y/(w/2)) |x-x0| kept where it wins
 *  pedestal  1 inside w-2e, exp(-((d)/e)^4) outside (e = edgeSlopeFactor)
 *  parabola  y - sign(dy) TYPICAL_Y (2/w)^2 (x-x0)^2, kept where it wins
 *  sinusoid  y cos(2 pi (x0-x)/lambda), lambda = 2 pi w / w_default,
 *            seven half-periods wide, cosine-squared taper of lambda/8
 *  freeform  drag the curve point by point
 *  tilt      pivot about the left edge, refused past |slope| = maxTilt
 *  shift     move the whole curve rigidly
 * ------------------------------------------------------------------ */
const MODES=[{id:'hill',name:'hill'},{id:'triangle',name:'triangle'},
             {id:'pedestal',name:'pedestal'},{id:'parabola',name:'parabola'},
             {id:'sinusoid',name:'sinusoid'},{id:'freeform',name:'freeform'},
             {id:'tilt',name:'tilt'},{id:'shift',name:'shift'}];
const SHAPE_MODES=['hill','triangle','pedestal','parabola','sinusoid'];

function idxAt(x,n){
  n=n||NPTS;
  const t=(x-XMIN)/XLEN;
  return clamp(Math.round(t*(n-1)),0,n-1);
}
function cellAt(x,n,dx){
  n=n||NPTS; dx=dx===undefined?DX:dx;
  return clamp(Math.floor((x-XMIN)/dx),0,n-2);
}
function gridOf(n){
  const dx=XLEN/(n-1), x=new Float64Array(n);
  for(let i=0;i<n;i++) x[i]=XMIN+i*dx;
  return {n,dx,x};
}
const GRID=gridOf(NPTS);

function regionZero(fs,g,a,b){
  for(let i=0;i<g.n;i++){
    const xx=g.x[i];
    if(xx<a||xx>b) continue;
    if(Math.abs(fs[i])>=REGION_ZERO) return false;
  }
  return true;
}

/* one shape laid on a SAVED curve.  Returns the new node values and the new
   corner flags; PhET's own rule for the flags is kept -- a point the new
   shape owns (weight > 0.999) becomes smooth, otherwise it keeps the type it
   had, and the places where a piecewise shape meets the old curve are cusps. */
function manipulate(fs,cs,mode,w,x0,y,g){
  g=g||GRID;
  const n=g.n, x=g.x, dx=g.dx;
  const i0=idxAt(x0,n), xc=x[i0];
  const f=new Float64Array(n), c=new Uint8Array(n);
  if(mode==='hill'||mode==='pedestal'){
    let P;
    if(mode==='hill'){
      const sd=w/(2*Math.sqrt(2));
      P=i=>Math.exp(-Math.pow((x[i]-xc)/sd,2));
    } else {
      const e=EDGE_SLOPE, s=w-2*e;
      P=i=>{
        const u=x[i]-xc;
        if(Math.abs(u)<s/2) return 1;
        const cen=u<=0?xc-s/2:xc+s/2;
        return Math.exp(-Math.pow((x[i]-cen)/e,4));
      };
    }
    for(let i=0;i<n;i++){
      const t=P(i);
      f[i]=t>BLEND_EPS?t*y+(1-t)*fs[i]:fs[i];
      c[i]=t>SMOOTH_W?0:cs[i];
    }
  } else if(mode==='triangle'||mode==='parabola'){
    const delta=y-fs[i0];
    const sg=delta>0?1:(delta<0?-1:0);
    const s=mode==='triangle'?TYPICAL_Y/(w/2):TYPICAL_Y*Math.pow(2/w,2);
    const shape=mode==='triangle'
      ? i=>y-sg*s*Math.abs(x[i]-xc)
      : i=>y-sg*s*Math.pow(x[i]-xc,2);
    let prev=null;
    for(let i=0;i<n;i++){
      const v=shape(i);
      const win=(delta>0&&v>fs[i])||(delta<0&&v<fs[i]);
      f[i]=win?v:fs[i];
      c[i]=win?0:cs[i];
      if(prev!==null&&prev!==win){ c[i]=1; c[i-1]=1; }
      prev=win;
    }
    if(mode==='triangle'){ c[i0]=1; if(i0+1<n) c[i0+1]=1; }
  } else if(mode==='sinusoid'){
    const lam=2*PI*w/W_DEF;
    const o=lam/2*7, a=lam/8;
    const lr=xc+o/2, hl=xc-o/2;
    const cR=lr>XMAX?lr:x[idxAt(lr,n)];
    const uL=hl<XMIN?hl:x[idxAt(hl,n)];
    const dR=cR-a, pL=uL+a;
    const gz=regionZero(fs,g,uL,pL), mz=regionZero(fs,g,dR,cR);
    const k=2*PI/lam;
    for(let i=0;i<n;i++){
      const xx=x[i];
      let t;
      if(xx>=pL&&xx<=dR) t=1;
      else if(xx>uL&&xx<pL) t=gz?1:Math.pow(Math.cos(PI/2*(xx-pL)/Math.abs(uL-pL)),2);
      else if(xx>dR&&xx<cR) t=mz?1:Math.pow(Math.cos(PI/2*(xx-dR)/Math.abs(cR-dR)),2);
      else t=0;
      f[i]=t*(y*Math.cos(k*(xc-xx)))+(1-t)*fs[i];
      c[i]=t>SMOOTH_W?0:cs[i];
    }
    if(gz&&hl>XMIN){ const j=idxAt(uL,n); c[j]=1; if(j+1<n) c[j+1]=1; }
    if(mz&&lr<XMAX){ const j=idxAt(cR,n); c[j]=1; if(j-1>=0) c[j-1]=1; }
  } else if(mode==='tilt'){
    const r=xc-x[0];
    f.set(fs); c.set(cs);
    if(r!==0&&Math.abs((y-fs[0])/r)<MAX_TILT){
      const t=(y-fs[i0])/r;
      for(let i=0;i<n;i++) f[i]=fs[i]+t*(x[i]-x[0]);
    }
  } else if(mode==='shift'){
    const delta=y-fs[i0];
    for(let i=0;i<n;i++) f[i]=fs[i]+delta;
    c.set(cs);
  } else {
    throw new Error('unsupported curve manipulation: '+mode);
  }
  return {f,c};
}

/* freeform: PhET sets the dragged point and joins it to the previous one by
   a straight run of nodes.  A single click with no previous point lays down a
   hill of PhET's own FREEFORM_W instead, so a tap still does something. */
function freeformStroke(f,c,xNow,yNow,xPrev,yPrev){
  const i=idxAt(xNow);
  f[i]=yNow; c[i]=1;
  if(xPrev===null||xPrev===undefined) return;
  const j=idxAt(xPrev);
  if(j===i) return;
  const lo=Math.min(i,j), hi=Math.max(i,j);
  const ya=(lo===i)?yNow:yPrev, yb=(hi===i)?yNow:yPrev;
  for(let k=lo;k<=hi;k++){
    const t=(k-lo)/(hi-lo);
    f[k]=(1-t)*ya+t*yb;
    c[k]=(k===lo||k===hi)?1:0;
  }
}

/* PhET's smoothing: a Gaussian of sd = smoothingStandardDeviation, sampled
   every dx, truncated at 3 sd and renormalised, with the ends clamped.  The
   renormalisation is what makes a constant survive exactly. */
function smoothCurve(f,n,dx,sigma){
  n=n||f.length; dx=dx===undefined?DX:dx; sigma=sigma===undefined?SMOOTH_SIGMA:sigma;
  const w0=1/(sigma*Math.sqrt(2*PI));
  const kern=t=>w0*Math.exp(-0.5*Math.pow(t/sigma,2));
  let K=0;
  while((K+1)*dx<=3*sigma) K++;
  const ws=new Float64Array(K+1);
  let tot=kern(0);
  ws[0]=tot;
  for(let k=1;k<=K;k++){ ws[k]=kern(k*dx); tot+=2*ws[k]; }
  const out=new Float64Array(n);
  for(let i=0;i<n;i++){
    let acc=f[i]*ws[0];
    for(let k=1;k<=K;k++){
      const a=clamp(i+k,0,n-1), b=clamp(i-k,0,n-1);
      acc+=ws[k]*(f[a]+f[b]);
    }
    out[i]=acc/tot;
  }
  /* w0 and tot are returned because the smoothed curve alone cannot see them:
     the weights are divided by their own sum, so PhET's 1/(sigma sqrt(2 pi))
     cancels EXACTLY and a mutant on it would be an equivalent mutant that the
     sweep reports as a survivor (Known-bad: a survivor that is equivalent is
     telling you the code carries meaning its tests do not).  selfTest pins
     both against derive.py, which makes the constant load-bearing again. */
  return {f:out,taps:K,w0:ws[0],tot};
}

/* ------------------------------------------------------------------ *
 *  reading the curve between the nodes, and the two tools
 * ------------------------------------------------------------------ */
function valueAt(f,x){
  const i=cellAt(x), t=(x-XG[i])/DX;
  return f[i]+t*(f[i+1]-f[i]);
}
/* the tangent tool: the slope of f at x IS the cell's own slope, because the
   drawn curve is straight across a cell.  The line it draws therefore passes
   exactly through both nodes of that cell, which is what selfTest asserts --
   a check on the DRAWN object, not a restatement of the lookup. */
function tangentAt(f,d,x){
  const i=cellAt(x);
  return {i,slope:d[i],y:valueAt(f,x),x0:XG[i],y0:f[i],x1:XG[i+1],y1:f[i+1]};
}
function integAt(f,F,x){
  const i=cellAt(x), t=(x-XG[i])/DX;
  const yv=f[i]+t*(f[i+1]-f[i]);
  return F[i]+0.5*(f[i]+yv)*(t*DX);
}
/* the area tool.  Every cell is split at its zero crossing and the two halves
   are counted separately, so this is a DIFFERENT algorithm from the running
   trapezium in integOf -- and net = pos - neg must still equal the integral
   curve, which is the cross-check the view exists to make. */
function signedAreas(f,xend){
  let pos=0,neg=0;
  const add=A=>{ if(A>=0) pos+=A; else neg-=A; };
  const last=cellAt(xend);
  for(let i=0;i<last;i++){
    const a=f[i], b=f[i+1];
    if(a*b<0){ const t=a/(a-b); add(0.5*a*(t*DX)); add(0.5*b*((1-t)*DX)); }
    else add(0.5*(a+b)*DX);
  }
  const t=(xend-XG[last])/DX;
  if(t>0){
    const a=f[last], b=f[last]+t*(f[last+1]-f[last]);
    if(a*b<0){ const tz=a/(a-b); add(0.5*a*(tz*t*DX)); add(0.5*b*((1-tz)*t*DX)); }
    else add(0.5*(a+b)*t*DX);
  }
  return {pos,neg,net:pos-neg};
}
/* the corners of a curve, from PhET's own flags rather than a threshold on the
   slope: a threshold that calls a narrow pedestal a corner is a threshold that
   is measuring the width slider.  Consecutive flagged nodes are one corner. */
function cornerList(c,d,maxN){
  const out=[];
  for(let i=1;i<c.length-1;i++){
    if(!c[i]) continue;
    if(out.length&&i-out[out.length-1].b<=1){ out[out.length-1].b=i; continue; }
    out.push({a:i,b:i});
    if(maxN&&out.length>=maxN) break;
  }
  for(const o of out){
    /* PhET flags a corner on a PAIR of nodes, and the cells between them are
       the transition: at a junction that cell carries a slope belonging to
       neither side (the corner falls inside it).  So the left limit is the
       cell ENDING at the first flagged node and the right limit the cell
       STARTING at the last one -- the transition is skipped by construction
       rather than by an offset chosen to make one shape come out right. */
    o.i=o.a;
    o.x=XG[o.a];
    o.left=d[Math.max(o.a-1,0)];
    o.right=d[Math.min(o.b,d.length-1)];
    o.jump=o.right-o.left;
  }
  return out;
}

/* ------------------------------------------------------------------ *
 *  the closed forms, for the analysis views
 * ------------------------------------------------------------------ */
/* erf by the all-positive series
      erf(z) = (2z/sqrt(pi)) e^{-z^2} SUM_n (2z^2)^n / (1.3.5...(2n+1)),
   which has no cancellation anywhere (the alternating Maclaurin series loses
   every digit past z ~ 3).  derive.py pins it against scipy over -6..6. */
function erf(z){
  if(z<0) return -erf(-z);
  if(z>6) return 1;
  let t=1,s=1;
  for(let n=1;n<200;n++){
    t*=2*z*z/(2*n+1);
    s+=t;
    if(t<1e-18*s) break;
  }
  return 2*z/Math.sqrt(PI)*Math.exp(-z*z)*s;
}

/* Gauss-Legendre nodes and weights, found by Newton on the Legendre
   polynomial rather than typed in: a hand-copied coefficient table is the
   same failure as a table quoted from memory (Known-bad, standard_candle). */
function gaussLegendre(n){
  const xs=new Float64Array(n), ws=new Float64Array(n);
  for(let i=0;i<n;i++){
    let z=Math.cos(PI*(i+0.75)/(n+0.5)), p0=0, dp=0;
    for(let it=0;it<100;it++){
      let a=1,b=0;
      for(let j=0;j<n;j++){ const cc=b; b=a; a=((2*j+1)*z*b-j*cc)/(j+1); }
      p0=a; dp=n*(z*a-b)/(z*z-1);
      const step=p0/dp; z-=step;
      if(Math.abs(step)<1e-16) break;
    }
    let a=1,b=0;
    for(let j=0;j<n;j++){ const cc=b; b=a; a=((2*j+1)*z*b-j*cc)/(j+1); }
    dp=n*(z*a-b)/(z*z-1);
    xs[i]=z; ws[i]=2/((1-z*z)*dp*dp);
  }
  return {xs,ws};
}
const GL=gaussLegendre(12);
function quadGL(fn,a,b,panels){
  panels=panels||8;
  let acc=0;
  const hstep=(b-a)/panels;
  for(let p=0;p<panels;p++){
    const lo=a+p*hstep, mid=lo+hstep/2, half=hstep/2;
    for(let i=0;i<GL.xs.length;i++) acc+=GL.ws[i]*fn(mid+half*GL.xs[i])*half;
  }
  return acc;
}

/* (value, exact derivative, exact integral from XMIN, the corner positions)
   for one shape laid on an EMPTY curve.  The integrals are elementary for
   four of the five; the pedestal's antiderivative is an incomplete gamma, so
   it is taken by Gauss-Legendre broken at the joins -- exact to 1e-15 for a
   smooth integrand, and derive.py pins it against scipy's gammainc. */
/* The grid matters here and it is easy to miss: the shape's centre is SNAPPED
   to a node, so a closed form built on the shipped 1251-point grid is centred
   somewhere else on a coarser one.  The first refinement ladder measured 1.9e-2
   at 313 cells against 4.4e-5 at 1250 -- the wrong way round -- and that was the
   whole cause.  Pass the grid the shape was built on. */
function shapeClosed(mode,w,x0,y,g){
  g=g||GRID;
  const xc=g.x[idxAt(x0,g.n)];
  if(mode==='hill'){
    const a=8/(w*w), k=0.5*Math.sqrt(PI/a), rt=Math.sqrt(a);
    return {xc,breaks:[],
      g:x=>y*Math.exp(-a*(x-xc)*(x-xc)),
      gp:x=>-2*a*(x-xc)*y*Math.exp(-a*(x-xc)*(x-xc)),
      G:x=>y*k*(erf(rt*(x-xc))-erf(rt*(XMIN-xc)))};
  }
  if(mode==='triangle'){
    const s=TYPICAL_Y/(w/2)*(y>0?1:-1), r=Math.abs(y)/Math.abs(s);
    const prim=u=>y*u-s*Math.sign(u)*u*u/2;
    const lo=Math.max(XMIN-xc,-r);
    return {xc,breaks:[xc-r,xc,xc+r],
      g:x=>Math.abs(x-xc)<r?y-s*Math.abs(x-xc):0,
      gp:x=>Math.abs(x-xc)<r?-s*Math.sign(x-xc):0,
      G:x=>prim(clamp(x-xc,-r,r))-prim(lo)};
  }
  if(mode==='parabola'){
    const s=TYPICAL_Y*Math.pow(2/w,2)*(y>0?1:-1), r=Math.sqrt(Math.abs(y)/Math.abs(s));
    const prim=u=>y*u-s*u*u*u/3;
    const lo=Math.max(XMIN-xc,-r);
    return {xc,breaks:[xc-r,xc+r],
      g:x=>Math.abs(x-xc)<r?y-s*(x-xc)*(x-xc):0,
      gp:x=>Math.abs(x-xc)<r?-2*s*(x-xc):0,
      G:x=>prim(clamp(x-xc,-r,r))-prim(lo)};
  }
  if(mode==='pedestal'){
    const e=EDGE_SLOPE, half=(w-2*e)/2;
    const P=x=>{ const u=Math.abs(x-xc); return u<half?1:Math.exp(-Math.pow((u-half)/e,4)); };
    const gg=x=>y*P(x);
    return {xc,breaks:[],
      g:gg,
      gp:x=>{ const u=Math.abs(x-xc);
              if(u<half) return 0;
              const q=(u-half)/e;
              return y*(-4*q*q*q/e)*Math.exp(-q*q*q*q)*Math.sign(x-xc); },
      G:x=>{ const cuts=[XMIN,xc-half,xc,xc+half,x].filter(v=>v>XMIN&&v<x);
             const pts=[XMIN].concat(cuts.sort((p,q)=>p-q)).concat([x]);
             let acc=0;
             for(let i=0;i<pts.length-1;i++) if(pts[i+1]>pts[i]) acc+=quadGL(gg,pts[i],pts[i+1],6);
             return acc; }};
  }
  if(mode==='sinusoid'){
    const lam=2*PI*w/W_DEF, o=lam/2*7;
    const lr=xc+o/2, hl=xc-o/2;
    const cR=lr>XMAX?lr:g.x[idxAt(lr,g.n)], uL=hl<XMIN?hl:g.x[idxAt(hl,g.n)];
    const k=2*PI/lam;
    const prim=z=>-y/k*Math.sin(k*(xc-z));
    const lo=Math.min(Math.max(XMIN,uL),cR);
    return {xc,breaks:[uL,cR].filter(v=>v>XMIN&&v<XMAX),
      g:x=>(x>uL&&x<cR)?y*Math.cos(k*(xc-x)):0,
      gp:x=>(x>uL&&x<cR)?y*k*Math.sin(k*(xc-x)):0,
      G:x=>prim(clamp(x,uL,cR))-prim(lo)};
  }
  throw new Error('no closed form for '+mode);
}

/* the exact integral of a closed-form shape at every node, cell by cell with
   Gauss-Legendre and each break used as a panel edge.  This is the SECOND
   route to the same quantity: selfTest asserts it against the elementary
   antiderivatives (hill, triangle, parabola, sinusoid) to 1e-13, which is
   what lets it stand alone for the pedestal, whose antiderivative is an
   incomplete gamma that derive.py evaluates in scipy instead. */
function cumExact(cf,g){
  g=g||GRID;
  const out=new Float64Array(g.n);
  for(let i=0;i<g.n-1;i++){
    const a=g.x[i], b=g.x[i+1];
    let acc=0, lo=a;
    const cuts=cf.breaks.filter(v=>v>a&&v<b).sort((p,q)=>p-q);
    for(const cval of cuts){ acc+=quadGL(cf.g,lo,cval,1); lo=cval; }
    acc+=quadGL(cf.g,lo,b,1);
    out[i+1]=out[i]+acc;
  }
  return out;
}

/* the discretisation error of both operators, for one shape, on a grid N
   times as fine as PhET's.  Cells within 2 dx of a corner and the far tails
   where PhET's 1e-8 blend cuts the shape off are left out: neither is a
   quadrature error, and mixing them in would hide the O(dx^2) rate. */
function gridError(mode,w,x0,y,n){
  const g=gridOf(n);
  const zero=new Float64Array(n), zc=new Uint8Array(n);
  const out=manipulate(zero,zc,mode,w,x0,y,g);
  const cf=shapeClosed(mode,w,x0,y,g);
  const d=derivOf(out.f,n,g.dx), F=integOf(out.f,n,g.dx);
  const Gx=cumExact(cf,g);
  let ed=0, eF=0;
  for(let i=0;i<n-1;i++){
    const xm=g.x[i]+g.dx/2;
    let skip=Math.abs(cf.g(xm))<=1e-6*Math.abs(y);
    for(const b of cf.breaks) if(Math.abs(xm-b)<=2*g.dx) skip=true;
    if(!skip) ed=Math.max(ed,Math.abs(d[i]-cf.gp(xm)));
  }
  for(let i=0;i<n;i++){
    let skip=false;
    for(const b of cf.breaks) if(Math.abs(g.x[i]-b)<=2*g.dx) skip=true;
    if(!skip) eF=Math.max(eF,Math.abs(F[i]-Gx[i]));
  }
  return {n,dx:g.dx,ed,eF};
}
