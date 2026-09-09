"""Lexical audit, not a frequency measurement of complete grammar patterns.
wordfreq 3.1.1 is a mixed-source snapshot through 2021.
Productive combinations are split transparently; topic words stay in the count.
"""
import json,re
from pathlib import Path
from wordfreq import tokenize,zipf_frequency
ROOT=Path(__file__).resolve().parents[1]
SPLITS={'我刚':'我 刚','喝点':'喝 点','做点':'做 点','慢慢来':'慢慢 来','听懂':'听 懂','听不懂':'听 不 懂','说不出来':'说 不 出来','说出来':'说 出来','就行':'就 行','听过':'听 过','听听':'听 听','一首':'一 首','这首':'这 首','那首':'那 首','首歌':'首 歌','这句':'这 句','那句':'那 句','这集':'这 集','一集':'一 集','这张':'这 张','一遍':'一 遍','看一遍':'看 一 遍','我能':'我 能','更难':'更 难','别急':'别 急','别动':'别 动','试一下':'试 一下','几次':'几 次','不太':'不 太','有太多':'有 太 多','不用说':'不用 说','忘不了':'忘 不 了','条路':'条 路','就够':'就 够','打不开':'打 不 开','换个':'换 个','会儿':'会 儿','有空':'有 空'}
SPLITS.update({'一只':'一 只','一部':'一 部','一句':'一 句','有个':'有 个','坐在':'坐 在','放在':'放 在','更好':'更 好','这一':'这 一','想过':'想 过','我会':'我 会','很想':'很 想','一段':'一 段','再有':'再 有','学到':'学 到','做好':'做 好','留着':'留 着'})
def audit():
    report={'source':'wordfreq 3.1.1 (data through 2021; mixed domains)','highFrequencyZipf':5,'commonZipf':4.5,'productiveSplits':SPLITS,'islands':[]}
    for file in sorted((ROOT/'content/islands').glob('*.json')):
        i=json.loads(file.read_text());phrases=[];alltokens=[]
        for p in i['phrases']:
            tokens=[part for token in tokenize(p['zh'],'zh') for part in SPLITS.get(token,token).split() if re.search('[\u4e00-\u9fff]',part)]
            alltokens+=tokens
            phrases.append({'id':p['id'],'highFrequencyShare':round(sum(zipf_frequency(t,'zh')>=5 for t in tokens)/len(tokens),3),'lessFrequent':[{'word':t,'zipf':zipf_frequency(t,'zh')} for t in dict.fromkeys(tokens) if zipf_frequency(t,'zh')<4.5]})
        high=sum(zipf_frequency(t,'zh')>=5 for t in alltokens)/len(alltokens)
        common=sum(zipf_frequency(t,'zh')>=4.5 for t in alltokens)/len(alltokens)
        report['islands'].append({'id':i['id'],'highFrequencyShare':round(high,3),'commonShare':round(common,3),'phrases':phrases})
        print(i['id'],f'high={high:.1%}',f'common={common:.1%}')
        assert high>=.80,f'{i["id"]}: revise vocabulary (minimum 80% Zipf >=5)'
        assert common>=.88,f'{i["id"]}: revise vocabulary (minimum 88% Zipf >=4.5)'
    (ROOT/'docs/frequency-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':audit()
