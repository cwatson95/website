
/* ================================================================== *
 *  state: the beaker (PhET's two volumes), the pH-meter probe, the    *
 *  clock the dropper and faucets run on, the per-view models, and the *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', off:'#161c2c',
           h3o:'#e8583a', oh:'#5ac8e0', h2o:'#8fa2c4', glass:'#8fb8d4',
           acid:'#e8843a', base:'#7b6cf0', neutral:'#b8ec4c'};
const RO_W=300;
/* the house #hint sits at bottom:11px on top of the last line of a caption anchored at
   H - 12, so every caption here ends HINT_H higher (build/wave-on-a-string/, Known-bad) */
const HINT_H=18;
const FRAME_DT=1/60;             /* a fixed step, so the headless suites are deterministic */

const LAW_LIST=[{id:'exact',name:'exact (Kw)'},{id:'phet',name:'PhET&rsquo;s rule'}];
const UNIT_LIST=[{id:'molar',name:'mol/L'},{id:'moles',name:'moles'}];
const SCALE_LIST=[{id:'log',name:'logarithmic'},{id:'linear',name:'linear'}];
const SOLUTE_LIST=SOLUTES.map(s=>({id:s.id,name:s.name}));

const DEFAULTS={view:TABS[0][0],
  solute:'orangeJuice', vSolute:PHET.AUTOFILL_VOLUME, vWater:0,
  law:'exact', ph:PHET.PH_DEFAULT, vMy:PHET.MY_VOL_DEFAULT,
  units:'molar', scaleKind:'log', linExp:-7,
  ratio:false, counts:false,
  pourSolute:false, pourWater:false, drain:false, running:true};
const ST=Object.assign({},DEFAULTS);

/* the pH meter's probe, in BEAKER-LOCAL coordinates: x across the inner width (0 at the
   left wall, 1 at the right), y up from the floor (0 at the floor, 1 at the brim).  The
   meter reads only when the tip is inside the liquid, exactly as PhET's does. */
const PROBE={x:0.62, y:0.16};
const PROBE0={x:0.62, y:0.16};
const DRAG={what:null};
const DOT_RNG=makeRng(20260921);
/* The tip is in the liquid when it is inside the walls and below the surface.  PhET's
   meter shows nothing when its probe is out of the solution, and so does this one — the
   readout prints "probe is out" rather than a pH, which is the honest thing for a meter
   that is measuring air. */
const PROBE_WALL=0.04;
function probeInLiquid(){
  return PROBE.x>=PROBE_WALL && PROBE.x<=1-PROBE_WALL
      && PROBE.y>=0 && PROBE.y<=fillFrac() && vTotal()>0;
}

function resetBeaker(){
  ST.vSolute=DEFAULTS.vSolute; ST.vWater=DEFAULTS.vWater;
  ST.pourSolute=false; ST.pourWater=false; ST.drain=false;
}

/* ---- the beaker ------------------------------------------------------------------- */
function vTotal(){ return ST.vSolute+ST.vWater; }
function fillFrac(){ return clamp(vTotal()/PHET.BEAKER_VOLUME,0,1); }
function soluteRatio(){ const t=vTotal(); return t>0?ST.vSolute/t:0; }
function currentSolute(){ return soluteById(ST.solute); }

/* The beaker's ions.  For a MIXTURE the net acid C is the primary quantity and both ion
   concentrations come from it — going out to a pH and back loses eight digits at a
   millionfold dilution, because a double holds 7 - eps to an absolute 8.9e-16 and eps is
   all that is left (derive.py measures 4.0e-9 there against 2.2e-12 at a thousandfold).
   The two degenerate cases are exact rather than round-tripped, as PhET's are. */
function beakerIons(){
  const t=vTotal();
  if(!(t>0)) return null;
  const sol=currentSolute();
  if(ST.law==='phet'){
    const p=mixPhet(sol.pH,ST.vSolute,ST.vWater);
    return {ph:p, h:concH3O(p), o:concOH(p), c:netAcid(p), law:'phet'};
  }
  if(ST.vWater===0) return {ph:sol.pH, h:concH3O(sol.pH), o:concOH(sol.pH),
                            c:netAcid(sol.pH), law:'exact'};
  if(ST.vSolute===0) return {ph:PHET.WATER_PH, h:concH3O(PHET.WATER_PH),
                             o:concOH(PHET.WATER_PH), c:0, law:'exact'};
  const c=mixNet(sol.pH,ST.vSolute,PHET.WATER_PH,ST.vWater);
  const h=h3oFromNet(c);
  return {ph:-Math.log10(h), h:h, o:KW/h, c:c, law:'exact'};
}
function beakerPH(){ const i=beakerIons(); return i?i.ph:null; }

/* acidic / neutral / basic, at PhET's own two decimal places: a solution reads neutral
   when the number the meter PRINTS is 7.00, which is what PhET's isEquivalentToWater
   does (it rounds to PH_METER_DECIMAL_PLACES first). */
function phClass(ph){
  if(ph===null||!isFinite(ph)) return 'empty';
  const r=Math.round(ph*100)/100;
  return r===PHET.WATER_PH?'neutral':(r<PHET.WATER_PH?'acidic':'basic');
}

/* ---- the clock: PhET's dropper and faucets ---------------------------------------- */
function stepFrame(){
  if(!ST.running) return false;
  let moved=false;
  const dt=FRAME_DT;
  if(ST.pourSolute){
    const room=PHET.BEAKER_VOLUME-vTotal();
    const d=Math.min(PHET.DROPPER_FLOW*dt,Math.max(0,room));
    if(d>0){ ST.vSolute+=d; moved=true; }
  }
  if(ST.pourWater){
    const room=PHET.BEAKER_VOLUME-vTotal();
    const d=Math.min(PHET.FAUCET_FLOW*dt,Math.max(0,room));
    if(d>0){ ST.vWater+=d; moved=true; }
  }
  if(ST.drain){
    const t=vTotal();
    const d=Math.min(PHET.FAUCET_FLOW*dt,t);
    if(d>0){
      /* draining removes SOLUTION, so the mixture keeps its ratio and its pH */
      const f=(t-d)/t;
      ST.vSolute*=f; ST.vWater*=f; moved=true;
    }
  }
  return moved;
}
/* PhET's autofill: 0.5 L of the chosen solute, straight in */
function autofill(){ ST.vSolute=PHET.AUTOFILL_VOLUME; ST.vWater=0; }
function emptyBeaker(){ ST.vSolute=0; ST.vWater=0; }
/* the beaker holds 1.2 L: setting one volume past the brim pushes the other down.
   Nothing else clamps, so selfTest sweeps the pair and asserts the total never exceeds it. */
function setSolute(v){
  ST.vSolute=clamp(v,0,PHET.BEAKER_VOLUME);
  if(vTotal()>PHET.BEAKER_VOLUME) ST.vWater=PHET.BEAKER_VOLUME-ST.vSolute;
}
function setWater(v){
  ST.vWater=clamp(v,0,PHET.BEAKER_VOLUME);
  if(vTotal()>PHET.BEAKER_VOLUME) ST.vSolute=PHET.BEAKER_VOLUME-ST.vWater;
}

/* ---- the models -------------------------------------------------------------------- */
function beakerModel(){
  const sol=currentSolute(), ions=beakerIons(), vT=vTotal(), r=soluteRatio();
  const M={sol, vS:ST.vSolute, vW:ST.vWater, vT, ratio:r,
           rgb:soluteRGB(sol,r), ions,
           ph:ions?ions.ph:null, cls:phClass(ions?ions.ph:null),
           phExact:mixExact(sol.pH,ST.vSolute,PHET.WATER_PH,ST.vWater),
           phPhet:mixPhet(sol.pH,ST.vSolute,ST.vWater),
           phAvg:mixAverage(sol.pH,ST.vSolute,PHET.WATER_PH,ST.vWater),
           full:vT>=PHET.BEAKER_VOLUME-1e-12, empty:!(vT>0),
           probeIn:probeInLiquid()};
  M.dilution=ST.vSolute>0?vT/ST.vSolute:null;
  if(ions){
    M.molesH=molesOf(ions.h,vT); M.molesO=molesOf(ions.o,vT);
    M.molesW=molesOf(PHET.WATER_CONC,vT);
    M.nH=M.molesH*NA; M.nO=M.molesO*NA; M.nW=M.molesW*NA;
    M.nHphet=M.molesH*NA_PHET;
    M.dots=dotCounts(Math.round(ions.ph*100)/100);
    /* both ratios MAJORITY per minority, whichever ion that is: written as H3O+/OH- a
       basic solution prints "drawn 0.00 : 1", which is arithmetically right and tells
       the reader nothing */
    M.basic=ions.o>ions.h;
    M.majName=M.basic?'OH-':'H3O+'; M.minName=M.basic?'H3O+':'OH-';
    M.majDots=M.basic?M.dots.o:M.dots.h; M.minDots=M.basic?M.dots.h:M.dots.o;
    M.drawnRatio=M.majDots/M.minDots;
    M.trueRatio=M.basic?ions.o/ions.h:ions.h/ions.o;
  }
  return M;
}
function myModel(){
  const ph=ST.ph, v=ST.vMy;
  const h=concH3O(ph), o=concOH(ph);
  return {ph, v, h, o, cls:phClass(ph),
          molesH:molesOf(h,v), molesO:molesOf(o,v), molesW:molesOf(PHET.WATER_CONC,v),
          nH:moleculesOf(h,v), nO:moleculesOf(o,v), nW:moleculesOf(PHET.WATER_CONC,v),
          dots:dotCounts(Math.round(ph*100)/100),
          c:netAcid(ph)};
}
/* the graph and the particle views read whichever solution the file is showing: the
   beaker on ph-scale's Micro screens, and My Solution's slider on its third */
function activeSolution(){
  if(ST.view==='my') { const m=myModel();
    return {ph:m.ph, h:m.h, o:m.o, v:m.v, molesH:m.molesH, molesO:m.molesO,
            molesW:m.molesW, nH:m.nH, nO:m.nO, nW:m.nW, dots:m.dots, from:'my'}; }
  const b=beakerModel();
  if(!b.ions) return {ph:null, h:null, o:null, v:0, from:'beaker', empty:true};
  return {ph:b.ph, h:b.ions.h, o:b.ions.o, v:b.vT, molesH:b.molesH, molesO:b.molesO,
          molesW:b.molesW, nH:b.nH, nO:b.nO, nW:b.nW, dots:b.dots, from:'beaker',
          rgb:b.rgb, sol:b.sol};
}

/* the dilution curves: pH against the dilution factor f = V/V0, three laws.  f runs to a
   millionfold even though the beaker only reaches 80x, because the interesting part —
   where an acid stops being an acid — is past the brim, and the reachable band is shaded
   and named on the canvas. */
const DIL_FMAX=6;                              /* decades of dilution drawn */
function dilutionCurves(ph0,n){
  const ex=[], ph=[], av=[], xs=[];
  const N=n||121;
  for(let i=0;i<=N;i++){
    const lx=DIL_FMAX*i/N, f=Math.pow(10,lx), v1=1, v2=f-1;
    xs.push(lx);
    ex.push(mixExact(ph0,v1,PHET.WATER_PH,v2));
    ph.push(mixPhet(ph0,v1,v2));
    av.push(mixAverage(ph0,v1,PHET.WATER_PH,v2));
  }
  return {xs, exact:ex, phet:ph, avg:av};
}
function dilutionModel(){
  const sol=currentSolute(), b=beakerModel();
  const cur=b.vS>0?Math.log10(b.vT/b.vS):0;
  const C=dilutionCurves(sol.pH,121);
  /* the difference panel: exact - PhET against the STOCK pH, at this dilution.  It is an
     odd function about pH 7 because C(14-pH) = -C(pH) and PhET's branch rule mirrors the
     same way — asserted in derive.py and in selfTest. */
  const f=Math.max(1,Math.pow(10,cur));
  /* The difference panel plots the WORST the two laws can differ over every dilution
     this beaker can hold, against the stock pH -- not the difference at the beaker's
     current dilution, which is identically zero at the default state and drew a flat
     line through the middle of an empty box (Known-bad: a default that makes the view's
     own subject invisible is a defect).  The envelope's peak IS derive.py's headline
     0.0948 pH, and the beaker's own difference is marked on top of it. */
  const fReach=PHET.BEAKER_VOLUME/PHET.MIN_SOLUTION_VOLUME;
  const dx=[], dy=[];
  for(let i=0;i<=160;i++){
    const p=PHET.PH_MIN+(PHET.PH_MAX-PHET.PH_MIN)*i/160;
    let best=0;
    for(let k=0;k<=48;k++){
      const ff=Math.pow(fReach,k/48);
      const d=mixExact(p,1,PHET.WATER_PH,ff-1)-mixPhet(p,1,ff-1);
      if(Math.abs(d)>Math.abs(best)) best=d;
    }
    dx.push(p); dy.push(best);
  }
  let worst=0, worstPh=7;
  for(let i=0;i<dx.length;i++) if(Math.abs(dy[i])>worst){ worst=Math.abs(dy[i]); worstPh=dx[i]; }
  return {sol, C, cur, f, fReach, dx, dy, worst, worstPh,
          hereDiff:(b.phExact===null?null:b.phExact-b.phPhet),
          envHere:(function(){ let best=0;
            for(let k=0;k<=48;k++){ const ff=Math.pow(fReach,k/48);
              const d=mixExact(sol.pH,1,PHET.WATER_PH,ff-1)-mixPhet(sol.pH,1,ff-1);
              if(Math.abs(d)>Math.abs(best)) best=d; }
            return best; })(),
          beakerF:b.vS>0?b.vT/b.vS:null,
          phNow:b.ph, phExact:b.phExact, phPhet:b.phPhet, phAvg:b.phAvg,
          reach:Math.log10(PHET.BEAKER_VOLUME/PHET.MIN_SOLUTION_VOLUME),
          b};
}
function scaleModel(){
  const rows=SOLUTES.map(s=>({s, h:concH3O(s.pH), o:concOH(s.pH),
                              nH:moleculesOf(concH3O(s.pH),PHET.BEAKER_VOLUME)}));
  const act=activeSolution();
  return {rows, act, sourced:SOLUTES.filter(s=>s.range).length};
}
function buildModel(){
  const v=ST.view, M={view:v};
  if(v==='beaker') M.B=beakerModel();
  else if(v==='particles'||v==='graph') { M.A=activeSolution(); M.B=beakerModel(); }
  else if(v==='my') { M.M=myModel(); M.A=activeSolution(); }
  else if(v==='dilution') M.D=dilutionModel();
  else if(v==='liquids') M.L=scaleModel();
  else M.S=scaleModel();
  return M;
}

/* ================================================================== *
 *  readout / equation bar / tag                                       *
 * ================================================================== */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
/* scientific notation.  HTML gets real markup; the canvas gets `1.23e-7`, because a
   superscript minus is not in the rasteriser's font (BRIEF: letter subscripts and exotic
   superscripts are tofu, digits are fine). */
function sci(x,nd){
  if(x===null||!isFinite(x)) return '&mdash;';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x)));
  const m=x/Math.pow(10,e);
  return fmt(m,nd===undefined?2:nd)+' &times; 10<sup>'+e+'</sup>';
}
function sciPlain(x,nd){
  if(x===null||!isFinite(x)) return '—';
  if(x===0) return '0';
  const e=Math.floor(Math.log10(Math.abs(x)));
  const m=x/Math.pow(10,e);
  return fmt(m,nd===undefined?2:nd)+'e'+e;
}
function phStr(ph,nd){
  return (ph===null||!isFinite(ph))?'&mdash;':fmt(ph,nd===undefined?PHET.PH_DECIMALS:nd);
}
function phPlain(ph,nd){
  return (ph===null||!isFinite(ph))?'—':fmt(ph,nd===undefined?PHET.PH_DECIMALS:nd);
}
function volStr(v){ return fmt(v,PHET.VOL_DECIMALS)+' L'; }
const CLS_NAME={acidic:'acidic', neutral:'neutral', basic:'basic', empty:'the beaker is empty'};
const H3O='H<sub>3</sub>O<sup>+</sup>', OHM='OH<sup>&minus;</sup>', H2O='H<sub>2</sub>O';

function ionRows(h,o,v,unitsOn){
  let s='';
  if(!SHOW_CONC) return s;
  if(ST.units==='moles'&&unitsOn!==false){
    s+=rrow(H3O+', moles',sci(molesOf(h,v),3),'good')
      +rrow(OHM+', moles',sci(molesOf(o,v),3))
      +rrow(H2O+', moles',sci(molesOf(PHET.WATER_CONC,v),3));
  } else {
    s+=rrow('['+H3O+']',sci(h,3)+' mol/L','good')
      +rrow('['+OHM+']',sci(o,3)+' mol/L')
      +rrow('['+H2O+']',fmt(PHET.WATER_CONC,0)+' mol/L');
  }
  return s;
}
function readoutHTML(M){
  let s='<div class="rname">pH scale<small>'+TABS.find(t=>t[0]===M.view)[1]+'</small></div><table>';
  if(M.view==='beaker'||M.view==='particles'||M.view==='graph'){
    const B=M.B;
    s+=hd('the beaker')
      +rrow('liquid',B.sol.name)
      +rrow('pH',B.probeIn?phStr(B.ph):'&mdash; <span class="bad">probe is out</span>',
            B.probeIn?'good':'')
      +rrow('',CLS_NAME[B.cls])
      +rrow('liquid poured',volStr(B.vS))
      +rrow('water added',volStr(B.vW))
      +rrow('total volume',volStr(B.vT)+(B.full?' (full)':''))
      +rrow('diluted',B.dilution?fmt(B.dilution,2)+'&times;':'&mdash;');
    if(B.ions){
      s+=hd('what is in it')+ionRows(B.ions.h,B.ions.o,B.vT);
      if(SHOW_CONC){
        s+=rrow(H3O+' molecules',sci(B.nH,3))
          +rrow(OHM+' molecules',sci(B.nO,3))
          +rrow('net acid C',sci(B.ions.c,3)+' mol/L');
      }
    }
    s+=hd('the two dilution laws')
      +rrow('exact, re-solved with K<sub>w</sub>',phStr(B.phExact,4),'good')
      +rrow('PhET&rsquo;s rule',phStr(B.phPhet,4),'')
      +rrow('difference',B.phExact===null?'&mdash;':fmt(B.phExact-B.phPhet,4)+' pH',
            Math.abs(B.phExact-B.phPhet)>0.005?'bad':'')
      +rrow('averaging the pH (wrong)',phStr(B.phAvg,4),'bad');
    if(M.view==='particles'&&B.ions){
      s+=hd('PhET&rsquo;s particle picture')
        +rrow(H3O+' dots',''+B.dots.h)
        +rrow(OHM+' dots',''+B.dots.o)
        +rrow('drawn, '+B.majName+' per '+B.minName,fmt(B.drawnRatio,2)+' : 1')
        +rrow('true, '+B.majName+' per '+B.minName,sci(B.trueRatio,3)+' : 1','bad');
    }
    if(M.view==='graph'&&B.ions){
      s+=hd('the graph')
        +rrow('scale',ST.scaleKind==='log'?'logarithmic':'linear')
        +rrow('units',ST.units==='moles'?'moles':'mol/L')
        +rrow('decades drawn',ST.scaleKind==='log'
              ?fmt(PHET.LOG_EXP_MAX-PHET.LOG_EXP_MIN,0)+' (PhET)'
              :'top of scale '+sci(PHET.LIN_MANTISSA_MAX*Math.pow(10,ST.linExp),2));
    }
  } else if(M.M){
    const m=M.M;
    s+=hd('my solution')
      +rrow('pH',phStr(m.ph),'good')
      +rrow('',CLS_NAME[m.cls])
      +rrow('volume',volStr(m.v))
      +hd('what follows from it')+ionRows(m.h,m.o,m.v);
    if(SHOW_CONC){
      s+=rrow(H3O+' molecules',sci(m.nH,3))
        +rrow(OHM+' molecules',sci(m.nO,3))
        +rrow('with PhET&rsquo;s N<sub>A</sub>',sci(m.h*m.v*NA_PHET,3))
        +rrow('net acid C',sci(m.c,3)+' mol/L');
    }
    s+=hd('the identity')
      +rrow('['+H3O+'][' +OHM+']',sci(m.h*m.o,4),'good')
      +rrow('K<sub>w</sub> at 25 &deg;C',sci(KW,4))
      +rrow('pH + pOH',fmt(m.ph+(PKW-m.ph),4));
  } else if(M.D){
    const D=M.D;
    s+=hd('the liquid')
      +rrow('stock',D.sol.name+', pH '+fmt(D.sol.pH,2))
      +rrow('net acid C',sci(netAcid(D.sol.pH),3)+' mol/L','good')
      +rrow('in the beaker now',D.beakerF?fmt(D.beakerF,2)+'&times; diluted':'&mdash;');
    s+=hd('the three laws, here')
      +rrow('exact, re-solved',phStr(D.phExact,4),'good')
      +rrow('PhET&rsquo;s rule',phStr(D.phPhet,4))
      +rrow('averaging the pH',phStr(D.phAvg,4),'bad')
      +rrow('exact &minus; PhET',D.phExact===null?'&mdash;':fmt(D.phExact-D.phPhet,4)+' pH')
      +rrow('exact &minus; average',D.phExact===null?'&mdash;':fmt(D.phExact-D.phAvg,4)+' pH','bad');
    s+=hd('the worst this beaker can do')
      +rrow('dilution now',fmt(D.f,2)+'&times;')
      +rrow('this beaker can reach',fmt(D.fReach,1)+'&times;')
      +rrow('worst gap, any pH',fmt(D.worst,4)+' pH','bad')
      +rrow('at stock pH',fmt(D.worstPh,2))
      +rrow('worst for this liquid',fmt(Math.abs(D.envHere),4)+' pH');
  } else {
    const S=M.S||M.L;
    s+=hd('PhET&rsquo;s twelve liquids');
    for(const r of S.rows)
      s+=rrow(r.s.name,fmt(r.s.pH,2),r.s.id===ST.solute?'good':'');
    s+=hd('measured ranges')
      +rrow('sourced here',S.sourced+' of '+SOLUTES.length)
      +rrow('blood','7.37&ndash;7.43')
      +rrow('orange juice','3.30&ndash;4.19')
      +rrow('milk','6.40&ndash;6.80')
      +rrow('chicken broth','5.80');
    /* the two concentrations are this view's SUBJECT, so they are printed even in the
       Basics build, whose beaker readout drops them as PhET's Basics does */
    if(S.act&&S.act.ph!==null&&M.S){
      s+=hd('where the beaker sits')
        +rrow('pH',phStr(S.act.ph),'good')
        +rrow('['+H3O+']',sci(S.act.h,3))
        +rrow('['+OHM+']',sci(S.act.o,3));
    } else if(S.act&&S.act.ph!==null){
      s+=hd('where the beaker sits')+rrow('pH',phStr(S.act.ph),'good')
        +rrow('the liquid',S.act.sol?S.act.sol.name:'—');
    }
  }
  s+='</table><div class="note">'+roNote(M)+'</div>';
  return s;
}
function roNote(M){
  const v=M.view;
  if(v==='beaker') return 'Every liquid here is treated as a STRONG acid or base of the stated pH &mdash; fully dissociated, no buffering. That is PhET&rsquo;s model too, and for blood it is a fiction: blood is a bicarbonate buffer and does not dilute like this.';
  if(v==='particles') return 'The dots are PhET&rsquo;s drawing rule, not a count: 50 per 10<sup>&minus;7</sup> mol/L inside pH 6&ndash;8, and outside it the minority ramps to 3000 while the majority saturates. The readout prints the drawn ratio and the true one.';
  if(v==='graph') return 'PhET&rsquo;s graph spans 18 decades on the logarithmic scale, which is the only way to put 10<sup>&minus;16</sup> and 55 mol/L on one axis. The linear scale can show one pair at a time, which is the point it makes.';
  if(v==='my') return 'Nothing is being mixed here: the pH is set and the two concentrations follow from [' +H3O+'] = 10<sup>&minus;pH</sup> and ['+OHM+'] = K<sub>w</sub>/['+H3O+']. Their product is K<sub>w</sub> at every setting, which the readout checks.';
  if(v==='dilution') return 'What dilutes is C = ['+H3O+'] &minus; ['+OHM+'], the net strong acid, because it is the quantity moles of which are conserved. Averaging the pH is wrong by whole units; PhET&rsquo;s rule is wrong by up to 0.095.';
  return 'PhET&rsquo;s pH values are the data. Four of the twelve have a measured range that could be sourced, and PhET&rsquo;s value lies inside every one of them; the other eight carry PhET&rsquo;s number alone and are drawn without a range.';
}
function eqbarHTML(M){
  const E=(eq,sm)=>'<span class="lhs">'+eq+'</span><span class="sm">'+sm+'</span>';
  const v=M.view;
  if(v==='beaker') return E('<span class="hl">['+H3O+'] = 10<sup>&minus;pH</sup></span>, &nbsp; ['+OHM+'] = K<sub>w</sub>/['+H3O+'], &nbsp; K<sub>w</sub> = 1.00 &times; 10<sup>&minus;14</sup> at 25 &deg;C',
    'the pH is nothing but a logarithm of the hydronium concentration, and the hydroxide is whatever is left once the water&rsquo;s own equilibrium is satisfied');
  if(v==='particles') return E('N = ['+H3O+'] V N<sub>A</sub> &nbsp;&rArr;&nbsp; <span class="hl">7.23 &times; 10<sup>16</sup></span> hydronium ions in 1.2 L of neutral water',
    'a beaker of pure water is not inert: a hundred million billion of its molecules have swapped a proton at any instant, and that is what pH 7 means');
  if(v==='graph') return E('['+H2O+'] = 55 mol/L &nbsp;&Gt;&nbsp; ['+H3O+']['+OHM+'] = <span class="hl">K<sub>w</sub> = 10<sup>&minus;14</sup></span>',
    'water outnumbers both ions by fourteen to eighteen orders of magnitude, so the logarithmic scale is not a stylistic choice');
  if(v==='my') return E('pH + pOH = <span class="hl">14</span>, &nbsp; ['+H3O+']['+OHM+'] = K<sub>w</sub>',
    'move one and the other moves the opposite way by the same amount: the product is fixed by the water, not by what you dissolved in it');
  if(v==='dilution') return E('<span class="hl">C = ['+H3O+'] &minus; ['+OHM+'] = C<sub>0</sub>V<sub>0</sub>/V</span>, &nbsp; then ['+H3O+'] &minus; K<sub>w</sub>/['+H3O+'] = C',
    'the net strong acid is what dilutes &mdash; it is a difference of analytical concentrations, so its moles are conserved; the pH follows by re-solving, and never by averaging');
  return E('C(pH) = &minus;2&radic;K<sub>w</sub> sinh[ln10 (pH &minus; 7)] &nbsp;&rArr;&nbsp; <span class="hl2">C(14 &minus; pH) = &minus;C(pH)</span>',
    'the scale is antisymmetric about 7: pH 2 and pH 12 are exactly as strong as one another, and equal volumes of them are exactly neutral');
}
function tagHTML(M){
  const v=M.view, nm=TABS.find(t=>t[0]===v)[1];
  if(M.B&&(v==='beaker'||v==='particles'||v==='graph')){
    const B=M.B, bits=[B.sol.name];
    if(B.empty) bits.push('the beaker is empty');
    else {
      bits.push(volStr(B.vT));
      bits.push('pH '+phPlain(B.ph));
      if(B.vW>0) bits.push(fmt(B.dilution,2)+'× diluted');
      if(ST.law==='phet') bits.push('PhET’s rule');
    }
    if(!ST.running) bits.push('paused');
    return '<b>'+nm+'</b> &mdash; '+bits.join(', ');
  }
  if(M.M) return '<b>'+nm+'</b> &mdash; pH '+phPlain(M.M.ph)+', '+volStr(M.M.v)+', '+CLS_NAME[M.M.cls];
  if(M.D) return '<b>'+nm+'</b> &mdash; '+M.D.sol.name+', stock pH '+fmt(M.D.sol.pH,2)
    +', worst gap '+fmt(M.D.worst,4)+' pH';
  return '<b>'+nm+'</b> &mdash; PhET&rsquo;s twelve liquids, and the two ions behind the number';
}
