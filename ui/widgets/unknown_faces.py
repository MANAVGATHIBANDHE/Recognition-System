"""
Today's Unknown Faces
Recognition System v2
"""

import customtkinter as ctk

from services.unknown_queue.queue_service import unknown_queue


class UnknownFaces(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.build_ui()

        self.refresh()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Today's Unknown Faces",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            pady=(20, 10)
        )

        self.count_label = ctk.CTkLabel(
            self,
            text="Unknown Faces : 0",
            font=("Segoe UI", 16)
        )

        self.count_label.pack(
            pady=(0, 20)
        )

        self.scroll = ctk.CTkScrollableFrame(
            self,
            width=900,
            height=520
        )

        self.scroll.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

    def refresh(self):

        for widget in self.scroll.winfo_children():
            widget.destroy()

        rows = unknown_queue.get_all()

        self.count_label.configure(
            text=f"Unknown Faces : {len(rows)}"
        )

        for row in rows:

            uid, photo, first_seen, last_seen, seen_count, status = row

            card = ctk.CTkFrame(
                self.scroll
            )

            card.pack(
                fill="x",
                padx=10,
                pady=8
            )

            ctk.CTkLabel(
                card,
                text=f"ID : {uid[:8]}",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 2)
            )

            ctk.CTkLabel(
                card,
                text=f"First Seen : {first_seen}",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                card,
                text=f"Last Seen : {last_seen}",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                card,
                text=f"Seen Count : {seen_count}",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15
            )

            ctk.CTkLabel(
                card,
                text=f"Status : {status}",
                anchor="w"
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )

        self.after(
            2000,
            self.refresh
        )