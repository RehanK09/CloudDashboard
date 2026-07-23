import customtkinter as ctk

from history import load_history


class ActivityCard:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(
            parent,
            corner_radius=15
        )

        self.frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        ctk.CTkLabel(

            self.frame,

            text="🕒 Recent Activity",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=18,
            pady=(16,12)
        )

        self.timeline = ctk.CTkScrollableFrame(
            self.frame,
            fg_color="transparent"
        )

        self.timeline.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

    def refresh(self):

        for widget in self.timeline.winfo_children():

            widget.destroy()

        try:

            history = load_history(limit=15)

        except:

            history = []

        if not history:

            ctk.CTkLabel(

                self.timeline,

                text="No recent activity",

                font=("Segoe UI",15),

                text_color="gray70"

            ).pack(
                pady=30
            )

            return

        for item in history:

            card = ctk.CTkFrame(
                self.timeline,
                corner_radius=12
            )

            card.pack(
                fill="x",
                pady=5,
                padx=5
            )

            if item.get("status") == "SUCCESS":

                icon = "🟢"

            else:

                icon = "🔴"

            top = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            top.pack(
                fill="x",
                padx=12,
                pady=(10,5)
            )

            ctk.CTkLabel(

                top,

                text=f"{icon}  {item.get('filename','Unknown')}",

                font=("Segoe UI Semibold",15),

                anchor="w"

            ).pack(
                side="left"
            )

            ctk.CTkLabel(

                top,

                text=item.get("time",""),

                font=("Segoe UI",13),

                text_color="gray70"

            ).pack(
                side="right"
            )

            bottom = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            bottom.pack(
                fill="x",
                padx=12,
                pady=(0,10)
            )

            info = (

                f"{item.get('size','')}"

                "   •   "

                f"{item.get('status','')}"

                "   •   "

                f"{item.get('speed','')}"

            )

            ctk.CTkLabel(

                bottom,

                text=info,

                font=("Segoe UI",13),

                text_color="gray75"

            ).pack(
                anchor="w"
            )