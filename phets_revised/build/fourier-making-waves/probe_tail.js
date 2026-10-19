/* a throwaway probe: print the op counts each configuration emits, so the
   "draws substance" floors in selfTest are measured rather than guessed.
   Appended to _out/run.js by hand; never part of the shipped file. */
const PCONF=[
  ['harmonics sine square',{view:'harm',preset:'square',series:'sin',N:11}],
  ['harmonics cosine triangle',{view:'harm',preset:'triangle',series:'cos',N:7,showInf:true}],
  ['harmonics sawtooth, time',{view:'harm',preset:'sawtooth',domain:'time',N:11,caliper:true,sel:3}],
  ['harmonics space & time',{view:'harm',preset:'square',domain:'both',t:0.7,N:5}],
  ['harmonics one harmonic',{view:'harm',preset:'sinusoid',N:1,showHarm:false}],
  ['harmonics all zero',{view:'harm',preset:'custom',_amps:new Array(NMAX).fill(0)}],
  ['harmonics wave packet',{view:'harm',preset:'wavePacket',N:11,showInf:true}],
  ['convergence square M=6',{view:'conv',convPre:'square',convM:6}],
  ['convergence square M=1',{view:'conv',convPre:'square',convM:1}],
  ['convergence square M=128',{view:'conv',convPre:'square',convM:128}],
  ['convergence triangle',{view:'conv',convPre:'triangle',series:'cos',convM:9}],
  ['convergence sawtooth',{view:'conv',convPre:'sawtooth',convM:20}],
  ['convergence sinusoid',{view:'conv',convPre:'sinusoid',convM:3}],
  ['spectrum square',{view:'spec',preset:'square',N:11}],
  ['spectrum single sine',{view:'spec',preset:'sinusoid',N:11}],
  ['spectrum all zero',{view:'spec',preset:'custom',_amps:new Array(NMAX).fill(0)}],
  ['game level 1',{view:'game',level:1,seed:3,_game:1}],
  ['game level 5 solved',{view:'game',level:5,seed:9,_game:1,showAns:true}],
  ['packet default',{view:'pack'}],
  ['packet continuous',{view:'pack',wpSp:0}],
  ['packet narrow spacing',{view:'pack',wpSp:1,wpSk:WP_SK_MAX,wpK0:WP_K0_MAX}],
  ['packet widest packet',{view:'pack',wpSp:3,wpSk:WP_SK_MIN,wpK0:WP_K0_MIN,wpEnv:false,wpWid:false}],
  ['packet in time',{view:'pack',wpDom:'time'}],
  ['transform pair default',{view:'pair'}],
  ['transform pair coarse',{view:'pair',pairK1:PAIR_K1_MAX,pairSk:WP_SK_MIN}],
  ['transform pair fine',{view:'pair',pairK1:PAIR_K1_MIN,pairSk:WP_SK_MAX}],
];
for(const [nm,over] of PCONF){
  const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
  Object.assign(ST,DEFAULTS,clean);
  if(over._amps) setAmps(over._amps); else applyPreset();
  if(over._game){ GAME.level=ST.level; GAME.seed=ST.seed;
    GAME.answer=gameAmplitudes(GAME.level,gameSeedOf(GAME.level,GAME.seed));
    setGuess(over.showAns?GAME.answer.slice():new Array(NMAX).fill(0)); }
  const line=[];
  for(const [W,H] of [[1400,820],[1100,700],[860,560]]){
    const c=makeShot(W,H);
    try{ drawView(c,W,H,buildModel()); }catch(e){ line.push('ERR '+e); continue; }
    line.push(c.ops.filter(o=>o.op==='fill').length+'f/'+c.ops.filter(o=>o.op==='stroke').length+'s/'+c.ops.filter(o=>o.op==='text').length+'t');
  }
  console.log(('                                        '+nm).slice(-38)+'  '+line.join('   '));
}
