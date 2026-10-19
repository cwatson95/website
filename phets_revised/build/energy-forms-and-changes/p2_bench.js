
/* ================================================================== *
 *  the bench (PhET's Intro screen): bodies, contact, the exchange     *
 *  step in PhET's order, stacks, the chunk rule, thermometers         *
 * ================================================================== */
const BODY_DEF=[['iron','block'],['brick','block'],['water','beaker'],['oil','beaker']];
function makeBody(i,mats){
  const [mat,kind]=BODY_DEF[i], M=(mats||MAT_PHET)[mat];
  const b={i,mat,kind,c:M.c,x:0,y:0,f:FLUID0};
  if(kind==='block'){ b.w=BLOCK; b.h=BLOCK; b.m=Math.pow(BLOCK,3)*M.rho; }
  else { b.w=BEAKER_W; b.h=BEAKER_H; b.m=Math.PI*Math.pow(b.w/2,2)*b.h*FLUID0*M.rho; }
  b.E=b.m*b.c*T_ROOM;
  return b;
}
function bodyT(b){ const t=b.E/(b.m*b.c); return b.kind==='beaker'?Math.min(t,T_BOIL[b.mat]):t; }
function bodyTraw(b){ return b.E/(b.m*b.c); }
function bodyMinE(b){ return T_FREEZE*b.m*b.c; }
function bodyCap(b){ return b.kind==='block'?T_BLOCK_MAX:T_BOIL[b.mat]; }
function bodyBeyond(b){ return Math.max(b.E-bodyCap(b)*b.m*b.c,0); }
function bodyBounds(b){ return {x0:b.x-b.w/2, y0:b.y, x1:b.x+b.w/2, y1:b.y+b.h, imm:false}; }
function bodyArea(b){
  if(b.kind==='block') return bodyBounds(b);
  return {x0:b.x-b.w/2, y0:b.y, x1:b.x+b.w/2, y1:b.y+b.h*b.f, imm:true};
}
/* PhET's ThermalContactArea.getThermalContactLength (a's method, b's area) */
function contactLen(a,b){
  const ox=Math.max(Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),0);
  const oy=Math.max(Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0),0);
  let n=0;
  if(ox>0&&oy>0){
    if(a.imm||b.imm){
      const rw=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0), rh=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);
      n=2*rw+2*rh;
      if(rw!==(a.x1-a.x0)&&rw!==(b.x1-b.x0)) n-=rh;
      if(rh!==(a.y1-a.y0)&&rh!==(b.y1-b.y0)) n-=rw;
    }
  } else if(ox>0||oy>0){
    /* PhET's precedence, kept: && binds tighter than || */
    if((ox>0&&Math.abs(a.y1-b.y0)<0.001)||Math.abs(a.y0-b.y1)<0.001||(oy>0&&Math.abs(a.x1-b.x0)<0.001)||Math.abs(a.x0-b.x1)<0.001) n=ox;
  }
  return n;
}
/* a.exchangeEnergyWith(b): substeps of at most 1/60 s; returns the energy that went a -> b */
function exchange(a,b,dt){
  let tot=0;
  const L=contactLen(bodyArea(a),bodyArea(b));
  if(L>0&&Math.abs(bodyT(b)-bodyT(a))>EQ_THRESH){
    const nsub=Math.floor(dt/MAXSTEP), rem=dt-nsub*MAXSTEP;
    for(let o=0;o<nsub+1;o++){
      const h=o<nsub?MAXSTEP:rem;
      const q=(bodyT(b)-bodyT(a))*L*K_BODY*h;
      b.E-=q; a.E+=q; tot+=-q;
    }
  }
  return tot;
}
/* Air.exchangeEnergyWith(b): the body's temperature held over the substeps; any
   energy past the body's cap goes too.  Returns the energy b -> the room. */
function airExchange(b,dt){
  let i=0;
  const L=contactLen(AIR_AREA,bodyArea(b));
  if(L>0){
    const nsub=Math.floor(dt/MAXSTEP), rem=dt-nsub*MAXSTEP;
    for(let o=0;o<nsub+1;o++){ const h=o<nsub?MAXSTEP:rem; i+=(bodyT(b)-T_AIR)*L*K_AIR*h; }
    if(i>=0) i=Math.max(i,bodyBeyond(b));
    b.E-=i;
  }
  return i;
}
function containsB(o,i){ return o.x0<=i.x0&&o.x1>=i.x1&&o.y0<=i.y0&&o.y1>=i.y1; }
function isImmersed(bodies,b){
  if(b.kind!=='block') return false;
  const bb=bodyBounds(b);
  for(const k of bodies) if(k!==b&&k.kind==='beaker'&&containsB(bodyArea(k),bb)) return true;
  return false;
}
/* PhET's perspective: a block is a cube 4.5 cm deep whose depth shifts by
   MAP_Z_TO_XY_OFFSET = 0.25 per unit (PERSP for half the depth).  PhET centres
   the cube on the model's rectangle; the remake draws its front face ON the
   rectangle (its beakers are flat) with the depth running up-right, and picks
   and senses with the shape it draws */
const PERSP=0.25*BLOCK/2;
function blockHex(b){
  const x0=b.x-b.w/2, x1=b.x+b.w/2, y0=b.y, y1=b.y+b.h, d=2*PERSP;
  return [[x0,y0],[x1,y0],[x1+d,y0+d],[x1+d,y1+d],[x0+d,y1+d],[x0,y1]];
}
function inPoly(pts,x,y){
  let ins=false;
  for(let i=0,j=pts.length-1;i<pts.length;j=i++){
    const xi=pts[i][0],yi=pts[i][1],xj=pts[j][0],yj=pts[j][1];
    if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi)) ins=!ins;
  }
  return ins;
}

/* ---- the live bench ---------------------------------------------------- */
const BENCH={};
const HIST_MAX=1200;
const BENCH_XLIM=[-0.29,0.29], BENCH_YMAX=0.24;
/* the thermometer tray (world, top-left) and a thermometer's drawn height */
const TRAY={x0:-0.300,y0:0.205,x1:-0.215,y1:0.285};
const THERMO_H=0.062;
function trayHome(k){ return {x:TRAY.x0+0.012+k*0.02, y:TRAY.y0+0.008}; }

function benchReset(B){
  B.bodies=[0,1,2,3].map(i=>makeBody(i));
  B.chains=[[0],[1],[],[],[2],[3]];
  B.held=null;
  benchLayout(B);
  B.room=0; B.work=0; B.workK=[0,0]; B.workAir=0; B.roomBodies=0;
  B.t=0; B.steps=0; B.acc=0;
  B.own=B.bodies.map(b=>nChunks(b.E)); B.own0=B.own.slice(); B.E0=B.bodies.map(b=>b.E);
  B.link={}; B.moved={pair:0,burner:0,air:0}; B.corr={excess:0,deficit:0}; B.maxdev=0;
  B.flights=[]; B.lastResid=0; B.worstResid=0; B.sumResid=0;
  B.therm=[0,1,2,3].map(k=>{ const h=trayHome(k); return {x:h.x,y:h.y,tray:true,att:null}; });
  B.hist={t:[],T:[[],[],[],[]],E:[[],[],[],[]],work:[],room:[],stride:1,skip:0};
  benchRecord(B);
}
/* each spot's stack, bottom to top: a body sits on the burner or ground, on a
   block's top, or 1 mm inside a beaker's bottom (PhET's topSurface) */
function benchLayout(B){
  for(let k=0;k<6;k++){
    const y0=(k===2||k===3)?BURNER_TOP:0; let prev=null;
    for(const i of B.chains[k]){
      const b=B.bodies[i]; b.x=SPOTS[k];
      b.y=prev===null?y0:(prev.kind==='beaker'?prev.y+0.001:prev.y+prev.h);
      prev=b;
    }
  }
  if(B.held) benchLayoutHeld(B);
}
function benchLayoutHeld(B){
  const H=B.held; let prev=null;
  for(const i of H.group){
    const b=B.bodies[i];
    if(prev===null){ b.x=H.x; b.y=H.y; }
    else { b.x=prev.x; b.y=prev.kind==='beaker'?prev.y+0.001:prev.y+prev.h; }
    prev=b;
  }
}
function chainOf(B,i){ for(let k=0;k<6;k++){ const j=B.chains[k].indexOf(i); if(j>=0) return [k,j]; } return null; }
/* PhET's drop rule: try the spots nearest first; a spot whose stack holds a
   beaker refuses a group that holds one (no beaker on or in a beaker) */
function spotOrder(x){ return [0,1,2,3,4,5].sort((a,b)=>Math.abs(SPOTS[a]-x)-Math.abs(SPOTS[b]-x)); }
function canStack(B,group,k){
  const gb=group.some(i=>B.bodies[i].kind==='beaker'), cb=B.chains[k].some(i=>B.bodies[i].kind==='beaker');
  return !(gb&&cb);
}
function benchPlace(B,i,k){
  const at=chainOf(B,i); let group;
  if(at){ group=B.chains[at[0]].slice(at[1]); B.chains[at[0]].length=at[1]; }
  else if(B.held&&B.held.group[0]===i){ group=B.held.group.slice(); B.held=null; }
  else return false;
  if(!canStack(B,group,k)){ if(at) B.chains[at[0]].push(...group); benchLayout(B); return false; }
  B.chains[k].push(...group); benchLayout(B); return true;
}
function benchGrab(B,i,x,y){
  const at=chainOf(B,i); if(!at) return false;
  const group=B.chains[at[0]].slice(at[1]); B.chains[at[0]].length=at[1];
  const b=B.bodies[i];
  B.held={i,group,x:b.x,y:b.y,dx:b.x-x,dy:b.y-y};
  benchLayout(B); return true;
}
function benchMoveHeld(B,x,y){
  const H=B.held; if(!H) return;
  H.x=clamp(x+H.dx,BENCH_XLIM[0],BENCH_XLIM[1]); H.y=clamp(y+H.dy,0,BENCH_YMAX);
  benchLayout(B);
}
function benchDropSpot(B,x,group){ for(const k of spotOrder(x)) if(canStack(B,group,k)) return k; return -1; }
function benchDrop(B){
  const H=B.held; if(!H) return -1;
  const k=benchDropSpot(B,H.x,H.group);
  B.held=null; B.chains[k].push(...H.group); benchLayout(B);
  return k;
}
/* the topmost body under a world point: blocks (front) before beakers */
function benchPick(B,x,y){
  for(const i of [1,0]){ const b=B.bodies[i]; if(inPoly(blockHex(b),x,y)) return i; }
  for(const i of [3,2]){ const b=B.bodies[i]; if(x>=b.x-b.w/2&&x<=b.x+b.w/2&&y>=b.y&&y<=b.y+b.h) return i; }
  return -1;
}
function burnerX(k){ return SPOTS[2+k]; }
function burnerContact(k,b){
  const a=bodyArea(b), cx=(a.x0+a.x1)/2, bx=burnerX(k);
  return cx>bx-BURNER_HALF&&cx<bx+BURNER_HALF&&Math.abs(a.y0-BURNER_TOP)<0.001;
}
/* linking is one mechanism, not two: every writer (both sliders, the lever
   drag, the link box) keeps lev0 and lev1 equal while linked, so the levels
   are simply the two keys (a second link check here made each copy's mutant
   equivalent -- the Known-bad two-guards trap) */
function burnerLevels(st){ return [st.lev0,st.lev1]; }

function benchFlow(B,key,a,b,q){
  let L=B.link[key];
  if(!L) L=B.link[key]={B:0,a,b,upd:false,key};
  L.B+=q; L.upd=true;
}
/* one step of PhET's stepModel; returns the step's ledger residual (J) */
function benchStep(B,lev){
  const bodies=B.bodies, dt=DT;
  for(const k in B.link) B.link[k].upd=false;
  /* 1. fluid displacement: one update per step, from the blocks' bounds */
  for(const bk of bodies){
    if(bk.kind!=='beaker') continue;
    const fx0=bk.x-bk.w/2, fy0=bk.y, fx1=fx0+bk.w, fy1=fy0+bk.h*bk.f;
    let area=0;
    for(const bl of bodies){
      if(bl.kind!=='block') continue;
      const bb=bodyBounds(bl);
      const ix0=Math.max(bb.x0,fx0), ix1=Math.min(bb.x1,fx1), iy0=Math.max(bb.y0,fy0), iy1=Math.min(bb.y1,fy1);
      if(ix1-ix0>=0&&iy1-iy0>=0) area+=(ix1-ix0)*(iy1-iy0);
    }
    bk.f=Math.min(FLUID0+DISPLACE*area,1);
  }
  let E0=0; for(const b of bodies) E0+=b.E;
  let work=0, room=0;
  /* 2. every pair once, blocks first (PhET's thermalContainers order) */
  for(let i=0;i<4;i++) for(let j=i+1;j<4;j++){
    const q=exchange(bodies[i],bodies[j],dt);
    if(contactLen(bodyArea(bodies[i]),bodyArea(bodies[j]))>0) benchFlow(B,'p'+i+j,i,j,q);
  }
  /* 3. the burners: into whatever sits on them, else into the room */
  for(let k=0;k<2;k++){
    const l=lev[k];
    if(bodies.some(b=>burnerContact(k,b))){
      bodies.forEach((b,i)=>{
        if(!burnerContact(k,b)) return;
        let q=0;
        if(bodyT(b)>T_FREEZE){ q=P_BURN*l*dt; if(l<0&&Math.abs(q)>b.E-bodyMinE(b)) q=-(b.E-bodyMinE(b)); }
        b.E+=q; work+=q; B.workK[k]+=q;
        benchFlow(B,'b'+k+i,'b'+k,i,q);
      });
    } else {
      const q=P_BURN_AIR*l*dt; work+=q; room+=q; B.workK[k]+=q; B.workAir+=q;
      benchFlow(B,'b'+k+'A','b'+k,'A',q);
    }
  }
  /* 4. the room: every body not immersed in a beaker */
  bodies.forEach((b,i)=>{
    if(isImmersed(bodies,b)) return;
    const q=airExchange(b,dt); room+=q; B.roomBodies+=q;
    benchFlow(B,'a'+i,i,'A',q);
  });
  B.work+=work; B.room+=room;
  let E1=0; for(const b of bodies) E1+=b.E;
  const resid=E1-E0+room-work;
  benchChunks(B,lev);
  B.t+=dt; B.steps++;
  for(const f of B.flights) f.t+=dt;
  B.flights=B.flights.filter(f=>f.t<f.dur);
  benchRecord(B);
  B.lastResid=resid;
  const scale=bodies.reduce((s,b)=>s+Math.abs(b.E),0)+Math.abs(B.room)+Math.abs(B.work);
  B.worstResid=Math.max(B.worstResid,Math.abs(resid)/scale); B.sumResid+=resid;
  return resid;
}

/* ---- the chunk rule ------------------------------------------------------
   (a) PhET's threshold pass: a link carries a chunk once more than a chunk's
       worth (EPC) has crossed it, never a body's last chunk;
   (b) the corrective pass: no body may sit a whole chunk or more from its
       energy, g(E) = PhET's map unrounded; it sends or takes one along the
       link carrying the most energy the right way (a partner that can take
       it first; the room always can).
   Every transfer moves the link's balance by EPC, so for each body
       E + (energy still in transit on its links) - EPC x chunks
   never changes: the exact identity selfTest pins. */
function isBodyRef(x){ return typeof x==='number'; }
function moveKind(a,b){ return isBodyRef(a)&&isBodyRef(b)?'pair':(a==='A'||b==='A'?'air':'burner'); }
function benchGive(B,src,dst,kind){
  if(isBodyRef(src)) B.own[src]--;
  if(isBodyRef(dst)) B.own[dst]++;
  B.moved[kind]++;
  const d=Math.max(0.35,Math.min(2.2,kind==='air'?1.6:(kind==='burner'?0.9:0.8)));
  B.flights.push({src,dst,t:0,dur:d,air:(src==='A'?dst:(dst==='A'?src:null))});
}
function benchChunks(B,lev){
  const bodies=B.bodies, keys=Object.keys(B.link).sort();
  for(const key of keys){
    const L=B.link[key]; if(!L.upd) continue;
    if(L.B>EPC){ if(!(isBodyRef(L.a)&&B.own[L.a]<=1)){ benchGive(B,L.a,L.b,moveKind(L.a,L.b)); L.B-=EPC; } }
    else if(L.B<-EPC){ if(!(isBodyRef(L.b)&&B.own[L.b]<=1)){ benchGive(B,L.b,L.a,moveKind(L.a,L.b)); L.B+=EPC; } }
  }
  for(let it=0;it<8;it++){
    let bad=false;
    for(let i=0;i<4;i++){
      const dev=B.own[i]-gChunks(bodies[i].E);
      if(dev>=1||dev<=-1){ bad=true; benchCorrect(B,i,dev>0,lev,keys); }
    }
    if(!bad) break;
  }
  for(let i=0;i<4;i++) B.maxdev=Math.max(B.maxdev,Math.abs(B.own[i]-gChunks(bodies[i].E)));
}
function okPartner(B,p,receiving,lev){
  if(p==='A') return true;
  if(!isBodyRef(p)){ const l=lev[+p[1]]; return receiving?l<0:l>0; }
  const dev=B.own[p]-gChunks(B.bodies[p].E);
  return receiving?dev<0:(dev>0&&B.own[p]>1);
}
function benchCorrect(B,i,excess,lev,keys){
  const cands=[];
  for(const key of keys){
    const L=B.link[key]; if(!L||!L.upd) continue;
    if(L.a===i) cands.push([L,L.b,L.B]); else if(L.b===i) cands.push([L,L.a,-L.B]);
  }
  let best=null;
  for(const [L,p,outb] of cands){ const sc=excess?outb:-outb; if(okPartner(B,p,excess,lev)&&(best===null||sc>best[0])) best=[sc,L,p]; }
  if(best===null) for(const [L,p,outb] of cands){ const sc=excess?outb:-outb; if(best===null||sc>best[0]) best=[sc,L,p]; }
  if(best===null) return;
  const L=best[1], p=best[2], kind=moveKind(i,p);
  B.corr[excess?'excess':'deficit']++;
  if(excess){ benchGive(B,i,p,kind); if(L.a===i) L.B-=EPC; else L.B+=EPC; }
  else { benchGive(B,p,i,kind); if(L.a===i) L.B+=EPC; else L.B-=EPC; }
}
/* E_i + S_i - EPC own_i, which the chunk rule keeps at its reset value */
function benchIdentity(B,i){
  let S=0;
  for(const k in B.link){ const L=B.link[k]; if(L.a===i) S+=L.B; else if(L.b===i) S-=L.B; }
  return B.bodies[i].E+S-EPC*B.own[i];
}
function benchIdentity0(B,i){ return B.E0[i]-EPC*B.own0[i]; }

/* ---- the clock: whole 1/60-s steps; x4 takes four a frame ---- */
const STEP_TOL=1e-9;
function benchAdvance(B,st,dtWall){
  B.acc+=dtWall*(st.speed==='fast'?SPEED_FAST:1);
  let n=0;
  while(B.acc>=DT*(1-STEP_TOL)&&n<40){ B.acc-=DT; benchStep(B,burnerLevels(st)); n++; }
  if(n>=40) B.acc=0;
  return n;
}

/* ---- the history the ledger view draws: every step to HIST_MAX points, then
   every other point kept and the stride doubled (deterministic) ---- */
function benchRecord(B){
  const H=B.hist;
  if(H.skip>0){ H.skip--; return; }
  H.skip=H.stride-1;
  H.t.push(B.t); H.work.push(B.work); H.room.push(B.room);
  for(let i=0;i<4;i++){ H.T[i].push(bodyT(B.bodies[i])); H.E[i].push(B.bodies[i].E); }
  if(H.t.length>HIST_MAX){
    const keep=(arr)=>arr.filter((v,k)=>k%2===0);
    H.t=keep(H.t); H.work=keep(H.work); H.room=keep(H.room);
    for(let i=0;i<4;i++){ H.T[i]=keep(H.T[i]); H.E[i]=keep(H.E[i]); }
    H.stride*=2; H.skip=H.stride-1;
  }
}

/* ---- thermometers: PhET's sensing order (blocks, then the beakers' liquid,
   then the steam over a boiling beaker, then a burner's flame or ice, else
   the room); a thermometer dropped on a body follows it ---- */
function steamProp(b){ const T=bodyT(b), tb=T_BOIL[b.mat]; return T>tb-10?clamp(1-(tb-T)/10,0,1):0; }
function thermoSense(B,x,y,lev){
  for(const i of [1,0]){ const b=B.bodies[i]; if(inPoly(blockHex(b),x,y)) return {T:bodyT(b),what:i}; }
  for(const i of [2,3]){ const a=bodyArea(B.bodies[i]); if(x>=a.x0&&x<=a.x1&&y>=a.y0&&y<=a.y1) return {T:bodyT(B.bodies[i]),what:i}; }
  for(const i of [2,3]){
    const b=B.bodies[i], a=bodyArea(b), sp=steamProp(b), top=a.y1, hS=2*b.h;
    if(sp>0&&x>=a.x0&&x<=a.x1&&y>=top&&y<=top+hS){
      const T=linearMap(0,hS*sp,bodyT(b),T_ROOM,y-top);
      return {T:Math.max(T,T_ROOM),what:'steam'+i};
    }
  }
  for(let k=0;k<2;k++){ const bx=burnerX(k);
    if(x>=bx-BURNER_HALF/2&&x<=bx+BURNER_HALF/2&&y>=BURNER_TOP/2&&y<=BURNER_TOP) return {T:Math.max(T_ROOM+100*lev[k],T_FREEZE),what:'burner'+k}; }
  return {T:T_AIR,what:'air'};
}
function thermoTip(B,th){
  if(th.att){ const b=B.bodies[th.att.i]; return {x:b.x+th.att.dx, y:b.y+th.att.dy}; }
  return {x:th.x, y:th.y};
}
function inTray(x,y){ return x>=TRAY.x0&&x<=TRAY.x1&&y>=TRAY.y0-0.01&&y<=TRAY.y1; }
function thermoDrop(B,k){
  const th=B.therm[k], p=thermoTip(B,th);
  th.att=null; th.x=p.x; th.y=p.y;
  if(inTray(p.x,p.y+THERMO_H/2)){ const h=trayHome(k); th.x=h.x; th.y=h.y; th.tray=true; return 'tray'; }
  th.tray=false;
  for(const i of [1,0]){ const b=B.bodies[i]; if(inPoly(blockHex(b),p.x,p.y)){ th.att={i,dx:p.x-b.x,dy:p.y-b.y}; return i; } }
  for(const i of [2,3]){ const a=bodyArea(B.bodies[i]); if(p.x>=a.x0&&p.x<=a.x1&&p.y>=a.y0&&p.y<=a.y1){ const b=B.bodies[i]; th.att={i,dx:p.x-b.x,dy:p.y-b.y}; return i; } }
  return 'free';
}
function thermoPick(B,x,y){
  for(let k=3;k>=0;k--){ const p=thermoTip(B,B.therm[k]);
    if(Math.abs(x-p.x)<=0.009&&y>=p.y-0.006&&y<=p.y+THERMO_H) return k; }
  return -1;
}

/* ---- presets: PhET's start and four set-ups that make the ledger move ---- */
const BENCH_PRESETS=[{id:'start',name:'PhET’s start'},{id:'heat',name:'heat the iron'},{id:'hot',name:'hot iron into water'},
                     {id:'stack',name:'brick on iron, cooling'},{id:'boil',name:'boil the water'}];
function benchPreset(B,st,id){
  benchReset(B);
  st.lev0=0; st.lev1=0; st.link=false;
  if(id==='heat'){ benchPlace(B,0,2); st.lev0=1; }
  else if(id==='hot'){ benchPlace(B,0,4); const b=B.bodies[0]; b.E=b.m*b.c*500; }
  else if(id==='stack'){ benchPlace(B,0,3); benchPlace(B,1,3); st.lev1=-1; }
  else if(id==='boil'){ benchPlace(B,2,2); st.lev0=1; }
  B.own=B.bodies.map(b=>nChunks(b.E)); B.own0=B.own.slice(); B.E0=B.bodies.map(b=>b.E);
  B.hist={t:[],T:[[],[],[],[]],E:[[],[],[],[]],work:[],room:[],stride:1,skip:0};
  benchRecord(B);
}
benchReset(BENCH);
