
/* ================================================================== *
 *  the analysis views: the spectrum, the law, the ledger, the         *
 *  solutes and the true colour                                        *
 * ================================================================== */

/* The shared axes() is given a tick COUNT, and one count cannot serve a 1400 px stage
   and a 560 px one: six y labels in a 90 px panel overlap each other.  axesFit() derives
   both counts from the panel's own size, and drops the x tick sitting exactly on the left
   edge -- the y label at that same corner is a pixel away from it, and a 1 px graze is a
   visible antialiased smear, not a rounding (Known-bad, wave_fronts). */
function axesFit(rc,b,xlo,xhi,ylo,yhi,opt){
  const o={};
  for(const k in (opt||{})) o[k]=opt[k];
  const xa=Math.min(xlo,xhi), xb=Math.max(xlo,xhi);
  const ya=Math.min(ylo,yhi), yb=Math.max(ylo,yhi);
  if(!o.xticks){
    const t=ticksFor(xa,xb,b.w<210?3:(b.w<360?4:6));
    const span=Math.abs(xhi-xlo)||1;
    const f=t.filter(v=>Math.abs(v-xlo)>1e-9*span);
    o.xticks=f.length?f:t;
  }
  if(!o.yticks) o.yticks=ticksFor(ya,yb,b.h<110?3:(b.h<180?4:5));
  axesR(rc,b,xlo,xhi,ylo,yhi,o);
}

/* legendAuto() dodges data curves and nothing else, so every legend in the collection
   is free to land on a label that lab() has already placed (Known-bad, pupil_plane).
   legendFit() tests the SAME corner list against both registries and then records its own
   text rectangle, so whatever is drawn afterwards dodges the legend in turn.  It is drawn
   after the curves, because the curve registry is what picks the corner. */
function legendFit(rc,b,items){
  rc.font='10.5px -apple-system, sans-serif';
  let w=0;
  for(const it of items) w=Math.max(w,rc.measureText(plain(it[1])).width);
  const bw=w+26, bh=items.length*15+8;
  const mx=b.x+(b.w-bw)/2, my=b.y+(b.h-bh)/2;
  const cands=[[b.x1-bw-8,b.y+8],[b.x+8,b.y1-bh-8],[b.x+8,b.y+8],
               [b.x1-bw-8,b.y1-bh-8],[mx,b.y+8],[mx,b.y1-bh-8],
               [b.x+8,my],[b.x1-bw-8,my]];
  for(const [cx,cy] of cands){
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4){
      const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
      if(Math.max(x0,x1)<cx||Math.min(x0,x1)>cx+bw||
         Math.max(y0,y1)<cy||Math.min(y0,y1)>cy+bh) continue;
      hit=true;
    }
    if(!hit) for(const o of LABELS)
      if(cx+22<o[2]-0.5&&cx+bw>o[0]+0.5&&cy<o[3]-0.5&&cy+bh>o[1]+0.5){ hit=true; break; }
    if(!hit){ legendBox(rc,cx,cy,items); LABELS.push([cx+22,cy,cx+bw,cy+bh]); return true; }
  }
  return false;                       /* nowhere clear: draw none rather than a lying one */
}

/* the house stage layout, with the bottom line kept clear of the HTML hint
   (build/wave-on-a-string/, Known-bad) */
function layoutPanels(rc,W,H,capFull,capShort,nBottom,bottomFrac){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+30;
  const fit=fitCaption(rc,W,H-HINT_H,capFull,capShort,capW,top+220);
  const avail=fit.capY-16-top;
  const nB=narrow?Math.min(1,nBottom):nBottom;
  noteCaption(rc,left,fit.capY,fit.txt,fit.capW);
  const out={narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,bottom:[]};
  /* with no bottom row the main panel runs to the caption, and its x tick labels and axis
     name hang 21 px BELOW its box -- so the box has to stop short of them */
  let mainH=avail-30;
  if(nB>0){
    const rowH=Math.max(86,Math.floor(avail*bottomFrac));
    mainH=avail-rowH-58;
    const gut=54, span=right-left, w=(span-gut*nB)/nB;
    for(let i=0;i<nB;i++)
      out.bottom.push(box(left+gut+i*(w+gut),fit.capY-18-rowH+10,w,rowH-34));
  }
  out.main=box(left,top,right-left,Math.max(80,mainH));
  return out;
}

/* ---------------------------------------------------------------- the ledger --------- */
const CAP_LEDGER='The beaker as bookkeeping. Every mole that goes in or out is counted, and '
  +'the residual printed beside the bars is what does not balance — it is zero, to the '
  +'last bit of a double, and the Python twin closes the same ledger exactly in rationals. '
  +'The drain is the one worth watching: it removes SOLUTION, so it carries solute away at '
  +'the dissolved concentration min(C, C sat) and leaves the solid on the bottom. The curve '
  +'is C = n/V with the moles held fixed, which is exactly what evaporating does: a '
  +'hyperbola up to the saturation volume n/C sat, flat after it, and the difference falls '
  +'out as solid.';
const CAP_LEDGER_S='Moles in minus moles out is what is in the beaker, to the last bit. '
  +'Evaporating follows C = n/V up to V = n/C sat, then C is pinned and solid appears.';

function waterfall(rc,p,rows,unit,W,H){
  let hi=0;
  for(const r of rows) hi=Math.max(hi,Math.abs(r[1]));
  hi=Math.max(hi,1e-6)*1.25;
  const n=rows.length, bw=Math.min(46,(p.w-14)/n-8);
  rc.font=SM_FONT;
  const zero=p.y1-14;
  rc.strokeStyle='#2a3040'; rc.lineWidth=1;
  rc.beginPath(); rc.moveTo(p.x,zero); rc.lineTo(p.x1,zero); rc.stroke();
  const colW=(p.w-14)/n;
  rows.forEach((r,i)=>{
    const x=p.x+10+i*colW;
    /* 22 px of headroom: the value label sits above the bar and the panel's note above
       that, and a full-height bar used to push one into the other */
    const hgt=(Math.abs(r[1])/hi)*(zero-p.y-22);
    rc.fillStyle=r[3];
    if(r[1]>=0) rc.fillRect(x,zero-hgt,bw,hgt);
    else rc.fillRect(x,zero,bw,Math.min(hgt,p.y1-zero-1));
    /* through lab(), so a tall bar's value dodges the panel note above it rather than
       landing on it at 560 x 380 */
    lab(rc,W,H,x+bw/2,(r[1]>=0?zero-hgt-9:zero+hgt+7),fmt(Math.abs(r[1]),3),r[3],
        SM_FONT,'center','middle');
    rc.textAlign='center'; rc.textBaseline='bottom';
    /* the key, truncated to the column it belongs to -- measured, not guessed */
    rc.fillStyle=COL.dim; rc.textBaseline='top';
    let key=plain(r[4]||r[0]);
    while(key.length>3&&rc.measureText(key).width>colW-6) key=key.slice(0,-1);
    rc.fillText(key,x+bw/2,p.y1-11);
  });
  lab(rc,W,H,p.x1-2,p.y+10,unit,COL.dim,SM_FONT,'right','middle');
}

function viewLedger(rc,W,H,M){
  const G=M.G, B=G.B, L=layoutPanels(rc,W,H,CAP_LEDGER,CAP_LEDGER_S,2,0.40);
  const b=L.main;
  const chi=Math.max(B.cs*1.35,0.2);
  axesFit(rc,b,0,PHET.VOL_MAX,0,chi,{
    title:'C = n/V as the volume changes, with n held at '+fmt(B.n,3)+' mol',
    xlab:'solution volume, L',ylab:'concentration, mol/L',
    xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,1)});
  /* the uncapped hyperbola, then the capped one the beaker actually reads */
  polyline(rc,b,G.vs,G.raw,0,PHET.VOL_MAX,0,chi,shade(COL.ref,0.55),1.2,[5,4]);
  polyline(rc,b,G.vs,G.C,0,PHET.VOL_MAX,0,chi,COL.pos,2.2);
  polyline(rc,b,[0,PHET.VOL_MAX],[B.cs,B.cs],0,PHET.VOL_MAX,0,chi,COL.ref,1.3,[4,4]);
  lab(rc,W,H,b.x1-4,b.y1-b.h*B.cs/chi-10,'C sat = '+fmt(B.cs,2)+' mol/L',
      COL.ref,LAB_FONT,'right','middle');
  if(B.n>0&&B.Vsat<PHET.VOL_MAX){
    const xv=b.x+b.w*B.Vsat/PHET.VOL_MAX;
    rc.strokeStyle=COL.solid; rc.lineWidth=1.2; rc.setLineDash([3,3]);
    rc.beginPath(); rc.moveTo(xv,b.y); rc.lineTo(xv,b.y1); rc.stroke(); rc.setLineDash([]);
    lab(rc,W,H,xv+5,b.y+30,'saturates at V = n/C sat = '+fmt(B.Vsat,4)+' L',
        COL.solid,SM_FONT,'left','middle');
  }
  if(B.V>0) marker(rc,b,0,PHET.VOL_MAX,0,chi,B.V,B.C,COL.live);
  legendFit(rc,b,[[COL.pos,'what the meter reads'],[shade(COL.ref,0.55),'n/V, uncapped'],
                   [COL.ref,'saturation']]);
  if(B.tSat!==null)
    lab(rc,W,H,b.x+8,b.y+14,'evaporating at '+fmt(ST.evap>0?ST.evap:PHET.EVAPORATION_MAX,3)
        +' L/s reaches it in '+fmt(B.tSat,2)+' s',COL.dim,SM_FONT,'left','middle');
  if(L.bottom[0]){
    const p=L.bottom[0];
    frame(rc,p,'#242a3a');
    lab(rc,W,H,p.x,p.y-11,'the mole ledger',COL.dim,'italic 13px Georgia, serif','left','bottom');
    /* the note costs the bars twelve pixels of headroom, which a 560 px stage has not
       got: there it is dropped and the readout carries the same two numbers */
    if(!isNarrow(W))
      lab(rc,W,H,p.x+6,p.y+12,'in beaker '+fmt(B.n,4)+' mol, residual '+sciPlain(B.resid.n,1),
          Math.abs(B.resid.n)>1e-12?COL.ref:COL.pos,SM_FONT,'left','middle');
    waterfall(rc,p,G.rows,'mol',W,H);
  }
  if(L.bottom[1]){
    const p=L.bottom[1];
    frame(rc,p,'#242a3a');
    lab(rc,W,H,p.x,p.y-11,'the volume ledger',COL.dim,'italic 13px Georgia, serif','left','bottom');
    if(!isNarrow(W))
      lab(rc,W,H,p.x+6,p.y+12,'in beaker '+fmt(B.V,4)+' L, residual '+sciPlain(B.resid.V,1),
          Math.abs(B.resid.V)>1e-12?COL.ref:COL.pos,SM_FONT,'left','middle');
    waterfall(rc,p,G.vrows,'L',W,H);
  }
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}

/* ---------------------------------------------------------------- true colour -------- */
const CAP_COLOUR='PhET’s colour is an interpolation between fixed stops; the row beside '
  +'it is what the solution actually transmits. T(λ) = 10^-(eps l c) '
  +'at every nanometre, integrated against the CIE 1931 2° observer on the same 1 nm '
  +'grid the spectra live on — nothing interpolated, nothing resampled — then '
  +'adapted so the illuminant itself renders exactly white, so an empty cuvette is '
  +'rgb(255,255,255). The gap is large, and it is not mainly brightness: PhET’s ramp '
  +'has no path length in it at all, so it cannot know the difference between a thin cuvette '
  +'and a thick one. Two illuminants are offered because no D65 spectrum could be sourced '
  +'offline; equal energy is flat by definition and illuminant A comes from the CIE’s '
  +'own formula.';
const CAP_COLOUR_S='PhET’s ramp against the transmitted colour: 10^-(eps l c)'
  +' per nanometre through the CIE observer, adapted so the illuminant is white.';

function viewColour(rc,W,H,M){
  const K=M.K, L=layoutPanels(rc,W,H,CAP_COLOUR,CAP_COLOUR_S,2,0.38);
  const b=L.main;
  frame(rc,b,'#242a3a');
  const n=K.sw.length, cw=b.w/n;
  /* laid out from what the panel HAS: two rows, their two headings, the tick numbers and
     the axis line under them all have to fit inside b, or the axis title is dropped */
  const rowH=clamp((b.h-106)/2,14,120);
  const yT=b.y+26, yP=yT+rowH+22;
  const yAxis=yP+rowH+5, roomForTitle=(yAxis+30<=b.y1);
  for(let i=0;i<n;i++){
    rc.fillStyle=rgbCss(K.sw[i].true_);
    rc.fillRect(b.x+i*cw,yT,cw+0.6,rowH);
    rc.fillStyle=rgbCss(K.sw[i].phet);
    rc.fillRect(b.x+i*cw,yP,cw+0.6,rowH);
  }
  frame(rc,box(b.x,yT,b.w,rowH),'#242a3a');
  frame(rc,box(b.x,yP,b.w,rowH),'#242a3a');
  lab(rc,W,H,b.x+4,yT-10,'what '+fmt(K.l,2)+' cm of it really transmits, under '
      +plain(K.illumName),COL.pos,LAB_FONT,'left','middle');
  lab(rc,W,H,b.x+4,yP-8,'PhET’s interpolation between its two stops',
      COL.ref,LAB_FONT,'left','middle');
  /* the concentration axis under the swatches */
  rc.font=SM_FONT; rc.fillStyle='#6f7789'; rc.textAlign='center'; rc.textBaseline='top';
  const nTick=b.w<320?3:5;
  for(let k=0;k<nTick;k++){
    const c=K.d.cMax*k/(nTick-1), x=b.x+b.w*k/(nTick-1);
    rc.fillText(fmt(c*K.d.scale,0),clamp(x,b.x+12,b.x1-12),yAxis);
  }
  if(roomForTitle)
    lab(rc,W,H,b.x+6,yAxis+21,'concentration, '+K.d.transform,COL.dim,LAB_FONT,'left','middle');
  /* the worst gap, marked */
  const xg=b.x+b.w*clamp(K.worstC/K.d.cMax,0,1);
  rc.strokeStyle=COL.live; rc.lineWidth=1.4;
  rc.beginPath(); rc.moveTo(xg,yT-4); rc.lineTo(xg,yP+rowH+4); rc.stroke();
  lab(rc,W,H,b.x1-4,roomForTitle?yAxis+21:b.y+12,
      'worst channel gap '+fmt(K.worst,0)+' of 255',COL.live,SM_FONT,'right','middle');
  /* where the beaker or the cuvette is now */
  const xh=b.x+b.w*clamp(K.c/K.d.cMax,0,1);
  rc.fillStyle=COL.live;
  rc.beginPath();
  rc.moveTo(xh,yT-16); rc.lineTo(xh-5,yT-24); rc.lineTo(xh+5,yT-24);
  rc.closePath(); rc.fill();
  if(L.bottom[0]){
    const p=L.bottom[0];
    axesFit(rc,p,LAM0,LAM1,0,1.05,{title:'T(λ) here, with the eye’s own weight',
      xlab:'nm',ylab:'T',xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
    polyline(rc,p,K.xs,K.ybar,LAM0,LAM1,0,1.05,shade(COL.eye,0.5),1.2,[4,3]);
    polyline(rc,p,K.xs,K.T,LAM0,LAM1,0,1.05,COL.pos,1.9);
    legendFit(rc,p,[[COL.pos,'T(λ)'],[shade(COL.eye,0.5),'y-bar(λ)']]);
  }
  if(L.bottom[1]){
    const p=L.bottom[1];
    const cs=K.sw.map(s=>s.c*K.d.scale), yt=K.sw.map(s=>s.Ytrue), yp=K.sw.map(s=>s.Yphet);
    axesFit(rc,p,0,K.d.cMax*K.d.scale,0,1.05,{title:'how much light is left',
      xlab:'concentration, '+K.d.transform,ylab:'relative',xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
    polyline(rc,p,cs,yt,0,K.d.cMax*K.d.scale,0,1.05,COL.pos,1.9);
    polyline(rc,p,cs,yp,0,K.d.cMax*K.d.scale,0,1.05,COL.ref,1.6,[5,4]);
    legendFit(rc,p,[[COL.pos,'transmitted, measured'],[COL.ref,'luminance of PhET’s swatch']]);
    marker(rc,p,0,K.d.cMax*K.d.scale,0,1.05,K.c*K.d.scale,K.here.Y,COL.live);
  }
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}
