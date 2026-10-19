/* capture_tail_beers-law-lab.js — display-list capture for beers-law-lab.html and
 * concentration.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js
 *   capture_tail_beers-law-lab.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log    (never through head/tail: a closed pipe
 * kills osascript before it writes display.json, and the next audit silently reads the
 * stale one).  Nothing here is named `run`: JXA calls a top-level run() for you.
 * Anything that is meant to be POURED is poured through stepFrame(), so the capture
 * exercises the real clock (wind_tunnel's advance()-not-step() lesson). */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
/* [name, ST overrides, {solute,n,V} for the beaker, frames of the real clock,
    {probe:[x,y], det:[x,y]}] */
const CAPS=[
  ['beaker_default',   {view:'beaker'},                        {n:0,V:0.5},          0,null],
  ['beaker_shaking',   {view:'beaker',form:'solid',shaking:true}, {n:0,V:0.6},      40,null],
  ['beaker_saturated', {view:'beaker',solute:'copperSulfate'},  {solute:'copperSulfate',n:3,V:0.5},0,null],
  ['beaker_empty',     {view:'beaker'},                         {n:0,V:0},           0,null],
  ['beaker_probe_out', {view:'beaker',solute:'potassiumPermanganate'},
                       {solute:'potassiumPermanganate',n:0.2,V:0.6}, 0,{probe:[0.5,0.95]}],
  ['beaker_dropper',   {view:'beaker',form:'solution',dropper:true,solute:'nickelIIChloride'},
                       {solute:'nickelIIChloride',n:0,V:0.4},  40,null],
  ['beaker_units',     {view:'beaker',meterUnits:'percent',beakerUnits:'milliliters',
                        showAmount:true,showVolume:true,solute:'potassiumChromate'},
                       {solute:'potassiumChromate',n:1.5,V:0.7}, 0,null],
  ['beaker_evap',      {view:'beaker',evap:PHET.EVAPORATION_MAX,solute:'cobaltChloride'},
                       {solute:'cobaltChloride',n:2,V:0.9},     30,null],
  ['beaker_full_drain',{view:'beaker',drain:true,solute:'drinkMix'},
                       {solute:'drinkMix',n:2,V:1},             20,null],
  ['ledger_run',       {view:'ledger',solute:'drinkMix',faucet:true,shaking:true,form:'solid'},
                       {solute:'drinkMix',n:0,V:0.2},          150,null],
  ['ledger_saturated', {view:'ledger',solute:'potassiumPermanganate'},
                       {solute:'potassiumPermanganate',n:0.3,V:0.5}, 0,null],
  ['ledger_empty',     {view:'ledger'},                         {n:0,V:0},           0,null],
  ['colour_default',   {view:'colour'},                         {n:0,V:0.5},         0,null],
  ['colour_illumA',    {view:'colour',illum:'A',blSolution:'potassiumPermanganate',
                        blConc:8e-4,cuvette:2,colourPath:2,solute:'potassiumPermanganate'},
                       {solute:'potassiumPermanganate',n:0.2,V:0.5}, 0,null],
  ['colour_thin',      {view:'colour',blSolution:'cobaltIINitrate',blConc:0.4,cuvette:0.5,
                        colourPath:0.05,solute:'cobaltIINitrate'},
                       {solute:'cobaltIINitrate',n:0.2,V:0.5},  0,null]
];
if(SHOW_BEERS){
  CAPS.push(
  ['cuvette_default',  {view:'cuvette'},                        null, 0,null],
  ['cuvette_full',     {view:'cuvette',blSolution:'potassiumPermanganate',blConc:8e-4,
                        cuvette:2,detector:'absorbance'},       null, 0,null],
  ['cuvette_zero',     {view:'cuvette',blConc:0,cuvette:0.5},    null, 0,null],
  ['cuvette_off',      {view:'cuvette',lightOn:false},           null, 0,null],
  ['cuvette_probe_out',{view:'cuvette'},                         null, 0,{det:[3.2,1.6]}],
  ['cuvette_variable', {view:'cuvette',lightMode:'variable',wavelength:410,
                        blSolution:'nickelIIChloride',blConc:0.35}, null,0,null],
  ['spectrum_default', {view:'spectrum'},                        null, 0,null],
  ['spectrum_all',     {view:'spectrum',allSpectra:true},        null, 0,null],
  ['spectrum_uM',      {view:'spectrum',blSolution:'potassiumDichromate',blConc:5e-4,
                        cuvette:2},                              null, 0,null],
  ['law_conc',         {view:'law'},                             null, 0,null],
  ['law_path',         {view:'law',lawX:'path',blSolution:'copperSulfate',blConc:0.2}, null,0,null],
  ['law_micro',        {view:'law',blSolution:'potassiumChromate',blConc:4e-4},        null,0,null]);
} else {
  CAPS.push(
  ['solutes_default',  {view:'solutes'},                         null, 0,null],
  ['solutes_kmno4',    {view:'solutes',solute:'potassiumPermanganate'},
                       {solute:'potassiumPermanganate',n:0.2,V:0.5}, 0,null]);
}
for(const [name,over,bk,frames,pos] of CAPS){
  Object.assign(ST,DEFAULTS,over);
  resetBeaker();
  if(bk){ BK.solute=bk.solute||ST.solute; BK.n=bk.n; BK.V=bk.V; resetLedger(); }
  PROBE.x=PROBE0.x; PROBE.y=PROBE0.y; DET.x=DET0.x; DET.y=DET0.y;
  if(pos&&pos.probe){ PROBE.x=pos.probe[0]; PROBE.y=pos.probe[1]; }
  if(pos&&pos.det){ DET.x=pos.det[0]; DET.y=pos.det[1]; }
  for(let k=0;k<frames;k++) stepFrame();
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  out.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS); resetBeaker();
ObjC.import('Foundation');
const json=JSON.stringify(out);
$.NSString.alloc.initWithUTF8String(json)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+json.length+' bytes');
