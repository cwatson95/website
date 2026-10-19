
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
const INFO_CLASSICAL='PhET&rsquo;s classical coin always has a face. Prepare it heads or tails and send it to be measured: it arrives showing that '
  +'face. Flip it and, a second later, it has a new one, heads with probability p, hidden under the cup. It is heads or tails from that moment, '
  +'whether anyone looks or not. Revealing it only shows you what was already there, and hiding and revealing it again changes nothing. '
  +'Ten, a hundred or ten thousand identical coins then count like a binomial, Np &plusmn; &radic;(Np(1&minus;p)): ten look like noise, ten '
  +'thousand almost like a law. Click a coin on the canvas to reveal or hide it.';
const INFO_QUANTUM='PhET&rsquo;s quantum &ldquo;coin&rdquo; is prepared, not flipped, in a state &alpha;|&uarr;&rang; + &beta;|&darr;&rang;. Until it is '
  +'observed it has no face at all, and the picture draws both arrows, each as bright as its probability. Observing it gives &uarr; with '
  +'probability |&alpha;|&sup2;: that is the Born rule, and the face comes into existence only then. After that the coin IS up, or down, and '
  +'hiding and observing it again shows the same face every time; only a repreparation brings the superposition back. Set |&alpha;|&sup2; '
  +'with the slider, or choose a basis state and the coin is certain. Its odds face-on are exactly a biased classical coin&rsquo;s. The '
  +'last tab shows the measurement that tells them apart.';
const INFO={classical:INFO_CLASSICAL,quantum:INFO_QUANTUM,binom:INFO_BINOM,mix:INFO_MIX};
const DERIV={classical:DERIV_COINS,quantum:DERIV_COINS,binom:DERIV_BINOM,mix:DERIV_MIX};
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Quantum Coin Toss (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
  +'New code; no PhET code or assets. PhET&rsquo;s values (the 1-s flip, 10/100/10 000 identical coins, bias steps of 0.05, the arrival '
  +'states and the start-hidden preference) are read from its build 1.0.4 and quantum-measurement&rsquo;s doc/model.md. Everything else is '
  +'exact and pinned in selfTest to build/quantum-measurement/derive.py and build/quantum-coin-toss/derive.py (a bit-exact PRNG twin, '
  +'scipy&rsquo;s binomial and &chi;&sup2;, numpy density matrices).';
const HINTS={classical:'click a coin to reveal or hide it · 1–4 switch views',quantum:'click a coin to observe or hide it · 1–4 switch views',
  binom:'change the seed for a fresh set of runs',mix:'the runs are seeded: change the seed for fresh coins'};
function boot(){
  const canvas=document.getElementById('scene');
  const panel=document.getElementById('panel');
  const tabsEl=document.getElementById('tabs');
  const roEl=document.getElementById('readout');
  const eqEl=document.getElementById('eqbar');
  const tagEl=document.getElementById('tag');
  const hintEl=document.getElementById('hint');
  const errEl=document.getElementById('errbox');
  const S=makeScene(canvas), st=ST;
  let dirty=false;
  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));
  function setView(k){
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)));
  const rows={}, syncers=[];
  function sliderF(id,lab2,lo,hi,step2,get,set,fmtf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.textContent=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); val.textContent=fmtf(get()); syncPanel(); dirty=true; refresh(); });
    rows[id]={row:rowEl,sync}; sync(); return rowEl;
  }
  function slider(key,lab2,lo,hi,step2,fmtf){ return sliderF(key,lab2,lo,hi,step2,()=>st[key],v=>{ st[key]=v; },fmtf); }
  function checkbox(id,lab2,get,set){
    const inp=h('input',{type:'checkbox'}); inp.checked=get();
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ set(inp.checked); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+id]={row:el,sync:()=>{ inp.checked=get(); }};
    return el;
  }
  function chipRow(list,get,set){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>wrapEl.appendChild(h('button',{class:'chip',onclick:()=>{ set(o.id); syncPanel(); dirty=true; refresh(); }},o.name)));
    syncers.push(()=>[].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===get()?' on':'')));
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); }
  function grp(title){ return h('div',{class:'grp'},h('h3',null,title)); }
  const sc=()=>sceneOf(st.view);

  const gCoin=grp('prepare the coin');
  const initC=chipRow([{id:'heads',name:'heads'},{id:'tails',name:'tails'}],()=>COINS.classical.init,v=>{ COINS.classical.init=v; });
  const initQ=chipRow([{id:'up',name:'↑'},{id:'down',name:'↓'}],()=>quantumInit(COINS.quantum.p),v=>{ COINS.quantum.p=v==='up'?1:0; });
  gCoin.appendChild(initC); gCoin.appendChild(initQ);
  gCoin.appendChild(sliderF('bias','P(heads) / P(↑)',0,1,BIAS_STEP,()=>sc().p,v=>{ sc().p=snapBias(v); },v=>fmt(v,2)));
  const goBtn=btn('send to measure',()=>sceneStart(sc())), newBtn=btn('new coin',()=>sceneNewCoin(sc()));
  gCoin.appendChild(h('div',{class:'btnrow'},goBtn,newBtn));
  const hiddenRow=h('div',{class:'checks'},checkbox('hidden','classical coins start hidden',()=>COINS.classical.startsHidden,v=>{ COINS.classical.startsHidden=v; }));
  gCoin.appendChild(hiddenRow);
  const coinTag=h('div',{class:'tag'}); gCoin.appendChild(coinTag);
  const gOne=grp('one coin'), gSet=grp('N identical coins');
  const oneTog=btn('reveal',()=>coinToggle(sc(),sc().single)), oneFlip=btn('flip',()=>coinPrepare(sc(),sc().single,false)), oneFR=btn('flip and reveal',()=>coinPrepare(sc(),sc().single,true));
  gOne.appendChild(h('div',{class:'btnrow'},oneTog,oneFlip)); gOne.appendChild(h('div',{class:'btnrow'},oneFR));
  const nChips=chipRow(COIN_NS.map(n=>({id:n,name:n===10000?'10 000':String(n)})),()=>sc().set.n,v=>setCoinCount(sc(),v));
  gSet.appendChild(nChips);
  const setTog=btn('reveal all',()=>coinToggle(sc(),sc().set)), setFlip=btn('flip all',()=>coinPrepare(sc(),sc().set,false)), setFR=btn('flip and reveal all',()=>coinPrepare(sc(),sc().set,true));
  gSet.appendChild(h('div',{class:'btnrow'},setTog,setFlip)); gSet.appendChild(h('div',{class:'btnrow'},setFR));
  const gBin=grp('the binomial');
  gBin.appendChild(chipRow(COIN_NS.map(n=>({id:n,name:'N = '+(n===10000?'10 000':n)})),()=>st.binN,v=>{ st.binN=v; }));
  gBin.appendChild(slider('binP','bias p',0,1,BIAS_STEP,v=>fmt(v,2)));
  gBin.appendChild(slider('binM','sets M',100,5000,100,v=>fmt(v,0)));
  gBin.appendChild(slider('binSeed','seed ',1,99,1,v=>fmt(v,0)));
  const gMix=grp('the two coins');
  gMix.appendChild(slider('mixP','bias p = P(up)',0,1,BIAS_STEP,v=>fmt(v,2)));
  gMix.appendChild(slider('mixShots','coins of each kind',100,5000,100,v=>fmt(v,0)));
  gMix.appendChild(slider('mixSeed','seed',1,99,1,v=>fmt(v,0)));
  const gInfo=grp('what you are looking at');
  gInfo.appendChild(h('div',{id:'info'}));
  gInfo.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>resetAll())));
  gInfo.appendChild(h('div',{class:'src',html:CREDIT}));
  const gPhys=grp('the physics'); gPhys.appendChild(h('div',{id:'phys'}));
  const GROUPS=[gCoin,gOne,gSet,gBin,gMix,gInfo,gPhys];
  GROUPS.forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');
  function resetAll(){ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; resetScenes(); for(const k in MEMO) delete MEMO[k]; }
  /* a control the view ignores is hidden, never live and inert */
  function syncPanel(){
    const v=st.view, coinV=isCoinView(v), c=sc(), q=c.quantum, prep=c.preparing;
    gCoin.hidden=!coinV; initC.hidden=!coinV||q; initQ.hidden=!coinV||!q; hiddenRow.hidden=!coinV||q;
    goBtn.hidden=!prep; newBtn.hidden=prep;
    rows.bias.row.children[0].textContent=q?'P(↑) = |α|²':'P(heads)';
    oneTog.textContent=c.single.state==='revealed'?'hide':(q?'observe':'reveal');
    oneFlip.textContent=q?'reprepare':'flip'; oneFR.textContent=q?'reprepare and observe':'flip and reveal';
    setTog.textContent=c.set.state==='revealed'?'hide all':(q?'observe all':'reveal all');
    setFlip.textContent=q?'reprepare all':'flip all'; setFR.textContent=q?'reprepare and observe all':'flip and reveal all';
    gOne.hidden=!coinV||prep; gSet.hidden=!coinV; nChips.hidden=!prep;
    [oneTog,oneFlip,oneFR].forEach(b=>b.disabled=c.single.state==='preparing');
    [setTog,setFlip,setFR].forEach(b=>{ b.disabled=c.set.state==='preparing'; b.hidden=prep; });
    coinTag.innerHTML=prep?'prepare the coin, then send it to be measured':(q?'reprepare makes a fresh superposition; observe collapses it':'flip hides a new face; reveal shows it');
    gBin.hidden=v!=='binom'; gMix.hidden=v!=='mix';
    for(const k in rows) rows[k].sync();
    for(const f of syncers) f();
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=HINTS[st.view]||'';
      infoEl.innerHTML=INFO[st.view]||''; physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }
  canvas.addEventListener('pointerdown',e=>{
    if(canvas.setPointerCapture) canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  canvas.addEventListener('pointerup',()=>{ S.pointer('up',0,0); });
  window.addEventListener('keydown',e=>{ if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]); });
  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });
  let frameN=0, last=0, wasBusy=false;
  function frameLoop(tm){
    frameN++;
    const dtw=last?Math.min((tm-last)/1000,0.05):0; last=tm;
    const advanced=S.step(dtw);
    if(advanced||dirty){ dirty=false; try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); } }
    /* a flip that has just finished changes the buttons: resync once */
    const busy=isCoinView(st.view)&&sceneAnimating(sc());
    if(wasBusy&&!busy){ syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
    wasBusy=busy;
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}
