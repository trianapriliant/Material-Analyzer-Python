import cv2
import numpy as np
from sem.processing import classify_brightness

def detect_edges(image, method="canny", **kwargs):
    """
    Deteksi tepi pada gambar SEM menggunakan metode yang ditentukan.

    Parameters:
    - image: np.ndarray, gambar SEM (grayscale)
    - method: str, metode deteksi tepi ("canny" atau "sobel")
    - kwargs: parameter tambahan untuk metode yang dipilih

    Returns:
    - edges: np.ndarray, gambar dengan tepi yang terdeteksi
    """
    if method == "canny":
        # Parameter default Canny: thresholds 100 dan 200 jika tidak disediakan
        low_threshold = kwargs.get("low_threshold", 100)
        high_threshold = kwargs.get("high_threshold", 200)
        edges = cv2.Canny(image, low_threshold, high_threshold)
    elif method == "sobel":
        # Parameter default Sobel: gunakan kernel ukuran 3 jika tidak disediakan
        ksize = kwargs.get("ksize", 3)
        grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
        edges = cv2.magnitude(grad_x, grad_y)
        edges = np.uint8(np.clip(edges, 0, 255))
    else:
        raise ValueError("Metode deteksi tepi tidak dikenal. Gunakan 'canny' atau 'sobel'.")

    return edges

def calculate_particle_properties(edges):
    """
    Hitung properti partikel berdasarkan gambar tepi (edges).

    Parameters:
    - edges: np.ndarray, gambar tepi hasil deteksi

    Returns:
    - properties: list of dict, daftar properti partikel (luas, diameter, dll.)
    """
    # Temukan kontur dari gambar tepi
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    properties = []
    for contour in contours:
        # Hitung luas kontur
        area = cv2.contourArea(contour)

        if area > 0:  # Hindari kontur dengan luas nol
            # Hitung diameter ekuivalen (asumsi partikel lingkaran)
            equivalent_diameter = np.sqrt(4 * area / np.pi)

            # Tambahkan properti ke daftar
            properties.append({
                "area": area,
                "equivalent_diameter": equivalent_diameter
            })

    return properties

def process_and_analyze(image_path, n_clusters=3, edge_method="canny", **edge_kwargs):
    """
    Proses lengkap: klasifikasi brightness, deteksi tepi, dan analisis partikel.

    Parameters:
    - image_path: str, path ke file gambar SEM
    - n_clusters: int, jumlah cluster brightness
    - edge_method: str, metode deteksi tepi
    - edge_kwargs: parameter tambahan untuk deteksi tepi

    Returns:
    - clustered_image: np.ndarray, gambar brightness yang diklasifikasikan
    - edges: np.ndarray, gambar dengan tepi yang terdeteksi
    - properties: list of dict, properti partikel
    """
    # Muat gambar dan klasifikasikan brightness
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    clustered_image, _ = classify_brightness(image, n_clusters=n_clusters)

    # Deteksi tepi pada gambar brightness yang diklasifikasikan
    edges = detect_edges(clustered_image, method=edge_method, **edge_kwargs)

    # Analisis properti partikel
    properties = calculate_particle_properties(edges)

    return clustered_image, edges, properties

if __name__ == "__main__":
    # Contoh penggunaan modul
    import matplotlib.pyplot as plt

    # Path ke gambar SEM
    image_path = "example_sem_image.jpg"  # Ganti dengan path Anda

    # Proses dan analisis gambar
    clustered_image, edges, properties = process_and_analyze(image_path, n_clusters=3, edge_method="canny", low_threshold=50, high_threshold=150)

    # Tampilkan hasil
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE), cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Clustered Image")
    plt.imshow(clustered_image, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Edges")
    plt.imshow(edges, cmap="gray")
    plt.axis("off")

    plt.show()

    print("Particle Properties:")
    for i, prop in enumerate(properties):
        print(f"Particle {i + 1}: Area = {prop['area']:.2f}, Diameter = {prop['equivalent_diameter']:.2f}")
