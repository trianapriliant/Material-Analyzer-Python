import os
import pandas as pd
from tkinter import filedialog, messagebox
from fpdf import FPDF
from .plotting import plot_graph  # Impor fungsi plot_graph dari modul plotting

def eksport_csv(gui):
    if gui.data_frames is None:
        messagebox.showerror("Error", "Tidak ada data yang diproses! Harap proses data terlebih dahulu.")
        return

    result = gui.data_frames[0][['Nomor', 'Lambda']].copy()
    sample_names = gui.sample_names_var.get().split(',')
    sample_names = [name.strip() for name in sample_names if name.strip()]
    for i, df in enumerate(gui.data_frames):
        result[f"Abs {sample_names[i]}"] = df['Absorbansi']
        result[f"Trans {sample_names[i]}"] = df['Transmitansi']

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Simpan File CSV"
    )
    if not file_path:
        return

    try:
        result.to_csv(file_path, index=False)
        messagebox.showinfo("Sukses", f"File CSV berhasil disimpan di: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file CSV: {str(e)}")

def eksport_gambar(gui):
    if gui.canvas is None:
        messagebox.showerror("Error", "Tidak ada grafik yang ditampilkan! Harap proses data terlebih dahulu.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")],
        title="Simpan Gambar Grafik"
    )
    if not file_path:
        return

    try:
        gui.canvas.figure.savefig(file_path, dpi=300, bbox_inches="tight")
        messagebox.showinfo("Sukses", f"Gambar grafik berhasil disimpan di: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar grafik: {str(e)}")

def export_report(gui):
    if gui.data_frames is None or gui.canvas is None:
        messagebox.showerror("Error", "Tidak ada data atau grafik yang tersedia! Harap proses data terlebih dahulu.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Simpan Laporan PDF"
    )
    if not file_path:
        return

    try:
        from .plotting import plot_graph  # Impor plot_graph dari modul plotting
        from .analysis import kinetika_degradasi, konsentrasi_relatif  # Impor fungsi analisis dari modul analysis

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Laporan Analisis UV-Vis", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Judul Grafik: {gui.graph_title_var.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Nama Sampel: {gui.sample_names_var.get()}", ln=True)
        pdf.ln(10)

        # Simpan Grafik Transmitansi
        temp_transmitansi_path = "temp_transmitansi.png"
        plot_graph(gui, show_absorbance=True)  # Panggil plot_graph dari modul plotting
        gui.canvas.figure.savefig(temp_transmitansi_path, dpi=300, bbox_inches="tight")
        pdf.cell(200, 10, txt="Grafik Transmitansi", ln=True)
        pdf.image(temp_transmitansi_path, x=10, y=None, w=180)
        pdf.ln(10)

        # Simpan Grafik Kinetika Degradasi
        temp_kinetika_path = "temp_kinetika.png"
        kinetika_degradasi(gui)  # Panggil kinetika_degradasi dari modul analysis
        gui.canvas.figure.savefig(temp_kinetika_path, dpi=300, bbox_inches="tight")
        pdf.cell(200, 10, txt="Grafik Kinetika Degradasi", ln=True)
        pdf.image(temp_kinetika_path, x=10, y=None, w=180)
        pdf.ln(10)

        # Simpan Grafik Konsentrasi Relatif
        temp_konsentrasi_path = "temp_konsentrasi.png"
        konsentrasi_relatif(gui)  # Panggil konsentrasi_relatif dari modul analysis
        gui.canvas.figure.savefig(temp_konsentrasi_path, dpi=300, bbox_inches="tight")
        pdf.cell(200, 10, txt="Grafik Konsentrasi Relatif", ln=True)
        pdf.image(temp_konsentrasi_path, x=10, y=None, w=180)
        pdf.ln(10)

        # Simpan PDF
        pdf.output(file_path)
        messagebox.showinfo("Sukses", f"Laporan berhasil disimpan di: {file_path}")

        # Hapus file gambar sementara
        os.remove(temp_transmitansi_path)
        os.remove(temp_kinetika_path)
        os.remove(temp_konsentrasi_path)

    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan laporan PDF: {str(e)}")