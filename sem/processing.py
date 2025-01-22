import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans  # Mengganti KMeans dengan MiniBatchKMeans

def classify_brightness(image, n_clusters=3):
    # Pastikan gambar dalam format grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reshape gambar menjadi array 1D untuk clustering
    pixels = image.reshape(-1, 1)

    # Terapkan MiniBatchKMeans Clustering
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)  # Menggunakan MiniBatchKMeans
    kmeans.fit(pixels)

    # Rekonstruksi gambar berdasarkan hasil clustering
    clustered = kmeans.labels_.reshape(image.shape)
    clustered_image = np.uint8(kmeans.cluster_centers_)[clustered]

    return clustered_image, np.sort(kmeans.cluster_centers_.flatten())

def preprocess_image(image_path):
    """
    Muat gambar dan ubah ukurannya jika diperlukan.

    Parameters:
    - image_path: str, path ke file gambar SEM

    Returns:
    - image: np.ndarray, gambar SEM yang sudah dimuat
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Gambar tidak ditemukan di path: {image_path}")
    return image

if __name__ == "__main__":
    # Contoh penggunaan modul
    import matplotlib.pyplot as plt

    # Path ke gambar SEM
    image_path = "example_sem_image.jpg"  # Ganti dengan path Anda

    # Muat dan proses gambar
    image = preprocess_image(image_path)
    clustered_image, cluster_centers = classify_brightness(image, n_clusters=3)

    # Tampilkan hasil
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(image, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Clustered Image")
    plt.imshow(clustered_image, cmap="gray")
    plt.axis("off")

    plt.show()

    print("Cluster Centers (Brightness Levels):", cluster_centers)