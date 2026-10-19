/* capture_tail_under-pressure.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_under-pressure.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capStateP(over){
  Object.assign(ST,DEFAULTS,over);
  clearAll();
}
const CAP_SCENES=[
  ['pool_default',      {view:'pool'}],
  ['pool_empty',        {view:'pool',volFrac:0}],
  ['pool_full',         {view:'pool',volFrac:1}],
  ['pool_grid_ruler',   {view:'pool',gridOn:true,rulerOn:true}],
  ['pool_feet_psi',     {view:'pool',units:'english',gridOn:true,rulerOn:true}],
  ['pool_no_atmosphere',{view:'pool',atmosphere:false,units:'atmosphere'}],
  ['pool_honey_jupiter',{view:'pool',rho:RHO_HONEY,grav:G_JUPITER}],
  ['pool_gasoline_mars',{view:'pool',rho:RHO_GASOLINE,grav:G_MARS}],
  ['pool_gauge_outside',{view:'pool',gAx:1.75,gAy:0.35,gBx:6.5,gBy:-0.4}],
  ['shapes_default',    {view:'shapes',gAx:2.4,gAy:-2.2,gBx:6.6,gBy:-2.2}],
  ['shapes_deep_pair',  {view:'shapes',volFrac:tzVolume(0.5)/TZ_VMAX,gAx:2.3,gAy:-2.75,gBx:6.7,gBy:-2.75}],
  ['shapes_in_channel', {view:'shapes',volFrac:0.05,gAx:2.4,gAy:-2.93,gBx:6.6,gBy:-2.93}],
  ['shapes_full',       {view:'shapes',volFrac:1,units:'atmosphere',gAx:3.0,gAy:-0.4,gBx:6.4,gBy:-2.7}],
  ['press_empty',       {view:'press',m500:false,gAx:2.95,gAy:-2.4,gBx:6.8,gBy:-2.4}],
  ['press_500',         {view:'press',m500:true,gAx:2.95,gAy:-2.4,gBx:6.8,gBy:-2.4}],
  ['press_1000',        {view:'press',m500:true,m250a:true,m250b:true,gAx:2.95,gAy:-2.4,gBx:6.8,gBy:-2.4}],
  ['press_capped',      {view:'press',rho:RHO_GASOLINE,m500:true,m250a:true,m250b:true,gAx:2.95,gAy:-2.4,gBx:6.8,gBy:-2.4}],
  ['press_honey_psi',   {view:'press',rho:RHO_HONEY,units:'english',m500:true,m250a:true}],
  ['mystery_fluid_A',   {view:'mystery'}],
  ['mystery_surface',   {view:'mystery',myDepth:0}],
  ['mystery_revealed',  {view:'mystery',myWhich:1,myGuess:'1',myReveal:true}],
  ['mystery_planet',    {view:'mystery',myMode:'planet',myWhich:2,myReveal:true,units:'atmosphere'}],
  ['paradox_default',   {view:'paradox'}],
  ['paradox_shallow',   {view:'paradox',parDepth:0.5,parPick:'tapered'}],
  ['paradox_stepped',     {view:'paradox',parPick:'stepped',rho:RHO_HONEY,grav:G_JUPITER}],
  ['column_default',    {view:'column'}],
  ['column_atm',        {view:'column',units:'atmosphere',colDepth:3}],
  ['column_psi_vacuum', {view:'column',units:'english',atmosphere:false,colAll:false}],
  ['column_mars',       {view:'column',grav:G_MARS,rho:RHO_GASOLINE,colDepth:0}],
];
const CAP_NARROW=[['pool_default',CAP_SCENES[0][1]],['shapes_default',CAP_SCENES[9][1]],
                  ['press_1000',CAP_SCENES[15][1]],['mystery_fluid_A',CAP_SCENES[18][1]],
                  ['paradox_default',CAP_SCENES[22][1]],['column_default',CAP_SCENES[25][1]]];
ObjC.import('Foundation');
function capWriteP(file,W,H,list){
  const out={W,H,views:{}};
  for(const pair of list){
    const name=pair[0], over=pair[1];
    capStateP(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,buildModel(ST),ST);
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWriteP('display.json',1400,820,CAP_SCENES);
capWriteP('display_narrow.json',820,520,CAP_NARROW);
capStateP({});
