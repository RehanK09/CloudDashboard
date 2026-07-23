"""
widgets/stats.py
------------------
Compact stat tiles: Upload Speed, Download Speed, Average Speed, Peak
Speed, Transfers, Used Storage, Free Storage, Errors. No giant cards —
each tile is a small labeled box in a grid.

HONEST SCOPE NOTE: "Download Speed" is in the mockup, but core/api.py
has no way to measure it — rclone's RC API doesn't split transfer
direction (same limitation noted in widgets/graph.py and
widgets/drive_card.py). Rather than fabricate a number, that tile
always shows "N/A" with a comment explaining why, instead of quietly
disappearing or lying with a fake 0.

Average and Peak Speed ARE real, computed here from the live
STATS_UPDATED stream (session-lifetime running average / max) — that's
UI-side aggregation, not a backend change, so it's fair game.
"""

import customtkinter as ctk

from core.events import bus, STATS_UPDATED, STORAGE_UPDATED
from utils import format_size, format_speed


class StatTile(ctk.CTkFrame):
    def __init__(self, master, label, **kwargs):
        super().__init__(master, corner_radius=8, **kwargs)
        self.value_label = ctk.CTkLabel(
            self, text="--", font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.value_label.pack(padx=10, pady=(8, 0))
        ctk.CTkLabel(
            self, text=label, font=ctk.CTkFont(size=10),
            text_color="#a0a0a0",
        ).pack(padx=10, pady=(0, 8))

    def set_value(self, text):
        self.value_label.configure(text=text)


class StatsPanel(ctk.CTkFrame):
    LABELS = [
        "Upload Speed", "Download Speed", "Average Speed", "Peak Speed",
        "Transfers", "Used Storage", "Free Storage", "Errors",
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._speed_sum = 0.0
        self._speed_samples = 0
        self._peak_speed = 0.0

        self.tiles = {}
        for i, label in enumerate(self.LABELS):
            tile = StatTile(self, label)
            tile.grid(row=i // 2, column=i % 2, padx=4, pady=4, sticky="nsew")
            self.tiles[label] = tile
        self.tiles["Download Speed"].set_value("N/A")

        self._unsubs = [
            bus.subscribe(STATS_UPDATED, self._on_stats),
            bus.subscribe(STORAGE_UPDATED, self._on_storage),
        ]
        self.bind("<Destroy>", self._on_destroy)

    def _on_stats(self, stats):
        speed = stats["speed"]
        self.tiles["Upload Speed"].set_value(format_speed(speed))

        if speed > 0:
            self._speed_sum += speed
            self._speed_samples += 1
        if speed > self._peak_speed:
            self._peak_speed = speed

        avg = (self._speed_sum / self._speed_samples) if self._speed_samples else 0
        self.tiles["Average Speed"].set_value(format_speed(avg))
        self.tiles["Peak Speed"].set_value(format_speed(self._peak_speed))
        self.tiles["Transfers"].set_value(str(len(stats["transferring"])))
        self.tiles["Errors"].set_value(str(stats["errors"]))

    def _on_storage(self, storage):
        self.tiles["Used Storage"].set_value(format_size(storage["used"]))
        self.tiles["Free Storage"].set_value(format_size(storage["free"]))

    def _on_destroy(self, _event):
        for unsub in self._unsubs:
            unsub()
