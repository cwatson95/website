/* ============ display-list capture for molecule-polarity.html ============== *
 * cat _out/run.js tools/recorder.js capture_tail_molecule-polarity.js > cap_run.js
 * osascript -l JavaScript cap_run.js > cap.log   (never through head: Known-bad)
 * Writes display.json in the working directory.  No helper is named `run`
 * (JXA calls a top-level run() with argv: Known-bad).                        */
const CAP_W=1400, CAP_H=820;
const capOut={W:CAP_W,H:CAP_H,views:{}};
function capConfig(name,over,prep){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  fieldReset();
  for(const k in MEMO) delete MEMO[k];
  if(over._psi!==undefined) setFieldPsi(over._psi*Math.PI/180);
  if(over._angle!==undefined) setBondAngleDeg(over._angle);
  if(over._settle){ let n=0; while(!FIELD.idle&&n<over._settle){ fieldStep(1/60); n++; } }
  if(over._frames) for(let k=0;k<over._frames;k++) fieldStep(1/60);
  if(prep) prep();
  const rc=makeRecorder(CAP_W,CAP_H);
  drawView(rc,CAP_W,CAP_H,buildModel());
  capOut.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
capConfig('two_default',{view:'two'});
capConfig('two_potential_max',{view:'two',enA:2,enB:4,surface:'potential',showCharges:true});
capConfig('two_density',{view:'two',enA:4,enB:2,surface:'density',showCharges:true});
capConfig('two_zero',{view:'two',enA:3,enB:3,surface:'potential',showCharges:true,showBondChar:true});
capConfig('two_rainbow',{view:'two',enA:2,enB:3.2,surface:'potential',surfColor:'roygb',showCharges:true});
capConfig('two_field_turning',{view:'two',enA:2,enB:4,field:true,showCharges:true,_psi:150,_frames:40});
capConfig('two_field_aligned',{view:'two',enA:2,enB:3.4,field:true,_psi:150,_settle:20000});
capConfig('two_reversed',{view:'two',enA:2,enB:3.6,dipoleDir:'negpos',showCharges:true,surface:'potential'});
capConfig('three_default',{view:'three',showCharges:true});
capConfig('three_linear',{view:'three',enA:2,enB:3.4,enC:2,showCharges:true,_angle:180});
capConfig('three_bent',{view:'three',enA:2,enB:3.4,enC:2,showCharges:true,_angle:104.5});
capConfig('three_asym',{view:'three',enA:2,enB:3.4,enC:2.6,showCharges:true,_angle:120});
capConfig('three_field',{view:'three',enA:2,enB:4,enC:2,field:true,_angle:104.5,_psi:120,_frames:30});
capConfig('real_water_basic',{view:'real',mol:'H2O',realMode:'basic'});
capConfig('real_water_adv',{view:'real',mol:'H2O',realMode:'advanced',showCharges:true});
capConfig('real_co2',{view:'real',mol:'CO2',realMode:'advanced',showCharges:true});
capConfig('real_ammonia',{view:'real',mol:'NH3',realMode:'advanced',showCharges:true});
capConfig('real_borane',{view:'real',mol:'BH3',realMode:'advanced',showCharges:true});
capConfig('real_chloroform',{view:'real',mol:'CHCl3',realMode:'advanced',showCharges:true});
capConfig('real_hcn',{view:'real',mol:'HCN',realMode:'advanced',showCharges:true});
capConfig('real_cf4_basic',{view:'real',mol:'CF4',realMode:'basic'});
capConfig('sum_symmetric',{view:'sum',enA:2,enB:3.4,enC:2,_angle:120});
capConfig('sum_linear',{view:'sum',enA:2,enB:3.4,enC:2,_angle:180});
capConfig('sum_asym',{view:'sum',enA:2,enB:3.4,enC:2.6,_angle:95});
capConfig('sum_flat',{view:'sum',enA:3,enB:3,enC:3,_angle:120});
capConfig('field_default',{view:'field'});
capConfig('field_under',{view:'field',zeta:0.2,psi0:150});
capConfig('field_over',{view:'field',zeta:2.6,psi0:-150,enB:4});
capConfig('field_nodipole',{view:'field',enA:3,enB:3,enC:3});
capConfig('atlas',{view:'atlas'});
ObjC.import('Foundation');
const capJson=JSON.stringify(capOut);
$.NSString.alloc.initWithUTF8String(capJson).writeToFileAtomicallyEncodingError('display.json',true,$.NSUTF8StringEncoding,$());
console.log('wrote display.json, '+capJson.length+' bytes');
