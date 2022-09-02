# Tile-granularity map data

import numpy as np

from _lib.commons import *

# Metadata bitmap
class Map:
    def __init__(self, size, name="UNTITLED"):
        ##########
        # GLOBAL #
        ##########
        # Global metadata
        self.meta = 0x0
        self.bgm = 0x0
        self.size = size


        ############
        # PER-TILE #
        ############

        # Metadata per tile
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
        #     0: Layer N specifies color code
        #     1: Layer N specifies tile code 
        self.meta_per_tile = np.zeros(size, dtype="uint32")
        
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

    def get_size(self):
        return self.size

    def get_size_grid(self):
        return [self.size[0] * GRID(1), self.size[1] * GRID(1)]


# Map Generator for development
class MapGen(Map):
    # Aggregate all data into 
    def aggregate_and_save(self):
        pass

m_test = Map([10, 10])
a = np.array(list(range(100)))
a.resize([10, 10])
m_test.meta_per_tile = a
#m_test.meta_per_tile = np.array([0] * 100).resize([10, 10])
m_test.layer1 = np.array([0x00ff00ff] * 100).resize([10, 10])

#print(m_test.meta_per_tile)
#for i in m_test.meta_per_tile:
#    print(i)