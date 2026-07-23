import customtkinter as ctk

from api import rclone_api


class Controls:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=15
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        ctk.CTkLabel(

            self.frame,

            text="⚡ Quick Actions",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=20,
            pady=(18,15)
        )

        self.grid = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.grid.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )

        self.grid.grid_columnconfigure((0,1), weight=1)
        self.grid.grid_rowconfigure((0,1), weight=1)

        self.pause_btn = ctk.CTkButton(

            self.grid,

            text="⏸\nPause",

            height=90,

            font=("Segoe UI",15),

            corner_radius=15,

            command=self.pause

        )

        self.pause_btn.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=6,
            pady=6
        )

        self.resume_btn = ctk.CTkButton(

            self.grid,

            text="▶\nResume",

            height=90,

            font=("Segoe UI",15),

            corner_radius=15,

            command=self.resume

        )

        self.resume_btn.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=6,
            pady=6
        )

        self.refresh_btn = ctk.CTkButton(

            self.grid,

            text="🔄\nRefresh",

            height=90,

            font=("Segoe UI",15),

            corner_radius=15,

            command=self.refresh

        )

        self.refresh_btn.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=6,
            pady=6
        )

        self.stop_btn = ctk.CTkButton(

            self.grid,

            text="⏹\nStop",

            height=90,

            font=("Segoe UI",15),

            corner_radius=15,

            fg_color="#C62828",

            hover_color="#8E0000",

            command=self.stop

        )

        self.stop_btn.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=6,
            pady=6
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