"""
Brodie Rogers 
<brodie.rogers@cune.students.edu>

tests.py


Testing file for the Terrain class I wrote. 
We check the different datasets that we have in different ways.
"""

from Terrain import Terrain

# set the file to be loaded into the Terrain object
crater_lake = 'terrain/terrain/CraterLake.terrain'
bay_area    = 'terrain/terrain/MarsCraters.terrain'
telka       = 'terrain/terrain/TelkaAMaui.terrain'
miami       = 'terrain/terrain/Miami.terrain'
iceland     = 'terrain/terrain/Iceland.terrain'


# Initialize the object and load the data 
terrain = Terrain()
terrain.load_data_from_file(iceland)

# Print the object(to make sure the data is loaded correctly)
# print(terrain)

# # Increment by 5 units
# for level in range(0, 100, 5):  
#     flooded = terrain.flood_terrain(terrain.water_level + level)
#     # Count flooded cells
#     flooded_count = flooded.sum().sum()
#     print(f"Water level: {terrain.water_level + level}, Flooded cells: {flooded_count}")

# testing the generate gif function
terrain.generate_gif(
    output_path="iceland.gif",
    step=100
)

# test elevations 
# print(terrain.min_elevation, terrain.max_elevation)