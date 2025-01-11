import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def plot_graph(gui, show_absorbance=True):
    if gui.canvas:
        gui.canvas.get_tk_widget().pack_forget()
    if gui.toolbar:
        gui.toolbar.pack_forget()

    figsize = (gui.fig_width_scale.get(), gui.fig_height_scale.get())
    fig, ax = plt.subplots(figsize=figsize)
    for i, df in enumerate(gui.data_frames):
        if show_absorbance:
            ax.plot(df['Lambda'], df['Absorbansi'], label=f"{gui.sample_names_var.get().split(',')[i].strip()} (Absorbansi)")
            if gui.show_peak_points.get():
                abs_max_idx = df['Absorbansi'].idxmax()
                max_lambda = df['Lambda'].iloc[abs_max_idx]
                max_abs = df['Absorbansi'].iloc[abs_max_idx]
                ax.scatter(max_lambda, max_abs, color='black', zorder=1, s=2)
                ax.text(max_lambda, max_abs, f'{max_abs:.2f}', color='black', fontsize=8, ha='left', va='bottom')
        else:
            ax.plot(df['Lambda'], df['Transmitansi'], label=f"{gui.sample_names_var.get().split(',')[i].strip()} (Transmitansi)")

    if gui.show_degradasi.get():
        degradasi_text = '\n'.join([f'% Degradasi {gui.sample_names_var.get().split(",")[0].strip()} ke {gui.sample_names_var.get().split(",")[i+1].strip()} Jam: {gui.degradasi_values[i]:.2f}%'
                                   for i in range(len(gui.degradasi_values))])
        ax.text(0.05, 0.95, degradasi_text, transform=ax.transAxes,
                fontsize=8, color='black', ha='left', va='top', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.25'))

    ax.set_xlabel('Panjang Gelombang (nm)')
    ax.set_ylabel('Absorbansi' if show_absorbance else 'Transmitansi')
    ax.set_title(gui.graph_title_var.get())

    if gui.show_legend.get():
        ax.legend(fontsize=8)

    ax.grid(True)

    gui.canvas = FigureCanvasTkAgg(fig, master=gui.graph_frame)
    gui.canvas.draw()
    gui.canvas.get_tk_widget().pack()

    gui.toolbar = NavigationToolbar2Tk(gui.canvas, gui.graph_frame)
    gui.toolbar.update()
    gui.toolbar.pack()