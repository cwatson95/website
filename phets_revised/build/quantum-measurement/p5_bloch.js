
/* ================================================================== *
 *  THE BLOCH SPHERE view (PhET's Bloch Sphere screen)                 *
 * ================================================================== */
function degs(x){ return fmt(x/DEG,0)+'°'; }
function blochModel(st,cam){
  const sc=BLO, r0=blochPrep(st), k0=ketOf(st.bTheta,st.bPhi), n=BASIS[st.bAxis].n;
  const s=st.bField?st.bStrength:0;
  const m={sc, r0, k0, n, s, field:st.bField, phase:sc.phase, tau:sc.tau, na:blochNAtoms(st)};
  m.fGHz=Math.abs(s);                                   /* f = |s| x 1 GHz: B0 turns the electron once a ns */
  m.BmT=s*B0_T*1e3;
  m.period=m.fGHz>0?1/m.fGHz:Infinity;                  /* ns */
  m.turnAtMeasure=st.bField?larmorAngle(s,st.bDelay):0; /* rad */
  m.rMeasure=st.bField?precess(r0,s,st.bDelay):r0;
  m.pUp=bornP(m.rMeasure,n);
  m.nObs=sc.up+sc.dn; m.frac=m.nObs>0?sc.up/m.nObs:NaN; m.fracSd=m.nObs>0?Math.sqrt(m.pUp*(1-m.pUp)/m.nObs):NaN;
  /* the single atom's ket now: prepared, turning, or collapsed */
  if(sc.phase==='observed'){ const up=dot3v(sc.r[0],n)>0; m.kNow=up?BASIS[st.bAxis].up.slice():BASIS[st.bAxis].dn.slice(); }
  else m.kNow=mApply(precessU(s,sc.phase==='timing'?sc.tau:0),k0);
  m.eqPrep=ketInBasis(k0,st.bBasis); m.eqNow=ketInBasis(m.kNow,st.bBasis);
  m.rNow=sc.r.map(v=>v.slice());
  /* the fringe: P(up along n) against the delay, for the strength on the slider
     (the field's own curve when it is on; what it WOULD do when it is off) */
  m.fringe=[]; for(let i=0;i<=200;i++){ const t=BL.DELAY_MAX*i/200; m.fringe.push([t,bornP(precess(r0,st.bStrength,t),n)]); }
  m.pFlat=bornP(r0,n);
  m.cam=cam||CAM_HOME;
  return m;
}
function blochGeo(ctx,W,H,Cap,na){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?18:56;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(150,Math.min(narrow?250:430,avail*0.62));
  /* the sphere and everything round it: the titles sit above the axis names
     (1.42 R), the stage line below the sphere, so R follows the height */
  const R=Math.max(36,Math.min(narrow?78:118,(upH-62)/2.6,(rightTop-left)*0.14));
  const prep={cx:left+R*1.45+6,cy:top+24+1.5*R,R};
  const meas={cx:prep.cx+R*2.9+(narrow?10:40),cy:prep.cy,R};
  const colX=meas.cx+R*1.55+(narrow?14:34);
  const hist=box(colX+22,top+22,Math.max(90,rightTop-colX-22),Math.max(70,upH*0.46));
  const timer=box(colX+22,hist.y1+52,Math.max(90,rightTop-colX-22),14);
  const lowTop=top+upH+34, eqs={x:left,y:lowTop,w:(narrow?W-18:W-26)-left,h:fit.capY-12-lowTop};
  /* the fringe panel, right of the equations (wide canvases only) */
  const fx=left+560, fringe=narrow?null:box(fx,lowTop+14,Math.min(560,(W-26)-fx),fit.capY-16-(lowTop+14)-34);
  /* ten atoms: PhET's rows of 3, 2, 3, 2 */
  const smallR=Math.max(16,Math.min(34,R*0.30)), ten=[];
  const rows=[3,2,3,2], dy=smallR*2.55, dx=smallR*2.55;
  rows.forEach((n,ri)=>{ for(let i=0;i<n;i++) ten.push({cx:meas.cx+(i-(n-1)/2)*dx*1.05,cy:meas.cy+(ri-1.5)*dy,R:smallR}); });
  return {narrow,top,left,fit,prep,meas,hist,timer,eqs,ten,fringe:fringe&&fringe.w>=240&&fringe.h>=70?fringe:null};
}
/* panel: whether the fringe panel is drawn (the caption names it only then) */
function blochCaption(M,panel){
  const m=M.B, st=M.st;
  const fld=st.bField?'The field is along z: B = '+sigf(m.BmT,3)+' mT turns an electron’s spin counterclockwise at '+sigf(m.fGHz,3)+' GHz, so in the '+fmt(st.bDelay,2)+'-ns delay it turns '+fmt(m.turnAtMeasure/DEG,0)+'°. ':'No field: the state waits unchanged. ';
  return {full:'Perspective 3-D; drag to turn both spheres. Left: the prepared state. Right: what is measured along '+st.bAxis+'. '+fld+'P(up) = ½(1 + r·n̂) = '+fmt(m.pUp,3)+' at the moment of measurement'+(panel!==false?'; the panel below draws it against the delay.':'.'),
          short:'Drag to turn. P(up along '+st.bAxis+') = '+fmt(m.pUp,3)+' at the measurement.'};
}
/* the caption and the geometry together: the fringe panel is optional */
function blochLayout(ctx,W,H,M){ return layoutNamed(p=>blochCaption(M,p),Cap=>blochGeo(ctx,W,H,Cap,M.B.na),G=>!!G.fringe); }
function eqRuns(E,b,sym,global){
  const r=[]; const bx=b.toLowerCase();
  if(global&&Math.abs(E.g)>1e-9&&Math.abs(E.g-2)>1e-9) r.push(['e',null],['i'+fmt(E.g,2)+'π','sup'],[' (',null]);
  if(E.a>1e-9) r.push([fmt(E.a,2)+'|↑',null],[bx,'sub'],['⟩',null]);
  if(E.a>1e-9&&E.c>1e-9) r.push([' + ',null]);
  if(E.c>1e-9){ r.push([fmt(E.c,2),null]); if(Math.abs(E.chi)>1e-9&&Math.abs(E.chi-2)>1e-9) r.push([' e',null],['i'+fmt(E.chi,2)+'π','sup']); r.push(['|↓',null],[bx,'sub'],['⟩',null]); }
  if(global&&Math.abs(E.g)>1e-9&&Math.abs(E.g-2)>1e-9) r.push([')',null]);
  return [[sym+' = ',null]].concat(r);
}
function drawBloch(ctx,W,H,M){
  const m=M.B, st=M.st, sc=m.sc, LY=blochLayout(ctx,W,H,M), Cap=LY.Cap, G=LY.G, cam=m.cam;
  /* the prepared state */
  const Sp=sphereProj(cam,G.prep.cx,G.prep.cy,G.prep.R);
  drawSphere(ctx,Sp,{});
  drawAngles(ctx,Sp,st.bTheta,st.bPhi,COL.struct);
  drawVec(ctx,Sp,m.r0,COL.pos,2.8,G.prep.R>60?'ψ':null);
  lab(ctx,W,H,G.prep.cx,G.top+4,'prepared',COL.text,'italic 13px Georgia, serif','center','middle');
  lab(ctx,W,H,G.prep.cx,G.prep.cy+G.prep.R+24,'θ = '+degs(st.bTheta)+', φ = '+degs(st.bPhi),COL.pos,LAB_FONT,'center','middle');
  /* what is measured: one atom, or ten */
  const n=m.n;
  const drawAtom=(S3,v,big)=>{
    drawSphere(ctx,S3,{grid:big,labels:big});
    /* the field's label goes left of its tip and the axis label right of its
       own, so B and Z never land on each other when both point along z */
    if(st.bField){ drawVec(ctx,S3,[0,0,1.3*Math.sign(m.s||1)],COL.struct,big?2:1.2,big?'B':null,'left'); }
    drawVec(ctx,S3,[1.12*n[0],1.12*n[1],1.12*n[2]],COL.ref,big?2:1.3,big?st.bAxis:null);
    if(sc.phase==='timing'&&big){ const tr=[]; const ang=larmorAngle(m.s,sc.tau); for(let i=0;i<=40;i++) tr.push(precess(m.r0,m.s,sc.tau*i/40)); if(Math.abs(ang)>1e-6) drawPath3(ctx,S3,tr,COL.live,1.6,[5,4]); }
    drawVec(ctx,S3,v,sc.phase==='observed'?(dot3v(v,n)>0?COL.pos:COL.neg):COL.pos,big?2.8:1.8,null);
  };
  if(m.na===1){ const S3=sphereProj(cam,G.meas.cx,G.meas.cy,G.meas.R); drawAtom(S3,m.rNow[0],true); }
  else G.ten.forEach((a,i)=>drawAtom(sphereProj(cam,a.cx,a.cy,a.R),m.rNow[i],false));
  lab(ctx,W,H,G.meas.cx,G.top+4,(m.na===1?'one atom, ':'ten atoms, ')+(G.narrow?'along ':'measured along ')+st.bAxis,COL.text,'italic 13px Georgia, serif','center','middle');
  const phaseTxt=sc.phase==='prepared'?(st.bField?'press start: the field turns it, then it is observed':'press observe'):(sc.phase==='timing'?'the field is turning the state':(m.na===1?'observed: '+(dot3v(m.rNow[0],n)>0?'up':'down')+' along '+st.bAxis:'observed: '+sc.lastUp+' of 10 up'));
  lab(ctx,W,H,G.meas.cx,G.meas.cy+(m.na===1?G.meas.R+24:G.meas.R*1.62),phaseTxt,sc.phase==='observed'?COL.pos:COL.dim,LAB_FONT,'center','middle');
  /* the counts against P(up) at the moment of measurement */
  const hb=G.hist;
  axesT(ctx,hb,0,2,0,1,{xticks:[],yticks:[0,0.5,1],title:fitTitle(hb,'up and down along '+st.bAxis+', against ½(1 + r·n̂)','against the Born rule')});
  { const bw=Math.min(44,hb.w*0.2), x1=px(hb,0.6,0,2), x2=px(hb,1.4,0,2);
    const f1=m.frac, f2=1-m.frac;
    if(m.nObs>0){ ctx.fillStyle=COL.pos; ctx.fillRect(x1-bw/2,py(hb,f1,0,1),bw,hb.y1-py(hb,f1,0,1)); ctx.fillStyle=COL.neg; ctx.fillRect(x2-bw/2,py(hb,f2,0,1),bw,hb.y1-py(hb,f2,0,1)); }
    /* the law's marks, then the values over them */
    ctx.beginPath(); ctx.moveTo(x1-bw/2-7,py(hb,m.pUp,0,1)); ctx.lineTo(x1+bw/2+7,py(hb,m.pUp,0,1)); ctx.moveTo(x2-bw/2-7,py(hb,1-m.pUp,0,1)); ctx.lineTo(x2+bw/2+7,py(hb,1-m.pUp,0,1));
    ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
    if(m.nObs>0){ barVal(ctx,W,H,x1,py(hb,f1,0,1),hb,String(sc.up),COL.pos,py(hb,m.pUp,0,1)); barVal(ctx,W,H,x2,py(hb,f2,0,1),hb,String(sc.dn),COL.neg,py(hb,1-m.pUp,0,1)); }
    else lab(ctx,W,H,hb.x+hb.w/2,freeY(hb,[py(hb,m.pUp,0,1),py(hb,1-m.pUp,0,1)]),'none yet',COL.dim,SM_FONT,'center','middle');     /* the top unless a mark is there: the 0.5 marks own the middle */
    ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.fillStyle=COL.pos; ctx.fillText('↑'+st.bAxis.toLowerCase(),x1,hb.y1+4); ctx.fillStyle=COL.neg; ctx.fillText('↓'+st.bAxis.toLowerCase(),x2,hb.y1+4); }
  /* the timer: the delay, and how far through it the field has turned the state */
  const tb=G.timer;
  if(st.bField){
    frame(ctx,tb,COL.edge);
    const f=st.bDelay>0?clamp(sc.tau/st.bDelay,0,1):1;
    ctx.fillStyle=shade(COL.live,0.7); ctx.fillRect(tb.x+1,tb.y+1,Math.max(0,(tb.w-2)*(sc.phase==='observed'?1:(sc.phase==='timing'?f:0))),tb.h-2);
    /* short lines: the column is narrow and the readout owns its right */
    lab(ctx,W,H,tb.x,tb.y-10,'delay '+fmt(st.bDelay,2)+' ns',COL.text,SM_FONT,'left','middle');
    lab(ctx,W,H,tb.x,tb.y1+11,'t = '+fmt(sc.phase==='observed'?st.bDelay:sc.tau,3)+' ns',COL.live,SM_FONT,'left','middle');
    lab(ctx,W,H,tb.x,tb.y1+26,'turns '+fmt(m.turnAtMeasure/DEG,0)+'° about z',COL.dim,SM_FONT,'left','middle');
  } else { lab(ctx,W,H,tb.x,tb.y,'no field:',COL.dim,SM_FONT,'left','middle'); lab(ctx,W,H,tb.x,tb.y+15,'measured at once',COL.dim,SM_FONT,'left','middle'); }
  /* the state written in the chosen basis */
  const E=G.eqs;
  if(E.h>=30){
    const fs=G.narrow?13:15.5, ex=E.x+(G.narrow?70:84);
    lab(ctx,W,H,E.x,E.y+2,'in the '+st.bBasis+' basis'+(st.bGlobal?', global phase shown':''),COL.dim,SM_FONT,'left','middle');
    /* the row names are separate texts, the equations start at one x */
    lab(ctx,W,H,E.x,E.y+22,'prepared',COL.dim,LAB_FONT,'left','middle');
    rich(ctx,ex,E.y+26,eqRuns(m.eqPrep,st.bBasis,'|ψ⟩',st.bGlobal),fs,'#e9e9f0','left',true);
    if(E.h>=56){ lab(ctx,W,H,E.x,E.y+48,sc.phase==='observed'?'after it':'now',COL.dim,LAB_FONT,'left','middle');
      rich(ctx,ex,E.y+52,eqRuns(m.eqNow,st.bBasis,'|ψ⟩',st.bGlobal),fs,COL.pos,'left',true); }
  }
  /* the fringe: what a measurement after a delay t sees, for this field */
  const fb=G.panelOff?null:G.fringe;
  if(fb){
    const ax=st.bAxis;
    axesT(ctx,fb,0,BL.DELAY_MAX,0,1,{xticks:[0,0.25,0.5,0.75,1],yticks:[0,0.5,1],xlab:'the delay t (ns)',
      xfmt:v=>v===0?'0':fmt(v,2),yfmt:v=>v===0?'0':fmt(v,1),        /* a bare 0 keeps the corner ticks apart */
      title:fitTitle(fb,'P(up along '+ax+') after a delay t: ½(1 + n̂·R_z(ωt) r)','P(up along '+ax+') against the delay')});
    const xs=m.fringe.map(q=>q[0]), ys=m.fringe.map(q=>q[1]);
    if(st.bField){ polyline(ctx,fb,xs,ys,0,BL.DELAY_MAX,0,1,COL.ref,2.2); vCursor(ctx,fb,st.bDelay,0,BL.DELAY_MAX); }
    else { polyline(ctx,fb,xs,ys,0,BL.DELAY_MAX,0,1,mix(COL.bg,COL.ref,0.45),1.4,[5,4]); polyline(ctx,fb,[0,BL.DELAY_MAX],[m.pFlat,m.pFlat],0,BL.DELAY_MAX,0,1,COL.ref,2.2); }
    if(m.nObs>0){ const xm=st.bField?st.bDelay:0.02; errBar(ctx,fb,xm,m.frac,m.fracSd,0,BL.DELAY_MAX,0,1,COL.pos); mark(ctx,px(fb,xm,0,BL.DELAY_MAX),py(fb,m.frac,0,1),'o',COL.pos,4); }
    /* the legend names the measured point exactly when it is drawn (it listed
       it before any observation with the field on, and never without, looked at) */
    const leg=st.bField?[[COL.ref,'the law, for this field']]:[[COL.ref,'no field: flat'],[mix(COL.bg,COL.ref,0.45),'with the field on (dashed)']];
    if(m.nObs>0) leg.push([COL.pos,'measured here ± 1σ']);
    legendAuto(ctx,fb,leg);
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function blochReadout(M){
  const m=M.B, st=M.st, sc=m.sc;
  let s=hd('the prepared state')+rrow('&theta;, &phi;',degs(st.bTheta)+', '+degs(st.bPhi))+rrow('r = (x, y, z)',m.r0.map(v=>fmt(v,3)).join(', '))
    +rrow('|&psi;&rang; = cos(&theta;/2)|&uarr;&rang; + e<sup>i&phi;</sup> sin(&theta;/2)|&darr;&rang;',fmt(Math.cos(st.bTheta/2),3)+', '+fmt(Math.sin(st.bTheta/2),3));
  s+=hd('the field (an electron)')+(st.bField?rrow('B = s B<sub>0</sub>',sigf(m.BmT,4)+' mT')+rrow('f = |&gamma;<sub>e</sub>|B/2&pi;',sigf(m.fGHz,4)+' GHz')
      +rrow('turned by the measurement',fmt(m.turnAtMeasure/DEG,1)+'&deg;'):rrow('field','off'));
  s+=hd('measured along '+st.bAxis)+rrow('P(up) = &frac12;(1 + r&middot;n&#770;)',fmt(m.pUp,4),'good')+rrow('atoms',String(m.na))
    +rrow('up, down',sc.up+', '+sc.dn)+rrow('fraction up &plusmn; &sigma;',m.nObs?fmt(m.frac,3)+' &plusmn; '+fmt(m.fracSd,3):'&mdash;')
    +rrow('stage',sc.phase==='prepared'?'prepared':(sc.phase==='timing'?'timing, t = '+fmt(sc.tau,3)+' ns':'observed'));
  return s;
}
function blochEq(M){ return ['<span class="hl">|&psi;&rang; = cos(&theta;/2)|&uarr;&rang; + e<sup>i&phi;</sup> sin(&theta;/2)|&darr;&rang;</span> &nbsp;&middot;&nbsp; &phi;(t) = &phi;<sub>0</sub> + &omega;t, &nbsp; &omega; = |&gamma;<sub>e</sub>|B &nbsp;&middot;&nbsp; P(&uarr;<sub>n</sub>) = &frac12;(1 + r&middot;n&#770;)',
  'two angles fix the state; a field along z only turns &phi;, and what a measurement sees depends on where the turning has got to'];}
function blochTag(M){ const st=M.st; return '<b>the Bloch sphere</b> — measured along '+st.bAxis+', '+(st.bAtoms===10?'ten atoms':'one atom')+(st.bField?', field on':', no field')+(st.running?'':', paused'); }
const INFO_BLOCH='PhET&rsquo;s Bloch Sphere screen puts a spin&rsquo;s state on a sphere: the polar angle &theta; sets how much of it is up, cos&sup2;(&theta;/2), and the '
  +'azimuth &phi; is the relative phase between up and down, which no z measurement can see. Measure along an axis n&#770; and the answer is up with '
  +'probability &frac12;(1 + r&middot;n&#770;); afterwards the state IS up or down along n&#770;, whatever it was. Turn on the field and the state precesses about z '
  +'during the measurement delay &mdash; &theta; stays, &phi; turns &mdash; so a z measurement is blind to the field while an x or y measurement oscillates '
  +'with the delay. That is how a spin is used as a clock. The field is PhET&rsquo;s abstract unit made real: an electron in B<sub>0</sub> = 35.68 mT '
  +'turns once a nanosecond. Choose one atom or ten, pick the axis, press observe (or start), then reprepare. Drag the canvas to turn the spheres; '
  +'the basis chips rewrite the same state in x, y or z.';
const DERIV_BLOCH='<h4>the state, its precession, its measurement</h4>'
  +EQ(1,'|&psi;&rang; = cos'+FR('&theta;','2')+'|&uarr;&rang; + e<sup>i&phi;</sup> sin'+FR('&theta;','2')+'|&darr;&rang;, &nbsp; r = (sin&theta; cos&phi;, sin&theta; sin&phi;, cos&theta;)')
  +EQ(2,'H = '+FR('&#8463;&omega;','2')+'&sigma;<sub>z</sub>, &nbsp; U(t) = e<sup>&minus;i&omega;t&sigma;<sub>z</sub>/2</sup> &nbsp;&rArr;&nbsp; &phi;(t) = &phi;<sub>0</sub> + &omega;t')
  +EQ(3,'&omega;/2&pi; = |&gamma;<sub>e</sub>|B/2&pi; = |g<sub>e</sub>|&mu;<sub>B</sub>B/h = 28.025 GHz/T &times; B')
  +EQ(4,'P(&uarr;<sub>n</sub>) = |&lang;&uarr;<sub>n</sub>|&psi;&rang;|&sup2; = &frac12;(1 + r&middot;n&#770;) = cos&sup2;(&Theta;/2)')
  +EQ(5,'|&uarr;<sub>y</sub>&rang; = (|&uarr;&rang; + i|&darr;&rang;)/&radic;2 &nbsp;&rArr;&nbsp; |+X&rang; &prop; |&uarr;<sub>y</sub>&rang; + e<sup>i&pi;/2</sup>|&darr;<sub>y</sub>&rang;')
  +'<p>The precession is an exact rotation of the prepared vector, never an integrated one; selfTest checks it against U(t) acting on the '
  +'ket and against scipy&rsquo;s matrix exponential. PhET&rsquo;s Y-basis equation prints 1.5&pi; for the +X state in [5], which rebuilds &minus;X '
  +'with PhET&rsquo;s own +Y; every equation here is rebuilt into its state in selfTest.</p>'
  +'<div class="cite">pins: three precessions against scipy expm (Bloch vector, U, P(up) on x, y, z); +X after the default 0.75 ns is &minus;Y, so a y '
  +'measurement is ALWAYS down; the equation in three bases for three states; B<sub>0</sub> = 35.6825 mT; 10 000 atoms, 3545 up along x &mdash; derive.py</div>';
