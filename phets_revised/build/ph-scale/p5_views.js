
/* ================================================================== *
 *  the views ph-scale carries and ph-scale-basics does not:           *
 *  THE PARTICLES and THE GRAPH (PhET's Micro screen) and MY SOLUTION  *
 * ================================================================== */

/* ---- the particles ---------------------------------------------------------------- */
const CAP_PART='PhET’s Micro screen: the same beaker, with the two ions drawn. The dot counts are PhET’s DRAWING rule and not a census — round(50 × concentration / 1e-7) inside pH 6 to 8, floored at five, and outside that window the minority ramps linearly to 3000 at the ends of the scale while the majority saturates. So the picture compresses: at pH 13 it draws 457 hydroxide for every hydronium where the true ratio is 1e12 to one, and the readout prints both numbers side by side. The counts that are real are the molecule counts, and they are enormous: a 1.2 L beaker of neutral water holds 7.23e16 hydronium ions.';
const CAP_PART_S='PhET’s particle picture. The dot counts are a drawing rule; the molecule counts beside them are real.';
function viewParticles(rc,W,H,M){
  const B=M.B;
  const L=beakerLayout(rc,W,H,CAP_PART,CAP_PART_S);
  drawApparatus(rc,L,B,W,H);
  drawBeaker(rc,L.bk,B,W,H);
  const bk=L.bk;
  if(B.ions){
    const d=B.dots;
    const fillH=bk.h*clamp(B.vT/PHET.BEAKER_VOLUME,0,1);
    /* keep a clear band at the foot of the glass: the volume label lives there and the
       dots are drawn after it, so they were scattered straight across it */
    const y0=bk.y1-fillH+6, y1=Math.max(bk.y1-fillH+8,bk.y1-26), x0=bk.x+6, x1=bk.x1-24;
    /* seeded from the counts, so the same solution always draws the same scatter */
    DOT_RNG.seed((d.h*7919+d.o*104729+1)>>>0);
    const r=clamp(Math.min(bk.w,bk.h)*0.012,1.4,3.4);
    const drawN=(n,col,stroke)=>{
      const m=Math.min(n,600);           /* a cap on the STROKES, printed on the canvas */
      for(let i=0;i<m;i++){
        const x=x0+(x1-x0)*DOT_RNG.next(), y=y0+(y1-y0)*DOT_RNG.next();
        dot(rc,x,y,r,col,stroke,0.8);
      }
      return m;
    };
    const mh=drawN(d.h,H3O_RGB,'rgba(249,210,194,.7)');
    const mo=drawN(d.o,OH_RGB,'rgba(0,0,0,.6)');
    /* above the liquid the background is the PAGE, not the solution, so this note has to
       be light: drawn in the liquid's own dark ink it was invisible */
    if(mh<d.h||mo<d.o)
      lab(rc,W,H,bk.x,bk.y-24,'the dots are capped at 600 each here ('+d.h+' and '+d.o
          +' called for)','#767e92',SM_FONT,'left','bottom');
    if(ST.ratio)
      lab(rc,W,H,bk.x+bk.w/2,bk.y1-fillH/2,d.h+' / '+d.o,'#0c1020',
          'italic 22px Georgia, serif','center');
    if(ST.counts){
      lab(rc,W,H,bk.x+8,bk.y1-fillH-10,
          LBL_H3O+' '+sciPlain(B.nH,2)+'   '+LBL_OH+' '+sciPlain(B.nO,2)
          +'   '+LBL_H2O+' '+sciPlain(B.nW,2),'#aeb6c6',SM_FONT,'left','bottom');
    }
    /* the two ratios, always, MAJORITY per minority so a base does not read "0.00 : 1" */
    lab(rc,W,H,bk.x,bk.y-8,
        'drawn '+fmt(B.drawnRatio,2)+' : 1   —   true '+sciPlain(B.trueRatio,3)
        +' : 1   ('+B.majName+' per '+B.minName+')',
        COL.ref,SM_FONT,'left','bottom');
  } else {
    lab(rc,W,H,bk.x+bk.w/2,bk.y+bk.h/2,'the beaker is empty — pour a liquid',
        '#7f8ba0',LAB_FONT,'center');
  }
  drawMeter(rc,L,B,W,H);
  caption(rc,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}

/* ---- the graph -------------------------------------------------------------------- */
const CAP_GRAPH='PhET’s concentration graph. The logarithmic scale spans its own eighteen decades, from 1e-16 to 100, because that is the only way to put the hydroxide in battery acid and the water it is dissolved in on the same axis. Switch to the linear scale and the point makes itself: whichever ion is in the minority disappears, and so does the water unless the exponent is wound right up. The two ions move in opposite directions, exactly one decade for one unit of pH, and their product never leaves Kw. Switching the units to moles multiplies everything by the volume, which moves all three bars together and changes nothing about their ratios.';
const CAP_GRAPH_S='PhET’s concentration graph, eighteen decades on the log scale. The linear scale makes the point by failing.';
function viewGraph(rc,W,H,M){
  const A=M.A;
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(rc,W,H-HINT_H,CAP_GRAPH,CAP_GRAPH_S,capW,top+200);
  /* room under the box for the species names, the product line and the caption */
  const availH=Math.max(160,fit.capY-66-top);
  const span=right-left;
  const gw=Math.min(span*(narrow?0.96:0.52),availH*1.1);
  const G=box(left+20,top,gw,availH);

  const logs=ST.scaleKind==='log';
  /* On the LINEAR scale the axis is drawn in units of 10^linExp -- PhET's own 0..8
     mantissa -- so the tick labels stay short.  A tick label wider than 34 px reaches
     the rotated y-axis title, which axes() puts at b.x - 40 and which no registry can
     see, and "4.0e-14" is 38 px wide.  The scale factor is printed in the axis title,
     as the house rule requires. */
  const lo=logs?PHET.LOG_EXP_MIN:0;
  const hi=logs?PHET.LOG_EXP_MAX:PHET.LIN_MANTISSA_MAX;
  const unit=logs?1:Math.pow(10,ST.linExp);
  const val=c=>{
    if(c===null||!isFinite(c)) return null;
    const q=ST.units==='moles'?c*(A.v||0):c;
    return logs?(q>0?Math.log10(q):null):q/unit;
  };
  const uname=ST.units==='moles'?'moles':'mol/L';
  axesRX(rc,G,0,3,lo,hi,{title:titleFor(G,
      logs?('each species, logarithmic, '+uname)
          :('each species, linear, '+uname+' in units of 1e'+fmt(ST.linExp,0)),
      logs?'logarithmic':('linear, 1e'+fmt(ST.linExp,0))),
    ylab:logs?('log10 of the '+uname):(uname+' / 1e'+fmt(ST.linExp,0)), nx:0, ny:logs?6:5,
    xticks:[], yfmt:t=>fmt(t,logs?0:1)});
  const species=[[LBL_H3O,A.h,COL.h3o],[LBL_OH,A.o,COL.oh],[LBL_H2O,PHET.WATER_CONC,COL.h2o]];
  const bw=G.w/(species.length*2);
  species.forEach((sp,i)=>{
    const cx=G.x+G.w*(i+0.5)/species.length;
    const v=val(sp[1]);
    let yTop, off=false;
    if(v===null){ yTop=G.y1; }
    else if(v>hi){ yTop=G.y+0.02*G.h; off=true; }
    else if(v<lo){ yTop=G.y1; off=true; }
    else yTop=G.y1-G.h*(v-lo)/(hi-lo);
    rc.fillStyle=sp[2];
    rc.globalAlpha=0.82;
    rc.fillRect(cx-bw/2,yTop,bw,G.y1-yTop);
    rc.globalAlpha=1;
    rc.strokeStyle=sp[2]; rc.lineWidth=1.4;
    rc.strokeRect(cx-bw/2+0.5,yTop+0.5,bw-1,Math.max(1,G.y1-yTop-1));
    if(off){
      rc.fillStyle=COL.ref;
      rc.beginPath(); rc.moveTo(cx-7,G.y+12); rc.lineTo(cx+7,G.y+12); rc.lineTo(cx,G.y+2);
      rc.closePath(); rc.fill();
      lab(rc,W,H,cx,G.y+26,'off scale',COL.ref,SM_FONT,'center');
    }
    lab(rc,W,H,cx,G.y1+16,sp[0],sp[2],LAB_FONT,'center','top');
    const q=sp[1]===null?null:(ST.units==='moles'?sp[1]*(A.v||0):sp[1]);
    lab(rc,W,H,cx,Math.max(G.y+40,Math.min(yTop-10,G.y1-8)),
        q===null?'—':sciPlain(q,2),'#cfd4de',SM_FONT,'center','bottom');
  });
  /* the product, which is the whole point of the picture */
  if(A.h!==null&&A.o!==null&&G.y1+52<fit.capY)
    lab(rc,W,H,G.x+G.w/2,G.y1+38,
        LBL_H3O+' x '+LBL_OH+' = '+sciPlain(A.h*A.o,4)+' = Kw, at every pH',
        COL.pos,SM_FONT,'center','top');

  /* the beaker beside it, small, so the graph is attached to something */
  if(!narrow&&M.B){
    const bw2=Math.min(right-G.x1-40,availH*0.62);
    if(bw2>110){
      const bh2=Math.min(availH*0.7,bw2/1.2);
      const bk=box(G.x1+34,top+(availH-bh2)/2,bw2,bh2);
      drawBeaker(rc,bk,M.B,W,H);
      lab(rc,W,H,bk.x+bk.w/2,bk.y-10,
          A.from==='my'?'my solution':'the beaker','#767e92',SM_FONT,'center','bottom');
    }
  }
  caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
}

/* ---- my solution ------------------------------------------------------------------ */
const CAP_MY='PhET’s third screen, with the constraint drawn. Set the pH and the volume; nothing is being mixed, so the two concentrations follow straight from [H3O+] = 10^-pH and [OH-] = Kw/[H3O+]. The right-hand panel is the whole of that in one line: on log-log axes the water equilibrium is a straight line of slope −1, and every solution that can exist at 25 °C lies on it. Moving the pH slides the marker along the line and cannot leave it. The diagonal is the locus pH + pOH = 14, the dot where it crosses the diagonal of equality is neutral water, and the far ends are PhET’s pH −1 and 15.';
const CAP_MY_S='Set the pH; the two concentrations follow. On log-log axes the Kw constraint is a straight line of slope −1.';
function viewMy(rc,W,H,M){
  const m=M.M;
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(rc,W,H-HINT_H,CAP_MY,CAP_MY_S,capW,top+200);
  const availH=Math.max(170,fit.capY-48-top);
  const span=right-left;
  /* the Kw panel is dropped by WIDTH, not by isNarrow(): at 820 x 560 the stage is
     "narrow" and still has 400 px to spare, and dropping the panel there left the view
     drawing three rectangles and one stroke */
  /* the gutter has to clear the Kw panel's ROTATED y-axis title, which axes() draws 53 px
     to the left of the box and which no registry can see: at 26 px it reached back into
     the pH strip and the strip's "14" landed inside "log10 [OH-]" */
  const gut=narrow?58:54;
  const lw=(span-gut)*0.42;
  const pw=span-gut-lw;
  const showP=pw>=230;
  /* the same 1.5 aspect as the Macro beaker, and room ABOVE it for the pH strip, which
     was being asked for at a y above the stage top and so never drawn at all */
  let bh=Math.min(availH-STRIP_H-30,360);
  let bw=bh*1.5;
  const maxW=showP?lw:span*0.6;
  if(bw>maxW){ bw=maxW; bh=bw/1.5; }
  bh=Math.max(90,bh);
  /* centre the strip-plus-beaker-plus-label block in the column rather than pinning it to
     the top, which left half the left-hand side empty at 1400 x 820 */
  const blockH=STRIP_H+14+bh+26;
  const y0=top+Math.max(0,(availH-blockH)/2);
  const bk=box(left+((showP?lw:span)-bw)/2,y0+STRIP_H+14,bw,bh);

  /* the beaker: PhET draws My Solution's as water, which is what it is */
  const fillH=bk.h*clamp(m.v/PHET.BEAKER_VOLUME,0,1);
  rc.fillStyle=rgbCss(WATER_RGB);
  rc.fillRect(bk.x+2,bk.y1-fillH,bk.w-4,fillH);
  rc.fillStyle='rgba(255,255,255,.22)'; rc.fillRect(bk.x+2,bk.y1-fillH,bk.w-4,2);
  rc.strokeStyle=COL.glass; rc.lineWidth=2.5; rc.lineJoin='round';
  rc.beginPath();
  rc.moveTo(bk.x+0.5,bk.y); rc.lineTo(bk.x+0.5,bk.y1-0.5);
  rc.lineTo(bk.x1-0.5,bk.y1-0.5); rc.lineTo(bk.x1-0.5,bk.y);
  rc.stroke();
  rc.font='italic 30px Georgia, serif'; rc.fillStyle='#0c1020';
  rc.textAlign='center'; rc.textBaseline='middle';
  rc.fillText('pH '+phPlain(m.ph),bk.x+bk.w/2,bk.y1-Math.max(fillH/2,18));
  lab(rc,W,H,bk.x+bk.w/2,bk.y1+16,volStr(m.v)+' — '+CLS_NAME[m.cls],'#aeb6c6',LAB_FONT,'center','top');
  { const sb=box(bk.x,bk.y-STRIP_H-6,bk.w,STRIP_H);
    if(sb.y>=top-4) phStrip(rc,sb,m.ph); }

  /* the Kw line, log-log */
  if(showP){
    const P=box(left+lw+gut,top,pw,availH-26);
    const lo=PHET.LOG_EXP_MIN, hi=PHET.LOG_EXP_MAX;
    axesRX(rc,P,lo,hi,lo,hi,{title:titleFor(P,'the water equilibrium, log-log','[OH-] vs [H3O+]'),
      xlab:'log10 [H3O+]  (mol/L)',ylab:'log10 [OH-]  (mol/L)',nx:5,ny:5,
      xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
    const xs=[lo,hi], ys=[-PKW-lo,-PKW-hi];
    polyline(rc,P,xs,ys,lo,hi,lo,hi,COL.pos,2.2);
    /* the line of equality, which meets it at neutral */
    polyline(rc,P,[lo,hi],[lo,hi],lo,hi,lo,hi,'rgba(143,162,196,.45)',1.2,[5,4]);
    marker(rc,P,lo,hi,lo,hi,-7,-7,COL.struct);
    marker(rc,P,lo,hi,lo,hi,clamp(Math.log10(m.h),lo,hi),clamp(Math.log10(m.o),lo,hi),COL.live);
    /* the long form reaches the y-tick gutter on a panel under 300 px, and axes() draws
       its tick labels outside any registry, so the note carries a short form */
    lab(rc,W,H,P.x+P.w*0.5,P.y+16,P.w<300?'log[H3O+] + log[OH-] = −14'
        :'log[H3O+] + log[OH-] = −14 everywhere on the line',COL.pos,SM_FONT,'center');
    lab(rc,W,H,P.x+P.w*0.5,P.y1-12,'the dot at (−7, −7) is neutral water',
        COL.struct,SM_FONT,'center','bottom');
  } else {
    lab(rc,W,H,left,bk.y1+34,'too narrow for the Kw panel — widen the window',
        '#767e92',SM_FONT,'left','top');
  }
  caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
}
