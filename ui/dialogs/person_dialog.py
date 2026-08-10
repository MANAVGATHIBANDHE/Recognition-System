"""
Person Registration Dialog
Recognition System v2
"""

import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry

from services.face.service import face_ai
from services.image.image_service import image_service
from services.person.person_service import person_service


class PersonDialog(ctk.CTkToplevel):

    def __init__(self, parent, face_image=None, embedding=None):

        super().__init__(parent)

        self.title("Register Person")
        self.geometry("620x760")
        self.resizable(False, False)

        self.grab_set()

        self.face_image = face_image
        self.embedding = embedding

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Person Registration",
            font=("Segoe UI", 26, "bold")
        ).pack(pady=(20, 15))

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

        self.birthdate = DateEntry(
            self,
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 12)
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

        self.phone = ctk.CTkEntry(
            self,
            placeholder_text="Phone Number"
        )
        self.phone.pack(fill="x", padx=20, pady=8)

        self.email = ctk.CTkEntry(
            self,
            placeholder_text="Email Address"
        )
        self.email.pack(fill="x", padx=20, pady=8)

        self.relationship = ctk.CTkOptionMenu(
            self,
            values=[
                "Family",
                "Friend",
                "Employee",
                "Visitor",
                "Student",
                "Customer",
                "Other"
            ]
        )
        self.relationship.pack(fill="x", padx=20, pady=8)

        self.notes = ctk.CTkTextbox(
            self,
            height=150
        )
        self.notes.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        self.save_button = ctk.CTkButton(
            self,
            text="💾 Save Person",
            height=40,
            command=self.save
        )

        self.save_button.pack(
            pady=(10, 20)
        )

    # ======================================================
    # SAVE
    # ======================================================

    def save(self):

        first_name = self.firstname.get().strip()
        last_name = self.lastname.get().strip()

        if not first_name:

            messagebox.showwarning(
                "Validation",
                "First Name is required."
            )
            return

        self.save_button.configure(state="disabled")

        try:

            photo = None

            if self.face_image is not None:

                photo = image_service.save_profile(
                    self.face_image
                )

            person_service.create_person(

                first_name=first_name,

                middle_name="",

                last_name=last_name,

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

                notes=self.notes.get(
                    "1.0",
                    "end"
                ).strip(),

                photo=photo,

                embedding=self.embedding

            )

            face_ai.recognizer.reload()

            messagebox.showinfo(
                "Success",
                "Person registered successfully."
            )

            self.destroy()

        except Exception as error:

            messagebox.showerror(
                "Registration Failed",
                str(error)
            )

            self.save_button.configure(
                state="normal"
            )