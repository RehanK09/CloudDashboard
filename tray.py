import threading
import pystray

from PIL import Image, ImageDraw

from history import open_history_window
from settings import open_settings_window
from api import rclone_api
from utils import open_drive


class TrayManager:

    def __init__(self, app, window_manager, drive_letter):

        self.app = app
        self.window_manager = window_manager
        self.drive_letter = drive_letter

        self.icon = None

        self.exit_callback = None

    def set_exit_callback(self, callback):

        self.exit_callback = callback

    def _create_icon(self):

        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))

        draw = ImageDraw.Draw(image)

        draw.ellipse((8, 8, 56, 56), fill=(30, 144, 255))
        draw.ellipse((20, 20, 44, 44), fill=(255, 255, 255))

        return image

    def _menu(self):

        return pystray.Menu(

            pystray.MenuItem(
                "Open Dashboard",
                self.restore
            ),

            pystray.MenuItem(
                "Open Drive",
                lambda: open_drive(self.drive_letter)
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "History",
                lambda: open_history_window(self.app)
            ),

            pystray.MenuItem(
                "Settings",
                lambda: open_settings_window(self.app)
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Pause Uploads",
                lambda: rclone_api.pause_uploads()
            ),

            pystray.MenuItem(
                "Resume Uploads",
                lambda: rclone_api.resume_uploads()
            ),

            pystray.Menu.SEPARATOR,

            pystray.MenuItem(
                "Exit",
                self.exit_app
            )

        )

    def start(self):

        if self.icon:
            return

        self.icon = pystray.Icon(
            "CloudDashboard",
            self._create_icon(),
            "Cloud Dashboard",
            self._menu()
        )

        threading.Thread(
            target=self.icon.run,
            daemon=True
        ).start()

    def hide(self):

        self.app.withdraw()

    def restore(self, icon=None, item=None):

        self.app.after(
            0,
            self.window_manager.focus_main
        )

    def exit_app(self, icon=None, item=None):

        if self.exit_callback:

            self.app.after(
                0,
                self.exit_callback
            )

        if self.icon:

            self.icon.stop()