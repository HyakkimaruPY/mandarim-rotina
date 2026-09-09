"""Build reproducible reference audio; never receives learner recordings."""
import asyncio, hashlib, json
from pathlib import Path
import edge_tts

ROOT=Path(__file__).resolve().parents[1]
VOICE='zh-CN-XiaoxiaoNeural'

async def main():
    phrases=[p for i in json.loads((ROOT/'dist/content.json').read_text())['islands'] for p in i['phrases']]
    directory=ROOT/'dist/audio';directory.mkdir(exist_ok=True)
    manifest_path=directory/'manifest.json'
    previous=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest={}
    sem=asyncio.Semaphore(3)
    async def one(p):
        filename=ROOT/'dist'/p['audio']
        digest=hashlib.sha256((VOICE+'|+0%|'+p['zh']).encode()).hexdigest()
        if previous.get(p['id'],{}).get('hash')==digest and filename.exists() and filename.stat().st_size>1500:
            manifest[p['id']]=previous[p['id']];return
        async with sem:
            for attempt in range(4):
                try:
                    temporary=filename.with_suffix('.partial')
                    await asyncio.wait_for(edge_tts.Communicate(p['zh'],VOICE,rate='+0%',volume='+0%',pitch='+0Hz').save(str(temporary)),60)
                    if temporary.stat().st_size<1500:raise ValueError('Empty audio')
                    temporary.replace(filename)
                    manifest[p['id']]={'hash':digest,'voice':VOICE,'rate':'+0%','bytes':filename.stat().st_size}
                    print(f'OK {p["id"]}',flush=True);return
                except Exception as e:
                    if attempt==3:raise RuntimeError(f'Audio failed: {p["id"]}: {e}') from e
                    await asyncio.sleep(2**attempt)
    await asyncio.gather(*(one(p) for p in phrases))
    assert len(manifest)==len(phrases)
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Validated {len(manifest)} reference files.')

if __name__=='__main__':asyncio.run(main())
