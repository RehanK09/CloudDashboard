import customtkinter as ctk


class GraphCard:

    def __init__(self, parent, graph):

        self.graph = graph

        self.container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0,15)
        )

        self.container.grid_columnconfigure(0, weight=3)
        self.container.grid_columnconfigure(1, weight=2)
        self.container.grid_rowconfigure(0, weight=1)

        # =====================================================
        # GRAPH
        # =====================================================

        self.graph_frame = ctk.CTkFrame(
            self.container,
            corner_radius=15
        )

        self.graph_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,6)
        )

        ctk.CTkLabel(

            self.graph_frame,

            text="📈 Live Upload Speed",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=18,
            pady=(16,10)
        )

        self.canvas = ctk.CTkCanvas(

            self.graph_frame,

            height=260,

            bg="#202020",

            highlightthickness=0

        )

        self.canvas.pack(

            fill="both",

            expand=True,

            padx=18,

            pady=(0,18)

        )

        # =====================================================
        # STATISTICS
        # =====================================================

        self.stats_frame = ctk.CTkFrame(
            self.container,
            corner_radius=15
        )

        self.stats_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6,0)
        )

        ctk.CTkLabel(

            self.stats_frame,

            text="📊 Statistics",

            font=("Segoe UI Semibold",18)

        ).pack(
            anchor="w",
            padx=18,
            pady=(16,15)
        )

        self.labels = {}

        items = [

            "Current Speed",

            "Peak Speed",

            "Transferred",

            "Active Transfers",

            "Errors"

        ]

        for item in items:

            row = ctk.CTkFrame(
                self.stats_frame,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=18,
                pady=4
            )

            ctk.CTkLabel(

                row,

                text=item,

                font=("Segoe UI",14),

                text_color="gray75"

            ).pack(
                side="left"
            )

            value = ctk.CTkLabel(

                row,

                text="--",

                font=("Segoe UI Semibold",15)

            )

            value.pack(
                side="right"
            )

            self.labels[item] = value

    def update_stats(self, stats):

        from formatters import format_size, format_speed, average

        self.labels["Current Speed"].configure(

            text=format_speed(
                stats.get("speed",0)
            )

        )

        self.labels["Peak Speed"].configure(

            text=format_speed(
                max(
                    self.graph.values
                ) if self.graph.values else 0
            )

        )

        self.labels["Transferred"].configure(

            text=format_size(
                stats.get("bytes",0)
            )

        )

        self.labels["Active Transfers"].configure(

            text=str(
                len(
                    stats.get(
                        "transferring",
                        []
                    )
                )
            )

        )

        self.labels["Errors"].configure(

            text=str(
                stats.get(
                    "errors",
                    0
                )
            )

        )

    def redraw(self):

        self.canvas.delete("all")

        values = self.graph.percent()

        if len(values) < 2:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10 or h < 10:
            return

        for i in range(5):

            y = h * i / 4

            self.canvas.create_line(

                0,

                y,

                w,

                y,

                fill="#303030"

            )

        step = w / (len(values)-1)

        pts = []

        for i, v in enumerate(values):

            x = i * step

            y = h - (v/100)*h

            pts.extend((x,y))

        self.canvas.create_line(

            *pts,

            smooth=True,

            width=3,

            fill="#3B82F6"

        )