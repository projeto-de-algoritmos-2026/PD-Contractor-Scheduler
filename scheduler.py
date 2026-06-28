import bisect
from typing import Optional
from trabalho import Trabalho


# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------

class Resultado:
    """Encapsula tudo que o algoritmo produz."""

    def __init__(self, valor_maximo: float, escolhidos: list[Trabalho],
                 todos: list[Trabalho], log: list[str]):
        self.valor_maximo = valor_maximo
        self.escolhidos = escolhidos
        self.todos = todos          # lista ordenada por fim_janela
        self.log = log

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
        for t in self.escolhidos:
            print(f"  ✔ {t.nome:20s}  janela [{t.inicio_janela}, {t.fim_janela}]"
                  f"  dur={t.duracao}  val={t.valor}")
        print("="*55)

    def imprimir_log(self):
        print("\n--- LOG DO ALGORITMO ---")
        for linha in self.log:
            print(linha)

    def imprimir_timeline(self, escala: int = 1):
        """
        Imprime uma timeline ASCII mostrando todos os trabalhos e
        marcando com ✔ os que foram escolhidos.

        escala: quantas unidades de tempo cada caractere representa.
        """
        if not self.todos:
            return

        escolhidos_nomes = {t.nome for t in self.escolhidos}
        max_fim = max(t.fim_janela for t in self.todos)
        largura = int(max_fim / escala) + 1

        print("\n--- TIMELINE ---")
        print("Legenda: [===] janela disponível | [###] duração alocada | ✔ escolhido\n")

        # Cabeçalho de tempo
        header = "".join(str(i * escala).ljust(5) for i in range(largura // 5 + 1))
        print(f"{'':22s}{header}")
        print(f"{'':22s}" + "|    " * (largura // 5 + 1))

        for t in self.todos:
            marcador = "✔" if t.nome in escolhidos_nomes else " "
            linha = [" "] * largura

            # Janela disponível
            ini = int(t.inicio_janela / escala)
            fim = int(t.fim_janela / escala)
            for i in range(ini, fim):
                linha[i] = "-"

            # Bloco de duração (começa no início da janela)
            dur = int(t.duracao / escala)
            for i in range(ini, min(ini + dur, largura)):
                linha[i] = "#"

            print(f"{marcador} {t.nome:20s}|{''.join(linha)}")

        print()


# ---------------------------------------------------------------------------
# Algoritmo principal
# ---------------------------------------------------------------------------

def _ultimo_compativel_binario(deadlines: list[float], fim_anterior: float) -> int:
    """
    Busca binária: retorna o maior índice j tal que
    deadlines[j] (= inicio_j + duracao_j, i.e., quando j termina)
    seja <= fim_anterior.

    Complexidade: O(log n)
    """
    # deadlines aqui guarda o "fim real" de cada trabalho ordenado
    idx = bisect.bisect_right(deadlines, fim_anterior) - 1
    return idx  # -1 se nenhum compatível


def weighted_interval_scheduling(trabalhos: list[Trabalho]) -> Resultado:
    """
    Weighted Interval Scheduling via Programação Dinâmica com memoização.

    Complexidade:
        - Ordenação       : O(n log n)
        - Pré-cômputo p[] : O(n log n)  ← busca binária
        - DP recursiva    : O(n)
        - Reconstrução    : O(n)
        Total             : O(n log n)

    Retorna um objeto Resultado com valor ótimo, trabalhos escolhidos e log.
    """
    log: list[str] = []

    # --- Caso vazio ---
    if not trabalhos:
        log.append("Lista de trabalhos vazia. Nada a agendar.")
        return Resultado(0.0, [], [], log)

    # --- Ordenação por fim_janela ---
    ordenados = sorted(trabalhos, key=lambda t: t.fim_janela)
    n = len(ordenados)
    log.append(f"Total de trabalhos recebidos: {n}")
    log.append("Ordenados por fim_janela:")
    for i, t in enumerate(ordenados):
        log.append(f"  [{i}] {t.nome}: janela=[{t.inicio_janela},{t.fim_janela}] "
                   f"dur={t.duracao} val={t.valor} deadline={t.deadline}")

    # --- Pré-cômputo de p[i]: último compatível com i ---
    # "fim real" de cada trabalho j = inicio_janela[j] + duracao[j]
    # trabalho j é compatível com i se j termina <= inicio de i
    fins_reais = [t.inicio_janela + t.duracao for t in ordenados]

    p: list[int] = []
    log.append("\nPré-cômputo de p[i] (último compatível via busca binária):")
    for i in range(n):
        # trabalho i começa no mais cedo em inicio_janela[i]
        idx = _ultimo_compativel_binario(fins_reais, ordenados[i].inicio_janela)
        # garante que não aponta pra si mesmo
        if idx >= i:
            idx = i - 1
        p.append(idx)
        compat_nome = ordenados[idx].nome if idx >= 0 else "nenhum"
        log.append(f"  p[{i}] ({ordenados[i].nome}) = {idx} ({compat_nome})")

    # --- DP com memoização ---
    memo: list[Optional[float]] = [None] * n

    def find_opt(i: int) -> float:
        if i < 0:
            return 0.0
        if memo[i] is not None:
            return memo[i]

        val_pega    = ordenados[i].valor + find_opt(p[i])
        val_nao_pega = find_opt(i - 1)

        memo[i] = max(val_pega, val_nao_pega)
        log.append(f"  OPT({i}={ordenados[i].nome}): "
                   f"pega={val_pega:.2f} | não_pega={val_nao_pega:.2f} "
                   f"→ memo={memo[i]:.2f}")
        return memo[i]

    log.append("\nComputando OPT (memoização):")
    find_opt(n - 1)

    # --- Reconstrução da solução ---
    def find_solution(i: int) -> list[Trabalho]:
        if i < 0:
            return []
        val_pega = ordenados[i].valor + (memo[p[i]] if p[i] >= 0 else 0.0)
        val_nao_pega = memo[i - 1] if i > 0 else 0.0

        if val_pega >= val_nao_pega:
            log.append(f"  find_solution({i}={ordenados[i].nome}): ESCOLHIDO")
            return find_solution(p[i]) + [ordenados[i]]
        else:
            log.append(f"  find_solution({i}={ordenados[i].nome}): pulado")
            return find_solution(i - 1)

    log.append("\nReconstruindo solução:")
    escolhidos = find_solution(n - 1)
    valor_maximo = memo[n - 1]

    log.append(f"\nValor máximo: {valor_maximo}")
    log.append(f"Trabalhos escolhidos: {[t.nome for t in escolhidos]}")

    return Resultado(valor_maximo, escolhidos, ordenados, log)
