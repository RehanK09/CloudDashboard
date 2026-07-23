import customtkinter as ctk

from graph import SpeedGraph
from logger import CloudLogger

from ui.window_manager import WindowManager
from ui.header import Header
from ui.status_card import StatusCard
from ui.progress_card import ProgressCard
from ui.activity_card import ActivityCard
from ui.controls import Controls
from ui.graph_card import GraphCard
from ui.refresh import RefreshManager

from utils import ask_exit, shutdown_everything


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Dashboard:

    def __init__(self):

        self.app = ctk.CTk()

        self.app.title("Cloud Dashboard")

        self.app.geometry("1100x850")

        self.app.minsize(1000, 800)

        CloudLogger.dashboard_opened()

        self.graph = SpeedGraph()

        self.window_manager = WindowManager(self.app)

        self.header = Header(
            self.app,
            self.window_manager,
            "X:"
        )

        self.status = StatusCard(
            self.app
        )

        self.progress = ProgressCard(
            self.app
        )

        self.activity = ActivityCard(
            self.app
        )

        self.controls = Controls(
            self.app
        )

        self.graph_card = GraphCard(
            self.app,
            self.graph
        )

        self.refresh = RefreshManager(

            self.app,

            self.status,

            self.progress,

            self.activity,

            self.graph_card,

            self.graph

        )

        self.controls.set_refresh_callback(
            self.refresh.force_refresh
        )

        self.app.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

    def close(self):

        stats = self.refresh.app.title()

        running = "Transfer" in stats

        if not ask_exit(running):
            return

        self.refresh.stop()

        CloudLogger.dashboard_closed()

        shutdown_everything("X:")

        self.app.destroy()

    def run(self):

        print("Starting API...")

        self.refresh.start()

        print("Entering mainloop...")

        self.app.mainloop()
        
if __name__ == "__main__":

    Dashboard().run()