
/* ================================================================== *
 *  the beaker (PhET's Concentration screen) and the cuvette (its      *
 *  Beer's Law screen)                                                 *
 * ================================================================== */

const CAP_BEAKER='PhET’s Concentration screen. The beaker holds 1 L and the solute amount '
  +'runs to 7 mol, both PhET’s. The liquid’s colour is PhET’s own three-stop '
  +'interpolation against concentration, not a transmission calculation — the true colour '
  +'view works that out. Each falling grain carries exactly 1/200 mol, PhET’s '
  +'particlesPerMole, and its moles arrive when it lands; the flight itself is drawn, not '
  +'modelled. PhET makes round(max(1, 0.2 x 200 x dt)) of them a frame, which at 60 fps is '
  +'one — so the shaker really delivers 0.30 mol/s against its own nominal 0.20. Solid '
  +'appears the instant n/V passes the saturation point, with no kinetics.';
const CAP_BEAKER_S='1 L beaker, 0–7 mol of solute (PhET). Colour is PhET’s '
  +'interpolation; each grain is 1/200 mol and counts when it lands.';

/* The caption is drawn last but owns the bottom of the stage from the moment it is
   measured.  Registering its rectangle is what lets lab() dodge it; without this the
   collision sweep found ninety overlaps, every one of them something-over-the-caption. */
function noteCaption(rc,left,capY,capTxt,capW){
  const n=wrapText(rc,capTxt,capW,CAP_FONT).length;
  LABELS.push([left,capY,left+capW,capY+n*14]);
}

/* ---- the beaker's own coordinates -------------------------------------------------- */
function bkX(b,u){ return b.x+u*b.w; }
function bkY(b,v){ return b.y1-v*b.h; }
function bkFromCanvas(b,X,Y){ return {x:(X-b.x)/b.w, y:(b.y1-Y)/b.h}; }

function beakerLayout(rc,W,H,capFull,capShort){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-52;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+26;
  const fit=fitCaption(rc,W,H-HINT_H,capFull,capShort,capW,top+210);
  const floor=fit.capY-26;
  /* the apparatus is a block: 118 px of headroom for the shaker and the faucet, then a
     beaker of its own proportions centred in whatever is left, rather than a short one
     pinned to the bottom of a tall stage */
  const band=floor-top-118;
  const bw=clamp((right-left)*0.42,190,430);
  const bh=clamp(Math.min(bw*0.92,band),120,430);
  const bx=left+86;
  const by=top+118+Math.max(0,(band-bh)/2);
  const bk=box(bx,by,bw,bh);
  noteCaption(rc,left,fit.capY,fit.txt,fit.capW);
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,top,floor,bk,
          headroom:by-top};
}

function drawGlass(rc,b,fill,fillFrac,W,H){
  /* the liquid first, then the glass over it, so the walls read as glass */
  const hgt=Math.max(0,fillFrac*b.h);
  if(hgt>0.5){
    rc.fillStyle=fill;
    rc.fillRect(b.x+1,b.y1-hgt,b.w-2,hgt);
    rc.fillStyle='rgba(255,255,255,.10)';
    rc.fillRect(b.x+1,b.y1-hgt,b.w-2,Math.min(4,hgt));
  }
  rc.strokeStyle=COL.glass; rc.lineWidth=2;
  rc.beginPath();
  rc.moveTo(b.x,b.y); rc.lineTo(b.x,b.y1); rc.lineTo(b.x1,b.y1); rc.lineTo(b.x1,b.y);
  rc.stroke();
  /* the graduations: PhET's beaker is 1 L, marked every fifth */
  rc.strokeStyle='rgba(143,184,212,.55)'; rc.lineWidth=1;
  rc.font=SM_FONT; rc.fillStyle='#7f8ca0'; rc.textAlign='left'; rc.textBaseline='middle';
  for(let k=1;k<=5;k++){
    const y=b.y1-b.h*k/5;
    const wLine=(k===5)?20:12;
    rc.beginPath(); rc.moveTo(b.x1-wLine,y); rc.lineTo(b.x1,y); rc.stroke();
    if(k%1===0&&k!==0){
      const v=PHET.BEAKER_VOLUME*k/5;
      lab(rc,W,H,b.x1+5,y,ST.beakerUnits==='milliliters'?fmt(v*1000,0):fmt(v,1),
          '#7f8ca0',SM_FONT,'left','middle');
    }
  }
}

function drawPrecipitate(rc,b,M){
  if(!(M.precip>0)) return;
  const n=Math.min(260,M.nParts);
  /* dark, not the solute's own colour: a saturated solution IS the solute's own colour,
     so grains painted in it disappear into the liquid they are sitting in */
  const col=mix('#05070c',rgbCss(M.sol.maxRGB),0.28);
  const col2=mix('#ffffff',rgbCss(M.sol.maxRGB),0.45);
  const r=makeRngB(9271);
  const bedH=Math.min(b.h*0.30,6+Math.sqrt(n)*2.4);
  for(let i=0;i<n;i++){
    const u=0.03+0.94*r(), v=r();
    const X=bkX(b,u), Y=b.y1-2-v*bedH;
    const s=3.2;
    rc.fillStyle=(i%3===0)?col2:col;
    rc.fillRect(X-s/2,Y-s/2,s,s);
  }
}

function drawShakerParticles(rc,b,M){
  const col=rgbCss(M.sol.maxRGB);
  rc.fillStyle=col;
  for(const p of M.parts){
    const X=bkX(b,p.x), Y=bkY(b,p.y), s=4;
    rc.fillRect(X-s/2,Y-s/2,s,s);
  }
}

/* the shaker, above the beaker, in the SOLID form */
function drawShaker(rc,b,M,active,W,H){
  const cx=bkX(b,0.34), cy=b.y-64;
  rc.save();
  rc.translate(cx,cy); rc.rotate(-0.42);
  rc.fillStyle=active?'#2b3346':'#1b2130';
  rc.fillRect(-34,-13,68,26);
  rc.strokeStyle=active?COL.pos:'#39415a'; rc.lineWidth=1.5;
  rc.strokeRect(-34,-13,68,26);
  rc.fillStyle=rgbCss(M.sol.maxRGB);
  rc.fillRect(26,-9,10,18);
  rc.restore();
  lab(rc,W,H,cx-40,cy-24,'shaker — '+M.sol.formula,COL.dim,SM_FONT,'left','middle');
}
/* the dropper, above the beaker, in the SOLUTION form */
function drawDropper(rc,b,M,active,W,H){
  const cx=bkX(b,0.52), cy=b.y-70;
  rc.fillStyle='#1b2130'; rc.fillRect(cx-15,cy-26,30,40);
  rc.strokeStyle=active?COL.pos:'#39415a'; rc.lineWidth=1.5;
  rc.strokeRect(cx-15,cy-26,30,40);
  rc.fillStyle=rgbCss(schemeColor(M.sol.id,M.sol.stock));
  rc.fillRect(cx-11,cy-22,22,32);
  rc.fillStyle='#1b2130'; rc.fillRect(cx-5,cy+14,10,12);
  if(active){
    rc.fillStyle=rgbCss(schemeColor(M.sol.id,M.sol.stock));
    rc.fillRect(cx-2.5,cy+26,5,b.y1-b.h*M.fill-cy-26);
  }
  lab(rc,W,H,cx+22,cy-16,'dropper — '+fmt(M.sol.stock,1)+' mol/L stock',
      COL.dim,SM_FONT,'left','middle');
}
function drawFaucet(rc,b,M,on,side,W,H){
  const x=side==='in'?b.x-58:b.x1+54;
  const y=side==='in'?b.y-52:b.y1-14;
  const surf=b.y1-b.h*M.fill;
  if(side==='in'){
    /* a pipe from off-stage, a body, and a spout pointing down into the beaker */
    rc.fillStyle='#161c28'; rc.fillRect(0,y-8,x-26,12);
    rc.fillStyle='#1b2130'; rc.fillRect(x-26,y-12,40,20);
    rc.strokeStyle=on?COL.struct:'#39415a'; rc.lineWidth=1.5;
    rc.strokeRect(x-26,y-12,40,20);
    rc.fillStyle='#1b2130'; rc.fillRect(x+6,y-12,10,24);
    rc.strokeRect(x+6,y-12,10,24);
    if(on){
      rc.fillStyle='rgba(120,190,230,.55)';
      rc.fillRect(x+8,y+12,6,Math.max(0,surf-y-12));
    }
    lab(rc,W,H,x-26,y-24,'water 0.25 L/s',COL.dim,SM_FONT,'left','middle');
  } else {
    /* the drain leaves the beaker's floor and goes off to the right */
    rc.fillStyle='#161c28'; rc.fillRect(b.x1,y-3,x-26-b.x1,8);
    rc.fillStyle='#1b2130'; rc.fillRect(x-26,y-12,40,20);
    rc.strokeStyle=on?COL.struct:'#39415a'; rc.lineWidth=1.5;
    rc.strokeRect(x-26,y-12,40,20);
    if(on){
      rc.fillStyle=rgbCss(M.rgb);
      rc.fillRect(b.x1,y-1,x-26-b.x1,4);
      rc.fillRect(x-10,y+8,6,26);
    }
    lab(rc,W,H,x-20,y+38,'drain 0.25 L/s',COL.dim,SM_FONT,'left','middle');
  }
}
/* PhET's concentration meter: a body with a reading, and a probe on a wire */
function drawMeter(rc,b,M,W,H){
  const px=bkX(b,PROBE.x), py=bkY(b,PROBE.y);
  const bodyX=Math.min(b.x1+64,b.x1+64), bodyY=b.y+6;
  /* the wire, as an explicit polyline: bezierCurveTo is not in the display-list
     recorder, so a curve drawn with it records as nothing at all */
  rc.strokeStyle='#4c5570'; rc.lineWidth=1.6;
  rc.beginPath();
  rc.moveTo(px,py-26);
  for(let i=1;i<=12;i++){
    const t=i/12, u=1-t;
    rc.lineTo(u*u*u*px+3*u*u*t*px+3*u*t*t*(bodyX+10)+t*t*t*(bodyX+18),
              u*u*u*(py-26)+3*u*u*t*(py-70)+3*u*t*t*(bodyY+64)+t*t*t*(bodyY+40));
  }
  rc.stroke();
  /* the probe */
  rc.fillStyle=M.probeIn?'#2b3346':'#1b2130';
  rc.fillRect(px-7,py-26,14,26);
  rc.strokeStyle=M.probeIn?COL.pos:'#6a7490'; rc.lineWidth=1.5;
  rc.strokeRect(px-7,py-26,14,26);
  rc.fillStyle=M.probeIn?COL.pos:'#6a7490';
  rc.fillRect(px-3,py-4,6,4);
  /* the body */
  const bw2=104, bh2=46;
  rc.fillStyle='#10141d'; rc.fillRect(bodyX,bodyY,bw2,bh2);
  frame(rc,box(bodyX,bodyY,bw2,bh2),'#39415a');
  rc.font=SM_FONT; rc.fillStyle=COL.dim; rc.textAlign='left'; rc.textBaseline='top';
  rc.fillText('concentration',bodyX+7,bodyY+6);
  rc.font='italic 15px Georgia, serif';
  rc.fillStyle=M.probeIn?COL.pos:'#6a7490'; rc.textBaseline='middle';
  rc.fillText(M.probeIn?(ST.meterUnits==='molar'?fmt(M.reading,PHET.DEC_CONC)
                                                :fmt(M.reading,PHET.DEC_PERCENT))
                       :'—',bodyX+7,bodyY+30);
  rc.font=SM_FONT; rc.fillStyle=COL.dim;
  rc.fillText(ST.meterUnits==='molar'?'mol/L':'%',bodyX+68,bodyY+30);
  if(!M.probeIn)
    lab(rc,W,H,bodyX+bw2/2,bodyY+bh2+13,'probe out of the solution',COL.dim,SM_FONT,'center','middle');
}

function viewBeaker(rc,W,H,M){
  const B=M.B, L=beakerLayout(rc,W,H,CAP_BEAKER,CAP_BEAKER_S), b=L.bk;
  if(ST.form==='solid') drawShaker(rc,b,B,ST.shaking,W,H);
  else drawDropper(rc,b,B,ST.dropper,W,H);
  drawFaucet(rc,b,B,ST.faucet,'in',W,H);
  drawFaucet(rc,b,B,ST.drain,'out',W,H);
  drawGlass(rc,b,rgbCss(B.rgb),B.fill,W,H);
  drawPrecipitate(rc,b,B);
  drawShakerParticles(rc,b,B);
  drawMeter(rc,b,B,W,H);
  /* the evaporation tray under the beaker */
  if(ST.evap>0){
    rc.strokeStyle=COL.ref; rc.lineWidth=1.4;
    const surf=b.y1-b.h*B.fill;
    for(let k=0;k<5;k++){
      const x=bkX(b,0.18+0.16*k);
      rc.beginPath();
      rc.moveTo(x,surf-6);
      for(let i=1;i<=9;i++){
        const t=i/9;
        rc.lineTo(x+6*Math.sin(t*PI*2),surf-6-36*t);
      }
      rc.stroke();
    }
    lab(rc,W,H,bkX(b,0.5),b.y1-b.h*B.fill-52,'evaporating '+fmt(ST.evap,3)+' L/s',
        COL.ref,SM_FONT,'center','middle');
  }
  /* PhET's "Saturated!" flag, on a pad ABOVE the liquid: dark orange on a bright
     solution is unreadable, and over the grains it is worse */
  if(B.sat){
    const x=bkX(b,0.5), y=Math.max(b.y+16,b.y1-b.h*B.fill-16);
    rc.fillStyle='rgba(10,12,18,.82)'; rc.fillRect(x-48,y-11,96,22);
    frame(rc,box(x-48,y-11,96,22),'#3a2a18');
    rc.font='italic 14px Georgia, serif'; rc.textAlign='center'; rc.textBaseline='middle';
    rc.fillStyle=COL.solid; rc.fillText('Saturated!',x,y);
  }
  /* the two optional readouts PhET puts on the beaker */
  if(ST.showAmount)
    lab(rc,W,H,bkX(b,0.5),b.y-16,'Solute Amount: '+fmt(B.grams,0)+' g',COL.pos,LAB_FONT,'center','middle');
  if(ST.showVolume)
    lab(rc,W,H,b.x-10,bkY(b,B.fill),volPlain(B.V),COL.struct,LAB_FONT,'right','middle');
  /* the numbers, as a strip to the right of the meter -- only where there is room for
     it, which at 560 px of stage there is not */
  const SW=156;
  const sx=b.x1+64, sy=b.y+78;
  if(sx+SW<=W-8&&sy+7*16<L.floor){
    const rows=[['n, solute',molStr(B.n),COL.pos],
                ['V, solution',volPlain(B.V),COL.struct],
                ['C = n/V',fmt(B.C,3)+' mol/L',COL.pos],
                ['C sat',fmt(B.cs,2)+' mol/L',COL.ref],
                ['solid',B.precip>0?fmt(B.precip,3)+' mol':'none',COL.solid],
                ['mass %',fmt(B.percent,1)+' %',COL.dim]];
    rows.forEach((r,i)=>{
      const y=sy+i*16;
      lab(rc,W,H,sx,y,r[0],COL.dim,SM_FONT,'left','middle');
      lab(rc,W,H,sx+SW,y,plain(r[1]),r[2],SM_FONT,'right','middle');
    });
    const gy=sy+rows.length*16+10;
    rc.fillStyle=COL.off; rc.fillRect(sx,gy,SW,7);
    rc.fillStyle=COL.pos; rc.fillRect(sx,gy,SW*clamp(B.n/PHET.SOLUTE_MOL_MAX,0,1),7);
    lab(rc,W,H,sx,gy+18,'solute, of PhET’s 7 mol ceiling',COL.dim,SM_FONT,'left','middle');
  }
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}

