import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk

from interface.form import handle_csv_upload, preencher_e_salvar
from manager.actions import (clear_output_folder, merge_pdf_files,
                             zip_output_folder)

root = tk.Tk()
root.title("Preencher PDF")

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

entry_tratamento_var = tk.StringVar()
combo_tratamento = ttk.Combobox(root, textvariable=entry_tratamento_var)
combo_tratamento['values'] = ("Avastin", "Eylia")
combo_tratamento.grid(row=4, column=1, padx=5, pady=5)

button_preencher_salvar = tk.Button(
    root, text="Preencher e Salvar", command=lambda: preencher_e_salvar(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var))
button_preencher_salvar.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

button_zip_output = tk.Button(
    root, text="Zip Output", command=zip_output_folder)
button_zip_output.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Adicione o botão de upload do CSV
button_upload_csv = tk.Button(
    root, text="Upload CSV", command=lambda: handle_csv_upload(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var))
button_upload_csv.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

button_clear_output = tk.Button(
    root, text="Limpar Output", command=clear_output_folder)
button_clear_output.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

button_merge_pdf = tk.Button(
    root, text="Merge PDF", command=merge_pdf_files)
button_merge_pdf.grid(row=9, column=0, columnspan=2, padx=5, pady=5)
# Vincula a função preencher_e_salvar à tecla "Enter" em qualquer campo de entrada
root.bind('<Return>', lambda event: preencher_e_salvar(entry_nome_paciente,
          entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var))

root.mainloop()
