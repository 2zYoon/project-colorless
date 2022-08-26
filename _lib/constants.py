
##########
# Common #
##########

# Colors
TRANSPARENT =   (0, 0, 0, 0)
WHITE =         (255, 255, 255)
BLACK =         (0, 0, 0)
GRAY =          (128, 128, 128)
GRAY10 =        (26, 26, 26)
GRAY20 =        (51, 51, 51)
GRAY30 =        (76, 76, 76)
GRAY40 =        (102, 102, 102)
GRAY50 =        (128, 128, 128)
GRAY60 =        (153, 153, 153)
GRAY70 =        (179, 179, 179)
GRAY80 =        (204, 204, 204)
GRAY90 =        (230, 230, 230)


############
# Launcher #
############

# Layouts
# key: (val-small, val-medium, val-large)
LAYOUT_SMALL = 0
LAYOUT_MEDIUM = 1
LAYOUT_LARGE = 2

LAUNCHER_LAYOUT = {
    # Window size: (w, h)
    "window": [ 
        (400, 300), 
        (800, 600),
        (1200, 900)
    ],
    # Game start button: (w, h, x, y)
    "btn_gamestart": [
        (280, 40, 10, 250, 30),
        (460, 50, 50, 510, 36),
        (740, 100, 60, 750, 48)
    ],
    # Setting button: (w, h, x, y, font-size)
    "btn_setting": [
        (90, 40, 300, 250, 22),
        (200, 50, 540, 510, 28),
        (300, 100, 840, 750, 40)
    ],
}

# Stylesheets
SS_BUTTON_DEFAULT = """
QPushButton { 
    background-color: #202020; 
    border: none; 
    border-radius: 5px; 
    font-size: 36px; 
    color: #dddddd; 
} 
QPushButton:hover { 
    background-color: #303030; 
}"""

SS_BUTTON_CTRL_DEFAULT = """
QPushButton { 
    border: none; 
    font: bold; 
    font-size: 15px; 
} 
QPushButton:hover { 
    background-color: #303030; 
}"""

SS_BUTTON_CTRL_DISABLED = """
QPushButton { 
    border: none; 
    font: bold; 
    font-size: 15px; 
    color: gray; 
}"""

SS_FONTSIZE = ["QPushButton { font-size: %dpx; }" % i for i in range(100) ]

###############
# Game engine #
###############
FPS = 60
MOVE_SCALE = 10




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