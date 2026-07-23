import json
import customtkinter as ctk

from graph import SpeedGraph

from ui.window_manager import WindowManager
from ui.header import Header
from ui.status_card import StatusCard
from ui.progress_card import ProgressCard
from ui.activity_card import ActivityCard
from ui.controls import Controls
from ui.graph_card import GraphCard
from ui.refresh import RefreshManager

from tray import TrayManager


class Layout:

    def __init__(self, app):

        self.app = app

        with open("config.json") as f:
            cfg = json.load(f)

        self.drive = cfg["drives"][0]["drive"]

        self.graph = SpeedGraph()

        self.window_manager = WindowManager(app)

        # -------------------------------------------------

        self.header = Header(
            app,
            self.window_manager,
            self.drive
        )

        self.status = StatusCard(app)

        # ===================== BODY ======================

        self.body = ctk.CTkFrame(
            app,
            fg_color="transparent"
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_rowconfigure(1, weight=1)

        # -------------------------------------------------

        self.left_top = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        self.left_top.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,8),
            pady=(0,8)
        )

        self.right_top = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        self.right_top.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8,0),
            pady=(0,8)
        )

        self.left_bottom = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        self.left_bottom.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0,8)
        )

        self.right_bottom = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        self.right_bottom.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8,0)
        )

        # -------------------------------------------------

        self.progress = ProgressCard(
            self.left_top
        )

        self.graph_card = GraphCard(
            self.right_top,
            self.graph
        )

        self.activity = ActivityCard(
            self.left_bottom
        )

        self.controls = Controls(
            self.right_bottom
        )

        # -------------------------------------------------

        self.refresh = RefreshManager(
            app,
            self.status,
            self.progress,
            self.activity,
            self.graph_card,
            self.graph
        )

        self.tray = TrayManager(
            app,
            self.window_manager,
            self.drive
        )

        self.controls.set_refresh_callback(
            self.refresh.force_refresh
        )