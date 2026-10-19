/* ============ display-list capture for bending-light.html ================= *
 * cat _out/run.js tools/recorder.js capture_tail_bending-light.js > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log   (never through head: Known-bad)
 * Writes display.json in the working directory.  No helper is named `run`
 * (JXA calls a top-level run() with argv: Known-bad).                        */
const CAP_W=1400, CAP_H=820;
const capOut={W:CAP_W,H:CAP_H,views:{}};
function capConfig(name,over){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  for(const k in MEMO) delete MEMO[k];
  if(over._phase!==undefined) ST.phase=over._phase;
  const rc=makeRecorder(CAP_W,CAP_H);
  drawView(rc,CAP_W,CAP_H,buildModel(ST),ST);
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
capConfig('bound_default',{view:'bound'});
capConfig('bound_normal',{view:'bound',angDeg:0});
capConfig('bound_grazing',{view:'bound',angDeg:88,showProtractor:true});
capConfig('bound_tir',{view:'bound',topSub:'water',botSub:'air',angDeg:70});
capConfig('bound_tir_edge',{view:'bound',topSub:'diamond',botSub:'air',angDeg:24.4});
capConfig('bound_white',{view:'bound',white:true,botSub:'diamond'});
capConfig('bound_brewster',{view:'bound',angDeg:56.3,botSub:'glass',pol:'p'});
capConfig('bound_off',{view:'bound',laserOn:false});
capConfig('wave_default',{view:'wave',_phase:0});
capConfig('wave_quarter',{view:'wave',_phase:PI/2});
capConfig('wave_tir',{view:'wave',topSub:'glass',botSub:'air',angDeg:60});
capConfig('wave_dense',{view:'wave',botSub:'diamond',angDeg:65,lamNm:450});
capConfig('wave_nofield',{view:'wave',paintField:false,angDeg:20});
capConfig('prism_triangle',{view:'prism'});
capConfig('prism_constant_dev',{view:'prism',beamY:1.3,beamTilt:-7});
capConfig('prism_white',{view:'prism',white:true});
capConfig('prism_white_fan',{view:'prism',white:true,manyRays:true});
capConfig('prism_diamond',{view:'prism',prismSub:'diamond',showReflections:true});
capConfig('prism_square',{view:'prism',prismId:'square',prismRot:20,showNormals:true});
capConfig('prism_circle',{view:'prism',prismId:'circle',white:true,beamY:2.4});
capConfig('prism_semicircle',{view:'prism',prismId:'semicircle',prismRot:0,beamY:0.9});
capConfig('prism_trapezoid',{view:'prism',prismId:'trapezoid',prismRot:-30,showReflections:true});
capConfig('fres_default',{view:'fres'});
capConfig('fres_tir',{view:'fres',topSub:'glass',botSub:'air'});
capConfig('fres_diamond',{view:'fres',botSub:'diamond',angDeg:67.5});
capConfig('spec_default',{view:'spec'});
capConfig('spec_water',{view:'spec',prismSub:'water',prismApex:45});
capConfig('spec_steep',{view:'spec',prismApex:75,prismSub:'diamond'});
capConfig('bow_primary',{view:'bow'});
capConfig('bow_secondary',{view:'bow',bowK:2});
capConfig('bow_white',{view:'bow',white:true,bowRays:false});
capConfig('bow_violet',{view:'bow',lamNm:400,bowPol:'s'});
ObjC.import('Foundation');
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson).writeToFileAtomicallyEncodingError('display.json',true,$.NSUTF8StringEncoding,$());
console.log('wrote display.json, '+capJson.length+' bytes');
