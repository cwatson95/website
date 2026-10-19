/* capture_tail_projectile-motion.js — display-list capture for projectile-motion.html.
 *   cd build/projectile-motion/_out
 *   cat run.js ../../../../../projects/simulations/tools/recorder.js ../capture_tail_projectile-motion.js > cap_run.js
 *   osascript -l JavaScript cap_run.js > cap.log     (never through head/tail: a closed pipe kills
 *   the process before display.json is written, and the audit then reads a stale file)
 * No helper is named `run` (JXA calls a top-level run() itself — Known-bad). */
const CAPW=1100, CAPH=700;
const capOut={W:CAPW,H:CAPH,views:{}};
const flyC=(v,t)=>{ fire(v); advance(v,t); };
const CAP_SCENES=[
  ['launch_default',        {view:'intro'}, null],
  ['launch_flight_vectors', {view:'intro',i_air:true,i_vt:true,i_at:true}, v=>flyC(v,0.6)],
  ['launch_stars_probe',    {view:'intro',i_tgt:21.4,probe:true,tape:true}, v=>{ flyC(v,2); SCN[v].probe={x:7.5,y:8.77}; SCN[v].tape={x0:0,y0:0,x1:21.4,y1:0}; }],
  ['launch_zoomout_five',   {view:'intro',zoom:0.3,i_h:0,i_v0:30,i_air:true}, v=>{ for(const a of [15,30,45,60,75,85]){ ST.i_th=a; flyC(v,5); } }],
  ['launch_golf_zoom2',     {view:'intro',i_obj:'golfBall',zoom:2,i_h:3,i_th:30,i_v0:8,i_vc:true}, v=>flyC(v,0.5)],
  ['vectors_default',       {view:'vectors'}, null],
  ['vectors_components',    {view:'vectors',v_mode:'components',v_frc:true}, v=>flyC(v,1.0)],
  ['drag_default',          {view:'drag'}, null],
  ['drag_streamlined_5km',  {view:'drag',d_cd:0.04,d_alt:5000}, v=>flyC(v,1.5)],
  ['drag_blunt_vectors',    {view:'drag',d_cd:1,d_d:1,d_m:1,d_th:45,d_vel:true,d_frc:true}, v=>flyC(v,0.5)],
  ['lab_default',           {view:'lab'}, v=>flyC(v,1.2)],
  ['lab_custom_extreme',    {view:'lab',l_obj:'custom',l_m:1,l_d:3,l_cd:1,l_air:true,l_g:20,l_h:15,l_th:60,l_v0:30}, v=>flyC(v,3)],
  ['lab_piano_g20',         {view:'lab',l_obj:'piano',l_m:400,l_d:2.2,l_cd:1.2,l_air:true,l_g:20}, v=>flyC(v,5)],
  ['lab_midflight_bend',    {view:'lab',l_obj:'pumpkin',l_m:5,l_d:0.37,l_cd:0.6,l_air:true,l_th:45,l_v0:25}, v=>{ flyC(v,0.8); ST.l_air=false; retarget(v); advance(v,0.6); }],
  ['env_default',           {view:'env'}, null],
  ['env_air_off',           {view:'env',a_air:false}, null],
  ['env_height_slow',       {view:'env',a_h:15,a_v0:5}, null],
  ['env_zero_speed',        {view:'env',a_v0:0}, null],
  ['hodo_default',          {view:'hodo'}, null],
  ['hodo_air_off',          {view:'hodo',a_air:false}, null],
  ['hodo_sphere_80',        {view:'hodo',a_obj:'sphere',a_th:80,a_v0:18}, null],
  ['hodo_vertical',         {view:'hodo',a_th:90}, null],
  ['hodo_tank_shell',       {view:'hodo',a_obj:'tankShell'}, null],
];
const NARROW=['launch_flight_vectors','drag_default','env_default','hodo_default'];
function capOne(name,over,setup,W,H){
  Object.assign(ST,DEFAULTS,over); SCENE_VIEWS.forEach(scnReset);
  if(setup) setup(over.view);
  const rc=makeRecorder(W,H);
  drawView(rc,W,H,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+' '+W+'x'+H+': '+rc.ops.length+' ops');
}
for(const [name,over,setup] of CAP_SCENES) capOne(name,over,setup,CAPW,CAPH);
Object.assign(ST,DEFAULTS); SCENE_VIEWS.forEach(scnReset);
const json=JSON.stringify(capOut);
const outPath=$.NSFileManager.defaultManager.currentDirectoryPath.js+'/display.json';
$.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(outPath, true, $.NSUTF8StringEncoding, $());
console.log('wrote '+outPath+', '+json.length+' bytes');
/* the narrow stage, into its own file (audit.py takes one W,H per file) */
const capNarrow={W:560,H:380,views:{}};
for(const [name,over,setup] of CAP_SCENES) if(NARROW.indexOf(name)>=0){
  Object.assign(ST,DEFAULTS,over); SCENE_VIEWS.forEach(scnReset); if(setup) setup(over.view);
  const rc=makeRecorder(560,380); drawView(rc,560,380,buildModel()); capNarrow.views[name+'_narrow']=rc.ops; console.log(name+' 560x380: '+rc.ops.length+' ops'); }
Object.assign(ST,DEFAULTS); SCENE_VIEWS.forEach(scnReset);
const json2=JSON.stringify(capNarrow);
const outPath2=$.NSFileManager.defaultManager.currentDirectoryPath.js+'/display_narrow.json';
$.NSString.alloc.initWithUTF8String(json2).writeToFileAtomicallyEncodingError(outPath2, true, $.NSUTF8StringEncoding, $());
console.log('wrote '+outPath2+', '+json2.length+' bytes');
