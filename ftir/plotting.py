from ftir.utils import identify_functional_groups

def plot_raw_data(ax, data, plot_name):
    """Memplot data FTIR mentah menggunakan transmitansi"""
    if '%T' not in data.columns:
        raise ValueError("Data tidak memiliki kolom '%T'. Pastikan data telah dimuat dengan benar.")
    ax.clear()
    ax.plot(data['wavenumber'], data['%T'], label='Data Mentah', color='blue', linewidth=1.0)
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('% Transmittance')
    ax.set_title(plot_name)
    ax.invert_xaxis()  # Membalik sumbu x agar 4000 cm⁻¹ di kiri dan 400 cm⁻¹ di kanan
    ax.legend()
    ax.grid(True)

def plot_spectrum(ax, data, peaks, plot_name):
    """Memplot spektrum FTIR dengan puncak dan label gugus fungsi di bawah puncak"""
    if '%T_corrected' not in data.columns:
        raise ValueError("Data tidak memiliki kolom '%T_corrected'. Pastikan koreksi baseline telah dilakukan.")
    ax.clear()
    ax.plot(data['wavenumber'], data['%T_corrected'], label='Spektrum Dikoreksi', color='blue', linewidth=1.0)
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('% Transmittance')
    ax.set_title(plot_name)
    
    # Identifikasi gugus fungsi berdasarkan puncak
    functional_groups = identify_functional_groups(data, peaks)
    
    # Kelompokkan gugus fungsi berdasarkan wavenumber untuk menangani puncak yang sama
    grouped_groups = {}
    for fg in functional_groups:
        wavenumber = fg['wavenumber']
        if wavenumber not in grouped_groups:
            grouped_groups[wavenumber] = []
        grouped_groups[wavenumber].append(fg)
    
    # Tentukan parameter untuk posisi garis dan label
    y_min, y_max = ax.get_ylim()
    line_length = 2  # Panjang garis penunjuk dalam satuan %T
    label_gap = 3  # Jarak antar-label jika ada lebih dari satu gugus
    
    # Tandai puncak dengan garis pendek dan label gugus fungsi
    for wavenumber, groups in grouped_groups.items():
        # Ambil nilai transmitansi pada puncak
        transmittance = data['%T_corrected'][data['wavenumber'] == wavenumber].iloc[0]
        
        # Garis dimulai dari posisi dekat puncak (di bawah puncak)
        y_start = transmittance + 1  # Sedikit di bawah puncak
        y_end = y_start + line_length  # Panjang garis pendek
        
        # Gambar garis pendek tepat di bawah puncak
        ax.plot([wavenumber, wavenumber], [y_start, y_end], color='red', linestyle='--', alpha=0.5)
        
        # Tambahkan label untuk setiap gugus fungsi
        for idx, fg in enumerate(groups):
            # Hitung posisi y untuk label berdasarkan indeks gugus
            label_y_position = y_end + (idx + 1) * label_gap
            # Tambahkan offset horizontal kecil untuk menghindari tumpang tindih
            label_x_offset = idx * 30  # Geser sedikit ke samping untuk setiap label
            label_x_position = wavenumber - label_x_offset
            
            # Gambar garis penghubung dari ujung garis pendek ke posisi label
            ax.plot([wavenumber, label_x_position], [y_end, label_y_position], color='black', linestyle='-', alpha=0.3)
            
            # Tambahkan label gugus fungsi secara vertikal (ambruk ke bawah)
            ax.text(label_x_position, label_y_position, fg['group'], rotation=270, fontsize=8, color='black',
                    verticalalignment='top', horizontalalignment='center')
    
    # Sesuaikan batas sumbu y agar label terlihat
    max_label_space = max(len(groups) for groups in grouped_groups.values()) * label_gap + 5
    ax.set_ylim(y_min - max_label_space, y_max)
    
    ax.invert_xaxis()  # Membalik sumbu x agar 4000 cm⁻¹ di kiri dan 400 cm⁻¹ di kanan
    ax.legend()
    ax.grid(True)