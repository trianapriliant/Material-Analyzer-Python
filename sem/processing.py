import pandas as pd

def process_sem_data(file_path):
    """
    Memproses data SEM dari file CSV.
    :param file_path: Path ke file data SEM.
    :return: DataFrame yang berisi data SEM.
    """
    # Baca data dari file CSV
    data = pd.read_csv(file_path)

    # Lakukan preprocessing data SEM di sini
    # Contoh: Membersihkan data, menghitung statistik, dll.

    return data