
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
  const W_=()=>worldOf(), G_=()=>worldOf().g;

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab)); });

  const rows={};
  function slider(key,lab,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(c.disabled) return;
        st[key]=o.id; if(onPick) onPick(o);
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS=[];
  function trackChips(el,list,key){ CHIPROWS.push([el,list,key]); }
  function button(lab,fn){ return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},lab); }
  /* PhET's updateWhenPaused: a change made with the clock stopped still shows */
  const touched=()=>{ if(!st.running) gasRefresh(G_()); };

  /* ---- the two species: PhET's own grids (10, 1, 5, 50) ---- */
  const gDiff=h('div',{class:'grp'},h('h3',null,'the two gases'));
  const presetChips=chipRow(PRESETS,'preset',o=>{
    st.d1n=o.a.n; st.d1m=o.a.m; st.d1r=o.a.r; st.d1T=o.a.T;
    st.d2n=o.b.n; st.d2m=o.b.m; st.d2r=o.b.r; st.d2T=o.b.T;
    st.divided=true; resetWorld();
  });
  gDiff.appendChild(presetChips); trackChips(presetChips,PRESETS,'preset');
  const diffCount=k=>()=>{ gasDiffCount(G_(),k,k?st.d2n:st.d1n,k?st.d2T:st.d1T); touched(); };
  const diffMT=k=>()=>{ gasDiffMassTemp(G_(),k,k?st.d2m:st.d1m,k?st.d2T:st.d1T); touched(); };
  const diffR=k=>()=>{ gasDiffRadius(G_(),k,k?st.d2r:st.d1r,st.running); touched(); };
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
  const speciesTag=h('div',{class:'tag'}); gDiff.appendChild(speciesTag);

  /* ---- the divider ---- */
  const gDiv=h('div',{class:'grp'},h('h3',null,'the divider'));
  const divBtn=h('button',{onclick:()=>{ const w=W_();
    if(w.g.divided) removeDivider(w,st); else resetDivider(w,st);
    syncChips(); syncPanel(); dirty=true; refresh(); }},'remove divider');
  gDiv.appendChild(h('div',{class:'btnrow'},divBtn));
  const divTag=h('div',{class:'tag'}); gDiv.appendChild(divTag);

  /* ---- what is drawn ---- */
  const gShow=h('div',{class:'grp'},h('h3',null,'what is drawn'));
  gShow.appendChild(h('div',{class:'checks'},checkbox('dCOM','centre of mass'),checkbox('dFlow','particle flow rate'),
                                             checkbox('dScale','scale'),checkbox('showWatch','stopwatch')));
  gShow.appendChild(h('div',{class:'checks'},checkbox('showMB','Maxwell–Boltzmann curves')));
  const watchBtns=h('div',{class:'btnrow'},button('stopwatch start / stop',()=>{ const g=G_(); g.watch.on=!g.watch.on; }),
                                           button('reset',()=>{ const g=G_(); g.watch.on=false; g.watch.t=0; }));
  gShow.appendChild(watchBtns);
  const unitTChips=chipRow(UNITS_T,'unitT'); gShow.appendChild(unitTChips); trackChips(unitTChips,UNITS_T,'unitT');

  /* ---- time ---- */
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const speedChips=chipRow(SPEEDS,'slow'); gRun.appendChild(speedChips); trackChips(speedChips,SPEEDS,'slow');
  gRun.appendChild(h('div',{class:'btnrow'},button('step 0.2 ps',()=>{ S.stepOnce(); }),
    button('restart',()=>{ st.divided=true; resetWorld(); })));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Diffusion (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s constants and control grids are read from its published build; the hard-disk engine is the one documented in build/gas-properties/ENGINE.md, and everything this sim measures against &mdash; '
      +'the starting centre of mass, the one-sided flux, the effusion time constant, the mixture&rsquo;s collision frequency and the &radic;(&pi;/4) drop in the mean speed &mdash; is derived in build/diffusion/derive.py with scipy and pinned in selfTest.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gDiff,gDiv,gShow,gRun,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':'')+(b.disabled?' off':''));
  }
  function syncPanel(){
    const g=G_(), v=st.view;
    divBtn.textContent=g.divided?'remove divider':'reset divider';
    watchBtns.hidden=!st.showWatch;
    rows.cb_showMB.row.hidden=(v!=='speeds');
    rows.cb_dFlow.row.hidden=(v!=='box');
    rows.cb_dCOM.row.hidden=(v!=='box');
    for(const k in rows) rows[k].sync();
    speciesTag.innerHTML='PhET&rsquo;s own grids: number in tens, mass in ones, radius in fives, temperature in fifties. Changing a mass or a starting temperature resets every particle of that species to &radic;(3kT/m), as PhET does.';
    divTag.innerHTML=g.divided?'drag the handle on top of the divider, or press the button'
      :'reset it and PhET regenerates both species in their own halves &mdash; the run starts over';
    runTag.innerHTML='space runs/pauses &nbsp; <b>s</b> steps 0.2 ps &nbsp; <b>r</b> restarts &nbsp; 1&ndash;4 switch views'
      +(st.slow?' &nbsp; (slow: PhET&rsquo;s 0.3 ps a second)':'');
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=G_().divided?'drag the handle on the divider to lift it out · space pauses · 1–4 switch views'
        :'space pauses · s steps · 1–4 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncPanel(); dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='s'){ S.stepOnce(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ st.divided=true; resetWorld(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0, lastDiv=null;
  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        if(advanced&&frameN%10===0){ const M=S.model(); roEl.innerHTML=readoutHTML(M); eqEl.innerHTML=eqbarHTML(M); tagEl.innerHTML=tagHTML(M); }
        const dv=G_().divided;
        if(dv!==lastDiv){ lastDiv=dv; st.divided=dv; syncPanel(); }
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  box:'PhET&rsquo;s Diffusion screen. Two gases start either side of a divider, each with its own number, mass, radius and starting temperature. Take the divider out '
    +'and they mix &mdash; not because anything pushes them, but because there are vastly more ways to be spread out than to be sorted. Watch the triangles under the box: '
    +'each is a species&rsquo; centre of mass, and each starts at exactly &mp;(W + d)/4 = &mp;4.025 nm from the middle, a number that does not depend on the particle radius at all '
    +'(a bigger disk is kept off both ends of its half equally, so the midpoint does not move). They drift to zero and then jiggle about it, never back. '
    +'The arrows over the middle are the flow rates, and the lighter gas leads because it is faster &mdash; Graham&rsquo;s law, visible in the first picosecond.',
  mixing:'How fast <i>can</i> a gas mix? Two answers bracket it. If each half stayed perfectly stirred and the middle were the only bottleneck, the imbalance would fall as a single '
    +'exponential with &tau; = (W &minus; 2r)/4&lang;v<sub>x</sub><sup>+</sup>&rang; &mdash; 27 ps for the default heavy gas. If instead the particles had to random-walk their way across, the slowest mode of the '
    +'diffusion equation would take &tau;<sub>D</sub> = W&sup2;/&pi;&sup2;D, about six times longer. The truth is in between, and the readout says why: this box is about twenty-two mean free paths across, '
    +'so a particle neither flies straight through nor takes a long walk. Switch the two species to <i>identical</i> and the mixing still happens, which is the entropy of mixing with nothing else going on. '
    +'The left panel is the same story as a picture: the profiles start as two blocks and end flat.',
  flow:'Two measurements that could come out wrong, side by side with what kinetic theory says they must be. The crossing rate of a species across the middle line is n&lang;v<sub>x</sub><sup>+</sup>&rang;(H &minus; 2r), '
    +'with n the density of its centres on that side; the height cancels, leaving N&lang;v<sub>x</sub><sup>+</sup>&rang;/(W/2 &minus; r), and &lang;v<sub>x</sub><sup>+</sup>&rang; = &radic;(kT&#8322;/2&pi;m) is exactly &lang;v&rang;/&pi;. '
    +'Since it goes as 1/&radic;m, the ratio of the two species&rsquo; rates is Graham&rsquo;s &radic;(m&#8321;/m&#8322;) &mdash; &radic;7 = 2.65 for nitrogen against helium. '
    +'The right panel counts something else entirely: how often <i>any</i> two disks meet, which kinetic theory puts at &Sigma;<sub>j</sub> n<sub>j</sub>(r<sub>i</sub>+r<sub>j</sub>)&lang;v<sub>rel</sub>&rang; per disk, with '
    +'&lang;v<sub>rel</sub>&rang; set by the reduced mass. Make the disks bigger and watch both numbers move together.',
  speeds:'PhET does something unphysical on purpose: it starts every particle of a species at exactly the same speed, &radic;(3kT/m). That is a spike, not a distribution, and it cannot survive. '
    +'Collisions share the energy out, and after a few collisions per particle the histogram has become the 2-D Maxwell&ndash;Boltzmann law (mv/kT&#8322;)e<sup>&minus;mv&sup2;/2kT&#8322;</sup>, drawn in orange at each '
    +'species&rsquo; own measured temperature. The energy never changed, so the <i>mean</i> speed must fall: from the rms &radic;(3kT/m) to &radic;(&pi;kT&#8322;/2m), a factor of exactly &radic;(&pi;/4) = 0.8862, '
    +'the same for any mass. The right panel measures that drop. Start the two species at different temperatures and watch a second, slower thing happen: the energy leaks from the hot gas to the cold one until '
    +'both read the number-weighted mean.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  box:'<h4>where the centres of mass start</h4>'
    +EQ(1,'<span class="rm">PhET scatters species 1 uniformly in</span> [left, mid &minus; d/2], <span class="rm">centres in</span> [left + r, mid &minus; d/2 &minus; r]')
    +EQ(2,'x&#772; = &frac12;[(left + r) + (mid &minus; d/2 &minus; r)] &nbsp;&rArr;&nbsp; x&#772; &minus; mid = &minus;'+FR('W + d','4')+' &nbsp;<span class="rm">(the r cancels)</span>')
    +EQ(3,'<span class="rm">W = 16000 pm, d = 100 pm:</span> &minus;4025 pm <span class="rm">exactly, and +4025 for species 2</span>')
    +EQ(4,'<span class="rm">sampling sd of the measurement:</span> L/&radic;(12N) = 222 pm <span class="rm">for 100 particles</span>')
    +'<p>The radius cancelling is the point worth checking: a 250-pm disk is kept 250 pm off both ends of its half, which shifts the two ends of the interval equally and leaves its midpoint alone.</p>'
    +'<div class="cite">pins: &minus;4025 pm at r = 50 and r = 250; the 222 pm spread against 4000 Monte-Carlo draws &mdash; derive.py</div>',
  mixing:'<h4>two limits on the mixing time</h4>'
    +EQ(1,'<span class="rm">effusion (each half stirred):</span> '+FR('dN<sub>L</sub>','dt')+' = &minus;'+FR('N<sub>L</sub> &minus; N<sub>R</sub>','W/2 &minus; r')+' &lang;v<sub>x</sub><sup>+</sup>&rang;')
    +EQ(2,'&rArr; &Delta;N &prop; e<sup>&minus;t/&tau;</sup>, &nbsp; &tau; = '+FR('W &minus; 2r','4 &lang;v<sub>x</sub><sup>+</sup>&rang;')+' = 27.0 ps <span class="rm">(28 AMU, 125 pm, 300 K;</span> &tau;<sub>D</sub> = 155 ps<span class="rm">)</span>')
    +EQ(3,'<span class="rm">Fickian:</span> &tau;<sub>D</sub> = '+FR('W&sup2;','&pi;&sup2;D')+', &nbsp; D &asymp; '+FR('&lang;v&rang;&lambda;','2')+' &nbsp;&rArr;&nbsp; '+FR('&tau;<sub>D</sub>','&tau;')+' = '+FR('8W','&pi;&sup3;&lambda;')+' = 5.7')
    +EQ(4,'<span class="rm">collisions off, ballistic:</span> &Delta;N/N = 0.6437 <span class="rm">at 10 ps,</span> 0.0115 <span class="rm">at 40</span>')
    +'<p>[4] is exact kinematics, not a model: with no collisions each disk simply bounces between the end walls, so the imbalance falls faster than [2] at first (the fast ones are across before anything stops them) and then rings about zero. It is the one of the three the simulation can reproduce to the digit, and selfTest does.</p>'
    +'<div class="cite">pins: &tau; from the two-box ODE; the ballistic curve from 4&times;10<sup>6</sup> exact folded trajectories; &tau;<sub>D</sub>/&tau; = 8W/&pi;&sup3;&lambda; &mdash; derive.py</div>',
  flow:'<h4>the flux across a line, and how often disks meet</h4>'
    +EQ(1,'&lang;v<sub>x</sub><sup>+</sup>&rang; = &int;<sub>0</sub><sup>&infin;</sup> v<sub>x</sub> f(v<sub>x</sub>) dv<sub>x</sub> = &radic;('+FR('kT&#8322;','2&pi;m')+') = '+FR('&lang;v&rang;','&pi;')+' &nbsp;<span class="rm">(exactly)</span>')
    +EQ(2,'&Phi; = n &lang;v<sub>x</sub><sup>+</sup>&rang; (H &minus; 2r) = '+FR('N &lang;v<sub>x</sub><sup>+</sup>&rang;','W/2 &minus; r')+' &nbsp;<span class="rm">(100 heavy at 300 K: 1.852/ps)</span>')
    +EQ(3,FR('rate&#8322;','rate&#8321;')+' = &radic;('+FR('m&#8321;','m&#8322;')+') &times; '+FR('W/2 &minus; r&#8321;','W/2 &minus; r&#8322;')+' &nbsp;<span class="rm">(Graham, with the excluded width)</span>')
    +EQ(4,'z<sub>k</sub> = &Sigma;<sub>j</sub> n<sub>j</sub> <span class="hl">2</span>(r<sub>k</sub>+r<sub>j</sub>) &lang;v<sub>rel,kj</sub>&rang;, &nbsp; &lang;v<sub>rel</sub>&rang; = &radic;('+FR('&pi;','2')+'('+FR('kT&#8322;<sup>k</sup>','m<sub>k</sub>')+' + '+FR('kT&#8322;<sup>j</sup>','m<sub>j</sub>')+'))')
    +EQ(5,'<span class="rm">pairs per ps:</span> &frac12; &Sigma;<sub>k</sub> N<sub>k</sub> z<sub>k</sub> = 73.4 <span class="rm">in the default box</span>')
    +'<p>The 2 in [4] is the swath width: a disk collides when the centres come within d = r<sub>k</sub> + r<sub>j</sub>, so it sweeps a strip of HALF-width d. Leaving it out halves every rate, and the simulation&rsquo;s own pair counter caught exactly that (it measured 2.05&times; the first draft). &lang;v<sub>rel</sub>&rang; reduces to &radic;(&pi;kT&#8322;/2&mu;) when both species are at one temperature, and to &radic;2&lang;v&rang; for identical disks &mdash; both asserted. The flux [2] does not care about the interactions: the velocity distribution of hard disks at equilibrium is exactly Maxwellian everywhere, so the only corrections are the excluded width and whether the side is really uniform yet.</p>'
    +'<div class="cite">pins: &lang;v<sub>x</sub><sup>+</sup>&rang; by scipy quad; &lang;v<sub>rel</sub>&rang; against 2&times;10<sup>6</sup> Monte-Carlo velocity pairs; [5] against the simulation&rsquo;s own collision counter &mdash; derive.py</div>',
  speeds:'<h4>the spike, and what it must become</h4>'
    +EQ(1,'<span class="rm">PhET&rsquo;s start:</span> |v| = &radic;(3kT/m) <span class="rm">for every particle, direction uniform</span>')
    +EQ(2,'f(v) = '+FR('m v','kT&#8322;')+' e<sup>&minus;mv&sup2;/2kT&#8322;</sup>, &nbsp; kT&#8322; = &frac32;kT, &nbsp; &lang;v&rang; = &radic;('+FR('&pi;kT&#8322;','2m')+')')
    +EQ(3,FR('&lang;v&rang;<sub>MB</sub>','&radic;(3kT/m)')+' = &radic;('+FR('&pi;','4')+') = 0.886227 &nbsp;&rArr;&nbsp; <span class="rm">&lang;v&rang; falls by 11.377 %, any mass</span>')
    +EQ(4,'<span class="rm">two species, energy conserved:</span> T<sub>&infin;</sub> = '+FR('N&#8321;T&#8321; + N&#8322;T&#8322;','N&#8321; + N&#8322;'))
    +'<p>[3] holds because the energy does not change: the rms speed is fixed by kT&#8322;, and Maxwell&ndash;Boltzmann simply has a smaller mean than rms. It is the sharpest single check on the relaxation, and it is the same number for a 4-AMU disk and a 32-AMU one.</p>'
    +'<div class="cite">pins: the 20 bin probabilities at 300 K against a direct quadrature; &radic;(&pi;/4) for both species; the common temperature &mdash; derive.py</div>'
};
