import streamlit as st
import pandas as pd
import math
import numpy as np
import os
os.system("streamlit run app.py --server.port 8000")

# Function to determine stability class
def stability_class(Us):
    if Us <= 3:
        return "B"
    elif 3 < Us < 6:
        return "C"
    elif Us >= 6:
        return "D"
    else:
        raise ValueError("Invalid stability class")

# Gaussian plume concentration calculation
def gaussian_plume(Q, bz, Hm, SIGMAz, U, SIGMAy):
    term1 = math.exp(-(bz - Hm)**2 / (2 * (SIGMAz**2)))
    term2 = math.exp(-(bz + Hm)**2 / (2 * (SIGMAz**2)))
    denominator = 2 * U * math.pi * SIGMAy * SIGMAz
    C = Q * (term1 + term2) / denominator
    return C


##Dispersion coordinate calculation SIGMAz and SIGMAy

## SIGMAy calculations using the US EPA ISC model

# Function to get the c and d values based on stability class
def get_c_d(stability_class):
    if stability_class == 'A':
        return 24.167, 2.5334
    elif stability_class == 'B':
        return 18.333, 1.8096
    elif stability_class == 'C':
        return 12.5, 1.0857
    elif stability_class == 'D':
        return 8.333, 0.72382
    elif stability_class == 'E':
        return 6.25, 0.54287
    elif stability_class == 'F':
        return 4.1667, 0.36191
    else:
        raise ValueError("Invalid stability class")

# Function to calculate sigma_y
def SIGMAy(x, Us):
    stability = stability_class(Us)
    c, d = get_c_d(stability)
    print( c, d)
    theta = (0.017453293 * (c - (d * np.log(x/1000))))
    sigma_y = (465.11628 * (x/1000)) * np.tan(theta)
    if np.isnan(sigma_y) or sigma_y <= 0:
        raise ValueError(f"Invalid sigma_y value: {sigma_y}")
    return sigma_y


##SIGMAz calculations
def SIGMAz(x, stability_class):
    if stability_class== 'B':
        return sigma_Zb(x)
    elif stability_class == 'C':
        return sigma_Zc(x)
    elif stability_class == 'D':
        return sigma_Zd(x)
    else:
        return "ERROR: Invalid stability condition"

def sigma_Zb(x):
    if x/1000 < 0.2:
        return 90.693 * (x/1000)**0.93198
    elif 0.2 <= x/1000 < 0.4:
        return 98.483 * (x/1000)**0.98332
    elif x/1000 >= 0.4:
        return 109.3 * (x/1000)**1.0971
    else:
        return "ERROR"

def sigma_Zc(x):
    result = 61.141 * (x/1000)**0.91465
    return min(result, 5000)

def sigma_Zd(x):
    if x/1000 < 0.3:
        return 34.459 * (x/1000)**0.86974
    elif 0.3 <= x/1000 < 1:
        return 32.093**0.81066
    elif 1 <= x/1000 < 3:
        return 32.093**0.64403
    elif 3 <= x/1000 < 10:
        return 33.504 * (x/1000)**0.60486
    elif 10 <= x/1000 < 30:
        return 36.65 * (x/1000)**0.56589
    elif x/1000 > 30:
        return 44.053 * (x/1000)**0.51179
    else:
        return "ERROR"


# Plume rise calculation
def calculate_plume_rise(Us, Vs, d, Ts, Ta, F):
    buoyant_rise = (Ts - Ta > 10)
    momentum_rise = (Vs > 10)
    wind_effects = (Us > 6)

    if buoyant_rise and (momentum_rise or wind_effects):
        plume_type = "Both buoyant and momentum-driven"
    elif buoyant_rise:
        plume_type = "Buoyant"
    elif momentum_rise or wind_effects:
        plume_type = "Momentum-driven"
    else:
        plume_type = "Neither"

    if (Vs / Us) <= 4:
        buoyant_deltaH = 1.6 * (F)**(1/3) * (3.5 * (14 * F**(5/8) if F <= 55 else 34 * F**(2/5)))**(2/3) / Us
    else:
        buoyant_deltaH = 0

    momentum_deltaH = 3 * d * Vs / Us if (Vs / Us) > 4 else 0

    if buoyant_rise and momentum_rise:
        total_deltaH = buoyant_deltaH + momentum_deltaH
    elif buoyant_rise:
        total_deltaH = buoyant_deltaH
    elif momentum_rise:
        total_deltaH = momentum_deltaH
    else:
        total_deltaH = 0

    return total_deltaH, buoyant_deltaH, momentum_deltaH, plume_type

# Modified effective height calculation
def Hm(ht, hs, DeltaH):
    H = hs + DeltaH
    if ht < 0:
        return H - ht
    elif 0 <= ht < hs:
        return H
    elif ht >= hs:
        return H - 0.5 * ht
    else:
        raise ValueError("Invalid terrain height")

