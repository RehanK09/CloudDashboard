import json
import os
from datetime import datetime
import customtkinter as ctk

HISTORY_FILE = "history.json"


def _ensure_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_history():
    _ensure_file()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


def add_history(
    filename,
    size="Unknown",
    status="SUCCESS",
    destination="Cloud",
    speed="",
    duration=""
):
    history = load_history()

    history.insert(
        0,
        {
            "date": datetime.now().strftime("%d-%m-%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "filename": filename,
            "size": size,
            "status": status,
            "destination": destination,
            "speed": speed,
            "duration": duration
        }
    )

    history = history[:1000]

    save_history(history)


def clear_history():
    save_history([])


def delete_entry(index):
    history = load_history()

    if 0 <= index < len(history):
        history.pop(index)

    save_history(history)


class HistoryWindow(ctk.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Upload History")
        self.geometry("900x550")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Upload History",
            font=("Segoe UI", 24, "bold")
        )
        title.grid(row=0, column=0, pady=15)

        self.box = ctk.CTkTextbox(
            self,
            font=("Consolas", 13)
        )

        self.box.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15
        )

        bottom = ctk.CTkFrame(self)
        bottom.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )

        refresh = ctk.CTkButton(
            bottom,
            text="Refresh",
            command=self.refresh
        )

        refresh.pack(side="left", padx=5)

        clear = ctk.CTkButton(
            bottom,
            text="Clear History",
            fg_color="#b71c1c",
            hover_color="#8b0000",
            command=self.clear
        )

        clear.pack(side="right", padx=5)

        self.refresh()

    def refresh(self):

        self.box.delete("1.0", "end")

        history = load_history()

        if len(history) == 0:

            self.box.insert(
                "end",
                "\nNo upload history available."
            )

            return

        for i, item in enumerate(history, 1):

            self.box.insert(
                "end",
                f"""
====================================================

#{i}

Date        : {item.get("date","")}

Time        : {item.get("time","")}

File        : {item.get("filename","")}

Size        : {item.get("size","")}

Status      : {item.get("status","")}

Destination : {item.get("destination","")}

Speed       : {item.get("speed","")}

Duration    : {item.get("duration","")}

====================================================

"""
            )

    def clear(self):
        clear_history()
        self.refresh()