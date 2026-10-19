
/* ================================================================== *
 *  drawing: the shared panel furniture, then the views                *
 * ================================================================== */
/* the house #hint sits at bottom:11px on top of the last line of a caption
   anchored at H - 12, and the canvas capture cannot see it because the hint
   is HTML: every caption here ends HINT_H higher, clear of it.
   (Known-bad, found by the wave-on-a-string build.) */
const HINT_H=18;

/* tick labels follow the tick SPACING, not a fixed decimal count: fmt(t,2)
   prints 12.00 whatever the range, and six of those do not fit a narrow
   panel (Known-bad, wave-on-a-string). */
function tickFmt(ticks){
  let g=Infinity; for(let i=1;i<ticks.length;i++) g=Math.min(g,Math.abs(ticks[i]-ticks[i-1]));
  if(!isFinite(g)||g<=0) return v=>sigf(v,3);
  let d=0; while(d<6&&Math.abs(Math.round(g*Math.pow(10,d))-g*Math.pow(10,d))>1e-6*Math.max(1,g*Math.pow(10,d))) d++;
  return v=>fmt(Math.abs(v)<1e-12?0:v,d);
}
function axesT(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=Object.assign({},opt||{});
  if(o.xticks===undefined) o.xticks=ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  if(o.yticks===undefined) o.yticks=ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||4);
  if(!o.xfmt) o.xfmt=tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt=tickFmt(o.yticks);
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
}
/* A row of stacked panels between the header and a measured caption.
   The gap has to clear the upper panel's x tick labels (b.y1+5, 12 px tall)
   AND the lower panel's title (b.y-9, 15 px tall), so anything under ~46 px
   puts one on the other; with an axis LABEL as well (b.y1+21) it needs ~62. */
function stackGeo(ctx,W,H,capFull,capShort,fracs,minTop,gap){
  const narrow=isNarrow(W), left=58, right=narrow?W-24:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,minTop||(stageTop()+30+150));
  const top=stageTop()+26, g=gap||46;
  /* 48, not 14: the LAST panel carries an axis label at its bottom + 21, and
     with only the caption's own 14 px of clearance that label lands on the
     first line of the caption */
  const avail=Math.max(110,fit.capY-48-top);
  const n=fracs.length, usable=Math.max(60,avail-g*(n-1));
  let tot=0; for(const f of fracs) tot+=f;
  const boxes=[]; let y=top;
  for(let i=0;i<n;i++){ const hh=Math.max(40,Math.floor(usable*fracs[i]/tot)); boxes.push(box(left,y,Math.max(120,right-left),hh)); y+=hh+g; }
  return {boxes,fit,narrow,left,right,capW};
}
/* the main-plus-bottom-row layout the analysis views use */
function mainGeo(ctx,W,H,capFull,capShort,nBottom,frac){
  const narrow=isNarrow(W), left=58, right=narrow?W-24:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,stageTop()+30+170);
  const top=stageTop()+26;
  const avail=Math.max(120,fit.capY-14-top);
  const nB=narrow?Math.min(1,nBottom):nBottom;
  let mainH=avail, bottom=[];
  if(nB>0){
    const rowH=Math.max(92,Math.floor(avail*(frac||0.36)));
    mainH=Math.max(90,avail-rowH-54);
    const gut=56, span=Math.max(160,right-left), w=(span-gut*(nB-1))/nB;
    /* 62, not 48: the main panel's axis label sits at its bottom + 21 and the
       bottom row's titles at their top - 24 */
    for(let i=0;i<nB;i++) bottom.push(box(left+i*(w+gut),top+mainH+62,Math.max(110,w-14),rowH-44));
  }
  return {main:box(left,top,Math.max(160,right-left),mainH),bottom,fit,narrow,left,right,capW};
}
function drawCap(ctx,G){ caption(ctx,G.left,G.fit.capY,G.fit.txt,G.capW,'#767e92',CAP_FONT); }
function zeroLine(ctx,b,ylo,yhi){
  if(ylo>0||yhi<0) return;
  const Y=b.y1-b.h*(0-ylo)/(yhi-ylo);
  ctx.save(); ctx.strokeStyle=COL.zero; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); ctx.stroke(); ctx.restore();
}

/* ---- the amplitude bars ------------------------------------------- *
 * PhET puts eleven sliders inside the chart; these are those sliders.
 * The geometry is shared between the drawing and the pointer, through
 * GEO, so a hit test can never disagree with the picture.             */
function barX(b,n,N){ return b.x+b.w*(n-0.5)/N; }
function barW(b,N){ return Math.max(3,Math.min(26,0.62*b.w/N)); }
function barY(b,a,amax){ return b.y1-b.h*(a+amax)/(2*amax); }
function barA(b,Y,amax){ return clamp((b.y1-Y)/b.h*2*amax-amax,-amax,amax); }
function barHit(b,x,y,N){
  if(y<b.y-10||y>b.y1+10||x<b.x-4||x>b.x1+4) return 0;
  const n=Math.floor((x-b.x)/b.w*N)+1;
  return (n>=1&&n<=N)?n:0;
}
function drawBars(ctx,b,amps,N,sel,amax,opt){
  const o=opt||{};
  const yt=[]; for(let v=-amax;v<=amax+1e-9;v+=amax/2) yt.push(+v.toFixed(6));
  axesT(ctx,b,0.5,N+0.5,-amax,amax,{title:o.title,ylab:o.ylab,
    xticks:intTicks(1,N),yticks:yt,ny:5});
  zeroLine(ctx,b,-amax,amax);
  const w=barW(b,N), y0=barY(b,0,amax);
  for(let n=1;n<=N;n++){
    const a=amps[n-1], X=barX(b,n,N), Y=barY(b,a,amax);
    if(o.ghost&&o.ghost[n-1]!==undefined&&o.ghost[n-1]!==null){
      const GY=barY(b,o.ghost[n-1],amax);
      ctx.strokeStyle=COL.ideal; ctx.lineWidth=1.4; ctx.setLineDash([3,3]);
      ctx.strokeRect(X-w/2-2.5,Math.min(GY,y0),w+5,Math.max(1.5,Math.abs(GY-y0)));
      ctx.setLineDash([]);
    }
    ctx.fillStyle=o.mono||harmCol(n);
    ctx.fillRect(X-w/2,Math.min(Y,y0),w,Math.max(1.5,Math.abs(Y-y0)));
    if(n===sel&&!o.noSel){
      ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
      ctx.strokeRect(X-w/2-2,Math.min(Y,y0)-2,w+4,Math.max(1.5,Math.abs(Y-y0))+4);
    }
    /* the handle, so the bar reads as something you can drag */
    ctx.fillStyle=a===0?'#4b5266':(n===sel?COL.live:'#d5dae4');
    ctx.fillRect(X-w/2-2,Y-1.5,w+4,3);
  }
  /* the harmonic numbers are the x TICKS (intTicks above); drawing a second
     row of them here put an identical label on top of every one of them. */
}

/* the geometry the pointer uses.  Filled on every draw; a hit test before
   the first draw simply finds nothing. */
const GEO={view:null};

/* ================================================================== *
 *  view 1: the harmonics — PhET's Discrete screen                     *
 * ================================================================== */
function harmCap(M){
  const st=M.st, u=xUnits(st.domain);
  const win=st.domain==='time'?'two periods of the fundamental, t = &minus;T to +T':'two wavelengths of the fundamental, x = &minus;L to +L';
  const dom=st.domain==='both'?' The whole pattern slides to the right at L/T = 0.44 m per ms; t is on the clock in the panel.':'';
  return {full:'Top: the '+(st.N===NMAX?'eleven':st.N)+' amplitudes, dragged here or set from a preset. Middle: each harmonic on its '
      +'own, coloured from green through to magenta as n runs 1 to '+st.N+'. Bottom: their sum, over '+win+', with the y axis fitted to the sum ('
      +sigf(M.yMax,3)+' full scale) and '+(st.showInf&&hasIdeal(st.preset)?'the waveform the infinite series converges to in orange.':'no reference curve.')
      +dom+' Lengths in '+u+'.',
    short:'Amplitudes, the harmonics, their sum. Two periods of the fundamental; y full scale '+sigf(M.yMax,3)+'.'};
}
function drawHarm(ctx,W,H,M){
  const st=M.st, cap=harmCap(M);
  const G=stackGeo(ctx,W,H,cap.full,cap.short,[0.9,1.05,1.25],stageTop()+30+230,46);
  const [bA,bH,bS]=G.boxes;
  const [xa,xb]=xWindow(st.domain), u=xUnits(st.domain);
  GEO.view='harm'; GEO.bars=bA; GEO.sum=bS; GEO.xa=xa; GEO.xb=xb; GEO.yMax=M.yMax;

  drawBars(ctx,bA,M.amps,st.N,st.sel,AMAX,{title:'amplitudes of the harmonics, A'+(st.N<NMAX?' (n &le; '+st.N+')':'')});

  /* the harmonics, each on its own */
  const hy=Math.max(0.2,Math.max.apply(null,M.amps.slice(0,st.N).map(Math.abs))||0.2);
  axesT(ctx,bH,xa,xb,-hy*1.1,hy*1.1,{title:titleFor(bH,'the harmonics, one curve each','harmonics'),ny:3});
  zeroLine(ctx,bH,-hy*1.1,hy*1.1);
  if(st.showHarm) for(let n=1;n<=st.N;n++){
    if(M.amps[n-1]===0) continue;
    const c=M.harms[n-1];
    polyline(ctx,bH,c.xs,c.ys,xa,xb,-hy*1.1,hy*1.1,harmCol(n),n===st.sel?2.4:1.3);
  }
  else lab(ctx,W,H,(bH.x+bH.x1)/2,(bH.y+bH.y1)/2,'harmonics hidden','#6f7789',LAB_FONT,'center','middle');

  /* the sum */
  axesT(ctx,bS,xa,xb,-M.yMax,M.yMax,{title:titleFor(bS,'the sum of the harmonics','the sum'),
    xlab:st.domain==='time'?'t ('+u+')':'x ('+u+')',ny:3});
  zeroLine(ctx,bS,-M.yMax,M.yMax);
  if(M.ideal) polyline(ctx,bS,M.ideal.xs,M.ideal.ys,xa,xb,-M.yMax,M.yMax,COL.ideal,4);   /* PhET's SECONDARY_WAVEFORM_LINE_WIDTH */
  polyline(ctx,bS,M.sum.xs,M.sum.ys,xa,xb,-M.yMax,M.yMax,COL.sum,1.8);
  if(st.caliper) drawCaliper(ctx,bS,st,M,xa,xb,u);
  const items=[[COL.sum,'the sum']];
  if(M.ideal) items.push([COL.ideal,'infinite harmonics']);
  if(st.caliper) items.push([COL.live,st.domain==='time'?'caliper: T/'+st.sel:'caliper: &lambda; = L/'+st.sel]);
  if(items.length>1) legendAuto(ctx,bS,items);
  drawCap(ctx,G);
}
/* PhET's wavelength/period caliper: its width IS the selected harmonic's
   wavelength, so lining it up on the curve measures that harmonic. */
function drawCaliper(ctx,b,st,M,xa,xb,u){
  const w=M.calW, x0=clamp(st.calX,xa,xb-w*0.02), x1=x0+w;
  const X0=b.x+b.w*(x0-xa)/(xb-xa), X1=b.x+b.w*(clamp(x1,xa,xb)-xa)/(xb-xa);
  const Y=b.y+10;
  ctx.save();
  ctx.strokeStyle=COL.live; ctx.lineWidth=1.6;
  ctx.beginPath();
  ctx.moveTo(X0,b.y); ctx.lineTo(X0,b.y1);
  ctx.moveTo(X1,b.y); ctx.lineTo(X1,b.y1);
  ctx.moveTo(X0,Y); ctx.lineTo(X1,Y);
  ctx.stroke();
  ctx.fillStyle=COL.live; ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='bottom';
  ctx.fillText(plain((st.domain==='time'?'T/':'&lambda; = L/')+st.sel+' = '+sigf(w,3)+' '+u),(X0+X1)/2,Y-3);
  ctx.restore();
  LABELS.push([(X0+X1)/2-50,Y-16,(X0+X1)/2+50,Y-2]);
}

/* ================================================================== *
 *  view 2: the convergence — Gibbs, and the error that does fall      *
 * ================================================================== */
/* canvas text carries NO letter subscripts: there is no Unicode subscript f
   at all and the ones that exist are not all in the rasteriser's font, so
   "S_M" is written with an ASCII underscore (Known-bad, greenhouse-effect).
   A log axis is labelled in plain decimals for the same reason. */
function logLab(v){
  if(!(v>0)||!isFinite(v)) return '';
  if(v>=0.001&&v<10000) return String(+Number(v).toPrecision(3));
  const e=Math.floor(Math.log10(v)), m=v/Math.pow(10,e);
  return (Math.abs(m-1)<0.05?'1':String(+Number(m).toPrecision(2)))+'e'+e;
}
/* logTicks gives ONE tick over a range under two decades, which leaves an axis
   with a single label.  Below two decades, subdivide each decade by 1-2-5. */
function logTicksFine(lo,hi){
  if(!(lo>0)||!(hi>0)||!isFinite(lo)||!isFinite(hi)||hi<=lo) return [];
  const dec=Math.log10(hi/lo);
  if(dec>2.2) return logTicks(lo,hi);
  const out=[];
  for(let e=Math.floor(Math.log10(lo));e<=Math.ceil(Math.log10(hi));e++)
    for(const m of [1,2,5]){ const v=m*Math.pow(10,e); if(v>=lo*0.999&&v<=hi*1.001) out.push(v); }
  return out.length?out:logTicks(lo,hi);
}
function convCap(M){
  const C=M.C;
  const g=C.jump>0?('The peak of S_M overshoots by '+sigf(100*(C.pk.val-1)/C.jump,4)
      +' % of the jump; as M grows that tends to '+sigf(100*GIBBS_FRACTION,6)+' %, not to zero. ')
    :'This waveform is continuous, so there is no jump and no overshoot: the partial sums stay inside it. ';
  return {full:'Green: the sum of the first '+C.M+' terms. Orange: the waveform the complete series converges to. '+g
      +'Bottom left: the peak of the square wave&rsquo;s partial sum against M, with the Wilbraham&ndash;Gibbs limit '
      +'in orange. Bottom right: the rms distance from the complete waveform, which does go to zero &mdash; the ringing '
      +'survives because it gets narrower, not shorter. Both axes there are logarithmic.',
    short:'S_M in green against the complete waveform in orange; the peak vs M, and the rms error vs M (log-log).'};
}
function drawConv(ctx,W,H,M){
  const C=M.C, cap=convCap(M);
  const G=mainGeo(ctx,W,H,cap.full,cap.short,2,0.34);
  const b=G.main;
  GEO.view='conv';
  let ym=1.35;
  for(const v of C.sm) ym=Math.max(ym,Math.abs(v)*1.12);
  const PILAB={};
  PILAB[fmt(-PI,2)]=plain('&minus;&pi;'); PILAB[fmt(-PI/2,2)]=plain('&minus;&pi;/2');
  PILAB[fmt(0,2)]='0'; PILAB[fmt(PI/2,2)]=plain('&pi;/2'); PILAB[fmt(PI,2)]=plain('&pi;');
  axesT(ctx,b,-PI,PI,-ym,ym,{title:'S_M against the waveform it converges to',
    xlab:'phase u (rad)',ylab:'F',ny:4,
    xticks:[-PI,-PI/2,0,PI/2,PI],xfmt:v=>PILAB[fmt(v,2)]||fmt(v,2)});
  zeroLine(ctx,b,-ym,ym);
  polyline(ctx,b,C.us,C.id,-PI,PI,-ym,ym,COL.ideal,4);   /* PhET's SECONDARY_WAVEFORM_LINE_WIDTH */
  polyline(ctx,b,C.us,C.sm,-PI,PI,-ym,ym,COL.sum,1.7);
  if(isFinite(C.pk.val)){
    marker(ctx,b,-PI,PI,-ym,ym,C.pk.u,C.pk.val,COL.live);
    const X=b.x+b.w*(C.pk.u+PI)/TAU, Y=b.y1-b.h*(C.pk.val+ym)/(2*ym);
    /* the label goes on the side AWAY from the panel edge: a sawtooth's ear is
       at u = pi N/(N+1), hard against the right edge, and a right-hand label
       there runs under the floating readout (audit: under-readout) */
    const rt=X>b.x+0.6*b.w;
    lab(ctx,W,H,X+(rt?-9:9),Y-5,'peak '+sigf(C.pk.val,6),COL.live,SM_FONT,rt?'right':'left','bottom');
  }
  legendAuto(ctx,b,[[COL.sum,'S_M, M = '+C.M],[COL.ideal,'the complete waveform'],
                    [COL.live,C.jump>0?'the first Gibbs peak':'the largest value']]);

  /* the overshoot against the number of ODD harmonics: the square wave's own
     partial-sum peak, which is where the Wilbraham-Gibbs constant lives */
  if(G.bottom.length>0){
    const p=G.bottom[0], lo=1.15, hi=1.30;
    axesT(ctx,p,1,64,lo,hi,{title:titleFor(p,'peak of the square wave S_M','peak vs M'),
      xlab:'odd harmonics kept',ny:4});
    polyline(ctx,p,C.ms,C.pks,1,64,lo,hi,COL.sum,1.6);
    /* the limit line goes on TOP of the curve it is the limit of, dashed: under
       it, the curve converging onto it hides it exactly where it matters */
    polyline(ctx,p,[1,64],[GIBBS_PEAK,GIBBS_PEAK],1,64,lo,hi,COL.ideal,1.8,[5,4]);
    for(let i=0;i<C.ms.length;i+=8) marker(ctx,p,1,64,lo,hi,C.ms[i],C.pks[i],'#6f8f2c');
    if(C.name==='square'&&C.odd<=64) marker(ctx,p,1,64,lo,hi,C.odd,squarePeakClosed(C.odd).val,COL.live);
    lab(ctx,W,H,p.x1-6,p.y+13,plain('(2/&pi;) Si(&pi;) = ')+sigf(GIBBS_PEAK,7),COL.ideal,SM_FONT,'right','top');
  }
  /* the rms error against M, log-log */
  if(G.bottom.length>1){
    const p=G.bottom[1];
    let emin=Infinity, emax=0;
    for(const e of C.errs) if(e>0){ emin=Math.min(emin,e); emax=Math.max(emax,e); }
    if(!(emin>0&&isFinite(emin))){ emin=1e-4; emax=1; }
    const lo=Math.log10(emin*0.5), hi=Math.log10(emax*2), xhi=Math.log10(128);
    const xs=[], ys=[];
    for(let i=0;i<C.Ns.length;i++) if(C.errs[i]>0){ xs.push(Math.log10(C.Ns[i])); ys.push(Math.log10(C.errs[i])); }
    axesT(ctx,p,0,xhi,lo,hi,{title:titleFor(p,'rms error |f &minus; S_M|','rms error'),
      xlab:'M',xticks:[0,1,2],xfmt:v=>String(Math.round(Math.pow(10,v))),
      yticks:logTicksFine(Math.pow(10,lo),Math.pow(10,hi)).map(v=>Math.log10(v)),
      yfmt:v=>logLab(Math.pow(10,v))});
    polyline(ctx,p,xs,ys,0,xhi,lo,hi,COL.sum,1.7);
    if(C.rms>0) marker(ctx,p,0,xhi,lo,hi,Math.log10(C.M),Math.log10(C.rms),COL.live);
  }
  drawCap(ctx,G);
}
