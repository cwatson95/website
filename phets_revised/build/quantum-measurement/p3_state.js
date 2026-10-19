
/* ================================================================== *
 *  state: the tabs, PhET's defaults, the live scenes, the model       *
 * ================================================================== */
const TABS=[['coins','the coins'],['photons','the photons'],['spins','the spins'],
            ['bloch','the Bloch sphere'],['born','the Born rule'],['binom','the binomial']];
const SIM_NAME='quantum measurement';
/* PhET's defaults where PhET has them: the classical coin scene first, one
   photon at a time polarized at 45 deg (classical behaviour), experiment 1
   with a +Z source and single particles, +X on the Bloch sphere measured
   along z with no field (strength 1, delay 0.75 ns when it is on).  House
   choices: a 60/s beam (PhET starts at 0), the analysis views' settings. */
const DEFAULTS={view:'coins', coinScene:'classical', running:true, speed:'normal',
  phMode:'single', phPreset:'fortyFive', phCustom:45, phBehavior:'classical', phRate:60,
  sgExp:'e1', sgMode:'single', sgSrc:'+Z', sgA2:1, sgAmount:0.1, sgBlock:'up', sgC1:'x', sgC2:'z', sgExpect:true,
  bTheta:Math.PI/2, bPhi:0, bPreset:'+X', bAxis:'Z', bAtoms:1, bField:false, bStrength:1, bDelay:BL.DELAY, bBasis:'Z', bGlobal:false,
  bornTh:60, bornAlpha:45, bornN:8, bornShots:2000, bornSeed:61,
  binN:100, binP:0.5, binM:1000, binSeed:5};
const ST=Object.assign({},DEFAULTS);
/* the live experiments: two coin scenes, two photon scenes (PhET keeps them
   separate too), the Stern-Gerlach bench and the Bloch-sphere bench, each
   with its own seeded stream so a reset reproduces the same draws */
const SEEDS={classical:101, quantum:202, single:303, many:404, sg:505, bloch:606};
let COINS, PHOT, SGS, BLO;
function resetScenes(){
  COINS={classical:makeCoinScene('classical',SEEDS.classical), quantum:makeCoinScene('quantum',SEEDS.quantum)};
  PHOT={single:makePhotonScene('single',SEEDS.single), many:makePhotonScene('many',SEEDS.many)};
  SGS=makeSgScene(SEEDS.sg);
  BLO=makeBlochScene(SEEDS.bloch); blochReprepare(BLO,ST);
}
resetScenes();
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function simFactor(st){ return st.speed==='slow'?PH.SLOW:1; }
/* readout helpers */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
let CAM={theta:CAM_HOME.theta, phi:CAM_HOME.phi};
let T_NOW=0;                     /* a frame clock for the flip animation */
/* the model: a snapshot of the live view, built fresh for every drawing */
function buildModel(){
  const st=Object.assign({},ST), v=st.view, M={view:v, st, tNow:T_NOW};
  if(v==='coins') M.C=coinsModel(COINS[st.coinScene]);
  else if(v==='photons') M.P=photonsModel(st);
  else if(v==='spins') M.S=spinsModel(st);
  else if(v==='bloch') M.B=blochModel(st,CAM);
  else if(v==='born') M.O=bornModel(st);
  else M.N=binomModel(st);
  return M;
}
function readoutHTML(M){
  const name=TABS.find(t=>t[0]===M.view)[1];
  let body='';
  if(M.view==='coins') body=coinsReadout(M);
  else if(M.view==='photons') body=photonsReadout(M);
  else if(M.view==='spins') body=spinsReadout(M);
  else if(M.view==='bloch') body=blochReadout(M);
  else if(M.view==='born') body=bornReadout(M);
  else body=binomReadout(M);
  return '<div class="rname">'+SIM_NAME+'<small>'+name+'</small></div><table>'+body+'</table>'
    +'<div class="note">PhET&rsquo;s values are from its build 1.0.5; the Born rule, the projections, the precession and the binomial are exact, '
    +'and every seeded count is pinned bit for bit to derive.py.</div>';
}
function eqbarHTML(M){
  const f={coins:coinsEq,photons:photonsEq,spins:spinsEq,bloch:blochEq,born:bornEq,binom:binomEq}[M.view];
  const e=f(M);
  return '<span class="lhs">'+e[0]+'</span><span class="sm">'+e[1]+'</span>';
}
function tagHTML(M){ return {coins:coinsTag,photons:photonsTag,spins:spinsTag,bloch:blochTag,born:bornTag,binom:binomTag}[M.view](M); }
