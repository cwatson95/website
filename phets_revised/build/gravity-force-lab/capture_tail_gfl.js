/* capture_tail_gfl.js — display-list capture for gravity-force-lab.html.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_gfl.js > _out/cap_run.js
 * (cd _out && osascript -l JavaScript cap_run.js > cap.log)   — never through head/tail
 * Frames of the fall are reached through runStep(), never by setting the clock. */
const CAPW=1400, CAPH=820;
const capOut={W:CAPW,H:CAPH,views:{}};
const SCENES=[
  ['lab_default',        {view:'lab'}],
  ['lab_scientific',     {view:'lab',fmode:'sci'}],
  ['lab_hidden_const',   {view:'lab',fmode:'hid',cs:true,m1:1000,m2:10}],
  ['lab_heavy_close',    {view:'lab',m1:1000,m2:1000,i1:-12,i2:12}],
  ['lab_light_far',      {view:'lab',m1:10,m2:10,i1:-50,i2:50}],
  ['lab_ruler_on_m1',    {view:'lab',rulerI:-30,rulerY:0}],
  ['lab_arrows_huge',    {view:'lab',arrowK:4}],
  ['inv_default',        {view:'inv'}],
  ['inv_heavy_close',    {view:'inv',m1:1000,m2:1000,i1:-12,i2:12}],
  ['prod_default',       {view:'prod'}],
  ['prod_blocked',       {view:'prod',i1:-10,i2:10}],
  ['fall_idle',          {view:'fall'}],
  ['fall_half',          {view:'fall',release:true,frames:300}],
  ['fall_contact',       {view:'fall',release:true,frames:600}],
  ['fall_heavy_light',   {view:'fall',m1:1000,m2:10,i1:-50,i2:50,release:true,frames:450}],
];
for(const [name,over] of SCENES){
  Object.assign(ST,DEFAULTS,over); simReset();
  if(over.release){ startRun(ST); for(let k=0;k<over.frames;k++) runStep(); }
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS); simReset();
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+capJson.length+' bytes');
