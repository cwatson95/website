/* capture_tail_sound-waves.js — display-list capture for sound-waves.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js capture_tail_sound-waves.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log      (never through head/tail: a closed pipe
 * kills osascript before it writes display.json, and the next audit silently reads the stale one)
 * The room is marched through runStep, never by setting the clock. */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const CAPS=[
  ['speaker',        {view:'intro'},340,null],
  ['speaker_1000',   {view:'intro',f:1000,graph:true},340,null],
  ['speaker_100',    {view:'intro',f:100,graph:true},340,null],
  ['speaker_parcels',{view:'intro',look:'particles'},340,null],
  ['speaker_both',   {view:'intro',look:'both'},340,null],
  ['speaker_off',    {view:'intro'},340,'off'],
  ['speaker_pulse',  {view:'intro',wave:'pulse'},110,'pulse'],
  ['bench',          {view:'measure',ruler:true,watch:true,graph:true},340,'watch'],
  ['bench_quiet',    {view:'measure',amp:0,ruler:true},160,null],
  ['two',            {view:'two'},460,null],
  ['two_close',      {view:'two',spk2y:4.4,f:900},460,null],
  ['two_low',        {view:'two',f:100},460,null],
  ['wall',           {view:'wall'},460,null],
  ['wall_upright',   {view:'wall',wallAng:WALLR.amax,wallX:WALLR.xmin},460,null],
  ['wall_flat',      {view:'wall',wallAng:WALLR.amin,wallX:WALLR.xmax,graph:true},460,null],
  ['air_full',       {view:'air'},340,null],
  ['air_thin',       {view:'air',pressure:0.12},340,null],
  ['air_vacuum',     {view:'air',pressure:0},340,null],
  ['law',            {view:'law'},0,null],
  ['law_1000',       {view:'law',f:1000},0,null],
];
for(const [name,over,steps,pre] of CAPS){
  Object.assign(ST,DEFAULTS,over);
  TOOLS.ruler=TOOLS0.ruler.slice(); TOOLS.listener=TOOLS0.listener.slice();
  resetAll();
  Object.assign(ST,DEFAULTS,over);
  if(pre==='pulse'){ setWaveMode(RUN,false); firePulse(RUN); }
  if(pre==='watch') CLOCK.watchOn=true;
  runFor(steps);
  if(pre==='off') pressSource(RUN);        /* switched off, its sound still crossing the room */
  if(ST.view==='law'){ for(let q=0;q<12;q++){ const M=buildModel(); if(!M.X.pending) break; } }
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
