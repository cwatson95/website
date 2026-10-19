
/* ================================================================== *
 *  selfTest — headless verification.  Reference values labelled       *
 *  (python) are lines of build/energy-forms-and-changes/refvals.txt,  *
 *  the printed output of derive.py (an independent Python twin, with  *
 *  scipy.linalg.expm for the exact solutions), read in full.          *
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
    beginPath(){ pend=null; }, moveTo(){}, lineTo(){ if(!pend) pend={n:0}; }, closePath(){},
    rect(){ if(!pend) pend={n:0}; pend.n++; }, arc(){ if(!pend) pend={n:0}; pend.n++; },
    fill(){ if(pend) ops.push({op:'fill',n:pend.n||1,style:ctx.fillStyle}); },
    stroke(){ ops.push({op:'stroke'}); }, clip(){},
    fillRect(x,y,w,hh){ ops.push({op:'fill',n:1,bb:[x,y,x+w,y+hh],style:ctx.fillStyle}); },
    strokeRect(){ ops.push({op:'stroke'}); }, clearRect(){},
    fillText(t,x,y){
      const w=(''+t).length*fsz()*0.52, fh=fsz()*1.15;
      const lx=st2.align==='center'?x-w/2:(st2.align==='right'?x-w:x);
      const ly=st2.base==='top'?y:(st2.base==='middle'?y-fh/2:(st2.base==='bottom'?y-fh:y-fh*0.8));
      const cs=[[lx,ly],[lx+w,ly],[lx,ly+fh],[lx+w,ly+fh]].map(c2=>app(c2[0],c2[1]));
      const xs=cs.map(c2=>c2[0]), ys=cs.map(c2=>c2[1]);
      ops.push({op:'text',t:''+t,bb:[Math.min.apply(0,xs),Math.min.apply(0,ys),Math.max.apply(0,xs),Math.max.apply(0,ys)]});
    },
    strokeText(){}, setLineDash(){},
    measureText(t){ return {width:(''+t).length*fsz()*0.52}; },
    createLinearGradient(){ return {addColorStop(){}}; },
  };
  let _fill='#000';
  Object.defineProperty(ctx,'fillStyle',{get:()=>_fill,set:v=>_fill=''+v});
  for(const kk of ['strokeStyle','lineWidth','globalAlpha','lineJoin','lineCap']){ let v2; Object.defineProperty(ctx,kk,{get:()=>v2,set:x=>v2=x}); }
  Object.defineProperty(ctx,'font',{get:()=>st2.font,set:v=>st2.font=''+v});
  Object.defineProperty(ctx,'textAlign',{get:()=>st2.align,set:v=>st2.align=''+v});
  Object.defineProperty(ctx,'textBaseline',{get:()=>st2.base,set:v=>st2.base=''+v});
  return ctx;
}

function selfTest(){
  let pass=0,fail=0;
  const ok=(c,name)=>{ if(c) pass++; else { fail++; console.log('FAIL — '+name); } };
  const eq=(a,b,name)=>ok(a===b,name+' ['+a+' vs '+b+']');
  const close=(a,b,tol,name)=>ok(Math.abs(a-b)<=tol,name+' ['+a+' vs '+b+']');
  const rel=(a,b,t,name)=>ok(Math.abs(a-b)<=t*Math.abs(b||1),name+' ['+a+' vs '+b+', rel '+(Math.abs(a-b)/Math.abs(b||1)).toExponential(2)+']');
  const R=k=>{ if(!(k in REF)) throw new Error('no reference value "'+k+'" in refvals.txt'); return REF[k]; };
  const T0=Date.now(), EPS=Math.pow(2,-52);
  const stSave=Object.assign({},ST);
  const NAMES=['iron','brick','water','oil'];
  function freshBench(){ const B={}; benchReset(B); return B; }
  function runBench(B,lev,n,chk){
    let worst=0, sum=0;
    for(let k=0;k<n;k++){
      const r=benchStep(B,lev);
      const sc=B.bodies.reduce((s,b)=>s+Math.abs(b.E),0)+Math.abs(B.room)+Math.abs(B.work);
      worst=Math.max(worst,Math.abs(r)/sc); sum+=r;
      if(chk) chk(B,k);
    }
    return {worst,sum};
  }
  /* the chunk rule's two guarantees, checked after EVERY step of a run */
  function chunkChecker(tag){
    const st={dev:0,id:0,min:99,bad:null};
    const fn=(B,k)=>{
      for(let i=0;i<4;i++){
        const d=Math.abs(B.own[i]-gChunks(B.bodies[i].E)); if(d>st.dev) st.dev=d;
        const idd=Math.abs(benchIdentity(B,i)-benchIdentity0(B,i))/Math.max(1,B.bodies[i].E); if(idd>st.id) st.id=idd;
        if(B.own[i]<st.min) st.min=B.own[i];
      }
    };
    fn.st=st; return fn;
  }

  /* ---------- A. PhET's constants, and PhET's own chunk tables ---------- */
  rel(EPC,R('EPC (J) = Fb(2) - Fb(1)'),1e-14,'EPC = Fb(2) - Fb(1) (python)');
  rel(EPC,5019.022369565224,1e-12,'EPC is 5019.022 J, absolute');
  rel(EPC,R('EPC direct = (ZB - QB)/1.15'),1e-12,'EPC agrees with the direct (ZB - QB)/1.15 (python)');
  rel(QB,R('QB brick energy at 273.15 K (J)'),1e-14,'QB (python)'); rel(ZB,R('ZB brick energy at 296 K (J)'),1e-14,'ZB (python)');
  eq(T_AIR,R('T_AIR (K)'),'the air sits at exactly 296 K (python)');
  for(let k=0;k<6;k++) eq(SPOTS[k],R('spot '+k+' x (m)'),'spot '+k+' (python)');
  eq(SPOTS[0],-0.241,'spot 0 is -0.241 (PhET rounds -241.4999... down), absolute');
  const B0=freshBench();
  B0.bodies.forEach((b,i)=>{
    rel(b.m,R('mass '+NAMES[i]+' (kg)'),1e-14,'mass of the '+NAMES[i]+' (python)');
    rel(b.m*b.c,R('C '+NAMES[i]+' (J/K)'),1e-14,'heat capacity of the '+NAMES[i]+' (python)');
    rel(b.E,R('E '+NAMES[i]+' at 296 K (J)'),1e-14,'energy of the '+NAMES[i]+' at 296 K (python)');
    rel(gChunks(b.E),R('g chunks '+NAMES[i]+' at 296 K'),1e-12,'g(E) of the '+NAMES[i]+' at 296 K (python)');
    eq(nChunks(b.E),R('n chunks '+NAMES[i]+' at 296 K'),'chunks of the '+NAMES[i]+' at 296 K (python)');
    eq(nChunks(bodyMinE(b)),R('n chunks '+NAMES[i]+' at 273.15 K'),'chunks of the '+NAMES[i]+' at 0 C (python)');
    eq(nChunks(bodyCap(b)*b.m*b.c),R('n chunks '+NAMES[i]+' at cap '+(b.kind==='block'?'620':(b.mat==='water'?'373.15':'573.15'))+' K'),'chunks of the '+NAMES[i]+' at its cap (python)');
  });
  /* PhET's predistributed chunk configurations (Beaker.js, Block.js, the heater's
     beaker) hold 6, 2, 34, 8 and 20 chunks: an independent check of the map and
     the masses, straight from PhET's build */
  eq(B0.own.join(','),'6,2,34,8','the four bodies start with PhET’s 6, 2, 34 and 8 chunks');
  eq(nChunks(HB_C*T_ROOM),20,'the heater’s beaker starts with PhET’s 20 chunks');
  rel(HB_M,R('heater beaker mass (kg)'),1e-14,'heater beaker mass (python)'); rel(HB_C,R('heater beaker C (J/K)'),1e-14,'heater beaker C (python)');
  rel(B0.bodies[0].m,0.710775,1e-12,'the iron block is 0.710775 kg, absolute'); rel(B0.bodies[2].m*B0.bodies[2].c,795.8488677091559,1e-12,'the water is 795.849 J/K, absolute');
  eq(roundSym(2.5),3,'roundSymmetric(2.5) = 3'); eq(roundSym(-2.5),-3,'roundSymmetric(-2.5) = -3'); eq(roundSym(2.4999),2,'roundSymmetric(2.4999) = 2');
  eq(nChunks(-1e9),0,'the map never goes below zero chunks');

  /* ---------- B. PhET's contact lengths ---------- */
  const blk=(x,y)=>({x0:x-0.0225,y0:y,x1:x+0.0225,y1:y+0.045,imm:false});
  const bkr=(x,y,f)=>({x0:x-0.0425,y0:y,x1:x+0.0425,y1:y+BEAKER_H*f,imm:true});
  rel(contactLen(blk(0,0),blk(0,0.045)),R('L stacked aligned'),1e-14,'stacked blocks touch along 4.5 cm (python)');
  rel(contactLen(blk(0,0),blk(0.01,0.045)),R('L stacked offset 0.01'),1e-14,'offset stack touches along the overlap (python)');
  rel(contactLen(blk(0,0.045),blk(0,0)),R('L stacked reversed'),1e-14,'contact is symmetric (python)');
  eq(contactLen(blk(0,0),blk(0.045,0)),R('L side by side'),'side by side, no contact (PhET) (python)');
  rel(contactLen(blk(0.145,0.001),bkr(0.145,0,0.743)),R('L immersed (block in beaker f=0.743)'),1e-14,'immersed: the whole 18-cm perimeter (python)');
  rel(contactLen(blk(0.145,0.001),bkr(0.145,0,0.3)),R('L half immersed (block top above fluid f=0.3)'),1e-12,'partly wet: the wetted perimeter less the dry top (python)');
  rel(contactLen(blk(0,0),bkr(0,0.045,0.5)),R('L beaker on block'),1e-14,'a beaker on a block touches along 4.5 cm (python)');
  rel(contactLen(AIR_AREA,blk(0,0)),R('L air around block'),1e-14,'the room: a block’s whole perimeter (python)');
  rel(contactLen(AIR_AREA,bkr(0.145,0,0.5)),R('L air around water f=0.5'),1e-14,'the room: the liquid’s perimeter (python)');
  eq(contactLen(bkr(0,0,0.5),bkr(0.085,0,0.5)),R('L beaker to beaker side by side'),'beakers side by side, no contact (python)');

  /* ---------- C. the bench's scenarios, step by step against the twin ---------- */
  const scen=(tag,B,worst,lev)=>{
    B.bodies.forEach((b,i)=>{
      rel(b.E,R(tag+' E '+NAMES[i]+' (J)'),1e-11,tag+': E of the '+NAMES[i]+' (python)');
      rel(bodyT(b),R(tag+' T '+NAMES[i]+' (K)'),1e-11,tag+': T of the '+NAMES[i]+' (python)');
    });
    rel(B.room,R(tag+' room (J)'),1e-9,tag+': the room’s intake (python)');
  };
  const ownEq=(tag,B)=>B.bodies.forEach((b,i)=>eq(B.own[i],R(tag+' own '+NAMES[i]),tag+': chunks of the '+NAMES[i]+' (python)'));
  const ckA=chunkChecker('A');
  const A=freshBench(); benchPlace(A,0,2);
  const rA=runBench(A,[1,0],1800,ckA);
  scen('A',A); ownEq('A',A);
  rel(A.work,R('A work (J)'),1e-12,'A: the burner did 150 kJ in 30 s (python)'); rel(A.work,150000,1e-12,'A: 5000 W x 30 s, absolute');
  ok(rA.worst<=8*EPS,'A: every step’s ledger closes to rounding ('+rA.worst.toExponential(2)+' of the energies)');
  ok(Math.abs(rA.sum)<1e-7,'A: summed over 1800 steps the residual is '+rA.sum.toExponential(2)+' J of 5e5');
  ok(ckA.st.dev<1,'A: no body ever a whole chunk from g(E) (max '+fmt(ckA.st.dev,4)+')');
  rel(ckA.st.dev,R('A max |own - g|'),1e-9,'A: the largest |own - g| (python)');
  ok(ckA.st.id<1e-12,'A: the chunk identity E + S - EPC n holds at every step ('+ckA.st.id.toExponential(2)+')');
  rel(bodyT(A.bodies[0]),T_BLOCK_MAX,1e-12,'A: the iron is held at PhET’s 620-K cap');
  /* B: then into the water */
  benchPlace(A,0,4);
  close(A.bodies[0].y,R('B iron y (m)'),1e-15,'B: the iron sits 1 mm inside the beaker (python)');
  const ckB=chunkChecker('B'); benchStep(A,[0,0]);
  rel(A.bodies[2].f,R('B water fluid proportion after one step'),1e-14,'B: one step lifts the water to 0.743 (python)');
  const rB=runBench(A,[0,0],599,ckB);
  scen('B',A); ownEq('B',A);
  ok(rB.worst<=8*EPS,'B: every step’s ledger closes ('+rB.worst.toExponential(2)+')');
  eq(A.moved.pair,R('B chunks moved pair'),'B: chunks moved between bodies (python)');
  eq(A.moved.burner,R('B chunks moved burner'),'B: chunks moved to and from the burner (python)');
  eq(A.moved.air,R('B chunks moved air'),'B: chunks moved to and from the room (python)');
  ok(ckB.st.dev<1&&ckB.st.id<1e-12,'B: the chunk rule holds through the plunge');
  ok(isImmersed(A.bodies,A.bodies[0]),'B: the iron counts as immersed (no room exchange of its own)');
  /* C: brick on iron on the right burner, cooling */
  const C=freshBench(); benchPlace(C,0,3); benchPlace(C,1,3);
  close(C.bodies[1].y,R('C brick y (m)'),1e-15,'C: the brick sits on the iron (python)');
  const ckC=chunkChecker('C'); const rC=runBench(C,[0,-1],1200,ckC);
  scen('C',C); ownEq('C',C); rel(C.work,R('C work (J)'),1e-10,'C: the burner’s (negative) work (python)');
  ok(rC.worst<=8*EPS&&ckC.st.dev<1&&ckC.st.min>=1,'C: ledger, chunk bound and never an empty body');
  ok(bodyT(C.bodies[0])>=T_FREEZE,'C: cooling never takes the iron below 0 C');
  /* D: boiling */
  const D=freshBench(); benchPlace(D,2,2); const rD=runBench(D,[1,0],3600,null);
  rel(D.bodies[2].E,R('D E water (J)'),1e-12,'D: the water ends at its boiling energy (python)');
  eq(bodyT(D.bodies[2]),T_BOIL.water,'D: the water is held at 373.15 K');
  rel(D.room,R('D room (J)'),1e-10,'D: the room took the steam (python)'); eq(D.own[2],R('D own water'),'D: chunks of the boiling water (python)');
  ok(rD.worst<=8*EPS,'D: the ledger closes through boiling');
  /* E, F, G, H */
  const Eb=freshBench(); benchPlace(Eb,3,3); runBench(Eb,[0,1],5400,null);
  rel(Eb.bodies[3].E,R('E E oil (J)'),1e-12,'E: the oil at its 573.15-K cap (python)'); rel(Eb.room,R('E room (J)'),1e-10,'E: the room (python)');
  const F=freshBench(); benchPlace(F,0,2); runBench(F,[1,0],7200,null);
  rel(F.bodies[0].E,R('F E iron (J)'),1e-12,'F: the iron at 620 K (python)'); rel(F.room,R('F room (J)'),1e-10,'F: the room (python)'); eq(F.own[0],R('F own iron'),'F: 27 chunks at the cap (python)');
  const G=freshBench(); benchPlace(G,2,2); runBench(G,[-1,0],2400,null);
  rel(G.bodies[2].E,R('G E water (J)'),1e-11,'G: the cooled water (python)'); rel(G.work,R('G work (J)'),1e-10,'G: the cooling work (python)');
  ok(bodyT(G.bodies[2])>=T_FREEZE-1e-12,'G: the water is clamped at 0 C');
  const Hh=freshBench(); runBench(Hh,[0.7,-0.4],600,null);
  rel(Hh.room,R('H room (J)'),1e-12,'H: empty burners work straight on the room (python)'); rel(Hh.room,4500,1e-12,'H: (0.7 - 0.4) x 1500 W x 10 s, absolute');
  eq(Hh.bodies[0].E,R('H E iron (J)'),'H: the iron is untouched');
  /* I: two blocks in the water: PhET's displacement, one update a step */
  const I=freshBench(); benchPlace(I,0,4); benchPlace(I,1,4);
  close(I.bodies[1].y,R('I brick y (m)'),1e-15,'I: the brick sits on the iron inside the beaker (python)');
  for(let s=1;s<=8;s++){ benchStep(I,[0,0]); rel(I.bodies[2].f,R('I water f after step '+s),1e-13,'I: the water level after step '+s+' (python)'); }
  close(I.bodies[2].f,0.986,1e-15,'I: two blocks lift the water to 0.5 + 120 x 0.00405 = 0.986');

  /* ---------- C2. the paths no scenario reaches, pinned directly ---------- */
  { const a=makeBody(0), b=makeBody(2); a.x=SPOTS[4]; b.x=SPOTS[4]; a.y=0.001; b.f=FLUID0+DISPLACE*BLOCK*BLOCK; a.E=a.m*a.c*450;
    const q=exchange(a,b,3/60);
    rel(a.E,R('substep exchange 3/60 s: E iron (J)'),1e-13,'PhET’s substeps: 3/60 s is three 1/60-s exchanges (python)');
    rel(b.E,R('substep exchange 3/60 s: E water (J)'),1e-13,'...the water (python)'); rel(q,R('substep exchange 3/60 s: energy iron -> water (J)'),1e-11,'...the energy moved (python)');
    const a1=makeBody(0), b1=makeBody(2); a1.x=SPOTS[4]; b1.x=SPOTS[4]; a1.y=0.001; b1.f=b.f; a1.E=a1.m*a1.c*450; exchange(a1,b1,DT);
    const one=a.m*a.c*450-a1.E; ok(Math.abs((a.m*a.c*450-a.E)-3*one)>1,'three substeps are not three times one: the temperatures update between them'); }
  rel(contactLen({x0:0.145-0.0425-0.0225,y0:0.001,x1:0.145-0.0425+0.0225,y1:0.046,imm:false},{x0:0.145-0.0425,y0:0,x1:0.145+0.0425,y1:BEAKER_H*0.743,imm:true}),
      R('L straddling the wall'),1e-14,'a block straddling the glass: the wetted perimeter less the dry side (python)');
  { const X=freshBench(); const b=X.bodies[1]; b.y=BURNER_TOP; b.x=burnerX(0)+0.035; ok(burnerContact(0,b),'3.5 cm off the burner’s centre a body still sits on it (PhET: centre within ±3.75 cm)');
    b.x=burnerX(0)+0.04; ok(!burnerContact(0,b),'4 cm off, it does not'); b.x=burnerX(0); b.y=BURNER_TOP+0.002; ok(!burnerContact(0,b),'2 mm above the burner, no contact (PhET’s 1-mm tolerance)'); }
  { const S={}, st=Object.assign({},DEFAULTS,{src:'teapot',conv:'generator',user:'fan',heat:1}); sysReset(S,st);
    for(let k=0;k<1200;k++) sysStep(S,st); rel(S.kettle,R('S10 kettle store when the burner goes off (J)'),1e-11,'S10: the kettle when the burner goes off (python)');
    st.heat=0; let tcut=null; for(let k=0;k<4800;k++){ sysStep(S,st); if(tcut===null&&S.kettle===0) tcut=S.t; }
    rel(tcut,R('S10 time the 30-W cut empties the kettle (s)'),1e-12,'S10: PhET’s 30-W cut empties the kettle at 74.4 s (python)');
    rel(S.sink.room,R('S10 room at 100 s (J)'),1e-11,'S10: the room (python)'); rel(S.sink.wind,R('S10 wind at 100 s (J)'),1e-11,'S10: the wind (python)');
    ok(Math.abs(sysClosure(S))<1e-8,'S10: the cut empties the kettle into the room, on the ledger'); }
  { const S={}, st=Object.assign({},DEFAULTS,{src:'faucet',conv:'generator',user:'fan',flow:1}); sysReset(S,st);
    for(let k=0;k<120;k++) sysStep(S,st); rel(S.fan,R('S9 fan omega at 2 s (rad/s)'),1e-12,'the fan mid-spin-up at 2 s, limited by PhET’s 4π rad/s² (python)');
    const f0=S.flights.length?S.flights[0].s:null; sysMoveFlights(S,DT); if(f0!==null) close(S.flights[0].s-f0,0.04/60,1e-15,'a chunk moves PhET’s 4 cm/s: 0.667 mm a step, absolute'); else ok(false,'sentinel: a chunk is in flight');
    /* swapping the CONVERTER out empties the wheel too */
    const w=S.wheel, r0=S.sink.room; ok(w>1000,'sentinel: the wheel holds '+fmt(w,0)+' J');
    sysSelect(S,st,'conv','panel'); rel(S.sink.room-r0,w,1e-12,'swapping the generator out sends its wheel’s store to the room'); eq(S.wheel,0,'and empties it');
    ok(Math.abs(sysClosure(S))<1e-8,'the ledger closes across the converter swap'); }
  { const S={}, st=Object.assign({},DEFAULTS,{src:'faucet',conv:'generator',user:'incandescent',flow:1}); sysReset(S,st);
    for(let k=0;k<600;k++) sysStep(S,st); sysSelect(S,st,'user','heater'); for(let k=0;k<30;k++) sysStep(S,st);
    rel(S.hp,R('S11 heater proportion 0.5 s after the swap'),1e-12,'switched into a running chain the heater ramps at PhET’s 0.5/s (python)');
    close(S.hp,0.25,1e-12,'0.25 after half a second, absolute'); rel(S.water-S.water0,R('S11 water above start 0.5 s after the swap (J)'),1e-10,'...and the water it has warmed (python)'); }
  { const X=freshBench(); benchGrab(X,2,SPOTS[4],0.05); benchMoveHeld(X,-0.4,0.05); const b=X.bodies[2];
    eq(b.x,BENCH_XLIM[0],'a held beaker stops at the bench’s left end');
    rel(contactLen(AIR_AREA,bodyArea(b)),2*b.w+2*b.h*b.f,1e-14,'and the room still wraps its whole perimeter there (PhET’s air box holds the bench)'); }
  { const K={}; benchReset(K); benchPlace(K,1,0); K.bodies[0].E=K.bodies[0].m*K.bodies[0].c*500;
    K.own=K.bodies.map(b=>nChunks(b.E)); K.own0=K.own.slice(); K.E0=K.bodies.map(b=>b.E);
    const ck=chunkChecker('K'); runBench(K,[0,0],3600,ck);
    eq(K.corr.excess,R('K corrections excess'),'K: the correction sheds chunks (a hot iron losing on two links) (python)');
    eq(K.corr.deficit,R('K corrections deficit'),'K: and takes them (python)'); ok(K.corr.excess>0&&K.corr.deficit>0,'K: both branches of the correction run');
    for(let i=0;i<4;i++){ rel(K.bodies[i].E,R('K E '+NAMES[i]+' (J)'),1e-11,'K: E of the '+NAMES[i]+' (python)'); eq(K.own[i],R('K own '+NAMES[i]),'K: chunks of the '+NAMES[i]+' (python)'); }
    ok(ck.st.id<1e-12,'K: the chunk identity holds through every correction'); ok(ck.st.dev<1,'K: |own - g| < 1 always');
    rel(K.room,R('K room (J)'),1e-10,'K: the room (python)'); }
  { const [a,b]=eqBodies('iron-water',380,296,'phet'); for(let k=0;k<1800;k++) eqStepOnce([a,b],false);
    rel(bodyT(a)-bodyT(b),R('insulated 30 s: T iron - T water (K)'),1e-6,'30 s insulated: the exchange stops within PhET’s 1e-6 K (python)');
    ok(bodyT(a)-bodyT(b)>0&&bodyT(a)-bodyT(b)<=EQ_THRESH,'and the gap is frozen just under the threshold'); }

  /* ---------- D. burner rules, drops, thermometers ---------- */
  { const X=freshBench(); benchPlace(X,0,2); const b=X.bodies[0]; b.E=(b.m*b.c)*T_FREEZE;
    while(bodyT(b)>T_FREEZE) b.E-=1e-10;
    ok(bodyT(b)<=T_FREEZE,'sentinel: the iron sits at 0 C, not a hair above');
    const e00=b.E; benchStep(X,[1,0]);
    rel(b.E-e00,(T_AIR-T_FREEZE)*0.18*K_AIR/60,1e-9,'at 0 C a burner adds nothing (PhET’s T > 273.15 gate): only the room’s 2.06 J a step goes in');
    const e1=b.E; benchStep(X,[1,0]); rel(b.E-e1,P_BURN/60-(bodyT(b)-T_AIR)*0.18*K_AIR/60,1e-3,'then the burner’s 83.3 J a step goes in');
    const Y=freshBench(); benchPlace(Y,0,2); benchPlace(Y,1,2);
    const e0=Y.bodies[1].E, i0=Y.bodies[0].E; benchStep(Y,[1,0]); benchStep(Y,[1,0]);
    ok(Y.bodies[1].E>e0&&Y.bodies[1].E-e0<1,'a block on a block on the burner gets no burner power, only its neighbour’s heat ('+fmt(Y.bodies[1].E-e0,3)+' J)');
    ok(Y.bodies[0].E-i0>160,'while the block on the burner takes 83.3 J a step');
    const Z=freshBench(); benchStep(Z,[0.5,0]); rel(Z.room,P_BURN_AIR*0.5/60,1e-12,'an empty burner works on the room at 1500 x level W'); }
  { const X=freshBench();
    eq(spotOrder(0.1).join(','),'4,3,5,2,1,0','drop order: the nearest spot first');
    ok(benchPlace(X,0,4),'a block drops into a beaker'); eq(X.bodies[0].y,0.001,'1 mm above the beaker’s bottom');
    ok(!benchPlace(X,3,4),'a beaker refuses to go on (or in) a beaker'); eq(chainOf(X,3).join(','),'5,0','and stays where it was');
    ok(benchPlace(X,2,1),'the water beaker (with the iron in it) moves onto the brick'); eq(X.chains[1].join(','),'1,2,0','and carries the iron with it');
    close(X.bodies[0].y,X.bodies[2].y+0.001,1e-15,'the iron keeps its place inside');
    benchGrab(X,1,X.bodies[1].x,0.02); eq(X.held.group.join(','),'1,2,0','grabbing the brick lifts everything on it');
    benchMoveHeld(X,0.05,0.1); const k=benchDrop(X); eq(k,3,'dropped at x = 0.05 it lands on the right burner');
    close(X.bodies[1].y,BURNER_TOP,1e-15,'on the burner’s top'); close(X.bodies[2].y,BURNER_TOP+BLOCK,1e-15,'the beaker on the brick');
    const Y=freshBench(); benchGrab(Y,3,SPOTS[5],0.05); benchMoveHeld(Y,0.15,0.05); eq(benchDrop(Y),5,'the oil beaker, dropped over the water, goes to the nearest spot that takes it');
    const Y2=freshBench(); benchGrab(Y2,3,SPOTS[5],0.05); benchMoveHeld(Y2,0.14,0.05); eq(benchDrop(Y2),3,'dropped a little left of the water, onto the right burner');
    eq(benchPick(freshBench(),SPOTS[0],0.02),0,'a click on the iron picks the iron'); eq(benchPick(freshBench(),SPOTS[4],0.02),2,'on the water, the water');
    eq(benchPick(freshBench(),0,0.2),-1,'on empty air, nothing'); }
  { const X=freshBench(), lev=[0.6,-0.3];
    rel(thermoSense(X,SPOTS[0],0.02,lev).T,T_ROOM,1e-12,'a thermometer in the iron reads 296 K'); eq(thermoSense(X,SPOTS[0],0.02,lev).what,0,'and names the iron');
    eq(thermoSense(X,SPOTS[4],0.02,lev).what,2,'in the water, the water'); eq(thermoSense(X,SPOTS[4],0.07,lev).what,'air','above the liquid, the room');
    rel(thermoSense(X,burnerX(0),0.06,lev).T,T_ROOM+60,1e-12,'in a flame at 0.6: 356 K (PhET: 296 + 100 x level)');
    rel(thermoSense(X,burnerX(1),0.06,[0,-0.2]).T,T_ROOM-20,1e-12,'in the ice at -0.2: 276 K');
    eq(thermoSense(X,burnerX(1),0.06,lev).T,T_FREEZE,'at -0.3 PhET clamps the ice at 273.15 K (296 - 30 would be 266)');
    const D2=freshBench(); benchPlace(D2,2,2); runBench(D2,[1,0],1200,null);
    const sp=steamProp(D2.bodies[2]); ok(sp===1,'the boiling water steams fully');
    const top=D2.bodies[2].y+D2.bodies[2].h*D2.bodies[2].f, sT=thermoSense(D2,SPOTS[2],top+0.01,[1,0]);
    ok(sT.what==='steam2'&&sT.T<T_BOIL.water&&sT.T>T_ROOM,'a thermometer in the steam reads between 296 K and boiling ('+fmt(sT.T,2)+' K)');
    rel(sT.T,linearMap(0,2*BEAKER_H,T_BOIL.water,T_ROOM,0.01),1e-12,'PhET’s steam profile: linear from the surface to 2h');
    const Y=freshBench(); Y.therm[0].tray=false; Y.therm[0].x=SPOTS[4]; Y.therm[0].y=0.02; eq(thermoDrop(Y,0),2,'a thermometer dropped in the water sticks to it');
    benchPlace(Y,2,1); const p=thermoTip(Y,Y.therm[0]); close(p.x,SPOTS[1],1e-15,'and follows the beaker when it moves');
    Y.therm[1].tray=false; Y.therm[1].x=TRAY.x0+0.02; Y.therm[1].y=TRAY.y0+0.01; eq(thermoDrop(Y,1),'tray','a thermometer dropped on the tray goes home'); }

  /* ---------- E. the chunk rule, on the presets ---------- */
  for(const P of BENCH_PRESETS){
    const X={}, st=Object.assign({},DEFAULTS); benchPreset(X,st,P.id);
    const ck=chunkChecker(P.id); const r=runBench(X,burnerLevels(st),1500,ck);
    ok(r.worst<=8*EPS,'preset '+P.id+': the ledger closes each step'); ok(ck.st.dev<1,'preset '+P.id+': |own - g| < 1 always ('+fmt(ck.st.dev,4)+')');
    ok(ck.st.id<1e-12,'preset '+P.id+': the chunk identity holds'); ok(ck.st.min>=1,'preset '+P.id+': no body is ever emptied of chunks');
    let fl=0; for(const f of X.flights) if(!(f.t>=0&&f.t<f.dur)) fl++; eq(fl,0,'preset '+P.id+': every chunk in flight is mid-flight');
  }
  { const X={}, st=Object.assign({},DEFAULTS); benchPreset(X,st,'hot');
    runBench(X,[0,0],180,null); rel(bodyT(X.bodies[0]),R('hot preset T iron at 3 s'),1e-11,'the hot-iron preset at 3 s (python)'); rel(bodyT(X.bodies[2]),R('hot preset T water at 3 s'),1e-11,'...the water (python)');
    const ck=chunkChecker('hot'); runBench(X,[0,0],3420,ck);
    rel(bodyT(X.bodies[0]),R('hot preset T iron at 60 s'),1e-10,'the hot-iron preset at 60 s (python)'); rel(bodyT(X.bodies[2]),R('hot preset T water at 60 s'),1e-10,'...the water (python)');
    eq(X.own[0],R('hot preset own iron at 60 s'),'...the iron’s chunks (python)'); eq(X.own[2],R('hot preset own water at 60 s'),'...the water’s chunks (python)');
    ok(X.moved.pair>0,'chunks moved from the iron into the water along their contact ('+X.moved.pair+')'); }
  { const X=freshBench(); benchPlace(X,0,2); let t300=null;
    while(X.t<40){ benchStep(X,[1,0]); if(t300===null&&bodyT(X.bodies[0])>=573.15) t300=X.t; }
    rel(t300,R('the iron on a full burner passes 300 C at (s)'),1e-12,'the prose’s “about twenty seconds” to 300 C is 21.08 s (python)'); }

  /* ---------- F. equilibrium: PhET's steps against the exact solution ---------- */
  for(const P of EQ_PAIRS) for(const mats of ['phet','real']){
    const tag='eqrun '+P.id+' '+mats+' air', L=eqLinear(P.id,380,296,mats,true), win=eqWindow(L), Rr=eqRun(P.id,380,296,mats,true,win);
    rel(win,R(tag+' window (s)'),1e-12,tag+': the window (python)'); eq(Rr.t.length-1,R(tag+' steps'),tag+': steps (python)');
    rel(L.G,R(tag+' G (W/K)'),1e-14,tag+': contact conductance (python)'); close(L.a1,R(tag+' a1 (W/K)'),1e-14,tag+': the block’s room conductance (python)');
    rel(L.a2,R(tag+' a2 (W/K)'),1e-14,tag+': the partner’s room conductance (python)');
    const n=Rr.t.length-1;
    rel(Rr.s1[n],R(tag+' T1 stepped end'),1e-12,tag+': stepped T1 at the end (python)'); rel(Rr.s2[n],R(tag+' T2 stepped end'),1e-12,tag+': stepped T2 (python)');
    rel(Rr.x1[n],R(tag+' T1 exact end'),1e-11,tag+': exact T1 (scipy expm)'); rel(Rr.x2[n],R(tag+' T2 exact end'),1e-11,tag+': exact T2 (scipy expm)');
    let dmax=0; for(let k=0;k<=n;k++){ dmax=Math.max(dmax,Math.abs(Rr.s1[k]-Rr.x1[k]),Math.abs(Rr.s2[k]-Rr.x2[k])); }
    rel(dmax,R(tag+' max gap (K)'),1e-7,tag+': the largest step-vs-exact gap (python)');
    eq(Rr.tCap===null?0:1,R(tag+' capped'),tag+': no cap reached (python)');
    ok(Math.abs(Rr.resid)<1e-8,tag+': energy conserved in the run ('+resid(Rr.resid)+')');
    const tg='eq '+P.id+' '+(mats==='real'?'real':'PhET');
    rel(L.C1,R(tg+' C1 (J/K)'),1e-12,tag+': C1 (python)'); rel(L.C2,R(tg+' C2 (J/K)'),1e-12,tag+': C2 (python)');
    rel(L.tau,R(tg+' tau (s)'),1e-12,tag+': tau (python)');
    rel(L.Teq,R(tg+' T_eq from 380 K and 296 K'),1e-13,tag+': T_eq (python)');
  }
  { const Rr=eqRun('iron-water',380,296,'phet',false,eqWindow(eqLinear('iron-water',380,296,'phet',false))), n=Rr.t.length-1;
    rel(Rr.s1[n],R('eqrun iron-water phet insulated T1 stepped end'),1e-12,'insulated: stepped T1 (python)'); rel(Rr.x1[n],R('eqrun iron-water phet insulated T1 exact end'),1e-11,'insulated: exact T1 (python)');
    ok(Math.abs(Rr.resid)<1e-9,'insulated: the pair keeps its energy ('+resid(Rr.resid)+')');
    const L=Rr.L, m=(L.C1*Rr.s1[n]+L.C2*Rr.s2[n])/(L.C1+L.C2); rel(m,L.Teq,1e-13,'insulated: the C-weighted mean stays at T_eq'); }
  { const L=eqLinear('iron-water',400,296,'phet',false);
    rel(L.Teq,R('J T_eq iron 400 K in water 296 K (K)'),1e-13,'T_eq, iron at 400 K into water (python)'); rel(L.tau,R('J tau (s)'),1e-13,'tau = 1.2675 s (python)');
    for(const t of [1,2,10]){ const x=eqExact(L,t); rel(x[0],R('J exact no air T iron at '+t+' s'),1e-12,'exact insulated iron at '+t+' s (python)'); rel(x[1],R('J exact no air T water at '+t+' s'),1e-12,'exact insulated water at '+t+' s (python)'); }
    const La=eqLinear('iron-water',400,296,'phet',true);
    for(const t of [1,5,30,120]){ const x=eqExact(La,t); rel(x[0],R('J exact air T iron at '+t+' s'),1e-11,'exact with the room, iron at '+t+' s (scipy)'); rel(x[1],R('J exact air T water at '+t+' s'),1e-11,'...water (scipy)'); }
    const ev=eqEigen(La.M); rel(ev[0],R('J eigenvalue slow (1/s)'),1e-10,'the slow rate (numpy)'); rel(ev[1],R('J eigenvalue fast (1/s)'),1e-12,'the fast rate (numpy)');
    /* the closed-form exponential satisfies its own ODE: d/dt e^{Mt} = M e^{Mt} */
    const h=1e-5, t=2.3, Ep=expm2(La.M,t+h), Em=expm2(La.M,t-h), E0=expm2(La.M,t);
    for(let i=0;i<2;i++) for(let j=0;j<2;j++){ const d=(Ep[i][j]-Em[i][j])/(2*h), me=La.M[i][0]*E0[0][j]+La.M[i][1]*E0[1][j]; close(d,me,1e-8,'expm2 obeys d/dt e^{Mt} = M e^{Mt} ['+i+j+']'); }
    const I0=expm2(La.M,0); ok(I0[0][0]===1&&I0[1][1]===1&&I0[0][1]===0&&I0[1][0]===0,'expm2 at t = 0 is the identity');
    const lam=1-L.G*(1/L.C1+1/L.C2)*DT; rel(lam,R('J discrete factor per step'),1e-13,'PhET’s per-step factor 1 - G(1/C1 + 1/C2)Δt (python)');
    rel(Math.exp(-DT/L.tau),R('J exact factor per step'),1e-13,'the exact per-step factor e^{-Δt/τ} (python)');
    ok(lam<Math.exp(-DT/L.tau),'PhET’s explicit step decays slightly faster than the exact exponential (O(Δt²) per step)'); }
  { let worst=0, ratio=0;
    for(const P of EQ_PAIRS) for(const mats of ['phet','real']) for(const air of [true,false]){
      const L=eqLinear(P.id,620,273.15,mats,air), Rr=eqRun(P.id,620,273.15,mats,air,eqWindow(L));
      let d=0; for(let k=0;k<Rr.t.length;k++){ if(Rr.tCap!==null&&Rr.t[k]>=Rr.tCap) break; d=Math.max(d,Math.abs(Rr.s1[k]-Rr.x1[k]),Math.abs(Rr.s2[k]-Rr.x2[k])); }
      worst=Math.max(worst,d); ratio=Math.max(ratio,d/(620-273.15)); }
    rel(worst,R('eqrun worst gap over every pair at 620 K / 273.15 K (K)'),1e-7,'the largest gap anywhere (python)');
    ok(ratio<0.004,'the prose’s “under 0.4 % of the starting difference” ('+fmt(100*ratio,3)+' %)');
    const Rc=eqRun('iron-water',620,296,'phet',true,eqWindow(eqLinear('iron-water',620,296,'phet',true)));
    rel(Rc.tCap,R('eqrun iron-water phet 620 into 296 cap time (s)'),1e-12,'a 620-K iron boils the water at 2.35 s (python)'); }
  rel(MAT_REAL.iron.c,R('real c iron (J/kg/K) from JANAF'),1e-14,'real iron c from JANAF over 55.845 (python)');
  rel(MAT_REAL.water.c*MAT_REAL.water.rho/(MAT_PHET.water.c*MAT_PHET.water.rho),R('real water C / PhET water C'),1e-14,'real water’s C is 1.39x PhET’s (python)');
  rel(MAT_REAL.brick.rho/MAT_PHET.brick.rho,R('real brick mass / PhET brick mass'),1e-14,'the real brick is 0.576 of PhET’s mass (python)');

  /* ---------- G. the Systems ledger, chain by chain ---------- */
  function sysRun(src,conv,user,n,ctl){
    const S={}, st=Object.assign({},DEFAULTS,{src,conv,user,pedal:0,flow:0,clouds:0,heat:0},ctl||{});
    sysReset(S,st); let worst=0;
    for(let k=0;k<n;k++){ sysStep(S,st); worst=Math.max(worst,Math.abs(sysClosure(S))/sysInputTotal(S)); }
    return {S,st,worst};
  }
  const sysCheckAll=(tag,o)=>{
    const S=o.S, b=sysBalance(S);
    for(const k of ['main','sun','gas']){ const key=tag+' input '+k+' (J)'; if(key in REF) rel(S.inp[k],R(key),1e-11,tag+': input '+k+' (python)'); else eq(S.inp[k],0,tag+': no '+k); }
    for(const k of ['light','wind','room','reflected','escaped']) rel(S.sink[k],R(tag+' sink '+k+' (J)'),1e-11,tag+': sink '+k+' (python)');
    rel(S.food,R(tag+' store food (J)'),1e-12,tag+': the food store (python)');
    rel(S.fall.reduce((a,c)=>a+c,0),R(tag+' store fall (J)'),1e-12,tag+': the falling water (python)');
    rel(S.kettle,R(tag+' store kettle (J)'),1e-11,tag+': the kettle (python)'); rel(S.wheel,R(tag+' store wheel (J)'),1e-11,tag+': the wheel (python)');
    rel(S.water-S.water0,R(tag+' store water above start (J)'),1e-10,tag+': the heater’s water (python)');
    rel(b.IN,R(tag+' balance IN (J)'),1e-11,tag+': IN (python)'); rel(b.OUT,R(tag+' balance OUT (J)'),1e-11,tag+': OUT (python)');
    rel(b.LOST,R(tag+' balance LOST (J)'),1e-11,tag+': LOST (python)'); rel(b.STORED,R(tag+' balance STORED (J)'),1e-10,tag+': STORED (python)');
    ok(Math.abs(b.resid)<=1e-12*Math.max(1,b.IN),tag+': IN = OUT + LOST + STORED ('+resid(b.resid)+')');
    ok(o.worst<1e-13,tag+': the global ledger closes at every step ('+o.worst.toExponential(2)+')');
    ok(S.worstEl<=4*EPS,tag+': every element closes its own ledger at every step ('+S.worstEl.toExponential(2)+')');
    eq(foodChunks(S),R(tag+' food chunks shown'),tag+': food chunks shown (python)');
    for(const c of CHANNELS){ const k=c[0], key=tag+' channel '+k+' sum (J)';
      if(key in REF){ rel(S.chsum[k],R(key),1e-11,tag+': channel '+k+' energy (python)'); eq(S.count[k],R(tag+' channel '+k+' chunks'),tag+': channel '+k+' chunks = floor(E/EPC) (python)'); }
      else eq(S.chsum[k],0,tag+': channel '+k+' idle');
      rel(S.count[k]*EPC+S.acc[k],S.chsum[k]||0,1e-12,tag+': channel '+k+': EPC x chunks + remainder = its energy');
      ok(S.acc[k]>=0&&S.acc[k]<EPC,tag+': channel '+k+' remainder within one chunk'); }
  };
  { const o=sysRun('faucet','generator','heater',1800,{flow:1}); sysCheckAll('S1',o); rel(o.S.hp,R('S1 heater proportion'),1e-10,'S1: the heater’s heat settles at 0.69 (python)'); }
  sysCheckAll('S2',sysRun('sun','panel','incandescent',600,{clouds:0.5}));
  { const o=sysRun('teapot','generator','fan',2400,{heat:1}); sysCheckAll('S3',o); rel(o.S.fan,R('S3 fan omega (rad/s)'),1e-10,'S3: the fan’s speed (python)'); }
  { const o=sysRun('biker','generator','fluorescent',1200,{pedal:1}); sysCheckAll('S4',o); eq(o.S.omega,R('S4 crank omega (rad/s)'),'S4: the rider has stopped (python)'); }
  sysCheckAll('S5',sysRun('biker','panel','incandescent',600,{pedal:1}));
  sysCheckAll('S6',sysRun('sun','generator','fan',300,{}));
  { const o=sysRun('biker','generator','heater',3600,{pedal:1}); sysCheckAll('S7',o);
    rel(o.S.water/HB_C,R('S7 water T (K)'),1e-12,'S7: the heater’s water after the food ran out (python)');
    const S2={}, st2=Object.assign({},DEFAULTS,{src:'biker',conv:'generator',user:'heater',pedal:1}); sysReset(S2,st2); let te=null;
    for(let k=0;k<3600;k++){ sysStep(S2,st2); if(te===null&&S2.food<=0) te=S2.t; }
    rel(te,R('S7 time the food runs out (s)'),1e-12,'the prose’s “about 13.5 seconds” of food (python)'); }
  { const o=sysRun('teapot','generator','incandescent',3600,{heat:0.3}); sysCheckAll('S8',o);
    rel(o.S.kettle/TAU_K,R('S8 steam power now (W)'),1e-10,'S8: the steam approaches 0.8 x 3 kW (python)'); }
  { const o=sysRun('faucet','generator','fan',600,{flow:1}), S=o.S, st=o.st;
    rel(S.wheel,R('S9 wheel store at 10 s (J)'),1e-11,'S9: the wheel’s store after 10 s (python)'); rel(S.fall.reduce((a,c)=>a+c,0),R('S9 fall store at 10 s (J)'),1e-12,'S9: 0.4 s of water falling = 4 kJ (python)');
    st.flow=0; for(let k=0;k<600;k++) sysStep(S,st);
    rel(S.wheel,R('S9 wheel store at 20 s (J)'),1e-9,'S9: the wheel runs down (python)'); eq(S.fall.reduce((a,c)=>a+c,0),0,'S9: the last water has landed');
    rel(S.sink.wind,R('S9 wind (J)'),1e-11,'S9: the wind, including what the stores sent on after the tap closed (python)');
    ok(Math.abs(sysClosure(S))<1e-8,'S9: the ledger closes through the run-down'); }
  /* the constants PhET's numbers imply, pinned */
  rel(ETA_W,R('ETA_W generator on water or steam (PhET at 60 fps)'),1e-15,'the wheel’s efficiency (python)'); rel(ETA_W,13/(6*Math.PI),1e-15,'= 13/(6 pi)');
  rel(R('PhET generator out/in at 60 fps, 5 kW'),ETA_W,1e-14,'PhET’s own wheel at 60 frames/s is the remake’s ETA_W (python)');
  rel(R('PhET generator out/in at 30 fps, 5 kW'),2*ETA_W,1e-14,'at 30 frames/s PhET’s wheel puts out 1.38x its input: the header’s claim (python)');
  rel(FAN_HEAT,R('FAN_HEAT used (1/14)'),1e-15,'the fan’s heat fraction'); close(R('PhET fan thermal chunk fraction at 10000 W'),FAN_HEAT,5e-4,'= PhET’s counter at full power (python)');
  eq(R('PhET fan thermal chunk fraction at 1000 W'),0,'PhET’s fan sends no chunk to heat at 1 kW (python): the counter is rate-dependent');
  for(const c of [0,0.25,0.5,0.99,1]) rel(sunFrac(c),R('sun fraction through clouds '+c),1e-15,'the sun through clouds '+c+' (python)');
  eq(R('PhET teapot steady steam / burner power below the cap'),2,'PhET’s teapot makes steam at twice its burner’s power (python)');
  rel(HB_L,R('heater beaker L to air (m)'),1e-15,'the heater beaker’s perimeter (python)');
  /* swapping keeps the ledger: stores go to the room, the rider is refed */
  { const S={}, st=Object.assign({},DEFAULTS,{src:'faucet',conv:'generator',user:'heater',flow:1}); sysReset(S,st);
    for(let k=0;k<300;k++) sysStep(S,st);
    const w=S.wheel, f=S.fall.reduce((a,c)=>a+c,0), wa=S.water-S.water0; ok(w>0&&f>0&&wa>0,'sentinel: the stores are full before the swap');
    const r0=S.sink.room; sysSelect(S,st,'src','teapot'); rel(S.sink.room-r0,w+f,1e-12,'swapping the faucet out empties the falling water and the wheel into the room');
    eq(st.flow,0,'and zeroes the faucet (PhET resets a swapped-out source)'); ok(Math.abs(sysClosure(S))<1e-8,'the ledger still closes');
    const r1=S.sink.room; sysSelect(S,st,'user','fan'); rel(S.sink.room-r1,wa,1e-12,'swapping the heater out empties its warm water into the room');
    sysSelect(S,st,'src','biker'); st.pedal=1; for(let k=0;k<2400;k++) sysStep(S,st);
    eq(S.food,0,'sentinel: the rider has eaten everything'); ok(sysFeed(S),'feed me refills him'); rel(S.food,FOOD0,1e-15,'to 21 chunks'); rel(S.inp.fed,FOOD0,1e-12,'logged as food eaten');
    ok(!sysFeed(S),'a full rider cannot be fed'); ok(Math.abs(sysClosure(S))<1e-8,'the ledger closes across feeding');
    sysSelect(S,st,'src','sun'); for(let k=0;k<60;k++) sysStep(S,st); sysSelect(S,st,'src','biker');
    rel(S.food,FOOD0,1e-15,'coming back, the rider is refed (PhET resets him)'); ok(Math.abs(sysClosure(S))<1e-8,'still closed');
    eq(sysSelect(S,st,'src','biker'),false,'selecting the same source changes nothing'); }
  { const S={}, st=Object.assign({},DEFAULTS,{src:'biker',conv:'generator',user:'heater',pedal:1}); sysReset(S,st);
    for(let k=0;k<3600;k++){ sysStep(S,st); const shown=foodChunks(S), burnt=S.count['b.chem']; if(shown!==FOOD_CHUNKS-burnt){ ok(false,'food shown = 21 - chemical chunks sent, at step '+k); break; } }
    ok(true,'food shown = 21 - chemical chunks sent, at every step'); }

  /* ---------- H. the scene: the bench's pointer ---------- */
  { resetAllState(); ST.view='bench';
    const cv={getContext:()=>makeShot(1400,820)}, Sc=makeScene(cv); Sc.W=1400; Sc.H=820; Sc.draw();
    const map=Sc.geo.map, B=BENCH;
    const kn=leverPos(0,0);
    ok(Sc.pointer('down',map.X(kn.x),map.Y(kn.y)),'pointer-down on the left lever grabs it'); eq(DRAG.what,'lever','the lever is in hand');
    Sc.pointer('move',map.X(kn.x),map.Y(0.03+0.02*0.5)); close(ST.lev0,0.5,1e-9,'dragging it up sets heat 0.5'); Sc.pointer('up',0,0); eq(DRAG.what,null,'released');
    close(leverPos(0,1).y-leverPos(0,-1).y,0.04,1e-15,'the lever’s track is 4 cm, absolute'); close(leverPos(0,1).y,0.05,1e-15,'and tops out below the flames at 5 cm');
    ST.link=true; const k1=leverPos(1,burnerLevels(ST)[1]);
    ok(Sc.pointer('down',map.X(k1.x),map.Y(k1.y)),'linked: the right lever, now at 0.5, is grabbed'); Sc.pointer('move',map.X(k1.x),map.Y(0.03-0.02*0.4));
    close(ST.lev0,-0.4,1e-9,'linked: the right lever drives the left'); close(burnerLevels(ST)[1],-0.4,1e-9,'and itself'); Sc.pointer('up',0,0); ST.link=false; ST.lev0=0; ST.lev1=0;
    Sc.draw();
    ok(Sc.pointer('down',map.X(SPOTS[0]+0.01),map.Y(0.02)),'pointer-down on the iron grabs it'); eq(DRAG.what,'body','a body is in hand');
    Sc.pointer('move',map.X(burnerX(0)),map.Y(0.15)); close(B.bodies[0].x,burnerX(0)-0.01,0.002,'the iron follows the pointer, keeping its grab offset');
    Sc.pointer('up',0,0); eq(chainOf(B,0)[0],2,'dropped over the left burner it lands on it'); close(B.bodies[0].y,BURNER_TOP,1e-15,'on its top');
    Sc.draw(); const tp=thermoTip(B,B.therm[0]);
    ok(Sc.pointer('down',map.X(tp.x),map.Y(tp.y+0.02)),'pointer-down on a thermometer in the tray grabs it'); eq(DRAG.what,'therm','a thermometer is in hand');
    Sc.pointer('move',map.X(SPOTS[4]),map.Y(0.04)); Sc.pointer('up',0,0);
    eq(B.therm[0].att&&B.therm[0].att.i,2,'dropped in the water it sticks to the water'); ok(!B.therm[0].tray,'and is out of the tray');
    ST.view='sys'; ok(!Sc.pointer('down',400,400),'the systems view ignores the pointer'); ST.view='ledger'; ok(!Sc.pointer('down',400,400),'so does the ledger');
    resetAllState(); }

  /* ---------- I. panels build clean for every view and preset ---------- */
  const badTxt=/NaN|undefined|Infinity|\[object/;
  function withState(over,fn){
    resetAllState(); const clean={}; for(const k in over) if(k[0]!=='_') clean[k]=over[k];
    Object.assign(ST,clean);
    if(over._preset) benchPreset(BENCH,ST,over._preset);
    if(over._bench) for(let k=0;k<over._bench;k++) benchStep(BENCH,burnerLevels(ST));
    if(over._therm){ const th=BENCH.therm[0]; th.tray=false; th.x=SPOTS[0]; th.y=0.02; thermoDrop(BENCH,0); const t2=BENCH.therm[1]; t2.tray=false; t2.x=0.0; t2.y=0.2; thermoDrop(BENCH,1); }
    if(over._sys){ sysReset(SYS,ST); for(let k=0;k<over._sys;k++) sysStep(SYS,ST); }
    try{ return fn(); } finally{ resetAllState(); }
  }
  const CONFIGS=[
    ['bench start',{view:'bench'}],['bench heat',{view:'bench',_preset:'heat',_bench:900,_therm:1}],['bench hot',{view:'bench',_preset:'hot',_bench:40}],
    ['bench stack cool',{view:'bench',_preset:'stack',_bench:1200}],['bench boil',{view:'bench',_preset:'boil',_bench:1500,_therm:1}],['bench no symbols',{view:'bench',symBench:false,_preset:'heat',_bench:300}],
    ['sys faucet',{view:'sys',_sys:600}],['sys biker',{view:'sys',src:'biker',pedal:1,_sys:400}],['sys biker empty',{view:'sys',src:'biker',pedal:1,_sys:1200}],
    ['sys sun panel',{view:'sys',src:'sun',conv:'panel',user:'incandescent',clouds:0.55,_sys:500}],['sys sun on generator',{view:'sys',src:'sun',user:'fan',_sys:300}],
    ['sys teapot fan',{view:'sys',src:'teapot',heat:1,user:'fan',_sys:1200}],['sys teapot panel',{view:'sys',src:'teapot',heat:0.6,conv:'panel',user:'fluorescent',_sys:600}],
    ['sys faucet fluor',{view:'sys',user:'fluorescent',_sys:900}],['sys no symbols',{view:'sys',symSys:false,_sys:200}],
    ['ledger idle',{view:'ledger'}],['ledger heat',{view:'ledger',_preset:'heat',_bench:1500}],['ledger hot',{view:'ledger',_preset:'hot',_bench:900}],['ledger stack',{view:'ledger',_preset:'stack',_bench:1800}],
    ['flow faucet',{view:'flow',_sys:900}],['flow idle',{view:'flow',flow:0,_sys:10}],['flow biker',{view:'flow',src:'biker',pedal:0.8,_sys:500}],['flow sun',{view:'flow',src:'sun',conv:'panel',user:'incandescent',clouds:0.3,_sys:400}],
    ['flow teapot',{view:'flow',src:'teapot',heat:1,user:'fan',_sys:900}],['flow miss',{view:'flow',src:'sun',_sys:200}],
    ['eq default',{view:'eq'}],['eq insulated real',{view:'eq',eqAir:false,eqMat:'real'}],['eq hot boil',{view:'eq',eqT1:620,eqT2:296}],['eq brick on iron',{view:'eq',eqPair:'brick-iron'}],
    ['eq water on iron',{view:'eq',eqPair:'water-iron',eqT1:500}],['eq oil cold',{view:'eq',eqPair:'iron-oil',eqT1:273.15,eqT2:373.15}],
  ];
  for(const [nm,over] of CONFIGS) withState(over,()=>{
    const M=buildModel(); let html='';
    try{ html=readoutHTML(M)+eqbarHTML(M)+tagHTML(M); }catch(e){ ok(false,nm+': the panels build ('+e+')'); return; }
    ok(!badTxt.test(html),nm+': readout, equation bar and tag are clean'+(badTxt.test(html)?' ('+html.match(badTxt)[0]+')':''));
    ok(html.length>200,nm+': the readout has substance');
  });
  withState({view:'bench',_preset:'heat',_bench:600},()=>{ const h=readoutHTML(buildModel()); ok(h.indexOf('5.00 kW into the iron')>=0,'the bench readout prints the burner’s 5.00 kW into the iron'); });
  withState({view:'sys',_sys:600},()=>{ const h=readoutHTML(buildModel()); ok(h.indexOf('7.00 kW')>=0,'the systems readout prints the faucet’s 7.00 kW'); });
  withState({view:'eq'},()=>{ const h=readoutHTML(buildModel()); ok(h.indexOf(fmt(R('eq iron-water PhET T_eq from 380 K and 296 K'),2)+' K')>=0,'the equilibrium readout prints T_eq = 320.08 K (python)'); });

  /* ---------- J. no slider setting produces a non-finite model ---------- */
  { let bad=null;
    for(const l0 of [-1,-0.37,0,0.61,1]) for(const l1 of [-1,0,1]){ const X=freshBench(); benchPlace(X,2,2); benchPlace(X,0,3);
      for(let k=0;k<400;k++) benchStep(X,[l0,l1]); for(const b of X.bodies) if(!isFinite(b.E)||!isFinite(bodyT(b))) bad='bench '+l0+','+l1; }
    for(const src of ['biker','faucet','sun','teapot']) for(const conv of ['generator','panel']) for(const user of ['heater','incandescent','fluorescent','fan'])
      for(const v of [0,0.33,1]){ const S={}, st=Object.assign({},DEFAULTS,{src,conv,user,pedal:v,flow:v,clouds:v,heat:v}); sysReset(S,st);
        for(let k=0;k<240;k++) sysStep(S,st); const b=sysBalance(S);
        if(!isFinite(b.IN)||!isFinite(b.resid)||!isFinite(S.water)) bad=src+'/'+conv+'/'+user+' '+v;
        if(Math.abs(b.resid)>1e-11*Math.max(1,b.IN)) bad='ledger '+src+'/'+conv+'/'+user+' '+v; }
    for(const P of EQ_PAIRS) for(const T1 of [273.15,400,620]) for(const T2 of [273.15,373.15]) for(const mats of ['phet','real']) for(const air of [true,false]){
      const L=eqLinear(P.id,T1,T2,mats,air), x=eqExact(L,3); if(!isFinite(x[0])||!isFinite(x[1])||!isFinite(eqWindow(L))) bad='eq '+P.id; }
    ok(!bad,'every bench lever pair, all 32 chains at three settings, every pair: finite, and each chain’s ledger closes'+(bad?' ('+bad+')':'')); }

  /* ---------- K. the layout sweep ---------- */
  const SIZES=[[1400,820],[1100,700],[820,520],[560,380]];
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over] of CONFIGS) for(const [W,H] of SIZES) withState(over,()=>{
    const c=makeShot(W,H); let err=null;
    try{ drawView(c,W,H,viewModel()); }catch(e){ err=e; }
    ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
    if(err) return;
    const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
    const strokes=c.ops.filter(o=>o.op==='stroke').length;
    ok(fills.length+strokes>=6&&texts.length>=1,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, '+strokes+' strokes)');
    let bad=null;
    for(const t of texts){
      if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
      if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
      if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; } }
    ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
    /* the house #hint (HTML, bottom:11px, 11px type) owns the bottom-left corner */
    const inHint=texts.filter(t=>t.bb[0]<340&&t.bb[3]>H-27);
    ok(!inHint.length,nm+' '+W+'x'+H+' no canvas text under the #hint line'+(inHint.length?' ("'+inHint[0].t.slice(0,30)+'" to y '+fmt(inHint[0].bb[3],0)+')':''));
    let hit=null;
    for(let i2=0;i2<texts.length&&!hit;i2++) for(let j2=i2+1;j2<texts.length;j2++){
      const a=texts[i2].bb,b=texts[j2].bb; const ox=Math.min(a[2],b[2])-Math.max(a[0],b[0]), oy=Math.min(a[3],b[3])-Math.max(a[1],b[1]);
      if(ox>0.5&&oy>0.5){ hit='"'+texts[i2].t.slice(0,22)+'" vs "'+texts[j2].t.slice(0,22)+'"'; break; } }
    ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
    let leg=null;
    for(const r of LEGEND_RECTS) for(let i2=0;i2<POLY_SEGS.length;i2+=4){
      const x0=POLY_SEGS[i2],y0=POLY_SEGS[i2+1],x1=POLY_SEGS[i2+2],y1=POLY_SEGS[i2+3];
      if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
      leg='a curve crosses the legend'; break; }
    ok(!leg,nm+' '+W+'x'+H+' legend clear');
  });

  Object.assign(ST,stSave); resetAllState(); ST.view=stSave.view;
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
