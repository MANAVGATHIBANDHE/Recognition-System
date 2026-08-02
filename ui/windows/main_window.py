"""
Main Window
Recognition System
"""

import customtkinter as ctk

from ui.widgets.dashboard import Dashboard


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Recognition System")
        self.geometry("1200x700")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.build_layout()

    def build_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        logo = ctk.CTkLabel(
            self.sidebar,
            text="Recognition\nSystem",
            font=("Segoe UI", 24, "bold")
        )

        logo.pack(pady=30)

        buttons = [
            "Dashboard",
            "Camera",
            "Face",
            "Object",
            "Voice",
            "OCR",
            "Settings"
        ]

        for name in buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=name,
                width=180
            )

            btn.pack(pady=8)

        self.content = ctk.CTkFrame(
            self
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        dashboard = Dashboard(self.content)

        dashboard.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )