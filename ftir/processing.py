import pandas as pd
import numpy as np
from pybaselines import Baseline

def load_data(file_path):
    """Memuat data FTIR dari file .txt"""
    data = pd.read_csv(file_path, sep='\s+', skiprows=1, header=None, names=['wavenumber', '%T'])
    return data

def baseline_correction(data):
    """Menerapkan koreksi baseline menggunakan pybaselines"""
    # Ambil data %T dan pastikan tidak ada NaN
    y = data['%T'].values
    if np.any(np.isnan(y)):
        raise ValueError("Data mengandung nilai NaN. Pastikan data valid sebelum koreksi baseline.")
    
    # Ambil wavenumber sebagai x_data untuk baseline correction
    x = data['wavenumber'].values
    
    # Inisialisasi objek Baseline
    baseline_fitter = Baseline(x_data=x)
    
    # Terapkan koreksi baseline dengan asls
    # lam=1e3 dan p=0.01 adalah parameter default yang umum untuk FTIR
    y_corrected, baseline = baseline_fitter.asls(y, lam=1e3, p=0.01)
    
    # Pastikan panjang y_corrected sesuai dengan data asli
    if len(y_corrected) != len(y):
        raise ValueError(f"Panjang data yang dikoreksi ({len(y_corrected)}) tidak sesuai dengan data asli ({len(y)}).")
    
    corrected_data = data.copy()
    corrected_data['%T_corrected'] = y_corrected
    return corrected_data