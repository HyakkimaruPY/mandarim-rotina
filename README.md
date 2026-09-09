# Ilhas de mandarim

[Praticar no GitHub Pages](https://hyakkimarupy.github.io/mandarim-rotina/)

Frases em cenas ligadas à rotina, música, histórias, arte e projetos. Ouça, grave, compare e guarde seu progresso neste navegador.

## Conteúdo modular

Cada ilha vive em `content/islands/<id>.json`, com pelo menos 30 frases. O build descobre novos arquivos automaticamente: não é necessário editar a interface, importações ou contagens. Leia [o guia de criação](docs/ISLANDS.md) antes de acrescentar uma ilha.

A seleção combina interesses, estruturas comuns e auditoria lexical. A revisão mantém uma base de conversa frequente com expressões de leitura, escrita e linguagem técnica; 36 frases receberam formulações mais simples, preservando outras como ampliação de registro. [O relatório](docs/frequency-audit.json) documenta a análise; a fonte [wordfreq](https://github.com/rspeer/wordfreq) contém dados até 2021, não estatísticas atuais da conversa nem frequência de padrões gramaticais completos. Consulte [Chinese Grammar Wiki](https://resources.allsetlearning.com/chinese/grammar/HSK_3_grammar_points) para o uso dos padrões.

## Voz

A captura pede ganho automático e desativa, quando aceito pelo aparelho, redução de ruído e cancelamento de eco que podem alterar fala suave. Use fones. Um medidor aparece apenas enquanto grava. O navegador pode ignorar preferências; isso não permite garantir o mesmo resultado em todos os microfones.

A análise remove componente contínua e normaliza o sinal antes de detectar atividade e altura, evitando o corte por um volume absoluto que rejeitava vozes baixas. A reprodução recebe ganho constante limitado a 32 vezes e pico de 0,82, sem mudar duração ou altura. Isso melhora audibilidade, mas não recupera informação perdida pelo hardware e pode elevar ruído junto com a voz.

A semelhança acústica continua experimental: duração 20%, energia relativa 40%, contorno de frequência fundamental 40%. Não reconhece palavras, não alinha fonemas e não dá nota de mandarim correto. Quando a curva não é confiável, mostra os indicadores disponíveis sem inventar uma pontuação global. Os áudios de referência usam a voz sintética Microsoft Xiaoxiao, velocidade padrão; não são a voz do ChatGPT ou gravações humanas.

## Privacidade

A gravação, inclusive sua versão normalizada, permanece em memória. Navegação, nova gravação, recarga ou saída descartam os blobs e desligam o microfone. Permissões tardias são descartadas. O localStorage contém apenas posição, revisões, preferências e data da última revisão; nada disso é sincronizado com o GitHub.

## Desenvolvimento e publicação

```sh
pip install wordfreq==3.1.1 jieba==0.42.1 edge-tts==7.2.8
python scripts/content.py
python scripts/frequency.py
python scripts/validate.py
node --test tests/*.test.mjs
python scripts/generate_audio.py
python scripts/validate.py --audio
```

Sirva `dist/` por HTTPS ou localhost. A geração de áudio acontece no GitHub Actions; arquivos ausentes bloqueiam a publicação. O cache preserva áudios de textos sem mudança. Os testes cobrem voz muito baixa, contorno variável com deslocamento DC, silêncio, ruído, ganho de reprodução e descarte do gravador. Não substituem teste de microfone em aparelho real.

A publicação evita conflitos com a publicação nativa da branch e verifica a página real, o catálogo, cada módulo e amostras dos MP3. A automação semanal do ChatGPT é responsável pela redação de uma nova ilha; o workflow faz o build e a publicação.
