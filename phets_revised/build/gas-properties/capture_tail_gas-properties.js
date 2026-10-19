/* capture_tail_gas-properties.js — display-list capture for gas-properties.html.
 * cat _out/run.js <sims>/tools/recorder.js capture_tail_gas-properties.js > _out/cap_run.js
 * cd _out && osascript -l JavaScript cap_run.js > cap.log     (never through head/tail)
 * CAP_W/CAP_H may be set before this tail to capture another size. */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const outCap={W:CAPW,H:CAPH,views:{}};
const PICK=['ideal default','ideal crowded','ideal lid open','ideal hold P V','ideal oops','ideal narrow wall',
            'explore squeezed','explore pulled','energy default','energy no collisions','energy empty',
            'diffusion default','diffusion mixing','diffusion big','pressure default','pressure no collisions','pressure dense',
            'equil delta','equil split','equil pump fresh','equil no collisions'];
for(const [nm,over,fn] of CONFIGS){
  if(PICK.indexOf(nm)<0) continue;
  setupConfig(over,fn);
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  const key=nm.replace(/ /g,'_');
  outCap.views[key]=rc.ops;
  console.log(key+': '+rc.ops.length+' ops');
}
ObjC.import('Foundation');
const jsonCap=JSON.stringify(outCap);
$.NSString.alloc.initWithUTF8String(jsonCap)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+jsonCap.length+' bytes');
