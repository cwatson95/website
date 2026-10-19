
/* ================================================================== *
 *  gravity: CODATA's G, PhET's spheres and track, the free fall       *
 * ================================================================== */
const G_N=6.6743e-11;          /* m^3 kg^-1 s^-2, CODATA 2022 (scipy.constants 1.18, derive.py) */
const G_PHET=6.67408e-11;      /* PhET's value (PHET_CORE/PhysicalConstants, CODATA 2014) */
const RHO_S=150;               /* PhET's value: sphere density for the mass-scaled size, kg/m^3 */
const R_CONST=0.5;             /* PhET's value: the radius in "constant size", m */
const M_MIN=10, M_MAX=1000, M_STEP=10;   /* PhET's mass range and its 10-kg slider rounding */
/* PhET's track: centres within +-5 m on a 0.1-m grid, surfaces 0.1 m apart.
   C = -G: like "charges" (masses) attract. */
const TRACK={q:0.1, perM:10, iL:-50, iR:50, sep:0.1, C:-G_N};
function sphereRadius(m,cs){ return cs?R_CONST:scaledRadius(m,RHO_S); }
function pairSteps(m1,m2,cs){ return minSteps(TRACK,sphereRadius(m1,cs),sphereRadius(m2,cs)); }
/* the strongest pull two equal masses m can reach: centres pairSteps apart */
function fmaxEqual(m,cs){ return forceMag(TRACK.C,m,m,pairSteps(m,m,cs)/TRACK.perM); }

/* ---- let them go: the radial two-body free fall from rest ---------------
   Released at separation r0, the separation obeys r'' = -G(m1+m2)/r^2 and
   energy gives the closing speed r' = -sqrt(2GM (1/r - 1/r0)).  From rest,
      t(r) = sqrt(r0^3 / 2GM) [ sqrt(x(1-x)) + asin sqrt(1-x) ],  x = r/r0.
   The asin form, not the textbook acos sqrt(x): near release x -> 1 and acos
   of a number near 1 loses half its digits.  1 - x is formed as (r0-r)/r0,
   exact for r within a factor of two of r0 (Sterbenz), never as 1 - r/r0. */
function fallTime(r,r0,GM){
  const x=r/r0, u=(r0-r)/r0;
  return Math.sqrt(r0*r0*r0/(2*GM))*(Math.sqrt(x*u)+Math.asin(Math.sqrt(u)));
}
/* the inverse r(t) by bisection on [rc, r0]: t(r) falls monotonically to 0 at r0 */
function fallR(t,r0,rc,GM){
  let lo=rc, hi=r0;
  for(let k=0;k<80;k++){ const m=0.5*(lo+hi); if(fallTime(m,r0,GM)>t) lo=m; else hi=m; }
  return 0.5*(lo+hi);
}
/* a run lasts FALL_FRAMES frames whatever its real duration; the clock factor is printed */
const FALL_FRAMES=600;
function fallModel(m1,m2,x1,x2,cs){
  const M=m1+m2, GM=G_N*M, r0=x2-x1, rc=sphereRadius(m1,cs)+sphereRadius(m2,cs);
  const tau=Math.sqrt(r0*r0*r0/(2*GM)), tc=fallTime(rc,r0,GM);
  return {m1,m2,M,GM,r0,rc,tau,tc,tff:PI/2*tau,xcm:(m1*x1+m2*x2)/M,x10:x1,x20:x2,clock:tc/(FALL_FRAMES/60)};
}
/* the state at time t: both bodies from the separation and the fixed centre of mass */
function fallState(F,t){
  const tt=clamp(t,0,F.tc);
  const r=tt<=0?F.r0:(tt>=F.tc?F.rc:fallR(tt,F.r0,F.rc,F.GM));
  const rdot=-Math.sqrt(Math.max(0,2*F.GM*(1/r-1/F.r0)));
  const x1=F.xcm-F.m2/F.M*r, x2=F.xcm+F.m1/F.M*r;
  return {t:tt,r,x1,x2,rdot,v1:-F.m2/F.M*rdot,v2:F.m1/F.M*rdot,
          F1:forceOn(TRACK.C,F.m1,F.m2,x1,x2,1),F2:forceOn(TRACK.C,F.m1,F.m2,x1,x2,2)};
}
/* the clock: hours and minutes (rounded to the minute) past an hour, else
   minutes and seconds (rounded to the second, so 59.6 s carries into 1 min) */
function hms(t){
  if(!isFinite(t)) return '—';
  const T=Math.round(t);
  if(T>=3600){ const Tm=Math.round(t/60), hh=Math.floor(Tm/60), mm=Tm-60*hh; return hh+' h '+(mm<10?'0':'')+mm+' min'; }
  const mm=Math.floor(T/60), ss=T-60*mm;
  return mm>0?mm+' min '+(ss<10?'0':'')+ss+' s':ss+' s';
}
