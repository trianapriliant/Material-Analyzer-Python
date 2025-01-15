import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

class SEMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SEM Analyzer")
        self.root.geometry("800x600")

        # Frame untuk input
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=10)

        # Tombol untuk memuat data SEM
        ttk.Button(self.input_frame, text="Load SEM Data", command=self.load_sem_data).pack(pady=10)

        # Frame untuk grafik
        self.graph_frame = ttk.Frame(self.root)
        self.graph_frame.pack(fill="both", expand=True)

        # Variabel untuk menyimpan data
        self.sem_data = None

    def load_sem_data(self):
        """Memuat data SEM dari file"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if not file_path:
            return

        try:
            # Proses data SEM (akan diimplementasikan di processing.py)
            from .processing import process_sem_data
            self.sem_data = process_sem_data(file_path)
            messagebox.showinfo("Success", "Data SEM berhasil dimuat!")
            self.plot_sem_data()  # Plot data setelah berhasil dimuat
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data SEM: {str(e)}")

    def plot_sem_data(self):
        """Plot data SEM"""
        if self.sem_data is None:
            return

        # Bersihkan frame grafik sebelumnya
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Plot data SEM (akan diimplementasikan di plotting.py)
        from .plotting import plot_sem_image
        fig, ax = plot_sem_image(self.sem_data)

        # Tampilkan grafik di GUI
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Tambahkan toolbar navigasi
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack()