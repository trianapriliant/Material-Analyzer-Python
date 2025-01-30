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
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(pixels)
    
    # Rekonstruksi gambar berdasarkan hasil clustering
    clustered = kmeans.labels_.reshape(image.shape)
    clustered_image = np.uint8(kmeans.cluster_centers_)[clustered]
    
    # Pastikan output adalah 2D array
    if len(clustered_image.shape) == 3 and clustered_image.shape[2] == 1:
        clustered_image = np.squeeze(clustered_image, axis=2)
    
    #debugging
    print(f"Clustered image shape after processing: {clustered_image.shape}")    
    
    return clustered_image, np.sort(kmeans.cluster_centers_.flatten())


def preprocess_image(image_path, blur_kernel=(5, 5), morph_kernel_size=3):
    """
    Muat gambar dan ubah ukurannya jika diperlukan.
    
    Parameters:
    - image_path: str, path ke file gambar SEM.
    - blur_kernel: tuple, ukuran kernel untuk Gaussian Blur.
    - morph_kernel_size: int, ukuran kernel untuk operasi morfologi.
    
    Returns:
    - binary_image: np.ndarray, gambar biner hasil preprocessing.
    """
    # Baca gambar
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Gambar tidak ditemukan di path: {image_path}")
    
    # Konversi ke grayscale jika gambar berwarna
    if len(image.shape) == 3:  # Gambar berwarna (3 channel)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gaussian Blur untuk mengurangi noise
    blurred = cv2.GaussianBlur(image, blur_kernel, 0)
    
    # Thresholding menggunakan Otsu's Method
    _, binary_image = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Operasi morfologi untuk membersihkan noise kecil
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (morph_kernel_size, morph_kernel_size))
    cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)
    print(f"Image shape after preprocessing: {image.shape}")
    return cleaned_image

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