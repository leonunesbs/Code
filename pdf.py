import io

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def preencher_pdf(pdf_template, dados, output_file):
    reader = PdfReader(pdf_template)
    writer = PdfWriter()

    try:
        for page_num, page_data in dados.items():
            overlay = io.BytesIO()
            can = canvas.Canvas(overlay, pagesize=letter)
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
