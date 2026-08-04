"""
Dashboard Widget
Recognition System v2.0
"""

from datetime import datetime

import customtkinter as ctk

from services.person.person_database import person_database

class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.start_time = datetime.now()

        self.build_ui()

        self.update_clock()
        self.update_dashboard()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Recognition Dashboard",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=(15, 10))

        self.camera_label = ctk.CTkLabel(
            self,
            text="📷 Camera : Ready",
            font=("Segoe UI", 16)
        )
        self.camera_label.pack(anchor="w", padx=30, pady=5)

        self.database_label = ctk.CTkLabel(
            self,
            text="🗄 Database : Connected",
            font=("Segoe UI", 16)
        )
        self.database_label.pack(anchor="w", padx=30, pady=5)

        self.ai_label = ctk.CTkLabel(
            self,
            text="🧠 AI : Face Recognition Loaded",
            font=("Segoe UI", 16)
        )
        self.ai_label.pack(anchor="w", padx=30, pady=5)

        self.face_label = ctk.CTkLabel(
            self,
            text="🙂 Face Profiles : 0",
            font=("Segoe UI", 16)
        )
        self.face_label.pack(anchor="w", padx=30, pady=5)

        self.voice_label = ctk.CTkLabel(
            self,
            text="🎤 Voice Profiles : 0",
            font=("Segoe UI", 16)
        )
        self.voice_label.pack(anchor="w", padx=30, pady=5)

        self.object_label = ctk.CTkLabel(
            self,
            text="📦 Objects Detected : 0",
            font=("Segoe UI", 16)
        )
        self.object_label.pack(anchor="w", padx=30, pady=5)

        self.recognition_label = ctk.CTkLabel(
            self,
            text="👤 Last Recognition : None",
            font=("Segoe UI", 16)
        )
        self.recognition_label.pack(anchor="w", padx=30, pady=5)

        self.confidence_label = ctk.CTkLabel(
            self,
            text="🎯 Confidence : 0%",
            font=("Segoe UI", 16)
        )
        self.confidence_label.pack(anchor="w", padx=30, pady=5)

        self.uptime = ctk.CTkLabel(
            self,
            text="Uptime : 00:00:00",
            font=("Segoe UI", 16, "bold")
        )
        self.uptime.pack(pady=(10, 15))

    def update_dashboard(self):

        try:
            persons = person_database.get_all_persons()

            self.face_label.configure(
                text=f"🙂 Face Profiles : {len(persons)}"
            )

        except Exception:
            pass

        self.after(2000, self.update_dashboard)

    def set_recognition(self, name, score):

        self.recognition_label.configure(
            text=f"👤 Last Recognition : {name}"
        )

        self.confidence_label.configure(
            text=f"🎯 Confidence : {score*100:.1f}%"
        )

    def update_clock(self):

        elapsed = datetime.now() - self.start_time

        seconds = int(elapsed.total_seconds())

        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        secs = seconds % 60

        self.uptime.configure(
            text=f"Uptime : {hrs:02}:{mins:02}:{secs:02}"
        )

        self.after(1000, self.update_clock)