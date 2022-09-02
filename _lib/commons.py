# DO NOT INCLUDE ANY INTERNAL LIBS

########################
# Color, Visualization #
########################
TRANSPARENT =   (0, 0, 0, 0)
WHITE =         (255, 255, 255)
BLACK =         (0, 0, 0)
GRAY =          (128, 128, 128)

BLACK_PERCENT = lambda pct: [int(255 * (100-pct) / 100)] * 3
ALPHA = lambda pct: int(255 * pct / 100)


############
# Launcher #
############


###############
# Game engine #
###############
FPS = 60
MOVE_SCALE = 1.0

GRID_UNIT=32
GRID = lambda n_grid: int(n_grid * GRID_UNIT)
COORDINATE_TO_GRID = lambda x: int(min(0, x // GRID_UNIT))

#############
# Mode bits #
#############

# Mode key (used by Runtime)
MODE_KEY_SYS = 0
MODE_KEY_GP = 1



# System
MODEBIT_SYS_MOVE_4K_ALLOWED    = 0  # Handles up/down/left/right key event for character moving
MODEBIT_SYS_MOVE_STUCK         = 1  # Does not move actually

# Graphic
MODEBIT_GP_SHOW_LEFT_MENU       = 10
MODEBIT_GP_SHOW_RIGHT_MENU     = 20

MODEBIT_GP_SHOW_GRID          = 50 # Show grid

LIST_MODE_INITIAL_SET = [
    None
]


