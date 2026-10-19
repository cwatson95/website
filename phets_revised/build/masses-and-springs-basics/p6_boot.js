
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

  /* PhET gives each screen its own model, and the Stretch screen sets the
     damping to 0.7 while Bounce and Lab set 0 — switching views does the same,
     and re-hangs that screen's masses at the unstretched end */
  function releaseView(){
    const seen={};
    for(const sp of springsOf(st)){ if(!seen[sp.i]){ slotReset(sp.i); seen[sp.i]=1; } }
  }
  function setView(k){
    st.view=k;
    if(VIEW_DAMPING[k]!==undefined) st.damping=VIEW_DAMPING[k];
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    releaseView();
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{
    tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2));
  });

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
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); dirty=true; refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS=[];
  function trackChips(g,list,key){ CHIPROWS.push([g,list,key]); }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); }

  /* the two-spring screens */
  const gTwo=h('div',{class:'grp'},h('h3',null,'the two springs'));
  gTwo.appendChild(slider('k1','spring 1 strength, N/m',KMIN,KMAX,1,v=>fmt(v,0)+' N/m'));
  const m1Chips=chipRow(RACK,'mass1',()=>slotReset(0)); gTwo.appendChild(m1Chips); trackChips(gTwo,RACK,'mass1');
  gTwo.appendChild(slider('k2','spring 2 strength, N/m',KMIN,KMAX,1,v=>fmt(v,0)+' N/m'));
  const m2Chips=chipRow(RACK,'mass2',()=>slotReset(1)); gTwo.appendChild(m2Chips); trackChips(gTwo,RACK,'mass2');
  const twoTag=h('div',{class:'tag'}); gTwo.appendChild(twoTag);

  /* the lab's single spring */
  const gOne=h('div',{class:'grp'},h('h3',null,'the spring'));
  gOne.appendChild(slider('kl','spring strength, N/m',KMIN,KMAX,1,v=>fmt(v,0)+' N/m'));
  const mlChips=chipRow(LAB_RACK,'labMass',()=>slotReset(2)); gOne.appendChild(mlChips); trackChips(gOne,LAB_RACK,'labMass');
  gOne.appendChild(slider('massG','mass, g',MASS_G_MIN,MASS_G_MAX,1,v=>fmt(v,0)+' g',()=>slotReset(2)));
  const oneTag=h('div',{class:'tag'}); gOne.appendChild(oneTag);

  const gGrav=h('div',{class:'grp'},h('h3',null,'gravity'));
  const bodyChips=chipRow(BODY_LIST,'body'); gGrav.appendChild(bodyChips); trackChips(gGrav,BODY_LIST,'body');
  gGrav.appendChild(slider('gCustom','g, m/s²',GMIN,GMAX,0.1,v=>fmt(v,1)+' m/s²'));
  gGrav.appendChild(h('div',{class:'checks'},checkbox('reveal','reveal the hidden values')));
  const gravTag=h('div',{class:'tag'}); gGrav.appendChild(gravTag);

  const gDamp=h('div',{class:'grp'},h('h3',null,'damping'));
  gDamp.appendChild(slider('damping','b, N s/m',BMIN,BMAX,0.01,v=>fmt(v,2)+' N s/m'));
  const dampTag=h('div',{class:'tag'}); gDamp.appendChild(dampTag);

  const gTime=h('div',{class:'grp'},h('h3',null,'time'));
  gTime.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const speedChips=chipRow(SPEED_LIST,'speed'); gTime.appendChild(speedChips); trackChips(gTime,SPEED_LIST,'speed');
  gTime.appendChild(h('div',{class:'btnrow'},btn('step',()=>{ if(liveViews(st.view)) advance(st,0.02*(st.speed==='slow'?SLOW:1)); }),
    btn('let go again',releaseView),
    btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v;
      if(VIEW_DAMPING[v]!==undefined) st.damping=VIEW_DAMPING[v]; liveReset(); syncChips(); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  const gTools=h('div',{class:'grp'},h('h3',null,'lines and tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('natLine','unstretched length'),checkbox('restLine','resting position'),
    checkbox('movLine','movable line'),checkbox('ruler','ruler'),checkbox('stopwatch','stopwatch'),checkbox('trace','period trace')));
  const swBtns=h('div',{class:'btnrow'},btn('start / stop',()=>{ LIVE.swOn=!LIVE.swOn; }),btn('clear',()=>{ LIVE.sw=0; }));
  gTools.appendChild(swBtns);
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  const gAna=h('div',{class:'grp'},h('h3',null,'the spring analysed'));
  gAna.appendChild(slider('kA','spring constant k, N/m',KMIN,KMAX,1,v=>fmt(v,0)+' N/m'));
  gAna.appendChild(slider('mAg','mass m, g',MASS_G_MIN,MASS_G_MAX,1,v=>fmt(v,0)+' g'));
  gAna.appendChild(slider('zeta','damping ratio ζ',0,2,0.01,v=>fmt(v,2)));
  const anaTag=h('div',{class:'tag'}); gAna.appendChild(anaTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Masses and Springs: Basics (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values (spring 3&ndash;12 N/m, masses 50&ndash;300 g and the '
      +'rack of 50/100/250 g, Moon 1.6, Earth 9.8, Planet X 14.2, Jupiter 24.8 m/s<sup>2</sup>, damping 0&ndash;0.7 N s/m, ceiling 1.47 m, natural '
      +'length 0.5 m, slow motion &times;1/8) are read from its build 1.0.28 and its doc/model.md; the real surface gravities are Moon 1.62, Earth '
      +'9.81, Jupiter 24.79 m/s<sup>2</sup>. Everything else is exact and pinned in selfTest to build/masses-and-springs-basics/derive.py '
      +'(scipy solve_ivp and quad, an RK4 whose order is measured, and the closed form).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gTwo,gOne,gGrav,gDamp,gTime,gTools,gAna,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [g,list,key] of CHIPROWS){
      const cws=g.querySelectorAll('.chips');
      for(const cw of cws){
        if(cw.children.length!==list.length) continue;
        let match=0;
        for(let i=0;i<list.length;i++) if(cw.children[i].textContent===list[i].name) match++;
        if(match===list.length)
          [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
      }
    }
  }
  /* a row the view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view, two=(v==='str'||v==='bnc'), one=(v==='lab'||v==='eng'), live=two||one;
    gTwo.hidden=!two; gOne.hidden=!one;
    rows.massG.row.hidden=(rackById(LAB_RACK,st.labMass).m!==null);
    gGrav.hidden=!live;
    rows.gCustom.row.hidden=(st.body!=='custom');
    rows.cb_reveal.row.hidden=!(M_anyHidden());
    gDamp.hidden=!live;
    gTime.hidden=!live;
    gTools.hidden=!(v==='str'||v==='bnc'||v==='lab');
    rows.cb_trace.row.hidden=(v!=='lab');
    swBtns.hidden=!st.stopwatch;
    gAna.hidden=!(v==='per'||v==='dmp');
    rows.zeta.row.hidden=(v!=='dmp');
    for(const k in rows) rows[k].sync();
    const bc=bCrit(st.mAg/1000,st.kA);
    twoTag.innerHTML='PhET&rsquo;s rack: 250, 100 and 50 g, and three unlabelled ones. Drag a mass on the canvas to move it; let go and it swings from there.';
    oneTag.innerHTML='PhET&rsquo;s lab mass runs 50&ndash;300 g; its two unlabelled masses are 180 and 120 g. Drag it on the canvas.';
    gravTag.innerHTML='PhET&rsquo;s own values, not the real ones (Earth 9.81, Moon 1.62, Jupiter 24.79). Planet X is its invented '
      +(st.reveal?'14.2 m/s<sup>2</sup>':'mystery &mdash; read the stretch and solve g = k y/m');
    dampTag.innerHTML='PhET&rsquo;s Basics has no damping slider: it fixes b at 0.7 on Stretch and 0 on Bounce and Lab, which is what switching '
      +'views here restores. This slider is the parent sim&rsquo;s, 0&ndash;0.7 N s/m.';
    timeTag.innerHTML='space runs/pauses &nbsp; <b>.</b> steps &nbsp; <b>r</b> lets go again &nbsp; 1&ndash;6 switch views'
      +(st.speed==='slow'?' &nbsp; slow motion &times;1/8 (PhET)':'');
    toolTag.innerHTML='drag the ruler and the movable line on the canvas'+(st.stopwatch?'; the stopwatch runs on the readout':'');
    anaTag.innerHTML='2&radic;(km) = '+sigf(bc,4)+' N s/m here, so &zeta; = 1 needs b = '+sigf(bc,4)
      +' &mdash; '+(bc>BMAX?'past':'inside')+' PhET&rsquo;s 0.7. The slider runs to &zeta; = 2 so the other two regimes can be drawn.';
  }
  function M_anyHidden(){
    if(st.body==='planetX') return true;
    for(const sp of springsOf(st)) if(sp.myst) return true;
    return false;
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='str'||st.view==='bnc'||st.view==='lab')
        ?'drag a mass, the ruler or the movable line · space pauses · 1–6 switch views'
        :'space pauses · 1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ releaseView(); dirty=true; refresh(); }
    else if(e.key==='.'){ if(liveViews(st.view)) advance(st,0.02*(st.speed==='slow'?SLOW:1)); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0, last=0;
  function frameLoop(tm){
    frameN++;
    const dtw=last?Math.min((tm-last)/1000,0.05):0; last=tm;
    const advanced=S.step(dtw);
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  str:'This is PhET&rsquo;s Stretch screen. Hang a mass on a spring and it falls until the spring is pulling up exactly as hard as gravity is '
    +'pulling down. A spring&rsquo;s pull grows in proportion to how far it has been stretched &mdash; that is Hooke&rsquo;s law, F = &minus;ky &mdash; '
    +'so the balance is at ky = mg and the mass comes to rest at y = mg/k. Everything on this screen is that one formula. Double the mass and the '
    +'stretch doubles. Double the spring constant and it halves. Move to the Moon and it shrinks by a factor of six; move to Jupiter and it grows '
    +'by two and a half. The springs are drawn at their true shape, so you can lay the ruler against them and read the answer off. PhET&rsquo;s own '
    +'Stretch screen fixes the damping at 0.7 N s/m so the mass settles quickly rather than bouncing, and that is what this view does too.',
  bnc:'PhET&rsquo;s Bounce screen, with the damping PhET sets there: none. Write the extension as the resting value plus a wobble, y = mg/k + u, '
    +'and the mg on the right of Newton&rsquo;s law cancels against the ky of the resting stretch. What is left is m&uuml; + b&#361; + ku = 0, the '
    +'plain harmonic oscillator, which knows nothing about gravity at all. So gravity decides where the spring hangs and has no say in what it does '
    +'afterwards. Let a mass go from the unstretched end and it is starting a whole amplitude away from the resting point, so it falls exactly '
    +'2mg/k, comes to a stop, and comes back &mdash; for ever, with no damping. Turn the damping up and the swing shrinks by the same factor every '
    +'period, which is the next view but one.',
  lab:'PhET&rsquo;s Lab screen: one spring, a mass you can set anywhere from 50 to 300 g, and a gravity you can move from the Moon to Jupiter. The '
    +'period trace marks each time the spring passes its resting point; two marks apart is one whole period, and the number it measures is '
    +'2&pi;&radic;(m/k) to every digit the trace can carry. Change the gravity and watch what happens: the mass hangs somewhere else entirely, and '
    +'the trace does not change at all. That is the single most useful thing about a mass on a spring, and it is why a spring balance has to be '
    +'recalibrated on the Moon while a spring clock does not. Planet X is PhET&rsquo;s puzzle: its gravity is hidden, but the stretch is not, so '
    +'g = ky/m gives it away. The unlabelled masses work the same way round, m = ky/g.',
  per:'T = 2&pi;&radic;(m/k) says the period depends on the mass and the spring and on nothing else &mdash; not on how far you pulled it, not on '
    +'where you are. The orange curves are that formula at the four spring constants PhET&rsquo;s slider marks; the green points are the period '
    +'MEASURED from the drawn motion, by finding two crossings of the resting point and taking the gap. They agree to about a part in 10<sup>15</sup>, '
    +'which is as close as a double can come. The bar chart below shows the same spring and mass on the Moon, on Earth, on Planet X and on Jupiter: '
    +'four very different hanging points, one period. Damping does change the period, but only at second order: the damped period is T/&radic;(1 &minus; '
    +'&zeta;&sup2;), so even at PhET&rsquo;s heaviest damping on its stiffest spring it is 1.7 % long.',
  dmp:'Add a damper and the equation becomes m&uuml; + b&#361; + ku = 0, whose solutions go as e<sup>st</sup> with ms&sup2; + bs + k = 0 &mdash; '
    +'PhET&rsquo;s own model notes say exactly this. Whether the two roots are complex, equal or real is decided by b&sup2; &minus; 4km, so the whole '
    +'behaviour hangs on the single ratio &zeta; = b/(2&radic;(km)). Below one, the roots are complex and the spring oscillates inside a shrinking '
    +'envelope. At exactly one, the roots coincide and the spring comes back as fast as it can without overshooting &mdash; which is how a door '
    +'closer and a car damper are tuned. Above one, it crawls back more slowly than that, because the slow root is nearer to zero. Now look at the '
    +'panel below left: PhET&rsquo;s damping stops at 0.7 N s/m, and 2&radic;(km) over its own masses and springs never falls below 0.7746, so '
    +'nothing PhET can draw is critically damped. The curves above go past its range on purpose, and say so.',
  eng:'Three energies are in play. The mass carries &frac12;mv&sup2;; the spring stores &frac12;ky&sup2;; gravity still has mg(y<sub>bot</sub> '
    +'&minus; y) to give, measured from the bottom of the swing at y<sub>bot</sub> = 2mg/k so that none of the three is ever negative. With no '
    +'damper they add to a constant for ever &mdash; the flat white line &mdash; and that constant is 2(mg)&sup2;/k, which is what gravity hands '
    +'over in the fall. Halfway down, at the resting point, the spring has stored exactly half of it and the mass carries the other half as kinetic '
    +'energy. Add a damper and it takes energy at bv&sup2; a '
    +'second, fastest where the mass is moving fastest. Released from rest, the turning points fall exactly half a damped period apart and the '
    +'energy at each one is E&#8320;e<sup>&minus;n&delta;</sup>, a clean geometric decay; the points on the panel below right sit on that curve.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  str:'<h4>Hooke&rsquo;s law</h4>'
    +EQ(1,'F<sub>spring</sub> = &minus;k y &nbsp;&middot;&nbsp; at rest &nbsp; k y = m g &nbsp;&rArr;&nbsp; y<sub>eq</sub> = '+FR('m g','k'))
    +EQ(2,'PE<sub>elastic</sub> = &frac12; k y&sup2; &nbsp;&middot;&nbsp; PE<sub>gravity</sub> = m g (y<sub>bot</sub> &minus; y), &nbsp; y<sub>bot</sub> = 2mg/k')
    +EQ(3,'<span class="rm">the drawn block:</span> r = 4&radic;(m/(80 &middot; 2.5 &pi;)) m, &nbsp; height 2.5 r &nbsp;<span class="rm">(PhET&rsquo;s rule)</span>')
    +'<p>Nothing on this screen is approximate: the spring is linear at every extension by construction, so the extension is exactly mg/k. At '
    +'PhET&rsquo;s largest mass on its softest spring at its largest gravity the extension is 3.00 m, well below the floor &mdash; PhET draws that too.</p>'
    +'<div class="cite">pins: mg/k over all 10040 (mass, spring constant, planet) states the sim allows, against derive.py&rsquo;s sum 3549.219863636362 m &mdash; derive.py</div>',
  bnc:'<h4>the oscillator, and why gravity drops out</h4>'
    +EQ(1,'m &#375; = m g &minus; k y &minus; b &#7823;')
    +EQ(2,'y = y<sub>eq</sub> + u, &nbsp; y<sub>eq</sub> = m g/k &nbsp;&rArr;&nbsp; m &uuml; + b &#361; + k u = 0')
    +EQ(3,'&omega;<sub>0</sub> = &radic;(k/m), &nbsp; &gamma; = '+FR('b','2m')+', &nbsp; &zeta; = '+FR('&gamma;','&omega;<sub>0</sub>')+' = '+FR('b','2&radic;(km)'))
    +EQ(4,'u = e<sup>&minus;&gamma;t</sup>[u<sub>0</sub>(C + &gamma;S) + v<sub>0</sub>S], &nbsp; v = e<sup>&minus;&gamma;t</sup>[&minus;&omega;<sub>0</sub>&sup2;u<sub>0</sub>S + v<sub>0</sub>(C &minus; &gamma;S)]')
    +EQ(5,'C = cos(&radic;s t), &nbsp; S = sin(&radic;s t)/&radic;s, &nbsp; s = &omega;<sub>0</sub>&sup2; &minus; &gamma;&sup2; &nbsp;<span class="rm">(cosh/sinh below 0, series at 0)</span>')
    +'<p>[4] is the sim&rsquo;s integrator: the state is advanced by the exact solution every frame, so the trajectory is the closed form at any '
    +'frame rate and in every regime. An RK4 of [2] runs beside it in the test suite and is measured to be fourth order.</p>'
    +'<div class="cite">pins: u and v at four times in six (m, k, b) cases against derive.py; scipy solve_ivp over 80 states to 2.4e&minus;12; the RK4 error ratios 16.03&ndash;16.44 per halving &mdash; derive.py</div>',
  lab:'<h4>the period</h4>'
    +EQ(1,'T = '+FR('2&pi;','&omega;<sub>0</sub>')+' = 2&pi;&radic;(m/k) &nbsp;<span class="rm">&mdash; no g, no amplitude</span>')
    +EQ(2,'T<sub>d</sub> = '+FR('2&pi;','&radic;(&omega;<sub>0</sub>&sup2; &minus; &gamma;&sup2;)')+' = '+FR('T','&radic;(1 &minus; &zeta;&sup2;)'))
    +EQ(3,'<span class="rm">released from rest, v = 0 exactly at</span> &omega;<sub>d</sub>t = n&pi; <span class="rm">and</span> |u<sub>n</sub>| = u<sub>0</sub>e<sup>&minus;n&delta;/2</sup>, &nbsp; &delta; = &gamma;T<sub>d</sub>')
    +EQ(4,'g = k y<sub>eq</sub>/m &nbsp;<span class="rm">(Planet X)</span>, &nbsp; m = k y<sub>eq</sub>/g &nbsp;<span class="rm">(the unlabelled masses)</span>')
    +'<p>[3] is exact and is why the period trace works: with the mass let go from rest, the velocity vanishes at whole multiples of half a damped '
    +'period whatever the damping, so the crossings of the resting point are evenly spaced.</p>'
    +'<div class="cite">pins: the measured period against 2&pi;&radic;(m/k) at five masses; the zeros 0.20278893379868057, 0.6083668013960417, 1.0139446689934029 s at 100 g on 6 N/m &mdash; derive.py</div>',
  per:'<h4>what the period does and does not depend on</h4>'
    +EQ(1,'T = 2&pi;&radic;(m/k): &nbsp; &part;T/&part;g = 0, &nbsp; &part;T/&part;A = 0')
    +EQ(2,'y<sub>eq</sub>(Jupiter)/y<sub>eq</sub>(Moon) = 24.8/1.6 = 15.5 &nbsp;<span class="rm">while T is unchanged</span>')
    +EQ(3,'T<sub>d</sub>/T = (1 &minus; &zeta;&sup2;)<sup>&minus;&frac12;</sup> = 1 + &zeta;&sup2;/2 + O(&zeta;<sup>4</sup>)')
    +'<p>The measured points come from bisecting u(t) for its zeros &mdash; the same function the stage steps with &mdash; so the agreement is a '
    +'statement about the solution, not about the drawing.</p>'
    +'<div class="cite">pins: the five measured periods to 1e&minus;12 of the closed form; T identical on all four planets to the last bit &mdash; derive.py</div>',
  dmp:'<h4>the three regimes</h4>'
    +EQ(1,'m s&sup2; + b s + k = 0 &nbsp;&rArr;&nbsp; s = &minus;&gamma; &plusmn; &radic;(&gamma;&sup2; &minus; &omega;<sub>0</sub>&sup2;)')
    +EQ(2,'&zeta; &lt; 1 <span class="rm">two complex roots &mdash; oscillates in</span> e<sup>&minus;&gamma;t</sup>; &nbsp; &zeta; = 1 <span class="rm">one double root</span>; &nbsp; &zeta; &gt; 1 <span class="rm">two real roots</span>')
    +EQ(3,'&delta; = &gamma;T<sub>d</sub> = '+FR('2&pi;&zeta;','&radic;(1 &minus; &zeta;&sup2;)')+' &nbsp;<span class="rm">amplitude &times; e<sup>&minus;&delta;</sup> per period</span>')
    +EQ(4,'b<sub>crit</sub> = 2&radic;(km) &isin; [0.774597, 3.794733] <span class="rm">N s/m over PhET&rsquo;s box</span> &nbsp;&rArr;&nbsp; &zeta; &le; 0.903696')
    +'<p>[4] is the whole content of the panel below left. Nothing PhET&rsquo;s own sliders can reach is critically damped; the closest it comes is '
    +'the lightest mass on the softest spring at full damping.</p>'
    +'<div class="cite">pins: u and v in the critical and overdamped cases against scipy; 2&radic;(km) at the four corners; &zeta;<sub>max</sub> = 0.9036961141150639 &mdash; derive.py</div>',
  eng:'<h4>the ledger</h4>'
    +EQ(1,'E = &frac12;mv&sup2; + &frac12;ku&sup2; &nbsp;&middot;&nbsp; '+FR('dE','dt')+' = &minus;b v&sup2;')
    +EQ(2,'&frac12;mv&sup2; + &frac12;ky&sup2; + mg(y<sub>bot</sub> &minus; y) = E + '+FR('3(mg)&sup2;','2k')+' &nbsp;<span class="rm">with</span> y<sub>bot</sub> = 2mg/k')
    +EQ(3,'<span class="rm">let go from y = 0:</span> E<sub>0</sub> = &frac12;k(mg/k)&sup2; = '+FR('(mg)&sup2;','2k')+', <span class="rm">swing</span> 0 &rarr; 2mg/k, <span class="rm">ledger</span> '+FR('2(mg)&sup2;','k'))
    +EQ(4,'E(nT<sub>d</sub>/2) = E<sub>0</sub> e<sup>&minus;n&delta;</sup> &nbsp;<span class="rm">exactly, for a release from rest</span>')
    +'<p>[2] is why the four shares add to a flat line: the gravitational and elastic terms carry a constant between them that the oscillation never '
    +'touches. The datum for the gravitational share is the BOTTOM of the swing, which keeps all three shares non-negative &mdash; with the zero at '
    +'the unstretched end the sum would be &minus;(mg)&sup2;/2k and would lie on the axis, where nobody could see it. [4] is exact because the '
    +'velocity vanishes exactly at &omega;<sub>d</sub>t = n&pi;.</p>'
    +'<div class="cite">pins: the sum flat to 1e&minus;16 J over three periods; E(0) &minus; E(t) against b&int;v&sup2;dt by scipy quad (residual 0 to 5e&minus;18 J) &mdash; derive.py</div>',
};
