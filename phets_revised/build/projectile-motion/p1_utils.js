
/* ================================================================== *
 *  numbers and the 2-D plotting layer.  Base: diffraction.html's       *
 *  drawing helpers (PLAYBOOK recipe).  Each block that the Known-bad   *
 *  list has since fixed is taken from the sim that carries the fix,    *
 *  named below, and asserted in selfTest section 0 so it cannot rot.   *
 * ================================================================== */
/* fmt, sigf — buoyancy.html (lineage sbs_sims.html); non-finite prints '—' */
function fmt(x,n){ return isFinite(x)?Number(x).toFixed(n===undefined?3:n):'—'; }
function sigf(x,n){
  if(!isFinite(x)) return '—';
  if(x===0) return '0';
  n=n||3;
  const a=Math.abs(x);
  if(a>=1e5||a<1e-4) return x.toExponential(n-1).replace('e','×10^');
  const d=Math.max(0,n-1-Math.floor(Math.log10(a)));
  return x.toFixed(Math.min(d,8));
}
/* ENTS + plain() — buoyancy.html (lineage sbs_sims.html): strips TAGS, decodes
   named AND numeric entities inside ONE wide match (a separate numeric pass
   makes narrowing the wide regex an equivalent mutant — sbs_state_surface
   Known-bad), capitals included (&Delta;).  Unknown entities pass through so
   the audits still see them.  Extended with the symbols this file writes. */
const ENTS={'&rsquo;':'’','&lsquo;':'‘','&mdash;':'—','&ndash;':'–',
            '&times;':'×','&deg;':'°','&nbsp;':' ','&minus;':'−',
            '&amp;':'&','&lt;':'<','&gt;':'>','&hellip;':'…',
            '&alpha;':'α','&beta;':'β','&gamma;':'γ','&delta;':'δ',
            '&epsilon;':'ε','&eta;':'η','&kappa;':'κ','&lambda;':'λ',
            '&mu;':'μ','&nu;':'ν','&pi;':'π','&rho;':'ρ',
            '&sigma;':'σ','&tau;':'τ','&phi;':'φ','&omega;':'ω',
            '&theta;':'θ','&Gamma;':'Γ','&Delta;':'Δ','&Lambda;':'Λ',
            '&Pi;':'Π','&Sigma;':'Σ','&Phi;':'Φ','&Omega;':'Ω',
            '&plusmn;':'±','&ne;':'≠','&asymp;':'≈','&equiv;':'≡',
            '&prop;':'∝','&radic;':'√','&infin;':'∞','&middot;':'·',
            '&rarr;':'→','&larr;':'←','&ell;':'ℓ','&sup2;':'²',
            '&sup3;':'³','&frac12;':'½','&le;':'≤','&ge;':'≥',
            '&prime;':'′','&Prime;':'″','&rArr;':'⇒','&hArr;':'⇔','&int;':'∫','&perp;':'⊥','&star;':'☆'};
function plain(s){
  return String(s).replace(/<\/?[a-zA-Z][^>]*>/g,'')
    .replace(/&#?[a-zA-Z0-9]+;/g,m=>{
      if(ENTS[m]!==undefined) return ENTS[m];
      let d=/^&#([0-9]+);$/.exec(m);
      if(d) return String.fromCodePoint(+d[1]);
      d=/^&#x([0-9a-fA-F]+);$/.exec(m);
      if(d) return String.fromCodePoint(parseInt(d[1],16));
      return m;
    });
}
/* wrapText, caption, box, frame, ticksFor — diffraction.html, unchanged.
   Text is wrapped on a MEASURED width, never on a character count. */
function wrapText(ctx,txt,maxW,font){
  if(font) ctx.font=font;
  const words=plain(txt).split(/\s+/), out=[]; let line='';
  for(const w of words){
    const t=line?line+' '+w:w;
    if(line&&ctx.measureText(t).width>maxW){ out.push(line); line=w; }
    else line=t;
  }
  if(line) out.push(line);
  return out;
}
function caption(ctx,x,y,txt,maxW,col,font){
  const f=font||'11.5px -apple-system, sans-serif';
  const ls=wrapText(ctx,txt,maxW,f);
  ctx.fillStyle=col||'#767e92'; ctx.textAlign='left'; ctx.textBaseline='top';
  for(let i=0;i<ls.length;i++) ctx.fillText(ls[i],x,y+i*14);
  return ls.length*14;
}
function box(x,y,w,hh){ return {x,y,w,h:hh,x1:x+w,y1:y+hh}; }
function frame(ctx,b,col){
  ctx.strokeStyle=col||'#232838'; ctx.lineWidth=1;
  ctx.strokeRect(Math.round(b.x)+0.5,Math.round(b.y)+0.5,Math.round(b.w),Math.round(b.h));
}
function ticksFor(lo,hi,want){
  const span=hi-lo; if(!(span>0)) return [lo];
  const raw=span/Math.max(2,want);
  const mag=Math.pow(10,Math.floor(Math.log10(raw)));
  const norm=raw/mag;
  const step=(norm<1.5?1:norm<3?2:norm<7?5:10)*mag;
  const out=[];
  for(let t=Math.ceil(lo/step)*step;t<=hi+step*1e-6;t+=step) out.push(t);
  return out;
}
/* tick labels take their decimals from the tick SPACING, never a fixed count
   (Known-bad, adiabatic_expansion: fmt(t,2) printed "318.00" six times into a
   210-px panel).  A float residue like -1e-17 must not print as "-0.0". */
function tickFmt(ts){
  const st=ts.length>1?Math.abs(ts[1]-ts[0]):0;
  const d=st>0?Math.max(0,Math.min(6,-Math.floor(Math.log10(st)+1e-9))):0;
  return v=>{ const s=Number(v).toFixed(d); return /^-0(\.0*)?$/.test(s)?s.slice(1):s; };
}
/* axes — buoyancy.html (lineage standard_candle / drum_head): the range is
   SORTED before asking for ticks (an inverted axis otherwise collapses to one
   tick), labels go through plain(), the title sits at b.y-9 clear of the top
   y-tick; plus the spacing-derived tick formatter above.  Two additions: the
   tick count follows the box's PIXELS (at most one x tick per 48 px, one y
   tick per 26 px), and every tick label is registered in LABELS so marker
   labels placed later dodge it (both found by the layout sweep at 560x380). */
function axes(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=opt||{};
  ctx.save();
  frame(ctx,b,'#242a3a');
  ctx.font='10.5px -apple-system, sans-serif';
  const nx=Math.max(2,Math.min(o.nx||6,Math.floor(b.w/48))), ny=Math.max(2,Math.min(o.ny||5,Math.floor(b.h/26)));
  const xt=o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),nx);
  const yt=o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),ny);
  const xf=o.xfmt||tickFmt(xt), yf=o.yfmt||tickFmt(yt);
  ctx.strokeStyle='#181d29'; ctx.lineWidth=1;
  ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle='#6f7789';
  for(const t of xt){
    const X=b.x+b.w*(t-xlo)/(xhi-xlo||1);
    if(X<b.x-0.5||X>b.x1+0.5) continue;
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke();
    const s=xf(t), w=s.length*10.5*0.52; ctx.fillText(s,X,b.y1+5); LABELS.push([X-w/2,b.y1+5,X+w/2,b.y1+5+10.5*1.15]);
  }
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(const t of yt){
    const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1);
    if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    ctx.beginPath(); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); ctx.stroke();
    const s=yf(t), w=s.length*10.5*0.52; ctx.fillText(s,b.x-6,Y); LABELS.push([b.x-6-w,Y-6,b.x-6,Y+6]);
  }
  if(o.xlab){ ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle='#8b93a6';
    ctx.font='11px -apple-system, sans-serif'; ctx.fillText(plain(o.xlab),b.x+b.w/2,b.y1+21); }
  if(o.ylab){ ctx.save(); ctx.translate(b.x-40,b.y+b.h/2); ctx.rotate(-PI/2);
    ctx.textAlign='center'; ctx.textBaseline='bottom'; ctx.fillStyle='#8b93a6';
    ctx.font='11px -apple-system, sans-serif'; ctx.fillText(plain(o.ylab),0,0); ctx.restore(); }
  if(o.title){ ctx.textAlign='left'; ctx.textBaseline='bottom'; ctx.fillStyle='#aeb6c6';
    ctx.font='italic 13px Georgia, serif'; ctx.fillText(plain(o.title),b.x,b.y-9); }
  ctx.restore();
}
/* polyline — buoyancy.html (lineage pupil_plane_interferometry): CLIPPED IN
   DATA SPACE, Liang-Barsky, in x AND y — a canvas clip() would fix the browser
   and not the display-list audit, and the endpoint test the siblings used
   drops a segment whose both ends are outside.  Every emitted segment is
   recorded in POLY_SEGS so selfTest can keep legends off the curves. */
let POLY_SEGS=[];
function polyline(ctx,b,xs,ys,xlo,xhi,ylo,yhi,col,lw,dash){
  ctx.save();
  ctx.beginPath();
  const n=Math.min(xs.length,ys.length);
  const px=x=>b.x+b.w*(x-xlo)/(xhi-xlo||1);
  const py=y=>b.y1-b.h*(y-ylo)/(yhi-ylo||1);
  const xa=Math.min(xlo,xhi), xb=Math.max(xlo,xhi), ya=Math.min(ylo,yhi), yb=Math.max(ylo,yhi);
  let started=false;
  for(let i=0;i<n-1;i++){
    const X0=xs[i], Y0=ys[i], X1=xs[i+1], Y1=ys[i+1];
    if(!isFinite(X0)||!isFinite(Y0)||!isFinite(X1)||!isFinite(Y1)){ started=false; continue; }
    let t0=0,t1=1; const dx=X1-X0, dy=Y1-Y0; let out=false;
    for(const [p,q] of [[-dx,X0-xa],[dx,xb-X0],[-dy,Y0-ya],[dy,yb-Y0]]){
      if(p===0){ if(q<0){ out=true; break; } continue; }
      const t=q/p;
      if(p<0){ if(t>t1){ out=true; break; } if(t>t0) t0=t; }
      else { if(t<t0){ out=true; break; } if(t<t1) t1=t; }
    }
    if(out||t0>t1){ started=false; continue; }
    const x0=X0+t0*dx, y0=Y0+t0*dy, x1=X0+t1*dx, y1=Y0+t1*dy;
    if(t0>0) started=false;
    if(!started){ ctx.moveTo(px(x0),py(y0)); started=true; }
    ctx.lineTo(px(x1),py(y1));
    POLY_SEGS.push(px(x0),py(y0),px(x1),py(y1));
    if(t1<1) started=false;
  }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.6;
  if(dash) ctx.setLineDash(dash);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}
/* legendBox / legendAuto — buoyancy.html (lineage adiabatic_expansion): the
   legend records its TEXT rectangle, and the placement tries the corners
   against the curves already drawn; no clear corner means no legend. */
let LEGEND_RECTS=[];
function legendBox(ctx,x,y,items){
  ctx.font='10.5px -apple-system, sans-serif';
  let w=0;
  for(const it of items) w=Math.max(w,ctx.measureText(plain(it[1])).width);
  const bw=w+26, bh=items.length*15+8;
  ctx.fillStyle='rgba(10,12,18,.78)'; ctx.fillRect(x,y,bw,bh);
  frame(ctx,box(x,y,bw,bh),'#242a3a');
  ctx.textAlign='left'; ctx.textBaseline='middle';
  items.forEach((it,i)=>{
    const yy=y+11+i*15;
    ctx.fillStyle=it[0]; ctx.fillRect(x+7,yy-3.5,10,7);
    ctx.fillStyle='#9aa2b4'; ctx.fillText(plain(it[1]),x+22,yy);
  });
  LEGEND_RECTS.push({x:x+22,y,w:bw-22,h:bh});
  LABELS.push([x,y,x+bw,y+bh]);
  return box(x,y,bw,bh);
}
function legendAuto(ctx,b,items){
  ctx.font='10.5px -apple-system, sans-serif';
  let w=0;
  for(const it of items) w=Math.max(w,ctx.measureText(plain(it[1])).width);
  const bw=w+26, bh=items.length*15+8;
  if(bw>b.w-16||bh>b.h-16) return null;
  const mx=b.x+(b.w-bw)/2, my=b.y+(b.h-bh)/2;
  const cands=[[b.x1-bw-8,b.y+8],[b.x+8,b.y1-bh-8],[b.x+8,b.y+8],
               [b.x1-bw-8,b.y1-bh-8],[mx,b.y+8],[mx,b.y1-bh-8],
               [b.x+8,my],[b.x1-bw-8,my]];
  for(const [cx,cy] of cands){
    let hit=false;
    for(let i=0;i<POLY_SEGS.length&&!hit;i+=4){
      const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
      if(Math.max(x0,x1)<cx||Math.min(x0,x1)>cx+bw||
         Math.max(y0,y1)<cy||Math.min(y0,y1)>cy+bh) continue;
      hit=true;
    }
    if(!hit&&labFits([cx,cy,cx+bw,cy+bh])) return legendBox(ctx,cx,cy,items);
  }
  return null;
}
/* the label registry — buoyancy.html p4 (lineage build_cycloid): a label that
   would overlap one already placed (at the audit's half-pixel rule) shifts,
   and if no shift fits it is dropped rather than drawn on top of another. */
let LABELS=[];
function labFits(bx){
  for(const o of LABELS) if(bx[0]<o[2]-0.5&&bx[2]>o[0]+0.5&&bx[1]<o[3]-0.5&&bx[3]>o[1]+0.5) return false;
  return true;
}
function lab(ctx,W,H,x,y,txt,col,font,align,base){
  ctx.fillStyle=col||'#aeb6c6'; ctx.font=font||'11px -apple-system, sans-serif';
  const al=align||'left', bl=base||'middle';
  ctx.textAlign=al; ctx.textBaseline=bl;
  const t=plain(txt), fs=parseFloat((font||'11px').match(/([\d.]+)px/)[1]), w=t.length*fs*0.52, hh=fs*1.15;
  for(const dy of [0,16,-16,32,-32]){
    let X=x, Y=y+dy;
    if(al==='left') X=clamp(X,2,W-w-2); else if(al==='right') X=clamp(X,w+2,W-2); else X=clamp(X,w/2+2,W-w/2-2);
    Y=clamp(Y,hh,H-hh);
    const lx=al==='center'?X-w/2:(al==='right'?X-w:X);
    const ly=bl==='top'?Y:(bl==='middle'?Y-hh/2:(bl==='bottom'?Y-hh:Y-hh*0.8));
    const bx=[lx,ly,lx+w,ly+hh];
    if(labFits(bx)){ LABELS.push(bx); ctx.fillText(t,X,Y); return true; }
  }
  return false;
}
function titleFor(b,longT,shortT){ return (b.w<330||plain(longT).length*13*0.52+10>b.w)?shortT:longT; }
function axesR(ctx,b,xlo,xhi,ylo,yhi,opt){
  axes(ctx,b,xlo,xhi,ylo,yhi,opt);
  if(opt&&opt.title){ const t=plain(opt.title), w=t.length*13*0.52; LABELS.push([b.x,b.y-9-13*1.15,b.x+w,b.y-9]); }
}
/* layout from the bottom up — buoyancy.html: measure the caption FIRST
   (wrapped text has no fixed height), then give the plots what is left */
function stageTop(){ return 46; }
function capFit(ctx,W,H,txt,capW){
  const lines=wrapText(ctx,txt,capW,'11.5px -apple-system, sans-serif').length;
  return {capY:H-12-lines*14,lines};
}
function fitCaption(ctx,W,H,fullTxt,shortTxt,capWraw,minTop){
  const capW=Math.max(300,Math.min(capWraw,W-148));
  let fit=capFit(ctx,W,H,fullTxt,capW);
  if(fit.capY>=minTop) return {capY:fit.capY,txt:fullTxt,capW};
  fit=capFit(ctx,W,H,shortTxt,capW);
  return {capY:fit.capY,txt:shortTxt,capW};
}
