"""
Testes para Weighted Interval Scheduling.
Execute com: python -m pytest tests.py -v
"""
import pytest
from trabalho import Trabalho
from scheduler import weighted_interval_scheduling


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make(nome, dur, ini, fim, val):
    return Trabalho(nome, dur, ini, fim, val)


# ---------------------------------------------------------------------------
# Testes de Trabalho (validação)
# ---------------------------------------------------------------------------

class TestTrabalho:

    def test_criacao_valida(self):
        t = make("A", 2, 0, 5, 100)
        assert t.deadline == 3

    def test_duracao_zero(self):
        with pytest.raises(ValueError, match="Duração"):
            make("A", 0, 0, 5, 100)

    def test_duracao_negativa(self):
        with pytest.raises(ValueError, match="Duração"):
            make("A", -1, 0, 5, 100)

    def test_inicio_negativo(self):
        with pytest.raises(ValueError, match="negativo"):
            make("A", 1, -1, 5, 100)

    def test_fim_menor_que_inicio(self):
        with pytest.raises(ValueError, match="fim_janela"):
            make("A", 1, 5, 3, 100)

    def test_nao_cabe_na_janela(self):
        with pytest.raises(ValueError, match="não cabe"):
            make("A", 10, 0, 5, 100)

    def test_valor_zero(self):
        with pytest.raises(ValueError, match="Valor"):
            make("A", 1, 0, 5, 0)

    def test_nome_vazio(self):
        with pytest.raises(ValueError, match="Nome"):
            make("", 1, 0, 5, 100)

    def test_de_dict(self):
        d = {"nome": "X", "duracao": 2, "inicio_janela": 0, "fim_janela": 5, "valor": 10}
        t = Trabalho.de_dict(d)
        assert t.nome == "X"

    def test_de_dict_campo_faltando(self):
        with pytest.raises(ValueError, match="Campo"):
            Trabalho.de_dict({"nome": "X"})

    def test_to_dict(self):
        t = make("A", 2, 0, 5, 50)
        d = t.to_dict()
        assert d["deadline"] == 3


# ---------------------------------------------------------------------------
# Testes do Algoritmo
# ---------------------------------------------------------------------------

class TestScheduler:

    def test_lista_vazia(self):
        r = weighted_interval_scheduling([])
        assert r.valor_maximo == 0
        assert r.escolhidos == []

    def test_um_trabalho(self):
        r = weighted_interval_scheduling([make("A", 2, 0, 5, 100)])
        assert r.valor_maximo == 100
        assert len(r.escolhidos) == 1

    def test_dois_compativeis(self):
        """Dois trabalhos que cabem juntos: devem ser ambos escolhidos."""
        t1 = make("Manhã",  2, 0, 4, 30)
        t2 = make("Tarde",  2, 4, 8, 40)
        r = weighted_interval_scheduling([t1, t2])
        assert r.valor_maximo == 70
        nomes = {t.nome for t in r.escolhidos}
        assert nomes == {"Manhã", "Tarde"}

    def test_dois_incompativeis_escolhe_maior(self):
        """Dois trabalhos sobrepostos: escolhe o de maior valor."""
        t1 = make("Barato",  4, 0, 6, 10)
        t2 = make("Caro",    3, 2, 6, 90)
        r = weighted_interval_scheduling([t1, t2])
        assert r.valor_maximo == 90
        assert r.escolhidos[0].nome == "Caro"

    # O CASO DE TESTE FOI FORMULADO INCORRETAMENTE
    # def test_caso_classico_livro(self):
    #     """
    #     Exemplo clássico do KT (Kleinberg & Tardos):
    #     4 trabalhos onde a solução ótima não é gulosa por valor.
    #     """
    #     trabalhos = [
    #         make("J1", 3, 0,  3, 3),
    #         make("J2", 3, 1,  4, 4),  # se pegar J2, perde J1 e J3
    #         make("J3", 3, 3,  6, 3),
    #         make("J4", 5, 0, 10, 8),  # bloqueia tudo mas vale menos que J1+J3
    #     ]
    #     r = weighted_interval_scheduling(trabalhos)
    #     # J1 + J3 = 6 > J2 = 4 > J4 = 8? Não: J4=8 > J1+J3=6
    #     assert r.valor_maximo == 8
    #     assert r.escolhidos[0].nome == "J4"

    def test_empate_de_valor(self):
        """Empate: qualquer escolha com valor igual é válida."""
        t1 = make("A", 3, 0, 4, 50)
        t2 = make("B", 3, 0, 4, 50)
        r = weighted_interval_scheduling([t1, t2])
        assert r.valor_maximo == 50
        assert len(r.escolhidos) == 1

    def test_todos_incompativeis(self):
        """N trabalhos todos sobrepostos: escolhe o de maior valor."""
        trabalhos = [
            make("A", 5, 0, 8, 10),
            make("B", 5, 1, 8, 20),
            make("C", 5, 2, 8, 99),
        ]
        r = weighted_interval_scheduling(trabalhos)
        assert r.valor_maximo == 99

    def test_solucao_nao_gulosa(self):
        """
        Caso onde algoritmo guloso por valor falharia:
        um trabalho de alto valor bloqueia dois de valor médio.
        """
        trabalhos = [
            make("Alto",  6, 0, 6, 10),
            make("Meio1", 2, 0, 2,  6),
            make("Meio2", 2, 2, 4,  6),
            make("Meio3", 2, 4, 6,  6),
        ]
        r = weighted_interval_scheduling(trabalhos)
        # Alto=10, Meio1+Meio2+Meio3=18 → ótimo é 18
        assert r.valor_maximo == 18
        nomes = {t.nome for t in r.escolhidos}
        assert nomes == {"Meio1", "Meio2", "Meio3"}

    def test_trabalho_duracao_igual_janela(self):
        """Trabalho que ocupa exatamente a janela inteira."""
        t = make("Exato", 5, 0, 5, 100)
        r = weighted_interval_scheduling([t])
        assert r.valor_maximo == 100

    def test_log_gerado(self):
        """Log deve conter entradas."""
        r = weighted_interval_scheduling([make("A", 1, 0, 5, 10)])
        assert len(r.log) > 0

    def test_resultado_to_dict(self):
        """to_dict deve serializar corretamente."""
        r = weighted_interval_scheduling([make("A", 1, 0, 5, 10)])
        d = r.to_dict()
        assert "valor_maximo" in d
        assert "escolhidos" in d
        assert "log" in d

    def test_grande_entrada(self):
        """Verifica que O(n log n) aguenta sem estourar recursão."""
        import sys
        sys.setrecursionlimit(10000)
        # 500 trabalhos não sobrepostos
        trabalhos = [make(f"T{i}", 1, i, i+1, i+1) for i in range(500)]
        r = weighted_interval_scheduling(trabalhos)
        assert r.valor_maximo == sum(i+1 for i in range(500))
        assert len(r.escolhidos) == 500


# ---------------------------------------------------------------------------
# Rodar direto
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
