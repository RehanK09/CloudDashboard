"""
widgets/drive_card.py
----------------------
Per-remote storage card: name, progress bar, used/free text, upload
speed, transfer count.

┌─────────────────────────┐
│ Google Drive             │
│ ████████░░               │
│ 68.8 GB free of 70 GB    │
│ ▲ 1.2 MB/s               │
│ 2 transfers              │
└─────────────────────────┘

HONEST SCOPE NOTE: core/api.py (left untouched, per your rule) tracks
exactly ONE remote — whatever's in config.json — with no per-remote
breakdown and no separate download-speed field (see the note in
core/refresh.py; rclone's RC API doesn't tag transfers with a
direction). So this card is built generic and reusable — it takes a
name and listens to the same global STORAGE_UPDATED/STATS_UPDATED
events — but dashboard_v4.py will only ever instantiate ONE of these
for now. Showing several real drives side by side (Google Drive +
OneDrive + Dropbox simultaneously) needs api.py to track stats
per-remote, which is a backend change and out of scope for this pass.
"""

import customtkinter as ctk

from core.events import bus, STORAGE_UPDATED, STATS_UPDATED
from utils import format_size, format_speed


class DriveCard(ctk.CTkFrame):
    def __init__(self, master, name, **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)
        self.name = name

        self._used = 0
        self._total = 0
        self._free = 0

        name_label = ctk.CTkLabel(
            self, text=name, font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        name_label.pack(fill="x", padx=12, pady=(10, 4))

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=12, pady=(0, 6))

        self.free_label = ctk.CTkLabel(
            self, text="-- free of --", font=ctk.CTkFont(size=11),
            anchor="w", text_color="#a0a0a0",
        )
        self.free_label.pack(fill="x", padx=12)

        self.upload_label = ctk.CTkLabel(
            self, text="▲ 0 B/s", font=ctk.CTkFont(size=11),
            anchor="w",
        )
        self.upload_label.pack(fill="x", padx=12, pady=(4, 0))

        self.transfers_label = ctk.CTkLabel(
            self, text="0 transfers", font=ctk.CTkFont(size=11),
            anchor="w", text_color="#a0a0a0",
        )
        self.transfers_label.pack(fill="x", padx=12, pady=(0, 10))

        self._unsubs = [
            bus.subscribe(STORAGE_UPDATED, self._on_storage),
            bus.subscribe(STATS_UPDATED, self._on_stats),
        ]
        self.bind("<Destroy>", self._on_destroy)

    def _on_storage(self, storage):
        self._used = storage["used"]
        self._total = storage["total"]
        self._free = storage["free"]

        fraction = (self._used / self._total) if self._total else 0
        self.progress.set(min(max(fraction, 0), 1))
        self.free_label.configure(
            text=f"{format_size(self._free)} free of {format_size(self._total)}"
        )

    def _on_stats(self, stats):
        self.upload_label.configure(text=f"▲ {format_speed(stats['speed'])}")
        count = len(stats["transferring"])
        self.transfers_label.configure(
            text=f"{count} transfer{'s' if count != 1 else ''}"
        )

    def _on_destroy(self, _event):
        for unsub in self._unsubs:
            unsub()
