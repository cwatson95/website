/* capture_tail_my-solar-system.js — display-list capture for my-solar-system.html.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_my-solar-system.js > _out/cap_run.js
 * osascript -l JavaScript _out/cap_run.js > _out/cap.log    (never through head/tail) */
const CAPW = 1400, CAPH = 820;
const out = {W: CAPW, H: CAPH, views: {}};
const SCENES = [
  ['intro_start',      {view: 'intro'}],
  ['intro_running',    {view: 'intro', frames: 260, com: true, grid: true}],
  ['intro_everything', {view: 'intro', frames: 140, com: true, speedLab: true, gravity: true, grid: true,
                        tape: true, values: true}],
  ['lab_sun_planet',   {view: 'lab', frames: 200}],
  ['lab_moon',         {view: 'lab', preset: 'sunPlanetMoon', frames: 300, zoom: 5}],
  ['lab_comet',        {view: 'lab', preset: 'sunPlanetComet', frames: 400}],
  ['lab_trojan',       {view: 'lab', preset: 'trojan', frames: 400, com: true}],
  ['lab_ellipses',     {view: 'lab', preset: 'ellipses', frames: 500}],
  ['lab_hyperbolic',   {view: 'lab', preset: 'hyperbolic', frames: 400, zoom: 3}],
  ['lab_slingshot',    {view: 'lab', preset: 'slingshot', frames: 350}],
  ['lab_double_sling', {view: 'lab', preset: 'doubleSlingshot', frames: 350, gravity: true}],
  ['lab_binary',       {view: 'lab', preset: 'binaryPlanet', frames: 300}],
  ['lab_ballet',       {view: 'lab', preset: 'fourStar', frames: 300, com: true}],
  ['lab_double_double',{view: 'lab', preset: 'doubleDouble', frames: 260}],
  ['exact_start',      {view: 'exact'}],
  ['exact_running',    {view: 'exact', frames: 420}],
  ['conserve_start',   {view: 'conserve', frames: 30}],
  ['conserve_running', {view: 'conserve', frames: 400}],
  ['conserve_ballet',  {view: 'conserve', preset: 'fourStar', frames: 300}],
  ['conserve_trojan',  {view: 'conserve', preset: 'trojan', frames: 350}]
];
for(const [name, over] of SCENES){
  const o = Object.assign({}, over); const frames = o.frames; delete o.frames;
  Object.assign(ST, DEFAULTS, o); simReset();
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
