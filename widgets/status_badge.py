import customtkinter as ctk


class StatusBadge(ctk.CTkLabel):

    COLORS = {

        "OFFLINE": "#C62828",

        "ONLINE": "#43A047",

        "IDLE": "#757575",

        "UPLOADING": "#1E88E5",

        "DOWNLOADING": "#43A047",

        "SYNCING": "#8E24AA",

        "PAUSED": "#F9A825",

        "ERROR": "#D32F2F"

    }

    def __init__(

        self,

        parent,

        text="OFFLINE"

    ):

        super().__init__(

            parent,

            text=text,

            width=110,

            height=30,

            corner_radius=15,

            font=("Segoe UI",11,"bold")

        )

        self.set(text)

    # =============================================

    def set(

        self,

        state

    ):

        state = str(state).upper()

        self.configure(

            text=state,

            fg_color=self.COLORS.get(

                state,

                "#616161"

            )

        )