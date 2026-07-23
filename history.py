"""
history.py
----------
Real transfer history, built entirely on api.py's cached data.

Replaces the old watch_uploads() in dashboard.py, which polled
/core/stats every 5s, diffed the total byte counter, and logged a
single fake "Unknown File" row per detected jump. That approach could
never know a real filename, and it merged multiple simultaneous
transfers into one entry.

This version watches the real per-file `transferring` list that
rclone_api.get_stats() exposes (name, size, bytes, speed) and turns
each file's full lifecycle — appears in the list, then disappears —
into one real history.json row: actual filename, actual size, start
time, end time, duration, average speed.

Two pieces:
- HistoryTracker  : call .tick() once per second from the dashboard's
                    existing app.after loop (no network — it only reads
                    rclone_api.get_stats(), which is already cached).
- open_history_window(master) : opens the singleton History window,
                    or focuses the existing one if it's already open.

CAVEAT (being upfront about it): rclone's RC API doesn't attach a
success/fail flag to an individual disappearing transfer. What we do
here is compare the global error counter at the moment a file started
transferring against the counter when it disappears — if it went up,
we mark that entry FAILED, otherwise SUCCESS. That's a reasonable
heuristic, not a guarantee, when multiple files are transferring at
once and only one of them errors.
"""

import csv
import json
import os
import subprocess
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import customtkinter as ctk

from api import rclone_api
from utils import format_size, format_speed

HISTORY_FILE = "history.json"
DEFAULT_HISTORY_LIMIT = 500


# ======================================================================
# Persistence
# ======================================================================
def _read_config_history_limit():
    try:
        with open("config.json", "r") as f:
            return json.load(f).get("history_limit", DEFAULT_HISTORY_LIMIT)
    except Exception:
        return DEFAULT_HISTORY_LIMIT


def load_history(limit=None):
    """Most-recent-first list of history entries."""
    try:
        with open(HISTORY_FILE, "r") as f:
            items = json.load(f)
    except Exception:
        items = []
    items = list(reversed(items))
    if limit:
        items = items[:limit]
    return items


def add_history_entry(entry):
    try:
        with open(HISTORY_FILE, "r") as f:
            items = json.load(f)
    except Exception:
        items = []

    items.append(entry)

    cap = _read_config_history_limit()
    if cap and len(items) > cap:
        items = items[-cap:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(items, f, indent=2)


def clear_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


def export_history_csv(path):
    items = load_history()
    fieldnames = [
        "date", "time", "filename", "size", "status",
        "destination", "speed", "duration",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow({k: item.get(k, "") for k in fieldnames})


def _format_duration(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m"


# ======================================================================
# HistoryTracker — turns live transferring[] entries into real rows
# ======================================================================
class HistoryTracker:
    def __init__(self):
        self._active = {}  # name -> {start_time, size, errors_at_start}

    def tick(self):
        """Call this once per second (or whatever your refresh rate is)
        from the dashboard's existing app.after loop. Reads only from
        rclone_api's cache — no network call happens here."""
        stats = rclone_api.get_stats()
        current_names = set()

        for item in stats["transferring"]:
            name = item["name"]
            transfer_id = f"{name}_{item.get('size',0)}"
            current_names.add(transfer_id)
            if transfer_id not in self._active:
                self._active[transfer_id] = {
                    "start_time": time.time(),
                    "size": item.get("size", 0),
                    "errors_at_start": stats.get("errors", 0),
                }

        finished = [
        n for n in self._active
        if n not in current_names
        ]
        for name in finished:
            record = self._active.pop(name)
            self._finalize(name, record, stats)

    def _finalize(self, name, record, stats):
        end_time = time.time()
        duration = max(end_time - record["start_time"], 0)
        avg_speed = (record["size"] / duration) if duration > 0 else 0
        failed = stats.get("errors", 0) > record["errors_at_start"]

        entry = {
            "date": time.strftime("%Y-%m-%d", time.localtime(record["start_time"])),
            "time": time.strftime("%H:%M:%S", time.localtime(record["start_time"])),
            "filename": name,
            "size": format_size(record["size"]),
            "status": "FAILED" if failed else "SUCCESS",
            "destination": rclone_api.remote,
            "speed": format_speed(avg_speed),
            "duration": _format_duration(duration),
        }
        add_history_entry(entry)

history_tracker = HistoryTracker()


# ======================================================================
# Singleton History window
# ======================================================================
_history_window = None


def open_history_window(master):
    """Singleton: focuses the existing History window instead of
    stacking up duplicates when the button is clicked repeatedly."""
    global _history_window
    if _history_window is not None and _history_window.winfo_exists():
        _history_window.lift()
        _history_window.focus_force()
        return _history_window

    _history_window = HistoryWindow(master)
    return _history_window


class HistoryWindow(ctk.CTkToplevel):
    COLUMNS = ("date", "time", "filename", "size", "status",
               "destination", "speed", "duration")
    HEADINGS = ("Date", "Time", "Filename", "Size", "Status",
                "Destination", "Speed", "Duration")

    def __init__(self, master):
        super().__init__(master)
        self.title("Transfer History")
        self.geometry("980x520")
        self.minsize(760, 400)

        self._all_items = []
        self._build_ui()
        self._reload()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ------------------------------------------------------------
    def _build_ui(self):
        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=(10, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        search_entry = ctk.CTkEntry(
            toolbar, textvariable=self.search_var,
            placeholder_text="Search filename...", width=240,
        )
        search_entry.pack(side="left", padx=(0, 8))

        self.filter_var = tk.StringVar(value="All")
        filter_menu = ctk.CTkOptionMenu(
            toolbar, values=["All", "SUCCESS", "FAILED"],
            variable=self.filter_var,
            command=lambda _v: self._apply_filter(),
            width=120,
        )
        filter_menu.pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            toolbar, text="Export CSV", width=110, command=self._export_csv,
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(
            toolbar, text="Clear History", width=120,
            fg_color="#c62828", hover_color="#8e0000",
            command=self._clear,
        ).pack(side="right")

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "History.Treeview",
            background="#1f1f1f", fieldbackground="#1f1f1f",
            foreground="white", rowheight=26, borderwidth=0,
        )
        style.configure(
            "History.Treeview.Heading",
            background="#2a2a2a", foreground="white", relief="flat",
        )

        self.tree = ttk.Treeview(
            table_frame, columns=self.COLUMNS, show="headings",
            style="History.Treeview",
        )
        for col, heading in zip(self.COLUMNS, self.HEADINGS):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=110, anchor="w")
        self.tree.column("filename", width=220)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self._open_containing_folder)

    # ------------------------------------------------------------
    def _reload(self):
        self._all_items = load_history()
        self._apply_filter()

    def _apply_filter(self):
        query = self.search_var.get().strip().lower()
        status_filter = self.filter_var.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self._all_items:
            if status_filter != "All" and item.get("status") != status_filter:
                continue
            if query and query not in item.get("filename", "").lower():
                continue
            self.tree.insert("", "end", values=[item.get(c, "") for c in self.COLUMNS])

    def _clear(self):
        if messagebox.askyesno("Clear History", "Delete all history entries?"):
            clear_history()
            self._reload()

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="history_export.csv",
        )
        if not path:
            return
        export_history_csv(path)
        messagebox.showinfo("Export Complete", f"History exported to:\n{path}")

    def _open_containing_folder(self, _event):
        selection = self.tree.selection()
        if not selection:
            return
        values = self.tree.item(selection[0], "values")
        filename = values[2] if len(values) > 2 else None
        if not filename:
            return

        local_path = os.path.join(rclone_api.drive + "\\", filename)
        folder = os.path.dirname(local_path) or rclone_api.drive
        try:
            if os.path.exists(folder):
                subprocess.Popen(["explorer", folder])
            else:
                messagebox.showwarning(
                    "Not Found",
                    "Couldn't locate this file's folder on the mounted drive "
                    "(it may have been moved or the drive may be unmounted).",
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def _on_close(self):
        global _history_window
        _history_window = None
        self.destroy()


    def stop_history():
        global _history_window
        if _history_window is not None:
            try:
                if _history_window.winfo_exists():
                    _history_window.destroy()
            except Exception:
                pass

        _history_window = None