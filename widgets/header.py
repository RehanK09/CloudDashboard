"""
widgets/header.py
------------------
Top bar: title, status pill, live speed.

┌──────────────────────────────────────────────────────────────────┐
│ Cloud Dashboard        ONLINE             ▲ 2.43 MB/s           │
└──────────────────────────────────────────────────────────────────┘

Fixed ~55px height per the v4 spec (pack_propagate(False) so child
widgets can't stretch it taller). Only subscribes to core.events —
never touches core.api directly.
"""

import customtkinter as ctk

from core.events import bus, STATS_UPDATED
from widgets.status_badge import StatusBadge
from utils import format_speed


class Header(ctk.CTkFrame):
    HEIGHT = 55

    def __init__(self, master, **kwargs):
        super().__init__(master, height=self.HEIGHT, corner_radius=0, **kwargs)
        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self, text="Cloud Dashboard",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title.pack(side="left", padx=16)

        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="right", padx=16)

        self.speed_label = ctk.CTkLabel(
            right, text="▲ 0 B/s",
            font=ctk.CTkFont(size=13),
        )
        self.speed_label.pack(side="right", padx=(10, 0))

        self.badge = StatusBadge(right)
        self.badge.pack(side="right")

        self._unsub = bus.subscribe(STATS_UPDATED, self._on_stats)
        self.bind("<Destroy>", self._on_destroy)

    def _on_stats(self, stats):
        self.speed_label.configure(text=f"▲ {format_speed(stats['speed'])}")

    def _on_destroy(self, _event):
        self._unsub()
