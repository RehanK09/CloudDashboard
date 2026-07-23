import customtkinter as ctk


class IconButton(ctk.CTkButton):

    def __init__(

        self,

        parent,

        icon,

        command=None,

        tooltip=None,

        width=38,

        height=38,

        fg="#2B2B2B",

        hover="#3A3A3A"

    ):

        super().__init__(

            parent,

            text=icon,

            width=width,

            height=height,

            corner_radius=10,

            font=("Segoe UI Emoji",16),

            fg_color=fg,

            hover_color=hover,

            command=command

        )

        self.tooltip = tooltip

    def enable(self):

        self.configure(

            state="normal"

        )

    def disable(self):

        self.configure(

            state="disabled"

        )

    def active(self):

        self.configure(

            border_width=2,

            border_color="#3B82F6"

        )

    def inactive(self):

        self.configure(

            border_width=0

        )

    def danger(self):

        self.configure(

            fg_color="#C62828",

            hover_color="#B71C1C"

        )

    def success(self):

        self.configure(

            fg_color="#2E7D32",

            hover_color="#1B5E20"

        )

    def warning(self):

        self.configure(

            fg_color="#F9A825",

            hover_color="#F57F17"

        )

    def normal(self):

        self.configure(

            fg_color="#2B2B2B",

            hover_color="#3A3A3A"

        )