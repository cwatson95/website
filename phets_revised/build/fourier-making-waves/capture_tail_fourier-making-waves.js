/* capture_tail_fourier-making-waves.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_fourier-making-waves.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (860 x 560).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  if(over._amps) setAmps(over._amps); else applyPreset();
  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
    setGuess(over._solve?GAME.answer.slice():new Array(NMAX).fill(0)); }
}
const CAP_SCENES=[
  ['harm_sinusoid',   {view:'harm',preset:'sinusoid'}],
  ['harm_square',     {view:'harm',preset:'square',showInf:true}],
  ['harm_triangle',   {view:'harm',preset:'triangle',series:'cos',showInf:true,sel:3}],
  ['harm_sawtooth',   {view:'harm',preset:'sawtooth',showInf:true,caliper:true,calX:-0.5,sel:2}],
  ['harm_packet',     {view:'harm',preset:'wavePacket'}],
  ['harm_time',       {view:'harm',preset:'square',domain:'time',caliper:true,calX:-1.5,sel:4}],
  ['harm_xt',         {view:'harm',preset:'square',domain:'both',t:0.7}],
  ['harm_three',      {view:'harm',preset:'square',N:3,showInf:true}],
  ['harm_zero',       {view:'harm',preset:'custom',_amps:new Array(NMAX).fill(0)}],
  ['harm_nohash',     {view:'harm',preset:'square',showHarm:false,showInf:true}],
  ['conv_square6',    {view:'conv',convPre:'square',convM:6}],
  ['conv_square1',    {view:'conv',convPre:'square',convM:1}],
  ['conv_square128',  {view:'conv',convPre:'square',convM:128}],
  ['conv_triangle',   {view:'conv',convPre:'triangle',series:'cos',convM:9}],
  ['conv_sawtooth',   {view:'conv',convPre:'sawtooth',convM:24}],
  ['spec_square',     {view:'spec',preset:'square'}],
  ['spec_packet',     {view:'spec',preset:'wavePacket'}],
  ['spec_sinusoid',   {view:'spec',preset:'sinusoid'}],
  ['game_l1',         {view:'game',level:1,seed:3,_game:1}],
  ['game_l3_solved',  {view:'game',level:3,seed:7,_game:1,_solve:1,showAns:true}],
  ['game_l5',         {view:'game',level:5,seed:11,_game:1}],
  ['pack_default',    {view:'pack'}],
  ['pack_continuous', {view:'pack',wpSp:0}],
  ['pack_quarter',    {view:'pack',wpSp:1}],
  ['pack_narrow',     {view:'pack',wpSp:2,wpSk:WP_SK_MIN,wpK0:WP_K0_MIN}],
  ['pack_wide',       {view:'pack',wpSp:3,wpSk:WP_SK_MAX,wpK0:WP_K0_MAX}],
  ['pack_time',       {view:'pack',wpDom:'time'}],
  ['pair_default',    {view:'pair'}],
  ['pair_coarse',     {view:'pair',pairK1:PAIR_K1_MAX}],
  ['pair_fine',       {view:'pair',pairK1:PAIR_K1_MIN,pairSk:WP_SK_MAX}],
];
const CAP_NARROW=[['harm_square',CAP_SCENES[1][1]],['conv_square6',CAP_SCENES[10][1]],
                  ['spec_square',CAP_SCENES[15][1]],['game_l1',CAP_SCENES[18][1]],
                  ['pack_default',CAP_SCENES[21][1]],['pair_default',CAP_SCENES[27][1]]];
ObjC.import('Foundation');
function capWrite(file,W,H,list){
  const out={W,H,views:{}};
  for(const [name,over] of list){
    capState(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,buildModel());
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWrite('display.json',1400,820,CAP_SCENES);
capWrite('display_narrow.json',860,560,CAP_NARROW);
capState({});
