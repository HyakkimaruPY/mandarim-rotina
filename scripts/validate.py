import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
content=json.loads((root/'dist/content.json').read_text())
catalog=json.loads((root/'dist/catalog.json').read_text())
assert len(catalog['islands'])==len(content['islands'])
for entry in catalog['islands']:
    module=json.loads((root/'dist'/entry['path']).read_text())
    assert module['id']==entry['id'] and len(module['phrases'])==entry['count']
ids=set();sentences=set()
for island in content['islands']:
    assert len(island['phrases'])>=30
    for p in island['phrases']:
        assert p['id'] not in ids and p['zh'] not in sentences
        ids.add(p['id']);sentences.add(p['zh'])
        for field in ['zh','pt','pinyin','note','scene','cue','audio']:assert p[field].strip()
        assert '..' not in p['audio'] and p['audio'].startswith('audio/')
        if '--audio' in sys.argv:assert (root/'dist'/p['audio']).stat().st_size>1500,p['id']
if '--audio' in sys.argv:
    manifest=json.loads((root/'dist/audio/manifest.json').read_text())
    assert set(manifest)==ids
print(f'OK: {len(content["islands"])} coherent islands, {len(ids)} unique phrases'+(' and all audio assets' if '--audio' in sys.argv else ''))
