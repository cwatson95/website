
/* ================================================================== *
 *  selfTest -- headless verification.  The shared suites (t_core,     *
 *  t_lines, t_far, t_rotor) assert the engine against derive.py, the  *
 *  family's Python twin; below them are this page's own model,        *
 *  panels and layout.                                                 *
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
  testFar(T,['magnet']);
  testRotor(T);
  testCaptions(T,withState);

  /* ---------- this page ---------- */
  ok(TABS.length===5&&TABS[0][0]==='bar','five views: PhET’s one screen and four that open it up');
  ok(ST.view==='bar'&&ST.pct===75&&ST.barField&&ST.barCompass&&!ST.barMeter&&!ST.seeInside&&!ST.earth,
     'it opens as PhET does: 75 %, the field shown, the compass out, the meter away');
  close(barMagnet(ST).S,225,0,'75 % of PhET\'s 300 G is 225 G');
  close(magMoment(225),225/G_PER_T/MU0*Math.PI*Math.pow(0.025,2)*0.25,1e-12,'the moment at 225 G is M V');
  close(magMoment(225),8.790,2e-3,'which is about 8.79 A m^2 for this bar');
  withState({pct:0},()=>{ const M=buildModel(); ok(M.src.S===0&&M.atCompass.B===0,'at zero strength there is no field at all'); });
  withState({},()=>{
    const before=meterReading(barMagnet(ST),560,380);
    flipMagnet(ST);
    const after=meterReading(barMagnet(ST),560,380);
    close(after.Bx,-before.Bx,1e-12,'flip polarity reverses B_x at a fixed point');
    close(after.By,-before.By,1e-12,'and B_y');
    close(ST.bar.ang,Math.PI,1e-15,'the magnet is turned through pi');
    ok(LIVE.barRot===null||LIVE.barRot.om!==0,'and the needle is kicked off the unstable equilibrium');
  });
  withState({},()=>{
    const r=rotorFor('barRot',barMagnet(ST),ST.barC), at=meterReading(barMagnet(ST),ST.barC.x,ST.barC.y);
    ok(r.rest&&Math.abs(wrapPi(r.phi-Math.atan2(at.By,at.Bx)))<1e-12,'the needle starts along the field, as PhET\'s does');
    ok(stepLive(1/60)===false,'so a settled page paints nothing at all');
    flipMagnet(ST);
    ok(stepLive(1/60)===true,'after a flip it moves again');
    let n=0; while(n<3000&&stepLive(1/60)) n++;
    const B=meterReading(barMagnet(ST),ST.barC.x,ST.barC.y);
    ok(n<3000,'and it settles again, after '+fmt(n/60,2)+' s');
    ok(Math.abs(wrapPi(LIVE.barRot.phi-Math.atan2(B.By,B.Bx)))<1e-3,'pointing along the reversed field');
  });
  withState({view:'needle'},()=>{ ok(stepLive(1/60)===true,'the needle view runs its own clock'); });
  withState({view:'lines'},()=>{ ok(stepLive(1/60)===false,'the analysis views are still'); });

  /* ---------- panels ---------- */
  const panels=over=>withState(over,()=>{ const M=buildModel(); return readoutHTML(M)+eqbarHTML(M)+tagHTML(M); });
  const CASES=[{},{pct:0},{pct:100,seeInside:true,earth:true,barMeter:true},{barCompass:false},{units:'T',barMeter:true},
    {view:'lines'},{view:'lines',pct:0},{view:'axis'},{view:'axis',axisH:false},{view:'far'},{view:'far',pct:0},
    {view:'needle'},{view:'needle',ndB:0.05,ndRel:179},{view:'needle',ndB:300,ndRel:1,ndDamp:0},{view:'needle',ndDamp:10}];
  for(const over of CASES){ const html=panels(over);
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean for '+JSON.stringify(over).slice(0,48)); }
  { const rd=meterReading({kind:'magnet',x:430,y:333,ang:0,S:225},125,218);
    ok(panels({barMeter:true}).indexOf(fmtField(rd.B,'G'))>=0,'the readout prints the meter\'s own |B| off the model'); }
  ok(panels({view:'far'}).indexOf(fmt(dipoleLimit('magnet',0,'axis').lim,10))>=0,'the far-field readout prints the numerically taken limit');
  ok(panels({view:'axis'}).indexOf(fmt(solAxis(0,MAG_R,MAG_B),6))>=0,'the axis readout prints cos alpha = 0.980581');
  ok(panels({view:'needle',ndB:5}).indexOf(sigf(2*Math.PI/Math.sqrt(KAPPA*5),4))>=0,'and the needle readout its small-swing period');
  ok(panels({units:'T'}).indexOf('× 10^')>=0&&panels({units:'T'}).indexOf(' G')<0,'in tesla the panels carry no gauss');
  { let bad=null;
    for(const pct of [0,35,100]) for(const view of TABS.map(t=>t[0])){ const html=panels({view,pct});
      if(/NaN|undefined|Infinity/.test(html)) bad=view+' '+pct; }
    for(const ndB of [0.05,5,300]) for(const ndRel of [1,90,179]) for(const ndDamp of [0,2,10]){
      const html=panels({view:'needle',ndB,ndRel,ndDamp}); if(/NaN|undefined|Infinity/.test(html)) bad='needle '+ndB+' '+ndRel+' '+ndDamp; }
    ok(!bad,'no combination of the sliders makes a non-finite panel ('+(bad||'none')+')'); }

  /* ---------- layout ---------- */
  const SIZES=[[1400,820],[1240,760],[1100,700],[820,560],[560,380]];
  const CONFIGS=[['bar',{}],['bar strong',{pct:100,barMeter:true,seeInside:true}],['bar earth',{earth:true,pct:20}],
    ['bar zero',{pct:0,barMeter:true}],['bar flipped',{bar:{x:180,y:120,ang:Math.PI},barMeter:true}],
    ['lines',{view:'lines'}],['lines no bound',{view:'lines',bound:false}],['lines zero',{view:'lines',pct:0}],
    ['axis',{view:'axis'}],['axis no H',{view:'axis',axisH:false}],['axis weak',{view:'axis',pct:5}],
    ['far',{view:'far'}],['far zero',{view:'far',pct:0}],
    ['needle',{view:'needle'}],['needle slow',{view:'needle',ndB:0.05,ndRel:179}],
    ['needle fast',{view:'needle',ndB:300,ndRel:20,ndDamp:0}],['needle overdamped',{view:'needle',ndB:0.2,ndDamp:10}]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over] of CONFIGS) for(const [W,H] of SIZES){
    withState(over,()=>{
      const c=makeShotMC(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill'), strokes=c.ops.filter(o=>o.op==='stroke');
      const says=texts.some(t=>/no field|strength 0/.test(t.t));
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
