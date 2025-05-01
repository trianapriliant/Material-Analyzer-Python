import numpy as np
from scipy.signal import find_peaks

def identify_peaks(data):
    """Mengidentifikasi puncak pada data transmitansi"""
    if '%T_corrected' not in data.columns:
        raise ValueError("Data tidak memiliki kolom '%T_corrected'. Pastikan koreksi baseline telah dilakukan.")
    
    # Gunakan data transmitansi untuk mendeteksi puncak ke atas (penurunan %T)
    y = data['%T_corrected'].values
    
    # Balik data untuk mendeteksi puncak ke atas (penurunan %T)
    peaks, _ = find_peaks(-y, distance=10)  # distance=10 untuk mencegah deteksi puncak yang terlalu rapat
    
    return peaks