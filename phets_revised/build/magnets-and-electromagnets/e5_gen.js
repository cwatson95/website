
/* ================================================================== *
 *  the generator: the turbine's bar magnet turns in the page; the     *
 *  pickup coil's loops are discs perpendicular to the page (axis +x). *
 *  The flux is the AREA integral of B_x over the disc, the 3-D field  *
 *  included (16-point Gauss-Legendre in radius x 32-point trapezoid   *
 *  in angle, 1e-16 against scipy dblquad); one turn is sampled at 128 *
 *  angles and kept as a Fourier series, so Phi(theta) and the exact   *
 *  derivative dPhi/dtheta are available at any angle, and             *
 *      EMF = -N dPhi/dt = -N omega dPhi/dtheta.                       *
 *  theta is the magnet's angle in the page and omega = dtheta/dt, so  *
 *  a wheel turning the other way simply reverses the EMF.             *
 * ================================================================== */
const TURB_X=285, TURB_Y=LAYOUT_H-375, PICK_X=520, PICK_Y=LAYOUT_H-375;   /* PhET's GeneratorScreenModel positions, y flipped */
const PICK_AMAX=70685, PICK_NMAX=4, PICK_AMIN_PCT=20;   /* PhET's pickup coil: maxLoopArea 70685 (radius 150), 1-4 loops, area 20-100 % */
const PICK_PITCH=44, PICK_WIRE=6;                       /* drawing only: the turns' spacing and wire radius */
const RPM_MAX=60;                             /* PhET: 60 rpm at full flow (2 pi/25 rad per frame at 25 frames/s) */
const E_FULL=12e4*1e-4*1e-6*25;               /* PhET's maxEMF, 12e4 G px^2/frame, in volts at 1 px = 1 mm: 0.30 mV */
const FLUX_NS=16, FLUX_NPSI=32, FLUX_M=128;
function pickArea(areaPct){ return areaPct/100*PICK_AMAX; }
function pickRadius(areaPct){ return Math.sqrt(pickArea(areaPct)/Math.PI); }
function pickLoopsX(N){ const out=[]; for(let k=0;k<N;k++) out.push((k-(N-1)/2)*PICK_PITCH); return out; }
/* PhET's drag of the pickup coil on the turbine (its own phetioDocumentation: "Drag on the
   turbine caused by the pickup coil"): a linear ramp in N x area, scaled by the magnet's
   strength.  It is phenomenological -- a real back-torque needs the circuit's resistance,
   which neither PhET nor this page models -- and it is carried only so the wheel slows as
   the coil is made to work harder, as PhET's does. */
const DRAG_MAX=0.2, NA_LO=PICK_AMIN_PCT/100*PICK_AMAX, NA_HI=PICK_NMAX*PICK_AMAX, DRAG_LO=NA_LO/NA_HI*DRAG_MAX;
function genDrag(N,areaPct,pct){ return pct/100*(DRAG_LO+(DRAG_MAX-DRAG_LO)*(N*pickArea(areaPct)-NA_LO)/(NA_HI-NA_LO)); }
function genRPM(g){ return g.flow/100*(1-genDrag(g.N,g.area,g.strength))*RPM_MAX; }
const GL16=gaussLegendre(FLUX_NS);
/* the flux of a unit-strength magnet (turbine centre, axis at angle th) through one loop of
   radius rc centred at the pickup coil, in G mm^2 per G of strength */
function flux1(th,rc,ns,npsi){
  ns=ns||FLUX_NS; npsi=npsi||FLUX_NPSI;
  const m={kind:'magnet',x:TURB_X,y:TURB_Y,ang:th,S:1};
  const G=ns===FLUX_NS?GL16:gaussLegendre(ns);
  let tot=0;
  for(let i=0;i<ns;i++){
    const s=0.5*rc*(G.x[i]+1);
    let acc=0;
    for(let j=0;j<npsi;j++){ const ps=2*Math.PI*j/npsi; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),s*Math.sin(ps))[0]; }
    tot+=0.5*rc*G.w[i]*s*acc*2*Math.PI/npsi;
  }
  return tot;
}
/* the ring average of B_x round the circle of radius s in the coil's plane, and the value
   PhET would use there: the field IN the page, taken to hold off it as well */
function ringBx(th,s,npsi){
  const m={kind:'magnet',x:TURB_X,y:TURB_Y,ang:th,S:1}, n=npsi||FLUX_NPSI;
  let acc=0;
  for(let j=0;j<n;j++){ const ps=2*Math.PI*j/n; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),s*Math.sin(ps))[0]; }
  return acc/n;
}
function pageBx(th,y){ return magnetField({kind:'magnet',x:TURB_X,y:TURB_Y,ang:th,S:1},PICK_X,PICK_Y+y,0)[0]; }
/* the true contribution of the strip at height y: B_x integrated ALONG the chord, off the
   page as well as in it.  PhET's rule is the same strip with B_x(y, 0) carried across all of
   it, so these two are the whole of the difference between the estimates. */
function chordBx(th,y,rc,ns){
  const c=Math.sqrt(Math.max(0,rc*rc-y*y));
  if(!(c>0)) return 0;
  const m={kind:'magnet',x:TURB_X,y:TURB_Y,ang:th,S:1}, G=(ns&&ns!==FLUX_NS)?gaussLegendre(ns):GL16;
  let s=0;
  for(let i=0;i<G.x.length;i++) s+=G.w[i]*magnetField(m,PICK_X,PICK_Y+y,c*G.x[i])[0];
  return c*s;
}
function chordPhet(th,y,rc){ return pageBx(th,y)*2*Math.sqrt(Math.max(0,rc*rc-y*y)); }
/* PhET's own estimate: B_x sampled on the vertical diameter IN THE PAGE every 5 mm (its
   sample spacing is the magnet's height/10), each sample weighted by its chord
   2 sqrt(r^2 - y^2) times the spacing -- the field off the page is taken to be the field in
   it.  Kept for the coil-face view's comparison; never used for the EMF. */
const PHET_SP=MAG_R*2/10;
function fluxPhet1(th,rc){
  const sp=PHET_SP, n=Math.floor(rc/sp);
  let tot=0;
  for(let k=-n;k<=n;k++){ const y=k*sp; tot+=pageBx(th,y)*2*Math.sqrt(Math.abs(rc*rc-y*y))*sp; }
  return tot;
}
const FLUX_CACHE={};
/* Fourier series of flux1 over one turn: Phi(th) = sum_k a_k cos k th + b_k sin k th */
function fluxSeries(rc){
  const key=rc.toFixed(9);
  if(FLUX_CACHE[key]) return FLUX_CACHE[key];
  const M=FLUX_M, F=[];
  for(let j=0;j<M;j++) F.push(flux1(2*Math.PI*j/M,rc));
  const a=[], b=[];
  for(let k=0;k<=M/2;k++){
    let sa=0, sb=0;
    for(let j=0;j<M;j++){ const ph=2*Math.PI*k*j/M; sa+=F[j]*Math.cos(ph); sb+=F[j]*Math.sin(ph); }
    const nrm=(k===0||k===M/2)?1/M:2/M;
    a.push(sa*nrm); b.push(sb*nrm);
  }
  return (FLUX_CACHE[key]={rc,a,b,F});
}
function seriesPhi(ser,th){ let s=0; for(let k=0;k<ser.a.length;k++) s+=ser.a[k]*Math.cos(k*th)+ser.b[k]*Math.sin(k*th); return s; }
function seriesDPhi(ser,th){ let s=0; for(let k=1;k<ser.a.length;k++) s+=k*(-ser.a[k]*Math.sin(k*th)+ser.b[k]*Math.cos(k*th)); return s; }
/* SI: 1 G mm^2 = 1e-10 Wb, so N turns of a magnet of strength S give these webers and volts */
const WB_PER_G_MM2=1e-10;
function fluxOf(ser,th,N,S){ return N*S*seriesPhi(ser,th)*WB_PER_G_MM2; }
function emfOf(ser,th,N,S,omega){ return -N*S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }
/* PhET's normalised current: the EMF against its full scale, clamped to +-1.  Nothing on
   this page's sliders reaches the clamp (the largest is about 0.7 of full scale, asserted in
   selfTest); PhET's own flux is half again as large, which is what its clamp is for. */
function normOf(emf){ return Math.max(-1,Math.min(1,emf/E_FULL)); }
/* the generator's state -> its electrical readings */
function genReadings(g){
  const rc=pickRadius(g.area), ser=fluxSeries(rc), S=S_MAX*g.strength/100;
  const rpm=genRPM(g), omega=2*Math.PI*rpm/60;
  const Phi=fluxOf(ser,g.th,g.N,S), emf=emfOf(ser,g.th,g.N,S,omega);
  const norm=normOf(emf);
  return {rc,ser,S,rpm,omega,drag:genDrag(g.N,g.area,g.strength),phi1:seriesPhi(ser,g.th),dphi1:seriesDPhi(ser,g.th),
          Phi,emf,norm,bulb:Math.abs(norm),needle:norm*90};
}
/* The peak of |EMF| over a turn, and where it stands: NOT at 90 degrees, because Phi(th) is
   not a cosine -- the magnet is close enough for its higher harmonics to matter.  Only odd
   harmonics survive, so |dPhi/dtheta| is symmetric about 90 degrees and there are always TWO
   peaks: the search is over the first quarter turn, which is the one the view marks. */
function emfPeak(ser){
  const f=th=>Math.abs(seriesDPhi(ser,th));
  let th0=0, best=-1;
  for(let i=0;i<=180;i++){ const th=0.5*Math.PI*i/180, v=f(th); if(v>best){ best=v; th0=th; } }
  let lo=Math.max(0,th0-Math.PI/360), hi=Math.min(Math.PI/2,th0+Math.PI/360);
  for(let i=0;i<80;i++){ const m1=lo+(hi-lo)/3, m2=hi-(hi-lo)/3; if(f(m1)<f(m2)) lo=m1; else hi=m2; }
  const th=0.5*(lo+hi);
  return {th, val:f(th), at90:f(Math.PI/2)};
}
