
/* ================================================================== *
 *  physics — point charges held in the plane z = 0, the 3-D Coulomb   *
 *  field and potential by exact superposition                         *
 * ================================================================== */
const DEG=PI/180;                       /* degrees INTO radians: 90*DEG = pi/2 */
/* the one measured constant: eps0, CODATA 2022, from the NIST constants
   page (physics.nist.gov/cgi-bin/cuu/Value?ep0), stored verbatim */
const EPS0=8.8541878188e-12;            /* F/m */
const K_SI=1/(4*PI*EPS0);               /* N m^2/C^2 = 8.98755e9 */
const KNC=K_SI*1e-9;                    /* V m/nC:  V[volt] = KNC q[nC] / r[m] */
const K_PHET=9;                         /* PhET's K_CONSTANT, a rounding of KNC */
/* PhET's layout and display values (ChargesAndFieldsConstants and the view
   classes of the 1.0.67 build), converted to metres at its 128 px/m: the
   play area, the charge bin, the arrow and voltage grids, the two colour
   saturations, the sensor-arrow scale (15 px per V/m), the field-arrow
   length (40 px), the charge radius (12 px), the 3-cm radius inside which
   no equipotential is seeded, and the reading above which a sensor shows a
   dash (MAX_EFIELD_MAGNITUDE) */
const PLANE={x0:-4,x1:4,y0:-2.5,y1:2.5};
const BIN={x0:-1.25,x1:1.25,y0:-2.3,y1:-1.7};
const ARROW_DX=0.5, MAP_DX=0.1;
const V_SAT=40, E_SAT=5;
const SENSOR_M_PER_VM=15/128, ARROW_LEN=40/128, CHARGE_R=12/128;
const EQ_REFUSE=0.03, E_MAX_READ=1e6;
const MAX_CHARGES=40, MAX_SENSORS=12, MAX_EQ=24;
/* the region an equipotential is followed over before it is called open —
   the plane with a 2-m margin (PhET's enlarged bounds are [-6,6]x[-2.5,7.5],
   lopsided for its screen layout) */
const EQ_BOX={x0:-6,x1:6,y0:-4.5,y1:4.5};

function potentialAt(ch,x,y){
  let s=0;
  for(let i=0;i<ch.length;i++){ const c=ch[i]; s+=c.q/Math.hypot(x-c.x,y-c.y); }
  return KNC*s;
}
/* V and E in one pass: E = k sum q (r - r_i)/|r - r_i|^3 */
function fieldAt(ch,x,y){
  let s=0, ex=0, ey=0;
  for(let i=0;i<ch.length;i++){
    const c=ch[i], dx=x-c.x, dy=y-c.y, r2=dx*dx+dy*dy, r=Math.sqrt(r2), r3=r2*r;
    s+=c.q/r; ex+=c.q*dx/r3; ey+=c.q*dy/r3;
  }
  return {V:KNC*s, ex:KNC*ex, ey:KNC*ey};
}
/* the Jacobian dE_a/dx_b = [dEx/dx, dEx/dy (= dEy/dx), dEy/dy]; symmetric
   because E = -grad V, and minus the in-plane Hessian of V */
function jacAt(ch,x,y){
  let a=0, b=0, d=0;
  for(let i=0;i<ch.length;i++){
    const c=ch[i], dx=x-c.x, dy=y-c.y, r2=dx*dx+dy*dy, r=Math.sqrt(r2), r3=r2*r, r5=r3*r2;
    a+=c.q*(1/r3-3*dx*dx/r5); b+=c.q*(-3*dx*dy/r5); d+=c.q*(1/r3-3*dy*dy/r5);
  }
  return [KNC*a,KNC*b,KNC*d];
}
function nearestCharge(ch,x,y){
  let r=Infinity, k=-1;
  for(let i=0;i<ch.length;i++){ const d=Math.hypot(x-ch[i].x,y-ch[i].y); if(d<r){ r=d; k=i; } }
  return {r,k};
}
function netCharge(ch){ let Q=0; for(const c of ch) Q+=c.q; return Q; }
/* the size of the terms being cancelled at a point, k sum |q|/r^2: the
   scale against which "E = 0" is judged */
function fieldScale(ch,x,y){
  let s=0; for(const c of ch){ const r2=(x-c.x)*(x-c.x)+(y-c.y)*(y-c.y); s+=Math.abs(c.q)/r2; }
  return KNC*s;
}
/* V with a rounding floor: a sum whose terms cancel to below 1e-12 of their
   total size is zero.  Off the exact bisector of a dipole by the 6e-17 of
   cos(90°), the plain sum read 1e-15 V and was drawn and printed as a value */
const ROUND_FLOOR=1e-12;
function potentialClean(ch,x,y){
  let s=0, sa=0;
  for(let i=0;i<ch.length;i++){ const c=ch[i], r=Math.hypot(x-c.x,y-c.y); s+=c.q/r; sa+=Math.abs(c.q)/r; }
  if(!isFinite(sa)) return KNC*s;
  return Math.abs(s)<=ROUND_FLOOR*sa?0:KNC*s;
}
function chargeKey(ch){ let s=''; for(const c of ch) s+=c.x+','+c.y+','+c.q+';'; return s; }
/* an E-field sensor's reading, PhET's way: magnitude and direction, a dash
   above 1e6 V/m (on top of a charge) */
function sensorReading(ch,x,y){
  const f=fieldAt(ch,x,y), V=potentialClean(ch,x,y);
  let m=Math.hypot(f.ex,f.ey), ex=f.ex, ey=f.ey;
  if(ch.length&&isFinite(m)&&m<=ROUND_FLOOR*fieldScale(ch,x,y)){ m=0; ex=0; ey=0; }   /* at a null: zero, not rounding */
  return {V, ex, ey, mag:m, ang:m>0?Math.atan2(ey,ex)/DEG:0, over:!(m<E_MAX_READ)};
}

/* ---- the two display grids (PhET's cell centres) ---- */
function vmapGrid(ch){
  const nx=Math.round((PLANE.x1-PLANE.x0)/MAP_DX), ny=Math.round((PLANE.y1-PLANE.y0)/MAP_DX), v=new Float64Array(nx*ny);
  for(let j=0;j<ny;j++) for(let i=0;i<nx;i++) v[j*nx+i]=potentialAt(ch,PLANE.x0+(i+0.5)*MAP_DX,PLANE.y0+(j+0.5)*MAP_DX);
  return {nx,ny,v};
}
function arrowGrid(ch){
  const nx=Math.round((PLANE.x1-PLANE.x0)/ARROW_DX), ny=Math.round((PLANE.y1-PLANE.y0)/ARROW_DX), out=[];
  for(let j=0;j<ny;j++) for(let i=0;i<nx;i++){
    const x=PLANE.x0+(i+0.5)*ARROW_DX, y=PLANE.y0+(j+0.5)*ARROW_DX, f=fieldAt(ch,x,y);
    out.push({x,y,ex:f.ex,ey:f.ey,mag:Math.hypot(f.ex,f.ey)});
  }
  return {nx,ny,a:out};
}
/* PhET's arrow opacity: |E|/5 V/m, clamped; "direction only" makes every
   arrow with a defined direction fully opaque */
function arrowAlpha(mag,dirOnly){ if(!(mag>1e-9)) return 0; return dirOnly?1:clamp(mag/E_SAT,0,1); }
/* PhET's voltage colour: linear in V to saturation at +-40 V */
function vLevel(V){ if(V!==V) return 0; return clamp(Math.abs(V)/V_SAT,0,1); }   /* NaN (coincident +q and -q) reads as zero */
/* a value safe to contour: +-infinity (a sample exactly on a charge) becomes
   a large finite number of the same sign, NaN (coincident +q and -q) zero */
function vSafe(V){ return V===V?clamp(V,-1e6,1e6):0; }

/* ================================================================== *
 *  equipotentials — RK4 along the tangent z x E/|E|, then Newton back  *
 *  onto V = V0 along E after every step                               *
 * ================================================================== */
/* the local length scale: the distance to the nearest charge, or |E|/|grad E|
   (the distance over which E changes by itself), whichever is smaller */
function lengthScale(ch,x,y){
  const nc=nearestCharge(ch,x,y), f=fieldAt(ch,x,y), j=jacAt(ch,x,y);
  const e=Math.hypot(f.ex,f.ey), jn=Math.sqrt(j[0]*j[0]+2*j[1]*j[1]+j[2]*j[2]);
  return Math.min(nc.r,jn>0?e/jn:Infinity);
}
function tangentAt(ch,x,y){ const f=fieldAt(ch,x,y), m=Math.hypot(f.ex,f.ey); return m>0?[-f.ey/m,f.ex/m]:null; }
function rk4Dir(dirFn,ch,x,y,h){
  const k1=dirFn(ch,x,y); if(!k1) return null;
  const k2=dirFn(ch,x+0.5*h*k1[0],y+0.5*h*k1[1]); if(!k2) return null;
  const k3=dirFn(ch,x+0.5*h*k2[0],y+0.5*h*k2[1]); if(!k3) return null;
  const k4=dirFn(ch,x+h*k3[0],y+h*k3[1]); if(!k4) return null;
  return [x+h*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6, y+h*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6];
}
/* Newton onto the level set: V(p + s E) = V(p) - s|E|^2 + ..., so s = (V - V0)/|E|^2 */
function projectToLevel(ch,x,y,V0){
  for(let it=0;it<4;it++){
    const f=fieldAt(ch,x,y), e2=f.ex*f.ex+f.ey*f.ey;
    if(!(e2>0)) break;
    const s=(f.V-V0)/e2; x+=s*f.ex; y+=s*f.ey;
    if(Math.abs(f.V-V0)<=1e-15*Math.max(1,Math.abs(V0))) break;
  }
  return [x,y];
}
/* Trace the equipotential through (x0, y0).  Refuses on an empty plane,
   within 3 cm of a charge (PhET's rule) and at a null of E, where the level
   set is not a single curve.  Follows one way until it closes on the seed
   (the step that crosses the seed's normal line, back within three steps of
   it) or leaves EQ_BOX; an open curve is then followed the other way too. */
function traceEquipotential(ch,x0,y0,opt){
  opt=opt||{};
  const c=opt.c||0.12, hmin=opt.hmin||0.004, hmax=opt.hmax||0.05, bx=opt.box||EQ_BOX, maxN=opt.maxN||8000;
  if(!ch.length) return {ok:false,why:'no charges on the plane'};
  if(nearestCharge(ch,x0,y0).r<EQ_REFUSE) return {ok:false,why:'too close to a charge'};
  const f0=fieldAt(ch,x0,y0), e0=Math.hypot(f0.ex,f0.ey);
  if(!(e0>1e-9*fieldScale(ch,x0,y0))) return {ok:false,why:'E = 0 here: no single equipotential'};
  const V0=f0.V, t0=[-f0.ey/e0,f0.ex/e0];
  function run(sgn){
    const pts=[[x0,y0]]; let x=x0, y=y0, s=0, closed=false, exit='steps', hLast=hmin;
    for(let n=0;n<maxN;n++){
      const h=clamp(c*lengthScale(ch,x,y),hmin,hmax); hLast=h;
      const q=rk4Dir(tangentAt,ch,x,y,sgn*h); if(!q){ exit='null'; break; }
      const p=projectToLevel(ch,q[0],q[1],V0);
      const before=(x-x0)*t0[0]+(y-y0)*t0[1], after=(p[0]-x0)*t0[0]+(p[1]-y0)*t0[1];
      s+=Math.hypot(p[0]-x,p[1]-y);
      if(s>6*hmin&&sgn*before<0&&sgn*after>=0&&Math.hypot(p[0]-x0,p[1]-y0)<3*h){ closed=true; exit='closed'; break; }
      x=p[0]; y=p[1]; pts.push([x,y]);
      if(x<bx.x0||x>bx.x1||y<bx.y0||y>bx.y1){ exit='box'; break; }
    }
    return {pts,closed,exit,h:hLast,s};
  }
  const fw=run(1);
  const V0c=potentialClean(ch,x0,y0);                /* the value to print (rounding floor) */
  if(fw.closed) return {ok:true,closed:true,pts:fw.pts,V0,V0c,x0,y0,gap:Math.hypot(fw.pts[fw.pts.length-1][0]-x0,fw.pts[fw.pts.length-1][1]-y0),exits:['closed']};
  const bw=run(-1);
  return {ok:true,closed:false,pts:bw.pts.slice(1).reverse().concat(fw.pts),V0,V0c,x0,y0,gap:null,exits:[bw.exit,fw.exit]};
}
function polyArea(pts){ let s=0; for(let i=0;i<pts.length;i++){ const a=pts[i], b=pts[(i+1)%pts.length]; s+=a[0]*b[1]-b[0]*a[1]; } return 0.5*s; }
function polyLength(pts,closed){ let s=0; const n=pts.length; for(let i=0;i<n-1;i++) s+=Math.hypot(pts[i+1][0]-pts[i][0],pts[i+1][1]-pts[i][1]);
  if(closed&&n>1) s+=Math.hypot(pts[0][0]-pts[n-1][0],pts[0][1]-pts[n-1][1]); return s; }

/* ================================================================== *
 *  field lines — RK4 on E/|E|, from the charges of the majority sign  *
 * ================================================================== */
/* R_ESC is far: the lines of a NEUTRAL configuration all come back, some only after
   a long excursion (a dipole line leaving at angle a from its axis reaches ~4a_d/a^2),
   and the step grows with the distance, so following them costs ~20 steps per e-fold */
const R_SEED=0.02, R_CAP=0.02, R_ESC=1e4, NULL_END=1e-7;
function unitE(sgn){ return (ch,x,y)=>{ const f=fieldAt(ch,x,y), m=Math.hypot(f.ex,f.ey); return m>0?[sgn*f.ex/m,sgn*f.ey/m]:null; }; }
/* follow sgn*E from (x0, y0): ends on a charge of the opposite sign (within
   R_CAP), beyond rEsc from the centre, at a null, or after maxN steps */
function traceFieldLine(ch,x0,y0,sgn,opt){
  opt=opt||{};
  /* no practical step floor: near a node the length scale |E|/|grad E| IS the distance
     to the null, so the steps shrink geometrically and the line reaches it; a floor
     made the RK4 step overshoot the node and orbit it until maxN (the triangle) */
  const c=opt.c||0.12, hmin=opt.hmin||1e-9, hmax=opt.hmax||1000, rEsc=opt.rEsc||R_ESC, maxN=opt.maxN||20000, cen=opt.cen||[0,0];
  const dir=unitE(sgn), pts=[[x0,y0]]; let x=x0, y=y0, end='steps', hit=-1;
  for(let n=0;n<maxN;n++){
    const h=clamp(c*lengthScale(ch,x,y),hmin,hmax);
    const q=rk4Dir(dir,ch,x,y,h); if(!q){ end='null'; break; }
    x=q[0]; y=q[1]; pts.push([x,y]);
    const nc=nearestCharge(ch,x,y);
    if(nc.r<R_CAP&&Math.sign(ch[nc.k].q)===-sgn){ end='charge'; hit=nc.k; break; }
    if(Math.hypot(x-cen[0],y-cen[1])>rEsc){ end='escape'; break; }
    /* a line can END at a null in the plane: at an in-plane minimum of V
       (the centre of three like charges) in-plane lines converge and the
       field turns out of the plane along z */
    const f=fieldAt(ch,x,y);
    if(!(Math.hypot(f.ex,f.ey)>NULL_END*fieldScale(ch,x,y))){ end='null'; break; }
  }
  return {pts,end,hit};
}
/* the seeding: N lines per charge of the majority sign (the positive ones
   when the plane is neutral), at angles (k + 1/2) 2 pi/N from the +x axis */
function fieldLines(ch,nPer,opt){
  opt=opt||{};
  if(!ch.length) return {lines:[],sgn:0,Q:0,ends:0,escapes:0,nulls:0,stalls:0};
  const Q=netCharge(ch), sgn=Q<0?-1:1, cen=moments(ch).c, lines=[];
  let ends=0, escapes=0, nulls=0, stalls=0;
  ch.forEach((cc,i)=>{
    if(Math.sign(cc.q)!==sgn) return;
    for(let k=0;k<nPer;k++){
      const a=(k+0.5)*TAU/nPer, L=traceFieldLine(ch,cc.x+R_SEED*Math.cos(a),cc.y+R_SEED*Math.sin(a),sgn,Object.assign({cen},opt));
      L.from=i; L.alpha=a; lines.push(L);
      if(L.end==='charge') ends++; else if(L.end==='escape') escapes++; else if(L.end==='null') nulls++; else stalls++;
    }
  });
  return {lines,sgn,Q,ends,escapes,nulls,stalls};
}
/* the Stokes flux function of charges on the x axis, sum q_i cos(theta_i):
   constant along every field line of such a configuration (3-D axisymmetry) */
function psiAxisX(ch,x,y){ let s=0; for(const c of ch) s+=c.q*(x-c.x)/Math.hypot(x-c.x,y-c.y); return s; }

/* ================================================================== *
 *  null points — Newton on E = 0 with the analytic Jacobian           *
 * ================================================================== */
function newtonNull(ch,x,y,bx){
  for(let it=0;it<60;it++){
    const f=fieldAt(ch,x,y), j=jacAt(ch,x,y), det=j[0]*j[2]-j[1]*j[1];
    if(!(Math.abs(det)>0)) return null;
    let dx=-( j[2]*f.ex-j[1]*f.ey)/det, dy=-(-j[1]*f.ex+j[0]*f.ey)/det;
    const st=Math.hypot(dx,dy); if(st>0.25){ dx*=0.25/st; dy*=0.25/st; }
    x+=dx; y+=dy;
    if(x<bx.x0-1||x>bx.x1+1||y<bx.y0-1||y>bx.y1+1) return null;
    if(Math.hypot(dx,dy)<1e-14*(1+Math.hypot(x,y))) break;
  }
  const f=fieldAt(ch,x,y);
  if(!(Math.hypot(f.ex,f.ey)<1e-10*fieldScale(ch,x,y))) return null;
  return [x,y];
}
/* classify by the in-plane Hessian of V, H = -J: det H < 0 is a saddle;
   det H > 0 with trace H > 0 an in-plane minimum, trace H < 0 a maximum.
   (Laplace's equation gives V_zz = -trace H: an in-plane minimum is a
   maximum along z, so Earnshaw still holds in 3-D.) */
function classifyNull(ch,x,y){
  const j=jacAt(ch,x,y), hxx=-j[0], hxy=-j[1], hyy=-j[2], det=hxx*hyy-hxy*hxy, tr=hxx+hyy;
  return {kind:det<0?'saddle':(tr>0?'min':'max'),det,tr};
}
function findNulls(ch,bx){
  bx=bx||PLANE;
  if(ch.length<2) return [];
  const seeds=[];
  for(let j=0;j<=16;j++) for(let i=0;i<=26;i++) seeds.push([bx.x0+(bx.x1-bx.x0)*i/26,bx.y0+(bx.y1-bx.y0)*j/16]);
  for(let a=0;a<ch.length;a++) for(let b=a+1;b<ch.length&&seeds.length<1400;b++) seeds.push([(ch[a].x+ch[b].x)/2,(ch[a].y+ch[b].y)/2]);
  const found=[];
  for(const s of seeds){
    if(nearestCharge(ch,s[0],s[1]).r<0.05) continue;
    const p=newtonNull(ch,s[0],s[1],bx); if(!p) continue;
    if(p[0]<bx.x0||p[0]>bx.x1||p[1]<bx.y0||p[1]>bx.y1) continue;
    if(nearestCharge(ch,p[0],p[1]).r<0.02) continue;
    if(found.some(q=>Math.hypot(q.x-p[0],q.y-p[1])<1e-6)) continue;
    const k=classifyNull(ch,p[0],p[1]);
    found.push({x:p[0],y:p[1],V:potentialAt(ch,p[0],p[1]),kind:k.kind,lap:k.tr});
  }
  found.sort((a,b)=>a.x-b.x||a.y-b.y);
  return found;
}

/* ================================================================== *
 *  multipoles — about the centre of charge (Q != 0) or the mean       *
 *  position (Q = 0); the coefficients along a ray two ways            *
 * ================================================================== */
function moments(ch){
  const n=ch.length;
  if(!n) return {c:[0,0],Q:0,p:[0,0],Qxx:0,Qxy:0,Qyy:0,dmax:0,sumAbs:0};
  const Q=netCharge(ch); let cx=0, cy=0, sa=0;
  if(Math.abs(Q)>1e-12){ for(const c of ch){ cx+=c.q*c.x; cy+=c.q*c.y; } cx/=Q; cy/=Q; }
  else { for(const c of ch){ cx+=c.x; cy+=c.y; } cx/=n; cy/=n; }
  let px=0, py=0, qxx=0, qxy=0, qyy=0, dmax=0;
  for(const c of ch){ const dx=c.x-cx, dy=c.y-cy, d2=dx*dx+dy*dy;
    px+=c.q*dx; py+=c.q*dy; qxx+=c.q*(3*dx*dx-d2); qxy+=c.q*3*dx*dy; qyy+=c.q*(3*dy*dy-d2);
    dmax=Math.max(dmax,Math.sqrt(d2)); sa+=Math.abs(c.q); }
  return {c:[cx,cy],Q,p:[px,py],Qxx:qxx,Qxy:qxy,Qyy:qyy,dmax,sumAbs:sa};
}
function legendreP(lmax,x){ const p=[1,x]; for(let l=1;l<lmax;l++) p.push(((2*l+1)*x*p[l]-l*p[l-1])/(l+1)); return p.slice(0,lmax+1); }
/* V(c + r n) = sum_l c_l / r^(l+1) for r > max|d_i|, with
   c_l = k sum_i q_i |d_i|^l P_l(n . d_i/|d_i|)  (the Legendre route) */
function seriesCoeffs(ch,th,lmax){
  const M=moments(ch), n=[Math.cos(th),Math.sin(th)], cs=new Array(lmax+1).fill(0);
  for(const c of ch){
    const dx=c.x-M.c[0], dy=c.y-M.c[1], d=Math.hypot(dx,dy);
    if(d===0){ cs[0]+=KNC*c.q; continue; }
    const pl=legendreP(lmax,(dx*n[0]+dy*n[1])/d);
    let dl=1; for(let l=0;l<=lmax;l++){ cs[l]+=KNC*c.q*dl*pl[l]; dl*=d; }
  }
  return cs;
}
/* the same first three from the moments (the tensor route) */
function tensorCoeffs(M,th){
  const n=[Math.cos(th),Math.sin(th)];
  return [KNC*M.Q, KNC*(M.p[0]*n[0]+M.p[1]*n[1]), KNC*0.5*(M.Qxx*n[0]*n[0]+2*M.Qxy*n[0]*n[1]+M.Qyy*n[1]*n[1])];
}
const ORDER_NAME=['monopole','dipole','quadrupole','octupole','hexadecapole'];
/* the lowest order with a coefficient above rounding along this ray */
function leadingOrder(cs,M){
  for(let l=0;l<cs.length;l++) if(Math.abs(cs[l])>1e-9*KNC*M.sumAbs*Math.pow(Math.max(M.dmax,1e-3),l)) return l;
  return null;
}
/* the far field along the ray at angle th (degrees): samples of the exact V,
   the leading term, and r^(l0+1) V(r) taken to its limit by Richardson
   extrapolation with the order gap m to the next non-zero coefficient */
const FAR_RLO=0.1, FAR_RHI=5000, FAR_N=241;
function farField(ch,thDeg){
  const M=moments(ch), th=thDeg*DEG, n=[Math.cos(th),Math.sin(th)], cs=seriesCoeffs(ch,th,8), l0=leadingOrder(cs,M);
  const rs=[], Vs=[], lead=[], ratio=[];
  for(let k=0;k<FAR_N;k++){
    const r=FAR_RLO*Math.pow(FAR_RHI/FAR_RLO,k/(FAR_N-1)), v=potentialClean(ch,M.c[0]+r*n[0],M.c[1]+r*n[1]);
    rs.push(r); Vs.push(v);
    lead.push(l0===null?NaN:cs[l0]/Math.pow(r,l0+1));
    ratio.push(l0===null?NaN:Math.pow(r,l0+1)*v/cs[l0]);
  }
  let m=null, lim=null, rate=null;
  if(l0!==null){
    for(let l=l0+1;l<cs.length;l++) if(Math.abs(cs[l])>1e-9*KNC*M.sumAbs*Math.pow(Math.max(M.dmax,1e-3),l)){ m=l-l0; break; }
    const f=r=>Math.pow(r,l0+1)*potentialAt(ch,M.c[0]+r*n[0],M.c[1]+r*n[1]);
    if(m===null){ lim=f(100); }
    else { const g=Math.pow(2,m); lim=(g*f(100)-f(50))/(g-1); rate=(f(50)-cs[l0])/(f(100)-cs[l0]); }
  }
  return {M,th:thDeg,n,cs,l0,m,lim,rate,rs,Vs,lead,ratio};
}

/* ================================================================== *
 *  the tape: V(A) - V(B), and the line integral of E that equals it    *
 * ================================================================== */
/* Gauss-Legendre nodes and weights by Newton on P_n (never typed) */
function gaussLegendre(n){
  const x=[], w=[];
  for(let i=1;i<=n;i++){
    let z=Math.cos(PI*(i-0.25)/(n+0.5)), dp=0;
    for(let it=0;it<100;it++){
      let p0=1, p1=z;
      for(let l=1;l<n;l++){ const p2=((2*l+1)*z*p1-l*p0)/(l+1); p0=p1; p1=p2; }
      dp=n*(z*p1-p0)/(z*z-1);
      const dz=p1/dp; z-=dz; if(Math.abs(dz)<1e-16) break;
    }
    x.push(z); w.push(2/((1-z*z)*dp*dp));
  }
  return {x,w};
}
const GL8=gaussLegendre(8);
function lineIntegralE(ch,ax,ay,bx,by,nPan){
  nPan=nPan||40;
  const L=Math.hypot(bx-ax,by-ay); if(!(L>0)) return 0;
  const tx=(bx-ax)/L, ty=(by-ay)/L; let s=0;
  for(let p=0;p<nPan;p++){ const s0=L*p/nPan, s1=L*(p+1)/nPan, hm=(s1-s0)/2, mid=(s0+s1)/2;
    for(let k=0;k<GL8.x.length;k++){ const ss=mid+hm*GL8.x[k], f=fieldAt(ch,ax+ss*tx,ay+ss*ty); s+=GL8.w[k]*hm*(f.ex*tx+f.ey*ty); } }
  return s;
}
function tapeModel(ch,t){
  const L=Math.hypot(t.bx-t.ax,t.by-t.ay), VA=potentialClean(ch,t.ax,t.ay), VB=potentialClean(ch,t.bx,t.by);
  return {L,cm:100*L,VA,VB,dV:VA-VB};
}

/* ================================================================== *
 *  superposition — each charge's term at a point                      *
 * ================================================================== */
function contributions(ch,x,y){
  return ch.map((c,i)=>{ const dx=x-c.x, dy=y-c.y, r2=dx*dx+dy*dy, r=Math.sqrt(r2), r3=r2*r;
    return {i,q:c.q,r,V:KNC*c.q/r,ex:KNC*c.q*dx/r3,ey:KNC*c.q*dy/r3}; });
}

/* ================================================================== *
 *  the landscape: V on a vertex grid over the plane, clipped           *
 * ================================================================== */
const LAND_NX=64, LAND_NY=40, LAND_HZ=1.25;      /* 65 x 41 vertices; LAND_HZ metres of height at the clip */
/* the camera distance that frames the surface's actual box (8 m x 5 m x
   2 LAND_HZ): bisected until all 8 corners project inside the middle 90 % of
   the panel (the bounding sphere of so flat a box left the surface small);
   the zoom then divides it */
function landFitDist(b,theta,phi){
  const corners=[]; for(const x of [PLANE.x0,PLANE.x1]) for(const y of [PLANE.y0,PLANE.y1]) for(const z of [-LAND_HZ,LAND_HZ]) corners.push([x,y,z]);
  const ix0=b.x+0.05*b.w, ix1=b.x+0.95*b.w, iy0=b.y+0.05*b.h, iy1=b.y+0.95*b.h;
  const fits=D=>{ const C=boxCamera(b,theta,phi,D,[0,0,0]); for(const p of corners){ const q=C.P(p); if(!q||q.x<ix0||q.x>ix1||q.y<iy0||q.y>iy1) return false; } return true; };
  let lo=1, hi=400; for(let it=0;it<60;it++){ const m=0.5*(lo+hi); if(fits(m)) hi=m; else lo=m; }
  return hi;
}
function landHeight(V,vcap){ const c=clamp(V,-vcap,vcap); return (c===c?c:0)/vcap*LAND_HZ; }
function landGrid(ch,vcap){
  const nx=LAND_NX, ny=LAND_NY, v=new Float64Array((nx+1)*(ny+1)), z=new Float64Array((nx+1)*(ny+1));
  let clipped=0;
  for(let j=0;j<=ny;j++) for(let i=0;i<=nx;i++){
    const x=PLANE.x0+(PLANE.x1-PLANE.x0)*i/nx, y=PLANE.y0+(PLANE.y1-PLANE.y0)*j/ny, V=potentialAt(ch,x,y);
    v[j*(nx+1)+i]=V; z[j*(nx+1)+i]=landHeight(V,vcap); if(!(Math.abs(V)<=vcap)) clipped++;
  }
  return {nx,ny,v,z,vcap,clipped};
}

/* ================================================================== *
 *  marching squares — contours of a sampled scalar                     *
 *  (the house implementation from dipole_radiation.html, unchanged)   *
 * ================================================================== */
function marchingSquares(grid, nx, ny, x0, z0, cs, level){
  const segs=[];
  const lerp=(pa,pb,va,vb)=>{ const f=(level-va)/((vb-va)||1e-30);
    return [pa[0]+(pb[0]-pa[0])*f, pa[1]+(pb[1]-pa[1])*f]; };
  for (let j=0;j<ny-1;j++){
    for (let i=0;i<nx-1;i++){
      const v00=grid[j*nx+i],   v10=grid[j*nx+i+1],
            v01=grid[(j+1)*nx+i], v11=grid[(j+1)*nx+i+1];
      let code=0;
      if (v00>level) code|=1;
      if (v10>level) code|=2;
      if (v11>level) code|=4;
      if (v01>level) code|=8;
      if (code===0||code===15) continue;
      const x=x0+i*cs, z=z0+j*cs;
      const p00=[x,z], p10=[x+cs,z], p01=[x,z+cs], p11=[x+cs,z+cs];
      const eB=()=>lerp(p00,p10,v00,v10), eR=()=>lerp(p10,p11,v10,v11),
            eT=()=>lerp(p01,p11,v01,v11), eL=()=>lerp(p00,p01,v00,v01);
      const put=(a,b)=>{ segs.push(a[0],a[1],b[0],b[1]); };
      switch(code){
        case 1:  put(eL(),eB()); break;
        case 2:  put(eB(),eR()); break;
        case 3:  put(eL(),eR()); break;
        case 4:  put(eR(),eT()); break;
        case 5:{ const mid=(v00+v10+v01+v11)/4;
                 if (mid>level){ put(eL(),eT()); put(eB(),eR()); }
                 else { put(eL(),eB()); put(eR(),eT()); } break; }
        case 6:  put(eB(),eT()); break;
        case 7:  put(eL(),eT()); break;
        case 8:  put(eT(),eL()); break;
        case 9:  put(eT(),eB()); break;
        case 10:{ const mid=(v00+v10+v01+v11)/4;
                 if (mid>level){ put(eT(),eR()); put(eL(),eB()); }
                 else { put(eT(),eL()); put(eB(),eR()); } break; }
        case 11: put(eT(),eR()); break;
        case 12: put(eR(),eL()); break;
        case 13: put(eR(),eB()); break;
        case 14: put(eB(),eL()); break;
      }
    }
  }
  return segs;
}
/* the evenly spaced family for the field-lines view: V on a 4-cm grid over
   the plane, contoured at every dV up to the +-40 V saturation (and at 0) */
const FAM_DX=0.04;
function equipotentialFamily(ch,dV){
  const nx=Math.round((PLANE.x1-PLANE.x0)/FAM_DX)+1, ny=Math.round((PLANE.y1-PLANE.y0)/FAM_DX)+1, g2=new Float64Array(nx*ny);
  for(let j=0;j<ny;j++) for(let i=0;i<nx;i++) g2[j*nx+i]=vSafe(potentialAt(ch,PLANE.x0+i*FAM_DX,PLANE.y0+j*FAM_DX));
  const levels=[0]; for(let k=1;k*dV<=V_SAT+1e-9;k++){ levels.push(k*dV,-k*dV); }
  const out=[];
  for(const L of levels){ const s=marchingSquares(g2,nx,ny,PLANE.x0,PLANE.y0,FAM_DX,L); if(s.length) out.push({V:L,segs:s}); }
  return out;
}
