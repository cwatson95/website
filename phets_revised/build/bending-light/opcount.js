/* diagnostic: how many fills/strokes/texts each sweep configuration emits */
const SIZES=[[1180,740],[1400,820],[900,600],[560,380]];
const SWEEP=[
  ['bound default',{view:'bound'}],
  ['bound TIR',{view:'bound',topSub:'water',botSub:'air',angDeg:70}],
  ['bound white',{view:'bound',white:true,showProtractor:true}],
  ['bound normal incidence',{view:'bound',angDeg:0,showAngles:true}],
  ['bound laser off',{view:'bound',laserOn:false}],
  ['wave default',{view:'wave'}],
  ['wave TIR',{view:'wave',topSub:'glass',botSub:'air',angDeg:60}],
  ['wave no field',{view:'wave',paintField:false}],
  ['prism triangle',{view:'prism'}],
  ['prism white',{view:'prism',white:true,manyRays:true}],
  ['prism diamond',{view:'prism',prismSub:'diamond',showReflections:true}],
  ['prism circle',{view:'prism',prismId:'circle',showNormals:true}],
  ['prism semicircle',{view:'prism',prismId:'semicircle',prismRot:35}],
  ['fres default',{view:'fres'}],
  ['fres TIR pair',{view:'fres',topSub:'glass',botSub:'air'}],
  ['spec default',{view:'spec'}],
  ['spec steep prism',{view:'spec',prismApex:75,prismSub:'diamond'}],
  ['bow primary',{view:'bow'}],
  ['bow secondary',{view:'bow',bowK:2,white:true}],
];
for(const [nm,over] of SWEEP){
  const line=[];
  for(const [W,H] of SIZES){
    const keep=Object.assign({},ST);
    Object.assign(ST,DEFAULTS,over); clearMemo();
    const c=makeShot(W,H);
    drawView(c,W,H,buildModel(ST),ST);
    const f=c.ops.filter(o=>o.op==='fill').length;
    const s=c.ops.filter(o=>o.op==='stroke').length;
    const t=c.ops.filter(o=>o.op==='text').length;
    line.push(W+'x'+H+': '+(f+s)+' draw ('+f+'f/'+s+'s), '+t+' texts');
    Object.assign(ST,keep); clearMemo();
  }
  console.log(nm.padEnd(24)+' | '+line.join(' | '));
}
