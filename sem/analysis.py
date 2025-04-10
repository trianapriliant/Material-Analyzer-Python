import cv2
import numpy as np
from sem.processing import classify_brightness, preprocess_image

def detect_edges(cleaned_image, method="canny", **kwargs):
    try:
        # Hapus dimensi tambahan jika ada
        if len(cleaned_image.shape) == 3 and cleaned_image.shape[2] == 1:
            cleaned_image = np.squeeze(cleaned_image, axis=2)
        
        # Validasi input
        if cleaned_image is None or len(cleaned_image.shape) != 2:
            raise ValueError("Input harus berupa gambar grayscale yang valid.")
        
        if method == "canny":
            low_threshold = kwargs.get("low_threshold", 100)
            high_threshold = kwargs.get("high_threshold", 200)
            edges = cv2.Canny(cleaned_image, low_threshold, high_threshold)
            
        elif method == "sobel":
            ksize = kwargs.get("ksize", 3)
            grad_x = cv2.Sobel(cleaned_image, cv2.CV_64F, 1, 0, ksize=ksize)
            grad_y = cv2.Sobel(cleaned_image, cv2.CV_64F, 0, 1, ksize=ksize)
            edges = cv2.magnitude(grad_x, grad_y)
            edges = np.uint8(np.clip(edges, 0, 255))
        else:
            raise ValueError("Metode deteksi tepi tidak dikenal. Gunakan 'canny' atau 'sobel'.")
        
        # Debugging
        print("Edge detection complete.")
        print(f"Edges image shape: {edges.shape}")
        # cv2.imshow("Edges", edges)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        return edges
    except Exception as e:
        print(f"Error in detect_edges: {e}")
        raise

def process_and_analyze(
    image_path, n_clusters=3, edge_method="canny", 
    min_area=None, min_circularity=None, pixel_to_um=1.0, **edge_kwargs
):
    # Gunakan nilai default jika parameter tidak diberikan
    min_area = min_area if min_area is not None else 50
    min_circularity = min_circularity if min_circularity is not None else 0.7
    
    # Validasi: Pastikan min_area dan min_circularity diberikan
    if min_area is None or min_circularity is None:
        raise ValueError("min_area and min_circularity must be provided.")
    
    #if min_area is None or min_circularity is None:
    #    raise ValueError("min_area and min_circularity must be provided.")
    
    try:
        # Muat dan preproses gambar
        preprocessed_image = preprocess_image(image_path)
        print(f"Preprocessed image shape: {preprocessed_image.shape}")
        
        # Klasifikasi brightness
        clustered_image, _ = classify_brightness(preprocessed_image, n_clusters=n_clusters)
        print(f"Clustered image shape: {clustered_image.shape}")
        
        # Deteksi tepi pada gambar brightness yang diklasifikasikan
        edges = detect_edges(clustered_image, method=edge_method, **edge_kwargs)
        print(f"Edges image shape: {edges.shape}")
        
        # Distance Transform dan Watershed
        dist_transform = cv2.distanceTransform(edges, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(edges, sure_fg)

        # Connected Components
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        # Pastikan markers berformat CV_32SC1
        markers = np.int32(markers)
        
        # Pastikan clustered_image berupa citra 3-channel (BGR)
        if len(clustered_image.shape) == 2:  # Grayscale
            clustered_image_bgr = cv2.cvtColor(clustered_image, cv2.COLOR_GRAY2BGR)
        else:
            clustered_image_bgr = clustered_image
        
        # Watershed
        markers = cv2.watershed(clustered_image_bgr, markers)
        segmented_image = clustered_image_bgr.copy()
        segmented_image[markers == -1] = [0, 255, 0]  # Tandai batas partikel
        
        # Analisis properti partikel
        properties = calculate_particle_properties(
            edges, min_area=min_area, min_circularity=min_circularity, pixel_to_um=pixel_to_um
        )
        print(f"Properties calculated: {len(properties)} particles detected.")
        #debugging
        print(f"Parameters passed to process_and_analyze: min_area={min_area}, min_circularity={min_circularity}")
        
        print(f"Clustered image type: {clustered_image.dtype}, shape: {clustered_image.shape}")
        print(f"Markers type: {markers.dtype}, shape: {markers.shape}")
        
        # Debugging
        print("Segmentation complete.")
        print(f"Markers shape: {markers.shape}")
        cv2.imshow("Segmented Image", segmented_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return clustered_image, edges, properties
    except Exception as e:
        print(f"Error in process_and_analyze: {e}")
        raise
    #debugging
    
def calculate_particle_properties(edges, min_area, min_circularity, pixel_to_um=1.0):
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
            
            #debugging
            print(f"Parameters received by calculate_particle_properties: min_area={min_area}, min_circularity={min_circularity}")
        
        # Debugging
            print(f"Number of particles detected: {len(contours)}")
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                perimeter = cv2.arcLength(contour, True)
                circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
                print(f"Particle {i + 1}: Area={area:.2f}, Circularity={circularity:.2f}")
        
        return properties, contours
    except Exception as e:
        print(f"Error in calculate_particle_properties: {e}")
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