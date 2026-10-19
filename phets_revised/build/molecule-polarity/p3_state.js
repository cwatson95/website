
/* ================================================================== *
 *  state, the live field rotation, the per-view model, readout,       *
 *  equation bar and tag                                               *
 * ================================================================== */
const COL={pos:'#b8ec4c', ref:'#e8843a', live:'#cd35c4', struct:'#5ac8e0', dim:'#8b93a6',
           edge:'#242a3a', text:'#aeb6c6', bond:'#9aa2b4', plateP:'#e8843a', plateN:'#5ac8e0',
           atomA:'rgb(255,255,90)', atomB:'rgb(0,255,0)', atomC:'rgb(255,175,175)'};
const RO_W=300;
const TABS=[['two','two atoms'],['three','three atoms'],['real','real molecules'],
            ['sum','the vector sum'],['field','the field'],['atlas','the dipole atlas']];

const DEFAULTS={view:'two',
  enA:2, enB:3, enC:2,                       /* PhET's defaults (B starts mid-range) */
  angAB:5*PI/6, angBC:PI/6,                  /* PhET's defaults: a 120 deg A-B-C angle */
  molAngle:0,
  surface:'none',                            /* none | density | potential */
  showBondDipole:true, showMolDipole:true, showCharges:false, showBondChar:true,
  showLabels:true,
  field:false, fieldE:1, zeta:0.7, fieldMode:'rotor',
  dipoleDir:'posneg',                        /* PhET's preference: positive to negative */
  mol:'H2O', realMode:'basic', surfColor:'rwb',
  camTheta:-1.05, camPhi:0.34, zoom:1,
  psi0:150};                                 /* the field view's start angle, degrees */
const ST=Object.assign({},DEFAULTS);
const MEMO={};
function memo(name,key,fn){ const m=MEMO[name]; if(m&&m.key===key) return m.val; const val=fn(); MEMO[name]={key,val}; return val; }

/* ---------------------------------------------------------------- *
 *  the molecule of the current model view, at a given rotation       *
 * ---------------------------------------------------------------- */
function molAt(view,theta){
  return view==='three'?triatomic(ST.enA,ST.enB,ST.enC,ST.angAB,ST.angBC,theta)
                       :diatomic(ST.enA,ST.enB,theta);
}
function liveMol(){ return molAt(ST.view==='three'?'three':'two',ST.molAngle); }
/* the dipole direction preference rotates every arrow by pi (PhET) */
function dirSign(){ return ST.dipoleDir==='negpos'?-1:1; }
function shownDipole(v){ const s=dirSign(); return [s*v[0],s*v[1]]; }

/* ---------------------------------------------------------------- *
 *  the field: the molecule turns until its (shown) dipole points +x  *
 *  -- at the positive plate, PhET's alignment.                       *
 * ---------------------------------------------------------------- */
const FIELD={w:0, t:0, idle:false};
function fieldIntrinsic(view){ const m=molAt(view,0); return {mu:vmag(m.mu), psi0:vang(m.mu)}; }
/* psi: the angle of the SHOWN dipole; 0 is aligned */
function fieldPsi(){
  const v=molAt(ST.view==='three'?'three':'two',ST.molAngle).mu;
  return normAngle(vang(shownDipole(v)),-PI);
}
function setFieldPsi(psi){
  const f=fieldIntrinsic(ST.view==='three'?'three':'two');
  const base=f.psi0+(dirSign()<0?PI:0);
  ST.molAngle=normAngle(psi-base,-PI);
}
function fieldReset(){ FIELD.w=0; FIELD.t=0; FIELD.idle=false; }
/* one frame of the alignment.  Returns true if anything moved. */
function fieldStep(dt){
  if(!ST.field||(ST.view!=='two'&&ST.view!=='three')) return false;
  const f=fieldIntrinsic(ST.view==='three'?'three':'two');
  if(!(f.mu>1e-9)){ FIELD.idle=true; return false; }
  let psi=fieldPsi();
  if(ST.fieldMode==='phet'){
    /* PhET's rule, at its own 60 Hz frame clock */
    const n=Math.max(1,Math.min(20,Math.round(dt*60)));
    let p=normAngle(psi);
    for(let k=0;k<n;k++) p=phetAdvance(p,f.mu);
    const moved=Math.abs(normAngle(p,-PI)-psi)>1e-15;
    setFieldPsi(normAngle(p,-PI)); FIELD.w=0; FIELD.idle=!moved;
    return moved;
  }
  const muE=f.mu*ST.fieldE;
  if(!(muE>1e-12)){ FIELD.idle=true; return false; }
  const b=rotorB(ST.zeta,muE);
  const hh=Math.min(dt,0.05), ns=Math.max(1,Math.min(40,Math.ceil(hh/0.004))), hs=hh/ns;
  let w=FIELD.w;
  for(let k=0;k<ns;k++){ const r=rotorStep(psi,w,muE,b,hs); psi=r[0]; w=r[1]; }
  FIELD.t+=hh;
  if(Math.abs(normAngle(psi,-PI))<1e-7&&Math.abs(w)<1e-7){ psi=0; w=0; FIELD.idle=true; }
  else FIELD.idle=false;
  FIELD.w=w; setFieldPsi(normAngle(psi,-PI));
  return !FIELD.idle;
}

/* ---------------------------------------------------------------- *
 *  the vector-sum view: |mu|(theta) for the current EN triple        *
 * ---------------------------------------------------------------- */
const SUM_N=181;
function sumCurve(dAB,dBC){
  const xs=[], ys=[];
  for(let k=0;k<SUM_N;k++){ const d=180*k/(SUM_N-1); xs.push(d); ys.push(mumagClosed(dAB,dBC,d*PI/180)); }
  return {xs,ys};
}
function sumFamily(){
  const dAB=ST.enB-ST.enA;
  return memo('fam',fmt(dAB,6),()=>[0.5,1.0,1.5,2.0].map(d=>({d,c:sumCurve(d,-d)})));
}

/* ---------------------------------------------------------------- *
 *  the field view: the three damping traces and PhET's staircase     *
 * ---------------------------------------------------------------- */
const FV={T:24, DT:0.004};
function fieldTrace(zeta,muE,psi0){
  const b=rotorB(zeta,muE), n=Math.round(FV.T/FV.DT);
  const xs=[], ys=[], vs=[];
  let p=psi0, w=0;
  for(let k=0;k<=n;k++){ xs.push(k*FV.DT); ys.push(p*180/PI); vs.push(w);
    if(k<n){ const r=rotorStep(p,w,muE,b,FV.DT); p=r[0]; w=r[1]; } }
  return {xs,ys,vs,b};
}
function phetTrace(mu,psi0){
  const xs=[], ys=[]; let p=normAngle(psi0);
  const n=Math.round(FV.T*60);
  for(let k=0;k<=n;k++){ xs.push(k/60); ys.push(normAngle(p,-PI)*180/PI); p=phetAdvance(p,mu); }
  return {xs,ys};
}
function settleTime(tr,tol){
  const need=Math.round(1.0/FV.DT);
  for(let i=0;i<tr.ys.length;i++){
    let good=true;
    for(let j=i;j<Math.min(tr.ys.length,i+need);j++) if(Math.abs(tr.ys[j])>=tol){ good=false; break; }
    if(good) return tr.xs[i];
  }
  return null;
}

/* ---------------------------------------------------------------- *
 *  the atlas                                                         *
 * ---------------------------------------------------------------- */
function atlasRows(){
  return memo('atlas','1',()=>MOLORDER.map(s=>{
    const r=realMol(s), m=measuredOf(s);
    return {sym:s,name:r.name,psi4:r.psi4mag,basic:r.sumBasicMag,adv:r.sumAdvMag,
            meas:m?m[0]:null,src:m?m[1]:null,
            diff:m?r.psi4mag-m[0]:null};
  }));
}
function atlasStats(){
  return memo('atlasStats','1',()=>{
    const rows=atlasRows().filter(r=>r.meas!==null);
    const d=rows.map(r=>Math.abs(r.diff));
    const worst=rows.slice().sort((a,b)=>Math.abs(b.diff)-Math.abs(a.diff))[0];
    return {n:rows.length,mae:d.reduce((a,b)=>a+b,0)/d.length,worst,
            zero:atlasRows().filter(r=>r.psi4<1e-3).map(r=>r.sym)};
  });
}

/* ---------------------------------------------------------------- *
 *  the per-view model                                                *
 * ---------------------------------------------------------------- */
function buildModel(){
  const st=ST, M={st,view:st.view};
  if(st.view==='two'){
    const m=diatomic(st.enA,st.enB,st.molAngle);
    M.m=m; M.dEN=m.dEN; M.character=bondCharacter(m.dEN);
    M.charFrac=Math.abs(m.dEN)/EN_SPAN;
    M.psi=fieldPsi(); M.muE=vmag(molAt('two',0).mu)*st.fieldE;
  } else if(st.view==='three'){
    const m=triatomic(st.enA,st.enB,st.enC,st.angAB,st.angBC,st.molAngle);
    M.m=m; M.bondAngleDeg=Math.abs(m.bondAngle)*180/PI;
    M.closed=mumagClosed(m.dAB,m.dBC,m.bondAngle);
    M.polarity=polarityOf(m.mumag);
    M.psi=fieldPsi(); M.muE=vmag(molAt('three',0).mu)*st.fieldE;
  } else if(st.view==='real'){
    M.r=realMol(st.mol); M.d=realDipoles(st.mol,st.realMode==='advanced');
    M.meas=measuredOf(st.mol); M.known=ANGLES_KNOWN[st.mol]||null;
  } else if(st.view==='sum'){
    const m=triatomic(st.enA,st.enB,st.enC,st.angAB,st.angBC,0);
    M.m=m; M.bondAngleDeg=Math.abs(m.bondAngle)*180/PI;
    M.curve=sumCurve(m.dAB,m.dBC); M.family=sumFamily();
    M.atMax=Math.abs(m.dAB-m.dBC); M.atMin=Math.abs(m.dAB+m.dBC);
    M.symmetric=Math.abs(m.dAB+m.dBC)<1e-12;
    M.here=mumagClosed(m.dAB,m.dBC,m.bondAngle);
  } else if(st.view==='field'){
    const f=fieldIntrinsic('three');
    M.mu=f.mu; M.muE=f.mu*st.fieldE;
    M.psi0=st.psi0*PI/180;
    M.traces=memo('ftr',[st.enA,st.enB,st.enC,st.angAB,st.angBC,st.fieldE,st.psi0,st.zeta].join(','),
      ()=>{ const out={};
        for(const z of [0.2,1,2]) out['z'+z]=fieldTrace(z,M.muE,M.psi0);
        out.live=fieldTrace(st.zeta,M.muE,M.psi0);
        out.phet=phetTrace(M.mu,M.psi0);
        return out; });
    M.omega0=rotorOmega0(M.muE); M.bcrit=2*Math.sqrt(ROTOR_I*M.muE);
    M.b=rotorB(st.zeta,M.muE);
    M.settle=M.muE>1e-9?settleTime(M.traces.live,0.5):null;
    M.phetFrames=M.mu>1e-9?Math.ceil(Math.abs(normAngle(M.psi0)<PI?normAngle(M.psi0):TAU-normAngle(M.psi0))/phetFieldStep(M.mu)):null;
  } else {
    M.rows=atlasRows(); M.stats=atlasStats();
  }
  return M;
}

/* ---------------------------------------------------------------- *
 *  readout / eqbar / tag                                             *
 * ---------------------------------------------------------------- */
function hd(t){ return '<tr><td class="hd" colspan="2">'+t+'</td></tr>'; }
function rrow(a,b,cls){ return '<tr><td>'+a+'</td><td class="v'+(cls?' '+cls:'')+'">'+b+'</td></tr>'; }
function degs(v){ return fmt(v,1)+'&deg;'; }
function signed(v,n){ return (v>=0?'+':'&minus;')+fmt(Math.abs(v),n===undefined?2:n); }
function formulaHTML(s){ return s.replace(/([A-Za-z])(\d+)/g,'$1<sub>$2</sub>'); }
function dirTxt(){ return ST.dipoleDir==='negpos'?'negative &rarr; positive':'positive &rarr; negative'; }
function surfTxt(){ return ST.surface==='none'?'none':ST.surface==='density'?'electron density':'electrostatic potential'; }

function readoutHTML(M){
  const st=M.st; let h='';
  if(M.view==='two'){
    const m=M.m;
    h+='<div class="rname">A&ndash;B<small>EN(A) = '+fmt(st.enA,1)+', EN(B) = '+fmt(st.enB,1)
      +' &middot; '+M.character+'</small></div><table>';
    h+=hd('the bond')+rrow('&Delta;EN = EN(B) &minus; EN(A)',signed(m.dEN,2),'good')
      +rrow('bond dipole |&mu;|',fmt(m.mumag,2)+' (PhET units)','good')
      +rrow('points at',m.dEN===0?'&mdash; (no dipole)':(m.dEN>0?'B':'A')+(st.dipoleDir==='negpos'?' (arrow reversed)':''))
      +rrow('arrow length',fmt(dipolePx(m.mumag),1)+' px of PhET&rsquo;s 135');
    h+=hd('partial charges')+rrow('atom A',signed(m.qA,2),m.qA>0?'good':m.qA<0?'bad':'')
      +rrow('atom B',signed(m.qB,2),m.qB>0?'good':m.qB<0?'bad':'')
      +rrow('sum',fmt(m.qA+m.qB,2));
    h+=hd('bond character')+rrow('band (PhET&rsquo;s)',M.character,'good')
      +rrow('along the bar',fmt(100*M.charFrac,1)+'% toward ionic');
    h+=hd('the surface')+rrow('showing',surfTxt())
      +rrow('gradient width',st.surface==='none'?'&mdash;':fmt(gradWidth(st.surface,m.dEN),1)+' of '+fmt(surfaceWidth(),0));
    if(st.field) h+=hd('the field')+rrow('mode',st.fieldMode==='phet'?'PhET&rsquo;s rule':'damped rotor, &zeta; = '+fmt(st.zeta,2))
      +rrow('dipole angle &psi;',degs(M.psi*180/PI),Math.abs(M.psi)<0.01?'good':'')
      +rrow('state',m.mumag<1e-9?'no dipole: nothing turns':FIELD.idle?'aligned':'turning',m.mumag<1e-9?'bad':FIELD.idle?'good':'');
    h+='</table><div class="note">The bond dipole is PhET&rsquo;s own rule: its magnitude is |&Delta;EN| exactly, and it lies along the bond, '
      +'pointing at the more electronegative atom. The partial charges are &plusmn;&Delta;EN. Nothing here is in debye &mdash; PhET&rsquo;s '
      +'two model screens carry no unit at all, which is the honest way to draw a quantity that is only linear in &Delta;EN by assumption.</div>';
  } else if(M.view==='three'){
    const m=M.m;
    h+='<div class="rname">A&ndash;B&ndash;C<small>'+degs(M.bondAngleDeg)+' &middot; '+M.polarity+'</small></div><table>';
    h+=hd('the two bonds')+rrow('&Delta;EN(A&rarr;B)',signed(m.dAB,2))+rrow('&Delta;EN(B&rarr;C)',signed(m.dBC,2))
      +rrow('|&mu;<sub>AB</sub>|',fmt(vmag(m.muAB),3),'good')+rrow('|&mu;<sub>BC</sub>|',fmt(vmag(m.muBC),3),'good');
    h+=hd('the molecular dipole')+rrow('|&mu;| = |&mu;<sub>AB</sub> + &mu;<sub>BC</sub>|',fmt(m.mumag,6),'good')
      +rrow('closed form',fmt(M.closed,6))
      +rrow('difference',sigf(Math.abs(m.mumag-M.closed),2))
      +rrow('direction',m.mumag<1e-12?'&mdash; (it cancels)':degs(m.muang*180/PI));
    h+=hd('partial charges')+rrow('A / B / C',signed(m.qA,2)+' / '+signed(m.qB,2)+' / '+signed(m.qC,2))
      +rrow('sum',fmt(m.qA+m.qB+m.qC,2),'good');
    if(st.field) h+=hd('the field')+rrow('mode',st.fieldMode==='phet'?'PhET&rsquo;s rule':'damped rotor, &zeta; = '+fmt(st.zeta,2))
      +rrow('dipole angle &psi;',degs(M.psi*180/PI),Math.abs(M.psi)<0.01?'good':'')
      +rrow('state',m.mumag<1e-9?'no dipole: nothing turns':FIELD.idle?'aligned':'turning',m.mumag<1e-9?'bad':FIELD.idle?'good':'');
    h+='</table><div class="note">The molecular dipole is the vector sum of the two bond dipoles, exactly, at every angle. '
      +'With EN(A) = EN(C) the two bond dipoles are equal and opposite in the bond directions, so the sum is '
      +'2|&Delta;EN| |cos(&theta;/2)| and it vanishes identically at &theta; = 180&deg;. That is why CO<sub>2</sub> is non-polar and water is not.</div>';
  } else if(M.view==='real'){
    const r=M.r, d=M.d;
    h+='<div class="rname">'+formulaHTML(r.sym)+' &mdash; '+r.name+'<small>'+(st.realMode==='advanced'?'advanced (quantum)':'basic (electronegativity)')+'</small></div><table>';
    h+=hd('bond dipoles ('+(st.realMode==='advanced'?'debye, from the Hirshfeld charges':'|&Delta;EN|, Pauling')+')');
    const seen={};
    d.bd.forEach((v,i)=>{ const [ia,ib]=r.bonds[i], key=r.syms[ia]+'&ndash;'+r.syms[ib];
      const val=fmt(v3len(v),3); seen[key]=seen[key]||[]; seen[key].push(val); });
    for(const k in seen) h+=rrow(k+(seen[k].length>1?' ('+seen[k].length+')':''),seen[k][0],'good');
    h+=rrow('vector sum |&Sigma;&mu;|',fmt(d.mag,4),'good');
    h+=hd('the molecular dipole');
    if(st.realMode==='advanced'){
      h+=rrow('PhET&rsquo;s value (Psi4)',fmt(r.psi4mag,3)+' D','good');
      h+=rrow('arrow scale',fmt(d.scale,4)+' &times;');
    } else h+=rrow('vector sum',fmt(r.sumBasicMag,4)+' (PhET units)','good');
    if(M.meas) h+=rrow('measured (CCCBDB)',fmt(M.meas[0],3)+' D','good')+rrow('source',M.meas[1]);
    else h+=rrow('measured','not in CCCBDB','bad');
    if(st.realMode==='advanced'&&M.meas) h+=rrow('Psi4 &minus; measured',signed(r.psi4mag-M.meas[0],3)+' D',
      Math.abs(r.psi4mag-M.meas[0])<0.1?'good':'bad');
    if(r.angles.length){
      h+=hd('PhET&rsquo;s stored geometry');
      h+=rrow('bond angles at '+r.syms[r.centre],r.angles.length>3?fmt(r.angles[0],1)+'&deg;&ndash;'+fmt(r.angles[r.angles.length-1],1)+'&deg;'
        :r.angles.map(a=>fmt(a,1)+'&deg;').join(', '));
      if(M.known){ const near=r.angles.reduce((p,c)=>Math.abs(c-M.known[1])<Math.abs(p-M.known[1])?c:p,r.angles[0]);
        h+=rrow(M.known[0]+' ('+(M.known[2]==='symmetry'?'by symmetry':'CCCBDB')+')',fmt(M.known[1],2)+'&deg;')
          +rrow('stored &minus; that',signed(near-M.known[1],2)+'&deg;',Math.abs(near-M.known[1])<0.5?'good':'bad'); }
      h+=rrow('bond lengths',fmt(Math.min.apply(null,r.lengths),3)+'&ndash;'+fmt(Math.max.apply(null,r.lengths),3)+' &Aring;');
    }
    h+=hd('partial charges (Hirshfeld)');
    const qs={}; r.syms.forEach((s,i)=>{ qs[s]=qs[s]||[]; qs[s].push(r.q[i]); });
    for(const s in qs) h+=rrow(s,signed(qs[s][0],3)+(qs[s].length>1?' (&times;'+qs[s].length+')':''),qs[s][0]<0?'bad':'good');
    h+='</table><div class="note">Basic uses the same rule as the two model screens, on the Pauling electronegativities PhET&rsquo;s element '
      +'table carries. Advanced uses the quantum numbers PhET ships: Hirshfeld charges for the bond dipoles and a Psi4 molecular dipole in debye. '
      +'The geometry is PubChem&rsquo;s, and it is not always the measured one &mdash; ammonia is stored 11.6&deg; too narrow.</div>';
  } else if(M.view==='sum'){
    const m=M.m;
    h+='<div class="rname">|&mu;| against the bond angle<small>&Delta;EN(A&rarr;B) = '+signed(m.dAB,2)
      +', &Delta;EN(B&rarr;C) = '+signed(m.dBC,2)+'</small></div><table>';
    h+=hd('at this angle')+rrow('&theta;',degs(M.bondAngleDeg))+rrow('|&mu;|',fmt(M.here,6),'good');
    h+=hd('the two ends')+rrow('&theta; = 0: |&Delta;<sub>AB</sub> &minus; &Delta;<sub>BC</sub>|',fmt(M.atMax,6))
      +rrow('&theta; = 180: |&Delta;<sub>AB</sub> + &Delta;<sub>BC</sub>|',fmt(M.atMin,6),M.symmetric?'good':'');
    h+=rrow('symmetric (EN(A) = EN(C))?',M.symmetric?'yes &mdash; it cancels exactly':'no',M.symmetric?'good':'bad');
    h+=hd('the law')+rrow('|&mu;|&sup2;','&Delta;<sub>AB</sub>&sup2; + &Delta;<sub>BC</sub>&sup2; &minus; 2&Delta;<sub>AB</sub>&Delta;<sub>BC</sub> cos&theta;')
      +rrow('symmetric case','2|&Delta;EN| |cos(&theta;/2)|');
    h+='</table><div class="note">The magnitude of a sum of two vectors depends on the angle between them, and that is the whole of it: '
      +'turn the bonds and the molecular dipole runs from |&Delta;<sub>AB</sub> &minus; &Delta;<sub>BC</sub>| at 0&deg; down to '
      +'|&Delta;<sub>AB</sub> + &Delta;<sub>BC</sub>| at 180&deg;. Only the symmetric molecule reaches zero, and it reaches it exactly.</div>';
  } else if(M.view==='field'){
    h+='<div class="rname">The alignment<small>|&mu;| = '+fmt(M.mu,2)+', E = '+fmt(ST.fieldE,2)+', &zeta; = '+fmt(ST.zeta,2)+'</small></div><table>';
    h+=hd('the rotor')+rrow('&mu;E',fmt(M.muE,4))+rrow('&omega;&#8320; = &radic;(&mu;E / I)',fmt(M.omega0,6),'good')
      +rrow('b = 2&zeta;&radic;(I&mu;E)',fmt(M.b,6))+rrow('critical b',fmt(M.bcrit,6),'')
      +rrow('regime',ST.zeta<1?'underdamped &mdash; it overshoots':ST.zeta>1?'overdamped &mdash; it creeps':'critically damped',ST.zeta===1?'good':'');
    h+=rrow('settles (|&psi;| &lt; 0.5&deg;)',M.settle===null?'&mdash;':fmt(M.settle,2)+' s',M.settle===null?'bad':'good');
    h+=hd('PhET&rsquo;s rule')+rrow('step per frame',fmt(phetFieldStep(M.mu),4)+' rad')
      +rrow('frames from '+degs(ST.psi0),M.phetFrames===null?'&mdash;':M.phetFrames)
      +rrow('at 60 fps',M.phetFrames===null?'&mdash;':fmt(M.phetFrames/60,3)+' s');
    h+=hd('the equilibria')+rrow('&psi; = 0','stable','good')+rrow('&psi; = 180&deg;','unstable','bad');
    h+='</table><div class="note">A dipole in a field feels a torque &minus;&mu;E sin&psi;, so the molecule is a pendulum: '
      +'it swings to alignment and the damping decides whether it overshoots. The energy &frac12;I&psi;&#775;&sup2; + &mu;E(1 &minus; cos&psi;) '
      +'can only fall, which is why &psi; = 0 is reached from anywhere but the unstable point itself. PhET instead moves the angle a fixed '
      +'step per frame, so its molecule arrives at constant speed and stops dead.</div>';
  } else {
    const s=M.stats;
    h+='<div class="rname">Nineteen molecules<small>PhET&rsquo;s Psi4 dipole against measurement</small></div><table>';
    h+=hd('the comparison')+rrow('molecules with a measured value',s.n)
      +rrow('mean |Psi4 &minus; measured|',fmt(s.mae,3)+' D','good')
      +rrow('worst',formulaHTML(s.worst.sym)+' '+signed(s.worst.diff,3)+' D','bad');
    h+=hd('the non-polar set')+rrow('|&mu;| &lt; 0.001 D',s.zero.map(formulaHTML).join(', '),'good')
      +rrow('why','every one is symmetric: the bond dipoles cancel');
    h+=hd('basic mode')+rrow('ozone, |&Sigma;&mu;| basic',fmt(realMol('O3').sumBasicMag,3),'bad')
      +rrow('ozone, measured',fmt(measuredOf('O3')[0],3)+' D');
    h+='</table><div class="note">Basic mode makes every bond dipole a function of &Delta;EN alone, so ozone &mdash; three oxygens &mdash; '
      +'comes out exactly non-polar, and it is not: it measures 0.530 D. That is the model&rsquo;s own boundary, drawn on the lower panel. '
      +'The quantum column does far better, and its two clear misses, water and ozone, are both traceable to PhET&rsquo;s stored geometry.</div>';
  }
  return h;
}
function eqbarHTML(M){
  const v=M.view;
  if(v==='two') return '<span class="lhs">&mu;<sub>bond</sub></span> = &Delta;EN &middot; <b>u</b><sub>A&rarr;B</sub>, &nbsp; &Delta;EN = EN(B) &minus; EN(A), &nbsp; q<sub>A</sub> = +&Delta;EN, q<sub>B</sub> = &minus;&Delta;EN'
    +'<span class="sm">PhET&rsquo;s rule: the dipole is exactly linear in the electronegativity difference and lies along the bond</span>';
  if(v==='three') return '<span class="lhs">&mu;<sub>mol</sub></span> = &mu;<sub>AB</sub> + &mu;<sub>BC</sub>, &nbsp; |&mu;<sub>mol</sub>|&sup2; = &Delta;<sub>AB</sub>&sup2; + &Delta;<sub>BC</sub>&sup2; &minus; 2&Delta;<sub>AB</sub>&Delta;<sub>BC</sub> cos&theta;'
    +'<span class="sm">the molecular dipole is the vector sum of the bond dipoles, at every bond angle</span>';
  if(v==='real') return '<span class="lhs">&mu;<sub>bond</sub></span> = |q<sub>1</sub> &minus; q<sub>2</sub>|/2 &middot; d / 0.208194 &nbsp;<span class="hl2">(debye, advanced)</span>, &nbsp; |&Delta;EN| <span class="hl2">(basic)</span>'
    +'<span class="sm">PhET&rsquo;s two modes: Hirshfeld charges across the measured bond length, or the electronegativity difference alone</span>';
  if(v==='sum') return '<span class="lhs">|&mu;|</span> = 2|&Delta;EN| |cos(&theta;/2)| &nbsp;<span class="hl2">(EN(A) = EN(C))</span>, &nbsp; = 0 <span class="hl2">at &theta; = 180&deg; exactly</span>'
    +'<span class="sm">why a symmetric triatomic can be built of polar bonds and still be non-polar</span>';
  if(v==='field') return '<span class="lhs">I &psi;&#776;</span> = &minus;&mu;E sin&psi; &minus; b&psi;&#775;, &nbsp; b = 2&zeta;&radic;(I&mu;E), &nbsp; &psi; &rarr; 0'
    +'<span class="sm">a dipole in a field is a damped pendulum; PhET turns it at a constant 0.085|&mu;| rad per frame instead</span>';
  return '<span class="lhs">&mu;<sub>mol</sub></span> = &Sigma;<sub>bonds</sub> &mu;<sub>bond</sub> &nbsp;&rarr;&nbsp; 0 <span class="hl2">whenever the bonds are symmetric</span>'
    +'<span class="sm">nineteen molecules, their computed dipole moments and the measured ones</span>';
}
function tagHTML(M){
  const v=M.view;
  if(v==='two') return '<b>&Delta;EN = '+fmt(M.m.dEN,1)+'</b> '+M.character;
  if(v==='three') return '<b>'+degs(M.bondAngleDeg)+'</b> |&mu;| = '+fmt(M.m.mumag,2);
  if(v==='real') return '<b>'+formulaHTML(M.r.sym)+'</b> '+(ST.realMode==='advanced'?fmt(M.r.psi4mag,2)+' D':M.r.name);
  if(v==='sum') return '<b>'+(M.symmetric?'cancels at 180&deg;':'min '+fmt(M.atMin,2))+'</b>';
  if(v==='field') return '<b>&zeta; = '+fmt(ST.zeta,2)+'</b> '+(ST.zeta<1?'underdamped':ST.zeta>1?'overdamped':'critical');
  return '<b>19</b> molecules, '+M.stats.n+' measured';
}
