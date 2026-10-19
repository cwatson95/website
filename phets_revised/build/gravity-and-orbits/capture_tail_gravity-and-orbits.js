/* capture_tail_gravity-and-orbits.js — display-list capture for gravity-and-orbits.html.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_gravity-and-orbits.js > _out/cap_run.js
 * osascript -l JavaScript _out/cap_run.js > _out/cap.log    (never through head/tail) */
const CAPW = 1400, CAPH = 820;
const out = {W: CAPW, H: CAPH, views: {}};
const CAPS = [
  ['model_start',       {view: 'model'}],
  ['model_running',     {view: 'model', frames: 400, grid: true, com: true}],
  ['model_everything',  {view: 'model', frames: 260, grid: true, com: true, tape: true, massOn: true, force: true}],
  ['model_moon',        {view: 'model', system: 'starPlanetMoon', frames: 400, massOn: true}],
  ['model_planet_moon', {view: 'model', system: 'planetMoon', frames: 400, grid: true, massOn: true}],
  ['model_station',     {view: 'model', system: 'planetSatellite', frames: 260, grid: true, massOn: true}],
  ['model_gravity_off', {view: 'model', frames: 200, gravity: false}],
  ['scale_start',       {view: 'scale'}],
  ['scale_running',     {view: 'scale', frames: 400, com: true}],
  ['scale_moon',        {view: 'scale', system: 'starPlanetMoon', frames: 300}],
  ['scale_planet_moon', {view: 'scale', system: 'planetMoon', frames: 400, tape: true}],
  ['scale_station',     {view: 'scale', system: 'planetSatellite', frames: 260, grid: true}],
  ['circ_one',          {view: 'circ'}],
  ['circ_slow',         {view: 'circ', vfrac: 0.45}],
  ['circ_fast',         {view: 'circ', vfrac: 1.3}],
  ['circ_escape',       {view: 'circ', vfrac: 1.55}],
  ['circ_station',      {view: 'circ', system: 'planetSatellite', vfrac: 0.8}],
  ['exact_start',       {view: 'exact'}],
  ['exact_running',     {view: 'exact', frames: 500}],
  ['exact_station',     {view: 'exact', screen: 'scale', system: 'planetSatellite', frames: 400}],
  ['exact_three',       {view: 'exact', system: 'starPlanetMoon'}],
  ['cons_start',        {view: 'cons'}],
  ['cons_scale',        {view: 'cons', screen: 'scale', frames: 400}],
  ['cons_model_moon',   {view: 'cons', screen: 'model', system: 'starPlanetMoon', frames: 400}],
  ['cons_gravity_off',  {view: 'cons', frames: 300, gravity: false}]
];
for(const [name, over] of CAPS){
  const o = Object.assign({}, over); const frames = o.frames; delete o.frames;
  Object.assign(ST, DEFAULTS, o);
  if(o.view === 'model' || o.view === 'scale') ST.screen = o.view;
  simReset();
  if(frames){ ST.running = true; for(let k = 0; k < frames; k++) runStep(); ST.running = false; }
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
