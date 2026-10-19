/* ================================================================== *
 *  views: the conjugate curve, the lens maker, the guides,            *
 *         the real lens  --  then the dispatch and the scene          *
 * ================================================================== */

/* ------------------------------------------------------ the conjugate curve */
const CONJ_CAP_FULL=
 'The law itself. d_i against d_o is a rectangular hyperbola whose asymptotes are d_o = f and '
+'d_i = f: bring the object in toward the focal point and the image runs away to infinity, cross it '
+'and the image reappears on the other side as a virtual one. Newton&rsquo;s form says the same thing '
+'in one product &mdash; measure both distances from the focal points and they multiply to f&sup2;. '
+'The lower panel is the magnification, which changes sign at the same place.';
const CONJ_CAP_SHORT='d_i against d_o: a hyperbola with asymptotes d_o = f and d_i = f. m changes sign at the pole.';

function conjGeo(ctx,W,H,M){
  const fa=Math.abs(M.f);
  const ylo=-3.2*fa, yhi=5.2*fa;
  const note='The d_i axis is cut at '+fmt(ylo,0)+' and '+fmt(yhi,0)
    +' cm &mdash; the curve really does run to &plusmn;&infin; at the pole &mdash; and m is cut at &plusmn;4.2.';
  const L=layout(ctx,W,H,CONJ_CAP_FULL+' '+note,CONJ_CAP_SHORT+' '+note,1,0.40,1);
  LAST_L=L;
  return {L:L,ylo:ylo,yhi:yhi,mlo:-4.2,mhi:4.2};
}
function drawConj(ctx,W,H,M,st){
  const G=conjGeo(ctx,W,H,M), L=G.L, b=L.main, b2=L.bottom[0];
  axesR(ctx,b,M.xlo,M.xhi,G.ylo,G.yhi,{xlab:'object distance d_o, cm',
    ylab:'image distance d_i, cm',title:titleFor(b,'the image distance against the object distance','d_i against d_o'),
    nx:7,ny:7,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  /* the asymptotes, clipped by polyline to the frame */
  if(M.pole!==null){
    polyline(ctx,b,[M.pole,M.pole],[G.ylo,G.yhi],M.xlo,M.xhi,G.ylo,G.yhi,rgba(COL.ref,0.55),1.2,[5,4]);
    lab(ctx,W,H,b.x+b.w*(M.pole-M.xlo)/(M.xhi-M.xlo)+5,b.y+13,'d_o = f',COL.ref,SM_FONT,'left');
  }
  polyline(ctx,b,[M.xlo,M.xhi],[M.f,M.f],M.xlo,M.xhi,G.ylo,G.yhi,rgba(COL.ref,0.55),1.2,[5,4]);
  lab(ctx,W,H,b.x1-5,b.y1-b.h*(M.f-G.ylo)/(G.yhi-G.ylo)-9,'d_i = f',COL.ref,SM_FONT,'right');
  polyline(ctx,b,[M.xlo,M.xhi],[0,0],M.xlo,M.xhi,G.ylo,G.yhi,rgba(COL.axis,0.9),1);
  M.branches.forEach(br=>polyline(ctx,b,br.xs,br.ys,M.xlo,M.xhi,G.ylo,G.yhi,COL.pos,2));
  if(isFinite(M.di)&&M.di>G.ylo&&M.di<G.yhi) marker(ctx,b,M.xlo,M.xhi,G.ylo,G.yhi,M.dO,M.di,COL.live);
  else lab(ctx,W,H,b.x+b.w*(M.dO-M.xlo)/(M.xhi-M.xlo),b.y+30,
      isFinite(M.di)?'d_i = '+sigf(M.di,5)+' cm, off this axis':'d_i is infinite here',COL.live,SM_FONT,'center');
  lab(ctx,W,H,b.x1-8,b.y1-10,'d_i > 0: real, on the far side'+(M.f>0?'':' \u2014 a diverging optic never reaches it'),
      COL.pos,SM_FONT,'right');

  axesR(ctx,b2,M.xlo,M.xhi,G.mlo,G.mhi,{xlab:'object distance d_o, cm',ylab:'m',
    title:'the magnification m = &minus;d_i/d_o',nx:7,ny:5,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  polyline(ctx,b2,[M.xlo,M.xhi],[0,0],M.xlo,M.xhi,G.mlo,G.mhi,rgba(COL.axis,0.9),1);
  polyline(ctx,b2,[M.xlo,M.xhi],[-1,-1],M.xlo,M.xhi,G.mlo,G.mhi,rgba(COL.ref,0.5),1.1,[5,4]);
  M.branches.forEach(br=>polyline(ctx,b2,br.xs,br.ms,M.xlo,M.xhi,G.mlo,G.mhi,COL.pos,2));
  if(M.pole!==null)
    polyline(ctx,b2,[M.pole,M.pole],[G.mlo,G.mhi],M.xlo,M.xhi,G.mlo,G.mhi,rgba(COL.ref,0.55),1.2,[5,4]);
  if(isFinite(M.m)&&M.m>G.mlo&&M.m<G.mhi) marker(ctx,b2,M.xlo,M.xhi,G.mlo,G.mhi,M.dO,M.m,COL.live);
  if(M.f>0) lab(ctx,W,H,b2.x1-6,b2.y1-b2.h*(-1-G.mlo)/(G.mhi-G.mlo)-8,'m = &minus;1 at d_o = 2f',COL.ref,SM_FONT,'right');
  drawCaption(ctx,L);
  legendSafe(ctx,b,[[COL.pos,'the solved d_i'],[COL.ref,'asymptotes'],[COL.live,'this bench']]);
}

/* ---------------------------------------------------------- the lens maker */
const MAKER_CAP_FULL=
 'Where f comes from. PhET gives both surfaces the same radius, so the lens maker&rsquo;s equation '
+'collapses to f = R/2(n&minus;1) and its contours in the (n, R) plane are straight lines through '
+'n = 1 &mdash; a lens of index 1 is not a lens. PhET offers the same optic two ways: set f directly '
+'with n pinned at 1.5, or set R and n and let f follow. The panel on the right is the shape the '
+'artwork actually draws, against the shape those numbers describe.';
const MAKER_CAP_SHORT='f = R/2(n&minus;1): contours in the (n, R) plane, and the drawn shape against the real one.';

const MAKER_NOTE='The contours are exact lines: R = 2f(n&minus;1). Neither panel is a ray trace &mdash; the '
+'bench treats this lens as ideal, and only THE REAL LENS asks what its two spheres actually do.';
function makerGeo(ctx,W,H,M){
  const L=layout(ctx,W,H,MAKER_CAP_FULL+' '+MAKER_NOTE,MAKER_CAP_SHORT+' '+MAKER_NOTE,1,0.42,1);
  LAST_L=L;
  return {L:L};
}
function drawMaker(ctx,W,H,M,st){
  const G=makerGeo(ctx,W,H,M), L=G.L, b=L.main, b2=L.bottom[0];
  const nlo=PHET.iorLens[0], nhi=PHET.iorLens[1], rlo=PHET.rocLens[0], rhi=PHET.rocLens[1];
  axesR(ctx,b,nlo,nhi,rlo,rhi,{xlab:'index of refraction n',ylab:'radius of curvature |R|, cm',
    title:titleFor(b,'contours of the focal length in PhET&rsquo;s (n, R) box','f in the (n, R) box'),
    nx:7,ny:6,xfmt:t=>fmt(t,2),yfmt:t=>fmt(t,0)});
  M.contours.forEach(c=>{
    const near=Math.abs(c.f-M.f)<1e-9;
    polyline(ctx,b,c.xs,c.ys,nlo,nhi,rlo,rhi,near?COL.pos:rgba(COL.struct,0.55),near?2.2:1.2);
    /* label each contour at the middle of the span it has INSIDE the box: a
       label at the box edge lands in the tick row and reads as a collision */
    const inb=[];
    for(let i=0;i<c.xs.length;i++) if(c.ys[i]>=rlo&&c.ys[i]<=rhi) inb.push(i);
    if(inb.length>3){
      const k=inb[Math.floor(inb.length/2)];
      lab(ctx,W,H,b.x+b.w*(c.xs[k]-nlo)/(nhi-nlo),
        b.y1-b.h*(c.ys[k]-rlo)/(rhi-rlo)-9,'f = '+c.f,near?COL.pos:rgba(COL.struct,0.8),
        SM_FONT,'center');
    }
  });
  marker(ctx,b,nlo,nhi,rlo,rhi,M.n,M.R,COL.live);
  {
    const mY=b.y1-b.h*(M.R-rlo)/(rhi-rlo);
    lab(ctx,W,H,b.x+b.w*(M.n-nlo)/(nhi-nlo)+8,clamp(mY+12,b.y+10,b.y1-10),
        'f = '+sigf(M.f,4)+' cm',COL.live,LAB_FONT,'left');
  }
  lab(ctx,W,H,b.x+8,b.y+14,'PhET&rsquo;s direct model sits on n = 1.50, where R = f exactly',
      rgba(COL.ref,0.95),SM_FONT,'left');
  polyline(ctx,b,[1.5,1.5],[rlo,rhi],nlo,nhi,rlo,rhi,rgba(COL.ref,0.6),1.2,[5,4]);

  /* the drawn shape against the real one, at equal aspect */
  const a=M.D/2;
  const ext={xmin:-Math.max(M.sagDrawn,isFinite(M.sagTrue)?M.sagTrue:0)*1.5-4,
             xmax:Math.max(M.sagDrawn,isFinite(M.sagTrue)?M.sagTrue:0)*1.5+4,
             ymin:-a-4,ymax:a+4};
  const map=worldFitUp(b2,ext,2);
  const trueProf=[],drawnProf=[];
  for(let i=0;i<=28;i++){
    const y=-a+2*a*i/28;
    if(isFinite(M.sagTrue)) trueProf.push([-(M.sagTrue-(M.R-Math.sqrt(Math.max(M.R*M.R-y*y,0)))),y]);
    drawnProf.push([-(M.sagDrawn-hollywoodSag(M.R,2*Math.abs(y))),y]);
  }
  const mirrorX=p=>p.map(q=>[-q[0],q[1]]);
  if(trueProf.length)
    worldPoly(ctx,map,trueProf.concat(mirrorX(trueProf).reverse()),rgba(COL.glass,0.40),COL.glass2,1.6);
  worldPoly(ctx,map,drawnProf.concat(mirrorX(drawnProf).reverse()),null,COL.ref,1.6,[5,4]);
  frame(ctx,b2,'#242a3a');
  lab(ctx,W,H,b2.x+8,b2.y+12,'the shape PhET draws (dashed) against the sphere it names',
      '#aeb6c6',LAB_FONT,'left');
  lab(ctx,W,H,b2.x+8,b2.y+28,'drawn half-thickness '+sigf(M.sagDrawn,4)+' cm',COL.ref,SM_FONT,'left');
  lab(ctx,W,H,b2.x+8,b2.y+42,M.exists?('true sag '+sigf(M.sagTrue,4)+' cm'):
      'no sphere of this radius carries this aperture',M.exists?COL.glass2:COL.live,SM_FONT,'left');
  lab(ctx,W,H,b2.x1-8,b2.y1-10,'equal aspect, '+sigf(map.s,3)+' px per cm','#6f7789',SM_FONT,'right');
  drawCaption(ctx,L);
}

/* ------------------------------------------------------------- the guides */
const GUIDE_CAP_FULL=
 'PhET invented the guides: two arms hinged at the rim of the lens, each turning the light through '
+'a fixed angle 2 arctan(D/4f). Where the two transmitted arms cross is meant to be the image. It very '
+'nearly is &mdash; and the gap is instructive, because a thin optic changes a ray&rsquo;s SLOPE by '
+'&minus;h/f while a guide rotates it by an ANGLE. The lower panel shrinks the lens and the object '
+'inclination together: the miss falls as the square, so the guides are the thin-optic construction '
+'to second order and no further. Orange: the guides. Green: the true rim rays, which the incident '
+'arms lie exactly on top of.';
const GUIDE_CAP_SHORT='PhET&rsquo;s hinged guides (orange) against the true rim rays (green): a fixed '
+'rotation where a thin optic changes a slope. The miss is O(e&sup2;).';

const GUIDE_NOTE='Both panels use the lens on the bench. Shrinking D alone does NOT fix it: the miss '
+'sticks near 4.5 %, because the surviving error is the u&sup2; of the ray&rsquo;s own inclination.';
function guidesGeo(ctx,W,H,M){
  const live='Here the guides cross '+sigf(M.miss,3)+' cm from the image ('+fmt(M.missPct,2)
    +' %), while the same pair bent by u&prime; = u &minus; h/f misses by '+M.slopeMiss.toExponential(1)+' cm.';
  const L=layout(ctx,W,H,GUIDE_CAP_FULL+' '+live+' '+GUIDE_NOTE,
                 GUIDE_CAP_SHORT+' '+live+' '+GUIDE_NOTE,1,0.40,1);
  LAST_L=L;
  const xs=[M.P[0],0,Math.abs(M.f),-Math.abs(M.f)];
  if(isFinite(M.img.x)&&Math.abs(M.img.x)<600) xs.push(M.img.x*1.08);
  if(isFinite(M.cross.x)&&Math.abs(M.cross.x)<600) xs.push(M.cross.x);
  const ys=[M.P[1],-M.P[1],M.D/2,-M.D/2,30,-30];
  if(isFinite(M.img.y)&&Math.abs(M.img.y)<300) ys.push(M.img.y,-M.img.y);
  const ext={xmin:Math.min.apply(null,xs)-20,xmax:Math.max.apply(null,xs)+20,
             ymin:Math.min.apply(null,ys)-10,ymax:Math.max.apply(null,ys)+10};
  return {L:L,map:worldFitUp(L.main,ext,6),ext:ext};
}
function drawGuides(ctx,W,H,M,st){
  const G=guidesGeo(ctx,W,H,M), L=G.L, map=G.map, b2=L.bottom[0], ext=G.ext;
  seg(ctx,map,[ext.xmin,0],[ext.xmax,0],rgba(COL.axis,0.95),1.2,[6,5]);
  const op=opticOf(st,'lens');
  drawOptic(ctx,map,op);
  const reach=2*(ext.xmax-ext.xmin);
  /* PhET's guides go down FIRST: their incident arms lie exactly on the true
     rays by construction, so whichever is painted last is the only one seen
     (Known-bad: the last fan drawn is the only one you see). */
  [M.top,M.bot].forEach(a=>{
    const arm=Math.min(Math.abs(M.P[0]),260)*0.5;
    segW(ctx,map,a.fulcrum,[a.fulcrum[0]+arm*Math.cos(a.incident),a.fulcrum[1]+arm*Math.sin(a.incident)],
        ext,rgba(COL.guide,0.85),3);
    segW(ctx,map,a.fulcrum,[a.fulcrum[0]+reach*Math.cos(a.transmitted),a.fulcrum[1]+reach*Math.sin(a.transmitted)],
        ext,rgba(COL.guide,0.85),3);
    dot(ctx,map.X(a.fulcrum[0]),map.Y(a.fulcrum[1]),4,COL.guide,'#fff',1.2);
  });
  /* then the true pair of rays through the rim, by the slope law, on top */
  [1,-1].forEach(s=>{
    const h=s*M.D/2;
    const u=(h-M.P[1])/M.dO, up=bend(u,h,M.f);
    segW(ctx,map,M.P,[0,h],ext,rgba(COL.pos,0.9),1.5);
    segW(ctx,map,[0,h],[reach,h+up*reach],ext,rgba(COL.pos,0.9),1.5);
  });
  if(Math.abs(M.P[1])>1.5)
    worldPoly(ctx,map,objPolyWorld(st.objKind,M.P[0],M.P[1]),rgba(COL.obj,0.3),COL.obj,1.5);
  dot(ctx,map.X(M.P[0]),map.Y(M.P[1]),3.5,COL.obj,'#fff',1);
  if(isFinite(M.img.x)){
    markPoint(ctx,W,H,map,M.img.x,M.img.y,COL.img,'the image',-12);
  }
  if(isFinite(M.cross.x)) markPoint(ctx,W,H,map,M.cross.x,M.cross.y,COL.guide,'guides cross',14);
  lab(ctx,W,H,map.X(0)+8,map.Y(M.D/2)-10,'r = D/4f = '+fmt(M.r,4),COL.guide,SM_FONT,'left');

  /* the shrink sweep, log-log */
  const xs=M.es.map(e=>Math.log10(e)), ys=M.ms.map(v=>Math.log10(Math.max(v,1e-9)));
  const ylo=Math.min.apply(null,ys)-0.3, yhi=Math.max.apply(null,ys)+0.3;
  axesR(ctx,b2,-2,0,ylo,yhi,{xlab:'shrink factor e  (lens D and object height both x e)',
    title:'the miss, cm, falls as e&sup2;',
    nx:5,ny:5,xfmt:t=>sigf(Math.pow(10,t),1),yfmt:t=>sigf(Math.pow(10,t),2)});
  polyline(ctx,b2,xs,ys,-2,0,ylo,yhi,COL.guide,2);
  /* the e^2 reference through the right-hand end */
  const k=ys[ys.length-1]-2*xs[xs.length-1];
  polyline(ctx,b2,[-2,0],[2*(-2)+k,k],-2,0,ylo,yhi,rgba(COL.ref,0.8),1.4,[5,4]);
  /* the curve runs bottom-left to top-right, so the top LEFT is the corner it
     never enters -- the first two placements both grazed it */
  lab(ctx,W,H,b2.x+10,b2.y+14,'dashed: a pure e&sup2; through the right-hand end',COL.ref,SM_FONT,'left');
  drawCaption(ctx,L);
  legendSafe(ctx,L.main,[[COL.pos,'the true rim rays'],[COL.guide,'PhET&rsquo;s guides'],
    [COL.img,'the image']]);
}

/* ----------------------------------------------------------- the real lens */
const REAL_CAP_FULL=
 'The same glass, taken at face value. Two spheres of the radius the lens maker&rsquo;s equation named, '
+'the index it named, the diameter PhET&rsquo;s slider sets &mdash; and exact vector Snell at each '
+'surface instead of u&prime; = u &minus; h/f. The focus then depends on where the ray struck the lens: '
+'it walks in as the square of the ray height, which is the third-order term the paraxial model drops. '
+'Stop the lens down and the two models converge; open it up and they do not.';
const REAL_CAP_SHORT='Exact Snell at two spheres: the focus walks in as h&sup2;. Stop it down and the paraxial model returns.';

function realGeo(ctx,W,H,M){
  /* the optic axis is z (horizontal on screen), the ray height is y (vertical);
     the world map wants x across, so z maps to world-x and y to world-y */
  if(!M.exists){
    const note='No lens: a sphere of radius '+sigf(M.R,4)+' cm cannot carry a semi-aperture of '
      +sigf(M.a,4)+' cm, so there is nothing to trace.';
    const L0=layout(ctx,W,H,REAL_CAP_FULL+' '+note,REAL_CAP_SHORT+' '+note,1,0.40,1);
    LAST_L=L0;
    return {L:L0,map:null};
  }
  const e2={xmin:-1.6*M.R,xmax:M.zEnd+6,ymin:-M.a-6,ymax:M.a+6};
  const L1=stageLayout(ctx,W,H-HINT_H,REAL_CAP_FULL,REAL_CAP_SHORT,1,0.40,1);
  const s=worldFitUp(L1.main,e2,4).s;
  const note='Here the rim ray crosses '+sigf(M.lsaRim,4)+' cm from the paraxial focus &mdash; '
    +fmt(M.pctF,2)+' % of the focal length &mdash; where the ideal optic of the other views has none. '
    +'Equal aspect, '+sigf(s,3)+' px per cm; the drawn fan is 11 rays and the curve is 48. '
    +'A concave mirror of the same radius misses by '+sigf(M.mirrorPar-M.mirrorRim,3)
    +' cm at the same rim height. The edge thickness is chosen here, not PhET&rsquo;s.';
  const L=layout(ctx,W,H,REAL_CAP_FULL+' '+note,REAL_CAP_SHORT+' '+note,1,0.40,1);
  LAST_L=L;
  return {L:L,map:worldFitUp(L.main,e2,4),ext:e2};
}
function drawReal(ctx,W,H,M,st){
  const G=realGeo(ctx,W,H,M), L=G.L;
  if(!M.exists){
    caption(ctx,L.left,L.main.y+40,
      'A sphere of radius '+sigf(M.R,4)+' cm cannot carry a semi-aperture of '+sigf(M.a,4)
      +' cm: the two surfaces would cross before they met the rim, so there is no lens to trace. '
      +'PhET&rsquo;s artwork draws one anyway, with its softened sag. Raise the radius or close the '
      +'diameter and the trace returns.',Math.min(460,L.right-L.left),COL.live,CAP_FONT);
    drawCaption(ctx,L);
    return;
  }
  const map=G.map, ext=G.ext, b2=L.bottom[0];
  seg(ctx,map,[ext.xmin,0],[ext.xmax,0],rgba(COL.axis,0.95),1.2,[6,5]);
  /* the lens body: front surface z = sag(R,y) - ... drawn in (z, y) */
  const NS=30, front=[],back=[];
  for(let i=0;i<=NS;i++){
    const y=-M.a+2*M.a*i/NS;
    const sg=M.R-Math.sqrt(Math.max(M.R*M.R-y*y,0));
    front.push([sg,y]); back.push([M.t-sg,y]);
  }
  worldPoly(ctx,map,front.concat(back.slice().reverse()),rgba(COL.glass,0.42),COL.glass2,1.6);
  /* the traced fan */
  M.fan.forEach(r=>{
    for(let i=0;i+1<r.pts.length;i++)
      segW(ctx,map,[r.pts[i][1],r.pts[i][0]],[r.pts[i+1][1],r.pts[i+1][0]],ext,
           rgba(COL.ray,0.55+0.4*Math.abs(r.h)/M.stop),1.3);
  });
  /* the paraxial focal plane, and the marginal crossing */
  seg(ctx,map,[M.zPar,-M.a],[M.zPar,M.a],rgba(COL.ref,0.9),1.6,[6,4]);
  lab(ctx,W,H,map.X(M.zPar),map.Y(M.a)-12,'paraxial focus',COL.ref,SM_FONT,'center');
  const zM=M.zPar+M.lsaMark;
  seg(ctx,map,[zM,-M.a*0.6],[zM,M.a*0.6],rgba(COL.live,0.9),1.6,[4,4]);
  lab(ctx,W,H,map.X(zM),map.Y(-M.a*0.6)+13,'h = '+sigf(M.hMark,3)+' cm crosses here',COL.live,SM_FONT,'center');
  lab(ctx,W,H,map.X(M.t/2),map.Y(-M.a)+14,'n = '+fmt(M.n,3)+', R = &plusmn;'+sigf(M.R,4)
      +' cm, t = '+sigf(M.t,4)+' cm',COL.glass2,SM_FONT,'center');

  /* LSA against ray height */
  const hs=M.hs, ls=M.ls;
  const ylo=Math.min(0,Math.min.apply(null,ls))*1.08, yhi=Math.max(0,Math.max.apply(null,ls))*1.08+1e-6;
  axesR(ctx,b2,0,M.stop,ylo,yhi,{xlab:'ray height h, cm',ylab:'LSA, cm',
    title:'longitudinal spherical aberration',nx:6,ny:5,xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  polyline(ctx,b2,[0,M.stop],[0,0],0,M.stop,ylo,yhi,rgba(COL.axis,0.9),1);
  polyline(ctx,b2,hs,ls,0,M.stop,ylo,yhi,COL.pos,2);
  const q=[],qy=[];
  for(let i=0;i<=40;i++){ const hh=M.stop*i/40; q.push(hh); qy.push(M.c2*hh*hh); }
  polyline(ctx,b2,q,qy,0,M.stop,ylo,yhi,rgba(COL.ref,0.85),1.4,[5,4]);
  marker(ctx,b2,0,M.stop,ylo,yhi,M.hMark,M.lsaMark,COL.live);
  drawCaption(ctx,L);
  legendSafe(ctx,b2,[[COL.pos,'exact trace'],
    [COL.ref,'&minus;C h&sup2;, C at h = '+sigf(M.stop*0.02,3)+' cm'],[COL.live,'this height']]);
}

/* ================================================================== *
 *  dispatch, and the scene object                                     *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(st.view==='bench'||st.view==='mirror') drawBench(ctx,W,H,M,st);
  else if(st.view==='conj') drawConj(ctx,W,H,M,st);
  else if(st.view==='maker') drawMaker(ctx,W,H,M,st);
  else if(st.view==='guides') drawGuides(ctx,W,H,M,st);
  else drawReal(ctx,W,H,M,st);
}

function makeScene(canvas){
  const S={st:ST,W:1180,H:740};
  S.model=()=>buildModel(ST);
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel(ST),ST); };
  /* nothing animates: every view solves its problem outright */
  S.step=function(){ return false; };
  /* drag the object on the two benches and in the guides view */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const v=ST.view;
    if(v!=='bench'&&v!=='mirror'&&v!=='guides') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(ST);
    const G=(v==='guides')?guidesGeo(ctx,S.W,S.H,M):benchGeo(ctx,S.W,S.H,M);
    const map=G.map;
    if(!map) return false;
    if(type==='down'){
      const P=objectPoint(ST);
      if(Math.hypot(x-map.X(P[0]),y-map.Y(P[1]))<22){
        DRAG.what='obj'; DRAG.off=[P[0]-map.wx(x),P[1]-map.wy(y)]; return true;
      }
      return false;
    }
    if(type==='move'&&DRAG.what==='obj'){
      ST.objX=clamp(map.wx(x)+DRAG.off[0],-460,-PHET.minObjectDist);
      ST.objY=clamp(map.wy(y)+DRAG.off[1],-PHET.maxOffAxis,PHET.maxOffAxis);
      clearMemo();
      return true;
    }
    return false;
  };
  return S;
}
