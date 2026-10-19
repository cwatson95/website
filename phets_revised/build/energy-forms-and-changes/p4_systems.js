
/* ================================================================== *
 *  drawing: the systems view                                          *
 * ================================================================== */
const SYS_CAP_FULL='PhET’s layout, in metres; the drawings are the remake’s. Energy chunks are the ledger quantised: each channel emits one chunk for every 5019 J that flows along it '
  +'(PhET’s ENERGY_PER_CHUNK), and each moves at PhET’s 4 cm/s, so a chunk you see left its element some seconds ago. Colours give the form.';
const SYS_CAP_SHORT='One chunk per 5019 J on each channel, moving at PhET’s 4 cm/s; colours give the form.';
const SYS_EXT={xmin:-0.275,xmax:0.175,ymin:-0.07,ymax:0.215};
function sysGeo(ctx,W,H){
  const narrow=isNarrow(W), left=16, right=narrow?W-14:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left-20));
  const fit=fitCaption(ctx,W,H-HINT_H,SYS_CAP_FULL,SYS_CAP_SHORT,capW,stageTop()+30+240);
  const legH=24, top=stageTop()+14, bottom=fit.capY-legH-12;
  const bx=box(left,top,right-left,Math.max(120,bottom-top));
  const map=worldFitUp(bx,SYS_EXT,0.004);
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW:fit.capW,bx,map,legY:fit.capY-legH+2};
}
function wline(ctx,map,pts,col,lw){ ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(map.X(p[0]),map.Y(p[1])); else ctx.lineTo(map.X(p[0]),map.Y(p[1])); }); ctx.strokeStyle=col; ctx.lineWidth=lw||1.2; ctx.stroke(); }
function ellipsePts(cx,cy,rx,ry,n){ const o=[]; for(let k=0;k<n;k++){ const a=TAU*k/n; o.push([cx+rx*Math.cos(a),cy+ry*Math.sin(a)]); } return o; }
function wheel(ctx,map,c,r,ang,spokes,col){
  worldPoly(ctx,map,ellipsePts(c.x,c.y,r,r,28),null,col,1.6);
  for(let k=0;k<spokes;k++){ const a=ang+TAU*k/spokes; wline(ctx,map,[[c.x,c.y],[c.x+r*Math.cos(a),c.y+r*Math.sin(a)]],rgba(col,0.7),1); }
}
/* the two outer tangents of two circles (the belt) */
function beltLines(c1,r1,c2,r2){
  const dx=c2.x-c1.x, dy=c2.y-c1.y, d=Math.hypot(dx,dy), a=Math.atan2(dy,dx), b=Math.acos((r1-r2)/d);
  const out=[];
  for(const s of [1,-1]){ const t=a+s*b; out.push([[c1.x+r1*Math.cos(t),c1.y+r1*Math.sin(t)],[c2.x+r2*Math.cos(t),c2.y+r2*Math.sin(t)]]); }
  return out;
}
/* a two-link leg: the knee bends forward (-x), toward the front wheel */
function kneeOf(hip,foot,L1,L2){
  const dx=foot[0]-hip[0], dy=foot[1]-hip[1], d=Math.min(Math.hypot(dx,dy),L1+L2-1e-6);
  const a=(L1*L1-L2*L2+d*d)/(2*d), h=Math.sqrt(Math.max(L1*L1-a*a,0)), ux=dx/(Math.hypot(dx,dy)||1), uy=dy/(Math.hypot(dx,dy)||1);
  const mx=hip[0]+a*ux, my=hip[1]+a*uy, k1=[mx-h*uy,my+h*ux], k2=[mx+h*uy,my-h*ux];
  return k1[0]<k2[0]?k1:k2;
}
function drawBiker(ctx,W,H,map,S,st){
  const crank=[SX+0.0058,-0.006], fw={x:SX-0.045,y:-0.01};  /* PhET's gear and rear-wheel offsets */
  wheel(ctx,map,RW,RW_R,S.rear,6,'#aeb6c6'); wheel(ctx,map,fw,RW_R,S.rear,6,'#aeb6c6');
  const seat=[SX+0.002,0.022], head=[SX-0.033,0.024];
  wline(ctx,map,[[RW.x,RW.y],crank,seat,[RW.x,RW.y]],'#5ac8e0',2);
  wline(ctx,map,[crank,head,[fw.x,fw.y]],'#5ac8e0',2);
  wline(ctx,map,[seat,head],'#5ac8e0',2);
  const hip=[SX+0.002,0.026], sh=[SX-0.018,0.06], hand=[SX-0.036,0.03];
  const a=S.crank, p1=[crank[0]+0.012*Math.cos(a),crank[1]+0.012*Math.sin(a)], p2=[crank[0]-0.012*Math.cos(a),crank[1]-0.012*Math.sin(a)];
  wline(ctx,map,[p1,p2],'#8b93a6',2);
  const k2=kneeOf(hip,p2,0.03,0.03); wline(ctx,map,[hip,k2,p2],'#6a7386',3);
  worldPoly(ctx,map,[[hip[0]+0.006,hip[1]-0.004],[sh[0]+0.007,sh[1]+0.004],[sh[0]-0.006,sh[1]+0.002],[hip[0]-0.007,hip[1]-0.002]],'#39414f','#cfd4de',1.2);
  wline(ctx,map,[sh,hand],'#cfd4de',2.5);
  const k1=kneeOf(hip,p1,0.03,0.03); wline(ctx,map,[hip,k1,p1],'#cfd4de',3);
  worldPoly(ctx,map,ellipsePts(SX-0.024,0.071,0.008,0.008,18),'#cfd4de',null);
  /* the food: 21 chemical chunks in the torso, one fewer for every 5019 J burned */
  if(st.symSys){ const n=foodChunks(S), sz=clamp(0.0068*map.s,5,9);
    for(let k=0;k<n;k++){ const r=Math.floor(k/3), c=k%3, u=(r+0.5)/7, x=hip[0]+(sh[0]-hip[0])*u+(c-1)*0.0045, y=hip[1]+(sh[1]-hip[1])*u;
      drawChunk(ctx,map.X(x),map.Y(y),sz,'chemical',1); } }
  if(S.food<=0) lab(ctx,W,H,map.X(SX),map.Y(0.105),'out of food: feed me',COL.ref,LAB_FONT,'center','middle');
}
function drawFaucet(ctx,map,S,st){
  worldPoly(ctx,map,[[SYS_EXT.xmin,0.113],[SX+0.076,0.113],[SX+0.076,0.127],[SYS_EXT.xmin,0.127]],'#39414f','#8b93a6',1);
  worldPoly(ctx,map,[[SX+0.062,0.105],[SX+0.076,0.105],[SX+0.076,0.114],[SX+0.062,0.114]],'#39414f','#8b93a6',1);
  const hx=SX+0.03, ang=Math.PI/2-st.flow*Math.PI/3;
  wline(ctx,map,[[hx,0.127],[hx,0.137]],'#8b93a6',2);
  wline(ctx,map,[[hx-0.014*Math.sin(ang),0.137+0.0*Math.cos(ang)],[hx+0.014*Math.sin(ang),0.137]],'#cfd4de',3);
  if(st.flow>0){
    const w=0.014*st.flow/2, bot=S.conv==='generator'?GW.y+0.03:FLOOR;
    worldPoly(ctx,map,[[SPOUT.x-w,SPOUT.y],[SPOUT.x+w,SPOUT.y],[SPOUT.x+w*0.8,bot],[SPOUT.x-w*0.8,bot]],rgba(COL.body.water,0.55),null);
  }
}
function drawSun(ctx,map,S,st){
  for(let k=0;k<12;k++){ const a=TAU*k/12; wline(ctx,map,[[SUN.x+1.2*SUN_R*Math.cos(a),SUN.y+1.2*SUN_R*Math.sin(a)],[SUN.x+1.55*SUN_R*Math.cos(a),SUN.y+1.55*SUN_R*Math.sin(a)]],rgba('#f4d03f',0.8),1.5); }
  worldPoly(ctx,map,ellipsePts(SUN.x,SUN.y,SUN_R,SUN_R,28),'#f4d03f',null);
  CLOUDS.forEach((c,i)=>{ const a=cloudStrength(st.clouds,i); if(a<=0) return;
    worldPoly(ctx,map,ellipsePts(c[0],c[1],CLOUD_RX,CLOUD_RY,22),rgba('#dfe6f0',0.85*a),rgba('#ffffff',0.6*a),1); });
}
function drawTeapot(ctx,map,S,st){
  worldPoly(ctx,map,[[SX-0.032,FLOOR],[SX+0.032,FLOOR],[SX+0.032,-0.012],[SX-0.032,-0.012]],'#121824',rgba(COL.struct,0.55),1.2);
  if(st.heat>0) for(let q=-1;q<=1;q++){ const cx=SX+q*0.014, hh=0.006+0.012*st.heat*(q===0?1:0.7);
    worldPoly(ctx,map,[[cx-0.006,-0.012],[cx+0.006,-0.012],[cx,-0.012+hh]],rgba('#ff8a2a',0.4+0.55*st.heat),rgba('#ffd27a',0.9),1); }
  const body=[]; for(let k=0;k<=16;k++){ const a=Math.PI+Math.PI*k/16; body.push([KETTLE.x+0.034*Math.cos(a),KETTLE.y+0.028*Math.sin(a)]); }
  body.push([KETTLE.x+0.028,KETTLE.y+0.018],[KETTLE.x+0.012,KETTLE.y+0.028],[KETTLE.x-0.012,KETTLE.y+0.028],[KETTLE.x-0.028,KETTLE.y+0.018]);
  worldPoly(ctx,map,[[SX+0.024,0.008],[SX+0.03,0.016],[KSPOUT.x+0.002,KSPOUT.y+0.003],[KSPOUT.x-0.004,KSPOUT.y],[SX+0.028,0.004]],'#7c8497','#aeb6c6',1);
  worldPoly(ctx,map,body,'#8b93a6','#cfd4de',1.2);
  worldPoly(ctx,map,ellipsePts(KETTLE.x,KETTLE.y+0.032,0.006,0.004,12),'#cfd4de',null);
  wline(ctx,map,[[SX-0.03,0.03],[SX-0.046,0.03],[SX-0.046,0.006],[SX-0.033,0.002]],'#aeb6c6',2);
  const P=S.kettle/TAU_K;
  if(P>1){ const u=clamp(P/(STEAM*MAXP),0.1,1), end=S.conv==='generator'?[GW.x-0.035,GW.y+0.045]:[KSPOUT.x+0.07,KSPOUT.y+0.085];
    for(let q=1;q<=5;q++){ const f=q/5, x=KSPOUT.x+(end[0]-KSPOUT.x)*f, y=KSPOUT.y+(end[1]-KSPOUT.y)*f, r=0.004+0.006*f;
      worldPoly(ctx,map,ellipsePts(x,y,r,r*0.7,10),rgba('#e9edf5',0.25+0.45*u*(1.1-f*0.6)),null); } }
}
function drawGenerator(ctx,map,S){
  worldPoly(ctx,map,[[CX-0.035,FLOOR],[CX+0.035,FLOOR],[CX+0.035,-0.018],[CX-0.035,-0.018]],'#1a2130',rgba(COL.struct,0.55),1.2);
  worldPoly(ctx,map,[[CX-0.016,-0.018],[CX+0.016,-0.018],[CX+0.016,GW.y],[CX-0.016,GW.y]],'#232b3a',rgba(COL.struct,0.4),1);
  worldPoly(ctx,map,ellipsePts(GW.x,GW.y,GW_R,GW_R,32),rgba('#10151f',0.9),'#aeb6c6',1.6);
  for(let k=0;k<8;k++){ const a=S.wAngle+TAU*k/8, c=Math.cos(a), s=Math.sin(a), w=0.0018;
    worldPoly(ctx,map,[[GW.x+0.014*c-w*s,GW.y+0.014*s+w*c],[GW.x+GW_PAD*c-w*s,GW.y+GW_PAD*s+w*c],[GW.x+GW_PAD*c+w*s,GW.y+GW_PAD*s-w*c],[GW.x+0.014*c+w*s,GW.y+0.014*s-w*c]],'#6f7789','#cfd4de',0.8); }
  worldPoly(ctx,map,ellipsePts(GW.x,GW.y,0.012,0.012,16),'#cfd4de',null);
  wline(ctx,map,[[CX+0.016,-0.03],[WIRE0.x,WIRE0.y]],'#cfd4de',1.6);
}
function drawPanel(ctx,map,S){
  worldPoly(ctx,map,[[CX-0.03,FLOOR],[CX+0.03,FLOOR],[CX+0.03,-0.036],[CX-0.03,-0.036]],'#1a2130',rgba(COL.struct,0.5),1);
  wline(ctx,map,[[CX+0.015,-0.036],[CX+0.015,0.03]],'#8b93a6',2.5);
  const a=PANEL[0], b=PANEL[1], th=0.007;
  worldPoly(ctx,map,[[a[0],a[1]],[b[0],b[1]],[b[0]+0.004,b[1]-th],[a[0]+0.004,a[1]-th]],'#0f2242','#aeb6c6',1);
  for(let k=1;k<6;k++){ const f=k/6; wline(ctx,map,[[a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f],[a[0]+(b[0]-a[0])*f+0.004,a[1]+(b[1]-a[1])*f-th]],rgba('#8fb8d4',0.6),1); }
  wline(ctx,map,[[a[0]+0.002,a[1]-th/2],[b[0]+0.002,b[1]-th/2]],rgba('#8fb8d4',0.6),1);
  wline(ctx,map,[[CX+0.015,-0.025],[CX+0.03,-0.0385],[WIRE0.x,WIRE0.y]],'#cfd4de',1.6);
}
function drawStand(ctx,map,topY){
  worldPoly(ctx,map,[[UX-0.03,FLOOR],[UX+0.03,FLOOR],[UX+0.03,-0.036],[UX-0.03,-0.036]],'#1a2130',rgba(COL.struct,0.5),1);
  wline(ctx,map,[[UX,-0.036],[UX,topY]],'#8b93a6',2.5);
}
function drawHeater(ctx,W,H,map,S,st){
  worldPoly(ctx,map,[[UX-0.042,FLOOR],[UX+0.042,FLOOR],[UX+0.042,0.012],[UX-0.042,0.012]],'#1a2130',rgba(COL.struct,0.55),1.2);
  const coil=[]; for(let k=0;k<=12;k++) coil.push([UX-0.03+0.06*k/12,0.006+((k%2)?0.003:-0.003)]);
  wline(ctx,map,coil,mix('#6f7789','#ff7a2a',clamp(S.hp,0,1)),2.2);
  const x0=UX-HB_W/2, x1=UX+HB_W/2, y0=0.016, y1=y0+HB_H, yf=y0+HB_H*FLUID0, T=Math.min(S.water/HB_C,T_BOIL.water);
  worldPoly(ctx,map,[[x0,y0],[x1,y0],[x1,yf],[x0,yf]],mix('#0a0c12',COL.body.water,0.55),null);
  wline(ctx,map,[[x0,y1],[x0,y0],[x1,y0],[x1,y1]],rgba('#e9edf5',0.8),1.5);
  if(st.symSys){ const n=nChunks(S.water), sz=clamp(0.0075*map.s,6,11);
    for(let k=0;k<n;k++){ const cols=8, fx=((k%cols)+0.5+(((k*0.618)%1)-0.5)*0.3)/cols, fy=(Math.floor(k/cols)+0.5)/Math.max(4,Math.ceil(n/cols));
      drawChunk(ctx,map.X(x0+0.006+(HB_W-0.012)*fx),map.Y(y0+0.004+(yf-y0-0.008)*fy),sz*0.8,'thermal',0.9); } }
  const tx=x1-0.008, frac=clamp((T-T_FREEZE)/(700-T_FREEZE),0,1);
  worldPoly(ctx,map,[[tx-0.0025,y0+0.012],[tx+0.0025,y0+0.012],[tx+0.0025,y1+0.012],[tx-0.0025,y1+0.012]],'#e9edf5',null);
  worldPoly(ctx,map,[[tx-0.0012,y0+0.012],[tx+0.0012,y0+0.012],[tx+0.0012,y0+0.012+(y1-y0)*frac],[tx-0.0012,y0+0.012+(y1-y0)*frac]],'#e0453a',null);
  lab(ctx,W,H,map.X(tx+0.006),map.Y(y1+0.004),fmt(kelvinC(T),1)+' °C','#e9edf5',SM_FONT,'left','middle');
  if(T>T_BOIL.water-10) for(let q=0;q<4;q++){ const cx=x0+HB_W*(0.25+0.17*q), cy=yf+0.01+0.012*(q%2);
    worldPoly(ctx,map,[[cx-0.01,cy],[cx,cy+0.007],[cx+0.01,cy],[cx,cy-0.005]],rgba('#e9edf5',0.35),null); }
}
function drawBulb(ctx,map,S,fluor){
  drawStand(ctx,map,0.02);
  worldPoly(ctx,map,[[UX-0.012,0.02],[UX+0.012,0.02],[UX+0.012,0.042],[UX-0.012,0.042]],'#8b93a6','#cfd4de',1);
  for(let k=1;k<4;k++) wline(ctx,map,[[UX-0.012,0.02+0.0055*k],[UX+0.012,0.02+0.0055*k-0.002]],'#5a6275',1);
  const lit=S.lit;
  if(lit>0){ worldPoly(ctx,map,ellipsePts(UX,0.075,0.055,0.055,30),rgba(fluor?'#e9f3ff':'#fff1a8',0.08+0.3*lit),null);
    worldPoly(ctx,map,ellipsePts(UX,0.075,0.036,0.036,30),rgba(fluor?'#e9f3ff':'#fff1a8',0.1+0.45*lit),null); }
  if(fluor){
    const pts=[]; for(let k=0;k<=90;k++){ const th=k/90*5*TAU; pts.push([UX+0.018*Math.sin(th),0.046+0.052*k/90]); }
    wline(ctx,map,pts,lit>0?mix('#8b93a6','#f4fbff',0.3+0.7*lit):'#8b93a6',4);
  } else {
    worldPoly(ctx,map,ellipsePts(UX,0.075,0.03,0.032,30),rgba('#e9edf5',0.08+0.25*lit),rgba('#e9edf5',0.7),1.2);
    const f=[]; for(let k=0;k<=8;k++) f.push([UX-0.008+0.016*k/8,0.066+((k%2)?0.003:-0.003)]);
    wline(ctx,map,[[UX-0.004,0.042],[UX-0.008,0.066]],'#8b93a6',1); wline(ctx,map,[[UX+0.004,0.042],[UX+0.008,0.066]],'#8b93a6',1);
    wline(ctx,map,f,lit>0?mix('#8b93a6','#fff1a8',0.3+0.7*lit):'#8b93a6',1.6);
  }
}
function drawFan(ctx,map,S){
  drawStand(ctx,map,0.012);
  const hub={x:UX-0.005,y:0.047};
  worldPoly(ctx,map,[[UX-0.022,0.006],[UX+0.012,0.006],[UX+0.012,0.03],[UX-0.022,0.03]],'#39414f','#8b93a6',1);
  for(let k=0;k<4;k++){ const a=S.fanAngle+TAU*k/4, c=Math.cos(a), s=Math.sin(a);
    worldPoly(ctx,map,[[hub.x,hub.y],[hub.x+0.03*c-0.009*s,hub.y+0.03*s+0.009*c],[hub.x+0.033*c,hub.y+0.033*s],[hub.x+0.03*c+0.006*s,hub.y+0.03*s-0.006*c]],'#aeb6c6',null); }
  worldPoly(ctx,map,ellipsePts(hub.x,hub.y,0.036,0.036,32),null,'#8b93a6',1.2);
  worldPoly(ctx,map,ellipsePts(hub.x,hub.y,0.005,0.005,12),'#cfd4de',null);
}
function drawSysChunks(ctx,map,S){
  const sz=clamp(0.0085*map.s,7,12);
  for(const f of S.flights){
    const p=pathAt(f.path,f.s), u=f.s/f.len;
    const radiate=/heat|refl|light|water|wind|loss|miss/.test(f.ch)&&f.ch!=='f.water';
    const a=radiate?clamp((1-u)*2.2,0,1):1;
    drawChunk(ctx,map.X(p[0]),map.Y(p[1]),sz,f.form,a);
  }
}
/* PhET's "Forms of Energy" key: the five forms, each chunk in its colour */
function drawFormLegend(ctx,W,H,G){
  let x=G.left+6; const y=G.legY+8;
  ctx.font=SM_FONT;
  lab(ctx,W,H,x,y,'forms of energy:','#8b93a6',SM_FONT,'left','middle');
  x+=17*10.5*0.52+10;
  for(const f of FORMS){
    drawChunk(ctx,x+6,y,11,f,1);
    lab(ctx,W,H,x+16,y,f,'#9aa2b4',SM_FONT,'left','middle');
    x+=f.length*10.5*0.52+34;
  }
}
function drawSystems(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[];
  const G=sysGeo(ctx,W,H), map=G.map, S=M.S, st=M.st;
  reserveCaption(G.left+4,G.capY,G.capTxt,G.capW,ctx);
  worldPoly(ctx,map,[[SYS_EXT.xmin+0.004,FLOOR-0.012],[SYS_EXT.xmax-0.004,FLOOR-0.012],[SYS_EXT.xmax-0.004,FLOOR],[SYS_EXT.xmin+0.004,FLOOR]],'#10151f',null);
  seg(ctx,map,[SYS_EXT.xmin+0.004,FLOOR],[SYS_EXT.xmax-0.004,FLOOR],rgba(COL.struct,0.55),1.2);
  wline(ctx,map,[[WIRE0.x,WIRE0.y],[WIRE1.x,WIRE1.y],[UX-0.02,-0.041],[UX-0.001,-0.036]],'#cfd4de',1.6);
  if(S.src==='biker') drawBiker(ctx,W,H,map,S,st); else if(S.src==='faucet') drawFaucet(ctx,map,S,st);
  else if(S.src==='sun') drawSun(ctx,map,S,st); else drawTeapot(ctx,map,S,st);
  if(S.conv==='generator'){
    drawGenerator(ctx,map,S);
    if(S.src==='biker') for(const L of beltLines(RW,RW_R,GW,GW_R)) wline(ctx,map,L,'#cfd4de',1.6);
  } else drawPanel(ctx,map,S);
  if(S.user==='heater') drawHeater(ctx,W,H,map,S,st); else if(S.user==='fan') drawFan(ctx,map,S);
  else drawBulb(ctx,map,S,S.user==='fluorescent');
  if(st.symSys) drawSysChunks(ctx,map,S);
  const F=M.F, ly=map.Y(FLOOR-0.012)+11;
  lab(ctx,W,H,map.X(SX),ly,srcName(S.src)+' · '+fmtW(F.srcIn),'#aeb6c6',SM_FONT,'center','middle');
  lab(ctx,W,H,map.X(CX),ly+15,convName(S.conv)+(M.takes?' · '+fmtW(F.cOut)+' out':' · cannot use it'),M.takes?'#aeb6c6':COL.ref,SM_FONT,'center','middle');
  lab(ctx,W,H,map.X(UX),ly,userName(S.user)+' · '+fmtW(F.uIn)+' in','#aeb6c6',SM_FONT,'center','middle');
  if(st.symSys) drawFormLegend(ctx,W,H,G);
  caption(ctx,G.left+4,G.capY,G.capTxt,G.capW,'#767e92',CAP_FONT);
  return G;
}
