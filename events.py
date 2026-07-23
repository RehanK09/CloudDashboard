from history import open_history_window
from settings import open_settings_window


class Events:

    def __init__(self, layout):

        self.layout = layout

        self.app = layout.app

        self.header = layout.header

        self.tray = layout.tray

        self.window_manager = layout.window_manager

        self._bind()

    def _bind(self):

        self.header.history_btn.configure(
            command=self.show_history
        )

        self.header.settings_btn.configure(
            command=self.show_settings
        )

        self.app.protocol(
            "WM_DELETE_WINDOW",
            self.hide_to_tray
        )

    def show_history(self):

        open_history_window(
            self.app
        )

    def show_settings(self):

        open_settings_window(
            self.app
        )

    def hide_to_tray(self):

        self.tray.hide()