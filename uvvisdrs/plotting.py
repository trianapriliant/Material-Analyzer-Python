import matplotlib.pyplot as plt

def plot_reflectance(wavelength, reflectance):
    plt.figure()
    plt.plot(wavelength, reflectance, label='%R')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Reflectance (%)')
    plt.title('UV-Vis Reflectance')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_kubelka_munk(wavelength, km_values):
    plt.figure()
    plt.plot(wavelength, km_values, label='Kubelka-Munk')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('F(R)')
    plt.title('Kubelka-Munk Function')
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_tauc(hv, y_values, bandgap_type="direct"):
    plt.figure()
    plt.plot(hv, y_values, label=f'Tauc Plot ({bandgap_type})')
    plt.xlabel('Photon Energy (eV)')
    plt.ylabel('$(hv·F(R))^n$')
    plt.title('Tauc Plot')
    plt.grid(True)
    plt.legend()
    plt.show()
