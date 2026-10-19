/* capture_tail_blackbody-spectrum.js — display-list capture for blackbody-spectrum.html.
 * cat _out/run.js <sim>/tools/recorder.js capture_tail_blackbody-spectrum.js > _out/cap_run.js
 * cd _out && osascript -l JavaScript cap_run.js > cap.log      (never through head/tail) */
const CAPW=(typeof CAP_W!=='undefined')?CAP_W:1400, CAPH=(typeof CAP_H!=='undefined')?CAP_H:820;
const out={W:CAPW,H:CAPH,views:{}};
const SCENES=[
  ['spec_default',      {view:'spec'},null],
  ['spec_all_on',       {view:'spec',gv:true,labels:true,inten:true,gvNm:1500},[3000,9950]],
  ['spec_earth',        {view:'spec',T:250},null],
  ['spec_earth_fitted', {view:'spec',T:250,ix:6,iy:1,gv:true,labels:true,inten:true},[200]],
  ['spec_sirius_750',   {view:'spec',T:9950,ix:0,labels:true,gv:true},null],
  ['spec_bulb_fitted',  {view:'spec',T:3000,ix:3,iy:8,labels:true,inten:true,gv:true,gvNm:2000},[5800]],
  ['spec_11000_top',    {view:'spec',T:11000,iy:0,labels:true},null],
  ['star_sun',          {view:'star'},null],
  ['star_200',          {view:'star',T:200},null],
  ['star_800',          {view:'star',T:800},null],
  ['star_3000',         {view:'star',T:3000},null],
  ['star_11000',        {view:'star',T:11000},null],
  ['peak_sun',          {view:'peak'},null],
  ['peak_200',          {view:'peak',T:200},null],
  ['total_sun',         {view:'total'},null],
  ['total_11000',       {view:'total',T:11000},null],
  ['limits_sun',        {view:'limits'},null],
  ['limits_200',        {view:'limits',T:200},null],
  ['limits_none',       {view:'limits',rj:false,wien:false},null],
];
for(const [name,over,saved] of SCENES){
  Object.assign(ST,DEFAULTS,over); ST.gvNm=over.gvNm!==undefined?over.gvNm:peakNm(ST.T);
  SAVED.length=0; if(saved) for(const T of saved) SAVED.push(T);
  const rc=makeRecorder(CAPW,CAPH);
  drawView(rc,CAPW,CAPH,buildModel());
  out.views[name]=rc.ops;
  console.log(name+': '+rc.ops.length+' ops');
}
Object.assign(ST,DEFAULTS); SAVED.length=0;
ObjC.import('Foundation');
const json=JSON.stringify(out);
$.NSString.alloc.initWithUTF8String(json)
  .writeToFileAtomicallyEncodingError('display.json', true, $.NSUTF8StringEncoding, $());
console.log('wrote display.json, '+json.length+' bytes');
