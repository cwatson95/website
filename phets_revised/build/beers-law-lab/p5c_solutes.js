
/* ================================================================== *
 *  the solutes against the literature.  Built only into               *
 *  concentration.html, which has the room for it.                     *
 * ================================================================== */
/* ---------------------------------------------------------------- the solutes -------- */
const CAP_SOLUTES='PhET’s nine solutes against the sources. The molar masses are the '
  +'literature’s to five decimal places — worst 5.6e-5 relative '
  +'— and PhET’s "drink mix" carries sucrose’s molar mass to a milligram per '
  +'mole, so it is sugar. The saturation points are within a per cent for the four whose '
  +'sources quote a room-temperature figure and further off for the rest, because the '
  +'source’s temperature is not 25 °C: the bar for cobalt(II) nitrate is a 0 '
  +'°C solubility and should be low. Every conversion assumes a litre of water makes a '
  +'litre of solution, which is the same displaced-volume assumption PhET makes.';
const CAP_SOLUTES_S='PhET’s nine solutes against Wikipedia’s infoboxes. Molar '
  +'masses match to 5.6e-5; saturations match where the source quotes room temperature.';

function viewSolutes(rc,W,H,M){
  /* nine rows will not fit under a bottom panel on a 380 px stage: at narrow widths the
     molar-mass table is dropped and the rows get the whole stage, and if even that is
     not enough the rows keep their bars and say where the numbers are */
  const U=M.U, L=layoutPanels(rc,W,H,CAP_SOLUTES,CAP_SOLUTES_S,isNarrow(W)?0:1,0.34);
  const b=L.main;
  let hi=0; for(const r of U.rows) hi=Math.max(hi,r.s.cSat,r.cLit);
  hi*=1.16;
  const n=U.rows.length;
  /* the colour roles go in the TITLE, not in a legend: at one line a row the text fills
     the panel edge to edge and a legend has nowhere to sit that is not on top of it */
  axesFit(rc,b,0,hi,0,n,{title:'saturation concentration — green: PhET, orange: the source',
    xlab:'mol/L',ylab:'',xfmt:t=>fmt(t,0),yticks:[]});
  rc.font=SM_FONT;
  /* two lines a row need about thirty pixels; below that the row carries one line with
     the numbers pushed to the right of the name instead */
  const hgt=b.h/n, twoLine=(hgt>=30), roomForText=(hgt>=15);
  U.rows.forEach((r,i)=>{
    /* PhET's own order, first at the top */
    const y0=b.y+b.h*i/n;
    const wP=b.w*clamp(r.s.cSat/hi,0,1), wL=b.w*clamp(r.cLit/hi,0,1);
    /* the text gets the top of the row and the two bars the bottom of it: painted on the
       bars, a green label on a green bar cannot be read */
    const barTop=twoLine?0.50:0.58;
    rc.fillStyle=r.s.id===U.here?COL.pos:shade(COL.pos,0.55);
    rc.fillRect(b.x,y0+hgt*barTop,wP,hgt*0.19);
    rc.fillStyle=COL.ref;
    rc.fillRect(b.x,y0+hgt*(barTop+0.22),wL,hgt*0.19);
    if(!roomForText) return;
    const nameTxt=plain(r.s.name)+'  ('+plain(r.s.formula)+')';
    const numTxt=fmt(r.s.cSat,2)+' vs '+fmt(r.cLit,2)+' mol/L  —  '
                +(r.dC>=0?'+':'')+fmt(100*r.dC,1)+' %   ['+plain(r.s.lit.temp)+']';
    rc.textBaseline='middle'; rc.textAlign='left';
    rc.fillStyle=r.s.id===U.here?COL.pos:COL.dim;
    rc.fillText(nameTxt,b.x+6,y0+hgt*0.22);
    rc.fillStyle=Math.abs(r.dC)>0.1?COL.ref:COL.dim;
    if(twoLine){ rc.textAlign='right'; rc.fillText(numTxt,b.x1-6,y0+hgt*0.22); }
    else { rc.textAlign='right'; rc.fillText(numTxt,b.x1-6,y0+hgt*0.22); }
  });
  if(!roomForText)
    lab(rc,W,H,b.x+6,b.y+12,'nine bars a row, PhET’s order top to bottom; the numbers '
        +'are in the readout',COL.dim,SM_FONT,'left','middle');
  if(L.bottom[0]){
    const p=L.bottom[0];
    frame(rc,p,'#242a3a');
    lab(rc,W,H,p.x,p.y-11,'molar mass, and what the original says',COL.dim,
        'italic 13px Georgia, serif','left','bottom');
    /* as many columns as the panel can hold at 150 px a column, laid out from what it
       HAS rather than from three columns that fit only at 1400 px */
    rc.font=SM_FONT; rc.textBaseline='middle';
    /* as many rows as the panel is tall enough for, then as few columns as that needs */
    const perCol=clamp(Math.floor((p.h-18)/16),1,9), nCol=Math.ceil(9/perCol);
    const colW=(p.w-16)/nCol;
    U.rows.forEach((r,i)=>{
      const cx=p.x+8+colW*Math.floor(i/perCol), cy=p.y+16+(i%perCol)*16;
      if(cy>p.y1-6) return;
      rc.textAlign='left'; rc.fillStyle=r.s.id===U.here?COL.pos:COL.dim;
      const nm=plain(r.s.formula);
      rc.fillText(nm,cx,cy);
      /* both masses, one mass, or none, depending on what the column can hold: measured,
         because a fixed column width is right at exactly one stage size */
      let num=fmt(r.s.molarMass,3)+'/'+fmt(r.s.lit.M,3);
      const room=colW-20-rc.measureText(nm).width;
      if(rc.measureText(num).width>room) num=fmt(r.s.molarMass,3);
      if(rc.measureText(num).width>room) num='';
      if(num){ rc.textAlign='right'; rc.fillStyle=COL.dim;
               rc.fillText(num,cx+colW-14,cy); }
    });
    lab(rc,W,H,p.x1-6,p.y-11,'g/mol, PhET / source',COL.dim,SM_FONT,'right','bottom');
  }
  drawCaption(rc,{left:L.left,capY:L.capY,capTxt:L.capTxt,capW:L.capW});
}

