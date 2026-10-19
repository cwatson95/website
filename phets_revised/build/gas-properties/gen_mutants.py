#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py, checking every pattern occurs exactly
once in the extracted script (a pattern that matches twice mutates two places;
one that matches none is a mutant you think you ran and did not).
Categories: PhET's constants, the collision algebra, the walls and the lid,
the heater, the hold-constant algorithms, the injection, the statistics, the
exact laws the views draw, the ledgers, and the UI (dirty flags, drags)."""
import io, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
M = [
    # --- PhET's constants and conversions
    ('BOLTZMANN 8316 -> 8314 (CODATA)', 'K:8316,', 'K:8314,', 'p'),
    ('pressure scale 1.66e6 -> 1.66e5', 'P_SCALE:1.66e6,', 'P_SCALE:1.66e5,', 'p'),
    ('atm per kPa 0.00986923 -> 0.0098692', 'ATM_PER_KPA:0.00986923,', 'ATM_PER_KPA:0.0098692,', 'p'),
    ('heatCool 800 -> 400', 'HEAT_COOL:800,', 'HEAT_COOL:400,', 'p'),
    ('frame 2.5/60 -> 2.5/50 ps', 'DT_FRAME:2.5/60,', 'DT_FRAME:2.5/50,', 'p'),
    ('entry height H/5 -> H/4', 'ENTRY_Y:8750/5,', 'ENTRY_Y:8750/4,', 'p'),
    ('pump fan pi/2 -> pi/3', 'FAN:Math.PI/2,', 'FAN:Math.PI/3,', 'p'),
    ('lid opening inset 1250 -> 1200', 'OPEN_L:1250,', 'OPEN_L:1200,', 'p'),
    ('maxPressure 2e4 -> 4e4', 'P_MAX:2e4,', 'P_MAX:4e4,', 'p'),
    # --- the random stream and the injection
    ('mulberry32 increment', 'a=(a+0x6D2B79F5)>>>0;', 'a=(a+0x6D2B79F4)>>>0;', 'p'),
    ('Box-Muller cos -> sin', 'Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2)', 'Math.sqrt(-2*Math.log(u1))*Math.sin(2*Math.PI*u2)', 'p'),
    ('injection spread 0.2T -> 0.25T', 'const v=T+0.2*T*g.rng.gauss();', 'const v=T+0.25*T*g.rng.gauss();', 'p'),
    ('injection mean not restored', 'const sh=T-s/n;', 'const sh=0;', 'p'),
    ('injection speed sqrt(3kT/m) -> sqrt(2kT/m)', 'v=Math.sqrt(3*GAS.K*Ts[q]/S.m);', 'v=Math.sqrt(2*GAS.K*Ts[q]/S.m);', 'p'),
    ('injection fan centred on pi -> pi/2', 'const th=Math.PI-GAS.FAN/2+g.rng.next()*GAS.FAN,', 'const th=Math.PI/2-GAS.FAN/2+g.rng.next()*GAS.FAN,', 'p'),
    # --- PhET's definitions
    ('T = (2/3)<KE>/k -> (1/2)', 'return n?(2/3)*gasEnergy(g,k)/n/GAS.K:null;', 'return n?(1/2)*gasEnergy(g,k)/n/GAS.K:null;', 'p'),
    ('P = NkT/V -> (N+1)kT/V', 'return N*GAS.K*(T||0)/V*GAS.P_SCALE;', 'return (N+1)*GAS.K*(T||0)/V*GAS.P_SCALE;', 'p'),
    ('kT2 = (3/2)kT -> kT', 'function gasKT2(T){ return 1.5*GAS.K*T; }', 'function gasKT2(T){ return 1.0*GAS.K*T; }', 'p'),
    # --- the exact laws the views draw
    ('MB mean speed 2m -> 4m', 'return Math.sqrt(Math.PI*kT2/(2*m));', 'return Math.sqrt(Math.PI*kT2/(4*m));', 'p'),
    ('MB speed cdf 2kT2 -> 3kT2', 'return v<=0?0:-Math.expm1(-m*v*v/(2*kT2));', 'return v<=0?0:-Math.expm1(-m*v*v/(3*kT2));', 'p'),
    ('finite-N law N-1 -> N-2', 'return -Math.expm1((N-1)*Math.log1p(-e/E));', 'return -Math.expm1((N-2)*Math.log1p(-e/E));', 'p'),
    ('B2 = pi s^2/2 -> /4', 'function hdB2(s){ return Math.PI*s*s/2; }', 'function hdB2(s){ return Math.PI*s*s/4; }', 'p'),
    ('B3/B2^2 sqrt3 -> sqrt2', 'const HD_B3_RATIO=4/3-Math.sqrt(3)/Math.PI;', 'const HD_B3_RATIO=4/3-Math.sqrt(2)/Math.PI;', 'p'),
    ('contact measure -4s^2 -> -2s^2', 'return 2*Math.PI*s*a*b-4*s*s*(a+b)+2*s*s*s;', 'return 2*Math.PI*s*a*b-2*s*s*(a+b)+2*s*s*s;', 'p'),
    ('first-order Z (N-1) -> N', 'function hdZ1(N,s,a,b){ return (N-1)*s', 'function hdZ1(N,s,a,b){ return N*s', 'p'),
    ('hard-disk adiabat W-2r -> W-r', 'const f=W=>hdZ(counts,radii,W,H)/(W-2*rb), hstep=(W0-W1)/n;', 'const f=W=>hdZ(counts,radii,W,H)/(W-rb), hstep=(W0-W1)/n;', 'p'),
    ('sound speed 2kT2/m -> kT2/m', 'function gasSound(kT2,mMean){ return Math.sqrt(2*kT2/mMean); }', 'function gasSound(kT2,mMean){ return Math.sqrt(kT2/mMean); }', 'p'),
    # --- the collision algebra
    ('contact time: the later root', 'return c/(-b+Math.sqrt(d));', 'return c/(-b-Math.sqrt(d));', 'p'),
    ('contact test b>=0 -> b>0 (b = 0 is unobservable: expected equivalent)', 'if(b>=0) return Infinity;', 'if(b>0) return Infinity;', 'p'),
    ('contact test deleted: separating pairs get past roots', 'if(b>=0) return Infinity;', '', 'p'),
    ('overlap test c<0 -> c<-1', 'if(c<0) return Infinity;', 'if(c<-1) return Infinity;', 'p'),
    ('impulse: masses swapped', 'const M=mi+mj, ci=2*mj/M*gn, cj=2*mi/M*gn;', 'const M=mi+mj, ci=2*mi/M*gn, cj=2*mj/M*gn;', 'p'),
    ('impulse: half strength', 'g.vx[i]-=ci*nx; g.vy[i]-=ci*ny; g.vx[j]+=cj*nx; g.vy[j]+=cj*ny;', 'g.vx[i]-=0.5*ci*nx; g.vy[i]-=0.5*ci*ny; g.vx[j]+=0.5*cj*nx; g.vy[j]+=0.5*cj*ny;', 'p'),
    ('pair virial sign', 'return -mi*ci*d;', 'return mi*ci*d;', 'p'),
    ('stale events processed (owner stamp ignored)', 'if(g.st[i]!==EVH.si[e]||g.out[i]){ g.stats.stale++; continue; }', 'if(g.out[i]){ g.stats.stale++; continue; }', 'p'),
    ('pair events: partner stamp ignored', 'if(kind===EV_PAIR&&(g.st[j]!==EVH.sj[e]||g.out[j])){ g.stats.stale++; continue; }', 'if(kind===EV_PAIR&&g.out[j]){ g.stats.stale++; continue; }', 'p'),
    ('opening prediction pushes every pair twice', 'if((half?j<=i:j===i)||g.out[j]) continue;', 'if((half?j===i:j===i)||g.out[j]) continue;', 'p'),
    ('re-prediction pairs only with higher indices', 'if((half?j<=i:j===i)||g.out[j]) continue;', 'if((half?j<=i:j<=i)||g.out[j]) continue;', 'p'),
    ('grid cell 2 v_b h -> 0.2 v_b h', 'const C=Math.max(smax+2*vb*h,1),', 'const C=Math.max(smax+0.2*vb*h,1),', 'p'),
    ('substeps halved (speed knob: expected equivalent)', 'return Math.max(1,Math.min(64,Math.ceil(2*vb*dt/smax)));', 'return Math.max(1,Math.min(64,Math.ceil(vb*dt/smax)));', 'p'),
    # --- the walls, the lid, the moving wall
    ('moving wall: PhET rule u - v', 'const vx0=g.vx[i], vx1=2*uu-vx0;', 'const vx0=g.vx[i], vx1=uu-vx0;', 'p'),
    ('right-wall impulse 2m -> m', 'Jx=-2*m*g.vx[i]; g.vx[i]=-g.vx[i];', 'Jx=-1*m*g.vx[i]; g.vx[i]=-g.vx[i];', 'p'),
    ('wall work ledger x2', 'const dE=0.5*m*(vx1*vx1-vx0*vx0); g.led.work+=dE;', 'const dE=0.5*m*(vx1*vx1-vx0*vx0); g.led.work+=2*dE;', 'p'),
    ('moving-wall virial correction halved', 'if(g.vir.on) g.vir.kin+=2*dE*(h-t); }', 'if(g.vir.on) g.vir.kin+=dE*(h-t); }', 'p'),
    ('kinetic virial halved', 'g.vir.kin+=e2*h; }', 'g.vir.kin+=e2*h*0.5; }', 'p'),
    ('escape virial: remaining 2KE dropped', 'g.vir.kin-=2*e0*(h-t); }', 'g.vir.kin-=0*e0*(h-t); }', 'p'),
    ('escape needs the whole disk in the gap -> the centre',
     'if(xc-r>gasOpenLeft(g)&&xc+r<gasOpenRight()) kind=EV_ESC; }\n      evPush(t0+dt,i,-1,kind,si,0);',
     'if(xc>gasOpenLeft(g)&&xc<gasOpenRight()) kind=EV_ESC; }\n      evPush(t0+dt,i,-1,kind,si,0);', 'p'),
    ('opening left edge: +wall', 'return g.lid.on?Math.round(g.left-GAS.WALL+g.lid.width):g.left+GAS.OPEN_L;', 'return g.lid.on?Math.round(g.left+GAS.WALL+g.lid.width):g.left+GAS.OPEN_L;', 'p'),
    ('lid blows only below 5 x 1500', 'if(g.lid&&(!gasLidOpen(g)||gasOpening(g)<GAS.LID_WIDE)) g.lid.on=false;', 'if(g.lid&&(!gasLidOpen(g)||gasOpening(g)<5*GAS.LID_WIDE)) g.lid.on=false;', 'p'),
    ('wall speed limit x2', 'const d=g.wantW-g.W, lim=g.wallSpeed*h;', 'const d=g.wantW-g.W, lim=2*g.wallSpeed*h;', 'p'),
    ('Ideal resize: x scaled by sqrt(ratio)', '    g.x[i]*=ratio;', '    g.x[i]*=Math.sqrt(ratio);', 'p'),
    ('hit energy x2 (effusion)', 'const eHit=0.5*m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]);', 'const eHit=m*(g.vx[i]*g.vx[i]+g.vy[i]*g.vy[i]);', 'p'),
    # --- the heater
    ('heater rate x2', 'const s=Math.pow(1+g.heat/GAS.HEAT_COOL,h/GAS.DT_FRAME);', 'const s=Math.pow(1+g.heat/GAS.HEAT_COOL,2*h/GAS.DT_FRAME);', 'p'),
    ('heater not locked by hold T', "if(g.heat!==0&&g.hold!=='temperature'&&g.hold!=='pressureT'){", "if(g.heat!==0&&g.hold!=='pressureT'){", 'p'),
    # --- PhET's hold-constant logic and the gauge
    ('P hold V: H*D -> H*H', 'let w=+(N*GAS.K*T/Pm/(g.H*g.D)).toFixed(5);', 'let w=+(N*GAS.K*T/Pm/(g.H*g.H)).toFixed(5);', 'p'),
    ('P hold T: Nk -> 1.01 Nk', 'gasSetTemp(g,(g.P/GAS.P_SCALE)*gasVolume(g)/(N*GAS.K));', 'gasSetTemp(g,(g.P/GAS.P_SCALE)*gasVolume(g)/(1.01*N*GAS.K));', 'p'),
    ('setTemperature: E/N -> E/(N+1)', 'const E=gasEnergy(g), f=1.5*T*GAS.K/(E/N), s=Math.sqrt(f);', 'const E=gasEnergy(g), f=1.5*T*GAS.K/(E/(N+1)), s=Math.sqrt(f);', 'p'),
    ('hold T allowed with the lid open', 'if(mode===\'temperature\') return gasCount(g)>0&&!gasLidOpen(g);', 'if(mode===\'temperature\') return gasCount(g)>0;', 'p'),
    ('gauge noise 50 kPa -> 40', 'const pn=Math.min(50,Math.max(0,50*(1-g.P/GAS.P_MAX)))', 'const pn=Math.min(50,Math.max(0,40*(1-g.P/GAS.P_MAX)))', 'p'),
    ('gauge noise T scale 45 -> 450', 'sn=Math.min(1,Math.max(0,((g.T||0)-5)/45));', 'sn=Math.min(1,Math.max(0,((g.T||0)-5)/450));', 'p'),
    ('gauge refresh 0.75 ps -> 1.5', 'if(g.pAcc>=GAS.P_REFRESH){\n      let e=0;', 'if(g.pAcc>=2*GAS.P_REFRESH){\n      let e=0;', 'p'),
    ('max temperature not enforced', 'if(g.T!==null&&g.T>=GAS.T_MAX){', 'if(g.T!==null&&g.T>=10*GAS.T_MAX){', 'p'),
    # --- statistics
    ('histogram floor -> round', 'const v=energy?gasKE(g,i):gasSpeed(g,i), b=Math.floor(v/w);', 'const v=energy?gasKE(g,i):gasSpeed(g,i), b=Math.round(v/w);', 'p'),
    ('sampler period 1 ps -> 2', 'if(S.dt>=GAS.SAMPLE-1e-9||!playing){', 'if(S.dt>=2*GAS.SAMPLE-1e-9||!playing){', 'p'),
    ('centre of mass from W/3', 'return sm>0?sx/sm-(g.left+g.W/2):null;', 'return sm>0?sx/sm-(g.left+g.W/3):null;', 'p'),
    ('flow window 300 -> 600', 'if(F.dts.length>GAS.FLOW_WINDOW){', 'if(F.dts.length>2*GAS.FLOW_WINDOW){', 'p'),
    ('diffusion mass/temperature: 3kT -> 2kT', 'const v=Math.sqrt(3*GAS.K*T/m);\n  for(let i=0;i<g.n;i++) if(g.sp[i]===k&&!g.out[i]){', 'const v=Math.sqrt(2*GAS.K*T/m);\n  for(let i=0;i<g.n;i++) if(g.sp[i]===k&&!g.out[i]){', 'p'),
    ('counter period x2', 'if(g.counter.t>=g.counter.period){ g.counter.on=false;', 'if(g.counter.t>=2*g.counter.period){ g.counter.on=false;', 'u'),
    ('the gas-law trace keeps its stale seed', 'if(M.w.trace.length===1&&M.g.t===0){ M.w.trace.length=0; idealRecord(M.w); }', '', 'p'),
    ('captions ignore the #hint band', 'const HINT_H=18;', 'const HINT_H=0;', 'p'),
    # --- UI: dirty flags, the drags, the pause, the spring
    ('UI: pointermove forgets dirty', "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;", "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){", 'u'),
    ('UI: frame loop ignores dirty', 'if(advanced||dirty){', 'if(advanced){', 'u'),
    ('UI: a held Ideal wall repaints every frame (frame-loop guard deleted)', "if(ST.view==='ideal'&&w.dragW!==null) return false;\n    const changed", "const changed", 'u'),
    ('UI: the step key steps while the Ideal wall is held (model guard deleted)', "if(w.view==='ideal'&&w.dragW!==null) return false;", "", 'u'),
    ('UI: heater does not spring back', "null,()=>{ st.heat=0; }));", "null,()=>{ }));", 'u'),
    ('UI: pump 50 per stroke -> 40', 'w.pump.acc+=dh*50;', 'w.pump.acc+=dh*40;', 'u'),
    ('UI: lid drag off by 2 walls', 'gasSetLid(g,G.wx(x-DRAG.off)-(g.left-GAS.WALL));', 'gasSetLid(g,G.wx(x-DRAG.off)-(g.left+GAS.WALL));', 'u'),
    ('UI: wall drag snaps to 100 pm', 'const wv=clamp(Math.round(-G.wx(x-DRAG.off)/10)*10,', 'const wv=clamp(Math.round(-G.wx(x-DRAG.off)/100)*100,', 'u'),
    ('UI: slider does not redraw', "      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });", "      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); });", 'u'),
    ('UI: an action clears its own Oops', 'function button(lab,fn){ return h(\'button\',{onclick:()=>{ clearOops(); fn();', 'function button(lab,fn){ return h(\'button\',{onclick:()=>{ fn(); clearOops();', 'u'),
]
bad = []
for lab, old, new, s in M:
    n = js.count(old)
    if n != 1:
        bad.append((lab, n))
if bad:
    for b in bad:
        print('PATTERN COUNT', b)
    sys.exit(1)
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps([list(m) for m in M], ensure_ascii=False, indent=1))
print('%d mutants (%d physics, %d UI), every pattern unique' % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
