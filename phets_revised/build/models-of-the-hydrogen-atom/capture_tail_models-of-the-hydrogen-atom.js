/* capture_tail_models-of-the-hydrogen-atom.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_models-of-the-hydrogen-atom.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520)
 * and _out/display_tiny.json (560 x 380).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions).   */
function capState(over){
  const clean = {};
  for(const k in over) if(k[0] !== '_') clean[k] = over[k];
  Object.assign(ST, DEFAULTS, clean);
  atomReset(ST);
  /* reach a state by STEPPING, never by writing the clock: a capture that sets
     t directly leaves every integrated state at its release (Known-bad) */
  for(let k = 0; k < (over._ticks === undefined ? 150 : over._ticks); k++) atomTick(ST);
  if(over._n !== undefined){ ATOM.n = over._n; ATOM.l = over._l || 0; ATOM.m = over._m || 0; }
}
const CAP_SCENES = [
  ['box_bohr',        {view: 'box'}],
  ['box_white',       {view: 'box', light: 'white', _ticks: 900}],
  ['box_offline',     {view: 'box', lam: 300, _ticks: 400}],
  ['box_billiard',    {view: 'box', model: 'billiard', light: 'white', _ticks: 300}],
  ['box_pudding',     {view: 'box', model: 'pudding', light: 'white', _ticks: 2400}],
  ['box_classical',   {view: 'box', model: 'classical', _ticks: 25}],
  ['box_classical_dead', {view: 'box', model: 'classical', _ticks: 120}],
  ['box_debroglie',   {view: 'box', model: 'debroglie', _ticks: 400}],
  ['box_db_bright',   {view: 'box', model: 'debroglie', dbRep: 'bright', _ticks: 400}],
  ['box_schrodinger', {view: 'box', model: 'schrodinger', light: 'white', _ticks: 1500}],
  ['box_experiment',  {view: 'box', model: 'experiment', light: 'white', _ticks: 1500}],
  ['box_nospectro',   {view: 'box', showSpectro: false, showExact: false, _ticks: 300}],
  ['levels_bohr',     {view: 'levels', _ticks: 300}],
  ['levels_schro',    {view: 'levels', model: 'schrodinger', light: 'white', _ticks: 900}],
  ['levels_exp',      {view: 'levels', model: 'experiment', light: 'white', _ticks: 600}],
  ['wave_radial_3',   {view: 'wave', nu: 3, _ticks: 20}],
  ['wave_radial_3p4', {view: 'wave', nu: 3.45, _ticks: 20}],
  ['wave_height_5',   {view: 'wave', dbRep: 'height', nu: 5, _ticks: 20}],
  ['wave_bright_2',   {view: 'wave', dbRep: 'bright', nu: 2, _ticks: 20}],
  ['wave_phet_radii', {view: 'wave', nu: 6, showExact: false, _ticks: 20}],
  ['orb_1s',          {view: 'orbitals', n: 1, l: 0, m: 0, _ticks: 0}],
  ['orb_2p0',         {view: 'orbitals', n: 2, l: 1, m: 0, _ticks: 0}],
  ['orb_3d0',         {view: 'orbitals', n: 3, l: 2, m: 0, _ticks: 0}],
  ['orb_3d2',         {view: 'orbitals', n: 3, l: 2, m: 2, _ticks: 0}],
  ['orb_4f1',         {view: 'orbitals', n: 4, l: 3, m: 1, _ticks: 0}],
  ['orb_6s',          {view: 'orbitals', n: 6, l: 0, m: 0, _ticks: 0}],
  ['orb_nonodes',     {view: 'orbitals', n: 5, l: 2, m: 1, showPhet: false, _ticks: 0}],
  ['series_all',      {view: 'series', _ticks: 0}],
  ['series_lyman',    {view: 'series', series: '1', lam: 122, _ticks: 0}],
  ['series_balmer',   {view: 'series', series: '2', lam: 656, _ticks: 0}],
  ['series_pfund',    {view: 'series', series: '5', lam: 700, _ticks: 0}],
  ['rates_6_bohr',    {view: 'rates', trials: 4000, _ticks: 0}],
  ['rates_2_bohr',    {view: 'rates', fromN: 2, trials: 4000, _ticks: 0}],
  ['rates_5_schro',   {view: 'rates', model: 'schrodinger', fromN: 5, trials: 4000, _ticks: 0}],
];
const CAP_NARROW = [['box_white', CAP_SCENES[1][1]], ['levels_schro', CAP_SCENES[13][1]],
                    ['wave_radial_3p4', CAP_SCENES[16][1]], ['orb_3d2', CAP_SCENES[23][1]],
                    ['series_all', CAP_SCENES[27][1]], ['rates_6_bohr', CAP_SCENES[31][1]]];
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
