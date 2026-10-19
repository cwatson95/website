/* capture_tail_buoyancy-basics.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_buoyancy-basics.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capStateB(over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  clearAll();
  /* the coupling has to be re-applied after a bare Object.assign, exactly as a
     material chip would, or a preset can carry an illegal (m, V) pair */
  if(over._syncA!==false){ setMat(ST,'A',ST.matA); if(over.volAL!==undefined) setVol(ST,'A',over.volAL);
    if(over.massA!==undefined) setMass(ST,'A',over.massA); }
  setMat(ST,'B',ST.matB);
  clearAll();
}
const CAP_SCENES=[
  ['explore_default',   {view:'explore'}],
  ['explore_two',       {view:'explore',two:true}],
  ['explore_mercury',   {view:'explore',fluid:'mercury',two:true,matA:'aluminum',massA:13.5,volAL:5}],
  ['explore_gasoline',  {view:'explore',fluid:'gasoline'}],
  ['explore_honey',     {view:'explore',fluid:'honey',matA:'pvc',volAL:6,_syncA:false}],
  ['explore_poolscale', {view:'explore',where:'poolscale',matA:'aluminum',massA:13.5,volAL:5}],
  ['explore_ground',    {view:'explore',where:'ground',matA:'aluminum',massA:13.5,volAL:5}],
  ['explore_scale_low', {view:'explore',where:'poolscale',scaleH:0}],
  ['explore_held',      {view:'explore',holdA:-POOL_H}],
  ['explore_no_forces', {view:'explore',forces:false}],
  ['sets_mass',         {view:'sets',setMode:'mass'}],
  ['sets_volume',       {view:'sets',setMode:'volume'}],
  ['sets_density',      {view:'sets',setMode:'density'}],
  ['sets_density_2500', {view:'sets',setMode:'density',sameRho:2500}],
  ['sets_honey',        {view:'sets',setMode:'mass',fluid:'honey'}],
  ['faces_deep',        {view:'faces',facesDepth:0.6,matA:'brick',volAL:5}],
  ['faces_mid',         {view:'faces',facesDepth:0.30,matA:'brick',volAL:5}],
  ['faces_shallow',     {view:'faces',facesDepth:0.08,matA:'brick',volAL:5}],
  ['faces_mercury',     {view:'faces',fluid:'mercury',facesDepth:0.5,matA:'brick',volAL:5}],
  ['faces_big',         {view:'faces',facesDepth:0.8,matA:'brick',volAL:10}],
  ['scale_top',         {view:'scale',lowered:0,matA:'brick',volAL:5}],
  ['scale_entering',    {view:'scale',lowered:0.45,matA:'brick',volAL:5}],
  ['scale_under',       {view:'scale',lowered:0.85,matA:'brick',volAL:5}],
  ['scale_wood',        {view:'scale',lowered:1}],
  ['scale_mercury',     {view:'scale',lowered:1,fluid:'mercury',matA:'aluminum',massA:13.5,volAL:5}],
  ['fluids_wood',       {view:'fluids'}],
  ['fluids_gold',       {view:'fluids',gridMat:'gold'}],
  ['fluids_lead',       {view:'fluids',gridMat:'lead'}],
];
const CAP_NARROW=[['explore_default',CAP_SCENES[0][1]],['sets_mass',CAP_SCENES[10][1]],
                  ['faces_mid',CAP_SCENES[16][1]],['scale_entering',CAP_SCENES[21][1]],
                  ['fluids_wood',CAP_SCENES[25][1]]];
ObjC.import('Foundation');
function capWriteB(file,W,H,list){
  const out={W,H,views:{}};
  for(const pair of list){
    const name=pair[0], over=pair[1];
    capStateB(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,buildModel(ST),ST);
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWriteB('display.json',1400,820,CAP_SCENES);
capWriteB('display_narrow.json',820,520,CAP_NARROW);
capStateB({});
