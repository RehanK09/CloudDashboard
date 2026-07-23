import customtkinter as ctk


class Section(ctk.CTkFrame):

    def __init__(

        self,

        parent,

        title="",

        subtitle="",

        **kwargs

    ):

        super().__init__(

            parent,

            corner_radius=16,

            **kwargs

        )

        self.grid_columnconfigure(0, weight=1)

        # ============================================

        self.header = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.header.grid(

            row=0,

            column=0,

            sticky="ew",

            padx=15,

            pady=(12,6)

        )

        self.header.grid_columnconfigure(0, weight=1)

        # ============================================

        self.title = ctk.CTkLabel(

            self.header,

            text=title,

            font=("Segoe UI Semibold",18),

            anchor="w"

        )

        self.title.grid(

            row=0,

            column=0,

            sticky="w"

        )

        self.subtitle = ctk.CTkLabel(

            self.header,

            text=subtitle,

            font=("Segoe UI",11),

            text_color="gray70"

        )

        self.subtitle.grid(

            row=1,

            column=0,

            sticky="w"

        )

        # ============================================

        self.content = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.content.grid(

            row=1,

            column=0,

            sticky="nsew",

            padx=10,

            pady=(0,10)

        )

        self.grid_rowconfigure(1, weight=1)

    # ============================================

    def body(self):

        return self.content

    # ============================================

    def set_title(

        self,

        text

    ):

        self.title.configure(

            text=text

        )

    def set_subtitle(

        self,

        text

    ):

        self.subtitle.configure(

            text=text

        )