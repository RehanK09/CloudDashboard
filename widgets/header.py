import customtkinter as ctk

from core.status import status


class Header(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=70,
            corner_radius=15
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # --------------------------------------------------

        self.title = ctk.CTkLabel(

            self,

            text="CloudDashboard",

            font=("Segoe UI Semibold",26),

            anchor="w"

        )

        self.title.grid(

            row=0,

            column=0,

            padx=20,

            pady=18,

            sticky="w"

        )

        # --------------------------------------------------

        self.state = ctk.CTkLabel(

            self,

            text="OFFLINE",

            width=120,

            height=34,

            corner_radius=17,

            fg_color="#C62828",

            font=("Segoe UI",13,"bold")

        )

        self.state.grid(

            row=0,

            column=1,

            padx=(0,10)

        )

        # --------------------------------------------------

        self.speed = ctk.CTkLabel(

            self,

            text="▲ 0 B/s",

            font=("Segoe UI",13)

        )

        self.speed.grid(

            row=0,

            column=2,

            padx=(0,20)

        )

    # =====================================================

    def refresh(

        self,

        stats=None

    ):

        self.state.configure(

            text=status.text,

            fg_color=status.color

        )

        if stats:

            speed = stats.get(

                "speed",

                0

            )

            units = [

                "B/s",

                "KB/s",

                "MB/s",

                "GB/s"

            ]

            value = float(speed)

            for unit in units:

                if value < 1024:

                    break

                value /= 1024

            self.speed.configure(

                text=f"▲ {value:.1f} {unit}"

            )

        else:

            self.speed.configure(

                text="▲ 0 B/s"

            )