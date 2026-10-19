/* capture_tail_waves-intro.js — display-list capture for waves-intro.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js capture_tail_waves-intro.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log      (never through head/tail: a closed pipe
 * kills osascript before it writes display.json, and the next audit silently reads the stale one)
 * The medium views are marched through runStep, never by setting the clock. */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const CAPS=[
  ['water_top',      {view:'water'},220,null],
  ['water_side',     {view:'water',look:'side',graph:true},220,null],
  ['water_tools',    {view:'water',tape:true,watch:true,meter:true,graph:true},220,R=>{ R.watch.on=true; }],
  ['water_pulse',    {view:'water',wave:'pulse'},95,R=>{ firePulse(R); }],
  ['water_off',      {view:'water'},220,null],
  ['water_quiet',    {view:'water',amp_water:0},120,null],
  ['sound_waves',    {view:'sound'},220,null],
  ['sound_particles',{view:'sound',soundView:'particles',graph:true},220,null],
  ['sound_both',     {view:'sound',soundView:'both',meter:true,tone:true},220,null],
  ['light_screen',   {view:'light'},300,null],
  ['light_inten',    {view:'light',inten:true,graph:true},300,null],
  ['light_violet',   {view:'light',f_light:SCENES.light.fmax},300,null],
  ['light_tools',    {view:'light',tape:true,watch:true,meter:true},300,null],
  ['media_default',  {view:'media'},0,null],
  ['media_ends',     {view:'media',f_water:SCENES.water.fmin,f_sound:SCENES.sound.fmax,f_light:SCENES.light.fmax},0,null],
];
for(const [name,over,steps,pre] of CAPS){
  Object.assign(ST,DEFAULTS,over); Object.assign(TOOLS,JSON.parse(JSON.stringify(TOOLS0)));
  if(MEDIA[ST.view]){
    resetRuns();
    const R=syncRun(ST.view);
    if(pre) pre(R);
    runFor(ST.view,steps);
    if(name==='water_off') pressSource(R);          /* the source switched off, its ripples still crossing */
  }
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  out.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS);
ObjC.import('Foundation');
const json=JSON.stringify(out);
$.NSString.alloc.initWithUTF8String(json)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+json.length+' bytes');
