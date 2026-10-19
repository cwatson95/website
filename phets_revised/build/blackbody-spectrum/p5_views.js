
/* ---- two panels side by side (one, the primary, on a narrow stage) ----------------------------- */
function twoPanels(ctx,W,H,capFull,capShort,frac){
  const narrow=isNarrow(W), left=66, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,right-56));
  const top=stageTop()+46;
  const fit=fitCaption(ctx,W,H,capFull,capShort,capW,top+180);
  const hgt=Math.max(60,fit.capY-16-40-top);
  const out={narrow,capY:fit.capY,capTxt:fit.txt,capW,left:56};
  if(narrow){ out.b1=box(left,top,right-left,hgt); out.b2=null; }
  else { const gap=92, w1=Math.round((right-left-gap)*frac); out.b1=box(left,top,w1,hgt); out.b2=box(left+w1+gap,top,right-left-gap-w1,hgt); }
  return out;
}
function drawCap(ctx,L){ caption(ctx,L.left,L.capY,L.capTxt,L.capW,'#767e92',CAP_FONT); }
function panelTitle(ctx,W,H,b,longT,shortT){ lab(ctx,W,H,b.x,b.y-9,titleFor(b,longT,shortT),'#aeb6c6',TITLE_FONT,'left','bottom'); }
/* decade ticks on a log10 axis, labelled as plain numbers or as powers of ten */
function decTicks(lo,hi,maxN){
  const out=[]; let step=1; const n=Math.floor(hi)-Math.ceil(lo)+1;
  if(n>maxN) step=Math.ceil(n/maxN);
  for(let e=Math.ceil(lo);e<=Math.floor(hi);e+=step) out.push(e);
  return out;
}
function plainPow(e){ return e>=0?String(Math.round(Math.pow(10,e))):Math.pow(10,e).toFixed(-e); }
function supPow(e){ return '10'+supNum(e); }
const CH_COL=['#ff6b6b','#6bdc6b','#6b9bff'];                  /* the red, green and blue channels */

/* ================================================================== *
 *  view: the star — PhET's photometer against CIE colorimetry         *
 * ================================================================== */
function starCaption(M,small){
  const C=M.C;
  const full='Left, PhET’s star at PhET’s size: its colour is the curve sampled at 650, 550 and 450 nm (the R, G and B discs), '
    +'each divided by the largest of the three and dimmed by min(1, 0.02√(T − 798 K)) — dark below the Draper point, full from 3298 K. '
    +'Right, the colour the CIE 1931 standard observer assigns the same spectrum: X, Y, Z = ∫M_λ(x̄, ȳ, z̄)dλ over the CIE’s own table, '
    +'clipped into the sRGB gamut, its brightness log-compressed (display only). The strips run the whole thermometer, 200–11000 K, both ways; '
    +'below them, the three channels against temperature (solid PhET, dashed CIE, each normalised to its brightest channel above 3298 K).';
  const shortT='PhET’s photometer star (left) against CIE 1931 colorimetry (right); the strips span 200–11000 K.';
  return [small?shortT:full,shortT];
}
function starGeo(ctx,W,H,M){
  const narrow=isNarrow(W), left=66, right=narrow?W-26:W-RO_W-44, small=narrow||H<600;
  const cap=starCaption(M,small), capW=Math.max(260,Math.min(W-148,right-56));
  const fit=fitCaption(ctx,W,H,cap[0],cap[1],capW,stageTop()+260);
  const top=stageTop()+40, s=small?0.55:(H<760?0.8:1), glyphH=small?128:Math.round(236*s);
  const g={narrow,small,left,right,top,s,capY:fit.capY,capTxt:fit.txt,capW,
           gy:top+glyphH/2+(small?4:10), phX:left+(right-left)*(small?0.40:0.40), cieX:left+(right-left)*0.80};
  const sh=small?13:18, y0=top+glyphH+30;
  g.strips={x:left,w:right-left,h:sh,y1:y0,y2:y0+sh+24};
  const pTop=g.strips.y2+sh+60, pBot=fit.capY-16-40;
  g.plot=(!small&&pBot-pTop>=110)?box(left,pTop,right-left,pBot-pTop):null;
  return g;
}
function stripX(g,T){ const n=(T_MAX-T_MIN)/T_SNAP+1; return g.strips.x+g.strips.w*((T-T_MIN)/T_SNAP+0.5)/n; }
function drawStrip(ctx,x0,y0,w,h,css){
  const n=css.length, cw=w/n;
  for(let i=0;i<n;i++){ ctx.fillStyle=css[i]; ctx.fillRect(x0+i*cw,y0,cw+0.6,h); }
  ctx.strokeStyle=COL.edge; ctx.lineWidth=1; ctx.strokeRect(x0,y0,w,h);
}
/* the CIE colour as a disc (radius 35 px, like PhET's star) behind a flat halo in the same style as PhET's:
   radius (35 + 60 L) px, opacity 0.3 L, L the log-compressed luminance (display only) */
function drawCieGlow(ctx,cx,cy,s,lin,level){
  if(level>0){ ctx.beginPath(); ctx.arc(cx,cy,(35+60*level)*s,0,TAU);
    ctx.fillStyle='rgba('+toRgb(cssOfLinear(lin,1)).join(',')+','+fmt(0.3*level,3)+')'; ctx.fill(); }
  dot(ctx,cx,cy,35*s,cssOfLinear(lin,level),'rgba(255,255,255,0.28)',1);
}
function drawStar(ctx,W,H,M){
  const C=M.C, g=starGeo(ctx,W,H,M), s=g.s, T=M.T, Sx=C.strips;
  /* the two glyphs */
  lab(ctx,W,H,g.left,g.top-6,g.small?'PhET’s star':'PhET’s star: three samples of the curve','#aeb6c6',TITLE_FONT,'left','bottom');
  const cieT='CIE 1931: what the eye makes of it', cx0=g.cieX-60*s;
  lab(ctx,W,H,cx0,g.top-6,(g.small||cx0+cieT.length*13*0.52>g.right)?'CIE 1931':cieT,'#aeb6c6',TITLE_FONT,'left','bottom');
  drawStarGlyph(ctx,g.phX,g.gy,s,C.ph,C.halo);
  drawBGR(ctx,W,H,[g.phX-200*s,g.phX-150*s,g.phX-100*s],g.gy,15*s,C.ph);
  drawCieGlow(ctx,g.cieX,g.gy,s,bbLinear(T),C.glow);
  const yl=g.gy+(g.small?60:112*s);
  lab(ctx,W,H,g.phX-100*s,yl,'R G B = '+C.ph.join(' ')+'   '+hexOfBytes(C.ph),COL.dim,SM_FONT,'center','middle');
  lab(ctx,W,H,g.cieX,yl,'x '+fmt(C.xy[0],4)+', y '+fmt(C.xy[1],4)+'   '+C.hex,COL.pos,SM_FONT,'center','middle');
  /* the strips over the whole thermometer */
  const st=g.strips;
  lab(ctx,W,H,st.x,st.y1-5,'PhET’s photometer',COL.dim,SM_FONT,'left','bottom');
  drawStrip(ctx,st.x,st.y1,st.w,st.h,Sx.phCss);
  lab(ctx,W,H,st.x,st.y2-5,'CIE 1931 (brightness log-compressed)',COL.dim,SM_FONT,'left','bottom');
  drawStrip(ctx,st.x,st.y2,st.w,st.h,Sx.cieCss);
  const xd=stripX(g,PH_DRAPER), xT=stripX(g,T);
  line(ctx,xd,st.y1-3,xd,st.y2+st.h+3,COL.ref,1.2,[3,3]);
  line(ctx,xT,st.y1-3,xT,st.y2+st.h+3,COL.live,1.6);
  ctx.beginPath(); ctx.moveTo(xT,st.y1-2); ctx.lineTo(xT-6,st.y1-11); ctx.lineTo(xT+6,st.y1-11); ctx.closePath(); ctx.fillStyle=COL.live; ctx.fill();
  for(const TT of [2000,4000,6000,8000,10000]){ const x=stripX(g,TT); line(ctx,x,st.y2+st.h,x,st.y2+st.h+4,COL.dim,1);
    lab(ctx,W,H,x,st.y2+st.h+12,TT+' K',COL.dim,SM_FONT,'center','middle'); }
  lab(ctx,W,H,xd+4,st.y2+st.h+12,'798 K, the Draper point',COL.ref,SM_FONT,'left','middle');
  /* the channels against temperature */
  if(g.plot){
    const b=g.plot, xs=Sx.Ts.map(v=>v/1000);
    axesR(ctx,b,T_MIN/1000,T_MAX/1000,0,255,{nx:8,ny:5,xfmt:v=>fmt(v,0),yfmt:v=>fmt(v,0),xlab:'temperature, 1000 K',ylab:'channel, 0–255'});
    panelTitle(ctx,W,H,b,'the three channels: PhET’s photometer (solid) and CIE 1931 (dashed)','the channels, PhET solid, CIE dashed');
    for(let c=0;c<3;c++){
      polyline(ctx,b,xs,Sx.ph.map(p=>p[c]),T_MIN/1000,T_MAX/1000,0,255,CH_COL[c],1.8);
      polyline(ctx,b,xs,Sx.cie.map(p=>p[c]),T_MIN/1000,T_MAX/1000,0,255,CH_COL[c],1.2,[6,4]);
    }
    const X=v=>b.x+b.w*(v-T_MIN/1000)/((T_MAX-T_MIN)/1000);
    line(ctx,X(PH_DRAPER/1000),b.y,X(PH_DRAPER/1000),b.y1,COL.ref,1,[3,3]);
    line(ctx,X((PH_DRAPER+2500)/1000),b.y,X((PH_DRAPER+2500)/1000),b.y1,COL.ref,1,[3,3]);
    lab(ctx,W,H,X((PH_DRAPER+2500)/1000)+5,b.y1-12,'3298 K: PhET’s ramp is full',COL.ref,SM_FONT,'left','middle');
    line(ctx,X(T/1000),b.y,X(T/1000),b.y1,COL.live,1.4);
    legendAuto(ctx,b,[[CH_COL[0],'red'],[CH_COL[1],'green'],[CH_COL[2],'blue']]);
  }
  drawCap(ctx,{left:g.left-10,capY:g.capY,capTxt:g.capTxt,capW:g.capW});
}

/* ================================================================== *
 *  view: the peak — Wien's law                                        *
 * ================================================================== */
const PEAK_X=[Math.log10(0.05),Math.log10(200)], PEAK_Y=[-8,4];
function peakCaption(M){
  const P=M.P;
  return ['Left, on log–log axes (every decade the same length): Planck’s curve at '+fmt(M.T,0)+' K (green) and at PhET’s four presets (grey); '
    +'the orange line is the locus of the peaks, M(λ_max) = K_peak (b/λ)⁵, a straight line of slope −5 because λ_max = b/T and the peak height grows as T⁵. '
    +'Right, every curve divided by its own peak and plotted against λ/λ_max: they are one curve. Its half-maximum runs from 0.613 to 1.817 λ_max '
    +'(λT from 1777 to 5265 µm·K); per unit frequency the same spectrum peaks at 1.760 λ_max, so where “the peak” is depends on the axis.',
    'Planck’s curve at '+fmt(M.T,0)+' K and the presets on log–log axes; orange: the locus of peaks, slope −5.'];
}
function drawPeak(ctx,W,H,M){
  const P=M.P, cap=peakCaption(M), L=twoPanels(ctx,W,H,cap[0],cap[1],0.6), b=L.b1;
  const lx=a=>a.xs.map(Math.log10), ly=a=>a.ys.map(v=>v>0?Math.log10(v):-Infinity);
  axesR(ctx,b,PEAK_X[0],PEAK_X[1],PEAK_Y[0],PEAK_Y[1],{xticks:decTicks(PEAK_X[0],PEAK_X[1],6),yticks:decTicks(PEAK_Y[0],PEAK_Y[1],7),
    xfmt:plainPow,yfmt:supPow,xlab:'wavelength λ, µm (log)',ylab:'M_λ, MW/m²/µm (log)'});
  panelTitle(ctx,W,H,b,'Planck’s family and the locus of its peaks (log–log)','the family, log–log');
  const X=v=>b.x+b.w*(v-PEAK_X[0])/(PEAK_X[1]-PEAK_X[0]), Y=v=>b.y1-b.h*(v-PEAK_Y[0])/(PEAK_Y[1]-PEAK_Y[0]);
  /* the locus: M = K_peak T⁵ with T = b/λ */
  const lxs=[], lys=[];
  for(let i=0;i<=40;i++){ const le=PEAK_X[0]+(PEAK_X[1]-PEAK_X[0])*i/40, lam=Math.pow(10,le)*1e-6; lxs.push(le); lys.push(Math.log10(K_PEAK*Math.pow(B_WIEN/lam,5)*TO_DISP)); }
  polyline(ctx,b,lxs,lys,PEAK_X[0],PEAK_X[1],PEAK_Y[0],PEAK_Y[1],COL.ref,1.4,[7,5]);
  for(const f of P.fam) polyline(ctx,b,lx(f.c),ly(f.c),PEAK_X[0],PEAK_X[1],PEAK_Y[0],PEAK_Y[1],'#56607a',1.3);
  polyline(ctx,b,lx(P.cur.c),ly(P.cur.c),PEAK_X[0],PEAK_X[1],PEAK_Y[0],PEAK_Y[1],COL.pos,2.4);
  for(const f of P.fam){ const px=X(Math.log10(f.lm/1000)), py=Y(Math.log10(f.Mp)); diamond(ctx,px,py,4.5,COL.ref,'#ffffff');
    labAvoid(ctx,W,H,[[px+8,py-8,'left','bottom'],[px+8,py+8,'left','top'],[px-8,py-8,'right','bottom'],[px-8,py+8,'right','top'],[px+10,py-24,'left','bottom']],
             f.name+', '+fmt(f.T,0)+' K',COL.dim,SM_FONT); }
  dot(ctx,X(Math.log10(P.lm/1000)),Y(Math.log10(P.Mp)),5,COL.live,'#ffffff',1.2);
  /* the locus crosses the panel from about 0.19 µm (top) to 48 µm (bottom): label it at 30 µm, below-left of the line */
  const yL=Math.log10(K_PEAK*Math.pow(B_WIEN/30e-6,5)*TO_DISP);
  const yL2=Math.log10(K_PEAK*Math.pow(B_WIEN/10e-6,5)*TO_DISP);
  labAvoid(ctx,W,H,[[X(Math.log10(30))-10,Y(yL)+8,'right','top'],[X(Math.log10(30))+10,Y(yL),'left','middle'],[X(1)+10,Y(yL2),'left','middle'],[X(1)-10,Y(yL2)+8,'right','top']],
           'the locus of the peaks ∝ λ⁻⁵',COL.ref,SM_FONT);
  if(L.b2){
    const c=L.b2;
    axesR(ctx,c,0,5,0,1.05,{nx:5,ny:5,xfmt:v=>fmt(v,0),yfmt:v=>fmt(v,1),xlab:'λ / λ_max',ylab:'M / M(λ_max)'});
    panelTitle(ctx,W,H,c,'every temperature, one curve','one curve');
    const Xc=v=>c.x+c.w*v/5, Yc=v=>c.y1-c.h*v/1.05;
    P.uni.forEach((u,i)=>polyline(ctx,c,u.xs,u.ys,0,5,0,1.05,i===0?COL.pos:'#56607a',i===0?2.4:1.2,i===0?null:[5,4]));
    line(ctx,Xc(0.61323368060735),Yc(0.5),Xc(1.8169998026431),Yc(0.5),COL.ref,1.4);
    diamond(ctx,Xc(1),Yc(1),4.5,COL.ref,'#ffffff');
    lab(ctx,W,H,Xc(1.83)+6,Yc(0.5),'half maximum: 0.613–1.817 λ_max',COL.ref,SM_FONT,'left','middle');
    line(ctx,Xc(X5/X3),Yc(0),Xc(X5/X3),Yc(0.2),COL.ref,1.2,[3,3]);
    labAvoid(ctx,W,H,[[Xc(X5/X3)+5,Yc(0.035),'left','middle'],[Xc(X5/X3)+5,Yc(0.3),'left','middle'],[Xc(X5/X3)-5,Yc(0.12),'right','middle']],
             'B_ν peaks here: 1.760 λ_max',COL.ref,SM_FONT);
  }
  drawCap(ctx,L);
}

/* ================================================================== *
 *  view: the total — Stefan–Boltzmann and the band budget             *
 * ================================================================== */
const TOT_X=[Math.log10(T_MIN),Math.log10(T_MAX)], TOT_Y=[1.5,9.5];
const BAND_FILL=['#3aa7b0','#7a62d8','#d9d08a','#b4513c','#2c3552'];
function totalCaption(M){
  const O=M.O;
  return ['Left, on log–log axes: the intensity σT⁴ against temperature, a straight line of slope 4 (green); PhET’s presets in orange, '
    +fmt(M.T,0)+' K in magenta, where the integral of Planck’s curve by a 1024-point Gauss–Legendre rule gives '+sci(O.quad,5)+' W/m² against σT⁴ = '+sci(O.I,5)+'. '
    +'Right, the same power split into PhET’s bands, stacked: X-ray below 10 nm (far too small to see below 11000 K), ultraviolet, visible (380–780 nm), '
    +'infrared to 100 µm, and beyond 100 µm (the thin band at the top left).',
    'σT⁴ against T on log–log axes (slope 4), and the share of it in each band.'];
}
function drawTotal(ctx,W,H,M){
  const O=M.O, cap=totalCaption(M), L=twoPanels(ctx,W,H,cap[0],cap[1],0.5), b=L.b1;
  const TT=[200,500,1000,2000,5000,10000];
  axesR(ctx,b,TOT_X[0],TOT_X[1],TOT_Y[0],TOT_Y[1],{xticks:TT.map(Math.log10),yticks:decTicks(TOT_Y[0],TOT_Y[1],8),
    xfmt:v=>String(Math.round(Math.pow(10,v))),yfmt:supPow,xlab:'temperature T, K (log)',ylab:'σT⁴, W/m² (log)'});
  panelTitle(ctx,W,H,b,'the Stefan–Boltzmann law (log–log)','σT⁴, log–log');
  const X=v=>b.x+b.w*(v-TOT_X[0])/(TOT_X[1]-TOT_X[0]), Y=v=>b.y1-b.h*(v-TOT_Y[0])/(TOT_Y[1]-TOT_Y[0]);
  polyline(ctx,b,O.curve.xs.map(v=>Math.log10(v*1000)),O.curve.ys.map(Math.log10),TOT_X[0],TOT_X[1],TOT_Y[0],TOT_Y[1],COL.pos,2.2);
  for(const p of PRESETS){ const px=X(Math.log10(p.T)), py=Y(Math.log10(intensity(p.T))); diamond(ctx,px,py,4.5,COL.ref,'#ffffff');
    lab(ctx,W,H,px+8,py+2,p.name,COL.dim,SM_FONT,'left','top'); }
  const cx=X(Math.log10(M.T)), cy=Y(Math.log10(O.I));
  dot(ctx,cx,cy,5,COL.live,'#ffffff',1.2);
  dot(ctx,cx,Y(Math.log10(O.quad)),8,null,COL.pos,1.2);
  const leftHalf=cx<b.x+b.w*0.45;
  lab(ctx,W,H,leftHalf?cx+10:cx-10,cy-12,sci(O.I,3)+' W/m²',COL.live,SM_FONT,leftHalf?'left':'right','bottom');
  labAvoid(ctx,W,H,[[b.x1-8,Y(TOT_Y[0]+0.28*(TOT_Y[1]-TOT_Y[0])),'right','middle'],[b.x1-8,Y(TOT_Y[0]+0.15*(TOT_Y[1]-TOT_Y[0])),'right','middle']],
           'slope 4: double T, sixteen times the power',COL.pos,SM_FONT);
  if(L.b2){
    const c=L.b2, Bg=O.budget, xs=Bg.Ts.map(v=>v/1000);
    axesR(ctx,c,T_MIN/1000,T_MAX/1000,0,1,{nx:6,ny:5,xfmt:v=>fmt(v,0),yfmt:v=>fmt(100*v,0),xlab:'temperature, 1000 K',ylab:'share of σT⁴, %'});
    panelTitle(ctx,W,H,c,'where the power goes, band by band','the bands');
    const Xc=v=>c.x+c.w*(v-T_MIN/1000)/((T_MAX-T_MIN)/1000), Yc=v=>c.y1-c.h*v;
    let lower=xs.map(()=>0);
    for(let k=0;k<BANDS.length;k++){
      const upper=lower.map((v,i)=>Math.min(1,v+Bg.f[k][i]));
      ctx.beginPath(); ctx.moveTo(Xc(xs[0]),Yc(lower[0]));
      for(let i=0;i<xs.length;i++) ctx.lineTo(Xc(xs[i]),Yc(upper[i]));
      for(let i=xs.length-1;i>=0;i--) ctx.lineTo(Xc(xs[i]),Yc(lower[i]));
      ctx.closePath(); ctx.fillStyle=BAND_FILL[k]; ctx.fill();
      lower=upper;
    }
    /* each band named inside itself, at a temperature where it is thick: the label's height is the
       middle of the band there, from the same fractions the fill is built from */
    for(const [k,Tk,col] of [[3,1500,'#ffffff'],[2,6500,COL.bg],[1,10000,'#ffffff']]){
      let lo=0; for(let j=0;j<k;j++) lo+=bandFrac(BANDS[j].lo,BANDS[j].hi,Tk);
      const th=bandFrac(BANDS[k].lo,BANDS[k].hi,Tk);
      const nm=BANDS[k].name.toLowerCase(), hw=nm.length*11*0.52/2+4;                 /* kept inside the panel */
      if(th>=0.08) lab(ctx,W,H,clamp(Xc(Tk/1000),c.x+hw,c.x1-hw),Yc(lo+th/2),nm,col,'600 11px -apple-system, sans-serif','center','middle');
    }
    line(ctx,Xc(M.T/1000),c.y,Xc(M.T/1000),c.y1,COL.live,1.6);
    const bi=O.bands, vis=bi[2], ir=bi[3], uv=bi[1];
    /* the shares at the current temperature, beside its line and inside the panel (one line if it fits, else two) */
    const xT=Xc(M.T/1000), one='UV '+pct(uv)+' · visible '+pct(vis)+' · IR '+pct(ir), wOne=one.length*10.5*0.52+8;
    const side=(xT+8+wOne<=c.x1)?1:((xT-8-wOne>=c.x)?-1:0);
    if(side) labPad(ctx,W,H,xT+side*8,c.y+12,one,COL.live,SM_FONT,side>0?'left':'right','top');
    else { const a2='UV '+pct(uv)+' · visible '+pct(vis), b2='IR '+pct(ir), sd=(xT-c.x>c.x1-xT)?-1:1, al2=sd>0?'left':'right';
      labPad(ctx,W,H,xT+sd*8,c.y+12,a2,COL.live,SM_FONT,al2,'top'); labPad(ctx,W,H,xT+sd*8,c.y+28,b2,COL.live,SM_FONT,al2,'top'); }
  }
  drawCap(ctx,L);
}

/* ================================================================== *
 *  view: the limits — Rayleigh–Jeans and Wien against Planck          *
 * ================================================================== */
const LIM_X=[-2,3], RAT_X=[-3,Math.log10(30)], RAT_Y=[-3,3];
function limitsCaption(M){
  const L=M.L;
  return ['Left, on log–log axes at '+fmt(M.T,0)+' K: Planck’s law (green), the classical Rayleigh–Jeans law 2πckT/λ⁴ (orange dashes) and Wien’s '
    +'approximation (blue dots). Rayleigh–Jeans climbs as λ⁻⁴ without limit toward short wavelengths, so its area is infinite; it is within 1 % of Planck only beyond '
    +um(L.lamRJ1,3)+'. Wien’s law is within 1 % below '+um(L.lamW1,3)+' and falls away at long wavelengths. Right, each law divided by Planck’s against x = hc/λkT, the same for every temperature: '
    +'(eˣ − 1)/x and 1 − e⁻ˣ; at the peak, x = 4.965, Rayleigh–Jeans is '+sigf(L.rjPeak,3)+' times too high and Wien’s law 0.70 % low.',
    'Planck (green), Rayleigh–Jeans (orange) and Wien (blue) at '+fmt(M.T,0)+' K, log–log; right, each over Planck against hc/λkT.'];
}
function drawLimits(ctx,W,H,M){
  const Lm=M.L, st=M.st, cap=limitsCaption(M), L=twoPanels(ctx,W,H,cap[0],cap[1],0.56), b=L.b1;
  const top=Math.ceil(Math.log10(Lm.Mp))+2, ylo=top-12;
  axesR(ctx,b,LIM_X[0],LIM_X[1],ylo,top,{xticks:decTicks(LIM_X[0],LIM_X[1],6),yticks:decTicks(ylo,top,7).filter(v=>v>ylo),xfmt:plainPow,yfmt:supPow,
    xlab:'wavelength λ, µm (log)',ylab:'M_λ, MW/m²/µm (log)'});
  panelTitle(ctx,W,H,b,'Planck’s law and the two laws it replaced (log–log)','Planck and the limits');
  const lx=a=>a.xs.map(Math.log10), ly=a=>a.ys.map(v=>v>0?Math.log10(v):-Infinity);
  const X=v=>b.x+b.w*(v-LIM_X[0])/(LIM_X[1]-LIM_X[0]);
  if(st.rj) polyline(ctx,b,lx(Lm.rj),ly(Lm.rj),LIM_X[0],LIM_X[1],ylo,top,COL.ref,1.8,[8,5]);
  if(st.wien) polyline(ctx,b,lx(Lm.wi),ly(Lm.wi),LIM_X[0],LIM_X[1],ylo,top,COL.wien,1.8,[2,4]);
  polyline(ctx,b,lx(Lm.pl),ly(Lm.pl),LIM_X[0],LIM_X[1],ylo,top,COL.pos,2.2);
  const xr=X(Math.log10(Lm.lamRJ1/1000)), xw=X(Math.log10(Lm.lamW1/1000));
  if(st.rj&&xr<b.x1){ line(ctx,xr,b.y1,xr,b.y1-26,COL.ref,1.4); lab(ctx,W,H,xr+4,b.y1-22,'RJ within 1 % →',COL.ref,SM_FONT,'left','middle'); }
  if(st.wien&&xw>b.x){ line(ctx,xw,b.y1,xw,b.y1-26,COL.wien,1.4); lab(ctx,W,H,xw-4,b.y1-22,'← Wien within 1 %',COL.wien,SM_FONT,'right','middle'); }
  if(st.rj) lab(ctx,W,H,b.x1-10,b.y+14,'Rayleigh–Jeans ∝ λ⁻⁴: the ultraviolet catastrophe',COL.ref,SM_FONT,'right','middle');
  if(L.b2){
    const c=L.b2, R=Lm.ratios, rx=R.xs.map(Math.log10);
    axesR(ctx,c,RAT_X[0],RAT_X[1],RAT_Y[0],RAT_Y[1],{xticks:decTicks(RAT_X[0],RAT_X[1],5),yticks:decTicks(RAT_Y[0],RAT_Y[1],7).filter(v=>v>RAT_Y[0]),
      xfmt:plainPow,yfmt:v=>v===0?'1':supPow(v),xlab:'x = hc/λkT (log)',ylab:'law / Planck (log)'});
    panelTitle(ctx,W,H,c,'each law over Planck’s, any temperature','over Planck’s');
    const Xc=v=>c.x+c.w*(v-RAT_X[0])/(RAT_X[1]-RAT_X[0]);
    polyline(ctx,c,[RAT_X[0],RAT_X[1]],[0,0],RAT_X[0],RAT_X[1],RAT_Y[0],RAT_Y[1],COL.pos,1.6);
    if(st.rj) polyline(ctx,c,rx,R.r.map(Math.log10),RAT_X[0],RAT_X[1],RAT_Y[0],RAT_Y[1],COL.ref,1.8,[8,5]);
    if(st.wien) polyline(ctx,c,rx,R.w.map(Math.log10),RAT_X[0],RAT_X[1],RAT_Y[0],RAT_Y[1],COL.wien,1.8,[2,4]);
    line(ctx,Xc(Math.log10(X5)),c.y,Xc(Math.log10(X5)),c.y1,COL.dim,1,[3,3]);
    lab(ctx,W,H,Xc(Math.log10(X5))-5,c.y+14,'the peak, x = 4.965',COL.dim,SM_FONT,'right','middle');
    lab(ctx,W,H,Xc(-2.2),c.y1-c.h*(0.5-RAT_Y[0])/(RAT_Y[1]-RAT_Y[0])+14,'Planck = 1',COL.pos,SM_FONT,'left','top');
  }
  drawCap(ctx,L);
}

/* ================================================================== *
 *  dispatch, scene object                                             *
 * ================================================================== */
function drawView(ctx,W,H,M){
  LEGEND_RECTS=[]; POLY_SEGS=[]; LABELS=[];
  ctx.fillStyle=COL.bg; ctx.fillRect(0,0,W,H);
  if(M.view==='spec') drawSpec(ctx,W,H,M);
  else if(M.view==='star') drawStar(ctx,W,H,M);
  else if(M.view==='peak') drawPeak(ctx,W,H,M);
  else if(M.view==='total') drawTotal(ctx,W,H,M);
  else drawLimits(ctx,W,H,M);
}
function makeScene(canvas){
  const S={st:ST,W:1100,H:712};
  S.model=buildModel;
  S.draw=function(){ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  /* the pointer, on the spectrum only: the Graph Values point (dragged along the curve, clamped to the
     axis as PhET's is) and the thermometer (the pointer's height, snapped to 50 K) */
  S.pointer=function(type,x,y){
    if(type==='up'){ const had=DRAG.what!==null; if(DRAG.what==='gv') ST.gvCue=false; DRAG.what=null; return had; }
    if(ST.view!=='spec') return false;
    const M=buildModel(), g=specGeo(canvas.getContext('2d'),S.W,S.H,M), b=g.b, Sm=M.S;
    if(type==='down'){
      if(ST.gv&&Sm.gv.inside){
        const gx=b.x+b.w*ST.gvNm/Sm.xmax, gy=Sm.gv.above?b.y:b.y1-b.h*Sm.gv.M/Sm.ymax;
        if(Math.hypot(x-gx,y-gy)<=14||(Math.abs(x-gx)<=6&&y>=gy&&y<=b.y1)){ DRAG.what='gv'; DRAG.off=gx-x; return true; }
      }
      const th=g.th;
      if(th&&x>=th.x-10&&x<=th.x+th.w+20&&y>=th.yTop-10&&y<=th.bulbY+th.bulbR){ DRAG.what='thermo'; setT(tempAtY(th,y)); return true; }
      return false;
    }
    if(DRAG.what==='gv'){ ST.gvNm=clamp((x+DRAG.off-b.x)/b.w*Sm.xmax,0,Sm.xmax); return true; }
    if(DRAG.what==='thermo'){ const T0=ST.T; setT(tempAtY(g.th,y)); return ST.T!==T0; }
    return false;
  };
  return S;
}
