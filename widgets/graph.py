import customtkinter as ctk


class GraphWidget(ctk.CTkFrame):

    MAX_POINTS = 120

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.upload = [0] * self.MAX_POINTS
        self.download = [0] * self.MAX_POINTS

        self.title = ctk.CTkLabel(

            self,

            text="Live Transfer Speed",

            font=("Segoe UI Semibold", 18)

        )

        self.title.pack(
            anchor="w",
            padx=15,
            pady=(12, 6)
        )

        self.canvas = ctk.CTkCanvas(

            self,

            height=230,

            highlightthickness=0,

            bd=0,

            bg="#202020"

        )

        self.canvas.pack(

            fill="both",

            expand=True,

            padx=12,

            pady=(0, 12)

        )

        self.after(

            100,

            self._resize

        )

    # =====================================================

    def _resize(self):

        self.redraw()

    # =====================================================

    def update(self, stats):

        upload_speed = float(

            stats.get(

                "speed",

                0

            )

        )

        #
        # rclone currently exposes upload speed.
        # Download speed will be added later.
        #

        download_speed = float(

            stats.get(

                "download_speed",

                0

            )

        )

        self.upload.append(upload_speed)
        self.download.append(download_speed)

        if len(self.upload) > self.MAX_POINTS:
            self.upload.pop(0)

        if len(self.download) > self.MAX_POINTS:
            self.download.pop(0)

        self.redraw()

    # =====================================================

    def redraw(self):

        self.canvas.delete("all")

        w = max(
            self.canvas.winfo_width(),
            100
        )

        h = max(
            self.canvas.winfo_height(),
            100
        )

        # Grid

        for i in range(6):

            y = h * i / 5

            self.canvas.create_line(

                0,

                y,

                w,

                y,

                fill="#333333"

            )

        for i in range(10):

            x = w * i / 9

            self.canvas.create_line(

                x,

                0,

                x,

                h,

                fill="#2A2A2A"

            )

        maximum = max(

            max(self.upload),

            max(self.download),

            1

        )

        self.draw_line(

            self.upload,

            "#4FC3F7",

            maximum,

            w,

            h

        )

        self.draw_line(

            self.download,

            "#81C784",

            maximum,

            w,

            h

        )

    # =====================================================

    def draw_line(

        self,

        values,

        color,

        maximum,

        width,

        height

    ):

        if len(values) < 2:
            return

        points = []

        for i, value in enumerate(values):

            x = i * width / (self.MAX_POINTS - 1)

            y = height - ((value / maximum) * height)

            points.extend([x, y])

        self.canvas.create_line(

            *points,

            fill=color,

            width=2,

            smooth=True

        )

    # =====================================================

    def refresh(self):

        self.redraw()