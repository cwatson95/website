
/* ================================================================== *
 *  boot — panel, tabs, handlers, frame loop                           *
 * ================================================================== */
function roundTo(x,step){ return Number((Math.round(x/step)*step).toFixed(8)); }
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
  let dirty=false, lastFly=-1, frameN=0;

  function fail(e){ errEl.style.display='block'; errEl.textContent=String(e&&e.stack||e); }
  window.addEventListener('error',ev=>fail(ev.error||ev.message));

  function setView(k){
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncChips(); syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  /* a change of air, altitude or gravity bends the projectiles already in the air */
  const envChanged=()=>{ retarget(st.view); };
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  /* a slider whose range follows the chosen projectile (PhET's Lab): linear,
     or logarithmic for the mass, which spans up to three decades */
  function rangeSlider(key,lab2,rangeFn,log,fmtf,onchg){
    const inp=h('input',{type:'range',min:0,max:1,step:0.001,value:0});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ const R=rangeFn();
      if(log){ inp.min=Math.log10(R[0]); inp.max=Math.log10(R[1]); inp.step=0.001; inp.value=Math.log10(st[key]); }
      else { inp.min=R[0]; inp.max=R[1]; inp.step=R[2]; inp.value=st[key]; }
      val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ const R=rangeFn(), x=parseFloat(inp.value);
      st[key]=roundTo(clamp(log?Math.pow(10,x):x,R[0],R[1]),R[2]);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; },inp};
    return el;
  }
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
        st[key]=o.id; if(onPick) onPick(o); syncChips(); syncPanel(); dirty=true; refresh(); }},o.name));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function button(label,fn){ return h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},label); }
  const fmtM=v=>sigf(v,3)+' m', fmtKg=v=>sigf(v,3)+' kg';

  /* ---- the projectile, one group per scene ---- */
  const gObjI=h('div',{class:'grp'},h('h3',null,'the projectile'));
  gObjI.appendChild(chipRow(OBJECTS.map(o=>({id:o.id,name:o.name})),'i_obj'));
  const tagObjI=h('div',{class:'tag'}); gObjI.appendChild(tagObjI);
  gObjI.appendChild(h('div',{class:'checks'},checkbox('i_air','air resistance',envChanged)));

  const gObjV=h('div',{class:'grp'},h('h3',null,'the sphere'));
  gObjV.appendChild(slider('v_d','diameter',SCREEN_OBJ.dR[0],SCREEN_OBJ.dR[1],SCREEN_OBJ.dR[2],fmtM));
  gObjV.appendChild(slider('v_m','mass',SCREEN_OBJ.mR[0],SCREEN_OBJ.mR[1],SCREEN_OBJ.mR[2],fmtKg));
  gObjV.appendChild(h('div',{class:'checks'},checkbox('v_air','air resistance',envChanged)));
  const tagObjV=h('div',{class:'tag'}); gObjV.appendChild(tagObjV);

  const gObjD=h('div',{class:'grp'},h('h3',null,'the sphere, in air'));
  gObjD.appendChild(slider('d_cd','drag coefficient',LIM.cd[0],LIM.cd[1],0.01,v=>fmt(v,2)));
  gObjD.appendChild(slider('d_d','diameter',SCREEN_OBJ.dR[0],SCREEN_OBJ.dR[1],SCREEN_OBJ.dR[2],fmtM));
  gObjD.appendChild(slider('d_m','mass',SCREEN_OBJ.mR[0],SCREEN_OBJ.mR[1],SCREEN_OBJ.mR[2],fmtKg));
  gObjD.appendChild(slider('d_alt','altitude',LIM.alt[0],LIM.alt[1],100,v=>fmt(v,0)+' m',envChanged));
  const tagObjD=h('div',{class:'tag'}); gObjD.appendChild(tagObjD);

  const gObjL=h('div',{class:'grp'},h('h3',null,'the projectile'));
  gObjL.appendChild(chipRow([{id:'custom',name:'custom'}].concat(OBJECTS.map(o=>({id:o.id,name:o.name}))),'l_obj',
    o=>{ const O=objById(o.id); st.l_m=O.m; st.l_d=O.d; st.l_cd=O.cd; }));
  gObjL.appendChild(rangeSlider('l_m','mass',()=>objById(st.l_obj).mR,true,fmtKg));
  gObjL.appendChild(rangeSlider('l_d','diameter',()=>objById(st.l_obj).dR,false,fmtM));
  gObjL.appendChild(slider('l_cd','drag coefficient',CUSTOM.cdR[0],CUSTOM.cdR[1],CUSTOM.cdR[2],v=>fmt(v,2)));
  const tagObjL=h('div',{class:'tag'}); gObjL.appendChild(tagObjL);
  const gWorld=h('div',{class:'grp'},h('h3',null,'the world'));
  gWorld.appendChild(slider('l_g','gravity',LIM.g[0],LIM.g[1],0.01,v=>fmt(v,2)+' m/s²',envChanged));
  gWorld.appendChild(h('div',{class:'checks'},checkbox('l_air','air resistance',envChanged)));
  gWorld.appendChild(slider('l_alt','altitude',LIM.alt[0],LIM.alt[1],100,v=>fmt(v,0)+' m',envChanged));

  /* ---- the cannon, one group per scene ---- */
  const fireBtns=[];
  function cannonGroup(p){
    const g=h('div',{class:'grp'},h('h3',null,'the cannon'));
    g.appendChild(slider(p+'h','height',LIM.h[0],LIM.h[1],0.1,v=>fmt(v,1)+' m'));
    g.appendChild(slider(p+'th','angle',LIM.th[0],LIM.th[1],1,v=>fmt(v,0)+'°'));
    g.appendChild(slider(p+'v0','initial speed',LIM.v0[0],LIM.v0[1],0.1,v=>fmt(v,1)+' m/s'));
    const fb=h('button',{onclick:()=>{ if(fire(st.view)){ syncPanel(); dirty=true; refresh(); } }},'fire');
    fireBtns.push(fb);
    g.appendChild(h('div',{class:'btnrow'},fb,button('erase',()=>erase(st.view))));
    g.appendChild(h('div',{class:'tag',html:'drag the barrel to aim, the pedestal to raise it'}));
    return g;
  }
  const gCanI=cannonGroup('i_'), gCanV=cannonGroup('v_'), gCanD=cannonGroup('d_'), gCanL=cannonGroup('l_');

  /* ---- vectors ---- */
  const gVecI=h('div',{class:'grp'},h('h3',null,'vectors'),h('div',{class:'checks'},
    checkbox('i_vt','velocity, total'),checkbox('i_vc','velocity, components'),
    checkbox('i_at','acceleration, total'),checkbox('i_ac','acceleration, components')));
  const MODES=[{id:'total',name:'total'},{id:'components',name:'components'}];
  const gVecV=h('div',{class:'grp'},h('h3',null,'vectors'),chipRow(MODES,'v_mode'),h('div',{class:'checks'},
    checkbox('v_vel','velocity'),checkbox('v_acc','acceleration'),checkbox('v_frc','force'),checkbox('v_strobe','strobe along the shot, every 0.5 s')));
  const gVecD=h('div',{class:'grp'},h('h3',null,'vectors'),chipRow(MODES,'d_mode'),h('div',{class:'checks'},
    checkbox('d_vel','velocity'),checkbox('d_frc','force')));

  /* ---- tools and time (every scene) ---- */
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'),h('div',{class:'checks'},
    checkbox('tape','tape measure'),checkbox('probe','data probe'),checkbox('vacRef','the same shot without air (when the air is on)')));
  gTools.appendChild(slider('zoom','zoom',ZOOM[0],ZOOM[1],0.01,v=>'×'+fmt(v,2)));
  const gTime=h('div',{class:'grp'},h('h3',null,'time'),h('div',{class:'checks'},checkbox('running','time runs')));
  gTime.appendChild(chipRow([{id:'normal',name:'normal'},{id:'slow',name:'slow (×0.33)'}],'speed'));
  gTime.appendChild(h('div',{class:'btnrow'},button('step',()=>{ if(isScene(st.view)) advance(st.view,S.dt()); })));
  const timeTag=h('div',{class:'tag'}); gTime.appendChild(timeTag);

  /* ---- the analysis views share one shot ---- */
  const gShot=h('div',{class:'grp'},h('h3',null,'the shot'));
  gShot.appendChild(chipRow(ANALYSIS_OBJS,'a_obj'));
  gShot.appendChild(h('div',{class:'checks'},checkbox('a_air','air resistance')));
  gShot.appendChild(slider('a_alt','altitude',LIM.alt[0],LIM.alt[1],100,v=>fmt(v,0)+' m'));
  gShot.appendChild(slider('a_g','gravity',LIM.g[0],LIM.g[1],0.01,v=>fmt(v,2)+' m/s²'));
  gShot.appendChild(slider('a_h','height',LIM.h[0],LIM.h[1],0.1,v=>fmt(v,1)+' m'));
  gShot.appendChild(slider('a_th','angle',LIM.th[0],LIM.th[1],1,v=>fmt(v,0)+'°'));
  gShot.appendChild(slider('a_v0','initial speed',LIM.v0[0],LIM.v0[1],0.1,v=>fmt(v,1)+' m/s'));
  const gEnvO=h('div',{class:'grp'},h('h3',null,'the fan'),h('div',{class:'checks'},checkbox('e_vac','the same fan in vacuum')));
  const gHodO=h('div',{class:'grp'},h('h3',null,'the flight'),h('div',{class:'checks'},checkbox('o_cliff','fly on past the ground, as if off a cliff')));

  const gReset=h('div',{class:'grp'},h('div',{class:'btnrow'},button('reset all',()=>{
    const v=st.view; Object.assign(st,DEFAULTS); st.view=v; SCENE_VIEWS.forEach(scnReset); DRAG.what=null; syncChips(); })));
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Projectile Motion (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values, read out of projectile-motion 1.0.34: '
      +'the nine projectiles&rsquo; mass, diameter and drag coefficient, g = 9.81 m/s&sup2;, the slider ranges, the target and its stars, '
      +'and NASA Glenn&rsquo;s air-density fit. Everything else is computed and pinned in selfTest to build/projectile-motion/derive.py '
      +'(scipy DOP853, the exact hodograph of quadratic drag, the vacuum and vertical closed forms).'}));
  const GROUPS=[gObjI,gObjV,gObjD,gObjL,gWorld,gCanI,gCanV,gCanD,gCanL,gVecI,gVecV,gVecD,gShot,gEnvO,gHodO,gTools,gTime,gReset,gInfo];
  GROUPS.forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS)
      [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  function syncPanel(){
    const v=st.view, sc=isScene(v);
    gObjI.hidden=v!=='intro'; gCanI.hidden=v!=='intro'; gVecI.hidden=v!=='intro';
    gObjV.hidden=v!=='vectors'; gCanV.hidden=v!=='vectors'; gVecV.hidden=v!=='vectors';
    gObjD.hidden=v!=='drag'; gCanD.hidden=v!=='drag'; gVecD.hidden=v!=='drag';
    gObjL.hidden=v!=='lab'; gWorld.hidden=v!=='lab'; gCanL.hidden=v!=='lab';
    gShot.hidden=sc; gEnvO.hidden=v!=='env'; gHodO.hidden=v!=='hodo';
    gTools.hidden=!sc; gTime.hidden=!sc;
    /* a control that is live but ignored is worse than none: dim it (Known-bad) */
    rows.l_cd.inp.disabled=!(st.l_obj==='custom'&&st.l_air);
    rows.l_alt.inp.disabled=!st.l_air; rows.a_alt.inp.disabled=!st.a_air;
    const full=sc&&flyingCount(v)>=MAX_FLYING; fireBtns.forEach(b=>{ b.disabled=full; });
    for(const k in rows) rows[k].sync();
    const O=objById(st.i_obj);
    tagObjI.innerHTML=O.name+': '+sigf(O.m,3)+' kg, '+sigf(O.d,3)+' m across, C<sub>d</sub> '+fmt(O.cd,2)+(st.i_air?'':' <span class="r">(C<sub>d</sub> unused: no air)</span>');
    tagObjV.innerHTML='drag coefficient '+fmt(SCREEN_OBJ.cd,2)+' (a sphere)'+(st.v_air?'':' <span class="r">— unused: no air</span>');
    tagObjD.innerHTML='C<sub>d</sub> '+fmt(st.d_cd,2)+': '+cdWord(st.d_cd)+'; air '+sigf(airDensity(st.d_alt),4)+' kg/m&sup3; at '+fmt(st.d_alt,0)+' m (NASA Glenn fit)';
    tagObjL.innerHTML=st.l_obj==='custom'?'custom: every value yours; C<sub>d</sub> works with the air on':'C<sub>d</sub> '+fmt(st.l_cd,2)+' is '+objById(st.l_obj).name+'&rsquo;s own (PhET&rsquo;s value)';
    timeTag.innerHTML='<b>f</b> fires &nbsp; <b>e</b> erases &nbsp; space pauses &nbsp; 1&ndash;6 switch views';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=isScene(st.view)?'fire · drag the barrel, the pedestal, the target, the tape, the probe · wheel zooms':'1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    const r=canvas.getBoundingClientRect();
    /* a grab changes nothing on screen, so it does not mark the frame dirty; the moves do */
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.setPointerCapture(e.pointerId); canvas.classList.add('dragging'); }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model()); tagEl.innerHTML=tagHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);
  canvas.addEventListener('wheel',e=>{ if(S.wheel(e.deltaY)){ e.preventDefault(); rows.zoom.sync(); dirty=true; } },{passive:false});

  window.addEventListener('keydown',e=>{
    if(e.key===' '){ e.preventDefault(); st.running=!st.running; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='f'){ if(fire(st.view)){ syncPanel(); dirty=true; refresh(); } }
    else if(e.key==='e'){ erase(st.view); syncPanel(); dirty=true; refresh(); }
    else if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  function frameLoop(){
    frameN++;
    const advanced=S.step();
    if(advanced||dirty){
      dirty=false;
      try{
        S.draw();
        const fly=isScene(st.view)?flyingCount(st.view):0;
        if(advanced&&(fly!==lastFly||frameN%8===0)){ roEl.innerHTML=readoutHTML(S.model()); syncPanel(); }
        lastFly=fly;
      }catch(e){ fail(e); }
    }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  intro:'This is PhET&rsquo;s Intro screen. The cannon sits on a pedestal: drag its barrel to aim it and the pedestal to raise it, '
    +'pick one of PhET&rsquo;s nine projectiles, and fire. Without air every one of them leaves on the same parabola &mdash; a golf ball '
    +'and a piano fly identical paths, because when gravity is the only force the mass cancels out of Newton&rsquo;s second law. Every '
    +'number about that parabola is closed form, down to the landing speed &radic;(v<sub>0</sub>&sup2; + 2gh), which does not depend on the angle at all. '
    +'Switch the air on and the objects part company: the drag &frac12;&rho;C<sub>d</sub>Av&sup2; is divided by the mass, so a light, wide, blunt '
    +'pumpkin loses far more than a dense, narrow, pointed tank shell. Land on the target for stars; the data probe reads the time, range and '
    +'height off the dots the flight leaves every tenth of a second, and the tape measures anything.',
  vectors:'PhET&rsquo;s Vectors screen. The velocity (green) is tangent to the path. The acceleration (magenta) in vacuum is g, straight down, '
    +'at every instant &mdash; the single fact that makes the path a parabola: v<sub>x</sub> never changes and v<sub>y</sub> falls at a steady rate. '
    +'With the air on, the drag adds a part pointing back along the velocity, so the acceleration leans against the motion and weakens as the '
    +'shot slows. The force arrows show the weight and the drag separately, the weight drawn at a fixed length so the drag reads as a fraction '
    +'of it. The dashed path carries a strobe of the same vectors every half second, before you fire. Resize or reweigh the sphere: in vacuum '
    +'nothing moves; with air a wider or lighter sphere is dragged harder, because only &rho;C<sub>d</sub>A/2m enters the motion.',
  drag:'PhET&rsquo;s Drag screen, with the air always on. The drag coefficient says how bluff the body is: 0.47 is a sphere, smaller values a '
    +'streamlined body, larger ones a sphere with its front cut flat, toward a flat-faced cup (the shape is drawn at the top left). The green '
    +'dashed curve is this shot with the air and the orange one the same shot in vacuum. The difference is not a shrunken copy: with drag the '
    +'shot climbs less, lands short, and comes down steeper than it went up, because it is slower on the way down. Raise the altitude and '
    +'the air thins &mdash; NASA Glenn&rsquo;s atmosphere fit, PhET&rsquo;s model, gives 1.227 kg/m&sup3; at sea level and 0.738 at 5 km &mdash; '
    +'so the shot flies further. The terminal speed &radic;(2mg/&rho;C<sub>d</sub>A) in the readout is where the drag would hold the weight: '
    +'this default sphere reaches it at 18.4 m/s, about the speed it is fired at.',
  lab:'PhET&rsquo;s Lab screen: any projectile, or a custom one, and a world you can change. Gravity runs from 5 to 20 m/s&sup2;; in vacuum, fired '
    +'from the ground, the range scales as 1/g, so halving gravity doubles it. The mass matters only with the air on, and only through k = &rho;C<sub>d</sub>A/2m: '
    +'a projectile twice as heavy and &radic;2 times as wide flies exactly the same path, which the self-test asserts. Changing gravity, the air or '
    +'the altitude while projectiles are in flight bends their paths from where they are, as in PhET; the mass, the size and the launch '
    +'settings apply to the next shot. The drag coefficient is each object&rsquo;s own (the piano&rsquo;s 1.2 is PhET&rsquo;s value); only the '
    +'custom projectile lets you set it.',
  env:'Every shot at one speed. In vacuum the family of parabolas has an envelope, the parabola of safety y = h + v<sub>0</sub>&sup2;/2g &minus; '
    +'gx&sup2;/2v<sub>0</sub>&sup2;, whose focus is the cannon: the shot at angle &theta; touches it where tan &theta; = v<sub>0</sub>&sup2;/gx, which is above the '
    +'ground for every shot steeper than the best angle (the flatter ones land first), and nothing fired at that speed reaches beyond it. '
    +'Its foot on the ground is the longest range, at tan &theta;* = v<sub>0</sub>/&radic;(v<sub>0</sub>&sup2; + 2gh): '
    +'45&deg; from the ground and less from a height, because a flatter shot spends the extra fall moving forward. With the air on the whole fan '
    +'shrinks and the best angle drops below 45&deg;, since a flatter shot spends less time in the air losing speed. That angle is found here by '
    +'golden-section search over full integrations and checked against scipy&rsquo;s.',
  hodo:'The hodograph is the path traced by the tip of the velocity vector. In vacuum it is a vertical line crossed at a steady rate: gravity '
    +'changes v<sub>y</sub> by g every second and leaves v<sub>x</sub> alone. Quadratic drag has no closed-form trajectory, but its hodograph '
    +'is exact: with u = v cos &phi; the horizontal velocity and &phi; its angle, 1/u&sup2; &minus; 1/u<sub>0</sub>&sup2; = (k/g)[F(&theta;) &minus; F(&phi;)], '
    +'F(&psi;) = sin &psi;/cos&sup2;&psi; + ln tan(&pi;/4 + &psi;/2). The orange curve is that formula and the green one the integrator, which '
    +'must lie on it. Integrating dt = &minus;u sec&sup2;&phi; d&phi;/g along the formula gives the range by a route that shares no code with the '
    +'integrator, and the readout compares the two. Let the shot fly on past the ground and the curve heads for (0, &minus;v<sub>t</sub>), where '
    +'the drag holds the weight. The energy ledger below must stay flat: what the shot loses in kinetic plus potential energy is exactly what '
    +'the air has taken, integrated inside the same steps.',
};
