
/* ================================================================== *
 *  drawing: the shared molecule layer and PhET's two model screens    *
 * ================================================================== */
/* the house #hint (HTML, bottom:11px, 11px type) sits on the last line of a
   caption anchored at H - 12: every caption here ends HINT_H higher, clear of
   it (lineage: build/wave-on-a-string) */
const HINT_H=18;
const TITLE_FONT='italic 13px Georgia, serif', BIG_FONT='italic 18px Georgia, serif';
const SMALL_FONT='10.5px -apple-system, sans-serif';
/* a canvas-safe signed number: the house minus sign, not a hyphen */
function sgn(v,n){ return (v<0?'&minus;':'')+fmt(Math.abs(v),n===undefined?2:n); }
let PICKS=[];                 /* draggable targets of the last draw */

/* a stage with one drawing box and a measured, bottom-anchored caption */
function stageMol(ctx,W,H,capFull,capShort,minBox){
  const narrow=isNarrow(W), left=20, right=narrow?W-20:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const top=stageTop()+22;
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+(minBox||240));
  const b=box(left,top,right-left,Math.max(80,fit.capY-14-top));
  return {narrow,left,right,capY:fit.capY,capTxt:fit.txt,capW,b};
}
function drawCap(ctx,L){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); }
/* model units -> pixels, equal on both axes (a molecule is a shape) */
function molMap(b,halfX,halfY){
  const s=Math.min(b.w/(2*halfX),b.h/(2*halfY));
  const cx=b.x+b.w/2, cy=b.y+b.h/2;
  return {s,cx,cy,X:x=>cx+s*x,Y:y=>cy+s*y,P:p=>[cx+s*p[0],cy+s*p[1]]};
}
function line2(ctx,x0,y0,x1,y1,col,w,cap){
  ctx.beginPath(); ctx.moveTo(x0,y0); ctx.lineTo(x1,y1);
  ctx.strokeStyle=col; ctx.lineWidth=w; ctx.lineCap=cap||'round'; ctx.stroke(); ctx.lineCap='butt';
}
function fillPoly(ctx,pts,fill,stroke,lw){
  ctx.beginPath(); pts.forEach((p,i)=>{ if(i===0) ctx.moveTo(p[0],p[1]); else ctx.lineTo(p[0],p[1]); });
  ctx.closePath();
  if(fill){ ctx.fillStyle=fill; ctx.fill(); }
  if(stroke){ ctx.strokeStyle=stroke; ctx.lineWidth=lw||1; ctx.stroke(); }
}
/* a shaded ball: base, a lit offset disc, a highlight (amino_acids.html's three discs) */
function ball(ctx,x,y,r,base,cue){
  dot(ctx,x,y,r,shade(base,0.5*(cue===undefined?1:cue)),null);
  if(r>=3){ const c=cue===undefined?1:cue;
    dot(ctx,x-0.2*r,y-0.2*r,0.64*r,shade(base,0.8*c),null);
    dot(ctx,x-0.34*r,y-0.34*r,0.24*r,mix(shade(base,c),'#ffffff',0.45),null); }
}
/* PhET's dipole arrow: a shaft, a solid head, and a cross bar at the tail
   (the chemistry symbol -- the bar marks the positive end) */
function dipoleArrow(ctx,x0,y0,ang,len,col,lw,bar){
  if(!(len>0.8)) return;
  const ux=Math.cos(ang), uy=Math.sin(ang), nx=-uy, ny=ux;
  const hl=Math.min(13,Math.max(5,0.34*len)), hw=Math.max(4,0.55*hl);
  const tx=x0+ux*(len-hl), ty=y0+uy*(len-hl);
  line2(ctx,x0,y0,tx,ty,col,lw||3.2);
  fillPoly(ctx,[[x0+ux*len,y0+uy*len],[tx+nx*hw,ty+ny*hw],[tx-nx*hw,ty-ny*hw]],col,null);
  if(bar!==false) line2(ctx,x0+nx*5.5,y0+ny*5.5,x0-nx*5.5,y0-ny*5.5,col,lw||3.2);
}

/* ---------------------------------------------------------------- *
 *  the surface: PhET's capsule (two discs of radius 2.25 r) filled   *
 *  strip by strip with the colour its linear gradient would paint.   *
 * ---------------------------------------------------------------- */
function drawSurface(ctx,map,m,kind,theta,scheme){
  if(kind==='none') return 0;
  const R=2.25*ATOM_DIAMETER/2, xa=-BOND_LENGTH/2, xb=BOND_LENGTH/2;
  const NS=112, x0=xa-R, x1=xb+R, dx=(x1-x0)/NS;
  ctx.save(); ctx.translate(map.cx,map.cy); ctx.rotate(theta); ctx.scale(map.s,map.s);
  let n=0;
  for(let i=0;i<NS;i++){
    const xl=x0+i*dx, xm=xl+dx/2;
    let hy=0;
    for(const xc of [xa,xb]){ const d=R*R-(xm-xc)*(xm-xc); if(d>0) hy=Math.max(hy,Math.sqrt(d)); }
    if(hy<=0) continue;
    ctx.fillStyle=rgbCss(surfaceColourScheme(kind,m.dEN,xm,scheme));
    ctx.fillRect(xl,-hy,dx*1.02,2*hy); n++;
  }
  ctx.restore();
  return n;
}
/* the colour key PhET draws under the surface control */
function drawColourKey(ctx,x,y,w,hh,kind,colourScheme){
  const stops=[];
  if(kind==='density'){ for(let i=0;i<=24;i++) stops.push(lerp3(RGB_WHITE,RGB_BLACK,i/24)); }
  else if(colourScheme==='roygb'){ for(let i=0;i<=34;i++) stops.push(roygb((0.5-i/34)/4)); }
  else { for(let i=0;i<=24;i++){ const s=i/24; stops.push(s<0.5?lerp3(RGB_BLUE,RGB_WHITE,2*s):lerp3(RGB_WHITE,RGB_RED,2*s-1)); } }
  const n=stops.length, cw=w/n;
  for(let i=0;i<n;i++){ ctx.fillStyle=rgbCss(stops[i]); ctx.fillRect(x+i*cw,y,cw*1.02,hh); }
  ctx.strokeStyle=COL.edge; ctx.lineWidth=1; ctx.strokeRect(x,y,w,hh);
  return n;
}

/* ---------------------------------------------------------------- *
 *  the plates.  PhET puts the NEGATIVE plate on the left and the     *
 *  POSITIVE on the right, so the field points in -x and the          *
 *  positive-to-negative arrow settles pointing at the + plate.       *
 * ---------------------------------------------------------------- */
function drawPlates(ctx,W,H,b,map,on){
  const px=map.X(-300), qx=map.X(300), y0=b.y+10, y1=b.y1-10;
  for(const [x,col,sgn] of [[px,COL.plateN,-1],[qx,COL.plateP,1]]){
    ctx.fillStyle=on?rgba(col,0.20):rgba(COL.dim,0.10);
    ctx.fillRect(x-7,y0,14,y1-y0);
    ctx.strokeStyle=on?col:COL.edge; ctx.lineWidth=1.4; ctx.strokeRect(x-7,y0,14,y1-y0);
    const cy=(y0+y1)/2, c=on?col:COL.dim;
    line2(ctx,x-6,cy,x+6,cy,c,2.4);
    if(sgn>0) line2(ctx,x,cy-6,x,cy+6,c,2.4);
    lab(ctx,W,H,x,y0-9,sgn>0?'positive plate':'negative plate',c,SMALL_FONT,'center','bottom');
  }
  if(on){ /* the field, from + (right) to - (left) */
    for(let k=0;k<4;k++){
      const y=y0+(y1-y0)*(k+0.5)/4;
      dipoleArrow(ctx,qx-24,y,PI,map.X(300)-map.X(-300)-48,rgba(COL.struct,0.30),2,false);
    }
    lab(ctx,W,H,(px+qx)/2,y0+12,'E points from + to &minus;',rgba(COL.struct,0.75),SMALL_FONT,'center','top');
  }
}

/* ---------------------------------------------------------------- *
 *  the bond-character bar (PhET's, 415 px of "more covalent" to      *
 *  "more ionic" with the pointer at |mu| / 2 of the way along)       *
 * ---------------------------------------------------------------- */
function drawBondChar(ctx,W,H,x,y,w,frac,name){
  const hh=13;
  const grd=[['#6fd0b0',0],['#cfd4de',0.5],['#e8843a',1]];
  const NS=40;
  for(let i=0;i<NS;i++){
    const t=(i+0.5)/NS;
    const c=t<0.5?mix(grd[0][0],grd[1][0],2*t):mix(grd[1][0],grd[2][0],2*t-1);
    ctx.fillStyle=c; ctx.fillRect(x+w*i/NS,y,w/NS*1.02,hh);
  }
  ctx.strokeStyle=COL.edge; ctx.lineWidth=1; ctx.strokeRect(x,y,w,hh);
  const px=x+w*clamp(frac,0,1);
  fillPoly(ctx,[[px,y-3],[px-5,y-11],[px+5,y-11]],COL.live,'#fff',1);
  lab(ctx,W,H,x,y+hh+4,'more covalent',COL.dim,SMALL_FONT,'left','top');
  lab(ctx,W,H,x+w,y+hh+4,'more ionic',COL.dim,SMALL_FONT,'right','top');
  lab(ctx,W,H,px,y-14,name,COL.live,SMALL_FONT,'center','bottom');
}

/* ================================================================== *
 *  view: two atoms (PhET's first screen)                              *
 * ================================================================== */
const TWO_CAP='PhET&rsquo;s Two Atoms screen. The bond dipole&rsquo;s length is |&Delta;EN| exactly, drawn at PhET&rsquo;s scale of 135 px for &Delta;EN = 2; '
  +'the partial charges are &plusmn;&Delta;EN. The surface is PhET&rsquo;s own linear gradient, stop for stop; PhET paints it at &alpha; = 0.72 over a pale '
  +'background, here it is opaque. Drag the molecule to turn it. Both axes are at one scale, PhET&rsquo;s drawing units: the bond is 150 and each atom 100 across.';
const TWO_CAP_S='PhET&rsquo;s Two Atoms screen: the bond dipole is |&Delta;EN| long, the charges are &plusmn;&Delta;EN, the surface is PhET&rsquo;s gradient. Drag to turn.';
function twoGeo(ctx,W,H){
  const L=stageMol(ctx,W,H,TWO_CAP,TWO_CAP_S,250);
  return {L,map:molMap(L.b,345/ST.zoom,215/ST.zoom)};
}
function drawTwo(ctx,W,H,M){
  const L=twoGeo(ctx,W,H), map=L.map, m=M.m, b=L.L.b;
  frame(ctx,b,COL.edge);
  if(ST.field) drawPlates(ctx,W,H,b,map,true);
  const nstrip=drawSurface(ctx,map,m,ST.surface,ST.molAngle,ST.surfColor);
  const A=map.P(m.A), B=map.P(m.B), r=map.s*ATOM_DIAMETER/2;
  line2(ctx,A[0],A[1],B[0],B[1],COL.bond,Math.max(3,map.s*18));
  ball(ctx,A[0],A[1],r,COL.atomA);
  ball(ctx,B[0],B[1],r,COL.atomB);
  PICKS=[{kind:'mol',x:(A[0]+B[0])/2,y:(A[1]+B[1])/2,r:Math.hypot(B[0]-A[0],B[1]-A[1])/2+r}];
  if(ST.showLabels){
    lab(ctx,W,H,A[0],A[1],'A','#1a1d26',BIG_FONT,'center','middle');
    lab(ctx,W,H,B[0],B[1],'B','#1a1d26',BIG_FONT,'center','middle');
  }
  /* the bond dipole, above the bond as PhET draws it */
  if(ST.showBondDipole&&m.mumag>1e-9){
    const mu=shownDipole(m.mu), ang=vang(mu), len=map.s*dipolePx(m.mumag)*1.15;
    const off=r+16, nx=Math.sin(ST.molAngle), ny=-Math.cos(ST.molAngle);
    const cx=(A[0]+B[0])/2+nx*off, cy=(A[1]+B[1])/2+ny*off;
    dipoleArrow(ctx,cx-Math.cos(ang)*len/2,cy-Math.sin(ang)*len/2,ang,len,COL.pos,3.4);
    lab(ctx,W,H,cx+nx*24,cy+ny*24,'bond dipole &mu; = '+fmt(m.mumag,2),COL.pos,SMALL_FONT,'center','middle');
  }
  if(ST.showCharges){
    /* over a pale surface the accent colours lose their contrast, so darken
       them there while keeping the hue that says which sign it is */
    const dark=ST.surface!=='none';
    for(const [P,q] of [[A,m.qA],[B,m.qB]]){
      const ux=(P[0]-map.cx), uy=(P[1]-map.cy), n=Math.hypot(ux,uy)||1;
      const c=q<0?COL.struct:COL.ref;
      lab(ctx,W,H,P[0]+ux/n*(r+16),P[1]+uy/n*(r+16),
        (q>0?'&delta;+':q<0?'&delta;&minus;':'&delta;')+' '+fmt(Math.abs(q),2),
        dark?mix(c,'#0a0d16',0.62):c,SMALL_FONT,'center','middle');
    }
  }
  /* the colour key */
  if(ST.surface!=='none'){
    const kx=b.x+14, ky=b.y+14, kw=Math.min(210,b.w*0.34);
    drawColourKey(ctx,kx,ky,kw,12,ST.surface,ST.surfColor);
    lab(ctx,W,H,kx,ky-4,ST.surface==='density'?'electron density':'electrostatic potential',COL.text,SMALL_FONT,'left','bottom');
    lab(ctx,W,H,kx,ky+16,ST.surface==='density'?'less':'positive',COL.dim,SMALL_FONT,'left','top');
    lab(ctx,W,H,kx+kw,ky+16,ST.surface==='density'?'more':'negative',COL.dim,SMALL_FONT,'right','top');
    lab(ctx,W,H,kx,ky+30,'gradient '+fmt(gradWidth(ST.surface,m.dEN),0)+' wide over a '+fmt(surfaceWidth(),0)+' surface',COL.dim,SMALL_FONT,'left','top');
    if(ST.surface==='potential'&&ST.surfColor==='roygb')
      lab(ctx,W,H,kx,ky+44,'PhET&rsquo;s rainbow scheme, which it applies to Real Molecules only',COL.dim,SMALL_FONT,'left','top');
  }
  if(ST.showBondChar){
    const bw=Math.min(BOND_CHAR_BAR,b.w-120);
    drawBondChar(ctx,W,H,b.x+(b.w-bw)/2,b.y1-42,bw,M.charFrac,M.character);
  }
  lab(ctx,W,H,b.x1-10,b.y+12,'dipole direction: '+dirTxt(),COL.dim,SMALL_FONT,'right','top');
  drawCap(ctx,L.L);
  return nstrip;
}

/* ================================================================== *
 *  view: three atoms (PhET's second screen)                           *
 * ================================================================== */
const THREE_CAP='PhET&rsquo;s Three Atoms screen. Drag atom A or atom C round B to change the bond angle, drag B to turn the whole molecule. '
  +'The two green bond dipoles add head to tail into the magenta molecular dipole, exactly, at every angle &mdash; and at 180&deg; with EN(A) = EN(C) '
  +'they cancel identically. PhET draws no surface here, because a dragged bond angle leaves the surface undefinable; neither does this. '
  +'One scale on both axes, PhET&rsquo;s drawing units.';
const THREE_CAP_S='Drag A or C to set the bond angle, B to turn the molecule: two bond dipoles adding to one molecular dipole. No surface, as in PhET.';
function threeGeo(ctx,W,H){
  const L=stageMol(ctx,W,H,THREE_CAP,THREE_CAP_S,250);
  return {L,map:molMap(L.b,(ST.field?345:265)/ST.zoom,215/ST.zoom)};
}
function drawThree(ctx,W,H,M){
  const L=threeGeo(ctx,W,H), map=L.map, m=M.m, b=L.L.b;
  frame(ctx,b,COL.edge);
  if(ST.field) drawPlates(ctx,W,H,b,map,true);
  const A=map.P(m.A), B=map.P(m.B), C=map.P(m.C), r=map.s*ATOM_DIAMETER/2;
  const lw=Math.max(3,map.s*18);
  line2(ctx,A[0],A[1],B[0],B[1],COL.bond,lw);
  line2(ctx,B[0],B[1],C[0],C[1],COL.bond,lw);
  /* the bond angle arc at B */
  const a1=Math.atan2(A[1]-B[1],A[0]-B[0]), a2=Math.atan2(C[1]-B[1],C[0]-B[0]);
  const rad=r+22, pts=[[B[0],B[1]]];
  let d=normAngle(a2-a1,-PI);
  for(let k=0;k<=24;k++){ const a=a1+d*k/24; pts.push([B[0]+rad*Math.cos(a),B[1]+rad*Math.sin(a)]); }
  fillPoly(ctx,pts,rgba(COL.struct,0.12),rgba(COL.struct,0.55),1.4);
  lab(ctx,W,H,B[0]+(rad+16)*Math.cos(a1+d/2),B[1]+(rad+16)*Math.sin(a1+d/2),
    fmt(M.bondAngleDeg,1)+'&deg;',COL.struct,SMALL_FONT,'center','middle');
  ball(ctx,A[0],A[1],r,COL.atomA); ball(ctx,B[0],B[1],r,COL.atomB); ball(ctx,C[0],C[1],r,COL.atomC);
  PICKS=[{kind:'A',x:A[0],y:A[1],r:r+8},{kind:'C',x:C[0],y:C[1],r:r+8},
         {kind:'mol',x:B[0],y:B[1],r:r+8}];
  if(ST.showLabels){
    lab(ctx,W,H,A[0],A[1],'A','#1a1d26',BIG_FONT,'center','middle');
    lab(ctx,W,H,B[0],B[1],'B','#1a1d26',BIG_FONT,'center','middle');
    lab(ctx,W,H,C[0],C[1],'C','#1a1d26',BIG_FONT,'center','middle');
  }
  if(ST.showCharges){
    /* A and C are labelled outward along their own bond; B is labelled along
       the OUTWARD bisector (the direction no bond points), never on the atom */
    const uA=[(A[0]-B[0]),(A[1]-B[1])], uC=[(C[0]-B[0]),(C[1]-B[1])];
    const na=Math.hypot(uA[0],uA[1])||1, nc=Math.hypot(uC[0],uC[1])||1;
    let bx=-(uA[0]/na+uC[0]/nc), by=-(uA[1]/na+uC[1]/nc);
    const nb=Math.hypot(bx,by);
    /* straight bonds leave no bisector: put the label above the atom, clear of
       the bond-angle arc that is drawn below it */
    if(nb<1e-6){ bx=0; by=-1; } else { bx/=nb; by/=nb; }
    /* B's label is pushed sideways off the bisector when the molecular dipole
       is drawn along it (there is no dipole to avoid when it cancels) */
    const side=m.mumag>1e-9?30:0;
    for(const [P,q,ux,uy,sd] of [[A,m.qA,uA[0]/na,uA[1]/na,0],[C,m.qC,uC[0]/nc,uC[1]/nc,0],[B,m.qB,bx,by,side]]){
      lab(ctx,W,H,P[0]+ux*(r+20)+sd*(-uy),P[1]+uy*(r+20)+sd*ux,
        (q>0?'&delta;+':q<0?'&delta;&minus;':'&delta;')+' '+fmt(Math.abs(q),2),
        q<0?COL.struct:COL.ref,SMALL_FONT,'center','middle');
    }
  }
  /* the bond dipoles, each drawn beside its bond */
  if(ST.showBondDipole){
    for(const [P,Q,v,nm] of [[A,B,m.muAB,'AB'],[B,C,m.muBC,'BC']]){
      const mag=vmag(v); if(mag<1e-9) continue;
      const mu=shownDipole(v), ang=vang(mu), len=map.s*dipolePx(mag)*1.15;
      const bx=(P[0]+Q[0])/2, by=(P[1]+Q[1])/2;
      const dxn=(Q[1]-P[1]), dyn=-(Q[0]-P[0]), nn=Math.hypot(dxn,dyn)||1;
      const off=(bx*0+1)*(r*0.62+12);
      let ox=dxn/nn*off, oy=dyn/nn*off;
      if((bx+ox-B[0])*(bx-B[0])+(by+oy-B[1])*(by-B[1])<0){ ox=-ox; oy=-oy; }
      dipoleArrow(ctx,bx+ox-Math.cos(ang)*len/2,by+oy-Math.sin(ang)*len/2,ang,len,COL.pos,3);
    }
    lab(ctx,W,H,b.x+12,b.y1-30,'bond dipoles |&mu;| = '+fmt(vmag(m.muAB),2)+' and '+fmt(vmag(m.muBC),2),COL.pos,SMALL_FONT,'left','bottom');
  }
  if(ST.showMolDipole){
    if(m.mumag>1e-9){
      const mu=shownDipole(m.mu), ang=vang(mu), len=map.s*dipolePx(m.mumag)*1.15;
      dipoleArrow(ctx,B[0]-Math.cos(ang)*len/2,B[1]-Math.sin(ang)*len/2,ang,len,COL.live,4);
      lab(ctx,W,H,B[0]+Math.cos(ang)*(len/2+18),B[1]+Math.sin(ang)*(len/2+18),
        'molecular dipole '+fmt(m.mumag,2),COL.live,SMALL_FONT,'center','middle');
    } else lab(ctx,W,H,B[0],B[1]-r-34,'molecular dipole = 0 exactly',COL.live,SMALL_FONT,'center','middle');
  }
  drawCap(ctx,L.L);
}
