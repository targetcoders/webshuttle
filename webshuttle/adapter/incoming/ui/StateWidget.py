from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel


class StateWidget(QWidget):
    def __init__(self, parent):
        super(StateWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self._vbox_layout = QVBoxLayout()
        title = QLabel()
        title.setText("현황")
        self._log_textedit = QTextEdit()
        self._log_textedit.setReadOnly(True)
        self._vbox_layout.addWidget(title)
        clear_btn = QPushButton('지우기')
        clear_btn.clicked.connect(self.clear_text)
        self._vbox_layout.addWidget(clear_btn)
        self._vbox_layout.addWidget(self._log_textedit)
        self.setLayout(self._vbox_layout)
        self.show()

    def get_text_edit(self):
        return self._log_textedit

    def clear_text(self):
        self._log_textedit.clear()
