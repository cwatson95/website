/* capture_tail_circuit-construction-kit-dc-virtual-lab.js -- display-list capture.
 *   python3 capture.py      (builds _out/cap_run.js = run.js + tools/recorder.js + this,
 *                             runs it with _out/ as the working directory, never through head/tail)
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
/* a custom bench, built with the same geometry format as the presets */
function capCustom(verts,els){ const C=newCircuit();
  verts.forEach((p,k)=>C.verts.push({id:k,x:p[0],y:p[1]}));
  els.forEach((e,k)=>C.els.push(makeEl(k,e[0],e[1],e[2],e[3]||{})));
  C.nv=verts.length; C.ne=els.length; return C; }
const CAP_HOUSE=()=>capCustom([[-51,120],[51,120],[160,120],[160,-10],[95,-10],[-35,-10],[-130,-10],[-205,-10],[-205,120],
    [95,-150],[5,-150],[-45,-10],[-45,-150]],
  [['battery',0,1],['wire',1,2],['wire',2,3],['wire',3,4],['pencil',4,5],['wire',5,11],['coin',11,6],['wire',6,7],['wire',7,8],['wire',8,0],
   ['wire',4,9],['eraser',9,10],['wire',10,12],['wire',12,11]]);
const CAP_MIX=()=>capCustom([[-51,130],[51,130],[180,130],[180,-20],[68,-20],[40,-20],[-70,-20],[-90,-20],[-190,-20],[-190,130]],
  [['battery',0,1],['wire',1,2],['wire',2,3],['switch',3,4,{closed:true}],['wire',4,5],['fuse',5,6],['wire',6,7],['rbulb',7,8],
   ['wire',8,9],['wire',9,0]]);
function capState(over){
  resetState({});
  if(over._preset) applyPreset(ST,over._preset);
  if(over._circ) ST.circ=over._circ();
  for(const k in over) if(k[0]!=='_') ST[k]=clone(over[k]);
  if(over._sel!==undefined) ST.sel=over._sel;
  if(over._r4!==undefined) ST.circ.els[9].R=over._r4;
  if(over._frames){ for(let f=0;f<over._frames;f++) advanceCharges(ST,solutionOf(ST),FRAME_DT); }
}
const CAP_SCENES=[
  ['lab_bulb',        {view:'lab',_frames:20}],
  ['lab_series_vals', {view:'lab',_preset:'series',showValues:true,_frames:30,_sel:3}],
  ['lab_parallel_sch',{view:'lab',_preset:'parallel',look:'schematic',showValues:true,_frames:30}],
  ['lab_bridge_meter',{view:'lab',_preset:'bridge',vm:{on:true,bx:40,by:150,rx:-120,ry:-30,kx:120,ky:-30},am:{on:true,bx:250,by:110,px:0,py:-140},_frames:10}],
  ['lab_twobat_conv', {view:'lab',_preset:'twobat',carrier:'conventional',showValues:true,_frames:40}],
  ['lab_short',       {view:'lab',_preset:'short',_frames:5,_sel:0}],
  ['lab_empty',       {view:'lab',_preset:'empty'}],
  ['lab_household',   {view:'lab',_circ:CAP_HOUSE,realBulbs:true,showValues:true,zoom:1.6,_frames:10}],
  ['lab_mix_schem',   {view:'lab',_circ:CAP_MIX,look:'schematic',showValues:true,realBulbs:true,_frames:10}],
  ['lab_mix_life',    {view:'lab',_circ:CAP_MIX,showValues:true,zoom:0.5,_frames:10}],
  ['graph_bulb',      {view:'graph'}],
  ['graph_bridge',    {view:'graph',_preset:'bridge'}],
  ['graph_twobat',    {view:'graph',_preset:'twobat'}],
  ['graph_empty',     {view:'graph',_preset:'empty'}],
  ['power_parallel',  {view:'power',_preset:'parallel'}],
  ['power_twobat',    {view:'power',_preset:'twobat'}],
  ['power_short',     {view:'power',_preset:'short'}],
  ['thev_bulb',       {view:'thev'}],
  ['thev_twobat_R3',  {view:'thev',_preset:'twobat',_sel:15}],
  ['thev_bridge_amm', {view:'thev',_preset:'bridge',_sel:12}],
  ['thev_battery',    {view:'thev',_preset:'twobat',_sel:0}],
  ['thev_real',       {view:'thev',_circ:CAP_MIX,_sel:7}],
  ['super_twobat',    {view:'super',_preset:'twobat'}],
  ['super_bulb',      {view:'super'}],
  ['super_empty',     {view:'super',_preset:'empty'}],
];
const CAP_NARROW=[['lab_bulb',CAP_SCENES[0][1]],['lab_bridge_meter',CAP_SCENES[3][1]],['graph_twobat',CAP_SCENES[12][1]],
                  ['power_twobat',CAP_SCENES[15][1]],['thev_twobat_R3',CAP_SCENES[18][1]],['super_twobat',CAP_SCENES[22][1]]];
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
