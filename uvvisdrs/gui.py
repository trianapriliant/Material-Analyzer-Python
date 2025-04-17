import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from . import processing
from . import plotting

class UVVisDRSWindow(tk.Toplevel):
    """Jendela GUI untuk analisis UV-Vis DRS."""
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Analisis UV-Vis DRS")
        self.geometry("600x450")
        self.configure(bg="#fafafa")

        self.frame = ttk.Frame(self, padding="30")
        self.frame.pack(expand=True, fill="both")

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
        self.style.configure("TLabel", font=("Segoe UI", 12), background="#fafafa")
        self.style.configure("TRadiobutton", font=("Segoe UI", 12), background="#fafafa")

        self.file_path = None
        self.nm = None
        self.percent_R = None
        self.R = None
        self.F_R = None
        self.F_R_smoothed = None
        self.E = None
        self.band_gap = None

        # Widget untuk input dan kontrol
        self.load_button = ttk.Button(self.frame, text="Muat CSV", command=self.load_file, style="TButton")
        self.load_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.plot_raw_button = ttk.Button(self.frame, text="Plot Data Mentah", command=self.plot_raw, style="TButton", state=tk.DISABLED)
        self.plot_raw_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.plot_km_original_button = ttk.Button(self.frame, text="Plot Kubelka-Munk (Asli)", command=self.plot_km_original, style="TButton", state=tk.DISABLED)
        self.plot_km_original_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.plot_km_smoothed_button = ttk.Button(self.frame, text="Plot Kubelka-Munk (Smoothed)", command=self.plot_km_smoothed, style="TButton", state=tk.DISABLED)
        self.plot_km_smoothed_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.transition_label = ttk.Label(self.frame, text="Pilih Tipe Transisi:")
        self.transition_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.transition_var = tk.StringVar(value='direct')
        self.direct_radio = ttk.Radiobutton(self.frame, text="Langsung", variable=self.transition_var, value='direct')
        self.direct_radio.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.indirect_radio = ttk.Radiobutton(self.frame, text="Tidak Langsung", variable=self.transition_var, value='indirect')
        self.indirect_radio.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.calculate_band_gap_button = ttk.Button(self.frame, text="Hitung Energi Band Gap", command=self.calculate_band_gap, style="TButton", state=tk.DISABLED)
        self.calculate_band_gap_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.plot_tauc_button = ttk.Button(self.frame, text="Plot Tauc dan Hitung Band Gap", command=self.plot_tauc, style="TButton", state=tk.DISABLED)
        self.plot_tauc_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

        # Label untuk menampilkan hasil energi band gap
        self.result_label = ttk.Label(self.frame, text="Energi Band Gap: Belum Dihitung", font=("Segoe UI", 12, "bold"), foreground="#333333")
        self.result_label.grid(row=9, column=0, padx=10, pady=15, sticky="w")

        self.frame.grid_columnconfigure(0, weight=1)

    def load_file(self):
        """Memuat file CSV dan memproses data."""
        self.file_path = filedialog.askopenfilename(filetypes=[("File CSV", "*.csv")])
        if self.file_path:
            self.nm, self.percent_R = processing.read_csv(self.file_path)
            self.R = processing.calculate_R(self.percent_R)
            self.F_R = processing.calculate_kubelka_munk(self.R)
            self.F_R_smoothed = processing.smooth_data(self.F_R)  # Simpan versi smoothed
            self.E = processing.calculate_energy(self.nm)
            self.plot_raw_button.config(state=tk.NORMAL)
            self.plot_km_original_button.config(state=tk.NORMAL)
            self.plot_km_smoothed_button.config(state=tk.NORMAL)
            self.calculate_band_gap_button.config(state=tk.NORMAL)
            self.plot_tauc_button.config(state=tk.NORMAL)
            self.result_label.config(text="Energi Band Gap: Belum Dihitung")

    def plot_raw(self):
        """Menampilkan plot data mentah."""
        plotting.plot_raw_data(self.nm, self.percent_R)

    def plot_km_original(self):
        """Menampilkan plot Kubelka-Munk tanpa smoothing."""
        plotting.plot_kubelka_munk(self.E, self.F_R, smoothed=False)

    def plot_km_smoothed(self):
        """Menampilkan plot Kubelka-Munk dengan smoothing."""
        plotting.plot_kubelka_munk(self.E, self.F_R_smoothed, smoothed=True)

    def calculate_band_gap(self):
        """Menghitung energi band gap tanpa menampilkan plot."""
        transition_type = self.transition_var.get()
        try:
            self.band_gap = plotting.calculate_band_gap(self.E, self.F_R_smoothed, transition_type)
            self.result_label.config(text=f"Energi Band Gap: {self.band_gap:.2f} eV", foreground="#45a049")
            messagebox.showinfo("Sukses", f"Energi Band Gap: {self.band_gap:.2f} eV")
        except ValueError as e:
            self.result_label.config(text="Error: Tidak dapat menghitung", foreground="red")
            messagebox.showerror("Error", f"Gagal menghitung energi band gap: {str(e)}")

    def plot_tauc(self):
        """Menampilkan plot Tauc dan menghitung energi band gap."""
        transition_type = self.transition_var.get()
        try:
            self.band_gap = plotting.plot_tauc(self.E, self.F_R_smoothed, transition_type)
            self.result_label.config(text=f"Energi Band Gap: {self.band_gap:.2f} eV", foreground="#45a049")
            messagebox.showinfo("Sukses", "Plot Tauc telah ditampilkan. Silakan periksa plot untuk garis tangensial dan nilai energi band gap.")
        except ValueError as e:
            self.result_label.config(text="Error: Tidak dapat menghitung", foreground="red")
            messagebox.showerror("Error", f"Gagal menghitung energi band gap: {str(e)}")