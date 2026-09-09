"""Discover standalone islands; generate the catalog and compatibility bundle."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build():
    islands=[];ids=set();sentences=set();concepts=set()
    for path in sorted((ROOT/'content/islands').glob('*.json')):
        i=json.loads(path.read_text())
        assert i['schemaVersion']==1 and re.fullmatch('[a-z0-9-]+',i['id'])
        assert path.stem==i['id'] and i['id'] not in ids
        assert i['concept'] not in concepts,'Duplicate island concept'
        concepts.add(i['concept']);ids.add(i['id'])
        assert len(i['phrases'])>=30 and len(i['corePatterns'])>=4
        for p in i['phrases']:
            assert p['id'] not in ids and re.fullmatch('[a-z0-9-]+',p['id'])
            ids.add(p['id']);key=re.sub(r'[^\u4e00-\u9fff]','',p['zh'])
            assert key not in sentences,f'Duplicate phrase: {p["id"]}'
            sentences.add(key)
            for field in ['zh','pt','pinyin','note','scene','cue','register']:assert p[field].strip()
            p['audio']=f'audio/{p["id"]}.mp3'
            p['audioVersion']=hashlib.sha256(p['zh'].encode()).hexdigest()[:12]
        islands.append(i)
    islands.sort(key=lambda i:(i.get('order',9999),i['id']))
    assert islands
    directory=ROOT/'dist/islands';directory.mkdir(exist_ok=True)
    for file in directory.glob('*.json'):
        if file.stem not in {i['id'] for i in islands}:file.unlink()
    for i in islands:(directory/f'{i["id"]}.json').write_text(json.dumps(i,ensure_ascii=False,indent=2)+'\n')
    catalog={'version':2,'islands':[{'id':i['id'],'path':f'islands/{i["id"]}.json','title':i['title'],'count':len(i['phrases'])} for i in islands]}
    (ROOT/'dist/catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'dist/content.json').write_text(json.dumps({'version':2,'title':'Ilhas de mandarim','islands':islands},ensure_ascii=False,indent=2)+'\n')
    print(f'{len(islands)} modules · {len(sentences)} phrases')
if __name__=='__main__':build()
