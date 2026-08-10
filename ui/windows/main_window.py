"""
Main Window
Recognition System v2
"""

import customtkinter as ctk

from core.logger.logger import app_logger

from ui.dialogs.person_dialog import PersonDialog

from ui.widgets.dashboard import Dashboard
from ui.widgets.face_gallery import FaceGallery
from ui.widgets.unknown_faces import UnknownFaces


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Recognition System v2")

        self.geometry("1400x850")

        self.minsize(1280, 720)

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.pages = {}
        self.nav_buttons = {}

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        self.build_layout()

    # =========================================================

    def build_layout(self):

        # ---------------- Sidebar ----------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Recognition\nSystem",
            font=("Segoe UI", 28, "bold")
        ).pack(
            pady=(25, 35)
        )

        page_names = [

            "Dashboard",

            "Registered Faces",

            "Today's Unknown Faces",

            "Attendance",

            "Analytics",

            "Object Detection",

            "Voice",

            "Security",

            "Settings"

        ]

        for page in page_names:

            button = ctk.CTkButton(

                self.sidebar,

                text=page,

                width=190,

                command=lambda p=page: self.show_page(p)

            )

            button.pack(
                pady=6
            )

            self.nav_buttons[page] = button

        # ---------------- Content ----------------

        self.content = ctk.CTkFrame(self)

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =====================================================
        # Dashboard
        # =====================================================

        self.dashboard = Dashboard(self.content)

        self.dashboard.place(
            relwidth=1,
            relheight=1
        )

        self.dashboard.register_button.configure(
            command=self.register_face
        )

        self.pages["Dashboard"] = self.dashboard

        # =====================================================
        # Face Gallery
        # =====================================================

        self.face_gallery = FaceGallery(self.content)

        self.face_gallery.place(
            relwidth=1,
            relheight=1
        )

        self.pages["Registered Faces"] = self.face_gallery

        # =====================================================
        # Unknown Faces
        # =====================================================

        self.unknown_faces = UnknownFaces(self.content)

        self.unknown_faces.place(
            relwidth=1,
            relheight=1
        )

        self.pages["Today's Unknown Faces"] = self.unknown_faces

        # =====================================================
        # Placeholder Pages
        # =====================================================

        for name in [

            "Attendance",

            "Analytics",

            "Object Detection",

            "Voice",

            "Security",

            "Settings"

        ]:

            frame = ctk.CTkFrame(self.content)

            frame.place(
                relwidth=1,
                relheight=1
            )

            ctk.CTkLabel(

                frame,

                text=f"{name}\nComing Soon",

                font=("Segoe UI", 30, "bold")

            ).pack(expand=True)

            self.pages[name] = frame

        self.show_page("Dashboard")

    # =========================================================

    def show_page(self, page):

        for frame in self.pages.values():

            frame.lower()

        self.pages[page].lift()

        for button in self.nav_buttons.values():

            button.configure(
                fg_color=("gray75", "#3B8ED0")
            )

        self.nav_buttons[page].configure(
            fg_color="#2563EB"
        )

        if page == "Registered Faces":

            self.face_gallery.refresh()

        elif page == "Today's Unknown Faces":

            self.unknown_faces.refresh()

    # =========================================================

    def register_face(self):

        frame = self.dashboard.camera_widget.current_frame

        face = self.dashboard.camera_widget.last_face_crop

        embedding = self.dashboard.camera_widget.current_embedding

        if frame is None:

            app_logger.warning(
                "Camera frame unavailable."
            )

            return

        dialog = PersonDialog(

            self,

            face_image=face,

            embedding=embedding

        )

        self.wait_window(dialog)

        self.face_gallery.refresh()

    # =========================================================

    def on_close(self):

        self.destroy()