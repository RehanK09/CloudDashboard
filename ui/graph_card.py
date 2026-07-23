import customtkinter as ctk


class GraphCard:

    def __init__(self, parent, graph):

        self.graph = graph

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.title = ctk.CTkLabel(
            self.frame,
            text="Live Upload Speed",
            font=("Segoe UI", 16, "bold")
        )

        self.title.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.canvas = ctk.CTkCanvas(
            self.frame,
            height=140,
            bg="#202020",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

    def redraw(self):

        self.canvas.delete("all")

        values = self.graph.percent()

        if len(values) < 2:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 10 or height <= 10:
            return

        step = width / (len(values) - 1)

        points = []

        for i, value in enumerate(values):

            x = i * step
            y = height - ((value / 100) * height)

            points.extend((x, y))

        try:

            self.canvas.create_line(
                *points,
                width=2,
                smooth=True,
                fill="#00D4FF"
            )

        except Exception:
            pass

        # Grid

        for i in range(1, 5):

            y = height * i / 5

            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#303030"
            )

        # Labels

        self.canvas.create_text(
            10,
            10,
            text="MAX",
            fill="#AAAAAA",
            anchor="nw"
        )

        self.canvas.create_text(
            10,
            height - 10,
            text="0",
            fill="#AAAAAA",
            anchor="sw"
        )