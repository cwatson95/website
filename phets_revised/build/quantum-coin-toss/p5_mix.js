
/* ================================================================== *
 *  THE HIDDEN DIFFERENCE view: a hidden face against a superposition, *
 *  face-on and sideways                                               *
 * ================================================================== */
/* the two coins at bias p, as Bloch vectors: the hidden classical face is a
   MIXTURE (0, 0, 2p-1), inside the ball; the quantum coin is the pure state
   sqrt(p)|up> + sqrt(1-p)|down>, on the sphere at (2 sqrt(p(1-p)), 0, 2p-1) */
function mixBloch(p){ return [0,0,2*p-1]; }
function pureBloch(p){ return [2*Math.sqrt(p*(1-p)),0,2*p-1]; }
function mixPx(p){ return bornP(mixBloch(p),[1,0,0]); }        /* 1/2, whatever p */
function purePx(p){ return bornP(pureBloch(p),[1,0,0]); }      /* (1 + 2 sqrt(p(1-p)))/2 */
function mixPurity(p){ return p*p+(1-p)*(1-p); }
/* seeded runs through the engine's own draws: n classical faces (u < p, as a
   coin set draws), n hidden faces turned sideways (the face, then a Born draw
   along x), n quantum coins face-on and n sideways (measureAlong) */
function mixRun(seed,p,n){
  const R=rngMake(seed), rq=pureBloch(p); let cz=0,cx=0,qz=0,qx=0;
  for(let i=0;i<n;i++) if(rngNext(R)<p) cz++;
  for(let i=0;i<n;i++){ const face=rngNext(R)<p; if(measureAlong(R,face?[0,0,1]:[0,0,-1],[1,0,0]).up) cx++; }
  for(let i=0;i<n;i++) if(measureAlong(R,rq,[0,0,1]).up) qz++;
  for(let i=0;i<n;i++) if(measureAlong(R,rq,[1,0,0]).up) qx++;
  return {cz,cx,qz,qx,n};
}
function mixModel(st){
  const p=st.mixP, n=st.mixShots, seed=st.mixSeed;
  const run=memo('mixRun',[p,n,seed].join(':'),()=>mixRun(seed,p,n));
  const sd=q=>Math.sqrt(q*(1-q)/n);
  return {p,n,seed,run, pz:p, pxC:mixPx(p), pxQ:purePx(p), coh:Math.sqrt(p*(1-p)), purC:mixPurity(p),
          f:{cz:run.cz/n,cx:run.cx/n,qz:run.qz/n,qx:run.qx/n}, sd:{z:sd(p),xc:sd(mixPx(p)),xq:sd(purePx(p))}};
}
function mixGeo(ctx,W,H,Cap){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?48:66;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(140,Math.min(narrow?220:330,avail*0.56));
  const wA=narrow?(rightTop-left)*0.58:Math.min(520,(rightTop-left)*0.56);
  const A=box(left,top+12,wA,upH-40);
  const discR=Math.max(30,Math.min((upH-80)/2,(rightTop-A.x1-90)/2.4));
  const disc={cx:A.x1+60+discR*1.2,cy:A.y+(upH-40)/2,r:discR};
  const lowTop=top+upH+30, C=box(left,lowTop,Math.min(narrow?W-18-left:720,(narrow?W-18:W-26)-left),fit.capY-16-lowTop-26);
  return {narrow,top,left,fit,A,disc,C};
}
/* below: whether the P(+x)-against-p panel is drawn (the caption names it only then) */
function mixCaption(M,below){
  const m=M.X;
  return {full:'Left: '+m.n+' seeded coins of each kind at p = '+fmt(m.p,2)+', measured face-on (up or down) and sideways (along x). Face-on the two coins are indistinguishable: P(up) = p for both. Sideways, a hidden face is a coin already up or down, and gives ½; the superposition gives (1 + 2√(p(1−p)))/2. Right: the two states on the Bloch disc — the mixture inside, the superposition on the edge.'+(below!==false?' Below: P(+x) against p.':''),
          short:'Face-on the coins agree; sideways the hidden face gives ½ and the superposition (1 + 2√(p(1−p)))/2.'};
}
/* the caption and the geometry together: the lower panel is optional */
function mixLayout(ctx,W,H,M){ return layoutNamed(b=>mixCaption(M,b),Cap=>mixGeo(ctx,W,H,Cap),G=>G.C.h>=55); }
function drawMix(ctx,W,H,M){
  const m=M.X, LY=mixLayout(ctx,W,H,M), Cap=LY.Cap, G=LY.G, A=G.A, C=G.C, D=G.disc;
  /* the four measurements against their laws */
  axesT(ctx,A,0,5,0,1.1,{xticks:[],yticks:[0,0.25,0.5,0.75,1],title:fitTitle(A,'face-on and sideways: measured (green) against the law (orange)','face-on and sideways')});
  const bars=[[0.7,m.f.cz,m.pz,m.sd.z,'classical'],[1.7,m.f.qz,m.pz,m.sd.z,'quantum'],[3.3,m.f.cx,m.pxC,m.sd.xc,'classical'],[4.3,m.f.qx,m.pxQ,m.sd.xq,'quantum']];
  const bw=Math.min(46,A.w*0.12);
  for(const [x,f,law,s,labt] of bars){
    const X=px(A,x,0,5), Y=py(A,f,0,1.1);
    ctx.fillStyle=shade(COL.pos,0.85); ctx.fillRect(X-bw/2,Y,bw,A.y1-Y);
    ctx.beginPath(); ctx.moveTo(X-bw/2-6,py(A,law,0,1.1)); ctx.lineTo(X+bw/2+6,py(A,law,0,1.1)); ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
    errBar(ctx,A,x,f,s,0,5,0,1.1,'#e9f5c8');
    lab(ctx,W,H,X,A.y1+10,labt,COL.text,SM_FONT,'center','middle');
  }
  lab(ctx,W,H,px(A,1.2,0,5),A.y1+26,'face-on: P(up)',COL.dim,SM_FONT,'center','middle');
  lab(ctx,W,H,px(A,3.8,0,5),A.y1+26,'sideways: P(+x)',COL.dim,SM_FONT,'center','middle');
  /* the Bloch disc (the x-z plane of the ball) */
  ctx.beginPath(); ctx.arc(D.cx,D.cy,D.r,0,TAU); ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(D.cx-D.r-8,D.cy); ctx.lineTo(D.cx+D.r+8,D.cy); ctx.moveTo(D.cx,D.cy-D.r-8); ctx.lineTo(D.cx,D.cy+D.r+8);
  ctx.setLineDash([4,3]); ctx.strokeStyle='#3d465e'; ctx.lineWidth=1; ctx.stroke(); ctx.setLineDash([]);
  lab(ctx,W,H,D.cx+6,D.cy-D.r-10,'z: face-on',COL.dim,SM_FONT,'left','middle');
  lab(ctx,W,H,D.cx+D.r+10,D.cy,'x: sideways',COL.dim,SM_FONT,'left','middle');
  const rp=pureBloch(m.p), rc=mixBloch(m.p);
  const Xp=D.cx+rp[0]*D.r, Yp=D.cy-rp[2]*D.r, Xc=D.cx+rc[0]*D.r, Yc=D.cy-rc[2]*D.r;
  ctx.beginPath(); ctx.moveTo(D.cx,D.cy); ctx.lineTo(Xp,Yp); ctx.strokeStyle=COL.pos; ctx.lineWidth=2.6; ctx.stroke(); mark(ctx,Xp,Yp,'o',COL.pos,4.2);
  ctx.beginPath(); ctx.moveTo(Xp,Yp); ctx.lineTo(Xp,D.cy); ctx.setLineDash([3,3]); ctx.strokeStyle=COL.pos; ctx.lineWidth=1; ctx.stroke(); ctx.setLineDash([]);
  mark(ctx,Xc,Yc,'d',COL.neg,5);
  lab(ctx,W,H,Xp+8,Yp-6,'quantum: pure',COL.pos,SM_FONT,'left','middle');
  /* lifted off its own height: the mixture sits ON the z axis (r = (0,0,2p-1)),
     so at p = 1/2 it is at the centre and the label sat on the x axis (looked at) */
  lab(ctx,W,H,Xc-8,Yc-10,'classical: mixed',COL.neg,SM_FONT,'right','middle');
  lab(ctx,W,H,D.cx,D.cy+D.r+18,'the Bloch disc (x–z)',COL.text,'italic 12.5px Georgia, serif','center','middle');
  /* P(+x) against p */
  if(!G.panelOff&&C.h>=55){
    axesT(ctx,C,0,1,0,1.1,{xticks:[0,0.25,0.5,0.75,1],yticks:C.h<100?[0,0.5,1]:[0,0.25,0.5,0.75,1],xlab:C.h>=95?'the bias p = P(up)':'',
      xfmt:v=>v===0?'0':fmt(v,2),yfmt:v=>v===0?'0':fmt(v,2),          /* a bare 0 keeps the corner ticks apart */
      title:fitTitle(C,'sideways: P(+x) = ½ for a hidden face, (1 + 2√(p(1−p)))/2 for the superposition','P(+x) against the bias')});
    const xs=[], yq=[], yc=[]; for(let i=0;i<=200;i++){ const p=i/200; xs.push(p); yq.push(purePx(p)); yc.push(mixPx(p)); }
    polyline(ctx,C,xs,yq,0,1,0,1.1,COL.ref,2.2); polyline(ctx,C,xs,yc,0,1,0,1.1,COL.ref,1.5,[6,4]);
    vCursor(ctx,C,m.p,0,1);
    errBar(ctx,C,m.p,m.f.qx,m.sd.xq,0,1,0,1.1,COL.pos); mark(ctx,px(C,m.p,0,1),py(C,m.f.qx,0,1.1),'o',COL.pos,4.2);
    errBar(ctx,C,m.p,m.f.cx,m.sd.xc,0,1,0,1.1,COL.neg); mark(ctx,px(C,m.p,0,1),py(C,m.f.cx,0,1.1),'d',COL.neg,4.2);
    legendAuto(ctx,C,[[COL.ref,'superposition (solid)'],[mix(COL.bg,COL.ref,0.75),'hidden face (dashed)'],[COL.pos,'quantum, seeded'],[COL.neg,'classical, seeded (diamond)']]);
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function mixReadout(M){
  const m=M.X, f=m.f;
  return hd('at p = '+fmt(m.p,2))
    +rrow('&rho; hidden face',"diag("+fmt(m.p,3)+', '+fmt(1-m.p,3)+')')
    +rrow('&rho; superposition, off-diagonal',fmt(m.coh,4),'good')
    +rrow('purity Tr&rho;&sup2;: hidden, superposition',fmt(m.purC,3)+', 1')
    +hd('face-on: P(up)')+rrow('both, exactly',fmt(m.pz,4))+rrow('measured: hidden, superposition',fmt(f.cz,3)+', '+fmt(f.qz,3))
    +hd('sideways: P(+x)')+rrow('hidden face: &frac12;',fmt(m.pxC,4))+rrow('superposition: (1 + 2&radic;(p(1&minus;p)))/2',fmt(m.pxQ,4),'good')
    +rrow('measured: hidden, superposition',fmt(f.cx,3)+', '+fmt(f.qx,3))+rrow('shots of each, seed',m.n+', '+m.seed);
}
function mixEq(M){ return ['<span class="hl">&rho;<sub>hidden</sub> = diag(p, 1&minus;p)</span>, &nbsp; &rho;<sub>quantum</sub> = |&psi;&rang;&lang;&psi;| <span class="rm">with off-diagonal</span> &radic;(p(1&minus;p)) &nbsp;&middot;&nbsp; P(+x) = &frac12; <span class="rm">against</span> (1 + 2&radic;(p(1&minus;p)))/2',
  'the same odds face-on; only a measurement along another axis sees the coherence that makes the coin quantum']; }
function mixTag(M){ return '<b>the hidden difference</b> — p = '+fmt(M.X.p,2)+', '+M.X.n+' coins of each kind'; }
const INFO_MIX='Face-on, the two coins cannot be told apart. A classical coin that was flipped and hidden comes up heads with probability p. '
  +'A quantum coin prepared as &radic;p|&uarr;&rang; + &radic;(1&minus;p)|&darr;&rang; comes up with probability p. No number of face-on '
  +'measurements will ever separate them. The difference is in the density matrix. The hidden face is a mixture, diag(p, 1&minus;p): the coin '
  +'is up or it is down and you do not know which. The quantum coin has off-diagonal terms &radic;(p(1&minus;p)) as well. Those terms '
  +'are invisible face-on and decisive sideways. Measure along x and a hidden face, being already up or down, splits evenly: &frac12;, '
  +'whatever p is. The superposition goes +x with probability (1 + 2&radic;(p(1&minus;p)))/2, which reaches 1 at p = &frac12;. On the Bloch '
  +'disc the mixture sits inside the ball, on the axis; the superposition sits on the edge, tilted toward x by exactly that coherence.';
const DERIV_MIX='<h4>a mixture against a superposition</h4>'
  +EQ(1,'&rho;<sub>hidden</sub> = p|&uarr;&rang;&lang;&uarr;| + (1&minus;p)|&darr;&rang;&lang;&darr;|, &nbsp; r = (0, 0, 2p&minus;1)')
  +EQ(2,'&rho;<sub>quantum</sub> = |&psi;&rang;&lang;&psi;|, &nbsp; |&psi;&rang; = &radic;p|&uarr;&rang; + &radic;(1&minus;p)|&darr;&rang;, &nbsp; r = (2&radic;(p(1&minus;p)), 0, 2p&minus;1)')
  +EQ(3,'P(&uarr;) = &frac12;(1 + r<sub>z</sub>) = p <span class="rm">for both;</span> &nbsp; P(+x) = &frac12;(1 + r<sub>x</sub>)')
  +EQ(4,'Tr&rho;&sup2; = p&sup2; + (1&minus;p)&sup2; <span class="rm">(mixture)</span> <span class="rm">against</span> 1 <span class="rm">(pure)</span>')
  +'<p>The seeded runs go through the engine&rsquo;s own draws: the hidden face is drawn as a coin draws it, u &lt; p, and then '
  +'measured along x from &plusmn;z; the superposition is measured with measureAlong. derive.py builds both density matrices in numpy '
  +'and takes Tr(&rho;P<sub>+x</sub>) independently.</p>'
  +'<div class="cite">pins: P(z), P(+x), purity and the coherence at seven biases (numpy); four seeded runs, e.g. p = 0.7, 1000 of each: '
  +'[674, 507, 721, 961]; at p = &frac12; the superposition goes +x 2000 times in 2000 &mdash; derive.py</div>';
