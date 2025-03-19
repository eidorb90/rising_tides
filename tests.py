"""
Brodie Rogers 
tests.py

"""

from Terrain import Terrain

# set the file to be loaded into the Terrain object
crater_lake = 'CraterLake.terrain'
bay_area    = 'terrain/terrain/BayArea.terrain'


# Initialize the object and load the data 
terrain = Terrain()
terrain.load_data_from_file(bay_area)

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
    output_path="bay_area.gif",
    step=100
)