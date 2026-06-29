# Contractor Scheduler

Número da Lista: 37<br>
Conteúdo da Disciplina: PD (Programação Dinâmica)<br>

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 21/1029512  |  Laís Cecília Soares Paes |
| 22/1008697  |  Sunamita Vitória Rodrigues dos Santos |

## Sobre
Aplicação do algoritmo **Weighted Interval Scheduling**(modificado) com Programação Dinâmica.

O problema consiste em um empreiteiro que possui uma lista de serviços, cada um com uma janela de tempo disponível (horário em que o cliente está em casa), uma duração e um valor. O objetivo é selecionar quais serviços realizar para **maximizar o valor total**, respeitando que dois serviços não podem ser executados ao mesmo tempo.

A solução utiliza:
- Ordenação dos trabalhos por fim da janela
- **DP recursiva com memoização** para calcular o valor ótimo
- Reconstrução da solução com `find_solution`

## Screenshots
_Adicione screenshots após rodar o projeto._

## Instalação
Linguagem: Python 3.10+<br>
Framework: Tkinter(somente GUI)<br>

Clone o repositório e entre na pasta:
```bash
git clone https://github.com/projeto-de-algoritmos-2026/PD-Contractor-Scheduler
cd PD-Contractor-Scheduler
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso
Rodar com exemplo embutido:
```bash
python main.py
```

Rodar com arquivo JSON próprio:
```bash
python main.py [exemplo.json]
```

O arquivo JSON deve seguir o formato:
```json
[
  {
    "nome": "Pintura da sala",
    "duracao": 2,
    "inicio_janela": 0,
    "fim_janela": 5,
    "valor": 50
  },
  ...
]
```

Rodar a inteface gráfica:
```bash
python gui.py
```

## Outros
O projeto inclui uma suíte de testes (`tests.py`) cobrindo casos como lista vazia, trabalhos incompatíveis, empates de valor e o caso clássico onde a solução gulosa por valor falha.

Para rodar os testes:

- Instale a framework de testes pytest:

```bash
pip install pytest
```

- Execute os testes

```bash
python tests.py
```
