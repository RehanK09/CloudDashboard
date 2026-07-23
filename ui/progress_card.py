import customtkinter as ctk
from formatters import (
    format_size,
    format_speed,
    format_eta,
    format_percentage,
    shorten_filename,
    format_storage
)







class ProgressCard:

    def __init__(self, parent):

        self.container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        self.container.pack(
            fill="x",
            padx=15,
            pady=(0,10)
        )

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # =====================================================
        # STORAGE CARD
        # =====================================================

        self.storage_card = ctk.CTkFrame(
            self.container,
            corner_radius=15
        )

        self.storage_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,6)
        )

        ctk.CTkLabel(

            self.storage_card,

            text="💾 Cloud Storage",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=18,
            pady=(16,10)
        )

        self.storage_bar = ctk.CTkProgressBar(
            self.storage_card,
            height=18,
            corner_radius=12
        )

        self.storage_bar.pack(
            fill="x",
            padx=18
        )

        self.storage_bar.set(0)

        self.storage_used = ctk.CTkLabel(

            self.storage_card,

            text="Used : --",

            font=("Segoe UI",14)

        )

        self.storage_used.pack(
            anchor="w",
            padx=18,
            pady=(12,2)
        )

        self.storage_free = ctk.CTkLabel(

            self.storage_card,

            text="Free : --",

            font=("Segoe UI",14)

        )

        self.storage_free.pack(
            anchor="w",
            padx=18,
            pady=2
        )

        self.storage_total = ctk.CTkLabel(

            self.storage_card,

            text="Total : --",

            font=("Segoe UI",14)

        )

        self.storage_total.pack(
            anchor="w",
            padx=18,
            pady=(2,16)
        )

        # =====================================================
        # CURRENT UPLOAD
        # =====================================================

        self.upload_card = ctk.CTkFrame(
            self.container,
            corner_radius=15
        )

        self.upload_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6,0)
        )

        ctk.CTkLabel(

            self.upload_card,

            text="⬆ Current Upload",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=18,
            pady=(16,10)
        )

        self.upload_name = ctk.CTkLabel(

            self.upload_card,

            text="Idle",

            font=("Segoe UI",15)

        )

        self.upload_name.pack(
            anchor="w",
            padx=18
        )

        self.upload_bar = ctk.CTkProgressBar(
            self.upload_card,
            height=18,
            corner_radius=12
        )

        self.upload_bar.pack(
            fill="x",
            padx=18,
            pady=(12,8)
        )

        self.upload_bar.set(0)

        self.upload_percent = ctk.CTkLabel(

            self.upload_card,

            text="0%",

            font=("Segoe UI",14)

        )

        self.upload_percent.pack(
            anchor="w",
            padx=18
        )

        self.upload_speed = ctk.CTkLabel(

            self.upload_card,

            text="Speed : --",

            font=("Segoe UI",14)

        )

        self.upload_speed.pack(
            anchor="w",
            padx=18,
            pady=(4,2)
        )

        self.upload_eta = ctk.CTkLabel(

            self.upload_card,

            text="ETA : --",

            font=("Segoe UI",14)

        )

        self.upload_eta.pack(
            anchor="w",
            padx=18,
            pady=(2,16)
        )

    def update(self, stats, storage, transfer):

        # ================= STORAGE =================

        percent = storage.get("percent", 0)

        self.storage_bar.set(percent / 100)


        storage_text = format_storage(
            storage.get("used", 0),
            storage.get("total", 0)
        )


        parts = storage_text.split("\n")

        self.storage_used.configure(
            text=parts[0]
        )

        self.storage_free.configure(
            text=parts[1]
        )

        self.storage_total.configure(
            text=""
        )





        # ================= UPLOAD =================

        if transfer:

            progress = transfer.get("percentage", 0)

            self.upload_bar.set(progress / 100)


            self.upload_name.configure(
                text=shorten_filename(
                    transfer.get("name", "Unknown")
                )
            )

            self.upload_percent.configure(
                text=format_percentage(progress)
            )

            self.upload_speed.configure(
                text=f"Speed : {format_speed(transfer.get('speed',0))}"
            )

            self.upload_eta.configure(
                text=f"ETA : {format_eta(transfer.get('eta'))}"
            )            



        else:

            self.upload_bar.set(0)

            self.upload_name.configure(
                text="Idle"
            )

            self.upload_percent.configure(
                text="0%"
            )

            self.upload_speed.configure(
                text="Speed : --"
            )

            self.upload_eta.configure(
                text="ETA : --"
            )