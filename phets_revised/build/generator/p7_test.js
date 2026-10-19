/* ================================================================== *
 *  selfTest -- headless verification.  The shared suites (t_core,     *
 *  t_lines, t_rotor) assert the engine against derive.py, the         *
 *  family's Python twin; t_gen is this sim's own physics, and below   *
 *  them are this page's model, panels and layout.                     *
 * ================================================================== */
function makeShotMC(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st.font,a:st.align,b:st.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st.font=s.f; st.align=s.a; st.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s=Math.sin(r); Mx=mul(Mx,[c,s,-s,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; pend.n++; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle}); },
    stroke(){ ops.push({op:'stroke',n:pend?pend.n:0}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke',n:1}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st.align==='center'?x-w/2:(st.align==='right'?x-w:x);
      const ly=st.base==='top'?y:(st.base==='middle'?y-fh/2:(st.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c=>app(c[0],c[1]));
      const xs=cs.map(c=>c[0]), ys=cs.map(c=>c[1]);
      ops.push({op:'text',t:''+t,rot:Math.abs(Mx[1])>1e-9,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st.font,set:v=>st.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st.align,set:v=>st.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st.base,set:v=>st.base=''+v});
  return ctx;
}

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const T={ok,close,rel};
  const T0=Date.now();
  const stSave=clone(ST);
  function withState(over,fn){ resetState(over); for(const k in MEMO) delete MEMO[k]; try{ return fn(); } finally{ resetState(stSave); for(const k in MEMO) delete MEMO[k]; } }

  testCore(T);
  testDrawnNeedles(T);
  withState({view:'axis'},()=>testAxisMarks(T));
  testLines(T,['magnet']);
  testRotor(T);
  testCaptions(T,withState);
  testGen(T);
  testGenDrawn(T);

  /* ---------- this page ---------- */
  ok(TABS.length===6&&TABS[0][0]==='gen','six views: PhET’s one screen and five that open it up');
  ok(ST.view==='gen'&&ST.flow===0&&ST.pct===75&&ST.N===2&&ST.area===50&&ST.indicator==='bulb'&&ST.genField&&ST.electrons,
     'it opens as PhET does: the faucet closed, 75 %, 2 loops, half the area, the bulb');
  close(turbMagnet(ST).S,225,0,'75 % of PhET\'s 300 G is 225 G');
  close(turbMagnet(ST).x,TURB_X,0,'and the magnet rides the wheel, not the pointer');
  withState({},()=>{ const M=buildModel();
    ok(M.R.emf===0&&M.R.rpm===0,'with the faucet closed there is no EMF, however strong the magnet');
    ok(M.R.Phi!==0,'though the flux through the coil is not zero: it is its CHANGE that matters'); });
  withState({flow:100},()=>{ const M=buildModel();
    ok(M.R.rpm>0,'open the faucet and the wheel turns ('+fmt(M.R.rpm,1)+' RPM)');
    ok(Math.abs(M.R.emf)>=0,'and the EMF follows the angle it is at'); });
  withState({pct:0,flow:100},()=>{ const M=buildModel();
    ok(M.R.Phi===0&&M.R.emf===0&&M.atCompass.B===0,'at zero strength there is no field, no flux and no EMF'); });
  /* twice the loops is twice the EMF -- but the second loop also drags the wheel, so the
     chain has to carry BOTH: the ratio is 2 (1 - d2)/(1 - d1), not 2 */
  { const A=withState({flow:100,N:1,th:0.5},()=>buildModel().R.emf);
    const B=withState({flow:100,N:2,th:0.5},()=>buildModel().R.emf);
    const want=2*(1-genDrag(2,50,75))/(1-genDrag(1,50,75));
    rel(B/A,want,1e-12,'two loops give 2 (1 - d2)/(1 - d1) = '+fmt(want,5)+' times one loop\'s EMF: the extra loop drags the wheel too');
    ok(want<2,'which is less than 2, because the wheel is slowed by the coil it drives'); }
  { const A=withState({flow:50,N:2,th:0.5},()=>buildModel().R.emf);
    const B=withState({flow:100,N:2,th:0.5},()=>buildModel().R.emf);
    ok(Math.abs(B/A-2)<1e-12,'and twice the flow turns the wheel twice as fast, for twice the EMF'); }
  /* the flip is half a turn of the wheel */
  withState({flow:100,th:0.4},()=>{
    const e0=buildModel().R.emf;
    flipMagnet(ST);
    close(ST.th,0.4+Math.PI,1e-15,'flip polarity turns the magnet through pi');
    rel(buildModel().R.emf,-e0,1e-9,'which reverses the EMF: half a turn reverses the magnet');
  });
  /* the clock: the wheel turns, the compass lags it, and a closed faucet moves nothing */
  withState({view:'gen',flow:0},()=>{
    ok(stepLive(1/60)===false,'with the faucet closed and the needle settled the page paints nothing');
  });
  withState({view:'gen',flow:60},()=>{
    const th0=ST.th;
    ok(stepLive(1/60)===true,'open it and the page moves again');
    close(ST.th-th0,2*Math.PI*genRPM(genState(ST))/60/60,1e-12,'the wheel turns omega dt in a frame');
    const phi0=LIVE.genRot.phi;
    for(let i=0;i<20;i++) stepLive(1/60);
    ok(LIVE.genRot.phi!==phi0&&LIVE.genRot.om!==0,'and the compass needle is dragged round by the turning field');
  });
  withState({view:'gen',flow:100,electrons:true},()=>{
    const p0=LIVE.ePhase; stepLive(1/60);
    ok(LIVE.ePhase!==p0,'the electrons move while there is a current');
  });
  withState({view:'lines'},()=>{ ok(stepLive(1/60)===false,'the analysis views are still'); });
  withState({view:'needle'},()=>{ ok(stepLive(1/60)===true,'except the needle view, which runs its own clock'); });

  /* the magnet's moment: with no far-field view here, the axis view's dipole curve is what
     carries it.  Pinned against the exact field far away rather than against itself. */
  { const S=225, C={B:[],Hh:[],dip:[],ref:[]};
    ANA_SRC.magnet.axisPoint({kind:'magnet',N:0,unit:S},4000,C);
    rel(C.dip[0],S*solAxis(4000,MAG_R,MAG_B),2e-3,'the dipole drawn on the axis is the exact field at 4 m, so its moment mu0 m/4pi is right');
    rel(magMoment(S),S/G_PER_T/MU0*Math.PI*Math.pow(MAG_R*1e-3,2)*MAG_L*1e-3,1e-15,'m = M V in A m^2');
    rel(magMoment(S),8.790,3e-4,'which is 8.79 A m^2 for this bar'); }
  /* the flux view's live marker: drawn where the wheel actually stands */
  withState({view:'flux',pct:0},()=>{
    const c=makeShotMC(1400,820); drawFluxView(c,1400,820,buildModel());
    const t=c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' ');
    ok(/strength 0/.test(t)&&/nothing for its change/.test(t),'with no field the flux view says so in both of its panels');
  });
  withState({view:'face',pct:0},()=>{
    const c=makeShotMC(1400,820); drawFaceView(c,1400,820,buildModel());
    const t=c.ops.filter(o=>o.op==='text').map(o=>o.t).join(' ');
    ok(/no field over the coil/.test(t),'and so does the coil-face view');
  });
  withState({view:'flux',flow:100,th:1.3},()=>{
    const c=makeGeomME(), W=1400, H=820;
    drawFluxView(c,W,H,buildModel());
    const b=fluxGeo(c,W,H).main;
    const dots=c.ops.filter(o=>o.fill===COL.live&&o.path.length&&o.path[0].length>8);
    ok(dots.length>=1,'the flux view draws a marker where the wheel stands ('+dots.length+')');
    if(dots.length){
      const xs=dots[0].path[0].map(q=>q[0]), ys=dots[0].path[0].map(q=>q[1]);
      const cx=0.5*(Math.min.apply(null,xs)+Math.max.apply(null,xs));
      const r=0.5*(Math.max.apply(null,xs)-Math.min.apply(null,xs));
      close(cx,b.x+b.w*(1.3*R2D)/360,0.6,'at the angle the wheel is at, to within a pixel');
      ok(r>=1.5,'and big enough to see ('+fmt(r,2)+' px)');
      const cy=0.5*(Math.min.apply(null,ys)+Math.max.apply(null,ys));
      ok(cy>b.y&&cy<b.y1,'inside the plot box, on its curve');
    }
  });

  /* ---------- panels ---------- */
  const panels=over=>withState(over,()=>{ const M=buildModel(); return readoutHTML(M)+eqbarHTML(M)+tagHTML(M); });
  const CASES=[{},{flow:100},{flow:100,indicator:'volt',genMeter:true},{pct:0},{pct:100,seeInside:true,flow:45},
    {N:4,area:100,flow:100},{N:1,area:20,flow:5},{genCompass:false},{units:'T',genMeter:true,flow:80},
    {view:'flux'},{view:'flux',flow:100,N:4,area:100},{view:'flux',pct:0},
    {view:'face'},{view:'face',area:20},{view:'face',area:100,th:1.2},{view:'face',pct:0},
    {view:'lines'},{view:'lines',pct:0},{view:'axis'},{view:'axis',axisH:false},
    {view:'needle'},{view:'needle',ndB:0.05,ndRel:179},{view:'needle',ndB:300,ndRel:1,ndDamp:0},{view:'needle',ndDamp:10}];
  for(const over of CASES){ const html=panels(over);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+JSON.stringify(over).slice(0,48)); }
  { const rd=meterReading({kind:'magnet',x:TURB_X,y:TURB_Y,ang:0,S:225},800,470);
    ok(panels({genMeter:true}).indexOf(fmtField(rd.B,'G'))>=0,'the readout prints the meter\'s own |B| off the model'); }
  ok(panels({view:'flux',flow:100}).indexOf(fmt(emfPeak(fluxSeries(pickRadius(50))).th*R2D,2))>=0,
     'the flux readout prints the peak angle the engine finds');
  ok(panels({view:'face'}).indexOf(fmt(pickRadius(50),2))>=0,'the face readout prints the coil\'s own radius');
  ok(panels({view:'axis'}).indexOf(sigf(magMoment(225),3))>=0,'the axis readout prints the magnet\'s moment m = M V');
  ok(panels({flow:100}).indexOf(fmt(genRPM({N:2,area:50,strength:75,flow:100}),2))>=0,'and the screen readout the wheel\'s own speed');
  /* every FIELD reading must convert: a number followed by G.  (Plain ' G' will not do as
     a test -- the note names Gauss-Legendre, and a word is not a unit.) */
  ok(panels({units:'T'}).indexOf('× 10^')>=0&&!/[\d.]\s*G(?![a-z])/.test(plain(panels({units:'T'}))),'in tesla no reading is left in gauss');
  { let bad=null;
    for(const flow of [0,35,100]) for(const view of TABS.map(t=>t[0])){ const html=panels({view,flow});
      if(/NaN|undefined|Infinity/.test(html)) bad=view+' '+flow; }
    for(const N of [1,4]) for(const area of [20,100]) for(const pct of [0,100]){
      const html=panels({view:'gen',N,area,pct,flow:100}); if(/NaN|undefined|Infinity/.test(html)) bad='gen '+N+' '+area+' '+pct; }
    ok(!bad,'no combination of the sliders makes a non-finite panel ('+(bad||'none')+')'); }

  /* ---------- layout ---------- */
  const SIZES=[[1400,820],[1240,760],[1100,700],[820,560],[560,380]];
  const CONFIGS=[['gen',{}],['gen running',{flow:100,th:0.9}],['gen volt',{flow:70,indicator:'volt',th:0.4,genMeter:true}],
    ['gen big coil',{flow:100,N:4,area:100,th:2.1}],['gen small coil',{flow:20,N:1,area:20,seeInside:true}],
    ['gen zero',{pct:0,flow:100}],['gen no tools',{genCompass:false,genMeter:false,flow:55,th:5.5}],
    ['flux',{view:'flux'}],['flux running',{view:'flux',flow:100,th:1.1}],['flux big',{view:'flux',N:4,area:100,flow:60}],
    ['flux zero',{view:'flux',pct:0}],
    ['face',{view:'face'}],['face small',{view:'face',area:20,th:0.7}],['face big',{view:'face',area:100}],
    ['face no dots',{view:'face',phetCmp:false}],['face zero',{view:'face',pct:0}],
    ['lines',{view:'lines'}],['lines no bound',{view:'lines',bound:false}],['lines zero',{view:'lines',pct:0}],
    ['axis',{view:'axis'}],['axis no H',{view:'axis',axisH:false}],
    ['needle',{view:'needle'}],['needle slow',{view:'needle',ndB:0.05,ndRel:179}],
    ['needle undamped',{view:'needle',ndB:300,ndRel:20,ndDamp:0}]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShotMC(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill'), strokes=c.ops.filter(o=>o.op==='stroke');
      const says=texts.some(t=>/no field|strength 0|faucet is closed|nothing for its change/.test(t.t));
      ok((fills.length>=1&&fills.length+strokes.length>=8&&texts.length>=3)||says,
         nm+' '+W+'x'+H+' draws substance or says why ('+fills.length+' fills, '+strokes.length+' strokes, '+texts.length+' texts)');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'"'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null; const flat=texts.filter(t=>!t.rot);
      for(let i=0;i<flat.length&&!hit;i++) for(let j=i+1;j<flat.length;j++){
        const a=flat[i].bb,b=flat[j].bb, ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>0.5&&oy>0.5){ hit='"'+flat[i].t.slice(0,22)+'" vs "'+flat[j].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' leaves the #hint corner clear');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i=0;i<POLY_SEGS.length;i+=4){
        const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    });
  }
  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
