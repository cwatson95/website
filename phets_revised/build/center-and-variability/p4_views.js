
/* ================================================================== *
 *  the drawing layer: the field, the number line, the dot plot and    *
 *  the five measures drawn on it — then PhET's first two screens.     *
 * ================================================================== */
/* The house #hint is HTML at bottom:11px and the display-list capture cannot
   see it, so every bottom-anchored caption ends HINT_H higher than the canvas
   floor and selfTest asserts the corner stays clear (wave-on-a-string). */
const HINT_H=18;
/* the number line spans PhET's VARIABILITY_DRAG_RANGE (0..16) so the interval
   handles and the pointer never leave the picture; the ticks are the 1..15 m
   of PHYSICAL_RANGE */
const XLO=0, XHI=16;
/* the band reserved UNDER the number line, laid out once so that nothing has
   to guess: tick marks at +0..+5, tick labels at +7..+19, the measure's own
   bars at +23..+45, and its labels from +46 down.  The first draft reserved
   22 px and the IQR labels landed in the caption at every canvas size. */
const NL_BELOW=76, NL_TICKLAB=7, NL_BAR=26, NL_LAB=34, NL_LAB2=50;

/* axes() and the number line draw their tick labels and axis titles straight
   to the canvas, outside the label registry, so lab() and legendAuto() cannot
   see them and put things on top (found by the layout sweep: an axis title
   under a note, a legend over a tick, a median label over a tick).  regText
   records what was drawn; axesQ wraps axesR so every axis registers itself. */
function regText(x,y,txt,px,align,base){
  const t=plain(txt), w=t.length*px*0.52, fh=px*1.15;
  const lx=align==='center'?x-w/2:(align==='right'?x-w:x);
  const ly=base==='top'?y:(base==='middle'?y-fh/2:(base==='bottom'?y-fh:y-fh*0.8));
  LABELS.push([lx,ly,lx+w,ly+fh]);
}
function axesQ(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=Object.assign({},opt||{});
  /* a rotated y-axis title is drawn at b.x - 40 and is about 13 px wide, so
     on a narrow panel it reaches into the NEIGHBOUR's tick gutter (the known
     trap: y-tick labels hang ~28 px left of their own panel).  Below 215 px
     of panel the title is dropped and the panel's own name carries the units. */
  if(o.ylab&&b.w<215) o.ylab=null;
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
  const xt=o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  const yt=o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||5);
  for(const t of xt){
    const X=b.x+b.w*(t-xlo)/(xhi-xlo||1);
    if(X<b.x-0.5||X>b.x1+0.5) continue;
    regText(X,b.y1+5,o.xfmt?o.xfmt(t):fmt(t,2),10.5,'center','top');
  }
  for(const t of yt){
    const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1);
    if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    regText(b.x-6,Y,o.yfmt?o.yfmt(t):fmt(t,2),10.5,'right','middle');
  }
  if(o.xlab) regText(b.x+b.w/2,b.y1+21,o.xlab,11,'center','top');
  if(o.ylab){ const hw=plain(o.ylab).length*11*0.26;
    LABELS.push([b.x-53,b.y+b.h/2-hw,b.x-40,b.y+b.h/2+hw]); }
}

/* The number line's y, and the dot stack's row height, are each computed in
   TWO places: the drawing and the pointer hit test.  They drifted once
   already — the hit test kept b.y1-22 after the drawing moved to
   b.y1-NL_BELOW, so the prediction thumbs were grabbable 54 px below where
   they were drawn — so both now come from here and nowhere else. */
function nlLineY(b){ return b.y1-NL_BELOW; }
/* how much room each view leaves above its tallest stack */
const DOT_HEADROOM={kicks:10,meanmed:30,spread:34,conv:60,balance:40,longrun:10};
function dotGeomOf(b,xs,view){
  const map=nlMap(b), ly=nlLineY(b);
  const stacks=cavStacks(xs), hMax=Math.max(1,cavStackHeight(xs));
  const avail=Math.max(14,ly-b.y-(DOT_HEADROOM[view]===undefined?10:DOT_HEADROOM[view]));
  const rowH=Math.min(12,avail/hMax);
  return {map,ly,stacks,hMax,rowH,r:Math.min(5.2,rowH*0.44),top:ly-rowH*hMax};
}
function nlMap(b){
  return {b,
    X:v=>b.x+b.w*(v-XLO)/(XHI-XLO),
    V:px=>XLO+(px-b.x)/b.w*(XHI-XLO),
    s:b.w/(XHI-XLO)};
}
/* the stage: a field on top (where the balls land) and the plot under it
   (the same data, with the measures drawn on it) */
function plotWantH(maxK){ return NL_BELOW+12*Math.max(5,maxK)+46; }
/* the field needs only the height its tallest stack occupies: a box three
   times taller than its content reads as a defect, not as headroom (found
   by looking at the PNGs).  The dot plot takes whatever is left, because
   THAT is where the stack grows as the kicks arrive. */
function fieldWantH(xs){ return 62+13*Math.max(1,cavStackHeight(xs))+18; }
function cavLayout(ctx,W,H,capFull,capShort,fieldFrac,gapIn,fieldWant,plotWant){
  const narrow=isNarrow(W);
  const left=58, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(280,Math.min(W-148,right-left));
  const top=stageTop()+30;
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+200);
  const avail=Math.max(120,fit.capY-24-top);
  const gap=gapIn===undefined?30:gapIn;
  const fh=fieldWant?Math.round(clamp(fieldWant,110,avail*0.5))
                    :Math.round(avail*fieldFrac);
  /* the dot plot needs the band under the line plus room for the TALLEST
     stack the kick limit allows; more than that is dead space, and the two
     boxes are centred in whatever is left rather than pinned to the top */
  const phWant=plotWant?Math.round(clamp(plotWant,150,avail-fh-gap)):(avail-fh-gap);
  const topShift=Math.round(Math.max(0,avail-fh-gap-phWant)*0.45);
  /* the caption is drawn LAST but occupies its space from the start, so it
     goes into the label registry now — otherwise every panel note lands on
     top of it, which is what the layout sweep found at all four sizes */
  const capLines=wrapText(ctx,fit.txt,capW,CAP_FONT).length;
  LABELS.push([left,fit.capY,left+capW,fit.capY+capLines*14]);
  /* a two-column bottom row collapses below ~430 px of column and its axis
     titles then land in the caption and under the #hint (the known trap).
     `room` says whether the analysis views may draw their second row at all;
     when they may not, the main panel takes the whole stage and the canvas
     says what was dropped. */
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,gap,
          room:!narrow&&(avail-fh-gap)>=150,
          field:box(left,top+topShift,right-left,fh),
          plot:box(left,top+topShift+fh+gap,right-left,Math.max(110,phWant)),
          full:box(left,top,right-left,avail)};
}
function cavCaption(ctx,L){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); }

/* ---- the field ---------------------------------------------------------- */
/* The kicker stands at the left edge and the balls land at their distance and
   stack.  The arc is a DRAWING DEVICE: PhET draws the kick distance from the
   kicker's weights first and then animates a ball to it, so nothing about the
   flight enters any statistic — said on the canvas, not only here. */
/* the field's geometry, computed WITHOUT drawing, so that the hit test and
   the picture cannot drift apart (waveguides Known-bad: a quantity computed
   independently in the drawing and in the camera fit will drift) */
function fieldGeomOf(b,xs){
  const map=nlMap(b), gy=b.y1-16;
  const rowH=Math.min(13,Math.max(6,(gy-b.y-44)/Math.max(1,cavStackHeight(xs))));
  return {map,gy,rowH,br:Math.min(6.5,rowH*0.46),stacks:cavStacks(xs)};
}
function drawField(ctx,b,M,st,W,H){
  const G=fieldGeomOf(b,M.xs);
  const map=G.map, gy=G.gy;
  ctx.fillStyle=COL.sky; ctx.fillRect(b.x,b.y,b.w,b.h);
  ctx.fillStyle=COL.grass; ctx.fillRect(b.x,gy,b.w,b.y1-gy);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(b.x,gy+0.5); ctx.lineTo(b.x1,gy+0.5); ctx.stroke();
  /* the yard lines: one per metre of PHYSICAL_RANGE */
  ctx.strokeStyle='rgba(90,200,224,.16)'; ctx.lineWidth=1;
  for(let v=CAV.VMIN;v<=CAV.VMAX;v++){
    const X=map.X(v);
    ctx.beginPath(); ctx.moveTo(X,gy); ctx.lineTo(X,gy-6); ctx.stroke();
  }
  /* the kicker */
  const kx=map.X(0)+10, r=9;
  ctx.fillStyle=M.kcol;
  ctx.fillRect(kx-6,gy-24,12,16);
  dot(ctx,kx,gy-30,6,M.kcol,'#0b0f1a',1);
  ctx.strokeStyle=M.kcol; ctx.lineWidth=2.2;
  ctx.beginPath(); ctx.moveTo(kx-3,gy-8); ctx.lineTo(kx-7,gy); ctx.moveTo(kx+3,gy-8); ctx.lineTo(kx+9,gy-3); ctx.stroke();
  /* the balls that have landed, stacked where they landed */
  const stacks=G.stacks, rowH=G.rowH, br=G.br;
  for(let i=0;i<M.xs.length;i++){
    const X=map.X(M.xs[i]), Y=gy-rowH*(stacks[i]+0.5);
    const grabbed=(DRAG.what==='ball'&&DRAG.idx===i);
    dot(ctx,X,Y,br,grabbed?COL.live:COL.ball,'#0b0f1a',1);
  }
  /* the balls in flight */
  for(const ball of M.F.air){
    const p=cavBallPos(ball);
    dot(ctx,map.X(p[0]),gy-p[1]*map.s,br,COL.ball,'#0b0f1a',1);
  }
  frame(ctx,b,'#1b2130');
  lab(ctx,W,H,b.x+8,b.y+12,
      'the arc is a drawing device — the distance is drawn from the kicker’s weights first, as PhET does',
      '#5d6578',SM_FONT,'left','middle');
  return G;
}
/* which landed ball is under the pointer, if any */
function ballAt(xs,G,x,y){
  let best=-1, bestD=1e9;
  for(let i=0;i<xs.length;i++){
    const X=G.map.X(xs[i]), Y=G.gy-G.rowH*(G.stacks[i]+0.5);
    const d=Math.hypot(x-X,y-Y);
    if(d<Math.max(G.br+5,10)&&d<bestD){ best=i; bestD=d; }
  }
  return best;
}

/* ---- the number line and the dot plot ----------------------------------- */
function drawNumberLine(ctx,b,title){
  const map=nlMap(b);
  ctx.fillStyle='rgba(10,12,18,.5)'; ctx.fillRect(b.x,b.y,b.w,b.h);
  frame(ctx,b,'#1b2130');
  const ly=nlLineY(b);
  ctx.strokeStyle=COL.line; ctx.lineWidth=1.4;
  ctx.beginPath(); ctx.moveTo(map.X(XLO),ly+0.5); ctx.lineTo(map.X(XHI),ly+0.5); ctx.stroke();
  ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='top';
  for(let v=CAV.VMIN;v<=CAV.VMAX;v++){
    const X=map.X(v);
    ctx.strokeStyle=COL.line; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(X,ly); ctx.lineTo(X,ly+5); ctx.stroke();
    ctx.fillStyle='#6f7789'; ctx.fillText(''+v,X,ly+NL_TICKLAB);
    regText(X,ly+NL_TICKLAB,''+v,10.5,'center','top');
  }
  if(title){ ctx.textAlign='left'; ctx.textBaseline='bottom';
    ctx.fillStyle='#aeb6c6'; ctx.font='italic 13px Georgia, serif';
    ctx.fillText(plain(title),b.x+2,b.y-4);
    LABELS.push([b.x+2,b.y-4-15,b.x+2+plain(title).length*6.8,b.y-4]); }
  return {map,ly};
}
/* the dot plot itself: one mark per kick, stacked at its value.  PhET offers
   a line plot (crosses) as an alternative in its preferences; both are here. */
function drawDots(ctx,geom,b,xs,plot,opt){
  const o=opt||{};
  const D=dotGeomOf(b,xs,o.view);
  const map=D.map, ly=D.ly, stacks=D.stacks, rowH=D.rowH, r=D.r;
  for(let i=0;i<xs.length;i++){
    const X=map.X(xs[i]), Y=ly-rowH*(stacks[i]+0.5);
    const hi=o.mark&&o.mark(i,xs[i]);
    if(plot==='line'){
      ctx.strokeStyle=hi||COL.pos; ctx.lineWidth=1.7;
      ctx.beginPath();
      ctx.moveTo(X-r,Y-r); ctx.lineTo(X+r,Y+r);
      ctx.moveTo(X-r,Y+r); ctx.lineTo(X+r,Y-r);
      ctx.stroke();
    } else {
      dot(ctx,X,Y,r,hi||COL.pos,'#0b0f1a',1);
    }
  }
  return D;
}
/* the cards PhET's Median screen sorts: the values in kick order, or sorted */
function drawCards(ctx,b,xs,sorted){
  const vals=sorted?cavSorted(xs):xs.slice();
  const n=vals.length;
  if(!n) return 0;
  const w=Math.min(34,(b.w-20)/Math.max(n,1)), hh=Math.min(30,b.h-8);
  const x0=b.x+10;
  ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='middle';
  /* the cards the median is resting on: the same indices
     getMedianObjectsFromSortedArray picks — one for odd n, two for even */
  const midSet={};
  if(sorted){
    const k=Math.floor((n-1)/2);
    midSet[k]=1; if(n%2===0) midSet[k+1]=1;
  }
  for(let i=0;i<n;i++){
    const X=x0+i*w, Y=b.y+4;
    const on=sorted&&midSet[i];
    ctx.fillStyle=on?'rgba(240,180,41,.22)':'rgba(16,19,27,.92)';
    ctx.fillRect(X,Y,w-3,hh);
    ctx.strokeStyle=on?COL.med:'#2a3040'; ctx.lineWidth=1;
    ctx.strokeRect(X+0.5,Y+0.5,w-4,hh-1);
    ctx.fillStyle=on?COL.med:'#cfd4de';
    ctx.fillText(''+vals[i],X+(w-3)/2,Y+hh/2);
    /* the card numerals go into the label registry too, or the row's own
       legend lands on them at the narrower canvas sizes */
    regText(X+(w-3)/2,Y+hh/2,''+vals[i],10.5,'center','middle');
  }
  return Object.keys(midSet).length;
}

/* ---- the measures, drawn on the line ------------------------------------ */
function downTriangle(ctx,x,y,s,col){
  ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-s,y-s*1.5); ctx.lineTo(x+s,y-s*1.5);
  ctx.closePath(); ctx.fillStyle=col; ctx.fill();
}
function upTriangle(ctx,x,y,s,col){
  ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-s,y+s*1.5); ctx.lineTo(x+s,y+s*1.5);
  ctx.closePath(); ctx.fillStyle=col; ctx.fill();
}
function medianMark(ctx,geom,v,col,label,W,H){
  if(v===null) return;
  const X=geom.map.X(v);
  ctx.strokeStyle=col; ctx.lineWidth=1.6; ctx.setLineDash([4,3]);
  ctx.beginPath(); ctx.moveTo(X,geom.ly); ctx.lineTo(X,geom.top0!==undefined?geom.top0:geom.ly-40); ctx.stroke();
  ctx.setLineDash([]);
  downTriangle(ctx,X,geom.ly-2,6,col);
  if(label) lab(ctx,W,H,X,geom.ly+NL_LAB,label,col,SM_FONT,'center','middle');
}
/* the mean drawn as what it is: a fulcrum under a beam, with the signed
   deviations as the loads.  The fulcrum sits at the computed mean — selfTest
   asserts the drawn x is the model's mean, not a separately computed one. */
function meanFulcrum(ctx,geom,mean,col,label,W,H){
  if(mean===null) return null;
  const X=geom.map.X(mean);
  upTriangle(ctx,X,geom.ly+2,7,col);
  ctx.strokeStyle=col; ctx.lineWidth=1.4; ctx.setLineDash([2,3]);
  ctx.beginPath(); ctx.moveTo(X,geom.ly); ctx.lineTo(X,geom.top0!==undefined?geom.top0:geom.ly-40); ctx.stroke();
  ctx.setLineDash([]);
  if(label) lab(ctx,W,H,X,geom.ly+NL_LAB2,label,col,SM_FONT,'center','middle');
  return X;
}
/* The two moments, drawn.  They are equal at the mean, so the two bars are
   the same length and the picture IS the identity.  Their scale is NOT the
   number line's — a moment is a sum of distances, not a distance — so the
   factor is returned and printed on the canvas, as the house requires of
   every scale distortion. */
function momentBars(ctx,geom,b,xs,mean){
  const Mm=cavMoments(xs,mean);
  const mx=geom.map.X(mean), y=geom.ly+NL_BAR;
  const room=Math.max(20,Math.min(mx-b.x-10,b.x1-mx-10));
  const sc=room/Math.max(Mm.neg,Mm.pos,1e-9);
  ctx.lineWidth=3.2;
  ctx.strokeStyle=COL.ref;
  ctx.beginPath(); ctx.moveTo(mx,y); ctx.lineTo(mx-Mm.neg*sc,y); ctx.stroke();
  ctx.strokeStyle=COL.mean;
  ctx.beginPath(); ctx.moveTo(mx,y); ctx.lineTo(mx+Mm.pos*sc,y); ctx.stroke();
  ctx.lineWidth=1.4; ctx.strokeStyle=COL.text;
  ctx.beginPath(); ctx.moveTo(mx,y-6); ctx.lineTo(mx,y+6); ctx.stroke();
  return {Mm,sc,y,mx};
}
/* PhET's prediction thumbs: the median one snaps to 0.5 m, the mean one is
   continuous.  Both are live markers, so both are magenta. */
function predictMark(ctx,geom,v,col,label,W,H,up){
  const X=geom.map.X(v);
  ctx.strokeStyle=col; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(X,geom.ly+(up?-2:2)); ctx.lineTo(X,geom.ly+(up?-22:22)); ctx.stroke();
  (up?downTriangle:upTriangle)(ctx,X,geom.ly+(up?-2:2),6,col);
  if(label) lab(ctx,W,H,X,geom.ly+(up?-32:NL_LAB),label,col,SM_FONT,'center','middle');
}

/* ================================================================== *
 *  view A — the kicks (PhET's Median screen)                          *
 * ================================================================== */
const KICKS_CAP_FULL='PhET&rsquo;s Median screen. A kicker sends balls to distances drawn from its own weights &mdash; every landing is an integer metre between 1 and 15, and balls that land together stack, which is what makes the field a dot plot already. Drag any ball along the line to move it; it snaps to a whole metre, as PhET&rsquo;s does. The median is the middle value of the sorted data, and with an even number of kicks it is the mean of the TWO middle values, so it can sit between the marks. Sort the cards to see which balls it is resting on.';
const KICKS_CAP_SHORT='PhET&rsquo;s Median screen: kicks stack into a dot plot, and the median is the middle of the sorted data &mdash; the mean of the two middles when the count is even.';
function viewKicks(ctx,W,H,M,st){
  /* the sorted cards live in the gap between the field and the plot, so the
     gap has to grow with them or the plot's own title lands on a card */
  const L=cavLayout(ctx,W,H,KICKS_CAP_FULL,KICKS_CAP_SHORT,0.50,st.mSort?62:30,fieldWantH(M.xs),plotWantH(M.maxK));
  drawField(ctx,L.field,M,st,W,H);
  const geom=drawNumberLine(ctx,L.plot,'kick distance (metres) &mdash; '+(st.mPlot==='line'?'line plot':'dot plot'));
  const d=drawDots(ctx,geom,L.plot,M.xs,st.mPlot,{view:'kicks'});
  geom.top0=d.top-6;
  if(st.mMedian&&M.stat.median!==null)
    medianMark(ctx,geom,M.stat.median,COL.med,'median '+fmt(M.stat.median,1)+' m',W,H);
  /* a sparse view has to say why it is sparse, or it reads as broken */
  if(!M.stat.n)
    lab(ctx,W,H,(L.plot.x+L.plot.x1)/2,geom.ly-26,
        'no kicks yet — there is no median to mark.  Press kick 1 or kick 5.',
        COL.dim,CAP_FONT,'center','middle');
  if(st.mPredict) predictMark(ctx,geom,st.mPredVal,COL.live,'your guess '+fmt(st.mPredVal,1),W,H,false);
  if(st.mSort&&M.xs.length){
    const cb=box(L.field.x,L.field.y1+4,L.field.w,24);
    drawCards(ctx,cb,M.xs,true);
    lab(ctx,W,H,cb.x+2,cb.y1+10,'sorted — the middle card'+(M.xs.length%2?'':'s')+' in gold',
        COL.med,SM_FONT,'left','middle');
  }
  cavCaption(ctx,L);
  return L;
}

/* ================================================================== *
 *  view B — mean and median (PhET's Mean & Median screen)             *
 * ================================================================== */
const MM_CAP_FULL='PhET&rsquo;s Mean &amp; Median screen. The same dot plot, with the mean drawn as what it is: the fulcrum of a beam loaded with the kicks. The two bars under the line are the moments: the total pull of the kicks below the mean, and of those above. They are equal exactly &mdash; that is what a balance point IS, and it is an identity rather than an approximation. They are drawn at their own scale, which the canvas prints, because a moment is a sum of distances and not a distance. Move one ball far out and watch the two statistics part company: the mean follows it at 1/n metres per metre, the median does not move at all once the ball has left the middle.';
const MM_CAP_SHORT='PhET&rsquo;s Mean &amp; Median screen: the mean as a fulcrum, the signed deviations as loads, and a median that ignores how far the far balls are.';
function viewMeanMed(ctx,W,H,M,st){
  const L=cavLayout(ctx,W,H,MM_CAP_FULL,MM_CAP_SHORT,0.44,30,fieldWantH(M.xs),plotWantH(M.maxK));
  drawField(ctx,L.field,M,st,W,H);
  const geom=drawNumberLine(ctx,L.plot,'kick distance (metres) &mdash; '+(st.aPlot==='line'?'line plot':'dot plot'));
  const d=drawDots(ctx,geom,L.plot,M.xs,st.aPlot,{view:'meanmed'});
  geom.top0=d.top-6;
  let mom=null;
  if(st.aMean&&M.stat.mean!==null&&M.stat.n) mom=momentBars(ctx,geom,L.plot,M.xs,M.stat.mean);
  if(st.aMedian&&M.stat.median!==null)
    medianMark(ctx,geom,M.stat.median,COL.med,'median '+fmt(M.stat.median,1),W,H);
  if(st.aMean&&M.stat.mean!==null)
    meanFulcrum(ctx,geom,M.stat.mean,COL.mean,'mean '+fmt(M.stat.mean,2),W,H);
  if(st.aPredMean) predictMark(ctx,geom,st.aPredMeanVal,COL.live,'mean guess '+fmt(st.aPredMeanVal,1),W,H,true);
  if(st.aPredMed) predictMark(ctx,geom,st.aPredMedVal,COL.live,'median guess '+fmt(st.aPredMedVal,1),W,H,false);
  /* letter subscripts are not safe on this canvas (the rasteriser's font has
     no full set), so the deviation sum is written with an ASCII subscript */
  if(mom){
    lab(ctx,W,H,L.plot.x+4,L.plot.y+13,
        'sum of (x_i − mean) = '+fmt(cavTorque(M.xs,M.stat.mean),12)+' m',
        COL.mean,SM_FONT,'left','middle');
    lab(ctx,W,H,mom.mx,geom.ly+NL_LAB2+16,
        'each side pulls '+fmt(mom.Mm.neg,3)+' m — equal, exactly  ·  the two bars are at 1 m = '
        +fmt(mom.sc,1)+' px, NOT the number line’s scale',
        COL.ref,SM_FONT,'center','middle');
  }
  cavCaption(ctx,L);
  return L;
}
