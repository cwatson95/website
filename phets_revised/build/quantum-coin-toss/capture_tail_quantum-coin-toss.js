/* capture_tail_quantum-coin-toss.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_quantum-coin-toss.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(v,over){
  const clean={view:v}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean); resetScenes();
  if(isCoinView(v)){ const sc=sceneOf(v); if(over._p!==undefined) sc.p=over._p; if(over._n) setCoinCount(sc,over._n);
    if(over._start) sceneStart(sc);
    if(over._flip){ coinPrepare(sc,sc.single,!!over._rev); coinPrepare(sc,sc.set,!!over._rev); coinStep(sc,sc.single,over._flip); coinStep(sc,sc.set,over._flip); }
    if(over._obs){ coinReveal(sc,sc.single); coinReveal(sc,sc.set); }
    if(over._hist) for(let i=0;i<over._hist;i++){ coinPrepare(sc,sc.single,true); coinStep(sc,sc.single,1); } }
}
const CAP_SCENES=[
  ['classical_prepare',{}],
  ['classical_counted',{_start:1,_flip:1,_rev:1,_hist:25}],
  ['classical_flipping',{_start:1,_n:10,_flip:0.62}],
  ['classical_10000',{_start:1,_n:10000,_p:0.8,_flip:1,_rev:1}],
  ['quantum_prepare',{_p:0.25}],
  ['quantum_ready',{_start:1,_p:0.6}],
  ['quantum_observed',{_start:1,_p:0.6,_obs:1,_hist:30}],
  ['quantum_certain',{_start:1,_p:1,_n:10,_obs:1}],
  ['binom_default',{}],
  ['binom_10000',{binN:10000,binP:0.35}],
  ['binom_10',{binN:10,binP:0.65,binM:3000,binSeed:73}],
  ['mix_default',{}],
  ['mix_half',{mixP:0.5,mixShots:2000,mixSeed:21}],
  ['mix_certain',{mixP:1,mixShots:500,mixSeed:9}],
  ['mix_low',{mixP:0.15,mixShots:1500,mixSeed:3}],
];
const CAP_NARROW=[['classical_counted',CAP_SCENES[1][1]],['quantum_observed',CAP_SCENES[6][1]],['binom_10000',CAP_SCENES[9][1]],['mix_default',{}]];
function capWrite(file,W,H,list){
  const out={W,H,views:{}};
  for(const [name,over] of list){
    const v=name.split('_')[0];
    capState(v,over);
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
capWrite('display_narrow.json',820,520,CAP_NARROW);
capState('classical',{});
