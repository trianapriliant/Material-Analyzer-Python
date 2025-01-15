import matplotlib.pyplot as plt

def plot_sem_image(data):
    """
    Plot data SEM sebagai gambar.
    :param data: DataFrame yang berisi data SEM.
    :return: Figure dan Axes untuk grafik.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Contoh: Plot data SEM sebagai gambar grayscale
    ax.imshow(data.values, cmap="gray")
    ax.set_title("SEM Image")
    ax.axis("off")  # Sembunyikan sumbu

    return fig, ax