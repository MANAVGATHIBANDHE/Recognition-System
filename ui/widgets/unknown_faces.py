"""
Today's Unknown Faces
Recognition System v2
"""
import customtkinter as ctk
from PIL import Image

import cv2

import os

from services.unknown_queue.queue_service import unknown_queue

from ui.dialogs.person_dialog import PersonDialog

import numpy as np


class UnknownFaces(ctk.CTkScrollableFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.refresh()

    def refresh(self):

        for widget in self.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            self,
            text="Today's Unknown Faces",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            pady=20
        )

        rows = unknown_queue.get_all()

        if not rows:

            empty = ctk.CTkLabel(
                self,
                text="No Unknown Faces"
            )

            empty.pack(pady=50)

            return

        for row in rows:

            uid = row[0]

            photo = row[1]

            embedding_blob = row[2]

            first_seen = row[3]

            last_seen = row[4]

            seen_count = row[5]

            status = row[6]

            embedding = np.frombuffer(

                embedding_blob,

                dtype=np.float32

            )

            face_image = None

            if photo and os.path.exists(photo):

                face_image = cv2.imread(photo)

            card = ctk.CTkFrame(self, corner_radius=12)

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
                padx=(0,20)
            )

            photo_frame.pack_propagate(False)

            if photo and os.path.exists(photo):

                try:

                    image = Image.open(photo)

                    image.thumbnail((110,110), Image.LANCZOS)

                    face = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(110,110)
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

                font=("Segoe UI",20,"bold")

            ).pack(anchor="w")

            ctk.CTkLabel(

                info,

                text=f"First Seen : {first_seen}"

            ).pack(anchor="w", pady=3)

            ctk.CTkLabel(

                info,

                text=f"Last Seen : {last_seen}"

            ).pack(anchor="w", pady=3)

            ctk.CTkLabel(

                info,

                text=f"Seen Count : {seen_count}"

            ).pack(anchor="w", pady=3)

            status_color = {
                "NEW": "#22c55e",
                "PENDING": "#f59e0b",
                "IGNORED": "#ef4444"
            }.get(status, "white")

            ctk.CTkLabel(
                info,
                text=f"Status : {status}",
                text_color=status_color
            ).pack(anchor="w", pady=3)

            buttons = ctk.CTkFrame(card, fg_color="transparent")

            buttons.pack(
                fill="x",
                padx=15,
                pady=(0,15)
            )

            ctk.CTkButton(

                buttons,

                text="Register",

                width=130,

                command=lambda

                img=face_image,

                emb=embedding,

                uid=uid:

                self.register(

                    uid,

                    img,

                    emb

                )

            ).pack(
                side="left",
                padx=(0,8)
            )

            ctk.CTkButton(

                buttons,

                text="Add To Existing",

                width=160

            ).pack(
                side="left",
                padx=5
            )

            ctk.CTkButton(

                buttons,

                text="Ignore",

                width=100,

                command=lambda u=uid:self.ignore(u)

            ).pack(
                side="left",
                padx=5
            )

            ctk.CTkButton(

                buttons,

                text="Delete",

                width=100,

                fg_color="#b91c1c",

                hover_color="#991b1b",

                command=lambda u=uid:self.delete(u)

            ).pack(
                side="left",
                padx=5
            )

    def ignore(self, uid):

        unknown_queue.mark_ignored(uid)

        self.refresh()

    def delete(self, uid):

        unknown_queue.delete(uid)

        self.refresh()

    def register(

        self,

        uid,

        image,

        embedding

    ):

        PersonDialog(

            self.winfo_toplevel(),

            face_image=image,

            embedding=embedding

        )

        unknown_queue.delete(uid)

        self.refresh()