/* ================================================================== *
 *  the analysis views: nodes and branches, the power budget, the      *
 *  rest of the circuit, one battery at a time; drawView; the scene    *
 * ================================================================== */
/* the stage left of the floating readout on a wide canvas, full width on a
   narrow one; captions are measured first and laid out from the bottom up,
   ending HINT_H above the canvas edge (the #hint owns the last line) */
function viewFrame(ctx,W,H,capFull,capShort){
  const narrow=W<900, left=56, right=narrow?W-26:W-RO_W-44;
  const capW=Math.max(260,Math.min(W-148,(narrow?W-26:W-40)-left));
  const top=stageTop()+30;
  const fit=fitCaption(ctx,W,H-HINT_H,capFull,capShort,capW,top+240);
  return {narrow,left,right,top,capY:fit.capY,capTxt:fit.txt,capW,full:W-40};
}
function sayWhy(ctx,W,H,txt){ caption(ctx,70,stageTop()+60,txt,Math.min(520,W-140),'#8b93a6','12.5px -apple-system, sans-serif'); }
/* the parts worth a row in a chart: everything but the wires */
function chartParts(SOL,C){ return C.els.filter(e=>e.type!=='wire'&&SOL.onK.has(e.id)); }
const LETTER={battery:'B',xbattery:'B',resistor:'R',xresistor:'R',bulb:'L',xbulb:'L',rbulb:'L',switch:'S',fuse:'F',ammeter:'A',
              coin:'c',clip:'c',pencil:'p',tpencil:'p',eraser:'e',bill:'d',wire:''};

/* ---------------- nodes and branches ---------------- */
const GRAPH_CAP_FULL='Every joint is a node and every part a branch, wires included, as in PhET’s solver. Cyan: a spanning tree; dashed: the chords, each of which closes one fundamental loop (B − N + C of them). Green arrows: the conventional current. The matrix is the system solved: the current law at every node but one per piece (top block) and each branch’s own law v(a) − v(b) − R i = −E (bottom block); cyan +1, orange −1, green −R. Below, both of Kirchhoff’s laws measured on the answer against the piece’s own scale, with the double-precision epsilon for comparison.';
const GRAPH_CAP_SHORT='The circuit as a graph (tree cyan, chords dashed), and Kirchhoff’s laws measured on the answer.';
/* the narrow stage has no room for the matrix, so its caption must not describe one */
const GRAPH_CAP_NARROW='Every joint is a node and every part a branch, wires included, as in PhET’s solver. Cyan: a spanning tree; dashed: the chords, each of which closes one fundamental loop (B − N + C of them). Green arrows: the conventional current. Below, both of Kirchhoff’s laws measured on the answer against the piece’s own scale, with the double-precision epsilon for comparison; a wider window shows the matrix itself.';
function drawGraph(ctx,W,H,M){
  const SOL=M.sol, C=M.st.circ;
  if(!C.els.length){ sayWhy(ctx,W,H,'There is nothing on the bench, so there is no graph to draw and no matrix to solve. Build a circuit in the lab, or pick one of the circuits in the panel.'); return; }
  const V=viewFrame(ctx,W,H,W<900?GRAPH_CAP_NARROW:GRAPH_CAP_FULL,GRAPH_CAP_SHORT);
  const stripH=Math.max(70,Math.min(120,(V.capY-V.top)*0.28));
  const topH=V.capY-24-stripH-46-V.top;
  const gW=V.narrow?V.right-V.left:Math.round((V.right-V.left)*0.56);
  const GB=box(V.left,V.top,gW,Math.max(90,topH));
  const MB=V.narrow?null:box(GB.x1+44,V.top,V.right-GB.x1-44,Math.max(90,topH));
  const RB=box(V.left,GB.y1+46,V.full-V.left,stripH);
  /* the graph: equal aspect, fitted to its box */
  let xmin=1e9,xmax=-1e9,ymin=1e9,ymax=-1e9;
  for(const v of C.verts){ xmin=Math.min(xmin,v.x); xmax=Math.max(xmax,v.x); ymin=Math.min(ymin,v.y); ymax=Math.max(ymax,v.y); }
  const pad=30, s=Math.min(GB.w/Math.max(1,xmax-xmin+2*pad),GB.h/Math.max(1,ymax-ymin+2*pad));
  const ox=GB.x+(GB.w-s*(xmax-xmin))/2-xmin*s, oy=GB.y+(GB.h-s*(ymax-ymin))/2-ymin*s;
  const P=v=>[ox+s*v.x,oy+s*v.y];
  frame(ctx,GB,'#242a3a');
  textAt(ctx,GB.x,GB.y-9,titleFor(GB,'the circuit as a graph: '+SOL.nodes+' nodes, '+SOL.branches+' branches, '+SOL.loops+' loops','the graph'),'#aeb6c6','italic 13px Georgia, serif','left','bottom');
  LABELS.push([GB.x,GB.y-24,GB.x+Math.min(GB.w,420),GB.y-9]);
  const br=SOL.net.br, tree=SOL.basis.tree, idx=SOL.net.idx;
  const vAt=new Map(); C.verts.forEach(v=>vAt.set(v.id,P(v)));
  br.forEach((e,k)=>{ const A=vAt.get(e.el.a), B=vAt.get(e.el.b);
    strokePts(ctx,[A,B],tree[k]?COL.struct:mix(COL.struct,'#070b18',0.25),tree[k]?2:1.6,tree[k]?null:[6,4]);
    POLY_SEGS.push(A[0],A[1],B[0],B[1]); });
  for(const el of SOL.net.off){ const A=vAt.get(el.a), B=vAt.get(el.b); strokePts(ctx,[A,B],'#3a4152',1.2,[2,4]); }
  /* current arrows and part letters at each branch's middle */
  const Imax=Math.max(SOL.Imax,1e-300);
  br.forEach((e,k)=>{ const A=vAt.get(e.el.a), B=vAt.get(e.el.b), I=SOL.sol.i[k];
    const mx=(A[0]+B[0])/2, my=(A[1]+B[1])/2, L=Math.hypot(B[0]-A[0],B[1]-A[1])||1, ux=(B[0]-A[0])/L, uy=(B[1]-A[1])/L;
    if(Math.abs(I)>1e-9*Imax&&L>14){ const d=I>0?1:-1, h=Math.min(9,L*0.3);
      fillPts(ctx,[[mx+d*ux*h,my+d*uy*h],[mx-d*ux*h*0.6+uy*h*0.6,my-d*uy*h*0.6-ux*h*0.6],[mx-d*ux*h*0.6-uy*h*0.6,my-d*uy*h*0.6+ux*h*0.6]],COL.pos); }
    const lt=LETTER[e.el.type]; if(lt) lab(ctx,W,H,mx+uy*14,my-ux*14,lt,'#aeb6c6','italic 11px Georgia, serif','center','middle'); });
  /* nodes, shaded by potential within their piece */
  const vmin=Math.min(...C.verts.map(v=>SOL.V.get(v.id))), vmax=Math.max(...C.verts.map(v=>SOL.V.get(v.id)));
  C.verts.forEach((v,q)=>{ const p=vAt.get(v.id), t=vmax>vmin?(SOL.V.get(v.id)-vmin)/(vmax-vmin):0;
    const isRef=[...SOL.sol.ref.values()].indexOf(idx.get(v.id))>=0;
    fillPts(ctx,circlePts(p,isRef?6:4.5),mix('#2a3346','#e9ecf2',t),isRef?COL.ref:'#070b18',1.2); });
  /* a few node voltages, where they fit */
  const shown=[...C.verts].sort((a,b)=>Math.abs(SOL.V.get(b.id))-Math.abs(SOL.V.get(a.id)));
  let nl=0; for(const v of shown){ if(nl>=10) break; const p=vAt.get(v.id);
    if(lab(ctx,W,H,p[0]+8,p[1]-11,'n'+idx.get(v.id)+' '+fmtV(SOL.V.get(v.id)),'#8b93a6','10px -apple-system, sans-serif','left','middle')) nl++; }
  /* the matrix */
  if(MB) drawMatrix(ctx,W,H,MB,SOL);
  /* Kirchhoff on the answer */
  drawResiduals(ctx,W,H,RB,SOL);
  caption(ctx,V.left,V.capY,V.capTxt,V.capW,'#767e92',CAP_FONT);
}
function drawMatrix(ctx,W,H,MB,SOL){
  const br=SOL.net.br, S=mnaSystem(SOL.net.N,br), n=S.n, nv=S.nv;
  textAt(ctx,MB.x,MB.y-9,titleFor(MB,'the matrix, '+n+' × '+n+' = (N − C) + B','the matrix'),'#aeb6c6','italic 13px Georgia, serif','left','bottom');
  LABELS.push([MB.x,MB.y-24,MB.x+Math.min(MB.w,300),MB.y-9]);
  if(!n){ caption(ctx,MB.x,MB.y+8,'No unknowns: nothing is connected.',MB.w,'#8b93a6'); return; }
  const side=Math.min(MB.w-30,MB.h-18), cs=side/(n+1.6), x0=MB.x+14, y0=MB.y+4;
  /* the unscaled matrix: current law rows, then v_a - v_b - R i = -E rows */
  const cell=(r,c,col)=>fillPts(ctx,[[x0+c*cs,y0+r*cs],[x0+(c+1)*cs-0.6,y0+r*cs],[x0+(c+1)*cs-0.6,y0+(r+1)*cs-0.6],[x0+c*cs,y0+(r+1)*cs-0.6]],col);
  fillPts(ctx,[[x0,y0],[x0+n*cs,y0],[x0+n*cs,y0+n*cs],[x0,y0+n*cs]],'#0b0f1c','#242a3a',1);
  br.forEach((e,k)=>{ const c=nv+k;
    if(S.vi[e.a]>=0) cell(S.vi[e.a],c,COL.struct);
    if(S.vi[e.b]>=0) cell(S.vi[e.b],c,COL.ref);
    const r=nv+k;
    if(S.vi[e.a]>=0) cell(r,S.vi[e.a],COL.struct);
    if(S.vi[e.b]>=0) cell(r,S.vi[e.b],COL.ref);
    const g=clamp((Math.log10(e.R)+12)/18,0.15,1); cell(r,c,mix('#1c2410',COL.pos,g)); });
  /* the right-hand side: -E on the battery rows */
  const xr=x0+(n+0.6)*cs;
  fillPts(ctx,[[xr,y0],[xr+cs,y0],[xr+cs,y0+n*cs],[xr,y0+n*cs]],'#0b0f1c','#242a3a',1);
  br.forEach((e,k)=>{ if(e.E!==0){ const r=nv+k; fillPts(ctx,[[xr,y0+r*cs],[xr+cs-0.6,y0+r*cs],[xr+cs-0.6,y0+(r+1)*cs-0.6],[xr,y0+(r+1)*cs-0.6]],e.E>0?COL.ref:COL.struct); } });
  /* the block borders */
  strokePts(ctx,[[x0+nv*cs,y0],[x0+nv*cs,y0+n*cs]],'#8b93a6',1); strokePts(ctx,[[x0,y0+nv*cs],[x0+n*cs,y0+nv*cs]],'#8b93a6',1);
  if(cs*nv>=18&&cs*(n-nv)>=18){
    const fs='italic '+Math.round(clamp(cs*1.2,10,14))+'px Georgia, serif';
    textAt(ctx,x0+nv*cs/2,y0+nv*cs/2,'0','#6f7789',fs);
    lab(ctx,W,H,x0+(nv+(n-nv)/2)*cs,y0-2,'A (current law)','#8b93a6','10px -apple-system, sans-serif','center','bottom');
    lab(ctx,W,H,x0-3,y0+(nv+(n-nv)/2)*cs,'Aᵀ','#8b93a6','italic 11px Georgia, serif','right','middle'); }
  lab(ctx,W,H,xr+cs/2,y0+n*cs+10,'rhs','#8b93a6','10px -apple-system, sans-serif','center','middle');
}
function drawResiduals(ctx,W,H,RB,SOL){
  const L=SOL.law, pts=[];
  const idx=SOL.net.idx, comp=SOL.sol.comp;
  for(let q=0;q<SOL.net.N;q++){ const m=L.Isc.get(comp[q])||0; pts.push({kind:'node',r:m>0?Math.abs(L.node[q])/m:0}); }
  for(const p of L.per) pts.push({kind:'loop',r:p.scale>0?Math.abs(p.sum)/p.scale:0});
  const lo=-19, hi=-12, eps=Math.log10(Number.EPSILON);
  axesR(ctx,RB,0,Math.max(1,pts.length),lo,hi,{title:titleFor(RB,'Kirchhoff on the answer: '+SOL.nodes+' nodes (current law) and '+SOL.loops+' loops (voltage law), residual ÷ the piece’s scale','Kirchhoff on the answer'),
    xticks:[],yticks:[-18,-16,-14,-12],yfmt:v=>pow10(v)});
  polyline(ctx,RB,[0,Math.max(1,pts.length)],[eps,eps],0,Math.max(1,pts.length),lo,hi,COL.ref,1.1,[5,4]);
  lab(ctx,W,H,RB.x1-4,RB.y1-RB.h*(eps-lo)/(hi-lo)-8,'ε = 2.2×10⁻¹⁶','#e8a25a','10px -apple-system, sans-serif','right','bottom');
  const n=pts.length, bw=Math.max(2,Math.min(14,RB.w/Math.max(1,n)*0.6));
  pts.forEach((p,j)=>{ const x=RB.x+RB.w*(j+0.5)/Math.max(1,n), lg=p.r>0?clamp(Math.log10(p.r),lo,hi):lo;
    const y=RB.y1-RB.h*(lg-lo)/(hi-lo), col=p.kind==='node'?COL.pos:COL.struct;
    if(p.r>0) fillPts(ctx,[[x-bw/2,y],[x+bw/2,y],[x+bw/2,RB.y1],[x-bw/2,RB.y1]],col);
    else fillPts(ctx,circlePts([x,RB.y1-3],2.2,8),col); });
  if(SOL.nodes>0) lab(ctx,W,H,RB.x+6,RB.y+9,'green: nodes · cyan: loops · a dot on the floor: exactly zero','#8b93a6','10px -apple-system, sans-serif','left','middle');
}

/* ---------------- the power budget ---------------- */
const POWER_CAP_FULL='A waterfall: each battery’s EMF raises the running total by E i (green; a battery being charged would lower it), each resistance lowers it by i²R (orange) — the batteries’ own internal resistance included. It ends exactly where it began because of Tellegen’s theorem. Parts below 0.5 % of the total are pooled. Beneath: PhET’s brightness rule, with each bulb at its power; the power axis is logarithmic.';
const POWER_CAP_SHORT='Where each watt comes from (green) and goes (orange); PhET’s brightness curve below (log axis).';
function drawPower(ctx,W,H,M){
  const SOL=M.sol, C=M.st.circ, B=M.bud;
  if(!(B.gen>0)){ sayWhy(ctx,W,H,C.els.length?'No battery is delivering power: nothing flows in this circuit, so there is no power to budget. Close a loop through a battery.':'There is nothing on the bench. Build a circuit in the lab, or pick one in the panel.'); return; }
  const V=viewFrame(ctx,W,H,POWER_CAP_FULL,POWER_CAP_SHORT);
  const avail=V.capY-24-V.top, h1=Math.round(avail*0.58);
  const WB=box(V.left,V.top,V.right-V.left,Math.max(80,h1-40));
  const BB=box(V.left,WB.y1+56,(V.narrow?V.right:V.full)-V.left,Math.max(60,V.capY-24-(WB.y1+56)));
  /* the ledger: sources then sinks, small ones pooled */
  const tot=B.gen, items=[];
  /* sources that deliver come first, so the running total never dips below zero */
  B.src.slice().sort((a,b)=>b.P-a.P).forEach(x=>items.push({lab:elTag(C,x.el)+' EMF',P:x.P,src:true}));
  let pool=0, npool=0;
  B.sink.slice().sort((a,b)=>b.P-a.P).forEach(x=>{ if(x.P>=0.005*tot) items.push({lab:elTag(C,x.el)+(x.internal?' (its r)':''),P:-x.P}); else { pool+=x.P; npool++; } });
  if(npool) items.push({lab:npool+' more',P:-pool});
  let run=0, peak=0; for(const it of items){ run+=it.P; peak=Math.max(peak,run); }
  const n=items.length, ymax=Math.max(peak,tot)*1.1;
  axesR(ctx,WB,0,n,0,ymax,{title:titleFor(WB,'the running total: '+fmtP(B.gen)+' delivered, '+fmtP(B.dis)+' dissipated','the running total'),xticks:[],yfmt:v=>siFmt(v,'W',2)});
  let cum=0; const bw=Math.min(46,WB.w/n*0.62);
  items.forEach((it,j)=>{ const x=WB.x+WB.w*(j+0.5)/n, y0=cum, y1=cum+it.P; cum=y1;
    const Y=v=>WB.y1-WB.h*v/ymax, ya=Y(Math.max(y0,y1)), yb=Y(Math.min(y0,y1));
    fillPts(ctx,[[x-bw/2,ya],[x+bw/2,ya],[x+bw/2,Math.max(yb,ya+1)],[x-bw/2,Math.max(yb,ya+1)]],it.src?COL.pos:COL.ref);
    if(j<n-1){ const xn=WB.x+WB.w*(j+1.5)/n; strokePts(ctx,[[x+bw/2,Y(y1)],[xn-bw/2,Y(y1)]],'#4a5162',1,[2,3]); }
    lab(ctx,W,H,x,WB.y1+8,it.lab,'#8b93a6','10px -apple-system, sans-serif','center','top'); });
  /* the brightness curve */
  const bulbs=C.els.filter(e=>isBulb(e.type)&&SOL.onK.has(e.id));
  const lx0=-3, lx1=4;
  axesR(ctx,BB,lx0,lx1,0,1,{title:titleFor(BB,'PhET’s brightness b = ln(1 + 0.35 P) / ln(1 + 0.35·2000) against the bulb’s power (log axis)','brightness against power (log)'),
    xticks:[-3,-2,-1,0,1,2,3,4],xfmt:v=>siFmt(Math.pow(10,v),'W',1),yticks:[0.5,1],yfmt:v=>fmt(v,1)});
  const xs=[], ys=[]; for(let k=0;k<=140;k++){ const lp=lx0+(lx1-lx0)*k/140; xs.push(lp); ys.push(brightnessOf(Math.pow(10,lp))); }
  polyline(ctx,BB,xs,ys,lx0,lx1,0,1,COL.ref,1.6);
  if(!bulbs.length) lab(ctx,W,H,BB.x+10,BB.y+14,'no bulb in this circuit','#8b93a6','10.5px -apple-system, sans-serif','left','middle');
  bulbs.slice(0,8).forEach(e=>{ const Pw=SOL.P.get(e.id), bb=SOL.bright.get(e.id); if(!(Pw>0)) return;
    const lp=clamp(Math.log10(Pw),lx0,lx1), x=BB.x+BB.w*(lp-lx0)/(lx1-lx0), y=BB.y1-BB.h*bb;
    dot(ctx,x,y,4.5,COL.live,'#fff',1.2); lab(ctx,W,H,x+7,y-10,elTag(C,e),'#cfd4de','10.5px -apple-system, sans-serif','left','middle'); });
  caption(ctx,V.left,V.capY,V.capTxt,V.capW,'#767e92',CAP_FONT);
}

/* ---------------- the rest of the circuit ---------------- */
const THEV_CAP_FULL='Take the part out and look back into the two holes: whatever is there — batteries, resistors, the other bulbs — behaves exactly like one EMF Vth behind one resistance Rth. Orange: that line, v = Vth − Rth i. Green: the part’s own law (a resistor’s straight line through the origin, a battery’s line, a real bulb’s curve). Where they cross is the operating point (magenta), which is exactly what the full solve gives. On the right, the power this part would take as its resistance is swept: largest when it matches Rth.';
const THEV_CAP_SHORT='Orange: the rest of the circuit, v = Vth − Rth i; green: the part’s own law; magenta: where they cross.';
/* without the power sweep (a narrow stage, or a battery, which has no load resistance to sweep) */
const THEV_CAP_ONE='Take the part out and look back into the two holes: whatever is there — batteries, resistors, the other bulbs — behaves exactly like one EMF Vth behind one resistance Rth. Orange: that line, v = Vth − Rth i. Green: the part’s own law (a resistor’s straight line through the origin, a battery’s line, a real bulb’s curve). Where they cross is the operating point (magenta), which is exactly what the full solve gives.';
function drawThev(ctx,W,H,M){
  const T=M.thev, C=M.st.circ;
  if(!T){ sayWhy(ctx,W,H,'There is no part to look from: the bench is empty. Build a circuit, or pick one in the panel.'); return; }
  const e=elById(C,M.focus);
  if(T.open){ sayWhy(ctx,W,H,'Seen from the '+elTag(C,e)+', the rest of the circuit never comes back: take the part out and nothing joins its two ends. It is not in any loop, so no current can flow through it, whatever the batteries do.'); return; }
  const res=T.E===0, split=W>=900&&res;
  const V=viewFrame(ctx,W,H,split?THEV_CAP_FULL:THEV_CAP_ONE,THEV_CAP_SHORT);
  const IB=box(V.left,V.top,split?Math.round((V.right-V.left)*0.55):V.right-V.left,Math.max(90,V.capY-24-40-V.top));
  const PB=split?box(IB.x1+60,V.top,V.right-IB.x1-60,IB.h):null;
  const Voc=T.Voc, Rth=T.Rth, i0=T.i, u0=T.R*i0-T.E;
  /* the i range: the operating point with room, the short-circuit current if it is near */
  const Isc=(Voc+T.E)/Math.max(Rth,1e-300);
  let imax=Math.max(1.4*Math.abs(i0),Math.abs(Isc)<4*Math.abs(i0)?1.1*Math.abs(Isc):0,1e-6);
  const imin=Math.min(0,1.4*i0);
  const real=e.type==='rbulb';
  const lawU=i=>real?NaN:T.R*i-T.E;
  const us=[Voc-Rth*imin,Voc-Rth*imax,lawU(imin),lawU(imax),0,u0].filter(isFinite);
  let ulo=Math.min(...us), uhi=Math.max(...us); const du=(uhi-ulo)||1; ulo-=0.08*du; uhi+=0.12*du;
  axesR(ctx,IB,imin,imax,ulo,uhi,{title:titleFor(IB,'seen from the '+elTag(C,e)+': the voltage across it, v(a) − v(b), against its current','the '+elTag(C,e)),xlab:'current i, from a to b',ylab:'v(a) − v(b)',xfmt:v=>siFmt(v,'A',2),yfmt:v=>siFmt(v,'V',3)});
  polyline(ctx,IB,[imin,imax],[Voc-Rth*imin,Voc-Rth*imax],imin,imax,ulo,uhi,COL.ref,1.8);
  if(real){ const xs=[], ys=[]; for(let k=0;k<=160;k++){ const u=ulo+(uhi-ulo)*k/160; xs.push(u/realBulbR(u)); ys.push(u); } polyline(ctx,IB,xs,ys,imin,imax,ulo,uhi,COL.pos,1.8); }
  else polyline(ctx,IB,[imin,imax],[lawU(imin),lawU(imax)],imin,imax,ulo,uhi,COL.pos,1.8);
  marker(ctx,IB,imin,imax,ulo,uhi,i0,u0,COL.live);
  lab(ctx,W,H,IB.x+IB.w*(i0-imin)/(imax-imin)+9,IB.y1-IB.h*(u0-ulo)/(uhi-ulo)-12,'i = '+fmtI(i0)+', v = '+fmtV(u0),'#cfd4de','10.5px -apple-system, sans-serif','left','middle');
  legendAuto(ctx,IB,[[COL.ref,'the rest: Vth = '+fmtV(Voc)+', Rth = '+fmtR(Rth)],[COL.pos,real?'the real bulb’s curve':'the part: v = R i'+(T.E!==0?' − E':'')]]);
  if(PB){
    /* the sweep: two decades either side of Rth, stretched to take in this
       part's own resistance (at most eight decades) */
    const lth0=Math.log10(Math.max(Rth,1e-12)), lR0=Math.log10(Math.max(T.R,1e-12));
    let lr0=Math.min(lth0-2,lR0-1), lr1=Math.max(lth0+2,lR0+1);
    if(lr1-lr0>8){ lr0=Math.max(lr0,lth0-2); lr1=lr0+8; }
    const xs=[], ys=[];
    let pmax=0; for(let k=0;k<=200;k++){ const lr=lr0+(lr1-lr0)*k/200, R=Math.pow(10,lr), Pw=Voc*Voc*R/Math.pow(Rth+R,2); xs.push(lr); ys.push(Pw); pmax=Math.max(pmax,Pw); }
    const ymax=pmax*1.18||1;
    const dec=[]; const stp=lr1-lr0>6?2:1; for(let v=Math.ceil(lr0);v<=lr1;v+=stp) dec.push(v);
    axesR(ctx,PB,lr0,lr1,0,ymax,{title:titleFor(PB,'the power it would take, P = Vth²R/(Rth + R)²','P against R'),xlab:'its resistance R (log axis)',ylab:'P',
      xticks:dec,xfmt:v=>siFmt(Math.pow(10,v),'Ω',1),yfmt:v=>siFmt(v,'W',2)});
    polyline(ctx,PB,xs,ys,lr0,lr1,0,ymax,COL.pos,1.8);
    const lth=Math.log10(Rth);
    polyline(ctx,PB,[lth,lth],[0,ymax],lr0,lr1,0,ymax,COL.ref,1.1,[5,4]);
    lab(ctx,W,H,PB.x+PB.w*(lth-lr0)/(lr1-lr0)+5,PB.y+10,'R = Rth','#e8a25a','10.5px -apple-system, sans-serif','left','middle');
    const lR=Math.log10(T.R), Pnow=i0*i0*T.R;
    if(lR>=lr0&&lR<=lr1) marker(ctx,PB,lr0,lr1,0,ymax,lR,Pnow,COL.live);
    else lab(ctx,W,H,PB.x+8,PB.y+26,'this part’s '+fmtR(T.R)+' is off this axis','#8b93a6','10.5px -apple-system, sans-serif','left','middle');
  }
  caption(ctx,V.left,V.capY,V.capTxt,V.capW,'#767e92',CAP_FONT);
}

/* ---------------- one battery at a time ---------------- */
const SUPER_CAP_FULL='Each row is one part (wires left out). Starting from zero, each coloured step is the current that one battery would drive through that part with every other battery’s EMF set to zero and its internal resistance kept; the steps add, with their signs, to exactly the current the whole circuit carries (the white tick). A battery can push a part’s current backwards; that is how two sources fight.';
const SUPER_CAP_SHORT='Each battery’s own contribution to each part’s current, and their sum (white).';
const BAT_COL=[COL.struct,COL.ref,COL.live,'#8b93a6'];
function drawSuper(ctx,W,H,M){
  const SOL=M.sol, C=M.st.circ, Sp=M.sup;
  if(!Sp.bats.length){ sayWhy(ctx,W,H,C.els.length?'There is no battery in the circuit, so nothing drives any current: superposition has nothing to add up.':'There is nothing on the bench. Build a circuit in the lab, or pick one in the panel.'); return; }
  const V=viewFrame(ctx,W,H,SUPER_CAP_FULL,SUPER_CAP_SHORT);
  const nb=Sp.parts.length, parts=chartParts(SOL,C);
  const avail=V.capY-24-V.top-64, minRow=nb*6+10, maxRows=Math.max(2,Math.floor(avail/minRow)), rows=parts.slice(0,maxRows);
  const rowH=Math.min(Math.max(minRow,avail/rows.length),nb*22+34);
  const lw=Math.min(150,Math.max(96,Math.max(...rows.map(e=>plain(elTag(C,e)).length))*5.6+10));
  const B=box(V.left+lw,V.top,V.right-V.left-lw,rowH*rows.length);
  let lo=0, hi=0;
  for(const e of rows){ const k=SOL.onK.get(e.id); let c=0; for(const p of Sp.parts){ c+=p[k]; lo=Math.min(lo,c); hi=Math.max(hi,c); } }
  const span=(hi-lo)||1; lo-=0.06*span; hi+=0.06*span;
  axesR(ctx,B,lo,hi,0,rows.length,{title:titleFor(B,'each part’s current, battery by battery: '+nb+' batter'+(nb===1?'y':'ies'),'current, battery by battery'),xlab:'current i, from a to b through the part',yticks:[],xfmt:v=>siFmt(v,'A',2)});
  const X=v=>B.x+B.w*(v-lo)/(hi-lo);
  if(lo<0&&hi>0) strokePts(ctx,[[X(0),B.y],[X(0),B.y1]],'#8b93a6',1);
  /* a waterfall per row: battery j's step on its own sub-row, starting where
     the previous one ended; the full solution as a white tick across the row */
  const sb=Math.min(16,(rowH-14)/nb);
  rows.forEach((e,r)=>{ const k=SOL.onK.get(e.id), y0=B.y+rowH*r+(rowH-nb*sb)/2;
    lab(ctx,W,H,B.x-8,B.y+rowH*(r+0.5),elTag(C,e),'#aeb6c6','10.5px -apple-system, sans-serif','right','middle');
    let c=0;
    Sp.parts.forEach((p,j)=>{ const c1=c+p[k], xa=X(Math.min(c,c1)), xb=Math.max(X(Math.max(c,c1)),xa+1), ya=y0+j*sb;
      fillPts(ctx,[[xa,ya+0.5],[xb,ya+0.5],[xb,ya+sb-0.5],[xa,ya+sb-0.5]],BAT_COL[Math.min(j,3)]);
      if(j<nb-1) strokePts(ctx,[[X(c1),ya+sb-0.5],[X(c1),ya+sb+0.5]],'#6f7789',1);
      c=c1; });
    const xt=X(SOL.sol.i[k]); strokePts(ctx,[[xt,y0-3],[xt,y0+nb*sb+3]],'#f2f4f8',2.2); });
  /* the key, below the axis where no bar can reach it */
  const items=Sp.bats.slice(0,3).map((kb,j)=>[BAT_COL[j],elTag(C,SOL.net.br[kb].el)+' alone']);
  if(nb>3) items.push([BAT_COL[3],(nb-3)+' more batteries']);
  items.push(['#f2f4f8','the full solution']);
  let lx=B.x; const ly=B.y1+46;
  for(const [col,txt] of items){ fillPts(ctx,[[lx,ly-4],[lx+11,ly-4],[lx+11,ly+4],[lx,ly+4]],col);
    lab(ctx,W,H,lx+16,ly,txt,'#9aa2b4','10.5px -apple-system, sans-serif','left','middle'); lx+=16+plain(txt).length*10.5*0.52+20; }
  if(parts.length>rows.length) lab(ctx,W,H,B.x,ly+18,(parts.length-rows.length)+' more parts not shown','#8b93a6','10.5px -apple-system, sans-serif','left','middle');
  caption(ctx,V.left,V.capY,V.capTxt,V.capW,'#767e92',CAP_FONT);
}

/* ---------------- dispatch and the scene ---------------- */
function drawView(ctx,W,H,M){
  POLY_SEGS=[]; LEGEND_RECTS=[]; LABELS=[];
  ctx.fillStyle=COL.bg; ctx.fillRect(0,0,W,H);
  if(M.view==='lab') drawLab(ctx,W,H,M);
  else if(M.view==='graph') drawGraph(ctx,W,H,M);
  else if(M.view==='power') drawPower(ctx,W,H,M);
  else if(M.view==='thev') drawThev(ctx,W,H,M);
  else drawSuper(ctx,W,H,M);
}
/* the charge animation: every part's charges slide by 25 units per second per
   ampere, times the speed-limit factor; a fixed step per frame keeps the
   headless suites deterministic */
const FRAME_DT=1/60;
function advanceCharges(st,SOL,dt){
  const sc=chargeScale(SOL.Imax);
  for(const e of st.circ.els){ const I=SOL.I.get(e.id); if(!(Math.abs(I)>1e-10)) continue;
    const L=elLength(st.circ,e)||1, p=(st.phase[e.id]||0)+dt*CHARGE_SPEED*I*sc;
    st.phase[e.id]=((p%L)+L)%L; }
  st.clock+=dt;
}
function makeScene(canvas){
  const S={st:ST,W:1400,H:820};
  S.model=()=>buildModel();
  S.draw=()=>{ const ctx=canvas.getContext('2d'); drawView(ctx,S.W,S.H,buildModel()); };
  S.pointer=(kind,x,y)=>ST.view==='lab'?labPointer(S,kind,x,y):false;
  S.wheel=dy=>{ if(ST.view!=='lab') return false;
    const i=Math.max(0,ZOOMS.indexOf(ST.zoom)), j=clamp(i+(dy<0?1:-1),0,ZOOMS.length-1);
    if(ZOOMS[j]===ST.zoom) return false; ST.zoom=ZOOMS[j]; return true; };
  /* the loop paints on its own only while charges are moving in the lab */
  S.animating=()=>{ if(ST.view!=='lab'||!ST.showCurrent) return false; return buildModel().sol.Imax>1e-10; };
  S.step=()=>{ if(!S.animating()) return false; advanceCharges(ST,buildModel().sol,FRAME_DT); return true; };
  return S;
}
