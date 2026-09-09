// Playback uses one constant gain, preserving relative emphasis and pitch.
export function normalizePlayback(samples,sampleRate){
  let mean=0;for(const x of samples)mean+=x;mean/=samples.length||1;
  let peak=0;for(const x of samples)peak=Math.max(peak,Math.abs(x-mean));
  const gain=peak>.00001?Math.min(32,.82/peak):1;
  const bytes=new ArrayBuffer(44+samples.length*2),v=new DataView(bytes);
  const str=(offset,s)=>{for(let i=0;i<s.length;i++)v.setUint8(offset+i,s.charCodeAt(i));};
  str(0,'RIFF');v.setUint32(4,bytes.byteLength-8,true);str(8,'WAVE');str(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,sampleRate,true);v.setUint32(28,sampleRate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);str(36,'data');v.setUint32(40,samples.length*2,true);
  for(let i=0;i<samples.length;i++)v.setInt16(44+i*2,Math.round(Math.max(-1,Math.min(1,(samples[i]-mean)*gain))*32767),true);
  return {blob:new Blob([bytes],{type:'audio/wav'}),gain,peak};
}
export function mono(buffer){
  if(buffer.numberOfChannels===1)return buffer.getChannelData(0);
  const result=new Float32Array(buffer.length);
  for(let c=0;c<buffer.numberOfChannels;c++){const channel=buffer.getChannelData(c);for(let i=0;i<result.length;i++)result[i]+=channel[i]/buffer.numberOfChannels;}
  return result;
}
