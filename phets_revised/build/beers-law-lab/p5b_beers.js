
/* ================================================================== *
 *  the spectrum and the law.  Built only into beers-law-lab.html.     *
 * ================================================================== */
/* ---------------------------------------------------------------- the spectrum ------- */
/* a 1 nm strip of the visible spectrum, drawn under a plot box whose x axis is in nm */
function spectrumStrip(rc,b,xlo,xhi,y,h){
  const n=Math.max(2,Math.round(b.w));
  for(let i=0;i<n;i++){
    const lam=xlo+(xhi-xlo)*(i+0.5)/n;
    rc.fillStyle=waveCss(lam);
    rc.fillRect(b.x+b.w*i/n,y,b.w/n+0.8,h);
  }
  frame(rc,box(b.x,y,b.w,h),'#242a3a');
}

const CAP_SPEC='PhET’s eight absorption spectra, one molar absorptivity per nanometre '
  +'from 380 to 780 nm exactly as the original ships them. The preset wavelength is the '
  +'maximum of the curve, found by scanning it, and ε is looked up rather than '
  +'interpolated — 500.0 nm and 500.9 nm read the same cell. NO literature molar '
  +'absorptivity could be sourced offline for these, so they stand as PhET’s data and '
  +'nothing is claimed for them beyond that. The strip under the axis is the wavelength’s '
  +'own colour through the CIE observer, faded by the eye’s response: display only.';
const CAP_SPEC_S='PhET’s eight spectra, 1 nm samples, ε looked up not interpolated. '
  +'No literature ε could be sourced; these are PhET’s data.';

function viewSpectrum(rc,W,H,M){
  const S=M.S, L=layoutPanels(rc,W,H,CAP_SPEC,CAP_SPEC_S,2,0.34);
  const b=L.main;
  const stripH=9;
  const plot=box(b.x,b.y,b.w,Math.max(60,b.h-stripH-16));
  if(ST.allSpectra){
    const ylo=-1.7, yhi=4;      /* cobalt(II) nitrate falls to eps = 0.03 at 780 nm */
    axesFit(rc,plot,LAM0,LAM1,ylo,yhi,{title:'every solution, log10 ε',
      xlab:'wavelength, nm',ylab:'log10 ε',
      yfmt:t=>fmt(t,0),xfmt:t=>fmt(t,0),ny:6});
    const items=[];
    S.all.forEach((a,i)=>{
      const ys=a.eps.map(v=>v>0?Math.log10(v):ylo-1);
      const col=a.id===S.d.id?COL.pos:neonCss(0.12+0.72*i/7);
      polyline(rc,plot,S.xs,ys,LAM0,LAM1,ylo,yhi,col,a.id===S.d.id?2.2:1.2);
      items.push([col,a.name]);
    });
    legendFit(rc,plot,items);
  } else {
    const yhi=S.epsMax*1.14;
    axesFit(rc,plot,LAM0,LAM1,0,yhi,{title:soluteById(S.d.solute).name+' — ε(λ)',
      xlab:'wavelength, nm',ylab:'ε, L/(mol cm)',
      xfmt:t=>fmt(t,0),yfmt:t=>yhi>50?fmt(t,0):fmt(t,1)});
    polyline(rc,plot,S.xs,S.eps,LAM0,LAM1,0,yhi,COL.pos,2.2);
    /* lambda_max */
    const xm=plot.x+plot.w*(S.lamMax-LAM0)/(LAM1-LAM0);
    rc.strokeStyle=COL.ref; rc.lineWidth=1.3; rc.setLineDash([5,4]);
    rc.beginPath(); rc.moveTo(xm,plot.y); rc.lineTo(xm,plot.y1); rc.stroke();
    rc.setLineDash([]);
    lab(rc,W,H,xm+5,plot.y+14,'λ max = '+fmt(S.lamMax,0)+' nm, ε = '+fmt(S.epsMax,2),
        COL.ref,LAB_FONT,'left','middle');
  }
  /* the live wavelength cursor */
  const xc=plot.x+plot.w*(S.lam-LAM0)/(LAM1-LAM0);
  if(xc>=plot.x-0.5&&xc<=plot.x1+0.5){
    rc.strokeStyle=COL.live; rc.lineWidth=1.6;
    rc.beginPath(); rc.moveTo(xc,plot.y); rc.lineTo(xc,plot.y1); rc.stroke();
    /* on whichever side of the cursor has room: right-aligned at 392 nm the label runs
       off the plot and into the y-tick gutter (audit, 560 x 380) */
    const leftish=(xc-plot.x)<plot.w*0.34;
    lab(rc,W,H,xc+(leftish?6:-6),plot.y1-14,fmt(S.lam,0)+' nm',COL.live,LAB_FONT,
        leftish?'left':'right','middle');
  }
  spectrumStrip(rc,plot,LAM0,LAM1,plot.y1+5,stripH);
  /* A(lambda) and T(lambda) at the bench's present l and c */
  if(L.bottom[0]){
    const p=L.bottom[0];
    let ahi=0; for(const v of S.A) ahi=Math.max(ahi,v);
    ahi=Math.max(0.2,ahi*1.15);
    axesFit(rc,p,LAM0,LAM1,0,ahi,{title:'A(λ) = ε(λ) l c',
      xlab:'nm',ylab:'A',xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,1)});
    polyline(rc,p,S.xs,S.A,LAM0,LAM1,0,ahi,COL.pos,1.8);
    for(const a of [1,2,3]){
      if(a>ahi) continue;
      polyline(rc,p,[LAM0,LAM1],[a,a],LAM0,LAM1,0,ahi,COL.ref,1,[4,4]);
      lab(rc,W,H,p.x1-4,p.y1-p.h*a/ahi-8,'A = '+a,COL.ref,SM_FONT,'right','middle');
    }
    marker(rc,p,LAM0,LAM1,0,ahi,S.lam,S.Ahere,COL.live);
  }
  if(L.bottom[1]){
    const p=L.bottom[1];
    axesFit(rc,p,LAM0,LAM1,0,100,{title:'T(λ) = 10^-A, per cent',
      xlab:'nm',ylab:'T, %',xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
    polyline(rc,p,S.xs,S.T.map(v=>100*v),LAM0,LAM1,0,100,COL.struct,1.8);
    marker(rc,p,LAM0,LAM1,0,100,S.lam,100*transmittance(S.Ahere),COL.live);
    lab(rc,W,H,p.x+12,p.y+14,'what a white beam would have left',COL.dim,SM_FONT,'left','middle');
  }
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}

/* ---------------------------------------------------------------- the law ------------ */
const CAP_LAW='Why an instrument measures transmittance and reports absorbance. A is linear '
  +'in the concentration and in the path length, so its plot is a straight line through the '
  +'origin whose slope is εl or εc; T is an exponential in both, and reading a '
  +'concentration off it would mean reading a log by eye. The third panel is the same curve '
  +'for every solution there is: T = 10^-A has nothing in it but A. The shaded band '
  +'is where a real solution stops obeying the law — above about 10 mM, a conventional '
  +'teaching bound and not a measurement, which is why it is drawn as a band and named.';
const CAP_LAW_S='A is linear in c and l; T is not. T = 10^-A is the same curve for '
  +'every solution. Past ~10 mM the straight line is an extrapolation.';

function viewLaw(rc,W,H,M){
  const L=M.L, Ly=layoutPanels(rc,W,H,CAP_LAW,CAP_LAW_S,2,0.36);
  const b=Ly.main, byCon=(ST.lawX==='conc');
  const xhi=byCon?L.d.cMax:PHET.CUVETTE_MAX;
  const xs=byCon?L.cs:L.ls;
  const yhi=Math.max(0.4,L.Amax*1.12);
  const xf=byCon?(t=>fmt(t*L.d.scale,0)):(t=>fmt(t,1));
  axesFit(rc,b,0,xhi,0,yhi,{title:byCon?'A against concentration, at l = '+fmt(L.l,2)+' cm'
                                     :'A against path length, at c = '+plain(blConcStr(L.c)),
    xlab:byCon?('concentration, '+L.d.transform):'path length, cm',
    ylab:'absorbance A',xfmt:xf,yfmt:t=>fmt(t,1)});
  if(byCon){
    /* the band where Beer-Lambert stops being true */
    if(L.linear<xhi){
      const x0=b.x+b.w*L.linear/xhi;
      rc.fillStyle='rgba(232,132,58,.055)';
      rc.fillRect(x0,b.y,b.x1-x0,b.h);
      rc.strokeStyle=COL.ref; rc.lineWidth=1; rc.setLineDash([4,4]);
      rc.beginPath(); rc.moveTo(x0,b.y); rc.lineTo(x0,b.y1); rc.stroke(); rc.setLineDash([]);
      lab(rc,W,H,x0+5,b.y+14,'past 10 mM: extrapolated',COL.ref,SM_FONT,'left','middle');
    }
    const items=[];
    for(const ln of L.lines){
      const col=Math.abs(ln.l-L.l)<1e-9?COL.pos:shade(COL.struct,0.55);
      polyline(rc,b,L.cs,ln.A,0,xhi,0,yhi,col,Math.abs(ln.l-L.l)<1e-9?2.2:1.2,
               Math.abs(ln.l-L.l)<1e-9?null:[5,4]);
      items.push([col,'l = '+fmt(ln.l,1)+' cm']);
    }
    polyline(rc,b,L.cs,L.Ac,0,xhi,0,yhi,COL.pos,2.2);
    legendFit(rc,b,items);
    marker(rc,b,0,xhi,0,yhi,L.c,L.A,COL.live);
  } else {
    polyline(rc,b,L.ls,L.Al,0,xhi,0,yhi,COL.pos,2.2);
    marker(rc,b,0,xhi,0,yhi,L.l,L.A,COL.live);
    lab(rc,W,H,b.x+8,b.y+14,'slope = εc = '+sciPlain(L.eps*L.c,3)+' per cm',
        COL.pos,LAB_FONT,'left','middle');
  }
  lab(rc,W,H,b.x+8,b.y+(byCon?30:30),'ε = '+fmt(L.eps,3)+' at '+fmt(L.lam,0)+' nm',
      COL.dim,SM_FONT,'left','middle');
  if(Ly.bottom[0]){
    const p=Ly.bottom[0];
    axesFit(rc,p,0,xhi,0,100,{title:byCon?'T against concentration':'T against path length',
      xlab:byCon?L.d.transform:'cm',ylab:'T, %',xfmt:xf,yfmt:t=>fmt(t,0)});
    polyline(rc,p,xs,(byCon?L.Tc:L.Tl).map(v=>100*v),0,xhi,0,100,COL.struct,2);
    marker(rc,p,0,xhi,0,100,byCon?L.c:L.l,100*L.T,COL.live);
    lab(rc,W,H,p.x+12,p.y+14,'a curve, not a line',COL.dim,SM_FONT,'left','middle');
  }
  if(Ly.bottom[1]){
    const p=Ly.bottom[1];
    axesFit(rc,p,0,4,0,100,{title:'T = 10^-A — every solution at once',
      xlab:'absorbance A',ylab:'T, %',xfmt:t=>fmt(t,0),yfmt:t=>fmt(t,0)});
    polyline(rc,p,L.As,L.Ts.map(v=>100*v),0,4,0,100,COL.pos,2);
    for(const a of [1,2,3]){
      polyline(rc,p,[a,a],[0,100*transmittance(a)],0,4,0,100,COL.ref,1,[4,4]);
      lab(rc,W,H,p.x+p.w*a/4+4,p.y1-p.h*transmittance(a)-10,
          fmt(100*transmittance(a),100*transmittance(a)<1?1:0)+' %',COL.ref,SM_FONT,'left','middle');
    }
    marker(rc,p,0,4,0,100,clamp(L.A,0,4),100*L.T,COL.live);
  }
  drawCaption(rc,{left:Ly.left,capY:Ly.capY,capTxt:Ly.capTxt,capW:Ly.capW});
}

