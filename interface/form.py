import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from manager.pdf import preencher_pdf


def preencher_e_salvar(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento, tratamento_var):
    nome_paciente = entry_nome_paciente.get()
    numero_prontuario = entry_numero_prontuario.get()
    nome_medico = entry_nome_medico.get()
    data_procedimento = entry_data_procedimento.get()
    escolha_tratamento = tratamento_var.get()

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

    modelo_pdf = '/Users/leonunesbs/Documents/HGF/Code/modelo.pdf'
    arquivo_saida = f'/Users/leonunesbs/Documents/HGF/Code/output/{
        formatar_nome(nome_paciente)}.pdf'
    if preencher_pdf(modelo_pdf, dados, arquivo_saida):
        messagebox.showinfo("Sucesso", "O arquivo foi criado com sucesso!")
        limpar_campos_formulario(
            entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento)
    else:
        messagebox.showerror("Erro", "Ocorreu um erro ao criar o arquivo.")


def limpar_campos_formulario(entry_nome_paciente, entry_numero_prontuario, entry_nome_medico, entry_data_procedimento):
    entry_nome_paciente.delete(0, tk.END)
    entry_numero_prontuario.delete(0, tk.END)
    entry_nome_medico.delete(0, tk.END)
    entry_data_procedimento.delete(0, tk.END)
    entry_data_procedimento.insert(0, datetime.now().strftime('%d/%m/%Y'))
    entry_nome_paciente.focus_set()


def formatar_nome(nome):
    return ' '.join(nome.upper().split())


def formatar_data(data):
    return datetime.strptime(data, '%d/%m/%Y').strftime('%d/%m/%Y')
