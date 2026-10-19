#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py, asserting that every pattern occurs
EXACTLY once in the assembled script (a pattern that matches twice mutates two
places; one that matches nothing is a mutant you think you ran and did not).
Run the sweep on the COPY in _out/, never on docs/phets_revised/<stem>.html:
  python3 <sims>/tools/mutate.py _out/energy-forms-and-changes.html mutants.json ui_drive_energy-forms-and-changes.js"""
import io, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
M = [
 # ---- PhET's constants: every leading coefficient and unit
 ['room temperature 297 K', "const T_ROOM=296;", "const T_ROOM=297;", 'p'],
 ['freezing at 273.0 K', "const T_FREEZE=273.15;", "const T_FREEZE=273.0;", 'p'],
 ['water boils at 372.15 K', "const T_BOIL={water:373.15, oil:573.15};", "const T_BOIL={water:372.15, oil:573.15};", 'p'],
 ['oil boils at 563.15 K', "const T_BOIL={water:373.15, oil:573.15};", "const T_BOIL={water:373.15, oil:563.15};", 'p'],
 ['blocks capped at 600 K', "const T_BLOCK_MAX=620;", "const T_BLOCK_MAX=600;", 'p'],
 ['iron c 460', "iron:{c:450,rho:7800}, brick:{c:840", "iron:{c:460,rho:7800}, brick:{c:840", 'p'],
 ['iron rho 7900', "iron:{c:450,rho:7800}, brick:{c:840", "iron:{c:450,rho:7900}, brick:{c:840", 'p'],
 ['brick c 850', "brick:{c:840,rho:3300}", "brick:{c:850,rho:3300}", 'p'],
 ['brick rho 3200', "brick:{c:840,rho:3300}", "brick:{c:840,rho:3200}", 'p'],
 ['water c 3100', "water:{c:3000,rho:1000}", "water:{c:3100,rho:1000}", 'p'],
 ['water rho 1010', "water:{c:3000,rho:1000}", "water:{c:3000,rho:1010}", 'p'],
 ['oil c 1400', "oil:{c:1411,rho:916}", "oil:{c:1400,rho:916}", 'p'],
 ['oil rho 920', "oil:{c:1411,rho:916}", "oil:{c:1411,rho:920}", 'p'],
 ['block 4.6 cm', "const BLOCK=0.045;", "const BLOCK=0.046;", 'p'],
 ['beaker 8.6 cm across', "const BEAKER_W=0.085, BEAKER_H=0.085*1.1;", "const BEAKER_W=0.086, BEAKER_H=0.085*1.1;", 'p'],
 ['beaker 1.2x tall', "const BEAKER_W=0.085, BEAKER_H=0.085*1.1;", "const BEAKER_W=0.085, BEAKER_H=0.085*1.2;", 'p'],
 ['beakers 55 % full', "const FLUID0=0.5;", "const FLUID0=0.55;", 'p'],
 ['displacement 100 per m^2', "const DISPLACE=120;", "const DISPLACE=100;", 'p'],
 ['body-body k 900', "const K_BODY=1000, K_AIR=30;", "const K_BODY=900, K_AIR=30;", 'p'],
 ['body-room k 25', "const K_BODY=1000, K_AIR=30;", "const K_BODY=1000, K_AIR=25;", 'p'],
 ['substeps of 1/50 s', "const MAXSTEP=1/60;", "const MAXSTEP=1/50;", 'p'],
 ['equal-temperature threshold 1e-3', "const EQ_THRESH=1e-6;", "const EQ_THRESH=1e-3;", 'p'],
 ['burner 4 kW into a body', "const P_BURN=5e3, P_BURN_AIR=1500;", "const P_BURN=4e3, P_BURN_AIR=1500;", 'p'],
 ['burner 1.4 kW into the room', "const P_BURN=5e3, P_BURN_AIR=1500;", "const P_BURN=5e3, P_BURN_AIR=1400;", 'p'],
 ['burner contact half-width 3 cm', "const BURNER_HALF=0.0375, BURNER_TOP=0.075;", "const BURNER_HALF=0.03, BURNER_TOP=0.075;", 'p'],
 ['burner 7 cm tall', "const BURNER_HALF=0.0375, BURNER_TOP=0.075;", "const BURNER_HALF=0.0375, BURNER_TOP=0.07;", 'p'],
 ['the air box 0.6 m wide', "const AIR_W=0.7, AIR_H=0.85;", "const AIR_W=0.6, AIR_H=0.85;", 'p'],
 ['10-kW rate 9 kW', "const MAXP=1e4;", "const MAXP=9e3;", 'p'],
 ['iron molar mass 55.85 (unit)', "const JANAF_FE_CP=25.094, M_FE=55.845;", "const JANAF_FE_CP=25.094, M_FE=55.85;", 'p'],
 ['real iron c per gram, not per kg', "iron:{c:JANAF_FE_CP/M_FE*1000,rho:7874}", "iron:{c:JANAF_FE_CP/M_FE*100,rho:7874}", 'p'],
 ['real water c 4186', "water:{c:4182.32,rho:997.577}", "water:{c:4186,rho:997.577}", 'p'],
 ['real brick rho 1920', "brick:{c:840,rho:1900}", "brick:{c:840,rho:1920}", 'p'],
 ['real oil c 1900', "oil:{c:1970,rho:911}", "oil:{c:1900,rho:911}", 'p'],
 # ---- the chunk map and its rounding
 ['EPC from Fb(3) - Fb(1)', "const EPC=fChunks(2)-fChunks(1);", "const EPC=fChunks(3)-fChunks(1);", 'p'],
 ['brick at 0 C is 1.3 chunks', "function gChunks(E){ return linearMap(QB,ZB,1.25,2.4,E); }", "function gChunks(E){ return linearMap(QB,ZB,1.3,2.4,E); }", 'p'],
 ['QB at 273 K', "const QB=3300*Math.pow(0.045,3)*840*273.15,", "const QB=3300*Math.pow(0.045,3)*840*273,", 'p'],
 ['roundSymmetric rounds 0.4 up', "function roundSym(v){ const a=Math.floor(Math.abs(v)+0.5);", "function roundSym(v){ const a=Math.floor(Math.abs(v)+0.6);", 'p'],
 ['spots divide by 6', "const SPOT_GAP=(0.568-0.085)/(6-1);", "const SPOT_GAP=(0.568-0.085)/6;", 'p'],
 # ---- contact, exchange, room, burner (signs and forms)
 ['immersed contact loses a side', "      n=2*rw+2*rh;", "      n=2*rw+rh;", 'p'],
 ['straddling: no dry side subtracted', "      if(rw!==(a.x1-a.x0)&&rw!==(b.x1-b.x0)) n-=rh;\n", "\n", 'p'],
 ['partly wet: no dry top subtracted', "      if(rh!==(a.y1-a.y0)&&rh!==(b.y1-b.y0)) n-=rw;\n", "\n", 'p'],
 ['stacked contact uses the y overlap', ")||Math.abs(a.x0-b.x1)<0.001) n=ox;", ")||Math.abs(a.x0-b.x1)<0.001) n=oy;", 'p'],
 ['heat flows up the gradient', "      const q=(bodyT(b)-bodyT(a))*L*K_BODY*h;", "      const q=(bodyT(a)-bodyT(b))*L*K_BODY*h;", 'p'],
 ['the exchange creates energy', "      b.E-=q; a.E+=q; tot+=-q;", "      b.E+=q; a.E+=q; tot+=-q;", 'p'],
 ['the room heats hot bodies', "i+=(bodyT(b)-T_AIR)*L*K_AIR*h; }", "i+=(T_AIR-bodyT(b))*L*K_AIR*h; }", 'p'],
 ['energy past the cap stays', "    if(i>=0) i=Math.max(i,bodyBeyond(b));\n", "\n", 'p'],
 ['a beaker is not capped at boiling', "function bodyT(b){ const t=b.E/(b.m*b.c); return b.kind==='beaker'?Math.min(t,T_BOIL[b.mat]):t; }",
  "function bodyT(b){ const t=b.E/(b.m*b.c); return t; }", 'p'],
 ['the 0-C gate lets heat in at 0 C', "        if(bodyT(b)>T_FREEZE){ q=P_BURN*l*dt;", "        if(bodyT(b)>=T_FREEZE){ q=P_BURN*l*dt;", 'p'],
 ['cooling not clamped at 0 C', "if(l<0&&Math.abs(q)>b.E-bodyMinE(b)) q=-(b.E-bodyMinE(b)); }", "}", 'p'],
 ['an empty burner heats nothing in the room', "const q=P_BURN_AIR*l*dt; work+=q; room+=q;", "const q=P_BURN_AIR*l*dt; work+=q;", 'p'],
 ['no displacement cap (equivalent)', "    bk.f=Math.min(FLUID0+DISPLACE*area,1);", "    bk.f=FLUID0+DISPLACE*area;", 'p'],
 ['immersed blocks also lose to the room', "  bodies.forEach((b,i)=>{\n    if(isImmersed(bodies,b)) return;\n", "  bodies.forEach((b,i)=>{\n", 'p'],
 ['a block sits on a beaker’s rim', "b.y=prev===null?y0:(prev.kind==='beaker'?prev.y+0.001:prev.y+prev.h);", "b.y=prev===null?y0:(prev.kind==='beaker'?prev.y+prev.h:prev.y+prev.h);", 'p'],
 ['beakers stack on beakers', "  return !(gb&&cb);\n}", "  return true;\n}", 'p'],
 # ---- the chunk rule
 ['a link carries a chunk at 2 EPC', "    if(L.B>EPC){ if(!(isBodyRef(L.a)&&B.own[L.a]<=1))", "    if(L.B>2*EPC){ if(!(isBodyRef(L.a)&&B.own[L.a]<=1))", 'p'],
 ['the correction waits for 1.5 chunks', "      if(dev>=1||dev<=-1){ bad=true; benchCorrect(B,i,dev>0,lev,keys); }", "      if(dev>=1.5||dev<=-1.5){ bad=true; benchCorrect(B,i,dev>0,lev,keys); }", 'p'],
 ['a correction moves half a chunk of balance', "  if(excess){ benchGive(B,i,p,kind); if(L.a===i) L.B-=EPC; else L.B+=EPC; }", "  if(excess){ benchGive(B,i,p,kind); if(L.a===i) L.B-=EPC/2; else L.B+=EPC/2; }", 'p'],
 ['a threshold transfer keeps its balance', "benchGive(B,L.a,L.b,moveKind(L.a,L.b)); L.B-=EPC; } }", "benchGive(B,L.a,L.b,moveKind(L.a,L.b)); } }", 'p'],
 # ---- the Systems screen
 ['five chunks in six becomes four in five', "const BIKE_MECH=5/6;", "const BIKE_MECH=4/5;", 'p'],
 ['no-load food rate MAXP/4', "const BIKE_LOAD=MAXP, BIKE_FREE=MAXP/5;", "const BIKE_LOAD=MAXP, BIKE_FREE=MAXP/4;", 'p'],
 ['crank top speed 2 pi', "const OMEGA_MAX=3*Math.PI;", "const OMEGA_MAX=2*Math.PI;", 'p'],
 ['crank accelerates at pi', "const CRANK_ACC=Math.PI/2;", "const CRANK_ACC=Math.PI;", 'p'],
 ['20 chunks of food', "const FOOD_CHUNKS=21;", "const FOOD_CHUNKS=20;", 'p'],
 ['water falls for 0.5 s', "const FALL_STEPS=24;", "const FALL_STEPS=30;", 'p'],
 ['kettle time constant 8 s', "const TAU_K=10;", "const TAU_K=8;", 'p'],
 ['75 % of the heat to steam', "const STEAM=0.8;", "const STEAM=0.75;", 'p'],
 ['the kettle cut at 60 W', "const KETTLE_CUT=30;", "const KETTLE_CUT=60;", 'p'],
 ['wheel radius 0.04 m', "const GEN_R=0.039;", "const GEN_R=0.04;", 'p'],
 ['wheel lag 2 s', "const TAU_W=5/3;", "const TAU_W=2;", 'p'],
 ['wheel damping 2, not 3', "const ETA_W=(GEN_R*0.5*(1/60)/3)*MAXP/(Math.PI/2);", "const ETA_W=(GEN_R*0.5*(1/60)/2)*MAXP/(Math.PI/2);", 'p'],
 ['panel 70 %', "const ETA_PANEL=0.68;", "const ETA_PANEL=0.7;", 'p'],
 ['heater 4 kW into the water', "const HEAT_MAXP=5e3, HEAT_RAMP=0.5;", "const HEAT_MAXP=4e3, HEAT_RAMP=0.5;", 'p'],
 ['heater ramps at 1/s', "const HEAT_MAXP=5e3, HEAT_RAMP=0.5;", "const HEAT_MAXP=5e3, HEAT_RAMP=1;", 'p'],
 ['heater beaker 8 cm across', "const HB_W=0.075, HB_H=0.0825;", "const HB_W=0.08, HB_H=0.0825;", 'p'],
 ['heater loses from its whole height', "const HB_L=2*HB_W+2*HB_H*FLUID0;", "const HB_L=2*HB_W+2*HB_H;", 'p'],
 ['incandescent 60 % light', "const LIGHT_FRAC={incandescent:0.65, fluorescent:0.8};", "const LIGHT_FRAC={incandescent:0.6, fluorescent:0.8};", 'p'],
 ['fluorescent 75 % light', "const LIGHT_FRAC={incandescent:0.65, fluorescent:0.8};", "const LIGHT_FRAC={incandescent:0.65, fluorescent:0.75};", 'p'],
 ['fan 0.005 rad/s per W', "const FAN_W=0.0051, FAN_MIN=4, FAN_ACC=4*Math.PI;", "const FAN_W=0.005, FAN_MIN=4, FAN_ACC=4*Math.PI;", 'p'],
 ['fan stalls below 40 rad/s', "const FAN_W=0.0051, FAN_MIN=4, FAN_ACC=4*Math.PI;", "const FAN_W=0.0051, FAN_MIN=40, FAN_ACC=4*Math.PI;", 'p'],
 ['fan spins up at 2 pi', "const FAN_W=0.0051, FAN_MIN=4, FAN_ACC=4*Math.PI;", "const FAN_W=0.0051, FAN_MIN=4, FAN_ACC=2*Math.PI;", 'p'],
 ['fan heat 1/12', "const FAN_HEAT=1/14;", "const FAN_HEAT=1/12;", 'p'],
 ['sun floor 0.2', "function sunFrac(c){ const i=1-c; return i===0?0:0.1+0.9*i; }", "function sunFrac(c){ const i=1-c; return i===0?0:0.2+0.8*i; }", 'p'],
 ['full cloud still lets 10 % through', "function sunFrac(c){ const i=1-c; return i===0?0:0.1+0.9*i; }", "function sunFrac(c){ const i=1-c; return 0.1+0.9*i; }", 'p'],
 ['chunks move at 5 cm/s', "const CHUNK_V=0.04;", "const CHUNK_V=0.05;", 'p'],
 ['the teapot loses nothing round the kettle', "    const Ek=STEAM*Ein; let El=Ein-Ek;", "    const Ek=Ein; let El=Ein-Ek;", 'p'],
 ['the wheel releases twice as fast', "      const Er=S.wheel*dt/TAU_W; S.wheel-=Er;", "      const Er=2*S.wheel*dt/TAU_W; S.wheel-=Er;", 'p'],
 ['the heater: the room warms hot water', "    if(Math.abs(s)>EQ_THRESH){ Ea=s*K_AIR*HB_L*dt; S.water-=Ea; }", "    if(Math.abs(s)>EQ_THRESH){ Ea=s*K_AIR*HB_L*dt; S.water+=Ea; }", 'p'],
 ['the heater keeps water past boiling', "    const Eb=Math.max(S.water-T_BOIL.water*HB_C,0); S.water-=Eb;", "    const Eb=0; S.water-=Eb;", 'p'],
 ['a swap forgets the wheel', "    if(S.conv==='generator'){ sysDump(S,S.wheel); S.wheel=0; S.wOmega=0; }", "    if(S.conv==='generator'){ S.wheel=0; S.wOmega=0; }", 'p'],
 ['feeding is not logged', "function sysFeed(S){ if(S.food>=FOOD0) return false; S.inp.fed+=FOOD0-S.food; S.food=FOOD0; return true; }",
  "function sysFeed(S){ if(S.food>=FOOD0) return false; S.food=FOOD0; return true; }", 'p'],
 ['the rider burns food he does not have', "    const Ec=Math.min(pchem*dt,S.food);", "    const Ec=pchem*dt;", 'p'],
 # ---- equilibrium: the exact solution and its conductances
 ['expm2 with sinh for cosh', "const q=Math.sqrt(Math.max(q2,0)), e=Math.exp(s*t), ch=Math.cosh(q*t);", "const q=Math.sqrt(Math.max(q2,0)), e=Math.exp(s*t), ch=Math.sinh(q*t);", 'p'],
 ['expm2 drops the -sI', "  return [[e*(ch+sh*(M[0][0]-s)),e*sh*M[0][1]],", "  return [[e*(ch+sh*(M[0][0])),e*sh*M[0][1]],", 'p'],
 ['an immersed block loses to the room', "const a1=air&&!imm?K_AIR*contactLen(AIR_AREA,bodyArea(a)):0", "const a1=air?K_AIR*contactLen(AIR_AREA,bodyArea(a)):0", 'p'],
 ['T_eq unweighted', "  const Teq=(C1*T1+C2*T2)/(C1+C2);\n  const Tss", "  const Teq=(T1+T2)/2;\n  const Tss", 'p'],
 ['the window 6 fast times', "function eqWindow(L){ const ev=eqEigen(L.M), fast=-1/ev[1]; return Math.min(Math.max(8*fast,4),60); }",
  "function eqWindow(L){ const ev=eqEigen(L.M), fast=-1/ev[1]; return Math.min(Math.max(6*fast,4),60); }", 'p'],
 # ---- the UI: dirty flags, handlers, visibility, resets
 ['pointer-move skips the dirty flag', "    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;", "    if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ ", 'u'],
 ['pointer-down skips the dirty flag', "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }",
  "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); }", 'u'],
 ['the lever drives the wrong burner', "if(ST.link){ ST.lev0=l; ST.lev1=l; } else if(DRAG.k===0) ST.lev0=l; else ST.lev1=l;", "if(ST.link){ ST.lev0=l; ST.lev1=l; } else if(DRAG.k===0) ST.lev1=l; else ST.lev0=l;", 'u'],
 ['a held body ignores its grab offset', "  H.x=clamp(x+H.dx,BENCH_XLIM[0],BENCH_XLIM[1]); H.y=clamp(y+H.dy,0,BENCH_YMAX);", "  H.x=clamp(x,BENCH_XLIM[0],BENCH_XLIM[1]); H.y=clamp(y,0,BENCH_YMAX);", 'p'],
 ['a dropped thermometer does not stick', "if(inPoly(blockHex(b),p.x,p.y)){ th.att={i,dx:p.x-b.x,dy:p.y-b.y}; return i; } }", "if(inPoly(blockHex(b),p.x,p.y)){ return i; } }", 'u'],
 ['the pedalling slider always shows', "rows.pedal.row.hidden=st.src!=='biker';", "rows.pedal.row.hidden=false;", 'u'],
 ['feed me never shows', "    feedRow.hidden=!(st.src==='biker'&&SYS.food<=0);", "    feedRow.hidden=true;", 'u'],
 ['time runs while paused', "    if(!ST.running) return false;\n", "\n", 'u'],
 ['fast forward is x2', "  B.acc+=dtWall*(st.speed==='fast'?SPEED_FAST:1);", "  B.acc+=dtWall*(st.speed==='fast'?2:1);", 'u'],
 ['reset all leaves the bench', "  benchReset(BENCH); sysReset(SYS,ST); DRAG.what=null; DRAG.k=null;", "  sysReset(SYS,ST); DRAG.what=null; DRAG.k=null;", 'u'],
 ['the energy-symbols box is ignored', "  const held=B.held?B.held.group[0]:-1, sz=clamp(0.0095*map.s,7,13), sym=M.st.symBench, inb=inboundOf(B);",
  "  const held=B.held?B.held.group[0]:-1, sz=clamp(0.0095*map.s,7,13), sym=true, inb=inboundOf(B);", 'u'],
 ['the left slider ignores the link', "slider('lev0','left burner',-1,1,0.01,levFmt,()=>{ if(st.link) st.lev1=st.lev0; })", "slider('lev0','left burner',-1,1,0.01,levFmt,()=>{})", 'u'],
 ['the right slider ignores the link', "slider('lev1','right burner',-1,1,0.01,levFmt,()=>{ if(st.link) st.lev0=st.lev1; })", "slider('lev1','right burner',-1,1,0.01,levFmt,()=>{})", 'u'],
 ['the link box does not align the levers', "checkbox('link','link heaters',()=>{ if(st.link) st.lev1=st.lev0; })", "checkbox('link','link heaters',()=>{})", 'u'],
 ['a linked lever drag moves one burner', "if(ST.link){ ST.lev0=l; ST.lev1=l; } else if(DRAG.k===0)", "if(ST.link){ ST.lev0=l; } else if(DRAG.k===0)", 'u'],
]
bad = []
for lab, old, new, suite in M:
    n = js.count(old)
    if n != 1:
        bad.append((lab, n))
if bad:
    for lab, n in bad:
        print('PATTERN COUNT %d: %s' % (n, lab))
    sys.exit(1)
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, ensure_ascii=False, indent=1))
print('%d mutants (%d physics, %d UI) written' % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
