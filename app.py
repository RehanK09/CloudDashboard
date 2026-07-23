import customtkinter as ctk

from dashboard import Dashboard


class CloudDashboard:

    def __init__(self):

        ctk.set_appearance_mode("Dark")

        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()

        self.app.title("Cloud Dashboard")

        self.app.geometry("1450x900")

        self.app.minsize(1200, 800)

        Dashboard(self.app)

    def run(self):

        self.app.mainloop()