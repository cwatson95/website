/* capture_tail_geometric-optics.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_geometric-optics.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)   never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capStateO(over){
  Object.assign(ST,DEFAULTS,over);
  clearMemo();
}
const CAP_SCENES=[
  ['lens_default',      {view:'bench'}],
  ['lens_at_2F',        {view:'bench',objX:-160}],
  ['lens_inside_F',     {view:'bench',objX:-50}],
  ['lens_at_F',         {view:'bench',objX:-80}],
  ['lens_concave',      {view:'bench',lensSurface:'concave'}],
  ['lens_principal',    {view:'bench',rays:'principal'}],
  ['lens_many',         {view:'bench',rays:'many',objX:-320}],
  ['lens_none_2F',      {view:'bench',rays:'none',show2F:true}],
  ['lens_second_point', {view:'bench',showSecond:true,objKind:'arrow'}],
  ['lens_guides',       {view:'bench',showGuides:true}],
  ['lens_light_screen', {view:'bench',objKind:'light',showSecond:true}],
  ['lens_light_far',    {view:'bench',objKind:'light',screenX:400}],
  ['lens_penguin_ruler',{view:'bench',objKind:'penguin',showRuler:true,objY:80}],
  ['lens_star_big_D',   {view:'bench',objKind:'star',lensD:120,lensR:40}],
  ['lens_axial_object', {view:'bench',objY:0,rays:'many'}],
  ['mirror_concave',    {view:'mirror'}],
  ['mirror_inside_F',   {view:'mirror',objX:-60}],
  ['mirror_convex',     {view:'mirror',mirrorSurface:'convex'}],
  ['mirror_flat',       {view:'mirror',mirrorSurface:'flat'}],
  ['mirror_many',       {view:'mirror',rays:'many',objX:-400}],
  ['conj_converging',   {view:'conj'}],
  ['conj_at_pole',      {view:'conj',objX:-80}],
  ['conj_inside_F',     {view:'conj',objX:-45}],
  ['conj_diverging',    {view:'conj',lensSurface:'concave'}],
  ['maker_default',     {view:'maker'}],
  ['maker_direct',      {view:'maker',fControl:'direct',lensF:120}],
  ['maker_impossible',  {view:'maker',lensR:40,lensD:120}],
  ['guides_default',    {view:'guides'}],
  ['guides_concave',    {view:'guides',lensSurface:'concave'}],
  ['guides_near_axis',  {view:'guides',objY:4,objX:-300}],
  ['real_default',      {view:'real'}],
  ['real_stopped',      {view:'real',realStop:0.3}],
  ['real_thick_edge',   {view:'real',realEdge:10,realH:0.5}],
  ['real_high_index',   {view:'real',lensN:1.8,lensR:120}],
  ['real_impossible',   {view:'real',lensR:40,lensD:120}],
];
const CAP_NARROW=[['lens_default',CAP_SCENES[0][1]],['mirror_concave',CAP_SCENES[15][1]],
                  ['conj_converging',CAP_SCENES[20][1]],['maker_default',CAP_SCENES[24][1]],
                  ['guides_default',CAP_SCENES[27][1]],['real_default',CAP_SCENES[30][1]]];
ObjC.import('Foundation');
function capWriteO(file,W,H,list){
  const out={W,H,views:{}};
  for(const pair of list){
    const name=pair[0], over=pair[1];
    capStateO(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,buildModel(ST),ST);
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWriteO('display.json',1400,820,CAP_SCENES);
capWriteO('display_narrow.json',820,520,CAP_NARROW);
capStateO({});
