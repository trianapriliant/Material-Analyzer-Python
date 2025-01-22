import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from sem.analysis import process_and_analyze
import numpy as np

class SEMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SEM Analysis")

        # Variables
        self.image_path = None
        self.clustered_image = None
        self.edges = None
        self.properties = None
        self.scale = None  # Skala piksel per unit jarak asli
        self.line_coords = None  # Koordinat garis yang digambar

        # Layout setup
        self.setup_ui()

    def setup_ui(self):
        # Top frame for buttons
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", pady=10)

        # Button for selecting image
        select_button = tk.Button(top_frame, text="Select Image", command=self.load_and_process_image, height=2)
        select_button.pack(side="left", padx=5)

        # Button for drawing scale line
        draw_line_button = tk.Button(top_frame, text="Draw Scale Line", command=self.draw_scale_line, height=2)
        draw_line_button.pack(side="left", padx=5)

        # Button for setting scale
        set_scale_button = tk.Button(top_frame, text="Set Scale", command=self.set_scale, height=2)
        set_scale_button.pack(side="left", padx=5)

        # Main frame for image display and results
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Notebook (Tab) for images
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Frame for original image
        self.original_frame = tk.Frame(self.notebook)
        self.notebook.add(self.original_frame, text="Original Image")

        # Frame for clustered image
        self.clustered_frame = tk.Frame(self.notebook)
        self.notebook.add(self.clustered_frame, text="Clustered Image")

        # Frame for edges
        self.edges_frame = tk.Frame(self.notebook)
        self.notebook.add(self.edges_frame, text="Edges")

        # Text frame for results (smaller area on the right)
        self.result_frame = tk.Frame(main_frame)
        self.result_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Results text box
        self.result_text = tk.Text(self.result_frame, width=40, height=25, wrap="word")
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("1.0", "Results will be displayed here...")
        self.result_text.config(state="disabled")

    def load_and_process_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
        )

        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        self.image_path = file_path

        try:
            # Process image
            self.clustered_image, self.edges, self.properties = process_and_analyze(
                self.image_path, n_clusters=3, edge_method="canny", low_threshold=50, high_threshold=150
            )
            self.display_images()
            self.display_results()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the image: {e}")

    def display_images(self):
        # Clear previous images
        for widget in self.original_frame.winfo_children():
            widget.destroy()
        for widget in self.clustered_frame.winfo_children():
            widget.destroy()
        for widget in self.edges_frame.winfo_children():
            widget.destroy()

        # Original Image
        original_image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        self.display_image_on_tab(self.original_frame, original_image, "Original Image")

        # Clustered Image
        self.display_image_on_tab(self.clustered_frame, self.clustered_image, "Clustered Image")

        # Edges
        self.display_image_on_tab(self.edges_frame, self.edges, "Edges")

    def display_image_on_tab(self, frame, image, title):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_title(title)
        ax.imshow(image, cmap="gray")
        ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Connect the mouse click event to the canvas (only for original image)
        if frame == self.original_frame:
            canvas.mpl_connect("button_press_event", self.on_canvas_click)

    def on_canvas_click(self, event):
        if self.line_coords is None:
            self.line_coords = [(event.xdata, event.ydata)]
        else:
            self.line_coords.append((event.xdata, event.ydata))
            self.draw_line_on_canvas()

    def draw_line_on_canvas(self):
        if len(self.line_coords) == 2:
            # Draw the line on the original image tab
            fig = self.original_frame.winfo_children()[0].figure
            ax = fig.axes[0]
            ax.plot([self.line_coords[0][0], self.line_coords[1][0]], [self.line_coords[0][1], self.line_coords[1][1]], color='red')
            self.original_frame.winfo_children()[0].draw()

    def draw_scale_line(self):
        self.line_coords = None
        messagebox.showinfo("Info", "Click on the image to draw a line for scale.")

    def set_scale(self):
        if self.line_coords is None or len(self.line_coords) < 2:
            messagebox.showerror("Error", "Please draw a line first.")
            return

        # Calculate the length of the line in pixels
        dx = self.line_coords[1][0] - self.line_coords[0][0]
        dy = self.line_coords[1][1] - self.line_coords[0][1]
        length_pixels = np.sqrt(dx**2 + dy**2)

        # Ask user for the real-world distance
        real_distance = simpledialog.askfloat("Input", "Enter the real-world distance corresponding to the line (in units):")
        if real_distance is None or real_distance <= 0:
            messagebox.showerror("Error", "Invalid distance entered.")
            return

        # Calculate the scale (pixels per unit)
        self.scale = length_pixels / real_distance
        messagebox.showinfo("Scale Set", f"Scale set to {self.scale:.2f} pixels per unit.")

        # Update results with scaled measurements
        self.display_results()

    def display_results(self):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        if not self.properties:
            self.result_text.insert("1.0", "No particles detected.")
        else:
            self.result_text.insert("1.0", "Detected Particles:\n")
            for i, prop in enumerate(self.properties):
                area = prop['area']
                diameter = prop['equivalent_diameter']
                if self.scale:
                    area_scaled = area / (self.scale ** 2)
                    diameter_scaled = diameter / self.scale
                    self.result_text.insert(
                        "end",
                        f"Particle {i + 1}: Area = {area_scaled:.2f} units^2, Diameter = {diameter_scaled:.2f} units\n"
                    )
                else:
                    self.result_text.insert(
                        "end",
                        f"Particle {i + 1}: Area = {area:.2f} pixels^2, Diameter = {diameter:.2f} pixels\n"
                    )

        self.result_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = SEMGUI(root)
    root.mainloop()