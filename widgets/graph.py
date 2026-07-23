"""
widgets/graph.py
------------------
Live upload-speed graph, Task-Manager style: grid background, smooth
line, 60-second rolling history. Built on a plain tkinter.Canvas — no
matplotlib, so nothing here can block the GUI thread.

HONEST SCOPE NOTE: your mockup shows two lines (upload + download).
rclone's RC API doesn't tag transfers with a direction (see the note
in core/refresh.py and widgets/drive_card.py) — core/api.py's `speed`
field is one aggregate number. So this graph draws ONE real line. A
second "download" line would have to be fabricated data, which is
worse than not showing it. If per-direction tracking gets added to
api.py later, this widget already accepts a second series — see
`add_series()`.

Samples once per second regardless of how fast core/refresh.py is
ticking (100ms while uploading would otherwise flood the graph with
noise) — gated locally by wall-clock time, not by tick count.
"""

import time
import tkinter as tk
from collections import deque

import customtkinter as ctk

from core.events import bus, STATS_UPDATED

HISTORY_SECONDS = 60


class SpeedGraph(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)

        self._series = {
            "upload": {"samples": deque([0.0] * HISTORY_SECONDS, maxlen=HISTORY_SECONDS),
                       "color": "#3498db"},
        }
        self._last_sample_time = 0.0

        self.canvas = tk.Canvas(self, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas.bind("<Configure>", lambda _e: self._redraw())

        self._unsub = bus.subscribe(STATS_UPDATED, self._on_stats)
        self.bind("<Destroy>", self._on_destroy)

    def add_series(self, key, color):
        """Call this if a future backend change exposes a second speed
        source (e.g. real download speed). Not used today."""
        self._series[key] = {
            "samples": deque([0.0] * HISTORY_SECONDS, maxlen=HISTORY_SECONDS),
            "color": color,
        }

    def _on_stats(self, stats):
        now = time.time()
        if now - self._last_sample_time < 1.0:
            return
        self._last_sample_time = now
        self._series["upload"]["samples"].append(stats["speed"])
        self._redraw()

    def _redraw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return

        # grid — 3 horizontal divider lines
        for i in range(1, 4):
            y = h * i / 4
            self.canvas.create_line(0, y, w, y, fill="#2a2a2a")

        all_samples = [s for series in self._series.values() for s in series["samples"]]
        max_speed = max(max(all_samples, default=0), 1)

        for series in self._series.values():
            samples = series["samples"]
            n = len(samples)
            step = w / (n - 1) if n > 1 else w
            points = []
            for i, sample in enumerate(samples):
                x = i * step
                y = h - (sample / max_speed) * (h - 10) - 5
                points.extend([x, y])
            if len(points) >= 4:
                self.canvas.create_line(*points, fill=series["color"], width=2, smooth=True)

    def _on_destroy(self, _event):
        self._unsub()
