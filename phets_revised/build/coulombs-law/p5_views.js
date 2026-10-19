
/* ================================================================== *
 *  captions                                                           *
 * ================================================================== */
const MACRO_CAP_FULL='PhET’s macro scale: two charged spheres 1.35 cm across on a 10-cm track, charges in microcoulombs. Drag either '
  +'charge, or the ruler; the sliders set the charges and positions. The green arrows are the force on each — equal and opposite, pointing '
  +'together for unlike charges and apart for like ones — drawn to the arrow scale printed below. Positions snap to PhET’s 1-mm grid, and '
  +'the centres never come closer than 1.4 cm (PhET rounds 13.5 + 1 mm down to 14 mm).';
const MACRO_CAP_SHORT='Drag the charges or the ruler. Green: the force on each, equal and opposite, to the printed arrow scale.';
const ATOMIC_CAP_FULL='PhET’s atomic scale: the same law with charges in units of e and distances in picometres, on a 100-pm track. Charge '
  +'comes only in whole multiples of e, so the sliders step by one. The balls are PhET’s 1.9-pm markers for point charges — a real ion is '
  +'a hundred times larger, a nucleus a thousand times smaller. The green arrows are the force on each, equal and opposite, to the printed '
  +'arrow scale; positions snap to PhET’s 1-pm grid.';
const ATOMIC_CAP_SHORT='Charges in e, distances in pm. Green: the force on each, equal and opposite, to the printed arrow scale.';
const INV_CAP_FULL='The force between the two charges against the distance between their centres, on the chosen scale. On log–log axes an '
  +'inverse-square law is a straight line of slope −2, whatever the charges or the units; the solid part is what PhET’s track allows, the '
  +'orange band the distances at which the balls would overlap, the paler band PhET’s gap. Lower left: the same force on linear axes. '
  +'Lower right: |F| r², flat at |k q₁q₂| — the dashed curve is an inverse-cube law through the same point.';
const INV_CAP_SHORT='|F| against r: slope −2 on log–log axes; |F| r² stays flat at |k q₁q₂|.';
const PROD_CAP_FULL='Every pair of charges on the chosen scale, at the current distance. Like signs repel (the upper-right and lower-left '
  +'quadrants), unlike signs attract, and on either axis one charge is zero and there is no force at all. |F| = (k/r²)|q₁q₂|, so each '
  +'contour of equal force is a hyperbola, the same in every quadrant. Lower left: the force on q₂ along the track as q₂ changes sign with '
  +'q₁ held, and the force on q₁ mirroring it. Lower right: the force on q₂ against the product q₁q₂ — the whole plane on one line.';
const PROD_CAP_SHORT='Like signs repel, unlike attract; |F| contours are hyperbolas |q₁q₂| = const. Below: straight lines through zero.';
const GRAV_CAP_FULL='An electron and a proton, the pair in a hydrogen atom: the electric force (green) and the gravitational one (orange) '
  +'against the distance between them, from a femtometre to a metre. Both fall as 1/r², so the lines are parallel and their ratio is the '
  +'same everywhere; the cyan line is the Bohr radius. The dashed magenta line is the atomic screen’s own pair. Lower left: the macro '
  +'screen turned round — the equal masses that would pull as hard as its charges, at any distance. Lower right: the ratio for three pairs.';
const GRAV_CAP_SHORT='Electric (green) and gravitational (orange) force on an electron and a proton: parallel, 2.27 × 10³⁹ apart.';

/* ================================================================== *
 *  view: the charge product                                           *
 * ================================================================== */
function drawProd(ctx,W,H,M){
  const L=M.L, P=M.P, T=L.T, qm=Q_MAX, un=L.w==='macro'?'µC':'e';
  const Lo=stageLayoutH(ctx,W,H,PROD_CAP_FULL,PROD_CAP_SHORT,2,0.36,1);
  const b=Lo.main, px=q=>b.x+b.w*(q+qm)/(2*qm), py=q=>b.y1-b.h*(q+qm)/(2*qm);
  /* the quadrants: like signs repel, unlike attract */
  ctx.fillStyle='rgba(232,132,58,0.07)'; ctx.fillRect(px(0),b.y,b.x1-px(0),py(0)-b.y); ctx.fillRect(b.x,py(0),px(0)-b.x,b.y1-py(0));
  ctx.fillStyle='rgba(90,200,224,0.06)'; ctx.fillRect(b.x,b.y,px(0)-b.x,py(0)-b.y); ctx.fillRect(px(0),py(0),b.x1-px(0),b.y1-py(0));
  /* the y axis starts its numbers one tick up: at -10 both axes would label
     the same corner and the two "-10"s collide */
  axesT(ctx,b,-qm,qm,-qm,qm,{title:titleFor(b,'the force over every pair of charges at r = '+fmt(L.r*T.uPerM,L.w==='macro'?1:0)+' '+T.unit+' ('+L.w+' scale)','F over (q₁, q₂)'),
    xlab:'q₁, '+un,ylab:'q₂, '+un,xticks:[-10,-5,0,5,10],yticks:[-5,0,5,10],xfmt:tickNum,yfmt:tickNum});
  polyline(ctx,b,[-qm,qm],[0,0],-qm,qm,-qm,qm,rgba(COL.struct,0.7),1.2);
  polyline(ctx,b,[0,0],[-qm,qm],-qm,qm,-qm,qm,rgba(COL.struct,0.7),1.2);
  for(const C of P.contours) for(const [sx,sy] of [[1,1],[-1,-1],[1,-1],[-1,1]])
    polyline(ctx,b,C.xs.map(x=>sx*x),C.ys.map(y=>sy*y),-qm,qm,-qm,qm,C.decade?rgba(COL.pos,0.85):rgba(COL.pos,0.35),C.decade?1.4:1);
  for(const C of P.contours){ if(!C.decade) continue; const d=Math.sqrt(C.c); if(d<qm*0.9) lab(ctx,W,H,px(d)+5,py(d)-5,sciPlain(C.F,1)+' N',COL.pos,SM_FONT,'left','bottom'); }
  if(P.live.c>0){ const sx=Math.sign(L.Q1), sy=Math.sign(L.Q2);
    polyline(ctx,b,P.live.xs.map(x=>sx*x),P.live.ys.map(y=>sy*y),-qm,qm,-qm,qm,COL.live,1.4,[5,4]); }
  lab(ctx,W,H,px(qm*0.55),py(qm*0.93),'repel',COL.ref,SM_FONT,'center');
  lab(ctx,W,H,px(-qm*0.55),py(-qm*0.93),'repel',COL.ref,SM_FONT,'center');
  lab(ctx,W,H,px(-qm*0.55),py(qm*0.93),'attract',COL.struct,SM_FONT,'center');
  lab(ctx,W,H,px(qm*0.55),py(-qm*0.93),'attract',COL.struct,SM_FONT,'center');
  marker(ctx,b,-qm,qm,-qm,qm,L.Q1,L.Q2,COL.live);
  labBeside(ctx,W,H,b,px(L.Q1),py(L.Q2)-8,'|F| = '+sciPlain(L.Fmag,3)+' N',COL.live,'bottom');
  const [bl,br]=lowerPanels(Lo);
  /* symmetric force axes: y numbers kept 14 px clear of the bottom corner,
     where the x axis prints its -10 */
  const symTicks=(yh,bx)=>ticksFor(-yh,yh,nyFor(bx.h)).filter(t=>(t+yh)/(2*yh)*bx.h>14);
  if(bl&&L.Q1===0){
    axesT(ctx,bl,-qm,qm,-1,1,{title:titleFor(bl,'the force on q₂ as q₂ changes sign (q₁ held)','F on q₂ against q₂'),xlab:'q₂, '+un,xticks:[-10,-5,0,5,10],yticks:[],xfmt:tickNum});
    labIn(ctx,W,H,bl,bl.x+bl.w/2,bl.y+bl.h/2,'q₁ is zero: no force on q₂, whatever its charge',COL.ref,'center','middle');
  } else if(bl){
    const yh=Math.max(...P.F2s.map(Math.abs))*1.1, ax=powAxis(yh,'F','N');
    axesT(ctx,bl,-qm,qm,-yh,yh,{title:titleFor(bl,'the force on q₂ as q₂ changes sign (q₁ held)','F on q₂ against q₂'),xlab:'q₂, '+un,ylab:ax.lab,
      yticks:symTicks(yh,bl),xfmt:tickNum,yfmt:ax.fmt});
    polyline(ctx,bl,[-qm,qm],[0,0],-qm,qm,-yh,yh,rgba(COL.struct,0.6),1);
    polyline(ctx,bl,P.q2s,P.F1s,-qm,qm,-yh,yh,COL.ref,1.3,[5,4]);
    polyline(ctx,bl,P.q2s,P.F2s,-qm,qm,-yh,yh,COL.pos,2);
    marker(ctx,bl,-qm,qm,-yh,yh,L.Q2,L.F2,COL.live);
    legendAuto(ctx,bl,[[COL.pos,'on q₂ (+x: pushed away)'],[COL.ref,'on q₁, its mirror']]);
  }
  if(br){
    const pm=qm*qm, yh=Math.max(...P.Fps.map(Math.abs))*1.1, ax=powAxis(yh,'F on q₂','N');
    axesT(ctx,br,-pm,pm,-yh,yh,{title:titleFor(br,'the force against the product q₁q₂: the whole plane on one line','F against q₁q₂'),xlab:'q₁q₂, '+un+'²',ylab:ax.lab,nx:5,
      yticks:symTicks(yh,br),xfmt:tickNum,yfmt:ax.fmt});
    polyline(ctx,br,[-pm,pm],[0,0],-pm,pm,-yh,yh,rgba(COL.struct,0.6),1);
    polyline(ctx,br,P.ps,P.Fps,-pm,pm,-yh,yh,COL.pos,2);
    marker(ctx,br,-pm,pm,-yh,yh,P.prod,L.F2,COL.live);
    labIn(ctx,W,H,br,br.x+br.w*0.25,br.y+12,'attract',COL.struct,'center','top');
    labIn(ctx,W,H,br,br.x+br.w*0.75,br.y1-14,'repel',COL.ref,'center','bottom');
  }
  drawCaption(ctx,Lo);
}

/* ================================================================== *
 *  view: electricity and gravity                                      *
 * ================================================================== */
function drawGrav(ctx,W,H,M){
  const E=M.E, La=M.La;
  const Lo=stageLayoutH(ctx,W,H,GRAV_CAP_FULL,GRAV_CAP_SHORT,2,0.36,1);
  const b=Lo.main, X0=-15, X1=0, Y0=-70, Y1=5;
  const px=lr=>b.x+b.w*(lr-X0)/(X1-X0), py=lf=>b.y1-b.h*(lf-Y0)/(Y1-Y0);
  /* y numbers from 10^-60 up: at 10^-70 they would share the corner with 10^-15;
     every 20 decades when 10 would put them under 14 px apart (a short panel) */
  const ystep=b.h*10/(Y1-Y0)<14?20:10;
  const xt=[], yt=[]; for(let e=X0;e<=X1;e+=3) xt.push(e); for(let e=-60;e<=0;e+=ystep) yt.push(e);
  axesT(ctx,b,X0,X1,Y0,Y1,{title:titleFor(b,'an electron and a proton: electric and gravitational force against distance, log–log','F against r, log–log'),
    xlab:'distance r, m',ylab:'F, N',xticks:xt,yticks:yt,xfmt:powLabel,yfmt:powLabel});
  const lr=E.rs.map(Math.log10);
  polyline(ctx,b,[Math.log10(A0),Math.log10(A0)],[Y0,Y1],X0,X1,Y0,Y1,rgba(COL.struct,0.7),1.2,[3,4]);
  polyline(ctx,b,lr,E.Fg.map(Math.log10),X0,X1,Y0,Y1,COL.ref,2);
  polyline(ctx,b,lr,E.Fe.map(Math.log10),X0,X1,Y0,Y1,COL.pos,2);
  if(La.Fmag>0) polyline(ctx,b,lr,E.Fa.map(Math.log10),X0,X1,Y0,Y1,COL.live,1.2,[5,4]);
  marker(ctx,b,X0,X1,Y0,Y1,Math.log10(A0),Math.log10(E.FeA0),COL.pos);
  marker(ctx,b,X0,X1,Y0,Y1,Math.log10(A0),Math.log10(E.FgA0),COL.ref);
  if(La.Fmag>0) marker(ctx,b,X0,X1,Y0,Y1,Math.log10(La.r),Math.log10(La.Fmag),COL.live);
  /* the gap between the parallel lines, at 1 um: the ratio, the same everywhere */
  const xr=-6, ye=Math.log10(forceMag(K_E,E_CH,E_CH,1e-6)), yg=Math.log10(forceMag(G_N,M_E,M_P,1e-6));
  ctx.strokeStyle=COL.text; ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.moveTo(px(xr),py(ye)+4); ctx.lineTo(px(xr),py(yg)-4);
  ctx.moveTo(px(xr)-4,py(ye)+10); ctx.lineTo(px(xr),py(ye)+4); ctx.lineTo(px(xr)+4,py(ye)+10);
  ctx.moveTo(px(xr)-4,py(yg)-10); ctx.lineTo(px(xr),py(yg)-4); ctx.lineTo(px(xr)+4,py(yg)-10); ctx.stroke();
  POLY_SEGS.push(px(xr),py(ye),px(xr),py(yg));
  lab(ctx,W,H,px(xr)+8,(py(ye)+py(yg))/2,'× '+sciPlain(E.ratioEP,3)+' at every distance',COL.text,LAB_FONT,'left');
  labIn(ctx,W,H,b,px(Math.log10(A0))+6,py(Math.log10(E.FeA0))-8,'Bohr radius: '+sciPlain(E.FeA0,3)+' N',COL.pos,'left','bottom');
  labIn(ctx,W,H,b,px(Math.log10(A0))+6,py(Math.log10(E.FgA0))+8,sciPlain(E.FgA0,3)+' N',COL.ref,'left','top');
  legendAuto(ctx,b,[[COL.pos,'electric, k e²/r²'],[COL.ref,'gravitational, G mₑmₚ/r²'],[COL.live,'the atomic screen’s pair']]);
  const [bl,br]=lowerPanels(Lo);
  if(bl){
    const yh=E.ms[E.ms.length-1]/1000*1.1;
    axesT(ctx,bl,0,Q_MAX*Q_MAX,0,yh,{title:titleFor(bl,'equal masses that pull as hard as the macro charges','masses for the macro charges'),xlab:'|q₁q₂|, µC²',ylab:'m, tonnes',nx:5,ny:nyFor(bl.h),
      xfmt:tickNum,yfmt:tickNum});
    polyline(ctx,bl,E.ps,E.ms.map(m=>m/1000),0,Q_MAX*Q_MAX,0,yh,COL.pos,2);
    marker(ctx,bl,0,Q_MAX*Q_MAX,0,yh,E.prodM,E.mEq/1000,COL.live);
    labBeside(ctx,W,H,bl,bl.x+bl.w*E.prodM/(Q_MAX*Q_MAX),bl.y1-bl.h*(E.mEq/1000)/yh+14,E.prodM>0?sigf(E.mEq/1000,3)+' t each, at any r':'no force, no mass',COL.live,'top');
  }
  if(br){
    const rows=[['two electrons',E.ratioEE],['electron–proton',E.ratioEP],['two protons',E.ratioPP]];
    const lo=30, hi=45, bx=v=>br.x+br.w*(Math.log10(v)-lo)/(hi-lo);
    axesT(ctx,br,lo,hi,0,3,{title:titleFor(br,'the ratio k e²/(G m m′) for three pairs','the ratio, three pairs'),xlab:'F electric / F gravitational',
      xticks:[30,33,36,39,42,45],yticks:[],xfmt:powLabel});
    rows.forEach(([nm,v],i)=>{ const yc=br.y+br.h*(i+0.5)/3, hgt=Math.min(18,br.h/5);
      ctx.fillStyle=rgba(COL.pos,0.75); ctx.fillRect(br.x,yc-hgt/2,bx(v)-br.x,hgt);
      labIn(ctx,W,H,br,br.x+6,yc-hgt/2-3,nm+': '+sciPlain(v,3),COL.text,'left','bottom'); });
  }
  drawCaption(ctx,Lo);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='macro'||M.view==='atomic') drawLab(ctx,W,H,labSpec(M));
  else if(M.view==='inv') drawInverse(ctx,W,H,invSpec(M));
  else if(M.view==='prod') drawProd(ctx,W,H,M);
  else drawGrav(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(){ return false; };             /* nothing here moves on its own */
  S.ended=function(){ return false; };
  /* the pointer: the charges and the ruler, on the two scale screens */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const w=ST.view;
    if(w!=='macro'&&w!=='atomic') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(), LS=labSpec(M), G=labGeo(ctx,S.W,S.H,LS), u=TRACKS[w].uPerM;
    if(type==='down'){
      const hit=labHit(G,LS,x,y);
      if(hit==='ruler'){ DRAG.what='ruler'; DRAG.off=G.wx(x)-LS.ruler.x0; DRAG.offY=y-G.ruler.y0; return true; }
      if(hit===1||hit===2){ DRAG.what=hit; DRAG.off=G.wx(x)-LS.bodies[hit-1].x; return true; }
      return false;
    }
    if(type==='move'){
      if(DRAG.what===1||DRAG.what===2){ setPosCL(ST,w,DRAG.what,(G.wx(x)-DRAG.off)/u); return true; }
      if(DRAG.what==='ruler'){ const y0=clamp(y-DRAG.offY,G.ruler.ryLo,G.ruler.ryHi); setRulerCL(ST,w,(G.wx(x)-DRAG.off)/u,G.wy(y0)); return true; }
    }
    return false;
  };
  return S;
}
