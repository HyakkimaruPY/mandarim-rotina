# Ilhas de mandarim

150 frases autorais em 5 ilhas de 30 frases: rotina, música, histórias, arte e projetos. Cada ilha tem seis cenas conectadas de cinco frases. O site abre diretamente na prática e guarda a última frase de cada ilha neste navegador.

## Experiência

- Referência em MP3 com voz sintética Microsoft `zh-CN-XiaoxiaoNeural`, velocidade padrão. Não é uma gravação humana ou a voz do ChatGPT. As indicações de emoção são orientação pedagógica; a síntese não assegura interpretação nativa em cada frase.
- Gravação com MediaRecorder; ouvir e pausar nos dois players, que não tocam simultaneamente.
- Comparação acústica local e experimental: duração (20%), envelope de energia normalizado (40%) e contorno relativo de frequência fundamental (40%). Não reconhece palavras, não alinha fonemas e não valida os tons de cada sílaba. Não é uma nota de pronúncia.
- Silêncio insuficiente é rejeitado. Se não houver contorno detectável suficiente, não há porcentagem global. Microfones, ruído, eco e timbre podem alterar a estimativa.
- Progresso no `localStorage`: posição por ilha, revisões por frase, preferências de pistas e data da última revisão. Revisões são confirmadas pelo estudante; não se confundem com domínio. Uma ilha percorrida tem todas as frases revisadas ao menos uma vez; uma volta completa é o mínimo de revisões entre suas frases.
- Nenhuma gravação do estudante é enviada ao servidor ou armazenada no localStorage. Trocar de frase/ilha, iniciar nova gravação, recarregar ou sair destrói os blobs e URLs temporários e encerra o microfone. Sair para outro aplicativo durante uma gravação também a descarta. Permissões tardias não ressuscitam uma gravação antiga.
- Pinyin e tradução recolhíveis, contraste, foco visível, navegação por teclado, controles nativos de áudio e layout móvel.

## Conteúdo e enriquecimento

Edite `scripts/content.py` e execute `python scripts/content.py` com `pypinyin==0.55.0`. O resultado versionado é `dist/content.json`. Mantenha os IDs para preservar o progresso existente. Para uma frase substituída por outra sem continuidade pedagógica, use um novo ID. Campos: `zh`, `pt`, `pinyin`, `note`, `scene`, `cue`, `register`, `audio`.

O pinyin usa tons de dicionário e dicionário contextual para caracteres polifônicos. Não é uma transcrição fonética do áudio; mudanças de 一, 不 e sequências de terceiro tom devem ser observadas na fala. As frases avançam de fala curta para escrita breve e não recebem um rótulo HSK artificial.

As situações se inspiram nos interesses solicitados, sem supor horários de trabalho ou uma agenda pessoal. São frases autorais, não citações de obras ou extrações de um corpus. A escolha prioriza uso transversal de estruturas comuns, sem alegar frequência estatística medida.

Referências de consulta: [Chinese Grammar Wiki — HSK 3](https://resources.allsetlearning.com/chinese/grammar/HSK_3_grammar_points), [exemplo de organização por etapas no 人民网 (2026)](https://cpc.people.com.cn/n1/2026/0713/c461783-40759206.html).

## Publicação

O workflow `.github/workflows/pages.yml` gera os 150 MP3, valida todos os arquivos e só então publica `dist/` no GitHub Pages. Os áudios são preservados no cache de build e no artefato `mandarim-rotina-site` por 30 dias; são regeneráveis a partir do texto e da voz. Não se publicam referências ausentes silenciosamente. O cache usa hashes de texto, voz e configuração.

Se o repositório ainda não estiver habilitado para Pages, configure **Settings → Pages → Source → GitHub Actions**. O token padrão de Actions pode não ter permissão administrativa para habilitar Pages pela primeira vez. Não inclua tokens ou chaves no front-end.

Para abrir localmente: `python -m http.server 8000 --directory dist`. Sem gerar os áudios, os players reportam referências indisponíveis. A gravação requer HTTPS ou localhost e permissão do microfone. A decodificação dos formatos de gravação varia por navegador; falha na análise não impede ouvir a gravação.

## Validação

```sh
python scripts/validate.py
node --check dist/app.mjs
node --test tests/analysis.test.mjs
python scripts/generate_audio.py
python scripts/validate.py --audio
```

Os testes acústicos cobrem silêncio, identidade, duração, normalização de volume e contorno ausente. Eles não substituem validação fonética por falante humano nem testes com microfone em aparelhos reais.
This is a simple storage of my study
