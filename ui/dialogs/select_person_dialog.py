"""
Select Existing Person Dialog
Recognition System v2
"""

import os

import customtkinter as ctk
from PIL import Image

from services.person.person_service import person_service


class SelectPersonDialog(ctk.CTkToplevel):

    def __init__(self, parent, callback):

        super().__init__(parent)

        self.title("Select Existing Person")
        self.geometry("560x650")
        self.resizable(False, False)

        self.grab_set()

        self.callback = callback
        self.search_text = ""

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(

            self,

            text="Select Existing Person",

            font=("Segoe UI", 24, "bold")

        ).grid(
            row=0,
            column=0,
            pady=(20,10)
        )

        self.search = ctk.CTkEntry(

            self,

            placeholder_text="Search person..."

        )

        self.search.grid(

            row=1,

            column=0,

            sticky="ew",

            padx=20,

            pady=(0,10)

        )

        self.search.bind(

            "<KeyRelease>",

            self.on_search

        )

        self.scroll = ctk.CTkScrollableFrame(self)

        self.scroll.grid(

            row=2,

            column=0,

            sticky="nsew",

            padx=20,

            pady=(0,20)

        )

        self.load_persons()

    # =====================================================
    # SEARCH
    # =====================================================

    def on_search(self, event=None):

        self.search_text = self.search.get().lower()

        self.load_persons()

    # =====================================================
    # LOAD
    # =====================================================

    def load_persons(self):

        for widget in self.scroll.winfo_children():

            widget.destroy()

        persons = person_service.get_all_persons()

        if not persons:

            ctk.CTkLabel(

                self.scroll,

                text="No Registered Persons",

                font=("Segoe UI",18)

            ).pack(
                pady=40
            )

            return

        for person in persons:

            name = person["full_name"]
            photo = person["photo"]
            relationship = person["relationship"]

            if self.search_text:

                if self.search_text not in name.lower():

                    continue

            card = ctk.CTkFrame(

                self.scroll,

                corner_radius=12

            )

            card.pack(

                fill="x",

                pady=6,

                padx=5

            )

            left = ctk.CTkFrame(

                card,

                fg_color="transparent"

            )

            left.pack(
                side="left",
                padx=12,
                pady=10
            )

            if photo and os.path.exists(photo):

                image = Image.open(photo)

                image.thumbnail((60,60))

                img = ctk.CTkImage(

                    light_image=image,

                    dark_image=image,

                    size=(60,60)

                )

                label = ctk.CTkLabel(

                    left,

                    image=img,

                    text=""

                )

                label.image = img

                label.pack()

            else:

                ctk.CTkLabel(

                    left,

                    text="🙂",

                    font=("Segoe UI",32)

                ).pack()

            info = ctk.CTkFrame(

                card,

                fg_color="transparent"

            )

            info.pack(

                side="left",

                fill="both",

                expand=True,

                padx=10

            )

            ctk.CTkLabel(

                info,

                text=name,

                font=("Segoe UI",18,"bold")

            ).pack(anchor="w")

            ctk.CTkLabel(

                info,

                text=relationship,

                text_color="#60a5fa"

            ).pack(anchor="w")

            ctk.CTkButton(

                card,

                text="Select",

                width=100,

                command=lambda n=name:self.select(n)

            ).pack(
                side="right",
                padx=15
            )

    # =====================================================
    # SELECT
    # =====================================================

    def select(self, name):

        self.callback(name)

        self.destroy()