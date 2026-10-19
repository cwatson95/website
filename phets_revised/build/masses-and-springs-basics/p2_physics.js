
/* ================================================================== *
 *  PhET's constants, and the damped oscillator in closed form         *
 *  every constant below is read out of PhET's own build 1.0.28        *
 *  (docs/phets/masses-and-springs-basics_en.html) — "PhET's value"    *
 * ================================================================== */

/* MassesAndSpringsConstants, verbatim from the minified build */
const CEILING_Y=1.47, FLOOR_Y=0, SHELF_H=0.02, HOOK_H=0.037, HOOK_C=0.0185;
const L0=0.5;                                  /* DEFAULT_SPRING_LENGTH */
const KMIN=3, KMAX=12, KDEF=6;                 /* SPRING_CONSTANT_RANGE, integers */
const BMIN=0, BMAX=0.7, BDEF=0.3;              /* DAMPING_RANGE, N s/m (the parent sim's slider) */
const GMIN=0, GMAX=30, GDEF=9.8;               /* GRAVITY_RANGE */
const G_EARTH=9.8, G_MOON=1.6, G_JUPITER=24.8, G_PLANETX=14.2;
const LEFT_SPRING_X=1.0, RIGHT_SPRING_X=1.3, SPRING_X=1.2;
const SLOW=1/8;                                /* SLOW_SIM_DT_RATIO = 8 */
/* the real surface gravities, for comparison only — NOT what the sim uses */
const G_EARTH_REAL=9.81, G_MOON_REAL=1.62, G_JUPITER_REAL=24.79;
/* per-screen damping: StretchScreen sets .7, BounceScreen and LabScreen 0 */
const B_STRETCH=0.7, B_BOUNCE=0, B_LAB=0;
/* MassValueControlPanel: Range(50, 300) grams, adjustable mass default 100 g */
const MASS_G_MIN=50, MASS_G_MAX=300, MASS_G_DEF=100;
/* MassNode geometry: density option 80, module constants S = 2.5 and y = 4 */
const MASS_DENS=80, MASS_S=2.5, MASS_Y=4;

const BODIES=[{id:'moon',name:'Moon',g:G_MOON,real:G_MOON_REAL},
              {id:'earth',name:'Earth',g:G_EARTH,real:G_EARTH_REAL},
              {id:'planetX',name:'Planet X',g:G_PLANETX,real:null},
              {id:'jupiter',name:'Jupiter',g:G_JUPITER,real:G_JUPITER_REAL},
              {id:'custom',name:'custom',g:null,real:null}];
/* addDefaultMasses(basicsVersion): .25, .25, .1, .1, .05, .05 labelled and
   mystery .2 (large), .1 (medium), .075 (small).  Distinct values as chips. */
const RACK=[{id:'none',name:'none',m:0},
            {id:'m50',name:'50 g',m:0.05},
            {id:'m100',name:'100 g',m:0.10},
            {id:'m250',name:'250 g',m:0.25},
            {id:'q75',name:'? small',m:0.075,myst:true},
            {id:'q100',name:'? medium',m:0.10,myst:true},
            {id:'q200',name:'? large',m:0.20,myst:true}];
/* the lab: an adjustable mass plus mystery masses of .18 and .12 kg */
const LAB_RACK=[{id:'adj',name:'adjustable',m:null},
                {id:'q180',name:'? large',m:0.18,myst:true},
                {id:'q120',name:'? medium',m:0.12,myst:true}];

function bodyById(id){ for(const b of BODIES) if(b.id===id) return b; return BODIES[1]; }
function rackById(list,id){ for(const r of list) if(r.id===id) return r; return list[0]; }
/* PhET's mass-block size rule */
function massRadius(m){ return Math.sqrt(m/(MASS_DENS*MASS_S*Math.PI))*MASS_Y; }
function massHeight(m){ return MASS_S*massRadius(m); }

/* ---- Hooke's law ------------------------------------------------- */
function springForce(k,y){ return -k*y; }          /* the spring pulls back: F = -k y */
function yEq(m,k,g){ return m*g/k; }               /* the static extension, mg/k */
function gFromStretch(k,y,m){ return k*y/m; }      /* what Planet X asks you to invert */
function mFromStretch(k,y,g){ return k*y/g; }      /* and what a mystery mass asks */

/* ---- the damped oscillator: m u" + b u' + k u = 0 ------------------ */
function omega0(m,k){ return Math.sqrt(k/m); }
function period0(m,k){ return TAU*Math.sqrt(m/k); }
function gammaOf(m,b){ return b/(2*m); }
function bCrit(m,k){ return 2*Math.sqrt(k*m); }
function zetaOf(m,k,b){ return b/bCrit(m,k); }
function discr(m,k,b){ const g=gammaOf(m,b); return k/m-g*g; }   /* s = w0^2 - gam^2 */
function omegaD(m,k,b){ const s=discr(m,k,b); return s>0?Math.sqrt(s):0; }
function periodD(m,k,b){ const w=omegaD(m,k,b); return w>0?TAU/w:Infinity; }
function logDec(m,k,b){ const z=zetaOf(m,k,b); return z<1?TAU*z/Math.sqrt(1-z*z):Infinity; }
function qFactor(m,k,b){ const z=zetaOf(m,k,b); return z>0?1/(2*z):Infinity; }

/* C(t) = cos(sqrt(s) t) and Sn(t) = sin(sqrt(s) t)/sqrt(s), both entire in s:
   cosh/sinh below s = 0, and their three-term series at the critical point,
   where the direct forms are 0/0.
   The join is |s| t^2 < 1e-5, chosen so that BOTH terms of each series are
   load-bearing at the top of the branch and the truncation is still far below
   a rounding error.  Measured (build/masses-and-springs-basics/_out/diag.py):
   at x = |s|t^2 = 1e-5 the three-term series agrees with cos and sin/w exactly
   (its next term is x^3/720 = 1.4e-18), while the x^2 terms are worth
   4.167e-12 of C and 8.333e-13 of Sn.  At the earlier join of 1e-8 those terms
   were 4.167e-18 and 8.333e-19 — BELOW half an ulp (1.11e-16) — so the result
   was bit-identical with or without them and no assertion could reach them. */
function CSn(s,t){
  const st2=Math.abs(s)*t*t;
  if(st2<1e-5){ const t2=t*t, s2=s*s;
    return [1-s*t2/2+s2*t2*t2/24, t*(1-s*t2/6+s2*t2*t2/120)]; }
  if(s>0){ const w=Math.sqrt(s); return [Math.cos(w*t),Math.sin(w*t)/w]; }
  const r=Math.sqrt(-s); return [Math.cosh(r*t),Math.sinh(r*t)/r];
}
/* the exact propagator of the linear equation: (u, v) at time t from (u0, v0).
   This IS the sim's integrator — its error is the rounding of exp/cos, at any
   step size, in all three regimes, which is how PhET advances its springs. */
function prop(m,k,b,u0,v0,t){
  const w02=k/m, gam=gammaOf(m,b), cs=CSn(w02-gam*gam,t), C=cs[0], Sn=cs[1], e=Math.exp(-gam*t);
  return [e*(u0*(C+gam*Sn)+v0*Sn), e*(-w02*u0*Sn+v0*(C-gam*Sn))];
}
/* classical RK4 of the same equation, for the order measurement in selfTest */
function rk4(m,k,b,u0,v0,T,n){
  const hh=T/n; let u=u0, v=v0;
  const fa=(u,v)=>v, fb=(u,v)=>(-k*u-b*v)/m;
  for(let i=0;i<n;i++){
    const a1=fa(u,v), b1=fb(u,v);
    const a2=fa(u+hh*a1/2,v+hh*b1/2), b2=fb(u+hh*a1/2,v+hh*b1/2);
    const a3=fa(u+hh*a2/2,v+hh*b2/2), b3=fb(u+hh*a2/2,v+hh*b2/2);
    const a4=fa(u+hh*a3,v+hh*b3), b4=fb(u+hh*a3,v+hh*b3);
    u+=hh*(a1+2*a2+2*a3+a4)/6; v+=hh*(b1+2*b2+2*b3+b4)/6;
  }
  return [u,v];
}
/* ---- energy ------------------------------------------------------- */
function energyU(m,k,u,v){ return 0.5*m*v*v+0.5*k*u*u; }          /* about the equilibrium */
function keOf(m,v){ return 0.5*m*v*v; }
function peElastic(k,y){ return 0.5*k*y*y; }
/* the gravitational zero is the BOTTOM of the swing, y_bot = 2mg/k, so all
   three shares are non-negative and their sum is a POSITIVE constant — a sum
   drawn on the zero line is a sum nobody can see */
function swingBottom(m,k,g){ return 2*yEq(m,k,g); }
function peGrav(m,g,y,ybot){ return m*g*(ybot-y); }
function gravOffset(m,k,g){ return 1.5*m*m*g*g/k; }               /* KE+PEel+PEgr = E_u + this */
function ledgerTotal(m,k,g){ return 2*m*m*g*g/k; }                /* ... and at the release */

/* the one bisection used for every crossing time — the live period trace and
   the measured period in selfTest go through this same function */
function zeroBetween(m,k,b,u0,v0,tlo,thi){
  let a=tlo, c=thi, fa=prop(m,k,b,u0,v0,a)[0], fc=prop(m,k,b,u0,v0,c)[0];
  if(fa===0) return a;
  if(fa*fc>0) return NaN;
  for(let i=0;i<200;i++){
    const mid=0.5*(a+c); if(mid<=a||mid>=c) break;
    const fm=prop(m,k,b,u0,v0,mid)[0];
    if(fm===0){ a=c=mid; break; }
    if(fa*fm<0){ c=mid; fc=fm; } else { a=mid; fa=fm; }
  }
  return 0.5*(a+c);
}
function extremumBetween(m,k,b,u0,v0,tlo,thi){
  let a=tlo, c=thi, fa=prop(m,k,b,u0,v0,a)[1];
  if(fa*prop(m,k,b,u0,v0,c)[1]>0) return NaN;
  for(let i=0;i<200;i++){
    const mid=0.5*(a+c); if(mid<=a||mid>=c) break;
    const fm=prop(m,k,b,u0,v0,mid)[1];
    if(fm===0){ a=c=mid; break; }
    if(fa*fm<0){ c=mid; } else { a=mid; fa=fm; }
  }
  return 0.5*(a+c);
}
/* the period measured from the drawn motion: two crossings apart, released
   from rest at u0 so the first zero is a quarter period in */
function measurePeriod(m,k,b,u0){
  const Td=periodD(m,k,b); if(!isFinite(Td)) return NaN;
  const z1=zeroBetween(m,k,b,u0,0,1e-12,Td*0.6);
  const z3=zeroBetween(m,k,b,u0,0,Td*1.1,Td*1.6);
  return z3-z1;
}

/* ---- the spring coil ---------------------------------------------- */
const COILS=10, COIL_R=0.045, LEG=0.06;
/* the drawn helix, top at the ceiling, running down to the bottom.  PhET's
   thickness rule: thickness proportional to k and to the natural length. */
function coilPoints(xc,ytop,len,n){
  const pts=[], body=Math.max(0.02,len-2*LEG);
  pts.push([xc,ytop]); pts.push([xc,ytop-LEG]);
  for(let i=0;i<=n;i++){
    const f=i/n, ph=TAU*COILS*f;
    pts.push([xc+COIL_R*Math.sin(ph),ytop-LEG-body*f]);
  }
  pts.push([xc,ytop-LEG-body]); pts.push([xc,ytop-len]);
  return pts;
}
function coilWidth(k){ return 1.6+2.6*(k-KMIN)/(KMAX-KMIN); }
