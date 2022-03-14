import configparser
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QMainWindow, QPushButton, QMessageBox
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from widgets.LogWidget import LogWidget
from widgets.MainWidget import MainWidget
from widgets.ShuttlesWidget import ShuttlesWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        chrome_service = Service(ChromeDriverManager().install())
        chrome_service.creationflags = 0x08000000
        self.main_widget = MainWidget(self, chrome_service, )
        self.shuttles_widget = ShuttlesWidget(self, chrome_service)
        self.log_widget = LogWidget(self)
        self.widgets = QtWidgets.QStackedWidget()
        self.widgets.addWidget(self.main_widget)
        self.widgets.addWidget(self.shuttles_widget)
        self.widgets.addWidget(self.log_widget)
        self.setCentralWidget(self.widgets)
        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(True)
        menu_move = menubar.addMenu('&View')
        menu_move.addAction(self._main_page_action())
        menu_move.addAction(self._shuttle_page_action())
        menu_move.addAction(self._log_page_action())
        menu_save = menubar.addMenu('&Save')
        menu_save.addAction(self._export_saved_shuttles_action())

        self.toolBar = self.addToolBar('Save this shuttle')
        self.toolBar.addAction(self._added_shuttle_action())

        self._import_external_shuttles_config()

        self.resize(750, 500)
        self._move_to_center()
        self.setWindowTitle('WebShuttle')
        self.show()

    def _go_log_widget(self, widgets):
        widgets.setCurrentIndex(2)
        self.toolBar.setVisible(False)

    def _go_setting_widget(self, widgets):
        widgets.setCurrentIndex(1)
        self.toolBar.setVisible(False)

    def _go_main_widget(self, widgets):
        widgets.setCurrentIndex(0)
        self.toolBar.setVisible(True)

    def _export_saved_shuttles_action(self):
        result = QAction('Save added shuttles', self)
        result.setShortcut('Ctrl+4')
        result.setStatusTip('Save added shuttles.')
        result.triggered.connect(self._export_saved_shuttles)
        return result

    def _log_page_action(self):
        result = QAction('Log', self)
        result.setShortcut('Ctrl+3')
        result.setStatusTip('Show the log page.')
        result.triggered.connect(lambda: self._go_log_widget(self.widgets))
        return result

    def _shuttle_page_action(self):
        result = QAction('Shuttles', self)
        result.setShortcut('Ctrl+2')
        result.setStatusTip('Show added shuttles')
        result.triggered.connect(lambda: self._go_setting_widget(self.widgets))
        return result

    def _main_page_action(self):
        result = QAction('Main', self)
        result.setShortcut('Ctrl+1')
        result.setStatusTip('Show the main page.')
        result.triggered.connect(lambda: self._go_main_widget(self.widgets))
        return result

    def _added_shuttle_action(self):
        result = QAction(QIcon('resource/images/save.png'), 'Add this shuttle', self)
        result.setShortcut('Ctrl+S')
        result.setStatusTip('Add this shuttle')
        result.triggered.connect(self._add_shuttle)
        return result

    def _move_to_center(self):
        qRect = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPos)
        self.move(qRect.topLeft())

    def _button_save(self):
        button_save = QPushButton('Save this shuttle')
        button_save.clicked.connect(self._add_shuttle)
        return button_save

    def _add_shuttle(self):
        main_widget = self.widgets.widget(0)
        shuttles_widget = self.widgets.widget(1)
        log_widget = self.widgets.widget(2)
        shuttle_name = main_widget.lineedit_shuttle_name.text()
        url = main_widget.lineedit_url.text()

        target_classes = main_widget.element_class_names
        if url is None or target_classes is None:
            QMessageBox.information(self, 'Error',
                                    'Some setting values are blank.',
                                    QMessageBox.Yes, QMessageBox.NoButton)
            return
        shuttles_widget.add_shuttle(url, 300, target_classes, shuttle_name, log_widget.get_edittext())
        QMessageBox.information(self, 'Success', 'Current settings saved in Shuttles menu.\n(Shortcut keys : Ctrl+2)',
                                QMessageBox.Yes, QMessageBox.NoButton)

    def _export_saved_shuttles(self):
        config = configparser.ConfigParser()
        saved_shuttles_tuple_list = self.shuttles_widget.get_saved_shuttles_array()
        for saved_shuttle in saved_shuttles_tuple_list:
            shuttle_id = saved_shuttle[0]
            shuttle_config_list = saved_shuttle[1]
            config[shuttle_id] = {}
            attributes = ['name', 'url', 'period', 'element_classes']
            for i in range(0, len(shuttle_config_list)):
                config[shuttle_id][attributes[i]] = shuttle_config_list[i]
        with open('shuttlesConfig.ini', 'w') as configfile:
            config.write(configfile)

    def _import_external_shuttles_config(self):
        config = configparser.ConfigParser()
        config.read('shuttlesConfig.ini', encoding='utf-8')
        for shuttle_id in config.sections():
            shuttle_name = config[shuttle_id]['name']
            url = config[shuttle_id]['url']
            period = config[shuttle_id]['period']
            element_classes = config[shuttle_id]['element_classes']
            self.shuttles_widget.add_shuttle(name=shuttle_name, url=url, period=period, target_classes=element_classes,
                                             log_edittext=self.log_widget.get_edittext())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())