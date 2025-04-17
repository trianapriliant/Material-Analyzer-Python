import tkinter as tk
from tkinter import ttk, font, PhotoImage
from uvvis.gui import UVVisGUI
from sem.gui import SEMGUI
from uvvisdrs.gui import UVVisDRSWindow  # Impor modul UV-Vis DRS

class UIMainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisis App")
        self.root.geometry("800x600")  # Ukuran window yang lebih besar
        self.root.configure(bg="#fafafa")  # Warna latar belakang soft

        # Frame untuk tombol pilihan analisis
        self.frame = ttk.Frame(self.root, padding="30")
        self.frame.pack(expand=True, fill="both")

        # Style untuk tombol
        self.style = ttk.Style()
        self.style.configure("TButton", 
                            font=("Segoe UI", 14), 
                            padding=15, 
                            background="#e0e0e0", 
                            foreground="#333333", 
                            borderwidth=0)
        self.style.map("TButton",
                       background=[("active", "#45a049")],  # Warna saat tombol dihover
                       foreground=[("active", "gray")])

        # Load ikon dari folder assets/icon/
        self.uvvis_icon = PhotoImage(file="assets/icons/uvvis_icon.png").subsample(2, 2)  # Sesuaikan path dan ukuran
        self.uvvis_drs_icon = PhotoImage(file="assets/icons/uvvisdrs_icon.png").subsample(2, 2)
        self.ftir_icon = PhotoImage(file="assets/icons/ftir_icon.png").subsample(2, 2)
        self.sem_icon = PhotoImage(file="assets/icons/sem_icon.png").subsample(2, 2)

        # Tombol dengan ikon
        ttk.Button(
            self.frame,
            text="UV-Vis",
            image=self.uvvis_icon,
            compound="top",  # Posisi ikon di atas teks
            command=self.open_uvvis,
            style="TButton"
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="UV-Vis-DRS (Under Dev)",
            image=self.uvvis_drs_icon,
            compound="top",
            command=self.open_uvvis_drs,
            style="TButton"
        ).grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="FTIR (Under Dev)",
            image=self.ftir_icon,
            compound="top",
            command=self.open_ftir,
            style="TButton"
        ).grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        ttk.Button(
            self.frame,
            text="SEM (Bugging)",
            image=self.sem_icon,
            compound="top",
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
            text="v1.5.2 - under development | made with ❤️ by rynn ~ personal use for physics of materials",
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
        uvvis_drs_window = tk.Toplevel(self.root)
        UVVisDRSWindow(uvvis_drs_window)

    def open_ftir(self):
        """Buka modul FTIR"""
        # Implementasi modul FTIR di sini
        pass

    def open_sem(self):
        """Buka modul SEM"""
        sem_window = tk.Toplevel(self.root)
        SEMGUI(sem_window)  # Menghubungkan ke antarmuka SEM


if __name__ == "__main__":
    root = tk.Tk()
    app = UIMainApp(root)
    root.mainloop()