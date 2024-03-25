import csv
import io
import os
import subprocess
import zipfile
from datetime import datetime
from tkinter import messagebox

from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from reportlab.lib.pagesizes import A2
from reportlab.pdfgen import canvas

from libs import output_folder


def clear_output_folder():
    # Função para limpar o diretório de saída
    def do_clear():
        folder_to_clear = output_folder
        for root, dirs, files in os.walk(folder_to_clear):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        messagebox.showinfo("Limpeza Concluída",
                            "O diretório de saída foi limpo com sucesso.")

    # Confirmar antes de limpar o diretório de saída
    confirm = messagebox.askyesno(
        "Confirmação", "Tem certeza de que deseja limpar o diretório de saída?")
    if confirm:
        do_clear()


def merge_pdf_files():
    merged_pdf_path = os.path.join(output_folder, 'merged_output.pdf')

    merger = PdfMerger()

    # Add all PDF files in the output folder to the merger
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.pdf'):
                merger.append(os.path.join(root, file))

    # Write the merged PDF to a file
    with open(merged_pdf_path, 'wb') as merged_pdf_file:
        merger.write(merged_pdf_file)

    messagebox.showinfo("Merge Concluído",
                        "Os arquivos PDF foram mesclados com sucesso.")
    subprocess.Popen(['open', '-R', output_folder])


def zip_output_folder():
    # Altere este caminho conforme necessário
    folder_to_zip = output_folder
    # Nome do arquivo zip de saída
    output_zip_file = f"archive/{datetime.now().strftime('%d%m%Y')}.zip"

    with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_to_zip):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(
                    file_path, folder_to_zip))

    # Abrir o Finder na pasta de destino
    subprocess.Popen(['open', '-R', output_zip_file])


def preencher_pdf(pdf_template, dados, output_file):
    reader = PdfReader(pdf_template)
    writer = PdfWriter()

    try:
        for page_num, page_data in dados.items():
            overlay = io.BytesIO()
            can = canvas.Canvas(overlay, pagesize=A2)
            can.setFontSize(10)

            for field, value in page_data.items():
                can.drawString(field[0], field[1], value)

            can.save()
            overlay.seek(0)
            overlay_pdf = PdfReader(overlay)

            page = reader.pages[page_num - 1]
            page.merge_page(overlay_pdf.pages[0])
            writer.add_page(page)

        with open(output_file, 'wb') as out:
            writer.write(out)

        return True

    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")
        return False
