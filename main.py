"""
main.py — ponto de entrada para demonstração e integração com frontend.

Uso:
    python main.py                    # roda exemplo embutido
    python main.py dados.json         # lê trabalhos de um arquivo JSON
"""
import json
import sys

from trabalho import Trabalho
from scheduler import weighted_interval_scheduling


def carregar_de_json(caminho: str) -> list[Trabalho]:
    """Lê lista de trabalhos de um arquivo JSON."""
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    trabalhos = []
    erros = []
    for i, d in enumerate(dados):
        try:
            trabalhos.append(Trabalho.de_dict(d))
        except ValueError as e:
            erros.append(f"  Item {i}: {e}")

    if erros:
        print("⚠ Erros encontrados nos dados de entrada:")
        for e in erros:
            print(e)
        print()

    return trabalhos


def agendar(trabalhos: list[Trabalho], verbose: bool = True):
    """
    Ponto de entrada principal.
    Retorna o objeto Resultado — o frontend pode chamar essa função
    e usar resultado.to_dict() para serializar a resposta.
    """
    if not trabalhos:
        print("Nenhum trabalho válido para agendar.")
        return None

    resultado = weighted_interval_scheduling(trabalhos)

    if verbose:
        resultado.imprimir_resumo()
        resultado.imprimir_timeline()
        resultado.imprimir_log()

    return resultado


# ---------------------------------------------------------------------------
# Exemplo embutido
# ---------------------------------------------------------------------------

EXEMPLO = [
    {"nome": "Pintura da sala",   "duracao": 2, "inicio_janela": 0, "fim_janela": 5,  "valor": 50},
    {"nome": "Encanamento",       "duracao": 3, "inicio_janela": 1, "fim_janela": 7,  "valor": 70},
    {"nome": "Elétrica",          "duracao": 2, "inicio_janela": 4, "fim_janela": 9,  "valor": 30},
    {"nome": "Reforma geral",     "duracao": 4, "inicio_janela": 0, "fim_janela": 10, "valor": 100},
    {"nome": "Jardinagem",        "duracao": 2, "inicio_janela": 6, "fim_janela": 10, "valor": 40},
    {"nome": "Limpeza pós-obra",  "duracao": 1, "inicio_janela": 9, "fim_janela": 12, "valor": 20},
]


def carregar_exemplos() -> list[dict]:
    """
    Retorna a lista de exemplos prontos como dicionários.
    
    O frontend chama essa função no botão 'Carregar exemplo'
    e popula os campos com os valores retornados.
    
    Exemplo de uso no Tkinter:
        def on_carregar():
            exemplos = carregar_exemplos()
            # limpa a tabela atual e preenche com os exemplos
            for ex in exemplos:
                adicionar_linha(ex['nome'], ex['duracao'],
                                ex['inicio_janela'], ex['fim_janela'], ex['valor'])
    """
    return [dict(d) for d in EXEMPLO]  # retorna cópias para não modificar o original


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Lê de arquivo JSON passado como argumento
        caminho = sys.argv[1]
        print(f"Lendo trabalhos de: {caminho}")
        trabalhos = carregar_de_json(caminho)
    else:
        # Usa exemplo embutido
        print("Usando exemplo embutido. Para usar seus dados: python main.py dados.json\n")
        trabalhos = []
        for d in EXEMPLO:
            try:
                trabalhos.append(Trabalho.de_dict(d))
            except ValueError as e:
                print(f"⚠ {e}")

    agendar(trabalhos, verbose=True)
