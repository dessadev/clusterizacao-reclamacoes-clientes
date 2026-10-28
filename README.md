# Clusterização de reclamações de clientes com HDBSCAN e K-means

Agrupamento de reclamações de clientes em grupos de problemas parecidos, separação do ruído e escolha da **reclamação mais representativa** de cada grupo, que pode orientar o time de atendimento ou alimentar um agente de IA.

> ⚠️ Os textos são **sintéticos**, gerados em [`src/gerar_textos.py`](src/gerar_textos.py): 1.500 reclamações de clientes de uma loja online em 6 temas e 120 mensagens genéricas que fazem papel de ruído. Nenhum dado real é usado. O tema real só é usado no fim, para avaliar o resultado.

## Problema

Ninguém rotula de que tipo é cada reclamação que chega. Sem rótulo, o caminho é o **aprendizado não supervisionado**: deixar os dados mostrarem quais grupos existem.

## Abordagem

| Etapa | Técnica | Por quê |
|---|---|---|
| Texto em vetores | TF-IDF + SVD (análise semântica latente) | aproxima textos com significado parecido, na ideia de *embeddings* |
| Quantos grupos existem? | **HDBSCAN** | descobre o número de grupos sozinho, aceita formatos diferentes e separa o ruído |
| Quem representa cada grupo? | **K-means** nos pontos sem ruído | a reclamação mais próxima do centroide é a mais representativa |
| Avaliação | Adjusted Rand Index, silhouette | compara com o tema real e mede a separação |

Os vetores são normalizados para que a distância se comporte como a **similaridade de cosseno**. O canal de contato e as palavras de urgência ("urgente", "pela segunda vez") saem do vocabulário, porque dizem *como* o cliente reclamou, não *do que* reclamou.

## Resultados

- **8 grupos** encontrados sem informar o número de grupos
- **Adjusted Rand Index de 0,82** entre os grupos e os temas reais
- **Silhouette de 0,60**
- **88% das mensagens genéricas** separadas como ruído

Exemplos de reclamações representativas:

| Termos principais | Reclamação representativa |
|---|---|
| app, aplicativo, fechando sozinho | app travando na tela inicial |
| cobrança duplicada, não reconhecida | cobrança duplicada no pagamento |
| entrega, rastreio parado, prazo | pedido atrasado na entrega |
| chat, suporte, sem solução | chat encerrado sem solução na central de ajuda |

## Aprendizados

- Cada algoritmo responde a uma pergunta: o HDBSCAN diz **quais grupos existem** e o K-means diz **quem representa cada um**.
- **Limpar o vocabulário importa:** na primeira versão, frases como "já reclamei antes" formavam grupos próprios. Removendo as palavras de urgência, o ARI subiu de 0,65 para 0,82.
- **Limite do TF-IDF:** um grupo juntou "valor cobrado errado" e "entregue no endereço errado" por causa da palavra "errado". Embeddings de um modelo de linguagem separariam pelo significado.
- Cobrança se dividiu em subgrupos (duplicada, estorno, valor errado), o que pode ser útil para o atendimento.

## Limitações e próximos passos

- Textos reais têm gírias, abreviações, erros de digitação e emojis.
- Trocar TF-IDF + SVD por embeddings de um modelo de linguagem (por exemplo, `sentence-transformers`).
- Validar os grupos com o time de atendimento e monitorar o surgimento de grupos novos.

## Como rodar

```bash
pip install -r requirements.txt
jupyter notebook clusterizacao_reclamacoes.ipynb
```

---
Feito por [Andressa Prudente](https://github.com/dessadev)
