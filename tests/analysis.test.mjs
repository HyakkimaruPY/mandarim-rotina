import test from 'node:test';
import assert from 'node:assert/strict';
import {features,compare} from '../dist/analysis.mjs';
const sr=8000;
function signal(seconds=1,hz=170,amplitude=.4){return Float32Array.from({length:sr*seconds},(_,i)=>amplitude*Math.sin(2*Math.PI*hz*i/sr));}
test('Silence never receives a score',()=>assert.throws(()=>features(new Float32Array(sr),sr),/fala clara/));
test('Identical signal has full acoustic similarity',()=>{const a=features(signal(),sr);const s=compare(a,a);assert.equal(s.total,100);});
test('Duration mismatch lowers duration similarity',()=>{const a=features(signal(),sr),b=features(signal(2),sr);assert(compare(a,b).duration<55);});
test('Different volume alone does not penalize normalized strength',()=>{const a=features(signal(),sr),b=features(signal(1,170,.1),sr);assert(compare(a,b).energy>=99);});
test('Missing pitch produces no overall score',()=>{const a=features(signal(),sr);const b={...a,voiced:0,pitch:a.pitch.map(()=>null)};assert.equal(compare(a,b).total,null);});
