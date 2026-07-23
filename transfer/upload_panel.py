import customtkinter as ctk


class UploadPanel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text="Upload Queue",
            font=("Segoe UI Semibold",18)
        )

        self.title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12,8)
        )

        self.list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.list.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0,10)
        )

        self.grid_rowconfigure(1, weight=1)

    def refresh(self, transfers):

        for child in self.list.winfo_children():
            child.destroy()

        if not transfers:

            ctk.CTkLabel(
                self.list,
                text="No Active Uploads",
                font=("Segoe UI",15)
            ).pack(
                pady=35
            )

            return

        for item in transfers:

            frame = ctk.CTkFrame(
                self.list,
                corner_radius=10
            )

            frame.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                frame,
                text=item["name"],
                anchor="w",
                font=("Segoe UI",14)
            ).pack(
                anchor="w",
                padx=10,
                pady=(8,2)
            )

            bar = ctk.CTkProgressBar(
                frame,
                height=8
            )

            bar.pack(
                fill="x",
                padx=10
            )

            bar.set(
                item["percentage"]/100
            )

            ctk.CTkLabel(
                frame,
                text=f'{item["percentage"]:.1f}%   •   {item["speed"]}',
                anchor="w",
                font=("Segoe UI",11)
            ).pack(
                anchor="w",
                padx=10,
                pady=(3,8)
            )