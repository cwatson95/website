/* capture_tail_density.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_density.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capStateD(over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  MEMO.pool=MEMO.sets=MEMO.mystery=MEMO.mv=MEMO.line=null;
  /* the coupling has to be re-applied after a bare Object.assign, exactly as a
     material chip would: otherwise a preset can carry an illegal (m, V) pair */
  if(over._syncA!==false){ setMat(ST,'A',ST.matA); if(over.volAL!==undefined) setVol(ST,'A',over.volAL);
    if(over.massA!==undefined) setMass(ST,'A',over.massA); }
  setMat(ST,'B',ST.matB);
  MEMO.pool=MEMO.sets=MEMO.mystery=MEMO.mv=MEMO.line=null;
}
const CAP_SCENES=[
  ['pool_default',     {view:'pool'}],
  ['pool_two',         {view:'pool',two:true}],
  ['pool_styrofoam',   {view:'pool',matA:'styrofoam',volAL:10}],
  ['pool_brick',       {view:'pool',matA:'brick',volAL:3}],
  ['pool_custom_heavy',{view:'pool',matA:'custom',massA:27,volAL:1,_syncA:false}],
  ['pool_held_under',  {view:'pool',holdA:-POOL_H}],
  ['pool_held_aloft',  {view:'pool',holdA:0.03}],
  ['pool_no_forces',   {view:'pool',forces:false}],
  ['sets_mass',        {view:'sets',setMode:'mass'}],
  ['sets_mass_10',     {view:'sets',setMode:'mass',sameMass:10}],
  ['sets_volume',      {view:'sets',setMode:'volume'}],
  ['sets_volume_10',   {view:'sets',setMode:'volume',sameVolL:10}],
  ['sets_density',     {view:'sets',setMode:'density'}],
  ['sets_density_1800',{view:'sets',setMode:'density',sameRho:1800}],
  ['mystery_1',        {view:'mystery',mset:'set 1'}],
  ['mystery_2',        {view:'mystery',mset:'set 2',mpick:'E'}],
  ['mystery_3',        {view:'mystery',mset:'set 3',mpick:'C',reveal:true}],
  ['mystery_floating', {view:'mystery',mset:'set 1',submerge:false}],
  ['mystery_shuffled', {view:'mystery',mset:'shuffled',seed:20260921}],
  ['mv_wood',          {view:'mv'}],
  ['mv_gold',          {view:'mv',mvMat:'gold'}],
  ['mv_styrofoam',     {view:'mv',mvMat:'styrofoam'}],
  ['mv_no_ref',        {view:'mv',mvMat:'pyrite',showRef:false}],
  ['line_water',       {view:'line'}],
  ['line_mercury',     {view:'line',lineFluid:'mercury'}],
  ['line_gasoline',    {view:'line',lineFluid:'gasoline'}],
  ['line_sinking',     {view:'line',matA:'brick'}],
  ['line_neutral',     {view:'line',matA:'custom',massA:5,volAL:5,_syncA:false}],
];
const CAP_NARROW=[['pool_default',CAP_SCENES[0][1]],['sets_mass',CAP_SCENES[8][1]],
                  ['mystery_1',CAP_SCENES[14][1]],['mv_wood',CAP_SCENES[19][1]],
                  ['line_mercury',CAP_SCENES[24][1]]];
ObjC.import('Foundation');
function capWriteD(file,W,H,list){
  const out={W,H,views:{}};
  for(const pair of list){
    const name=pair[0], over=pair[1];
    capStateD(over);
    const rc=makeRecorder(W,H);
    drawView(rc,W,H,buildModel(ST),ST);
    out.views[name]=rc.ops;
    console.log(file+' '+name+': '+rc.ops.length+' ops');
  }
  const json=JSON.stringify(out);
  $.NSString.alloc.initWithUTF8String(json).writeToFileAtomicallyEncodingError(file,true,$.NSUTF8StringEncoding,$());
  console.log('wrote '+file+', '+json.length+' bytes');
}
capWriteD('display.json',1400,820,CAP_SCENES);
capWriteD('display_narrow.json',820,520,CAP_NARROW);
capStateD({});
