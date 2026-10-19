/* capture_tail_calculus-grapher.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_calculus-grapher.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (860 x 560).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(over){
  const clean={};
  for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  const d=buildDefaultCurve();
  CURVE=d.f; CFLAG=d.c;
  PRED=new Float64Array(NPTS); PFLAG=new Uint8Array(NPTS);
  if(over._recipe){
    let f=new Float64Array(NPTS), c=new Uint8Array(NPTS);
    for(const [mode,w,x,y] of over._recipe){ const o=manipulate(f,c,mode,w,x,y); f=o.f; c=o.c; }
    CURVE=f; CFLAG=c;
  }
  if(over._erase){ CURVE=new Float64Array(NPTS); CFLAG=new Uint8Array(NPTS); }
  if(over._pred){
    let f=new Float64Array(NPTS), c=new Uint8Array(NPTS);
    for(const [mode,w,x,y] of over._pred){ const o=manipulate(f,c,mode,w,x,y); f=o.f; c=o.c; }
    PRED=f; PFLAG=c;
  }
  if(over._smooth) for(let i=0;i<over._smooth;i++){ const o=smoothCurve(CURVE); CURVE=o.f; CFLAG=new Uint8Array(NPTS); }
  SAVED=CURVE.slice(); SFLAG=CFLAG.slice(); UNDO=[]; CVER++;
}
const TWO_HILLS=[['hill',2.0,2.5,1.2],['hill',2.0,7.0,-1.0]];
const CAP_SCENES=[
  ['deriv_default',    {view:'deriv'}],
  ['deriv_corner',     {view:'deriv',xT:6.9,_recipe:[['triangle',2.4,6.8,-1.2]]}],
  ['deriv_sinusoid',   {view:'deriv',mode:'sinusoid',_recipe:[['sinusoid',1.0,5.0,1.4]]}],
  ['deriv_predict',    {view:'deriv',predict:true,showF:true,_pred:[['hill',2.6,3.6,1.2]]}],
  ['deriv_erased',     {view:'deriv',_erase:1}],
  ['deriv_dashed',     {view:'deriv',discont:'dashedLine',values:true,_recipe:[['triangle',2.4,5.0,1.5]]}],
  ['integ_default',    {view:'integ',area:true,xA:6.4}],
  ['integ_crossing',   {view:'integ',area:true,xA:10,values:true,_recipe:TWO_HILLS}],
  ['integ_early',      {view:'integ',area:true,xA:1.2}],
  ['lab_default',      {view:'lab',refLine:true,values:true,xR:6.8}],
  ['lab_leibniz',      {view:'lab',refLine:true,notation:'leibniz',variable:'t',xR:3.2}],
  ['lab_predict',      {view:'lab',predict:true,showF:false,_pred:[['parabola',3.0,5.0,1.4]]}],
  ['corner_triangle',  {view:'corner',refShape:'triangle',refW:2,refY:1.5,refX:5,cornerSel:1}],
  ['corner_triangle0', {view:'corner',refShape:'triangle',refW:2,refY:1.5,refX:5,cornerSel:0}],
  ['corner_hill',      {view:'corner',refShape:'hill',refW:2,refY:1.5,refX:5}],
  ['corner_pedestal',  {view:'corner',refShape:'pedestal',refW:3,refY:1.2,refX:5}],
  ['corner_parabola',  {view:'corner',refShape:'parabola',refW:2.5,refY:-1.4,refX:5,cornerSel:0}],
  ['corner_sinusoid',  {view:'corner',refShape:'sinusoid',refW:0.6,refY:1.0,refX:5,cornerSel:0}],
  ['ftc_default',      {view:'ftc'}],
  ['ftc_two_hills',    {view:'ftc',_recipe:TWO_HILLS}],
  ['ftc_erased',       {view:'ftc',_erase:1}],
  ['ftc_smoothed',     {view:'ftc',_smooth:3}],
  ['grid_hill',        {view:'grid',refShape:'hill',refW:2,refY:1.5,refX:3,gridMult:2}],
  ['grid_hill_coarse', {view:'grid',refShape:'hill',refW:2,refY:1.5,refX:3,gridMult:0}],
  ['grid_triangle',    {view:'grid',refShape:'triangle',refW:2,refY:1.5,refX:4,gridMult:2}],
  ['grid_pedestal',    {view:'grid',refShape:'pedestal',refW:3,refY:1.2,refX:5,gridMult:4}],
  ['grid_sinusoid',    {view:'grid',refShape:'sinusoid',refW:2,refY:1,refX:5,gridMult:3}],
];
const CAP_NARROW=[['deriv_default',CAP_SCENES[0][1]],['integ_default',CAP_SCENES[6][1]],
                  ['lab_default',CAP_SCENES[9][1]],['corner_triangle',CAP_SCENES[12][1]],
                  ['ftc_default',CAP_SCENES[18][1]],['grid_hill',CAP_SCENES[22][1]]];
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
capWrite('display_narrow.json',860,560,CAP_NARROW);
capState({});
