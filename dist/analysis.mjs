// Acoustic resemblance only: no word recognition, phoneme alignment or tone grading.
export const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n));
function median(a){if(!a.length)return 0;const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)];}
function pitch(frame,sr){
  let mean=0;for(const n of frame)mean+=n;mean/=frame.length;
  let best=0,bestLag=0;
  for(let lag=Math.floor(sr/500);lag<=Math.ceil(sr/70);lag++){
    let cross=0,a=0,b=0;
    for(let i=0;i<frame.length-lag;i++){const x=frame[i]-mean,y=frame[i+lag]-mean;cross+=x*y;a+=x*x;b+=y*y;}
    const v=cross/Math.sqrt(a*b+1e-14);
    if(v>best){best=v;bestLag=lag;}
    // Prefer the first strong peak to reduce octave errors.
    if(best>.91&&v<best-.015)break;
  }
  return best>.65?sr/bestLag:0;
}
export function features(samples,sampleRate){
  // 8 kHz is enough for this 70–500 Hz contour estimate. Averaging reduces aliasing.
  const factor=Math.max(1,Math.floor(sampleRate/8000)),sr=sampleRate/factor;
  const x=new Float32Array(Math.floor(samples.length/factor));
  let clipped=0;for(let i=0;i<samples.length;i++)if(Math.abs(samples[i])>.985)clipped++;
  for(let i=0;i<x.length;i++){let s=0;for(let j=0;j<factor;j++)s+=samples[i*factor+j];x[i]=s/factor;}
  const hop=Math.round(sr*.02),win=Math.round(sr*.04),rms=[],f0=[];
  for(let i=0;i+win<=x.length;i+=hop){let e=0;for(let k=i;k<i+win;k++)e+=x[k]*x[k];rms.push(Math.sqrt(e/win));}
  const peak=Math.max(0,...rms),threshold=Math.max(.004,peak*.09);
  const start=rms.findIndex(v=>v>threshold),end=rms.findLastIndex(v=>v>threshold);
  if(start<0||end-start<8||peak<.009)throw Error('Não encontrei uma fala clara. Aproxime o microfone e tente novamente.');
  for(let k=start;k<=end;k++)f0.push(rms[k]>threshold?pitch(x.subarray(k*hop,k*hop+win),sr):0);
  const voiced=f0.filter(Boolean),baseline=median(voiced);
  return {duration:(end-start+2)*.02,energy:rms.slice(start,end+1).map(v=>v/peak),pitch:f0.map(v=>v?12*Math.log2(v/baseline):null),voiced:voiced.length/f0.length,clipping:clipped/samples.length};
}
function resample(a,n=64){return Array.from({length:n},(_,i)=>{const p=i*(a.length-1)/(n-1),l=Math.floor(p),r=Math.min(l+1,a.length-1);if(a[l]===null||a[r]===null)return null;return a[l]+(a[r]-a[l])*(p-l);});}
export function compare(a,b){
  const duration=clamp(Math.min(a.duration,b.duration)/Math.max(a.duration,b.duration));
  const ea=resample(a.energy),eb=resample(b.energy),energy=clamp(1-ea.reduce((s,v,i)=>s+Math.abs(v-eb[i]),0)/ea.length);
  const pa=resample(a.pitch),pb=resample(b.pitch);let error=0,count=0;
  for(let i=0;i<pa.length;i++)if(pa[i]!==null&&pb[i]!==null){error+=Math.min(Math.abs(pa[i]-pb[i]),12);count++;}
  const contour=count>=18&&a.voiced>.25&&b.voiced>.25?clamp(1-error/count/8):null;
  const total=contour===null?null:Math.round(100*(.2*duration+.4*energy+.4*contour));
  return {total,duration:Math.round(duration*100),energy:Math.round(energy*100),contour:contour===null?null:Math.round(contour*100),referenceDuration:a.duration,userDuration:b.duration,clipping:b.clipping};
}
