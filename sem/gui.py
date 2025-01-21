import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from sem.analysis import process_and_analyze

class SEMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SEM Analysis GUI")

        # Variables
        self.image_path = None
        self.clustered_image = None
        self.edges = None
        self.properties = None

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Frame for file selection
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10, padx=10, fill="x")

        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)

        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side="left")

        process_button = ttk.Button(file_frame, text="Process", command=self.process_image)
        process_button.pack(side="left", padx=5)

        # Canvas for displaying images
        self.image_canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.image_canvas.pack(pady=10)

        # Result display
        self.result_text = tk.Text(self.root, height=10, wrap="word")
        self.result_text.pack(pady=10, padx=10, fill="x")
        self.result_text.insert("1.0", "Results will be displayed here...")
        self.result_text.config(state="disabled")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def process_image(self):
        self.image_path = self.file_entry.get()
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return

        try:
            # Process the image using analysis module
            self.clustered_image, self.edges, self.properties = process_and_analyze(
                self.image_path, n_clusters=3, edge_method="canny", low_threshold=50, high_threshold=150
            )

            # Display results
            self.display_images()
            self.display_results()

        except FileNotFoundError:
            messagebox.showerror("Error", "The selected file was not found.")
        except cv2.error as e:
            messagebox.showerror("Error", f"OpenCV error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def display_images(self):
        # Load original image
        original_image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        # Create a new figure for displaying results using matplotlib
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        ax1.set_title("Original Image")
        ax1.imshow(original_image, cmap="gray")
        ax1.axis("off")

        ax2.set_title("Clustered Image")
        ax2.imshow(self.clustered_image, cmap="gray")
        ax2.axis("off")

        ax3.set_title("Edges")
        ax3.imshow(self.edges, cmap="gray")
        ax3.axis("off")

        # Embed the plot in the Tkinter GUI
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def display_results(self):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        if not self.properties:
            self.result_text.insert("1.0", "No particles detected.")
        else:
            self.result_text.insert("1.0", "Detected Particles:\n")
            for i, prop in enumerate(self.properties):
                self.result_text.insert(
                    "end", f"Particle {i + 1}: Area = {prop['area']:.2f}, Diameter = {prop['equivalent_diameter']:.2f}\n"
                )

        self.result_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    SEMGUI(root)
    root.mainloop()