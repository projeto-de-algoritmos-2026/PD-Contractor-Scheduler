class Trabalho:
    """
    Representa um trabalho/serviço com janela de tempo, duração e valor.

    Atributos:
        nome          (str)   : identificador do trabalho
        duracao       (float) : tempo necessário para executar
        inicio_janela (float) : momento mais cedo que pode começar
        fim_janela    (float) : momento mais tarde que o trabalho pode ser CONCLUÍDO
        valor         (float) : ganho obtido ao realizar o trabalho

    Propriedade derivada:
        deadline : último momento em que pode COMEÇAR (fim_janela - duracao)
    """

    def __init__(self, nome: str, duracao: float, inicio_janela: float,
                 fim_janela: float, valor: float):
        self._validar(nome, duracao, inicio_janela, fim_janela, valor)
        self.nome = nome
        self.duracao = duracao
        self.inicio_janela = inicio_janela
        self.fim_janela = fim_janela
        self.valor = valor
        self.deadline = fim_janela - duracao  # último instante para começar

    @staticmethod
    def _validar(nome, duracao, inicio_janela, fim_janela, valor):
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome deve ser uma string não vazia.")
        if duracao <= 0:
            raise ValueError(f"[{nome}] Duração deve ser positiva. Recebido: {duracao}")
        if inicio_janela < 0:
            raise ValueError(f"[{nome}] Início da janela não pode ser negativo. Recebido: {inicio_janela}")
        if fim_janela <= inicio_janela:
            raise ValueError(f"[{nome}] fim_janela ({fim_janela}) deve ser maior que inicio_janela ({inicio_janela}).")
        if duracao > (fim_janela - inicio_janela):
            raise ValueError(
                f"[{nome}] Trabalho não cabe na janela: duração {duracao} > "
                f"tamanho da janela {fim_janela - inicio_janela}."
            )
        if valor <= 0:
            raise ValueError(f"[{nome}] Valor deve ser positivo. Recebido: {valor}")

    @classmethod
    def de_dict(cls, d: dict) -> "Trabalho":
        """Cria um Trabalho a partir de um dicionário (útil para JSON)."""
        try:
            return cls(
                nome=d["nome"],
                duracao=d["duracao"],
                inicio_janela=d["inicio_janela"],
                fim_janela=d["fim_janela"],
                valor=d["valor"],
            )
        except KeyError as e:
            raise ValueError(f"Campo obrigatório ausente no dicionário: {e}")

    def to_dict(self) -> dict:
        """Serializa o trabalho para dicionário (útil para JSON)."""
        return {
            "nome": self.nome,
            "duracao": self.duracao,
            "inicio_janela": self.inicio_janela,
            "fim_janela": self.fim_janela,
            "valor": self.valor,
            "deadline": self.deadline,
        }

    def __repr__(self):
        return (f"Trabalho(nome='{self.nome}', duracao={self.duracao}, "
                f"janela=[{self.inicio_janela}, {self.fim_janela}], "
                f"deadline={self.deadline}, valor={self.valor})")
