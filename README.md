# Monte Carlo Simulation for Etching Thickness Analysis

## Overview

This project provides a Monte Carlo simulation to analyze the etching process in semiconductor manufacturing, specifically focusing on the remaining thickness of a material, for example SiO₂ (Silicon Dioxide), and another material, for example SiNx (Silicon Nitride) layers. The simulation takes into account variability in parameters such as initial thickness, etch rates, and standard deviations, helping to evaluate how these factors impact the etching results.

The code is designed to generate visualizations, including histograms and bar charts, that provide insights into the distribution of the remaining thickness after the etching process. Additionally, the project includes an interactive graphical user interface (GUI) for users to input key parameters, making the simulation accessible for quick analysis.

## Features

- **Monte Carlo Simulation**: Simulates the etching process for SiO₂ and SiNx, incorporating variability in initial thickness and etch rates.
- **Interactive GUI**: Allows users to input parameters like the number of samples, etch times, thicknesses, and more through an intuitive interface.
- **Detailed Visualizations**: Generates histograms and plots to visualize initial and remaining thickness distributions, as well as the area under the normal distribution for a given value.
- **Statistical Analysis**: Computes mean, standard deviation, and distribution areas to assist in analyzing the etching process outcomes.

## Why This Project Is Useful

Semiconductor manufacturing requires precise control over etching processes to achieve desired layer thicknesses. This project helps engineers understand how variability in process parameters impacts the final etched thickness. By visualizing the results through Monte Carlo simulations, the project aids in risk assessment and process optimization, making it an invaluable tool for engineers and researchers working in semiconductor fabrication.

## Getting Started

To run the project, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine using the following command:
   ```sh
   git clone https://github.com/yourusername/montecarlo-etching-simulation.git
   ```

2. **Install Requirements**: Make sure you have Python installed along with the necessary libraries. Install the required packages using:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Script**: Run the script to start the GUI and enter the desired parameters for the simulation:
   ```sh
   python etching_simulation.py
   ```

## Visualizations

The simulation generates the following visualizations to provide insights into the etching process:

- **Initial and Final Thickness Structure**: A comparison of the initial and final thickness of SiO₂ and SiNx after etching.
- **Histograms of Remaining Thickness**: Shows the distribution of remaining thicknesses for SiO₂, SiNx, and the total structure.
- **Normal Distribution Plots**: Illustrates the area under the remaining normal distribution for a given limit, indicating the proportion of remaining thickness below that value.

## Getting Help

If you have questions or encounter issues, please open an issue on the GitHub repository. We welcome contributions and feedback to improve the project.

## Contributors

This project is maintained by [Cosimo Spagnolo](https://github.com/yourusername). Contributions are welcome. If you would like to contribute, please feel free to submit a pull request or contact us through the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

