"""
Dashboard Header
Recognition System v2
"""

import customtkinter as ctk


class StatisticCard(ctk.CTkFrame):
    """
    Reusable statistics card.
    """

    def __init__(
        self,
        master,
        title: str,
        value="0",
        color="#3B82F6"
    ):
        super().__init__(
            master,
            corner_radius=12,
            fg_color="#1E293B",
            height=110
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 14)
        )

        self.title_label.grid(
            row=0,
            column=0,
            pady=(15, 5)
        )

        self.value_label = ctk.CTkLabel(
            self,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )

        self.value_label.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

    def set_value(self, value):
        self.value_label.configure(text=str(value))


class DashboardHeader(ctk.CTkFrame):
    """
    Top statistics row.
    """

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="transparent"
        )

        for column in range(4):
            self.grid_columnconfigure(column, weight=1)

        self.face_card = StatisticCard(
            self,
            "Registered Faces",
            color="#22C55E"
        )

        self.face_card.grid(
            row=0,
            column=0,
            padx=8,
            sticky="ew"
        )

        self.unknown_card = StatisticCard(
            self,
            "Unknown Faces",
            color="#F59E0B"
        )

        self.unknown_card.grid(
            row=0,
            column=1,
            padx=8,
            sticky="ew"
        )

        self.track_card = StatisticCard(
            self,
            "Active Tracks",
            color="#3B82F6"
        )

        self.track_card.grid(
            row=0,
            column=2,
            padx=8,
            sticky="ew"
        )

        self.fps_card = StatisticCard(
            self,
            "FPS",
            color="#EF4444"
        )

        self.fps_card.grid(
            row=0,
            column=3,
            padx=8,
            sticky="ew"
        )