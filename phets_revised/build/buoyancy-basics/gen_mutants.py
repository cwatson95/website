#!/usr/bin/env python3
"""Write mutants.json for buoyancy-basics.html.

The engine is the same file as density.html's, so the shared-engine mutants are
the same; what is new here is the fluids, the two scales, the pool scale as an
obstacle in the free-surface solve, the face-pressure view, the lowering curve
and the float-or-sink grid.  `old` must appear exactly once in the extracted
script, which is checked here.
"""
import io
import json
import os

here = os.path.dirname(os.path.abspath(__file__))
sim = os.path.abspath(os.path.join(here, '..', '..', 'buoyancy-basics.html'))

M = [
    # ---- the shared engine -------------------------------------------------
    ["POOL_H: 0.15 -> 0.1", "POOL_H=0.15/0.9/0.4", "POOL_H=0.1/0.9/0.4", "p"],
    ["A_POOL: W*D -> W*W", "const A_POOL=POOL_W*POOL_D;", "const A_POOL=POOL_W*POOL_W;", "p"],
    ["VF0: 0.1 -> 0.12", "const VF0=0.1;", "const VF0=0.12;", "p"],
    ["netFluid ADDS the displaced volume", "t-=blockState(b,yw,rhoF).Vsub", "t+=blockState(b,yw,rhoF).Vsub", "p"],
    ["netFluid ignores the obstacles", "return t-obstacleVolume(obs,yw);", "return t;", "p"],
    ["poolLevel takes the SUPREMUM instead of the infimum",
     "if(netFluid(mid,blocks,obs,rhoF)<Vf) lo=mid; else hi=mid;",
     "if(netFluid(mid,blocks,obs,rhoF)<=Vf) hi=mid; else lo=mid;", "p"],
    ["poolLevel: 80 halvings -> 8", "const n=nit||80;", "const n=nit||8;", "p"],
    ["obstacleVolume: clamp top at 2h", "t+=o.a*clamp(yw-o.y0,0,o.h)", "t+=o.a*clamp(yw-o.y0,0,2*o.h)", "p"],
    ["cubeSide: V^(1/3) -> V^(1/2)", "return Math.pow(V,1/3);", "return Math.pow(V,1/2);", "p"],
    ["cubeBelow: s*s -> s", "return s*s*(yw-yb);", "return s*(yw-yb);", "p"],
    ["cubeBelow saturates at s^3, not V", "if(yw>=yb+s) return V;", "if(yw>=yb+s) return s*s*s;", "p"],
    ["floatDraft: rho_b/rho_f -> rho_f/rho_b", "return cubeSide(V)*rho/rhoF;", "return cubeSide(V)*rhoF/rho;", "p"],
    ["the floating displaced volume drops rho_b/rho_f",
     "return {Vsub:b.V*b.rho/rhoF,yb:yb,mode:'float',s:s};",
     "return {Vsub:b.V,yb:yb,mode:'float',s:s};", "p"],
    ["float/sink decided by mass, not density", "if(b.rho<rhoF){", "if(b.rho*b.V<rhoF){", "p"],
    ["submergedFraction: min -> max", "return Math.min(1,rho/rhoF);", "return Math.max(1,rho/rhoF);", "p"],
    ["apparentWeight: sign of the upthrust", "return rho*V*G-rhoF*G*(Vsub===undefined?V:Vsub);",
     "return rho*V*G+rhoF*G*(Vsub===undefined?V:Vsub);", "p"],
    ["riseFloating uses rho_f twice", "function riseFloating(m,rhoF){ return m/(rhoF*A_POOL); }",
     "function riseFloating(m,rhoF){ return m/(rhoF*rhoF*A_POOL); }", "p"],
    ["riseSunk: V/A -> V*A", "function riseSunk(V){ return V/A_POOL; }", "function riseSunk(V){ return V*A_POOL; }", "p"],
    ["the buoyant force drops g", "const st=blockState(b,yw,rhoF), m=b.rho*b.V, W=m*G, Fb=rhoF*G*st.Vsub;",
     "const st=blockState(b,yw,rhoF), m=b.rho*b.V, W=m*G, Fb=rhoF*st.Vsub;", "p"],
    ["the contact force uses W+Fb", "const N=(st.mode==='rest')?(W-Fb):0;",
     "const N=(st.mode==='rest')?(W+Fb):0;", "p"],
    ["a floating or held block is given a contact force too", "const N=(st.mode==='rest')?(W-Fb):0;",
     "const N=(W-Fb);", "p"],
    ["the hand force drops the upthrust", "const hand=(st.mode==='held')?(W-Fb):0;",
     "const hand=(st.mode==='held')?W:0;", "p"],
    ["an out-of-pool block still displaces", "if(b.inPool===false) return {Vsub:0,",
     "if(b.inPool===false) return {Vsub:b.V,", "p"],
    # ---- the pressure on the faces -----------------------------------------
    ["the bottom-face pressure drops rho", "const pBot=yb<yw?rhoF*G*(yw-yb):0",
     "const pBot=yb<yw?G*(yw-yb):0", "p"],
    ["the net face force uses pBot+pTop", "net:(pBot-pTop)*A", "net:(pBot+pTop)*A", "p"],
    ["the side-face pressure is taken at the BOTTOM, not the mid-depth",
     "const side=rhoF*G*(yw-0.5*(yb+yl))*s*dsub;", "const side=rhoF*G*(yw-yb)*s*dsub;", "p"],
    ["the top face is wetted even above the surface", "pTop=yt<yw?rhoF*G*(yw-yt):0;",
     "pTop=rhoF*G*(yw-yt);", "p"],
    ["the wetted strip of a side face ignores the surface", "const yl=Math.min(yw,yt), dsub=Math.max(0,yl-yb);",
     "const yl=yt, dsub=Math.max(0,yl-yb);", "p"],
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
    ["PhET's mercury 13593 -> 13546", "{id:'mercury',  name:'mercury',   phet:13593,",
     "{id:'mercury',  name:'mercury',   phet:13546,", "p"],
    ["PhET's gasoline 680 -> 750", "{id:'gasoline', name:'gasoline',  phet:680,",
     "{id:'gasoline', name:'gasoline',  phet:750,", "p"],
    ["PhET's wood 400 -> 450", "{id:'wood',     name:'wood',      phet:400,", "{id:'wood',     name:'wood',      phet:450,", "p"],
    ["PhET's aluminium 2700 -> 2698.9", "{id:'aluminum', name:'aluminium', phet:2700,", "{id:'aluminum', name:'aluminium', phet:2698.9,", "p"],
    ["the fluid list drops seawater", "const BUOY_FLUIDS=['gasoline','oil','water','seawater','honey','mercury'];",
     "const BUOY_FLUIDS=['gasoline','oil','water','honey','mercury'];", "p"],
    ["the mass range drops the litre conversion", "return [clamp(rho*VMIN_L/LITERS,MMIN,MMAX),clamp(rho*VMAX_L/LITERS,MMIN,MMAX)];",
     "return [clamp(rho*VMIN_L,MMIN,MMAX),clamp(rho*VMAX_L,MMIN,MMAX)];", "p"],
    ["PhET's mass ceiling 27 -> 30", "MMAX=27,", "MMAX=30,", "p"],
    # ---- the scales ---------------------------------------------------------
    ["the scale's own volume: 0.15 x 0.06 x 0.2 -> half the depth",
     "const SCALE_W=0.15, SCALE_H=0.06, SCALE_D=0.2, SCALE_V=SCALE_W*SCALE_H*SCALE_D;",
     "const SCALE_W=0.15, SCALE_H=0.06, SCALE_D=0.1, SCALE_V=SCALE_W*SCALE_H*SCALE_D;", "p"],
    ["the pool scale's height ignores its own thickness",
     "function poolScaleY0(st){ return -POOL_H+st.scaleH*(POOL_H-SCALE_H); }",
     "function poolScaleY0(st){ return -POOL_H+st.scaleH*POOL_H; }", "p"],
    ["the pool scale's top is its base", "function poolScaleTop(st){ return poolScaleY0(st)+SCALE_H; }",
     "function poolScaleTop(st){ return poolScaleY0(st); }", "p"],
    ["a block on the pool scale still sits on the floor",
     "support:onScale?poolScaleTop(st):(onGround?SCALE_H:-POOL_H),",
     "support:onGround?SCALE_H:-POOL_H,", "p"],
    ["a block on the ground scale is still in the pool", "inPool:!onGround,", "inPool:true,", "p"],
    ["the ground scale reads a block out of the pool as if it were in it",
     "const groundReads=(st.where==='ground')?A.W:0;",
     "const groundReads=(st.where==='ground')?A.N:0;", "p"],
    ["the pool scale reads the weight, not the contact force",
     "const poolReads=(st.where==='poolscale')?A.N:0;",
     "const poolReads=(st.where==='poolscale')?A.W:0;", "p"],
    # ---- the Compare screen -------------------------------------------------
    ["PhET's same-mass default 4 -> 5 kg", "BB_SAME_MASS=4,", "BB_SAME_MASS=5,", "p"],
    ["PhET's same-density default is water, not wood", "BB_SAME_RHO=400;", "BB_SAME_RHO=1000;", "p"],
    ["the brick cube is 2 L, not 3", "{tag:'A',tagV:'A',tagD:'A',mv:0.002,vm:10,dv:0.005,col:'#c08a3c'},",
     "{tag:'A',tagV:'A',tagD:'A',mv:0.003,vm:10,dv:0.005,col:'#c08a3c'},", "p"],
    ["Compare same-mass: rho = V/m", "return {tag:c.tag, V:c.mv,  rho:mass/c.mv,        col:c.col,idx:i};",
     "return {tag:c.tag, V:c.mv,  rho:c.mv/mass,        col:c.col,idx:i};", "p"],
    ["Compare same-volume uses the same-mass volume", "return {tag:c.tagV,V:volM3, rho:c.vm/volM3,       col:c.col,idx:i};",
     "return {tag:c.tagV,V:c.mv, rho:c.vm/c.mv,       col:c.col,idx:i};", "p"],
    # ---- the lowering curve -------------------------------------------------
    ["the lowering starts below the surface, not above",
     "const top=poolLevel([],[],MAT[st.fluid].phet,VF0)+0.02;",
     "const top=poolLevel([],[],MAT[st.fluid].phet,VF0)-0.02;", "p"],
    ["the lowering ends above the floor", "const bot=-POOL_H;", "const bot=-POOL_H+0.05;", "p"],
    ["the lowering is not clamped to 0..1", "return top+(bot-top)*clamp(st.lowered,0,1);",
     "return top+(bot-top)*st.lowered;", "p"],
    ["the scale reading is allowed to go negative", "const read=Math.max(0,b.W-b.Fb);", "const read=b.W-b.Fb;", "p"],
    ["the lowering curve is built from 24 points, not 241", "const curve=[], N=241;", "const curve=[], N=24;", "p"],
    # ---- the grid -----------------------------------------------------------
    ["a grid cell floats when rho_b <= rho_f, so a neutral block floats",
     "floats:m.phet<f.rho,", "floats:m.phet<=f.rho,", "p"],
    ["the grid's fraction ignores the cap at 1", "grid=rows.map(m=>cols.map(f=>({frac:submergedFraction(m.phet,f.rho),",
     "grid=rows.map(m=>cols.map(f=>({frac:m.phet/f.rho,", "p"],
    ["the grid rows are not sorted by density", "const rows=MATERIALS.filter(m=>m.id!=='air').slice().sort((a,b)=>a.phet-b.phet);",
     "const rows=MATERIALS.filter(m=>m.id!=='air').slice();", "p"],
    ["the mercury float count counts the fluid itself", "mercuryFloats:rows.filter(m=>m.phet<MAT.mercury.phet).length,",
     "mercuryFloats:rows.filter(m=>m.phet<=MAT.mercury.phet).length,", "p"],
    # ---- the drawing scales -------------------------------------------------
    ["the reference force is the FIRST block's weight, not the biggest",
     "Fref=Math.max(Fref,b.W,b.Fb,Math.abs(b.mode==='held'?b.hand:b.N));", "Fref=Math.max(1,b.W);", "p"],
    ["the arrow length ignores the room available",
     "return {len:Math.max(0.035,Math.min(0.13,room)),Fref:Fref};", "return {len:0.13,Fref:Fref};", "p"],
    ["the arrow length is not proportional to the force",
     "return {W:len*fr(bk.W),Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};",
     "return {W:len,Fb:len*fr(bk.Fb),extra:len*fr(extra),sign:extra>0?1:-1,raw:extra};", "p"],
    ["the hold ceiling forgets the block's own height", "function holdCeiling(s){ return POOL_YTOP-s-0.012; }",
     "function holdCeiling(s){ return POOL_YTOP-0.012; }", "p"],
    # ---- the UI -------------------------------------------------------------
    ["the drag never marks the frame dirty",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.explore=null; dirty=true;",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ MEMO.explore=null;", "u"],
    ["the grab keeps no offset, so the block jumps", "DRAG.what=bk.tag; DRAG.off=bk.yb-map.wy(y); return true;",
     "DRAG.what=bk.tag; DRAG.off=0; return true;", "u"],
    ["releasing does not let the block go", "if(DRAG.what==='A') ST.holdA=null; else if(DRAG.what==='B') ST.holdB=null;",
     "if(false) ST.holdA=null;", "u"],
    ["the hold is not clamped", "const yb=clamp(map.wy(y)+DRAG.off,-POOL_H,holdCeiling(sB));",
     "const yb=map.wy(y)+DRAG.off;", "u"],
    ["a block out of the pool can still be grabbed", "if(bk.mode==='out') continue;", "if(false) continue;", "u"],
    ["the panel is redrawn but never re-synced",
     "clearAll(); syncPanel(); dirty=true; refresh(); });\n    rows[key]={row:rowEl,sync,input:inp};",
     "clearAll(); dirty=true; refresh(); });\n    rows[key]={row:rowEl,sync,input:inp};", "u"],
    ["reset all keeps the view AND everything else", "btn('reset all',()=>{ const v=st.view; Object.assign(st,DEFAULTS); st.view=v;",
     "btn('reset all',()=>{ const v=st.view; st.view=v;", "u"],
    ["the B rows stay live when there is one block", "matChipsB.hidden=!(v==='explore'&&st.two);",
     "matChipsB.hidden=false;", "u"],
    ["the fluid group stays live on the float-or-sink view", "gFluid.hidden=(v==='fluids');", "gFluid.hidden=false;", "u"],
    ["the pool-scale height slider is live everywhere", "gScales.hidden=!(v==='explore'||v==='sets');",
     "gScales.hidden=false;", "u"],
]

script = io.open(sim, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = [(lab, script.count(old)) for lab, old, _, _ in M if script.count(old) != 1]
for lab, n in bad:
    print('PATTERN %s: %d matches — %s' % ('MISSING' if n == 0 else 'AMBIGUOUS', n, lab))
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=1))
print('%d mutants (%d physics, %d ui), %d bad patterns'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u'), len(bad)))
