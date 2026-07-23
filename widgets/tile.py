import customtkinter as ctk


class Tile(ctk.CTkFrame):

    def __init__(

        self,

        parent,

        title,

        value="",

        width=170,

        height=90

    ):

        super().__init__(

            parent,

            width=width,

            height=height,

            corner_radius=14

        )

        self.grid_propagate(False)

        self.title = ctk.CTkLabel(

            self,

            text=title,

            font=("Segoe UI",12),

            text_color="gray75"

        )

        self.title.pack(

            anchor="w",

            padx=12,

            pady=(10,2)

        )

        self.value = ctk.CTkLabel(

            self,

            text=value,

            font=("Segoe UI Semibold",22)

        )

        self.value.pack(

            anchor="w",

            padx=12

        )

    def set(

        self,

        value

    ):

        self.value.configure(

            text=value

        )