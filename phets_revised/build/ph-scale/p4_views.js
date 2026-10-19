
/* ================================================================== *
 *  the beaker apparatus, and the three views every build carries:     *
 *  THE BEAKER (PhET's Macro screen), DILUTION and THE SCALE           *
 *  Canvas strings are ASCII for the ion formulae — a superscript plus *
 *  and a letter subscript are tofu in the rasteriser's font (BRIEF).  *
 * ================================================================== */
const LBL_H3O='H3O+', LBL_OH='OH-', LBL_H2O='H2O';

/* a caption under a panel, drawn only if it clears the main caption */
function capUnder(ctx,x,y,txt,w,limitY){
  const ls=wrapText(ctx,txt,w,SM_FONT).length;
  if(y+ls*14>limitY) return 0;
  return caption(ctx,x,y,txt,w,'#767e92',SM_FONT);
}
/* axesR registers the TITLE box only, so a label placed under a panel lands on the axis
   title of the x axis instead — which is how "pH" ended up inside "the lines cross at
   pH 7" at 1400 x 820.  Register the x-axis label too, and everything placed with lab()
   dodges it. */
function axesRX(ctx,b,xlo,xhi,ylo,yhi,opt){
  axesR(ctx,b,xlo,xhi,ylo,yhi,opt);
  if(opt&&opt.xlab){
    const t=plain(opt.xlab), w=t.length*11*0.52, cx=b.x+b.w/2;
    LABELS.push([cx-w/2,b.y1+21,cx+w/2,b.y1+21+11*1.15]);
  }
}

/* ---- the stage ------------------------------------------------------------------- */
function beakerLayout(ctx,W,H,capFull,capShort,wantStrip){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+180);
  const availH=Math.max(160,fit.capY-18-top);
  const span=right-left;
  const apH=Math.min(150,Math.max(64,availH*0.26));      /* the dropper / faucet band */
  /* the pH strip is part of the LAYOUT, not an afterthought squeezed underneath: sized
     from what was left over it never fitted at any stage size at all, and the view
     simply lost it */
  const strip=(wantStrip&&availH>=300)?STRIP_H+26:0;
  /* PhET's beaker is 450 x 300, so this one keeps that 1.5 aspect rather than filling
     whatever box is left: taken from the leftover height alone it came out 600 x 420 at
     1400 x 820 and read as a tank.  The block is then centred in what is left over. */
  /* the meter's width comes OUT of the span before the beaker is sized: taken from what
     was left over it was placed at right - 140 and sat on top of the glass at 560 x 380 */
  const meterW=Math.max(110,Math.min(190,span*0.20));
  const room=Math.max(160,span-meterW-26);
  const maxW=Math.min(room,760);
  let bh=Math.min(availH-apH-12-strip,400);
  let bw=bh*1.5;
  if(bw>maxW){ bw=maxW; bh=bw/1.5; }
  bh=Math.max(90,bh);
  const bx=left+Math.max(0,(room-bw)/2);
  const blockH=apH+12+bh+strip;
  const y0=top+Math.max(0,(availH-blockH)/2);
  const bk=box(bx,y0+apH+12,bw,bh);
  const meter=box(Math.min(bk.x1+22,right-meterW),bk.y,meterW,bh);
  return {narrow,left,right,top,span,apH,bk,meter,
          stripY:strip?bk.y1+20:null,
          capY:fit.capY,capTxt:fit.txt,capW};
}
/* beaker-local (x across, y up from the floor) -> canvas */
function bkX(bk,x){ return bk.x+bk.w*x; }
function bkY(bk,y){ return bk.y1-bk.h*y; }
function bkFromCanvas(bk,X,Y){ return {x:(X-bk.x)/bk.w, y:(bk.y1-Y)/bk.h}; }

function drawBeaker(ctx,bk,M,W,H){
  const fillH=bk.h*clamp(M.vT/PHET.BEAKER_VOLUME,0,1);
  /* the liquid */
  if(M.vT>0){
    ctx.fillStyle=rgbCss(M.rgb);
    ctx.fillRect(bk.x+2,bk.y1-fillH,bk.w-4,fillH);
    /* a lighter meniscus line so a pale liquid still reads as liquid */
    ctx.fillStyle='rgba(255,255,255,.22)';
    ctx.fillRect(bk.x+2,bk.y1-fillH,bk.w-4,2);
  }
  /* the glass: three sides, open at the top */
  ctx.strokeStyle=COL.glass; ctx.lineWidth=2.5; ctx.lineJoin='round';
  ctx.beginPath();
  ctx.moveTo(bk.x+0.5,bk.y); ctx.lineTo(bk.x+0.5,bk.y1-0.5);
  ctx.lineTo(bk.x1-0.5,bk.y1-0.5); ctx.lineTo(bk.x1-0.5,bk.y);
  ctx.stroke();
  /* volume ticks every 0.2 L, on the inside of the right wall */
  ctx.strokeStyle='rgba(143,184,212,.55)'; ctx.lineWidth=1;
  ctx.font=SM_FONT; ctx.fillStyle='#7f8ba0'; ctx.textAlign='right'; ctx.textBaseline='middle';
  const every=bk.h>170?0.2:0.6;
  for(let k=1;k*0.2<=PHET.BEAKER_VOLUME+1e-9;k++){
    const v=k*0.2, y=bk.y1-bk.h*v/PHET.BEAKER_VOLUME;
    const big=Math.abs(v/every-Math.round(v/every))<1e-9;
    ctx.beginPath(); ctx.moveTo(bk.x1-1,y); ctx.lineTo(bk.x1-(big?17:10),y); ctx.stroke();
    if(big) ctx.fillText(fmt(v,1),bk.x1-21,y);
  }
  ctx.textAlign='left'; ctx.textBaseline='middle';
  ctx.fillText('L',bk.x1-18,bk.y+10);
  /* the tick labels and the L are raw fillText, so lab() cannot see them and has pushed
     a note straight on top of them; register the gutter as occupied */
  LABELS.push([bk.x1-44,bk.y,bk.x1,bk.y1]);
  lab(ctx,W,H,bk.x+9,bk.y1-7,
      M.vT>0?(plain(M.sol.name)+', '+fmt(M.vT,2)+' L'):'empty',
      M.vT>0?'#0c1020':'#7f8ba0',LAB_FONT,'left','bottom');
}
/* the dropper above the beaker, and the water faucet beside it */
function drawApparatus(ctx,L,M,W,H){
  const bk=L.bk, yTop=L.top, yBot=bk.y;
  const xd=bk.x+bk.w*0.26, xw=bk.x+bk.w*0.74;
  /* the dropper: a bulb and a tube, filled with the stock colour */
  const bulbR=Math.min(17,L.apH*0.22), tubeW=Math.max(9,bulbR*0.72);
  const stock=rgbCss(M.sol.stock);
  ctx.fillStyle=stock;
  dot(ctx,xd,yTop+bulbR+4,bulbR,stock,'#cfd4de',1.6);
  ctx.fillRect(xd-tubeW/2,yTop+bulbR+4,tubeW,yBot-24-(yTop+bulbR+4));
  ctx.strokeStyle='#cfd4de'; ctx.lineWidth=1.4;
  ctx.strokeRect(xd-tubeW/2,yTop+bulbR+4,tubeW,yBot-24-(yTop+bulbR+4));
  if(ST.pourSolute&&!M.full){
    ctx.fillStyle=stock;
    ctx.fillRect(xd-tubeW*0.22,yBot-24,tubeW*0.44,24+bk.h*(1-clamp(M.vT/PHET.BEAKER_VOLUME,0,1)));
  }
  /* the water faucet: a pipe that reaches the spout it feeds (drawn from the beaker's
     right wall it was a floating bar with nothing under it) and the spout itself */
  ctx.fillStyle='#39404f';
  ctx.fillRect(xw-9,yTop+6,Math.max(20,L.right-xw+9),12);
  ctx.fillRect(xw-9,yTop+6,18,22);
  ctx.strokeStyle='#5c6577'; ctx.lineWidth=1.2;
  ctx.strokeRect(xw-9,yTop+6,18,22);
  if(ST.pourWater&&!M.full){
    ctx.fillStyle=rgbCss(WATER_RGB);
    ctx.globalAlpha=0.75;
    ctx.fillRect(xw-5,yTop+28,10,bk.y1-bk.h*clamp(M.vT/PHET.BEAKER_VOLUME,0,1)-(yTop+28));
    ctx.globalAlpha=1;
  }
  lab(ctx,W,H,xd,yTop+bulbR*2+14,plain(M.sol.name),'#aeb6c6',SM_FONT,'center');
  lab(ctx,W,H,xw,yTop+34,'water','#aeb6c6',SM_FONT,'center');
  /* the drain, out of the bottom left */
  ctx.fillStyle='#39404f';
  ctx.fillRect(bk.x-26,bk.y1-12,26,10);
  if(ST.drain&&M.vT>0){
    ctx.fillStyle=rgbCss(M.rgb);
    ctx.fillRect(bk.x-26,bk.y1-2,8,Math.min(46,H-bk.y1));
  }
  lab(ctx,W,H,bk.x-28,bk.y1-18,'drain','#7f8ba0',SM_FONT,'right');
}
/* PhET's pH meter: a body with the reading, a wire, and a probe you drag */
function drawMeter(ctx,L,M,W,H){
  const m=L.meter, bk=L.bk;
  /* three stacked lines, laid out from the top: the name, the reading and (only when
     there is room for it) the "probe is out" note.  Centring the reading and anchoring
     the note to the bottom put them on top of each other at every body under 82 px. */
  const bodyH=Math.max(50,Math.min(96,m.h*0.42));
  const b=box(m.x,m.y,m.w,bodyH);
  const room=bodyH>=70;
  ctx.fillStyle='#141a2b'; ctx.fillRect(b.x,b.y,b.w,b.h);
  ctx.strokeStyle='#4a5468'; ctx.lineWidth=1.4;
  ctx.strokeRect(b.x+0.5,b.y+0.5,b.w-1,b.h-1);
  ctx.font=SM_FONT; ctx.fillStyle='#7f8ba0'; ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillText('pH meter',b.x+8,b.y+6);
  ctx.font='italic '+(room?26:20)+'px Georgia, serif';
  ctx.fillStyle=M.probeIn?COL.pos:'#5c6577';
  ctx.fillText(M.probeIn?phPlain(M.ph):'—',b.x+8,b.y+21);
  if(!M.probeIn&&room){
    ctx.font=SM_FONT; ctx.fillStyle='#8b93a6';
    ctx.fillText('probe out of the liquid',b.x+8,b.y+54);
  }
  /* the wire and the probe */
  const px=bkX(bk,PROBE.x), py=bkY(bk,PROBE.y);
  ctx.strokeStyle='#5c6577'; ctx.lineWidth=1.6;
  ctx.beginPath();
  ctx.moveTo(b.x+4,b.y1);
  ctx.lineTo(b.x+4,b.y1+18); ctx.lineTo(px,b.y1+18); ctx.lineTo(px,py-16);
  ctx.stroke();
  ctx.fillStyle=M.probeIn?COL.live:'#5c6577';
  ctx.fillRect(px-5,py-16,10,16);
  ctx.beginPath(); ctx.moveTo(px-5,py-1); ctx.lineTo(px+5,py-1); ctx.lineTo(px,py+7);
  ctx.closePath(); ctx.fill();
  ctx.strokeStyle='#e9eef7'; ctx.lineWidth=1;
  ctx.strokeRect(px-5.5,py-16.5,11,16);
  return b;
}
/* the acidic / neutral / basic strip over PhET's whole -1..15 range.  The three WORDS
   live in the upper band and the NUMBERS in the lower one: written on one line they
   collided ("0" under "acidic" at every size, since pH 0 is a sixteenth of the way
   along).  The strip's own rectangle goes into the label registry, so nothing lab()
   places can be pushed down on top of it — which is how "spit 7.4" landed on
   "neutral" at 820 x 560. */
const STRIP_H=32;
function phStrip(ctx,b,mark){
  const lo=PHET.PH_MIN, hi=PHET.PH_MAX;
  const X=p=>b.x+b.w*(p-lo)/(hi-lo);
  for(let i=0;i<b.w;i++){
    const p=lo+(hi-lo)*i/b.w;
    ctx.fillStyle=p<7?mix(COL.acid,'#f3e9c0',clamp(p/7,0,1))
                     :mix('#f3e9c0',COL.base,clamp((p-7)/7,0,1));
    ctx.fillRect(b.x+i,b.y,1.4,b.h);
  }
  frame(ctx,b,'#2a3346');
  const words=b.h>=STRIP_H-2;
  if(words){
    ctx.textBaseline='top'; ctx.font='italic 12px Georgia, serif'; ctx.fillStyle='#0c1020';
    ctx.textAlign='left'; ctx.fillText('acidic',b.x+6,b.y+3);
    ctx.textAlign='right'; ctx.fillText('basic',b.x1-6,b.y+3);
    ctx.textAlign='center'; ctx.fillText('neutral',X(7),b.y+3);
  }
  ctx.font=SM_FONT; ctx.textAlign='center'; ctx.textBaseline='top';
  const numY=words?b.y+b.h-14:b.y+(b.h-12)/2;
  for(let p=0;p<=14;p+=1){
    const x=X(p);
    ctx.strokeStyle='rgba(12,16,32,.45)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(x,b.y1-4); ctx.lineTo(x,b.y1); ctx.stroke();
    if(p%2===0){ ctx.fillStyle='#0c1020'; ctx.fillText(''+p,x,numY); }
  }
  if(mark!==null&&mark!==undefined&&isFinite(mark)){
    const x=X(clamp(mark,lo,hi));
    ctx.strokeStyle=COL.live; ctx.lineWidth=2.4;
    ctx.beginPath(); ctx.moveTo(x,b.y-6); ctx.lineTo(x,b.y1+6); ctx.stroke();
  }
  LABELS.push([b.x,b.y,b.x1,b.y1]);
  return X;
}

/* ================================================================== *
 *  VIEW: the beaker — PhET's Macro screen                             *
 * ================================================================== */
const CAP_BEAKER='Pour a liquid from the dropper, run the tap to dilute it, open the drain, and drag the meter probe in and out. The beaker holds PhET’s 1.2 L and the dropper and faucets run at PhET’s 0.05 and 0.25 L/s. The colour is PhET’s own law: water to the liquid’s colour-stop shade over the first quarter of the mixture, then to its stock colour. The pH is computed by mixing MOLES of net strong acid and re-solving the water equilibrium, never by averaging the pH — the chip switches to PhET’s own rule so you can see the difference, which is at most 0.095 pH anywhere this beaker can reach.';
const CAP_BEAKER_S='Pour, dilute, drain, and drag the probe. The pH mixes moles of net strong acid and re-solves with Kw.';
function viewBeaker(rc,W,H,M){
  const B=M.B;
  const L=beakerLayout(rc,W,H,CAP_BEAKER,CAP_BEAKER_S,true);
  drawApparatus(rc,L,B,W,H);
  drawBeaker(rc,L.bk,B,W,H);
  drawMeter(rc,L,B,W,H);
  /* the strip under the beaker, with the beaker's own pH marked */
  if(L.stripY!==null){
    const sb=box(L.bk.x,L.stripY,Math.max(200,L.meter.x1-L.bk.x),STRIP_H);
    phStrip(rc,sb,B.probeIn?B.ph:null);
    if(!B.probeIn)
      lab(rc,W,H,sb.x+sb.w/2,sb.y-9,'dip the probe to read the scale','#767e92',SM_FONT,'center','bottom');
  }
  /* the honest note about the strong-acid model, on the canvas */
  lab(rc,W,H,L.bk.x,L.bk.y-8,
      'every liquid is modelled as a STRONG acid or base of PhET’s stated pH — no buffering',
      '#767e92',SM_FONT,'left','bottom');
  caption(rc,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  VIEW: dilution — the mixing law, three ways                        *
 * ================================================================== */
const CAP_DIL='The law on the left, its error on the right. What dilutes is not the pH and not either ion but C = [H3O+] − [OH-], the net strong acid: it is a difference of ANALYTICAL concentrations, so its moles are conserved and it volume-averages, and water carries exactly none of it. Dilute f-fold and C is divided by exactly f; the pH then follows by re-solving [H3O+] − Kw/[H3O+] = C. The dashed line is what you get by averaging the pH instead, which is wrong by up to 4.4 units. The right-hand panel is the WORST that exact minus PhET can be anywhere this beaker can reach — every dilution from 1 to 80 times, against the stock pH. It peaks at 0.0947 pH near 4.9 and 9.1 and is an ODD function about 7, because C(14−pH) = −C(pH) and PhET’s two branches mirror each other the same way.';
const CAP_DIL_S='C = [H3O+] − [OH-] is what dilutes. The dashed line averages the pH instead, and is wrong by units.';
function viewDilution(rc,W,H,M){
  const D=M.D;
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(rc,W,H-HINT_H,CAP_DIL,CAP_DIL_S,capW,top+200);
  /* 62 px below the plot box, not 30: the x-axis label sits at b.y1 + 21, and the note
     under the difference panel at b.y1 + 38, so a shallow gutter runs both of them into
     the first line of the caption at every size */
  const availH=Math.max(150,fit.capY-62-top);
  const span=right-left;
  const gut=narrow?0:64;
  const pw=narrow?span:(span-gut)*0.56;
  const A=box(left,top,pw,availH);
  const Bp=narrow?null:box(A.x1+gut,top,span-gut-pw,availH);

  /* --- the main panel: pH against dilution --- */
  const ylo=PHET.PH_MIN, yhi=PHET.PH_MAX;
  axesRX(rc,A,0,DIL_FMAX,ylo,yhi,{title:titleFor(A,'pH against dilution, '+plain(D.sol.name),'pH vs dilution'),
    xlab:'dilution factor V/V₀ (decades)',ylab:'pH',ny:5,
    xfmt:t=>Math.abs(t)<1e-9?'1':('10'+String(Math.round(t)).replace(/\d/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[+d]))});
  /* the band this beaker can actually reach */
  { const xr=A.x+A.w*Math.min(D.reach,DIL_FMAX)/DIL_FMAX;
    rc.fillStyle='rgba(90,200,224,.07)'; rc.fillRect(A.x,A.y,xr-A.x,A.h);
    rc.strokeStyle='rgba(90,200,224,.35)'; rc.lineWidth=1;
    rc.beginPath(); rc.moveTo(xr,A.y); rc.lineTo(xr,A.y1); rc.stroke(); }
  /* neutral */
  { const y=A.y1-A.h*(7-ylo)/(yhi-ylo);
    rc.strokeStyle='rgba(184,236,76,.30)'; rc.lineWidth=1;
    rc.setLineDash([4,4]); rc.beginPath(); rc.moveTo(A.x,y); rc.lineTo(A.x1,y); rc.stroke();
    rc.setLineDash([]); }
  polyline(rc,A,D.C.xs,D.C.avg,0,DIL_FMAX,ylo,yhi,'#8b6b4a',1.4,[5,4]);
  polyline(rc,A,D.C.xs,D.C.phet,0,DIL_FMAX,ylo,yhi,COL.ref,1.8);
  polyline(rc,A,D.C.xs,D.C.exact,0,DIL_FMAX,ylo,yhi,COL.pos,2.2);
  if(isFinite(D.cur)&&D.cur>=0)
    marker(rc,A,0,DIL_FMAX,ylo,yhi,clamp(D.cur,0,DIL_FMAX),
           clamp(D.phNow===null?7:D.phNow,ylo,yhi),COL.live);
  { const lb=legendAuto(rc,A,[[COL.pos,'exact: mix C, re-solve with Kw'],
                              [COL.ref,'PhET’s rule'],
                              ['#8b6b4a','averaging the pH (wrong)'],
                              [COL.live,'the beaker now']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]); }
  lab(rc,W,H,A.x+A.w*Math.min(D.reach,DIL_FMAX)/DIL_FMAX-6,A.y+14,
      'this beaker stops here ('+fmt(Math.pow(10,D.reach),0)+'×)',COL.struct,SM_FONT,'right');

  /* --- the difference panel --- */
  if(Bp){
    const ext=Math.max(0.02,D.worst*1.25);
    axesRX(rc,Bp,PHET.PH_MIN,PHET.PH_MAX,-ext,ext,
      {title:titleFor(Bp,'the worst exact − PhET this beaker can reach',
                      'worst exact − PhET'),
       xlab:'stock pH',ylab:'pH difference',ny:5,nx:5,
       yfmt:t=>fmt(t,3)});
    { const y=Bp.y1-Bp.h*(0-(-ext))/(2*ext);
      rc.strokeStyle='rgba(143,162,196,.30)'; rc.lineWidth=1;
      rc.beginPath(); rc.moveTo(Bp.x,y); rc.lineTo(Bp.x1,y); rc.stroke(); }
    { const x=Bp.x+Bp.w*(7-PHET.PH_MIN)/(PHET.PH_MAX-PHET.PH_MIN);
      rc.strokeStyle='rgba(184,236,76,.30)'; rc.lineWidth=1;
      rc.setLineDash([4,4]); rc.beginPath(); rc.moveTo(x,Bp.y); rc.lineTo(x,Bp.y1); rc.stroke();
      rc.setLineDash([]); }
    polyline(rc,Bp,D.dx,D.dy,PHET.PH_MIN,PHET.PH_MAX,-ext,ext,COL.ref,1.9);
    /* green: the worst this liquid can reach.  magenta: what the beaker is doing now,
       which is exactly zero when nothing has been diluted -- and saying so is the point */
    marker(rc,Bp,PHET.PH_MIN,PHET.PH_MAX,-ext,ext,D.sol.pH,clamp(D.envHere,-ext,ext),COL.pos);
    if(D.hereDiff!==null)
      marker(rc,Bp,PHET.PH_MIN,PHET.PH_MAX,-ext,ext,D.sol.pH,clamp(D.hereDiff,-ext,ext),COL.live);
    { const lb=legendAuto(rc,Bp,[[COL.ref,'worst over every dilution'],
                                 [COL.pos,'worst for '+plain(D.sol.name)],
                                 [COL.live,'the beaker now']]);
      if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]); }
    lab(rc,W,H,Bp.x+Bp.w*0.5,Bp.y1+38,
        'odd about pH 7 — worst '+fmt(D.worst,4)+' pH at stock pH '+fmt(D.worstPh,2),
        '#767e92',SM_FONT,'center','top');
  }
  caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
}

/* ================================================================== *
 *  VIEW: the scale — the twelve liquids, and the two ions             *
 * ================================================================== */
const CAP_SCALE='PhET’s twelve liquids on the scale they belong to, and underneath, the two concentrations that scale IS. One pH unit is a factor of ten in [H3O+] and a factor of ten the other way in [OH-], which is why the lower panel is two straight lines crossing at pH 7 — their product is fixed at Kw everywhere. The bars are MEASURED pH ranges: only four of the twelve could be sourced here (blood, orange juice, milk, chicken broth), and PhET’s value lies inside every one of them. The other eight carry PhET’s number alone and are drawn without a bar rather than given an invented range.';
const CAP_SCALE_S='The twelve liquids on the scale, and the two straight lines the scale is made of. Bars are sourced ranges; four of twelve.';
function viewScale(rc,W,H,M){
  const S=M.S||M.L;
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(rc,W,H-HINT_H,CAP_SCALE,CAP_SCALE_S,capW,top+200);
  /* 62 px below the lower plot: its x-axis label, and the sentence under that */
  const availH=Math.max(180,fit.capY-62-top);
  const span=right-left;
  /* three label lanes plus the strip plus the sourcing note: sized from what it HOLDS,
     not as a fraction of the stage — a fraction left a third of the picture empty */
  const stripH=3*16+14+STRIP_H+18;
  const A=box(left,top,span,stripH);
  const bh=availH-stripH-58;
  const Bp=bh>=90?box(left,A.y1+52,span,bh):null;

  /* --- the liquids on the strip --- */
  const sb=box(A.x,A.y+A.h-STRIP_H-2,A.w,STRIP_H);
  const X=phStrip(rc,sb,S.act&&S.act.ph!==null?S.act.ph:null);
  /* markers and labels above, alternating height so twelve fit */
  const order=S.rows.slice().sort((a,b)=>a.s.pH-b.s.pH);
  order.forEach((r,i)=>{
    const x=X(r.s.pH);
    const lane=i%3;
    const y=sb.y-14-lane*16;
    const on=r.s.id===ST.solute;
    if(r.s.range){
      const x0=X(r.s.range[0]), x1=X(r.s.range[1]);
      rc.strokeStyle=COL.ref; rc.lineWidth=3;
      rc.beginPath(); rc.moveTo(Math.min(x0,x-2),sb.y-4); rc.lineTo(Math.max(x1,x+2),sb.y-4);
      rc.stroke();
    }
    rc.strokeStyle=on?COL.pos:'#9aa2b4'; rc.lineWidth=on?1.8:1;
    rc.beginPath(); rc.moveTo(x,sb.y); rc.lineTo(x,y+4); rc.stroke();
    dot(rc,x,sb.y,on?4.5:3,rgbCss(r.s.stock),on?COL.pos:'#0c1020',1.4);
    lab(rc,W,H,x,y,plain(r.s.name)+' '+fmt(r.s.pH,r.s.pH===Math.round(r.s.pH)?0:1),
        on?COL.pos:'#aeb6c6',SM_FONT,'center','bottom');
  });
  lab(rc,W,H,A.x,sb.y-14-3*16-4,'orange bars: MEASURED ranges, '+S.sourced+' of '
      +SOLUTES.length+' sourced — the rest carry PhET’s value alone',
      COL.ref,SM_FONT,'left','bottom');

  /* --- the two straight lines.  At a stage too short for a second panel the view drops
     it and says so, rather than drawing an unreadable sliver (Known-bad: a sparse view
     is not a broken one, but it must say why). --- */
  if(!Bp){
    lab(rc,W,H,left,A.y1+26,'too short for the concentration panel \u2014 widen the window',
        '#767e92',SM_FONT,'left','top');
    caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
    return;
  }
  const ylo=PHET.LOG_EXP_MIN, yhi=PHET.LOG_EXP_MAX;
  axesRX(rc,Bp,PHET.PH_MIN,PHET.PH_MAX,ylo,yhi,
    {title:titleFor(Bp,'the two concentrations, log scale (mol/L)','the two concentrations'),
     xlab:'pH',ylab:'log10 of the concentration',ny:5,nx:8,yfmt:t=>fmt(t,0)});
  const xs=[], yh=[], yo=[];
  for(let i=0;i<=80;i++){
    const p=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/80;
    xs.push(p); yh.push(-p); yo.push(p-PKW);
  }
  polyline(rc,Bp,xs,yh,PHET.PH_MIN,PHET.PH_MAX,ylo,yhi,COL.h3o,2.0);
  polyline(rc,Bp,xs,yo,PHET.PH_MIN,PHET.PH_MAX,ylo,yhi,COL.oh,2.0);
  { const yw=Math.log10(PHET.WATER_CONC), pts=[PHET.PH_MIN,PHET.PH_MAX];
    polyline(rc,Bp,pts,[yw,yw],PHET.PH_MIN,PHET.PH_MAX,ylo,yhi,COL.h2o,1.4,[6,4]); }
  if(S.act&&S.act.ph!==null){
    marker(rc,Bp,PHET.PH_MIN,PHET.PH_MAX,ylo,yhi,clamp(S.act.ph,PHET.PH_MIN,PHET.PH_MAX),
           clamp(-S.act.ph,ylo,yhi),COL.live);
  }
  { const lb=legendAuto(rc,Bp,[[COL.h3o,LBL_H3O],[COL.oh,LBL_OH],
                               [COL.h2o,LBL_H2O+', 55 mol/L']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]); }
  lab(rc,W,H,Bp.x+Bp.w*0.5,Bp.y1+38,
      'the lines cross at pH 7, where both are 1e-7 mol/L — one unit of pH is one decade',
      '#767e92',SM_FONT,'center','top');
  caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
}
