
/* ===================================================================
 * capture_tail_magnets-and-electromagnets.js -- the display-list capture.
 *   cat _out/run.js ../../../projects/simulations/tools/recorder.js \
 *       capture_tail_magnets-and-electromagnets.js > _out/cap_run.js
 *   osascript -l JavaScript _out/cap_run.js > _out/cap.log   (writes display.json)
 * Never pipe it through head: a closed pipe kills osascript before it writes the file
 * and the audit then reads a stale one (Known-bad).
 * The clocks are reached by STEPPING, never by setting them: the compass is an
 * integrated state and would otherwise sit where it was released (Known-bad).
 * Nothing here may be called `run` -- JXA calls a top-level run() itself.
 * =================================================================== */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const capOut={W:CAPW,H:CAPH,views:{}};
const CAP_SCENES=[
  ['bar',                 {},                                                                 0],
  ['bar_strong',          {pct:100,barMeter:true,seeInside:true,barM:{x:760,y:430}},           0],
  ['bar_earth',           {earth:true,pct:40},                                                 0],
  ['bar_zero',            {pct:0,barMeter:true},                                               0],
  ['bar_flipped_corner',  {bar:{x:210,y:150,ang:Math.PI},barMeter:true,barM:{x:520,y:300},barC:{x:360,y:330}}, 3],
  ['em',                  {view:'em'},                                                         1],
  ['em_one_loop',         {view:'em',loops:1,dcV:-10,emMeter:true,emM:{x:520,y:300}},          1],
  ['em_ac',               {view:'em',supply:'ac',acPk:100,acFp:100},                           0.32],
  ['em_off',              {view:'em',dcV:0,emMeter:true},                                      1],
  ['lines_magnet',        {view:'lines'},                                                      0],
  ['lines_coil',          {view:'lines',src:'coil'},                                           0],
  ['lines_coil_one',      {view:'lines',src:'coil',loops:1,dcV:-10},                           0],
  ['axis_magnet',         {view:'axis'},                                                       0],
  ['axis_coil',           {view:'axis',src:'coil'},                                            0],
  ['far_magnet',          {view:'far'},                                                        0],
  ['far_coil',            {view:'far',src:'coil',loops:3},                                     0],
  ['needle',              {view:'needle'},                                                     1.4],
  ['needle_slow',         {view:'needle',ndB:0.05,ndRel:179},                                  6],
  ['needle_undamped',     {view:'needle',ndB:300,ndRel:150,ndDamp:0},                          0.4],
];
for(const [name,over,secs] of CAP_SCENES){
  resetState(over);
  for(const k in MEMO) delete MEMO[k];
  const n=Math.round(secs*60);
  for(let i=0;i<n;i++) stepLive(1/60);      /* reach the clock by stepping it */
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
ObjC.import('Foundation');
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson)
  .writeToFileAtomicallyEncodingError((typeof CAP_FILE!=='undefined')?CAP_FILE:'display.json',true,$.NSUTF8StringEncoding,$());
console.log('wrote '+((typeof CAP_FILE!=='undefined')?CAP_FILE:'display.json')+', '+capJson.length+' bytes');
