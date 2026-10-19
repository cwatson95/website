
/* ================================================================== *
 *  test library (shared by the family): a text-and-fill recorder, the *
 *  layout checker, and the engine's pins.  Reference values labelled  *
 *  (derive) are lines of build/quantum-measurement/refvals.txt, the   *
 *  printed output of derive.py, read in full; (scipy) marks scipy.    *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null, nanPath=false, segs=[], cur=null;
  const fin=(...a)=>{ for(const v of a) if(!isFinite(v)) nanPath=true; };
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); }, rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    /* line segments are kept per path (in canvas pixels) so the layout check
       can see a stroke: the law's marks on the bars */
    beginPath(){ pend=null; segs=[]; cur=null; }, moveTo(x,y){ fin(x,y); cur=app(x,y); },
    lineTo(x,y){ fin(x,y); if(!pend) pend={n:0}; const p=app(x,y); if(cur) segs.push([cur[0],cur[1],p[0],p[1]]); cur=p; }, closePath(){},
    rect(x,y,w,hh){ fin(x,y,w,hh); if(!pend) pend={n:0}; pend.n++; }, arc(x,y,r){ fin(x,y,r); if(!pend) pend={n:0}; pend.n++; cur=null; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1}); }, stroke(){ ops.push({op:'stroke',style:ctx.strokeStyle,lw:ctx.lineWidth,segs:segs.slice()}); }, clip(){},
    fillRect(x,y,w,hh){ fin(x,y,w,hh); ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){ fin(x,y);
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
    nan(){ return nanPath; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>{ _fill=''+v; if(/NaN|undefined/.test(_fill)) nanPath=true; }});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}
/* a negative zero on screen: toFixed prints cos 90 deg = -6e-17 as "-0.000"
   (the photon view's "expected" at 45 deg, found in the capture).  A minus
   glued to a zero that no other digit follows, and not a subtraction (no digit,
   dot or letter before it). */
const NEGZERO_RE=/(^|[^\d.\w])[-−]0(\.0+)?(?![\d.])/;
function negZeroIn(s){ const p=plain(s), m=NEGZERO_RE.exec(p); return m?'"'+p.slice(Math.max(0,m.index-14),m.index+m[0].length+3)+'"':null; }
/* one drawing, every layout rule: no throw, substance, clean text (no entity,
   tag, NaN, negative zero), nothing off the canvas, nothing in the #hint's corner (the HTML
   hint is 11px at bottom:11px, so it owns y > H - 27 on the left), no two
   texts overlapping, no data curve through a legend, no non-finite geometry */
function layoutCheck(T,name,draw,W,H,minFills){
  const c=makeShot(W,H); let err=null;
  try{ draw(c,W,H); }catch(e){ err=e; }
  T.ok(!err,name+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
  if(err) return null;
  const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
  T.ok(fills.length>=minFills&&texts.length>=1,name+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+')');
  T.ok(!c.nan(),name+' '+W+'x'+H+' no non-finite coordinate or colour');
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  let bad=null;
  for(const t of texts){
    if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
    if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
    if(NEGZERO_RE.test(t.t)){ bad='negative zero: "'+t.t.slice(0,48)+'"'; break; }
    if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
  T.ok(!bad,name+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
  const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
  T.ok(!inHint.length,name+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
  let hit=null;
  for(let i=0;i<texts.length&&!hit;i++) for(let j=i+1;j<texts.length;j++){
    const a=texts[i].bb,b=texts[j].bb, ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
    if(ox>0.5&&oy>0.5){ hit='"'+texts[i].t.slice(0,22)+'" vs "'+texts[j].t.slice(0,22)+'"'; break; } }
  T.ok(!hit,name+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
  /* no text on a law mark (a short horizontal orange stroke, 2 px or wider:
     the expected value on a bar).  A label set above its bar alone sat on the
     0.5 mark when the bar stopped just short of it (28.1/s, looked at). */
  let onMark=null;
  { const marks=[];
    for(const o of c.ops) if(o.op==='stroke'&&o.style===COL.ref&&o.lw>=2) for(const s of o.segs) if(Math.abs(s[1]-s[3])<0.5&&Math.abs(s[2]-s[0])<=90) marks.push(s);
    for(const t of texts){ for(const s of marks){ const y=(s[1]+s[3])/2, xa=Math.min(s[0],s[2]), xb=Math.max(s[0],s[2]);
        if(t.bb[0]<xb-0.5&&t.bb[2]>xa+0.5&&t.bb[1]<y+1.1&&t.bb[3]>y-1.1){ onMark='"'+t.t.slice(0,20)+'" on the mark at y '+fmt(y,0); break; } }
      if(onMark) break; } }
  T.ok(!onMark,name+' '+W+'x'+H+' no text on a law mark ('+(onMark||'ok')+')');
  let leg=null;
  for(const r of LEGEND_RECTS) for(let i=0;i<POLY_SEGS.length;i+=4){
    const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
    if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
    leg='a curve crosses a legend'; break; }
  T.ok(!leg,name+' '+W+'x'+H+' legend clear');
  return c;
}
/* the engine's pins: the PRNG, the binomial, the coins */
function engineTests(T){
  const {ok,eq,close,rel}=T;
  /* the shared-helper fixes cannot rot */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(mix('#070b18',mix('#b8ec4c','#cd35c4',0.5),1)!=='rgb(0,0,0)','mix() output is a legal mix() input (not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  eq(tickFmt([0,0.25,0.5])(0.25),'0.25','tick labels follow the spacing (0.25 needs two decimals)'); eq(tickFmt([0,2,4])(4),'4','and 2 needs none');
  close(90*DEG,Math.PI/2,1e-15,'DEG converts degrees INTO radians: 90 DEG = pi/2 (Known-bad: which way a unit constant converts)');
  ok(NEGZERO_RE.test('(expected -0.000)')&&NEGZERO_RE.test('−0')&&NEGZERO_RE.test('x = −0.00 s')&&!!negZeroIn('P = &minus;0.000'),'the negative-zero rule catches -0.000, −0, −0.00 and &minus;0.000');
  ok(!NEGZERO_RE.test('-0.5')&&!NEGZERO_RE.test('−0.05')&&!NEGZERO_RE.test('1−0.000')&&!NEGZERO_RE.test('1e-05')&&!NEGZERO_RE.test('-0.0001')&&!NEGZERO_RE.test('0.000'),'and passes -0.5, −0.05, a subtraction 1−0.000, 1e-05, -0.0001 and 0.000');
  eq(fmt(-Math.cos(Math.PI/2),3),'-0.000','the trap: -cos 90 deg is -6e-17 in floating point and toFixed prints it -0.000');
  eq(fmt0(-Math.cos(Math.PI/2),3),'0.000','fmt0 prints it 0.000');
  eq(fmt0(-0.25,2),'-0.25','and keeps a real sign'); eq(fmt0(-0.0004,0),'0','and a negative that rounds to zero at any precision');
  /* a bar's value against the law's mark (box y 100..300) */
  { const b=box(0,100,100,200), at=(yt,ym)=>barValY(yt,ym,b);
    ok(at(206,200).y===191&&!at(206,200).inside,'a 0.47 bar under the 0.5 mark: its value goes above the MARK, y 191 (it sat on the mark, looked at)');
    ok(at(194,200).y===185&&at(206,undefined).y===197,'a 0.53 bar over the mark, and a bar with no mark: 9 px above the bar');
    ok(at(100,150).y===110&&at(100,150).inside,'a full bar: inside it at the top, dark');
    ok(at(100,106).y===116&&at(100,106).inside,'a full bar with the mark 6 px down: inside, under the mark');
    ok(at(280,110).y===271,'a short bar under a high mark: just above the bar');
    let worst=Infinity, outside=0;
    for(const hb of [200,80,50]){ const bb=box(0,100,100,hb);
      for(let i=0;i<=100;i++) for(let j=0;j<=20;j++){ const yt=bb.y1-hb*i/100, ym=bb.y1-hb*j/20, p=barValY(yt,ym,bb);
        worst=Math.min(worst,Math.abs(p.y-ym)); if(p.y<bb.y+8||p.y>bb.y1-6||(p.inside&&p.y<yt+6)) outside++; } }
    ok(worst>=BAR_CLEAR&&outside===0,'every bar height x every mark (3 boxes, 6363 pairs): the value clears the mark by '+fmt(worst,1)+' px (>= '+BAR_CLEAR+') and stays in its box ('+outside+' outside)');
    let worstF=Infinity, outF=0;
    for(const hb of [200,80,50]){ const bb=box(0,100,100,hb);
      for(let i=0;i<=200;i++){ const p=i/200, ms=[py(bb,p,0,1),py(bb,1-p,0,1)], y=freeY(bb,ms);
        worstF=Math.min(worstF,Math.abs(y-ms[0]),Math.abs(y-ms[1])); if(y<bb.y+8||y>bb.y1-8) outF++; } }
    ok(worstF>=BAR_CLEAR&&outF===0,'the empty-box note clears both marks p and 1-p for every p (3 boxes, 603 cases) by '+fmt(worstF,1)+' px and stays in its box ('+outF+' outside)');
    ok(freeY(b,[py(b,0.5,0,1)])===112&&freeY(b,[py(b,0.97,0,1),py(b,0.03,0,1)])===200,'the note: at the top (y 112) unless a mark is there, then the middle (y 200)'); }
  { const F=[]; layoutCheck({ok:(c,msg)=>{ if(!c) F.push(msg); }},'probe',(ctx,W,H)=>{ LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
      ctx.fillStyle='#fff'; ctx.fillRect(10,10,20,20);
      ctx.beginPath(); ctx.moveTo(40,100); ctx.lineTo(90,100); ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
      ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText('28.1/s',65,97); },400,300,1);
    ok(F.length===1&&/law mark/.test(F[0]),'the layout check flags a value label on a law mark, and only that ('+F.join('; ')+')'); }
  /* ---- the PRNG, bit for bit ---- */
  for(const [seed,want] of [[1,[0.6270739405881613,0.002735721180215478,0.5274470399599522,0.9810509674716741,0.9683778982143849]],
      [42,[0.6011037519201636,0.44829055899754167,0.8524657934904099,0.6697340414393693,0.17481389874592423]],
      [20260918,[0.2512540686875582,0.11133433040231466,0.9283873115200549,0.4453971297480166,0.5996743175201118]],
      [2147483653,[0.5801103678531945,0.08632027637213469,0.9113832253497094,0.7611181102693081,0.923633924452588]]]){
    const R=rngMake(seed), got=[]; for(let i=0;i<5;i++) got.push(rngNext(R));
    ok(got.every((v,i)=>v===want[i]),'mulberry32 seed '+seed+': the first five draws, bit for bit (derive)');
  }
  { const R=rngMake(7); let v; for(let i=0;i<1000;i++) v=rngNext(R); eq(v,0.5222152776550502,'seed 7: the 1000th draw (derive)'); }
  { const R=rngMake(3); let s=0, mn=1, mx=0; for(let i=0;i<100000;i++){ const u=rngNext(R); s+=u; if(u<mn) mn=u; if(u>mx) mx=u; }
    rel(s/100000,0.5008785905108624,1e-12,'seed 3: the mean of 100 000 draws (derive)'); ok(Math.abs(s/100000-0.5)<4*0.0009128709291752768,'and within 4 sigma of 1/2 (sd sqrt(1/12/n) = 0.000913, derive)');
    eq(mn,1.2770527973771095e-05,'its smallest draw (derive)'); eq(mx,0.9999905922450125,'its largest, below 1 (derive)'); }
  { const a=rngMake(5), b={s:a.s}; rngNext(a); ok(b.s!==a.s,'the state is plain data: a copy does not advance with the original'); }
  /* ---- ln n! and the binomial ---- */
  for(const [n,lg] of [[5,4.787491742782047],[20,42.335616460753485],[30,74.65823634883016],[31,78.0922235533153],[100,363.73937555556347],[1000,5912.128178488163],[10000,82108.92783681436]])
    rel(lnFact(n),lg,2e-15,'ln '+n+'! against math.lgamma (derive)');
  { /* both branches across the join at 30: the table and the engine's own Stirling series (not a re-typed copy) */
    rel(lnFactStirling(30),lnFact(30),2e-15,'at the join the Stirling series and the summed-log table agree (both branches pinned)');
    rel(lnFactStirling(25),LNF[25],2e-15,'and below it, where the table rules');
    let s=0; for(let i=1;i<=31;i++) s+=Math.log(i); rel(lnFact(31),s,2e-15,'ln 31! from Stirling = the brute-force sum of logs'); }
  for(const [N,k,p,want] of [[10,3,0.3,0.2668279319999998],[100,50,0.5,0.07958923738717871],[10000,5000,0.5,0.007978646139382161],[10000,3500,0.35,0.008363866192253181],
      [100,0,0.05,0.005920529220334024],[100,100,0.95,0.0059205292203339975],[10,10,0.5,0.0009765625],[1000,312,0.3,0.019369138407836956]])
    rel(binomPmf(N,k,p),want,1e-10,'binomial pmf('+k+'; '+N+', '+p+') against scipy (scipy)');
  { let s=0; for(let k=0;k<=10000;k++) s+=binomPmf(10000,k,0.35); close(s,1,1e-9,'the N = 10 000 pmf sums to 1 (derive: 1 + 2.5e-12)'); }
  { const C=(n,k)=>{ let c=1; for(let i=1;i<=k;i++) c=c*(n-k+i)/i; return c; };
    let w=0; for(let k=0;k<=10;k++) w=Math.max(w,Math.abs(binomPmf(10,k,0.3)-C(10,k)*Math.pow(0.3,k)*Math.pow(0.7,10-k)));
    ok(w<1e-15,'the pmf at N = 10 equals the direct C(n,k) p^k q^(n-k) to '+w.toExponential(1)+' (brute force)'); }
  eq(binomPmf(5,-1,0.4),0,'pmf outside 0..N is 0'); eq(binomPmf(7,0,0),1,'p = 0 puts everything on k = 0'); eq(binomPmf(7,7,1),1,'p = 1 on k = N');
  rel(binomSD(10000,0.35),47.69696007084728,1e-15,'sd of 10 000 coins at 0.35 (derive)');
  /* ---- the coins: the state machine through the SAME code the view runs ---- */
  { const sc=makeCoinScene('classical',20260918); sc.p=0.3; sceneStart(sc);
    eq(sc.single.state,'revealed','classical coins arrive showing the prepared face (PhET)'); eq(sc.single.vals[0],1,'heads, the prepared face');
    const s0=sc.R.s; let first='';
    for(let i=0;i<10000;i++){ coinPrepare(sc,sc.single,false); coinStep(sc,sc.single,0.5); coinStep(sc,sc.single,0.5); coinReveal(sc,sc.single); if(i<20) first+=sc.single.vals[0]; }
    eq(first,'11000110000100000000','one coin flipped: its first 20 faces, bit for bit (derive)');
    eq(sc.single.nUp,3011,'one coin flipped 10 000 times at p = 0.3: 3011 heads (derive)');
    ok(Math.abs(3011-3000)<4*45.8257569495584,'within 4 sigma of Np = 3000 (sd 45.8, derive)');
    eq(sc.single.nObs,10000,'and every flip was revealed once'); eq(sc.single.hist.length,HIST_KEEP,'the strip keeps the last '+HIST_KEEP);
    ok(s0!==sc.R.s,'the flips consumed the stream'); }
  { const sc=makeCoinScene('classical',11); sc.p=0.35; setCoinCount(sc,10000); eq(sc.set.n,10000,'the set takes 10 000 coins while preparing');
    sceneStart(sc); eq(sc.set.kUp,10000,'all heads on arrival'); coinPrepare(sc,sc.set,false);
    eq(sc.set.state,'preparing','a flip is under way'); coinStep(sc,sc.set,0.999); eq(sc.set.state,'preparing','still flipping at 0.999 s (PhET flips for 1 s)');
    coinStep(sc,sc.set,0.002); eq(sc.set.state,'hidden','after 1 s the faces exist, under the cup');
    const s1=sc.R.s, k=sc.set.kUp; coinReveal(sc,sc.set); eq(sc.R.s,s1,'revealing a classical coin draws NOTHING: the face was already there');
    eq(sc.set.kUp,k,'and shows the face it had'); eq(sc.set.kUp,3490,'10 000 coins at p = 0.35: 3490 heads (derive)');
    ok(Math.abs(3490-3500)<4*47.69696007084728,'within 4 sigma of Np'); coinHide(sc,sc.set); coinReveal(sc,sc.set); eq(sc.set.kUp,3490,'hide and reveal again: the same faces');
    setCoinCount(sc,10); eq(sc.set.n,10000,'but not once the coins are being measured (PhET)'); }
  { const sc=makeCoinScene('classical',3); setCoinCount(sc,10); sceneStart(sc); coinPrepare(sc,sc.set,true); coinStep(sc,sc.set,1);
    eq(sc.set.state,'revealed','flip and reveal ends revealed'); eq(Array.from(sc.set.vals.slice(0,10)).join(''),'0111011110','ten coins at p = 0.5: the faces (derive)'); }
  { const sc=makeCoinScene('quantum',99); sc.p=0.3; sceneStart(sc);
    eq(sc.single.state,'ready','a quantum coin arrives READY: no face exists (PhET)'); const s0=sc.R.s;
    coinHide(sc,sc.single); eq(sc.single.state,'ready','there is nothing to hide before it is observed'); eq(sc.R.s,s0,'and nothing was drawn');
    coinReveal(sc,sc.single); ok(sc.R.s!==s0,'observing it draws: the collapse'); const v=sc.single.vals[0], s1=sc.R.s;
    coinHide(sc,sc.single); coinReveal(sc,sc.single); eq(sc.single.vals[0],v,'hidden and observed again, it shows the same face'); eq(sc.R.s,s1,'without a new draw');
    coinPrepare(sc,sc.single,false); coinStep(sc,sc.single,1); eq(sc.single.state,'ready','reprepared: ready again, faceless');
    sc.p=1; for(let i=0;i<200;i++){ coinPrepare(sc,sc.single,true); coinStep(sc,sc.single,1); }
    eq(sc.single.hist.slice(-HIST_KEEP).join(''),'1'.repeat(HIST_KEEP),'P(up) = |alpha|^2 = 1: always up');
    sc.p=0; for(let i=0;i<60;i++){ coinPrepare(sc,sc.single,true); coinStep(sc,sc.single,1); } eq(sc.single.hist.join(''),'0'.repeat(HIST_KEEP),'= 0: always down');
    sc.p=0.3; setCoinCount(sc,10000); }
  { const sc=makeCoinScene('quantum',11); sc.p=0.35; sceneNewCoin(sc); setCoinCount(sc,10000); sceneStart(sc); coinReveal(sc,sc.set);
    eq(sc.set.kUp,3490,'a quantum set observed from the same seed collapses to the same faces: the Born rule draws u < |alpha|^2 exactly as a bias does (derive)'); }
  eq(quantumInit(1),'up','bias 1 is the basis state up'); eq(quantumInit(0),'down','0 is down'); eq(quantumInit(0.5),'superposition','between, a superposition');
  eq(quantumInit(0.999),'superposition','and ANY bias short of 1 is a superposition (the contract, off the 0.05 grid)'); eq(quantumInit(0.001),'superposition','or above 0');
  close(snapBias(0.33),0.35,1e-15,'the bias snaps to 0.05 (PhET)'); close(snapBias(0.31),0.3,1e-15,'both ways');
  eq(snapBias(0.33),0.35,'and lands EXACTLY on the double nearest 0.35 (k/20, not k x 0.05 = 0.35000000000000003)');
  { /* the collapse: after a measurement the state IS +n or -n, exactly (a sim
       that only ever measures once cannot see this, so it is pinned here) */
    const R=rngMake(1); let nUp=0, nDn=0, bad=0;
    for(let i=0;i<60;i++){ const n=[Math.sin(i),0,Math.cos(i)], m=measureAlong(R,[0.6,0,0.8],n), s=m.up?1:-1;
      if(m.up) nUp++; else nDn++; if(!(m.r[0]===s*n[0]&&m.r[1]===s*n[1]&&m.r[2]===s*n[2])) bad++; }
    ok(bad===0&&nUp>5&&nDn>5,'measureAlong leaves the state at +n on up and -n on down, exactly ('+nUp+' up, '+nDn+' down)'); }
  { const sc=makeCoinScene('classical',1); sc.startsHidden=true; sceneStart(sc); eq(sc.single.state,'hidden','with "classical coins start hidden" they arrive under the cup (PhET preference)'); }
  { const sc=makeCoinScene('classical',1); sc.init='tails'; sceneStart(sc); eq(sc.set.kUp,0,'prepared tails, they arrive tails'); sceneNewCoin(sc); ok(sc.preparing,'new coin returns to preparing'); }
  { const sc=makeCoinScene('classical',5); sc.p=0.5; setCoinCount(sc,100); sceneStart(sc); coinPrepare(sc,sc.set,true); coinStep(sc,sc.set,1);
    const m=coinsModel(sc); close(m.z,(sc.set.kUp-50)/5,1e-12,'the set z-score is (k - Np)/sqrt(Np(1-p)) off the model'); ok(m.setShown,'and it is shown only when revealed'); }
  /* ---- M sets of N coins ---- */
  { const r=repeatsRun(5,100,0.5,2000);
    eq(r.mean,49.9645,'2000 sets of 100 at 0.5: the sample mean (derive)'); rel(r.v,24.08728339169585,1e-12,'the sample variance (derive)');
    rel(r.chi,20.355592512456422,1e-10,'the binned chi-square (derive)'); eq(r.dof,28,'on 28 dof (derive)');
    ok(r.chi<56.89228539335361,'below the 99.9 % point, 56.89 (scipy)');
    ok(Math.abs(r.mean-50)<4*0.11180339887498948,'the mean within 4 sd of the mean, 4 x 0.112 (derive)');
    ok(Math.abs(r.v-25)<4*0.7866066361276137,'the variance within 4 sd of Npq, from the fourth moment (derive)');
    eq(Array.from(r.ks.slice(0,10)).join(','),'49,55,51,51,49,58,56,49,55,55','the first ten sets (derive)'); eq(r.obs[50],159,'159 sets of exactly 50 (derive)'); }
  for(const [seed,N,p,M,mean,v,chi,dof,q] of [[71,100,0.3,1000,29.951,22.703302302302305,34.07443399161474,23,49.72823246643149],
      [72,10000,0.5,200,4997.815,2918.975653266332,36.41152780730935,34,65.24721746094244],[73,10,0.65,3000,6.498333333333333,2.299430365677448,4.22415254284819,8,26.12448155837614]]){
    const r=repeatsRun(seed,N,p,M), tag=M+' sets of '+N+' at '+p+': ';
    rel(r.mean,mean,1e-13,tag+'mean (derive)'); rel(r.v,v,1e-11,tag+'variance (derive)'); rel(r.chi,chi,1e-9,tag+'chi-square (derive)'); eq(r.dof,dof,tag+'dof (derive)');
    ok(r.chi<q,tag+'chi-square below the 99.9 % point (scipy)'); ok(Math.abs(r.mean-N*p)<4*Math.sqrt(N*p*(1-p)/M),tag+'mean within 4 sigma/sqrt(M)');
    rel(chi2Quantile(dof,Z999),q,dof>=20?1e-2:1.5e-2,tag+'Wilson-Hilferty quantile within '+(dof>=20?'1':'1.5')+' % of scipy (measured)');
  }
  rel(Z999,3.090232306167813,1e-15,'the normal 99.9 % point (scipy)');
  eq(binEffM(10000,5000),200,'N = 10 000 caps M at 200 (2e6 draws)'); eq(binEffM(100,1000),1000,'N = 100 does not');
}
