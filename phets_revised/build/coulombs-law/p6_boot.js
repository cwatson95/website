
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
    syncPanel(); dirty=true; refresh();
  }
  TABS.forEach(([k,lab2])=>{ tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2)); });
  /* the scale screen the display controls act on (the lab views only show them) */
  const scrW=()=>st.view==='atomic'?'atomic':'macro';

  const rows={};
  function slider(id,lab2,lo,hi,step2,fmtf,get,set){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:get()});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=get(); val.textContent=fmtf(get()); };
    inp.addEventListener('input',()=>{ set(parseFloat(inp.value)); syncPanel(); dirty=true; refresh(); });
    rows[id]={row:rowEl,sync}; sync(); return rowEl;
  }
  function checkbox(id,lab2,get,set){
    const inp=h('input',{type:'checkbox'}); inp.checked=!!get();
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ if(inp.disabled) return; set(inp.checked); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+id]={row:el,inp,sync:()=>{ inp.checked=!!get(); }};
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

  const gScale=h('div',{class:'grp'},h('h3',null,'which scale'));
  gScale.appendChild(chipRow([{id:'macro',name:'macro scale'},{id:'atomic',name:'atomic scale'}],'scale'));

  const gMac=h('div',{class:'grp'},h('h3',null,'macro charges'));
  gMac.appendChild(slider('mq1','q₁, µC',-Q_MAX,Q_MAX,1,v=>(v>0?'+':'')+fmt(v,0),()=>st.mq1,v=>setCharge(st,'macro',1,v)));
  gMac.appendChild(slider('mq2','q₂, µC',-Q_MAX,Q_MAX,1,v=>(v>0?'+':'')+fmt(v,0),()=>st.mq2,v=>setCharge(st,'macro',2,v)));
  gMac.appendChild(slider('mx1','x₁, cm',-5,5,0.1,v=>fmt(v,1),()=>st.mi1/10,v=>setPosCL(st,'macro',1,v/100)));
  gMac.appendChild(slider('mx2','x₂, cm',-5,5,0.1,v=>fmt(v,1),()=>st.mi2/10,v=>setPosCL(st,'macro',2,v/100)));

  const gAt=h('div',{class:'grp'},h('h3',null,'atomic charges'));
  gAt.appendChild(slider('aq1','q₁, e',-Q_MAX,Q_MAX,1,v=>(v>0?'+':'')+fmt(v,0),()=>st.aq1,v=>setCharge(st,'atomic',1,v)));
  gAt.appendChild(slider('aq2','q₂, e',-Q_MAX,Q_MAX,1,v=>(v>0?'+':'')+fmt(v,0),()=>st.aq2,v=>setCharge(st,'atomic',2,v)));
  gAt.appendChild(slider('ax1','x₁, pm',-50,50,1,v=>fmt(v,0),()=>st.ai1,v=>setPosCL(st,'atomic',1,v*1e-12)));
  gAt.appendChild(slider('ax2','x₂, pm',-50,50,1,v=>fmt(v,0),()=>st.ai2,v=>setPosCL(st,'atomic',2,v*1e-12)));

  const gDisp=h('div',{class:'grp'},h('h3',null,'force values'));
  gDisp.appendChild(h('div',{class:'checks'},
    checkbox('force','force values',()=>st[PRE[scrW()]+'Force'],v=>{ st[PRE[scrW()]+'Force']=v; }),
    checkbox('sci','scientific notation',()=>st[PRE[scrW()]+'Sci'],v=>{ st[PRE[scrW()]+'Sci']=v; })));
  gDisp.appendChild(slider('arrowK','arrow scale',0,ARROW_KMAX,1,k=>sciPlain(arrowStep(k,ARROW_E0[scrW()]),1)+' N/'+TRACKS[scrW()].unit,
    ()=>st[PRE[scrW()]+'ArrowK'],v=>{ st[PRE[scrW()]+'ArrowK']=Math.round(v); }));
  gDisp.appendChild(h('div',{class:'checks'},checkbox('dist','the distance between centres',()=>st.showDist,v=>{ st.showDist=v; })));
  gDisp.appendChild(h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ rulerToQ1(st,scrW()); dirty=true; refresh(); }},'ruler to q₁'),
    h('button',{onclick:()=>{ rulerHomeCL(st,scrW()); dirty=true; refresh(); }},'ruler home')));
  const dispTag=h('div',{class:'tag'}); gDisp.appendChild(dispTag);

  const gReset=h('div',{class:'grp'},h('div',{class:'btnrow'},
    h('button',{onclick:()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v; syncChips(); syncPanel(); dirty=true; refresh(); }},'reset all')));

  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Coulomb&rsquo;s Law (University of Colorado Boulder, '
      +'phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets.'}),
    h('div',{class:'src',html:'k = 1/4&pi;&epsilon;<sub>0</sub>, e, G, m<sub>e</sub>, m<sub>p</sub> and the Bohr radius: CODATA 2022 through scipy.constants. '
      +'PhET&rsquo;s values: radii 6.75 mm and 0.95 pm, the &plusmn;5 cm and &plusmn;50 pm tracks on 1-mm and 1-pm grids, gaps of 1 mm and 0.1 pm, '
      +'charges &plusmn;10 &micro;C and &plusmn;10 e (read from PhET&rsquo;s build 1.0.32). Every number is pinned in selfTest to build/coulombs-law/derive.py.'}));
  [gScale,gMac,gAt,gDisp,gReset,gInfo].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info');

  function syncChips(){
    for(const [cw,list,key] of CHIPROWS) [].forEach.call(cw.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  function syncPanel(){
    const v=st.view, sc=(v==='inv'||v==='prod')?st.scale:v;
    gScale.hidden=!(v==='inv'||v==='prod');
    gMac.hidden=!(sc==='macro'||v==='grav');
    gAt.hidden=!(sc==='atomic'||v==='grav');
    gDisp.hidden=!(v==='macro'||v==='atomic');
    for(const k in rows) rows[k].sync();
    /* PhET greys out scientific notation while the force values are hidden: a
       live control that does nothing is worse than none */
    const on=!!st[PRE[scrW()]+'Force'];
    rows.cb_sci.inp.disabled=!on; rows.cb_sci.row.style.opacity=on?'1':'0.45';
    const T=TRACKS[scrW()];
    dispTag.innerHTML='drag a charge or the ruler on the canvas; the charges snap to '+(T.unit==='cm'?'1 mm':'1 pm')+', the closest centres are '
      +sigf(chargeSteps(T)/T.perM*T.uPerM,3)+' '+T.unit+' apart';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='macro'||st.view==='atomic')?'drag a charge or the ruler · 1–5 switch views':'1–5 switch views';
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
    if(e.key>='1'&&e.key<=String(TABS.length)) setView(TABS[+e.key-1][0]);
  });

  function resize(){
    const r=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
    canvas.width=Math.round(r.width*dpr); canvas.height=Math.round(r.height*dpr);
    canvas.getContext('2d').setTransform(dpr,0,0,dpr,0,0);
    S.W=r.width; S.H=r.height;
  }
  window.addEventListener('resize',()=>{ resize(); dirty=true; refresh(); });

  function frameLoop(){
    const advanced=S.step();
    if(advanced||dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  macro:'Charles-Augustin de Coulomb measured it in 1785 with a torsion balance of his own design: two charged spheres push or pull along '
    +'the line between them with a force proportional to each charge and to the inverse square of the distance between their centres. Like '
    +'charges repel and unlike charges attract &mdash; change a sign with its slider and both arrows turn round together, still equal and '
    +'opposite, because Newton&rsquo;s third law holds for charges at rest. These are PhET&rsquo;s macro-scale charges, spheres 1.35 cm across '
    +'carrying a few microcoulombs. That is a great deal of charge for a ball this size: a microcoulomb alone would hold it at over a million '
    +'volts, far beyond what air can insulate, which is why real demonstrations use nanocoulombs. The model puts each charge at its sphere&rsquo;s '
    +'centre, which is exact for a rigid, uniformly charged sphere; two conducting spheres this close would shift their charge toward or away '
    +'from each other and depart from the formula.',
  atomic:'At the atomic scale the law is the same, with charge counted in units of the elementary charge, e = 1.602176634 &times; 10<sup>&minus;19</sup> C '
    +'(exact since the 2019 redefinition of the SI), and distance in picometres, 10<sup>&minus;12</sup> m. Charge comes only in whole multiples of '
    +'e, so the sliders step by one. The forces look tiny in newtons &mdash; about a micronewton at the defaults &mdash; but they act on particles of '
    +'almost no mass: the default pull on a proton would accelerate it at nearly 10<sup>21</sup> m/s&sup2; (the readout prints it). PhET draws each charge as a 1.9-pm ball, a '
    +'marker for a point charge rather than a picture of an ion (a real ion is about a hundred times larger, a nucleus a thousand times '
    +'smaller). The law between two point charges holds exactly at these distances; what quantum mechanics changes is where the charge in an '
    +'atom sits, not the force between two charges.',
  inv:'Double the distance and the force falls to a quarter, on either scale and for any pair of charges: an inverse-square law is a straight '
    +'line of slope &minus;2 on logarithmic axes, and the readout measures that slope off the model at the live distance. Multiply the force by '
    +'r&sup2; and what remains, |k q&#8321;q&#8322;|, does not depend on distance at all &mdash; the lower-right panel shows it flat against the falling '
    +'curve of an inverse-cube law. Coulomb&rsquo;s torsion balance supported the exponent 2 only roughly; the tight tests are null experiments '
    +'with charged concentric spheres, first Cavendish&rsquo;s and then Maxwell&rsquo;s, because only an exact inverse square leaves the inside of '
    +'a charged shell free of field.',
  prod:'The force depends on the charges only through their product. When q&#8321;q&#8322; is positive &mdash; both charges the same sign &mdash; they '
    +'repel; when it is negative they attract; on either axis one charge is zero and there is no force at all. Its size is proportional to '
    +'|q&#8321;q&#8322;|, so the contours of equal force are hyperbolas, the same in all four quadrants. The lower-left panel holds q&#8321; fixed and '
    +'sweeps q&#8322; through zero: the force on q&#8322; is a straight line through the origin that changes direction as the sign does, and the force '
    +'on q&#8321; is its mirror image. The lower-right panel collapses the whole plane onto one line: every pair of charges with the same product '
    +'feels the same force.',
  grav:'Electricity and gravity are both inverse-square laws, so for any pair of particles their ratio does not depend on the distance. For '
    +'the electron and proton of a hydrogen atom it is k e&sup2;/(G m<sub>e</sub>m<sub>p</sub>) = 2.27 &times; 10<sup>39</sup>: at the Bohr radius the '
    +'electric pull is 8.2 &times; 10<sup>&minus;8</sup> N and the gravitational one 3.6 &times; 10<sup>&minus;47</sup> N. That is why atoms, molecules and '
    +'everything built from them are held together by electric forces, and why gravity only wins for bodies so large that their positive and '
    +'negative charges cancel almost exactly. The lower-left panel turns the comparison round for the macro screen: two masses that pulled as '
    +'hard as its charges would need tens of tonnes each, and squeezed into PhET&rsquo;s 1.35-cm spheres they would have a density of about '
    +'5 &times; 10<sup>10</sup> kg/m&sup3;.',
};
