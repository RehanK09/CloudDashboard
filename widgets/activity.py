import customtkinter as ctk

from history import history_tracker


class ActivityWidget(ctk.CTkFrame):

    MAX_ITEMS = 150

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.title = ctk.CTkLabel(

            self,

            text="Recent Activity",

            font=("Segoe UI Semibold",18)

        )

        self.title.pack(

            anchor="w",

            padx=15,

            pady=(12,8)

        )

        self.list = ctk.CTkScrollableFrame(

            self,

            fg_color="transparent"

        )

        self.list.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0,10)

        )

        self.rows = []

        self.refresh()

    # ====================================================

    def _badge_color(self, status):

        status = status.lower()

        colors = {

            "completed": "#43A047",

            "uploading": "#1976D2",

            "downloading": "#2E7D32",

            "paused": "#F9A825",

            "failed": "#D32F2F",

            "deleted": "#8E24AA"

        }

        return colors.get(

            status,

            "#616161"

        )

    # ====================================================

    def refresh(self):

        for row in self.rows:

            row.destroy()

        self.rows.clear()

        try:

            history = list(

                reversed(

                    history_tracker.history[-self.MAX_ITEMS:]

                )

            )

        except Exception:

            history = []

        if not history:

            lbl = ctk.CTkLabel(

                self.list,

                text="No Recent Activity",

                font=("Segoe UI",16),

                text_color="gray70"

            )

            lbl.pack(

                pady=20

            )

            self.rows.append(lbl)

            return

        for item in history:

            frame = ctk.CTkFrame(

                self.list,

                corner_radius=10

            )

            frame.pack(

                fill="x",

                padx=4,

                pady=4

            )

            left = ctk.CTkFrame(

                frame,

                fg_color="transparent"

            )

            left.pack(

                side="left",

                fill="x",

                expand=True,

                padx=10,

                pady=8

            )

            name = ctk.CTkLabel(

                left,

                text=item.get(

                    "name",

                    "Unknown File"

                ),

                anchor="w",

                font=("Segoe UI",15)

            )

            name.pack(

                anchor="w"

            )

            detail = ctk.CTkLabel(

                left,

                text=item.get(

                    "time",

                    ""

                ),

                anchor="w",

                font=("Segoe UI",12),

                text_color="gray70"

            )

            detail.pack(

                anchor="w"

            )

            badge = ctk.CTkLabel(

                frame,

                text=item.get(

                    "status",

                    "DONE"

                ).upper(),

                width=95,

                height=28,

                corner_radius=14,

                fg_color=self._badge_color(

                    item.get(

                        "status",

                        ""

                    )

                ),

                font=("Segoe UI",11,"bold")

            )

            badge.pack(

                side="right",

                padx=10

            )

            self.rows.append(frame)

    # ====================================================

    def update(self):

        self.refresh()