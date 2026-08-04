import customtkinter as ctk
from ui.dialogs.person_dialog import PersonDialog
from PIL import Image

class UnknownPersonDialog(ctk.CTkToplevel):

    def __init__(self, parent, image=None):

        super().__init__(parent)

        self.title("Unknown Person")
        self.geometry("430x500")

        self.grab_set()
        self.face_image = image

        label = ctk.CTkLabel(
            self,
            text="Unknown Person Detected",
            font=("Segoe UI",18,"bold")
        )

        label.pack(pady=(15,10))

        if self.face_image is not None:

            image = Image.fromarray(self.face_image)

            photo = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(170,170)
            )

            preview = ctk.CTkLabel(
                self,
                image=photo,
                text=""
            )

            preview.image = photo

            preview.pack(pady=10)

        ctk.CTkButton(

            self,

            text="Register New",

            command=self.open_registration

        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Maybe Later",
            command=self.maybe_later
        ).pack(
            pady=5
        )

        ctk.CTkButton(

            self,

            text="Ignore",

            command=self.destroy

        ).pack()

    def open_registration(self):

        window = self.master
        PersonDialog(window, face_image=window.camera_widget.last_face_crop, embedding=window.camera_widget.current_embedding)

        self.destroy()

    def maybe_later(self):

        print("Queued for later registration")

        self.destroy()