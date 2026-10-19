
/* ================================================================== *
 *  THE COINS view (PhET's Coins screen) — shared by the family        *
 * ================================================================== */
function coinWord(sc,v){ return sc.quantum?(v?'up':'down'):(v?'heads':'tails'); }
function coinGlyph(sc,v){ return sc.quantum?(v?'↑':'↓'):(v?'heads':'tails'); }
function stateWord(s){ return {preparing:'being flipped',ready:'ready, unobserved',hidden:'hidden',revealed:'revealed'}[s]||s; }
/* a snapshot of one scene for the drawing and the readout */
function coinsModel(sc){
  const p=sc.p, N=sc.set.n, sd=binomSD(N,p);
  const m={sc, quantum:sc.quantum, p, q:1-p, N, alpha:Math.sqrt(p), beta:Math.sqrt(1-p),
           init:sc.quantum?quantumInit(p):sc.init, preparing:sc.preparing,
           sState:sc.single.state, setState:sc.set.state, kUp:sc.set.kUp, sd, mean:N*p};
  m.setShown=!sc.preparing&&sc.set.state==='revealed';
  m.z=m.setShown&&sd>0?(sc.set.kUp-N*p)/sd:NaN;
  m.exact=m.setShown&&sd===0;                 /* p = 0 or 1: every coin must agree */
  const h=sc.single; m.nObs=h.nObs; m.nUp=h.nUp; m.frac=h.nObs>0?h.nUp/h.nObs:NaN;
  m.fracSd=h.nObs>0?Math.sqrt(p*(1-p)/h.nObs):NaN;
  return m;
}
/* the stage: the prepared coin, one coin under test, N identical coins, and
   below them the counts.  Returned so the pointer and the tests use the SAME
   boxes the drawing uses. */
function coinsGeo(ctx,W,H,C){
  const narrow=isNarrow(W), top=stageTop()+30, left=narrow?18:56;
  const rightTop=narrow?W-18:W-RO_W-44;
  const fit=capLayout(ctx,W,H,C.full,C.short,left,narrow?W-18:W-26,top+300);
  const avail=fit.capY-16-top;
  /* no floor on the lower row: when it does not fit it is not drawn, rather
     than drawn under the caption and the #hint (found at 560 x 380) */
  const upH=Math.max(150,Math.min(narrow?200:330,avail*0.56));
  const span=rightTop-left, gap=narrow?16:28;
  const wA=narrow?Math.max(150,span*0.26):Math.max(200,Math.min(250,span*0.24));
  const wB=narrow?Math.max(150,span*0.30):Math.max(220,Math.min(300,span*0.30));
  const A=box(left,top,wA,upH), B=box(A.x1+gap,top,wB,upH), Cb=box(B.x1+gap,top,Math.max(120,rightTop-(B.x1+gap)),upH);
  const lowTop=top+upH+44, lowH=fit.capY-16-lowTop-20;
  const hist=box(left+34,lowTop,Math.min(narrow?W-18-left-34:560,(narrow?W-18:W-26)-left-34),lowH);
  /* the strip starts below the floating readout's zone (y < 480 on the right) */
  const sTop=Math.max(lowTop,486);
  const strip=narrow?null:box(hist.x1+60,sTop,Math.min(520,Math.max(0,(W-26)-(hist.x1+60))),lowH-(sTop-lowTop));
  const rS=Math.min(B.w,B.h-40)*0.30;
  const single={cx:B.x+B.w/2, cy:B.y+22+(B.h-40)/2, r:rS};
  return {narrow,top,left,fit,A,B,C:Cb,hist,strip:strip&&strip.w>150?strip:null,single};
}
/* where each of the N coins sits inside the set's box */
function coinGrid(Cb,N){
  const cols=N===10?5:(N===100?10:100), rows=N/cols;
  const inner=box(Cb.x+10,Cb.y+26,Cb.w-20,Cb.h-36);
  const cell=Math.min(inner.w/cols,inner.h/rows);
  const x0=inner.x+(inner.w-cell*cols)/2, y0=inner.y+(inner.h-cell*rows)/2;
  return {cols,rows,cell,x0,y0,box:box(x0,y0,cell*cols,cell*rows)};
}
/* hist: whether the histogram is drawn (the caption names it only then) */
function coinsCaption(M,hist){
  const m=M.C, sc=m.sc, q=sc.quantum, h=hist!==false;
  const what=q?'A quantum “coin” is prepared as |ψ⟩ = α|↑⟩ + β|↓⟩ with |α|² = '+fmt(m.p,2)+'. Until it is observed it has no face at all — drawn here as both arrows, each as bright as its probability — and observing it gives ↑ with probability |α|²: that is the Born rule, and the face appears only then.'
                :'A classical coin always has a face: flipping it hides a definite heads or tails under the cup, with P(heads) = '+fmt(m.p,2)+' set by the bias, and revealing it only shows you what was already there.';
  const set=m.N===10000?' The 10 000 coins are drawn as a 100 × 100 grid of squares, one square per coin.':'';
  return {full:what+(h?' The histogram counts the '+fmtN(m.N)+' identical coins against the binomial’s Np ± √(Np(1−p)) in orange.':'')+set,
          short:(q?'Quantum coin: no face until observed; P(↑) = |α|² = ':'Classical coin: a hidden face; P(heads) = ')+fmt(m.p,2)+'.'+(h?' Orange: Np ± √(Np(1−p)).':'')};
}
/* the caption and the geometry together: the histogram is optional */
function coinsLayout(ctx,W,H,M){ return layoutNamed(h=>coinsCaption(M,h),Cap=>coinsGeo(ctx,W,H,Cap),G=>G.hist.h>=50); }
function drawCoinSet(ctx,Cb,sc,t){
  const c=sc.set, N=c.n, G=coinGrid(Cb,N);
  if(N<=100){
    const r=G.cell*0.40;
    for(let i=0;i<N;i++){
      const cx=G.x0+(i%G.cols+0.5)*G.cell, cy=G.y0+(Math.floor(i/G.cols)+0.5)*G.cell;
      coinFace(ctx,cx,cy,r,coinKind(sc,c,c.vals[i],t,i),coinOpts(sc,c,t,i));
    }
    return G;
  }
  /* 10 000: three batched fills (+, -, and the undecided/hidden colour) */
  const s=G.cell, pad=s>3?0.6:0.25, paths={pos:[],neg:[],other:[]};
  for(let i=0;i<N;i++){
    const x=G.x0+(i%G.cols)*s, y=G.y0+Math.floor(i/G.cols)*s;
    let k='other';
    if(c.state==='revealed') k=c.vals[i]?'pos':'neg';
    else if(c.state==='preparing'&&!sc.quantum) k=((i*7+Math.floor(t*14))%3===0)?'pos':(((i*5+Math.floor(t*11))%3===0)?'neg':'other');
    paths[k].push(x,y);
  }
  const other=c.state==='ready'?shade(mix(COL.neg,COL.pos,sc.p),0.55):(c.state==='hidden'?'#39404f':'#2b3140');
  for(const [k,col] of [['pos',COL.pos],['neg',COL.neg],['other',other]]){
    const a=paths[k]; if(!a.length) continue;
    ctx.beginPath(); for(let j=0;j<a.length;j+=2) ctx.rect(a[j],a[j+1],s-pad,s-pad);
    ctx.fillStyle=k==='other'?other:shade(col,0.85); ctx.fill();
  }
  return G;
}
function coinKind(sc,c,v,t,i){
  if(c.state==='hidden') return 'hidden';
  if(c.state==='ready') return 'S';
  if(c.state==='preparing'){ if(sc.quantum) return 'S'; const ph=Math.cos(TAU*3*t+(i||0)*0.37); return ph>=0?'H':'T'; }
  return sc.quantum?(v?'U':'D'):(v?'H':'T');
}
function coinOpts(sc,c,t,i){
  const o={p:sc.p};
  if(c.state==='preparing') o.sx=sc.quantum?0.25+0.75*Math.min(1,t/FLIP_T):Math.cos(TAU*3*t+(i||0)*0.37);
  return o;
}
function drawCoins(ctx,W,H,M){
  const m=M.C, sc=m.sc, q=sc.quantum, LY=coinsLayout(ctx,W,H,M), Cap=LY.Cap, G=LY.G;
  const A=G.A, B=G.B, Cb=G.C, t=M.tNow||0;
  /* titles sit above their boxes, like the plot titles (they sat on the frame) */
  const title=(b,txt)=>{ lab(ctx,W,H,b.x,b.y-10,txt,COL.text,'italic 13px Georgia, serif','left','middle'); };
  /* A: the prepared coin */
  frame(ctx,A,COL.edge);
  title(A,sc.preparing?(q?'the “coin” to prepare':'the coin to prepare'):(q?'the prepared state':'the coin'));
  const rA=Math.max(20,Math.min(A.w*0.24,58,A.h*0.17)), cxA=A.x+A.w/2, cyA=A.y+18+rA;
  coinFace(ctx,cxA,cyA,rA,q?(m.p>=1?'U':(m.p<=0?'D':'S')):(sc.init==='heads'?'H':'T'),{p:m.p});
  let yy=cyA+rA+22;
  if(q){ rich(ctx,cxA,yy,[['|ψ⟩ = '+fmt(m.alpha,3)+'|↑⟩ + '+fmt(m.beta,3)+'|↓⟩',null]],13.5,'#e9e9f0','center',true); yy+=22;
         lab(ctx,W,H,cxA,yy,'P(↑) = |α|² = '+fmt(m.p,2),COL.pos,SM_FONT,'center','middle'); yy+=16;
         lab(ctx,W,H,cxA,yy,'P(↓) = |β|² = '+fmt(m.q,2),COL.neg,SM_FONT,'center','middle'); yy+=16;
         lab(ctx,W,H,cxA,yy,m.init==='superposition'?'a superposition':('the basis state '+(m.init==='up'?'↑':'↓')),COL.dim,SM_FONT,'center','middle'); }
  else { lab(ctx,W,H,cxA,yy,'starts '+sc.init+' up',COL.text,LAB_FONT,'center','middle'); yy+=18;
         lab(ctx,W,H,cxA,yy,'P(heads) = '+fmt(m.p,2),COL.pos,SM_FONT,'center','middle'); yy+=16;
         lab(ctx,W,H,cxA,yy,'P(tails) = '+fmt(m.q,2),COL.neg,SM_FONT,'center','middle'); }
  if(!sc.preparing&&yy+22<A.y1-12) lab(ctx,W,H,cxA,A.y1-12,'sent to be measured',COL.faint,SM_FONT,'center','middle');
  /* B: one coin under test */
  const idle=sc.preparing;
  ctx.setLineDash(idle?[5,4]:[]); frame(ctx,B,idle?COL.faint:COL.struct); ctx.setLineDash([]);
  title(B,'one coin');
  if(idle) lab(ctx,W,H,B.x+B.w/2,B.y+B.h/2,'empty: send the coin to be measured',COL.dim,SM_FONT,'center','middle');
  else {
    const c=sc.single;
    coinFace(ctx,G.single.cx,G.single.cy,G.single.r,coinKind(sc,c,c.vals[0],c.t),coinOpts(sc,c,c.t));
    const st=c.state==='revealed'?coinWord(sc,c.vals[0]):stateWord(c.state);
    lab(ctx,W,H,B.x+B.w/2,B.y1-12,st,c.state==='revealed'?(c.vals[0]?COL.pos:COL.neg):COL.dim,LAB_FONT,'center','middle');
  }
  /* C: N identical coins */
  ctx.setLineDash(idle?[5,4]:[]); frame(ctx,Cb,idle?COL.faint:COL.struct); ctx.setLineDash([]);
  title(Cb,'N = '+fmtN(m.N)+' identical coins');
  if(idle) lab(ctx,W,H,Cb.x+Cb.w/2,Cb.y+Cb.h/2,'empty',COL.dim,SM_FONT,'center','middle');
  else drawCoinSet(ctx,Cb,sc,sc.set.t);
  /* the counts of the set against the binomial */
  const hb=G.hist, N=m.N;
  if(!G.panelOff&&hb.h>=50){
    axesT(ctx,hb,0,2,0,N,{xticks:[],yticks:ticksFor(0,N,hb.h<110?2:4),yfmt:v=>fmtN(Math.round(v)),title:fitTitle(hb,'the '+fmtN(m.N)+' coins: counted, against Np ± √(Np(1−p))','counts against the binomial')});
    if(m.setShown){
      const k1=sc.set.kUp, k2=N-k1, bw=Math.min(60,hb.w*0.18);
      const x1=px(hb,0.6,0,2), x2=px(hb,1.4,0,2);
      ctx.fillStyle=COL.pos; ctx.fillRect(x1-bw/2,py(hb,k1,0,N),bw,hb.y1-py(hb,k1,0,N));
      ctx.fillStyle=COL.neg; ctx.fillRect(x2-bw/2,py(hb,k2,0,N),bw,hb.y1-py(hb,k2,0,N));
      /* the law: Np and N(1-p), each with +-1 sd */
      for(const [xc,mu] of [[x1,m.mean],[x2,N-m.mean]]){
        const Y=py(hb,mu,0,N), Ya=py(hb,Math.min(N,mu+m.sd),0,N), Yb=py(hb,Math.max(0,mu-m.sd),0,N);
        ctx.beginPath(); ctx.moveTo(xc-bw/2-8,Y); ctx.lineTo(xc+bw/2+8,Y); ctx.strokeStyle=COL.ref; ctx.lineWidth=2.2; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(xc+bw/2+4,Ya); ctx.lineTo(xc+bw/2+4,Yb); ctx.moveTo(xc+bw/2+1,Ya); ctx.lineTo(xc+bw/2+7,Ya); ctx.moveTo(xc+bw/2+1,Yb); ctx.lineTo(xc+bw/2+7,Yb);
        ctx.strokeStyle=COL.ref; ctx.lineWidth=1.2; ctx.stroke();
      }
      barVal(ctx,W,H,x1,py(hb,k1,0,N),hb,fmtN(k1),COL.pos,py(hb,m.mean,0,N));
      barVal(ctx,W,H,x2,py(hb,k2,0,N),hb,fmtN(k2),COL.neg,py(hb,N-m.mean,0,N));
    } else lab(ctx,W,H,hb.x+hb.w/2,hb.y+hb.h/2,sc.preparing?'nothing measured yet':(sc.set.state==='preparing'?'being '+(q?'reprepared':'flipped'):(sc.set.state==='ready'?'not observed yet: no faces to count':'hidden: reveal to count')),COL.dim,SM_FONT,'center','middle');
    ctx.font='italic 12px Georgia, serif'; ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.fillStyle=COL.pos; ctx.fillText(q?'↑':'heads',px(hb,0.6,0,2),hb.y1+4); ctx.fillStyle=COL.neg; ctx.fillText(q?'↓':'tails',px(hb,1.4,0,2),hb.y1+4);
  }
  /* the single coin's record: its last outcomes and its running fraction */
  const sb=G.strip;
  if(sb&&sb.h>=50){
    const hs=sc.single.hist, n=hs.length;
    axesT(ctx,sb,0,HIST_KEEP,-1.3,1.3,{xticks:[],yticks:[],title:fitTitle(sb,'one coin, its last '+HIST_KEEP+' outcomes','its last outcomes')});
    const mid=py(sb,0,-1.3,1.3), cw=sb.w/HIST_KEEP;
    ctx.beginPath(); ctx.moveTo(sb.x,mid); ctx.lineTo(sb.x1,mid); ctx.strokeStyle=COL.faint; ctx.lineWidth=1; ctx.stroke();
    for(let i=0;i<n;i++){ const x=sb.x+i*cw+1, v=hs[i], hh=sb.h*0.34;
      ctx.fillStyle=v?COL.pos:COL.neg; if(v) ctx.fillRect(x,mid-hh,Math.max(1,cw-2),hh); else ctx.fillRect(x,mid+1,Math.max(1,cw-2),hh); }
    if(!n) lab(ctx,W,H,sb.x+sb.w/2,sb.y+14,'none yet: '+(q?'observe':'reveal')+' the coin',COL.dim,SM_FONT,'center','middle');
    else lab(ctx,W,H,sb.x+4,sb.y1+12,m.nUp+' '+(q?'up':'heads')+' of '+m.nObs+' = '+fmt(m.frac,3)+'  (p = '+fmt(m.p,2)+' ± '+fmt(m.fracSd,3)+')',COL.text,SM_FONT,'left','middle');
  }
  drawCap(ctx,G.left,G.fit);
  return G;
}
/* ---- readout, equation bar, tag ---- */
function coinsReadout(M){
  const m=M.C, sc=m.sc, q=sc.quantum, c1=sc.single, cs=sc.set;
  let s=hd(q?'the prepared state':'the prepared coin');
  if(q) s+=rrow('|&psi;&rang; = &alpha;|&uarr;&rang; + &beta;|&darr;&rang;',fmt(m.alpha,3)+', '+fmt(m.beta,3))
          +rrow('P(&uarr;) = |&alpha;|&sup2;',fmt(m.p,2),'good')+rrow('P(&darr;) = |&beta;|&sup2;',fmt(m.q,2))
          +rrow('|&alpha;|&sup2; + |&beta;|&sup2;',fmt(m.alpha*m.alpha+m.beta*m.beta,12))+rrow('state',m.init);
  else s+=rrow('starts',sc.init+' up')+rrow('P(heads), the bias',fmt(m.p,2),'good')+rrow('P(tails)',fmt(m.q,2));
  s+=hd('one coin')+rrow('state',sc.preparing?'&mdash; (preparing)':stateWord(c1.state));
  if(!sc.preparing&&c1.state==='revealed') s+=rrow('face',coinWord(sc,c1.vals[0]),c1.vals[0]?'good':'');
  s+=rrow((q?'observed':'revealed')+', '+(q?'up':'heads'),m.nObs+', '+m.nUp)
    +rrow('fraction &plusmn; &radic;(p(1&minus;p)/n)',m.nObs?fmt(m.frac,3)+' &plusmn; '+fmt(m.fracSd,3):'&mdash;');
  s+=hd('N identical coins')+rrow('N',String(cs.n))+rrow('state',sc.preparing?'&mdash; (preparing)':stateWord(cs.state));
  s+=rrow('expected Np &plusmn; &radic;(Np(1&minus;p))',fmt(m.mean,m.N>=1000?0:1)+' &plusmn; '+sigf(m.sd,3));
  if(m.setShown) s+=rrow((q?'up':'heads')+', '+(q?'down':'tails'),cs.kUp+', '+(cs.n-cs.kUp),'good')
    +rrow('z = (k &minus; Np)/&sigma;',m.exact?'exact':fmt(m.z,2),Math.abs(m.z)>3?'bad':'');
  return s;
}
function coinsEq(M){
  const q=M.C.quantum;
  if(q) return ['<span class="hl">|&psi;&rang; = &alpha;|&uarr;&rang; + &beta;|&darr;&rang;</span>, &nbsp; P(&uarr;) = |&alpha;|&sup2;, &nbsp; P(&darr;) = |&beta;|&sup2;, &nbsp; |&alpha;|&sup2; + |&beta;|&sup2; = 1 &nbsp;&middot;&nbsp; P(k of N) = C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup>',
                'the Born rule: the amplitudes become odds only when the coin is observed, and N identical coins then count like a binomial'];
  return ['<span class="hl">P(heads) = p, &nbsp; P(tails) = 1 &minus; p</span> &nbsp;&middot;&nbsp; P(k of N) = C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup>, &nbsp; k = Np &plusmn; &radic;(Np(1&minus;p))',
          'a classical coin has a face before you look: flipping hides it, revealing shows it, and N coins count like a binomial'];
}
function coinsTag(M){ const m=M.C; return '<b>the coins</b> — '+(m.quantum?'a quantum “coin”':'a classical coin')+', P('+(m.quantum?'&uarr;':'heads')+') = '+fmt(m.p,2)+', N = '+m.N+(m.preparing?' · preparing':''); }
const INFO_COINS='PhET&rsquo;s Coins screen sets a classical coin beside a quantum &ldquo;coin&rdquo;. The classical coin always has a face. '
  +'Flipping it takes a second and leaves a definite heads or tails under the cup, with the probability of heads set by the bias; revealing it only '
  +'shows you what was already there, and hiding it again changes nothing. The quantum coin is prepared in a state &alpha;|&uarr;&rang; + &beta;|&darr;&rang;. '
  +'Until it is observed it has no face at all &mdash; the picture draws both arrows, each as bright as its probability &mdash; and observing it gives '
  +'&uarr; with probability |&alpha;|&sup2;, the Born rule. After that it is up (or down), and hiding and revealing it shows the same face every time: '
  +'only a repreparation brings the superposition back. Ten, a hundred or ten thousand identical coins then count like a binomial, '
  +'Np &plusmn; &radic;(Np(1&minus;p)), which is why ten thousand of them look almost deterministic and ten look like noise. Set a bias, press '
  +'&ldquo;send to measure&rdquo;, then flip, reveal and observe; click a coin on the canvas to reveal or hide it.';
function FR(t,b){ return '<span class="frac"><span class="t">'+t+'</span><span class="b">'+b+'</span></span>'; }
function EQ(n,body){ return '<div class="eq"><span class="n">['+n+']</span>'+body+'</div>'; }
const DERIV_COINS='<h4>two coins</h4>'
  +EQ(1,'<span class="rm">classical:</span> P(heads) = p, &nbsp; P(tails) = 1 &minus; p &nbsp; <span class="rm">(a face exists, hidden or not)</span>')
  +EQ(2,'<span class="rm">quantum:</span> |&psi;&rang; = &alpha;|&uarr;&rang; + &beta;|&darr;&rang;, &nbsp; &alpha; = &radic;p, &beta; = &radic;(1&minus;p)')
  +EQ(3,'P(&uarr;) = |&lang;&uarr;|&psi;&rang;|&sup2; = |&alpha;|&sup2;, &nbsp; <span class="rm">then</span> |&psi;&rang; &rarr; |&uarr;&rang;')
  +EQ(4,'P(k of N) = C(N,k) p<sup>k</sup>(1&minus;p)<sup>N&minus;k</sup>, &nbsp; &lang;k&rang; = Np, &nbsp; &sigma;<sub>k</sub> = &radic;(Np(1&minus;p))')
  +'<p>Both coins give the same odds when they are looked at face-on: nothing measured along the up&ndash;down axis can tell a hidden '
  +'classical face from a superposition. PhET&rsquo;s seeded sets draw u &lt; p for heads (or up) one coin at a time; this remake does '
  +'the same from one mulberry32 stream.</p>'
  +'<div class="cite">pins: the stream against derive.py bit for bit; one coin flipped 10 000 times (3011 heads at p = 0.3, 4&sigma; = 183); '
  +'10 000 coins (3490 at p = 0.35); 2000 sets of 100 against the binomial, &chi;&sup2; = 20.36 on 28 dof (scipy&rsquo;s 99.9 % point 56.9)</div>';
