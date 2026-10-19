
/* ================================================================== *
 *  display-list capture tail for molecules-and-light.html             *
 *  (never name a helper `run` here: JXA calls a top-level run() for   *
 *  you, with argv -- Known-bad, wind_tunnel 2026-08-12)               *
 * ================================================================== */
const CW = 1400, CH2 = 820;
const outCap = {W: CW, H: CH2, views: {}};

/* Fifteen configurations, including the awkward ones: the molecule that
   answers nothing, the one that comes apart, PhET's own animation beside the
   derived one, the mode that is infrared-inactive, the tiny ensemble, and a
   cold surface. */
const SCENES = [
  ['chamber_co2_ir', {view: 'chamber', mol: 'CO2', band: 'infrared'}, 2.2],
  ['chamber_co2_ir_phet', {view: 'chamber', mol: 'CO2', band: 'infrared', anim: 'phet'}, 2.2],
  ['chamber_n2_uv', {view: 'chamber', mol: 'N2', band: 'ultraviolet', showRadius: true}, 2.2],
  ['chamber_o3_uv', {view: 'chamber', mol: 'O3', band: 'ultraviolet'}, 6.0],
  ['chamber_h2o_micro', {view: 'chamber', mol: 'H2O', band: 'microwave'}, 2.6],
  ['chamber_no2_vis', {view: 'chamber', mol: 'NO2', band: 'visible'}, 2.6],
  ['spectrum_ir', {view: 'spectrum', mol: 'CO2', band: 'infrared'}, 0],
  ['spectrum_micro', {view: 'spectrum', mol: 'CO', band: 'microwave'}, 0],
  ['table_no2_vis', {view: 'table', mol: 'NO2', band: 'visible'}, 0],
  ['table_n2_uv', {view: 'table', mol: 'N2', band: 'ultraviolet'}, 0],
  ['modes_co2_bend', {view: 'modes', mol: 'CO2', modeIdx: 2}, 0],
  ['modes_co2_sym', {view: 'modes', mol: 'CO2', modeIdx: 1}, 0],
  ['modes_ch4', {view: 'modes', mol: 'CH4', modeIdx: 3}, 0],
  ['modes_h2o', {view: 'modes', mol: 'H2O', modeIdx: 0}, 0],
  ['modes_n2', {view: 'modes', mol: 'N2', modeIdx: 0}, 0],
  ['stats', {view: 'stats', nStat: 20000, statSeed: 77003}, 0],
  ['stats_small', {view: 'stats', nStat: 500, statSeed: 5}, 0],
  ['air', {view: 'air', tempK: 288}, 0],
  ['air_cold', {view: 'air', tempK: 230, showWindow: false}, 0],
];

const Scap = makeScene({getContext: () => null});
Scap.W = CW;
Scap.H = CH2;
for (const [name, over, tsec] of SCENES) {
  Object.assign(ST, DEFAULTS, over);
  for (const k in MEMO) delete MEMO[k];
  chamberRebuild();
  MODEPHASE = 1.05;                       /* a fixed, non-zero phase */
  /* reach t through the real step, never by writing the clock: a capture that
     sets the clock directly leaves the integrated state at its release
     (Known-bad, the tautochrone beads) */
  if (tsec > 0) { ST.running = true; for (let i = 0; i < Math.round(tsec * 60); i++) sceneStep(1 / 60); }
  const rc = makeRecorder(CW, CH2);
  drawView(rc, CW, CH2, buildModel());
  outCap.views[name] = rc.ops;
  console.log(name + ': ' + rc.ops.length + ' ops');
}

/* stdout truncates at these sizes, so write the file directly */
ObjC.import('Foundation');
const jsonCap = JSON.stringify(outCap);
$.NSString.alloc.initWithUTF8String(jsonCap)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, ' + jsonCap.length + ' bytes');
