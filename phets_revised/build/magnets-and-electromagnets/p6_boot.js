
/* ================================================================== *
 *  the scene, the dispatch, boot                                      *
 * ================================================================== */
function drawView(ctx,W,H,M){
  if(M.view==='bar') return drawBarScreen(ctx,W,H,M);
  if(M.view==='em') return drawEMScreen(ctx,W,H,M);
  if(M.view==='lines') return drawLinesView(ctx,W,H,M);
  if(M.view==='axis') return drawAxisView(ctx,W,H,M);
  if(M.view==='far') return drawFarView(ctx,W,H,M);
  return drawNeedleView(ctx,W,H,M);
}
function makeScene(canvas){
  const S={canvas,W:1400,H:820,st:ST};
  S.ctx=()=>canvas&&canvas.getContext?canvas.getContext('2d'):null;
  S.model=()=>buildModel();
  S.draw=()=>{ drawView(canvas.getContext('2d'),S.W,S.H,buildModel()); };
  S.step=dt=>stepLive(dt);
  S.pointer=(type,x,y)=>screenPointer(type,x,y,S.W,S.H,S.ctx());
  return S;
}
function flipMagnet(st){
  st.bar.ang=(st.bar.ang+Math.PI)%(2*Math.PI);
  /* PhET kicks the needle when the magnet flips, or it would sit on the unstable equilibrium */
  if(LIVE.barRot){ LIVE.barRot.om+=FLIP_KICK; LIVE.barRot.rest=false; }
}

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
    st.view=k; DRAG.what=null;
    [].forEach.call(tabsEl.children,(b,i)=>b.className=TABS[i][0]===st.view?'active':'');
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg,tr,itr){
    /* tr/itr: an optional transform between the slider's position and the state (log sliders) */
    const toS=tr||(v=>v), toP=itr||(v=>v);
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:toP(st[key])});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=toP(st[key]); val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=toS(parseFloat(inp.value)); val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked; if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; },inp};
    return el;
  }
  const chipRows=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{ wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
      if(onPick) onPick(o); else st[key]=o.id; syncPanel(); dirty=true; refresh(); }},o.name)); });
    chipRows.push({el:wrapEl,list,key}); return wrapEl;
  }
  const btn=(txt,fn)=>h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},txt);

  /* the bar magnet screen */
  const gBar=h('div',{class:'grp'},h('h3',null,'the bar magnet'));
  gBar.appendChild(slider('pct','strength',0,100,5,v=>fmt(v,0)+' %'));
  const flipBtn=btn('flip polarity',()=>flipMagnet(st));
  gBar.appendChild(h('div',{class:'btnrow'},flipBtn));
  gBar.appendChild(h('div',{class:'checks'},checkbox('barField','magnetic field (B)'),checkbox('seeInside','see inside'),checkbox('earth','Earth')));
  const gBarTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gBarTools.appendChild(h('div',{class:'checks'},checkbox('barCompass','compass',()=>{ LIVE.barRot=null; }),checkbox('barMeter','field meter')));
  const barTag=h('div',{class:'tag'}); gBarTools.appendChild(barTag);

  /* the electromagnet screen */
  const gEM=h('div',{class:'grp'},h('h3',null,'the electromagnet'));
  gEM.appendChild(slider('loops','loops',1,COIL_NMAX,1,v=>fmt(v,0)));
  gEM.appendChild(h('div',{class:'tag'},'current source'));
  gEM.appendChild(chipRow([{id:'dc',name:'DC power supply'},{id:'ac',name:'AC power supply'}],'supply',o=>{ st.supply=o.id; LIVE.emT=0; }));
  gEM.appendChild(slider('dcV','battery voltage',-DC_VMAX,DC_VMAX,0.5,v=>(v>0?'+':v<0?'−':'')+fmt(Math.abs(v),1)+' V'));
  gEM.appendChild(slider('acPk','maximum voltage',0,100,5,v=>fmt(v,0)+' %'));
  gEM.appendChild(slider('acFp','frequency',10,100,5,v=>fmt(v,0)+' %'));
  gEM.appendChild(h('div',{class:'checks'},checkbox('electrons','electrons'),checkbox('emField','magnetic field (B)')));
  const gEMTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gEMTools.appendChild(h('div',{class:'checks'},checkbox('emCompass','compass',()=>{ LIVE.emRot=null; }),checkbox('emMeter','field meter')));
  const emTag=h('div',{class:'tag'}); gEMTools.appendChild(emTag);

  /* the analysis views */
  const gSrc=h('div',{class:'grp'},h('h3',null,'the source'));
  gSrc.appendChild(chipRow([{id:'magnet',name:'bar magnet'},{id:'coil',name:'electromagnet'}],'src'));
  gSrc.appendChild(h('div',{class:'checks'},checkbox('bound','bound current on the magnet'),checkbox('axisH','μ₀H inside the magnet')));
  const srcTag=h('div',{class:'tag'}); gSrc.appendChild(srcTag);

  /* the needle */
  const gNd=h('div',{class:'grp'},h('h3',null,'the needle'));
  gNd.appendChild(slider('ndB','|B|',Math.log10(0.05),Math.log10(S_MAX),0.01,v=>sigf(v,3)+' G',null,p=>+Math.pow(10,p).toPrecision(3),v=>Math.log10(v)));
  gNd.appendChild(slider('ndRel','released at',1,179,1,v=>fmt(v,0)+'°'));
  gNd.appendChild(slider('ndDamp','damping γ',0,10,0.1,v=>fmt(v,1)+' /s'));
  const ndTag=h('div',{class:'tag'}); gNd.appendChild(ndTag);

  /* preferences, run, reset */
  const gPref=h('div',{class:'grp'},h('h3',null,'units and conventions'));
  gPref.appendChild(chipRow([{id:'G',name:'G (gauss)'},{id:'T',name:'T (tesla)'}],'units'));
  gPref.appendChild(chipRow([{id:'electron',name:'electron'},{id:'conventional',name:'conventional'}],'flowConv'));
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('run','animate')));
  gRun.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; resetState({view:v}); DRAG.what=null; for(const k in MEMO) delete MEMO[k]; })));
  const keysTag=h('div',{class:'tag'}); gRun.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Magnets and Electromagnets (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'Measured: &mu;<sub>0</sub> = 1.25663706127&times;10<sup>&minus;6</sup> N/A&sup2; (CODATA 2022, NIST), the only measured number. '
      +'PhET&rsquo;s values (read from its 1.0.7 build): the 250 &times; 50 bar (a cylinder, MathCAD model of strength 1 G), 0&ndash;300 G, 75 % at start; the 40-px needle grid and its 2(|B|/300 G)<sup>1/2.7</sup> brightness; '
      +'the compass constants 0.01 /G/frame&sup2; and 0.08 /frame at 25 frames/s; the coil of 1&ndash;4 loops of radius 50 and wire width 16; the &plusmn;10 V battery, the 0&ndash;110 V AC supply at 1.25 Hz &times; its frequency %. '
      +'Everything else is computed, pinned in selfTest to build/magnets-and-electromagnets/derive.py (scipy dblquad, quad, solve_ivp, brentq).'}));
  const groups={bar:[gBar,gBarTools],em:[gEM,gEMTools],lines:[gSrc],axis:[gSrc],far:[gSrc],needle:[gNd]};
  [gBar,gBarTools,gEM,gEMTools,gSrc,gNd,gPref,gRun,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncPanel(){
    const v=st.view;
    for(const g of [gBar,gBarTools,gEM,gEMTools,gSrc,gNd]) g.hidden=groups[v].indexOf(g)<0;
    /* a control that is live but ignored is worse than none: dim what does nothing */
    rows.dcV.inp.disabled=st.supply!=='dc'; rows.acPk.inp.disabled=st.supply!=='ac'; rows.acFp.inp.disabled=st.supply!=='ac';
    rows.cb_bound.inp.disabled=!(v==='lines'&&st.src==='magnet'); rows.cb_axisH.inp.disabled=!(v==='axis'&&st.src==='magnet');
    for(const k in rows) rows[k].sync();
    for(const c of chipRows) [].forEach.call(c.el.children,(b,i)=>b.className='chip'+(st[c.key]===c.list[i].id?' on':''));
    flipBtn.textContent=st.earth?'flip Earth':'flip polarity';
    barTag.innerHTML='drag the magnet, the compass and the meter; the needle is a damped rotor, so it swings';
    emTag.innerHTML='drag the coil, the compass and the meter; '+(st.supply==='ac'?'the AC supply swings the current, and the field, back and forth':'the battery voltage sets a steady current');
    srcTag.innerHTML=st.src==='magnet'?'the bar magnet at its strength ('+fB(S_MAX*st.pct/100)+')':'the electromagnet at its present current';
    ndTag.innerHTML='critical damping at |B| = &gamma;&sup2;/4&kappa; = '+sigf(st.ndDamp*st.ndDamp/(4*KAPPA),3)+' G';
    keysTag.innerHTML='<b>1</b>&ndash;<b>6</b> switch views, <b>space</b> pauses, <b>f</b> flips the magnet';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='bar'||st.view==='em'?'drag the objects · ':'')+'space pauses · 1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    if(canvas.setPointerCapture) canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }
  });
  canvas.addEventListener('pointermove',e=>{
    if(!DRAG.what) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
    else if(e.key===' '){ if(e.preventDefault) e.preventDefault(); st.run=!st.run; syncPanel(); dirty=true; refresh(); }
    else if(e.key==='f'&&st.view==='bar'){ flipMagnet(st); syncPanel(); dirty=true; refresh(); }
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  /* the loop: the live clocks advance only while 'animate' is on, and the page repaints only
     when something moved or a handler marked it dirty */
  let last=null;
  function frameLoop(ts){
    const dt=(last===null)?0:Math.min(0.05,Math.max(0,(ts-last)/1000)); last=ts;
    if(st.run&&dt>0&&S.step(dt)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  bar:'This is PhET&rsquo;s Bar Magnet screen. The magnet is a cylinder 250 mm long and 50 mm across, magnetised uniformly along its length, and the field it makes is computed exactly: a uniformly magnetised bar produces precisely the field of a solenoid whose current flows round its surface, so the field is the closed form for a finite solenoid, built from complete elliptic integrals. PhET computed that same field once, in MathCAD, and stored it on grids; this page evaluates it wherever it is needed. The needles show the direction of the field everywhere at once; their brightness follows PhET&rsquo;s display rule, which fades them with distance but is not the field&rsquo;s size. Drag the compass around the magnet and its needle swings into line with the field, overshoots and settles, because a compass needle is a little magnet on a pivot, a damped pendulum in the field. The field meter reads the field at its crosshair. Inside the magnet the field runs from the south pole to the north pole, closing every loop that leaves the north end; tick <b>see inside</b> to see it. The Earth is drawn the way PhET draws it, as a reminder that the Earth&rsquo;s magnetic field is roughly that of a bar magnet whose south pole lies near the geographic north.',
  em:'This is PhET&rsquo;s Electromagnet screen: a coil of one to four loops driven by a battery or an alternating supply. Each loop&rsquo;s field comes from the Biot&ndash;Savart law, summed exactly around the loop in complete elliptic integrals, and the loops simply add. More current or more loops make a stronger field, and reversing the current reverses it, so on the AC supply the needles and the compass swing back and forth as the current alternates. Outside the coil the field has the same shape as the bar magnet&rsquo;s: an electromagnet is a magnet you can switch off. The current is set so that PhET&rsquo;s strongest setting, four loops at full current, makes PhET&rsquo;s strongest field, 300 G at the centre; that takes 704 A through four turns, which is why real electromagnets use many turns of thin wire instead. The electrons are drawn moving round the loops at a speed that shows the size and direction of the current, not the real drift speed.',
  lines:'Field lines follow the field. Because both sources are symmetric about their axis and the page contains that axis, every line drawn here is an exact field line, traced by small steps along B. They are spaced so that the same amount of flux runs between each neighbouring pair when the lines are spun round the axis into tubes, which is why they crowd where the field is strong. Every B line is a closed loop: it leaves the north face, curls round, returns into the south face and runs back through the magnet to where it started, because magnetic field lines never begin or end; there are no magnetic charges. The dots and crosses on the magnet&rsquo;s long sides mark the bound current that circulates round its surface. A solenoid carrying the same current per length makes exactly the same field, and the electromagnet&rsquo;s lines, which you can switch to, have the same shape outside the coil.',
  axis:'Along the axis the field of the magnet is elementary: it is half of &mu;<sub>0</sub>M times the difference between two cosines, one for each pole face. It is strongest at the centre, 0.981 of &mu;<sub>0</sub>M for this long thin bar, and exactly half as strong at each face, and it passes through the faces without a break. The other field, H, does not: inside the magnet &mu;<sub>0</sub>H is B minus &mu;<sub>0</sub>M, so it jumps by &mu;<sub>0</sub>M at each face and points backwards inside, from the north pole to the south pole. That backward field is the demagnetising field, and it is why a short, fat magnet is weaker inside than a long, thin one. For the electromagnet, each loop gives the textbook field on its axis and the loops add; a continuous sheet of current with the same total ampere-turns, the ideal solenoid, is drawn beside them. More, closer loops tend to it, with an error that falls as the square of the spacing.',
  far:'From far away every magnet looks the same: a point dipole, whose field falls as the inverse cube of the distance and is twice as strong along the axis as on the bisector at the same distance. Its strength is set by one number, the magnetic moment: the magnetisation times the volume for the bar, the number of turns times the current times the loop&rsquo;s area for the coil. The first correction is the octupole, which fades two powers of the distance faster, so the fractional difference from the dipole falls as one over the distance squared: the straight lines of slope &minus;2 in the lower plot. Both limits are taken numerically in the readout by evaluating the exact field at 2, 4 and 8 m and extrapolating, and both come out at 1 to within a few parts in a billion, while the approach agrees with the octupole coefficients worked out in closed form.',
  needle:'A compass needle is a small magnet on a pivot, and in a field it behaves like a pendulum: the torque pulling it back is proportional to the sine of its angle from the field, so it swings, and friction makes the swings die away. This view releases the needle at an angle and integrates its motion, using PhET&rsquo;s constants for the needle&rsquo;s response to the field and its damping. For small swings the solution is the damped oscillator, drawn in orange; at large angles the needle lingers near the top of its swing and the period grows, exactly as for a pendulum, by the factor given by the complete elliptic integral. The period of small swings is 2&pi;/&radic;(&kappa;|B|), so it halves when the field is four times stronger: timing a swinging magnet is how Gauss first measured the strength of the Earth&rsquo;s field in 1832. The energy of the needle plus the work done against the damping is conserved, and the readout checks it.'
};
