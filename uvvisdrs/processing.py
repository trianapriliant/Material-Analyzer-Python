import pandas as pd
import numpy as np
from scipy.signal import savgol_filter

def read_csv(file_path):
    """Membaca file CSV dan mengembalikan kolom nm dan %R."""
    data = pd.read_csv(file_path, skiprows=1)
    nm = data['nm'].values
    percent_R = data['%R'].values
    return nm, percent_R

def calculate_R(percent_R):
    """Mengonversi %R ke R (reflektansi desimal)."""
    return percent_R / 100.0

def calculate_kubelka_munk(R):
    """Menghitung fungsi Kubelka-Munk F(R)."""
    return (1 - R)**2 / (2 * R)

def smooth_data(data, window_length=11, polyorder=2):
    """Menerapkan smoothing pada data menggunakan Savitzky-Golay filter."""
    return savgol_filter(data, window_length=window_length, polyorder=polyorder)

def calculate_energy(nm):
    """Mengonversi panjang gelombang (nm) ke energi foton (eV)."""
    return 1240 / nm