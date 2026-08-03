"""
Main Window
Recognition System
"""

from core.camera import frame
import customtkinter as ctk

from ui.widgets.dashboard import Dashboard
from ui.widgets.camera_widget import CameraWidget
from services.face.trainer import face_trainer
from services.camera.manager import camera_service
from ui.widgets.face_gallery import FaceGallery


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Recognition System")
        self.geometry("1200x700")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.build_layout()
        self.bind_all("<KeyPress-r>", self.register_face_event)
        self.bind_all("<KeyPress-R>", self.register_face_event)

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
                width=180,
                command=lambda n=name: self.change_page(n)
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

        self.dashboard = Dashboard(self.content)

        self.dashboard.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.camera_widget = CameraWidget(self.dashboard)
        self.camera_widget.focus_set()

        self.camera_widget.pack(
            pady=20
        )

        self.face_gallery = FaceGallery(self.content)

        # self.register_btn = ctk.CTkButton(
        #     self.content,
        #     text="Register My Face",
        #     command=self.register_face
        # )

        # self.register_btn.pack(pady=10)

    def register_face(self):

        print("Register button/key pressed")

        frame = getattr(self.camera_widget, "current_frame", None)

        if frame is None:
            print("No current frame available")
            return

        try:

            print("Sending frame to trainer...")

            success = face_trainer.register(frame, "Manav")

            if success:
                self.face_gallery.refresh()
                print("✅ Manav Registered Successfully")
            else:
                print("❌ No face found")

        except Exception as e:
            print("ERROR:", e)

    def register_face_event(self, event):
        self.register_face()

    def change_page(self, page):

        self.dashboard.pack_forget()
        self.face_gallery.pack_forget()

        if page == "Dashboard":

            self.dashboard.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

        elif page == "Face":

            self.face_gallery.refresh()

            self.face_gallery.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

        else:

            self.dashboard.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )


    def refresh_gallery(self):

        self.face_gallery.refresh()