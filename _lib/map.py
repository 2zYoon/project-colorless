# Tile-granularity map data

import numpy as np

#



class MAP:
    def __init__(self, size):
        # Meta: Overall metadata
        # [0-1]
        #   00: Use LAYER 0
        #   01: Use LAYER 1
        #   10: Make transparent
        #   11: Fill with BLACK
        # []
        self.meta = np.zeros(size, dtype="uint16")
        
        # Layer1: Mostly used. This is under the character
        self.layer1 = np.zeros(size, dtype="uint16")

        # Layer2: This is on the chracter
        self.layer2 = np.zeros(size, dtype="uint16")

        # System: Used in game
        self.system = np.zeros(size, dtype="uint16")

# Map Generator for development
class MAPGen(MAP):
    # Aggregate all data into 
    def aggregate_and_save(self):
        pass

m = MAP([40, 40])

print(m)