/* capture_tail_cl.js — display-list capture for coulombs-law.html.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_cl.js > _out/cap_run.js
 * (cd _out && osascript -l JavaScript cap_run.js > cap.log)   — never through head/tail */
const CAPW=1400, CAPH=820;
const capOut={W:CAPW,H:CAPH,views:{}};
const SCENES=[
  ['macro_default',      {view:'macro'}],
  ['macro_repel_sci',    {view:'macro',mq1:5,mq2:5,mSci:true}],
  ['macro_close',        {view:'macro',mq1:10,mq2:-10,mi1:-7,mi2:7}],
  ['macro_zero_hidden',  {view:'macro',mq1:0,mForce:false}],
  ['macro_ruler_on_q1',  {view:'macro',mRulerI:-10,mRulerY:0}],
  ['atomic_default',     {view:'atomic'}],
  ['atomic_close_dec',   {view:'atomic',aq1:10,aq2:10,ai1:-1,ai2:1,aSci:false}],
  ['atomic_far',         {view:'atomic',aq1:1,aq2:-1,ai1:-50,ai2:50}],
  ['inv_macro',          {view:'inv'}],
  ['inv_atomic_repel',   {view:'inv',scale:'atomic',aq1:3,aq2:3}],
  ['inv_zero',           {view:'inv',mq1:0}],
  ['prod_macro',         {view:'prod'}],
  ['prod_atomic_repel',  {view:'prod',scale:'atomic',aq1:7,aq2:3}],
  ['prod_zero',          {view:'prod',mq1:0}],
  ['grav_default',       {view:'grav'}],
  ['grav_big',           {view:'grav',mq1:10,mq2:10,aq1:10,aq2:-10,ai1:-1,ai2:1}],
];
for(const [name,over] of SCENES){
  Object.assign(ST,DEFAULTS,over);
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS);
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+capJson.length+' bytes');
