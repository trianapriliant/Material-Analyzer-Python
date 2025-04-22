import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from .processing import smooth_data

# Daftar material fotokatalis beserta rentang band gap literatur
MATERIAL_BAND_GAPS = {
    "TiO2 (anatase)": (3.0, 3.4),
    "TiO2 (rutile)": (2.8, 3.2),
    "SrTiO3 (murni)": (3.0, 3.4),
    "SrTiO3(La, Cr)": (2.5, 3.0),
    "ZnO": (3.1, 3.5),
    "WO3": (2.5, 2.9),
    "BiVO4": (2.3, 2.6),
    "g-C3N4": (2.5, 2.9)
}

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

def plot_kubelka_munk(E, F_R, smoothed=False):
    """Memplot F(R) vs E, dengan opsi smoothing."""
    if smoothed:
        F_R = smooth_data(F_R)
        title = 'Kubelka-Munk (Smoothed)'
    else:
        title = 'Kubelka-Munk (Asli)'
    
    plt.figure(figsize=(8, 6), facecolor='#fafafa')
    plt.plot(E, F_R, color='#333333')
    plt.xlabel('Energi (eV)', fontfamily='Segoe UI', fontsize=12)
    plt.ylabel('F(R)', fontfamily='Segoe UI', fontsize=12)
    plt.title(title, fontfamily='Segoe UI', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.gca().set_facecolor('#fafafa')
    plt.show()

def calculate_band_gap(E, F_R, transition_type='direct', material=None):
    """Menghitung energi band gap berdasarkan puncak F(R) dan penurunan tajam jika ada."""
    if transition_type == 'direct':
        y = (F_R * E)**2
        exponent = 2
    elif transition_type == 'indirect':
        y = (F_R * E)**0.5
        exponent = 0.5
    else:
        raise ValueError("Tipe transisi tidak valid")

    # Urutkan data berdasarkan energi (E)
    sorted_indices = np.argsort(E)
    E_sorted = E[sorted_indices]
    F_R_sorted = F_R[sorted_indices]
    y_sorted = y[sorted_indices]

    # Tentukan rentang energi berdasarkan material
    if material and material in MATERIAL_BAND_GAPS:
        e_min, e_max = MATERIAL_BAND_GAPS[material]
    else:
        e_min, e_max = 1.0, 4.0

    mask = (E_sorted >= e_min) & (E_sorted <= e_max)
    E_filtered = E_sorted[mask]
    F_R_filtered = F_R_sorted[mask]
    y_filtered = y_sorted[mask]

    if len(E_filtered) < 10:
        raise ValueError(f"Data dalam rentang energi {e_min}–{e_max} eV terlalu sedikit untuk analisis")

    # Hitung turunan pertama F(R) untuk menemukan puncak
    dF_R = np.diff(F_R_filtered) / np.diff(E_filtered)
    E_diff = (E_filtered[:-1] + E_filtered[1:]) / 2

    # Cari titik puncak (di mana F(R) maksimum)
    peak_idx = np.argmax(F_R_filtered)

    # Ambil turunan setelah puncak
    if peak_idx < len(dF_R):  # Pastikan ada data setelah puncak
        dF_R_after_peak = dF_R[peak_idx:]
        E_after_peak = E_diff[peak_idx:]
    else:
        # Jika puncak berada di ujung data, gunakan daerah sebelum puncak sebagai fallback
        dF_R_after_peak = dF_R[max(0, peak_idx - 10):peak_idx]
        E_after_peak = E_diff[max(0, peak_idx - 10):peak_idx]
        peak_idx = max(0, peak_idx - 10)

    # Cari daerah penurunan tajam (turunan negatif besar)
    negative_dF_R = dF_R_after_peak[dF_R_after_peak < 0]
    if len(negative_dF_R) > 0:
        dF_R_threshold = np.percentile(negative_dF_R, 10)  # 10% turunan negatif terbesar
        sharp_decline_indices = np.where(dF_R_after_peak <= dF_R_threshold)[0]
        if len(sharp_decline_indices) > 0:
            start_idx = peak_idx + sharp_decline_indices[0]
            start_idx = max(0, start_idx - 5)
            end_idx = min(len(E_filtered) - 1, start_idx + 20)
        else:
            # Jika tidak ada penurunan tajam, gunakan daerah setelah puncak
            start_idx = peak_idx
            end_idx = min(len(E_filtered) - 1, peak_idx + 20)
    else:
        # Jika tidak ada turunan negatif, gunakan daerah setelah puncak sebagai fallback
        start_idx = peak_idx
        end_idx = min(len(E_filtered) - 1, peak_idx + 20)

    if end_idx - start_idx < 2:
        # Jika daerah linier terlalu pendek, perluas secara default
        start_idx = max(0, peak_idx - 10)
        end_idx = min(len(E_filtered) - 1, peak_idx + 10)

    if end_idx - start_idx < 2:
        raise ValueError("Tidak dapat menemukan daerah linier yang cukup untuk fitting")

    # Ambil rentang data linier pada kurva Tauc
    E_linear = E_filtered[start_idx:end_idx + 1]
    y_linear = y_filtered[start_idx:end_idx + 1]

    # Lakukan linear fitting
    slope, intercept, _, _, _ = linregress(E_linear, y_linear)
    
    # Hitung titik potong dengan sumbu x
    band_gap = -intercept / slope

    # Validasi band gap
    if not e_min <= band_gap <= e_max:
        raise ValueError(f"Nilai band gap ({band_gap:.2f} eV) di luar rentang yang diharapkan ({e_min}–{e_max} eV)")

    return band_gap

def plot_tauc(E, F_R, transition_type='direct', material=None):
    """Memplot Tauc plot dengan kurva Kubelka-Munk sebagai latar belakang."""
    if transition_type == 'direct':
        y = (F_R * E)**2
        exponent = 2
    elif transition_type == 'indirect':
        y = (F_R * E)**0.5
        exponent = 0.5
    else:
        raise ValueError("Tipe transisi tidak valid")

    # Urutkan data berdasarkan energi (E)
    sorted_indices = np.argsort(E)
    E_sorted = E[sorted_indices]
    F_R_sorted = F_R[sorted_indices]
    y_sorted = y[sorted_indices]

    # Tentukan rentang energi berdasarkan material
    if material and material in MATERIAL_BAND_GAPS:
        e_min, e_max = MATERIAL_BAND_GAPS[material]
    else:
        e_min, e_max = 1.0, 4.0

    mask = (E_sorted >= e_min) & (E_sorted <= e_max)
    E_filtered = E_sorted[mask]
    F_R_filtered = F_R_sorted[mask]
    y_filtered = y_sorted[mask]

    if len(E_filtered) < 10:
        raise ValueError(f"Data dalam rentang energi {e_min}–{e_max} eV terlalu sedikit untuk analisis")

    # Hitung turunan pertama F(R)
    dF_R = np.diff(F_R_filtered) / np.diff(E_filtered)
    E_diff = (E_filtered[:-1] + E_filtered[1:]) / 2

    # Cari titik puncak
    peak_idx = np.argmax(F_R_filtered)

    # Ambil turunan setelah puncak
    if peak_idx < len(dF_R):
        dF_R_after_peak = dF_R[peak_idx:]
        E_after_peak = E_diff[peak_idx:]
    else:
        dF_R_after_peak = dF_R[max(0, peak_idx - 10):peak_idx]
        E_after_peak = E_diff[max(0, peak_idx - 10):peak_idx]
        peak_idx = max(0, peak_idx - 10)

    # Cari daerah penurunan tajam
    negative_dF_R = dF_R_after_peak[dF_R_after_peak < 0]
    if len(negative_dF_R) > 0:
        dF_R_threshold = np.percentile(negative_dF_R, 10)
        sharp_decline_indices = np.where(dF_R_after_peak <= dF_R_threshold)[0]
        if len(sharp_decline_indices) > 0:
            start_idx = peak_idx + sharp_decline_indices[0]
            start_idx = max(0, start_idx - 5)
            end_idx = min(len(E_filtered) - 1, start_idx + 20)
        else:
            start_idx = peak_idx
            end_idx = min(len(E_filtered) - 1, peak_idx + 20)
    else:
        start_idx = peak_idx
        end_idx = min(len(E_filtered) - 1, peak_idx + 20)

    if end_idx - start_idx < 2:
        start_idx = max(0, peak_idx - 10)
        end_idx = min(len(E_filtered) - 1, peak_idx + 10)

    if end_idx - start_idx < 2:
        raise ValueError("Tidak dapat menemukan daerah linier yang cukup untuk fitting")

    # Ambil rentang data linier
    E_linear = E_filtered[start_idx:end_idx + 1]
    y_linear = y_filtered[start_idx:end_idx + 1]

    # Lakukan linear fitting
    slope, intercept, _, _, _ = linregress(E_linear, y_linear)
    
    # Hitung titik potong
    band_gap = -intercept / slope

    # Validasi band gap
    if not e_min <= band_gap <= e_max:
        raise ValueError(f"Nilai band gap ({band_gap:.2f} eV) di luar rentang yang diharapkan ({e_min}–{e_max} eV)")

    # Plot Tauc dengan kurva Kubelka-Munk
    fig, ax1 = plt.subplots(figsize=(8, 6), facecolor='#fafafa')

    # Sumbu y kiri untuk Tauc plot
    ax1.plot(E_filtered, y_filtered, color='#333333', label='Data Tauc Plot')
    ax1.set_xlabel('Energi (eV)', fontfamily='Segoe UI', fontsize=12)
    ax1.set_ylabel(f'(F(R) E)^{exponent}', fontfamily='Segoe UI', fontsize=12, color='#333333')
    ax1.tick_params(axis='y', labelcolor='#333333')

    # Sumbu y kanan untuk F(R)
    ax2 = ax1.twinx()
    ax2.plot(E_filtered, F_R_filtered, color='blue', linestyle='--', alpha=0.5, label='F(R) (Kubelka-Munk)')
    ax2.set_ylabel('F(R)', fontfamily='Segoe UI', fontsize=12, color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Plot garis tangensial
    x_fit = np.array([e_min, max(E_linear) + 0.5])
    y_fit = slope * x_fit + intercept
    ax1.plot(x_fit, y_fit, 'r--', label=f'Garis Tangensial (E_g = {band_gap:.2f} eV)', linewidth=2)

    # Plot garis vertikal energi band gap
    y_min, y_max = min(y_filtered), max(y_filtered)
    ax1.vlines(x=band_gap, ymin=y_min, ymax=y_max, color='green', linestyle=':', 
               label=f'Energi Band Gap: {band_gap:.2f} eV', alpha=0.7, linewidth=2)
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    # Tambahkan anotasi
    ax1.annotate(f'E_g = {band_gap:.2f} eV', 
                 xy=(band_gap, 0), 
                 xytext=(band_gap + 0.2, y_max * 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                 fontsize=10, fontfamily='Segoe UI')

    # Tambahkan judul dan grid
    plt.title(f'Tauc Plot (Transisi {transition_type})', fontfamily='Segoe UI', fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_facecolor('#fafafa')

    # Gabungkan legenda dari kedua sumbu
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='best')

    plt.show()

    return band_gap