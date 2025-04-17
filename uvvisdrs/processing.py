import pandas as pd
import numpy as np

def load_reflectance_data(filepath):
    df = pd.read_csv(filepath, skiprows=2)
    df = df.dropna()
    wavelength = df.iloc[:, 0].astype(float).values  # nm
    reflectance = df.iloc[:, 1].astype(float).values  # %R
    return wavelength, reflectance

def kubelka_munk(R_percent):
    R = R_percent / 100  # convert to decimal
    return ((1 - R) ** 2) / (2 * R + 1e-8)  # Avoid divide by zero

def tauc_plot(wavelength, KM_values, bandgap_type="direct"):
    h = 4.135667696e-15  # Planck constant (eV.s)
    c = 3e8  # speed of light (m/s)
    wavelength_m = wavelength * 1e-9
    hv = h * c / wavelength_m  # photon energy in eV

    if bandgap_type == "direct":
        y = (hv * KM_values) ** 2
    elif bandgap_type == "indirect":
        y = (hv * KM_values) ** 0.5
    else:
        raise ValueError("bandgap_type must be 'direct' or 'indirect'")

    return hv, y
