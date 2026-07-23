import customtkinter as ctk

from widgets.header import Header
from widgets.graph import GraphWidget
from widgets.stats import StatsWidget
from widgets.activity import ActivityWidget
from widgets.quick_actions import QuickActions

from storage.storage_card import StorageCard

from transfer.transfer_manager import TransferManager

from core.refresh import RefreshManager
from core.api import api


from transfer.upload_panel import UploadPanel


class DashboardV4:

    def __init__(self, app):

        self.app = app

        # ======================================================
        # ROOT
        # ======================================================

        self.root = ctk.CTkFrame(
            app,
            fg_color="transparent"
        )

        self.root.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        # Layout
        #
        # Header
        #
        # Left | Center | Right
        #
        # Bottom Toolbar
        #

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)

        self.root.grid_columnconfigure(0, weight=28)
        self.root.grid_columnconfigure(1, weight=47)
        self.root.grid_columnconfigure(2, weight=25)

        # ======================================================
        # HEADER
        # ======================================================

        self.header = Header(self.root)

        self.header.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(0,8)
        )

        # ======================================================
        # LEFT
        # ======================================================

        self.left = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        self.left.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0,6)
        )

        self.left.grid_rowconfigure(0, weight=45)
        self.left.grid_rowconfigure(1, weight=55)

        # ======================================================
        # CENTER
        # ======================================================

        self.center = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        self.center.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=6
        )

        self.center.grid_rowconfigure(0, weight=58)
        self.center.grid_rowconfigure(1, weight=42)

        # ======================================================
        # RIGHT
        # ======================================================

        self.right = ctk.CTkFrame(
            self.root,
            corner_radius=15
        )

        self.right.grid(
            row=1,
            column=2,
            sticky="nsew",
            padx=(6,0)
        )

        self.right.grid_rowconfigure(0, weight=1)

        # ======================================================
        # BOTTOM BAR
        # ======================================================

        self.toolbar = ctk.CTkFrame(
            self.root,
            height=48,
            corner_radius=12
        )

        self.toolbar.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(8,0)
        )

        self.toolbar.grid_propagate(False)

        # ======================================================
        # LEFT SIDE
        # ======================================================

        self.storage = StorageCard(self.left)

        self.storage.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(8,4)
        )

        self.graph = GraphWidget(self.left)

        self.graph.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(4,8)
        )

        # ======================================================
        # CENTER
        # ======================================================

        # self.transfer_manager = TransferManager(self.center)

        # self.transfer_manager.grid(
        #     row=0,
        #     column=0,
        #     sticky="nsew",
        #     padx=8,
        #     pady=(8,4)
        # )

        self.upload_panel = UploadPanel(
            self.center
        )
        
        self.upload_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(8,4)
        )

        self.activity = ActivityWidget(self.center)

        self.activity.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(4,8)
        )

        # ======================================================
        # RIGHT
        # ======================================================

        self.stats = StatsWidget(self.right)

        self.stats.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=8
        )

        # ======================================================
        # TOOLBAR
        # ======================================================

        self.actions = QuickActions(self.toolbar)

        self.actions.pack(
            pady=5
        )

        # ======================================================
        # BACKEND
        # ======================================================

        self.refresh = RefreshManager(self)

        self.refresh.api = api

        self.refresh.start()


    # ======================================================
    # API
    # ======================================================

    def refresh_all(self):

        try:
            self.storage.refresh()
        except:
            pass

        try:
            pass
        except:
            pass

        try:
            self.graph.refresh()
        except:
            pass

        try:
            self.stats.refresh()
        except:
            pass

        try:
            self.activity.refresh()
        except:
            pass

    # ======================================================

    def set_title(self, text):

        self.app.title(

            f"Cloud Dashboard | {text}"

        )

    # ======================================================

    def set_status(

        self,

        text,

        color="#4CAF50"

    ):

        try:

            self.header.state.configure(

                text=text,

                fg_color=color

            )

        except:

            pass

    # ======================================================

    def hide(self):

        self.app.withdraw()

    def show(self):

        self.app.deiconify()

        self.app.lift()

        self.app.focus_force()

    # ======================================================

    def close(self):

        try:

            self.refresh.stop()

        except:

            pass

        self.app.destroy()
