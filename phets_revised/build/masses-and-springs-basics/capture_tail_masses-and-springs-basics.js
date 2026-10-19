/* capture_tail_masses-and-springs-basics.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_masses-and-springs-basics.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * Time is reached by STEPPING (advance), never by writing the clock, so the
 * integrated state matches the picture (Known-bad: a capture that sets the
 * clock leaves integrated states at their releases).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  if(clean.damping===undefined&&VIEW_DAMPING[ST.view]!==undefined) ST.damping=VIEW_DAMPING[ST.view];
  liveReset(); DRAG.what=null;
  if(over._live&&liveViews(ST.view)) for(let k=0;k<over._live;k++) advance(ST,0.02);
  if(over._sw!==undefined){ LIVE.sw=over._sw; LIVE.swOn=true; }
}
const CAP_SCENES=[
  ['str_default',    {view:'str'}],
  ['str_settled',    {view:'str',_live:300}],
  ['str_soft_stiff', {view:'str',k1:3,k2:12,mass1:'m250',mass2:'m50',_live:300}],
  ['str_moon',       {view:'str',body:'moon',_live:300}],
  ['str_jupiter',    {view:'str',body:'jupiter',k1:3,mass1:'m250',_live:300}],
  ['str_tools',      {view:'str',ruler:true,movLine:true,stopwatch:true,_sw:3.21,_live:300}],
  ['str_empty',      {view:'str',mass1:'none',mass2:'none'}],
  ['str_mystery',    {view:'str',mass1:'q200',mass2:'q75',_live:300}],
  ['str_floor',      {view:'str',body:'custom',gCustom:30,k1:3,mass1:'m250',_live:300}],
  ['bnc_start',      {view:'bnc'}],
  ['bnc_mid',        {view:'bnc',_live:90}],
  ['bnc_long',       {view:'bnc',k1:3,k2:12,_live:320}],
  ['bnc_damped',     {view:'bnc',damping:0.5,_live:220}],
  ['lab_default',    {view:'lab',_live:260}],
  ['lab_planetX',    {view:'lab',body:'planetX',_live:300}],
  ['lab_heavy_soft', {view:'lab',kl:3,massG:300,ruler:true,_live:340}],
  ['lab_light_damped',{view:'lab',kl:12,massG:50,damping:0.6,_live:260}],
  ['lab_zero_g',     {view:'lab',body:'custom',gCustom:0,_live:200}],
  ['per_default',    {view:'per'}],
  ['per_soft_heavy', {view:'per',kA:3,mAg:300,damping:0.7}],
  ['dmp_default',    {view:'dmp'}],
  ['dmp_critical',   {view:'dmp',zeta:1}],
  ['dmp_tiny',       {view:'dmp',zeta:0.02,kA:3,mAg:300}],
  ['eng_undamped',   {view:'eng',damping:0,_live:120}],
  ['eng_damped',     {view:'eng',damping:0.5,_live:120}],
];
const CAP_NARROW=[['str_soft_stiff',CAP_SCENES[2][1]],['bnc_mid',CAP_SCENES[10][1]],
                  ['lab_planetX',CAP_SCENES[14][1]],['per_default',CAP_SCENES[18][1]],
                  ['dmp_default',CAP_SCENES[20][1]],['eng_damped',CAP_SCENES[24][1]]];
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
