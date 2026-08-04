import os
import customtkinter as ctk
from PIL import Image
from services.person.person_database import person_database
from services.face.service import face_ai


class FaceGallery(ctk.CTkScrollableFrame):

    def __init__(self, master):
        super().__init__(master)

        self.refresh()

    def refresh(self):

        for widget in self.winfo_children():
            widget.destroy()

        faces = person_database.get_all_persons()

        if len(faces) == 0:

            ctk.CTkLabel(
                self,
                text="No Registered Faces",
                font=("Segoe UI", 18, "bold")
            ).pack(pady=30)

            return

        for row in faces:

            name = row[0]
            image_path = row[1]
            relationship = row[2]
            count = row[3]
            created = row[4]

            card = ctk.CTkFrame(self)

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

            left = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            left.pack(
                side="left",
                padx=15,
                pady=15
            )

            if image_path and os.path.exists(image_path):

                image = Image.open(image_path)

                image = ctk.CTkImage(
                    image,
                    size=(90,90)
                )

                ctk.CTkLabel(
                    left,
                    image=image,
                    text=""
                ).pack()

            else:

                ctk.CTkLabel(
                    left,
                    text="🙂",
                    font=("Segoe UI",40)
                ).pack()

            right = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            right.pack(
                side="left",
                fill="both",
                expand=True,
                padx=10
            )

            ctk.CTkLabel(
                right,
                text=name,
                font=("Segoe UI",18,"bold")
            ).pack(anchor="w")

            ctk.CTkLabel(
                right,
                text= f"{relationship}\nRecognized : {count} times\nRegistered : {created}",
                text_color="gray"
            ).pack(anchor="w")

            ctk.CTkButton(
                right,
                text="Delete",
                fg_color="red",
                command=lambda n=name:self.delete_face(n)
            ).pack(
                anchor="e",
                pady=8
            )

    def delete_face(self,name):

        person_database.delete_person(name)

        face_ai.recognizer.reload()

        self.refresh()