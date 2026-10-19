#!/usr/bin/env python3
"""Write mutants.json and check every pattern matches EXACTLY ONCE in the
extracted script (a pattern that matches twice mutates two places; one that
matches none is a mutant you think you ran and did not).

Usage: python3 gen_mutants.py [basics]"""
import io, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
basics = len(sys.argv) > 1 and sys.argv[1] == 'basics'
dest = os.path.join(here, '..', 'molecule-shapes-basics') if basics else here
stem = 'molecule-shapes-basics' if basics else 'molecule-shapes'
html = os.path.abspath(os.path.join(here, '..', '..', stem + '.html'))
src = io.open(html, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]

M = []


def m(label, old, new, suite='p'):
    M.append([label, old, new, suite])


# ---- the model: constants, slots, energy, relaxation
m('the pair energy exponent 2 -> 3', 'const EXPN=2;', 'const EXPN=3;')
m("PhET's lone-pair radius 0.7 -> 0.6", 'const RHO_PHET=7/10;', 'const RHO_PHET=6/10;')
m('the descent step 0.1 -> 0.2', 'const ETA=0.1, GTOL=1e-13', 'const ETA=0.2, GTOL=1e-13')
m('the convergence tolerance 1e-13 -> 1e-9', 'GTOL=1e-13, ITMAX', 'GTOL=1e-9, ITMAX')
m("PhET's six pairs -> seven", 'const MAXG=6;', 'const MAXG=7;')
m('the tetrahedral angle arccos(-1/3) -> arccos(-1/4)', 'const TET=Math.acos(-1/3)*RAD;', 'const TET=Math.acos(-1/4)*RAD;')
m('the tetrahedron slot elevation -1/3 -> -1/4', '[T8,0,-1/3]', '[T8,0,-1/4]')
m('the trigonal slot -0.5 -> -0.4', '3:[[0,0,1],[SQ3/2,0,-0.5],[-SQ3/2,0,-0.5]],', '3:[[0,0,1],[SQ3/2,0,-0.4],[-SQ3/2,0,-0.4]],')
m('lone pairs take the AXIAL bipyramid slots first',
  '5:[[1,0,0],[-0.5,SQ3/2,0],[-0.5,-SQ3/2,0],[0,0,1],[0,0,-1]],',
  '5:[[0,0,1],[0,0,-1],[1,0,0],[-0.5,SQ3/2,0],[-0.5,-SQ3/2,0]],')
m('lone pairs take CIS octahedral slots first',
  '6:[[0,0,1],[0,0,-1],[1,0,0],[-1,0,0],[0,1,0],[0,-1,0]],',
  '6:[[0,0,1],[1,0,0],[0,0,-1],[-1,0,0],[0,1,0],[0,-1,0]],')
m('the energy power -s/2 -> -s', 'E+=Math.pow(dx*dx+dy*dy+dz*dz,-s/2);', 'E+=Math.pow(dx*dx+dy*dy+dz*dz,-s);')
m('the gradient loses its leading s', 'const w=-s*Math.pow(dx*dx+dy*dy+dz*dz,-s/2-1);', 'const w=-Math.pow(dx*dx+dy*dy+dz*dz,-s/2-1);')
m('the gradient loses the radius chain rule', 'G.push([R[i]*gx,R[i]*gy,R[i]*gz]);', 'G.push([gx,gy,gz]);')
m('the tangential projection changes sign', 'return [g[0]-c*u[0],g[1]-c*u[1],g[2]-c*u[2]];', 'return [g[0]+c*u[0],g[1]+c*u[1],g[2]+c*u[2]];')
m('the descent walks uphill', 'U=U.map((u,i)=>vnorm([u[0]-ETA*Gt[i][0],u[1]-ETA*Gt[i][1],u[2]-ETA*Gt[i][2]]));',
  'U=U.map((u,i)=>vnorm([u[0]+ETA*Gt[i][0],u[1]+ETA*Gt[i][1],u[2]+ETA*Gt[i][2]]));')
m('bonds get the lone pairs\' radius and back', 'out.push((lpSet?lpSet.indexOf(k)>=0:k<e)?rho:1);', 'out.push((lpSet?lpSet.indexOf(k)>=0:k<e)?1:rho);')
m('the isomer ladder merges distinct arrangements', 'if(!found.some(f=>Math.abs(f.E-r.E)<1e-8))', 'if(!found.some(f=>Math.abs(f.E-r.E)<1e-2))')
# ---- the fit
m("Horn's 4x4 loses a sign", 'const N=[[Sxx+Syy+Szz,Syz-Szy,Szx-Sxz,Sxy-Syx],', 'const N=[[Sxx+Syy+Szz,Szy-Syz,Szx-Sxz,Sxy-Syx],')
m('the quaternion to matrix flips a cross term', '[[q0*q0+qx*qx-qy*qy-qz*qz,2*(qx*qy-q0*qz),2*(qx*qz+q0*qy)],',
  '[[q0*q0+qx*qx-qy*qy-qz*qz,2*(qx*qy+q0*qz),2*(qx*qz+q0*qy)],')
m("Jacobi's rotation takes the other root", 'const t=(th>=0?1:-1)/(Math.abs(th)+Math.sqrt(th*th+1))', 'const t=(th>=0?-1:1)/(Math.abs(th)+Math.sqrt(th*th+1))')
m('rotAtoB loses the Rodrigues factor', 'const f=1/(1+c), K=', 'const f=1/(2+c), K=')
# ---- the PRNG and the random starts
m('mulberry32 constant', 'a=a+0x6D2B79F5|0;', 'a=a+0x6D2B79F4|0;')
m('random directions lose the uniform-z map', 'const z=2*rnd()-1,', 'const z=rnd(),')
# ---- PhET's naming rules
m("the AXE rule for x = 2 drops e = 4", "if(x===2) return (e===0||e===3||e===4)?'linear':'bent';", "if(x===2) return (e===0||e===3)?'linear':'bent';")
m('the AXE rule for x = 3 names AX3E3 a seesaw', "if(x===3) return ['trigonalPlanar','trigonalPyramidal','tShaped','tShaped'][e];",
  "if(x===3) return ['trigonalPlanar','trigonalPyramidal','tShaped','seesaw'][e];")
m('the electron geometries of 5 and 6 swap',
  "const EL_GEOM=['empty','diatomic','linear','trigonalPlanar','tetrahedral','trigonalBipyramidal','octahedral'];",
  "const EL_GEOM=['empty','diatomic','linear','trigonalPlanar','tetrahedral','octahedral','trigonalBipyramidal'];")
m('the ideal angles of a class count the lone pairs too', 'const S=SLOTS[n], out=[]; for(let i=e;i<n;i++)', 'const S=SLOTS[n], out=[]; for(let i=0;i<n;i++)')
# ---- PhET's measured data
m("PhET's tetrahedral elevation", 'const PHET_UP=-19.471220333;', 'const PHET_UP=-19.5;')
m("PhET's NH3 polar angle", 'const PHET_NH3_POLAR=1.202623030417028;', 'const PHET_NH3_POLAR=1.2026;')
m("H2O's 104.5 deg", 't=104.5/2*DEG;', 't=104.0/2*DEG;')
m("SF4's axial 173.1 deg", 'const ta=173.1/2*DEG, te=101.6/2*DEG;', 'const ta=172.1/2*DEG, te=101.6/2*DEG;')
m("SF4's equatorial 101.6 deg", 'const ta=173.1/2*DEG, te=101.6/2*DEG;', 'const ta=173.1/2*DEG, te=100.6/2*DEG;')
m("ClF3's 87.5 deg", 't=87.5*DEG;', 't=88.5*DEG;')
m("BrF5's 84.8 deg", 'let t=84.8*DEG;', 'let t=85.8*DEG;')
m("SO2's 119 deg", 't=119/2*DEG;', 't=118/2*DEG;')
m("CO2's double bonds become single", "add('CO2','C',0,1.163,'O',2,2,", "add('CO2','C',0,1.163,'O',2,1,")
m("PCl5's axial bond length 2.14 A", '[[[1,0,0],2.14],[[-1,0,0],2.14]]', '[[[1,0,0],2.12],[[-1,0,0],2.12]]')
m('an outer atom takes a lone-pair slot for its bond', 'const S=SLOTS[k+1], R=rotAtoB(S[k],', 'const S=SLOTS[k+1], R=rotAtoB(S[0],')
m("PhET's frame is no longer turned lone-pairs-up", 'const PHET_TO_WORLD=[[1,0,0],[0,0,-1],[0,1,0]];', 'const PHET_TO_WORLD=[[1,0,0],[0,1,0],[0,0,1]];')
# ---- the views' own quantities
m("PhET's arc threshold for four bonds", 'const ARC_LO=[0,0,0,0.1,0.35,0.45,0.5]', 'const ARC_LO=[0,0,0,0.1,0.30,0.45,0.5]')
m('three bonds always show their arcs', 'if(nb<=2) return 1;', 'if(nb<=3) return 1;')
m('the bent class is compared against 120 deg', 'AX2E2:[2,2,2,3,TET]', 'AX2E2:[2,2,2,3,120]')
m('the camera fitter uses the near-point approximation', 'return R*Math.sqrt(1+(f/want)*(f/want));', 'return R*(1+f/want);')
m('the display frame picks the WORST orientation', 'if(!best||worst>best.worst+1e-12) best={worst,M};', 'if(!best||worst<best.worst-1e-12) best={worst,M};')
m('the pointer grabs the far side of the sphere', 'const t=disc>=0?-ed-Math.sqrt(disc):-ed;', 'const t=disc>=0?-ed+Math.sqrt(disc):-ed;')
m('the flow loses its steering (KS = 0)', 'const FLOW={RATE:1.8, KAP:1, KS:3, SUB:0.03, SNAP:1e-7};', 'const FLOW={RATE:1.8, KAP:1, KS:0, SUB:0.03, SNAP:1e-7};')
m('the flow loses its repulsion (KAP = 0)', 'const FLOW={RATE:1.8, KAP:1, KS:3, SUB:0.03, SNAP:1e-7};', 'const FLOW={RATE:1.8, KAP:0, KS:3, SUB:0.03, SNAP:1e-7};')
m('remove takes the FIRST pair of a kind, not the last', 'for(let i=LIVE.groups.length-1;i>=0;i--) if(LIVE.groups[i].order===order){',
  'for(let i=0;i<LIVE.groups.length;i++) if(LIVE.groups[i].order===order){')
if not basics:
    m('the rho a drag sets is not snapped to the slider step',
      'function rhoAtX(b,x){ return Math.round(clamp(RHO_MIN+(x-b.x)/b.w*(RHO_MAX-RHO_MIN),RHO_MIN,RHO_MAX)*100)/100; }',
      'function rhoAtX(b,x){ return clamp(RHO_MIN+(x-b.x)/b.w*(RHO_MAX-RHO_MIN),RHO_MIN,RHO_MAX); }')
# ---- the UI
m('the camera theta is frozen on a drag', "if(DRAG.what==='orbit'){ ST.camTheta-=dx*0.0075;", "if(DRAG.what==='orbit'){ ST.camTheta-=0*dx*0.0075;", 'u')
m('the camera phi is frozen on a drag', 'ST.camPhi=clamp(ST.camPhi+dy*0.006,-1.45,1.45); return true; }', 'ST.camPhi=clamp(ST.camPhi+0*dy*0.006,-1.45,1.45); return true; }', 'u')
m('a pointer-down no longer marks the frame dirty', "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); dirty=true; }",
  "if(S.pointer('down',e.clientX-r.left,e.clientY-r.top)){ canvas.classList.add('dragging'); }", 'u')
m('a pointer-move no longer marks the frame dirty', "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true; if(st.view==='squeeze') refresh(); }",
  "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ if(st.view==='squeeze') refresh(); }", 'u')
m('the wheel no longer marks the frame dirty', 'if(S.wheel(e.deltaY)) dirty=true; },{passive:false});', 'S.wheel(e.deltaY); },{passive:false});', 'u')
if not basics:      # Basics builds no slider, so the mutant could only survive
    m('a slider no longer repaints', 'val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); refresh(); });',
      'val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); });', 'u')
m('the flow never snaps, so it never goes idle', 'if(dev<FLOW.SNAP&&LIVE.held<0){', 'if(false&&dev<FLOW.SNAP&&LIVE.held<0){', 'u')
m('a grabbed pair stops following the pointer', "g.u=pointerDir(modelGeo(ctx,S.W,S.H).C,x,y,g.order===0?ST.rho:1); LIVE.anim=true; return true; }",
  "LIVE.anim=true; return true; }", 'u')
m('a click on the table is never a click', "if(DRAG.what==='orbit'&&v==='table'&&DRAG.moved<4){", "if(DRAG.what==='orbit'&&v==='table'&&DRAG.moved<0){", 'u')
m('a tab click no longer repaints', 'syncChips(); syncPanel(); refresh();\n  }', 'syncChips(); syncPanel();\n  }', 'u')
m('a checkbox no longer repaints', 'if(onchg) onchg(); syncPanel(); refresh(); });\n    rows[\'cb_\'+key]', 'if(onchg) onchg(); syncPanel(); });\n    rows[\'cb_\'+key]', 'u')
m('a button no longer repaints', 'const b=h(\'button\',{onclick:()=>{ fn(); syncPanel(); refresh(); }},label);', 'const b=h(\'button\',{onclick:()=>{ fn(); syncPanel(); }},label);', 'u')

bad = [(lab, src.count(old)) for lab, old, new, s in M if src.count(old) != 1]
for lab, n in bad:
    print('PATTERN MATCHES %d TIMES: %s' % (n, lab))
io.open(os.path.join(dest, 'mutants.json'), 'w', encoding='utf-8').write(json.dumps(M, indent=1))
print('%d mutants (%d physics, %d ui) -> %s/mutants.json%s'
      % (len(M), sum(1 for x in M if x[3] == 'p'), sum(1 for x in M if x[3] == 'u'),
         os.path.basename(os.path.abspath(dest)), '' if not bad else '   *** %d BAD PATTERNS ***' % len(bad)))
sys.exit(1 if bad else 0)
