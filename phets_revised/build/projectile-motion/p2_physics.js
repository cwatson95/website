
/* ================================================================== *
 *  physics — PhET's projectiles and air, the vacuum closed forms, the  *
 *  drag integrator and its playback, and the exact hodograph route     *
 *  the suite checks the integrator against                             *
 * ================================================================== */
/* ---- PhET's values: projectile-motion_en.html 1.0.34 ---------------------- */
const G_EARTH=9.81;                               /* ProjectileMotionConstants.GRAVITY_ON_EARTH */
const LIM={h:[0,15], th:[-90,90], v0:[0,30], alt:[0,5000], g:[5,20], cd:[0.04,1]};
const TARGET_X0=15, TARGET_W=3;                   /* TARGET_X_DEFAULT, TARGET_WIDTH (m) */
const DOT=0.1, BIG_DOT_EVERY=10;                  /* TIME_PER_MINOR_DOT 100 ms, TIME_PER_MAJOR_DOT 1000 ms */
const MAX_FLYING=3, MAX_TRAJ=5, SLOW=0.33;        /* MAX_NUMBER_OF_FLYING_PROJECTILES, _TRAJECTORIES; slow motion */
/* ProjectileObjectType: mass kg, diameter m, drag coefficient, and the Lab
   screen's slider range and rounding for mass and diameter.  The fill and
   the outline shape are this file's own drawing, not PhET's images. */
const OBJECTS=[
  {id:'cannonball', name:'cannonball', m:17.6, d:0.18, cd:0.47, mR:[1,31,0.01],   dR:[0.1,1,0.01],  fill:'#5b6272', shape:'ball'},
  {id:'tankShell',  name:'tank shell', m:42,   d:0.15, cd:0.06, mR:[5,200,1],     dR:[0.1,1,0.01],  fill:'#8f9a6a', shape:'shell'},
  {id:'golfBall',   name:'golf ball',  m:0.05, d:0.04, cd:0.25, mR:[0.01,5,0.01], dR:[0.01,1,0.01], fill:'#eef0f4', shape:'ball'},
  {id:'baseball',   name:'baseball',   m:0.15, d:0.07, cd:0.35, mR:[0.01,5,0.01], dR:[0.01,1,0.01], fill:'#e2dccd', shape:'ball'},
  {id:'football',   name:'football',   m:0.41, d:0.17, cd:0.05, mR:[0.01,5,0.01], dR:[0.01,1,0.01], fill:'#9a6038', shape:'spheroid'},
  {id:'pumpkin',    name:'pumpkin',    m:5,    d:0.37, cd:0.6,  mR:[1,1000,1],    dR:[0.1,3,0.01],  fill:'#e07a26', shape:'ball'},
  {id:'human',      name:'human',      m:70,   d:0.5,  cd:0.6,  mR:[10,200,1],    dR:[0.1,1.5,0.1], fill:'#c9a27a', shape:'ball'},
  {id:'piano',      name:'piano',      m:400,  d:2.2,  cd:1.2,  mR:[50,1000,1],   dR:[0.5,3,0.1],   fill:'#3b3f4a', shape:'box'},
  {id:'car',        name:'car',        m:2000, d:2,    cd:0.55, mR:[100,5000,1],  dR:[0.5,3,0.1],   fill:'#5a7fa0', shape:'box'},
];
const CUSTOM={id:'custom', name:'custom', m:100, d:1, cd:0.47, mR:[1,5000,0.01], dR:[0.01,3,0.01], cdR:[0.04,1,0.01], fill:'#7c8494', shape:'cd'};
/* the Vectors and Drag screens' projectile: PhET's default ProjectileObjectType
   ranges (mass 1..10 by 1, diameter 0.1..1 by 0.1, C_d 0.04..1 by 0.01) */
const SCREEN_OBJ={id:'sphere', name:'the 5-kg sphere', m:5, d:0.8, cd:0.47, mR:[1,10,1], dR:[0.1,1,0.1], cdR:[0.04,1,0.01], fill:'#7c8494', shape:'cd'};
function objById(id){
  if(id==='custom') return CUSTOM;
  if(id==='sphere') return SCREEN_OBJ;
  const o=OBJECTS.find(q=>q.id===id);
  if(!o) throw new Error('unknown projectile "'+id+'"');
  return o;
}

/* ---- the air ------------------------------------------------------------------
   NASA Glenn Research Center, "Earth Atmosphere Model" (metric), troposphere —
   PhET's calculateAirDensity: T = 15.04 - 0.00649 h (deg C), p = 101.29
   [(T + 273.1)/288.08]^5.256 (kPa), rho = p/(0.2869 (T + 273.1)).  PhET's
   other two branches start at 11 km; the slider stops at 5 km, so only this
   one is reachable and only this one is here. */
function airDensity(alt){
  const T=15.04-0.00649*alt;
  const p=101.29*Math.pow((T+273.1)/288.08,5.256);
  return p/(0.2869*(T+273.1));
}
/* the ISA / US Standard Atmosphere 1976 troposphere, printed beside it */
function isaDensity(alt){
  const T0=288.15, L=0.0065, R=287.05287, g0=9.80665, T=T0-L*alt;
  return 101325*Math.pow(T/T0,g0/(R*L))/(R*T);
}
/* a_drag = -k |v| v with k = rho C_d A / 2m, A = pi d^2/4 (per metre) */
function dragK(m,d,cd,rho){ return rho*cd*(PI*d*d/4)/(2*m); }
/* v_t = sqrt(g/k): the drag balances the weight.  The same number is
   sqrt(2mg/(rho C_d A)); selfTest asserts the two spellings agree. */
function terminalSpeed(g,k){ return k>0?Math.sqrt(g/k):Infinity; }

/* ---- vacuum: everything in closed form ----------------------------------------- */
function vacuum(h,thDeg,v0,g){
  const th=thDeg*DEG, u=v0*Math.cos(th), w=v0*Math.sin(th);
  const T=(h<=0&&w<=0)?0:(w+Math.sqrt(w*w+2*g*h))/g;
  const vy=w-g*T, vL=Math.sqrt(u*u+vy*vy);
  const apex=w>0?{t:w/g, x:u*w/g, y:h+w*w/(2*g)}:null;
  return {T, R:u*T, H:apex?apex.y:h, apex, vx:u, vy, vL, angL:vL>0?Math.atan2(-vy,u)*RAD:NaN};
}
/* the best angle from a height h: tan th* = v0/sqrt(v0^2 + 2gh), R* = v0 sqrt(v0^2 + 2gh)/g */
function vacuumOptimum(h,v0,g){
  const s=Math.sqrt(v0*v0+2*g*h);
  return {th:Math.atan2(v0,s)*RAD, R:v0*s/g};
}
/* the parabola of safety: the envelope of every vacuum trajectory at speed v0 */
function envelopeY(x,h,v0,g){ return h+v0*v0/(2*g)-g*x*x/(2*v0*v0); }
function vacuumPath(h,thDeg,v0,g,n){
  const V=vacuum(h,thDeg,v0,g), th=thDeg*DEG, xs=[], ys=[];
  for(let i=0;i<=n;i++){ const t=V.T*i/n; xs.push(v0*Math.cos(th)*t); ys.push(h+v0*Math.sin(th)*t-0.5*g*t*t); }
  return {xs,ys};
}

/* ---- the drag integrator ---------------------------------------------------------
   State s = [x, y, vx, vy, w]: w is the energy per kilogram the air has taken,
   dw/dt = k|v|^3, carried as a fifth state INSIDE the RK4 stages so the ledger
   e_k + g y + w = e_0 holds to the integrator's truncation, not to a quadrature
   laid over it (Known-bad, cart_pendulum).  The step is h = min(H_MAX,
   C_STEP/(k|v|)), cut so a step ends exactly on every 0.1-s dot; the apex and
   the ground are found by bisecting the partial step.  build/projectile-motion/
   derive.py is this function's Python twin, line for line. */
const H_MAX=0.002, C_STEP=0.005, N_BIS=60, STEP_CAP=2000000;
function rk4s(s,h,g,k){
  const x=s[0], y=s[1], vx=s[2], vy=s[3], w=s[4];
  let sp=Math.sqrt(vx*vx+vy*vy), kd=k*sp;
  const a1=-kd*vx, b1=-g-kd*vy, p1=kd*sp*sp;
  const vx2=vx+0.5*h*a1, vy2=vy+0.5*h*b1;
  sp=Math.sqrt(vx2*vx2+vy2*vy2); kd=k*sp;
  const a2=-kd*vx2, b2=-g-kd*vy2, p2=kd*sp*sp;
  const vx3=vx+0.5*h*a2, vy3=vy+0.5*h*b2;
  sp=Math.sqrt(vx3*vx3+vy3*vy3); kd=k*sp;
  const a3=-kd*vx3, b3=-g-kd*vy3, p3=kd*sp*sp;
  const vx4=vx+h*a3, vy4=vy+h*b3;
  sp=Math.sqrt(vx4*vx4+vy4*vy4); kd=k*sp;
  const a4=-kd*vx4, b4=-g-kd*vy4, p4=kd*sp*sp;
  return [x+h/6*(vx+2*vx2+2*vx3+vx4), y+h/6*(vy+2*vy2+2*vy3+vy4),
          vx+h/6*(a1+2*a2+2*a3+a4), vy+h/6*(b1+2*b2+2*b3+b4), w+h/6*(p1+2*p2+2*p3+p4)];
}
function pushState(F,t,s){ F.t.push(t); F.x.push(s[0]); F.y.push(s[1]); F.vx.push(s[2]); F.vy.push(s[3]); F.w.push(s[4]); }
/* L = {h, th (deg), v0};  E = {g, k};  opt.from = [t, x, y, vx, vy, w] continues
   from a node; opt.cliff flies on past y = 0 (the ground is recorded, not
   obeyed) until opt.tEnd, a multiple of DOT. */
function flight(L,E,opt){
  opt=opt||{};
  const g=E.g, k=E.k, cliff=!!opt.cliff;
  let t, s;
  if(opt.from){ const f=opt.from; t=f[0]; s=[f[1],f[2],f[3],f[4],f[5]]; }
  else { const th=L.th*DEG; t=0; s=[0,L.h,L.v0*Math.cos(th),L.v0*Math.sin(th),0]; }
  const F={t:[t],x:[s[0]],y:[s[1]],vx:[s[2]],vy:[s[3]],w:[s[4]],dots:[],apexI:-1,landI:-1,steps:0,g,k};
  if(Math.abs(t/DOT-Math.round(t/DOT))<1e-9) F.dots.push(0);
  let nd=Math.floor(t/DOT+1e-9)+1;
  if(!cliff&&s[1]<=0&&s[3]<=0){ F.landI=0; return finishFlight(F); }   /* fired into the ground */
  for(;;){
    let hh=H_MAX;
    if(k>0){ const sp=Math.sqrt(s[2]*s[2]+s[3]*s[3]); if(k*sp*hh>C_STEP) hh=C_STEP/(k*sp); }
    const tD=nd*DOT; let hit=false;
    if(t+hh>tD-1e-9){ hh=tD-t; hit=true; }
    const ns=rk4s(s,hh,g,k); F.steps++;
    if(s[3]>0&&ns[3]<=0){                                   /* the apex is inside this step */
      let lo=0, hi=hh;
      for(let i=0;i<N_BIS;i++){ const m=0.5*(lo+hi); if(rk4s(s,m,g,k)[3]>0) lo=m; else hi=m; }
      pushState(F,t+hi,rk4s(s,hi,g,k)); F.apexI=F.t.length-1;
    }
    if(F.landI<0&&ns[1]<=0&&(s[1]>0||s[3]>0)){              /* and the ground */
      let lo=0, hi=hh;
      for(let i=0;i<N_BIS;i++){ const m=0.5*(lo+hi); if(rk4s(s,m,g,k)[1]>0) lo=m; else hi=m; }
      const Ls=rk4s(s,hi,g,k); Ls[1]=0;
      pushState(F,t+hi,Ls); F.landI=F.t.length-1;
      if(!cliff) return finishFlight(F);
    }
    s=ns;
    if(hit){ t=tD; nd++; } else t=t+hh;
    pushState(F,t,s);
    if(hit) F.dots.push(F.t.length-1);
    if(cliff&&hit&&t>=opt.tEnd-1e-9) return finishFlight(F);
    if(F.steps>STEP_CAP) throw new Error('flight: step cap exceeded');
  }
}
function finishFlight(F){
  const i=F.landI;
  if(i>=0){ const vx=F.vx[i], vy=F.vy[i];
    F.T=F.t[i]; F.R=F.x[i]; F.vL=Math.sqrt(vx*vx+vy*vy); F.angL=F.vL>0?Math.atan2(-vy,vx)*RAD:NaN; F.W=F.w[i]; }
  else { F.T=NaN; F.R=NaN; F.vL=NaN; F.angL=NaN; F.W=NaN; }
  F.H=F.apexI>=0?F.y[F.apexI]:F.y[0];
  F.apex=F.apexI>=0?{t:F.t[F.apexI],x:F.x[F.apexI],y:F.y[F.apexI]}:null;
  return F;
}
/* ---- playback: cubic Hermite between nodes (positions AND velocities) ---- */
function nodeBefore(F,tau){
  const t=F.t; let lo=0, hi=t.length-1;
  if(tau>=t[hi]) return hi;
  while(hi-lo>1){ const m=(lo+hi)>>1; if(t[m]<=tau) lo=m; else hi=m; }
  return lo;
}
function stateAt(F,tau){
  const n=F.t.length;
  if(!(tau>F.t[0])) return {x:F.x[0],y:F.y[0],vx:F.vx[0],vy:F.vy[0],i:0};
  if(tau>=F.t[n-1]) return {x:F.x[n-1],y:F.y[n-1],vx:F.vx[n-1],vy:F.vy[n-1],i:n-1};
  const i=nodeBefore(F,tau), h=F.t[i+1]-F.t[i];
  if(!(h>0)) return {x:F.x[i+1],y:F.y[i+1],vx:F.vx[i+1],vy:F.vy[i+1],i:i+1};
  const s=(tau-F.t[i])/h, s2=s*s, s3=s2*s;
  const h00=2*s3-3*s2+1, h10=s3-2*s2+s, h01=-2*s3+3*s2, h11=s3-s2;
  return {x:h00*F.x[i]+h10*h*F.vx[i]+h01*F.x[i+1]+h11*h*F.vx[i+1],
          y:h00*F.y[i]+h10*h*F.vy[i]+h01*F.y[i+1]+h11*h*F.vy[i+1],
          vx:F.vx[i]+s*(F.vx[i+1]-F.vx[i]), vy:F.vy[i]+s*(F.vy[i+1]-F.vy[i]), i};
}
/* a change of air or gravity mid-flight: keep the path to the last node at
   or before tau and fly on from that node in the new conditions */
function continueFlight(F,tau,E){
  const i=Math.min(nodeBefore(F,tau),F.landI>0?F.landI-1:F.t.length-1);
  const C=flight(null,E,{from:[F.t[i],F.x[i],F.y[i],F.vx[i],F.vy[i],F.w[i]]});
  const cat=(a,b)=>a.slice(0,i+1).concat(b.slice(1));
  const G={t:cat(F.t,C.t),x:cat(F.x,C.x),y:cat(F.y,C.y),vx:cat(F.vx,C.vx),vy:cat(F.vy,C.vy),w:cat(F.w,C.w),
           dots:F.dots.filter(j=>j<=i).concat(C.dots.filter(j=>j>0).map(j=>j+i)),
           apexI:(F.apexI>=0&&F.apexI<=i)?F.apexI:(C.apexI>0?C.apexI+i:-1),
           landI:C.landI>=0?C.landI+i:-1, steps:F.steps+C.steps, g:E.g, k:E.k};
  return finishFlight(G);
}

/* ---- the exact hodograph of quadratic drag ------------------------------------------
   With phi the angle of the velocity, u = v cos(phi) obeys du/dphi = k u^3/(g cos^3 phi),
   so 1/u^2 = 1/u0^2 + (k/g)[F(th) - F(phi)], F(psi) = sin psi/cos^2 psi + ln tan(pi/4 + psi/2)
   (twice the integral of sec^3).  Then dt = -u sec^2(phi) dphi/g, dx = u dt, dy = u tan(phi) dt:
   t, x and y are quadratures over phi, done here by composite Gauss-Legendre.  None of
   this shares a line with the integrator above. */
function hodoF(psi){ const c=Math.cos(psi); return Math.sin(psi)/(c*c)+Math.log(Math.tan(PI/4+psi/2)); }
function hodoU(phi,th,u0,g,k){ return u0/Math.sqrt(1+k*u0*u0/g*(hodoF(th)-hodoF(phi))); }
/* Gauss-Legendre nodes and weights by Newton on P_n — computed, never typed
   (Known-bad: hand-transcribed coefficients fail silently in the tail) */
function gaussLegendre(n){
  const xs=[], ws=[];
  for(let i=1;i<=n;i++){
    let x=Math.cos(PI*(i-0.25)/(n+0.5)), p0=1, p1=x, dp=1;
    for(let it=0;it<100;it++){
      p0=1; p1=x;
      for(let j=2;j<=n;j++){ const p2=((2*j-1)*x*p1-(j-1)*p0)/j; p0=p1; p1=p2; }
      dp=n*(x*p1-p0)/(x*x-1);
      const dx=p1/dp; x-=dx;
      if(Math.abs(dx)<1e-16) break;
    }
    p0=1; p1=x;
    for(let j=2;j<=n;j++){ const p2=((2*j-1)*x*p1-(j-1)*p0)/j; p0=p1; p1=p2; }
    dp=n*(x*p1-p0)/(x*x-1);
    xs.push(x); ws.push(2/((1-x*x)*dp*dp));
  }
  return {xs,ws};
}
const GL10=gaussLegendre(10);
/* t, x, y at velocity angle phi (radians), for a launch at th from height h */
function hodoTXY(phi,th,v0,h,g,k,panels){
  const u0=v0*Math.cos(th), N=panels||48, a=phi, b=th, hw=(b-a)/(2*N);   /* 48: converged, see derive/refvals */
  let it=0, ix=0, iy=0;
  for(let p=0;p<N;p++){
    const c=a+(2*p+1)*hw;
    for(let q=0;q<10;q++){
      const psi=c+hw*GL10.xs[q], wq=hw*GL10.ws[q];
      const u=hodoU(psi,th,u0,g,k), cs=Math.cos(psi), sec2=1/(cs*cs);
      it+=wq*u*sec2; ix+=wq*u*u*sec2; iy+=wq*u*u*Math.tan(psi)*sec2;
    }
  }
  return {t:it/g, x:ix/g, y:h+iy/g};
}
/* the landing: the velocity angle at which y returns to 0 (bisection; y falls
   monotonically once phi < 0).  Valid for launch angles strictly inside
   (-90, 90) degrees and landing angles above 89.9 degrees below horizontal. */
function hodoLanding(L,E){
  const th=L.th*DEG;
  let lo=-89.9*DEG, hi=Math.min(th,0);
  if(!(hodoTXY(lo,th,L.v0,L.h,E.g,E.k).y<0)) return null;
  for(let i=0;i<70;i++){ const m=0.5*(lo+hi); if(hodoTXY(m,th,L.v0,L.h,E.g,E.k).y>0) hi=m; else lo=m; }
  const phi=0.5*(lo+hi), P=hodoTXY(phi,th,L.v0,L.h,E.g,E.k), u=hodoU(phi,th,L.v0*Math.cos(th),E.g,E.k);
  return {phi, angL:-phi*RAD, T:P.t, R:P.x, vL:u/Math.cos(phi)};
}

/* ---- range against angle, and the best angle -------------------------------------- */
function rangeAt(L,E,thDeg){
  if(!(E.k>0)) return vacuum(L.h,thDeg,L.v0,E.g).R;
  return flight({h:L.h,th:thDeg,v0:L.v0},E).R;
}
const GOLD_IT=40;
function optimumAngle(L,E){
  if(!(E.k>0)){ const V=vacuumOptimum(L.h,L.v0,E.g); return {th:V.th,R:V.R}; }
  const f=th=>rangeAt(L,E,th), r=(Math.sqrt(5)-1)/2;
  let a=0, b=90, c=b-r*(b-a), d=a+r*(b-a), fc=f(c), fd=f(d);
  for(let i=0;i<GOLD_IT;i++){
    if(fc>fd){ b=d; d=c; fd=fc; c=b-r*(b-a); fc=f(c); }
    else { a=c; c=d; fc=fd; d=a+r*(b-a); fd=f(d); }
  }
  const th=0.5*(a+b);
  return {th, R:f(th)};
}

/* ---- the target (PhET's Score: three stars inside W/6, two inside W/3, one inside W/2) ---- */
function starsFor(x,xt){
  const d=Math.abs(x-xt);
  return d<=TARGET_W/6?3:(d<=TARGET_W/3?2:(d<=TARGET_W/2?1:0));
}
