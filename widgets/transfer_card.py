"""
widgets/transfer_card.py
--------------------------
One card in the upload queue: filename, progress bar, percentage,
current speed, ETA, transferred/total.

┌───────────────────────────────────────────┐
│ movie.mkv                                  │
│ █████████░░░░░░░░░░░  42%                  │
│ 2.1 GB / 5.0 GB   18.2 MB/s      ETA 2m 15s │
└───────────────────────────────────────────┘

This card is a dumb, reusable component — it does NOT subscribe to
core.events itself. With N simultaneous transfers each needing its own
card, deciding which filename maps to which card is a job for a
manager (transfer/upload_panel.py, not built yet), not something one
card should guess at from the global STATS_UPDATED payload. Call
.update(transfer_dict) with one entry from
rclone_api.get_stats()["transferring"] whenever it changes.
"""

import customtkinter as ctk

from utils import format_size, format_speed


def _format_eta(seconds):
    """rclone gives raw seconds (or None/negative when unknown) — this
    is the fix for 'ETA shows 157824983 instead of 2m 15s'."""
    if seconds is None or seconds < 0:
        return "--"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m"


class TransferCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)
        self.filename = None

        self.name_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
        )
        self.name_label.pack(fill="x", padx=12, pady=(8, 2))

        progress_row = ctk.CTkFrame(self, fg_color="transparent")
        progress_row.pack(fill="x", padx=12)

        self.progress = ctk.CTkProgressBar(progress_row)
        self.progress.set(0)
        self.progress.pack(side="left", fill="x", expand=True)

        self.percent_label = ctk.CTkLabel(
            progress_row, text="0%", font=ctk.CTkFont(size=11), width=40,
        )
        self.percent_label.pack(side="left", padx=(8, 0))

        detail_row = ctk.CTkFrame(self, fg_color="transparent")
        detail_row.pack(fill="x", padx=12, pady=(2, 8))

        self.size_label = ctk.CTkLabel(
            detail_row, text="0 B / 0 B", font=ctk.CTkFont(size=11),
            text_color="#a0a0a0",
        )
        self.size_label.pack(side="left")

        self.speed_label = ctk.CTkLabel(
            detail_row, text="0 B/s", font=ctk.CTkFont(size=11),
            text_color="#a0a0a0",
        )
        self.speed_label.pack(side="left", padx=(12, 0))

        self.eta_label = ctk.CTkLabel(
            detail_row, text="ETA --", font=ctk.CTkFont(size=11),
            text_color="#a0a0a0",
        )
        self.eta_label.pack(side="right")

    def update(self, transfer):
        """transfer: one dict from rclone_api.get_stats()['transferring'],
        e.g. {'name','size','bytes','percentage','speed','eta'}."""
        self.filename = transfer["name"]
        pct = transfer.get("percentage", 0) or 0

        self.name_label.configure(text=transfer["name"])
        self.progress.set(min(max(pct / 100, 0), 1))
        self.percent_label.configure(text=f"{int(pct)}%")
        self.size_label.configure(
            text=f"{format_size(transfer.get('bytes', 0))} / "
                 f"{format_size(transfer.get('size', 0))}"
        )
        self.speed_label.configure(text=format_speed(transfer.get("speed", 0)))
        self.eta_label.configure(text=f"ETA {_format_eta(transfer.get('eta'))}")
