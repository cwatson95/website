/* capture_tail_wave-on-a-string.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_wave-on-a-string.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  liveRestart(); LIVE.sw=0; LIVE.swOn=false; LIVE.arrows=true; reflReset(ST); standReset(ST);
  if(over._wr!==undefined){ LIVE.wr=over._wr; LIVE.wrPrev=over._wr; }
  if(over._pulse) sendPulse(ST);
  if(over._live) for(let k=0;k<over._live;k++) liveStepOnce(ST,1);
  if(over._acc) LIVE.acc=over._acc*dtOf(ST.tension);
  if(over._refl) for(let k=0;k<over._refl;k++) reflStep(ST);
  if(over._stand) for(let k=0;k<over._stand;k++) standStep(ST);
  if(over._sw!==undefined){ LIVE.sw=over._sw; LIVE.swOn=true; }
}
const CAP_SCENES=[
  ['str_manual',      {view:'str'}],
  ['str_kink',        {view:'str',_wr:1.2,_live:25}],
  ['str_osc',         {view:'str',mode:'osc',_live:90,_acc:0.4}],
  ['str_pulse',       {view:'str',mode:'pulse',_pulse:1,_live:40}],
  ['str_loose_tools', {view:'str',mode:'osc',end:'loose',_live:70,rulers:true,stopwatch:true,refline:true,_sw:1.23}],
  ['str_none',        {view:'str',mode:'osc',end:'none',_live:120}],
  ['str_offscale',    {view:'str',mode:'osc',freq:1.25,damping:0,_live:3000}],
  ['str_lowT',        {view:'str',mode:'osc',tension:TMIN,_live:60}],
  ['xt_empty',        {view:'xt'}],
  ['xt_osc',          {view:'xt',mode:'osc',_live:400}],
  ['xt_pulse_fixed',  {view:'xt',mode:'pulse',_pulse:1,_live:200}],
  ['refl_40',         {view:'refl',_refl:40}],
  ['refl_75',         {view:'refl',_refl:75}],
  ['refl_110',        {view:'refl',_refl:110}],
  ['stand_default',   {view:'stand',_stand:200}],
  ['stand_res',       {view:'stand',freq:1.25,damping:0.02,_stand:400}],
  ['stand_loose',     {view:'stand',end:'loose',freq:1.47,_stand:300}],
  ['stand_none',      {view:'stand',end:'none',_stand:200}],
  ['disp_default',    {view:'disp'}],
  ['disp_half',       {view:'disp',alpha:0.5}],
  ['disp_chain',      {view:'disp',alpha:0.05,tension:TMIN,freq:3}],
];
const CAP_NARROW=[['str_osc',CAP_SCENES[2][1]],['xt_osc',CAP_SCENES[9][1]],['refl_75',CAP_SCENES[12][1]],['stand_res',CAP_SCENES[15][1]],['disp_half',CAP_SCENES[19][1]]];
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
capWrite('display_narrow.json',820,520,CAP_NARROW);
capState({});
