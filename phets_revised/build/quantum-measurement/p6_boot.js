
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
const INFO={coins:INFO_COINS,photons:INFO_PHOTONS,spins:INFO_SPINS,bloch:INFO_BLOCH,born:INFO_BORN,binom:INFO_BINOM};
const DERIV={coins:DERIV_COINS,photons:DERIV_PHOTONS,spins:DERIV_SPINS,bloch:DERIV_BLOCH,born:DERIV_BORN,binom:DERIV_BINOM};
const CREDIT='Remake of PhET Interactive Simulations&rsquo; Quantum Measurement (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
  +'New code; no PhET code or assets. PhET&rsquo;s values (the 1-s flip, 10/100/10 000 coins, bias steps of 0.05, the photon bench and its 0.3/s photons, '
  +'the six Stern&ndash;Gerlach experiments, the Bloch sphere&rsquo;s 15&deg; steps, ten atoms and 0&ndash;1 ns delay) are read from its build 1.0.5 and its '
  +'doc/model.md; the electron&rsquo;s &gamma;/2&pi; is CODATA 2022 (as in bloch_sphere.html). Everything else is exact and pinned in selfTest to '
  +'build/quantum-measurement/derive.py (a bit-exact PRNG twin, scipy&rsquo;s binomial and &chi;&sup2;, numpy projectors, scipy expm).';
const HINTS={coins:'click a coin to reveal or hide it · 1–6 switch views',photons:'click the laser for a photon · drag the dial · space pauses',
  spins:'click the source for a particle · space pauses',bloch:'drag to turn the spheres · r resets the view · space pauses',
  born:'drag on a panel to move its cursor',binom:'change the seed for a fresh set of runs'};
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
  /* a slider bound to a getter and a setter (the coin bias lives in its scene) */
  function sliderF(id,lab2,lo,hi,step2,get,set,fmtf){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.textContent=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); val.textContent=fmtf(get()); syncPanel(); dirty=true; refresh(); });
    rows[id]={row:rowEl,sync}; sync(); return rowEl;
  }
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){ return sliderF(key,lab2,lo,hi,step2,()=>st[key],v=>{ st[key]=v; if(onchg) onchg(); },fmtf); }
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
  function btn(label,fn){ const b=h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); return b; }
  function grp(title){ return h('div',{class:'grp'},h('h3',null,title)); }
  const sc=()=>COINS[st.coinScene];

  /* ---- the coins ---- */
  const gCoin=grp('the coin');
  gCoin.appendChild(chipRow([{id:'classical',name:'classical coin'},{id:'quantum',name:'quantum “coin”'}],()=>st.coinScene,v=>{ st.coinScene=v; }));
  const initC=chipRow([{id:'heads',name:'heads'},{id:'tails',name:'tails'}],()=>sc().init,v=>{ sc().init=v; });
  const initQ=chipRow([{id:'up',name:'↑'},{id:'down',name:'↓'}],()=>quantumInit(sc().p),v=>{ sc().p=v==='up'?1:0; });
  gCoin.appendChild(initC); gCoin.appendChild(initQ);
  gCoin.appendChild(sliderF('bias','P(heads) / P(↑)',0,1,BIAS_STEP,()=>sc().p,v=>{ sc().p=snapBias(v); },v=>fmt(v,2)));
  const goBtn=btn('send to measure',()=>sceneStart(sc())), newBtn=btn('new coin',()=>sceneNewCoin(sc()));
  gCoin.appendChild(h('div',{class:'btnrow'},goBtn,newBtn));
  gCoin.appendChild(h('div',{class:'checks'},checkbox('hidden','classical coins start hidden',()=>COINS.classical.startsHidden,v=>{ COINS.classical.startsHidden=v; })));
  const coinTag=h('div',{class:'tag'}); gCoin.appendChild(coinTag);
  const gOne=grp('one coin'), gSet=grp('N identical coins');
  const oneTog=btn('reveal',()=>coinToggle(sc(),sc().single)), oneFlip=btn('flip',()=>coinPrepare(sc(),sc().single,false)), oneFR=btn('flip and reveal',()=>coinPrepare(sc(),sc().single,true));
  gOne.appendChild(h('div',{class:'btnrow'},oneTog,oneFlip)); gOne.appendChild(h('div',{class:'btnrow'},oneFR));
  const nChips=chipRow(COIN_NS.map(n=>({id:n,name:n===10000?'10 000':String(n)})),()=>sc().set.n,v=>setCoinCount(sc(),v));
  gSet.appendChild(nChips);
  const setTog=btn('reveal all',()=>coinToggle(sc(),sc().set)), setFlip=btn('flip all',()=>coinPrepare(sc(),sc().set,false)), setFR=btn('flip and reveal all',()=>coinPrepare(sc(),sc().set,true));
  gSet.appendChild(h('div',{class:'btnrow'},setTog,setFlip)); gSet.appendChild(h('div',{class:'btnrow'},setFR));

  /* ---- the photons ---- */
  const gPh=grp('the photons');
  gPh.appendChild(chipRow([{id:'single',name:'one photon at a time'},{id:'many',name:'a beam'}],()=>st.phMode,v=>{ st.phMode=v; }));
  const emitRow=h('div',{class:'btnrow'},btn('emit a photon',()=>{ photonEmit(PHOT.single,st,0); st.running=true; }));
  gPh.appendChild(emitRow);
  gPh.appendChild(slider('phRate','photons per second',0,PH.RATE_MAX,1,v=>fmt(v,0)+' /s'));
  gPh.appendChild(chipRow(['vertical','horizontal','fortyFive','unpolarized','custom'].map(k=>({id:k,name:presetName(k)})),()=>st.phPreset,v=>{ st.phPreset=v; photonAfterAngle(); }));
  gPh.appendChild(slider('phCustom','custom angle',0,90,PH.CUSTOM_STEP,v=>fmt(v,0)+'°',photonAfterAngle));
  gPh.appendChild(chipRow([{id:'classical',name:'classical'},{id:'quantum',name:'quantum'}],()=>st.phBehavior,v=>{ if(st.phBehavior!==v){ st.phBehavior=v; photonClear(PHOT[st.phMode]); } }));
  gPh.appendChild(h('div',{class:'btnrow'},btn('clear photon counts',()=>photonCounts(PHOT[st.phMode]))));
  const phTag=h('div',{class:'tag'}); gPh.appendChild(phTag);

  /* ---- the spins ---- */
  const gSg=grp('the spins');
  gSg.appendChild(chipRow(SG_EXPS.map(e=>({id:e.id,name:e.name})),()=>st.sgExp,v=>{ st.sgExp=v; sgAfterChange(); }));
  gSg.appendChild(chipRow([{id:'single',name:'single particles'},{id:'continuous',name:'continuous'}],()=>st.sgMode,v=>{ st.sgMode=v; sgAfterChange(); }));
  const shootRow=h('div',{class:'btnrow'},btn('shoot a particle',()=>{ sgShoot(SGS,st); st.running=true; }));
  gSg.appendChild(shootRow);
  gSg.appendChild(slider('sgAmount','particle amount',0,1,0.01,v=>fmt(v,2),()=>{}));
  const srcChips=chipRow(['+Z','+X','-Z'].map(k=>({id:k,name:k.replace('-','−')})),()=>st.sgSrc,v=>{ st.sgSrc=v; sgAfterChange(); });
  gSg.appendChild(srcChips);
  gSg.appendChild(slider('sgA2','|α|² = P(↑z)',0,1,BIAS_STEP,v=>fmt(v,2),sgAfterChange));
  const c1Chips=chipRow([{id:'z',name:'magnet 1: z'},{id:'x',name:'magnet 1: x'}],()=>st.sgC1,v=>{ st.sgC1=v; sgAfterChange(); });
  const c2Chips=chipRow([{id:'z',name:'magnets 2, 3: z'},{id:'x',name:'magnets 2, 3: x'}],()=>st.sgC2,v=>{ st.sgC2=v; sgAfterChange(); });
  gSg.appendChild(c1Chips); gSg.appendChild(c2Chips);
  const blockChips=chipRow([{id:'up',name:'block ↑'},{id:'down',name:'block ↓'}],()=>st.sgBlock,v=>{ st.sgBlock=v; sgResetCounts(SGS); });
  gSg.appendChild(blockChips);
  gSg.appendChild(h('div',{class:'checks'},checkbox('sgExpect','expected percentage',()=>st.sgExpect,v=>{ st.sgExpect=v; })));
  gSg.appendChild(h('div',{class:'btnrow'},btn('clear spin counts',()=>sgResetCounts(SGS))));

  /* ---- the Bloch sphere ---- */
  const bPrep=()=>{ blochReprepare(BLO,st); blochResetCounts(BLO); };
  const gBp=grp('prepare the spin');
  gBp.appendChild(chipRow(Object.keys(BL_PRESETS).map(k=>({id:k,name:k.replace('-','−')})),()=>st.bPreset,v=>{ st.bPreset=v; st.bTheta=BL_PRESETS[v][0]; st.bPhi=BL_PRESETS[v][1]; bPrep(); }));
  gBp.appendChild(slider('bTheta','polar angle θ',0,Math.PI,BL.STEP,v=>fmt(v/DEG,0)+'°',()=>{ st.bPreset='custom'; bPrep(); }));
  gBp.appendChild(slider('bPhi','azimuth φ',0,2*Math.PI,BL.STEP,v=>fmt(v/DEG,0)+'°',()=>{ st.bPreset='custom'; bPrep(); }));
  const gBm=grp('measure it');
  gBm.appendChild(chipRow(['X','Y','Z'].map(k=>({id:k,name:k})),()=>st.bAxis,v=>{ st.bAxis=v; blochResetCounts(BLO); }));
  /* PhET resets the counts on the state, the axis, the delay and the field, not on the number of atoms */
  gBm.appendChild(chipRow([{id:1,name:'× 1 atom'},{id:10,name:'× 10 atoms'}],()=>st.bAtoms,v=>{ st.bAtoms=v; blochReprepare(BLO,st); }));
  const obsBtn=btn('observe',()=>blochButton(BLO,st));
  gBm.appendChild(h('div',{class:'btnrow'},obsBtn,btn('clear atom counts',()=>blochResetCounts(BLO))));
  gBm.appendChild(h('div',{class:'checks'},checkbox('bField','magnetic field along z',()=>st.bField,v=>{ st.bField=v; blochReprepare(BLO,st); blochResetCounts(BLO); })));
  gBm.appendChild(slider('bStrength','field B / B₀',-1,1,0.05,v=>fmt(v,2),()=>{ blochReprepare(BLO,st); blochResetCounts(BLO); }));
  gBm.appendChild(slider('bDelay','delay, ns',0,BL.DELAY_MAX,0.01,v=>fmt(v,2)+' ns',()=>{ blochReprepare(BLO,st); blochResetCounts(BLO); }));
  gBm.appendChild(chipRow(['Z','X','Y'].map(k=>({id:k,name:k+' basis'})),()=>st.bBasis,v=>{ st.bBasis=v; }));
  gBm.appendChild(h('div',{class:'checks'},checkbox('bGlobal','show the global phase',()=>st.bGlobal,v=>{ st.bGlobal=v; })));
  gBm.appendChild(h('div',{class:'btnrow'},btn('reset the view',()=>resetCam())));
  const blTag=h('div',{class:'tag'}); gBm.appendChild(blTag);

  /* ---- time (the photons, the spins, the Bloch sphere) ---- */
  const gTime=grp('time');
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs',()=>st.running,v=>{ st.running=v; })));
  const speedChips=chipRow([{id:'normal',name:'normal'},{id:'slow',name:'slow motion'}],()=>st.speed,v=>{ st.speed=v; });
  gTime.appendChild(speedChips);
  gTime.appendChild(h('div',{class:'btnrow'},btn('step',()=>stepOnce())));

  /* ---- the analysis views ---- */
  const gBorn=grp('the Born rule');
  gBorn.appendChild(slider('bornTh','angle Θ',0,180,1,v=>fmt(v,0)+'°'));
  gBorn.appendChild(slider('bornAlpha','middle angle α',0,180,1,v=>fmt(v,0)+'°'));
  gBorn.appendChild(slider('bornN','magnets in the chain',1,64,1,v=>fmt(v,0)));
  gBorn.appendChild(slider('bornShots','shots per point',100,5000,100,v=>fmt(v,0)));
  gBorn.appendChild(slider('bornSeed','seed',1,99,1,v=>fmt(v,0)));
  const gBin=grp('the binomial');
  gBin.appendChild(chipRow(COIN_NS.map(n=>({id:n,name:'N = '+(n===10000?'10 000':n)})),()=>st.binN,v=>{ st.binN=v; }));
  gBin.appendChild(slider('binP','bias p',0,1,BIAS_STEP,v=>fmt(v,2)));
  gBin.appendChild(slider('binM','sets M',100,5000,100,v=>fmt(v,0)));
  gBin.appendChild(slider('binSeed','seed ',1,99,1,v=>fmt(v,0)));

  const gInfo=grp('what you are looking at');
  gInfo.appendChild(h('div',{id:'info'}));
  gInfo.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>resetAll())));
  gInfo.appendChild(h('div',{class:'src',html:CREDIT}));
  const gPhys=grp('the physics'); gPhys.appendChild(h('div',{id:'phys'}));
  const GROUPS=[gCoin,gOne,gSet,gPh,gSg,gBp,gBm,gTime,gBorn,gBin,gInfo,gPhys];
  GROUPS.forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetAll(){
    const v=st.view; Object.assign(st,DEFAULTS); st.view=v;
    resetScenes(); resetCam(); for(const k in MEMO) delete MEMO[k];
  }
  function stepOnce(){
    const dt=PH.STEP_DT, v=st.view;          /* PhET's step: 2/60 s */
    if(v==='photons') photonAdvance(PHOT[st.phMode],st,dt*simFactor(st));
    else if(v==='spins') sgAdvance(SGS,st,dt);
    else if(v==='bloch') blochAdvance(BLO,st,dt);
  }
  /* a control the view ignores is hidden, never live and inert */
  function syncPanel(){
    const v=st.view, c=sc(), q=c.quantum, prep=c.preparing;
    gCoin.hidden=gOne.hidden=gSet.hidden=v!=='coins';
    initC.hidden=q; initQ.hidden=!q;
    goBtn.hidden=!prep; newBtn.hidden=prep;
    rows.bias.row.children[0].textContent=q?'P(↑) = |α|²':'P(heads)';
    oneTog.textContent=c.single.state==='revealed'?'hide':(q?'observe':'reveal');
    oneFlip.textContent=q?'reprepare':'flip'; oneFR.textContent=q?'reprepare and observe':'flip and reveal';
    setTog.textContent=c.set.state==='revealed'?'hide all':(q?'observe all':'reveal all');
    setFlip.textContent=q?'reprepare all':'flip all'; setFR.textContent=q?'reprepare and observe all':'flip and reveal all';
    gOne.hidden=gSet.hidden=v!=='coins'||prep; nChips.hidden=!prep;
    if(v==='coins'&&prep) gSet.hidden=false;
    [oneTog,oneFlip,oneFR].forEach(b=>b.disabled=c.single.state==='preparing');
    [setTog,setFlip,setFR].forEach(b=>b.disabled=c.set.state==='preparing');
    [setTog,setFlip,setFR].forEach(b=>b.hidden=prep);
    coinTag.innerHTML=prep?'prepare the coin, then send it to be measured':(q?'reprepare makes a fresh superposition; observe collapses it':'flip hides a new face; reveal shows it');
    gPh.hidden=v!=='photons';
    emitRow.hidden=st.phMode!=='single'; rows.phRate.row.hidden=st.phMode!=='many'; rows.phCustom.row.hidden=st.phPreset!=='custom';
    phTag.innerHTML=st.phMode==='single'?'PhET caps each count at 999; a new polarization clears the counts':'the rates are averaged over 1 s in 0.5-s samples (PhET)';
    gSg.hidden=v!=='spins';
    const cust=st.sgExp==='custom', two=sgAxes(st).length>1, cont=st.sgMode==='continuous';
    shootRow.hidden=cont; rows.sgAmount.row.hidden=!cont; srcChips.hidden=cust; rows.sgA2.row.hidden=!cust;
    c1Chips.hidden=c2Chips.hidden=!cust; blockChips.hidden=!(cont&&two);
    gBp.hidden=gBm.hidden=v!=='bloch';
    rows.bStrength.row.hidden=rows.bDelay.row.hidden=!st.bField;
    obsBtn.textContent=BLO.phase==='observed'?'reprepare':(BLO.phase==='timing'?'timing…':(st.bField?'start':'observe'));
    obsBtn.disabled=BLO.phase==='timing';
    blTag.innerHTML='B<sub>0</sub> = '+fmt(B0_T*1e3,2)+' mT turns an electron once a nanosecond';
    gTime.hidden=!(v==='photons'||v==='spins'||v==='bloch');
    speedChips.hidden=v!=='photons';
    gBorn.hidden=v!=='born'; gBin.hidden=v!=='binom';
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
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'||e.key==='R'){ resetCam(); dirty=true; refresh(); }
    else if(e.key==='.'){ stepOnce(); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });
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
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    /* a flip or a timing that has just finished changes the buttons: resync once */
    const busy=(st.view==='coins'&&sceneAnimating(sc()))||(st.view==='bloch'&&BLO.phase==='timing');
    if(wasBusy&&!busy){ syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }
    wasBusy=busy;
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}
