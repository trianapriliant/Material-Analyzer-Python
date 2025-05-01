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
    
    # Atur rentang sumbu y dari 10 hingga maksimum
    y_min = 10
    y_max = data['%T'].max() + 5  # Tambahkan sedikit ruang di atas nilai maksimum
    ax.set_ylim(y_min, y_max)
    
    ax.legend()
    ax.grid(True)

def plot_spectrum(ax, data, peaks, plot_name):
    """Memplot spektrum FTIR dengan puncak, label angka gelombang, dan gugus fungsi di bawah garis spektrum"""
    if '%T_corrected' not in data.columns:
        raise ValueError("Data tidak memiliki kolom '%T_corrected'. Pastikan koreksi baseline telah dilakukan.")
    ax.clear()
    ax.plot(data['wavenumber'], data['%T_corrected'], label='Spektrum Dikoreksi', color='blue', linewidth=1.0)
    ax.set_xlabel('Wavenumber (cm⁻¹)')
    ax.set_ylabel('% Transmittance')
    ax.set_title(plot_name)
    
    # Identifikasi gugus fungsi berdasarkan puncak
    functional_groups = identify_functional_groups(data, peaks)
    
    # Kelompokkan gugus fungsi berdasarkan wavenumber
    grouped_groups = {}
    for fg in functional_groups:
        wavenumber = fg['wavenumber']
        if wavenumber not in grouped_groups:
            grouped_groups[wavenumber] = []
        grouped_groups[wavenumber].append(fg)
    
    # Urutkan puncak berdasarkan wavenumber untuk menangani tumpang tindih
    peak_info = [(data['wavenumber'].iloc[peak], peak) for peak in peaks]
    peak_info.sort(key=lambda x: x[0], reverse=True)  # Urutkan dari besar ke kecil (karena sumbu x terbalik)
    
    # Tentukan parameter untuk posisi garis dan label
    y_data_min = data['%T_corrected'].min()
    y_data_max = data['%T_corrected'].max()
    line_length = -3  # Panjang garis penunjuk dalam satuan %T
    label_gap = -10  # Jarak antar-label (wavenumber dan gugus fungsi)
    
    # Tentukan posisi dasar di bawah garis spektrum
    # Ambil nilai minimum %T pada setiap wavenumber untuk memastikan posisi di bawah garis
    base_y_positions = {}
    for wavenumber, peak in peak_info:
        transmittance = data['%T_corrected'].iloc[peak]
        base_y_positions[wavenumber] = transmittance - 1  # Mulai dari posisi di bawah garis
    
    # Tandai puncak dengan garis pendek, label wavenumber, dan gugus fungsi
    label_positions = []  # Simpan posisi label untuk mendeteksi tumpang tindih
    for wavenumber, peak in peak_info:
        # Ambil posisi dasar di bawah garis
        y_start = base_y_positions[wavenumber]
        y_end = y_start + line_length  # Panjang garis pendek
        
        # Gambar garis pendek di bawah garis spektrum
        ax.plot([wavenumber, wavenumber], [y_start, y_end], color='black', linestyle='-', alpha=0.5)
        
        # Tentukan posisi label wavenumber
        label_y_position = y_end
        label_x_position = wavenumber
        
        # Cek tumpang tindih dengan label sebelumnya
        label_width = 50  # Perkiraan lebar label dalam satuan wavenumber
        overlap = True
        offset_idx = 0
        while overlap:
            overlap = False
            for prev_x, prev_idx in label_positions:
                if abs(label_x_position - prev_x) < label_width:
                    # Jika tumpang tindih, geser ke samping (ke kiri, karena sumbu x terbalik)
                    offset_idx += 1
                    label_x_position = wavenumber - offset_idx * label_width
                    overlap = True
                    break
        
        # Tambahkan label angka gelombang secara vertikal (ambruk ke bawah)
        ax.text(label_x_position, label_y_position, f"{int(wavenumber)}", rotation=270, fontsize=8, color='black',
                verticalalignment='top', horizontalalignment='center')
        
        # Pilih gugus fungsi dominan (misalnya, yang pertama dalam daftar)
        if wavenumber in grouped_groups and grouped_groups[wavenumber]:
            dominant_group = grouped_groups[wavenumber][0]['group']  # Ambil gugus pertama sebagai dominan
            # Tambahkan label gugus fungsi di bawah label wavenumber
            group_y_position = label_y_position + label_gap
            ax.text(label_x_position, group_y_position, dominant_group, rotation=270, fontsize=8, color='black',
                    verticalalignment='top', horizontalalignment='center')
        
        # Simpan posisi label untuk pemeriksaan tumpang tindih berikutnya
        label_positions.append((label_x_position, peak))
    
    # Atur rentang sumbu y dari 10 hingga maksimum
    y_min = 0
    y_max = y_data_max + 5  # Tambahkan sedikit ruang di atas nilai maksimum
    # Sesuaikan batas sumbu y agar semua label terlihat
    max_label_space = 20 + label_gap  # Ruang untuk wavenumber dan gugus fungsi
    ax.set_ylim(y_min - max_label_space, y_max)
    
    ax.invert_xaxis()  # Membalik sumbu x agar 4000 cm⁻¹ di kiri dan 400 cm⁻¹ di kanan
    ax.legend()
    ax.grid(True)