import matplotlib.pyplot as plt
import numpy as np
import cv2


def plot_images(original, clustered, edges, figsize=(15, 5), cmap="gray"):
    """
    Plot gambar asli, clustered, dan edges secara berdampingan.
    
    Parameters:
    - original: np.ndarray, gambar asli
    - clustered: np.ndarray, gambar hasil klasifikasi brightness
    - edges: np.ndarray, gambar hasil deteksi tepi
    - figsize: tuple, ukuran figure matplotlib
    - cmap: str, colormap untuk menampilkan gambar (default: "gray")
    """
    # Pastikan gambar asli dalam format grayscale
    if len(original.shape) == 3:  # Gambar berwarna (3 channel)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    plt.figure(figsize=figsize)
    plt.subplot(1, 3, 1)
    plt.title("Original Image")
    plt.imshow(original, cmap=cmap)
    plt.axis("off")
    
    plt.subplot(1, 3, 2)
    plt.title("Clustered Image")
    plt.imshow(clustered, cmap=cmap)
    plt.axis("off")
    
    plt.subplot(1, 3, 3)
    plt.title("Edges")
    plt.imshow(edges, cmap=cmap)
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()


def plot_particle_histogram(properties, property_key="area", bins=10, figsize=(8, 5)):
    """
    Plot histogram dari properti partikel (misalnya luas atau diameter).
    
    Parameters:
    - properties: list of dict, daftar properti partikel
    - property_key: str, kunci properti yang ingin diplot ("area" atau "equivalent_diameter")
    - bins: int, jumlah bin pada histogram
    - figsize: tuple, ukuran figure matplotlib
    """
    if not properties:
        print("Tidak ada partikel yang terdeteksi. Histogram tidak dapat ditampilkan.")
        return
    
    # Validasi property_key
    if property_key not in ["area", "equivalent_diameter"]:
        raise ValueError("property_key harus 'area' atau 'equivalent_diameter'.")
    
    values = [prop[property_key] for prop in properties]
    plt.figure(figsize=figsize)
    plt.hist(values, bins=bins, color="skyblue", edgecolor="black")
    plt.title(f"Histogram of Particle {property_key.capitalize()}")
    plt.xlabel(property_key.capitalize() + (" (µm²)" if property_key == "area" else " (µm)"))
    plt.ylabel("Frequency")
    plt.grid(alpha=0.5)
    plt.show()

def plot_particle_overlay(original, contours, figsize=(10, 5)):
    """
    Plot overlay partikel pada gambar asli.
    
    Parameters:
    - original: np.ndarray, gambar asli (grayscale)
    - contours: list of np.ndarray, kontur partikel
    - figsize: tuple, ukuran figure matplotlib
    """
    if original is None:
        raise ValueError("Gambar asli harus berupa array numpy yang valid.")
    
    output_image = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)
    
    plt.figure(figsize=figsize)
    plt.title("Particle Overlay")
    plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    # Contoh penggunaan modul plotting
    from sem.analysis import process_and_analyze

    # Path ke gambar SEM
    image_path = "example_sem_image.jpg"  # Ganti dengan path Anda

    # Proses dan analisis gambar
    clustered_image, edges, properties = process_and_analyze(image_path, n_clusters=3, edge_method="canny", low_threshold=50, high_threshold=150)

    # Muat gambar asli
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Plot gambar
    plot_images(original_image, clustered_image, edges)

    # Plot histogram luas partikel
    plot_particle_histogram(properties, property_key="area", bins=15)

    # Plot histogram diameter ekuivalen
    plot_particle_histogram(properties, property_key="equivalent_diameter", bins=15)