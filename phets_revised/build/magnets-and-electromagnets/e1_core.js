
/* ================================================================== *
 *  the magnetism engine: Bulirsch's cel, the finite solenoid (the bar *
 *  magnet), the current loop (the coil), sources in the world frame,  *
 *  the field meter's readings, the needle grid, the compass rotor     *
 *  (shared by the magnets-and-electromagnets family; the twin is      *
 *  build/magnets-and-electromagnets/derive.py)                        *
 * ================================================================== */
const D2R=Math.PI/180, R2D=180/Math.PI;     /* D2R turns degrees INTO radians (Known-bad: DEG/RAD read backwards) */
const MU0=1.25663706127e-6;                 /* N/A^2, CODATA 2022 (NIST); measured since the 2019 SI */
const G_PER_T=1e4;
const MAG_L=250, MAG_R=25, MAG_B=125;       /* mm. PhET's bar is 250 x 50 x 50: a horizontal cylinder, radius 25 */
/* mu0 m / 4 pi per unit source: the magnet's moment is M V = M pi R^2 L, so mu0 m/4pi =
   S R^2 L/4 (G mm^3 per G); N loops carry m = N I pi a^2, so mu0 m/4pi = mu0 I N a^2/4. */
const MAG_DIP=MAG_R*MAG_R*MAG_L/4;
const S_MAX=300;                            /* G: PhET's MAGNET_STRENGTH_RANGE is (0, 300) */
const KAPPA=6.25, GAMMA_C=2;                /* compass rotor: PhET's 0.01/G per frame^2 and 0.08 per frame at 25 frames/s */
const FLIP_KICK=0.75;                       /* rad/s: PhET's startMovingNow, 0.03 rad per frame at 25 frames/s */
const NEEDLE_SPACING=40, NEEDLE_LEN=25, FIELD_SCALE=2.7;   /* PhET's FieldNode: 40-px grid, 25-px needles, alpha exponent 1/2.7 */
const LAYOUT_W=1024, LAYOUT_H=618;          /* PhET's layout bounds, mm here (1 PhET px = 1 mm) */

/* Bulirsch's generalized complete elliptic integral
     cel(kc,p,c,s) = int_0^{pi/2} (c cos^2 + s sin^2) / ((cos^2 + p sin^2) sqrt(cos^2 + kc^2 sin^2)) dphi
   (the algorithm as listed by Derby & Olbert, Am. J. Phys. 78, 229 (2010)).  K(k) = cel(kc,1,1,1),
   E(k) = cel(kc,1,1,kc^2).  Converges quadratically; kc = 0 is the logarithmic singularity. */
function cel(kc,p,c,s){
  if(kc===0) return NaN;
  let k=Math.abs(kc), pp=p, cc=c, ss=s, em=1, f, g, q;
  if(p>0){ pp=Math.sqrt(p); ss=s/pp; }
  else { f=kc*kc; q=1-f; g=1-pp; f=f-pp; q=q*(ss-c*pp); pp=Math.sqrt(f/g); cc=(c-ss)/g; ss=-q/(g*g*pp)+cc*pp; }
  f=cc; cc=cc+ss/pp; g=k/pp; ss=2*(ss+f*g); pp=g+pp; g=em; em=k+em;
  let kk=k, it=0;
  while(Math.abs(g-k)>g*1e-15){
    k=2*Math.sqrt(kk); kk=k*em; f=cc; cc=cc+ss/pp; g=kk/pp; ss=2*(ss+f*g); pp=g+pp; g=em; em=k+em;
    if(++it>60) return NaN;
  }
  return (Math.PI/2)*(ss+cc*em)/(em*(em+pp));
}
function ellK(kc){ return cel(kc,1,1,1); }
function ellE(kc){ return cel(kc,1,1,kc*kc); }
/* n-point Gauss-Legendre on [-1, 1], nodes by Newton on P_n (asserted: exact for x^(2n-2)) */
const GL_CACHE={};
function gaussLegendre(n){
  if(GL_CACHE[n]) return GL_CACHE[n];
  const x=[], w=[];
  for(let i=0;i<n;i++){
    let z=Math.cos(Math.PI*(i+0.75)/(n+0.5)), pp=0;
    for(let it=0;it<100;it++){
      let p1=1, p2=0;
      for(let j=0;j<n;j++){ const p3=p2; p2=p1; p1=((2*j+1)*z*p2-j*p3)/(j+1); }
      pp=n*(z*p1-p2)/(z*z-1);
      const dz=p1/pp; z-=dz; if(Math.abs(dz)<1e-16) break;
    }
    x.push(z); w.push(2/((1-z*z)*pp*pp));
  }
  return (GL_CACHE[n]={x,w});
}

/* The ideal finite solenoid, radius a, half-length b, axis u, centred at 0, in units of mu0 n I
   (Derby & Olbert 2010).  A uniformly magnetised cylinder IS this solenoid for B, everywhere:
   its bound current K = M x n flows round the side wall (Ampere's equivalence).  Returns
   [B_rho, B_u].  On the side wall itself (rho = a, |u| < b) it returns the mean of the two
   sides (B_u jumps by exactly mu0 n I there); at the rims (rho = a, |u| = b) the field is
   logarithmically singular and the point is nudged 1e-9 a outward. */
function solB(rho,u,a,b){
  if(Math.abs(rho-a)<1e-9*a && Math.abs(Math.abs(u)-b)<1e-9*a) rho=a*(1+1e-9);
  const zp=u+b, zm=u-b, ra=rho+a;
  const sp=Math.sqrt(zp*zp+ra*ra), sm=Math.sqrt(zm*zm+ra*ra);
  const g=(a-rho)/ra, g2=g*g;
  const kp=Math.sqrt(zp*zp+(a-rho)*(a-rho))/sp, km=Math.sqrt(zm*zm+(a-rho)*(a-rho))/sm;
  const Br=(a/sp*cel(kp,1,1,-1)-a/sm*cel(km,1,1,-1))/Math.PI;
  const Bu=a/ra*(zp/sp*cel(kp,g2,1,g)-zm/sm*cel(km,g2,1,g))/Math.PI;
  return [Br,Bu];
}
/* the same on the axis, in closed form (asserted equal to solB(0,u) in selfTest) */
function solAxis(u,a,b){ return 0.5*((u+b)/Math.hypot(u+b,a)-(u-b)/Math.hypot(u-b,a)); }

/* #emag */
/* A circular current loop, radius a, at z = 0, axis z, unit mu0 I (field in 1/mm).  Returns
   [B_rho, B_z, Psi] with Psi = rho A_phi the flux function (the flux through the coaxial circle
   through the point is 2 pi Psi; field lines are its level sets).  B_z is the textbook K,E
   form.  B_rho and Psi are NOT: the textbook forms subtract two nearly equal elliptic
   integrals near the axis (B_rho is 11% wrong at rho = 1e-6 a, derive.py), so both are
   written as single cel integrals with no cancellation:
     B_rho = a z cel(kc,1,1,-kc^2) / (pi D^1.5 kc^2),   Psi = -a rho cel(kc,1,1,-1) / (pi sqrt D). */
function loopB(rho,z,a){
  const D=(a+rho)*(a+rho)+z*z, d2=(a-rho)*(a-rho)+z*z, kc2=d2/D, kc=Math.sqrt(kc2);
  const K=cel(kc,1,1,1), E=cel(kc,1,1,kc2);
  const Bz=(K+(a*a-rho*rho-z*z)/d2*E)/(2*Math.PI*Math.sqrt(D));
  const Br=a*z*cel(kc,1,1,-kc2)/(Math.PI*D*Math.sqrt(D)*kc2);
  const Psi=-a*rho/Math.sqrt(D)*cel(kc,1,1,-1)/Math.PI;
  return [Br,Bz,Psi];
}
function loopAxis(z,a){ return a*a/(2*Math.pow(a*a+z*z,1.5)); }
/* #endemag */

/* ---------------- sources in the world frame (mm, gauss) ---------------- *
 * magnet: {kind:'magnet', x, y, ang, S}  centre, axis angle (N end along ang), strength S = mu0 M in G.
 * coil:   {kind:'coil', x, y, N, I}      centre, loops along +x at the winding's pitch, current I in A
 *         (positive I makes +x the north end).  Fields are 3-D; the page is the plane z = 0. */
function magnetLocal(m,px,py,pz){
  const c=Math.cos(m.ang), s=Math.sin(m.ang), dx=px-m.x, dy=py-m.y, dz=pz||0;
  const u=dx*c+dy*s, vx=dx-u*c, vy=dy-u*s, vz=dz;
  return {u,vx,vy,vz,rho:Math.sqrt(vx*vx+vy*vy+vz*vz),c,s};
}
function magnetField(m,px,py,pz){
  const L=magnetLocal(m,px,py,pz), b=solB(L.rho,L.u,MAG_R,MAG_B);
  const Br=m.S*b[0], Bu=m.S*b[1];
  if(L.rho>0) return [Bu*L.c+Br*L.vx/L.rho, Bu*L.s+Br*L.vy/L.rho, Br*L.vz/L.rho];
  return [Bu*L.c, Bu*L.s, 0];
}
function insideMagnet(m,px,py){ const L=magnetLocal(m,px,py,0); return Math.abs(L.u)<=MAG_B && L.rho<=MAG_R; }
function sourceField(src,px,py,pz){
  if(src.kind==='magnet') return magnetField(src,px,py,pz);
/* #emag */
  if(src.kind==='coil') return coilField(src,px,py,pz);
/* #endemag */
  throw new Error('no such source: '+src.kind);
}
/* the angle of the field in the page, degrees in (-180, 180] (PhET's field meter theta) */
function fieldAngleDeg(B){ return Math.atan2(B[1],B[0])*R2D; }

/* ---------------- the field meter ---------------- *
 * The meter reads the model at its crosshair: no smoothing, no grid.  Units as PhET's
 * preference: G with two decimals ('~ 0 G' below 0.01 G), or T in scientific notation. */
function meterReading(src,x,y){
  const B=sourceField(src,x,y,0);
  return {Bx:B[0],By:B[1],B:Math.hypot(B[0],B[1]),ang:(B[0]===0&&B[1]===0)?NaN:fieldAngleDeg(B)};
}
function fmtField(v,units){
  if(!isFinite(v)) return '—';
  if(units==='T'){
    if(v===0) return '0 T';
    const t=(v/G_PER_T).toExponential(2).split('e');
    return t[0]+' × 10^'+(+t[1])+' T';
  }
  const a=Math.abs(v);
  if(a>0&&a<0.01) return '~ 0 G';
  return (v===0?'0':v.toFixed(2))+' G';
}
function fmtAngle(deg){ return isFinite(deg)?deg.toFixed(2)+'°':'—'; }

/* ---------------- the needle grid (PhET's FieldNode) ---------------- *
 * one needle every 40 mm, pointing along B, brightness min(1, 2 (|B|/300 G)^(1/2.7)) --
 * PhET's own mapping, a display choice, not physics (said on the canvas) */
function needleAlpha(Bmag){ return Math.min(1,2*Math.pow(Bmag/S_MAX,1/FIELD_SCALE)); }
function needleGrid(src,x0,y0,x1,y1){
  const out=[];
  const i0=Math.ceil((x0-20)/NEEDLE_SPACING), i1=Math.floor((x1-20)/NEEDLE_SPACING);
  const j0=Math.ceil((y0-20)/NEEDLE_SPACING), j1=Math.floor((y1-20)/NEEDLE_SPACING);
  for(let i=i0;i<=i1;i++) for(let j=j0;j<=j1;j++){
    const x=20+i*NEEDLE_SPACING, y=20+j*NEEDLE_SPACING, B=sourceField(src,x,y,0), mg=Math.hypot(B[0],B[1]);
    if(!(mg>0)||!isFinite(mg)) continue;
    out.push({x,y,ang:Math.atan2(B[1],B[0]),alpha:needleAlpha(mg),B:mg});
  }
  return out;
}

/* ---------------- the compass: a damped rotor (MODELLED) ---------------- *
 *   phi'' = kappa |B| sin(theta_B - phi) - gamma phi'
 * with PhET's kinematic-compass constants in SI: kappa = 6.25 per G per s^2, gamma = 2 per s.
 * Small swings ring at omega0 = sqrt(kappa |B|) (period 2.5 s at 1 G, 0.26 s at 100 G); PhET
 * snaps the needle to the field above 10 G, this page integrates the rotor at every field.
 * RK4 with steps <= 0.1/omega0; the field may depend on time (AC coil, turning magnet), so it
 * is sampled at each RK4 stage.  The energy per moment of inertia,
 *   E = phi'^2/2 + kappa |B| (1 - cos(phi - theta_B)),
 * and the work done by the damping, W = int gamma phi'^2 dt, are integrated as extra states
 * INSIDE the same RK4 stages, so E + W is conserved to the integrator's own accuracy in a
 * steady field (Known-bad: a ledger kept beside the integrator drifts). */
function rotorDeriv(y,Bv,kap,gam){
  const Bm=Math.hypot(Bv[0],Bv[1]), th=Math.atan2(Bv[1],Bv[0]);
  return [y[1], kap*Bm*Math.sin(th-y[0])-gam*y[1], gam*y[1]*y[1]];
}
function rotorAdvance(r,Bfun,t,dt,kap,gam){
  kap=(kap===undefined)?KAPPA:kap; gam=(gam===undefined)?GAMMA_C:gam;
  let Bmax=0; for(const tt of [t,t+dt/2,t+dt]){ const B=Bfun(tt); Bmax=Math.max(Bmax,Math.hypot(B[0],B[1])); }
  const w0=Math.sqrt(kap*Bmax);
  const n=Math.max(1,Math.ceil(dt*w0/0.1), Math.ceil(dt*gam/0.1));
  const h=dt/n;
  let y=[r.phi,r.om,r.W||0];
  for(let i=0;i<n;i++){
    const t0=t+i*h, Ba=Bfun(t0), Bb=Bfun(t0+h/2), Bc=Bfun(t0+h);
    const k1=rotorDeriv(y,Ba,kap,gam);
    const y2=[y[0]+h/2*k1[0],y[1]+h/2*k1[1],y[2]+h/2*k1[2]], k2=rotorDeriv(y2,Bb,kap,gam);
    const y3=[y[0]+h/2*k2[0],y[1]+h/2*k2[1],y[2]+h/2*k2[2]], k3=rotorDeriv(y3,Bb,kap,gam);
    const y4=[y[0]+h*k3[0],y[1]+h*k3[1],y[2]+h*k3[2]], k4=rotorDeriv(y4,Bc,kap,gam);
    for(let j=0;j<3;j++) y[j]+=h/6*(k1[j]+2*k2[j]+2*k3[j]+k4[j]);
  }
  r.phi=y[0]; r.om=y[1]; r.W=y[2];
  return n;
}
function rotorEnergy(r,Bv,kap){
  kap=(kap===undefined)?KAPPA:kap;
  const Bm=Math.hypot(Bv[0],Bv[1]), th=Math.atan2(Bv[1],Bv[0]);
  return r.om*r.om/2+kap*Bm*(1-Math.cos(r.phi-th));
}
/* wrap an angle to (-pi, pi] (the needle is drawn with it; the rotor state keeps the winding) */
function wrapPi(a){ a=(a+Math.PI)%(2*Math.PI); if(a<0) a+=2*Math.PI; return a-Math.PI; }
