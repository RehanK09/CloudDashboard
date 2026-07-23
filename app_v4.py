import customtkinter as ctk

from dashboard_v4 import DashboardV4


class CloudDashboardV4:

    def __init__(self):

        ctk.set_appearance_mode("Dark")

        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()

        self.app.title("Cloud Dashboard V4")

        self.app.geometry("1550x920")

        self.app.minsize(1350, 850)

        DashboardV4(self.app)

    def run(self):

        self.app.mainloop()


if __name__ == "__main__":

    CloudDashboardV4().run()