#!/usr/bin/env python3
"""Write mutants.json for tools/mutate.py, checking every pattern occurs
exactly once in the extracted script (a pattern that matches twice mutates two
places; one that matches none is a mutant you think you ran and did not).

Categories: PhET's constants and control grids, the collision algebra, the
divider and the placement, the exact kinetic theory this sim measures against
(the one-sided flux, the effusion time, the relative speed, the collision
swath, the Maxwell-Boltzmann bins), the drawing, and the UI (the divider drag,
the dirty flags, the frame loop).

The sweep is run against a COPY of the html inside _out/ — never
docs/phets_revised/diffusion.html in place — because mutate.py writes its
scratch _mutant.js next to the html it tests and parallel agents would share
one docs/phets_revised/_mutant.js.
"""
import io, json, os
here = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(here, '_out', 'run.js'), encoding='utf-8').read()
M = [
    # --- PhET's constants and the Diffusion control grids
    ('BOLTZMANN 8316 -> 8314 (CODATA)', 'K:8316,', 'K:8314,', 'p'),
    ('pressure scale 1.66e6 -> 1.66e5', 'P_SCALE:1.66e6,', 'P_SCALE:1.66e5,', 'p'),
    ('atm per kPa 0.00986923 -> 0.0098692', 'ATM_PER_KPA:0.00986923,', 'ATM_PER_KPA:0.0098692,', 'p'),
    ('container height 8750 -> 8700', 'H:8750, D:4000, WALL:75,', 'H:8700, D:4000, WALL:75,', 'p'),
    ('container depth 4000 -> 4500', 'H:8750, D:4000, WALL:75,', 'H:8750, D:4500, WALL:75,', 'p'),
    ('frame 2.5/60 -> 2.5/50 ps', 'DT_FRAME:2.5/60,', 'DT_FRAME:2.5/50,', 'p'),
    ('slow 0.3/60 -> 0.6/60 ps', 'DT_SLOW:0.3/60,', 'DT_SLOW:0.6/60,', 'p'),
    ('step button 0.2 -> 0.25 ps', 'STEP:0.2,', 'STEP:0.25,', 'p'),
    ('Diffusion box 16000 -> 15000 pm', 'DIFF_W:16000, DIVIDER:100,', 'DIFF_W:15000, DIVIDER:100,', 'p'),
    ('divider 100 -> 200 pm', 'DIFF_W:16000, DIVIDER:100,', 'DIFF_W:16000, DIVIDER:200,', 'p'),
    ('count range 200/10 -> 200/20',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,',
     'DIFF_NMAX:200, DIFF_DN:20, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,', 'p'),
    ('mass range 4-32 -> 4-30',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,30], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,', 'p'),
    ('radius step 5 -> 10',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:10, DIFF_T:[50,500], DIFF_TSTEP:50,', 'p'),
    ('temperature range 50-500 -> 50-400',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,500], DIFF_TSTEP:50,',
     'DIFF_NMAX:200, DIFF_DN:10, DIFF_M:[4,32], DIFF_R:[50,250], DIFF_RSTEP:5, DIFF_T:[50,400], DIFF_TSTEP:50,', 'p'),
    ('flow window 300 -> 150 frames', 'FLOW_WINDOW:300', 'FLOW_WINDOW:150', 'p'),
    # --- PhET's definitions
    ('T = (2/3)<KE>/k -> (1/2)', 'return n?(2/3)*gasEnergy(g,k)/n/GAS.K:null;', 'return n?(1/2)*gasEnergy(g,k)/n/GAS.K:null;', 'p'),
    ('P = NkT/V -> (N+1)kT/V', 'return N*GAS.K*(T||0)/V*GAS.P_SCALE;', 'return (N+1)*GAS.K*(T||0)/V*GAS.P_SCALE;', 'p'),
    ('kT2 = (3/2)kT -> kT', 'function gasKT2(T){ return 1.5*GAS.K*T; }', 'function gasKT2(T){ return 1.0*GAS.K*T; }', 'p'),
    # --- the exact 2-D Maxwell-Boltzmann laws
    ('MB mean speed 2m -> 4m', 'return Math.sqrt(Math.PI*kT2/(2*m));', 'return Math.sqrt(Math.PI*kT2/(4*m));', 'p'),
    ('MB rms 2kT2 -> 3kT2', 'function mbRmsSpeed(m,kT2){ return Math.sqrt(2*kT2/m); }', 'function mbRmsSpeed(m,kT2){ return Math.sqrt(3*kT2/m); }', 'p'),
    ('MB speed cdf 2kT2 -> 3kT2', 'return v<=0?0:-Math.expm1(-m*v*v/(2*kT2));', 'return v<=0?0:-Math.expm1(-m*v*v/(3*kT2));', 'p'),
    ('MB mode sqrt(kT2/m) -> sqrt(2kT2/m)', 'function mbModeSpeed(m,kT2){ return Math.sqrt(kT2/m); }',
     'function mbModeSpeed(m,kT2){ return Math.sqrt(2*kT2/m); }', 'p'),
    ('the speed bins 20 x 150 -> 20 x 175 m/s', 'const SPD_NB=20, SPD_BW=150;', 'const SPD_NB=20, SPD_BW=175;', 'p'),
    # --- THIS sim's kinetic theory
    ('one-sided flux <vx+> = sqrt(kT2/2 pi m) -> sqrt(kT2/pi m)',
     'function vxPlus(m,T){ return T===null||!(T>0)?null:Math.sqrt(gasKT2(T)/(2*PI*m)); }',
     'function vxPlus(m,T){ return T===null||!(T>0)?null:Math.sqrt(gasKT2(T)/(PI*m)); }', 'p'),
    ('flow rate: the excluded half-width W/2 - r -> W/2',
     'const halfW=g.W/2-g.species[k].r;', 'const halfW=g.W/2;', 'p'),
    ('flow rate: divided by the FULL width, not the half',
     'return halfW>0?nSide*v/halfW:null;', 'return halfW>0?nSide*v/(2*halfW):null;', 'p'),
    ('effusion tau: (W - 2r)/4<vx+> -> (W - 2r)/2<vx+>',
     'return v===null?null:(g.W-2*g.species[k].r)/(4*v);',
     'return v===null?null:(g.W-2*g.species[k].r)/(2*v);', 'p'),
    ('<v_rel>: sqrt(pi/2) -> sqrt(pi)', 'return Math.sqrt(PI*s2/2);', 'return Math.sqrt(PI*s2);', 'p'),
    ('<v_rel>: the two variances subtracted, not added',
     'const s2=gasKT2(Tk)/g.species[k].m+gasKT2(Tj)/g.species[j].m;',
     'const s2=Math.abs(gasKT2(Tk)/g.species[k].m-gasKT2(Tj)/g.species[j].m)+1e-30;', 'p'),
    ('the collision swath 2(r_k+r_j) -> (r_k+r_j)  [the factor this sim FOUND]',
     's+=nj/A*2*(g.species[k].r+g.species[j].r)*vr;',
     's+=nj/A*(g.species[k].r+g.species[j].r)*vr;', 'p'),
    ('the swath uses one radius, not the sum',
     's+=nj/A*2*(g.species[k].r+g.species[j].r)*vr;',
     's+=nj/A*2*(g.species[k].r)*vr;', 'p'),
    ('pair rate: every collision counted twice', 'return s/2;', 'return s;', 'p'),
    ('mean free path <v>/z -> <v>/(2z)',
     'return (T===null||z===null||!(z>0))?null:mbMeanSpeed(g.species[k].m,gasKT2(T))/z;',
     'return (T===null||z===null||!(z>0))?null:mbMeanSpeed(g.species[k].m,gasKT2(T))/(2*z);', 'p'),
    ('D = <v> lambda/2 -> <v> lambda',
     'return (T===null||l===null)?null:mbMeanSpeed(g.species[k].m,gasKT2(T))*l/2;',
     'return (T===null||l===null)?null:mbMeanSpeed(g.species[k].m,gasKT2(T))*l;', 'p'),
    ('tau_D = W^2/(pi^2 D) -> W^2/(pi D)',
     'return (D===null||!(D>0))?null:g.W*g.W/(PI*PI*D);',
     'return (D===null||!(D>0))?null:g.W*g.W/(PI*D);', 'p'),
    ('the common temperature: number-weighted -> plain mean',
     'M.Tmix=(n0+n1)?((n0*(M.Tsp[0]||0)+n1*(M.Tsp[1]||0))/(n0+n1)):null;',
     'M.Tmix=(n0+n1)?(((M.Tsp[0]||0)+(M.Tsp[1]||0))/2):null;', 'p'),
    ('Graham: sqrt(m1/m2) -> m1/m2', 'M.graham=Math.sqrt(g.species[0].m/g.species[1].m);',
     'M.graham=g.species[0].m/g.species[1].m;', 'p'),
    # --- the collision algebra and the placement
    ('contact time: the later root', 'return c/(-b+Math.sqrt(d));', 'return c/(-b-Math.sqrt(d));', 'p'),
    ('overlap test c<0 -> c<-1', 'if(c<0) return Infinity;', 'if(c<-1) return Infinity;', 'p'),
    ('impulse: masses swapped', 'const M=mi+mj, ci=2*mj/M*gn, cj=2*mi/M*gn;', 'const M=mi+mj, ci=2*mi/M*gn, cj=2*mj/M*gn;', 'p'),
    ('impulse: half strength', 'g.vx[i]-=ci*nx; g.vy[i]-=ci*ny; g.vx[j]+=cj*nx; g.vy[j]+=cj*ny;',
     'g.vx[i]-=0.5*ci*nx; g.vy[i]-=0.5*ci*ny; g.vx[j]+=0.5*cj*nx; g.vy[j]+=0.5*cj*ny;', 'p'),
    ('PhET placement speed sqrt(3kT/m) -> sqrt(2kT/m)',
     'const S=g.species[k], R=g.rng, v=Math.sqrt(3*GAS.K*T/S.m);',
     'const S=g.species[k], R=g.rng, v=Math.sqrt(2*GAS.K*T/S.m);', 'p'),
    ('a new mass/temperature no longer re-speeds the species',
     'const s=gasSpeed(g,i); if(s>0){ g.vx[i]*=v/s; g.vy[i]*=v/s; } else { g.vx[i]=v; g.vy[i]=0; } }',
     '}', 'p'),
    ('the divider stops confining species 1',
     "function gasXhi(g,k){ return (g.divided&&k===0)?g.dividerX-g.dividerHalf:0; }",
     "function gasXhi(g,k){ return 0; }", 'p'),
    ('the divider sits a quarter of the way along, not the middle',
     'function gasSetDivided(g,on){ g.divided=!!on; g.dividerX=g.left+g.W/2; }',
     'function gasSetDivided(g,on){ g.divided=!!on; g.dividerX=g.left+g.W/4; }', 'p'),
    ('species 2 is scattered into the LEFT half too',
     'return k===0?[g.left,mid-g.dividerHalf]:[mid+g.dividerHalf,0];',
     'return [g.left,mid-g.dividerHalf];', 'p'),
    ('the COM is measured from the left wall, not the middle',
     'return sm>0?sx/sm-(g.left+g.W/2):null;', 'return sm>0?sx/sm-g.left:null;', 'p'),
    ('the flow counts crossings the wrong way round',
     'if(g.px[i]>=g.dividerX&&g.x[i]<g.dividerX) cL[k]++; else if(g.px[i]<=g.dividerX&&g.x[i]>g.dividerX) cR[k]++; }',
     'if(g.px[i]>=g.dividerX&&g.x[i]<g.dividerX) cR[k]++; else if(g.px[i]<=g.dividerX&&g.x[i]>g.dividerX) cL[k]++; }', 'p'),
    ('the side split uses the left wall, not the divider',
     "const s=g.x[i]<g.dividerX?0:1;", "const s=g.x[i]<g.left+g.W/4?0:1;", 'p'),
    # --- this sim's own bookkeeping
    ('the imbalance is not normalised by the count',
     "return n?(side[0]['n'+k]-side[1]['n'+k])/n:null;",
     "return n?(side[0]['n'+k]-side[1]['n'+k]):null;", 'p'),
    ('the profile bins 32 -> 16', 'const NPROF=32;', 'const NPROF=16;', 'p'),
    ('the pair window counts cumulative hits, not the increment',
     'w.pairs.push([dt,g.stats.pairHits-(w.lastPairs||0)]);',
     'w.pairs.push([dt,g.stats.pairHits]);', 'p'),
    ('reset divider does not regenerate (PhET restarts)',
     'gasDiffRestart(g,st.d1n,st.d1T,st.d2n,st.d2T); st.divided=true;',
     'gasSetDivided(g,true); st.divided=true;', 'p'),
    ('the caption clears the #hint by 18 px -> 0', 'const HINT_H=18;', 'const HINT_H=0;', 'p'),
    # --- the UI
    ('the divider drag removes it at 50 % of the travel',
     'w.divLift=clamp((DRAG.y0-y)/DIV_TRAVEL,0,1);',
     'w.divLift=clamp((DRAG.y0-y)/DIV_TRAVEL*2,0,1);', 'u'),
    ('the divider drag never removes it',
     'if(w.divLift>=1&&M.g.divided){ removeDivider(w,ST); DRAG.what=null; w.divLift=0; }',
     'if(false){ removeDivider(w,ST); DRAG.what=null; w.divLift=0; }', 'u'),
    ('the divider handle is not grabbable',
     'if(k&&x>=k.x-6&&x<=k.x+k.w+6&&y>=k.y-6&&y<=k.y+k.h+6){ DRAG.what=\'divider\'; DRAG.y0=y; w.divLift=0; return true; }',
     'if(false){ DRAG.what=\'divider\'; DRAG.y0=y; w.divLift=0; return true; }', 'u'),
    ('drag: the pointer handler stops dirtying the canvas',
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }",
     "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); }", 'u'),
    ('drag: a move no longer dirties',
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; roEl.innerHTML=readoutHTML(S.model()); }",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ roEl.innerHTML=readoutHTML(S.model()); }", 'u'),
    ('the frame loop stops honouring the dirty flag', 'if(advanced||dirty){', 'if(advanced){', 'u'),
    ('the step key steps 0.2 -> 0.4 ps',
     'S.stepOnce=function(){ worldStep(worldOf(),ST,GAS.STEP); if(S.onCounts) S.onCounts(); };',
     'S.stepOnce=function(){ worldStep(worldOf(),ST,2*GAS.STEP); if(S.onCounts) S.onCounts(); };', 'u'),
    ('slow mode is ignored by the clock', 'function viewDt(st){ return st.slow?GAS.DT_SLOW:GAS.DT_FRAME; }',
     'function viewDt(st){ return GAS.DT_FRAME; }', 'u'),
    ('the views stop sharing one gas', "function worldKey(){ return 'box'; }", "function worldKey(v){ return v||'box'; }", 'u'),
    ('the Maxwell-Boltzmann checkbox is ignored', 'if(M.st.showMB) for(const k of [0,1]){', 'if(true) for(const k of [0,1]){', 'u'),
]
bad = []
for label, old, new, suite in M:
    n = js.count(old)
    if n != 1:
        bad.append('%s: pattern matches %d times' % (label, n))
    if old == new:
        bad.append('%s: no-op mutant' % label)
labels = [m[0] for m in M]
if len(set(labels)) != len(labels):
    bad.append('duplicate labels')
if bad:
    raise SystemExit('\n'.join(bad))
io.open(os.path.join(here, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps([list(m) for m in M], indent=1, ensure_ascii=False) + '\n')
print('%d mutants (%d physics, %d UI)' % (len(M), sum(1 for m in M if m[3] == 'p'),
                                          sum(1 for m in M if m[3] == 'u')))
