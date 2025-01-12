import os
import pandas as pd
from tkinter import messagebox

def process_data(gui):
    folder_path = gui.folder_path_var.get()
    if not folder_path or not os.path.exists(folder_path):
        messagebox.showerror("Error", "Folder path tidak valid!")
        return

    sample_names = gui.sample_names_var.get().split(',')
    sample_names = [name.strip() for name in sample_names if name.strip()]
    if not sample_names:
        messagebox.showerror("Error", "Nama sampel harus diisi!")
        return

    graph_title = gui.graph_title_var.get()
    if not graph_title:
        messagebox.showerror("Error", "Judul grafik harus diisi!")
        return

    alat_terpilih = gui.alat_var.get()
    
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]
    if not file_paths:
        messagebox.showinfo("Info", "Tidak ada file CSV ditemukan di folder: " + folder_path)
        return

    gui.data_frames = [] # inisialisasi data_frames
    for file_path in file_paths:
        try:
            if alat_terpilih == 1:
                df = pd.read_csv(file_path, skiprows=45, delimiter="\t", header=None)
                if df.shape[1] >= 3:
                    df = df.iloc[:, :3]
                else:
                    messagebox.showerror("Error", f"File {file_path} memiliki csv dengan format berbeda, coba pilih alat lain")
                    return
                df.columns = ['Nomor', 'Lambda', 'Absorbansi']
            else:
                df = pd.read_csv(file_path, delimiter=";")
                if df.shape[1] >= 2:
                    df = df.iloc[:, :2]
                else:
                    messagebox.showerror("Error", f"File {file_path} memiliki csv dengan format berbeda, coba pilih alat lain")
                    return
                df.columns = ['Lambda', 'Absorbansi']
                df['Nomor'] = range(1, len(df) + 1)

            df['Lambda'] = pd.to_numeric(df['Lambda'], errors='coerce')
            df['Absorbansi'] = pd.to_numeric(df['Absorbansi'], errors='coerce')
            df['Transmitansi'] = 10 ** (-df['Absorbansi'])
            gui.data_frames.append(df)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file {file_path}: {str(e)}")
            return

    abs_max_values = [df['Absorbansi'].max() for df in gui.data_frames]
    gui.degradasi_values = [(abs_max_values[0] - value) / abs_max_values[0] * 100 for value in abs_max_values[1:]]

    from .plotting import plot_graph
    plot_graph(gui, show_absorbance=gui.plot_type.get() == 1)