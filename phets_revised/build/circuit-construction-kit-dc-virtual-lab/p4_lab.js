/* ================================================================== *
 *  the lab: layout, the toolbox, the parts drawn lifelike or as        *
 *  schematic symbols, the meters, and the pointer that builds with     *
 *  them.  Every point is computed in screen pixels -- no canvas        *
 *  transforms -- so the display-list capture sees what the browser    *
 *  draws.                                                              *
 * ================================================================== */
const ZOOMS=[0.5,1,1.6];                       /* PhET's ZOOM_SCALES */
const HINT_H=18;                               /* the house #hint owns the last line: keep canvas text above it */
const TOOL_LABEL={wire:['wire'],battery:['battery'],bulb:['light bulb'],resistor:['resistor'],switch:['switch'],
  fuse:['fuse'],xbattery:['extreme','battery'],xbulb:['extreme','bulb'],xresistor:['extreme','resistor'],
  bill:['dollar','bill'],clip:['paper clip'],coin:['coin'],eraser:['eraser'],pencil:['pencil'],tpencil:['thin','pencil'],
  rbulb:['real bulb'],ammeter:['series','ammeter'],voltmeter:['voltmeter'],probe:['non-contact','ammeter']};
function toolItems(st){ return TOOL_ORDER.filter(k=>k!=='rbulb'||st.realBulbs).concat(['voltmeter','probe']); }

function labGeo(W,H,st){
  st=st||ST;
  const items=toolItems(st), n=items.length, top=stageTop(), bot=H-14-HINT_H;
  const narrow=W<700, cw=narrow?54:62, avail=bot-top-24;
  let cols=2, rows=Math.ceil(n/cols), ch=Math.min(58,Math.floor(avail/rows));
  if(ch<36){ cols=3; rows=Math.ceil(n/cols); ch=Math.min(58,Math.floor(avail/rows)); }
  const tb={x:10,y:top,w:cols*cw+12,h:24+rows*ch+6,cols,rows,cw,ch,items:[]};
  items.forEach((k,j)=>{ const c=j%cols, r=Math.floor(j/cols); tb.items.push({key:k,x:tb.x+6+c*cw,y:tb.y+24+r*ch,w:cw,h:ch}); });
  const x0=tb.x+tb.w+14, x1=W-14, y0=top+6, y1=bot-16;
  const right=W>=900?W-RO_W-22:x1;
  /* the presets fill about half the bench; on a large canvas the bench scales
     up to 1.4x, as PhET scales its whole screen to the window */
  const s0=Math.min(1.4,(right-x0)/520,(y1-y0)/420);
  const sc=s0*st.zoom, cx=(x0+right)/2, cy=(y0+y1)/2;
  const map={sc,X:x=>cx+x*sc,Y:y=>cy+y*sc,wx:X=>(X-cx)/sc,wy:Y=>(Y-cy)/sc};
  return {tb,map,x0,x1,y0,y1,right,cx,cy,sc,s0,W,H};
}
const inRect=(x,y,r)=>x>=r.x&&x<=r.x+r.w&&y>=r.y&&y<=r.y+r.h;

/* ---------------- tiny geometry ---------------- */
/* the frame of a part: t runs along it from A (its start) to B, s across it,
   positive on the left of the direction of travel (up, for a part lying
   left to right) */
function frameOf(A,B){ const dx=B[0]-A[0], dy=B[1]-A[1], L=Math.hypot(dx,dy)||1, ux=dx/L, uy=dy/L;
  return {A,B,L,ux,uy,nx:uy,ny:-ux,P:(t,s)=>[A[0]+ux*t+uy*s,A[1]+uy*t-ux*s]}; }
function pathPts(ctx,pts,close){ ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); if(close) ctx.closePath(); }
function fillPts(ctx,pts,fill,stroke,lw){ pathPts(ctx,pts,true); if(fill){ ctx.fillStyle=fill; ctx.fill(); } if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1; ctx.stroke(); } }
function strokePts(ctx,pts,col,lw,dash){ pathPts(ctx,pts,false); ctx.strokeStyle=col; ctx.lineWidth=lw||1; if(dash) ctx.setLineDash(dash); ctx.stroke(); if(dash) ctx.setLineDash([]); }
/* a rectangle in the part's frame, t0..t1 along and s0..s1 across */
function rectF(F,t0,t1,s0,s1){ return [F.P(t0,s0),F.P(t1,s0),F.P(t1,s1),F.P(t0,s1)]; }
/* a circle as an explicit polygon (the recorder has no ellipse and cannot
   carry a scaled arc through restore(); Known-bad, pupil_plane) */
function circlePts(c,r,n){ const out=[]; n=n||Math.max(12,Math.min(48,Math.ceil(r)));
  for(let i=0;i<n;i++){ const a=TAU*i/n; out.push([c[0]+r*Math.cos(a),c[1]+r*Math.sin(a)]); } return out; }
function capsule(F,t0,t1,h){ /* a rod with rounded ends */
  const out=[], n=8;
  for(let i=0;i<=n;i++){ const a=PI/2+PI*i/n; out.push(F.P(t0+h*Math.cos(a)*0.6,h*Math.sin(a))); }
  for(let i=0;i<=n;i++){ const a=-PI/2+PI*i/n; out.push(F.P(t1+h*Math.cos(a)*0.6,h*Math.sin(a))); }
  return out; }
/* a tag drawn on a part, centred, whose box goes into the label registry so
   the value labels drawn later step round it */
function tagText(ctx,x,y,txt,col,font){ textAt(ctx,x,y,txt,col,font);
  const fs=parseFloat(/([\d.]+)px/.exec(font)[1]), w=plain(txt).length*fs*0.52, hh=fs*1.15;
  LABELS.push([x-w/2,y-hh/2,x+w/2,y+hh/2]); }
function textAt(ctx,x,y,txt,col,font,align,base){ ctx.fillStyle=col; ctx.font=font; ctx.textAlign=align||'center'; ctx.textBaseline=base||'middle'; ctx.fillText(plain(txt),x,y); }

/* resistor colour code: two significant figures and a multiplier */
const BAND=['#1b1b1b','#6b3b1a','#c0392b','#e67e22','#f1c40f','#27ae60','#2e86de','#8e44ad','#95a5a6','#ecf0f1'];
function colourBands(R){
  if(!(R>0)) return ['#1b1b1b'];
  let e=Math.floor(Math.log10(R))-1, m=Math.round(R/Math.pow(10,e));
  if(m>=100){ m=Math.round(m/10); e++; }
  const d1=Math.floor(m/10), d2=m%10;
  const mult=e===-1?'#c9a34e':e===-2?'#bdc3c7':BAND[clamp(e,0,9)];
  return [BAND[d1],BAND[d2],mult];
}

/* ---------------- the parts ---------------- */
/* half-width of each part's body in world units (hit tests use it too) */
const HALF={wire:6,battery:18,xbattery:18,resistor:12,xresistor:12,bulb:14,xbulb:14,rbulb:14,switch:10,fuse:12,
            ammeter:22,coin:26,clip:10,pencil:10,tpencil:7,eraser:17,bill:27};
function drawPartLife(ctx,e,A,B,w,o){
  const F=frameOf(A,B), L=F.L, lw=x=>Math.max(1,x*w), t=e.type;
  const lead=(t0,t1,col)=>strokePts(ctx,[F.P(t0,0),F.P(t1,0)],col||'#8f949e',lw(3.2));
  if(t==='wire'){
    ctx.lineCap='round';
    strokePts(ctx,[A,B],'#3b2413',Math.max(2.5,12*w)); strokePts(ctx,[A,B],'#c07a45',Math.max(1.6,8*w));
    strokePts(ctx,[F.P(0,1.8*w),F.P(L,1.8*w)],'#e3a877',Math.max(0.6,1.6*w));
    ctx.lineCap='butt'; return; }
  if(isBattery(t)){
    const body=t==='xbattery'?'#5c2433':'#3a3f4b';
    fillPts(ctx,rectF(F,0,0.76*L,-17*w,17*w),body,'#1d2029',lw(1.2));
    fillPts(ctx,rectF(F,0,0.76*L,5*w,11*w),t==='xbattery'?'#7a3446':'#4a5163');
    fillPts(ctx,rectF(F,0.76*L,0.97*L,-17*w,17*w),'#c9a34e','#6d5520',lw(1.2));
    fillPts(ctx,rectF(F,0.97*L,L,-7*w,7*w),'#d9dce3','#6f7789',lw(1));
    if(w>=0.45&&!o.icon){ const f=Math.round(Math.max(9,15*w))+'px -apple-system, sans-serif';
      const m=F.P(0.13*L,0), p=F.P(0.865*L,0);
      textAt(ctx,m[0],m[1],'−','#e9ecf2',f); textAt(ctx,p[0],p[1],'+','#2b2410',f); }
    return; }
  if(t==='resistor'||t==='xresistor'){
    lead(0,0.12*L); lead(0.88*L,L);
    fillPts(ctx,capsule(F,0.14*L,0.86*L,11*w),t==='xresistor'?'#9fb2c6':'#d9c69c',t==='xresistor'?'#4a5a6c':'#6b5b3a',lw(1.2));
    const bands=colourBands(e.R), at=[0.27,0.38,0.49];
    bands.forEach((c,j)=>fillPts(ctx,rectF(F,at[j]*L,at[j]*L+0.055*L,-10.5*w,10.5*w),c));
    fillPts(ctx,rectF(F,0.72*L,0.72*L+0.055*L,-10.5*w,10.5*w),'#c9a34e');
    return; }
  if(isBulb(t)){
    /* PhET's lit glass: opacity rises linearly to full at brightness 0.5 */
    const b=o.bright||0, g=glowOf(b);
    lead(0,0.33*L); lead(0.67*L,L);
    strokePts(ctx,[F.P(0.33*L,0),F.P(0.36*L,6*w)],'#8f949e',lw(3)); strokePts(ctx,[F.P(0.67*L,0),F.P(0.64*L,6*w)],'#8f949e',lw(3));
    const c=F.P(0.5*L,52*w), R=30*w;
    if(b>1e-6){                               /* the glow and the rays grow with PhET's brightness */
      fillPts(ctx,circlePts(c,R*(1+1.5*b)),'rgba(255,236,160,'+fmt(0.10+0.22*g,3)+')');
      ctx.lineCap='round';
      for(let k=0;k<12;k++){ const a=TAU*k/12+0.13, r0=R*1.12, r1=R*(1.2+1.3*b);
        strokePts(ctx,[[c[0]+r0*Math.cos(a),c[1]+r0*Math.sin(a)],[c[0]+r1*Math.cos(a),c[1]+r1*Math.sin(a)]],'rgba(255,230,140,'+fmt(0.25+0.55*b,3)+')',Math.max(1,2.2*w*(0.5+b))); }
      ctx.lineCap='butt'; }
    const glass=t==='xbulb'?'#241c2e':t==='rbulb'?'#1f2126':'#1b2130';
    fillPts(ctx,circlePts(c,R),mix(glass,'#fff1b3',g),'#aeb6c6',lw(1.5));
    fillPts(ctx,rectF(F,0.36*L,0.64*L,6*w,24*w),'#b8bcc6','#5d626e',lw(1));
    for(let k=1;k<4;k++) strokePts(ctx,[F.P(0.36*L,(6+4.5*k)*w),F.P(0.64*L,(6+4.5*k)*w)],'#7d828e',lw(1));
    const fil=mix(t==='rbulb'?'#8a5a2a':'#6b6f7a',t==='rbulb'?'#ffd27a':'#fff8d0',g);
    const zz=[F.P(0.43*L,24*w),F.P(0.43*L,44*w)];
    for(let k=0;k<=6;k++) zz.push(F.P((0.43+0.14*k/6)*L,(44+(k%2?5:0))*w));
    zz.push(F.P(0.57*L,44*w),F.P(0.57*L,24*w));
    strokePts(ctx,zz,fil,lw(1.8));
    return; }
  if(t==='switch'){
    const s1=L/3, s2=2*L/3;
    lead(0,s1,'#c07a45'); lead(s2,L,'#c07a45');
    fillPts(ctx,rectF(F,0.26*L,0.74*L,-9*w,-4*w),'#5d4b3a','#2e241b',lw(1));
    const p1=F.P(s1,0), p2=F.P(s2,0);
    const end=e.closed?p2:[p1[0]+(s2-s1)*(Math.cos(PI/4)*F.ux+Math.sin(PI/4)*F.nx),p1[1]+(s2-s1)*(Math.cos(PI/4)*F.uy+Math.sin(PI/4)*F.ny)];
    ctx.lineCap='round'; strokePts(ctx,[p1,end],'#d9dce3',Math.max(2,6*w)); ctx.lineCap='butt';
    fillPts(ctx,circlePts(p1,6*w),'#9aa0aa','#3a3f4b',lw(1)); fillPts(ctx,circlePts(p2,6*w),'#9aa0aa','#3a3f4b',lw(1));
    return; }
  if(t==='fuse'){
    lead(0,0.12*L); lead(0.88*L,L);
    fillPts(ctx,rectF(F,0.22*L,0.78*L,-10*w,10*w),'#152030','#6f7789',lw(1));
    fillPts(ctx,rectF(F,0.12*L,0.22*L,-12*w,12*w),'#b8bcc6','#5d626e',lw(1)); fillPts(ctx,rectF(F,0.78*L,0.88*L,-12*w,12*w),'#b8bcc6','#5d626e',lw(1));
    if(e.tripped){ strokePts(ctx,[F.P(0.22*L,0),F.P(0.44*L,1.5*w)],'#d9dce3',lw(1.8)); strokePts(ctx,[F.P(0.56*L,-1.5*w),F.P(0.78*L,0)],'#d9dce3',lw(1.8));
      fillPts(ctx,circlePts(F.P(0.5*L,0),4.5*w),COL.ref); }
    else strokePts(ctx,[F.P(0.22*L,0),F.P(0.78*L,0)],'#d9dce3',lw(1.8));
    return; }
  if(t==='ammeter'){
    lead(0,0.1*L); lead(0.9*L,L);
    fillPts(ctx,rectF(F,0.1*L,0.9*L,-21*w,21*w),'#10131b','#aeb6c6',lw(1.4));
    const c=F.P(0.5*L,0), fs=Math.round(Math.max(9,Math.min(14,13*w)));
    if(!o.icon) textAt(ctx,c[0],c[1],o.reading,COL.ink,'600 '+fs+'px -apple-system, sans-serif');
    return; }
  if(t==='coin'){
    lead(0,0.22*L,'#c9a34e'); lead(0.78*L,L,'#c9a34e');
    const c=F.P(0.5*L,0);
    const ring=circlePts(c,0.22*L);
    fillPts(ctx,circlePts(c,0.3*L),'#c99a4e','#7a5a22',lw(1.4)); strokePts(ctx,ring.concat([ring[0]]),'#a47a33',lw(1));
    return; }
  if(t==='clip'){
    const out=capsule(F,0.06*L,0.94*L,9*w), inn=capsule(F,0.22*L,0.78*L,4.5*w);
    strokePts(ctx,out.concat([out[0]]),'#c0c6d0',lw(2.4)); strokePts(ctx,inn.slice(0,inn.length-3),'#c0c6d0',lw(2.4));
    return; }
  if(t==='pencil'||t==='tpencil'){
    const h=t==='tpencil'?5.5*w:9*w;
    fillPts(ctx,[F.P(0,0),F.P(0.06*L,-0.3*h),F.P(0.06*L,0.3*h)],'#3a3f4b');
    fillPts(ctx,[F.P(0.06*L,-0.3*h),F.P(0.16*L,-h),F.P(0.16*L,h),F.P(0.06*L,0.3*h)],'#e0c9a0');
    fillPts(ctx,rectF(F,0.16*L,0.84*L,-h,h),'#d9b44a','#7a6320',lw(1));
    strokePts(ctx,[F.P(0.16*L,0),F.P(0.84*L,0)],'#b8942e',lw(1));
    fillPts(ctx,rectF(F,0.84*L,0.9*L,-h,h),'#b8bcc6');
    fillPts(ctx,rectF(F,0.9*L,L,-h,h),'#d98a9a');
    return; }
  if(t==='eraser'){
    fillPts(ctx,capsule(F,0.1*L,0.9*L,16*w),'#d9a0a8','#8a5a60',lw(1.2));
    fillPts(ctx,rectF(F,0.36*L,0.64*L,-16*w,16*w),'#5a7fb0');
    return; }
  if(t==='bill'){
    fillPts(ctx,rectF(F,0,L,-26*w,26*w),'#7c9a6c','#3f5537',lw(1.2));
    fillPts(ctx,rectF(F,0.06*L,0.94*L,-20*w,20*w),null,'#56704a',lw(1));
    const c=F.P(0.5*L,0); fillPts(ctx,circlePts(c,13*w),'#9fbb8f','#56704a',lw(1));
    if(w>=0.5&&!o.icon) textAt(ctx,c[0],c[1],'1','#2e4027',Math.round(Math.max(8,13*w))+'px Georgia, serif');
    return; }
}
function drawPartSchem(ctx,e,A,B,w,o){
  const F=frameOf(A,B), L=F.L, col=COL.struct, lw=Math.max(1.5,3*w), t=e.type;
  const line=(t0,t1)=>strokePts(ctx,[F.P(t0,0),F.P(t1,0)],col,lw);
  if(t==='wire'){ strokePts(ctx,[A,B],col,lw); return; }
  if(t==='battery'){ line(0,0.44*L); line(0.56*L,L);
    strokePts(ctx,[F.P(0.44*L,-10*w),F.P(0.44*L,10*w)],col,Math.max(2.5,6*w)); strokePts(ctx,[F.P(0.56*L,-20*w),F.P(0.56*L,20*w)],col,lw);
    if(w>=0.45&&!o.icon){ const p=F.P(0.66*L,16*w); tagText(ctx,p[0],p[1],'+',col,Math.round(Math.max(9,13*w))+'px -apple-system, sans-serif'); }
    return; }
  if(t==='xbattery'){ line(0,0.34*L); line(0.66*L,L); strokePts(ctx,[F.P(0.44*L,0),F.P(0.56*L,0)],col,lw,[3,3]);
    for(const [a,b] of [[0.34,0.42],[0.58,0.66]]){ strokePts(ctx,[F.P(a*L,-8*w),F.P(a*L,8*w)],col,Math.max(2.5,6*w)); strokePts(ctx,[F.P(b*L,-18*w),F.P(b*L,18*w)],col,lw); }
    return; }
  if(isBulb(t)){ const c=F.P(0.5*L,0), R=18*w, b=o.bright||0; line(0,0.5*L-R); line(0.5*L+R,L);
    fillPts(ctx,circlePts(c,R),b>1e-6?'rgba(255,236,160,'+fmt(0.12+0.6*b,3)+')':null,col,lw);
    const d=R*0.7; strokePts(ctx,[[c[0]-d,c[1]-d],[c[0]+d,c[1]+d]],col,lw); strokePts(ctx,[[c[0]-d,c[1]+d],[c[0]+d,c[1]-d]],col,lw);
    if(t!=='bulb'&&w>=0.45&&!o.icon){ const p=F.P(0.5*L,-R-9*w); tagText(ctx,p[0],p[1],t==='rbulb'?'real':'×1000',COL.dim,Math.round(Math.max(8,10*w))+'px -apple-system, sans-serif'); }
    return; }
  if(t==='switch'){ const s1=L/3, s2=2*L/3; line(0,s1); line(s2,L);
    const p1=F.P(s1,0), p2=F.P(s2,0), a=e.closed?0:PI/6;
    const end=[p1[0]+(s2-s1)*(Math.cos(a)*F.ux+Math.sin(a)*F.nx),p1[1]+(s2-s1)*(Math.cos(a)*F.uy+Math.sin(a)*F.ny)];
    strokePts(ctx,[p1,end],col,lw); fillPts(ctx,circlePts(p1,3.5*w+1),col); fillPts(ctx,circlePts(p2,3.5*w+1),col); return; }
  if(t==='fuse'){ line(0,0.25*L); line(0.75*L,L); fillPts(ctx,rectF(F,0.25*L,0.75*L,-8*w,8*w),null,col,lw);
    if(e.tripped){ line(0.25*L,0.42*L); line(0.58*L,0.75*L); fillPts(ctx,circlePts(F.P(0.5*L,0),3.5*w+1),COL.ref); } else line(0.25*L,0.75*L); return; }
  if(t==='ammeter'){ const c=F.P(0.5*L,0), R=20*w; line(0,0.5*L-R); line(0.5*L+R,L); fillPts(ctx,circlePts(c,R),null,col,lw);
    if(!o.icon) textAt(ctx,c[0],c[1],'A',col,'italic '+Math.round(Math.max(9,15*w))+'px Georgia, serif');
    if(!o.icon){ const p=F.P(0.5*L,-R-12*w); tagText(ctx,p[0],p[1],o.reading,COL.ink,'600 '+Math.round(Math.max(9,12*w))+'px -apple-system, sans-serif'); } return; }
  if(t==='coin'||t==='clip'){ line(0,L); fillPts(ctx,circlePts(F.P(0.5*L,0),4*w+1.5),col); return; }
  /* resistors and the household resistances: the IEEE zigzag */
  line(0,0.2*L); line(0.8*L,L);
  const z=[F.P(0.2*L,0)]; for(let k=1;k<12;k+=2) z.push(F.P((0.2+0.6*k/12)*L,(k%4===1?9:-9)*w)); z.push(F.P(0.8*L,0));
  strokePts(ctx,z,col,lw);
  if(t==='xresistor'&&w>=0.45&&!o.icon){ const p=F.P(0.5*L,-17*w); tagText(ctx,p[0],p[1],'×1000',COL.dim,Math.round(Math.max(8,10*w))+'px -apple-system, sans-serif'); }
}
function drawPart(ctx,e,A,B,w,look,o){ if(look==='schematic') drawPartSchem(ctx,e,A,B,w,o); else drawPartLife(ctx,e,A,B,w,o); }
/* the bulb's glass pokes out on its + s side: the hit region includes it */
function glassCentre(e,A,B,w,look){ if(!isBulb(e.type)||look==='schematic') return null; const F=frameOf(A,B); return {c:F.P(0.5*F.L,52*w),r:30*w}; }

/* ---------------- fire ---------------- */
function drawFire(ctx,c,w){
  const h=Math.max(16,46*w), b=Math.max(8,20*w), pts=[], pts2=[];
  for(let k=0;k<=16;k++){ const u=k/16, x=c[0]+(u-0.5)*2*b, wig=Math.sin(u*PI*3)*0.18*h;
    pts.push([x,c[1]-h*Math.sin(u*PI)*(0.7+0.3*Math.cos(u*TAU*2))-Math.abs(wig)]); }
  pts.push([c[0]+b,c[1]]); pts.push([c[0]-b,c[1]]);
  for(let k=0;k<=12;k++){ const u=k/12; pts2.push([c[0]+(u-0.5)*b,c[1]-0.55*h*Math.sin(u*PI)]); }
  fillPts(ctx,pts,'rgba(232,132,58,0.92)'); fillPts(ctx,pts2,'rgba(242,193,78,0.95)');
}

/* ---------------- the meters ---------------- */
function vmGeo(G,st){ const m=G.map, w=G.sc, v=st.vm;
  const bw=Math.max(92,118*w), bh=Math.max(52,62*w), bx=m.X(v.bx), by=m.Y(v.by);
  const probe=(x,y)=>{ const T=[m.X(x),m.Y(y)], hh=Math.max(34,46*w); return {T,H:[T[0],T[1]-hh],box:{x:T[0]-Math.max(8,9*w),y:T[1]-hh,w:2*Math.max(8,9*w),h:hh}}; };
  return {body:{x:bx-bw/2,y:by-bh/2,w:bw,h:bh},c:[bx,by],red:probe(v.rx,v.ry),black:probe(v.kx,v.ky)}; }
function amGeo(G,st){ const m=G.map, w=G.sc, a=st.am;
  const bw=Math.max(92,112*w), bh=Math.max(48,56*w), bx=m.X(a.bx), by=m.Y(a.by), r=RING_HALF*w, P=[m.X(a.px),m.Y(a.py)];
  const hh=Math.max(26,40*w);
  return {body:{x:bx-bw/2,y:by-bh/2,w:bw,h:bh},c:[bx,by],ring:{c:P,r:Math.max(6,r)},handle:[P[0],P[1]-Math.max(6,r)-hh],
          box:{x:P[0]-Math.max(10,r+4),y:P[1]-Math.max(6,r)-hh,w:2*Math.max(10,r+4),h:hh+2*Math.max(6,r)}}; }
function cable(ctx,p,q,col){ const pts=[]; for(let k=0;k<=14;k++){ const u=k/14, sag=Math.sin(u*PI)*Math.min(60,0.25*Math.hypot(q[0]-p[0],q[1]-p[1]));
  pts.push([lerp(p[0],q[0],u),lerp(p[1],q[1],u)+sag]); } strokePts(ctx,pts,col,1.6); }
function drawVoltmeter(ctx,G,st,M){
  const g=vmGeo(G,st), b=g.body;
  cable(ctx,[b.x+b.w*0.3,b.y+b.h],g.red.H,'#9b3a37'); cable(ctx,[b.x+b.w*0.7,b.y+b.h],g.black.H,'#4a4f5c');
  fillPts(ctx,[[b.x,b.y],[b.x+b.w,b.y],[b.x+b.w,b.y+b.h],[b.x,b.y+b.h]],'#10131b','#aeb6c6',1.4);
  textAt(ctx,b.x+b.w/2,b.y+11,'voltmeter',COL.dim,'italic 10.5px Georgia, serif');
  textAt(ctx,b.x+b.w/2,b.y+b.h*0.62,voltageText(M.vm&&M.vm.V),M.vm&&M.vm.V!==null?COL.pos:COL.dim,'600 '+Math.round(Math.max(12,Math.min(17,15*G.sc)))+'px -apple-system, sans-serif');
  for(const [p,fill] of [[g.red,COL.probeRed],[g.black,'#2c313d']]){
    const T=p.T, hw=p.box.w/2;
    fillPts(ctx,[T,[T[0]-hw*0.55,T[1]-hw*1.3],[T[0]-hw,T[1]-hw*1.6],[T[0]-hw,p.H[1]],[T[0]+hw,p.H[1]],[T[0]+hw,T[1]-hw*1.6],[T[0]+hw*0.55,T[1]-hw*1.3]],fill,'#e9ecf2',1.1);
    fillPts(ctx,circlePts(T,2.4),COL.live); }
}
function drawAmmeterProbe(ctx,G,st,M){
  const g=amGeo(G,st), b=g.body, R=g.ring;
  cable(ctx,[b.x+b.w*0.5,b.y+b.h],g.handle,'#4a4f5c');
  fillPts(ctx,[[b.x,b.y],[b.x+b.w,b.y],[b.x+b.w,b.y+b.h],[b.x,b.y+b.h]],'#10131b','#aeb6c6',1.4);
  textAt(ctx,b.x+b.w/2,b.y+11,'ammeter',COL.dim,'italic 10.5px Georgia, serif');
  textAt(ctx,b.x+b.w/2,b.y+b.h*0.62,currentText(M.am?Math.abs(M.am.I):null,false),M.am?COL.pos:COL.dim,'600 '+Math.round(Math.max(12,Math.min(17,15*G.sc)))+'px -apple-system, sans-serif');
  strokePts(ctx,[[R.c[0],R.c[1]-R.r],g.handle],'#8f949e',Math.max(3,5*G.sc));
  const ring=circlePts(R.c,R.r); strokePts(ctx,ring.concat([ring[0]]),COL.live,Math.max(2,3.5*G.sc));
}

/* ---------------- the toolbox ---------------- */
function drawToolbox(ctx,G,st){
  const tb=G.tb, C=st.circ;
  fillPts(ctx,[[tb.x,tb.y],[tb.x+tb.w,tb.y],[tb.x+tb.w,tb.y+tb.h],[tb.x,tb.y+tb.h]],'rgba(16,19,27,0.94)','#2a2f3d',1);
  textAt(ctx,tb.x+10,tb.y+12,'toolbox',COL.dim,'italic 12px Georgia, serif','left');
  for(const it of tb.items){
    const k=it.key, meter=k==='voltmeter'||k==='probe';
    const left=meter?((k==='voltmeter'?st.vm.on:st.am.on)?0:1):remaining(C,k);
    const labels=st.showLabels&&it.h>=40, iconY=it.y+(labels?(TOOL_LABEL[k].length>1?it.h*0.3:it.h*0.38):it.h*0.5);
    if(left<=0) fillPts(ctx,[[it.x+1,it.y+1],[it.x+it.w-1,it.y+1],[it.x+it.w-1,it.y+it.h-1],[it.x+1,it.y+it.h-1]],'rgba(7,11,24,0.55)');
    if(meter) drawMeterIcon(ctx,k,[it.x+it.w/2,iconY],it.w,left>0);
    else { const L=TYPES[k].L||100, look=st.look, glassy=isBulb(k)&&look!=='schematic';
      /* a bulb stands 85 units tall with its glass: shrink it to its cell */
      const w=glassy?Math.min((it.w-16)/L,(labels?(TOOL_LABEL[k].length>1?it.h-24:it.h-14):it.h-6)/88):(it.w-16)/L, span=w*L;
      const A=[it.x+(it.w-span)/2,iconY], B=[it.x+(it.w+span)/2,iconY];
      const yo=glassy?-(labels?20:32)*w:0;          /* keep the glass inside the cell */
      drawPart(ctx,{type:k,R:TYPES[k].R,E:TYPES[k].E,rating:TYPES[k].rating,closed:false,tripped:false,a:0,b:1,id:-1},[A[0],A[1]-yo],[B[0],B[1]-yo],w,look,{bright:0,reading:'—',icon:true}); }
    if(labels){ const ls=TOOL_LABEL[k]; ls.forEach((s,j)=>textAt(ctx,it.x+it.w/2,it.y+it.h-6-(ls.length-1-j)*10.5,s,left>0?'#9aa2b4':'#5a6172','9.5px -apple-system, sans-serif','center','bottom')); }
    if(!meter&&TYPES[k].max>1&&it.h>=34) textAt(ctx,it.x+it.w-3,it.y+8,'×'+left,left>0?'#6f7789':'#4a5162','8.5px -apple-system, sans-serif','right');
  }
}
function drawMeterIcon(ctx,k,c,w,on){
  const col=on?'#aeb6c6':'#4a5162';
  fillPts(ctx,[[c[0]-w*0.3,c[1]-9],[c[0]+w*0.3,c[1]-9],[c[0]+w*0.3,c[1]+5],[c[0]-w*0.3,c[1]+5]],'#10131b',col,1);
  if(k==='voltmeter'){ fillPts(ctx,circlePts([c[0]-w*0.18,c[1]+11],2.5),COL.probeRed); fillPts(ctx,circlePts([c[0]+w*0.18,c[1]+11],2.5),'#e9ecf2'); }
  else { const r=circlePts([c[0]+w*0.2,c[1]+11],4); strokePts(ctx,r.concat([r[0]]),COL.live,1.4); }
}

/* ---------------- the whole lab ---------------- */
function drawLab(ctx,W,H,M){
  const st=M.st, C=st.circ, SOL=M.sol, G=labGeo(W,H,st), m=G.map, w=G.sc, look=st.look;
  const P=v=>[m.X(v.x),m.Y(v.y)];
  const vmap=new Map(); for(const v of C.verts) vmap.set(v.id,P(v));
  /* the selection glows under its part */
  const selOutline=()=>{ if(!(M.sel&&vmap.has(M.sel.a))) return;
    const A=vmap.get(M.sel.a), B=vmap.get(M.sel.b), F=frameOf(A,B), hw=(HALF[M.sel.type]||12)*w+Math.max(4,6*w), pad=Math.max(4,6*w);
    const cap=capsule(F,-pad,F.L+pad,hw); strokePts(ctx,cap.concat([cap[0]]),COL.live,2);
    const gl=glassCentre(M.sel,A,B,w,look); if(gl){ const ring=circlePts(gl.c,gl.r+Math.max(4,6*w)); strokePts(ctx,ring.concat([ring[0]]),COL.live,2); } };
  /* wires under the parts, as PhET layers them */
  for(const pass of [0,1]) for(const e of C.els){
    if((pass===0)!==(e.type==='wire')) continue;
    drawPart(ctx,e,vmap.get(e.a),vmap.get(e.b),w,look,{bright:SOL.bright.get(e.id)||0,reading:e.type==='ammeter'?currentText((r=>r===null?null:Math.abs(r))(seriesReading(C,SOL,e)),true):''});
  }
  /* the joints: solder where parts meet, an open ring at a loose end */
  for(const v of C.verts){ const p=vmap.get(v.id), n=elsAt(C,v.id).length, r=Math.max(3,7*w);
    if(n>=2) fillPts(ctx,circlePts(p,r),'#9aa0aa','#3a3f4b',1);
    else { const ring=circlePts(p,r+1); strokePts(ctx,ring.concat([ring[0]]),'#8b93a6',1.4); } }
  /* the current: electrons or conventional charges riding each part */
  if(st.showCurrent){
    const rad=Math.max(2.2,4.6*w);
    for(const e of C.els){ const I=SOL.I.get(e.id); if(!(Math.abs(I)>1e-10)||e.type==='ammeter') continue;   /* a meter's box hides them */
      const A=vmap.get(e.a), B=vmap.get(e.b), F=frameOf(A,B), Lw=elLength(C,e);
      for(const s of chargePositions(Lw,st.phase[e.id]||0,st.carrier)){ const q=F.P(s*w,0);
        if(st.carrier==='electrons') fillPts(ctx,circlePts(q,rad,10),COL.pos,'#1f2a10',1);
        else { const d=I>0?1:-1, a=[q[0]+d*F.ux*rad*1.6,q[1]+d*F.uy*rad*1.6], bl=[q[0]-d*F.ux*rad+F.nx*rad,q[1]-d*F.uy*rad+F.ny*rad], br=[q[0]-d*F.ux*rad-F.nx*rad,q[1]-d*F.uy*rad-F.ny*rad];
          fillPts(ctx,[a,bl,br],COL.pos,'#1f2a10',1); } } }
  }
  selOutline();
  /* fire, over everything it belongs to */
  for(const eid of SOL.fire){ const e=elById(C,eid); if(!e) continue; const A=vmap.get(e.a), B=vmap.get(e.b);
    drawFire(ctx,[(A[0]+B[0])/2,(A[1]+B[1])/2-Math.max(6,12*w)],w); }
  /* values, beside each part, on the side away from a bulb's glass */
  if(st.showValues) for(const e of C.els){ const txt=valueText(e,SOL); if(!txt) continue;
    const A=vmap.get(e.a), B=vmap.get(e.b), F=frameOf(A,B), off=((HALF[e.type]||10)+12)*w+7;
    /* above a part that lies across the screen, right of one that stands up,
       and always away from a bulb's glass */
    const qa=F.P(F.L/2,off), qb=F.P(F.L/2,-off), vert=Math.abs(F.nx)>Math.abs(F.ny);
    let q=vert?(qa[0]>qb[0]?qa:qb):(qa[1]<qb[1]?qa:qb);
    if(isBulb(e.type)&&look!=='schematic') q=qb;
    lab(ctx,W,H,q[0],q[1],txt,'#cfd4de','11px -apple-system, sans-serif',vert?(q[0]>(A[0]+B[0])/2?'left':'right'):'center','middle'); }
  /* the selected joint: a ring, and PhET's scissors as a "split" button */
  if(st.selV!==null&&vmap.has(st.selV)){ const p=vmap.get(st.selV), ring=circlePts(p,Math.max(9,13*w)); strokePts(ctx,ring.concat([ring[0]]),COL.live,2);
    const sb=splitButton(G,st); if(sb){ fillPts(ctx,[[sb.x,sb.y],[sb.x+sb.w,sb.y],[sb.x+sb.w,sb.y+sb.h],[sb.x,sb.y+sb.h]],'#2a1830',COL.live,1.2);
      textAt(ctx,sb.x+sb.w/2,sb.y+sb.h/2,'split',COL.ink,'italic 11.5px Georgia, serif'); } }
  /* the drop target while dragging: the 30-unit radius, around the joint it would join */
  if(DRAG.what==='el'||DRAG.what==='vert'){ const t=dropTarget(C,DRAG.what==='vert'?[DRAG.vid]:[...DRAG.group]);
    if(t){ const p=vmap.get(t.dst), q=vmap.get(t.src), ring=circlePts(p,SNAP_R*w,36);
      strokePts(ctx,ring.concat([ring[0]]),COL.live,1.6,[5,4]); strokePts(ctx,[q,p],COL.live,1.2,[2,3]); } }
  if(st.vm.on) drawVoltmeter(ctx,G,st,M);
  if(st.am.on) drawAmmeterProbe(ctx,G,st,M);
  drawToolbox(ctx,G,st);
  /* an empty bench says what to do */
  if(!C.els.length) caption(ctx,G.x0+10,G.cy-20,'The bench is empty. Drag a battery, a light bulb and two wires out of the toolbox, and drop the end of one on the end of another to join them; a loop through the battery lights the bulb.',Math.min(460,G.right-G.x0-20),'#8b93a6','12px -apple-system, sans-serif');
  /* the scale, bottom right and above the #hint line */
  /* the scale and the speed limit, bottom right above the #hint line; each
     falls back to a short form rather than run into the toolbox */
  const room=G.x1-(G.tb.x+G.tb.w+12), fits=t=>plain(t).length*10.5*0.52<=room;
  const pick=(a,b)=>fits(a)?a:(fits(b)?b:'');
  const note=pick('zoom '+fmt(st.zoom,1)+'× · 100 units of wire = '+fmt(100*LEN_PER_UNIT*100,0)+' cm (PhET’s scale) · '+(look==='schematic'?'schematic (IEEE)':'lifelike'),
                  'zoom '+fmt(st.zoom,1)+'× · 100 units = 5 cm of wire');
  if(note) textAt(ctx,G.x1,H-14-HINT_H,note,'#6f7789','10.5px -apple-system, sans-serif','right','bottom');
  if(st.showCurrent&&M.scale<1){ const pc=100*M.scale, sp=pick(speedNote(M.scale),'charges slowed to '+(pc>=1?fmt(pc,0):sigf(pc,2))+'% (PhET’s speed limit)');
    if(sp) textAt(ctx,G.x1,H-14-HINT_H-15,sp,COL.ref,'10.5px -apple-system, sans-serif','right','bottom'); }
}
/* PhET's words, with a percentage that says something below 1 % */
function speedNote(scale){ const p=100*scale; return 'Animation speed limit reached! Current animation speed reduced to '+(p>=1?fmt(p,0):sigf(p,2))+'% normal.'; }
function splitButton(G,st){
  if(st.selV===null) return null;
  const v=vById(st.circ,st.selV); if(!v||elsAt(st.circ,v.id).length<2) return null;
  const x=G.map.X(v.x), y=G.map.Y(v.y);
  return {x:x-21,y:y-Math.max(22,20*G.sc)-22,w:42,h:20};
}

/* ---------------- hit tests (screen pixels) ---------------- */
function hitToolbox(G,x,y){ for(const it of G.tb.items) if(inRect(x,y,it)) return it; return null; }
function overToolbox(G,x,y){ return inRect(x,y,G.tb); }
function hitVertex(G,st,x,y){ let best=null; const r=Math.max(10,12*G.sc);
  for(const v of st.circ.verts){ const d=Math.hypot(G.map.X(v.x)-x,G.map.Y(v.y)-y); if(d<=r&&(!best||d<best.d)) best={d,id:v.id}; }
  return best?best.id:null; }
function hitElement(G,st,x,y){
  const C=st.circ, m=G.map, w=G.sc; let best=null;
  /* fixed parts sit on top of wires, so they win a tie */
  for(const e of C.els){ const A=vById(C,e.a), B=vById(C,e.b), Ap=[m.X(A.x),m.Y(A.y)], Bp=[m.X(B.x),m.Y(B.y)];
    const s=segDist(x,y,Ap[0],Ap[1],Bp[0],Bp[1]), hw=Math.max(6,(HALF[e.type]||10)*w);
    let d=s.d<=hw?s.d:Infinity;
    const gl=glassCentre(e,Ap,Bp,w,st.look); if(gl){ const dg=Math.hypot(x-gl.c[0],y-gl.c[1]); if(dg<=gl.r) d=Math.min(d,0.5); }
    if(d<Infinity){ const score=d+(e.type==='wire'?1000:0); if(!best||score<best.score) best={score,id:e.id}; } }
  return best?best.id:null;
}
function hitMeter(G,st,x,y){
  if(st.vm.on){ const g=vmGeo(G,st);
    if(inRect(x,y,g.red.box)||Math.hypot(x-g.red.T[0],y-g.red.T[1])<=8) return 'vm-red';
    if(inRect(x,y,g.black.box)||Math.hypot(x-g.black.T[0],y-g.black.T[1])<=8) return 'vm-black';
    if(inRect(x,y,g.body)) return 'vm-body'; }
  if(st.am.on){ const g=amGeo(G,st);
    if(inRect(x,y,g.box)) return 'am-probe';
    if(inRect(x,y,g.body)) return 'am-body'; }
  return null;
}

/* ---------------- dragging a joint ---------------- */
/* a joint of wires alone follows the pointer; one rigid part swings about
   its other end (its length is fixed); two or more rigid parts meeting here
   move together as one body */
function dragVertex(C,vid,x,y){
  const v=vById(C,vid); if(!v) return;
  const fixed=elsAt(C,vid).filter(e=>e.type!=='wire');
  if(!fixed.length){ v.x=x; v.y=y; return; }
  if(fixed.length===1){ const e=fixed[0], o=vById(C,otherEnd(e,vid)), L=TYPES[e.type].L, d=Math.hypot(x-o.x,y-o.y);
    if(d<1e-9) return; v.x=o.x+(x-o.x)*L/d; v.y=o.y+(y-o.y)*L/d; return; }
  translateVerts(C,fixedGroup(C,vid),x-v.x,y-v.y);
}
function moveSetOf(C,e){ const s=fixedGroup(C,e.a); if(e.type==='wire') for(const x of fixedGroup(C,e.b)) s.add(x); return s; }

/* the lab's pointer: returns true when something changed.  Pointer-down on
   the toolbox makes the part and starts dragging it; a release over the
   toolbox puts it back; a release anywhere else, after ANY movement, joins
   the nearest legal pair of ends within the drop radius (PhET's
   endDrag(vertex, dragged)); and a release within PhET's 15-px tap
   threshold of the press ALSO selects (and toggles a switch) -- PhET does
   both, so a short nudge onto a neighbouring end joins it. */
function labPointer(S,kind,x,y){
  const st=S.st, C=st.circ, G=labGeo(S.W,S.H,st), m=G.map;
  if(kind==='down'){
    DRAG.what=null; DRAG.sx=x; DRAG.sy=y; DRAG.moved=false; DRAG.dragged=false; DRAG.fromBox=false;
    const sb=splitButton(G,st);
    if(sb&&inRect(x,y,sb)){ splitVertex(C,st.selV); st.selV=null; circuitEdited(st); return true; }
    const mh=hitMeter(G,st,x,y);
    if(mh){ DRAG.what=mh; DRAG.last=[m.wx(x),m.wy(y)]; return true; }
    const it=hitToolbox(G,x,y);
    if(it){ const wx=m.wx(x), wy=m.wy(y);
      if(it.key==='voltmeter'){ if(st.vm.on) return false; st.vm={on:true,bx:wx,by:wy,rx:wx-35,ry:wy+85,kx:wx+35,ky:wy+85}; DRAG.what='vm-body'; DRAG.fromBox=true; DRAG.last=[wx,wy]; return true; }
      if(it.key==='probe'){ if(st.am.on) return false; st.am={on:true,bx:wx,by:wy,px:wx,py:wy+95}; DRAG.what='am-body'; DRAG.fromBox=true; DRAG.last=[wx,wy]; return true; }
      const el=addElement(C,it.key,wx,wy); if(!el) return false;
      DRAG.what='el'; DRAG.eid=el.id; DRAG.group=moveSetOf(C,el); DRAG.last=[wx,wy]; DRAG.fromBox=true;
      st.sel=el.id; st.selV=null; circuitEdited(st); return true; }
    const vid=hitVertex(G,st,x,y);
    if(vid!==null){ DRAG.what='vert'; DRAG.vid=vid; DRAG.last=[m.wx(x),m.wy(y)]; return true; }
    const eid=hitElement(G,st,x,y);
    if(eid!==null){ const e=elById(C,eid); DRAG.what='el'; DRAG.eid=eid; DRAG.group=moveSetOf(C,e); DRAG.last=[m.wx(x),m.wy(y)]; return true; }
    DRAG.what='none'; return false;
  }
  if(kind==='move'){
    if(!DRAG.what||DRAG.what==='none') return false;
    if(Math.hypot(x-DRAG.sx,y-DRAG.sy)>=TAP_PX) DRAG.moved=true;
    if(x!==DRAG.sx||y!==DRAG.sy) DRAG.dragged=true;
    const wx=m.wx(x), wy=m.wy(y), dx=wx-DRAG.last[0], dy=wy-DRAG.last[1];
    const d=DRAG.what;
    if(d==='el'){ translateVerts(C,DRAG.group,dx,dy); circuitEdited(st); }
    else if(d==='vert'){ dragVertex(C,DRAG.vid,wx,wy); circuitEdited(st); }
    else if(d==='vm-body'){ st.vm.bx+=dx; st.vm.by+=dy; if(DRAG.fromBox){ st.vm.rx+=dx; st.vm.ry+=dy; st.vm.kx+=dx; st.vm.ky+=dy; } }
    else if(d==='vm-red'){ st.vm.rx+=dx; st.vm.ry+=dy; }
    else if(d==='vm-black'){ st.vm.kx+=dx; st.vm.ky+=dy; }
    else if(d==='am-body'){ st.am.bx+=dx; st.am.by+=dy; if(DRAG.fromBox){ st.am.px+=dx; st.am.py+=dy; } }
    else if(d==='am-probe'){ st.am.px+=dx; st.am.py+=dy; }
    DRAG.last=[wx,wy];
    return true;
  }
  /* up */
  const d=DRAG.what; DRAG.what=null;
  if(!d) return false;
  if(d==='none'){ if(!DRAG.moved&&(st.sel!==null||st.selV!==null)){ st.sel=null; st.selV=null; return true; } return false; }
  if(d==='el'){ const e=elById(C,DRAG.eid); if(!e) return true;
    const A=vById(C,e.a), B=vById(C,e.b), mx=m.X((A.x+B.x)/2), my=m.Y((A.y+B.y)/2);
    if(overToolbox(G,mx,my)){ deleteElement(C,e.id); if(st.sel===e.id) st.sel=null; circuitEdited(st); return true; }
    if(DRAG.dragged){ const t=dropTarget(C,[...DRAG.group]); if(t){ connect(C,t.src,t.dst); circuitEdited(st); } }
    if(!DRAG.moved&&!DRAG.fromBox){ st.sel=e.id; st.selV=null; st.thevEl=null; if(e.type==='switch'){ e.closed=!e.closed; circuitEdited(st); } }
    return true; }
  if(d==='vert'){ let vid=DRAG.vid;
    if(DRAG.dragged){ const t=dropTarget(C,[vid]); if(t){ connect(C,t.src,t.dst); circuitEdited(st); vid=t.dst; } }
    if(!DRAG.moved){ st.selV=vid; st.sel=null; }
    return true; }
  if(d==='vm-body'||d==='am-body'){ const g=d==='vm-body'?vmGeo(G,st):amGeo(G,st), cx=g.c[0], cy=g.c[1];
    if(overToolbox(G,cx,cy)){ if(d==='vm-body') st.vm.on=false; else st.am.on=false; } return true; }
  return true;
}
