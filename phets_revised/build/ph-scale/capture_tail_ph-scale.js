/* capture_tail_ph-scale.js — display-list capture for ph-scale.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js
 *   capture_tail_ph-scale.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log    (never through head/tail: a closed pipe
 * kills osascript before it writes display.json, and the next audit silently reads the
 * stale one).  Nothing here is named `run`: JXA calls a top-level run() for you.
 * The beaker is filled through stepFrame() wherever a configuration is meant to be
 * POURED rather than set, so the capture exercises the real clock (wind_tunnel's
 * advance()-not-step() lesson). */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const CAPS=[
  ['beaker_default',    {view:'beaker'},                                                    0],
  ['beaker_pouring',    {view:'beaker',vSolute:0,vWater:0,pourSolute:true},                60],
  ['beaker_diluted',    {view:'beaker',solute:'orangeJuice',vSolute:0.1,vWater:1.1},        0],
  ['beaker_drain',      {view:'beaker',solute:'drainCleaner',vSolute:0.9,vWater:0.3,drain:true},12],
  ['beaker_empty',      {view:'beaker',vSolute:0,vWater:0},                                 0],
  ['beaker_probe_out',  {view:'beaker',vSolute:0.1,vWater:0},                               0],
  ['beaker_phet_rule',  {view:'beaker',solute:'chickenSoup',vSolute:0.1,vWater:1.1,law:'phet'},0],
  ['beaker_milk_full',  {view:'beaker',solute:'milk',vSolute:1.2,vWater:0},                 0],
  ['particles_default', {view:'particles'},                                                 0],
  ['particles_base',    {view:'particles',solute:'drainCleaner',ratio:true,counts:true},     0],
  ['particles_acid',    {view:'particles',solute:'batteryAcid',vSolute:0.9,vWater:0.3,counts:true},0],
  ['particles_empty',   {view:'particles',vSolute:0,vWater:0},                              0],
  ['graph_log',         {view:'graph'},                                                     0],
  ['graph_log_moles',   {view:'graph',units:'moles',solute:'drainCleaner'},                 0],
  ['graph_linear',      {view:'graph',scaleKind:'linear',linExp:-7},                        0],
  ['graph_linear_top',  {view:'graph',scaleKind:'linear',linExp:1},                         0],
  ['graph_linear_deep', {view:'graph',scaleKind:'linear',linExp:-14,solute:'drainCleaner'}, 0],
  ['my_neutral',        {view:'my'},                                                        0],
  ['my_acid',           {view:'my',ph:-1,vMy:0.01},                                         0],
  ['my_base',           {view:'my',ph:15,vMy:1.2},                                          0],
  ['dilution_oj',       {view:'dilution'},                                                  0],
  ['dilution_base',     {view:'dilution',solute:'drainCleaner'},                            0],
  ['dilution_thin',     {view:'dilution',solute:'milk',vSolute:0.015,vWater:1.185},         0],
  ['dilution_water',    {view:'dilution',solute:'water'},                                   0],
  ['scale_default',     {view:'scale'},                                                     0],
  ['scale_blood',       {view:'scale',solute:'blood'},                                      0]
];
for(const [name,over,frames] of CAPS){
  Object.assign(ST,DEFAULTS,over);
  PROBE.x=PROBE0.x; PROBE.y=PROBE0.y;
  for(let k=0;k<frames;k++) stepFrame();
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
