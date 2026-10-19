
/* ============ display-list capture for molecule-shapes.html ================ *
 * cat _out/run.js tools/recorder.js capture_tail_molecule-shapes.js > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log   (never through head: Known-bad)
 * Writes display.json in the working directory.  No helper is named `run`
 * (JXA calls a top-level run() with argv: Known-bad).                        */
const CAP_W=1400, CAP_H=820;
const capOut={W:CAP_W,H:CAP_H,views:{}};
function capConfig(name,over,prep){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  liveInit(); LIVE.realBlend=0; RELAX.seed=0; RELAX.key='';
  if(over._empty) liveRemoveAll();
  if(over._load) liveLoad(over._load[0],over._load[1]);
  if(over._add) for(const o of over._add) liveAdd(o);
  liveSettle();
  if(over._blend!==undefined) LIVE.realBlend=over._blend;
  if(over._seed!==undefined) RELAX.seed=over._seed;
  if(over._run!==undefined){ relaxEnsure(); if(over._run==='all') relaxRun(); else for(let k=0;k<over._run;k++) relaxAdvance(1); }
  if(prep) prep();
  const rc=makeRecorder(CAP_W,CAP_H);
  drawView(rc,CAP_W,CAP_H,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
const LPS=VARIANT!=='basics';
capConfig('model_default',{view:'model',showAngles:true});
capConfig('model_water',{view:'model',_load:[2,LPS?2:0],showAngles:true,showMolName:true,showElName:true});
capConfig('model_pyramid',{view:'model',_load:[3,LPS?1:0],showAngles:true});
capConfig('model_seesaw',{view:'model',_load:[4,LPS?1:0],showAngles:true,showMolName:true,showElName:true});
capConfig('model_octa',{view:'model',_load:[6,0],showAngles:true,showMolName:true});
capConfig('model_tbp',{view:'model',_load:[5,0],showAngles:true});
capConfig('model_orders',{view:'model',_add:LPS?[2,3,0]:[2,3,1]});
capConfig('model_empty',{view:'model',_empty:true,showMolName:true});
capConfig('model_dragging',{view:'model',_load:[3,LPS?2:0],showAngles:true},()=>{
  const S=makeScene({getContext:()=>makeRecorder(CAP_W,CAP_H)}); S.W=CAP_W; S.H=CAP_H;
  drawView(makeRecorder(CAP_W,CAP_H),CAP_W,CAP_H,buildModel());
  const p=PICK.find(q=>LIVE.groups[q.i].order>0); S.pointer('down',p.x,p.y); S.pointer('move',p.x+90,p.y-60);
  for(let k=0;k<12;k++) liveStep(1/60); });
capConfig('real_first',{view:'real',showAngles:true,showMolName:true});
capConfig('real_last',{view:'real',mol:MOL_LIST[MOL_LIST.length-1],showAngles:true,showOuterLP:true,showMolName:true,showElName:true});
if(LPS){
  capConfig('real_sf4_model',{view:'real',mol:'SF4',realMode:'model',_blend:1,showAngles:true,showOuterLP:true,showMolName:true,showElName:true});
  capConfig('real_sf4_real',{view:'real',mol:'SF4',showAngles:true});
  capConfig('real_xef4_blend',{view:'real',mol:'XeF4',_blend:0.5,showOuterLP:true});
  capConfig('real_co2',{view:'real',mol:'CO2',showAngles:true,showOuterLP:true});
}
capConfig('real_pcl5',{view:'real',mol:'PCl5',showAngles:true});
capConfig('table',{view:'table'});
capConfig('table_rho1',{view:'table',rho:1,camTheta:-0.4,camPhi:0.6});
if(LPS){ capConfig('squeeze',{view:'squeeze'}); capConfig('squeeze_083',{view:'squeeze',rho:0.83}); }
capConfig('relax_stuck',{view:'relax',_load:[4,LPS?2:0],_seed:2,_run:'all'});
capConfig('relax_mid',{view:'relax',_load:[6,0],_seed:1,_run:30});
capConfig('relax_empty',{view:'relax',_load:[1,0]});
ObjC.import('Foundation');
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson).writeToFileAtomicallyEncodingError('display.json',true,$.NSUTF8StringEncoding,$());
console.log('wrote display.json, '+capJson.length+' bytes');
