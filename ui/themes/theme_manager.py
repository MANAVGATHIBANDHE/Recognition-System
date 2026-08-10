"""
Theme Manager
Recognition System v2
"""

import customtkinter as ctk

from config.settings import Settings


class ThemeManager:
    """
    Centralized UI theme manager.
    """

    _THEMES = {
        "blue": "blue",
        "green": "green",
        "dark-blue": "dark-blue"
    }

    @classmethod
    def load(cls):

        appearance = getattr(
            Settings,
            "THEME",
            "dark"
        ).lower()

        if appearance not in ("dark", "light", "system"):
            appearance = "dark"

        ctk.set_appearance_mode(
            appearance.capitalize()
            if appearance != "system"
            else "System"
        )

        ctk.set_default_color_theme(
            cls._THEMES["blue"]
        )

    @classmethod
    def set_appearance(cls, mode: str):

        mode = mode.lower()

        if mode not in (
            "dark",
            "light",
            "system"
        ):
            return

        ctk.set_appearance_mode(
            mode.capitalize()
            if mode != "system"
            else "System"
        )

    @classmethod
    def set_theme(cls, theme: str):

        theme = theme.lower()

        if theme not in cls._THEMES:
            return

        ctk.set_default_color_theme(
            cls._THEMES[theme]
        )

    @classmethod
    def available_themes(cls):

        return list(cls._THEMES.keys())