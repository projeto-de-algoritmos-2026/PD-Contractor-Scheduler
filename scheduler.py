from typing import Optional
from trabalho import Trabalho


# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------

class Resultado:
    """Encapsula tudo que o algoritmo produz."""

    def __init__(self, valor_maximo, escolhidos: list[Trabalho],
                 todos: list[Trabalho], tempos_de_inicio, log: Logger):
        self.valor_maximo = valor_maximo
        self.escolhidos = escolhidos
        self.todos = todos          # lista ordenada por fim_janela
        self.tempos_de_inicio = tempos_de_inicio
        self.log = log.log

    def to_dict(self) -> dict:
        return {
            "valor_maximo": self.valor_maximo,
            "escolhidos": [t.to_dict() for t in self.escolhidos],
            "log": self.log,
        }

    def imprimir_resumo(self):
        print("\n" + "="*55)
        print(f"  Valor máximo obtido : {self.valor_maximo}")
        print(f"  Trabalhos escolhidos: {len(self.escolhidos)}")
        print("="*55)
        for i, t in enumerate(self.escolhidos):
            print(f"  ✔ {t.nome:20s}  janela [{t.inicio_janela}, {t.fim_janela}]"
                  f"  dur={t.duracao}  val={t.valor}  inicio={self.tempos_de_inicio[self.todos.index(t)]}")
        print("="*55)

    def imprimir_log(self):
        print("\n--- LOG DO ALGORITMO ---")
        for linha in self.log:
            print(linha)

    def imprimir_timeline(self, escala: float = 1):
        """
        Imprime uma timeline ASCII mostrando todos os trabalhos e
        marcando com ✔ os que foram escolhidos.

        escala: quantas unidades de tempo cada caractere representa.
        """
        if not self.todos:
            return
        

        escolhidos_nomes = {t.nome for t in self.escolhidos}
        max_fim = self.todos[-1].fim_janela
        largura = int(max_fim / escala) + 1

        print("\n--- TIMELINE ---")
        print("Legenda: [---] janela disponível | [###] duração alocada | ✔ escolhido\n")

        # Cabeçalho de tempo
        header = "".join(f'{i * escala * 5:<5.1f}' for i in range(largura // 5 + 1))
        print(f"{'':22s}{header}")
        print(f"{'':22s}" + "|    " * (largura // 5 + 1))

        for i, t in enumerate(self.todos):
            marcador = "✔" if t.nome in escolhidos_nomes else " "
            linha = [" "] * largura

            # Janela disponível
            ini = int(t.inicio_janela / escala)
            fim = int(t.fim_janela / escala)
            for j in range(ini, fim):
                linha[j] = "-"

            if t in self.escolhidos:
                # Bloco de duração
                dur = int(t.duracao / escala)
                ini = int(self.tempos_de_inicio[i] / escala)
                fim = ini + dur
                for j in range(ini, min(fim, largura)):
                    linha[j] = "#"

            print(f"{marcador} {t.nome:20s}|{''.join(linha)}")

        print()


# ---------------------------------------------------------------------------
# Algoritmo principal
# ---------------------------------------------------------------------------

def _ultimo_compativel(ordenadas: list[Trabalho], inicio_anterior: float) -> int:
    """
    retorna o maior índice j em ordenadas tal que ordenadas[j] pode ser concuido até o tempo inicio_anterior
    ou seja <= ordenadas[j].inicio_janela + ordenadas[j].duracao <= inicio_anterior

    Complexidade: O(n)
    """

    for j in range(len(ordenadas) -1, -1, -1):
        if ordenadas[j].inicio_janela + ordenadas[j].duracao <= inicio_anterior:
            return j

    return -1  # -1 se nenhum compatível



class Logger:
    def __init__(self, active):
        self.active = active
        self.log = []
    
    def logInfo(self, string : str) -> None:
        self.log.append(string)
        if self.active:
            print(string)

def weighted_interval_scheduling(trabalhos: list[Trabalho], log_realtime: bool = True) -> Resultado:
    """
    Weighted Interval Scheduling(modificado) via Programação Dinâmica com memoização.

    Complexidade:
        - Ordenação       : O(n log n)
        - DP recursiva    : O(n^2)
          - Encontrar o último trabalho compatível  : O(n)
        - Reconstrução    : O(n)
        Total             : O(n^2)

    Retorna um objeto Resultado com valor ótimo, trabalhos escolhidos e log.
    """
    log: Logger = Logger(log_realtime)

    # --- Caso vazio ---
    if not trabalhos:
        log.logInfo("Lista de trabalhos vazia. Nada a agendar.")
        return Resultado(0.0, [], [], [], log)

    # --- Ordenação por fim_janela ---
    ordenados = sorted(trabalhos, key=lambda t: t.fim_janela)
    n = len(ordenados)
    log.logInfo(f"Total de trabalhos recebidos: {n}")
    log.logInfo("Ordenados por fim_janela:")
    for i, t in enumerate(ordenados):
        log.logInfo(f"  [{i}] {t.nome}:\n"
                    f"      janela=[{t.inicio_janela},{t.fim_janela}] \n"
                    f"      dur={t.duracao}\n"
                    f"      val={t.valor}\n"
                    f"      deadline={t.deadline}")


    # "fim real" de cada trabalho j = inicio_janela[j] + duracao[j]
    fins_reais = [t.fim_janela - t.duracao for t in ordenados]

    # --- DP com memoização ---
    memo: list[Optional[float]] = [None] * n

    def find_opt(i: int) -> float:
        return _find_opt(i, i, 0)
    def _find_opt(i: int, trab_max_i: int, tempo_comprometido_max: int) -> float:
        if i < 0:
            return 0.0
        if memo[i] is not None:
            return memo[i]
        if i == trab_max_i:
            tempo_comprometido_max = ordenados[i].fim_janela

        tempo_inicia_trabalho = min(tempo_comprometido_max - ordenados[i].duracao, fins_reais[i])

        ultimo_compativel = _ultimo_compativel(ordenados[:i], tempo_inicia_trabalho)

        log.logInfo(
            f'  find_opt({i}):\n'
            f'      compromisso = {tempo_comprometido_max}\n'
            f'      inicio = {tempo_inicia_trabalho}\n'
            f'      {ultimo_compativel = }'
        )


        val_pega    = ordenados[i].valor + _find_opt(ultimo_compativel, trab_max_i, tempo_inicia_trabalho)
        val_nao_pega = _find_opt(i - 1, trab_max_i, tempo_comprometido_max)


        memo[i] = max(val_pega, val_nao_pega)

        log.logInfo(f"  OPT({i}={ordenados[i].nome}):\n"
                   f"       pega={val_pega:.2f}\n"
                   f"       não_pega={val_nao_pega:.2f}\n"
                   f"       {"PEGA" if val_pega > val_nao_pega else "NÃO PEGA"}")
        return memo[i]

    log.logInfo("\nComputando OPT (memorização):")
    find_opt(n - 1)

    # --- Reconstrução da solução ---
    start: list[Optional[float]] = [None] * n
    def find_solution(i: int):
        return _find_solution(i, ordenados[-1].fim_janela)
    def _find_solution(i: int, tempo_comprometido_max: int) -> list[Trabalho]:
        if i < 0:
            return []
        
        tempo_inicia_trabalho = min(tempo_comprometido_max - ordenados[i].duracao, fins_reais[i])
        ultimo_compativel = _ultimo_compativel(ordenados[:i], tempo_inicia_trabalho)

        val_pega = ordenados[i].valor + (memo[ultimo_compativel] if ultimo_compativel >= 0 else 0)
        val_nao_pega = memo[i-1] if  i-1 > 0 else 0

        # print(f'{i=} - {val_pega=} - {val_nao_pega=}')

        if val_pega > val_nao_pega:
            log.logInfo(f"  [{i}] - {ordenados[i].nome}")
            start[i] = tempo_inicia_trabalho
            return _find_solution(ultimo_compativel, tempo_inicia_trabalho) + [ordenados[i]]
        else:
            return _find_solution(i-1, tempo_comprometido_max)

    log.logInfo("\nReconstruindo solução:")
    escolhidos = find_solution(n - 1)
    valor_maximo = memo[n - 1]

    log.logInfo(f"\nValor alcançado: {valor_maximo}")

    return Resultado(valor_maximo, escolhidos, ordenados, start, log)
