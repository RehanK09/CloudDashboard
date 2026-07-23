"""
dashboard_v4.py
-----------------
Assembles the CloudDashboard V4 window: Header, Drives, Upload Queue,
Live Graph, Statistics, Recent Activity, and the bottom Toolbar.

┌──────────────────────────────────────────────────────────────────┐
│ Cloud Dashboard        ONLINE             ▲ 2.43 MB/s           │
├──────────────┬────────────────────────────┬──────────────────────┤
│ Drives       │ Upload Queue               │ Statistics           │
├──────────────┼────────────────────────────┤                      │
│ Live Graph   │ Recent Activity            │                      │
├──────────────┴────────────────────────────┴──────────────────────┤
│ ▶ Start   ⏸ Pause   ⏹ Stop   🔄 Refresh   📂 Drive   📜 History │
└──────────────────────────────────────────────────────────────────┘

SCOPE NOTE: transfer/upload_panel.py (the dedicated manager meant to
pool TransferCard instances by filename) isn't built yet. Rather than
block this file on that, the upload-queue panel is built inline here
as _UploadQueuePanel — create-on-appear / update-in-place /
destroy-on-disappear, subscribed to STATS_UPDATED. When
transfer/upload_panel.py gets built, lift this class out into that
file verbatim and import it here instead — the logic doesn't need to
change, only its location.
"""

import customtkinter as ctk

from core.events import bus, STATS_UPDATED
from core.refresh import start_refresh
from widgets.header import Header
from widgets.drive_card import DriveCard
from widgets.transfer_card import TransferCard
from widgets.graph import SpeedGraph
from widgets.stats import StatsPanel
from widgets.activity import ActivityList
from widgets.toolbar import Toolbar

WINDOW_SIZE = "1280x760"
WINDOW_MIN_SIZE = (1100, 680)


class _UploadQueuePanel(ctk.CTkScrollableFrame):
    """Stopgap for transfer/upload_panel.py — see module docstring."""

    def __init__(self, master, **kwargs):
        super().__init__(master, label_text="Upload Queue", **kwargs)
        self._cards = {}  # filename -> TransferCard

        self._unsub = bus.subscribe(STATS_UPDATED, self._on_stats)
        self.bind("<Destroy>", self._on_destroy)

    def _on_stats(self, stats):
        current_names = set()
        for transfer in stats["transferring"]:
            name = transfer["name"]
            current_names.add(name)
            card = self._cards.get(name)
            if card is None:
                card = TransferCard(self)
                card.pack(fill="x", padx=6, pady=4)
                self._cards[name] = card
            card.update(transfer)

        for name in list(self._cards):
            if name not in current_names:
                self._cards.pop(name).destroy()

    def _on_destroy(self, _event):
        self._unsub()


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, on_settings=None, **kwargs):
        super().__init__(master, **kwargs)

        self.header = Header(self)
        self.header.pack(fill="x")

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=10, pady=(6, 0))
        body.grid_columnconfigure(0, weight=1, uniform="col")
        body.grid_columnconfigure(1, weight=2, uniform="col")
        body.grid_columnconfigure(2, weight=1, uniform="col")
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        drives_frame = ctk.CTkFrame(body, fg_color="transparent")
        drives_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 6))
        # Single real drive today — see the multi-remote scope note in
        # widgets/drive_card.py for why this isn't several cards yet.
        self.drive_card = DriveCard(drives_frame, name="Cloud Drive")
        self.drive_card.pack(fill="x")

        self.upload_queue = _UploadQueuePanel(body)
        self.upload_queue.grid(row=0, column=1, sticky="nsew", padx=6, pady=(0, 6))

        self.stats_panel = StatsPanel(body)
        self.stats_panel.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(6, 0))

        graph_frame = ctk.CTkFrame(body, fg_color="transparent")
        graph_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=(6, 0))
        self.graph = SpeedGraph(graph_frame)
        self.graph.pack(fill="both", expand=True)

        self.activity_list = ActivityList(body)
        self.activity_list.grid(row=1, column=1, sticky="nsew", padx=6, pady=(6, 0))

        self.toolbar = Toolbar(self, on_settings=on_settings)
        self.toolbar.pack(fill="x", side="bottom")


def build_dashboard(root, on_settings=None):
    """Call from app_v4.py once `root` (the CTk() window) exists.
    Sizes the window, builds the Dashboard, packs it, and starts
    core.refresh's adaptive scheduler. Returns the Dashboard instance."""
    root.geometry(WINDOW_SIZE)
    root.minsize(*WINDOW_MIN_SIZE)

    dashboard = Dashboard(root, on_settings=on_settings)
    dashboard.pack(fill="both", expand=True)

    start_refresh(root)
    return dashboard
