
/* ================================================================== *
 *  THE PRISM, THE REFLECTED FRACTION, THE SPECTRUM, THE RAINBOW       *
 * ================================================================== */
const PRISM_WORLD={xmin:-19,xmax:19,ymin:-13.3,ymax:13.3};

function prismGeo(ctx,W,H,M,st){
  const capFull='PhET’s five prism prototypes, at PhET’s own size — an equilateral triangle, '
    +'trapezoid and square of side 10 red wavelengths, and a circle and semicircle of radius 5. Every face '
    +'is met by exact intersection (a linear solve for a polygon edge, the stable quadratic root for an arc) '
    +'and crossed by vector Snell; where Snell has no solution the ray reflects instead. Segment opacity is '
    +'the power fraction. PhET’s limits are kept: '+PHET.maxSteps+' segments and a floor of '
    +PHET.powerMin+' on the power.';
  const capShort='PhET’s prism prototypes, traced by exact intersection and vector Snell.';
  const L=stageLayoutH(ctx,W,H,capFull,capShort,0,0,0);
  const map=worldFitUp(L.main,PRISM_WORLD,0.5);
  return {L:L,map:map};
}
function shapeOutline(sh,n){
  if(sh.kind==='poly') return sh.pts;
  const out=[];
  if(sh.kind==='circle'){ for(let i=0;i<=n;i++){ const a=TAU*i/n; out.push([sh.c[0]+sh.r*Math.cos(a),sh.c[1]+sh.r*Math.sin(a)]); } return out; }
  /* the semicircle: the diameter, then the arc on the `half` side */
  const a0=Math.atan2(sh.a[1]-sh.c[1],sh.a[0]-sh.c[0]);
  const a1=Math.atan2(sh.b[1]-sh.c[1],sh.b[0]-sh.c[0]);
  const mid=Math.atan2(sh.half[1],sh.half[0]);
  let s=a1, e=a0;
  /* walk from b to a the way that passes through the `half` direction */
  let span=e-s; while(span<0) span+=TAU; while(span>TAU) span-=TAU;
  let probe=s+span/2; let dmid=Math.atan2(Math.sin(probe-mid),Math.cos(probe-mid));
  if(Math.abs(dmid)>PI/2){ s=a0; e=a1; span=e-s; while(span<0) span+=TAU; }
  out.push(sh.a.slice());
  for(let i=0;i<=n;i++){ const a=s+span*i/n; out.push([sh.c[0]+sh.r*Math.cos(a),sh.c[1]+sh.r*Math.sin(a)]); }
  return out;
}
function drawPrism(ctx,W,H,M,st){
  const G=prismGeo(ctx,W,H,M,st), L=G.L, map=G.map, P=M.prism;
  const X0=map.X(PRISM_WORLD.xmin),X1=map.X(PRISM_WORLD.xmax);
  const Ytop=map.Y(PRISM_WORLD.ymax),Ybot=map.Y(PRISM_WORLD.ymin);
  ctx.fillStyle=mediumFill(P.nOut); ctx.fillRect(X0,Ytop,X1-X0,Ybot-Ytop);
  frame(ctx,box(X0,Ytop,X1-X0,Ybot-Ytop),COL.edge);
  if(st.showProtractor) protractorW(ctx,W,H,map,11);
  const outline=shapeOutline(P.shape,72);
  worldPoly(ctx,map,outline,mediumFill(P.nIn+0.7),COL.struct,1.6);
  /* the rays */
  if(st.laserOn&&st.white) for(const g of P.groups){
    /* white light: merged segments are drawn once in white, separated ones
       one wavelength at a time (see mergeMask) */
    const mask=mergeMask(g.map(b=>b.tr),map.s);
    const ref=g[Math.floor(g.length/2)];
    for(let k=0;k<mask.length;k++){
      const r=ref.tr.segs[k];
      if(mask[k]){
        segW(ctx,map,[r[0],r[1]],[r[2],r[3]],PRISM_WORLD,
             'rgba(255,255,255,'+fmt(clamp(0.25+0.7*Math.sqrt(clamp(r[4],0,1)),0,1),3)+')',
             1.2+1.8*Math.sqrt(clamp(r[4],0,1)));
      } else for(const bnd of g){
        const sg=bnd.tr.segs[k];
        segW(ctx,map,[sg[0],sg[1]],[sg[2],sg[3]],PRISM_WORLD,beamCss(st,bnd.lam,sg[4]),1.5);
      }
    }
    /* branches that only some wavelengths have: drawn individually */
    for(const bnd of g) for(let k=mask.length;k<bnd.tr.segs.length;k++){
      const sg=bnd.tr.segs[k];
      segW(ctx,map,[sg[0],sg[1]],[sg[2],sg[3]],PRISM_WORLD,beamCss(st,bnd.lam,sg[4]),1.2);
    }
  }
  if(st.laserOn&&!st.white) for(const bnd of P.bundles){
    for(const s of bnd.tr.segs){
      segW(ctx,map,[s[0],s[1]],[s[2],s[3]],PRISM_WORLD,beamCss(st,bnd.lam,s[4]),
           1.1+2.0*Math.sqrt(clamp(s[4],0,1)));
    }
    if(st.showNormals) for(let i=0;i<bnd.tr.segs.length-1;i++){
      const s=bnd.tr.segs[i], hit=[s[2],s[3]];
      const h=shapeHit(P.shape,[hit[0]-1e-6*(s[2]-s[0]),hit[1]-1e-6*(s[3]-s[1])],
                       [s[2]-s[0],s[3]-s[1]]);
      if(!h) continue;
      seg(ctx,map,[hit[0]-2.4*h.n[0],hit[1]-2.4*h.n[1]],[hit[0]+2.4*h.n[0],hit[1]+2.4*h.n[1]],
          rgba(COL.norm,0.55),1,[3,3]);
    }
  }
  /* the laser: a drag on it SLIDES the beam here, it does not swing it.  It
     is drawn AT the beam's own origin, so the beam leaves its barrel. */
  laserW(ctx,map,P.beam.d,st.laserOn,'beam',0.5,P.beam.origins[0],0.6);
  lab(ctx,W,H,X0+9,Ytop+13,'environment: '+subLabel(st.envSub,P.nOut),rgba(COL.struct,0.95),LAB_FONT,'left');
  lab(ctx,W,H,X0+9,Ytop+29,'prism: '+subLabel(st.prismSub,P.nIn),rgba(COL.struct,0.95),LAB_FONT,'left');
  if(isFinite(P.tc))
    lab(ctx,W,H,X0+9,Ytop+45,'critical angle inside: '+fmt(P.tc*RAD,2)+'°',COL.ref,LAB_FONT,'left');
  if(st.prismId==='triangle'){
    const Dm=prismMinDeviation(P.nOut,P.nIn,P.apex);
    lab(ctx,W,H,X1-9,Ytop+13,isFinite(Dm)
        ?'minimum deviation '+fmt(Dm*RAD,2)+'° at θ₁ = '+fmt((P.apex+Dm)/2*RAD,2)+'°'
        :'a 60° apex cannot pass this index: 2θc = '+fmt(2*P.tc*RAD,2)+'°',
        isFinite(Dm)?COL.pos:COL.ref,LAB_FONT,'right');
  }
  if(st.white)
    lab(ctx,W,H,X1-9,Ytop+29,WHITE_WL.length+' wavelengths, 400–690 nm (PhET’s set); white where '
        +'they still lie within '+WHITE_MERGE_PX+' px of each other',COL.dim,SM_FONT,'right');
  drawCaption(ctx,L);
}

/* ------------------------------------------------ the reflected fraction */
function fresGeo(ctx,W,H,M,st){
  const capFull='The Fresnel equations, at the pair of indices the boundary view is set to. R and T are '
    +'POWER fractions, so R + T = 1 at every angle — the suite asserts it to 7×10⁻¹⁶ over '
    +'eight pairs and 601 angles. R_p touches zero at Brewster’s angle and nowhere else, which is why '
    +'reflected glare is polarised; past the critical angle both are exactly one. The orange rules are the '
    +'two special angles, the magenta marker is the angle the laser is set to.';
  const capShort='R and T against the angle of incidence, both polarisations. R + T = 1 everywhere.';
  return stageLayoutH(ctx,W,H,capFull,capShort,2,0.34,1);
}
function drawFres(ctx,W,H,M,st){
  const L=fresGeo(ctx,W,H,M,st), b=L.main, B=M.b, F=M.fres;
  const tcD=isFinite(B.tc)?B.tc*RAD:NaN, tbD=B.tb*RAD;
  axesRB(ctx,b,0,90,0,1,{title:titleFor(b,'reflected and transmitted power against the angle of incidence',
                                       'R and T against θ₁'),
    xlab:'angle of incidence θ₁ (degrees)',ylab:'fraction of the power',nx:7,ny:nyFor(b),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  polyline(ctx,b,F.th,F.Ts,0,90,0,1,rgba(COL.pos,0.35),1.4,[5,4]);
  polyline(ctx,b,F.th,F.Tp,0,90,0,1,rgba(COL.live,0.35),1.4,[5,4]);
  polyline(ctx,b,F.th,F.Ru,0,90,0,1,COL.unpol,1.4);
  polyline(ctx,b,F.th,F.Rs,0,90,0,1,COL.sPol,2.0);
  polyline(ctx,b,F.th,F.Rp,0,90,0,1,COL.pPol,2.0);
  /* the two special angles, clipped to the box by construction */
  const rule=(x,col,txt)=>{
    if(!isFinite(x)||x<0||x>90) return;
    polyline(ctx,b,[x,x],[0,1],0,90,0,1,rgba(col,0.8),1.2,[4,4]);
    lab(ctx,W,H,b.x+b.w*x/90+5,b.y+14,txt,col,SM_FONT,'left');
  };
  rule(tbD,COL.ref,'Brewster '+fmt(tbD,2)+'°');
  rule(tcD,COL.ref,'critical '+fmt(tcD,2)+'°');
  marker(ctx,b,0,90,0,1,st.angDeg,powerSplit(B.f,st.pol).R,COL.live);
  legendA(ctx,b,[[COL.sPol,'R_s'],[COL.pPol,'R_p'],[COL.unpol,'R unpolarised'],
                    [rgba(COL.pos,0.35),'T_s (dashed)'],[rgba(COL.live,0.35),'T_p (dashed)']]);
  if(L.bottom.length>=1) fresPhase(ctx,W,H,L.bottom[0],M,st);
  if(L.bottom.length>=2) fresRatio(ctx,W,H,L.bottom[1],M,st);
  drawCaption(ctx,L);
}
/* the phase of the reflected amplitude: pi jumps, and the TIR phase */
function fresPhase(ctx,W,H,b,M,st){
  const B=M.b, th=[],ps=[],pp=[];
  for(let i=0;i<=180;i++){
    const t=i/180*(90-1e-4)*DEG;
    const f=fresnel(B.n1,B.n2,t);
    th.push(t*RAD);
    if(f.tir){ ps.push(f.phs*RAD); pp.push(f.php*RAD); }
    else { ps.push(f.rs>=0?0:180); pp.push(f.rp>=0?0:180); }
  }
  axesRB(ctx,b,0,90,-200,200,{title:titleFor(b,'the phase of the reflected amplitude','phase of r'),
    xlab:'θ₁ (degrees)',ylab:'arg r (degrees)',nx:4,ny:nyFor(b),xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  polyline(ctx,b,th,ps,0,90,-200,200,COL.sPol,1.8);
  polyline(ctx,b,th,pp,0,90,-200,200,COL.pPol,1.8);
  lab(ctx,W,H,b.x+6,b.y1-12,B.n2>B.n1?'r_s is negative throughout: a hard reflection'
                                     :'past θc the phase slides — Goos–Hänchen',
      COL.dim,SM_FONT,'left');
}
/* R at normal incidence against the index ratio */
function fresRatio(ctx,W,H,b,M,st){
  const B=M.b, ms=[],rs=[];
  for(let i=0;i<=200;i++){ const m=0.25+2.25*i/200; ms.push(m); rs.push(Math.pow((1-m)/(1+m),2)); }
  axesRB(ctx,b,0.25,2.5,0,0.25,{title:titleFor(b,'reflection at normal incidence','R at 0°'),
    xlab:'n₂/n₁',ylab:'R(0)',nx:4,ny:nyFor(b),xfmt:t=>fmt(t,1),yfmt:t=>fmt(t,2)});
  polyline(ctx,b,ms,rs,0.25,2.5,0,0.25,COL.pos,1.8);
  const m=B.n2/B.n1;
  marker(ctx,b,0.25,2.5,0,0.25,clamp(m,0.25,2.5),Math.pow((1-m)/(1+m),2),COL.live);
  noteIn(ctx,W,H,b,'n₂/n₁ = '+fmt(m,4)+' → R(0) = '+fmt(100*Math.pow((1-m)/(1+m),2),2)+'%');
}

/* -------------------------------------------------------- the spectrum */
function specGeo(ctx,W,H,M,st){
  const capFull='PhET’s dispersion is one curve, not six: the Sellmeier index of BK7 glass blended '
    +'linearly with Edlen’s standard air so that the result passes through the substance’s stated '
    +'index at 650 nm. The blend weight is '+fmt(blendFraction(1.5),3)+' for glass and '
    +fmt(blendFraction(2.419),3)+' for diamond — nearly three times BK7’s own dispersion, so the '
    +'diamond curve is an extrapolation of the model rather than a measurement of the stone. The strip under '
    +'the axis is the true colour of each wavelength, from the CIE 1931 2° observer.';
  const capShort='Index against wavelength: PhET’s BK7-and-air blend, with the CIE colour of each wavelength.';
  return stageLayoutH(ctx,W,H,capFull,capShort,2,0.34,1);
}
function spectrumStrip(ctx,b,lamLo,lamHi,y,h){
  for(let X=b.x;X<b.x1;X+=2){
    const lam=lamLo+(lamHi-lamLo)*(X-b.x)/b.w;
    ctx.fillStyle=cssOfLinear(monoLinear(lam),monoLevel(lam));
    ctx.fillRect(X,y,2.6,h);
  }
}
function drawSpec(ctx,W,H,M,st){
  const L=specGeo(ctx,W,H,M,st), b=L.main, S=M.spec;
  const lo=PHET.lamMin, hi=PHET.lamMax;
  /* n itself spans 1.0 to 2.5 and every curve looks flat on that axis, which
     hides the one thing this view exists to say.  Plot the CHANGE from the
     reference wavelength, n(lambda) - n(650), and put the absolute index in
     the legend, where it belongs. */
  const rel={}; let nhi=0;
  const shown=[['diamond',COL.ref],['glass',COL.pos],['water',COL.struct],['mysteryB',COL.live],['air',COL.dim]];
  for(const [id] of shown){
    const n0=S.rows[id][fnIdx(S.lam,PHET.lamRed)];
    rel[id]=S.rows[id].map(v=>v-n0);
    for(const v of rel[id]) nhi=Math.max(nhi,Math.abs(v));
  }
  const nlo=-Math.ceil(nhi*100)/100*0.35, nhiR=Math.ceil(nhi*100)/100;
  axesRB(ctx,b,lo,hi,nlo,nhiR,{title:titleFor(b,'how far the index moves with wavelength, n(λ) − n(650 nm)',
                                            'n(λ) − n(650)'),
    xlab:'wavelength in vacuum (nm)',ylab:'change in index',nx:7,ny:nyFor(b),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,3)});
  /* the colour strip goes INSIDE the box: at b.y1+2 it covered the tick row */
  spectrumStrip(ctx,b,lo,hi,b.y1-9,9);
  for(const [id,col] of shown) polyline(ctx,b,S.lam,rel[id],lo,hi,nlo,nhiR,col,1.8);
  marker(ctx,b,lo,hi,nlo,nhiR,st.lamNm,
         mediumIndex(st.botSub,st.botN,st.lamNm)-mediumIndex(st.botSub,st.botN,PHET.lamRed),COL.live);
  legendA(ctx,b,shown.map(([id,c])=>[c,subById(id).name+', n = '+fmt(indexOf(subById(id).n,PHET.lamRed),4)]));
  if(L.bottom.length>=1) specDeviation(ctx,W,H,L.bottom[0],M,st);
  if(L.bottom.length>=2) specFan(ctx,W,H,L.bottom[1],M,st);
  drawCaption(ctx,L);
}
function specDeviation(ctx,W,H,b,M,st){
  const S=M.spec;
  const ds=S.dev.map(d=>isFinite(d)?d*RAD:NaN);
  let lo=Infinity,hi=-Infinity;
  for(const d of ds) if(isFinite(d)){ lo=Math.min(lo,d); hi=Math.max(hi,d); }
  if(!isFinite(lo)){
    caption(ctx,b.x,b.y+b.h/2-14,'a '+fmt(st.prismApex,0)+'° prism of this index traps the ray at '
      +'every entry angle: 2θc = '+fmt(2*criticalAngle(prismIndex(st),envIndex(st))*RAD,2)
      +'° is less than the apex angle, so there is no deviation to plot.',b.w,COL.ref,CAP_FONT);
    frame(ctx,b,COL.edge);
    return;
  }
  const pad=Math.max(0.2,(hi-lo)*0.25);
  axesRB(ctx,b,PHET.lamMin,PHET.lamMax,lo-pad,hi+pad,
    {title:titleFor(b,'deviation through a '+fmt(st.prismApex,0)+'° prism','deviation vs λ'),
     xlab:'wavelength (nm)',ylab:'deviation (degrees)',nx:4,ny:nyFor(b),xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  polyline(ctx,b,S.lam,ds,PHET.lamMin,PHET.lamMax,lo-pad,hi+pad,COL.pos,1.8);
  spectrumStrip(ctx,b,PHET.lamMin,PHET.lamMax,b.y1-7,7);
  const i4=fnIdx(S.lam,400), i7=fnIdx(S.lam,700);
  lab(ctx,W,H,b.x+b.w/2,b.y1-22,'violet is bent '+fmt(ds[i4]-ds[i7],3)+'° more than red',
      COL.dim,SM_FONT,'center');
}
/* the spread as it would land on a screen: the exit fan, drawn */
function specFan(ctx,W,H,b,M,st){
  const S=M.spec;
  frame(ctx,b,COL.edge);
  ctx.fillStyle='#aeb6c6'; ctx.font='italic 13px Georgia, serif';
  ctx.textAlign='left'; ctx.textBaseline='bottom';
  ctx.fillText(plain(titleFor(b,'the fan, and where it lands','the fan')),b.x,b.y-9);
  LABELS.push([b.x,b.y-9-15,b.x+130,b.y-9]);
  const ds=S.dev.map(d=>isFinite(d)?d:NaN);
  let lo=Infinity,hi=-Infinity;
  for(const d of ds) if(isFinite(d)){ lo=Math.min(lo,d); hi=Math.max(hi,d); }
  if(!isFinite(lo)){
    caption(ctx,b.x+8,b.y+b.h/2-7,'nothing emerges at this index.',b.w-16,COL.ref,CAP_FONT);
    return;
  }
  const ox=b.x+26, oy=b.y+b.h/2, len=b.w-64;
  const spread=Math.max(hi-lo,1e-6);
  const gain=clamp((b.h*0.42)/(len*Math.tan(spread/2)+1e-9),1,60);
  for(let i=0;i<S.lam.length;i++){
    if(!isFinite(ds[i])) continue;
    const a=(ds[i]-(lo+hi)/2)*gain;
    ctx.strokeStyle=cssOfLinear(monoLinear(S.lam[i]),monoLevel(S.lam[i]));
    ctx.lineWidth=1.6;
    ctx.beginPath(); ctx.moveTo(ox,oy); ctx.lineTo(ox+len*Math.cos(a),oy-len*Math.sin(a)); ctx.stroke();
  }
  dot(ctx,ox,oy,3.5,COL.struct,'#fff',1);
  lab(ctx,W,H,b.x+b.w/2,b.y1-10,'angles exaggerated ×'+fmt(gain,1)+' — the true spread is '
      +fmt((hi-lo)*RAD,3)+'°',COL.ref,SM_FONT,'center');
}

/* --------------------------------------------------------- the rainbow */
function bowGeo(ctx,W,H,M,st){
  const capFull='A sphere of water, lit by parallel light. Every ray is refracted in, reflected k times '
    +'inside, and refracted out; the deviation D depends on where it struck, and it is STATIONARY at '
    +'cos²θ = (n²−1)/(k²+2k). Rays pile up at that angle and nowhere else, which is the bow. '
    +'Because n depends on the wavelength the pile-up angle does too, and the bow is coloured: '
    +fmt(M.bow.bows[1].ang[700],2)+'° for red, '+fmt(M.bow.bows[1].ang[400],2)
    +'° for violet. The drop is drawn at true shape; the rays are geometric, so there are no '
    +'supernumerary bows here.';
  const capShort='Descartes’ stationary deviation in a water drop — the rays pile up at the bow angle.';
  return stageLayoutH(ctx,W,H,capFull,capShort,2,0.34,1);
}
function drawBow(ctx,W,H,M,st){
  const L=bowGeo(ctx,W,H,M,st), b=L.main, Wb=M.bow;
  const ext={xmin:-3.9,xmax:3.9,ymin:-1.39,ymax:1.39};
  const map=worldFitUp(b,ext,0.05);
  frame(ctx,b,COL.edge);
  /* the drop */
  circleW(ctx,map,[0,0],1,COL.struct,1.6,null,rgba(COL.struct,0.10));
  /* the rays */
  const lams=st.white?[420,470,520,570,620,670]:[st.lamNm];
  const nRays=st.bowRays?31:9;
  for(const lam of lams){
    const n=dropIndex(lam);
    const col=cssOfLinear(monoLinear(lam),st.white?0.45:0.8);
    for(let i=-(nRays-1);i<nRays;i++){
      if(i===0) continue;
      const bimp=i/nRays;                  /* both signs: a drop is lit all over */
      const th=Math.asin(bimp);
      const P=dropPath(n,st.bowK,th);
      segW(ctx,map,[-4,P.pts[0][1]],P.pts[0],ext,col,1.0);
      for(let j=0;j<P.pts.length-1;j++) segW(ctx,map,P.pts[j],P.pts[j+1],ext,col,1.0);
      const last=P.pts[P.pts.length-1];
      segW(ctx,map,last,[last[0]+8*P.out[0],last[1]+8*P.out[1]],ext,col,1.0);
    }
  }
  /* the stationary ray, in the live colour */
  {
    const P=dropPath(Wb.n,st.bowK,Wb.thStar);
    segW(ctx,map,[-4,P.pts[0][1]],P.pts[0],ext,COL.live,2.2);
    for(let j=0;j<P.pts.length-1;j++) segW(ctx,map,P.pts[j],P.pts[j+1],ext,COL.live,2.2);
    const last=P.pts[P.pts.length-1];
    segW(ctx,map,last,[last[0]+8*P.out[0],last[1]+8*P.out[1]],ext,COL.live,2.2);
    lab(ctx,W,H,b.x+10,b.y+46,'the stationary ray struck at θi = '+fmt(Wb.thStar*RAD,2)+'°',
        COL.live,SM_FONT,'left');
    /* the bow direction itself, named: the rays pile up along it */
    const a=-Wb.devStar*DEG;
    segW(ctx,map,[0,0],[8*Math.cos(a),8*Math.sin(a)],ext,rgba(COL.ref,0.8),1.3,[5,4]);
    segW(ctx,map,[0,0],[8*Math.cos(-a),8*Math.sin(-a)],ext,rgba(COL.ref,0.8),1.3,[5,4]);
    lab(ctx,W,H,b.x+10,b.y+60,'the dashed lines are '+fmt(Wb.angStar,2)
        +'° from the antisolar direction',COL.ref,SM_FONT,'left');
  }
  /* the ray fan runs right across the top-left, so the caption block needs a
     pad of its own or it is unreadable */
  /* the pad is the BACKING for the three labels that follow, so it must not
     go into the registry — registering it made lab() dodge it and put the
     first line outside the panel altogether */
  ctx.fillStyle='rgba(7,11,24,.86)'; ctx.fillRect(b.x+1,b.y+1,Math.min(370,b.w-2),68);
  lab(ctx,W,H,b.x+10,b.y+14,'k = '+st.bowK+' internal reflection'+(st.bowK>1?'s':'')
      +'  →  bow at '+fmt(Wb.angStar,3)+'°',COL.pos,LAB_FONT,'left');
  lab(ctx,W,H,b.x+10,b.y+30,'water n/n_air = '+fmt(Wb.n,5)+' at '+fmt(st.lamNm,0)+' nm',COL.dim,SM_FONT,'left');
  lab(ctx,W,H,b.x1-10,b.y+14,'throughput '+fmt(100*Wb.through,2)+'% ('+st.bowPol+')',COL.ref,LAB_FONT,'right');
  if(L.bottom.length>=1) bowDeviation(ctx,W,H,L.bottom[0],M,st);
  if(L.bottom.length>=2) bowProfile(ctx,W,H,L.bottom[1],M,st);
  drawCaption(ctx,L);
}
function bowDeviation(ctx,W,H,b,M,st){
  const Wb=M.bow;
  const xs=Wb.th.map(t=>t*RAD);
  axesRB(ctx,b,0,90,120,250,{title:titleFor(b,'deviation against where the ray struck','D against θi'),
    xlab:'impact angle θi (degrees)',ylab:'deviation D (degrees)',nx:4,ny:nyFor(b),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
  polyline(ctx,b,xs,Wb.devs[1],0,90,120,250,COL.pos,1.8);
  polyline(ctx,b,xs,Wb.devs[2],0,90,120,250,COL.ref,1.8);
  for(const k of [1,2]){
    const th=rainTheta(Wb.n,k)*RAD, D=rainDev(Wb.n,k,rainTheta(Wb.n,k))*RAD;
    if(D>=120&&D<=250) marker(ctx,b,0,90,120,250,th,D,COL.live);
  }
  legendA(ctx,b,[[COL.pos,'k = 1, primary'],[COL.ref,'k = 2, secondary']]);
  noteIn(ctx,W,H,b,'flat bottom = rays pile up = a bow');
}
function bowProfile(ctx,W,H,b,M,st){
  const Wb=M.bow;
  axesRB(ctx,b,36,56,0,1,{title:titleFor(b,'where each colour lands','colour against angle'),
    xlab:'angle from the antisolar point (degrees)',ylab:'relative brightness',nx:4,ny:nyFor(b),
    xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
  /* the bow of each wavelength, as a band of the Airy-free geometric width */
  for(let lam=400;lam<=700;lam+=5){
    const n=dropIndex(lam);
    for(const k of [1,2]){
      const a=bowAngle(n,k)*RAD;
      if(a<36||a>56) continue;
      const th=rainTheta(n,k);
      const w=bowThroughput(indexOf(1.000293,lam),indexOf(1.333,lam),k,th,st.bowPol);
      const X=b.x+b.w*(a-36)/20;
      ctx.fillStyle=cssOfLinear(monoLinear(lam),clamp(monoLevel(lam)*clamp(w/0.06,0,1),0,1));
          ctx.fillRect(X-1.6,b.y1-b.h*clamp(w/0.06,0,1),3.2,b.h*clamp(w/0.06,0,1));
    }
  }
  const p1=Wb.bows[1], p2=Wb.bows[2];
  polyline(ctx,b,[p1.ang[700],p1.ang[700]],[0,1],36,56,0,1,rgba(COL.dim,0.6),1,[3,3]);
  polyline(ctx,b,[p2.ang[700],p2.ang[700]],[0,1],36,56,0,1,rgba(COL.dim,0.6),1,[3,3]);
  lab(ctx,W,H,b.x+b.w*(0.5*(p1.ang[400]+p2.ang[700])-36)/20,b.y+16,
      'Alexander’s dark band, '+fmt(Wb.gap,2)+'°',COL.ref,SM_FONT,'center');
  lab(ctx,W,H,b.x1-8,b.y1-12,'the secondary is reversed, and '
      +fmt(bowThroughput(Wb.nA,Wb.nW,1,rainTheta(Wb.n,1),st.bowPol)
          /Math.max(bowThroughput(Wb.nA,Wb.nW,2,rainTheta(Wb.n,2),st.bowPol),1e-12),1)
      +'× fainter',COL.dim,SM_FONT,'right');
}

/* ================================================================== *
 *  the dispatch and the scene                                         *
 * ================================================================== */
function drawView(ctx,W,H,M,st){
  st=st||ST;
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[]; PICKS=[];
  ctx.fillStyle='#070b18'; ctx.fillRect(0,0,W,H);
  if(st.view==='bound') drawBound(ctx,W,H,M,st);
  else if(st.view==='wave') drawWave(ctx,W,H,M,st);
  else if(st.view==='prism') drawPrism(ctx,W,H,M,st);
  else if(st.view==='fres') drawFres(ctx,W,H,M,st);
  else if(st.view==='spec') drawSpec(ctx,W,H,M,st);
  else drawBow(ctx,W,H,M,st);
}

/* the phase advance per frame: a fixed amount, so the headless suites and the
   capture are deterministic (no wall clock anywhere in the model) */
const PHASE_STEP=TAU/48;
function makeScene(canvas){
  const S={st:ST,W:1180,H:740};
  S.model=()=>buildModel(ST);
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel(ST),ST); };
  /* only the wave view animates */
  S.step=function(){
    if(ST.view!=='wave'||!ST.anim) return false;
    ST.phase=(ST.phase+PHASE_STEP*ST.waveSpeed)%TAU;
    return true;
  };
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; DRAG.what=null; return had; }
    const v=ST.view;
    if(v!=='bound'&&v!=='wave'&&v!=='prism') return false;
    const ctx=canvas.getContext('2d'), M=buildModel(ST);
    if(type==='down'){
      for(const p of PICKS) if(Math.hypot(x-p.x,y-p.y)<p.r){ DRAG.what=p.kind; return true; }
      return false;
    }
    if(type==='move'&&DRAG.what==='laser'&&(v==='bound'||v==='wave')){
      const G=(v==='bound')?boundGeo(ctx,S.W,S.H,M,ST):waveGeo(ctx,S.W,S.H,M,ST);
      const wx=G.map.wx(x), wy=G.map.wy(y);
      /* the laser sits up-LEFT of the origin: its angle from the normal */
      const a=Math.atan2(-wx,Math.max(wy,1e-6))*RAD;
      ST.angDeg=clamp(a,0,89.9);
      clearMemo();
      return true;
    }
    if(type==='move'&&DRAG.what==='beam'&&v==='prism'){
      const G=prismGeo(ctx,S.W,S.H,M,ST);
      ST.beamY=clamp(G.map.wy(y),PRISM_WORLD.ymin+1,PRISM_WORLD.ymax-1);
      clearMemo();
      return true;
    }
    return false;
  };
  return S;
}
