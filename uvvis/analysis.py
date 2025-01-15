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

    abs_max_values = [df['Absorbansi'].max() for df in gui.data_frames]
    waktu = np.arange(0, len(abs_max_values))

    def model_kinetika(t, k, C0):
        return C0 * np.exp(-k * t)

    try:
        popt, _ = curve_fit(model_kinetika, waktu, abs_max_values, p0=[0.1, abs_max_values[0]])
        k, C0 = popt
    except Exception as e:
        messagebox.showerror("Error", f"Gagal melakukan fitting data: {str(e)}")
        return

    fig, ax = plt.subplots()
    ax.scatter(waktu, abs_max_values, label='Data Eksperimen')
    ax.plot(waktu, model_kinetika(waktu, k, C0), label=f'Fitting: k={k:.4f}, C0={C0:.2f}', color='red')
    ax.set_xlabel('Waktu (Jam)')
    ax.set_ylabel('Absorbansi Maksimum')
    ax.set_title('Kinetika Degradasi')
    ax.legend()
    ax.grid(True)

    persamaan = f"Persamaan Kinetika:\nC(t) = {C0:.2f} * e^(-{k:.4f} * t)"
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