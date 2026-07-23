import customtkinter as ctk

from formatters import format_speed, format_size


class StatusCard:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=15
        )

        self.frame.pack(
            fill="x",
            padx=15,
            pady=(0,10)
        )

        # ---------------- TOP ----------------

        self.top = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.top.pack(
            fill="x",
            padx=20,
            pady=(18,12)
        )

        self.status = ctk.CTkLabel(

            self.top,

            text="🔴 Waiting for rclone...",

            font=("Segoe UI Semibold",22)

        )

        self.status.pack(
            side="left"
        )

        self.badge = ctk.CTkLabel(

            self.top,

            text="OFFLINE",

            width=95,

            height=32,

            corner_radius=16,

            fg_color="#b71c1c",

            font=("Segoe UI",13,"bold")

        )

        self.badge.pack(
            side="right"
        )

        # ---------------- GRID ----------------

        self.grid = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        self.grid.pack(
            fill="x",
            padx=20,
            pady=(0,18)
        )

        self.cards = []

        names = [

            "Upload Speed",
            "Uploaded",
            "Transfers",
            "Errors"

        ]

        for i, name in enumerate(names):

            card = ctk.CTkFrame(
                self.grid,
                corner_radius=12
            )

            card.grid(
                row=0,
                column=i,
                padx=6,
                sticky="nsew"
            )

            self.grid.grid_columnconfigure(
                i,
                weight=1
            )

            title = ctk.CTkLabel(

                card,

                text=name,

                font=("Segoe UI",12),

                text_color="gray70"

            )

            title.pack(
                pady=(12,4)
            )

            value = ctk.CTkLabel(

                card,

                text="--",

                font=("Segoe UI Semibold",20)

            )

            value.pack(
                pady=(0,12)
            )

            self.cards.append(value)

        # ---------------- CURRENT ----------------

        self.bottom = ctk.CTkFrame(
            self.frame,
            corner_radius=12
        )

        self.bottom.pack(
            fill="x",
            padx=20,
            pady=(0,18)
        )

        self.current_file = ctk.CTkLabel(

            self.bottom,

            text="No active transfer",

            font=("Segoe UI",15)

        )

        self.current_file.pack(
            anchor="w",
            padx=15,
            pady=(12,4)
        )

        self.eta = ctk.CTkLabel(

            self.bottom,

            text="ETA : --",

            font=("Segoe UI",13),

            text_color="gray70"

        )

        self.eta.pack(
            anchor="w",
            padx=15,
            pady=(0,12)
        )

    def update(self, stats, transfer):

        connected = stats.get("connected", False)

        if connected:

            self.status.configure(
                text="🟢 Connected"
            )

            self.badge.configure(
                text="ONLINE",
                fg_color="#2e7d32"
            )

        else:

            self.status.configure(
                text="🔴 Waiting for rclone..."
            )

            self.badge.configure(
                text="OFFLINE",
                fg_color="#b71c1c"
            )

        self.cards[0].configure(
            text=format_speed(
                stats.get("speed",0)
            )
        )

        self.cards[1].configure(
            text=format_size(
                stats.get("bytes",0)
            )
        )

        self.cards[2].configure(
            text=str(
                len(stats.get("transferring",[]))
            )
        )

        self.cards[3].configure(
            text=str(
                stats.get("errors",0)
            )
        )

        if transfer:

            self.current_file.configure(
                text=transfer.get(
                    "name",
                    "Unknown"
                )
            )

            eta = transfer.get("eta")

            if eta is None:

                eta = "--"

            self.eta.configure(
                text=f"ETA : {eta}"
            )

        else:

            self.current_file.configure(
                text="No active transfer"
            )

            self.eta.configure(
                text="ETA : --"
            )