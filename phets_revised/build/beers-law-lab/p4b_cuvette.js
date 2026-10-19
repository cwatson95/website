
/* ================================================================== *
 *  the cuvette (PhET's Beer's Law screen).  Built only into           *
 *  beers-law-lab.html: concentration.html has no light source.        *
 * ================================================================== */
/* ---- the cuvette ------------------------------------------------------------------- */
const CAP_CUVETTE='PhET’s Beer’s Law screen, drawn to scale: the bench is in '
  +'centimetres and the cuvette is as wide as the number beside it. The beam’s colour is '
  +'the wavelength’s own, and its brightness past the cuvette is the transmittance, so the '
  +'picture and the reading are the same number. A = εlc and T = 10^-A exactly; '
  +'ε is looked up at one value per nanometre and never interpolated.';
const CAP_CUVETTE_S='Beer’s Law screen to scale. Beam brightness past the cuvette IS the '
  +'transmittance. A = εlc, T = 10^-A, ε per nanometre.';

function cuvetteLayout(rc,W,H){
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-52;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+26;
  const fit=fitCaption(rc,W,H-HINT_H,CAP_CUVETTE,CAP_CUVETTE_S,capW,top+200);
  const floor=fit.capY-40;
  const BENCH_CM=8.4;                     /* how much of the bench is drawn, in cm */
  const CUV0=2.2;                         /* where the cuvette's LEFT face sits on it */
  const px=clamp((right-left-40)/BENCH_CM,26,120);
  const x0=left+24;                       /* the bench's own zero, in canvas x */
  const axis=Math.round((top+floor)/2)-14;        /* the beam axis */
  noteCaption(rc,left,fit.capY,fit.txt,fit.capW);
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,top,floor,
          px,x0,axis,BENCH_CM,CUV0,
          X:cm=>x0+cm*px, cmOf:X=>(X-x0)/px};
}
function viewCuvette(rc,W,H,M){
  const C=M.C, L=cuvetteLayout(rc,W,H);
  const axis=L.axis, px=L.px;
  const hCuv=Math.min(190,Math.max(70,(L.floor-L.top)*0.50));
  const xL=L.X(L.CUV0), xR=L.X(L.CUV0+C.l);
  const xSrc0=L.X(0.15), xSrc1=L.X(1.05);
  const beamHalf=Math.max(3,BEAM_HALF*px);
  const wave=rgbCss(C.wave);
  /* the source */
  rc.fillStyle='#161c28'; rc.fillRect(xSrc0,axis-26,xSrc1-xSrc0,52);
  frame(rc,box(xSrc0,axis-26,xSrc1-xSrc0,52),C.on?COL.struct:'#39415a');
  rc.fillStyle=C.on?wave:'#2a3040';
  rc.fillRect(xSrc1-8,axis-beamHalf,8,2*beamHalf);
  lab(rc,W,H,xSrc0,axis+40,C.on?'source '+fmt(C.lam,0)+' nm':'source off',
      C.on?COL.struct:COL.dim,SM_FONT,'left','middle');
  /* the cuvette's own colour goes down FIRST: the beam has to be drawn ON it, or the
     one thing this view exists to show is painted over */
  rc.fillStyle=mix('#070b18',rgbCss(C.rgb),0.92);
  rc.fillRect(xL,axis-hCuv/2,xR-xL,hCuv);
  /* the beam in, through, and out.  The run before the glass is a real centimetre and a
     bit, so the brightness the cuvette takes out of it has something to be compared with */
  if(C.on){
    rc.fillStyle=wave;
    rc.globalAlpha=0.78;
    rc.fillRect(xSrc1,axis-beamHalf,xL-xSrc1,2*beamHalf);
    rc.globalAlpha=1;
    /* inside the cuvette the beam dies off exponentially -- drawn in 24 slabs, each with
       the transmittance of the depth it sits at, which is the same 10^-eps l c the
       detector reads */
    const NS=24;
    for(let i=0;i<NS;i++){
      const d0=C.l*i/NS, d1=C.l*(i+1)/NS;
      const t=transmittance(absorbance(C.eps,(d0+d1)/2,C.c));
      rc.globalAlpha=0.78*clamp(t,0.02,1);
      rc.fillStyle=wave;
      rc.fillRect(L.X(L.CUV0+d0),axis-beamHalf,L.X(d1)-L.X(d0)+0.6,2*beamHalf);
    }
    rc.globalAlpha=0.78*clamp(C.T,0.02,1);
    rc.fillStyle=wave;
    rc.fillRect(xR,axis-beamHalf,L.X(L.BENCH_CM)-xR,2*beamHalf);
    rc.globalAlpha=1;
  }
  /* the glass itself, over the fill and the beam */
  rc.strokeStyle=COL.glass; rc.lineWidth=2;
  rc.beginPath();
  rc.moveTo(xL,axis-hCuv/2); rc.lineTo(xL,axis+hCuv/2);
  rc.lineTo(xR,axis+hCuv/2); rc.lineTo(xR,axis-hCuv/2);
  rc.stroke();
  /* the draggable right wall */
  rc.fillStyle=DRAG.what==='cuvette'?COL.live:COL.glass;
  rc.fillRect(xR-3,axis-hCuv/2-10,6,20);
  rc.fillRect(xR-3,axis+hCuv/2-10,6,20);
  lab(rc,W,H,(xL+xR)/2,axis+hCuv/2+16,'l = '+fmt(C.l,2)+' cm — drag the right wall',
      COL.glass,LAB_FONT,'center','middle');
  /* the detector: a probe on a wire into a body */
  const dx=L.X(L.CUV0+DET.x), dy=axis-DET.y*px;
  const sensor=Math.max(8,SENSOR_HALF*px);
  /* an explicit polyline, for the same reason the meter's wire is one */
  rc.strokeStyle='#4c5570'; rc.lineWidth=1.6;
  rc.beginPath();
  rc.moveTo(dx,dy+sensor);
  { const x3=L.X(L.BENCH_CM)-40, y3=L.floor-26, x2=L.X(L.BENCH_CM)-50, y2=L.floor-40;
    for(let i=1;i<=12;i++){
      const t=i/12, u=1-t;
      rc.lineTo(u*u*u*dx+3*u*u*t*dx+3*u*t*t*x2+t*t*t*x3,
                u*u*u*(dy+sensor)+3*u*u*t*(dy+sensor+52)+3*u*t*t*y2+t*t*t*y3);
    } }
  rc.stroke();
  rc.fillStyle=C.inBeam&&C.on?'#2b3346':'#1b2130';
  rc.fillRect(dx-9,dy-sensor,18,2*sensor);
  rc.strokeStyle=(C.inBeam&&C.on)?COL.pos:'#6a7490'; rc.lineWidth=1.6;
  rc.strokeRect(dx-9,dy-sensor,18,2*sensor);
  const bodyX=Math.min(W-152,L.X(L.BENCH_CM)-44), bodyY=L.floor-58;
  rc.fillStyle='#10141d'; rc.fillRect(bodyX,bodyY,126,50);
  frame(rc,box(bodyX,bodyY,126,50),'#39415a');
  rc.font=SM_FONT; rc.fillStyle=COL.dim; rc.textAlign='left'; rc.textBaseline='top';
  rc.fillText(C.det==='absorbance'?'absorbance':'transmittance',bodyX+7,bodyY+6);
  rc.font='italic 17px Georgia, serif'; rc.textBaseline='middle';
  rc.fillStyle=C.reading===null?'#6a7490':COL.pos;
  rc.fillText(C.reading===null?'—'
              :(C.det==='absorbance'?fmt(C.A,PHET.DEC_A):fmt(100*C.T,PHET.DEC_T)),
              bodyX+7,bodyY+31);
  if(C.reading!==null&&C.det!=='absorbance'){
    rc.font=SM_FONT; rc.fillStyle=COL.dim; rc.fillText('%',bodyX+66,bodyY+33);
  }
  if(C.reading===null)
    /* above the body, not below it: below is the bench ruler */
    lab(rc,W,H,bodyX+63,bodyY-11,C.on?'probe is out of the beam':'the light is off',
        COL.dim,SM_FONT,'center','middle');
  /* the bench ruler, so the centimetres are visible rather than asserted */
  const ry=L.floor+6;
  rc.strokeStyle='#39415a'; rc.lineWidth=1;
  rc.beginPath(); rc.moveTo(L.X(0),ry); rc.lineTo(L.X(L.BENCH_CM),ry); rc.stroke();
  rc.font=SM_FONT; rc.fillStyle='#6f7789'; rc.textAlign='center'; rc.textBaseline='top';
  for(let k=0;k<=Math.floor(L.BENCH_CM);k++){
    const x=L.X(k);
    rc.beginPath(); rc.moveTo(x,ry); rc.lineTo(x,ry+5); rc.stroke();
    rc.fillText(''+k,x,ry+7);
  }
  lab(rc,W,H,L.X(0),ry+27,'centimetres, '+fmt(px,0)+' px each',COL.dim,SM_FONT,'left','middle');
  /* the arithmetic, written out where the beam is */
  const ax=L.left, ay=L.top+4;
  const lines=[['A = eps l c',COL.pos],
               ['  = '+fmt(C.eps,3)+' × '+fmt(C.l,2)+' × '+sciPlain(C.c,3)
                +' = '+fmt(C.A,4),COL.pos],
               ['T = 10^-A = '+fmt(100*C.T,3)+' %',COL.struct],
               ['eps at '+fmt(C.lam,0)+' nm'+(C.atMax?' (the peak)':''),COL.dim]];
  lines.forEach((r,i)=>{ lab(rc,W,H,ax,ay+i*15,r[0],r[1],LAB_FONT,'left','middle'); });
  if(C.beyondLinear)
    lab(rc,W,H,ax,ay+lines.length*15+6,
        'c is past 10 mM: a real solution stops being linear there',COL.ref,SM_FONT,'left','middle');
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}
