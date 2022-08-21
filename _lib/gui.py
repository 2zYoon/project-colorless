from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyleFactory
from PyQt5.QtCore import Qt, QSize

# Make sure QApp is constructed before widget
class GUI(QWidget):
    def __init__(self, **config):
        super().__init__()

        self.config = config
        self.default = {
            "title": " ",
            "w": 320,
            "h": 240,
            "opacity": 1.0,

            "stylesheet": 
            """
                background-color: #404040; 
            """,

            "winflags": Qt.Window,

            # Button: enable | disable | hide
            "min-button": "enable",
            "max-button": "disable",
            "close-button": "enable",
        }
        
        self.initUI()

    # Ready to show
    def ready(self):
        self.show()

    # Helps get configuration and set default value
    def cfg(self, key):
        try:
            return self.config.get(key, self.default[key])
        except:
            raise KeyError("GUI default config is not defined ({})".format(key))

    # Basic UI initializtion
    def initUI(self):
        # apply configurations
        self.setWindowFlags(self.cfg("winflags"))
        self.setStyleSheet(self.cfg("stylesheet"))
        self.setWindowOpacity(self.cfg("opacity"))
        self.setWindowTitle(self.cfg("title"))
        self.setFixedSize(self.cfg("w"), self.cfg("h"))        \

        self.center()



    # Add button on demand
    def add_button(self, name="Button", w=None, h=None, x=0, y=0, stylesheet="", tooltip=None, func_cb=None):

        button = QPushButton(name, self)
        
        if tooltip != None:
            button.setToolTip(str(tooltip))

        if func_cb != None:
            button.clicked.connect(func_cb)
    
        if w != None and h != None:
            button.setFixedSize(QSize(w, h))

        button.setStyleSheet(stylesheet)
        
        button.move(x, y)
        
    # Allows centering on "active" screen
    # https://stackoverflow.com/questions/20243637/pyqt4-center-window-on-active-screen
    def center(self):
        qr = self.frameGeometry()
        scr = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        cp = QApplication.desktop().screenGeometry(scr).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
