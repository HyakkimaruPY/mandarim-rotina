import test from 'node:test';
import assert from 'node:assert/strict';
import {features,compare} from '../dist/analysis.mjs';
import {normalizePlayback} from '../dist/audio.mjs';
const sr=8000;
function signal(seconds=1,hz=170,amplitude=.4){return Float32Array.from({length:sr*seconds},(_,i)=>amplitude*Math.sin(2*Math.PI*hz*i/sr));}
test('Silence never receives a score',()=>assert.throws(()=>features(new Float32Array(sr),sr),/sinal suficiente/));
test('Identical signal has full acoustic similarity',()=>{const a=features(signal(),sr);const s=compare(a,a);assert.equal(s.total,100);});
test('Duration mismatch lowers duration similarity',()=>{const a=features(signal(),sr),b=features(signal(2),sr);assert(compare(a,b).duration<55);});
test('Different volume alone does not penalize normalized strength',()=>{const a=features(signal(),sr),b=features(signal(1,170,.1),sr);assert(compare(a,b).energy>=99);});
test('Missing pitch produces no overall score',()=>{const a=features(signal(),sr);const b={...a,voiced:0,pitch:a.pitch.map(()=>null)};assert.equal(compare(a,b).total,null);});
test('A clean voice 200 times quieter keeps its contour and score',()=>{const loud=signal(2),quiet=Float32Array.from(loud,x=>x/200);const s=compare(features(loud,sr),features(quiet,sr));assert(s.contour>=99);assert(s.total>=99);});
test('Quiet moving pitch is retained with a microphone DC offset',()=>{let phase=0;const loud=Float32Array.from({length:sr*2},(_,i)=>{phase+=2*Math.PI*(150+60*Math.sin(i/sr*4))/sr;return .2*Math.sin(phase);});const quiet=Float32Array.from(loud,x=>x/100+.025);assert(compare(features(loud,sr),features(quiet,sr)).contour>=95);});
test('Broadband noise is not certified as a clear pitch contour',()=>{let seed=123;const noise=Float32Array.from({length:sr},()=>{seed=(1664525*seed+1013904223)>>>0;return (seed/2**32-.5)*.02;});const f=features(noise,sr);assert.equal(compare(f,f).total,null);});
test('Playback normalization raises quiet audio without clipping or changing duration',async()=>{const p=normalizePlayback(signal(1,170,.002),sr);assert(p.gain>1&&p.gain<=32);const buffer=await p.blob.arrayBuffer();assert.equal(buffer.byteLength,44+sr*2);const v=new DataView(buffer);let peak=0;for(let i=44;i<buffer.byteLength;i+=2)peak=Math.max(peak,Math.abs(v.getInt16(i,true)));assert(peak>1000&&peak<32767);});
