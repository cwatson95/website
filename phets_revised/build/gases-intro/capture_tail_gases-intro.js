/* capture_tail_gases-intro.js — display-list capture for gases-intro.html.
 * cat _out/run.js <sims>/tools/recorder.js capture_tail_gases-intro.js > _out/cap_run.js
 * cd _out && osascript -l JavaScript cap_run.js > cap.log     (never through head/tail:
 * a closed pipe kills osascript before it writes display.json and the next
 * audit silently reports the STALE file)
 * CAP_W/CAP_H may be set before this tail to capture another size. */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const outCap={W:CAPW,H:CAPH,views:{}};
const PICK=['intro default','intro empty','intro crowded','intro lid open','intro narrow',
            'laws nothing','laws hold V heating','laws hold P V','laws hold T','laws oops',
            'pv default','pv squeezed at T','pv empty',
            'sweep idle','sweep boyle','sweep charles','sweep gay','sweep avogadro','sweep part way'];
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
