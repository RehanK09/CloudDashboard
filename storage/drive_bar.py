import customtkinter as ctk

from formatters import format_size, format_speed


class DriveBar(ctk.CTkFrame):

    def __init__(self, parent, drive):

        super().__init__(
            parent,
            corner_radius=12
        )

        self.drive = drive

        # =====================================================

        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=12,
            pady=(10,4)
        )

        self.name = ctk.CTkLabel(
            top,
            text="",
            font=("Segoe UI Semibold",16),
            anchor="w"
        )

        self.name.pack(
            side="left"
        )

        self.status = ctk.CTkLabel(
            top,
            text="OFFLINE",
            width=90,
            height=26,
            corner_radius=13,
            font=("Segoe UI",11,"bold")
        )

        self.status.pack(
            side="right"
        )

        # =====================================================

        self.progress = ctk.CTkProgressBar(
            self,
            height=12
        )

        self.progress.pack(
            fill="x",
            padx=12,
            pady=6
        )

        self.progress.set(0)

        # =====================================================

        self.storage = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            font=("Segoe UI",12)
        )

        self.storage.pack(
            fill="x",
            padx=12
        )

        self.speed = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            font=("Segoe UI",12)
        )

        self.speed.pack(
            fill="x",
            padx=12,
            pady=(2,8)
        )

        self.refresh()

    # =====================================================

    def refresh(self):

        d = self.drive

        self.name.configure(

            text=f"{d.name} ({d.letter})"

        )

        self.status.configure(

            text=d.status.upper(),

            fg_color=d.color

        )

        self.progress.set(

            d.percent / 100

        )

        self.storage.configure(

            text=(

                f"{format_size(d.free)} free of "

                f"{format_size(d.total)}"

            )

        )

        self.speed.configure(

            text=(

                f"↑ {format_speed(d.speed_up)}    "

                f"↓ {format_speed(d.speed_down)}"

                f"    •    {d.transfers} transfer(s)"

            )

        )