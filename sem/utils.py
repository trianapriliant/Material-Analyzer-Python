import pandas as pd
from fpdf import FPDF

def export_sem_report(data, output_path):
    """
    Ekspor laporan analisis SEM ke PDF.
    :param data: DataFrame yang berisi data SEM.
    :param output_path: Path untuk menyimpan laporan PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Tambahkan konten ke PDF
    pdf.cell(200, 10, txt="Laporan Analisis SEM", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Data SEM:", ln=True)
    pdf.ln(10)

    # Contoh: Tambahkan tabel data ke PDF
    for index, row in data.iterrows():
        pdf.cell(200, 10, txt=str(row), ln=True)

    # Simpan PDF
    pdf.output(output_path)