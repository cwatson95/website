
/* ================================================================== *
 *  views: real molecules, the vector sum, the field, the atlas        *
 * ================================================================== */

/* ---------------------------------------------------------------- *
 *  view: real molecules (PhET's third screen)                        *
 * ---------------------------------------------------------------- */
const REAL_CAP='PhET&rsquo;s Real Molecules screen. The geometry is PhET&rsquo;s own table &mdash; PubChem coordinates in angstrom, drawn to scale '
  +'with PhET&rsquo;s display radii (a quarter of the van der Waals radius). Basic makes each bond dipole |&Delta;EN| with Pauling electronegativities; '
  +'Advanced makes it |q&#8321;&minus;q&#8322;|/2 &times; d / 0.208194 debye from the Hirshfeld charges, and scales the arrows so the molecular one carries the '
  +'Psi4 magnitude. Drag to turn, wheel to zoom. PhET&rsquo;s per-vertex surface mesh is not carried here.';
const REAL_CAP_S='PhET&rsquo;s real molecules, its own geometry and charges: Basic from &Delta;EN, Advanced from Hirshfeld charges in debye. Drag to turn.';
function realGeo(ctx,W,H){
  const L=stageMol(ctx,W,H,REAL_CAP,REAL_CAP_S,250);
  const r=realMol(ST.mol);
  /* PhET's origin is its central atom, which is where the dipoles are drawn
     from; the CAMERA aims at the centroid so an off-centre molecule (HCN,
     formaldehyde) is not pushed against one wall */
  const want=0.94*ST.zoom*Math.min(L.b.w,L.b.h)/2;
  const f=(L.b.h/2)/Math.tan(0.78/2);
  const R=Math.max(0.8,r.extentC*1.04);
  const dist=R*Math.sqrt(1+(f/want)*(f/want));
  const C=boxCamera(L.b,ST.camTheta,ST.camPhi,dist,r.centroid);
  return {L,C,r,dist};
}
function drawReal(ctx,W,H,M){
  const G=realGeo(ctx,W,H), C=G.C, r=G.r, b=G.L.b, d=M.d;
  frame(ctx,b,COL.edge);
  const pa=r.pos.map(p=>C.P(p));
  let z0=Infinity,z1=-Infinity; for(const q of pa) if(q){ z0=Math.min(z0,q.z); z1=Math.max(z1,q.z); }
  const cue=z=>z1>z0?0.62+0.38*clamp((z1-z)/(z1-z0),0,1):1;
  const f=C.B.f;
  const items=[];
  pa.forEach((q,i)=>{ if(q) items.push({z:q.z,kind:0,i}); });
  r.bonds.forEach((bd,k)=>{ const A=pa[bd[0]], B=pa[bd[1]]; if(!A||!B) return;
    items.push({z:(3*A.z+B.z)/4,kind:1,from:bd[0],to:bd[1],k});
    items.push({z:(3*B.z+A.z)/4,kind:1,from:bd[1],to:bd[0],k}); });
  items.sort((a,b2)=>b2.z-a.z);
  const rad=pa.map((q,i)=>q?Math.max(1.5,f*r.radii[i]/q.z):0);
  for(const it of items){
    if(it.kind===0){ const q=pa[it.i];
      ball(ctx,q.x,q.y,rad[it.i],ELCOL[r.syms[it.i]]||'#aab2c0',cue(q.z));
    } else {
      const A=pa[it.from], B=pa[it.to], mx=(A.x+B.x)/2, my=(A.y+B.y)/2, c=cue(A.z);
      const order=r.bonds[it.k][2];
      const lo=pa[Math.min(r.bonds[it.k][0],r.bonds[it.k][1])], hi=pa[Math.max(r.bonds[it.k][0],r.bonds[it.k][1])];
      const Lp=Math.hypot(hi.x-lo.x,hi.y-lo.y)||1, nx=-(hi.y-lo.y)/Lp, ny=(hi.x-lo.x)/Lp, s=f/A.z;
      const k2=Math.round(order), w=k2>=3?0.035*s:k2===2?0.045*s:0.075*s, gap=k2===2?0.09*s:0.11*s;
      const offs=k2<=1?[0]:k2===2?[-gap,gap]:[-gap,0,gap];
      for(const o of offs){
        line2(ctx,A.x+nx*o,A.y+ny*o,mx+nx*o,my+ny*o,shade(COL.bond,0.72*c),Math.max(1.2,w));
        line2(ctx,A.x+nx*o,A.y+ny*o,mx+nx*o,my+ny*o,shade('#e4e8f0',0.55*c),Math.max(0.6,0.35*w));
      }
    }
  }
  /* labels and charges on the atoms.  The central atom's charge label is pushed
     ACROSS the molecular dipole, which is drawn through it. */
  let across=null;
  { const sm=d.sum, mg=v3len(sm);
    if(mg>1e-5){ const u=v3scale(sm,1/mg);
      const q0=C.P(v3scale(u,-0.3)), q1=C.P(v3scale(u,0.3));
      if(q0&&q1){ const dx=q1.x-q0.x, dy=q1.y-q0.y, n2=Math.hypot(dx,dy)||1; across=[-dy/n2,dx/n2]; } } }
  if(ST.showLabels||ST.showCharges){
    const idx=pa.map((q,i)=>({q,i})).filter(o=>o.q).sort((a,b2)=>a.q.z-b2.q.z);
    for(const o of idx){
      const q=o.q, i=o.i;
      if(ST.showLabels) lab(ctx,W,H,q.x,q.y,r.syms[i],'#12151d',
        'italic '+Math.max(9,Math.min(18,rad[i]*0.95)).toFixed(0)+'px Georgia, serif','center','middle');
      if(ST.showCharges&&ST.realMode==='advanced'){
        const cq=C.P(r.centroid);
        let ox=cq?q.x-cq.x:0, oy=cq?q.y-cq.y:1, nn=Math.hypot(ox,oy);
        if(nn<1e-6){ ox=0; oy=1; nn=1; }
        if(i===r.centre&&across){ ox=across[0]; oy=across[1]; nn=1; }
        lab(ctx,W,H,q.x+ox/nn*(rad[i]+13),q.y+oy/nn*(rad[i]+13),
          (r.q[i]>0?'&delta;+':'&delta;&minus;')+' '+fmt(Math.abs(r.q[i]),3),
          r.q[i]<0?COL.struct:COL.ref,SMALL_FONT,'center','middle');
      }
    }
  }
  /* the bond dipoles and the molecular dipole, in 3-D */
  if(ST.showBondDipole){
    r.bonds.forEach((bd,k)=>{
      const v=d.bd[k], mag=v3len(v); if(mag<1e-6) return;
      const mid=v3scale(v3plus(r.pos[bd[0]],r.pos[bd[1]]),0.5);
      const u=v3scale(v,1/mag), L2=mag*d.scale;      /* PhET's own arrow scale */
      const p0=C.P(v3plus(mid,v3scale(u,-L2/2))), p1=C.P(v3plus(mid,v3scale(u,L2/2)));
      if(!p0||!p1) return;
      const ang=Math.atan2(p1.y-p0.y,p1.x-p0.x), len=Math.hypot(p1.x-p0.x,p1.y-p0.y);
      dipoleArrow(ctx,p0.x,p0.y,ang,len,COL.pos,2.6);
    });
  }
  if(ST.showMolDipole){
    const s=d.sum, mag=v3len(s);
    if(mag>1e-5){
      /* PhET scales the arrows so the molecular one carries the Psi4 magnitude:
         sum * scale = psi4mag * 0.75 in advanced, sum * 0.75 in basic */
      const u=v3scale(s,1/mag), L2=(ST.realMode==='advanced'?r.psi4mag:mag)*0.75;
      const p0=C.P(v3scale(u,-L2/2)), p1=C.P(v3scale(u,L2/2));
      if(p0&&p1){
        const ang=Math.atan2(p1.y-p0.y,p1.x-p0.x), len=Math.hypot(p1.x-p0.x,p1.y-p0.y);
        dipoleArrow(ctx,p0.x,p0.y,ang,len,COL.live,3.6);
        lab(ctx,W,H,b.x+b.w/2,b.y+12,'molecular dipole '+fmt(ST.realMode==='advanced'?r.psi4mag:mag,3)
          +(ST.realMode==='advanced'?' D':''),COL.live,SMALL_FONT,'center','top');
      }
    } else lab(ctx,W,H,b.x+b.w/2,b.y+18,'molecular dipole = 0: the bond dipoles cancel by symmetry',COL.live,SMALL_FONT,'center','top');
  }
  lab(ctx,W,H,b.x+12,b.y+12,formulaOnCanvas(r.sym)+'  '+r.name,COL.text,TITLE_FONT,'left','top');
  lab(ctx,W,H,b.x+12,b.y+30,ST.realMode==='advanced'?'advanced: Hirshfeld charges, debye':'basic: |&Delta;EN|, no unit',
    COL.dim,SMALL_FONT,'left','top');
  if(M.meas) lab(ctx,W,H,b.x1-12,b.y+12,'measured '+fmt(M.meas[0],3)+' D (CCCBDB)',COL.ref,SMALL_FONT,'right','top');
  else lab(ctx,W,H,b.x1-12,b.y+12,'no measured value in CCCBDB',COL.ref,SMALL_FONT,'right','top');
  lab(ctx,W,H,b.x1-12,b.y+28,'drawn to scale in angstrom; radii are PhET&rsquo;s (vdW/4)',COL.dim,SMALL_FONT,'right','top');
  drawCap(ctx,G.L);
}
/* subscripts on the canvas: digits only (letter subscripts are not safe here) */
function formulaOnCanvas(s){
  const SUB='₀₁₂₃₄₅₆₇₈₉';
  return s.replace(/(\d)/g,d=>SUB[+d]);
}

/* ---------------------------------------------------------------- *
 *  view: the vector sum                                              *
 * ---------------------------------------------------------------- */
const SUM_CAP='The whole of molecular polarity in one plot: the molecular dipole is a sum of two vectors, so its length depends on the angle between them. '
  +'Top, |&mu;| against the bond angle for the electronegativities you set, with the symmetric family behind it. Bottom left, the same sum drawn head to tail. '
  +'Bottom right, the two ends of the curve. Only a symmetric molecule reaches zero, and at 180&deg; it reaches it exactly &mdash; that is CO&#8322;.';
const SUM_CAP_S='|&mu;| against the bond angle: the sum of two vectors, its head-to-tail construction, and the exact cancellation at 180&deg;.';
function sumGeo(ctx,W,H){ return stageLayout(ctx,W,H-HINT_H,SUM_CAP,SUM_CAP_S,2,0.40,2); }
function drawSum(ctx,W,H,M){
  const L=sumGeo(ctx,W,H), b=L.main;
  const ymax=Math.max(0.25,1.06*Math.max(M.atMax,Math.max.apply(null,M.family.map(f=>2*f.d))));
  axesR(ctx,b,0,180,0,ymax,{xlab:'bond angle &theta; (degrees)',ylab:'|&mu;|',
    title:titleFor(b,'the molecular dipole against the bond angle','|&mu;| against &theta;'),
    xticks:[0,30,60,90,120,150,180]});
  for(const f of M.family)
    polyline(ctx,b,f.c.xs,f.c.ys,0,180,0,ymax,rgba(COL.ref,0.38),1.2,[4,4]);
  polyline(ctx,b,M.curve.xs,M.curve.ys,0,180,0,ymax,COL.pos,2.2);
  marker(ctx,b,0,180,0,ymax,M.bondAngleDeg,M.here,COL.live);
  /* the exact zero, when there is one */
  if(M.symmetric){
    const X=b.x+b.w, Y=b.y1;
    dot(ctx,X,Y,4.5,COL.live,'#fff');
    lab(ctx,W,H,X-8,Y-22,'exactly 0 at 180&deg;',COL.live,SMALL_FONT,'right','bottom');
  }
  lab(ctx,W,H,b.x+10,b.y1-26,'&Delta;AB = '+sgn(M.m.dAB,2)+', &Delta;BC = '+sgn(M.m.dBC,2),COL.pos,SMALL_FONT,'left','bottom');
  lab(ctx,W,H,b.x+10,b.y1-12,'dashed: the symmetric family &Delta; = 0.5, 1, 1.5, 2',rgba(COL.ref,0.8),SMALL_FONT,'left','bottom');

  /* bottom left: the head-to-tail construction */
  const p=L.bottom[0];
  if(p){
    frame(ctx,p,COL.edge);
    lab(ctx,W,H,p.x+p.w/2,p.y-9,'head to tail',COL.text,TITLE_FONT,'center','bottom');
    const m=M.m, span=Math.max(1e-9,Math.max(vmag(m.muAB)+vmag(m.muBC),m.mumag));
    const s=0.78*Math.min(p.w,p.h)/span;
    const cx=p.x+p.w/2-s*(m.mu[0])/2, cy=p.y+p.h/2-s*(m.mu[1])/2;
    const P1=[cx+s*m.muAB[0],cy+s*m.muAB[1]], P2=[cx+s*m.mu[0],cy+s*m.mu[1]];
    if(vmag(m.muAB)>1e-9) dipoleArrow(ctx,cx,cy,vang(m.muAB),s*vmag(m.muAB),COL.pos,2.6,false);
    if(vmag(m.muBC)>1e-9) dipoleArrow(ctx,P1[0],P1[1],vang(m.muBC),s*vmag(m.muBC),COL.pos,2.6,false);
    if(m.mumag>1e-9) dipoleArrow(ctx,cx,cy,vang(m.mu),s*m.mumag,COL.live,3.2,false);
    else { dot(ctx,cx,cy,4,COL.live,'#fff'); lab(ctx,W,H,cx,cy-12,'they cancel',COL.live,SMALL_FONT,'center','bottom'); }
    lab(ctx,W,H,p.x+8,p.y1-8,'green: bond dipoles &middot; magenta: their sum',COL.dim,SMALL_FONT,'left','bottom');
  }
  /* bottom right: the two ends */
  const q=L.bottom[1]||L.bottom[0];
  if(q&&L.bottom.length>1){
    frame(ctx,q,COL.edge);
    lab(ctx,W,H,q.x+q.w/2,q.y-9,'the two ends of the curve',COL.text,TITLE_FONT,'center','bottom');
    const rows=[['&theta; = 0&deg;','|&Delta;AB &minus; &Delta;BC| = '+sgn(M.atMax,4),COL.ref],
                ['&theta; = 180&deg;','|&Delta;AB + &Delta;BC| = '+sgn(M.atMin,4),M.symmetric?COL.pos:COL.ref],
                ['here, &theta; = '+fmt(M.bondAngleDeg,1)+'&deg;',sgn(M.here,4),COL.live],
                ['symmetric?',M.symmetric?'yes: zero at 180&deg;':'no: the minimum is '+fmt(M.atMin,3),M.symmetric?COL.pos:COL.dim]];
    rows.forEach((rw,i)=>{
      const y=q.y+22+i*Math.min(26,(q.h-30)/rows.length);
      lab(ctx,W,H,q.x+12,y,rw[0],COL.dim,SMALL_FONT,'left','middle');
      lab(ctx,W,H,q.x1-12,y,rw[1],rw[2],SMALL_FONT,'right','middle');
    });
  }
  drawCaption(ctx,L);
}

/* ---------------------------------------------------------------- *
 *  view: the field                                                   *
 * ---------------------------------------------------------------- */
const FIELD_CAP='What the field really does. A dipole &mu; in a field E feels a torque &minus;&mu;E sin&psi;, so the molecule is a pendulum about alignment: '
  +'under-damped it overshoots, critically damped it arrives fastest without crossing, over-damped it creeps. The energy &frac12;I(d&psi;/dt)&sup2; + &mu;E(1 &minus; cos&psi;) '
  +'can only fall, so &psi; = 0 is reached from every start but the unstable point itself. Orange is PhET&rsquo;s own rule: a fixed 0.085|&mu;| radians every frame, '
  +'a straight line that stops dead. Drag the top panel to set the starting angle.';
const FIELD_CAP_S='A dipole in a field is a damped pendulum. Green: the rotor at three dampings. Orange: PhET&rsquo;s constant-speed rule. Drag to set the start.';
function fieldGeo(ctx,W,H){ return stageLayout(ctx,W,H-HINT_H,FIELD_CAP,FIELD_CAP_S,1,0.44,1); }
function drawField(ctx,W,H,M){
  const L=fieldGeo(ctx,W,H), b=L.main;
  const T=FV.T;
  axesR(ctx,b,0,T,-185,185,{xlab:'time (arbitrary units)',ylab:'dipole angle &psi; (degrees)',
    title:titleFor(b,'the molecule turning until its dipole lines up','&psi; against time'),
    yticks:[-180,-90,0,90,180]});
  polyline(ctx,b,[0,T],[0,0],0,T,-185,185,rgba(COL.struct,0.5),1,[5,5]);
  if(M.muE>1e-9){
    const styles=[['z0.2',rgba(COL.pos,0.42),1.4],['z1',rgba(COL.pos,0.42),1.4],['z2',rgba(COL.pos,0.42),1.4]];
    for(const [k,c,w] of styles){ const tr=M.traces[k]; polyline(ctx,b,tr.xs,tr.ys,0,T,-185,185,c,w,[4,4]); }
    polyline(ctx,b,M.traces.live.xs,M.traces.live.ys,0,T,-185,185,COL.pos,2.2);
    for(const [k,lb] of [['z0.2','&zeta; = 0.2'],['z1','&zeta; = 1'],['z2','&zeta; = 2']]){
      const tr=M.traces[k], i=Math.round(tr.xs.length*0.20);
      const X=b.x+b.w*tr.xs[i]/T, Y=b.y1-b.h*(tr.ys[i]+185)/370;
      lab(ctx,W,H,X,Y-8,lb,rgba(COL.pos,0.75),SMALL_FONT,'center','bottom');
    }
  }
  if(M.mu>1e-9) polyline(ctx,b,M.traces.phet.xs,M.traces.phet.ys,0,T,-185,185,COL.ref,2);
  marker(ctx,b,0,T,-185,185,0,M.psi0*180/PI,COL.live);
  lab(ctx,W,H,b.x+10,b.y1-26,'green: the rotor, &zeta; = '+fmt(ST.zeta,2)+' (dashed: 0.2, 1, 2)',COL.pos,SMALL_FONT,'left','bottom');
  lab(ctx,W,H,b.x+10,b.y1-12,'orange: PhET&rsquo;s rule, '+fmt(phetFieldStep(M.mu),4)+' rad per frame at 60 fps',COL.ref,SMALL_FONT,'left','bottom');
  if(!(M.muE>1e-9)) lab(ctx,W,H,b.x+b.w/2,b.y+b.h*0.33,'no dipole, or no field: nothing turns',COL.ref,TITLE_FONT,'center','middle');

  /* the phase portrait */
  const p=L.bottom[0];
  if(p){
    const wmax=Math.max(0.35,1.15*Math.max.apply(null,M.traces.live.vs.map(Math.abs)));
    axesR(ctx,p,-185,185,-wmax,wmax,{xlab:'&psi; (degrees)',ylab:'d&psi;/dt',
      title:titleFor(p,'the phase portrait: every orbit spirals into &psi; = 0','phase portrait'),
      xticks:[-180,-90,0,90,180]});
    if(M.muE>1e-9){
      /* the separatrix of the undamped rotor, for reference */
      const xs=[], ys=[], xs2=[], ys2=[];
      for(let k=0;k<=240;k++){ const a=-PI+TAU*k/240, e=2*M.muE*(1+Math.cos(a));
        const w=Math.sqrt(Math.max(0,e)); xs.push(a*180/PI); ys.push(w); xs2.push(a*180/PI); ys2.push(-w); }
      polyline(ctx,p,xs,ys,-185,185,-wmax,wmax,rgba(COL.struct,0.45),1.2,[4,4]);
      polyline(ctx,p,xs2,ys2,-185,185,-wmax,wmax,rgba(COL.struct,0.45),1.2,[4,4]);
      const tr=M.traces.live;
      polyline(ctx,p,tr.ys,tr.vs,-185,185,-wmax,wmax,COL.pos,1.8);
      marker(ctx,p,-185,185,-wmax,wmax,0,0,COL.live);
      lab(ctx,W,H,p.x+p.w/2,p.y+12,'&psi; = 0 stable &middot; &psi; = &plusmn;180&deg; unstable &middot; dashed: the undamped separatrix',
        COL.dim,SMALL_FONT,'center','top');
    }
  }
  drawCaption(ctx,L);
}

/* ---------------------------------------------------------------- *
 *  view: the dipole atlas                                            *
 * ---------------------------------------------------------------- */
const ATLAS_CAP='All nineteen of PhET&rsquo;s molecules against measurement. Top: its Psi4 dipole moment against the NIST CCCBDB experimental value, '
  +'with the line of equality. Bottom: the Basic model&rsquo;s vector sum of |&Delta;EN| against the same measurements &mdash; it has no debye scale at all, only an '
  +'ordering, and ozone breaks even that, since three identical atoms give &Delta;EN = 0 on both bonds. Green: within 0.1 D. Orange: further.';
const ATLAS_CAP_S='PhET&rsquo;s computed dipole moments against the measured ones, and the Basic model&rsquo;s |&Delta;EN| sum against the same values.';
function atlasGeo(ctx,W,H){ return stageLayout(ctx,W,H-HINT_H,ATLAS_CAP,ATLAS_CAP_S,1,0.44,1); }
function drawAtlas(ctx,W,H,M){
  const L=atlasGeo(ctx,W,H), b=L.main;
  const rows=M.rows.filter(r=>r.meas!==null);
  const hi=3.2;
  axesR(ctx,b,0,hi,0,hi,{xlab:'measured |&mu;| (debye, CCCBDB)',ylab:'PhET&rsquo;s Psi4 |&mu;| (debye)',
    title:titleFor(b,'the quantum column against measurement','Psi4 against measured')});
  polyline(ctx,b,[0,hi],[0,hi],0,hi,0,hi,rgba(COL.struct,0.6),1.3,[5,5]);
  for(const r of rows){
    const X=b.x+b.w*clamp(r.meas,0,hi)/hi, Y=b.y1-b.h*clamp(r.psi4,0,hi)/hi;
    const good=Math.abs(r.diff)<0.1;
    dot(ctx,X,Y,4.2,good?COL.pos:COL.ref,'#0b0e16',1);
    if(r.meas>0.02||r.psi4>0.02) lab(ctx,W,H,X+7,Y-2,formulaOnCanvas(r.sym),good?COL.pos:COL.ref,SMALL_FONT,'left','middle');
  }
  lab(ctx,W,H,b.x+b.w*0.30,b.y1-14,'the nine symmetric molecules sit on the origin',COL.dim,SMALL_FONT,'left','bottom');
  lab(ctx,W,H,b.x+10,b.y+12,'mean |difference| '+fmt(M.stats.mae,3)+' D',COL.text,SMALL_FONT,'left','top');
  lab(ctx,W,H,b.x+10,b.y+27,'worst: '+formulaOnCanvas(M.stats.worst.sym)+' '+fmt(M.stats.worst.diff,3)+' D',COL.ref,SMALL_FONT,'left','top');

  const p=L.bottom[0];
  if(p){
    const bmax=Math.max(2.4,1.1*Math.max.apply(null,rows.map(r=>r.basic)));
    axesR(ctx,p,0,hi,0,bmax,{xlab:'measured |&mu;| (debye)',ylab:'basic |&Sigma;&mu;| (&Delta;EN units)',
      title:titleFor(p,'the Basic model has an ordering, not a scale','basic |&Sigma;&mu;| against measured')});
    for(const r of rows){
      const X=p.x+p.w*clamp(r.meas,0,hi)/hi, Y=p.y1-p.h*clamp(r.basic,0,bmax)/bmax;
      const bad=r.meas>0.2&&r.basic<0.05;
      dot(ctx,X,Y,4.2,bad?COL.ref:COL.pos,'#0b0e16',1);
      if(bad||r.meas>1.5) lab(ctx,W,H,X+7,Y-2,formulaOnCanvas(r.sym),bad?COL.ref:COL.pos,SMALL_FONT,'left','middle');
    }
    lab(ctx,W,H,p.x+p.w/2,p.y+12,'ozone: three oxygens, so &Delta;EN = 0 on both bonds and Basic calls it non-polar. It measures '
      +fmt(measuredOf('O3')[0],3)+' D.',COL.ref,SMALL_FONT,'center','top');
  }
  drawCaption(ctx,L);
}

/* ================================================================== *
 *  dispatch and the scene                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LABELS=[]; POLY_SEGS=[]; LEGEND_RECTS=[]; PICKS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(M.view==='two') drawTwo(ctx,W,H,M);
  else if(M.view==='three') drawThree(ctx,W,H,M);
  else if(M.view==='real') drawReal(ctx,W,H,M);
  else if(M.view==='sum') drawSum(ctx,W,H,M);
  else if(M.view==='field') drawField(ctx,W,H,M);
  else drawAtlas(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712,onView:null};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.step=function(dt){ return fieldStep(dt); };
  S.resetCam=function(){ ST.camTheta=DEFAULTS.camTheta; ST.camPhi=DEFAULTS.camPhi; ST.zoom=1; };
  S.wheel=function(dy){ if(ST.view!=='real'&&ST.view!=='two'&&ST.view!=='three') return false;
    ST.zoom=clamp(ST.zoom*(dy>0?0.93:1.075),0.5,2.5); return true; };
  S.pointer=function(type,x,y){
    const v=ST.view, ctx=canvas.getContext('2d');
    if(type==='down'){
      DRAG.x0=x; DRAG.y0=y; DRAG.lx=x; DRAG.ly=y; DRAG.moved=0;
      if(v==='two'||v==='three'){
        let best=null;
        for(const p of PICKS){ if(p.kind==='mol') continue;
          const d=Math.hypot(x-p.x,y-p.y); if(d<=p.r&&(!best||d<best.d)){ best=p; best.d=d; } }
        DRAG.what=best?best.kind:'mol';      /* anywhere else turns the molecule */
        if(ST.field) fieldReset();
        return true;
      }
      if(v==='real'){ DRAG.what='orbit'; return true; }
      if(v==='sum'){ const G=sumGeo(ctx,S.W,S.H), b=G.main;
        if(x>=b.x&&x<=b.x1&&y>=b.y&&y<=b.y1){ DRAG.what='sumAngle'; setBondAngleDeg(180*(x-b.x)/b.w); return true; } return false; }
      if(v==='field'){ const G=fieldGeo(ctx,S.W,S.H), b=G.main;
        if(x>=b.x&&x<=b.x1&&y>=b.y&&y<=b.y1){ DRAG.what='psi0'; ST.psi0=clamp(185-370*(y-b.y)/b.h,-180,180); return true; } return false; }
      return false;
    }
    if(type==='move'){
      if(!DRAG.what) return false;
      const dx=x-DRAG.lx, dy=y-DRAG.ly; DRAG.lx=x; DRAG.ly=y; DRAG.moved+=Math.abs(dx)+Math.abs(dy);
      if(DRAG.what==='orbit'){ ST.camTheta-=dx*0.0075; ST.camPhi=clamp(ST.camPhi+dy*0.006,-1.45,1.45); return true; }
      if(DRAG.what==='mol'){ const G=v==='three'?threeGeo(ctx,S.W,S.H):twoGeo(ctx,S.W,S.H), map=G.map;
        const a0=Math.atan2(y-dy-map.cy,x-dx-map.cx), a1=Math.atan2(y-map.cy,x-map.cx);
        ST.molAngle=normAngle(ST.molAngle+(a1-a0),-PI); FIELD.w=0; return true; }
      if(DRAG.what==='A'||DRAG.what==='C'){
        const G=threeGeo(ctx,S.W,S.H), map=G.map;
        const a=Math.atan2(y-map.cy,x-map.cx)-ST.molAngle;
        if(DRAG.what==='A') ST.angAB=normAngle(a,-PI); else ST.angBC=normAngle(a,0);
        FIELD.w=0; return true; }
      if(DRAG.what==='sumAngle'){ const G=sumGeo(ctx,S.W,S.H), b=G.main;
        setBondAngleDeg(180*(x-b.x)/b.w); return true; }
      if(DRAG.what==='psi0'){ const G=fieldGeo(ctx,S.W,S.H), b=G.main;
        ST.psi0=clamp(185-370*(y-b.y)/b.h,-180,180); return true; }
      return false;
    }
    const had=DRAG.what!==null; DRAG.what=null; return had;
  };
  return S;
}
/* set the A-B-C angle, keeping the molecule's bisector where it is */
function setBondAngleDeg(deg){
  const d=clamp(deg,0,180)*PI/180, mid=(ST.angAB+ST.angBC)/2;
  ST.angAB=normAngle(mid+d/2,-PI); ST.angBC=normAngle(mid-d/2,0);
}
