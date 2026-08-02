"""
Theme Manager

Project:
    Recognition System
"""

import customtkinter as ctk


class ThemeManager:
    """Application theme configuration."""

    @staticmethod
    def initialize() -> None:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")