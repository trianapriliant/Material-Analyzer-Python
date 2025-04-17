import matplotlib.pyplot as plt
import numpy as np

def plot_raw_data(nm, percent_R):
    """Memplot data mentah %R vs nm dengan nm meningkat."""
    sorted_indices = np.argsort(nm)
    nm_sorted = nm[sorted_indices]
    percent_R_sorted = percent_R[sorted_indices]
    plt.figure(figsize=(8, 6), facecolor='#fafafa')
    plt.plot(nm_sorted, percent_R_sorted, color='#333333')
    plt.xlabel('Panjang Gelombang (nm)', fontfamily='Segoe UI', fontsize=12)
    plt.ylabel('%R', fontfamily='Segoe UI', fontsize=12)
    plt.title('Data Mentah', fontfamily='Segoe UI', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#fafafa')
    plt.show()

def plot_kubelka_munk(E, F_R):
    """Memplot F(R) vs E."""
    plt.figure(figsize=(8, 6), facecolor='#fafafa')
    plt.plot(E, F_R, color='#333333')
    plt.xlabel('Energi (eV)', fontfamily='Segoe UI', fontsize=12)
    plt.ylabel('F(R)', fontfamily='Segoe UI', fontsize=12)
    plt.title('Kubelka-Munk', fontfamily='Segoe UI', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#fafafa')
    plt.show()

def plot_tauc(E, F_R, transition_type='direct'):
    """Memplot Tauc plot berdasarkan tipe transisi."""
    if transition_type == 'direct':
        y = (F_R * E)**2
        exponent = 2
    elif transition_type == 'indirect':
        y = (F_R * E)**0.5
        exponent = 0.5
    else:
        raise ValueError("Tipe transisi tidak valid")
    plt.figure(figsize=(8, 6), facecolor='#fafafa')
    plt.plot(E, y, color='#333333')
    plt.xlabel('Energi (eV)', fontfamily='Segoe UI', fontsize=12)
    plt.ylabel(f'(F(R) E)^{exponent}', fontfamily='Segoe UI', fontsize=12)
    plt.title(f'Tauc Plot (Transisi {transition_type})', fontfamily='Segoe UI', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#fafafa')
    plt.show()