
/* ================================================================== *
 *  the chemistry.  Every function here has a twin in                  *
 *  build/beers-law-lab/derive.py, and every constant it leans on is   *
 *  a line of p2_data.js, which was written from the minified          *
 *  original.  No DOM.                                                 *
 * ================================================================== */

/* ---- lookups ---------------------------------------------------------------------- */
function soluteById(id){
  for(const s of SOLUTES) if(s.id===id) return s;
  return SOLUTES[0];                       /* an unknown id falls back rather than throwing */
}
function blsById(id){
  for(const s of BLSOLS) if(s.id===id) return s;
  return BLSOLS[0];
}
function hasSpectrum(id){ return Object.prototype.hasOwnProperty.call(EPS,id); }

/* ---- Beer-Lambert ------------------------------------------------------------------ *
 * PhET's model.md: "A = abC" and "T = 10^-A".  a is the molar absorptivity in 1/(cm M),
 * b the path length in cm, C the concentration in mol/L.  Nothing is approximated.      */
function absorbance(eps,l,c){ return eps*l*c; }
function transmittance(A){ return Math.pow(10,-A); }
/* the inverse.  Math.log10(0) is -Infinity in JavaScript, which is the honest answer for a
   detector reading exactly zero: no finite absorbance produces it. */
function absorbanceOfT(T){ return -Math.log10(T); }

/* PhET's molar absorptivity is a LOOKUP, not an interpolation: the table is indexed by
   floor(lambda - 380), so 500.0 nm and 500.9 nm read the same cell.  Outside the table
   there is no data and this returns null rather than a number nobody measured. */
function epsAt(id,lam){
  const t=EPS[id];
  if(!t) return null;
  const i=Math.floor(lam-LAM0);
  if(i<0||i>=NLAM) return null;
  return t[i];
}
function lambdaMaxOf(id){
  const t=EPS[id]; if(!t) return null;
  let best=t[0], k=0;
  for(let i=0;i<t.length;i++) if(t[i]>best){ best=t[i]; k=i; }   /* strict >, as PhET's is */
  return LAM0+k;
}
function epsMaxOf(id){ const lm=lambdaMaxOf(id); return lm===null?null:epsAt(id,lm); }

/* ---- the beaker: PhET's ConcentrationModel at the level of moles and litres --------- */
/* Each mechanism returns the amount that ACTUALLY moved, which is what lets the ledger
   close when a clamp bites.  The order of the five is PhET's own step(). */
function makeBeaker(soluteId,n,V){
  return {solute:soluteId, n:n, V:V, n0:n, V0:V, parts:[],
          led:{shaker:0, dropper:0, drained:0, faucet:0, evaporated:0,
               drainedV:0, dropperV:0, flying:0}};
}
function csatOf(id){ return soluteById(id).cSat; }
function bkPrecip(B){
  const z=B.n-B.V*csatOf(B.solute);
  return z>0?z:0;
}
/* PhET carries an updatePrecipitateAmount flag that it clears across the dropper's volume
   add, because its precipitate is a derived Property and would otherwise recompute on the
   half-finished state (volume raised, solute not yet added).  There is no counterpart here:
   bkPrecip is computed on demand and nothing reads it between the two writes, so the flag
   could not change an answer and would be a no-op nobody calls.  selfTest asserts the end
   state instead -- the dropper's effect on the solid is the same either way. */
function bkConc(B){
  if(!(B.V>0)) return 0;
  const q=B.n/B.V, cs=csatOf(B.solute);
  return q>cs?cs:q;
}
function bkSaturated(B){ return B.V>0 && B.n/B.V>csatOf(B.solute); }
function bkAddSolvent(B,d){
  if(!(d>0)) return 0;
  const v0=B.V; B.V=Math.min(PHET.VOL_MAX,B.V+d); return B.V-v0;
}
function bkRemoveSolvent(B,d){
  if(!(d>0)) return 0;
  const v0=B.V; B.V=Math.max(PHET.VOL_MIN,B.V-d); return v0-B.V;
}
function bkAddSolute(B,d){
  if(!(d>0)) return 0;
  const n0=B.n; B.n=Math.min(PHET.SOLUTE_MOL_MAX,B.n+d); return B.n-n0;
}
function bkRemoveSolute(B,d){
  if(!(d>0)) return 0;
  const n0=B.n; B.n=Math.max(PHET.SOLUTE_MOL_MIN,B.n-d); return n0-B.n;
}
/* the shaker's particles.  PhET's part is the arithmetic: round(max(1, rate * 200 * dt))
   of them a frame, each carrying exactly 1/200 mol, and the moles arrive when the particle
   LANDS, not when it is released.  Their flight is this file's own -- ballistic in the
   beaker's own coordinates (x across the inner width, y up from the floor in units of the
   beaker's height) -- and the canvas says so. */
const MOLE_PER_PARTICLE=1/PHET.PARTICLES_PER_MOLE;
const SHAKER_G=2.6;                       /* beaker heights per second squared, drawing-only */
function shakerPerFrame(dt){
  return Math.round(Math.max(1,PHET.SHAKER_RATE*PHET.PARTICLES_PER_MOLE*dt));
}
function makeRngB(seed){
  let s=seed>>>0;
  return function(){ s=(s*1664525+1013904223)>>>0; return s/4294967296; };
}
function bkStep(B,dt,ctl,rng){
  /* 1  the solvent faucet */
  B.led.faucet+=bkAddSolvent(B,ctl.faucet*dt);
  /* 2  the drain: it removes SOLUTION, so the solute leaves at the DISSOLVED
        concentration and the precipitate stays on the bottom */
  const dOut=ctl.drain*dt;
  if(dOut>0){
    const c=bkConc(B);
    const got=bkRemoveSolvent(B,dOut);
    B.led.drainedV+=got;
    B.led.drained+=bkRemoveSolute(B,c*got);
  }
  /* 3  the dropper: stock solution.  PhET freezes the precipitate across the volume add,
        so a stock drop cannot momentarily re-dissolve what is already on the bottom */
  const dIn=ctl.dropper*dt;
  if(dIn>0){
    const got=bkAddSolvent(B,dIn);
    B.led.dropperV+=got;
    B.led.dropper+=bkAddSolute(B,soluteById(B.solute).stock*got);
  }
  /* 4  evaporation: solvent leaves, solute does not */
  B.led.evaporated+=bkRemoveSolvent(B,ctl.evap*dt);
  /* 5  the shaker's particles fall, and land */
  const surf=bkFill(B);
  const keep=[];
  for(const p of B.parts){
    p.vy-=SHAKER_G*dt;
    p.x+=p.vx*dt; p.y+=p.vy*dt; p.rot+=p.spin*dt;
    if(p.x<0.02){ p.x=0.02; p.vx=Math.abs(p.vx); }
    if(p.x>0.98){ p.x=0.98; p.vx=-Math.abs(p.vx); }
    if(p.y<=surf){ B.led.shaker+=bkAddSolute(B,MOLE_PER_PARTICLE); }
    else keep.push(p);
  }
  B.parts=keep;
  /* 6  and the shaker makes more */
  if(ctl.shaking){
    const k=shakerPerFrame(dt);
    for(let i=0;i<k;i++)
      B.parts.push({x:0.30+0.12*rng(), y:1.28+0.05*rng(),
                    vx:0.22+0.10*rng(), vy:-0.05*rng(),
                    rot:TAU*rng(), spin:(rng()-0.5)*7});
  }
  B.led.flying=MOLE_PER_PARTICLE*B.parts.length;
  return B;
}
function bkFill(B){ return clamp(B.V/PHET.BEAKER_VOLUME,0,1); }
/* the ledger's two closures, as residuals the readout prints */
function bkLedgerResidual(B){
  return {n:B.n-(B.n0+B.led.shaker+B.led.dropper-B.led.drained),
          V:B.V-(B.V0+B.led.faucet+B.led.dropperV-B.led.drainedV-B.led.evaporated)};
}

/* grams, and PhET's mass percent.  Only the DISSOLVED solute is weighed: PhET's
   soluteGramsProperty subtracts the precipitate first. */
function soluteGrams(n,V,cs,M){
  const p=Math.max(0,n-V*cs);
  return M*Math.max(0,n-p);
}
function percentConcentration(g,V){
  return V<=0?0:g/(g+V*PHET.WATER_DENSITY)*100;
}
/* PhET's stockSolutionPercentConcentration: M c 100 / (rho + M c) */
function stockPercent(sol){
  return sol.molarMass*sol.stock*100/(PHET.WATER_DENSITY+sol.molarMass*sol.stock);
}
/* the volume at which evaporating a fixed n first saturates, and how long PhET's
   evaporator takes to get there from V */
function saturationVolume(n,cs){ return cs>0?n/cs:Infinity; }
function timeToSaturate(n,V,cs,rate){
  const vs=saturationVolume(n,cs);
  return (rate>0&&V>vs)?(V-vs)/rate:null;
}
/* PhET's precipitate particle count: round(200 * moles), but never zero while any exists */
function particleCount(pm){
  let k=Math.round(PHET.PARTICLES_PER_MOLE*pm);
  if(k===0&&pm>0) k=1;
  return k;
}

/* ---- PhET's two colour laws -------------------------------------------------------- */
/* Color.interpolateRGBA FLOORS each channel -- it is not a rounding.  Halfway between
   (224,255,255) and (255,225,225) is (239,240,240), not (240,240,240). */
function lerpRGBfloor(a,b,t){
  return [Math.floor(a[0]+(b[0]-a[0])*t),
          Math.floor(a[1]+(b[1]-a[1])*t),
          Math.floor(a[2]+(b[2]-a[2])*t)];
}
function rgbCss(v){ return 'rgb('+v[0]+','+v[1]+','+v[2]+')'; }
/* the Concentration screen: SoluteColorScheme's three stops, with
   ConcentrationSolution.createColor's "c = 0 shows the solvent" in front of it */
/* Two of SoluteColorScheme's four branches cannot be reached with PhET's own data, and
   they are kept because they are PhET's rather than because they do anything: every one
   of the nine has cMin = 0 and a minColor equal to the water colour, so "c = 0 shows the
   solvent" and "c <= cMin shows minColor" agree and neither can fire for c > 0.  Both
   properties are asserted in selfTest, so the branches begin to matter the moment a
   solute with a non-zero low stop is added -- and the two mutants on them are left out
   of the sweep with this as the reason, rather than reported as survivors. */
function schemeColor(id,c){
  const d=soluteById(id);
  if(!(c>0)) return WATER_RGB.slice();
  if(c>=d.cSat) return d.maxRGB.slice();
  if(c<=d.cMin) return d.minRGB.slice();
  if(c<=d.cMid) return lerpRGBfloor(d.minRGB,d.midRGB,(c-d.cMin)/(d.cMid-d.cMin));
  return lerpRGBfloor(d.midRGB,d.maxRGB,(c-d.cMid)/(d.cSat-d.cMid));
}
/* the Beer's Law screen: a straight two-stop RGB line over the solution's own range, with
   water at exactly zero.  The step at c = 0+ is PhET's and is drawn rather than smoothed. */
function rampColor(id,c){
  const d=blsById(id);
  if(!(c>0)) return WATER_RGB.slice();
  const t=clamp(c/d.cMax,0,1);
  return lerpRGBfloor(d.loRGB,d.hiRGB,t);
}

/* ---- the colour the solution really transmits --------------------------------------- *
 * XYZ over the CIE 1931 2-degree observer on the same 1 nm grid the spectra live on, so
 * nothing is interpolated.  Two illuminants: E, the equal-energy white (flat by
 * definition), and CIE standard illuminant A, from the CIE's own defining formula.  No
 * D65 spectrum could be sourced offline, and none is invented.                            */
const C2_ILLUM_A=1.435e-2, T_ILLUM_A=2848;     /* the CIE's 1931 c2, in m K, and its 2848 K */
function illumAt(kind,lam){
  if(kind==='E') return 1;
  return 100*Math.pow(560/lam,5)*(Math.exp(C2_ILLUM_A*1e9/(T_ILLUM_A*560))-1)
            /(Math.exp(C2_ILLUM_A*1e9/(T_ILLUM_A*lam))-1);
}
const SRGB_M=[[ 3.2406,-1.5372,-0.4986],
              [-0.9689, 1.8758, 0.0415],
              [ 0.0557,-0.2040, 1.0570]];
/* the sRGB transfer curve (IEC 61966-2-1).  The clamp is HERE and nowhere else: a
   second clamp on the caller's side would make each mutant on the other equivalent
   (Known-bad, buoyancy.html -- two guards on one path). */
function srgbGamma(u){
  u=clamp(u,0,1);
  return u<=0.0031308?12.92*u:1.055*Math.pow(u,1/2.4)-0.055;
}
function xyzToLin(X,Y,Z){
  return [SRGB_M[0][0]*X+SRGB_M[0][1]*Y+SRGB_M[0][2]*Z,
          SRGB_M[1][0]*X+SRGB_M[1][1]*Y+SRGB_M[1][2]*Z,
          SRGB_M[2][0]*X+SRGB_M[2][1]*Y+SRGB_M[2][2]*Z];
}
/* returns {xyz, white, Y} -- the transmitted tristimulus, the illuminant's own, and the
   photopic transmittance Y/Yw, which is the fraction of the LIGHT (not of the beam at
   lambda_max) that gets through. */
function transmittedXYZ(id,l,c,kind){
  const t=EPS[id];
  if(!t) return null;
  let X=0,Y=0,Z=0,Xw=0,Yw=0,Zw=0;
  for(let i=0;i<NLAM;i++){
    const S=illumAt(kind||'E',LAM0+i);
    const T=Math.pow(10,-t[i]*l*c);
    const sx=S*CIE_X[i], sy=S*CIE_Y[i], sz=S*CIE_Z[i];
    X+=T*sx; Y+=T*sy; Z+=T*sz;
    Xw+=sx;  Yw+=sy;  Zw+=sz;
  }
  return {xyz:[X,Y,Z], white:[Xw,Yw,Zw], Y:Y/Yw};
}
/* Adapted so the illuminant itself renders EXACTLY white: each linear sRGB channel is
   divided by the same channel for the illuminant alone.  That is a von Kries adaptation
   carried out in the display's own primaries, it needs no white-point constant, and it
   makes an empty cuvette rgb(255,255,255) under either illuminant. */
function trueRGB(id,l,c,kind){
  const r=transmittedXYZ(id,l,c,kind);
  if(!r) return null;
  const lin=xyzToLin(r.xyz[0],r.xyz[1],r.xyz[2]);
  const w=xyzToLin(r.white[0],r.white[1],r.white[2]);
  /* out-of-gamut channels come out negative; srgbGamma clamps them, and clamping them
     again here would only make its mutant equivalent */
  const v=[lin[0]/w[0],lin[1]/w[1],lin[2]/w[2]];
  return {rgb:[Math.round(255*srgbGamma(v[0])),
               Math.round(255*srgbGamma(v[1])),
               Math.round(255*srgbGamma(v[2]))],
          Y:r.Y};
}
/* relative luminance of an sRGB triple, for comparing PhET's ramp against the true colour
   on the one axis they can both be put on */
function relLum(v){
  const inv=u=>{ u/=255; return u<=0.04045?u/12.92:Math.pow((u+0.055)/1.055,2.4); };
  return 0.2126*inv(v[0])+0.7152*inv(v[1])+0.0722*inv(v[2]);
}
/* a monochromatic wavelength's own colour, for the spectrum view's wavelength cursor and
   the beam.  Normalised to its brightest channel and faded by the eye's own response, as
   diffraction.html does -- display only, and the canvas says so. */
function waveRGB(lam){
  const i=Math.round(lam)-LAM0;
  if(i<0||i>=NLAM) return [0,0,0];
  let v=xyzToLin(CIE_X[i],CIE_Y[i],CIE_Z[i]);
  const lo=Math.min(v[0],v[1],v[2]);
  if(lo<0) v=v.map(u=>u-lo);
  const m=Math.max(v[0],v[1],v[2]);
  if(!(m>0)) return [0,0,0];
  const k=Math.sqrt(Math.min(1,4*CIE_Y[i]));
  return v.map(u=>Math.round(255*srgbGamma(u/m*k)));
}
function waveCss(lam){ return rgbCss(waveRGB(lam)); }

/* ---- where Beer-Lambert stops being true ------------------------------------------- *
 * Not modelled, but named: above roughly 10 mM a real solution's molar absorptivity drifts
 * (refractive index, ion pairing, solute-solute interaction), so the straight line the law
 * view draws is an extrapolation past that.  The number is a conventional teaching bound,
 * not a measurement, and it is labelled that way wherever it appears.                     */
const LINEAR_LIMIT=0.01;
