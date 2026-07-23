from tkinter import messagebox

from api import rclone_api
from utils import shutdown_everything


class Lifecycle:

    def __init__(self, layout):

        self.layout = layout

        self.app = layout.app

        self.refresh = layout.refresh

        self.tray = layout.tray

        self.drive = layout.drive

        self.tray.set_exit_callback(
            self.exit_application
        )

    def start(self):

        self.tray.start()

        self.refresh.start()

    def exit_application(self):

        stats = rclone_api.get_stats()

        transfers = stats.get(
            "transferring",
            []
        )

        if transfers:

            ok = messagebox.askyesno(

                "Upload Running",

                "Upload is still in progress.\n\n"
                "Exit anyway?"

            )

            if not ok:
                return

        self.refresh.stop()

        shutdown_everything(
            self.drive
        )

        try:

            if self.tray.icon:
                self.tray.icon.stop()

        except:
            pass

        self.app.destroy()