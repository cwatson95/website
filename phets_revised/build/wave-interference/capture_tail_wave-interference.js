/* capture_tail_wave-interference.js — display-list capture for wave-interference.html.
 * { echo "var CAP_W=1400, CAP_H=820;"; cat _out/run.js <sim>/tools/recorder.js capture_tail_wave-interference.js; } > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log      (never through head/tail)
 * Lattice views are marched through runStep (never by setting the clock) to a filled state. */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const CAPS=[
  ['tank_water',        {view:'tank'},300,null],
  ['tank_side_tools',   {view:'tank',look:'side',graph:true,tape:true,watch:true,meter:true},300,R=>{ R.watch.on=true; }],
  ['tank_sound_both',   {view:'tank',scene:'sound',soundView:'both'},260,null],
  ['tank_sound_parcels',{view:'tank',scene:'sound',soundView:'particles',graph:true},260,null],
  ['tank_light_all',    {view:'tank',scene:'light',graph:true,meter:true},300,null],
  ['tank_light_violet', {view:'tank',scene:'light',f_light:SCENES.light.fmax},300,null],
  ['tank_water_pulse',  {view:'tank',wave:'pulse'},110,R=>{ firePulse(R); }],
  ['two_water',         {view:'two'},300,null],
  ['two_sound',         {view:'two',scene:'sound',sep_sound:320},300,null],
  ['two_light',         {view:'two',scene:'light'},340,null],
  ['slits_light_two',   {view:'slits',scene:'light',barrier:'two'},420,null],
  ['slits_light_one',   {view:'slits',scene:'light',barrier:'one',graph:true},420,null],
  ['slits_water_two',   {view:'slits',barrier:'two',graph:true,tape:true},400,null],
  ['slits_sound_one',   {view:'slits',scene:'sound',barrier:'one',bcol:40},380,null],
  ['far_ellipse',       {view:'far'},0,null],
  ['far_rect',          {view:'far',ap:'rect',recW:0.3,recH:0.06},0,null],
  ['far_cs',            {view:'far',ap:'cs'},0,null],
  ['far_disorder',      {view:'far',ap:'disorder',disL:3},0,null],
  ['far_figure',        {view:'far',ap:'figure',figH:0.25,figR:20},0,null],
  ['far_gauss_lin',     {view:'far',ap:'gauss',farMode:'lin'},0,null],
  ['far_slits5_red',    {view:'far',ap:'slits',sltN:5,lam:700},0,null],
  ['path_default',      {view:'path'},0,null],
  ['path_near',         {view:'path',pd:8,pL:3},0,null],
  ['lattice_water',     {view:'lattice'},0,null],
  ['lattice_light',     {view:'lattice',scene:'light',latTh:20},0,null],
];
for(const [name,over,steps,pre] of CAPS){
  Object.assign(ST,DEFAULTS,over); Object.assign(TOOLS,JSON.parse(JSON.stringify(TOOLS0)));
  if(LATTICE_VIEWS[ST.view]){ resetRuns(); const R=syncRun(ST.view); if(pre) pre(R); runFor(ST.view,steps); }
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
