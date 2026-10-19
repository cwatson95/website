/* capture_tail_energy-forms-and-changes.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_energy-forms-and-changes.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820), _out/display_mid.json (1100 x 700)
 * and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(over){
  resetAllState();
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,clean);
  if(over._preset) benchPreset(BENCH,ST,over._preset);
  if(over._grab){ const g=over._grab; benchGrab(BENCH,g[0],BENCH.bodies[g[0]].x,BENCH.bodies[g[0]].y+0.01); benchMoveHeld(BENCH,g[1],g[2]); DRAG.what='body'; DRAG.k=g[0]; }
  if(over._bench) for(let k=0;k<over._bench;k++) benchStep(BENCH,burnerLevels(ST));
  if(over._therm){ const th=BENCH.therm[0]; th.tray=false; th.x=SPOTS[0]+0.004; th.y=0.02; thermoDrop(BENCH,0);
    const t2=BENCH.therm[1]; t2.tray=false; t2.x=0.0; t2.y=0.19; thermoDrop(BENCH,1);
    const t3=BENCH.therm[2]; t3.tray=false; t3.x=SPOTS[4]+0.02; t3.y=0.03; thermoDrop(BENCH,2); }
  if(over._sys){ sysReset(SYS,ST); for(let k=0;k<over._sys;k++) sysStep(SYS,ST); }
}
const CAP_SCENES=[
  ['bench_start',       {view:'bench'}],
  ['bench_heat',        {view:'bench',_preset:'heat',_bench:900,_therm:1}],
  ['bench_hot',         {view:'bench',_preset:'hot',_bench:45}],
  ['bench_stack',       {view:'bench',_preset:'stack',_bench:1200,_therm:1}],
  ['bench_boil',        {view:'bench',_preset:'boil',_bench:1500}],
  ['bench_drag',        {view:'bench',_grab:[2,-0.02,0.16],_bench:30}],
  ['sys_faucet',        {view:'sys',_sys:600}],
  ['sys_biker',         {view:'sys',src:'biker',pedal:1,_sys:420}],
  ['sys_biker_empty',   {view:'sys',src:'biker',pedal:1,user:'fan',_sys:1100}],
  ['sys_sun_panel',     {view:'sys',src:'sun',conv:'panel',user:'incandescent',clouds:0.55,_sys:500}],
  ['sys_sun_generator', {view:'sys',src:'sun',user:'fan',_sys:300}],
  ['sys_teapot_fan',    {view:'sys',src:'teapot',heat:1,user:'fan',_sys:1200}],
  ['sys_teapot_panel',  {view:'sys',src:'teapot',heat:0.6,conv:'panel',user:'fluorescent',_sys:600}],
  ['ledger_idle',       {view:'ledger'}],
  ['ledger_heat',       {view:'ledger',_preset:'heat',_bench:1800}],
  ['ledger_hot',        {view:'ledger',_preset:'hot',_bench:900}],
  ['ledger_stack',      {view:'ledger',_preset:'stack',_bench:2400}],
  ['flow_faucet',       {view:'flow',_sys:900}],
  ['flow_biker',        {view:'flow',src:'biker',pedal:0.8,_sys:500}],
  ['flow_sun',          {view:'flow',src:'sun',conv:'panel',user:'incandescent',clouds:0.3,_sys:400}],
  ['flow_teapot',       {view:'flow',src:'teapot',heat:1,user:'fan',_sys:900}],
  ['flow_miss',         {view:'flow',src:'sun',_sys:200}],
  ['flow_idle',         {view:'flow',flow:0,_sys:10}],
  ['eq_default',        {view:'eq'}],
  ['eq_insulated_real', {view:'eq',eqAir:false,eqMat:'real'}],
  ['eq_boil',           {view:'eq',eqT1:620,eqT2:296}],
  ['eq_brick_iron',     {view:'eq',eqPair:'brick-iron'}],
  ['eq_water_iron',     {view:'eq',eqPair:'water-iron',eqT1:500}],
];
const CAP_MID=[['bench_heat',CAP_SCENES[1][1]],['sys_teapot_fan',CAP_SCENES[11][1]],['ledger_hot',CAP_SCENES[15][1]],['flow_faucet',CAP_SCENES[17][1]],['eq_boil',CAP_SCENES[25][1]]];
const CAP_NARROW=[['bench_heat',CAP_SCENES[1][1]],['sys_biker',CAP_SCENES[7][1]],['sys_sun_panel',CAP_SCENES[9][1]],['ledger_heat',CAP_SCENES[14][1]],['flow_teapot',CAP_SCENES[20][1]],['eq_default',CAP_SCENES[23][1]]];
ObjC.import('Foundation');
function capWrite(file,W,H,list){
  const out={W,H,views:{}};
  for(const [name,over] of list){
    capState(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,viewModel());
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWrite('display.json',1400,820,CAP_SCENES);
capWrite('display_mid.json',1100,700,CAP_MID);
capWrite('display_narrow.json',820,520,CAP_NARROW);
capState({}); DRAG.what=null;
