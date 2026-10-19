/* capture_tail_build-an-atom.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_build-an-atom.js > _out/cap_run.js
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
  gameReset(ST);
  /* the best scores are NOT part of gameReset, and selfTest runs before this
     tail does (the entry block calls it when there is no document), so every
     level card read "best 10/10" in the first capture — a drawing test that
     reads ambient module state shows whatever ran last (Known-bad). */
  GAME.best = [0, 0, 0, 0];
  FRAME.jig = over._jig || 0;
  /* the game's phases are reached by PLAYING, never by writing GAME.phase:
     a capture that sets the state directly draws a configuration the sim
     cannot actually be in (Known-bad, the tautochrone beads) */
  if(over._play !== undefined){
    gameStart(ST);
    for(let k = 0; k < over._play; k++){
      const c = gameCurrent();
      if(!c) break;
      GAME.given = correctAnswer(c.type, c.atom);
      gameCheck();
      if(k < over._play - 1 || over._stay === undefined) gameNext();
    }
    if(over._wrong){
      const c = gameCurrent();
      if(c){
        const a = correctAnswer(c.type, c.atom), f = Object.keys(a)[0];
        GAME.given = Object.assign({}, a);
        GAME.given[f] = a[f] + (a[f] < FIELD_RANGE[f][1] ? 1 : -1);
        gameCheck();
        /* a second wrong answer needs the retry in between: gameCheck does
           nothing while the phase is 'wrong', so calling it twice left the
           capture in the one-more-try state under a name that said the
           answer had been shown */
        if(over._wrong === 2){ gameRetry(); gameCheck(); }
      }
    }
  }
}
const CAP_SCENES = [
  ['atom_carbon12',    {view: 'atom'}],
  ['atom_empty',       {view: 'atom', p: 0, n: 0, e: 0}],
  ['atom_full',        {view: 'atom', p: 10, n: 13, e: 10}],
  ['atom_cloud',       {view: 'atom', model: 'cloud', p: 8, n: 8, e: 10}],
  ['atom_cloud_empty', {view: 'atom', model: 'cloud', p: 3, n: 4, e: 0}],
  ['atom_unstable',    {view: 'atom', p: 6, n: 8, e: 6, jiggle: true, _jig: 2}],
  ['atom_bare',        {view: 'atom', showName: false, showIon: false, showStab: false,
                        showTable: false}],
  ['atom_hydrogen',    {view: 'atom', p: 1, n: 0, e: 0}],
  ['symbol_carbon12',  {view: 'symbol'}],
  ['symbol_ion',       {view: 'symbol', p: 8, n: 10, e: 10}],
  ['symbol_first',     {view: 'symbol', p: 3, n: 4, e: 2, notation: 'first'}],
  ['symbol_empty',     {view: 'symbol', p: 0, n: 0, e: 0}],
  ['game_levels',      {view: 'game'}],
  ['game_l1',          {view: 'game', level: 1, gseed: 5, _play: 0}],
  ['game_l2',          {view: 'game', level: 2, gseed: 12345, _play: 0}],
  ['game_l3',          {view: 'game', level: 3, gseed: 12345, _play: 2}],
  ['game_l4',          {view: 'game', level: 4, gseed: 12345, _play: 1}],
  ['game_wrong',       {view: 'game', level: 2, gseed: 4242, _play: 0, _wrong: 1}],
  ['game_shown',       {view: 'game', level: 2, gseed: 4242, _play: 0, _wrong: 2}],
  ['game_done',        {view: 'game', level: 1, gseed: 5, _play: 5}],
  ['count_stability',  {view: 'counting'}],
  ['count_element',    {view: 'counting', countMode: 'element', p: 3, n: 4, e: 1}],
  ['count_mass',       {view: 'counting', countMode: 'mass', p: 10, n: 13, e: 10}],
  ['chart_full',       {view: 'chart'}],
  ['chart_light',      {view: 'chart', chartZmax: 12}],
  ['chart_plain',      {view: 'chart', chartCompare: false, chartMagic: false}],
  ['mass_carbon',      {view: 'mass'}],
  ['mass_neon',        {view: 'mass', p: 10, n: 12, e: 10}],
  ['mass_chlorine',    {view: 'mass', p: 17, n: 18, e: 17}],
  ['mass_beryllium',   {view: 'mass', p: 4, n: 5, e: 4}],
  ['mass_low',         {view: 'mass', bindAll: false}],
  ['mass_nodata',      {view: 'mass', p: 0, n: 0, e: 0}],
];
const CAP_SMALL = [['atom_carbon12', CAP_SCENES[0][1]], ['atom_cloud', CAP_SCENES[3][1]],
                   ['symbol_ion', CAP_SCENES[9][1]], ['game_levels', CAP_SCENES[12][1]],
                   ['game_l3', CAP_SCENES[15][1]], ['count_stability', CAP_SCENES[20][1]],
                   ['chart_full', CAP_SCENES[23][1]], ['mass_carbon', CAP_SCENES[26][1]]];
ObjC.import('Foundation');
function capWrite(file, W, H, list){
  const out = {W, H, views: {}};
  for(const [name, over] of list){
    capState(over);
    const rc = makeRecorder(W, H);
    drawView(rc, W, H, buildModel(ST));
    out.views[name] = rc.ops;
    console.log(file + ' ' + name + ': ' + rc.ops.length + ' ops');
  }
  const json = JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(
    file, true, $.NSUTF8StringEncoding, $());
  console.log('wrote ' + file + ', ' + json.length + ' bytes');
}
capWrite('display.json', 1400, 820, CAP_SCENES);
capWrite('display_narrow.json', 820, 520, CAP_SMALL);
capWrite('display_tiny.json', 560, 380, CAP_SMALL);
capState({});
