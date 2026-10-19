
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
  function clearOops(){ const w=WORLD[worldKey(st.view)]; if(w) w.g.oops=null; }
  /* the model changed without time passing: PhET's updateWhenPaused */
  const touched=()=>{ const g=G_(); if(!st.running) gasRefresh(g); };

  /* ---- the particles ---- */
  const gPart=h('div',{class:'grp'},h('h3',null,'the particles'));
  gPart.appendChild(slider('nH','heavy (28 AMU)',0,GAS.NMAX,1,v=>fmt(v,0),()=>{ gasSetCount(G_(),0,st.nH); touched(); syncCounts(); }));
  gPart.appendChild(slider('nL','light (4 AMU)',0,GAS.NMAX,1,v=>fmt(v,0),()=>{ gasSetCount(G_(),1,st.nL); touched(); syncCounts(); }));
  const pumpChips=chipRow(PUMPS,'pump'); gPart.appendChild(h('div',{class:'tag'},'the pump (drag its handle) pumps:')); gPart.appendChild(pumpChips); trackChips(pumpChips,PUMPS,'pump');
  gPart.appendChild(h('div',{class:'btnrow'},button('erase particles',()=>{ gasRemoveAll(G_()); touched(); })));
  const partTag=h('div',{class:'tag'}); gPart.appendChild(partTag);

  /* ---- hold constant (the Laws screen only: PhET's hasHoldConstantFeature) ---- */
  const gHold=h('div',{class:'grp'},h('h3',null,'hold constant'));
  const holdChips=chipRow(HOLDS,'hold',o=>{ const g=G_(); if(!gasSetHold(g,o.id)) st.hold=g.hold; });
  gHold.appendChild(holdChips); trackChips(holdChips,HOLDS,'hold');
  const holdTag=h('div',{class:'tag'}); gHold.appendChild(holdTag);

  /* ---- heat / cool: PhET's slider snaps back to zero when released ---- */
  const gHeat=h('div',{class:'grp'},h('h3',null,'heat / cool'));
  gHeat.appendChild(slider('heat','cool ← → heat',-1,1,0.01,v=>(v>0?'+':'')+fmt(v,2),null,()=>{ st.heat=0; }));
  const heatTag=h('div',{class:'tag'}); gHeat.appendChild(heatTag);

  /* ---- the container ---- */
  const gBox=h('div',{class:'grp'},h('h3',null,'the container'));
  const lidBtn=h('div',{class:'btnrow'},button('return lid',()=>{ gasReturnLid(G_()); touched(); }));
  gBox.appendChild(lidBtn);
  const boxTag=h('div',{class:'tag'}); gBox.appendChild(boxTag);

  /* ---- the sweep ---- */
  const gSweep=h('div',{class:'grp'},h('h3',null,'sweep a law'));
  const lawChips=chipRow(LAWS,'law',()=>{ W_().sweep=null; });
  gSweep.appendChild(lawChips); trackChips(lawChips,LAWS,'law');
  const restartS=()=>{ const w=W_(); w.sweep=null; resetWorld('sweep'); };
  gSweep.appendChild(slider('sN','disks at the start',20,400,10,v=>fmt(v,0),restartS));
  gSweep.appendChild(slider('sT','temperature at the start, K',100,600,50,v=>fmt(v,0)+' K',restartS));
  gSweep.appendChild(slider('sWin','counting window, ps',5,60,5,v=>fmt(v,0)+' ps'));
  const runBtn=h('button',{onclick:()=>{ clearOops(); const w=W_();
    if(w.sweep&&!w.sweep.done) w.sweep=null; else { sweepStart(w,st); st.running=true; }
    syncCounts(); syncChips(); syncPanel(); dirty=true; refresh(); }},'run the sweep');
  gSweep.appendChild(h('div',{class:'btnrow'},runBtn));
  const sweepTag=h('div',{class:'tag'}); gSweep.appendChild(sweepTag);

  /* ---- tools ---- */
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  const cbCounter=checkbox('showCounter','collision counter');
  gTools.appendChild(h('div',{class:'checks'},checkbox('showWidth','width'),checkbox('showWatch','stopwatch'),cbCounter));
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

  /* ---- time ---- */
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  gRun.appendChild(h('div',{class:'btnrow'},button('step 0.2 ps',()=>{ S.stepOnce(); }),
    button('reset this view',()=>{ resetView(); })));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Gases Intro (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s constants are read from its published build; the hard-disk engine is the one documented in build/gas-properties/ENGINE.md, and everything this sim adds &mdash; the one-sided flux, the wall-hit rate, the hard-disk contact measure and the four laws&rsquo; invariants &mdash; is derived in build/gases-intro/derive.py with scipy and pinned in selfTest.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gPart,gHold,gHeat,gBox,gSweep,gTools,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function resetView(){
    const v=st.view;
    if(v==='sweep'){ st.law=st.law; resetWorld('sweep'); WORLD.sweep.sweep=null; }
    else { st.heat=0; st.hold='nothing'; resetWorld(v); }
  }
  function syncCounts(){
    const g=G_(); st.nH=gasCount(g,0); st.nL=gasCount(g,1); st.hold=g.hold;
    if(rows.nH){ rows.nH.sync(); rows.nL.sync(); }
  }
  S.onCounts=()=>{ syncCounts(); };
  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const v=st.view, g=G_(), sweepV=(v==='sweep');
    gPart.hidden=sweepV; gHold.hidden=!(v==='laws'||v==='pv'); gHeat.hidden=sweepV;
    gBox.hidden=sweepV; gSweep.hidden=!sweepV;
    st.hold=g.hold;
    /* PhET's enabling: T needs particles and a closed lid; P needs a pressure */
    [].forEach.call(holdChips.children,(b,i)=>{ const ok=gasHoldAllowed(g,HOLDS[i].id); b.disabled=!ok; b.style.opacity=ok?'1':'0.4'; });
    const locked=heaterLocked({view:v,g});
    rows.heat.inp.disabled=locked; rows.heat.row.style.opacity=locked?'0.45':'1';
    lidBtn.hidden=!(g.lid&&!g.lid.on);
    watchBtns.hidden=!st.showWatch;
    counterBtns.hidden=!st.showCounter; periodChips.hidden=!st.showCounter;
    const S2=WORLD.sweep?WORLD.sweep.sweep:null;
    runBtn.textContent=(S2&&!S2.done)?'stop the sweep':'run the sweep';
    for(const k in rows) rows[k].sync();
    partTag.innerHTML='a full stroke of the pump adds 50; at most '+GAS.NMAX+' of each';
    holdTag.innerHTML=g.hold==='pressureV'?'the wall moves to keep P: V = NkT/P':g.hold==='pressureT'?'the temperature follows to keep P: T = PV/Nk':g.hold==='temperature'?'the heater is locked and the lid is shut':g.hold==='volume'?'the wall is locked':'change N, T or V and P answers';
    heatTag.innerHTML='PhET&rsquo;s heater scales every speed by 1 + a/800 per 60-fps frame; the slider springs back to zero when you let go';
    boxTag.innerHTML=g.lid&&g.lid.on?(gasLidOpen(g)?'the lid is open '+fmt(gasOpening(g)/1000,2)+' nm: particles that reach the gap leave':'drag the knob on the lid to open it'):'the lid blew off (P &gt; 20,000 kPa): return it';
    sweepTag.innerHTML='each step settles 2 ps, then counts wall hits for '+fmt(st.sWin,0)+' ps; the sweep runs '+SWEEP_BATCH+' model frames a frame so it takes seconds, not a minute';
    runTag.innerHTML='space runs/pauses &nbsp; <b>s</b> steps 0.2 ps &nbsp; <b>r</b> resets this view &nbsp; 1&ndash;4 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='sweep'?'press run the sweep · space pauses · 1–4 switch views'
        :'drag the wall grip, the lid knob or the pump · space pauses · 1–4 switch views';
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

  let frameN=0, lastHold=null, lastPhase=null;
  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        const g=G_();
        if(advanced&&frameN%10===0){ roEl.innerHTML=readoutHTML(S.model()); eqEl.innerHTML=eqbarHTML(S.model()); tagEl.innerHTML=tagHTML(S.model()); }
        /* a model-side change of the hold (an Oops) re-enables the panel; so
           does the sweep finishing */
        const S2=WORLD.sweep?WORLD.sweep.sweep:null, ph=S2?(S2.done?'done':S2.phase+S2.i):null;
        if(g.hold!==lastHold||ph!==lastPhase){ lastHold=g.hold; lastPhase=ph; st.hold=g.hold; syncChips(); syncPanel(); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncCounts(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  intro:'PhET&rsquo;s Intro screen. A box of hard disks &mdash; heavy ones like nitrogen (28 AMU) and light ones like helium (4 AMU) &mdash; bouncing off each '
    +'other and the walls without losing any energy. Pump some in, heat or cool them from below, slide the left wall, or open the lid and watch the fast ones escape first. '
    +'The thermometer reads PhET&rsquo;s temperature, T = (2/3)&lang;KE&rang;/k, and the gauge PhET&rsquo;s pressure, P = NkT/V: both are <i>definitions</i>, so PV = NkT here is arithmetic, not a discovery. '
    +'The collision counter is different. Nothing defines how often the disks hit the walls; that follows from how fast they move and how much room they have, and kinetic theory says the rate is '
    +'2 n Z &lang;v&rang;/&pi; (a + b). The plot on the right compares the two, with the counting error shown, and the dashed line is what the rate would be if the disks never met each other.',
  laws:'PhET&rsquo;s Laws screen: the same box, plus the Hold Constant panel. The whole point of the screen is that PV = NkT has three free quantities and you may only fix one at a time. '
    +'Hold V and heat: P climbs with T (Gay-Lussac). Hold T and squeeze: P climbs as 1/V (Boyle). Hold P and heat: the wall walks out, V in step with T (Charles). Hold P and pump: '
    +'the temperature falls to make room (Avogadro, at fixed P and V). The left plot shows the quantities that are still free, each divided by its value when you started, so the one that '
    +'stays flat is the one being held. The right plot is the held invariant itself, in parts per million &mdash; that is the controller&rsquo;s own arithmetic error, and it should be a flat line at zero. '
    +'Ask for the impossible &mdash; hold T in an empty box, or hold P when the container would have to be wider than 15 nm &mdash; and you get PhET&rsquo;s Oops.',
  pv:'The same gas as the Laws screen, drawn where a chemist would draw it: one point on the pressure&ndash;volume plane. The orange hyperbolas are isotherms, P = NkT/V at fixed T, '
    +'and they move outward as you pump because N is in the numerator. Now hold something and act. Hold T and drag the wall: the point slides <i>along</i> one hyperbola, which is Boyle&rsquo;s law drawn rather than stated. '
    +'Hold V and heat: it climbs straight up, crossing the isotherms, which is Gay-Lussac. Hold P and heat: it runs horizontally across them, which is Charles. The green line is everything the gas has actually done since you '
    +'last reset it, so the shape of the path <i>is</i> the law you chose.',
  sweep:'The four named laws, measured rather than asserted. Pick one and press run: the sim engages PhET&rsquo;s hold, steps the controlled variable to five targets, lets the gas settle for 2 ps, '
    +'then counts wall hits for the counting window. The left plot puts the five measured states on the exact line. They land on it &mdash; and they have to, because PhET <i>defines</i> P = NkT/V, so the only thing that could '
    +'go wrong is the controller, and the readout prints how far the invariant actually moved (about a part in 10<sup>9</sup>, which is PhET rounding the held-pressure width to five decimals). '
    +'The right plot is the honest half. The wall-hit rate is not defined into existence: it depends on the density, the mean speed and how much the collisions crowd the disks against the walls. '
    +'Sweep Boyle and watch it climb as the box narrows; sweep Gay-Lussac and watch it grow as &radic;T. The error bars are &radic;n/t, so widen the counting window if they are wider than the gap between the two orange curves.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  intro:'<h4>PhET&rsquo;s gas law, and the one number it does not fix</h4>'
    +EQ(1,'T = '+FR('2','3')+' '+FR('&lang;KE&rang;','k')+', &nbsp; P = '+FR('N k T','V')+' &times; 1.66&times;10<sup>6</sup> kPa, &nbsp; V = w &times; 8750 pm &times; 4000 pm')
    +EQ(2,'k = 8316 AMU pm&sup2; ps<sup>&minus;2</sup> K<sup>&minus;1</sup> &nbsp;<span class="rm">(CODATA k<sub>B</sub>/u: 8314.46, +1.85&times;10<sup>&minus;4</sup>)</span>')
    +EQ(3,'&lang;v<sub>x</sub><sup>+</sup>&rang; = &int;<sub>0</sub><sup>&infin;</sup> v<sub>x</sub> f(v<sub>x</sub>) dv<sub>x</sub> = &radic;('+FR('kT&#8322;','2&pi;m')+') = '+FR('&lang;v&rang;','&pi;')+' &nbsp;<span class="rm">(exactly)</span>')
    +EQ(4,'<span class="rm">hits/ps</span> = 2 n Z &lang;v<sub>x</sub><sup>+</sup>&rang; (a + b), &nbsp; a = W &minus; 2r, &nbsp; b = H &minus; 2r, &nbsp; n = N/ab')
    +EQ(5,'Z = 1 + '+FR('(N&minus;1) &sigma; M','4(ab)&sup2;')+'&middot;(1 + '+FR('B&#8323;','B&#8322;&sup2;')+' '+FR('B&#8322; N','ab')+'), &nbsp; '+FR('B&#8323;','B&#8322;&sup2;')+' = '+FR('4','3')+' &minus; '+FR('&radic;3','&pi;')+' = 0.78200')
    +EQ(6,'M = 2&pi;&sigma;ab &minus; 4&sigma;&sup2;(a+b) + 2&sigma;&sup3;, &nbsp; B&#8322; = '+FR('&pi;&sigma;&sup2;','2')+', &nbsp; &sigma; = 2r')
    +'<p>[4] is [3] times the density of centres at the wall, over the perimeter their centres can reach; [5] raises that density because hard disks crowd each other against the wall. For 100 heavy disks at 300 K in the 10 nm box the rate is 6.4234/ps with Z = 1 and 7.2178/ps with Z &mdash; a 12.4 % difference the counter can see.</p>'
    +'<div class="cite">pins: &lang;v<sub>x</sub><sup>+</sup>&rang; by scipy quad; the hit rate three ways (the flux form, the per-particle form |v<sub>x</sub>|/a, and a free-flight run of 4000 disks); M term by term, the +2&sigma;&sup3; from the four corner integrals &mdash; derive.py</div>',
  laws:'<h4>the four holds, and what each keeps</h4>'
    +EQ(1,'<span class="rm">hold V:</span> '+FR('P','T')+' = '+FR('N k','V')+' &nbsp;<span class="rm">(Gay-Lussac)</span> &nbsp;&middot;&nbsp; <span class="rm">hold T:</span> P V = N k T &nbsp;<span class="rm">(Boyle)</span>')
    +EQ(2,'<span class="rm">hold P by moving the wall:</span> w = '+FR('N k T','P H D')+' <span class="rm">(rounded to 5 decimals)</span> &nbsp;&rArr;&nbsp; '+FR('V','T')+' <span class="rm">const (Charles)</span>')
    +EQ(3,'<span class="rm">hold P by changing T:</span> T = '+FR('P V','N k')+' <span class="rm">(every KE scaled)</span> &nbsp;&rArr;&nbsp; N T <span class="rm">const (Avogadro)</span>')
    +EQ(4,'<span class="rm">the container:</span> 5000 &le; w &le; 15000 pm &nbsp;&rArr;&nbsp; at P and N fixed, 150 K &le; T &le; 450 K <span class="rm">(else: Oops)</span>')
    +'<p>PhET&rsquo;s setTemperature multiplies every kinetic energy by the same factor, so the temperature it reaches is exact, and the resize does no work, so Boyle&rsquo;s invariant is exact too. The only departure is the five-decimal rounding of the held-pressure width, about a part in 10<sup>9</sup>.</p>'
    +'<div class="cite">pins: the four invariants at five sweep points each, and the 150&ndash;450 K window the container allows &mdash; derive.py</div>',
  pv:'<h4>the isotherm</h4>'
    +EQ(1,'P(V) = '+FR('N k T','V')+' &nbsp;&rArr;&nbsp; <span class="rm">an isotherm is a hyperbola; doubling N doubles it everywhere</span>')
    +EQ(2,'<span class="rm">100 disks at 300 K:</span> 2366.5 kPa at 175 nm&sup3;, 1183.2 at 350, 788.8 at 525')
    +EQ(3,'<span class="rm">the path:</span> hold T &rarr; along one curve; hold V &rarr; straight up; hold P &rarr; straight across')
    +'<p>V is the full three-dimensional volume w &times; 8.75 nm &times; 4 nm, so the axis is linear in the width the wall shows: 175 nm&sup3; at 5 nm, 525 nm&sup3; at 15 nm.</p>'
    +'<div class="cite">pins: the isotherms at 150, 300, 600 and 1000 K, at three widths each, to 17 digits &mdash; derive.py</div>',
  sweep:'<h4>what a sweep can and cannot test</h4>'
    +EQ(1,'<span class="rm">Boyle:</span> P V &nbsp;&middot;&nbsp; <span class="rm">Charles:</span> V/T &nbsp;&middot;&nbsp; <span class="rm">Gay-Lussac:</span> P/T &nbsp;&middot;&nbsp; <span class="rm">Avogadro:</span> N T')
    +EQ(2,'<span class="rm">each is exact because</span> P &equiv; NkT/V <span class="rm">; the measurement is of the CONTROLLER</span>')
    +EQ(3,'<span class="rm">the hit rate is not:</span> 2 n Z &lang;v&rang;/&pi; (a + b), <span class="rm">error</span> &radic;n / t')
    +EQ(4,'<span class="rm">Boyle:</span> hits &prop; '+FR('1','a')+' + '+FR('1','b')+' <span class="rm">as the box narrows;</span> &nbsp; <span class="rm">Gay-Lussac:</span> hits &prop; &radic;T')
    +'<p>A sweep of 5 points with a 20 ps window counts a few hundred hits a point, so the error bar is a few per cent &mdash; about the size of the Z correction. Widen the window to separate them.</p>'
    +'<div class="cite">pins: the four invariants; the hit rate at each swept state against derive.py&rsquo;s closed form &mdash; selfTest</div>'
};
