#!/usr/bin/env python
import os, sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication

from _lib.gui import GUI
from _lib.runtime import Runtime


###########
# Globals #
###########




##################
# Initialization #
##################
app = QApplication([])

launcher_cfg = {
    "title": "Game Launcher",
    "w": 800,
    "h": 600,
}

launcher_main = GUI(**launcher_cfg)

a = lambda: sys.exit()

ss_button_interact = \
"""
QPushButton {
    background-color: #202020;
    border: none;
    border-radius: 5px;
    font-size: 36px;
    color: #dddddd;
}
QPushButton:hover {
    background-color: #303030;
}
"""

launcher_main.add_button(name="Game Start", w=400, h=100, x=40, y=460,
    func_cb=a,
    stylesheet=ss_button_interact
)
launcher_main.add_button(name="Setting", w=150, h=45, x=450, y=460,
    func_cb=a,
    stylesheet=ss_button_interact + "QPushButton { font-size: 24px; }"
)
launcher_main.add_button(name="Credits", w=150, h=45, x=450, y=515,
    func_cb=a,
    stylesheet=ss_button_interact + "QPushButton { font-size: 24px; }"
)
launcher_main.add_button(name="TEMP", w=150, h=100, x=610, y=460,
    func_cb=a,
    stylesheet=ss_button_interact + "QPushButton { font-size: 24px; }"
)

########
# Test #
########


############
# Launcher #
############
launcher_main.ready()
app.exec_()




#ex1 = GUI()

#qapp.exec_()