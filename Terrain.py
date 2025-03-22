"""
Brodie Rogers
<brodie.rogers@cune.students.edu>

Terrain.py


This file contains the Terrain class for simulating water flow over terrain.
The class loads terrain data from .terrain files, processes the data, and
provides methods for flooding simulation and visualization.

Key features:
- Loading terrain data from .terrain files
- Simulating flood patterns at different water levels
- Generating GIFs to visualize flooding progression
- Tracking water sources and their propagation
"""

import pandas as pd
import numpy as np
from collections import deque
from PIL import Image, ImageDraw
import tqdm
import os


class Terrain:
    """
    A class for modeling and simulating water flow over terrain.

    This class loads terrain data from .terrain files, processes elevation data,
    tracks water sources, and simulates how water would flood the terrain at
    different water levels. It also provides functionality to visualize the
    flooding process through GIF generation.

    Attributes:
        size (tuple): Dimensions of the terrain grid (rows, columns)
        grid (DataFrame): Pandas DataFrame containing elevation data
        water_sources (list): List of (x, y) coordinates of water sources
        water_df (DataFrame): Boolean DataFrame marking water source locations
        water_level (float): Elevation of the initial water source
        max_elevation (float): Maximum elevation in the terrain
        min_elevation (float): Minimum elevation in the terrain
    """

    def __init__(self):
        self.size = None
        self.grid = None
        self.water_sources = None
        self.water_df = None
        self.water_level = None
        self.max_elevation = None
        self.min_elevation = None

    def load_data_from_file(self, file_path: str):
        """Loads data from a .terrain file into a Pandas Dataframe. While also creating a list for the water sources

        Args:
            file_path (str): String to the location of your desired .terrain file

        Raises:
            ValueError: Raises 'ValueError' when the file doesn't have the .terrain file header
        """
        with open(file_path, "r") as file:
            # Make sure that the file has correct "terrain" header
            header = file.readline().strip()
            if header != "terrain":
                raise ValueError(
                    "Not valid terrain file!! Expected 'terrain' as first line "
                )

            # read in the dimensions (this was missing in your code)
            dimensions = file.readline().strip().split()
            num_cols = int(dimensions[0])
            num_rows = int(dimensions[1])

            # read number of water sources
            num_of_water_sources = int(file.readline().strip())

            # read water source coords
            water_sources = []
            for _ in range(num_of_water_sources):
                water_coord = file.readline().strip().split()
                water_sources.append((int(water_coord[0]), int(water_coord[1])))

            # Rest of your code remains the same...

            # read in terrain data
            terrain_data = []
            for line in file:
                row_values = [float(val) for val in line.strip().split()]
                terrain_data.append(row_values)

            # create Pandas Dataframe for the Terrain
            terrain_df = pd.DataFrame(terrain_data)

            # Get the actual dimensions of the terrain data
            actual_rows, actual_cols = terrain_df.shape

            # create a Pandas Dataframe for the water sources
            water_df = pd.DataFrame(np.zeros((actual_rows, actual_cols), dtype=bool))

            # Set water source locations - with bounds checking
            for col, row in water_sources:
                # Make sure indices are within bounds
                if 0 <= row < actual_rows and 0 <= col < actual_cols:
                    water_df.iloc[row, col] = True
                else:
                    print(
                        f"Warning: Water source at ({col}, {row}) is outside valid range for terrain of shape {actual_rows} rows x {actual_cols} columns"
                    )

            # Get elevation of the first water source
            if water_sources:
                col, row = water_sources[0]
                # Make sure water source coordinates are valid before getting water level
                if 0 <= row < actual_rows and 0 <= col < actual_cols:
                    self.water_level = terrain_df.iloc[row, col]
                else:
                    print(
                        f"Warning: First water source at ({col}, {row}) is outside valid range!"
                    )
                    # Try to set a reasonable default
                    self.water_level = terrain_df.iloc[
                        0, 0
                    ]  # Use first cell's elevation as default
            else:
                # No water sources defined
                print("Warning: No water sources defined in terrain file!")
                self.water_level = terrain_df.iloc[
                    0, 0
                ]  # Use first cell's elevation as default

            # set the objects values
            self.size = (actual_rows, actual_cols)
            self.grid = terrain_df
            self.water_sources = water_sources
            self.water_df = water_df
            self.max_elevation = self.grid.max().max()
            self.min_elevation = self.grid.min().min()

    def flood_terrain(self, water_level: float):
        """Simulates flooding the set terrain grid at a certain elevation.

        Args:
            water_level (float): This is the elevation to simulate the water at.

        Returns:
            flooded (Pandas DataFrame): Pandas DataFrame that tracks the 'flooded' tiles.
        """
        # Create a copy of water_df to track flooded cells for this water level
        flooded = self.water_df.copy()

        # get the size of the DataFrame
        num_rows, num_cols = self.size

        # Define the four cardinal directions: up, right, down, left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # Initialize the Queue for the BFS
        queue = deque()

        # Add all water sources to the queue and mark them as flooded
        for col, row in self.water_sources:
            # Skip water sources that are out of bounds
            if not (0 <= row < num_rows and 0 <= col < num_cols):
                continue

            if self.grid.iloc[row, col] <= water_level:
                queue.append((row, col))
                flooded.iloc[row, col] = True

        # Perform the BFS to flood the terrain
        while queue:
            # Queue cell and add it to be process
            current_row, current_col = queue.popleft()

            # Check each of the 4 neighboring cells
            for dr, dc in directions:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                # Check to make sure that we are within the grids boundaries
                if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols:
                    # check to make sure that its not already flooded and its elevation is <= water_level
                    if (
                        not flooded.iloc[neighbor_row, neighbor_col]
                        and self.grid.iloc[neighbor_row, neighbor_col] <= water_level
                    ):
                        # mark as flooded and add to Queue
                        flooded.iloc[neighbor_row, neighbor_col] = True
                        queue.append((neighbor_row, neighbor_col))

        return flooded

    def get_terrain_color(self, norm_elevation):
        """
        Get color for terrain based on normalized elevation value (0.0 to 1.0).
        Creates distinct elevation bands for a topographic map effect.
        """
        # Define distinct elevation bands with their colors - more bands for detailed visualization
        elevation_bands = [
            (0.00, (0, 60, 0)),  # Very dark green
            (0.05, (0, 80, 0)),  # Darker green
            (0.10, (0, 100, 0)),  # Dark green
            (0.15, (0, 120, 0)),  # Medium-dark green
            (0.20, (0, 140, 0)),  # Medium green
            (0.25, (0, 160, 0)),  # Medium-light green
            (0.30, (20, 180, 0)),  # Light green
            (0.35, (40, 200, 0)),  # Lighter green
            (0.40, (80, 215, 0)),  # Yellow-green
            (0.45, (120, 230, 0)),  # Light yellow-green
            (0.50, (160, 240, 0)),  # Green-yellow
            (0.55, (200, 245, 0)),  # Yellow-green-yellow
            (0.60, (240, 240, 0)),  # Yellow
            (0.65, (250, 220, 0)),  # Yellow-orange
            (0.70, (255, 200, 0)),  # Light orange
            (0.75, (255, 170, 0)),  # Orange
            (0.80, (255, 140, 0)),  # Medium orange
            (0.85, (255, 110, 0)),  # Dark orange
            (0.90, (255, 80, 0)),  # Orange-red
            (0.95, (255, 40, 0)),  # Light red
            (1.00, (255, 0, 0)),  # Red
        ]

        # Find which band the elevation falls into
        for i in range(len(elevation_bands)):
            threshold, color = elevation_bands[i]

            # If we're at the last band or the elevation is below the next threshold
            if (
                i == len(elevation_bands) - 1
                or norm_elevation < elevation_bands[i + 1][0]
            ):
                return color

        # Fallback (should never reach here)
        return (255, 255, 255)

    def gen_frame(self, level=None, terrain_min=None, terrain_max=None, save_path=None):
        """
        Generates a single frame for the water level simulation.

        Args:
            level (float, optional): The water level to simulate. Defaults to current water level.
            terrain_min (float, optional): Minimum elevation for color normalization. Defaults to water level.
            terrain_max (float, optional): Maximum elevation for color normalization. Defaults to max elevation.
            save_path (str, optional): Path to save the frame as PNG. If None, frame is not saved to disk.

        Returns:
            Image: PIL Image object representing the frame
        """

        # Use water level if level is not specified
        if level is None:
            level = self.water_level

        # Set range for normalization
        if terrain_min is None:
            terrain_min = self.min_elevation
        if terrain_max is None:
            terrain_max = self.max_elevation

        # Calculate terrain range for normalization
        terrain_range = terrain_max - terrain_min

        # Get the flooded terrain for the water level
        flooded = self.flood_terrain(level)

        # Create RGB image for this frame
        img = Image.new("RGB", (self.size[1], self.size[0]))
        pixels = img.load()

        # Use tqdm for pixel processing - rows only
        for row in tqdm.tqdm(
            range(self.size[0]), desc=f"Processing level {level:.1f}", leave=False
        ):
            for col in range(self.size[1]):
                if flooded.iloc[row, col]:
                    # Water color (blue)
                    pixels[col, row] = (0, 0, 255)
                else:
                    # Color based on elevation
                    elevation = self.grid.iloc[row, col]
                    norm_elevation = (elevation - terrain_min) / terrain_range
                    pixels[col, row] = self.get_terrain_color(norm_elevation)

        # Add water level text to the image
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), f"Water Level: {level:.1f}", fill=(255, 255, 255))

        # Save the image if a path is provided
        if save_path:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            img.save(save_path, format="PNG")
            print(f"Frame saved to {save_path}")

        return img

    def generate_gif(
        self,
        output_path="terrain_flood.gif",
        min_level=None,
        max_level=None,
        step=5,
        duration=10,
    ):
        """
        Generates a GIF showing the flooding of terrain as water level rises.

        Args:
            output_path (str): Path where the GIF will be saved
            min_level (float): Minimum water level to start with (defaults to terrain's minimum elevation)
            max_level (float): Maximum water level to end with (defaults to terrain's maximum elevation)
            step (float): Increment size for water level
            duration (int): Duration for each frame in milliseconds
        """

        # Make sure that the values given for the gif are valid
        if min_level is None or min_level < self.water_level:
            min_level = self.water_level
        if max_level is None or max_level > self.grid.max().max():
            max_level = self.grid.max().max()

        # Get terrain elevation range for coloring
        terrain_min = self.grid.min().min()
        terrain_max = self.grid.max().max()

        # Generate water levels
        water_levels = np.arange(min_level, max_level + step, step)

        # Create a list to store frames
        frames = []

        # Use tqdm for the outer loop to show overall progress
        for level in tqdm.tqdm(water_levels, desc="Generating frames"):
            # Generate frame for this water level
            img = self.gen_frame(level, terrain_min, terrain_max)

            # Add frame to the list
            frames.append(img)

        # Save frames as GIF
        print("Saving GIF...")

        # Ensure the gifs directory exists

        os.makedirs("gifs", exist_ok=True)

        frames[0].save(
            f"gifs/{output_path}",
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=duration,
            loop=0,
        )

        print(f"GIF saved to gifs/{output_path}")
        return output_path

    def __str__(self):
        string = f"Water level     : {self.water_level}\nSize            : {self.size}\nGrid            : \n{self.grid.head()} \nWater Sources({len(self.water_sources)})   : {self.water_sources}"
        return string
