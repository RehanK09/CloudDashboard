import customtkinter as ctk

from transfer.transfer_card import TransferCard
from transfer.transfer import Transfer


class UploadQueue(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.transfers = {}

        # -----------------------------------------------------

        self.header = ctk.CTkLabel(

            self,

            text="⬆ Upload Queue (0)",

            font=("Segoe UI Semibold",18)

        )

        self.header.pack(

            anchor="w",

            padx=15,

            pady=(12,8)

        )

        # -----------------------------------------------------

        self.canvas = ctk.CTkScrollableFrame(

            self,

            fg_color="transparent"

        )

        self.canvas.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0,10)

        )

        self.empty = ctk.CTkLabel(

            self.canvas,

            text="No Active Uploads",

            text_color="gray70",

            font=("Segoe UI",15)

        )

        self.empty.pack(

            pady=25

        )

    # ======================================================

    def update(self, stats):

        active = {}

        transferring = stats.get(

            "transferring",

            []

        )

        for item in transferring:

            name = item.get(

                "name",

                "Unknown"

            )

            active[name] = True

            if name not in self.transfers:

                transfer = Transfer(

                    name=name,

                    direction="upload"

                )

                card = TransferCard(

                    self.canvas,

                    transfer

                )

                self.transfers[name] = (

                    transfer,

                    card

                )

                card.pack(

                    fill="x",

                    pady=6,

                    padx=5

                )

            transfer, card = self.transfers[name]

            transfer.update(

                size=item.get(

                    "size",

                    0

                ),

                transferred=item.get(

                    "bytes",

                    0

                ),

                speed=item.get(

                    "speed",

                    0

                ),

                eta=item.get(

                    "eta"

                ),

                status="uploading"

            )

            card.refresh()

        remove = []

        for name in self.transfers:

            if name not in active:

                remove.append(

                    name

                )

        for name in remove:

            transfer, card = self.transfers.pop(

                name

            )

            card.destroy()

        count = len(

            self.transfers

        )

        self.header.configure(

            text=f"⬆ Upload Queue ({count})"

        )

        if count == 0:

            if not self.empty.winfo_exists():

                self.empty = ctk.CTkLabel(

                    self.canvas,

                    text="No Active Uploads",

                    text_color="gray70",

                    font=("Segoe UI",15)

                )

                self.empty.pack(

                    pady=25

                )

        else:

            if self.empty.winfo_exists():

                self.empty.destroy()