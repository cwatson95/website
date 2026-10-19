
/* ================================================================== *
 *  the views: PhET's five screens (the speaker, the bench, two        *
 *  speakers, the wall, thin air) and one analysis view of its own     *
 * ================================================================== */
function boxGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,boxCaption(M,true),boxCaption(M,false),capW,top+220);
  const avail=fit.capY-18-top;
  /* the air view always gets a panel under the box: with the row graph off it carries the
     point of that screen — the speed against the density — which is the one thing the
     picture itself cannot show */
  const wantG=ST.graph||M.view==='air', wantT=ST.listener&&!narrow;
  let gH=wantG?Math.max(70,Math.min(140,Math.round(avail*0.22))):0;
  const gGap=44;
  const below=()=>Math.max(gH?gH+gGap+38:0, SPK_H/2+14+BTN_R+16);
  if(gH&&avail-below()<170) gH=0;
  const left=SPK_W+22;
  const rightNeed=(wantT?(narrow?0:210):0);
  const side=Math.max(110,Math.floor(Math.min(avail-below(), W-left-30-rightNeed, narrow?W:W*0.62)));
  const sq=box(left,top,side,side);
  const G={sq,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,narrow};
  if(wantG&&gH) G.gb=box(sq.x,sq.y1+gGap,sq.w,gH);
  G.graphDropped=wantG&&!gH;
  /* the listener's trace goes below the floating readout, which the audit takes to
     reach y = 470: its TITLE sits 24 px above the panel, so the panel starts at 502 */
  if(wantT){
    const x0=Math.max(sq.x1+60,sq.x1+40), y0=502, y1=fit.capY-44;
    if(W-24-x0>=160&&y1-y0>=70) G.tb=box(x0,y0,W-24-x0,y1-y0);
  }
  return G;
}
function boxCaption(M,full){
  const base='PhET’s wave area: '+fmt(AIR.W,0)+' m across, '+LAT.VIS+' lattice cells of '
    +sigf(M.dx*100,3)+' cm; white is a compression, black a rarefaction, and ±'+fmt(U_FULL,1)
    +' in lattice units is full contrast.';
  if(!full) return base;
  let s=base+' One hard source drives the cell in front of the speaker at 1.2 × the amplitude (PhET’s value); the waves leave through the absorbing edge 20 cells beyond the frame.';
  if(!M.active) s+=(ST.wave==='pulse'?' No pulse is running — press the button to fire one.':' The speaker is off — press its button. The sound already made carries on without it.');
  if(M.R.A===0) s+=' The amplitude is zero: the speaker is running and moving nothing.';
  if(ST.look!=='waves') s+=' The air parcels are pushed along ∇p (ξ = ∇p/ρω², exaggerated so that a full-contrast wave moves one '+fmt(PARC_PUSH,2)+' of the parcel spacing): they crowd where the pressure is high and never travel with the wave, and the cyan one is there to be watched jiggling in place.';
  if(M.view==='two') s+=' The two speakers are the same lattice field read at two rows, which is exact because the equation is linear. Orange: the quiet hyperbolae |r₁ − r₂| = (m + ½)λ, and dotted, the far-field asymptote of the outermost one, at d sinθ = (m + ½)λ.';
  if(M.view==='wall') s+=' Nothing is drawn behind the wall. Orange marks the speaker’s mirror image, whose sound IS the reflected sound; green is the ray that reaches the listener off the wall, with the two angles printed at the bounce.';
  if(M.view==='air') s+=' The air density scales the drive, as PhET’s pressure does; the sound already in the box keeps going, and only new sound is quieter. The panel below is the point of this screen: the wavefronts keep their spacing however thin the air gets, because c = √(γp/ρ) and p and ρ fall together.';
  if(M.view==='measure') s+=' The ruler is PhET’s, 5 m long and rigid; drag it across the crests. The stopwatch runs in the sim’s own slowed time, which is '+fmt(1/AIR.phetTimeScale,0)+' × slower than real.';
  return s;
}
/* the quiet hyperbolae of two sources, clipped to the box by polyline() */
function drawNodes(ctx,W,H,sq,M){
  const T=M.two, lam=M.lam;
  if(!T||!T.orders.length) return;
  for(const m of T.orders){
    for(const sgn of [1,-1]){
      const xs=[], ys=[];
      for(let q=0;q<=90;q++){
        const x=AIR.W*q/90-T.xs;
        if(x<0) continue;
        const y=nodeY(m,lam,T.d,x);
        if(!isFinite(y)) continue;
        xs.push(T.xs+x); ys.push(T.ym+sgn*y);
      }
      polyline(ctx,box(sq.x,sq.y,sq.w,sq.h),xs,ys,0,AIR.W,AIR.W,0,rgba(COL.ref,0.85),1.3);
    }
  }
  /* ONE asymptote pair, for the widest branch: drawn for every order they are
     indistinguishable from the hyperbolae they belong to and the picture is a fan */
  const mL=T.orders[T.orders.length-1], thL=nodeFarAngle(mL,lam,T.d);
  if(isFinite(thL)){
    const a=(mL+0.5)*lam/2, c=T.d/2, sl=a/Math.sqrt(c*c-a*a);
    for(const sgn of [1,-1])
      polyline(ctx,box(sq.x,sq.y,sq.w,sq.h),[T.xs,AIR.W],[T.ym,T.ym+sgn*sl*(AIR.W-T.xs)],
               0,AIR.W,AIR.W,0,rgba(COL.ref,0.45),1.1,[4,4]);
    /* label it three quarters of the way along the part that is IN the box: the widest
       asymptote leaves through the floor long before it reaches the right-hand edge */
    const xEnd=Math.min(AIR.W,T.xs+(AIR.W*0.96-T.ym)/sl);
    const xL=T.xs+0.75*(xEnd-T.xs), yL=T.ym+sl*(xL-T.xs);
    if(xL>T.xs+0.6&&yL<AIR.W*0.96)
      labOver(ctx,W,H,mx(sq,xL),my(sq,yL)+11,'d sinθ = '+sigf(mL+0.5,2)+'λ, θ = '+sigf(thL/DEG,3)+'°',
              COL.ref,'center');
  }
  const m0=T.orders[0];
  if(m0!==undefined){
    const y=nodeY(m0,lam,T.d,AIR.W*0.62-T.xs);
    if(isFinite(y)&&T.ym+y<AIR.W*0.95)
      labOver(ctx,W,H,mx(sq,AIR.W*0.62),my(sq,T.ym+y)-9,'|r₁ − r₂| = ½λ',COL.ref,'center');
  }
}
function drawBoxView(ctx,W,H,M){
  const G=boxGeo(ctx,W,H,M), sq=G.sq;
  if(ST.ruler) LABELS.push(rulerRect(sq));          /* reserved before any overlay label */
  if(ST.look!=='particles') drawField(ctx,sq,M);
  else { ctx.fillStyle=COL.air0; ctx.fillRect(sq.x,sq.y,sq.w,sq.h);
         if(M.g.nfront!==LAT.VIS*LAT.VIS){ /* the wall's shadow still reads as dead air */ } }
  if(M.parcels) drawParcels(ctx,sq,M);
  if(M.mode==='wall'){ drawWall(ctx,W,H,sq,M); if(ST.image) drawImageRay(ctx,W,H,sq,M); }
  if(M.mode==='two'&&ST.nodes) drawNodes(ctx,W,H,sq,M);
  frame(ctx,sq,'#2a3040');
  for(let k=0;k<M.speakers.length;k++) drawSpeaker(ctx,W,H,sq,M,k);
  if(ST.ruler) drawRuler(ctx,W,H,sq,M);
  if(ST.listener) drawListener(ctx,W,H,sq,M);
  /* PhET's scale bar and the clock */
  const sb=AIR.scaleLen/AIR.W*sq.w, yb=sq.y-10;
  ctx.fillStyle='#cfd4de'; ctx.fillRect(sq.x,yb-2,sb,3);
  lab(ctx,W,H,sq.x+sb+6,yb,fmt(AIR.scaleLen,0)+' m','#cfd4de',SM_FONT,'left');
  /* the slow-motion factor only when the box is wide enough to hold it: on a narrow stage
     the whole line is longer than the box and lab() shunts it down onto the picture */
  const conv=sq.w<420?'':'  (×'+fmt(1/AIR.phetTimeScale,0)+' slower than real)';
  lab(ctx,W,H,sq.x1,yb,(ST.running?'':'paused · ')+'t = '+sigf(M.t*1000,3)+' ms'+conv,
      '#8b93a6',SM_FONT,'right');
  if(ST.watch){
    const t='stopwatch '+sigf(M.watch*1000,4)+' ms', tw=t.length*11*0.58+18;
    ctx.fillStyle='rgba(10,12,18,.8)'; ctx.fillRect(sq.x1-tw-6,sq.y+6,tw,20);
    lab(ctx,W,H,sq.x1-tw+1,sq.y+16,t,M.watchOn?COL.pos:'#cfd4de',LAB_FONT,'left');
  }
  if(M.view==='air'){
    const t=sigf(ST.pressure,3)+' atm  ·  '+(ST.pressure>0?sigf(dbOf(ST.pressure),3)+' dB':'silent');
    const tw=t.length*11*0.58+18;
    ctx.fillStyle='rgba(10,12,18,.8)'; ctx.fillRect(sq.x+6,sq.y+6,tw,20);
    lab(ctx,W,H,sq.x+13,sq.y+16,t,ST.pressure>0.02?COL.pos:COL.ref,LAB_FONT,'left');
  }
  if(G.gb){ if(M.view==='air'&&!ST.graph) drawAirPanel(ctx,W,H,G.gb,M); else drawAxisGraph(ctx,W,H,G.gb,M); }
  if(G.tb) drawTrace(ctx,W,H,G.tb,M);
  const note=(y,t)=>{ ctx.fillStyle='rgba(7,11,24,.78)'; ctx.fillRect(sq.x+4,y-8,t.length*10.5*0.52+10,16);
    lab(ctx,W,H,sq.x+8,y,t,'#aeb6c6',SM_FONT,'left'); };
  if(G.graphDropped) note(sq.y1-12,'the graph needs a taller window');
  else if(ST.listener&&!G.tb&&!G.narrow) note(sq.y1-12,'the listener’s trace: widen the window to see it');
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ================================================================== *
 *  the analysis view: lambda = v/f measured on the lattice            *
 * ================================================================== */
const LAWPL={x0:1.93, x1:3.12, y0:-0.585, y1:0.625};
function lawGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,lawCaption(M,true),lawCaption(M,false),capW,top+200);
  const right=narrow?W-26:W-RO_W-44;
  const planeH=Math.max(120,Math.min(Math.round(0.42*(fit.capY-top)),486-44-top));
  const y2=Math.max(top+10+planeH+66,500);
  const h2=fit.capY-46-y2;
  const G={capY:fit.capY,capTxt:fit.txt,capW:fit.capW,narrow,strips:[]};
  G.plane=box(64,top+10,Math.max(160,right-74),planeH);
  if(!narrow&&h2>=80){
    const gut=62, span=(W-24)-64, w=(span-gut)/2;
    G.strips.push(box(64,y2,w,h2));
    G.strips.push(box(64+w+gut,y2,w,h2));
  }
  return G;
}
function lawCaption(M,full){
  const base='λ = v/f across PhET’s whole slider, on log scales: a fixed speed is a straight line of slope −1.';
  if(!full) return base;
  return base+' Orange is the law, the thick cyan stretch is the range PhET’s slider covers, the magenta ring is where it is set now,'
    +' and the green dots are the wavelength MEASURED on the lattice — a least-squares fit against the drive’s own phase at every cell'
    +' of a '+MEAS.N+'-cell tank, then the slope of the phase over cells '+MEAS.R0+' to '+MEAS.R1+'.'
    +' Below left: that measurement’s error, against what PhET’s single fixed time step does to the same wavelengths.'
    +' Below right: why this lattice is '+LAT.N+' cells and not PhET’s 151 — the phase and group speeds it carries, and how much longer a'
    +' wave is along the diagonal than along an axis. At 1000 Hz it holds '+sigf(cellsPerWave(AIR.fmax),3)
    +' cells per wavelength where PhET’s holds '+sigf(AIR.v/AIR.fmax/(AIR.W/AIR.phetVis),3)+'.';
}
function drawLaw(ctx,W,H,M){
  const G=lawGeo(ctx,W,H,M), b=G.plane, X=M.X;
  const xt=[100,200,500,1000].map(Math.log10), yt=[0.3,0.5,1,2,3].map(Math.log10);
  const dec=t=>sigf(Math.pow(10,t),2);
  axesR(ctx,b,LAWPL.x0,LAWPL.x1,LAWPL.y0,LAWPL.y1,{xticks:xt,yticks:yt,xfmt:dec,yfmt:dec,
    title:titleFor(b,'wavelength against frequency: λ = v/f, measured on the lattice','λ = v/f'),
    xlab:'frequency f, Hz',ylab:'wavelength λ, m'});
  const lv=Math.log10(AIR.v);
  /* the slider's range first, the law ON TOP of it: drawn the other way round the
     thick cyan band hides the one line the panel is about */
  const fa=Math.log10(AIR.fmin), fb=Math.log10(AIR.fmax);
  polyline(ctx,b,[fa,fb],[lv-fa,lv-fb],LAWPL.x0,LAWPL.x1,LAWPL.y0,LAWPL.y1,COL.struct,5);
  polyline(ctx,b,[LAWPL.x0,LAWPL.x1],[lv-LAWPL.x0,lv-LAWPL.x1],LAWPL.x0,LAWPL.x1,LAWPL.y0,LAWPL.y1,COL.ref,1.5,[7,4]);
  for(const r of X.rows) if(r.m){
    const px=b.x+b.w*(Math.log10(r.f)-LAWPL.x0)/(LAWPL.x1-LAWPL.x0);
    const py=b.y1-b.h*(Math.log10(r.m.lam)-LAWPL.y0)/(LAWPL.y1-LAWPL.y0);
    if(px>=b.x&&px<=b.x1&&py>=b.y&&py<=b.y1) dot(ctx,px,py,3.6,COL.pos);
  }
  marker(ctx,b,LAWPL.x0,LAWPL.x1,LAWPL.y0,LAWPL.y1,Math.log10(M.R.f),Math.log10(M.lam),COL.live);
  /* the legend goes in the clear band between the plane and the two panels: the law runs
     corner to corner, so legendAuto would rightly refuse every corner of the plane itself */
  if(G.strips.length&&b.w>=340){
    const lb=legendBox(ctx,b.x,b.y1+46,[[COL.ref,'λ = v/f, v = 343 m/s'],[COL.struct,'PhET’s slider'],
                                        [COL.live,'set now'],[COL.pos,'measured on the lattice']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
  }
  if(X.pending) lab(ctx,W,H,b.x+8,b.y1-12,'measuring '+X.pending+' more frequency'+(X.pending>1?'ies':'')+'…',
                    COL.dim,SM_FONT,'left');
  if(G.strips.length){
    drawErrPanel(ctx,W,H,G.strips[0],M);
    drawDispPanel(ctx,W,H,G.strips[1],M);
  } else if(!G.narrow) lab(ctx,W,H,b.x,b.y1+30,'the two panels below: a taller window shows them','#8b93a6',SM_FONT,'left');
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}
function drawErrPanel(ctx,W,H,b,M){
  const D=M.disp, xs=D.map(r=>r.f), ph=D.map(r=>100*r.phet);
  const lo=Math.min(-14,Math.min.apply(null,ph)*1.1);
  axesR(ctx,b,AIR.fmin,AIR.fmax,lo,2,{nx:4,ny:4,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0),
    title:titleFor(b,'how far the wavelength is from v/f, per cent','error in λ, %'),xlab:'frequency, Hz'});
  polyline(ctx,b,[AIR.fmin,AIR.fmax],[0,0],AIR.fmin,AIR.fmax,lo,2,'#3a4152',1);
  polyline(ctx,b,xs,ph,AIR.fmin,AIR.fmax,lo,2,COL.ref,1.6);
  const mf=[], me=[];
  for(const r of M.X.rows) if(r.m){ mf.push(r.f); me.push(100*r.m.err); }
  const ord=mf.map((v,i)=>i).sort((a,c)=>mf[a]-mf[c]);
  polyline(ctx,b,ord.map(i=>mf[i]),ord.map(i=>me[i]),AIR.fmin,AIR.fmax,lo,2,COL.pos,1.6);
  for(let i=0;i<mf.length;i++){
    const px=b.x+b.w*(mf[i]-AIR.fmin)/(AIR.fmax-AIR.fmin), py=b.y1-b.h*(me[i]-lo)/(2-lo);
    if(px>=b.x&&px<=b.x1&&py>=b.y&&py<=b.y1) dot(ctx,px,py,3,COL.pos);
  }
  const lb=legendAuto(ctx,b,[[COL.pos,'this lattice, measured'],[COL.ref,'PhET’s one fixed step']]);
  if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
}
function drawDispPanel(ctx,W,H,b,M){
  const D=M.disp, xs=D.map(r=>r.f);
  axesR(ctx,b,AIR.fmin,AIR.fmax,0.84,1.06,{nx:4,ny:4,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,2),
    title:titleFor(b,'what the square lattice does to a wave: speeds and shape','the lattice’s dispersion'),
    xlab:'frequency, Hz'});
  polyline(ctx,b,[AIR.fmin,AIR.fmax],[1,1],AIR.fmin,AIR.fmax,0.84,1.06,'#3a4152',1);
  polyline(ctx,b,xs,D.map(r=>r.vp),AIR.fmin,AIR.fmax,0.84,1.06,COL.struct,1.6);
  polyline(ctx,b,xs,D.map(r=>r.vg),AIR.fmin,AIR.fmax,0.84,1.06,COL.pos,1.6);
  polyline(ctx,b,xs,D.map(r=>1+r.aniso),AIR.fmin,AIR.fmax,0.84,1.06,COL.live,1.6);
  const lb=legendAuto(ctx,b,[[COL.struct,'phase speed / v'],[COL.pos,'group speed / v'],
                             [COL.live,'diagonal λ / axis λ']]);
  if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
}

/* ================================================================== *
 *  dispatch and the scene object                                      *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='law') return drawLaw(ctx,W,H,M);
  return drawBoxView(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(){ return ST.view==='law'?false:clockFrame()>0; };
  /* the pointer: the speaker button, the listener, the ruler and (two speakers)
     the second speaker */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(ST.view==='law') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(), G=boxGeo(ctx,S.W,S.H,M), sq=G.sq;
    if(type==='down'){
      const g=speakerGeo(sq,M,0);
      if(Math.hypot(x-g.btn.x,y-g.btn.y)<g.btn.r+3){ DRAG.what='button'; return pressSource(M.R); }
      if(ST.listener){
        const LX=mx(sq,M.listener.x), LY=my(sq,M.listener.y);
        if(Math.hypot(x-LX,y-LY)<13){ DRAG.what='listener'; return true; }
      }
      if(M.mode==='two'){
        const s2=speakerGeo(sq,M,1);
        if(x>=s2.x0-6&&x<=s2.x1+6&&Math.abs(y-s2.y)<20){ DRAG.what='spk2'; return true; }
      }
      if(ST.ruler){
        const r=rulerGeo(sq,M);
        if(x>=r.x0&&x<=r.x1&&Math.abs(y-r.y)<r.h/2+3){ DRAG.what='ruler'; return true; }
      }
      return false;
    }
    if(type==='move'){
      if(!DRAG.what||DRAG.what==='button') return false;
      const X=clamp((x-sq.x)/sq.w*AIR.W,0,AIR.W), Y=clamp((y-sq.y)/sq.h*AIR.W,0,AIR.W);
      if(DRAG.what==='listener'){ TOOLS.listener=[X,Y]; return true; }
      if(DRAG.what==='spk2'){ ST.spk2y=clamp(Y,0.35,AIR.W-0.35); return true; }
      if(DRAG.what==='ruler'){ TOOLS.ruler=[clamp(X-RULER_LEN/2,-1,AIR.W-1),Y]; return true; }
    }
    return false;
  };
  return S;
}
