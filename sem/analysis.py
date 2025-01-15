import numpy as np

def analyze_particle_size(data):
    """
    Menganalisis ukuran partikel dari data SEM.
    :param data: DataFrame yang berisi data SEM.
    :return: Dictionary yang berisi hasil analisis.
    """
    # Contoh: Hitung ukuran partikel
    particle_sizes = np.random.rand(10) * 100  # Contoh data acak
    return {
        "mean_size": np.mean(particle_sizes),
        "std_size": np.std(particle_sizes),
    }