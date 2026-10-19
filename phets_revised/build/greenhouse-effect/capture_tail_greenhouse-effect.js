/* capture_tail_greenhouse-effect.js — display-list capture for greenhouse-effect.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js
 *   capture_tail_greenhouse-effect.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log    (never through head/tail: a closed pipe
 * kills osascript before it writes display.json, and the next audit silently reads the
 * stale one).  Nothing here is named `run`: JXA calls a top-level run() for you.
 * The sky views are marched through stepFrame(), never by writing the temperature — the
 * photons only exist because real frames were pumped (wind_tunnel's advance()-not-step()
 * lesson, and the tautochrone's SIM.t = t lesson). */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const CAPS=[
  ['waves_default',   {view:'waves'},                                                 true, 60],
  ['waves_settling',  {view:'waves'},                                                 false,120],
  ['waves_1750',      {view:'waves',mode:'date',date:'y1750'},                        true, 60],
  ['waves_iceage',    {view:'waves',mode:'date',date:'iceAge',sheets:true},            true, 60],
  ['waves_2020_flux', {view:'waves',mode:'date',date:'y2020',flux:true},              true, 60],
  ['waves_c0_cloud',  {view:'waves',conc:0,cloud:true,unit:'K'},                      true, 60],
  ['waves_c1',        {view:'waves',conc:1,unit:'F',flux:true},                       true, 60],
  ['waves_sunoff',    {view:'waves',sun:false},                                       true, 60],
  ['photons_default', {view:'photons'},                                               true,420],
  ['photons_more',    {view:'photons',mode:'date',date:'y2020',morePhotons:true},     true,420],
  ['photons_c0',      {view:'photons',conc:0,flux:true},                              true,420],
  ['layers_0',        {view:'layers',nLayers:0},                                      true, 60],
  ['layers_3_black',  {view:'layers',nLayers:3,absorb:1,flux:true,sheets:true},        true, 60],
  ['layers_1_thin',   {view:'layers',nLayers:1,absorb:0.1,intensity:2,albedo:0.9,unit:'K'}, true,60],
  ['layers_2_kirch',  {view:'layers',nLayers:2,absorb:0.5,intensity:0.5,albedo:0,kirch:true}, true,60],
  ['ladder',          {view:'ladder'},                                                true,  0],
  ['ladder_K',        {view:'ladder',unit:'K',nLayers:3,absorb:0.6},                  true,  0],
  ['record',          {view:'record'},                                                true,  0],
  ['record_F_2020',   {view:'record',unit:'F',mode:'date',date:'y2020'},              true,  0]
];
for(const [name,over,jump,frames] of CAPS){
  Object.assign(ST,DEFAULTS,over);
  PROBE.z=PROBE0.z;
  resetThermal();
  if(jump) settle();
  ST.running=true;
  for(let k=0;k<frames;k++) stepFrame();
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  out.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS); resetThermal();
ObjC.import('Foundation');
const json=JSON.stringify(out);
$.NSString.alloc.initWithUTF8String(json)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+json.length+' bytes');
