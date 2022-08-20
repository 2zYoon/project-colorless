# Several constants
from typing import Final

##########
# Common #
##########

# Colors
WHITE: Final =      (255, 255, 255)
BLACK: Final =      (0, 0, 0)
GRAY: Final =       (128, 128, 128)
GRAY10: Final =     (26, 26, 26)
GRAY20: Final =     (51, 51, 51)
GRAY30: Final =     (76, 76, 76)
GRAY40: Final =     (102, 102, 102)
GRAY50: Final =     (128, 128, 128)
GRAY60: Final =     (153, 153, 153)
GRAY70: Final =     (179, 179, 179)
GRAY80: Final =     (204, 204, 204)
GRAY90: Final =     (230, 230, 230)


############
# Launcher #
############

# Layouts
# key: (val-small, val-medium, val-large)
LAYOUT_SMALL: Final = 0
LAYOUT_MEDIUM: Final = 1
LAYOUT_LARGE: Final = 2

LAUNCHER_LAYOUT: Final = {
    # Window size: (w, h)
    "window": [ 
        (400, 300), 
        (800, 600),
        (1200, 900)
    ],
    # Game start button: (w, h, x, y)
    "btn_gamestart": [
        (280, 90, 10, 200, 30),
        (460, 100, 50, 460, 36),
        (740, 150, 60, 700, 48)
    ],
    # Setting button: (w, h, x, y, font-size)
    "btn_setting": [
        (90, 90, 300, 200, 22),
        (200, 100, 540, 460, 28),
        (300, 150, 840, 700, 40)
    ],
}

# Stylesheets
SS_BUTTON_DEFAULT: Final = """
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

SS_BUTTON_CTRL_DEFAULT: Final = """
QPushButton { 
    border: none; 
    font: bold; 
    font-size: 15px; 
} 
QPushButton:hover { 
    background-color: #303030; 
}"""

SS_BUTTON_CTRL_DISABLED: Final = """
QPushButton { 
    border: none; 
    font: bold; 
    font-size: 15px; 
    color: gray; 
}"""

SS_FONTSIZE: Final = ["QPushButton { font-size: %dpx; }" % i for i in range(100) ]

###############
# Game engine #
###############
FPS: Final = 60
