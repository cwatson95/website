
/* ================================================================== *
 *  state: the tabs, PhET's defaults, the two coin scenes, the model   *
 * ================================================================== */
const TABS=[['classical','the classical coin'],['quantum','the quantum coin'],['binom','the binomial'],['mix','the hidden difference']];
const SIM_NAME='quantum coin toss';
/* PhET's Coins screen: the classical scene first, each scene with its own
   state (heads up at bias 0.5; the quantum coin at 0.5, a superposition);
   the analysis views' settings are the remake's */
const DEFAULTS={view:'classical', binN:100, binP:0.5, binM:1000, binSeed:5, mixP:0.7, mixShots:1000, mixSeed:7};
const ST=Object.assign({},DEFAULTS);
const SEEDS={classical:101, quantum:202};
let COINS;
function resetScenes(){ COINS={classical:makeCoinScene('classical',SEEDS.classical), quantum:makeCoinScene('quantum',SEEDS.quantum)}; }
resetScenes();
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
let T_NOW=0;
function sceneOf(v){ return v==='quantum'?COINS.quantum:COINS.classical; }
function isCoinView(v){ return v==='classical'||v==='quantum'; }
function buildModel(){
  const st=Object.assign({},ST), v=st.view, M={view:v, st, tNow:T_NOW};
  if(isCoinView(v)) M.C=coinsModel(sceneOf(v));
  else if(v==='binom') M.N=binomModel(st);
  else M.X=mixModel(st);
  return M;
}
function readoutHTML(M){
  const name=TABS.find(t=>t[0]===M.view)[1];
  const body=isCoinView(M.view)?coinsReadout(M):(M.view==='binom'?binomReadout(M):mixReadout(M));
  return '<div class="rname">'+SIM_NAME+'<small>'+name+'</small></div><table>'+body+'</table>'
    +'<div class="note">PhET&rsquo;s values are from its build 1.0.4; the Born rule and the binomial are exact, and every seeded count is '
    +'pinned bit for bit to the Python twins.</div>';
}
function eqbarHTML(M){
  const e=isCoinView(M.view)?coinsEq(M):(M.view==='binom'?binomEq(M):mixEq(M));
  return '<span class="lhs">'+e[0]+'</span><span class="sm">'+e[1]+'</span>';
}
function tagHTML(M){ return isCoinView(M.view)?coinsTag(M):(M.view==='binom'?binomTag(M):mixTag(M)); }
