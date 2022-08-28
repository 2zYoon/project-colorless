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
        #   010: Normal local link, within a map 
        #   011: Forceful local link,
        # 
        #  
        # 
        # 

        # [ ] For visuailzation
        #     0: Use LAYER 0 (under the chracter)
        #     1: Use LAYER 1 (on the character)
        # [2] 
        self.meta = np.zeros(size, dtype="uint16")
        
        # Layer1: Layer1 mapcode. Mostly used. This is under the character
        # 0 is reserved for UNUSED
        self.layer1 = np.zeros(size, dtype="uint16")

        # Layer2: This is on the chracter
        # 0 is reserved for UNUSED
        self.layer2 = np.zeros(size, dtype="uint16")

        # Ingame: Used in game
        # [0] movable
        # [1] 
        self.ingame = np.zeros(size, dtype="uint16")

# Map Generator for development
class MapGen(Map):
    # Aggregate all data into 
    def aggregate_and_save(self):
        pass

m = Map([40, 40])

print(m)