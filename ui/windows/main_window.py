"""
Main Window
Recognition System
"""

# from core.camera import frame
import customtkinter as ctk

from ui.widgets.dashboard import Dashboard
from ui.widgets.camera_widget import CameraWidget
# from services.camera.manager import camera_service
from ui.widgets.face_gallery import FaceGallery
from ui.dialogs.person_dialog import PersonDialog
from services.watcher.unknown_watcher import unknown_watcher
from ui.dialogs.unknown_person_dialog import UnknownPersonDialog


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Recognition System")
        self.geometry("1200x700")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.unknown_popup = None

        self.build_layout()
        # self.bind_all("<KeyPress-r>", self.register_face_event)
        # self.bind_all("<KeyPress-R>", self.register_face_event)

    def check_unknown(self, name):

        if unknown_watcher.update(name):

            if self.unknown_popup is None or not self.unknown_popup.winfo_exists():

                self.unknown_popup = UnknownPersonDialog(self, self.camera_widget.last_face_crop)

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

        self.register_button = ctk.CTkButton(
            self.dashboard,
            text="➕ Register Person",
            width=220,
            height=38,
            command=self.register_face
        )

        self.register_button.pack(pady=(5, 15))

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
        face_crop = getattr(self.camera_widget, "last_face_crop", None)
        embedding = getattr(self.camera_widget, "current_embedding", None)
        print("Embedding passed to dialog:", embedding is not None)
        print("=" * 50)
        print("MAIN WINDOW")
        print("Embedding:", embedding is not None)

        if embedding is not None:
            print(embedding.shape)

        print("=" * 50)


        if frame is None:
            print("No current frame available")
            return

        try:

            print("Sending frame to trainer...")

            print("=" * 50)

            print("Embedding object:")

            print(embedding)

            print(type(embedding))

            if embedding is not None:
                print(embedding.shape)

            print("=" * 50)

            dialog = PersonDialog(self, face_image=face_crop, embedding=embedding)

            self.wait_window(dialog)

            self.face_gallery.refresh()

        except Exception as e:
            print("ERROR:", e)

    # def register_face_event(self, event):
    #     self.register_face()

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