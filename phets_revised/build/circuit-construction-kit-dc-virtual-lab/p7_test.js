/* ================================================================== *
 *  selfTest -- headless verification.  Reference values labelled      *
 *  (python) come from REF, emitted by build/circuit-construction-kit- *
 *  dc-virtual-lab/derive.py from EXACT rational solves by nodal       *
 *  analysis (a different formulation from this file's), printed in    *
 *  refvals.txt and read in full.                                      *
 * ================================================================== */
function makeShot(W,H){
  const ops=[]; let Mx=[1,0,0,1,0,0]; const stack=[];
  const st2={font:'10px x',align:'left',base:'alphabetic'};
  const mul=(A,B)=>[A[0]*B[0]+A[2]*B[1],A[1]*B[0]+A[3]*B[1],A[0]*B[2]+A[2]*B[3],A[1]*B[2]+A[3]*B[3],
                    A[0]*B[4]+A[2]*B[5]+A[4],A[1]*B[4]+A[3]*B[5]+A[5]];
  const app=(x,y)=>[Mx[0]*x+Mx[2]*y+Mx[4],Mx[1]*x+Mx[3]*y+Mx[5]];
  const fsz=()=>{ const m=/([\d.]+)px/.exec(st2.font); return m?parseFloat(m[1]):10; };
  let pend=null;
  const ctx={ops,
    save(){ stack.push({M:Mx.slice(),f:st2.font,a:st2.align,b:st2.base}); },
    restore(){ const s=stack.pop(); if(s){ Mx=s.M; st2.font=s.f; st2.align=s.a; st2.base=s.b; } },
    translate(x,y){ Mx=mul(Mx,[1,0,0,1,x,y]); },
    rotate(r){ const c=Math.cos(r),s3=Math.sin(r); Mx=mul(Mx,[c,s3,-s3,c,0,0]); },
    scale(x,y){ Mx=mul(Mx,[x,0,0,y,0,0]); }, setTransform(){ Mx=[1,0,0,1,0,0]; },
    beginPath(){ pend={n:0,pts:[]}; }, moveTo(x,y){ if(pend) pend.pts.push(app(x,y)); }, lineTo(x,y){ if(pend){ pend.n++; pend.pts.push(app(x,y)); } }, closePath(){},
    rect(x,y,w,hh){ if(pend){ pend.n++; pend.pts.push(app(x,y),app(x+w,y+hh)); } }, arc(x,y){ if(pend){ pend.n++; pend.pts.push(app(x,y)); } },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle,pts:pend.pts}); },
    stroke(){ ops.push({op:'stroke',style:ctx.strokeStyle,pts:pend?pend.pts:[]}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle,pts:[app(x,y),app(x+w,y+hh)]}); },
    strokeRect(){ ops.push({op:'stroke',pts:[]}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,rot:Math.abs(Mx[1])>1e-9,style:ctx.fillStyle,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000', _stroke='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  Object.defineProperty(ctx,'strokeStyle',{get:()=>_stroke,set:v=>_stroke=''+v});
  for(const kk of ['lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}
function brightnessCss(css){ const c=toRgb(css); return Math.max(c[0],c[1],c[2]); }
function netOf(R){ return R.br.map(b=>({a:b[0],b:b[1],R:b[2],E:b[3],kind:b[4]})); }

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const EPS=Number.EPSILON;
  const T0=Date.now();
  const stSave=clone(ST);
  function withState(over,fn){ resetState(over); try{ return fn(); } finally{ resetState(stSave); } }
  const G0={rho:RHO_MIN,rbat:BATT_R_MIN};

  /* ---------- 0. the shared-helper fixes cannot rot ---------- */
  ok(plain('&Delta;x &theta; &#955;')==='Δx θ λ','plain() decodes named, capital and numeric entities');
  ok(plain('a<sub>B</sub>b')==='aBb','plain() strips tags');
  ok(plain('10 &Omega;')==='10 Ω','plain() knows the ohm sign');
  ok(ticksFor(0.8,0.2,5).length===1&&ticksFor(0.2,0.8,5).length>=3,'axes() range-sort is what rescues an inverted axis');
  { let threw=false; try{ toRgb('nope'); }catch(e){ threw=true; } ok(threw,'toRgb throws on garbage'); }
  ok(brightnessCss(shade(mix(COL.struct,COL.pos,0.5),0.9))>60,'mix() output is a legal mix() input (a two-stage blend is not black)');
  { const stub={beginPath(){},moveTo(){},lineTo(){},stroke(){},save(){},restore(){},setLineDash(){}};
    const bb=box(100,100,200,100); POLY_SEGS=[];
    polyline(stub,bb,[-1,2],[0.5,0.5],0,1,0,1,'#fff',1);
    ok(POLY_SEGS.length===4&&Math.abs(POLY_SEGS[0]-bb.x)<1e-9&&Math.abs(POLY_SEGS[2]-bb.x1)<1e-9,'polyline clips a both-ends-outside segment to the frame edges');
    POLY_SEGS=[]; }
  ok(logTicks(0,10).length===0,'logTicks refuses a non-positive bound instead of looping');

  /* the formats the readout and the canvas share */
  eq(fmtI(REF.presets.bulb.i['4']),'900 mA','0.89999 A reads 900 mA'); eq(fmtR(REF.thev.bulb_4.Rth),'100 µΩ','1.0007e-4 ohm reads 100 µΩ');
  eq(fmtV(-3.5999927975088135),'−3.60 V','negative voltages carry a true minus sign'); eq(fmtP(REF.thev.bulb_4.Pmax),'202 kW','2.0235e5 W reads 202 kW');
  eq(fmtV(1),'1.00 V','exactly 1 V stays in volts (the prefix boundary)'); eq(fmtI(1e-3),'1.00 mA','exactly 1 mA in milliamps'); eq(fmtR(Infinity),'∞','an open part is infinite');
  eq(pow10(-16),'10⁻¹⁶','powers of ten are set as superscripts'); eq(fmtRes(0),'0 (exact)','an exact zero residual says so'); eq(fmtRes(3.4e-16),'3.4×10⁻¹⁶','a residual shows its power of ten');
  /* the resistor colour code PhET paints: two significant figures and a multiplier */
  const BN=n=>BAND[n];
  ok(JSON.stringify(colourBands(10))===JSON.stringify([BN(1),BN(0),BN(0)]),'10 ohm: brown black black');
  ok(JSON.stringify(colourBands(20))===JSON.stringify([BN(2),BN(0),BN(0)]),'20 ohm: red black black');
  ok(JSON.stringify(colourBands(4.7))===JSON.stringify([BN(4),BN(7),'#c9a34e']),'4.7 ohm: yellow violet gold');
  ok(JSON.stringify(colourBands(1000))===JSON.stringify([BN(1),BN(0),BN(2)]),'1000 ohm: brown black red');
  ok(JSON.stringify(colourBands(99.6))===JSON.stringify([BN(1),BN(0),BN(1)]),'99.6 ohm rounds up to 100: brown black brown');
  eq(valueText(makeEl(0,'fuse',0,1),null),'15.0 mΩ ≤ 4.0 A','a 4-A fuse is labelled as PhET labels it');

  /* ---------- 1. PhET's small laws, against python ---------- */
  eq(RHO_MIN,REF.consts.RHO_MIN,'resistivity floor 1e-10 ohm m (PhET)'); eq(RHO_MAX,REF.consts.RHO_MAX,'resistivity ceiling 0.0168 ohm m (PhET)');
  eq(MIN_R,REF.consts.MIN_R,'a zero resistance becomes 1.1e-10 ohm (PhET)'); eq(BATT_R_MIN,REF.consts.BATT_R_MIN,'battery resistance floor 1e-4 ohm (PhET)');
  for(const k in REF.consts.wireR){ const [d,r]=k.split('_'); rel(wireR(+d,r==='min'?RHO_MIN:RHO_MAX),REF.consts.wireR[k],1e-14,'wire of '+d+' units at rho '+r+' (python)'); }
  rel(wireR(100,RHO_MAX),1.68,1e-14,'100 units of wire at the top of the slider is 1.68 ohm: 0.0168 x 0.05 m / 5e-4 m^2');
  eq(wireR(0,RHO_MAX),MIN_WIRE_R,'a zero-length wire is held at 1e-14 ohm (PhET)');
  for(const k in REF.consts.fuseR) rel(fuseR(+k),REF.consts.fuseR[k],1e-15,'fuse rated '+k+' A is 0.06/rating ohm (python)');
  for(const k in REF.consts.bright) close(brightnessOf(+k),REF.consts.bright[k],1e-15,'brightness at '+k+' W, PhET\'s rule (python)');
  ok(brightnessOf(1999)<1&&brightnessOf(2000)===1&&brightnessOf(1e6)===1,'brightness reaches 1 exactly at 2 kW and clamps above it');
  for(const k in REF.consts.realR) rel(realBulbR(+k),REF.consts.realR[k],1e-14,'real bulb at '+k+' V (python)');
  rel(realBulbR(-9),realBulbR(9),1e-15,'the real bulb depends on |V|');
  for(const k in REF.consts.charges){ const got=chargeLayout(+k), want=REF.consts.charges[k];
    ok(got.length===want.length&&got.every((x,j)=>Math.abs(x-want[j])<1e-9),'charge layout on '+k+' units (PhET\'s rule, python) ['+got.map(x=>fmt(x,2))+']'); }
  rel(REF.consts.Icap,14.448,1e-12,'the speed limit binds above 14.448 A (python)');
  eq(chargeScale(REF.consts.Icap*0.999),1,'below the limit the charges run at full speed');
  rel(chargeScale(2*REF.consts.Icap),0.5,1e-12,'at twice the limiting current they run at half speed');
  rel(chargeScale(10*REF.consts.Icap),0.1,1e-12,'and at ten times, a tenth');

  /* the scale of each connected piece of a solution: its largest current and
     its largest voltage (node, EMF or drop) -- the ruler rounding is made on */
  function scales(N,br,v,i){
    const comp=componentsOf(N,br), Isc=new Map(), Vsc=new Map();
    const up=(m,c,x)=>{ if(!(m.get(c)>=x)) m.set(c,x); };
    br.forEach((e,k)=>{ up(Isc,comp[e.a],Math.abs(i[k])); up(Vsc,comp[e.a],Math.max(Math.abs(e.E),Math.abs(e.R*i[k]))); });
    for(let q=0;q<N;q++){ up(Vsc,comp[q],Math.abs(v[q])); if(!Isc.has(comp[q])) Isc.set(comp[q],0); }
    return {comp,Isc,Vsc};
  }
  /* a solution against the exact one, each number measured against its
     piece's scale; returns the worst current and voltage errors */
  function vsExact(N,br,s,Rv,Ri){
    const sc=scales(N,br,Rv,Ri); let wi=0, wv=0;
    br.forEach((e,k)=>{ const m=sc.Isc.get(sc.comp[e.a]); wi=Math.max(wi,m>0?Math.abs(s.i[k]-Ri[k])/m:Math.abs(s.i[k])); });
    for(let q=0;q<N;q++){ const m=sc.Vsc.get(sc.comp[q]); wv=Math.max(wv,m>0?Math.abs(s.v[q]-Rv[q])/m:Math.abs(s.v[q])); }
    return {wi,wv};
  }
  const TOL_I=16*EPS, TOL_V=64*EPS, TOL_LAW=8*EPS;

  /* ---------- 2. the solver against exact rational solves (python) ---------- */
  for(const name in REF.nets){
    const R=REF.nets[name], br=netOf(R), s=mnaSolve(R.N,br), law=kirchhoff(R.N,br,s,cycleBasis(R.N,br)), e=vsExact(R.N,br,s,R.v,R.i);
    ok(e.wi<=TOL_I,name+': every branch current matches the exact solve to 16 eps of its piece (python) ['+e.wi.toExponential(2)+']');
    ok(e.wv<=TOL_V,name+': every node voltage matches to 64 eps of its piece (python) ['+e.wv.toExponential(2)+']');
    ok(law.kcl<=TOL_LAW,name+': the current law closes at every node to 8 eps ['+law.kcl.toExponential(2)+']');
    ok(law.kvl<=TOL_LAW,name+': the voltage law closes round every loop to 8 eps ['+law.kvl.toExponential(2)+']');
    eq(cycleBasis(R.N,br).loops.length,br.length-R.N+new Set(componentsOf(R.N,br)).size,name+': B - N + C fundamental loops');
  }
  { const R=REF.nets.series3, s=mnaSolve(R.N,netOf(R)); rel(s.i[0],12/60.5,2*EPS,'series: I = E/(r + R1 + R2 + R3) = 12/60.5 (closed form)');
    rel(s.v[1]-s.v[0],12-0.5*12/60.5,4*EPS,'series: terminal voltage E - I r'); }
  { const R=REF.nets.parallel3, s=mnaSolve(R.N,netOf(R)), Rp=1/(1/10+1/20+1/40), It=9/(1e-4+2e-8+Rp);
    rel(s.i[0],It,4*EPS,'parallel: I = E/(r + wires + R1||R2||R3), R|| = 40/7 (closed form)');
    rel(s.i[2]/s.i[3],2,4*EPS,'parallel: 10 ohm carries twice what 20 ohm does'); rel(s.i[3]/s.i[4],2,4*EPS,'and 20 ohm twice what 40 ohm does'); }
  { const R=REF.nets.bridge_bal, s=mnaSolve(R.N,netOf(R));
    ok(Math.abs(s.i[5])<=4*EPS*Math.abs(s.i[0]),'balanced Wheatstone bridge (R1/R2 = R3/R4): no current in the galvanometer, exactly zero in python ['+s.i[5].toExponential(2)+' A]');
    close(s.v[1],s.v[2],4*EPS*10,'and its two midpoints sit at one potential'); }
  { const R=REF.nets.bridge_unbal, br=netOf(R), s=mnaSolve(R.N,br);
    rel(s.i[5],REF.misc.bridgeUnbal.I5,8*EPS,'unbalanced bridge: galvanometer current (python)');
    const rest=br.slice(0,5), T1=mnaSolve(R.N,rest), T2=mnaSolve(R.N,rest,{inj:[[1,1],[2,-1]],zeroE:true});
    /* V_th is a difference of two ~6.5-V node voltages: its error is absolute, on the 10-V scale */
    close(T1.v[1]-T1.v[2],REF.misc.bridgeUnbal.Voc,16*EPS*10,'its Thevenin voltage at the galvanometer, to 16 eps of 10 V (python)');
    rel(T2.v[1]-T2.v[2],REF.misc.bridgeUnbal.Rth,16*EPS,'its Thevenin resistance (python)');
    rel(s.i[5],(T1.v[1]-T1.v[2])/((T2.v[1]-T2.v[2])+50),64*EPS,'I_g = V_th/(R_th + R_g), to the rounding V_th carries');
    const brI=br.map((e,k)=>k===0?{a:e.a,b:e.b,R:1e-30,E:e.E,kind:'B'}:e), sI=mnaSolve(R.N,brI);
    rel(sI.i[5],REF.misc.bridgeIdealIg,1e-13,'with an ideal source it is the textbook E(R2/(R1+R2) - R4/(R3+R4))/(R1||R2 + R3||R4 + R5) (python)'); }
  { const R=REF.nets.floating, s=mnaSolve(R.N,netOf(R));
    eq(Math.abs(s.i[3]),0,'a dangling resistor carries no current'); close(s.v[3],s.v[2],0,'and its free end sits at its joint\'s voltage');
    ok(s.i[4]===0&&s.i[5]===0&&s.i[6]===0,'a loop with no battery carries nothing'); ok(s.v[4]===0&&s.v[5]===0&&s.v[6]===0,'and sits at its own 0 V');
    eq(s.i[7],0,'a lone battery drives no current'); rel(s.v[8]-s.v[7],6,EPS,'and shows its full EMF across its terminals');
    ok([...s.v,...s.i].every(isFinite),'floating pieces solve without a NaN'); }
  { const R=REF.nets.short, s=mnaSolve(R.N,netOf(R)); rel(s.i[0],9/(1e-4+3.02e-8),4*EPS,'a dead short: I = E/(r + R_wire), 90 kA, finite'); }
  { const R=REF.nets.zeroloop, s=mnaSolve(R.N,netOf(R)); rel(s.i[2],s.i[3],4*EPS,'two zero-ohm parts side by side (1.1e-10 each) split the current evenly'); }
  { const R=REF.nets.twobat, br=netOf(R), s=mnaSolve(R.N,br), P=REF.misc.twobatParts;
    const p0=mnaSolve(R.N,br,{only:0}).i, p1=mnaSolve(R.N,br,{only:4}).i;
    let w=0; for(let k=0;k<br.length;k++){ w=Math.max(w,Math.abs(p0[k]-P[0][k]),Math.abs(p1[k]-P[1][k]),Math.abs(p0[k]+p1[k]-s.i[k])); }
    ok(w<=TOL_I*0.25,'superposition, two batteries: each alone matches python, and the two sum to the full solution ['+w.toExponential(2)+' A]');
    const T=REF.misc.twobatThev, rest=br.slice(0,2).concat(br.slice(3));
    const T1=mnaSolve(R.N,rest), T2=mnaSolve(R.N,rest,{inj:[[2,1],[0,-1]],zeroE:true});
    rel(T1.v[2]-T1.v[0],T.Voc,8*EPS,'Thevenin voltage seen by R3 (python)'); rel(T2.v[2]-T2.v[0],T.Rth,8*EPS,'Thevenin resistance seen by R3 (python)');
    T.loads.forEach((RL,j)=>{ const b2=br.map((e,k)=>k===2?{a:e.a,b:e.b,R:RL,E:0,kind:'R'}:e), s2=mnaSolve(R.N,b2);
      rel(s2.i[2],T.I[j],8*EPS,'R3 = '+fmt(RL,3)+' ohm: I (python)'); rel(s2.i[2],T.Voc/(T.Rth+RL),8*EPS,'and I = V_th/(R_th + R3)'); });
    const Pm=Math.max(...T.P); rel(T.P[T.loads.length-1],Pm,1e-15,'the power is largest at R3 = R_th (python)'); }
  for(const [r,RL,I,Vt] of REF.misc.internal){
    const s=mnaSolve(2,[{a:0,b:1,R:r,E:9,kind:'B'},{a:1,b:0,R:RL,E:0,kind:'R'}]);
    rel(s.i[0],I,4*EPS,'battery r = '+r+', load '+RL+': I = E/(r + R_L) (python)'); rel(s.v[1]-s.v[0],Vt,4*EPS,'and the terminal voltage E - I r (python)'); }
  { /* maximum power transfer: the load that takes most from a 9-V, 5-ohm battery is 5 ohm */
    const Pof=RL=>{ const s=mnaSolve(2,[{a:0,b:1,R:5,E:9,kind:'B'},{a:1,b:0,R:RL,E:0,kind:'R'}]); return s.i[1]*s.i[1]*RL; };
    let lo=-2, hi=4; for(let it=0;it<90;it++){ const m1=lo+(hi-lo)/3, m2=hi-(hi-lo)/3; if(Pof(Math.pow(10,m1))<Pof(Math.pow(10,m2))) lo=m1; else hi=m2; }
    rel(Math.pow(10,(lo+hi)/2),5,1e-6,'maximum power transfer: the best load equals the internal resistance (golden section on the solver)');
    rel(Pof(5),81/20,4*EPS,'and takes E^2/4r = 4.05 W'); }

  /* ---------- 3. the presets, the circuits the UI builds, against python ---------- */
  function presetCheck(key,Rp,tag,setup){
    const C=presetCircuit(key); const glob={rho:RHO_MIN,rbat:BATT_R_MIN}; if(setup) setup(C,glob);
    const SOL=solveCircuit(C,glob), N=SOL.net.N, br=SOL.net.br;
    const Rv=C.verts.map((v,q)=>Rp.v[q]), Ri=br.map(e=>Rp.i[String(e.el.id)]);
    const e=vsExact(N,br,SOL.sol,Rv,Ri);
    ok(e.wi<=TOL_I,tag+': every current matches the exact nodal solve (python) ['+e.wi.toExponential(2)+']');
    ok(e.wv<=TOL_V,tag+': every node voltage matches (python) ['+e.wv.toExponential(2)+']');
    ok(SOL.law.kcl<=TOL_LAW&&SOL.law.kvl<=TOL_LAW,tag+': Kirchhoff closes on the answer ['+SOL.law.kcl.toExponential(1)+', '+SOL.law.kvl.toExponential(1)+']');
    eq(SOL.loops,Rp.loops,tag+': '+Rp.loops+' independent loops'); eq(SOL.comps,Rp.comps,tag+': pieces'); eq(SOL.nodes,Rp.nodes,tag+': nodes'); eq(SOL.branches,Rp.branches,tag+': branches');
    if(Rp.bright) for(const k in Rp.bright) close(SOL.bright.get(+k),Rp.bright[k],1e-14,tag+': bulb '+k+' brightness, PhET\'s rule (python)');
    let gen=0, dis=0, tel=0, big=0; br.forEach((b,k)=>{ const i=SOL.sol.i[k]; gen+=b.E*i; dis+=b.R*i*i; const t=(SOL.sol.v[b.a]-SOL.sol.v[b.b])*i; tel+=t; big=Math.max(big,Math.abs(t),Math.abs(b.E*i)); });
    rel(gen,Rp.Pgen,1e-13,tag+': the EMFs deliver '+fmt(Rp.Pgen,4)+' W (python)'); rel(dis,gen,1e-13,tag+': and the resistances take exactly that');
    ok(Math.abs(tel)<=16*EPS*big*br.length,tag+': Tellegen, sum of (v_a - v_b) i = 0 ['+(tel/big).toExponential(1)+']');
    return {C,SOL};
  }
  for(const key of PRESET_ORDER.slice(1)){
    const g=PRESET_GEOM[key];
    ok(g.els.every(e=>!TYPES[e[0]].L||Math.abs(Math.hypot(g.verts[e[2]][0]-g.verts[e[1]][0],g.verts[e[2]][1]-g.verts[e[1]][1])-TYPES[e[0]].L)<1e-9),key+': every rigid part is PhET\'s length');
    presetCheck(key,REF.presets[key],key); }
  { const {SOL}=presetCheck('short',REF.presets.short,'short (fire)'); ok(SOL.fire.has(0)&&SOL.fire.size===1,'a dead short sets the battery on fire, and only the battery (python) ['+[...SOL.fire]+']');
    ok(REF.presets.short.fire&&REF.presets.short.fire[0]===0,'python agrees which part burns'); }
  presetCheck('bulb',REF.variants.bulb_r2,'one bulb, battery r = 2 ohm',(C,g)=>{ g.rbat=2; });
  presetCheck('bulb',REF.variants.bulb_r10,'one bulb, battery r = 10 ohm',(C,g)=>{ g.rbat=10; });
  presetCheck('bulb',REF.variants.bulb_rhomax,'one bulb, the most resistive wire',(C,g)=>{ g.rho=RHO_MAX; });
  presetCheck('parallel',REF.variants.parallel_r5,'parallel, battery r = 5 ohm',(C,g)=>{ g.rbat=5; });
  { const {SOL}=presetCheck('bridge',REF.variants.bridge_bal,'bridge balanced (R4 = 60)',C=>{ C.els[9].R=60; });
    close(SOL.I.get(12),REF.variants.bridge_bal.i['12'],4*EPS*0.4,'the balanced bridge\'s ammeter carries 3.0e-11 A, from the rails\' 2.4e-8 ohm (python), known to the rounding of the 0.4-A currents it is the difference of'); }
  rel(presetCheck('bulb',REF.presets.bulb,'one bulb (closed form)').SOL.I.get(4),REF.misc.bulbI,2*EPS,'one bulb: I = 9/(1e-4 + 10 + 7.18e-8 of wire), exactly (python)');
  /* PhET's own formulation, the independent twin */
  for(const key of PRESET_ORDER.slice(1)){ const C=presetCircuit(key), SOL=solveCircuit(C,G0), N=SOL.net.N, br=SOL.net.br, ph=phetSolve(N,br);
    const Rv=C.verts.map((v,q)=>REF.presets[key].v[q]), Ri=br.map(e=>REF.presets[key].i[String(e.el.id)]), e=vsExact(N,br,ph,Rv,Ri);
    ok(e.wv<=1e-5&&e.wi<=1e-4,key+': PhET\'s own formulation (resistors as conductances) agrees to 1e-5 in voltage, 1e-4 in current ['+e.wv.toExponential(1)+', '+e.wi.toExponential(1)+']'); }
  { const C=presetCircuit('bridge'), SOL=solveCircuit(C,G0), N=SOL.net.N, br=SOL.net.br, ph=phetSolve(N,br);
    const Rv=C.verts.map((v,q)=>REF.presets.bridge.v[q]), Ri=br.map(e=>REF.presets.bridge.i[String(e.el.id)]);
    const a=vsExact(N,br,SOL.sol,Rv,Ri), b=vsExact(N,br,ph,Rv,Ri);
    ok(b.wi>1e3*Math.max(a.wi,EPS),'and it is why every current is an unknown here: on the bridge the conductance form is '+fmt(b.wi/Math.max(a.wi,EPS),0)+'x further from the exact currents'); }

  /* ---------- 4. Thevenin and superposition on the presets (python) ---------- */
  for(const key in REF.thev){ const [pk,lab2]=key.split('_'), R=REF.thev[key], C=presetCircuit(pk), SOL=solveCircuit(C,G0), T=theveninOf(SOL,+lab2);
    ok(T&&!T.open,key+': the part is in a loop');
    rel(T.Voc,R.Voc,1e-12,key+': V_th with the part removed (python)'); rel(T.Rth,R.Rth,1e-11,key+': R_th with the EMFs zeroed (python)');
    rel((T.Voc+T.E)/(T.R+T.Rth),T.i,1e-12,key+': (V_th + E)/(R + R_th) reproduces the full solve'); rel(T.i,R.i,1e-14,key+': the current itself (python)');
    if(R.Pmax!==undefined) rel(T.Voc*T.Voc/(4*T.Rth),R.Pmax,1e-11,key+': P_max = V_th^2/4R_th (python)'); }
  { const C=presetCircuit('twobat'), SOL=solveCircuit(C,G0), Sp=superpose(SOL), R=REF.super;
    eq(Sp.bats.length,2,'two batteries to superpose');
    let w=0, ws=0; SOL.net.br.forEach((e,k)=>{ const j=R.labels.indexOf(e.el.id); w=Math.max(w,Math.abs(Sp.parts[0][k]-R.parts[0][j]),Math.abs(Sp.parts[1][k]-R.parts[1][j])); ws=Math.max(ws,Math.abs(Sp.parts[0][k]+Sp.parts[1][k]-SOL.sol.i[k])); });
    ok(w<=TOL_I,'two-battery preset: each battery alone matches python ['+w.toExponential(2)+' A]'); ok(ws<=4*EPS,'and the parts sum to the full solution ['+ws.toExponential(2)+' A]'); }
  { const C=presetCircuit('bulb'); C.els.splice(1,1); C.verts=C.verts.filter(v=>C.els.some(e=>e.a===v.id||e.b===v.id));
    const SOL=solveCircuit(C,G0), T=theveninOf(SOL,4); ok(T&&T.open,'with a wire gone the bulb is in no loop: the view says so rather than divide by nothing'); }

  /* ---------- 5. random circuits: 16 decades of resistance (python) ---------- */
  { let wi=0, wv=0, wk=0, wl=0, ti=0;
    for(const R of REF.random){ const br=netOf(R), s=mnaSolve(R.N,br), e=vsExact(R.N,br,s,R.v,R.i), law=kirchhoff(R.N,br,s,cycleBasis(R.N,br));
      wi=Math.max(wi,e.wi); wv=Math.max(wv,e.wv); wk=Math.max(wk,law.kcl); wl=Math.max(wl,law.kvl);
      ti=Math.max(ti,vsExact(R.N,br,phetSolve(R.N,br),R.v,R.i).wi); }
    ok(wi<=TOL_I,'30 random circuits: every current to 16 eps of its piece, against exact rationals (python) ['+wi.toExponential(2)+']');
    ok(wv<=TOL_V,'and every voltage to 64 eps ['+wv.toExponential(2)+']');
    ok(wk<=TOL_LAW&&wl<=TOL_LAW,'and both of Kirchhoff\'s laws close to 8 eps ['+wk.toExponential(1)+', '+wl.toExponential(1)+']');
    ok(ti>1e-8&&ti<1e-3,'the conductance form (PhET\'s) loses digits on them: '+ti.toExponential(1)+' of a piece\'s current (python measures numpy at '+REF.misc.randomNumpyWorst.toExponential(1)+')'); }
  { let seed=97531; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; };
    let wk=0, wl=0, fin=true;
    for(let t=0;t<300;t++){ const N=3+Math.floor(rnd()*10), br=[];
      for(let q=1;q<N;q++) br.push({a:q,b:Math.floor(rnd()*q),R:Math.pow(10,-14+20*rnd()),E:0,kind:'R'});
      const ex=Math.floor(rnd()*N); for(let q=0;q<ex;q++){ const a=Math.floor(rnd()*N), b=Math.floor(rnd()*N); if(a!==b) br.push({a,b,R:Math.pow(10,-14+20*rnd()),E:0,kind:'R'}); }
      const nb=1+Math.floor(rnd()*3); for(let q=0;q<nb;q++){ const a=Math.floor(rnd()*N), b=Math.floor(rnd()*N); if(a!==b) br.push({a,b,R:Math.pow(10,-4+5*rnd()),E:1e5*rnd(),kind:'B'}); }
      const s=mnaSolve(N,br), law=kirchhoff(N,br,s,cycleBasis(N,br));
      wk=Math.max(wk,law.kcl); wl=Math.max(wl,law.kvl); fin=fin&&[...s.v,...s.i].every(isFinite); }
    ok(fin,'300 more random circuits (1e-14 to 1e6 ohm, up to 100 kV): no NaN, no infinity');
    ok(wk<=TOL_LAW&&wl<=TOL_LAW,'and Kirchhoff closes on every one to 8 eps ['+wk.toExponential(1)+', '+wl.toExponential(1)+']'); }

  /* ---------- 6. real bulbs, fuses, switches, fire ---------- */
  for(const [key,lab2] of [['bulb',4],['series',5]]){ const C=presetCircuit(key); C.els[lab2].type='rbulb'; const SOL=solveCircuit(C,G0), R=REF.real[key];
    rel(SOL.R.get(lab2),R.R,1e-13,key+' with a real bulb: its resistance at the fixed point (python, 50 digits)');
    rel(SOL.I.get(lab2),R.I,1e-13,key+' with a real bulb: its current (python)'); ok(SOL.passes<=60,key+': converged in '+SOL.passes+' passes');
    rel(SOL.R.get(lab2),realBulbR(SOL.V.get(C.els[lab2].a)-SOL.V.get(C.els[lab2].b)),1e-13,key+': R = 10 + 3|V|/log2(|V|+2) holds at the answer'); }
  ok(Math.abs(REF.real.series.phetR-REF.real.series.R)>1e-11*REF.real.series.R,'PhET\'s ten passes stop short of the fixed point in the series preset (python: '+(Math.abs(REF.real.series.phetR-REF.real.series.R)/REF.real.series.R).toExponential(1)+')');
  { const mk=R3=>{ const C=presetCircuit('series'); C.els[3].R=R3; C.els[5]=makeEl(5,'fuse',C.els[5].a,C.els[5].b); return C; };
    const C1=mk(1), S1=solveCircuit(C1,G0); ok(C1.els[5].tripped,'a 4-A fuse in series with 1 ohm (8.87 A, python) blows');
    ok(S1.Imax===0&&S1.trips[0]===5,'and then nothing flows'); eq(S1.R.get(5),Infinity,'a blown fuse is out of the circuit');
    const C3=mk(3), S3=solveCircuit(C3,G0); ok(!C3.els[5].tripped,'with 3 ohm (2.98 A) it holds'); rel(S3.I.get(5),REF.fuse['3'].I,4*EPS,'and carries 2.98 A (python)');
    rel(S3.R.get(5),0.015,1e-15,'a 4-A fuse is 15 milliohm (PhET)');
    const C1r=mk(1); reverseBattery(C1r,0); const S1r=solveCircuit(C1r,G0); ok(C1r.els[5].tripped,'with the battery reversed, 8.87 A the other way blows it just the same');
    C1.els[5].tripped=false; const S1b=solveCircuit(C1,G0); ok(C1.els[5].tripped&&S1b.Imax===0,'repaired into the same circuit, it blows again');
    /* the threshold is the rating plus 1e-6 A: aim just below and just above it */
    const Ctot=R3=>{ const C=mk(R3); return BATT_R_MIN+R3+0.015+wireR(139+160+30+140+160+139,RHO_MIN); };
    const aim=(I)=>{ const C=mk(2); C.els[0].E=I*Ctot(2); return C; };
    const Cb=aim(4+0.5e-6); solveCircuit(Cb,G0); ok(!Cb.els[5].tripped,'4.0000005 A through a 4-A fuse: holds (the margin is 1e-6 A, PhET)');
    const Ca=aim(4+2e-6); solveCircuit(Ca,G0); ok(Ca.els[5].tripped,'4.000002 A: blows'); }
  { const C=presetCircuit('series'); C.els[3]=makeEl(3,'switch',C.els[3].a,C.els[3].b);
    let S=solveCircuit(C,G0); eq(S.Imax,0,'an open switch (PhET\'s default) breaks the loop'); ok(S.net.off.length===1&&!S.onK.has(3),'and is not in the netlist at all');
    C.els[3].closed=true; S=solveCircuit(C,G0);
    rel(S.I.get(5),9/(BATT_R_MIN+MIN_R+10+wireR(139+160+30+140+160+139,RHO_MIN)),4*EPS,'closed, it is 0 ohm -> 1.1e-10 ohm (PhET), and the bulb carries E/(r + 10 + wires)'); }
  { const C=presetCircuit('bulb'); C.els[4]=makeEl(4,'resistor',C.els[4].a,C.els[4].b,{R:0.5}); const S=solveCircuit(C,G0);
    ok(S.I.get(4)>=15&&S.fire.has(4)&&S.fire.has(0),'a 0.5-ohm resistor on 9 V carries 18 A: it and the battery burn');
    const C2=presetCircuit('bulb'); C2.els[4].R=0.5; const S2=solveCircuit(C2,G0); ok(S2.I.get(4)>=15&&!S2.fire.has(4),'a bulb carrying the same 18 A never burns (PhET\'s bulbs are not flammable)');
    const C3=presetCircuit('bulb'); C3.els[4]=makeEl(4,'coin',C3.els[4].a,C3.els[4].b); const S3=solveCircuit(C3,G0);
    ok(S3.I.get(4)>1e4&&!S3.fire.has(4)&&S3.fire.has(0),'a coin across the battery: 90 kA, the battery burns, the coin (0 ohm < 1e-8) does not');
    const C4=presetCircuit('bulb'); C4.els[4].R=0.5; C4.els[0].E=7.4; const S4=solveCircuit(C4,G0); ok(S4.I.get(0)<15&&!S4.fire.has(0),'14.8 A is not yet a fire (the line is 15 A)');
    const C6=presetCircuit('bulb'); C6.els[4].R=0.5; C6.els[0].E=7.75; const S6=solveCircuit(C6,G0); ok(S6.I.get(0)>15&&S6.I.get(0)<16&&S6.fire.has(0),'15.5 A is (PhET\'s line is 15 A, not 16) ['+fmt(S6.I.get(0),2)+' A]');
    const C5=presetCircuit('bulb'); C5.els[4]=makeEl(4,'resistor',C5.els[4].a,C5.els[4].b,{R:0.5}); reverseBattery(C5,0); const S5=solveCircuit(C5,G0);
    ok(S5.I.get(4)<=-15&&S5.fire.has(4)&&S5.fire.has(0),'18 A the other way burns just the same'); }

  /* the household objects are PhET's 1.5.2 values: coin and paper clip 0 (so
     1.1e-10), pencil 25, thin pencil 50, eraser and dollar bill 1e6 ohm --
     pinned through a solve, each put where the one-bulb circuit's bulb was */
  for(const [t,R] of [['coin',MIN_R],['clip',MIN_R],['pencil',25],['tpencil',50],['eraser',1e6],['bill',1e6],['resistor',10],['xresistor',1000],['xbulb',1000],['bulb',10]]){
    const C=presetCircuit('bulb'); C.els[4]=makeEl(4,t,C.els[4].a,C.els[4].b); const S=solveCircuit(C,G0);
    rel(S.I.get(4),9/(BATT_R_MIN+R+REF.misc.bulbWireR),4*EPS,TYPES[t].name+' in the loop: '+sigf(R,3)+' ohm (PhET\'s value)'); }

  /* ---------- 7. the editor's operations ---------- */
  { const C=newCircuit(), b=addElement(C,'battery',0,0), A=vById(C,b.a), B=vById(C,b.b);
    close(B.x-A.x,102,0,'a new battery is 102 units long, lying left to right (PhET)'); ok(A.y===0&&B.y===0,'and level');
    const r=addElement(C,'resistor',300,0); close(elLength(C,r),110,1e-12,'a resistor is 110'); const w=addElement(C,'wire',0,120); close(elLength(C,w),100,1e-12,'a new wire is 100');
    for(let k=0;k<4;k++) addElement(C,'xbattery',0,-200); eq(addElement(C,'xbattery',0,-200),null,'PhET\'s toolbox holds four extreme batteries'); eq(remaining(C,'xbattery'),0,'and counts them down');
    eq(remaining(C,'coin'),1,'one coin'); addElement(C,'coin',400,300); eq(addElement(C,'coin',400,400),null,'and no second');
    /* drag the wire's left end onto the battery's - terminal */
    dragVertex(C,w.a,-45,9); const t=dropTarget(C,[w.a]); ok(t&&t.dst===b.a,'a loose end dropped 11 units from a terminal finds it (radius 30, PhET)');
    connect(C,t.src,t.dst); eq(w.a,b.a,'and joins it'); ok(!vById(C,t.src),'the dropped vertex is merged away');
    ok(!canConnect(C,w.b,b.b),'but the wire\'s other end may not join the + terminal: the two would share a neighbour (PhET\'s rule)');
    ok(!canConnect(C,b.a,b.b),'nor may a part\'s two ends join each other');
    const w2=addElement(C,'wire',200,200); dragVertex(C,w2.a,61,5); ok(dropTarget(C,[w2.a]).dst===b.b,'a second wire finds the + terminal');
    dragVertex(C,w2.a,51+25,0); ok(dropTarget(C,[w2.a])&&dropTarget(C,[w2.a]).dst===b.b,'25 units away it still finds it (PhET\'s radius is 30)');
    dragVertex(C,w2.a,51+31,0); eq(dropTarget(C,[w2.a]),null,'31 units away it finds nothing');
    { const C9=newCircuit(), w9=addElement(C9,'wire',0,0), b9=addElement(C9,'battery',120,17);
      const t9=dropTarget(C9,[b9.a,b9.b]); ok(t9&&t9.src===b9.a&&t9.dst===w9.b,'a battery dropped with its - end 17 units off a wire end finds it');
      connect(C9,t9.src,t9.dst); close(elLength(C9,b9),102,1e-12,'and snapping carries the whole battery, so it stays 102 long'); close(vById(C9,b9.b).y,0,1e-12,'and level with the wire'); }
    /* rigid parts: a joint of two batteries moves them as one */
    const C2=newCircuit(), b1=addElement(C2,'battery',0,0), b2=addElement(C2,'battery',102,0);
    connect(C2,b2.a,b1.b); eq(fixedGroup(C2,b1.a).size,3,'two batteries end to end are one rigid body of three vertices');
    dragVertex(C2,b1.b,51,50); close(vById(C2,b1.a).y,50,1e-12,'dragging their shared joint carries both'); close(elLength(C2,b1),102,1e-12,'at their lengths');
    const C3=newCircuit(), rr=addElement(C3,'resistor',0,0), o=vById(C3,rr.a); dragVertex(C3,rr.b,-55,60);
    close(elLength(C3,rr),110,1e-12,'a lone resistor dragged by one end (to a point 60 from the other) swings about the other, keeping its 110');
    close(vById(C3,rr.b).y,110,1e-12,'pointing where the pointer is'); close(vById(C3,rr.a).x,o.x,0,'and the other end stays put');
    /* split and delete */
    const C4=presetCircuit('bulb'), nv=C4.verts.length; ok(splitVertex(C4,1),'the battery\'s + joint splits'); eq(C4.verts.length,nv+1,'into one more vertex');
    eq(solveCircuit(C4,G0).Imax,0,'and the loop is open'); ok(!splitVertex(C4,C4.verts.find(v=>elsAt(C4,v.id).length===1).id),'a loose end has nothing to split');
    close(elLength(C4,C4.els[1]),75,1e-9,'the wire\'s end stepped 24 units back along it (99 -> 75)');
    const C5=presetCircuit('bulb'); deleteElement(C5,1); eq(C5.els.length,7,'deleting a part removes it'); eq(C5.verts.length,8,'and keeps joints still in use');
    deleteElement(C5,0); eq(C5.verts.length,7,'then deleting the battery drops its + terminal, now joined to nothing');
    const C6=newCircuit(), x=addElement(C6,'bulb',0,0); deleteElement(C6,x.id); eq(C6.verts.length,0,'a lone part takes its vertices with it');
    const C7=presetCircuit('bulb'), I0=solveCircuit(C7,G0).I.get(4); reverseBattery(C7,0); rel(solveCircuit(C7,G0).I.get(4),-I0,4*EPS,'reversing the battery reverses every current'); }

  /* ---------- 8. the meters (PhET's connection rules) ---------- */
  { const C=presetCircuit('bulb'), SOL=solveCircuit(C,G0), R=REF.presets.bulb;
    const V1=voltmeterReading(C,SOL,[51,100],[-51,100]); rel(V1.V,R.v[1]-R.v[0],4*EPS,'voltmeter across the battery reads its terminal voltage (python)'); eq(voltageText(V1.V),'9.00 V','shown as PhET does: 9.00 V');
    const V2=voltmeterReading(C,SOL,[45,108],[-51,100]); ok(V2.V!==null&&V2.r.vid===1&&V2.r.el===undefined,'a probe 10 units from a joint, off every wire, reads the joint (PhET\'s 11.2-unit solder radius)');
    eq(voltmeterReading(C,SOL,[43,108],[-51,100]).V,null,'at 11.3 units it reads nothing');
    const Vq=voltmeterReading(C,SOL,[150,60],[-51,100]); rel(Vq.V,R.v[2]+0.25*(R.v[3]-R.v[2])-R.v[0],1e-15,'a quarter of the way along a wire it reads a quarter of the way between its ends');
    const V3=voltmeterReading(C,SOL,[150,20],[-51,100]); rel(V3.V,(R.v[2]+R.v[3])/2-R.v[0],1e-15,'on the middle of a wire it reads halfway between the ends (interpolated, PhET)');
    eq(voltmeterReading(C,SOL,[0,100],[-51,100]).V,null,'on the battery\'s body it reads nothing (not metal)'); eq(voltageText(null),'—','an open probe shows a dash');
    eq(voltmeterReading(C,SOL,[0,0],[-51,100]).V,null,'in empty space, nothing');
    const A1=ammeterReading(C,SOL,0,-60); rel(A1.I,R.i['4'],4*EPS,'the non-contact ammeter over the bulb reads its current (python)'); eq(currentText(Math.abs(A1.I),false),'0.90 A','as 0.90 A');
    eq(ammeterReading(C,SOL,300,300),null,'over nothing, nothing'); eq(currentText(null,false),'—','shown as a dash');
    const Cb=presetCircuit('bridge'), Sb=solveCircuit(Cb,G0); const Ab=ammeterReading(Cb,Sb,-120,-30);
    ok(Ab.el===3,'at a joint of two resistors and a wire the ring reads a resistor, not the wire (PhET: fixed parts first)');
    rel(seriesReading(Cb,Sb,Cb.els[12]),REF.presets.bridge.i['12'],1e-13,'the series ammeter in the bridge reads its branch (python)');
    deleteElement(Cb,13); eq(seriesReading(Cb,solveCircuit(Cb,G0),Cb.els.find(e=>e.id===12)),null,'with one end loose it reads nothing');
    eq(currentText(2e10,false),'> 10^10','PhET\'s ammeter saturates above 1e10 A'); eq(currentText(5e9,false),'5000000000.00 A','and reads 5e9 A in full');
    eq(currentText(2e3,true),'> 10^3','the series ammeter saturates above 1e3 A'); eq(currentText(500,true),'500.00 A','and reads 500 A in full'); eq(currentText(-0.456,false),'0.46 A','and reads magnitudes');
    const Cf=newCircuit(); const f1=addElement(Cf,'battery',0,0), f2=addElement(Cf,'battery',0,300); const Sf=solveCircuit(Cf,G0);
    const Vf=voltmeterReading(Cf,Sf,[51,0],[51,300]); ok(Vf.V===null&&Vf.apart,'probes on two unconnected pieces read nothing (PhET)'); }

  /* ---------- 9. the charges ---------- */
  { const st=clone(DEFAULTS); st.circ=presetCircuit('bulb'); const SOL=solveCircuit(st.circ,G0);
    advanceCharges(st,SOL,FRAME_DT); rel(st.phase[4],CHARGE_SPEED*REF.presets.bulb.i['4']*FRAME_DT,1e-12,'one frame moves the bulb\'s charges 25 units/s per ampere (PhET)');
    const L=elLength(st.circ,st.circ.els[4]), pe=chargePositions(L,10,'electrons'), pc=chargePositions(L,10,'conventional'), p0=chargeLayout(L);
    ok(pe.every((x,j)=>Math.abs(x-((p0[j]-10+L)%L))<1e-9),'electrons slide against the current'); ok(pc.every((x,j)=>Math.abs(x-((p0[j]+10)%L))<1e-9),'conventional charge with it');
    const s2=clone(DEFAULTS); s2.circ=presetCircuit('short'); const S2=solveCircuit(s2.circ,G0); advanceCharges(s2,S2,FRAME_DT);
    rel(s2.phase[0],CHARGE_SPEED*REF.consts.Icap*FRAME_DT,1e-9,'in a dead short the speed limit holds every charge to 14.448 A\'s pace');
    ok(speedNote(chargeScale(S2.Imax)).indexOf('0.016%')>0,'and says so to two figures ('+speedNote(chargeScale(S2.Imax)).slice(-15)+')'); }

  /* ---------- 10. the panels: clean, and carrying the model's numbers ---------- */
  function setupState(over){
    resetState({});
    if(over._preset) applyPreset(ST,over._preset);
    if(over._mod) over._mod(ST);
    for(const k in over) if(k[0]!=='_') ST[k]=clone(over[k]);
  }
  const panels=over=>{ const save=clone(ST); try{ setupState(over); const M=buildModel(); return readoutHTML(M)+eqbarHTML(M)+tagHTML(M); } finally{ resetState(save); } };
  const PCONF=[{},{_preset:'empty'},{_preset:'short',sel:0},{_preset:'bridge',vm:{on:true,bx:0,by:200,rx:-120,ry:-30,kx:120,ky:-30},am:{on:true,bx:200,by:200,px:0,py:-140}},
    {_preset:'twobat',sel:15},{_preset:'series',_mod:st=>{ st.circ.els[5]=makeEl(5,'fuse',st.circ.els[5].a,st.circ.els[5].b); st.circ.els[3].R=1; },sel:5},
    {_preset:'bulb',_mod:st=>{ st.circ.els[4].type='rbulb'; },sel:4,realBulbs:true},{_preset:'parallel',rho:RHO_MAX,rbat:10,sel:0}];
  for(const [v] of TABS) for(const over of PCONF){
    const html=panels(Object.assign({view:v},over));
    ok(html.indexOf('NaN')<0&&html.indexOf('undefined')<0&&html.indexOf('Infinity')<0,'panels clean: '+v+' '+(over._preset||'default')); }
  { const R=REF.presets.bulb;
    ok(panels({sel:4}).indexOf(fmt(R.bright['4'],3))>=0,'the lab readout prints the selected bulb\'s brightness off the model (0.205)');
    ok(panels({sel:4}).indexOf(fmtI(R.i['4']))>=0,'and its current ('+fmtI(R.i['4'])+')');
    ok(panels({view:'power'}).indexOf(fmtP(R.Pgen))>=0,'the power readout prints what the EMF delivers ('+fmtP(R.Pgen)+')');
    ok(panels({view:'thev'}).indexOf(fmtR(REF.thev.bulb_4.Rth))>=0,'the rest-of-the-circuit readout prints R_th ('+fmtR(REF.thev.bulb_4.Rth)+')');
    ok(panels({view:'graph'}).indexOf('<td class="v">15</td>')>=0,'nodes and branches counts 7 + 8 = 15 unknowns');
    const sp=panels({view:'super',_preset:'twobat'}); ok(sp.indexOf(fmtI(REF.super.parts[0][0]))>=0,'superposition prints what battery 1 alone drives ('+fmtI(REF.super.parts[0][0])+')');
    ok(panels({_preset:'short'}).indexOf('0.016%')>=0,'the short\'s readout carries PhET\'s speed-limit note, to two figures');
    ok(panels({_preset:'bridge',vm:{on:true,bx:0,by:200,rx:-120,ry:-140,kx:-120,ky:80},am:{on:false,bx:0,by:0,px:0,py:0}}).indexOf(voltageText(REF.presets.bridge.v[3]-REF.presets.bridge.v[5]))>=0,'the voltmeter row reads across the bridge\'s left divider');
    ok(panels({_preset:'series',_mod:st=>{ st.circ.els[5]=makeEl(5,'fuse',st.circ.els[5].a,st.circ.els[5].b); st.circ.els[3].R=1; }}).indexOf('blown fuse')>=0,'a blown fuse is announced'); }

  /* ---------- 11. layout: every view x configuration x size ---------- */
  const house=()=>{ const C=newCircuit(); [[-51,120],[51,120],[160,120],[160,-10],[95,-10],[-35,-10],[-130,-10],[-205,-10],[-205,120],[95,-150],[5,-150],[-45,-10],[-45,-150]].forEach((p,k)=>C.verts.push({id:k,x:p[0],y:p[1]}));
    [['battery',0,1],['wire',1,2],['wire',2,3],['wire',3,4],['pencil',4,5],['wire',5,11],['coin',11,6],['wire',6,7],['wire',7,8],['wire',8,0],['wire',4,9],['eraser',9,10],['wire',10,12],['wire',12,11]].forEach((e,k)=>C.els.push(makeEl(k,e[0],e[1],e[2])));
    C.nv=13; C.ne=14; return C; };
  const mixed=()=>{ const C=newCircuit(); [[-51,130],[51,130],[180,130],[180,-20],[68,-20],[40,-20],[-70,-20],[-90,-20],[-190,-20],[-190,130]].forEach((p,k)=>C.verts.push({id:k,x:p[0],y:p[1]}));
    [['battery',0,1],['wire',1,2],['wire',2,3],['switch',3,4,{closed:true}],['wire',4,5],['fuse',5,6],['wire',6,7],['rbulb',7,8],['wire',8,9],['wire',9,0]].forEach((e,k)=>C.els.push(makeEl(k,e[0],e[1],e[2],e[3])));
    C.nv=10; C.ne=10; return C; };
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const CONFIGS=[
    ['lab default',{}],['lab series values',{_preset:'series',showValues:true,sel:3}],['lab parallel schematic',{_preset:'parallel',look:'schematic',showValues:true}],
    ['lab bridge meters',{_preset:'bridge',vm:{on:true,bx:40,by:150,rx:-120,ry:-30,kx:120,ky:-30},am:{on:true,bx:250,by:110,px:0,py:-140},showValues:true}],
    ['lab twobat conventional',{_preset:'twobat',carrier:'conventional',showValues:true}],['lab short',{_preset:'short',sel:0,showValues:true}],['lab empty',{_preset:'empty'}],
    ['lab household',{_mod:st=>{ st.circ=house(); },realBulbs:true,showValues:true,zoom:1.6}],['lab mixed schematic',{_mod:st=>{ st.circ=mixed(); },look:'schematic',showValues:true,realBulbs:true}],
    ['lab mixed 0.5',{_mod:st=>{ st.circ=mixed(); },showValues:true,zoom:0.5,selV:3}],['lab no labels',{showLabels:false,_preset:'twobat'}],
    ['graph bulb',{view:'graph'}],['graph bridge',{view:'graph',_preset:'bridge'}],['graph twobat',{view:'graph',_preset:'twobat'}],['graph empty',{view:'graph',_preset:'empty'}],['graph household',{view:'graph',_mod:st=>{ st.circ=house(); }}],
    ['power parallel',{view:'power',_preset:'parallel'}],['power twobat',{view:'power',_preset:'twobat'}],['power short',{view:'power',_preset:'short'}],['power empty',{view:'power',_preset:'empty'}],['power mixed',{view:'power',_mod:st=>{ st.circ=mixed(); }}],
    ['thev bulb',{view:'thev'}],['thev R3',{view:'thev',_preset:'twobat',sel:15}],['thev ammeter',{view:'thev',_preset:'bridge',sel:12}],['thev battery',{view:'thev',_preset:'twobat',sel:0}],
    ['thev real',{view:'thev',_mod:st=>{ st.circ=mixed(); },sel:7}],['thev empty',{view:'thev',_preset:'empty'}],['thev open',{view:'thev',_mod:st=>{ st.circ.els.splice(1,1); },sel:4}],
    ['super twobat',{view:'super',_preset:'twobat'}],['super bulb',{view:'super'}],['super empty',{view:'super',_preset:'empty'}],['super household',{view:'super',_mod:st=>{ st.circ=house(); }}],
  ];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over] of CONFIGS) for(const [W,H] of SIZES){
    const save=clone(ST); setupState(over);
    try{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) continue;
      /* the floor counts what the ops carry (a line plot is strokes), not fills alone */
      const texts=c.ops.filter(o=>o.op==='text'), marks=c.ops.filter(o=>o.op==='fill'||(o.op==='stroke'&&o.pts.length>=2));
      ok((marks.length>=8&&texts.length>=1)||texts.some(t=>/nothing on the bench|no part|not in any loop|no battery|never comes back|bench is empty/.test(t.t)),nm+' '+W+'x'+H+' draws substance or says why ('+marks.length+' marks)');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null; const flat=texts.filter(t=>!t.rot);
      for(let i2=0;i2<flat.length&&!hit;i2++) for(let j2=i2+1;j2<flat.length;j2++){
        const a=flat[i2].bb,b=flat[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
        if(ox>0.5&&oy>0.5){ hit='"'+flat[i2].t.slice(0,22)+'" vs "'+flat[j2].t.slice(0,22)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner */
      const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
      ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
        const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses the legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legend clear');
    } finally{ resetState(save); }
  }
  /* a caption describes only what its view drew (Known-bad: a clause true of
     one case printed in another) */
  for(const [W,H] of SIZES) for(const [v,pre,sel] of [['thev','twobat',15],['thev','twobat',0],['graph','bridge',null]]){
    const save=clone(ST); resetState({view:v}); applyPreset(ST,pre); ST.sel=sel;
    const c=makeShot(W,H); drawView(c,W,H,buildModel()); const ts=c.ops.filter(o=>o.op==='text').map(o=>o.t), txt=ts.join(' '); resetState(save);
    const sweep=ts.some(t=>t==='its resistance R (log axis)'), mat=ts.some(t=>/^the matrix/.test(t));
    if(v==='thev') ok(sweep===/On the right, the power/.test(txt),'thev '+pre+'/'+sel+' '+W+'x'+H+': the caption names the power sweep exactly when it is drawn ('+sweep+')');
    else ok(mat===/The matrix is the system/.test(txt),'graph '+W+'x'+H+': the caption describes the matrix exactly when it is drawn ('+mat+')'); }
  /* PhET's three zooms scale the bench, about its centre */
  { const z1=labGeo(1400,820,Object.assign(clone(ST),{zoom:1})), z16=labGeo(1400,820,Object.assign(clone(ST),{zoom:1.6})), z05=labGeo(1400,820,Object.assign(clone(ST),{zoom:0.5}));
    rel(z16.sc,1.6*z1.sc,1e-15,'zoom 1.6 draws the bench 1.6 times larger'); rel(z05.sc,0.5*z1.sc,1e-15,'and zoom 0.5 half size');
    close(z16.map.X(0),z1.map.X(0),0,'about the same centre'); rel(z16.map.X(100)-z16.map.X(0),1.6*(z1.map.X(100)-z1.map.X(0)),1e-15,'so 100 units of wire span 1.6 times the pixels'); }
  /* the toolbox never reaches the #hint line, at any size, with the real bulbs in */
  for(const [W,H] of SIZES){ const save=clone(ST); ST.realBulbs=true; const G=labGeo(W,H,ST); resetState(save);
    ok(G.tb.y+G.tb.h<=H-27,'the toolbox ends above the #hint line at '+W+'x'+H+' ('+fmt(G.tb.y+G.tb.h,0)+')');
    ok(G.tb.items.length===19&&G.tb.items.every(it=>it.x+it.w<=G.tb.x+G.tb.w+0.5),'and holds all 19 tools inside it'); }
  /* the bulb's glow is PhET's opacity map, and it reaches the drawn colour */
  close(glowOf(0.2),0.4,1e-15,'lit glass at brightness 0.2 is 40 % on (PhET: linear to full at 0.5)'); eq(glowOf(0.7),1,'and full above 0.5');
  { const save=clone(ST); resetState({}); const c=makeShot(1400,820); drawView(c,1400,820,buildModel()); const lit=c.ops.filter(o=>o.op==='fill'&&/^rgb\(/.test(o.style)).map(o=>brightnessCss(o.style));
    ST.circ.els[0].E=0; for(const k in MEMO) delete MEMO[k]; const c2=makeShot(1400,820); drawView(c2,1400,820,buildModel()); const dark=c2.ops.filter(o=>o.op==='fill'&&/^rgb\(/.test(o.style)).map(o=>brightnessCss(o.style));
    resetState(save);
    ok(Math.max(...lit)>Math.max(...dark)+20,'a lit bulb draws brighter glass than a dark one ('+Math.max(...lit)+' vs '+Math.max(...dark)+')'); }

  /* ---------- 12. building a circuit with the pointer, headless ---------- */
  withState({},()=>{
    applyPreset(ST,'empty'); ST.showCurrent=false;
    const shot=makeShot(1400,820), S=makeScene({getContext:()=>shot}); S.W=1400; S.H=820;
    const G=labGeo(1400,820,ST), m=G.map, tool=k=>G.tb.items.find(it=>it.key===k), mid=it=>[it.x+it.w/2,it.y+it.h/2];
    const drag=(p,q)=>{ const r=S.pointer('down',p[0],p[1]); S.pointer('move',(p[0]+q[0])/2,(p[1]+q[1])/2); S.pointer('move',q[0],q[1]); S.pointer('up',0,0); return r; };
    const W2S=(x,y)=>[m.X(x),m.Y(y)];
    ok(drag(mid(tool('battery')),W2S(0,100)),'pressing the toolbox\'s battery picks one up'); eq(ST.circ.els.length,1,'and dropped on the bench it stays');
    const bat=ST.circ.els[0]; close(vById(ST.circ,bat.a).x,-51,1e-9,'where it was dropped (centred under the pointer)'); close(vById(ST.circ,bat.b).y,100,1e-9,'level');
    eq(ST.preset,'custom','a hand-built bench lets go of the preset chip');
    drag(mid(tool('bulb')),W2S(0,-60)); const bulb=ST.circ.els[1]; eq(bulb.type,'bulb','a bulb next');
    drag(mid(tool('wire')),W2S(100,20)); drag(mid(tool('wire')),W2S(-100,20)); eq(ST.circ.els.length,4,'and two wires');
    const w1=ST.circ.els[2], w2=ST.circ.els[3];
    /* join the ends: each dropped a few units off a terminal, inside PhET's 30-unit radius */
    drag(W2S(50,20),W2S(55,96)); eq(w1.a,bat.b,'wire 1\'s end, dropped 6 units from the battery\'s + terminal, joins it');
    drag(W2S(150,20),W2S(46,-52)); eq(w1.b,bulb.b,'its other end joins the bulb');
    drag(W2S(-50,20),W2S(-55,-66)); eq(w2.b,bulb.a,'wire 2 joins the bulb\'s other end');
    drag(W2S(-150,20),W2S(-47,93)); eq(w2.a,bat.a,'and closes the loop at the - terminal');
    let SOL=solutionOf(ST); eq(SOL.loops,1,'one loop'); const Rw=wireR(elLength(ST.circ,w1),RHO_MIN)+wireR(elLength(ST.circ,w2),RHO_MIN);
    rel(Math.abs(SOL.I.get(bulb.id)),9/(BATT_R_MIN+10+Rw),4*EPS,'and the bulb carries E/(r + R + wires), whatever length the wires were dragged to');
    ok(SOL.I.get(bulb.id)<0,'from its b end to its a end, the way it was wired (the battery\'s + joins the bulb\'s b)');
    close(SOL.bright.get(bulb.id),brightnessOf(SOL.I.get(bulb.id)**2*10),1e-15,'and glows by PhET\'s rule');
    /* a tap selects; a tap on a switch toggles it */
    ST.thevEl=bat.id; const bc=W2S(0,-60); S.pointer('down',bc[0],bc[1]); S.pointer('up',0,0); eq(ST.sel,bulb.id,'a tap on the bulb selects it');
    eq(focusElement(ST,solutionOf(ST)),bulb.id,'and hands the rest-of-the-circuit view to it, over a part stepped to earlier');
    drag(mid(tool('switch')),W2S(0,230)); const sw=ST.circ.els[4]; eq(sw.closed,false,'a new switch is open (PhET)');
    const sc2=W2S(0,230); S.pointer('down',sc2[0],sc2[1]); S.pointer('move',sc2[0]+3,sc2[1]+2); S.pointer('up',0,0); eq(sw.closed,true,'a tap (moving less than 15 px) closes it'); eq(ST.sel,sw.id,'and selects it');
    S.pointer('down',sc2[0]+3,sc2[1]+2); S.pointer('up',0,0); eq(sw.closed,false,'another tap opens it');
    /* back into the toolbox: gone */
    const n0=ST.circ.els.length; drag(W2S(0,230),mid(tool('fuse'))); eq(ST.circ.els.length,n0-1,'a part dropped on the toolbox goes back into it');
    eq(ST.sel,null,'and is no longer selected');
    /* a part dragged whole, and a joint dragged: rigid parts swing */
    const b0=vById(ST.circ,bat.a).x; drag(W2S(-20,100),W2S(-20,140)); close(vById(ST.circ,bat.a).y,140,1e-9,'dragging the battery\'s body moves it'); close(vById(ST.circ,bat.a).x,b0,1e-9,'straight down');
    rel(Math.abs(solutionOf(ST).I.get(bulb.id)),9/(BATT_R_MIN+10+wireR(elLength(ST.circ,w1),RHO_MIN)+wireR(elLength(ST.circ,w2),RHO_MIN)),4*EPS,'the wires stretched with it and the circuit re-solved');
    /* the split button */
    const jb=W2S(vById(ST.circ,bat.b).x,vById(ST.circ,bat.b).y); S.pointer('down',jb[0],jb[1]); S.pointer('up',0,0); eq(ST.selV,bat.b,'a tap on a joint selects it');
    const sb=splitButton(G,ST); ok(!!sb,'and offers PhET\'s split button'); S.pointer('down',sb.x+5,sb.y+5); S.pointer('up',0,0);
    eq(solutionOf(ST).loops,0,'splitting the joint opens the loop'); eq(ST.selV,null,'and clears the joint selection');
    /* the meters */
    ok(S.pointer('down',...mid(tool('voltmeter'))),'the voltmeter comes out of the toolbox'); S.pointer('move',...W2S(300,150)); S.pointer('up',0,0); ok(ST.vm.on,'and stays out');
    const Vg=vmGeo(G,ST); ok(S.pointer('down',Vg.red.T[0],Vg.red.T[1])&&DRAG.what==='vm-red','its red probe grabs by the tip');
    S.pointer('move',...W2S(vById(ST.circ,bat.a).x,vById(ST.circ,bat.a).y)); S.pointer('up',0,0);
    const Vg2=vmGeo(G,ST); S.pointer('down',Vg2.black.T[0],Vg2.black.T[1]); S.pointer('move',...W2S(vById(ST.circ,bat.b).x,vById(ST.circ,bat.b).y)); S.pointer('up',0,0);
    rel(buildModel().vm.V,-9,1e-12,'red on -, black on +: the voltmeter reads -9.00 V across the open battery'); eq(voltageText(buildModel().vm.V),'-9.00 V','shown as PhET does, -9.00 V');
    const Vg3=vmGeo(G,ST); drag(Vg3.c,mid(tool('bulb'))); ok(!ST.vm.on,'dropped on the toolbox, it is put away');
    ok(S.pointer('down',...mid(tool('probe'))),'the non-contact ammeter comes out'); S.pointer('move',...W2S(300,100)); S.pointer('up',0,0); ok(ST.am.on,'and stays');
    /* the wheel steps PhET's three zooms */
    eq(ST.zoom,1,'zoom 1'); ok(S.wheel(-100)&&ST.zoom===1.6,'the wheel zooms in to 1.6'); ok(!S.wheel(-100),'and no further');
    ok(S.wheel(100)&&S.wheel(100)&&ST.zoom===0.5,'and out to 0.5'); ok(!S.wheel(100),'and no further');
    ST.view='graph'; ok(!S.wheel(-100),'only the lab zooms'); ok(!S.pointer('down',500,300),'and only the lab takes the pointer'); ST.view='lab';
    ok(!S.pointer('down',1300,760),'empty bench grabs nothing'); S.pointer('up',0,0);
  });
  withState({},()=>{
    const C=newCircuit(); ST.circ=C; const wz=addElement(C,'wire',0,0), rz=addElement(C,'resistor',0,-9);
    vById(C,wz.a).x=-200; vById(C,wz.b).x=200; const G=labGeo(1400,820,ST), m=G.map;
    eq(hitElement(G,ST,m.X(0),m.Y(-3)),rz.id,'where a wire runs under a resistor, the pointer takes the resistor (PhET: parts sit over wires)');
    eq(hitElement(G,ST,m.X(150),m.Y(-3)),wz.id,'and away from it, the wire');
    const S=makeScene({getContext:()=>makeShot(1400,820)}); S.W=1400; S.H=820; const sw=addElement(C,'switch',0,200), p=[m.X(0),m.Y(200)];
    S.pointer('down',p[0],p[1]); S.pointer('move',p[0]+10,p[1]); S.pointer('up',0,0); eq(sw.closed,true,'a press that travels 10 px is still a tap (PhET\'s threshold is 15 px) and toggles the switch');
    S.pointer('down',p[0]+10,p[1]); S.pointer('move',p[0]+30,p[1]); S.pointer('up',0,0); eq(sw.closed,true,'one that travels 20 px is a drag and leaves it alone');
  });
  /* the drop target a drag would join, and a tap on empty space that deselects */
  withState({},()=>{
    const S=makeScene({getContext:()=>makeShot(1400,820)}); S.W=1400; S.H=820; const G=labGeo(1400,820,ST), m=G.map;
    ST.sel=4; S.pointer('down',m.X(0),m.Y(60)); ok(S.pointer('up',0,0)&&ST.sel===null,'a tap on empty bench clears the selection');
    const p=[m.X(150),m.Y(20)]; S.pointer('down',p[0],p[1]); eq(DRAG.what,'el','a press on a wire grabs the wire'); S.pointer('up',0,0); eq(ST.sel,2,'and a tap selects it');
    const r=[m.X(-150),m.Y(-60)]; S.pointer('down',r[0],r[1]); eq(DRAG.what,'vert','a press on a joint grabs the joint'); S.pointer('up',0,0);
  });

  /* ---------- 13. the frame loop's contract ---------- */
  withState({},()=>{
    const S=makeScene({getContext:()=>makeShot(1400,820)}); S.W=1400; S.H=820;
    ok(S.animating(),'the lab with current flowing animates'); const p0=ST.phase[4]||0; ok(S.step()&&ST.phase[4]!==p0,'and each frame moves the charges');
    ST.showCurrent=false; ok(!S.animating()&&!S.step(),'with the current hidden it is still');
    ST.showCurrent=true; ST.view='graph'; ok(!S.animating(),'the analysis views never animate');
    ST.view='lab'; applyPreset(ST,'empty'); ok(!S.animating(),'nor does an empty bench');
  });

  const dt=(Date.now()-T0)/1000;
  console.log(pass+' passed, '+fail+' failed  ('+fmt(dt,1)+' s)');
  if(fail>0) throw new Error(fail+' self-test failure(s)');
  return fail;
}

/* ============================== entry ============================= */
if(typeof document==='undefined'){
  selfTest();
} else {
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',boot);
  else boot();
}
