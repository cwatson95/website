
/* ================================================================== *
 *  drawing primitives shared by the family: the needle field, the     *
 *  bar magnet, the Earth, the compass, the field meter, the coil, the *
 *  supplies, electrons.  Everything is an explicit polygon in device  *
 *  coordinates (Known-bad: the recorder has no ellipse(), and a       *
 *  scaled arc does not survive restore()).                            *
 * ================================================================== */
const HINT_H=18;       /* the house #hint (HTML, bottom 11 px) owns the last line: every caption ends above it */
function ellipsePts(cx,cy,rx,ry,rot,a0,a1,n){
  const out=[], c=Math.cos(rot||0), s=Math.sin(rot||0);
  n=n||40; a0=a0||0; a1=(a1===undefined)?TAU:a1;
  for(let i=0;i<=n;i++){ const t=a0+(a1-a0)*i/n, x=rx*Math.cos(t), y=ry*Math.sin(t); out.push([cx+x*c-y*s, cy+x*s+y*c]); }
  return out;
}
/* a label at exactly this place or not at all (lab() shifts by 16 px, which would carry the
   N and S off the magnet); it honours the same registry, so a tool's panel reserved before the
   magnet is drawn makes the letters underneath it step aside */
function labStrict(ctx,x,y,txt,col,font,align,base){
  const t=plain(txt), fs=parseFloat(font.match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  const lx=align==='center'?x-w/2:(align==='right'?x-w:x);
  const ly=base==='top'?y:(base==='middle'?y-hh/2:(base==='bottom'?y-hh:y-hh*0.8));
  const bx=[lx,ly,lx+w,ly+hh];
  if(!labFits(bx)) return false;
  LABELS.push(bx); ctx.fillStyle=col; ctx.font=font; ctx.textAlign=align; ctx.textBaseline=base; ctx.fillText(t,x,y);
  return true;
}
function pathPts(ctx,pts,close){ ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); }); if(close) ctx.closePath(); }
/* the world rectangle of the magnet (centre, axis angle) in device coordinates */
function magnetCorners(map,m,halfL,halfW){
  const c=Math.cos(m.ang), s=Math.sin(m.ang);
  const P=(u,v)=>[map.X(m.x+u*c-v*s), map.Y(m.y+u*s+v*c)];
  return {P, pts:[P(-halfL,-halfW),P(halfL,-halfW),P(halfL,halfW),P(-halfL,halfW)]};
}
/* the needle field: each needle a diamond, north half green (the computed direction), south
   half grey; brightness is PhET's display mapping of |B| */
function drawNeedleField(ctx,map,grid,scale){
  const Lh=NEEDLE_LEN/2*map.s*(scale||1), Wh=Math.max(1.2,NEEDLE_LEN*0.14*map.s*(scale||1));
  for(const n of grid){
    if(n.alpha<0.02) continue;
    const X=map.X(n.x), Y=map.Y(n.y), c=Math.cos(n.ang), s=-Math.sin(n.ang);
    const tip=[X+Lh*c,Y+Lh*s], tail=[X-Lh*c,Y-Lh*s], l=[X-Wh*s,Y+Wh*c], r=[X+Wh*s,Y-Wh*c];
    ctx.globalAlpha=n.alpha;
    pathPts(ctx,[tip,l,r],true); ctx.fillStyle=COL.north; ctx.fill();
    pathPts(ctx,[tail,l,r],true); ctx.fillStyle=COL.needleS; ctx.fill();
  }
  ctx.globalAlpha=1;
}
/* the bar magnet: N half green, S half magenta (field lines leave N and enter S, as they
   leave + and enter - in the charges sims); see-inside draws it as an outline with the
   interior field as small needles along the model's own B inside */
function drawBarMagnet(ctx,map,m,opt){
  const o=opt||{}, K=magnetCorners(map,m,MAG_B,MAG_R), P=K.P;
  /* ghost: the body drawn see-through so the field lines running through it stay visible --
     an opaque magnet hides the very thing the field-lines view exists to show (Known-bad) */
  const inside=!!o.seeInside, ghost=!!o.ghost;
  const nFill=ghost?rgba(COL.north,0.16):(inside?rgba(COL.north,0.10):mix('#070b18',COL.north,0.78));
  const sFill=ghost?rgba(COL.south,0.16):(inside?rgba(COL.south,0.10):mix('#070b18',COL.south,0.72));
  pathPts(ctx,[P(0,-MAG_R),P(MAG_B,-MAG_R),P(MAG_B,MAG_R),P(0,MAG_R)],true); ctx.fillStyle=nFill; ctx.fill();
  pathPts(ctx,[P(-MAG_B,-MAG_R),P(0,-MAG_R),P(0,MAG_R),P(-MAG_B,MAG_R)],true); ctx.fillStyle=sFill; ctx.fill();
  pathPts(ctx,K.pts,true); ctx.strokeStyle=(inside||ghost)?'#cfd4de':'#0b0e16'; ctx.lineWidth=(inside||ghost)?1.2:1.4; ctx.stroke();
  if(inside&&m.S>0){
    /* 7 x 2 needles like PhET's, but each points along the model's B at its place */
    const src={kind:'magnet',x:m.x,y:m.y,ang:m.ang,S:m.S}, c=Math.cos(m.ang), s=Math.sin(m.ang);
    const pts=[];
    for(let i=0;i<7;i++) for(const v of [-MAG_R*0.5,MAG_R*0.5]){ const u=-MAG_B+MAG_L*(i+0.5)/7; pts.push({x:m.x+u*c-v*s,y:m.y+u*s+v*c}); }
    const g=pts.map(p=>{ const B=magnetField(src,p.x,p.y,0), mg=Math.hypot(B[0],B[1]); return {x:p.x,y:p.y,ang:Math.atan2(B[1],B[0]),alpha:needleAlpha(mg)}; });
    drawNeedleField(ctx,map,g,0.9);
  }
  if(o.bound){
    /* the bound current K = M x n on the side wall: out of the page along one long edge,
       into it along the other (dots and crosses), the same current an equal solenoid carries */
    const n=9, r=Math.max(2.4,4.2*map.s);
    for(let i=0;i<n;i++){
      const u=-MAG_B+MAG_L*(i+0.5)/n;
      const A=P(u,MAG_R), B=P(u,-MAG_R);
      dot(ctx,A[0],A[1],r,'#070b18',COL.bound,1.1); dot(ctx,A[0],A[1],r*0.28,COL.bound);
      dot(ctx,B[0],B[1],r,'#070b18',COL.bound,1.1);
      ctx.beginPath(); ctx.moveTo(B[0]-r*0.62,B[1]-r*0.62); ctx.lineTo(B[0]+r*0.62,B[1]+r*0.62);
      ctx.moveTo(B[0]-r*0.62,B[1]+r*0.62); ctx.lineTo(B[0]+r*0.62,B[1]-r*0.62); ctx.strokeStyle=COL.bound; ctx.lineWidth=1.1; ctx.stroke();
    }
  }
  if(o.labels!==false&&map.s*MAG_R>7){
    const fs=Math.max(10,Math.min(20,MAG_R*1.1*map.s)), fnt='600 '+fs.toFixed(1)+'px -apple-system, sans-serif';
    const nP=P(MAG_B*0.62,0), sP=P(-MAG_B*0.62,0);
    labStrict(ctx,nP[0],nP[1],'N',(inside||ghost)?COL.north:'#0b0e16',fnt,'center','middle');
    labStrict(ctx,sP[0],sP[1],'S',(inside||ghost)?COL.south:'#0b0e16',fnt,'center','middle');
  }
}
/* the Earth (a qualitative picture, as PhET's): a globe round the magnet, geographic north at
   the magnet's SOUTH pole, because Earth's north magnetic pole is a south pole */
const EARTH_R=190;
function drawEarth(ctx,map,m){
  const X=map.X(m.x), Y=map.Y(m.y), R=EARTH_R*map.s;
  dot(ctx,X,Y,R,'#0f2438','#3d6d8f',1.2);
  const c=Math.cos(m.ang), s=-Math.sin(m.ang);   /* device-space unit vector along the magnet's N */
  ctx.strokeStyle='rgba(120,170,205,0.35)'; ctx.lineWidth=0.9;
  for(const lat of [-60,-30,0,30,60]){           /* parallels: chords perpendicular to the polar axis */
    const d=Math.sin(lat*D2R)*R, w=Math.cos(lat*D2R)*R;
    const cx=X-d*c, cy=Y-d*s;
    ctx.beginPath(); ctx.moveTo(cx-w*s,cy+w*c); ctx.lineTo(cx+w*s,cy-w*c); ctx.stroke();
  }
  for(const f of [0.35,0.75]){                    /* meridians: ellipses through the poles */
    pathPts(ctx,ellipsePts(X,Y,R,R*f,Math.atan2(s,c),0,TAU,48),false); ctx.stroke();
  }
  const gn=[X-R*1.08*c,Y-R*1.08*s];
  lab(ctx,99999,99999,gn[0],gn[1],'geographic N',COL.dim,SM_FONT,'center','middle');
}
/* the compass: PhET's ring (radius 35) and needle (length 55), at world scale */
function drawCompass(ctx,map,x,y,phi){
  const X=map.X(x), Y=map.Y(y), R=35*map.s, Lh=27.5*map.s, Wh=Math.max(2,7.7*map.s);
  dot(ctx,X,Y,R+4*map.s,'rgba(10,12,18,0.72)');
  ctx.beginPath(); ctx.arc(X,Y,R,0,TAU); ctx.strokeStyle='#aeb6c6'; ctx.lineWidth=Math.max(2,6*map.s); ctx.stroke();
  for(let k=0;k<8;k++){ const a=k*Math.PI/4; dot(ctx,X+R*Math.cos(a),Y-R*Math.sin(a),Math.max(1.4,2.6*map.s),'#070b18'); }
  const c=Math.cos(phi), s=-Math.sin(phi);
  const tip=[X+Lh*c,Y+Lh*s], tail=[X-Lh*c,Y-Lh*s], l=[X-Wh*s,Y+Wh*c], r=[X+Wh*s,Y-Wh*c];
  pathPts(ctx,[tip,l,r],true); ctx.fillStyle=COL.north; ctx.fill();
  pathPts(ctx,[tail,l,r],true); ctx.fillStyle='#d9dde6'; ctx.fill();
  dot(ctx,X,Y,Math.max(1.6,3*map.s),'#070b18','#aeb6c6',1);
}
/* the field meter: the probe (crosshair ring) and a body carrying B, Bx, By and theta */
function meterBodyBox(map,x,y){
  const X=map.X(x), Y=map.Y(y), r=Math.max(10,18*map.s);
  return {X,Y,r,bx:X-58,by:Y+r+Math.max(8,15*map.s),bw:116,bh:70};
}
function drawFieldMeter(ctx,map,x,y,rd,units){
  const G=meterBodyBox(map,x,y);
  ctx.beginPath(); ctx.moveTo(G.X,G.Y+G.r); ctx.lineTo(G.X,G.by); ctx.strokeStyle='#dfe3ea'; ctx.lineWidth=3; ctx.stroke();
  ctx.beginPath(); ctx.arc(G.X,G.Y,G.r,0,TAU); ctx.strokeStyle='#dfe3ea'; ctx.lineWidth=3; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(G.X-G.r*0.55,G.Y); ctx.lineTo(G.X+G.r*0.55,G.Y); ctx.moveTo(G.X,G.Y-G.r*0.55); ctx.lineTo(G.X,G.Y+G.r*0.55);
  ctx.strokeStyle=COL.live; ctx.lineWidth=1.4; ctx.stroke();
  ctx.fillStyle='rgba(16,19,27,0.94)'; ctx.fillRect(G.bx,G.by,G.bw,G.bh);
  ctx.strokeStyle='#3a4152'; ctx.lineWidth=1; ctx.strokeRect(G.bx+0.5,G.by+0.5,G.bw-1,G.bh-1);
  LABELS.push([G.bx,G.by,G.bx+G.bw,G.by+G.bh]);
  const rows=[['B',fmtField(rd.B,units)],['Bx',fmtField(rd.Bx,units)],['By',fmtField(rd.By,units)],['θ',fmtAngle(rd.ang)]];
  ctx.font='10.5px -apple-system, sans-serif';
  rows.forEach((rw,i)=>{ const yy=G.by+11+i*16;
    ctx.textAlign='left'; ctx.textBaseline='middle'; ctx.fillStyle='#8b93a6'; ctx.fillText(rw[0],G.bx+7,yy);
    ctx.textAlign='right'; ctx.fillStyle='#e9ecf2'; ctx.fillText(rw[1],G.bx+G.bw-7,yy); });
  return G;
}
/* ---------------- the coil (electromagnet and pickup) ---------------- *
 * each loop is drawn as an ellipse (width 0.36 of its height, a perspective hint only),
 * the back half first and dim, the front half after the field needles; the wire is drawn
 * at its world width */
/* #coil */
const COIL_TILT=0.28;
function loopPts(map,cx,cy,a,half){
  /* half: 'back' (the far side, z < 0, drawn left) or 'front' (z > 0, drawn right) */
  const X=map.X(cx), Y=map.Y(cy), ry=a*map.s, rx=a*COIL_TILT*map.s;
  return half==='back'?ellipsePts(X,Y,rx,ry,0,Math.PI/2,1.5*Math.PI,30):ellipsePts(X,Y,rx,ry,0,-Math.PI/2,Math.PI/2,30);
}
/* One half of every turn, in two passes: all the dark rims first, then all the copper, so one
   turn's rim cannot paint over its neighbour's face.  At PhET's wire width (16 mm) and loop
   spacing (0) the turns touch, and without the rims the coil reads as a solid tube. */
function drawCoilHalf(ctx,map,xs,cx,cy,a,wire,half){
  const lw=Math.max(2,wire*map.s), paths=xs.map(xk=>loopPts(map,cx+xk,cy,a,half));
  ctx.lineCap='round';
  for(const p of paths){ pathPts(ctx,p,false); ctx.strokeStyle='#0a0d15'; ctx.lineWidth=lw+2; ctx.stroke(); }
  for(const p of paths){ pathPts(ctx,p,false); ctx.strokeStyle=half==='back'?mix('#070b18',COL.copper,0.5):COL.copper; ctx.lineWidth=Math.max(1.2,lw-2.2); ctx.stroke(); }
  ctx.lineCap='butt';
}
/* electrons on the front halves, staggered turn by turn so they read as a flow along the
   winding rather than as a lattice */
function drawElectrons(ctx,map,xs,cx,cy,a,phase,per){
  const r=Math.max(1.8,3.2*map.s);
  xs.forEach((xk,k)=>{
    for(let i=0;i<per;i++){
      const t=(((i+(k%2?0.5:0))/per+phase)%1+1)%1, ang=-Math.PI/2+Math.PI*t;
      const X=map.X(cx+xk)+a*COIL_TILT*map.s*Math.cos(ang), Y=map.Y(cy)-a*map.s*Math.sin(ang);
      dot(ctx,X,Y,r,COL.electron,'#070b18',0.8);
    }
  });
}
/* #endcoil */
/* #emag */
/* the battery (PhET's DC supply): a cell whose + terminal is the side the current leaves by */
function drawBattery(ctx,map,x,y,V){
  const X=map.X(x), Y=map.Y(y), w=Math.max(96,140*map.s), h=Math.max(30,44*map.s), flip=V<0;
  ctx.fillStyle='#1b2130'; ctx.fillRect(X-w/2,Y-h/2,w,h);
  ctx.fillStyle=mix('#070b18',COL.copper,0.6); ctx.fillRect(flip?X-w/2:X+w/2-w*0.22,Y-h/2,w*0.22,h);
  ctx.strokeStyle='#5c6478'; ctx.lineWidth=1; ctx.strokeRect(X-w/2+0.5,Y-h/2+0.5,w-1,h-1);
  const nub=Math.max(5,7*map.s);
  ctx.fillStyle='#8b93a6'; ctx.fillRect(flip?X-w/2-nub:X+w/2,Y-h*0.22,nub,h*0.44);
  ctx.font='600 '+Math.max(10,12.5*map.s).toFixed(1)+'px -apple-system, sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillStyle='#e9ecf2';
  ctx.fillText((V>0?'+':V<0?'\u2212':'')+fmt(Math.abs(V),1)+' V',X+(flip?w*0.1:-w*0.1),Y);
  ctx.font='600 '+Math.max(9,11*map.s).toFixed(1)+'px -apple-system, sans-serif'; ctx.fillStyle='#0b0e16';
  ctx.fillText(flip?'\u2212':'+',flip?X-w/2+w*0.11:X+w/2-w*0.11,Y);
  return {left:[X-w/2-(flip?nub:0),Y],right:[X+w/2+(flip?0:nub),Y],w,h};
}
/* the AC supply: a box with its voltage trace over one period and the present point */
function drawACSupply(ctx,map,x,y,V,Vpk,phase){
  const X=map.X(x), Y=map.Y(y), w=120*map.s, h=58*map.s;
  ctx.fillStyle='#161b27'; ctx.fillRect(X-w/2,Y-h/2,w,h);
  ctx.strokeStyle='#5c6478'; ctx.lineWidth=1; ctx.strokeRect(X-w/2+0.5,Y-h/2+0.5,w-1,h-1);
  const bx=X-w/2+8*map.s, bw=w-16*map.s, by=Y-h/2+6*map.s, bh=h-24*map.s, amp=(bh/2)*(Vpk/AC_VMAX);
  ctx.beginPath(); ctx.moveTo(bx,by+bh/2); ctx.lineTo(bx+bw,by+bh/2); ctx.strokeStyle='#2a3142'; ctx.lineWidth=1; ctx.stroke();
  ctx.beginPath();
  for(let i=0;i<=48;i++){ const t=i/48, yy=by+bh/2-amp*Math.sin(TAU*t); if(i===0) ctx.moveTo(bx+bw*t,yy); else ctx.lineTo(bx+bw*t,yy); }
  ctx.strokeStyle=COL.ref; ctx.lineWidth=1.3; ctx.stroke();
  const pt=((phase%1)+1)%1; dot(ctx,bx+bw*pt,by+bh/2-amp*Math.sin(TAU*pt),Math.max(2,3*map.s),COL.live);
  ctx.font=Math.max(9.5,11*map.s).toFixed(1)+'px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='bottom';
  ctx.fillStyle='#e9ecf2'; ctx.fillText((V<0?'−':'')+fmt(Math.abs(V),1)+' V',X,Y+h/2-2);
  return {left:[X-w/2,Y],right:[X+w/2,Y]};
}
/* #endemag */
/* #gen */
/* The light bulb.  The MODEL brightness is PhET's own rule, |EMF| against full scale, and
   the readout prints it; but this generator's peak is only about a fifth of full scale, so
   the glass is painted through a display mapping, sqrt(b) -- the same kind of thing PhET does
   to the field needles' alpha.  BULB_GAMMA is that mapping and nothing else depends on it. */
const BULB_GAMMA=0.5, BULB_ON=0.02;
function bulbShade(b){ return Math.pow(Math.min(1,Math.max(0,b)),BULB_GAMMA); }
function drawBulb(ctx,map,x,y,b){
  const X=map.X(x), Y=map.Y(y), R=34*map.s, g=bulbShade(b);
  /* the glow in three nested discs rather than one: a single translucent circle reads as a
     disc with a hard edge, three of them fade */
  if(b>BULB_ON){ ctx.globalAlpha=Math.min(1,g);
    for(const k of [2.1,1.7,1.35]) dot(ctx,X,Y,R*(1+(k-1)*(0.4+0.6*g)),'rgba(255,224,130,0.11)');
    ctx.globalAlpha=1; }
  dot(ctx,X,Y,R,mix('#1b2130','#ffe38a',g),'#aeb6c6',1.2);
  ctx.fillStyle='#5c6478'; ctx.fillRect(X-R*0.45,Y+R*0.85,R*0.9,R*0.55);
  if(b>BULB_ON){ ctx.strokeStyle=rgba('#ffe38a',Math.min(1,g)); ctx.lineWidth=1.4;
    for(let k=0;k<8;k++){ const a=k*Math.PI/4+Math.PI/8; ctx.beginPath(); ctx.moveTo(X+R*1.15*Math.cos(a),Y-R*1.15*Math.sin(a)); ctx.lineTo(X+R*(1.35+0.5*g)*Math.cos(a),Y-R*(1.35+0.5*g)*Math.sin(a)); ctx.stroke(); } }
  return {bottom:[X,Y+R*1.4]};
}
/* the voltmeter: a dial from -90 to +90 degrees; the needle is (EMF / full scale) x 90 degrees */
function drawVoltmeter(ctx,map,x,y,deg,emf){
  const X=map.X(x), Y=map.Y(y), R=46*map.s;
  ctx.fillStyle='#161b27'; ctx.fillRect(X-R*1.15,Y-R*0.95,R*2.3,R*1.45);
  ctx.strokeStyle='#5c6478'; ctx.lineWidth=1; ctx.strokeRect(X-R*1.15+0.5,Y-R*0.95+0.5,R*2.3-1,R*1.45-1);
  ctx.beginPath(); ctx.arc(X,Y+R*0.3,R*0.95,Math.PI,2*Math.PI); ctx.strokeStyle='#5c6478'; ctx.lineWidth=1.2; ctx.stroke();
  for(const t of [-90,-45,0,45,90]){ const a=(90-t)*D2R, c=Math.cos(a), s=Math.sin(a);
    ctx.beginPath(); ctx.moveTo(X+R*0.82*c,Y+R*0.3-R*0.82*s); ctx.lineTo(X+R*0.95*c,Y+R*0.3-R*0.95*s); ctx.stroke(); }
  const a=(90-deg)*D2R;
  ctx.beginPath(); ctx.moveTo(X,Y+R*0.3); ctx.lineTo(X+R*0.88*Math.cos(a),Y+R*0.3-R*0.88*Math.sin(a)); ctx.strokeStyle=COL.live; ctx.lineWidth=2; ctx.stroke();
  dot(ctx,X,Y+R*0.3,Math.max(2,3*map.s),'#aeb6c6');
  ctx.font=Math.max(9.5,10.5*map.s).toFixed(1)+'px -apple-system, sans-serif'; ctx.textAlign='center'; ctx.textBaseline='bottom';
  ctx.fillStyle='#e9ecf2'; ctx.fillText(sigf(emf*1e3,3)+' mV',X,Y+R*0.48);
  return {bottom:[X,Y+R*0.5]};
}
/* #endgen */
/* a world-space polyline of meridional (rho, u) points about a source frame, one half */
function linePts(map,cx,cy,ang,pts,sgn){
  const c=Math.cos(ang), s=Math.sin(ang), out=new Array(pts.length);
  for(let i=0;i<pts.length;i++){ const u=pts[i][1], v=sgn*pts[i][0]; out[i]=[map.X(cx+u*c-v*s), map.Y(cy+u*s+v*c)]; }
  return out;
}
/* clip a device polyline to a box (Liang-Barsky per segment), stroke it, and record it */
function strokeClipped(ctx,b,pts,col,lw,dash){
  ctx.beginPath(); let started=false;
  for(let i=0;i<pts.length-1;i++){
    const X0=pts[i][0],Y0=pts[i][1],X1=pts[i+1][0],Y1=pts[i+1][1];
    let t0=0,t1=1; const dx=X1-X0, dy=Y1-Y0; let out=false;
    for(const [p,q] of [[-dx,X0-b.x],[dx,b.x1-X0],[-dy,Y0-b.y],[dy,b.y1-Y0]]){
      if(p===0){ if(q<0){ out=true; break; } continue; }
      const t=q/p; if(p<0){ if(t>t1){ out=true; break; } if(t>t0) t0=t; } else { if(t<t0){ out=true; break; } if(t<t1) t1=t; }
    }
    if(out||t0>t1){ started=false; continue; }
    const xa=X0+t0*dx, ya=Y0+t0*dy, xb=X0+t1*dx, yb=Y0+t1*dy;
    if(t0>0) started=false;
    if(!started){ ctx.moveTo(xa,ya); started=true; }
    ctx.lineTo(xb,yb); POLY_SEGS.push(xa,ya,xb,yb);
    if(t1<1) started=false;
  }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.3; if(dash) ctx.setLineDash(dash); ctx.stroke(); ctx.setLineDash([]);
}
/* an arrowhead at the midpoint of a device polyline, pointing along it (sgn -1 reverses) */
function lineArrow(ctx,b,pts,frac,col,sgn){
  if(pts.length<3) return;
  let L=0; const cum=[0];
  for(let i=1;i<pts.length;i++){ L+=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]); cum.push(L); }
  const target=L*frac; let i=1; while(i<pts.length-1&&cum[i]<target) i++;
  const p=pts[i], q=pts[i-1]; const X=p[0], Y=p[1];
  if(X<b.x+4||X>b.x1-4||Y<b.y+4||Y>b.y1-4) return;
  let ux=p[0]-q[0], uy=p[1]-q[1]; const m=Math.hypot(ux,uy)||1; ux=ux/m*(sgn||1); uy=uy/m*(sgn||1);
  const hh=6.5;
  ctx.beginPath(); ctx.moveTo(X+ux*hh*0.6,Y+uy*hh*0.6); ctx.lineTo(X-ux*hh*0.6-uy*hh*0.5,Y-uy*hh*0.6+ux*hh*0.5);
  ctx.lineTo(X-ux*hh*0.6+uy*hh*0.5,Y-uy*hh*0.6-ux*hh*0.5); ctx.closePath(); ctx.fillStyle=col; ctx.fill();
}
