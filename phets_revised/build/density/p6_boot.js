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
      MEMO.pool=MEMO.sets=MEMO.mystery=MEMO.mv=MEMO.line=null;
      syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,input:inp}; sync(); return rowEl;
  }
  function checkbox(key,lb,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lb);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg();
      syncPanel(); dirty=true; refresh(); });
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
        syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); }
  const clearMemo=()=>{ MEMO.pool=MEMO.sets=MEMO.mystery=MEMO.mv=MEMO.line=null; };

  /* ---- group 1: the block (PhET's Intro controls) ---- */
  const gBlock=h('div',{class:'grp'},h('h3',null,'the block'));
  const matChipsA=chipRow(MAT_LIST,'matA',()=>{ setMat(st,'A',st.matA); clearMemo(); }); gBlock.appendChild(matChipsA);
  gBlock.appendChild(slider('massA','mass, kg',MMIN,MMAX,0.1,v=>fmt(v,2)+' kg',
    v=>{ setMass(st,'A',v); clearMemo(); }));
  gBlock.appendChild(slider('volAL','volume, L',VMIN_L,VMAX_L,0.5,v=>fmt(v,2)+' L',
    v=>{ setVol(st,'A',v); clearMemo(); }));
  gBlock.appendChild(h('div',{class:'checks'},checkbox('two','two blocks',clearMemo)));
  const matChipsB=chipRow(MAT_LIST,'matB',()=>{ setMat(st,'B',st.matB); clearMemo(); }); gBlock.appendChild(matChipsB);
  gBlock.appendChild(slider('massB','B mass, kg',MMIN,MMAX,0.1,v=>fmt(v,2)+' kg',
    v=>{ setMass(st,'B',v); clearMemo(); }));
  gBlock.appendChild(slider('volBL','B volume, L',VMIN_L,VMAX_L,0.5,v=>fmt(v,2)+' L',
    v=>{ setVol(st,'B',v); clearMemo(); }));
  const blockTag=h('div',{class:'tag'}); gBlock.appendChild(blockTag);

  /* ---- group 2: the set (PhET's Compare controls) ---- */
  const gSet=h('div',{class:'grp'},h('h3',null,'the set'));
  gSet.appendChild(chipRow(SET_LIST,'setMode',clearMemo));
  gSet.appendChild(slider('sameMass','same mass, kg',DENS_MASS_RANGE[0],DENS_MASS_RANGE[1],0.1,v=>fmt(v,2)+' kg',
    v=>{ st.sameMass=v; clearMemo(); }));
  gSet.appendChild(slider('sameVolL','same volume, L',DENS_VOL_RANGE[0]*LITERS,DENS_VOL_RANGE[1]*LITERS,0.5,v=>fmt(v,2)+' L',
    v=>{ st.sameVolL=v; clearMemo(); }));
  gSet.appendChild(slider('sameRho','same density',DENS_RHO_RANGE[0],DENS_RHO_RANGE[1],10,v=>fmt(v,0)+' kg/m³',
    v=>{ st.sameRho=v; clearMemo(); }));
  const setTag=h('div',{class:'tag'}); gSet.appendChild(setTag);

  /* ---- group 3: the mystery ---- */
  const gMys=h('div',{class:'grp'},h('h3',null,'the mystery'));
  gMys.appendChild(chipRow(MSET_LIST,'mset',clearMemo));
  gMys.appendChild(chipRow(PICK_LIST,'mpick',clearMemo));
  gMys.appendChild(h('div',{class:'checks'},
    checkbox('submerge','hold them under',clearMemo),
    checkbox('reveal','reveal the answers',clearMemo)));
  const shuffleBtn=h('div',{class:'btnrow'},btn('a new shuffle',()=>{ st.mset='shuffled'; st.seed=(st.seed*1103515245+12345)>>>0||1; clearMemo(); syncChips(); }));
  gMys.appendChild(shuffleBtn);
  const mysTag=h('div',{class:'tag'}); gMys.appendChild(mysTag);

  /* ---- group 4: the plane ---- */
  const gPlane=h('div',{class:'grp'},h('h3',null,'the plane'));
  gPlane.appendChild(chipRow(MVMAT_LIST,'mvMat',clearMemo));
  gPlane.appendChild(h('div',{class:'checks'},checkbox('showRef','draw the handbook value too',clearMemo)));
  const planeTag=h('div',{class:'tag'}); gPlane.appendChild(planeTag);

  /* ---- group 5: the fluid ---- */
  const gFluid=h('div',{class:'grp'},h('h3',null,'the fluid'));
  gFluid.appendChild(chipRow(FLUID_LIST,'lineFluid',clearMemo));
  const fluidTag=h('div',{class:'tag'}); gFluid.appendChild(fluidTag);

  /* ---- group 6: the drawing ---- */
  const gDraw=h('div',{class:'grp'},h('h3',null,'the drawing'));
  gDraw.appendChild(h('div',{class:'checks'},checkbox('forces','force arrows'),checkbox('levels','label the arrows')));
  gDraw.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; clearMemo(); syncChips(); })));
  const drawTag=h('div',{class:'tag'}); gDraw.appendChild(drawTag);

  /* ---- group 7: what you are looking at ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Density (University of Colorado Boulder, phet.colorado.edu, '
      +'CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values &mdash; the pool 0.9 &times; 0.4 &times; 0.4167 m holding 100 L, '
      +'g = 9.8 m/s&sup2;, cubes of 1&ndash;10 L and 0.1&ndash;27 kg, and every material density &mdash; are read from its build 1.2.10 and '
      +'its doc/model.md. Handbook densities: Wikipedia, &ldquo;Densities of various materials&rdquo;, fetched 2026-09-21; six materials have no '
      +'row there and the file says so. Everything else is exact and pinned in selfTest to build/density/derive.py (scipy.brentq, a 2000-point '
      +'perimeter sum, a 4000-strip face integral).'}));
  /* ---- group 8: the physics ---- */
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gBlock,gSet,gMys,gPlane,gFluid,gDraw,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row this view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view;
    gBlock.hidden=!(v==='pool'||v==='mv'||v==='line');
    matChipsB.hidden=!(v==='pool'&&st.two);
    rows.massB.row.hidden=!(v==='pool'&&st.two);
    rows.volBL.row.hidden=!(v==='pool'&&st.two);
    rows.cb_two.row.hidden=(v!=='pool');
    gSet.hidden=(v!=='sets');
    rows.sameMass.row.hidden=(st.setMode!=='mass');
    rows.sameVolL.row.hidden=(st.setMode!=='volume');
    rows.sameRho.row.hidden=(st.setMode!=='density');
    gMys.hidden=(v!=='mystery');
    gPlane.hidden=(v!=='mv');
    gFluid.hidden=(v!=='line');
    gDraw.hidden=!(v==='pool');
    for(const k in rows) rows[k].sync();
    const rhoA=rhoOf(st,'A');
    blockTag.innerHTML=(st.matA==='custom'
      ? 'custom: mass and volume are free and the density follows, &rho; = m/V = <b>'+sigf(rhoA,4)+'</b> kg/m&sup3;'
      : 'PhET&rsquo;s coupling: the material fixes &rho; = <b>'+sigf(MAT[st.matA].phet,4)+'</b> kg/m&sup3;, so mass and volume move together. '
        +'Its mass slider reaches '+fmt(massRangeFor(MAT[st.matA].phet,false)[0],2)+'&ndash;'+fmt(massRangeFor(MAT[st.matA].phet,false)[1],2)+' kg')
      +(MAT[st.matA]&&MAT[st.matA].note?' &nbsp; <span class="r">'+MAT[st.matA].note+'</span>':'');
    setTag.innerHTML=st.setMode==='mass'?'PhET&rsquo;s four volumes are 10, 5, 2.5 and 1.25 L'
      :st.setMode==='volume'?'PhET&rsquo;s four masses are 8, 6, 4 and 2 kg'
      :'PhET&rsquo;s four volumes are 6, 4, 2 and 1 L';
    mysTag.innerHTML=(st.mset==='shuffled'?'seed '+st.seed+' &mdash; five of the thirteen table materials at whole-litre volumes, as PhET&rsquo;s refresh button draws them'
      :'PhET&rsquo;s fixed '+st.mset)
      +(st.submerge?'':' &nbsp; <span class="r">the floaters are measuring as water</span>');
    planeTag.innerHTML='green: PhET&rsquo;s value &nbsp; orange: the handbook&rsquo;s &nbsp; magenta: the material picked here';
    fluidTag.innerHTML='PhET&rsquo;s six Buoyancy fluids. The Density sim itself is water only; the companion '
      +'buoyancy-basics.html puts all six in the pool.';
    drawTag.innerHTML='drag a block in the pool view to hold it under or lift it clear &nbsp; 1&ndash;5 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M,st);
      eqEl.innerHTML=eqbarHTML(M,st);
      tagEl.innerHTML=tagHTML(M,st);
      hintEl.textContent=(st.view==='pool'?'drag a block to hold it under · ':'')+'1–5 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.pool=null; dirty=true; roEl.innerHTML=readoutHTML(S.model(),st); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ MEMO.pool=null; dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key==='r'){ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; clearMemo(); syncChips(); syncPanel(); dirty=true; refresh(); }
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
  pool:'This is PhET&rsquo;s Intro screen. A cube of a chosen material goes into a pool holding 100 litres of water, and two '
    +'numbers about it are yours to set: how much of it there is, and how heavy it is. They are not independent. Pick a real '
    +'material and its density is fixed, so mass and volume move together &mdash; doubling the volume doubles the mass, because '
    +'m = &rho;V. Pick <i>custom</i> and they come apart, and the density is whatever the two of them make. Whether the block '
    +'floats has nothing to do with how heavy it is: a 20 kg block of wood floats and a 1 kg block of aluminium does not. It is '
    +'the density, and only the density, compared with the water&rsquo;s. Watch the level: a floating block raises it by its own '
    +'mass divided by &rho;<sub>f</sub>A, a sunk one by its own volume divided by A, and those two statements are exact.',
  sets:'PhET&rsquo;s Compare screen holds one of the three quantities fixed across four blocks and lets the other two do what '
    +'&rho; = m/V makes them. Matched in <b>mass</b>, the blocks are all equally heavy and the small ones are the dense ones; at '
    +'5 kg PhET&rsquo;s four volumes give 500, 1000, 2000 and 4000 kg/m&sup3;, and the second is exactly water &mdash; it neither '
    +'floats nor presses on the floor, which is worth seeing once. Matched in <b>volume</b> they are all the same size and the '
    +'heavy ones are the dense ones. Matched in <b>density</b> they are the same stuff in four sizes, and every one of them floats '
    +'to exactly the same fraction of its own height, because size cancels out of the floating law completely.',
  mystery:'PhET&rsquo;s Mystery screen asks you to name five materials from measurements alone. The scale gives the mass. The '
    +'water gives the volume &mdash; but only if the block is <b>fully under</b>. A floating block pushes aside its own weight of '
    +'water, not its own volume, so the litres it displaces are m/&rho;<sub>f</sub> and dividing the mass by them returns '
    +'&rho;<sub>f</sub> for every floater alike: wood, ice and styrofoam would all measure as water. Hold them under and the '
    +'displaced volume is the block&rsquo;s volume, the division gives its density, and the table names it. That the table really '
    +'does name it is a claim this file checks rather than assumes: it prints how far each reading lands from its own material and '
    +'from the next nearest one.',
  mv:'Density is a ratio, and a ratio is a straight line through the origin. Put volume across and mass up and every material is '
    +'one ray, steeper the denser it is; a block is a point, and the point&rsquo;s ray tells you what it is made of. The cyan box '
    +'is what PhET&rsquo;s controls reach &mdash; 1 to 10 litres, 0.1 to 27 kilograms &mdash; and it explains the material list: at '
    +'10 litres gold would weigh 193 kg, so the Intro screen stops at aluminium. The second thing this view is for is provenance. '
    +'Green is the density PhET&rsquo;s code actually runs on; orange, where it exists, is the handbook value. Most agree to a few '
    +'parts in a thousand. Four do not, and they are teaching choices rather than measurements: PhET&rsquo;s styrofoam is twice as '
    +'dense as real expanded polystyrene, its concrete a third too dense, its PVC a fifth, and its glass is simply aluminium&rsquo;s '
    +'number reused.',
  line:'Everything about floating is in one line. A floating body must displace its own weight, &rho;<sub>b</sub>gV = '
    +'&rho;<sub>f</sub>gV<sub>sub</sub>, so V<sub>sub</sub>/V = &rho;<sub>b</sub>/&rho;<sub>f</sub> &mdash; and for a cube the draft '
    +'is the same fraction of the side. Size has cancelled; so has gravity, which is why this works identically on the Moon. The '
    +'line stops at 1 because a body cannot be more than completely submerged: past that the upthrust is stuck at '
    +'&rho;<sub>f</sub>gV, it is less than the weight, and the floor takes the difference, N = (&rho;<sub>b</sub> &minus; '
    +'&rho;<sub>f</sub>)gV. Exactly at the kink the two are equal and nothing chooses a depth at all. Swap water for mercury and '
    +'the picture moves under your feet: lead floats, and so does everything PhET carries except platinum and tantalum.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  pool:'<h4>the free surface</h4>'
    +EQ(1,'G(y) = A<sub>pool</sub>(y + H) &minus; &Sigma;<sub>i</sub> V<sub>i</sub>(y) &nbsp;=&nbsp; V<sub>fluid</sub>')
    +EQ(2,'y<sub>w</sub> = inf { y : G(y) &ge; V<sub>fluid</sub> } &nbsp; <span class="rm">(G is non-decreasing)</span>')
    +EQ(3,'&Delta;y = '+FR('m','&rho;<sub>f</sub> A')+' <span class="rm">(floating)</span> &nbsp;&nbsp; &Delta;y = '+FR('V','A')+' <span class="rm">(submerged)</span>')
    +'<p>The <i>infimum</i> in [2] is the physics rather than a convention: a body that spans the pool&rsquo;s cross-section makes '
    +'G flat, and the fluid then stands at the bottom of the flat stretch with the surplus above the body, not inside it. '
    +'A = '+fmt(A_POOL,2)+' m&sup2; and H = '+fmt(POOL_H,4)+' m are PhET&rsquo;s own bounds.</p>'
    +'<div class="cite">pins: the bare level, both single-block levels and the two-block level; the level law both ways; '
    +'G non-decreasing over 4001 levels &mdash; derive.py</div>',
  sets:'<h4>&rho; = m/V, three ways</h4>'
    +EQ(1,'<span class="rm">same m:</span> V<sub>i</sub> <span class="rm">given</span> &rArr; &rho;<sub>i</sub> = m/V<sub>i</sub>')
    +EQ(2,'<span class="rm">same V:</span> m<sub>i</sub> <span class="rm">given</span> &rArr; &rho;<sub>i</sub> = m<sub>i</sub>/V')
    +EQ(3,'<span class="rm">same &rho;:</span> V<sub>i</sub> <span class="rm">given</span> &rArr; m<sub>i</sub> = &rho;V<sub>i</sub>, <span class="rm">and every draft is</span> &rho;/&rho;<sub>f</sub>')
    +'<p>PhET&rsquo;s numbers: volumes 10, 5, 2.5, 1.25 L at a common mass; masses 8, 6, 4, 2 kg at a common volume; volumes '
    +'6, 4, 2, 1 L at a common density. At the default 5 kg the second block is exactly water.</p>'
    +'<div class="cite">pins: all twelve densities and masses, and which of each set floats &mdash; derive.py</div>',
  mystery:'<h4>measuring a density</h4>'
    +EQ(1,'&rho; = '+FR('m','V')+', &nbsp; m <span class="rm">from the scale,</span> V <span class="rm">from the water</span>')
    +EQ(2,'<span class="rm">held under:</span> V<sub>disp</sub> = V &nbsp;&rArr;&nbsp; &rho; <span class="rm">is the block&rsquo;s</span>')
    +EQ(3,'<span class="rm">left floating:</span> V<sub>disp</sub> = '+FR('m','&rho;<sub>f</sub>')+' &nbsp;&rArr;&nbsp; '+FR('m','V<sub>disp</sub>')+' = &rho;<sub>f</sub> <span class="rm">always</span>')
    +'<p>[3] is the trap, and it is exact: the reading is the fluid&rsquo;s own density for every floating block, whatever it is '
    +'made of. The identification is checked at the printed precision (two decimals in kg and in litres), not at full precision.</p>'
    +'<div class="cite">pins: all fifteen fixed-set blocks identified, worst reading error 0.19 %, smallest gap to the runner-up '
    +'3.3 %; and all 130 material &times; whole-litre combinations of the shuffled set &mdash; derive.py</div>',
  mv:'<h4>the ray, and the box</h4>'
    +EQ(1,'m = &rho;V &nbsp; <span class="rm">a ray of slope &rho; through the origin</span>')
    +EQ(2,'<span class="rm">PhET:</span> 1 L &le; V &le; 10 L, &nbsp; 0.1 kg &le; m &le; 27 kg')
    +EQ(3,'<span class="rm">so the mass slider runs</span> [&rho;V<sub>min</sub>, &rho;V<sub>max</sub>] &cap; [0.1, 27] kg')
    +'<p>Aluminium at 10 L is 27 kg exactly, which is where PhET&rsquo;s maximum comes from and why its Intro list stops there. '
    +'The handbook column is Wikipedia&rsquo;s table; six materials have no row in it and are marked, not guessed.</p>'
    +'<div class="cite">pins: every mass range; the PhET-against-handbook differences; the six materials with no row &mdash; derive.py</div>',
  line:'<h4>the floating law</h4>'
    +EQ(1,'&rho;<sub>b</sub> g V = &rho;<sub>f</sub> g V<sub>sub</sub> &nbsp;&rArr;&nbsp; '+FR('V<sub>sub</sub>','V')+' = '+FR('&rho;<sub>b</sub>','&rho;<sub>f</sub>'))
    +EQ(2,'<span class="rm">a cube:</span> d = s '+FR('&rho;<sub>b</sub>','&rho;<sub>f</sub>')+', &nbsp; s = V<sup>1/3</sup>')
    +EQ(3,'&rho;<sub>b</sub> &ge; &rho;<sub>f</sub>: &nbsp; F<sub>b</sub> = &rho;<sub>f</sub>gV, &nbsp; N = (&rho;<sub>b</sub> &minus; &rho;<sub>f</sub>) g V &ge; 0')
    +EQ(4,'<span class="rm">the upthrust, the long way:</span> (p<sub>bot</sub> &minus; p<sub>top</sub>) s&sup2; = &rho;<sub>f</sub> g s&sup2; (y<sub>t</sub> &minus; y<sub>b</sub>) = &rho;<sub>f</sub> g V')
    +'<p>[4] is where the upthrust comes from: the pressure on the bottom face exceeds the pressure on the top by '
    +'&rho;<sub>f</sub>g times the height of the block, and the four side faces cancel in pairs. This file computes it both ways '
    +'and asserts they agree.</p>'
    +'<div class="cite">pins: the draft against scipy.brentq (1.4e-17); the face integral against &rho;<sub>f</sub>gV<sub>sub</sub>; '
    +'the per-edge polygon integral against a 2000-point perimeter sum; the neutral case at three depths &mdash; derive.py</div>',
};
