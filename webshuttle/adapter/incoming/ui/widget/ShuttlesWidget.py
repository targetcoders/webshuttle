import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from webshuttle.adapter.incoming.ui.widget.shuttle.ShuttleDeleteButton import ShuttleDeleteButton
from webshuttle.adapter.incoming.ui.widget.shuttle.ShuttleFrame import ShuttleFrame
from webshuttle.adapter.incoming.ui.widget.shuttle.ShuttleLayout import ShuttleLayout
from webshuttle.application.port.incoming import LoadShuttlesUseCase
from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.incoming.ExportShuttlesUseCase import ExportShuttlesUseCase
from webshuttle.application.port.incoming.GetShuttlesUseCase import GetShuttlesUseCase
from webshuttle.domain.ShuttleWidgetGroup import ShuttleWidgetGroup

pygame.init()


class ShuttlesWidget(QWidget):
    def __init__(self, parent, chrome_driver, get_shuttles_usecase, load_shuttles_usecase, export_shuttles_usecase,
                 file_name="shuttle.json"):
        super(ShuttlesWidget, self).__init__(parent)
        self.shuttle_seq = 0
        self.shuttle_frames = {}
        self.shuttles = {}
        self.driver_chrome = chrome_driver
        self._init_ui()
        self.file_name = file_name
        self.get_shuttles_service: GetShuttlesUseCase = get_shuttles_usecase
        self.load_shuttles_service: LoadShuttlesUseCase = load_shuttles_usecase
        self.export_shuttles_service: ExportShuttlesUseCase = export_shuttles_usecase

    def _init_ui(self):
        self.title_vbox_layout = QVBoxLayout()
        self.shuttles_vbox_layout = QVBoxLayout()
        self.title_vbox_layout.addWidget(QLabel('셔틀 목록'))
        wrap_vbox_layout = QVBoxLayout()
        wrap_vbox_layout.addLayout(self.title_vbox_layout)
        wrap_vbox_layout.addLayout(self.shuttles_vbox_layout)
        stretch_vbox_layout = QVBoxLayout()
        stretch_vbox_layout.addStretch(4)
        wrap_vbox_layout.addLayout(stretch_vbox_layout)
        self.setLayout(wrap_vbox_layout)
        self.show()

    def add_shuttle(self, shuttle_widget_group: ShuttleWidgetGroup):
        shuttle_frame = ShuttleFrame(shuttles=self.shuttles,
                                     shuttle_seq=self.shuttle_seq,
                                     chrome_driver=self.driver_chrome,
                                     shuttle_widget_group=shuttle_widget_group,
                                     shuttles_widget=self)
        self.shuttle_frames[self.shuttle_seq] = shuttle_frame
        self._add_shuttle_hbox_layout_to_vbox_layout(shuttle_frame, shuttle_widget_group)
        self.shuttle_seq += 1
        self.save_shuttles()

    def _add_shuttle_hbox_layout_to_vbox_layout(self, shuttle_frame, shuttle_widget_group):
        shuttle_delete_button = ShuttleDeleteButton(self, shuttle_frame, shuttle_widget_group)
        self.shuttles_vbox_layout.addLayout(ShuttleLayout(shuttle_frame.get_frame_widget(), shuttle_delete_button))

    def save_shuttles(self):
        export_shuttles_command = ExportShuttlesCommand(shuttle_properties_list=self.saved_shuttles_json(), file_name=self.file_name)
        self.export_shuttles_service.export(export_shuttles_command)

    def saved_shuttles_json(self):
        if self.shuttles_vbox_layout is None:
            return {}
        return self.get_shuttles_service.saved_shuttles_to_json(self.shuttle_frames)

