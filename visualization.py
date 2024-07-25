# Updated visualization.py with new 3D visualization function
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd

def plot_gaussian_distribution(df):
    fig = px.line(df, x='Receptor distance from stack, x (m)', y='C at receptor height (x,0,ht+bz), C (ug/m3)', 
                  title='Gaussian Distribution: Distance vs Concentration',
                  labels={'Receptor distance from stack, x (m)': 'Distance (m)', 'C at receptor height (x,0,ht+bz), C (ug/m3)': 'Concentration (ug/m3)'})
    return fig

def plot_2d_contour(df):
    fig = go.Figure(data=go.Contour(
        z=df.pivot(index='height at receptor location, ht (m)', columns='Receptor distance from stack, x (m)', values='C at receptor height (x,0,ht+bz), C (ug/m3)').values,
        x=df['Receptor distance from stack, x (m)'].unique(),
        y=df['height at receptor location, ht (m)'].unique(),
        contours=dict(
            coloring='heatmap',
            showlabels=True
        ),
        colorbar=dict(
            title='Concentration (ug/m3)'
        )
    ))
    fig.update_layout(title='2D Contour Plot: Concentration Distribution')
    return fig

def plot_3d_visualization(df):
    fig = go.Figure(data=[go.Surface(
        z=df.pivot(index='height at receptor location, ht (m)', columns='Receptor distance from stack, x (m)', values='C at receptor height (x,0,ht+bz), C (ug/m3)').values,
        x=df['Receptor distance from stack, x (m)'].unique(),
        y=df['height at receptor location, ht (m)'].unique()
    )])
    fig.update_layout(title='3D Surface Plot: Concentration Distribution',
                      scene=dict(
                          xaxis_title='Distance from Stack (m)',
                          yaxis_title='Height at Receptor Location (m)',
                          zaxis_title='Concentration (ug/m3)'
                      ))
    return fig

def plot_3d_surface(df):
    fig = go.Figure(data=[go.Surface(
        z=df['height at receptor location, ht (m)'],
        x=df['Receptor distance from stack, x (m)'],
        y=df['height at receptor location, ht (m)']
    )])
    fig.update_layout(title='3D Surface Plot: Terrain Height',
                      scene=dict(
                          xaxis_title='Distance from Stack (m)',
                          yaxis_title='Terrain Height (m)',
                          zaxis_title='Height (m)'
                      ))
    return fig

def plot_parallel_coordinates(df):
    fig = px.parallel_coordinates(df, color="C at receptor height (x,0,ht+bz), C (ug/m3)", labels={
        'Receptor distance from stack, x (m)': 'Distance (m)',
        'height at receptor location, ht (m)': 'Terrain Height (m)',
        'Pasquill Class': 'Pasquill Class',
        'SIGMAy': 'Sigma Y',
        'provisional SIGMAz': 'Provisional Sigma Z',
        'SIGMAz': 'Sigma Z',
        'Buoyancy Flux F': 'Buoyancy Flux',
        'DeltaH': 'Plume Rise',
        'h': 'Effective Stack Height',
        'C at receptor height (x,0,ht+bz), C (ug/m3)': 'Concentration (ug/m3)'
    }, title="Parallel Coordinates Plot")
    return fig
