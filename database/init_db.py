# database/init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database/materials.db')
    cursor = conn.cursor()

    # Buat tabel uvvis_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uvvis_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_name TEXT NOT NULL,
            wavelength REAL NOT NULL,
            absorbance REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Buat tabel ftir_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ftir_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_name TEXT NOT NULL,
            wavenumber REAL NOT NULL,
            intensity REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Buat tabel sem_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sem_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_name TEXT NOT NULL,
            magnification INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Buat tabel analysis_results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_name TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            result TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()