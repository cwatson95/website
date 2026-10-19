#!/usr/bin/env python3
"""mutants.json for tools/mutate.py: [label, old, new, suite].  Every `old`
must occur EXACTLY once in the extracted script (_out/run.js) or the sweep
would skip it; this script refuses to write a list that would be skipped."""
import io, os, json
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
P = [  # physics: every leading coefficient, exponent, unit conversion and sign
 ('g = 9.81 (PhET)',                 'const G_EARTH=9.81;', 'const G_EARTH=9.8;'),
 ('NASA T lapse 0.00649',            'const T=15.04-0.00649*alt;', 'const T=15.04-0.0065*alt;'),
 ('NASA T0 15.04',                   'const T=15.04-0.00649*alt;', 'const T=15.00-0.00649*alt;'),
 ('NASA p0 101.29 kPa',              'const p=101.29*Math.pow(', 'const p=101.3*Math.pow('),
 ('NASA exponent 5.256',             '/288.08,5.256);', '/288.08,5.26);'),
 ('NASA 288.08',                     '(T+273.1)/288.08,', '(T+273.1)/288.15,'),
 ('NASA R 0.2869',                   'return p/(0.2869*(T+273.1));', 'return p/(0.287*(T+273.1));'),
 ('NASA kelvin 273.1',               'return p/(0.2869*(T+273.1));', 'return p/(0.2869*(T+273.15));'),
 ('drag area pi d^2/4',              'return rho*cd*(PI*d*d/4)/(2*m);', 'return rho*cd*(PI*d*d/2)/(2*m);'),
 ('drag 1/2m',                       'return rho*cd*(PI*d*d/4)/(2*m);', 'return rho*cd*(PI*d*d/4)/(m);'),
 ('terminal speed sqrt(g/k)',        'return k>0?Math.sqrt(g/k):Infinity;', 'return k>0?Math.sqrt(2*g/k):Infinity;'),
 ('vacuum T: 2gh',                   'const T=(h<=0&&w<=0)?0:(w+Math.sqrt(w*w+2*g*h))/g;', 'const T=(h<=0&&w<=0)?0:(w+Math.sqrt(w*w+g*h))/g;'),
 ('vacuum apex y: w^2/2g',           'y:h+w*w/(2*g)}', 'y:h+w*w/g}'),
 ('vacuum optimum atan2 order',      'return {th:Math.atan2(v0,s)*RAD, R:v0*s/g};', 'return {th:Math.atan2(s,v0)*RAD, R:v0*s/g};'),
 ('envelope g x^2/2v0^2',            'return h+v0*v0/(2*g)-g*x*x/(2*v0*v0);', 'return h+v0*v0/(2*g)-g*x*x/(v0*v0);'),
 ('vacuum landing angle sign',       'angL:vL>0?Math.atan2(-vy,u)*RAD:NaN', 'angL:vL>0?Math.atan2(vy,u)*RAD:NaN'),
 ('vacuumPath g t^2/2',              'ys.push(h+v0*Math.sin(th)*t-0.5*g*t*t);', 'ys.push(h+v0*Math.sin(th)*t-g*t*t);'),
 ('RK4 stage-1 drag sign',           'const a1=-kd*vx, b1=-g-kd*vy, p1=kd*sp*sp;', 'const a1=kd*vx, b1=-g-kd*vy, p1=kd*sp*sp;'),
 ('RK4 stage-4 gravity',             'const a4=-kd*vx4, b4=-g-kd*vy4, p4=kd*sp*sp;', 'const a4=-kd*vx4, b4=-kd*vy4, p4=kd*sp*sp;'),
 ('RK4 half step',                   'const vx2=vx+0.5*h*a1, vy2=vy+0.5*h*b1;', 'const vx2=vx+h*a1, vy2=vy+h*b1;'),
 ('RK4 weights 1,2,2,1 -> 1,2,1,2',  'vx+h/6*(a1+2*a2+2*a3+a4)', 'vx+h/6*(a1+2*a2+a3+2*a4)'),
 ('ledger power k|v|^3',             'const a1=-kd*vx, b1=-g-kd*vy, p1=kd*sp*sp;', 'const a1=-kd*vx, b1=-g-kd*vy, p1=kd*sp;'),
 ('step rule C/(k|v|)',              'if(k*sp*hh>C_STEP) hh=C_STEP/(k*sp); }', 'if(k*sp*hh>C_STEP) hh=2*C_STEP/(k*sp); }'),
 ('C_STEP 0.005',                    'const H_MAX=0.002, C_STEP=0.005,', 'const H_MAX=0.002, C_STEP=0.01,'),
 ('H_MAX 2 ms',                      'const H_MAX=0.002, C_STEP=0.005,', 'const H_MAX=0.004, C_STEP=0.005,'),
 ('event bisections 60',             'N_BIS=60,', 'N_BIS=20,'),
 ('dot snap tolerance',              'if(t+hh>tD-1e-9){ hh=tD-t; hit=true; }', 'if(t+hh>tD){ hh=tD-t; hit=true; }'),
 ('apex test vy>0',                  'if(s[3]>0&&ns[3]<=0){', 'if(s[3]>=0&&ns[3]<=0){'),
 ('landing angle sign',              'F.angL=F.vL>0?Math.atan2(-vy,vx)*RAD:NaN;', 'F.angL=F.vL>0?Math.atan2(vy,vx)*RAD:NaN;'),
 ('Hermite h10',                     'h10=s3-2*s2+s,', 'h10=s3-2*s2,'),
 ('continuation dot offset',         'C.dots.filter(j=>j>0).map(j=>j+i)', 'C.dots.filter(j=>j>0).map(j=>j+i+1)'),
 ('hodograph F: + ln tan',           'return Math.sin(psi)/(c*c)+Math.log(Math.tan(PI/4+psi/2));', 'return Math.sin(psi)/(c*c)-Math.log(Math.tan(PI/4+psi/2));'),
 ('hodograph u: F(th)-F(phi)',       '(hodoF(th)-hodoF(phi))', '(hodoF(phi)-hodoF(th))'),
 ('hodograph y integrand u^2',       'iy+=wq*u*u*Math.tan(psi)*sec2;', 'iy+=wq*u*Math.tan(psi)*sec2;'),
 ('Gauss-Legendre weight 2',         'ws.push(2/((1-x*x)*dp*dp));', 'ws.push(1/((1-x*x)*dp*dp));'),
 ('stars: W/6',                      'return d<=TARGET_W/6?3:', 'return d<=TARGET_W/5?3:'),
 ('target width 3 m',                'TARGET_X0=15, TARGET_W=3;', 'TARGET_X0=15, TARGET_W=4;'),
 ('three in flight',                 'MAX_FLYING=3, MAX_TRAJ=5,', 'MAX_FLYING=4, MAX_TRAJ=5,'),
 ('slow motion 0.33',                'SLOW=0.33;', 'SLOW=0.5;'),
 ('probe radius / zoom',             'return 0.45/ST.zoom;', 'return 0.45*ST.zoom;'),
 ('retarget: the lead is the oldest', 'for(const p of tr.projs) if(p.t0<lead.t0) lead=p;', 'for(const p of tr.projs) if(p.t0>lead.t0) lead=p;'),
 ('keep the latest landed',          'if(p.tl>keep.tl||(p.tl===keep.tl&&p.t0>keep.t0)) keep=p;', 'if(p.tl<keep.tl||(p.tl===keep.tl&&p.t0<keep.t0)) keep=p;'),
 ('dedup refuses changed paths',     'if(last&&!last.changed&&last.key===key){', 'if(last&&last.key===key){'),
 ('fan step 7.5',                    'FAN_STEP=7.5,', 'FAN_STEP=10,'),
 ('v_t within reach: 25 s',          'reach=isFinite(vt)&&3*vt/E.g<=25;', 'reach=isFinite(vt)&&3*vt/E.g<=250;'),
 ('ledger residual g y',             '+F.g*F.y[i]+F.w[i]; worst=', '+F.w[i]; worst='),
 ('envOf altitude',                  'const rho=airDensity(alt);\n  return {g,rho,', 'const rho=airDensity(0);\n  return {g,rho,'),
 ('envOf lab gravity',               "const g=v==='lab'?st.l_g:(an?st.a_g:G_EARTH);", "const g=an?st.a_g:G_EARTH;"),
 ('golden section ratio',            'r=(Math.sqrt(5)-1)/2;', 'r=0.5;'),
]
U = [  # the UI: repaint flags, the drags, the controls
 ('pointermove dirty flag',          "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;", "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){"),
 ('wheel dirty flag',                'rows.zoom.sync(); dirty=true; } },{passive:false});', 'rows.zoom.sync(); } },{passive:false});'),
 ('frame loop ignores advanced',     'if(advanced||dirty){', 'if(dirty){'),
 ('barrel angle ignores the pivot',  "ST[p+'th']=clamp(Math.round(Math.atan2(wy-ST[p+'h'],wx)*RAD)", "ST[p+'th']=clamp(Math.round(Math.atan2(wy,wx)*RAD)"),
 ('height drag ignores the grab',    "ST[p+'h']=clamp(Math.round((wy-DRAG.dy)*10)/10", "ST[p+'h']=clamp(Math.round((wy)*10)/10"),
 ('target drag frozen',              "ST[p+'tgt']=clamp(Math.round((wx-DRAG.dx)*10)/10", "ST[p+'tgt']=clamp(Math.round((DRAG.dx)*10)/10"),
 ('probe drag frozen x',             'sc.probe.x=clamp(wx-DRAG.dx,xa,xb);', 'sc.probe.x=clamp(sc.probe.x,xa,xb);'),
 ('paused still steps',              'if(!ST.running||!isScene(ST.view)) return false;', 'if(!isScene(ST.view)) return false;'),
 ('step button inert',               "button('step',()=>{ if(isScene(st.view)) advance(st.view,S.dt()); })", "button('step',()=>{ })"),
 ('slider does not redraw',          'st[key]=parseFloat(inp.value);\n      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });',
                                     'st[key]=parseFloat(inp.value);\n      val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; });'),
 ('air change does not re-route',    'const envChanged=()=>{ retarget(st.view); };', 'const envChanged=()=>{ };'),
 ('fire button never disabled',      'fireBtns.forEach(b=>{ b.disabled=full; });', 'fireBtns.forEach(b=>{ b.disabled=false; });'),
 ('lab C_d lock ignores the object', "rows.l_cd.inp.disabled=!(st.l_obj==='custom'&&st.l_air);", "rows.l_cd.inp.disabled=!(st.l_air);"),
 ('lab chip keeps the old C_d',      'st.l_m=O.m; st.l_d=O.d; st.l_cd=O.cd;', 'st.l_m=O.m; st.l_d=O.d;'),
 ('f key does not fire',             "else if(e.key==='f'){", "else if(e.key==='F'){"),
 ('reset keeps the scenes',          'st.view=v; SCENE_VIEWS.forEach(scnReset); DRAG.what=null;', 'st.view=v; DRAG.what=null;'),
 ('tab switch skips syncPanel',      "b.className=TABS[i][0]===st.view?'active':'');\n    syncChips(); syncPanel();", "b.className=TABS[i][0]===st.view?'active':'');\n    syncChips();"),
 ('wheel ignores the view',          'S.wheel=function(dy){\n    if(!isScene(ST.view)) return false;', 'S.wheel=function(dy){'),
]
out = []
bad = []
for lab, old, new in P:
    n = js.count(old)
    if n != 1: bad.append((lab, n))
    out.append([lab, old, new, 'p'])
for lab, old, new in U:
    n = js.count(old)
    if n != 1: bad.append((lab, n))
    out.append([lab, old, new, 'u'])
if bad:
    for b in bad: print('PATTERN NOT UNIQUE:', b)
    raise SystemExit(1)
json.dump(out, io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('mutants.json: %d physics + %d UI mutants, every pattern unique' % (len(P), len(U)))
