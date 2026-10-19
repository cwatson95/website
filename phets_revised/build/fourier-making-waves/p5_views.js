
/* ================================================================== *
 *  view 3: the spectrum — Parseval, and the amplitudes coming back    *
 * ================================================================== */
function specCap(M){
  const S=M.S;
  return {full:'Top: the amplitudes you set (bars) with the amplitudes RECOVERED from the drawn waveform '
      +'(magenta rings) laid over them. The waveform is sampled at '+SPEC_NS+' points of one period and projected '
      +'back onto sin nu and cos nu by a radix-2 FFT; the two agree to '+sigf(S.dFFT,2)+', and the FFT agrees with a '
      +'direct O(N&sup2;) sum to '+sigf(S.dDir,2)+'. Bottom left: the power each harmonic carries, &frac12;A&sup2;, and the '
      +'running fraction of the total (magenta, right-hand scale 0 to 1). Bottom right: the waveform with its rms '
      +'level &plusmn;'+sigf(S.rms,4)+' in orange &mdash; that level IS &radic;(&frac12;&Sigma;A&sup2;), which is Parseval.',
    short:'The amplitudes, recovered from the waveform (magenta rings); the power per harmonic; the rms level.'};
}
function drawSpec(ctx,W,H,M){
  const S=M.S, st=M.st, cap=specCap(M);
  const G=mainGeo(ctx,W,H,cap.full,cap.short,2,0.5);
  const b=G.main;
  GEO.view='spec'; GEO.bars=b;
  drawBars(ctx,b,M.amps,st.N,st.sel,AMAX,{title:'the amplitudes, and the same amplitudes read back out of the waveform'});
  for(let n=1;n<=st.N;n++){
    const X=barX(b,n,st.N), Y=barY(b,clamp(S.back[n-1],-AMAX,AMAX),AMAX);
    dot(ctx,X,Y,4,null,COL.live,1.6);
  }
  legendAuto(ctx,b,[[COL.live,'recovered by the FFT']]);

  if(G.bottom.length>0){
    const p=G.bottom[0];
    const pmax=Math.max(1e-6,Math.max.apply(null,S.P)*1.15);
    axesT(ctx,p,0.5,st.N+0.5,0,pmax,{title:titleFor(p,'power per harmonic, half A squared','power'),
      xlab:'n',xticks:intTicks(1,st.N),ny:4});
    const w=barW(p,st.N);
    for(let n=1;n<=st.N;n++){
      const X=barX(p,n,st.N), Y=p.y1-p.h*S.P[n-1]/pmax;
      ctx.fillStyle=harmCol(n); ctx.fillRect(X-w/2,Y,w,Math.max(1,p.y1-Y));
    }
    const cx=[], cy=[];
    for(let n=1;n<=st.N;n++){ cx.push(n); cy.push(S.cum[n-1]*pmax); }
    polyline(ctx,p,cx,cy,0.5,st.N+0.5,0,pmax,COL.live,1.6);
    for(let n=1;n<=st.N;n++) marker(ctx,p,0.5,st.N+0.5,0,pmax,n,S.cum[n-1]*pmax,COL.live);
    lab(ctx,W,H,p.x1-4,p.y+13,'magenta: running fraction, 0 to 1',COL.live,SM_FONT,'right','top');
  }
  if(G.bottom.length>1){
    const p=G.bottom[1];
    const ym=Math.max(1e-6,yFit(S.y,0.3));
    const us=[], ys=[];
    for(let j=0;j<SPEC_NS;j++){ us.push(TAU*j/SPEC_NS); ys.push(S.y[j]); }
    us.push(TAU); ys.push(S.y[0]);
    axesT(ctx,p,0,TAU,-ym,ym,{title:titleFor(p,'the waveform and its rms level','the waveform'),xlab:'phase u (rad)',ny:4,
      xticks:[0,PI,TAU],xfmt:v=>v===0?'0':(Math.abs(v-PI)<1e-9?plain('&pi;'):plain('2&pi;'))});
    zeroLine(ctx,p,-ym,ym);
    polyline(ctx,p,[0,TAU],[S.rms,S.rms],0,TAU,-ym,ym,COL.ideal,1.6,[5,4]);
    polyline(ctx,p,[0,TAU],[-S.rms,-S.rms],0,TAU,-ym,ym,COL.ideal,1.6,[5,4]);
    polyline(ctx,p,us,ys,0,TAU,-ym,ym,COL.sum,1.7);
    lab(ctx,W,H,p.x+5,p.y+13,'rms '+sigf(S.rms,4),COL.ideal,SM_FONT,'left','top');
  }
  drawCap(ctx,G);
}

/* ================================================================== *
 *  view 4: the wave game — PhET's Wave Game screen                    *
 * ================================================================== */
function gameCap(M){
  return {full:'Magenta: a waveform built from '+M.nzAns+' of the eleven harmonics, amplitudes hidden. Green: your guess. '
      +'Drag the bars below (or use the harmonic and amplitude controls) until the two curves lie on top of each other. '
      +(M.match?'They match exactly &mdash; every one of the eleven amplitudes agrees. '
               :'The worst amplitude is still out by '+sigf(M.worst,3)+', and the two waveforms differ by an rms of '+sigf(M.rmsErr,3)+'. ')
      +'PhET allows amplitudes in steps of '+fmt(G_STEP,1)+' on this screen, and counts a guess right only when every '
      +'amplitude matches exactly &mdash; being close is not enough.',
    short:'Magenta: the waveform to match. Green: your guess. Drag the bars until they coincide.'};
}
function drawGame(ctx,W,H,M){
  const st=M.st, cap=gameCap(M);
  const G=stackGeo(ctx,W,H,cap.full,cap.short,[1.15,1],stageTop()+30+190,62);
  const [bC,bA]=G.boxes;
  const [xa,xb]=xWindow('space');
  GEO.view='game'; GEO.bars=bA;
  axesT(ctx,bC,xa,xb,-M.yMax,M.yMax,{title:'the waveform to match, and your guess',xlab:'x (m)',ny:3});
  zeroLine(ctx,bC,-M.yMax,M.yMax);
  polyline(ctx,bC,M.target.xs,M.target.ys,xa,xb,-M.yMax,M.yMax,COL.target,4);   /* PhET's SECONDARY_WAVEFORM_LINE_WIDTH: the reference curve is wider so the guess drawn on it still shows */
  polyline(ctx,bC,M.guess.xs,M.guess.ys,xa,xb,-M.yMax,M.yMax,COL.guess,1.7);
  legendAuto(ctx,bC,[[COL.target,'the waveform to match'],[COL.guess,'your guess'+(M.match?' (matched)':'')]]);
  drawBars(ctx,bA,M.amps,NMAX,st.sel,AMAX,
    {title:'your amplitudes'+(st.showAns?' (the answer is shown)':'')+', in steps of '+fmt(G_STEP,1)});
  if(st.showAns){
    const w=barW(bA,NMAX), y0=barY(bA,0,AMAX);
    for(let n=1;n<=NMAX;n++){
      const X=barX(bA,n,NMAX), Y=barY(bA,M.ans[n-1],AMAX);
      ctx.strokeStyle=COL.ideal; ctx.lineWidth=1.4; ctx.setLineDash([3,3]);
      ctx.strokeRect(X-w/2-3,Math.min(Y,y0)-1,w+6,Math.max(2,Math.abs(Y-y0))+2);
      ctx.setLineDash([]);
    }
    lab(ctx,W,H,bA.x1-4,bA.y+13,'orange: the answer',COL.ideal,SM_FONT,'right','top');
  }
  drawCap(ctx,G);
}

/* ================================================================== *
 *  view 5: the wave packet — PhET's Wave Packet screen                *
 * ================================================================== */
function packCap(M){
  const P=M.P, tm=M.st.wpDom==='time';
  const ku=tm?'rad/ms':'rad/m', xu=tm?'ms':'m', sk=tm?'w':'k', sx=tm?'t':'x';
  return {full:(P.cont
        ? 'Top: the amplitude density A(k) itself &mdash; with the spacing set to zero there are no separate components '
          +'to draw, only infinitely many of them. Middle: nothing can be drawn there either. Bottom: the integral they '
          +'add up to, with its envelope in orange. '
        : 'Top: the amplitude of every component, A(k)k&#8321;, as a stem at its own k; the orange curve is the '
          +'continuous A(k)k&#8321; the stems sample. Middle: those components drawn as waves. Bottom: their sum, with '
          +'the envelope in orange. There are '+P.n+' of them, spaced '+sigf(P.k1,3)+' '+ku+' apart, which makes the sum '
          +'repeat every '+sigf(P.lam1,3)+' '+xu+'. ')
      +'The width markers show 2 sigma_'+sk+' on the spectrum and 2 sigma_'+sx+' on the packet, and their product is '
      +'exactly 1: sigma_'+sx+' = 1/sigma_'+sk+' = '+sigf(P.sx,4)+' '+xu+'.',
    short:'The components, their waves, and their sum with its envelope. 2 sigma_'+sk+' across the spectrum, 2 sigma_'+sx+' across the packet.'};
}
function drawPack(ctx,W,H,M){
  const P=M.P, st=M.st, cap=packCap(M);
  const G=stackGeo(ctx,W,H,cap.full,cap.short,[0.95,0.95,1.2],stageTop()+30+235,50);
  const [bK,bC,bS]=G.boxes;
  const ku=st.wpDom==='time'?'rad/ms':'rad/m', xu=st.wpDom==='time'?'ms':'m';
  const kl=st.wpDom==='time'?'omega':'k', xl=st.wpDom==='time'?'t':'x';
  GEO.view='pack';

  /* the spectrum */
  const amax=Math.max(P.peakPlot*1.22,1e-12);
  /* the axis name goes in the TITLE here: a separate xlab under this panel
     would land on the next panel's title (the stack gap is 50 px) */
  axesT(ctx,bK,0,WP_KMAX,0,amax,{title:'the amplitude of each component, against '+kl+' in '+ku,nx:5,ny:3});
  if(!P.cont){
    const cxs=[], cys=[];
    for(let j=0;j<=400;j++){ const k=WP_KMAX*j/400; cxs.push(k); cys.push(wpAmp(k,P.k0,P.sk)*P.k1); }
    polyline(ctx,bK,cxs,cys,0,WP_KMAX,0,amax,COL.ideal,1.6);
    for(const c of P.comps){
      const X=bK.x+bK.w*c.k/WP_KMAX, Y=bK.y1-bK.h*c.a/amax;
      ctx.strokeStyle=neonCss(clamp((c.k-P.k0+2.5*P.sk)/(5*P.sk),0,1)); ctx.lineWidth=2;
      ctx.beginPath(); ctx.moveTo(X,bK.y1); ctx.lineTo(X,Y); ctx.stroke();
    }
  } else {
    const cxs=[], cys=[];
    for(let j=0;j<=400;j++){ const k=WP_KMAX*j/400; cxs.push(k); cys.push(wpAmp(k,P.k0,P.sk)); }
    polyline(ctx,bK,cxs,cys,0,WP_KMAX,0,amax,COL.ideal,2);
    lab(ctx,W,H,bK.x+6,bK.y+13,'continuous: A(k), not A(k)k1',COL.ideal,SM_FONT,'left','top');
  }
  if(st.wpWid) widthBar(ctx,W,H,bK,0,WP_KMAX,0,amax,P.k0-P.sk,P.k0+P.sk,
    P.peakPlot*Math.exp(-0.5),'2 sigma_'+(st.wpDom==='time'?'w':'k')+' = '+sigf(2*P.sk,3));

  /* The components as waves, over a ZOOMED window.  Across the full +-2 m the
     highest component runs 48 cycles, which no number of samples can draw as
     anything but a band -- and sampling it at the sum's resolution aliases it
     into a curve that is not the component at all.  The window is 3 sigma_x
     either side, the zoom factor is printed, and the sum panel below carries a
     magenta bracket showing which slice this is. */
  const [xa,xb]=[-2,2];
  const xz=clamp(3*P.sx,0.12,2), nsC=clamp(Math.ceil(16*WP_KMAX*xz/PI),360,1600);
  if(!P.cont){
    let cm=1e-9; for(const c of P.comps) cm=Math.max(cm,c.a);
    axesT(ctx,bC,-xz,xz,-cm*1.2,cm*1.2,{title:titleFor(bC,'the components, drawn as waves','the components'),ny:3});
    zeroLine(ctx,bC,-cm*1.2,cm*1.2);
    let drawn=0;
    for(const c of P.comps){
      if(c.a<P.amax*0.02) continue;
      const xs=[], ys=[];
      for(let j=0;j<=nsC;j++){ const x=-xz+2*xz*j/nsC; xs.push(x); ys.push(c.a*Math.cos(c.k*x)); }
      polyline(ctx,bC,xs,ys,-xz,xz,-cm*1.2,cm*1.2,neonCss(clamp((c.k-P.k0+2.5*P.sk)/(5*P.sk),0,1)),1.1);
      drawn++;
    }
    lab(ctx,W,H,bC.x+5,bC.y+13,drawn+' of '+P.n+' components, over '+sigf(2*xz,3)+' '+xu
        +' (x'+sigf((xb-xa)/(2*xz),2)+' zoom)','#8b93a6',SM_FONT,'left','top');
  } else {
    axesT(ctx,bC,-xz,xz,-1,1,{title:titleFor(bC,'the components, drawn as waves','the components'),ny:3});
    zeroLine(ctx,bC,-1,1);
    lab(ctx,W,H,(bC.x+bC.x1)/2,(bC.y+bC.y1)/2,'an infinite number of components cannot be drawn','#6f7789',LAB_FONT,'center','middle');
  }

  /* the sum */
  const ym=Math.max(1.15,yFit(P.sum,1));
  axesT(ctx,bS,xa,xb,-ym,ym,{title:titleFor(bS,'the sum of the components','the sum'),xlab:xl+' ('+xu+')',ny:3});
  zeroLine(ctx,bS,-ym,ym);
  if(st.wpEnv){
    polyline(ctx,bS,P.xs,P.env,xa,xb,-ym,ym,COL.env,1.6);
    polyline(ctx,bS,P.xs,P.env.map(v=>-v),xa,xb,-ym,ym,COL.env,1.6);
  }
  polyline(ctx,bS,P.xs,P.sum,xa,xb,-ym,ym,COL.sum,1.7);
  /* the bracket marking the slice the components panel above is zoomed into */
  { const X0=bS.x+bS.w*(-xz-xa)/(xb-xa), X1=bS.x+bS.w*(xz-xa)/(xb-xa);
    ctx.save(); ctx.strokeStyle=rgba(COL.struct,0.55); ctx.lineWidth=1.2;
    ctx.beginPath();
    ctx.moveTo(X0,bS.y); ctx.lineTo(X0,bS.y+7); ctx.moveTo(X0,bS.y); ctx.lineTo(X1,bS.y);
    ctx.moveTo(X1,bS.y); ctx.lineTo(X1,bS.y+7);
    ctx.stroke(); ctx.restore(); }
  if(st.wpWid) widthBar(ctx,W,H,bS,xa,xb,-ym,ym,-P.sx,P.sx,Math.exp(-0.5),'2 sigma_'+(st.wpDom==='time'?'t':'x')+' = '+sigf(2*P.sx,3));
  const items=[[COL.sum,'the sum']];
  if(st.wpEnv) items.push([COL.env,'the envelope']);
  if(st.wpWid) items.push([COL.live,'width at 1/sqrt(e)']);
  legendAuto(ctx,bS,items);
  drawCap(ctx,G);
}
/* PhET's width indicator: a horizontal bar with end caps, drawn at the
   height where the Gaussian has fallen to 1/sqrt(e), which is where the
   full width IS twice the standard deviation. */
function widthBar(ctx,W,H,b,xlo,xhi,ylo,yhi,x0,x1,y,txt){
  const X0=b.x+b.w*(x0-xlo)/(xhi-xlo), X1=b.x+b.w*(x1-xlo)/(xhi-xlo);
  const Y=b.y1-b.h*(y-ylo)/(yhi-ylo);
  if(!isFinite(X0)||!isFinite(X1)||Y<b.y||Y>b.y1) return;
  const A=clamp(X0,b.x,b.x1), B=clamp(X1,b.x,b.x1);
  ctx.save(); ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
  ctx.beginPath();
  ctx.moveTo(A,Y); ctx.lineTo(B,Y);
  ctx.moveTo(A,Y-5); ctx.lineTo(A,Y+5);
  ctx.moveTo(B,Y-5); ctx.lineTo(B,Y+5);
  ctx.stroke(); ctx.restore();
  lab(ctx,W,H,(A+B)/2,Y-9,txt,COL.live,SM_FONT,'center','bottom');
}

/* ================================================================== *
 *  view 6: the transform pair — Poisson, and sigma_x sigma_k = 1      *
 * ================================================================== */
function pairCap(M){
  const T=M.T;
  return {full:'The same Gaussian packet, drawn over three metres instead of two. Green: the sum over the discrete '
      +'components spaced k&#8321; = '+sigf(T.k1,3)+' rad/m apart. Orange: the exact continuous transform, '
      +'exp(&minus;sigma_k&sup2;x&sup2;/2)cos(k&#8320;x). They are not approximations of each other: by Poisson summation the '
      +'discrete sum IS the continuous packet repeated every lambda&#8321; = 2pi/k&#8321; = '+sigf(T.lam1,3)+' m, and the magenta '
      +'ticks mark where the copies sit. Narrow the spacing and the copies walk out of the window. Bottom left: the two '
      +'widths are exactly reciprocal. Bottom right: how far the discrete sum is from the continuous one, over the whole '
      +'window (green) and inside one period (magenta), against the orange Gaussian-tail floor. Logarithmic in both.',
    short:'The discrete packet (green) is the continuous one (orange) repeated every lambda1. The reciprocal widths, and the error.'};
}
function drawPair(ctx,W,H,M){
  const T=M.T, cap=pairCap(M);
  const G=mainGeo(ctx,W,H,cap.full,cap.short,2,0.36);
  const b=G.main;
  GEO.view='pair';
  const ym=1.25;
  axesT(ctx,b,-T.W,T.W,-ym,ym,{title:'the discrete sum against the exact continuous packet',
    xlab:'x (m)',ylab:'F',ny:4});
  zeroLine(ctx,b,-ym,ym);
  polyline(ctx,b,T.xs,T.con,-T.W,T.W,-ym,ym,COL.cont,4);   /* wider, so the discrete sum lying exactly on it still shows the orange */
  polyline(ctx,b,T.xs,T.dis,-T.W,T.W,-ym,ym,COL.sum,1.6);
  for(let m=-6;m<=6;m++){
    if(m===0) continue;
    const x=m*T.lam1;
    if(Math.abs(x)>T.W) continue;
    const X=b.x+b.w*(x+T.W)/(2*T.W);
    ctx.save(); ctx.strokeStyle=COL.live; ctx.lineWidth=1.3; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke(); ctx.restore();
  }
  legendAuto(ctx,b,[[COL.sum,'the discrete sum'],[COL.cont,'the continuous packet'],
                    [COL.live,'copies at multiples of lambda1']]);

  if(G.bottom.length>0){
    const p=G.bottom[0], sxm=1/WP_SK_MIN*1.22;
    axesT(ctx,p,0,WP_SK_MAX*1.05,0,sxm,{title:titleFor(p,'the two widths are reciprocal','sigma_x vs sigma_k'),
      xlab:'sigma_k (rad/m)',ny:4});
    polyline(ctx,p,T.sks,T.sxs,0,WP_SK_MAX*1.05,0,sxm,COL.ideal,1.8);
    marker(ctx,p,0,WP_SK_MAX*1.05,0,sxm,T.sk,T.sx,COL.live);
    lab(ctx,W,H,p.x1-4,p.y+13,'sigma_x sigma_k = '+fmt(T.prod,10),COL.live,SM_FONT,'right','top');
  }
  if(G.bottom.length>1){
    const p=G.bottom[1];
    let emin=T.tail*0.4, emax=2;
    for(const e of T.errW) if(e>0) emax=Math.max(emax,e);
    for(const e of T.errP) if(e>0) emin=Math.min(emin,e);
    const lo=Math.log10(Math.max(1e-9,emin*0.5)), hi=Math.log10(emax*1.6);
    const xa=Math.log10(T.k1s[0]), xb=Math.log10(T.k1s[T.k1s.length-1]);
    const lx=T.k1s.map(Math.log10);
    const xtk=logTicksFine(T.k1s[0],T.k1s[T.k1s.length-1]);
    axesT(ctx,p,xa,xb,lo,hi,{title:titleFor(p,'how far the discrete sum is from the continuous one','the error'),
      xlab:'k1 (rad/m)',
      xticks:xtk.map(Math.log10),xfmt:v=>sigf(Math.pow(10,v),2),
      yticks:logTicksFine(Math.pow(10,lo),Math.pow(10,hi)).map(Math.log10),yfmt:v=>logLab(Math.pow(10,v))});
    polyline(ctx,p,[xa,xb],[Math.log10(T.tail),Math.log10(T.tail)],xa,xb,lo,hi,COL.ideal,1.6,[5,4]);
    polyline(ctx,p,lx,T.errW.map(v=>Math.log10(Math.max(v,1e-12))),xa,xb,lo,hi,COL.sum,1.7);
    polyline(ctx,p,lx,T.errP.map(v=>Math.log10(Math.max(v,1e-12))),xa,xb,lo,hi,COL.live,1.5,[4,3]);
    marker(ctx,p,xa,xb,lo,hi,Math.log10(T.k1),Math.log10(Math.max(T.devW,1e-12)),COL.live);
    lab(ctx,W,H,p.x+5,p.y+13,'orange: the Gaussian tail',COL.ideal,SM_FONT,'left','top');
  }
  drawCap(ctx,G);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  POLY_SEGS=[]; LABELS=[]; LEGEND_RECTS=[];
  GEO.view=null; GEO.bars=null; GEO.sum=null;
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  const v=M.view;
  if(v==='harm') drawHarm(ctx,W,H,M);
  else if(v==='conv') drawConv(ctx,W,H,M);
  else if(v==='spec') drawSpec(ctx,W,H,M);
  else if(v==='game') drawGame(ctx,W,H,M);
  else if(v==='pack') drawPack(ctx,W,H,M);
  else drawPair(ctx,W,H,M);
}

function makeScene(canvas){
  const S={st:ST,W:1200,H:760,canvas,
    model:buildModel,
    draw(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); },
    step(dt){                       /* PhET: t runs only in the space & time domain */
      if(ST.view==='harm'&&ST.running&&ST.domain==='both'&&dt>0){ ST.t+=dt; return true; }
      return false;
    },
    stepOnce(){ ST.t+=0.05; },      /* PhET's step button: +0.05 ms */
    pointer(kind,x,y){
      if(kind==='up'){ const was=S.drag; S.drag=null; return !!was; }
      if(kind==='down'){
        S.drag=null;
        if((GEO.view==='harm'||GEO.view==='game'||GEO.view==='spec')&&GEO.bars){
          const N=GEO.view==='harm'?ST.N:(GEO.view==='spec'?ST.N:NMAX);
          const n=barHit(GEO.bars,x,y,N);
          if(n){ S.drag={what:'bar',n}; ST.sel=n; return S.setBar(n,y); }
        }
        if(GEO.view==='harm'&&ST.caliper&&GEO.sum&&x>=GEO.sum.x-8&&x<=GEO.sum.x1+8&&y>=GEO.sum.y&&y<=GEO.sum.y1){
          S.drag={what:'cal'}; return S.setCal(x);
        }
        return false;
      }
      if(!S.drag) return false;
      if(S.drag.what==='bar') return S.setBar(S.drag.n,y);
      if(S.drag.what==='cal') return S.setCal(x);
      return false;
    },
    setBar(n,y){
      const step=GEO.view==='game'?G_STEP:A_STEP;
      const a=snapAmp(barA(GEO.bars,y,AMAX),step), arr=ampArray();
      if(arr[n-1]===a) return false;
      arr[n-1]=a;
      if(GEO.view!=='game') ST.preset='custom';
      return true;
    },
    setCal(x){
      const b=GEO.sum, w=GEO.xb-GEO.xa;
      const v=GEO.xa+w*clamp((x-b.x)/b.w,0,1);
      if(Math.abs(v-ST.calX)<1e-12) return false;
      ST.calX=v; return true;
    },
    drag:null};
  return S;
}
