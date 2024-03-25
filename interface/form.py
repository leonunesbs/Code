import csv
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

from libs import root_directory
from manager.actions import preencher_pdf

start_csv_row = 5


def handle_csv_upload(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            tratamento_var = entry_tratamento_var.get()
            if not tratamento_var:
                raise ValueError('Selecione o tipo de tratamento!')
            with open(file_path, newline='', encoding='utf-8') as csvfile:

                reader = csv.reader(csvfile, delimiter=';')

                for i in range(start_csv_row - 1):
                    next(reader)
                for row in reader:
                    entry_nome_paciente.delete(0, tk.END)
                    entry_numero_prontuario.delete(0, tk.END)
                    entry_nome_medico.delete(0, tk.END)

                    entry_numero_prontuario.insert(0, row[0])
                    entry_nome_paciente.insert(0, row[1])
                    entry_nome_medico.insert(0, row[3])

                    # Chame a função para preencher e salvar o PDF
                    preencher_e_salvar(
                        entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var)

            messagebox.showinfo(
                "Sucesso", "PDFs gerados com sucesso a partir do CSV!")
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao processar o arquivo CSV: {e}")
            limpar_campos_formulario(
                entry_nome_paciente, entry_numero_prontuario, entry_nome_medico)


def preencher_e_salvar(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, entry_tratamento_var):
    nome_paciente = entry_nome_paciente.get()
    numero_prontuario = entry_numero_prontuario.get()
    nome_medico = entry_nome_medico.get()
    data_procedimento = entry_data_procedimento.get()
    escolha_tratamento = entry_tratamento_var.get()

    if not data_procedimento:
        data_procedimento = datetime.now().strftime('%d/%m/%Y')

    tratamento = ""
    if escolha_tratamento == "Avastin":
        tratamento = "INJEÇÃO INTRAVÍTREA DE AVASTIN"
    elif escolha_tratamento == "Eylia":
        tratamento = "INJEÇÃO INTRAVÍTREA DE EYLIA"
    else:
        messagebox.showerror(
            "Erro", "Escolha inválida. Por favor, selecione Avastin para Injeção Avastin ou Eylia para Eylia.")
        return

    dados = {
        # página 1
        1: {
            (100, 633): formatar_nome(nome_paciente),
            (475, 633): numero_prontuario,
            (53, 483): formatar_data(data_procedimento),
            (215, 483): formatar_data(data_procedimento),
            (60, 110): formatar_data(data_procedimento),
            (50, 300): tratamento
        },
        2: {
            (100, 705): formatar_nome(nome_paciente),
            (440, 705): numero_prontuario,
            (45, 670): formatar_data(data_procedimento),
            (75, 640): formatar_nome(nome_medico),
        },
        3: {
            (75, 330): formatar_nome(nome_paciente),
            (345, 330): formatar_data(data_procedimento),
            (485, 330): formatar_nome(nome_paciente),
            (760, 330): formatar_data(data_procedimento),
        }
    }

    modelo_pdf = os.path.join(root_directory, 'modelo.pdf')
    arquivo_saida = os.path.join(
        root_directory, 'output', f'{formatar_nome(nome_paciente)}.pdf')
    if preencher_pdf(modelo_pdf, dados, arquivo_saida):
        messagebox.showinfo(
            "Sucesso", f"O arquivo foi criado com sucesso! ID: {numero_prontuario}")
        limpar_campos_formulario(
            entry_nome_paciente, entry_numero_prontuario, entry_nome_medico)
    else:
        messagebox.showerror("Erro", "Ocorreu um erro ao criar o arquivo.")


def limpar_campos_formulario(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico):
    entry_nome_paciente.delete(0, tk.END)
    entry_numero_prontuario.delete(0, tk.END)
    entry_nome_medico.delete(0, tk.END)
    entry_nome_paciente.focus_set()


def formatar_nome(nome):
    return ' '.join(nome.upper().split())


def formatar_data(data):
    return datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
