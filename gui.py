import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from trabalho import *
from scheduler import weighted_interval_scheduling, Resultado
from main import carregar_de_json

class RefinedGraphApp:
    def __init__(self, root):
        plt.style.use('ggplot')
        self.root = root
        self.root.title("Projeto Algoritmos - Agendador para empreiteiros")
        self.root.geometry("1000x800") # Janela maior para acomodar os gráficos
        self.root.configure(bg="#f5f5f5")

        self.caminho_arquivo = ""
        self.resultado: Resultado | None = None
    
        self.header_frame = tk.Frame(root, bg="#f5f5f5")
        self.header_frame.pack(pady=10)
        # tk.Label(self.header_frame, 
        #          font=("Segoe UI", 18, "bold"), bg="#f5f5f5", fg="#333").pack()

   
        self.ctrl_frame = tk.Frame(root, width=250, bg="white", relief=tk.RIDGE, borderwidth=1)
        self.ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)
        self.ctrl_frame.pack_propagate(False) # Mantém tamanho fixo

        tk.Label(self.ctrl_frame, text="Controles", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=10)
        
        self.btn_carregar = tk.Button(self.ctrl_frame, text="📂 Carregar arquivo", 
                                      command=self.acao_carregar, font=("Segoe UI", 10))
        self.btn_carregar.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(self.ctrl_frame, text="Log de Análise", font=("Segoe UI", 10), bg="white").pack(pady=(20, 5))
        self.log_area = scrolledtext.ScrolledText(self.ctrl_frame, height=25, font=("Consolas", 9))
        self.log_area.pack(padx=10, pady=(5,30), fill=tk.BOTH, expand=True)
        self.log_area.insert(tk.END, "Aguardando arquivo...\n")

       
        self.plot_frame = tk.Frame(root, bg="#e0e0e0")
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

       
        self.fig, self.ax = plt.subplots(dpi=100)
        self.fig.tight_layout(pad=0.0)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.configurar_eixos_iniciais() 

    #  Funções de Interface 

    def configurar_eixos_iniciais(self):
        # Limpa e coloca títulos padrão
        self.ax.clear()
        self.ax.axis('off')
        
        self.canvas.draw()

    def update_log(self, text, type="normal"):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END) # Scroll automático

  

    def acao_carregar(self):
        self.caminho_arquivo = filedialog.askopenfilename(filetypes=[("arquivos JSON", "*.json"), ("Todos os arquivos", "*")])
        if self.caminho_arquivo:
            try:
                self.log_area.delete(1.0, tk.END)
                fname = self.caminho_arquivo.split('/')[-1]
                self.update_log(f"✅ Arquivo carregado: {fname}")
                
                self.configurar_eixos_iniciais()

                # Pré-carrega o grafo para ver se está lendo ok
                self.resultado = weighted_interval_scheduling(carregar_de_json(self.caminho_arquivo))
                self.update_log("\n".join(self.resultado.log))

            except Exception as e:
                messagebox.showerror("Erro de Leitura", f"Erro ao ler arquivo:\n{str(e)}")
        self.desenhar_grafos()
    
    # Funções de Plotagem 

    def desenhar_grafos(self):

        self.ax.clear()
        self.ax.set_title(f"Agenda Planejada (valor: {self.resultado.valor_maximo:.2f})")

        data = [(j.inicio_janela, self.resultado.tempos_de_inicio[self.resultado.todos.index(j)], self.resultado.tempos_de_inicio[self.resultado.todos.index(j)] + (j.duracao) / 2, self.resultado.tempos_de_inicio[self.resultado.todos.index(j)] + j.duracao, j.fim_janela) for j in self.resultado.escolhidos]


        rank_mul = 4
        width=3
        positions = []
        ranks = []

        for j in self.resultado.escolhidos:
            if not positions:
                positions.append(rank_mul)
                ranks.append(j)
                continue
            
            for i, r in enumerate(ranks):
                if j.inicio_janela >= r.fim_janela:
                    ranks[i] = j
                    positions.append((i + 1) * rank_mul)
                    break
            else:
                positions.append((len(ranks) + 1) * rank_mul)
                ranks.append(j)


        for i in range(len(data)):
            self.ax.boxplot([data[i]],
                            positions=[positions[i]],
                            label= 'teste',
                            whis= 100,
                            patch_artist=True,
                            medianprops={"color": "white", "linewidth": 0},
                            boxprops={"facecolor": "C" + str(i), "edgecolor": "white",
                                    "linewidth": 0},
                            widths=width,
                            orientation='horizontal')

        ylim = (0 - rank_mul, max(positions) + rank_mul * 2)

        rightend = max([j.fim_janela for j in self.resultado.escolhidos])
        leftend = min([j.inicio_janela for j in self.resultado.escolhidos])

        self.ax.set(xlim=(leftend - 0.5, rightend + 0.5), xticks=range(int(leftend), int(rightend + 1)),
            ylim=ylim)

        self.ax.set_yticks([])

        fontsize = 12

        for i in range(len(data)):
            plt.text(data[i][2], positions[i], self.resultado.escolhidos[i].nome, ha='center', va='center', color = 'black', fontsize=fontsize)

        self.fig.tight_layout()
        self.canvas.draw()

def stop():
    root.destroy()
    root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    # Tenta definir um ícone padrão do Windows para bolinha, se falhar, ok
    try: root.iconbitmap(None) 
    except: pass
    app = RefinedGraphApp(root)
    root.protocol("WM_DELETE_WINDOW", stop)
    root.mainloop()
