import customtkinter as ctk

from formatters import (
    format_speed,
    format_size
)


class StatTile(ctk.CTkFrame):

    def __init__(self, parent, title):

        super().__init__(
            parent,
            corner_radius=12
        )

        self.title = ctk.CTkLabel(

            self,

            text=title,

            font=("Segoe UI",12)

        )

        self.title.pack(
            pady=(8,2)
        )

        self.value = ctk.CTkLabel(

            self,

            text="0",

            font=("Segoe UI Semibold",22)

        )

        self.value.pack(
            pady=(0,8)
        )

    def set(self, value):

        self.value.configure(
            text=value
        )


# =========================================================


class StatsWidget(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.grid_columnconfigure((0,1), weight=1)

        self.title = ctk.CTkLabel(

            self,

            text="Statistics",

            font=("Segoe UI Semibold",18)

        )

        self.title.grid(

            row=0,

            column=0,

            columnspan=2,

            sticky="w",

            padx=15,

            pady=(12,10)

        )

        self.upload = StatTile(
            self,
            "Upload Speed"
        )

        self.download = StatTile(
            self,
            "Download Speed"
        )

        self.transfers = StatTile(
            self,
            "Transfers"
        )

        self.storage = StatTile(
            self,
            "Used Storage"
        )

        self.upload.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.download.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.transfers.grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        self.storage.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="nsew"
        )

    # =====================================================

    def update(

        self,

        stats,

        storage

    ):

        self.upload.set(

            format_speed(

                stats.get(

                    "speed",

                    0

                )

            )

        )

        self.download.set(

            format_speed(

                stats.get(

                    "download_speed",

                    0

                )

            )

        )

        self.transfers.set(

            str(

                len(

                    stats.get(

                        "transferring",

                        []

                    )

                )

            )

        )

        self.storage.set(

            format_size(

                storage.get(

                    "used",

                    0

                )

            )

        )

    def refresh(self):

        pass