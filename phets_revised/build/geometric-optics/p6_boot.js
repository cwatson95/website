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
      clearMemo(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,input:inp}; sync(); return rowEl;
  }
  function checkbox(key,lb){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lb);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; clearMemo();
      syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was); clearMemo();
        [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
        syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){ return h('button',{onclick:()=>{ fn(); clearMemo(); syncPanel(); dirty=true; refresh(); }},label); }

  /* ---- group 1: the lens (PhET's Lens-screen optic controls) ---- */
  const gLens=h('div',{class:'grp'},h('h3',null,'the lens'));
  gLens.appendChild(chipRow(LENS_LIST,'lensSurface'));
  const fctlRow=chipRow(FCTL_LIST,'fControl',(o,was)=>{
    /* PhET keeps the two models in step: switching copies the other one's
       value across, constrained to this one's range */
    if(o.id==='direct') st.lensF=clamp(phetFocalFromR(st.lensR,st.lensN),PHET.fLens[0],PHET.fLens[1]);
    else st.lensR=clamp(phetRFromFocal(st.lensF,st.lensN),PHET.rocLens[0],PHET.rocLens[1]);
  });
  gLens.appendChild(fctlRow);
  gLens.appendChild(slider('lensF','focal length',PHET.fLens[0],PHET.fLens[1],PHET.fStep,v=>fmt(v,0)+' cm'));
  gLens.appendChild(slider('lensR','radius R',PHET.rocLens[0],PHET.rocLens[1],PHET.rocStep,v=>fmt(v,0)+' cm'));
  gLens.appendChild(slider('lensN','index n',PHET.iorLens[0],PHET.iorLens[1],PHET.iorStep,v=>fmt(v,2)));
  gLens.appendChild(slider('lensD','diameter D',PHET.dLens[0],PHET.dLens[1],PHET.dStep,v=>fmt(v,0)+' cm'));
  const lensTag=h('div',{class:'tag'}); gLens.appendChild(lensTag);

  /* ---- group 2: the mirror (PhET's Mirror screen) ---- */
  const gMir=h('div',{class:'grp'},h('h3',null,'the mirror'));
  gMir.appendChild(chipRow(MIRROR_LIST,'mirrorSurface'));
  gMir.appendChild(slider('mirrorF','focal length',PHET.fMirror[0],PHET.fMirror[1],PHET.fStep,v=>fmt(v,0)+' cm'));
  gMir.appendChild(slider('mirrorR','radius R',PHET.rocMirror[0],PHET.rocMirror[1],PHET.rocStep,v=>fmt(v,0)+' cm'));
  gMir.appendChild(slider('mirrorD','diameter D',PHET.dMirror[0],PHET.dMirror[1],PHET.dStep,v=>fmt(v,0)+' cm'));
  const mirTag=h('div',{class:'tag'}); gMir.appendChild(mirTag);

  /* ---- group 3: the object ---- */
  const gObj=h('div',{class:'grp'},h('h3',null,'the object'));
  gObj.appendChild(chipRow(OBJ_LIST,'objKind'));
  gObj.appendChild(slider('objX','position x',-460,-PHET.minObjectDist,1,v=>fmt(v,0)+' cm'));
  gObj.appendChild(slider('objY','height y',-PHET.maxOffAxis,PHET.maxOffAxis,0.5,v=>fmt(v,1)+' cm'));
  gObj.appendChild(slider('secondOff','second point',PHET.secondOffset,0,0.5,v=>fmt(v,1)+' cm'));
  const objTag=h('div',{class:'tag'}); gObj.appendChild(objTag);

  /* ---- group 4: the rays ---- */
  const gRays=h('div',{class:'grp'},h('h3',null,'the rays'));
  gRays.appendChild(chipRow(RAY_LIST,'rays'));
  const rayTag=h('div',{class:'tag'}); gRays.appendChild(rayTag);

  /* ---- group 5: the drawing ---- */
  const gDraw=h('div',{class:'grp'},h('h3',null,'the drawing'));
  gDraw.appendChild(h('div',{class:'checks'},
    checkbox('showF','Focal Points (F)'),checkbox('show2F','2F Points'),
    checkbox('showVirtual','Virtual Image'),checkbox('showLabels','Labels'),
    checkbox('showSecond','Second Point'),checkbox('showGuides','Guides'),
    checkbox('showRuler','ruler')));
  gDraw.appendChild(slider('screenX','screen at x',PHET.minScreenDist,420,5,v=>fmt(v,0)+' cm'));
  gDraw.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{
    const v=st.view; Object.assign(st,DEFAULTS); st.view=v; syncChips(); })));
  const drawTag=h('div',{class:'tag'}); gDraw.appendChild(drawTag);

  /* ---- group 6: the real lens ---- */
  const gReal=h('div',{class:'grp'},h('h3',null,'the real lens'));
  gReal.appendChild(slider('realEdge','edge thickness',0.5,12,0.5,v=>fmt(v,1)+' cm'));
  gReal.appendChild(slider('realStop','stopped to',0.2,1,0.02,v=>fmt(100*v,0)+' % of D'));
  gReal.appendChild(slider('realH','marked ray at',0.05,1,0.01,v=>fmt(100*v,0)+' % of the stop'));
  const realTag=h('div',{class:'tag'}); gReal.appendChild(realTag);

  /* ---- group 7: what you are looking at ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Geometric Optics (University of '
      +'Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. '
      +'PhET&rsquo;s values &mdash; the 40&ndash;120 cm focal length and radius ranges, the 1.2&ndash;1.8 '
      +'index, the 60&ndash;120 cm diameter, the mirror&rsquo;s 75&ndash;150 and 150&ndash;300 cm ranges, '
      +'the fixed n = 1.5 and n = 2, the flat mirror&rsquo;s 100 000 cm, the object positions, the '
      +'&minus;56.5 cm second point, the screen at 200 cm, the 120&deg; fan and its ray count, the '
      +'guides&rsquo; own arithmetic and the softened lens sag &mdash; are read out of its build 1.3.16 '
      +'(docs/phets/geometric-optics_en.html) and its doc/model.md. Everything else is exact and pinned '
      +'in selfTest to build/geometric-optics/derive.py (scipy.brentq on the lens equation, '
      +'scipy.minimize_scalar on the spot size, a closed-form sphere intersection checked against '
      +'Newton on the sag).'}));
  /* ---- group 8: the physics ---- */
  const gPhys=h('div',{class:'grp'},h('h3',null,'the physics'),h('div',{id:'phys'}));
  [gLens,gMir,gObj,gRays,gDraw,gReal,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row this view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view;
    const lensish=(v==='bench'||v==='conj'||v==='maker'||v==='guides'||v==='real');
    gLens.hidden=!lensish;
    rows.lensF.row.hidden=(st.fControl!=='direct');
    rows.lensR.row.hidden=(st.fControl!=='indirect');
    rows.lensN.row.hidden=(st.fControl!=='indirect');
    rows.lensD.row.hidden=(v==='conj');
    fctlRow.hidden=false;
    gMir.hidden=(v!=='mirror');
    rows.mirrorF.row.hidden=(st.fControl!=='direct'||st.mirrorSurface==='flat');
    rows.mirrorR.row.hidden=(st.fControl!=='indirect'||st.mirrorSurface==='flat');
    gObj.hidden=!(v==='bench'||v==='mirror'||v==='conj'||v==='guides');
    rows.objY.row.hidden=(v==='conj');
    rows.secondOff.row.hidden=!((v==='bench'||v==='mirror')&&st.showSecond);
    gRays.hidden=!(v==='bench'||v==='mirror');
    gDraw.hidden=!(v==='bench'||v==='mirror');
    rows.screenX.row.hidden=!(v==='bench'&&st.objKind==='light');
    rows.cb_showGuides.row.hidden=(v!=='bench');
    gReal.hidden=(v!=='real');
    for(const k in rows) rows[k].sync();

    const n=lensIndex(st), R=Math.abs(lensRadius(st)), f=Math.abs(lensFocal(st));
    lensTag.innerHTML=(st.fControl==='direct'
      ? 'PhET&rsquo;s <b>direct</b> model: you set |f| and it holds n = 1.50, so R = 2f(n&minus;1) = <b>'
        +sigf(R,4)+'</b> cm follows'
      : 'PhET&rsquo;s <b>indirect</b> model: you set |R| and n, and |f| = |R|/2(n&minus;1) = <b>'
        +sigf(f,4)+'</b> cm follows')
      +' &nbsp; signed f = '+sigf(lensFocal(st),4)+' cm ('+(lensFocal(st)>0?'converging':'diverging')+')';
    mirTag.innerHTML=st.mirrorSurface==='flat'
      ? 'PhET&rsquo;s flat mirror is a converging optic of f = 100 000 cm, not a true plane &mdash; the '
        +'readout prints how far that is from m = 1'
      : 'PhET gives a mirror n = 2, so |f| = |R|/2(2&minus;1) = |R|/2 = <b>'
        +sigf(Math.abs(mirrorFocal(st)),4)+'</b> cm &mdash; the paraxial mirror formula, out of the '
        +'lens maker&rsquo;s equation';
    objTag.innerHTML='drag the object on the canvas. PhET keeps it at least '+PHET.minObjectDist
      +' cm from the optic and within '+PHET.maxOffAxis+' cm of the axis; its own defaults are '
      +'(&minus;170, 27) on the Lens screen and (&minus;150, 72.5) on the Mirror screen.'
      +(st.objKind==='light'?' The second source sits '+LIGHT_DX+' cm downstream, which is PhET&rsquo;s own offset.':'');
    rayTag.innerHTML=st.rays==='many'
      ? 'PhET&rsquo;s fan: 20&middot;(&lfloor;d_o/300&rfloor;+1) = <b>'+manyRayCount(Math.abs(objectPoint(st)[0]))
        +'</b> rays over 120&deg;'
      : st.rays==='principal'
      ? 'the three construction rays. They are not physical &mdash; PhET lets them through the optic '
        +'plane whatever their height, and so does this'
      : st.rays==='marginal'
      ? 'to the centre and to the two rim points: the rays the aperture actually admits'
      : 'no rays drawn; the image is still solved';
    drawTag.innerHTML='1&ndash;6 switch views &nbsp; r resets';
    realTag.innerHTML='edge thickness is chosen here, not PhET&rsquo;s &mdash; PhET never gives its lens '
      +'a thickness at all. Everything else is the lens the other views describe.';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M,st);
      eqEl.innerHTML=eqbarHTML(M,st);
      tagEl.innerHTML=tagHTML(M,st);
      hintEl.textContent=((st.view==='bench'||st.view==='mirror'||st.view==='guides')
        ?'drag the object · ':'')+'1–6 switch views';
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
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key==='r'){ const v=st.view; Object.assign(st,DEFAULTS); st.view=v;
      clearMemo(); syncChips(); syncPanel(); dirty=true; refresh(); }
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
  bench:'PhET&rsquo;s <b>Lens</b> screen. An object stands on the optical axis in front of a convex or '
   +'concave lens; drag it, or drive it with the sliders, and watch the image answer. What is worth '
   +'watching is not that the picture looks right but that it <b>has to be</b> right: every ray is bent '
   +'by one line, u&prime; = u &minus; h/f, and nothing in the drawing knows where the image is. Where the '
   +'rays meet is therefore a consequence, and the readout prints the residual of the equation it agrees '
   +'with. Cross the focal point with the object and the outgoing rays go parallel &mdash; there is no '
   +'image at all &mdash; and then reconverge on the near side as the dashed backward extensions of '
   +'diverging light, which is the whole content of the phrase &ldquo;virtual image&rdquo;.',
  mirror:'PhET&rsquo;s <b>Mirror</b> screen, and the same equation. The only thing that changes is which '
   +'way the light leaves: a real image forms to the <b>left</b> of a mirror, where the light actually '
   +'goes, so d_i &gt; 0 now points the other way. PhET builds its mirror out of the same code as its '
   +'lens by giving it an index of exactly 2, which turns f = R/2(n&minus;1) into the paraxial mirror '
   +'formula f = R/2; the concave mirror converges and the convex one diverges. Its flat mirror is not a '
   +'plane but a converging optic of focal length 100 000 cm, and the readout says what that costs.',
  conj:'The governing law, drawn. Everything on the two benches is one rectangular hyperbola: '
   +'d_i = f d_o/(d_o &minus; f), whose asymptotes are the lines d_o = f and d_i = f. Slide the object '
   +'and watch the live point run up the branch toward the pole &mdash; the image distance grows without '
   +'bound as the object reaches the focal point, and the instant it passes inside, the point reappears '
   +'on the negative branch, which is the virtual image. Newton wrote the same thing more symmetrically: '
   +'measure both distances <b>from the focal points</b> and their product is f&sup2;, with no special '
   +'cases and no pole. A diverging optic has no pole in range at all, which is why its image is always '
   +'virtual, always upright and always smaller.',
  maker:'Where the focal length comes from. PhET gives its optic the same radius on both faces, so the '
   +'lens maker&rsquo;s equation 1/f = (n&minus;1)(1/R&#8321; &minus; 1/R&#8322;) collapses to '
   +'f = R/2(n&minus;1), whose contours in the (n, R) plane are straight lines aimed at n = 1. The sim '
   +'offers you the same lens through two different doors &mdash; set f and let R follow at a fixed '
   +'n = 1.5, or set R and n and let f follow &mdash; and PhET keeps them in step, which is why switching '
   +'the control here copies one value into the other. The lower panel is a quieter point: the shape the '
   +'artwork draws uses a softened sag that belongs to no sphere, and at a large aperture it draws a lens '
   +'that could not be ground.',
  guides:'PhET invented this. Two arms hinge at the rim of the lens; each takes the ray that reaches it '
   +'and turns it through a fixed angle 2 arctan(D/4f), and where the two transmitted arms cross is '
   +'offered as the image without any ray tracing at all. It is a good construction and it is not exact, '
   +'and the difference is worth having: a thin optic changes a ray&rsquo;s <b>slope</b> by &minus;h/f, '
   +'while a guide rotates it by an <b>angle</b>. Those coincide only for small angles, so shrinking the '
   +'lens alone leaves the miss stuck near four and a half per cent; shrink the lens and the '
   +'object&rsquo;s inclination together and the miss falls as the square, which the lower panel measures '
   +'rather than asserts.',
  real:'The counterweight. Every other view here treats the optic as ideal, because that is the model '
   +'PhET is teaching and it is the right one to teach. This view takes the same numbers &mdash; the same '
   +'index, the same radius, the same diameter &mdash; builds two real spherical surfaces out of them and '
   +'refracts each ray with vector Snell instead. The focus then depends on where the ray struck the '
   +'lens, walking in as the square of the ray height: that h&sup2; is the leading term the paraxial '
   +'expansion throws away, and at PhET&rsquo;s default diameter this is an f/1 lens, so it is not small. '
   +'Stop the aperture down and the ideal model comes back; open it and no single plane is in focus at '
   +'all.'
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const CONV='<h4>sign convention</h4><p>x runs right, the optic is at x = 0, the object is always at '
  +'x &lt; 0. <i>d</i><sub>o</sub> = &minus;x<sub>obj</sub> &gt; 0. <i>f</i> &gt; 0 converging (convex '
  +'lens, concave mirror), &lt; 0 diverging. <i>d</i><sub>i</sub> &gt; 0 is a real image &mdash; to the '
  +'right of a lens, to the left of a mirror; &lt; 0 is virtual. <i>m</i> &lt; 0 is inverted. '
  +'<i>R</i> &gt; 0 convex, &lt; 0 concave, which is PhET&rsquo;s own convention.</p>';
const DERIV={
  bench:CONV
   +'<h4>the thin-optic equation</h4>'
   +EQ(1,FR('1','d<sub>o</sub>')+' + '+FR('1','d<sub>i</sub>')+' = '+FR('1','f'))
   +EQ(2,'d<sub>i</sub> = '+FR('f d<sub>o</sub>','d<sub>o</sub> &minus; f')+' , &nbsp; m = &minus;'
        +FR('d<sub>i</sub>','d<sub>o</sub>'))
   +'<h4>and the ray transfer that has to agree with it</h4>'
   +'<p>A ray leaving the object at height <i>y</i><sub>o</sub> and crossing the optic plane at height '
   +'<i>h</i> arrives with slope <i>u</i> = (<i>h</i> &minus; <i>y</i><sub>o</sub>)/<i>d</i><sub>o</sub>. '
   +'The optic changes the slope, by an amount proportional to the height and to nothing else:</p>'
   +EQ(3,'u&prime; = u &minus; '+FR('h','f'))
   +'<p>Put [3] into the outgoing ray at path length <i>d</i><sub>i</sub> and the height is</p>'
   +EQ(4,'h + (u &minus; h/f) d<sub>i</sub> = h d<sub>i</sub>&#8203;('+FR('1','d<sub>i</sub>')+' + '
        +FR('1','d<sub>o</sub>')+' &minus; '+FR('1','f')+') &minus; y<sub>o</sub>'+FR('d<sub>i</sub>','d<sub>o</sub>'))
   +'<p>The bracket is [1], so it is zero, and the height is <i>m y</i><sub>o</sub> &mdash; for '
   +'<b>every</b> <i>h</i>. That is why the rays meet: not because they were aimed at the image, but '
   +'because [1] holds. <span class="ok">selfTest asserts this over 1200 configurations, worst residual '
   +'1.8&times;10<sup>&minus;13</sup>, and separately that the three principal rays meet pairwise at the '
   +'image (1.0&times;10<sup>&minus;15</sup> over 360).</span></p>'
   +'<p class="cite">PhET&rsquo;s ray modes: marginal = to the centre and the two rim points; principal '
   +'= parallel, through the centre, through the near F; many = a 120&deg; fan of '
   +'20(&lfloor;d<sub>o</sub>/300&rfloor;+1) rays.</p>',
  mirror:CONV
   +'<h4>the same equation, the other sign</h4>'
   +EQ(1,FR('1','d<sub>o</sub>')+' + '+FR('1','d<sub>i</sub>')+' = '+FR('1','f')+' , &nbsp; f = '+FR('R','2'))
   +'<p>PhET reaches <i>f</i> = <i>R</i>/2 by handing the lens maker&rsquo;s equation an index of exactly '
   +'2: <i>R</i>/2(<i>n</i>&minus;1) with <i>n</i> = 2 is <i>R</i>/2. The paraxial mirror formula and the '
   +'lens maker&rsquo;s equation then live in one line of code.</p>'
   +'<h4>the flat mirror is a stand-in</h4>'
   +'<p>PhET does not model a plane. It uses <i>f</i> = 100 000 cm, so an object at '
   +'<i>d</i><sub>o</sub> = 150 cm images at &minus;150.2253 cm rather than exactly &minus;150, and '
   +'<i>m</i> = 1.0015 rather than 1. <span class="warn">Both numbers are printed in the readout rather '
   +'than rounded away.</span></p>'
   +'<p class="cite">F and 2F: a lens has them on both sides; a concave mirror has both to the left, a '
   +'convex mirror both to the right, a flat mirror neither (PhET, doc/model.md).</p>',
  conj:CONV
   +'<h4>two ways to write one statement</h4>'
   +EQ(1,FR('1','d<sub>o</sub>')+' + '+FR('1','d<sub>i</sub>')+' = '+FR('1','f'))
   +EQ(2,'(d<sub>o</sub> &minus; f)(d<sub>i</sub> &minus; f) = f<sup>2</sup>')
   +'<p>Expand [2]: <i>d</i><sub>o</sub><i>d</i><sub>i</sub> &minus; <i>f</i>(<i>d</i><sub>o</sub> + '
   +'<i>d</i><sub>i</sub>) + <i>f</i><sup>2</sup> = <i>f</i><sup>2</sup>, i.e. '
   +'<i>d</i><sub>o</sub><i>d</i><sub>i</sub> = <i>f</i>(<i>d</i><sub>o</sub> + <i>d</i><sub>i</sub>), '
   +'which divided by <i>f d</i><sub>o</sub><i>d</i><sub>i</sub> is [1]. So [2] is not an extra fact; it '
   +'is [1] with the origin moved to the focal points, and it is why the curve is a rectangular '
   +'hyperbola. <span class="ok">selfTest pins the product against f&sup2; to 4.5&times;10<sup>&minus;16</sup> '
   +'over 35 (f, d<sub>o</sub>) pairs.</span></p>'
   +'<h4>the pole</h4>'
   +'<p>At <i>d</i><sub>o</sub> = <i>f</i> the equation has no solution: the outgoing rays are parallel '
   +'and the image is at infinity. This file returns Infinity there and says so, rather than PhET&rsquo;s '
   +'10<sup>7</sup> cm. Either side of it <i>d</i><sub>i</sub> is &plusmn;6.4&times;10<sup>9</sup> cm at '
   +'one micron of object displacement &mdash; a pole, not a large number.</p>',
  maker:CONV
   +'<h4>the lens maker&rsquo;s equation</h4>'
   +EQ(1,FR('1','f')+' = (n &minus; 1)&#8203;('+FR('1','R<sub>1</sub>')+' &minus; '+FR('1','R<sub>2</sub>')+')')
   +'<p>PhET sets <i>R</i><sub>1</sub> = +<i>R</i> and <i>R</i><sub>2</sub> = &minus;<i>R</i>, so the '
   +'bracket is 2/<i>R</i> and</p>'
   +EQ(2,'f = '+FR('R','2(n &minus; 1)')+' , &nbsp; R = 2f(n &minus; 1)')
   +'<p>Its <i>doc/model.md</i> prints this as <i>f</i> = <i>R</i>/2(1&minus;<i>n</i>); the code computes '
   +'the magnitude as |<i>R</i>|/2(<i>n</i>&minus;1) and puts the sign on from the surface type, which is '
   +'what is implemented here. <span class="ok">Asserted against [1] to 1.4&times;10<sup>&minus;16</sup> '
   +'over twenty (n, R) pairs.</span></p>'
   +'<h4>the shape on screen</h4>'
   +EQ(3,'sag = |R| &minus; &radic;(R<sup>2</sup> &minus; (D/2)<sup>2</sup>) &nbsp;&nbsp; vs &nbsp;&nbsp; '
        +'a<sub>PhET</sub> = '+FR('(D/2)<sup>2</sup>','2(|R| + 100)'))
   +'<p class="warn">At R = 80, D = 80 those are 10.72 cm and 4.44 cm. At R = 40, D = 120 the true sag '
   +'does not exist at all and PhET&rsquo;s still returns 12.86 cm. The artwork is a picture of a lens, '
   +'not of <i>this</i> lens &mdash; which matters not at all to the model, and entirely to anyone who '
   +'reads the picture as a specification.</p>',
  guides:CONV
   +'<h4>PhET&rsquo;s construction, exactly</h4>'
   +'<p>Fulcrum at (0, <i>sD</i>/2) with <i>s</i> = +1 top, &minus;1 bottom. With '
   +'<i>r</i> = <i>D</i>/4<i>f</i> (signed <i>f</i>):</p>'
   +EQ(1,'&theta;<sub>out</sub> = &theta;<sub>in</sub> + &pi; &minus; s&middot;2 arctan r &nbsp;&nbsp; (convex)')
   +EQ(2,'&theta;<sub>out</sub> = &theta;<sub>in</sub> + &pi; &minus; s(arctan 3r &minus; arctan r) &nbsp;&nbsp; (concave)')
   +'<p>The two branches agree to third order and differ by exactly '
   +'3 arctan <i>r</i> &minus; arctan 3<i>r</i> = 8<i>r</i><sup>3</sup> + O(<i>r</i><sup>5</sup>), which '
   +'<span class="ok">selfTest checks by measured ratio at four values of r</span>.</p>'
   +'<h4>why it is only nearly right</h4>'
   +'<p>A thin optic sends <i>u</i> to <i>u</i> &minus; <i>h/f</i>. A guide sends <i>&theta;</i> to '
   +'<i>&theta;</i> &minus; 2 arctan <i>r</i>. Since tan(<i>&theta;</i>+<i>&delta;</i>) = tan <i>&theta;</i> '
   +'+ <i>&delta;</i>(1 + tan<sup>2</sup><i>&theta;</i>) + &hellip;, the two agree only when the rays are '
   +'near-axial in <b>angle</b>, not merely when <i>D</i>/<i>f</i> is small. At PhET&rsquo;s defaults the '
   +'crossing lands 6.71 cm short of a 151.11 cm image &mdash; 4.4 % &mdash; and shrinking D alone takes '
   +'it to 4.548 % rather than to zero.</p>',
  real:CONV
   +'<h4>what the paraxial model dropped</h4>'
   +'<p>Snell&rsquo;s law is <i>n</i><sub>1</sub> sin <i>&theta;</i><sub>1</sub> = <i>n</i><sub>2</sub> '
   +'sin <i>&theta;</i><sub>2</sub>. The paraxial model is its first term. Keeping the next one gives, for '
   +'a lens of fixed shape, a focal shift quadratic in the ray height:</p>'
   +EQ(1,'LSA(h) = &minus;C h<sup>2</sup> + O(h<sup>4</sup>)')
   +'<p>which is measured here, not assumed: halving <i>h</i> divides the traced LSA by 4.0001, 4.0006, '
   +'4.0023 and 4.0091 at 0.25, 0.5, 1 and 2 cm. <span class="ok">Both the ratio and the coefficient are '
   +'pinned in selfTest against derive.py.</span></p>'
   +'<h4>the thick lens, since it now has a thickness</h4>'
   +EQ(2,FR('1','f')+' = (n&minus;1)&#8203;['+FR('1','R<sub>1</sub>')+' &minus; '+FR('1','R<sub>2</sub>')
        +' + '+FR('(n&minus;1)t','n R<sub>1</sub>R<sub>2</sub>')+']')
   +EQ(3,'BFD = f&#8203;(1 &minus; '+FR('(n&minus;1)t','n R<sub>1</sub>')+')')
   +'<p>At PhET&rsquo;s defaults the thin form gives 80 cm, the thick form 84.11 cm and the back focal '
   +'distance 75.89 cm, and the rim ray crosses 43.5 cm inside the paraxial focus &mdash; 51.7 % of the '
   +'focal length. <span class="warn">None of that is a criticism of PhET: it is what &ldquo;ideal '
   +'lens&rdquo; buys you, made visible.</span></p>'
   +'<p class="cite">The intersection is the closed-form sphere root; a Newton-on-the-sag route is '
   +'implemented beside it and the suite asserts the two agree to 1.4&times;10<sup>&minus;14</sup> cm.</p>'
};
