
/* ================================================================== *
 *  state, the per-view model, readout, eqbar, tag                     *
 * ================================================================== */
const TABS=[['bench','the bench'],['sys','the systems'],['ledger','the heat ledger'],['flow','the energy flow'],['eq','equilibrium']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a', text:'#aeb6c6',
           form:{mechanical:'#a7b0c2', electrical:'#3d7bff', thermal:'#ff5a4a', light:'#f4d03f', chemical:'#46c46a'},
           body:{iron:'#8e96a6', brick:'#8f3b2e', water:'#6cc3dc', oil:'#d9b53a'},
           acct:{bodies:'#b8ec4c', room:'#5ac8e0', work:'#e8843a', resid:'#cd35c4'}};
const FORMS=['mechanical','electrical','thermal','light','chemical'];
const RO_W=300;
const SPEED_LIST=[{id:'normal',name:'normal'},{id:'fast',name:'fast ×4'}];

/* PhET's defaults, except where the header says otherwise: energy symbols
   shown, and the Systems screen opening on the faucet running */
const DEFAULTS={view:'bench', running:true, speed:'normal', symBench:true, symSys:true, link:false, lev0:0, lev1:0, preset:'start',
                src:'faucet', conv:'generator', user:'heater', pedal:0, flow:0.7, clouds:0, heat:0,
                eqPair:'iron-water', eqT1:380, eqT2:296, eqMat:'phet', eqAir:true};
const ST=Object.assign({},DEFAULTS);
sysReset(SYS,ST);

function kelvinC(T){ return T-273.15; }
function fmtT(T){ return fmt(kelvinC(T),1)+' °C'; }
function fmtJ(E){ const a=Math.abs(E); return a>=1e6?sigf(E/1e6,4)+' MJ':(a>=1e3?sigf(E/1e3,4)+' kJ':sigf(E,3)+' J'); }
function fmtW(P){ const a=Math.abs(P); return a>=1e3?sigf(P/1e3,3)+' kW':(a<0.5?'0 W':sigf(P,3)+' W'); }
function resid(r){ return r===0?'0 J':sigf(r,2)+' J'; }

/* the model carries a SNAPSHOT of the state, so a readout rendered later
   cannot read whatever state ran last (Known-bad) */
function buildModel(){
  const st=Object.assign({},ST), view=st.view, M={view,st};
  if(view==='bench'||view==='ledger'){
    const B=BENCH, lev=burnerLevels(st);
    M.B=B; M.lev=lev; M.t=B.t;
    M.T=B.bodies.map(bodyT); M.E=B.bodies.map(b=>b.E); M.own=B.own.slice(); M.g=B.bodies.map(b=>gChunks(b.E));
    M.dE=B.bodies.reduce((s,b,i)=>s+b.E-B.E0[i],0);
    M.resid=M.dE+B.room-B.work;
    M.onBurner=[0,1].map(k=>B.bodies.findIndex(b=>burnerContact(k,b)));
    /* nominal: 5000 x level W into a body on the burner (PhET stops cooling at 0 C), 1500 x level W into the room */
    M.power=[0,1].map(k=>M.onBurner[k]>=0?P_BURN*lev[k]:P_BURN_AIR*lev[k]);
    M.imm=B.bodies.map(b=>isImmersed(B.bodies,b));
    M.idDrift=[0,1,2,3].map(i=>benchIdentity(B,i)-benchIdentity0(B,i));
    M.therm=B.therm.map(th=>{ const p=thermoTip(B,th); return th.tray?null:Object.assign({x:p.x,y:p.y},thermoSense(B,p.x,p.y,lev)); });
  }
  if(view==='sys'||view==='flow'){
    const S=SYS;
    M.S=S; M.F=S.flows; M.bal=sysBalance(S); M.closure=sysClosure(S); M.t=S.t;
    M.waterT=Math.min(S.water/HB_C,T_BOIL.water); M.food=foodChunks(S);
    M.takes=convTakes(S.conv,S.src);
  }
  if(view==='eq'){
    const L=eqLinear(st.eqPair,st.eqT1,st.eqT2,st.eqMat,st.eqAir);
    M.win=eqWindow(L);
    M.R=memo('eqrun',[st.eqPair,st.eqT1,st.eqT2,st.eqMat,st.eqAir].join('|'),()=>eqRun(st.eqPair,st.eqT1,st.eqT2,st.eqMat,st.eqAir,M.win));
    M.L=M.R.L; M.ev=eqEigen(M.L.M);
    let dmax=0; const n=M.R.t.length;
    for(let k=0;k<n;k++){ if(M.R.tCap!==null&&M.R.t[k]>=M.R.tCap) break; dmax=Math.max(dmax,Math.abs(M.R.s1[k]-M.R.x1[k]),Math.abs(M.R.s2[k]-M.R.x2[k])); }
    M.dmax=dmax;
  }
  return M;
}
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function srcName(id){ return SOURCES.find(o=>o.id===id).name; }
function convName(id){ return CONVERTERS.find(o=>o.id===id).name; }
function userName(id){ return USERS.find(o=>o.id===id).name; }
function levText(l){ return l>0?'heat '+fmt(l,2):(l<0?'cool '+fmt(-l,2):'off'); }
function benchRows(M){
  let s=hd('the bodies · t = '+fmt(M.t,1)+' s');
  M.B.bodies.forEach((b,i)=>{ s+=rrow(MAT_NAME[b.mat]+(M.imm[i]?' (immersed)':''),fmtT(M.T[i])+' · '+M.own[i]+' chunks'); });
  s+=hd('the burners');
  for(let k=0;k<2;k++){
    const on=M.onBurner[k], what=on>=0?'into the '+MAT_NAME[M.B.bodies[on].mat]:'into the room';
    s+=rrow((k?'right':'left')+', '+levText(M.lev[k]),fmtW(M.power[k])+' '+what);
  }
  return s;
}
function benchLedgerRows(M){
  const B=M.B;
  return hd('the ledger since the start')+rrow('the burners did',fmtJ(B.work))+rrow('the bodies gained',fmtJ(M.dE))
    +rrow('the room took',fmtJ(B.room))+rrow('gained + took &minus; did',resid(M.resid),Math.abs(M.resid)<=1e-9*Math.max(1,Math.abs(B.work)+Math.abs(B.room)+1e5)?'good':'bad');
}
function readoutHTML(M){
  const st=M.st;
  let s='<div class="rname">energy forms and changes<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='bench'){
    s+=benchRows(M)+benchLedgerRows(M);
    const th=M.therm.filter(x=>x);
    if(th.length) s+=hd('thermometers')+th.map((x,k)=>rrow('#'+(k+1)+' in the '+thermoWhat(M,x.what),fmtT(x.T))).join('');
    s+='</table><div class="note">One chunk is PhET&rsquo;s ENERGY_PER_CHUNK, '+fmt(EPC,1)+' J; a body holds the count PhET&rsquo;s map gives its energy, give or take one in transit. '
      +'The room is an infinite bath at 296 K.</div>';
    return s;
  }
  if(M.view==='ledger'){
    s+=benchLedgerRows(M);
    const B=M.B;
    s+=hd('where the burners&rsquo; work went')+rrow('left burner',fmtJ(B.workK[0]))+rrow('right burner',fmtJ(B.workK[1]))+rrow('&hellip; straight into the room',fmtJ(B.workAir));
    s+=hd('the chunk identity, each body')+M.B.bodies.map((b,i)=>rrow(MAT_NAME[b.mat]+': '+M.own[i]+' vs g = '+fmt(M.g[i],2),'drift '+resid(M.idDrift[i]),Math.abs(M.idDrift[i])<1e-6?'good':'bad')).join('');
    s+=hd('moved so far')+rrow('chunks between bodies',String(B.moved.pair))+rrow('to and from burners',String(B.moved.burner))+rrow('to and from the room',String(B.moved.air));
    s+='</table><div class="note">E + (energy still in transit on a body&rsquo;s links) &minus; '+fmt(EPC,1)+' J &times; chunks never changes: the chunks are the ledger, quantised.</div>';
    return s;
  }
  if(M.view==='sys'||M.view==='flow'){
    const S=M.S, F=M.F, b=M.bal;
    s+=hd('the source: '+srcName(S.src))+rrow('supply',fmtW(F.srcIn))+rrow('to the '+convName(S.conv),fmtW(F.srcOut));
    if(S.src==='biker') s+=rrow('food left',M.food+' chunks ('+fmtJ(S.food)+')',M.food>0?'':'bad');
    if(S.src==='faucet') s+=rrow('water falling',fmtJ(S.fall.reduce((a,c)=>a+c,0)));
    if(S.src==='teapot') s+=rrow('held in the kettle',fmtJ(S.kettle));
    if(S.src==='sun') s+=rrow('the clouds send back',fmtW(F.refl));
    s+=hd('the converter: '+convName(S.conv));
    if(!M.takes) s+=rrow('it cannot use '+srcForm(S.src),'all of it misses','bad');
    else s+=rrow('electrical out',fmtW(F.cOut))+rrow('lost as heat',fmtW(F.cLoss))+(S.conv==='generator'&&S.src!=='biker'?rrow('in the wheel',fmtJ(S.wheel)):'');
    s+=hd('the user: '+userName(S.user))+rrow('electrical in',fmtW(F.uIn));
    if(S.user==='heater') s+=rrow('into the water',fmtW(F.water))+rrow('water',fmtT(M.waterT));
    else if(S.user==='fan') s+=rrow('wind',fmtW(F.wind))+rrow('blade',sigf(S.fan,3)+' rad/s');
    else s+=rrow('light',fmtW(F.light))+rrow('brightness',fmt(S.lit,2));
    s+=hd('the ledger since the start ('+fmt(M.t,1)+' s)')+rrow('in',fmtJ(b.IN))+rrow('out (light, wind)',fmtJ(b.OUT))+rrow('lost (heat, missed)',fmtJ(b.LOST))
      +rrow('stored now',fmtJ(b.STORED))+rrow('in &minus; out &minus; lost &minus; stored',resid(b.resid),Math.abs(b.resid)<1e-6*Math.max(1,b.IN)?'good':'bad');
    s+='</table><div class="note">Every element: in = out + losses + the change in its store, every step. PhET&rsquo;s rates; where PhET&rsquo;s own numbers do not close, the header says how this does.</div>';
    return s;
  }
  const L=M.L, P=eqPair(st.eqPair), n1=MAT_NAME[BODY_DEF[P.b1][0]], n2=MAT_NAME[BODY_DEF[P.b2][0]];
  s+=hd(P.name+', '+(st.eqMat==='real'?'real materials':'PhET&rsquo;s materials'))
    +rrow('C '+n1+', '+n2,sigf(L.C1,4)+', '+sigf(L.C2,4)+' J/K')+rrow('contact conductance kL',sigf(L.G,4)+' W/K')
    +rrow('T<sub>eq</sub> = (C<sub>1</sub>T<sub>1</sub> + C<sub>2</sub>T<sub>2</sub>)/(C<sub>1</sub> + C<sub>2</sub>)',fmtT(L.Teq)+' ('+fmt(L.Teq,2)+' K)','good')
    +rrow('&tau; = 1/[kL(1/C<sub>1</sub> + 1/C<sub>2</sub>)]',sigf(L.tau,4)+' s');
  s+=hd(st.eqAir?'with the room':'insulated')+rrow('to the room, '+n1+', '+n2,sigf(L.a1,3)+', '+sigf(L.a2,3)+' W/K')
    +rrow('rates',sigf(-M.ev[0],3)+', '+sigf(-M.ev[1],3)+' per s');
  s+=hd('PhET&rsquo;s steps against the exact solution')+rrow('largest gap',sigf(M.dmax*1000,3)+' mK')
    +rrow('a cap reached',M.R.tCap===null?'no':'at '+fmt(M.R.tCap,2)+' s',M.R.tCap===null?'':'bad')+rrow('ledger residual',resid(M.R.resid),Math.abs(M.R.resid)<1e-8?'good':'bad');
  s+='</table><div class="note">PhET&rsquo;s explicit step of 1/60 s lags the exact exponential by O(&Delta;t): the gap is the price of the step, not a bug. '
    +'Real materials: NIST water and iron, handbook brick and olive oil (see the source line).</div>';
  return s;
}
function thermoWhat(M,w){
  if(typeof w==='number') return MAT_NAME[M.B.bodies[w].mat];
  if(w==='air') return 'room';
  if(w.slice(0,5)==='steam') return 'steam';
  return (w==='burner0'?'left':'right')+' burner';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='bench') return E('<span class="hl">dQ/dt = k L (T<sub>b</sub> &minus; T<sub>a</sub>)</span> &nbsp;&middot;&nbsp; k = 1000 W/(m&middot;K) between bodies, 30 W/(m&middot;K) to the room &nbsp;&middot;&nbsp; E = mcT',
    'heat flows down the temperature difference, in proportion to the length of contact: PhET&rsquo;s model, stepped 60 times a second');
  if(M.view==='sys') return E('<span class="hl">E<sub>in</sub> = E<sub>out</sub> + E<sub>lost</sub> + &Delta;E<sub>stored</sub></span> &nbsp;&middot;&nbsp; <span class="rm">for the source, the converter and the user, every step</span>',
    'energy changes form at each element and some of it leaves as heat; none of it appears or vanishes');
  if(M.view==='ledger') return E('<span class="hl">&Delta;E<sub>bodies</sub> + E<sub>room</sub> = W<sub>burners</sub></span> &nbsp;&middot;&nbsp; EPC &times; &Delta;chunks = &Delta;E + E<sub>in transit</sub>',
    'the first law for the bench: what the burners do is what the bodies gained plus what the room took');
  if(M.view==='flow') return E('<span class="hl">IN = OUT + LOST + STORED</span> &nbsp;&middot;&nbsp; <span class="rm">efficiency of the chain</span> = OUT/IN',
    'the Sankey diagram draws every flow to scale: the widths at each element add up');
  return E('<span class="hl">T<sub>eq</sub> = (C<sub>1</sub>T<sub>1</sub> + C<sub>2</sub>T<sub>2</sub>)/(C<sub>1</sub> + C<sub>2</sub>)</span> &nbsp;&middot;&nbsp; T<sub>1</sub> &minus; T<sub>2</sub> &prop; e<sup>&minus;t/&tau;</sup>, &nbsp; &tau; = 1/[kL(1/C<sub>1</sub> + 1/C<sub>2</sub>)]',
    'two bodies in contact end at the heat-capacity-weighted mean, approached exponentially; the room then pulls both to 296 K');
}
function tagHTML(M){
  const st=M.st;
  if(M.view==='bench') return '<b>the bench</b> — t = '+fmt(M.t,1)+' s'+(st.running?'':', paused')+(st.speed==='fast'?', ×4':'');
  if(M.view==='ledger') return '<b>the heat ledger</b> — the bench, since its start';
  if(M.view==='sys') return '<b>the systems</b> — '+srcName(st.src)+' → '+convName(st.conv)+' → '+userName(st.user)+(st.running?'':', paused');
  if(M.view==='flow') return '<b>the energy flow</b> — '+srcName(st.src)+' → '+convName(st.conv)+' → '+userName(st.user);
  return '<b>equilibrium</b> — '+eqPair(st.eqPair).name+(st.eqAir?'':', insulated');
}
