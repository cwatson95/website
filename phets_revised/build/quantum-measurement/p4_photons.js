
/* ================================================================== *
 *  THE PHOTONS view (PhET's Photons screen)                           *
 * ================================================================== */
const PH_EXT={xmin:-0.215,xmax:0.175,ymin:-0.175,ymax:0.285};
function presetName(k){ return {vertical:'vertical (V)',horizontal:'horizontal (H)',fortyFive:'45°',unpolarized:'unpolarized',custom:'custom'}[k]; }
function photonsModel(st){
  const ps=PHOT[st.phMode], ang=photonAngle(st);
  const m={ps, mode:st.phMode, ang, unpol:ang===null};
  m.pv=ang===null?0.5:pV(ang); m.ph=1-m.pv;
  m.expect=ang===null?0:expectP(ang);            /* the unpolarized mixture's is 0 */
  if(st.phMode==='single'){ m.NV=ps.nV; m.NH=ps.nH; }
  else { m.NV=ps.avgV.value; m.NH=ps.avgH.value; }
  m.N=m.NV+m.NH;
  m.fracV=m.N>0?m.NV/m.N:NaN;
  m.avgPol=m.N>0?(m.NV-m.NH)/m.N:NaN;
  /* the spread of the mean of N +-1 outcomes: sqrt((1 - <P>^2)/N) (counts only) */
  m.avgSd=st.phMode==='single'&&m.N>0?Math.sqrt(Math.max(0,1-m.expect*m.expect)/m.N):NaN;
  m.fracSd=st.phMode==='single'&&m.N>0?Math.sqrt(m.pv*(1-m.pv)/m.N):NaN;
  m.inFlight=ps.photons.length;
  m.capped=st.phMode==='single'&&(ps.nV>=PH.CAP||ps.nH>=PH.CAP);
  return m;
}
function photonsGeo(ctx,W,H,Cap){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?18:56;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,Cap.full,Cap.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  const upH=Math.max(150,Math.min(narrow?260:390,avail*(narrow?0.68:0.62)));
  const dialR=narrow?40:Math.min(62,upH*0.17);
  const dial={cx:left+dialR+8, cy:top+dialR+30, r:dialR};
  const appX=left+2*dialR+(narrow?30:52);
  const appW=narrow?Math.min(rightTop-appX,upH*0.95):Math.min(470,(rightTop-appX)*0.56);
  const app=box(appX,top,appW,upH);
  const histX=app.x1+(narrow?20:46);
  const hist=box(histX,top+18,Math.max(90,rightTop-histX),Math.max(80,upH*0.52));
  const lineB=box(hist.x,hist.y1+58,hist.w,22);
  const lowTop=top+upH+48, lowH=fit.capY-16-lowTop-18;          /* no floor: skipped when it does not fit */
  const malus=box(left+34,lowTop,Math.min(narrow?W-18-left-34:470,(narrow?W-18:W-26)-left-34),lowH);
  return {narrow,top,left,fit,dial,app,hist,lineB,malus,map:worldFitUp(app,PH_EXT,0)};
}
function photonsCaption(M){
  const m=M.P, st=M.st, q=st.phBehavior==='quantum';
  const how=q?'Quantum: past the splitter each photon is drawn on BOTH paths, each as bright as its probability, and it collapses onto one at the detectors.'
             :'Classical: each photon takes one path at the splitter, V with probability sin²θ.';
  const src=m.unpol?'Unpolarized: every photon has its own random angle, so half go each way.':'Polarized at θ = '+fmt(m.ang,0)+'° from horizontal: P(V) = sin²θ = '+fmt(m.pv,3)+'.';
  return {full:'True aspect, PhET’s model units: the arms from the splitter to the two detectors are equal (0.2), so a photon arrives 1.167 s after it leaves the laser, whichever way it goes. '+src+' '+how,
          short:src+' True aspect; equal arms.'};
}
function drawPhotons(ctx,W,H,M){
  const m=M.P, st=M.st, ps=m.ps, Cap=photonsCaption(M), G=photonsGeo(ctx,W,H,Cap), map=G.map;
  const X=map.X, Y=map.Y, s=map.s, q=st.phBehavior==='quantum';
  /* the polarization dial: looking along the beam */
  const D=G.dial;
  ctx.beginPath(); ctx.arc(D.cx,D.cy,D.r,0,TAU); ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(D.cx-D.r-6,D.cy); ctx.lineTo(D.cx+D.r+6,D.cy); ctx.moveTo(D.cx,D.cy-D.r-6); ctx.lineTo(D.cx,D.cy+D.r+6);
  ctx.strokeStyle=COL.faint; ctx.lineWidth=1; ctx.stroke();
  lab(ctx,W,H,D.cx+D.r+10,D.cy,'H',COL.neg,'italic 12px Georgia, serif','left','middle');
  lab(ctx,W,H,D.cx,D.cy-D.r-12,'V',COL.pos,'italic 12px Georgia, serif','center','middle');
  if(m.unpol){
    for(let k=0;k<12;k++){ const a=k*15*DEG, c=Math.cos(a)*D.r*0.92, sn=Math.sin(a)*D.r*0.92;
      ctx.beginPath(); ctx.moveTo(D.cx-c,D.cy+sn); ctx.lineTo(D.cx+c,D.cy-sn); ctx.strokeStyle=shade(COL.live,0.45); ctx.lineWidth=1.2; ctx.stroke(); }
  } else {
    const a=m.ang*DEG, c=Math.cos(a)*D.r, sn=Math.sin(a)*D.r;
    ctx.beginPath(); ctx.moveTo(D.cx,D.cy); ctx.lineTo(D.cx+c,D.cy); ctx.moveTo(D.cx+c,D.cy); ctx.lineTo(D.cx+c,D.cy-sn);
    ctx.setLineDash([3,3]); ctx.strokeStyle=COL.struct; ctx.lineWidth=1; ctx.stroke(); ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(D.cx-c,D.cy+sn); ctx.lineTo(D.cx+c,D.cy-sn); ctx.strokeStyle=COL.live; ctx.lineWidth=2.4; ctx.stroke();
    mark(ctx,D.cx+c,D.cy-sn,'o',COL.live,3.5); mark(ctx,D.cx-c,D.cy+sn,'o',COL.live,3.5);
  }
  lab(ctx,W,H,D.cx,D.cy+D.r+16,m.unpol?'random for each photon':'θ = '+fmt(m.ang,0)+'°',COL.live,LAB_FONT,'center','middle');
  lab(ctx,W,H,D.cx,D.cy+D.r+32,'along the beam',COL.dim,SM_FONT,'center','middle');
  if(!G.narrow) lab(ctx,W,H,D.cx,D.cy+D.r+46,'(drag to set)',COL.faint,SM_FONT,'center','middle');
  /* the apparatus */
  const beam=(pts,col,lw)=>{ ctx.beginPath(); pts.forEach((p,i)=>{ if(i) ctx.lineTo(X(p[0]),Y(p[1])); else ctx.moveTo(X(p[0]),Y(p[1])); }); ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.stroke(); };
  beam([[PH.X0,0],[0,0],[0,PH.DV]],'#1d2536',Math.max(2,PH.BEAM_W*s)); beam([[0,0],[PH.MX,0],[PH.MX,PH.DH]],'#1d2536',Math.max(2,PH.BEAM_W*s));
  /* the laser */
  ctx.fillStyle='#232a3a'; ctx.fillRect(X(-0.205),Y(0.022),0.055*s,0.044*s); frame(ctx,box(X(-0.205),Y(0.022),0.055*s,0.044*s),COL.struct);
  lab(ctx,W,H,X(-0.178),Y(-0.045),st.phMode==='single'?'laser (click)':'laser',COL.text,SM_FONT,'center','middle');
  /* the polarizing beam splitter: a cube with its diagonal surface */
  const c0=X(-PH.PBS), c1=Y(PH.PBS), cw=2*PH.PBS*s;
  ctx.fillStyle='rgba(90,200,224,0.10)'; ctx.fillRect(c0,c1,cw,cw); frame(ctx,box(c0,c1,cw,cw),COL.struct);
  ctx.beginPath(); ctx.moveTo(X(-PH.PBS),Y(-PH.PBS)); ctx.lineTo(X(PH.PBS),Y(PH.PBS)); ctx.strokeStyle=COL.struct; ctx.lineWidth=2; ctx.stroke();
  lab(ctx,W,H,X(0),Y(-PH.PBS)+14,'polarizing beam splitter',COL.dim,SM_FONT,'center','middle');
  /* the mirror, on x + y = 0.11 */
  const mh=0.0475/Math.SQRT2;
  ctx.beginPath(); ctx.moveTo(X(PH.MX-mh),Y(mh)); ctx.lineTo(X(PH.MX+mh),Y(-mh)); ctx.strokeStyle='#c9d2e2'; ctx.lineWidth=3; ctx.stroke();
  lab(ctx,W,H,X(PH.MX-mh)-4,Y(mh)-4,'mirror',COL.dim,SM_FONT,'right','middle');   /* left of it: the histogram's ticks own the right */
  /* the detectors: a cup whose mouth is the detection line */
  const det=(x0,y0,dir,name,val,col)=>{
    const hw=PH.AP/2, dep=0.055*dir, bx=box(X(x0-hw),Math.min(Y(y0),Y(y0+dep)),PH.AP*s,Math.abs(dep)*s);
    ctx.fillStyle=shade(col,0.22); ctx.fillRect(bx.x,bx.y,bx.w,bx.h); frame(ctx,bx,col);
    lab(ctx,W,H,bx.x+bx.w/2,bx.y+bx.h/2,name,col,'italic 12px Georgia, serif','center','middle');
    lab(ctx,W,H,bx.x1+8,bx.y+bx.h/2,val,col,'12px -apple-system, sans-serif','left','middle');
  };
  const vtxt=st.phMode==='single'?String(ps.nV):sigf(ps.avgV.value,3)+'/s', htxt=st.phMode==='single'?String(ps.nH):sigf(ps.avgH.value,3)+'/s';
  /* the photons (the detectors are drawn after them, so a photon that has
     reached one disappears into it rather than covering its letter) */
  const bright='#f4f8e8';
  for(const ph of ps.photons){
    const d=PH.V*(ps.t-ph.t0), L=photonLegs(ph.y0);
    if(d<0) continue;
    const r=Math.max(2,0.0034*s);
    if(ph.route===null&&d>L.d1&&q){                /* quantum: on both paths, each as bright as its probability */
      const pv=pV(ph.ang), a=photonPos(ph,d,'V'), b=photonPos(ph,d,'H');
      mark(ctx,X(a[0]),Y(a[1]),'o',mix(COL.bg,bright,0.12+0.88*pv),r); mark(ctx,X(b[0]),Y(b[1]),'o',mix(COL.bg,bright,0.12+0.88*(1-pv)),r);
    } else {
      const p=photonPos(ph,d,ph.route||'H');
      mark(ctx,X(p[0]),Y(p[1]),'o',ph.counted?(ph.route==='V'?COL.pos:COL.neg):bright,r);
    }
  }
  det(0,PH.DV,1,'V',vtxt,COL.pos); det(PH.MX,PH.DH,-1,'H',htxt,COL.neg);
  lab(ctx,W,H,G.app.x+4,G.app.y1+14,'true aspect · PhET’s model units · '+(st.phMode==='single'?'one photon at a time':fmt(st.phRate,0)+' photons/s'),COL.faint,SM_FONT,'left','middle');
  /* the detected fractions against sin^2 and cos^2 */
  const hb=G.hist;
  axesT(ctx,hb,0,2,0,1,{xticks:[],yticks:[0,0.25,0.5,0.75,1],title:fitTitle(hb,st.phMode==='single'?'counted: V and H, against sin²θ, cos²θ':'rates: V and H, against sin²θ, cos²θ','V and H against the law')});
  { const bw=Math.min(50,hb.w*0.2), x1=px(hb,0.6,0,2), x2=px(hb,1.4,0,2), f1=m.NV/m.N, f2=m.NH/m.N;
    if(m.N>0){ ctx.fillStyle=COL.pos; ctx.fillRect(x1-bw/2,py(hb,f1,0,1),bw,hb.y1-py(hb,f1,0,1)); ctx.fillStyle=COL.neg; ctx.fillRect(x2-bw/2,py(hb,f2,0,1),bw,hb.y1-py(hb,f2,0,1)); }
    /* the law's marks, then the values over them */
    ctx.beginPath(); ctx.moveTo(x1-bw/2-7,py(hb,m.pv,0,1)); ctx.lineTo(x1+bw/2+7,py(hb,m.pv,0,1)); ctx.moveTo(x2-bw/2-7,py(hb,m.ph,0,1)); ctx.lineTo(x2+bw/2+7,py(hb,m.ph,0,1));
    ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
    if(m.N>0){ barVal(ctx,W,H,x1,py(hb,f1,0,1),hb,st.phMode==='single'?String(m.NV):sigf(m.NV,3)+'/s',COL.pos,py(hb,m.pv,0,1));
               barVal(ctx,W,H,x2,py(hb,f2,0,1),hb,st.phMode==='single'?String(m.NH):sigf(m.NH,3)+'/s',COL.neg,py(hb,m.ph,0,1)); }
    else lab(ctx,W,H,hb.x+hb.w/2,freeY(hb,[py(hb,m.pv,0,1),py(hb,m.ph,0,1)]),st.phMode==='single'?'no photons yet: click the laser':'no detections yet',COL.dim,SM_FONT,'center','middle');
    ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.fillStyle=COL.pos; ctx.fillText('V',x1,hb.y1+4); ctx.fillStyle=COL.neg; ctx.fillText('H',x2,hb.y1+4); }
  /* the average polarization, (N_V - N_H)/N, on its line from -1 (H) to +1 (V) */
  const lb=G.lineB;
  lab(ctx,W,H,lb.x,lb.y-16,'average polarization '+(m.N>0?fmt0(m.avgPol,3):'—')+'   (expected '+fmt0(m.expect,3)+')',COL.text,'italic 12.5px Georgia, serif','left','middle');
  ctx.beginPath(); ctx.moveTo(lb.x,lb.y+lb.h/2); ctx.lineTo(lb.x1,lb.y+lb.h/2); ctx.strokeStyle=COL.struct; ctx.lineWidth=1.2; ctx.stroke();
  for(const v of [-1,-0.5,0,0.5,1]){ const x=lb.x+lb.w*(v+1)/2; ctx.beginPath(); ctx.moveTo(x,lb.y+lb.h/2-5); ctx.lineTo(x,lb.y+lb.h/2+5); ctx.stroke();
    lab(ctx,W,H,x,lb.y1+9,v===-1?'−1 (H)':(v===1?'+1 (V)':String(v)),COL.dim,SM_FONT,'center','middle'); }
  { const x=lb.x+lb.w*(m.expect+1)/2; ctx.beginPath(); ctx.moveTo(x,lb.y-2); ctx.lineTo(x,lb.y1+2); ctx.strokeStyle=COL.ref; ctx.lineWidth=2.4; ctx.stroke(); }
  if(m.N>0){ const x=lb.x+lb.w*(m.avgPol+1)/2; mark(ctx,x,lb.y+lb.h/2,'d',COL.pos,4.5);
    if(isFinite(m.avgSd)){ const e=lb.w*m.avgSd/2; ctx.beginPath(); ctx.moveTo(Math.max(lb.x,x-e),lb.y+lb.h/2); ctx.lineTo(Math.min(lb.x1,x+e),lb.y+lb.h/2); ctx.strokeStyle=COL.pos; ctx.lineWidth=2; ctx.stroke(); } }
  /* Malus: P(V) against theta, the law and where this beam sits on it */
  const mb=G.malus;
  if(mb.h>=55){
    const yt=[0,0.5,1];
    axesT(ctx,mb,0,90,0,1,{xticks:[0,15,30,45,60,75,90],yticks:yt,xlab:mb.h>=90?'θ from horizontal (°)':'',title:fitTitle(mb,'P(V) = sin²θ and P(H) = cos²θ: Malus at the splitter','Malus at the splitter')});
    const xs=[], s2=[], c2=[]; for(let i=0;i<=90;i++){ xs.push(i); s2.push(pV(i)); c2.push(1-pV(i)); }
    polyline(ctx,mb,xs,s2,0,90,0,1,COL.ref,2); polyline(ctx,mb,xs,c2,0,90,0,1,COL.ref,1.5,[5,4]);
    /* the measured point in both modes (the rates' fraction in a beam, where
       the counts' sigma does not apply); the legend names only what is drawn
       (it listed the point in the beam and unpolarized views, looked at) */
    const shown=!m.unpol&&m.N>0;
    if(!m.unpol){ vCursor(ctx,mb,m.ang,0,90); if(shown){ const Xp=px(mb,m.ang,0,90), Yp=py(mb,m.fracV,0,1);
      if(isFinite(m.fracSd)) errBar(ctx,mb,m.ang,m.fracV,m.fracSd,0,90,0,1,COL.pos); mark(ctx,Xp,clamp(Yp,mb.y,mb.y1),'o',COL.pos,4); } }
    const leg=[[COL.ref,'P(V) = sin²θ'],[mix(COL.bg,COL.ref,0.7),'P(H) = cos²θ (dashed)']];
    if(shown) leg.push([COL.pos,st.phMode==='single'?'measured V fraction ± 1σ':'measured V fraction']);
    legendAuto(ctx,mb,leg);
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
function photonsReadout(M){
  const m=M.P, st=M.st, one=st.phMode==='single';
  let s=hd('the source')+rrow('mode',one?'one photon at a time':fmt(st.phRate,0)+' photons/s')+rrow('polarization',presetName(st.phPreset)+(m.unpol?'':' = '+fmt(m.ang,0)+'&deg;'))
    +rrow('behaviour',st.phBehavior);
  s+=hd('the odds')+rrow('P(V) = sin&sup2;&theta;',fmt(m.pv,4),'good')+rrow('P(H) = cos&sup2;&theta;',fmt(m.ph,4))
    +rrow('&lang;P&rang; = P(V) &minus; P(H) = &minus;cos 2&theta;',fmt0(m.expect,4));
  s+=hd(one?'counted':'rates (1-s average)');
  if(one) s+=rrow('V, H',m.NV+', '+m.NH+(m.capped?' (PhET caps at 999)':''),m.capped?'bad':'')+rrow('V fraction &plusmn; &sigma;',m.N?fmt(m.fracV,3)+' &plusmn; '+fmt(m.fracSd,3):'&mdash;');
  else s+=rrow('V, H',sigf(m.NV,3)+'/s, '+sigf(m.NH,3)+'/s')+rrow('V fraction',m.N?fmt(m.fracV,3):'&mdash;');
  s+=rrow('average polarization (N<sub>V</sub>&minus;N<sub>H</sub>)/N',m.N?fmt0(m.avgPol,3):'&mdash;','good')+rrow('photons in flight',String(m.inFlight));
  return s;
}
function photonsEq(M){ return ['<span class="hl">P(V) = sin&sup2;&theta;, &nbsp; P(H) = cos&sup2;&theta;</span> &nbsp;&middot;&nbsp; &lang;P&rang; = P(V) &minus; P(H) = &minus;cos 2&theta; &nbsp;&middot;&nbsp; P&#772; = (N<sub>V</sub> &minus; N<sub>H</sub>)/N',
  'Malus&rsquo;s law, one photon at a time: the splitter never splits a photon&rsquo;s energy &mdash; it sends the whole photon one way, with these odds']; }
function photonsTag(M){ const st=M.st; return '<b>the photons</b> — '+(st.phMode==='single'?'single photons':'a beam')+', '+presetName(st.phPreset)+', '+st.phBehavior+(st.running?'':', paused')+(st.speed==='slow'?', slow motion':''); }
const INFO_PHOTONS='PhET&rsquo;s Photons screen sends light through a polarizing beam splitter, a cube whose diagonal reflects vertically polarized '
  +'light up to one detector and passes horizontally polarized light on to a mirror and the other. A beam polarized at &theta; is split in the ratio '
  +'sin&sup2;&theta; : cos&sup2;&theta;, which is Malus&rsquo;s law. Turn the source down to one photon at a time and the law survives, but only as odds: '
  +'each photon arrives whole at one detector or the other, never half at each, with probability sin&sup2;&theta; of V. The two behaviours are two '
  +'stories about the same statistics. In the classical one the photon picks its path at the splitter. In the quantum one it goes both ways, '
  +'drawn at each path&rsquo;s probability, and the choice is made only at the detectors. The two arms are the same length, so both halves arrive '
  +'together. Nothing downstream of one splitter can tell the stories apart. The average polarization, (N<sub>V</sub> &minus; N<sub>H</sub>)/N, '
  +'wanders toward &minus;cos 2&theta; as the counts grow. Click the laser for a photon, or drag the dial to set the angle.';
const DERIV_PHOTONS='<h4>one photon at a splitter</h4>'
  +EQ(1,'|&theta;&rang; = cos&theta; |H&rang; + sin&theta; |V&rang;')
  +EQ(2,'P(V) = |&lang;V|&theta;&rang;|&sup2; = sin&sup2;&theta;, &nbsp; P(H) = cos&sup2;&theta;')
  +EQ(3,'&lang;P&rang; = (+1)P(V) + (&minus;1)P(H) = &minus;cos 2&theta;, &nbsp; &sigma;<sub>P&#772;</sub> = &radic;((1 &minus; &lang;P&rang;&sup2;)/N)')
  +EQ(4,'<span class="rm">unpolarized:</span> &rho; = &frac12;&#120793; &nbsp;&rArr;&nbsp; P(V) = &frac12;, &nbsp; &lang;P&rang; = 0')
  +'<p>The geometry is PhET&rsquo;s: the diagonal is y = x, the mirror x + y = 0.11, the detector lines y = 0.2 and y = &minus;0.09. A photon at '
  +'height y<sub>0</sub> meets the diagonal at x = y<sub>0</sub>, and both arms from there are 0.2 &minus; y<sub>0</sub> long, so every photon arrives '
  +'(0.2 + 0.15)/0.3 = 1.167 s after leaving the laser, whichever way it goes and wherever it is in the 0.04-wide beam.</p>'
  +'<div class="cite">pins: the arms at five heights (derive.py); sin&sup2;&theta; at seven angles; 5000 photons at 30&deg;, 1236 V (4&sigma; = 122 of 1250); '
  +'5000 unpolarized, 2536 V; the 1-s averaging counter, 20.3226/s</div>';
