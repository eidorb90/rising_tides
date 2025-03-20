"""
Terrain Test Suite
Author: Brodie Rogers <brodie.rogers@cune.students.edu>

A comprehensive test suite for the Terrain class with parameterized
tests across multiple datasets.
"""

import unittest
import os
from Terrain import Terrain

class TerrainTest(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures and shared resources."""
        self.terrain_files = {
            'crater_lake': 'terrain/terrain/CraterLake.terrain',
            'mars_craters': 'terrain/terrain/MarsCraters.terrain',
            'telka': 'terrain/terrain/TeIkaAMaui.terrain',
            'miami': 'terrain/terrain/Miami.terrain',
            'iceland': 'terrain/terrain/Iceland.terrain'
        }
        
        # Ensure output directory exists
        os.makedirs("test_output", exist_ok=True)
    
    def test_terrain_loading(self):
        """Test that terrain files load correctly with proper dimensions."""
        for name, file_path in self.terrain_files.items():
            with self.subTest(terrain=name):
                terrain = Terrain()
                terrain.load_data_from_file(file_path)
                
                # Verify terrain was loaded
                self.assertIsNotNone(terrain.grid)
                self.assertGreater(terrain.grid.shape[0], 0)
                self.assertGreater(terrain.grid.shape[1], 0)
                
                # Verify water sources were loaded
                self.assertGreater(len(terrain.water_sources), 0)
                
                # Verify elevation data makes sense
                self.assertLess(terrain.min_elevation, terrain.max_elevation)
                self.assertGreaterEqual(terrain.water_level, terrain.min_elevation)
    
    def test_flood_simulation(self):
        """Test the flooding algorithm with incremental water levels."""
        terrain = Terrain()
        terrain.load_data_from_file(self.terrain_files['iceland'])
        
        # Test progressive flooding
        prev_flooded_count = 0
        for level in range(0, 100, 20):
            flooded = terrain.flood_terrain(terrain.water_level + level)
            flooded_count = flooded.sum().sum()
            
            # As water level increases, more cells should be flooded
            self.assertGreaterEqual(flooded_count, prev_flooded_count)
            prev_flooded_count = flooded_count
    
    def test_gif_generation(self):
        """Test GIF generation functionality."""
        for name, file_path in self.terrain_files.items():
            with self.subTest(terrain=name):
                terrain = Terrain()
                terrain.load_data_from_file(file_path)
                
                output_path = f"test_output/{name}_test.gif"
                terrain.generate_gif(
                    output_path=output_path,
                    step=20,  # Larger step for faster testing
                    duration=50  # Faster animation for testing
                )
                
                # Verify file was created
                self.assertTrue(os.path.exists(output_path))
                self.assertGreater(os.path.getsize(output_path), 0)

    def test_edge_cases(self):
        """Test edge cases in the flooding algorithm."""
        terrain = Terrain()
        terrain.load_data_from_file(self.terrain_files['iceland'])
        
        # Test flooding at very low elevation
        # We expect only the water source cells to be flooded when water level is below terrain
        flooded = terrain.flood_terrain(terrain.min_elevation - 10)
        # Should only have the number of water sources flooded
        self.assertEqual(flooded.sum().sum(), len(terrain.water_sources))
        
        # Test flooding above maximum elevation (should flood everything)
        flooded = terrain.flood_terrain(terrain.max_elevation + 10)
        # All cells should be flooded
        self.assertEqual(flooded.sum().sum(), terrain.grid.size)

if __name__ == '__main__':
    unittest.main()