
/* ================================================================== *
 *  the inverse-square engine — PhET's INVERSE_SQUARE_LAW_COMMON,      *
 *  rebuilt from its behaviour: two bodies on a line, a force          *
 *  C v1 v2 / r^2, and the rule that keeps them apart.  Shared         *
 *  verbatim by gravity-force-lab.html and coulombs-law.html           *
 *  (source: build/gravity-force-lab/p2_engine.js).                    *
 * ================================================================== */

/* PhET's roundSymmetric: the nearest integer, halves away from zero.
   Math.round alone sends -2.5 to -2, which would make the grid lopsided. */
function symRound(y){ return y<0?-Math.round(-y):Math.round(y); }

/* A track T (built per screen): centres live on a grid of q metres; perM is
   the grid count per metre (10, 1000 or 1e12 — an exact integer, so
   i / perM is the double nearest the decimal position); counts iL..iR are
   the ends of the track; sep is the surface gap PhET asks for; C is the
   signed force constant — C > 0 pushes like values apart (Coulomb's k),
   C < 0 pulls them together (-G for masses). */
function posOf(T,i){ return i/T.perM; }

/* The fewest grid steps two centres may be apart.  PhET snaps r1 + r2 + sep
   to the grid, summed in that order: a sum a hair under a half step rounds
   DOWN (Coulomb's macro screen: 6.75 + 6.75 + 1 mm = 14.4999... mm -> 14). */
function minSteps(T,r1,r2){ return symRound((r1+r2+T.sep)/T.q); }

/* After a body grows into its neighbour.  k is the body whose size changed
   LAST: its neighbour is pushed aside, unless the neighbour is against the
   end of the track, in which case the grown body moves instead (PhET's
   ISLCModel.step; its two-frame resolution collapses to this one call).
   Returns the new pair of counts. */
function settlePair(i1,i2,n,iL,iR,k){
  if(i2-i1>=n) return [i1,i2];
  if(k===1){ if(i2<iR) i2=Math.min(i1+n,iR); if(i2-i1<n) i1=i2-n; }
  else     { if(i1>iL) i1=Math.max(i2-n,iL); if(i2-i1<n) i2=i1+n; }
  return [i1,i2];
}

/* A drag of body k to x (metres): snapped to the grid, held inside the track
   and clear of the other body.  The bounds are grid counts, so clamping and
   snapping commute (PhET clamps first; the result is the same). */
function dragSteps(T,k,x,i1,i2,n){
  const i=symRound(x*T.perM);
  return k===1?clamp(i,T.iL,i2-n):clamp(i,i1+n,T.iR);
}

/* The force ON body `on` along +x: C v1 v2 (x_on - x_other) / |x_on - x_other|^3.
   Each body's force is computed from its own geometry, so Newton's third law
   (F_on1 = -F_on2) is an output the tests check, not an assumption. */
function forceOn(C,v1,v2,x1,x2,on){
  const d=on===1?x1-x2:x2-x1;
  return C*v1*v2*d/(Math.abs(d)*d*d);
}
function forceMag(C,v1,v2,r){ return Math.abs(C*v1*v2)/(r*r); }

/* PhET's two readout formats.  Decimal: `places` decimals with the digits
   after the point grouped in threes.  Scientific: a two-decimal mantissa and
   a power of ten (none when the exponent is 0).  A zero force stays decimal
   in either mode, as PhET's does. */
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function supText(n){ return String(n).replace(/[-0-9]/g,c=>SUPS[c]); }
function decGrouped(x,places){
  const s=Number(x).toFixed(places), i=s.indexOf('.');
  if(i<0) return s;
  let out=s.slice(0,i+4);
  for(let j=i+4;j<s.length;j+=3) out+=' '+s.slice(j,j+3);
  return out;
}
function sciText(x,digits){
  const s=Number(x).toExponential(digits), k=s.indexOf('e'), ex=parseInt(s.slice(k+1),10);
  return ex===0?s.slice(0,k):s.slice(0,k)+' × 10'+supText(ex);
}
function forceValueText(F,mode,places){
  const a=Math.abs(F);
  return (mode==='sci'&&a!==0)?sciText(a,2):decGrouped(a,places);
}
/* the label PhET prints over each arrow */
function forceLabel(me,other,F,mode,places){
  return 'Force on '+me+' by '+other+(mode==='hid'?'':' = '+forceValueText(F,mode,places)+' N');
}
/* the same number for the HTML readout, significant figures and a real
   superscript (sigf's ×10^ form is for the canvas-free fallbacks) */
function sciHTML(x,n){
  if(!isFinite(x)) return '—';
  if(x===0) return '0';
  const a=Math.abs(x);
  if(a>=1e-3&&a<1e5) return sigf(x,n);
  const s=x.toExponential(n-1), k=s.indexOf('e');
  return s.slice(0,k)+' &times; 10<sup>'+parseInt(s.slice(k+1),10)+'</sup>';
}
/* ...and for canvas text (no markup: Unicode superscripts) */
function sciPlain(x,n){
  if(!isFinite(x)) return '—';
  if(x===0) return '0';
  const a=Math.abs(x);
  if(a>=1e-3&&a<1e5) return sigf(x,n);
  const s=x.toExponential(n-1), k=s.indexOf('e');
  return s.slice(0,k)+' × 10'+supText(parseInt(s.slice(k+1),10));
}

/* The force-arrow scale: a 1-2-5 ladder.  Step k is
   [1,2,5][k mod 3] x 10^(floor(k/3) + e0) newtons per display unit of arrow. */
function arrowStep(k,e0){ return [1,2,5][((k%3)+3)%3]*Math.pow(10,Math.floor(k/3)+e0); }

/* The inverse-square view's samples, all through forceMag (never a closed form
   of the answer), so a wrong exponent shows as an F r^2 that is not flat:
   a log-spaced sweep over [lo, hi], a linear one over the distances the track
   can hold [dmin, rTrack], the log-log slope measured at the live distance by
   a central difference, and the inverse-cube comparison through the live point. */
function invSample(C,v1,v2,r,rTouch,dmin,rTrack){
  const lo=0.5*rTouch, hi=2*rTrack, n=120, rs=[], Fs=[];
  for(let i=0;i<=n;i++){ const x=lo*Math.pow(hi/lo,i/n); rs.push(x); Fs.push(forceMag(C,v1,v2,x)); }
  const lin={rs:[],Fs:[],Fr2:[],F3r2:[]}, Fnow=forceMag(C,v1,v2,r);
  for(let i=0;i<=100;i++){ const x=dmin+(rTrack-dmin)*i/100, F=forceMag(C,v1,v2,x);
    lin.rs.push(x); lin.Fs.push(F); lin.Fr2.push(F*x*x); lin.F3r2.push(Fnow*r*r*r/x); }
  const e=1e-3, slope=(Math.log(forceMag(C,v1,v2,r*(1+e)))-Math.log(forceMag(C,v1,v2,r*(1-e))))/(Math.log(1+e)-Math.log(1-e));
  return {lo,hi,rs,Fs,lin,rTouch,dmin,rTrack,slope,Fnow,F2r:forceMag(C,v1,v2,2*r),
          Fnear:forceMag(C,v1,v2,dmin),Ffar:forceMag(C,v1,v2,rTrack),prod:Math.abs(C*v1*v2)};
}

/* the radius of a uniform sphere of mass m and density rho */
function scaledRadius(m,rho){ return Math.pow(3*m/rho/(4*PI),1/3); }
