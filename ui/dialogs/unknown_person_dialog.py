import customtkinter as ctk
from PIL import Image

from ui.dialogs.person_dialog import PersonDialog
from core.logger.logger import app_logger


class UnknownPersonDialog(ctk.CTkToplevel):

    def __init__(self, parent, image=None):

        super().__init__(parent)

        self.title("Unknown Person")
        self.geometry("430x500")

        self.transient(parent)
        self.grab_set()

        self.face_image = image

        self.protocol("WM_DELETE_WINDOW", self.close)

        label = ctk.CTkLabel(
            self,
            text="Unknown Person Detected",
            font=("Segoe UI", 18, "bold")
        )
        label.pack(pady=(15, 10))

        if self.face_image is not None:

            img = Image.fromarray(self.face_image)

            self.preview_image = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=(170, 170)
            )

            preview = ctk.CTkLabel(
                self,
                image=self.preview_image,
                text=""
            )

            preview.pack(pady=10)

        self.register_button = ctk.CTkButton(
            self,
            text="Register New",
            command=self.open_registration
        )
        self.register_button.pack(pady=10)

        self.later_button = ctk.CTkButton(
            self,
            text="Maybe Later",
            command=self.maybe_later
        )
        self.later_button.pack(pady=5)

        self.ignore_button = ctk.CTkButton(
            self,
            text="Ignore",
            command=self.close
        )
        self.ignore_button.pack()

    def close(self):
        try:
            self.grab_release()
        except Exception:
            pass

        if self.winfo_exists():
            self.destroy()

    def open_registration(self):

        if not self.master.winfo_exists():
            self.close()
            return

        window = self.master

        PersonDialog(
            window,
            face_image=window.camera_widget.last_face_crop,
            embedding=window.camera_widget.current_embedding
        )

        self.close()

    def maybe_later(self):
        app_logger.info("Unknown person registration postponed")
        self.close()