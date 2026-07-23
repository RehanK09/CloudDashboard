import customtkinter as ctk

from utils import open_drive


class Header:

    def __init__(self, parent, window_manager, drive_letter):

        self.window_manager = window_manager
        self.drive_letter = drive_letter

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            height=70
        )

        self.frame.pack(
            fill="x",
            padx=15,
            pady=(15,10)
        )

        self.left = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.left.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.title = ctk.CTkLabel(

            self.left,

            text="☁ Cloud Dashboard",

            font=("Segoe UI Semibold",28)

        )

        self.title.pack(anchor="w")

        self.subtitle = ctk.CTkLabel(

            self.left,

            text="Monitor your cloud in real time",

            font=("Segoe UI",13),

            text_color="gray70"

        )

        self.subtitle.pack(anchor="w")

        self.right = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.right.pack(
            side="right",
            padx=20
        )

        self.history_btn = ctk.CTkButton(

            self.right,

            text="📜 History",

            width=115,

            height=40,

            corner_radius=12,

            font=("Segoe UI",14)

        )

        self.history_btn.pack(
            side="left",
            padx=5
        )

        self.settings_btn = ctk.CTkButton(

            self.right,

            text="⚙ Settings",

            width=115,

            height=40,

            corner_radius=12,

            font=("Segoe UI",14)

        )

        self.settings_btn.pack(
            side="left",
            padx=5
        )

        self.drive_btn = ctk.CTkButton(

            self.right,

            text="📂 Open Drive",

            width=135,

            height=40,

            corner_radius=12,

            font=("Segoe UI",14),

            command=lambda: open_drive(self.drive_letter)

        )

        self.drive_btn.pack(
            side="left",
            padx=5
        )