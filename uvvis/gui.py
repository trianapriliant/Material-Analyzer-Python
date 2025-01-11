import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class UVVisGUI:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("Absorbance Plot UV-Vis")
        self.data_frames = None
        self.degradasi_values = None
        self.canvas = None
        self.toolbar = None

        self.splash = tk.Toplevel(root)
        self.splash.title("Loading...")
        self.splash.geometry("300x100")
        tk.Label(self.splash, text="Membuka Aplikasi, Harap Tunggu...", font=("Arial", 12)).pack(pady=10)
        self.progress = ttk.Progressbar(self.splash, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)
        self.splash.update()

        self.loading_progress = 0
        self.update_progress()

    def update_progress(self):
        if self.loading_progress <= 100:
            self.progress['value'] = self.loading_progress
            self.splash.update()
            self.loading_progress += 10
            self.root.after(20, self.update_progress)
        else:
            self.setup_gui()
            self.splash.destroy()
            self.root.deiconify()

    def setup_gui(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        analisis_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Analisis", menu=analisis_menu)
        analisis_menu.add_command(label="Kinetika Degradasi", command=self.kinetika_degradasi)
        analisis_menu.add_command(label="Konsentrasi Relatif", command=self.konsentrasi_relatif)

        eksport_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Eksport", menu=eksport_menu)
        eksport_menu.add_command(label="Eksport CSV", command=self.eksport_csv)
        eksport_menu.add_command(label="Eksport Gambar", command=self.eksport_gambar)
        eksport_menu.add_command(label="Export Report", command=self.export_report)

        input_frame = tk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        tk.Label(input_frame, text="Folder Path:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.folder_path_var = tk.StringVar()
        self.folder_path_entry = tk.Entry(input_frame, textvariable=self.folder_path_var, width=40, fg="grey")
        self.folder_path_entry.grid(row=0, column=1, padx=5, pady=2)
        self.folder_path_entry.insert(0, "folder berisi file-file csv")
        self.folder_path_entry.bind("<FocusIn>", self.on_entry_click_folder)
        self.folder_path_entry.bind("<FocusOut>", self.on_focus_out_folder)
        tk.Button(input_frame, text="Browse", command=self.select_folder).grid(row=0, column=2, padx=5, pady=2)

        tk.Label(input_frame, text="Sample Names:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.sample_names_var = tk.StringVar()
        self.sample_names_entry = tk.Entry(input_frame, textvariable=self.sample_names_var, width=40, fg="grey")
        self.sample_names_entry.grid(row=1, column=1, padx=5, pady=2)
        self.sample_names_entry.insert(0, "pisahkan nama-nama sampel dengan koma")
        self.sample_names_entry.bind("<FocusIn>", self.on_entry_click)
        self.sample_names_entry.bind("<FocusOut>", self.on_focus_out)

        tk.Label(input_frame, text="Graph Title:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.graph_title_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=self.graph_title_var, width=40).grid(row=2, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Pilih Alat:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
        self.alat_var = tk.IntVar(value=1)
        tk.Radiobutton(input_frame, text="Alat Lama", variable=self.alat_var, value=1).grid(row=3, column=1, padx=5, pady=2, sticky="w")
        tk.Radiobutton(input_frame, text="Alat Baru", variable=self.alat_var, value=2).grid(row=3, column=2, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Pilih Jenis Grafik:").grid(row=4, column=0, padx=5, pady=0, sticky="w")
        self.plot_type = tk.IntVar(value=1)
        tk.Radiobutton(input_frame, text="Absorbansi", variable=self.plot_type, value=1).grid(row=4, column=1, padx=5, pady=0, sticky="w")
        tk.Radiobutton(input_frame, text="Transmitansi", variable=self.plot_type, value=2).grid(row=4, column=2, padx=5, pady=0, sticky="w")

        tk.Label(input_frame, text="Lebar Grafik:").grid(row=5, column=0, padx=5, pady=2, sticky="w")
        self.fig_width_scale = tk.Scale(input_frame, from_=4, to=20, orient="horizontal")
        self.fig_width_scale.set(8)
        self.fig_width_scale.grid(row=5, column=1, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Tinggi Grafik:").grid(row=5, column=2, padx=5, pady=2, sticky="w")
        self.fig_height_scale = tk.Scale(input_frame, from_=2, to=16, orient="horizontal")
        self.fig_height_scale.set(4)
        self.fig_height_scale.grid(row=5, column=3, padx=5, pady=2, sticky="w")

        self.show_degradasi = tk.IntVar(value=1)
        tk.Checkbutton(input_frame, text="% Degradasi", variable=self.show_degradasi).grid(row=6, column=0, sticky="ew", padx=2, pady=2)
        self.show_peak_points = tk.IntVar(value=1)
        tk.Checkbutton(input_frame, text="Titik Puncak", variable=self.show_peak_points).grid(row=6, column=1, sticky="ew", padx=2, pady=2)
        self.show_legend = tk.IntVar(value=1)
        tk.Checkbutton(input_frame, text="Legend", variable=self.show_legend).grid(row=6, column=2, sticky="ew", padx=2, pady=2)

        tk.Button(input_frame, text="Process Data", command=self.process_data).grid(row=9, column=0, columnspan=4, pady=5)

        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        credit_label = tk.Label(
            self.root,
            text="v1.5 - under development | made with ❤️ by rynn ~ personal use for physics of materials",
            font=("Segoe UI Emoji", 8),
            fg="gray"
        )
        credit_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_folder(self):
        folder = filedialog.askdirectory()
        self.folder_path_var.set(folder)

    def on_entry_click_folder(self, event):
        if self.folder_path_entry.get() == "folder berisi file-file csv":
            self.folder_path_entry.delete(0, "end")
            self.folder_path_entry.config(fg="black")

    def on_focus_out_folder(self, event):
        if self.folder_path_entry.get() == "":
            self.folder_path_entry.insert(0, "folder berisi file-file csv")
            self.folder_path_entry.config(fg="grey")

    def on_entry_click(self, event):
        if self.sample_names_entry.get() == "pisahkan nama-nama sampel dengan koma":
            self.sample_names_entry.delete(0, "end")
            self.sample_names_entry.config(fg="black")

    def on_focus_out(self, event):
        if self.sample_names_entry.get() == "":
            self.sample_names_entry.insert(0, "pisahkan nama-nama sampel dengan koma")
            self.sample_names_entry.config(fg="grey")

    def on_close(self):
        self.root.quit()

    def process_data(self):
        from .processing import process_data
        process_data(self)

    def kinetika_degradasi(self):
        from .analysis import kinetika_degradasi
        kinetika_degradasi(self)

    def konsentrasi_relatif(self):
        from .analysis import konsentrasi_relatif
        konsentrasi_relatif(self)

    def eksport_csv(self):
        from .utils import eksport_csv
        eksport_csv(self)

    def eksport_gambar(self):
        from .utils import eksport_gambar
        eksport_gambar(self)

    def export_report(self):
        from .utils import export_report
        export_report(self)