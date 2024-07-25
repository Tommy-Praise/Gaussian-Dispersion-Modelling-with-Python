# Gaussian Plume Model Dispersion

This project implements a Gaussian Plume Model for atmospheric dispersion using Streamlit. It calculates the concentration of pollutants at various distances from a stack and visualizes the results through various plots.

## Features

- Input data for the Gaussian Plume Model.
- Calculation of stability classes and dispersion parameters.
- Plume rise calculations based on buoyant and momentum-driven models.
- Visualization of the results using 2D contour plots, 3D surface plots, and parallel coordinates.

## Files

- `main.py`: Contains the core functions for stability class determination, Gaussian plume calculation, dispersion parameters, and plume rise calculation.
- `app.py`: The Streamlit application that provides an interface for input, computation, and visualization.
- `visualization.py`: Functions for generating various plots using Plotly.

## Getting Started

### Prerequisites

- Python 3.x
- Streamlit
- Plotly
- Pandas
- NumPy

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to access the application.

## Usage

1. Enter the input parameters for the Gaussian Plume Model.
2. Edit the receptor distance table as needed.
3. Click the "Compute Dispersion" button to calculate the pollutant concentration and visualize the results.

## Visualizations

- Gaussian Distribution: Line plot showing the concentration of pollutants at various distances.
- 2D Contour Plot: Heatmap of the concentration distribution.
- 3D Surface Plot: Terrain height visualization.
- Parallel Coordinates Plot: Visualization of the relationship between multiple variables.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to Dr. Babatunde Oladimeji, H.O.D of PHysics Mountain Top University for overseeing this project.

