"""
widgets/status_badge.py
------------------------
Colored status pill: ONLINE / OFFLINE / UPLOADING / PAUSED.

State priority (highest wins):
1. Not connected to the rclone RC API          -> OFFLINE (red)
2. User has paused (toolbar Pause clicked)      -> PAUSED (amber)
3. Anything actively transferring right now     -> UPLOADING (blue)
4. Otherwise                                    -> ONLINE (green)

"Paused" isn't backend state — api.py has no concept of it (pausing
is a core/bwlimit throttle, not a real stop). widgets/toolbar.py
publishes PAUSE_STATE_CHANGED when its Pause/Start buttons are
clicked; this widget just listens for it. Never imports core.api
directly — only core.events.
"""

import customtkinter as ctk

from core.events import bus, STATS_UPDATED, CONNECTION_CHANGED, PAUSE_STATE_CHANGED

_COLORS = {
    "ONLINE": ("#1b3a2c", "#2ecc71"),
    "OFFLINE": ("#3a1b1b", "#e74c3c"),
    "UPLOADING": ("#1b2a3a", "#3498db"),
    "PAUSED": ("#3a331b", "#f39c12"),
}


class StatusBadge(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self._connected = False
        self._uploading = False
        self._paused = False

        self.label = ctk.CTkLabel(
            self, text="OFFLINE",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=10, width=90, height=24,
        )
        self.label.pack()

        self._unsubs = [
            bus.subscribe(STATS_UPDATED, self._on_stats),
            bus.subscribe(CONNECTION_CHANGED, self._on_connection),
            bus.subscribe(PAUSE_STATE_CHANGED, self._on_pause),
        ]
        self.bind("<Destroy>", self._on_destroy)
        self._render()

    def _on_stats(self, stats):
        self._uploading = bool(stats["transferring"])
        self._render()

    def _on_connection(self, connected):
        self._connected = connected
        self._render()

    def _on_pause(self, paused):
        self._paused = paused
        self._render()

    def _render(self):
        if not self._connected:
            state = "OFFLINE"
        elif self._paused:
            state = "PAUSED"
        elif self._uploading:
            state = "UPLOADING"
        else:
            state = "ONLINE"

        bg, fg = _COLORS[state]
        self.label.configure(text=state, fg_color=bg, text_color=fg)

    def _on_destroy(self, _event):
        for unsub in self._unsubs:
            unsub()
