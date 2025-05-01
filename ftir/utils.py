import pandas as pd
import matplotlib.pyplot as plt

# Tabel rentang angka gelombang untuk gugus fungsi
FUNCTIONAL_GROUPS = [
    {"group": "O-H (Alcohol, Phenol)", "range": (3200, 3600), "description": "Kuat, lebar"},
    {"group": "O-H (Carboxylic Acid)", "range": (2500, 3600), "description": "Sangat lebar"},
    {"group": "N-H (Amine, Amide)", "range": (3350, 3500), "description": "Kuat, tajam"},
    {"group": "C-H (Alkane)", "range": (2840, 2950), "description": "Sedang hingga lemah"},
    {"group": "C-H (Alkene, Aromatic)", "range": (3000, 3100), "description": "Lemah"},
    {"group": "C≡N (Nitrile)", "range": (2200, 2260), "description": "Tajam, sedang"},
    {"group": "C≡C (Alkyne)", "range": (2100, 2260), "description": "Variabel, sering lemah"},
    {"group": "C=O (Ketone, Aldehyde)", "range": (1715, 1745), "description": "Kuat, tajam"},
    {"group": "C=O (Ester)", "range": (1720, 1750), "description": "Kuat, tajam"},
    {"group": "C=O (Carboxylic Acid)", "range": (1680, 1715), "description": "Kuat, tajam"},
    {"group": "C=C (Alkene)", "range": (1600, 1680), "description": "Lemah"},
    {"group": "C=C (Aromatic)", "range": (1400, 1600), "description": "Lemah, beberapa puncak"},
    {"group": "C-O (Alcohol, Ether)", "range": (1050, 1250), "description": "Kuat, beberapa puncak"},
    {"group": "NO₂ (Nitro)", "range": (1300, 1600), "description": "Kuat"},
]

def identify_functional_groups(data, peaks):
    """Mengidentifikasi gugus fungsi berdasarkan posisi puncak"""
    functional_groups = []
    for peak in peaks:
        wavenumber = data['wavenumber'].iloc[peak]
        for fg in FUNCTIONAL_GROUPS:
            low, high = fg['range']
            if low <= wavenumber <= high:
                functional_groups.append({
                    "wavenumber": wavenumber,
                    "group": fg['group'],
                    "description": fg['description']
                })
    return functional_groups

def export_to_excel(data, peaks, file_path):
    """Ekspor data dan puncak ke file Excel"""
    export_data = data.copy()
    export_data['Peak'] = False
    export_data.loc[peaks, 'Peak'] = True
    export_data.to_excel(file_path, index=False)

def export_plot(figure, file_path):
    """Ekspor plot ke file gambar"""
    figure.savefig(file_path)