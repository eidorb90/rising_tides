""" 
Brodie Rogers 
Terrain.py


"""

import pandas as pd
import numpy as np
from collections import deque
from PIL import Image, ImageDraw

class Terrain:
    def __init__(self):
        self.size = None
        self.grid = None
        self.water_sources = None
        self.water_df = None
        self.water_level = None
        self.max_elevation = None

    def load_data_from_file(self, file_path: str):
        """Loads data from a .terrain file into a Pandas Dataframe. While also creating a list for the water sources

        Args:
            file_path (str): String to the location of your desired .terrain file

        Raises:
            ValueError: Raises 'ValueError' when the file doesn't have the .terrain file header
        """
        with open(file_path, 'r') as file:
            # Make sure that the file has correct "terrain" header 
            header = file.readline().strip()
            if header != "terrain":
                raise ValueError("Not valid terrain file!! Expected 'terrain' as first line ")
            
            # read in the dimensions (this was missing in your updated code)
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
                if 0 <= row < actual_rows and 0 <= col < actual_cols:
                    water_df.iloc[row, col] = True
                else:
                    print(f"Warning: Water source at ({col}, {row}) is out of bounds for grid of shape {actual_rows}x{actual_cols}")
            
            # Get elevation of the first water source
            col, row = water_sources[0]
            
            # set the objects values 
            self.size = (actual_rows, actual_cols)
            self.grid = terrain_df
            self.water_sources = water_sources
            self.water_df = water_df
            self.max_elevation = self.grid.max().max()
            
            # Make sure water source coordinates are valid before getting water level
            if 0 <= row < actual_rows and 0 <= col < actual_cols:
                self.water_level = terrain_df.iloc[row, col]
            else:
                print(f"Warning: Water source at ({col}, {row}) is out of bounds!")
                self.water_level = 0  # Default value

    def flood_terrain(self, water_level: float):
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
            if self.grid.iloc[row, col] <= water_level:
                queue.append((row, col))
                flooded.iloc[row, col] = True

        # Preform the BFS to flood the terrain
        while queue:
                    
            # Queue cell and add it to be process
            current_row, current_col = queue.popleft()

            # Check each of the 4 neighboring cells 
            for dr, dc in directions:
                neighbor_row, neighbor_col = current_row + dr, current_col + dc

                # Check to make sure that we are within the grids boundaries
                if (0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols):
                    # check to make sure that its not already flooded and its elevation is <= water_level
                    if not flooded.iloc[neighbor_row, neighbor_col] and self.grid.iloc[neighbor_row, neighbor_col] <= water_level:
                        # mark as flooeded and add to Queue
                        flooded.iloc[neighbor_row, neighbor_col] = True
                        queue.append((neighbor_row, neighbor_col))

        return flooded

    def generate_gif(self, output_path="terrain_flood.gif", min_level=None, max_level=None, step=5, duration=10):
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

        # create a list to store frames
        frames = []
    
        # Generate colormap for visualization
        # We'll use a colormap where:
        # - Blue for water
        # - Green to yellow to red for increasing elevation
        terrain_cmap = {
            'water': (0, 0, 255),      # Blue
            'low': (0, 200, 0),        # Green
            'mid': (255, 255, 0),      # Yellow
            'high': (255, 0, 0)        # Red
        }

        # Normalize terrain values for coloring
        terrain_min = self.grid.min().min()
        terrain_max = self.grid.max().max()
        terrain_range = terrain_max - terrain_min

        water_levels = np.arange(min_level, max_level + step, step)

        for level in water_levels:
            # get the flooded terrain for the water level
            flooded = self.flood_terrain(level)

            # create and RGB image for this frame 
            img = Image.new("RGB", (self.size[1], self.size[0]))
            pixels = img.load()

            # fill in the previously created pixels
            for row in range(self.size[0]):
                for col in range(self.size[1]):
                    if flooded.iloc[row, col]:
                        # water color (blue)
                        pixels[col, row] = terrain_cmap['water']

                    else:
                        # Color based on elevation 
                        elevation = self.grid.iloc[row, col]
                        norm_elevation = (elevation - terrain_min) / terrain_range

                        if norm_elevation < 0.33:
                            # Low elevation (green)
                            pixels[col, row] = terrain_cmap['low']
                        elif norm_elevation < 0.67:
                            # Medium elevation (yellow)
                            pixels[col, row] = terrain_cmap['mid']
                        else:
                            # High elevation (red)
                            pixels[col, row] = terrain_cmap['high']

            # Add water level text to the image
            draw = ImageDraw.Draw(img)
            draw.text((10, 10), f"Water Level: {level:.1f}", fill=(255, 255, 255))
            
            # Add frame to the list
            frames.append(img)

            # Print progress
            print(f"Generated frame for water level {level:.1f}")

        # Save frames as GIF
        frames[0].save(
            output_path,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=duration,
            loop=0
        )
        
        print(f"GIF saved to {output_path}")
        return output_path

        
    
    def __str__(self):
        string = (f"Water level     : {self.water_level}\nSize            : {self.size}\nGrid            : \n{self.grid.head()} \nWater Sources({len(self.water_sources)})   : {self.water_sources}")
        return string