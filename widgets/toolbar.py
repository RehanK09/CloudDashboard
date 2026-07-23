"""
widgets/toolbar.py
--------------------
Bottom action bar: Start, Pause, Stop, Refresh, Open Drive, History,
Settings — equal-width buttons, single row.

This is where real control happens, not just UI:
- Start/Pause call core.api's resume_uploads()/pause_uploads() (a
  core/bwlimit throttle — see the caveat next to PAUSE_STATE_CHANGED
  in core/events.py) and publish PAUSE_STATE_CHANGED so
  widgets/status_badge.py can show PAUSED without api.py changing.
- Stop calls rclone_api.stop_all(), which lists real running rclone
  jobs and stops each one (the original jobid=-1 in an earlier draft
  wasn't a valid rclone jobid — fixed in core/api.py already).
- Refresh re-publishes whatever's already cached instantly, instead of
  waiting for the next core/refresh.py tick.
- Open Drive shells out to Explorer on the configured drive letter.
- History opens the singleton history.py window.
- Settings takes an `on_settings` callback: settings.py doesn't have a
  singleton-window entry point built yet in this pass, so rather than
  guess at an interface that isn't built, the button stays present but
  disabled until you wire one in.
"""

import subprocess

import customtkinter as ctk

from core.api import rclone_api
from core.events import bus, PAUSE_STATE_CHANGED, STATS_UPDATED, STORAGE_UPDATED
from history import open_history_window


class Toolbar(ctk.CTkFrame):
    def __init__(self, master, on_settings=None, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self._paused = False
        self._on_settings = on_settings
        self.buttons = {}

        button_defs = [
            ("▶ Start", self._on_start),
            ("⏸ Pause", self._on_pause),
            ("⏹ Stop", self._on_stop),
            ("🔄 Refresh", self._on_refresh),
            ("📂 Open Drive", self._on_open_drive),
            ("📜 History", self._on_history),
            ("⚙ Settings", self._on_settings_click),
        ]

        for text, handler in button_defs:
            btn = ctk.CTkButton(self, text=text, command=handler, height=32)
            btn.pack(side="left", expand=True, fill="x", padx=4, pady=6)
            self.buttons[text] = btn

        if self._on_settings is None:
            self.buttons["⚙ Settings"].configure(state="disabled")

    def _on_start(self):
        rclone_api.resume_uploads()
        self._paused = False
        bus.publish(PAUSE_STATE_CHANGED, False)

    def _on_pause(self):
        rclone_api.pause_uploads()
        self._paused = True
        bus.publish(PAUSE_STATE_CHANGED, True)

    def _on_stop(self):
        rclone_api.stop_all()

    def _on_refresh(self):
        bus.publish(STATS_UPDATED, rclone_api.get_stats())
        bus.publish(STORAGE_UPDATED, rclone_api.get_storage())

    def _on_open_drive(self):
        drive = rclone_api.drive
        if not drive:
            return
        path = drive if drive.endswith("\\") else drive + "\\"
        try:
            subprocess.Popen(["explorer", path])
        except Exception:
            pass

    def _on_history(self):
        open_history_window(self)

    def _on_settings_click(self):
        if self._on_settings:
            self._on_settings()
