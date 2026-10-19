#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py, checking every pattern occurs
exactly once in the extracted script (a pattern that matches twice mutates two
places; one that matches none is a mutant you think you ran and did not).

Categories: PhET's constants, the collision algebra, the walls and the lid, the
heater, the hold-constant algorithms, the injection, the exact laws the views
draw, the wall-hit rate (this sim's one falsifiable measurement), the sweep,
and the UI (dirty flags, drags, the frame loop).

The sweep is run against a COPY of the html inside _out/ — never
docs/phets_revised/gases-intro.html in place — because mutate.py writes its
scratch _mutant.js next to the html it tests and parallel agents would share
one docs/phets_revised/_mutant.js.
"""
import io, json, os
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
M = [
    # --- PhET's constants and conversions
    ('BOLTZMANN 8316 -> 8314 (CODATA)', 'K:8316,', 'K:8314,', 'p'),
    ('pressure scale 1.66e6 -> 1.66e5', 'P_SCALE:1.66e6,', 'P_SCALE:1.66e5,', 'p'),
    ('atm per kPa 0.00986923 -> 0.0098692', 'ATM_PER_KPA:0.00986923,', 'ATM_PER_KPA:0.0098692,', 'p'),
    ('heatCool 800 -> 400', 'HEAT_COOL:800,', 'HEAT_COOL:400,', 'p'),
    ('frame 2.5/60 -> 2.5/50 ps', 'DT_FRAME:2.5/60,', 'DT_FRAME:2.5/50,', 'p'),
    ('step button 0.2 -> 0.25 ps', 'STEP:0.2,', 'STEP:0.25,', 'p'),
    ('container height 8750 -> 8700', 'H:8750, D:4000, WALL:75,', 'H:8700, D:4000, WALL:75,', 'p'),
    ('container depth 4000 -> 4500', 'H:8750, D:4000, WALL:75,', 'H:8750, D:4500, WALL:75,', 'p'),
    ('width range 5000-15000 -> 5000-14000', 'WMIN:5000, WMAX:15000, WDEF:10000,', 'WMIN:5000, WMAX:14000, WDEF:10000,', 'p'),
    ('heavy mass 28 -> 27', 'HEAVY:{m:28,r:125}', 'HEAVY:{m:27,r:125}', 'p'),
    ('heavy radius 125 -> 120', 'HEAVY:{m:28,r:125}', 'HEAVY:{m:28,r:120}', 'p'),
    ('light mass 4 -> 3', 'LIGHT:{m:4,r:87.5}', 'LIGHT:{m:3,r:87.5}', 'p'),
    ('entry height H/5 -> H/4', 'ENTRY_Y:8750/5,', 'ENTRY_Y:8750/4,', 'p'),
    ('pump fan pi/2 -> pi/3', 'FAN:Math.PI/2,', 'FAN:Math.PI/3,', 'p'),
    ('maxPressure 2e4 -> 4e4', 'P_MAX:2e4,', 'P_MAX:4e4,', 'p'),
    ('counter periods 5,10,20 -> 5,12,20', 'PERIODS:[5,10,20],', 'PERIODS:[5,12,20],', 'p'),
    # --- PhET's definitions
    ('T = (2/3)<KE>/k -> (1/2)', 'return n?(2/3)*gasEnergy(g,k)/n/GAS.K:null;', 'return n?(1/2)*gasEnergy(g,k)/n/GAS.K:null;', 'p'),
    ('P = NkT/V -> (N+1)kT/V', 'return N*GAS.K*(T||0)/V*GAS.P_SCALE;', 'return (N+1)*GAS.K*(T||0)/V*GAS.P_SCALE;', 'p'),
    ('V = W H D -> W H (D/2)', 'function gasVolume(g){ return g.W*g.H*g.D; }', 'function gasVolume(g){ return g.W*g.H*g.D/2; }', 'p'),
    ('kT2 = (3/2)kT -> kT', 'function gasKT2(T){ return 1.5*GAS.K*T; }', 'function gasKT2(T){ return 1.0*GAS.K*T; }', 'p'),
    # --- the exact laws the views and the tests draw
    ('MB mean speed 2m -> 4m', 'return Math.sqrt(Math.PI*kT2/(2*m));', 'return Math.sqrt(Math.PI*kT2/(4*m));', 'p'),
    ('MB rms 2kT2 -> 3kT2', 'function mbRmsSpeed(m,kT2){ return Math.sqrt(2*kT2/m); }', 'function mbRmsSpeed(m,kT2){ return Math.sqrt(3*kT2/m); }', 'p'),
    ('B2 = pi s^2/2 -> /4', 'function hdB2(s){ return Math.PI*s*s/2; }', 'function hdB2(s){ return Math.PI*s*s/4; }', 'p'),
    ('B3/B2^2 sqrt3 -> sqrt2', 'const HD_B3_RATIO=4/3-Math.sqrt(3)/Math.PI;', 'const HD_B3_RATIO=4/3-Math.sqrt(2)/Math.PI;', 'p'),
    ('contact measure -4s^2 -> -2s^2', 'return 2*Math.PI*s*a*b-4*s*s*(a+b)+2*s*s*s;', 'return 2*Math.PI*s*a*b-2*s*s*(a+b)+2*s*s*s;', 'p'),
    ('contact measure: the corner term +2s^3 dropped', 'return 2*Math.PI*s*a*b-4*s*s*(a+b)+2*s*s*s;', 'return 2*Math.PI*s*a*b-4*s*s*(a+b);', 'p'),
    ('first-order Z (N-1) -> N', 'function hdZ1(N,s,a,b){ return (N-1)*s', 'function hdZ1(N,s,a,b){ return N*s', 'p'),
    ('Z: the 1/(2N) normalisation -> 1/N', 'let z=S/(2*N);', 'let z=S/N;', 'p'),
    # --- THIS sim's measurement: the wall-hit rate
    ('hit rate: <vx+> = sqrt(kT2/2 pi m) -> sqrt(kT2/pi m)',
     "s+=nk/(a*b)*Math.sqrt(gasKT2(T)/(2*Math.PI*masses[k]))*2*(a+b);",
     "s+=nk/(a*b)*Math.sqrt(gasKT2(T)/(Math.PI*masses[k]))*2*(a+b);", 'p'),
    ('hit rate: the perimeter 2(a+b) -> (a+b)',
     "s+=nk/(a*b)*Math.sqrt(gasKT2(T)/(2*Math.PI*masses[k]))*2*(a+b);",
     "s+=nk/(a*b)*Math.sqrt(gasKT2(T)/(2*Math.PI*masses[k]))*(a+b);", 'p'),
    ('hit rate: the excluded strip a = W-2r -> W',
     "const r=radii[k], a=W-2*r, b=Hh-2*r;",
     "const r=radii[k], a=W, b=Hh;", 'p'),
    ('hit rate: Z applied even with collisions off',
     "[g.species[0].m,g.species[1].m],g.W,g.H,g.T,useZ&&g.collisions!==false);",
     "[g.species[0].m,g.species[1].m],g.W,g.H,g.T,useZ);", 'p'),
    ('hit rate: Z dropped altogether',
     "return s*(useZ?hdZ(counts,radii,W,Hh):1);", "return s*1;", 'p'),
    # --- the collision algebra
    ('contact time: the later root', 'return c/(-b+Math.sqrt(d));', 'return c/(-b-Math.sqrt(d));', 'p'),
    ('overlap test c<0 -> c<-1', 'if(c<0) return Infinity;', 'if(c<-1) return Infinity;', 'p'),
    ('impulse: masses swapped', 'const M=mi+mj, ci=2*mj/M*gn, cj=2*mi/M*gn;', 'const M=mi+mj, ci=2*mi/M*gn, cj=2*mj/M*gn;', 'p'),
    ('impulse: half strength', 'g.vx[i]-=ci*nx; g.vy[i]-=ci*ny; g.vx[j]+=cj*nx; g.vy[j]+=cj*ny;',
     'g.vx[i]-=0.5*ci*nx; g.vy[i]-=0.5*ci*ny; g.vx[j]+=0.5*cj*nx; g.vy[j]+=0.5*cj*ny;', 'p'),
    # --- the injection and the heater
    ('injection speed sqrt(3kT/m) -> sqrt(2kT/m)', 'v=Math.sqrt(3*GAS.K*Ts[q]/S.m);', 'v=Math.sqrt(2*GAS.K*Ts[q]/S.m);', 'p'),
    ('injection mean not restored', 'const sh=T-s/n;', 'const sh=0;', 'p'),
    ('a full pump stroke 50 -> 40', 'w.pump.acc+=dh*50;', 'w.pump.acc+=dh*40;', 'u'),
    ('the heater: the per-frame exponent doubled',
     'const s=Math.pow(1+g.heat/GAS.HEAT_COOL,h/GAS.DT_FRAME);',
     'const s=Math.pow(1+g.heat/GAS.HEAT_COOL,2*h/GAS.DT_FRAME);', 'p'),
    ('the heater: the exponent dropped (one factor per SUBSTEP)',
     'const s=Math.pow(1+g.heat/GAS.HEAT_COOL,h/GAS.DT_FRAME);',
     'const s=1+g.heat/GAS.HEAT_COOL;', 'p'),
    # --- the hold-constant algorithms
    ('hold P by V: w = NkT/(P H D) -> NkT/(P H)',
     'let w=+(N*GAS.K*T/Pm/(g.H*g.D)).toFixed(5);', 'let w=+(N*GAS.K*T/Pm/(g.H)).toFixed(5);', 'p'),
    ('hold P by V: the 5-decimal rounding -> 1 decimal',
     'let w=+(N*GAS.K*T/Pm/(g.H*g.D)).toFixed(5);', 'let w=+(N*GAS.K*T/Pm/(g.H*g.D)).toFixed(1);', 'p'),
    ('hold P by T: T = PV/Nk -> PV/(2Nk)',
     'gasSetTemp(g,(g.P/GAS.P_SCALE)*gasVolume(g)/(N*GAS.K));',
     'gasSetTemp(g,(g.P/GAS.P_SCALE)*gasVolume(g)/(2*N*GAS.K));', 'p'),
    ('hold T: the restore after a removal deleted',
     "} else if(g.hold==='temperature'&&Tbefore!==null) gasSetTemp(g,Tbefore);",
     "} else if(false&&g.hold==='temperature'&&Tbefore!==null) gasSetTemp(g,Tbefore);", 'p'),
    ('hold T allowed with the lid open',
     "if(mode==='temperature') return gasCount(g)>0&&!gasLidOpen(g);",
     "if(mode==='temperature') return gasCount(g)>0;", 'p'),
    ('setTemperature: sqrt(f) -> f', 'const E=gasEnergy(g), f=1.5*T*GAS.K/(E/N), s=Math.sqrt(f);',
     'const E=gasEnergy(g), f=1.5*T*GAS.K/(E/N), s=f;', 'p'),
    ('the Ideal wall stops redistributing (disks left outside the new wall)',
     'if(redistribute) for(let i=0;i<g.n;i++) if(!g.out[i]){',
     'if(false) for(let i=0;i<g.n;i++) if(!g.out[i]){', 'p'),
    # --- the lid and the gauge
    ('lid blow-off gap 1500 -> 3000', 'LID_WIDE:1500,', 'LID_WIDE:3000,', 'p'),
    ('gauge refresh 0.75 -> 1.5 ps', 'P_REFRESH:0.75,', 'P_REFRESH:1.5,', 'p'),
    # --- the sweep
    ('sweep: Boyle plotted against V but exact against 2V',
     "if(S.law==='boyle')   return gasPressureOf(S.N0,S.T0,x*1e9);",
     "if(S.law==='boyle')   return gasPressureOf(S.N0,S.T0,2*x*1e9);", 'p'),
    ('sweep: Charles exact V = NkT/P -> 2NkT/P',
     "if(S.law==='charles') return S.N0*GAS.K*x/(S.P0/GAS.P_SCALE)/1e9;",
     "if(S.law==='charles') return 2*S.N0*GAS.K*x/(S.P0/GAS.P_SCALE)/1e9;", 'p'),
    ('sweep: Avogadro exact T = PV/Nk -> PV/(N k)/2',
     "return (S.P0/GAS.P_SCALE)*V0/(x*GAS.K);",
     "return (S.P0/GAS.P_SCALE)*V0/(x*GAS.K)/2;", 'p'),
    ('sweep: the settle skipped (measure a clump)', 'const SWEEP_SETTLE=48,', 'const SWEEP_SETTLE=0,', 'p'),
    ('sweep: the measurement window halved', 'measure:Math.round(st.sWin/FRAME_DT),', 'measure:Math.round(st.sWin/FRAME_DT/2),', 'p'),
    ('sweep: the hit rate divided by the wrong time', 'const rate=S.ht>0?S.hits/S.ht:null;', 'const rate=S.ht>0?S.hits/(2*S.ht):null;', 'p'),
    ('sweep: Avogadro uses the pump again (a clump, not a gas)',
     "else { gasSetHold(g,'pressureT'); sweepSetCount(g,v,g.T); }",
     "else { gasSetHold(g,'pressureT'); gasSetCount(g,0,v); }", 'p'),
    ('sweep: Charles targets not kept inside the container',
     "return [0,1,2,3,4].map(i=>clamp(Tlo+(Thi-Tlo)*i/4,Tlo*(1+1e-9),Thi*(1-1e-9)));",
     "return [0,1,2,3,4].map(i=>Tlo+(Thi-Tlo)*i/4);", 'p'),
    # --- the drawing layer the tests read
    ('the P-V isotherm built at 2T', 'ys.push(gasPressureOf(N,T,V*1e9)); }', 'ys.push(gasPressureOf(N,2*T,V*1e9)); }', 'p'),
    ('the P-V isotherm: V in nm³ used as pm³', 'ys.push(gasPressureOf(N,T,V*1e9)); }', 'ys.push(gasPressureOf(N,T,V)); }', 'p'),
    ('the P-V isotherm samples the wrong V range', 'const V=V0+(V1-V0)*i/n; xs.push(V);', 'const V=V0+(V1-V0)*i/(2*n); xs.push(V);', 'p'),
    ('the caption clears the #hint by 18 px -> 0', 'const HINT_H=18;', 'const HINT_H=0;', 'p'),
    ('the lone trace point is not re-seeded after a paused edit',
     'if(M.w.trace.length===1&&M.g.t===0){ M.w.trace.length=0; traceRecord(M.w); }',
     'if(false){ M.w.trace.length=0; traceRecord(M.w); }', 'p'),
    ('the P-V isotherm label falls back to the wrong side',
     'const right=li>xs.length*0.85;', 'const right=false;', 'p'),
    # --- the UI
    ('drag: the pointer handler stops dirtying the canvas',
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }",
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); }", 'u'),
    ('drag: a move no longer dirties',
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; syncCounts(); roEl.innerHTML=readoutHTML(S.model()); }",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ syncCounts(); roEl.innerHTML=readoutHTML(S.model()); }", 'u'),
    ('drag: the wall follows the pointer to 100 pm, not 10',
     "w.dragW=clamp(Math.round(-G.wx(x-DRAG.off)/10)*10,g.wRange[0],g.wRange[1]); return true;",
     "w.dragW=clamp(Math.round(-G.wx(x-DRAG.off)/100)*100,g.wRange[0],g.wRange[1]); return true;", 'u'),
    ('drag: the Ideal screen is no longer paused while the wall is held',
     "if(w.view!=='sweep'&&w.dragW!==null) return false;   /* PhET pauses while the wall is dragged */",
     "if(false) return false;", 'u'),
    ('drag: the wall does work on release (no redistribute)',
     "gasResize(g,w.dragW,true); w.dragW=null; g.counter.on=false; gasRefresh(g);",
     "gasResize(g,w.dragW,false); w.dragW=null; g.counter.on=false; gasRefresh(g);", 'u'),
    ('the heater no longer springs back', "gHeat.appendChild(slider('heat','cool ← → heat',-1,1,0.01,v=>(v>0?'+':'')+fmt(v,2),null,()=>{ st.heat=0; }));",
     "gHeat.appendChild(slider('heat','cool ← → heat',-1,1,0.01,v=>(v>0?'+':'')+fmt(v,2),null,()=>{}));", 'u'),
    ('the Intro screen grows a Hold Constant panel',
     "gPart.hidden=sweepV; gHold.hidden=!(v==='laws'||v==='pv'); gHeat.hidden=sweepV;",
     "gPart.hidden=sweepV; gHold.hidden=false; gHeat.hidden=sweepV;", 'u'),
    ('the P-V view stops sharing the Laws gas',
     "function worldKey(view){ return view==='pv'?'laws':view; }",
     "function worldKey(view){ return view; }", 'u'),
    ('the step key steps 0.2 -> 0.4 ps',
     "S.stepOnce=function(){ const w=worldOf(ST.view); worldStep(w,ST,GAS.STEP); if(S.onCounts) S.onCounts(); };",
     "S.stepOnce=function(){ const w=worldOf(ST.view); worldStep(w,ST,2*GAS.STEP); if(S.onCounts) S.onCounts(); };", 'u'),
    ('the frame loop stops honouring the dirty flag',
     "if(advanced||dirty){", "if(advanced){", 'u'),
]
seen = {}
bad = []
for label, old, new, suite in M:
    n = js.count(old)
    if n != 1:
        bad.append('%s: pattern matches %d times' % (label, n))
    if old == new:
        bad.append('%s: no-op mutant' % label)
    seen.setdefault(old, []).append(label)
for old, labels in seen.items():
    if len(labels) > 1 and len(set(labels)) != len(labels):
        bad.append('duplicate label on %s' % old[:40])
if bad:
    raise SystemExit('\n'.join(bad))
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps([list(m) for m in M], indent=1, ensure_ascii=False) + '\n')
print('%d mutants (%d physics, %d UI)' % (len(M), sum(1 for m in M if m[3] == 'p'),
                                          sum(1 for m in M if m[3] == 'u')))
