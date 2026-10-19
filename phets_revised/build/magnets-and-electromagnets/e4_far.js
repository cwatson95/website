
/* ================================================================== *
 *  the far field: every closed current distribution looks like a      *
 *  point dipole from far enough away.  Taken numerically here:        *
 *  r^3 B / (point-dipole prediction) at 2, 4 and 8 m, Richardson-      *
 *  extrapolated twice (the corrections go as 1/r^2 and 1/r^4), must    *
 *  tend to 1; and the approach is the octupole term C/r^2, whose       *
 *  coefficient has a closed form for both sources.                     *
 * ================================================================== */
/* Each source registers what the far field needs to know about it: its mu0 m/4pi per unit
   source, its field on the axis and on the bisector, and its octupole coefficient in closed
   form.  A page without an electromagnet carries no coil entry (family.py strips it and
   checks that no coil symbol is left in the file). */
const FAR_SRC={
  magnet:{
    dip:()=>MAG_DIP,
    field:(N,r,where)=>where==='axis'?solB(0,r,MAG_R,MAG_B)[1]:-solB(r,0,MAG_R,MAG_B)[1],
    oct:()=>2*(MAG_B*MAG_B-0.75*MAG_R*MAG_R),
  },
};
/* #emag */
FAR_SRC.coil={
  dip:N=>N*COIL_A*COIL_A/4,
  field:(N,r,where)=>{ const b=where==='axis'?coilRU(N,0,r):coilRU(N,r,0); return where==='axis'?b[1]:-b[1]; },
  oct:N=>{ const xs=coilLoopsX(N); let s2=0; for(const x of xs) s2+=x*x; return 6*s2/xs.length-1.5*COIL_A*COIL_A; },
};
/* #endemag */
/* #emag */
function coilDip(N){ return FAR_SRC.coil.dip(N); }
/* #endemag */
function farField(kind,N,r,where){ return FAR_SRC[kind].field(N,r,where); }
function dipPred(kind,N,r,where){ return (where==='axis'?2:1)*FAR_SRC[kind].dip(N)/(r*r*r); }
function farRatio(kind,N,r,where){ return farField(kind,N,r,where)/dipPred(kind,N,r,where); }
/* twice-Richardson limit of f(r) = 1 + c2/r^2 + c4/r^4 + ... sampled at r0, 2 r0, 4 r0 */
function richardson(f,r0){
  const f1=f(r0), f2=f(2*r0), f4=f(4*r0);
  const a=(4*f2-f1)/3, b=(4*f4-f2)/3;
  return {f1,f2,f4,lim:(16*b-a)/15};
}
function dipoleLimit(kind,N,where){ return richardson(r=>farRatio(kind,N,r,where),2000); }
/* the octupole coefficient: on the axis as registered, on the bisector -3/4 of it (the
   axis-to-equator ratio of any l = 3 field against the l = 1 dipole) */
function octCoef(kind,N,where){ const c=FAR_SRC[kind].oct(N); return where==='axis'?c:-0.75*c; }
/* the measured approach: (ratio - 1) r^2, Richardson-extrapolated to r -> infinity */
function octMeasured(kind,N,where){ return richardson(r=>(farRatio(kind,N,r,where)-1)*r*r,2000).lim; }
