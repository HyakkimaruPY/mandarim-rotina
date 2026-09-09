// State-level integration: no microphone permission, browser or network is used.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
class Element {
  constructor(){this.children=[];this.listeners={};this.hidden=false;this.value=0;this.open=false;this.classList={add(){},remove(){}};}
  append(...nodes){this.children.push(...nodes);}
  replaceChildren(...nodes){this.children=nodes;}
  setAttribute(k,v){this[k]=v;}
  removeAttribute(k){delete this[k];}
  addEventListener(k,f){(this.listeners[k]??=[]).push(f);}
  pause(){} load(){} focus(){}
}
const turn=()=>new Promise(r=>setImmediate(r));
test('Late microphone permission, navigation, rerecording and page exit discard audio',async()=>{
  const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,new Element());return nodes.get(id);};
  const windowEvents={};
  globalThis.document={getElementById:get,createElement:()=>new Element(),addEventListener(){}};
  globalThis.window={addEventListener:(n,f)=>windowEvents[n]=f};
  const storage=new Map();globalThis.localStorage={getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)};
  const content=JSON.parse(await readFile(new URL('../dist/content.json',import.meta.url),'utf8'));
  globalThis.fetch=async()=>({ok:true,json:async()=>content});
  let resolvePermission,stops=0,instances=0,activeURLs=new Set();
  const media={getUserMedia:()=>new Promise(r=>resolvePermission=r)};
  Object.defineProperty(globalThis,'navigator',{value:{mediaDevices:media},configurable:true});
  const newStream=()=>{const t={stop(){stops++;}};return {getTracks:()=>[t],getAudioTracks:()=>[t]};};
  class Recorder {
    static isTypeSupported(){return true;}
    constructor(){this.state='inactive';this.mimeType='audio/webm';instances++;}
    start(){this.state='recording';}
    stop(){this.state='inactive';this.ondataavailable?.({data:new Blob(['x'.repeat(300)])});this.onstop?.();}
  }
  window.MediaRecorder=Recorder;globalThis.MediaRecorder=Recorder;
  const originalCreate=URL.createObjectURL,originalRevoke=URL.revokeObjectURL;
  URL.createObjectURL=()=>{const url=`blob:test-${Math.random()}`;activeURLs.add(url);return url;};
  URL.revokeObjectURL=url=>activeURLs.delete(url);
  try{
    await import('../dist/app.mjs');await turn();
    assert.equal(get('sentence').textContent,content.islands[0].phrases[0].zh);
    get('complete').onclick();get('complete').onclick();
    assert.equal(JSON.parse(storage.get('mandarim-rotina:v1')).reviews['rotina-01'],1,'Double click cannot duplicate a review');
    const delayed=get('record').onclick();get('next').onclick();resolvePermission(newStream());await delayed;
    assert.equal(stops,1,'Late permission immediately closes its stream');assert.equal(instances,0);
    media.getUserMedia=async()=>newStream();await get('record').onclick();assert.equal(instances,1);
    get('stop').onclick();await turn();assert.equal(activeURLs.size,1);assert.equal(get('mine').hidden,false);
    assert(!storage.get('mandarim-rotina:v1').includes('blob:'),'Storage contains no recording');
    get('next').onclick();assert.equal(activeURLs.size,0);assert.equal(get('mine').hidden,true);
    await get('record').onclick();get('stop').onclick();await turn();assert.equal(activeURLs.size,1);
    await get('record').onclick();assert.equal(activeURLs.size,0,'Rerecord immediately revokes previous audio');
    windowEvents.pagehide();assert.equal(activeURLs.size,0);assert.equal(get('stop').disabled,true);
    assert.equal(JSON.parse(storage.get('mandarim-rotina:v1')).positions.rotina,2);
  }finally{URL.createObjectURL=originalCreate;URL.revokeObjectURL=originalRevoke;windowEvents.pagehide?.();}
});
