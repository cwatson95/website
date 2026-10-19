
/* ================================================================== *
 *  the inline layout sweep (lineage: build_buoy/p7_test.js section I, *
 *  shared by both sims).  Every configuration at every stage size     *
 *  must draw without throwing, draw substance, keep every text op on  *
 *  the canvas and free of entities, tags, NaN and undefined, keep     *
 *  text boxes apart at tools/audit.py's own half-pixel rule, keep     *
 *  data curves out of the legends it placed, and — on a wide stage —  *
 *  keep text out from under the floating readout.                     *
 * ================================================================== */
function layoutSweep(ok,withState,configs,sizes){
  const entRe=/&#?[a-zA-Z0-9]+;|<[a-zA-Z][^>]*>/;
  for(const [nm,over,minFills] of configs) for(const [W,H] of sizes){
    withState(over,()=>{
      const c=makeShot(W,H); let err=null;
      try{ drawView(c,W,H,buildModel()); }catch(e){ err=e; }
      ok(!err,nm+' '+W+'x'+H+' draws without throwing'+(err?': '+(err.stack||err):''));
      if(err) return;
      const texts=c.ops.filter(o=>o.op==='text'), fills=c.ops.filter(o=>o.op==='fill');
      ok(fills.length>=minFills&&texts.length>=1,nm+' '+W+'x'+H+' draws substance ('+fills.length+' fills, floor '+minFills+')');
      let bad=null;
      for(const t of texts){
        if(entRe.test(t.t)){ bad='entity/tag: "'+t.t.slice(0,40)+'"'; break; }
        if(/undefined|NaN|Infinity/.test(t.t)){ bad='NaN/undefined: "'+t.t.slice(0,40)+'"'; break; }
        if(t.bb[0]<-1||t.bb[2]>W+1||t.bb[1]<-1||t.bb[3]>H+1){ bad='off-canvas: "'+t.t.slice(0,30)+'" ['+t.bb.map(v=>fmt(v,0))+']'; break; }
        if(W>=900&&t.bb[2]>W-13-280-24&&t.bb[1]<470){ bad='under the readout: "'+t.t.slice(0,30)+'"'; break; }
        /* the HTML #hint's corner (left 14, bottom 11, 11-px text up to ~330 px long) */
        if(t.bb[0]<14+330&&t.bb[3]>H-26){ bad='in the hint\'s corner: "'+t.t.slice(0,30)+'"'; break; } }
      ok(!bad,nm+' '+W+'x'+H+' text clean ('+(bad||'ok')+')');
      let hit=null;
      for(let i=0;i<texts.length&&!hit;i++) for(let j=i+1;j<texts.length;j++){
        const a=texts[i].bb, b=texts[j].bb;
        if(Math.min(a[2],b[2])-Math.max(a[0],b[0])>0.5&&Math.min(a[3],b[3])-Math.max(a[1],b[1])>0.5){
          hit='"'+texts[i].t.slice(0,24)+'" vs "'+texts[j].t.slice(0,24)+'"'; break; } }
      ok(!hit,nm+' '+W+'x'+H+' no text collisions ('+(hit||'ok')+')');
      let leg=null;
      for(const r of LEGEND_RECTS) for(let i=0;i<POLY_SEGS.length;i+=4){
        const x0=POLY_SEGS[i],y0=POLY_SEGS[i+1],x1=POLY_SEGS[i+2],y1=POLY_SEGS[i+3];
        if(Math.max(x0,x1)<r.x||Math.min(x0,x1)>r.x+r.w||Math.max(y0,y1)<r.y||Math.min(y0,y1)>r.y+r.h) continue;
        leg='a curve crosses a legend'; break; }
      ok(!leg,nm+' '+W+'x'+H+' legends clear');
    });
  }
}
