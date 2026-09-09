# Como acrescentar uma ilha

A fonte canônica é `content/islands/<id>.json`. Uma ilha nova requer apenas um novo arquivo nessa pasta. `scripts/content.py` descobre os módulos, valida, ordena por `order` e gera `dist/catalog.json`, `dist/islands/*.json` e o agregado `dist/content.json`. A aplicação lê o catálogo e os módulos; o workflow gera os áudios automaticamente. Não altere HTML, JavaScript, contagens fixas ou uma lista manual de importações para acrescentar conteúdo.

Use uma ilha existente como exemplo estrutural. Campos de ilha: `schemaVersion: 1`, `id` igual ao nome do arquivo, `title`, `zh`, `description`, `concept` (situação e objetivo comunicativo), `order`, `corePatterns` (pelo menos quatro), `topicWords` e `phrases` (pelo menos 30). Cada frase tem `id`, `zh`, `pt`, `pinyin`, `note`, `scene`, `cue` e `register`. O caminho de áudio deriva do ID; o build o preenche. IDs usam letras latinas minúsculas, números e hífen.

## Critério pedagógico

1. Escolha uma situação ligada a rotina, música chinesa suave e antiga, dramas modernos, xianxia, desenho, criação ou projetos no celular. Não suponha horários, emprego ou novos hábitos pessoais.
2. Leia TODOS os módulos existentes antes de propor o tema. Compare conceito, objetivo comunicativo, cenas e frases. Um novo título para o mesmo conteúdo não é uma ilha nova. Evite duplicatas semânticas, além das duplicatas textuais que o build detecta.
3. Monte pelo menos seis pequenas cenas conectadas de cinco frases. Faça o tema avançar; não empilhe exemplos aleatórios ou sinônimos só para completar 30. As frases iniciais devem ser curtas e ter menor carga lexical; amplie sem perder a situação.
4. O núcleo é mandarim comum: 我想…, 有没有…, 能不能…, 还没…, 我觉得…, 先…再…, …的时候, …以后, 如果…就… e estruturas semelhantes. Reapresente pelo menos quatro padrões em duas ou mais cenas quando isso soar natural. A naturalidade e a conexão entre falas são requisitos, não sacrifícios aceitáveis por uma métrica.
5. Vocabulário de interesse serve de pequeno apoio temático. Mescle também formas de livros, artigos e linguagem técnica: o usuário explicitamente gosta delas. Reserve uma pequena parte da ilha, por exemplo 4–6 frases, para esses registros dentro das cenas, sem transformar a ilha inteira em fala básica. Introduza em geral no máximo um termo menos frequente novo por frase; mantenha o contexto e a explicação. Marque o registro no campo register (Conversa, Leitura e escrita ou Técnica).
6. Execute a auditoria lexical: no mínimo 80% dos componentes com Zipf >=5 no conjunto e 88% com Zipf >=4.5 em cada ilha. Os termos temáticos CONTINUAM no denominador. Leia o relatório por frase, revisando concentração de palavras raras; não acrescente palavras vazias para aumentar a porcentagem. As divisões produtivas explicitadas em `scripts/frequency.py` separam, por exemplo, 我/刚 e 听/懂. Não crie divisões artificiais para passar no teste.
7. Esses limiares são um critério editorial, não prova de fluência ou de frequência de uma construção inteira. A base wordfreq 3.1.1 contém dados de múltiplas fontes até 2021; não a descreva como corpus de 2026 ou exclusivamente oral. Revise o uso contemporâneo com fontes adequadas, quando necessário. Consulte o Chinese Grammar Wiki para os padrões, sem afirmar que rótulo HSK mede frequência.
8. Faça tradução natural em português e uma nota curta sobre um padrão reutilizável. Verifique pinyin, caracteres polifônicos, palavras neutras e coerência do sentido. O pinyin automático é rascunho, não revisão linguística. A indicação de emoção é orientação, não garantia de atuação da síntese.

## Publicação e progresso

O progresso permanece no localStorage do estudante; nenhuma gravação ou estatística é enviada ao GitHub. A geração semanal não depende de progresso individual. Preserve os IDs, a ordem das frases existentes e os módulos anteriores. Para uma frase com objetivo realmente diferente, use ID novo; uma correção de redação dentro da mesma lição pode preservar o ID.

Antes de publicar, execute `python scripts/content.py`, `python scripts/frequency.py`, `python scripts/validate.py` e `node --test tests/*.test.mjs`. O GitHub gera os MP3 e testa os módulos/áudios públicos. Aguarde o workflow terminar e confirme a etapa `Verify live application and audio`. A aplicação publicada pode ter mais módulos que o agregado versionado se a alteração adicionou apenas a fonte; o build sempre regenera o catálogo a partir das fontes.

O workflow aceita o Pages ativado por branch: espera a publicação nativa terminar antes de colocar a aplicação no ar. Não retire essa proteção ou os nomes únicos dos pacotes de cada tentativa.

## Atualização semanal

Uma automação do ChatGPT acrescenta uma única ilha inédita por execução, domingo às 07:00 em America/Sao_Paulo. Ela deve ler este guia e os módulos, criar conteúdo coerente, publicar no repositório autorizado e verificar o site. Não há coleta de progresso, tokens no front-end ou cron que chame um modelo sem credenciais. Informe no chat o tema, as estruturas reutilizadas e o resultado da publicação. Se já houver ilha criada para a mesma execução/data, verifique-a em vez de duplicá-la.
