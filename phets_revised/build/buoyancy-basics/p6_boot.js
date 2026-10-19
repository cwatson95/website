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
    syncChips(); syncPanel(); dirty=true; refresh();
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
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        clearAll(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); clearAll(); syncPanel(); dirty=true; refresh(); }},label); }

  /* ---- group 1: the block ---- */
  const gBlock=h('div',{class:'grp'},h('h3',null,'the block'));
  const matChipsA=chipRow(MAT_LIST,'matA',()=>{ setMat(st,'A',st.matA); }); gBlock.appendChild(matChipsA);
  gBlock.appendChild(slider('massA','mass, kg',MMIN,MMAX,0.1,v=>fmt(v,2)+' kg',v=>setMass(st,'A',v)));
  gBlock.appendChild(slider('volAL','volume, L',VMIN_L,VMAX_L,0.5,v=>fmt(v,2)+' L',v=>setVol(st,'A',v)));
  gBlock.appendChild(h('div',{class:'checks'},checkbox('two','two blocks')));
  const matChipsB=chipRow(MAT_LIST,'matB',()=>{ setMat(st,'B',st.matB); }); gBlock.appendChild(matChipsB);
  gBlock.appendChild(slider('massB','B mass, kg',MMIN,MMAX,0.1,v=>fmt(v,2)+' kg',v=>setMass(st,'B',v)));
  gBlock.appendChild(slider('volBL','B volume, L',VMIN_L,VMAX_L,0.5,v=>fmt(v,2)+' L',v=>setVol(st,'B',v)));
  const blockTag=h('div',{class:'tag'}); gBlock.appendChild(blockTag);

  /* ---- group 2: the fluid ---- */
  const gFluid=h('div',{class:'grp'},h('h3',null,'the fluid'));
  gFluid.appendChild(chipRow(FLUID_LIST,'fluid'));
  const fluidTag=h('div',{class:'tag'}); gFluid.appendChild(fluidTag);

  /* ---- group 3: the scales ---- */
  const gScales=h('div',{class:'grp'},h('h3',null,'the scales'));
  gScales.appendChild(chipRow(WHERE_LIST,'where'));
  gScales.appendChild(slider('scaleH','pool scale height',0,1,0.01,v=>fmt(v,2)));
  const scalesTag=h('div',{class:'tag'}); gScales.appendChild(scalesTag);

  /* ---- group 4: the set ---- */
  const gSet=h('div',{class:'grp'},h('h3',null,'the set'));
  gSet.appendChild(chipRow(SET_LIST,'setMode'));
  gSet.appendChild(slider('sameMass','same mass, kg',1,10,0.1,v=>fmt(v,2)+' kg'));
  gSet.appendChild(slider('sameVolL','same volume, L',1,10,0.5,v=>fmt(v,2)+' L'));
  gSet.appendChild(slider('sameRho','same density',BB_RHO_RANGE[0],BB_RHO_RANGE[1],10,v=>fmt(v,0)+' kg/m³'));
  const setTag=h('div',{class:'tag'}); gSet.appendChild(setTag);

  /* ---- group 5: the depth ---- */
  const gDepth=h('div',{class:'grp'},h('h3',null,'the depth'));
  gDepth.appendChild(slider('facesDepth','the bottom face, m',0.05,0.9,0.01,v=>fmt(100*v,0)+' cm down'));
  gDepth.appendChild(slider('lowered','lowered',0,1,0.005,v=>fmt(v,3)));
  const depthTag=h('div',{class:'tag'}); gDepth.appendChild(depthTag);

  /* ---- group 6: the grid ---- */
  const gGrid=h('div',{class:'grp'},h('h3',null,'the grid'));
  gGrid.appendChild(chipRow(GRID_LIST,'gridMat'));
  const gridTag=h('div',{class:'tag'}); gGrid.appendChild(gridTag);

  /* ---- group 7: the drawing ---- */
  const gDraw=h('div',{class:'grp'},h('h3',null,'the drawing'));
  gDraw.appendChild(h('div',{class:'checks'},checkbox('forces','force arrows'),checkbox('labels','label the arrows')));
  gDraw.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; syncChips(); })));
  const drawTag=h('div',{class:'tag'}); gDraw.appendChild(drawTag);

  /* ---- group 8: what you are looking at ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Buoyancy: Basics (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values &mdash; the pool 0.9 &times; 0.4 &times; '
      +'0.4167 m holding 100 L, the scales 0.15 &times; 0.06 &times; 0.2 m (1.8 L), g = 9.8 m/s&sup2;, cubes of 1&ndash;10 L and '
      +'0.1&ndash;27 kg, the six fluids and every material density &mdash; are read from its build 1.2.11 and the shared '
      +'doc/model.md. Handbook densities: Wikipedia, &ldquo;Densities of various materials&rdquo;, fetched 2026-09-21; six '
      +'materials have no row there and the file says so. The engine is the same file as density.html&rsquo;s, and every number is '
      +'pinned in selfTest to build/density/derive.py (scipy.brentq, a 4000-strip face integral, a 2000-point perimeter sum).'}));
  /* ---- group 9: the physics ---- */
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gBlock,gFluid,gScales,gSet,gDepth,gGrid,gDraw,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row this view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view;
    gBlock.hidden=!(v==='explore'||v==='faces'||v==='scale');
    matChipsB.hidden=!(v==='explore'&&st.two);
    rows.massB.row.hidden=!(v==='explore'&&st.two);
    rows.volBL.row.hidden=!(v==='explore'&&st.two);
    rows.cb_two.row.hidden=(v!=='explore');
    gFluid.hidden=(v==='fluids');
    gScales.hidden=!(v==='explore'||v==='sets');
    gSet.hidden=(v!=='sets');
    rows.sameMass.row.hidden=(st.setMode!=='mass');
    rows.sameVolL.row.hidden=(st.setMode!=='volume');
    rows.sameRho.row.hidden=(st.setMode!=='density');
    gDepth.hidden=!(v==='faces'||v==='scale');
    rows.facesDepth.row.hidden=(v!=='faces');
    rows.lowered.row.hidden=(v!=='scale');
    gGrid.hidden=(v!=='fluids');
    gDraw.hidden=!(v==='explore'||v==='sets');
    for(const k in rows) if(rows[k].sync) rows[k].sync();
    const rhoA=rhoOf(st,'A');
    blockTag.innerHTML=(st.matA==='custom'
      ? 'custom: mass and volume are free and the density follows, &rho; = m/V = <b>'+sigf(rhoA,4)+'</b> kg/m&sup3;'
      : 'PhET&rsquo;s coupling: the material fixes &rho; = <b>'+sigf(MAT[st.matA].phet,4)+'</b> kg/m&sup3;, so mass and volume move '
        +'together. Its mass slider reaches '+fmt(massRangeFor(MAT[st.matA].phet,false)[0],2)+'&ndash;'
        +fmt(massRangeFor(MAT[st.matA].phet,false)[1],2)+' kg')
      +(MAT[st.matA]&&MAT[st.matA].note?' &nbsp; <span class="r">'+MAT[st.matA].note+'</span>':'');
    fluidTag.innerHTML='PhET&rsquo;s six Buoyancy fluids, '+sigf(MAT.gasoline.phet,3)+' to '+sigf(MAT.mercury.phet,5)
      +' kg/m&sup3;. The block floats when its density is below the fluid&rsquo;s, and sinks to exactly &rho;<sub>b</sub>/&rho;<sub>f</sub> of itself.';
    scalesTag.innerHTML='both scales read newtons, as PhET&rsquo;s do. The pool scale displaces '+fmt(SCALE_V*LITERS,1)
      +' L of fluid itself, which is in the level.';
    setTag.innerHTML=st.setMode==='mass'?'PhET&rsquo;s two volumes are 2 L (brick) and 10 L (wood)'
      :st.setMode==='volume'?'PhET&rsquo;s two masses are 10 kg (brick) and 2 kg (wood)'
      :'PhET&rsquo;s two volumes are 5 L and 10 L, both at the wood&rsquo;s 400 kg/m&sup3;';
    depthTag.innerHTML=(st.view==='faces'
      ? 'the block is held at this depth with a flat free surface above it; below '
        +fmt(100*cubeSide(st.volAL/LITERS),1)+' cm its top is out of the fluid'
      : 'lowered 0 is clear of the surface, 1 is resting on the pool floor');
    gridTag.innerHTML='27 materials &times; 6 fluids. The highlighted row is the one the readout prints.';
    drawTag.innerHTML='drag a block in the pool view to hold it under or lift it clear &nbsp; 1&ndash;5 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M,st);
      eqEl.innerHTML=eqbarHTML(M,st);
      tagEl.innerHTML=tagHTML(M,st);
      hintEl.textContent=(st.view==='explore'?'drag a block to hold it under · ':'')+'1–5 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.explore=null; dirty=true; roEl.innerHTML=readoutHTML(S.model(),st); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ MEMO.explore=null; dirty=true; refresh(); } };
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

  function frameLoop(tm){
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  explore:'This is PhET&rsquo;s Explore screen. A cube of a chosen material goes into a pool of a chosen fluid, and the '
    +'three forces on it are drawn: gravity pulling down, buoyancy pushing up, and the contact force from whatever it is '
    +'resting on. At rest those three add to nothing, which is what the arrows show. Change the fluid and the picture moves '
    +'under your feet: the same aluminium block that sits flat on the floor of a water pool floats in mercury, a fifth of it '
    +'under. Put the block on the pool scale and read what it presses with; put it on the ground scale and read what it '
    +'weighs in air. The difference between the two readings is the weight of the fluid the block pushed aside &mdash; which '
    +'is the whole of Archimedes&rsquo; principle, in two numbers you can compare on screen.',
  sets:'PhET&rsquo;s Compare screen is one question asked three ways. Take a brick and a piece of wood and give them the same '
    +'MASS: the wood has to be five times the size, and it floats while the brick does not, so weight alone decides nothing. '
    +'Give them the same VOLUME: now the brick weighs five times as much, and it is still the brick that sinks. Give them the '
    +'same DENSITY and they become the same stuff in two sizes &mdash; and they float to exactly the same fraction of '
    +'themselves, because size cancels out of &rho;<sub>b</sub>/&rho;<sub>f</sub> completely. Only the third comparison '
    +'changes what happens, which is the point of the screen.',
  faces:'Buoyancy is not an extra force that fluids have. It is what is left when you add up the pressure on every face. '
    +'Hydrostatic pressure is &rho;<sub>f</sub>g times the depth, and it pushes inward everywhere, perpendicular to the '
    +'surface. On the four vertical faces the pressure at any given depth is the same on the left as on the right, so those '
    +'cancel in pairs exactly &mdash; they squeeze the block but do not lift it. The bottom face and the top face do not '
    +'cancel, because the bottom is deeper by the height of the block: the difference in pressure is &rho;<sub>f</sub>g '
    +'times that height, and multiplied by the face area it is &rho;<sub>f</sub>gV. This view computes the force both ways, '
    +'face by face and round the polygon edge by edge, and prints how far apart the two answers are.',
  scale:'Hang a block on a spring scale and lower it into a fluid. Nothing happens while it is in the air. The moment the '
    +'bottom face touches the surface the reading starts to fall, and it falls in a straight line, because the submerged '
    +'volume grows in proportion to how far in the block has gone. Then the top face goes under, and the reading stops '
    +'changing altogether. That is the part worth watching: the pressure on the bottom face keeps growing with depth, but so '
    +'does the pressure on the top, by exactly the same amount, and what the scale reads is the difference. A block that '
    +'floats reaches zero before it is fully under and the string goes slack; a block that sinks reaches '
    +'(&rho;<sub>b</sub> &minus; &rho;<sub>f</sub>)gV and stays there until it lands.',
  fluids:'Whether something floats is not a fact about the thing; it is a comparison between two densities. This grid puts '
    +'every material PhET carries against every fluid it carries, ordered by density, and the pattern is a staircase: for '
    +'each fluid there is a line above which everything sinks and below which everything floats, and that line is at the '
    +'fluid&rsquo;s own density. In mercury, at 13593 kg/m&sup3;, everything on the list floats except tantalum and platinum '
    +'&mdash; lead floats, gold very nearly does. In gasoline, at 680, almost nothing does. Where a cell is green the number '
    +'in it is the fraction of the block that ends up under, and that fraction is exactly &rho;<sub>b</sub>/&rho;<sub>f</sub>: '
    +'the same law, read off a table.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  explore:'<h4>the three forces</h4>'
    +EQ(1,'W = &rho;<sub>b</sub> g V, &nbsp; F<sub>b</sub> = &rho;<sub>f</sub> g V<sub>sub</sub>, &nbsp; N &ge; 0')
    +EQ(2,'<span class="rm">at rest:</span> N = W &minus; F<sub>b</sub> &nbsp; <span class="rm">(resting)</span>, &nbsp; N = 0 <span class="rm">(floating or held)</span>')
    +EQ(3,'<span class="rm">the free surface:</span> A<sub>pool</sub>(y + H) &minus; &Sigma;V<sub>i</sub>(y) &minus; V<sub>scale</sub>(y) = V<sub>fluid</sub>')
    +EQ(4,'&Delta;y = '+FR('m','&rho;<sub>f</sub> A')+' <span class="rm">(floating)</span>, &nbsp; &Delta;y = '+FR('V','A')+' <span class="rm">(submerged)</span>')
    +'<p>N &ge; 0 is a property of the solve, not a clamp: a block only rests when the upthrust cannot lift it. selfTest '
    +'sweeps 84 configurations to check it, and a clamp that was there to enforce it has been deleted as dead code.</p>'
    +'<div class="cite">pins: the level with and without the pool scale; the scale&rsquo;s own 1.8 L; 118.44 N on the pool scale '
    +'against 132.30 N in air for PhET&rsquo;s aluminium block; the per-cent submerged of wood and aluminium in all six fluids &mdash; derive.py</div>',
  sets:'<h4>&rho; = m/V, three ways</h4>'
    +EQ(1,'<span class="rm">same m:</span> &rho;<sub>i</sub> = m/V<sub>i</sub> &nbsp;&rarr;&nbsp; 2 L &rarr; 2000, 10 L &rarr; 400')
    +EQ(2,'<span class="rm">same V:</span> &rho;<sub>i</sub> = m<sub>i</sub>/V &nbsp;&rarr;&nbsp; 10 kg &rarr; 2000, 2 kg &rarr; 400')
    +EQ(3,'<span class="rm">same &rho;:</span> '+FR('V<sub>sub</sub>','V')+' = '+FR('&rho;','&rho;<sub>f</sub>')+' <span class="rm">for both, whatever the size</span>')
    +'<p>PhET&rsquo;s numbers are the brick&rsquo;s 2000 and the wood&rsquo;s 400 kg/m&sup3;, reached from 4 kg at 2 and 10 L, or '
    +'from 5 L at 10 and 2 kg.</p>'
    +'<div class="cite">pins: both blocks in each of the three modes, and which of them floats &mdash; derive.py</div>',
  faces:'<h4>the pressure integral</h4>'
    +EQ(1,'p(y) = &rho;<sub>f</sub> g (y<sub>w</sub> &minus; y) &nbsp; <span class="rm">gauge, linear in y</span>')
    +EQ(2,'<span class="rm">sides:</span> &nbsp; F<sub>+x</sub> + F<sub>&minus;x</sub> = 0 <span class="rm">exactly, at every depth</span>')
    +EQ(3,'<span class="rm">net up:</span> (p<sub>bot</sub> &minus; p<sub>top</sub>) A = &rho;<sub>f</sub> g (y<sub>t</sub> &minus; y<sub>b</sub>) A = &rho;<sub>f</sub> g V')
    +EQ(4,'<span class="rm">per edge (2-D):</span> F = &minus;p(mid) n L <span class="rm">is exact, because p is linear along a straight edge</span>')
    +'<p>The 2-D route clips the cross-section at the waterline and integrates round it; its vertical sum is &rho;g&times;the '
    +'submerged area per unit depth, and the resultant passes through the centroid of that area.</p>'
    +'<div class="cite">pins: 49.000 N from the faces against 49 N from &rho;gV (3e-16 relative); one side face 59.0782 N and the '
    +'pair summing to exactly 0; 114.6215 N/m per edge against a 2000-point perimeter sum &mdash; derive.py</div>',
  scale:'<h4>the apparent weight</h4>'
    +EQ(1,'<span class="rm">reading</span> = W &minus; &rho;<sub>f</sub> g V<sub>sub</sub>(d)')
    +EQ(2,'<span class="rm">entering:</span> V<sub>sub</sub> = s&sup2; d &nbsp;&rArr;&nbsp; <span class="rm">the reading falls linearly</span>')
    +EQ(3,'<span class="rm">under:</span> V<sub>sub</sub> = V &nbsp;&rArr;&nbsp; <span class="rm">reading</span> = (&rho;<sub>b</sub> &minus; &rho;<sub>f</sub>) g V, <span class="rm">constant</span>')
    +EQ(4,'&rho;<sub>b</sub> &lt; &rho;<sub>f</sub> &rArr; <span class="rm">the reading reaches 0 at</span> d = s &rho;<sub>b</sub>/&rho;<sub>f</sub>')
    +'<p>The entering leg is not quite a straight line in the lowering coordinate, because the fluid rises as the block goes '
    +'in: the surface comes up to meet it. The curve here is solved at every one of its 241 points rather than drawn from '
    +'[2].</p>'
    +'<div class="cite">pins: the reading at seven depths for a 5 L brick, 98 N in air falling to 49 N under &mdash; derive.py</div>',
  fluids:'<h4>the staircase</h4>'
    +EQ(1,FR('V<sub>sub</sub>','V')+' = min(1, '+FR('&rho;<sub>b</sub>','&rho;<sub>f</sub>')+') &nbsp; <span class="rm">floats iff</span> &rho;<sub>b</sub> &lt; &rho;<sub>f</sub>')
    +EQ(2,'<span class="rm">mercury 13593: everything but tantalum (16650) and platinum (21450)</span>')
    +EQ(3,'<span class="rm">gasoline 680: styrofoam (150) and wood (400) only</span>')
    +'<p>The fraction has no size and no gravity in it, which is why this is a table of two numbers rather than a simulation.</p>'
    +'<div class="cite">pins: the per-cent submerged of wood and aluminium in all six fluids, and the float counts in the '
    +'extreme columns &mdash; derive.py</div>',
};
