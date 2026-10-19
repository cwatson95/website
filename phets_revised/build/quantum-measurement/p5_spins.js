
/* ================================================================== *
 *  THE SPINS view (PhET's Spin screen: Stern-Gerlach)                 *
 * ================================================================== */
const SG_EXT={xmin:-1.05,xmax:5.55,ymin:-1.12,ymax:1.12};
function axisName(a){ return a==='z'?'z':'x'; }
function spinsModel(st){
  const sc=SGS, axes=sgAxes(st), r0=sgSource(st), two=axes.length>1, block=sgBlock(st);
  const m={sc, axes, r0, two, block, probs:sgProbs(r0,axes)};
  m.p1=bornP(r0,AXV[axes[0]]);
  m.p2=two?bornP(AXV[axes[0]],AXV[axes[1]]):NaN;
  m.p3=two?bornP(AXV[axes[0]].map(v=>-v),AXV[axes[2]]):NaN;
  m.theta=Math.atan2(r0[0],r0[2]);             /* polar angle in the x-z plane */
  m.alpha=Math.sqrt(bornP(r0,[0,0,1])); m.beta=Math.sqrt(1-m.alpha*m.alpha);
  m.phetP=st.sgExp==='custom'?(1+Math.cos(phetCustomTheta(st.sgA2)))/2:NaN;
  /* the per-magnet tallies: counts (single) or averaged rates (continuous) */
  const cont=st.sgMode==='continuous';
  m.tal=sc.c.map(c=>{ const u=cont?c.up.value:c.nU, d=cont?c.dn.value:c.nD, n=u+d; return {u,d,n,f:n>0?u/n:NaN}; });
  m.last=sc.last; m.inFlight=sc.parts.length;
  return m;
}
function spinsGeo(ctx,W,H,Cap){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?18:56;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(140,Math.min(narrow?230:345,avail*0.58));
  const app=box(left,top,rightTop-left,upH);
  const map=worldFitUp(app,SG_EXT,0);
  const lowTop=top+upH+40, lowH=fit.capY-16-lowTop-20;           /* no floor: the row is skipped when it does not fit */
  const discR=Math.max(20,Math.min(64,(lowH-34)*0.42));
  const disc={cx:left+discR+22, cy:lowTop+20+discR, r:discR, show:lowH>=70};
  const hx0=disc.cx+discR+(narrow?64:84), hw=narrow?Math.max(90,(W-18-hx0)/2-24):150;
  const h1=box(hx0,lowTop+14,hw,lowH-44), h2=box(h1.x1+(narrow?30:56),lowTop+14,hw,lowH-44);
  const tbl=narrow?null:box(h2.x1+56,lowTop,Math.max(0,(W-26)-(h2.x1+56)),lowH);
  return {narrow,top,left,fit,app,map,disc,h1,h2,tbl:tbl&&tbl.w>=200?tbl:null};
}
function spinsCaption(M){
  const m=M.S, st=M.st;
  const seq=m.two?'Magnet 1’s up beam goes to the upper magnet and its down beam to the lower one; each measurement leaves the spin exactly along its magnet’s axis, so the second stage sees ±n₁, never the source.':'One magnet: P(up) = ½(1 + r·n) = cos²(Θ/2).';
  return {full:'Schematic, not to scale: the magnets are ideal filters, drawn as boxes. '+seq+(m.block!=='none'?' Magnet 1’s '+m.block+' beam is blocked.':'')+(st.sgMode==='single'?' Click the source for one particle; the dials show its spin at each stage.':''),
          short:'Schematic: ideal Stern–Gerlach filters. P(up) = cos²(Θ/2) at every magnet.'};
}
function sgMagnetBoxes(map,m,st){
  const X=map.X, Y=map.Y, out=[];
  out.push({k:0,b:box(X(SGL.S1[0]),Y(0.34),(SGL.S1[1]-SGL.S1[0])*map.s,0.68*map.s),ax:m.axes[0],show:true});
  if(m.two){ out.push({k:1,b:box(X(SGL.S2[0]),Y(SGL.Y2+0.3),(SGL.S2[1]-SGL.S2[0])*map.s,0.6*map.s),ax:m.axes[1],show:m.block!=='up'});
             out.push({k:2,b:box(X(SGL.S2[0]),Y(-SGL.Y2+0.3),(SGL.S2[1]-SGL.S2[0])*map.s,0.6*map.s),ax:m.axes[2],show:m.block!=='down'}); }
  return out;
}
/* the single-particle mode's stage dials (PhET's measurement devices), in
   pixels: two above the first stage; after magnet 2 on the midline between
   the second magnets' inner beams, labelled to its right (up at y 0.84 it sat
   on the upper magnet's up beam, looked at).  selfTest holds every dial clear
   of every beam band. */
function sgDials(map,m){
  const X=map.X, Y=map.Y, r=Math.max(12,0.2*map.s), L=m.last;
  const d=[{x:X(0.45),y:Y(0.84),r,v:L?L.r0:null,label:'from the source',side:'top'},
           {x:X(2.55),y:Y(0.84),r,v:L&&L.up1!==null?L.r1:null,label:'after magnet 1',side:'top'}];
  if(m.two) d.push({x:X(4.6),y:Y(0),r,v:L&&L.up2!==null?L.r2:null,label:'after magnet 2',side:'right'});
  return d;
}
function drawStateDial(ctx,cx,cy,r,v,col,label,W,H,faint){
  ctx.beginPath(); ctx.arc(cx,cy,r,0,TAU); ctx.strokeStyle=faint?COL.faint:COL.struct; ctx.lineWidth=1; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx-r,cy); ctx.lineTo(cx+r,cy); ctx.moveTo(cx,cy-r); ctx.lineTo(cx,cy+r); ctx.strokeStyle='#1d2330'; ctx.stroke();
  if(v){ const ex=cx+v[0]*r*0.92, ey=cy-v[2]*r*0.92; ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(ex,ey); ctx.strokeStyle=col; ctx.lineWidth=2.2; ctx.stroke(); mark(ctx,ex,ey,'o',col,2.6); }
  if(label) lab(ctx,W,H,cx,cy-r-9,label,COL.dim,SM_FONT,'center','middle');
}
function drawSpins(ctx,W,H,M){
  const m=M.S, st=M.st, sc=m.sc, Cap=spinsCaption(M), G=spinsGeo(ctx,W,H,Cap), map=G.map, X=map.X, Y=map.Y, s=map.s;
  /* the beams first; a blocked branch ends at the blocker */
  const faintBeam=(pts)=>{ ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(X(p[0]),Y(p[1])); else ctx.moveTo(X(p[0]),Y(p[1])); });
    ctx.strokeStyle='#1f2738'; ctx.lineWidth=Math.max(2,0.07*s); ctx.stroke(); };
  const upTo=(pts,L)=>{ const out=[pts[0]]; let acc=0;
    for(let i=1;i<pts.length;i++){ const sl=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);
      if(acc+sl>=L){ out.push(polyAt(pts,L)); return out; } acc+=sl; out.push(pts[i]); } return out; };
  for(const u1 of [true,false]){
    if(!m.two){ faintBeam(sgWaypoints({jy:0,up1:u1,two:false,up2:null})); continue; }
    const blocked=(m.block==='up'&&u1)||(m.block==='down'&&!u1);
    if(blocked) faintBeam(upTo(sgWaypoints({jy:0,up1:u1,two:true,up2:true}),SG_BLOCK_D));
    else for(const u2 of [true,false]) faintBeam(sgWaypoints({jy:0,up1:u1,two:true,up2:u2}));
  }
  /* the particles, UNDER the source and the magnets: what happens inside a
     magnet is not on view, as in a real apparatus (and in PhET) */
  const live=st.sgMode==='single';
  for(const p of sc.parts){
    const d=SG_SPEED*(sc.t-p.t0); if(d<0) continue;
    const q=polyAt(sgWaypoints(p),d);
    mark(ctx,X(q[0]),Y(q[1]),'o',live?COL.live:(p.up1===null?'#e9f0ff':(p.two&&p.up2!==null?(p.up2?COL.pos:COL.neg):(p.up1?COL.pos:COL.neg))),live?4.5:2.3);
  }
  /* the source */
  const sb=box(X(-0.95),Y(0.36),0.95*s,0.72*s);
  ctx.fillStyle='#161b28'; ctx.fillRect(sb.x,sb.y,sb.w,sb.h); frame(ctx,sb,COL.struct);
  lab(ctx,W,H,sb.x+sb.w/2,sb.y+sb.h/2-8,'spin-½',COL.text,SM_FONT,'center','middle');
  lab(ctx,W,H,sb.x+sb.w/2,sb.y+sb.h/2+8,st.sgMode==='single'?'source (click)':'source',COL.text,SM_FONT,'center','middle');
  for(const mg of sgMagnetBoxes(map,m,st)){
    if(!mg.show) continue;
    const b=mg.b; ctx.fillStyle='#1a2030'; ctx.fillRect(b.x,b.y,b.w,b.h);
    frame(ctx,b,st.sgExp==='custom'?COL.live:COL.struct);     /* magenta: it can be turned */
    lab(ctx,W,H,b.x+b.w/2,b.y+b.h/2,'SG'+axisName(mg.ax),COL.text,'italic 14px Georgia, serif','center','middle');
    /* the field gradient's sense (which exit is "up" along the axis), INSIDE
       the magnet at its exit face: the particles pass under the magnets, so
       nothing covers it (outside, on the beams, a particle sat on the ↓z,
       looked at).  Only where the box has room for three rows. */
    if(b.h>=50&&b.w>=70){ lab(ctx,W,H,b.x1-5,b.y+10,mg.ax==='z'?'↑z':'+x',COL.pos,SM_FONT,'right','middle');
      lab(ctx,W,H,b.x1-5,b.y1-10,mg.ax==='z'?'↓z':'−x',COL.neg,SM_FONT,'right','middle'); }
  }
  if(st.sgExp==='custom') lab(ctx,W,H,X(1.5),Y(-0.34)+12,'click a magnet to turn it',COL.live,SM_FONT,'center','middle');
  /* the blocker on magnet 1's exit */
  if(m.block!=='none'){ const yb=m.block==='up'?0.16+(0.62-0.16)*0.30:-(0.16+(0.62-0.16)*0.30);
    ctx.fillStyle='#d5dbe8'; ctx.fillRect(X(2.28),Y(yb+0.13),0.05*s,0.26*s); lab(ctx,W,H,X(2.3),Y(yb+0.13)-9,'blocked',COL.dim,SM_FONT,'center','middle'); }
  /* the per-branch tallies at the ends */
  const tal=m.tal, cnt=(v)=>st.sgMode==='single'?String(v):sigf(v,3)+'/s';
  if(!m.two){ lab(ctx,W,H,X(SGL.END)+6,Y(SGL.Y2),'↑ '+cnt(tal[0].u),COL.pos,LAB_FONT,'left','middle'); lab(ctx,W,H,X(SGL.END)+6,Y(-SGL.Y2),'↓ '+cnt(tal[0].d),COL.neg,LAB_FONT,'left','middle'); }
  else for(const [k,ys] of [[1,1],[2,-1]]){ if((k===1&&m.block==='up')||(k===2&&m.block==='down')) continue;
    lab(ctx,W,H,X(SGL.END)+6,Y(ys*SGL.Y2+SGL.EXIT*2.2),'+ '+cnt(tal[k].u),COL.pos,SM_FONT,'left','middle');
    lab(ctx,W,H,X(SGL.END)+6,Y(ys*SGL.Y2-SGL.EXIT*2.2),'− '+cnt(tal[k].d),COL.neg,SM_FONT,'left','middle'); }
  /* single-particle mode: the particle's spin at each stage (PhET's measurement devices) */
  if(live){
    for(const d of sgDials(map,m)){ drawStateDial(ctx,d.x,d.y,d.r,d.v,COL.live,d.side==='top'?d.label:null,W,H,!d.v);
      if(d.side==='right') lab(ctx,W,H,d.x+d.r+6,d.y,d.label,COL.dim,SM_FONT,'left','middle'); }
  }
  lab(ctx,W,H,G.app.x+2,G.app.y1+12,'schematic, not to scale · '+(live?'one particle at a time':fmt(SG_RATE*st.sgAmount,0)+' particles/s'),COL.faint,SM_FONT,'left','middle');
  /* the prepared state: its Bloch vector in the x-z plane, with its projections */
  const D=G.disc;
  if(D.show){
    drawStateDial(ctx,D.cx,D.cy,D.r,m.r0,COL.pos,null,W,H,false);
    ctx.beginPath(); ctx.moveTo(D.cx,D.cy); ctx.lineTo(D.cx+m.r0[0]*D.r*0.92,D.cy); ctx.moveTo(D.cx,D.cy); ctx.lineTo(D.cx,D.cy-m.r0[2]*D.r*0.92);
    ctx.setLineDash([3,3]); ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.stroke(); ctx.setLineDash([]);
    lab(ctx,W,H,D.cx-D.r-4,D.cy-D.r-10,'prepared'+(st.sgExp==='custom'?' (drag)':': '+st.sgSrc.replace('-','−')),COL.text,SM_FONT,'left','middle');
    lab(ctx,W,H,D.cx+5,D.cy-D.r+4,'z',COL.dim,'italic 12px Georgia, serif','left','middle'); lab(ctx,W,H,D.cx+D.r+7,D.cy,'x',COL.dim,'italic 12px Georgia, serif','left','middle');
  }
  /* each magnet's up fraction against its projection */
  const hist=(b,k,title,pe,labU,labD)=>{
    const t=tal[k];
    axesT(ctx,b,0,2,0,1,{xticks:[],yticks:[0,0.5,1],title:fitTitle(b,title,title.split(':')[0])});
    const bw=Math.min(36,b.w*0.22), x1=px(b,0.6,0,2), x2=px(b,1.4,0,2);
    if(t.n>0){ ctx.fillStyle=COL.pos; ctx.fillRect(x1-bw/2,py(b,t.f,0,1),bw,b.y1-py(b,t.f,0,1)); ctx.fillStyle=COL.neg; ctx.fillRect(x2-bw/2,py(b,1-t.f,0,1),bw,b.y1-py(b,1-t.f,0,1)); }
    /* the law's marks before the value labels, so a label is never struck through */
    const on=st.sgExpect&&isFinite(pe), yU=on?py(b,pe,0,1):null, yD=on?py(b,1-pe,0,1):null;
    if(on){ ctx.beginPath(); ctx.moveTo(x1-bw/2-6,yU); ctx.lineTo(x1+bw/2+6,yU); ctx.moveTo(x2-bw/2-6,yD); ctx.lineTo(x2+bw/2+6,yD); ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke(); }
    /* each value clear of its bar and its mark; the empty-box note clear of both marks */
    if(t.n>0){ barVal(ctx,W,H,x1,py(b,t.f,0,1),b,fmt(100*t.f,0)+'%',COL.pos,yU); barVal(ctx,W,H,x2,py(b,1-t.f,0,1),b,fmt(100*(1-t.f),0)+'%',COL.neg,yD); }
    else lab(ctx,W,H,b.x+b.w/2,freeY(b,on?[yU,yD]:[]),'nothing yet',COL.dim,SM_FONT,'center','middle');
    ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.fillStyle=COL.pos; ctx.fillText(labU,x1,b.y1+4); ctx.fillStyle=COL.neg; ctx.fillText(labD,x2,b.y1+4);
  };
  const ax=a=>a==='z'?'z':'x';
  if(G.h1.h>=45){
    hist(G.h1,0,'magnet 1 (SG'+ax(m.axes[0])+'): up, down',m.p1,'↑'+ax(m.axes[0]),'↓'+ax(m.axes[0]));
    if(m.two&&G.h2.x1<=W-8){ const k=m.block==='up'?2:1, a=m.axes[k];
      hist(G.h2,k,(k===1?'upper':'lower')+' magnet (SG'+ax(a)+'): up, down',k===1?m.p2:m.p3,'↑'+ax(a),'↓'+ax(a)); }
  }
  /* products of projections, against what came out */
  if(G.tbl){
    const b=G.tbl; let y=b.y+10;
    lab(ctx,W,H,b.x,y,'products of projections',COL.text,'italic 13px Georgia, serif','left','middle'); y+=20;
    const pr=m.probs, names=m.two?['↑↑','↑↓','↓↑','↓↓']:['↑','↓'];
    for(let i=0;i<names.length;i++){
      const txt=m.two?('P('+names[i]+') = '+(i<2?fmt(m.p1,3):fmt(1-m.p1,3))+' × '+(i<2?fmt(i===0?m.p2:1-m.p2,3):fmt(i===2?m.p3:1-m.p3,3))+' = '+fmt(pr[i],3))
                     :('P('+names[i]+') = '+fmt(pr[i],3));
      lab(ctx,W,H,b.x,y,txt,i%2===0?COL.pos:COL.neg,SM_FONT,'left','middle'); y+=15;
    }
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function spinsReadout(M){
  const m=M.S, st=M.st, e=SG_EXPS.find(x=>x.id===st.sgExp);
  let s=hd('the experiment')+rrow('experiment',e.id==='custom'?'custom [SG'+m.axes[0]+', SG'+m.axes[1]+']':e.name)+rrow('source',st.sgMode==='single'?'single particles':fmt(SG_RATE*st.sgAmount,0)+' per second');
  s+=hd('the prepared spin')+rrow('r = (x, z)',fmt(m.r0[0],3)+', '+fmt(m.r0[2],3))+rrow('|&psi;&rang; = &alpha;|&uarr;z&rang; + &beta;|&darr;z&rang;',fmt(m.alpha,3)+', '+fmt(m.beta,3))
    +rrow('P(&uarr;z) = |&alpha;|&sup2;',fmt(m.alpha*m.alpha,3),'good');
  if(st.sgExp==='custom') s+=rrow('PhET&rsquo;s &theta; = &pi;(1&minus;|&alpha;|&sup2;) would give',fmt(m.phetP,3),Math.abs(m.phetP-m.alpha*m.alpha)>1e-9?'bad':'');
  s+=hd('magnet 1 (SG'+m.axes[0]+')')+rrow('P(up) = &frac12;(1 + r&middot;n&#770;)',fmt(m.p1,3))+rrow('measured up',isFinite(m.tal[0].f)?fmt(m.tal[0].f,3)+' of '+(st.sgMode==='single'?m.tal[0].n:sigf(m.tal[0].n,3)+'/s'):'&mdash;','good');
  if(m.two){
    s+=hd('second stage')+rrow('upper: P(up | &uarr;<sub>1</sub>) = &frac12;(1 + n&#770;<sub>1</sub>&middot;n&#770;<sub>2</sub>)',fmt(m.p2,3))
      +rrow('lower: P(up | &darr;<sub>1</sub>) = &frac12;(1 &minus; n&#770;<sub>1</sub>&middot;n&#770;<sub>3</sub>)',fmt(m.p3,3))
      +rrow('P(&uarr;&uarr;), P(&uarr;&darr;), P(&darr;&uarr;), P(&darr;&darr;)',m.probs.map(v=>fmt(v,3)).join(', '));
    if(m.block!=='none') s+=rrow('blocked',"magnet 1&rsquo;s "+m.block+' beam');
  }
  return s;
}
function spinsEq(M){ return ['<span class="hl">P(&uarr;<sub>n</sub>) = |&lang;&uarr;<sub>n</sub>|&psi;&rang;|&sup2; = &frac12;(1 + r&middot;n&#770;) = cos&sup2;(&Theta;/2)</span> &nbsp;&middot;&nbsp; P(&uarr;<sub>1</sub>&uarr;<sub>2</sub>) = P(&uarr;<sub>1</sub>) cos&sup2;(&Theta;<sub>12</sub>/2)',
  'each magnet asks one yes/no question and leaves the spin along its own axis, so a sequence of magnets multiplies projections']; }
function spinsTag(M){ const st=M.st, e=SG_EXPS.find(x=>x.id===st.sgExp); return '<b>the spins</b> — experiment '+e.name+', '+(st.sgMode==='single'?'single particles':'a continuous beam')+(st.running?'':', paused'); }
const INFO_SPINS='PhET&rsquo;s Spin screen fires spin-&frac12; atoms through Stern&ndash;Gerlach magnets. Each magnet asks one question &mdash; is the spin up or '
  +'down along my axis? &mdash; and each atom answers up with probability &frac12;(1 + r&middot;n&#770;) = cos&sup2;(&Theta;/2), where &Theta; is the angle between the '
  +'spin&rsquo;s Bloch vector and the magnet&rsquo;s axis. That is the half-angle: a spin along x put into a z magnet is split fifty-fifty, not sent '
  +'through at cos&sup2;(90&deg;) = 0. The atoms that come out are no longer what went in. They are exactly along the magnet&rsquo;s axis, up or down, so a '
  +'second magnet sees &plusmn;n&#770;<sub>1</sub> and never the source: the probabilities of a sequence multiply. Experiment 4 (z then z) passes every '
  +'up atom again. Experiment 3 (z then x) splits them fifty-fifty again, because a z measurement erased whatever x the atoms had. In the custom '
  +'experiment you can turn each magnet and drag the prepared spin anywhere in the x&ndash;z plane.';
const DERIV_SPINS='<h4>a magnet, and then another</h4>'
  +EQ(1,'P<sub>&plusmn;n</sub> = &frac12;(&#120793; &plusmn; n&#770;&middot;&sigma;), &nbsp; P(&uarr;<sub>n</sub>) = Tr(&rho;P<sub>+n</sub>) = &frac12;(1 + r&middot;n&#770;)')
  +EQ(2,'<span class="rm">after the magnet:</span> r &rarr; &plusmn;n&#770;, <span class="rm">whatever r was</span>')
  +EQ(3,'P(s<sub>1</sub>, s<sub>2</sub>) = ||P<sub>s2 n2</sub>P<sub>s1 n1</sub>|&psi;&rang;||&sup2; = P(s<sub>1</sub>) &middot; &frac12;(1 + s<sub>1</sub>s<sub>2</sub> n&#770;<sub>1</sub>&middot;n&#770;<sub>2</sub>)')
  +EQ(4,'<span class="rm">custom:</span> |&psi;&rang; = &alpha;|&uarr;z&rang; + &beta;|&darr;z&rang;, &nbsp; &theta; = 2 arccos|&alpha;|, &nbsp; r = (sin&theta;, 0, cos&theta;)')
  +'<p>PhET&rsquo;s custom state uses &theta; = &pi;(1 &minus; |&alpha;|&sup2;), so its own equation disagrees with its |&alpha;|&sup2; slider except at 0, '
  +'&frac12; and 1 (at 0.75 its z magnet passes 0.854). Here the slider is P(&uarr;z) exactly.</p>'
  +'<div class="cite">pins: all seven experiments &times; four sources against 2&times;2 complex projectors (numpy); 10 000 atoms through z then x from +X, '
  +'[2558, 2517, 2473, 2452]; through x then z from +Z, [2500, 2553, 2522, 2425] &mdash; derive.py</div>';
