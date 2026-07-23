import customtkinter as ctk

from api import rclone_api


class Controls:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.pause_btn = ctk.CTkButton(
            self.frame,
            text="Pause",
            width=120,
            command=self.pause
        )

        self.pause_btn.pack(
            side="left",
            padx=8,
            pady=10
        )

        self.resume_btn = ctk.CTkButton(
            self.frame,
            text="Resume",
            width=120,
            command=self.resume
        )

        self.resume_btn.pack(
            side="left",
            padx=8
        )

        self.stop_btn = ctk.CTkButton(
            self.frame,
            text="Stop",
            width=120,
            fg_color="#c62828",
            hover_color="#8e0000",
            command=self.stop
        )

        self.stop_btn.pack(
            side="left",
            padx=8
        )

        self.refresh_btn = ctk.CTkButton(
            self.frame,
            text="Refresh",
            width=120,
            command=self.refresh
        )

        self.refresh_btn.pack(
            side="right",
            padx=8
        )

        self.refresh_callback = None

    def pause(self):

        rclone_api.pause_uploads()

    def resume(self):

        rclone_api.resume_uploads()

    def stop(self):

        rclone_api.stop_all()

    def refresh(self):

        if self.refresh_callback:
            self.refresh_callback()

    def set_refresh_callback(self, callback):

        self.refresh_callback = callback