import tkinter as tk
from tkinter import ttk, filedialog
from . import processing
from . import plotting

class UVVisDRSWindow(tk.Toplevel):
    """Jendela GUI untuk analisis UV-Vis DRS."""
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Analisis UV-Vis DRS")
        self.geometry("600x400")  # Ukuran jendela seragam
        self.configure(bg="#fafafa")  # Latar belakang sama dengan aplikasi utama

        # Frame utama dengan padding
        self.frame = ttk.Frame(self, padding="30")
        self.frame.pack(expand=True, fill="both")

        # Style untuk tombol, sesuai dengan ui.py
        self.style = ttk.Style()
        self.style.configure("TButton", 
                            font=("Segoe UI", 14), 
                            padding=15, 
                            background="#e0e0e0", 
                            foreground="#333333", 
                            borderwidth=0)
        self.style.map("TButton",
                       background=[("active", "#45a049")],
                       foreground=[("active", "gray")])

        # Style untuk label dan radio button
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#fafafa")
        self.style.configure("TRadiobutton", font=("Segoe UI", 12), background="#fafafa")

        self.file_path = None
        self.nm = None
        self.percent_R = None
        self.R = None
        self.F_R = None
        self.E = None

        # Membuat widget dengan tata letak grid
        self.load_button = ttk.Button(self.frame, text="Muat CSV", command=self.load_file, style="TButton")
        self.load_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.plot_raw_button = ttk.Button(self.frame, text="Plot Data Mentah", command=self.plot_raw, style="TButton", state=tk.DISABLED)
        self.plot_raw_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.plot_km_button = ttk.Button(self.frame, text="Plot Kubelka-Munk", command=self.plot_km, style="TButton", state=tk.DISABLED)
        self.plot_km_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Label untuk memilih tipe transisi
        self.transition_label = ttk.Label(self.frame, text="Pilih Tipe Transisi:")
        self.transition_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.transition_var = tk.StringVar(value='direct')
        self.direct_radio = ttk.Radiobutton(self.frame, text="Langsung", variable=self.transition_var, value='direct')
        self.direct_radio.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.indirect_radio = ttk.Radiobutton(self.frame, text="Tidak Langsung", variable=self.transition_var, value='indirect')
        self.indirect_radio.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.plot_tauc_button = ttk.Button(self.frame, text="Plot Tauc", command=self.plot_tauc, style="TButton", state=tk.DISABLED)
        self.plot_tauc_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        # Mengatur ukuran kolom agar tombol memiliki ukuran yang sama
        self.frame.grid_columnconfigure(0, weight=1)

    def load_file(self):
        """Memuat file CSV dan memproses data."""
        self.file_path = filedialog.askopenfilename(filetypes=[("File CSV", "*.csv")])
        if self.file_path:
            self.nm, self.percent_R = processing.read_csv(self.file_path)
            self.R = processing.calculate_R(self.percent_R)
            self.F_R = processing.calculate_kubelka_munk(self.R)
            self.E = processing.calculate_energy(self.nm)
            self.plot_raw_button.config(state=tk.NORMAL)
            self.plot_km_button.config(state=tk.NORMAL)
            self.plot_tauc_button.config(state=tk.NORMAL)

    def plot_raw(self):
        """Menampilkan plot data mentah."""
        plotting.plot_raw_data(self.nm, self.percent_R)

    def plot_km(self):
        """Menampilkan plot Kubelka-Munk."""
        plotting.plot_kubelka_munk(self.E, self.F_R)

    def plot_tauc(self):
        """Menampilkan plot Tauc berdasarkan tipe transisi."""
        transition_type = self.transition_var.get()
        plotting.plot_tauc(self.E, self.F_R, transition_type)