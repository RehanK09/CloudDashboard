import customtkinter as ctk

from utils import (
    format_speed,
    format_size
)


class StatusCard:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="x",
            padx=10
        )

        self.status = ctk.CTkLabel(
            self.frame,
            text="🔴 Waiting for rclone...",
            font=("Segoe UI", 20, "bold")
        )

        self.status.pack(
            anchor="w",
            padx=20,
            pady=(12,4)
        )

        self.speed = ctk.CTkLabel(
            self.frame,
            text="Speed : --"
        )

        self.speed.pack(
            anchor="w",
            padx=20
        )

        self.uploaded = ctk.CTkLabel(
            self.frame,
            text="Uploaded : --"
        )

        self.uploaded.pack(
            anchor="w",
            padx=20
        )

        self.transfers = ctk.CTkLabel(
            self.frame,
            text="Transfers : --"
        )

        self.transfers.pack(
            anchor="w",
            padx=20
        )

        self.errors = ctk.CTkLabel(
            self.frame,
            text="Errors : --"
        )

        self.errors.pack(
            anchor="w",
            padx=20
        )

        self.current_file = ctk.CTkLabel(
            self.frame,
            text="Current File : Idle"
        )

        self.current_file.pack(
            anchor="w",
            padx=20
        )

        self.eta = ctk.CTkLabel(
            self.frame,
            text="ETA : --"
        )

        self.eta.pack(
            anchor="w",
            padx=20,
            pady=(0,12)
        )

    def update(self, stats, transfer):

        if stats.get("connected"):

            self.status.configure(
                text="🟢 Connected"
            )

        else:

            self.status.configure(
                text="🔴 Waiting for rclone..."
            )

        self.speed.configure(
            text=f"Speed : {format_speed(stats.get('speed',0))}"
        )

        self.uploaded.configure(
            text=f"Uploaded : {format_size(stats.get('bytes',0))}"
        )

        self.transfers.configure(
            text=f"Transfers : {len(stats.get('transferring',[]))}"
        )

        self.errors.configure(
            text=f"Errors : {stats.get('errors',0)}"
        )

        if transfer:

            self.current_file.configure(
                text=f"Current File : {transfer['name']}"
            )

            eta = transfer.get("eta")

            if eta is None:

                eta = "--"

            self.eta.configure(
                text=f"ETA : {eta}"
            )

        else:

            self.current_file.configure(
                text="Current File : Idle"
            )

            self.eta.configure(
                text="ETA : --"
            )