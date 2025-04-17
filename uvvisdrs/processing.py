import pandas as pd
import numpy as np

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

def calculate_energy(nm):
    """Mengonversi panjang gelombang (nm) ke energi foton (eV)."""
    return 1240 / nm