import customtkinter as ctk

from core.api import api
from utils import open_drive
from history import open_history_window


class QuickActions(ctk.CTkFrame):

    BTN_W = 85
    BTN_H = 30

    def __init__(self, parent):

        super().__init__(
            parent,
            corner_radius=15
        )

        self.refresh_callback = None

        self.grid_columnconfigure((0,1,2), weight=1)

        self.start = ctk.CTkButton(

            self,

            text="▶ Start",

            width=self.BTN_W,

            height=self.BTN_H,

            command=self.resume

        )

        self.pause = ctk.CTkButton(

            self,

            text="⏸ Pause",

            width=self.BTN_W,

            height=self.BTN_H,

            command=self.pause_uploads

        )

        self.stop = ctk.CTkButton(

            self,

            text="⏹ Stop",

            width=self.BTN_W,

            height=self.BTN_H,

            fg_color="#C62828",

            hover_color="#B71C1C",

            command=self.stop_uploads

        )

        self.refresh = ctk.CTkButton(

            self,

            text="🔄 Refresh",

            width=self.BTN_W,

            height=self.BTN_H,

            command=self.do_refresh

        )

        self.drive = ctk.CTkButton(

            self,

            text="📂 Drive",

            width=self.BTN_W,

            height=self.BTN_H,

            command=open_drive

        )

        self.history = ctk.CTkButton(

            self,

            text="📜 History",

            width=self.BTN_W,

            height=self.BTN_H,

            command=lambda: open_history_window(self.winfo_toplevel())

        )

        self.start.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.pause.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        self.stop.grid(
            row=0,
            column=2,
            padx=5,
            pady=5
        )

        self.refresh.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.drive.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        self.history.grid(
            row=1,
            column=2,
            padx=5,
            pady=5
        )

    # ==================================================

    def set_refresh_callback(

        self,

        callback

    ):

        self.refresh_callback = callback

    # ==================================================

    def do_refresh(self):

        if self.refresh_callback:

            self.refresh_callback()

    # ==================================================

    def pause_uploads(self):

        try:

            api.pause()

        except Exception:

            pass

    # ==================================================

    def resume(self):

        try:

            api.resume()

        except Exception:

            pass

    # ==================================================

    def stop_uploads(self):

        try:

            api.stop_all()

        except Exception:

            pass