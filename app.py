# app.py
import streamlit as st
import pandas as pd
import numpy as np
from main import stability_class, SIGMAy, SIGMAz, calculate_plume_rise, Hm, gaussian_plume
from visualization import plot_gaussian_distribution, plot_2d_contour, plot_3d_visualization, plot_3d_surface, plot_parallel_coordinates

# Default data for the table
default_data = {
    'Receptor distance from stack, x (m)': [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500],
    'height at receptor location, ht (m)': [-1] * 11,
    'Pasquill Class': [''] * 11,
    'SIGMAy': [0] * 11,
    'provisional SIGMAz': [0] * 11,
    'SIGMAz': [0] * 11,
    'Buoyancy Flux F': [0] * 11,
    'DeltaH': [0] * 11,
    'h': [0] * 11,
    'hs': [0] * 11,
    'C at receptor height (x,0,ht+bz), C (ug/m3)': [0] * 11
}

df = pd.DataFrame(default_data)

st.title('Gaussian Plume Model Dispersion')

# Input fields
Q = st.number_input('PM emission rate from stack, Q (ug/s)', value=36475)
Us = st.number_input('Wind speed at source height, Us (m/s)', value=5.57)
hs = st.number_input('Stack height from ground, hs (m)', value=43)
d = st.number_input('Stack diameter, d (m)', value=2.8)
Vs = st.number_input('Stack gas exit velocity, Vs (m/s)', value=11)
Ts = st.number_input('Stack gas exit temperature, Ts (C)', value=100)
Ta = st.number_input('Ambient air temperature, Ta (C)', value=25)
bz = st.number_input('Height of breathing zone, bz (m)', value=1.43)

st.write('### Input Data Table')
df_editable = st.data_editor(df, num_rows="dynamic", key='editable_table')

if st.button('Compute Dispersion'):
    pasquill_class = stability_class(Us)
    DeltaH, buoyant_deltaH, momentum_deltaH, plume_type = calculate_plume_rise(Us, Vs, d, Ts, Ta, (9.807 * Vs * d**2 * (Ts - Ta)) / (4 * (Ts + 273.15)))

    for i in range(len(df_editable)):
        x = df_editable.at[i, 'Receptor distance from stack, x (m)']
        ht = df_editable.at[i, 'height at receptor location, ht (m)']

        sigma_y = SIGMAy(x, Us)
        sigma_z = SIGMAz(x, pasquill_class)
        F = (9.807 * Vs * d**2 * (Ts - Ta)) / (4 * (Ts + 273.15))  # Buoyancy flux calculation

        H = Hm(ht, hs, DeltaH)

        # Ensure sigma_y and sigma_z are within expected ranges
        if not np.isnan(sigma_y) and not np.isnan(sigma_z):
            C = gaussian_plume(Q, bz, H, sigma_z, Us, sigma_y)
            df_editable.at[i, 'C at receptor height (x,0,ht+bz), C (ug/m3)'] = C
        else:
            st.error(f"Invalid dispersion values for row {i}: sigma_y = {sigma_y}, sigma_z = {sigma_z}")

        df_editable.at[i, 'Pasquill Class'] = pasquill_class
        df_editable.at[i, 'SIGMAy'] = sigma_y
        df_editable.at[i, 'SIGMAz'] = sigma_z
        df_editable.at[i, 'Buoyancy Flux F'] = F
        df_editable.at[i, 'DeltaH'] = DeltaH
        df_editable.at[i, 'h'] = hs + DeltaH
        df_editable.at[i, 'hs'] = hs
        df_editable.at[i, 'height at receptor location, ht (m)'] = ht

    st.write('### Output Data Table - Plume Type: ' + plume_type)
    st.write(df_editable)

    st.write('### Gaussian Distribution')
    fig_gaussian = plot_gaussian_distribution(df_editable)
    st.plotly_chart(fig_gaussian)

    st.write('### 2D Contour Plot')
    fig_2d_contour = plot_2d_contour(df_editable)
    st.plotly_chart(fig_2d_contour)

    st.write('### 3D Visualization')
    fig_3d = plot_3d_visualization(df_editable)
    st.plotly_chart(fig_3d)

    st.write('### 3D Surface Plot')
    fig_3d_surface = plot_3d_surface(df_editable)
    st.plotly_chart(fig_3d_surface)

    st.write('### Parallel Coordinates Plot')
    fig_parallel_coordinates = plot_parallel_coordinates(df_editable)
    st.plotly_chart(fig_parallel_coordinates)
