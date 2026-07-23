import customtkinter as ctk

from history import open_history_window
from settings import open_settings_window


class WindowManager:

    def __init__(self, app):

        self.app = app

    def open_history(self):

        open_history_window(self.app)

    def open_settings(self):

        open_settings_window(self.app)

    def focus_main(self):

        self.app.deiconify()

        self.app.lift()

        self.app.focus_force()

    def minimize(self):

        self.app.iconify()

    def maximize(self):

        self.app.state("zoomed")

    def restore(self):

        self.app.state("normal")

    def close(self):

        self.app.destroy()