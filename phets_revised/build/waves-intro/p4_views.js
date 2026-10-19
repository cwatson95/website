
/* ================================================================== *
 *  the views: the wave generator and its button, the tank, the side   *
 *  view, PhET's light screen, the graphs, and the analysis of the     *
 *  three media.  (The field, the parcels, the tape, the probes and    *
 *  the wave meter are in p4_draw.js, extracted from wave-interference *
 *  unchanged.)                                                        *
 * ================================================================== */
const GEN_W=46, GEN_H=30, BTN_R=9;
/* the generator sits outside the tank, on the source's own row; its button is
   below it (PhET's green wave-generator button) */
function genGeo(sq,R){
  const cs=sq.w/LAT.VIS, L=R.lat, y=sq.y+((L.ny-1)/2-L.pad+0.5)*cs, x1=sq.x-10, x0=x1-GEN_W;
  return {x0,x1,y,cs, sx:cellX(sq,R,srcCol(L)), btn:{x:(x0+x1)/2, y:y+GEN_H/2+14, r:BTN_R}};
}
function drawGenerator(ctx,W,H,sq,M){
  const R=M.R, g=genGeo(sq,R), x0=g.x0, x1=g.x1, y=g.y, on=M.active;
  ctx.fillStyle='#161c2c'; ctx.strokeStyle=COL.struct; ctx.lineWidth=1.3;
  const poly=pts=>{ ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); });
    ctx.closePath(); ctx.fill(); ctx.stroke(); };
  if(R.scene==='water'){                                   /* a faucet seen from above */
    poly([[x0,y-8],[x1-12,y-8],[x1-12,y-4],[x1,y-4],[x1,y+4],[x1-12,y+4],[x1-12,y+8],[x0,y+8]]);
  } else if(R.scene==='sound'){                            /* a loudspeaker */
    poly([[x0,y-9],[x0+16,y-9],[x0+16,y+9],[x0,y+9]]);
    poly([[x0+16,y-7],[x1,y-13],[x1,y+13],[x0+16,y+7]]);
  } else {                                                 /* a laser */
    poly([[x0,y-9],[x1-13,y-9],[x1-13,y+9],[x0,y+9]]);
    poly([[x1-13,y-3.5],[x1,y-3.5],[x1,y+3.5],[x1-13,y+3.5]]);
  }
  /* the nozzle reaches the source cell, which is five cells inside the tank */
  ctx.beginPath(); ctx.moveTo(x1,y); ctx.lineTo(g.sx,y);
  ctx.strokeStyle=on?rgba(COL.live,0.75):'#3a4254'; ctx.lineWidth=1.6; ctx.stroke();
  dot(ctx,g.sx,y,4.5,on?COL.live:'#3a4254','#ffffff',1.2);
  /* PhET's button: filled while the source runs, hollow while it waits */
  dot(ctx,g.btn.x,g.btn.y,g.btn.r,on?COL.live:'#141a28',on?'#ffffff':COL.live,1.6);
  lab(ctx,W,H,g.btn.x,g.btn.y+g.btn.r+9,M.mode==='pulse'?'fire':(on?'on':'off'),
      on?COL.live:'#8b93a6',SM_FONT,'center');
}
/* PhET's side view of the water, along the centre row (adapted from
   wave-interference's drawSide: the drop falls only while the source runs) */
function drawSideIntro(ctx,sq,M){
  const R=M.R, L=R.lat, pad=L.pad, nx=L.nx, mid=(L.ny-1)/2, cs=sq.w/LAT.VIS;
  const yb=sq.y+0.52*sq.h, hs=0.16*sq.h/U_FULL;
  ctx.fillStyle='#03060d'; ctx.fillRect(sq.x,sq.y,sq.w,sq.h);
  /* the source cell swings 1.2 x the amplitude, four times past the colour scale: its own
     spike is clipped here rather than drawn through the floor of the view (the caption says so) */
  const pts=[[sq.x,sq.y1]];
  for(let i=0;i<LAT.VIS;i++){ const v=clamp(L.u[mid*nx+pad+i],-1.8*U_FULL,1.8*U_FULL); pts.push([sq.x+(i+0.5)*cs,yb-hs*v]); }
  pts.push([sq.x1,sq.y1]);
  ctx.beginPath(); pts.forEach((p,k)=>{ if(k===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); ctx.closePath();
  ctx.fillStyle=mix(COL.water0,'#1d5f96',0.55); ctx.fill();
  ctx.beginPath();
  for(let k=1;k<pts.length-1;k++){ if(k===1) ctx.moveTo(pts[k][0],pts[k][1]); else ctx.lineTo(pts[k][0],pts[k][1]); }
  ctx.strokeStyle=COL.water1; ctx.lineWidth=1.6; ctx.stroke();
  /* the dripper over the source, and a drop on its way down at each crest */
  const xs=sq.x+(srcCol(L)-pad+0.5)*cs;
  ctx.fillStyle=COL.body; ctx.fillRect(xs-9,sq.y+6,18,14); ctx.fillRect(xs-3,sq.y+20,6,8);
  if(M.active){ const ph=((R.phi/TAU)%1+1)%1, yd=sq.y+32+ph*(yb-sq.y-40);
    dot(ctx,xs,yd,3.2,COL.water1); }
}
/* the air parcels (positions from parcelPositions, extracted from wave-interference): one
   parcel is marked, so that a single one can be watched jiggling in place.  Its colour is CYAN
   here, not wave-interference's magenta: in this sim magenta is the source, its button, the
   tape's ends and the probes, and a fifth magenta dot in the middle of the field would be a
   fifth meaning for one colour (Known-bad: two conventions on one plot is one too many). */
function drawParcelsIntro(ctx,sq,R){
  const P=parcelPositions(R), cs=sq.w/LAT.VIS, pad=R.lat.pad, MARK=220;
  ctx.beginPath();
  for(let q=0;q<P.length;q++){
    if(q===MARK) continue;
    const x=sq.x+(P[q][0]-pad+0.5)*cs, y=sq.y+(P[q][1]-pad+0.5)*cs;
    if(x<sq.x||x>sq.x1||y<sq.y||y>sq.y1) continue;
    ctx.moveTo(x+2.1,y); ctx.arc(x,y,2.1,0,TAU);
  }
  ctx.fillStyle='#d6dae4'; ctx.fill();
  const c=P[MARK];
  dot(ctx,sq.x+(c[0]-pad+0.5)*cs,sq.y+(c[1]-pad+0.5)*cs,3.4,COL.struct,'#ffffff',1);
}
/* PhET's light screen: one fill per brightness class, the base colour being the
   CIE colour of the wavelength scaled by PhET's brightness (PhET scales its own
   sRGB triple the same way) */
function drawScreenStrip(ctx,b,M){
  const B=M.bright, rows=B.length, base=specCss(M.lam,1), cs=b.h/rows, K=24, groups={};
  ctx.fillStyle='#000000'; ctx.fillRect(b.x,b.y,b.w,b.h);
  for(let r=0;r<rows;r++){ const q=Math.round(K*clamp(B[r],0,1)); if(q===0) continue; (groups[q]=groups[q]||[]).push(r); }
  for(const q in groups){
    ctx.beginPath();
    for(const r of groups[q]) ctx.rect(b.x,Math.round(b.y+r*cs),b.w,Math.round(b.y+(r+1)*cs)-Math.round(b.y+r*cs));
    ctx.fillStyle=mix('#000000',base,q/K); ctx.fill();
  }
  frame(ctx,b,'#2a3040');
}
/* the intensity along the screen, against the 1/r a point source would give
   (not in PhET's Waves Intro: its intensity checkbox is switched off) */
function drawIntensity(ctx,W,H,b,M){
  const I=M.I, S=M.S, rows=I.length, mx=M.Imax>0?M.Imax:1, xs=[], ys=[];
  for(let r=0;r<rows;r++){ ys.push((r+0.5)*S.W/rows); xs.push(I[r]/mx); }
  axesR(ctx,b,0,1.05,S.W,0,{xticks:[0,0.5,1],yticks:[],xfmt:t=>fmt(t,1),title:'intensity',xlab:'I / its peak'});
  if(M.th) polyline(ctx,b,Array.from(M.th),ys,0,1.05,S.W,0,COL.ref,1.4);
  polyline(ctx,b,xs,ys,0,1.05,S.W,0,COL.pos,1.8);
}
/* the wave meter's chart (after wave-interference's drawMeter, with one change: the window is
   2.5 periods of the frequency ON SHOW, not 2.5 of the medium's slowest, so the chart is full
   of the wave the tank is making rather than mostly empty) */
function drawMeterIntro(ctx,W,H,b,M){
  const R=M.R, S=M.S, tr=R.trace, win=2.5/R.f, t1=Math.max(R.t,win), t0=t1-win, Y=1.5*U_FULL;
  axesR(ctx,b,t0,t1,-Y,Y,{nx:5,ny:3,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),
    title:titleFor(b,'wave meter: the two probes against time','wave meter'),xlab:'time, '+S.tunit});
  for(let p=0;p<2;p++){
    const xs=[], ys=[];
    for(const s of tr) if(s[0]>=t0&&s.length>p+1){ xs.push(s[0]); ys.push(s[p+1]); }
    polyline(ctx,b,xs,ys,t0,t1,-Y,Y,p===0?COL.pos:COL.live,1.5);
  }
}
/* PhET's "Graph": the centre row, in the scene's own units */
function drawCentre(ctx,W,H,b,M){
  const R=M.R, S=M.S, L=R.lat, mid=(L.ny-1)/2, xs=[], ys=[];
  for(let i=0;i<LAT.VIS;i++){ xs.push(xOfCell(R,L.pad+i)); ys.push(L.u[mid*L.nx+L.pad+i]); }
  const Y=1.5*U_FULL;
  axesR(ctx,b,0,S.W,-Y,Y,{nx:6,ny:3,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),
    title:titleFor(b,GRAPH_TITLE[R.scene]+' — '+S.what+' along the middle row',GRAPH_TITLE[R.scene]),
    xlab:'position, '+S.unit});
  polyline(ctx,b,xs,ys,0,S.W,-Y,Y,COL.pos,1.6);
}

/* ---- the layout of a medium view ---- */
function latGeo(ctx,W,H,M){
  const R=M.L.R, light=(M.view==='light'), narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const fit=fitCaption(ctx,W,H-HINT_H,latCaption(M,true),latCaption(M,false),capW,top+220);
  const avail=fit.capY-18-top;
  const showScr=light&&ST.screen, showI=light&&ST.inten;
  let gH=ST.graph?Math.max(64,Math.min(130,Math.round(avail*0.2))):0;
  const gGap=44;
  /* what has to fit under the square: the graph and its axis labels, or the
     intensity graph's labels, or the generator's button — measured, never guessed */
  const below=()=>Math.max(gH?gH+gGap+36:0, showI?38:0, GEN_H/2+14+BTN_R+16);
  if(gH&&avail-below()<150) gH=0;
  const rightNeed=(showScr?40:0)+(showI?(narrow?120:190):0);
  const left=GEN_W+20;
  const side=Math.max(100,Math.floor(Math.min(avail-below(), W-left-30-rightNeed, narrow?W:W*0.6)));
  const sq=box(left,top,side,side);
  const G={sq,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,narrow};
  let xr=sq.x1+14;
  if(showScr){ G.scr=box(xr,sq.y,22,sq.h); xr+=34; }
  if(showI){ G.ib=box(xr,sq.y,(narrow?100:160),sq.h); xr=G.ib.x1+16; }
  if(ST.graph&&gH) G.gb=box(sq.x,sq.y1+gGap,sq.w,gH);
  G.graphDropped=ST.graph&&!gH;
  /* the wave meter's chart goes below the floating readout (which reaches ~480 px) */
  if(ST.meter&&!narrow){
    const x0=Math.max(xr+44,sq.x1+60), y0=510, y1=fit.capY-40;
    if(W-24-x0>=150&&y1-y0>=60) G.mb=box(x0,y0,W-24-x0,y1-y0);
  }
  return G;
}
function latCaption(M,full){
  const L=M.L, R=L.R, S=L.S, v=M.view;
  const base=S.name+': '+fmt(S.W,0)+' '+S.unit+' across, 111 lattice cells of '+sigf(L.dx,3)+' '+S.unit
    +'; colour is the '+S.what+' (±2.14 in lattice units is full colour, PhET’s scale).';
  if(!full) return base;
  let s=base+' One hard source five cells in from the left edge, driven at 1.2 × the amplitude; the waves leave through the absorbing edge 20 cells beyond the frame.';
  if(!L.active) s+=(L.mode==='pulse'?' No pulse is running — press the button to fire one.':' The source is off — press its button. The waves already made carry on without it.');
  if(L.R.A===0) s+=' The amplitude is zero: the source is running and moving nothing.';
  if(v==='water'&&ST.look==='side') s+=' Side view along the centre row: the height is the water level in lattice units, exaggerated, not to scale with the tank, and clipped where the source cell itself swings past ±1.8 of the colour scale.';
  if(v==='sound'&&ST.soundView!=='waves') s+=' Air parcels are pushed along ∇p, exaggerated: a wave at full colour moves one 0.3 of the parcel spacing, and beside the source, where the field is stronger than that, about 0.4. They crowd where the pressure is high and never travel with the wave; the cyan one is there to be watched jiggling in place.';
  if(v==='light'&&ST.screen) s+=' The screen at the right edge is PhET’s: the mean square of the last column, smoothed over three rows, averaged over ±39 rows, then PhET’s brightness table.';
  if(v==='light'&&ST.inten) s+=' The intensity graph (green) is not in PhET’s Waves Intro; orange is the 1/r a point source would give, and the ripple on it is the tank’s own edges.';
  return s;
}
function drawMediumView(ctx,W,H,M){
  const G=latGeo(ctx,W,H,M), sq=G.sq, L=M.L, R=L.R, S=L.S, v=M.view;
  if(v==='water'&&ST.look==='side') drawSideIntro(ctx,sq,L);
  else {
    if(!(v==='sound'&&ST.soundView==='particles')) drawField(ctx,sq,R);
    else { ctx.fillStyle='#05070c'; ctx.fillRect(sq.x,sq.y,sq.w,sq.h); }
    if(v==='sound'&&ST.soundView!=='waves') drawParcelsIntro(ctx,sq,R);
  }
  frame(ctx,sq,'#2a3040');
  drawGenerator(ctx,W,H,sq,L);
  /* PhET's scale bar and its clock */
  const sb=S.scaleLen/S.W*sq.w, yb=sq.y-10;
  ctx.fillStyle='#cfd4de'; ctx.fillRect(sq.x,yb-2,sb,3);
  lab(ctx,W,H,sq.x+sb+6,yb,S.scaleLen+' '+S.unit,'#cfd4de',SM_FONT,'left');
  const conv=sq.w<380?'':(S.tunit==='ms'?'  (1 ms = 10⁻³ s)':S.tunit==='fs'?'  (1 fs = 10⁻¹⁵ s)':'');
  lab(ctx,W,H,sq.x1,yb,(ST.running?'':'paused · ')+'t = '+sigf(R.t,3)+' '+S.tunit+conv,'#8b93a6',SM_FONT,'right');
  if(ST.tape) drawTape(ctx,W,H,sq,S,L);
  if(ST.meter) drawProbes(ctx,sq);
  if(ST.watch){
    const t='stopwatch '+sigf(R.watch.t,4)+' '+S.tunit, tw=t.length*11*0.52+14;
    ctx.fillStyle='rgba(10,12,18,.8)'; ctx.fillRect(sq.x1-tw-6,sq.y+6,tw,20);
    lab(ctx,W,H,sq.x1-tw+1,sq.y+16,t,R.watch.on?COL.pos:'#cfd4de',LAB_FONT,'left');
  }
  if(G.scr) drawScreenStrip(ctx,G.scr,L);
  if(G.ib) drawIntensity(ctx,W,H,G.ib,L);
  if(G.gb) drawCentre(ctx,W,H,G.gb,L);
  if(G.mb) drawMeterIntro(ctx,W,H,G.mb,L);
  const note=(y,t)=>{ ctx.fillStyle='rgba(7,11,24,.78)'; ctx.fillRect(sq.x+4,y-8,t.length*10.5*0.52+10,16);
    lab(ctx,W,H,sq.x+8,y,t,'#aeb6c6',SM_FONT,'left'); };
  if(!G.mb&&ST.meter) note(sq.y1-12,'wave meter: widen the window to see its chart');
  if(G.graphDropped) note(sq.y1-(ST.meter&&!G.mb?30:12),'graph: needs a taller window');
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ================================================================== *
 *  the three media: v = f lambda, and the wavelength measured on the  *
 *  lattice                                                            *
 * ================================================================== */
function pow10(e){ return '10'+supTxt(Math.round(e)); }
const PLANE={x0:-1, x1:16, y0:-7, y1:1};
const STRIP_MIN=76;
function mediaGeo(ctx,W,H,M){
  const narrow=isNarrow(W), top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-RO_W-44)-56));
  const full=mediaCaption(M,true), short=mediaCaption(M,false);
  const right=narrow?W-26:W-RO_W-44;
  const strips=(capY)=>{
    /* the strips sit below the floating readout; how much is left after the caption? */
    const planeH=Math.max(120,Math.min(Math.round(0.42*(capY-top)),486-44-top));
    const y2=Math.max(top+10+planeH+66,510);
    return {planeH,y2,h2:capY-46-y2};
  };
  let fit=fitCaption(ctx,W,H-HINT_H,full,short,capW,top+200), s=strips(fit.capY);
  /* a caption long enough to squeeze the strips out takes the short form instead — the
     strips are the measurement, and the caption's job is to explain them */
  if(!narrow&&s.h2<STRIP_MIN&&full!==short){
    const f2=fitCaption(ctx,W,H-HINT_H,short,short,capW,top+200), s2=strips(f2.capY);
    if(s2.h2>=STRIP_MIN){ fit=f2; s=s2; }
  }
  const G={capY:fit.capY,capTxt:fit.txt,capW:fit.capW,narrow,strips:[]};
  if(narrow){
    G.plane=box(64,top+10,Math.max(140,right-80),Math.max(90,fit.capY-62-top));
    return G;
  }
  G.plane=box(64,top+10,Math.max(160,right-74),s.planeH);
  if(s.h2>=STRIP_MIN){
    const gut=56, span=(W-24)-64, w=(span-2*gut)/3;
    for(let i=0;i<3;i++) G.strips.push(box(64+i*(w+gut),s.y2,w,s.h2));
  }
  return G;
}
function mediaCaption(M,full){
  /* the speeds are read off the model, never typed twice */
  const base='v = fλ for the three media, on log scales: a fixed speed is a straight line of slope −1, and the three media are three parallel lines ('
    +M.X.rows.map(q=>q.S.name+' '+sciTxt(q.vSI,3)+' m/s').join(', ')+').';
  if(!full) return base;
  return base+' The thick cyan stretch of each line is the range PhET’s slider covers, the magenta ring is where it is set now, and the green dot is the wavelength MEASURED on the lattice at that setting.'
    +' Below, for each medium, the tank at steady state along the axis, from 5 cells out: green is the lattice, orange the 1/√r a spreading 2-D wave must follow, the cyan band the cells the fit uses, and the magenta arrow the wavelength it returns.';
}
function drawMedia(ctx,W,H,M){
  const G=mediaGeo(ctx,W,H,M), b=G.plane, rows=M.X.rows;
  const xt=[], yt=[];
  for(let e=0;e<=16;e+=2) xt.push(e);
  for(let e=PLANE.y0;e<=PLANE.y1;e++) yt.push(e);
  axesR(ctx,b,PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,{xticks:xt,yticks:yt,xfmt:pow10,yfmt:pow10,
    title:titleFor(b,'wavelength against frequency: λ = v/f, one line per medium','λ = v/f'),
    xlab:'frequency f, Hz',ylab:'wavelength λ, m'});
  for(const q of rows){
    const lv=Math.log10(q.vSI);
    /* the law, drawn right across the plane: log lambda = log v - log f */
    polyline(ctx,b,[PLANE.x0,PLANE.x1],[lv-PLANE.x0,lv-PLANE.x1],PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,COL.ref,1.3,[5,4]);
    /* the stretch PhET's own slider covers */
    const fa=Math.log10(q.S.fmin/SI_TIME[q.id]), fb=Math.log10(q.S.fmax/SI_TIME[q.id]);
    polyline(ctx,b,[fa,fb],[lv-fa,lv-fb],PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,COL.struct,4);
    marker(ctx,b,PLANE.x0,PLANE.x1,PLANE.y0,PLANE.y1,Math.log10(q.fSI),Math.log10(q.lamSI),COL.live);
    const mx=Math.log10(q.fSI), my=Math.log10(q.m.lam*SI_LEN[q.id]);
    dot(ctx,b.x+b.w*(mx-PLANE.x0)/(PLANE.x1-PLANE.x0),b.y1-b.h*(my-PLANE.y0)/(PLANE.y1-PLANE.y0),3.4,COL.pos);
  }
  /* the legend goes in the clear band between the plane and the strips: every corner of the
     plane itself is crossed by one of the three lines, so legendAuto would rightly refuse */
  if(b.w>=320&&G.strips.length){
    const lb=legendBox(ctx,b.x,b.y1+46,[[COL.ref,'λ = v/f'],[COL.struct,'PhET’s slider range'],
                                        [COL.live,'set now'],[COL.pos,'measured on the lattice']]);
    if(lb) LABELS.push([lb.x,lb.y,lb.x1,lb.y1]);
  }
  /* the labels last, so they dodge each other rather than the curves; a label that would run
     off the panel's right edge (and so under the floating readout) is hung to the left instead */
  ctx.font=LAB_FONT;
  /* the lines fall one decade of lambda per decade of f, so a label set above-RIGHT of a marker
     is clear of its own line; light's marker sits near the right-hand edge and near the floor,
     where the label has to hang to the LEFT — and there it must also clear the rise of the line
     it is naming (slope px/px below), or it lies along it.  Where even the medium's name will
     not fit, no label is drawn: the caption and the readout still name all three speeds. */
  const slope=(b.h/(PLANE.y1-PLANE.y0))/(b.w/(PLANE.x1-PLANE.x0));
  for(const q of rows){
    const lv=Math.log10(q.vSI), fm=0.5*(Math.log10(q.S.fmin/SI_TIME[q.id])+Math.log10(q.S.fmax/SI_TIME[q.id]));
    const X=b.x+b.w*(fm-PLANE.x0)/(PLANE.x1-PLANE.x0), Y=b.y1-b.h*((lv-fm)-PLANE.y0)/(PLANE.y1-PLANE.y0);
    for(const txt of [q.S.name+' · '+sciTxt(q.vSI,3)+' m/s',q.S.name]){
      const w=ctx.measureText(plain(txt)).width;
      if(X+10+w<=b.x1-2){ lab(ctx,W,H,X+10,Y-12,txt,COL.struct,LAB_FONT,'left'); break; }
      const up=(10+w)*slope+12;
      if(X-10-w>=b.x+2&&Y-up>=b.y+8){ lab(ctx,W,H,X-10,Y-up,txt,COL.struct,LAB_FONT,'right'); break; }
    }
  }
  /* the strips: the tank at steady state along its axis */
  G.strips.forEach((sb,i)=>{
    const q=rows[i], m=q.m, R0=MEAS.R0, R1=MEAS.R1, dx=q.dx;
    const x0=5*dx, x1=(m.nc-1)*dx, Y=1.15*m.amp[5];
    axesR(ctx,sb,x0,x1,-Y,Y,{nx:4,ny:3,xfmt:t=>sigf(t,3),yfmt:t=>fmt(t,1),
      title:titleFor(sb,q.S.name+' at '+freqStr(q.S,q.f)+', along the axis',q.S.name),
      xlab:'distance from the source, '+q.S.unit});
    /* the cells the fit uses */
    const px=x=>sb.x+sb.w*(x-x0)/(x1-x0);
    ctx.fillStyle=rgba(COL.struct,0.1); ctx.fillRect(px(R0*dx),sb.y,px(R1*dx)-px(R0*dx),sb.h);
    const xs=[], us=[], ep=[], em=[];
    for(let c=5;c<m.nc;c++){ const x=c*dx; xs.push(x); us.push(m.snap[c]); ep.push(m.afit/Math.sqrt(c)); em.push(-m.afit/Math.sqrt(c)); }
    polyline(ctx,sb,xs,ep,x0,x1,-Y,Y,COL.ref,1.2,[4,3]);
    polyline(ctx,sb,xs,em,x0,x1,-Y,Y,COL.ref,1.2,[4,3]);
    polyline(ctx,sb,xs,us,x0,x1,-Y,Y,COL.pos,1.5);
    /* the measured wavelength, drawn from the crest nearest the middle of the fit; at the long
       end of water the tank does not hold a whole wavelength past that crest, and then the
       figure is given without the arrow rather than drawn off the end of the strip */
    let cr=-1;
    for(let c=Math.round((R0+R1)/2);c<R1-2;c++) if(m.snap[c]>m.snap[c-1]&&m.snap[c]>=m.snap[c+1]){ cr=c; break; }
    const ya=sb.y+sb.h*0.16;
    if(cr>0&&cr+m.lamCells<=m.nc-1){
      const xA=px(cr*dx), xB=px((cr+m.lamCells)*dx);
      ctx.beginPath(); ctx.moveTo(xA,ya); ctx.lineTo(xB,ya);
      ctx.moveTo(xA,ya); ctx.lineTo(xA+6,ya-4); ctx.moveTo(xA,ya); ctx.lineTo(xA+6,ya+4);
      ctx.moveTo(xB,ya); ctx.lineTo(xB-6,ya-4); ctx.moveTo(xB,ya); ctx.lineTo(xB-6,ya+4);
      ctx.strokeStyle=COL.live; ctx.lineWidth=1.6; ctx.stroke();
      lab(ctx,W,H,(xA+xB)/2,ya-11,'λ = '+lenU(m.lam,q.S),COL.live,SM_FONT,'center');
    } else {
      lab(ctx,W,H,sb.x+sb.w*0.55,ya,'λ = '+lenU(m.lam,q.S)+' — longer than the tank',COL.live,SM_FONT,'center');
    }
    /* the footer, in the longest form the strip can hold */
    ctx.font=SM_FONT;
    const pw=fmt(m.pexp,2).replace('-','−');          /* one minus sign in a line of prose */
    const long='v/f = '+lenU(m.lam0,q.S)+' · measured '+pct(m.err)+' · power '+pw+' (1/√r: −0.50)';
    const shortF='measured '+pct(m.err)+' · power '+pw;
    lab(ctx,W,H,sb.x+4,sb.y1-9,ctx.measureText(plain(long)).width<=sb.w-10?long:shortF,'#8b93a6',SM_FONT,'left');
  });
  if(!G.strips.length&&!G.narrow) lab(ctx,W,H,G.plane.x,G.plane.y1+30,'the three tanks: a taller window shows them','#8b93a6',SM_FONT,'left');
  drawCaption(ctx,{left:56,capY:G.capY,capTxt:G.capTxt,capW:G.capW});
  return G;
}

/* ================================================================== *
 *  dispatch and the scene object                                      *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.L) return drawMediumView(ctx,W,H,M);
  return drawMedia(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* only a medium view has a clock; the three media are a still picture */
  S.step=function(){ return MEDIA[ST.view]?clockFrame()>0:false; };
  /* the pointer: PhET's generator button, the tape's ends and the probes */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    if(!MEDIA[ST.view]) return false;
    const ctx=canvas.getContext('2d'), M=buildModel(), G=latGeo(ctx,S.W,S.H,M), sq=G.sq, R=M.L.R;
    if(type==='down'){
      const g=genGeo(sq,R);
      if(Math.hypot(x-g.btn.x,y-g.btn.y)<g.btn.r+3){ DRAG.what='button'; return pressSource(R); }
      const hits=[];
      if(ST.tape) TOOLS.tape.forEach((p,q)=>hits.push(['tape'+q,sq.x+p[0]*sq.w,sq.y+p[1]*sq.h]));
      if(ST.meter) TOOLS.probes.forEach((p,q)=>hits.push(['probe'+q,sq.x+p[0]*sq.w,sq.y+p[1]*sq.h]));
      for(const h2 of hits) if(Math.hypot(x-h2[1],y-h2[2])<10){ DRAG.what=h2[0]; return true; }
      return false;
    }
    if(type==='move'){
      if(!DRAG.what||DRAG.what==='button') return false;
      const q=+DRAG.what.slice(-1), arr=DRAG.what.indexOf('tape')===0?TOOLS.tape:TOOLS.probes;
      arr[q]=[clamp((x-sq.x)/sq.w,0,1),clamp((y-sq.y)/sq.h,0,1)];
      return true;
    }
    return false;
  };
  return S;
}
