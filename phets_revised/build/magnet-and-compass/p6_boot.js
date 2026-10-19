
/* ================================================================== *
 *  the scene, the dispatch, boot                                      *
 * ================================================================== */
function drawView(ctx,W,H,M){
  if(M.view==='bar') return drawBarScreen(ctx,W,H,M);
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
  function chipRow(list,key){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{ wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),onclick:()=>{
      st[key]=o.id; syncPanel(); dirty=true; refresh(); }},o.name)); });
    chipRows.push({el:wrapEl,list,key}); return wrapEl;
  }
  const btn=(txt,fn)=>h('button',{onclick:()=>{ fn(); syncPanel(); dirty=true; refresh(); }},txt);

  const gBar=h('div',{class:'grp'},h('h3',null,'the bar magnet'));
  gBar.appendChild(slider('pct','strength',0,100,5,v=>fmt(v,0)+' %'));
  const flipBtn=btn('flip polarity',()=>flipMagnet(st));
  gBar.appendChild(h('div',{class:'btnrow'},flipBtn));
  gBar.appendChild(h('div',{class:'checks'},checkbox('barField','magnetic field (B)'),checkbox('seeInside','see inside'),checkbox('earth','Earth')));
  const gTools=h('div',{class:'grp'},h('h3',null,'tools'));
  gTools.appendChild(h('div',{class:'checks'},checkbox('barCompass','compass',()=>{ LIVE.barRot=null; }),checkbox('barMeter','field meter')));
  const barTag=h('div',{class:'tag'}); gTools.appendChild(barTag);

  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},checkbox('bound','bound current on the magnet'),checkbox('axisH','μ₀H inside the magnet')));
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  const gNd=h('div',{class:'grp'},h('h3',null,'the needle'));
  gNd.appendChild(slider('ndB','|B|',Math.log10(0.05),Math.log10(S_MAX),0.01,v=>sigf(v,3)+' G',null,p=>+Math.pow(10,p).toPrecision(3),v=>Math.log10(v)));
  gNd.appendChild(slider('ndRel','released at',1,179,1,v=>fmt(v,0)+'°'));
  gNd.appendChild(slider('ndDamp','damping γ',0,10,0.1,v=>fmt(v,1)+' /s'));
  const ndTag=h('div',{class:'tag'}); gNd.appendChild(ndTag);

  const gPref=h('div',{class:'grp'},h('h3',null,'units'));
  gPref.appendChild(chipRow([{id:'G',name:'G (gauss)'},{id:'T',name:'T (tesla)'}],'units'));
  const gRun=h('div',{class:'grp'},h('h3',null,'time'));
  gRun.appendChild(h('div',{class:'checks'},checkbox('run','animate')));
  gRun.appendChild(h('div',{class:'btnrow'},btn('reset all',()=>{ const v=st.view; resetState({view:v}); DRAG.what=null; for(const k in MEMO) delete MEMO[k]; })));
  const keysTag=h('div',{class:'tag'}); gRun.appendChild(keysTag);

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Magnet and Compass (University of Colorado Boulder, phet.colorado.edu, CC-BY 4.0). '
      +'New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'Measured: &mu;<sub>0</sub> = 1.25663706127&times;10<sup>&minus;6</sup> N/A&sup2; (CODATA 2022, NIST), the only measured number. '
      +'PhET&rsquo;s values (read from its 1.0.7 build): the 250 &times; 50 bar (a cylinder, MathCAD model of strength 1 G), 0&ndash;300 G, 75 % at start; the 40-px needle grid and its '
      +'2(|B|/300 G)<sup>1/2.7</sup> brightness; the compass constants 0.01 /G/frame&sup2; and 0.08 /frame at 25 frames/s; the 1024 &times; 618 layout and the objects&rsquo; places. '
      +'Everything else is computed, pinned in selfTest to build/magnets-and-electromagnets/derive.py (scipy dblquad, quad, solve_ivp, brentq).'}));
  const groups={bar:[gBar,gTools],lines:[gShow],axis:[gShow],far:[],needle:[gNd]};
  [gBar,gTools,gShow,gNd,gPref,gRun,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncPanel(){
    const v=st.view;
    for(const g of [gBar,gTools,gShow,gNd]) g.hidden=groups[v].indexOf(g)<0;
    /* a control that is live but ignored is worse than none: dim what does nothing here */
    rows.cb_bound.inp.disabled=(v!=='lines'); rows.cb_axisH.inp.disabled=(v!=='axis');
    for(const k in rows) rows[k].sync();
    for(const c of chipRows) [].forEach.call(c.el.children,(b,i)=>b.className='chip'+(st[c.key]===c.list[i].id?' on':''));
    flipBtn.textContent=st.earth?'flip Earth':'flip polarity';
    barTag.innerHTML='drag the magnet, the compass and the meter; the needle is a damped rotor, so it swings';
    showTag.innerHTML=v==='lines'?'the bound current is the surface current a solenoid would carry to make this field'
      :'&mu;<sub>0</sub>H = B &minus; &mu;<sub>0</sub>M inside the magnet, and points the other way';
    ndTag.innerHTML='critical damping at |B| = &gamma;&sup2;/4&kappa; = '+sigf(st.ndDamp*st.ndDamp/(4*KAPPA),3)+' G';
    keysTag.innerHTML='<b>1</b>&ndash;<b>5</b> switch views, <b>space</b> pauses, <b>f</b> flips the magnet';
  }
  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='bar'?'drag the magnet and the tools · ':'')+'space pauses · 1–5 switch views';
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
  bar:'This is PhET&rsquo;s Bar Magnet screen, the whole of Magnet and Compass. The magnet is a cylinder 250 mm long and 50 mm across, magnetised uniformly along its length, and the field it makes is computed exactly: a uniformly magnetised bar produces precisely the field of a solenoid whose current flows round its surface, so the field is the closed form for a finite solenoid, built from complete elliptic integrals. PhET computed that same field once, in MathCAD, and stored it on grids; this page evaluates it wherever it is needed. The needles show the direction of the field everywhere at once; their brightness follows PhET&rsquo;s display rule, which fades them with distance but is not the field&rsquo;s size. Drag the compass around the magnet and its needle swings into line, overshoots and settles, because a compass needle is a little magnet on a pivot, a damped pendulum in the field. The field meter reads the field at its crosshair. Inside the magnet the field runs from the south pole to the north pole, closing every loop that leaves the north end; tick <b>see inside</b> to see it. The Earth is drawn the way PhET draws it, as a reminder that the Earth&rsquo;s magnetic field is roughly that of a bar magnet whose south pole lies near the geographic north &mdash; which is why the end of a compass needle we call north points that way.',
  lines:'Field lines follow the field. Because the magnet is symmetric about its axis and the page contains that axis, every line drawn here is an exact field line, traced by small steps along B. They are spaced so that the same flux runs between each neighbouring pair when the lines are spun round the axis into tubes, which is why they crowd where the field is strong. Every B line is a closed loop: it leaves the north face, curls round, returns into the south face and runs back through the magnet to where it started, because magnetic field lines never begin or end; there are no magnetic charges. The dots and crosses on the magnet&rsquo;s long sides mark the bound current that circulates round its surface: a solenoid carrying the same current per unit length makes exactly the same field, inside and out.',
  axis:'Along the axis the field is elementary: it is half of &mu;<sub>0</sub>M times the difference between two cosines, one for each pole face. It is strongest at the centre, 0.981 of &mu;<sub>0</sub>M for this long thin bar, and exactly half as strong at each face, and it passes through the faces without a break. The other field, H, does not: inside the magnet &mu;<sub>0</sub>H is B minus &mu;<sub>0</sub>M, so it jumps by &mu;<sub>0</sub>M at each face and points backwards inside, from the north pole to the south pole. That backward field is the demagnetising field, and it is why a short, fat magnet is weaker inside than a long, thin one. Far from the magnet both fall away as the point dipole, drawn in orange.',
  far:'From far away any magnet looks the same: a point dipole, whose field falls as the inverse cube of the distance and is twice as strong along the axis as on the bisector at the same distance. Its strength is set by one number, the magnetic moment, which for this bar is its magnetisation times its volume. The first correction is the octupole, which fades two powers of the distance faster, so the fractional difference from the dipole falls as one over the distance squared: the straight lines of slope &minus;2 in the lower plot. Both limits are taken numerically in the readout by evaluating the exact field at 2, 4 and 8 m and extrapolating, and both come out at 1 to within a few parts in a billion, while the approach agrees with the octupole coefficients worked out in closed form.',
  needle:'A compass needle is a small magnet on a pivot, and in a field it behaves like a pendulum: the torque pulling it back is proportional to the sine of its angle from the field, so it swings, and friction makes the swings die away. This view releases the needle at an angle and integrates its motion, using PhET&rsquo;s constants for the needle&rsquo;s response to the field and its damping. For small swings the solution is the damped oscillator, drawn in orange; at large angles the needle lingers near the top of its swing and the period grows, exactly as for a pendulum, by the factor given by the complete elliptic integral. The period of small swings is 2&pi;/&radic;(&kappa;|B|), so it halves when the field is four times stronger: timing a swinging magnet is how Gauss first measured the strength of the Earth&rsquo;s field in 1832. The energy of the needle plus the work done against the damping is conserved, and the readout checks it.'
};
