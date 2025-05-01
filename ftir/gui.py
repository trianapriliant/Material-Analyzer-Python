import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ftir.processing import load_data, baseline_correction
from ftir.analysis import identify_peaks
from ftir.plotting import plot_spectrum, plot_raw_data
from ftir.utils import export_to_excel, export_plot, identify_functional_groups

class FtirWindow:
    def __init__(self, master):
        self.master = master
        master.title("Analisis FTIR")
        
        # Menu bar di pojok kiri atas
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)
        
        # Menu File untuk ekspor
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Ekspor Data ke Excel", command=self.export_data)
        self.file_menu.add_command(label="Ekspor Plot", command=self.export_plot)
        
        # Frame utama untuk membagi tata letak (kiri: kontrol, kanan: plot)
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame kiri untuk tombol, kontrol, dan tabel
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # Frame untuk tombol utama
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(fill=tk.X)
        
        # Tombol untuk memuat data
        self.load_button = tk.Button(self.button_frame, text="Muat Data FTIR", command=self.load_data)
        self.load_button.grid(row=0, column=0, padx=10, pady=5)
        
        # Input untuk nama plot
        self.plot_name_label = tk.Label(self.button_frame, text="Nama Plot:")
        self.plot_name_label.grid(row=0, column=1, padx=10, pady=5)
        self.plot_name_entry = tk.Entry(self.button_frame)
        self.plot_name_entry.grid(row=0, column=2, padx=10, pady=5)
        
        # Tombol untuk plot data mentah
        self.plot_raw_button = tk.Button(self.button_frame, text="Plot Data Mentah", command=self.plot_raw)
        self.plot_raw_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Tombol untuk koreksi baseline
        self.correct_button = tk.Button(self.button_frame, text="Koreksi Baseline", command=self.baseline_correction)
        self.correct_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Tombol untuk analisis puncak
        self.analyze_button = tk.Button(self.button_frame, text="Identifikasi Puncak", command=self.identify_peaks)
        self.analyze_button.grid(row=1, column=2, padx=10, pady=5)
        
        # Tombol untuk memplot spektrum yang dikoreksi
        self.plot_button = tk.Button(self.button_frame, text="Plot Spektrum Dikoreksi", command=self.plot_spectrum)
        self.plot_button.grid(row=2, column=0, padx=10, pady=5)
        
        # Frame untuk kontrol tampilan grafik
        self.control_frame = tk.Frame(self.left_frame)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        # Checkbox untuk mengatur tampilan grafik
        self.show_legend = tk.BooleanVar(value=True)
        self.show_peaks = tk.BooleanVar(value=True)
        self.show_groups = tk.BooleanVar(value=True)
        
        tk.Checkbutton(self.control_frame, text="Tampilkan Legend", variable=self.show_legend,
                       command=self.update_plot).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(self.control_frame, text="Tampilkan Puncak", variable=self.show_peaks,
                       command=self.update_plot).pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(self.control_frame, text="Tampilkan Gugus", variable=self.show_groups,
                       command=self.update_plot).pack(side=tk.LEFT, padx=5)
        
        # Frame untuk mode identifikasi gugus
        self.mode_frame = tk.Frame(self.left_frame)
        self.mode_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.mode_frame, text="Mode Identifikasi Gugus:").pack(side=tk.LEFT, padx=5)
        self.mode = tk.StringVar(value="auto")  # Default: otomatis
        tk.Radiobutton(self.mode_frame, text="Otomatis", variable=self.mode, value="auto",
                       command=self.update_table).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.mode_frame, text="Manual", variable=self.mode, value="manual",
                       command=self.update_table).pack(side=tk.LEFT, padx=5)
        
        # Frame untuk tabel puncak
        self.table_frame = tk.Frame(self.left_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.table = ttk.Treeview(self.table_frame, columns=("Wavenumber", "Gugus"), show="headings")
        self.table.heading("Wavenumber", text="Wavenumber (cm⁻¹)")
        self.table.heading("Gugus", text="Gugus Fungsional")
        self.table.pack(fill=tk.BOTH, expand=True)
        
        # Bind klik pada tabel untuk edit manual
        self.table.bind("<Double-1>", self.edit_table_cell)
        
        # Frame untuk checkbox gugus fungsional
        self.group_check_frame = tk.Frame(self.left_frame)
        self.group_check_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.group_check_frame, text="Pilih Gugus untuk Ditampilkan:").pack(anchor=tk.W)
        
        # Dictionary untuk menyimpan status centang gugus fungsional
        self.group_check_vars = {}
        
        # Frame kanan untuk plot dan toolbar
        self.plot_frame = tk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Figure untuk plotting dengan ukuran yang lebih besar
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Tambahkan toolbar navigasi
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Variabel untuk menyimpan data
        self.data = None
        self.corrected_data = None
        self.peaks = None
        self.functional_groups = None
        self.peak_table_data = []  # Simpan data puncak untuk tabel
        
    def load_data(self):
        """Memuat data FTIR dari file .txt"""
        file_path = filedialog.askopenfilename(filetypes=[("File Teks", "*.txt")])
        if file_path:
            self.data = load_data(file_path)
            messagebox.showinfo("Info", "Data dimuat dengan sukses")
        else:
            messagebox.showwarning("Peringatan", "Tidak ada file yang dipilih")
        
    def plot_raw(self):
        """Memplot data FTIR mentah menggunakan transmitansi"""
        if self.data is None:
            messagebox.showwarning("Peringatan", "Silakan muat data terlebih dahulu")
            return
        try:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Mentah"
            plot_raw_data(self.ax, self.data, plot_name)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat plotting data mentah: {str(e)}")
        
    def baseline_correction(self):
        """Menerapkan koreksi baseline"""
        if self.data is None:
            messagebox.showwarning("Peringatan", "Silakan muat data terlebih dahulu")
            return
        try:
            self.corrected_data = baseline_correction(self.data)
            messagebox.showinfo("Info", "Koreksi baseline diterapkan")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat koreksi baseline: {str(e)}")
        
    def identify_peaks(self):
        """Mengidentifikasi puncak pada data yang dikoreksi dan memperbarui tabel"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        try:
            self.peaks = identify_peaks(self.corrected_data)
            self.functional_groups = identify_functional_groups(self.corrected_data, self.peaks)
            
            # Simpan data puncak untuk tabel
            self.peak_table_data = []
            for wavenumber, peak in [(self.corrected_data['wavenumber'].iloc[p], p) for p in self.peaks]:
                groups = [fg['group'] for fg in self.functional_groups if fg['wavenumber'] == wavenumber]
                dominant_group = groups[0] if groups else "Tidak Diketahui"
                self.peak_table_data.append({"wavenumber": int(wavenumber), "group": dominant_group})
            
            # Perbarui functional_groups agar sesuai dengan peak_table_data
            self.functional_groups = [
                {"wavenumber": entry["wavenumber"], "group": entry["group"]}
                for entry in self.peak_table_data
            ]
            
            # Buat checkbox untuk setiap gugus fungsional
            self.create_group_checkboxes()
            
            # Perbarui tabel tanpa memperbarui plot
            self.update_table(update_plot=False)
            messagebox.showinfo("Info", f"{len(self.peaks)} puncak diidentifikasi")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat identifikasi puncak: {str(e)}")
        
    def create_group_checkboxes(self):
        """Buat checkbox untuk setiap gugus fungsional yang terdeteksi, dengan default dicentang untuk wavenumber > 1500"""
        # Hapus checkbox sebelumnya
        for widget in self.group_check_frame.winfo_children():
            if isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Label):
                widget.destroy()
        
        tk.Label(self.group_check_frame, text="Pilih Gugus untuk Ditampilkan:").pack(anchor=tk.W)
        
        # Reset dictionary status centang
        self.group_check_vars = {}
        
        # Buat checkbox untuk setiap wavenumber dan gugus
        for entry in self.peak_table_data:
            wavenumber = entry["wavenumber"]
            group = entry["group"]
            key = f"{wavenumber}_{group}"
            # Centang secara default hanya jika wavenumber > 1500
            self.group_check_vars[key] = tk.BooleanVar(value=(wavenumber > 1500))
            tk.Checkbutton(self.group_check_frame, 
                          text=f"{wavenumber} cm⁻¹: {group}",
                          variable=self.group_check_vars[key],
                          command=self.update_plot).pack(anchor=tk.W)
        
    def plot_spectrum(self):
        """Memplot spektrum FTIR yang dikoreksi"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        if self.peaks is None:
            messagebox.showwarning("Peringatan", "Silakan identifikasi puncak terlebih dahulu")
            return
        try:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Dikoreksi"
            # Filter gugus fungsional berdasarkan yang dicentang
            filtered_groups = self.get_filtered_functional_groups()
            plot_spectrum(self.ax, self.corrected_data, self.peaks, plot_name,
                          show_legend=self.show_legend.get(),
                          show_peaks=self.show_peaks.get(),
                          show_groups=self.show_groups.get(),
                          custom_functional_groups=filtered_groups)
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat plotting: {str(e)}")
        
    def update_plot(self):
        """Perbarui plot berdasarkan opsi tampilan"""
        if self.data is None:
            return
        self.ax.clear()
        if self.corrected_data is not None and self.peaks is not None:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Dikoreksi"
            # Filter gugus fungsional berdasarkan yang dicentang
            filtered_groups = self.get_filtered_functional_groups()
            plot_spectrum(self.ax, self.corrected_data, self.peaks, plot_name,
                          show_legend=self.show_legend.get(),
                          show_peaks=self.show_peaks.get(),
                          show_groups=self.show_groups.get(),
                          custom_functional_groups=filtered_groups)
        else:
            plot_name = self.plot_name_entry.get() or "Spektrum FTIR Mentah"
            plot_raw_data(self.ax, self.data, plot_name)
        self.canvas.draw()
    
    def get_filtered_functional_groups(self):
        """Filter gugus fungsional berdasarkan checkbox yang dicentang"""
        filtered_groups = []
        for entry in self.peak_table_data:
            wavenumber = entry["wavenumber"]
            group = entry["group"]
            key = f"{wavenumber}_{group}"
            if key in self.group_check_vars and self.group_check_vars[key].get():
                filtered_groups.append({"wavenumber": wavenumber, "group": group})
        return filtered_groups
    
    def update_table(self, update_plot=True):
        """Perbarui tabel berdasarkan mode identifikasi gugus"""
        # Kosongkan tabel
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Perbarui functional_groups berdasarkan peak_table_data
        if self.peak_table_data:
            if self.mode.get() == "auto":
                # Dalam mode otomatis, gunakan gugus fungsi bawaan
                temp_groups = identify_functional_groups(self.corrected_data, self.peaks)
                self.functional_groups = []
                for entry in self.peak_table_data:
                    for fg in temp_groups:
                        if fg['wavenumber'] == entry["wavenumber"]:
                            entry["group"] = fg['group']
                            break
                    self.functional_groups.append({
                        "wavenumber": entry["wavenumber"],
                        "group": entry["group"]
                    })
            else:
                # Dalam mode manual, gunakan gugus yang telah diedit
                self.functional_groups = [
                    {"wavenumber": entry["wavenumber"], "group": entry["group"]}
                    for entry in self.peak_table_data
                ]
        
        # Isi tabel
        for entry in self.peak_table_data:
            self.table.insert("", tk.END, values=(entry["wavenumber"], entry["group"]))
        
        # Perbarui checkbox gugus fungsional
        self.create_group_checkboxes()
        
        # Perbarui plot hanya jika diminta
        if update_plot:
            self.update_plot()
    
    def edit_table_cell(self, event):
        """Edit gugus fungsi di tabel secara manual dan perbarui plot"""
        if self.mode.get() != "manual":
            return
        
        selected_item = self.table.selection()
        if not selected_item:
            return
        
        item = self.table.item(selected_item)
        wavenumber = item['values'][0]
        
        # Buat jendela input untuk mengedit gugus
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Edit Gugus untuk Wavenumber {wavenumber}")
        
        tk.Label(edit_window, text="Gugus Fungsional:").pack()
        entry = tk.Entry(edit_window)
        entry.insert(0, item['values'][1])
        entry.pack()
        
        def save_edit():
            new_group = entry.get()
            # Perbarui data tabel
            for data_entry in self.peak_table_data:
                if data_entry["wavenumber"] == wavenumber:
                    data_entry["group"] = new_group
                    break
            # Perbarui functional_groups
            for fg in self.functional_groups:
                if fg["wavenumber"] == wavenumber:
                    fg["group"] = new_group
                    break
            # Perbarui tabel
            self.table.item(selected_item, values=(wavenumber, new_group))
            # Perbarui checkbox gugus fungsional
            self.create_group_checkboxes()
            # Perbarui plot
            self.update_plot()
            edit_window.destroy()
        
        tk.Button(edit_window, text="Simpan", command=save_edit).pack()
        
    def export_data(self):
        """Ekspor data ke Excel"""
        if self.corrected_data is None:
            messagebox.showwarning("Peringatan", "Silakan lakukan koreksi baseline terlebih dahulu")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("File Excel", "*.xlsx")])
        if file_path:
            try:
                export_to_excel(self.corrected_data, self.peaks, file_path)
                messagebox.showinfo("Info", "Data diekspor ke Excel")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat ekspor data: {str(e)}")
        
    def export_plot(self):
        """Ekspor plot ke file gambar"""
        if self.ax.get_lines() == []:
            messagebox.showwarning("Peringatan", "Tidak ada plot yang tersedia untuk diekspor")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("File PNG", "*.png")])
        if file_path:
            try:
                export_plot(self.figure, file_path)
                messagebox.showinfo("Info", "Plot diekspor")
            except Exception as e:
                messagebox.showerror("Error", f"Terjadi kesalahan saat ekspor plot: {str(e)}")