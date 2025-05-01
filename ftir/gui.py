import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ftir.processing import load_data, baseline_correction
from ftir.analysis import identify_peaks
from ftir.plotting import plot_spectrum, plot_raw_data
from ftir.utils import export_to_excel, export_plot

class FtirWindow:
    def __init__(self, master):
        self.master = master
        master.title("Analisis FTIR")
        
        # Menu bar di pojok kiri atas
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)
        
        # Menu File untuk ekspor
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Ekspor Data ke Excel", command=self.export_data)
        self.file_menu.add_command(label="Ekspor Plot", command=self.export_plot)
        
        # Frame untuk tombol utama
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)
        
        # Tombol untuk memuat data
        self.load_button = tk.Button(self.button_frame, text="Muat Data FTIR", command=self.load_data)
        self.load_button.grid(row=0, column=0, padx=10, pady=5)
        
        # Input untuk nama plot
        self.plot_name_label = tk.Label(self.button_frame, text="Nama Plot:")
        self.plot_name_label.grid(row=0, column=1, padx=10, pady=5)
        self.plot_name_entry = tk.Entry(self.button_frame)
        self.plot_name_entry.grid(row=0, column=2, padx=10, pady=5)
        
        # Tombol untuk plot data mentah
        self.plot_raw_button = tk.Button(self.button_frame, text="Plot Data Mentah", command=self.plot_raw)
        self.plot_raw_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Tombol untuk koreksi baseline
        self.correct_button = tk.Button(self.button_frame, text="Koreksi Baseline", command=self.baseline_correction)
        self.correct_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Tombol untuk analisis puncak
        self.analyze_button = tk.Button(self.button_frame, text="Identifikasi Puncak", command=self.identify_peaks)
        self.analyze_button.grid(row=1, column=2, padx=10, pady=5)
        
        # Tombol untuk memplot spektrum yang dikoreksi
        self.plot_button = tk.Button(self.button_frame, text="Plot Spektrum Dikoreksi", command=self.plot_spectrum)
        self.plot_button.grid(row=2, column=0, padx=10, pady=5)
        
        # Frame untuk plot dan toolbar
        self.plot_frame = tk.Frame(master)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Figure untuk plotting dengan ukuran yang lebih besar
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Tambahkan toolbar navigasi
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Variabel untuk menyimpan data
        self.data = None
        self.corrected_data = None
        self.peaks = None
        
    def load_data(self):
        """Memuat data FTIR dari file .txt"""
        file_path = filedialog.askopenfilename(filetypes=[("File Teks", "*.txt")])
        if file_path:
            self.data = load_data(file_path)
            messagebox.showinfo("Info", "Data dimuat dengan sukses")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada file yang dipilih")
        
    def plot_raw(self):
        """Memplot data FTIR mentah menggunakan transmitansi"""
        if self.data is None:
            messagebox.showwarning("Peringatan", "Silakan muat data terlebih dahulu")
            return
        try:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Mentah"
            plot_raw_data(self.ax, self.data, plot_name)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat plotting data mentah: {str(e)}")
        
    def baseline_correction(self):
        """Menerapkan koreksi baseline"""
        if self.data is None:
            messagebox.showwarning("Peringatan", "Silakan muat data terlebih dahulu")
            return
        try:
            self.corrected_data = baseline_correction(self.data)
            messagebox.showinfo("Info", "Koreksi baseline diterapkan")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat koreksi baseline: {str(e)}")
        
    def identify_peaks(self):
        """Mengidentifikasi puncak pada data yang dikoreksi"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        try:
            self.peaks = identify_peaks(self.corrected_data)
            messagebox.showinfo("Info", f"{len(self.peaks)} puncak diidentifikasi")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat identifikasi puncak: {str(e)}")
        
    def plot_spectrum(self):
        """Memplot spektrum FTIR yang dikoreksi"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        try:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Dikoreksi"
            plot_spectrum(self.ax, self.corrected_data, self.peaks, plot_name)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat plotting: {str(e)}")
        
    def export_data(self):
        """Ekspor data ke Excel"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("File Excel", "*.xlsx")])
        if file_path:
            try:
                export_to_excel(self.corrected_data, self.peaks, file_path)
                messagebox.showinfo("Info", "Data diekspor ke Excel")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat ekspor data: {str(e)}")
        
    def export_plot(self):
        """Ekspor plot ke file gambar"""
        if self.ax.get_lines() == []:
            messagebox.showwarning("Peringatan", "Tidak ada plot yang tersedia untuk diekspor")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("File PNG", "*.png")])
        if file_path:
            try:
                export_plot(self.figure, file_path)
                messagebox.showinfo("Info", "Plot diekspor")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat ekspor plot: {str(e)}")