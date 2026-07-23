import customtkinter as ctk

from utils import open_drive


class Header:

    def __init__(
        self,
        parent,
        window_manager,
        drive_letter
    ):

        self.window_manager = window_manager
        self.drive_letter = drive_letter

        self.frame = ctk.CTkFrame(
            parent,
            height=60
        )

        self.frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.title = ctk.CTkLabel(
            self.frame,
            text="☁ Cloud Dashboard",
            font=("Segoe UI", 26, "bold")
        )

        self.title.pack(
            side="left",
            padx=20
        )

        self.theme_btn = ctk.CTkButton(
            self.frame,
            text="Theme",
            width=110,
            command=self.change_theme
        )

        self.theme_btn.pack(
            side="right",
            padx=8
        )

        self.drive_btn = ctk.CTkButton(
            self.frame,
            text="Open Drive",
            width=110,
            command=lambda: open_drive(self.drive_letter)
        )

        self.drive_btn.pack(
            side="right",
            padx=8
        )

        self.settings_btn = ctk.CTkButton(
            self.frame,
            text="Settings",
            width=110,
            command=self.window_manager.open_settings
        )

        self.settings_btn.pack(
            side="right",
            padx=8
        )

        self.history_btn = ctk.CTkButton(
            self.frame,
            text="History",
            width=110,
            command=self.window_manager.open_history
        )

        self.history_btn.pack(
            side="right",
            padx=8
        )

    def change_theme(self):

        # Placeholder for future theme manager
        pass