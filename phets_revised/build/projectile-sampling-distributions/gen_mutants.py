#!/usr/bin/env python3
"""Write mutants.json for projectile-sampling-distributions.html and check
every pattern appears EXACTLY once in the extracted script.

The sweep runs against a COPY inside _out/, never the published html:
mutate.py writes its scratch _mutant.js next to the file it tests, and the
parallel remakes would share one docs/phets_revised/_mutant.js.

    python3 gen_mutants.py
    python3 <tools>/mutate.py _out/sweep.html mutants.json \\
        ui_drive_projectile-sampling-distributions.js
"""
import io
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, '..', '..', 'projectile-sampling-distributions.html'))

M = [
    # ---- PhET's constants, this sim's branch of them ---------------------
    ["g = 9.81 -> 9.82", "G:9.81,                 /*", "G:9.82,                 /*", "p"],
    ["the field is 100 m -> 110", "FIELD:100,", "FIELD:110,", "p"],
    ["angle sd range max 5 -> 4", "ANG_SD:[0.2,5],", "ANG_SD:[0.2,4],", "p"],
    ["angle sd range min 0.2 -> 0.3", "ANG_SD:[0.2,5],", "ANG_SD:[0.3,5],", "p"],
    ["spring mean speed 23 -> 22", "mean:23,sd:0.5", "mean:22,sd:0.5", "p"],
    ["spring speed sd 0.5 -> 0.6", "mean:23,sd:0.5", "mean:23,sd:0.6", "p"],
    ["pressure mean speed 24 -> 23", "mean:24,sd:0.2", "mean:23,sd:0.2", "p"],
    ["pressure speed sd 0.2 -> 0.25", "mean:24,sd:0.2", "mean:24,sd:0.25", "p"],
    ["explosion mean speed 25 -> 26", "mean:25,sd:1.2", "mean:26,sd:1.2", "p"],
    ["explosion speed sd 1.2 -> 1.1", "mean:25,sd:1.2", "mean:25,sd:1.1", "p"],
    ["the fixed orientation 30 -> 31", "const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:0}];",
     "const ORIENTS=[{id:'angle30',name:'30°',ang:31,h:0}];", "p"],
    ["the fixed orientation gains a height",
     "const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:0}];",
     "const ORIENTS=[{id:'angle30',name:'30°',ang:30,h:1}];", "p"],
    ["the cannonball's multiplier 1 -> 1.05",
     "const PTYPES=[{id:'cannonball',name:'cannonball',mult:1}];",
     "const PTYPES=[{id:'cannonball',name:'cannonball',mult:1.05}];", "p"],
    ["launcher 1's angle sd: the centre -> the min",
     "{n:1,mech:'spring',sdAng:ANG_C}", "{n:1,mech:'spring',sdAng:PDL.ANG_SD[0]}", "p"],
    ["launcher 4's angle sd: min+len/4 -> min+len/2",
     "ANG_Q=PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])/4",
     "ANG_Q=PDL.ANG_SD[0]+(PDL.ANG_SD[1]-PDL.ANG_SD[0])/2", "p"],
    ["the angle-sd centre 0.5 -> 0.4", "ANG_C=0.5*(PDL.ANG_SD[0]+PDL.ANG_SD[1])",
     "ANG_C=0.4*(PDL.ANG_SD[0]+PDL.ANG_SD[1])", "p"],
    ["the sample sizes 2,5,15,40 -> 2,5,15,45", "SIZES:[2,5,15,40],      /*", "SIZES:[2,5,15,45],      /*", "p"],
    ["this sim's bin widths gain the data lab's 10", "BINW:[0.5,1,2,5],", "BINW:[0.5,1,2,5,10],", "p"],
    ["its default bin width 0.5 -> 1 (the data lab's)", "BINW_DEF:0.5,", "BINW_DEF:1,", "p"],
    ["the zoom ladder's top 250 -> 300", "ZOOM_MAX:[250,200,150,100,75,50,25], /*",
     "ZOOM_MAX:[300,200,150,100,75,50,25], /*", "p"],
    ["the zoom ladder's bottom 25 -> 30", "ZOOM_MAX:[250,200,150,100,75,50,25], /*",
     "ZOOM_MAX:[250,200,150,100,75,50,30], /*", "p"],
    ["the speed-mean floor 20 -> 15 (the data lab's)", "SPEED_MEAN_MIN:20,", "SPEED_MEAN_MIN:15,", "p"],
    ["the 200-sample ceiling -> 300", "MAX_SAMPLES:200,        /*", "MAX_SAMPLES:300,        /*", "p"],
    ["the 500-projectile ceiling -> 400", "MAX_PROJ:500,           /*", "MAX_PROJ:400,           /*", "p"],
    ["a sample of 40 takes 9 s -> 12", "SAMPLE_TIME:{2:0.75,5:2,15:5,40:9},",
     "SAMPLE_TIME:{2:0.75,5:2,15:5,40:12},", "p"],
    ["a sample of 2 takes 0.75 s -> 1", "SAMPLE_TIME:{2:0.75,5:2,15:5,40:9},",
     "SAMPLE_TIME:{2:1,5:2,15:5,40:9},", "p"],
    ["the launches of a sample are not spread over its time",
     "function sampleStep(size){ return (PDL.SAMPLE_TIME[size]||2)/size; }",
     "function sampleStep(size){ return (PDL.SAMPLE_TIME[size]||2); }", "p"],
    # ---- the trajectory ---------------------------------------------------
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
    ["the max-range angle loses its half",
     "function pdlMaxAngle(v,h){ return 0.5*Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }",
     "function pdlMaxAngle(v,h){ return Math.acos(PDL.G*h/(v*v+PDL.G*h))*180/Math.PI; }", "p"],
    ["v*(r,theta) at h = 0: sin2th -> sinth",
     "if(h===0) return s<=0?null:Math.sqrt(r*PDL.G/Math.sin(2*th));",
     "if(h===0) return s<=0?null:Math.sqrt(r*PDL.G/Math.sin(th));", "p"],
    # ---- PhET's launch mechanism -----------------------------------------
    # PhET's angle stabiliser is a Sources-screen control and make_engine.py
    # trims it out of this sim entirely, so there is nothing here to mutate —
    # the first sweep reported it as a survivor, which is what dead code does.
    ["the angle re-draw window (0, 90) -> (0, 80)",
     "while(k<100&&(a<=0||a>=90))", "while(k<100&&(a<=0||a>=80))", "p"],
    ["the angle re-draw window opens at 0 -> closes at 0",
     "while(k<100&&(a<=0||a>=90))", "while(k<100&&(a<0||a>=90))", "p"],
    ["the speed re-draw window v <= 0 -> v < 0", "while(v<=0) v=mu+rng.gauss()*cfg.sdSpeed;",
     "while(v<0) v=mu+rng.gauss()*cfg.sdSpeed;", "p"],
    ["the launch forgets the projectile's speed multiplier",
     "const mu=cfg.meanSpeed*cfg.mult;", "const mu=cfg.meanSpeed;", "p"],
    ["the launch draws the speed before the angle",
     "let a=cfg.meanAng+rng.gauss()*cfg.sdAng;", "let a=cfg.meanAng+0*rng.gauss()*cfg.sdAng;", "p"],
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
    ["Box-Muller: u1 = 1 - next() -> next()", "const u1=1-R.next(), u2=R.next();",
     "const u1=R.next(), u2=R.next();", "p"],
    # ---- the quadrature and the exact law ---------------------------------
    ["Gauss-Legendre: the weight's leading 2", "w[i]=2/((1-z*z)*pp*pp);", "w[i]=1/((1-z*z)*pp*pp);", "p"],
    # the density's panel count: one panel rings by 29 % at launcher 2 and two
    # are still 1.2 % out, both measured and asserted in selfTest
    ["the density's theta integral drops to ONE panel", "  NPANEL:8", "  NPANEL:1", "p"],
    ["the density's theta integral drops to two panels", "  NPANEL:8", "  NPANEL:2", "p"],
    ["the drawn density curve is cached under the axis alone, not the launcher",
     "const k=pdlCfgKey(cfg)+'/'+lo+'/'+hi+'/'+n;", "const k=''+lo+'/'+hi+'/'+n;", "p"],
    # the legend dodges the curves AND their labels: dropping the second loop
    # puts it on a bar value label at 1100x712 (that is how it was found)
    ["the legend dodges the data curves but not their labels",
     "for(let i=0;i<LABELS.length&&!hit;i++){", "for(let i=0;i<0&&!hit;i++){", "u"],
    ["Gauss-Legendre: the recurrence's (2j+1)", "p1=((2*j+1)*z*p2-j*p3)/(j+1);",
     "p1=((2*j+2)*z*p2-j*p3)/(j+1);", "p"],
    ["Gauss-Legendre: the seed's divisor n+0.5 -> n+1.5", "Math.cos(Math.PI*(i+sd)/(n+0.5))",
     "Math.cos(Math.PI*(i+sd)/(n+1.5))", "p"],
    ["the normal density loses its 1/2 in the exponent",
     "function pdlPhi(z){ return NORM*Math.exp(-0.5*z*z); }",
     "function pdlPhi(z){ return NORM*Math.exp(-z*z); }", "p"],
    ["the normal density loses its 1/sqrt(2 pi)", "const NORM=1/Math.sqrt(2*Math.PI);", "const NORM=1;", "p"],
    ["the truncation cap 12 sd -> 4 sd", "ZCAP:12,", "ZCAP:4,", "p"],
    ["the angle truncation (0, 90) in the quadrature -> (0, 80)",
     "pdlZRule.apply(null,pdlZRange(cfg.meanAng,cfg.sdAng,0,90));\n  let wsum=0;",
     "pdlZRule.apply(null,pdlZRange(cfg.meanAng,cfg.sdAng,0,80));\n  let wsum=0;", "p"],
    ["the central moments are taken about the wrong centre",
     "for(let k=0;k<N;k++){ const d=R[k]-mean, d2=d*d; c2+=P[k]*d2; c3+=P[k]*d2*d; c4+=P[k]*d2*d2; }",
     "for(let k=0;k<N;k++){ const d=R[k]-mean*1.0000000001, d2=d*d; c2+=P[k]*d2; c3+=P[k]*d2*d; c4+=P[k]*d2*d2; }", "p"],
    ["the closed form: E[cos a0] loses its 1/2", "const C=a=>Math.cos(a*m)*Math.exp(-0.5*a*a*w*w);",
     "const C=a=>Math.cos(a*m)*Math.exp(-a*a*w*w);", "p"],
    ["the closed form: E[sin a0] loses its 1/2", "const S=a=>Math.sin(a*m)*Math.exp(-0.5*a*a*w*w);",
     "const S=a=>Math.sin(a*m)*Math.exp(-a*a*w*w);", "p"],
    ["the closed form: E[v^2] loses its sigma^2", "const v2=mu*mu+s*s;", "const v2=mu*mu;", "p"],
    ["the density divides by dx/dv twice",
     "tot+=w*(NORM*Math.exp(-0.5*zz*zz)/sv)/pdlDRdv(vs,th,cfg.h);",
     "tot+=w*(NORM*Math.exp(-0.5*zz*zz)/sv)/pdlDRdv(vs,th,cfg.h)/pdlDRdv(vs,th,cfg.h);", "p"],
    ["the density forgets to normalise by the truncation", "return tot/(tw*vw);", "return tot;", "p"],
    # ---- the statistics ---------------------------------------------------
    ["the standard deviation divides by n, not n-1", "return Math.sqrt(s/(n-d));", "return Math.sqrt(s/n);", "p"],
    ["the standard deviation is defined at one value", "if(n<=d) return null;", "if(n<d) return null;", "p"],
    ["the standard error divides by n, not sqrt(n)", "return s===null?null:s/Math.sqrt(xs.length);",
     "return s===null?null:s/xs.length;", "p"],
    ["the median of an even sample takes the upper middle",
     "return n%2?a[(n-1)/2]:0.5*(a[n/2-1]+a[n/2]);", "return n%2?a[(n-1)/2]:a[n/2];", "p"],
    ["the median does not sort at all", "const a=xs.slice().sort((p,q)=>p-q);", "const a=xs.slice();", "p"],
    ["the binning rounds instead of flooring", "function pdlBinIndex(x,w){ return Math.floor(x/w); }",
     "function pdlBinIndex(x,w){ return Math.round(x/w); }", "p"],
    ["a sample's mean is the mean of the wrong slice",
     "F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs)});\n    /* the field shows",
     "F.samples.push({n:F.sampleN,xs,mean:pdlMean(xs.slice(1))});\n    /* the field shows", "p"],
    ["the auto zoom crops the tallest bin", "const want=Math.max(4,Math.ceil(maxCount*1.15));",
     "const want=Math.max(4,Math.ceil(maxCount*0.5));", "p"],
    ["the auto zoom uses a ladder of its own", "const ZOOM_FINE=[4,6,8,10,15,20];",
     "const ZOOM_FINE=[4,6,8,10,15,20,30,40];", "p"],
    ["the general-case angle window in the quadrature: 90 -> 85",
     "pdlZRange(cfg.meanAng,cfg.sdAng,0,90);\n  const rv=",
     "pdlZRange(cfg.meanAng,cfg.sdAng,0,85);\n  const rv=", "p"],
    ["the standard error's own contract: s/sqrt(n) -> s",
     "return s===null?null:s/Math.sqrt(xs.length);", "return s===null?null:s;", "p"],
    ["the density's SPEED acceptance divisor: tw*vw -> tw",
     "return tot/(tw*vw);", "return tot/tw;", "p"],
    ["the density's ANGLE acceptance divisor: tw*vw -> vw",
     "return tot/(tw*vw);", "return tot/vw;", "p"],
    ["starting a sample no longer clears the field",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; F.tSample=0; }",
     "function sampleStart(F){ F.air.length=0; F.launched=0; F.tSample=0; }", "u"],
    ["starting a sample no longer rewinds its clock",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; F.tSample=0; }",
     "function sampleStart(F){ F.landed.length=0; F.air.length=0; F.launched=0; }", "u"],
    ["the closed form: E[cos 4th] -> E[cos 3th]", "const s1=S(2), s2=0.5*(1-C(4)),",
     "const s1=S(2), s2=0.5*(1-C(3)),", "p"],
    # ---- the UI ------------------------------------------------------------
    ["the pointer-move handler stops setting the dirty flag",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=true;",
     "if(S.pointer('move',e.clientX-r.left,e.clientY-r.top)){ dirty=false;", "u"],
    ["the launcher drag measures from the pivot, not the grab point",
     "const n=clamp(Math.round(DRAG.start+(DRAG.yDown-y)/14),1,PDL.N_FIELDS);",
     "const n=clamp(Math.round(DRAG.start+(DRAG.Y0-y)/14),1,PDL.N_FIELDS);", "u"],
    ["the launcher drag does not clamp at six",
     "const n=clamp(Math.round(DRAG.start+(DRAG.yDown-y)/14),1,PDL.N_FIELDS);",
     "const n=Math.max(1,Math.round(DRAG.start+(DRAG.yDown-y)/14));", "u"],
    ["the barrel cannot be grabbed at all", "if(Math.abs(x-X0)>44||y<Y0-44||y>Y0+16) return null;",
     "return null;", "u"],
    ["the barrel can be grabbed anywhere on the field",
     "if(Math.abs(x-X0)>44||y<Y0-44||y>Y0+16) return null;",
     "if(y<Y0-44||y>Y0+16) return null;", "u"],
    ["a slider stops repainting at once",
     "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; refresh(); });",
     "val.textContent=fmtf(st[key]); if(onchg) onchg(); syncPanel(); dirty=true; });", "u"],
    ["a single sample does not stop itself",
     "F.firing=st.mode==='continuous'&&F.samples.length<PDL.MAX_SAMPLES;",
     "F.firing=F.samples.length<PDL.MAX_SAMPLES;", "u"],
    ["each (launcher, n) pair does NOT keep its own field",
     "const w=worldOf(view), key=lau+'/'+n;", "const w=worldOf(view), key='one';", "u"],
    ["the vertical-scale chips stay live on every view",
     "[].forEach.call(zr.children,b=>{ b.disabled=!zoomLive; b.style.opacity=zoomLive?'1':'0.4'; });",
     "[].forEach.call(zr.children,b=>{ b.style.opacity=zoomLive?'1':'0.4'; });", "u"],
    ["a manual start does not begin a new sample at all",
     "F.firing=true; sampleStart(F);", "F.firing=true;", "u"],
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
