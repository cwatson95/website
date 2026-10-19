
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
  let dirty=false;      /* only the pointer and the wheel set it; every other path calls refresh() */

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k;
    [].forEach.call(tabsEl.children,(bt,i)=>bt.className=TABS[i][0]===st.view?'active':'');
    fieldReset(); syncChips(); syncPanel(); refresh();
  }
  S.onView=setView;
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      if(onchg) onchg(); val.textContent=fmtf(st[key]); syncPanel(); refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg(); syncPanel(); refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        [].forEach.call(wrapEl.children,(bt,i)=>bt.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  const BTN={};
  function btn(label,fn){ const bt=h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); refresh(); }},label); BTN[label]=bt; return bt; }

  /* --- electronegativity: PhET's sliders, 2 to 4, snapping to 0.2 --- */
  const gEN=h('div',{class:'grp'},h('h3',null,'electronegativity'));
  gEN.appendChild(slider('enA','atom A',EN_MIN,EN_MAX,EN_STEP,v=>fmt(v,1),()=>{ st.enA=snapEN(st.enA); FIELD.w=0; }));
  gEN.appendChild(slider('enB','atom B',EN_MIN,EN_MAX,EN_STEP,v=>fmt(v,1),()=>{ st.enB=snapEN(st.enB); FIELD.w=0; }));
  const rowC=slider('enC','atom C',EN_MIN,EN_MAX,EN_STEP,v=>fmt(v,1),()=>{ st.enC=snapEN(st.enC); FIELD.w=0; });
  gEN.appendChild(rowC);
  const enTag=h('div',{class:'tag'}); gEN.appendChild(enTag);

  /* --- the bond angle (three atoms, the vector sum) --- */
  const gGeom=h('div',{class:'grp'},h('h3',null,'the bond angle'));
  const angRow=h('div',{class:'sliderrow'},h('label',null,'A&ndash;B&ndash;C'),
    h('input',{type:'range',min:0,max:180,step:0.5,value:120}),h('span',{class:'val'}));
  const angInp=angRow.children[1], angVal=angRow.children[2];
  angInp.addEventListener('input',()=>{ setBondAngleDeg(parseFloat(angInp.value)); syncPanel(); refresh(); });
  rows.bondAngle={row:angRow,sync:()=>{ const d=Math.abs(normAngle(st.angAB-st.angBC,-PI))*180/PI;
    angInp.value=d; angVal.textContent=fmt(d,1)+'°'; }};
  gGeom.appendChild(angRow);
  gGeom.appendChild(h('div',{class:'btnrow'},btn('linear 180°',()=>setBondAngleDeg(180)),
    btn('water 104.5°',()=>setBondAngleDeg(104.5)),btn('120°',()=>setBondAngleDeg(120))));
  const geomTag=h('div',{class:'tag'}); gGeom.appendChild(geomTag);

  /* --- PhET's View checkboxes --- */
  const gView=h('div',{class:'grp'},h('h3',null,'view'));
  const viewChecks=h('div',{class:'checks'},
    checkbox('showBondDipole','bond dipole(s)'),
    checkbox('showMolDipole','molecular dipole'),
    checkbox('showCharges','partial charges'),
    checkbox('showBondChar','bond character'),
    checkbox('showLabels','atom labels'));
  gView.appendChild(viewChecks);

  /* --- PhET's Surface control --- */
  const gSurf=h('div',{class:'grp'},h('h3',null,'surface'));
  const SURF_LIST=[{id:'none',name:'none'},{id:'density',name:'electron density'},
                   {id:'potential',name:'electrostatic potential'}];
  gSurf.appendChild(chipRow(SURF_LIST,'surface'));
  const COLOUR_LIST=[{id:'rwb',name:'blue–white–red'},{id:'roygb',name:'rainbow'}];
  gSurf.appendChild(chipRow(COLOUR_LIST,'surfColor'));
  const surfTag=h('div',{class:'tag'}); gSurf.appendChild(surfTag);

  /* --- the electric field --- */
  const gField=h('div',{class:'grp'},h('h3',null,'the electric field'));
  gField.appendChild(h('div',{class:'checks'},checkbox('field','electric field on',()=>{ fieldReset(); })));
  const MODE_LIST=[{id:'rotor',name:'damped rotor'},{id:'phet',name:'PhET’s rule'}];
  gField.appendChild(chipRow(MODE_LIST,'fieldMode',()=>fieldReset()));
  gField.appendChild(slider('fieldE','field E',0.1,2,0.05,v=>fmt(v,2),()=>fieldReset()));
  gField.appendChild(slider('zeta','damping ζ',0.1,3,0.05,v=>fmt(v,2),()=>fieldReset()));
  gField.appendChild(h('div',{class:'btnrow'},btn('turn the molecule 150°',()=>{ setFieldPsi(150*PI/180); fieldReset(); })));
  const fieldTag=h('div',{class:'tag'}); gField.appendChild(fieldTag);

  /* --- the field view's start angle --- */
  const gStart=h('div',{class:'grp'},h('h3',null,'the alignment run'));
  gStart.appendChild(slider('psi0','start ψ',-180,180,1,v=>fmt(v,0)+'°'));
  const startTag=h('div',{class:'tag'}); gStart.appendChild(startTag);

  /* --- the real molecules --- */
  const gMol=h('div',{class:'grp'},h('h3',null,'molecule'));
  const MOLCHIPS=MOLORDER.map(id=>({id,name:id}));
  gMol.appendChild(chipRow(MOLCHIPS,'mol'));
  const REALMODE=[{id:'basic',name:'basic'},{id:'advanced',name:'advanced'}];
  gMol.appendChild(chipRow(REALMODE,'realMode'));
  const molTag=h('div',{class:'tag'}); gMol.appendChild(molTag);

  /* --- PhET's preference --- */
  const gPref=h('div',{class:'grp'},h('h3',null,'dipole direction'));
  const DIRS=[{id:'posneg',name:'positive → negative'},{id:'negpos',name:'negative → positive'}];
  gPref.appendChild(chipRow(DIRS,'dipoleDir'));
  const prefTag=h('div',{class:'tag'}); gPref.appendChild(prefTag);

  const gReset=h('div',{class:'grp'},h('h3',null,'reset'));
  gReset.appendChild(h('div',{class:'btnrow'},btn('reset view',()=>S.resetCam()),
    btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; fieldReset(); S.resetCam(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Molecule Polarity (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values (build 2.0.2): the electronegativity range 2&ndash;4 '
      +'and its 0.2 step, the bond length 150 and atom diameter 100, the 5&pi;/6 and &pi;/6 opening angles, the surface gradient multiplier 5, '
      +'135 px per &Delta;EN = 2, the 415-px bond-character bar and its six bands, the 0.17 rad e-field constant, the RWB and 35-stop rainbow ramps, '
      +'and the whole real-molecule table (PubChem geometry, ORCA Hirshfeld charges, Psi4 dipole moments). Measured dipole moments and bond angles: '
      +'NIST CCCBDB (cccbdb.nist.gov), retrieved 2026-09-22, to the precision it prints. Every model number is pinned in selfTest to '
      +'build/molecule-polarity/derive.py, the Python twin.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gEN,gGeom,gView,gSurf,gField,gStart,gMol,gPref,gReset,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(bt,i)=>bt.className='chip'+(list[i].id===st[key]?' on':''));
  }
  function syncPanel(){
    const v=st.view, model=(v==='two'||v==='three');
    gEN.hidden=!(model||v==='sum'||v==='field');
    rowC.hidden=(v==='two');
    gGeom.hidden=!(v==='three'||v==='sum'||v==='field');
    gView.hidden=!(model||v==='real');
    rows.cb_showMolDipole.row.hidden=(v==='two');
    rows.cb_showBondChar.row.hidden=(v!=='two');
    gSurf.hidden=(v!=='two');
    gField.hidden=!model;
    gStart.hidden=(v!=='field');
    rows.zeta.row.hidden=!(v==='field'||(model&&st.fieldMode==='rotor'));
    rows.fieldE.row.hidden=!(v==='field'||model);
    gMol.hidden=(v!=='real');
    gPref.hidden=!(model||v==='real');
    for(const k in rows) rows[k].sync();
    const dEN=st.enB-st.enA;
    enTag.innerHTML='PhET&rsquo;s sliders run 2.0 to 4.0 and snap to 0.2. &Delta;EN(A&rarr;B) = <b>'+fmt(dEN,1)
      +'</b>, which is the bond dipole&rsquo;s magnitude exactly.';
    geomTag.innerHTML='PhET opens at 120&deg; (bond angles 5&pi;/6 and &pi;/6). At 180&deg; with EN(A) = EN(C) the molecular dipole is <b>exactly</b> zero.';
    surfTag.innerHTML='Black = more electron density; red = negative potential. The gradient narrows as &Delta;EN grows: '
      +(st.surface==='none'?'pick a surface to see it.':'<b>'+fmt(gradWidth(st.surface,dEN),0)+'</b> wide over a '+fmt(surfaceWidth(),0)+' surface.')
      +' The rainbow scheme is PhET&rsquo;s Real-Molecules-only option.';
    fieldTag.innerHTML='PhET&rsquo;s plates: <span class="r">negative left</span>, <span class="g">positive right</span>, so E points in &minus;x and the '
      +'positive-to-negative arrow ends pointing right. '+(st.fieldMode==='phet'
        ?'PhET&rsquo;s rule moves it <b>'+fmt(phetFieldStep(vmag(molAt(v==='three'?'three':'two',0).mu)),4)+'</b> rad a frame.'
        :'&zeta; &lt; 1 overshoots, &zeta; = 1 is critical, &zeta; &gt; 1 creeps.');
    startTag.innerHTML='Where the dipole starts, in degrees from alignment. Drag the top panel to set it.';
    const r=realMol(st.mol);
    molTag.innerHTML='<b>'+r.sym+'</b> '+r.name+' &mdash; '+r.syms.length+' atoms, '+r.bonds.length+' bonds'
      +(measuredOf(st.mol)?', measured |&mu;| = <b>'+fmt(measuredOf(st.mol)[0],3)+'</b> D':', no measured value');
    prefTag.innerHTML='PhET&rsquo;s preference. Chemists draw the arrow from &delta;+ to &delta;&minus;; the physicist&rsquo;s <b>p</b> = q<b>d</b> points the other way.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      const v=st.view;
      hintEl.textContent=v==='two'?'drag to turn the molecule · wheel to zoom · 1–6 switch views'
        :v==='three'?'drag A or C to set the angle · drag elsewhere to turn · 1–6 switch views'
        :v==='real'?'drag to turn · the wheel zooms · 1–6 switch views'
        :v==='sum'?'drag the top panel to set the bond angle · 1–6 switch views'
        :v==='field'?'drag the top panel to set the starting angle · 1–6 switch views'
        :'1–6 switch views';
      infoEl.innerHTML=INFO[v]||'';
      physEl.innerHTML=DERIV[v]||'';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;
      if(ST.view==='sum'||ST.view==='field'||ST.view==='three') refresh(); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  canvas.addEventListener('wheel',e=>{ e.preventDefault(); if(S.wheel(e.deltaY)) dirty=true; },{passive:false});

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.field=!st.field; fieldReset(); syncPanel(); refresh(); }
    else if(e.key==='r'){ S.resetCam(); refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); refresh(); });

  let frameN=0, last=0, wasBusy=false;
  function frameLoop(tm){
    frameN++;
    const dtw=last?Math.min((tm-last)/1000,0.05):0; last=tm;
    const advanced=S.step(dtw);
    if(advanced||dirty){
      dirty=false;
      try{ S.draw(); if(advanced&&frameN%8===0) roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); }
    }
    if(wasBusy&&!advanced){ try{ syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); } }
    wasBusy=advanced;
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  two:'PhET&rsquo;s first screen. Two atoms, one bond, and two sliders that set how strongly each atom pulls on the shared electrons. '
    +'The difference between those two electronegativities, &Delta;EN, is the whole model: the bond dipole is a vector along the bond whose length '
    +'is |&Delta;EN| and which points at the greedier atom, and the partial charges are &plusmn;&Delta;EN. Turn on the partial charges to watch '
    +'&delta;+ and &delta;&minus; grow as you pull the sliders apart, and the bond-character bar slide from covalent toward ionic. The surface is '
    +'the same quantity painted as colour: electron density in black and white, electrostatic potential in red, white and blue &mdash; red where the '
    +'potential is negative, which is where the electrons have gone. Switch the field on and the molecule turns until the dipole points at the '
    +'positive plate. Nothing here is in debye, and that is deliberate: a dipole moment that is exactly linear in electronegativity is a teaching '
    +'model, not a measurement.',
  three:'PhET&rsquo;s second screen, and the point of the whole simulation. Two bonds now, so two bond dipoles, and the molecular dipole is their '
    +'vector sum. Drag atom A or atom C round the middle and watch the sum change with nothing else changing: same bonds, same charges, different '
    +'molecule. Straighten the angle to 180&deg; with A and C the same and the sum is not small, it is exactly zero &mdash; the two arrows are equal '
    +'and opposite. That is carbon dioxide: two of the most polar bonds in ordinary chemistry, and no molecular dipole at all. Bend it and the '
    +'dipole appears; that is water. PhET draws no surface on this screen, because dragging the bond angle leaves the surface undefinable, and '
    +'neither does this file.',
  real:'PhET&rsquo;s third screen: nineteen real molecules in three dimensions, with its own data. Basic keeps the two model screens&rsquo; rule and '
    +'applies it to Pauling electronegativities, so every bond dipole is |&Delta;EN| and the molecular one is their sum. Advanced swaps in quantum '
    +'chemistry: Hirshfeld partial charges from ORCA give each bond dipole in debye, and the molecular dipole is Psi4&rsquo;s, computed from the '
    +'electron density. The measured value sits beside it. Two things are worth noticing. The nine symmetric molecules come out non-polar to five '
    +'decimal places, which is the vector sum doing its work in three dimensions. And PhET&rsquo;s geometry is PubChem&rsquo;s, not the measured one: '
    +'ammonia is stored at 95.1&deg; where it measures 106.7&deg;, and water at 97.9&deg; where it measures 104.5&deg;, which is most of why '
    +'water&rsquo;s computed dipole comes out 0.34 D low.',
  sum:'One plot for the idea the simulation is built on. Two vectors of fixed length, with an angle between them: the length of their sum runs '
    +'from |&Delta;<sub>AB</sub> &minus; &Delta;<sub>BC</sub>| when they lie along each other at &theta; = 0 to |&Delta;<sub>AB</sub> + '
    +'&Delta;<sub>BC</sub>| when the bonds are straight. When the two end atoms are the same the bond dipoles are equal and opposite along the '
    +'bonds, the second of those is zero, and the cancellation is exact &mdash; not small, not numerical, identically zero, because the sum is '
    +'2|&Delta;EN| cos(&theta;/2) and cos 90&deg; = 0. Drag along the top panel to move the molecule round the curve. The head-to-tail panel is '
    +'the same statement drawn rather than plotted.',
  field:'PhET switches a field on and the molecule turns until the dipole lines up. What does the turning really obey? A dipole &mu; in a field E '
    +'has energy &minus;&mu;&middot;E, so a torque &minus;&mu;E sin&psi; about alignment: the molecule is a pendulum. Give it a moment of inertia '
    +'and some damping and you get I&psi;&#776; = &minus;&mu;E sin&psi; &minus; b&psi;&#775;, whose stable equilibrium is &psi; = 0 and whose only '
    +'other equilibrium, &psi; = 180&deg;, is unstable &mdash; start there exactly and nothing happens, start a thousandth of a radian away and it '
    +'falls. The energy can only fall, so alignment is reached from everywhere else. The damping decides the style: overshoot, critical, or creep. '
    +'PhET does none of this; it moves the angle a fixed 0.085|&mu;| radians every frame, which is the orange line &mdash; straight, frame-rate '
    +'dependent, and stopping dead on arrival. Both are here; the chip in the field panel switches the molecule screens between them.',
  atlas:'The nineteen molecules laid out against measurement. The quantum column does well: its mean miss is about a tenth of a debye and hydrogen '
    +'cyanide lands within 0.003 D. Its two clear failures, water and ozone, are both geometry: the stored PubChem structures are 6.6&deg; and '
    +'2.7&deg; away from the measured ones. The lower panel is the Basic model&rsquo;s turn, and it is the honest limit of the whole '
    +'electronegativity idea. Basic has no unit &mdash; its numbers are sums of &Delta;EN, not debye &mdash; so all it can offer is an ordering, and '
    +'even that breaks: ozone is three oxygen atoms, every &Delta;EN is zero, and the model calls it non-polar. It measures 0.530 D. A bond dipole '
    +'is not a function of electronegativity alone, which is exactly what PhET&rsquo;s own model notes say.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  two:'<h4>the bond dipole</h4>'
    +EQ(1,'&Delta;EN = EN(B) &minus; EN(A), &nbsp; <b>&mu;</b> = &Delta;EN &middot; <b>u</b><sub>A&rarr;B</sub>')
    +EQ(2,'q<sub>A</sub> = +&Delta;EN, &nbsp; q<sub>B</sub> = &minus;&Delta;EN, &nbsp; q<sub>A</sub> + q<sub>B</sub> = 0')
    +EQ(3,'<span class="rm">gradient width</span> = linear(1, 0, W, 5W, |&Delta;EN|/2), &nbsp; W = 150 + 2&times;2.25&times;50 = 375')
    +'<p>PhET builds the dipole as createPolar(|&Delta;EN|, &alpha;) with &alpha; the bond angle plus &pi; when &Delta;EN &lt; 0. That is the same '
    +'vector as [1] in one line, and selfTest asserts the two agree over the whole slider grid. The surface gradient is PhET&rsquo;s: it is five times '
    +'the surface width at &Delta;EN = 0, so the whole surface reads the neutral colour, and exactly the surface width at &Delta;EN = 2.</p>'
    +'<div class="cite">pins: both branches over 1573 cases, the gradient widths and the stop colours at five positions, the six bond-character bands &mdash; derive.py</div>',
  three:'<h4>the vector sum</h4>'
    +EQ(1,'<b>&mu;</b><sub>mol</sub> = <b>&mu;</b><sub>AB</sub> + <b>&mu;</b><sub>BC</sub>')
    +EQ(2,'|<b>&mu;</b><sub>mol</sub>|&sup2; = &Delta;<sub>AB</sub>&sup2; + &Delta;<sub>BC</sub>&sup2; &minus; 2&Delta;<sub>AB</sub>&Delta;<sub>BC</sub> cos&theta;')
    +EQ(3,'q<sub>A</sub> = EN<sub>B</sub> &minus; EN<sub>A</sub>, &nbsp; q<sub>C</sub> = EN<sub>B</sub> &minus; EN<sub>C</sub>, &nbsp; q<sub>B</sub> = &minus;(q<sub>A</sub> + q<sub>C</sub>)')
    +'<p>[2] follows from <b>u</b><sub>A&rarr;B</sub> &middot; <b>u</b><sub>B&rarr;C</sub> = &minus;cos&theta; and is asserted against the '
    +'componentwise sum over 47&thinsp;916 (EN, EN, EN, &theta;) combinations, worst difference 3e&minus;15. The charges sum to zero identically, '
    +'checked over the whole 11&sup3; grid.</p>'
    +'<div class="cite">pins: the closed form, the charge sum, PhET&rsquo;s opening 120&deg; and its dipole angle &mdash; derive.py</div>',
  real:'<h4>PhET&rsquo;s two modes</h4>'
    +EQ(1,'<span class="rm">basic:</span> |<b>&mu;</b>| = |&Delta;EN|, <span class="rm">Pauling</span>')
    +EQ(2,'<span class="rm">advanced:</span> |<b>&mu;</b>| = '+FR('|q<sub>1</sub> &minus; q<sub>2</sub>|','2')+' &middot; '+FR('d','0.208194')+' <span class="rm">debye</span>')
    +EQ(3,'<span class="rm">arrow scale</span> = |<b>&mu;</b><sub>Psi4</sub>| / |&Sigma;<b>&mu;</b><sub>bond</sub>| &times; 0.75')
    +'<p>0.208194 is the debye in e&middot;&aring;ngstr&ouml;m, so [2] is just q d. PhET rescales the drawn arrows by [3] so the molecular arrow '
    +'carries the Psi4 magnitude while the bond arrows keep their ratios. The Hirshfeld charges sum to zero to 7e&minus;6 on every molecule, and the '
    +'nine symmetric ones cancel to 1.2e&minus;3 debye or better.</p>'
    +'<div class="cite">pins: all nineteen molecules&rsquo; bond dipoles, sums, arrow scales, bond angles and lengths &mdash; derive.py</div>',
  sum:'<h4>the cancellation</h4>'
    +EQ(1,'<span class="rm">EN(A) = EN(C):</span> &nbsp; &Delta;<sub>BC</sub> = &minus;&Delta;<sub>AB</sub>')
    +EQ(2,'|<b>&mu;</b>|&sup2; = 2&Delta;&sup2;(1 + cos&theta;) = 4&Delta;&sup2; cos&sup2;(&theta;/2)')
    +EQ(3,'|<b>&mu;</b>| = 2|&Delta;EN| |cos(&theta;/2)| &rArr; 0 <span class="rm">at</span> &theta; = 180&deg;')
    +'<p>The zero is an identity of the sum, not a numerical accident: at &theta; = 180&deg; the two bond dipoles are the same vector with opposite '
    +'signs. Over the whole 121-pair electronegativity grid the computed magnitude at 180&deg; never exceeds 7.3e&minus;16, which is rounding in the '
    +'trigonometry, and the law [3] agrees with the componentwise sum to 2.2e&minus;15.</p>'
    +'<div class="cite">pins: the 180&deg; zero, the symmetric law, the two ends |&Delta;<sub>AB</sub> &plusmn; &Delta;<sub>BC</sub>| &mdash; derive.py</div>',
  field:'<h4>the damped rotor</h4>'
    +EQ(1,'W(&psi;) = &minus;<b>p</b>&middot;<b>E</b> = &minus;&mu;E cos&psi;, &nbsp; &tau; = &minus;&part;W/&part;&psi; = &minus;&mu;E sin&psi;')
    +EQ(2,'I&psi;&#776; + b&psi;&#775; + &mu;E sin&psi; = 0, &nbsp; &omega;&#8320; = &radic;(&mu;E/I), &nbsp; b<sub>c</sub> = 2&radic;(I&mu;E)')
    +EQ(3,'<span class="rm">d/dt</span>(&frac12;I&psi;&#775;&sup2; + &mu;E(1&minus;cos&psi;)) = &minus;b&psi;&#775;&sup2; &le; 0')
    +'<p>[3] is the Lyapunov function: the energy can only fall, so every orbit but the one starting exactly at &psi; = &pi; ends at &psi; = 0. '
    +'The RK4 used here agrees with scipy&rsquo;s adaptive solver to 2e&minus;12 at t = 3, the small-angle limit reproduces the linear solution '
    +'e<sup>&minus;&zeta;&omega;&#8320;t</sup>(cos&omega;<sub>d</sub>t + &hellip;) to 2e&minus;10 relative, and the zero-crossing count is 9 at '
    +'&zeta; = 0.2 and 0 at &zeta; &ge; 1. PhET&rsquo;s rule instead takes 16 frames from 150&deg; at |&mu;| = 2 and 77 at |&mu;| = 0.4.</p>'
    +'<div class="cite">pins: &omega;&#8320;, b<sub>c</sub>, four damping traces with their energy monotonicity, scipy, the crossing counts, PhET&rsquo;s frame counts &mdash; derive.py</div>',
  atlas:'<h4>computed against measured</h4>'
    +EQ(1,'<span class="rm">mean</span> | |&mu;|<sub>Psi4</sub> &minus; |&mu;|<sub>meas</sub> | = 0.104 D <span class="rm">over 18 molecules</span>')
    +EQ(2,'<span class="rm">Spearman &rho; on the 10 polar ones:</span> 0.782 (Psi4), 0.188 (basic)')
    +EQ(3,'O<sub>3</sub>: &nbsp; &Delta;EN = 0 <span class="rm">on both bonds</span> &rArr; |<b>&mu;</b>|<sub>basic</sub> = 0, <span class="rm">measured</span> 0.530 D')
    +'<p>The rank correlation is computed in the Python twin with average ranks and pinned. The basic model&rsquo;s failure on ozone is structural, '
    +'not a tuning problem: it is what an electronegativity-only bond dipole must say about a homonuclear bent molecule.</p>'
    +'<div class="cite">pins: the nineteen Psi4 magnitudes, the measured table, the mean and worst differences, both rank correlations &mdash; derive.py; measured values NIST CCCBDB</div>',
};
