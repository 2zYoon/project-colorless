# Deals with runtime data (at engine.py)

class Runtime:
    def __init__(self, **kwargs):
        self.live = {
            # Mode
            # - A mode consists of several mode bits
            "mode": [int(0), int(0), int(0)],

            # Current location
            # @mapcode: unique map code
            # @loc:     (x, y) location in map
            #           uses float type but casted to int at the end
            "mapcode": int(0),
            "loc": [float(0), float(0)],
            
            # Battle data
            # - Only used in battle phase
            "inbattle": {
                # Current turn
                # - start with 1
                "turn": int(0),

                # Character live information
                # - Initialized using...
                #   - Orignal character data
                #   - Map/event data
                "char": {
                    # Current/max HP
                    "hp_cur": int(0),
                    "hp_max": int(0),

                    # Action point
                    # - Almost all the actions consume action point
                    # - This point is re-filled after a turn
                    "act_cur": int(0),
                    "act_max": int(0),

                    # Several stats
                    "atk": int(0),
                    "def": int(0),
                },

                # Enemy live information
                # - Initialized using...
                #   - Original enemy data
                #   - Map/event data
                "enemy": {
                    # Unique enemy code
                    "enemy-code": int(0),

                    # Current/max HP
                    "hp_cur": int(0),
                    "hp_max": int(0),
                },
            }
        }

        self.config = {
            "sys": {},
            "ingame": {},
        }


    ######################
    # General Interfaces #
    ######################
    # Load all the data at initialization, from both local and remote
    # @return: returns 0 if success
    #          returns nonzero value otherwise
    def LoadAll(self):
        pass

    # Store all the data at initialization, to both local and remote
    # @return: returns 0 if success
    #          retunrs nonzero value otherwise
    def StoreAll(self):
        pass

    def Load(self, **kwargs):
        pass
    
    def Store(self, **kwargs):
        pass

    def GetLocal(self, key):
        pass

    #######################
    # In-game manipulator #
    #######################
    # Returns destination but does not move actually
    def move_ch_check(self, delta):
        return self.live["loc"][0] + delta[0], self.live["loc"][1] + delta[1]

    # Moves character
    # The caller (engine) is responsible to check
    def move_ch(self, delta):
        self.live["loc"][0] += delta[0]
        self.live["loc"][1] += delta[1]


    ##################
    # Getter/setters #
    ##################
    # Gets/sets a single bit
    def get_mode(self, modekey, bit):
        return (self.live["mode"][modekey] >> bit) & 1

    def set_mode(self, modekey, bit):
        self.live["mode"][modekey] = self.live["mode"][modekey] | (1 << bit)

    def unset_mode(self, modekey, bit):
        self.live["mode"][modekey] = self.live["mode"][modekey] & ~(1 << bit)

    # Gets/sets character location
    def get_ch_loc(self):
        return self.live["loc"]
    
    def get_ch_loc_int(self):
        return int(self.live["loc"][0]), int(self.live["loc"][1])
    
    def set_ch_loc(self, loc_new):
        self.live["loc"] = loc_new

    ####################
    # Internal methods #
    ####################
    
    # Set all/specific data to default value
    # @key: key to set
    #       if None is given, all the data is set to default
    def set_default(self, key=None, **kwargs):
        pass

    def load_local(self, key, **kwargs):
        pass

    def load_remote(self, key, **kwargs):
        pass

    def store_local(self, key, **kwargs):
        pass

    def store_remote(self, key, **kwargs):
        pass
    
    
     
