
/* ================================================================== *
 *  selfTest — headless verification (runs when there is no document). *
 *  (derive) marks build/quantum-measurement/refvals.txt for the shared *
 *  engine and build/quantum-coin-toss/refvals.txt for this view.       *
 * ================================================================== */
function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T={ok,eq,close,rel}, T0=Date.now();
  const stSave=Object.assign({},ST);
  function fresh(over){ Object.assign(ST,DEFAULTS,over||{}); resetScenes(); }
  function withState(over,fn){ fresh(over); try{ return fn(); } finally{ fresh(stSave); } }

  engineTests(T);

  /* ---------- A. PhET's values and the sim's shape ---------- */
  eq(FLIP_T,1,'a flip takes 1 s (PhET\'s value)'); eq(COIN_NS.join(','),'10,100,10000','10, 100 or 10 000 identical coins (PhET\'s value)'); eq(BIAS_STEP,0.05,'bias steps of 0.05 (PhET\'s value)');
  eq(TABS.map(t=>t[0]).join(','),'classical,quantum,binom,mix','four views: PhET\'s two scenes, then the analysis');
  { const c=COINS.classical, q=COINS.quantum; ok(c.init==='heads'&&c.p===0.5&&c.preparing,'the classical scene starts heads up at 0.5, being prepared (PhET)');
    ok(q.p===0.5&&quantumInit(q.p)==='superposition'&&q.preparing,'the quantum scene starts in a superposition at 0.5 (PhET)'); ok(c!==q&&c.R!==q.R,'each scene has its own state and its own stream'); }
  ok(sceneOf('quantum')===COINS.quantum&&sceneOf('classical')===COINS.classical,'each coin tab shows its own scene');

  /* ---------- B. the hidden difference ---------- */
  for(const [p,want,bm,bp] of [[0,[0,0,0.5,0.5,1,1,0],[0,0,-1],[0,0,-1]],[0.05,[0.05,0.049999999999999996,0.5,0.7179449471770336,0.9049999999999999,1,0.21794494717703367],[0,0,-0.8999999999999999],[0.43588989435406733,0,-0.8999999999999998]],
      [0.3,[0.3,0.29999999999999993,0.5,0.958257569495584,0.58,1,0.458257569495584],[0,0,-0.39999999999999997],[0.916515138991168,0,-0.40000000000000013]],
      [0.5,[0.5,0.5000000000000001,0.5,1.0000000000000002,0.5,1,0.5000000000000001],[0,0,0],[1.0000000000000002,0,0]],
      [0.7,[0.7,0.7000000000000001,0.5,0.9582575694955842,0.58,1,0.45825756949558405],[0,0,0.3999999999999999],[0.9165151389911681,0,0.39999999999999997]],
      [0.85,[0.85,0.8500000000000001,0.5,0.8570714214271425,0.7449999999999999,1,0.35707142142714254],[0,0,0.7],[0.7141428428542851,0,0.7000000000000001]],
      [1,[1,1,0.5,0.5,1,1,0],[0,0,1],[0,0,1]]]){
    const tag='p = '+p+': ';
    close(bornP(mixBloch(p),[0,0,1]),want[0],1e-14,tag+'face-on, the hidden face comes up with p (numpy, derive)');
    close(bornP(pureBloch(p),[0,0,1]),want[1],1e-14,tag+'and so does the superposition (derive)');
    close(mixPx(p),want[2],1e-15,tag+'sideways the hidden face gives 1/2 (derive)');
    close(purePx(p),want[3],1e-14,tag+'the superposition (1 + 2 sqrt(p(1-p)))/2 (derive)');
    close(mixPurity(p),want[4],1e-14,tag+'the mixture\'s purity p^2 + (1-p)^2 (derive)');
    close(Math.sqrt(p*(1-p)),want[6],1e-14,tag+'the superposition\'s coherence sqrt(p(1-p)) (derive)');
    ok(Math.max(Math.abs(mixBloch(p)[0]-bm[0]),Math.abs(mixBloch(p)[2]-bm[2]))<1e-14,tag+'the mixture sits at (0, 0, 2p-1), inside the ball (derive)');
    ok(Math.max(Math.abs(pureBloch(p)[0]-bp[0]),Math.abs(pureBloch(p)[2]-bp[2]))<1e-14,tag+'the superposition on the sphere (derive)');
  }
  { /* the pure state IS the quantum coin's ket: same Bloch vector two ways */
    let w=0; for(let i=0;i<=20;i++){ const p=i/20, k=[Math.sqrt(p),0,Math.sqrt(1-p),0], r=blochOfKet(k), b=pureBloch(p); w=Math.max(w,Math.abs(r[0]-b[0]),Math.abs(r[2]-b[2])); }
    ok(w<1e-14,'pureBloch(p) = <psi|sigma|psi> for sqrt(p)|up> + sqrt(1-p)|down> over 21 biases ('+w.toExponential(1)+')');
    let mono=true; for(let i=1;i<=10;i++) if(!(purePx(i/20)>purePx((i-1)/20))) mono=false; ok(mono,'P(+x) of the superposition rises to its maximum, 1, at p = 1/2');
    for(const [p,v] of [[0.1,0.8],[0.25,0.9330127018922193],[0.5,1],[0.75,0.9330127018922193],[0.9,0.8]]) close(purePx(p),v,1e-14,'the law at p = '+p+' (derive)'); }
  for(const [seed,p,n,want] of [[7,0.7,1000,[674,507,721,961]],[21,0.5,2000,[991,1038,980,2000]],[3,0.15,1500,[209,783,225,1278]],[9,1,500,[500,265,500,230]]]){
    const r=mixRun(seed,p,n), got=[r.cz,r.cx,r.qz,r.qx], tag='seed '+seed+', p = '+p+', '+n+' of each: ';
    eq(got.join(','),want.join(','),tag+'the four counts, bit for bit (derive)');
    const laws=[p,0.5,p,purePx(p)]; let okk=true; for(let i=0;i<4;i++){ const q=laws[i]; if(Math.abs(got[i]-n*q)>4*Math.sqrt(n*q*(1-q))+1e-9) okk=false; }
    ok(okk,tag+'each within 4 sigma of n x its law');
  }
  withState({view:'mix',mixP:0.5,mixShots:2000,mixSeed:21},()=>{ const m=mixModel(ST); eq(m.run.qx,2000,'at p = 1/2 the superposition goes +x every time'); ok(Math.abs(m.f.cx-0.5)<4*Math.sqrt(0.25/2000),'while the hidden face splits evenly'); });

  /* ---------- C. the models and the readouts ---------- */
  const PRESETS={classical:[{},{_start:1},{_start:1,_flip:1},{_n:10000,_start:1,_flip:1,_rev:1},{_start:1,_p:0,_flip:1,_rev:1},{_hidden:1,_start:1}],
    quantum:[{},{_start:1},{_start:1,_obs:1},{_n:10000,_start:1,_obs:1},{_p:1,_start:1,_obs:1},{_p:0.85}],
    binom:[{},{binN:10},{binN:10000,binP:0.35},{binP:1}],
    mix:[{},{mixP:0},{mixP:0.5},{mixP:1,mixShots:100},{mixP:0.15,mixShots:5000,mixSeed:3}]};
  function applyPreset(v,over){
    const clean={view:v}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    fresh(clean);
    if(isCoinView(v)){ const sc=sceneOf(v); if(over._p!==undefined) sc.p=over._p; if(over._n) setCoinCount(sc,over._n); if(over._hidden) sc.startsHidden=true;
      if(over._start) sceneStart(sc); if(over._flip){ coinPrepare(sc,sc.single,!!over._rev); coinPrepare(sc,sc.set,!!over._rev); coinStep(sc,sc.single,1); coinStep(sc,sc.set,1); }
      if(over._obs){ coinReveal(sc,sc.single); coinReveal(sc,sc.set); } }
  }
  for(const [v] of TABS) for(const over of PRESETS[v]){
    applyPreset(v,over); const M=buildModel(), html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M);
    ok(!/NaN|undefined|Infinity/.test(html),'panels clean for '+v+' '+JSON.stringify(over));
    { const nz=negZeroIn(html); ok(!nz,'no negative zero in the panels for '+v+' '+JSON.stringify(over)+(nz?': '+nz:'')); }
  }
  applyPreset('mix',{mixP:0.7}); ok(readoutHTML(buildModel()).indexOf('0.9583')>=0,'the hidden-difference readout prints P(+x) = 0.9583 at p = 0.7 off the model');
  applyPreset('quantum',{}); ok(readoutHTML(buildModel()).indexOf('0.707')>=0,'the quantum coin readout prints alpha = 0.707 at bias 0.5');
  applyPreset('classical',{_start:1}); ok(readoutHTML(buildModel()).indexOf('revealed')>=0,'the classical coin arrives revealed (the readout says so)');
  fresh(stSave);

  /* ---------- D. the pointer ---------- */
  { const shot=makeShot(1100,712), S=makeScene({getContext:()=>shot});
    withState({view:'classical'},()=>{ ok(!S.pointer('down',400,300),'while preparing the coins cannot be clicked'); sceneStart(COINS.classical);
      const G=viewGeo(shot,S.W,S.H,buildModel()); ok(S.pointer('down',G.single.cx,G.single.cy),'clicking the single coin'); eq(COINS.classical.single.state,'hidden','hides it');
      S.pointer('up',0,0); ok(S.pointer('down',G.C.x+G.C.w/2,G.C.y+G.C.h/2),'clicking the set'); eq(COINS.classical.set.state,'hidden','hides the set'); S.pointer('up',0,0); });
    withState({view:'quantum'},()=>{ sceneStart(COINS.quantum); const G=viewGeo(shot,S.W,S.H,buildModel()); const s0=COINS.quantum.R.s;
      ok(S.pointer('down',G.single.cx,G.single.cy),'clicking the quantum coin'); eq(COINS.quantum.single.state,'revealed','observes it'); ok(COINS.quantum.R.s!==s0,'with a draw: the collapse'); S.pointer('up',0,0); });
    for(const v of ['binom','mix']) withState({view:v},()=>ok(!S.pointer('down',400,300),'the '+v+' view ignores the pointer'));
  }

  /* ---------- E. the layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const FLOOR={classical:2,quantum:2,binom:4,mix:6};
  /* legendAuto draws NO legend when every spot is crossed, so a legend can
     vanish silently: at the two large sizes every legend must find its spot
     (quantum-measurement lost two, looked at and tested) */
  const legendAuto0=legendAuto; let legLost=[];
  legendAuto=function(ctx,b,items){ const r=legendAuto0(ctx,b,items); if(r===null) legLost.push(items.map(i=>i[1]).join(', ')); return r; };
  for(const [v] of TABS) for(const over of PRESETS[v]) for(const [W,H] of SIZES){
    applyPreset(v,over); legLost=[];
    layoutCheck(T,v+' '+JSON.stringify(over),(c,w,hh)=>drawView(c,w,hh,buildModel()),W,H,FLOOR[v]);
    if(W>=1100) ok(!legLost.length,v+' '+JSON.stringify(over)+' '+W+'x'+H+' every legend is drawn'+(legLost.length?' (lost: '+legLost[0]+')':''));
  }
  legendAuto=legendAuto0;
  /* a caption names only panels that are drawn (quantum-measurement's named panels its small sizes skip, looked at) */
  { const NAMES={classical:/histogram counts|Orange:/,quantum:/histogram counts|Orange:/,binom:/Below:|one long run/,mix:/Below:/};
    const LAY={classical:coinsLayout,quantum:coinsLayout,binom:binomLayout,mix:mixLayout};
    let bad=null, n=0; const off={};
    for(const v in LAY) for(const over of PRESETS[v]) for(const [W,H] of SIZES.concat([[700,450],[900,560]])){
      applyPreset(v,over); const L=LAY[v](makeShot(W,H),W,H,buildModel()); n++;
      if(L.G.panelOff){ off[v]=(off[v]||0)+1; if(NAMES[v].test(L.G.fit.txt)&&!bad) bad=v+' '+W+'x'+H+': "'+L.G.fit.txt.slice(0,60)+'"'; }
      else if(!NAMES[v].test(L.Cap.full)&&!bad) bad=v+' '+W+'x'+H+': the panel is drawn but the full caption does not name it'; }
    ok(!bad&&Object.keys(LAY).every(v=>off[v]>0),'every caption names only the panels that are drawn ('+n+' layouts; optional panel off in '+JSON.stringify(off)+(bad?'; '+bad:'')+')'); }
  { applyPreset('classical',{}); const c=makeShot(1400,820); drawView(c,1400,820,buildModel()); const low=c.ops.filter(o=>o.op==='text').reduce((a,o)=>Math.max(a,o.bb[3]),0);
    ok(low<=820-HINT_H,'the lowest canvas text ends '+fmt(820-low,0)+' px above the bottom, clear of the 18-px hint band'); }
  fresh(stSave);
  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
