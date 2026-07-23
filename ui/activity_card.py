import customtkinter as ctk

from history import load_history


class ActivityCard:

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.title = ctk.CTkLabel(
            self.frame,
            text="Recent Activity",
            font=("Segoe UI", 18, "bold")
        )

        self.title.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.textbox = ctk.CTkTextbox(
            self.frame,
            height=180
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.textbox.configure(
            state="disabled"
        )

    def refresh(self):

        self.textbox.configure(
            state="normal"
        )

        self.textbox.delete(
            "1.0",
            "end"
        )

        try:

            items = load_history(limit=20)

            if not items:

                self.textbox.insert(
                    "end",
                    "No transfer history yet."
                )

            else:

                for item in items:

                    icon = "✔"

                    if item.get("status") == "FAILED":
                        icon = "❌"

                    line = (
                        f"{icon} "
                        f"{item.get('time','')}   "
                        f"{item.get('filename','Unknown')}   "
                        f"{item.get('size','')}   "
                        f"{item.get('status','')}\n"
                    )

                    self.textbox.insert(
                        "end",
                        line
                    )

        except Exception as e:

            self.textbox.insert(
                "end",
                str(e)
            )

        self.textbox.configure(
            state="disabled"
        )