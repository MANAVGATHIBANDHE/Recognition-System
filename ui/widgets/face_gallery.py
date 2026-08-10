"""
Professional Face Gallery
Recognition System v2
"""

import os

import customtkinter as ctk
from PIL import Image

from services.face.service import face_ai
from services.person.person_database import person_database


class FaceGallery(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master)

        self.search_text = ""

        self.build_header()

        self.refresh()

    # ==========================================================
    # HEADER
    # ==========================================================

    def build_header(self):

        header = ctk.CTkFrame(self)

        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            header,
            text="Registered Faces",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left",
            padx=15
        )

        self.search = ctk.CTkEntry(
            header,
            width=260,
            placeholder_text="Search person..."
        )

        self.search.pack(
            side="right",
            padx=15
        )

        self.search.bind(
            "<KeyRelease>",
            self.on_search
        )

    # ==========================================================

    def on_search(self, event=None):

        self.search_text = self.search.get().lower()

        self.refresh()

    # ==========================================================

    def refresh(self):

        widgets = self.winfo_children()[1:]

        for widget in widgets:

            widget.destroy()

        persons = person_database.get_all_persons()

        if not persons:

            ctk.CTkLabel(
                self,
                text="No Registered Faces",
                font=("Segoe UI", 20, "bold")
            ).pack(
                pady=40
            )

            return

        total = 0

        for row in persons:

            name = row[0]
            photo = row[1]
            relationship = row[2]
            count = row[3]
            created = row[4]

            if self.search_text:

                if self.search_text not in name.lower():

                    continue

            total += 1

            self.create_card(
                name,
                photo,
                relationship,
                count,
                created
            )

        ctk.CTkLabel(
            self,
            text=f"{total} Registered Face(s)",
            text_color="gray"
        ).pack(
            pady=15
        )

    # ==========================================================

    def create_card(
        self,
        name,
        photo,
        relationship,
        count,
        created
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        card.pack(
            fill="x",
            padx=15,
            pady=8
        )

        # ---------------- Photo ----------------

        left = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            padx=20,
            pady=15
        )

        if photo and os.path.exists(photo):

            image = Image.open(photo)

            image.thumbnail((90, 90))

            face = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(90, 90)
            )

            label = ctk.CTkLabel(
                left,
                image=face,
                text=""
            )

            label.image = face

            label.pack()

        else:

            ctk.CTkLabel(
                left,
                text="🙂",
                font=("Segoe UI", 42)
            ).pack()

        # ---------------- Info ----------------

        info = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=15
        )

        ctk.CTkLabel(
            info,
            text=name,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Relationship : {relationship}",
            text_color="#60A5FA"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Recognized : {count}",
            text_color="gray"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Registered : {created}",
            text_color="gray"
        ).pack(anchor="w")

        # ---------------- Actions ----------------

        actions = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        actions.pack(
            side="right",
            padx=20
        )

        ctk.CTkButton(
            actions,
            text="Delete",
            width=110,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=lambda n=name: self.delete_face(n)
        ).pack(
            pady=25
        )

    # ==========================================================

    def delete_face(self, name):

        person_database.delete_person(name)

        face_ai.recognizer.reload()

        self.refresh()