import tkinter as tk
from tkinter import filedialog, messagebox
from uvvis.uvvisdrs import processing, plotting

def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return

    try:
        wl, R = processing.load_reflectance_data(filepath)
        km = processing.kubelka_munk(R)
        hv, y_direct = processing.tauc_plot(wl, km, bandgap_type="direct")

        plotting.plot_reflectance(wl, R)
        plotting.plot_kubelka_munk(wl, km)
        plotting.plot_tauc(hv, y_direct, "direct")
        
        messagebox.showinfo("Success", "Plots generated successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup GUI
root = tk.Tk()
root.title("UV-Vis DRS Analyzer")

btn = tk.Button(root, text="Load CSV and Analyze", command=browse_file)
btn.pack(pady=20, padx=20)

root.mainloop()
