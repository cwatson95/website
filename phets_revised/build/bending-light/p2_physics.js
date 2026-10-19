
/* ================================================================== *
 *  the physics — dispersion, Snell, Fresnel, the wave, the prism      *
 *  tracer, the rainbow.  Every closed form here is re-derived in      *
 *  build/bending-light/derive.py and pinned in selfTest against the   *
 *  printed lines of refvals.txt.                                      *
 * ================================================================== */

/* Angles.  A constant named after a unit does not say which way it converts
   (Known-bad, bloch_sphere): DEG multiplies degrees INTO radians, RAD
   multiplies radians INTO degrees, and selfTest pins both against pi/2. */
const DEG=PI/180, RAD=180/PI;

/* ---- PhET's constants, read out of build 1.2.5 (docs/phets/bending-light_en.html) ---- */
const PHET={
  lamRed:650,                 /* WAVELENGTH_RED = 65e-8 m, the reference wavelength */
  lamMin:380, lamMax:700,     /* LASER_MIN_WAVELENGTH (VisibleColor), LASER_MAX_WAVELENGTH */
  c:299792458,                /* SPEED_OF_LIGHT */
  maxWaveAngle:3.0194,        /* MAX_ANGLE_IN_WAVE_MODE, rad */
  maxSteps:50,                /* maxLightRaySteps query parameter, default 50 */
  powerMin:0.001,             /* the prism tracer gives up below this */
  drawMin:0.005,              /* the Intro screen stops drawing a reflected ray below this */
  laserAngle0:3*Math.PI/4,    /* the Intro laser's initial angle => 45 deg of incidence */
  modelW:62, modelH:43.4,     /* the model world, in red wavelengths (62 x 0.7*62) */
  prismT:10,                  /* the prism prototypes are 10 red wavelengths across */
  fanSpacing:0.5, fanLo:-1, fanHi:1.1,  /* the five-ray fan: i = -T .. 1.1T step T/2 */
  nSliderLo:1.000293, nSliderHi:1.6,    /* the index slider's range */
  nCustom0:2.6,               /* the custom substance starts at MYSTERY_B + 1.2 */
};
/* PhET's white light: _.range(400, 700, 10) — 400, 410, ... 690 nm, 30 of them */
const WHITE_WL=(()=>{ const a=[]; for(let l=400;l<700;l+=10) a.push(l); return a; })();
/* Thirty strokes on almost the same path cannot be composited into white on
   a canvas: source-over with alpha is not addition, so whichever end of the
   spectrum is painted last simply wins (the lenses.html Known-bad — a fan of
   four Fraunhofer lines read as one red beam there; here thirty of them read
   as one green one).  The rule this file uses instead is geometric and says
   something true: WHERE THE THIRTY WAVELENGTHS LIE WITHIN A LINE WIDTH OF ONE
   ANOTHER THE BEAM IS DRAWN WHITE, because thirty wavelengths together are
   white; where they have separated by more than that they are drawn
   one at a time in their own colours.  mergeMask decides that per segment,
   outside any draw call, so selfTest can assert it. */
const WHITE_MERGE_PX=2.5;
function mergeMask(traces,pxPerUnit,tol){
  const lim=(tol===undefined?WHITE_MERGE_PX:tol)/Math.max(pxPerUnit,1e-9);
  let n=Infinity;
  for(const t of traces) n=Math.min(n,t.segs.length);
  if(!isFinite(n)) return [];
  const ref=traces[Math.floor(traces.length/2)];
  const out=[];
  for(let k=0;k<n;k++){
    let spread=0;
    const r=ref.segs[k];
    for(const t of traces){
      const a=t.segs[k];
      spread=Math.max(spread,Math.hypot(a[0]-r[0],a[1]-r[1]),Math.hypot(a[2]-r[2],a[3]-r[3]));
    }
    out.push(spread<=lim);
  }
  return out;
}

/* ---- the substances, with PhET's index at 650 nm ---- */
const SUBS=[
  {id:'air',      name:'air',       n:1.000293, phet:true},
  {id:'water',    name:'water',     n:1.333,    phet:true},
  {id:'glass',    name:'glass',     n:1.5,      phet:true},
  {id:'diamond',  name:'diamond',   n:2.419,    phet:false},
  {id:'mysteryA', name:'Mystery A', n:2.419,    phet:true, mystery:true},
  {id:'mysteryB', name:'Mystery B', n:1.4,      phet:true, mystery:true},
  {id:'custom',   name:'custom',    n:null,     phet:true},
];
function subById(id){ for(const s of SUBS) if(s.id===id) return s; throw new Error('no substance '+id); }

/* ---- dispersion (PhET's model, written out from the formulas in its build) ----
   A Sellmeier curve for BK7 glass and an Edlen curve for air, blended linearly
   so that the result passes through the substance's stated index at 650 nm.
   The Sellmeier coefficients are the published SCHOTT N-BK7 set (lambda in
   metres, so the C are in m^2) and the air coefficients are Edlen's for
   standard air (15 C, 101.325 kPa, dry, 0.03% CO2).  Both are checked against
   published values in selfTest rather than trusted. */
const SELL_B=[1.03961212,0.231792344,1.01046945];
const SELL_C=[6.00069867e-15,2.00179144e-14,1.03560653e-10];
const AIR_A=[0.05792105,0.00167917], AIR_K=[238.0185,57.362];
const NM=1e-9;

function sellmeier(lamM){
  const l2=lamM*lamM;
  let s=1;
  for(let i=0;i<3;i++) s+=SELL_B[i]*l2/(l2-SELL_C[i]);
  return Math.sqrt(s);
}
function airIndex(lamM){
  const sig2=Math.pow(lamM*1e6,-2);          /* 1/lambda[um]^2 */
  return 1+AIR_A[0]/(AIR_K[0]-sig2)+AIR_A[1]/(AIR_K[1]-sig2);
}
/* how much of BK7's dispersion this substance carries; PhET clamps it at 0 */
function blendFraction(nRef){
  const a=airIndex(PHET.lamRed*NM);
  return Math.max(0,(nRef-a)/(sellmeier(PHET.lamRed*NM)-a));
}
/* the index of a substance named by nRef (its index at 650 nm) at lamNm */
function indexOf(nRef,lamNm){
  const s=blendFraction(nRef), lamM=lamNm*NM;
  return s*sellmeier(lamM)+(1-s)*airIndex(lamM);
}
/* the index a medium of the state has at a wavelength */
function mediumIndex(subId,customN,lamNm){
  const s=subById(subId);
  return indexOf(s.n===null?customN:s.n,lamNm);
}

/* ---- Snell's law ---- */
/* theta_2, or NaN when n1 sin(th1) > n2 (total internal reflection) */
function refractAngle(n1,n2,th1){
  const s=n1*Math.sin(th1)/n2;
  return Math.abs(s)>1?NaN:Math.asin(s);
}
/* the angle past which nothing is transmitted, or NaN when there is none */
function criticalAngle(n1,n2){ return n2>=n1?NaN:Math.asin(n2/n1); }
/* Brewster's angle: the angle at which R_p is exactly zero */
function brewster(n1,n2){ return Math.atan2(n2,n1); }

/* ---- the Fresnel equations ----
   s: the electric field perpendicular to the plane of incidence
   p: the electric field in the plane of incidence
   R + T = 1 exactly, in both, at every angle: the transmitted POWER carries
   the factor (n2 cos th2)/(n1 cos th1) because the beam changes width and
   speed when it crosses.  PhET uses the s pair for its ray brightness and its
   intensity meter; this file computes both and says which one is shown. */
function fresnel(n1,n2,th1){
  const c1=Math.cos(th1), s2=n1*Math.sin(th1)/n2;
  if(Math.abs(s2)<=1){
    const c2=Math.sqrt(Math.max(0,1-s2*s2));
    const rs=(n1*c1-n2*c2)/(n1*c1+n2*c2), rp=(n2*c1-n1*c2)/(n2*c1+n1*c2);
    const ts=2*n1*c1/(n1*c1+n2*c2), tp=2*n1*c1/(n2*c1+n1*c2);
    const k=c1>0?(n2*c2)/(n1*c1):0;
    return {rs:rs,rp:rp,ts:ts,tp:tp,Rs:rs*rs,Rp:rp*rp,Ts:k*ts*ts,Tp:k*tp*tp,
            th2:Math.asin(s2),tir:false,phs:0,php:0};
  }
  /* past the critical angle cos(th2) is imaginary: |r| = 1 and nothing is
     transmitted, and the reflected amplitude picks up the Goos-Hanchen phase.
     The evanescent DECAY CONSTANT is not returned here: fresnelSComplex owns
     it, and everything that draws or reads it takes it from there.  This
     function used to carry a second copy that nothing called, which a 109-
     mutant sweep duly reported as a survivor. */
  const g=Math.sqrt(s2*s2-1);
  return {rs:1,rp:1,ts:0,tp:0,Rs:1,Rp:1,Ts:0,Tp:0,th2:NaN,tir:true,
          phs:-2*Math.atan2(n2*g,n1*c1), php:-2*Math.atan2(n1*g,n2*c1)};
}
/* The complex s-polarised amplitudes, valid through total internal
   reflection: r = (a - b)/(a + b), t = 2a/(a + b) with a = n1 cos th1 and
   b = n2 cos th2 (real) or i n2 g (imaginary, past the critical angle).
   This is the ONLY place the evanescent decay constant is computed:
   kap = n2 sqrt(s2^2 - 1) = sqrt(n1^2 sin^2 th1 - n2^2), in units of k0, and
   it is zero wherever the transmitted wave propagates. */
function fresnelSComplex(n1,n2,th1){
  const a=n1*Math.cos(th1), s2=n1*Math.sin(th1)/n2;
  if(Math.abs(s2)<=1){
    const b=n2*Math.sqrt(Math.max(0,1-s2*s2));
    return {rRe:(a-b)/(a+b),rIm:0,tRe:2*a/(a+b),tIm:0,ky2:b,kap:0,tir:false};
  }
  const B=n2*Math.sqrt(s2*s2-1), den=a*a+B*B;
  return {rRe:(a*a-B*B)/den, rIm:-2*a*B/den,
          tRe:2*a*a/den, tIm:-2*a*B/den, ky2:0, kap:B, tir:true};
}
const cAbs=(re,im)=>Math.hypot(re,im);
const cArg=(re,im)=>Math.atan2(im,re);

/* ---- the wave: wavelength and speed inside a medium ---- */
function lambdaIn(lam0,n){ return lam0/n; }
function speedIn(n){ return PHET.c/n; }

/* The field of the two-medium problem, in world units (one unit = one red
   wavelength in vacuum), at phase `ph` = omega t.  y > 0 is medium 1.
   Returns the s-polarised scalar field; medium 1 carries incident + reflected
   and medium 2 the transmitted (or evanescent) wave. */
function waveAt(W,x,y,ph){
  const kx=W.k0*W.n1*Math.sin(W.th1);
  if(y>=0){
    const ky=W.k0*W.n1*Math.cos(W.th1);
    const rA=cAbs(W.f.rRe,W.f.rIm), rP=cArg(W.f.rRe,W.f.rIm);
    return Math.cos(kx*x-ky*y-ph)+rA*Math.cos(kx*x+ky*y-ph+rP);
  }
  const tA=cAbs(W.f.tRe,W.f.tIm), tP=cArg(W.f.tRe,W.f.tIm);
  const ky2=W.k0*W.f.ky2, kap=W.k0*W.f.kap;
  return tA*Math.exp(kap*y)*Math.cos(kx*x-ky2*y-ph+tP);
}
/* The TIME-AVERAGED intensity <E^2>, which depends on y alone.  Above the
   boundary the incident and reflected waves interfere into a standing
   pattern, <E^2> = (1 + |r|^2)/2 + |r| cos(2 k_y y + arg r); below it the
   transmitted wave carries |t|^2/2, times exp(2 kappa y) past the critical
   angle.  Continuous at y = 0, because |1 + r|^2 = |t|^2 exactly. */
function meanIntensity(W,y){
  if(y>=0){
    const rA=cAbs(W.f.rRe,W.f.rIm), rP=cArg(W.f.rRe,W.f.rIm);
    const ky=W.k0*W.n1*Math.cos(W.th1);
    return 0.5*(1+rA*rA)+rA*Math.cos(2*ky*y+rP);
  }
  const tA=cAbs(W.f.tRe,W.f.tIm);
  return 0.5*tA*tA*Math.exp(2*W.k0*W.f.kap*y);
}
/* everything the wave view needs, in one object */
function waveState(n1,n2,th1,lam0Nm){
  /* k0 in world units: one world unit is one RED wavelength in vacuum, so a
     wave of vacuum wavelength lam0 has k0 = 2 pi (lamRed/lam0) per unit */
  const k0=TAU*PHET.lamRed/lam0Nm;
  return {n1:n1,n2:n2,th1:th1,lam0:lam0Nm,k0:k0,f:fresnelSComplex(n1,n2,th1)};
}

/* ================================================================== *
 *  the prism tracer — exact intersection, vector Snell at every face  *
 * ================================================================== */
const TRACE_EPS=1e-9;

/* nearest forward hit of the ray p + t d with a CLOSED polygon whose points
   run counter-clockwise; the normal returned points OUT of the polygon */
function polyHit(p,d,pts){
  let bt=null, bn=null;
  const m=pts.length;
  for(let i=0;i<m;i++){
    const a=pts[i], b=pts[(i+1)%m];
    const ex=b[0]-a[0], ey=b[1]-a[1];
    const den=d[0]*ey-d[1]*ex;
    if(Math.abs(den)<1e-15) continue;
    const qx=a[0]-p[0], qy=a[1]-p[1];
    const t=(qx*ey-qy*ex)/den, u=(qx*d[1]-qy*d[0])/den;
    if(t>TRACE_EPS&&u>=-1e-12&&u<=1+1e-12&&(bt===null||t<bt)){
      const L=Math.hypot(ex,ey);
      bt=t; bn=[ey/L,-ex/L];
    }
  }
  return bt===null?null:{t:bt,n:bn};
}
/* nearest forward hit with a circle; with `half` given only the arc on that
   side of the centre counts (that is how the semicircle's curved face works) */
function circleHit(p,d,c,r,half){
  const ox=p[0]-c[0], oy=p[1]-c[1];
  const a=d[0]*d[0]+d[1]*d[1], b=2*(ox*d[0]+oy*d[1]), cc=ox*ox+oy*oy-r*r;
  const disc=b*b-4*a*cc;
  if(disc<0) return null;
  const sq=Math.sqrt(disc);
  /* the stable pair of roots: one from the well-conditioned branch, the other
     from the product of the roots */
  const q=-0.5*(b+(b<0?-sq:sq));
  const roots=(Math.abs(q)>1e-300?[q/a,cc/q]:[(-b-sq)/(2*a),(-b+sq)/(2*a)]).sort((u,v)=>u-v);
  for(const t of roots){
    if(t<=TRACE_EPS) continue;
    const hx=p[0]+t*d[0], hy=p[1]+t*d[1];
    if(half&&((hx-c[0])*half[0]+(hy-c[1])*half[1])<=0) continue;
    const L=Math.hypot(hx-c[0],hy-c[1]);
    return {t:t,n:[(hx-c[0])/L,(hy-c[1])/L]};
  }
  return null;
}
function segHit(p,d,a,b,outN){
  const ex=b[0]-a[0], ey=b[1]-a[1], den=d[0]*ey-d[1]*ex;
  if(Math.abs(den)<1e-15) return null;
  const qx=a[0]-p[0], qy=a[1]-p[1];
  const t=(qx*ey-qy*ex)/den, u=(qx*d[1]-qy*d[0])/den;
  if(t>TRACE_EPS&&u>=-1e-12&&u<=1+1e-12) return {t:t,n:outN};
  return null;
}
function shapeHit(sh,p,d){
  if(sh.kind==='poly') return polyHit(p,d,sh.pts);
  if(sh.kind==='circle') return circleHit(p,d,sh.c,sh.r,null);
  if(sh.kind==='semi'){
    const h1=segHit(p,d,sh.a,sh.b,[-sh.half[0],-sh.half[1]]);
    const h2=circleHit(p,d,sh.c,sh.r,sh.half);
    if(!h1) return h2;
    if(!h2) return h1;
    return h1.t<h2.t?h1:h2;
  }
  throw new Error('shape '+sh.kind);
}
function shapeInside(sh,p){
  if(sh.kind==='poly'){
    const pts=sh.pts; let c=0;
    for(let i=0;i<pts.length;i++){
      const a=pts[i], b=pts[(i+1)%pts.length];
      if((a[1]>p[1])!==(b[1]>p[1])){
        const x=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1]);
        if(x>p[0]) c++;
      }
    }
    return c%2===1;
  }
  if(sh.kind==='circle') return Math.hypot(p[0]-sh.c[0],p[1]-sh.c[1])<sh.r;
  if(sh.kind==='semi'){
    const dx=p[0]-sh.c[0], dy=p[1]-sh.c[1];
    return Math.hypot(dx,dy)<sh.r&&dx*sh.half[0]+dy*sh.half[1]>0;
  }
  throw new Error('shape '+sh.kind);
}
/* vector Snell: `nrm` points back against the incoming ray */
function vecRefract(d,nrm,n1,n2){
  const eta=n1/n2, ci=-(d[0]*nrm[0]+d[1]*nrm[1]);
  const k=1-eta*eta*(1-ci*ci);
  if(k<0) return null;
  const s=eta*ci-Math.sqrt(k);
  return [eta*d[0]+s*nrm[0],eta*d[1]+s*nrm[1]];
}
function vecReflect(d,nrm){
  const dn=d[0]*nrm[0]+d[1]*nrm[1];
  return [d[0]-2*dn*nrm[0],d[1]-2*dn*nrm[1]];
}
/* PhET's five prism prototypes, in units of the red wavelength (t = 10).
   The vertices are PhET's own; the polygons are wound counter-clockwise so
   that polyHit's outward normal is outward. */
function prismShape(id){
  const t=PHET.prismT, i=t/2, r3=Math.sqrt(3);
  if(id==='triangle') return {kind:'poly',pts:[[-t/2,-t/(2*r3)],[t/2,-t/(2*r3)],[0,t/r3]]};
  if(id==='trapezoid') return {kind:'poly',pts:[[-t/2,-t*r3/4],[t/2,-t*r3/4],[t/4,t*r3/4],[-t/4,t*r3/4]]};
  if(id==='square') return {kind:'poly',pts:[[-t/2,-t/2],[t/2,-t/2],[t/2,t/2],[-t/2,t/2]]};
  if(id==='circle') return {kind:'circle',c:[0,0],r:i};
  if(id==='semicircle') return {kind:'semi',c:[0,0],r:i,a:[0,-i],b:[0,i],half:[-1,0]};
  throw new Error('prism '+id);
}
/* rotate a shape about the origin */
function rotShape(sh,a){
  if(a===0) return sh;
  const ca=Math.cos(a), sa=Math.sin(a);
  const R=p=>[p[0]*ca-p[1]*sa,p[0]*sa+p[1]*ca];
  if(sh.kind==='poly') return {kind:'poly',pts:sh.pts.map(R)};
  if(sh.kind==='circle') return {kind:'circle',c:R(sh.c),r:sh.r};
  return {kind:'semi',c:R(sh.c),r:sh.r,a:R(sh.a),b:R(sh.b),half:R(sh.half)};
}
/* Trace one ray through one shape.  Returns the drawn segments
   [x0,y0,x1,y1,power,inside] and the exit direction of the primary branch.
   PhET's own limits: at most maxSteps segments, and a branch is dropped once
   its power falls below powerMin. */
function traceRay(sh,p,d,nOut,nIn,opt){
  opt=opt||{};
  const reach=opt.reach===undefined?40:opt.reach;
  const refl=opt.reflections!==false;
  const maxSteps=opt.maxSteps===undefined?PHET.maxSteps:opt.maxSteps;
  const pmin=opt.powerMin===undefined?PHET.powerMin:opt.powerMin;
  const segs=[];
  let exitDir=null, exitPt=null, path=0;
  const queue=[{p:p,d:d,pw:1,ins:shapeInside(sh,p),depth:0,primary:true}];
  let steps=0;
  while(queue.length&&steps<maxSteps){
    steps++;
    const it=queue.shift();
    if(it.pw<pmin||it.depth>12) continue;
    const hit=shapeHit(sh,it.p,it.d);
    if(!hit){
      segs.push([it.p[0],it.p[1],it.p[0]+reach*it.d[0],it.p[1]+reach*it.d[1],it.pw,it.ins]);
      if(it.primary&&!exitDir){ exitDir=it.d; exitPt=it.p; }
      continue;
    }
    const hx=it.p[0]+hit.t*it.d[0], hy=it.p[1]+hit.t*it.d[1];
    segs.push([it.p[0],it.p[1],hx,hy,it.pw,it.ins]);
    if(it.primary) path+=hit.t*(it.ins?nIn:nOut);
    const n1=it.ins?nIn:nOut, n2=it.ins?nOut:nIn;
    const dn=it.d[0]*hit.n[0]+it.d[1]*hit.n[1];
    const nn=dn<0?hit.n:[-hit.n[0],-hit.n[1]];
    const cos1=clamp(-(it.d[0]*nn[0]+it.d[1]*nn[1]),-1,1);
    const f=fresnel(n1,n2,Math.acos(cos1));
    const R=0.5*(f.Rs+f.Rp);
    const td=vecRefract(it.d,nn,n1,n2), rd=vecReflect(it.d,nn);
    const off=1e-9;
    if(!td){
      queue.push({p:[hx+off*rd[0],hy+off*rd[1]],d:rd,pw:it.pw,ins:it.ins,
                  depth:it.depth+1,primary:it.primary});
    } else {
      queue.push({p:[hx+off*td[0],hy+off*td[1]],d:td,pw:it.pw*(1-R),ins:!it.ins,
                  depth:it.depth+1,primary:it.primary});
      if(refl&&it.pw*R>=pmin)
        queue.push({p:[hx+off*rd[0],hy+off*rd[1]],d:rd,pw:it.pw*R,ins:it.ins,
                    depth:it.depth+1,primary:false});
    }
  }
  return {segs:segs,exitDir:exitDir,exitPt:exitPt,path:path,steps:steps};
}

/* ---- the prism, in closed form, for the tracer to be checked against ----
   a ray entering one face of a prism of apex angle A at th1 leaves deviated by
   D = th1 + th2 - A, with th2 got by Snell at each face in turn */
function prismDeviation(n1,n2,A,th1){
  const r1=refractAngle(n1,n2,th1);
  if(!isFinite(r1)) return NaN;
  const r2=A-r1, s=n2*Math.sin(r2)/n1;
  if(Math.abs(s)>1) return NaN;
  return th1+Math.asin(s)-A;
}
/* the minimum deviation, where the ray crosses the prism symmetrically:
   n2/n1 = sin((A + D_min)/2)/sin(A/2).  NaN when the apex angle exceeds
   2 theta_c and the prism simply traps the ray. */
function prismMinDeviation(n1,n2,A){
  const arg=n2/n1*Math.sin(A/2);
  return Math.abs(arg)>1?NaN:2*Math.asin(arg)-A;
}
/* Enter the left face of PhET's equilateral triangle at th1 and TRACE the ray
   out; returns the deviation of the emergent beam.  This is the check that
   matters: it shares no arithmetic with prismDeviation, so the two agreeing is
   evidence about the intersection code, not about one formula. */
function traceTriangleDeviation(nEnv,nPr,th1){
  const tri=prismShape('triangle'), pts=tri.pts;
  const apex=pts[2], bl=pts[0];
  const mid=[0.5*(apex[0]+bl[0]),0.5*(apex[1]+bl[1])];
  const ex=bl[0]-apex[0], ey=bl[1]-apex[1], L=Math.hypot(ex,ey);
  const out=[ey/L,-ex/L];                     /* the CCW polygon's outward normal */
  const inw=[-out[0],-out[1]];
  const ca=Math.cos(th1), sa=Math.sin(th1);
  const d=[inw[0]*ca-inw[1]*sa,inw[0]*sa+inw[1]*ca];
  const start=[mid[0]-6*d[0],mid[1]-6*d[1]];
  const tr=traceRay(tri,start,d,nEnv,nPr,{reflections:false});
  if(!tr.exitDir) return NaN;
  return Math.abs(Math.atan2(d[0]*tr.exitDir[1]-d[1]*tr.exitDir[0],
                             d[0]*tr.exitDir[0]+d[1]*tr.exitDir[1]));
}
/* the lateral displacement of a beam through a slab of thickness t */
function slabOffset(n1,n2,th1,t){
  const th2=refractAngle(n1,n2,th1);
  return isFinite(th2)?t*Math.sin(th1-th2)/Math.cos(th2):NaN;
}

/* ================================================================== *
 *  the rainbow — Descartes' stationary deviation in a sphere          *
 * ================================================================== */
/* k internal reflections: D(th) = 2 th - 2(k+1) asin(sin th/n) + k pi */
function rainDev(n,k,th){ return 2*th-2*(k+1)*Math.asin(Math.sin(th)/n)+k*PI; }
/* dD/dth = 0 exactly where cos^2 th = (n^2 - 1)/(k^2 + 2k) */
function rainTheta(n,k){
  const c2=(n*n-1)/(k*k+2*k);
  return (c2<0||c2>1)?NaN:Math.acos(Math.sqrt(c2));
}
/* the angular radius of the bow about the antisolar point */
function bowAngle(n,k){
  const th=rainTheta(n,k);
  return isFinite(th)?Math.abs(PI-rainDev(n,k,th)):NaN;
}
/* the RELATIVE index of the drop against what surrounds it: this is what
   Snell's law at the drop's surface carries, so it is what the rainbow
   geometry uses (n_water/n_air, not n_water) */
function dropIndex(lamNm){ return indexOf(1.333,lamNm)/indexOf(1.000293,lamNm); }
/* the Fresnel throughput of the primary path: transmit in, reflect k times,
   transmit out — unpolarised, or one polarisation */
function bowThroughput(nOut,nIn,k,th,pol){
  const thr=Math.asin(Math.sin(th)/nIn*nOut);
  const fin=fresnel(nOut,nIn,th), fint=fresnel(nIn,nOut,thr);
  const T1=pol==='s'?fin.Ts:pol==='p'?fin.Tp:0.5*(fin.Ts+fin.Tp);
  const Rr=pol==='s'?fint.Rs:pol==='p'?fint.Rp:0.5*(fint.Rs+fint.Rp);
  const T2=pol==='s'?fint.Ts:pol==='p'?fint.Tp:0.5*(fint.Ts+fint.Tp);
  return T1*Math.pow(Rr,k)*T2;
}
/* the path of one ray through a unit sphere at impact parameter b = sin(th),
   with k internal reflections: the chord points on the circle */
/* At the stationary ray the geometry forces n1 cos th1 = (k+1) n2 cos th2 at
   the internal bounce, so the reflectance there is exact and, for s
   polarisation, INDEPENDENT OF THE INDEX.  Both are asserted. */
function bowRsExact(k){ return Math.pow(k/(k+2),2); }
function bowRpExact(k,m){ return Math.pow(((k+1)-m*m)/((k+1)+m*m),2); }
/* and therefore the WHOLE s-polarised throughput of the k-th bow is exact and
   index-independent too: the entry interface is the same interface at the
   conjugate angle, so it reflects (k/(k+2))^2 as well. */
function bowThroughputSExact(k){
  const R=Math.pow(k/(k+2),2);
  return (1-R)*(1-R)*Math.pow(R,k);
}
/* The path of one ray through a unit sphere at impact parameter b = sin(th)
   with k internal reflections: the chord points on the circle, and the
   EMERGENT DIRECTION obtained by refracting at the exit face rather than by
   turning the incoming direction through D.  selfTest asserts the two agree,
   which is what ties the drawing to rainDev (Known-bad: assert on the objects
   the view draws, not on the formula beside them). */
function dropPath(n,k,th){
  const thr=Math.asin(Math.sin(th)/n);
  const pts=[];
  /* enter at angle `a0` on the circle, measured so that the ray comes in
     horizontally from the left at height b = sin(th) */
  let a=PI-th;                       /* the entry point's polar angle */
  pts.push([Math.cos(a),Math.sin(a)]);
  for(let i=0;i<=k;i++){
    a=a-(PI-2*thr);                  /* each chord subtends pi - 2 thr */
    pts.push([Math.cos(a),Math.sin(a)]);
  }
  const last=pts[pts.length-1], prev=pts[pts.length-2];
  const L=Math.hypot(last[0]-prev[0],last[1]-prev[1]);
  const din=[(last[0]-prev[0])/L,(last[1]-prev[1])/L];
  const nrm=[-last[0],-last[1]];     /* pointing back against the inside ray */
  const out=vecRefract(din,nrm,n,1);
  return {pts:pts,thr:thr,dev:rainDev(n,k,th),
          out:out||vecReflect(din,nrm),tir:!out};
}
