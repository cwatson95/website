
/* ================================================================== *
 *  drawing helpers particular to this sim, then THE BOUNDARY and      *
 *  THE WAVE                                                           *
 * ================================================================== */
const WORLD={xmin:-31,xmax:31,ymin:-21.7,ymax:21.7};     /* PhET's model bounds, in red wavelengths */
/* the wave world is wide and shallow so that it FILLS the stage: a box of
   the boundary view's aspect leaves two thirds of the width empty and makes
   every wavelength three times smaller than it needs to be */
const WAVE_WORLD={xmin:-14,xmax:14,ymin:-5,ymax:5};
let PICKS=[];                                             /* what the last draw made draggable */

/* The house #hint is HTML at bottom:11px and the canvas capture cannot see it,
   so a caption anchored at H-12 sits underneath it (wave-on-a-string
   Known-bad).  Every layout here reserves HINT_H at the bottom. */
function stageLayoutH(ctx,W,H,capFull,capShort,nBottom,bottomFrac,nBottomNarrow){
  return stageLayout(ctx,W,H-HINT_H,capFull,capShort,nBottom,bottomFrac,nBottomNarrow);
}
/* a short plot cannot carry five y labels without them colliding */
function nyFor(b){ return b.h<110?3:(b.h<170?4:5); }
/* a note under a panel lands on the axis label or on the caption; put it
   inside the box, where lab() can dodge whatever is already there */
function noteIn(ctx,W,H,b,txt,col){ lab(ctx,W,H,b.x+b.w/2,b.y1-11,txt,col||COL.dim,SM_FONT,'center'); }
/* axes() draws its tick labels with raw fillText, so the registry does not
   know about them and a note nudged downward by lab() lands on the x ticks
   (the neural_playground Known-bad, one panel in).  axesRB registers the two
   tick strips: the row under the box and the column to its left. */
function axesRB(ctx,b,xlo,xhi,ylo,yhi,opt){
  axesR(ctx,b,xlo,xhi,ylo,yhi,opt);
  LABELS.push([b.x,b.y1,b.x1,b.y1+34]);
  LABELS.push([b.x-46,b.y-8,b.x,b.y1+8]);
}
/* legendAuto records its box in LEGEND_RECTS, which lab() does not consult —
   so a note placed afterwards lands on top of it.  Register it in LABELS too. */
function legendA(ctx,b,items){
  const lb=legendAuto(ctx,b,items);
  if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
  return lb;
}

/* a ray from `p` along the unit vector `d`, of world length L, CLIPPED in
   data space to the world box (the house rule: never ctx.clip, because the
   display-list recorder treats it as a no-op and the audit would still lie) */
function rayW(ctx,map,p,d,L,col,lw,ext){
  segW(ctx,map,p,[p[0]+L*d[0],p[1]+L*d[1]],ext||WORLD,col,lw);
}
function segW(ctx,map,a,b,ext,col,lw,dash){
  const c=clipSegY(a[0],a[1],b[0],b[1],ext.ymin,ext.ymax,ext.xmin,ext.xmax);
  if(!c) return;
  seg(ctx,map,[c[0],c[1]],[c[2],c[3]],col,lw,dash);
}
/* a dashed arc from angle a0 to a1 (radians, measured from +x, world frame) */
function arcW(ctx,map,c,r,a0,a1,col,lw){
  const n=Math.max(6,Math.round(Math.abs(a1-a0)*26));
  const xs=[],ys=[];
  for(let i=0;i<=n;i++){ const a=a0+(a1-a0)*i/n; xs.push(c[0]+r*Math.cos(a)); ys.push(c[1]+r*Math.sin(a)); }
  ctx.beginPath();
  for(let i=0;i<=n;i++){ const X=map.X(xs[i]),Y=map.Y(ys[i]); if(i===0) ctx.moveTo(X,Y); else ctx.lineTo(X,Y); }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.2; ctx.stroke();
}
/* PhET's protractor: a half-circle of degree ticks centred on the origin,
   zero on the normal, drawn on whichever side the laser is */
function protractorW(ctx,W,H,map,r){
  ctx.strokeStyle=rgba(COL.dim,0.55); ctx.lineWidth=1;
  arcW(ctx,map,[0,0],r,0,TAU,rgba(COL.dim,0.45),1);
  for(let dgr=0;dgr<360;dgr+=5){
    const a=dgr*DEG, f=(dgr%15===0)?0.90:0.955;
    seg(ctx,map,[r*f*Math.cos(a),r*f*Math.sin(a)],[r*Math.cos(a),r*Math.sin(a)],
        rgba(COL.dim,dgr%15===0?0.8:0.4),1);
  }
  for(let dgr=0;dgr<360;dgr+=30){
    const a=dgr*DEG, lbl=((dgr+270)%360);
    const from90=Math.abs(((lbl+180)%360)-180);
    lab(ctx,W,H,map.X(r*0.80*Math.cos(a)),map.Y(r*0.80*Math.sin(a)),
        fmt(from90,0)+'°',rgba(COL.dim,0.9),SM_FONT,'center');
  }
}
/* the laser body: a barrel pointing along d, ending at the origin.  `kind`
   is what a drag on it does -- swing the beam ('laser') or slide it ('beam'). */
function laserW(ctx,map,d,on,kind,sc,at,gap){
  const k=sc===undefined?1:sc, A=at||[0,0], g=gap===undefined?5.2:gap;
  const back=[A[0]-14*k*d[0],A[1]-14*k*d[1]], front=[A[0]-g*k*d[0],A[1]-g*k*d[1]];
  const perp=[-d[1],d[0]], w=1.9*k;
  const quad=[[back[0]+perp[0]*w,back[1]+perp[1]*w],[front[0]+perp[0]*w,front[1]+perp[1]*w],
              [front[0]-perp[0]*w,front[1]-perp[1]*w],[back[0]-perp[0]*w,back[1]-perp[1]*w]];
  worldPoly(ctx,map,quad,on?'#2b3446':'#1b2130',COL.live,1.6);
  const knob=[[back[0]+perp[0]*w*1.5,back[1]+perp[1]*w*1.5],
              [back[0]-perp[0]*w*1.5,back[1]-perp[1]*w*1.5],
              [back[0]-d[0]*1.6*k-perp[0]*w*1.5,back[1]-d[1]*1.6*k-perp[1]*w*1.5],
              [back[0]-d[0]*1.6*k+perp[0]*w*1.5,back[1]-d[1]*1.6*k+perp[1]*w*1.5]];
  worldPoly(ctx,map,knob,COL.live,null,1);
  PICKS.push({kind:kind||'laser',x:map.X(back[0]),y:map.Y(back[1]),r:26});
}

/* ---------------------------------------------------------- the boundary */
function boundGeo(ctx,W,H,M,st){
  const capFull='The world is PhET’s own: '+PHET.modelW+' × '+fmt(PHET.modelH,1)
    +' red wavelengths across, i.e. '+fmt(PHET.modelW*PHET.lamRed/1000,1)+' × '
    +fmt(PHET.modelH*PHET.lamRed/1000,1)+' µm — the sim is a few tens of wavelengths wide, '
    +'which is why the wave view works at all. Ray thickness and opacity carry the power fraction; '
    +'the light is drawn in the true colour of its wavelength (CIE 1931). Angles are measured from '
    +'the normal, never from the surface.';
  const capShort='PhET’s world, '+PHET.modelW+' red wavelengths wide. Ray opacity carries power.';
  const L=stageLayoutH(ctx,W,H,capFull,capShort,0,0,0);
  const map=worldFitUp(L.main,WORLD,1.5);
  return {L:L,map:map};
}
function drawBound(ctx,W,H,M,st){
  const G=boundGeo(ctx,W,H,M,st), L=G.L, map=G.map, B=M.b;
  /* the two media */
  const X0=map.X(WORLD.xmin),X1=map.X(WORLD.xmax),Ytop=map.Y(WORLD.ymax),Ymid=map.Y(0),Ybot=map.Y(WORLD.ymin);
  ctx.fillStyle=mediumFill(B.n1); ctx.fillRect(X0,Ytop,X1-X0,Ymid-Ytop);
  ctx.fillStyle=mediumFill(B.n2); ctx.fillRect(X0,Ymid,X1-X0,Ybot-Ymid);
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.4;
  ctx.beginPath(); ctx.moveTo(X0,Ymid); ctx.lineTo(X1,Ymid); ctx.stroke();
  POLY_SEGS.push(X0,Ymid,X1,Ymid);
  frame(ctx,box(X0,Ytop,X1-X0,Ybot-Ytop),COL.edge);
  if(st.showProtractor) protractorW(ctx,W,H,map,17);
  /* the normal */
  if(st.showNormal){
    seg(ctx,map,[0,WORLD.ymin*0.92],[0,WORLD.ymax*0.92],rgba(COL.norm,0.8),1.2,[5,4]);
    lab(ctx,W,H,map.X(0)+7,map.Y(WORLD.ymax*0.86),'normal',rgba(COL.norm,0.95),SM_FONT,'left');
  }
  /* the laser and its rays */
  laserW(ctx,map,B.dIn,st.laserOn);
  if(st.laserOn){
    const wls=st.white?WHITE_WL:[st.lamNm];
    if(st.white){
      /* the incident and reflected rays are the SAME line for every
         wavelength — reflection does not disperse — so they are drawn once,
         white.  Only the transmitted ray fans out, and that fan is drawn one
         wavelength at a time. */
      const b0=boundaryModel(st,550);
      rayW(ctx,map,[-5.2*b0.dIn[0],-5.2*b0.dIn[1]],b0.dIn,5.2,'rgba(255,255,255,0.92)',3.0);
      if(drawsReflected(b0.R))
        rayW(ctx,map,[0,0],b0.dRefl,60,'rgba(255,255,255,'+fmt(clamp(0.25+0.7*Math.sqrt(b0.R),0,1),3)+')',
             1.2+2.4*Math.sqrt(b0.R));
      for(const lam of wls){
        const b=boundaryModel(st,lam);
        if(b.dTrans) rayW(ctx,map,[0,0],b.dTrans,60,beamCss(st,lam,b.T),1.5);
      }
    } else for(const lam of wls){
      const b=boundaryModel(st,lam);
      rayW(ctx,map,[-5.2*b.dIn[0],-5.2*b.dIn[1]],b.dIn,5.2,beamCss(st,lam,1),3.0);
      if(drawsReflected(b.R))
        rayW(ctx,map,[0,0],b.dRefl,60,beamCss(st,lam,b.R),1.2+2.4*Math.sqrt(b.R));
      if(b.dTrans)
        rayW(ctx,map,[0,0],b.dTrans,60,beamCss(st,lam,b.T),1.2+2.4*Math.sqrt(b.T));
    }
  }
  /* the angle arcs */
  if(st.showAngles&&st.laserOn){
    const r=9.5;
    arcW(ctx,map,[0,0],r,PI/2,PI/2+B.th1,COL.arc,1.3);
    lab(ctx,W,H,map.X(r*1.16*Math.cos(PI/2+B.th1/2)),map.Y(r*1.16*Math.sin(PI/2+B.th1/2)),
        fmt(st.angDeg,1)+'°',COL.arc,LAB_FONT,'center');
    arcW(ctx,map,[0,0],r*0.78,PI/2-B.th1,PI/2,rgba(COL.arc,0.7),1.1);
    if(isFinite(B.th2)){
      arcW(ctx,map,[0,0],r,-PI/2,-PI/2+B.th2,COL.pos,1.3);
      lab(ctx,W,H,map.X(r*1.2*Math.cos(-PI/2+B.th2/2)),map.Y(r*1.2*Math.sin(-PI/2+B.th2/2)),
          fmt(B.th2*RAD,1)+'°',COL.pos,LAB_FONT,'center');
    }
  }
  /* the critical-angle marker, on the incoming side */
  if(isFinite(B.tc)){
    const d=[Math.sin(B.tc),Math.cos(B.tc)];
    segW(ctx,map,[0,0],[-24*d[0],24*d[1]],WORLD,rgba(COL.ref,0.55),1.1,[4,5]);
    lab(ctx,W,H,map.X(-22*d[0]),map.Y(22*d[1]),'θc = '+fmt(B.tc*RAD,1)+'°',
        rgba(COL.ref,0.95),SM_FONT,'left');
  }
  /* the media names */
  lab(ctx,W,H,X0+9,Ytop+13,subLabel(st.topSub,B.n1),rgba(COL.struct,0.95),LAB_FONT,'left');
  lab(ctx,W,H,X0+9,Ybot-13,subLabel(st.botSub,B.n2),rgba(COL.struct,0.95),LAB_FONT,'left');
  /* PhET's intensity meter */
  if(st.showMeter&&st.laserOn) meterBox(ctx,W,H,map,B,st);
  if(B.tir)
    lab(ctx,W,H,(X0+X1)/2,Ytop+15,'total internal reflection — nothing is transmitted',
        COL.ref,LAB_FONT,'center');
  if(st.white&&st.laserOn)
    lab(ctx,W,H,(X0+X1)/2,Ytop+31,(X1-X0)<620
        ? 'white: only the transmitted fan disperses'
        : 'white: the incident and reflected rays are one line for every wavelength '
          +'— only the transmitted fan disperses',COL.dim,SM_FONT,'center');
  drawCaption(ctx,L);
}
/* PhET's intensity meter: a probe on the reflected ray and a body reading a
   percentage.  PhET reads the s-polarised reflectance; the chips switch it. */
function meterBox(ctx,W,H,map,B,st){
  const d=B.dRefl, probe=[13*d[0],13*d[1]];
  dot(ctx,map.X(probe[0]),map.Y(probe[1]),5,rgba(COL.live,0.85),'#fff',1.2);
  const w=126,h=56, PX=map.X(probe[0]), PY=map.Y(probe[1]);
  /* four candidate corners; take the first that no label already occupies
     (at normal incidence the probe sits on the normal line and its label) */
  let x=clamp(PX+12,4,W-w-4), y=clamp(PY-56,stageTop()+2,H-h-HINT_H-4);
  for(const [dx,dy] of [[12,-56],[-w-12,-56],[12,10],[-w-12,10],[12,-116],[-w-12,-116]]){
    const cx=clamp(PX+dx,4,W-w-4), cy=clamp(PY+dy,stageTop()+2,H-h-HINT_H-4);
    if(labFits([cx,cy,cx+w,cy+h])){ x=cx; y=cy; break; }
  }
  LABELS.push([x,y,x+w,y+h]);
  ctx.fillStyle='rgba(10,12,18,.86)'; ctx.fillRect(x,y,w,h);
  frame(ctx,box(x,y,w,h),COL.edge2||'#2a2f3d');
  ctx.fillStyle=COL.dim; ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillText('intensity, reflected',x+7,y+5);
  ctx.fillStyle=COL.pos; ctx.font='italic 19px Georgia, serif';
  ctx.fillText(fmt(100*B.R,1)+'%',x+7,y+18);
  ctx.fillStyle=COL.dim; ctx.font=SM_FONT;
  ctx.fillText(st.pol==='s'?'s-polarised (PhET’s reading)':st.pol==='p'?'p-polarised':'unpolarised',
               x+7,y+42);
}

/* -------------------------------------------------------------- the wave */
function waveGeo(ctx,W,H,M,st){
  const capFull='Crest lines, drawn where the phase is a whole number of cycles. The construction is the '
    +'whole of Snell’s law: the crests must meet along the boundary, so the spacing they cut there — '
    +'λ/sinθ — has to be the same measured from either side. The field is painted from the exact '
    +'s-polarised amplitudes, so the standing pattern above the boundary and the travelling wave below '
    +'are the real ones, not a sketch. World: '+fmt(WAVE_WORLD.xmax*2,0)+' red wavelengths wide.';
  const capShort='Crest lines and the exact s-polarised field. The crest spacing along the boundary is Snell’s law.';
  const L=stageLayoutH(ctx,W,H,capFull,capShort,2,0.34,1);
  const map=worldFitUp(L.main,WAVE_WORLD,0.3);
  return {L:L,map:map};
}
function drawWave(ctx,W,H,M,st){
  const G=waveGeo(ctx,W,H,M,st), L=G.L, map=G.map, B=M.b, Wv=M.wave;
  const ph=st.phase;
  const X0=map.X(WAVE_WORLD.xmin),X1=map.X(WAVE_WORLD.xmax);
  const Ytop=map.Y(WAVE_WORLD.ymax),Ymid=map.Y(0),Ybot=map.Y(WAVE_WORLD.ymin);
  ctx.fillStyle=mediumFill(B.n1); ctx.fillRect(X0,Ytop,X1-X0,Ymid-Ytop);
  ctx.fillStyle=mediumFill(B.n2); ctx.fillRect(X0,Ymid,X1-X0,Ybot-Ytop>0?Ybot-Ymid:0);
  /* The background is the TIME-AVERAGED intensity, which depends on y alone:
     above the boundary it is the standing-wave pattern the incident and
     reflected waves make, below it the constant (or exponentially decaying)
     intensity of the transmitted wave.  Painting the instantaneous field on a
     cell grid instead aliased into a checkerboard and drowned the crest lines
     it was supposed to sit behind. */
  if(st.paintField){
    const rgb=monoLinear(st.lamNm);
    let mx=1e-9;
    const rows=Math.max(40,Math.min(220,Math.round(Ybot-Ytop)));
    const vals=[];
    for(let i=0;i<rows;i++){
      const y=map.wy(Ytop+(i+0.5)*(Ybot-Ytop)/rows);
      const v=meanIntensity(Wv,y); vals.push(v); mx=Math.max(mx,v);
    }
    for(let i=0;i<rows;i++){
      /* dim: the crest lines are drawn in the same hue on top of it, and a
         bright wash swallows them */
      ctx.fillStyle=cssOfLinear(rgb,0.05+0.23*clamp(vals[i]/mx,0,1));
      ctx.fillRect(X0,Ytop+i*(Ybot-Ytop)/rows,X1-X0,(Ybot-Ytop)/rows+1);
    }
  }
  /* the crest lines: exact loci of phase = 2 pi m */
  const kx=Wv.k0*Wv.n1*Math.sin(B.th1);
  crestFamily(ctx,map,B.dIn,Wv.k0*Wv.n1,ph,0,WAVE_WORLD.ymax,st,1.0,'in');
  const rA=cAbs(Wv.f.rRe,Wv.f.rIm), rP=cArg(Wv.f.rRe,Wv.f.rIm);
  if(rA>0.02) crestFamily(ctx,map,B.dRefl,Wv.k0*Wv.n1,ph-rP,0,WAVE_WORLD.ymax,st,rA,'refl');
  if(B.dTrans){
    const tA=cAbs(Wv.f.tRe,Wv.f.tIm), tP=cArg(Wv.f.tRe,Wv.f.tIm);
    crestFamily(ctx,map,B.dTrans,Wv.k0*Wv.n2,ph-tP,WAVE_WORLD.ymin,0,st,tA,'trans');
  } else if(st.showEvanescent){
    /* the evanescent tail: crests run PARALLEL to the boundary's normal
       direction of travel (straight down the x axis) and decay with depth */
    const dec=Wv.k0*Wv.f.kap;
    for(let m=-40;m<=40;m++){
      const x0=(TAU*m+ph-cArg(Wv.f.tRe,Wv.f.tIm))/kx;
      if(!isFinite(x0)||x0<WAVE_WORLD.xmin||x0>WAVE_WORLD.xmax) continue;
      const depth=Math.min(WAVE_WORLD.ymax,3/Math.max(dec,1e-6));
      seg(ctx,map,[x0,0],[x0,-depth],rgba('#e8843a',0.5),1.2,[3,3]);
    }
    lab(ctx,W,H,(X0+X1)/2,Ymid+38,'evanescent — decays in '+fmt(B.lam/(TAU*Wv.f.kap),0)
        +' nm, carries no power',COL.ref,SM_FONT,'center');
  }
  ctx.strokeStyle=COL.struct; ctx.lineWidth=1.4;
  ctx.beginPath(); ctx.moveTo(X0,Ymid); ctx.lineTo(X1,Ymid); ctx.stroke();
  /* the laser, drawn at a quarter size because this world is a fifth as wide */
  laserW(ctx,map,B.dIn,true,'laser',0.28);
  rayW(ctx,map,[-1.5*B.dIn[0],-1.5*B.dIn[1]],B.dIn,1.5,beamCss(st,st.lamNm,1),2.4);
  /* the crest marks the two media cut on the boundary: they coincide */
  const dx1=B.lam1/PHET.lamRed/Math.max(Math.sin(B.th1),1e-9);
  {
    /* one tick per crest, but only while they are far enough apart to read as
       ticks rather than as a comb */
    const stepPx=Math.abs(TAU/kx)*map.s;
    const every=Math.max(1,Math.ceil(13/Math.max(stepPx,1e-6)));
    if(stepPx>2.5) for(let m=-200;m<=200;m++){
      if(m%every!==0) continue;
      const x=(TAU*m+ph)/kx;
      if(!isFinite(x)||x<WAVE_WORLD.xmin||x>WAVE_WORLD.xmax) continue;
      seg(ctx,map,[x,-0.30],[x,0.30],COL.pos,2.0);
    }
  }
  frame(ctx,box(X0,Ytop,X1-X0,Ybot-Ytop),COL.edge);
  lab(ctx,W,H,X0+9,Ytop+13,subLabel(st.topSub,B.n1)+'  λ = '+fmt(B.lam1,0)+' nm',
      rgba(COL.struct,0.95),LAB_FONT,'left');
  lab(ctx,W,H,X0+9,Ybot-13,subLabel(st.botSub,B.n2)+'  λ = '+fmt(B.lam2,0)+' nm',
      rgba(COL.struct,0.95),LAB_FONT,'left');
  lab(ctx,W,H,X1-9,Ymid-26,st.angDeg<1
      ? 'at normal incidence the crests run along the boundary'
      : 'crest spacing along the boundary '+fmt(B.lam1/Math.sin(B.th1),0)+' nm',
      COL.pos,SM_FONT,'right');
  /* the two lower panels */
  if(L.bottom.length>=1) waveProfile(ctx,W,H,L.bottom[0],M,st);
  if(L.bottom.length>=2) waveSensor(ctx,W,H,L.bottom[1],M,st);
  drawCaption(ctx,L);
}
/* one family of crest lines: the loci k.r = 2 pi m + ph, clipped to a y band */
function crestFamily(ctx,map,d,k,ph,ylo,yhi,st,amp,kind){
  const col=cssOfLinear(monoLinear(st.lamNm),clamp(0.35+0.6*amp,0,1));
  const perp=[-d[1],d[0]];
  for(let m=-60;m<=60;m++){
    /* the crest line passes through the point s*d with k*s = 2 pi m + ph */
    const s=(TAU*m+ph)/k;
    const p=[s*d[0],s*d[1]];
    const xs=[],ys=[];
    for(const t of [-40,40]){ xs.push(p[0]+t*perp[0]); ys.push(p[1]+t*perp[1]); }
    /* clip to the y band in data space */
    const seg2=clipSegY(xs[0],ys[0],xs[1],ys[1],ylo,yhi,WAVE_WORLD.xmin,WAVE_WORLD.xmax);
    if(!seg2) continue;
    seg(ctx,map,[seg2[0],seg2[1]],[seg2[2],seg2[3]],col,kind==='in'?1.7:1.3);
  }
}
/* Liang-Barsky in data space (the house rule: clip data, never ctx.clip) */
function clipSegY(x0,y0,x1,y1,ylo,yhi,xlo,xhi){
  let t0=0,t1=1; const dx=x1-x0, dy=y1-y0;
  const ps=[[-dx,x0-xlo],[dx,xhi-x0],[-dy,y0-ylo],[dy,yhi-y0]];
  for(const pq of ps){
    const p=pq[0], q=pq[1];
    if(p===0){ if(q<0) return null; continue; }
    const t=q/p;
    if(p<0){ if(t>t1) return null; if(t>t0) t0=t; }
    else { if(t<t0) return null; if(t<t1) t1=t; }
  }
  if(t0>t1) return null;
  return [x0+t0*dx,y0+t0*dy,x0+t1*dx,y0+t1*dy];
}
/* the field along a vertical cut at x = 0 */
function waveProfile(ctx,W,H,b,M,st){
  const Wv=M.wave, B=M.b;
  const ys=[],es=[],ep=[],em=[];
  for(let i=0;i<=200;i++){
    const y=WAVE_WORLD.ymin+(WAVE_WORLD.ymax-WAVE_WORLD.ymin)*i/200;
    /* the envelope of the standing pattern: sqrt(2 <E^2>), which is what the
       painted background carries, so the two panels cannot drift apart */
    const a=Math.sqrt(2*Math.max(meanIntensity(Wv,y),0));
    ys.push(y); es.push(waveAt(Wv,0,y,st.phase)); ep.push(a); em.push(-a);
  }
  axesRB(ctx,b,-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,
        {title:titleFor(b,'the field on the cut x = 0','field at x = 0'),
         xlab:'E (s-polarised)',ylab:'y (red wavelengths)',nx:4,ny:nyFor(b),
         xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  polyline(ctx,b,[0,0],[WAVE_WORLD.ymin,WAVE_WORLD.ymax],-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,
           rgba(COL.dim,0.5),1,[4,4]);
  polyline(ctx,b,[-2,2],[0,0],-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,COL.struct,1.4);
  polyline(ctx,b,ep,ys,-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,COL.ref,1.3,[4,3]);
  polyline(ctx,b,em,ys,-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,COL.ref,1.3,[4,3]);
  polyline(ctx,b,es,ys,-2,2,WAVE_WORLD.ymin,WAVE_WORLD.ymax,COL.pos,1.6);
  lab(ctx,W,H,b.x+b.w/2,b.y1-11,(B.tir?'evanescent below':'travelling below')
      +' · orange: the envelope',COL.dim,SM_FONT,'center');
}
/* PhET's More Tools wave sensor: two probes, one each side, against time */
function waveSensor(ctx,W,H,b,M,st){
  const Wv=M.wave;
  const ts=[],e1=[],e2=[];
  for(let i=0;i<=240;i++){
    const t=i/240*2*TAU;
    ts.push(t/TAU); e1.push(waveAt(Wv,0,2.0,st.phase+t)); e2.push(waveAt(Wv,0,-2.0,st.phase+t));
  }
  axesRB(ctx,b,0,2,-2.1,2.1,
        {title:titleFor(b,'the wave sensor: two probes against time','two probes vs time'),
         xlab:'time (periods)',ylab:'E',nx:3,ny:nyFor(b),xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  polyline(ctx,b,[0,2],[0,0],0,2,-2.1,2.1,rgba(COL.dim,0.5),1,[4,4]);
  polyline(ctx,b,ts,e1,0,2,-2.1,2.1,COL.pos,1.6);
  polyline(ctx,b,ts,e2,0,2,-2.1,2.1,COL.live,1.6);
  legendA(ctx,b,[[COL.pos,'probe above, y = +2'],[COL.live,'probe below, y = −2']]);
  noteIn(ctx,W,H,b,'the same period on both sides');
}
