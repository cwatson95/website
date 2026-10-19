
/* capture_tail_charges-and-fields.js — display-list capture.
 *   cat _out/run.js ../../../../projects/simulations/tools/recorder.js capture_tail_charges-and-fields.js > _out/cap_run.js
 *   osascript -l JavaScript _out/cap_run.js > _out/cap.log     (never through head/tail)
 * No helper here may be called run(): JXA invokes a top-level run() itself. */
const CAPW=1400, CAPH=820;
const capOut={W:CAPW,H:CAPH,views:{}};
const S3c=Math.sqrt(3);
const manyC=(()=>{ let s=12345; const r=()=>{ s=(s*1103515245+12345)%2147483648; return s/2147483648; };
  const o=[]; for(let k=0;k<40;k++) o.push({x:-3.6+7.2*r(),y:-1.5+3.8*r(),q:k%2?1:-1}); return o; })();
const SCENES=[
  ['plane_default',      {}],
  ['plane_empty',        {preset:'empty',charges:[],eqSeeds:[]}],
  ['plane_all_on',       {preset:'rows',charges:presetCharges('rows'),showV:true,showVals:true,showGrid:true,showTape:true,
                          eqSeeds:[{x:1.5,y:0.9},{x:2.6,y:0},{x:-2.4,y:1.6}],esens:[{x:-1.8,y:1.2},{x:3,y:-1.5},{x:0.25,y:0}]}],
  ['plane_voltage',      {showV:true,showE:false,eqSeeds:[{x:1.5,y:0.9},{x:0.9,y:0.0},{x:-1.1,y:0.6}]}],
  ['plane_dir_only',     {preset:'triangle',charges:presetCharges('triangle'),dirOnly:true,showVals:true,eqSeeds:[{x:0,y:0.05},{x:0,y:1.2}]}],
  ['plane_40_charges',   {preset:'custom',charges:manyC,showV:true,eqSeeds:[]}],
  ['plane_sensor_edge',  {vs:{x:3.6,y:-2.35},showVals:true,eqSeeds:[],esens:[{x:0.62,y:0.05}]}],
  ['lines_dipole',       {view:'lines'}],
  ['lines_rows',         {view:'lines',preset:'rows',charges:presetCharges('rows')}],
  ['lines_triangle',     {view:'lines',preset:'triangle',charges:presetCharges('triangle')}],
  ['lines_like_32',      {view:'lines',preset:'like',charges:presetCharges('like'),nLines:32}],
  ['lines_quad_nofam',   {view:'lines',preset:'quad',charges:presetCharges('quad'),showFam:false}],
  ['lines_empty',        {view:'lines',preset:'empty',charges:[]}],
  ['land_dipole',        {view:'land'}],
  ['land_rows_10V',      {view:'land',preset:'rows',charges:presetCharges('rows'),vcap:10}],
  ['land_triangle_top',  {view:'land',preset:'triangle',charges:presetCharges('triangle'),vcap:100,camPhi:1.45,eqSeeds:[{x:0,y:0.05}]}],
  ['land_like_low',      {view:'land',preset:'like',charges:presetCharges('like'),camPhi:0.12,camZoom:1.6,eqSeeds:[{x:0,y:0.4},{x:0,y:1.1}]}],
  ['super_dipole',       {view:'super'}],
  ['super_rows',         {view:'super',preset:'rows',charges:presetCharges('rows'),probe:{x:0.3,y:0.2}}],
  ['super_on_charge',    {view:'super',probe:{x:0.5,y:0}}],
  ['super_corner',       {view:'super',probe:{x:3.95,y:2.45}}],
  ['far_dipole',         {view:'far'}],
  ['far_bisector',       {view:'far',farTheta:90}],
  ['far_quad_diag',      {view:'far',preset:'quad',charges:presetCharges('quad'),farTheta:45}],
  ['far_rows',           {view:'far',preset:'rows',charges:presetCharges('rows'),farTheta:60}],
  ['far_triangle',       {view:'far',preset:'triangle',charges:presetCharges('triangle'),farTheta:20}],
  ['far_empty',          {view:'far',preset:'empty',charges:[]}],
];
const tCap0=Date.now();
for(const [name,over] of SCENES){
  resetState(over);
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
resetState();
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson)
  .writeToFileAtomicallyEncodingError('_out/display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote _out/display.json, '+capJson.length+' bytes in '+((Date.now()-tCap0)/1000).toFixed(1)+' s');
