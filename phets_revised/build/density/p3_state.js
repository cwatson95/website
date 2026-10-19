/* ================================================================== *
 *  state, the per-view model, the readout, the equation bar, the tag  *
 * ================================================================== */
const TABS=[['pool','the pool'],['sets','the sets'],['mystery','the mystery'],
            ['mv','mass and volume'],['line','the waterline']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a', gold:'#d9b44a',
           fluid:'#163a55', fluid2:'#1e4f73', body:'#4a5060', body2:'#6b7285', air:'#0d1626'};
const RO_W=300;
const HINT_H=18;   /* the house #hint (HTML, bottom:11px) owns the bottom-left corner */

const MAT_LIST=SIMPLE_MATS.map(id=>({id:id,name:MAT[id].name})).concat([{id:'custom',name:'custom'}]);
const SET_LIST=[{id:'mass',name:'same mass'},{id:'volume',name:'same volume'},{id:'density',name:'same density'}];
const MSET_LIST=MYSTERY_LIST.map(n=>({id:n,name:n}));
const PICK_LIST=['A','B','C','D','E'].map(t=>({id:t,name:t}));
const MVMAT_LIST=MATERIALS.filter(m=>m.id!=='air').map(m=>({id:m.id,name:m.name}));
const FLUID_LIST=BUOY_FLUIDS.map(id=>({id:id,name:MAT[id].name}));

const DEFAULTS={
  view:'pool',
  /* the pool (PhET's Intro screen) */
  two:false, matA:'wood', massA:2, volAL:5, matB:'aluminum', massB:13.5, volBL:5,
  holdA:null, holdB:null,
  /* the sets (Compare) — PhET's own defaults, taken from the constants rather
     than retyped, so a mutation of either moves both (Known-bad: a number
     written in two places is two numbers and only one gets mutated) */
  setMode:'mass', sameMass:DENS_SAME_MASS, sameVolL:DENS_SAME_VOL*LITERS, sameRho:DENS_SAME_RHO,
  /* the mystery */
  mset:'set 1', seed:1, reveal:false, mpick:'A', submerge:true,
  /* mass and volume */
  mvMat:'wood', showRef:true,
  /* the waterline */
  lineFluid:'water',
  /* shared overlays */
  forces:true, levels:true,
};
const ST=Object.assign({},DEFAULTS);

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* -------------------------------------------------- the two adjustable blocks
   PhET's coupling exactly: with a real material the density is fixed, so mass
   and volume move together; the custom material leaves them free and the
   density follows, rho = m/V. */
function rhoOf(st,w){
  const mat=w==='A'?st.matA:st.matB;
  if(mat!=='custom') return MAT[mat].phet;
  const m=w==='A'?st.massA:st.massB, V=(w==='A'?st.volAL:st.volBL)/LITERS;
  return m/V;
}
function setMass(st,w,m){
  const mat=w==='A'?st.matA:st.matB, custom=(mat==='custom');
  const rng=massRangeFor(custom?0:MAT[mat].phet,custom);
  m=clamp(m,rng[0],rng[1]);
  if(w==='A') st.massA=m; else st.massB=m;
  if(!custom){
    const V=clamp(m/MAT[mat].phet*LITERS,VMIN_L,VMAX_L);
    if(w==='A') st.volAL=V; else st.volBL=V;
    /* if the volume clipped, the mass has to follow it back */
    const mm=MAT[mat].phet*V/LITERS;
    if(Math.abs(mm-m)>1e-12){ if(w==='A') st.massA=mm; else st.massB=mm; }
  }
}
function setVol(st,w,V){
  const mat=w==='A'?st.matA:st.matB, custom=(mat==='custom');
  V=clamp(V,VMIN_L,VMAX_L);
  if(w==='A') st.volAL=V; else st.volBL=V;
  if(!custom) setMass(st,w,MAT[mat].phet*V/LITERS);
  else { /* rho follows; keep the mass inside its own range */
    const m=w==='A'?st.massA:st.massB;
    const mm=clamp(m,MMIN_CUSTOM,MMAX);
    if(w==='A') st.massA=mm; else st.massB=mm;
  }
}
/* switching material keeps the VOLUME and rebuilds the mass (PhET keeps the
   cube's size and re-densities it); if that mass leaves 0.1-27 kg the volume
   gives way instead */
function setMat(st,w,id){
  if(w==='A') st.matA=id; else st.matB=id;
  const V=w==='A'?st.volAL:st.volBL;
  if(id==='custom'){ const m=clamp((w==='A'?st.massA:st.massB),MMIN_CUSTOM,MMAX);
    if(w==='A') st.massA=m; else st.massB=m; return; }
  setMass(st,w,MAT[id].phet*V/LITERS);
}
function blockOf(st,w,x){
  const rho=rhoOf(st,w), V=(w==='A'?st.volAL:st.volBL)/LITERS, held=w==='A'?st.holdA:st.holdB;
  return {tag:w,V:V,rho:rho,x:x,mat:w==='A'?st.matA:st.matB,
          col:matColor(w==='A'?st.matA:st.matB,rho),held:(held===null?undefined:held)};
}

/* ------------------------------------------------------------- the pool view */
const RHO_WATER=1000;      /* Density runs on water only — PhET's 'justWater' */
function poolModel(st){
  const key=[st.two,st.matA,st.massA,st.volAL,st.matB,st.massB,st.volBL,st.holdA,st.holdB].join('|');
  return memo('pool',key,()=>{
    const blocks=[blockOf(st,'A',-0.22)];
    if(st.two) blocks.push(blockOf(st,'B',0.22));
    const sol=solvePool(blocks,RHO_WATER);
    const bare=poolLevel([],[],RHO_WATER,VF0);
    for(const b of sol.blocks){
      b.faces=cubeFaceForces(b.V,b.yb,sol.yw,RHO_WATER);
      b.floats=b.rho<RHO_WATER;
      b.draft=b.floats?floatDraft(b.V,b.rho,RHO_WATER):b.s;
      b.rise=b.mode==='float'?riseFloating(b.m,RHO_WATER):riseSunk(b.Vsub);
    }
    return {rhoF:RHO_WATER,yw:sol.yw,bare:bare,blocks:sol.blocks,
            rise:sol.yw-bare, VfDisp:(sol.yw-bare)*A_POOL};
  });
}

/* ------------------------------------------------------------- the sets view */
function setsModel(st){
  const key=[st.setMode,st.sameMass,st.sameVolL,st.sameRho].join('|');
  return memo('sets',key,()=>{
    const raw=compareBlocks(DENS_CUBES,st.setMode,st.sameMass,st.sameVolL/LITERS,st.sameRho);
    const xs=[-0.315,-0.105,0.105,0.315];
    raw.forEach((b,i)=>{ b.x=xs[i]; });
    const sol=solvePool(raw,RHO_WATER);
    sol.blocks.forEach((b,i)=>{ b.tag=raw[i].tag; b.col=raw[i].col; b.floats=b.rho<RHO_WATER; });
    /* the matched quantity, and the one the set makes vary */
    const matched=st.setMode==='mass'?'mass':(st.setMode==='volume'?'volume':'density');
    return {yw:sol.yw,blocks:sol.blocks,matched:matched,
            nFloat:sol.blocks.filter(b=>b.mode==='float').length,
            nNeutral:sol.blocks.filter(b=>Math.abs(b.rho-RHO_WATER)<1e-9).length};
  });
}

/* ---------------------------------------------------------- the mystery view */
function mysteryModel(st){
  const key=[st.mset,st.seed,st.mpick,st.reveal,st.submerge].join('|');
  return memo('mystery',key,()=>{
    const set=mysterySet(st.mset,st.seed);
    const xs=[-0.33,-0.165,0,0.165,0.33];
    set.forEach((b,i)=>{ b.x=xs[i]; });
    /* holding a block under is what makes the displaced volume the block's
       volume: left alone a floating block displaces its own WEIGHT of water,
       so the measurement returns rho_f and every floater reads as water */
    const sol=solvePool(set.map(b=>({tag:b.tag,V:b.V,rho:b.rho,x:b.x,col:b.col,
                                     held:st.submerge?-POOL_H:undefined})),RHO_WATER);
    const bare=poolLevel([],[],RHO_WATER,VF0);
    const rows=set.map((b,i)=>{
      const Vdisp=sol.blocks[i].Vsub;                       /* what the pool measures */
      const mD=disp2(b.m), VD=disp2(Vdisp*LITERS), id=identify(mD,VD);
      /* the material the block REALLY is: the table entry nearest its true
         density (PhET's set 2 A is 11340 against the table's lead 11342) */
      const truth=identify(b.rho/LITERS,1).id;
      return {tag:b.tag,V:b.V,rho:b.rho,m:b.m,col:b.col,mDisp:mD,VDisp:VD,VmeasL:VD,
              rhoRead:id.rho,guess:id.id,err:id.err,gap:id.gap,
              readErr:Math.abs(id.rho-b.rho)/b.rho, ok:(id.id===truth),
              truth:truth,mode:sol.blocks[i].mode,frac:sol.blocks[i].frac,x:b.x};
    });
    const pick=rows.find(r=>r.tag===st.mpick)||rows[0];
    return {rows:rows,pick:pick,yw:sol.yw,bare:bare,blocks:sol.blocks,
            nWrong:rows.filter(r=>!r.ok).length,
            worstErr:Math.max.apply(null,rows.map(r=>r.readErr)),
            worstGap:Math.min.apply(null,rows.map(r=>r.gap)),
            table:DENSITY_TABLE.map(k=>({id:k,name:MAT[k].name,rho:MAT[k].phet,ref:MAT[k].ref}))
                               .sort((a,b)=>a.rho-b.rho)};
  });
}

/* ------------------------------------------------- the mass-volume plane view */
function mvModel(st){
  const key=[st.mvMat,st.showRef,st.matA,st.massA,st.volAL].join('|');
  return memo('mv',key,()=>{
    const pick=MAT[st.mvMat];
    const live={m:st.massA,V:st.volAL,rho:rhoOf(st,'A')};
    /* every material that can be drawn inside the 1-10 L x 0.1-27 kg box */
    const pts=MATERIALS.filter(m=>m.id!=='air').map(m=>{
      const rng=massRangeFor(m.phet,false);
      return {id:m.id,name:m.name,rho:m.phet,ref:m.ref,note:m.note,col:m.col,
              mLo:rng[0],mHi:rng[1],inBox:m.phet*VMIN_L/LITERS<=MMAX,
              dRel:m.ref===null?null:(m.phet-m.ref)/m.ref};
    });
    const worst=pts.filter(p=>p.dRel!==null).sort((a,b)=>Math.abs(b.dRel)-Math.abs(a.dRel))[0];
    return {pick:pick,live:live,pts:pts,worst:worst,
            nRef:pts.filter(p=>p.ref!==null).length,nNo:pts.filter(p=>p.ref===null).length};
  });
}

/* --------------------------------------------------------- the waterline view */
function lineModel(st){
  const key=[st.lineFluid,st.matA,st.massA,st.volAL].join('|');
  return memo('line',key,()=>{
    const rhoF=MAT[st.lineFluid].phet, rhoB=rhoOf(st,'A'), V=st.volAL/LITERS;
    const r=rhoB/rhoF;
    const curve=[];
    for(let i=0;i<=400;i++){ const rr=3*i/400; curve.push([rr,Math.min(1,rr)]); }
    /* what every material does in this fluid */
    const rows=MATERIALS.filter(m=>m.id!=='air').map(m=>({id:m.id,name:m.name,rho:m.phet,
      r:m.phet/rhoF, frac:submergedFraction(m.phet,rhoF), floats:m.phet<rhoF, col:m.col}));
    const one=solvePool([{V:V,rho:rhoB}],rhoF);
    const b=one.blocks[0];
    return {rhoF:rhoF,rhoB:rhoB,V:V,r:r,frac:submergedFraction(rhoB,rhoF),
            draft:floatDraft(V,rhoB,rhoF),side:cubeSide(V),curve:curve,rows:rows,
            yw:one.yw,blk:b,N:b.N,app:apparentWeight(V,rhoB,rhoF,b.Vsub),
            rise:b.mode==='float'?riseFloating(b.m,rhoF):riseSunk(b.Vsub),
            neutral:Math.abs(rhoB-rhoF)<1e-9};
  });
}

function buildModel(st){
  st=st||ST;
  if(st.view==='pool') return poolModel(st);
  if(st.view==='sets') return setsModel(st);
  if(st.view==='mystery') return mysteryModel(st);
  if(st.view==='mv') return mvModel(st);
  return lineModel(st);
}

/* ================================================================== *
 *  readout / equation bar / stage tag                                 *
 * ================================================================== */
function row(l,v,cls){ return '<tr><td>'+l+'</td><td class="v'+(cls?' '+cls:'')+'">'+v+'</td></tr>'; }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function kgm3(x){ return sigf(x,x>=1000?5:4)+' kg/m<sup>3</sup>'; }
/* a relative error, said in words when it is below what any display could show */
function pct(x){ return x<1e-9?'exact':(sigf(100*x,2)+' %'); }

function readoutHTML(M,st){
  st=st||ST;
  const v=st.view;
  let name='', sub='', body='', note='';
  if(v==='pool'){
    const A=M.blocks[0], B=M.blocks[1];
    name='the pool'; sub='one block' + (st.two?'s — A and B':'');
    if(st.two) sub='two blocks, A and B';
    body=hd('block A — '+matName(st.matA))
      +row('mass',fmt(A.m,2)+' kg')
      +row('volume',fmt(A.V*LITERS,2)+' L')
      +row('density',kgm3(A.rho),'good')
      +row('cube side',fmt(A.s*100,2)+' cm')
      +row('state',A.mode==='float'?'floats':(A.mode==='held'?'held':(Math.abs(A.rho-M.rhoF)<1e-9?'neutral — rests, no push':'sinks')),A.mode==='float'?'good':'bad')
      +row('submerged',fmt(100*A.frac,1)+' %')
      +row('weight W',fmt(A.W,2)+' N')
      +row('upthrust F<sub>b</sub>',fmt(A.Fb,2)+' N','good')
      +row(A.mode==='held'?'your hand':'floor pushes',fmt(A.mode==='held'?A.hand:A.N,2)+' N',A.mode==='held'?'':'bad');
    if(B) body+=hd('block B — '+matName(st.matB))
      +row('mass',fmt(B.m,2)+' kg')
      +row('volume',fmt(B.V*LITERS,2)+' L')
      +row('density',kgm3(B.rho),'good')
      +row('state',B.mode==='float'?'floats':'sinks',B.mode==='float'?'good':'bad')
      +row('submerged',fmt(100*B.frac,1)+' %');
    body+=hd('the pool')
      +row('water',fmt(VF0*LITERS,0)+' L in '+fmt(V_POOL*LITERS,0)+' L')
      +row('level',fmt(100*(M.yw+POOL_H),2)+' cm above the floor')
      +row('risen by',fmt(1000*M.rise,2)+' mm','good')
      +row('= displaced',fmt(M.VfDisp*LITERS,2)+' L');
    note='<b>A floating block raises the level by its own mass over &rho;<sub>f</sub>A</b>, and a sunk one by its own volume over A — both exactly. '
      +'A = '+fmt(A_POOL,2)+' m<sup>2</sup>, so one litre is '+fmt(1000/A_POOL*0.001,2)+' mm.';
  } else if(v==='sets'){
    name='the sets'; sub='matched in '+M.matched;
    body=hd('the four blocks');
    for(const b of M.blocks)
      body+=row(b.tag+' &nbsp; '+fmt(b.m,2)+' kg, '+fmt(b.V*LITERS,2)+' L',
                sigf(b.rho,4)+(b.mode==='float'?' &uarr;':' &darr;'),b.mode==='float'?'good':'bad');
    body+=hd('the matched quantity')
      +row(M.matched,st.setMode==='mass'?fmt(st.sameMass,2)+' kg':(st.setMode==='volume'?fmt(st.sameVolL,2)+' L':kgm3(st.sameRho)),'good')
      +row('floating',M.nFloat+' of '+M.blocks.length)
      +row('level',fmt(100*(M.yw+POOL_H),2)+' cm');
    note=st.setMode==='mass'?'Same mass, different volume: the small ones are the dense ones. PhET&rsquo;s four volumes are 10, 5, 2.5 and 1.25 L, so at 5 kg the densities are 500, 1000, 2000 and 4000 &mdash; and the second is <b>exactly water</b>, neither floating nor pressing on the floor.'
      :st.setMode==='volume'?'Same volume, different mass: the heavy ones are the dense ones. PhET&rsquo;s four masses are 8, 6, 4 and 2 kg, so at 5 L the densities are 1600, 1200, 800 and 400.'
      :'Same density, different size: every one of them floats to the same depth, '+fmt(100*st.sameRho/RHO_WATER,1)+' % of its side, whatever its size. That is the whole content of the floating law.';
  } else if(v==='mystery'){
    const p=M.pick;
    name='the mystery'; sub=st.mset;
    body=hd('block '+p.tag+' — what the sim shows you')
      +row('scale reads',fmt(p.mDisp,2)+' kg')
      +row('water rose by',fmt(p.VmeasL,2)+' L')
      +row('&rho; = m/V',kgm3(p.rhoRead),'good')
      +hd('reading it off the table')
      +row('nearest',MAT[p.guess].name,p.ok?'good':'bad')
      +row('off by',pct(p.err),'good')
      +row('runner-up is',pct(p.gap)+' away','good');
    if(st.reveal) body+=row('really',MAT[p.truth].name+(p.ok?'':' — MISSED'),p.ok?'good':'bad');
    body+=hd('the whole set')
      +row('identified',(5-M.nWrong)+' of 5',M.nWrong?'bad':'good')
      +row('worst reading error',pct(M.worstErr))
      +row('smallest gap to 2nd',pct(M.worstGap),'good');
    note=st.submerge
      ? 'The claim that these numbers <b>identify</b> the material is asserted, not assumed: every block&rsquo;s printed mass and '
        +'displaced volume put it within '+pct(M.worstErr)+' of its own density and no closer than '+pct(M.worstGap)+' to any other '
        +'table entry. PhET&rsquo;s 2700 blocks are aluminium, but aluminium is not on the Density table &mdash; glass, also 2700, is the answer it wants.'
      : '<b>The floating blocks are lying to you.</b> A floating body pushes aside its own <i>weight</i> of water, not its own volume, '
        +'so m/V comes out at the water&rsquo;s own density however light it is. Switch &ldquo;hold them under&rdquo; back on.';
  } else if(v==='mv'){
    const p=M.pick, L=M.live;
    name='mass and volume'; sub='&rho; = m/V, one ray per material';
    body=hd(p.name)
      +row('PhET&rsquo;s value',kgm3(p.phet),'good')
      +row('handbook',p.ref===null?'no row':kgm3(p.ref),'ref')
      +row('difference',p.ref===null?'&mdash;':(p.phet>p.ref?'+':'')+sigf(100*(p.phet-p.ref)/p.ref,3)+' %',p.ref===null?'':'bad')
      +row('1 L weighs',fmt(p.phet/LITERS,3)+' kg')
      +row('10 L weighs',fmt(10*p.phet/LITERS,2)+' kg');
    body+=hd('block A, live')
      +row('mass',fmt(L.m,2)+' kg')
      +row('volume',fmt(L.V,2)+' L')
      +row('density',kgm3(L.rho),'good');
    body+=hd('the two columns')
      +row('with a handbook row',M.nRef+' of '+M.pts.length)
      +row('without one',M.nNo)
      +row('furthest apart',MAT[M.worst.id].name+', '+(M.worst.dRel>0?'+':'')+sigf(100*M.worst.dRel,3)+' %','bad');
    note='<b>Green is PhET&rsquo;s number, orange the handbook&rsquo;s.</b> Six materials &mdash; brick, pyrite, apple, human, gasoline, honey &mdash; '
      +'have no row in Wikipedia&rsquo;s table at all, and this file says so rather than inventing one. Source: Wikipedia, &ldquo;Densities of various materials&rdquo;, fetched 2026-09-21.';
  } else {
    name='the waterline'; sub=MAT[st.lineFluid].name;
    body=hd('the block, in '+MAT[st.lineFluid].name)
      +row('&rho;<sub>b</sub>',kgm3(M.rhoB),'good')
      +row('&rho;<sub>f</sub>',kgm3(M.rhoF),'ref')
      +row('ratio &rho;<sub>b</sub>/&rho;<sub>f</sub>',fmt(M.r,4),'live')
      +row('submerged',fmt(100*M.frac,2)+' %','good')
      +row(M.blk.mode==='float'?'draft':'side',fmt(100*(M.blk.mode==='float'?M.draft:M.side),2)+' cm')
      +hd('the forces')
      +row('weight',fmt(M.blk.W,2)+' N')
      +row('upthrust',fmt(M.blk.Fb,2)+' N','good')
      +row('floor pushes',fmt(M.N,2)+' N','bad')
      +row('a spring scale would read',fmt(M.app,2)+' N')
      +hd('the pool')
      +row('level rose',fmt(1000*M.rise,2)+' mm','good');
    note=M.neutral?'<b>Exactly neutral.</b> &rho;<sub>b</sub> = &rho;<sub>f</sub>, so the upthrust equals the weight at every depth: the block neither floats nor presses on the floor, and a spring scale reads zero. Nothing chooses a depth for it.'
      :(M.blk.mode==='float'?'It floats. The submerged fraction is <b>exactly</b> &rho;<sub>b</sub>/&rho;<sub>f</sub> &mdash; it does not depend on the size, the shape&rsquo;s cross-section, or gravity.'
        :'It sinks and the floor takes the rest: N = (&rho;<sub>b</sub> &minus; &rho;<sub>f</sub>)gV = '+fmt(M.N,2)+' N.');
  }
  return '<div class="rname">'+name+'<small>'+sub+'</small></div><table>'+body+'</table><div class="note">'+note+'</div>';
}

function eqbarHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='pool') return '<span class="lhs">F<sub>b</sub></span> = <span class="hl">&rho;<sub>f</sub> g V<sub>sub</sub></span>'
    +' &nbsp;&nbsp; N = W &minus; F<sub>b</sub> = <span class="hl2">'+fmt(M.blocks[0].N,2)+' N</span>'
    +'<span class="sm">Archimedes: the upthrust is the weight of the fluid the block pushes aside &mdash; nothing else</span>';
  if(v==='sets') return '<span class="lhs">&rho;</span> = <span class="hl">m / V</span>'
    +' &nbsp;&nbsp; matched '+M.matched+' &nbsp;&rarr;&nbsp; <span class="hl2">'+M.nFloat+' of '+M.blocks.length+' float</span>'
    +'<span class="sm">fix any two of mass, volume and density and the third is forced</span>';
  if(v==='mystery') return '<span class="lhs">&rho;</span> = <span class="hl">m / V</span> = '
    +fmt(M.pick.mDisp,2)+' kg / '+fmt(M.pick.VDisp,2)+' L = <span class="hl2">'+sigf(M.pick.rhoRead,5)+' kg/m<sup>3</sup></span>'
    +'<span class="sm">weigh it, drop it in, divide &mdash; and read the name off the table</span>';
  if(v==='mv') return '<span class="lhs">m</span> = <span class="hl">&rho; V</span>'
    +' &nbsp;&nbsp; a ray of slope &rho; through the origin'
    +'<span class="sm">every material is one line in the mass-volume plane; the steeper it is, the denser</span>';
  return '<span class="lhs">V<sub>sub</sub>/V</span> = <span class="hl">min(1, &rho;<sub>b</sub>/&rho;<sub>f</sub>)</span>'
    +' = <span class="hl2">'+fmt(M.frac,4)+'</span>'
    +'<span class="sm">a floating body displaces its own weight, so it sinks to exactly that fraction of itself</span>';
}

function tagHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='pool') return '<b>the pool</b> &mdash; PhET&rsquo;s Intro screen';
  if(v==='sets') return '<b>the sets</b> &mdash; PhET&rsquo;s Compare screen';
  if(v==='mystery') return '<b>the mystery</b> &mdash; PhET&rsquo;s Mystery screen, '+st.mset;
  if(v==='mv') return '<b>mass and volume</b> &mdash; &rho; = m/V made visible';
  return '<b>the waterline</b> &mdash; the floating law, exactly';
}
