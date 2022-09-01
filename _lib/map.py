# Tile-granularity map data

import numpy as np

#



class Map:
    def __init__(self, size, name="UNTITLED"):
        # Meta: Overall metadata 
        #       this must be checked at the first
        # [0-2] Type
        #   000: Normal movable tile
        #   001: Not movable, such as wall
        #   010: Normal local link 
        #   011: Forceful local link
        #   100: Normal remote link
        #   101: Forceful remote link
        #   100: Battle field
        #   111: UNUSED
        #
        # [3] Layer used
        #     0: Use LAYER 0 (under the chracter)
        #     1: Use LAYER 1 (on the character)
        # 
        # [4] Code for visualization
        #     0: Layer N specifies tile code
        #     1: Layer N specifies color code
        self.meta = np.zeros(size, dtype="uint32")
        
        # Layer1: Layer1 mapcode. Mostly used. This is under the character
        # 0 is reserved for UNUSED
        self.layer1 = np.zeros(size, dtype="uint32")

        # Layer2: This is on the chracter
        # 0 is reserved for UNUSED
        self.layer2 = np.zeros(size, dtype="uint32")

        # Ingame: Used in game
        # [0] movable
        # [1] 
        self.ingame = np.zeros(size, dtype="uint32")

# Map Generator for development
class MapGen(Map):
    # Aggregate all data into 
    def aggregate_and_save(self):
        pass

m = Map([40, 40])

print(m)