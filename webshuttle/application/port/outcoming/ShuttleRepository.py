from webshuttle.application.port.incoming.ExportShuttlesCommand import ExportShuttlesCommand
from webshuttle.application.port.incoming.LoadShuttlesCommand import LoadShuttlesCommand


class ShuttleRepository:
    def export(self, export_shuttles_command: ExportShuttlesCommand):
        pass

    def load(self, shuttles_widget, state_widget):
        pass
