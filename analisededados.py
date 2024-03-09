import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from pandastable import Table, TableModel

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análise de Dados")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        
        self.load_button = tk.Button(self.frame, text="Carregar Dados", command=self.load_data)
        self.load_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.select_columns_label = tk.Label(self.frame, text="Selecione Colunas:")
        self.select_columns_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.selected_columns = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=30, height=5)
        self.selected_columns.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        self.analyze_button = tk.Button(self.frame, text="Analisar Dados", command=self.analyze_data)
        self.analyze_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        
        self.plot_button = tk.Button(self.frame, text="Plotar Gráfico", command=self.plot_data)
        self.plot_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        
        self.show_data_button = tk.Button(self.frame, text="Mostrar Dados", command=self.show_data)
        self.show_data_button.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        
        self.save_analysis_button = tk.Button(self.frame, text="Salvar Análise", command=self.save_analysis)
        self.save_analysis_button.grid(row=6, column=0, padx=5, pady=5, sticky="ew")
        
        self.data = None
        
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.selected_columns.delete(0, tk.END)  # Limpa a lista de colunas selecionadas
                for column in self.data.columns:
                    self.selected_columns.insert(tk.END, column)
                self.update_status_bar("Dados carregados com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
    
    def analyze_data(self):
        if self.data is None:
            messagebox.showwarning("Aviso", "Por favor, carregue os dados primeiro!")
            return
        
        selected_columns = [self.selected_columns.get(idx) for idx in self.selected_columns.curselection()]
        if not selected_columns:
            messagebox.showwarning("Aviso", "Por favor, selecione pelo menos uma coluna para análise!")
            return
        
        analysis_result = self.data[selected_columns].describe()
        messagebox.showinfo("Análise de Dados", f"{analysis_result}")
    
    def plot_data(self):
        if self.data is None:
            messagebox.showwarning("Aviso", "Por favor, carregue os dados primeiro!")
            return
        
        try:
            selected_columns = [self.selected_columns.get(idx) for idx in self.selected_columns.curselection()]
            if not selected_columns:
                messagebox.showwarning("Aviso", "Por favor, selecione pelo menos uma coluna para plotar o gráfico!")
                return
            
            self.data[selected_columns].plot()
            plt.title("Gráfico de Dados")
            plt.xlabel("Índice")
            plt.ylabel("Valor")
            plt.legend(selected_columns)
            plt.show()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao plotar gráfico: {str(e)}")
    
    def show_data(self):
        if self.data is None:
            messagebox.showwarning("Aviso", "Por favor, carregue os dados primeiro!")
            return
        
        top = tk.Toplevel(self.root)
        top.title("Visualização de Dados")
        table = Table(top, dataframe=self.data.head())
        table.show()
    
    def save_analysis(self):
        if self.data is None:
            messagebox.showwarning("Aviso", "Por favor, carregue os dados primeiro!")
            return
        
        selected_columns = [self.selected_columns.get(idx) for idx in self.selected_columns.curselection()]
        if not selected_columns:
            messagebox.showwarning("Aviso", "Por favor, selecione pelo menos uma coluna para análise!")
            return
        
        analysis_result = self.data[selected_columns].describe()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(str(analysis_result))
                self.update_status_bar(f"Análise salva em: {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar análise: {str(e)}")
    
    def update_status_bar(self, message):
        status_bar = ttk.Label(self.frame, text=message)
        status_bar.grid(row=7, column=0, padx=5, pady=5, sticky="ew")
        status_bar.after(5000, status_bar.destroy)  # Remove o status após 5 segundos

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
