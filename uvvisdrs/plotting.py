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
    """Menghitung energi band gap tanpa menampilkan plot."""
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
    y_sorted = y[sorted_indices]

    # Tentukan rentang energi berdasarkan material
    if material and material in MATERIAL_BAND_GAPS:
        e_min, e_max = MATERIAL_BAND_GAPS[material]
    else:
        e_min, e_max = 1.0, 4.0  # Default jika material tidak dikenal

    mask = (E_sorted >= e_min) & (E_sorted <= e_max)
    E_filtered = E_sorted[mask]
    y_filtered = y_sorted[mask]

    if len(E_filtered) < 10:
        raise ValueError(f"Data dalam rentang energi {e_min}–{e_max} eV terlalu sedikit untuk analisis")

    # Hitung turunan pertama dan kedua untuk menemukan daerah linier
    dy = np.diff(y_filtered) / np.diff(E_filtered)
    d2y = np.diff(dy) / np.diff(E_filtered[:-1])  # Turunan kedua
    E_diff = (E_filtered[:-2] + E_filtered[2:]) / 2

    # Cari titik infleksi (d2y mendekati nol) untuk mendeteksi awal transisi
    inflection_points = np.where(np.abs(d2y) < np.percentile(np.abs(d2y), 20))[0]
    
    if len(inflection_points) > 0:
        start_idx = inflection_points[0]
        # Cari daerah linier setelah titik infleksi
        dy_region = dy[start_idx:]
        E_region = E_filtered[start_idx:-1]
        # Fokus pada daerah dengan turunan tertinggi setelah titik infleksi
        dy_percentile = np.percentile(dy_region, 50)
        linear_region = np.where(dy_region > dy_percentile)[0]
        if len(linear_region) > 0:
            start_idx = start_idx + linear_region[0]
            end_idx = start_idx + linear_region[-1] + 1
        else:
            end_idx = start_idx + len(dy_region) // 2
    else:
        mid_idx = len(E_filtered) // 2
        start_idx = mid_idx - len(E_filtered) // 8
        end_idx = mid_idx + len(E_filtered) // 8

    if end_idx - start_idx < 2:
        raise ValueError("Tidak dapat menemukan daerah linier yang cukup untuk fitting")

    # Ambil rentang data linier
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
    """Memplot Tauc plot berdasarkan tipe transisi dan menghitung energi band gap."""
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
    y_sorted = y[sorted_indices]

    # Tentukan rentang energi berdasarkan material
    if material and material in MATERIAL_BAND_GAPS:
        e_min, e_max = MATERIAL_BAND_GAPS[material]
    else:
        e_min, e_max = 1.0, 4.0

    mask = (E_sorted >= e_min) & (E_sorted <= e_max)
    E_filtered = E_sorted[mask]
    y_filtered = y_sorted[mask]

    if len(E_filtered) < 10:
        raise ValueError(f"Data dalam rentang energi {e_min}–{e_max} eV terlalu sedikit untuk analisis")

    # Hitung turunan pertama dan kedua
    dy = np.diff(y_filtered) / np.diff(E_filtered)
    d2y = np.diff(dy) / np.diff(E_filtered[:-1])
    E_diff = (E_filtered[:-2] + E_filtered[2:]) / 2

    # Cari titik infleksi
    inflection_points = np.where(np.abs(d2y) < np.percentile(np.abs(d2y), 20))[0]
    
    if len(inflection_points) > 0:
        start_idx = inflection_points[0]
        dy_region = dy[start_idx:]
        E_region = E_filtered[start_idx:-1]
        dy_percentile = np.percentile(dy_region, 50)
        linear_region = np.where(dy_region > dy_percentile)[0]
        if len(linear_region) > 0:
            start_idx = start_idx + linear_region[0]
            end_idx = start_idx + linear_region[-1] + 1
        else:
            end_idx = start_idx + len(dy_region) // 2
    else:
        mid_idx = len(E_filtered) // 2
        start_idx = mid_idx - len(E_filtered) // 8
        end_idx = mid_idx + len(E_filtered) // 8

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

    # Plot Tauc plot
    plt.figure(figsize=(8, 6), facecolor='#fafafa')
    plt.plot(E_filtered, y_filtered, color='#333333', label='Data Tauc Plot')
    
    # Plot garis tangensial
    x_fit = np.array([min(E_linear), band_gap])
    y_fit = slope * x_fit + intercept
    plt.plot(x_fit, y_fit, 'r--', label=f'Garis Tangensial (E_g = {band_gap:.2f} eV)', linewidth=2)
    
    # Plot titik potong
    plt.axvline(x=band_gap, color='green', linestyle=':', label=f'Energi Band Gap: {band_gap:.2f} eV', alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    # Tambahkan anotasi
    plt.annotate(f'E_g = {band_gap:.2f} eV', 
                 xy=(band_gap, 0), 
                 xytext=(band_gap + 0.2, max(y_filtered) * 0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                 fontsize=10, fontfamily='Segoe UI')

    plt.xlabel('Energi (eV)', fontfamily='Segoe UI', fontsize=12)
    plt.ylabel(f'(F(R) E)^{exponent}', fontfamily='Segoe UI', fontsize=12)
    plt.title(f'Tauc Plot (Transisi {transition_type})', fontfamily='Segoe UI', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.gca().set_facecolor('#fafafa')
    plt.show()

    return band_gap