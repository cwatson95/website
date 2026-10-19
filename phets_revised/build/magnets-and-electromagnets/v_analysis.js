
/* ================================================================== *
 *  the analysis views: field lines, on the axis, the far field, the   *
 *  needle                                                             *
 * ================================================================== */
const SUPS={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
function pow10Label(e){ return '10'+String(e).split('').map(c=>SUPS[c]).join(''); }
function viewBack(ctx,W,H){ ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H); LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[]; }
/* the house stage layout, with the caption kept clear of the #hint line */
function stageLayoutH(ctx,W,H,full,short,nB,frac){
  const L=stageLayout(ctx,W,H-HINT_H,full,short,nB||0,frac||0.3);
  /* stageLayout leaves 16 px under a lone main panel, which is not enough for its x-tick
     labels (b.y1 + 5) and axis title (b.y1 + 21): give them 34 */
  if(!nB) L.main=box(L.main.x,L.main.y,L.main.w,Math.max(80,L.main.h-34));
  return L;
}
/* axesR with tick counts from the box, and the lowest y label dropped when it would share the
   bottom-left corner with the first x label (the y labels hang ~28 px left of the frame, so the
   corner belongs to both: Known-bad, a tick gutter is part of a panel's footprint) */
function tickFmt(ticks){
  let g=Infinity;
  for(let i=1;i<ticks.length;i++) g=Math.min(g,Math.abs(ticks[i]-ticks[i-1]));
  const d=Math.max(0,Math.min(4,Math.ceil(-Math.log10(g||1))));
  return t=>fmt(t,d);
}
function axesQ(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o={}; for(const k in (opt||{})) o[k]=opt[k];
  if(!o.xticks) o.xticks=ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),b.w<430?4:(o.nx||6));
  if(!o.yticks) o.yticks=ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),b.h<250?3:(o.ny||5));
  o.yticks=o.yticks.filter(t=>b.y1-b.h*(t-ylo)/(yhi-ylo||1)<b.y1-11);
  if(!o.xfmt) o.xfmt=tickFmt(o.xticks);
  if(!o.yfmt) o.yfmt=tickFmt(o.yticks);
  axesR(ctx,b,xlo,xhi,ylo,yhi,o);
}
/* log ticks with 2 and 5 between the decades when the span is short, so a two-decade axis
   is not labelled twice */
function logTicksFine(lo,hi,wpx){
  const dec=decadeTicks(lo,hi,wpx);
  if(Math.floor(hi)-Math.ceil(lo)>3||wpx<380) return dec;
  const out=[];
  for(let e=Math.floor(lo)-1;e<=Math.ceil(hi);e++) for(const m of [1,2,5]){
    const v=e+Math.log10(m); if(v>=lo-1e-9&&v<=hi+1e-9) out.push(v); }
  return out.length>=3?out:dec;
}
const logLabel=t=>t>=4?pow10Label(Math.round(t)):sigf(Math.pow(10,t),2);
/* decade ticks, thinned so their labels cannot touch on a short axis */
function decadeTicks(lo,hi,hpx){
  const n=Math.floor(hi)-Math.ceil(lo)+1, step=Math.max(1,Math.ceil(15*n/Math.max(1,hpx)));
  const out=[]; for(let e=Math.ceil(lo);e<=Math.floor(hi);e+=step) out.push(e);
  return out.length?out:[Math.round((lo+hi)/2)];
}
function scaleBar(ctx,map,b,mm,label){
  const X0=b.x+14, Y0=b.y1-14, len=mm*map.s;
  if(len>b.w*0.5) return;
  ctx.beginPath(); ctx.moveTo(X0,Y0); ctx.lineTo(X0+len,Y0); ctx.moveTo(X0,Y0-4); ctx.lineTo(X0,Y0+4); ctx.moveTo(X0+len,Y0-4); ctx.lineTo(X0+len,Y0+4);
  ctx.strokeStyle='#8b93a6'; ctx.lineWidth=1; ctx.stroke();
  ctx.font=SM_FONT; ctx.textAlign='left'; ctx.textBaseline='bottom'; ctx.fillStyle='#8b93a6'; ctx.fillText(label,X0,Y0-6);
  LABELS.push([X0,Y0-6-12,X0+label.length*10.5*0.52,Y0-6]);
}

/* ---------------- field lines ---------------- */
/* what each source contributes to the analysis views: the frame it wants, what it says about
   itself, how its body is drawn, and its curve on the axis.  The coil's entry is stripped from
   pages that have no electromagnet. */
const ANA_SRC={
  magnet:{
    extent:{xr:430,yr:270}, axisRange:520,
    body:(ctx,map,A)=>drawBarMagnet(ctx,map,{x:0,y:0,ang:0,S:A.unit},{ghost:true,bound:ST.bound}),
    title:A=>'the bar magnet, '+fB(A.unit),
    /* B and mu0 H = B - mu0 M inside, and the point dipole outside the bar */
    axisPoint:(A,x,C)=>{ const b=A.unit*solAxis(x,MAG_R,MAG_B);
      C.B.push(b); C.Hh.push(Math.abs(x)<MAG_B?b-A.unit:b);
      C.dip.push(Math.abs(x)>MAG_B*1.05?2*A.unit*MAG_DIP/Math.pow(Math.abs(x),3):NaN); },
    axisMarks:A=>[-MAG_B,MAG_B],                 /* the pole faces, where B passes through and H jumps */
    marks:(ctx,map,A)=>{},
    linesCap:'Field lines of B in the page, which contains the magnet’s axis, so each is an exact line in its plane. They are seeded at equal flux across the middle of the magnet: between neighbouring lines, as rings round the axis, runs the same flux. Every line leaves the north face, returns to the south face and runs back through the magnet; B lines never end. Inside, all ten are packed into the bar’s 50 mm, which is what a strong field is: the flux that spreads over metres outside is concentrated there.',
    /* said only while it is drawn: a caption must not describe what a checkbox has hidden */
    boundCap:()=>ST.bound?' Dots and crosses: the bound current K = M × n on the side wall, which is all a solenoid needs to make exactly this field.':'',
    off:'strength 0: no field, no lines',
  },
};
/* #emag */
ANA_SRC.coil={
  extent:{xr:260,yr:165}, axisRange:260,
  body:(ctx,map,A)=>{},
  title:A=>'the electromagnet, '+ST.loops+' loop'+(ST.loops>1?'s':'')+', I = '+plain(fI(A.I||0)),
  /* the loops add; the reference is the continuous sheet with the same ampere-turns */
  axisPoint:(A,x,C)=>{ let s=0; for(const xk of coilLoopsX(A.N)) s+=loopAxis(x-xk,COIL_A);
    C.B.push(A.unit*s); C.ref.push(A.unit*solAxis(x,COIL_A,A.N*COIL_PITCH/2)/COIL_PITCH); },
  axisMarks:A=>coilLoopsX(A.N),                  /* where the turns sit */
  marks:(ctx,map,A)=>{
    const xs=coilLoopsX(A.N), r=Math.max(3,WIRE_R*map.s), on=A.unit!==0, sgn=A.unit<0?-1:1;
    for(const x of xs) for(const top of [true,false]){
      const X=map.X(x), Y=map.Y(top?COIL_A:-COIL_A);
      dot(ctx,X,Y,r,mix('#070b18',COL.copper,0.8),'#070b18',1);
      if(!on) continue;
      if((top?1:-1)*sgn>0) dot(ctx,X,Y,r*0.3,'#070b18');
      else { ctx.beginPath(); ctx.moveTo(X-r*0.55,Y-r*0.55); ctx.lineTo(X+r*0.55,Y+r*0.55);
             ctx.moveTo(X-r*0.55,Y+r*0.55); ctx.lineTo(X+r*0.55,Y-r*0.55); ctx.strokeStyle='#070b18'; ctx.lineWidth=1.4; ctx.stroke(); }
    }
  },
  linesCap:'Field lines of B in the page, which contains the coil’s axis, seeded at equal flux across the coil’s middle: between neighbours, as rings round the axis, runs the same flux. The wires’ cross-sections show the current, out of the page (dot) and into it (cross).',
  boundCap:()=>'',
  off:'no current, so no field and no lines',
};
/* #endemag */
function linesExtent(kind){ return ANA_SRC[kind].extent; }
function linesGeo(ctx,W,H,M){
  const L=stageLayoutH(ctx,W,H,LINES_CAP(M,true),LINES_CAP(M,false),0), e=linesExtent(M.as.kind);
  const map=worldFitUp(L.main,{xmin:-e.xr,xmax:e.xr,ymin:-e.yr,ymax:e.yr},0);
  return {L,map,e};
}
function LINES_CAP(M,full){
  const F=M.fl, out=F.lines.filter(l=>Math.max(...l.pts.map(p=>Math.abs(p[1])))>linesExtent(M.as.kind).xr||Math.max(...l.pts.map(p=>p[0]))>linesExtent(M.as.kind).yr).length;
  const tail=out?' '+out+' of the '+F.lines.length+' lines on each side reach beyond this frame before they turn back.':'';
  const bc=ANA_SRC[M.as.kind].boundCap();
  if(!full) return 'Field lines of B in the page, which contains the axis; equal flux between neighbours.'+(bc?' Dots and crosses: the bound current.':'')+(out?' '+out+' reach beyond the frame.':'');
  return ANA_SRC[M.as.kind].linesCap+bc+tail;
}
function drawLinesView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const G=linesGeo(ctx,W,H,M), map=G.map, b=G.L.main, F=M.fl, A=M.as;
  ctx.fillStyle='#090e1c'; ctx.fillRect(b.x,b.y,b.w,b.h); frame(ctx,b,'#1a2032');
  /* the axis */
  ctx.setLineDash([4,5]); ctx.beginPath(); ctx.moveTo(b.x,map.Y(0)); ctx.lineTo(b.x1,map.Y(0)); ctx.strokeStyle='#2a3142'; ctx.lineWidth=1; ctx.stroke(); ctx.setLineDash([]);
  const on=A.unit!==0;
  const sgn=A.unit<0?-1:1;
  /* the source goes down FIRST, see-through, so the lines running through it stay visible */
  ANA_SRC[A.kind].body(ctx,map,A);
  if(on){
    for(const l of F.lines){
      for(const side of [1,-1]){
        const pts=linePts(map,0,0,0,l.pts,side);
        strokeClipped(ctx,b,pts,COL.north,1.35);
        lineArrow(ctx,b,pts,0.18,COL.north,sgn); lineArrow(ctx,b,pts,0.62,COL.north,sgn);
      }
    }
  }
  ANA_SRC[A.kind].marks(ctx,map,A);
  if(!on) lab(ctx,W,H,b.x+b.w/2,b.y+24,ANA_SRC[A.kind].off,COL.dim,LAB_FONT,'center','middle');
  scaleBar(ctx,map,b,100,'100 mm');
  axesTitle(ctx,b,ANA_SRC[A.kind].title(A));
  drawCaption(ctx,G.L);
}
function axesTitle(ctx,b,t){
  ctx.font='italic 13px Georgia, serif'; ctx.textAlign='left'; ctx.textBaseline='bottom'; ctx.fillStyle='#aeb6c6';
  const tt=plain(t); ctx.fillText(tt,b.x,b.y-9); LABELS.push([b.x,b.y-9-13*1.15,b.x+tt.length*13*0.52,b.y-9]);
}

/* ---------------- on the axis ---------------- */
/* A FUNCTION, not a const: half of the magnet's caption is about mu0 H, which has its own
   checkbox, and a caption built once at load cannot follow one. */
function axisCap(k){
/* #emag */
  if(k==='coil') return ['Along the coil’s axis each loop gives μ₀I a²/2(a² + x²)^(3/2) and the loops simply add (green). Orange: a continuous current sheet of the same length and ampere-turns, the solenoid the loops approximate; the N-loop sum tends to it as the midpoint rule does, the error falling as the square of the pitch.',
        'On the axis: the loops add (green); orange: the continuous sheet with the same ampere-turns.'];
/* #endemag */
  const h=ST.axisH;
  return ['Along the magnet’s axis the field is elementary: B is ½μ₀M times the difference of the two faces’ cosines, continuous through the pole faces, strongest at the centre (cos α = 0.981 of μ₀M) and half that at a face.'
          +(h?' μ₀H = B − μ₀M inside (cyan): it jumps by μ₀M at each face and points backwards, from N to S, inside the magnet.':'')
          +' Far away B falls as the dipole, 2(μ₀m/4π)/x³ (orange).',
          'On the axis: B continuous through the faces;'+(h?' μ₀H jumps by μ₀M there and points backwards inside;':'')+' orange: the point dipole.'];
}
function axisGeo(ctx,W,H,M){ const c=axisCap(M.as.kind); return stageLayoutH(ctx,W,H,c[0],c[1],0); }
function axisCurves(M){
  const A=M.as, n=801, xs=[], B=[], Hh=[], dip=[], ref=[], xr=ANA_SRC[A.kind].axisRange;
  for(let i=0;i<n;i++){
    const x=-xr+2*xr*i/(n-1); xs.push(x);
    ANA_SRC[A.kind].axisPoint(A,x,{B,Hh,dip,ref});
  }
  return {xs,B,Hh,dip,ref,xr};
}
function drawAxisView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const L=axisGeo(ctx,W,H,M), b=L.main, A=M.as, C=axisCurves(M);
  let lo=0, hi=0;
  for(const arr of [C.B,C.Hh,C.ref]) for(const v of arr) if(isFinite(v)){ lo=Math.min(lo,v); hi=Math.max(hi,v); }
  if(!(hi>lo)){ hi=1; lo=-1; }
  const pad=0.08*(hi-lo); lo-=pad; hi+=pad;
  axesQ(ctx,b,-C.xr,C.xr,lo,hi,{xlab:'x along the axis, mm',ylab:'field on the axis, G',title:A.kind==='magnet'?(ST.axisH?'B and μ₀H along the magnet’s axis':'B along the magnet’s axis'):'B along the coil’s axis',nx:8,ny:6});
  /* the source's extent */
  const X=x=>b.x+b.w*(x+C.xr)/(2*C.xr), Y0=b.y1-b.h*(0-lo)/(hi-lo);
  ctx.setLineDash([3,4]); ctx.strokeStyle='#39415a'; ctx.lineWidth=1;
  for(const f of ANA_SRC[A.kind].axisMarks(A)){ ctx.beginPath(); ctx.moveTo(X(f),b.y); ctx.lineTo(X(f),b.y1); ctx.stroke(); }
  ctx.setLineDash([]);
  if(Y0>b.y&&Y0<b.y1){ ctx.beginPath(); ctx.moveTo(b.x,Y0); ctx.lineTo(b.x1,Y0); ctx.strokeStyle='#2a3142'; ctx.stroke(); }
  const items=[];
  if(A.kind==='magnet'){
    polyline(ctx,b,C.xs,C.dip,-C.xr,C.xr,lo,hi,COL.ref,1.3,[6,4]); items.push([COL.ref,'point dipole, 2(μ₀m/4π)/x³']);
    if(ST.axisH){
      /* H breaks at the faces: draw it in three pieces so the jumps are not joined */
      for(const [a0,a1] of [[-C.xr,-MAG_B],[-MAG_B,MAG_B],[MAG_B,C.xr]]){
        const xs=[], hs=[]; C.xs.forEach((x,i)=>{ if(x>a0+1e-9&&x<a1-1e-9){ xs.push(x); hs.push(C.Hh[i]); } });
        polyline(ctx,b,xs,hs,-C.xr,C.xr,lo,hi,COL.struct,1.5);
      }
      items.push([COL.struct,'μ₀H = B − μ₀M inside']);
    }
    polyline(ctx,b,C.xs,C.B,-C.xr,C.xr,lo,hi,COL.north,2); items.push([COL.north,'B, exact']);
  } else {
    polyline(ctx,b,C.xs,C.ref,-C.xr,C.xr,lo,hi,COL.ref,1.4,[6,4]); items.push([COL.ref,'continuous sheet, same N I']);
    polyline(ctx,b,C.xs,C.B,-C.xr,C.xr,lo,hi,COL.north,2); items.push([COL.north,A.N+' loop'+(A.N>1?'s':'')+', Biot–Savart']);
  }
  legendAuto(ctx,b,items);
  if(A.unit===0) lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2-20,A.kind==='magnet'?'strength 0: no field':'no current: no field',COL.dim,LAB_FONT,'center','middle');
  drawCaption(ctx,L);
}

/* #far */
/* ---------------- the far field ---------------- */
const FAR_CAP=['Top: |B| along the axis and on the bisector against distance from the centre, both axes logarithmic; orange dashed, the point dipole with the source’s own moment. Below: how far each is from the dipole, |B/B_dip − 1|, which falls as C/r² (slope −2, orange: the octupole closed forms). The limits r³B/B_dip → 1 are taken numerically in the readout.',
  'Log–log: |B| on the axis and bisector against the point dipole (orange); below, |B/B_dip − 1| against C/r².'];
function farGeo(ctx,W,H){ return stageLayoutH(ctx,W,H,FAR_CAP[0],FAR_CAP[1],1,0.42,1); }
function farCurves(M){
  const A=M.as, r0=A.kind==='magnet'?150:70, r1=10000, n=160, rs=[], ax=[], eq=[], dax=[], deq=[], rax=[], req=[];
  for(let i=0;i<n;i++){
    const r=r0*Math.pow(r1/r0,i/(n-1)); rs.push(r);
    const fa=farField(A.kind,A.N,r,'axis'), fe=farField(A.kind,A.N,r,'bis');
    ax.push(Math.abs(fa*A.unit)); eq.push(Math.abs(fe*A.unit));
    dax.push(Math.abs(dipPred(A.kind,A.N,r,'axis')*A.unit)); deq.push(Math.abs(dipPred(A.kind,A.N,r,'bis')*A.unit));
    rax.push(Math.abs(fa/dipPred(A.kind,A.N,r,'axis')-1)); req.push(Math.abs(fe/dipPred(A.kind,A.N,r,'bis')-1));
  }
  return {rs,ax,eq,dax,deq,rax,req,r0,r1};
}
function drawFarView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const L=farGeo(ctx,W,H), b=L.main, A=M.as, C=farCurves(M);
  const lg=v=>v>0?Math.log10(v):NaN;
  const lx=C.rs.map(lg);
  if(A.unit===0){
    /* no field to draw: keep BOTH frames the view promises, with the same decade axes, and
       say why they are empty (Known-bad: a view that quietly draws less than its caption
       describes, and axis labels that fall back to raw logarithms) */
    const xt0=logTicksFine(lx[0],lx[lx.length-1],b.w), yt0=decadeTicks(-6,2,b.h);
    axesQ(ctx,b,lx[0],lx[lx.length-1],-6,2,{title:'|B| against distance from the centre',xlab:'distance r, mm (log scale)',
      ylab:'|B|, G (log scale)',xticks:xt0,yticks:yt0,xfmt:logLabel,yfmt:t=>pow10Label(t)});
    lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2,ANA_SRC[A.kind].off,COL.dim,LAB_FONT,'center','middle');
    if(L.bottom.length){ const bb=L.bottom[0];
      axesQ(ctx,bb,lx[0],lx[lx.length-1],-6,1,{title:'|B/B_dip − 1|: the approach to the dipole',xlab:'distance r, mm (log scale)',
        ylab:'|B/B_dip − 1| (log scale)',xticks:logTicksFine(lx[0],lx[lx.length-1],bb.w),yticks:decadeTicks(-6,1,bb.h),
        xfmt:logLabel,yfmt:t=>pow10Label(t)});
      lab(ctx,W,H,bb.x+bb.w/2,bb.y+bb.h/2,'nothing to compare with a dipole',COL.dim,LAB_FONT,'center','middle'); }
    drawCaption(ctx,L); return; }
  const ys=[...C.ax,...C.eq].map(lg).filter(isFinite);
  let lo=Math.floor(Math.min(...ys)), hi=Math.ceil(Math.max(...ys));
  const xt=logTicksFine(lx[0],lx[lx.length-1],b.w), yt=decadeTicks(lo,hi,b.h);
  axesQ(ctx,b,lx[0],lx[lx.length-1],lo,hi,{title:'|B| against distance from the centre',xlab:'distance r, mm (log scale)',ylab:'|B|, G (log scale)',
    xticks:xt,yticks:yt,xfmt:logLabel,yfmt:t=>pow10Label(t)});
  polyline(ctx,b,lx,C.dax.map(lg),lx[0],lx[lx.length-1],lo,hi,COL.ref,1.3,[6,4]);
  polyline(ctx,b,lx,C.deq.map(lg),lx[0],lx[lx.length-1],lo,hi,COL.ref,1.3,[2,4]);
  polyline(ctx,b,lx,C.ax.map(lg),lx[0],lx[lx.length-1],lo,hi,COL.north,2);
  polyline(ctx,b,lx,C.eq.map(lg),lx[0],lx[lx.length-1],lo,hi,COL.struct,2);
  legendAuto(ctx,b,[[COL.north,'on the axis'],[COL.struct,'on the bisector'],[COL.ref,'point dipole (dashed: axis, dotted: bisector)']]);
  if(L.bottom.length){
    const bb=L.bottom[0];
    const dv=[...C.rax,...C.req].map(lg).filter(isFinite);
    const dlo=Math.floor(Math.min(...dv)), dhi=Math.ceil(Math.max(...dv));
    const yt2=decadeTicks(dlo,dhi,bb.h), xt2=logTicksFine(lx[0],lx[lx.length-1],bb.w);
    axesQ(ctx,bb,lx[0],lx[lx.length-1],dlo,dhi,{title:'|B/B_dip − 1|: the approach to the dipole',xlab:'distance r, mm (log scale)',ylab:'|B/B_dip − 1| (log scale)',
      xticks:xt2,yticks:yt2,xfmt:logLabel,yfmt:t=>pow10Label(t)});
    const ca=Math.abs(octCoef(A.kind,A.N,'axis')), ce=Math.abs(octCoef(A.kind,A.N,'bis'));
    polyline(ctx,bb,lx,C.rs.map(r=>lg(ca/(r*r))),lx[0],lx[lx.length-1],dlo,dhi,COL.ref,1.2,[6,4]);
    polyline(ctx,bb,lx,C.rs.map(r=>lg(ce/(r*r))),lx[0],lx[lx.length-1],dlo,dhi,COL.ref,1.2,[2,4]);
    polyline(ctx,bb,lx,C.rax.map(lg),lx[0],lx[lx.length-1],dlo,dhi,COL.north,1.8);
    polyline(ctx,bb,lx,C.req.map(lg),lx[0],lx[lx.length-1],dlo,dhi,COL.struct,1.8);
    legendAuto(ctx,bb,[[COL.ref,'octupole C/r² (slope −2)']]);
  }
  drawCaption(ctx,L);
}

/* #endfar */
/* ---------------- the needle ---------------- */
const NEEDLE_CAP=['The compass needle released at an angle from a steady field, integrated as a damped rotor (green) against the small-swing solution (orange, dashed) and its decay envelope. Below: the period of small swings, 2π/√(κ|B|), falls as the inverse square root of the field (slope −½ on these log axes) — which is how Gauss measured the Earth’s field with a swinging magnet. The rotor and its constants are PhET’s model, not a measured compass.',
  'The damped rotor (green) against the small-swing solution (orange); below, the period ∝ |B|^(−½).'];
function needleGeo(ctx,W,H){ return stageLayoutH(ctx,W,H,NEEDLE_CAP[0],NEEDLE_CAP[1],1,0.38,1); }
function drawNeedleView(ctx,W,H,M){
  viewBack(ctx,W,H);
  const L=needleGeo(ctx,W,H), N=M.nd;
  const dial=L.narrow?null:box(L.main.x,L.main.y,Math.min(190,L.main.h),Math.min(190,L.main.h));
  const b=dial?box(dial.x1+64,L.main.y,L.main.x1-dial.x1-64,L.main.h):L.main;
  const lim=Math.max(N.rel,0.2)*R2D*1.12;
  axesQ(ctx,b,0,N.Tw,-lim,lim,{title:'needle angle from the field against time',xlab:'t, s',ylab:'φ − θ_B, degrees',nx:8,ny:6,xfmt:t=>fmt(t,t<10?1:0),yfmt:t=>fmt(t,0)});
  const env=N.ts.map(t=>N.rel*R2D*Math.exp(-N.gam*t/2));
  polyline(ctx,b,N.ts,env,0,N.Tw,-lim,lim,'#39415a',1,[2,3]); polyline(ctx,b,N.ts,env.map(v=>-v),0,N.Tw,-lim,lim,'#39415a',1,[2,3]);
  polyline(ctx,b,N.ts,N.lin.map(v=>v*R2D),0,N.Tw,-lim,lim,COL.ref,1.4,[6,4]);
  polyline(ctx,b,N.ts,N.ph.map(v=>v*R2D),0,N.Tw,-lim,lim,COL.north,2);
  legendAuto(ctx,b,[[COL.north,'damped rotor, integrated'],[COL.ref,'small-swing solution']]);
  /* the time cursor */
  const tt=Math.min(LIVE.ndT,N.Tw), Xc=b.x+b.w*tt/N.Tw;
  ctx.beginPath(); ctx.moveTo(Xc,b.y); ctx.lineTo(Xc,b.y1); ctx.strokeStyle=rgba(COL.live,0.5); ctx.lineWidth=1; ctx.stroke();
  const idx=Math.min(N.ph.length-1,Math.round(tt/N.Tw*(N.ph.length-1)));
  if(dial){
    const map={s:dial.w/100,X:x=>dial.x+dial.w/2+x*dial.w/100,Y:y=>dial.y+dial.h/2-y*dial.w/100};
    drawCompass(ctx,map,0,0,N.ph[idx]);
    arrowW(ctx,map,[-46,-46],[30,0],COL.ref,1.6);
    lab(ctx,W,H,dial.x+dial.w/2,dial.y1+12,'B →  (t = '+fmt(tt,2)+' s)',COL.dim,SM_FONT,'center','middle');
  }
  if(L.bottom.length){
    const bb=L.bottom[0], lB0=-2, lB1=Math.log10(S_MAX);
    const Bs=[], T0=[], Td=[];
    for(let i=0;i<=120;i++){ const lb=lB0+(lB1-lB0)*i/120, B=Math.pow(10,lb); Bs.push(lb); const w0=Math.sqrt(KAPPA*B); T0.push(Math.log10(2*Math.PI/w0));
      const d=w0*w0-N.gam*N.gam/4; Td.push(d>0?Math.log10(2*Math.PI/Math.sqrt(d)):NaN); }
    const tv=[...T0,...Td].filter(isFinite), tlo=Math.floor(Math.min(...tv)), thi=Math.ceil(Math.max(...tv));
    const xt=decadeTicks(lB0,lB1,bb.w), yt=decadeTicks(tlo,thi,bb.h);
    axesQ(ctx,bb,lB0,lB1,tlo,thi,{title:'period against field strength',xlab:'|B|, G (log scale)',ylab:'period, s (log)',xticks:xt,yticks:yt,xfmt:t=>sigf(Math.pow(10,t),1),yfmt:t=>sigf(Math.pow(10,t),1)});
    polyline(ctx,bb,Bs,T0,lB0,lB1,tlo,thi,COL.ref,1.4,[6,4]);
    polyline(ctx,bb,Bs,Td,lB0,lB1,tlo,thi,COL.north,1.8);
    marker(ctx,bb,lB0,lB1,tlo,thi,Math.log10(N.Bmag),isFinite(N.wd)?Math.log10(2*Math.PI/N.wd):Math.log10(N.T0),COL.live);
    legendAuto(ctx,bb,[[COL.ref,'2π/ω₀, undamped'],[COL.north,'2π/ω_d with this damping']]);
  }
  drawCaption(ctx,L);
}
