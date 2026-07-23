import customtkinter as ctk

from storage.storage_manager import StorageManager
from storage.drive_bar import DriveBar


class StorageCard(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.manager = StorageManager()

        self.bars = []

        # --------------------------------------------------

        self.title = ctk.CTkLabel(

            self,

            text="💾 Storage Overview",

            font=("Segoe UI Semibold",20)

        )

        self.title.pack(

            anchor="w",

            padx=15,

            pady=(12,10)

        )

        # --------------------------------------------------

        self.scroll = ctk.CTkScrollableFrame(

            self,

            fg_color="transparent"

        )

        self.scroll.pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0,10)

        )

        # --------------------------------------------------

        self.build()

    # ======================================================

    def build(self):

        for widget in self.scroll.winfo_children():

            widget.destroy()

        self.bars.clear()

        for drive in self.manager.get():

            bar = DriveBar(

                self.scroll,

                drive

            )

            bar.pack(

                fill="x",

                pady=6,

                padx=4

            )

            self.bars.append(bar)

    # ======================================================

    def refresh(

        self,

        storage=None,

        stats=None

    ):

        #
        # Temporary:
        # First drive uses current API.
        # Later every drive will query individually.
        #

        if storage and self.manager.drives:

            drive = self.manager.drives[0]

            drive.connected = True

            drive.update_storage(

                storage.get(

                    "used",

                    0

                ),

                storage.get(

                    "free",

                    0

                ),

                storage.get(

                    "total",

                    0

                )

            )

            if stats:

                drive.update_activity(

                    uploading=len(

                        stats.get(

                            "transferring",

                            []

                        )

                    ) > 0,

                    speed_up=stats.get(

                        "speed",

                        0

                    ),

                    transfers=len(

                        stats.get(

                            "transferring",

                            []

                        )

                    ),

                    errors=stats.get(

                        "errors",

                        0

                    )

                )

        for bar in self.bars:

            bar.refresh()