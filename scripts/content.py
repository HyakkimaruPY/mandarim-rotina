"""Frases autorais: cenas conectadas; mandarim contemporâneo sem ranking de corpus."""
import json
from pathlib import Path
from pypinyin import pinyin, Style, load_phrases_dict

load_phrases_dict({'音乐': [['yīn'], ['yuè']], '觉得': [['jué'], ['de']], '重复': [['chóng'], ['fù']], '重新': [['chóng'], ['xīn']], '长大': [['zhǎng'], ['dà']], '还没': [['hái'], ['méi']]})
load_phrases_dict({'多长': [['duō'], ['cháng']], '不长': [['bù'], ['cháng']], '说得': [['shuō'], ['de']], '看得': [['kàn'], ['de']], '还得': [['hái'], ['děi']], '舒服': [['shū'], ['fu']], '眼睛': [['yǎn'], ['jing']]})
ROOT=Path(__file__).resolve().parents[1]
islands=[]
def island(id,title,zh,description,scenes,lines):
    rows=[line.split('|') for line in lines.strip().splitlines()]
    assert len(rows)==30,(id,len(rows))
    phrases=[]
    for i,(text,pt,note) in enumerate(rows):
        scene=scenes[i//5]
        phrases.append(dict(id=f'{id}-{i+1:02}',zh=text,pt=pt,pinyin=' '.join(x[0] for x in pinyin(text,style=Style.TONE,neutral_tone_with_five=False)),note=note,scene=scene[0],cue=scene[1],register='Escrita breve' if scene[0].startswith('Diário') else 'Conversa',audio=f'audio/{id}-{i+1:02}.mp3'))
    islands.append(dict(id=id,title=title,zh=zh,description=description,phrases=phrases))

island('rotina','No seu tempo','日常','Pequenas decisões, uma pausa para estudar e o fim do dia.',[
('Começar o dia','Tom tranquilo, de quem acabou de acordar.'),('Uma pausa para o mandarim','Curiosidade; fale como se estivesse pensando em voz alta.'),('Ouvir e tentar de novo','Pedido amigável, sem recitar palavra por palavra.'),('Resolver o básico','Conversa leve, com pausas entre as ações.'),('Encerrar o dia','Alívio e cansaço suave.'),('Diário · um dia possível','Relato pessoal, com ritmo de conversa.')],'''
我刚起来。|Acabei de levantar.|刚 situa uma ação que acabou de acontecer.
先喝点水吧。|Vamos tomar um pouco de água primeiro.|点 reduz a quantidade; 吧 suaviza a sugestão.
今天想做点什么？|O que quero fazer hoje?|想做点什么 serve para pensar em planos sem decidir tudo.
我还没想好。|Ainda não decidi.|还没 + resultado: o processo ainda não chegou à conclusão.
不着急，慢慢来。|Sem pressa, vamos com calma.|慢慢来 é uma expressão cotidiana de encorajamento.
我想先听一会儿中文。|Quero ouvir um pouco de chinês primeiro.|一会儿 delimita um período curto, sem horário exato.
不用每个字都听懂。|Não preciso entender cada palavra.|不用 indica que algo não é necessário; 都 abrange todos.
先听一遍，再跟着说。|Primeiro ouço uma vez, depois repito junto.|先…再… organiza ações; 遍 conta uma passagem completa.
这句话我好像听过。|Acho que já ouvi essa frase.|好像 deixa a impressão em aberto; 过 marca experiência.
换个地方，我也能用。|Em outro contexto, também consigo usar.|换个… é uma maneira coloquial de propor uma mudança.
刚才那句是什么意思？|O que significa aquela frase de agora há pouco?|刚才 retoma o momento recente; 那句 evita repetir 话.
你能不能再说一遍？|Você pode dizer mais uma vez?|能不能 transforma a possibilidade em pergunta.
不用放慢，正常说就行。|Não precisa desacelerar; pode falar normalmente.|…就行 significa que isso basta.
我再试一次。|Vou tentar mais uma vez.|再 aponta uma nova tentativa; 次 conta ocorrências.
这次比刚才顺一点。|Desta vez saiu um pouco mais fluido.|比 compara; 一点 torna a diferença pequena.
手机快没电了。|O celular está quase sem bateria.|快…了 indica uma mudança prestes a acontecer.
我先充会儿电。|Vou carregar um pouco primeiro.|充会儿电 encaixa a duração dentro de 充电.
等一下，我去拿耳机。|Espera um pouco, vou pegar os fones.|去拿 liga deslocamento e objetivo.
你先忙，我等你。|Pode terminar o que está fazendo; eu espero.|你先忙 é uma maneira natural de respeitar o tempo de alguém.
好了，现在可以了。|Pronto, agora dá.|好了 sinaliza que algo ficou pronto ou foi resolvido.
今天有点累。|Hoje estou um pouco cansado.|有点 costuma introduzir um estado levemente indesejado.
我想安静一会儿。|Quero ficar quieto um pouco.|安静 pode funcionar como estado desejado depois de 想.
再听一首就睡。|Vou ouvir só mais uma música e dormir.|再…就… cria um limite; 首 conta músicas.
剩下的明天再说吧。|O resto fica para amanhã.|明天再说 pode adiar a resolução, não só uma conversa.
今天就到这儿吧。|Por hoje, vamos ficar por aqui.|就到这儿 encerra uma atividade de modo natural.
今天没有安排太多事情。|Hoje não planejei muitas coisas.|没有 nega uma ação passada; 太多 quantifica em excesso.
有空的时候，我会听听中文。|Quando tenho tempo, costumo ouvir um pouco de chinês.|…的时候 cria o contexto; 听听 torna a atividade breve e leve.
听不懂的地方，我会再听一遍。|Nas partes que não entendo, ouço mais uma vez.|听不懂的地方 transforma a dificuldade em assunto da frase.
虽然只练了一会儿，但感觉不错。|Embora tenha praticado só um pouco, foi bom.|虽然…但… relaciona uma limitação e um resultado positivo.
不用一次学完，明天还能继续。|Não preciso aprender tudo de uma vez; amanhã posso continuar.|学完 marca conclusão; 还能 expressa possibilidade que permanece.
''')

island('musica','Entre uma música e outra','音乐','Escolher uma canção, perceber a voz e conversar sobre o que ficou.',[
('Escolher o que ouvir','Interesse tranquilo; uma conversa sobre preferências.'),('A voz e o arranjo','Admiração discreta, sem exagerar cada palavra.'),('Encontrar o sentido','Curiosidade e uma pequena descoberta.'),('Ouvir junto','Convite amigável; perguntas abertas.'),('Uma lembrança na música','Nostalgia suave, mantendo os tons das palavras.'),('Diário · depois de ouvir','Reflexão íntima, com pausas naturais.')],'''
我想听点老歌。|Quero ouvir umas músicas antigas.|听点… apresenta uma vontade sem tornar a frase formal.
有没有安静一点的？|Tem alguma mais calma?|…一点的 omite o substantivo já entendido na conversa.
我比较喜欢女声。|Prefiro vozes femininas.|比较喜欢 expressa preferência com suavidade.
这首歌你听过吗？|Você já ouviu esta música?|听过 pergunta por experiência, não por uma ação acontecendo.
我在网易云音乐上找到的。|Encontrei no NetEase Music.|…上找到的 destaca onde ocorreu a descoberta.
她的声音很温柔。|A voz dela é muito suave.|声音 descreve a voz ou o som; 温柔 descreve sua qualidade.
这首歌听着很舒服。|É gostoso ouvir esta música.|听着 descreve a sensação enquanto se ouve.
伴奏不会盖过她的声音。|O acompanhamento não encobre a voz dela.|盖过 funciona como superar ou encobrir em intensidade.
我更喜欢这个版本。|Gosto mais desta versão.|更 compara com uma alternativa já presente no contexto.
尤其是最后那一句。|Principalmente aquela última frase.|尤其是 destaca uma parte; pode continuar a fala anterior.
这句歌词是什么意思？|O que significa este verso?|歌词 é a letra da música; 这句 recorta um verso.
我听出来了，但还不太懂。|Consegui distinguir o que foi dito, mas ainda não entendo bem.|听出来 e 懂 separam reconhecimento pelo ouvido e compreensão.
原来是在说想念一个人。|Ah, então fala de sentir falta de alguém.|原来 apresenta uma descoberta que reorganiza o sentido.
怪不得听起来有点难过。|Por isso soa um pouco triste.|怪不得 liga a descoberta a uma impressão anterior.
知道意思以后，感觉不一样了。|Depois de entender, a sensação mudou.|…以后 situa o depois; 不一样了 marca mudança.
你听听这一段。|Ouve este trecho.|听听 suaviza o convite; 段 conta trechos.
是不是很好听？|É bonita, né?|是不是 pode buscar concordância sobre uma impressão.
你更喜欢哪一首？|De qual música você gosta mais?|哪一首 pede uma escolha entre músicas.
我把这首加到歌单里了。|Coloquei esta música na playlist.|把…加到…里 apresenta o destino de algo conhecido.
下次我们一起听。|Da próxima vez, ouvimos juntos.|下次 abre uma proposta para outra ocasião.
这首歌让我想起以前的事。|Esta música me faz lembrar de coisas do passado.|让…想起… conecta algo a uma lembrança.
说不上来，就是有点感动。|Não sei explicar; só me emociona um pouco.|说不上来 expressa dificuldade de pôr a impressão em palavras.
我不是难过，只是想静一静。|Não estou triste; só quero ficar quieto um pouco.|不是…只是… corrige uma interpretação com delicadeza.
有些歌越听越喜欢。|De algumas músicas, gosto mais a cada vez que ouço.|越…越… relaciona duas mudanças progressivas.
再放一遍吧。|Coloca mais uma vez.|放 é usado para tocar áudio; 遍 conta a execução inteira.
今天又听到了那首老歌。|Hoje ouvi aquela música antiga de novo.|又 apresenta uma repetição que já aconteceu.
旋律很简单，却让人忘不了。|A melodia é simples, mas não sai da memória.|却 cria contraste; 忘不了 indica não conseguir esquecer.
歌词里没有说得很直接。|A letra não diz tudo de forma muito direta.|说得很直接 descreve a maneira de expressar algo.
但我好像明白了那种感觉。|Mas acho que entendi aquela sensação.|那种感觉 retoma um tipo de sentimento compartilhado no contexto.
对我来说，听歌也是在学中文。|Para mim, ouvir música também é aprender chinês.|对我来说 introduz a perspectiva pessoal.
''')

island('historias','Dentro da história','故事','Dr dramas cotidianos a xianxia: acompanhar, reagir e contar sem dar spoiler.'.replace('Dr dramas','De dramas'),[
('Escolher um drama','Conversa curiosa e descontraída.'),('Acompanhar a cena','Dúvida real: pergunte sem transformar tudo em exclamação.'),('Entender por contexto','Pequenos momentos de compreensão.'),('Conversar sobre xianxia','Entusiasmo contido, como entre amigos.'),('Sem dar spoiler','Expectativa, surpresa e pedidos leves.'),('Diário · depois do episódio','Reflexão sobre a história; cadência clara.')],'''
你最近在看什么剧？|Que drama você está vendo ultimamente?|最近在看 pergunta por uma atividade em andamento neste período.
我在看一部现代剧。|Estou vendo um drama contemporâneo.|部 conta obras audiovisuais; 现代剧 contrasta com dramas de época.
一集大概多长？|Quanto tempo dura mais ou menos um episódio?|大概 pede uma estimativa; 多长 pergunta duração aqui.
这集不长，先看完吧。|Este episódio é curto; vamos terminar primeiro.|看完 destaca chegar ao fim do que se assiste.
我想先不看字幕。|Quero tentar sem olhar as legendas primeiro.|先不… propõe deixar algo de lado nesta primeira tentativa.
他刚才为什么那么说？|Por que ele disse aquilo agora há pouco?|那么说 retoma a maneira ou o conteúdo de uma fala.
她是不是生气了？|Será que ela ficou brava?|生气了 sugere mudança de estado.
我觉得他没听懂。|Acho que ele não entendeu.|我觉得 introduz interpretação; 没听懂 nega o resultado.
你看，她根本不相信他。|Olha, ela não acredita nele de jeito nenhum.|根本不 intensifica a negação.
先别急着下结论。|Não vamos tirar conclusões tão cedo.|先别急着… pede que se adie uma ação precipitada.
这句话我能听懂。|Esta frase eu consigo entender.|O assunto 这句话 aparece antes do sujeito.
但让我自己说，我还说不出来。|Mas, se for para eu falar, ainda não consigo.|说不出来 é não conseguir produzir ou expressar a fala.
再看一遍就明白了。|Vendo mais uma vez, dá para entender.|…就… liga uma ação a um resultado acessível.
原来他是在开玩笑。|Ah, ele estava brincando.|原来…是在… apresenta a intenção percebida depois.
难怪她笑了。|Por isso ela sorriu.|难怪 comenta algo que agora faz sentido.
我也喜欢看仙侠剧。|Também gosto de dramas xianxia.|也 conecta seu gosto ao que já foi dito.
你看过《仙逆》吗？|Você já viu Xian Ni?|看过 pode perguntar por uma obra vista ou lida; o contexto resolve.
我想知道他后来怎么样了。|Quero saber o que aconteceu com ele depois.|后来 pergunta pela sequência narrativa, não pelo futuro de hoje.
他为什么非要走这条路？|Por que ele insiste em seguir esse caminho?|非要 expressa insistência; 路 pode ser uma escolha de vida.
如果是你，你会怎么选？|Se fosse você, o que escolheria?|如果…会… cria uma situação hipotética para conversar.
先别告诉我结局。|Não me conte o final ainda.|先别… pede para não fazer algo por enquanto.
我还没看到那里。|Ainda não cheguei nessa parte.|看到那里 localiza o ponto alcançado na história.
没想到会这样。|Não imaginei que seria assim.|没想到 reage a um resultado inesperado.
这一段看得我有点难受。|Esse trecho me deixou um pouco angustiado.|看得我… descreve o efeito de assistir sobre quem fala.
看完以后再聊吧。|Vamos conversar depois de terminar.|看完以后 une resultado concluído e momento seguinte.
这集没有太多对白。|Este episódio não tem muitos diálogos.|对白 se refere às falas de personagens.
人物的表情已经说明了很多。|As expressões dos personagens já dizem muito.|已经 indica que o efeito já está presente; 说明 expressa evidenciar.
有些话不用说出来，也能听懂。|Algumas coisas podem ser entendidas mesmo sem serem ditas.|不用…也能… liga ausência de necessidade e possibilidade.
比起结局，我更在意他的选择。|Mais do que o final, me importam as escolhas dele.|比起…更… organiza prioridades, não só diferenças de grau.
这个故事让我想了很久。|Esta história me deixou pensando por muito tempo.|让…想了很久 descreve um efeito que durou.
''')

island('arte','O que o desenho sugere','画画','Começar um desenho, rever escolhas e deixar espaço para quem olha.',[
('Uma ideia aparece','Tom de descoberta; fale com espontaneidade.'),('Escolher o clima','Imagine que está mostrando um rascunho a alguém.'),('Olhar de novo','Observação cuidadosa, sem pressa artificial.'),('Trocar impressões','Curiosidade respeitosa; espaço para outra leitura.'),('Ajustar sem perder a ideia','Decisão tranquila, com ênfase na mudança desejada.'),('Diário · sobre criar','Reflexivo, mantendo uma leitura fluida.')],'''
我突然有个想法。|De repente, tive uma ideia.|有个想法 é uma abertura coloquial; 突然 marca o surgimento.
我想把它画下来。|Quero colocar isso num desenho.|把…画下来 apresenta registrar uma ideia desenhando.
先画个大概吧。|Vou fazer um esboço primeiro.|画个大概 é desenhar a ideia geral, sem detalhar tudo.
细节可以慢慢加。|Os detalhes podem vir aos poucos.|慢慢加 permite um processo gradual.
我还没想好背景。|Ainda não decidi o fundo.|想好 indica chegar a uma decisão.
我想画一只黑猫。|Quero desenhar um gato preto.|只 conta animais como gatos.
让它坐在月亮下面。|Vou colocá-lo sentado sob a lua.|让它… introduz o que você quer que a figura faça na cena.
颜色不用太亮。|As cores não precisam ser muito claras ou vivas.|不用太… limita uma característica sem negá-la por completo.
我想留一点空白。|Quero deixar um pouco de espaço em branco.|留一点… expressa reservar uma pequena parte.
这样看起来更安静。|Assim, a cena parece mais tranquila.|看起来 relata uma impressão visual.
这里是不是有点挤？|Será que esta parte está um pouco apertada?|是不是 + 有点 torna a observação menos categórica.
把这个往左移一点。|Move isto um pouco para a esquerda.|往左 dá direção; 一点 mede uma mudança pequena.
现在舒服多了。|Agora ficou bem mais agradável.|…多了 indica uma melhora perceptível em relação a antes.
不过，眼睛还得改一下。|Mas ainda preciso ajustar os olhos.|还得 significa ainda ter que; 一下 suaviza o ajuste.
我想让它看起来有点孤独。|Quero que ele pareça um pouco solitário.|想让…看起来… conecta intenção e impressão visual.
你觉得这张画怎么样？|O que você acha deste desenho?|你觉得…怎么样 convida a pessoa a formular uma avaliação.
你第一眼看到了什么？|O que você viu à primeira vista?|第一眼 localiza a impressão inicial.
我不想把意思说得太清楚。|Não quero deixar o sentido explícito demais.|把意思说得… focaliza a forma de comunicar a ideia.
每个人看到的可能不一样。|Cada pessoa pode enxergar algo diferente.|看到的 transforma aquilo que se vê em assunto da frase.
你这么说，我倒是没想到。|Não tinha pensado nisso que você disse.|倒是 marca uma mudança inesperada na perspectiva.
这一版比之前自然一点。|Esta versão ficou um pouco mais natural que a anterior.|比之前 compara com uma etapa do próprio trabalho.
我想保留原来的感觉。|Quero preservar a sensação original.|保留原来的… serve para preservar uma qualidade existente.
不是越复杂越好。|Nem sempre quanto mais complexo, melhor.|不是越…越… questiona uma relação automática.
少一点，反而更有感觉。|Com um pouco menos, acaba transmitindo mais.|反而 apresenta um resultado contrário ao esperado.
先放一放，明天再看。|Vou deixar de lado um pouco e olhar amanhã.|放一放 sugere interromper temporariamente, sem abandonar.
画到一半的时候，我换了个想法。|No meio do desenho, mudei de ideia.|…到一半的时候 situa uma mudança durante o processo.
我发现留白比加细节更难。|Percebi que deixar espaço em branco é mais difícil que detalhar.|发现 introduz uma descoberta; 比 compara duas ações.
有时候，画面不用解释太多。|Às vezes, a imagem não precisa explicar tanto.|有时候 restringe a observação a certas situações.
我希望别人能在里面看到自己的故事。|Espero que outras pessoas encontrem ali a própria história.|希望…能… expressa um desejo sobre a experiência de alguém.
至于答案，可以慢慢想。|Quanto à resposta, dá para pensar aos poucos.|至于 muda o foco do texto para um novo aspecto.
''')

island('projetos','Da ideia ao teste','项目','Explicar uma ferramenta, encontrar um erro e testar uma correção.',[
('Explicar a ideia','Clareza de uma conversa entre colaboradores.'),('Encontrar o problema','Dúvida atenta; evite soar acusatório.'),('Investigar antes de mudar','Tom prático, com etapas bem conectadas.'),('Pedir um ajuste','Pedido direto e cortês.'),('Testar e confirmar','Concentração; alívio apenas quando o teste funciona.'),('Diário · o que aprendi','Relato simples de causa, tentativa e resultado.')],'''
我有个小项目。|Tenho um pequeno projeto.|有个… introduz um assunto novo de forma coloquial.
我想做一个练中文的网页。|Quero criar uma página para praticar chinês.|练中文的 modifica 网页 e explica sua finalidade.
打开以后就能直接用。|Ao abrir, já dá para usar.|…以后就能… liga uma etapa a uma capacidade imediata.
最好在手机上也能用。|Seria melhor se também funcionasse no celular.|最好 expressa uma preferência de implementação.
先把基本功能做好。|Primeiro, vamos fazer o básico funcionar bem.|把…做好 enfatiza realizar algo com um bom resultado.
这里好像有个问题。|Parece que há um problema aqui.|好像 apresenta uma hipótese antes de confirmar.
我点了，但是没反应。|Cliquei, mas não aconteceu nada.|没反应 é uma forma cotidiana de descrever falta de resposta.
页面一直在加载。|A página não para de carregar.|一直在… indica continuidade de uma ação.
刚才还能用，现在不行了。|Agora há pouco funcionava; agora não funciona.|还…现在…了 contrasta o estado anterior com uma mudança.
是不是哪里没设置好？|Será que alguma configuração ficou faltando?|哪里 não precisa ser um lugar físico; 没…好 indica resultado incompleto.
先看看报错信息。|Vamos olhar a mensagem de erro primeiro.|看看 apresenta uma verificação rápida.
这个地址打不开。|Não consigo abrir este endereço.|打不开 expressa impossibilidade de alcançar o resultado de abrir.
换一个试试。|Troca por outro para testar.|试试 propõe experimentar sem prometer o resultado.
别急着改，先找原因。|Não vamos alterar às pressas; primeiro achar a causa.|别急着…先… organiza cautela e próximo passo.
我想知道到底是哪一步出了问题。|Quero saber exatamente em qual etapa surgiu o problema.|到底 reforça a busca por uma resposta precisa.
能不能加一个播放按钮？|Dá para adicionar um botão de reprodução?|能不能 faz um pedido sobre possibilidade.
录完以后，我想听听自己的声音。|Depois de gravar, quero ouvir minha própria voz.|录完以后 situa o que vem após concluir a gravação.
切换句子的时候，把录音删掉。|Ao mudar de frase, apague a gravação.|切换句子 explicita trocar a frase praticada; 删掉 enfatiza remoção.
只保存进度就够了。|Basta salvar o progresso.|只…就够了 delimita o que é suficiente.
其他功能先别动。|Por enquanto, não altere as outras funções.|先别动 pode pedir para preservar uma parte do projeto.
改好了，我再试一下。|Ajustei; vou testar de novo.|改好了 anuncia conclusão; 再 indica uma nova tentativa.
这次能正常播放了。|Desta vez, reproduziu normalmente.|能…了 marca uma capacidade restaurada.
但我还想多测几次。|Mas quero testar mais algumas vezes.|多…几次 pede repetição adicional, sem número fechado.
如果又卡住，就把情况记下来。|Se travar de novo, registre o que aconteceu.|如果…就… define uma resposta a uma condição.
确认没问题以后再更新。|Só atualize depois de confirmar que está tudo certo.|…以后再… estabelece uma condição temporal antes da ação.
今天的问题比我想的复杂。|O problema de hoje era mais complexo do que imaginei.|比我想的 compara a realidade com uma expectativa.
一开始，我以为是网络的问题。|No começo, achei que fosse a rede.|以为 apresenta uma crença anterior, frequentemente corrigida depois.
后来才发现，是我把数据看错了。|Só depois percebi que tinha interpretado os dados errado.|才 enfatiza a descoberta tardia; 看错了 marca erro de interpretação.
找到原因以后，修改就简单多了。|Depois de achar a causa, ficou bem mais simples corrigir.|…就… liga a descoberta à consequência; 多了 intensifica a diferença.
下次遇到类似的问题，我就知道怎么查了。|Da próxima vez que algo parecido acontecer, saberei investigar.|遇到…就… liga uma situação futura à resposta aprendida.
''')

output=dict(version=1,title='Ilhas de mandarim',islands=islands)
(ROOT/'dist/content.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(f'{len(islands)} ilhas · {sum(len(x["phrases"]) for x in islands)} frases')
