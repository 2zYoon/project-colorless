# Grid-granularity map data

import os
import numpy as np

from _lib.commons import *

MAP_BASEDIR = os.path.join(os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "gamedat"), "map")

SUFFIX_MAP_META = "_meta"
SUFFIX_MAP_DATA = "_data"


TILEMETA_NORMAL                 = 0
TILEMETA_WALL                   = 1
TILEMETA_LOCALLINK              = 2
TILEMETA_LOCALLINK_FORCEFUL     = 3
TILEMETA_REMOTELINK             = 4
TILEMETA_REMOTELINK_FORCEFUL    = 5

LAYER_UNDER_CHARACTER           = 4
LAYER_OVER_CHARACTER            = 6

RENDER_TYPE_COLOR               = 0
RENDER_TYPE_IMAGE               = 1

# Metadata bitmap
class Map:
    def __init__(self, size=[-1, -1], name="UNTITLED", name_to_load=None):        
        ##########
        # GLOBAL #
        ##########

        self.name = name

        # Global metadata
        self.flags = 0x0

        # Base BGM code
        self.basebgm = 0

        # map size (grid)
        self.size = size

        ############
        # PER-TILE #
        ############

        # Tile type
        # [0-2] Type
        #   000: Normal movable tile
        #   001: Not movable, such as wall
        #   010: Normal local link 
        #   011: Forceful local link
        #   100: Normal remote link
        #   101: Forceful remote link
        #   100: UNUSED
        #   111: UNUSED
        #
        # [3-4] Battle field
        #    00: peaceful field (battle gauge does not increase)
        #    01: battle field (battle gauge increases as move)
        #    10: UNUSED
        #    11: UNUSED
        #
        # [5] Layer used
        #     0: Use LAYER 0 (under the chracter)
        #     1: Use LAYER 1 (on the character)
        # 
        # [6] Code for visualization
        #     0: LayerN specifies color code
        #     1: LayerN specifies image code 
        self.meta_per_tile = None 
        
        # Layer1: Layer1 mapcode. Mostly used. This is under the character
        # 0 is reserved for UNUSED
        self.layer1 = None
        
        # Layer2: This is on the chracter
        # 0 is reserved for UNUSED
        self.layer2 = None
        
        # Ingame: Used in game
        # [0] 
        # [1] 
        self.ingame = None
        
        if name_to_load != None:
            self.__load(name_to_load)
            return

        elif size[0] != -1 and size[1] != -1:
            self.meta_per_tile = np.zeros(size, dtype="uint32")            
            self.layer1 = np.zeros(size, dtype="uint32")
            self.layer2 = np.zeros(size, dtype="uint32")
            self.ingame = np.zeros(size, dtype="uint32")
            return

        else:
            raise ValueError("ERROR: Invalid map size")

    # @mapname: map ename (suffix excluded)
    def __load(self, mapname):
        with open(os.path.join(MAP_BASEDIR, mapname + SUFFIX_MAP_META)) as f:
            self.name = f.readline().strip()
            self.flags = int(f.readline().strip()) 
            self.basebgm = int(f.readline().strip())
            self.size[0] = int(f.readline().strip())
            self.size[1] = int(f.readline().strip())

        loaded = np.load(os.path.join(MAP_BASEDIR, mapname + SUFFIX_MAP_DATA + ".npz"), allow_pickle=True)
        self.meta_per_tile = loaded["meta_per_tile"]
        self.layer1 = loaded["layer1"]
        self.layer2 = loaded["layer2"]
        self.ingame = loaded["ingame"]

    def get_global_meta(self):
        return [
            self.name,
            self.flags,
            self.basebgm,
            self.size[0],
            self.size[1],
            ]

    def get_size_grid(self):
        return self.size

    def get_size(self):
        return [self.size[0] * GRID(1), self.size[1] * GRID(1)]

    # @return: [screen_num(layer), render_type(img/color), value(imgcode/colorcode)]
    def render_tile(self, x, y):
        meta = self.meta_per_tile[x, y]

        # screen number to render
        meta_layer = (meta >> 5) & 0x1
        if meta_layer == 1:
            screen_num = LAYER_OVER_CHARACTER
        else:
            screen_num = LAYER_UNDER_CHARACTER

        # render type (image or color)
        meta_render_type = (meta >> 6) & 0x1
        if meta_render_type == 1:
            render_type = RENDER_TYPE_IMAGE
        else:
            render_type = RENDER_TYPE_COLOR
        
        # value
        if screen_num == LAYER_OVER_CHARACTER:
            value = self.layer2[x, y]
        else:
            value = self.layer1[x, y]

        return [screen_num, render_type, value]


# Map Generator for development
class MapGen(Map):
    def save(self):
        name_meta = self.name + SUFFIX_MAP_META
        name_data = self.name + SUFFIX_MAP_DATA

        with open(os.path.join(MAP_BASEDIR, name_meta), "w") as f:
            for dat in list(map(str, self.get_global_meta())):
                f.write(dat + "\n")

        np.savez(os.path.join(MAP_BASEDIR, name_data),
                meta_per_tile=self.meta_per_tile,
                layer1=self.layer1,
                layer2=self.layer2,
                ingame=self.ingame,
                )



m_test = MapGen(name_to_load="test")
m_test.meta_per_tile = np.zeros([24, 10], dtype="uint32")
a = np.zeros([24, 10], dtype="uint32")
a[:, :] = 0x00ff00ff
a[1:4, 1:6] = 0xff0000ff

m_test.layer1 = a

#m_test = MapGen([24, 10], "test")
#a = np.array(list(range(240)))
#a.resize([24, 10])
#m_test.meta_per_tile = a
#m_test.layer1 = np.array([0x00ff00ff] * 240).resize([24, 10])

#m_test.save()
#print(m_test.meta_per_tile)
#for i in m_test.meta_per_tile:
#    print(i)