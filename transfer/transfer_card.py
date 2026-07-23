import customtkinter as ctk

from formatters import (
    shorten_filename,
    format_speed,
    format_eta,
    format_percentage
)


class TransferCard(ctk.CTkFrame):

    STATUS_COLORS = {

        "waiting": "#757575",

        "uploading": "#1976D2",

        "downloading": "#2E7D32",

        "paused": "#F9A825",

        "completed": "#43A047",

        "failed": "#E53935"

    }

    def __init__(self, parent, transfer):

        super().__init__(

            parent,

            corner_radius=12

        )

        self.transfer = transfer

        # ---------------------------------

        top = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        top.pack(

            fill="x",

            padx=12,

            pady=(10,4)

        )

        self.filename = ctk.CTkLabel(

            top,

            text="",

            font=("Segoe UI Semibold",14),

            anchor="w"

        )

        self.filename.pack(

            side="left",

            fill="x",

            expand=True

        )

        self.status = ctk.CTkLabel(

            top,

            text="WAITING",

            width=95,

            height=26,

            corner_radius=13,

            font=("Segoe UI",11,"bold")

        )

        self.status.pack(

            side="right"

        )

        # ---------------------------------

        self.bar = ctk.CTkProgressBar(

            self,

            height=12,

            corner_radius=8

        )

        self.bar.pack(

            fill="x",

            padx=12,

            pady=6

        )

        self.bar.set(0)

        # ---------------------------------

        bottom = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        bottom.pack(

            fill="x",

            padx=12,

            pady=(2,10)

        )

        self.left = ctk.CTkLabel(

            bottom,

            text="",

            font=("Segoe UI",12),

            anchor="w"

        )

        self.left.pack(

            side="left"

        )

        self.right = ctk.CTkLabel(

            bottom,

            text="",

            font=("Segoe UI",12),

            anchor="e"

        )

        self.right.pack(

            side="right"

        )

        self.refresh()

    # ====================================================

    def refresh(self):

        t = self.transfer

        self.filename.configure(

            text=shorten_filename(

                t.name,

                40

            )

        )

        self.bar.set(

            t.progress / 100

        )

        state = t.status.lower()

        self.status.configure(

            text=state.upper(),

            fg_color=self.STATUS_COLORS.get(

                state,

                "#616161"

            )

        )

        self.left.configure(

            text=(

                f"{format_speed(t.speed)}"

                "   •   "

                f"{format_eta(t.eta)}"

            )

        )

        self.right.configure(

            text=format_percentage(

                t.progress

            )

        )