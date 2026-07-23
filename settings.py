import customtkinter as ctk

_settings_window = None


def open_settings_window(master):

    global _settings_window

    if _settings_window is not None:

        try:
            if _settings_window.winfo_exists():
                _settings_window.lift()
                _settings_window.focus_force()
                return _settings_window
        except:
            pass

    _settings_window = SettingsWindow(master)

    return _settings_window


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, master):

        super().__init__(master)

        self.title("Settings")

        self.geometry("700x500")

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Segoe UI", 26, "bold")
        )

        title.pack(
            pady=20
        )

        notebook = ctk.CTkTabview(self)

        notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        general = notebook.add("General")

        appearance = notebook.add("Appearance")

        cloud = notebook.add("Cloud")

        advanced = notebook.add("Advanced")

        ctk.CTkLabel(
            general,
            text="General settings will be here."
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            appearance,
            text="Appearance settings will be here."
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            cloud,
            text="Cloud settings will be here."
        ).pack(
            pady=20
        )

        ctk.CTkLabel(
            advanced,
            text="Advanced settings will be here."
        ).pack(
            pady=20
        )

    def close(self):

        global _settings_window

        _settings_window = None

        self.destroy()