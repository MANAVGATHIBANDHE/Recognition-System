"""
Professional Dashboard
Recognition System v2
"""

from datetime import datetime

import customtkinter as ctk

from services.person.person_database import person_database
from ui.widgets.dashboard_header import DashboardHeader
from ui.widgets.camera_widget import CameraWidget


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.start_time = datetime.now()

        self.last_name = "None"
        self.last_score = 0.0
        self.current_fps = 0

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.build_ui()

        self.update_clock()
        self.update_dashboard()

    # ======================================================
    # BUILD UI
    # ======================================================

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Recognition Dashboard",
            font=("Segoe UI", 30, "bold")
        )

        title.grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        self.header = DashboardHeader(self)

        self.header.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.body = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.body.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 15)
        )

        self.body.grid_columnconfigure(0, weight=3)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        # ======================================================
        # LEFT PANEL
        # ======================================================

        self.left = ctk.CTkFrame(self.body)

        self.left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=15
        )

        self.camera_widget = CameraWidget(self.left)

        self.camera_widget.pack(
            pady=20
        )

        self.register_button = ctk.CTkButton(
            self.left,
            text="➕ Register Person",
            width=220,
            height=40
        )

        self.register_button.pack(
            pady=(0, 20)
        )

        ctk.CTkLabel(
            self.left,
            text="System Status",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 10)
        )

        self.face_label = ctk.CTkLabel(
            self.left,
            text="🙂 Registered Faces : 0",
            font=("Segoe UI", 16)
        )

        self.face_label.pack(anchor="w", padx=20, pady=4)

        self.recognition_label = ctk.CTkLabel(
            self.left,
            text="👤 Last Recognition : None",
            font=("Segoe UI", 16)
        )

        self.recognition_label.pack(anchor="w", padx=20, pady=4)

        self.confidence_label = ctk.CTkLabel(
            self.left,
            text="🎯 Confidence : 0%",
            font=("Segoe UI", 16)
        )

        self.confidence_label.pack(anchor="w", padx=20, pady=4)

        self.fps_label = ctk.CTkLabel(
            self.left,
            text="⚡ FPS : 0",
            font=("Segoe UI", 16)
        )

        self.fps_label.pack(anchor="w", padx=20, pady=4)

        # ======================================================
        # RIGHT PANEL
        # ======================================================

        self.right = ctk.CTkFrame(self.body)

        self.right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 15),
            pady=15
        )

        ctk.CTkLabel(
            self.right,
            text="System Information",
            font=("Segoe UI", 20, "bold")
        ).pack(
            pady=(20, 15)
        )

        self.uptime = ctk.CTkLabel(
            self.right,
            text="00:00:00",
            font=("Segoe UI", 28, "bold")
        )

        self.uptime.pack()

        self.status = ctk.CTkTextbox(
            self.right,
            height=300
        )

        self.status.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.status.insert(
            "end",
            "Recognition System Ready\n\n"
            "Waiting for camera..."
        )

        self.status.configure(state="disabled")

    # ======================================================
    # UPDATE
    # ======================================================

    def update_dashboard(self):

        try:

            total = len(person_database.get_all_persons())

            self.face_label.configure(
                text=f"🙂 Registered Faces : {total}"
            )

            self.header.face_card.set_value(total)

        except Exception:
            pass

        self.after(
            2000,
            self.update_dashboard
        )

    # ======================================================
    # EXTERNAL UPDATE
    # ======================================================

    def set_recognition(
        self,
        name,
        score
    ):

        self.last_name = name
        self.last_score = score

        self.recognition_label.configure(
            text=f"👤 Last Recognition : {name}"
        )

        self.confidence_label.configure(
            text=f"🎯 Confidence : {score*100:.1f}%"
        )

    def set_fps(self, fps):

        self.current_fps = fps

        self.fps_label.configure(
            text=f"⚡ FPS : {fps}"
        )

    # ======================================================
    # CLOCK
    # ======================================================

    def update_clock(self):

        elapsed = datetime.now() - self.start_time

        seconds = int(elapsed.total_seconds())

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        self.uptime.configure(
            text=f"{h:02}:{m:02}:{s:02}"
        )

        self.after(
            1000,
            self.update_clock
        )