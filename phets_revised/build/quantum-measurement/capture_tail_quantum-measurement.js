/* capture_tail_quantum-measurement.js — display-list capture.
 *   cat _out/run.js <sims>/tools/recorder.js capture_tail_quantum-measurement.js > _out/cap_run.js
 *   (cd _out && osascript -l JavaScript cap_run.js > cap.log)     never through head/tail
 * Writes _out/display.json (1400 x 820) and _out/display_narrow.json (820 x 520).
 * No helper here is named run, sig or makeRecorder (Known-bad collisions). */
function capState(v,over){
  const clean={view:v}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean); resetScenes(); resetCam();
  if(v==='coins'){ const sc=COINS[ST.coinScene]; if(over._p!==undefined) sc.p=over._p; if(over._n) setCoinCount(sc,over._n);
    if(over._start) sceneStart(sc);
    if(over._flip){ coinPrepare(sc,sc.single,!!over._rev); coinPrepare(sc,sc.set,!!over._rev); coinStep(sc,sc.single,over._flip); coinStep(sc,sc.set,over._flip); }
    if(over._obs){ coinReveal(sc,sc.single); coinReveal(sc,sc.set); }
    if(over._hist){ for(let i=0;i<over._hist;i++){ coinPrepare(sc,sc.single,true); coinStep(sc,sc.single,1); } } }
  if(v==='photons'){ const ps=PHOT[ST.phMode];
    if(over._n1) for(let i=0;i<over._n1;i++){ photonEmit(ps,ST,0); for(let f=0;f<75;f++) photonAdvance(ps,ST,1/60); }
    if(over._fly){ photonEmit(ps,ST,0); photonAdvance(ps,ST,over._fly); }
    if(over._run) for(let f=0;f<over._run;f++) photonAdvance(ps,ST,1/60); }
  if(v==='spins'){
    if(over._n1) for(let i=0;i<over._n1;i++){ sgShoot(SGS,ST); for(let f=0;f<240;f++) sgAdvance(SGS,ST,1/60); }
    if(over._fly){ sgShoot(SGS,ST); sgAdvance(SGS,ST,over._fly); }
    if(over._run) for(let f=0;f<over._run;f++) sgAdvance(SGS,ST,1/60); }
  if(v==='bloch'){ blochReprepare(BLO,ST);
    if(over._cam){ CAM.theta=over._cam[0]; CAM.phi=over._cam[1]; }
    if(over._rounds) for(let i=0;i<over._rounds;i++){ blochReprepare(BLO,ST); blochButton(BLO,ST); blochAdvance(BLO,ST,5); }
    if(over._time!==undefined){ blochReprepare(BLO,ST); blochButton(BLO,ST); blochAdvance(BLO,ST,over._time); } }
}
const CAP_SCENES=[
  ['coins_prepare',{}],
  ['coins_classical_counted',{_start:1,_flip:1,_rev:1,_hist:30}],
  ['coins_classical_flipping',{_start:1,_flip:0.37}],
  ['coins_classical_hidden10',{_n:10,_start:1,_flip:1}],
  ['coins_quantum_ready',{coinScene:'quantum',_p:0.7,_start:1}],
  ['coins_quantum_10000',{coinScene:'quantum',_p:0.3,_n:10000,_start:1,_obs:1,_hist:40}],
  ['coins_quantum_prepare',{coinScene:'quantum',_p:0.85}],
  ['photons_single',{phPreset:'custom',phCustom:30,_n1:12,_fly:0.3}],
  ['photons_quantum_split',{phBehavior:'quantum',phPreset:'custom',phCustom:60,_n1:5,_fly:0.85}],
  ['photons_beam',{phMode:'many',phRate:120,_run:240}],
  ['photons_unpolarized',{phMode:'many',phPreset:'unpolarized',phRate:60,_run:200}],
  ['spins_e1_flight',{_fly:0.8}],
  ['spins_e3_single',{sgExp:'e3',sgSrc:'+X',_n1:3,_fly:1.9}],
  ['spins_e5_beam',{sgExp:'e5',sgMode:'continuous',_run:300}],
  ['spins_e4_blockdown',{sgExp:'e4',sgMode:'continuous',sgBlock:'down',sgSrc:'+X',_run:300}],
  ['spins_custom',{sgExp:'custom',sgA2:0.3,sgMode:'continuous',_run:200}],
  ['bloch_default',{}],
  ['bloch_timing',{bField:true,_time:1.7}],
  ['bloch_observedY',{bField:true,bAxis:'Y',_rounds:12}],
  ['bloch_ten',{bAtoms:10,bTheta:Math.PI/3,bPhi:Math.PI/4,bAxis:'X',_rounds:5,bBasis:'X'}],
  ['bloch_turned',{bTheta:2*Math.PI/3,bPhi:5*Math.PI/4,bBasis:'Y',bGlobal:true,_cam:[1.6,0.8]}],
  ['born_default',{}],
  ['born_edges',{bornTh:180,bornAlpha:90,bornN:2,bornShots:500,bornSeed:9}],
  ['binom_default',{}],
  ['binom_10000',{binN:10000,binP:0.35}],
  ['binom_p1',{binP:1,binN:10}],
];
const CAP_NARROW=[['coins_quantum_10000',CAP_SCENES[5][1]],['photons_quantum_split',CAP_SCENES[8][1]],['spins_e5_beam',CAP_SCENES[13][1]],
                  ['bloch_ten',CAP_SCENES[19][1]],['born_default',{}],['binom_10000',CAP_SCENES[24][1]]];
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
capState('coins',{});
