from PyQt5.QtWidgets import QTextEdit

from webshuttle.domain.Observer import Observer
from webshuttle.domain.Subject import Subject


class ShuttleWidgetGroup(Subject):
    def __init__(self, state_widget, target_classes_widget, period_widget, url_widget, shuttle_name_widget,
                 filtering_keyword_widget="", parent=None):

        self.state_widget: QTextEdit = state_widget
        self.target_classes_widget = target_classes_widget
        self.period_widget = period_widget
        self.url_widget = url_widget
        self.shuttle_name_widget = shuttle_name_widget
        self.filtering_keyword_widget = filtering_keyword_widget
        self.parent = parent
        self.observer_list: list = []

    def register_observer(self, observer: Observer):
        self.observer_list.append(observer)

    def remove_observer(self, observer: Observer):
        self.observer_list.remove(observer)

    def notify_update(self):
        for observer in self.observer_list:
            observer.update()

    def get_url_widget(self):
        return self.url_widget
