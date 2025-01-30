import cv2
import numpy as np
from sem.processing import classify_brightness, preprocess_image

def detect_edges(image, method="canny", **kwargs):
    try:
        # Hapus dimensi tambahan jika ada
        if len(image.shape) == 3 and image.shape[2] == 1:
            image = np.squeeze(image, axis=2)
        
        # Validasi input
        if image is None or len(image.shape) != 2:
            raise ValueError("Input harus berupa gambar grayscale yang valid.")
        
        if method == "canny":
            low_threshold = kwargs.get("low_threshold", 100)
            high_threshold = kwargs.get("high_threshold", 200)
            edges = cv2.Canny(image, low_threshold, high_threshold)
        elif method == "sobel":
            ksize = kwargs.get("ksize", 3)
            grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
            grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
            edges = cv2.magnitude(grad_x, grad_y)
            edges = np.uint8(np.clip(edges, 0, 255))
        else:
            raise ValueError("Metode deteksi tepi tidak dikenal. Gunakan 'canny' atau 'sobel'.")
        
        return edges
    except Exception as e:
        print(f"Error in detect_edges: {e}")
        raise

    # debugging
    print("Edge detection complete.")
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def calculate_particle_properties(edges, min_area=50, min_circularity=0.7, pixel_to_um=1.0):
    try:
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        properties = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:
                continue
            
            perimeter = cv2.arcLength(contour, True)
            if perimeter == 0:
                continue
            circularity = (4 * np.pi * area) / (perimeter ** 2)
            if circularity < min_circularity:
                continue
            
            equivalent_diameter = np.sqrt(4 * area / np.pi)
            area_um = area * (pixel_to_um ** 2)
            diameter_um = equivalent_diameter * pixel_to_um
            
            properties.append({
                "area": area_um,
                "equivalent_diameter": diameter_um,
                "circularity": circularity
            })
            
            
        return properties
    except Exception as e:
        print(f"Error in calculate_particle_properties: {e}")
        raise
    
    # debugging
    print(f"Number of particles detected: {len(contours)}")
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        print(f"Particle {i + 1}: Area = {area:.2f} pixels^2")

def process_and_analyze(
    image_path, n_clusters=3, edge_method="canny", 
    min_area=50, min_circularity=0.7, pixel_to_um=1.0, **edge_kwargs
):
    try:
        # Muat dan preproses gambar
        preprocessed_image = preprocess_image(image_path)
        print(f"Preprocessed image shape: {preprocessed_image.shape}")
        
        # Klasifikasi brightness
        clustered_image, _ = classify_brightness(preprocessed_image, n_clusters=n_clusters)
        print(f"Clustered image shape: {clustered_image.shape}")
        
        # Deteksi tepi pada gambar brightness yang diklasifikasikan
        # Ubah low_threshold dan high_threshold sesuai kebutuhan dan sesuaikan dengan gambar tampilannya
        edges = detect_edges(clustered_image, method=edge_method, **edge_kwargs)
        print(f"Edges image shape: {edges.shape}")
        
        # Analisis properti partikel
        # Ubah min_area, min_circularity, dan pixel_to_um sesuai kebutuhan dan temukan yang ideal, ini direncanakan untuk ditampilkan di user interface agar pengguna dapat menentukan kesesuaiannya.
        properties = calculate_particle_properties(
            edges, min_area=10, min_circularity=0.5, pixel_to_um=1.0
        )
        print(f"Properties calculated: {len(properties)} particles detected.")
        
        return clustered_image, edges, properties
    except Exception as e:
        print(f"Error in process_and_analyze: {e}")
        raise

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