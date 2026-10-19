
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
    if(st.view!==k){ st.view=k; simReset(); }
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  /* a slider bound either to st[key] or to a get/set pair (the actions that
     enforce PhET's rules); after every input the whole panel re-syncs, so a
     slider pushed past a constraint springs back to where the rule held it */
  function slider(key,lab2,lo,hi,step2,fmtf,opt){
    const o=opt||{}, get=o.get||(()=>st[key]), set=o.set||(v=>{ st[key]=v; });
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.textContent=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ if(onchg) onchg(inp.checked); else st[key]=inp.checked; syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        st[key]=o.id; syncChips(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }

  const gSph=h('div',{class:'grp'},h('h3',null,'the spheres'));
  gSph.appendChild(slider('m1','mass m₁, kg',M_MIN,M_MAX,M_STEP,v=>fmt(v,0),{set:v=>setMass(st,1,v)}));
  gSph.appendChild(slider('m2','mass m₂, kg',M_MIN,M_MAX,M_STEP,v=>fmt(v,0),{set:v=>setMass(st,2,v)}));
  gSph.appendChild(slider('x1','centre x₁, m',TRACK.iL/TRACK.perM,TRACK.iR/TRACK.perM,0.1,v=>fmt(v,1),
    {get:()=>st.i1/TRACK.perM,set:v=>setPos(st,1,v)}));
  gSph.appendChild(slider('x2','centre x₂, m',TRACK.iL/TRACK.perM,TRACK.iR/TRACK.perM,0.1,v=>fmt(v,1),
    {get:()=>st.i2/TRACK.perM,set:v=>setPos(st,2,v)}));
  gSph.appendChild(h('div',{class:'checks'},checkbox('cs','constant size (0.5 m)',v=>setConstSize(st,v))));
  const sphTag=h('div',{class:'tag'}); gSph.appendChild(sphTag);

  const gDisp=h('div',{class:'grp'},h('h3',null,'force values'));
  gDisp.appendChild(chipRow([{id:'dec',name:'decimal notation'},{id:'sci',name:'scientific notation'},{id:'hid',name:'hidden'}],'fmode'));
  gDisp.appendChild(slider('arrowK','arrow scale',0,ARROW_KMAX,1,k=>sciPlain(arrowStep(k,ARROW_E0),1)+' N/m'));
  gDisp.appendChild(h('div',{class:'checks'},checkbox('showDist','the distance between centres')));
  gDisp.appendChild(h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ rulerToM1(st); dirty=true; refresh(); }},'ruler to m₁'),
    h('button',{onclick:()=>{ rulerHome(st); dirty=true; refresh(); }},'ruler home')));
  const dispTag=h('div',{class:'tag'}); gDisp.appendChild(dispTag);

  const gRun=h('div',{class:'grp'},h('h3',null,'the release'));
  gRun.appendChild(h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ startRun(st); dirty=true; refresh(); }},'release'),
    h('button',{onclick:()=>{ simReset(); dirty=true; refresh(); }},'stop & reset')));
  gRun.appendChild(h('div',{class:'checks'},checkbox('running','time runs')));
  const runTag=h('div',{class:'tag'}); gRun.appendChild(runTag);

  const gReset=h('div',{class:'grp'},h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; simReset();
      syncChips(); syncPanel(); dirty=true; refresh(); }},'reset all')));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Gravity Force Lab (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'G: CODATA 2022 through scipy.constants. PhET&rsquo;s values: density 150 kg/m&sup3;, constant radius 0.5 m, '
      +'masses 10&ndash;1000 kg, the &plusmn;5 m track on a 0.1-m grid, a 0.1-m gap between surfaces (read from PhET&rsquo;s build 2.2.25). '
      +'Every number is pinned in selfTest to build/gravity-force-lab/derive.py (scipy solve_ivp and brentq for the fall).'}));
  [gSph,gDisp,gRun,gReset,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS) [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  function syncPanel(){
    const v=st.view;
    gDisp.hidden=(v!=='lab');
    gRun.hidden=(v!=='fall');
    for(const k in rows) rows[k].sync();
    const L=labModel(st);
    sphTag.innerHTML='centres at least '+fmt(L.dmin,1)+' m apart here (r&#8321; + r&#8322; + 0.1 m, snapped to the grid)';
    dispTag.innerHTML='drag a sphere or the ruler on the canvas; the ruler snaps to 0.1 m';
    runTag.innerHTML='space pauses &nbsp; <b>r</b> resets the run &nbsp; 1&ndash;4 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='lab')?'drag a sphere or the ruler · 1–4 switch views'
        :(st.view==='fall')?'release, then space pauses · r resets · 1–4 switch views':'1–4 switch views';
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
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ simReset(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  let frameN=0;
  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{ S.draw();
        if(advanced&&(frameN%10===0||S.ended())){ const M=S.model(); roEl.innerHTML=readoutHTML(M); tagEl.innerHTML=tagHTML(M); } }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  simReset(); resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  lab:'Newton&rsquo;s law of universal gravitation, published in the <i>Principia</i> in 1687, says that any two masses attract with a force '
    +'proportional to each mass and to the inverse square of the distance between them. Henry Cavendish first measured that pull between '
    +'laboratory lead spheres in 1797&ndash;98, which is what fixes the constant G. Drag either sphere, or set it with the sliders, and change the '
    +'masses: both arrows always change together, because the force on m&#8321; by m&#8322; and the force on m&#8322; by m&#8321; are the same size and '
    +'point opposite ways &mdash; Newton&rsquo;s third law. The distance is measured between the centres, and for a uniform sphere that is exact '
    +'rather than an approximation: a spherical shell attracts as though all its mass sat at its centre (Newton&rsquo;s shell theorem). With '
    +'constant size off, a sphere&rsquo;s radius grows as the cube root of its mass at 150 kg/m&sup3; (PhET&rsquo;s choice, about a seventh of '
    +'water&rsquo;s density, so the spheres fit on screen); with it on, every sphere has a radius of 0.5 m and its colour carries the mass. '
    +'The ruler measures distances: drag it, or send its zero to the centre of m&#8321;.',
  inv:'The law&rsquo;s signature is its exponent. Double the distance and the force falls to a quarter; halve it and the force grows four '
    +'times. On logarithmic axes an inverse-square law is a straight line of slope &minus;2 &mdash; any other power would tilt it &mdash; and the '
    +'readout measures that slope off the model at the live distance. Multiplying the force by r&sup2; should then leave a constant, '
    +'G m&#8321;m&#8322;, whatever the distance: the lower-right panel shows it flat, against the falling curve an inverse-cube law would draw. '
    +'The shaded bands are the distances the spheres cannot reach: inside the orange band they would overlap, and the paler one is the gap '
    +'PhET keeps between their surfaces. The same exponent has been tested from torsion balances at sub-millimetre range out to the orbits of '
    +'the planets.',
  prod:'The force is proportional to each mass separately: double m&#8321; and the force doubles, double both and it quadruples. So at a '
    +'fixed distance every pair with the same product m&#8321;m&#8322; feels the same force, and the contours of equal force are hyperbolas. '
    +'PhET&rsquo;s spheres add a twist. Their size grows with their mass, as the cube root at 150 kg/m&sup3;, and the centres can never come '
    +'closer than the two radii plus a gap, so heavy spheres cannot be brought as close as light ones. The lower-right panel shows the '
    +'strongest pull two equal masses can reach: for constant-size spheres it grows as m&sup2;, but for real ones the closest distance grows '
    +'with the mass too, and the maximum rises only about as m<sup>4/3</sup> &mdash; for touching spheres exactly '
    +'G m<sup>4/3</sup>(4&pi;&rho;/3)<sup>2/3</sup>/4. It is the reason a planet&rsquo;s surface gravity grows only as the cube root of its mass '
    +'when its density is fixed.',
  fall:'PhET holds the spheres in place. Here they are let go. Released from rest they fall toward each other along the track, and because '
    +'the forces on them are equal and opposite, their momenta stay equal and opposite: the centre of mass never moves, and the lighter sphere '
    +'covers most of the gap. The separation obeys one equation, r&Prime; = &minus;G(m&#8321; + m&#8322;)/r&sup2;, solved exactly here &mdash; the '
    +'time to fall from r&#8320; to r is the closed form in the equation bar, the same one that describes a comet plunging straight into the '
    +'Sun. For laboratory masses the answer is startling: 100 kg and 400 kg released 4 m apart take about twelve hours to touch, and meet at '
    +'a closing speed of 0.18 mm/s. Gravity is by far the weakest of the forces; only masses the size of planets make it feel strong. The '
    +'clock runs thousands of times fast, and the run stops at the moment of contact, where the model ends.',
};
