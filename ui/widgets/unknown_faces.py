"""
Unknown Faces
Recognition System v2
"""

import os
import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image

from services.face.service import face_ai
from services.person.person_service import person_service
from services.unknown_queue.queue_service import unknown_queue

from ui.dialogs.person_dialog import PersonDialog
from ui.dialogs.select_person_dialog import SelectPersonDialog


class UnknownFaces(ctk.CTkScrollableFrame):

    def __init__(self, master):

        super().__init__(master)

        self.search_text = ""

        self.refresh()

    # ======================================================

    def refresh(self):

        for widget in self.winfo_children():
            widget.destroy()

        header = ctk.CTkFrame(self)

        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            header,
            text="Today's Unknown Faces",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )

        search = ctk.CTkEntry(
            header,
            width=220,
            placeholder_text="Search UID..."
        )

        search.insert(0, self.search_text)

        search.pack(
            side="right"
        )

        search.bind(
            "<KeyRelease>",
            lambda e: self.search(search.get())
        )

        rows = unknown_queue.get_all()

        if not rows:

            ctk.CTkLabel(
                self,
                text="No Unknown Faces",
                font=("Segoe UI", 20)
            ).pack(
                pady=60
            )

            return

        for row in rows:

            if self.search_text:

                if self.search_text.lower() not in row["uuid"].lower():
                    continue

            uid = row["uuid"]
            photo = row["photo"]
            embedding_blob = row["embedding"]
            first_seen = row["first_seen"]
            last_seen = row["last_seen"]
            seen_count = row["seen_count"]
            status = row["status"]

            if not isinstance(embedding_blob, (bytes, bytearray)):
                continue

            embedding = np.frombuffer(
                embedding_blob,
                dtype=np.float32
            ).copy()

            face_image = None

            if photo and os.path.exists(photo):

                face_image = cv2.imread(photo)

            self.create_card(
                uid,
                photo,
                embedding,
                face_image,
                first_seen,
                last_seen,
                seen_count,
                status
            )

    # ======================================================

    def create_card(
        self,
        uid,
        photo,
        embedding,
        face_image,
        first_seen,
        last_seen,
        seen_count,
        status
    ):

        card = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        card.pack(
            fill="x",
            padx=15,
            pady=10
        )

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=15
        )

        photo_frame = ctk.CTkFrame(
            top,
            width=120,
            height=120
        )

        photo_frame.pack(
            side="left",
            padx=(0, 20)
        )

        photo_frame.pack_propagate(False)

        if photo and os.path.exists(photo):

            try:

                image = Image.open(photo)

                image.thumbnail((110, 110))

                face = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(110, 110)
                )

                label = ctk.CTkLabel(
                    photo_frame,
                    image=face,
                    text=""
                )

                label.image = face

                label.pack(expand=True)

            except Exception:

                ctk.CTkLabel(
                    photo_frame,
                    text="Image Error"
                ).pack(expand=True)

        info = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        info.pack(
            side="left",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            info,
            text=f"Unknown Face #{uid[:8]}",
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"First Seen : {first_seen}"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Last Seen : {last_seen}"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Seen Count : {seen_count}"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Status : {status}"
        ).pack(anchor="w")

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        ctk.CTkButton(
            buttons,
            text="Register",
            command=lambda:
            self.register(
                uid,
                face_image,
                embedding
            )
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Add To Existing",
            command=lambda:
            self.select_person(
                uid,
                embedding
            )
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Ignore",
            command=lambda:
            self.ignore(uid)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Delete",
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=lambda:
            self.delete(uid)
        ).pack(side="left", padx=5)

    # ======================================================

    def search(self, text):

        self.search_text = text

        self.refresh()

    # ======================================================

    def register(
        self,
        uid,
        image,
        embedding
    ):

        dialog = PersonDialog(
            self.winfo_toplevel(),
            face_image=image,
            embedding=embedding
        )

        self.wait_window(dialog)

        face_ai.recognizer.reload()

        unknown_queue.delete(uid)

        self.refresh()

    # ======================================================

    def select_person(
        self,
        uid,
        embedding
    ):

        SelectPersonDialog(
            self.winfo_toplevel(),
            callback=lambda name:
            self.add_existing(
                uid,
                name,
                embedding
            )
        )

    def add_existing(
        self,
        uid,
        name,
        embedding
    ):

        if person_service.add_to_existing(
            name,
            embedding
        ):

            face_ai.recognizer.reload()

            unknown_queue.delete(uid)

            self.refresh()

    # ======================================================

    def ignore(self, uid):

        unknown_queue.mark_ignored(uid)

        self.refresh()

    def delete(self, uid):

        unknown_queue.delete(uid)

        self.refresh()