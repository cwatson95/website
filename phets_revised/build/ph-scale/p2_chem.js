
/* ================================================================== *
 *  the chemistry, PhET's constants, and PhET's two drawing rules      *
 *  Every number marked (PhET) was read out of the minified original,  *
 *  docs/phets/ph-scale_en.html 1.7.6.  Every number marked (SI) or    *
 *  derived is re-derived in build/ph-scale/derive.py.                 *
 * ================================================================== */

/* Kw at 25 C by convention: pKw = 14.000 exactly, which is what PhET's hard-coded 14
   encodes (PHModel writes 14 - pH and 14 + log10 everywhere).  Neutral is pH 7.000.
   Temperature dependence is NOT modelled — pKw really does move with temperature, and a
   warm beaker's neutral point is below 7; this file has one temperature and says so. */
const KW=1e-14, PKW=14, SQRTKW=1e-7, LN10=Math.LN10;
const NA=6.02214076e23;          /* (SI 2019, exact) */
const NA_PHET=6.023e23;          /* (PhET) doc/model.md and computeParticleCount */

const PHET={
  BEAKER_VOLUME:1.2,             /* PHScaleConstants.BEAKER_VOLUME, L */
  MIN_SOLUTION_VOLUME:0.015,     /* PHScaleConstants.MIN_SOLUTION_VOLUME, L */
  PH_MIN:-1, PH_MAX:15, PH_DEFAULT:7,        /* PHScaleConstants.PH_RANGE */
  PH_DECIMALS:2, VOL_DECIMALS:2,
  MY_VOL_MIN:0.01, MY_VOL_DEFAULT:0.5,       /* MySolution.totalVolumeProperty */
  DROPPER_FLOW:0.05,             /* Dropper maxFlowRate, L/s */
  FAUCET_FLOW:0.25,              /* Faucet maxFlowRate, L/s (water and drain) */
  AUTOFILL_VOLUME:0.5, AUTOFILL_FLOW:0.45,   /* PHModel autofill */
  WATER_CONC:55, WATER_PH:7,                 /* Water.concentration, Water.pH */
  LOG_EXP_MIN:-16, LOG_EXP_MAX:2,            /* LOGARITHMIC_EXPONENT_RANGE */
  LIN_EXP_MIN:-14, LIN_EXP_MAX:1,            /* LINEAR_EXPONENT_RANGE */
  LIN_MANTISSA_MAX:8,                        /* LINEAR_MANTISSA_RANGE */
  DOTS_AT_PH7:50, DOTS_REF_CONC:1e-7,        /* ParticlesNode: round(50 c / 1e-7) */
  DOTS_MIN:5, DOTS_MAX:3000, DOTS_PH_LO:6, DOTS_PH_HI:8,
  COLOR_STOP_RATIO:0.25                      /* Solute's default colorStopRatio */
};
const WATER_RGB=[224,255,255];   /* (PhET) PHScaleColors.WATER, and the default dilutedColor */
const H3O_RGB='rgb(204,0,0)';    /* (PhET) PHScaleColors.H3O_PARTICLES */
const OH_RGB='rgb(0,0,255)';     /* (PhET) PHScaleColors.OH_PARTICLES */

/* PhET's twelve liquids, verbatim from the Solute.BATTERY_ACID .. Solute.WATER block.
   `range` is a MEASURED pH range with a source; null means none could be sourced here and
   the canvas says so rather than inventing one. */
const SOLUTES=[
  {id:'batteryAcid', name:'battery acid',  pH:1,   stock:[255,255,0],   stop:[255,224,204], range:null},
  {id:'blood',       name:'blood',         pH:7.4, stock:[211,79,68],   stop:[255,207,204],
   range:[7.37,7.43], src:'Merck Manual Professional, “Acid-Base Regulation” (J. L. Lewis III)'},
  {id:'chickenSoup', name:'chicken soup',  pH:5.8, stock:[255,240,104], stop:[255,250,204],
   range:[5.80,5.80], src:'FDA, “Approximate pH of Foods and Food Products”, row “Chicken Broth, rts.”'},
  {id:'coffee',      name:'coffee',        pH:5,   stock:[164,99,7],    stop:[255,240,204], range:null},
  {id:'drainCleaner',name:'drain cleaner', pH:13,  stock:[255,255,0],   stop:[255,255,204], range:null},
  {id:'handSoap',    name:'hand soap',     pH:10,  stock:[224,141,242], stop:[232,204,255], range:null},
  {id:'milk',        name:'milk',          pH:6.5, stock:[250,250,250], stop:null,
   range:[6.40,6.80], src:'FDA, same table, row “Milk, cow”'},
  {id:'orangeJuice', name:'orange juice',  pH:3.5, stock:[255,180,0],   stop:[255,242,204],
   range:[3.30,4.19], src:'FDA, same table, row “Orange Juice, California”'},
  {id:'soda',        name:'soda pop',      pH:2.5, stock:[204,255,102], stop:[238,255,204], range:null},
  {id:'spit',        name:'spit',          pH:7.4, stock:[202,240,239], stop:null,          range:null},
  {id:'vomit',       name:'vomit',         pH:2,   stock:[255,171,120], stop:[255,224,204], range:null},
  {id:'water',       name:'water',         pH:7,   stock:WATER_RGB,     stop:null,          range:null}
];
function soluteById(id){
  for(let i=0;i<SOLUTES.length;i++) if(SOLUTES[i].id===id) return SOLUTES[i];
  return SOLUTES[7];
}

/* ---- the two concentrations ------------------------------------------------------ */
function concH3O(ph){ return Math.pow(10,-ph); }
/* Kw/[H3O+], NOT 10^-(14-pH): pH - 14 is inexact in a double whenever pH < 7 (5.8 - 14
   needs one bit more than a double carries), so PhET's spelling is out by up to 2.1e-15
   while this is out by 2.1e-16 and keeps [H3O+][OH-] = Kw to a rounding (derive.py). */
function concOH(ph){ return KW/Math.pow(10,-ph); }
function concOHPhet(ph){ return Math.pow(10,-(PKW-ph)); }
function phFromH3O(c){ return (c===null||c===0)?null:-Math.log10(c); }
function phFromOH(c){ const p=phFromH3O(c); return p===null?null:PKW-p; }
function molesOf(c,v){ return c*v; }
function moleculesOf(c,v,na){ return c*v*(na===undefined?NA:na); }

/* ---- the net strong acid: the quantity that actually dilutes ---------------------- *
 * C = [H3O+] - [OH-] is a difference of ANALYTICAL concentrations (the spectator ions
 * cancel out of the charge balance), so moles of C are conserved on mixing and C simply
 * volume-averages.  Water has C = 0 exactly.  Written as a sinh it is exact everywhere;
 * written as the difference it cancels near neutral (1.9e-11 relative at pH 6.999999,
 * 1.7e-13 at 6.9999 — measured in derive.py, which also asserts the naive form is STILL
 * that bad so this branch cannot be quietly deleted).                                 */
function netAcid(ph){ return -2*SQRTKW*Math.sinh(LN10*(ph-0.5*PKW)); }
function netAcidNaive(ph){ return concH3O(ph)-concOH(ph); }

/* [H3O+] from C: the root of h - Kw/h = C.  The textbook root (C + sqrt(C^2+4Kw))/2 is
   catastrophic cancellation for every base — 3.6e-5 relative at pH 13, 8.0e-4 at pH 14,
   11 % at pH 15, all inside PhET's own range — so C < 0 takes the rationalised branch. */
function h3oFromNet(c){
  const r=Math.sqrt(c*c+4*KW);
  return c>=0 ? 0.5*(c+r) : 2*KW/(r-c);
}
function h3oFromNetNaive(c){ return 0.5*(c+Math.sqrt(c*c+4*KW)); }
function phFromNet(c){ return -Math.log10(h3oFromNet(c)); }
/* the same number in closed form, asinh being stable for every sign and size of C.
   Implemented twice on purpose: selfTest asserts the two agree, which catches typing. */
function phFromNetAsinh(c){ return 0.5*PKW-Math.asinh(c/(2*SQRTKW))/LN10; }

/* ---- mixing ---------------------------------------------------------------------- */
/* moles of net acid per litre of the mixture */
function mixNet(ph1,v1,ph2,v2){
  const vt=v1+v2;
  return vt<=0?null:(netAcid(ph1)*v1+netAcid(ph2)*v2)/vt;
}
/* THE EXACT LAW: average the net acid, then re-solve the charge balance with Kw.  The
   two degenerate cases are exact rather than round-tripped, as PhET's are. */
function mixExact(ph1,v1,ph2,v2){
  const vt=v1+v2;
  if(!(vt>0)) return null;
  if(v2===0) return ph1;
  if(v1===0) return ph2;
  return phFromNet(mixNet(ph1,v1,ph2,v2));
}
/* PhET's own rule (doc/model.md and PHModel.computePH), reimplemented from its
   arithmetic: mix the MAJORITY ion linearly and take a log, water contributing 1e-7 of
   that ion, with the branch chosen by whether the solute is an acid.  It never
   re-solves, so water's autoionisation is counted on one side and dropped on the other. */
function mixPhet(ph1,v1,v2){
  const vt=v1+v2;
  if(!(vt>0)) return null;
  if(v2===0) return ph1;
  if(v1===0) return PHET.WATER_PH;
  if(ph1<7) return -Math.log10((Math.pow(10,-ph1)*v1+Math.pow(10,-PHET.WATER_PH)*v2)/vt);
  return PKW+Math.log10((Math.pow(10,ph1-PKW)*v1+Math.pow(10,PHET.WATER_PH-PKW)*v2)/vt);
}
/* volume-averaging the pH — the mistake the dilution view exists to rule out */
function mixAverage(ph1,v1,ph2,v2){
  const vt=v1+v2;
  return vt<=0?null:(ph1*v1+ph2*v2)/vt;
}

/* ---- PhET's solute colour law ----------------------------------------------------- *
 * Solute.computeColor, reimplemented from its arithmetic.  ratio = V_solute/V_total:
 * with a colour stop the ramp is water -> stop over [0, 0.25] and stop -> stock over
 * [0.25, 1]; without one it is water -> stock over the whole range.                    */
function lerpRGB(a,b,t){
  return [a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t, a[2]+(b[2]-a[2])*t];
}
function soluteRGB(sol,ratio){
  const r=clamp(ratio,0,1), s=PHET.COLOR_STOP_RATIO;
  if(!sol.stop) return lerpRGB(WATER_RGB,sol.stock,r);
  return r>s ? lerpRGB(sol.stop,sol.stock,(r-s)/(1-s)) : lerpRGB(WATER_RGB,sol.stop,r/s);
}
function rgbCss(c){
  return 'rgb('+Math.round(c[0])+','+Math.round(c[1])+','+Math.round(c[2])+')';
}

/* ---- PhET's particle-drawing rule -------------------------------------------------- *
 * ParticlesNode.update: inside pH 6..8 the two counts are the true concentrations at 50
 * dots per 1e-7 mol/L, floored at 5.  Outside that window the majority saturates and the
 * MINORITY ramps linearly to 3000 at the ends of PH_RANGE — a drawing rule, not a count:
 * at pH 13 the drawn ratio is 457:1 where the true one is 1e12:1, which the canvas says. */
function rawDots(c){ return PHET.DOTS_AT_PH7*c/PHET.DOTS_REF_CONC; }
function dotCounts(ph){
  const lo=PHET.DOTS_PH_LO, hi=PHET.DOTS_PH_HI;
  let h,o;
  if(ph>=lo&&ph<=hi){
    h=Math.max(PHET.DOTS_MIN,rawDots(concH3O(ph)));
    o=Math.max(PHET.DOTS_MIN,rawDots(concOH(ph)));
  } else if(ph>hi){
    const s=ph-hi, slope=(PHET.DOTS_MAX-rawDots(concOH(hi)))/(PHET.PH_MAX-hi);
    h=Math.max(PHET.DOTS_MIN,rawDots(concH3O(hi))-s);
    o=rawDots(concOH(hi))+s*slope;
  } else {
    const s=lo-ph, slope=(PHET.DOTS_MAX-rawDots(concOH(hi)))/(PHET.PH_MAX-hi);
    h=rawDots(concH3O(lo))+s*slope;
    o=Math.max(PHET.DOTS_MIN,rawDots(concOH(lo))-s);
  }
  return {h:Math.round(h), o:Math.round(o)};
}

/* ---- a small seeded generator, so the dot scatter repeats exactly ------------------ */
function makeRng(seed){
  let s=seed>>>0;
  return {seed(x){ s=x>>>0; },
          next(){ s=(s*1664525+1013904223)>>>0; return s/4294967296; }};
}
