from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QStyleFactory
from PyQt5.QtCore import Qt

# Make sure QApp is constructed before widget
class GUI(QWidget):
    def __init__(self, **config):
        super().__init__()

        self.config = config
        self.default = {
            "title": " ",
            "w": 320,
            "h": 240,
            "opacity": 1,

            "stylesheet": """
                background-color: #10105F;
            """,

            "winflags": Qt.Window
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
        self.setWindowFlags(self.cfg("winflags"))

        self.setStyleSheet(self.cfg("stylesheet"))

        self.setWindowOpacity(self.cfg("opacity"))
        self.setWindowTitle(self.cfg("title"))
        self.resize(self.cfg("w"), self.cfg("h"))
        
        self.center()

    # Add button on demand
    def add_button(self, name="Button", x=0, y=0, stylesheet="", tooltip=None, func_cb=None):
        button = QPushButton(name, self)
        
        if tooltip != None:
            button.setToolTip(str(tooltip))

        if func_cb != None:
            button.clicked.connect(func_cb)

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