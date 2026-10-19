/* list every text collision and every off-canvas box, per view and size */
(function(){
  const SIZES=[[1400,820],[1100,700],[900,560],[700,470],[560,380]];
  const seen={};
  for(const [W,H] of SIZES){
    for(const [v] of TABS){
      ST.view=v;
      BK=makeBeaker(ST.solute,1.4,0.6);
      const rc=makeShot(W,H);
      drawView(rc,W,H,buildModel());
      const texts=rc.ops.filter(o=>o.op==='text');
      for(let i=0;i<texts.length;i++) for(let j=i+1;j<texts.length;j++){
        const a=texts[i].bb, b=texts[j].bb;
        if(a[0]<b[2]-0.5&&a[2]>b[0]+0.5&&a[1]<b[3]-0.5&&a[3]>b[1]+0.5){
          const k=v+' | '+String(texts[i].t).slice(0,34)+' || '+String(texts[j].t).slice(0,34);
          seen[k]=(seen[k]||0)+1;
        }
      }
      for(const t of texts)
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1)
          console.log('OFF  '+v+' '+W+'x'+H+' "'+String(t.t).slice(0,40)+'" bb='
                      +t.bb.map(x=>Math.round(x)).join(','));
    }
  }
  const keys=Object.keys(seen).sort();
  console.log('DISTINCT COLLISIONS: '+keys.length);
  for(const k of keys) console.log('  x'+seen[k]+'  '+k);
})();
