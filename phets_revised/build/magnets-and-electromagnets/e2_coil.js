
/* ================================================================== *
 *  the electromagnet: N thin circular loops (Biot-Savart, exact), the *
 *  DC and AC supplies, the current, the electrons' phase              *
 * ================================================================== */
const COIL_A=50, COIL_PITCH=16, WIRE_R=8, COIL_NMAX=4;   /* PhET: loop area 7854 = pi 50^2, wire width 16, spacing 0 */
const DC_VMAX=10, AC_VMAX=110, AC_F100=1.25;             /* PhET: battery +-10 V; AC 0-110 V; 2 pi/20 rad per frame at 25 frames/s = 1.25 Hz at 100 % */
function coilLoopsX(N){ const out=[]; for(let k=0;k<N;k++) out.push((k-(N-1)/2)*COIL_PITCH); return out; }
/* 1 mm^-1 of loop field per unit mu0 I is mu0 I x 1e3 T, i.e. mu0 I x 1e7 G */
function coilGaussPerUnit(I){ return MU0*I*1e3*G_PER_T; }
/* the calibration, computed rather than typed: the current that makes PhET's maximum
   field, 300 G, at the centre of the 4-loop coil (asserted against derive.py) */
const I_MAX=(function(){ let s=0; for(const xk of coilLoopsX(COIL_NMAX)) s+=loopAxis(xk,COIL_A); return S_MAX/(MU0*1e3*G_PER_T*s); })();

/* the coil's field at a 3-D point; loops in planes x = cl.x + x_k, axis +x through (cl.x, cl.y) */
function coilField(cl,px,py,pz){
  const dy=py-cl.y, dz=pz||0, rho=Math.hypot(dy,dz), k=coilGaussPerUnit(cl.I);
  let bx=0, br=0;
  for(const xk of coilLoopsX(cl.N)){ const b=loopB(rho,px-cl.x-xk,COIL_A); br+=b[0]; bx+=b[1]; }
  if(rho>0) return [k*bx, k*br*dy/rho, k*br*dz/rho];
  return [k*bx,0,0];
}
/* the coil's flux function (unit mu0 I): field lines are its level sets */
function coilPsi(N,rho,u){ let p=0; for(const xk of coilLoopsX(N)) p+=loopB(rho,u-xk,COIL_A)[2]; return p; }
function coilRU(N,rho,u){ let br=0,bu=0; for(const xk of coilLoopsX(N)){ const b=loopB(rho,u-xk,COIL_A); br+=b[0]; bu+=b[1]; } return [br,bu]; }
/* inside the wire's 8-mm radius the thin-filament field is not the field of the drawn wire */
function inWire(cl,px,py){
  const dy=Math.abs(py-cl.y);
  for(const xk of coilLoopsX(cl.N)) if(Math.hypot(px-cl.x-xk,dy-COIL_A)<WIRE_R) return true;
  return false;
}

/* ---------------- the supplies (PhET's DC and AC power supplies) ---------------- *
 * Each supply drives the coil in proportion to its own full scale, as PhET's normalised
 * current does: I = I_max V / 10 V for the battery, I_max V / 110 V for the AC supply
 * (as if each had an internal resistance of V_full / I_max).  The AC voltage is
 * V = V_peak sin(2 pi f t), V_peak = 110 V x (max %)/100, f = 1.25 Hz x (frequency %)/100. */
function supplyVoltage(sup,t){
  if(sup.kind==='dc') return sup.V;
  return AC_VMAX*sup.pk/100*Math.sin(2*Math.PI*acFreq(sup)*t);
}
function acFreq(sup){ return AC_F100*sup.fp/100; }
function supplyCurrent(sup,t){ return I_MAX*supplyVoltage(sup,t)/(sup.kind==='dc'?DC_VMAX:AC_VMAX); }
