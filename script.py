"""
Akinator de Personagens - simula o fluxo do Orange:
File -> Tree -> (perguntas interativas para adivinhar o personagem)

A árvore de decisão é treinada para prever "nome" a partir das
características do personagem. A coluna "genero_filme" é transformada
em várias colunas sim/nao (uma para cada gênero), assim cada pergunta
da árvore é sempre uma pergunta simples sobre uma única característica.
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import os

# ---------- 1. Carregar dados (equivalente ao bloco "File") ----------
diretorio_atual = os.getcwd()

dados = pd.read_csv(os.path.join(diretorio_atual, "akinator_filmes.csv"))

coluna_alvo = "nome"

# Transforma "genero_filme" em colunas sim/nao: genero_acao, genero_aventura, etc.
generos = sorted(dados["genero_filme"].unique())
for genero in generos:
    dados[f"genero_{genero}"] = dados["genero_filme"].apply(
        lambda g, genero=genero: "sim" if g == genero else "nao"
    )

dados = dados.drop(columns=["genero_filme"])

colunas_caracteristicas = [coluna for coluna in dados.columns if coluna != coluna_alvo]

# Todas as colunas restantes são sim/nao, então usamos LabelEncoder em cada uma
codificadores = {}
dados_caracteristicas = dados[colunas_caracteristicas].copy()

for coluna in colunas_caracteristicas:
    codificador = LabelEncoder()
    dados_caracteristicas[coluna] = codificador.fit_transform(
        dados_caracteristicas[coluna]
    )
    codificadores[coluna] = codificador

rotulos = dados[coluna_alvo]

# ---------- 2. Treinar a árvore (equivalente ao bloco "Tree") ----------
arvore_decisao = DecisionTreeClassifier(criterion="entropy", random_state=42)
arvore_decisao.fit(dados_caracteristicas, rotulos)


# ---------- 3. Jogar Akinator percorrendo a árvore ----------
def pergunta_sim_nao(texto):
    while True:
        resposta = input(f"{texto} (sim/nao): ").strip().lower()
        if resposta in ("sim", "s"):
            return "sim"
        if resposta in ("nao", "n"):
            return "nao"
        print("Responda apenas 'sim' (s) ou 'nao' (n).")


def texto_pergunta(coluna):
    if coluna.startswith("genero_"):
        genero = coluna.replace("genero_", "")
        return f"O filme é do gênero {genero}?"
    return f"O personagem se encaixa em: {coluna.replace('_', ' ')}?"


def jogar():
    print("Pense em um personagem do CSV e responda as perguntas!\n")

    estrutura_arvore = arvore_decisao.tree_
    no_atual = 0  # raiz

    while estrutura_arvore.feature[no_atual] != -2:  # -2 = nó folha
        indice_caracteristica = estrutura_arvore.feature[no_atual]
        coluna = colunas_caracteristicas[indice_caracteristica]
        limite = estrutura_arvore.threshold[no_atual]

        resposta = pergunta_sim_nao(texto_pergunta(coluna))
        valor_codificado = codificadores[coluna].transform([resposta])[0]

        # Decide qual caminho seguir na árvore
        if valor_codificado <= limite:
            no_atual = estrutura_arvore.children_left[no_atual]
        else:
            no_atual = estrutura_arvore.children_right[no_atual]

    # Chegou numa folha: pega a classe mais provável
    indice_classe = estrutura_arvore.value[no_atual].argmax()
    nome_previsto = arvore_decisao.classes_[indice_classe]

    print(f"\nEu acho que o personagem é: {nome_previsto}!")


if __name__ == "__main__":
    jogar()
