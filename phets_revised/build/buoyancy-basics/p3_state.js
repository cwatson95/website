/* ================================================================== *
 *  state, the per-view model, the readout, the equation bar, the tag  *
 * ================================================================== */
const TABS=[['explore','the pool'],['sets','the sets'],['faces','the faces'],
            ['scale','the scale'],['fluids','float or sink']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a', gold:'#d9b44a',
           fluid:'#163a55', fluid2:'#1e4f73', body:'#4a5060', body2:'#6b7285', air:'#0d1626'};
const RO_W=300;
const HINT_H=18;   /* the house #hint (HTML, bottom:11px) owns the bottom-left corner */

const MAT_LIST=SIMPLE_MATS.map(id=>({id:id,name:MAT[id].name})).concat([{id:'custom',name:'custom'}]);
const FLUID_LIST=BUOY_FLUIDS.map(id=>({id:id,name:MAT[id].name}));
const SET_LIST=[{id:'mass',name:'same mass'},{id:'volume',name:'same volume'},{id:'density',name:'same density'}];
const WHERE_LIST=[{id:'floor',name:'the pool floor'},{id:'poolscale',name:'the pool scale'},
                  {id:'ground',name:'the ground scale'}];
const GRID_LIST=MATERIALS.filter(m=>m.id!=='air').map(m=>({id:m.id,name:m.name}));

/* where things stand.  The pool scale is PhET's: 0.15 x 0.06 x 0.2 m, its
   height a fraction of the way up the pool (PhET's heightProperty, 0.5). */
const SCALE_X=0.27, GROUND_SCALE_X=-POOL_W/2-0.13;
const BLOCK_A_X=-0.22, BLOCK_B_X=0.02;

const DEFAULTS={
  view:'explore',
  /* the blocks (PhET's Explore controls) */
  two:false, matA:'wood', massA:2, volAL:5, matB:'aluminum', massB:13.5, volBL:5,
  holdA:null, holdB:null,
  /* the fluid and the furniture */
  fluid:'water', where:'floor', scaleH:0.5,
  /* the sets (Compare) */
  setMode:'mass', sameMass:BB_SAME_MASS, sameVolL:BB_SAME_VOL*LITERS, sameRho:BB_SAME_RHO,
  /* the faces */
  facesDepth:0.45,
  /* the scale view */
  lowered:0.55,
  /* float or sink */
  gridMat:'wood',
  /* overlays */
  forces:true, labels:true,
};
const ST=Object.assign({},DEFAULTS);

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function clearAll(){ MEMO.explore=MEMO.sets=MEMO.faces=MEMO.scale=MEMO.fluids=null; }

/* -------------------------------------------------- the two adjustable blocks
   PhET's coupling exactly: a real material fixes the density, so mass and
   volume move together; custom leaves them free and the density follows. */
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
    const mm=MAT[mat].phet*V/LITERS;
    if(Math.abs(mm-m)>1e-12){ if(w==='A') st.massA=mm; else st.massB=mm; }
  }
}
function setVol(st,w,V){
  const mat=w==='A'?st.matA:st.matB, custom=(mat==='custom');
  V=clamp(V,VMIN_L,VMAX_L);
  if(w==='A') st.volAL=V; else st.volBL=V;
  if(!custom) setMass(st,w,MAT[mat].phet*V/LITERS);
  else { const m=w==='A'?st.massA:st.massB, mm=clamp(m,MMIN_CUSTOM,MMAX);
    if(w==='A') st.massA=mm; else st.massB=mm; }
}
function setMat(st,w,id){
  if(w==='A') st.matA=id; else st.matB=id;
  const V=w==='A'?st.volAL:st.volBL;
  if(id==='custom'){ const m=clamp((w==='A'?st.massA:st.massB),MMIN_CUSTOM,MMAX);
    if(w==='A') st.massA=m; else st.massB=m; return; }
  setMass(st,w,MAT[id].phet*V/LITERS);
}
/* the pool scale's top, from PhET's height fraction */
function poolScaleY0(st){ return -POOL_H+st.scaleH*(POOL_H-SCALE_H); }
function poolScaleTop(st){ return poolScaleY0(st)+SCALE_H; }
function poolObstacles(st){ return [{a:SCALE_W*SCALE_D,y0:poolScaleY0(st),h:SCALE_H}]; }

function blockOf(st,w){
  const rho=rhoOf(st,w), V=(w==='A'?st.volAL:st.volBL)/LITERS, held=w==='A'?st.holdA:st.holdB;
  const onScale=(w==='A'&&st.where==='poolscale'), onGround=(w==='A'&&st.where==='ground');
  return {tag:w,V:V,rho:rho,
          x:onScale?SCALE_X:(onGround?GROUND_SCALE_X:(w==='A'?BLOCK_A_X:BLOCK_B_X)),
          mat:w==='A'?st.matA:st.matB,col:matColor(w==='A'?st.matA:st.matB,rho),
          support:onScale?poolScaleTop(st):(onGround?SCALE_H:-POOL_H),
          inPool:!onGround, yb:onGround?SCALE_H:undefined,
          held:(held===null||held===undefined)?undefined:held};
}

/* ------------------------------------------------------------ the pool view */
function exploreModel(st){
  const key=[st.two,st.matA,st.massA,st.volAL,st.matB,st.massB,st.volBL,st.holdA,st.holdB,
             st.fluid,st.where,st.scaleH].join('|');
  return memo('explore',key,()=>{
    const rhoF=MAT[st.fluid].phet, obs=poolObstacles(st);
    const blocks=[blockOf(st,'A')];
    if(st.two) blocks.push(blockOf(st,'B'));
    const sol=solvePool(blocks,rhoF,obs);
    const bare=poolLevel([],obs,rhoF,VF0);
    for(const b of sol.blocks){
      b.faces=cubeFaceForces(b.V,b.yb,sol.yw,rhoF);
      b.floats=b.rho<rhoF;
      b.pct=100*b.frac;
    }
    const A=sol.blocks[0];
    /* the two scales, in newtons, as PhET shows them */
    const poolReads=(st.where==='poolscale')?A.N:0;
    const groundReads=(st.where==='ground')?A.W:0;
    return {rhoF:rhoF,fluid:st.fluid,yw:sol.yw,bare:bare,blocks:sol.blocks,obs:obs,
            scaleTop:poolScaleTop(st),scaleY0:poolScaleY0(st),
            poolReads:poolReads,groundReads:groundReads,
            rise:sol.yw-bare,VfDisp:(sol.yw-bare)*A_POOL};
  });
}

/* ------------------------------------------------------------- the sets view */
function setsModel(st){
  const key=[st.setMode,st.sameMass,st.sameVolL,st.sameRho,st.fluid,st.scaleH].join('|');
  return memo('sets',key,()=>{
    const rhoF=MAT[st.fluid].phet, obs=poolObstacles(st);
    const raw=compareBlocks(BB_CUBES,st.setMode,st.sameMass,st.sameVolL/LITERS,st.sameRho);
    const xs=[-0.26,0.02];
    raw.forEach((b,i)=>{ b.x=xs[i]; });
    const sol=solvePool(raw,rhoF,obs);
    sol.blocks.forEach((b,i)=>{ b.tag=raw[i].tag; b.col=raw[i].col; b.floats=b.rho<rhoF; b.pct=100*b.frac; });
    const matched=st.setMode==='mass'?'mass':(st.setMode==='volume'?'volume':'density');
    /* PhET builds this screen out of a brick and a piece of wood */
    const names=sol.blocks.map(b=>{
      const hit=MATERIALS.find(m=>Math.abs(m.phet-b.rho)<1e-9);
      return hit?hit.name:'custom';
    });
    return {rhoF:rhoF,yw:sol.yw,blocks:sol.blocks,matched:matched,names:names,
            scaleTop:poolScaleTop(st),scaleY0:poolScaleY0(st),obs:obs,
            nFloat:sol.blocks.filter(b=>b.mode==='float').length};
  });
}

/* ------------------------------------------------------------ the faces view */
function facesModel(st){
  const key=[st.matA,st.massA,st.volAL,st.fluid,st.facesDepth].join('|');
  return memo('faces',key,()=>{
    const rhoF=MAT[st.fluid].phet, rho=rhoOf(st,'A'), V=st.volAL/LITERS, s=cubeSide(V);
    /* the cube's bottom, as a depth below a flat free surface at y = 0 */
    const yb=-st.facesDepth, yw=0;
    const F=cubeFaceForces(V,yb,yw,rhoF);
    const poly=cubePoly(V,yb,0), sub=clipBelow(poly,yw);
    const E=edgeForces(sub,yw,rhoF), fine=finePerimeter(sub,yw,rhoF,2000);
    const Asub=polyArea(sub), C=Asub>1e-12?polyCentroid(sub):[0,0];
    const Vsub=cubeBelow(V,yb,yw);
    return {rhoF:rhoF,rho:rho,V:V,s:s,yb:yb,yw:yw,F:F,E:E,fine:fine,Asub:Asub,C:C,
            Vsub:Vsub,arch:rhoF*G*Vsub,W:rho*V*G,
            resid:Math.abs(F.net-rhoF*G*Vsub)/Math.max(1e-12,rhoF*G*Vsub),
            resid2d:Math.abs(E.tot[1]-rhoF*G*Asub)/Math.max(1e-12,rhoF*G*Asub),
            fineResid:Math.abs(fine[1]-E.tot[1])/Math.max(1e-12,Math.abs(E.tot[1])),
            fullyUnder:yb+s<=yw};
  });
}

/* ------------------------------------------------------------ the scale view */
/* lowering a block on a spring scale: `lowered` runs 0 (clear of the surface)
   to 1 (resting on the floor).  The free surface is solved at every step, so
   the curve carries the rise of the fluid as the block goes in. */
function loweredY(st,s){
  const top=poolLevel([],[],MAT[st.fluid].phet,VF0)+0.02;
  const bot=-POOL_H;
  return top+(bot-top)*clamp(st.lowered,0,1);
}
function scaleModel(st){
  const key=[st.matA,st.massA,st.volAL,st.fluid,st.lowered].join('|');
  return memo('scale',key,()=>{
    const rhoF=MAT[st.fluid].phet, rho=rhoOf(st,'A'), V=st.volAL/LITERS, s=cubeSide(V);
    const curve=[], N=241;
    for(let i=0;i<N;i++){
      const t=i/(N-1), st2={fluid:st.fluid,lowered:t};
      const yb=loweredY(st2,s);
      const r=solvePool([{V:V,rho:rho,held:yb}],rhoF)['blocks'][0];
      const rest=(yb<=-POOL_H+1e-12);
      const hang=rest?Math.max(0,r.W-r.Fb-0):r.hand;      /* the string can only pull */
      curve.push([t,r.W-r.Fb,r.Vsub,yb]);
    }
    const yb=loweredY(st,s);
    const sol=solvePool([{V:V,rho:rho,held:yb}],rhoF);
    const b=sol.blocks[0];
    const resting=(yb<=-POOL_H+1e-12);
    /* once the block reaches the floor the string goes slack if it floats or
       the floor takes the rest; the spring reads what it still carries */
    const read=Math.max(0,b.W-b.Fb);
    return {rhoF:rhoF,rho:rho,V:V,s:s,yb:yb,yw:sol.yw,blk:b,curve:curve,
            read:read,slack:(b.W-b.Fb)<=0,resting:resting,
            W:b.W,Fb:b.Fb,Vsub:b.Vsub,frac:b.frac,
            tEnter:1-(loweredY({fluid:st.fluid,lowered:0},s)-sol.yw)/(loweredY({fluid:st.fluid,lowered:0},s)+POOL_H),
            full:apparentWeight(V,rho,rhoF)};
  });
}

/* ----------------------------------------------------- the float-or-sink view */
function fluidsModel(st){
  const key=[st.gridMat,st.matA,st.massA,st.volAL].join('|');
  return memo('fluids',key,()=>{
    const rows=MATERIALS.filter(m=>m.id!=='air').slice().sort((a,b)=>a.phet-b.phet);
    const cols=BUOY_FLUIDS.map(id=>({id:id,name:MAT[id].name,rho:MAT[id].phet}));
    const grid=rows.map(m=>cols.map(f=>({frac:submergedFraction(m.phet,f.rho),
                                         floats:m.phet<f.rho,
                                         neutral:Math.abs(m.phet-f.rho)<1e-9})));
    const pick=MAT[st.gridMat], pi=rows.findIndex(m=>m.id===st.gridMat);
    return {rows:rows,cols:cols,grid:grid,pick:pick,pi:pi,
            nFloat:grid.reduce((t,r)=>t+r.filter(c=>c.floats).length,0),
            nCells:rows.length*cols.length,
            mercuryFloats:rows.filter(m=>m.phet<MAT.mercury.phet).length,
            gasolineFloats:rows.filter(m=>m.phet<MAT.gasoline.phet).length};
  });
}

function buildModel(st){
  st=st||ST;
  if(st.view==='explore') return exploreModel(st);
  if(st.view==='sets') return setsModel(st);
  if(st.view==='faces') return facesModel(st);
  if(st.view==='scale') return scaleModel(st);
  return fluidsModel(st);
}

/* ================================================================== *
 *  readout / equation bar / stage tag                                 *
 * ================================================================== */
function row(l,v,cls){ return '<tr><td>'+l+'</td><td class="v'+(cls?' '+cls:'')+'">'+v+'</td></tr>'; }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function kgm3(x){ return sigf(x,x>=1000?5:4)+' kg/m<sup>3</sup>'; }
function pct(x){ return x<1e-9?'exact':(sigf(100*x,2)+' %'); }

function readoutHTML(M,st){
  st=st||ST;
  const v=st.view;
  let name='', sub='', body='', note='';
  if(v==='explore'){
    const A=M.blocks[0], B=M.blocks[1];
    name='the pool'; sub=MAT[st.fluid].name+(st.two?', two blocks':', one block');
    body=hd('block A — '+matName(st.matA))
      +row('mass',fmt(A.m,2)+' kg')
      +row('volume',fmt(A.V*LITERS,2)+' L')
      +row('density',kgm3(A.rho),'good')
      +row('fluid density',kgm3(M.rhoF),'ref')
      +row('state',A.mode==='float'?'floats':(A.mode==='held'?'held':(A.mode==='out'?'in air':
           (Math.abs(A.rho-M.rhoF)<1e-9?'neutral':'sinks'))),A.mode==='float'?'good':'bad')
      +row('% submerged',fmt(A.pct,1)+' %','good')
      +row('gravity W',fmt(A.W,2)+' N','bad')
      +row('buoyancy F<sub>b</sub>',fmt(A.Fb,2)+' N','good')
      +row('contact N',fmt(A.N,2)+' N','live');
    if(B) body+=hd('block B — '+matName(st.matB))
      +row('mass',fmt(B.m,2)+' kg')
      +row('density',kgm3(B.rho),'good')
      +row('% submerged',fmt(B.pct,1)+' %')
      +row('buoyancy',fmt(B.Fb,2)+' N','good');
    body+=hd('the scales, in newtons')
      +row('pool scale',st.where==='poolscale'?fmt(M.poolReads,2)+' N':'nothing on it',st.where==='poolscale'?'good':'')
      +row('ground scale',st.where==='ground'?fmt(M.groundReads,2)+' N':'nothing on it',st.where==='ground'?'good':'')
      +hd('the pool')
      +row('fluid',fmt(VF0*LITERS,0)+' L of '+MAT[st.fluid].name)
      +row('level',fmt(100*(M.yw+POOL_H),2)+' cm')
      +row('risen by',fmt(1000*M.rise,2)+' mm','good');
    note='<b>The two scales say the same thing twice.</b> In air the block weighs &rho;<sub>b</sub>gV; under the fluid it '
      +'presses down by &rho;<sub>b</sub>gV &minus; &rho;<sub>f</sub>gV<sub>sub</sub>, and the difference is the weight of '
      +'the fluid it pushed aside. PhET ignores air buoyancy (a &ldquo;vacuum assumption&rdquo;); in real air this block '
      +'would read '+sigf(100*1.2*A.V/A.m,2)+' % light.';
  } else if(v==='sets'){
    name='the sets'; sub='matched in '+M.matched+', in '+MAT[st.fluid].name;
    body=hd('the two blocks');
    M.blocks.forEach((b,i)=>{
      body+=row(b.tag+' &nbsp; '+M.names[i],sigf(b.rho,4)+(b.mode==='float'?' &uarr;':' &darr;'),b.mode==='float'?'good':'bad')
        +row('&nbsp; mass / volume',fmt(b.m,2)+' kg, '+fmt(b.V*LITERS,2)+' L')
        +row('&nbsp; % submerged',fmt(b.pct,1)+' %');
    });
    body+=hd('the matched quantity')
      +row(M.matched,st.setMode==='mass'?fmt(st.sameMass,2)+' kg':(st.setMode==='volume'?fmt(st.sameVolL,2)+' L':kgm3(st.sameRho)),'good')
      +row('floating',M.nFloat+' of 2')
      +row('level',fmt(100*(M.yw+POOL_H),2)+' cm');
    note=st.setMode==='mass'?'PhET&rsquo;s Compare screen starts with a brick and a piece of wood of the same mass, 4 kg: '
        +'2 L of brick and 10 L of wood. Same weight, and one floats.'
      :st.setMode==='volume'?'Same size, 5 L each: 10 kg of brick and 2 kg of wood. The heavy one is the dense one, and it sinks.'
      :'Same density, so the same stuff in two sizes &mdash; and they float to exactly the same fraction of themselves, '
        +fmt(100*Math.min(1,st.sameRho/M.rhoF),1)+' %, whatever the size.';
  } else if(v==='faces'){
    name='the faces'; sub=M.fullyUnder?'fully submerged':'partly submerged';
    body=hd('the pressure on the block')
      +row('depth of the bottom',fmt(100*M.F.dBot,2)+' cm')
      +row('depth of the top',fmt(100*M.F.dTop,2)+' cm')
      +row('p at the bottom',sigf(M.F.pBot,5)+' Pa','good')
      +row('p at the top',sigf(M.F.pTop,5)+' Pa','ref')
      +row('face area',fmt(M.F.A*1e4,2)+' cm<sup>2</sup>')
      +hd('the forces on the faces')
      +row('bottom pushes up',fmt(M.F.Fbot,2)+' N','good')
      +row('top pushes down',fmt(M.F.Ftop,2)+' N','bad')
      +row('net, up',fmt(M.F.net,2)+' N','good')
      +row('one side face',fmt(M.F.side,2)+' N','live')
      +row('the four sides',fmt(M.F.sideSum,2)+' N')
      +hd('Archimedes says')
      +row('&rho;<sub>f</sub> g V<sub>sub</sub>',fmt(M.arch,2)+' N','good')
      +row('they differ by',pct(M.resid))
      +hd('the same, round the polygon')
      +row('per-edge closed form',fmt(M.E.tot[1],2)+' N/m','good')
      +row('vs &rho;g&times;area',pct(M.resid2d))
      +row('vs a 2000-point sum',pct(M.fineResid))
      +row('horizontal',fmt(M.E.tot[0],2)+' N/m');
    note='<b>This is where the upthrust comes from.</b> Nothing pushes up on a submerged body except the fluid, and all the '
      +'fluid does is press on every face at &rho;<sub>f</sub>g times the depth. The four sides cancel in pairs exactly. The '
      +'bottom is deeper than the top by the block&rsquo;s own height, so it is pressed harder by &rho;<sub>f</sub>g&times;height, '
      +'and times the face area that is &rho;<sub>f</sub>gV. No approximation anywhere.';
  } else if(v==='scale'){
    name='the scale'; sub=M.resting?'resting on the floor':(M.Vsub>0?'in the fluid':'in air');
    body=hd('the block')
      +row('mass',fmt(M.blk.m,2)+' kg')
      +row('weight in air',fmt(M.W,2)+' N','bad')
      +row('volume',fmt(M.V*LITERS,2)+' L')
      +hd('now')
      +row('submerged',fmt(M.Vsub*LITERS,2)+' L of '+fmt(M.V*LITERS,2))
      +row('buoyancy',fmt(M.Fb,2)+' N','good')
      +row('the scale reads',fmt(M.read,2)+' N','live')
      +row('lost',fmt(M.W-M.read,2)+' N');
    body+=hd('once it is fully under')
      +row('it reads',fmt(Math.max(0,M.full),2)+' N','good')
      +row('and stops changing','however deep')
      +row('unless it floats',M.full<0?'this one floats — the string goes slack':'this one sinks');
    note='<b>The apparent weight falls only while the block is entering.</b> Once it is under, V<sub>sub</sub> is the whole '
      +'volume and the reading is stuck at (&rho;<sub>b</sub> &minus; &rho;<sub>f</sub>)gV, whatever the depth &mdash; '
      +'pressure grows with depth on the bottom face and on the top face by exactly the same amount. The kink in the curve '
      +'is the moment the top face goes under.';
  } else {
    name='float or sink'; sub=M.pick.name;
    body=hd(M.pick.name+' in each fluid');
    M.cols.forEach((f,j)=>{
      const c=M.grid[M.pi][j];
      body+=row(f.name+' ('+sigf(f.rho,5)+')',c.floats?fmt(100*c.frac,1)+' % under':'sinks',c.floats?'good':'bad');
    });
    body+=hd('the whole grid')
      +row('cells',M.nCells+' = '+M.rows.length+' &times; '+M.cols.length)
      +row('floating',M.nFloat,'good')
      +row('float in mercury',M.mercuryFloats+' of '+M.rows.length,'good')
      +row('float in gasoline',M.gasolineFloats+' of '+M.rows.length,'bad');
    note='<b>Floating is a comparison, not a property.</b> Lead floats in mercury and aluminium floats in mercury; nothing '
      +'PhET carries floats in gasoline except styrofoam and wood. The only thing that decides is '
      +'&rho;<sub>b</sub> &lt; &rho;<sub>f</sub>, and how far under is exactly the ratio.';
  }
  return '<div class="rname">'+name+'<small>'+sub+'</small></div><table>'+body+'</table><div class="note">'+note+'</div>';
}

function eqbarHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='explore') return '<span class="lhs">F<sub>b</sub></span> = <span class="hl">&rho;<sub>f</sub> g V<sub>sub</sub></span>'
    +' &nbsp;&nbsp; W &minus; F<sub>b</sub> &minus; N = 0 &nbsp;&rarr;&nbsp; N = <span class="hl2">'+fmt(M.blocks[0].N,2)+' N</span>'
    +'<span class="sm">the three forces PhET draws: gravity down, buoyancy up, and whatever the floor or the scale still has to take</span>';
  if(v==='sets') return '<span class="lhs">&rho;</span> = <span class="hl">m / V</span>'
    +' &nbsp;&nbsp; matched '+M.matched+' &nbsp;&rarr;&nbsp; <span class="hl2">'+M.nFloat+' of 2 float</span>'
    +'<span class="sm">a brick and a piece of wood, held equal in one quantity at a time</span>';
  if(v==='faces') return '<span class="lhs">(p<sub>bot</sub> &minus; p<sub>top</sub>) A</span> = '
    +'<span class="hl">&rho;<sub>f</sub> g (y<sub>t</sub> &minus; y<sub>b</sub>) A</span> = '
    +'<span class="hl2">&rho;<sub>f</sub> g V<sub>sub</sub></span> = '+fmt(M.F.net,2)+' N'
    +'<span class="sm">the upthrust is not a new force &mdash; it is the pressure difference between the bottom face and the top</span>';
  if(v==='scale') return '<span class="lhs">scale</span> = <span class="hl">W &minus; &rho;<sub>f</sub> g V<sub>sub</sub></span>'
    +' = <span class="hl2">'+fmt(M.read,2)+' N</span>'
    +'<span class="sm">the apparent weight falls while the block enters and then stops, because V<sub>sub</sub> stops growing</span>';
  return '<span class="lhs">V<sub>sub</sub>/V</span> = <span class="hl">min(1, &rho;<sub>b</sub>/&rho;<sub>f</sub>)</span>'
    +' &nbsp;&nbsp; floats &hArr; <span class="hl2">&rho;<sub>b</sub> &lt; &rho;<sub>f</sub></span>'
    +'<span class="sm">every material against every fluid PhET carries, at once</span>';
}

function tagHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='explore') return '<b>the pool</b> &mdash; PhET&rsquo;s Explore screen';
  if(v==='sets') return '<b>the sets</b> &mdash; PhET&rsquo;s Compare screen';
  if(v==='faces') return '<b>the faces</b> &mdash; where the upthrust comes from';
  if(v==='scale') return '<b>the scale</b> &mdash; the apparent weight, all the way down';
  return '<b>float or sink</b> &mdash; every material in every fluid';
}
