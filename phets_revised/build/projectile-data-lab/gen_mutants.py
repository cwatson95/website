#!/usr/bin/env python3
"""Write mutants.json for projectile-data-lab.html and check every pattern
appears EXACTLY once in the extracted script (a pattern that matches twice
mutates two places silently; one that matches none is a mutant you believe you
ran and did not).

The sweep itself runs against a COPY inside _out/, never the published html:
mutate.py writes its scratch _mutant.js next to the file it tests, and the
parallel remakes would share one docs/phets_revised/_mutant.js.

    python3 gen_mutants.py
    python3 <tools>/mutate.py _out/sweep.html mutants.json ui_drive_projectile-data-lab.js
"""
import io
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, '..', '..', 'projectile-data-lab.html'))

M = [
    # ---- PhET's own constants -------------------------------------------
    ["g = 9.81 -> 9.82", "G:9.81,                 /*", "G:9.82,                 /*", "p"],
    ["the field is 100 m -> 110", "FIELD:100,", "FIELD:110,", "p"],
    ["the raised launcher 12 m -> 11", "RAISED_H:12,", "RAISED_H:11,", "p"],
    ["angle sd range max 5 -> 4", "ANG_SD:[0.2,5],", "ANG_SD:[0.2,4],", "p"],
    ["angle sd range min 0.2 -> 0.3", "ANG_SD:[0.2,5],", "ANG_SD:[0.3,5],", "p"],
    ["spring mean speed 23 -> 22", "mean:23,sd:0.5", "mean:22,sd:0.5", "p"],
    ["spring speed sd 0.5 -> 0.6", "mean:23,sd:0.5", "mean:23,sd:0.6", "p"],
    ["pressure mean speed 24 -> 23", "mean:24,sd:0.2", "mean:23,sd:0.2", "p"],
    ["pressure speed sd 0.2 -> 0.25", "mean:24,sd:0.2", "mean:24,sd:0.25", "p"],
    ["explosion mean speed 25 -> 26", "mean:25,sd:1.2", "mean:26,sd:1.2", "p"],
    ["explosion speed sd 1.2 -> 1.1", "mean:25,sd:1.2", "mean:25,sd:1.1", "p"],
    ["pumpkin multiplier 1.1 -> 1.15", "name:'pumpkin',mult:1.1", "name:'pumpkin',mult:1.15", "p"],
    ["piano multiplier 0.9 -> 0.95", "name:'piano',mult:0.9", "name:'piano',mult:0.95", "p"],
    ["the 45 deg orientation -> 44", "name:'45°',ang:45", "name:'45°',ang:44", "p"],
    ["the raised orientation loses its height", "name:'0° raised',ang:0,h:PDL.RAISED_H",
     "name:'0° raised',ang:0,h:0", "p"],
    ["launcher 1's angle sd: the centre -> the min",
     "{n:1,mech:'spring',sdAng:ANG_C}", "{n:1,mech:'spring',sdAng:PDL.ANG_SD[0]}", "p"],
    ["launcher 4's angle sd: min+len/4 -> min+len/2",
     "ANG_Q=PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])/4",
     "ANG_Q=PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])/2", "p"],
    ["the angle-sd centre 0.5 -> 0.4", "ANG_C=0.5*(PDL.ANG_SD[0]+PDL.ANG_SD[1])",
     "ANG_C=0.4*(PDL.ANG_SD[0]+PDL.ANG_SD[1])", "p"],
    ["the sample sizes 2,5,15,40 -> 2,5,15,45", "SIZES:[2,5,15,40],      /*", "SIZES:[2,5,15,45],      /*", "p"],
    ["the bin widths lose the 0.5", "BINW:[0.5,1,2,5,10],", "BINW:[0.25,1,2,5,10],", "p"],
    ["the minimum gap between launches 0.7 -> 0.5", "LAUNCH_GAP:0.7,         /*", "LAUNCH_GAP:0.5,         /*", "p"],
    # ---- the trajectory --------------------------------------------------
    ["the range: the sign of the root",
     "return v*Math.cos(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*h));",
     "return v*Math.cos(th)/PDL.G*(v*s-Math.sqrt(v*v*s*s+2*PDL.G*h));", "p"],
    ["the range: 2gh -> gh",
     "return v*Math.cos(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*h));",
     "return v*Math.cos(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+PDL.G*h));", "p"],
    ["the range: cos -> sin",
     "return v*Math.cos(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*h));",
     "return v*Math.sin(th)/PDL.G*(v*s+Math.sqrt(v*v*s*s+2*PDL.G*h));", "p"],
    ["the flight time: 2h/g -> h/g", "return a+Math.sqrt(a*a+2*h/PDL.G);",
     "return a+Math.sqrt(a*a+h/PDL.G);", "p"],
    ["the flight time: v sin/g -> v/g", "const s=Math.sin(thDeg*Math.PI/180), a=v*s/PDL.G;",
     "const s=Math.sin(thDeg*Math.PI/180), a=v/PDL.G;", "p"],
    ["the height: the 1/2 in g t^2/2", "return h+v*Math.sin(thDeg*Math.PI/180)*t-0.5*PDL.G*t*t;",
     "return h+v*Math.sin(thDeg*Math.PI/180)*t-PDL.G*t*t;", "p"],
    ["dx/dv: the leading 2 v sin", "return c/PDL.G*(2*v*s+(2*v*v*s*s+2*PDL.G*h)/Q);",
     "return c/PDL.G*(v*s+(2*v*v*s*s+2*PDL.G*h)/Q);", "p"],
    ["dx/dv: 2v^2sin^2 -> v^2sin^2", "return c/PDL.G*(2*v*s+(2*v*v*s*s+2*PDL.G*h)/Q);",
     "return c/PDL.G*(2*v*s+(v*v*s*s+2*PDL.G*h)/Q);", "p"],
    ["the max-range angle loses its half",
     "function pdlMaxAngle(v,h){ return 0.5*Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }",
     "function pdlMaxAngle(v,h){ return Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }", "p"],
    ["the max-range angle: gh/(v^2+gh) -> gh/v^2",
     "function pdlMaxAngle(v,h){ return 0.5*Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }",
     "function pdlMaxAngle(v,h){ return 0.5*Math.acos(PDL.G*h/(v*v))*180/Math.PI; }", "p"],
    ["v*(r,theta) at h = 0: sin2th -> sinth",
     "if(h===0) return s<=0?null:Math.sqrt(r*PDL.G/Math.sin(2*th));",
     "if(h===0) return s<=0?null:Math.sqrt(r*PDL.G/Math.sin(th));", "p"],
    ["v* drops its downward-launch ceiling", "if(s<0&&r>=h*c/(-s)) return null;",
     "if(false) return null;", "p"],
    ["the conjugate form of the range loses its 2gh",
     "return v*Math.cos(th)/PDL.G*(2*PDL.G*h)/(Q-v*s);",
     "return v*Math.cos(th)/PDL.G*(PDL.G*h)/(Q-v*s);", "p"],
    # ---- PhET's angle stabiliser and its launch mechanism ----------------
    ["the stabiliser runs the RIGHT way round (PhET's runs backwards)",
     "function pdlSdOfStab(stab){ return PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])*(1-stab); }",
     "function pdlSdOfStab(stab){ return PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])*stab; }", "p"],
    ["the launch draws the speed before the angle",
     "let a=cfg.meanAng+rng.gauss()*cfg.sdAng;", "let a=cfg.meanAng+0*rng.gauss()*cfg.sdAng;", "p"],
    ["the launch forgets the projectile's speed multiplier",
     "const mu=cfg.meanSpeed*cfg.mult;", "const mu=cfg.meanSpeed;", "p"],
    ["the angle re-draw window (0, 90) -> (0, 80)",
     "while(k<100&&(a<=0||a>=90))", "while(k<100&&(a<=0||a>=80))", "p"],
    # ---- the random stream ------------------------------------------------
    ["mulberry32's increment", "a=(a+0x6D2B79F5)>>>0;", "a=(a+0x6D2B79F4)>>>0;", "p"],
    ["mulberry32's first shift 15 -> 14", "Math.imul(a^(a>>>15),a|1)", "Math.imul(a^(a>>>14),a|1)", "p"],
    ["mulberry32's 61", "Math.imul(t^(t>>>7),t|61)", "Math.imul(t^(t>>>7),t|59)", "p"],
    ["mulberry32's final shift 14 -> 13", "((t^(t>>>14))>>>0)/4294967296", "((t^(t>>>13))>>>0)/4294967296", "p"],
    ["Box-Muller: the -2 in sqrt(-2 ln u)",
     "return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2);",
     "return Math.sqrt(-Math.log(u1))*Math.cos(2*Math.PI*u2);", "p"],
    ["Box-Muller: cos -> sin (a different stream, same law)",
     "return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2);",
     "return Math.sqrt(-2*Math.log(u1))*Math.sin(2*Math.PI*u2);", "p"],
    ["Box-Muller: 2 pi u2 -> pi u2", "return Math.sqrt(-2*Math.log(u1))*Math.cos(2*Math.PI*u2);",
     "return Math.sqrt(-2*Math.log(u1))*Math.cos(Math.PI*u2);", "p"],
    ["Box-Muller: u1 = 1 - next() -> next()", "const u1=1-R.next(), u2=R.next();",
     "const u1=R.next(), u2=R.next();", "p"],
    # ---- the quadrature and the exact law ---------------------------------
    # the Newton seed: 0.75 and 0.50 converge to bit-identical roots, which
    # selfTest measures, so this one is an EQUIVALENT mutant by construction
    # and is kept in the sweep as the record of that.  The divisor is not
    # equivalent, and is mutated beside it.
    ["Gauss-Legendre: the Newton seed 0.75 -> 0.5 (EQUIVALENT, proven in selfTest)",
     "const sd=seed===undefined?0.75:seed;", "const sd=seed===undefined?0.5:seed;", "p"],
    ["Gauss-Legendre: the seed's divisor n+0.5 -> n+1.5", "Math.cos(Math.PI*(i+sd)/(n+0.5))",
     "Math.cos(Math.PI*(i+sd)/(n+1.5))", "p"],
    ["Gauss-Legendre: the weight's leading 2", "w[i]=2/((1-z*z)*pp*pp);", "w[i]=1/((1-z*z)*pp*pp);", "p"],
    # the density's panel count: one panel rings by 29 % (292 % raised) and
    # four are still 7 % out, both measured and asserted in selfTest
    ["the density's theta integral drops to ONE panel", "  NPANEL:8", "  NPANEL:1", "p"],
    ["the density's theta integral drops to four panels", "  NPANEL:8", "  NPANEL:4", "p"],
    ["the drawn density curve is cached under the axis alone, not the launcher",
     "const k=pdlCfgKey(cfg)+'/'+lo+'/'+hi+'/'+n;", "const k=''+lo+'/'+hi+'/'+n;", "p"],
    # the legend dodges the curves AND their labels: dropping the second loop
    # puts it on a bar value label at 1100x712 (that is how it was found)
    ["the legend dodges the data curves but not their labels",
     "for(let i=0;i<LABELS.length&&!hit;i++){", "for(let i=0;i<0&&!hit;i++){", "u"],
    ["Gauss-Legendre: the recurrence's (2j+1)", "p1=((2*j+1)*z*p2-j*p3)/(j+1);",
     "p1=((2*j+2)*z*p2-j*p3)/(j+1);", "p"],
    ["the normal density loses its 1/2 in the exponent",
     "function pdlPhi(z){ return NORM*Math.exp(-0.5*z*z); }",
     "function pdlPhi(z){ return NORM*Math.exp(-z*z); }", "p"],
    ["the normal density loses its 1/sqrt(2 pi)",
     "const NORM=1/Math.sqrt(2*Math.PI);", "const NORM=1;", "p"],
    ["the truncation cap 12 sd -> 4 sd", "ZCAP:12,", "ZCAP:4,", "p"],
    ["the angle truncation (0, 90) in the quadrature -> (0, 80)",
     "pdlZRule.apply(null,pdlZRange(cfg.meanAng,cfg.sdAng,0,90));\n  let wsum=0;",
     "pdlZRule.apply(null,pdlZRange(cfg.meanAng,cfg.sdAng,0,80));\n  let wsum=0;", "p"],
    ["the moments are assembled from the raw ones (the cancellation)",
     "for(let k=0;k<N;k++){ const d=R[k]-mean, d2=d*d; c2+=P[k]*d2; c3+=P[k]*d2*d; c4+=P[k]*d2*d2; }",
     "for(let k=0;k<N;k++){ const d=R[k]-mean*1.0000000001, d2=d*d; c2+=P[k]*d2; c3+=P[k]*d2*d; c4+=P[k]*d2*d2; }", "p"],
    ["the closed form: E[cos a0] loses its 1/2", "const C=a=>Math.cos(a*m)*Math.exp(-0.5*a*a*w*w);",
     "const C=a=>Math.cos(a*m)*Math.exp(-a*a*w*w);", "p"],
    ["the closed form: E[sin a0] loses its 1/2", "const S=a=>Math.sin(a*m)*Math.exp(-0.5*a*a*w*w);",
     "const S=a=>Math.sin(a*m)*Math.exp(-a*a*w*w);", "p"],
    ["the closed form: E[v^2] loses its sigma^2", "const v2=mu*mu+s*s;", "const v2=mu*mu;", "p"],
    ["the closed form: E[sin^2 2t] loses its half", "const s1=S(2), s2=0.5*(1-C(4)),",
     "const s1=S(2), s2=(1-C(4)),", "p"],
    ["the closed form: sin(2m) -> sin(m)", "const s1=S(2), s2=0.5*(1-C(4)),",
     "const s1=S(1), s2=0.5*(1-C(4)),", "p"],
    ["PhET's delta method: the leading 2 on dx/dv", "const a=2*v/PDL.G*Math.sin(2*s), b=2*v*v/PDL.G*Math.cos(2*s);",
     "const a=v/PDL.G*Math.sin(2*s), b=2*v*v/PDL.G*Math.cos(2*s);", "p"],
    ["PhET's delta method: cos2t -> sin2t on the angle term",
     "const a=2*v/PDL.G*Math.sin(2*s), b=2*v*v/PDL.G*Math.cos(2*s);",
     "const a=2*v/PDL.G*Math.sin(2*s), b=2*v*v/PDL.G*Math.sin(2*s);", "p"],
    ["PhET's delta method: the angle sd stays in degrees",
     "const s=thDeg*Math.PI/180, r=sdthDeg*Math.PI/180;", "const s=thDeg*Math.PI/180, r=sdthDeg;", "p"],
    ["the density divides by dx/dv twice",
     "tot+=w*(NORM*Math.exp(-0.5*zz*zz)/sv)/pdlDRdv(vs,th,cfg.h);",
     "tot+=w*(NORM*Math.exp(-0.5*zz*zz)/sv)/pdlDRdv(vs,th,cfg.h)/pdlDRdv(vs,th,cfg.h);", "p"],
    ["the density forgets to normalise by the truncation", "return tot/(tw*vw);", "return tot;", "p"],
    ["the density's SPEED acceptance divisor: tw*vw -> tw", "return tot/(tw*vw);", "return tot/tw;", "p"],
    ["the density's ANGLE acceptance divisor: tw*vw -> vw", "return tot/(tw*vw);", "return tot/vw;", "p"],
    ["starting a sample no longer clears the field",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; F.tSample=0; }",
     "function sampleStart(F){ F.air.length=0; F.launched=0; F.tSample=0; }", "u"],
    ["starting a sample no longer rewinds its clock",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; F.tSample=0; }",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; }", "u"],
    ["P(a <= x <= b): Simpson's 1/3 -> 1/2", "s+=c*pdlPdf(a+i*dx,cfg); }\n  return s*dx/3;",
     "s+=c*pdlPdf(a+i*dx,cfg); }\n  return s*dx/2;", "p"],
    # ---- the statistics ---------------------------------------------------
    ["the standard deviation divides by n, not n-1", "return Math.sqrt(s/(n-d));", "return Math.sqrt(s/n);", "p"],
    ["the standard deviation is defined at one value", "if(n<=d) return null;", "if(n<d) return null;", "p"],
    ["the standard error divides by n, not sqrt(n)", "return s===null?null:s/Math.sqrt(xs.length);",
     "return s===null?null:s/xs.length;", "p"],
    ["the median of an even sample takes the upper middle",
     "return n%2?a[(n-1)/2]:0.5*(a[n/2-1]+a[n/2]);", "return n%2?a[(n-1)/2]:a[n/2];", "p"],
    # the median reads symmetric positions out of the sorted array, so the
    # direction of the sort cannot change it: an EQUIVALENT mutant, and
    # selfTest asserts the invariance rather than leaving it a blind spot
    ["the median sorts descending (EQUIVALENT: it reads symmetric positions)",
     "const a=xs.slice().sort((p,q)=>p-q);", "const a=xs.slice().sort((p,q)=>q-p);", "p"],
    ["the median does not sort at all", "const a=xs.slice().sort((p,q)=>p-q);",
     "const a=xs.slice();", "p"],
    ["the binning rounds instead of flooring", "function pdlBinIndex(x,w){ return Math.floor(x/w); }",
     "function pdlBinIndex(x,w){ return Math.round(x/w); }", "p"],
    ["the interval tool opens both its ends", "let k=0; for(const x of xs) if(x>=a&&x<=b) k++;",
     "let k=0; for(const x of xs) if(x>a&&x<b) k++;", "p"],
    ["the interval tool ignores which edge is which",
     "const a=Math.min(lo,hi), b=Math.max(lo,hi);", "const a=lo, b=hi;", "p"],
    ["the total-bins width 100/n -> 100/(n+1)",
     "return st.binStrat==='binWidth'?st.binW:PDL.FIELD/st.nBins;",
     "return st.binStrat==='binWidth'?st.binW:PDL.FIELD/(st.nBins+1);", "p"],
    ["a sample's mean is the mean of the wrong slice",
     "F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs)});\n    /* the field shows",
     "F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs.slice(1))});\n    /* the field shows", "p"],
    # ---- the UI ------------------------------------------------------------
    ["the pointer-move handler stops setting the dirty flag",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=false;", "u"],
    ["the interval drag forgets the histogram's left edge",
     "const v=clamp((x-DRAG.x0)*DRAG.per,0,PDL.FIELD);", "const v=clamp(x*DRAG.per,0,PDL.FIELD);", "u"],
    ["the interval drag moves both edges when only one was grabbed",
     "if(DRAG.what==='e1') ST.e1=Math.round(v*10)/10;",
     "if(DRAG.what==='e1'){ ST.e1=Math.round(v*10)/10; ST.e2=ST.e1+20; }", "u"],
    ["a middle drag stops keeping the window's width",
     "ST.e1=Math.round((c-DRAG.w0/2)*10)/10; ST.e2=Math.round((c+DRAG.w0/2)*10)/10;",
     "ST.e1=Math.round((c-DRAG.w0/4)*10)/10; ST.e2=Math.round((c+DRAG.w0/2)*10)/10;", "u"],
    ["the interval edges cannot be grabbed at all", "if(d1<=9&&d1<=d2) return {what:'e1',per,x0};",
     "if(false) return {what:'e1',per,x0};", "u"],
    ["the interval tool is grabbable while it is hidden",
     "if(M.view!=='measures'||!M.st.showInterval) return null;", "if(M.view!=='measures') return null;", "u"],
    ["a slider stops repainting at once",
     "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });",
     "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; });", "u"],
    ["single fire does not stop itself", "if(fieldMode(st)==='single') F.firing=false;",
     "if(false) F.firing=false;", "u"],
    ["continuous fire ignores the 0.7 s gap", "} else if(F.sinceLaunch>=PDL.LAUNCH_GAP){",
     "} else if(F.sinceLaunch>=0){", "u"],
    ["changing a field's launcher keeps its old shots",
     "F.cfg=cfgMystery(st.lau); F.lau=st.lau; fieldClear(F); };",
     "F.cfg=cfgMystery(st.lau); F.lau=st.lau; };", "u"],
    ["the bin-width chips stay live under the total-bins strategy",
     "[].forEach.call(bwRow.children,b=>{ b.disabled=!byW; b.style.opacity=byW?'1':'0.4'; });",
     "[].forEach.call(bwRow.children,b=>{ b.style.opacity=byW?'1':'0.4'; });", "u"],
    ["a sampling field forgets which sample size it is",
     "F.size=st.pN; sampleBatch(F,st.pN,30);", "F.size=st.pN; sampleBatch(F,2,30);", "u"],
]

js = io.open(SIM, encoding='utf-8').read().split('<script>', 1)[1].rsplit('</script>', 1)[0]
bad = [(m[0], js.count(m[1])) for m in M if js.count(m[1]) != 1]
io.open(os.path.join(HERE, 'mutants.json'), 'w', encoding='utf-8').write(
    json.dumps(M, ensure_ascii=False, indent=1))
os.makedirs(os.path.join(HERE, '_out'), exist_ok=True)
shutil.copyfile(SIM, os.path.join(HERE, '_out', 'sweep.html'))
print('%d mutants (%d physics, %d ui); _out/sweep.html refreshed'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u')))
for b in bad:
    print('  PATTERN NOT UNIQUE: %-56s count %d' % b)
