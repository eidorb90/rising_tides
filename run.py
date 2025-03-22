from Terrain import Terrain
import os

crater_lake = "terrain/terrain/CraterLake.terrain"
mars_craters = "terrain/terrain/MarsCraters.terrain"
telka = "terrain/terrain/TeIkaAMaui.terrain"
miami = "terrain/terrain/Miami.terrain"
iceland = "terrain/terrain/Iceland.terrain"
bay_area = "terrain/terrain/BayArea.terrain"
guam = "terrain/terrain/Guam.terrain"
gulf_of_guinea = "terrain/terrain/GulfOfGuinea.terrain"
new_york = "terrain/terrain/NewYorkCity.terrain"
south_bay_area = "terrain/terrain/SouthBayArea.terrain"


terrain_list = [
    crater_lake,
    mars_craters,
    telka,
    miami,
    iceland,
    bay_area,
    guam,
    gulf_of_guinea,
    new_york,
    south_bay_area,
]

# terrain = Terrain()
# terrain.load_data_from_file(telka)

# terrain.generate_gif(output_path="telka.gif", step=100)

# check the gen frame for all data
for t in terrain_list:
    try:
        # Extract terrain name from path
        terrain_name = os.path.basename(t).replace(".terrain", "")
        print(f"Processing {terrain_name}...")

        terrain = Terrain()
        terrain.load_data_from_file(t)

        # Create directory if it doesn't exist
        os.makedirs("height_map", exist_ok=True)

        # Save height map with proper filename
        save_path = f"height_map/{terrain_name}_height_map.png"
        terrain.gen_frame(save_path=save_path)

        print(f"Generated height map for {terrain_name}")
    except Exception as e:
        print(f"Error processing {os.path.basename(t)}: {e}")
        print("Continuing with next terrain file...")
        continue
