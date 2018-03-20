# How to make

## Baixar e ajustar os dados do projeto

- Fazer um FORK do projeto, para que modificações futuras não alterem nos resultados
- Extrair os commits para o sqlite (como em <https://gitlab.com/rodrigorgs/msr17-challenge/tree/master#get-information-from-repository>)
- O DB com os commits do projeto tem que ser copiados para `minning-util-codes/DBs/project_name`

### Dividir os intervalos e criar as branches

- O projeto tem que estar na pasta `minning-util-codes/projects/project_name`
- Execute:
1. `minning-util-codes/src/divide-in-intervals.py PROJECT_NAME`: pega o DB da ultima versão do projeto e divide e tenta dividir os commits em branches de 200. Caso não der certo 200, ele pega o número maior e mais próximo de 200.
2. `minning-util-codes/src/remove-duplicated.py PROJECT_NAME`: para retirar de uma parte os commits que tem na parte anterior.
3. `minning-util-codes/src/create-branches.py PROJECT_NAME`: cria as branches do ultimo commit do intervalo.

### Sentiment analysis

- Primeiro, baixe os dados de sentistrength: http://sentistrength.wlv.ac.uk/
- Baixe a ferramenta Java do sentistrength: http://gateway.path.berkeley.edu:8080/artifactory/list/release-local/com/sentistrength/sentistrength/0.1/sentistrength-0.1.jar
- Extraia os dados de sentistrength para `sentment-analysis/data/sentistrength/sentistrength_data/`. E mova a ferramenta Java sentistrength para `sentment-analysis/data/sentistrength/`.
- Renomear `data/sentistrength/sentistrength_data/EmotionLookupTable.txt` para `data/sentistrength/sentistrength_data/EmotionLookupTable-old.txt`.
- Copiar o arquivo de palavras neutras para `data/sentistrength/words-neutral.txt`
- Execute:
1. `sentiment-analysis/src/filter-wordlist.py`: remover as palavras que são específicas do contexto.
2. `sentiment-analysis/src/from-sqlite-to-file.py PROJECT_NAME`: para que o sentistrength possa analisar as mensagens, é necessário que todas as mensagens estejam em um único arquivo, um por linha.
3. `sentiment-analysis/src/compute-sentiment.py PROJECT_NAME`: para computar os sentimentos nas partes.
4. `sentiment-analysis/src/put-sentiments-in-sqlite.py PROJECT_NAME`: converter os sentimntos do arquivo gerado no passo anterior em uma tabela, com os sentimentos para cada commit.
5. `sentiment-analysis/src/sort-commits.py PROJECT_NAME`: classifica as mensagens em "positivo", "negativo" ou "neutro" e gera um CSV com as informações das quantidades para cada parte.

### Get refactorations

1. `minning-util-codes/src/clone-branches.py`: baixar cada parte (branch) do repositório remoto em uma pasta diferente.