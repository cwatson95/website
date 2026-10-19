
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
function resetAllState(){
  const v=ST.view; Object.assign(ST,DEFAULTS); ST.view=v;
  benchReset(BENCH); sysReset(SYS,ST); DRAG.what=null; DRAG.k=null;
  for(const k in MEMO) delete MEMO[k];
}
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

  function setView(k){
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; if(onPick) onPick(o,was); else st[key]=o.id;
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},label); }

  /* ---- the bench: presets, the burners (heat/cool, linkable), energy symbols ---- */
  const gBench=h('div',{class:'grp'},h('h3',null,'the bench'));
  const presetChips=chipRow(BENCH_PRESETS,'preset',o=>{ st.preset=o.id; benchPreset(BENCH,st,o.id); });
  gBench.appendChild(presetChips);
  const levFmt=v=>v>0?'heat '+fmt(v,2):(v<0?'cool '+fmt(-v,2):'off');
  gBench.appendChild(slider('lev0','left burner',-1,1,0.01,levFmt,()=>{ if(st.link) st.lev1=st.lev0; }));
  gBench.appendChild(slider('lev1','right burner',-1,1,0.01,levFmt,()=>{ if(st.link) st.lev0=st.lev1; }));
  gBench.appendChild(h('div',{class:'checks'},checkbox('link','link heaters',()=>{ if(st.link) st.lev1=st.lev0; }),checkbox('symBench','energy symbols')));
  const benchTag=h('div',{class:'tag'}); gBench.appendChild(benchTag);

  /* ---- the chain: a source, a converter, a user ---- */
  const gChain=h('div',{class:'grp'},h('h3',null,'the chain'));
  const srcChips=chipRow(SOURCES,'src',o=>sysSelect(SYS,st,'src',o.id)); gChain.appendChild(srcChips);
  gChain.appendChild(slider('pedal','pedalling',0,1,0.01,v=>fmt(v*OMEGA_MAX,2)+' rad/s'));
  gChain.appendChild(slider('flow','water flow',0,1,0.01,v=>fmt(v*MAXP/1000,1)+' kW'));
  gChain.appendChild(slider('clouds','clouds',0,1,0.01,v=>v===0?'none':(v===1?'lots':fmt(v,2))));
  gChain.appendChild(slider('heat','teapot burner',0,1,0.01,v=>fmt(v*MAXP/1000,1)+' kW'));
  const feedRow=h('div',{class:'btnrow'},btn('feed me',()=>{ sysFeed(SYS); }));
  gChain.appendChild(feedRow);
  const convChips=chipRow(CONVERTERS,'conv',o=>sysSelect(SYS,st,'conv',o.id)); gChain.appendChild(convChips);
  const userChips=chipRow(USERS,'user',o=>sysSelect(SYS,st,'user',o.id)); gChain.appendChild(userChips);
  gChain.appendChild(h('div',{class:'checks'},checkbox('symSys','energy symbols (systems)')));
  const chainTag=h('div',{class:'tag'}); gChain.appendChild(chainTag);

  /* ---- equilibrium: the pair, the materials, the two temperatures, the room ---- */
  const gPair=h('div',{class:'grp'},h('h3',null,'the pair'));
  gPair.appendChild(chipRow(EQ_PAIRS,'eqPair'));
  gPair.appendChild(chipRow(EQ_MATS,'eqMat'));
  const kFmt=v=>fmt(v,2)+' K';
  gPair.appendChild(slider('eqT1','hot block',T_FREEZE,T_BLOCK_MAX,0.05,kFmt));
  gPair.appendChild(slider('eqT2','its partner',T_FREEZE,T_BOIL.water,0.05,kFmt));
  gPair.appendChild(h('div',{class:'checks'},checkbox('eqAir','the room takes heat')));
  const pairTag=h('div',{class:'tag'}); gPair.appendChild(pairTag);

  /* ---- time ---- */
  const stepView=()=>{ if(st.view==='bench'||st.view==='ledger'){ BENCH.acc=0; benchStep(BENCH,burnerLevels(st)); } else if(st.view==='sys'||st.view==='flow'){ SYS.acc_t=0; sysStep(SYS,st); } };
  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const speedChips=chipRow(SPEED_LIST,'speed'); gTime.appendChild(speedChips);
  gTime.appendChild(h('div',{class:'btnrow'},btn('step',stepView),btn('reset all',()=>{ resetAllState(); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Energy Forms and Changes (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets. PhET&rsquo;s values (specific heats, densities, sizes, the heat-transfer constants 1000 and 30 W/(m&middot;K), the burners&rsquo; 5000 and 1500 W, '
      +'the 10-kW rates, ENERGY_PER_CHUNK) are read from its build 1.4.24 and its doc/model.md. Real materials: NIST Chemistry WebBook (water, IAPWS-95, 296 K), NIST-JANAF (iron), '
      +'Arblaster 2018 (iron&rsquo;s density), Engineering ToolBox and Wikipedia&rsquo;s tables (brick, olive oil), the USDA grading manual (olive oil&rsquo;s density). '
      +'Everything else is exact and pinned in selfTest to build/energy-forms-and-changes/derive.py.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gBench,gChain,gPair,gTime,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [w,list,key] of CHIPROWS) [].forEach.call(w.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row the view ignores is hidden, never left live and inert (Known-bad) */
  function syncPanel(){
    const v=st.view, bench=(v==='bench'||v==='ledger'), chain=(v==='sys'||v==='flow');
    gBench.hidden=!bench; gChain.hidden=!chain; gPair.hidden=(v!=='eq'); gTime.hidden=(v==='eq');
    speedChips.hidden=!bench;
    rows.pedal.row.hidden=st.src!=='biker'; rows.flow.row.hidden=st.src!=='faucet';
    rows.clouds.row.hidden=st.src!=='sun'; rows.heat.row.hidden=st.src!=='teapot';
    feedRow.hidden=!(st.src==='biker'&&SYS.food<=0);
    for(const k in rows) rows[k].sync();
    const lev=burnerLevels(st);
    benchTag.innerHTML='drag the bodies and thermometers on the bench; the levers on the burners drag too'+(st.link?' &nbsp; (linked: one lever drives both)':'')
      +'<br>left '+levFmt(lev[0])+', right '+levFmt(lev[1]);
    chainTag.innerHTML=srcName(st.src)+' &rarr; '+convName(st.conv)+' &rarr; '+userName(st.user)
      +(convTakes(st.conv,st.src)?'':' &nbsp; <span class="r">the '+convName(st.conv)+' cannot use '+srcForm(st.src)+' energy</span>');
    pairTag.innerHTML='the block starts hot, its partner at the second temperature; T<sub>eq</sub> assumes the room shut out';
    timeTag.innerHTML='space runs/pauses &nbsp; <b>.</b> steps 1/60 s &nbsp; <b>r</b> resets all &nbsp; 1&ndash;5 switch views';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=st.view==='bench'?'drag bodies, levers, thermometers · space pauses':(st.view==='eq'?'1–5 switch views':'space pauses · 1–5 switch views');
      infoEl.innerHTML=INFO[st.view]||''; physEl.innerHTML=DERIV[st.view]||'';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; if(DRAG.what==='lever'){ for(const k of ['lev0','lev1']) rows[k].sync(); } }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='.'){ stepView(); dirty=true; refresh(); }
    else if(e.key==='r'){ resetAllState(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0, last=0, fed=SYS.food<=0;
  function frameLoop(tm){
    frameN++;
    const dtw=last?Math.min((tm-last)/1000,0.05):0; last=tm;
    const advanced=S.step(dtw);
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    if((SYS.food<=0)!==fed){ fed=SYS.food<=0; syncPanel(); }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  bench:'This is PhET&rsquo;s first screen, and its model to the digit. Every body carries energy E = mcT, and every sixtieth of a second each pair that touches '
    +'trades heat in proportion to the difference in their temperatures and to the length of their contact: a block stacked on a block touches along its 4.5-cm width, '
    +'a block dropped into a beaker touches the liquid all round, and everything touches the room. A burner pushes 5000 W times its lever into whatever sits on it, '
    +'or 1500 W into the room if nothing does; cooling stops at 0 &deg;C, because freezing is not in the model. Heat the iron and it passes 300 &deg;C in '
    +'21 seconds; drop it in the water and the two meet at their heat-capacity-weighted mean within seconds, then drift together back to the room&rsquo;s 22.85 &deg;C. '
    +'The red squares are PhET&rsquo;s energy chunks, each 5019 J, and they move only when energy does: along the contact that carried it, down from a flame, up into the room.',
  sys:'PhET&rsquo;s second screen: energy from a source is converted and used. The faucet&rsquo;s falling water or the teapot&rsquo;s steam turns a water wheel that drives a '
    +'generator; the cyclist turns it through a belt; sunlight falls on a solar panel. The electricity lights a bulb, warms a beaker of water or spins a fan. Pick the '
    +'wrong converter and nothing arrives: a generator cannot use sunlight, and a solar panel cannot use water. The chunks show each form as it travels: grey mechanical, '
    +'blue electrical, red thermal, yellow light, green chemical. Heat leaks at every step, which is why the chunks that reach the bulb are fewer than the ones that left the '
    +'source. The cyclist eats: 21 chunks of food last about 13.5 seconds at full pedalling with the generator attached, and then the rider needs feeding. The rates are PhET&rsquo;s; '
    +'where PhET&rsquo;s own numbers do not add up, the teapot and the cyclist chief among them, this version keeps the ledger closed (the header says how).',
  ledger:'The first law of thermodynamics for the bench, as bookkeeping. Three accounts run at once: the work the burners have done, the energy the bodies have gained, '
    +'and the energy the room has taken. The law says that the bodies&rsquo; gain plus the room&rsquo;s intake is exactly the burners&rsquo; work, and the readout prints '
    +'the difference: it stays at the level of rounding, a few parts in 10<sup>16</sup> of the energies each step and about 10<sup>&minus;14</sup> of them after half a minute '
    +'of heating. The chunks obey a second, exact identity. PhET moves a '
    +'chunk along a contact once more than 5019 J has crossed it, and this version adds a correction so that no body is ever a whole chunk away from the count its energy '
    +'deserves. So the change in each body&rsquo;s energy, counting what has crossed its contacts but not yet ridden a chunk, is exactly 5019 J times the change in its chunks. The staircase on the right shows '
    +'the chunks tracking PhET&rsquo;s map as the energies move.',
  flow:'The chain as a Sankey diagram, in watts. The supply enters at the left; at each element the bands leaving it (on to the next element, into a store, or away as heat) '
    +'add up to the band that arrived. The stores are real: water takes 0.4 s to fall from the faucet, the teapot&rsquo;s kettle fills before it steams, the water wheel '
    +'spins up over PhET&rsquo;s 5/3-second lag, and the heater&rsquo;s water holds what it has been given. Close the faucet and the stores empty through the chain for a '
    +'while, still on the ledger. The strip below is the running total. Everything that came in is either delivered (light, wind), lost (heat, light sent back by clouds, '
    +'energy the converter could not use) or still stored, and the three add up to the input to the last digit.',
  eq:'Two bodies in contact and nothing else: what temperature do they end at, and how fast? With the room shut out, energy is conserved, so the final temperature is the '
    +'heat-capacity-weighted mean, T<sub>eq</sub> = (C<sub>1</sub>T<sub>1</sub> + C<sub>2</sub>T<sub>2</sub>)/(C<sub>1</sub> + C<sub>2</sub>). The difference between them '
    +'decays as e<sup>&minus;t/&tau;</sup>, with &tau; = 1/[kL(1/C<sub>1</sub> + 1/C<sub>2</sub>)]. PhET&rsquo;s contact is fast: an iron block in water settles in about '
    +'a second. The solid curves are PhET&rsquo;s model, stepped 60 times a second; the orange halos are the exact solution of the same equations, and the gap between them is '
    +'the cost of the step, under 0.4 % of the starting difference. With the room let in, both bodies then drift to 296 K on a slower clock. Switch to the real materials and water&rsquo;s '
    +'heat capacity grows by 39 %, because PhET&rsquo;s 3000 J/(kg&middot;K) is not water&rsquo;s 4182, and the brick loses more than a third of its mass: T<sub>eq</sub> moves.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  bench:'<h4>PhET&rsquo;s step, in order</h4>'
    +EQ(1,'E = m c T, &nbsp; T = '+FR('E','mc')+' &nbsp;<span class="rm">(a beaker stops at its boiling point)</span>')
    +EQ(2,'&Delta;E<sub>a</sub> = &minus;&Delta;E<sub>b</sub> = k L (T<sub>b</sub> &minus; T<sub>a</sub>) &Delta;t, &nbsp; k = 1000 W/(m&middot;K)')
    +EQ(3,'<span class="rm">burner:</span> 5000 &times; lever W <span class="rm">into what sits on it, else</span> 1500 &times; lever W <span class="rm">into the room</span>')
    +EQ(4,'<span class="rm">room:</span> &Delta;E = &minus;30 &times; (2w + 2h)(T &minus; 296 K) &Delta;t <span class="rm">for every body not immersed</span>')
    +'<p>L is the length of contact: a stacked pair&rsquo;s overlap (4.5 cm), an immersed block&rsquo;s wetted perimeter (18 cm). A block in a beaker raises the level by '
    +'120 &times; its submerged area (m<sup>2</sup>). Energy past a block&rsquo;s 620 K, or past a liquid&rsquo;s boiling point, leaves for the room.</p>'
    +'<div class="cite">pins: masses, heat capacities, contact lengths, six scenarios step by step (heating, immersion, stacking and cooling, boiling, the 620-K cap, the 0-&deg;C clamp) &mdash; derive.py</div>',
  sys:'<h4>the rates, PhET&rsquo;s, and the ledger</h4>'
    +EQ(1,'E<sub>in</sub> = E<sub>out</sub> + E<sub>lost</sub> + &Delta;E<sub>stored</sub> <span class="rm">at every element, every step</span>')
    +EQ(2,'<span class="rm">cyclist:</span> P<sub>food</sub> = 10 kW &times; &omega;/3&pi; <span class="rm">(2 kW with no load)</span>, &nbsp; '+FR('5','6')+' <span class="rm">to the pedals</span>')
    +EQ(3,'<span class="rm">generator on water or steam:</span> &eta; = '+FR('0.039 &times; 0.5 &times; (1/60)','3')+' &times; '+FR('10 kW','&pi;/2')+' = '+FR('13','6&pi;')+' = 68.97 %')
    +EQ(4,'<span class="rm">teapot:</span> '+FR('dE<sub>kettle</sub>','dt')+' = 0.8 P<sub>burner</sub> &minus; '+FR('E<sub>kettle</sub>','10 s')+', &nbsp; <span class="rm">steam</span> = '+FR('E<sub>kettle</sub>','10 s'))
    +EQ(5,'<span class="rm">sun through clouds c:</span> 10 kW &times; (0.1 + 0.9(1 &minus; c)), <span class="rm">none at c = 1; panel 68 %</span>')
    +'<p>PhET&rsquo;s teapot settles at 20 kW &times; heat of steam from 10 kW &times; heat of burner, and its generator&rsquo;s efficiency depends on the frame rate; the remake keeps the '
    +'rates that close (the header lists each change).</p><div class="cite">pins: nine chains, the stores, every channel&rsquo;s chunk count, PhET&rsquo;s fan counter &mdash; derive.py</div>',
  ledger:'<h4>the first law, and the chunks</h4>'
    +EQ(1,'&Delta;E<sub>bodies</sub> + E<sub>room</sub> = W<sub>burners</sub> &nbsp;<span class="rm">(each step, to rounding)</span>')
    +EQ(2,'g(E) = 1.25 + '+FR('E &minus; E<sub>brick</sub>(273.15 K)','EPC')+', &nbsp; EPC = '+FR('E<sub>brick</sub>(296 K) &minus; E<sub>brick</sub>(273.15 K)','1.15')+' = 5019.02 J')
    +EQ(3,'E<sub>i</sub> + &Sigma;<sub>links</sub> B<sub>i&rarr;</sub> &minus; EPC &middot; n<sub>i</sub> = <span class="rm">constant</span>, &nbsp; |n<sub>i</sub> &minus; g(E<sub>i</sub>)| &lt; 1')
    +'<p>B is the energy that has crossed a link and not yet been carried by a chunk. PhET moves a chunk when |B| &gt; EPC; the correction moves one when a body strays a whole chunk from g(E). '
    +'Either way B changes by EPC as the chunk moves, so [3] is exact.</p><div class="cite">pins: the identity for every body over every scenario, and |n &minus; g| &lt; 1 at every step &mdash; derive.py</div>',
  flow:'<h4>the chain&rsquo;s ledger</h4>'
    +EQ(1,'IN = OUT + LOST + STORED')
    +EQ(2,'IN = <span class="rm">water + sunlight + gas + food burned</span>, &nbsp; OUT = <span class="rm">light + wind</span>')
    +EQ(3,'STORED = <span class="rm">falling water + kettle + wheel + the heater&rsquo;s water above 296 K</span>')
    +'<p>Swapping an element out empties its store into the room as heat, and bringing the cyclist back refills his food: both are logged, so the ledger closes across a swap too.</p>'
    +'<div class="cite">pins: the global ledger to 1e&minus;12 of the input over every chain, and every element&rsquo;s own &mdash; derive.py</div>',
  eq:'<h4>two bodies and the room</h4>'
    +EQ(1,'C<sub>1</sub>T&#775;<sub>1</sub> = &minus;G(T<sub>1</sub> &minus; T<sub>2</sub>) &minus; a<sub>1</sub>(T<sub>1</sub> &minus; T<sub>room</sub>)')
    +EQ(2,'C<sub>2</sub>T&#775;<sub>2</sub> = &minus;G(T<sub>2</sub> &minus; T<sub>1</sub>) &minus; a<sub>2</sub>(T<sub>2</sub> &minus; T<sub>room</sub>)')
    +EQ(3,'T(t) = T<sub>ss</sub> + e<sup>Mt</sup>(T(0) &minus; T<sub>ss</sub>), &nbsp; e<sup>Mt</sup> = e<sup>st</sup>[cosh qt &middot; I + '+FR('sinh qt','q')+'(M &minus; sI)]')
    +EQ(4,'a = 0: &nbsp; T<sub>eq</sub> = '+FR('C<sub>1</sub>T<sub>1</sub> + C<sub>2</sub>T<sub>2</sub>','C<sub>1</sub> + C<sub>2</sub>')+', &nbsp; &tau; = '+FR('1','G(1/C<sub>1</sub> + 1/C<sub>2</sub>)'))
    +'<p>G = kL is the contact&rsquo;s conductance and a = 30 W/(m&middot;K) times a body&rsquo;s perimeter its conductance to the room (none for an immersed block). '
    +'s = tr M/2 and q = &radic;(s&sup2; &minus; det M): M is a symmetric matrix scaled by the heat capacities, so its eigenvalues are real.</p>'
    +'<div class="cite">pins: T<sub>eq</sub> and &tau; for every pair in both materials; the closed-form exponential against scipy.linalg.expm; stepped against exact at four times &mdash; derive.py</div>',
};
