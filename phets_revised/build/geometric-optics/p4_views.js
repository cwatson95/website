/* ================================================================== *
 *  view: the lens bench / the mirror bench  (PhET's two screens)      *
 *                                                                     *
 *  Everything here is drawn at EQUAL ASPECT and the scale is printed  *
 *  on the canvas: this is a construction in which the ray slopes have *
 *  to read correctly, so the two axes cannot be fitted independently  *
 *  (buoyancy/Rayleigh-Taylor Known-bad, the other way round).         *
 * ================================================================== */

/* Every layout reserves HINT_H at the bottom: the house #hint is HTML at
   bottom:11px and the canvas capture cannot see it, so a caption anchored at
   H - 12 would sit underneath it (Known-bad, wave-on-a-string).  The caption
   is painted LAST but occupies the bottom band from the moment the layout is
   known, so its rectangle goes into the label registry FIRST -- otherwise a
   stage label near the bottom dodges nothing and lands on the prose. */
function layout(ctx,W,H,full,short,nB,frac,nBn){
  const L=stageLayout(ctx,W,H-HINT_H,full,short,nB,frac,nBn);
  LABELS.push([L.left-2,L.capY-5,L.left+L.capW+2,H-HINT_H-6]);
  return L;
}
/* Anything non-obvious about the drawing itself -- above all a scale factor or
   a degenerate case -- belongs IN the caption, not floating above it: a second
   text block just above the caption band collides with the bottom panel's axis
   label at every canvas size that has one. */
function capWith(base,notes){ return notes.length?(base+' '+notes.join(' ')):base; }

/* The last layout, so selfTest can assert that nothing was drawn into the
   caption band.  Every geo function sets it. */
let LAST_L=null;

/* Liang-Barsky clip of a world-space segment to the world box.  A ray is DATA
   rather than an axis line, but the house rule covers both: everything drawn
   inside a frame is clipped to it.  Without this the outgoing rays ran across
   the caption and, in the analysis views, across the panel below -- found by
   looking at the PNGs, which is the only thing that can see it. */
function clipSeg(a,b,ext){
  let t0=0,t1=1;
  const dx=b[0]-a[0], dy=b[1]-a[1];
  const p=[-dx,dx,-dy,dy], q=[a[0]-ext.xmin,ext.xmax-a[0],a[1]-ext.ymin,ext.ymax-a[1]];
  for(let i=0;i<4;i++){
    if(p[i]===0){ if(q[i]<0) return null; continue; }
    const r=q[i]/p[i];
    if(p[i]<0){ if(r>t1) return null; if(r>t0) t0=r; }
    else { if(r<t0) return null; if(r<t1) t1=r; }
  }
  return [[a[0]+t0*dx,a[1]+t0*dy],[a[0]+t1*dx,a[1]+t1*dy]];
}
function segW(ctx,map,a,b,ext,col,lw,dash){
  const c=clipSeg(a,b,ext); if(!c) return false;
  seg(ctx,map,c[0],c[1],col,lw,dash); return true;
}
/* legendAuto() avoids CURVES and not LABELS, so it lands on a stage label that
   was drawn earlier (Known-bad, pupil_plane).  This checks both registries and
   then registers its own rectangle, so later labels dodge it as well.  If every
   corner is taken it draws nothing rather than a legend on top of the picture --
   the captions name the colours. */
function legendSafe(ctx,b,items){
  ctx.font='10.5px -apple-system, sans-serif';
  let w=0;
  for(const it of items) w=Math.max(w,ctx.measureText(plain(it[1])).width);
  const bw=w+26, bh=items.length*15+8;
  const cands=[[b.x1-bw-8,b.y+8],[b.x+8,b.y1-bh-8],[b.x+8,b.y+8],[b.x1-bw-8,b.y1-bh-8],
               [b.x+(b.w-bw)/2,b.y+8],[b.x+(b.w-bw)/2,b.y1-bh-8]];
  for(const c of cands){
    const cx=c[0], cy=c[1];
    if(cx<0||cy<0||cx+bw>b.x1+2||cy+bh>b.y1+2) continue;
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4){
      const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
      if(Math.max(x0,x1)<cx||Math.min(x0,x1)>cx+bw||
         Math.max(y0,y1)<cy||Math.min(y0,y1)>cy+bh) continue;
      hit=true;
    }
    if(!hit) for(const o of LABELS)
      if(cx<o[2]-0.5&&cx+bw>o[0]+0.5&&cy<o[3]-0.5&&cy+bh>o[1]+0.5){ hit=true; break; }
    if(!hit){ const r=legendBox(ctx,cx,cy,items); LABELS.push([cx,cy,cx+bw,cy+bh]); return r; }
  }
  return null;
}

/* a point source: PhET's Light scene has no arrow to image, it has a lamp */
function drawSource(ctx,map,P,alpha){
  const X=map.X(P[0]), Y=map.Y(P[1]);
  for(let i=0;i<8;i++){ const a=i*PI/4;
    ctx.beginPath();
    ctx.moveTo(X+7*Math.cos(a),Y+7*Math.sin(a));
    ctx.lineTo(X+12.5*Math.cos(a),Y+12.5*Math.sin(a));
    ctx.strokeStyle=rgba('#ffe9a8',0.8*alpha); ctx.lineWidth=1.3; ctx.stroke(); }
  dot(ctx,X,Y,4.5,rgba('#ffe9a8',0.95*alpha),'#fff',1.2);
}

/* the object silhouettes, in a unit frame: u across (-0.5..0.5), v along the
   object from the axis (0) to its tip (1).  They are flat cards standing on
   the optical axis; the image is the same card scaled by m, which is PhET's
   convention and is stated on the canvas. */
const OBJ_ASPECT={pencil:0.30,penguin:0.46,star:0.80,arrow:0.34,light:0.34};
const OBJ_SHAPE={
  pencil:[[-0.22,0],[0.22,0],[0.22,0.74],[0.16,0.84],[0,1],[-0.16,0.84],[-0.22,0.74]],
  penguin:[[-0.16,0],[-0.05,0.03],[0.05,0.03],[0.16,0],[0.13,0.07],
           [0.22,0.20],[0.30,0.42],[0.28,0.60],[0.20,0.72],
           [0.14,0.80],[0.13,0.88],[0.08,0.96],[0,0.99],[-0.08,0.96],[-0.13,0.88],
           [-0.14,0.80],[-0.20,0.72],[-0.28,0.60],[-0.30,0.42],[-0.22,0.20],[-0.13,0.07]],
  star:null,      /* built below */
  arrow:[[-0.06,0],[0.06,0],[0.06,0.68],[0.20,0.68],[0,1],[-0.20,0.68],[-0.06,0.68]],
  light:null
};
(function(){
  const pts=[];
  for(let i=0;i<10;i++){
    const a=PI/2+i*PI/5, r=(i%2===0)?0.5:0.20;
    pts.push([r*Math.cos(a),0.52+r*Math.sin(a)*1.0]);
  }
  /* a stem down to the axis so the star stands on it like the others */
  OBJ_SHAPE.star=pts.concat([[0.04,0.10],[0.04,0],[-0.04,0],[-0.04,0.10]]);
})();
function objPolyWorld(kind,x,tip,scale){
  const shp=OBJ_SHAPE[kind]||OBJ_SHAPE.arrow;
  const wid=OBJ_ASPECT[kind]*Math.abs(tip)*Math.abs(scale===undefined?1:scale);
  const hgt=tip*(scale===undefined?1:scale);
  return shp.map(p=>[x+p[0]*wid*2,p[1]*hgt]);
}

/* PhET's optic outline.  The lens uses the TRUE sag |R| - sqrt(R^2 - (D/2)^2)
   when the sphere can carry the aperture, and PhET's softened
   (D/2)^2/2(|R|+100) when it cannot -- which the canvas says. */
function opticOutline(op){
  const a=op.D/2, R=Math.abs(op.R);
  const trueSag=(a<R)?R-Math.sqrt(R*R-a*a):NaN;
  const sag=isFinite(trueSag)?trueSag:hollywoodSag(R,op.D);
  const NS=22, pts=[];
  if(op.kind==='mirror'){
    /* A CONCAVE mirror is the inside of a sphere whose centre of curvature sits
       in FRONT of it, so its rim reaches back toward the light (x < 0) and its
       vertex is the deepest point (x = 0).  A convex mirror is the other way
       round.  The first version had this backwards and drew a concave mirror
       with the shape of a convex one -- correct physics, wrong picture, and
       only a PNG can see it. */
    const s=(op.surface==='concave')?-1:1;
    if(op.surface==='flat') return {front:[[0,-a],[0,a]],body:null,sag:0,hollywood:false};
    for(let i=0;i<=NS;i++){
      const y=-a+2*a*i/NS;
      const sg=isFinite(trueSag)?(R-Math.sqrt(Math.max(R*R-y*y,0))):hollywoodSag(R,2*Math.abs(y));
      pts.push([s*sg,y]);
    }
    /* the silvered backing is BEHIND the mirror, which is +x for both kinds */
    const back=pts.slice().reverse().map(p=>[p[0]+5,p[1]]);
    return {front:pts,body:pts.concat(back),sag:sag,hollywood:!isFinite(trueSag)};
  }
  const conv=(op.surface==='convex');
  const front=[],back=[];
  for(let i=0;i<=NS;i++){
    const y=-a+2*a*i/NS;
    const sg=isFinite(trueSag)?(R-Math.sqrt(Math.max(R*R-y*y,0))):hollywoodSag(R,2*Math.abs(y));
    if(conv){ front.push([-(sag-sg),y]); back.push([sag-sg,y]); }
    else    { front.push([-sg,y]);       back.push([sg,y]); }
  }
  return {front:front,body:front.concat(back.slice().reverse()),sag:sag,
          hollywood:!isFinite(trueSag)};
}

function drawOptic(ctx,map,op){
  const o=opticOutline(op);
  if(op.surface==='flat'){
    ctx.strokeStyle=COL.glass2; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(map.X(0),map.Y(-op.D/2)); ctx.lineTo(map.X(0),map.Y(op.D/2)); ctx.stroke();
    POLY_SEGS.push(map.X(0),map.Y(-op.D/2),map.X(0),map.Y(op.D/2));
    /* the hatching that says "this side is the back" */
    for(let i=0;i<=10;i++){
      const y=-op.D/2+op.D*i/10;
      ctx.beginPath(); ctx.moveTo(map.X(0),map.Y(y)); ctx.lineTo(map.X(0)+7,map.Y(y)+7);
      ctx.strokeStyle=rgba(COL.glass2,0.6); ctx.lineWidth=1; ctx.stroke();
    }
    return o;
  }
  worldPoly(ctx,map,o.body,rgba(COL.glass,0.42),COL.glass2,1.6);
  return o;
}

/* a small cross marker with a label */
function markPoint(ctx,W,H,map,x,y,col,txt,dy){
  const X=map.X(x), Y=map.Y(y), r=4.5;
  ctx.strokeStyle=col; ctx.lineWidth=1.6;
  ctx.beginPath(); ctx.moveTo(X-r,Y-r); ctx.lineTo(X+r,Y+r);
  ctx.moveTo(X-r,Y+r); ctx.lineTo(X+r,Y-r); ctx.stroke();
  if(txt) lab(ctx,W,H,X,Y+(dy===undefined?-12:dy),txt,col,SM_FONT,'center');
}

function drawRuler(ctx,W,H,map,y0){
  const L=PHET.rulerH, x0=-L/2;
  const Y=map.Y(y0), X0=map.X(x0), X1=map.X(x0+L);
  ctx.fillStyle='rgba(20,26,40,.86)'; ctx.fillRect(X0,Y,X1-X0,19);
  frame(ctx,box(X0,Y,X1-X0,19),'#39506b');
  ctx.textAlign='center'; ctx.textBaseline='top'; ctx.font='9px -apple-system, sans-serif';
  for(let c=0;c<=L;c+=10){
    const X=map.X(x0+c), big=(c%50===0);
    ctx.strokeStyle='#8fb8d4'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(X,Y); ctx.lineTo(X,Y+(big?9:5)); ctx.stroke();
    if(big){ ctx.fillStyle='#8fb8d4'; ctx.fillText(String(c),X,Y+9); }
  }
  /* the ruler's own name goes ABOVE the band: inside it, it lands on the
     zero tick label, which is exactly where the eye looks first */
  lab(ctx,W,H,X0+2,Y-8,'PhET&rsquo;s 260 cm ruler','#6f7789',SM_FONT,'left');
}

const BENCH_CAP_FULL=
 'PhET&rsquo;s bench. Drag the object (or use the sliders); the rays are bent by u&prime; = u &minus; h/f '
+'at the optic plane and nothing else &mdash; so where they meet IS the image the thin-optic equation '
+'gives, to machine precision, and the readout prints the residual. Solid green: light that really '
+'goes there. Dashed orange: the backward extension, which is all a virtual image ever is.';
const BENCH_CAP_SHORT='Rays bent by u&prime; = u &minus; h/f meet at the image the equation gives.';

/* the notes the bench must print, whatever the caption ends up saying */
function benchNotes(M,st,map){
  const op=M.op, notes=[];
  notes.push('Equal aspect, '+sigf(map?map.s:1,3)+' px per cm.');
  const a=op.D/2, R=Math.abs(op.R);
  if(!(a<R)) notes.push('The drawn lens uses PhET&rsquo;s softened sag: R = '+sigf(R,3)
    +' cm cannot carry a '+sigf(a,3)+' cm semi-aperture.');
  if(!isFinite(M.img.di)) notes.push('d_o = f exactly: there is no image and the outgoing rays are parallel.');
  else if(M.offFrame) notes.push('The image is off the frame, at x = '+sigf(M.img.x,5)+' cm.');
  if(M.nThrough===0&&st.rays!=='none') notes.push('No ray reaches the optic at this aperture.');
  if(op.flat) notes.push('PhET&rsquo;s flat mirror is f = 100 000 cm, not a plane: its image sits '
    +sigf(Math.abs(M.img.di)-M.dO,3)+' cm further back and m = '+fmt(M.img.m,5)+', not 1.');
  return notes;
}
function benchGeo(ctx,W,H,M,st){
  st=st||ST;
  /* the map is needed for the scale note and the note changes the caption
     height, so the layout is taken twice: once to size the world, once with
     the finished caption.  Both are cheap. */
  const L0=stageLayout(ctx,W,H-HINT_H,BENCH_CAP_FULL,BENCH_CAP_SHORT,0,0,0);
  const notes=benchNotes(M,st,worldFitUp(L0.main,M.ext,8));
  const L=layout(ctx,W,H,capWith(BENCH_CAP_FULL,notes),capWith(BENCH_CAP_SHORT,notes),0,0,0);
  LAST_L=L;
  return {L:L,map:worldFitUp(L.main,M.ext,8)};
}

function drawBench(ctx,W,H,M,st){
  const G=benchGeo(ctx,W,H,M,st), L=G.L, map=G.map;
  const op=M.op, ext=M.ext;
  /* the optical axis */
  seg(ctx,map,[ext.xmin,0],[ext.xmax,0],rgba(COL.axis,0.95),1.2,[6,5]);
  lab(ctx,W,H,map.X(ext.xmin)+4,map.Y(0)+(M.P[1]>=0?11:-10),'optical axis',COL.axis,SM_FONT,'left');

  /* F and 2F.  A lens has them on both sides; a concave mirror has both to the
     LEFT, a convex mirror both to the right, and a flat mirror has none
     (PhET's doc/model.md says exactly this). */
  const fa=Math.abs(op.f);
  if(M.drawF){
    for(const s of M.fSides){
      if(st.showF) markPoint(ctx,W,H,map,s*fa,0,COL.ref,st.showLabels?'F':'',-11);
      if(st.show2F) markPoint(ctx,W,H,map,s*2*fa,0,rgba(COL.ref,0.65),st.showLabels?'2F':'',-11);
    }
  }

  /* the rays, under the optic and the object so the shapes stay readable */
  M.bundles.forEach(b=>{
    const alpha=b.tag===1?1:0.55;
    b.rays.forEach(r=>{
      segW(ctx,map,r.inSeg[0],r.inSeg[1],ext,rgba(COL.ray,0.9*alpha),1.5);
      if(r.outSeg) segW(ctx,map,r.outSeg[0],r.outSeg[1],ext,rgba(r.missed?COL.dim:COL.ray,0.9*alpha),1.5);
      if(r.virtSeg&&st.showVirtual) segW(ctx,map,r.virtSeg[0],r.virtSeg[1],ext,rgba(COL.virt,0.85*alpha),1.6,[5,4]);
    });
  });

  /* PhET's guides */
  if(M.guides){
    M.guides.forEach(g=>{
      [g.top,g.bot].forEach(a=>{
        const arm=Math.min(Math.abs(M.P[0]),240)*0.55;
        const A=[a.fulcrum[0]+arm*Math.cos(a.incident),a.fulcrum[1]+arm*Math.sin(a.incident)];
        const B=[a.fulcrum[0]+arm*Math.cos(a.transmitted),a.fulcrum[1]+arm*Math.sin(a.transmitted)];
        segW(ctx,map,a.fulcrum,A,ext,rgba(COL.guide,0.75),2.4);
        segW(ctx,map,a.fulcrum,B,ext,rgba(COL.guide,0.75),2.4);
        dot(ctx,map.X(a.fulcrum[0]),map.Y(a.fulcrum[1]),3,COL.guide,'#fff',1);
      });
      if(isFinite(g.cross.x)) markPoint(ctx,W,H,map,g.cross.x,g.cross.y,COL.guide,
        st.showLabels&&g.tag===1?'guides cross':'',12);
    });
  }

  /* the projection screen and the light spots */
  if(M.light){
    const sx=M.screenX, hH=PHET.screenH/2;
    worldPoly(ctx,map,[[sx-8,-hH],[sx+8,-hH],[sx+8,hH],[sx-8,hH]],'rgba(200,206,220,.16)','#aeb6c6',1.4);
    M.bundles.forEach(b=>{
      if(!b.spot) return;
      const y0=Math.min(b.spot.top,b.spot.bottom), y1=Math.max(b.spot.top,b.spot.bottom);
      const I=spotIntensity(b.spot.diameter,op.D);
      const yy0=clamp(y0,-hH,hH), yy1=clamp(y1,-hH,hH);
      if(yy1>yy0) worldPoly(ctx,map,[[sx-8,yy0],[sx+8,yy0],[sx+8,yy1],[sx-8,yy1]],
        rgba('#ffe9a8',0.18+0.7*I),null,0);
    });
    lab(ctx,W,H,map.X(sx),map.Y(hH)-12,'screen (geometric shadow)','#aeb6c6',SM_FONT,'center');
  }

  /* the optic */
  const oo=drawOptic(ctx,map,op);
  seg(ctx,map,[0,-op.D/2],[0,op.D/2],rgba(COL.struct,0.35),1,[3,4]);

  /* the object and its image */
  M.bundles.forEach(b=>{
    const alpha=b.tag===1?1:0.55;
    if(M.light) drawSource(ctx,map,b.P,alpha);
    else {
      if(Math.abs(b.P[1])>1.5)
        worldPoly(ctx,map,objPolyWorld(st.objKind,b.P[0],b.P[1]),rgba(COL.obj,0.32*alpha),COL.obj,1.6);
      dot(ctx,map.X(b.P[0]),map.Y(b.P[1]),3.5,COL.obj,'#fff',1);
    }
    const im=b.img;
    if(isFinite(im.x)&&(!im.virtual||st.showVirtual)&&Math.abs(im.x)<4000&&Math.abs(im.y)<4000){
      const dash=im.virtual?[5,4]:null;
      /* a POINT source has a point image: drawing a silhouette there would be
         a picture of something that is not in the model */
      if(Math.abs(im.y)>1.5&&!M.light){
        const poly=objPolyWorld(st.objKind,im.x,b.P[1]*im.m,1);
        worldPoly(ctx,map,poly,rgba(COL.img,(im.virtual?0.12:0.28)*alpha),
                  im.virtual?COL.virt:COL.img,1.6,dash);
      }
      dot(ctx,map.X(im.x),map.Y(im.y),3.5,im.virtual?COL.virt:COL.img,'#fff',1);
    }
  });

  /* labels */
  if(st.showLabels){
    lab(ctx,W,H,map.X(M.P[0]),map.Y(M.P[1])-13,'Object',COL.obj,LAB_FONT,'center');
    const im=M.img;
    if(isFinite(im.x)&&(!im.virtual||st.showVirtual)&&Math.abs(im.x)<4000)
      lab(ctx,W,H,map.X(im.x),map.Y(im.y)+(im.y<0?15:-13),
          im.virtual?'Virtual Image':'Real Image',im.virtual?COL.virt:COL.img,LAB_FONT,'center');
    lab(ctx,W,H,map.X(0),map.Y(op.D/2)-13,surfName(M),COL.glass2,LAB_FONT,'center');
  }
  if(st.showRuler) drawRuler(ctx,W,H,map,ext.ymin+6);

  /* everything the reader must not have to assume is already in the caption */
  drawCaption(ctx,L);
  legendSafe(ctx,L.main,[[COL.ray,'real ray'],[COL.virt,'virtual extension'],
    [COL.obj,'object'],[COL.img,'image'],[COL.ref,'F, 2F']]);
}
