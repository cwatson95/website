/* ================================================================== *
 *  the optics                                                         *
 *                                                                     *
 *  Conventions, stated once and used everywhere (they are also        *
 *  printed on the canvas and in the panel):                           *
 *                                                                     *
 *    x runs to the RIGHT, the optic sits at x = 0, the object is      *
 *    always at x < 0, y is measured from the optical axis, up is +.   *
 *    d_o = -x_object > 0                     object distance          *
 *    f   > 0 converging (convex lens, concave mirror)                 *
 *        < 0 diverging  (concave lens, convex mirror)                 *
 *    d_i > 0 real image, < 0 virtual.  A lens puts a real image at    *
 *        x = +d_i, a mirror at x = -d_i  (PhET's `sign` = +1 / -1).   *
 *    m   = -d_i/d_o  (negative = inverted)                            *
 *    R   > 0 convex optic, < 0 concave optic (PhET's own sign).       *
 *                                                                     *
 *  Every reference value asserted in selfTest is a printed line of    *
 *  build/geometric-optics/refvals.txt (derive.py).                    *
 * ================================================================== */

/* ---- PhET's values, read out of docs/phets/geometric-optics_en.html
        (build 1.3.16).  Ranges are [min, max, default], centimetres. ---- */
const PHET={
  fLens:[40,120,80], rocLens:[40,120,80], iorLens:[1.2,1.8,1.5], dLens:[60,120,80],
  fMirror:[75,150,90], rocMirror:[150,300,180], dMirror:[60,120,80],
  iorDirectLens:1.5,          /* the direct lens model holds n at 1.5 */
  iorMirror:2,                /* Vm = Range(2,2,2): makes f = R/2 fall out */
  flatF:1e5, flatR:2e5,       /* the flat mirror's stand-in */
  minObjectDist:40,           /* MIN_DISTANCE_FROM_OBJECT_TO_OPTIC */
  minScreenDist:60,           /* MIN_DISTANCE_FROM_OPTIC_TO_PROJECTION_SCREEN */
  maxOffAxis:100,             /* MAX_DISTANCE_FROM_OBJECT_TO_OPTICAL_AXIS */
  framedLens:[-170,27], framedMirror:[-150,72.5],
  arrow1Lens:[-160,60], arrow2Lens:[-125,30],
  arrow1Mirror:[-150,60], arrow2Mirror:[-165,30],
  light1:[-170,20], light2:[-124,-20],
  secondOffset:-56.5,         /* SecondPoint.VERTICAL_OFFSET_RANGE.min */
  screenX:200, screenH:123,
  manyFanDeg:120,             /* LightRays: toRadians(120) */
  arrowMax:80,                /* ArrowObject.MAX_MAGNITUDE */
  rulerH:260, rulerV:160,
  fStep:5, rocStep:5, iorStep:0.05, dStep:5,
  hollywoodPad:100            /* LensShapes: a = (D/2)^2 / (2(|R| + 100)) */
};

/* =============================== the thin optic ==================== */
/* d_i from 1/d_o + 1/d_i = 1/f.  PhET returns 1e7 at d_o = f; the honest
   answer is that the image is at infinity, so this returns Infinity and every
   consumer has to decide what to do about it. */
function imageDistance(f,dO){
  if(dO===f) return Infinity;
  return f*dO/(dO-f);
}
function magnif(f,dO){
  if(dO===0) return 1;
  const di=imageDistance(f,dO);
  return isFinite(di)?-di/dO:-Infinity;
}
/* the residual of the defining equation: the suite asserts this, not the
   formula, so a mutation of the formula cannot hide behind itself */
function lensEqResidual(f,dO,di){ return 1/dO+1/di-1/f; }
/* Newton's form.  x x' = f^2 with x = d_o - f, x' = d_i - f. */
function newtonProduct(f,dO){
  const di=imageDistance(f,dO);
  return (dO-f)*(di-f);
}
const opticSign=kind=>kind==='mirror'?-1:1;

function imagePoint(kind,f,dO,yO){
  const di=imageDistance(f,dO), m=isFinite(di)?-di/dO:-Infinity;
  return {x:opticSign(kind)*di, y:m*yO, di:di, m:m, virtual:di<0};
}

/* =============================== ray transfer ====================== */
/* The whole of paraxial ray optics.  u is the transverse slope of the
   incoming ray (dy/dx, x increasing); u' is the slope of the outgoing ray
   measured along ITS OWN direction of travel, which is +x for a lens and -x
   for a mirror.  It never blows up -- not even at d_o = f. */
function bend(u,h,f){ return u-h/f; }
/* Height of the outgoing ray at signed path length s from the optic.  s < 0
   is the backward extension, which is exactly where a virtual image lives. */
function rayHeightAt(u,h,f,s){ return h+bend(u,h,f)*s; }

/* Where a ray from P in direction d meets the optic plane x = 0.
   Returns null when it never gets there. */
function opticHit(P,d){
  if(!(d[0]>1e-12)) return null;
  const t=-P[0]/d[0];
  if(!(t>0)) return null;
  return {t:t,h:P[1]+t*d[1],u:d[1]/d[0]};
}

/* PhET's four ray modes, as directions leaving the source point.
   marginal : to the centre and to the two rim points
   principal: parallel to the axis, through the centre, through the near F
   many     : a 120-degree fan of 20*(floor(d_o/300)+1) rays
   none     : nothing */
function manyRayCount(dO){ return 20*(Math.floor(Math.abs(dO)/300)+1); }
function rayDirections(mode,P,f,D){
  const dO=-P[0];
  const out=[];
  const norm=v=>{ const L=Math.hypot(v[0],v[1]); return [v[0]/L,v[1]/L]; };
  if(mode==='marginal'){
    out.push(norm([dO,-P[1]]));
    out.push(norm([dO,D/2-P[1]]));
    out.push(norm([dO,-D/2-P[1]]));
  }else if(mode==='principal'){
    out.push([1,0]);
    out.push(norm([dO,-P[1]]));
    /* the ray that crosses the axis at the front focal point x = -f */
    const v=[dO-f,-P[1]];
    if(v[0]<0){ v[0]=-v[0]; v[1]=-v[1]; }
    out.push(norm(v));
  }else if(mode==='many'){
    const half=PHET.manyFanDeg*PI/360, n=manyRayCount(dO), step=2*half/(n-1);
    for(let i=0;i<n;i++){ const a=half-i*step; out.push([Math.cos(a),Math.sin(a)]); }
  }
  return out;
}

/* One ray, traced.  Returns the incoming segment, the outgoing segment and
   (when the image is virtual and the ray was deviated) the dashed backward
   extension that reaches the virtual image.  `reach` is how far past the optic
   the outgoing ray is drawn, in cm of path length. */
function traceRay(kind,f,D,P,d,reach,aperture){
  const hit=opticHit(P,d);
  if(hit===null) return null;
  const sgn=opticSign(kind);
  const inSeg=[[P[0],P[1]],[0,hit.h]];
  const inside=(aperture===false)||(Math.abs(hit.h)<=D/2+1e-9);
  if(!inside){
    /* misses the optic.  A lens lets it through undeviated; a mirror has
       nothing there to reflect it, so the ray simply ends. */
    if(kind==='mirror') return {inSeg:inSeg,outSeg:null,virtSeg:null,h:hit.h,missed:true};
    const s=reach;
    return {inSeg:inSeg,outSeg:[[0,hit.h],[s,hit.h+hit.u*s]],virtSeg:null,h:hit.h,missed:true};
  }
  const up=bend(hit.u,hit.h,f);
  const outSeg=[[0,hit.h],[sgn*reach,hit.h+up*reach]];
  let virtSeg=null;
  const di=imageDistance(f,-P[0]);
  if(isFinite(di)&&di<0) virtSeg=[[0,hit.h],[sgn*di,hit.h+up*di]];
  return {inSeg:inSeg,outSeg:outSeg,virtSeg:virtSeg,h:hit.h,u:hit.u,up:up,missed:false};
}

/* =============================== the lens maker ==================== */
const invR=R=>(isFinite(R)&&R!==0)?1/R:0;
function fThin(n,R1,R2){ return 1/((n-1)*(invR(R1)-invR(R2))); }
function fThick(n,R1,R2,t){
  return 1/((n-1)*(invR(R1)-invR(R2)+(n-1)*t*invR(R1)*invR(R2)/n));
}
/* back focal distance, measured from the REAR vertex */
function backFocal(n,R1,R2,t){
  return fThick(n,R1,R2,t)*(1-(n-1)*t*invR(R1)/n);
}
/* PhET's optic has the same radius on both surfaces, R1 = +R, R2 = -R, so the
   lens maker's equation collapses to |f| = |R| / (2(n-1)).  Its doc/model.md
   prints f = R/(2(1-n)); the code computes the MAGNITUDE this way and puts the
   sign on from the surface type, which is what is done here. */
function phetFocalFromR(R,n){ return Math.abs(R)/(2*(n-1)); }
function phetRFromFocal(f,n){ return 2*Math.abs(f)*(n-1); }

/* the sag of a spherical surface of radius R at height h (h <= |R|) */
function sphereSag(R,h){
  if(!isFinite(R)||R===0) return 0;
  const d=R*R-h*h;
  if(d<0) return NaN;
  return h*h/(R*(1+Math.sqrt(d)/Math.abs(R)));
}
/* PhET's DRAWN half-thickness: a softened sag that never refuses.  Its lens
   artwork uses this, not the true sag -- so at R = 40, D = 120 it happily
   draws a lens whose surfaces could not exist. */
function hollywoodSag(R,D){ return 0.5*(D/2)*(D/2)/(Math.abs(R)+PHET.hollywoodPad); }

/* =============================== PhET's guides ===================== */
/* A guide is hinged at the rim of the lens and turns the ray by a FIXED angle.
   s = +1 top, -1 bottom; f is SIGNED; r = D/(4f). */
function guideRatio(f,D){ return D/(4*f); }
function guideTurn(surface,f,D,s){
  const r=guideRatio(f,D);
  return surface==='convex' ? -s*(2*Math.atan(r))
                            : -s*(Math.atan(3*r)-Math.atan(r));
}
function guideAngles(surface,f,D,obj,s){
  const fy=s*D/2;
  const inc=Math.atan2(obj[1]-fy,obj[0]-0);
  return {fulcrum:[0,fy],incident:inc,transmitted:inc+PI+guideTurn(surface,f,D,s),
          r:guideRatio(f,D)};
}
/* where the two transmitted guides cross -- PhET's approximation to the image */
function guideCross(surface,f,D,obj){
  const A=guideAngles(surface,f,D,obj,1), B=guideAngles(surface,f,D,obj,-1);
  const m1=Math.tan(A.transmitted), m2=Math.tan(B.transmitted);
  if(m1===m2) return {x:Infinity,y:Infinity};
  const y1=D/2, y2=-D/2;
  const x=(y2-y1)/(m1-m2);
  return {x:x,y:y1+m1*x};
}
/* the same pair of rays bent by the SLOPE law instead of by a rotation.  This
   one is exact for every object, which is the whole point of the comparison. */
function slopeCross(f,D,dO,yO){
  const h1=D/2, h2=-D/2;
  const u1=bend((h1-yO)/dO,h1,f), u2=bend((h2-yO)/dO,h2,f);
  /* the heights come back with the crossing: ANY two distinct rays from one
     object point meet at the image, so the crossing alone cannot say which
     rays were used -- and the whole point of this pair is that they are the
     guides' own fulcrum heights. */
  if(u1===u2) return {x:Infinity,y:Infinity,h1:h1,h2:h2};
  const x=(h2-h1)/(u1-u2);
  return {x:x,y:h1+u1*x,h1:h1,h2:h2};
}
/* the turn an ideal thin optic gives the ray that strikes the fulcrum height */
function idealTurn(f,dO,yO,D,s){
  const h=s*D/2, u=(h-yO)/dO;
  return Math.atan(bend(u,h,f))-Math.atan(u);
}

/* =============================== the light spot ==================== */
/* Where the ray from a rim point through the image crosses the screen plane.
   The optic is at x = 0 -- PhET fixes it there and so does this file -- so the
   rim's x never appears; carrying it would be dead generality that no test can
   reach. */
function spotEdge(screenX,rimY,img){
  const n=(img.x===0)?1e7:screenX/img.x;
  return rimY+(img.y-rimY)*n;
}
function lightSpot(screenX,D,f,dO,yO){
  const img=imagePoint('lens',f,dO,yO);
  const yt=spotEdge(screenX,D/2,img), yb=spotEdge(screenX,-D/2,img);
  return {y:0.5*(yt+yb),diameter:Math.abs(yt-yb),top:yt,bottom:yb};
}
/* the same diameter in closed form: the cone from the rim to the image,
   continued to the screen.  Asserted against the two-ray construction. */
function spotDiameterClosed(screenX,D,f,dO){
  const di=imageDistance(f,dO);
  return D*Math.abs(screenX-di)/Math.abs(di);
}
/* PhET's own brightness formula -- a lens-diameter term times 14/diameter,
   clamped to [0,1].  It is not a radiometric calculation and the canvas says
   so where the spot is drawn. */
function spotIntensity(spotD,opticD){
  if(spotD===0) return 0;
  const lo=PHET.dLens[0], hi=PHET.dLens[1];
  const k=0.5+(1-0.5)*(opticD-lo)/(hi-lo);
  return clamp(k*14/spotD,0,1);
}

/* ==================== the real lens: exact ray tracing =============
   Two spherical surfaces, the front vertex at z = 0 and the rear at z = t.
   A ray is [y, z] with z along the axis.  Nothing below is paraxial: the
   paraxial formulas above are checked AGAINST this, in the limit, rather
   than used by it.  (The intersection is the closed-form sphere root; a
   Newton-on-the-sag route is implemented beside it and selfTest asserts the
   two agree, which is what stops a quadratic-root sign slip.) ============ */
function hitSphere(p,d,z0,R,semi){
  if(!isFinite(R)||R===0){
    if(Math.abs(d[1])<1e-15) return null;
    const t=(z0-p[1])/d[1];
    if(!(t>1e-12)) return null;
    const q=[p[0]+t*d[0],z0];
    return Math.abs(q[0])<=semi?q:null;
  }
  const cz=z0+R;
  const oy=p[0], oz=p[1]-cz;
  const b=2*(oy*d[0]+oz*d[1]);
  const c=oy*oy+oz*oz-R*R;
  const disc=b*b-4*c;
  if(disc<0) return null;
  const sq=Math.sqrt(disc);
  const ts=[(-b-sq)/2,(-b+sq)/2].sort((a,b2)=>a-b2);
  for(const t of ts){
    if(!(t>1e-12)) continue;
    const q=[p[0]+t*d[0],p[1]+t*d[1]];
    if(Math.abs(q[0])>semi) continue;
    if(Math.abs(q[1]-z0)>Math.abs(R)) continue;   /* the vertex-side branch */
    return q;
  }
  return null;
}
function hitSphereNewton(p,d,z0,R,semi){
  if(!isFinite(R)||R===0) return hitSphere(p,d,z0,R,semi);
  if(Math.abs(d[1])<1e-15) return null;
  let t=(z0-p[1])/d[1];
  for(let i=0;i<80;i++){
    const y=p[0]+t*d[0], z=p[1]+t*d[1];
    if(Math.abs(y)>=Math.abs(R)) return null;
    const s=sphereSag(R,y);
    if(!isFinite(s)) return null;
    const disc=1-y*y/(R*R);
    if(disc<=0) return null;
    const dsdy=y/(R*Math.sqrt(disc));
    const den=d[1]-dsdy*d[0];
    if(Math.abs(den)<1e-15) return null;
    const dt=-(z-(z0+s))/den;
    t+=dt;
    if(Math.abs(dt)<1e-14) break;
  }
  if(!(t>1e-12)) return null;
  const q=[p[0]+t*d[0],p[1]+t*d[1]];
  return Math.abs(q[0])<=semi?q:null;
}
function sphereNormal(y,R){
  if(!isFinite(R)||R===0) return [0,-1];
  const disc=1-y*y/(R*R);
  if(disc<=0) return [0,-1];
  const dsdy=y/(R*Math.sqrt(disc));
  const L=Math.hypot(dsdy,1);
  return [-dsdy/L,1/L];
}
/* vector Snell; null on total internal reflection */
function refractVec(d,nrm,n1,n2){
  const L=Math.hypot(d[0],d[1]);
  let dx=d[0]/L, dy=d[1]/L, nx=nrm[0], ny=nrm[1];
  let ci=-(nx*dx+ny*dy);
  if(ci<0){ nx=-nx; ny=-ny; ci=-ci; }
  const eta=n1/n2, k=1-eta*eta*(1-ci*ci);
  if(k<0) return null;
  const g=eta*ci-Math.sqrt(k);
  return [eta*dx+g*nx,eta*dy+g*ny];
}
function traceRealLens(p0,d0,n,R1,R2,t,semi,useNewton){
  const hit=useNewton?hitSphereNewton:hitSphere;
  const L=Math.hypot(d0[0],d0[1]);
  let d=[d0[0]/L,d0[1]/L], p=[p0[0],p0[1]];
  const pts=[[p[0],p[1]]];
  let q=hit(p,d,0,R1,semi);
  if(q===null) return null;
  let dd=refractVec(d,sphereNormal(q[0],R1),1,n);
  if(dd===null) return null;
  pts.push([q[0],q[1]]); p=q; d=dd;
  q=hit(p,d,t,R2,semi);
  if(q===null) return null;
  dd=refractVec(d,sphereNormal(q[0],R2),n,1);
  if(dd===null) return null;
  pts.push([q[0],q[1]]);
  return {pts:pts,p:q,d:dd};
}
function axisCrossing(p,d){
  if(Math.abs(d[0])<1e-15) return Infinity;
  return p[1]+(-p[0]/d[0])*d[1];
}
/* longitudinal spherical aberration at ray height h, measured from the
   paraxial back focus (both from the rear vertex).  Negative = the marginal
   ray crosses EARLIER, which is what a positive lens does. */
function lsaAt(h,n,R1,R2,t,semi){
  const r=traceRealLens([h,-1000],[0,1],n,R1,R2,t,semi,false);
  if(r===null) return NaN;
  return (axisCrossing(r.p,r.d)-t)-backFocal(n,R1,R2,t);
}
/* the marginal ray's height at the PARAXIAL focal plane: the transverse blur */
function blurAt(h,n,R1,R2,t,semi){
  const r=traceRealLens([h,-1000],[0,1],n,R1,R2,t,semi,false);
  if(r===null) return NaN;
  const zf=t+backFocal(n,R1,R2,t);
  return r.p[0]+((zf-r.p[1])/r.d[1])*r.d[0];
}
/* a real CONCAVE MIRROR's marginal focus, in closed form.  A ray parallel to
   the axis at height h reflects to cross the axis at R - R/(2 cos(asin(h/R)))
   in front of the vertex; the paraxial R/2 is the h -> 0 limit. */
function mirrorMarginalFocus(R,h){
  const a=Math.abs(h/R);
  if(a>=1) return NaN;
  return Math.abs(R)-Math.abs(R)/(2*Math.sqrt(1-a*a));
}
/* the same by exact vector reflection -- the independent route selfTest pins
   the closed form against.  Vertex at z = 0, light running +z, the centre of
   curvature at z = -R, so a concave mirror's rim is nearer the source. */
function mirrorFocusTrace(R,h){
  const Rm=Math.abs(R), th=Math.asin(h/Rm);
  const zhit=-Rm*(1-Math.cos(th));
  const nx=Math.sin(th), ny=Math.cos(th);
  const dot=0*nx+1*ny;
  const rx=0-2*dot*nx, ry=1-2*dot*ny;
  if(rx===0) return Infinity;
  return -(zhit+(-h/rx)*ry);
}
