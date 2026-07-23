import customtkinter as ctk

from utils import format_size


class ProgressCard:

    DAILY_GOAL = 50 * 1024 * 1024 * 1024  # 50 GB

    def __init__(self, parent):

        self.frame = ctk.CTkFrame(parent)

        self.frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ---------------- Storage ----------------

        ctk.CTkLabel(
            self.frame,
            text="Cloud Storage"
        ).pack(anchor="w", padx=20)

        self.storage_bar = ctk.CTkProgressBar(self.frame)

        self.storage_bar.pack(
            fill="x",
            padx=20
        )

        self.storage_bar.set(0)

        self.storage_info = ctk.CTkLabel(
            self.frame,
            text="--"
        )

        self.storage_info.pack(
            anchor="w",
            padx=20,
            pady=(0,12)
        )

        # ---------------- Upload ----------------

        ctk.CTkLabel(
            self.frame,
            text="Current Upload"
        ).pack(anchor="w", padx=20)

        self.upload_bar = ctk.CTkProgressBar(self.frame)

        self.upload_bar.pack(
            fill="x",
            padx=20
        )

        self.upload_bar.set(0)

        self.upload_info = ctk.CTkLabel(
            self.frame,
            text="Idle"
        )

        self.upload_info.pack(
            anchor="w",
            padx=20,
            pady=(0,12)
        )

        # ---------------- Queue ----------------

        ctk.CTkLabel(
            self.frame,
            text="Transfer Queue"
        ).pack(anchor="w", padx=20)

        self.queue_bar = ctk.CTkProgressBar(self.frame)

        self.queue_bar.pack(
            fill="x",
            padx=20
        )

        self.queue_bar.set(0)

        self.queue_info = ctk.CTkLabel(
            self.frame,
            text="0 Active"
        )

        self.queue_info.pack(
            anchor="w",
            padx=20,
            pady=(0,12)
        )

        # ---------------- Daily Goal ----------------

        ctk.CTkLabel(
            self.frame,
            text="Today's Upload Goal"
        ).pack(anchor="w", padx=20)

        self.today_bar = ctk.CTkProgressBar(self.frame)

        self.today_bar.pack(
            fill="x",
            padx=20
        )

        self.today_bar.set(0)

        self.today_info = ctk.CTkLabel(
            self.frame,
            text="0 B / 50 GB"
        )

        self.today_info.pack(
            anchor="w",
            padx=20,
            pady=(0,15)
        )

    def update(self, stats, storage, transfer):

        # -------- Storage --------

        percent = storage.get("percent", 0)

        self.storage_bar.set(percent / 100)

        self.storage_info.configure(
            text=(
                f"{format_size(storage.get('used',0))}"
                f" / "
                f"{format_size(storage.get('total',0))}"
                f" ({percent:.1f}%)"
            )
        )

        # -------- Upload --------

        if transfer:

            progress = transfer.get("percentage", 0)

            self.upload_bar.set(progress / 100)

            self.upload_info.configure(
                text=f"{progress:.1f}%"
            )

        else:

            self.upload_bar.set(0)

            self.upload_info.configure(
                text="Idle"
            )

        # -------- Queue --------

        transfers = stats.get("transferring", [])

        active = len(transfers)

        self.queue_bar.set(
            min(active / 10, 1)
        )

        self.queue_info.configure(
            text=f"{active} Active"
        )

        # -------- Daily Goal --------

        uploaded = stats.get("bytes", 0)

        today_percent = min(
            uploaded / self.DAILY_GOAL,
            1
        )

        self.today_bar.set(today_percent)

        self.today_info.configure(
            text=(
                f"{format_size(uploaded)}"
                f" / "
                f"{format_size(self.DAILY_GOAL)}"
            )
        )