#!/usr/bin/env python3
"""gen_mutants.py -- the mutation list for generator.html.

The engine's mutants are the family's, kept in
build/magnets-and-electromagnets/gen_mutants.py: this takes the ones whose text is
actually in THIS page (the electromagnet's, the bar-magnet screen's and the far-field
view's are not, the build having stripped them) and adds this sim's own -- the flux
integral, the Fourier series, Faraday's law, the turbine and the pickup coil.  Anything
that matches other than exactly once is reported here rather than left for mutate.py to
skip in silence.

    python3 gen_mutants.py
"""
import importlib.util
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FAMILY = os.path.join(os.path.dirname(HERE), 'magnets-and-electromagnets')
PAGE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'generator.html')

spec = importlib.util.spec_from_file_location('fam_mut', os.path.join(FAMILY, 'gen_mutants.py'))
fam = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fam)

html = io.open(PAGE, encoding='utf-8').read()
js = html.split('<script>', 1)[1].rsplit('</script>', 1)[0]

MINE = [  # ---- the generator's own physics ----
    ('the flux integrand carries its own radius (the disc Jacobian)',
     'tot+=0.5*rc*G.w[i]*s*acc*2*Math.PI/npsi;', 'tot+=0.5*rc*G.w[i]*acc*2*Math.PI/npsi;', 'p'),
    ('the radial rule runs from 0 to rc', 'const s=0.5*rc*(G.x[i]+1);', 'const s=0.5*rc*(G.x[i]+0.9);', 'p'),
    ('the ring is in 3-D: the points leave the page',
     'for(let j=0;j<npsi;j++){ const ps=2*Math.PI*j/npsi; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),s*Math.sin(ps))[0]; }',
     'for(let j=0;j<npsi;j++){ const ps=2*Math.PI*j/npsi; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),0)[0]; }', 'p'),
    ('the flux is of B along the coil AXIS (x), not across it',
     'tot+=0.5*rc*G.w[i]*s*acc*2*Math.PI/npsi;\n  }\n  return tot;', 'tot+=0.5*rc*G.w[i]*s*acc*2*Math.PI/npsi;\n  }\n  return -tot;', 'p'),
    ('the ring average divides by its samples', 'return acc/n;\n}', 'return acc;\n}', 'p'),
    ('the ring is sampled round a circle', 'const ps=2*Math.PI*j/n; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),s*Math.sin(ps))[0]; }\n  return acc/n;',
     'const ps=Math.PI*j/n; acc+=magnetField(m,PICK_X,PICK_Y+s*Math.cos(ps),s*Math.sin(ps))[0]; }\n  return acc/n;', 'p'),
    ('the coil radius comes from its area', 'function pickRadius(areaPct){ return Math.sqrt(pickArea(areaPct)/Math.PI); }',
     'function pickRadius(areaPct){ return Math.sqrt(pickArea(areaPct)*Math.PI); }', 'p'),
    ("the largest loop is PhET's 70685 mm^2", 'const PICK_AMAX=70685, PICK_NMAX=4, PICK_AMIN_PCT=20;',
     'const PICK_AMAX=70000, PICK_NMAX=4, PICK_AMIN_PCT=20;', 'p'),
    ('the turbine and the coil stand where PhET puts them',
     'const TURB_X=285, TURB_Y=LAYOUT_H-375, PICK_X=520, PICK_Y=LAYOUT_H-375;',
     'const TURB_X=285, TURB_Y=LAYOUT_H-375, PICK_X=500, PICK_Y=LAYOUT_H-375;', 'p'),
    ("PhET's sample spacing is the magnet's height/10", 'const PHET_SP=MAG_R*2/10;', 'const PHET_SP=MAG_R*2/8;', 'p'),
    ("PhET's line sample weights each point by its CHORD",
     'for(let k=-n;k<=n;k++){ const y=k*sp; tot+=pageBx(th,y)*2*Math.sqrt(Math.abs(rc*rc-y*y))*sp; }',
     'for(let k=-n;k<=n;k++){ const y=k*sp; tot+=pageBx(th,y)*Math.sqrt(Math.abs(rc*rc-y*y))*sp; }', 'p'),
    # 2/M -> 1/M for every k bites; the k = 0 and Nyquist exception cannot, because both of
    # those coefficients are zero here (selfTest asserts they are), so that mutant would be
    # equivalent and is not offered
    ('the Fourier normalisation is 2/M', 'const nrm=(k===0||k===M/2)?1/M:2/M;', 'const nrm=(k===0||k===M/2)?1/M:1/M;', 'p'),
    # the sine terms are zero here and selfTest says so, so dropping them is equivalent: the
    # mutant that bites is on the harmonic itself
    ('the series runs over the harmonics of the turn', 'function seriesPhi(ser,th){ let s=0; for(let k=0;k<ser.a.length;k++) s+=ser.a[k]*Math.cos(k*th)+ser.b[k]*Math.sin(k*th); return s; }',
     'function seriesPhi(ser,th){ let s=0; for(let k=0;k<ser.a.length;k++) s+=ser.a[k]*Math.cos(k*th+0.1)+ser.b[k]*Math.sin(k*th); return s; }', 'p'),
    ('the derivative brings down a factor k', 'function seriesDPhi(ser,th){ let s=0; for(let k=1;k<ser.a.length;k++) s+=k*(-ser.a[k]*Math.sin(k*th)+ser.b[k]*Math.cos(k*th)); return s; }',
     'function seriesDPhi(ser,th){ let s=0; for(let k=1;k<ser.a.length;k++) s+=(-ser.a[k]*Math.sin(k*th)+ser.b[k]*Math.cos(k*th)); return s; }', 'p'),
    ('the derivative of a cosine is minus a sine', 'let s=0; for(let k=1;k<ser.a.length;k++) s+=k*(-ser.a[k]*Math.sin(k*th)+ser.b[k]*Math.cos(k*th)); return s;',
     'let s=0; for(let k=1;k<ser.a.length;k++) s+=k*(ser.a[k]*Math.sin(k*th)+ser.b[k]*Math.cos(k*th)); return s;', 'p'),
    ('1 G mm^2 is 1e-10 Wb', 'const WB_PER_G_MM2=1e-10;', 'const WB_PER_G_MM2=1e-9;', 'p'),
    ('Faraday: the minus sign', 'function emfOf(ser,th,N,S,omega){ return -N*S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }',
     'function emfOf(ser,th,N,S,omega){ return N*S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }', 'p'),
    ('Faraday: the EMF is N times one loop\'s', 'function emfOf(ser,th,N,S,omega){ return -N*S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }',
     'function emfOf(ser,th,N,S,omega){ return -S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }', 'p'),
    ('Faraday: dPhi/dt is omega dPhi/dtheta', 'function emfOf(ser,th,N,S,omega){ return -N*S*seriesDPhi(ser,th)*omega*WB_PER_G_MM2; }',
     'function emfOf(ser,th,N,S,omega){ return -N*S*seriesDPhi(ser,th)*WB_PER_G_MM2; }', 'p'),
    ('the flux through N turns is N times one turn\'s', 'function fluxOf(ser,th,N,S){ return N*S*seriesPhi(ser,th)*WB_PER_G_MM2; }',
     'function fluxOf(ser,th,N,S){ return S*seriesPhi(ser,th)*WB_PER_G_MM2; }', 'p'),
    ("full scale is PhET's maxEMF at 25 frames a second", 'const E_FULL=12e4*1e-4*1e-6*25;', 'const E_FULL=12e4*1e-4*1e-6*30;', 'p'),
    ('60 RPM at full flow', 'const RPM_MAX=60;', 'const RPM_MAX=50;', 'p'),
    ('the wheel is slowed by the drag, not sped up', 'function genRPM(g){ return g.flow/100*(1-genDrag(g.N,g.area,g.strength))*RPM_MAX; }',
     'function genRPM(g){ return g.flow/100*(1+genDrag(g.N,g.area,g.strength))*RPM_MAX; }', 'p'),
    ('the speed follows the flow', 'function genRPM(g){ return g.flow/100*(1-genDrag(g.N,g.area,g.strength))*RPM_MAX; }',
     'function genRPM(g){ return (1-genDrag(g.N,g.area,g.strength))*RPM_MAX; }', 'p'),
    ("the drag's floor is (N_min A_min)/(N_max A_max) of its ceiling",
     'const DRAG_MAX=0.2, NA_LO=PICK_AMIN_PCT/100*PICK_AMAX, NA_HI=PICK_NMAX*PICK_AMAX, DRAG_LO=NA_LO/NA_HI*DRAG_MAX;',
     'const DRAG_MAX=0.2, NA_LO=PICK_AMIN_PCT/100*PICK_AMAX, NA_HI=PICK_NMAX*PICK_AMAX, DRAG_LO=0.02;', 'p'),
    ('the drag ramps with N x area', 'function genDrag(N,areaPct,pct){ return pct/100*(DRAG_LO+(DRAG_MAX-DRAG_LO)*(N*pickArea(areaPct)-NA_LO)/(NA_HI-NA_LO)); }',
     'function genDrag(N,areaPct,pct){ return pct/100*(DRAG_LO+(DRAG_MAX-DRAG_LO)*(pickArea(areaPct)-NA_LO)/(NA_HI-NA_LO)); }', 'p'),
    ("the drag follows the magnet's strength", 'function genDrag(N,areaPct,pct){ return pct/100*(DRAG_LO+',
     'function genDrag(N,areaPct,pct){ return 1*(DRAG_LO+', 'p'),
    ('the EMF peak is looked for in the first quarter turn', 'for(let i=0;i<=180;i++){ const th=0.5*Math.PI*i/180, v=f(th); if(v>best){ best=v; th0=th; } }',
     'for(let i=0;i<=180;i++){ const th=Math.PI*i/180, v=f(th); if(v>best){ best=v; th0=th; } }', 'p'),
    ('the normalised current is clamped at PhET\'s full scale', 'function normOf(emf){ return Math.max(-1,Math.min(1,emf/E_FULL)); }',
     'function normOf(emf){ return emf/E_FULL; }', 'p'),
    ('the normalised current is the EMF against full scale', 'function normOf(emf){ return Math.max(-1,Math.min(1,emf/E_FULL)); }',
     'function normOf(emf){ return Math.max(-1,Math.min(1,emf/(2*E_FULL))); }', 'p'),
    ('the readings are taken at the wheel\'s own angle', 'const Phi=fluxOf(ser,g.th,g.N,S), emf=emfOf(ser,g.th,g.N,S,omega);',
     'const Phi=fluxOf(ser,g.th,g.N,S), emf=emfOf(ser,0,g.N,S,omega);', 'p'),
    ('the wheel turns omega dt in a frame', 'if(om>0){ st.th=wrap2pi(st.th+om*dt); moved=true; }',
     'if(om>0){ st.th=wrap2pi(st.th+om); moved=true; }', 'p'),
    ('and forwards', 'if(om>0){ st.th=wrap2pi(st.th+om*dt); moved=true; }',
     'if(om>0){ st.th=wrap2pi(st.th-om*dt); moved=true; }', 'p'),
    ('the turns are centred on the coil', 'function pickLoopsX(N){ const out=[]; for(let k=0;k<N;k++) out.push((k-(N-1)/2)*PICK_PITCH); return out; }',
     'function pickLoopsX(N){ const out=[]; for(let k=0;k<N;k++) out.push(k*PICK_PITCH); return out; }', 'p'),
    ('the flip is half a turn of the wheel', 'st.th=wrap2pi(st.th+Math.PI);', 'st.th=wrap2pi(st.th+Math.PI/2);', 'p'),

    # ---- the generator's own picture and controls ----
    ('the wheel turns with the magnet', 'const a=th+k*TAU/8, c=Math.cos(a), s=Math.sin(a);', 'const a=k*TAU/8, c=Math.cos(a), s=Math.sin(a);', 'u'),
    ('the wheel has eight paddles', 'for(let k=0;k<8;k++){\n    const a=th+k*TAU/8', 'for(let k=0;k<6;k++){\n    const a=th+k*TAU/8', 'u'),
    ('the water column widens with the flow', 'function waterW(flow){ return 4+46*flow/100; }', 'function waterW(flow){ return 4+0*flow/100; }', 'u'),
    ('the water falls as far as the wheel', 'function waterHit(){ return TURB_Y+Math.sqrt(Math.max(0,WHEEL_R*WHEEL_R-Math.pow(TURB_X-FAUCET_X,2))); }',
     'function waterHit(){ return TURB_Y; }', 'u'),
    ('a closed faucet pours no water', 'if(flow>0){\n    const ww=Math.max(2,waterW(flow)*map.s);', 'if(flow>=0){\n    const ww=Math.max(2,waterW(flow)*map.s);', 'u'),
    ('the indicator rides above the coil', 'function indicatorPos(rc){ return {x:PICK_X, y:PICK_Y+rc+IND_GAP}; }',
     'function indicatorPos(rc){ return {x:PICK_X, y:PICK_Y+IND_GAP}; }', 'u'),
    ('the voltmeter needle is the EMF against full scale', 'const a=(90-deg)*D2R;', 'const a=(90-0.5*deg)*D2R;', 'u'),
    ('the bulb brightens with the EMF', "dot(ctx,X,Y,R,mix('#1b2130','#ffe38a',g),'#aeb6c6',1.2);",
     "dot(ctx,X,Y,R,mix('#1b2130','#ffe38a',1),'#aeb6c6',1.2);", 'u'),
    ('the bulb\'s display mapping rises with the EMF', 'function bulbShade(b){ return Math.pow(Math.min(1,Math.max(0,b)),BULB_GAMMA); }',
     'function bulbShade(b){ return Math.pow(Math.min(1,Math.max(0,b)),0); }', 'u'),
    ('the electrons move while a current runs', "if(Math.abs(R.norm)>1e-12){ LIVE.ePhase=(LIVE.ePhase+R.norm*dt*(st.flowConv==='electron'?1:-1)+1)%1; moved=true; }",
     "if(Math.abs(R.norm)>1e-12){ LIVE.ePhase=(LIVE.ePhase+0*R.norm*dt*(st.flowConv==='electron'?1:-1)+1)%1; moved=true; }", 'u'),
    ('the electrons follow the current', "if(Math.abs(R.norm)>1e-12){ LIVE.ePhase=(LIVE.ePhase+R.norm*dt*(st.flowConv==='electron'?1:-1)+1)%1; moved=true; }",
     "if(Math.abs(R.norm)>1e-12){ LIVE.ePhase=(LIVE.ePhase+R.norm*dt*(st.flowConv==='electron'?1:1)+1)%1; moved=true; }", 'u'),
    ('the wheel writes its speed in its hub', 'function drawRPM(ctx,map,rpm){\n  if(!(rpm>0)) return;',
     'function drawRPM(ctx,map,rpm){\n  if(true) return;', 'u'),
    ('and only while it turns', 'function drawRPM(ctx,map,rpm){\n  if(!(rpm>0)) return;',
     'function drawRPM(ctx,map,rpm){\n  if(false) return;', 'u'),
    ('the speed goes on after the magnet', '  drawBarMagnet(ctx,map,M.src,{seeInside:st.seeInside});\n  drawRPM(ctx,map,R.rpm);',
     '  drawRPM(ctx,map,R.rpm);\n  drawBarMagnet(ctx,map,M.src,{seeInside:st.seeInside});', 'u'),
    ('the screen says why nothing happens with the faucet shut', "if(st.flow===0) lab(ctx,W,H,map.X(TURB_X),map.Y(TURB_Y-WHEEL_R-26),'the faucet is closed: nothing turns, so no EMF',COL.dim,SM_FONT,'center','middle');",
     "if(false) lab(ctx,W,H,map.X(TURB_X),map.Y(TURB_Y-WHEEL_R-26),'the faucet is closed: nothing turns, so no EMF',COL.dim,SM_FONT,'center','middle');", 'u'),
    ("the panel hides the other views' groups", 'for(const g of [gWater,gBar,gCoil,gTools,gShow,gNd]) g.hidden=groups[v].indexOf(g)<0;',
     'for(const g of [gWater,gBar,gCoil,gTools,gShow,gNd]) g.hidden=false;', 'u'),
    ('a dead control is dimmed', "rows.cb_bound.inp.disabled=(v!=='lines'); rows.cb_axisH.inp.disabled=(v!=='axis'); rows.cb_phetCmp.inp.disabled=(v!=='face');",
     'rows.cb_bound.inp.disabled=false; rows.cb_axisH.inp.disabled=false; rows.cb_phetCmp.inp.disabled=false;', 'u'),
    ("PhET's sample points are drawn on the coil face", "if(ST.phetCmp) for(const p of C.sp) dot(ctx,X(p.s),Y(p.p*S),Math.max(1.8,2.6),COL.struct,'#070b18',0.8);",
     "if(false) for(const p of C.sp) dot(ctx,X(p.s),Y(p.p*S),Math.max(1.8,2.6),COL.struct,'#070b18',0.8);", 'u'),
    ('the flux view marks where the wheel stands', 'dot(ctx,Xd(thd),Yv(F.rd.Phi*1e6,b,lo-pd,hi+pd),Math.max(2.5,3.5),COL.live);',
     'dot(ctx,Xd(thd),Yv(F.rd.Phi*1e6,b,lo-pd,hi+pd),0,COL.live);', 'u'),
    ('and marks it at the angle the wheel is at', 'dot(ctx,Xd(thd),Yv(F.rd.Phi*1e6,b,lo-pd,hi+pd),Math.max(2.5,3.5),COL.live);',
     'dot(ctx,Xd(0),Yv(F.rd.Phi*1e6,b,lo-pd,hi+pd),Math.max(2.5,3.5),COL.live);', 'u'),
    ('the magnet cannot be dragged off the wheel', "DRAG_CANDS.gen=(st,map,X,Y)=>[{k:'genM',on:st.genMeter,hit:p=>hitMeter(map,p,X,Y),mx:10,my:10},",
     "DRAG_CANDS.gen=(st,map,X,Y)=>[{k:'genM',on:true,hit:p=>hitMeter(map,p,X,Y),mx:10,my:10},", 'u'),
    ('the meter reads at its own crosshair', 'M.meter=st.genMeter?meterReading(M.src,st.genM.x,st.genM.y):null;',
     'M.meter=st.genMeter?meterReading(M.src,st.genC.x,st.genC.y):null;', 'u'),
    ('the strength is a percentage of 300 G',
     "function turbMagnet(st,th){ return {kind:'magnet',x:TURB_X,y:TURB_Y,ang:(th===undefined?st.th:th),S:S_MAX*st.pct/100}; }",
     "function turbMagnet(st,th){ return {kind:'magnet',x:TURB_X,y:TURB_Y,ang:(th===undefined?st.th:th),S:S_MAX*st.pct/50}; }", 'p'),
    ('the magnet rides the wheel at its own angle',
     "function turbMagnet(st,th){ return {kind:'magnet',x:TURB_X,y:TURB_Y,ang:(th===undefined?st.th:th),S:S_MAX*st.pct/100}; }",
     "function turbMagnet(st,th){ return {kind:'magnet',x:TURB_X,y:TURB_Y,ang:0,S:S_MAX*st.pct/100}; }", 'p'),
    ('the flip kicks the needle', 'if(LIVE.genRot){ LIVE.genRot.om+=FLIP_KICK; LIVE.genRot.rest=false; }',
     'if(LIVE.genRot){ LIVE.genRot.om+=0; LIVE.genRot.rest=false; }', 'u'),
]

out, dropped, bad = [], [], []
for lab, old, new in fam.P:
    n = js.count(old)
    if n == 0:
        dropped.append(lab)
    elif n == 1:
        out.append([lab, old, new, 'p'])
    else:
        bad.append((lab, n))
for lab, old, new in fam.U:
    n = js.count(old)
    if n == 0:
        dropped.append(lab)
    elif n == 1:
        out.append([lab, old, new, 'u'])
    else:
        bad.append((lab, n))
for lab, old, new, suite in MINE:
    n = js.count(old)
    if n != 1:
        bad.append((lab, n))
    else:
        out.append([lab, old, new, suite])

io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(out, indent=1))
print('mutants.json: %d mutants (%d physics, %d UI)' % (len(out), sum(1 for m in out if m[3] == 'p'), sum(1 for m in out if m[3] == 'u')))
print('   not in this page: %d -- %s' % (len(dropped), ', '.join(dropped)))
if bad:
    raise SystemExit('patterns that do not match exactly once: %s' % bad)
