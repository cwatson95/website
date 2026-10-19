
/* ================================================================== *
 *  state, the per-view model, the readout, the equation bar, the tag  *
 * ================================================================== */
const TABS=[['pool','the pool'],['shapes','the shapes'],['press','the press'],
            ['mystery','the mystery'],['paradox','the paradox'],['column','the column']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0',
           dim:'#8b93a6', off:'#161c2c', edge:'#242a3a', gold:'#d9b44a',
           fluid:'#163a55', fluid2:'#1e4f73', wall:'#39405a', wall2:'#4b5472',
           air:'#0b1020', mass:'#6b7285'};
const RO_W=300;
const HINT_H=18;   /* the house #hint (HTML, bottom:11px) owns the bottom-left corner */

const UNIT_LIST=[{id:'metric',name:'kPa'},{id:'atmosphere',name:'atm'},{id:'english',name:'psi'}];
const FLUID_TICKS=[{id:'gasoline',name:'gasoline',rho:RHO_GASOLINE},
                   {id:'water',name:'water',rho:RHO_WATER},
                   {id:'honey',name:'honey',rho:RHO_HONEY}];
const G_TICKS=[{id:'mars',name:'Mars',g:G_MARS},
               {id:'earth',name:'Earth',g:G_EARTH},
               {id:'jupiter',name:'Jupiter',g:G_JUPITER}];
const MY_MODE_LIST=[{id:'fluid',name:'mystery fluid'},{id:'planet',name:'mystery planet'}];
const MY_PICK_LIST=[{id:'0',name:'A'},{id:'1',name:'B'},{id:'2',name:'C'}];
const VESSEL_LIST=VESSELS.map(v=>({id:v.id,name:v.name}));

const DEFAULTS={
  view:'pool',
  /* the fluid and the world (PhET's defaults: water, Earth, atmosphere on) */
  rho:RHO_WATER, grav:G_EARTH, atmosphere:true, units:'metric',
  gridOn:false, rulerOn:false,
  /* the faucet and the drain: the fraction of the pool's volume that is full.
     PhET's PoolWithFaucetsModel starts at volume 1.5 of 3, i.e. half. */
  volFrac:0.5,
  /* the two gauges, in world metres */
  gAx:3.1, gAy:-2.4, gBx:5.2, gBy:-2.4,
  /* the mass platform (PhET's one 500 kg and two 250 kg) */
  m500:true, m250a:false, m250b:false,
  /* the mystery scene */
  myMode:'fluid', myWhich:0, myGuess:'0', myReveal:false, myDepth:1.5,
  /* the paradox */
  parDepth:2.0, parPick:'flared',
  /* the column */
  colDepth:1.5, colAll:true,
};
const ST=Object.assign({},DEFAULTS);

const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }
function clearAll(){ MEMO.pool=MEMO.shapes=MEMO.press=MEMO.mystery=MEMO.paradox=MEMO.column=null; }

/* the fluid the current scene actually has: the mystery scene hides it */
function sceneRho(st){ return (st.view==='mystery'&&st.myMode==='fluid')?MYSTERY_RHO[st.myWhich]:st.rho; }
function sceneG(st){ return (st.view==='mystery'&&st.myMode==='planet')?MYSTERY_G[st.myWhich]:st.grav; }
function fluidName(rho){
  for(const f of FLUID_TICKS) if(Math.abs(f.rho-rho)<1e-9) return f.name;
  return 'a fluid at '+sigf(rho,4)+' kg/m3';
}
function gName(g){
  for(const t of G_TICKS) if(Math.abs(t.g-g)<1e-9) return t.name;
  return sigf(g,3)+' m/s2';
}
function pStr(pa,st,dp){
  const u=UNITS[st.units];
  return fmt(toUnit(pa,st.units),dp===undefined?u.dp:dp)+' '+u.name;
}

/* ---------------------------------------------------- the simple pools ---
   A probe anywhere: inside the fluid it reads p_air(surface) + rho g h,
   above it reads the air, outside the vessel it reads nothing at all. */
function probeFlat(x,y,ySurf,inside,rho,g,atmosphere){
  /* ABOVE the ground the gauge reads the air, wherever it is -- PhET's
     getPressureAtCoords does exactly that (`if (y > 0) return air(y)`).  Only
     a point buried in the solid ground has no reading at all. */
  if(y>0) return {p:airP(y,g,atmosphere),wet:false,out:false,air:true,depth:0,surf:null};
  if(!inside(x,y)) return {p:0,wet:false,out:true,air:false,depth:0,surf:null};
  if(y>ySurf) return {p:airP(y,g,atmosphere),wet:false,out:false,air:true,depth:0,surf:ySurf};
  return {p:pressureAt(ySurf-y,rho,g,ySurf,atmosphere),wet:true,out:false,air:false,depth:ySurf-y,surf:ySurf};
}
function sqInside(x,y){ return x>=SQ_X0&&x<=SQ_X1&&y>=-POOL_H&&y<=0; }
function sqLevel(volFrac){ return clamp(volFrac,0,1)*POOL_H; }

function poolCommon(st,rho,g){
  const level=sqLevel(st.volFrac), ySurf=-POOL_H+level;
  const V=SQ_A*level;
  const ins=(x,y)=>sqInside(x,y);
  const A=probeFlat(st.gAx,st.gAy,ySurf,ins,rho,g,st.atmosphere);
  const B=probeFlat(st.gBx,st.gBy,ySurf,ins,rho,g,st.atmosphere);
  return {level:level,ySurf:ySurf,V:V,Vmax:SQ_VMAX,A:A,B:B,rho:rho,g:g,
          pBot:pressureAt(level,rho,g,ySurf,st.atmosphere),
          pSurf:pressureAt(0,rho,g,ySurf,st.atmosphere),
          pAir:airP(ySurf,g,st.atmosphere),
          mass:rho*V, weight:rho*g*V, Fbot:pressureAt(level,rho,g,ySurf,st.atmosphere)*SQ_A};
}
function poolModel(st){
  const key=[st.rho,st.grav,st.atmosphere,st.volFrac,st.gAx,st.gAy,st.gBx,st.gBy,st.units].join('|');
  return memo('pool',key,()=>{
    const M=poolCommon(st,st.rho,st.grav);
    M.scene='square';
    /* the same depth in the other two pools, for the cross-scene claim */
    M.depthMatch=(M.A.wet&&M.B.wet)?Math.abs(M.A.p-M.B.p):null;
    M.sameDepth=(M.A.wet&&M.B.wet&&Math.abs(M.A.depth-M.B.depth)<1e-12);
    return M;
  });
}

/* ------------------------------------------------------- the trapezoid --- */
function tzChamberVolumeAbove(which,yFrom,ySurf){
  /* the fluid in one chamber between yFrom and the surface, exactly:
     the width is linear in height, so the trapezium rule is exact. */
  if(ySurf<=yFrom) return 0;
  const f=(y)=>{ const t=y+POOL_H, e=which==='left'?tzLeft(t):tzRight(t); return e[1]-e[0]; };
  return 0.5*(f(yFrom)+f(ySurf))*(ySurf-yFrom)*DEPTH_OUT;
}
function shapesModel(st){
  const key=[st.rho,st.grav,st.atmosphere,st.volFrac,st.gAx,st.gAy,st.gBx,st.gBy,st.units].join('|');
  return memo('shapes',key,()=>{
    const rho=st.rho, g=st.grav;
    const V=clamp(st.volFrac,0,1)*TZ_VMAX, level=tzLevel(V), ySurf=-POOL_H+level;
    const A=probeFlat(st.gAx,st.gAy,ySurf,tzInside,rho,g,st.atmosphere);
    const B=probeFlat(st.gBx,st.gBy,ySurf,tzInside,rho,g,st.atmosphere);
    const t=level;
    const wl=tzLeft(t), wr=tzRight(t);
    const colA=A.wet?tzChamberVolumeAbove(st.gAx<(TZ_CTOP+TZ_SEP/2)?'left':'right',st.gAy,ySurf):0;
    const colB=B.wet?tzChamberVolumeAbove(st.gBx<(TZ_CTOP+TZ_SEP/2)?'left':'right',st.gBy,ySurf):0;
    return {scene:'trapezoid',rho:rho,g:g,V:V,Vmax:TZ_VMAX,level:level,ySurf:ySurf,
            A:A,B:B,wLeft:wl[1]-wl[0],wRight:wr[1]-wr[0],wSum:(wl[1]-wl[0])+(wr[1]-wr[0]),
            width:tzWidth(level),inChannel:level<TZ_CHAN.t1,
            colA:colA,colB:colB,
            sameDepth:(A.wet&&B.wet&&Math.abs(A.depth-B.depth)<1e-9),
            dP:(A.wet&&B.wet)?Math.abs(A.p-B.p):null,
            mass:rho*V,pBot:pressureAt(level,rho,g,ySurf,st.atmosphere),
            pAir:airP(ySurf,g,st.atmosphere)};
  });
}

/* ---------------------------------------------------------- the press --- */
function stackMass(st){
  let m=0;
  for(const o of CH_MASSES) if(st[o.id]) m+=o.m;
  return m;
}
function pressModel(st){
  const key=[st.rho,st.grav,st.atmosphere,st.m500,st.m250a,st.m250b,st.gAx,st.gAy,st.gBx,st.gBy,st.units].join('|');
  return memo('press',key,()=>{
    const rho=st.rho, g=st.grav, M=stackMass(st);
    const P=pascal(M,rho,g,st.atmosphere);
    const A=chamberPressure(st.gAx,st.gAy,P,rho,g,st.atmosphere);
    const B=chamberPressure(st.gBx,st.gBy,P,rho,g,st.atmosphere);
    /* the two routes to the same deep point, which must agree */
    const yc=-2.5;
    const viaL=airP(P.yL,g,st.atmosphere)+P.dp+rho*g*(P.yL-yc);
    const viaR=airP(P.yR,g,st.atmosphere)+rho*g*(P.yR-yc);
    return {scene:'chamber',rho:rho,g:g,M:M,P:P,A:A,B:B,
            viaL:viaL,viaR:viaR,routeResid:Math.abs(viaL-viaR),
            pFloorL:airP(P.yR,g,st.atmosphere)+rho*g*(P.yR+POOL_H),
            onMasses:CH_MASSES.filter(o=>st[o.id]),
            liftable:M*CH_RATIO, rhoEff:rhoEff(rho,st.atmosphere)};
  });
}

/* -------------------------------------------------------- the mystery --- */
function mysteryModel(st){
  const key=[st.myMode,st.myWhich,st.myGuess,st.myReveal,st.myDepth,st.rho,st.grav,st.atmosphere,st.volFrac,st.units].join('|');
  return memo('mystery',key,()=>{
    const rho=sceneRho(st), g=sceneG(st);
    const level=sqLevel(st.volFrac), ySurf=-POOL_H+level;
    const d=clamp(st.myDepth,0,level);
    const p=pressureAt(d,rho,g,ySurf,st.atmosphere);
    /* what each of PhET's three candidates would read at the same depth */
    const cands=[0,1,2].map(i=>{
      const r=st.myMode==='fluid'?MYSTERY_RHO[i]:st.rho;
      const gg=st.myMode==='fluid'?st.grav:MYSTERY_G[i];
      return {i:i,label:'ABC'[i],rho:r,g:gg,p:pressureAt(d,r,gg,ySurf,st.atmosphere)};
    });
    let sep=Infinity;
    for(let i=0;i<3;i++) for(let j=i+1;j<3;j++) sep=Math.min(sep,Math.abs(cands[i].p-cands[j].p));
    /* the readout's own resolution, in pascals */
    const u=UNITS[st.units], res=Math.pow(10,-u.dp)*u.per;
    const inv=st.myMode==='fluid'
      ? (d>0?rhoFromReading(p,g,d,ySurf,st.atmosphere):NaN)
      : gFromReading(p,rho,d,ySurf,st.atmosphere);
    const truth=st.myMode==='fluid'?MYSTERY_RHO[st.myWhich]:MYSTERY_G[st.myWhich];
    return {scene:'mystery',rho:rho,g:g,level:level,ySurf:ySurf,d:d,p:p,cands:cands,
            sep:sep,res:res,unique:sep>res,inv:inv,truth:truth,
            invResid:isFinite(inv)?Math.abs(inv-truth):NaN,
            correct:(+st.myGuess===st.myWhich),
            degenerate:(st.myMode==='fluid'&&d<=0),
            pAir:airP(ySurf,g,st.atmosphere),
            mass:rho*SQ_A*level};
  });
}

/* -------------------------------------------------------- the paradox --- */
function paradoxModel(st){
  const key=[st.rho,st.grav,st.parDepth,st.parPick,st.units,st.atmosphere].join('|');
  return memo('paradox',key,()=>{
    const rho=st.rho, g=st.grav, H=clamp(st.parDepth,0.2,PAR_H);
    const rows=VESSELS.map(v=>vesselStats(v,rho,g,H));
    const pick=rows.find(r=>r.id===st.parPick)||rows[0];
    const Vs=rows.map(r=>r.V);
    /* the same integral by brute force, so the closed form is checked here too */
    const brute=VESSELS.map(v=>profWallVerticalSum(v.prof,H,rho,g,20000));
    return {scene:'paradox',rho:rho,g:g,H:H,rows:rows,pick:pick,
            pBase:rho*g*H,Fbase:rows[0].Fbase,
            spread:Math.max.apply(null,Vs)/Math.min.apply(null,Vs),
            brute:brute,
            worstResid:Math.max.apply(null,rows.map((r,i)=>Math.abs(r.Fwall-brute[i])/Math.max(1,Math.abs(r.Fwall)))),
            pAirTop:airP(0,g,st.atmosphere)};
  });
}

/* --------------------------------------------------------- the column --- */
function columnModel(st){
  const key=[st.rho,st.grav,st.atmosphere,st.colDepth,st.colAll,st.units].join('|');
  return memo('column',key,()=>{
    const g=st.grav, d=clamp(st.colDepth,0,POOL_H);
    const lines=FLUID_TICKS.map(f=>({name:f.name,rho:f.rho,
      slope:f.rho*g,
      p0:airP(0,g,st.atmosphere),
      p:pressureAt(d,f.rho,g,0,st.atmosphere)}));
    const here={name:fluidName(st.rho),rho:st.rho,slope:st.rho*g,
                p:pressureAt(d,st.rho,g,0,st.atmosphere)};
    /* the depth at which the reading is exactly twice the surface value */
    const p0=airP(0,g,st.atmosphere);
    const dDouble=p0>0?p0/(st.rho*g):NaN;
    /* one atmosphere of this fluid under this gravity */
    const dAtm=PA_PER_ATM/(st.rho*g);
    return {scene:'column',g:g,d:d,lines:lines,here:here,p0:p0,
            dDouble:dDouble,dAtm:dAtm,
            dAtmWaterStd:PA_PER_ATM/(RHO_WATER*G_STD),
            psiPerAtm:PA_PER_ATM/PA_PER_PSI,
            kpaPerAtm:PA_PER_ATM/PA_PER_KPA,
            airErr:Math.abs(airP(150,G_EARTH,true)-airExact(150)),
            phetAtm:Math.abs(PA_PER_ATM*PHET_ATM_PER_PA-1),
            phetPsi:Math.abs(PA_PER_ATM*PHET_PSI_PER_PA-PA_PER_ATM/PA_PER_PSI)};
  });
}

function buildModel(st){
  st=st||ST;
  if(st.view==='pool') return poolModel(st);
  if(st.view==='shapes') return shapesModel(st);
  if(st.view==='press') return pressModel(st);
  if(st.view==='mystery') return mysteryModel(st);
  if(st.view==='paradox') return paradoxModel(st);
  return columnModel(st);
}

/* ================================================================== *
 *  readout / equation bar / stage tag                                 *
 * ================================================================== */
function row(l,v,cls){ return '<tr><td>'+l+'</td><td class="v'+(cls?' '+cls:'')+'">'+v+'</td></tr>'; }
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function kgm3(x){ return sigf(x,x>=1000?5:4)+' kg/m<sup>3</sup>'; }
function litres(V){ return fmt(1000*V,0)+' L'; }
function gaugeRow(tag,G,st){
  if(G.out) return row(tag,'buried in the ground','');
  if(!G.wet) return row(tag,pStr(G.p,st)+' (air)','ref');
  return row(tag,pStr(G.p,st),'good');
}

function readoutHTML(M,st){
  st=st||ST;
  const v=st.view, u=UNITS[st.units];
  let name='', sub='', body='', note='';
  if(v==='pool'||v==='mystery'){
    if(v==='pool'){
      name='the pool'; sub=fluidName(M.rho)+' on '+gName(M.g);
      body=hd('the gauges')
        +gaugeRow('gauge A',M.A,st)
        +row('&nbsp; depth',M.A.wet?fmt(M.A.depth,2)+' m':'&mdash;')
        +gaugeRow('gauge B',M.B,st)
        +row('&nbsp; depth',M.B.wet?fmt(M.B.depth,2)+' m':'&mdash;')
        +row('they differ by',M.depthMatch===null?'&mdash;':(M.depthMatch<1e-9?'nothing at all':pStr(M.depthMatch,st,4)),
             M.sameDepth?'good':'live')
        +hd('the fluid')
        +row('density &rho;',kgm3(M.rho),'good')
        +row('gravity g',fmt(M.g,2)+' m/s<sup>2</sup>','good')
        +row('&rho;g',fmt(M.rho*M.g/1000,3)+' kPa/m','live')
        +hd('the pool')
        +row('level',fmt(M.level,2)+' m of '+fmt(POOL_H,0))
        +row('fluid in it',litres(M.V)+' of '+litres(M.Vmax))
        +row('its mass',fmt(M.mass,0)+' kg')
        +hd('top and bottom')
        +row('at the surface',pStr(M.pSurf,st),'ref')
        +row('at the floor',pStr(M.pBot,st),'good')
        +row('&rho;gh alone',pStr(M.pBot-M.pAir,st),'live')
        +row('force on the floor',fmt(M.Fbot/1000,1)+' kN')
        +row('weight of fluid',fmt(M.weight/1000,1)+' kN','ref');
      note='<b>The gauge does not care how much fluid there is.</b> Fill the pool to the top and the reading at a fixed '
        +'depth does not move; it moves only when the surface above the gauge does. The force on the floor here is '
        +fmt(M.Fbot/1000,1)+' kN and the fluid weighs '+fmt(M.weight/1000,1)+' kN, and they differ because the floor also '
        +'carries the atmosphere pressing on the surface'+(st.atmosphere?'':' &mdash; which is switched off, so here they agree')+'.';
    } else {
      name='the mystery'; sub=(st.myMode==='fluid'?'which fluid?':'which planet?');
      body=hd('what you are given')
        +row('the gauge reads',pStr(M.p,st),'good')
        +row('at depth',fmt(M.d,2)+' m')
        +row(st.myMode==='fluid'?'gravity':'the fluid',
             st.myMode==='fluid'?fmt(st.grav,2)+' m/s<sup>2</sup>':kgm3(st.rho),'ref')
        +row('atmosphere',st.atmosphere?'on, '+pStr(M.pAir,st):'off')
        +hd('what each choice would read');
      M.cands.forEach(c=>{
        body+=row((st.myMode==='fluid'?'Fluid ':'Planet ')+c.label
                  +(st.myReveal?' &nbsp; '+(st.myMode==='fluid'?sigf(c.rho,4):sigf(c.g,3)):''),
                  pStr(c.p,st),c.i===st.myWhich&&st.myReveal?'live':'');
      });
      body+=row('closest pair',M.sep<1e-12?'identical':pStr(M.sep,st,4),M.unique?'good':'bad')
        +row('the readout resolves',pStr(M.res,st,4),'ref')
        +row('so the reading is',M.unique?'enough':'not enough',M.unique?'good':'bad')
        +hd('solving for it')
        +row(st.myMode==='fluid'?'&rho; = (p &minus; p<sub>atm</sub>)/gh':'g from p = P<sub>0</sub>g/g<sub>0</sub> + &rho;gh',
             isFinite(M.inv)?(st.myMode==='fluid'?sigf(M.inv,5)+' kg/m<sup>3</sup>':sigf(M.inv,4)+' m/s<sup>2</sup>'):'no answer at the surface',
             isFinite(M.inv)?'good':'bad')
        +row('your answer',(st.myMode==='fluid'?'Fluid ':'Planet ')+'ABC'[+st.myGuess],
             st.myReveal?(M.correct?'good':'bad'):'')
        +row('the answer',st.myReveal?(st.myMode==='fluid'?'Fluid ':'Planet ')+'ABC'[M.correct?+st.myGuess:st.myWhich]:'hidden',
             st.myReveal?'live':'');
      note=M.degenerate
        ? '<b>At the surface every fluid reads the same.</b> The gauge is at zero depth, so &rho;gh = 0 and all three '
          +'candidates read the air pressure exactly. A surface reading cannot identify a fluid, and this file says so '
          +'rather than pretending. Lower the gauge.'
        : '<b>One reading is enough &mdash; but only because everything else is known.</b> The law has three unknowns on '
          +'its right-hand side and you are given two of them, so the third comes out by division. The three candidates '
          +'are '+pStr(M.sep,st,4)+' apart at their closest, against a readout that resolves '+pStr(M.res,st,4)+'.';
    }
  } else if(v==='shapes'){
    name='the shapes'; sub=fluidName(M.rho)+', two chambers, one level';
    body=hd('the two gauges')
      +gaugeRow('gauge A (left)',M.A,st)
      +row('&nbsp; depth',M.A.wet?fmt(M.A.depth,3)+' m':'&mdash;')
      +row('&nbsp; fluid above it',M.A.wet?litres(M.colA):'&mdash;','ref')
      +gaugeRow('gauge B (right)',M.B,st)
      +row('&nbsp; depth',M.B.wet?fmt(M.B.depth,3)+' m':'&mdash;')
      +row('&nbsp; fluid above it',M.B.wet?litres(M.colB):'&mdash;','ref')
      +row('same depth?',M.sameDepth?'yes':'no',M.sameDepth?'good':'live')
      +row('readings differ by',M.dP===null?'&mdash;':(M.dP<1e-9?'nothing at all':pStr(M.dP,st,4)),
           (M.sameDepth&&M.dP!==null&&M.dP<1e-9)?'good':'live')
      +hd('the two chambers at the surface')
      +row('left is',fmt(M.wLeft,3)+' m wide','live')
      +row('right is',fmt(M.wRight,3)+' m wide','live')
      +row('they sum to',fmt(M.wSum,6)+' m','good')
      +hd('the pool')
      +row('level',fmt(M.level,3)+' m')
      +row('fluid in it',litres(M.V)+' of '+litres(M.Vmax))
      +row('cross-section',fmt(M.width,3)+' m'+(M.inChannel?' (in the floor channel)':''))
      +row('at the floor',pStr(M.pBot,st),'good');
    note='<b>The two chambers taper opposite ways and their widths add to a constant '+fmt(M.wSum,3)+' m.</b> That is why '
      +'the level rises uniformly with the volume above the floor channel, and it is why the two gauges cannot disagree: '
      +'the pressure is set by the depth below the free surface and by nothing else &mdash; not by the shape of the '
      +'chamber, not by how much fluid is standing above the gauge'
      +((M.A.wet&&M.B.wet&&M.colA>0&&M.colB>0)?' (here, '+fmt(Math.max(M.colA,M.colB)/Math.max(1e-9,Math.min(M.colA,M.colB)),2)
        +' times as much on one side as the other)':'')+'.';
  } else if(v==='press'){
    name='the press'; sub=M.M>0?fmt(M.M,0)+' kg on the small piston':'nothing on the platform';
    body=hd('the two pistons')
      +row('small, area A<sub>1</sub>',fmt(CH_A_L,2)+' m<sup>2</sup>','ref')
      +row('large, area A<sub>2</sub>',fmt(CH_A_R,2)+' m<sup>2</sup>','ref')
      +row('A<sub>2</sub>/A<sub>1</sub>',fmt(CH_RATIO,3),'good')
      +hd('the load')
      +row('mass on it',fmt(M.M,0)+' kg')
      +row('its weight F<sub>1</sub>',fmt(M.P.Fin/1000,3)+' kN','bad')
      +row('&Delta;p = F<sub>1</sub>/A<sub>1</sub>',pStr(M.P.dp,st,4),'good')
      +row('F<sub>2</sub> = &Delta;p A<sub>2</sub>',fmt(M.P.Fout/1000,3)+' kN','good')
      +row('it would hold',fmt(M.liftable,0)+' kg','live')
      +hd('the two surfaces')
      +row('small side falls',fmt(M.P.dL,4)+' m','bad')
      +row('large side rises',fmt(M.P.dR,4)+' m','good')
      +row('they separate by',fmt(M.P.dh,4)+' m','live')
      +row('M/(&rho;<sub>eff</sub>A<sub>1</sub>)',fmt(M.M/(M.rhoEff*CH_A_L),4)+' m','ref')
      +row('&rho;<sub>eff</sub>',kgm3(M.rhoEff),st.atmosphere?'ref':'good')
      +hd('the gauges')
      +gaugeRow('gauge A',M.A,st)
      +gaugeRow('gauge B',M.B,st)
      +row('p at y = &minus;2.5, two ways',M.routeResid<1e-6?'agree':'differ',M.routeResid<1e-6?'good':'bad')
      +row('&nbsp; residual',M.routeResid.toExponential(1)+' Pa');
    note=M.P.capped
      ? '<b>The small column has reached the foot of its shaft.</b> Beyond this the two-column picture stops applying and '
        +'the numbers are capped, not solved. Take a mass off, or choose a denser fluid.'
      : '<b>Pascal&rsquo;s principle is one sentence.</b> A pressure applied anywhere in an enclosed fluid appears '
        +'everywhere in it. Put '+fmt(M.M,0)+' kg on '+fmt(CH_A_L,2)+' m<sup>2</sup> and you add '+pStr(M.P.dp,st,4)
        +' to every point of the fluid; the same pressure on the large piston is '+fmt(CH_RATIO,2)+' times the force. '
        +'What you do not get for free is distance: the small side falls '+fmt(CH_RATIO,2)+' times as far as the large '
        +'side rises, so the work is the same both ways.';
  } else if(v==='paradox'){
    name='the paradox'; sub=fluidName(M.rho)+', depth '+fmt(M.H,2)+' m';
    body=hd('every base, the same force')
      +row('depth h',fmt(M.H,2)+' m')
      +row('p at the base',pStr(M.pBase,st),'good')
      +row('base area',fmt(VESSELS[0].prof[0][1]*DEPTH_OUT,2)+' m<sup>2</sup>')
      +row('force on every base',fmt(M.Fbase/1000,2)+' kN','good')
      +hd('what each one holds');
    M.rows.forEach(r=>{
      body+=row(r.name,fmt(1000*r.V,0)+' L &nbsp; '+fmt(r.ratio,3),r.id===st.parPick?'live':'');
    });
    body+=row('heaviest / lightest',fmt(M.spread,3),'ref')
      +hd(M.pick.name+', in full')
      +row('volume',litres(M.pick.V))
      +row('weight W',fmt(M.pick.W/1000,2)+' kN','ref')
      +row('force on the base',fmt(M.pick.Fbase/1000,2)+' kN','good')
      +row('F/W',fmt(M.pick.ratio,4),'live')
      +row('walls push up by',fmt(M.pick.Fwall/1000,2)+' kN','good')
      +row('W &minus; F<sub>base</sub>',fmt((M.pick.W-M.pick.Fbase)/1000,2)+' kN','ref')
      +row('they differ by',M.pick.resid<1e-6?'nothing':M.pick.resid.toExponential(1)+' N',
           M.pick.resid<1e-6?'good':'bad')
      +row('vs a 20000-strip sum',M.worstResid.toExponential(1));
    note='<b>The force on the base is not the weight of the fluid.</b> It is p times the area, and p is &rho;gh whatever '
      +'the vessel looks like. The difference is carried by the slanted walls: they push '
      +(M.pick.Fwall>=0?'UP on the fluid where the vessel widens with height':'DOWN on the fluid where it narrows')
      +', by exactly W &minus; F<sub>base</sub>. This view computes that wall force by integrating the pressure over the '
      +'walls, without using the force balance, so the agreement is a check and not a definition.';
  } else {
    name='the column'; sub=fluidName(M.here.rho)+' on '+gName(M.g);
    body=hd('the line')
      +row('intercept p<sub>atm</sub>',pStr(M.p0,st),'ref')
      +row('slope &rho;g',fmt(M.here.slope/1000,4)+' kPa/m','good')
      +row('&nbsp; in atm',sigf(M.here.slope/PA_PER_ATM,4)+' atm/m')
      +row('&nbsp; in psi',sigf(M.here.slope/PA_PER_PSI,4)+' psi/m')
      +row('at h = '+fmt(M.d,2)+' m',pStr(M.here.p,st),'live')
      +hd('the same number, three ways')
      +row('kPa',fmt(toUnit(M.here.p,'metric'),3),'good')
      +row('atm',fmt(toUnit(M.here.p,'atmosphere'),5),'good')
      +row('psi',fmt(toUnit(M.here.p,'english'),4),'good')
      +hd('the exact definitions')
      +row('1 atm',fmt(PA_PER_ATM,0)+' Pa','ref')
      +row('1 psi',fmt(PA_PER_PSI,6)+' Pa','ref')
      +row('1 atm in psi',fmt(M.psiPerAtm,8),'ref')
      +row('PhET&rsquo;s atm is off by',M.phetAtm.toExponential(2)+' atm')
      +row('PhET&rsquo;s psi is off by',M.phetPsi.toExponential(2)+' psi')
      +hd('depths worth knowing')
      +row('one atmosphere of this',fmt(M.dAtm,3)+' m','good')
      +row('&nbsp; water at g<sub>n</sub>',fmt(M.dAtmWaterStd,4)+' m','ref')
      +row('the reading doubles at',isFinite(M.dDouble)?fmt(M.dDouble,3)+' m':'never (no atmosphere)','live');
    note='<b>The whole sim is one straight line.</b> Pressure against depth has intercept p<sub>atm</sub> and slope '
      +'&rho;g, and every control in this file moves exactly one of those two. Changing the units does not move the line '
      +'at all &mdash; it relabels the axis, which is why the three scales are drawn on the same picture.';
  }
  return '<div class="rname">'+name+'<small>'+sub+'</small></div><table>'+body+'</table><div class="note">'+note+'</div>';
}

function eqbarHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='pool') return '<span class="lhs">p</span> = <span class="hl">p<sub>atm</sub> + &rho; g h</span>'
    +' &nbsp;&nbsp; at h = '+fmt(M.level,2)+' m &nbsp;&rarr;&nbsp; <span class="hl2">'+pStr(M.pBot,st)+'</span>'
    +'<span class="sm">the depth below the free surface is the only geometry in it</span>';
  if(v==='shapes') return '<span class="lhs">p<sub>left</sub>(h)</span> = <span class="hl">p<sub>right</sub>(h)</span>'
    +' &nbsp;&nbsp; w<sub>left</sub> + w<sub>right</sub> = <span class="hl2">'+fmt(M.wSum,3)+' m</span> at every height'
    +'<span class="sm">two chambers that taper opposite ways, one level, one pressure at one depth</span>';
  if(v==='press') return '<span class="lhs">&Delta;p</span> = <span class="hl">F<sub>1</sub>/A<sub>1</sub> = F<sub>2</sub>/A<sub>2</sub></span>'
    +' &nbsp;&rarr;&nbsp; F<sub>2</sub> = <span class="hl2">'+fmt(CH_RATIO,2)+' F<sub>1</sub></span> = '+fmt(M.P.Fout/1000,2)+' kN'
    +'<span class="sm">Pascal: the added pressure reaches every point, so the force scales with the area it acts on</span>';
  if(v==='mystery') return '<span class="lhs">'+(st.myMode==='fluid'?'&rho;':'g')+'</span> = <span class="hl">'
    +(st.myMode==='fluid'?'(p &minus; p<sub>atm</sub>) / g h':'p / (P<sub>0</sub>/g<sub>0</sub> + &rho;h)')+'</span>'
    +' &nbsp;&rarr;&nbsp; <span class="hl2">'+(isFinite(M.inv)?sigf(M.inv,5):'no answer at h = 0')+'</span>'
    +'<span class="sm">one reading, everything else known, and the unknown comes out by division</span>';
  if(v==='paradox') return '<span class="lhs">F<sub>base</sub></span> = <span class="hl">&rho; g h A</span>'
    +' &ne; W &nbsp;&nbsp; F<sub>wall,z</sub> = <span class="hl2">W &minus; F<sub>base</sub></span> = '
    +fmt((M.pick.W-M.pick.Fbase)/1000,2)+' kN'
    +'<span class="sm">the base feels the depth, not the weight; the slanted walls carry the rest</span>';
  return '<span class="lhs">dp/dy</span> = <span class="hl">&minus;&rho; g</span>'
    +' &nbsp;&nbsp; 1 atm = 101325 Pa = <span class="hl2">'+fmt(M.psiPerAtm,6)+' psi</span>'
    +'<span class="sm">a straight line, and three names for the same number</span>';
}

function tagHTML(M,st){
  st=st||ST;
  const v=st.view;
  if(v==='pool') return '<b>the pool</b> &mdash; PhET&rsquo;s square pool';
  if(v==='shapes') return '<b>the shapes</b> &mdash; PhET&rsquo;s trapezoid pool';
  if(v==='press') return '<b>the press</b> &mdash; PhET&rsquo;s chamber pool';
  if(v==='mystery') return '<b>the mystery</b> &mdash; PhET&rsquo;s mystery pool';
  if(v==='paradox') return '<b>the paradox</b> &mdash; same base, same depth, different weight';
  return '<b>the column</b> &mdash; the law as a straight line';
}
