
/* ===================================================================
 * capture_tail_generator.js -- the display-list capture.
 * Run through build/magnets-and-electromagnets/capture.py, which
 * concatenates _out/run.js + tools/recorder.js + this file and
 * redirects osascript to a log (never a pipe: a closed pipe kills it
 * before the JSON is written and the audit then reads a stale file).
 * Clocks are reached by STEPPING, never by setting them -- so a scene
 * with the faucet open moves on from the angle it is given.
 * Nothing here may be called `run` -- JXA calls a top-level run() itself.
 * =================================================================== */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const capOut={W:CAPW,H:CAPH,views:{}};
const CAP_SCENES=[
  ['gen',                {},                                                            0],
  ['gen_running',        {flow:100,th:0.55},                                            0],
  ['gen_electrons',      {flow:100,th:0.3,genCompass:false},                          0.4],
  ['gen_volt',           {flow:70,indicator:'volt',th:0.42,genMeter:true},              0],
  ['gen_big_coil',       {flow:100,N:4,area:100,th:2.1},                                0],
  ['gen_small_coil',     {flow:30,N:1,area:20,th:1.2,seeInside:true},                   0],
  ['gen_zero',           {flow:100,pct:0},                                              0],
  ['gen_closed_meter',   {genMeter:true,genM:{x:640,y:520}},                            0],
  ['flux',               {view:'flux'},                                                 0],
  ['flux_running',       {view:'flux',flow:100,th:0.9},                                 0],
  ['flux_big',           {view:'flux',flow:60,N:4,area:100,th:2.4},                     0],
  ['flux_zero',          {view:'flux',pct:0},                                           0],
  ['face',               {view:'face'},                                                 0],
  ['face_small',         {view:'face',area:20,th:0.7},                                  0],
  ['face_big',           {view:'face',area:100},                                        0],
  ['face_no_dots',       {view:'face',phetCmp:false,th:1.1},                            0],
  ['face_zero',          {view:'face',pct:0},                                            0],
  ['lines',              {view:'lines'},                                                0],
  ['lines_no_bound',     {view:'lines',bound:false},                                    0],
  ['axis',               {view:'axis'},                                                 0],
  ['axis_no_H',          {view:'axis',axisH:false},                                     0],
  ['needle',             {view:'needle'},                                             1.4],
  ['needle_slow',        {view:'needle',ndB:0.05,ndRel:179},                            6],
];
for(const [name,over,secs] of CAP_SCENES){
  resetState(over);
  for(const k in MEMO) delete MEMO[k];
  const n=Math.round(secs*60);
  for(let i=0;i<n;i++) stepLive(1/60);
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
