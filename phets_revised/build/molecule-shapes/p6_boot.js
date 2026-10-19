
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
  let dirty=false;      /* only the pointer and the wheel set it: every other path calls refresh(), which draws */
  liveInit();

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    if(k==='relax') relaxEnsure();
    syncChips(); syncPanel(); refresh();
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
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      const c=h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); refresh(); }},o.name);
      wrapEl.appendChild(c);
    });
    return wrapEl;
  }
  const CHIPROWS=[];
  function trackChips(g,list,key){ CHIPROWS.push([g,list,key]); }
  const BTN={};
  function btn(label,fn){ const b=h('button',{onclick:()=>{ fn(); syncPanel(); refresh(); }},label); BTN[label]=b; return b; }

  /* PhET: single, double and triple bonds (and, in Molecule Shapes, lone pairs) each
     have an add button and a remove button that takes off the last one of that kind */
  const gBond=h('div',{class:'grp'},h('h3',null,'bonding'));
  gBond.appendChild(h('div',{class:'btnrow'},btn('+ single',()=>liveAdd(1)),btn('+ double',()=>liveAdd(2)),btn('+ triple',()=>liveAdd(3))));
  gBond.appendChild(h('div',{class:'btnrow'},btn('− single',()=>liveRemove(1)),btn('− double',()=>liveRemove(2)),btn('− triple',()=>liveRemove(3))));
  let lpRow=null;
  if(HAS_LP){ lpRow=h('div',{class:'btnrow'},btn('+ lone pair',()=>liveAdd(0)),btn('− lone pair',()=>liveRemove(0))); gBond.appendChild(lpRow); }
  gBond.appendChild(h('div',{class:'btnrow'},btn('remove all',()=>liveRemoveAll())));
  const bondTag=h('div',{class:'tag'}); gBond.appendChild(bondTag);

  let gModel=null, modelTag=null;
  if(HAS_LP){
    gModel=h('div',{class:'grp'},h('h3',null,'the model'));
    gModel.appendChild(slider('rho','lone-pair radius ρ',RHO_MIN,RHO_MAX,0.01,v=>fmt(v,2),()=>{ LIVE.anim=true; }));
    modelTag=h('div',{class:'tag'}); gModel.appendChild(modelTag);
  }

  const gMol=h('div',{class:'grp'},h('h3',null,'molecule'));
  const MOLCHIPS=MOL_LIST.map(id=>({id,name:formulaText(id)}));
  const molChips=chipRow(MOLCHIPS,'mol'); gMol.appendChild(molChips); trackChips(gMol,MOLCHIPS,'mol');
  let modeChips=null;
  const MODE_LIST=[{id:'real',name:'real'},{id:'model',name:'model'}];
  if(HAS_LP){ modeChips=chipRow(MODE_LIST,'realMode'); gMol.appendChild(modeChips); trackChips(gMol,MODE_LIST,'realMode'); }
  const molTag=h('div',{class:'tag'}); gMol.appendChild(molTag);

  const gOpt=h('div',{class:'grp'},h('h3',null,'options'));
  const optChecks=h('div',{class:'checks'});
  if(HAS_LP) optChecks.appendChild(checkbox('showLP','show lone pairs'));
  optChecks.appendChild(checkbox('showAngles','show bond angles'));
  let outerRow=null;
  if(HAS_LP){ outerRow=checkbox('showOuterLP','show outer lone pairs'); optChecks.appendChild(outerRow); }
  gOpt.appendChild(optChecks);

  const gName=h('div',{class:'grp'},h('h3',null,'name'));
  const nameChecks=h('div',{class:'checks'},checkbox('showMolName','molecule geometry'));
  if(HAS_LP) nameChecks.appendChild(checkbox('showElName','electron geometry'));
  gName.appendChild(nameChecks);

  const gRelax=h('div',{class:'grp'},h('h3',null,'the descent'));
  gRelax.appendChild(h('div',{class:'btnrow'},btn('new random start',()=>{ RELAX.seed++; relaxReset(); })));
  const relaxTag=h('div',{class:'tag'}); gRelax.appendChild(relaxTag);

  const gView=h('div',{class:'grp'},h('h3',null,'view'));
  gView.appendChild(h('div',{class:'btnrow'},btn('reset view',()=>S.resetCam()),
    btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; liveInit(); LIVE.realBlend=0; RELAX.seed=0; relaxReset(); S.resetCam(); syncChips(); })));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; '+(VARIANT==='basics'?'Molecule Shapes: Basics':'Molecule Shapes')
      +' (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values: the real-molecule table (build 1.6.19; '
      +'&ldquo;pulled from a mix of PubChem and/or reconstructed from the best known bond angles&rdquo;, its notes say), '
      +(HAS_LP?'the lone pairs&rsquo; 7-to-10 radius, ':'')+'six pairs at most, the lone-pair slot order, the arc thresholds, the AXE names. '
      +'Every model number is pinned in selfTest to build/'+(VARIANT==='basics'?'molecule-shapes-basics':'molecule-shapes')+'/derive.py (a Python twin, scipy BFGS, a Hessian audit).'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gBond,gModel,gMol,gOpt,gName,gRelax,gView,gInfo,gPhys].forEach(g=>{ if(g) panel.appendChild(g); });
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [g,list,key] of CHIPROWS){
      for(const cw of g.querySelectorAll('.chips')){
        if(cw.children.length!==list.length) continue;
        let match=0; for(let i=0;i<list.length;i++) if(cw.children[i].textContent===list[i].name) match++;
        if(match===list.length) [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
      }
    }
  }
  /* a row the view ignores is hidden, never left live and inert; a button that
     cannot act is disabled */
  function syncPanel(){
    const v=st.view;
    gBond.hidden=(v!=='model');
    if(gModel) gModel.hidden=!(v==='model'||(v==='real'&&st.realMode==='model')||v==='table'||v==='squeeze'||(v==='relax'&&RELAX.e>0));
    gMol.hidden=(v!=='real');
    gOpt.hidden=!(v==='model'||v==='real');
    if(outerRow) outerRow.hidden=(v!=='real');
    gName.hidden=!(v==='model'||v==='real');
    gRelax.hidden=(v!=='relax');
    for(const o of [1,2,3]){ BTN[['','+ single','+ double','+ triple'][o]].disabled=!canAdd(o); BTN[['','− single','− double','− triple'][o]].disabled=!liveHasOrder(o); }
    if(HAS_LP){ BTN['+ lone pair'].disabled=!canAdd(0); BTN['− lone pair'].disabled=!liveHasOrder(0); }
    BTN['remove all'].disabled=LIVE.groups.length===0;
    for(const k in rows) rows[k].sync();
    const c=liveCounts();
    bondTag.innerHTML=c.x+' bond'+(c.x===1?'':'s')+(HAS_LP?', '+c.e+' lone pair'+(c.e===1?'':'s'):'')+' round A; PhET allows six pairs at most'
      +(HAS_LP&&!st.showLP?'; lone pairs are hidden, so none can be added':'');
    if(modelTag) modelTag.innerHTML='PhET&rsquo;s lone pairs sit at 7 against 10 for its bonds: &rho; = 0.70. At &rho; = 1 a lone pair is a bond and every angle is ideal.';
    molTag.innerHTML=REAL[st.mol]?formulaHTML(st.mol)+': '+axeHTML(REAL[st.mol].bonds.length,REAL[st.mol].clp)+', PhET&rsquo;s measured geometry'+(HAS_LP?'; the model chip swaps in the least-energy shape':''):'';
    relaxTag.innerHTML='the molecule of the model view'+(HAS_LP?' at the current &rho;':'')+'; space starts again';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      const v=st.view;
      hintEl.textContent=v==='model'?'drag a pair to move it · drag elsewhere to turn · 1–'+TABS.length+' switch views'
        :v==='real'?'drag to turn · the wheel zooms · 1–'+TABS.length+' switch views'
        :v==='table'?'click a shape to build it · drag to turn them · 1–'+TABS.length+' switch views'
        :v==='squeeze'?'drag the top panel to set ρ · 1–'+TABS.length+' switch views'
        :'space: a new random start · drag to turn · 1–'+TABS.length+' switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; if(st.view==='squeeze') refresh(); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ syncPanel(); refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  canvas.addEventListener('wheel',e=>{ e.preventDefault(); if(S.wheel(e.deltaY)) dirty=true; },{passive:false});

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); if(st.view==='relax'){ RELAX.seed++; relaxReset(); refresh(); } }
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
    /* the frame that settles repaints the readout and the buttons once */
    if(wasBusy&&!advanced){ try{ syncPanel(); roEl.innerHTML=readoutHTML(S.model()); }catch(e){ fail(e); } }
    wasBusy=advanced;
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  model:(HAS_LP
    ?'This is PhET&rsquo;s Model screen. A central atom A holds up to six electron pairs, each either a bond to another atom or a lone pair '
    +'that belongs to A alone. Every pair repels every other, so they spread out over the atom until the pushes balance, and where they end up '
    +'is the shape of the molecule. That is VSEPR, valence-shell electron-pair repulsion. The model here makes the rule literal: bonds sit on a '
    +'sphere of radius 1, lone pairs on a smaller one of radius &rho; because they are held by one nucleus rather than two, and every pair repels '
    +'every other with an energy 1/d&sup2;. The shape you see is the arrangement of least total energy. With no lone pairs it is always one of '
    +'five ideal shapes, exactly. A lone pair is closer to everything, so it pushes harder, and the bonds bend away from it: water&rsquo;s '
    +'two bonds close from 109.5&deg; toward 105&deg;. Drag &rho; to 1 and every angle springs back to its ideal value. Add or remove pairs, drag '
    +'one round the atom and let go, and switch on the angles and the two names: the electron geometry counts every pair, the molecule geometry '
    +'only the atoms.'
    :'This is PhET&rsquo;s Model screen in its Basics form. A central atom A holds up to six bonds, single, double or triple, and every bond '
    +'repels every other, so they spread out over the atom until the pushes balance. Where they end up is the shape. The model makes that '
    +'literal: every bond is a point on a sphere, every pair of bonds repels with an energy 1/d&sup2;, and the drawn shape is the arrangement of '
    +'least total energy. Two bonds make a line, three a flat triangle at 120&deg;, four a tetrahedron at 109.5&deg;, five a trigonal '
    +'bipyramid with 90&deg; and 120&deg; angles, six an octahedron at 90&deg;, and those are exact. A double or a triple bond counts as one '
    +'direction, as PhET counts it. Drag an atom round the centre and let go to watch it slide back.'),
  real:(HAS_LP
    ?'PhET&rsquo;s second screen: thirteen real molecules, their atoms placed where measured bond angles put them. Where A has no lone pair the '
    +'measured shape is the ideal one to the last digit PhET stores. Where it has lone pairs the angles close up: H<sub>2</sub>O is 104.5&deg; '
    +'where a tetrahedron gives 109.5&deg;, NH<sub>3</sub> 107.8&deg;, ClF<sub>3</sub>&rsquo;s arms 87.5&deg; from its stem. The model chip swaps '
    +'the measured shape for this model&rsquo;s least-energy one, fitted onto it so the two can be compared, and the readout lists all three '
    +'sets of angles: measured, model, ideal. SF<sub>4</sub> is the case to look at: its two equatorial fluorines close to 101.6&deg;, and the '
    +'model, like every point-pair model tried in the build, opens them instead. The outer atoms&rsquo; lone pairs can be drawn; as in PhET they '
    +'push on nothing.'
    :'PhET&rsquo;s second screen in its Basics form: five real molecules with no lone pair on the central atom, and therefore the five ideal '
    +'shapes. BeCl<sub>2</sub> is linear, BF<sub>3</sub> trigonal planar, CH<sub>4</sub> tetrahedral, PCl<sub>5</sub> a trigonal bipyramid and '
    +'SF<sub>6</sub> an octahedron, with the measured angles of PhET&rsquo;s table. The readout adds the measured bond lengths, which the drawing '
    +'leaves out: PhET draws every bond of a molecule at one length, and PCl<sub>5</sub>&rsquo;s axial bonds are really longer (2.14 &Aring;) '
    +'than its equatorial ones (2.02 &Aring;).'),
  table:(HAS_LP
    ?'The AXE table: A the central atom, X its bonded atoms, E its lone pairs. Down the side is the steric number x + e, which fixes the '
    +'electron geometry; along the top, bonds are swapped one at a time for lone pairs. The atoms alone then make the molecule geometry, which '
    +'is where the names come from: a tetrahedron missing one vertex is a trigonal pyramid, missing two it is bent. Two choices hide in the '
    +'table. A lone pair in a trigonal bipyramid goes equatorial, giving the seesaw and the T-shape, and two lone pairs in an octahedron go '
    +'opposite each other, giving the square plane. PhET builds those choices in. Here they come out of the energy: derive.py finds that for '
    +'every class and every &rho; on the slider they are the arrangements of least energy.'
    :'The five shapes of the Basics sim side by side. They are what two to six equal pairs do on a sphere when they push each other apart: '
    +'two go to opposite poles, three to a triangle, four to a tetrahedron, five to a trigonal bipyramid, six to an octahedron. Only the '
    +'bipyramid has two kinds of position, three round its equator at 120&deg; and two at its poles at 90&deg; to them. It still is the '
    +'least-energy arrangement of five, which the relaxation view shows from any random start.'),
  squeeze:'How much does a lone pair squeeze a bond angle? In this model that is set by &rho;, the lone pairs&rsquo; radius. At &rho; = 1 a lone '
    +'pair is just another bond and every angle is ideal; pull the lone pairs in and each class bends away from them, linearly at first. The '
    +'top panel follows seven angles from &rho; = 1 to PhET&rsquo;s 0.70, and the measured molecules sit on their curves where the model '
    +'reproduces them. Three need a &rho; between 0.79 and 0.96; three need more squeeze than the model gives at 0.70; and one, SF<sub>4</sub>&rsquo;s '
    +'equatorial angle, bends the wrong way entirely. The bottom panel puts all seven side by side at the current &rho;. A single number cannot '
    +'fit them all, which is the honest result: point pairs capture the direction of every lone-pair effect but one, not its size.',
  relax:(HAS_LP
    ?'The same energy as the model view, minimised the plainest way: start the pairs anywhere and walk every one downhill along its sphere. '
    +'With no lone pairs the walk always ends in the ideal shape, from any start. With lone pairs it can end somewhere else: a local minimum, '
    +'an arrangement where every pair is balanced but a lower one exists, and derive.py counts how often: 65 of 100 random '
    +'starts of AX<sub>4</sub>E<sub>2</sub> stall with its lone pairs cis, 24 of 100 of AX<sub>3</sub>E<sub>3</sub>. Try a few starts of either. The readout lists every arrangement of the lone pairs over the slots with its energy, and the plot marks them as orange '
    +'lines; the green curve drops to rounding error only when the walk finds the VSEPR one. PhET&rsquo;s notes say its animation must avoid '
    +'exactly these traps; the model view does it by starting from the VSEPR slots.'
    :'The same energy as the model view, minimised the plainest way: scatter the bonds anywhere on the sphere and walk each one downhill '
    +'until nothing pushes it sideways. From every random start the walk ends in the ideal shape &mdash; derive.py tried a hundred starts each for '
    +'five and for six pairs and lost none &mdash; and the energy above the minimum falls geometrically to rounding error. That is the precise sense in '
    +'which the five shapes are what equal repulsion makes: for two to six pairs each is the only minimum there is.'),
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  model:'<h4>the energy</h4>'
    +EQ(1,'U = &Sigma;<sub>i&lt;j</sub> |<b>x</b><sub>i</sub> &minus; <b>x</b><sub>j</sub>|<sup>&minus;2</sup>, &nbsp; <b>x</b><sub>i</sub> = R<sub>i</sub> <b>u</b><sub>i</sub>'+(HAS_LP?', &nbsp; R = 1 or &rho;':''))
    +EQ(2,'&part;U/&part;<b>u</b><sub>i</sub> = &minus;2R<sub>i</sub> &Sigma;<sub>j</sub> (<b>x</b><sub>i</sub> &minus; <b>x</b><sub>j</sub>) / |<b>x</b><sub>i</sub> &minus; <b>x</b><sub>j</sub>|<sup>4</sup>, &nbsp; &nabla;<sub>t</sub> = (1 &minus; <b>u</b><b>u</b><sup>T</sup>) &part;U/&part;<b>u</b>')
    +EQ(3,'<span class="rm">equal pairs:</span> U<sub>min</sub> = '+FR('1','4')+', 1, '+FR('9','4')+', '+FR('17','4')+', '+FR('27','4')+' <span class="rm">for 2 to 6</span>')
    +'<p>The equilibrium is relaxed from the ideal slots with the lone pairs in the high-repulsion ones (PhET&rsquo;s order), by the descent of the '
    +'relaxation view; it agrees with scipy&rsquo;s BFGS to 1e&minus;10&deg;. '+(HAS_LP?'For &rho; &ge; 0.64 that arrangement is the global minimum of every class '
    +'and a true local minimum (derive.py: every slot assignment, 16 random starts, the Hessian); PhET&rsquo;s 0.70 has room to spare. With Coulomb&rsquo;s '
    +'1/d at 0.70, ClF<sub>3</sub> would be trigonal planar.':'')+'</p>'
    +'<div class="cite">pins: every class at &rho; = 0.70, 0.85, 1 (angles, energies), the closed forms, the gradient against a finite difference &mdash; derive.py</div>',
  real:'<h4>the measured geometry</h4>'
    +EQ(1,'&theta;<sub>ij</sub> = arccos(<b>u</b><sub>i</sub> &middot; <b>u</b><sub>j</sub>), &nbsp; <b>u</b> <span class="rm">built from PhET&rsquo;s stored angles</span>')
    +EQ(2,'NH<sub>3</sub>: cos &theta; = sin&sup2;&beta; cos 120&deg; + cos&sup2;&beta;, &nbsp; &beta; = 1.202623030417028 &rArr; &theta; = 107.8&deg;')
    +(HAS_LP?EQ(3,'<span class="rm">lone pairs:</span> R = argmin &Sigma; |R <b>s</b><sub>&sigma;(k)</sub> &minus; <b>b</b><sub>k</sub>|&sup2;, &nbsp; <b>e</b><sub>k</sub> = R <b>s</b><sub>k</sub> <span class="rm">(Horn&rsquo;s quaternion fit)</span>'):'')
    +'<p>PhET stores each molecule as the numbers its constructor is given: SF<sub>4</sub>&rsquo;s 173.1&deg; and 101.6&deg;, BrF<sub>5</sub>&rsquo;s 84.8&deg;, '
    +'CH<sub>4</sub>&rsquo;s elevation &minus;19.471220333&deg; (so its angles are 109.47122033&deg; and 109.47122094&deg;, not quite ideal). Those are kept verbatim '
    +'and every angle is computed from them.</p>'
    +'<div class="cite">pins: the distinct angles of all fourteen molecules, the NH<sub>3</sub> angle, the lone-pair fits &mdash; derive.py</div>',
  table:'<h4>the naming rule</h4>'
    +EQ(1,'<span class="rm">electron geometry</span> = f(x + e), &nbsp; <span class="rm">molecule geometry</span> = g(x, e)')
    +EQ(2,'x = 2: &nbsp; e = 0, 3, 4 &rArr; linear; &nbsp; e = 1, 2 &rArr; bent')
    +EQ(3,'x = 3: &nbsp; trigonal planar, trigonal pyramidal, T-shaped, T-shaped <span class="rm">for e = 0 to 3</span>')
    +EQ(4,'x = 4: &nbsp; tetrahedral, seesaw, square planar; &nbsp; x = 5: trigonal bipyramidal, square pyramidal')
    +'<p>These are PhET&rsquo;s rules, all 22 cases pinned. '+(HAS_LP?'derive.py confirms each shape the rules name is where the energy puts the pairs.':'')+'</p>'
    +'<div class="cite">pins: the 22 names; the fifteen relaxed classes &mdash; derive.py</div>',
  squeeze:'<h4>the squeeze</h4>'
    +EQ(1,'&Delta;&theta;(&rho;) = &theta;(&rho;) &minus; &theta;<sub>ideal</sub>, &nbsp; &Delta;&theta;(1) = 0, &nbsp; &Delta;&theta; &asymp; c (1 &minus; &rho;) <span class="rm">near 1</span>')
    +'<p>The approach to &rho; = 1 is linear: halving 1 &minus; &rho; halves every &Delta;&theta; (derive.py: ratios 1.96 to 2.00 between &rho; = 0.98 and 0.99). '
    +'The fitted &rho; of a molecule is where its curve crosses the measured value, found by bisection on the relaxation itself: 0.954 for SO<sub>2</sub>, '
    +'0.833 for NH<sub>3</sub>, 0.792 for SF<sub>4</sub>&rsquo;s axial pair.</p>'
    +'<div class="cite">pins: the seven curves at &rho; = 0.70 and 0.85, the three fitted &rho; (brentq in derive.py), the directions &mdash; derive.py</div>',
  relax:'<h4>the descent</h4>'
    +EQ(1,'<b>u</b><sub>i</sub> &larr; '+FR('<b>u</b><sub>i</sub> &minus; &eta;&nabla;<sub>t,i</sub>U','|<b>u</b><sub>i</sub> &minus; &eta;&nabla;<sub>t,i</sub>U|')+', &nbsp; &eta; = 0.1')
    +EQ(2,'<span class="rm">stable when</span> &eta; &lambda;<sub>max</sub> &lt; 2: &nbsp; &lambda;<sub>max</sub> = 8.24 <span class="rm">over every class</span>')
    +'<p>Random starts use mulberry32, the house generator, so the Python twin replays the same starts; derive.py lands every equal-pair start on the ideal shape '
    +'to 1e&minus;11&deg;.</p>'
    +'<div class="cite">pins: fifteen seeded starts, N = 2 to 6, and their step counts &mdash; derive.py</div>',
};
