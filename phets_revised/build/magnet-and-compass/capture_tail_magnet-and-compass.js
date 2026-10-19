
/* ===================================================================
 * capture_tail_magnet-and-compass.js -- the display-list capture.
 * Run through build/magnets-and-electromagnets/capture.py, which
 * concatenates _out/run.js + tools/recorder.js + this file and
 * redirects osascript to a log (never a pipe: a closed pipe kills it
 * before the JSON is written and the audit then reads a stale file).
 * Clocks are reached by STEPPING, never by setting them.  Nothing here
 * may be called `run` -- JXA calls a top-level run() itself.
 * =================================================================== */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const capOut={W:CAPW,H:CAPH,views:{}};
const CAP_SCENES=[
  ['bar',                {},                                                                  0],
  ['bar_strong',         {pct:100,barMeter:true,seeInside:true,barM:{x:760,y:430}},            0],
  ['bar_earth',          {earth:true,pct:40},                                                  0],
  ['bar_zero',           {pct:0,barMeter:true},                                                0],
  ['bar_flipped_corner', {bar:{x:210,y:150,ang:Math.PI},barMeter:true,barM:{x:520,y:300},barC:{x:360,y:330}}, 3],
  ['bar_weak',           {pct:5,barMeter:true,barM:{x:700,y:250}},                             2],
  ['lines',              {view:'lines'},                                                       0],
  ['lines_no_bound',     {view:'lines',bound:false},                                           0],
  ['lines_zero',         {view:'lines',pct:0},                                                 0],
  ['axis',               {view:'axis'},                                                        0],
  ['axis_no_H',          {view:'axis',axisH:false},                                            0],
  ['far',                {view:'far'},                                                         0],
  ['far_zero',           {view:'far',pct:0},                                                   0],
  ['needle',             {view:'needle'},                                                      1.4],
  ['needle_slow',        {view:'needle',ndB:0.05,ndRel:179},                                   6],
  ['needle_undamped',    {view:'needle',ndB:300,ndRel:150,ndDamp:0},                           0.4],
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
