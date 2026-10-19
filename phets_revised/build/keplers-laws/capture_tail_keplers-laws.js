/* capture_tail_keplers-laws.js — display-list capture for keplers-laws.html.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_keplers-laws.js > _out/cap_run.js
 * osascript -l JavaScript _out/cap_run.js > _out/cap.log     (never through head/tail:
 * a closed pipe kills osascript before it writes display.json) */
const CAPW = 1400, CAPH = 820;
const out = {W: CAPW, H: CAPH, views: {}};
const SCENES = [
  ['first_default',    {view: 'first'}],
  ['first_everything', {view: 'first', foci: true, string: true, axes: true, semiaxes: true, ecc: true,
                        grid: true, tape: true, stopwatch: true, gravity: true}],
  ['first_target_mars',{view: 'first', target: 'mars', foci: true}],
  ['first_circular',   {view: 'first', circular: true, axes: true, semiaxes: true}],
  ['first_escaping',   {view: 'first', vy: auYrToKms(0.995 * Math.sqrt(K_SUN))}],
  ['first_crashing',   {view: 'first', vy: 3}],
  ['second_start',     {view: 'second'}],
  ['second_running',   {view: 'second', frames: 120, areaVals: true, timeVals: true}],
  ['second_six',       {view: 'second', div: 6, frames: 220, apo: true, peri: true}],
  ['second_two_ecc',   {view: 'second', div: 2, px: 0.7, py: 0, vx: 0, vy: 46, frames: 60}],
  ['third_linear',     {view: 'third'}],
  ['third_correct',    {view: 'third', pa: 3, pt: 2, target: 'mars'}],
  ['third_loglog',     {view: 'third', loglog: true, zoom: 'far'}],
  ['third_jupiter',    {view: 'third', target: 'jupiter', zoom: 'far', pa: 3, pt: 2}],
  ['all_default',      {view: 'all', foci: true, string: true}],
  ['all_running',      {view: 'all', frames: 150, axes: true, semiaxes: true, apo: true, peri: true, showT: true}],
  ['anom_early',       {view: 'anom', mfrac: 0.18}],
  ['anom_quarter',     {view: 'anom', mfrac: 0.25}],
  ['anom_high_e',      {view: 'anom', px: 0.6, py: 0, vx: 0, vy: 50, mfrac: 0.1}],
  ['anom_circular',    {view: 'anom', circular: true, mfrac: 0.4}]
];
for(const [name, over] of SCENES){
  const o = Object.assign({}, over); const frames = o.frames; delete o.frames;
  Object.assign(ST, DEFAULTS, o); simReset();
  if(o.mfrac !== undefined){
    const el = klOrbit(ST.px, ST.py, ST.vx, ST.vy, ST.mass, ST.circular);
    if(el.allowed) SIM.t = o.mfrac * el.T;
  }
  if(frames){ setRunning(true); for(let k = 0; k < frames; k++) runStep(); }
  const rc = makeRecorder(CAPW, CAPH);
  drawView(rc, CAPW, CAPH, buildModel());
  out.views[name] = rc.ops;
  console.log(name + ': ' + rc.ops.length + ' ops');
}
Object.assign(ST, DEFAULTS); simReset();
ObjC.import('Foundation');
const json = JSON.stringify(out);
$.NSString.alloc.initWithUTF8String(json)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, ' + json.length + ' bytes');
