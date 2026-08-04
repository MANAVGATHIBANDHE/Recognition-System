import customtkinter as ctk

from services.person.person_service import person_service
from services.image.image_service import image_service
from services.face.service import face_ai


class PersonDialog(ctk.CTkToplevel):

    def __init__(self, parent, face_image=None, embedding=None):

        super().__init__(parent)

        self.title("Register Person")
        self.geometry("600x700")

        self.grab_set()

        self.face_image = face_image
        self.embedding = embedding

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Person Registration",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=20)

        self.firstname = ctk.CTkEntry(
            self,
            placeholder_text="First Name"
        )
        self.firstname.pack(fill="x", padx=20, pady=8)

        self.lastname = ctk.CTkEntry(
            self,
            placeholder_text="Last Name"
        )
        self.lastname.pack(fill="x", padx=20, pady=8)

        self.birthdate = ctk.CTkEntry(
            self,
            placeholder_text="Birth Date (DD/MM/YYYY)"
        )
        self.birthdate.pack(fill="x", padx=20, pady=8)

        self.gender = ctk.CTkOptionMenu(
            self,
            values=[
                "Male",
                "Female",
                "Other"
            ]
        )
        self.gender.pack(fill="x", padx=20, pady=8)

        self.address = ctk.CTkEntry(
            self,
            placeholder_text="Address"
        )
        self.address.pack(fill="x", padx=20, pady=8)

        self.phone = ctk.CTkEntry(
            self,
            placeholder_text="Phone"
        )
        self.phone.pack(fill="x", padx=20, pady=8)

        self.email = ctk.CTkEntry(
            self,
            placeholder_text="Email"
        )
        self.email.pack(fill="x", padx=20, pady=8)

        self.relationship = ctk.CTkEntry(
            self,
            placeholder_text="Relationship (Friend, Family...)"
        )
        self.relationship.pack(fill="x", padx=20, pady=8)

        self.notes = ctk.CTkTextbox(
            self,
            height=120
        )
        self.notes.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkButton(
            self,
            text="Save",
            command=self.save
        ).pack(pady=20)

    def save(self):

        photo = None

        if self.face_image is not None:

            photo = image_service.save_profile(
                self.face_image
            )

        person_service.create_person(

            first_name=self.firstname.get(),

            middle_name="",

            last_name=self.lastname.get(),

            gender=self.gender.get(),

            dob=self.birthdate.get(),

            phone=self.phone.get(),

            email=self.email.get(),

            house="",

            area="",

            city="",

            state="",

            country="",

            postal_code="",

            occupation="",

            relationship=self.relationship.get(),

            tags="",

            notes=self.notes.get("1.0","end").strip(),

            photo=photo,

            embedding=self.embedding

        )

        face_ai.recognizer.reload()

        self.destroy()
