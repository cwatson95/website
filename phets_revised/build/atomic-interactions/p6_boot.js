
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

  function setView(k){
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(id,lab2,lo,hi,step2,fmtf,get,set){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.textContent=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); syncPanel(); dirty=true; refresh(); });
    rows[id]={row:rowEl,inp,sync}; sync(); return rowEl;
  }
  function checkbox(id,lab2,get,set){
    const inp=h('input',{type:'checkbox'}); inp.checked=!!get();
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ if(inp.disabled) return; set(inp.checked); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+id]={row:el,inp,sync:()=>{ inp.checked=!!get(); }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onpick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        if(onpick) onpick(o.id); else st[key]=o.id;
        syncChips(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }

  /* PhET's Atoms panel: the seven pairs */
  const gPair=h('div',{class:'grp'},h('h3',null,'atoms'));
  gPair.appendChild(chipRow(PAIRS.map(p=>({id:p.key,name:p.label})),'pair',k=>setPair(st,k)));
  const gAdj=h('div',{class:'grp'},h('h3',null,'adjustable attraction'));
  gAdj.appendChild(slider('adjSig','atom diameter σ',PHET_MIN_SIGMA,PHET_MAX_SIGMA,5,
    v=>fmt(v,0)+' pm',()=>st.adjSig,v=>setAdjSig(st,v)));
  gAdj.appendChild(slider('adjEps','interaction ε',PHET_MIN_EPSILON,PHET_MAX_EPSILON,5,
    v=>fmt(v,0)+' K',()=>st.adjEps,v=>setAdjEps(st,v)));
  gAdj.appendChild(h('div',{class:'tag',html:'PhET&rsquo;s own ranges: &sigma; 75&ndash;500 pm and &epsilon;/k<sub>B</sub> 20&ndash;450 K, '
    +'both snapped to multiples of 5. <i>small&ndash;large</i> and <i>weak&ndash;strong</i> are PhET&rsquo;s tick labels.'}));

  /* PhET's Forces control, plus the two model choices this remake adds */
  const gForce=h('div',{class:'grp'},h('h3',null,'forces'));
  gForce.appendChild(chipRow(FORCE_MODES.map(m=>({id:m[0],name:m[1]})),'forces'));
  const gModel=h('div',{class:'grp'},h('h3',null,'the model'));
  gModel.appendChild(h('div',{class:'checks'},
    checkbox('pinned','left atom pinned (PhET’s)',()=>st.pinned,v=>setPinned(st,v)),
    checkbox('lit','literature ε, σ instead of PhET’s',()=>st.lit,v=>setLit(st,v))));
  const modelTag=h('div',{class:'tag'}); gModel.appendChild(modelTag);

  /* the motion */
  const gMotion=h('div',{class:'grp'},h('h3',null,'the motion'));
  gMotion.appendChild(slider('rel','release at r_min +',-20,120,0.5,v=>fmt(v,1)+' pm',
    ()=>st.rel,v=>{ st.rel=v; }));
  gMotion.appendChild(slider('v0f','launch speed',0,1.4,0.02,
    v=>fmt(v,2)+' × escape',()=>st.v0f,v=>{ st.v0f=v; }));
  gMotion.appendChild(h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ releaseAtom(st); syncPanel(); dirty=true; refresh(); }},'release'),
    h('button',{onclick:()=>{ st.running=!st.running; dirty=true; refresh(); }},'play / pause'),
    h('button',{onclick:()=>{ returnAtom(st); syncPanel(); dirty=true; refresh(); }},'return atom')));
  gMotion.appendChild(h('div',{class:'checks'},
    checkbox('slow','slow (PhET’s speed switch)',()=>st.slow,v=>{ st.slow=v; })));
  const motionTag=h('div',{class:'tag'}); gMotion.appendChild(motionTag);

  const gSmall=h('div',{class:'grp'},h('h3',null,'amplitude'));
  gSmall.appendChild(slider('amp','release offset A',0.05,60,0.05,v=>fmt(v,2)+' pm',
    ()=>st.amp,v=>{ st.amp=v; }));

  const gPairs=h('div',{class:'grp'},h('h3',null,'what to overlay'));
  gPairs.appendChild(h('div',{class:'checks'},
    checkbox('showLit','the literature wells, dashed',()=>st.showLit,v=>{ st.showLit=v; })));

  const gReset=h('div',{class:'grp'},h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; simReset();
      syncChips(); syncPanel(); dirty=true; refresh(); }},'reset all')));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Atomic Interactions (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'PhET&rsquo;s values (build 1.2.21): &epsilon;/k<sub>B</sub> 35.8, 111.84, 1000, 59.5, 51, 85 K and '
      +'&sigma; 308, 376, 200, 343, 306, 340 pm; van der Waals radii 154, 188, 152 pm; masses 20.1797, 39.948, 15.9994 u. '
      +'Literature: Ne and Ar from Attard arXiv:1702.00096 Table I (after van Sciver, <i>Helium Cryogenics</i> 2nd ed., 2012); '
      +'Ar and O<sub>2</sub> from Bird, Stewart &amp; Lightfoot, <i>Transport Phenomena</i> 2nd ed. (2007) pp. 864&ndash;865. '
      +'k<sub>B</sub>, m<sub>u</sub>: CODATA 2022 via scipy.constants. Every closed form is pinned in selfTest to '
      +'build/atomic-interactions/derive.py.'}));
  [gPair,gAdj,gForce,gModel,gMotion,gSmall,gPairs,gReset,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS) [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  function syncPanel(){
    const v=st.view;
    gAdj.hidden=!(st.pair==='Adj');
    gForce.hidden=!(v==='atoms'||v==='well');
    gMotion.hidden=!(v==='motion');
    gSmall.hidden=!(v==='small');
    gPairs.hidden=!(v==='pairs');
    gModel.hidden=(v==='pairs'||v==='steppers');
    for(const k in rows) rows[k].sync();
    /* the literature switch cannot act on the adjustable pair — its epsilon and
       sigma ARE the two sliders — so disable it there rather than leave a live
       control that does nothing (Known-bad). */
    const litOn=st.pair!=='Adj';
    rows.cb_lit.inp.disabled=!litOn;
    rows.cb_lit.row.style.opacity=litOn?'1':'0.45';
    const P=pairInfo(st);
    modelTag.innerHTML='&mu; = '+sigf(P.mu,5)+' u &mdash; '+(st.pinned
      ? 'only the right atom moves, so &mu; is its own mass'
      : 'both move, so &mu; = m<sub>1</sub>m<sub>2</sub>/(m<sub>1</sub>+m<sub>2</sub>) and every period is shorter')
      +'. T = 2&pi;/&omega; = '+sigf(P.period,4)+' ps.';
    const L=liveModel(st);
    motionTag.innerHTML='escape speed where the atom is now: '+sigf(L.vEsc,4)+' m/s. '
      +'The clock runs at '+fmt(PS_PER_SEC*(st.slow?SLOW_FACTOR:1),2)+' ps per second; the integrator substeps at '
      +fmt(DT_INT*1000,1)+' fs whatever the frame rate.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='atoms')?'drag the right-hand atom · 1–6 switch views · space plays'
        :'1–6 switch views'+(st.view==='motion'?' · space plays · r releases':'');
      infoEl.innerHTML=INFO[st.view]||'';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){
      dirty=true; const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)){ setView(TABS[+e.key-1][0]); return; }
    if(e.key===' '){ st.running=!st.running; dirty=true; refresh(); }
    if(e.key==='r'||e.key==='R'){ releaseAtom(st); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let ticks=0;
  function frameLoop(){
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&(++ticks%6===0)){ const M=S.model();
        roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); } }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  atoms:'This is PhET&rsquo;s screen. Two atoms sit on a line; the left one is pinned and the right one you drag. What holds them, '
    +'pushes them apart and lets them go is one curve &mdash; the Lennard-Jones potential, V(r) = 4&epsilon;[(&sigma;/r)<sup>12</sup> &minus; (&sigma;/r)<sup>6</sup>]. '
    +'The r<sup>&minus;6</sup> term is the London dispersion attraction, which every pair of neutral atoms has because their electron clouds '
    +'fluctuate in step; the r<sup>&minus;12</sup> term is a convenient stand-in for the Pauli repulsion that stops two closed shells occupying the '
    +'same space (it is chosen because it is the square of the r<sup>&minus;6</sup>, not because anything says twelve). Two parameters set the whole '
    +'curve: &sigma;, where it crosses zero, and &epsilon;, how deep it goes. The force is minus its slope, so the atoms attract on the outer '
    +'slope, repel on the inner wall, and feel nothing at all at the bottom &mdash; which is exactly 2<sup>1/6</sup>&sigma;, about 12% outside &sigma;.',
  well:'The force is not an extra assumption: it is the slope of the curve, F(r) = &minus;dV/dr, and everything the atoms do follows from that one '
    +'line. PhET writes the two halves separately &mdash; 48&epsilon;&sigma;<sup>12</sup>/r<sup>13</sup> pushing out and 24&epsilon;&sigma;<sup>6</sup>/r<sup>7</sup> '
    +'pulling in &mdash; and their difference is exactly the derivative, which the readout checks every time you move the atom. The force crosses '
    +'zero at the bottom of the well and is most attractive not there but at the inflection of V, at (26/7)<sup>1/6</sup>&sigma;; past that point pulling '
    +'the atoms further apart gets easier, which is why a solid has a finite tensile strength. The residual panel is the honest version of &ldquo;F is '
    +'the derivative&rdquo;: the closed form minus a numerical derivative of V, in units of the force scale, sitting at the level of one rounding error.',
  motion:'Let go and the atom falls into the well, overshoots, climbs the wall and comes back. Because the total energy is conserved it turns round '
    +'wherever V(r) rises to meet E, and those two points have a closed form: with u = (&sigma;/r)<sup>6</sup> the condition V = E is a quadratic, so '
    +'u<sub>in</sub> + u<sub>out</sub> = 1 exactly. Give it enough speed and E reaches zero, the outer turning point runs off to infinity and the pair '
    +'dissociates &mdash; the dashed curve in the phase portrait is that separatrix. Real neon is not like this: at these depths (&epsilon;/k<sub>B</sub> is '
    +'36 K) the vibration is quantum, the levels are discrete and the zero-point energy is a serious fraction of the well, so a classical trajectory is '
    +'a picture of the potential rather than of the dimer.',
  small:'Close enough to the bottom, every smooth minimum is a parabola, and a parabola gives simple harmonic motion whose period does not depend '
    +'on how far you pull it. Here the spring constant is V&Prime;(r<sub>min</sub>) = 72&epsilon;/(2<sup>1/3</sup>&sigma;&sup2;) and the frequency is '
    +'&radic;(V&Prime;/&mu;), with &mu; the mass of whatever is actually free to move: the movable atom&rsquo;s own mass while the other one is pinned, '
    +'and the reduced mass m<sub>1</sub>m<sub>2</sub>/(m<sub>1</sub>+m<sub>2</sub>) when both are free &mdash; which for a like pair makes every period '
    +'shorter by &radic;2. The lower panel is the departure from that limit. It is quadratic in the amplitude, and its coefficient is not a fit: Landau '
    +'and Lifshitz&rsquo;s anharmonic formula, fed the Taylor coefficients of this well (72, &minus;1512, 26712 in units of &epsilon;/r<sub>min</sub><sup>n</sup>), '
    +'gives T = T<sub>0</sub>[1 + (91/4) a&sup2;/r<sub>min</sub>&sup2;], and the quadrature follows it to a part in 10<sup>5</sup>.',
  pairs:'Two numbers describe a pair, and where they come from matters. PhET&rsquo;s &sigma; is twice the van der Waals radius &mdash; 308 pm for neon, '
    +'376 for argon. The literature&rsquo;s &sigma; for the same atoms is 278.9 and 341.8 pm, about 10% smaller; but the literature&rsquo;s r<sub>min</sub> is '
    +'313.1 and 383.7 pm, within 2% of PhET&rsquo;s numbers. A van der Waals radius is measured where atoms actually sit in a crystal, which is the bottom of '
    +'the well, and the bottom of an LJ well is 2<sup>1/6</sup> = 1.1225 times &sigma;. So PhET&rsquo;s &sigma; is really an r<sub>min</sub>, and its wells are '
    +'12% too wide. Oxygen is a different matter: 1000 K and 200 pm match neither the literature (113 K, 343 pm) nor PhET&rsquo;s own States-of-Matter '
    +'constants (113 K, 365 pm), and at 200 pm the minimum lies well inside the two drawn spheres. The mixed pairs are usually guessed by the '
    +'Lorentz&ndash;Berthelot rules; PhET&rsquo;s neon&ndash;argon row follows them, and its oxygen rows cannot.',
  steppers:'A molecular-dynamics code lives or dies on its integrator, and the reason is visible here. The left panel measures the ORDER: halve the step '
    +'and velocity Verlet&rsquo;s energy error falls by four, semi-implicit Euler&rsquo;s by two. The right panel measures something else, and it is the more '
    +'important half. Verlet and semi-implicit Euler are symplectic &mdash; each exactly conserves an energy a little different from the true one &mdash; so '
    +'their error oscillates for ever and never grows, at any step size they are stable at. Forward Euler conserves nothing, and its error climbs steadily '
    +'whatever step you give it; a gas integrated that way heats itself up. PhET&rsquo;s own model uses semi-implicit Euler (a = F/m, then v += a&Delta;t, '
    +'then x += v&Delta;t), which is why its atoms stay in the well; this sim uses velocity Verlet for the extra order.',
};
