
/* ================================================================== *
 *  boot — the control panel, the tabs, the handlers, the frame loop   *
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
  TABS.forEach(([k,lab2])=>{
    tabsEl.appendChild(h('button',{class:st.view===k?'active':'',onclick:()=>setView(k)},lab2));
  });

  const rows={};
  function slider(key,lab2,lo,hi,step2,fmtf,onchg){
    const inp=h('input',{type:'range',min:lo,max:hi,step:step2,value:st[key]});
    const val=h('span',{class:'val'});
    const rowEl=h('div',{class:'sliderrow'},h('label',null,lab2),inp,val);
    const sync=()=>{ inp.value=st[key]; val.textContent=fmtf(st[key]); };
    inp.addEventListener('input',()=>{ st[key]=parseFloat(inp.value);
      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows[key]={row:rowEl,sync,inp}; sync(); return rowEl;
  }
  function checkbox(key,lab2,onchg){
    const inp=h('input',{type:'checkbox'}); inp.checked=st[key];
    const el=h('label',null,inp,lab2);
    inp.addEventListener('change',()=>{ st[key]=inp.checked;
      if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });
    rows['cb_'+key]={row:el,sync:()=>{ inp.checked=st[key]; }};
    return el;
  }
  /* a chip row REGISTERS ITSELF, so syncChips never has to find it again by
     matching label text: the DOM stub does not decode entities in innerHTML
     and a real browser does (Known-bad, the drum_head harness). */
  const CHIPROWS=[];
  function chipRow(list,key,onPick){
    const wrapEl=h('div',{class:'chips'});
    list.forEach(o=>{
      wrapEl.appendChild(h('button',{class:'chip'+(st[key]===o.id?' on':''),html:o.name,onclick:()=>{
        const was=st[key]; st[key]=o.id; if(onPick) onPick(o,was);
        syncChips(); syncPanel(); dirty=true; refresh(); }}));
    });
    CHIPROWS.push([wrapEl,list,key]);
    return wrapEl;
  }
  function btn(label,fn){
    return h('button',{onclick:()=>{ fn(); syncChips(); syncPanel(); dirty=true; refresh(); }},label);
  }

  /* ---- the curve ---- */
  const gCurve=h('div',{class:'grp'},h('h3',null,'the curve'));
  const modeChips=chipRow(MODES,'mode');
  gCurve.appendChild(modeChips);
  const wRow=slider('width','shape width w',W_MIN,W_MAX,0.05,v=>fmt(v,2));
  gCurve.appendChild(wRow);
  gCurve.appendChild(slider('height','shape height y',Y_MIN,Y_MAX,0.05,v=>fmt(v,2)));
  gCurve.appendChild(slider('placeX','shape centre x',XMIN,XMAX,0.1,v=>fmt(v,2)));
  gCurve.appendChild(h('div',{class:'btnrow'},
    btn('lay it down',()=>S.place()),
    btn('smooth',()=>doSmooth()),
    btn('undo',()=>doUndo())));
  gCurve.appendChild(h('div',{class:'btnrow'},
    btn('erase',()=>doErase()),
    btn('reset all',()=>resetAll())));
  const curveTag=h('div',{class:'tag'}); gCurve.appendChild(curveTag);

  /* ---- the tools ---- */
  const gTools=h('div',{class:'grp'},h('h3',null,'the tools'));
  const toolChecks=h('div',{class:'checks'},
    checkbox('tangent','tangent'),
    checkbox('area','area under curve'),
    checkbox('refLine','reference line'));
  gTools.appendChild(toolChecks);
  const xTRow=slider('xT','tangent at x',XMIN,XMAX,0.008,v=>fmt(v,3));
  const xARow=slider('xA','area up to x',XMIN,XMAX,0.008,v=>fmt(v,3));
  const xRRow=slider('xR','reference line x',XMIN,XMAX,0.008,v=>fmt(v,3));
  gTools.appendChild(xTRow); gTools.appendChild(xARow); gTools.appendChild(xRRow);
  const toolTag=h('div',{class:'tag'}); gTools.appendChild(toolTag);

  /* ---- what to show ---- */
  const gShow=h('div',{class:'grp'},h('h3',null,'what to show'));
  gShow.appendChild(h('div',{class:'checks'},
    checkbox('grid','grid'),
    checkbox('values','values')));
  const discChips=chipRow(DISCONTS,'discont');
  gShow.appendChild(h('div',{class:'tag',html:'at a discontinuity of the derivative:'}));
  gShow.appendChild(discChips);
  const showTag=h('div',{class:'tag'}); gShow.appendChild(showTag);

  /* ---- notation (PhET's two preferences) ---- */
  const gNot=h('div',{class:'grp'},h('h3',null,'notation'));
  const notChips=chipRow(NOTATIONS,'notation');
  const varChips=chipRow(VARIABLES,'variable');
  gNot.appendChild(notChips);
  gNot.appendChild(h('div',{class:'tag',html:'variable:'}));
  gNot.appendChild(varChips);
  const notTag=h('div',{class:'tag'}); gNot.appendChild(notTag);

  /* ---- predict ---- */
  const gPred=h('div',{class:'grp'},h('h3',null,'predict'));
  gPred.appendChild(h('div',{class:'checks'},
    checkbox('predict','predict f myself'),
    checkbox('showF','show f')));
  const predTag=h('div',{class:'tag'}); gPred.appendChild(predTag);

  /* ---- the reference shape (the analysis views) ---- */
  const gRef=h('div',{class:'grp'},h('h3',null,'the reference shape'));
  const refChips=chipRow(SHAPE_MODES.map(m=>({id:m,name:m})),'refShape',()=>{ st.cornerSel=0; });
  gRef.appendChild(refChips);
  gRef.appendChild(slider('refW','reference width w',W_MIN,W_MAX,0.05,v=>fmt(v,2)));
  gRef.appendChild(slider('refY','reference height y',Y_MIN,Y_MAX,0.05,v=>fmt(v,2)));
  gRef.appendChild(slider('refX','reference centre x',XMIN,XMAX,0.1,v=>fmt(v,2)));
  const cornRow=slider('cornerSel','which corner',0,7,1,v=>String(Math.round(v)+1));
  gRef.appendChild(cornRow);
  const multRow=slider('gridMult','cells shown',0,GRID_MULTS.length-1,1,
                       v=>String(Math.round((NPTS-1)*GRID_MULTS[clamp(Math.round(v),0,GRID_MULTS.length-1)])));
  gRef.appendChild(multRow);
  const refTag=h('div',{class:'tag'}); gRef.appendChild(refTag);

  /* ---- prose ---- */
  const gInfo=h('div',{class:'grp'},h('h3',null,'what you are looking at'),
    h('div',{id:'info'}),
    h('div',{class:'src',html:'Remake of PhET Interactive Simulations&rsquo; Calculus Grapher (University of '
      +'Colorado Boulder, phet.colorado.edu, CC-BY 4.0). New code; no PhET code or assets. PhET&rsquo;s values '
      +'(x from 0 to 10 in 1251 points, TYPICAL_Y = 1, shape width 1&ndash;5 default 2, y from &minus;2 to 2, '
      +'edgeSlopeFactor = 0.4, smoothing &sigma; = 0.05, maxTilt = 25, undo depth 20, the tangent and area '
      +'gauges &plusmn;8) are read out of its build 1.1.1 by build/calculus-grapher/derive.py. Everything '
      +'else is mathematics, re-derived there with numpy and scipy (erf, the incomplete gamma, '
      +'Gauss&ndash;Legendre quadrature) and pinned in selfTest.'}));
  const gPhys=h('div',{class:'grp'},h('h3',null,'the mathematics'),h('div',{id:'phys'}));
  [gCurve,gTools,gShow,gNot,gPred,gRef,gInfo,gPhys].forEach(g=>panel.appendChild(g));
  const infoEl=gInfo.querySelector('#info'), physEl=gPhys.querySelector('#phys');

  function syncChips(){
    for(const [wrapEl,list,key] of CHIPROWS)
      [].forEach.call(wrapEl.children,(b,i)=>b.className='chip'+(list[i].id===st[key]?' on':''));
  }
  /* a row the view ignores is hidden, never left live and inert */
  function syncPanel(){
    const v=st.view, draws=(v==='deriv'||v==='integ'||v==='lab'||v==='ftc');
    gCurve.hidden=!draws;
    wRow.hidden=(SHAPE_MODES.indexOf(st.mode)<0);
    gTools.hidden=!(v==='deriv'||v==='integ'||v==='lab');
    rows.cb_tangent.row.hidden=(v==='integ');
    rows.cb_area.row.hidden=(v==='deriv');
    rows.cb_refLine.row.hidden=false;
    xTRow.hidden=(v==='integ'||!st.tangent);
    xARow.hidden=(v==='deriv'||!st.area);
    xRRow.hidden=!st.refLine;
    gShow.hidden=false;
    discChips.hidden=(v==='integ'||v==='ftc'||v==='grid');
    gNot.hidden=!(draws||v==='corner');
    gPred.hidden=!draws;
    rows.cb_showF.row.hidden=!st.predict;
    gRef.hidden=!(v==='corner'||v==='grid');
    rows.refW.row.hidden=false;
    cornRow.hidden=(v!=='corner');
    multRow.hidden=(v!=='grid');
    for(const k in rows) rows[k].sync();
    curveTag.innerHTML=(SHAPE_MODES.indexOf(st.mode)>=0)
      ? 'drag on the f panel, or set the three numbers and press <b>lay it down</b> '
        +'&mdash; the shape is laid on the curve as it was when the drag began, so a '
        +'drag moves one shape instead of stacking hundreds'
      : (st.mode==='freeform'
         ? 'freeform: drag and the curve follows the pointer; a single click lays a hill of PhET&rsquo;s '
           +'own width '+fmt(FREEFORM_W,2)
         : (st.mode==='tilt'
            ? 'tilt pivots about the left edge and refuses a slope of '+MAX_TILT+' or more (PhET&rsquo;s maxTilt)'
            : 'shift moves the whole curve rigidly, so every slope is unchanged and the integral gains '
              +'&Delta;y &times; x'));
    toolTag.innerHTML='the tangent reads the slope of the cell it stands in; the area tool splits every cell '
      +'at its zero crossing, which is why its net and the integral curve agreeing is a <b>check</b>';
    showTag.innerHTML=st.values?'values are printed where the reference line crosses each curve'
      :'PhET&rsquo;s Grid and Values checkboxes';
    notTag.innerHTML='PhET&rsquo;s Notation and Variable preferences &mdash; Lagrange f&prime;('+st.variable
      +'), Leibniz <i>d</i>f/<i>d</i>'+st.variable;
    predTag.innerHTML=st.predict
      ? 'you are drawing your guess at f; the other panels keep showing the <b>real</b> f&rsquo;s derivative '
        +'and integral, which is the whole exercise'
      : 'PhET&rsquo;s Predict: hide f, sketch what you think it is, then show it';
    refTag.innerHTML=(v==='grid')
      ? 'the ladder runs from '+Math.round((NPTS-1)*GRID_MULTS[0])+' to '
        +Math.round((NPTS-1)*GRID_MULTS[GRID_MULTS.length-1])+' cells; PhET&rsquo;s own grid is '+(NPTS-1)
      : 'these views work on one analytic shape laid on an empty curve, so the closed form to compare '
        +'against is unambiguous';
  }

  function refresh(){
    try{
      const M=S.model();
      roEl.innerHTML=readoutHTML(M);
      eqEl.innerHTML=eqbarHTML(M);
      tagEl.innerHTML=tagHTML(M);
      hintEl.textContent=(st.view==='deriv'||st.view==='integ'||st.view==='lab'||st.view==='ftc')
        ? 'drag on the f panel to shape it · drag a scrubber to move it · 1–6 switch views'
        : '1–6 switch views';
      infoEl.innerHTML=INFO[st.view]||'';
      physEl.innerHTML=DERIV[st.view]||'';
      S.draw();
    }catch(e){ fail(e); }
  }

  canvas.addEventListener('pointerdown',e=>{
    canvas.setPointerCapture(e.pointerId);
    const r=canvas.getBoundingClientRect();
    if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){
      canvas.classList.add('dragging'); dirty=true; syncPanel(); refresh();
    } else if(S.drag) canvas.classList.add('dragging');
  });
  canvas.addEventListener('pointermove',e=>{
    if(!canvas.classList.contains('dragging')&&e.buttons===0) return;
    const r=canvas.getBoundingClientRect();
    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){
      dirty=true; syncPanel(); roEl.innerHTML=readoutHTML(S.model());
    }
  });
  const up=()=>{ canvas.classList.remove('dragging'); if(S.pointer('up',0,0)){ dirty=true; refresh(); } };
  canvas.addEventListener('pointerup',up); canvas.addEventListener('pointercancel',up);

  window.addEventListener('keydown',e=>{
    if(e.key==='s'){ doSmooth(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='u'){ doUndo(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='e'){ doErase(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='r'){ resetAll(); syncChips(); syncPanel(); dirty=true; refresh(); }
    else if(e.key==='ArrowLeft'||e.key==='ArrowRight'){
      e.preventDefault();
      const key=st.tangent&&st.view!=='integ'?'xT':(st.area&&st.view!=='deriv'?'xA':'xR');
      st[key]=clamp(st[key]+(e.key==='ArrowRight'?5*DX:-5*DX),XMIN,XMAX);
      syncPanel(); dirty=true; refresh();
    }
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
    if(dirty){ dirty=false; try{ S.draw(); }catch(e){ fail(e); } }
    requestAnimationFrame(frameLoop);
  }
  resetAll();
  resize(); syncChips(); syncPanel(); refresh(); requestAnimationFrame(frameLoop);
  return S;
}

const INFO={
  deriv:'This is PhET&rsquo;s Derivative screen. Drag anywhere on the upper panel and the curve takes the '
    +'shape you chose &mdash; a hill, a triangle, a pedestal, a parabola, a sinusoid, or freehand &mdash; and '
    +'the lower panel follows instantly, because it is not a separate calculation at all. The curve you see '
    +'is a polyline through 1251 points, so it is <b>straight across every cell</b>, and the slope of a '
    +'straight segment is a division: (f<sub>i+1</sub> &minus; f<sub>i</sub>)/&Delta;x. That is why the '
    +'derivative here is drawn at the cell MIDPOINTS rather than at the points themselves &mdash; that is '
    +'where the quotient actually lives, and putting it there is what makes the whole file exact. Turn on the '
    +'tangent and drag it along: the magenta line is the cell&rsquo;s own segment extended, its slope is the '
    +'number in the gauge, and that number is the height of the lower curve at the same x. Those two things '
    +'agreeing is the single idea the screen exists to teach.',
  integ:'PhET&rsquo;s Integral screen, read the other way round. The lower panel is f with the area under it '
    +'painted in, cyan where f is above the axis and orange where it is below, and the upper panel is the '
    +'running total &mdash; the integral from 0 up to wherever you put the scrubber. Two things are worth '
    +'watching. Where f is negative the total comes <i>down</i>, which is what &ldquo;signed&rdquo; area '
    +'means, and where f crosses zero the total has a turning point, because the integral&rsquo;s slope is f '
    +'itself. The readout gives the positive area and the negative area separately and their difference, and '
    +'then gives the same number read off the integral curve. Those two numbers come from different '
    +'arithmetic: the painted area is counted cell by cell with every cell cut at its own zero crossing, '
    +'while the curve is a running trapezium sum. They agree to the last bit a double can hold.',
  lab:'PhET&rsquo;s Lab screen, with its Advanced screen&rsquo;s preferences folded in: the integral, the '
    +'function, the first derivative and the second, one above the other, with a reference line through all '
    +'four. Read down the column at a corner of f and you can see the whole hierarchy break at once &mdash; f '
    +'is continuous, f&prime; jumps, and f&Prime; has a spike. The spike is the honest part: the second '
    +'derivative of a corner is not a large number, it is a delta function, and what the panel shows is that '
    +'delta smeared over one cell. Refine the grid and the spike gets taller without limit while the area '
    +'under it stays exactly the size of the slope jump. <b>Predict</b> hides f and lets you sketch it while '
    +'the other panels keep showing the real one; the readout scores your guess by its rms distance from f.',
  corner:'A function has a derivative at a point when the difference quotient has the same limit from both '
    +'sides. At a corner both limits exist and they are different, so there is no derivative &mdash; and the '
    +'right thing to draw is not a value but the two limits. The zoom at the bottom magnifies &plusmn;25 cells '
    +'about the corner and lays the two one-sided rays over the curve; on this grid the cells either side of '
    +'a triangle&rsquo;s apex are entirely on one side of it, so the numbers in the readout are <b>exact</b>, '
    +'not estimates. The shapes differ in an instructive way. A triangle has three corners: the apex, and the '
    +'two places where it meets the flat curve. A parabola has only the two outer ones &mdash; its vertex is '
    +'smooth. A sinusoid laid on an empty curve ends in two corners, because PhET drops its taper when there '
    +'is nothing to blend into. And the hill and the pedestal have none at all.',
  ftc:'The fundamental theorem says differentiation and integration undo each other. Most numerical '
    +'implementations satisfy it approximately; this one satisfies it to the last bit, and the reason is a '
    +'choice about <i>where</i> each quantity lives. The derivative belongs to a cell and the integral to a '
    +'node, and with that staggering the integral of the derivative telescopes back to f exactly, while '
    +'differentiating the integral returns the mean of each cell&rsquo;s two ends &mdash; which for a straight '
    +'segment is f at the midpoint, exactly, by the mean value theorem. The top panel has three curves on it '
    +'and looks like one. The middle panel is the residual multiplied by a thousand million million so that '
    +'it can be seen at all. The bottom panel is what PhET&rsquo;s own pair does instead: its derivative sits '
    +'on the nodes and averages the two neighbouring slopes, so differentiating its integral gives the '
    +'[1,2,1]/4 average of f rather than f. That is second order in &Delta;x and entirely defensible &mdash; '
    +'it is simply a different choice, and this view names the difference rather than hiding it.',
  grid:'Everything else in this file is exact, so this view is where the discretisation actually shows. Pick '
    +'a shape, and the top panel draws what the sim stores against the closed form it came from; they are the '
    +'same curve. The middle panel is the difference between the cell derivative and the true derivative, and '
    +'the bottom panel is how that difference behaves as the grid is refined, on log axes, for both '
    +'operators. The straight line of slope &minus;2 is the claim: the midpoint difference carries '
    +'(&Delta;x)&sup2;g&prime;&prime;&prime;/24 and the trapezium carries (&Delta;x)&sup2;[g&prime;(b) &minus; '
    +'g&prime;(a)]/12, so halving &Delta;x quarters both. Two shapes are exceptions and they are the '
    +'interesting ones. A triangle is piecewise linear, so the cell derivative is <b>exact</b>; a parabola is '
    +'quadratic, so a centred difference is exact on it too, and its trapezium error is the '
    +'Euler&ndash;Maclaurin term with nothing left over, because the expansion terminates.',
};

function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV={
  deriv:'<h4>the derivative of a polyline</h4>'
    +EQ(1,'f(x) = f<sub>i</sub> + (x &minus; x<sub>i</sub>) '+FR('f<sub>i+1</sub> &minus; f<sub>i</sub>','&Delta;x')
        +' &nbsp;<span class="rm">on</span>&nbsp; x<sub>i</sub> &le; x &le; x<sub>i+1</sub>')
    +EQ(2,'&rArr; f&prime;(x) = '+FR('f<sub>i+1</sub> &minus; f<sub>i</sub>','&Delta;x')
        +' &nbsp;<span class="rm">everywhere inside the cell</span>')
    +EQ(3,'<span class="rm">against a smooth g:</span> &nbsp; '
        +FR('g(x<sub>i+1</sub>) &minus; g(x<sub>i</sub>)','&Delta;x')
        +' = g&prime;(x<sub>i+&frac12;</sub>) + '+FR('(&Delta;x)&sup2;','24')+' g&prime;&prime;&prime; + &hellip;')
    +'<p>[2] is why this file plots f&prime; at the cell midpoints: that is the only place the quotient is '
    +'the slope rather than an estimate of it. [3] is the price of asking a SMOOTH function for its slope on a '
    +'grid, and it is measured in <i>the grid</i> view rather than assumed &mdash; 4.4&times;10<sup>&minus;5</sup> '
    +'for the default hill, and a factor of four smaller every time &Delta;x is halved.</p>'
    +'<div class="cite">pins: [2] exactly on a triangle (1.1e&minus;13) and a parabola (1.7e&minus;13); [3] '
    +'against scipy for all five shapes, and the measured O(&Delta;x&sup2;) rate &mdash; derive.py</div>',
  integ:'<h4>the integral of a polyline, and the signed area</h4>'
    +EQ(1,'F<sub>i+1</sub> = F<sub>i</sub> + &frac12;(f<sub>i</sub> + f<sub>i+1</sub>)&Delta;x, &nbsp; F<sub>0</sub> = 0')
    +EQ(2,'<span class="rm">exactly the area of the trapezium under a straight segment, so [1] is not a rule '
        +'but an identity</span>')
    +EQ(3,'A<sub>+</sub> &minus; A<sub>&minus;</sub> = &#8747;<sub>0</sub><sup>b</sup> f dx, &nbsp; '
        +'<span class="rm">each cell cut at</span> f = 0')
    +EQ(4,'<span class="rm">against a smooth g:</span> &nbsp; F(b) &minus; &#8747;<sub>a</sub><sup>b</sup> g = '
        +FR('(&Delta;x)&sup2;','12')+'[ g&prime;(b) &minus; g&prime;(a) ] + &hellip;')
    +'<p>[3] is the cross-check the screen exists for: the painted area is accumulated by a different loop, '
    +'with every sign change located exactly inside its cell, and it comes back equal to [1] at 2.8&times;'
    +'10<sup>&minus;16</sup>. [4] terminates for a quadratic, and derive.py checks that: the parabola&rsquo;s '
    +'trapezium error over [5.4, 6.4] is 6.826667&times;10<sup>&minus;6</sup> against a predicted '
    +'6.826667&times;10<sup>&minus;6</sup>, 7.1&times;10<sup>&minus;16</sup> apart.</p>'
    +'<div class="cite">pins: [3] at eight endpoints; [4] as an exact identity on the parabola; the total '
    +'signed area of all five shapes against their closed forms &mdash; derive.py</div>',
  lab:'<h4>the second derivative, and what it is at a corner</h4>'
    +EQ(1,'f&Prime;<sub>i</sub> = '+FR('d<sub>i</sub> &minus; d<sub>i&minus;1</sub>','&Delta;x')+' = '
        +FR('f<sub>i+1</sub> &minus; 2f<sub>i</sub> + f<sub>i&minus;1</sub>','(&Delta;x)&sup2;'))
    +EQ(2,'&Sigma;<sub>i=a</sub><sup>b</sup> f&Prime;<sub>i</sub> &Delta;x = d<sub>b</sub> &minus; '
        +'d<sub>a&minus;1</sub> &nbsp;<span class="rm">(it telescopes &mdash; exactly)</span>')
    +EQ(3,'<span class="rm">so across a corner the spike&rsquo;s AREA is the slope jump, whatever &Delta;x is;'
        +' its HEIGHT is that jump over &Delta;x</span>')
    +'<p>[2] is the honest statement about the spike. The default triangle&rsquo;s apex has one-sided slopes '
    +'&plusmn;1, and the sum in [2] over 81 nodes about it is &minus;2.0000000000000018 &mdash; the jump, to '
    +'rounding. Refining the grid multiplies the height and leaves that number alone, which is what it means '
    +'to say f&Prime; is a delta there rather than a function.</p>'
    +'<div class="cite">pins: [1] against the nodes either side; [2] to 1e&minus;12 over the apex window; the '
    +'spike height as the jump over &Delta;x &mdash; derive.py</div>',
  corner:'<h4>one-sided limits</h4>'
    +EQ(1,'f&prime;(a<sup>&minus;</sup>) = lim<sub>h&rarr;0<sup>&minus;</sup></sub> '
        +FR('f(a+h) &minus; f(a)','h')+', &nbsp; f&prime;(a<sup>+</sup>) = lim<sub>h&rarr;0<sup>+</sup></sub> '
        +FR('f(a+h) &minus; f(a)','h'))
    +EQ(2,'<span class="rm">triangle:</span> &nbsp; &plusmn;'+FR('TYPICAL_Y','w/2')
        +' &nbsp;<span class="rm">at the apex; the junctions drop to 0</span>')
    +EQ(3,'<span class="rm">parabola:</span> &nbsp; &#8723;2&radic;(s|y|) &rarr; 0 '
        +'<span class="rm">at</span> x<sub>0</sub> &plusmn; &radic;(|y|/s), &nbsp; s = TYPICAL_Y(2/w)&sup2;')
    +EQ(4,'<span class="rm">pedestal:</span> &nbsp; exp(&minus;u&#8308;) <span class="rm">has</span> '
        +'1, 0, 0, 0 <span class="rm">at</span> u = 0 &nbsp;&rArr;&nbsp; <span class="rm">C&sup3;, no corner</span>')
    +'<p>[2] is exact on this grid and the sim reads it off the picture rather than computing it: the cell to '
    +'the left of the apex has both its nodes on the rising side, so its slope IS the left-hand limit. [3] is '
    +'not: a parabola&rsquo;s junction falls inside a cell, so the nearest clean cell is about 1.5&Delta;x away '
    +'and reads 1.879 where the limit is 1.893. A corner&rsquo;s position is known to one cell; its limits are '
    +'not.</p>'
    +'<div class="cite">pins: [2] to 1e&minus;13; [3] and the 1.5&Delta;x shortfall; [4] as a measured '
    +'slope-step bound &mdash; derive.py</div>',
  ftc:'<h4>why it is exact, and what PhET&rsquo;s pair does instead</h4>'
    +EQ(1,'&Sigma;<sub>k&lt;i</sub> d<sub>k</sub>&Delta;x = &Sigma;<sub>k&lt;i</sub>(f<sub>k+1</sub> &minus; '
        +'f<sub>k</sub>) = f<sub>i</sub> &minus; f<sub>0</sub>')
    +EQ(2,FR('F<sub>i+1</sub> &minus; F<sub>i</sub>','&Delta;x')+' = &frac12;(f<sub>i</sub> + f<sub>i+1</sub>) '
        +'= f(x<sub>i+&frac12;</sub>) &nbsp;<span class="rm">(a straight segment)</span>')
    +EQ(3,'<span class="rm">PhET:</span> D<sub>c</sub>(I(f))<sub>i</sub> = '
        +FR('f<sub>i&minus;1</sub> + 2f<sub>i</sub> + f<sub>i+1</sub>','4')+' = f<sub>i</sub> + '
        +FR('(&Delta;x)&sup2;','4')+' f&Prime; + &hellip;')
    +'<p>[1] is a telescoping sum, so it is exact in exact arithmetic and carries only rounding in floating '
    +'point. [2] is the mean value theorem with the mean value known: on a straight segment it sits at the '
    +'midpoint. [3] is an identity, checked to 6.2&times;10<sup>&minus;15</sup>, and it is why a node-centred '
    +'derivative cannot invert a trapezium integral exactly &mdash; the smoothing is built into the pairing, '
    +'not into either operator.</p>'
    +'<div class="cite">pins: [1] and [2] to 2e&minus;12 over six random curves; [3] to 2e&minus;12; the '
    +'residual of PhET&rsquo;s pair on the shipped curve &mdash; derive.py</div>',
  grid:'<h4>Euler&ndash;Maclaurin, and the two exceptions</h4>'
    +EQ(1,FR('g(x+&Delta;x) &minus; g(x)','&Delta;x')+' &minus; g&prime;(x + &Delta;x/2) = '
        +FR('(&Delta;x)&sup2;','24')+' g&prime;&prime;&prime;(x) + O((&Delta;x)&#8308;)')
    +EQ(2,'T &minus; &#8747;<sub>a</sub><sup>b</sup> g = '+FR('(&Delta;x)&sup2;','12')
        +'[ g&prime;(b) &minus; g&prime;(a) ] &minus; '+FR('(&Delta;x)&#8308;','720')
        +'[ g&prime;&prime;&prime;(b) &minus; g&prime;&prime;&prime;(a) ] + &hellip;')
    +EQ(3,'<span class="rm">piecewise linear:</span> g&prime;&prime;&prime; &equiv; 0 &rArr; [1] <span class="rm">is exact</span>')
    +EQ(4,'<span class="rm">quadratic:</span> g&prime;&prime;&prime; &equiv; 0 <span class="rm">and [2] TERMINATES</span>')
    +'<p>The rate is the claim. Measured ratios on halving &Delta;x: 4.0000, 4.0000 and 3.9999 for the hill, '
    +'the sinusoid and the pedestal. The pedestal is the worst of the five (1.07&times;10<sup>&minus;3</sup> at '
    +'PhET&rsquo;s grid) because its quartic edge turns over inside 0.4 in x, so g&prime;&prime;&prime; there is '
    +'large &mdash; nothing is wrong with it, it is simply the sharpest smooth shape in the set.</p>'
    +'<div class="cite">pins: [1] and [2] for five shapes at four refinements; [2] as an exact identity on the '
    +'parabola; the triangle&rsquo;s remaining 1.6e&minus;5, which is not quadrature at all but the two '
    +'junction cells &mdash; derive.py</div>',
};
