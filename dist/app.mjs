import {features,compare} from './analysis.mjs?v=2';
import {normalizePlayback,mono} from './audio.mjs?v=2';
const $=id=>document.getElementById(id),KEY='mandarim-rotina:v1';
let data,state,island,phrase,epoch=0,recorder=null,stream=null,chunks=[],objectURL=null,clock=null,limit=null,ctx=null,captureCtx=null,sourceNode=null,levelClock=null,abort=null,reviewLocked=false,pending=false;
const reference=$('reference'),mine=$('mine');
const audioURL=p=>p.audio+'?v='+encodeURIComponent(p.audioVersion||'1');
function initial(){return {version:1,island:'rotina',positions:{},reviews:{},preferences:{pinyin:false,meaning:false},lastReviewed:null};}
function readState(){
  try{const s=JSON.parse(localStorage.getItem(KEY));if(!s||s.version!==1)return initial();
    const base=initial();if(data.islands.some(i=>i.id===s.island))base.island=s.island;
    for(const i of data.islands){const p=s.positions?.[i.id];if(Number.isInteger(p)&&p>=0&&p<i.phrases.length)base.positions[i.id]=p;
      for(const f of i.phrases){const n=s.reviews?.[f.id];if(Number.isSafeInteger(n)&&n>=0)base.reviews[f.id]=n;}}
    base.preferences={pinyin:s.preferences?.pinyin===true,meaning:s.preferences?.meaning===true};
    if(typeof s.lastReviewed==='string')base.lastReviewed=s.lastReviewed;return base;
  }catch{$('storage-warning').hidden=false;return initial();}
}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch{$('storage-warning').hidden=false;}}
const count=f=>state.reviews[f.id]||0;
const done=i=>i.phrases.filter(f=>count(f)>0).length;
function el(tag,text,className){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(className)n.className=className;return n;}
function showNavigation(){
  $('islands').replaceChildren();data.islands.forEach((i,index)=>{const b=el('button',undefined,'island-button');b.setAttribute('aria-current',String(i.id===island.id));b.append(el('span',String(index+1).padStart(2,'0'),'number'));const label=el('span');label.append(el('strong',i.title),el('small',`${done(i)} / ${i.phrases.length} frases percorridas`));b.append(label);b.onclick=()=>select(i.id,state.positions[i.id]||0,true);$('islands').append(b);});
  $('total-done').textContent=`${data.islands.filter(i=>done(i)===i.phrases.length).length} / ${data.islands.length} ilhas`;
}
function showProgress(){
  const visited=done(island),reviews=island.phrases.reduce((s,f)=>s+count(f),0),rounds=Math.min(...island.phrases.map(count));
  $('island-progress').max=island.phrases.length;$('island-progress').value=visited;
  $('island-progress-text').textContent=`${visited} de ${island.phrases.length} frases percorridas`;
  $('island-reviews').textContent=`${reviews} revisões · ${rounds} voltas completas`;
  $('phrase-reviews').textContent=`Esta frase: ${count(phrase)} ${count(phrase)===1?'revisão':'revisões'}`;
  showNavigation();
}
function resetComparison(){$('comparison').hidden=true;$('comparison-result').replaceChildren(el('p','Depois de gravar, compare o ritmo, a força relativa da voz e o desenho da entonação.','muted'));}
function dispose(){
  epoch++;pending=false;stopMeter();abort?.abort();abort=null;
  clearInterval(clock);clearTimeout(limit);clock=null;limit=null;
  if(recorder){recorder.ondataavailable=null;recorder.onstop=null;recorder.onerror=null;if(recorder.state!=='inactive')recorder.stop();recorder=null;}
  stream?.getTracks().forEach(t=>t.stop());stream=null;chunks=[];
  reference.pause();mine.pause();mine.removeAttribute('src');mine.load();mine.hidden=true;
  if(objectURL)URL.revokeObjectURL(objectURL);objectURL=null;
  if(ctx){ctx.close().catch(()=>{});ctx=null;}
  $('record').disabled=false;$('stop').disabled=true;$('record').classList.remove('recording-active');$('record').innerHTML='<span aria-hidden="true">●</span> Gravar';$('timer').textContent='0:00';$('rec-indicator').textContent='';
  resetComparison();
}
function phraseList(){
  const list=$('phrase-list');list.replaceChildren();let last='',group;
  island.phrases.forEach((p,i)=>{if(p.scene!==last){group=el('section',undefined,'scene-group');group.append(el('h3',p.scene));list.append(group);last=p.scene;}
    const b=el('button',undefined,'phrase-link');b.setAttribute('aria-current',String(p.id===phrase.id));const text=el('span',`${String(i+1).padStart(2,'0')} · ${p.zh}`);text.lang='zh-CN';b.append(text,el('small',`${count(p)} revisões`));b.onclick=()=>select(island.id,i,true);group.append(b);});
}
function select(id,index,focus=false){
  dispose();island=data.islands.find(i=>i.id===id)||data.islands[0];index=Math.min(Math.max(index,0),island.phrases.length-1);phrase=island.phrases[index];state.island=island.id;state.positions[island.id]=index;save();reviewLocked=false;
  $('complete').disabled=false;$('complete').textContent='Concluir revisão';
  $('catalog-count').textContent=`${data.islands.length} ilhas · ${data.islands.reduce((n,i)=>n+i.phrases.length,0)} frases`;
  $('island-no').textContent=`ILHA ${String(data.islands.indexOf(island)+1).padStart(2,'0')} / ${String(data.islands.length).padStart(2,'0')}`;
  $('island-title').textContent=island.title;$('island-description').textContent=island.description;$('island-zh').textContent=island.zh;
  $('sentence').textContent=phrase.zh;$('scene').textContent=phrase.scene;$('phrase-number').textContent=`${index+1} / ${island.phrases.length}`;
  $('cue').textContent=`${phrase.register} · ${phrase.cue}`;$('pinyin').textContent=phrase.pinyin;$('translation').textContent=phrase.pt;$('structure').textContent=phrase.note;
  $('pinyin-details').open=state.preferences.pinyin;$('meaning-details').open=state.preferences.meaning;
  reference.src=audioURL(phrase);reference.playbackRate=1;reference.load();$('ref-status').textContent='';$('rec-status').textContent='';
  $('phrase-select').replaceChildren(...island.phrases.map((f,j)=>{const opt=el('option',`${String(j+1).padStart(2,'0')} · ${f.zh}`);opt.value=j;return opt;}));$('phrase-select').value=index;
  $('previous').disabled=index===0;$('next').disabled=index===island.phrases.length-1;
  showProgress();phraseList();if(focus)$('sentence').focus({preventScroll:false});
}
function unlockReview(){reviewLocked=false;$('complete').disabled=false;$('complete').textContent='Concluir revisão';}
function stopMeter(){clearInterval(levelClock);levelClock=null;sourceNode?.disconnect();sourceNode=null;if(captureCtx){captureCtx.close().catch(()=>{});captureCtx=null;}$('input-level').hidden=true;}
function startMeter(activeStream,ticket){const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;try{captureCtx=new AC();captureCtx.resume().catch(()=>{});const analyser=captureCtx.createAnalyser();analyser.fftSize=1024;sourceNode=captureCtx.createMediaStreamSource(activeStream);sourceNode.connect(analyser);const samples=new Float32Array(analyser.fftSize);$('input-level').hidden=false;levelClock=setInterval(()=>{if(ticket!==epoch)return;analyser.getFloatTimeDomainData(samples);const rms=Math.sqrt(samples.reduce((s,x)=>s+x*x,0)/samples.length);const db=20*Math.log10(Math.max(rms,.000001));$('level-meter').value=Math.max(0,Math.min(100,(db+65)/60*100));$('level-text').textContent=db<-50?'Voz baixa — aproxime o microfone':db>-6?'Muito forte — afaste um pouco':'Microfone recebendo sua voz';},180);}catch{stopMeter();}}
function stop(){if(recorder&&recorder.state==='recording'){stopMeter();recorder.stop();stream?.getTracks().forEach(t=>t.stop());clearInterval(clock);clearTimeout(limit);$('stop').disabled=true;$('record').classList.remove('recording-active');$('rec-indicator').textContent='';$('rec-status').textContent='Preparando sua gravação…';}}
async function startRecording(){
  dispose();unlockReview();const ticket=epoch,refPath=audioURL(phrase);
  if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){$('rec-status').textContent='Este navegador não oferece gravação. Abra a página HTTPS no Chrome, Firefox ou Safari atualizado.';return;}
  pending=true;$('record').disabled=true;$('rec-status').textContent='Autorize o microfone no navegador para começar.';
  let localStream,localRecorder;
  try{
    localStream=await navigator.mediaDevices.getUserMedia({audio:{channelCount:{ideal:1},echoCancellation:{ideal:false},noiseSuppression:{ideal:false},autoGainControl:{ideal:true}}});
    if(ticket!==epoch){localStream.getTracks().forEach(t=>t.stop());return;}
    pending=false;stream=localStream;
    const type=['audio/webm;codecs=opus','audio/mp4','audio/ogg;codecs=opus'].find(t=>MediaRecorder.isTypeSupported(t));
    localRecorder=new MediaRecorder(stream,type?{mimeType:type}:{});recorder=localRecorder;chunks=[];
    const mime=localRecorder.mimeType;
    localRecorder.ondataavailable=e=>{if(ticket===epoch&&e.data.size)chunks.push(e.data);};
    localRecorder.onerror=()=>{if(ticket===epoch){dispose();$('rec-status').textContent='A gravação foi interrompida. Tente novamente.';}};
    localRecorder.onstop=async()=>{
      if(ticket!==epoch)return;stopMeter();stream?.getTracks().forEach(t=>t.stop());stream=null;recorder=null;clearInterval(clock);clearTimeout(limit);
      const blob=new Blob(chunks,{type:mime});chunks=[];
      $('record').disabled=false;$('record').innerHTML='<span aria-hidden="true">●</span> Gravar de novo';
      if(blob.size<100){$('rec-status').textContent='A gravação ficou vazia. Tente novamente.';return;}
      objectURL=URL.createObjectURL(blob);mine.src=objectURL;mine.hidden=false;mine.load();$('rec-status').textContent='Gravação pronta. Ouça, pause e compare com a referência.';
      await analyze(blob,refPath,ticket);
    };
    localRecorder.start(200);startMeter(stream,ticket);$('stop').disabled=false;$('record').classList.add('recording-active');$('rec-indicator').textContent='GRAVANDO';$('rec-status').textContent='Gravando. Toque em Parar quando terminar (limite: 30 segundos).';
    const started=Date.now();clock=setInterval(()=>{$('timer').textContent=`0:${String(Math.min(30,Math.floor((Date.now()-started)/1000))).padStart(2,'0')}`;},200);limit=setTimeout(stop,30000);
    for(const track of stream.getAudioTracks())track.onended=()=>{if(ticket===epoch)stop();};
  }catch(e){localStream?.getTracks().forEach(t=>t.stop());if(ticket!==epoch)return;pending=false;stream=null;recorder=null;$('record').disabled=false;$('stop').disabled=true;$('rec-status').textContent=e.name==='NotAllowedError'?'Microfone não autorizado. Ative a permissão nas configurações deste site e tente novamente.':e.name==='NotFoundError'?'Não encontrei um microfone neste aparelho.':'Não foi possível iniciar o microfone. Feche outros gravadores e tente novamente.';}
}
async function analyze(blob,path,ticket){
  $('comparison').hidden=false;const result=$('comparison-result');result.replaceChildren(el('p','Comparando os sinais neste aparelho…','muted'));
  try{
    const AudioContext=window.AudioContext||window.webkitAudioContext;if(!AudioContext)throw Error('A comparação acústica não está disponível neste navegador. Você ainda pode comparar pelo ouvido.');
    ctx=new AudioContext();const currentContext=ctx;abort=new AbortController();const signal=abort.signal;
    const recordingBytes=await blob.arrayBuffer();
    const b=await currentContext.decodeAudioData(recordingBytes);if(ticket!==epoch)return;
    const userSamples=mono(b),normalized=normalizePlayback(userSamples,b.sampleRate);
    // Replace playback even if the reference cannot be fetched or the pitch is unreliable.
    mine.pause();if(objectURL)URL.revokeObjectURL(objectURL);objectURL=URL.createObjectURL(normalized.blob);mine.src=objectURL;mine.load();
    $('rec-status').textContent=normalized.gain>1.2?'Volume ajustado para ouvir melhor.':'Pronto para ouvir.';
    const response=await fetch(path,{signal});if(!response.ok)throw Error('Não consegui carregar a referência. Sua gravação já pode ser ouvida.');
    const a=await currentContext.decodeAudioData(await response.arrayBuffer());if(ticket!==epoch)return;
    const fa=features(mono(a),a.sampleRate),fb=features(userSamples,b.sampleRate);const score=compare(fa,fb);if(ticket!==epoch)return;
    displayScore(score);await currentContext.close();if(ctx===currentContext)ctx=null;
  }catch(e){if(ticket!==epoch||e.name==='AbortError')return;result.replaceChildren(el('p',e.message||'Não foi possível comparar estes formatos de áudio. Use os dois players para comparar pelo ouvido.','muted'));if(ctx){ctx.close().catch(()=>{});ctx=null;}}
}
function displayScore(s){
  const root=$('comparison-result');root.replaceChildren();
  const row=el('div',undefined,'score-row');row.append(el('strong',s.total===null?'—':`${s.total}%`),el('span',s.total===null?'Ritmo disponível; curva da voz ainda sem sinal suficiente.':'Semelhança acústica estimada'));root.append(row);
  const metrics=el('div',undefined,'metrics');[['Duração',s.duration],['Força relativa',s.energy],['Curva da voz',s.contour]].forEach(([label,value])=>{const card=el('div',undefined,'metric');card.append(el('span',label),el('strong',value===null?'Indisponível':`${value}%`));if(value!==null){const bar=el('progress');bar.max=100;bar.value=value;bar.setAttribute('aria-label',label);card.append(bar);}metrics.append(card);});root.append(metrics);
  let advice=s.duration<70?'Experimente acompanhar a duração da referência sem correr nem arrastar as sílabas.':s.energy<70?'Ouça onde a referência ganha força e onde faz pequenas pausas.':s.contour!==null&&s.contour<65?'Repare no caminho da voz: onde sobe, desce e se mantém. Preserve os tons das palavras.':'Ouça as duas versões e escolha uma diferença pequena para trabalhar na próxima tentativa.';
  if(s.clipping>.02)advice='O áudio parece saturado. Afaste um pouco o microfone e tente novamente antes de interpretar a porcentagem.';
  root.append(el('p',`Fala detectada: referência ${s.referenceDuration.toFixed(1)} s · você ${s.userDuration.toFixed(1)} s. ${advice}`,'feedback'));
}
reference.addEventListener('play',()=>{if(recorder||pending){reference.pause();$('ref-status').textContent='Pare a gravação antes de ouvir a referência.';return;}mine.pause();});
mine.addEventListener('play',()=>reference.pause());
reference.addEventListener('ended',()=>{unlockReview();$('ref-status').textContent='Agora repita ou escute sua gravação para comparar.';});
reference.addEventListener('error',()=>{$('ref-status').textContent='Áudio indisponível no momento. Verifique sua conexão e tente selecionar a frase novamente.';});
$('record').onclick=startRecording;$('stop').onclick=stop;
$('previous').onclick=()=>select(island.id,state.positions[island.id]-1,true);
$('next').onclick=()=>select(island.id,state.positions[island.id]+1,true);
$('phrase-select').onchange=e=>select(island.id,Number(e.target.value),true);
$('complete').onclick=()=>{if(reviewLocked)return;state.reviews[phrase.id]=Math.min(Number.MAX_SAFE_INTEGER,count(phrase)+1);state.lastReviewed=new Date().toISOString();save();reviewLocked=true;$('complete').disabled=true;$('complete').textContent='Revisão registrada ✓';showProgress();phraseList();};
for(const [id,key] of [['pinyin-details','pinyin'],['meaning-details','meaning']])$(id).addEventListener('toggle',()=>{if(state){state.preferences[key]=$(id).open;save();}});
window.addEventListener('pagehide',dispose);
window.addEventListener('pageshow',e=>{if(e.persisted&&data)select(state.island,state.positions[state.island]||0);});
document.addEventListener('visibilitychange',()=>{if(document.hidden&&(recorder||pending)){dispose();$('rec-status').textContent='Gravação descartada ao sair da página.';}});
async function init(){try{const r=await fetch('./catalog.json',{cache:'no-cache'});if(!r.ok)throw Error();const catalog=await r.json();const islands=await Promise.all(catalog.islands.map(async entry=>{const response=await fetch('./'+entry.path,{cache:'no-cache'});if(!response.ok)throw Error();const module=await response.json();if(module.id!==entry.id)throw Error();return module;}));data={version:2,islands};if(!data.islands.length)throw Error();state=readState();select(state.island,state.positions[state.island]||0);$('loading').hidden=true;$('workspace').hidden=false;}catch{$('loading').textContent='Não foi possível abrir o material. Verifique a conexão e recarregue a página.';}}
init();
