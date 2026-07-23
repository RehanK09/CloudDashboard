"""
widgets/activity.py
---------------------
Recent Activity: compact list, newest first — Time, Filename, Status,
Speed, Transferred.

Reads real data from history.py, which is itself fed by real per-file
transfer lifecycles in core/api.py's transferring[] (see history.py's
own docstring for the FAILED-detection caveat). Rather than re-read
history.json on a timer, this widget subscribes to
core.events.HISTORY_UPDATED, which history.py publishes the instant it
writes a finished transfer — so it shows up here immediately, not on
the next poll.
"""

import customtkinter as ctk

from core.events import bus, HISTORY_UPDATED
from history import load_history

MAX_ROWS = 50


class ActivityRow(ctk.CTkFrame):
    def __init__(self, master, entry, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        color = "#2ecc71" if entry.get("status") == "SUCCESS" else "#e74c3c"

        ctk.CTkLabel(
            self, text=entry.get("time", ""), width=70,
            font=ctk.CTkFont(size=11), text_color="#a0a0a0", anchor="w",
        ).pack(side="left", padx=(6, 4))

        ctk.CTkLabel(
            self, text=entry.get("filename", ""), font=ctk.CTkFont(size=11),
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=4)

        ctk.CTkLabel(
            self, text=entry.get("speed", ""), width=90,
            font=ctk.CTkFont(size=11), text_color="#a0a0a0", anchor="e",
        ).pack(side="left", padx=4)

        ctk.CTkLabel(
            self, text=entry.get("size", ""), width=80,
            font=ctk.CTkFont(size=11), text_color="#a0a0a0", anchor="e",
        ).pack(side="left", padx=4)

        ctk.CTkLabel(
            self, text=entry.get("status", ""), width=70,
            font=ctk.CTkFont(size=11, weight="bold"), text_color=color, anchor="e",
        ).pack(side="left", padx=(4, 6))


class ActivityList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, label_text="Recent Activity", **kwargs)

        self._entries = load_history(limit=MAX_ROWS)
        self._rows = []
        self._render()

        self._unsub = bus.subscribe(HISTORY_UPDATED, self._on_new_entry)
        self.bind("<Destroy>", self._on_destroy)

    def _on_new_entry(self, entry):
        self._entries.insert(0, entry)
        self._entries = self._entries[:MAX_ROWS]
        self._render()

    def _render(self):
        for row in self._rows:
            row.destroy()
        self._rows = []
        for entry in self._entries:
            row = ActivityRow(self, entry)
            row.pack(fill="x", pady=1)
            self._rows.append(row)

    def _on_destroy(self, _event):
        self._unsub()
