# Akinator de Filmes 🎬

Esse projeto é uma versão simplificada do Akinator, mas focada apenas em
**personagens de filmes** , a partir de um conjunto de perguntas sim/não.

A ideia é mostrar como uma **árvore de decisão** (Decision Tree), que é o
mesmo tipo de modelo usado no Orange, pode ser usada para "jogar" um jogo de
adivinhação. Cada pergunta que o programa faz corresponde a um nó da árvore,
e suas respostas vão guiando o caminho até chegar numa folha, que é o
personagem adivinhado.

## Como funciona

1. **Dados (`akinator_filmes.csv`)** : cada linha é um personagem, com várias
   colunas sim/não descrevendo características dele (é homem? é vilão
   presente? tem final feliz? etc.) e o gênero do filme.
2. **Treinamento da árvore** : o script carrega esse CSV e treina uma
   `DecisionTreeClassifier` (do scikit-learn) para aprender a relação entre
   essas características e o nome do personagem.
3. **Jogo interativo** : depois de treinada, o programa percorre a árvore do
   topo até uma folha. Em cada nó, ele faz uma pergunta sim/não pra você
   (baseada na característica daquele nó) e usa sua resposta para decidir se
   vai pro ramo da esquerda ou da direita. Quando chega numa folha, ele
   "chuta" o personagem.

Isso é exatamente o que acontece quando você olha pra árvore no **Tree
Viewer** do Orange e vai seguindo os ramos manualmente — só que aqui o
programa faz isso sozinho, perguntando pra você.

## Arquivos

- `script.py` — o script principal, com o treinamento e o jogo.
- `akinator_filmes.csv` — a base de dados com os personagens.
- `requirements.txt` — as bibliotecas Python necessárias.

## Como rodar

1. (Opcional, mas recomendado) Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # no Windows: venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script (certifique-se de que o arquivo `akinator_filmes.csv`
   está na mesma pasta):
   ```bash
   python3 script.py
   ```
4. Pense em um personagem da lista do CSV e vá respondendo as perguntas com
   `sim`/`s` ou `nao`/`n`. No final, o programa vai dizer qual personagem ele
   acha que você escolheu!
