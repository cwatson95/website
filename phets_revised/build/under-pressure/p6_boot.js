
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
    clearAll(); syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lb])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lb)); });

  const rows={};
  function slider(key,lb,lo,hi,step,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lb),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ const v=parseFloat(inp.value);
      if(onchg) onchg(v); else st[key]=v;
      clearAll(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,input:inp}; sync(); return rowEl;
  }
  function checkbox(key,lb,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lb);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg();
      clearAll(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick,getSel){
    const wrapEl=h('div',{class:'chips'});
    const sel=getSel||(()=>st[key]);
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(sel()===o.id?' on':''),onclick:()=>{
        if(onPick) onPick(o); else st[key]=o.id;
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(sel()===list[i].id?' on':''));
        clearAll(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,sel]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); clearAll(); syncChips(); syncPanel(); dirty=true; refresh(); }},label); }

  /* ---- group 1: the fluid ---- */
  const gFluid=h('div',{class:'grp'},h('h3',null,'the fluid'));
  gFluid.appendChild(chipRow(FLUID_TICKS,'rho',o=>{ st.rho=o.rho; },
    ()=>{ const f=FLUID_TICKS.find(o=>Math.abs(o.rho-st.rho)<1e-9); return f?f.id:null; }));
  gFluid.appendChild(slider('rho','density ρ',RHO_GASOLINE,RHO_HONEY,1,v=>fmt(v,0)+' kg/m³'));
  const fluidTag=h('div',{class:'tag'}); gFluid.appendChild(fluidTag);

  /* ---- group 2: the world ---- */
  const gWorld=h('div',{class:'grp'},h('h3',null,'the world'));
  gWorld.appendChild(chipRow(G_TICKS,'grav',o=>{ st.grav=o.g; },
    ()=>{ const t=G_TICKS.find(o=>Math.abs(o.g-st.grav)<1e-9); return t?t.id:null; }));
  gWorld.appendChild(slider('grav','gravity g',G_MARS,G_JUPITER,0.01,v=>fmt(v,2)+' m/s²'));
  gWorld.appendChild(h('div',{class:'checks'},checkbox('atmosphere','atmosphere')));
  const worldTag=h('div',{class:'tag'}); gWorld.appendChild(worldTag);

  /* ---- group 3: the pool ---- */
  const gPool=h('div',{class:'grp'},h('h3',null,'the pool'));
  gPool.appendChild(slider('volFrac','faucet and drain',0,1,0.01,v=>fmt(100*v,0)+' % full'));
  gPool.appendChild(h('div',{class:'checks'},checkbox('gridOn','grid'),checkbox('rulerOn','ruler')));
  const poolTag=h('div',{class:'tag'}); gPool.appendChild(poolTag);

  /* ---- group 4: the gauges ---- */
  const gGauge=h('div',{class:'grp'},h('h3',null,'the gauges'));
  gGauge.appendChild(slider('gAx','gauge A, across',1.4,8.2,0.01,v=>fmt(v,2)+' m'));
  gGauge.appendChild(slider('gAy','gauge A, height',-POOL_H,0.6,0.01,v=>fmt(v,2)+' m'));
  gGauge.appendChild(slider('gBx','gauge B, across',1.4,8.2,0.01,v=>fmt(v,2)+' m'));
  gGauge.appendChild(slider('gBy','gauge B, height',-POOL_H,0.6,0.01,v=>fmt(v,2)+' m'));
  gGauge.appendChild(h('div',{class:'btnrow'},
    btn('same depth',()=>{ st.gBy=st.gAy; }),
    btn('reset the gauges',()=>{ st.gAx=DEFAULTS.gAx; st.gAy=DEFAULTS.gAy; st.gBx=DEFAULTS.gBx; st.gBy=DEFAULTS.gBy; })));
  const gaugeTag=h('div',{class:'tag'}); gGauge.appendChild(gaugeTag);

  /* ---- group 5: the platform ---- */
  const gStack=h('div',{class:'grp'},h('h3',null,'the platform'));
  gStack.appendChild(h('div',{class:'checks'},checkbox('m500','500 kg'),
                       checkbox('m250a','250 kg'),checkbox('m250b','250 kg again')));
  const stackTag=h('div',{class:'tag'}); gStack.appendChild(stackTag);

  /* ---- group 6: the mystery ---- */
  const gMy=h('div',{class:'grp'},h('h3',null,'the mystery'));
  gMy.appendChild(chipRow(MY_MODE_LIST,'myMode'));
  gMy.appendChild(chipRow(MY_PICK_LIST,'myWhich',o=>{ st.myWhich=+o.id; },()=>String(st.myWhich)));
  gMy.appendChild(slider('myDepth','the gauge, depth',0,POOL_H,0.01,v=>fmt(v,2)+' m'));
  gMy.appendChild(h('div',{class:'gsub'},'your answer'));
  gMy.appendChild(chipRow(MY_PICK_LIST,'myGuess'));
  gMy.appendChild(h('div',{class:'checks'},checkbox('myReveal','show the answer')));
  const myTag=h('div',{class:'tag'}); gMy.appendChild(myTag);

  /* ---- group 7: the vessels ---- */
  const gVes=h('div',{class:'grp'},h('h3',null,'the vessels'));
  gVes.appendChild(chipRow(VESSEL_LIST,'parPick'));
  gVes.appendChild(slider('parDepth','fluid depth',0.2,PAR_H,0.01,v=>fmt(v,2)+' m'));
  const vesTag=h('div',{class:'tag'}); gVes.appendChild(vesTag);

  /* ---- group 8: the line ---- */
  const gLine=h('div',{class:'grp'},h('h3',null,'the line'));
  gLine.appendChild(slider('colDepth','read it at',0,POOL_H,0.01,v=>fmt(v,2)+' m'));
  gLine.appendChild(h('div',{class:'checks'},checkbox('colAll','the three named fluids')));
  const lineTag=h('div',{class:'tag'}); gLine.appendChild(lineTag);

  /* ---- group 9: the units ---- */
  const gUnit=h('div',{class:'grp'},h('h3',null,'the units'));
  gUnit.appendChild(chipRow(UNIT_LIST,'units'));
  gUnit.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; })));
  const unitTag=h('div',{class:'tag'}); gUnit.appendChild(unitTag);

  /* ---- group 10: what you are looking at ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Under Pressure (University of Colorado '
      +'Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values &mdash; gasoline '
      +'700, water 1000 and honey 1420 kg/m&sup3;; Mars 3.71, Earth 9.8 and Jupiter 24.9 m/s&sup2;; air 101325 Pa at the '
      +'ground falling linearly to 99490 Pa at 150 m and scaled by g/g<sub>earth</sub>; a 3 m pool; the trapezoid&rsquo;s '
      +'0.7 and 3.15 m widths; the chamber&rsquo;s 0.5 and 2.3 m shafts and its 500/250/250 kg masses; the mystery fluids '
      +'1700, 840, 1100 and the mystery planets 20, 14, 6.5 &mdash; are read out of its build 1.1.36. The unit '
      +'conversions are NOT PhET&rsquo;s rounded factors but the definitions: 1 atm = 101325 Pa, 1 psi = 0.45359237 '
      +'&times; 9.80665 / 0.0254&sup2; Pa, 1 ft = 0.3048 m. Every number is pinned in selfTest to '
      +'build/under-pressure/derive.py (scipy.integrate.quad, scipy.optimize.brentq, a 400 000-strip Riemann sum).'}));
  /* ---- group 11: the physics ---- */
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gFluid,gWorld,gPool,gGauge,gStack,gMy,gVes,gLine,gUnit,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,sel] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(sel()===list[i].id?' on':''));
  }
  /* a row this view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view;
    const scene=(v==='pool'||v==='shapes'||v==='press'||v==='mystery');
    gFluid.hidden=(v==='mystery'&&st.myMode==='fluid');
    gWorld.hidden=(v==='mystery'&&st.myMode==='planet');
    rows.cb_atmosphere.row.hidden=false;
    gPool.hidden=!(v==='pool'||v==='shapes'||v==='mystery');
    rows.volFrac.row.hidden=(v==='mystery');
    gGauge.hidden=!(v==='pool'||v==='shapes'||v==='press');
    gStack.hidden=(v!=='press');
    gMy.hidden=(v!=='mystery');
    gVes.hidden=(v!=='paradox');
    gLine.hidden=(v!=='column');
    for(const k in rows) if(rows[k].sync) rows[k].sync();
    syncChips();
    fluidTag.innerHTML='PhET&rsquo;s slider runs from gasoline to honey and its three ticks are the named fluids. '
      +'&rho;g here is <b>'+fmt(st.rho*st.grav/1000,3)+'</b> kPa per metre of depth.';
    worldTag.innerHTML='PhET&rsquo;s gravity slider runs Mars to Jupiter. Switching the atmosphere off drops the '
      +'intercept to zero, so the gauge reads <b>gauge pressure</b> &mdash; and it makes the press exact: '
      +'&Delta;h = M/(&rho;A<sub>1</sub>) with no air to weigh.';
    poolTag.innerHTML='the faucet and the drain set the level. This is a level control, not a flow rate, so nothing is '
      +'animated. The grid and the ruler follow the unit chips: metres, or feet at 0.3048 m exactly.';
    gaugeTag.innerHTML='drag either gauge on the canvas, or place it here. Outside the pool a gauge reads nothing; '
      +'above the surface it reads the air.';
    stackTag.innerHTML='PhET carries one 500 kg and two 250 kg masses. On '+fmt(CH_A_L,2)+' m&sup2; the whole stack adds '
      +'<b>'+fmt(CH_MASS_MAX*st.grav/CH_A_L/1000,2)+'</b> kPa to every point of the fluid.';
    myTag.innerHTML='pick which one is in the pool, read the gauge, then answer. The densities and the planet are hidden '
      +'until you show the answer.';
    vesTag.innerHTML='four vessels, one base of '+fmt(VESSELS[0].prof[0][1]*DEPTH_OUT,2)+' m&sup2;, one depth. The '
      +'highlighted one is the one the readout takes apart.';
    lineTag.innerHTML='the marker reads the line at this depth. Every unit chip relabels the axis; none of them moves '
      +'the line.';
    unitTag.innerHTML='kPa, atm and psi. 1 atm = 101325 Pa exactly and 1 psi = <b>'+fmt(PA_PER_PSI,6)+'</b> Pa exactly, '
      +'so 1 atm = '+fmt(PA_PER_ATM/PA_PER_PSI,8)+' psi.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M,st);
      eqEl.innerHTML=eqbarHTML(M,st);
      tagEl.innerHTML=tagHTML(M,st);
      hintEl.textContent=(sceneOf(st.view)&&st.view!=='mystery'?'drag a gauge · ':'')+'1–6 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model(),st); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key==='r'){ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; clearAll(); syncChips(); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  function frameLoop(){
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  pool:'This is PhET&rsquo;s square pool. Fill it with the faucet, empty it with the drain, and drag the two gauges '
    +'anywhere you like. The reading is p<sub>atm</sub> + &rho;gh and nothing else: not the width of the pool, not how '
    +'much fluid is in it, not what the container is made of. Put both gauges at the same depth and the two numbers are '
    +'identical to the last digit; move one sideways and it does not change at all. The two sliders change exactly the '
    +'two things the law has &mdash; &rho; and g &mdash; and the atmosphere switch removes the intercept, which is the '
    +'difference between absolute pressure and gauge pressure. The force on the floor and the weight of the fluid in the '
    +'readout are deliberately printed together: they are equal only when the atmosphere is off, because otherwise the '
    +'floor is also carrying the air standing on the surface.',
  shapes:'PhET&rsquo;s trapezoid pool is the hydrostatic paradox, set up as an experiment you can do. The left chamber '
    +'is narrow at the top and wide at the bottom; the right one is the same shape turned over; a channel along the '
    +'floor joins them, so the fluid is one connected body and the two surfaces must stand level. Now put a gauge in '
    +'each, at the same depth. There is several times as much fluid standing over one of them as the other, and the two '
    +'read the same number. The panel beside the pool shows something else these two shapes happen to have: their widths '
    +'are equal and opposite linear functions of height, so they SUM to a constant, which is why the level here rises '
    +'uniformly with the volume even though neither chamber alone would.',
  press:'A pressure applied anywhere in an enclosed fluid appears everywhere in it &mdash; that is Pascal&rsquo;s '
    +'principle, and this is the machine you build out of it. The small piston has an area of '+fmt(CH_A_L,2)+' m&sup2; '
    +'and the large one '+fmt(CH_A_R,2)+' m&sup2;. A load on the small one adds F/A to the pressure at every point, so '
    +'the large piston feels that same pressure over '+fmt(CH_RATIO,1)+' times the area and therefore '+fmt(CH_RATIO,1)
    +' times the force. Nothing is created: the small side sinks '+fmt(CH_RATIO,1)+' times as far as the large side '
    +'rises, so force &times; distance is the same on both. The one subtlety is that with the atmosphere on the air '
    +'between the two surfaces has weight of its own, so the exact answer is &Delta;h = M/(A<sub>1</sub>(&rho; + '
    +'&lambda;/g<sub>earth</sub>)) &mdash; the air simply subtracts its own 1.25 kg/m&sup3;. Switch the atmosphere off '
    +'and the classical M/(&rho;A<sub>1</sub>) is exact.',
  mystery:'Here either the fluid or the planet is hidden and you have one number. That is enough, because the law has '
    +'only three things in it on the right and you are given two of them. With the fluid hidden, &rho; = (p &minus; '
    +'p<sub>atm</sub>)/gh, and the three candidates PhET offers separate cleanly at any real depth. With the planet '
    +'hidden it is subtler: PhET scales the air pressure by g/g<sub>earth</sub> as well as the &rho;gh term, so g has to '
    +'be solved out of p = P<sub>0</sub>g/g<sub>0</sub> + &rho;gh &mdash; which is still one division, and which means '
    +'the planets are distinguishable even at zero depth while the fluids are not. At the surface all three fluids read '
    +'exactly the air pressure, and the readout says so instead of offering an answer.',
  paradox:'Four vessels, the same base, the same depth of the same fluid, and between 3.1 and 8.4 cubic metres in them. '
    +'The force on every base is the same. It has to be: the force is the pressure times the area, and the pressure at '
    +'the base is &rho;gh whatever is happening further up. The weight of fluid is not what the base carries. What '
    +'carries the rest is the slanted wall &mdash; a vessel that widens with height has walls that hold fluid up, a '
    +'vessel that narrows has walls that push down, and either way the vertical part of the pressure on them is exactly '
    +'W &minus; F<sub>base</sub>. This view integrates that wall force directly, by '
    +'&int;p(y)w&prime;(y)D dy over the profile, and prints how far it is from W &minus; F<sub>base</sub>. It is zero '
    +'to machine precision, and it has to be computed independently or the check means nothing.',
  column:'Strip the pictures away and the whole simulation is one straight line. Pressure against depth is p = '
    +'p<sub>atm</sub> + &rho;gh: intercept p<sub>atm</sub>, slope &rho;g. The fluid slider tilts it. The gravity slider '
    +'tilts it and lifts the intercept with it, because PhET scales the air pressure by g/g<sub>earth</sub>. The '
    +'atmosphere switch drops the intercept to zero. That is every control in the file. The unit chips do none of those '
    +'things: they relabel the vertical axis, which is why the three scales are drawn on one picture underneath with the '
    +'same physical pressure marked on all three. The conversions are exact by definition, and the panel prints how far '
    +'PhET&rsquo;s rounded factors are from them.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  pool:'<h4>the hydrostatic law</h4>'
    +EQ(1,'dp/dy = &minus;&rho;g &nbsp; <span class="rm">(a slab of fluid in equilibrium)</span>')
    +EQ(2,'p(y) = p<sub>atm</sub>(y<sub>s</sub>) + &rho;g(y<sub>s</sub> &minus; y) = p<sub>atm</sub> + &rho;gh')
    +EQ(3,'p<sub>atm</sub>(y) = (101325 + &lambda;y)&middot;g/g<sub>0</sub>, &nbsp; &lambda; = &minus;12.2333 Pa/m &nbsp; <span class="rm">(PhET)</span>')
    +EQ(4,'F<sub>floor</sub> = pA = (p<sub>atm</sub> + &rho;gh)A &nbsp;&ne;&nbsp; W = &rho;gV <span class="rm">unless the atmosphere is off</span>')
    +'<p>PhET&rsquo;s air pressure is a straight line over the first 150 m. A real isothermal column falls as '
    +'exp(&minus;y/H<sub>s</sub>) with H<sub>s</sub> = 8434.5 m; the two are never more than 49 Pa apart over that '
    +'range, which is 0.048 % of an atmosphere, and selfTest asserts it.</p>'
    +'<div class="cite">pins: p at 3 fluids &times; 3 gravities &times; 3 depths, with the atmosphere on and off; the '
    +'11466-point slider sweep; the surface reading equal to the air pressure exactly &mdash; derive.py</div>',
  shapes:'<h4>the two tapers</h4>'
    +EQ(1,'w<sub>L</sub>(t) = 3.15 &minus; (2.45/3)t, &nbsp; w<sub>R</sub>(t) = 0.7 + (2.45/3)t')
    +EQ(2,'w<sub>L</sub> + w<sub>R</sub> = 3.85 m &nbsp; <span class="rm">for every t &mdash; the tapers cancel</span>')
    +EQ(3,'V(t) = '+fmt(TZ_WCHAN,3)+'&middot;D&middot;t <span class="rm">(t &le; 0.21)</span>, &nbsp; V<sub>chan</sub> + 3.85&middot;D&middot;(t &minus; 0.21) <span class="rm">above</span>')
    +EQ(4,'p<sub>L</sub>(h) = p<sub>R</sub>(h) &nbsp; <span class="rm">at every depth h, whatever is above</span>')
    +'<p>The cross-section through the floor channel is one band '+fmt(TZ_WCHAN,3)+' m wide that slides sideways with '
    +'height rather than changing width, so the volume is piecewise linear with one kink and inverts exactly.</p>'
    +'<div class="cite">pins: the constant width sum at 40 heights; V(t) against scipy.integrate.quad at five levels; '
    +'the volume&ndash;level round trip to 1e-12; the two gauges equal to 1e-12 Pa at equal depth &mdash; derive.py</div>',
  press:'<h4>Pascal, solved rather than asserted</h4>'
    +EQ(1,'&Delta;p = F<sub>1</sub>/A<sub>1</sub> &nbsp; <span class="rm">added everywhere in the connected fluid</span>')
    +EQ(2,'p<sub>atm</sub>(y<sub>L</sub>) + &Delta;p + &rho;g(y<sub>L</sub>&minus;y) = p<sub>atm</sub>(y<sub>R</sub>) + &rho;g(y<sub>R</sub>&minus;y)')
    +EQ(3,'&rArr; &Delta;p = (&rho;g + &lambda;)&Delta;h &nbsp;&rArr;&nbsp; &Delta;h = '+FR('M','A<sub>1</sub>(&rho; + &lambda;/g<sub>0</sub>)')+' &nbsp; <span class="rm">g cancels</span>')
    +EQ(4,'A<sub>1</sub>&delta;<sub>1</sub> = A<sub>2</sub>&delta;<sub>2</sub>, &nbsp; F<sub>2</sub> = &Delta;p A<sub>2</sub> = '+fmt(CH_RATIO,1)+' F<sub>1</sub>, &nbsp; F<sub>1</sub>&delta;<sub>1</sub> = F<sub>2</sub>&delta;<sub>2</sub>')
    +'<p>[2] is the statement that the pressure at one point does not depend on the route taken to it, and it is what '
    +'makes [3] a derivation rather than a definition. With the atmosphere off &lambda; = 0 and [3] is the classical '
    +'M/(&rho;A<sub>1</sub>) exactly.</p>'
    +'<div class="cite">pins: &Delta;h at five loads both ways; the closed form at three gravities; the two routes to '
    +'p(y = &minus;2.5) agreeing to 1e-9 Pa at every mass, fluid and atmosphere setting &mdash; derive.py</div>',
  mystery:'<h4>one reading, one unknown</h4>'
    +EQ(1,'&rho; = '+FR('p &minus; p<sub>atm</sub>','g h')+' &nbsp; <span class="rm">has no value at h = 0</span>')
    +EQ(2,'p = P<sub>0</sub>'+FR('g','g<sub>0</sub>')+' + &rho;gh &nbsp;&rArr;&nbsp; g = '+FR('p','P<sub>0</sub>/g<sub>0</sub> + &rho;h'))
    +EQ(3,'<span class="rm">fluids: closest pair 127.4 Pa apart at h = 0.05 m, 3822 Pa at h = 1.5 m</span>')
    +EQ(4,'<span class="rm">planets: 62036 Pa apart even at h = 0 &mdash; the air term carries g</span>')
    +'<p>[1] is why a surface reading cannot name a fluid, and [2] is why it can name a planet. Both inversions are '
    +'exact, with residuals at the 1e-13 level.</p>'
    +'<div class="cite">pins: each candidate&rsquo;s reading at h = 1.5 m; both inversions recovering PhET&rsquo;s value; '
    +'the minimum separation over depths 0.05&ndash;3.00 m &mdash; derive.py</div>',
  paradox:'<h4>base, weight, walls</h4>'
    +EQ(1,'F<sub>base</sub> = &rho;ghA<sub>base</sub> &nbsp; <span class="rm">the same for all four</span>')
    +EQ(2,'W = &rho;gD&int;w(y)dy &nbsp; <span class="rm">exact on a piecewise-linear profile</span>')
    +EQ(3,'F<sub>wall,z</sub> = D&int;<sub>0</sub><sup>h</sup> p(y)w&prime;(y)dy = &rho;gDk'+FR('h&sup2;','2')+' <span class="rm">per linear segment</span>')
    +EQ(4,'F<sub>wall,z</sub> = W &minus; F<sub>base</sub> &nbsp; <span class="rm">force balance &mdash; never used to get [3]</span>')
    +'<p>Each wall&rsquo;s inward normal is (&mp;1, w&prime;/2)/&radic;(1+(w&prime;/2)&sup2;) and its area element carries '
    +'the same &radic;, so the root cancels and the vertical part is p w&prime;/2 per wall, twice over.</p>'
    +'<div class="cite">pins: the four volumes against scipy.quad and a 400 000-strip sum; F/W = 1, 0.5714, 1.5484, '
    +'0.6738 independent of fluid and gravity; [3] against [4] to 1e-9 relative &mdash; derive.py</div>',
  column:'<h4>the units, from their definitions</h4>'
    +EQ(1,'1 atm &equiv; 101325 Pa &nbsp; <span class="rm">(CGPM 1954)</span>')
    +EQ(2,'1 lbf = 0.45359237 &times; 9.80665 N, &nbsp; 1 in = 0.0254 m &nbsp;&rArr;&nbsp; 1 psi = '+fmt(PA_PER_PSI,9)+' Pa')
    +EQ(3,'1 atm = '+fmt(PA_PER_ATM/PA_PER_PSI,8)+' psi = 101.325 kPa')
    +EQ(4,'h(1 atm of water) = '+FR('101325','&rho;g')+' = '+fmt(PA_PER_ATM/(RHO_WATER*G_EARTH),4)+' m <span class="rm">(9.8)</span>, '+fmt(PA_PER_ATM/(RHO_WATER*G_STD),4)+' m <span class="rm">(9.80665)</span>')
    +'<p>PhET stores the rounded 9.8692e-6 atm/Pa and 1.4504e-4 psi/Pa; at one atmosphere those are 3.3e-6 atm and '
    +'2.3e-4 psi from the exact values. This file uses the definitions and round-trips every conversion to 1.4e-16.</p>'
    +'<div class="cite">pins: all three constants; the round trip over 0&ndash;4 MPa; the three scales at five depths '
    +'&mdash; derive.py</div>',
};
