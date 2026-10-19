
/* ================================================================== *
 *  the one view ph-scale-basics carries and ph-scale does not:        *
 *  THE LIQUIDS — PhET's twelve as a table, with what dilution does    *
 *  to each of them and which of them carry a measured range           *
 * ================================================================== */
const CAP_LIQ='PhET’s twelve liquids, their pH values, and what a full beaker of water does to each of them. The last two columns are the same pour — 0.1 L of the liquid, topped up to the beaker’s 1.2 L — worked out two ways: by mixing moles of net strong acid and re-solving the water equilibrium, and by PhET’s own rule. They agree to a hundredth of a unit for most of the list and part company by 0.08 for chicken soup, which sits near the pH where the gap is largest. Notice how little twelve-fold dilution moves anything: pH is a logarithm, so a twelvefold cut in the acid is 1.08 units and no more. The measured column is a real range with a source where one could be found, and empty where one could not.';
const CAP_LIQ_S='PhET’s twelve, and what a full beaker of water does to each. Twelvefold dilution is only 1.08 pH.';
function viewLiquids(rc,W,H,M){
  const L=M.L;
  const narrow=isNarrow(W);
  const left=56, right=narrow?W-26:W-RO_W-44;
  const top=stageTop()+30;
  const capW=Math.max(260,Math.min(W-148,right-left));
  const fit=fitCaption(rc,W,H-HINT_H,CAP_LIQ,CAP_LIQ_S,capW,top+200);
  const availH=Math.max(160,fit.capY-24-top);
  const T=box(left,top+24,right-left,availH-24);

  /* the two right-hand headers are short on purpose: "0.1 L in 1.2 L" and "by PhET's
     rule" are 76 px each in an 84 px column at 1100 x 700 and collided */
  const cols=narrow
    ? ['liquid','PhET pH','measured','diluted 12x']
    : ['liquid','PhET pH','acid or base','measured range','source','diluted 12x','PhET’s rule'];
  const n=cols.length;
  /* the name column is wide, the rest share what is left: a source line is a sentence and
     an equal split ran it into the column beside it */
  const wFrac=narrow?[0.30,0.18,0.24,0.28]:[0.15,0.08,0.11,0.12,0.28,0.13,0.13];
  const colX=[], colW=[];
  { let x=T.x+6;
    for(let i=0;i<n;i++){ colW.push((T.w-12)*wFrac[i]); colX.push(x); x+=colW[i]; } }
  const xOf=i=>i===0?colX[i]:colX[i]+colW[i]-8;

  rc.font='italic 13px Georgia, serif'; rc.fillStyle='#aeb6c6';
  rc.textAlign='left'; rc.textBaseline='bottom';
  /* the long title is 649 px and ran off a 560 px stage */
  rc.fillText(plain(narrow?'PhET’s twelve liquids'
    :'PhET’s twelve liquids — the left columns are PhET’s, the right two are this file’s solve of them'),
              T.x,T.y-8);
  rc.font=SM_FONT; rc.textBaseline='top';
  for(let i=0;i<n;i++){
    rc.textAlign=i?'right':'left'; rc.fillStyle='#6f7789';
    rc.fillText(plain(cols[i]),xOf(i),T.y+2);
  }
  rc.beginPath(); rc.moveTo(T.x,T.y+19); rc.lineTo(T.x1,T.y+19);
  rc.strokeStyle='#242a3a'; rc.lineWidth=1; rc.stroke();
  /* let the twelve rows fill the panel: capped at 26 the table used a third of the stage
     and left the rest of a 1400 x 820 picture empty */
  const rowH=Math.max(15,Math.min(40,(T.h-56)/SOLUTES.length));
  const rows=L.rows.slice().sort((a,b)=>a.s.pH-b.s.pH);
  rows.forEach((r,k)=>{
    const y=T.y+24+k*rowH;
    const on=r.s.id===ST.solute;
    const ex=mixExact(r.s.pH,0.1,PHET.WATER_PH,1.1), ph=mixPhet(r.s.pH,0.1,1.1);
    const meas=r.s.range
      ? (r.s.range[0]===r.s.range[1]?fmt(r.s.range[0],2)
         :fmt(r.s.range[0],2)+'–'+fmt(r.s.range[1],2))
      : 'not sourced';
    const src=r.s.src?plain(r.s.src).replace(/,.*$/,''):'—';
    const vals=narrow
      ? [plain(r.s.name),fmt(r.s.pH,2),meas,phPlain(ex)]
      : [plain(r.s.name),fmt(r.s.pH,2),CLS_NAME[phClass(r.s.pH)],meas,src,
         phPlain(ex),phPlain(ph)];
    /* the selected row gets a band, not just a colour: the chip changed nothing the
       display-list capture could see, so "picking another liquid redraws the table" was
       failing on a view that really did only change ink */
    if(on){
      rc.fillStyle='rgba(184,236,76,.10)';
      rc.fillRect(T.x-1,y-3,T.w+2,Math.max(10,rowH));
    }
    /* a swatch of the liquid's own colour, so the table and the beaker agree */
    rc.fillStyle=rgbCss(r.s.stock);
    rc.fillRect(T.x-1,y+2,4,Math.max(6,rowH-6));
    /* the columns are coloured by ROLE, named explicitly: green is the exact solve,
       orange the measured range and PhET's own rule, dim the ones with no source.  A
       "last two are green" shortcut painted the narrow layout's measured column green,
       which said the opposite of what it meant. */
    const iMeas=narrow?2:3, iExact=narrow?3:5, iPhet=narrow?-1:6;
    for(let i=0;i<n;i++){
      rc.textAlign=i?'right':'left';
      if(i===0) rc.fillStyle=on?COL.pos:'#aeb6c6';
      else if(i===iExact) rc.fillStyle=COL.pos;
      else if(i===iPhet) rc.fillStyle=COL.ref;
      else if(i===iMeas) rc.fillStyle=r.s.range?COL.ref:'#5c6577';
      else rc.fillStyle=on?'#cfd4de':'#8b93a6';
      rc.fillText(plain(vals[i]),xOf(i),y);
    }
  });
  /* the one line worth taking away */
  const foot=T.y+24+SOLUTES.length*rowH+10;
  if(foot+16<fit.capY)
    lab(rc,W,H,T.x,foot,narrow
        ?'green: moles of net strong acid, re-solved with Kw'
        :'the green column mixes MOLES of net strong acid and re-solves with Kw; '
         +'the orange one is PhET’s rule, and the two differ by at most 0.08 pH here',
        '#767e92',SM_FONT,'left','top');
  caption(rc,left,fit.capY,fit.txt,capW,'#767e92',CAP_FONT);
}
