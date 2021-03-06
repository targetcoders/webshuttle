import atexit

from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from webshuttle.adapter.incoming.ui.BaseWidget import BaseWidget
from webshuttle.adapter.incoming.ui.StateWidget import StateWidget
from webshuttle.adapter.incoming.ui.ShuttleAddWidget import ShuttleAddWidget
from webshuttle.adapter.incoming.ui.ShuttlesWidget import ShuttlesWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.chrome_driver = ChromeDriverManager().install()
        self.shuttles_widget = ShuttlesWidget(self, self.chrome_driver)
        self.statusBar()
        self.state_widget = StateWidget(self)
        self.shuttle_add_widget = ShuttleAddWidget(self, self.shuttles_widget, self.state_widget, self.chrome_driver)
        self.base_widget = BaseWidget(self, self.shuttle_add_widget, self.shuttles_widget, self.state_widget)
        self.setCentralWidget(self.base_widget)

        self.shuttles_widget.import_external_shuttles(self.state_widget)

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())
