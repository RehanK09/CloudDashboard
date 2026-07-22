import json
import os
import customtkinter as ctk

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "rc_port": 5572,
    "refresh_ms": 1000,
    "theme": "dark",
    "daily_goal_gb": 50,
    "auto_mount": True,
    "start_with_windows": False,
    "minimize_to_tray": False,
    "history_limit": 1000
}


def load_config():

    if not os.path.exists(CONFIG_FILE):

        save_config(DEFAULT_CONFIG)

        return DEFAULT_CONFIG.copy()

    try:

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:

            cfg = json.load(f)

    except Exception:

        cfg = DEFAULT_CONFIG.copy()

    for k, v in DEFAULT_CONFIG.items():

        cfg.setdefault(k, v)

    return cfg


def save_config(cfg):

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:

        json.dump(cfg, f, indent=4)


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Settings")

        self.geometry("520x520")

        self.resizable(False, False)

        self.cfg = load_config()

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Segoe UI", 26, "bold")
        )

        title.pack(pady=15)

        self.port = ctk.CTkEntry(self)
        self.port.insert(0, str(self.cfg["rc_port"]))
        self.port.pack(fill="x", padx=25, pady=8)

        self.refresh = ctk.CTkEntry(self)
        self.refresh.insert(0, str(self.cfg["refresh_ms"]))
        self.refresh.pack(fill="x", padx=25, pady=8)

        self.goal = ctk.CTkEntry(self)
        self.goal.insert(0, str(self.cfg["daily_goal_gb"]))
        self.goal.pack(fill="x", padx=25, pady=8)

        self.auto_mount = ctk.CTkCheckBox(
            self,
            text="Auto Mount"
        )

        if self.cfg["auto_mount"]:
            self.auto_mount.select()

        self.auto_mount.pack(anchor="w", padx=25, pady=8)

        self.startup = ctk.CTkCheckBox(
            self,
            text="Start with Windows"
        )

        if self.cfg["start_with_windows"]:
            self.startup.select()

        self.startup.pack(anchor="w", padx=25, pady=8)

        self.tray = ctk.CTkCheckBox(
            self,
            text="Minimize to Tray"
        )

        if self.cfg["minimize_to_tray"]:
            self.tray.select()

        self.tray.pack(anchor="w", padx=25, pady=8)

        save = ctk.CTkButton(
            self,
            text="Save Settings",
            command=self.save
        )

        save.pack(pady=25)

    def save(self):

        self.cfg["rc_port"] = int(self.port.get())
        self.cfg["refresh_ms"] = int(self.refresh.get())
        self.cfg["daily_goal_gb"] = int(self.goal.get())

        self.cfg["auto_mount"] = bool(self.auto_mount.get())
        self.cfg["start_with_windows"] = bool(self.startup.get())
        self.cfg["minimize_to_tray"] = bool(self.tray.get())

        save_config(self.cfg)

        self.destroy()