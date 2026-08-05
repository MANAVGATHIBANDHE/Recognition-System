"""
Main Window
Recognition System
"""

import customtkinter as ctk
from core.logger.logger import app_logger
from ui.widgets.dashboard import Dashboard
from ui.widgets.camera_widget import CameraWidget
from ui.widgets.face_gallery import FaceGallery
from ui.widgets.unknown_faces import UnknownFaces
from ui.dialogs.person_dialog import PersonDialog


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
            "Registered Faces",
            "Today's Unknown Faces",
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

        self.register_button = ctk.CTkButton(
            self.dashboard,
            text="➕ Register Person",
            width=220,
            height=38,
            command=self.register_face
        )

        self.register_button.pack(pady=(5, 15))

        self.face_gallery = FaceGallery(self.content)

        self.unknown_faces = UnknownFaces(self.content)

    def register_face(self):

        frame = getattr(self.camera_widget, "current_frame", None)
        face_crop = getattr(self.camera_widget, "last_face_crop", None)
        embedding = getattr(self.camera_widget, "current_embedding", None)


        if frame is None:
            app_logger.warning("No camera frame available.")
            return

        try:
            dialog = PersonDialog(self, face_image=face_crop, embedding=embedding)

            self.wait_window(dialog)

            self.face_gallery.refresh()

        except Exception as e:
            app_logger.exception(e)

    def change_page(self, page):

        self.dashboard.pack_forget()
        self.face_gallery.pack_forget()
        self.unknown_faces.pack_forget()

        if page == "Dashboard":

            self.dashboard.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

        elif page == "Registered Faces":

            self.face_gallery.refresh()

            self.face_gallery.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=20
            )

        elif page == "Today's Unknown Faces":

            self.unknown_faces.refresh()

            self.unknown_faces.pack(
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