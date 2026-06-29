# Contractor Scheduler

Número da Lista: 37<br>
Conteúdo da Disciplina: PD (Programação Dinâmica)<br>
Apresentação: [https://youtu.be/GEoPmyxTK2k](https://youtu.be/GEoPmyxTK2k)

## Alunos
| Matrícula | Aluno |
| -- | -- |
| 21/1029512  |  Laís Cecília Soares Paes |
| 22/1008697  |  Sunamita Vitória Rodrigues dos Santos |

## Nota ao prof / monitores

Ambos os integrantes participaram, porém houve um problema com os commits da Sunamita, que não estão atrelados ao seu github

<img width="1290" height="177" alt="image" src="https://github.com/user-attachments/assets/47d59abb-89a6-484d-b1ca-30bf2f9910bb" />


## Sobre
Aplicação do algoritmo **Weighted Interval Scheduling**(modificado) com Programação Dinâmica.

O problema consiste em um empreiteiro que possui uma lista de serviços, cada um com uma janela de tempo disponível (horário em que o cliente está em casa), uma duração e um valor. O objetivo é selecionar quais serviços realizar para **maximizar o valor total**, respeitando que dois serviços não podem ser executados ao mesmo tempo.

A solução utiliza:
- Ordenação dos trabalhos por fim da janela
- **DP recursiva com memoização** para calcular o valor ótimo
- Reconstrução da solução com `find_solution`

## Screenshots

CLI no terminal:
<img width="933" height="501" alt="image" src="https://github.com/user-attachments/assets/ae6c7dbb-6f1c-4746-a0f2-59618e611ece" />

GUI vazia:
<img width="1432" height="958" alt="Screenshot_20260629_184848" src="https://github.com/user-attachments/assets/97541b97-2d0c-4a55-956e-e0a655679b6a" />

GUI com exemplos:

<img width="1505" height="958" alt="Screenshot_20260629_184759" src="https://github.com/user-attachments/assets/944ebb23-6fa6-4d55-9b67-34aa733b1aaa" />

<img width="1505" height="958" alt="Screenshot_20260629_184823" src="https://github.com/user-attachments/assets/0b9ca85d-44e3-484e-9001-b68e72119fd3" />


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
### CLI

<ul>
  
<li> Rodar com exemplo embutido:
```bash
python main.py
```

<li> Rodar com arquivo JSON próprio:
```bash
python main.py [exemplo.json]
```

<li>Opções:
<ul>
<code>python main.py [arquivo] [-q/--quiet] [-s/--scale NUM]</code>
<li> arquivo: o arquivo JSON de entrada
<li> <b>-q</b>/<b>--quiet</b>: não mostra a execução passo-a-passo, somente o resultado
<li> <b>-s</b>/<b>--scale</b>: valor numérico (float ou int) de escala horizontal para a timeline
<li> exemplos:
  <ul>
  <li>  <code>python main.py --scale 2 --quiet</code>: exemplo embutido, sem passo-a-passo e com escala horizontal 2
  <li>  <code>python main.py entradas/exemplos3.json -s 2.5</code>: arquivo de exemplo, com passo-a-passo e com escala horizontal 2.5
  <li>  <code>python main.py ~/caminho/ao/meu_arquivo.json -q</code>: arquivo próprio, sem passo-a-passo e com escala horizontal 1
  <li>  <code>python main.py -qs5 ~caminho/ao/meu/arquivo.json</code>: arquivo próprio, sem passo-a-passo e com escala horizontal 5
  </ul>
</ul>
</ul>

O arquivo JSON de entrada deve seguir o formato a seguir, em que cada objeto `{...}` é um trabalho:
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
### GUI
1. Inicialize a inteface gráfica:
```bash
python gui.py
```
2. Clique em "Carregar arquivo" e selecione uma entrada válida

<img width="1130" height="958" alt="image" src="https://github.com/user-attachments/assets/33ba97ca-809f-4527-a481-c31bbdf97463" />

O arquivo JSON de entrada deve seguir o formato a seguir, em que cada objeto `{...}` é um trabalho:
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
