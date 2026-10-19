
/* ================================================================== *
 *  state: four views of ONE experiment.  PhET's Diffusion is a single  *
 *  screen, so all four views share one gas and one clock — the tabs    *
 *  change the instrument, not the run.                                 *
 * ================================================================== */
const TABS=[['box','the divided box'],['mixing','the mixing'],['flow','the flow'],['speeds','the speeds']];
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6', edge:'#242a3a',
           heavy:'#6c9cff', light:'#ff6f6f', heavyHi:'#b9d0ff', lightHi:'#ffc0bb',
           box:'#0d1422', wall:'#5ac8e0', lid:'#7f93b3', text:'#aeb6c6'};
const RO_W=300;
const SEED=31;
const UNITS_T=[{id:'K',name:'K'},{id:'C',name:'°C'}];
const SPEEDS=[{id:false,name:'normal'},{id:true,name:'slow'}];
/* four starting pairs worth comparing.  PhET's own defaults are both species
   28 AMU, 125 pm, 300 K with N = 0; this sim opens on 'heavy and light' so the
   box is not empty, and keeps PhET's pair as a chip. */
const PRESETS=[
  {id:'hl',   name:'heavy and light', a:{n:100,m:28,r:125,T:300}, b:{n:100,m:4, r:90, T:300}},
  {id:'same', name:'identical',       a:{n:100,m:28,r:125,T:300}, b:{n:100,m:28,r:125,T:300}},
  {id:'hot',  name:'hot and cold',    a:{n:100,m:28,r:125,T:500}, b:{n:100,m:28,r:125,T:100}},
  {id:'size', name:'big and small',   a:{n:100,m:28,r:250,T:300}, b:{n:100,m:28,r:50, T:300}}
];
const FRAME_DT=GAS.DT_FRAME;
const NPROF=32;                 /* bins along the box for the concentration profile */
const PAIR_WINDOW=240;          /* frames in the rolling pair-collision measurement */
const HIST_MAX=4000;

const DEFAULTS={view:'box', running:true, slow:false, unitT:'K',
  preset:'hl',
  d1n:100, d1m:28, d1r:125, d1T:300,
  d2n:100, d2m:4,  d2r:90,  d2T:300,
  divided:true, dCOM:true, dFlow:true, dScale:true, showWatch:false, showCounter:false,
  showMB:true, showProfile:true};
const ST=Object.assign({},DEFAULTS);
const BOXVIEWS={box:1, mixing:1, flow:1, speeds:1};
function worldKey(){ return 'box'; }    /* one experiment, four instruments */

/* ---- the world ------------------------------------------------------------- */
const WORLD={};
function makeWorld(view,st){
  const w={view:'box', hist:[], pairs:[], pump:{h:0,acc:0}, dragW:null};
  const g=w.g=gasMake({width:GAS.DIFF_W, wRange:[GAS.DIFF_W,GAS.DIFF_W], noLid:true, seed:SEED,
                       species:[{m:st.d1m,r:st.d1r},{m:st.d2m,r:st.d2r}]});
  gasSetDivided(g,st.divided);
  diffScatter(g,st);
  gasFlowOn(g); gasLedgerReset(g); gasRefresh(g);
  histRecord(w);
  return w;
}
function diffScatter(g,st){
  const half=g.dividerHalf, dx=g.left+g.W/2;
  gasScatter(g,0,st.d1n,st.d1T,g.left,dx-half);
  gasScatter(g,1,st.d2n,st.d2T,dx+half,0);
}
function worldOf(){ if(!WORLD.box) WORLD.box=makeWorld('box',ST); return WORLD.box; }
function resetWorld(){ WORLD.box=makeWorld('box',ST); return WORLD.box; }
function resetAllWorlds(){ for(const k in WORLD) delete WORLD[k]; }

/* ---- the exact laws this sim measures against ------------------------------- */
/* the one-sided flux of a 2-D Maxwellian: <vx+> = sqrt(kT2/2 pi m) = <v>/pi */
function vxPlus(m,T){ return T===null||!(T>0)?null:Math.sqrt(gasKT2(T)/(2*PI*m)); }
/* particles of species k crossing the divider line one way, per ps, from the
   side that holds nSide of them: n <vx+> (H - 2r) with n the density of
   CENTRES in that half, which makes the height cancel */
function flowTheory(g,k,nSide){
  const T=gasTemp(g,k), v=vxPlus(g.species[k].m,T);
  if(v===null) return null;
  const halfW=g.W/2-g.species[k].r;
  return halfW>0?nSide*v/halfW:null;
}
/* the time constant of the left-right imbalance if each side stayed mixed:
   d(DeltaN)/dt = -(4 <vx+>/(W - 2r)) DeltaN */
function tauEffusion(g,k){
  const v=vxPlus(g.species[k].m,gasTemp(g,k));
  return v===null?null:(g.W-2*g.species[k].r)/(4*v);
}
/* the mean relative speed of two 2-D Maxwellians, each component Gaussian with
   variance kT2/m, so the relative velocity has variance kT2_k/m_k + kT2_j/m_j
   and <v_rel> = sqrt(pi/2) times its scale (= sqrt(pi kT2/2 mu) at equal T) */
function vRel(g,k,j){
  const Tk=gasTemp(g,k), Tj=gasTemp(g,j);
  if(Tk===null||Tj===null) return null;
  const s2=gasKT2(Tk)/g.species[k].m+gasKT2(Tj)/g.species[j].m;
  return Math.sqrt(PI*s2/2);
}
/* collisions per ps suffered by one disk of species k: sum_j n_j 2(r_k+r_j) <v_rel>.
   The 2 is the swath: a disk collides when the centres come within
   d = r_k + r_j, so it sweeps a strip of HALF-width d — width 2d.  Writing
   n_j d <v_rel> halves every rate, and this sim's own pair counter found that
   (it measured 2.05 times the first draft's prediction). */
function zRate(g,k){
  const A=g.W*g.H; let s=0;
  for(const j of [0,1]){
    const nj=gasCount(g,j); if(!nj) continue;
    const vr=vRel(g,k,j); if(vr===null) return null;
    s+=nj/A*2*(g.species[k].r+g.species[j].r)*vr;
  }
  return s;
}
/* every unordered pair, so half the sum over disks */
function pairRateTheory(g){
  let s=0;
  for(const k of [0,1]){ const nk=gasCount(g,k); if(!nk) continue; const z=zRate(g,k); if(z===null) return null; s+=nk*z; }
  return s/2;
}
function mfp(g,k){
  const T=gasTemp(g,k), z=zRate(g,k);
  return (T===null||z===null||!(z>0))?null:mbMeanSpeed(g.species[k].m,gasKT2(T))/z;
}
/* the Fickian bound: the slowest cosine mode of dc/dt = D d2c/dx2 on a box of
   width W with no flux through the ends decays at D (pi/W)^2.  D = <v> lambda/2
   is the elementary 2-D kinetic-theory ESTIMATE, with an O(1) factor this file
   does not pin, so it is drawn and labelled as a bound, not a prediction. */
function dEstimate(g,k){
  const T=gasTemp(g,k), l=mfp(g,k);
  return (T===null||l===null)?null:mbMeanSpeed(g.species[k].m,gasKT2(T))*l/2;
}
function tauDiffusive(g,k){
  const D=dEstimate(g,k);
  return (D===null||!(D>0))?null:g.W*g.W/(PI*PI*D);
}

/* ---- what each frame records ------------------------------------------------ */
/* the left-right imbalance of species k, as a fraction of its count */
function imbalance(g,side,k){
  const n=side[0]['n'+k]+side[1]['n'+k];
  return n?(side[0]['n'+k]-side[1]['n'+k])/n:null;
}
function histRecord(w){
  const g=w.g, side=gasSideData(g);
  w.hist.push([g.t,gasCOM(g,0),gasCOM(g,1),imbalance(g,side,0),imbalance(g,side,1),
               gasTemp(g,0),gasTemp(g,1),gasMeanSpeedOf(g,0),gasMeanSpeedOf(g,1)]);
  if(w.hist.length>HIST_MAX) w.hist.splice(0,w.hist.length-HIST_MAX);
}
function pairRecord(w,dt){
  const g=w.g;
  w.pairs.push([dt,g.stats.pairHits-(w.lastPairs||0)]);
  w.lastPairs=g.stats.pairHits;
  if(w.pairs.length>PAIR_WINDOW) w.pairs.shift();
}
function pairRateMeasured(w){
  let t=0,c=0; for(const r of w.pairs){ t+=r[0]; c+=r[1]; }
  return t>0?{rate:c/t, n:c, t, sd:Math.sqrt(Math.max(1,c))/t}:null;
}
/* the concentration profile: counts of each species in NPROF bins along x */
function profile(g){
  const out=[new Array(NPROF).fill(0),new Array(NPROF).fill(0)];
  for(let i=0;i<g.n;i++){ if(g.out[i]) continue;
    const q=Math.floor((g.x[i]-g.left)/g.W*NPROF);
    if(q>=0&&q<NPROF) out[g.sp[i]][q]++; }
  return out;
}
/* the speed histogram this sim draws, and the exact 2-D Maxwell-Boltzmann
   counts in the same bins (derive.py section 7a) */
const SPD_NB=20, SPD_BW=150;
function mbBinCounts(Nk,m,T){
  const out=[], kt2=gasKT2(T);
  for(let b=0;b<SPD_NB;b++){
    const lo=b*SPD_BW, hi=lo+SPD_BW;
    out.push(Nk*(mbSpeedCdf(hi,m,kt2)-mbSpeedCdf(lo,m,kt2)));
  }
  return out;
}

/* PhET's Remove Divider / Reset Divider.  Removing it just takes it out and
   restarts the flow counters; resetting it regenerates BOTH species in their
   own halves, as PhET does, so the run starts over. */
function removeDivider(w,st){
  const g=w.g;
  gasSetDivided(g,false); st.divided=false; gasFlowOn(g);
  w.hist=[]; w.pairs=[]; w.lastPairs=g.stats.pairHits; histRecord(w);
}
function resetDivider(w,st){
  const g=w.g;
  gasDiffRestart(g,st.d1n,st.d1T,st.d2n,st.d2T); st.divided=true;
  gasRefresh(g); w.hist=[]; w.pairs=[]; w.lastPairs=g.stats.pairHits; g.t=0; histRecord(w);
}

function viewDt(st){ return st.slow?GAS.DT_SLOW:GAS.DT_FRAME; }
function worldStep(w,st,dt){
  const g=w.g;
  const n0=gasCount(g,0), n1=gasCount(g,1);
  gasStep(g,dt);
  pairRecord(w,dt);
  histRecord(w);
  return gasCount(g,0)!==n0||gasCount(g,1)!==n1;
}

/* ---- the models the readout and the views read ------------------------------- */
function fmtT(T,st){ if(T===null||T===undefined||!isFinite(T)) return '—'; return st.unitT==='C'?sigf(T-273.15,4)+' °C':sigf(T,4)+' K'; }
function fmtP(Pk,st){ if(!isFinite(Pk)) return '—'; return Math.round(Pk)+' kPa'; }
function zJ(e){ return e*GAS.KG_PER_AMU*1e21; }
function presetOf(id){ return PRESETS.find(p=>p.id===id)||PRESETS[0]; }
function buildModel(){
  const st=ST, view=st.view, w=worldOf(), g=w.g;
  const N=gasCount(g), n0=gasCount(g,0), n1=gasCount(g,1);
  const M={view,st,w,g,N,nH:n0,nL:n1,T:g.T,t:g.t,oops:g.oops,
           side:gasSideData(g), com:[gasCOM(g,0),gasCOM(g,1)], flow:g.flow,
           Tsp:[gasTemp(g,0),gasTemp(g,1)]};
  M.kT2=g.T===null?null:gasKT2(g.T);
  M.mfp=[mfp(g,0),mfp(g,1)];
  M.tauEff=[tauEffusion(g,0),tauEffusion(g,1)];
  M.tauDif=[tauDiffusive(g,0),tauDiffusive(g,1)];
  M.flowTh=[[flowTheory(g,0,M.side[0].n0),flowTheory(g,0,M.side[1].n0)],
            [flowTheory(g,1,M.side[0].n1),flowTheory(g,1,M.side[1].n1)]];
  M.pairTh=pairRateTheory(g);
  M.pairMe=pairRateMeasured(w);
  M.mean=[gasMeanSpeedOf(g,0),gasMeanSpeedOf(g,1)];
  M.mb=[M.Tsp[0]===null?null:mbMeanSpeed(g.species[0].m,gasKT2(M.Tsp[0])),
        M.Tsp[1]===null?null:mbMeanSpeed(g.species[1].m,gasKT2(M.Tsp[1]))];
  M.graham=Math.sqrt(g.species[0].m/g.species[1].m);
  /* the common temperature the two species must reach: energy is conserved and
     T = (2/3)<KE>/k, so it is the number-weighted mean */
  M.Tmix=(n0+n1)?((n0*(M.Tsp[0]||0)+n1*(M.Tsp[1]||0))/(n0+n1)):null;
  return M;
}

/* ================================================================== *
 *  readout / eqbar / tag                                              *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function readoutHTML(M){
  const st=M.st, g=M.g, D=M.side, sp=g.species;
  let s='<div class="rname">diffusion<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  /* PhET's Data panel */
  s+=hd('left of the divider')+rrow('particle 1, particle 2',D[0].n0+', '+D[0].n1)+rrow('T<sub>avg</sub>',fmtT(D[0].T,st));
  s+=hd('right of the divider')+rrow('particle 1, particle 2',D[1].n0+', '+D[1].n1)+rrow('T<sub>avg</sub>',fmtT(D[1].T,st));
  s+=hd('centre of mass, nm from the middle')
    +rrow('particle 1',M.com[0]===null?'—':sigf(M.com[0]/1000,3),'good')
    +rrow('particle 2',M.com[1]===null?'—':sigf(M.com[1]/1000,3),'good')
    +rrow('each half full is',fmt((g.W/4+g.dividerHalf/2)/1000,3)+' nm');
  if(M.view==='box'||M.view==='flow'){
    s+=hd('particle flow (particles/ps)');
    if(M.flow&&!g.divided){
      s+=rrow('particle 1 → left, → right',fmt(M.flow.rateL[0],2)+', '+fmt(M.flow.rateR[0],2),'good')
        +rrow('… kinetic theory',(M.flowTh[0][1]===null?'—':fmt(M.flowTh[0][1],2))+', '+(M.flowTh[0][0]===null?'—':fmt(M.flowTh[0][0],2)))
        +rrow('particle 2 → left, → right',fmt(M.flow.rateL[1],2)+', '+fmt(M.flow.rateR[1],2),'good')
        +rrow('… kinetic theory',(M.flowTh[1][1]===null?'—':fmt(M.flowTh[1][1],2))+', '+(M.flowTh[1][0]===null?'—':fmt(M.flowTh[1][0],2)));
    } else s+=rrow('the divider is in','nothing crosses');
    s+=rrow('Graham &radic;(m₁/m₂)',fmt(M.graham,3));
  }
  if(M.view==='mixing'){
    s+=hd('how fast it can mix (particle 1)')
      +rrow('&tau;, effusion model',M.tauEff[0]===null?'—':fmt(M.tauEff[0],1)+' ps')
      +rrow('&tau;, Fickian estimate',M.tauDif[0]===null?'—':fmt(M.tauDif[0],1)+' ps')
      +rrow('mean free path &lambda;',M.mfp[0]===null?'—':sigf(M.mfp[0],3)+' pm')
      +rrow('the box, in &lambda;',M.mfp[0]===null?'—':fmt(g.W/M.mfp[0],1),'good');
  }
  if(M.view==='flow'){
    s+=hd('pair collisions per ps');
    if(M.pairMe&&M.pairMe.n>0)
      s+=rrow('measured, last '+fmt(M.pairMe.t,1)+' ps',fmt(M.pairMe.rate,1)+' ± '+fmt(M.pairMe.sd,1),'good')
        +rrow('kinetic theory',M.pairTh===null?'—':fmt(M.pairTh,1))
        +rrow('measured / theory',M.pairTh?fmt(M.pairMe.rate/M.pairTh,3):'—',
              (M.pairTh&&Math.abs(M.pairMe.rate-M.pairTh)<3*M.pairMe.sd)?'good':'');
    else s+=rrow('measured','run the clock');
  }
  if(M.view==='speeds'){
    s+=hd('mean speed, m/s')
      +rrow('particle 1, measured',M.mean[0]===null?'—':sigf(M.mean[0],4),'good')
      +rrow('… Maxwell–Boltzmann',M.mb[0]===null?'—':sigf(M.mb[0],4))
      +rrow('particle 2, measured',M.mean[1]===null?'—':sigf(M.mean[1],4),'good')
      +rrow('… Maxwell–Boltzmann',M.mb[1]===null?'—':sigf(M.mb[1],4))
      +rrow('PhET starts every disk at &radic;(3kT/m), so &lang;v&rang; must fall by','11.38 %');
  }
  s+=hd('the two species')
    +rrow('particle 1: m, r, T',fmt(sp[0].m,0)+' AMU, '+fmt(sp[0].r,0)+' pm, '+fmtT(M.Tsp[0],st))
    +rrow('particle 2: m, r, T',fmt(sp[1].m,0)+' AMU, '+fmt(sp[1].r,0)+' pm, '+fmtT(M.Tsp[1],st))
    +rrow('the common T they must reach',fmtT(M.Tmix,st))
    +rrow('time',fmt(g.t,2)+' ps'+(st.slow?' (slow)':''));
  if(st.showWatch) s+=rrow('stopwatch',fmt(g.watch.t,2)+' ps'+(g.watch.on?' (running)':''));
  s+='</table><div class="note">'+(g.divided
    ?'The divider is in: each species is confined to its own side, and its centre of mass sits at &minus;'+fmt((g.W/4+g.dividerHalf/2)/1000,3)+' nm exactly, whatever the radius.'
    :'The divider is out. The flow rates count crossings of the middle line, averaged over 300 frames as PhET does.')+'</div>';
  return s;
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  if(M.view==='box') return E('x<sub>cm</sub> = &Sigma;m x / &Sigma;m &nbsp;&middot;&nbsp; <span class="hl">at the start it is &minus;(W + d)/4 = &minus;4.025 nm</span>, exactly, whatever the radius',
    'take the divider out and each centre of mass drifts to the middle — not because anything pushes it, but because there are more ways to be mixed than not');
  if(M.view==='mixing') return E('<span class="hl">&Delta;N/N &rarr; 0</span> &nbsp;&middot;&nbsp; effusion: &tau; = (W &minus; 2r)/4&lang;v<sub>x</sub><sup>+</sup>&rang; &nbsp;&middot;&nbsp; Fickian: &tau;<sub>D</sub> = W&sup2;/&pi;&sup2;D, D &asymp; &lang;v&rang;&lambda;/2',
    'the imbalance between the halves falls between two limits: free flight through a mixed gas, and a random walk of step λ');
  if(M.view==='flow') return E('<span class="hl">&Phi; = n &lang;v<sub>x</sub><sup>+</sup>&rang; (H &minus; 2r)</span>, &nbsp; &lang;v<sub>x</sub><sup>+</sup>&rang; = &radic;(kT&#8322;/2&pi;m) = &lang;v&rang;/&pi; &nbsp;&rArr;&nbsp; rate &prop; 1/&radic;m (Graham)',
    'the height cancels, so the rate is N⟨vx⁺⟩/(W/2 − r); the collision rate beside it is Σⱼ nⱼ (rᵢ+rⱼ) ⟨v_rel⟩');
  return E('<span class="hl">f(v) = (m v/kT&#8322;) e<sup>&minus;mv&sup2;/2kT&#8322;</sup></span> &nbsp;&middot;&nbsp; &lang;v&rang; = &radic;(&pi;kT&#8322;/2m) = &radic;(&pi;/4) &times; &radic;(3kT/m)',
    'PhET starts every particle at one speed; collisions turn that spike into Maxwell–Boltzmann and the mean speed falls by exactly 11.38 %');
}
function tagHTML(M){
  const g=M.g;
  if(M.view==='box') return '<b>the divided box</b> — PhET&rsquo;s Diffusion screen'+(g.divided?', divided':', mixing');
  if(M.view==='mixing') return '<b>the mixing</b> — the profiles and the imbalance'+(g.divided?' (take the divider out)':'');
  if(M.view==='flow') return '<b>the flow</b> — measured against kinetic theory'+(g.divided?' (take the divider out)':'');
  return '<b>the speeds</b> — PhET&rsquo;s spike relaxing to Maxwell&ndash;Boltzmann';
}
