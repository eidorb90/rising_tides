# Rising Tides: Terrain Water Flow Simulation

A Python application for simulating and visualizing water flow over terrain data, allowing for realistic flooding simulations across various landscapes.

## Overview

Rising Tides loads terrain elevation data from `.terrain` files and simulates how water would flood the terrain at different water levels. It provides functionality for:

- Loading and processing terrain elevation data
- Simulating flood patterns at various water levels
- Generating animated GIFs to visualize flooding progression
- Generate static heatmap images to show the elevation
- Tracking water sources and their propagation through breadth-first search algorithms

## Features

- **Terrain Loading**: Parse and load terrain data from standardized `.terrain` files
- **Flood Simulation**: Calculate water propagation using a breadth-first search algorithm
- **Visualization**: Generate color-coded GIF animations showing flooding patterns over time
- **Heatmap Generation**: Generate color-coded Heatmap Images showing the elevations of the desired terrain
- **Multiple Water Sources**: Support for terrain with multiple water sources
- **Customizable Parameters**: Adjust simulation parameters like water level increment and animation speed

## Installation

This project requires Python 3.12 or newer.

```bash
# Clone the repository
git clone https://github.com/eidorb90/rising_tides.git
cd rising-tides

# Install dependencies
uv pip install .
```

### Dependencies

- NumPy (>=2.2.4)
- Pandas (>=2.2.3)
- Pillow (>=11.1.0)

## Usage

### Basic Usage

```python
from Terrain import Terrain

# Initialize and load terrain data
terrain = Terrain()
terrain.load_data_from_file('path/to/terrain_file.terrain')

# Print information about the terrain
print(terrain)

# Generate a flooding animation
terrain.generate_gif(
    output_path="flood_simulation.gif",
    step=5,  # water level increment
    duration=100  # frame duration in milliseconds
)
```

### Customizing Simulation Parameters

```python
# Simulate flooding at a specific water level
flooded = terrain.flood_terrain(terrain.water_level + 50)

# Generate a more detailed animation with smaller steps
terrain.generate_gif(
    output_path="detailed_flood.gif",
    min_level=terrain.water_level,
    max_level=terrain.water_level + 200,
    step=2,  # smaller increments for more detailed animation
    duration=50  # faster animation
)
```

## Terrain File Format

The `.terrain` files follow this structure:

```
terrain
[# of columns] [# of rows]
[number of water sources]
[column index 1] [row index 1]
[column index 2] [row index 2]
...
[elevation data grid as space-separated values]
```

## Data Sources

The terrain data used in this project comes from various sources:

- National Oceanic and Atmospheric Administration (NOAA)
- GEBCO 2020 Gridded Bathymetry Survey
- ASU Mars data
- Norwegian Mapping Agency
- US Department of Agriculture's National Elevation Dataset

## Example Terrains

The project includes several example terrain files:

- `CraterLake.terrain`
- `MarsCraters.terrain`
- `TeIkaAMaui.terrain`
- `Miami.terrain`
- `Iceland.terrain`

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This means:

- You are free to use, modify, and distribute this software
- If you distribute modified versions, you must make your source code available
- Any derivative works must also be licensed under GPL v3.0
- Full details are in the LICENSE file

## Acknowledgments

- Original data sourced from NOAA and GEBCO
- Mars data created by Varun Shenoy based on ASU data
- Norway data created by Staale Jordan based on Norwegian Mapping Agency data

## Author

Brodie Rogers - <brodie.rogers@cune.students.edu>
