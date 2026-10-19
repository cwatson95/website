/* ================================================================== *
 *  small utilities  (extracted from sbs_sims.html, via                 *
 *  build_lagr/p1_utils.js, verbatim)                                  *
 * ================================================================== */
const clamp=(x,a,b)=>x<a?a:x>b?b:x;
const lerp=(a,b,t)=>a+(b-a)*t;
const TAU=Math.PI*2, PI=Math.PI;
const smoothstep=t=>t*t*(3-2*t);

/* Accepts '#rgb', '#rrggbb' AND 'rgb(r,g,b)' — mix() returns the latter, so its
   own output must be a legal input or a two-stage blend silently turns black:
   parseInt('rgb(58,111,142)', 16) is NaN, and NaN & 255 is 0, which yields a
   perfectly well-formed rgb(0,0,0) and no error anywhere.  Unparseable input
   THROWS rather than defaulting.  (Known-bad list, steam_carnot_cycle.html.) */
function toRgb(c){
  const s=''+c;
  const m=s.match(/^rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)/);
  if(m) return [Math.round(+m[1]),Math.round(+m[2]),Math.round(+m[3])];
  let h=s.replace('#','');
  if(h.length===3) h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
  if(!/^[0-9a-fA-F]{6}$/.test(h)) throw new Error('toRgb: cannot parse colour "'+s+'"');
  const n=parseInt(h,16); return [(n>>16)&255,(n>>8)&255,n&255];
}
function mix(a,b,t){ const A=toRgb(a),B=toRgb(b);
  return 'rgb('+Math.round(A[0]+(B[0]-A[0])*t)+','+Math.round(A[1]+(B[1]-A[1])*t)+','
              +Math.round(A[2]+(B[2]-A[2])*t)+')'; }
function rgba(hex,a){ const c=toRgb(hex); return 'rgba('+c[0]+','+c[1]+','+c[2]+','+a+')'; }
function shade(col,sh){ return mix('#070b18',col,clamp(sh,0,1)); }
/* Mathematica NeonColors — same table as the other sims in this collection */
const NEON_STOPS=[
  [0.0000,0.7203,0.9238,0.2976],[0.0667,0.7332,0.8250,0.2939],
  [0.1333,0.7462,0.7263,0.2903],[0.2000,0.7591,0.6275,0.2866],
  [0.2667,0.7720,0.5287,0.2830],[0.3333,0.7849,0.4300,0.2793],
  [0.4000,0.8089,0.3632,0.2617],[0.4667,0.8316,0.3178,0.2550],
  [0.5333,0.8515,0.3153,0.2700],[0.6000,0.8580,0.3213,0.3191],
  [0.6667,0.8577,0.3317,0.3854],[0.7333,0.8473,0.3071,0.4623],
  [0.8000,0.8369,0.2825,0.5391],[0.8667,0.8266,0.2578,0.6160],
  [0.9333,0.8162,0.2332,0.6929],[1.0000,0.8058,0.2086,0.7698],
];
function neon(t){
  t=clamp(t,0,1); const S=NEON_STOPS; let i=0;
  while (i<S.length-2 && t>S[i+1][0]) i++;
  const a=S[i], b=S[i+1], f=(t-a[0])/((b[0]-a[0])||1);
  return [a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f, a[3]+(b[3]-a[3])*f];
}
function neonCss(t){ const c=neon(t);
  return 'rgb('+Math.round(255*c[0])+','+Math.round(255*c[1])+','+Math.round(255*c[2])+')'; }

/* tiny DOM helper (only touched when a document exists) */
function h(tag,attrs){
  const e=document.createElement(tag);
  if(attrs) for(const k in attrs){
    if(k==='class') e.className=attrs[k];
    else if(k==='html') e.innerHTML=attrs[k];
    else if(k.slice(0,2)==='on') e.addEventListener(k.slice(2),attrs[k]);
    else e.setAttribute(k,attrs[k]);
  }
  for(let i=2;i<arguments.length;i++){
    const c=arguments[i]; if(c==null) continue;
    e.appendChild(typeof c==='string'?document.createTextNode(c):c);
  }
  return e;
}
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
            '&prime;':'′','&Prime;':'″','&rArr;':'⇒','&hArr;':'⇔','&oint;':'∮','&int;':'∫','&perp;':'⊥','&ycirc;':'ŷ'};
/* plain(): strips tags, decodes numeric + named entities.  The wide regex and
   the numeric decode INSIDE its handler are both load-bearing: the narrow
   /&[a-z]+;/ let &#955; and &Lambda; reach the canvas verbatim (wave_fronts
   Known-bad), and a SEPARATE numeric pass makes narrowing the wide match an
   equivalent mutant the sweep cannot see (sbs_state_surface Known-bad).
   Unknown named entities pass through unchanged so the audits still see them. */
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
/* log-axis ticks (decades), guarded: a non-positive bound is an infinite loop
   in a naive generator (sbs_sims Known-bad) — return [] instead */
function logTicks(lo,hi){
  if(!(lo>0)||!(hi>0)||!isFinite(lo)||!isFinite(hi)) return [];
  const out=[];
  const e0=Math.floor(Math.log10(lo)), e1=Math.ceil(Math.log10(hi));
  const step=(e1-e0)>7?2:1;
  for(let e=e0;e<=e1;e+=step){ const v=Math.pow(10,e); if(v>=lo*0.999&&v<=hi*1.001) out.push(v); }
  return out;
}
function axes(ctx,b,xlo,xhi,ylo,yhi,opt){
  const o=opt||{};
  ctx.save();
  frame(ctx,b,'#242a3a');
  ctx.font='10.5px -apple-system, sans-serif';
  /* ticksFor returns a SINGLE value when hi < lo, so an inverted axis silently
     gets one tick and no grid.  Sort the range before asking for ticks; the
     placement below already handles either direction. (standard_candle.html) */
  const xt=o.xticks||ticksFor(Math.min(xlo,xhi),Math.max(xlo,xhi),o.nx||6);
  const yt=o.yticks||ticksFor(Math.min(ylo,yhi),Math.max(ylo,yhi),o.ny||5);
  ctx.strokeStyle='#181d29'; ctx.lineWidth=1;
  ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle='#6f7789';
  for(const t of xt){
    const X=b.x+b.w*(t-xlo)/(xhi-xlo||1);
    if(X<b.x-0.5||X>b.x1+0.5) continue;
    ctx.beginPath(); ctx.moveTo(X,b.y); ctx.lineTo(X,b.y1); ctx.stroke();
    ctx.fillText(o.xfmt?o.xfmt(t):fmt(t,2),X,b.y1+5);
  }
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(const t of yt){
    const Y=b.y1-b.h*(t-ylo)/(yhi-ylo||1);
    if(Y<b.y-0.5||Y>b.y1+0.5) continue;
    ctx.beginPath(); ctx.moveTo(b.x,Y); ctx.lineTo(b.x1,Y); ctx.stroke();
    ctx.fillText(o.yfmt?o.yfmt(t):fmt(t,2),b.x-6,Y);
  }
  /* labels go through plain() too — axis titles have carried '&ndash;' raw
     onto the canvas before (drum_head.html, Known-bad) */
  if(o.xlab){ ctx.textAlign='center'; ctx.textBaseline='top'; ctx.fillStyle='#8b93a6';
    ctx.font='11px -apple-system, sans-serif'; ctx.fillText(plain(o.xlab),b.x+b.w/2,b.y1+21); }
  if(o.ylab){ ctx.save(); ctx.translate(b.x-40,b.y+b.h/2); ctx.rotate(-PI/2);
    ctx.textAlign='center'; ctx.textBaseline='bottom'; ctx.fillStyle='#8b93a6';
    ctx.font='11px -apple-system, sans-serif'; ctx.fillText(plain(o.ylab),0,0); ctx.restore(); }
  /* title baseline at b.y-9, not b.y-6: the topmost y-tick label is centred on
     b.y and a 10.5px font spans +/-5.25 px, so a 6 px gap collides with it. */
  if(o.title){ ctx.textAlign='left'; ctx.textBaseline='bottom'; ctx.fillStyle='#aeb6c6';
    ctx.font='italic 13px Georgia, serif'; ctx.fillText(plain(o.title),b.x,b.y-9); }
  ctx.restore();
}
/* Polyline, CLIPPED IN DATA SPACE to the y-range AND the x-range (the
   siblings clip y only).  A canvas ctx.clip() would fix the browser but NOT
   the audit — the display-list recorder treats clip() as a no-op, so the
   captured geometry would still lie.  Crossings are interpolated so a clipped
   curve still meets the frame edge exactly.
   Every emitted segment is also recorded in POLY_SEGS (screen coords), which
   is what lets selfTest assert that no data curve crosses a legend box. */
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
    /* Liang-Barsky: the parameter range [t0,t1] of the segment inside the box.
       A segment whose BOTH endpoints lie outside can still cross the box; the
       endpoint-only test the siblings used dropped it. */
    let t0=0,t1=1; const dx=X1-X0, dy=Y1-Y0; let out=false;
    for(const [p,q] of [[-dx,X0-xa],[dx,xb-X0],[-dy,Y0-ya],[dy,yb-Y0]]){
      if(p===0){ if(q<0){ out=true; break; } continue; }
      const t=q/p;
      if(p<0){ if(t>t1){ out=true; break; } if(t>t0) t0=t; }
      else { if(t<t0){ out=true; break; } if(t<t1) t1=t; }
    }
    if(out||t0>t1){ started=false; continue; }
    const x0=X0+t0*dx, y0=Y0+t0*dy, x1=X0+t1*dx, y1=Y0+t1*dy;
    if(t0>0) started=false;                 /* enters the box part-way: new stroke */
    if(!started){ ctx.moveTo(px(x0),py(y0)); started=true; }
    ctx.lineTo(px(x1),py(y1));
    POLY_SEGS.push(px(x0),py(y0),px(x1),py(y1));
    if(t1<1) started=false;                 /* leaves the box: the next stroke restarts */
  }
  ctx.strokeStyle=col; ctx.lineWidth=lw||1.6;
  if(dash) ctx.setLineDash(dash);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}
/* legend that RECORDS its own text rectangle, so selfTest can assert no data
   polyline runs through one (adiabatic_expansion lesson).  Reset per draw. */
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
  return box(x,y,bw,bh);
}
/* pick the first corner of panel b that no already-recorded curve segment
   crosses — call AFTER the panel's polylines are drawn (Known-bad: deciding
   which corner is empty by looking at one configuration keeps being wrong) */
function legendAuto(ctx,b,items){
  ctx.font='10.5px -apple-system, sans-serif';
  let w=0;
  for(const it of items) w=Math.max(w,ctx.measureText(plain(it[1])).width);
  const bw=w+26, bh=items.length*15+8;
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
    if(!hit) return legendBox(ctx,cx,cy,items);
  }
  /* every spot is crossed: draw no legend rather than a lying one — the
     caption names the colours */
  return null;
}

function stageTop(){ return 46; }
/* measure a caption BEFORE laying out the panel above it (Known-bad: wrapped
   text has no fixed height) — returns {capY, lines} for a bottom-anchored cap */
function capFit(ctx,W,H,txt,capW){
  const lines=wrapText(ctx,txt,capW,'11.5px -apple-system, sans-serif').length;
  return {capY:H-12-lines*14,lines};
}
function sparseTicks(lo,hi,hpx){
  return ticksFor(lo,hi,hpx<90?2:(hpx<140?3:5));
}
/* choose the full caption if the panel above it keeps at least minTop of
   height, else a one-line fallback (sparse-view honesty at tiny sizes).
   capW is floored: at very narrow widths text may run under the floating
   readout, which the audit reports as advisory, like the siblings. */
function fitCaption(ctx,W,H,fullTxt,shortTxt,capWraw,minTop){
  const capW=Math.max(300,Math.min(capWraw,W-148));
  let fit=capFit(ctx,W,H,fullTxt,capW);
  if(fit.capY>=minTop) return {capY:fit.capY,txt:fullTxt,capW};
  fit=capFit(ctx,W,H,shortTxt,capW);
  return {capY:fit.capY,txt:shortTxt,capW};
}
function intTicks(lo,hi){
  const out=[];
  for(let t=Math.ceil(lo);t<=Math.floor(hi);t++) out.push(t);
  return out.length?out:[Math.round(lo)];
}

