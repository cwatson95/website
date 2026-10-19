/* capture_tail_atomic-interactions.js — display-list capture.
 * cat _out/run.js ../../../../projects/simulations/tools/recorder.js \
 *     capture_tail_atomic-interactions.js > _out/cap_run.js
 * (cd _out && osascript -l JavaScript cap_run.js > cap.log)  — never through head/tail:
 * a closed pipe kills osascript BEFORE it writes display.json and the audit then
 * silently reports the previous run (Known-bad). */
const CAPW=1400, CAPH=820;
const capOut={W:CAPW,H:CAPH,views:{}};
/* a scene may need the clock run rather than the state set: reach t through
   S.step(), never by writing ST.t (cycloids Known-bad) */
function capRun(frames){
  const S=makeScene({getContext:()=>({})});
  releaseAtom(ST);
  for(let i=0;i<frames;i++) S.step();
}
const SCENES=[
  ['atoms_default',      {view:'atoms'},0],
  ['atoms_total_out',    {view:'atoms',forces:'total',r:420},0],
  ['atoms_components_in',{view:'atoms',forces:'components',r:300},0],
  ['atoms_far',          {view:'atoms',forces:'total',r:900},0],
  ['atoms_argon',        {view:'atoms',forces:'components',pair:'ArAr',r:460},0],
  ['atoms_oxygen',       {view:'atoms',forces:'total',pair:'OO',r:224.5},0],
  ['atoms_adjustable',   {view:'atoms',forces:'components',pair:'Adj',r:430},0],
  ['atoms_literature',   {view:'atoms',forces:'total',lit:true,r:330},0],
  ['well_default',       {view:'well'},0],
  ['well_components',    {view:'well',forces:'components',r:330},0],
  ['well_oxygen',        {view:'well',pair:'OO',r:230},0],
  ['well_adj_small',     {view:'well',pair:'Adj',adjSig:75,adjEps:20,r:90},0],
  ['well_adj_big',       {view:'well',pair:'Adj',adjSig:500,adjEps:450,r:600},0],
  ['motion_fresh',       {view:'motion'},0],
  ['motion_running',     {view:'motion',rel:10},220],
  ['motion_wide',        {view:'motion',rel:60},260],
  ['motion_escaping',    {view:'motion',rel:10,v0f:1.1},200],
  ['motion_free_argon',  {view:'motion',pair:'ArAr',pinned:false,rel:14},240],
  ['small_default',      {view:'small'},0],
  ['small_tiny',         {view:'small',amp:0.05},0],
  ['small_wide',         {view:'small',amp:60},0],
  ['small_free_lit',     {view:'small',pair:'ArAr',pinned:false,lit:true,amp:6},0],
  ['pairs_default',      {view:'pairs'},0],
  ['pairs_no_overlay',   {view:'pairs',showLit:false},0],
  ['steppers_neon',      {view:'steppers'},0],
  ['steppers_argon',     {view:'steppers',pair:'ArAr'},0],
];
for(const [name,over,frames] of SCENES){
  Object.assign(ST,DEFAULTS,over); simReset();
  if(frames) capRun(frames);
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
