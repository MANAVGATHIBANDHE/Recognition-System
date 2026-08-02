"""
Main Window

Project:
    Recognition System
"""

from __future__ import annotations

import customtkinter as ctk

from config.application import ApplicationConfig


class MainWindow(ctk.CTk):
    """Main desktop application window."""

    def __init__(self) -> None:
        super().__init__()

        self.initialize_window()

    def initialize_window(self) -> None:

        self.title(
            f"{ApplicationConfig.NAME} {ApplicationConfig.VERSION}"
        )

        self.geometry(
            f"{ApplicationConfig.WINDOW_WIDTH}x{ApplicationConfig.WINDOW_HEIGHT}"
        )

        self.minsize(
            ApplicationConfig.MIN_WIDTH,
            ApplicationConfig.MIN_HEIGHT,
        )

        self.create_layout()

    def create_layout(self) -> None:

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
        )

        sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        title = ctk.CTkLabel(
            sidebar,
            text="Recognition\nSystem",
            font=("Segoe UI", 24, "bold"),
        )

        title.pack(pady=30)

        buttons = [
            "Dashboard",
            "Face Recognition",
            "Object Detection",
            "Voice Recognition",
            "OCR",
            "Events",
            "Settings",
        ]

        for item in buttons:
            button = ctk.CTkButton(
                sidebar,
                text=item,
                height=40,
            )

            button.pack(
                padx=15,
                pady=6,
                fill="x",
            )

        self.content = ctk.CTkFrame(self)

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        welcome = ctk.CTkLabel(
            self.content,
            text="Recognition System\nDesktop Platform",
            font=("Segoe UI", 30, "bold"),
        )

        welcome.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )