
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
function boot(){
  const canvas=document.getElementById('scene');
  const panel=document.getElementById('panel');
  const tabsEl=document.getElementById('tabs');
  const roEl=document.getElementById('readout');
  const eqEl=document.getElementById('eqbar');
  const tagEl=document.getElementById('tag');
  const hintEl=document.getElementById('hint');
  const errEl=document.getElementById('errbox');
  const S=makeScene(canvas), st=S.st;
  let dirty=false;

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));
  const W_=()=>worldOf(st.view), G_=()=>W_().g;

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncCounts(); syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab)); });

  const rows={};
  function slider(key,lab,lo,hi,step2,fmtf,onchg,onrelease){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ clearOops(); st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    if(onrelease) inp.addEventListener('change',()=>{ onrelease(); sync(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab);
    inp.addEventListener('change',()=>{ clearOops(); st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(c.disabled) return;
        clearOops(); st[key]=o.id; if(onPick) onPick(o);
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS=[];
  function trackChips(el,list,key){ CHIPROWS.push([el,list,key]); }
  function button(lab,fn){ return h('button',{onclick:()=>{ clearOops(); fn(); syncCounts(); syncChips(); syncPanel(); dirty=true; refresh(); }},lab); }
  /* an action dismisses the Oops on screen BEFORE it acts, so one it raises
     itself (erasing while T is held) is the one the user sees */
  function clearOops(){ const w=WORLD[st.view]; if(w) w.g.oops=null; }
  /* the model changed without time passing: PhET's updateWhenPaused */
  const touched=()=>{ const g=G_(); if(!st.running) gasRefresh(g); };

  /* ---- the particles (the gas law, the moving wall, the energy) ---- */
  const gPart=h('div',{class:'grp'},h('h3',null,'the particles'));
  gPart.appendChild(slider('nH','heavy (28 AMU)',0,GAS.NMAX,1,v=>fmt(v,0),()=>{ gasSetCount(G_(),0,st.nH); touched(); syncCounts(); }));
  gPart.appendChild(slider('nL','light (4 AMU)',0,GAS.NMAX,1,v=>fmt(v,0),()=>{ gasSetCount(G_(),1,st.nL); touched(); syncCounts(); }));
  const pumpChips=chipRow(PUMPS,'pump'); gPart.appendChild(h('div',{class:'tag'},'the pump (drag its handle) pumps:')); gPart.appendChild(pumpChips); trackChips(pumpChips,PUMPS,'pump');
  gPart.appendChild(h('div',{class:'btnrow'},button('erase particles',()=>{ gasRemoveAll(G_()); touched(); })));
  const partTag=h('div',{class:'tag'}); gPart.appendChild(partTag);

  /* ---- hold constant (the gas law) ---- */
  const gHold=h('div',{class:'grp'},h('h3',null,'hold constant'));
  const holdChips=chipRow(HOLDS,'hold',o=>{ const g=G_(); if(!gasSetHold(g,o.id)) st.hold=g.hold; });
  gHold.appendChild(holdChips); trackChips(holdChips,HOLDS,'hold');
  const holdTag=h('div',{class:'tag'}); gHold.appendChild(holdTag);

  /* ---- heat / cool: PhET's slider snaps back to zero when released ---- */
  const gHeat=h('div',{class:'grp'},h('h3',null,'heat / cool'));
  gHeat.appendChild(slider('heat','cool ← → heat',-1,1,0.01,v=>(v>0?'+':'')+fmt(v,2),null,()=>{ st.heat=0; }));
  const heatTag=h('div',{class:'tag'}); gHeat.appendChild(heatTag);

  /* ---- the moving wall's speed limit (PhET: 800 m/s) ---- */
  const gWall=h('div',{class:'grp'},h('h3',null,'the wall'));
  gWall.appendChild(slider('wallU','speed limit, m/s',10,800,10,v=>fmt(v,0),()=>{ G_().wallSpeed=st.wallU; }));
  const wallTag=h('div',{class:'tag'}); gWall.appendChild(wallTag);

  /* ---- the container ---- */
  const gBox=h('div',{class:'grp'},h('h3',null,'the container'));
  const lidBtn=h('div',{class:'btnrow'},button('return lid',()=>{ gasReturnLid(G_()); touched(); }));
  gBox.appendChild(lidBtn);
  const boxTag=h('div',{class:'tag'}); gBox.appendChild(boxTag);

  /* ---- the injection temperature, collisions, histograms (the energy) ---- */
  const gInj=h('div',{class:'grp'},h('h3',null,'injection temperature'));
  const injChips=chipRow(INJ,'injMode',()=>{ const g=G_(); g.injectT=st.injMode==='set'?st.injT:null; });
  gInj.appendChild(injChips); trackChips(injChips,INJ,'injMode');
  gInj.appendChild(slider('injT','set to, K',50,1000,50,v=>fmt(v,0)+' K',()=>{ const g=G_(); if(st.injMode==='set') g.injectT=st.injT; }));
  gInj.appendChild(h('div',{class:'checks'},checkbox('coll','particle–particle collisions',()=>{ G_().collisions=st.coll; })));
  gInj.appendChild(h('div',{class:'checks'},checkbox('histH','heavy histogram'),checkbox('histL','light histogram')));
  gInj.appendChild(h('div',{class:'tag'},'histogram scale (particles):'));
  const zoomChips=chipRow(ZOOM_LIST,'zoom'); gInj.appendChild(zoomChips); trackChips(zoomChips,ZOOM_LIST,'zoom');

  /* ---- tools ---- */
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  const cbWall=checkbox('showWallVel','wall velocity');
  const cbCounter=checkbox('showCounter','collision counter');
  gTools.appendChild(h('div',{class:'checks'},checkbox('showWidth','width'),checkbox('showWatch','stopwatch'),cbCounter,cbWall));
  const watchBtns=h('div',{class:'btnrow'},button('stopwatch start / stop',()=>{ const g=G_(); g.watch.on=!g.watch.on; }),
                                           button('reset',()=>{ const g=G_(); g.watch.on=false; g.watch.t=0; }));
  gTools.appendChild(watchBtns);
  const counterBtns=h('div',{class:'btnrow'},button('count wall hits',()=>{ const g=G_(); g.counter.on=true; g.counter.count=0; g.counter.t=0; g.counter.period=st.period; }));
  gTools.appendChild(counterBtns);
  const periodChips=chipRow(PERIODS,'period',()=>{ const g=G_(); g.counter.on=false; g.counter.count=0; g.counter.t=0; g.counter.period=st.period; });
  gTools.appendChild(periodChips); trackChips(periodChips,PERIODS,'period');
  const unitTChips=chipRow(UNITS_T,'unitT'), unitPChips=chipRow(UNITS_P,'unitP');
  gTools.appendChild(unitTChips); trackChips(unitTChips,UNITS_T,'unitT');
  gTools.appendChild(unitPChips); trackChips(unitPChips,UNITS_P,'unitP');
  gTools.appendChild(h('div',{class:'checks'},checkbox('noise','pressure noise (PhET’s gauge jitter)',()=>{ G_().noiseOn=st.noise; })));

  /* ---- diffusion ---- */
  const gDiff=h('div',{class:'grp'},h('h3',null,'the two gases'));
  const diffCount=k=>()=>{ const g=G_(); gasDiffCount(g,k,k?st.d2n:st.d1n,k?st.d2T:st.d1T); };
  const diffMT=k=>()=>{ const g=G_(); gasDiffMassTemp(g,k,k?st.d2m:st.d1m,k?st.d2T:st.d1T); };
  const diffR=k=>()=>{ const g=G_(); gasDiffRadius(g,k,k?st.d2r:st.d1r,st.running); };
  gDiff.appendChild(h('div',{class:'tag'},'particle 1 (blue, starts on the left)'));
  gDiff.appendChild(slider('d1n','number',0,GAS.DIFF_NMAX,GAS.DIFF_DN,v=>fmt(v,0),diffCount(0)));
  gDiff.appendChild(slider('d1m','mass, AMU',GAS.DIFF_M[0],GAS.DIFF_M[1],1,v=>fmt(v,0),diffMT(0)));
  gDiff.appendChild(slider('d1r','radius, pm',GAS.DIFF_R[0],GAS.DIFF_R[1],GAS.DIFF_RSTEP,v=>fmt(v,0),diffR(0)));
  gDiff.appendChild(slider('d1T','initial T, K',GAS.DIFF_T[0],GAS.DIFF_T[1],GAS.DIFF_TSTEP,v=>fmt(v,0),diffMT(0)));
  gDiff.appendChild(h('div',{class:'tag'},'particle 2 (red, starts on the right)'));
  gDiff.appendChild(slider('d2n','number ',0,GAS.DIFF_NMAX,GAS.DIFF_DN,v=>fmt(v,0),diffCount(1)));
  gDiff.appendChild(slider('d2m','mass, AMU ',GAS.DIFF_M[0],GAS.DIFF_M[1],1,v=>fmt(v,0),diffMT(1)));
  gDiff.appendChild(slider('d2r','radius, pm ',GAS.DIFF_R[0],GAS.DIFF_R[1],GAS.DIFF_RSTEP,v=>fmt(v,0),diffR(1)));
  gDiff.appendChild(slider('d2T','initial T, K ',GAS.DIFF_T[0],GAS.DIFF_T[1],GAS.DIFF_TSTEP,v=>fmt(v,0),diffMT(1)));
  const divBtn=h('button',{onclick:()=>{ const g=G_();
    if(g.divided){ gasSetDivided(g,false); st.divided=false; if(g.flow) gasFlowOn(g); }
    else { gasDiffRestart(g,st.d1n,st.d1T,st.d2n,st.d2T); st.divided=true; W_().hist=[]; }
    syncPanel(); dirty=true; refresh(); }},'remove divider');
  gDiff.appendChild(h('div',{class:'btnrow'},divBtn));
  gDiff.appendChild(h('div',{class:'checks'},checkbox('dCOM','centre of mass'),checkbox('dFlow','particle flow rate'),checkbox('dScale','scale')));
  const speedChips=chipRow([{id:false,name:'normal'},{id:true,name:'slow'}],'slow');
  gDiff.appendChild(speedChips); trackChips(speedChips,[{id:false,name:'normal'},{id:true,name:'slow'}],'slow');

  /* ---- the pressure ---- */
  const gPress=h('div',{class:'grp'},h('h3',null,'the gas on the walls'));
  const restartP=()=>{ resetWorld('pressure'); };
  gPress.appendChild(slider('pN','heavy disks',10,400,10,v=>fmt(v,0),restartP));
  gPress.appendChild(slider('pT','temperature, K',100,1000,50,v=>fmt(v,0)+' K',restartP));
  gPress.appendChild(h('div',{class:'checks'},checkbox('pColl','particle–particle collisions',restartP)));
  gPress.appendChild(h('div',{class:'btnrow'},button('restart the count',restartP)));
  const pressTag=h('div',{class:'tag'}); gPress.appendChild(pressTag);

  /* ---- equilibrium ---- */
  const gEq=h('div',{class:'grp'},h('h3',null,'the start'));
  const restartE=()=>{ resetWorld('equil'); };
  const startChips=chipRow(STARTS,'eStart',restartE); gEq.appendChild(startChips); trackChips(startChips,STARTS,'eStart');
  gEq.appendChild(slider('eN','disks (half heavy)',20,600,20,v=>fmt(v,0),restartE));
  gEq.appendChild(h('div',{class:'checks'},checkbox('eColl','particle–particle collisions',restartE)));
  gEq.appendChild(h('div',{class:'btnrow'},button('restart',restartE)));

  /* ---- time ---- */
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gRun.appendChild(h('div',{class:'btnrow'},button('step 0.2 ps',()=>{ S.stepOnce(); }),
    button('reset this view',()=>{ resetView(); })));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Gas Properties (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s constants are read from its published build and its model notes; everything else is derived and pinned in selfTest to build/gas-properties/derive.py '
      +'(exact rational collision algebra, a brute-force event-driven run, bit-exact mulberry32, Dirichlet moments, B₂ and B₃ by quadrature).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gPart,gHold,gHeat,gWall,gBox,gInj,gTools,gDiff,gPress,gEq,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetView(){
    const v=st.view;
    if(v==='ideal'||v==='explore'||v==='energy'){ st.heat=0; if(v==='ideal') st.hold='nothing'; }
    if(v==='diffusion') st.divided=true;
    resetWorld(v);
  }
  function syncCounts(){
    if(!BOXVIEWS[st.view]) return;
    const g=G_(); st.nH=gasCount(g,0); st.nL=gasCount(g,1); st.hold=g.hold;
    if(rows.nH){ rows.nH.sync(); rows.nL.sync(); }
  }
  S.onCounts=()=>{ syncCounts(); };
  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const v=st.view, box=!!BOXVIEWS[v], g=G_();
    gPart.hidden=!box; gHold.hidden=(v!=='ideal'); gHeat.hidden=!box; gWall.hidden=(v!=='explore'); gBox.hidden=!box; gInj.hidden=(v!=='energy');
    gTools.hidden=!box; gDiff.hidden=(v!=='diffusion'); gPress.hidden=(v!=='pressure'); gEq.hidden=(v!=='equil');
    if(box){
      st.hold=g.hold;
      /* PhET's enabling: T needs particles and a closed lid; P needs a pressure */
      [].forEach.call(holdChips.children,(b,i)=>{ const ok=gasHoldAllowed(g,HOLDS[i].id); b.disabled=!ok; b.style.opacity=ok?'1':'0.4'; });
      const locked=v==='ideal'&&(g.hold==='temperature'||g.hold==='pressureT');
      rows.heat.inp.disabled=locked; rows.heat.row.style.opacity=locked?'0.45':'1';
      lidBtn.hidden=!(g.lid&&!g.lid.on);
      rows.cb_showCounter.row.hidden=(v==='energy'); counterBtns.hidden=(v==='energy'||!st.showCounter); periodChips.hidden=(v==='energy'||!st.showCounter);
      rows.cb_showWallVel.row.hidden=(v!=='explore'); watchBtns.hidden=!st.showWatch;
      rows.injT.row.style.opacity=st.injMode==='set'?'1':'0.45'; rows.injT.inp.disabled=st.injMode!=='set';
    }
    divBtn.textContent=st.divided?'remove divider':'reset divider';
    for(const k in rows) rows[k].sync();
    partTag.innerHTML=v==='energy'?'the width is fixed here (PhET holds V on this screen)':'a full stroke of the pump adds 50; at most '+GAS.NMAX+' of each';
    holdTag.innerHTML=g.hold==='pressureV'?'the wall moves to keep P: V = NkT/P':g.hold==='pressureT'?'the temperature follows to keep P: T = PV/Nk':g.hold==='temperature'?'the heater is locked and the lid is shut':g.hold==='volume'?'the wall is locked':'change N, T or V and P answers';
    heatTag.innerHTML='PhET&rsquo;s heater scales every speed by 1 + a/800 per 60-fps frame; the slider springs back to zero when you let go';
    wallTag.innerHTML='PhET&rsquo;s limit is 800 m/s, faster than sound in the heavy gas at 300 K (517 m/s): a shock. Try 20 m/s for a reversible push';
    boxTag.innerHTML=g.lid&&g.lid.on?(gasLidOpen(g)?'the lid is open '+fmt(gasOpening(g)/1000,2)+' nm: particles that reach the gap leave':'drag the knob on the lid to open it'):'the lid blew off (P &gt; 20,000 kPa): return it';
    pressTag.innerHTML='changing anything restarts the count; the plot is the running average since the start';
    runTag.innerHTML='space runs/pauses &nbsp; <b>s</b> steps 0.2 ps &nbsp; <b>r</b> resets this view &nbsp; 1&ndash;6 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=BOXVIEWS[st.view]?'drag the wall grip, the lid knob or the pump · space pauses · 1–6 switch views':'space pauses · 1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncCounts(); roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncCounts(); syncPanel(); dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='s'){ S.stepOnce(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ resetView(); syncCounts(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0, lastHold=null;
  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        const g=G_();
        if(advanced&&frameN%10===0){ roEl.innerHTML=readoutHTML(S.model()); eqEl.innerHTML=eqbarHTML(S.model()); }
        /* a model-side change of the hold (an Oops) re-enables the panel */
        if(BOXVIEWS[st.view]&&g.hold!==lastHold){ lastHold=g.hold; st.hold=g.hold; syncChips(); syncPanel(); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncCounts(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  ideal:'A box of hard disks: heavy ones like nitrogen (28 AMU) and light ones like helium (4 AMU), bouncing off each other and the walls '
    +'without losing any energy. Pump some in, heat or cool them from below, slide the left wall, or open the lid and watch the fast ones '
    +'escape first. The thermometer reads PhET&rsquo;s temperature, T = (2/3)&lang;KE&rang;/k, and the gauge PhET&rsquo;s pressure, P = NkT/V, '
    +'so PV = NkT holds by construction; the question the screen asks is what happens to the other two when you hold one still. Hold V and '
    +'heat: P climbs with T (Gay-Lussac). Hold T and squeeze: P climbs as 1/V (Boyle). Hold P and heat: the wall walks out, V in step with T '
    +'(Charles). Hold P and pump: the temperature falls to make room (Avogadro, at fixed P and V). Ask for the impossible &mdash; hold T in an '
    +'empty box, or hold P past the box&rsquo;s range &mdash; and you get PhET&rsquo;s Oops.',
  explore:'The same box, but now the left wall is a piston that does work. Each disk that meets the moving wall leaves with v&prime; = 2u &minus; v: '
    +'push in (u &gt; 0) and it comes back faster; pull out and it comes back slower. Push slowly and the gas warms along its adiabat. For points '
    +'that would be T&middot;V = constant, because a disk has only two ways to move (&gamma; = 1 + 2/f = 2; a real monatomic gas, with three, follows '
    +'T&middot;V<sup>2/3</sup>); disks of finite size are stiffer, and 100 heavy ones squeezed from 10 to 7 nm end 6.9 % above the point law, exactly '
    +'where their virial pressure says they should. Now push at PhET&rsquo;s limit, 800 m/s: that is faster than sound in the heavy gas at 300 K '
    +'(517 m/s), the wall drives a shock, and the gas ends two or three times hotter than the adiabat allows &mdash; irreversibly. Pull it out that fast and almost no disk catches it: the gas does no work, which is Joule&rsquo;s free expansion, and it does not cool at all. '
    +'PhET&rsquo;s own wall returns v&prime; = u &minus; v, which does half this work; this remake uses the elastic rule.',
  energy:'Why do the disks settle into the spread of speeds they do? Every collision shares energy out differently, and after a few per disk the '
    +'histogram stops changing: it is the Maxwell&ndash;Boltzmann distribution. In two dimensions the energy law is a pure exponential, e<sup>&minus;E/kT&#8322;</sup>, '
    +'the same for both species; the speed law is (mv/kT&#8322;) e<sup>&minus;mv&sup2;/2kT&#8322;</sup>, so the light disks run &radic;7 = 2.6 times faster on average. '
    +'Turn collisions off and inject at a set temperature: every disk keeps the speed it came in with, and the histogram stays a spike. '
    +'The averaging (19 bins, 1 ps) is PhET&rsquo;s; the orange curves are the exact law at the thermometer&rsquo;s temperature.',
  diffusion:'Two gases, one on each side of a divider. Remove it and they mix, not because anything pushes them but because random walks spread out. '
    +'Each species crosses the middle at a rate set by its density and its mean speed; lighter molecules are faster, so they lead '
    +'(Graham&rsquo;s law: rate &prop; 1/&radic;m). Watch the centres of mass: they drift toward the middle and then jiggle about it. Set the two '
    +'species identical and the mixing still happens &mdash; that is the entropy of mixing, and nothing in the mechanics runs it backwards. '
    +'Change a mass or a starting temperature and, as in PhET, every particle of that species is reset to the one speed &radic;(3kT/m).',
  pressure:'Where does the gauge&rsquo;s number come from? Here the walls count: every bounce delivers 2m v&perp; of momentum, and the running total '
    +'divided by time and area is the pressure the wall actually feels. It is not PhET&rsquo;s NkT/V. Three factors separate them, each derived '
    +'and each measured: 3/2, because PhET assigns (3/2)kT to disks that move in only two dimensions; W/(W&minus;2r), because a disk&rsquo;s centre '
    +'cannot reach the last radius of the box; and Z, the push the collisions carry across the gas, which for hard disks is the exact virial '
    +'series 1 + B&#8322;&rho; + B&#8323;&rho;&sup2; + &hellip; Switch collisions off and Z = 1 exactly: the ideal gas law is what bouncing gives.',
  equil:'Start the gas far from equilibrium &mdash; every disk at one speed, or the heavy disks hot and the light ones cold, or all of them squirted in '
    +'at one point &mdash; and watch it forget. Boltzmann&rsquo;s H, the relative entropy of the energy histogram against e<sup>&minus;E/kT&#8322;</sup>, falls to '
    +'the floor that a finite sample of the exact law would show, (K&minus;1)/2N; the two species&rsquo; mean energies meet, whatever their masses '
    +'(equipartition). Nothing in the collision rule prefers the exponential: it is simply the shape almost every way of sharing a fixed energy '
    +'among the disks looks like. Turn collisions off and nothing relaxes at all.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  ideal:'<h4>PhET&rsquo;s gas law, in its units</h4>'
    +EQ(1,'T = '+FR('2','3')+' '+FR('&lang;KE&rang;','k')+', &nbsp; P = '+FR('N k T','V')+' &times; 1.66&times;10<sup>6</sup> kPa, &nbsp; V = w &times; 8750 pm &times; 4000 pm')
    +EQ(2,'k = 8316 AMU pm&sup2; ps<sup>&minus;2</sup> K<sup>&minus;1</sup> &nbsp;<span class="rm">(CODATA: 8314.46, +1.85&times;10<sup>&minus;4</sup>)</span>')
    +EQ(3,'<span class="rm">P&#8597;V:</span> w = '+FR('N k T','P H D')+' <span class="rm">(5 decimals)</span>; &nbsp; <span class="rm">P&#8597;T:</span> T = '+FR('P V','N k')+' <span class="rm">(every KE scaled)</span>')
    +EQ(4,'<span class="rm">pump:</span> |v| = &radic;(3kT<sub>i</sub>/m), &nbsp; T<sub>i</sub> ~ N(T, 0.2T) <span class="rm">with the mean restored</span>, &nbsp; &theta; &isin; [3&pi;/4, 5&pi;/4]')
    +EQ(5,'<span class="rm">heater:</span> v &rarr; v (1 + a/800)<sup>h/(1/24 ps)</sup>, &nbsp; a &isin; [&minus;1, 1] &nbsp;<span class="rm">(300 &rarr; 1000 K in 20.1 ps at full heat)</span>')
    +'<p>The gauge is 0 until the first wall hit, refreshes every 0.75 ps, and jitters by up to 50(1 &minus; P/20000) kPa (PhET&rsquo;s noise law). Above 20,000 kPa the lid blows off; at 10<sup>5</sup> K every particle is removed.</p>'
    +'<div class="cite">pins: PhET&rsquo;s constants, P = 1183.248 kPa for 100 at 300 K, the hold-constant laws to 10<sup>&minus;6</sup>, every Oops, the injection value by value (bit-exact mulberry32) &mdash; derive.py</div>',
  explore:'<h4>the moving wall</h4>'
    +EQ(1,'<span class="rm">contact:</span> x + v t &minus; r = x<sub>w</sub> + u t &nbsp;&rArr;&nbsp; t = '+FR('x<sub>w</sub> + r &minus; x','v &minus; u')+' &nbsp;<span class="rm">(needs v &lt; u)</span>')
    +EQ(2,'v&prime; = 2u &minus; v, &nbsp; &Delta;E = '+FR('m','2')+'(v&prime;&sup2; &minus; v&sup2;) = 2 m u (u &minus; v)')
    +EQ(3,'<span class="rm">slowly:</span> dE = &minus;F<sub>x</sub> dW, &nbsp; F<sub>x</sub>(W&minus;2r) = E Z(W) &nbsp;&rArr;&nbsp; ln '+FR('T<sub>1</sub>','T<sub>0</sub>')+' = &int;<sub>W<sub>1</sub></sub><sup>W<sub>0</sub></sup> '+FR('Z dW','W &minus; 2r'))
    +EQ(4,'<span class="rm">points (Z = 1, r = 0):</span> T W = <span class="rm">const</span>; &nbsp; <span class="rm">100 heavy, 10 &rarr; 7 nm:</span> T<sub>1</sub>W<sub>1</sub>/T<sub>0</sub>W<sub>0</sub> = 1.0691 <span class="rm">(points 1.0111)</span>')
    +EQ(5,'c = &radic;(&gamma;P/&rho;) = &radic;(2kT&#8322;/m) = 517 m/s <span class="rm">(heavy, 300 K)</span> &nbsp;&rArr;&nbsp; 800 m/s = Mach 1.55')
    +EQ(6,'<span class="rm">PhET&rsquo;s rule:</span> v&prime; = u &minus; v, &nbsp; &Delta;E = m u (u/2 &minus; v) &nbsp;&rArr;&nbsp; <span class="rm">half the work;</span> T V<sup>1/2</sup> = <span class="rm">const for points</span>')
    +'<p>Squeezed at 20 m/s, three runs of 100 heavy disks end at 1.0740, 1.0694 and 1.0650 against the hard-disk 1.0691; at 800 m/s the same squeeze ends near 3. The engine&rsquo;s wall work matches a brute-force event-driven run to the last digit (23,040,000 AMU pm&sup2;/ps&sup2; in the reference case).</p>'
    +'<div class="cite">pins: the contact time and the work in exact rationals; the reference run R2 (six disks, the wall at 300 m/s for 5 ps); the adiabat integral by scipy quad &mdash; derive.py</div>',
  energy:'<h4>Maxwell&ndash;Boltzmann in two dimensions</h4>'
    +EQ(1,'f(v<sub>x</sub>, v<sub>y</sub>) &prop; e<sup>&minus;m(v<sub>x</sub>&sup2;+v<sub>y</sub>&sup2;)/2kT&#8322;</sup> &nbsp;&rArr;&nbsp; f(v) = '+FR('m v','kT&#8322;')+' e<sup>&minus;mv&sup2;/2kT&#8322;</sup>, &nbsp; f(E) = '+FR('1','kT&#8322;')+' e<sup>&minus;E/kT&#8322;</sup>')
    +EQ(2,'kT&#8322; = &lang;E&rang; = &frac32; k T &nbsp;<span class="rm">(PhET&rsquo;s T)</span>, &nbsp; &lang;v&rang; = &radic;(&pi;kT&#8322;/2m), &nbsp; v<sub>mode</sub> = &radic;(kT&#8322;/m)')
    +EQ(3,'<span class="rm">300 K:</span> &lang;v&rang; = 458.19 m/s (heavy), 1212.25 m/s (light)')
    +EQ(4,'<span class="rm">closed box, N disks:</span> E<sub>i</sub>/E ~ Dirichlet(1,&hellip;,1), &nbsp; F(E<sub>i</sub>) = 1 &minus; (1 &minus; E<sub>i</sub>/E)<sup>N&minus;1</sup>')
    +'<p>The exact finite-N law is what the self-test uses: its moments give the tolerances (e.g. &lang;E&sup2;&rang;/&lang;E&rang;&sup2; = 2N/(N+1)), not a guess.</p>'
    +'<div class="cite">pins: PhET&rsquo;s bin probabilities at 300 K, the mean speeds (scipy quad), the Dirichlet moments and a Monte-Carlo chi-square quantile &mdash; derive.py</div>',
  diffusion:'<h4>effusion across the middle</h4>'
    +EQ(1,'<span class="rm">flux per unit length:</span> &Phi; = n &lang;v<sub>x</sub><sup>+</sup>&rang; = n &radic;(kT&#8322;/2&pi;m)')
    +EQ(2,FR('rate<sub>1</sub>','rate<sub>2</sub>')+' = '+FR('n<sub>1</sub>','n<sub>2</sub>')+' &radic;('+FR('m<sub>2</sub>','m<sub>1</sub>')+') &nbsp;<span class="rm">(equal T; Graham)</span>')
    +EQ(3,'x<sub>cm</sub> = &Sigma;m x / &Sigma;m, &nbsp; <span class="rm">reported from the centre;</span> &nbsp; rate = &Sigma;<sub>300 frames</sub> crossings / &Sigma; &Delta;t')
    +'<p>PhET places each species uniformly in its half with every particle at the one speed &radic;(3kT/m) in a random direction; collisions turn that spike into Maxwell&ndash;Boltzmann within a few collision times.</p>'
    +'<div class="cite">pins: &lang;v<sub>x</sub><sup>+</sup>&rang; at 300 K (145.85 and 385.87 m/s), Graham&rsquo;s &radic;7 &mdash; derive.py</div>',
  pressure:'<h4>the virial theorem, collision by collision</h4>'
    +EQ(1,FR('d','dt')+' &Sigma; m r&middot;v = 2 KE + &Sigma; r&middot;F &nbsp;&rArr;&nbsp; <span class="rm">over a run:</span> &Delta;G = &int;2KE dt + &Sigma;<sub>walls</sub> r&middot;J + &Sigma;<sub>pairs</sub> &sigma;|J|')
    +EQ(2,'F<sub>x</sub>(W&minus;2r) + F<sub>y</sub>(H&minus;2r) = 2E Z, &nbsp; Z = 1 + '+FR('&Sigma; &sigma;|J| / t','2E')+' &minus; '+FR('&Delta;G / t','2E'))
    +EQ(3,'Z = 1 + B&#8322;&rho; + B&#8323;&rho;&sup2; + &hellip;, &nbsp; B&#8322; = &pi;&sigma;&sup2;/2, &nbsp; B&#8323;/B&#8322;&sup2; = 4/3 &minus; &radic;3/&pi; = 0.78200')
    +EQ(4,'<span class="rm">finite box, first order:</span> Z &minus; 1 = (N&minus;1) &sigma; M / 4(ab)&sup2;, &nbsp; M = 2&pi;&sigma;ab &minus; 4&sigma;&sup2;(a+b) + 2&sigma;&sup3;')
    +EQ(5,'P<sub>wall</sub> = '+FR('F<sub>x</sub>','H D')+' = &frac32; '+FR('W','W&minus;2r')+' Z &middot; '+FR('NkT','V'))
    +'<p>The ledger [1] closes to about 10<sup>&minus;15</sup> of its terms, because every impulse is applied at its true contact point. For 90 heavy disks in the 10 nm box (&eta; = 0.050) the measured Z &minus; 1 is 0.110, against 0.1102 with B&#8323; and 0.1018 without: the simulation resolves the third virial coefficient. Past &eta; &asymp; 0.1 the terms beyond B&#8323; matter and the truncated series falls below the measurement (the literature&rsquo;s B&#8324; &asymp; 0.532 B&#8322;&sup3; is not re-derived here).</p>'
    +'<div class="cite">pins: B&#8323; by quadrature of the three-disk Mayer integral; M by quadrature and Monte Carlo; the ledger on the brute-force runs &mdash; derive.py</div>',
  equil:'<h4>why the exponential</h4>'
    +EQ(1,'H = &Sigma;<sub>k</sub> p<sub>k</sub> ln(p<sub>k</sub>/q<sub>k</sub>), &nbsp; q<sub>k</sub> = 1/K <span class="rm">over K = 12 bins of equal probability under</span> e<sup>&minus;E/kT&#8322;</sup>')
    +EQ(2,'<span class="rm">sampling floor:</span> &lang;H&rang; &asymp; (K &minus; 1)/2N <span class="rm">for N draws from the exact law</span>')
    +EQ(3,'<span class="rm">the energy shell:</span> &Sigma; E<sub>i</sub> = E <span class="rm">fixed, every point equally likely</span> &nbsp;&rArr;&nbsp; E<sub>i</sub>/E ~ Beta(1, N&minus;1) &rarr; e<sup>&minus;E<sub>i</sub>/&lang;E&rang;</sup>')
    +EQ(4,'&lang;E<sub>heavy</sub>&rang; = &lang;E<sub>light</sub>&rang; = E/N &nbsp;<span class="rm">(each disk has two quadratic degrees of freedom, whatever its mass)</span>')
    +'<p>The masses do not appear in [3] at all: a heavy disk and a light one hold the same share of the energy on average, which is equipartition, and the light one simply moves faster to hold it.</p>'
    +'<div class="cite">pins: the Dirichlet moments; equipartition from a 6:1 energy split, 40 seeds, to 0.2 sd &mdash; selfTest</div>'
};
