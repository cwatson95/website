
/* ================================================================== *
 *  the systems (PhET's Systems screen): a source, a converter and a   *
 *  user, stepped at 1/60 s on a ledger that closes                    *
 * ================================================================== */
const SOURCES=[{id:'biker',name:'cyclist'},{id:'faucet',name:'faucet'},{id:'sun',name:'sun'},{id:'teapot',name:'teapot'}];
const CONVERTERS=[{id:'generator',name:'generator'},{id:'panel',name:'solar panel'}];
const USERS=[{id:'heater',name:'beaker heater'},{id:'incandescent',name:'incandescent bulb'},{id:'fluorescent',name:'fluorescent bulb'},{id:'fan',name:'fan'}];
/* the chunk channels: [id, form, what it carries] */
const CHANNELS=[['b.chem','chemical','food burned'],['b.mech','mechanical','the pedals, to the belt'],['b.heat','thermal','body heat'],
  ['f.water','mechanical','falling water'],['s.light','light','sunlight past the clouds'],['s.refl','light','sunlight the clouds send back'],
  ['t.flame','thermal','the burner, into the kettle'],['t.loss','thermal','heat round the kettle'],['t.steam','mechanical','steam'],
  ['g.elec','electrical','the generator, to the wire'],['g.heat','thermal','the wheel’s losses'],['p.elec','electrical','the panel, to the wire'],
  ['p.heat','thermal','the panel’s losses'],['h.coil','thermal','the coil, into the water'],['h.loss','thermal','the coil’s loss'],
  ['h.water','thermal','the water, to the room'],['l.light','light','the bulb’s light'],['l.heat','thermal','the bulb’s heat'],
  ['n.wind','mechanical','the fan’s wind'],['n.heat','thermal','the motor’s heat'],['x.miss','*','what the converter cannot use']];
const CH_FORM={}; CHANNELS.forEach(c=>CH_FORM[c[0]]=c[1]);
function srcForm(src){ return src==='sun'?'light':'mechanical'; }
function convTakes(conv,src){ return conv==='generator'?srcForm(src)==='mechanical':srcForm(src)==='light'; }

const SYS={};
function sysReset(S,st){
  S.src=st.src; S.conv=st.conv; S.user=st.user;
  S.omega=0; S.crank=0; S.rear=0; S.food=FOOD0;
  S.fall=new Array(FALL_STEPS).fill(0);
  S.kettle=0; S.wheel=0; S.wAngle=0; S.wOmega=0;
  S.hp=0; S.water=HB_C*T_ROOM; S.water0=S.water;
  S.fan=0; S.fanAngle=0; S.lit=0;
  S.acc={}; S.count={}; S.chsum={}; for(const c of CHANNELS){ S.acc[c[0]]=0; S.count[c[0]]=0; S.chsum[c[0]]=0; }
  S.inp={fed:0,main:0,sun:0,gas:0}; S.sink={light:0,wind:0,room:0,reflected:0,escaped:0}; S.swap=0;
  S.stores0=sysStores(S);
  S.t=0; S.steps=0; S.acc_t=0; S.worstEl=0; S.worstClosure=0; S.flights=[]; S.flows=sysZeroFlows();
  S.hist={t:[],sup:[],use:[],loss:[],store:[],stride:1,skip:0};
  S.feedBase=0; S.foodChem0=0;
}
function sysStores(S){ return S.food+S.fall.reduce((a,b)=>a+b,0)+S.kettle+S.wheel+(S.water-S.water0); }
function sysClosure(S){
  const inp=S.inp.fed+S.inp.main+S.inp.sun+S.inp.gas;
  const out=S.sink.light+S.sink.wind+S.sink.room+S.sink.reflected+S.sink.escaped;
  return inp-out-(sysStores(S)-S.stores0);
}
function sysInputTotal(S){ return S.inp.fed+S.inp.main+S.inp.sun+S.inp.gas+Math.abs(S.stores0); }
function sysZeroFlows(){ return {srcIn:0,srcOut:0,srcLoss:0,srcStore:0,cIn:0,cOut:0,cLoss:0,cStore:0,cMiss:0,uIn:0,uOut:0,uLoss:0,uStore:0,
  refl:0,light:0,wind:0,water:0,waterLoss:0,coilLoss:0}; }
/* one element's ledger: in = out + loss + change in its store */
function sysCheck(S,inE,out,loss,dstore,store){
  const r=inE-out-loss-dstore, sc=Math.abs(inE)+Math.abs(out)+Math.abs(loss)+Math.abs(dstore)+Math.abs(store||0);
  if(sc>0) S.worstEl=Math.max(S.worstEl,Math.abs(r)/sc);
  return r;
}
function sysChan(S,c,E){
  S.chsum[c]+=E; S.acc[c]+=E;
  while(S.acc[c]>=EPC){ S.acc[c]-=EPC; S.count[c]++; sysSpawn(S,c); }
}

function sysStep(S,st){
  const dt=DT, F=sysZeroFlows();
  let form=null, Eout=0;
  /* ---------------- the source */
  if(S.src==='biker'){
    const target=st.pedal*OMEGA_MAX, tgt=S.food>0?target:0, d=tgt-S.omega;
    if(d!==0){ const r=CRANK_ACC*dt; S.omega=d>0?Math.min(S.omega+r,target):Math.max(S.omega-r,0); }
    S.crank=(S.crank+S.omega*dt)%TAU; S.rear=(S.rear+S.omega*dt)%TAU;
    const load=S.conv==='generator';
    const pchem=(load?BIKE_LOAD:BIKE_FREE)*S.omega/OMEGA_MAX;
    const Ec=Math.min(pchem*dt,S.food);
    S.food-=Ec;
    const Em=load?BIKE_MECH*Ec:0, Eh=Ec-Em;
    S.sink.room+=Eh;
    sysCheck(S,0,Em,Eh,-Ec,S.food+Ec);
    sysChan(S,'b.chem',Ec); sysChan(S,'b.mech',Em); sysChan(S,'b.heat',Eh);
    F.srcIn=Ec; F.srcOut=Em; F.srcLoss=Eh;     /* the food burned is the supply band itself */
    form='mechanical'; Eout=Em;
  } else if(S.src==='faucet'){
    const Ein=MAXP*st.flow*dt;
    S.inp.main+=Ein;
    S.fall.push(Ein); Eout=S.fall.shift();
    sysCheck(S,Ein,Eout,0,Ein-Eout,S.fall.reduce((a,b)=>a+b,0)+Eout);
    sysChan(S,'f.water',Ein);
    F.srcIn=Ein; F.srcOut=Eout; F.srcStore=Ein-Eout;
    form='mechanical';
  } else if(S.src==='sun'){
    const Ein=MAXP*dt, Et=MAXP*sunFrac(st.clouds)*dt, Er=Ein-Et;
    S.inp.sun+=Ein; S.sink.reflected+=Er;
    sysCheck(S,Ein,Et,Er,0);
    sysChan(S,'s.light',Et); sysChan(S,'s.refl',Er);
    F.srcIn=Ein; F.srcOut=Et; F.srcLoss=Er; F.refl=Er;
    form='light'; Eout=Et;
  } else {
    const Ein=MAXP*st.heat*dt; S.inp.gas+=Ein;
    const Ek=STEAM*Ein; let El=Ein-Ek;
    const k0=S.kettle; S.kettle+=Ek;
    let Es=S.kettle*dt/TAU_K;
    if(st.heat===0&&Es/dt<KETTLE_CUT){ El+=S.kettle; S.kettle=0; Es=0; } else S.kettle-=Es;
    S.sink.room+=El;
    sysCheck(S,Ein,Es,El,S.kettle-k0,k0+Ek);
    sysChan(S,'t.flame',Ein); sysChan(S,'t.loss',El); sysChan(S,'t.steam',Es);
    F.srcIn=Ein; F.srcOut=Es; F.srcLoss=El; F.srcStore=S.kettle-k0;
    form='mechanical'; Eout=Es;
  }
  /* ---------------- the converter */
  let Ee=0;
  F.cIn=Eout;
  if(S.conv==='generator'&&form==='mechanical'){
    if(S.src==='biker'){ Ee=Eout; sysCheck(S,Eout,Ee,0,0); }
    else {
      const w0=S.wheel; S.wheel+=Eout;
      const Er=S.wheel*dt/TAU_W; S.wheel-=Er;
      Ee=ETA_W*Er; const Eh=Er-Ee;
      S.sink.room+=Eh; sysCheck(S,Eout,Ee,Eh,S.wheel-w0,w0+Eout);
      sysChan(S,'g.heat',Eh); F.cLoss=Eh; F.cStore=S.wheel-w0;
    }
    sysChan(S,'g.elec',Ee);
    /* PhET: the output is 10 kW x w/(pi/2), so the wheel turns at (pi/2) P/10 kW */
    S.wOmega=(Math.PI/2)*(Ee/dt)/MAXP; S.wAngle=(S.wAngle+S.wOmega*dt)%TAU;
  } else if(S.conv==='panel'&&form==='light'){
    Ee=ETA_PANEL*Eout; const Eh=Eout-Ee;
    S.sink.room+=Eh; sysCheck(S,Eout,Ee,Eh,0);
    sysChan(S,'p.elec',Ee); sysChan(S,'p.heat',Eh); F.cLoss=Eh;
    S.wOmega=0;
  } else {
    S.sink.escaped+=Eout; sysCheck(S,Eout,0,Eout,0); sysChan(S,'x.miss',Eout); F.cMiss=Eout;
    S.wOmega=0;
  }
  F.cOut=Ee;
  /* ---------------- the user */
  F.uIn=Ee;
  if(S.user==='heater'){
    const r=(Ee/dt)/MAXP;
    S.hp=Math.min(r,S.hp+HEAT_RAMP*dt);
    const Ew=HEAT_MAXP*S.hp*dt, El=Ee-Ew, w0=S.water;
    S.water+=Ew;
    const T=Math.min(S.water/HB_C,T_BOIL.water), s=T-T_ROOM;
    let Ea=0;
    if(Math.abs(s)>EQ_THRESH){ Ea=s*K_AIR*HB_L*dt; S.water-=Ea; }
    const Eb=Math.max(S.water-T_BOIL.water*HB_C,0); S.water-=Eb;
    S.sink.room+=El+Ea+Eb;
    sysCheck(S,Ee,0,El+Ea+Eb,S.water-w0,w0+Ew);
    sysChan(S,'h.coil',Ew); sysChan(S,'h.loss',El); sysChan(S,'h.water',Ea+Eb);
    F.uLoss=El+Ea+Eb; F.uStore=S.water-w0; F.water=Ew; F.waterLoss=Ea+Eb; F.coilLoss=El;
    S.lit=0;
  } else if(S.user==='incandescent'||S.user==='fluorescent'){
    const El=LIGHT_FRAC[S.user]*Ee, Eh=Ee-El;
    S.sink.light+=El; S.sink.room+=Eh; sysCheck(S,Ee,El,Eh,0);
    sysChan(S,'l.light',El); sysChan(S,'l.heat',Eh);
    F.uOut=El; F.uLoss=Eh; F.light=El;
    S.lit=clamp((Ee/dt)/MAXP,0,1);
  } else {
    const Eh=FAN_HEAT*Ee, Ew=Ee-Eh;
    S.sink.wind+=Ew; S.sink.room+=Eh; sysCheck(S,Ee,Ew,Eh,0);
    sysChan(S,'n.wind',Ew); sysChan(S,'n.heat',Eh);
    F.uOut=Ew; F.uLoss=Eh; F.wind=Ew;
    let tgt=FAN_W*Ee/dt; tgt=tgt<FAN_MIN?0:tgt;
    const d=tgt-S.fan;
    if(d!==0) S.fan=d>0?Math.min(S.fan+FAN_ACC*dt,tgt):Math.max(S.fan-FAN_ACC*dt,0);
    S.fanAngle=(S.fanAngle+S.fan*dt)%TAU; S.lit=0;
  }
  for(const k in F) F[k]/=dt;              /* the flows are kept as powers, W */
  S.flows=F;
  S.t+=dt; S.steps++;
  const c=sysClosure(S), sc=sysInputTotal(S);
  S.worstClosure=Math.max(S.worstClosure,Math.abs(c)/Math.max(sc,1));
  sysMoveFlights(S,dt);
  sysRecord(S);
}
function sysAdvance(S,st,dtWall){
  S.acc_t+=dtWall; let n=0;
  while(S.acc_t>=DT*(1-STEP_TOL)&&n<40){ S.acc_t-=DT; sysStep(S,st); n++; }
  if(n>=40) S.acc_t=0;
  return n;
}
/* the cumulative ledger for the flow view.  IN is what entered the chain
   (water, sunlight, gas, and the food the cyclist burned), OUT what it
   delivered (light, wind), LOST what went to the room or never arrived, and
   STORED what the falling water, the kettle, the wheel and the heater's water
   hold now.  IN = OUT + LOST + STORED is the global ledger with the food store
   taken as the cyclist's supply (fed - change in food = food burned). */
function sysBalance(S){
  const IN=S.inp.main+S.inp.sun+S.inp.gas+S.chsum['b.chem'];
  const OUT=S.sink.light+S.sink.wind;
  const LOST=S.sink.room+S.sink.reflected+S.sink.escaped;
  const STORED=S.fall.reduce((a,b)=>a+b,0)+S.kettle+S.wheel+(S.water-S.water0);
  return {IN,OUT,LOST,STORED,resid:IN-OUT-LOST-STORED};
}
function sysRecord(S){
  const H=S.hist;
  if(H.skip>0){ H.skip--; return; }
  H.skip=H.stride-1;
  const L=sysBalance(S);
  H.t.push(S.t); H.sup.push(L.IN); H.use.push(L.OUT); H.loss.push(L.LOST); H.store.push(L.STORED);
  if(H.t.length>HIST_MAX){
    const keep=a=>a.filter((v,k)=>k%2===0);
    H.t=keep(H.t); H.sup=keep(H.sup); H.use=keep(H.use); H.loss=keep(H.loss); H.store=keep(H.store);
    H.stride*=2; H.skip=H.stride-1;
  }
}
/* chain changes, PhET's way: the element swapped out is reset (its control to
   zero, the cyclist refed when he comes back); whatever its stores held goes to
   the room as heat, logged, so the ledger still closes */
function sysDump(S,E){ if(E!==0){ S.sink.room+=E; S.swap+=E; } }
function sysSelect(S,st,which,id){
  if(which==='src'){
    if(S.src===id) return false;
    if(S.src==='faucet'){ sysDump(S,S.fall.reduce((a,b)=>a+b,0)); S.fall.fill(0); st.flow=0; }
    if(S.src==='teapot'){ sysDump(S,S.kettle); S.kettle=0; st.heat=0; }
    if(S.src==='sun') st.clouds=0;
    if(S.src==='biker'){ st.pedal=0; S.omega=0; }
    if(S.conv==='generator'){ sysDump(S,S.wheel); S.wheel=0; }
    S.src=id; st.src=id;
    if(id==='biker'&&S.food<FOOD0){ S.inp.fed+=FOOD0-S.food; S.food=FOOD0; }
  } else if(which==='conv'){
    if(S.conv===id) return false;
    if(S.conv==='generator'){ sysDump(S,S.wheel); S.wheel=0; S.wOmega=0; }
    S.conv=id; st.conv=id;
  } else {
    if(S.user===id) return false;
    if(S.user==='heater'){ sysDump(S,S.water-S.water0); S.water=S.water0; S.hp=0; }
    if(S.user==='fan') S.fan=0;
    S.user=id; st.user=id; S.lit=0;
  }
  S.flights=S.flights.filter(f=>chainHas(S,f.ch));
  return true;
}
function sysFeed(S){ if(S.food>=FOOD0) return false; S.inp.fed+=FOOD0-S.food; S.food=FOOD0; return true; }
function foodChunks(S){ return Math.ceil(S.food/EPC-1e-9); }
function chainHas(S,ch){
  const p=ch[0];
  if(p==='b') return S.src==='biker'; if(p==='f') return S.src==='faucet'; if(p==='s') return S.src==='sun'; if(p==='t') return S.src==='teapot';
  if(p==='g') return S.conv==='generator'; if(p==='p') return S.conv==='panel'; if(p==='x') return true;
  if(p==='h') return S.user==='heater'; if(p==='l') return S.user==='incandescent'||S.user==='fluorescent'; if(p==='n') return S.user==='fan';
  return false;
}

/* ---- the layout (world metres, y up), after PhET's: the source at
   (-0.15, 0), the converter at (-0.025, 0), the user at (0.09, 0) ---- */
const SX=-0.15, CX=-0.025, UX=0.09, FLOOR=-0.045;
const GW={x:CX,y:0.03}, GW_R=GEN_R, GW_PAD=0.058;           /* the generator's wheel (PhET's 0.039 m) and its paddles */
const RW={x:SX+0.035,y:-0.01}, RW_R=0.021;                   /* the cyclist's rear wheel (PhET's offset) */
const SPOUT={x:SX+0.069,y:0.105};                            /* the faucet's water leaves here (PhET's) */
const SUN={x:SX-0.05,y:0.12}, SUN_R=0.02;
const CLOUDS=[[SX-0.01,0.08],[SX+0.017,0.0875],[SX+0.02,0.105]], CLOUD_RX=0.0175, CLOUD_RY=0.035*0.55/2;
const KETTLE={x:SX,y:0.02}, KSPOUT={x:SX+0.05,y:0.045};
const WIRE0={x:CX+0.057,y:-0.041}, WIRE1={x:UX-0.04,y:-0.041};
const PANEL=[[CX-0.075,0.0],[CX+0.075,0.07]];
function cloudStrength(c,i){ return clamp(c*3-i,0,1); }
function pathLen(p){ let L=0; for(let i=1;i<p.length;i++) L+=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]); return L; }
function pathAt(p,s){
  for(let i=1;i<p.length;i++){
    const d=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]);
    if(s<=d||i===p.length-1){ const u=d>0?clamp(s/d,0,1):1; return [p[i-1][0]+(p[i][0]-p[i-1][0])*u, p[i-1][1]+(p[i][1]-p[i-1][1])*u]; }
    s-=d;
  }
  return p[p.length-1].slice();
}
/* each channel's path; `k` spreads a channel's chunks (deterministic) */
function chunkPath(S,ch,k){
  const j=((k*0.6180339887)%1)-0.5;
  const userIn=[[WIRE0.x,WIRE0.y],[WIRE1.x,WIRE1.y],[UX-0.02,-0.041],[UX-0.001,-0.027],[UX,0.0]];
  switch(ch){
    case 'b.chem': return [[SX+0.012+0.008*j,0.058],[SX+0.006,0.035],[SX+0.0058,-0.006]];
    case 'b.mech': return [[SX+0.0058,-0.006],[RW.x,RW.y],[RW.x,RW.y+RW_R],[GW.x,GW.y+GW_R],[GW.x,GW.y]];
    case 'b.heat': return S.conv==='generator'?[[SX+0.014,0.06],[SX+0.03+0.03*j,0.2]]:[[RW.x,RW.y],[RW.x+0.03*j,0.2]];
    case 'f.water': return S.conv==='generator'?[[SPOUT.x+0.004*j,SPOUT.y],[SPOUT.x+0.004*j,GW.y+0.012],[GW.x,GW.y]]:[[SPOUT.x+0.004*j,SPOUT.y],[SPOUT.x+0.004*j,FLOOR]];
    case 's.light': { const z=convTakes(S.conv,'sun')?[CX-0.03+0.06*j,0.03+0.028*j]:[CX+0.04*j,FLOOR], a=Math.atan2(z[1]-SUN.y,z[0]-SUN.x);
      return [[SUN.x+SUN_R*Math.cos(a),SUN.y+SUN_R*Math.sin(a)],z]; }
    case 's.refl': { const c=CLOUDS[Math.abs(Math.round(j*4))%3], a=Math.atan2(c[1]-SUN.y,c[0]-SUN.x);
      return [[SUN.x+SUN_R*Math.cos(a),SUN.y+SUN_R*Math.sin(a)],[c[0],c[1]],[c[0]-0.06+0.02*j,0.21]]; }
    case 't.flame': return [[SX+0.02*j,-0.03],[SX+0.02*j,0.012]];
    case 't.loss': return [[SX-0.02,0.03],[SX-0.07+0.03*j,0.2]];
    case 't.steam': return S.conv==='generator'?[[KSPOUT.x,KSPOUT.y],[GW.x-0.035,GW.y+0.045],[GW.x,GW.y]]:[[KSPOUT.x,KSPOUT.y],[KSPOUT.x+0.08,KSPOUT.y+0.095]];
    case 'g.elec': return [[GW.x,GW.y],[CX+0.011,-0.02],[CX+0.03,-0.0405],[WIRE0.x,WIRE0.y]].concat(userIn.slice(1));
    case 'g.heat': return [[GW.x,GW.y],[GW.x+0.04*j,0.2]];
    case 'p.elec': return [[CX+0.03*j,0.035+0.02*j],[CX+0.015,0.0065],[CX+0.015,-0.025],[CX+0.03,-0.0385],[WIRE0.x,WIRE0.y]].concat(userIn.slice(1));
    case 'p.heat': return [[CX+0.03*j,0.035+0.02*j],[CX+0.05*j,0.2]];
    case 'x.miss': return [[CX-0.05+0.03*j,-0.02],[CX-0.05+0.03*j,FLOOR]];
    case 'h.coil': return [[UX+0.03*j,0.004],[UX+0.03*j,0.045]];
    case 'h.loss': return [[UX+0.03*j,0.0],[UX+0.05+0.01*j,0.02],[UX+0.065,0.19]];
    case 'h.water': return [[UX+0.03*j,0.057],[UX+0.03*j,0.2]];
    case 'l.light': case 'l.heat': { const a=Math.PI/3+(Math.PI/3)*(j+0.5); return [[UX,0.066],[UX+0.13*Math.cos(a),0.066+0.13*Math.sin(a)]]; }
    case 'n.wind': return [[UX-0.0265,0.045],[UX+0.02,0.045+0.01*j],[UX+0.07,0.045+0.02*j]];
    case 'n.heat': return [[UX-0.0265,0.019],[UX-0.05,0.19]];
  }
  return [[0,0],[0,0.2]];
}
/* 'x.miss' is counted but not drawn: the source's own chunks already carry
   that energy on past a converter that cannot use it */
function sysSpawn(S,ch){
  if(ch==='x.miss') return;
  const k=S.count[ch], form=CH_FORM[ch];
  const path=chunkPath(S,ch,k);
  S.flights.push({ch,form,path,s:0,len:pathLen(path)});
  if(S.flights.length>400) S.flights.shift();
}
function sysMoveFlights(S,dt){
  for(const f of S.flights) f.s+=CHUNK_V*dt;
  S.flights=S.flights.filter(f=>f.s<f.len);
}
