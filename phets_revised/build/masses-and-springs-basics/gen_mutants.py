#!/usr/bin/env python3
"""Write mutants.json and check every `old` appears EXACTLY once in the
assembled html (mutate.py skips a pattern that matches twice or not at all)."""
import io, json, os

here = os.path.dirname(os.path.abspath(__file__))
sim = os.path.abspath(os.path.join(here, '..', '..', 'masses-and-springs-basics.html'))

M = [
    # ---- Hooke's law and the constants it is evaluated with ----
    ["y_eq halved", "function yEq(m,k,g){ return m*g/k; }", "function yEq(m,k,g){ return m*g/(2*k); }", "p"],
    ["y_eq inverts k and m", "function yEq(m,k,g){ return m*g/k; }", "function yEq(m,k,g){ return k*g/m; }", "p"],
    ["spring force sign", "function springForce(k,y){ return -k*y; }", "function springForce(k,y){ return k*y; }", "p"],
    ["g = ky/m inverted", "function gFromStretch(k,y,m){ return k*y/m; }", "function gFromStretch(k,y,m){ return k*m/y; }", "p"],
    ["m = ky/g inverted", "function mFromStretch(k,y,g){ return k*y/g; }", "function mFromStretch(k,y,g){ return k*g/y; }", "p"],
    ["PhET's Earth becomes the real one", "G_EARTH=9.8,", "G_EARTH=9.81,", "p"],
    ["PhET's Moon becomes the real one", "G_MOON=1.6,", "G_MOON=1.62,", "p"],
    ["PhET's Jupiter becomes the real one", "G_JUPITER=24.8,", "G_JUPITER=24.79,", "p"],
    ["Planet X moved", "G_PLANETX=14.2;", "G_PLANETX=14.5;", "p"],
    ["spring constant floor", "const KMIN=3, KMAX=12, KDEF=6;", "const KMIN=2, KMAX=12, KDEF=6;", "p"],
    ["damping ceiling", "const BMIN=0, BMAX=0.7, BDEF=0.3;", "const BMIN=0, BMAX=0.75, BDEF=0.3;", "p"],
    ["lightest mass", "const MASS_G_MIN=50, MASS_G_MAX=300, MASS_G_DEF=100;", "const MASS_G_MIN=40, MASS_G_MAX=300, MASS_G_DEF=100;", "p"],
    ["slow motion ratio", "const SLOW=1/8;", "const SLOW=1/4;", "p"],
    ["the ceiling", "const CEILING_Y=1.47,", "const CEILING_Y=1.5,", "p"],
    ["the hook centre", "HOOK_C=0.0185;", "HOOK_C=0.02;", "p"],
    ["the natural length", "const L0=0.5;", "const L0=0.55;", "p"],
    ["the Stretch screen's damping", "const B_STRETCH=0.7, B_BOUNCE=0, B_LAB=0;", "const B_STRETCH=0.5, B_BOUNCE=0, B_LAB=0;", "p"],
    ["the block density", "const MASS_DENS=80, MASS_S=2.5, MASS_Y=4;", "const MASS_DENS=60, MASS_S=2.5, MASS_Y=4;", "p"],
    ["the block size exponent", "return Math.sqrt(m/(MASS_DENS*MASS_S*Math.PI))*MASS_Y;", "return Math.pow(m/(MASS_DENS*MASS_S*Math.PI),1/3)*MASS_Y;", "p"],
    ["the block aspect", "function massHeight(m){ return MASS_S*massRadius(m); }", "function massHeight(m){ return massRadius(m); }", "p"],
    # ---- the oscillator ----
    ["w0 inverts m and k", "function omega0(m,k){ return Math.sqrt(k/m); }", "function omega0(m,k){ return Math.sqrt(m/k); }", "p"],
    ["the period's 2 pi", "function period0(m,k){ return TAU*Math.sqrt(m/k); }", "function period0(m,k){ return PI*Math.sqrt(m/k); }", "p"],
    ["the period inverts m and k", "function period0(m,k){ return TAU*Math.sqrt(m/k); }", "function period0(m,k){ return TAU*Math.sqrt(k/m); }", "p"],
    ["gamma loses its 2", "function gammaOf(m,b){ return b/(2*m); }", "function gammaOf(m,b){ return b/m; }", "p"],
    ["critical damping loses its 2", "function bCrit(m,k){ return 2*Math.sqrt(k*m); }", "function bCrit(m,k){ return Math.sqrt(k*m); }", "p"],
    ["critical damping inverts m", "function bCrit(m,k){ return 2*Math.sqrt(k*m); }", "function bCrit(m,k){ return 2*Math.sqrt(k/m); }", "p"],
    ["zeta halved", "function zetaOf(m,k,b){ return b/bCrit(m,k); }", "function zetaOf(m,k,b){ return b/(2*bCrit(m,k)); }", "p"],
    ["the discriminant's sign", "return k/m-g*g;", "return k/m+g*g;", "p"],
    ["the discriminant's factor", "return k/m-g*g;", "return k/m-2*g*g;", "p"],
    ["the log decrement's root", "return z<1?TAU*z/Math.sqrt(1-z*z):Infinity;", "return z<1?TAU*z/Math.sqrt(1+z*z):Infinity;", "p"],
    ["the log decrement's 2 pi", "return z<1?TAU*z/Math.sqrt(1-z*z):Infinity;", "return z<1?PI*z/Math.sqrt(1-z*z):Infinity;", "p"],
    ["Q loses its 2", "return z>0?1/(2*z):Infinity;", "return z>0?1/z:Infinity;", "p"],
    # ---- the closed form ----
    ["the C series' 1/24", "1-s*t2/2+s2*t2*t2/24", "1-s*t2/2+s2*t2*t2/12", "p"],
    ["the C series' 1/2", "1-s*t2/2+s2*t2*t2/24", "1-s*t2/4+s2*t2*t2/24", "p"],
    ["the Sn series' 1/6", "t*(1-s*t2/6+s2*t2*t2/120)", "t*(1-s*t2/3+s2*t2*t2/120)", "p"],
    ["the Sn series' 1/120", "t*(1-s*t2/6+s2*t2*t2/120)", "t*(1-s*t2/6+s2*t2*t2/60)", "p"],
    ["the series join moved up", "if(st2<1e-5){", "if(st2<1.5){", "p"],
    ["Sn on the cosine branch", "return [Math.cos(w*t),Math.sin(w*t)/w];", "return [Math.cos(w*t),Math.sin(w*t)*w];", "p"],
    ["the cosh branch", "return [Math.cosh(r*t),Math.sinh(r*t)/r];", "return [Math.cos(r*t),Math.sinh(r*t)/r];", "p"],
    ["the decay's exponent", "e=Math.exp(-gam*t);", "e=Math.exp(-2*gam*t);", "p"],
    ["the discriminant fed to CSn", "cs=CSn(w02-gam*gam,t)", "cs=CSn(w02+gam*gam,t)", "p"],
    ["u's gamma term", "e*(u0*(C+gam*Sn)+v0*Sn)", "e*(u0*(C-gam*Sn)+v0*Sn)", "p"],
    ["v's w0 squared", "e*(-w02*u0*Sn+v0*(C-gam*Sn))", "e*(-w02*w02*u0*Sn+v0*(C-gam*Sn))", "p"],
    ["v's gamma term", "e*(-w02*u0*Sn+v0*(C-gam*Sn))", "e*(-w02*u0*Sn+v0*(C+gam*Sn))", "p"],
    ["the RK4 weights", "u+=hh*(a1+2*a2+2*a3+a4)/6;", "u+=hh*(a1+2*a2+2*a3+a4)/5;", "p"],
    ["the RK4 half step", "const a2=fa(u+hh*a1/2,v+hh*b1/2), b2=fb(u+hh*a1/2,v+hh*b1/2);", "const a2=fa(u+hh*a1/3,v+hh*b1/3), b2=fb(u+hh*a1/3,v+hh*b1/3);", "p"],
    ["the bisection runs backwards", "if(fa*fm<0){ c=mid; fc=fm; } else { a=mid; fa=fm; }", "if(fa*fm<0){ a=mid; fa=fm; } else { c=mid; fc=fm; }", "p"],
    ["the third-crossing bracket", "const z3=zeroBetween(m,k,b,u0,0,Td*1.1,Td*1.6);", "const z3=zeroBetween(m,k,b,u0,0,Td*1.6,Td*2.1);", "p"],
    # ---- energy ----
    ["the kinetic 1/2", "function keOf(m,v){ return 0.5*m*v*v; }", "function keOf(m,v){ return m*v*v; }", "p"],
    ["the kinetic exponent", "function keOf(m,v){ return 0.5*m*v*v; }", "function keOf(m,v){ return 0.5*m*v; }", "p"],
    ["the elastic 1/2", "function peElastic(k,y){ return 0.5*k*y*y; }", "function peElastic(k,y){ return k*y*y; }", "p"],
    ["the elastic exponent", "function peElastic(k,y){ return 0.5*k*y*y; }", "function peElastic(k,y){ return 0.5*k*y; }", "p"],
    ["the oscillator energy's k term", "return 0.5*m*v*v+0.5*k*u*u; }", "return 0.5*m*v*v+0.25*k*u*u; }", "p"],
    ["the gravitational share's sign", "function peGrav(m,g,y,ybot){ return m*g*(ybot-y); }", "function peGrav(m,g,y,ybot){ return m*g*(y-ybot); }", "p"],
    ["the swing bottom", "function swingBottom(m,k,g){ return 2*yEq(m,k,g); }", "function swingBottom(m,k,g){ return yEq(m,k,g); }", "p"],
    ["the ledger constant", "function gravOffset(m,k,g){ return 1.5*m*m*g*g/k; }", "function gravOffset(m,k,g){ return 0.5*m*m*g*g/k; }", "p"],
    ["the ledger total", "function ledgerTotal(m,k,g){ return 2*m*m*g*g/k; }", "function ledgerTotal(m,k,g){ return 4*m*m*g*g/k; }", "p"],
    # ---- the live model ----
    ["the stepper's equilibrium sign", "const ye=yEq(sp.m,sp.k,g), u0=S.y-ye, v0=S.v;", "const ye=yEq(sp.m,sp.k,g), u0=S.y+ye, v0=S.v;", "p"],
    ["the stepper puts the equilibrium back with the wrong sign", "S.y=u1+ye; S.v=r[1];", "S.y=u1-ye; S.v=r[1];", "p"],
    ["the drawn spring's free end", "o.bottom=CEILING_Y-L0-S.y;", "o.bottom=CEILING_Y-L0+S.y;", "p"],
    ["the traced period is one crossing, not two", "return c.length>=3?c[c.length-1]-c[c.length-3]:NaN;", "return c.length>=3?c[c.length-1]-c[c.length-2]:NaN;", "p"],
    ["the thermal share's sign", "const th=E0-energyU(m,k,r[0],r[1]); TH.push(th);", "const th=energyU(m,k,r[0],r[1])-E0; TH.push(th);", "p"],
    ["the reachable zeta ceiling uses the heaviest mass", "zMaxPhet:BMAX/bCrit(MASS_G_MIN/1000,KMIN)", "zMaxPhet:BMAX/bCrit(MASS_G_MAX/1000,KMIN)", "p"],
    ["the damping plane's smallest 2 sqrt(km)", "bPhet:BMAX,bcMin:bCrit(MASS_G_MIN/1000,KMIN),bcMax:bCrit(MASS_G_MAX/1000,KMAX)", "bPhet:BMAX,bcMin:bCrit(MASS_G_MAX/1000,KMIN),bcMax:bCrit(MASS_G_MAX/1000,KMAX)", "p"],
    ["the damping curves' b", "const curves=zlist.map(o=>({z:o.z,lab:o.lab,col:o.col,b:o.z*bc,", "const curves=zlist.map(o=>({z:o.z,lab:o.lab,col:o.col,b:o.z*bc/2,", "p"],
    ["the drawn peaks are half a period apart", "for(let n2=0;n2<6;n2++){\n    const t=n2*Td; peaks.push({n:n2,t,u:prop(m,k,st.zeta*bc,u0,0,t)[0]});", "for(let n2=0;n2<6;n2++){\n    const t=n2*Td/2; peaks.push({n:n2,t,u:prop(m,k,st.zeta*bc,u0,0,t)[0]});", "p"],
    ["the coil radius", "const COILS=10, COIL_R=0.045, LEG=0.06;", "const COILS=10, COIL_R=0.055, LEG=0.06;", "p"],
    ["the coil stops short", "pts.push([xc,ytop-len]);", "pts.push([xc,ytop-len*0.9]);", "p"],
    ["the wire weight runs backwards", "return 1.6+2.6*(k-KMIN)/(KMAX-KMIN);", "return 1.6+2.6*(KMAX-k)/(KMAX-KMIN);", "p"],
    ["the crossing threshold lets the noise through", "&&Math.abs(v0)>CROSS_V", "", "p"],
    # ---- the UI ----
    ["a drag no longer marks the frame dirty",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ roEl.innerHTML=readoutHTML(S.model()); }", "u"],
    ["a grab no longer marks the frame dirty",
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; syncPanel(); }",
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); syncPanel(); }", "u"],
    ["the mass drag loses its grab offset", "DRAG.what='mass'; DRAG.sp=s.i; DRAG.oy=s.bottom-wy; return true; }", "DRAG.what='mass'; DRAG.sp=s.i; DRAG.oy=0; return true; }", "u"],
    ["letting go no longer stops the mass", "if(DRAG.what==='mass'){ LIVE.slot[DRAG.sp].v=0; }", "if(DRAG.what==='mass'){ }", "u"],
    ["a held mass keeps stepping", "for(const sp of sps){ if(DRAG.what===null||DRAG.sp!==sp.i) stepSlot(sp,g,b,dts); }", "for(const sp of sps){ stepSlot(sp,g,b,dts); }", "u"],
    ["a hidden movable line is still grabbable", "if(ST.movLine&&Math.abs(y-map.Y(ST.movY))<=7)", "if(Math.abs(y-map.Y(ST.movY))<=7)", "u"],
    ["switching screens no longer restores PhET's damping", "if(VIEW_DAMPING[k]!==undefined) st.damping=VIEW_DAMPING[k];", "if(false) st.damping=VIEW_DAMPING[k];", "u"],
    ["a slider no longer redraws", "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });", "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; });", "u"],
    ["the ignored mass slider stays live", "rows.massG.row.hidden=(rackById(LAB_RACK,st.labMass).m!==null);", "rows.massG.row.hidden=false;", "u"],
    ["slow motion runs at full speed", "const dts=(dtWall||0)*(ST.speed==='slow'?SLOW:1);", "const dts=(dtWall||0)*1;", "u"],
    ["a mass chip no longer re-hangs its spring", "const m1Chips=chipRow(RACK,'mass1',()=>slotReset(0));", "const m1Chips=chipRow(RACK,'mass1',()=>{});", "u"],
    ["the ruler drag loses its offset", "DRAG.what='ruler'; DRAG.ox=ST.rulerX-wx; DRAG.oy=ST.rulerY-wy; return true; }", "DRAG.what='ruler'; DRAG.ox=0; DRAG.oy=0; return true; }", "u"],
]

src = io.open(sim, encoding='utf-8').read()
js = src.split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = 0
for lab, old, new, suite in M:
    n = js.count(old)
    if n != 1:
        print('!! %-55s matches %d times' % (lab, n))
        bad += 1
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=0) + '\n')
print('%d mutants (%d physics, %d ui); %d bad patterns'
      % (len(M), sum(1 for x in M if x[3] == 'p'), sum(1 for x in M if x[3] == 'u'), bad))
