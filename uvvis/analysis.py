import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def kinetika_degradasi(gui):
    if gui.data_frames is None:
        messagebox.showerror("Error", "Harap proses data terlebih dahulu!")
        return

    sample_names = gui.sample_names_var.get().split(',')
    sample_names = [name.strip() for name in sample_names if name.strip()]

    # Ambil nilai absorbansi maksimum untuk setiap waktu
    abs_max_values = [df['Absorbansi'].max() for df in gui.data_frames]
    A0 = abs_max_values[0]  # Absorbansi awal
    waktu = np.arange(0, len(abs_max_values))  # Waktu (indeks)

    # Hitung ln(A0/At)
    ln_A0_At = np.log(A0 / np.array(abs_max_values))

    # Model fitting: y = k * t + C
    def model_kinetika(t, k, C):
        return k * t + C

    try:
        # Lakukan fitting data
        popt, _ = curve_fit(model_kinetika, waktu, ln_A0_At, p0=[0.1, 0])
        k, C = popt  # k adalah konstanta laju degradasi, C adalah konstanta
    except Exception as e:
        messagebox.showerror("Error", f"Gagal melakukan fitting data: {str(e)}")
        return

    # Buat grafik
    fig, ax = plt.subplots()
    ax.scatter(waktu, ln_A0_At, label='Data Eksperimen (ln(A₀/Aₜ))')
    ax.plot(waktu, model_kinetika(waktu, k, C), label=f'Fitting: k={k:.4f}, C={C:.2f}', color='red')
    ax.set_xlabel('Waktu (Jam)')
    ax.set_ylabel('ln(A₀/Aₜ)')
    ax.set_title('Kinetika Degradasi')
    ax.legend()
    ax.grid(True)

    # Tampilkan persamaan fitting
    persamaan = f"Persamaan Kinetika:\nln(A₀/Aₜ) = {k:.4f} * t + {C:.2f}"
    ax.text(0.05, 0.95, persamaan, transform=ax.transAxes, fontsize=10, color='blue',
            ha='left', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Tampilkan grafik di GUI
    if gui.canvas:
        gui.canvas.get_tk_widget().pack_forget()
    if gui.toolbar:
        gui.toolbar.pack_forget()

    gui.canvas = FigureCanvasTkAgg(fig, master=gui.graph_frame)
    gui.canvas.draw()
    gui.canvas.get_tk_widget().pack()

    gui.toolbar = NavigationToolbar2Tk(gui.canvas, gui.graph_frame)
    gui.toolbar.update()
    gui.toolbar.pack()

def konsentrasi_relatif(gui):
    if gui.data_frames is None:
        messagebox.showerror("Error", "Harap proses data terlebih dahulu!")
        return

    sample_names = gui.sample_names_var.get().split(',')
    sample_names = [name.strip() for name in sample_names if name.strip()]

    abs_max_values = [df['Absorbansi'].max() for df in gui.data_frames]
    C0 = abs_max_values[0]
    konsentrasi_rel = [abs_value / C0 for abs_value in abs_max_values]

    fig, ax = plt.subplots()
    ax.plot(range(len(konsentrasi_rel)), konsentrasi_rel, marker='o', label='Konsentrasi Relatif')
    ax.set_xlabel('Waktu (Jam)')
    ax.set_ylabel('Konsentrasi Relatif')
    ax.set_title('Konsentrasi Relatif')
    ax.legend()
    ax.grid(True)

    persamaan = "Persamaan Konsentrasi Relatif:\nC(t)/C₀"
    ax.text(0.05, 0.95, persamaan, transform=ax.transAxes, fontsize=10, color='blue',
            ha='left', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    if gui.canvas:
        gui.canvas.get_tk_widget().pack_forget()
    if gui.toolbar:
        gui.toolbar.pack_forget()

    gui.canvas = FigureCanvasTkAgg(fig, master=gui.graph_frame)
    gui.canvas.draw()
    gui.canvas.get_tk_widget().pack()

    gui.toolbar = NavigationToolbar2Tk(gui.canvas, gui.graph_frame)
    gui.toolbar.update()
    gui.toolbar.pack()