/* capture_tail_rutherford-scattering.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_rutherford-scattering.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)   never through head/tail:
 *   a closed pipe kills osascript BEFORE it writes display.json and the next
 *   audit silently reports the stale file (Known-bad).
 * Writes _out/display.json (1400 x 820), _out/display_narrow.json (820 x 520)
 * and _out/display_tiny.json (560 x 380).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions:
 * JXA calls a top-level run() for you, with argv).                          */
function capState(over){
  const clean = {};
  for(const k in over) if(k[0] !== '_') clean[k] = over[k];
  Object.assign(ST, DEFAULTS, clean);
  engineReset(ST);
  /* reach a state by STEPPING, never by writing the clock: a capture that
     sets t directly leaves every integrated state at its release (Known-bad,
     the tautochrone beads) */
  const n = over._ticks === undefined ? 700 : over._ticks;
  for(let k = 0; k < n; k++) stepOne(ST, DT_TICK);
}
const CAP_SCENES = [
  ['nucleus_default',   {view: 'nucleus'}],
  ['nucleus_long',      {view: 'nucleus', _ticks: 2400}],
  ['nucleus_notrace',   {view: 'nucleus', traces: false, showClosed: false, _ticks: 900}],
  ['nucleus_weak',      {view: 'nucleus', protons: 20, energy: 100, _ticks: 1600}],
  ['nucleus_strong',    {view: 'nucleus', protons: 100, energy: 50, _ticks: 1600}],
  ['nucleus_fewneut',   {view: 'nucleus', neutrons: 20, _ticks: 900}],
  ['nucleus_gunoff',    {view: 'nucleus', gunOn: false, _ticks: 400}],
  ['foil_default',      {view: 'foil', _ticks: 1800}],
  ['foil_long',         {view: 'foil', _ticks: 5000}],
  ['foil_strong',       {view: 'foil', protons: 100, energy: 50, _ticks: 3000}],
  ['foil_notrace',      {view: 'foil', traces: false, _ticks: 1800}],
  ['pudding_true',      {view: 'pudding', _ticks: 1500}],
  ['pudding_exagg',     {view: 'pudding', exagg: 4001, _ticks: 1500}],
  ['pudding_lowE',      {view: 'pudding', EMeV: 0.5, exagg: 2001, _ticks: 1500}],
  ['hyper_default',     {view: 'hyperbola', _ticks: 0}],
  ['hyper_headon',      {view: 'hyperbola', bModel: 0, _ticks: 0}],
  ['hyper_90',          {view: 'hyperbola', bModel: 15.9375, _ticks: 0}],
  ['hyper_grazing',     {view: 'hyperbola', bModel: 120, nPaths: 19, _ticks: 0}],
  ['hyper_one',         {view: 'hyperbola', nPaths: 1, showAsym: false, showInt: false, _ticks: 0}],
  ['hyper_strong',      {view: 'hyperbola', protons: 100, energy: 50, bModel: 40, _ticks: 0}],
  ['sigma_default',     {view: 'sigma', _ticks: 0}],
  ['sigma_small',       {view: 'sigma', nSample: 2000, bMax: 20, _ticks: 0}],
  ['sigma_big',         {view: 'sigma', nSample: 60000, bMax: 160, _ticks: 0}],
  ['sigma_closedonly',  {view: 'sigma', showSample: false, showJac: false, _ticks: 0}],
  ['gold_default',      {view: 'gold', _ticks: 0}],
  ['gold_lowE',         {view: 'gold', EMeV: 0.5, foilNm: 4000, _ticks: 0}],
  ['gold_touching',     {view: 'gold', EMeV: 25.6, foilNm: 50, _ticks: 0}],
  ['gold_light',        {view: 'gold', protons: 20, EMeV: 7.7, _ticks: 0}],
];
const CAP_NARROW = [['nucleus_default', CAP_SCENES[0][1]], ['foil_long', CAP_SCENES[8][1]],
                    ['pudding_exagg', CAP_SCENES[12][1]], ['hyper_default', CAP_SCENES[14][1]],
                    ['sigma_default', CAP_SCENES[20][1]], ['gold_default', CAP_SCENES[24][1]]];
ObjC.import('Foundation');
function capWrite(file, W, H, list){
  const out = {W, H, views: {}};
  for(const [name, over] of list){
    capState(over);
    const rc = makeRecorder(W, H);
    drawView(rc, W, H, buildModel());
    out.views[name] = rc.ops;
    console.log(file + ' ' + name + ': ' + rc.ops.length + ' ops');
  }
  const json = JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(
    file, true, $.NSUTF8StringEncoding, $());
  console.log('wrote ' + file + ', ' + json.length + ' bytes');
}
capWrite('display.json', 1400, 820, CAP_SCENES);
capWrite('display_narrow.json', 820, 520, CAP_NARROW);
capWrite('display_tiny.json', 560, 380, CAP_NARROW);
capState({});
