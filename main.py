import tkinter as tk
from datetime import datetime
from tkinter import ttk

from gui import preencher_e_salvar

# Cria a janela principal
root = tk.Tk()
root.title("Preencher PDF")

# Cria e posiciona os widgets na janela
widgets = {
    "Nome do Paciente": (0, 0),
    "Número do Prontuário": (1, 0),
    "Nome do Médico": (2, 0),
    "Data do Procedimento": (3, 0),
    "Tratamento": (4, 0)
}

for label_text, (row, column) in widgets.items():
    label = tk.Label(root, text=label_text + ":")
    label.grid(row=row, column=column, padx=5, pady=5, sticky="e")

entry_nome_paciente = tk.Entry(root)
entry_nome_paciente.grid(row=0, column=1, padx=5, pady=5)
entry_nome_paciente.focus_set()

entry_numero_prontuario = tk.Entry(root)
entry_numero_prontuario.grid(row=1, column=1, padx=5, pady=5)

entry_nome_medico = tk.Entry(root)
entry_nome_medico.grid(row=2, column=1, padx=5, pady=5)

entry_data_procedimento = tk.Entry(root)
entry_data_procedimento.grid(row=3, column=1, padx=5, pady=5)
entry_data_procedimento.insert(0, datetime.now().strftime('%d/%m/%Y'))

tratamento_var = tk.StringVar()
combo_tratamento = ttk.Combobox(root, textvariable=tratamento_var)
combo_tratamento['values'] = ("Avastin", "Eylia")
combo_tratamento.grid(row=4, column=1, padx=5, pady=5)

button_preencher_salvar = tk.Button(
    root, text="Preencher e Salvar", command=lambda: preencher_e_salvar(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, tratamento_var))
button_preencher_salvar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Vincula a função preencher_e_salvar à tecla "Enter" em qualquer campo de entrada
root.bind('<Return>', lambda event: preencher_e_salvar(entry_nome_paciente,
          entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, tratamento_var))

# Inicia o loop principal da aplicação
root.mainloop()
