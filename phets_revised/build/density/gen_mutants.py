#!/usr/bin/env python3
"""Write mutants.json for density.html.

Every leading coefficient, exponent, unit conversion and sign in the physics,
plus the UI mutants (the drag's dirty flag, the hold, the release, the panel
sync).  `old` must appear exactly once in the extracted script, so each pattern
carries enough context to be unique; assemble.py's output is checked here.
"""
import io
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
sim = os.path.abspath(os.path.join(here, '..', '..', 'density.html'))

M = [
    # ---- the pool geometry and the free-surface solve -----------------------
    ["POOL_H: 0.15 -> 0.1", "POOL_H=0.15/0.9/0.4", "POOL_H=0.1/0.9/0.4", "p"],
    ["A_POOL: W*D -> W*W", "const A_POOL=POOL_W*POOL_D;", "const A_POOL=POOL_W*POOL_W;", "p"],
    ["VF0: 0.1 -> 0.12", "const VF0=0.1;", "const VF0=0.12;", "p"],
    ["the pool volume below yw drops the +H", "A_POOL*Math.max(0,yw+POOL_H)", "A_POOL*Math.max(0,yw)", "p"],
    ["netFluid ADDS the displaced volume", "t-=blockState(b,yw,rhoF).Vsub", "t+=blockState(b,yw,rhoF).Vsub", "p"],
    ["netFluid ignores the obstacles", "return t-obstacleVolume(obs,yw);", "return t;", "p"],
    ["poolLevel takes the SUPREMUM instead of the infimum",
     "if(netFluid(mid,blocks,obs,rhoF)<Vf) lo=mid; else hi=mid;",
     "if(netFluid(mid,blocks,obs,rhoF)<=Vf) hi=mid; else lo=mid;", "p"],
    ["poolLevel: 80 halvings -> 8", "const n=nit||80;", "const n=nit||8;", "p"],
    ["obstacleVolume: clamp top at 2h", "t+=o.a*clamp(yw-o.y0,0,o.h)", "t+=o.a*clamp(yw-o.y0,0,2*o.h)", "p"],
    # ---- the cube -----------------------------------------------------------
    ["cubeSide: V^(1/3) -> V^(1/2)", "return Math.pow(V,1/3);", "return Math.pow(V,1/2);", "p"],
    ["cubeBelow: s*s -> s", "return s*s*(yw-yb);", "return s*(yw-yb);", "p"],
    ["cubeBelow saturates at s^3, not V", "if(yw>=yb+s) return V;", "if(yw>=yb+s) return s*s*s;", "p"],
    # ---- Archimedes ---------------------------------------------------------
    ["floatDraft: rho_b/rho_f -> rho_f/rho_b", "return cubeSide(V)*rho/rhoF;", "return cubeSide(V)*rhoF/rho;", "p"],
    ["floatDraft loses the side", "function floatDraft(V,rho,rhoF){ return cubeSide(V)*rho/rhoF; }",
     "function floatDraft(V,rho,rhoF){ return rho/rhoF; }", "p"],
    ["the floating displaced volume drops rho_b/rho_f",
     "return {Vsub:b.V*b.rho/rhoF,yb:yb,mode:'float',s:s};",
     "return {Vsub:b.V,yb:yb,mode:'float',s:s};", "p"],
    ["the float test uses <= on the SUPPORT, not the draft", "if(yb>=sup) return {Vsub:b.V*b.rho/rhoF",
     "if(yb>=sup-1) return {Vsub:b.V*b.rho/rhoF", "p"],
    ["float/sink decided by mass, not density", "if(b.rho<rhoF){", "if(b.rho*b.V<rhoF){", "p"],
    ["submergedFraction: min -> max", "return Math.min(1,rho/rhoF);", "return Math.max(1,rho/rhoF);", "p"],
    ["apparentWeight: sign of the upthrust", "return rho*V*G-rhoF*G*(Vsub===undefined?V:Vsub);",
     "return rho*V*G+rhoF*G*(Vsub===undefined?V:Vsub);", "p"],
    ["riseFloating uses the volume, not the mass", "function riseFloating(m,rhoF){ return m/(rhoF*A_POOL); }",
     "function riseFloating(m,rhoF){ return m/(rhoF*rhoF*A_POOL); }", "p"],
    ["riseSunk: V/A -> V*A", "function riseSunk(V){ return V/A_POOL; }", "function riseSunk(V){ return V*A_POOL; }", "p"],
    ["the buoyant force drops g", "const st=blockState(b,yw,rhoF), m=b.rho*b.V, W=m*G, Fb=rhoF*G*st.Vsub;",
     "const st=blockState(b,yw,rhoF), m=b.rho*b.V, W=m*G, Fb=rhoF*st.Vsub;", "p"],
    ["the contact force is clamped at zero again (the dead clamp returns)",
     "const N=(st.mode==='rest')?(W-Fb):0;", "const N=(st.mode==='rest')?Math.max(1e-6,W-Fb):0;", "p"],
    ["the contact force uses W+Fb", "const N=(st.mode==='rest')?(W-Fb):0;",
     "const N=(st.mode==='rest')?(W+Fb):0;", "p"],
    ["a floating block is given a contact force too", "const N=(st.mode==='rest')?(W-Fb):0;",
     "const N=(W-Fb);", "p"],
    ["the hand force drops the upthrust", "const hand=(st.mode==='held')?(W-Fb):0;",
     "const hand=(st.mode==='held')?W:0;", "p"],
    # ---- the pressure on the faces -----------------------------------------
    ["the bottom-face pressure drops rho", "const pBot=yb<yw?rhoF*G*(yw-yb):0",
     "const pBot=yb<yw?G*(yw-yb):0", "p"],
    ["the net face force uses pBot+pTop", "net:(pBot-pTop)*A", "net:(pBot+pTop)*A", "p"],
    ["the side-face pressure is taken at the BOTTOM, not the mid-depth",
     "const side=rhoF*G*(yw-0.5*(yb+yl))*s*dsub;", "const side=rhoF*G*(yw-yb)*s*dsub;", "p"],
    ["the top face is wetted even above the surface", "pTop=yt<yw?rhoF*G*(yw-yt):0;",
     "pTop=rhoF*G*(yw-yt);", "p"],
    ["the edge force uses the normal the wrong way round", "const fx=-p*dy, fy=p*dx;",
     "const fx=p*dy, fy=-p*dx;", "p"],
    ["the edge pressure is taken at a vertex, not the midpoint",
     "const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2], p=rhoF*G*(w-mid[1]);",
     "const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2], p=rhoF*G*(w-a[1]);", "p"],
    ["polyArea loses its half", "return 0.5*s; }", "return s; }", "p"],
    ["clipBelow clips ABOVE", "const a=poly[i], b=poly[(i+1)%n], ain=a[1]<=w, bin=b[1]<=w;",
     "const a=poly[i], b=poly[(i+1)%n], ain=a[1]>=w, bin=b[1]>=w;", "p"],
    # ---- units, constants and PhET's data ----------------------------------
    ["gravity 9.8 -> 9.80665", "const G=9.8;", "const G=9.80665;", "p"],
    ["litres in a cubic metre: 1000 -> 100", "const LITERS=1000;", "const LITERS=100;", "p"],
    ["PhET's water 1000 -> 998", "{id:'water',    name:'water',     phet:1000,", "{id:'water',    name:'water',     phet:998,", "p"],
    ["PhET's wood 400 -> 450", "{id:'wood',     name:'wood',      phet:400,", "{id:'wood',     name:'wood',      phet:450,", "p"],
    ["PhET's lead 11342 -> 11340", "{id:'lead',     name:'lead',      phet:11342,", "{id:'lead',     name:'lead',      phet:11340,", "p"],
    ["PhET's aluminium 2700 -> 2698.9", "{id:'aluminum', name:'aluminium', phet:2700,", "{id:'aluminum', name:'aluminium', phet:2698.9,", "p"],
    ["the mass range drops the litre conversion", "return [clamp(rho*VMIN_L/LITERS,MMIN,MMAX),clamp(rho*VMAX_L/LITERS,MMIN,MMAX)];",
     "return [clamp(rho*VMIN_L,MMIN,MMAX),clamp(rho*VMAX_L,MMIN,MMAX)];", "p"],
    ["PhET's mass ceiling 27 -> 30", "MMAX=27,", "MMAX=30,", "p"],
    ["PhET's volume ceiling 10 L -> 12 L", "VMAX_L=10,", "VMAX_L=12,", "p"],
    # ---- the screens --------------------------------------------------------
    ["Compare same-mass: rho = V/m", "return {tag:c.tag, V:c.mv,  rho:mass/c.mv,        col:c.col,idx:i};",
     "return {tag:c.tag, V:c.mv,  rho:c.mv/mass,        col:c.col,idx:i};", "p"],
    ["Compare same-volume uses the same-mass volume", "return {tag:c.tagV,V:volM3, rho:c.vm/volM3,       col:c.col,idx:i};",
     "return {tag:c.tagV,V:c.mv, rho:c.vm/c.mv,       col:c.col,idx:i};", "p"],
    ["Compare same-density gives every block the same VOLUME",
     "return                     {tag:c.tagD,V:c.dv,  rho:rho,              col:c.col,idx:i};",
     "return                     {tag:c.tagD,V:0.005, rho:rho,              col:c.col,idx:i};", "p"],
    ["PhET's same-mass default 5 -> 4 kg", "DENS_SAME_MASS=5,", "DENS_SAME_MASS=4,", "p"],
    ["the first Compare cube 10 L -> 8 L", "mv:0.01,   vm:8,dv:0.006", "mv:0.008,   vm:8,dv:0.006", "p"],
    ["Mystery set 1 C: 19320 -> 19300", "['C','V',0.001,19320]", "['C','V',0.001,19300]", "p"],
    ["Mystery set 2 A: 11340 -> 11000", "['A','M',18,11340]", "['A','M',18,11000]", "p"],
    ["the mystery display rounds to 1 dp, not 2",
     "function disp2(x){ return Math.floor(Math.abs(x)*100+0.5)/100*(x<0?-1:1); }",
     "function disp2(x){ return Math.floor(Math.abs(x)*10+0.5)/10*(x<0?-1:1); }", "p"],
    ["identify divides the wrong way", "const rho=mDisp/VdispL*LITERS;", "const rho=VdispL/mDisp*LITERS;", "p"],
    ["identify drops the litre conversion", "const rho=mDisp/VdispL*LITERS;", "const rho=mDisp/VdispL;", "p"],
    ["identify takes the SECOND nearest material", "return {rho:rho,id:d[0].id,err:d[0].e,gap:d[1].e};",
     "return {rho:rho,id:d[1].id,err:d[1].e,gap:d[0].e};", "p"],
    ["the mystery blocks are NOT held under", "held:st.submerge?-POOL_H:undefined", "held:undefined", "p"],
    ["the shuffled set draws 4 volumes below 7 L, not 3",
     "const lo=shuffleWith(rnd,[1,2,3,4,5,6]).slice(0,3), hi=shuffleWith(rnd,[7,8,9,10]).slice(0,2);",
     "const lo=shuffleWith(rnd,[1,2,3,4,5,6]).slice(0,4), hi=shuffleWith(rnd,[7,8,9,10]).slice(0,1);", "p"],
    ["the shuffled set may repeat a material", "const rnd=lcg(seed), mats=shuffleWith(rnd,DENSITY_TABLE).slice(0,5);",
     "const rnd=lcg(seed), mats=[0,1,2,3,4].map(()=>DENSITY_TABLE[Math.floor(rnd()*13)]);", "p"],
    # ---- PhET's mass/volume coupling ---------------------------------------
    ["a real material no longer forces V = m/rho", "const V=clamp(m/MAT[mat].phet*LITERS,VMIN_L,VMAX_L);",
     "const V=clamp(m*MAT[mat].phet/LITERS,VMIN_L,VMAX_L);", "p"],
    ["setVol does not drive the mass for a real material", "if(!custom) setMass(st,w,MAT[mat].phet*V/LITERS);",
     "if(false) setMass(st,w,MAT[mat].phet*V/LITERS);", "p"],
    ["custom density taken as V/m", "return m/V;", "return V/m;", "p"],
    # ---- the UI -------------------------------------------------------------
    ["the drag never marks the frame dirty",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.pool=null; dirty=true;",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.pool=null;", "u"],
    ["the grab keeps no offset, so the block jumps", "DRAG.what=bk.tag; DRAG.off=bk.yb-map.wy(y); return true;",
     "DRAG.what=bk.tag; DRAG.off=0; return true;", "u"],
    ["releasing does not let the block go", "if(DRAG.what==='A') ST.holdA=null; else if(DRAG.what==='B') ST.holdB=null;",
     "if(false) ST.holdA=null;", "u"],
    ["the hold is not clamped to the pool floor",
     "const yb=clamp(map.wy(y)+DRAG.off,-POOL_H,holdCeiling(sB));",
     "const yb=map.wy(y)+DRAG.off;", "u"],
    ["the hold ceiling forgets the block's own height", "function holdCeiling(s){ return POOL_YTOP-s-0.012; }",
     "function holdCeiling(s){ return POOL_YTOP-0.012; }", "u"],
    ["the reference force is the FIRST block's weight, not the biggest",
     "Fref=Math.max(Fref,b.W,b.Fb,Math.abs(b.mode==='held'?b.hand:b.N));",
     "Fref=Math.max(1,b.W);", "p"],
    ["the arrow length ignores the room available",
     "return {len:Math.max(0.035,Math.min(0.13,room)),Fref:Fref};",
     "return {len:0.13,Fref:Fref};", "p"],
    ["the arrow length is not proportional to the force",
     "return {W:len*fr(bk.W),Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};",
     "return {W:len,Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};", "p"],
    ["a pointer-down anywhere grabs the block", "if(x>=X0&&x<=X1&&y>=Y0&&y<=Y1){ DRAG.what=bk.tag;",
     "if(true){ DRAG.what=bk.tag;", "u"],
    ["the panel is redrawn but never re-synced", "syncPanel(); dirty=true; refresh(); });\n    rows[key]={row:rowEl,sync,input:inp};",
     "dirty=true; refresh(); });\n    rows[key]={row:rowEl,sync,input:inp};", "u"],
    ["reset all keeps the view AND everything else", "btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v;",
     "btn('reset all',()=>{ const v=st.view; st.view=v;", "u"],
    ["the B rows stay live when there is one block", "matChipsB.hidden=!(v==='pool'&&st.two);",
     "matChipsB.hidden=false;", "u"],
]

script = io.open(sim, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = [(lab, script.count(old)) for lab, old, _, _ in M if script.count(old) != 1]
for lab, n in bad:
    print('PATTERN %s: %d matches — %s' % ('MISSING' if n == 0 else 'AMBIGUOUS', n, lab))
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=1))
print('%d mutants (%d physics, %d ui), %d bad patterns'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u'), len(bad)))
