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


def agendar(trabalhos: list[Trabalho], scale, quiet, verbose: bool = True):
    """
    Ponto de entrada principal.
    Retorna o objeto Resultado — o frontend pode chamar essa função
    e usar resultado.to_dict() para serializar a resposta.
    """
    if not trabalhos:
        print("Nenhum trabalho válido para agendar.")
        return None

    resultado = weighted_interval_scheduling(trabalhos, not quiet)

    if verbose:
        resultado.imprimir_resumo()
        resultado.imprimir_timeline(scale)

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

class IllegalArgumentError(ValueError):
    pass


if __name__ == "__main__":
    scale = 1.0
    caminho = ''
    quiet = False

    argc = len(sys.argv)
    # if argc > 1:
    i = 1
    while i < argc:
        if sys.argv[i].startswith('--'):
            match sys.argv[i]:
                case '--scale':
                    try:
                        scale = float(sys.argv[i+1])
                    except ValueError, IndexError:
                        print(f'Could not get value of option --scale')
                        raise
                    i += 1
                case '--quiet':
                    quiet = True
                case _:
                    raise IllegalArgumentError(f'Unknown option or flag: {sys.argv[i]}')
        elif sys.argv[i].startswith('-'):
            c = 1
            while c < len(sys.argv[i]):
                match sys.argv[i][c]:
                    case 'q':
                        quiet = True
                    case 's':
                        if c + 1 == len(sys.argv[i]):
                            try:
                                scale = float(sys.argv[i+1])
                            except ValueError, IndexError:
                                print(f'Could not get value of option -s')
                                raise
                            i += 1
                            break
                        else:
                            try:
                                scale = float(sys.argv[i][c+1:])
                            except ValueError:
                                print(f'Could not get attached value of option -s ({sys.argv[i][c+1:]})')
                                raise
                            break
                    case _:
                        raise IllegalArgumentError(f'Unknown option or flag: -{sys.argv[i][c]}')

                c += 1
        else:
            caminho = sys.argv[i]
        i += 1


    # #     # Lê de arquivo JSON passado como argumento
    # #     caminho = sys.argv[1]
    # #     print(f"Lendo trabalhos de: {caminho}")
    # #     if argc > 2:
    # #         try:
    # #             scale = float(sys.argv[2])
    # #         except TypeError:
    # #             print("Valor inválido para escala, deve ser float")
    # #             raise
    # #     trabalhos = carregar_de_json(caminho)
    # else:
    #     # Usa exemplo embutido, com escala 1
    #     print("Usando exemplo embutido. Para usar seus dados: python main.py dados.json\n")
    #     trabalhos = []
    #     for d in EXEMPLO:
    #         try:
    #             trabalhos.append(Trabalho.de_dict(d))
    #         except ValueError as e:
    #             print(f"⚠ {e}")

    trabalhos: list[Trabalho]

    if caminho:
        trabalhos = carregar_de_json(caminho)
    else:
        trabalhos = []
        for d in EXEMPLO:
            try:
                trabalhos.append(Trabalho.de_dict(d))
            except ValueError as e:
                print(f"⚠ {e}")

    agendar(trabalhos, 1 / scale, quiet, verbose=True)
