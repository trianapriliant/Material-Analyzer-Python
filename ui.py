import tkinter as tk
from tkinter import ttk, font, PhotoImage
from uvvis.gui import UVVisGUI
# Impor modul GUI untuk analisis lain (UVVisDRS, FTIR, SEM) di sini

class UIMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisis App")
        self.root.geometry("600x400")  # Ukuran window yang lebih besar
        self.root.configure(bg="#f0f0f0")  # Warna latar belakang

        # Frame untuk tombol pilihan analisis
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True, fill="both")

        # Style untuk tombol
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.map("TButton",
                       background=[("active", "#45a049")],  # Warna saat tombol dihover
                       foreground=[("active", "white")])

        # Load ikon dari folder assets/icon/
        self.uvvis_icon = PhotoImage(file="assets/icons/uvvis-icon.png").subsample(2, 2)  # Sesuaikan path dan ukuran
        self.uvvis_drs_icon = PhotoImage(file="assets/icons/uvvis-drs-icon.png").subsample(2, 2)
        self.ftir_icon = PhotoImage(file="assets/icons/ftir-icon.png").subsample(2, 2)
        self.sem_icon = PhotoImage(file="assets/icons/sem-icon.png").subsample(2, 2)

        # Tombol dengan ikon
        ttk.Button(
            self.frame,
            text="UV-Vis",
            image=self.uvvis_icon,
            compound="left",  # Posisi ikon di sebelah kiri teks
            command=self.open_uvvis,
            style="TButton"
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="UV-Vis DRS (soon)",
            image=self.uvvis_drs_icon,
            compound="left",
            command=self.open_uvvis_drs,
            style="TButton"
        ).grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="FTIR (soon)",
            image=self.ftir_icon,
            compound="left",
            command=self.open_ftir,
            style="TButton"
        ).grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="SEM (soon)",
            image=self.sem_icon,
            compound="left",
            command=self.open_sem,
            style="TButton"
        ).grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        # Mengatur ukuran kolom dan baris agar tombol memiliki ukuran yang sama
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)

        # Credit Label
        credit_label = ttk.Label(
            self.root,
            text="v1.5 - under development | made with ❤️ by rynn ~ personal use for physics of materials",
            font=("Segoe UI Emoji", 8),
            foreground="gray"
        )
        credit_label.pack(side="bottom", pady=10)

    def open_uvvis(self):
        """Buka modul UV-Vis"""
        uvvis_window = tk.Toplevel(self.root)
        UVVisGUI(uvvis_window)

    def open_uvvis_drs(self):
        """Buka modul UV-Vis DRS"""
        # Implementasi modul UV-Vis DRS di sini
        pass

    def open_ftir(self):
        """Buka modul FTIR"""
        # Implementasi modul FTIR di sini
        pass

    def open_sem(self):
        """Buka modul SEM"""
        # Implementasi modul SEM di sini
        pass