import os
import cv2
import numpy as np

def load_image(image_path):
    """
    Muat gambar dari path yang diberikan.

    Parameters:
    - image_path: str, path ke file gambar

    Returns:
    - image: np.ndarray, gambar dalam format grayscale
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Gambar tidak ditemukan di path: {image_path}")

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Gambar tidak dapat dimuat. Pastikan format file didukung.")

    return image

def save_image(image, save_path):
    """
    Simpan gambar ke path yang diberikan.

    Parameters:
    - image: np.ndarray, gambar untuk disimpan
    - save_path: str, path tujuan penyimpanan
    """
    cv2.imwrite(save_path, image)

def normalize_image(image):
    """
    Normalisasi intensitas gambar ke rentang [0, 255].

    Parameters:
    - image: np.ndarray, gambar input

    Returns:
    - normalized_image: np.ndarray, gambar yang dinormalisasi
    """
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image

def resize_image(image, width=None, height=None):
    """
    Ubah ukuran gambar sesuai dimensi yang diberikan sambil mempertahankan aspek rasio.

    Parameters:
    - image: np.ndarray, gambar input
    - width: int, lebar baru (opsional)
    - height: int, tinggi baru (opsional)

    Returns:
    - resized_image: np.ndarray, gambar yang telah diubah ukurannya
    """
    if width is None and height is None:
        return image  # Tidak ada perubahan ukuran jika dimensi tidak diberikan

    h, w = image.shape[:2]
    if width is not None:
        aspect_ratio = width / w
        new_size = (width, int(h * aspect_ratio))
    elif height is not None:
        aspect_ratio = height / h
        new_size = (int(w * aspect_ratio), height)

    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    return resized_image

def apply_mask(image, mask):
    """
    Terapkan mask pada gambar, hanya mempertahankan bagian yang sesuai dengan mask.

    Parameters:
    - image: np.ndarray, gambar input
    - mask: np.ndarray, mask biner

    Returns:
    - masked_image: np.ndarray, hasil gambar setelah mask diterapkan
    """
    if image.shape != mask.shape:
        raise ValueError("Dimensi gambar dan mask harus sama.")

    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image

if __name__ == "__main__":
    # Contoh penggunaan modul
    image_path = "example_sem_image.jpg"  # Ganti dengan path Anda

    # Muat gambar
    try:
        image = load_image(image_path)
        print("Gambar berhasil dimuat.")
    except (FileNotFoundError, ValueError) as e:
        print(e)

    # Normalisasi gambar
    normalized = normalize_image(image)

    # Ubah ukuran gambar
    resized = resize_image(normalized, width=300)

    # Simpan hasil gambar
    save_image(resized, "resized_image.jpg")
    print("Gambar berhasil disimpan sebagai resized_image.jpg.")