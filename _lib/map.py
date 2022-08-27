# Tile-granularity map data

import numpy as np

#



class MAP:
    def __init__(self, size):
        # Meta: Overall metadata
        # [0-1]
        #   00: Use terrain code
        #   01: Fill with BLACK
        #   10: Make Transparent
        #   11: UNUSED
        # []
        self.meta = np.zeros(size, dtype="uint16")
        
        # Terrain: Code for terrain visualization
        self.terrain = np.zeros(size, dtype="uint16")

        # System: Used in game
        self.system = np.zeros(size, dtype="uint16")

# Map Generator for development
class MAPGen(MAP):
    # Aggregate all data into 
    def aggregate_and_save(self):
        pass

m = MAP([40, 40])

print(m)