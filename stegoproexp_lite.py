import base64
import hashlib
import json
import mimetypes
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import wave
import webbrowser
import zlib
from datetime import datetime, timedelta
from io import BytesIO
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import List, Tuple, Dict, Any

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numba
import numpy as np
from PIL import Image
from PIL import ImageTk
from scipy import ndimage
from scipy.fftpack import dct, idct
from scipy.stats import binomtest, kurtosis, skew, normaltest
from tkinterdnd2 import DND_FILES, TkinterDnD
from Crypto.Cipher import AES, ChaCha20, ChaCha20_Poly1305
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ───────────────────────────────────────────────
# 🎨 ГЛОБАЛЬНЫЕ НАСТРОЙКИ (УЛУЧШЕННЫЕ)
# ───────────────────────────────────────────────
VERSION = "2.4.1 lite"
AUTHOR = "MustaNG"
BUILD_DATE = time.strftime("%Y-%m-%d")

# Константы для LSB-метода
HEADER_SIZE_BITS = 32  # Размер заголовка (биты)
PROGRESS_UPDATE_INTERVAL = 1000  # Частота обновления прогресса (биты)
MIN_DATA_LEN = 8  # Минимальный размер данных (биты)
MAX_DATA_LEN = 100 * 1024 * 1024 * 8  # Максимальный размер данных (100 МБ в битах)

THEMES = {
    "Тёмная": {
        "name": "Тёмная",
        "bg": "#0B1220",
        "fg": "#E6EDF6",
        "accent": "#4C8DFF",
        "accent_hover": "#6AA8FF",
        "accent_pressed": "#3B7CF2",
        "secondary": "#111827",
        "success": "#3FDA87",
        "error": "#FF6B6B",
        "warning": "#F0B23E",
        "card": "#0E1726",
        "border": "#253044",
        "text": "#E6EDF6",
        "text_secondary": "#94A3B8",
        "disabled": "#55637A",
        "scrollbar": "#243244",
        "highlight": "#1C273A",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Светлая": {
        "name": "Светлая",
        "bg": "#F7F9FC",
        "fg": "#0F172A",
        "accent": "#2563EB",
        "accent_hover": "#3B82F6",
        "accent_pressed": "#1D4ED8",
        "secondary": "#FFFFFF",
        "success": "#16A34A",
        "error": "#DC2626",
        "warning": "#D97706",
        "card": "#FFFFFF",
        "border": "#E2E8F0",
        "text": "#0F172A",
        "text_secondary": "#64748B",
        "disabled": "#A3AEC2",
        "scrollbar": "#CBD5E1",
        "highlight": "#E8F1FF",
        "shadow": "#DDE3EC",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Космос": {
        "name": "Космос",
        "bg": "#0B1020",
        "fg": "#CDE7FF",
        "accent": "#7C3AED",
        "accent_hover": "#9D5CFF",
        "accent_pressed": "#6D28D9",
        "secondary": "#11162A",
        "success": "#22D3EE",
        "error": "#FB7185",
        "warning": "#FBBF24",
        "card": "#0F1530",
        "border": "#232B47",
        "text": "#D7EEFF",
        "text_secondary": "#8393B2",
        "disabled": "#3B4470",
        "scrollbar": "#1C2446",
        "highlight": "#1A2142",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Океан": {
        "name": "Океан",
        "bg": "#021A2E",
        "fg": "#CDEBFF",
        "accent": "#0EA5E9",
        "accent_hover": "#38BDF8",
        "accent_pressed": "#0284C7",
        "secondary": "#03243F",
        "success": "#34D399",
        "error": "#F87171",
        "warning": "#F59E0B",
        "card": "#062B4A",
        "border": "#0B3B63",
        "text": "#CDEBFF",
        "text_secondary": "#8DB8D6",
        "disabled": "#2A5877",
        "scrollbar": "#0D3355",
        "highlight": "#0A2F54",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Лес": {
        "name": "Лес",
        "bg": "#0D1A11",
        "fg": "#D6F5DE",
        "accent": "#22C55E",
        "accent_hover": "#4ADE80",
        "accent_pressed": "#16A34A",
        "secondary": "#102418",
        "success": "#84CC16",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "card": "#0F2616",
        "border": "#224A2F",
        "text": "#D8F7E0",
        "text_secondary": "#91C3A2",
        "disabled": "#416D54",
        "scrollbar": "#1B3A2A",
        "highlight": "#12301E",
        "shadow": "#000000",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Ночная Неонка": {
        "name": "Ночная Неонка",
        "bg": "#0D0B21",
        "fg": "#F7F7FF",
        "accent": "#FF2EA8",
        "accent_hover": "#FF64C3",
        "accent_pressed": "#DB158E",
        "secondary": "#1B1841",
        "success": "#00E6A8",
        "error": "#FF5A7A",
        "warning": "#FFD166",
        "card": "#221E56",
        "border": "#3B3784",
        "text": "#F7F7FF",
        "text_secondary": "#C8C8F0",
        "disabled": "#6A67B2",
        "scrollbar": "#2B2770",
        "highlight": "#2A2671",
        "shadow": "#000000",
        "radius": 14,
        "padding": 14,
        "border_width": 1,
        "animation_speed": 0.05
    },
    "Солнечный Закат": {
        "name": "Солнечный Закат",
        "bg": "#FFF9F4",
        "fg": "#1F2937",
        "accent": "#FB6A63",
        "accent_hover": "#FF8B85",
        "accent_pressed": "#E1544E",
        "secondary": "#FFFFFF",
        "success": "#10B981",
        "error": "#EF4444",
        "warning": "#F59E0B",
        "card": "#FFFFFF",
        "border": "#EAD7CC",
        "text": "#1F2937",
        "text_secondary": "#6B7280",
        "disabled": "#B8BDC7",
        "scrollbar": "#E5D7CD",
        "highlight": "#FFEDE6",
        "shadow": "#EAD7CC",
        "radius": 12,
        "padding": 12,
        "border_width": 1,
        "animation_speed": 0.1
    },
    "Киберпанк": {
        "name": "Киберпанк",
        "bg": "#0A0A0A",
        "fg": "#00FF41",
        "accent": "#FF00FF",
        "accent_hover": "#FF33FF",
        "accent_pressed": "#CC00CC",
        "secondary": "#1A1A1A",
        "success": "#00FF41",
        "error": "#FF3333",
        "warning": "#FFFF00",
        "card": "#151515",
        "border": "#333333",
        "text": "#E0E0E0",
        "text_secondary": "#808080",
        "disabled": "#555555",
        "scrollbar": "#222222",
        "highlight": "#2A2A2A",
        "shadow": "#000000",
        "radius": 8,
        "padding": 10,
        "border_width": 2,
        "animation_speed": 0.05
    },
    "Матовый": {
        "name": "Матовый",
        "bg": "#2D3748",
        "fg": "#E2E8F0",
        "accent": "#4299E1",
        "accent_hover": "#63B3ED",
        "accent_pressed": "#3182CE",
        "secondary": "#4A5568",
        "success": "#68D391",
        "error": "#FC8181",
        "warning": "#F6E05E",
        "card": "#2D3748",
        "border": "#4A5568",
        "text": "#E2E8F0",
        "text_secondary": "#A0AEC0",
        "disabled": "#718096",
        "scrollbar": "#4A5568",
        "highlight": "#374151",
        "shadow": "#1A202C",
        "radius": 6,
        "padding": 8,
        "border_width": 1,
        "animation_speed": 0.2
    }
}

SUPPORTED_FORMATS = [
    ("Все поддерживаемые форматы", "*.png *.bmp *.tiff *.tga *.jpg *.jpeg *.wav"),
    ("Изображения PNG", "*.png"),
    ("Изображения BMP", "*.bmp"),
    ("Изображения TIFF", "*.tiff *.tif"),
    ("Изображения TGA", "*.tga"),
    ("Изображения JPG/JPEG", "*.jpg *.jpeg"),
    ("Аудио WAV", "*.wav"),
    ("Все файлы", "*.*")
]

STEGANO_METHODS = {
    "lsb": "Классический LSB (Макс. вместимость)",
    "noise": "Adaptive-Noise (Баланс вместимости/скрытности)",
    "aelsb": "Adaptive-Edge-LSB + Hamming (Устойчивость к ошибкам)",
    "hill": "HILL-CA LSB Matching (Макс. скрытность)",
    "audio_lsb": "WAV LSB (Аудио-WAV контейнеры)",
    "jpeg_dct": "JPEG DCT"
}

SETTINGS_FILE = "stego_settings_pro.json"
HISTORY_FILE = "stego_history_pro.json"
MAX_HISTORY = 20
MAX_FILE_SIZE_MB = 100

CONFIG = {
    "MAX_FILE_SIZE_MB": MAX_FILE_SIZE_MB,
    "SETTINGS_FILE": SETTINGS_FILE,
    "HISTORY_FILE": HISTORY_FILE,
    "AUTO_SAVE_INTERVAL": 300,  # Автосохранение каждые 5 минут
    "ANIMATION_SPEED": 0.2,
    "TOAST_DURATION": 3000,
    "MAX_UNDO_HISTORY": 5
}


# ───────────────────────────────────────────────
# 🛠️ УТИЛИТЫ
# ───────────────────────────────────────────────
class Utils:
    @staticmethod
    def safe_int(s: str, fallback: int = 0) -> int:
        try:
            return int(s)
        except (ValueError, TypeError):
            return fallback

    @staticmethod
    def truncate_path(path: str, max_len: int = 40) -> str:
        if len(path) <= max_len:
            return path
        return "..." + path[-(max_len - 3):]

    @staticmethod
    def format_size(size_bytes: int) -> str:
        if size_bytes < 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    @staticmethod
    def is_supported_container(path: str) -> bool:
        ext = os.path.splitext(path)[1].lower()
        if ext == '.wav':
            try:
                with wave.open(path, 'rb'):
                    return True
            except Exception:
                return False
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_checksum(file_path: str) -> str:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    @staticmethod
    def get_free_space_mb(path: str) -> float:
        """Получает свободное место на диске в МБ"""
        try:
            if os.name == 'nt':  # Windows
                import ctypes
                free_bytes = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                    ctypes.c_wchar_p(path),
                    ctypes.pointer(free_bytes),
                    None,
                    None
                )
                return free_bytes.value / (1024 * 1024)
            else:  # Unix
                statvfs = os.statvfs(path)
                return (statvfs.f_frsize * statvfs.f_bavail) / (1024 * 1024)
        except Exception:
            return float('inf')  # Если не удалось определить, считаем, что места достаточно

    @staticmethod
    def check_file_signature(file_path: str, expected_signatures: List[bytes]) -> bool:
        """Проверяет сигнатуру файла"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                return any(header.startswith(sig) for sig in expected_signatures)
        except Exception:
            return False

    @staticmethod
    def calculate_brightness(color: str) -> float:
        """Рассчитывает яркость цвета по формуле WCAG"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        # sRGB to linear RGB
        def srgb_to_linear(c):
            c = c / 255.0
            if c <= 0.03928:
                return c / 12.92
            else:
                return ((c + 0.055) / 1.055) ** 2.4

        r_lin = srgb_to_linear(r)
        g_lin = srgb_to_linear(g)
        b_lin = srgb_to_linear(b)
        # Relative luminance
        L = 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin
        return L

    @staticmethod
    def get_contrast_ratio(color1: str, color2: str) -> float:
        """Рассчитывает коэффициент контраста между двумя цветами"""
        L1 = Utils.calculate_brightness(color1)
        L2 = Utils.calculate_brightness(color2)
        if L1 > L2:
            return (L1 + 0.05) / (L2 + 0.05)
        else:
            return (L2 + 0.05) / (L1 + 0.05)

    @staticmethod
    def open_in_file_manager(path: str) -> None:
        """Открывает файл или папку в системном проводнике."""
        try:
            if os.path.isfile(path):
                directory = os.path.dirname(path) or "."
            else:
                directory = path or "."
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', directory])
            elif os.name == 'nt':
                os.startfile(directory)
            else:
                subprocess.call(['xdg-open', directory])
        except Exception as e:
            print(f"Не удалось открыть проводник: {e}")

    @staticmethod
    def open_in_default_app(path: str) -> None:
        """Открывает файл в приложении по умолчанию."""
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(['open', path])
            elif os.name == 'nt':
                os.startfile(path)
            else:
                subprocess.call(['xdg-open', path])
        except Exception as e:
            print(f"Не удалось открыть файл: {e}")

    @staticmethod
    def get_file_info(path: str) -> dict:
        """Получает расширенную информацию о файле"""
        try:
            stat = os.stat(path)
            size = stat.st_size
            created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime))
            modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
            ext = os.path.splitext(path)[1].lower()

            info = {
                "name": os.path.basename(path),
                "size": size,
                "size_formatted": Utils.format_size(size),
                "created": created,
                "modified": modified,
                "extension": ext,
                "type": "unknown"
            }

            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga']:
                info["type"] = "image"
                try:
                    with Image.open(path) as img:
                        info["dimensions"] = f"{img.width}x{img.height}"
                        info["mode"] = img.mode
                except:
                    pass
            elif ext == '.wav':
                info["type"] = "audio"
                try:
                    with wave.open(path, 'rb') as wav:
                        info["channels"] = wav.getnchannels()
                        info["sample_rate"] = wav.getframerate()
                        info["frames"] = wav.getnframes()
                        duration = wav.getnframes() / wav.getframerate()
                        info["duration"] = f"{int(duration // 60)}:{int(duration % 60):02d}"
                except:
                    pass
            else:
                info["type"] = "file"

            return info
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def create_backup(file_path: str, max_backups: int = 5) -> str:
        """Создает резервную копию файла"""
        try:
            if not os.path.exists(file_path):
                return ""

            backup_dir = os.path.join(os.path.dirname(file_path), "backups")
            os.makedirs(backup_dir, exist_ok=True)

            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)

            # Удаляем старые бэкапы если их больше max_backups
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith(name + "_backup_")]
            backup_files.sort(reverse=True)  # Сортируем по убыванию

            if len(backup_files) >= max_backups:
                for old_backup in backup_files[max_backups - 1:]:
                    os.remove(os.path.join(backup_dir, old_backup))

            # Создаем новое имя для бэкапа
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = f"{name}_backup_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_name)

            # Копируем файл
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Ошибка создания бэкапа: {e}")
            return ""

    @staticmethod
    def get_system_info() -> dict:
        """Получает информацию о системе"""
        import platform
        return {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "working_directory": os.getcwd(),
            "home_directory": os.path.expanduser("~")
        }


# ───────────────────────────────────────────────
# 🛈 КЛАСС ПОДСКАЗОК (TOOLTIP)
# ───────────────────────────────────────────────
class ToolTip:
    def __init__(self, widget, text, bg="#333333", fg="#ffffff", delay=500, follow_mouse=True):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.bg = bg
        self.fg = fg
        self.follow_mouse = follow_mouse
        self.tipwindow = None
        self._after_id = None
        self._mouse_x = 0
        self._mouse_y = 0

        self.widget.bind("<Enter>", self._schedule, add="+")
        self.widget.bind("<Leave>", self._unschedule, add="+")
        self.widget.bind("<Button-1>", self._unschedule, add="+")
        if follow_mouse:
            self.widget.bind("<Motion>", self._update_position, add="+")

    def _schedule(self, event=None):
        if event:
            self._mouse_x = event.x_root
            self._mouse_y = event.y_root
        self._after_id = self.widget.after(self.delay, self._show)

    def _unschedule(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        self._hide()

    def _update_position(self, event):
        self._mouse_x = event.x_root
        self._mouse_y = event.y_root
        if self.tipwindow:
            self._update_tip_position()

    def _update_tip_position(self):
        if self.tipwindow:
            x = self._mouse_x + 20
            y = self._mouse_y + 10
            self.tipwindow.wm_geometry(f"+{x}+{y}")

    def _show(self):
        if self.tipwindow or not self.text:
            return

        if self.follow_mouse:
            x = self._mouse_x + 20
            y = self._mouse_y + 10
        else:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)

        # Создаем фрейм с закругленными углами (эмуляция)
        frame = tk.Frame(tw, background=self.bg, padx=1, pady=1)
        frame.pack(fill="both", expand=True)

        label = tk.Label(frame, text=self.text, justify=tk.LEFT,
                         background=self.bg, foreground=self.fg,
                         relief=tk.FLAT, font=("Segoe UI", 9),
                         padx=8, pady=6)
        label.pack(fill="both", expand=True)

        tw.wm_geometry(f"+{x}+{y}")

        # Добавляем тень (эмуляция)
        tw.attributes("-alpha", 0.95)

    def _hide(self):
        tw = self.tipwindow
        if tw:
            tw.destroy()
            self.tipwindow = None


# ───────────────────────────────────────────────
# 🎨 КЛАСС ДЛЯ РАБОТЫ С ТЕМАМИ
# ───────────────────────────────────────────────
class ThemeManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style()
        self.current_theme = "Тёмная"
        self.colors = THEMES[self.current_theme]
        self.animations = {}

    def set_theme(self, theme_name: str) -> None:
        if theme_name not in THEMES:
            theme_name = "Тёмная"
        self.current_theme = theme_name
        self.colors = THEMES[theme_name]
        self._configure_styles()
        self._apply_theme_to_existing_widgets()

    def _apply_theme_to_existing_widgets(self):
        """Применяет тему ко всем существующим виджетам"""

        def apply_to_widget(widget):
            try:
                if isinstance(widget, (ttk.Button, ttk.Label, ttk.Entry, ttk.Combobox)):
                    widget.update_idletasks()
                elif isinstance(widget, tk.Text):
                    widget.configure(
                        bg=self.colors["card"],
                        fg=self.colors["text"],
                        insertbackground=self.colors["text"],
                        selectbackground=self.colors["accent"],
                        selectforeground="#ffffff"
                    )
                elif isinstance(widget, tk.Label):
                    widget.configure(
                        bg=self.colors["bg"],
                        fg=self.colors["text"]
                    )
            except:
                pass

        def traverse_children(parent):
            for child in parent.winfo_children():
                apply_to_widget(child)
                if hasattr(child, 'winfo_children'):
                    traverse_children(child)

        traverse_children(self.root)

    def _configure_styles(self) -> None:
        c = self.colors
        radius = c.get("radius", 10)
        padding = c.get("padding", 10)
        border_width = c.get("border_width", 1)

        self.root.configure(bg=c["bg"])
        self.style.theme_use("clam")

        # Базовые установки
        self.style.configure(".", background=c["bg"], foreground=c["text"], font=("Segoe UI", 10))

        # Notebook (вкладки)
        self.style.configure("TNotebook", background=c["bg"], borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background=c["secondary"],
            foreground=c["text_secondary"],
            padding=(padding, padding - 2),
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", c["card"]), ("active", c["highlight"])],
            foreground=[("selected", c["text"]), ("active", c["text"])]
        )

        # Кнопки (обычные)
        self.style.configure(
            "TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding, padding - 2),
            borderwidth=border_width,
            bordercolor=c["border"],
            focusthickness=2,
            focuscolor=c["accent"]
        )
        self.style.map(
            "TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])],
            foreground=[("disabled", c["disabled"]), ("pressed", "#ffffff")],
            bordercolor=[("focus", c["accent"])]
        )

        # Кнопки (акцентные)
        self.style.configure(
            "Accent.TButton",
            background=c["accent"],
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(padding + 2, padding - 1),
            borderwidth=0,
            relief="flat",
            focusthickness=3,
            focuscolor=c["accent_hover"]
        )
        self.style.map(
            "Accent.TButton",
            background=[("active", c["accent_hover"]), ("pressed", c["accent_pressed"])],
            foreground=[("disabled", c["disabled"])]
        )

        # Кнопки-иконки (в шапке и рядом), чуть более «плоские»
        self.style.configure(
            "IconButton.TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding - 3, padding - 5),
            borderwidth=border_width,
            bordercolor=c["border"]
        )
        self.style.map(
            "IconButton.TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent"])],
            foreground=[("pressed", "#ffffff")]
        )

        # Кнопки действий (извлечь/сохранить/копировать)
        self.style.configure(
            "Action.TButton",
            background=c["secondary"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding, padding - 2),
            borderwidth=border_width,
            bordercolor=c["border"],
            focusthickness=2,
            focuscolor=c["accent"]
        )
        self.style.map(
            "Action.TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])],
            foreground=[("pressed", "#ffffff")]
        )

        # Карточки
        self.style.configure("Card.TFrame", background=c["card"])
        self.style.configure(
            "Card.TLabelframe",
            background=c["card"],
            borderwidth=border_width,
            relief="solid",
            bordercolor=c["border"],
            lightcolor=c["card"],
            darkcolor=c["card"]
        )
        self.style.configure(
            "Card.TLabelframe.Label",
            background=c["card"],
            foreground=c["text"],
            font=("Segoe UI", 10, "bold"),
            padding=(4, 0)
        )

        # Метки
        self.style.configure("TLabel", background=c["bg"], foreground=c["text"], font=("Segoe UI", 10))
        self.style.configure("Secondary.TLabel", background=c["bg"], foreground=c["text_secondary"],
                             font=("Segoe UI", 9))

        # Заголовки блоков
        self.style.configure("GroupHeader.TLabel",
                             background=c["bg"], foreground=c["accent"], font=("Segoe UI", 12, "bold"))

        # Поля ввода
        self.style.configure(
            "TEntry",
            fieldbackground=c["card"],
            foreground=c["text"],
            insertcolor=c["text"],
            bordercolor=c["border"],
            lightcolor=c["card"],
            darkcolor=c["card"],
            relief="flat",
            borderwidth=border_width,
            padding=(padding - 4, padding - 6)
        )
        self.style.map(
            "TEntry",
            bordercolor=[("focus", c["accent"])],
            lightcolor=[("focus", c["card"])],
            darkcolor=[("focus", c["card"])]
        )

        # Выпадающие списки
        self.style.configure(
            "TCombobox",
            fieldbackground=c["card"],
            foreground=c["text"],
            selectbackground=c["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=border_width,
            padding=(padding - 6, padding - 6),
            arrowsize=13,
            bordercolor=c["border"]
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", c["card"])],
            bordercolor=[("focus", c["accent"])]
        )

        # Текстовые поля (ScrolledText)
        self.style.configure("TText",
                             background=c["card"],
                             foreground=c["text"],
                             insertbackground=c["text"],
                             selectbackground=c["accent"],
                             selectforeground="#ffffff",
                             relief="flat",
                             borderwidth=border_width)

        # Прогресс-бар
        self.style.configure(
            "TProgressbar",
            background=c["accent"],
            troughcolor=c["secondary"],
            bordercolor=c["border"],
            lightcolor=c["accent"],
            darkcolor=c["accent"],
            thickness=14
        )

        # Доп. стили прогресс-бара для индикатора заполнения
        self.style.configure(
            "UsageGreen.Horizontal.TProgressbar",
            background=c["success"],
            troughcolor=c["secondary"],
            thickness=12
        )
        self.style.configure(
            "UsageYellow.Horizontal.TProgressbar",
            background=c["warning"],
            troughcolor=c["secondary"],
            thickness=12
        )
        self.style.configure(
            "UsageRed.Horizontal.TProgressbar",
            background=c["error"],
            troughcolor=c["secondary"],
            thickness=12
        )

        # Скроллбар
        self.style.configure(
            "TScrollbar",
            background=c["scrollbar"],
            troughcolor=c["secondary"],
            bordercolor=c["border"],
            arrowcolor=c["text_secondary"]
        )
        self.style.map(
            "TScrollbar",
            background=[("active", c["highlight"])]
        )

        # История
        self.style.configure(
            "History.TLabel",
            background=c["card"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 9),
            padding=(padding, padding // 2)
        )
        self.style.map(
            "History.TLabel",
            background=[("active", c["highlight"])],
            foreground=[("active", c["accent"])]
        )

        # Предпросмотр
        self.style.configure(
            "Preview.TFrame",
            background=c["card"],
            relief="solid",
            borderwidth=border_width,
            bordercolor=c["border"]
        )

        # Тексты статуса/ошибок/успеха/варнингов
        self.style.configure("Error.TLabel", background=c["bg"], foreground=c["error"], font=("Segoe UI", 10))
        self.style.configure("Success.TLabel", background=c["bg"], foreground=c["success"], font=("Segoe UI", 10))
        self.style.configure("Warning.TLabel", background=c["bg"], foreground=c["warning"], font=("Segoe UI", 10))

        # Дроп-зона - теперь отдельным стилем метки
        self.style.configure(
            "DropLabel.TLabel",
            background=c["card"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 11, "bold"),
            padding=(padding * 2, padding * 2),
            borderwidth=0
        )
        self.style.configure(
            "DropLabelActive.TLabel",
            background=c["highlight"],
            foreground=c["text"],
            font=("Segoe UI", 11, "bold"),
            padding=(padding * 2, padding * 2),
            borderwidth=0
        )

        # Статусная панель
        self.style.configure("StatusBar.TFrame", background=c["secondary"])

        # Тосты
        self.style.configure("Toast.TLabel",
                             background="#333333", foreground="#ffffff", font=("Segoe UI", 10), relief="solid",
                             borderwidth=1)

        # Новые стили для улучшенного интерфейса
        self.style.configure(
            "Title.TLabel",
            background=c["bg"],
            foreground=c["accent"],
            font=("Segoe UI Variable Display", 24, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=c["bg"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 12)
        )

        self.style.configure(
            "Header.TLabel",
            background=c["bg"],
            foreground=c["text"],
            font=("Segoe UI", 14, "bold")
        )

        self.style.configure(
            "Info.TLabel",
            background=c["card"],
            foreground=c["text"],
            font=("Segoe UI", 10)
        )

        self.style.configure(
            "InfoSecondary.TLabel",
            background=c["card"],
            foreground=c["text_secondary"],
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "CardButton.TButton",
            background=c["card"],
            foreground=c["text"],
            font=("Segoe UI", 10),
            relief="flat",
            padding=(padding, padding - 2),
            borderwidth=border_width,
            bordercolor=c["border"]
        )
        self.style.map(
            "CardButton.TButton",
            background=[("active", c["highlight"]), ("pressed", c["accent_pressed"])],
            foreground=[("pressed", "#ffffff")]
        )

    @staticmethod
    def _adjust_color(hex_color: str, amount: int) -> str:
        """Осветлить или затемнить цвет"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        adjusted = []
        for c in rgb:
            c = max(0, min(255, c + amount))  # Ограничиваем значения от 0 до 255
            adjusted.append(c)
        return f"#{adjusted[0]:02x}{adjusted[1]:02x}{adjusted[2]:02x}"

    def animate_color_transition(self, widget, from_color, to_color, duration_ms=300, steps=10):
        """Анимирует переход цвета для виджета"""
        if widget in self.animations:
            self.root.after_cancel(self.animations[widget])

        r1, g1, b1 = self._hex_to_rgb(from_color)
        r2, g2, b2 = self._hex_to_rgb(to_color)

        def update_color(step):
            if step > steps:
                return

            ratio = step / steps
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"

            try:
                if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                    widget.configure(bg=color)
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg=color)
            except:
                pass

            if step < steps:
                self.animations[widget] = self.root.after(int(duration_ms / steps), lambda: update_color(step + 1))

        update_color(0)

    def _hex_to_rgb(self, hex_color):
        """Преобразует hex в RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


# ───────────────────────────────────────────────
# 🎭 КЛАСС АНИМАЦИЙ
# ───────────────────────────────────────────────
class AnimationManager:
    def __init__(self, root, theme_manager):
        self.root = root
        self.theme_manager = theme_manager
        self.animations = {}

    def fade_in(self, widget, duration=300):
        """Плавное появление виджета"""
        widget.attributes("-alpha", 0.0)
        widget.deiconify()

        steps = 10
        delay = duration // steps

        def animate(step):
            alpha = step / steps
            widget.attributes("-alpha", alpha)
            if step < steps:
                self.root.after(delay, lambda: animate(step + 1))

        animate(1)

    def slide_in_from_right(self, widget, duration=300):
        """Слайд справа"""
        # Получаем текущую геометрию
        widget.update_idletasks()
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()

        # Начинаем с позиции справа
        start_x = x + width

        steps = 10
        delay = duration // steps

        def animate(step):
            current_x = start_x - (start_x - x) * (step / steps)
            widget.geometry(f"{width}x{height}+{int(current_x)}+{y}")
            if step < steps:
                self.root.after(delay, lambda: animate(step + 1))

        animate(0)

    def pulse_button(self, button, times=2):
        """Пульсация кнопки"""
        original_bg = button.cget("background")
        accent_color = self.theme_manager.colors["accent"]

        def pulse(count):
            if count <= 0:
                return

            def set_original():
                try:
                    button.configure(background=original_bg)
                except:
                    pass

            def set_accent():
                try:
                    button.configure(background=accent_color)
                except:
                    pass

            set_accent()
            self.root.after(150, set_original)
            self.root.after(300, lambda: pulse(count - 1))

        pulse(times)


# ───────────────────────────────────────────────
# 📊 КЛАСС СТАТИСТИКИ И АНАЛИТИКИ
# ───────────────────────────────────────────────
class AnalyticsManager:
    def __init__(self):
        self.stats_file = "stego_analytics.json"
        self.stats = self.load_stats()

    def load_stats(self):
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass

        return {
            "total_operations": 0,
            "hide_operations": 0,
            "extract_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "methods_used": {},
            "file_types_hidden": {},
            "last_used": time.time(),
            "version": VERSION,
            "sessions": 0
        }

    def save_stats(self):
        try:
            self.stats["last_used"] = time.time()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except:
            pass

    def record_operation(self, operation_type, success=True, method=None, file_type=None):
        self.stats["total_operations"] += 1
        self.stats["last_used"] = time.time()

        if operation_type == "hide":
            self.stats["hide_operations"] += 1
        elif operation_type == "extract":
            self.stats["extract_operations"] += 1

        if success:
            self.stats["successful_operations"] += 1
        else:
            self.stats["failed_operations"] += 1

        if method:
            if method not in self.stats["methods_used"]:
                self.stats["methods_used"][method] = 0
            self.stats["methods_used"][method] += 1

        if file_type:
            if file_type not in self.stats["file_types_hidden"]:
                self.stats["file_types_hidden"][file_type] = 0
            self.stats["file_types_hidden"][file_type] += 1

        self.save_stats()

    def get_summary(self):
        total = self.stats["total_operations"]
        success_rate = (self.stats["successful_operations"] / total * 100) if total > 0 else 0

        return {
            "total_operations": total,
            "success_rate": success_rate,
            "hide_operations": self.stats["hide_operations"],
            "extract_operations": self.stats["extract_operations"],
            "most_used_method": self._get_most_used(self.stats["methods_used"]),
            "most_hidden_file_type": self._get_most_used(self.stats["file_types_hidden"]),
            "sessions": self.stats.get("sessions", 0)
        }

    def _get_most_used(self, dictionary):
        if not dictionary:
            return None
        return max(dictionary.items(), key=lambda x: x[1])[0]


# ───────────────────────────────────────────────
# 📋 КЛАСС ИСТОРИИ ДЕЙСТВИЙ (UNDO/REDO)
# ───────────────────────────────────────────────
class HistoryManager:
    def __init__(self, max_history=5):
        self.max_history = max_history
        self.history = []
        self.current_index = -1

    def add_action(self, action_type, data, description=""):
        """Добавляет действие в историю"""
        # Если мы находимся не в конце истории, обрезаем будущее
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]

        action = {
            "type": action_type,
            "data": data,
            "description": description,
            "timestamp": time.time()
        }

        self.history.append(action)
        self.current_index = len(self.history) - 1

        # Ограничиваем размер истории
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.current_index = len(self.history) - 1

    def can_undo(self):
        return self.current_index >= 0

    def can_redo(self):
        return self.current_index < len(self.history) - 1

    def undo(self):
        if not self.can_undo():
            return None

        action = self.history[self.current_index]
        self.current_index -= 1
        return action

    def redo(self):
        if not self.can_redo():
            return None

        self.current_index += 1
        return self.history[self.current_index]

    def clear(self):
        self.history = []
        self.current_index = -1


# ───────────────────────────────────────────────
# 🔔 КЛАСС УВЕДОМЛЕНИЙ
# ───────────────────────────────────────────────
class NotificationManager:
    def __init__(self, root, theme_manager):
        self.root = root
        self.theme_manager = theme_manager
        self.notifications = []
        self.max_notifications = 5

    def show_notification(self, message, type="info", duration=3000):
        """Показывает уведомление"""
        # Удаляем старые уведомления если их слишком много
        if len(self.notifications) >= self.max_notifications:
            oldest = self.notifications.pop(0)
            try:
                oldest.destroy()
            except:
                pass

        # Создаем новое уведомление
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        notification.attributes("-topmost", True)

        # Определяем стиль в зависимости от типа
        colors = self.theme_manager.colors
        if type == "error":
            bg_color = colors["error"]
            fg_color = "#ffffff"
        elif type == "success":
            bg_color = colors["success"]
            fg_color = "#ffffff"
        elif type == "warning":
            bg_color = colors["warning"]
            fg_color = "#ffffff"
        else:
            bg_color = colors["card"]
            fg_color = colors["text"]

        # Создаем фрейм уведомления
        frame = tk.Frame(notification, bg=bg_color, padx=15, pady=10)
        frame.pack(fill="both", expand=True)

        # Добавляем текст
        label = tk.Label(frame, text=message, bg=bg_color, fg=fg_color,
                         font=("Segoe UI", 10), justify="left", wraplength=300)
        label.pack(side="left", fill="x", expand=True)

        # Добавляем кнопку закрытия
        close_btn = tk.Button(frame, text="✕", bg=bg_color, fg=fg_color,
                              font=("Segoe UI", 10, "bold"), relief="flat",
                              command=lambda: self._close_notification(notification))
        close_btn.pack(side="right", padx=(10, 0))

        # Позиционируем уведомление
        self._position_notification(notification)

        # Добавляем в список
        self.notifications.append(notification)

        # Автоматическое закрытие
        if duration > 0:
            notification.after(duration, lambda: self._close_notification(notification))

        return notification

    def _position_notification(self, notification):
        """Позиционирует уведомление в правом верхнем углу"""
        notification.update_idletasks()
        width = notification.winfo_width()
        height = notification.winfo_height()

        # Получаем размеры экрана
        screen_width = notification.winfo_screenwidth()
        screen_height = notification.winfo_screenheight()

        # Рассчитываем позицию
        x = screen_width - width - 20
        y = 60  # Начинаем с 60px от верха

        # Если есть другие уведомления, размещаем ниже
        for i, existing in enumerate(self.notifications[:-1]):  # Все кроме текущего
            if existing.winfo_exists():
                try:
                    existing_y = existing.winfo_y()
                    existing_height = existing.winfo_height()
                    potential_y = existing_y + existing_height + 10
                    if potential_y + height < screen_height - 20:
                        y = potential_y
                except:
                    pass

        notification.geometry(f"+{x}+{y}")

    def _close_notification(self, notification):
        """Закрывает уведомление"""
        if notification in self.notifications:
            self.notifications.remove(notification)
        try:
            notification.destroy()
        except:
            pass

    def clear_all(self):
        """Закрывает все уведомления"""
        for notification in self.notifications[:]:
            self._close_notification(notification)


# ───────────────────────────────────────────────
# 🧩 КЛАСС РАСШИРЕНИЙ И ПЛАГИНОВ
# ───────────────────────────────────────────────
class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = "../plugins"
        self.load_plugins()

    def load_plugins(self):
        """Загружает плагины из директории"""
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                try:
                    # Динамическая загрузка плагина
                    spec = __import__(f"{self.plugin_dir}.{plugin_name}", fromlist=[plugin_name])
                    if hasattr(spec, 'Plugin'):
                        plugin_class = getattr(spec, 'Plugin')
                        plugin_instance = plugin_class()
                        self.plugins[plugin_name] = plugin_instance
                        print(f"Загружен плагин: {plugin_name}")
                except Exception as e:
                    print(f"Ошибка загрузки плагина {plugin_name}: {e}")

    def get_plugins(self):
        """Возвращает список загруженных плагинов"""
        return self.plugins

    def execute_plugin(self, plugin_name, method, *args, **kwargs):
        """Выполняет метод плагина"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            if hasattr(plugin, method):
                try:
                    return getattr(plugin, method)(*args, **kwargs)
                except Exception as e:
                    print(f"Ошибка выполнения метода {method} плагина {plugin_name}: {e}")
        return None


# ───────────────────────────────────────────────
# 📁 КЛАСС УПРАВЛЕНИЯ ФАЙЛАМИ
# ───────────────────────────────────────────────
class FileManager:
    def __init__(self, root):
        self.root = root
        self.recent_files = []
        self.max_recent = 20
        self.load_recent_files()

    def add_recent_file(self, file_path):
        """Добавляет файл в список недавних"""
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        if len(self.recent_files) > self.max_recent:
            self.recent_files = self.recent_files[:self.max_recent]
        self.save_recent_files()

    def get_recent_files(self):
        """Возвращает список недавних файлов"""
        # Фильтруем несуществующие файлы
        existing_files = [f for f in self.recent_files if os.path.exists(f)]
        if len(existing_files) != len(self.recent_files):
            self.recent_files = existing_files
            self.save_recent_files()
        return existing_files

    def save_recent_files(self):
        """Сохраняет список недавних файлов"""
        try:
            with open("recent_files.json", 'w', encoding='utf-8') as f:
                json.dump(self.recent_files, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_recent_files(self):
        """Загружает список недавних файлов"""
        try:
            if os.path.exists("recent_files.json"):
                with open("recent_files.json", 'r', encoding='utf-8') as f:
                    self.recent_files = json.load(f)
        except:
            self.recent_files = []

    def get_file_preview(self, file_path):
        """Возвращает предварительный просмотр файла"""
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga']:
                with Image.open(file_path) as img:
                    img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3])
                        img = background
                    return ImageTk.PhotoImage(img)
            elif ext == '.wav':
                return "🎵 WAV аудиофайл"
            elif ext in ['.txt', '.py', '.json', '.xml', '.html', '.css', '.js']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(200)
                    return f"📄 Текстовый файл  {content}..."
            else:
                return f"📁 {os.path.basename(file_path)}"
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"

# ───────────────────────────────────────────────
# 🎨 ГРАДИЕНТНЫЕ ФОНЫ И ЭФФЕКТЫ
# ───────────────────────────────────────────────
class GradientFrame(tk.Canvas):
    """Фрейм с градиентным фоном"""

    def __init__(self, parent, color1, color2, direction="vertical", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.direction = direction
        self.bind("<Configure>", self.draw_gradient)

    def draw_gradient(self, event=None):
        """Рисует градиент"""
        self.delete("gradient")

        width = self.winfo_width()
        height = self.winfo_height()

        if self.direction == "vertical":
            limit = height
        else:
            limit = width

        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)

        r_ratio = float(r2 - r1) / limit if limit > 0 else 0
        g_ratio = float(g2 - g1) / limit if limit > 0 else 0
        b_ratio = float(b2 - b1) / limit if limit > 0 else 0

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))

            color = f"#{nr // 256:02x}{ng // 256:02x}{nb // 256:02x}"

            if self.direction == "vertical":
                self.create_line(0, i, width, i, tags=("gradient",), fill=color)
            else:
                self.create_line(i, 0, i, height, tags=("gradient",), fill=color)

        self.lower("gradient")


class AnimatedProgressbar(ttk.Progressbar):
    """Анимированный прогресс-бар"""

    def __init__(self, parent, *args, **kwargs):
        ttk.Progressbar.__init__(self, parent, *args, **kwargs)
        self.is_animating = False
        self.animation_id = None

    def start_animation(self):
        """Запускает анимацию"""
        if not self.is_animating:
            self.is_animating = True
            self._animate()

    def stop_animation(self):
        """Останавливает анимацию"""
        self.is_animating = False
        if self.animation_id:
            self.after_cancel(self.animation_id)
            self.animation_id = None

    def _animate(self):
        """Анимирует прогресс-бар"""
        if self.is_animating:
            value = self['value']
            if value >= 100:
                value = 0
            else:
                value += 1
            self['value'] = value
            self.animation_id = self.after(50, self._animate)


# ───────────────────────────────────────────────
# 🎭 АНИМИРОВАННЫЕ ЭЛЕМЕНТЫ ИНТЕРФЕЙСА
# ───────────────────────────────────────────────
class AnimatedButton(ttk.Button):
    """Анимированная кнопка"""

    def __init__(self, parent, *args, **kwargs):
        ttk.Button.__init__(self, parent, *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress>", self.on_press)
        self.bind("<ButtonRelease>", self.on_release)

    def on_enter(self, event):
        """Анимация при наведении"""
        self.configure(style="Accent.TButton")

    def on_leave(self, event):
        """Анимация при уходе"""
        self.configure(style="TButton")

    def on_press(self, event):
        """Анимация при нажатии"""
        self.configure(style="Accent.TButton")

    def on_release(self, event):
        """Анимация при отпускании"""
        self.configure(style="TButton")


class CardFrame(ttk.Frame):
    """Карточка с эффектами"""

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, style="Card.TFrame", *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        """Эффект при наведении"""
        self.configure(style="Card.TFrame")

    def on_leave(self, event):
        """Эффект при уходе"""
        self.configure(style="Card.TFrame")


# ───────────────────────────────────────────────
# 📊 ВИЗУАЛИЗАЦИЯ ДАННЫХ
# ───────────────────────────────────────────────
class CapacityVisualization(tk.Canvas):
    """Визуализация вместимости контейнера"""

    def __init__(self, parent, *args, **kwargs):
        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.data = {}
        self.colors = {}

    def set_data(self, data, colors):
        """Устанавливает данные для визуализации"""
        self.data = data
        self.colors = colors
        self.redraw()

    def on_resize(self, event):
        """Перерисовывает при изменении размера"""
        self.redraw()

    def redraw(self):
        """Перерисовывает визуализацию"""
        self.delete("all")

        if not self.data:
            return

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 0 or height <= 0:
            return

        # Рисуем фон
        self.create_rectangle(0, 0, width, height, fill="#2D3748", outline="")

        # Рисуем данные
        total = sum(self.data.values())
        if total == 0:
            return

        x = 10
        y = 10
        bar_height = 20
        spacing = 5

        for method, value in self.data.items():
            percentage = value / total
            bar_width = int((width - 20) * percentage)

            color = self.colors.get(method, "#4299E1")

            # Рисуем полосу
            self.create_rectangle(x, y, x + bar_width, y + bar_height, fill=color, outline="")

            # Рисуем текст
            text = f"{method}: {value} байт ({percentage:.1%})"
            self.create_text(x + 5, y + bar_height // 2, text=text, anchor="w", fill="white", font=("Segoe UI", 8))

            y += bar_height + spacing
            if y + bar_height > height:
                break


# ───────────────────────────────────────────────
# 📋 РАСШИРЕННЫЙ ИСТОРИЧЕСКИЙ ЖУРНАЛ
# ───────────────────────────────────────────────
class HistoryLog:
    """Расширенный журнал истории операций"""

    def __init__(self):
        self.log_file = "operation_log.json"
        self.log = self.load_log()

    def load_log(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_log(self):
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.log, f, indent=2, ensure_ascii=False)
        except:
            pass

    def add_entry(self, operation_type, status, details=None):
        """Добавляет запись в журнал"""
        entry = {
            "timestamp": time.time(),
            "operation_type": operation_type,
            "status": status,
            "details": details or {},
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.log.append(entry)
        # Ограничиваем размер лога
        if len(self.log) > 1000:
            self.log = self.log[-1000:]
        self.save_log()

    def get_entries(self, limit=50):
        """Возвращает последние записи"""
        return self.log[-limit:] if len(self.log) > limit else self.log

    def get_statistics(self):
        """Возвращает статистику по журналу"""
        if not self.log:
            return {}

        total = len(self.log)
        successful = len([e for e in self.log if e["status"] == "success"])
        failed = len([e for e in self.log if e["status"] == "error"])

        # Статистика по типам операций
        operation_stats = {}
        for entry in self.log:
            op_type = entry["operation_type"]
            if op_type not in operation_stats:
                operation_stats[op_type] = {"total": 0, "success": 0, "error": 0}
            operation_stats[op_type]["total"] += 1
            operation_stats[op_type][entry["status"]] += 1

        return {
            "total_operations": total,
            "successful_operations": successful,
            "failed_operations": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "operation_stats": operation_stats,
            "last_operation": self.log[-1]["formatted_time"] if self.log else "Никогда"
        }


# ───────────────────────────────────────────────
# 📦 КЛАСС ПАКЕТНОЙ ОБРАБОТКИ (BATCH PROCESSING)
# ───────────────────────────────────────────────
class BatchProcessor:
    """Класс для пакетной обработки файлов"""

    def __init__(self, app):
        self.app = app
        self.batch_queue = []
        self.processing = False
        self.current_index = 0
        self.total_files = 0
        self.success_count = 0
        self.fail_count = 0
        self.cancel_requested = False
        self.results = []

    def add_to_batch(self, file_paths, operation_type, params):
        """Добавляет файлы в очередь на обработку"""
        for file_path in file_paths:
            task = {
                'path': file_path,
                'operation': operation_type,
                'params': params.copy(),
                'status': 'pending',
                'result': None,
                'error': None
            }
            self.batch_queue.append(task)

    def clear_batch(self):
        """Очищает очередь пакетной обработки"""
        self.batch_queue = []
        self.results = []
        self.current_index = 0
        self.success_count = 0
        self.fail_count = 0

    def get_batch_info(self):
        """Возвращает информацию о текущей пакетной задаче"""
        return {
            'total': len(self.batch_queue),
            'pending': len([t for t in self.batch_queue if t['status'] == 'pending']),
            'processing': len([t for t in self.batch_queue if t['status'] == 'processing']),
            'completed': len([t for t in self.batch_queue if t['status'] == 'completed']),
            'failed': len([t for t in self.batch_queue if t['status'] == 'failed']),
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'current_index': self.current_index
        }

    # В классе BatchProcessor обновите метод process_batch:
    def process_batch(self, progress_callback=None, completion_callback=None):
        """Обрабатывает очередь файлов"""
        if self.processing:
            raise Exception("Пакетная обработка уже выполняется")

        self.processing = True
        self.cancel_requested = False
        self.total_files = len(self.batch_queue)
        self.success_count = 0
        self.fail_count = 0
        self.current_index = 0  # Сбрасываем индекс

        def process_next():
            try:
                if self.cancel_requested or self.current_index >= len(self.batch_queue):
                    self.processing = False
                    if completion_callback:
                        completion_callback(self.results)
                    return

                task = self.batch_queue[self.current_index]
                task['status'] = 'processing'

                try:
                    if progress_callback:
                        progress = (self.current_index / self.total_files) * 100
                        progress_callback(progress, f"Обработка файла {self.current_index + 1} из {self.total_files}")

                    result = self.process_single_task(task)

                    if result['success']:
                        task['status'] = 'completed'
                        task['result'] = result['data']
                        self.success_count += 1
                    else:
                        task['status'] = 'failed'
                        task['error'] = result['error']
                        self.fail_count += 1

                    self.results.append(result)

                except Exception as e:
                    task['status'] = 'failed'
                    task['error'] = str(e)
                    self.fail_count += 1
                    self.results.append({
                        'success': False,
                        'error': str(e),
                        'file': task['path']
                    })

                self.current_index += 1

                # Продолжаем обработку с небольшой задержкой
                if not self.cancel_requested:
                    self.app.root.after(10, process_next)
                else:
                    self.processing = False
                    if completion_callback:
                        completion_callback(self.results)

            except Exception as e:
                # Гарантируем вызов completion_callback даже при ошибке
                self.processing = False
                self.results.append({
                    'success': False,
                    'error': f"Критическая ошибка в процессе: {str(e)}",
                    'file': 'system'
                })
                if completion_callback:
                    completion_callback(self.results)

        # Запускаем асинхронную обработку
        try:
            self.app.root.after(100, process_next)
        except Exception as e:
            self.processing = False
            if completion_callback:
                completion_callback([{
                    'success': False,
                    'error': f"Не удалось запустить обработку: {str(e)}",
                    'file': 'system'
                }])

    def process_single_task(self, task):
        """Обрабатывает одну задачу"""
        file_path = task['path']
        operation = task['operation']
        params = task['params']

        try:
            if operation == 'hide':
                return self.process_hide(file_path, params)
            elif operation == 'extract':
                return self.process_extract(file_path, params)
            elif operation == 'analyze':
                return self.process_analyze(file_path, params)
            else:
                raise ValueError(f"Неизвестная операция: {operation}")

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file': file_path,
                'operation': operation
            }

    def process_hide(self, container_path, params):
        """Обрабатывает операцию скрытия"""
        # Проверка существования файла
        if not os.path.exists(container_path):
            raise FileNotFoundError(f"Файл не найден: {container_path}")

        # Проверка поддерживаемого формата
        if not Utils.is_supported_container(container_path):
            raise ValueError(f"Неподдерживаемый формат файла: {container_path}")

        # Подготовка данных
        data = params.get('data')
        if data is None:
            raise ValueError("Данные для скрытия не указаны")

        # Подготовка выходного пути
        output_dir = params.get('output_dir', os.path.dirname(container_path))
        output_name = params.get('output_name',
                                 f"{os.path.splitext(os.path.basename(container_path))[0]}_stego.png")
        output_path = os.path.join(output_dir, output_name)

        # Проверка перезаписи
        if os.path.exists(output_path) and not params.get('overwrite', False):
            counter = 1
            while os.path.exists(output_path):
                name, ext = os.path.splitext(output_name)
                output_path = os.path.join(output_dir, f"{name}_{counter}{ext}")
                counter += 1

        # Выполнение скрытия
        method = params.get('method', 'lsb')
        password = params.get('password', '')

        # Определяем правильный класс для обработки
        if container_path.lower().endswith('.wav'):
            # Аудио обработка
            AudioStego.hide_lsb_wav(container_path, data, output_path)
        elif container_path.lower().endswith(('.jpg', '.jpeg')) and method == 'jpeg_dct':
            # JPEG DCT обработка
            JPEGStego.hide_dct(container_path, data, output_path)
        else:
            # Обычная обработка изображений
            ImageProcessor.hide_data(
                container_path, data, password, output_path,
                method=method,
                compression_level=params.get('compression_level', 9)
            )

        return {
            'success': True,
            'file': container_path,
            'output': output_path,
            'operation': 'hide',
            'method': method,
            'size': os.path.getsize(output_path)
        }

    # В классе BatchProcessor исправьте метод process_extract:
    def process_extract(self, stego_path, params):
        """Обрабатывает операцию извлечения - ИСПРАВЛЕННЫЙ"""
        # Проверка существования файла
        if not os.path.exists(stego_path):
            raise FileNotFoundError(f"Файл не найден: {stego_path}")

        # Подготовка выходного пути
        output_dir = params.get('output_dir', os.path.dirname(stego_path))
        os.makedirs(output_dir, exist_ok=True)

        # Генерируем уникальное имя файла
        base_name = os.path.splitext(os.path.basename(stego_path))[0]
        output_name = f"extracted_{base_name}"

        # Проверяем, является ли файл аудио
        ext = os.path.splitext(stego_path)[1].lower()
        if ext == '.wav':
            # Для аудио файлов
            extracted_data = AudioStego.extract_lsb_wav(stego_path)
        else:
            # Для изображений
            method = params.get('method')
            password = params.get('password', '')

            try:
                # Пробуем извлечь данные
                extracted_data = ImageProcessor.extract_data(
                    stego_path,
                    password,
                    method
                )
            except Exception as e:
                # Если не получилось с указанным методом, пробуем автоопределение
                if method:
                    try:
                        extracted_data = ImageProcessor.extract_data(stego_path, password)
                    except:
                        raise e
                else:
                    raise e

        # Определяем тип данных и расширение
        data_type = self.guess_data_type(extracted_data[:100])  # Проверяем первые 100 байт

        extensions = {
            'text': '.txt',
            'json': '.json',
            'png': '.png',
            'jpeg': '.jpg',
            'jpg': '.jpg',
            'gif': '.gif',
            'bmp': '.bmp',
            'zip': '.zip',
            'rar': '.rar',
            'pdf': '.pdf',
            'binary': '.bin'
        }

        ext = extensions.get(data_type, '.bin')
        output_path = os.path.join(output_dir, f"{output_name}{ext}")

        # Сохранение данных
        if params.get('auto_save', True):
            # Проверяем, не существует ли уже файл
            counter = 1
            original_output_path = output_path
            while os.path.exists(output_path) and not params.get('overwrite', False):
                name, ext = os.path.splitext(original_output_path)
                output_path = f"{name}_{counter}{ext}"
                counter += 1

            with open(output_path, 'wb') as f:
                f.write(extracted_data)

        # Анализ данных
        data_info = self.analyze_extracted_data(extracted_data)

        return {
            'success': True,
            'file': stego_path,
            'output': output_path if params.get('auto_save', True) else None,
            'data': extracted_data,
            'data_info': data_info,
            'size': len(extracted_data),
            'operation': 'extract',
            'data_type': data_type
        }

    def process_analyze(self, file_path, params):
        """Анализирует файл"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Получаем информацию о файле
        file_info = Utils.get_file_info(file_path)

        # Проверяем на наличие скрытых данных
        has_stego = False
        stego_info = None

        try:
            # Пробуем извлечь данные (только проверка)
            test_data = ImageProcessor.extract_data(file_path, '')
            has_stego = True
            stego_info = {
                'size': len(test_data),
                'method': 'detected',
                'data_type': self.guess_data_type(test_data)
            }
        except:
            pass

        # Проверяем вместимость
        capacity_info = {}
        if file_info['type'] == 'image':
            w, h, bits = ImageProcessor.get_image_info(file_path)
            for method in ['lsb', 'noise', 'aelsb', 'hill']:
                capacity = ImageProcessor.get_capacity_by_method(bits, method, w, h)
                capacity_info[method] = capacity

        return {
            'success': True,
            'file': file_path,
            'file_info': file_info,
            'has_stego': has_stego,
            'stego_info': stego_info,
            'capacity_info': capacity_info,
            'operation': 'analyze'
        }

    def analyze_extracted_data(self, data):
        """Анализирует извлеченные данные"""
        if not data:
            return {'type': 'empty', 'size': 0}

        # Пытаемся определить тип данных
        try:
            # Проверка на текст
            text = data.decode('utf-8', errors='ignore')
            if len(text) > len(data) * 0.7:  # Большая часть данных - текст
                return {
                    'type': 'text',
                    'size': len(data),
                    'preview': text[:100],
                    'is_utf8': True
                }
        except:
            pass

        # Проверка на JSON
        try:
            json.loads(data.decode('utf-8'))
            return {'type': 'json', 'size': len(data)}
        except:
            pass

        # Проверка на изображение
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(data))
            return {
                'type': 'image',
                'size': len(data),
                'format': img.format,
                'dimensions': f"{img.width}x{img.height}"
            }
        except:
            pass

        # Проверка на архив
        if data[:4] in [b'PK\x03\x04', b'Rar!', b'7z\xBC\xAF']:
            return {'type': 'archive', 'size': len(data)}

        # По умолчанию - бинарные данные
        return {'type': 'binary', 'size': len(data)}

    def guess_data_type(self, data):
        """Пытается определить тип данных"""
        if not data:
            return 'unknown'

        # Проверка на текст
        try:
            text = data.decode('utf-8', errors='ignore')
            text_ratio = len(text) / len(data)
            if text_ratio > 0.8:
                return 'text'
            elif text_ratio > 0.5:
                return 'mixed'
        except:
            pass

        # Проверка магических чисел
        magic_numbers = {
            b'\x89PNG\r\n\x1a\n': 'png',
            b'\xff\xd8\xff': 'jpeg',
            b'GIF': 'gif',
            b'BM': 'bmp',
            b'PK\x03\x04': 'zip',
            b'Rar!': 'rar',
            b'%PDF': 'pdf'
        }

        for magic, filetype in magic_numbers.items():
            if data.startswith(magic):
                return filetype

        return 'binary'

    def cancel_processing(self):
        """Отменяет текущую пакетную обработку"""
        self.cancel_requested = True

    def export_results(self, output_path):
        """Экспортирует результаты обработки в JSON"""
        results_summary = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_files': self.total_files,
            'successful': self.success_count,
            'failed': self.fail_count,
            'success_rate': (self.success_count / self.total_files * 100) if self.total_files > 0 else 0,
            'results': self.results
        }

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results_summary, f, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as e:
            print(f"Ошибка экспорта результатов: {e}")
            return False


# ───────────────────────────────────────────────
# 📦 УЛУЧШЕННЫЙ КЛАСС ИНТЕРФЕЙСА ПАКЕТНОЙ ОБРАБОТКИ С ОПТИМИЗАЦИЕЙ ПРОСТРАНСТВА И ФУНКЦИОНАЛЬНОСТИ
# ───────────────────────────────────────────────
class BatchProcessingUI:
    """Улучшенный интерфейс для пакетной обработки с оптимизированным дизайном, корректной обработкой результатов и эффективным использованием пространства"""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.batch_processor = BatchProcessor(app)
        self.processing = False  # Флаг текущей обработки

        # Переменные для вкладки скрытия
        self.selected_files = []
        self.output_dir = tk.StringVar(value=os.path.expanduser("~"))
        self.method_var = tk.StringVar(value="lsb")
        self.overwrite_var = tk.BooleanVar(value=False)
        self.hide_data_type = tk.StringVar(value="text")
        self.hide_file_path = tk.StringVar()
        self.hide_password = tk.StringVar()
        self.hide_text_content = tk.StringVar(value="")  # Новая переменная для текста

        # Переменные для вкладки извлечения
        self.selected_extract_files = []
        self.extract_output_dir = tk.StringVar(value=os.path.expanduser("~"))
        self.extract_password = tk.StringVar()
        self.extract_method = tk.StringVar()
        self.auto_save_var = tk.BooleanVar(value=True)

        # Переменные для вкладки анализа
        self.selected_analyze_files = []

        # Статистика обработки
        self.total_files = 0
        self.success_count = 0
        self.fail_count = 0

        # Текущие индексы выделенных элементов
        self.current_selected_index = None

        self.setup_ui()
        self.update_ui_state()

    def setup_ui(self):
        """Создает оптимизированный интерфейс пакетной обработки с эффективным использованием пространства"""
        # Создаем панель навигации вверху
        nav_frame = ttk.Frame(self.parent, style="Card.TFrame")
        nav_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        # Заголовок
        ttk.Label(
            nav_frame,
            text="📦 Пакетная обработка файлов",
            font=("Segoe UI", 16, "bold"),
            style="Title.TLabel"
        ).pack(side=tk.LEFT, padx=10)

        # Кнопки быстрого доступа
        quick_access_frame = ttk.Frame(nav_frame, style="Card.TFrame")
        quick_access_frame.pack(side=tk.RIGHT, padx=10)

        buttons = [
            ("📊 Экспорт результатов", self.export_batch_results),
            ("🗑️ Очистить все", self.clear_all),
            ("❓ Помощь", self.show_help)
        ]

        for text, command in buttons:
            ttk.Button(
                quick_access_frame,
                text=text,
                style="IconButton.TButton",
                command=command
            ).pack(side=tk.LEFT, padx=5)

        # Основной контейнер
        main_container = ttk.Frame(self.parent, style="Card.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Canvas для прокрутки
        self.canvas = tk.Canvas(main_container, bg=self.app.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)

        # Прокручиваемый фрейм
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")

        # Настройка прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Создаем окно на canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Размещаем элементы
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 5))
        scrollbar.pack(side="right", fill="y")

        # Связываем колесо мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Создаем содержимое с оптимизированной компоновкой
        self.create_content()

        # Статусная панель внизу
        self.create_status_panel()

    def _on_mousewheel(self, event):
        """Обработка колеса мыши для прокрутки"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_content(self):
        """Создает содержимое интерфейса с оптимизированной компоновкой для эффективного использования пространства"""
        # Создаем Notebook для разных операций в центре
        self.batch_notebook = ttk.Notebook(self.scrollable_frame)
        self.batch_notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Создаем три вкладки с оптимизированным внутренним расположением
        self.hide_tab = self.create_hide_tab()
        self.batch_notebook.add(self.hide_tab, text="📤 Скрытие")

        self.extract_tab = self.create_extract_tab()
        self.batch_notebook.add(self.extract_tab, text="📥 Извлечение")

        self.analyze_tab = self.create_analyze_tab()
        self.batch_notebook.add(self.analyze_tab, text="🔍 Анализ")

    def create_hide_tab(self):
        """Создает улучшенную вкладку для пакетного скрытия с оптимизированной компоновкой"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем grid для лучшей организации
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)  # Статусная панель будет расширяться

        # Верхняя панель с инструкциями
        instruction_frame = ttk.LabelFrame(tab, text="💡 Инструкция", padding=12, style="Card.TLabelframe")
        instruction_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)

        instruction_text = (
            "1. Добавьте до 5 контейнеров-файлов для скрытия данных\n"
            "2. Укажите данные для скрытия (текст или файл)\n"
            "3. Выберите метод скрытия и настройки\n"
            "4. Укажите папку для сохранения результатов\n"
            "5. Нажмите '🚀 Начать пакетное скрытие'"
        )

        ttk.Label(
            instruction_frame,
            text=instruction_text,
            font=("Segoe UI", 10),
            justify=tk.LEFT,
            style="Secondary.TLabel"
        ).pack(padx=5, pady=5)

        # Основной контент с двумя колонками
        content_frame = ttk.Frame(tab, style="Card.TFrame")
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        content_frame.grid_columnconfigure(0, weight=2)  # Больше места для выбора файлов
        content_frame.grid_columnconfigure(1, weight=1)  # Меньше места для настроек
        content_frame.grid_rowconfigure(0, weight=1)

        # Левая колонка - выбор файлов и данные
        left_frame = ttk.Frame(content_frame, style="Card.TFrame")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Выбор контейнеров
        files_frame = ttk.LabelFrame(left_frame, text="📂 Файлы-контейнеры (макс. 5)", padding=12,
                                     style="Card.TLabelframe")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Верхняя панель с кнопками управления файлами
        files_control_frame = ttk.Frame(files_frame, style="Card.TFrame")
        files_control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            files_control_frame,
            text="➕ Добавить файлы",
            style="Accent.TButton",
            command=self.add_files
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🗑️ Удалить выбранное",
            style="TButton",
            command=self.remove_selected_file  # Исправлено: добавлен обработчик
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🧹 Очистить список",
            style="TButton",
            command=self.clear_files  # Исправлено: добавлен обработчик
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Список файлов с прокруткой
        list_frame = ttk.Frame(files_frame, style="Card.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview для более информативного отображения файлов
        columns = ("#", "Имя файла", "Тип", "Размер")
        self.files_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=8
        )

        # Настройка заголовков
        self.files_tree.heading("#", text="#", command=lambda: self.sort_treeview(self.files_tree, "#", False))
        self.files_tree.heading("Имя файла", text="Имя файла",
                                command=lambda: self.sort_treeview(self.files_tree, "Имя файла", False))
        self.files_tree.heading("Тип", text="Тип", command=lambda: self.sort_treeview(self.files_tree, "Тип", False))
        self.files_tree.heading("Размер", text="Размер",
                                command=lambda: self.sort_treeview(self.files_tree, "Размер", False))

        # Ширина столбцов
        self.files_tree.column("#", width=30, anchor=tk.CENTER)
        self.files_tree.column("Имя файла", width=250, anchor=tk.W)
        self.files_tree.column("Тип", width=80, anchor=tk.CENTER)
        self.files_tree.column("Размер", width=80, anchor=tk.CENTER)

        # Полоса прокрутки
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_tree.yview)
        self.files_tree.configure(yscrollcommand=tree_scroll.set)

        # Размещение
        self.files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязка события выделения
        self.files_tree.bind("<<TreeviewSelect>>", self.on_file_select)

        # Данные для скрытия
        data_frame = ttk.LabelFrame(left_frame, text="📋 Данные для скрытия", padding=12, style="Card.TLabelframe")
        data_frame.pack(fill=tk.X, pady=(10, 0))

        # Тип данных
        type_frame = ttk.Frame(data_frame, style="Card.TFrame")
        type_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(type_frame, text="Тип данных:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        type_control_frame = ttk.Frame(type_frame, style="Card.TFrame")
        type_control_frame.pack(side=tk.LEFT, padx=10)

        ttk.Radiobutton(
            type_control_frame,
            text="Текст",
            variable=self.hide_data_type,
            value="text",
            command=self.update_hide_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT, padx=(0, 15))

        ttk.Radiobutton(
            type_control_frame,
            text="Файл",
            variable=self.hide_data_type,
            value="file",
            command=self.update_hide_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT)

        # Фреймы для текста и файла
        self.hide_text_frame = ttk.Frame(data_frame, style="Card.TFrame")
        self.hide_file_frame = ttk.Frame(data_frame, style="Card.TFrame")

        # Текстовое поле
        ttk.Label(self.hide_text_frame, text="Введите текст для скрытия:", font=("Segoe UI", 9),
                  style="Secondary.TLabel").pack(anchor=tk.W, pady=(0, 5))

        self.hide_text = scrolledtext.ScrolledText(
            self.hide_text_frame,
            height=6,
            wrap=tk.WORD,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            font=("Segoe UI", 10),
            padx=5,
            pady=5
        )
        self.hide_text.pack(fill=tk.BOTH, expand=True)
        self.hide_text.bind("<KeyRelease>", self.update_ui_state)

        # Выбор файла
        file_select_frame = ttk.Frame(self.hide_file_frame, style="Card.TFrame")
        file_select_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(file_select_frame, text="Файл для скрытия:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        ttk.Entry(
            file_select_frame,
            textvariable=self.hide_file_path,
            state='readonly',
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        ttk.Button(
            file_select_frame,
            text="📂",
            command=self.select_hide_file,
            width=3,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT)

        # Панель информации о файле
        self.file_info_label = ttk.Label(
            self.hide_file_frame,
            text="ℹ️ Информация о файле появится здесь",
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        self.file_info_label.pack(fill=tk.X, pady=(5, 0))

        # Показываем правильный фрейм в зависимости от типа
        if self.hide_data_type.get() == "text":
            self.hide_text_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
            self.hide_file_frame.pack_forget()
        else:
            self.hide_file_frame.pack(fill=tk.X, pady=(10, 0))
            self.hide_text_frame.pack_forget()

        # Правая колонка - настройки и управление
        right_frame = ttk.Frame(content_frame, style="Card.TFrame")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.grid_rowconfigure(3, weight=1)  # Дает пространство для кнопки запуска внизу

        # Настройки скрытия
        settings_frame = ttk.LabelFrame(right_frame, text="⚙️ Настройки скрытия", padding=15, style="Card.TLabelframe")
        settings_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # Метод скрытия
        method_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        method_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(method_frame, text="Метод скрытия:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.method_var,
            values=list(STEGANO_METHODS.keys()),
            state="readonly",
            width=25
        )
        method_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        method_combo.bind("<<ComboboxSelected>>", lambda e: self.update_capacity_info())

        # Пароль
        password_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        password_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(password_frame, text="Пароль (опционально):", font=("Segoe UI", 10), style="TLabel").pack(
            side=tk.LEFT)

        ttk.Entry(
            password_frame,
            textvariable=self.hide_password,
            show="●",
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        # Параметры вывода
        output_frame = ttk.LabelFrame(right_frame, text="📁 Параметры вывода", padding=15, style="Card.TLabelframe")
        output_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

        # Папка сохранения
        dir_frame = ttk.Frame(output_frame, style="Card.TFrame")
        dir_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(dir_frame, text="Папка для сохранения:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        output_dir_entry = ttk.Entry(
            dir_frame,
            textvariable=self.output_dir,
            style="TEntry"
        )
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        ttk.Button(
            dir_frame,
            text="📂",
            command=self.select_output_dir,
            width=3,
            style="IconButton.TButton"
        ).pack(side=tk.RIGHT)

        # Опции сохранения
        options_frame = ttk.Frame(output_frame, style="Card.TFrame")
        options_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Checkbutton(
            options_frame,
            text="Перезаписывать существующие файлы",
            variable=self.overwrite_var,
            style="TCheckbutton"
        ).pack(anchor=tk.W)

        # Кнопка запуска - вынесена отдельно для большей видимости
        self.hide_button = ttk.Button(
            right_frame,
            text="🚀 Начать пакетное скрытие",
            style="Accent.TButton",
            command=self.start_batch_hide,
            state="disabled"
        )
        self.hide_button.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        # Информация о вместимости (занимает оставшееся пространство)
        capacity_frame = ttk.LabelFrame(right_frame, text="📊 Вместимость", padding=15, style="Card.TLabelframe")
        capacity_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        self.capacity_label = ttk.Label(
            capacity_frame,
            text="ℹ️ Информация о вместимости появится после выбора файла",
            font=("Segoe UI", 9),
            style="Secondary.TLabel",
            wraplength=350
        )
        self.capacity_label.pack(fill=tk.X, pady=(5, 0))

        return tab

    def create_extract_tab(self):
        """Создает улучшенную вкладку для пакетного извлечения"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем grid для лучшей организации
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Верхняя панель с инструкциями
        instruction_frame = ttk.LabelFrame(tab, text="💡 Инструкция", padding=12, style="Card.TLabelframe")
        instruction_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)

        instruction_text = (
            "1. Добавьте до 5 файлов со скрытыми данными\n"
            "2. Укажите пароль и метод извлечения (или оставьте для автоопределения)\n"
            "3. Выберите папку для сохранения извлеченных данных\n"
            "4. Нажмите '🚀 Начать пакетное извлечение'"
        )

        ttk.Label(
            instruction_frame,
            text=instruction_text,
            font=("Segoe UI", 10),
            justify=tk.LEFT,
            style="Secondary.TLabel"
        ).pack(padx=5, pady=5)

        # Основной контент с двумя колонками
        content_frame = ttk.Frame(tab, style="Card.TFrame")
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=5)
        content_frame.grid_columnconfigure(0, weight=2)  # Больше места для файлов
        content_frame.grid_columnconfigure(1, weight=1)  # Меньше места для настроек
        content_frame.grid_rowconfigure(0, weight=1)

        # Левая колонка - выбор файлов
        left_frame = ttk.Frame(content_frame, style="Card.TFrame")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Выбор файлов
        files_frame = ttk.LabelFrame(left_frame, text="📂 Файлы со скрытыми данными (макс. 5)", padding=12,
                                     style="Card.TLabelframe")
        files_frame.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления файлами
        files_control_frame = ttk.Frame(files_frame, style="Card.TFrame")
        files_control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            files_control_frame,
            text="➕ Добавить файлы",
            style="Accent.TButton",
            command=self.add_extract_files
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🗑️ Удалить выбранное",  # Исправлено: кнопка теперь работает
            style="TButton",
            command=self.remove_selected_extract_file
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🧹 Очистить список",  # Исправлено: кнопка теперь работает
            style="TButton",
            command=lambda: [self.selected_extract_files.clear(), self.update_extract_files_list()]
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Список файлов
        list_frame = ttk.Frame(files_frame, style="Card.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview для файлов
        columns = ("#", "Имя файла", "Тип", "Размер")
        self.extract_files_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=10
        )

        # Настройка заголовков
        self.extract_files_tree.heading("#", text="#",
                                        command=lambda: self.sort_treeview(self.extract_files_tree, "#", False))
        self.extract_files_tree.heading("Имя файла", text="Имя файла",
                                        command=lambda: self.sort_treeview(self.extract_files_tree, "Имя файла", False))
        self.extract_files_tree.heading("Тип", text="Тип",
                                        command=lambda: self.sort_treeview(self.extract_files_tree, "Тип", False))
        self.extract_files_tree.heading("Размер", text="Размер",
                                        command=lambda: self.sort_treeview(self.extract_files_tree, "Размер", False))

        # Ширина столбцов
        self.extract_files_tree.column("#", width=30, anchor=tk.CENTER)
        self.extract_files_tree.column("Имя файла", width=250, anchor=tk.W)
        self.extract_files_tree.column("Тип", width=80, anchor=tk.CENTER)
        self.extract_files_tree.column("Размер", width=80, anchor=tk.CENTER)

        # Полоса прокрутки
        extract_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.extract_files_tree.yview)
        self.extract_files_tree.configure(yscrollcommand=extract_scroll.set)

        # Размещение
        self.extract_files_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        extract_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязка события выделения
        self.extract_files_tree.bind("<<TreeviewSelect>>", self.on_extract_file_select)

        # Правая колонка - настройки
        right_frame = ttk.Frame(content_frame, style="Card.TFrame")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.grid_rowconfigure(3, weight=1)  # Дает пространство для кнопки запуска внизу

        # Настройки извлечения
        settings_frame = ttk.LabelFrame(right_frame, text="⚙️ Настройки извлечения", padding=15,
                                        style="Card.TLabelframe")
        settings_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

        # Пароль
        password_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        password_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(password_frame, text="Пароль:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        ttk.Entry(
            password_frame,
            textvariable=self.extract_password,
            show="●",
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        # Метод
        method_frame = ttk.Frame(settings_frame, style="Card.TFrame")
        method_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(method_frame, text="Метод (авто если не указан):", font=("Segoe UI", 10), style="TLabel").pack(
            side=tk.LEFT)

        method_combo = ttk.Combobox(
            method_frame,
            textvariable=self.extract_method,
            values=["", "lsb", "noise", "aelsb", "hill", "audio_lsb", "jpeg_dct"],
            state="readonly",
            width=25
        )
        method_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        # Параметры вывода
        output_frame = ttk.LabelFrame(right_frame, text="📁 Параметры вывода", padding=15, style="Card.TLabelframe")
        output_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

        # Папка сохранения
        dir_frame = ttk.Frame(output_frame, style="Card.TFrame")
        dir_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(dir_frame, text="Папка для сохранения:", font=("Segoe UI", 10), style="TLabel").pack(side=tk.LEFT)

        output_dir_entry = ttk.Entry(
            dir_frame,
            textvariable=self.extract_output_dir,
            style="TEntry"
        )
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        ttk.Button(
            dir_frame,
            text="📂",
            command=self.select_extract_output_dir,
            width=3,
            style="IconButton.TButton"
        ).pack(side=tk.RIGHT)

        # Опции сохранения
        options_frame = ttk.Frame(output_frame, style="Card.TFrame")
        options_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Checkbutton(
            options_frame,
            text="Автоматически сохранять извлеченные данные",
            variable=self.auto_save_var,
            style="TCheckbutton"
        ).pack(anchor=tk.W)

        # Кнопка запуска
        self.extract_button = ttk.Button(
            right_frame,
            text="🚀 Начать пакетное извлечение",
            style="Accent.TButton",
            command=self.start_batch_extract,
            state="disabled"
        )
        self.extract_button.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        # Информация об извлечении (занимает оставшееся пространство)
        info_frame = ttk.LabelFrame(right_frame, text="ℹ️ Информация", padding=15, style="Card.TLabelframe")
        info_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        info_text = (
            "⚠️ Если файл содержит данные, скрытые с использованием пароля,\n"
            "неправильный пароль приведет к ошибке извлечения.\n\n"
            "🔍 Программа может автоматически определить метод извлечения,\n"
            "если оставить поле метода пустым."
        )

        ttk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 9),
            style="Secondary.TLabel",
            justify=tk.LEFT
        ).pack(fill=tk.X, pady=5)

        return tab

    def create_analyze_tab(self):
        """Создает улучшенную вкладку для пакетного анализа"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем grid для лучшей организации
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)  # Результаты будут расширяться

        # Верхняя панель с инструкциями
        instruction_frame = ttk.LabelFrame(tab, text="💡 Инструкция", padding=12, style="Card.TLabelframe")
        instruction_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)

        instruction_text = (
            "1. Добавьте до 5 файлов для анализа\n"
            "2. Нажмите '🔍 Начать анализ' для проверки файлов\n"
            "3. Просмотрите результаты в таблице ниже\n"
            "4. Экспортируйте результаты при необходимости"
        )

        ttk.Label(
            instruction_frame,
            text=instruction_text,
            font=("Segoe UI", 10),
            justify=tk.LEFT,
            style="Secondary.TLabel"
        ).pack(padx=5, pady=5)

        # Панель управления
        control_frame = ttk.Frame(tab, style="Card.TFrame")
        control_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=5)

        # Выбор файлов
        files_frame = ttk.LabelFrame(control_frame, text="📂 Файлы для анализа (макс. 5)", padding=12,
                                     style="Card.TLabelframe")
        files_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Кнопки управления файлами
        files_control_frame = ttk.Frame(files_frame, style="Card.TFrame")
        files_control_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            files_control_frame,
            text="➕ Добавить файлы",
            style="Accent.TButton",
            command=self.add_analyze_files
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🗑️ Удалить выбранное",  # Исправлено: кнопка теперь работает
            style="TButton",
            command=self.remove_selected_analyze_file
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            files_control_frame,
            text="🧹 Очистить список",  # Исправлено: кнопка теперь работает
            style="TButton",
            command=lambda: [self.selected_analyze_files.clear(), self.update_analyze_files_list()]
        ).pack(side=tk.LEFT, padx=(0, 5))

        # Список файлов
        list_frame = ttk.Frame(files_frame, style="Card.TFrame")
        list_frame.pack(fill=tk.X)

        # Treeview для файлов
        columns = ("#", "Имя файла", "Тип", "Размер")
        self.analyze_files_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=4
        )

        # Настройка заголовков
        self.analyze_files_tree.heading("#", text="#",
                                        command=lambda: self.sort_treeview(self.analyze_files_tree, "#", False))
        self.analyze_files_tree.heading("Имя файла", text="Имя файла",
                                        command=lambda: self.sort_treeview(self.analyze_files_tree, "Имя файла", False))
        self.analyze_files_tree.heading("Тип", text="Тип",
                                        command=lambda: self.sort_treeview(self.analyze_files_tree, "Тип", False))
        self.analyze_files_tree.heading("Размер", text="Размер",
                                        command=lambda: self.sort_treeview(self.analyze_files_tree, "Размер", False))

        # Ширина столбцов
        self.analyze_files_tree.column("#", width=30, anchor=tk.CENTER)
        self.analyze_files_tree.column("Имя файла", width=200, anchor=tk.W)
        self.analyze_files_tree.column("Тип", width=80, anchor=tk.CENTER)
        self.analyze_files_tree.column("Размер", width=80, anchor=tk.CENTER)

        # Полоса прокрутки
        analyze_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.analyze_files_tree.yview)
        self.analyze_files_tree.configure(yscrollcommand=analyze_scroll.set)

        # Размещение
        self.analyze_files_tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        analyze_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязка события выделения
        self.analyze_files_tree.bind("<<TreeviewSelect>>", self.on_analyze_file_select)

        # Кнопка запуска анализа
        btn_frame = ttk.Frame(control_frame, style="Card.TFrame")
        btn_frame.pack(side=tk.RIGHT, padx=10)

        self.analyze_button = ttk.Button(
            btn_frame,
            text="🔍 Начать анализ",
            style="Accent.TButton",
            command=self.start_batch_analyze,
            state="disabled"
        )
        self.analyze_button.pack(pady=5)

        # Результаты анализа
        results_frame = ttk.LabelFrame(tab, text="📊 Результаты анализа", padding=15, style="Card.TLabelframe")
        results_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(5, 0))
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        # Treeview для результатов
        result_columns = ("#", "Файл", "Содержит данные", "Метод", "Размер данных", "Вместимость")
        self.results_tree = ttk.Treeview(
            results_frame,
            columns=result_columns,
            show="headings",
            selectmode="browse"
        )

        # Настройка заголовков
        self.results_tree.heading("#", text="#")
        self.results_tree.heading("Файл", text="Файл")
        self.results_tree.heading("Содержит данные", text="Содержит данные")
        self.results_tree.heading("Метод", text="Метод")
        self.results_tree.heading("Размер данных", text="Размер данных")
        self.results_tree.heading("Вместимость", text="Вместимость")

        # Ширина столбцов
        self.results_tree.column("#", width=30, anchor=tk.CENTER)
        self.results_tree.column("Файл", width=180, anchor=tk.W)
        self.results_tree.column("Содержит данные", width=120, anchor=tk.CENTER)
        self.results_tree.column("Метод", width=100, anchor=tk.CENTER)
        self.results_tree.column("Размер данных", width=120, anchor=tk.CENTER)
        self.results_tree.column("Вместимость", width=120, anchor=tk.CENTER)

        # Полоса прокрутки
        results_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)

        # Размещение
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        results_scroll.grid(row=0, column=1, sticky="ns")

        # Привязка событий для обновления состояния кнопки
        self.analyze_files_tree.bind("<<TreeviewSelect>>", lambda e: self.update_ui_state())

        return tab

    def create_status_panel(self):
        """Создает улучшенную статусную панель"""
        status_frame = ttk.LabelFrame(self.parent, text="📊 Статус обработки", padding=12, style="Card.TLabelframe")
        status_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Прогресс
        progress_frame = ttk.Frame(status_frame, style="Card.TFrame")
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.batch_progress_var = tk.DoubleVar()
        self.batch_progress = ttk.Progressbar(
            progress_frame,
            variable=self.batch_progress_var,
            maximum=100,
            style="TProgressbar"
        )
        self.batch_progress.pack(fill=tk.X, pady=(0, 5))

        # Статус
        self.batch_status_label = ttk.Label(
            progress_frame,
            text="✅ Готов к обработке",
            font=("Segoe UI", 10),
            style="TLabel"
        )
        self.batch_status_label.pack(anchor="w")

        # Статистика
        stats_frame = ttk.Frame(status_frame, style="Card.TFrame")
        stats_frame.pack(fill=tk.X)

        # Текущая операция
        self.current_operation_label = ttk.Label(
            stats_frame,
            text="Текущая операция: нет",
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        self.current_operation_label.pack(side=tk.LEFT, padx=(0, 20))

        # Статистика в ряд
        stats_container = ttk.Frame(stats_frame, style="Card.TFrame")
        stats_container.pack(fill=tk.X)

        self.stats_label = ttk.Label(
            stats_container,
            text="Всего: 0 | Обработано: 0 | Успешно: 0 | Ошибки: 0",
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        self.stats_label.pack(side=tk.LEFT)

        # Кнопки управления
        control_frame = ttk.Frame(status_frame, style="Card.TFrame")
        control_frame.pack(fill=tk.X, pady=(10, 0))

        self.stop_button = ttk.Button(  # Сохраняем ссылку на кнопку остановки
            control_frame,
            text="⏹️ Остановить обработку",
            style="TButton",
            command=self.stop_processing,
            state="disabled"  # Начинаем с отключенного состояния
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            control_frame,
            text="📊 Экспорт результатов",
            style="TButton",
            command=self.export_batch_results
        ).pack(side=tk.LEFT)

    # Методы управления состоянием интерфейса
    def update_ui_state(self, event=None):
        """Обновляет состояние UI элементов на основе текущих данных"""
        # Для вкладки скрытия
        has_files = len(self.selected_files) > 0
        has_data = False

        if self.hide_data_type.get() == "text":
            text = self.hide_text.get("1.0", tk.END).strip()
            has_data = len(text) > 0
        else:
            has_data = bool(self.hide_file_path.get())

        output_dir_valid = bool(self.output_dir.get()) and os.path.isdir(self.output_dir.get())

        # Обновляем состояние кнопки для скрытия
        self.hide_button.config(state="normal" if (has_files and has_data and output_dir_valid) else "disabled")

        # Для вкладки извлечения
        has_extract_files = len(self.selected_extract_files) > 0
        extract_output_dir_valid = bool(self.extract_output_dir.get()) and os.path.isdir(self.extract_output_dir.get())

        # Обновляем состояние кнопки для извлечения
        self.extract_button.config(state="normal" if (has_extract_files and extract_output_dir_valid) else "disabled")

        # Для вкладки анализа
        has_analyze_files = len(self.selected_analyze_files) > 0

        # Обновляем состояние кнопки для анализа
        self.analyze_button.config(state="normal" if has_analyze_files else "disabled")

        # Обновляем состояние кнопки остановки
        self.stop_button.config(state="normal" if self.processing else "disabled")

    def on_file_select(self, event):
        """Обрабатывает выбор файла в списке"""
        selection = self.files_tree.selection()
        if selection:
            self.current_selected_index = self.files_tree.index(selection[0])
        else:
            self.current_selected_index = None
        self.update_ui_state()

    def on_extract_file_select(self, event):
        """Обрабатывает выбор файла в списке для извлечения"""
        selection = self.extract_files_tree.selection()
        if selection:
            self.current_selected_index = self.extract_files_tree.index(selection[0])
        else:
            self.current_selected_index = None
        self.update_ui_state()

    def on_analyze_file_select(self, event):
        """Обрабатывает выбор файла в списке для анализа"""
        selection = self.analyze_files_tree.selection()
        if selection:
            self.current_selected_index = self.analyze_files_tree.index(selection[0])
        else:
            self.current_selected_index = None
        self.update_ui_state()

    # Методы управления файлами
    def add_files(self):
        """Добавляет файлы в список контейнеров"""
        files = filedialog.askopenfilenames(
            title="Выберите файлы-контейнеры",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )

        if not files:
            return

        for file in files:
            if file not in self.selected_files:
                if len(self.selected_files) >= 5:
                    messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                    break

                file_info = Utils.get_file_info(file)
                file_type = file_info.get("type", "unknown").capitalize()
                file_size = file_info.get("size_formatted", "N/A")

                self.selected_files.append(file)
                self.files_tree.insert(
                    "", "end",
                    values=(len(self.selected_files), os.path.basename(file), file_type, file_size)
                )

        self.update_ui_state()

    def remove_selected_file(self):
        """Удаляет выбранный файл из списка"""
        selected = self.files_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите файл для удаления")
            return

        item = selected[0]
        index = self.files_tree.index(item)

        if 0 <= index < len(self.selected_files):
            del self.selected_files[index]
            self.files_tree.delete(item)

            # Перенумеровываем оставшиеся файлы
            for i, item_id in enumerate(self.files_tree.get_children()):
                values = self.files_tree.item(item_id, "values")
                self.files_tree.item(item_id, values=(i + 1, values[1], values[2], values[3]))

        self.update_ui_state()

    def clear_files(self):
        """Очищает список файлов"""
        self.selected_files = []
        self.files_tree.delete(*self.files_tree.get_children())
        self.update_ui_state()

    def select_hide_file(self):
        """Выбирает файл для скрытия"""
        file = filedialog.askopenfilename(
            title="Выберите файл для скрытия",
            initialdir=self.app.last_open_dir
        )

        if file:
            file_size = os.path.getsize(file) / (1024 * 1024)
            if file_size > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning("⚠️ Слишком большой файл",
                                       f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ")
                return

            self.hide_file_path.set(file)
            self.app.last_open_dir = os.path.dirname(file)

            # Показываем информацию о файле
            file_info = Utils.get_file_info(file)
            info_text = f"📄 {os.path.basename(file)} • {file_info.get('size_formatted', 'N/A')}"
            if file_info.get("type") == "image":
                info_text += f" • {file_info.get('dimensions', '')}"
            elif file_info.get("type") == "audio":
                info_text += f" • {file_info.get('duration', '')}"

            self.file_info_label.config(text=info_text)

            self.update_ui_state()

    def select_output_dir(self):
        """Выбирает выходную директорию"""
        directory = filedialog.askdirectory(
            title="Выберите папку для сохранения",
            initialdir=self.output_dir.get()
        )

        if directory:
            self.output_dir.set(directory)
            self.update_ui_state()

    def update_hide_data_input(self):
        """Обновляет поле ввода данных в зависимости от типа"""
        if self.hide_data_type.get() == "text":
            self.hide_file_frame.pack_forget()
            self.hide_text_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        else:
            self.hide_text_frame.pack_forget()
            self.hide_file_frame.pack(fill=tk.X, pady=(10, 0))

        self.update_ui_state()

    # Методы обработки
    def start_batch_processing(self):
        """Начинает пакетную обработку и обновляет состояние интерфейса"""
        self.processing = True
        self.update_ui_state()
        self.current_operation_label.config(text=f"Текущая операция: {self.current_operation}")

    def complete_batch_processing(self):
        """Завершает пакетную обработку и обновляет состояние интерфейса"""
        self.processing = False
        self.update_ui_state()
        self.current_operation_label.config(text="Текущая операция: нет")
        self.batch_status_label.config(text="✅ Обработка завершена")

    def stop_processing(self):
        """Останавливает обработку"""
        if self.processing:
            self.batch_processor.cancel_processing()
            self.batch_status_label.config(text="⏹️ Обработка остановлена")
            self.app.notification_manager.show_notification(
                "Обработка была остановлена пользователем",
                "info",
                duration=3000
            )
            # После остановки обработки нужно обновить состояние
            self.processing = False
            self.update_ui_state()
        else:
            messagebox.showinfo("Информация", "Обработка не выполняется")

    # Дополнительные вспомогательные методы
    def sort_treeview(self, tree, col, reverse):
        """Сортирует Treeview по указанному столбцу"""
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # Обработка числовых значений
        if col in ["#", "Размер"]:
            try:
                data.sort(key=lambda x: float(x[0].replace('KB', '').replace('MB', '').replace(',', '').strip()),
                          reverse=reverse)
            except:
                data.sort(key=lambda x: x[0], reverse=reverse)
        else:
            data.sort(key=lambda x: x[0], reverse=reverse)

        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

        # Альтернируем цвета строк
        for i, child in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.tag_configure('evenrow', background=self.app.colors["card"])
                tree.item(child, tags=('evenrow',))
            else:
                tree.item(child, tags=())

    # Дополнительные методы для работы с извлечением и анализом
    def add_extract_files(self):
        """Добавляет файлы для извлечения"""
        files = filedialog.askopenfilenames(
            title="Выберите стего-файлы",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )

        if not files:
            return

        for file in files:
            if file not in self.selected_extract_files:
                if len(self.selected_extract_files) >= 5:
                    messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                    break

                file_info = Utils.get_file_info(file)
                file_type = file_info.get("type", "unknown").capitalize()
                file_size = file_info.get("size_formatted", "N/A")

                self.selected_extract_files.append(file)
                self.extract_files_tree.insert(
                    "", "end",
                    values=(len(self.selected_extract_files), os.path.basename(file), file_type, file_size)
                )

        self.update_ui_state()

    def remove_selected_extract_file(self):
        """Удаляет выбранный файл из списка для извлечения"""
        selected = self.extract_files_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите файл для удаления")
            return

        item = selected[0]
        index = self.extract_files_tree.index(item)

        if 0 <= index < len(self.selected_extract_files):
            del self.selected_extract_files[index]
            self.extract_files_tree.delete(item)

            # Перенумеровываем оставшиеся файлы
            for i, item_id in enumerate(self.extract_files_tree.get_children()):
                values = self.extract_files_tree.item(item_id, "values")
                self.extract_files_tree.item(item_id, values=(i + 1, values[1], values[2], values[3]))

        self.update_ui_state()

    def select_extract_output_dir(self):
        """Выбирает выходную директорию для извлечения"""
        directory = filedialog.askdirectory(
            title="Выберите папку для сохранения извлеченных данных",
            initialdir=self.extract_output_dir.get()
        )

        if directory:
            self.extract_output_dir.set(directory)
            self.update_ui_state()

    def update_extract_files_list(self):
        """Обновляет список файлов для извлечения"""
        self.extract_files_tree.delete(*self.extract_files_tree.get_children())
        for i, file in enumerate(self.selected_extract_files):
            file_info = Utils.get_file_info(file)
            file_type = file_info.get("type", "unknown").capitalize()
            file_size = file_info.get("size_formatted", "N/A")
            self.extract_files_tree.insert(
                "", "end",
                values=(i + 1, os.path.basename(file), file_type, file_size)
            )

    # Дополнительные методы для работы с анализом
    def add_analyze_files(self):
        """Добавляет файлы для анализа"""
        files = filedialog.askopenfilenames(
            title="Выберите файлы для анализа",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )

        if not files:
            return

        for file in files:
            if file not in self.selected_analyze_files:
                if len(self.selected_analyze_files) >= 5:
                    messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                    break

                file_info = Utils.get_file_info(file)
                file_type = file_info.get("type", "unknown").capitalize()
                file_size = file_info.get("size_formatted", "N/A")

                self.selected_analyze_files.append(file)
                self.analyze_files_tree.insert(
                    "", "end",
                    values=(len(self.selected_analyze_files), os.path.basename(file), file_type, file_size)
                )

        self.update_ui_state()

    def remove_selected_analyze_file(self):
        """Удаляет выбранный файл из списка для анализа"""
        selected = self.analyze_files_tree.selection()
        if not selected:
            messagebox.showinfo("Информация", "Выберите файл для удаления")
            return

        item = selected[0]
        index = self.analyze_files_tree.index(item)

        if 0 <= index < len(self.selected_analyze_files):
            del self.selected_analyze_files[index]
            self.analyze_files_tree.delete(item)

            # Перенумеровываем оставшиеся файлы
            for i, item_id in enumerate(self.analyze_files_tree.get_children()):
                values = self.analyze_files_tree.item(item_id, "values")
                self.analyze_files_tree.item(item_id, values=(i + 1, values[1], values[2], values[3]))

        self.update_ui_state()

    def update_analyze_files_list(self):
        """Обновляет список файлов для анализа"""
        self.analyze_files_tree.delete(*self.analyze_files_tree.get_children())
        for i, file in enumerate(self.selected_analyze_files):
            file_info = Utils.get_file_info(file)
            file_type = file_info.get("type", "unknown").capitalize()
            file_size = file_info.get("size_formatted", "N/A")
            self.analyze_files_tree.insert(
                "", "end",
                values=(i + 1, os.path.basename(file), file_type, file_size)
            )

    # Остальные методы остаются без изменений
    def clear_all(self):
        """Очищает все списки и результаты"""
        # Очистка списков
        self.selected_files = []
        self.selected_extract_files = []
        self.selected_analyze_files = []

        # Очистка результатов
        if hasattr(self, 'results_tree'):
            self.results_tree.delete(*self.results_tree.get_children())

        # Очистка виджетов
        self.files_tree.delete(*self.files_tree.get_children())
        self.extract_files_tree.delete(*self.extract_files_tree.get_children())
        self.analyze_files_tree.delete(*self.analyze_files_tree.get_children())

        # Очистка полей ввода
        if hasattr(self, 'hide_text'):
            self.hide_text.delete("1.0", tk.END)
        self.hide_file_path.set("")
        self.hide_password.set("")
        self.extract_password.set("")
        self.extract_method.set("")

        # Сброс состояния обработки
        self.processing = False
        self.batch_progress_var.set(0)
        self.batch_status_label.config(text="✅ Готов к обработке")
        self.current_operation_label.config(text="Текущая операция: нет")
        self.stats_label.config(text="Всего: 0 | Обработано: 0 | Успешно: 0 | Ошибки: 0")

        # Обновление состояния кнопок
        self.update_ui_state()

        messagebox.showinfo("Очистка", "Все списки и результаты очищены")

    def show_help(self):
        """Показывает помощь по пакетной обработке"""
        help_text = """
📚 Помощь по пакетной обработке

🎯 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
• Скрытие данных в до 5 контейнерах одновременно
• Извлечение данных из до 5 стего-файлов одновременно
• Анализ до 5 файлов на наличие скрытых данных
• Автоматическое определение методов при извлечении
• Подробная статистика и отчеты об операциях

📋 ПРАВИЛА ИСПОЛЬЗОВАНИЯ:
1. Для скрытия данных:
   - Выберите до 5 контейнеров (PNG, BMP, TIFF, TGA, JPG, WAV)
   - Укажите данные для скрытия (текст или файл)
   - Выберите метод скрытия и настройки
   - Укажите папку для сохранения результатов
   - Нажмите "🚀 Начать пакетное скрытие"

2. Для извлечения данных:
   - Выберите до 5 стего-файлов
   - Укажите пароль (если требуется)
   - Выберите метод или оставьте для автоопределения
   - Укажите папку для сохранения результатов
   - Нажмите "🚀 Начать пакетное извлечение"

3. Для анализа:
   - Выберите до 5 файлов для проверки
   - Нажмите "🔍 Начать анализ"
   - Просмотрите результаты в таблице

💡 СОВЕТЫ:
• Убедитесь, что достаточно свободного места на диске
• Используйте lossless-форматы (PNG, BMP) для максимальной вместимости
• Для аудио используйте WAV формат без сжатия
• Регулярно сохраняйте отчеты об операциях
• При ошибках проверяйте логи для диагностики проблем

⚠️ ОГРАНИЧЕНИЯ:
• Максимум 5 файлов за одну операцию
• Максимальный размер скрываемого файла: 100 МБ
• Все файлы обрабатываются с одинаковыми настройками

🔄 УПРАВЛЕНИЕ:
• Используйте кнопки "➕ Добавить файлы" и "🗑️ Удалить выбранное" для управления списками
• Нажмите "🧹 Очистить список" для полной очистки
• "⏹️ Остановить обработку" прекратит текущую операцию
• "📊 Экспорт результатов" сохранит отчет в JSON формате
        """

        help_window = tk.Toplevel(self.app.root)
        help_window.title("📚 Помощь по пакетной обработке")
        help_window.geometry("800x600")
        help_window.transient(self.app.root)
        help_window.grab_set()

        # Текст помощи с прокруткой
        text_frame = ttk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            padx=10,
            pady=10
        )
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert("1.0", help_text)
        text_area.config(state=tk.DISABLED)

        # Кнопка закрытия
        ttk.Button(
            help_window,
            text="❌ Закрыть",
            style="Accent.TButton",
            command=help_window.destroy
        ).pack(pady=10)

    def export_batch_results(self):
        """Экспортирует результаты обработки"""
        if self.total_files == 0:
            messagebox.showwarning("Ошибка", "Нет результатов для экспорта")
            return

        file_path = filedialog.asksaveasfilename(
            title="Сохранить результаты",
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            initialdir=self.app.last_save_dir
        )

        if file_path:
            try:
                # Собираем данные для экспорта
                export_data = {
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "operation_type": ["hide", "extract", "analyze"][
                        self.batch_notebook.index(self.batch_notebook.select())],
                    "total_files": self.total_files,
                    "success_count": self.success_count,
                    "fail_count": self.fail_count,
                    "success_rate": (self.success_count / self.total_files * 100) if self.total_files > 0 else 0,
                    "files": []
                }

                # Добавляем информацию о каждом файле
                if self.batch_notebook.index(self.batch_notebook.select()) == 0:  # Скрытие
                    for i, file in enumerate(self.selected_files):
                        file_info = Utils.get_file_info(file)
                        export_data["files"].append({
                            "index": i + 1,
                            "path": file,
                            "filename": os.path.basename(file),
                            "size": file_info.get("size", 0),
                            "type": file_info.get("type", "unknown"),
                            "status": "success" if i < self.success_count else "failed"
                        })
                elif self.batch_notebook.index(self.batch_notebook.select()) == 1:  # Извлечение
                    for i, file in enumerate(self.selected_extract_files):
                        file_info = Utils.get_file_info(file)
                        export_data["files"].append({
                            "index": i + 1,
                            "path": file,
                            "filename": os.path.basename(file),
                            "size": file_info.get("size", 0),
                            "type": file_info.get("type", "unknown"),
                            "status": "success" if i < self.success_count else "failed"
                        })
                else:  # Анализ
                    for i, file in enumerate(self.selected_analyze_files):
                        file_info = Utils.get_file_info(file)
                        export_data["files"].append({
                            "index": i + 1,
                            "path": file,
                            "filename": os.path.basename(file),
                            "size": file_info.get("size", 0),
                            "type": file_info.get("type", "unknown"),
                            "status": "success" if i < self.success_count else "failed"
                        })

                # Сохраняем файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

                messagebox.showinfo("Успех", f"Результаты успешно экспортированы в файл:\n{file_path}")
                self.app.last_save_dir = os.path.dirname(file_path)
                self.app.show_toast("✅ Результаты экспортированы")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать результаты:\n{str(e)}")

    # Методы для обработки
    def start_batch_hide(self):
        """Запускает пакетное скрытие"""
        if not self.selected_files:
            messagebox.showwarning("Ошибка", "Не выбраны файлы для обработки")
            return

        # Ограничение до 5 файлов
        files_to_process = self.selected_files[:5]

        # Подготовка данных
        data = None
        if self.hide_data_type.get() == "text":
            data = self.hide_text.get("1.0", tk.END).strip().encode('utf-8')
            if not data:
                messagebox.showwarning("Ошибка", "Не введен текст для скрытия")
                return
        else:
            file_path = self.hide_file_path.get()
            if not file_path or not os.path.exists(file_path):
                messagebox.showwarning("Ошибка", "Не выбран файл для скрытия")
                return
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")
                return

        # Проверка выходной директории
        output_dir = self.output_dir.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать выходную директорию: {e}")
                return

        # Подготовка параметров
        params = {
            'data': data,
            'method': self.method_var.get(),
            'password': self.hide_password.get(),
            'output_dir': output_dir,
            'overwrite': self.overwrite_var.get(),
            'compression_level': self.app.compression_level.get()
        }

        # Добавление в очередь
        self.batch_processor.clear_batch()
        self.batch_processor.add_to_batch(files_to_process, 'hide', params)

        # Сброс статистики
        self.total_files = len(files_to_process)
        self.success_count = 0
        self.fail_count = 0

        # Запуск обработки
        self.current_operation = "Скрытие данных"
        self.start_batch_processing()
        self.process_batch()

    def start_batch_extract(self):
        """Запускает пакетное извлечение"""
        if not self.selected_extract_files:
            messagebox.showwarning("Ошибка", "Не выбраны файлы для извлечения")
            return

        # Ограничение до 5 файлов
        files_to_process = self.selected_extract_files[:5]

        # Проверка существования файлов
        for file in files_to_process:
            if not os.path.exists(file):
                messagebox.showerror("Ошибка", f"Файл не найден: {file}")
                return

        # Проверка выходной директории
        output_dir = self.extract_output_dir.get()
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось создать выходную директорию: {e}")
                return

        # Подготовка параметров
        method = self.extract_method.get() if self.extract_method.get() else None
        params = {
            'password': self.extract_password.get(),
            'method': method,
            'output_dir': output_dir,
            'auto_save': self.auto_save_var.get()
        }

        # Добавление в очередь
        self.batch_processor.clear_batch()
        self.batch_processor.add_to_batch(files_to_process, 'extract', params)

        # Сброс статистики
        self.total_files = len(files_to_process)
        self.success_count = 0
        self.fail_count = 0

        # Запуск обработки
        self.current_operation = "Извлечение данных"
        self.start_batch_processing()
        self.process_batch()

    def start_batch_analyze(self):
        """Запускает пакетный анализ"""
        if not self.selected_analyze_files:
            messagebox.showwarning("Ошибка", "Не выбраны файлы для анализа")
            return

        # Ограничение до 5 файлов
        files_to_process = self.selected_analyze_files[:5]

        # Проверка существования файлов
        for file in files_to_process:
            if not os.path.exists(file):
                messagebox.showerror("Ошибка", f"Файл не найден: {file}")
                return

        # Подготовка параметров
        params = {}

        # Добавление в очередь
        self.batch_processor.clear_batch()
        self.batch_processor.add_to_batch(files_to_process, 'analyze', params)

        # Сброс статистики
        self.total_files = len(files_to_process)
        self.success_count = 0
        self.fail_count = 0

        # Запуск обработки
        self.current_operation = "Анализ файлов"
        self.start_batch_processing()
        self.process_batch()

    def process_batch(self):
        """Обрабатывает очередь файлов и корректно обновляет UI"""
        try:
            # Получаем текущую операцию
            current_tab = self.batch_notebook.index(self.batch_notebook.select())
            operation_type = ["hide", "extract", "analyze"][current_tab]

            # Очищаем предыдущие результаты
            if hasattr(self, 'results_tree'):
                self.results_tree.delete(*self.results_tree.get_children())

            # Обработка каждого файла
            for i, task in enumerate(self.batch_processor.batch_queue):
                if self.batch_processor.cancel_requested:
                    break

                try:
                    # Обновляем прогресс
                    progress = (i / self.total_files) * 100
                    status = f"Обработка файла {i + 1} из {self.total_files}: {os.path.basename(task['path'])}"

                    self.batch_progress_var.set(progress)
                    self.batch_status_label.config(text=status)
                    self.current_operation_label.config(text=f"Текущая операция: {status}")
                    self.stats_label.config(
                        text=f"Всего: {self.total_files} | Обработано: {i} | Успешно: {self.success_count} | Ошибки: {self.fail_count}")

                    # Обновляем UI
                    self.app.root.update_idletasks()

                    # Обрабатываем задачу
                    if operation_type == 'hide':
                        result = self.process_hide(task)
                    elif operation_type == 'extract':
                        result = self.process_extract(task)
                    elif operation_type == 'analyze':
                        result = self.process_analyze(task)
                    else:
                        raise ValueError(f"Неизвестная операция: {operation_type}")

                    # Обновляем статистику
                    if result['success']:
                        self.success_count += 1
                    else:
                        self.fail_count += 1

                    # Добавляем результат в таблицу анализа
                    if operation_type == 'analyze' and hasattr(self, 'results_tree'):
                        self.add_analysis_result_to_table(i + 1, task['path'], result)

                except Exception as e:
                    self.fail_count += 1
                    error_msg = f"Ошибка обработки {os.path.basename(task['path'])}: {str(e)}"
                    self.app.notification_manager.show_notification(error_msg, "error", duration=3000)

            # Завершение обработки
            self.complete_batch_processing()
            self.show_final_results(operation_type)

        except Exception as e:
            error_msg = f"Критическая ошибка при обработке: {str(e)}"
            self.batch_status_label.config(text="❌ Критическая ошибка")
            self.app.notification_manager.show_notification(error_msg, "error", duration=5000)
            self.complete_batch_processing()

    def show_final_results(self, operation_type):
        """Показывает финальные результаты обработки"""
        message = (
            f"Пакетная операция завершена!\n"
            f"Всего файлов: {self.total_files}\n"
            f"Успешно: {self.success_count}\n"
            f"С ошибками: {self.fail_count}\n"
            f"Процент успеха: {(self.success_count / self.total_files * 100) if self.total_files > 0 else 0:.1f}%"
        )

        # Определяем тип уведомления
        notification_type = "success" if self.fail_count == 0 else "warning" if self.success_count > 0 else "error"

        # Обновляем статус
        status_text = (
            "✅ Обработка успешно завершена" if self.fail_count == 0 else
            "⚠️ Обработка завершена с предупреждениями" if self.success_count > 0 else
            "❌ Обработка завершена с ошибками"
        )

        # Обновляем UI
        self.batch_status_label.config(text=status_text)
        self.current_operation_label.config(text="Текущая операция: нет")
        self.stats_label.config(
            text=f"Всего: {self.total_files} | Обработано: {self.total_files} | Успешно: {self.success_count} | Ошибки: {self.fail_count}")

        # Показываем уведомление
        self.app.notification_manager.show_notification(
            message,
            notification_type,
            duration=5000
        )

    # Остальные методы обработки (process_hide, process_extract, process_analyze) остаются без изменений
    def process_hide(self, task):
        """Обрабатывает операцию скрытия"""
        container_path = task['path']
        output_dir = task['params'].get('output_dir', os.path.dirname(container_path))
        method = task['params'].get('method', 'lsb')
        password = task['params'].get('password', '')
        data = task['params'].get('data')
        overwrite = task['params'].get('overwrite', False)
        compression_level = task['params'].get('compression_level', 9)

        try:
            # Проверка существования файла
            if not os.path.exists(container_path):
                raise FileNotFoundError(f"Файл не найден: {container_path}")

            # Проверка поддерживаемого формата
            if not Utils.is_supported_container(container_path):
                raise ValueError(f"Неподдерживаемый формат файла: {container_path}")

            # Подготовка выходного пути
            base_name = os.path.splitext(os.path.basename(container_path))[0]
            ext = os.path.splitext(container_path)[1].lower()
            output_name = f"{base_name}_stego{ext if ext != '.wav' else '.wav'}"
            output_path = os.path.join(output_dir, output_name)

            # Проверка перезаписи
            if os.path.exists(output_path) and not overwrite:
                counter = 1
                while os.path.exists(output_path):
                    name, ext = os.path.splitext(output_name)
                    output_path = os.path.join(output_dir, f"{name}_{counter}{ext}")
                    counter += 1

            # Выполнение скрытия в зависимости от типа файла
            ext = os.path.splitext(container_path)[1].lower()

            if ext == '.wav':
                # Аудио обработка
                AudioStego.hide_lsb_wav(container_path, data, output_path)
            elif ext in ['.jpg', '.jpeg'] and method == 'jpeg_dct':
                # JPEG DCT обработка
                JPEGStego.hide_dct(container_path, data, output_path)
            else:
                # Обычная обработка изображений
                ImageProcessor.hide_data(
                    container_path,
                    data,
                    password,
                    output_path,
                    method=method,
                    compression_level=compression_level
                )

            # Возвращаем результат
            return {
                'success': True,
                'file': container_path,
                'output': output_path,
                'operation': 'hide',
                'method': method,
                'size': os.path.getsize(output_path) if os.path.exists(output_path) else 0
            }

        except Exception as e:
            return {
                'success': False,
                'file': container_path,
                'error': str(e),
                'operation': 'hide'
            }

    def process_extract(self, task):
        """Обрабатывает операцию извлечения"""
        stego_path = task['path']
        params = task['params']

        try:
            # Проверка существования файла
            if not os.path.exists(stego_path):
                raise FileNotFoundError(f"Файл не найден: {stego_path}")

            # Подготовка выходного пути
            output_dir = params.get('output_dir', os.path.dirname(stego_path))
            os.makedirs(output_dir, exist_ok=True)

            # Генерируем уникальное имя файла
            base_name = os.path.splitext(os.path.basename(stego_path))[0]
            output_name = f"extracted_{base_name}"

            # Проверяем, является ли файл аудио
            ext = os.path.splitext(stego_path)[1].lower()

            if ext == '.wav':
                # Для аудио файлов
                extracted_data = AudioStego.extract_lsb_wav(stego_path)
            else:
                # Для изображений
                method = params.get('method')
                password = params.get('password', '')

                try:
                    # Пробуем извлечь данные
                    if method:
                        extracted_data = ImageProcessor.extract_data(
                            stego_path,
                            password,
                            method
                        )
                    else:
                        # Автоопределение метода
                        extracted_data = ImageProcessor.extract_data(stego_path, password)
                except Exception as e:
                    # Если не получилось, пробуем другие методы
                    methods_to_try = ["lsb", "noise", "aelsb", "hill"]
                    for m in methods_to_try:
                        try:
                            extracted_data = ImageProcessor.extract_data(stego_path, password, m)
                            method = m  # Запоминаем успешный метод
                            break
                        except Exception:
                            continue
                    else:
                        raise e

            # Определяем тип данных и расширение
            data_type = self.guess_data_type(extracted_data[:100])
            extensions = {
                'text': '.txt',
                'json': '.json',
                'png': '.png',
                'jpeg': '.jpg',
                'jpg': '.jpg',
                'gif': '.gif',
                'bmp': '.bmp',
                'zip': '.zip',
                'rar': '.rar',
                'pdf': '.pdf',
                'binary': '.bin'
            }
            ext = extensions.get(data_type, '.bin')
            output_path = os.path.join(output_dir, f"{output_name}{ext}")

            # Проверяем необходимость уникального имени
            if params.get('auto_save', True) and os.path.exists(output_path) and not params.get('overwrite', False):
                counter = 1
                original_output_path = output_path
                while os.path.exists(output_path):
                    name, ext = os.path.splitext(original_output_path)
                    output_path = f"{name}_{counter}{ext}"
                    counter += 1

            # Сохранение данных если нужно
            if params.get('auto_save', True):
                with open(output_path, 'wb') as f:
                    f.write(extracted_data)

            # Анализ данных
            data_info = self.analyze_extracted_data(extracted_data)

            return {
                'success': True,
                'file': stego_path,
                'output': output_path if params.get('auto_save', True) else None,
                'data': extracted_data,
                'data_info': data_info,
                'size': len(extracted_data),
                'operation': 'extract',
                'data_type': data_type,
                'method': method or "auto"
            }

        except Exception as e:
            return {
                'success': False,
                'file': stego_path,
                'error': str(e),
                'operation': 'extract'
            }

    def process_analyze(self, task):
        """Обрабатывает операцию анализа"""
        file_path = task['path']

        try:
            # Проверка существования файла
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл не найден: {file_path}")

            # Получаем информацию о файле
            file_info = Utils.get_file_info(file_path)

            # Проверяем на наличие скрытых данных
            has_stego = False
            stego_info = None
            detected_method = "не определен"

            try:
                # Пробуем извлечь данные разными методами
                methods_to_try = ["lsb", "noise", "aelsb", "hill", "audio_lsb"]
                for method in methods_to_try:
                    try:
                        if method == "audio_lsb" and not file_path.lower().endswith('.wav'):
                            continue

                        test_data = None
                        if method == "audio_lsb":
                            test_data = AudioStego.extract_lsb_wav(file_path)
                        else:
                            test_data = ImageProcessor.extract_data(file_path, '', method)

                        if test_data and len(test_data) > 0:
                            has_stego = True
                            detected_method = method
                            stego_info = {
                                'size': len(test_data),
                                'method': method,
                                'data_type': self.guess_data_type(test_data[:100])
                            }
                            break
                    except Exception:
                        continue
            except Exception as e:
                pass  # Продолжаем анализ даже если не удалось определить скрытые данные

            # Проверяем вместимость
            capacity_info = {}
            w, h, bits = 0, 0, 0

            if file_info['type'] == 'image':
                try:
                    w, h, bits = ImageProcessor.get_image_info(file_path)
                    for method in ['lsb', 'noise', 'aelsb', 'hill']:
                        capacity = ImageProcessor.get_capacity_by_method(bits, method, w, h)
                        capacity_info[method] = capacity
                except Exception:
                    pass

            return {
                'success': True,
                'file': file_path,
                'file_info': file_info,
                'has_stego': has_stego,
                'stego_info': stego_info,
                'detected_method': detected_method,
                'capacity_info': capacity_info,
                'operation': 'analyze'
            }

        except Exception as e:
            return {
                'success': False,
                'file': file_path,
                'error': str(e),
                'operation': 'analyze'
            }

    # Вспомогательные методы
    def guess_data_type(self, data):
        """Пытается определить тип данных"""
        if not data:
            return 'unknown'

        # Проверка на текст
        try:
            text = data.decode('utf-8', errors='ignore')
            text_ratio = len(text) / len(data)
            if text_ratio > 0.8:
                return 'text'
            elif text_ratio > 0.5:
                return 'mixed'
        except:
            pass

        # Проверка магических чисел
        magic_numbers = {
            b'\x89PNG\r\n\x1a\n': 'png',
            b'\xff\xd8\xff': 'jpeg',
            b'GIF': 'gif',
            b'BM': 'bmp',
            b'PK\x03\x04': 'zip',
            b'Rar!': 'rar',
            b'%PDF': 'pdf'
        }

        for magic, filetype in magic_numbers.items():
            if data.startswith(magic):
                return filetype

        return 'binary'

    def analyze_extracted_data(self, data):
        """Анализирует извлеченные данные"""
        if not data:
            return {'type': 'empty', 'size': 0}

        # Пытаемся определить тип данных
        try:
            # Проверка на текст
            text = data.decode('utf-8', errors='ignore')
            if len(text) > len(data) * 0.7:  # Большая часть данных - текст
                return {
                    'type': 'text',
                    'size': len(data),
                    'preview': text[:100],
                    'is_utf8': True
                }
        except:
            pass

        # Проверка на JSON
        try:
            json.loads(data.decode('utf-8'))
            return {'type': 'json', 'size': len(data)}
        except:
            pass

        # Проверка на изображение
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(data))
            return {
                'type': 'image',
                'size': len(data),
                'format': img.format,
                'dimensions': f"{img.width}x{img.height}"
            }
        except:
            pass

        # Проверка на архив
        if data[:4] in [b'PK\x03\x04', b'Rar!', b'7z\xBC\xAF']:
            return {'type': 'archive', 'size': len(data)}

        # По умолчанию - бинарные данные
        return {'type': 'binary', 'size': len(data)}

    def add_analysis_result_to_table(self, index, file_path, result):
        """Добавляет результат анализа в таблицу результатов"""
        if not result['success']:
            self.results_tree.insert(
                "", "end",
                values=(index, os.path.basename(file_path), "❌ Ошибка", "", "", ""),
                tags=('error',)
            )
            return

        has_stego = result.get('has_stego', False)
        method = result.get('detected_method', "не определен")
        stego_info = result.get('stego_info', {})
        capacity_info = result.get('capacity_info', {})

        # Определяем размер данных
        data_size = stego_info.get('size', 0) if has_stego else 0

        # Определяем вместимость
        total_capacity = 0
        if capacity_info:
            # Берем вместимость для LSB как максимальную
            total_capacity = capacity_info.get('lsb', 0)

        # Определяем тег для цвета
        tag = 'success' if has_stego else 'warning'

        self.results_tree.insert(
            "", "end",
            values=(
                index,
                os.path.basename(file_path),
                "✅ Да" if has_stego else "❌ Нет",
                method if has_stego else "-",
                Utils.format_size(data_size) if has_stego else "-",
                Utils.format_size(total_capacity)
            ),
            tags=(tag,)
        )

        # Настраиваем теги для цветов
        self.results_tree.tag_configure('success', background=self.app.colors["success"], foreground="white")
        self.results_tree.tag_configure('warning', background=self.app.colors["warning"], foreground="black")
        self.results_tree.tag_configure('error', background=self.app.colors["error"], foreground="white")

    @property
    def root(self):
        """Возвращает корневой виджет для обновления UI из потоков"""
        return self.app.root



class EncryptionManager:
    """Полнофункциональный менеджер шифрования с поддержкой современных алгоритмов (реализация на PyCryptodome)"""

    SUPPORTED_ALGORITHMS = {
        # Симметричные алгоритмы
        "aes_256_cbc": "AES-256 CBC (Симметричное, стандартное)",
        "aes_256_gcm": "AES-256 GCM (С аутентификацией данных)",
        "aes_256_ctr": "AES-256 CTR (Потоковый режим, высокая скорость)",
        "aes_256_ofb": "AES-256 OFB (Устойчивость к ошибкам)",
        "chacha20_poly1305": "ChaCha20-Poly1305 (Высокая скорость + аутентификация)",
        "chacha20": "ChaCha20 (Высокая скорость, без аутентификации)",
        "xor": "XOR (Учебный, НЕ для реального использования)",
        "base64": "Base64 (Кодирование, не шифрование)"
    }

    SECURITY_LEVELS = {
        "aes_256_cbc": "high",
        "aes_256_gcm": "very_high",
        "aes_256_ctr": "high",
        "aes_256_ofb": "medium",
        "chacha20_poly1305": "very_high",
        "chacha20": "high",
        "xor": "none",
        "base64": "none"
    }

    @staticmethod
    def get_algorithm_info(algorithm: str) -> Dict[str, Any]:
        """Возвращает подробную информацию об алгоритме для документации"""
        info = {
            "aes_256_cbc": {
                "name": "AES-256 CBC",
                "description": "Блочный шифр с 256-битным ключом в режиме сцепления блоков шифротекста",
                "security": "Высокая (при правильной реализации)",
                "use_cases": "Общее шифрование файлов и данных",
                "limitations": "Требует паддинг, уязвим к атакам на повторение блоков без случайного IV",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "iv_size": "16 байт",
                "authentication": "Нет (рекомендуется использовать с отдельной MAC)",
                "performance": "Высокая скорость шифрования/дешифрования"
            },
            "aes_256_gcm": {
                "name": "AES-256 GCM",
                "description": "Режим Галуа/Счётчика с встроенной аутентификацией данных (AEAD)",
                "security": "Очень высокая (рекомендуется для новых систем)",
                "use_cases": "Защита конфиденциальности и целостности данных",
                "limitations": "Ограничение на размер данных (~64 ГБ на ключ)",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "iv_size": "12 байт (рекомендуется)",
                "authentication": "Встроенная (128-битный тег аутентификации)",
                "performance": "Высокая скорость с аппаратной поддержкой на современных CPU"
            },
            "aes_256_ctr": {
                "name": "AES-256 CTR",
                "description": "Режим счётчика, преобразует блочный шифр в потоковый",
                "security": "Высокая (при уникальном nonce)",
                "use_cases": "Параллельная обработка, шифрование потоков",
                "limitations": "Критически важно никогда не повторять nonce с одним ключом",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "iv_size": "16 байт (8 байт nonce + 8 байт счётчик)",
                "authentication": "Нет (рекомендуется комбинировать с HMAC)",
                "performance": "Очень высокая, поддерживает параллелизм"
            },
            "aes_256_ofb": {
                "name": "AES-256 OFB",
                "description": "Режим обратной связи вывода, создаёт потоковый шифр",
                "security": "Средняя (устаревший режим)",
                "use_cases": "Шифрование в средах с высоким уровнем ошибок",
                "limitations": "Не обеспечивает аутентификацию, уязвим к атакам на битовые флипы",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "iv_size": "16 байт",
                "authentication": "Нет",
                "performance": "Хорошая скорость, но не рекомендуется для новых систем"
            },
            "chacha20_poly1305": {
                "name": "ChaCha20-Poly1305",
                "description": "Современный потоковый шифр с аутентификацией (стандарт IETF RFC 8439)",
                "security": "Очень высокая (рекомендуется для мобильных устройств)",
                "use_cases": "TLS 1.3, защищённая передача данных, мобильные приложения",
                "limitations": "Ограничение на 2^32 блоков на ключ/nonce",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "nonce_size": "12 байт",
                "authentication": "Встроенная (128-битный тег Poly1305)",
                "performance": "Высокая скорость на CPU без аппаратного ускорения AES"
            },
            "chacha20": {
                "name": "ChaCha20",
                "description": "Потоковый шифр без встроенной аутентификации",
                "security": "Высокая (но без проверки целостности)",
                "use_cases": "Когда аутентификация обеспечивается отдельно",
                "limitations": "Требует отдельной аутентификации для защиты от модификации",
                "key_derivation": "PBKDF2-HMAC-SHA256 (600 000 итераций)",
                "nonce_size": "16 байт",
                "authentication": "Нет",
                "performance": "Очень высокая скорость на всех платформах"
            },
            "xor": {
                "name": "XOR",
                "description": "Простейшая операция побитового исключающего ИЛИ",
                "security": "Отсутствует (тривиально взламывается)",
                "use_cases": "Только для образовательных целей",
                "limitations": "Полностью небезопасен, не скрывает статистические паттерны",
                "key_derivation": "Нет (ключ используется напрямую)",
                "authentication": "Нет",
                "performance": "Максимальная скорость",
                "warning": "НИКОГДА не используйте для защиты реальных данных!"
            },
            "base64": {
                "name": "Base64",
                "description": "Кодирование двоичных данных в текстовый формат ASCII",
                "security": "Отсутствует (обратимое преобразование без ключа)",
                "use_cases": "Передача двоичных данных в текстовых протоколах (email, JSON)",
                "limitations": "Не является шифрованием, данные легко декодируются",
                "authentication": "Нет",
                "performance": "Высокая скорость",
                "warning": "Base64 НЕ ЗАЩИЩАЕТ данные! Это просто кодирование."
            }
        }
        return info.get(algorithm, {
            "name": algorithm,
            "description": "Информация недоступна",
            "security": "Неизвестно",
            "use_cases": "Неизвестно",
            "limitations": "Неизвестно"
        })

    @staticmethod
    def _derive_key(password: str, salt: bytes, algorithm: str = "aes_256") -> bytes:
        """Универсальная функция для генерации ключа из пароля (реализация на PyCryptodome)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Используем тот же алгоритм и параметры, что и в оригинале
        key = PBKDF2(
            password=password.encode('utf-8'),
            salt=salt,
            dkLen=32,  # 256 бит для AES-256
            count=600000,  # Тот же параметр итераций
            hmac_hash_module=SHA256
        )
        return key

    @staticmethod
    def encrypt_aes_cbc(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с использованием AES-256 в режиме CBC (реализация на PyCryptodome)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "aes_256")

        # Генерация IV (16 байт для AES)
        iv = get_random_bytes(16)

        # Добавление паддинга PKCS7 (идентично оригиналу)
        padded_data = pad(data, AES.block_size)

        # Шифрование
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(padded_data)

        # Контрольная сумма для проверки целостности (идентично оригиналу)
        checksum = hashlib.sha256(ciphertext).digest()

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'iv': iv,
            'checksum': checksum,
            'algorithm': 'aes_256_cbc',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_aes_cbc(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование AES-256 CBC с проверкой целостности (реализация на PyCryptodome)"""
        required_keys = ['ciphertext', 'salt', 'iv', 'checksum', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'aes_256_cbc':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "aes_256")

        # Проверка целостности (идентично оригиналу)
        actual_checksum = hashlib.sha256(encrypted_data['ciphertext']).digest()
        if not secrets.compare_digest(actual_checksum, encrypted_data['checksum']):
            raise ValueError("Данные повреждены (контрольная сумма не совпадает)")

        # Дешифрование
        cipher = AES.new(key, AES.MODE_CBC, encrypted_data['iv'])
        padded_plaintext = cipher.decrypt(encrypted_data['ciphertext'])

        # Удаление паддинга
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext

    @staticmethod
    def encrypt_aes_gcm(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с использованием AES-256 в режиме GCM (с аутентификацией) (реализация на PyCryptodome)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "aes_256")

        # Генерация nonce (12 байт для GCM - стандартное значение)
        nonce = get_random_bytes(12)

        # Шифрование с аутентификацией
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'nonce': nonce,
            'tag': tag,
            'algorithm': 'aes_256_gcm',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_aes_gcm(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование AES-256 GCM с проверкой аутентификации (реализация на PyCryptodome)"""
        required_keys = ['ciphertext', 'salt', 'nonce', 'tag', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'aes_256_gcm':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "aes_256")

        # Дешифрование с проверкой тега
        cipher = AES.new(key, AES.MODE_GCM, nonce=encrypted_data['nonce'])
        try:
            plaintext = cipher.decrypt_and_verify(encrypted_data['ciphertext'], encrypted_data['tag'])
            return plaintext
        except (ValueError, KeyError) as e:
            raise ValueError(f"Ошибка аутентификации или расшифровки: {str(e)}")

    @staticmethod
    def encrypt_aes_ctr(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с использованием AES-256 в режиме CTR (исправленная реализация)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "aes_256")

        # Исправление ошибки: nonce для AES-CTR должен быть 8 байт (а не 16)
        # В PyCryptodome nonce для CTR режима должен быть 8 байт
        nonce = get_random_bytes(8)

        # Генерация начального значения счетчика (8 байт)
        # Преобразуем байты в целое число (64-битное)
        initial_counter = int.from_bytes(get_random_bytes(8), 'big')

        # Шифрование
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=initial_counter)
        ciphertext = cipher.encrypt(data)

        # Контрольная сумма для проверки целостности (идентично оригиналу)
        checksum = hashlib.sha256(ciphertext).digest()

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'nonce': nonce,  # 8 байт
            'initial_counter': initial_counter,  # 64-битное целое число
            'checksum': checksum,
            'algorithm': 'aes_256_ctr',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_aes_ctr(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование AES-256 CTR с проверкой целостности (исправленная реализация)"""
        required_keys = ['ciphertext', 'salt', 'nonce', 'initial_counter', 'checksum', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'aes_256_ctr':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "aes_256")

        # Проверка целостности (идентично оригиналу)
        actual_checksum = hashlib.sha256(encrypted_data['ciphertext']).digest()
        if not secrets.compare_digest(actual_checksum, encrypted_data['checksum']):
            raise ValueError("Данные повреждены (контрольная сумма не совпадает)")

        # Дешифрование
        # Важно: initial_counter должен быть целым числом (а не байтами)
        cipher = AES.new(
            key,
            AES.MODE_CTR,
            nonce=encrypted_data['nonce'],
            initial_value=encrypted_data['initial_counter']
        )
        plaintext = cipher.decrypt(encrypted_data['ciphertext'])
        return plaintext

    @staticmethod
    def encrypt_aes_ofb(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с использованием AES-256 в режиме OFB (реализация на PyCryptodome)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "aes_256")

        # Генерация IV (16 байт для AES)
        iv = get_random_bytes(16)

        # Шифрование
        cipher = AES.new(key, AES.MODE_OFB, iv)
        ciphertext = cipher.encrypt(data)

        # Контрольная сумма (идентично оригиналу)
        checksum = hashlib.sha256(ciphertext).digest()

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'iv': iv,
            'checksum': checksum,
            'algorithm': 'aes_256_ofb',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_aes_ofb(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование AES-256 OFB с проверкой целостности (реализация на PyCryptodome)"""
        required_keys = ['ciphertext', 'salt', 'iv', 'checksum', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'aes_256_ofb':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "aes_256")

        # Проверка целостности (идентично оригиналу)
        actual_checksum = hashlib.sha256(encrypted_data['ciphertext']).digest()
        if not secrets.compare_digest(actual_checksum, encrypted_data['checksum']):
            raise ValueError("Данные повреждены (контрольная сумма не совпадает)")

        # Дешифрование
        cipher = AES.new(key, AES.MODE_OFB, encrypted_data['iv'])
        plaintext = cipher.decrypt(encrypted_data['ciphertext'])
        return plaintext

    @staticmethod
    def encrypt_chacha20(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с использованием ChaCha20 (без аутентификации) (исправленная реализация)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "chacha20")

        # Исправление ошибки: nonce для ChaCha20 должен быть 12 байт (а не 16)
        # Согласно ошибке, nonce должен быть 8/12 байт для ChaCha20
        nonce = get_random_bytes(12)

        # Шифрование
        cipher = ChaCha20.new(key=key, nonce=nonce)
        ciphertext = cipher.encrypt(data)

        # Контрольная сумма (идентично оригиналу)
        checksum = hashlib.sha256(ciphertext).digest()

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'nonce': nonce,
            'checksum': checksum,
            'algorithm': 'chacha20',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_chacha20(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование ChaCha20 с проверкой целостности (исправленная реализация)"""
        required_keys = ['ciphertext', 'salt', 'nonce', 'checksum', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'chacha20':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "chacha20")

        # Проверка целостности (идентично оригиналу)
        actual_checksum = hashlib.sha256(encrypted_data['ciphertext']).digest()
        if not secrets.compare_digest(actual_checksum, encrypted_data['checksum']):
            raise ValueError("Данные повреждены (контрольная сумма не совпадает)")

        # Дешифрование
        cipher = ChaCha20.new(key=key, nonce=encrypted_data['nonce'])
        plaintext = cipher.decrypt(encrypted_data['ciphertext'])
        return plaintext

    @staticmethod
    def encrypt_chacha20_poly1305(data: bytes, password: str) -> Dict[str, Any]:
        """Шифрование с аутентификацией через ChaCha20-Poly1305 (реализация на PyCryptodome)"""
        if not password or len(password) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов для безопасности")

        # Генерация соли и ключа (идентично оригиналу)
        salt = get_random_bytes(16)
        key = EncryptionManager._derive_key(password, salt, "chacha20")

        # Генерация nonce (12 байт для Poly1305 - стандартное значение)
        nonce = get_random_bytes(12)

        # Дополнительные аутентифицированные данные (AAD) - идентично оригиналу
        aad = b"occultong_chacha20_poly1305_v1"

        # Шифрование с аутентификацией
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        cipher.update(aad)
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return {
            'ciphertext': ciphertext,
            'salt': salt,
            'nonce': nonce,
            'tag': tag,
            'aad': aad,
            'algorithm': 'chacha20_poly1305',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_chacha20_poly1305(encrypted_data: Dict[str, Any], password: str) -> bytes:
        """Дешифрование с проверкой аутентификации ChaCha20-Poly1305 (реализация на PyCryptodome)"""
        required_keys = ['ciphertext', 'salt', 'nonce', 'tag', 'aad', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные или поврежденные зашифрованные данные")
        if encrypted_data['algorithm'] != 'chacha20_poly1305':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        # Восстановление ключа (идентично оригиналу)
        key = EncryptionManager._derive_key(password, encrypted_data['salt'], "chacha20")

        # Дешифрование с проверкой тега
        cipher = ChaCha20_Poly1305.new(key=key, nonce=encrypted_data['nonce'])
        cipher.update(encrypted_data['aad'])
        try:
            plaintext = cipher.decrypt_and_verify(encrypted_data['ciphertext'], encrypted_data['tag'])
            return plaintext
        except (ValueError, KeyError) as e:
            raise ValueError(f"Ошибка аутентификации или расшифровки: {str(e)}")

    @staticmethod
    def encrypt_xor(data: bytes, key: str) -> Dict[str, Any]:
        """Учебное шифрование XOR (НЕ БЕЗОПАСНО!) - без изменений (не зависит от криптобиблиотеки)"""
        if not key:
            raise ValueError("Ключ XOR не может быть пустым")
        key_bytes = key.encode('utf-8')
        if len(key_bytes) == 0:
            raise ValueError("Ключ должен содержать хотя бы один символ")

        # Повторяем ключ для соответствия длине данных
        extended_key = (key_bytes * (len(data) // len(key_bytes) + 1))[:len(data)]

        # XOR операция
        ciphertext = bytes([b ^ k for b, k in zip(data, extended_key)])

        return {
            'ciphertext': ciphertext,
            'key': key,
            'algorithm': 'xor',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_xor(encrypted_data: Dict[str, Any]) -> bytes:
        """Дешифрование XOR (НЕ БЕЗОПАСНО!) - без изменений (не зависит от криптобиблиотеки)"""
        required_keys = ['ciphertext', 'key', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные зашифрованные данные")
        if encrypted_data['algorithm'] != 'xor':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")

        data = encrypted_data['ciphertext']
        key = encrypted_data['key'].encode('utf-8')

        # Повторяем ключ для соответствия длине данных
        extended_key = (key * (len(data) // len(key) + 1))[:len(data)]

        # XOR операция (обратима)
        plaintext = bytes([b ^ k for b, k in zip(data, extended_key)])
        return plaintext

    @staticmethod
    def encrypt_base64(data: bytes) -> Dict[str, Any]:
        """Кодирование Base64 (НЕ ШИФРОВАНИЕ!) - без изменений (стандартная библиотека)"""
        encoded = base64.b64encode(data)
        return {
            'encoded': encoded,
            'algorithm': 'base64',
            'version': '1.0'
        }

    @staticmethod
    def decrypt_base64(encrypted_data: Dict[str, Any]) -> bytes:
        """Декодирование Base64 (НЕ ДЕШИФРОВАНИЕ!) - без изменений (стандартная библиотека)"""
        required_keys = ['encoded', 'algorithm']
        if not all(key in encrypted_data for key in required_keys):
            raise ValueError("Неполные закодированные данные")
        if encrypted_data['algorithm'] != 'base64':
            raise ValueError(f"Несовместимый алгоритм: {encrypted_data['algorithm']}")
        try:
            decoded = base64.b64decode(encrypted_data['encoded'])
            return decoded
        except Exception as e:
            raise ValueError(f"Ошибка декодирования Base64: {str(e)}")

    @staticmethod
    def serialize_encrypted_data(encrypted_data: Dict[str, Any]) -> str:
        """Сериализация зашифрованных данных в строку JSON с Base64 (без изменений)"""
        serializable = {}
        # Обработка бинарных данных
        for key, value in encrypted_data.items():
            if isinstance(value, bytes):
                serializable[key] = base64.b64encode(value).decode('utf-8')
            else:
                serializable[key] = value
        # Добавление метаданных
        serializable['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        serializable['format'] = 'occultong_encrypted_v1'
        return json.dumps(serializable, ensure_ascii=False, indent=2)

    @staticmethod
    def deserialize_encrypted_data(serialized: str) -> Dict[str, Any]:
        """Десериализация зашифрованных данных из строки JSON (без изменений)"""
        try:
            data = json.loads(serialized)
        except json.JSONDecodeError as e:
            raise ValueError(f"Неверный формат данных: {str(e)}")
        # Проверка формата
        if data.get('format') != 'occultong_encrypted_v1':
            raise ValueError("Неподдерживаемый формат зашифрованных данных")
        # Восстановление бинарных данных
        deserialized = {}
        binary_keys = ['ciphertext', 'salt', 'iv', 'tag', 'nonce', 'checksum', 'initial_counter', 'encoded', 'aad']
        for key, value in data.items():
            if key in binary_keys and isinstance(value, str):
                try:
                    deserialized[key] = base64.b64decode(value.encode('utf-8'))
                except Exception as e:
                    raise ValueError(f"Ошибка декодирования {key}: {str(e)}")
            else:
                deserialized[key] = value
        return deserialized

    @staticmethod
    def save_encrypted_file(encrypted_data: Dict[str, Any], filepath: str) -> None:
        """Сохранение зашифрованных данных в файл с расширением .ongcrypt (без изменений)"""
        serialized = EncryptionManager.serialize_encrypted_data(encrypted_data)
        # Добавление сигнатуры файла для идентификации
        signature = b'ONGCRYPT\x01\x00\x00\x00'  # Магические байты + версия
        with open(filepath, 'wb') as f:
            f.write(signature)
            f.write(serialized.encode('utf-8'))

    @staticmethod
    def load_encrypted_file(filepath: str) -> Dict[str, Any]:
        """Загрузка зашифрованных данных из файла .ongcrypt (без изменений)"""
        with open(filepath, 'rb') as f:
            # Проверка сигнатуры
            signature = f.read(12)
            expected_signature = b'ONGCRYPT\x01\x00\x00\x00'
            if signature != expected_signature:
                # Попытка загрузить как обычный JSON (без сигнатуры)
                f.seek(0)
                content = f.read().decode('utf-8')
                return EncryptionManager.deserialize_encrypted_data(content)
            # Загрузка основного содержимого
            content = f.read().decode('utf-8')
            return EncryptionManager.deserialize_encrypted_data(content)

    @staticmethod
    def identify_data_type(data: bytes) -> Dict[str, Any]:
        """Определяет тип данных с расширенной информацией (без изменений)"""
        # Попытка декодировать как UTF-8
        try:
            decoded = data.decode('utf-8')
            # Проверка, что большая часть данных - текст
            text_ratio = sum(1 for c in decoded if c.isprintable() or c in '\n\r\t') / len(decoded)
            if text_ratio > 0.8:
                return {
                    'type': 'text',
                    'encoding': 'utf-8',
                    'preview': decoded[:100],
                    'is_text': True
                }
        except UnicodeDecodeError:
            pass

        # Проверка на изображение
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(data))
            return {
                'type': 'image',
                'format': img.format,
                'dimensions': f"{img.width}x{img.height}",
                'mode': img.mode,
                'size': len(data),
                'is_text': False
            }
        except:
            pass

        # Проверка на аудио
        try:
            import wave
            import io
            with wave.open(io.BytesIO(data), 'rb') as wav:
                return {
                    'type': 'audio',
                    'channels': wav.getnchannels(),
                    'sample_rate': wav.getframerate(),
                    'frames': wav.getnframes(),
                    'duration': f"{wav.getnframes() / wav.getframerate():.2f} sec",
                    'size': len(data),
                    'is_text': False
                }
        except:
            pass

        # Проверка на архив
        if data[:4] in [b'PK\x03\x04', b'Rar!', b'7z\xBC\xAF']:
            return {
                'type': 'archive',
                'size': len(data),
                'is_text': False
            }

        # По умолчанию - бинарные данные
        return {
            'type': 'binary',
            'size': len(data),
            'is_text': False
        }


# ───────────────────────────────────────────────
# 📊 КЛАСС АНАЛИЗА ФАЙЛОВ ДЛЯ СТЕГАНОГРАФИИ
# ───────────────────────────────────────────────
class FileAnalyzer:
    """Класс для анализа файлов на наличие стеганографических данных с расширенным набором тестов (15+ метрик)"""

    @staticmethod
    def calculate_entropy(data: bytes) -> float:
        """
        Рассчитывает энтропию Шеннона для данных.
        Энтропия измеряет степень случайности/хаотичности данных.
        """
        if not data:
            return 0.0
        # Подсчитываем частоту каждого байта
        byte_counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
        total = len(data)
        # Рассчитываем вероятности
        probabilities = byte_counts / total
        probabilities = probabilities[probabilities > 0]  # Исключаем нулевые вероятности
        # Формула энтропии Шеннона
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    @staticmethod
    def calculate_block_entropy(pixels: np.ndarray, block_size: int = 8) -> dict:
        """
        Рассчитывает энтропию по блокам изображения для выявления аномалий.
        Стеганография часто создает неравномерное распределение энтропии по блокам.
        """
        if pixels.ndim == 3:
            # Конвертируем в оттенки серого для анализа
            gray = np.dot(pixels[..., :3], [0.299, 0.587, 0.114])
        else:
            gray = pixels.astype(np.float32)
        h, w = gray.shape
        blocks_h = h // block_size
        blocks_w = w // block_size
        block_entropies = []
        entropy_map = np.zeros((blocks_h, blocks_w))

        for i in range(blocks_h):
            for j in range(blocks_w):
                block = gray[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]
                # Рассчитываем энтропию блока
                hist, _ = np.histogram(block.flatten(), bins=16, range=(0, 256))
                hist = hist[hist > 0]
                if len(hist) > 0:
                    probs = hist / np.sum(hist)
                    entropy = -np.sum(probs * np.log2(probs + 1e-10))
                    block_entropies.append(entropy)
                    entropy_map[i, j] = entropy

        if not block_entropies:
            return {
                'mean_entropy': 0.0,
                'std_entropy': 0.0,
                'min_entropy': 0.0,
                'max_entropy': 0.0,
                'block_count': 0,
                'suspicion_level': 10,
                'interpretation': 'Недостаточно данных',
                'entropy_map': entropy_map.tolist()
            }

        mean_entropy = np.mean(block_entropies)
        std_entropy = np.std(block_entropies)
        min_entropy = np.min(block_entropies)
        max_entropy = np.max(block_entropies)

        # Низкая дисперсия энтропии по блокам может указывать на стеганографию
        # Естественные изображения имеют вариативную энтропию по блокам
        if std_entropy < 0.3:
            suspicion_level = 85
            interpretation = 'Подозрительно низкая вариативность энтропии по блокам'
        elif std_entropy < 0.5:
            suspicion_level = 60
            interpretation = 'Умеренная вариативность энтропии'
        elif std_entropy < 0.8:
            suspicion_level = 30
            interpretation = 'Нормальная вариативность энтропии'
        else:
            suspicion_level = 10
            interpretation = 'Высокая вариативность энтропии (естественно)'

        # Дополнительная проверка: слишком высокая энтропия во всех блоках
        if mean_entropy > 7.8 and std_entropy < 0.4:
            suspicion_level = min(100, suspicion_level + 15)
            interpretation += ' + аномально высокая энтропия во всех блоках'

        return {
            'mean_entropy': float(mean_entropy),
            'std_entropy': float(std_entropy),
            'min_entropy': float(min_entropy),
            'max_entropy': float(max_entropy),
            'block_count': len(block_entropies),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'entropy_values': block_entropies,
            'entropy_map': entropy_map.tolist(),
            'block_size': block_size
        }

    @staticmethod
    def analyze_lsb_distribution(pixels: np.ndarray) -> dict:
        """
        Анализирует распределение младших битов (LSB) с применением статистического теста.
        При стеганографии распределение LSB становится искусственно равномерным (близко к 50/50),
        в то время как естественные изображения часто имеют статистически значимое смещение.
        """
        # Извлекаем младшие биты всех каналов
        if pixels.ndim == 3:
            # Обрабатываем все каналы отдельно для большей точности
            lsb_values = []
            for channel in range(min(3, pixels.shape[2])):
                channel_data = pixels[:, :, channel].flatten()
                lsb_values.append(channel_data & 1)
            lsb_values = np.concatenate(lsb_values)
        else:
            lsb_values = (pixels & 1).flatten()

        # Подсчитываем количество нулей и единиц
        zeros_count = np.sum(lsb_values == 0)
        ones_count = np.sum(lsb_values == 1)
        total = len(lsb_values)

        if total == 0:
            return {
                'zeros_count': 0,
                'ones_count': 0,
                'balance': 0.0,
                'p_value': 1.0,
                'chi_square': 0.0,
                'suspicion_level': 0,
                'interpretation': 'Недостаточно данных для анализа',
                'is_statistically_significant': False,
                'deviation': 0.0
            }

        # Рассчитываем фактическое соотношение
        ratio_ones = ones_count / total
        balance = abs(ratio_ones - 0.5)  # 0.0 = идеально 50/50, 0.5 = полностью смещено
        deviation = ratio_ones - 0.5  # Со знаком для определения направления смещения

        # СТАТИСТИЧЕСКИЙ ТЕСТ 1: биномиальный тест на равномерность
        p_value = binomtest(ones_count, n=total, p=0.5, alternative='two-sided').pvalue

        # СТАТИСТИЧЕСКИЙ ТЕСТ 2: хи-квадрат тест
        expected = total / 2
        chi_square = ((zeros_count - expected) ** 2 + (ones_count - expected) ** 2) / expected

        # ИНТЕРПРЕТАЦИЯ:
        # - Очень низкий p-value (<0.01) = распределение СТАТИСТИЧЕСКИ ЗНАЧИМО отлично от 50/50 → ЕСТЕСТВЕННОЕ изображение
        # - Очень высокий p-value (>0.8) = распределение СЛИШКОМ близко к 50/50 → ПОДОЗРИТЕЛЬНО (стеганография)
        # - Средние значения = неопределённость
        if p_value > 0.85:
            suspicion_level = 90
            interpretation = 'Крайне подозрительно: распределение искусственно близко к 50/50 (p=%.4f)' % p_value
            is_significant = True
        elif p_value > 0.7:
            suspicion_level = 75
            interpretation = 'Подозрительно: распределение слишком равномерное (p=%.4f)' % p_value
            is_significant = True
        elif p_value > 0.3:
            suspicion_level = 40
            interpretation = 'Умеренная равномерность распределения (p=%.4f)' % p_value
            is_significant = False
        elif p_value > 0.05:
            suspicion_level = 20
            interpretation = 'Незначительное отклонение от равномерности (p=%.4f)' % p_value
            is_significant = False
        else:  # p_value <= 0.05
            suspicion_level = 5
            interpretation = 'Естественное распределение с выраженным смещением (p=%.4f)' % p_value
            is_significant = True

        # Усиление подозрения при очень низком хи-квадрат
        if chi_square < 0.1:
            suspicion_level = min(100, suspicion_level + 10)
            interpretation += ' | χ²=%.3f (очень низкий)' % chi_square

        return {
            'zeros_count': int(zeros_count),
            'ones_count': int(ones_count),
            'ratio_ones': float(ratio_ones),
            'balance': float(balance),  # 0.0 = идеально 50/50
            'deviation': float(deviation),  # Со знаком
            'p_value': float(p_value),
            'chi_square': float(chi_square),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'is_statistically_significant': is_significant,
            'description': 'Равномерное распределение младших битов (близко к 50/50) часто указывает на стеганографию. Естественные изображения обычно имеют статистически значимое смещение.'
        }

    @staticmethod
    def analyze_pixel_correlation(pixels: np.ndarray) -> dict:
        """
        Анализирует корреляцию между соседними пикселями без искажения знака.
        Естественные изображения имеют высокую ПОЛОЖИТЕЛЬНУЮ корреляцию (>0.8).
        Стеганография снижает корреляцию, делая её ближе к нулю или отрицательной.
        """
        if pixels.ndim == 3:
            # Конвертируем в оттенки серого для анализа пространственных зависимостей
            gray = np.dot(pixels[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        else:
            gray = pixels.astype(np.uint8)

        h, w = gray.shape
        if h < 2 or w < 2:
            return {
                'horizontal_corr': 0.0,
                'vertical_corr': 0.0,
                'diagonal_corr': 0.0,
                'avg_corr': 0.0,
                'suspicion_level': 10,
                'interpretation': 'Изображение слишком маленькое для анализа корреляции',
                'description': 'Корреляция соседних пикселей снижается при стеганографии. Естественные изображения имеют высокую положительную корреляцию (>0.8).'
            }

        # Горизонтальная корреляция (БЕЗ абсолютного значения!)
        x_h = gray[:, :-1].flatten().astype(np.float32)
        y_h = gray[:, 1:].flatten().astype(np.float32)
        if len(x_h) > 1:
            mean_x_h, mean_y_h = np.mean(x_h), np.mean(y_h)
            numerator_h = np.sum((x_h - mean_x_h) * (y_h - mean_y_h))
            denominator_h = np.sqrt(np.sum((x_h - mean_x_h) ** 2) * np.sum((y_h - mean_y_h) ** 2))
            horizontal_corr = numerator_h / denominator_h if denominator_h != 0 else 0.0
        else:
            horizontal_corr = 0.0

        # Вертикальная корреляция (БЕЗ абсолютного значения!)
        x_v = gray[:-1, :].flatten().astype(np.float32)
        y_v = gray[1:, :].flatten().astype(np.float32)
        if len(x_v) > 1:
            mean_x_v, mean_y_v = np.mean(x_v), np.mean(y_v)
            numerator_v = np.sum((x_v - mean_x_v) * (y_v - mean_y_v))
            denominator_v = np.sqrt(np.sum((x_v - mean_x_v) ** 2) * np.sum((y_v - mean_y_v) ** 2))
            vertical_corr = numerator_v / denominator_v if denominator_v != 0 else 0.0
        else:
            vertical_corr = 0.0

        # Диагональная корреляция (дополнительная метрика)
        min_dim = min(h, w) - 1
        if min_dim > 1:
            x_d = gray[:min_dim, :min_dim].flatten().astype(np.float32)
            y_d = gray[1:min_dim + 1, 1:min_dim + 1].flatten().astype(np.float32)
            mean_x_d, mean_y_d = np.mean(x_d), np.mean(y_d)
            numerator_d = np.sum((x_d - mean_x_d) * (y_d - mean_y_d))
            denominator_d = np.sqrt(np.sum((x_d - mean_x_d) ** 2) * np.sum((y_d - mean_y_d) ** 2))
            diagonal_corr = numerator_d / denominator_d if denominator_d != 0 else 0.0
        else:
            diagonal_corr = 0.0

        # Средняя корреляция (сохраняем знак!)
        avg_corr = (horizontal_corr + vertical_corr + diagonal_corr) / 3.0

        # ИНТЕРПРЕТАЦИЯ:
        # Естественные изображения: высокая ПОЛОЖИТЕЛЬНАЯ корреляция (>0.8)
        # Стеганография: снижение корреляции (<0.7), возможна отрицательная корреляция
        if avg_corr < 0.5:
            suspicion_level = 90
            interpretation = 'Крайне низкая корреляция (%.3f) - сильный признак стеганографии' % avg_corr
        elif avg_corr < 0.65:
            suspicion_level = 75
            interpretation = 'Значительно сниженная корреляция (%.3f)' % avg_corr
        elif avg_corr < 0.78:
            suspicion_level = 50
            interpretation = 'Умеренно сниженная корреляция (%.3f)' % avg_corr
        elif avg_corr < 0.85:
            suspicion_level = 25
            interpretation = 'Нормальная корреляция (%.3f)' % avg_corr
        else:
            suspicion_level = 10
            interpretation = 'Высокая корреляция (%.3f) - естественное изображение' % avg_corr

        # Дополнительная проверка: отрицательная корреляция всегда подозрительна
        negative_count = sum(1 for c in [horizontal_corr, vertical_corr, diagonal_corr] if c < 0)
        if negative_count > 0:
            suspicion_level = min(100, suspicion_level + 20 * negative_count)
            interpretation += ' | обнаружена отрицательная корреляция (%d направлений)' % negative_count

        return {
            'horizontal_corr': float(horizontal_corr),
            'vertical_corr': float(vertical_corr),
            'diagonal_corr': float(diagonal_corr),
            'avg_corr': float(avg_corr),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'description': 'Естественные изображения имеют высокую положительную корреляцию соседних пикселей (>0.8). Стеганография снижает корреляцию, делая изображение более "случайным". Отрицательная корреляция - сильный признак аномалии.'
        }

    @staticmethod
    def analyze_noise_pattern(image: np.ndarray) -> dict:
        """
        Анализирует шумовой паттерн изображения.
        Стеганография может создавать аномальные шумовые паттерны.
        """
        if image.ndim == 3:
            # Конвертируем в оттенки серого для анализа
            gray = np.dot(image[..., :3], [0.299, 0.587, 0.114])
        else:
            gray = image.astype(np.float32)

        # Применяем размытие для выделения шумовой компоненты
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = gray - blurred

        # Анализируем статистику шума
        noise_std = np.std(noise)
        noise_mean = np.mean(noise)
        noise_skewness = skew(noise.flatten()) if noise_std > 0 else 0.0
        noise_kurtosis = kurtosis(noise.flatten()) if noise_std > 0 else 0.0

        # Правильная интерпретация:
        if noise_std < 2.0:  # Слишком низкая дисперсия = подозрительно
            suspicion_level = 85
            interpretation = 'Аномально низкая дисперсия шума (%.2f) - подозрительно' % noise_std
        elif noise_std < 4.0:
            suspicion_level = 60
            interpretation = 'Пониженная дисперсия шума (%.2f)' % noise_std
        elif noise_std > 15.0:  # Слишком высокая дисперсия тоже подозрительна
            suspicion_level = 70
            interpretation = 'Аномально высокая дисперсия шума (%.2f) - возможна обработка' % noise_std
        else:
            suspicion_level = 10
            interpretation = 'Нормальная дисперсия шума (%.2f)' % noise_std

        # Дополнительная проверка: асимметрия шума
        if abs(noise_skewness) > 1.0:
            suspicion_level = min(100, suspicion_level + 15)
            interpretation += ' | асимметрия шума (%.2f)' % noise_skewness

        return {
            'std_deviation': float(noise_std),
            'mean': float(noise_mean),
            'skewness': float(noise_skewness),
            'kurtosis': float(noise_kurtosis),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'noise_map': noise.tolist()  # Для визуализации
        }

    @staticmethod
    def analyze_histogram(data: np.ndarray) -> dict:
        """
        Анализирует гистограмму распределения значений.
        Выявляет аномалии в распределении (провалы, пики, периодичность).
        """
        # Строим гистограмму
        if data.ndim == 3:
            data = data.flatten()
        histogram, bin_edges = np.histogram(data, bins=256, range=(0, 256))

        # Анализируем гладкость гистограммы
        smoothness = np.mean(np.abs(np.diff(histogram)))

        # Ищем пики и провалы
        peaks = np.where(histogram > np.mean(histogram) + 2 * np.std(histogram))[0]
        valleys = np.where(histogram < np.mean(histogram) - 2 * np.std(histogram))[0]

        # Периодичность может указывать на стеганографию
        # Проверяем корреляцию между соседними бинами
        autocorr = np.correlate(histogram - np.mean(histogram),
                                histogram - np.mean(histogram), mode='full')
        periodicity_score = np.max(autocorr[len(autocorr) // 2 + 1:]) / autocorr[len(autocorr) // 2] if autocorr[
                                                                                                            len(autocorr) // 2] != 0 else 0.0

        # Анализ равномерности распределения (тест Колмогорова-Смирнова)
        from scipy.stats import kstest
        ks_stat, ks_pvalue = kstest(histogram, 'uniform')

        # Интерпретация результатов
        suspicion_level = 0
        issues = []
        if len(peaks) > 10:
            suspicion_level += 20
            issues.append('Много пиков (%d)' % len(peaks))
        if len(valleys) > 10:
            suspicion_level += 20
            issues.append('Много провалов (%d)' % len(valleys))
        if periodicity_score > 0.3:
            suspicion_level += 30
            issues.append('Периодичность (%.2f)' % periodicity_score)
        if smoothness < np.mean(histogram) * 0.1:
            suspicion_level += 20
            issues.append('Негладкое распределение')
        if ks_pvalue > 0.95:  # Слишком равномерное распределение
            suspicion_level += 25
            issues.append('Искусственно равномерное распределение (KS p=%.3f)' % ks_pvalue)

        return {
            'histogram': histogram.tolist(),
            'smoothness': float(smoothness),
            'peaks_count': len(peaks),
            'valleys_count': len(valleys),
            'periodicity_score': float(periodicity_score),
            'ks_statistic': float(ks_stat),
            'ks_pvalue': float(ks_pvalue),
            'suspicion_level': min(suspicion_level, 100),
            'issues': issues,
            'interpretation': ', '.join(issues) if issues else 'Нормальное распределение'
        }

    @staticmethod
    def analyze_color_channel_correlation(pixels: np.ndarray) -> dict:
        """
        Анализирует корреляцию между цветовыми каналами (только для цветных изображений).
        Стеганография может нарушать естественные соотношения между каналами.
        """
        if pixels.ndim != 3 or pixels.shape[2] < 3:
            return {
                'correlation_r_g': 0.0,
                'correlation_g_b': 0.0,
                'correlation_r_b': 0.0,
                'avg_correlation': 0.0,
                'channel_balance': 0.0,
                'suspicion_level': 0,
                'interpretation': 'Не цветное изображение'
            }

        # Извлекаем каналы
        r = pixels[:, :, 0].flatten().astype(np.float32)
        g = pixels[:, :, 1].flatten().astype(np.float32)
        b = pixels[:, :, 2].flatten().astype(np.float32)

        # Рассчитываем корреляции
        corr_rg = np.corrcoef(r, g)[0, 1] if len(r) > 1 else 0.0
        corr_gb = np.corrcoef(g, b)[0, 1] if len(g) > 1 else 0.0
        corr_rb = np.corrcoef(r, b)[0, 1] if len(r) > 1 else 0.0

        # Средняя корреляция
        avg_corr = (abs(corr_rg) + abs(corr_gb) + abs(corr_rb)) / 3

        # Анализ баланса каналов (отношение средних значений)
        mean_r, mean_g, mean_b = np.mean(r), np.mean(g), np.mean(b)
        max_mean = max(mean_r, mean_g, mean_b)
        min_mean = min(mean_r, mean_g, mean_b)
        channel_balance = (max_mean - min_mean) / max_mean if max_mean > 0 else 0.0

        # Естественные изображения имеют высокую корреляцию между каналами (>0.85)
        if avg_corr < 0.7:
            suspicion_level = 80
            interpretation = 'Низкая корреляция каналов (%.3f) - подозрительно' % avg_corr
        elif avg_corr < 0.8:
            suspicion_level = 60
            interpretation = 'Умеренная корреляция каналов (%.3f)' % avg_corr
        elif avg_corr < 0.9:
            suspicion_level = 30
            interpretation = 'Нормальная корреляция каналов (%.3f)' % avg_corr
        else:
            suspicion_level = 10
            interpretation = 'Высокая корреляция каналов (%.3f) - естественно' % avg_corr

        # Дополнительная проверка: сильный дисбаланс каналов
        if channel_balance > 0.4:
            suspicion_level = min(100, suspicion_level + 15)
            interpretation += ' | дисбаланс каналов (%.2f)' % channel_balance

        return {
            'correlation_r_g': float(corr_rg),
            'correlation_g_b': float(corr_gb),
            'correlation_r_b': float(corr_rb),
            'avg_correlation': float(avg_corr),
            'channel_balance': float(channel_balance),
            'mean_r': float(mean_r),
            'mean_g': float(mean_g),
            'mean_b': float(mean_b),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'description': 'Естественные изображения имеют высокую корреляцию между цветовыми каналами (>0.85) и сбалансированные средние значения.'
        }

    @staticmethod
    def analyze_jpeg_artifacts(image_path: str) -> dict:
        """
        Анализирует артефакты JPEG сжатия для выявления признаков стеганографии.
        Работает только с JPEG изображениями.
        """
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in ['.jpg', '.jpeg']:
            return {
                'artifact_score': 0.0,
                'blockiness': 0.0,
                'dct_histogram': [],
                'quality_estimate': 0,
                'suspicion_level': 0,
                'interpretation': 'Не JPEG изображение'
            }

        try:
            # Загружаем изображение в градациях серого
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                return {
                    'artifact_score': 0.0,
                    'blockiness': 0.0,
                    'dct_histogram': [],
                    'quality_estimate': 0,
                    'suspicion_level': 0,
                    'interpretation': 'Не удалось загрузить изображение'
                }

            h, w = img.shape

            # Анализируем границы блоков 8x8 (характерные для JPEG)
            blockiness_scores = []

            # Проверяем вертикальные границы блоков
            for x in range(8, w, 8):
                left_col = img[:, x - 1].astype(np.int16)
                right_col = img[:, x].astype(np.int16)
                diff = np.abs(left_col - right_col)
                blockiness_scores.append(np.mean(diff))

            # Проверяем горизонтальные границы блоков
            for y in range(8, h, 8):
                top_row = img[y - 1, :].astype(np.int16)
                bottom_row = img[y, :].astype(np.int16)
                diff = np.abs(top_row - bottom_row)
                blockiness_scores.append(np.mean(diff))

            if not blockiness_scores:
                return {
                    'artifact_score': 0.0,
                    'blockiness': 0.0,
                    'dct_histogram': [],
                    'quality_estimate': 0,
                    'suspicion_level': 10,
                    'interpretation': 'Недостаточно данных'
                }

            avg_blockiness = np.mean(blockiness_scores)

            # Анализ DCT коэффициентов (приблизительный через разность соседних пикселей)
            # В JPEG изображениях высокочастотные DCT коэффициенты часто обнуляются
            # что создает характерные артефакты
            horizontal_diff = np.abs(np.diff(img.astype(np.int16), axis=1))
            vertical_diff = np.abs(np.diff(img.astype(np.int16), axis=0))
            avg_diff = (np.mean(horizontal_diff) + np.mean(vertical_diff)) / 2

            # Оценка качества сжатия (грубая)
            quality_estimate = min(100, max(10, int(100 - avg_blockiness * 5)))

            # Высокая блочность может указывать на стеганографию или повторное сжатие
            if avg_blockiness > 8.0:
                suspicion_level = 70
                interpretation = 'Высокая блочность (%.2f) - возможно стеганография или повторное сжатие' % avg_blockiness
            elif avg_blockiness > 5.0:
                suspicion_level = 40
                interpretation = 'Умеренная блочность (%.2f)' % avg_blockiness
            else:
                suspicion_level = 20
                interpretation = 'Низкая блочность (%.2f) - естественные артефакты JPEG' % avg_blockiness

            # Дополнительная проверка: аномально низкая вариативность разностей
            diff_std = np.std(np.concatenate([horizontal_diff.flatten(), vertical_diff.flatten()]))
            if diff_std < 5.0:
                suspicion_level = min(100, suspicion_level + 20)
                interpretation += ' | аномально низкая вариативность градиентов'

            # Гистограмма разностей для анализа DCT-подобных артефактов
            diff_hist, _ = np.histogram(np.concatenate([horizontal_diff.flatten(), vertical_diff.flatten()]),
                                        bins=50, range=(0, 50))

            return {
                'artifact_score': float(avg_blockiness),
                'blockiness': float(avg_blockiness),
                'dct_histogram': diff_hist.tolist(),
                'quality_estimate': quality_estimate,
                'diff_std': float(diff_std),
                'avg_diff': float(avg_diff),
                'suspicion_level': suspicion_level,
                'interpretation': interpretation,
                'block_count_horizontal': w // 8,
                'block_count_vertical': h // 8,
                'description': 'Анализ артефактов блочной структуры JPEG. Аномальная блочность или низкая вариативность градиентов могут указывать на стеганографию.'
            }
        except Exception as e:
            return {
                'artifact_score': 0.0,
                'blockiness': 0.0,
                'dct_histogram': [],
                'quality_estimate': 0,
                'suspicion_level': 0,
                'interpretation': f'Ошибка анализа: {str(e)}'
            }

    @staticmethod
    def analyze_audio_spectral_features(audio_path: str) -> dict:
        """
        Анализирует спектральные характеристики аудиофайла.
        Стеганография может создавать аномалии в спектре.
        """
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext != '.wav':
            return {
                'spectral_centroid_mean': 0.0,
                'spectral_flatness_mean': 0.0,
                'spectral_flatness_std': 0.0,
                'zero_crossing_rate': 0.0,
                'mfcc_mean': [],
                'suspicion_level': 0,
                'interpretation': 'Не WAV аудиофайл'
            }

        try:
            with wave.open(audio_path, 'rb') as wav:
                n_channels = wav.getnchannels()
                sample_rate = wav.getframerate()
                n_frames = wav.getnframes()
                frames = wav.readframes(n_frames)

                # Конвертируем в массив
                if wav.getsampwidth() == 2:  # 16-bit
                    audio_data = np.frombuffer(frames, dtype=np.int16)
                else:  # 8-bit
                    audio_data = np.frombuffer(frames, dtype=np.uint8).astype(np.int16) - 128

                # Для стерео берем один канал
                if n_channels > 1:
                    audio_data = audio_data[::n_channels]

                if len(audio_data) < 1024:
                    return {
                        'spectral_centroid_mean': 0.0,
                        'spectral_flatness_mean': 0.0,
                        'spectral_flatness_std': 0.0,
                        'zero_crossing_rate': 0.0,
                        'mfcc_mean': [],
                        'suspicion_level': 10,
                        'interpretation': 'Аудио слишком короткое'
                    }

                # Анализ zero-crossing rate (ZCR)
                zero_crossings = np.where(np.diff(np.signbit(audio_data)))[0]
                zcr = len(zero_crossings) / len(audio_data)

                # Делим на сегменты для анализа
                segment_size = 1024
                hop_size = 512
                n_segments = max(1, (len(audio_data) - segment_size) // hop_size)

                spectral_centroids = []
                spectral_flatness = []
                mfcc_coeffs = []

                for i in range(n_segments):
                    start = i * hop_size
                    end = start + segment_size
                    if end > len(audio_data):
                        break

                    segment = audio_data[start:end].astype(np.float32)

                    # Вычисляем спектр
                    spectrum = np.abs(np.fft.rfft(segment))
                    freqs = np.fft.rfftfreq(segment_size, 1 / sample_rate)

                    if np.sum(spectrum) > 0:
                        # Спектральный центроид
                        centroid = np.sum(freqs * spectrum) / np.sum(spectrum)
                        spectral_centroids.append(centroid)

                        # Спектральная плоскостность (мера шума)
                        geometric_mean = np.exp(np.mean(np.log(spectrum + 1e-10)))
                        arithmetic_mean = np.mean(spectrum)
                        flatness = geometric_mean / arithmetic_mean if arithmetic_mean > 0 else 0.0
                        spectral_flatness.append(flatness)

                    # MFCC (упрощенный расчет)
                    if i == 0:  # Только для первого сегмента для экономии времени
                        try:
                            from scipy.fftpack import dct as dct_transform
                            # Применяем окно Хэмминга
                            windowed = segment * np.hamming(segment_size)
                            # Спектр мощности
                            power_spectrum = np.abs(np.fft.rfft(windowed)) ** 2
                            # Фильтры в мел-шкале (упрощенно)
                            n_mfcc = 13
                            mfcc = dct_transform(np.log(power_spectrum[1:40] + 1e-10), type=2, norm='ortho')[:n_mfcc]
                            mfcc_coeffs.append(mfcc.tolist())
                        except:
                            mfcc_coeffs.append([0.0] * 13)

                if not spectral_centroids or not spectral_flatness:
                    return {
                        'spectral_centroid_mean': 0.0,
                        'spectral_flatness_mean': 0.0,
                        'spectral_flatness_std': 0.0,
                        'zero_crossing_rate': float(zcr),
                        'mfcc_mean': [],
                        'suspicion_level': 10,
                        'interpretation': 'Недостаточно данных'
                    }

                centroid_mean = np.mean(spectral_centroids)
                flatness_mean = np.mean(spectral_flatness)
                flatness_std = np.std(spectral_flatness)
                mfcc_mean = np.mean(mfcc_coeffs, axis=0).tolist() if mfcc_coeffs else []

                # Низкая вариативность спектральной плоскостности может указывать на стеганографию
                suspicion_level = 0
                issues = []

                if flatness_std < 0.05:
                    suspicion_level += 40
                    issues.append('Очень низкая вариативность спектра')
                elif flatness_std < 0.1:
                    suspicion_level += 25
                    issues.append('Низкая вариативность спектра')
                elif flatness_std < 0.2:
                    suspicion_level += 10
                    issues.append('Умеренная вариативность спектра')
                else:
                    suspicion_level += 5
                    issues.append('Высокая вариативность спектра')

                # Анализ ZCR
                if zcr < 0.05 or zcr > 0.3:  # Аномальные значения
                    suspicion_level += 20
                    issues.append('Аномальный zero-crossing rate (%.3f)' % zcr)

                # Анализ спектрального центроида
                if centroid_mean < 500 or centroid_mean > 8000:  # Зависит от типа аудио
                    suspicion_level += 15
                    issues.append('Аномальный спектральный центроид (%.0f Гц)' % centroid_mean)

                suspicion_level = min(100, suspicion_level)
                interpretation = '; '.join(issues[:3])  # Первые 3 проблемы

                return {
                    'spectral_centroid_mean': float(centroid_mean),
                    'spectral_flatness_mean': float(flatness_mean),
                    'spectral_flatness_std': float(flatness_std),
                    'zero_crossing_rate': float(zcr),
                    'mfcc_mean': mfcc_mean,
                    'segment_count': n_segments,
                    'sample_rate': sample_rate,
                    'suspicion_level': suspicion_level,
                    'interpretation': interpretation,
                    'description': 'Анализ спектральных характеристик аудио. Низкая вариативность спектральных признаков может указывать на стеганографию.'
                }
        except Exception as e:
            return {
                'spectral_centroid_mean': 0.0,
                'spectral_flatness_mean': 0.0,
                'spectral_flatness_std': 0.0,
                'zero_crossing_rate': 0.0,
                'mfcc_mean': [],
                'suspicion_level': 0,
                'interpretation': f'Ошибка анализа: {str(e)}'
            }

    @staticmethod
    def analyze_gradient_statistics(pixels: np.ndarray) -> dict:
        """
        Анализирует статистику градиентов изображения.
        Стеганография изменяет распределение градиентов, делая его более равномерным.
        """
        if pixels.ndim == 3:
            gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        else:
            gray = pixels.astype(np.uint8)

        # Вычисляем градиенты Собеля
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)

        # Статистика градиентов
        grad_mean = np.mean(gradient_magnitude)
        grad_std = np.std(gradient_magnitude)
        grad_skew = skew(gradient_magnitude.flatten())
        grad_kurt = kurtosis(gradient_magnitude.flatten())

        # Анализ распределения градиентов
        hist, _ = np.histogram(gradient_magnitude.flatten(), bins=50, range=(0, 255))
        smoothness = np.mean(np.abs(np.diff(hist)))

        # Тест на равномерность распределения градиентов
        from scipy.stats import chisquare
        chi2_stat, chi2_p = chisquare(hist + 1)  # +1 для избежания нулей

        # Интерпретация
        suspicion_level = 0
        issues = []

        if chi2_p > 0.9:  # Слишком равномерное распределение
            suspicion_level += 40
            issues.append('Искусственно равномерное распределение градиентов')

        if grad_std < 10.0:  # Слишком низкая вариативность градиентов
            suspicion_level += 30
            issues.append('Аномально низкая вариативность градиентов')

        if abs(grad_skew) < 0.5:  # Слишком симметричное распределение
            suspicion_level += 20
            issues.append('Слишком симметричное распределение градиентов')

        suspicion_level = min(100, suspicion_level)
        interpretation = '; '.join(issues) if issues else 'Нормальное распределение градиентов'

        return {
            'gradient_mean': float(grad_mean),
            'gradient_std': float(grad_std),
            'gradient_skewness': float(grad_skew),
            'gradient_kurtosis': float(grad_kurt),
            'chi2_statistic': float(chi2_stat),
            'chi2_pvalue': float(chi2_p),
            'smoothness': float(smoothness),
            'suspicion_level': suspicion_level,
            'interpretation': interpretation,
            'gradient_map': gradient_magnitude.tolist(),
            'description': 'Стеганография часто создает аномально равномерное распределение градиентов изображения.'
        }

    @staticmethod
    def analyze_frequency_domain(pixels: np.ndarray) -> dict:
        """
        Анализирует частотный спектр изображения (DCT и FFT).
        Стеганография создает аномалии в высокочастотных компонентах.
        """
        if pixels.ndim == 3:
            gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
        else:
            gray = pixels.astype(np.float32)

        h, w = gray.shape

        # Анализ через DCT (более релевантен для JPEG)
        try:
            # Блочное DCT 8x8
            block_size = 8
            blocks_h, blocks_w = h // block_size, w // block_size
            dc_coeffs = []
            high_freq_energy = []

            for i in range(blocks_h):
                for j in range(blocks_w):
                    block = gray[i * block_size:(i + 1) * block_size, j * block_size:(j + 1) * block_size]
                    if block.shape == (block_size, block_size):
                        dct_block = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
                        dc_coeffs.append(dct_block[0, 0])
                        # Энергия высокочастотных коэффициентов (правый нижний квадрант)
                        hf_block = dct_block[4:, 4:]
                        high_freq_energy.append(np.sum(hf_block ** 2))

            dc_std = np.std(dc_coeffs) if dc_coeffs else 0.0
            hf_mean = np.mean(high_freq_energy) if high_freq_energy else 0.0
            hf_std = np.std(high_freq_energy) if high_freq_energy else 0.0

            # Анализ аномалий в распределении DC коэффициентов
            dc_hist, _ = np.histogram(dc_coeffs, bins=32)
            dc_smoothness = np.mean(np.abs(np.diff(dc_hist)))

            # Подозрительно, если:
            # 1. Очень низкая вариативность DC коэффициентов
            # 2. Очень высокая вариативность высокочастотной энергии
            suspicion_level = 0
            issues = []

            if dc_std < 5.0:
                suspicion_level += 35
                issues.append('Аномально низкая вариативность DC коэффициентов DCT')

            if hf_std > hf_mean * 2.0 and hf_mean > 0:
                suspicion_level += 30
                issues.append('Аномально высокая вариативность высокочастотной энергии')

            if dc_smoothness < np.mean(dc_hist) * 0.2:
                suspicion_level += 25
                issues.append('Неравномерное распределение DC коэффициентов')

            suspicion_level = min(100, suspicion_level)
            interpretation = '; '.join(issues) if issues else 'Нормальный частотный спектр'

            return {
                'dc_std': float(dc_std),
                'hf_mean': float(hf_mean),
                'hf_std': float(hf_std),
                'dc_smoothness': float(dc_smoothness),
                'block_count': len(dc_coeffs),
                'suspicion_level': suspicion_level,
                'interpretation': interpretation,
                'description': 'Стеганография часто создает аномалии в распределении DCT коэффициентов, особенно в высокочастотных компонентах.'
            }
        except Exception as e:
            return {
                'dc_std': 0.0,
                'hf_mean': 0.0,
                'hf_std': 0.0,
                'dc_smoothness': 0.0,
                'block_count': 0,
                'suspicion_level': 10,
                'interpretation': f'Ошибка DCT анализа: {str(e)}',
                'description': 'Ошибка при анализе частотного спектра'
            }

    @staticmethod
    def analyze_texture_features(pixels: np.ndarray) -> dict:
        """
        Анализирует текстурные признаки изображения через GLCM без использования skimage.
        Результаты идентичны graycomatrix/graycoprops.
        """
        if pixels.ndim == 3:
            gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        else:
            gray = pixels.astype(np.uint8)

        # Нормализуем до 8 уровней для устойчивости GLCM
        gray_8bit = (gray // 32).clip(0, 7).astype(np.uint8)

        distances = [1]
        angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
        levels = 8

        contrast_values = []
        homogeneity_values = []
        energy_values = []
        correlation_values = []

        try:
            h, w = gray_8bit.shape
            for angle in angles:
                # 1. Вычисляем смещение (аналог skimage)
                dx = int(round(np.cos(angle)))
                dy = int(-round(np.sin(angle)))

                # Ограничиваем области для извлечения пар пикселей
                y_slice = slice(max(0, dy), min(h, h + dy))
                x_slice = slice(max(0, dx), min(w, w + dx))
                y_neigh = slice(max(0, -dy), min(h, h - dy))
                x_neigh = slice(max(0, -dx), min(w, w - dx))

                target = gray_8bit[y_slice, x_slice].ravel()
                neighbor = gray_8bit[y_neigh, x_neigh].ravel()

                # 2. Строим матрицу совместной встречаемости (GLCM)
                glcm = np.zeros((levels, levels), dtype=np.float64)
                # Эффективный подсчет пар
                for t, n in zip(target, neighbor):
                    glcm[t, n] += 1

                # symmetric=True
                glcm += glcm.T

                # normed=True
                sum_glcm = np.sum(glcm)
                if sum_glcm > 0:
                    glcm /= sum_glcm

                # 3. Вычисляем признаки (Props)
                i, j = np.ogrid[:levels, :levels]

                # Contrast
                contrast = np.sum(glcm * (i - j) ** 2)
                # Homogeneity
                homogeneity = np.sum(glcm / (1.0 + (i - j) ** 2))
                # Energy
                energy = np.sqrt(np.sum(glcm ** 2))
                # Correlation
                mean_i = np.sum(i * glcm)
                mean_j = np.sum(j * glcm)
                std_i = np.sqrt(np.sum(glcm * (i - mean_i) ** 2))
                std_j = np.sqrt(np.sum(glcm * (j - mean_j) ** 2))

                if std_i > 1e-10 and std_j > 1e-10:
                    correlation = np.sum(glcm * (i - mean_i) * (j - mean_j)) / (std_i * std_j)
                else:
                    correlation = 1.0

                contrast_values.append(contrast)
                homogeneity_values.append(homogeneity)
                energy_values.append(energy)
                correlation_values.append(correlation)

            # Статистика (без изменений)
            contrast_mean = np.mean(contrast_values)
            contrast_std = np.std(contrast_values)
            homogeneity_mean = np.mean(homogeneity_values)
            energy_mean = np.mean(energy_values)
            correlation_mean = np.mean(correlation_values)

            suspicion_level = 0
            issues = []

            if contrast_std < 0.05:
                suspicion_level += 40
                issues.append('Аномально однородная текстура во всех направлениях')

            if homogeneity_mean > 0.9:
                suspicion_level += 30
                issues.append('Аномально высокая однородность текстуры')

            if energy_mean > 0.15:
                suspicion_level += 25
                issues.append('Аномально высокая энергия GLCM')

            suspicion_level = min(100, suspicion_level)
            interpretation = '; '.join(issues) if issues else 'Нормальные текстурные характеристики'

            return {
                'contrast_mean': float(contrast_mean),
                'contrast_std': float(contrast_std),
                'homogeneity_mean': float(homogeneity_mean),
                'energy_mean': float(energy_mean),
                'correlation_mean': float(correlation_mean),
                'suspicion_level': suspicion_level,
                'interpretation': interpretation,
                'description': 'Стеганография часто создает аномально однородную текстуру с низким контрастом и высокой однородностью.'
            }
        except Exception as e:
            return {
                'contrast_mean': 0.0,
                'contrast_std': 0.0,
                'homogeneity_mean': 0.0,
                'energy_mean': 0.0,
                'correlation_mean': 0.0,
                'suspicion_level': 10,
                'interpretation': f'Ошибка анализа текстуры: {str(e)}',
                'description': 'Ошибка при анализе текстурных признаков'
            }

    @staticmethod
    def analyze_wavelet_features(pixels: np.ndarray) -> dict:
        """
        Анализирует вейвлет-коэффициенты изображения без использования pywt.
        Реализовано двухуровневое разложение Хаара через numpy.
        """
        if pixels.ndim == 3:
            gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32)
        else:
            gray = pixels.astype(np.float32)

        def haar_step(image):
            # Разделяем на четные и нечетные строки/столбцы
            h, w = image.shape
            # Если размеры нечетные - обрезаем (как это делает wavedec2 в определенных режимах)
            img = image[:h - h % 2, :w - w % 2]

            # Вычисляем средние и разности (Haar)
            # Вертикальные суммы и разности
            row_sum = (img[0::2, :] + img[1::2, :]) / np.sqrt(2)
            row_diff = (img[0::2, :] - img[1::2, :]) / np.sqrt(2)

            # Горизонтальные суммы и разности
            cA = (row_sum[:, 0::2] + row_sum[:, 1::2]) / np.sqrt(2)  # Аппроксимация
            cH = (row_sum[:, 0::2] - row_sum[:, 1::2]) / np.sqrt(2)  # Горизонтальные детали
            cV = (row_diff[:, 0::2] + row_diff[:, 1::2]) / np.sqrt(2)  # Вертикальные детали
            cD = (row_diff[:, 0::2] - row_diff[:, 1::2]) / np.sqrt(2)  # Диагональные детали

            return cA, (cH, cV, cD)

        try:
            # Уровень 1
            cA1, details1 = haar_step(gray)
            # Уровень 2
            cA2, details2 = haar_step(cA1)

            # Собираем детализирующие коэффициенты (как это делал pywt.wavedec2)
            # В wavedec2 coeffs[1:] - это кортежи (cH, cV, cD) для каждого уровня
            detail_coeffs = []
            for level in [details1, details2]:
                for detail_map in level:
                    detail_coeffs.extend(detail_map.flatten())

            if len(detail_coeffs) == 0:
                return {
                    'coeff_std': 0.0,
                    'coeff_skewness': 0.0,
                    'coeff_kurtosis': 0.0,
                    'suspicion_level': 10,
                    'interpretation': 'Недостаточно данных для анализа',
                    'description': 'Недостаточно данных для вейвлет-анализа'
                }

            detail_array = np.array(detail_coeffs)
            coeff_std = np.std(detail_array)
            coeff_skew = skew(detail_array)
            coeff_kurt = kurtosis(detail_array)

            k2_stat, k2_pvalue = normaltest(detail_array)

            suspicion_level = 0
            issues = []

            if coeff_kurt > -0.5:
                suspicion_level += 45
                issues.append('Аномально высокий эксцесс вейвлет-коэффициентов (%.2f)' % coeff_kurt)

            if k2_pvalue > 0.1:
                suspicion_level += 35
                issues.append('Распределение вейвлет-коэффициентов слишком близко к нормальному')

            if coeff_std < 5.0:
                suspicion_level += 25
                issues.append('Аномально низкая вариативность вейвлет-коэффициентов')

            suspicion_level = min(100, suspicion_level)
            interpretation = '; '.join(issues) if issues else 'Нормальное распределение вейвлет-коэффициентов'

            return {
                'coeff_std': float(coeff_std),
                'coeff_skewness': float(coeff_skew),
                'coeff_kurtosis': float(coeff_kurt),
                'normality_pvalue': float(k2_pvalue),
                'coeff_count': len(detail_coeffs),
                'suspicion_level': suspicion_level,
                'interpretation': interpretation,
                'description': 'Стеганография часто делает распределение вейвлет-коэффициентов более гауссовым, нарушая естественную субгауссовость.'
            }
        except Exception as e:
            return {
                'coeff_std': 0.0,
                'coeff_skewness': 0.0,
                'coeff_kurtosis': 0.0,
                'normality_pvalue': 0.0,
                'coeff_count': 0,
                'suspicion_level': 10,
                'interpretation': f'Ошибка вейвлет-анализа: {str(e)}',
                'description': 'Ошибка при анализе вейвлет-коэффициентов'
            }

    @staticmethod
    def analyze_pairwise_pixel_statistics(pixels: np.ndarray) -> dict:
        """
        Анализирует статистику пар пикселей по методу Кера (Ker's Pair Analysis).
        Оригинальный метод Кера: в естественных изображениях пары (2i,2i+1) и (2i+1,2i+2)
        имеют разную частоту появления. Стеганография LSB выравнивает эти частоты.

        Метрика α = |f(2i,2i+1) - f(2i+1,2i+2)| / (f(2i,2i+1) + f(2i+1,2i+2))
        Низкое α (< 0.05) → сильный признак стеганографии.
        """
        if pixels.ndim == 3:
            gray = cv2.cvtColor(pixels.astype(np.uint8), cv2.COLOR_RGB2GRAY)
        else:
            gray = pixels.astype(np.uint8)
        h, w = gray.shape
        if h < 2 or w < 2:
            return {
                'alpha': 1.0,
                'regularity': 0.5,
                'deviation': 0.0,
                'count_group_a': 0,
                'count_group_b': 0,
                'total_pairs': 0,
                'suspicion_level': 10,
                'interpretation': 'Изображение слишком маленькое',
                'description': 'Недостаточно данных для анализа пар пикселей методом Кера'
            }

        try:
            # Собираем все соседние пары пикселей с разницей = 1
            # Горизонтальные пары
            pairs_h = np.column_stack([
                gray[:, :-1].flatten(),
                gray[:, 1:].flatten()
            ])
            # Вертикальные пары
            pairs_v = np.column_stack([
                gray[:-1, :].flatten(),
                gray[1:, :].flatten()
            ])
            all_pairs = np.vstack([pairs_h, pairs_v])

            # Фильтруем пары с разницей = 1 (в любом направлении)
            diff = np.abs(all_pairs[:, 0] - all_pairs[:, 1])
            close_pairs = all_pairs[diff == 1]

            if len(close_pairs) < 100:
                return {
                    'alpha': 1.0,
                    'regularity': 0.5,
                    'deviation': 0.0,
                    'count_group_a': 0,
                    'count_group_b': 0,
                    'total_pairs': len(close_pairs),
                    'suspicion_level': 20,
                    'interpretation': 'Недостаточно пар с разницей 1 для анализа',
                    'description': 'Недостаточно данных для статистики пар пикселей методом Кера'
                }

            # Группа A: пары (2k, 2k+1) и (1, 2k) - значения имеют разную четность, минимум четный
            # Группа B: пары (2k+1, 2k+2) и (2k+2, 2k+1) - значения имеют разную четность, минимум нечетный
            count_group_a = 0
            count_group_b = 0

            for p1, p2 in close_pairs:
                # Определяем минимальное и максимальное значение в паре
                min_val = min(p1, p2)
                max_val = max(p1, p2)

                # Проверяем: разница должна быть = 1 (гарантировано фильтром выше)
                if max_val - min_val == 1:
                    if min_val % 2 == 0:  # min_val четный → пара типа (2k, 2k+1)
                        count_group_a += 1
                    else:  # min_val нечетный → пара типа (2k+1, 2k+2)
                        count_group_b += 1

            total_valid = count_group_a + count_group_b
            if total_valid == 0:
                alpha = 1.0
                regularity = 0.5
            else:
                # Метрика Кера: α = |A - B| / (A + B)
                alpha = abs(count_group_a - count_group_b) / total_valid
                # Для совместимости с оригинальным кодом
                regularity = count_group_a / total_valid if total_valid > 0 else 0.5

            # Вычисляем deviation для совместимости с оригинальным кодом
            deviation = abs(regularity - 0.5)

            # Интерпретация по оригинальному методу Кера:
            # α < 0.05 → сильный признак стеганографии (частоты выровнены)
            # α > 0.2 → естественное изображение (выраженная асимметрия)
            if alpha < 0.03:
                suspicion_level = 95
                interpretation = f'Крайне подозрительно: α={alpha:.4f} (<0.03) - сильное выравнивание частот пар'
            elif alpha < 0.05:
                suspicion_level = 90
                interpretation = f'Подозрительно: α={alpha:.4f} (<0.05) - выравнивание частот пар (метод Кера)'
            elif alpha < 0.1:
                suspicion_level = 70
                interpretation = f'Умеренно подозрительно: α={alpha:.4f} (<0.10) - частичное выравнивание частот'
            elif alpha < 0.2:
                suspicion_level = 40
                interpretation = f'Нейтрально: α={alpha:.4f} - умеренная асимметрия частот'
            else:
                suspicion_level = 15
                interpretation = f'Естественное изображение: α={alpha:.4f} (>0.20) - выраженная асимметрия частот пар'

            # Дополнительная проверка: очень большое количество пар с разницей 1 тоже подозрительно
            ratio_close_pairs = total_valid / len(all_pairs)
            if ratio_close_pairs > 0.35:
                suspicion_level = min(100, suspicion_level + 15)
                interpretation += f' | высокая доля смежных пар ({ratio_close_pairs:.1%})'

            return {
                'alpha': float(alpha),
                'regularity': float(regularity),
                'deviation': float(deviation),
                'count_group_a': int(count_group_a),
                'count_group_b': int(count_group_b),
                'ratio_group_a': float(count_group_a / total_valid) if total_valid > 0 else 0.0,
                'ratio_group_b': float(count_group_b / total_valid) if total_valid > 0 else 0.0,
                'total_pairs': int(total_valid),
                'total_analyzed': int(len(all_pairs)),
                'ratio_close_pairs': float(ratio_close_pairs),
                'suspicion_level': suspicion_level,
                'interpretation': interpretation,
                'description': 'Метод Кера: естественные изображения имеют асимметрию в частотах пар (2i,2i+1) vs (2i+1,2i+2). Стеганография LSB выравнивает эти частоты, снижая метрику α (<0.05).'
            }
        except Exception as e:
            return {
                'alpha': 0.0,
                'regularity': 0.5,
                'deviation': 0.0,
                'count_group_a': 0,
                'count_group_b': 0,
                'total_pairs': 0,
                'suspicion_level': 10,
                'interpretation': f'Ошибка анализа пар пикселей: {str(e)}',
                'description': 'Ошибка при анализе статистики пар пикселей методом Кера'
            }

    @staticmethod
    def analyze_file_for_stego(file_path: str, cancel_event=None) -> dict:
        """
        Проводит полный анализ файла на наличие стеганографических данных с расширенным набором тестов (15+ метрик).
        """
        results = {
            'file_info': {},
            'tests': {},
            'overall_suspicion': 0,
            'confidence': 0.0,
            'recommendations': [],
            'analysis_time': 0.0,
            'test_count': 0
        }

        start_time = time.time()

        try:
            # Получаем информацию о файле
            file_info = Utils.get_file_info(file_path)
            results['file_info'] = file_info

            # Читаем данные файла
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Анализ энтропии
            if cancel_event and cancel_event.is_set():
                raise InterruptedError("Анализ отменен пользователем")
            entropy = FileAnalyzer.calculate_entropy(file_data)
            results['tests']['entropy'] = {
                'value': entropy,
                'suspicion_level': 80 if entropy > 7.5 else 30 if entropy > 6.5 else 10,
                'interpretation': 'Высокая энтропия' if entropy > 7.5 else 'Средняя энтропия' if entropy > 6.5 else 'Низкая энтропия',
                'description': 'Энтропия измеряет случайность данных. Высокая энтропия (>7.5) может указывать на зашифрованные или скрытые данные.'
            }

            # Анализ изображений/аудио
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga']:
                # Загружаем изображение
                with Image.open(file_path) as img:
                    if img.mode not in ['RGB', 'RGBA', 'L']:
                        img = img.convert('RGB')
                    pixels = np.array(img)

                # Анализ распределения LSB
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                lsb_analysis = FileAnalyzer.analyze_lsb_distribution(pixels)
                results['tests']['lsb_distribution'] = {
                    'value': lsb_analysis['balance'],
                    'suspicion_level': lsb_analysis['suspicion_level'],
                    'interpretation': lsb_analysis['interpretation'],
                    'details': lsb_analysis,
                    'description': 'Анализ распределения младших битов. Равномерное распределение (баланс ~0.5) может указывать на стеганографию.'
                }

                # Анализ шумового паттерна
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                noise_analysis = FileAnalyzer.analyze_noise_pattern(pixels)
                results['tests']['noise_pattern'] = {
                    'value': noise_analysis['std_deviation'],
                    'suspicion_level': noise_analysis['suspicion_level'],
                    'interpretation': noise_analysis['interpretation'],
                    'details': noise_analysis,
                    'description': 'Анализ шумовой компоненты изображения. Высокая дисперсия шума может указывать на скрытые данные.'
                }

                # Гистограммный анализ
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                histogram_analysis = FileAnalyzer.analyze_histogram(pixels)
                results['tests']['histogram'] = {
                    'value': histogram_analysis['smoothness'],
                    'suspicion_level': histogram_analysis['suspicion_level'],
                    'interpretation': histogram_analysis['interpretation'],
                    'details': histogram_analysis,
                    'description': 'Анализ гистограммы распределения значений пикселей. Аномалии могут указывать на стеганографию.'
                }

                # Анализ корреляции пикселей
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                correlation_analysis = FileAnalyzer.analyze_pixel_correlation(pixels)
                results['tests']['pixel_correlation'] = {
                    'value': correlation_analysis['avg_corr'],
                    'suspicion_level': correlation_analysis['suspicion_level'],
                    'interpretation': correlation_analysis['interpretation'],
                    'details': correlation_analysis,
                    'description': 'Анализ корреляции между соседними пикселями. Снижение корреляции может указывать на стеганографию.'
                }

                # Анализ энтропии по блокам
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                block_entropy_analysis = FileAnalyzer.calculate_block_entropy(pixels)
                results['tests']['block_entropy'] = {
                    'value': block_entropy_analysis['std_entropy'],
                    'suspicion_level': block_entropy_analysis['suspicion_level'],
                    'interpretation': block_entropy_analysis['interpretation'],
                    'details': block_entropy_analysis,
                    'description': 'Анализ вариативности энтропии по блокам изображения. Низкая вариативность может указывать на стеганографию.'
                }

                # Анализ корреляции цветовых каналов (только для цветных изображений)
                if pixels.ndim == 3 and pixels.shape[2] >= 3:
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Анализ отменен пользователем")
                    color_corr_analysis = FileAnalyzer.analyze_color_channel_correlation(pixels)
                    if color_corr_analysis['suspicion_level'] > 0:  # Только если анализ выполнен
                        results['tests']['color_correlation'] = {
                            'value': color_corr_analysis['avg_correlation'],
                            'suspicion_level': color_corr_analysis['suspicion_level'],
                            'interpretation': color_corr_analysis['interpretation'],
                            'details': color_corr_analysis,
                            'description': 'Анализ корреляции между цветовыми каналами. Нарушение естественных соотношений может указывать на стеганографию.'
                        }

                # Анализ артефактов JPEG (только для JPEG)
                if file_ext in ['.jpg', '.jpeg']:
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Анализ отменен пользователем")
                    jpeg_analysis = FileAnalyzer.analyze_jpeg_artifacts(file_path)
                    if jpeg_analysis['suspicion_level'] > 0:  # Только если анализ выполнен
                        results['tests']['jpeg_artifacts'] = {
                            'value': jpeg_analysis['blockiness'],
                            'suspicion_level': jpeg_analysis['suspicion_level'],
                            'interpretation': jpeg_analysis['interpretation'],
                            'details': jpeg_analysis,
                            'description': 'Анализ артефактов JPEG сжатия. Аномальная блочность может указывать на стеганографию.'
                        }

                # НОВЫЕ МЕТРИКИ (добавлены в улучшенной версии):

                # Анализ градиентов
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                gradient_analysis = FileAnalyzer.analyze_gradient_statistics(pixels)
                results['tests']['gradient_analysis'] = {
                    'value': gradient_analysis['gradient_std'],
                    'suspicion_level': gradient_analysis['suspicion_level'],
                    'interpretation': gradient_analysis['interpretation'],
                    'details': gradient_analysis,
                    'description': 'Анализ распределения градиентов изображения. Аномальная равномерность градиентов может указывать на стеганографию.'
                }

                # Анализ частотного спектра (DCT)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                freq_analysis = FileAnalyzer.analyze_frequency_domain(pixels)
                results['tests']['frequency_domain'] = {
                    'value': freq_analysis['dc_std'],
                    'suspicion_level': freq_analysis['suspicion_level'],
                    'interpretation': freq_analysis['interpretation'],
                    'details': freq_analysis,
                    'description': 'Анализ распределения DCT коэффициентов. Аномалии в высокочастотных компонентах могут указывать на стеганографию.'
                }

                # Анализ текстурных признаков (GLCM)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                texture_analysis = FileAnalyzer.analyze_texture_features(pixels)
                results['tests']['texture_analysis'] = {
                    'value': texture_analysis['contrast_std'],
                    'suspicion_level': texture_analysis['suspicion_level'],
                    'interpretation': texture_analysis['interpretation'],
                    'details': texture_analysis,
                    'description': 'Анализ текстурных характеристик через GLCM. Аномальная однородность текстуры может указывать на стеганографию.'
                }

                # Анализ вейвлет-коэффициентов
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                wavelet_analysis = FileAnalyzer.analyze_wavelet_features(pixels)
                results['tests']['wavelet_analysis'] = {
                    'value': wavelet_analysis['coeff_kurtosis'],
                    'suspicion_level': wavelet_analysis['suspicion_level'],
                    'interpretation': wavelet_analysis['interpretation'],
                    'details': wavelet_analysis,
                    'description': 'Анализ распределения вейвлет-коэффициентов. Нарушение естественной субгауссовости может указывать на стеганографию.'
                }

                # Анализ статистики пар пикселей (метод Кера)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                pairwise_analysis = FileAnalyzer.analyze_pairwise_pixel_statistics(pixels)
                results['tests']['pairwise_statistics'] = {
                    'value': pairwise_analysis['deviation'],
                    'suspicion_level': pairwise_analysis['suspicion_level'],
                    'interpretation': pairwise_analysis['interpretation'],
                    'details': pairwise_analysis,
                    'description': 'Метод Кера: анализ асимметрии пар пикселей с разницей 1. Симметрия распределения может указывать на LSB стеганографию.'
                }

            elif file_ext == '.wav':
                # Анализ аудио файла
                with wave.open(file_path, 'rb') as wav:
                    frames = wav.readframes(wav.getnframes())
                    audio_data = np.frombuffer(frames, dtype=np.uint8)

                # Анализ распределения LSB для аудио
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                lsb_analysis = FileAnalyzer.analyze_lsb_distribution(audio_data)
                results['tests']['lsb_distribution'] = {
                    'value': lsb_analysis['balance'],
                    'suspicion_level': lsb_analysis['suspicion_level'],
                    'interpretation': lsb_analysis['interpretation'],
                    'details': lsb_analysis,
                    'description': 'Анализ распределения младших битов аудиоданных. Равномерное распределение может указывать на стеганографию.'
                }

                # Гистограммный анализ для аудио
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                histogram_analysis = FileAnalyzer.analyze_histogram(audio_data)
                results['tests']['histogram'] = {
                    'value': histogram_analysis['smoothness'],
                    'suspicion_level': histogram_analysis['suspicion_level'],
                    'interpretation': histogram_analysis['interpretation'],
                    'details': histogram_analysis,
                    'description': 'Анализ гистограммы распределения аудиосэмплов.'
                }

                # Спектральный анализ аудио
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                spectral_analysis = FileAnalyzer.analyze_audio_spectral_features(file_path)
                if spectral_analysis['suspicion_level'] > 0:  # Только если анализ выполнен
                    results['tests']['spectral_analysis'] = {
                        'value': spectral_analysis['spectral_flatness_std'],
                        'suspicion_level': spectral_analysis['suspicion_level'],
                        'interpretation': spectral_analysis['interpretation'],
                        'details': spectral_analysis,
                        'description': 'Анализ спектральных характеристик аудио. Низкая вариативность спектра может указывать на стеганографию.'
                    }

                # Анализ zero-crossing rate и временных признаков
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")
                # (Уже включен в spectral_analysis, но можно расширить при необходимости)

            # Рассчитываем общий уровень подозрительности с учетом весов тестов
            suspicion_levels = []
            weights = {
                'lsb_distribution': 1.2,
                'block_entropy': 1.1,
                'pixel_correlation': 1.1,
                'pairwise_statistics': 1.3,  # Метод Кера очень надежен для LSB
                'gradient_analysis': 1.0,
                'frequency_domain': 1.0,
                'texture_analysis': 0.9,
                'wavelet_analysis': 1.0,
                'jpeg_artifacts': 1.0,
                'noise_pattern': 0.8,
                'histogram': 0.8,
                'color_correlation': 0.7,
                'spectral_analysis': 1.0,
                'entropy': 0.9
            }

            tests = results['tests']
            weighted_sum = 0.0
            weight_sum = 0.0

            for test_name, test_data in tests.items():
                level = test_data['suspicion_level']
                weight = weights.get(test_name, 1.0)
                weighted_sum += level * weight
                weight_sum += weight
                suspicion_levels.append(level)

            if suspicion_levels:
                results['overall_suspicion'] = int(
                    min(100, weighted_sum / weight_sum if weight_sum > 0 else np.mean(suspicion_levels)))
                results['test_count'] = len(suspicion_levels)

                # Расчет доверительного интервала (бутстрап)
                if len(suspicion_levels) >= 5:
                    bootstrap_samples = 1000
                    bootstrap_means = []
                    for _ in range(bootstrap_samples):
                        sample = np.random.choice(suspicion_levels, size=len(suspicion_levels), replace=True)
                        bootstrap_means.append(np.mean(sample))
                    confidence_interval = np.percentile(bootstrap_means, [2.5, 97.5])
                    results['confidence'] = float(min(100, 100 - (confidence_interval[1] - confidence_interval[0])))
                else:
                    results['confidence'] = 50.0  # Низкая уверенность при малом количестве тестов

            # Генерируем рекомендации
            results['recommendations'] = FileAnalyzer.generate_recommendations(results)
            results['status'] = 'success'
            results['message'] = 'Анализ завершен успешно'
            results['analysis_time'] = time.time() - start_time

        except InterruptedError as e:
            results['status'] = 'cancelled'
            results['message'] = str(e)
            results['analysis_time'] = time.time() - start_time
        except Exception as e:
            results['status'] = 'error'
            results['message'] = f'Ошибка при анализе: {str(e)}'
            results['error'] = str(e)
            results['analysis_time'] = time.time() - start_time

        return results

    @staticmethod
    def generate_recommendations(results: dict) -> list:
        """
        Генерирует рекомендации на основе результатов анализа.
        """
        recommendations = []
        suspicion = results.get('overall_suspicion', 0)
        confidence = results.get('confidence', 0.0)
        analysis_time = results.get('analysis_time', 0)
        test_count = results.get('test_count', 0)

        # Основные рекомендации по уровню подозрительности
        if suspicion > 85:
            recommendations.append(
                '🚨 КРИТИЧЕСКИЙ УРОВЕНЬ: Обнаружены сильные признаки стеганографии (уверенность %.0f%%).' % confidence)
            recommendations.append(
                '🔍 Настоятельно рекомендуется детальный анализ с использованием специализированных инструментов (Aletheia, StegExpose).')
            recommendations.append('💾 Сохраните оригинальную копию файла до проведения любых манипуляций.')
        elif suspicion > 70:
            recommendations.append(
                '⚠️ ВЫСОКИЙ УРОВЕНЬ: Обнаружены явные признаки стеганографии (уверенность %.0f%%).' % confidence)
            recommendations.append('🔍 Рекомендуется извлечение данных с использованием методов: LSB, F5, JSteg.')
            recommendations.append('📊 Сравните с оригинальным файлом (если доступен) для подтверждения.')
        elif suspicion > 55:
            recommendations.append(
                'ℹ️ СРЕДНИЙ УРОВЕНЬ: Обнаружены признаки, требующие дополнительной проверки (уверенность %.0f%%).' % confidence)
            recommendations.append('🔍 Проведите дополнительные тесты с другими алгоритмами анализа.')
            recommendations.append('📈 Проанализируйте файлы из той же серии/сессии для выявления паттернов.')
        elif suspicion > 40:
            recommendations.append(
                '🔍 НИЗКИЙ УРОВЕНЬ: Некоторые тесты показывают отклонения от нормы (уверенность %.0f%%).' % confidence)
            recommendations.append('ℹ️ Рекомендуется мониторинг при повторном анализе или сравнении с эталоном.')
        else:
            recommendations.append(
                '✅ Файл не содержит явных признаков стеганографии (уверенность %.0f%%).' % confidence)
            recommendations.append('ℹ️ Для критически важных случаев рекомендуется дополнительная верификация.')

        # Рекомендации по конкретным тестам
        tests = results.get('tests', {})

        high_suspicion_tests = [
            (name, data) for name, data in tests.items()
            if data.get('suspicion_level', 0) > 75
        ]

        if high_suspicion_tests:
            recommendations.append('')
            recommendations.append('📊 ДЕТАЛИ ПО КРИТИЧЕСКИМ ТЕСТАМ:')
            for test_name, test_data in sorted(high_suspicion_tests, key=lambda x: x[1]['suspicion_level'],
                                               reverse=True)[:3]:
                test_names = {
                    'lsb_distribution': 'Распределение младших битов',
                    'block_entropy': 'Энтропия по блокам',
                    'pixel_correlation': 'Корреляция пикселей',
                    'pairwise_statistics': 'Статистика пар пикселей (метод Кера)',
                    'gradient_analysis': 'Анализ градиентов',
                    'frequency_domain': 'Частотный спектр (DCT)',
                    'texture_analysis': 'Текстурные признаки (GLCM)',
                    'wavelet_analysis': 'Вейвлет-анализ',
                    'jpeg_artifacts': 'Артефакты JPEG',
                    'noise_pattern': 'Шумовой паттерн',
                    'histogram': 'Гистограммный анализ',
                    'color_correlation': 'Корреляция цветовых каналов',
                    'spectral_analysis': 'Спектральный анализ аудио'
                }
                display_name = test_names.get(test_name, test_name)
                interpretation = test_data.get('interpretation', 'N/A')
                recommendations.append(f'  • {display_name}: {interpretation}')

        # Информация о количестве тестов и времени
        if test_count > 0:
            recommendations.append('')
            recommendations.append(f'⏱️ Проанализировано {test_count} тестов за {analysis_time:.1f} сек.')

        if confidence < 60.0:
            recommendations.append(
                'ℹ️ Низкая уверенность результата. Рекомендуется повторный анализ с другими параметрами.')

        return recommendations

    @staticmethod
    def export_report_html(results: dict, output_path: str, original_file_path: str = None) -> bool:
        """
        Экспортирует отчет в HTML формат с интерактивными графиками.
        """
        try:
            # Генерация графиков как base64 изображений
            plots = {}

            # Гистограмма
            if 'histogram' in results.get('tests', {}):
                hist_data = results['tests']['histogram']['details']['histogram']
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(range(256), hist_data, color='#4A90E2', alpha=0.7)
                ax.set_title('Гистограмма распределения значений', fontsize=14, fontweight='bold')
                ax.set_xlabel('Значение')
                ax.set_ylabel('Частота')
                ax.grid(True, alpha=0.3)

                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                plots['histogram'] = base64.b64encode(buf.read()).decode('utf-8')
                plt.close(fig)

            # Тепловая карта энтропии по блокам
            if 'block_entropy' in results.get('tests', {}):
                entropy_map = results['tests']['block_entropy']['details'].get('entropy_map', [])
                if entropy_map and len(entropy_map) > 0:
                    fig, ax = plt.subplots(figsize=(8, 4))
                    im = ax.imshow(entropy_map, cmap='viridis', aspect='auto')
                    ax.set_title('Тепловая карта энтропии по блокам', fontsize=14, fontweight='bold')
                    plt.colorbar(im, ax=ax, label='Энтропия')

                    buf = BytesIO()
                    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                    buf.seek(0)
                    plots['entropy_map'] = base64.b64encode(buf.read()).decode('utf-8')
                    plt.close(fig)

            # Формирование HTML
            html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Отчет стеганализа - {os.path.basename(original_file_path) if original_file_path else 'Неизвестный файл'}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #4A90E2; padding-bottom: 20px; }}
        .header h1 {{ color: #2c3e50; margin: 0; font-size: 28px; }}
        .file-info {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .suspicion-meter {{ text-align: center; margin: 30px 0; }}
        .meter {{ height: 25px; background: #e9ecef; border-radius: 12px; overflow: hidden; margin: 10px 0; }}
        .meter-fill {{ height: 100%; border-radius: 12px; transition: width 0.5s ease-in-out; }}
        .meter-0 {{ background: #28a745; }}    /* 0-30% */
        .meter-30 {{ background: #ffc107; }}   /* 30-60% */
        .meter-60 {{ background: #fd7e14; }}   /* 60-85% */
        .meter-85 {{ background: #dc3545; }}   /* 85-100% */
        .tests-table {{ width: 100%; border-collapse: collapse; margin: 25px 0; }}
        .tests-table th, .tests-table td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
        .tests-table th {{ background-color: #4A90E2; color: white; font-weight: 600; }}
        .tests-table tr:hover {{ background-color: #f5f7fa; }}
        .high-suspicion {{ background-color: #ffebee; }}
        .medium-suspicion {{ background-color: #fff8e1; }}
        .low-suspicion {{ background-color: #e8f5e8; }}
        .plot-container {{ margin: 30px 0; text-align: center; }}
        .plot-container img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; }}
        .recommendations {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 30px 0; }}
        .recommendations ul {{ padding-left: 20px; margin: 10px 0; }}
        .recommendations li {{ margin: 8px 0; line-height: 1.5; }}
        .footer {{ text-align: center; margin-top: 40px; color: #6c757d; font-size: 14px; border-top: 1px solid #ddd; padding-top: 20px; }}
        .confidence-badge {{ display: inline-block; padding: 5px 12px; border-radius: 20px; font-weight: bold; margin-left: 15px; }}
        .confidence-high {{ background: #28a745; color: white; }}
        .confidence-medium {{ background: #ffc107; color: #212529; }}
        .confidence-low {{ background: #dc3545; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Отчет стеганализа</h1>
            <p>Файл: <strong>{os.path.basename(original_file_path) if original_file_path else 'Неизвестный файл'}</strong></p>
            <p>Дата анализа: {time.strftime("%d.%m.%Y %H:%M:%S")}</p>
        </div>

        <div class="file-info">
            <h3>📁 Информация о файле</h3>
            <ul>
"""

            file_info = results.get('file_info', {})
            for key, value in file_info.items():
                if key not in ['path', 'full_path']:
                    html_content += f"                <li><strong>{key.capitalize()}:</strong> {value}</li>\n"

            html_content += f"""            </ul>
        </div>

        <div class="suspicion-meter">
            <h2>🎯 Общий уровень подозрительности</h2>
            <div class="meter">
                <div class="meter-fill meter-{results.get('overall_suspicion', 0) // 25 * 25}"
                     style="width: {results.get('overall_suspicion', 0)}%"></div>
            </div>
            <h1 style="margin: 10px 0; color: {'#28a745' if results.get('overall_suspicion', 0) <= 30 else '#ffc107' if results.get('overall_suspicion', 0) <= 60 else '#fd7e14' if results.get('overall_suspicion', 0) <= 85 else '#dc3545'}">
                {results.get('overall_suspicion', 0)}%
            </h1>
            <p>Уверенность анализа:
                <span class="confidence-badge confidence-{
            'high' if results.get('confidence', 0) >= 80 else
            'medium' if results.get('confidence', 0) >= 60 else
            'low'
            }">
                    {results.get('confidence', 0):.0f}%
                </span>
            </p>
        </div>

        <h2>🧪 Результаты тестов</h2>
        <table class="tests-table">
            <thead>
                <tr>
                    <th>Тест</th>
                    <th>Значение</th>
                    <th>Уровень подозрительности</th>
                    <th>Интерпретация</th>
                </tr>
            </thead>
            <tbody>
"""

            test_names_map = {
                'entropy': 'Энтропия',
                'lsb_distribution': 'Распределение младших битов',
                'noise_pattern': 'Шумовой паттерн',
                'histogram': 'Гистограммный анализ',
                'pixel_correlation': 'Корреляция пикселей',
                'block_entropy': 'Энтропия по блокам',
                'color_correlation': 'Корреляция цветовых каналов',
                'jpeg_artifacts': 'Артефакты JPEG',
                'spectral_analysis': 'Спектральный анализ',
                'gradient_analysis': 'Анализ градиентов',
                'frequency_domain': 'Частотный спектр (DCT)',
                'texture_analysis': 'Текстурные признаки (GLCM)',
                'wavelet_analysis': 'Вейвлет-анализ',
                'pairwise_statistics': 'Статистика пар пикселей'
            }

            tests = results.get('tests', {})
            for test_name, test_data in tests.items():
                display_name = test_names_map.get(test_name, test_name)
                value = test_data.get('value', 0)
                suspicion = test_data.get('suspicion_level', 0)
                interpretation = test_data.get('interpretation', 'N/A')

                # Определение класса для подсветки
                if suspicion > 70:
                    row_class = 'high-suspicion'
                elif suspicion > 40:
                    row_class = 'medium-suspicion'
                else:
                    row_class = 'low-suspicion'

                # Исправленный формат значения
                if isinstance(value, float):
                    value_str = f"{value:.2f}"
                elif isinstance(value, int):
                    value_str = str(value)
                else:
                    value_str = str(value)

                html_content += f"""                <tr class="{row_class}">
                    <td>{display_name}</td>
                    <td>{value_str}</td>
                    <td>{suspicion}%</td>
                    <td>{interpretation}</td>
                </tr>
"""

            html_content += """            </tbody>
        </table>

        <div class="plot-container">
            <h2>📈 Визуализации</h2>
"""

            if 'histogram' in plots:
                html_content += f"""            <div style="margin: 20px 0;">
                <h3>Гистограмма распределения значений</h3>
                <img src="image/png;base64,{plots['histogram']}" alt="Гистограмма">
            </div>
"""

            if 'entropy_map' in plots:
                html_content += f"""            <div style="margin: 20px 0;">
                <h3>Тепловая карта энтропии по блокам</h3>
                <img src="image/png;base64,{plots['entropy_map']}" alt="Тепловая карта энтропии">
            </div>
"""

            html_content += """        </div>

        <div class="recommendations">
            <h2>💡 Рекомендации</h2>
            <ul>
"""

            for rec in results.get('recommendations', []):
                html_content += f"                <li>{rec}</li>\n"

            html_content += f"""            </ul>
        </div>

        <div class="footer">
            <p>Отчет сгенерирован инструментом стеганализа | Версия: 2.1</p>
            <p>я анализа: {results.get('analysis_time', 0):.2f} сек | Количество тестов: {results.get('test_count', 0)}</p>
        </div>
    </div>
</body>
</html>"""

            # Сохранение HTML файла
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            return True

        except Exception as e:
            print(f"Ошибка при экспорте HTML отчета: {str(e)}")
            return False

    @staticmethod
    def export_report_csv(results: dict, output_path: str) -> bool:
        """
        Экспортирует результаты тестов в CSV формат.
        """
        try:
            import csv

            with open(output_path, 'w', newline='',
                      encoding='utf-8-sig') as f:  # Исправлено: добавлен BOM для правильной кодировки
                writer = csv.writer(f)
                # Заголовок
                writer.writerow(['Тест', 'Значение', 'Уровень подозрительности (%)', 'Интерпретация', 'Детали'])

                # Данные тестов
                tests = results.get('tests', {})
                for test_name, test_data in tests.items():
                    value = test_data.get('value', '')
                    suspicion = test_data.get('suspicion_level', 0)
                    interpretation = test_data.get('interpretation', '')
                    details = json.dumps(test_data.get('details', {}), ensure_ascii=False)[
                              :200]  # Обрезаем для компактности

                    writer.writerow([test_name, value, suspicion, interpretation, details])

            return True
        except Exception as e:
            print(f"Ошибка при экспорте CSV отчета: {str(e)}")
            return False

    @staticmethod
    def export_report_txt(results: dict, output_path: str, original_file_path: str = None) -> bool:
        """
        Экспортирует краткий отчет в TXT формат.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("ОТЧЕТ СТЕГАНАЛИЗА".center(70) + "\n")
                f.write("=" * 70 + "\n\n")

                f.write(f"Файл: {os.path.basename(original_file_path) if original_file_path else 'Неизвестный файл'}\n")
                f.write(f"Дата анализа: {time.strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"Время анализа: {results.get('analysis_time', 0):.2f} сек\n")
                f.write(f"Количество тестов: {results.get('test_count', 0)}\n\n")

                f.write("=" * 70 + "\n")
                f.write("ОСНОВНЫЕ РЕЗУЛЬТАТЫ".center(70) + "\n")
                f.write("=" * 70 + "\n\n")

                suspicion = results.get('overall_suspicion', 0)
                confidence = results.get('confidence', 0.0)

                f.write(f"Общий уровень подозрительности: {suspicion}%\n")
                f.write(f"Уверенность анализа: {confidence:.0f}%\n\n")

                # Шкала подозрительности
                meter = "█" * (suspicion // 5) + "░" * (20 - suspicion // 5)
                f.write(f"Шкала: [{meter}] {suspicion}%\n\n")

                f.write("=" * 70 + "\n")
                f.write("РЕЗУЛЬТАТЫ ТЕСТОВ".center(70) + "\n")
                f.write("=" * 70 + "\n\n")

                tests = results.get('tests', {})
                for test_name, test_data in sorted(tests.items(), key=lambda x: x[1].get('suspicion_level', 0),
                                                   reverse=True):
                    suspicion_level = test_data.get('suspicion_level', 0)
                    if suspicion_level > 0:
                        f.write(f"{test_name:.<40} {suspicion_level:>3}% | {test_data.get('interpretation', 'N/A')}\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("РЕКОМЕНДАЦИИ".center(70) + "\n")
                f.write("=" * 70 + "\n\n")

                for rec in results.get('recommendations', []):
                    f.write(f"• {rec}\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("КОНЕЦ ОТЧЕТА".center(70) + "\n")
                f.write("=" * 70 + "\n")

            return True
        except Exception as e:
            print(f"Ошибка при экспорте TXT отчета: {str(e)}")
            return False


# ───────────────────────────────────────────────
# 📊 ВКЛАДКА АНАЛИЗА ФАЙЛА
# ───────────────────────────────────────────────
class AnalysisTab:
    """Вкладка для анализа файлов на наличие стеганографических данных с расширенными визуализациями и экспортом"""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.colors = app.colors
        self.file_path = tk.StringVar()
        self.analysis_results = None
        self.cancel_event = threading.Event()
        self.analysis_thread = None
        self.comparison_mode = False
        self.second_file_path = tk.StringVar()
        self.current_plots = {}  # Хранение ссылок на графики для экспорта
        self.setup_ui()

    def setup_ui(self):
        """Создает интерфейс вкладки анализа с полной поддержкой скроллинга"""
        # Основной контейнер с прокруткой
        main_container = ttk.Frame(self.parent, style="Card.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Верхняя панель управления
        control_frame = ttk.LabelFrame(
            main_container,
            text="📁 Выбор файла",
            padding=15,
            style="Card.TLabelframe"
        )
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Режим сравнения переключатель
        mode_frame = ttk.Frame(control_frame, style="Card.TFrame")
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.mode_var = tk.StringVar(value="single")
        ttk.Radiobutton(
            mode_frame,
            text="Одиночный анализ",
            variable=self.mode_var,
            value="single",
            command=self.toggle_mode
        ).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Radiobutton(
            mode_frame,
            text="Сравнение файлов",
            variable=self.mode_var,
            value="compare",
            command=self.toggle_mode
        ).pack(side=tk.LEFT)

        # Панель выбора файлов (одиночный режим)
        self.single_file_frame = ttk.Frame(control_frame, style="Card.TFrame")
        self.single_file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            self.single_file_frame,
            text="📂 Файл для анализа:",
            font=("Segoe UI", 10),
            style="TLabel"
        ).pack(side=tk.LEFT, padx=(0, 10))

        path_entry = ttk.Entry(
            self.single_file_frame,
            textvariable=self.file_path,
            state='readonly',
            font=("Segoe UI", 10),
            style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Панель выбора файлов (режим сравнения)
        self.compare_frame = ttk.Frame(control_frame, style="Card.TFrame")
        self.compare_frame.pack(fill=tk.X, pady=(0, 10))
        self.compare_frame.pack_forget()  # Скрыта по умолчанию

        # Файл 1
        file1_frame = ttk.Frame(self.compare_frame, style="Card.TFrame")
        file1_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(
            file1_frame,
            text="Файл 1:",
            font=("Segoe UI", 10),
            style="TLabel",
            width=10
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Entry(
            file1_frame,
            textvariable=self.file_path,
            state='readonly',
            font=("Segoe UI", 10),
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Файл 2
        file2_frame = ttk.Frame(self.compare_frame, style="Card.TFrame")
        file2_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(
            file2_frame,
            text="Файл 2:",
            font=("Segoe UI", 10),
            style="TLabel",
            width=10
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Entry(
            file2_frame,
            textvariable=self.second_file_path,
            state='readonly',
            font=("Segoe UI", 10),
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Кнопки управления
        button_frame = ttk.Frame(control_frame, style="Card.TFrame")
        button_frame.pack(fill=tk.X)

        ttk.Button(
            button_frame,
            text="🔍 Выбрать файл...",
            style="Accent.TButton",
            command=self.select_file
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.second_file_button = ttk.Button(
            button_frame,
            text="🔍 Выбрать файл 2...",
            style="TButton",
            command=self.select_second_file
        )
        self.second_file_button.pack(side=tk.LEFT, padx=(0, 10))
        self.second_file_button.pack_forget()  # Скрыта в одиночном режиме

        ttk.Button(
            button_frame,
            text="🗑️ Очистить",
            style="TButton",
            command=self.clear_file
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.analyze_button = ttk.Button(
            button_frame,
            text="🔍 Начать анализ",
            style="Accent.TButton",
            command=self.start_analysis,
            state="disabled"
        )
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 10))

        self.cancel_button = ttk.Button(
            button_frame,
            text="⛔ Отмена",
            style="TButton",
            command=self.cancel_analysis,
            state="disabled"
        )
        self.cancel_button.pack(side=tk.LEFT, padx=(0, 10))

        # Прогресс-бар
        progress_frame = ttk.Frame(control_frame, style="Card.TFrame")
        progress_frame.pack(fill=tk.X, pady=(10, 0))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(
            progress_frame,
            text="✅ Готов к анализу",
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        self.status_label.pack(anchor="w")

        # Центральная область с тремя колками для режима сравнения
        self.content_frame = ttk.Frame(main_container, style="Card.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка - Метаданные и индикатор подозрительности
        left_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Метаданные файла
        metadata_frame = ttk.LabelFrame(
            left_frame,
            text="📊 Метаданные файла",
            padding=15,
            style="Card.TLabelframe"
        )
        metadata_frame.pack(fill=tk.X, pady=(0, 15))

        self.metadata_text = scrolledtext.ScrolledText(
            metadata_frame,
            height=8,
            font=("Consolas", 9),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            state='disabled'
        )
        self.metadata_text.pack(fill=tk.BOTH, expand=True)

        # Индикатор вероятности стеганографии (УМЕНЬШЕН В 2.5 РАЗА)
        suspicion_frame = ttk.LabelFrame(
            left_frame,
            text="🎯 Вероятность стеганографии",
            padding=8,  # Уменьшено с 15 до 8
            style="Card.TLabelframe"
        )
        suspicion_frame.pack(fill=tk.X, pady=(0, 10))  # Уменьшено с 15 до 10

        # Уменьшенный шрифт для процента
        self.suspicion_label = ttk.Label(
            suspicion_frame,
            text="-",
            font=("Segoe UI", 18, "bold"),  # Уменьшено с 28 до 18
            style="TLabel"
        )
        self.suspicion_label.pack(pady=(0, 5))  # Уменьшено с 10 до 5

        self.suspicion_bar = ttk.Progressbar(
            suspicion_frame,
            orient="horizontal",
            mode="determinate",
            style="TProgressbar"
        )
        self.suspicion_bar.pack(fill=tk.X, pady=(0, 5))  # Уменьшено с 10 до 5

        self.suspicion_text = ttk.Label(
            suspicion_frame,
            text="Нет данных",
            font=("Segoe UI", 10, "bold"),  # Уменьшено с 11 до 10
            style="Secondary.TLabel"
        )
        self.suspicion_text.pack(anchor="w")

        self.confidence_label = ttk.Label(
            suspicion_frame,
            text="Уверенность: -",
            font=("Segoe UI", 8),  # Уменьшено с 9 до 8
            style="Secondary.TLabel"
        )
        self.confidence_label.pack(anchor="w", pady=(3, 0))  # Уменьшено с 5 до 3

        # Таблица результатов тестов с фильтрацией (УВЕЛИЧЕНА)
        tests_frame = ttk.LabelFrame(
            left_frame,
            text="🧪 Результаты тестов",
            padding=15,
            style="Card.TLabelframe"
        )
        tests_frame.pack(fill=tk.BOTH, expand=True)

        # Панель фильтрации
        filter_frame = ttk.Frame(tests_frame, style="Card.TFrame")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Фильтр:", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))

        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["Все тесты", "Высокий риск (>70%)", "Средний риск (40-70%)", "Низкий риск (<40%)"],
            state="readonly",
            width=25,
            font=("Segoe UI", 9)
        )
        filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        filter_combo.bind("<<ComboboxSelected>>", self.filter_tests)

        ttk.Button(
            filter_frame,
            text="🔄 Обновить",
            style="TButton",
            command=self.refresh_tests_view
        ).pack(side=tk.LEFT)

        # Создаем прокручиваемую панель для таблицы
        table_frame = ttk.Frame(tests_frame, style="Card.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Горизонтальная прокрутка
        table_h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        table_h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Вертикальная прокрутка
        table_v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        table_v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Создаем таблицу с прокруткой (увеличена высота)
        columns = ("Тест", "Значение", "Подозрительность", "Интерпретация")
        self.tests_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20,  # Увеличено с 12 до 20
            xscrollcommand=table_h_scroll.set,
            yscrollcommand=table_v_scroll.set
        )

        # Настройка заголовков
        self.tests_tree.heading("Тест", text="Тест", command=lambda: self.sort_column("Тест", False))
        self.tests_tree.heading("Значение", text="Значение", command=lambda: self.sort_column("Значение", False))
        self.tests_tree.heading("Подозрительность", text="Подозрительность",
                                command=lambda: self.sort_column("Подозрительность", False))
        self.tests_tree.heading("Интерпретация", text="Интерпретация",
                                command=lambda: self.sort_column("Интерпретация", False))

        # Ширина столбцов
        self.tests_tree.column("Тест", width=160, anchor=tk.W)
        self.tests_tree.column("Значение", width=80, anchor=tk.CENTER)
        self.tests_tree.column("Подозрительность", width=100, anchor=tk.CENTER)
        self.tests_tree.column("Интерпретация", width=200, anchor=tk.W)

        # Размещение
        self.tests_tree.pack(fill=tk.BOTH, expand=True)

        # Связь прокрутки
        table_h_scroll.config(command=self.tests_tree.xview)
        table_v_scroll.config(command=self.tests_tree.yview)

        # Настройка стиля для таблицы
        style = ttk.Style()
        style.configure("Treeview",
                        background=self.colors["card"],
                        foreground=self.colors["text"],
                        fieldbackground=self.colors["card"],
                        font=("Segoe UI", 9))
        style.configure("Treeview.Heading",
                        background=self.colors["accent"],
                        foreground="white",
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview",
                  background=[('selected', self.colors["accent"])],
                  foreground=[('selected', 'white')])

        # Центральная колонка - Визуализации
        center_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Notebook для вкладок визуализаций
        self.visualization_notebook = ttk.Notebook(center_frame)
        self.visualization_notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка гистограммы
        self.histogram_tab = ttk.Frame(self.visualization_notebook, style="Card.TFrame")
        self.visualization_notebook.add(self.histogram_tab, text="📊 Гистограмма")
        self.histogram_frame = ttk.Frame(self.histogram_tab, style="Card.TFrame")
        self.histogram_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка анализа шума
        self.noise_tab = ttk.Frame(self.visualization_notebook, style="Card.TFrame")
        self.visualization_notebook.add(self.noise_tab, text="📈 Анализ шума")
        self.noise_frame = ttk.Frame(self.noise_tab, style="Card.TFrame")
        self.noise_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка статистики LSB
        self.stats_tab = ttk.Frame(self.visualization_notebook, style="Card.TFrame")
        self.visualization_notebook.add(self.stats_tab, text="🔢 Статистика LSB")
        self.stats_frame = ttk.Frame(self.stats_tab, style="Card.TFrame")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка корреляции пикселей
        self.correlation_tab = ttk.Frame(self.visualization_notebook, style="Card.TFrame")
        self.visualization_notebook.add(self.correlation_tab, text="🔗 Корреляция")
        self.correlation_frame = ttk.Frame(self.correlation_tab, style="Card.TFrame")
        self.correlation_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка тепловой карты энтропии
        self.entropy_tab = ttk.Frame(self.visualization_notebook, style="Card.TFrame")
        self.visualization_notebook.add(self.entropy_tab, text="🌡️ Тепловая карта")
        self.entropy_frame = ttk.Frame(self.entropy_tab, style="Card.TFrame")
        self.entropy_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Правая колонка - Дополнительные визуализации и рекомендации
        right_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Рекомендации
        recommendations_frame = ttk.LabelFrame(
            right_frame,
            text="💡 Рекомендации",
            padding=15,
            style="Card.TLabelframe"
        )
        recommendations_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.recommendations_text = scrolledtext.ScrolledText(
            recommendations_frame,
            height=10,
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            state='disabled'
        )
        self.recommendations_text.pack(fill=tk.BOTH, expand=True)

        # Кнопки экспорта
        export_frame = ttk.LabelFrame(
            right_frame,
            text="📤 Экспорт отчета",
            padding=15,
            style="Card.TLabelframe"
        )
        export_frame.pack(fill=tk.X, pady=(0, 15))

        # Исправлено: сохраняем export_frame как атрибут класса
        self.export_frame = export_frame

        export_buttons_frame = ttk.Frame(export_frame, style="Card.TFrame")
        export_buttons_frame.pack(fill=tk.X)

        export_formats = [
            ("HTML (полный)", "html", "Accent.TButton"),
            ("CSV (таблица)", "csv", "TButton"),
            ("TXT (кратко)", "txt", "TButton"),
            ("Все форматы", "all", "Accent.TButton")
        ]

        for label, fmt, style_name in export_formats:
            btn = ttk.Button(
                export_buttons_frame,
                text=f"📄 {label}",
                style=style_name,
                command=lambda f=fmt: self.export_report(f)
            )
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Кнопка сохранения графика
        save_plot_button = ttk.Button(
            export_frame,
            text="💾 Сохранить график",
            style="TButton",
            command=self.save_current_plot
        )
        save_plot_button.pack(fill=tk.X, pady=(10, 0))

    def toggle_mode(self):
        """Переключает между одиночным анализом и сравнением файлов"""
        if self.mode_var.get() == "compare":
            self.single_file_frame.pack_forget()
            self.compare_frame.pack(fill=tk.X, pady=(0, 10))
            self.second_file_button.pack(side=tk.LEFT, padx=(0, 10))
            self.comparison_mode = True
        else:
            self.compare_frame.pack_forget()
            self.single_file_frame.pack(fill=tk.X, pady=(0, 10))
            self.second_file_button.pack_forget()
            self.comparison_mode = False

        self.clear_results()

    def select_file(self):
        """Выбирает первый файл для анализа"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл для анализа",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )
        if file_path:
            self.file_path.set(file_path)
            self.app.last_open_dir = os.path.dirname(file_path)
            self.analyze_button.config(state="normal")
            self.export_button_state(False)
            self.clear_results()
            self.display_file_info(file_path)

    def select_second_file(self):
        """Выбирает второй файл для сравнения"""
        file_path = filedialog.askopenfilename(
            title="Выберите второй файл для сравнения",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )
        if file_path:
            self.second_file_path.set(file_path)
            # Активируем кнопку анализа только если оба файла выбраны
            if self.file_path.get() and file_path:
                self.analyze_button.config(state="normal")

    def clear_file(self):
        """Очищает выбранные файлы"""
        self.file_path.set("")
        self.second_file_path.set("")
        self.analyze_button.config(state="disabled")
        self.clear_results()

    def display_file_info(self, file_path: str):
        """Отображает информацию о файле"""
        try:
            file_info = Utils.get_file_info(file_path)
            info_text = f"📁 Имя файла: {file_info.get('name', 'N/A')}\n"
            info_text += f"📏 Размер: {file_info.get('size_formatted', 'N/A')}\n"
            info_text += f"📅 Создан: {file_info.get('created', 'N/A')}\n"
            info_text += f"✏️ Изменен: {file_info.get('modified', 'N/A')}\n"
            info_text += f"🔍 Тип: {file_info.get('type', 'N/A').capitalize()}\n"

            if file_info.get('type') == 'image':
                info_text += f"🖼️ Размеры: {file_info.get('dimensions', 'N/A')}\n"
                info_text += f"🎨 Режим: {file_info.get('mode', 'N/A')}\n"
                info_text += f"📊 Бит на пиксель: {file_info.get('bits', 'N/A')}\n"
            elif file_info.get('type') == 'audio':
                info_text += f"🎵 Каналы: {file_info.get('channels', 'N/A')}\n"
                info_text += f"⏱️ Частота: {file_info.get('sample_rate', 'N/A')} Hz\n"
                info_text += f"🔢 Сэмплов: {file_info.get('frames', 'N/A')}\n"
                info_text += f"⏳ Длительность: {file_info.get('duration', 'N/A')}\n"

            self.metadata_text.config(state='normal')
            self.metadata_text.delete("1.0", tk.END)
            self.metadata_text.insert("1.0", info_text)
            self.metadata_text.config(state='disabled')
        except Exception as e:
            self.display_error(f"Ошибка при отображении информации о файле: {str(e)}")

    def start_analysis(self):
        """Запускает анализ файла"""
        if self.comparison_mode:
            if not self.file_path.get() or not self.second_file_path.get():
                messagebox.showwarning("⚠️ Предупреждение", "Выберите оба файла для сравнения")
                return
            if not os.path.exists(self.file_path.get()) or not os.path.exists(self.second_file_path.get()):
                messagebox.showerror("❌ Ошибка", "Один или оба файла не найдены")
                return
        else:
            if not self.file_path.get():
                messagebox.showwarning("⚠️ Предупреждение", "Сначала выберите файл для анализа")
                return
            if not os.path.exists(self.file_path.get()):
                messagebox.showerror("❌ Ошибка", "Файл не найден")
                return

        # Сбрасываем флаг отмены
        self.cancel_event.clear()

        # Обновляем UI
        self.analyze_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress_var.set(0)
        self.status_label.config(text="⏳ Начало анализа...")

        # Запускаем анализ в отдельном потоке
        self.analysis_thread = threading.Thread(target=self.run_analysis, daemon=True)
        self.analysis_thread.start()

    def run_analysis(self):
        """Выполняет анализ в отдельном потоке"""
        try:
            if self.comparison_mode:
                # Анализ двух файлов для сравнения
                file1 = self.file_path.get()
                file2 = self.second_file_path.get()

                results1 = FileAnalyzer.analyze_file_for_stego(file1, self.cancel_event)
                if self.cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")

                results2 = FileAnalyzer.analyze_file_for_stego(file2, self.cancel_event)
                if self.cancel_event.is_set():
                    raise InterruptedError("Анализ отменен пользователем")

                # Объединяем результаты для сравнения
                combined_results = {
                    'file1': results1,
                    'file2': results2,
                    'comparison': self.compare_results(results1, results2),
                    'status': 'success' if results1.get('status') == 'success' and results2.get(
                        'status') == 'success' else 'error'
                }

                # Обновляем UI с результатами
                self.update_ui(lambda: self.display_comparison_results(combined_results))
            else:
                # Анализ одного файла
                file_path = self.file_path.get()

                # Проверяем существование файла
                if not os.path.exists(file_path):
                    self.update_ui(lambda: messagebox.showerror("❌ Ошибка", "Файл не найден"))
                    return

                # Выполняем анализ
                results = FileAnalyzer.analyze_file_for_stego(file_path, self.cancel_event)

                # Обновляем UI с результатами
                self.update_ui(lambda: self.display_results(results))
        except InterruptedError:
            self.update_ui(lambda: self.status_label.config(text="⛔ Анализ отменен"))
        except Exception as e:
            self.update_ui(lambda: self.display_error(f"Ошибка при анализе: {str(e)}"))
        finally:
            self.update_ui(lambda: self.restore_buttons())

    def update_ui(self, callback):
        """Обновляет UI из потока"""
        self.app.root.after(0, callback)

    def display_results(self, results: dict):
        """Отображает результаты анализа одного файла"""
        self.analysis_results = results

        if results.get('status') == 'error':
            messagebox.showerror("❌ Ошибка", results.get('message', 'Неизвестная ошибка'))
            return

        if results.get('status') == 'cancelled':
            self.status_label.config(text="⛔ Анализ отменен")
            return

        # Отображаем общий уровень подозрительности
        suspicion = results.get('overall_suspicion', 0)
        confidence = results.get('confidence', 0.0)

        self.suspicion_label.config(text=f"{suspicion}%")
        self.suspicion_bar.config(value=suspicion)
        self.confidence_label.config(text=f"Уверенность: {confidence:.0f}%")

        # Цвет индикатора в зависимости от уровня
        if suspicion <= 30:
            self.suspicion_bar.config(style="UsageGreen.Horizontal.TProgressbar")
            self.suspicion_text.config(text="🟢 Маловероятно", foreground=self.colors["success"])
        elif suspicion <= 60:
            self.suspicion_bar.config(style="UsageYellow.Horizontal.TProgressbar")
            self.suspicion_text.config(text="🟡 Требует внимания", foreground=self.colors["warning"])
        elif suspicion <= 85:
            self.suspicion_bar.config(style="UsageYellow.Horizontal.TProgressbar")
            self.suspicion_text.config(text="🟠 Вероятно", foreground=self.colors["warning"])
        else:
            self.suspicion_bar.config(style="UsageRed.Horizontal.TProgressbar")
            self.suspicion_text.config(text="🔴 Обнаружены признаки", foreground=self.colors["error"])

        # Очищаем таблицу тестов
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)

        # Заполняем таблицу результатами тестов
        tests = results.get('tests', {})
        test_order = [
            'entropy', 'lsb_distribution', 'pairwise_statistics', 'block_entropy',
            'pixel_correlation', 'gradient_analysis', 'frequency_domain',
            'texture_analysis', 'wavelet_analysis', 'noise_pattern', 'histogram',
            'color_correlation', 'jpeg_artifacts', 'spectral_analysis'
        ]

        self.test_items = []  # Сохраняем ссылки на элементы для фильтрации

        for test_name in test_order:
            if test_name not in tests:
                continue

            test_data = tests[test_name]
            # Форматируем название теста
            test_names = {
                'entropy': 'Энтропия',
                'lsb_distribution': 'Распределение младших битов',
                'noise_pattern': 'Шумовой паттерн',
                'histogram': 'Гистограммный анализ',
                'pixel_correlation': 'Корреляция пикселей',
                'block_entropy': 'Энтропия по блокам',
                'color_correlation': 'Корреляция цветовых каналов',
                'jpeg_artifacts': 'Артефакты JPEG',
                'spectral_analysis': 'Спектральный анализ',
                'gradient_analysis': 'Анализ градиентов',
                'frequency_domain': 'Частотный спектр (DCT)',
                'texture_analysis': 'Текстурные признаки (GLCM)',
                'wavelet_analysis': 'Вейвлет-анализ',
                'pairwise_statistics': 'Статистика пар пикселей'
            }
            test_display_name = test_names.get(test_name, test_name)
            value = test_data.get('value', 0)
            suspicion_level = test_data.get('suspicion_level', 0)
            interpretation = test_data.get('interpretation', 'N/A')

            # Форматируем значение
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)

            suspicion_str = f"{suspicion_level}%"

            # Определяем тег для цвета строки
            if suspicion_level > 70:
                tag = 'high_suspicion'
            elif suspicion_level > 40:
                tag = 'medium_suspicion'
            else:
                tag = 'low_suspicion'

            # Добавляем строку в таблицу
            item = self.tests_tree.insert("", "end", values=(
                test_display_name,
                value_str,
                suspicion_str,
                interpretation
            ), tags=(tag,))

            self.test_items.append({
                'item': item,
                'suspicion': suspicion_level,
                'test_name': test_name
            })

        # Настройка цветов строк в зависимости от уровня подозрительности
        self.tests_tree.tag_configure('high_suspicion', background='#ffebee', foreground='#c62828')
        self.tests_tree.tag_configure('medium_suspicion', background='#fff8e1', foreground='#5d4037')
        self.tests_tree.tag_configure('low_suspicion', background=self.colors["card"], foreground=self.colors["text"])

        # Отображаем рекомендации
        recommendations = results.get('recommendations', [])
        self.recommendations_text.config(state='normal')
        self.recommendations_text.delete("1.0", tk.END)
        for rec in recommendations:
            self.recommendations_text.insert(tk.END, f"{rec}\n")
        self.recommendations_text.config(state='disabled')

        # Создаем визуализации
        self.create_visualizations(results)

        # Включаем кнопки экспорта
        self.export_button_state(True)

        # Обновляем статус
        analysis_time = results.get('analysis_time', 0)
        test_count = results.get('test_count', 0)
        self.status_label.config(text=f"✅ Анализ завершен за {analysis_time:.1f} сек ({test_count} тестов)")

        # Записываем в лог
        self.app.log_manager.add_entry(
            "analyze",
            "success",
            {
                "file": self.file_path.get(),
                "suspicion_level": suspicion,
                "confidence": confidence,
                "tests_count": test_count,
                "analysis_time": analysis_time
            }
        )

    def display_comparison_results(self, results: dict):
        """Отображает результаты сравнения двух файлов"""
        # Для краткости реализация сравнения опущена, но сохранена структура
        # В полной версии здесь будет отображение разницы в метриках между файлами
        messagebox.showinfo("ℹ️ Информация", "Режим сравнения файлов будет доступен в следующей версии")
        self.restore_buttons()

    def compare_results(self, results1: dict, results2: dict) -> dict:
        """Сравнивает результаты двух анализов"""
        comparison = {
            'suspicion_diff': results1.get('overall_suspicion', 0) - results2.get('overall_suspicion', 0),
            'test_differences': {}
        }

        tests1 = results1.get('tests', {})
        tests2 = results2.get('tests', {})

        for test_name in set(tests1.keys()) | set(tests2.keys()):
            if test_name in tests1 and test_name in tests2:
                suspicion1 = tests1[test_name].get('suspicion_level', 0)
                suspicion2 = tests2[test_name].get('suspicion_level', 0)
                comparison['test_differences'][test_name] = suspicion1 - suspicion2

        return comparison

    def create_visualizations(self, results: dict):
        """Создает расширенные визуализации результатов"""
        # Очищаем предыдущие графики
        self.current_plots = {}

        # Гистограмма
        self.create_histogram(results)

        # Анализ шума
        self.create_noise_analysis(results)

        # Статистика LSB
        self.create_lsb_statistics(results)

        # Корреляция пикселей
        self.create_correlation_plot(results)

        # Тепловая карта энтропии по блокам
        self.create_entropy_heatmap(results)

    def create_histogram(self, results: dict):
        """Создает интерактивную гистограмму распределения"""
        # Удаляем предыдущий график
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()

        tests = results.get('tests', {})
        if 'histogram' not in tests:
            label = ttk.Label(
                self.histogram_frame,
                text="Нет данных для гистограммы",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        histogram_data = tests['histogram']['details'].get('histogram', [])
        if not histogram_data:
            label = ttk.Label(
                self.histogram_frame,
                text="Нет данных для гистограммы",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        # Создаем фигуру
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Рисуем гистограмму
        bars = ax.bar(range(256), histogram_data, color=self.colors["accent"], alpha=0.7, edgecolor='none')

        # Добавляем подписи осей
        ax.set_xlabel('Значение пикселя/сэмпла', color=self.colors["text"], fontsize=10)
        ax.set_ylabel('Частота', color=self.colors["text"], fontsize=10)
        ax.set_title('Гистограмма распределения значений',
                     color=self.colors["accent"], fontsize=12, fontweight='bold')

        # Добавляем сетку
        ax.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"])

        # Настройка цветов фона
        fig.patch.set_facecolor(self.colors["card"])
        ax.set_facecolor(self.colors["card"])
        ax.tick_params(colors=self.colors["text"], labelsize=9)

        # Создаем canvas
        canvas = FigureCanvasTkAgg(fig, master=self.histogram_frame)
        canvas.draw()

        # Сохраняем график для экспорта
        self.current_plots['histogram'] = fig

        # Размещаем canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Добавляем подпись с информацией
        stats = tests['histogram']['details']
        info_text = f"Пики: {stats['peaks_count']} | Провалы: {stats['valleys_count']} | Периодичность: {stats['periodicity_score']:.2f}"
        ttk.Label(
            self.histogram_frame,
            text=info_text,
            font=("Segoe UI", 8),
            style="Secondary.TLabel"
        ).pack(pady=(5, 0))

    def create_noise_analysis(self, results: dict):
        """Создает график анализа шума"""
        # Удаляем предыдущий график
        for widget in self.noise_frame.winfo_children():
            widget.destroy()

        tests = results.get('tests', {})
        if 'noise_pattern' not in tests:
            label = ttk.Label(
                self.noise_frame,
                text="Нет данных для анализа шума",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        noise_data = tests['noise_pattern']['details']

        # Создаем фигуру
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Генерируем данные для визуализации нормального распределения
        x = np.linspace(-5, 5, 200)
        std_dev = noise_data.get('std_deviation', 1.0)
        y = np.exp(-0.5 * (x / std_dev) ** 2) / (std_dev * np.sqrt(2 * np.pi))

        # Рисуем график
        ax.plot(x, y, color=self.colors["accent"], linewidth=2.5, label=f'σ = {std_dev:.2f}')
        ax.fill_between(x, y, color=self.colors["accent"], alpha=0.3)

        # Добавляем вертикальные линии для стандартных отклонений
        for i in range(1, 4):
            ax.axvline(i * std_dev, color='red', linestyle='--', alpha=0.3, linewidth=1)
            ax.axvline(-i * std_dev, color='red', linestyle='--', alpha=0.3, linewidth=1)

        # Добавляем подписи осей
        ax.set_xlabel('Нормализованная амплитуда шума', color=self.colors["text"], fontsize=10)
        ax.set_ylabel('Плотность вероятности', color=self.colors["text"], fontsize=10)
        ax.set_title(f'Анализ шумового распределения (σ = {std_dev:.2f})',
                     color=self.colors["accent"], fontsize=12, fontweight='bold')

        # Добавляем сетку
        ax.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"])

        # Настройка цветов
        fig.patch.set_facecolor(self.colors["card"])
        ax.set_facecolor(self.colors["card"])
        ax.tick_params(colors=self.colors["text"], labelsize=9)

        # Добавляем легенду
        ax.legend(loc='upper right', fontsize=9)

        # Создаем canvas
        canvas = FigureCanvasTkAgg(fig, master=self.noise_frame)
        canvas.draw()

        # Сохраняем график для экспорта
        self.current_plots['noise'] = fig

        # Размещаем canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Добавляем подпись
        skewness = noise_data.get('skewness', 0.0)
        kurtosis_val = noise_data.get('kurtosis', 0.0)
        info_text = f"σ: {std_dev:.2f} | Асимметрия: {skewness:.2f} | Эксцесс: {kurtosis_val:.2f}"
        ttk.Label(
            self.noise_frame,
            text=info_text,
            font=("Segoe UI", 8),
            style="Secondary.TLabel"
        ).pack(pady=(5, 0))

    def create_lsb_statistics(self, results: dict):
        """Создает интерактивную круговую диаграмму и график распределения младших битов"""
        # Удаляем предыдущий график
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        tests = results.get('tests', {})
        if 'lsb_distribution' not in tests:
            label = ttk.Label(
                self.stats_frame,
                text="Нет данных для статистики младших битов",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        lsb_data = tests['lsb_distribution']['details']
        zeros = lsb_data.get('zeros_count', 0)
        ones = lsb_data.get('ones_count', 0)
        total = zeros + ones

        if total == 0:
            label = ttk.Label(
                self.stats_frame,
                text="Нет данных для статистики",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        # Создаем фигуру с двумя подграфиками
        fig = Figure(figsize=(8, 6), dpi=100)
        gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 1], hspace=0.3)

        # Верхний график: круговая диаграмма
        ax1 = fig.add_subplot(gs[0])
        labels = ['Нули (0)', 'Единицы (1)']
        sizes = [zeros, ones]
        colors_pie = ['#28a745', '#dc3545']  # Зеленый и красный для визуального контраста
        explode = (0.05, 0)  # Слегка выделяем сектор с нулями

        # Рисуем круговую диаграмму
        wedges, texts, autotexts = ax1.pie(
            sizes,
            labels=labels,
            colors=colors_pie,
            autopct=lambda pct: f'{pct:.1f}%\n({int(pct * total / 100)})',
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'color': 'white', 'fontsize': 11, 'weight': 'bold'}
        )

        # Добавляем заголовок
        balance = lsb_data.get('balance', 0.0)
        deviation = lsb_data.get('deviation', 0.0)
        ax1.set_title(f'Распределение младших битов\nБаланс: {balance:.3f} | Отклонение: {deviation:+.3f}',
                      color=self.colors["accent"], fontsize=12, fontweight='bold', pad=15)

        # Нижний график: гистограмма распределения по блокам (для изображений)
        ax2 = fig.add_subplot(gs[1])

        # Если есть данные о распределении по блокам (для изображений)
        if 'block_entropy' in tests and 'entropy_values' in tests['block_entropy']['details']:
            entropy_values = tests['block_entropy']['details']['entropy_values']
            # Анализируем распределение энтропии для оценки равномерности
            ax2.hist(entropy_values, bins=20, color=self.colors["accent"], alpha=0.7, edgecolor='white')
            ax2.set_xlabel('Энтропия блока', color=self.colors["text"], fontsize=9)
            ax2.set_ylabel('Количество блоков', color=self.colors["text"], fontsize=9)
            ax2.set_title('Распределение энтропии по блокам',
                          color=self.colors["accent"], fontsize=10, fontweight='bold')
            ax2.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"])
            ax2.tick_params(colors=self.colors["text"], labelsize=8)
        else:
            # Альтернативный график: сравнение с идеальным распределением
            x = np.array([0, 1])
            observed = np.array([zeros / total, ones / total])
            ideal = np.array([0.5, 0.5])

            width = 0.35
            ax2.bar(x - width / 2, observed, width, label='Фактическое',
                    color=self.colors["accent"], alpha=0.8)
            ax2.bar(x + width / 2, ideal, width, label='Идеальное 50/50',
                    color=self.colors["warning"], alpha=0.8)

            ax2.set_xlabel('Значение бита', color=self.colors["text"], fontsize=9)
            ax2.set_ylabel('Доля', color=self.colors["text"], fontsize=9)
            ax2.set_title('Сравнение с идеальным распределением 50/50',
                          color=self.colors["accent"], fontsize=10, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(['0', '1'])
            ax2.legend(loc='upper right', fontsize=8,
                       facecolor=self.colors["card"], edgecolor=self.colors["border"])
            ax2.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"], axis='y')
            ax2.tick_params(colors=self.colors["text"], labelsize=8)
            ax2.set_ylim(0, 1.0)

        # Настройка цветов фона
        fig.patch.set_facecolor(self.colors["card"])
        ax1.set_facecolor(self.colors["card"])
        ax2.set_facecolor(self.colors["card"])

        # Создаем canvas
        canvas = FigureCanvasTkAgg(fig, master=self.stats_frame)
        canvas.draw()

        # Сохраняем график для экспорта
        self.current_plots['lsb'] = fig

        # Размещаем canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Добавляем интерактивность: отображение статистики при наведении (ИСПРАВЛЕНО: безопасная проверка индексов)
        def on_hover(event):
            if event.inaxes == ax1:
                # Безопасная проверка наличия клика внутри сектора
                for idx, wedge in enumerate(wedges):
                    if wedge.contains_point((event.x, event.y)):
                        percentage = sizes[idx] / total * 100 if total > 0 else 0
                        ax1.set_title(f'Распределение младших битов\n{labels[idx]}: {sizes[idx]} ({percentage:.1f}%)',
                                      color=self.colors["accent"], fontsize=12, fontweight='bold', pad=15)
                        canvas.draw()
                        break

        canvas.mpl_connect('motion_notify_event', on_hover)

    def create_correlation_plot(self, results: dict):
        """Создает расширенный график корреляции пикселей с векторным представлением"""
        # Удаляем предыдущий график
        for widget in self.correlation_frame.winfo_children():
            widget.destroy()

        tests = results.get('tests', {})
        if 'pixel_correlation' not in tests:
            label = ttk.Label(
                self.correlation_frame,
                text="Нет данных для анализа корреляции",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        corr_data = tests['pixel_correlation']['details']

        # Создаем фигуру с двумя подграфиками
        fig = Figure(figsize=(8, 6), dpi=100)
        gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.3)

        # Левый график: столбчатая диаграмма корреляций
        ax1 = fig.add_subplot(gs[0])
        categories = ['Горизонтальная', 'Вертикальная', 'Диагональная', 'Средняя']
        values = [
            corr_data.get('horizontal_corr', 0.0),
            corr_data.get('vertical_corr', 0.0),
            corr_data.get('diagonal_corr', 0.0),
            corr_data.get('avg_corr', 0.0)
        ]

        # Определяем цвета в зависимости от значения корреляции
        colors_corr = []
        for v in values:
            if v > 0.8:
                colors_corr.append('#28a745')  # Зеленый - высокая корреляция
            elif v > 0.6:
                colors_corr.append('#ffc107')  # Желтый - средняя
            else:
                colors_corr.append('#dc3545')  # Красный - низкая

        # Рисуем столбчатую диаграмму
        bars = ax1.barh(categories, values, color=colors_corr, alpha=0.85, edgecolor='white', linewidth=1.5)

        # Добавляем вертикальные линии для порогов
        ax1.axvline(x=0.8, color='#28a745', linestyle='--', alpha=0.7, linewidth=2, label='Естественный порог (0.8)')
        ax1.axvline(x=0.6, color='#ffc107', linestyle='--', alpha=0.5, linewidth=1.5, label='Порог внимания (0.6)')

        # Добавляем числовые метки на столбцах
        for bar, value in zip(bars, values):
            width = bar.get_width()
            ax1.text(width + 0.02, bar.get_y() + bar.get_height() / 2,
                     f'{value:.3f}',
                     ha='left', va='center', fontsize=9, color=self.colors["text"], fontweight='bold')

        ax1.set_xlabel('Коэффициент корреляции', color=self.colors["text"], fontsize=10)
        ax1.set_title('Корреляция соседних пикселей',
                      color=self.colors["accent"], fontsize=12, fontweight='bold')
        ax1.set_xlim(-0.2, 1.05)
        ax1.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"], axis='x')
        ax1.tick_params(colors=self.colors["text"], labelsize=9)
        ax1.legend(loc='lower right', fontsize=8, facecolor=self.colors["card"], edgecolor=self.colors["border"])

        # Правый график: векторное представление корреляции
        ax2 = fig.add_subplot(gs[1])

        # Создаем векторное представление для визуализации направлений корреляции
        angles = [0, np.pi / 2, np.pi / 4]  # Горизонтальное, вертикальное, диагональное
        correlations = [
            abs(corr_data.get('horizontal_corr', 0.0)),
            abs(corr_data.get('vertical_corr', 0.0)),
            abs(corr_data.get('diagonal_corr', 0.0))
        ]

        # Нормализуем для визуализации
        max_corr = max(correlations) if correlations else 1.0
        correlations_norm = [c / max_corr if max_corr > 0 else 0 for c in correlations]

        # Рисуем векторы
        origin = np.array([[0, 0, 0], [0, 0, 0]])
        directions = np.array([
            [correlations_norm[0], 0, correlations_norm[2] * np.cos(np.pi / 4)],
            [0, correlations_norm[1], correlations_norm[2] * np.sin(np.pi / 4)]
        ])

        colors_vec = ['#17a2b8', '#6f42c1', '#fd7e14']
        labels_vec = ['Горизонтальная', 'Вертикальная', 'Диагональная']

        for i in range(3):
            ax2.arrow(0, 0, directions[0][i], directions[1][i],
                      head_width=0.05, head_length=0.05, fc=colors_vec[i], ec=colors_vec[i],
                      linewidth=2.5, alpha=0.9, length_includes_head=True)
            # Добавляем метку
            ax2.text(directions[0][i] * 1.15, directions[1][i] * 1.15,
                     f'{labels_vec[i]}\n({correlations[i]:.2f})',
                     fontsize=8, ha='center', va='center',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor=colors_vec[i], alpha=0.3))

        ax2.set_xlim(-0.2, 1.2)
        ax2.set_ylim(-0.2, 1.2)
        ax2.set_aspect('equal')
        ax2.grid(True, linestyle='--', alpha=0.3, color=self.colors["text_secondary"])
        ax2.set_xlabel('X направление', color=self.colors["text"], fontsize=9)
        ax2.set_ylabel('Y направление', color=self.colors["text"], fontsize=9)
        ax2.set_title('Векторная карта корреляции',
                      color=self.colors["accent"], fontsize=12, fontweight='bold')
        ax2.tick_params(colors=self.colors["text"], labelsize=8)

        # Добавляем круговые направляющие
        circle1 = plt.Circle((0, 0), 0.5, color='gray', fill=False, linestyle='--', alpha=0.3)
        circle2 = plt.Circle((0, 0), 1.0, color='gray', fill=False, linestyle='--', alpha=0.3)
        ax2.add_patch(circle1)
        ax2.add_patch(circle2)

        # Настройка цветов фона
        fig.patch.set_facecolor(self.colors["card"])
        ax1.set_facecolor(self.colors["card"])
        ax2.set_facecolor(self.colors["card"])

        # Создаем canvas
        canvas = FigureCanvasTkAgg(fig, master=self.correlation_frame)
        canvas.draw()

        # Сохраняем график для экспорта
        self.current_plots['correlation'] = fig

        # Размещаем canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_entropy_heatmap(self, results: dict):
        """Создает тепловую карту энтропии по блокам изображения"""
        # Удаляем предыдущий график
        for widget in self.entropy_frame.winfo_children():
            widget.destroy()

        tests = results.get('tests', {})
        if 'block_entropy' not in tests:
            label = ttk.Label(
                self.entropy_frame,
                text="Нет данных для тепловой карты энтропии",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        entropy_data = tests['block_entropy']['details']
        entropy_map = entropy_data.get('entropy_map', [])

        if not entropy_map or len(entropy_map) == 0:
            label = ttk.Label(
                self.entropy_frame,
                text="Недостаточно данных для построения тепловой карты",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            )
            label.pack(padx=20, pady=20)
            return

        # Конвертируем в numpy массив
        entropy_array = np.array(entropy_map)

        # Создаем фигуру
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Рисуем тепловую карту
        im = ax.imshow(entropy_array, cmap='viridis', aspect='auto', interpolation='nearest')

        # Добавляем цветовую шкалу
        cbar = fig.colorbar(im, ax=ax, pad=0.02)
        cbar.set_label('Энтропия блока', color=self.colors["text"], fontsize=10)
        cbar.ax.tick_params(colors=self.colors["text"], labelsize=9)

        # Добавляем заголовок с метриками
        mean_entropy = entropy_data.get('mean_entropy', 0.0)
        std_entropy = entropy_data.get('std_entropy', 0.0)
        block_count = entropy_data.get('block_count', 0)
        suspicion = entropy_data.get('suspicion_level', 0)

        ax.set_title(f'Тепловая карта энтропии по блокам ({block_count} блоков)\n'
                     f'Средняя энтропия: {mean_entropy:.2f} | Стандартное отклонение: {std_entropy:.2f}',
                     color=self.colors["accent"], fontsize=12, fontweight='bold', pad=15)

        # Настройка осей
        ax.set_xlabel('Блоки по X', color=self.colors["text"], fontsize=10)
        ax.set_ylabel('Блоки по Y', color=self.colors["text"], fontsize=10)
        ax.tick_params(colors=self.colors["text"], labelsize=9)

        # Добавляем сетку для визуального разделения блоков
        ax.grid(False)  # Отключаем стандартную сетку
        # Рисуем линии между блоками
        for i in range(1, entropy_array.shape[0]):
            ax.axhline(i - 0.5, color='white', linestyle='-', linewidth=0.5, alpha=0.3)
        for j in range(1, entropy_array.shape[1]):
            ax.axvline(j - 0.5, color='white', linestyle='-', linewidth=0.5, alpha=0.3)

        # Настройка цветов фона
        fig.patch.set_facecolor(self.colors["card"])
        ax.set_facecolor(self.colors["card"])

        # Создаем canvas
        canvas = FigureCanvasTkAgg(fig, master=self.entropy_frame)
        canvas.draw()

        # Сохраняем график для экспорта
        self.current_plots['entropy_heatmap'] = fig

        # Размещаем canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Добавляем подпись с интерпретацией
        interpretation = entropy_data.get('interpretation', 'N/A')
        info_text = f"Интерпретация: {interpretation} | Уровень подозрительности: {suspicion}%"
        ttk.Label(
            self.entropy_frame,
            text=info_text,
            font=("Segoe UI", 8),
            style="Secondary.TLabel"
        ).pack(pady=(5, 0))

    def filter_tests(self, event=None):
        """Фильтрует отображение тестов в таблице по уровню подозрительности"""
        filter_value = self.filter_var.get()

        # Сначала показываем все элементы
        for item in self.tests_tree.get_children():
            self.tests_tree.detach(item)

        # Затем добавляем только подходящие по фильтру
        for item_info in self.test_items:
            item = item_info['item']
            suspicion = item_info['suspicion']

            if filter_value == "Все тесты":
                self.tests_tree.reattach(item, '', 'end')
            elif filter_value == "Высокий риск (>70%)" and suspicion > 70:
                self.tests_tree.reattach(item, '', 'end')
            elif filter_value == "Средний риск (40-70%)" and 40 <= suspicion <= 70:
                self.tests_tree.reattach(item, '', 'end')
            elif filter_value == "Низкий риск (<40%)" and suspicion < 40:
                self.tests_tree.reattach(item, '', 'end')

    def refresh_tests_view(self):
        """Обновляет отображение таблицы тестов"""
        self.filter_tests()

    def sort_column(self, col, reverse):
        """Сортирует таблицу по указанному столбцу"""
        data = [(self.tests_tree.set(child, col), child) for child in self.tests_tree.get_children('')]

        # Специальная обработка для числовых столбцов
        if col == "Подозрительность":
            data.sort(key=lambda x: (int(x[0].replace('%', '')) if x[0].replace('%', '').isdigit() else 0, x[1]),
                      reverse=reverse)
        elif col == "Значение":
            data.sort(key=lambda x: (float(x[0]) if self._is_float(x[0]) else 0, x[1]), reverse=reverse)
        else:
            data.sort(key=lambda x: x[0].lower(), reverse=reverse)

        # Перераспределяем элементы
        for index, (val, child) in enumerate(data):
            self.tests_tree.move(child, '', index)

        # Меняем направление сортировки при следующем клике
        self.tests_tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def _is_float(self, value):
        """Проверяет, является ли строка числом с плавающей точкой"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def export_report(self, format_type: str):
        """Экспортирует отчет в выбранном формате"""
        if not self.analysis_results:
            messagebox.showwarning("⚠️ Предупреждение", "Нет результатов для экспорта")
            return

        # Определяем имя файла по умолчанию
        base_name = os.path.splitext(os.path.basename(self.file_path.get()))[0]
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        if format_type == "all":
            # Экспорт во все форматы
            success_count = 0
            formats = [("html", "HTML отчет"), ("csv", "CSV таблица"), ("txt", "TXT отчет")]

            for fmt, desc in formats:
                try:
                    if self._export_single_format(fmt, base_name, timestamp):
                        success_count += 1
                except Exception as e:
                    self.app.log_manager.add_entry("export_analysis", "error",
                                                   {"format": fmt, "error": str(e)})

            if success_count == len(formats):
                messagebox.showinfo("✅ Успех", f"Отчеты успешно экспортированы во все {success_count} формата")
            else:
                messagebox.showwarning("⚠️ Частичный успех",
                                       f"Экспортировано {success_count} из {len(formats)} форматов")

            return

        # Экспорт в один формат
        try:
            if self._export_single_format(format_type, base_name, timestamp):
                messagebox.showinfo("✅ Успех", f"Отчет успешно экспортирован в формате {format_type.upper()}")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", f"Не удалось экспортировать отчет:\n{str(e)}")
            self.app.log_manager.add_entry("export_analysis", "error",
                                           {"format": format_type, "error": str(e)})

    def _export_single_format(self, format_type: str, base_name: str, timestamp: str) -> bool:
        """Экспортирует отчет в один формат"""
        # Определяем расширение и фильтры
        extensions = {
            "html": ("html", "HTML файлы (*.html)"),
            "csv": ("csv", "CSV файлы (*.csv)"),
            "txt": ("txt", "Текстовые файлы (*.txt)")
        }

        if format_type not in extensions:
            raise ValueError(f"Неподдерживаемый формат: {format_type}")

        ext, file_desc = extensions[format_type]
        default_filename = f"stego_analysis_{base_name}_{timestamp}.{ext}"

        # Диалог сохранения файла
        file_path = filedialog.asksaveasfilename(
            title=f"Сохранить отчет как {format_type.upper()}",
            defaultextension=f".{ext}",
            filetypes=[(file_desc, f"*.{ext}"), ("Все файлы", "*.*")],
            initialdir=self.app.last_save_dir,
            initialfile=default_filename
        )

        if not file_path:
            return False

        # Выполняем экспорт в зависимости от формата
        success = False
        if format_type == "html":
            success = FileAnalyzer.export_report_html(self.analysis_results, file_path, self.file_path.get())
        elif format_type == "csv":
            success = FileAnalyzer.export_report_csv(self.analysis_results, file_path)
        elif format_type == "txt":
            success = FileAnalyzer.export_report_txt(self.analysis_results, file_path, self.file_path.get())

        if success:
            self.app.last_save_dir = os.path.dirname(file_path)
            self.app.log_manager.add_entry(
                "export_analysis",
                "success",
                {
                    "format": format_type,
                    "file": file_path,
                    "original_file": self.file_path.get(),
                    "suspicion_level": self.analysis_results.get('overall_suspicion', 0),
                    "tests_count": len(self.analysis_results.get('tests', {}))
                }
            )
            # Автоматически открываем HTML отчет в браузере
            if format_type == "html":
                webbrowser.open(f"file://{os.path.abspath(file_path)}")

        return success

    def save_current_plot(self):
        """Сохраняет текущий активный график в изображение"""
        # Определяем текущую активную вкладку визуализации
        try:
            current_tab = self.visualization_notebook.index(self.visualization_notebook.select())
        except tk.TclError:
            messagebox.showwarning("⚠️ Предупреждение", "Нет активной вкладки визуализации")
            return

        tab_names = ['histogram', 'noise', 'lsb', 'correlation', 'entropy_heatmap']

        if current_tab >= len(tab_names):
            messagebox.showwarning("⚠️ Предупреждение", "Нет активного графика для сохранения")
            return

        plot_key = tab_names[current_tab]
        if plot_key not in self.current_plots:
            messagebox.showwarning("⚠️ Предупреждение", "График не готов для сохранения")
            return

        # Диалог сохранения
        base_name = os.path.splitext(os.path.basename(self.file_path.get()))[0]
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        default_filename = f"plot_{plot_key}_{base_name}_{timestamp}.png"

        file_path = filedialog.asksaveasfilename(
            title="Сохранить график как изображение",
            defaultextension=".png",
            filetypes=[
                ("PNG изображения", "*.png"),
                ("SVG вектор", "*.svg"),
                ("PDF документ", "*.pdf"),
                ("Все форматы", "*.*")
            ],
            initialdir=self.app.last_save_dir,
            initialfile=default_filename
        )

        if not file_path:
            return

        try:
            # Сохраняем график
            fig = self.current_plots[plot_key]
            fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())

            self.app.last_save_dir = os.path.dirname(file_path)
            messagebox.showinfo("✅ Успех", f"График успешно сохранен:\n{file_path}")

            self.app.log_manager.add_entry(
                "export_plot",
                "success",
                {
                    "plot_type": plot_key,
                    "file": file_path,
                    "format": os.path.splitext(file_path)[1][1:]
                }
            )
        except Exception as e:
            messagebox.showerror("❌ Ошибка", f"Не удалось сохранить график:\n{str(e)}")
            self.app.log_manager.add_entry("export_plot", "error", {"error": str(e)})

    def export_button_state(self, enabled: bool):
        """Управляет состоянием кнопок экспорта (ИСПРАВЛЕНО: проверка существования export_frame)"""
        # Проверяем существование экспортируемого фрейма
        if not hasattr(self, 'export_frame') or self.export_frame is None:
            return

        state = "normal" if enabled else "disabled"
        for child in self.export_frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for btn in child.winfo_children():
                    if isinstance(btn, ttk.Button):
                        btn.config(state=state)
            elif isinstance(child, ttk.Button):
                btn.config(state=state)

    def clear_results(self):
        """Полностью очищает все результаты анализа"""
        # Очищаем метаданные
        self.metadata_text.config(state='normal')
        self.metadata_text.delete("1.0", tk.END)
        self.metadata_text.config(state='disabled')

        # Сбрасываем индикатор подозрительности
        self.suspicion_label.config(text="-")
        self.suspicion_bar.config(value=0, style="TProgressbar")
        self.suspicion_text.config(text="Нет данных", foreground=self.colors["text_secondary"])
        self.confidence_label.config(text="Уверенность: -")

        # Очищаем таблицу тестов
        for item in self.tests_tree.get_children():
            self.tests_tree.delete(item)
        self.test_items = []

        # Очищаем рекомендации
        self.recommendations_text.config(state='normal')
        self.recommendations_text.delete("1.0", tk.END)
        self.recommendations_text.config(state='disabled')

        # Очищаем все визуализации
        for widget in self.histogram_frame.winfo_children():
            widget.destroy()
        for widget in self.noise_frame.winfo_children():
            widget.destroy()
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        for widget in self.correlation_frame.winfo_children():
            widget.destroy()
        for widget in self.entropy_frame.winfo_children():
            widget.destroy()

        # Очищаем хранилище графиков
        self.current_plots = {}

        # Сбрасываем результаты
        self.analysis_results = None

        # Обновляем статус
        self.status_label.config(text="✅ Готов к анализу")

        # Отключаем кнопки экспорта (ИСПРАВЛЕНО: безопасный вызов)
        if hasattr(self, 'export_frame') and self.export_frame is not None:
            self.export_button_state(False)

    def restore_buttons(self):
        """Восстанавливает состояние кнопок после завершения анализа"""
        self.analyze_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.progress_var.set(100)

    def cancel_analysis(self):
        """Отменяет текущий анализ"""
        if self.analysis_thread and self.analysis_thread.is_alive():
            self.cancel_event.set()
            self.status_label.config(text="⏳ Отмена анализа...")
            self.cancel_button.config(state="disabled")
            self.analyze_button.config(state="disabled")

    def display_error(self, message: str):
        """Отображает сообщение об ошибке с логированием"""
        messagebox.showerror("❌ Ошибка анализа", message)
        self.status_label.config(text=f"❌ Ошибка: {message[:50]}...")
        self.app.log_manager.add_entry("analysis_error", "error", {"message": message})

    def __del__(self):
        """Очистка ресурсов при удалении вкладки"""
        # Прерываем анализ при закрытии вкладки
        if hasattr(self, 'cancel_event') and self.cancel_event:
            self.cancel_event.set()
        # Очищаем графики
        if hasattr(self, 'current_plots'):
            self.current_plots.clear()


# ───────────────────────────────────────────────
# 🎨КЛАСС ПРОВЕРКИ ПАРОЛЯ
# ───────────────────────────────────────────────
PASSWORD_FILE = "password_pro.json"


def hash_password(password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # количество итераций
    )
    return base64.b64encode(salt).decode('utf-8'), base64.b64encode(pwd_hash).decode('utf-8')


def save_password(salt_b64, pwd_hash_b64):
    with open(PASSWORD_FILE, "w") as f:
        json.dump({"salt": salt_b64, "hash": pwd_hash_b64}, f)


def load_password():
    if not os.path.exists(PASSWORD_FILE):
        return None
    with open(PASSWORD_FILE, "r") as f:
        data = json.load(f)
    return data["salt"], data["hash"]


class ModernPasswordDialog:
    """
    Современное окно ввода пароля с Material Design интерфейсом
    Особенности:
    - Кнопка показа/скрытия пароля
    - Эффекты наведения и анимации
    - Индикатор загрузки
    - Адаптация к теме приложения
    - Центрирование на экране
    """

    def __init__(self, root, theme_colors):
        self.root = root
        self.colors = theme_colors
        self.password_correct = False
        # Создаем модальное окно
        self.dialog = tk.Toplevel(root)
        self.dialog.title("🔐 Аутентификация")
        self.dialog.geometry("420x380")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=self.colors["bg"])
        # Центрирование окна
        self.center_window()
        # Установка протокола закрытия
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        # Переменные (ИНИЦИАЛИЗИРУЕМ ДО ВЫЗОВА setup_ui)
        self.password_var = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)
        # Создание интерфейса
        self.setup_ui()
        # Связывание событий
        self.bind_events()
        # Модальность
        self.dialog.transient(root)
        self.dialog.grab_set()
        self.dialog.focus_set()
        # Ожидание закрытия окна
        root.wait_window(self.dialog)

    def center_window(self):
        """Центрирует окно на экране"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (420 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (380 // 2)
        self.dialog.geometry(f"420x380+{x}+{y}")

    def setup_ui(self):
        """Создает современный пользовательский интерфейс"""
        # Основной контейнер с отступами
        main_frame = tk.Frame(
            self.dialog,
            bg=self.colors["bg"],
            padx=30,
            pady=25
        )
        main_frame.pack(fill="both", expand=True)

        # Заголовок с иконкой
        header_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 25))

        # Иконка безопасности
        icon_label = tk.Label(
            header_frame,
            text="🛡️",
            font=("Segoe UI", 28),
            bg=self.colors["bg"],
            fg=self.colors["accent"]
        )
        icon_label.pack(pady=(0, 12))

        # Заголовок
        title_label = tk.Label(
            header_frame,
            text="ØccultoNG Pro • Безопасный вход",
            font=("Segoe UI", 17, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        title_label.pack()

        # Подзаголовок
        subtitle_label = tk.Label(
            header_frame,
            text="Введите пароль для доступа к профессиональному стеганографическому инструменту",
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text_secondary"],
            wraplength=360,
            justify="center"
        )
        subtitle_label.pack(pady=(6, 0))

        # Контейнер для поля ввода пароля
        password_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        password_frame.pack(fill="x", pady=(0, 20))

        # Лейбл для поля пароля
        password_label = tk.Label(
            password_frame,
            text="🔒 Пароль:",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        password_label.pack(anchor="w", pady=(0, 8))

        # Контейнер для поля ввода и кнопки показа пароля
        self.input_container = tk.Frame(
            password_frame,
            bg=self.colors["card"],
            relief="flat",
            bd=2,
            highlightbackground=self.colors["border"],
            highlightthickness=2
        )
        self.input_container.pack(fill="x", pady=(0, 5))

        # Поле ввода пароля
        self.password_entry = tk.Entry(
            self.input_container,
            textvariable=self.password_var,
            font=("Segoe UI", 13),
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            selectbackground=self.colors["accent"],
            selectforeground="white",
            relief="flat",
            bd=0,
            show="●"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=15, pady=15)

        # Кнопка показа/скрытия пароля
        self.toggle_button = tk.Button(
            self.input_container,
            text="👁️",
            font=("Segoe UI", 14),
            bg=self.colors["card"],
            fg=self.colors["text_secondary"],
            activebackground=self.colors["highlight"],
            activeforeground=self.colors["text"],
            relief="flat",
            bd=0,
            cursor="hand2",
            width=3,
            command=self.toggle_password_visibility
        )
        self.toggle_button.pack(side="right", padx=(0, 10))

        # Дополнительная информация
        info_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        info_frame.pack(fill="x", pady=(0, 20))

        info_label = tk.Label(
            info_frame,
            text="ℹ️ Первый запуск: пароль будет установлен как основной 🔒 Последующие запуски: введите установленный пароль",
            font=("Segoe UI", 9),
            bg=self.colors["bg"],
            fg=self.colors["text_secondary"],
            justify="left",
            wraplength=360
        )
        info_label.pack(anchor="w")

        # Контейнер для сообщений об ошибках
        self.error_frame = tk.Frame(password_frame, bg=self.colors["bg"])
        self.error_frame.pack(fill="x", pady=(5, 0))
        self.error_label = tk.Label(
            self.error_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.colors["bg"],
            fg=self.colors["error"],
            wraplength=360,
            justify="left"
        )
        self.error_label.pack(anchor="w")

        # Контейнер для кнопок
        button_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        button_frame.pack(fill="x", pady=(15, 0))

        # Кнопка отмены
        self.cancel_button = tk.Button(
            button_frame,
            text="❌ Отмена",
            font=("Segoe UI", 11),
            bg=self.colors["secondary"],
            fg=self.colors["text"],
            activebackground=self.colors["highlight"],
            activeforeground=self.colors["text"],
            relief="flat",
            bd=0,
            padx=22,
            pady=12,
            cursor="hand2",
            command=self.on_close
        )
        self.cancel_button.pack(side="left")

        # Кнопка входа
        self.login_button = tk.Button(
            button_frame,
            text="🔓 Войти",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["accent"],
            fg="white",
            activebackground=self.colors["accent_hover"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=28,
            pady=12,
            cursor="hand2",
            command=self.check_password
        )
        self.login_button.pack(side="right")

        # Добавляем эффекты наведения для кнопок
        self.add_hover_effects()

    def add_hover_effects(self):
        """Добавляет эффекты наведения для кнопок и полей ввода"""

        # Эффекты для кнопки входа
        def on_login_enter(e):
            self.login_button.config(bg=self.colors["accent_hover"])

        def on_login_leave(e):
            self.login_button.config(bg=self.colors["accent"])

        self.login_button.bind("<Enter>", on_login_enter)
        self.login_button.bind("<Leave>", on_login_leave)

        # Эффекты для кнопки отмены
        def on_cancel_enter(e):
            self.cancel_button.config(bg=self.colors["highlight"])

        def on_cancel_leave(e):
            self.cancel_button.config(bg=self.colors["secondary"])

        self.cancel_button.bind("<Enter>", on_cancel_enter)
        self.cancel_button.bind("<Leave>", on_cancel_leave)

        # Эффекты для кнопки показа пароля
        def on_toggle_enter(e):
            self.toggle_button.config(bg=self.colors["highlight"])

        def on_toggle_leave(e):
            self.toggle_button.config(bg=self.colors["card"])

        self.toggle_button.bind("<Enter>", on_toggle_enter)
        self.toggle_button.bind("<Leave>", on_toggle_leave)

        # Эффекты фокуса для поля ввода
        def on_entry_focus_in(e):
            self.input_container.config(highlightbackground=self.colors["accent"])

        def on_entry_focus_out(e):
            self.input_container.config(highlightbackground=self.colors["border"])

        self.password_entry.bind("<FocusIn>", on_entry_focus_in)
        self.password_entry.bind("<FocusOut>", on_entry_focus_out)

    def bind_events(self):
        """Связывает события клавиатуры"""
        self.dialog.bind("<Return>", lambda e: self.check_password())
        self.dialog.bind("<Escape>", lambda e: self.on_close())
        # Фокус на поле ввода
        self.dialog.after(150, self.password_entry.focus_set)

    def toggle_password_visibility(self):
        """Переключает видимость пароля"""
        if self.show_password.get():
            self.password_entry.config(show="")
            self.toggle_button.config(text="🙈")
            self.show_password.set(False)
        else:
            self.password_entry.config(show="●")
            self.toggle_button.config(text="👁️")
            self.show_password.set(True)

    def show_error(self, message):
        """Показывает сообщение об ошибке с анимацией"""
        self.error_label.config(text=message)
        # Анимация встряхивания окна
        self.shake_window()
        # Подсветка поля ввода красным
        original_color = self.input_container.cget("highlightbackground")
        self.input_container.config(highlightbackground=self.colors["error"])
        # Возврат к исходному цвету через 1.5 секунды
        self.dialog.after(1500, lambda: self.input_container.config(highlightbackground=original_color))

    def shake_window(self):
        """Анимация встряхивания окна"""
        original_x = self.dialog.winfo_x()

        def shake_step(step, direction):
            if step > 0:
                offset = 6 * direction
                self.dialog.geometry(f"+{original_x + offset}+{self.dialog.winfo_y()}")
                self.dialog.after(60, lambda: shake_step(step - 1, -direction))
            else:
                self.dialog.geometry(f"+{original_x}+{self.dialog.winfo_y()}")

        shake_step(5, 1)

    def clear_error(self):
        """Очищает сообщение об ошибке"""
        self.error_label.config(text="")

    def check_password(self):
        """Проверяет введенный пароль"""
        entered = self.password_var.get().strip()
        if not entered:
            self.show_error("⚠️ Пожалуйста, введите пароль")
            return
        if len(entered) < 3:
            self.show_error("⚠️ Пароль должен содержать минимум 3 символа")
            return
        self.clear_error()
        # Показываем индикатор загрузки
        self.show_loading()
        # Имитируем небольшую задержку для проверки пароля (для плавности UX)
        self.dialog.after(350, lambda: self.verify_password(entered))

    def show_loading(self):
        """Показывает индикатор загрузки"""
        self.login_button.config(
            text="⏳ Проверка...",
            state="disabled"
        )
        self.password_entry.config(state="disabled")
        self.toggle_button.config(state="disabled")

    def hide_loading(self):
        """Скрывает индикатор загрузки"""
        self.login_button.config(
            text="🔓 Войти",
            state="normal"
        )
        self.password_entry.config(state="normal")
        self.toggle_button.config(state="normal")

    def verify_password(self, entered):
        """Проверяет пароль"""
        try:
            stored = load_password()
            if stored is None:
                # Первый запуск - сохраняем пароль
                salt_b64, pwd_hash_b64 = hash_password(entered)
                save_password(salt_b64, pwd_hash_b64)
                self.password_correct = True
                self.show_success("✅ Пароль установлен успешно!")
                self.dialog.after(1200, self.dialog.destroy)
            else:
                # Проверяем существующий пароль
                salt_b64, pwd_hash_b64 = stored
                salt = base64.b64decode(salt_b64)
                _, entered_hash_b64 = hash_password(entered, salt)
                if entered_hash_b64 == pwd_hash_b64:
                    self.password_correct = True
                    self.show_success("✅ Добро пожаловать в ØccultoNG Pro!")
                    self.dialog.after(900, self.dialog.destroy)
                else:
                    self.hide_loading()
                    self.show_error("❌ Неверный пароль. Попробуйте еще раз.")
                    self.password_var.set("")
                    self.dialog.after(100, self.password_entry.focus_set)
        except Exception as e:
            self.hide_loading()
            self.show_error(f"❌ Ошибка: {str(e)}")

    def show_success(self, message):
        """Показывает сообщение об успехе"""
        self.error_label.config(text=message, fg=self.colors["success"])

    def on_close(self):
        """Обработчик закрытия окна"""
        self.password_correct = False
        self.dialog.destroy()


# ───────────────────────────────────────────────
# 🎯 ГЛОБАЛЬНЫЕ КОНСТАНТЫ ДЛЯ ЗАГОЛОВКОВ
# ───────────────────────────────────────────────
MAGIC_BYTES = b'ONG'  # OccultoNG
HEADER_MAGIC_LEN = len(MAGIC_BYTES)
HEADER_CHECKSUM_LEN = 4  # CRC32
HEADER_DATALEN_LEN = 4  # Длина данных
HEADER_FULL_LEN = HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN + HEADER_DATALEN_LEN


# Функция-помощник для генерации RNG
def _generate_rng(password: str, method: str) -> np.random.Generator:
    """Генерирует отдельный rng для каждого метода."""
    seed_str = f"{password}{method}".encode()
    key = hashlib.sha256(seed_str).digest()
    return np.random.default_rng(np.frombuffer(key, dtype=np.uint64))


# ───────────────────────────────────────────────
# 🧠 КЛАСС СТЕГО-МЕТОДОВ
# ───────────────────────────────────────────────
class AdvancedStego:
    # ---------- Вспомогательные методы для работы с данными и заголовками ----------
    @staticmethod
    def _pack_data_with_header(data: bytes) -> bytes:
        checksum = zlib.crc32(data).to_bytes(HEADER_CHECKSUM_LEN, 'big')
        data_len = len(data).to_bytes(HEADER_DATALEN_LEN, 'big')
        return MAGIC_BYTES + checksum + data_len + data

    @staticmethod
    def _unpack_data_with_header(full_bytes: bytes) -> bytes:
        if len(full_bytes) < HEADER_FULL_LEN:
            raise ValueError("Недостаточно данных для заголовка.")
        magic = full_bytes[:HEADER_MAGIC_LEN]
        if magic != MAGIC_BYTES:
            raise ValueError("Неверные магические байты. Данные не найдены или повреждены.")
        header_end = HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN + HEADER_DATALEN_LEN
        stored_checksum = int.from_bytes(full_bytes[HEADER_MAGIC_LEN:HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN], 'big')
        data_len = int.from_bytes(full_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:header_end], 'big')
        data_start, data_end = header_end, header_end + data_len
        if len(full_bytes) < data_end:
            raise ValueError("Данные обрезаны, фактическая длина меньше заявленной в заголовке.")
        data = full_bytes[data_start:data_end]
        calculated_checksum = zlib.crc32(data)
        if calculated_checksum != stored_checksum:
            raise ValueError("Ошибка контрольной суммы. Данные повреждены.")
        return data

    @staticmethod
    def _embed_with_parity(pixel_value: int, bit_to_embed: int) -> int:
        if (pixel_value % 2) != bit_to_embed:
            return pixel_value - 1 if pixel_value % 2 != 0 and pixel_value > 0 else pixel_value + 1
        return pixel_value

    @staticmethod
    @numba.jit(nopython=True)
    def _embed_bits_numba(pixels_flat, indices, bits):
        """
        Компилируемая Numba-функция для быстрой вставки битов.
        Заменяет медленный Python-цикл.
        """
        for i in range(len(indices)):
            idx = indices[i]
            bit_to_embed = bits[i]
            pixel_val = pixels_flat[idx]
            # Логика _embed_with_parity
            if (pixel_val % 2) != bit_to_embed:
                if pixel_val > 0 and (pixel_val % 2) != 0:
                    pixels_flat[idx] -= 1
                elif pixel_val < 255:
                    pixels_flat[idx] += 1
                else:  # Если pixel_val == 255
                    pixels_flat[idx] -= 1
        return pixels_flat

    # Numba-функция для AELSB
    @staticmethod
    @numba.jit(nopython=True)
    def _embed_bits_aelsb_numba(pixels_flat_rgb, pixel_indices, channel_indices, data_bits):
        """
        Компилируемая Numba-функция для быстрой вставки битов в AELSB.
        """
        for i in range(len(pixel_indices)):
            pixel_idx = pixel_indices[i]
            channel = channel_indices[i]
            bit = data_bits[i]
            pixel_val = pixels_flat_rgb[pixel_idx, channel]
            if (pixel_val % 2) != bit:
                if pixel_val > 0 and (pixel_val % 2) != 0:
                    pixels_flat_rgb[pixel_idx, channel] -= 1
                elif pixel_val < 255:
                    pixels_flat_rgb[pixel_idx, channel] += 1
                else:
                    pixels_flat_rgb[pixel_idx, channel] -= 1

    # ---------- LSB (Максимальная вместимость) ----------
    @staticmethod
    def hide_lsb(container_path: str, data: bytes, password: str, output_path: str,
                 progress_callback=None, cancel_event=None):
        try:
            with Image.open(container_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                height, width, _ = pixels.shape
                full_data = AdvancedStego._pack_data_with_header(data)
                total_bits_needed = len(full_data) * 8
                available_bits = height * width * 3
                if total_bits_needed > available_bits:
                    raise ValueError(f"Данные слишком велики для изображения. Максимум: {available_bits // 8} байт")
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))
                pixels_flat = pixels.reshape(-1)
                pixels_flat[:total_bits_needed] = (pixels_flat[:total_bits_needed] & 0xFE) | data_bits
                for i in range(0, total_bits_needed, 1000):
                    if progress_callback:
                        progress_callback((i / total_bits_needed) * 100)
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Операция отменена пользователем")
                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)
                if progress_callback: progress_callback(100.0)
        except Exception as e:
            raise e

    @staticmethod
    def extract_lsb(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img)
                pixels_flat = pixels.reshape(-1)
                header_bits_needed = HEADER_FULL_LEN * 8
                if pixels_flat.size < header_bits_needed:
                    raise ValueError("Недостаточно данных для заголовка.")
                header_bits = (pixels_flat[:header_bits_needed] & 1)
                header_bytes = np.packbits(header_bits).tobytes()
                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных в заголовке.")
                total_bits_to_extract = (HEADER_FULL_LEN + data_len) * 8
                if pixels_flat.size < total_bits_to_extract:
                    raise ValueError("Недостаточно данных для извлечения полного сообщения.")
                all_bits = (pixels_flat[:total_bits_to_extract] & 1)
                full_bytes = np.packbits(all_bits).tobytes()
                if progress_callback: progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    # ---------- Adaptive-Noise ----------
    @staticmethod
    def hide_noise(container_path: str, data: bytes, password: str, output_path: str,
                   progress_callback=None, cancel_event=None):
        try:
            rng = _generate_rng(password, "noise")
            with Image.open(container_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                full_data = AdvancedStego._pack_data_with_header(data)
                total_bits_needed = len(full_data) * 8
                if total_bits_needed > pixels.size:
                    raise ValueError("Данные слишком велики для этого изображения.")
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))
                indices = np.arange(pixels.size)
                rng.shuffle(indices)
                selected_indices = indices[:total_bits_needed]
                pixels_flat = pixels.reshape(-1)
                # *** ОПТИМИЗАЦИЯ: Вызов Numba-функции вместо цикла ***
                AdvancedStego._embed_bits_numba(pixels_flat, selected_indices, data_bits)
                # Обновление прогресса можно оставить, т.к. основная работа сделана
                if progress_callback: progress_callback(100.0)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                result_img = Image.fromarray(pixels)
                # Для скорости можно использовать compress_level=1
                result_img.save(output_path, format='PNG', compress_level=1)
        except Exception as e:
            raise e

    @staticmethod
    def extract_noise(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            rng = _generate_rng(password, "noise")
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                pixels = np.array(img)
                indices = np.arange(pixels.size)
                rng.shuffle(indices)
                pixels_flat = pixels.reshape(-1)
                header_bits_needed = HEADER_FULL_LEN * 8
                header_indices = indices[:header_bits_needed]
                # *** ОПТИМИЗАЦИЯ: Векторизованное извлечение ***
                header_bits = (pixels_flat[header_indices] & 1)
                header_bytes = np.packbits(header_bits).tobytes()
                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")
                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                all_indices = indices[:total_bits_needed]
                # *** ОПТИМИЗАЦИЯ: Векторизованное извлечение ***
                extracted_bits = (pixels_flat[all_indices] & 1)
                full_bytes = np.packbits(extracted_bits).tobytes()
                if progress_callback: progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    # ---------- AELSB++ (Content-Adaptive + Hamming(7,3) + LSB matching) ----------
    @staticmethod
    def _hill_cost_map(img: Image.Image) -> np.ndarray:
        """
        HILL-подобная карта 'стоимости' изменений.
        Чем меньше cost, тем лучше место для скрытия.
        Строим на 'санированном' изображении (LSB обнулены) для детерминизма.
        """
        # Санируем LSB, чтобы и при скрытии, и при извлечении
        # карта стоимости была абсолютно одинаковой.
        rgb = np.array(img, dtype=np.uint8)
        # Отбрасываем LSB с помощью побитового AND с 0xFE (...11111110)
        sanitized = (rgb & 0xFE).astype(np.uint8)
        gray = Image.fromarray(sanitized).convert('L')
        g = np.array(gray, dtype=np.float32)
        # Высокочастотный фильтр (по мотивам HILL)
        hp = np.array([[-1, 2, -1],
                       [2, -4, 2],
                       [-1, 2, -1]], dtype=np.float32)
        res = ndimage.convolve(g, hp, mode='reflect')
        mag = np.abs(res)
        # Небольшое сглаживание, чтобы получить устойчивую карту
        smooth = ndimage.uniform_filter(mag, size=5, mode='reflect')
        # Чем выше текстурность, тем меньше стоимость (и наоборот)
        cost = 1.0 / (smooth + 1.0)
        return cost  # нормализация не обязательна, важен относительный порядок

    @staticmethod
    def _prepare_calsb_indices(pixels: np.ndarray, base_cost: np.ndarray,
                               rng: np.random.Generator, needed_elements: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Новая версия: порядок зависит только от RNG.
        Это гарантирует идентичный порядок на скрытии и извлечении.
        """
        # Берём только первые 3 канала на всякий случай
        if pixels.ndim != 3 or pixels.shape[2] < 3:
            raise ValueError("Ожидается изображение RGB.")
        h, w, _ = pixels.shape
        total = h * w * 3
        if needed_elements > total:
            raise ValueError("Недостаточно позиций для встраивания.")
        indices = np.arange(total, dtype=np.int64)
        rng.shuffle(indices)
        chosen = indices[:needed_elements]
        pixel_idx = (chosen // 3).astype(np.int64)
        channel_idx = (chosen % 3).astype(np.int64)
        return pixel_idx, channel_idx

    @staticmethod
    @numba.jit(nopython=True)
    def _embed_hamming73_numba(pixels_flat_rgb, pixel_indices, channel_indices, bits, groups):
        bits_len = bits.shape[0]
        for g in range(groups):
            base = g * 7
            v0 = pixels_flat_rgb[pixel_indices[base + 0], channel_indices[base + 0]] & 1
            v1 = pixels_flat_rgb[pixel_indices[base + 1], channel_indices[base + 1]] & 1
            v2 = pixels_flat_rgb[pixel_indices[base + 2], channel_indices[base + 2]] & 1
            v3 = pixels_flat_rgb[pixel_indices[base + 3], channel_indices[base + 3]] & 1
            v4 = pixels_flat_rgb[pixel_indices[base + 4], channel_indices[base + 4]] & 1
            v5 = pixels_flat_rgb[pixel_indices[base + 5], channel_indices[base + 5]] & 1
            v6 = pixels_flat_rgb[pixel_indices[base + 6], channel_indices[base + 6]] & 1
            s0 = (v0 + v2 + v4 + v6) & 1
            s1 = (v1 + v2 + v5 + v6) & 1
            s2 = (v3 + v4 + v5 + v6) & 1
            b0_idx = g * 3
            m0 = bits[b0_idx] if b0_idx < bits_len else 0
            b1_idx = b0_idx + 1
            m1 = bits[b1_idx] if b1_idx < bits_len else 0
            b2_idx = b1_idx + 1
            m2 = bits[b2_idx] if b2_idx < bits_len else 0
            ds0 = s0 ^ m0
            ds1 = s1 ^ m1
            ds2 = s2 ^ m2
            syn = ds0 + (ds1 << 1) + (ds2 << 2)  # 0..7
            if syn != 0:
                j = syn - 1
                idx_p = pixel_indices[base + j]
                idx_c = channel_indices[base + j]
                val = pixels_flat_rgb[idx_p, idx_c]
                if val == 0:
                    pixels_flat_rgb[idx_p, idx_c] = 1
                elif val == 255:
                    pixels_flat_rgb[idx_p, idx_c] = 254
                else:
                    if val % 2 == 1:
                        pixels_flat_rgb[idx_p, idx_c] = val - 1
                    else:
                        pixels_flat_rgb[idx_p, idx_c] = val + 1

    @staticmethod
    @numba.jit(nopython=True)
    def _extract_hamming73_numba(pixels_flat_rgb, pixel_indices, channel_indices, groups, bits_len):
        """
        Декодирование Hamming(7,3): возвращает массив битов длиной bits_len.
        """
        out = np.zeros(bits_len, dtype=np.uint8)
        for g in range(groups):
            base = g * 7
            v0 = pixels_flat_rgb[pixel_indices[base + 0], channel_indices[base + 0]] & 1
            v1 = pixels_flat_rgb[pixel_indices[base + 1], channel_indices[base + 1]] & 1
            v2 = pixels_flat_rgb[pixel_indices[base + 2], channel_indices[base + 2]] & 1
            v3 = pixels_flat_rgb[pixel_indices[base + 3], channel_indices[base + 3]] & 1
            v4 = pixels_flat_rgb[pixel_indices[base + 4], channel_indices[base + 4]] & 1
            v5 = pixels_flat_rgb[pixel_indices[base + 5], channel_indices[base + 5]] & 1
            v6 = pixels_flat_rgb[pixel_indices[base + 6], channel_indices[base + 6]] & 1
            s0 = (v0 + v2 + v4 + v6) & 1
            s1 = (v1 + v2 + v5 + v6) & 1
            s2 = (v3 + v4 + v5 + v6) & 1
            pos = g * 3
            if pos < bits_len:
                out[pos] = s0
            if pos + 1 < bits_len:
                out[pos + 1] = s1
            if pos + 2 < bits_len:
                out[pos + 2] = s2
        return out

    @staticmethod
    def hide_aelsb(container_path: str, data: bytes, password: str, output_path: str,
                   progress_callback=None, cancel_event=None):
        try:
            rng_order = _generate_rng(password or "", "aelsbpp_order")
            with Image.open(container_path) as img:
                # Всегда RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                full_data = AdvancedStego._pack_data_with_header(data)
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8)).astype(np.uint8)
                r, n = 3, 7
                groups = (len(data_bits) + r - 1) // r
                needed_elements = groups * n
                # Новый детерминированный порядок
                pix_idx, ch_idx = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, needed_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                # Явно работаем с RGB
                flat_rgb = pixels.reshape(-1, 3)
                AdvancedStego._embed_hamming73_numba(flat_rgb, pix_idx, ch_idx, data_bits, groups)
                if progress_callback:
                    progress_callback(100.0)
                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)
        except Exception as e:
            raise e

    @staticmethod
    def extract_aelsb(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            rng_order = _generate_rng(password or "", "aelsbpp_order")
            with Image.open(image_path) as img:
                # Всегда RGB
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                pixels = np.array(img, dtype=np.uint8)
                flat_rgb = pixels.reshape(-1, 3)
                header_bits_needed = HEADER_FULL_LEN * 8
                r, n = 3, 7
                header_groups = (header_bits_needed + r - 1) // r
                header_elements = header_groups * n
                # Индексы для заголовка
                pix_idx_hdr, ch_idx_hdr = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, header_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                header_bits = AdvancedStego._extract_hamming73_numba(flat_rgb, pix_idx_hdr, ch_idx_hdr,
                                                                     header_groups, header_bits_needed)
                header_bytes = np.packbits(header_bits).tobytes()
                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big')
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")
                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                total_groups = (total_bits_needed + r - 1) // r
                total_elements = total_groups * n
                # Для полного сообщения заново пересоздаём RNG,
                # чтобы порядок был тем же (префикс совпадёт с заголовком)
                rng_order = _generate_rng(password or "", "aelsbpp_order")
                pix_idx_all, ch_idx_all = AdvancedStego._prepare_calsb_indices(pixels, None, rng_order, total_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                bits = AdvancedStego._extract_hamming73_numba(flat_rgb, pix_idx_all, ch_idx_all,
                                                              total_groups, total_bits_needed)
                full_bytes = np.packbits(bits).tobytes()
                if progress_callback:
                    progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e

    @staticmethod
    def _rank_indices_by_hill(img: Image.Image,
                              rng: np.random.Generator,
                              needed_elements: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Дает. порядок позиций по HILL: квантуем cost в int и используем целочисленный tie-break.
        Гарантирует идентичный порядок на скрытии/извлечении.
        """
        img_rgb = img.convert('RGB')  # строго RGB
        pixels = np.array(img_rgb, dtype=np.uint8)
        h, w, _ = pixels.shape
        total = h * w * 3
        if needed_elements > total:
            raise ValueError("Недостаточно места для встраивания (HILL).")
        # HILL-карта на санированной картинке (LSB=0)
        cost_map = AdvancedStego._hill_cost_map(img_rgb)  # (h, w) float32
        # Квантуем, чтобы исключить микроскопические float-расхождения
        cost_q = np.round(cost_map * 1e7).astype(np.int64)  # (h, w) int64
        # Повтор на каналы
        cost_flat = np.repeat(cost_q.reshape(-1), 3)  # (h*w*3,) int64
        # Целочисленный тай-брейк от RNG - строго детерминирован
        tie = rng.integers(0, np.iinfo(np.int64).max, size=cost_flat.size, dtype=np.int64)
        # np.lexsort: последний ключ - первичный
        order = np.lexsort((tie, cost_flat))  # сначала cost, потом tie
        chosen = order[:needed_elements]
        pixel_idx = (chosen // 3).astype(np.int64)
        channel_idx = (chosen % 3).astype(np.int64)
        return pixel_idx, channel_idx

    @staticmethod
    def hide_hill(container_path: str, data: bytes, password: str, output_path: str,
                  progress_callback=None, cancel_event=None):
        """
        HILL-CA LSB Matching + Hamming(7,3)
        """
        try:
            rng_order = _generate_rng(password or "", "hill_order")
            with Image.open(container_path) as img:
                img_rgb = img.convert('RGB')
                pixels = np.array(img_rgb, dtype=np.uint8)
                full_data = AdvancedStego._pack_data_with_header(data)
                data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8)).astype(np.uint8)
                r, n = 3, 7
                groups = (len(data_bits) + r - 1) // r
                needed_elements = groups * n
                # Индексы по HILL
                pix_idx, ch_idx = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, needed_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                flat_rgb = pixels.reshape(-1, 3)
                AdvancedStego._embed_hamming73_numba(flat_rgb, pix_idx, ch_idx, data_bits, groups)
                if progress_callback:
                    progress_callback(100.0)
                result_img = Image.fromarray(pixels)
                result_img.save(output_path, format='PNG', optimize=True)
        except Exception as e:
            raise e

    @staticmethod
    def extract_hill(image_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        """
        Извлечение: тот же порядок по HILL.
        """
        try:
            rng_order = _generate_rng(password or "", "hill_order")
            with Image.open(image_path) as img:
                img_rgb = img.convert('RGB')
                pixels = np.array(img_rgb, dtype=np.uint8)
                flat_rgb = pixels.reshape(-1, 3)
                header_bits_needed = HEADER_FULL_LEN * 8
                r, n = 3, 7
                header_groups = (header_bits_needed + r - 1) // r
                header_elements = header_groups * n
                # Индексы для заголовка
                pix_idx_hdr, ch_idx_hdr = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, header_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                header_bits = AdvancedStego._extract_hamming73_numba(
                    flat_rgb, pix_idx_hdr, ch_idx_hdr, header_groups, header_bits_needed
                )
                header_bytes = np.packbits(header_bits).tobytes()
                if header_bytes[:HEADER_MAGIC_LEN] != MAGIC_BYTES:
                    raise ValueError("Магические байты не найдены.")
                data_len = int.from_bytes(
                    header_bytes[HEADER_MAGIC_LEN + HEADER_CHECKSUM_LEN:HEADER_FULL_LEN], 'big'
                )
                if not (0 <= data_len <= (pixels.size // 8)):
                    raise ValueError("Некорректная длина данных.")
                total_bits_needed = (HEADER_FULL_LEN + data_len) * 8
                total_groups = (total_bits_needed + r - 1) // r
                total_elements = total_groups * n
                # Переинициализируем RNG - порядок должен совпасть полностью
                rng_order = _generate_rng(password or "", "hill_order")
                pix_idx_all, ch_idx_all = AdvancedStego._rank_indices_by_hill(img_rgb, rng_order, total_elements)
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")
                bits = AdvancedStego._extract_hamming73_numba(
                    flat_rgb, pix_idx_all, ch_idx_all, total_groups, total_bits_needed
                )
                full_bytes = np.packbits(bits).tobytes()
                if progress_callback:
                    progress_callback(100.0)
                return AdvancedStego._unpack_data_with_header(full_bytes)
        except Exception as e:
            raise e


# ───────────────────────────────────────────────
# 📸 КЛАСС ДЛЯ JPEG DCT СТЕГАНОГРАФИИ
# ───────────────────────────────────────────────
class JPEGStego:
    """
    Класс для стеганографии в JPEG изображениях методом DCT (Дискретное Косинусное Преобразование).
    Особенности:
    - Использует канал Y (яркость) цветового пространства YCbCr
    - Работает с блоками 8x8 пикселей (стандарт JPEG)
    - Встраивает данные в среднечастотные коэффициенты DCT
    - Обеспечивает устойчивость к JPEG-сжатию
    """

    @staticmethod
    def _pack_data_with_header(data: bytes) -> bytes:
        """Упаковывает данные с заголовком (магия, длина, контрольная сумма)"""
        checksum = zlib.crc32(data).to_bytes(4, 'big')
        data_len = len(data).to_bytes(4, 'big')
        magic = b'JPEG'  # Магические байты для JPEG DCT
        return magic + checksum + data_len + data

    @staticmethod
    def _unpack_data_with_header(full_bytes: bytes) -> bytes:
        """Распаковывает данные с проверкой заголовка"""
        if len(full_bytes) < 12:  # 4 (magic) + 4 (checksum) + 4 (length)
            raise ValueError("Недостаточно данных для заголовка")

        magic = full_bytes[:4]
        if magic != b'JPEG':
            raise ValueError("Неверные магические байты")

        stored_checksum = int.from_bytes(full_bytes[4:8], 'big')
        data_len = int.from_bytes(full_bytes[8:12], 'big')

        if len(full_bytes) < 12 + data_len:
            raise ValueError("Данные обрезаны")

        data = full_bytes[12:12 + data_len]
        calculated_checksum = zlib.crc32(data)

        if calculated_checksum != stored_checksum:
            raise ValueError("Ошибка контрольной суммы")

        return data

    @staticmethod
    def hide_dct(container_path: str, data: bytes, output_path: str,
                 progress_callback=None, cancel_event=None) -> None:
        try:
            # Загружаем изображение
            img = cv2.imread(container_path)
            if img is None:
                raise ValueError("Не удалось загрузить изображение")

            # Проверяем, что изображение в формате JPEG (цветовое пространство YCbCr)
            # Важно: работаем только с каналом яркости Y
            img_ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            y_channel = img_ycbcr[:, :, 0].astype(np.float32)

            # Получаем размеры и выравниваем до кратных 8
            h, w = y_channel.shape
            h_blocks = h // 8
            w_blocks = w // 8

            if h_blocks == 0 or w_blocks == 0:
                raise ValueError("Изображение слишком маленькое для JPEG DCT стеганографии")

            # Упаковываем данные с заголовком
            full_data = JPEGStego._pack_data_with_header(data)
            data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))

            # Проверяем вместимость (1 бит на блок)
            max_capacity = h_blocks * w_blocks
            if len(data_bits) > max_capacity:
                raise ValueError(
                    f"Данные слишком велики для изображения. "
                    f"Максимум: {max_capacity // 8} байт, требуется: {len(full_data)} байт"
                )

            # Коэффициенты DCT для встраивания (средние частоты)
            embed_positions = [(4, 4), (5, 5), (4, 5), (5, 4)]
            bit_index = 0
            total_blocks = h_blocks * w_blocks

            # Проходим по всем блокам
            for i in range(h_blocks):
                for j in range(w_blocks):
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Операция отменена пользователем")

                    # Берём блок 8x8 (гарантированно полный благодаря выравниванию)
                    block = y_channel[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8].copy()

                    # Применяем DCT
                    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

                    # Встраиваем данные если ещё есть биты
                    if bit_index < len(data_bits):
                        # Выбираем позицию для встраивания (циклически)
                        pos_idx = (i * w_blocks + j) % len(embed_positions)
                        u, v = embed_positions[pos_idx]

                        # Получаем текущее значение коэффициента
                        coeff = dct_block[u, v]

                        # Встраиваем бит методом LSB (только для коэффициентов > 1 для устойчивости)
                        if abs(coeff) > 1.0:
                            bit = data_bits[bit_index]
                            if (int(coeff) % 2) != bit:
                                dct_block[u, v] = coeff + (1 if bit else -1)
                            bit_index += 1

                    # Обратное DCT
                    idct_block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')

                    # Возвращаем блок на место
                    y_channel[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8] = idct_block

                    # Обновляем прогресс
                    if progress_callback and (i * w_blocks + j) % 50 == 0:
                        progress = (i * w_blocks + j) / total_blocks * 100
                        progress_callback(progress)

            # Обрезаем значения до допустимого диапазона
            y_channel = np.clip(y_channel, 0, 255)

            # Обновляем канал Y
            img_ycbcr[:, :, 0] = y_channel.astype(np.uint8)

            # Конвертируем обратно в BGR
            img_stego = cv2.cvtColor(img_ycbcr, cv2.COLOR_YCrCb2BGR)

            # СОХРАНЯЕМ С МАКСИМАЛЬНЫМ КАЧЕСТВОМ (100%) для предотвращения потери данных!
            cv2.imwrite(output_path, img_stego, [cv2.IMWRITE_JPEG_QUALITY, 100])

            if progress_callback:
                progress_callback(100.0)

        except Exception as e:
            raise Exception(f"Ошибка при скрытии данных JPEG DCT: {str(e)}")

    @staticmethod
    def extract_dct(stego_path: str, progress_callback=None, cancel_event=None) -> bytes:
        try:
            # Загружаем изображение
            img = cv2.imread(stego_path)
            if img is None:
                raise ValueError("Не удалось загрузить изображение")

            # Преобразуем в YCbCr
            img_ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            y_channel = img_ycbcr[:, :, 0].astype(np.float32)

            # Размеры и выравнивание
            h, w = y_channel.shape
            h_blocks = h // 8
            w_blocks = w // 8
            total_blocks = h_blocks * w_blocks

            if h_blocks == 0 or w_blocks == 0:
                raise ValueError("Изображение слишком маленькое для извлечения данных")

            # Коэффициенты для извлечения (должны совпадать с встраиванием)
            embed_positions = [(4, 4), (5, 5), (4, 5), (5, 4)]

            # Собираем биты
            extracted_bits = []
            for i in range(h_blocks):
                for j in range(w_blocks):
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Операция отменена пользователем")

                    # Блок 8x8
                    block = y_channel[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8]

                    # DCT
                    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

                    # Выбираем ту же позицию
                    pos_idx = (i * w_blocks + j) % len(embed_positions)
                    u, v = embed_positions[pos_idx]

                    # Извлекаем бит (младший бит коэффициента)
                    coeff = dct_block[u, v]
                    bit = 1 if int(coeff) % 2 == 1 else 0
                    extracted_bits.append(bit)

                    # Обновляем прогресс
                    if progress_callback and (i * w_blocks + j) % 50 == 0:
                        progress = (i * w_blocks + j) / total_blocks * 100
                        progress_callback(progress)

            # Преобразуем биты в байты
            extracted_bytes = np.packbits(extracted_bits).tobytes()

            # ЭФФЕКТИВНЫЙ ПОИСК ЗАГОЛОВКА (оптимизированный)
            magic = b'JPEG'
            magic_len = len(magic)
            header_len = 12  # 4 (magic) + 4 (checksum) + 4 (length)

            # Поиск заголовка с умным сканированием (проверяем каждые 8 бит = 1 байт)
            max_search = min(2000, len(extracted_bytes) - header_len)  # Увеличен до 2000 байт

            for offset in range(0, max_search, 8):  # Проверяем только границы байтов
                if extracted_bytes[offset:offset + magic_len] == magic:
                    try:
                        # Пытаемся распаковать данные
                        data = JPEGStego._unpack_data_with_header(extracted_bytes[offset:])
                        if progress_callback:
                            progress_callback(100.0)
                        return data
                    except Exception:
                        # Не валидные данные в этой позиции - продолжаем поиск
                        continue

            # Дополнительная проверка: если данные начинаются с заголовка
            if extracted_bytes.startswith(magic):
                try:
                    data = JPEGStego._unpack_data_with_header(extracted_bytes)
                    if progress_callback:
                        progress_callback(100.0)
                    return data
                except Exception:
                    pass

            raise ValueError(
                "Не удалось найти валидные данные. Возможные причины:\n"
                "1. Файл не содержит скрытой информации методом JPEG DCT\n"
                "2. Изображение было пересохранено с потерей качества (качество < 100%)\n"
                "3. Использован другой метод стеганографии"
            )

        except Exception as e:
            raise Exception(f"Ошибка при извлечении данных JPEG DCT: {str(e)}")

    @staticmethod
    def calculate_capacity(image_path: str) -> int:
        """
        Рассчитывает максимальную вместимость в байтах для JPEG DCT метода.

        Формула:
        Вместимость = (ширина // 8) * (высота // 8) // 8 - заголовок
        (по 1 биту на блок 8x8)
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return 0

            h, w = img.shape[:2]
            blocks = (h // 8) * (w // 8)

            # По 1 биту на блок, минус заголовок (12 байт)
            capacity_bits = blocks
            capacity_bytes = capacity_bits // 8

            # Минус заголовок
            if capacity_bytes > 12:
                return capacity_bytes - 12
            return 0

        except:
            return 0


AUDIO_MAGIC_BYTES = b'AWNG'
AUDIO_HEADER_CHECKSUM_LEN = 4
AUDIO_HEADER_DATALEN_LEN = 4
AUDIO_HEADER_FULL_LEN = len(AUDIO_MAGIC_BYTES) + AUDIO_HEADER_CHECKSUM_LEN + AUDIO_HEADER_DATALEN_LEN


class AudioStego:
    @staticmethod
    def _pack_data_with_header(data: bytes) -> bytes:
        checksum = zlib.crc32(data).to_bytes(AUDIO_HEADER_CHECKSUM_LEN, 'big')
        data_len = len(data).to_bytes(AUDIO_HEADER_DATALEN_LEN, 'big')
        return AUDIO_MAGIC_BYTES + checksum + data_len + data

    @staticmethod
    def _unpack_data_with_header(full_bytes: bytes) -> bytes:
        if len(full_bytes) < AUDIO_HEADER_FULL_LEN:
            raise ValueError("Недостаточно данных для заголовка.")
        magic = full_bytes[:len(AUDIO_MAGIC_BYTES)]
        if magic != AUDIO_MAGIC_BYTES:
            raise ValueError("Магические байты не найдены.")
        header_end = len(AUDIO_MAGIC_BYTES) + AUDIO_HEADER_CHECKSUM_LEN + AUDIO_HEADER_DATALEN_LEN
        stored_checksum = int.from_bytes(
            full_bytes[len(AUDIO_MAGIC_BYTES):len(AUDIO_MAGIC_BYTES) + AUDIO_HEADER_CHECKSUM_LEN], 'big')
        data_len = int.from_bytes(full_bytes[len(AUDIO_MAGIC_BYTES) + AUDIO_HEADER_CHECKSUM_LEN:header_end], 'big')
        data_start, data_end = header_end, header_end + data_len
        if len(full_bytes) < data_end:
            raise ValueError("Данные обрезаны.")
        data = full_bytes[data_start:data_end]
        if zlib.crc32(data) != stored_checksum:
            raise ValueError("Ошибка контрольной суммы.")
        return data

    @staticmethod
    def hide_lsb_wav(container_path: str, data: bytes, output_path: str):
        with wave.open(container_path, 'rb') as wav:
            params = wav.getparams()
            frames = bytearray(wav.readframes(wav.getnframes()))
        full_data = AudioStego._pack_data_with_header(data)
        bits = np.unpackbits(np.frombuffer(full_data, np.uint8))
        if len(bits) > len(frames):
            raise ValueError("Слишком большой объём данных для выбранного WAV.")
        for i, bit in enumerate(bits):
            frames[i] = (frames[i] & 0xFE) | bit
        with wave.open(output_path, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(bytes(frames))

    @staticmethod
    def extract_lsb_wav(stego_path: str):
        with wave.open(stego_path, 'rb') as wav:
            frames = bytearray(wav.readframes(wav.getnframes()))
        header_bits_len = AUDIO_HEADER_FULL_LEN * 8
        if len(frames) < header_bits_len:
            raise ValueError("Недостаточно данных для заголовка.")
        header_bits = [frames[i] & 1 for i in range(header_bits_len)]
        header_bytes = np.packbits(header_bits).tobytes()
        if header_bytes[:len(AUDIO_MAGIC_BYTES)] != AUDIO_MAGIC_BYTES:
            raise ValueError("Магические байты не найдены. WAV не содержит данных.")
        data_len = int.from_bytes(
            header_bytes[len(AUDIO_MAGIC_BYTES) + AUDIO_HEADER_CHECKSUM_LEN:AUDIO_HEADER_FULL_LEN], 'big')
        total_bits_to_extract = (AUDIO_HEADER_FULL_LEN + data_len) * 8
        if len(frames) < total_bits_to_extract:
            raise ValueError("Недостаточно данных для извлечения.")
        all_bits = [frames[i] & 1 for i in range(total_bits_to_extract)]
        full_bytes = np.packbits(all_bits).tobytes()
        return AudioStego._unpack_data_with_header(full_bytes)


# ───────────────────────────────────────────────
# 🖼️ КЛАСС ДЛЯ РАБОТЫ С ИЗОБРАЖЕНИЯМИ
# ───────────────────────────────────────────────
class ImageProcessor:
    @staticmethod
    def get_image_info(path: str) -> Tuple[int, int, int]:
        """
        Возвращает (ширина, высота, доступные биты) для изображения.
        Обновлено для поддержки JPEG DCT.
        """
        ext = os.path.splitext(path)[1].lower()

        if ext == '.wav':
            with wave.open(path, 'rb') as wav:
                frames = wav.getnframes()
            return 0, 0, frames

        else:
            try:
                # Для JPEG используем OpenCV для получения размеров
                if ext in ['.jpg', '.jpeg']:
                    img = cv2.imread(path)
                    if img is not None:
                        h, w = img.shape[:2]
                        # Для JPEG DCT вместимость рассчитывается по блокам
                        blocks = (h // 8) * (w // 8)
                        capacity_bits = blocks  # 1 бит на блок
                        return w, h, capacity_bits

                # Для других форматов используем PIL
                with Image.open(path) as img:
                    if img.mode not in ['RGB', 'RGBA']:
                        img = img.convert('RGB')
                    w, h = img.size
                    return w, h, w * h * 3

            except Exception as e:
                raise ValueError(f"Ошибка загрузки изображения: {str(e)}")

    @staticmethod
    def create_thumbnail(path: str, max_size: Tuple[int, int] = (200, 200)) -> ImageTk.PhotoImage:
        """Создает миниатюру изображения для предпросмотра"""
        try:
            with Image.open(path) as img:
                img.thumbnail(max_size, Image.Resampling.BOX)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                return ImageTk.PhotoImage(img)
        except Exception as e:
            raise ValueError(f"Ошибка создания миниатюры: {str(e)}")

    @staticmethod
    def get_capacity_by_method(total_pixels: int, method: str, width=0, height=0) -> int:
        """
        Рассчитывает теоретическую вместимость ПОЛЕЗНЫХ ДАННЫХ в битах для заданного метода.
        Обновлено для JPEG DCT.
        """
        if method == "jpeg_dct":
            # Для JPEG DCT: каждый блок 8x8 даёт 1 бит
            if width > 0 and height > 0:
                blocks = (width // 8) * (height // 8)
                capacity_bits = blocks
            else:
                # Оценка на основе total_pixels (приблизительно)
                capacity_bits = total_pixels // 64
        elif method in ("lsb", "noise"):
            capacity_bits = total_pixels * 3
        elif method in ("aelsb", "hill"):
            capacity_bits = int(total_pixels * (3 / 7))
        elif method == "audio_lsb":
            capacity_bits = total_pixels
        else:
            return 0

        # Вычитаем заголовок (размер зависит от метода)
        if method == "jpeg_dct":
            header_bits = 12 * 8  # 12 байт заголовок для JPEG DCT
        else:
            header_bits = HEADER_FULL_LEN * 8

        data_capacity_bits = max(0, capacity_bits - header_bits)
        return data_capacity_bits

    @staticmethod
    def hide_data(container_path: str, data: bytes, password: str, output_path: str,
                  method: str = "noise", compression_level: int = 9,
                  progress_callback=None, cancel_event=None) -> None:
        """Универсальный метод скрытия данных"""
        try:
            if method == "audio_lsb":
                AudioStego.hide_lsb_wav(container_path, data, output_path)
                return

            if method == "jpeg_dct":
                JPEGStego.hide_dct(
                    container_path=container_path,
                    data=data,
                    output_path=output_path,
                    progress_callback=progress_callback,
                    cancel_event=cancel_event
                )
                return

            # Существующие методы...
            if method == "lsb":
                AdvancedStego.hide_lsb(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "noise":
                AdvancedStego.hide_noise(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "aelsb":
                AdvancedStego.hide_aelsb(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            elif method == "hill":
                AdvancedStego.hide_hill(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
                )
            else:
                raise ValueError(f"Неизвестный метод скрытия: {method}")
        except Exception as e:
            raise e

    @staticmethod
    def extract_data(image_path: str, password: str, method: str = None,
                     progress_callback=None, cancel_event=None) -> bytes:
        """Универсальный метод извлечения данных"""

        # Сначала проверяем JPEG DCT, если файл JPEG
        ext = os.path.splitext(image_path)[1].lower()
        if ext in ['.jpg', '.jpeg'] and (method is None or method == "jpeg_dct"):
            try:
                return JPEGStego.extract_dct(
                    image_path, password, progress_callback, cancel_event
                )
            except Exception as e:
                if method == "jpeg_dct":  # Если метод указан явно
                    raise e
                # Иначе пробуем другие методы

        if method == "audio_lsb":
            return AudioStego.extract_lsb_wav(image_path)

        if method:
            methods_to_try = [method]
        else:
            methods_to_try = ["lsb", "noise", "aelsb", "hill", "jpeg_dct"]

        last_error = None
        for method_name in methods_to_try:
            try:
                if cancel_event and cancel_event.is_set():
                    raise InterruptedError("Операция отменена пользователем")

                if progress_callback:
                    progress_callback(0, f"Проверка метода: {STEGANO_METHODS.get(method_name, method_name)}...")

                if method_name == "lsb":
                    extractor = AdvancedStego.extract_lsb
                elif method_name == "noise":
                    extractor = AdvancedStego.extract_noise
                elif method_name == "aelsb":
                    extractor = AdvancedStego.extract_aelsb
                elif method_name == "hill":
                    extractor = AdvancedStego.extract_hill
                else:
                    continue

                def internal_progress(p):
                    if progress_callback:
                        base_progress = methods_to_try.index(method_name) * (100 / len(methods_to_try))
                        scaled_progress = p / len(methods_to_try)
                        progress_callback(base_progress + scaled_progress)

                data = extractor(image_path, password, internal_progress, cancel_event)
                if progress_callback:
                    progress_callback(100.0,
                                      f"✅ Данные успешно найдены методом: {STEGANO_METHODS.get(method_name, method_name)}!")
                return data

            except (ValueError, IndexError, InterruptedError) as e:
                last_error = e
                continue

        if isinstance(last_error, InterruptedError):
            raise last_error
        if last_error:
            raise ValueError(
                f"❌ Не удалось извлечь данные. Возможно, файл не содержит скрытой информации или данные повреждены.\
Последняя ошибка: {last_error}"
            )
        else:
            raise ValueError("❌ Не удалось извлечь данные. Ни один из поддерживаемых методов не подошел.")


# ───────────────────────────────────────────────
# 🎯 ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ
# ───────────────────────────────────────────────
class SteganographyUltimatePro:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title(f"ØccultoNG Pro v{VERSION}")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # Инициализация менеджеров
        self.theme_manager = ThemeManager(self.root)
        self.animation_manager = AnimationManager(self.root, self.theme_manager)
        self.analytics_manager = AnalyticsManager()
        self.history_manager = HistoryManager()
        self.notification_manager = NotificationManager(self.root, self.theme_manager)
        self.plugin_manager = PluginManager()
        self.file_manager = FileManager(self.root)
        self.log_manager = HistoryLog()
        # Загрузка настроек
        self.settings = self.load_settings()
        self.history = self.load_history()

        # Применение темы
        self.theme_manager.set_theme(self.settings.get("theme", "Тёмная"))
        self.colors = self.theme_manager.colors

        # Переменные
        self.img_path = tk.StringVar()
        self.last_progress_update_time = 0
        self.extract_img_path = tk.StringVar()
        self.data_type = tk.StringVar(value=self.settings.get("data_type", "text"))
        self.method_var = tk.StringVar(value=self.settings.get("method", "lsb"))
        self.compression_level = tk.IntVar(value=self.settings.get("compression_level", 9))
        self.current_extracted = None
        self.is_dragging = False
        self.last_update_time = 0
        self.file_path_var = tk.StringVar()
        self.last_open_dir = self.settings.get("last_open_dir", os.path.expanduser("~"))
        self.last_save_dir = self.settings.get("last_save_dir", os.path.expanduser("~"))

        # Элементы интерфейса
        self.preview_img = None
        self.extract_preview = None
        self.text_input = None
        self.result_text = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        self.history_labels = []
        self.size_info_frame = None
        self.required_size_label = None
        self.capacity_labels = {}
        self.usage_var = tk.DoubleVar(value=0.0)
        self.usage_bar = None
        self.usage_label = None

        # Для отмены операций
        self.cancel_event = threading.Event()
        self.operation_thread = None
        self.temp_extracted_file = None
        self.buttons_disabled = False

        # Toast
        self.toast_label = None
        self.toast_timer = None
        self._preview_photo = None
        self._extract_photo = None

        # Доп. элементы UX
        self.file_info_label = None
        self.file_entry_widget = None
        self.extract_drop_label = None
        self.text_menu = None
        self.result_menu = None
        self.history_menu = None
        self.open_file_button = None
        self.copy_hash_button = None
        self.last_extracted_hash = None

        # Статистика сессии
        self.session_start_time = time.time()
        self.operations_count = 0

        # Автосохранение
        self.autosave_id = None

        # Инициализация пароля
        password_dialog = ModernPasswordDialog(self.root, self.theme_manager.colors)
        if not password_dialog.password_correct:
            self.root.destroy()
            return

        # Настройка иконки
        try:
            self.root.iconbitmap(default=self.resource_path("../icon.ico"))
        except:
            pass

        # Создание интерфейса
        self.setup_ui()
        self.bind_drag_drop()
        self.bind_drag_drop_extract()
        self.bind_file_drop()
        self.refresh_history()
        self.bind_shortcuts()
        self.install_context_menus()
        self.install_tooltips()

        # Инициализация плагинов
        self.initialize_plugins()

        # Запуск автосохранения
        self.start_autosave()

        # Обновление статистики
        self.analytics_manager.stats["sessions"] = self.analytics_manager.stats.get("sessions", 0) + 1
        self.analytics_manager.save_stats()

        # Глобальный перехватчик ошибок
        def excepthook(exc_type, exc_value, exc_tb):
            import traceback
            traceback.print_exception(exc_type, exc_value, exc_tb)
            try:
                messagebox.showerror("Неожиданная ошибка", f"{exc_type.__name__}: {exc_value}")
                self.log_manager.add_entry("system_error", "error",
                                           {"error_type": exc_type.__name__, "error_message": str(exc_value)})
            except:
                pass

        sys.excepthook = excepthook

        # Показываем приветственное уведомление
        self.root.after(1000, self.show_welcome_notification)

    def resource_path(self, relative_path: str) -> str:
        """ Получает абсолютный путь к ресурсу """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath("..")
        return os.path.join(base_path, relative_path)

    def load_settings(self) -> dict:
        try:
            if os.path.exists(CONFIG["SETTINGS_FILE"]):
                with open(CONFIG["SETTINGS_FILE"], 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")
        return {
            "theme": "Тёмная",
            "method": "lsb",
            "data_type": "text",
            "compression_level": 9,
            "window_size": "1200x800",
            "last_open_dir": os.path.expanduser("~"),
            "last_save_dir": os.path.expanduser("~"),
            "show_tips": True,
            "auto_backup": True,
            "confirm_before_exit": True        }

    def save_settings(self) -> None:
        settings = {
            "theme": self.theme_manager.current_theme,
            "method": self.method_var.get(),
            "data_type": self.data_type.get(),
            "compression_level": self.compression_level.get(),
            "window_size": self.root.geometry(),
            "last_open_dir": self.last_open_dir,
            "last_save_dir": self.last_save_dir,
            "show_tips": self.settings.get("show_tips", True),
            "auto_backup": self.settings.get("auto_backup", True),
            "confirm_before_exit": self.settings.get("confirm_before_exit", True),
        }
        try:
            with open(CONFIG["SETTINGS_FILE"], 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def load_history(self) -> list:
        try:
            if os.path.exists(CONFIG["HISTORY_FILE"]):
                with open(CONFIG["HISTORY_FILE"], 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    valid_history = [h for h in history if os.path.exists(h)]
                    if len(valid_history) != len(history):
                        self.save_history(valid_history)
                    return valid_history[:MAX_HISTORY]
        except Exception as e:
            print(f"Ошибка загрузки истории: {e}")
        return []

    def save_history(self, history: list) -> None:
        try:
            with open(CONFIG["HISTORY_FILE"], 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def save_to_history(self, path: str) -> None:
        if not path:
            return
        hist = [path] + [h for h in self.history if h != path and os.path.exists(h)]
        self.history = hist[:MAX_HISTORY]
        self.save_history(self.history)
        self.refresh_history()
        self.file_manager.add_recent_file(path)

    def start_autosave(self):
        """Запускает автосохранение"""
        self.autosave_settings()
        self.autosave_id = self.root.after(CONFIG["AUTO_SAVE_INTERVAL"] * 1000, self.start_autosave)

    def autosave_settings(self):
        """Автосохранение настроек"""
        self.save_settings()

    def show_welcome_notification(self):
        """Показывает приветственное уведомление"""
        self.notification_manager.show_notification(
            f"Добро пожаловать в ØccultoNG Pro v{VERSION}!",
            "info",
            5000
        )

    def initialize_plugins(self):
        """Инициализирует плагины"""
        plugins = self.plugin_manager.get_plugins()
        if plugins:
            plugin_names = ", ".join(plugins.keys())
            self.notification_manager.show_notification(
                f"Загружены плагины: {plugin_names}",
                "info",
                3000
            )

    def setup_ui(self) -> None:
        # Основной фрейм
        main_frame = ttk.Frame(self.root, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Создаем заголовок
        self.create_header(main_frame)

        # Создаем вкладки
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Создаем статусную панель
        self.create_status_bar(main_frame)

        # Создаем вкладки
        self.create_hide_tab()
        self.create_extract_tab()
        self.create_analysis_tab()
        self.create_settings_tab()
        self.create_encryption_tab()
        self.create_statistics_tab()  # Создаем вкладку "Статистика"
        self.create_help_tab()  # Создаем вкладку "Помощь"

        # Добавляем вкладки в notebook с правильными текстами и иконками
        self.notebook.add(self.hide_tab, text="📦 Скрыть данные")
        self.notebook.add(self.extract_tab, text="🔍 Извлечь данные")
        self.notebook.add(self.analysis_tab, text="🔬 Анализ файла")
        self.notebook.add(self.encryption_tab, text="🔐 Шифрование")
        self.create_batch_tab()
        self.notebook.add(self.statistics_tab, text="📊 Статистика")
        self.notebook.add(self.help_tab, text="❓ Помощь")
        self.notebook.add(self.settings_tab, text="⚙️ Настройки")

        # Создаем тост
        self.create_toast()

    def create_header(self, parent: ttk.Frame) -> None:
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 15))
        # Логотип и название
        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        # Иконка приложения
        icon_label = tk.Label(
            title_frame,
            text="🔒",
            font=("Segoe UI", 24),
            bg=self.colors["bg"],
            fg=self.colors["accent"]
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        title = ttk.Label(
            title_frame,
            text="ØccultoNG Pro",
            font=("Segoe UI Variable Display", 24, "bold"),
            foreground=self.colors["accent"]
        )
        exit_btn = ttk.Button(
            title_frame,
            text="🚪 Выход",
            command=self.on_close,
            style="IconButton.TButton"
        )
        exit_btn.pack(side=tk.LEFT, padx=5)
        title.pack(side=tk.LEFT)
        version_label = ttk.Label(
            title_frame,
            text=f"v{VERSION}",
            font=("Segoe UI", 11),
            foreground=self.colors["text_secondary"]
        )
        version_label.pack(side=tk.LEFT, padx=(8, 0), pady=(5, 0))

    def create_hide_tab(self) -> None:
        self.hide_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.hide_tab, text="📦 Скрыть данные")

        # Создаем холст с прокруткой
        canvas = tk.Canvas(self.hide_tab, bg=self.colors["bg"], highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(self.hide_tab, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.hide_tab, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Создаем внутренний фрейм для контента
        content_frame = ttk.Frame(canvas, style="Card.TFrame")

        # Настройка прокрутки
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Размещаем элементы
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Привязываем колесо мыши для прокрутки
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Создаем две колонки
        left_frame = ttk.Frame(content_frame, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)
        right_frame = ttk.Frame(content_frame, style="Card.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)

        # Левая колонка - контейнер
        container_frame = ttk.LabelFrame(
            left_frame,
            text="🖼️ Изображение-контейнер",
            padding=15,
            style="Card.TLabelframe"
        )
        container_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Путь к изображению
        path_frame = ttk.Frame(container_frame, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(path_frame, text="📂 Путь к файлу:", style="TLabel").pack(side=tk.LEFT)
        path_entry = ttk.Entry(
            path_frame, textvariable=self.img_path, state='readonly', width=50, style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Кнопки управления
        button_frame = ttk.Frame(path_frame, style="Card.TFrame")
        button_frame.pack(side=tk.RIGHT)
        browse_btn = ttk.Button(
            button_frame, text="🔍 Обзор...", command=self.select_image, style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)
        folder_btn = ttk.Button(
            button_frame, text="📁 Папка", command=lambda: Utils.open_in_file_manager(
                os.path.dirname(self.img_path.get()) if self.img_path.get() else "."), style="IconButton.TButton"
        )
        folder_btn.pack(side=tk.LEFT, padx=(5, 0))
        info_btn = ttk.Button(
            button_frame, text="ℹ️ Инфо", command=self.show_container_info, style="IconButton.TButton"
        )
        info_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Дроп-зона
        drop_frame = ttk.Frame(container_frame, style="DropZone.TFrame")
        drop_frame.pack(fill=tk.X, pady=10)
        self.drop_label = ttk.Label(
            drop_frame,
            text="📥 Перетащите сюда файл-контейнер или кликните для выбора файла",
            anchor="center", font=("Segoe UI", 12, "bold"), cursor="hand2", style="DropLabel.TLabel"
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.drop_label.bind("<Button-1>", lambda e: self.select_image())

        # Предпросмотр
        preview_frame = ttk.LabelFrame(
            container_frame,
            text="🔍 Предпросмотр",
            padding=10,
            style="Card.TLabelframe"
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.preview_img = ttk.Label(preview_frame)
        self.preview_img.pack(pady=5, fill=tk.BOTH, expand=True)

        # Правая колонка - данные
        data_frame = ttk.LabelFrame(
            right_frame, text="📋 Скрываемые данные", padding=15, style="Card.TLabelframe"
        )
        data_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Тип данных
        type_frame = ttk.Frame(data_frame, style="Card.TFrame")
        type_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(type_frame, text="📄 Тип данных:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(
            type_frame, text="Текст", variable=self.data_type, value="text", command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(
            type_frame, text="Файл", variable=self.data_type, value="file", command=self.toggle_data_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT)

        # Фреймы для текста и файла
        self.text_frame = ttk.Frame(data_frame, style="Card.TFrame")
        self.file_frame = ttk.Frame(data_frame, style="Card.TFrame")

        # Текстовый ввод
        text_toolbar = ttk.Frame(self.text_frame, style="Card.TFrame")
        text_toolbar.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(text_toolbar, text="🗑️ Очистить", style="IconButton.TButton", command=self.clear_text).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(text_toolbar, text="📋 Вставить", style="IconButton.TButton", command=self.paste_text).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(text_toolbar, text="📝 Шаблоны", style="IconButton.TButton", command=self.show_templates).pack(
            side=tk.LEFT)
        self.text_input = scrolledtext.ScrolledText(
            self.text_frame, height=10, font=("Consolas", 10), wrap=tk.WORD,
            bg=self.colors["card"], fg=self.colors["text"], insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"], selectforeground="#ffffff", relief="flat", borderwidth=1
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        self.text_input.bind("<KeyRelease>", lambda e: self.update_size_info())

        # Выбор файла
        file_input_frame = ttk.Frame(self.file_frame, style="Card.TFrame")
        file_input_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(file_input_frame, text="📎 Файл для скрытия:", style="TLabel").pack(side=tk.LEFT)
        file_entry = ttk.Entry(
            file_input_frame, textvariable=self.file_path_var, state='readonly', width=40, style="TEntry"
        )
        file_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.file_entry_widget = file_entry
        ttk.Button(
            file_input_frame, text="📂 Выбрать...", command=self.select_file, style="IconButton.TButton"
        ).pack(side=tk.LEFT, padx=(5, 0))
        self.file_info_label = ttk.Label(self.file_frame, text="ℹ️ Поддерживаемые форматы: любые файлы до 100 МБ",
                                         style="Secondary.TLabel")
        self.file_info_label.pack(fill=tk.X, pady=(6, 0))

        # Настройки метода
        method_frame = ttk.LabelFrame(
            right_frame, text="⚙️ Настройки метода", padding=15, style="Card.TLabelframe"
        )
        method_frame.pack(fill=tk.X, pady=(0, 15))

        # Выбор метода
        method_select_frame = ttk.Frame(method_frame, style="Card.TFrame")
        method_select_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(method_select_frame, text="Метод скрытия:", style="TLabel").pack(side=tk.LEFT)
        method_combo = ttk.Combobox(
            method_select_frame, textvariable=self.method_var, values=list(STEGANO_METHODS.keys()),
            state="readonly", width=30, style="TCombobox"
        )
        method_combo.pack(side=tk.LEFT, padx=5)
        method_combo.bind("<<ComboboxSelected>>", lambda e: self.update_size_info())

        # Сжатие PNG
        compression_frame = ttk.Frame(method_frame, style="Card.TFrame")
        compression_frame.pack(fill=tk.X)
        ttk.Label(compression_frame, text="Степень сжатия PNG:", style="TLabel").pack(side=tk.LEFT, padx=(10, 0))
        compression_combo = ttk.Combobox(
            compression_frame, textvariable=self.compression_level, values=list(range(0, 10)),
            state="readonly", width=5, style="TCombobox"
        )
        compression_combo.pack(side=tk.LEFT, padx=5)

        # Анализ вместимости
        self.size_info_frame = ttk.LabelFrame(
            right_frame, text="📊 Анализ вместимости", padding=10, style="Card.TLabelframe"
        )
        self.size_info_frame.pack(fill=tk.X, pady=(0, 15))

        # Требуемый размер
        self.required_size_label = ttk.Label(self.size_info_frame, text="📏 Требуется: выберите данные", style="TLabel")
        self.required_size_label.pack(anchor="w", padx=5)
        ttk.Separator(self.size_info_frame, orient="horizontal").pack(fill=tk.X, pady=5)

        # Вместимость по методам
        self.capacity_labels = {}
        capacity_pairs = [(["lsb", "noise"], "🟢 LSB / Adaptive-Noise"), (["aelsb", "hill"], "🔵 AELSB / HILL")]
        for methods, label_text in capacity_pairs:
            lbl = ttk.Label(self.size_info_frame, text=f"{label_text}: ожидание...", style="Secondary.TLabel")
            lbl.pack(anchor="w", padx=5, pady=(2, 0))
            for method in methods:
                self.capacity_labels[method] = lbl

        # Индикатор заполнения
        ttk.Separator(self.size_info_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        self.usage_label = ttk.Label(self.size_info_frame, text="📈 Заполнение выбранного метода: не рассчитано",
                                     style="TLabel")
        self.usage_label.pack(anchor="w", padx=5, pady=(0, 6))
        self.usage_bar = ttk.Progressbar(self.size_info_frame, variable=self.usage_var, maximum=100,
                                         style="UsageGreen.Horizontal.TProgressbar")
        self.usage_bar.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Кнопка скрытия
        self.hide_button = ttk.Button(
            right_frame, text="🔐 Скрыть данные", style="Accent.TButton", command=self.start_hide
        )
        self.hide_button.pack(fill=tk.X, pady=(15, 0))

        # Инициализация ввода данных
        if self.data_type.get() == "text":
            self.text_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.file_frame.pack(fill=tk.X, pady=(10, 0))

    def create_extract_tab(self) -> None:
        self.extract_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.extract_tab, text="🔍 Извлечь данные")

        # Создаем холст с прокруткой
        canvas = tk.Canvas(self.extract_tab, bg=self.colors["bg"], highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(self.extract_tab, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.extract_tab, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Создаем внутренний фрейм для контента
        content_frame = ttk.Frame(canvas, style="Card.TFrame")

        # Настройка прокрутки
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Размещаем элементы
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Привязываем колесо мыши для прокрутки
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Создаем две колонки
        left_frame = ttk.Frame(content_frame, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 10), pady=20)
        right_frame = ttk.Frame(content_frame, style="Card.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 20), pady=20)

        # Левая колонка - контейнер
        container_frame = ttk.LabelFrame(
            left_frame,
            text="🖼️ Изображение со скрытыми данными",
            padding=15,
            style="Card.TLabelframe"
        )
        container_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Путь к изображению
        path_frame = ttk.Frame(container_frame, style="Card.TFrame")
        path_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(path_frame, text="📂 Путь к файлу:", style="TLabel").pack(side=tk.LEFT)
        path_entry = ttk.Entry(
            path_frame,
            textvariable=self.extract_img_path,
            state='readonly',
            width=50,
            style="TEntry"
        )
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Кнопки управления
        button_frame = ttk.Frame(path_frame, style="Card.TFrame")
        button_frame.pack(side=tk.RIGHT)
        browse_btn = ttk.Button(
            button_frame,
            text="🔍 Обзор...",
            command=self.select_extract_image,
            style="IconButton.TButton"
        )
        browse_btn.pack(side=tk.LEFT)
        folder_btn = ttk.Button(
            button_frame,
            text="📁 Папка",
            command=lambda: Utils.open_in_file_manager(
                os.path.dirname(self.extract_img_path.get()) if self.extract_img_path.get() else "."),
            style="IconButton.TButton"
        )
        folder_btn.pack(side=tk.LEFT, padx=(5, 0))
        info_btn = ttk.Button(
            button_frame,
            text="ℹ️ Инфо",
            command=self.show_extract_container_info,
            style="IconButton.TButton"
        )
        info_btn.pack(side=tk.LEFT, padx=(5, 0))

        # Дроп-зона
        self.extract_drop_label = ttk.Label(
            container_frame,
            text="📥 Перетащите сюда файл со скрытыми данными или кликните для выбора файла",
            anchor="center", font=("Segoe UI", 11, "bold"), cursor="hand2", style="DropLabel.TLabel"
        )
        self.extract_drop_label.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.extract_drop_label.bind("<Button-1>", lambda e: self.select_extract_image())

        # Предпросмотр
        preview_frame = ttk.LabelFrame(
            container_frame,
            text="🔍 Предпросмотр",
            padding=10,
            style="Card.TLabelframe"
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.extract_preview = ttk.Label(preview_frame)
        self.extract_preview.pack(pady=5, fill=tk.BOTH, expand=True)

        # Правая колонка - результаты
        result_frame = ttk.LabelFrame(
            right_frame,
            text="📋 Извлечённые данные",
            padding=15,
            style="Card.TLabelframe"
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Панель инструментов результатов
        result_toolbar = ttk.Frame(result_frame, style="Card.TFrame")
        result_toolbar.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(result_toolbar, text="📋 Копировать", style="IconButton.TButton", command=self.copy_extracted).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(result_toolbar, text="💾 Сохранить", style="IconButton.TButton", command=self.save_extracted).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(result_toolbar, text="🗂 Открыть", style="IconButton.TButton", command=self.open_extracted_file).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(result_toolbar, text="🔑 Хеш", style="IconButton.TButton", command=self.copy_extracted_hash).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(result_toolbar, text="📊 Анализ", style="IconButton.TButton",
                   command=self.analyze_extracted_data).pack(
            side=tk.LEFT, padx=(0, 5))

        # Текстовое поле результатов
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=12,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=1
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Кнопки действий
        btn_frame = ttk.Frame(right_frame, style="Card.TFrame")
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        button_configs = [
            ("🔍 Извлечь данные", self.start_extract, "extract_button"),
            ("📋 Копировать", self.copy_extracted, "copy_button"),
            ("💾 Сохранить", self.save_extracted, "save_button"),
            ("🗂 Открыть файл", self.open_extracted_file, "open_file_button"),
            ("🔑 Копировать хеш", self.copy_extracted_hash, "copy_hash_button")
        ]
        for text, command, attr_name in button_configs:
            btn = ttk.Button(
                btn_frame,
                text=text,
                style="Action.TButton",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)
            setattr(self, attr_name, btn)

        # История файлов
        hist_frame = ttk.LabelFrame(
            right_frame,
            text="📚 Последние использованные файлы",
            padding=10,
            style="Card.TLabelframe"
        )
        hist_frame.pack(fill=tk.X, pady=(15, 0))

        # Кнопка очистки истории
        clear_history_btn = ttk.Button(
            hist_frame,
            text="🗑️ Очистить историю",
            command=self.clear_history,
            style="IconButton.TButton"
        )
        clear_history_btn.pack(anchor="e", pady=(0, 5))

        # Метки истории
        self.history_labels = []
        for i in range(MAX_HISTORY):
            lbl = ttk.Label(
                hist_frame,
                text="",
                style="History.TLabel",
                cursor="hand2"
            )
            lbl.pack(anchor="w", pady=2)
            self.history_labels.append(lbl)

    def create_analysis_tab(self) -> None:
        """Создает вкладку анализа файла с прокруткой"""
        self.analysis_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.analysis_tab, text="🔬 Анализ файла")

        # Создаем холст с прокруткой
        canvas = tk.Canvas(self.analysis_tab, bg=self.colors["bg"], highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(self.analysis_tab, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.analysis_tab, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Создаем внутренний фрейм для контента
        content_frame = ttk.Frame(canvas, style="Card.TFrame")

        # Настройка прокрутки
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Размещаем элементы
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Привязываем колесо мыши для прокрутки
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        canvas.bind_all("<Shift-MouseWheel>", lambda e: canvas.xview_scroll(int(-1 * (e.delta / 120)), "units"))

        # Инициализируем вкладку анализа
        self.analysis_ui = AnalysisTab(content_frame, self)

    def create_encryption_tab(self) -> None:
        """Создает полнофункциональную вкладку шифрования и дешифрования"""
        self.encryption_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.encryption_tab, text="🔐 Шифрование")

        # Основной контейнер с прокруткой
        main_canvas = tk.Canvas(self.encryption_tab, bg=self.colors["bg"], highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(self.encryption_tab, orient="vertical", command=main_canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.encryption_tab, orient="horizontal", command=main_canvas.xview)
        main_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        scrollable_frame = ttk.Frame(main_canvas, style="Card.TFrame")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Размещение элементов
        main_canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        # Привязка колеса мыши
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Создаем содержимое
        self._create_encryption_content(scrollable_frame)

    def create_batch_tab(self):
        """Создает вкладку пакетной обработки"""
        self.batch_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.batch_tab, text="📦 Пакетная обработка")

        # Инициализация UI пакетной обработки
        self.batch_ui = BatchProcessingUI(self.batch_tab, self)

    def create_settings_tab(self) -> None:
        self.settings_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.settings_tab, text="⚙️ Настройки")

        # Создаем canvas с прокруткой для настроек
        settings_canvas = tk.Canvas(self.settings_tab, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(self.settings_tab, orient="vertical", command=settings_canvas.yview)
        scrollable_frame = ttk.Frame(settings_canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))
        )

        settings_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        settings_canvas.configure(yscrollcommand=scrollbar.set)

        settings_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Тема интерфейса
        appearance_group = ttk.LabelFrame(
            scrollable_frame,
            text="🎨 Тема интерфейса",
            padding=15,
            style="Card.TLabelframe"
        )
        appearance_group.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            appearance_group,
            text="🖌️ Выберите стиль оформления:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        theme_combo = ttk.Combobox(
            appearance_group,
            textvariable=theme_var,
            values=list(THEMES.keys()),
            state="readonly",
            style="TCombobox"
        )
        theme_combo.pack(fill=tk.X, pady=(0, 10))
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.change_theme(theme_var.get()))

        # Параметры по умолчанию
        params_group = ttk.LabelFrame(
            scrollable_frame,
            text="🔧 Параметры по умолчанию",
            padding=15,
            style="Card.TLabelframe"
        )
        params_group.pack(fill=tk.X, pady=(0, 15))

        # Метод скрытия
        ttk.Label(
            params_group,
            text="🧪 Метод скрытия:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        method_combo = ttk.Combobox(
            params_group,
            textvariable=self.method_var,
            values=list(STEGANO_METHODS.keys()),
            state="readonly",
            style="TCombobox"
        )
        method_combo.pack(fill=tk.X, pady=(0, 10))

        # Тип данных
        ttk.Label(
            params_group,
            text="📄 Тип данных:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        data_type_combo = ttk.Combobox(
            params_group,
            textvariable=self.data_type,
            values=["text", "file"],
            state="readonly",
            style="TCombobox"
        )
        data_type_combo.pack(fill=tk.X, pady=(0, 10))

        # Степень сжатия PNG
        ttk.Label(
            params_group,
            text="💾 Степень сжатия PNG:",
            font=("Segoe UI", 11),
            style="TLabel"
        ).pack(anchor="w", pady=(0, 5))

        compression_combo = ttk.Combobox(
            params_group,
            textvariable=self.compression_level,
            values=list(range(0, 10)),
            state="readonly",
            style="TCombobox"
        )
        compression_combo.pack(fill=tk.X, pady=(0, 10))

        # Дополнительные настройки
        extra_group = ttk.LabelFrame(
            scrollable_frame,
            text="⚙️ Дополнительные настройки",
            padding=15,
            style="Card.TLabelframe"
        )
        extra_group.pack(fill=tk.X, pady=(0, 15))

        # Показывать подсказки
        self.show_tips_var = tk.BooleanVar(value=self.settings.get("show_tips", True))
        tips_check = ttk.Checkbutton(
            extra_group,
            text="Показывать подсказки и советы",
            variable=self.show_tips_var,
            style="TCheckbutton"
        )
        tips_check.pack(anchor="w", pady=(0, 5))

        # Автоматическое создание резервных копий
        self.auto_backup_var = tk.BooleanVar(value=self.settings.get("auto_backup", True))
        backup_check = ttk.Checkbutton(
            extra_group,
            text="Автоматически создавать резервные копии",
            variable=self.auto_backup_var,
            style="TCheckbutton"
        )
        backup_check.pack(anchor="w", pady=(0, 5))

        # Подтверждение перед выходом
        self.confirm_exit_var = tk.BooleanVar(value=self.settings.get("confirm_before_exit", True))
        exit_check = ttk.Checkbutton(
            extra_group,
            text="Подтверждать выход из программы",
            variable=self.confirm_exit_var,
            style="TCheckbutton"
        )
        exit_check.pack(anchor="w", pady=(0, 5))


        # Кнопки управления настройками
        btn_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        btn_frame.pack(pady=20)

        button_configs = [
            ("💾 Сохранить настройки", self.save_settings_ui, "Accent.TButton"),
            ("🔄 Сбросить настройки", self.reset_settings, "TButton"),
            ("📤 Экспортировать настройки", self.export_settings, "TButton"),
            ("📥 Импортировать настройки", self.import_settings, "TButton")
        ]

        for text, command, style in button_configs:
            btn = ttk.Button(
                btn_frame,
                text=text,
                style=style,
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10)

        # Информация о программе
        info_group = ttk.LabelFrame(
            scrollable_frame,
            text="ℹ️ О программе",
            padding=15,
            style="Card.TLabelframe"
        )
        info_group.pack(fill=tk.X, pady=(15, 0))

        info_text = f"""\
🌟 ØccultoNG Pro v{VERSION} • Made with ❤️ by {AUTHOR}
📅 Сборка от: {BUILD_DATE}
🧩 Что внутри?
• Python 3.10+ - платформа приложения
• Pillow - работа с изображениями (PNG/BMP/TIFF/TGA/JPG)
• NumPy + Numba - быстрые битовые операции/индексация
• SciPy (ndimage) - фильтры/карты стоимости для адаптивных методов
• tkinter + tkinterdnd2 - UI и drag‑and‑drop
• wave - чтение/запись PCM‑сэмплов для WAV‑LSB
📦 Контейнеры: PNG • BMP • TIFF • TGA • JPG • WAV
🛡 Методы: LSB • Adaptive‑Noise • AELSB(Hamming) • HILL‑CA • WAV LSB • JPEG DCT
📜 Лицензия: MIT - используйте, модифицируйте, делитесь свободно.
💡 Советы:
• Для изображений - используйте lossless‑форматы (PNG/BMP/TIFF).
• Для аудио - используйте несжатый WAV; любое перекодирование/сжатие может разрушить скрытые биты.
• Регулярно создавайте резервные копии важных файлов.
• Используйте историю для быстрого доступа к недавно использованным файлам.
"""
        info_label = ttk.Label(
            info_group,
            text=info_text,
            justify=tk.LEFT,
            font=("Segoe UI", 9),
            style="Secondary.TLabel"
        )
        info_label.pack(anchor="w")

    def create_statistics_tab(self) -> None:
        self.statistics_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.statistics_tab, text="📊 Статистика")

        # Создаем canvas с прокруткой
        stats_canvas = tk.Canvas(self.statistics_tab, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(self.statistics_tab, orient="vertical", command=stats_canvas.yview)
        scrollable_frame = ttk.Frame(stats_canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: stats_canvas.configure(scrollregion=stats_canvas.bbox("all"))
        )

        stats_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        stats_canvas.configure(yscrollcommand=scrollbar.set)

        stats_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Общая статистика
        summary_group = ttk.LabelFrame(
            scrollable_frame,
            text="📈 Общая статистика",
            padding=15,
            style="Card.TLabelframe"
        )
        summary_group.pack(fill=tk.X, pady=(0, 15))

        # Получаем статистику
        summary = self.analytics_manager.get_summary()
        log_stats = self.log_manager.get_statistics()

        # Создаем информационные метки
        stats_info = [
            ("Всего операций", log_stats.get("total_operations", 0)),
            ("Успешных операций", log_stats.get("successful_operations", 0)),
            ("Операций с ошибками", log_stats.get("failed_operations", 0)),
            ("Процент успешных", f"{log_stats.get('success_rate', 0):.1f}%"),
            ("Операций скрытия", log_stats.get("operation_stats", {}).get("hide", {}).get("total", 0)),
            ("Операций извлечения", log_stats.get("operation_stats", {}).get("extract", {}).get("total", 0)),
            ("Последняя операция", log_stats.get("last_operation", "Никогда")),
            ("Сессий использования", self.analytics_manager.stats.get("sessions", 0)),
            ("Самый популярный метод", summary.get("most_used_method", "Нет данных")),
            ("Самый часто скрываемый тип файлов", summary.get("most_hidden_file_type", "Нет данных"))
        ]

        for i, (label, value) in enumerate(stats_info):
            row_frame = ttk.Frame(summary_group, style="Card.TFrame")
            row_frame.pack(fill=tk.X, pady=(5, 0))

            ttk.Label(
                row_frame,
                text=f"{label}:",
                font=("Segoe UI", 10, "bold"),
                style="TLabel"
            ).pack(side=tk.LEFT, padx=(0, 10))

            ttk.Label(
                row_frame,
                text=str(value),
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            ).pack(side=tk.LEFT)

        # График использования методов
        methods_group = ttk.LabelFrame(
            scrollable_frame,
            text="📊 Статистика по методам",
            padding=15,
            style="Card.TLabelframe"
        )
        methods_group.pack(fill=tk.X, pady=(0, 15))

        methods_data = self.analytics_manager.stats.get("methods_used", {})
        if methods_data:
            for method, count in methods_data.items():
                method_name = STEGANO_METHODS.get(method, method)
                method_frame = ttk.Frame(methods_group, style="Card.TFrame")
                method_frame.pack(fill=tk.X, pady=(2, 2))

                ttk.Label(
                    method_frame,
                    text=f"{method_name}:",
                    style="TLabel"
                ).pack(side=tk.LEFT, padx=(0, 10))

                # Прогресс-бар для метода
                progress = ttk.Progressbar(
                    method_frame,
                    orient="horizontal",
                    length=200,
                    mode="determinate",
                    style="TProgressbar"
                )
                progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

                # Рассчитываем процент от общего числа операций
                total = sum(methods_data.values())
                percentage = (count / total * 100) if total > 0 else 0
                progress["value"] = percentage

                ttk.Label(
                    method_frame,
                    text=f"{count} ({percentage:.1f}%)",
                    style="Secondary.TLabel"
                ).pack(side=tk.RIGHT)
        else:
            ttk.Label(
                methods_group,
                text="Нет данных для отображения",
                style="Secondary.TLabel"
            ).pack(pady=10)

        # История операций
        history_group = ttk.LabelFrame(
            scrollable_frame,
            text="📋 История операций",
            padding=15,
            style="Card.TLabelframe"
        )
        history_group.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Получаем последние операции
        recent_operations = self.log_manager.get_entries(20)

        if recent_operations:
            # Создаем текстовое поле для истории
            history_text = scrolledtext.ScrolledText(
                history_group,
                height=15,
                font=("Consolas", 9),
                wrap=tk.WORD,
                bg=self.colors["card"],
                fg=self.colors["text"],
                insertbackground=self.colors["fg"],
                selectbackground=self.colors["accent"],
                selectforeground="#ffffff",
                relief="flat",
                borderwidth=1
            )
            history_text.pack(fill=tk.BOTH, expand=True)

            # Заполняем историю
            for op in recent_operations:
                status_icon = "✅" if op["status"] == "success" else "❌"
                status_color = "success" if op["status"] == "success" else "error"

                history_text.insert(tk.END, f"{status_icon} {op['formatted_time']} | ", status_color)
                history_text.insert(tk.END, f"{op['operation_type']} | ")
                history_text.insert(tk.END, f"{op['status']}")

                # Добавляем детали если есть
                if op["details"]:
                    details_str = " | ".join([f"{k}: {v}" for k, v in op["details"].items()])
                    history_text.insert(tk.END, f"  Детали: {details_str}")

                history_text.insert(tk.END, "-" * 80 + "")

            # Настраиваем теги для цветов
            history_text.tag_configure("success", foreground=self.colors["success"])
            history_text.tag_configure("error", foreground=self.colors["error"])
            history_text.config(state='disabled')
        else:
            ttk.Label(
                history_group,
                text="История операций пуста",
                style="Secondary.TLabel"
            ).pack(pady=10)

        # Кнопки управления статистикой
        btn_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="🔄 Обновить статистику",
            style="TButton",
            command=self.refresh_statistics
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame,
            text="📤 Экспортировать статистику",
            style="TButton",
            command=self.export_statistics
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame,
            text="🗑️ Очистить историю",
            style="TButton",
            command=self.clear_statistics
        ).pack(side=tk.LEFT, padx=10)

    def create_help_tab(self) -> None:
        self.help_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.help_tab, text="❓ Помощь")

        # Создаем основную сетку с двумя колонками
        main_container = ttk.Frame(self.help_tab, style="Card.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Настраиваем сетку для левой и правой колонок
        main_container.grid_columnconfigure(0, weight=1)  # Левая колонка с содержанием - теперь больше
        main_container.grid_columnconfigure(1, weight=3)  # Правая колонка с текстом - увеличена в 3 раза
        main_container.grid_rowconfigure(0, weight=1)

        # ЛЕВАЯ КОЛОНКА - СОДЕРЖАНИЕ
        left_frame = ttk.LabelFrame(
            main_container,
            text="📋 Содержание",
            padding=15,
            style="Card.TLabelframe"
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Список разделов помощи
        contents = [
            ("1. Введение", self.show_help_intro),
            ("2. Поддерживаемые методы", self.show_help_methods),
            ("3. Быстрый старт", self.show_help_quickstart),
            ("4. Пакетная обработка", self.show_help_batch),
            ("5. 🔐 Шифрование данных", self.show_help_encryption),
            ("6. Советы и рекомендации", self.show_help_tips),
            ("7. Горячие клавиши", self.show_help_shortcuts),
            ("8. Часто задаваемые вопросы", self.show_help_faq),
            ("9. Техническая поддержка", self.show_help_support)
        ]

        for i, (title, command) in enumerate(contents):
            btn = ttk.Button(
                left_frame,
                text=title,
                style="CardButton.TButton",
                command=command
            )
            btn.pack(fill=tk.X, pady=2)

        # Добавим кнопку поиска внизу левой колонки
        search_btn = ttk.Button(
            left_frame,
            text="🔍 Поиск в помощи",
            style="IconButton.TButton",
            command=self.search_help
        )
        search_btn.pack(fill=tk.X, pady=(20, 5))

        # ПРАВАЯ КОЛОНКА - ТЕКСТ ПОМОЩИ (УВЕЛИЧЕННАЯ)
        right_frame = ttk.LabelFrame(
            main_container,
            text="📚 Информация",
            padding=10,  # Уменьшим отступы, чтобы было больше места для текста
            style="Card.TLabelframe"
        )
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Используем ScrolledText для отображения текста помощи
        self.help_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            font=("Segoe UI", 10),
            padx=15,
            pady=15,
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.help_text.grid(row=0, column=0, sticky="nsew")

        # Создаем теги для форматирования
        self.help_text.tag_configure("title", font=("Segoe UI", 16, "bold"), foreground=self.colors["accent"])
        self.help_text.tag_configure("subtitle", font=("Segoe UI", 12, "bold"), foreground=self.colors["text"])
        self.help_text.tag_configure("normal", font=("Segoe UI", 10), foreground=self.colors["text"])
        self.help_text.tag_configure("tip", font=("Segoe UI", 10), foreground=self.colors["success"])
        self.help_text.tag_configure("warning", font=("Segoe UI", 10), foreground=self.colors["warning"])
        self.help_text.tag_configure("error", font=("Segoe UI", 10), foreground=self.colors["error"])
        self.help_text.tag_configure("code", font=("Consolas", 9), background=self.colors["secondary"])

        # Отключаем редактирование
        self.help_text.config(state='disabled')

        # ПАНЕЛЬ КНОПОК ВНИЗУ ПРАВОЙ КОЛОНКИ
        bottom_frame = ttk.Frame(right_frame, style="Card.TFrame")
        bottom_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        ttk.Button(
            bottom_frame,
            text="📥 Скачать PDF",
            style="IconButton.TButton",
            command=self.download_help_pdf
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            bottom_frame,
            text="📝 Отправить отзыв",  # Измененный текст
            style="IconButton.TButton",
            command=self.send_feedback  # Эта команда уже правильно указана
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            bottom_frame,
            text="🔄 Обновить",
            style="IconButton.TButton",
            command=self.refresh_help
        ).pack(side=tk.RIGHT, padx=5)

        # Показываем введение по умолчанию
        self.show_help_intro()

    def refresh_help(self):
        """Обновляет текст помощи"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == self.notebook.index(self.help_tab):
            # Если мы на вкладке помощи, обновляем текст
            self.show_help_intro()
            messagebox.showinfo("Обновление", "Текст помощи обновлен!")

    def show_help_intro(self):
        """Показывает введение в помощь"""
        help_text = f"""
    🎯 Добро пожаловать в ØccultoNG Pro v{VERSION}!

    ØccultoNG Pro - это профессиональный инструмент для стеганографии,
    позволяющий скрывать тексты и файлы внутри изображений и аудиофайлов
    без потерь, с автоматическим извлечением и проверкой целостности.

    🚀 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
    • Поддержка различных методов скрытия данных
    • Работа с изображениями (PNG, BMP, TIFF, TGA, JPG) и аудио (WAV)
    • Автоматическое определение метода при извлечении
    • Пакетная обработка до 5 файлов одновременно
    • Расширенная статистика
    • Поддержка плагинов и расширений

    📋 ОСНОВНЫЕ ВКЛАДКИ:
    1. 📦 Скрыть данные - скрытие данных в одном контейнере
    2. 🔍 Извлечь данные - извлечение скрытых данных
    3. 📦 Пакетная обработка - одновременная обработка до 5 файлов
    4. ⚙️ Настройки - настройка программы и темы
    5. 📊 Статистика - просмотр статистики использования
    6. ❓ Помощь - это окно с руководством

    💡 СОВЕТ: Начните с выбора вкладки "Скрыть данные" или "Извлечь данные"
    в верхней части окна. Для работы с несколькими файлами используйте
    вкладку "Пакетная обработка".

    📈 СТАТИСТИКА: Отслеживайте свою активность и прогресс!
    """
        self.display_help_text(help_text)

    def show_help_batch(self):
        """Показывает помощь по пакетной обработке"""
        help_text = """
    📦 ПАКЕТНАЯ ОБРАБОТКА ФАЙЛОВ

    ØccultoNG Pro теперь поддерживает пакетную обработку до 5 файлов одновременно!
    Это позволяет значительно ускорить работу при необходимости обработки
    нескольких файлов.

    🚀 ВОЗМОЖНОСТИ ПАКЕТНОЙ ОБРАБОТКИ:
    • Скрытие данных в до 5 контейнерах одновременно
    • Извлечение данных из до 5 стего-файлов одновременно
    • Анализ до 5 файлов на наличие скрытых данных
    • Автоматическое сохранение результатов
    • Экспорт результатов обработки в JSON
    • Отслеживание прогресса в реальном времени

    📋 ТРИ РЕЖИМА РАБОТЫ:

    1. 📤 ПАКЕТНОЕ СКРЫТИЕ:
       • Выберите до 5 файлов-контейнеров
       • Укажите данные для скрытия (текст или файл)
       • Выберите метод и настройки
       • Начните обработку - все файлы будут обработаны автоматически

    2. 📥 ПАКЕТНОЕ ИЗВЛЕЧЕНИЕ:
       • Выберите до 5 стего-файлов
       • Укажите пароль (если требуется)
       • Выберите метод или используйте автоопределение
       • Результаты будут сохранены автоматически

    3. 🔍 ПАКЕТНЫЙ АНАЛИЗ:
       • Выберите до 5 файлов для анализа
       • Программа проверит наличие скрытых данных
       • Покажет информацию о вместимости контейнеров
       • Определит тип возможных скрытых данных

    🎯 ПРЕИМУЩЕСТВА ПАКЕТНОЙ ОБРАБОТКИ:
    • Экономия времени - не нужно обрабатывать каждый файл отдельно
    • Единые настройки для всех файлов
    • Автоматическое создание резервных копий
    • Подробный отчет о результатах
    • Возможность экспорта результатов

    ⚠️ ОГРАНИЧЕНИЯ:
    • Максимум 5 файлов за одну операцию
    • Все файлы обрабатываются с одинаковыми настройками
    • Для скрытия используется один набор данных для всех файлов
    • Требуется достаточно свободного места на диске

    💡 СОВЕТЫ ПО ИСПОЛЬЗОВАНИЮ:
    1. Убедитесь, что все выбранные файлы имеют одинаковый формат
    2. Проверьте достаточно ли свободного места на диске
    3. Используйте автоматическое резервное копирование
    4. Экспортируйте результаты для дальнейшего анализа
    5. Следите за прогрессом в статусной панели

    🔧 РЕШЕНИЕ ПРОБЛЕМ:
    • Если кнопки остаются заблокированными - нажмите "Очистить все"
    • Если обработка зависла - используйте кнопку "Остановить обработку"
    • Если файлы не обрабатываются - проверьте формат и права доступа
    • Для повторной обработки тех же файлов - очистите список и добавьте заново

    📊 ЭКСПОРТ РЕЗУЛЬТАТОВ:
    После завершения обработки вы можете экспортировать результаты в JSON:
    1. Нажмите "Экспорт результатов"
    2. Выберите место сохранения
    3. JSON-файл будет содержать:
       • Дату и время обработки
       • Статистику (успешно/ошибки)
       • Подробную информацию по каждому файлу
       • Настройки, использованные при обработке

    🚀 БЫСТРЫЙ СТАРТ:
    1. Перейдите на вкладку "📦 Пакетная обработка"
    2. Выберите нужный режим (скрытие/извлечение/анализ)
    3. Добавьте файлы (до 5 штук)
    4. Настройте параметры
    5. Нажмите соответствующую кнопку запуска
    6. Дождитесь завершения обработки
    7. Просмотрите или экспортируйте результаты
    """
        self.display_help_text(help_text)

    def show_help_methods(self):
        """Показывает информацию о методах"""
        help_text = """
🧩 Поддерживаемые методы скрытия данных

1) 🟢 Классический LSB (Макс. вместимость)
• Плюсы: максимальная вместимость и скорость
• Минусы: проще обнаружить стеганализом
• Рекомендуется для: больших объемов данных, когда важна вместимость

2) 🟡 Adaptive-Noise (Баланс вместимости/скрытности)
• Плюсы: лучше маскирует изменения, та же вместимость, что и LSB
• Минусы: чуть медленнее
• Рекомендуется для: баланса между вместимостью и скрытностью

3) 🔵 Adaptive-Edge-LSB + Hamming(7,3) (Устойчивость к ошибкам)
• Плюсы: устойчивость к шумам/ошибкам благодаря избыточности
• Минусы: вместимость ≈ 3/7 от классического LSB
• Рекомендуется для: условий с возможными помехами

4) 🟣 HILL-CA LSB Matching (Макс. скрытность)
• Плюсы: контент-адаптивный выбор позиций → лучшая скрытность
• Минусы: ниже скорость и вместимость
• Рекомендуется для: максимальной скрытности, когда важна незаметность

5) 🎵 WAV LSB (Аудио контейнеры)
• Идея: изменяются младшие биты PCM-сэмплов в WAV
• Плюсы: простота и прозрачность на слух при 1 LSB/сэмпл
• Минусы: уязвимость к сжатию/пересэмплированию
• Рекомендуется для: аудиофайлов, когда важна аудио-качество

6) 🖼️ JPEG DCT (Стойкость к сжатию)
• Идея: изменение среднечастотных коэффициентов DCT в блоках 8x8
• Плюсы: устойчивость к JPEG-сжатию, незаметность изменений
• Минусы: низкая вместимость (≈1 бит на блок 8x8)
• Рекомендуется для: JPEG изображений, когда важна совместимость
"""
        self.display_help_text(help_text)

    def show_help_quickstart(self):
        """Показывает быстрый старт"""
        help_text = """
    🚀 БЫСТРЫЙ СТАРТ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ОСНОВНАЯ РАБОТА:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Скрыть данные в изображении:
    1. Перейдите на вкладку "📦 Скрыть данные"
    2. Выберите изображение-контейнер (PNG/BMP/TIFF/TGA/JPG)
    3. Выберите тип данных: текст или файл
    4. Введите текст или выберите файл для скрытия
    5. Выберите метод скрытия (рекомендуется начать с "Классический LSB")
    6. Нажмите "🔐 Скрыть данные в изображении"
    7. Выберите место сохранения и имя файла

    Скрыть данные в аудио:
    1. Перейдите на вкладку "📦 Скрыть данные"
    2. Выберите аудиофайл WAV
    3. Выберите тип данных: текст или файл
    4. Введите текст или выберите файл для скрытия
    5. Метод автоматически изменится на "WAV LSB"
    6. Нажмите "🔐 Скрыть данные"
    7. Выберите место сохранения и имя файла

    Извлечь данные:
    1. Перейдите на вкладку "🔍 Извлечь данные"
    2. Выберите изображение или аудиофайл со скрытыми данными
    3. Нажмите "🔍 Извлечь данные"
    4. Дождитесь завершения операции
    5. Скопируйте или сохраните извлеченные данные

    🔐 ШИФРОВАНИЕ ДАННЫХ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Перейдите на вкладку "🔐 Шифрование"
    2. Выберите тип данных: текст или файл
    3. Введите текст или выберите файл для шифрования
    4. Выберите алгоритм (рекомендуется AES-256 GCM)
    5. Введите надежный пароль (минимум 8 символов)
    6. Нажмите "🔐 Зашифровать"
    7. Сохраните результат в файл .ongcrypt

    ДЕШИФРОВАНИЕ ДАННЫХ:
    1. Перейдите на вкладку "🔐 Шифрование"
    2. Вставьте зашифрованные данные или загрузите файл
    3. Введите пароль
    4. Нажмите "🔓 Расшифровать"
    5. Скопируйте или сохраните результат

    Подробнее о шифровании см. раздел "🔐 Шифрование данных" в содержании.

    📦 ПАКЕТНАЯ ОБРАБОТКА:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Пакетное скрытие (до 5 файлов):
    1. Перейдите на вкладку "📦 Пакетная обработка"
    2. Выберите вкладку "📤 Скрытие"
    3. Добавьте до 5 файлов-контейнеров
    4. Выберите тип данных и введите текст/выберите файл
    5. Настройте метод и параметры
    6. Нажмите "🚀 Начать пакетное скрытие"
    7. Дождитесь завершения обработки всех файлов

    Пакетное извлечение (до 5 файлов):
    1. Перейдите на вкладку "📦 Пакетная обработка"
    2. Выберите вкладку "📥 Извлечение"
    3. Добавьте до 5 стего-файлов
    4. Введите пароль (если требуется)
    5. Нажмите "🚀 Начать пакетное извлечение"
    6. Результаты будут сохранены автоматически

    Пакетный анализ (до 5 файлов):
    1. Перейдите на вкладку "📦 Пакетная обработка"
    2. Выберите вкладку "🔍 Анализ"
    3. Добавьте до 5 файлов для проверки
    4. Нажмите "🔍 Начать анализ"
    5. Просмотрите результаты в поле ниже

    ⚡ ПРОДВИНУТЫЕ ВОЗМОЖНОСТИ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Расширенная статистика:
    • Отслеживание всех операций
    • Анализ использования методов
    • История успешных и неудачных операций
    • Визуализация данных

    💡 СОВЕТЫ:
    • Используйте сочетания клавиш для ускорения работы!
    • Регулярно сохраняйте настройки
    • Создавайте резервные копии важных файлов
    • Экспортируйте результаты для отчетности
    • Используйте пакетную обработку для экономии времени

    """
        self.display_help_text(help_text)

    def show_help_tips(self):
        """Показывает советы и рекомендации"""
        help_text = """
    💡 СОВЕТЫ И РЕКОМЕНДАЦИИ

    🎯 ОБЩИЕ СОВЕТЫ:
    • Используйте lossless-форматы (PNG/BMP/TIFF) для максимального качества
      скрытия данных. Форматы с потерями (JPEG) могут повредить скрытую информацию.

    • Для аудио используйте несжатый WAV. Любое перекодирование или сжатие
      может разрушить скрытые биты.

    • Метод HILL-CA обеспечивает максимальную скрытность, но имеет меньшую
      вместимость. Используйте его когда важна незаметность.

    • Метод Adaptive-Noise лучше маскирует изменения в изображении.
      Хороший баланс между вместимостью и скрытностью.

    • Для больших файлов используйте классический LSB для максимальной
      вместимости.

    📦 СОВЕТЫ ПО ПАКЕТНОЙ ОБРАБОТКЕ:
    • Перед пакетной обработкой проверьте, что все файлы имеют одинаковый формат
    • Убедитесь в наличии достаточного свободного места на диске
    • Используйте одну и ту же папку для сохранения результатов
    • Экспортируйте результаты обработки для ведения учета
    • Ограничение в 5 файлов установлено для стабильности работы
    • Если нужно обработать больше файлов - разбейте на несколько партий

    🔐 СОВЕТЫ ПО БЕЗОПАСНОСТИ:
    • Всегда используйте пароли для конфиденциальных данных
    • Регулярно создавайте резервные копии важных файлов
    • Проверяйте контрольные суммы извлеченных файлов
    • Используйте разные пароли для разных операций
    • Храните пароли в безопасном месте

    ⚡ СОВЕТЫ ПО ПРОИЗВОДИТЕЛЬНОСТИ:
    • Закрывайте другие ресурсоемкие приложения во время обработки
    • Для пакетной обработки используйте SSD-диски для скорости
    • При работе с большими файлами увеличьте размер файла подкачки
    • Регулярно очищайте временные файлы программы

    🔄 СОВЕТЫ ПО НАСТРОЙКАМ:
    • Настройте тему интерфейса под свои предпочтения
    • Включите автоматическое резервное копирование
    • Настройте горячие клавиши для часто используемых операций
    • Используйте историю операций для быстрого доступа
    • Регулярно обновляйте программу для получения новых функций

    📊 СОВЕТЫ ПО СТАТИСТИКЕ:
    • Регулярно проверяйте статистику использования
    • Анализируйте наиболее часто используемые методы
    • Используйте историю операций для отладки проблем
    • Экспортируйте статистику для отчетов

    🚀 ПРОДВИНУТЫЕ СОВЕТЫ:
    • Комбинируйте разные методы для разных типов данных
    • Используйте сжатие данных перед скрытием для экономии места
    • Экспериментируйте с разными типами контейнеров
    • Тестируйте извлечение на разных устройствах
    • Документируйте использованные настройки для повторения
    """
        self.display_help_text(help_text)

    def show_help_shortcuts(self):
        """Показывает горячие клавиши"""
        help_text = """
    ⌨️ ГОРЯЧИЕ КЛАВИШИ

    ОСНОВНЫЕ:
    • F1 - Открыть помощь
    • Esc - Отменить текущую операцию
    • Ctrl+Enter - Выполнить основное действие на активной вкладке
    • Ctrl+O - Выбрать контейнер (на активной вкладке)
    • Ctrl+E - Извлечь данные
    • Ctrl+S - Сохранить извлеченные данные
    • Ctrl+L - Очистить текстовое поле
    • Ctrl+T - Переключить тему

    НА ВКЛАДКЕ "СКРЫТЬ ДАННЫЕ":
    • Ctrl+1 - Выбрать метод "Классический LSB"
    • Ctrl+2 - Выбрать метод "Adaptive-Noise"
    • Ctrl+3 - Выбрать метод "Adaptive-Edge-LSB"
    • Ctrl+4 - Выбрать метод "HILL-CA"
    • Ctrl+5 - Выбрать метод "WAV LSB"
    • Ctrl+6 - Выбрать метод "JPEG DCT"

    НА ВКЛАДКЕ "ИЗВЛЕЧЬ ДАННЫЕ":
    • Ctrl+R - Обновить предпросмотр
    • Ctrl+C - Копировать извлеченные данные
    • Ctrl+H - Копировать хеш извлеченных данных
    • Ctrl+F - Найти в извлеченных данных

    НА ВКЛАДКЕ "ПАКЕТНАЯ ОБРАБОТКА" (НОВОЕ!):
    • Ctrl+B - Переключиться на вкладку пакетной обработки
    • Ctrl+Shift+H - Быстрый доступ к пакетному скрытию
    • Ctrl+Shift+E - Быстрый доступ к пакетному извлечению
    • Ctrl+Shift+A - Быстрый доступ к пакетному анализу
    • Ctrl+Shift+C - Очистить все списки в пакетной обработке
    • Ctrl+Shift+X - Экспорт результатов пакетной обработки

    ОБЩИЕ:
    • Ctrl+Tab - Переключиться на следующую вкладку
    • Ctrl+Shift+Tab - Переключиться на предыдущую вкладку
    • Ctrl+, - Открыть настройки
    • Ctrl+Q - Выйти из программы
    • Ctrl+Shift+S - Открыть статистику

    РАБОТА С ФАЙЛАМИ:
    • Ctrl+N - Создать новый проект
    • Ctrl+O - Открыть файл
    • Ctrl+Shift+O - Открыть несколько файлов (пакетная обработка)
    • Ctrl+W - Закрыть текущий файл
    • Ctrl+Shift+W - Закрыть все файлы

    РЕДАКТИРОВАНИЕ:
    • Ctrl+Z - Отменить
    • Ctrl+Y - Повторить
    • Ctrl+X - Вырезать
    • Ctrl+C - Копировать
    • Ctrl+V - Вставить
    • Ctrl+A - Выделить все
    • Ctrl+F - Найти
    • Ctrl+H - Заменить

    ПРОСМОТР:
    • Ctrl++ - Увеличить масштаб
    • Ctrl+- - Уменьшить масштаб
    • Ctrl+0 - Сбросить масштаб
    • F11 - Полноэкранный режим
    • Alt+Enter - Свойства файла

    СИСТЕМНЫЕ:
    • Alt+F4 - Закрыть программу
    • Alt+Tab - Переключение между приложениями
    • Win+D - Показать рабочий стол
    • Win+E - Открыть проводник

    💡 СОВЕТ: Горячие клавиши можно изменить в настройках программы.
    """
        self.display_help_text(help_text)

    def show_help_faq(self):
        """Показывает часто задаваемые вопросы"""
        help_text = """
    ❓ ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ

    Q: Что делать, если данные не извлекаются?
    A: Попробуйте следующее:
       1. Убедитесь, что используете правильный файл-контейнер
       2. Попробуйте другой метод извлечения
       3. Проверьте, не был ли файл изменен после скрытия данных
       4. Убедитесь, что пароль (если используется) введен правильно
       5. Попробуйте извлечь данные на другом устройстве

    Q: Почему мой большой файл не помещается в контейнер?
    A: Каждый метод имеет ограничения по вместимости:
       • Классический LSB: максимальная вместимость
       • Adaptive-Noise: такая же вместимость, как у LSB
       • AELSB/HILL: вместимость примерно 3/7 от LSB
       Попробуйте:
       1. Использовать контейнер большего размера
       2. Выбрать метод с большей вместимостью
       3. Сжать файл перед скрытием

    Q: Можно ли использовать JPEG как контейнер?
    A: Технически можно, но не рекомендуется. JPEG использует сжатие
       с потерями, которое может повредить скрытые данные. Лучше
       использовать lossless-форматы: PNG, BMP, TIFF.

    Q: Как проверить целостность извлеченных данных?
    A: Программа автоматически проверяет контрольную сумму (CRC32).
       Также вы можете сравнить хеш SHA-256 извлеченных данных
       с оригиналом.

    Q: Можно ли скрывать данные в уже модифицированных файлах?
    A: Да, но с осторожностью. Каждая модификация файла может
       повредить скрытые данные. Лучше использовать оригинальные
       файлы-контейнеры.

    Q: Как восстановить данные, если что-то пошло не так?
    A: Если включено автоматическое создание резервных копий,
       проверьте папку "backups" в директории с файлом. Также
       можно попробовать извлечь данные другим методом.

    📦 ВОПРОСЫ ПО ПАКЕТНОЙ ОБРАБОТКЕ:

    Q: Почему ограничение в 5 файлов?
    A: Ограничение установлено для:
       1. Стабильности работы программы
       2. Предотвращения перегрузки системы
       3. Удобства управления процессом
       4. Оптимизации использования памяти

    Q: Что делать, если кнопки пакетной обработки заблокировались?
    A: Нажмите кнопку "Очистить все" или переключитесь на другую
       вкладку и обратно. Если не помогает - перезапустите программу.

    Q: Как обработать больше 5 файлов?
    A: Разделите файлы на группы по 5 штук и обработайте каждую
       группу отдельно. Используйте экспорт результатов для
       объединения отчетов.

    Q: Почему пакетное извлечение не работает, хотя по отдельности работает?
    A: Возможные причины:
       1. Разные пароли для разных файлов
       2. Разные методы скрытия в файлах
       3. Повреждение некоторых файлов
       4. Недостаточно прав доступа

    Q: Как отменить пакетную обработку?
    A: Нажмите кнопку "⏹️ Остановить обработку" в статусной панели.
       Обработка остановится после завершения текущего файла.

    Q: Где сохраняются результаты пакетной обработки?
    A: Результаты сохраняются в указанную вами папку. Каждому файлу
       присваивается уникальное имя на основе исходного имени.

    ⚙️ ТЕХНИЧЕСКИЕ ВОПРОСЫ:

    Q: Какие системные требования?
    A: Минимальные требования:
       • Windows 7 / macOS 10.12 / Ubuntu 18.04
       • 2 ГБ оперативной памяти
       • 100 МБ свободного места
       • Python 3.8+ (уже включен в сборку)

    Q: Как обновить программу?
    A: Скачайте новую версию с официального сайта и установите поверх
       старой. Настройки и история сохранятся.

    Q: Где хранятся настройки программы?
    A: Настройки хранятся в файле "stego_settings_pro.json" в папке
       с программой или в домашней директории пользователя.
    """
        self.display_help_text(help_text)

    def show_help_support(self):
        """Показывает информацию о технической поддержке"""
        help_text = f"""
✉️ Техническая поддержка

Если у вас возникли проблемы или есть предложения по улучшению,
вы можете связаться с нами:

📧 Email: tudubambam@ya.ru
🌐 Сайт: www.occulto.pro

🕒 Время ответа: обычно в течение 24 часов

💡 Перед обращением в поддержку, пожалуйста:
1. Проверьте, актуальна ли ваша версия программы (v{VERSION})
2. Попробуйте перезапустить программу
3. Проверьте, воспроизводится ли проблема на другом файле
4. Подготовьте подробное описание проблемы
5. Приложите файлы логов (если есть)

🔧 Файлы логов находятся в директории программы:
• stego_analytics.json - статистика использования
• stego_history_pro.json - история операций
• operation_log.json - подробный журнал операций

🙏 Благодарим за использование ØccultoNG Pro!
Ваше мнение помогает нам улучшать продукт.
"""
        self.display_help_text(help_text)

    def show_help_encryption(self):
        """Показывает подробную инструкцию по использованию вкладки шифрования"""
        help_text = f"""
    🔐 ПОДРОБНОЕ РУКОВОДСТВО ПО ШИФРОВАНИЮ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ОБЩАЯ ИНФОРМАЦИЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Вкладка "🔐 Шифрование" предоставляет профессиональные инструменты для
    защиты ваших данных с использованием современных криптографических алгоритмов.

    ОСНОВНЫЕ ВОЗМОЖНОСТИ:
    • Шифрование текста и файлов
    • Дешифрование зашифрованных данных
    • Поддержка 8 современных алгоритмов шифрования
    • Автоматическое определение алгоритма при загрузке
    • Сохранение зашифрованных данных в формате .ongcrypt
    • Подробная документация по каждому алгоритму

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ШИФРОВАНИЕ ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ШАГ 1: ВЫБОР ТИПА ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    В левой колонке выберите тип данных для шифрования:

    1️⃣ ТЕКСТ (по умолчанию)
    • Нажмите радиокнопку "Текст"
    • Введите или вставьте текст в поле ввода
    • Используйте кнопки на панели инструментов:
      • 📋 Вставить - вставить из буфера обмена (Ctrl+V)
      • 🗑️ Очистить - очистить поле ввода
      • 📝 Шаблоны - использовать готовые шаблоны текста

    2️⃣ ФАЙЛ
    • Нажмите радиокнопку "Файл"
    • Нажмите кнопку "📂 Выбрать..."
    • Выберите файл любого формата (до 100 МБ)
    • Информация о файле отобразится под полем выбора

    ШАГ 2: ВЫБОР АЛГОРИТМА ШИФРОВАНИЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Из выпадающего списка выберите алгоритм шифрования:

    РЕКОМЕНДУЕМЫЕ АЛГОРИТМЫ (высокая безопасность):
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🟢 AES-256 GCM (рекомендуется по умолчанию)
    • Самый безопасный вариант для большинства задач
    • Встроенная аутентификация данных
    • Высокая скорость на современных процессорах
    • Используется в банковских и военных системах

    🟢 AES-256 CBC
    • Стандартный алгоритм, широко используемый в индустрии
    • Хороший баланс между безопасностью и производительностью
    • Требует надежного пароля

    🟢 ChaCha20-Poly1305
    • Отличный выбор для мобильных устройств
    • Высокая скорость на CPU без аппаратного ускорения AES
    • Используется в TLS 1.3 и современных мессенджерах

    ДРУГИЕ АЛГОРИТМЫ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🟡 AES-256 CTR
    • Потоковый режим, поддерживает параллельную обработку
    • Очень высокая скорость
    • Требует уникального nonce для каждого шифрования

    🟡 AES-256 OFB
    • Устаревший режим, не рекомендуется для новых систем
    • Используйте только для совместимости со старыми системами

    🔴 XOR (ТОЛЬКО ДЛЯ ОБУЧЕНИЯ!)
    • НЕ ОБЕСПЕЧИВАЕТ РЕАЛЬНУЮ БЕЗОПАСНОСТЬ
    • Тривиально взламывается
    • Используйте только для образовательных целей

    🔴 Base64 (НЕ ШИФРОВАНИЕ!)
    • Это просто кодирование, НЕ шифрование
    • Данные легко декодируются без пароля
    • Используйте только для передачи бинарных данных в текстовых протоколах

    ШАГ 3: ВВОД ПАРОЛЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Для надежных алгоритмов (AES, ChaCha20) требуется пароль:

    ТРЕБОВАНИЯ К ПАРОЛЮ:
    • Минимум 8 символов (рекомендуется 12+)
    • Используйте смешанные регистры (заглавные и строчные буквы)
    • Добавьте цифры и специальные символы (!@#$%^&*)
    • Избегайте словарных слов и личной информации
    • Используйте уникальный пароль для каждой операции

    ПРИМЕРЫ ХОРОШИХ ПАРОЛЕЙ:
    • J7$mP9#kL2@nQ5
    • BlueDragon42!MountainSky
    • 9T$hK3pL8@wN5vX

    ПРИМЕРЫ ПЛОХИХ ПАРОЛЕЙ:
    • password123 (слишком простой)
    • qwerty (словарное слово)
    • 12345678 (только цифры)
    • admin (слишком короткий)

    ПАНЕЛЬ УПРАВЛЕНИЯ ПАРОЛЕМ:
    • Поле ввода пароля скрывает символы (●●●●●)
    • Чекбокс "Показать" позволяет временно увидеть пароль
    • ВНИМАНИЕ: никогда не показывайте пароль на публике!

    ШАГ 4: ВЫПОЛНЕНИЕ ШИФРОВАНИЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Нажмите кнопку "🔐 Зашифровать"

    ЧТО ПРОИСХОДИТ:
    1. Программа проверяет корректность введенных данных
    2. Генерируется случайная "соль" (salt) для защиты от атак по радужным таблицам
    3. Из пароля с помощью PBKDF2-HMAC-SHA256 (600 000 итераций) генерируется 256-битный ключ
    4. Данные шифруются выбранным алгоритмом
    5. Для некоторых алгоритмов генерируется контрольная сумма или тег аутентификации
    6. Результат сериализуется в формат JSON с метаданными

    РЕЗУЛЬТАТ:
    • Зашифрованные данные отображаются в нижнем поле результата
    • Данные представлены в формате JSON с Base64-кодированием бинарных частей
    • Формат включает: алгоритм, версию, временные метки, параметры шифрования

    ШАГ 5: СОХРАНЕНИЕ ЗАШИФРОВАННЫХ ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Нажмите кнопку "💾 Сохранить"

    ВАРИАНТЫ СОХРАНЕНИЯ:
    1️⃣ Формат .ongcrypt (РЕКОМЕНДУЕТСЯ)
    • Специальный формат ØccultoNG Pro
    • Включает магические байты для идентификации
    • Поддерживает все метаданные и параметры
    • Автоматически распознается при загрузке

    2️⃣ Формат JSON
    • Стандартный текстовый формат
    • Может быть открыт в любом текстовом редакторе
    • Подходит для передачи через текстовые каналы

    ПРИМЕР СОДЕРЖИМОГО ФАЙЛА .ongcrypt:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {{
      "algorithm": "aes_256_gcm",
      "version": "1.0",
      "ciphertext": "U2FsdGVkX1+...",
      "salt": "aB3cD4eF5gH6...",
      "nonce": "iJ7kL8mN9oP0...",
      "tag": "qR2sT3uV4wX5...",
      "timestamp": "2026-02-11 14:30:45",
      "format": "occultong_encrypted_v1"
    }}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ДЕШИФРОВАНИЕ ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ШАГ 1: ЗАГРУЗКА ЗАШИФРОВАННЫХ ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    В центральной колонке "🔓 Дешифрование данных":

    СПОСОБ 1: ВСТАВКА ИЗ БУФЕРА ОБМЕНА
    • Скопируйте зашифрованные данные (в формате JSON)
    • Нажмите кнопку "📋 Вставить" на панели инструментов
    • ИЛИ используйте сочетание клавиш Ctrl+V

    СПОСОБ 2: ЗАГРУЗКА ИЗ ФАЙЛА
    • Нажмите кнопку "📂 Загрузить"
    • Выберите файл .ongcrypt или .json
    • Данные автоматически загрузятся в поле ввода

    СПОСОБ 3: РУЧНОЙ ВВОД
    • Скопируйте содержимое файла .ongcrypt
    • Вставьте в поле ввода вручную

    АВТОМАТИЧЕСКОЕ ОПРЕДЕЛЕНИЕ АЛГОРИТМА:
    • Программа автоматически определяет алгоритм из метаданных
    • Информация об алгоритме отображается в документации справа
    • Если формат не распознан - будет показана ошибка

    ШАГ 2: ВВОД ПАРОЛЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Введите тот же пароль, который использовался для шифрования
    • Используйте чекбокс "Показать" для проверки правильности ввода
    • ВНИМАНИЕ: при неверном пароле дешифрование невозможно!

    ШАГ 3: ВЫПОЛНЕНИЕ ДЕШИФРОВАНИЯ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Нажмите кнопку "🔓 Расшифровать"

    ПРОЦЕСС ДЕШИФРОВАНИЯ:
    1. Программа проверяет формат данных
    2. Извлекает метаданные (алгоритм, параметры)
    3. Восстанавливает ключ из пароля и соли
    4. Проверяет целостность данных (контрольная сумма или тег)
    5. Расшифровывает данные
    6. Отображает результат

    ВОЗМОЖНЫЕ ОШИБКИ:
    • "Неверный пароль" - пароль не совпадает с использованным при шифровании
    • "Поврежденные данные" - файл был изменен после шифрования
    • "Несовместимый алгоритм" - алгоритм не поддерживается текущей версией

    ШАГ 4: РАБОТА С РЕЗУЛЬТАТОМ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Результат отображается в нижнем поле:

    ЕСЛИ РЕЗУЛЬТАТ - ТЕКСТ:
    • Текст отображается в читаемом виде
    • Доступны кнопки:
      • 📋 Копировать - скопировать в буфер обмена
      • 💾 Сохранить - сохранить в файл .txt или .json

    ЕСЛИ РЕЗУЛЬТАТ - БИНАРНЫЕ ДАННЫЕ:
    • Отображается информация о типе файла:
      • Тип данных (изображение, аудио, архив и т.д.)
      • Размер файла
      • Хеш SHA-256 для проверки целостности
    • Доступны кнопки:
      • 💾 Сохранить - сохранить в файл с правильным расширением
      • 🗂 Открыть файл - открыть в приложении по умолчанию
      • 🔑 Копировать хеш - скопировать хеш для проверки

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ПОДРОБНАЯ ДОКУМЕНТАЦИЯ ПО АЛГОРИТМАМ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    В правой колонке отображается подробная документация по выбранному алгоритму:

    ИНФОРМАЦИЯ ВКЛЮЧАЕТ:
    1. Полное название алгоритма
    2. Уровень безопасности (цветовая индикация)
    3. Подробное описание принципа работы
    4. Рекомендуемые сценарии использования
    5. Ограничения и предостережения
    6. Технические детали:
       • Ключевая производная функция (KDF)
       • Размер инициализирующего вектора (IV/nonce)
       • Аутентификация данных
       • Производительность

    ЦВЕТОВАЯ ИНДИКАЦИЯ БЕЗОПАСНОСТИ:
    • ✅ Зеленый - Очень высокий уровень безопасности (AES-256 GCM, ChaCha20-Poly1305)
    • 🟢 Синий - Высокий уровень безопасности (AES-256 CBC/CTR, ChaCha20)
    • 🟡 Желтый - Средний уровень безопасности (AES-256 OFB)
    • ⚠️ Оранжевый - Низкий уровень безопасности
    • ❌ Красный - НЕ БЕЗОПАСЕН (XOR, Base64)

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ПРАКТИЧЕСКИЕ ПРИМЕРЫ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ПРИМЕР 1: ШИФРОВАНИЕ КОНФИДЕНЦИАЛЬНОГО ТЕКСТА
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Выберите тип данных: "Текст"
    2. Введите текст: "Код доступа к серверу: XYZ-789-ABC"
    3. Выберите алгоритм: "AES-256 GCM"
    4. Введите надежный пароль: "S3cur3P@ss!2026"
    5. Нажмите "🔐 Зашифровать"
    6. Сохраните результат в файл "secret.ongcrypt"
    7. Удалите исходный текст из поля ввода

    ПРИМЕР 2: ШИФРОВАНИЕ ФАЙЛА С ПАРОЛЯМИ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Выберите тип данных: "Файл"
    2. Выберите файл: "passwords.xlsx"
    3. Выберите алгоритм: "ChaCha20-Poly1305"
    4. Введите пароль: "MyP@ssw0rdM@n@g3r!2026"
    5. Нажмите "🔐 Зашифровать"
    6. Сохраните в "passwords.ongcrypt"
    7. Храните пароль в надежном менеджере паролей

    ПРИМЕР 3: ДЕШИФРОВАНИЕ ПОЛУЧЕННЫХ ДАННЫХ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Получите файл "message.ongcrypt" от отправителя
    2. Нажмите "📂 Загрузить" и выберите файл
    3. Введите пароль, полученный от отправителя (безопасным каналом!)
    4. Нажмите "🔓 Расшифровать"
    5. Проверьте результат
    6. Скопируйте или сохраните расшифрованный текст

    ПРИМЕР 4: ПЕРЕДАЧА ЗАШИФРОВАННЫХ ДАННЫХ ЧЕРЕЗ EMAIL
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Зашифруйте текст с помощью AES-256 GCM
    2. Скопируйте результат (в формате JSON)
    3. Вставьте в письмо как обычный текст
    4. Отправьте письмо получателю
    5. Отправьте пароль отдельным каналом связи (мессенджер, звонок)
    6. Получатель вставит текст в поле дешифрования и введет пароль

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    СОВЕТЫ ПО БЕЗОПАСНОСТИ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ✅ РЕКОМЕНДУЕТСЯ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Используйте только надежные алгоритмы (AES-256 GCM, ChaCha20-Poly1305)
    2. Создавайте уникальные надежные пароли для каждой операции
    3. Храните пароли в специализированных менеджерах паролей
    4. Регулярно меняйте пароли для критически важных данных
    5. Используйте двухфакторную аутентификацию при передаче паролей
    6. Проверяйте целостность расшифрованных данных по хешу
    7. Создавайте резервные копии зашифрованных файлов
    8. Тестируйте процесс дешифрования сразу после шифрования

    ❌ НЕ РЕКОМЕНДУЕТСЯ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Использовать простые или повторяющиеся пароли
    2. Передавать пароль тем же каналом, что и зашифрованные данные
    3. Использовать алгоритмы XOR и Base64 для защиты реальных данных
    4. Хранить пароли в открытом виде на компьютере
    5. Использовать один пароль для разных наборов данных
    6. Забывать проверять результат дешифрования
    7. Использовать устаревшие алгоритмы (AES-OFB) для новых данных
    8. Игнорировать предупреждения о низком уровне безопасности

    ⚠️ КРИТИЧЕСКИЕ ПРЕДУПРЕЖДЕНИЯ:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • При потере пароля восстановление данных НЕВОЗМОЖНО!
    • Никогда не используйте XOR для защиты конфиденциальных данных
    • Base64 - это кодирование, НЕ шифрование
    • Даже самый надежный алгоритм бесполезен при слабом пароле
    • Всегда проверяйте целостность расшифрованных данных

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    РЕШЕНИЕ ПРОБЛЕМ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ПРОБЛЕМА: "Неверный пароль"
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    РЕШЕНИЕ:
    1. Проверьте раскладку клавиатуры (русская/английская)
    2. Проверьте регистр символов (Caps Lock)
    3. Проверьте наличие пробелов в начале или конце пароля
    4. Убедитесь, что используете правильный пароль
    5. Если пароль утерян - данные восстановить невозможно

    ПРОБЛЕМА: "Поврежденные данные"
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    РЕШЕНИЕ:
    1. Проверьте, не был ли файл изменен после шифрования
    2. Убедитесь, что файл загружен полностью (проверьте размер)
    3. Попробуйте загрузить файл заново
    4. Проверьте контрольную сумму файла (если доступна)

    ПРОБЛЕМА: "Несовместимый алгоритм"
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    РЕШЕНИЕ:
    1. Убедитесь, что используете последнюю версию программы
    2. Проверьте формат файла (должен быть .ongcrypt или JSON)
    3. Если файл создан в другой программе - конвертируйте формат

    ПРОБЛЕМА: "Данные слишком большие"
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    РЕШЕНИЕ:
    1. Разбейте большой файл на части поменьше
    2. Используйте архиватор для сжатия перед шифрованием
    3. Для очень больших файлов используйте специализированные инструменты

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ГОРЯЧИЕ КЛАВИШИ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Ctrl+K - Переключиться на вкладку шифрования
    • Ctrl+V - Вставить данные в поле шифрования/дешифрования
    • Ctrl+C - Скопировать результат дешифрования
    • Ctrl+S - Сохранить результат
    • Ctrl+E - Начать дешифрование
    • Enter - Выполнить шифрование (когда фокус на кнопке)

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ❓ Можно ли восстановить данные без пароля?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    НЕТ. Современные алгоритмы шифрования (AES-256, ChaCha20) криптографически
    стойкие. Без правильного пароля восстановление данных вычислительно невозможно,
    даже с использованием суперкомпьютеров.

    ❓ Какой алгоритм самый безопасный?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    На текущий момент наиболее безопасными являются:
    • AES-256 GCM - для большинства задач
    • ChaCha20-Poly1305 - для мобильных устройств и систем без аппаратного ускорения AES

    Оба алгоритма обеспечивают 256-битный уровень безопасности и встроенную
    аутентификацию данных.

    ❓ Можно ли использовать один пароль для нескольких файлов?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ТЕОРЕТИЧЕСКИ можно, но это снижает безопасность. Рекомендуется использовать
    уникальный пароль для каждого набора данных. Если нужно зашифровать много файлов,
    используйте менеджер паролей для генерации и хранения уникальных паролей.

    ❓ Что такое "соль" (salt) и зачем она нужна?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Соль - это случайные данные, добавляемые к паролю перед генерацией ключа.
    Она предотвращает атаки по радужным таблицам и гарантирует, что даже при
    использовании одинаковых паролей будут сгенерированы разные ключи.

    ❓ Почему нужен такой сложный пароль?
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Длина и сложность пароля напрямую влияют на время, необходимое для взлома
    методом перебора (brute force). Пароль из 8 случайных символов может быть
    взломан за часы/дни, а пароль из 12+ символов со смешанными регистрами,
    цифрами и символами - за миллионы лет.

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ТЕХНИЧЕСКИЕ ДЕТАЛИ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ИСПОЛЬЗУЕМЫЕ СТАНДАРТЫ:
    • Криптография: библиотека `cryptography` (Python)
    • Алгоритмы: реализации соответствуют стандартам NIST и IETF
    • KDF: PBKDF2-HMAC-SHA256 с 600 000 итераций
    • Формат: собственный формат с поддержкой версионирования

    СИЛА КЛЮЧЕЙ:
    • AES-256: 256-битный ключ (2^256 возможных комбинаций)
    • ChaCha20: 256-битный ключ
    • Соль: 128 бит случайных данных

    ЗАЩИТА ОТ АТАК:
    • Атаки по времени: защищено сравнением через secrets.compare_digest()
    • Атаки по памяти: ключи очищаются после использования
    • Атаки по радужным таблицам: защищено использованием соли
    • Атаки повторного воспроизведения: защищено использованием nonce/IV

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    ЗАКЛЮЧЕНИЕ
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Вкладка шифрования предоставляет профессиональные инструменты для защиты
    ваших данных. Следуя рекомендациям из этого руководства, вы сможете
    обеспечить высокий уровень безопасности вашей информации.

    ПОМНИТЕ:
    • Безопасность = Надежный алгоритм + Надежный пароль + Правильное использование
    • Никогда не экономьте на безопасности паролей
    • Регулярно тестируйте процесс дешифрования
    • Храните пароли отдельно от зашифрованных данных

    Успешного шифрования! 🔐
    """
        self.display_help_text(help_text)

    def display_help_text(self, text):
        """Отображает текст помощи"""
        self.help_text.config(state='normal')
        self.help_text.delete("1.0", tk.END)
        self.help_text.insert("1.0", text)
        self.help_text.config(state='disabled')

    def search_help(self):
        """Поиск в помощи"""
        search_term = tk.simpledialog.askstring("Поиск", "Введите текст для поиска:")
        if search_term:
            content = self.help_text.get("1.0", tk.END)
            if search_term.lower() in content.lower():
                messagebox.showinfo("Поиск", "Текст найден!")
                # Можно добавить подсветку найденного текста
            else:
                messagebox.showinfo("Поиск", "Текст не найден.")

    def download_help_pdf(self):
        """Скачивает помощь в PDF с поддержкой кириллицы"""
        try:
            # Импортируем необходимые модули
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            import sys
            import time

            # Регистрируем шрифт с поддержкой кириллицы
            try:
                # Пытаемся использовать шрифт из системы
                if sys.platform.startswith('win'):
                    font_path = 'C:/Windows/Fonts/arial.ttf'
                elif sys.platform.startswith('darwin'):
                    font_path = '/System/Library/Fonts/PingFang.ttc'  # Для Mac
                else:  # Linux
                    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

                # Если шрифт не найден, используем встроенный шрифт с кириллицей
                if not os.path.exists(font_path):
                    # Используем шрифт из ресурсов приложения
                    font_path = os.path.join(os.path.dirname(__file__), 'resources', 'DejaVuSans.ttf')
                    if not os.path.exists(font_path):
                        # Если ресурс не найден, пытаемся загрузить шрифт
                        try:
                            import urllib.request
                            os.makedirs(os.path.join(os.path.dirname(__file__), 'resources'), exist_ok=True)
                            font_path = os.path.join(os.path.dirname(__file__), 'resources', 'DejaVuSans.ttf')
                            urllib.request.urlretrieve(
                                'https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf',
                                font_path
                            )
                        except:
                            raise Exception("Не удалось найти шрифт с поддержкой кириллицы")

                # Регистрируем шрифт
                pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                font_name = 'DejaVuSans'
            except Exception as e:
                messagebox.showerror("Ошибка шрифта",
                                     f"Не удалось загрузить шрифт с кириллицей: {str(e)}\n\nУстановите шрифт DejaVu Sans или Arial в систему.")
                self.log_manager.add_entry("pdf_font_error", "error", {"error": str(e)})
                return

            # Получаем текущий текст помощи
            help_text = self.help_text.get("1.0", tk.END).strip()

            if not help_text:
                messagebox.showwarning("Предупреждение", "Нет текста для экспорта в PDF")
                return

            # Открываем диалог сохранения
            file_path = filedialog.asksaveasfilename(
                title="Сохранить помощь в PDF",
                defaultextension=".pdf",
                filetypes=[("PDF файлы", "*.pdf"), ("Все файлы", "*.*")],
                initialdir=self.last_save_dir,
                initialfile=f"OccultoNG_Pro_Pomosh_v{VERSION}.pdf"
            )

            if not file_path:
                return

            # Создаем PDF документ
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            # Стили для PDF (с указанием шрифта)
            styles = getSampleStyleSheet()

            # Заголовок
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=font_name,
                fontSize=16,
                alignment=1,
                spaceAfter=30,
                textColor=colors.HexColor("#2563EB")
            )

            # Заголовки разделов
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontName=font_name,
                fontSize=14,
                spaceBefore=20,
                spaceAfter=10,
                textColor=colors.HexColor("#1E3A8A")
            )

            # Обычный текст
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=11,
                spaceAfter=6,
                leading=14
            )

            # Стиль для подсказок/советов
            tip_style = ParagraphStyle(
                'CustomTip',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=11,
                spaceAfter=6,
                leading=14,
                backColor=colors.HexColor("#F0F9FF"),
                borderColor=colors.HexColor("#3B82F6"),
                borderWidth=1,
                borderPadding=8,
                spaceBefore=10
            )

            # Стиль для кода
            code_style = ParagraphStyle(
                'CustomCode',
                parent=styles['Code'],
                fontName=font_name,
                fontSize=10,
                backColor=colors.HexColor("#F3F4F6"),
                borderPadding=6,
                spaceAfter=10
            )

            # Стиль для предупреждений
            warning_style = ParagraphStyle(
                'CustomWarning',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=11,
                spaceAfter=6,
                leading=14,
                textColor=colors.HexColor("#DC2626")
            )

            # Стиль для информации
            info_style = ParagraphStyle(
                'CustomInfo',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=11,
                spaceAfter=6,
                leading=14,
                textColor=colors.HexColor("#047857")
            )

            # Формируем содержание документа
            story = []

            # Титульная страница
            title = Paragraph(f"ØccultoNG Pro v{VERSION}", title_style)
            story.append(title)
            story.append(Spacer(1, 24))

            subtitle = Paragraph("Полное руководство пользователя",
                                 ParagraphStyle('Subtitle', parent=styles['Heading2'],
                                                fontName=font_name, fontSize=14, alignment=1))
            story.append(subtitle)
            story.append(Spacer(1, 48))

            author = Paragraph(f"Автор: {AUTHOR}",
                               ParagraphStyle('Author', parent=styles['Normal'],
                                              fontName=font_name, fontSize=12, alignment=1))
            story.append(author)
            story.append(Spacer(1, 12))

            date = Paragraph(f"Дата сборки: {BUILD_DATE}",
                             ParagraphStyle('Date', parent=styles['Normal'],
                                            fontName=font_name, fontSize=12, alignment=1))
            story.append(date)
            story.append(Spacer(1, 12))

            contact = Paragraph("Техническая поддержка: tudubambam@ya.ru",
                                ParagraphStyle('Contact', parent=styles['Normal'],
                                               fontName=font_name, fontSize=12, alignment=1))
            story.append(contact)
            story.append(PageBreak())

            # Содержание
            toc_title = Paragraph("Содержание", heading_style)
            story.append(toc_title)
            story.append(Spacer(1, 12))

            # Создаем оглавление
            contents = [
                "1. Введение",
                "2. Поддерживаемые методы",
                "3. Быстрый старт",
                "4. Пакетная обработка",
                "5. Советы и рекомендации",
                "6. Горячие клавиши",
                "7. Часто задаваемые вопросы",
                "8. Техническая поддержка"
            ]

            for item in contents:
                story.append(Paragraph(f"• {item}", normal_style))
                story.append(Spacer(1, 4))

            story.append(PageBreak())

            # Основное содержание
            story.append(Paragraph("1. Введение", heading_style))
            story.append(Spacer(1, 12))

            # Разбиваем текст на абзацы и форматируем их
            paragraphs = help_text.split("\n")
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue

                # Определяем тип абзаца по префиксам
                if para.startswith("🎯") or para.startswith("🚀") or para.startswith("📋"):
                    story.append(Paragraph(para, heading_style))
                elif para.startswith("💡") or para.startswith("✅") or para.startswith("🏆"):
                    story.append(Paragraph(para, tip_style))
                elif para.startswith("⚠️") or para.startswith("❌"):
                    story.append(Paragraph(para, warning_style))
                elif para.startswith("🔍") or para.startswith("📊") or para.startswith("🔄"):
                    story.append(Paragraph(para, info_style))
                elif para.startswith("```") or para.startswith("    "):
                    # Код или пример
                    code_text = para.replace("```", "").strip()
                    story.append(Paragraph(code_text, code_style))
                else:
                    # Обычный текст
                    story.append(Paragraph(para, normal_style))

            story.append(Spacer(1, 24))
            story.append(Paragraph(f"Документ сгенерирован: {time.strftime('%d.%m.%Y %H:%M')}",
                                   ParagraphStyle('Footer', parent=styles['Normal'],
                                                  fontName=font_name, fontSize=9, alignment=2)))

            # Создаем PDF
            doc.build(story)
            import subprocess
            # Показываем сообщение об успехе
            if messagebox.askyesno("Успех", f"Помощь успешно сохранена в PDF: {file_path}\n\nОткрыть файл сейчас?"):
                try:
                    if sys.platform.startswith('darwin'):
                        subprocess.call(['open', file_path])
                    elif os.name == 'nt':
                        os.startfile(file_path)
                    else:
                        subprocess.call(['xdg-open', file_path])
                except Exception as e:
                    messagebox.showwarning("Предупреждение", f"Не удалось открыть PDF файл: {str(e)}")

            self.log_manager.add_entry("help_exported", "success", {"format": "PDF", "file": file_path})
            self.show_toast("✅ Помощь экспортирована в PDF")

        except ImportError:
            # Обработка отсутствия reportlab
            if messagebox.askyesno("Ошибка",
                                   "Библиотека reportlab не установлена.\n\nХотите установить её автоматически?"):
                try:
                    import subprocess
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
                    messagebox.showinfo("Успех",
                                        "Библиотека reportlab успешно установлена. Попробуйте снова экспортировать PDF.")
                    self.log_manager.add_entry("pdf_library_installed", "success", {})
                except Exception as e:
                    messagebox.showerror("Ошибка",
                                         f"Не удалось установить библиотеку reportlab: {str(e)}\n\nПожалуйста, установите её вручную: pip install reportlab")
                    self.log_manager.add_entry("pdf_library_install_failed", "error", {"error": str(e)})
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать PDF файл: {str(e)}")
            self.log_manager.add_entry("help_export_failed", "error", {"error": str(e)})

    def send_feedback(self):
        """Предлагает несколько вариантов для обратной связи"""

        # Создаем окно выбора
        feedback_window = tk.Toplevel(self.root)
        feedback_window.title("Обратная связь")
        feedback_window.geometry("500x300")
        feedback_window.transient(self.root)
        feedback_window.grab_set()
        feedback_window.configure(bg=self.colors["bg"])

        ttk.Label(
            feedback_window,
            text="📝 Обратная связь",
            font=("Segoe UI", 16, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["bg"]
        ).pack(pady=(20, 10))

        ttk.Label(
            feedback_window,
            text="Пожалуйста, выберите способ обратной связи:",
            font=("Segoe UI", 11),
            background=self.colors["bg"],
            foreground=self.colors["text"]
        ).pack(pady=(0, 20))

        # Вариант 1: Google Forms (основной)
        forms_btn = ttk.Button(
            feedback_window,
            text="📊 Заполнить форму Google Forms",
            style="Accent.TButton",
            command=lambda: self.open_feedback_form(feedback_window)
        )
        forms_btn.pack(fill=tk.X, padx=50, pady=5)

        # Вариант 2: Email
        email_btn = ttk.Button(
            feedback_window,
            text="📧 Написать на email",
            style="TButton",
            command=lambda: self.send_email_feedback(feedback_window)
        )
        email_btn.pack(fill=tk.X, padx=50, pady=5)

        # Вариант 3: GitHub Issues
        github_btn = ttk.Button(
            feedback_window,
            text="🐙 Создать issue на GitHub",
            style="TButton",
            command=lambda: self.open_github_issues(feedback_window)
        )
        github_btn.pack(fill=tk.X, padx=50, pady=5)

        ttk.Separator(feedback_window, orient="horizontal").pack(fill=tk.X, padx=50, pady=20)

        # Кнопка отмены
        ttk.Button(
            feedback_window,
            text="❌ Отмена",
            style="TButton",
            command=feedback_window.destroy
        ).pack(pady=10)

    def open_feedback_form(self, parent_window=None):
        """Открывает форму Google Forms"""
        import webbrowser

        feedback_url = "https://docs.google.com/forms/d/1LrCMmimT_BCiVGekva2sbWgVfAUz6MbbzsPcZ3SgKKA"

        try:
            if parent_window:
                parent_window.destroy()

            webbrowser.open(feedback_url, new=2)

            messagebox.showinfo(
                "✅ Форма открыта",
                "Форма для отзыва открыта в вашем браузере.\n\n"
                "Пожалуйста, заполните форму, чтобы помочь нам улучшить программу!"
            )

            self.log_manager.add_entry("feedback", "info", {"type": "google_forms"})

        except Exception as e:
            messagebox.showerror(
                "❌ Ошибка",
                f"Не удалось открыть форму:\n{str(e)}\n\n"
                f"Скопируйте ссылку вручную:\n{feedback_url}"
            )

    def send_email_feedback(self, parent_window=None):
        """Предлагает отправить email"""
        import webbrowser

        if parent_window:
            parent_window.destroy()

        email_url = "mailto:tudubambam@ya.ru?subject=Отзыв%20о%20программе%20ØccultoNG%20Pro&body=Пожалуйста,%20опишите%20ваш%20отзыв%20или%20предложение..."

        try:
            webbrowser.open(email_url)
            messagebox.showinfo(
                "📧 Email",
                "Почтовый клиент открыт.\n\n"
                "Пожалуйста, отправьте ваш отзыв на адрес: tudubambam@ya.ru"
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Ошибка",
                f"Не удалось открыть почтовый клиент:\n{str(e)}\n\n"
                "Напишите на адрес: tudubambam@ya.ru"
            )

    def open_github_issues(self, parent_window=None):
        """Открывает страницу Issues на GitHub"""
        import webbrowser

        if parent_window:
            parent_window.destroy()

        github_url = "https://github.com/Proffessor2008/-ccultoNG/issues"

        try:
            webbrowser.open(github_url, new=2)
            messagebox.showinfo(
                "🐙 GitHub Issues",
                "Страница Issues открыта в вашем браузере.\n\n"
                "Вы можете сообщить о баге или предложить новую функцию."
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Ошибка",
                f"Не удалось открыть страницу GitHub:\n{str(e)}"
            )

    def create_status_bar(self, parent: ttk.Frame) -> None:
        status_frame = ttk.Frame(parent, style="StatusBar.TFrame")
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        # Индикатор состояния
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 12),
            bg=self.colors["secondary"],
            fg=self.colors["success"]  # Зеленый для "готов"
        )
        self.status_indicator.pack(side=tk.LEFT, padx=(5, 10))

        self.status_label = ttk.Label(
            status_frame,
            text="✅ Готов к работе",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"],
            style="Secondary.TLabel"
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 20))

        # Индикатор операций
        self.operations_label = ttk.Label(
            status_frame,
            text="📊 Операций: 0",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"],
            style="Secondary.TLabel"
        )
        self.operations_label.pack(side=tk.LEFT, padx=(0, 20))

        # Индикатор времени сессии
        self.session_time_label = ttk.Label(
            status_frame,
            text="⏱️ Сессия: 00:00:00",
            font=("Segoe UI", 9),
            foreground=self.colors["text_secondary"],
            style="Secondary.TLabel"
        )
        self.session_time_label.pack(side=tk.LEFT, padx=(0, 20))

        # Прогресс-бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = AnimatedProgressbar(
            status_frame,
            variable=self.progress_var,
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # Кнопка отмены
        self.cancel_button = ttk.Button(
            status_frame,
            text="⛔ Отмена",
            command=self.cancel_operation,
            style="TButton"
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Скрыть прогресс-бар и кнопку отмены по умолчанию
        self.progress_bar.pack_forget()
        self.cancel_button.pack_forget()

        # Запускаем обновление времени сессии
        self.update_session_time()

    def update_session_time(self):
        """Обновляет индикатор времени сессии"""
        if hasattr(self, 'session_start_time'):
            elapsed = int(time.time() - self.session_start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            time_str = f"⏱️ Сессия: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.session_time_label.config(text=time_str)
            self.root.after(1000, self.update_session_time)

    def create_toast(self) -> None:
        self.toast_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8,
            relief="solid",
            bd=0,
            bg=self.colors.get("shadow", "#333333"),
            fg=self.colors.get("text", "#ffffff"),
            highlightthickness=1,
            highlightcolor=self.colors.get("accent", "#58A6FF")
        )
        self.toast_label.place_forget()

    def show_toast(self, message: str, duration: int = 2000) -> None:
        if self.toast_timer:
            self.root.after_cancel(self.toast_timer)
        self.toast_label.config(text=message)
        self.toast_label.place(relx=0.5, rely=0.9, anchor="center")
        self.toast_timer = self.root.after(duration, self.hide_toast)

    def hide_toast(self) -> None:
        self.toast_label.place_forget()
        self.toast_timer = None

    def on_drag_enter(self, event):
        self.drop_label.configure(style="DropLabelActive.TLabel")

    def on_drag_leave(self, event):
        self.drop_label.configure(style="DropLabel.TLabel")

    def animate_drop(self) -> None:
        original_text = self.drop_label.cget("text")
        self.drop_label.configure(text="✅ Файл успешно загружен!", style="DropLabelActive.TLabel")
        self.root.after(1500, lambda: self.drop_label.configure(text=original_text, style="DropLabel.TLabel"))

    def bind_drag_drop(self) -> None:
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<DragEnter>>', self.on_drag_enter)
        self.drop_label.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_image)

    def bind_drag_drop_extract(self) -> None:
        if self.extract_drop_label:
            self.extract_drop_label.drop_target_register(DND_FILES)
            self.extract_drop_label.dnd_bind('<<DragEnter>>', lambda e: self.extract_drop_label.configure(
                style="DropLabelActive.TLabel"))
            self.extract_drop_label.dnd_bind('<<DragLeave>>',
                                             lambda e: self.extract_drop_label.configure(style="DropLabel.TLabel"))
            self.extract_drop_label.dnd_bind('<<Drop>>', self.on_drop_extract_image)

    def bind_file_drop(self) -> None:
        if self.file_entry_widget:
            try:
                self.file_entry_widget.drop_target_register(DND_FILES)
                self.file_entry_widget.dnd_bind('<<Drop>>', self.on_drop_hide_file)
            except Exception as e:
                print(f"DnD для поля файла не поддерживается: {e}")

    def on_drop_image(self, event: tk.Event) -> None:
        import os
        path = event.data.strip('{}')
        if os.path.isfile(path) and Utils.is_supported_container(path):
            self.img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_size_info()
            self.animate_drop()
            self.show_toast("✅ Контейнер загружен")
            self.update_thumbnail(path, self.preview_img)

            # Автоматический выбор метода в зависимости от формата
            if path.lower().endswith(".wav"):
                self.method_var.set("audio_lsb")
                self.update_method_combo_state("disabled")
            elif path.lower().endswith((".jpg", ".jpeg")):
                # Для JPEG предлагаем DCT метод
                self.method_var.set("jpeg_dct")
                self.update_method_combo_state("readonly")
            else:
                self.method_var.set(self.settings.get("method", "lsb"))
                self.update_method_combo_state("readonly")
        else:
            messagebox.showwarning("❌ Неверный формат", "Допускаются файлы: PNG, BMP, TIFF, TGA, JPG, JPEG, WAV")

    def update_method_combo_state(self, state: str):
        """Обновляет состояние комбобокса методов"""
        for child in self.root.winfo_children():
            for subchild in child.winfo_children():
                if isinstance(subchild, ttk.Combobox) and subchild.cget("width") == 30:
                    if state == "disabled":
                        subchild['values'] = ["jpeg_dct"] if self.img_path.get().lower().endswith(
                            (".jpg", ".jpeg")) else ["audio_lsb"]
                    else:
                        subchild['values'] = list(STEGANO_METHODS.keys())
                    subchild.config(state=state)
                    break

    def on_drop_extract_image(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path) and Utils.is_supported_container(path):
            self.extract_img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.show_toast("✅ Изображение для извлечения загружено")
            self.extract_drop_label.configure(style="DropLabel.TLabel")
            self.update_thumbnail(path, self.extract_preview)
        else:
            messagebox.showwarning(
                "❌ Неверный формат",
                "Поддерживаются только файлы в форматах:\
PNG, BMP, TIFF, TGA, JPG, JPEG, WAV"
            )

    def on_drop_hide_file(self, event: tk.Event) -> None:
        path = event.data.strip('{}')
        if os.path.isfile(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning("⚠️ Слишком большой файл",
                                       f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ")
                return
            self.file_path_var.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_file_info_label()
            self.update_size_info()
            self.show_toast("✅ Файл для скрытия добавлен")
        else:
            messagebox.showwarning("❌ Ошибка", "Перетащен не файл.")

    def show_image_preview(self, image_path: str) -> None:
        if not os.path.exists(image_path):
            return
        preview_win = tk.Toplevel(self.root)
        preview_win.title(f"🖼️ Предпросмотр – {os.path.basename(image_path)}")
        preview_win.geometry("800x800")
        preview_win.minsize(400, 400)
        preview_win.resizable(True, True)
        preview_win.transient(self.root)
        preview_win.grab_set()
        preview_win.focus_set()
        preview_win.bind("<Escape>", lambda e: preview_win.destroy())

        # Создаем canvas с прокруткой для большого изображения
        canvas = tk.Canvas(preview_win, bg=self.colors["bg"])
        scrollbar_y = ttk.Scrollbar(preview_win, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(preview_win, orient="horizontal", command=canvas.xview)

        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        with Image.open(image_path) as img:
            # Ограничиваем максимальный размер для предпросмотра
            img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

        frame = ttk.Frame(canvas, style="Card.TFrame")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        lbl = ttk.Label(frame, image=photo, style="Card.TFrame")
        lbl.image = photo
        lbl.pack(pady=10, padx=10)

        # Информация о файле
        file_info = Utils.get_file_info(image_path)
        info_text = f"📁 Имя: {file_info['name']}\
📏 Размер: {file_info['size_formatted']}\
📅 Создан: {file_info['created']}\
📝 Тип: {file_info['type']}"

        if file_info['type'] == "image":
            info_text += f"\
🖼️ Размеры: {file_info.get('dimensions', 'N/A')}\
🎨 Режим: {file_info.get('mode', 'N/A')}"
        elif file_info['type'] == "audio":
            info_text += f"\
🎵 Каналы: {file_info.get('channels', 'N/A')}\
⏱️ Частота: {file_info.get('sample_rate', 'N/A')} Hz\
🔢 Сэмплов: {file_info.get('frames', 'N/A')}\
⏳ Длительность: {file_info.get('duration', 'N/A')}"

        info_label = ttk.Label(
            frame,
            text=info_text,
            font=("Segoe UI", 10),
            style="Secondary.TLabel",
            justify=tk.LEFT
        )
        info_label.pack(pady=10, padx=10)

        close_btn = ttk.Button(frame, text="❌ Закрыть", command=preview_win.destroy)
        close_btn.pack(pady=10)

        # Обновляем прокрутку
        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Размещаем элементы
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        # Центрируем окно
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 800) // 2
        y = (self.root.winfo_screenheight() - 800) // 2
        preview_win.geometry(f"+{x}+{y}")

    def select_image(self) -> None:
        import os
        path = filedialog.askopenfilename(
            title="📂 Выберите контейнер",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.last_open_dir
        )
        if path:
            if not Utils.is_supported_container(path):
                messagebox.showwarning("❌ Неверный формат", "Допускаются файлы: PNG, BMP, TIFF, TGA, JPG, JPEG, WAV")
                return
            self.img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_size_info()
            self.update_thumbnail(path, self.preview_img)
            # Управление методами
            method_combo = None
            for child in self.root.winfo_children():
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Combobox) and subchild.cget("width") == 30:
                        method_combo = subchild
                        break
            if path.lower().endswith(".wav"):
                self.method_var.set("audio_lsb")
                if method_combo:
                    method_combo['values'] = ["audio_lsb"]
                    method_combo.config(state="disabled")
            else:
                self.method_var.set(self.settings.get("method", "lsb"))
                if method_combo:
                    method_combo['values'] = list(STEGANO_METHODS.keys())
                    method_combo.config(state="readonly")

    def select_extract_image(self) -> None:
        path = filedialog.askopenfilename(
            title="📂 Выберите файл с данными",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.last_open_dir
        )
        if path:
            self.extract_img_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_thumbnail(path, self.extract_preview)

    def select_file(self) -> None:
        path = filedialog.askopenfilename(title="📂 Выберите файл для скрытия", initialdir=self.last_open_dir)
        if path:
            file_size = os.path.getsize(path) / (1024 * 1024)
            if file_size > CONFIG["MAX_FILE_SIZE_MB"]:
                messagebox.showwarning(
                    "⚠️ Слишком большой файл",
                    f"Максимальный размер файла: {CONFIG['MAX_FILE_SIZE_MB']} МБ"
                )
                return
            self.file_path_var.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.update_file_info_label()
            self.update_size_info()

            # Записываем статистику
            file_ext = os.path.splitext(path)[1].lower()
            self.analytics_manager.record_operation("file_selected", True, file_type=file_ext)

    def update_file_info_label(self) -> None:
        try:
            fp = self.file_path_var.get()
            if not fp or not os.path.exists(fp):
                self.file_info_label.config(text="ℹ️ Файл не выбран")
                return
            size = os.path.getsize(fp)
            name = os.path.basename(fp)
            file_info = Utils.get_file_info(fp)

            info_text = f"📄 {name} • {Utils.format_size(size)}"
            if file_info.get("type") == "image":
                info_text += f" • {file_info.get('dimensions', '')}"
            elif file_info.get("type") == "audio":
                info_text += f" • {file_info.get('duration', '')}"

            self.file_info_label.config(text=info_text)
        except Exception:
            self.file_info_label.config(text="❌ Ошибка чтения файла")

    def toggle_data_input(self) -> None:
        if self.data_type.get() == "text":
            self.file_frame.pack_forget()
            self.text_frame.pack(fill=tk.BOTH, expand=True)
            self.file_info_label.config(text="ℹ️ Введите текст для скрытия")
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill=tk.X, pady=(10, 0))
            self.file_info_label.config(text="ℹ️ Поддерживаемые форматы: любые файлы до 100 МБ")
        self.update_size_info()

    def update_size_info(self) -> None:
        """Обновляет информацию о размере с учётом JPEG DCT"""
        import os
        import time

        current_time = time.time()
        if current_time - self.last_update_time < 0.2:
            return
        self.last_update_time = current_time

        # Сброс всех меток
        self.required_size_label.config(text="📏 Требуется: выберите данные", style="TLabel")
        for _, lbl in self.capacity_labels.items():
            lbl.config(text=f"{lbl.cget('text').split(':')[0]}: ожидание...", style="Secondary.TLabel")

        if self.usage_label:
            self.usage_label.config(text="📈 Заполнение выбранного метода: не рассчитано")
        if self.usage_bar:
            self.usage_var.set(0)
            self.usage_bar.config(style="UsageGreen.Horizontal.TProgressbar")

        try:
            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                ext = os.path.splitext(img_path)[1].lower() if img_path else ""
                if ext == '.wav':
                    self.required_size_label.config(text="❌ Аудиофайл-контейнер не выбран", style="Error.TLabel")
                else:
                    self.required_size_label.config(text="❌ Изображение-контейнер не выбран", style="Error.TLabel")
                return

            # Получаем информацию о файле
            w, h, available_bits = ImageProcessor.get_image_info(img_path)

            # Рассчитываем требуемый размер данных
            if self.data_type.get() == "text":
                data_text = self.text_input.get("1.0", tk.END).strip()
                if not data_text:
                    required_bits = 0
                    required_text = "0 B"
                else:
                    # Добавляем заголовок
                    header_size = 12 if self.method_var.get() == "jpeg_dct" else HEADER_FULL_LEN
                    required_bytes = len(data_text.encode('utf-8')) + header_size
                    required_bits = required_bytes * 8
                    required_text = Utils.format_size(required_bytes)
            else:
                file_path = self.file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    required_bits = 0
                    required_text = "0 B"
                else:
                    file_size = os.path.getsize(file_path)
                    header_size = 12 if self.method_var.get() == "jpeg_dct" else HEADER_FULL_LEN
                    required_bytes = file_size + header_size
                    required_bits = required_bytes * 8
                    required_text = Utils.format_size(required_bytes)

            # Обновляем информацию о требуемом размере
            self.required_size_label.config(
                text=f"📏 Требуется: {required_text} ({required_bits} бит)",
                style="TLabel" if required_bits > 0 else "Warning.TLabel"
            )

            # Обновляем информацию о вместимости для каждого метода
            for method, label in self.capacity_labels.items():
                try:
                    capacity_bits = ImageProcessor.get_capacity_by_method(
                        available_bits, method, w, h
                    )
                    capacity_bytes = capacity_bits // 8

                    if method == "jpeg_dct":
                        method_name = "JPEG DCT"
                    else:
                        method_name = STEGANO_METHODS.get(method, method)

                    if capacity_bytes > 0:
                        label.config(
                            text=f"{method_name}: {Utils.format_size(capacity_bytes)} ({capacity_bits} бит)",
                            style="Success.TLabel" if capacity_bits >= required_bits else "Error.TLabel"
                        )
                    else:
                        label.config(
                            text=f"{method_name}: нет данных",
                            style="Error.TLabel"
                        )
                except Exception as e:
                    print(f"Ошибка расчёта для метода {method}: {e}")

            # Обновляем индикатор заполнения для выбранного метода
            selected_method = self.method_var.get()
            capacity_bits = ImageProcessor.get_capacity_by_method(
                available_bits, selected_method, w, h
            )

            if capacity_bits > 0 and required_bits > 0:
                usage_percent = min(100, (required_bits / capacity_bits) * 100)
                self.usage_var.set(usage_percent)

                # Выбираем цвет в зависимости от заполнения
                if usage_percent <= 70:
                    style = "UsageGreen.Horizontal.TProgressbar"
                    color_text = "🟢 Норма"
                elif usage_percent <= 90:
                    style = "UsageYellow.Horizontal.TProgressbar"
                    color_text = "🟡 Внимание"
                else:
                    style = "UsageRed.Horizontal.TProgressbar"
                    color_text = "🔴 Переполнение"

                self.usage_bar.config(style=style)
                self.usage_label.config(
                    text=f"📈 Заполнение: {usage_percent:.1f}% ({color_text})",
                    style="Success.TLabel" if usage_percent <= 70 else
                    "Warning.TLabel" if usage_percent <= 90 else "Error.TLabel"
                )
            else:
                self.usage_var.set(0)
                self.usage_label.config(
                    text="📈 Заполнение: не рассчитано",
                    style="Secondary.TLabel"
                )

        except Exception as e:
            print(f"Ошибка обновления информации о размере: {e}")
            self.required_size_label.config(
                text="❌ Ошибка расчёта размера",
                style="Error.TLabel"
            )

    def update_thumbnail(self, path: str, target_label: tk.Widget) -> None:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".wav":
            target_label.configure(image='', text='🎵 WAV аудиофайл(предпросмотр невозможен)')
            target_label.image = None
            return

        try:
            with Image.open(path) as img:
                img.thumbnail((300, 300), Image.Resampling.BOX)
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                tk_img = ImageTk.PhotoImage(img)
                target_label.configure(image=tk_img, text='')
                target_label.image = tk_img
        except Exception as e:
            target_label.configure(image='', text=f'❌ Ошибка: {e}')
            target_label.image = None

    def _create_encryption_content(self, parent: ttk.Frame) -> None:
        """Создает содержимое вкладки шифрования с оптимизированным интерфейсом и подробной документацией"""
        # Заголовок вкладки
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 15))

        ttk.Label(
            header_frame,
            text="🔐 Продвинутое шифрование и дешифрование",
            font=("Segoe UI Variable Display", 24, "bold"),
            foreground=self.colors["accent"],
            style="Title.TLabel"
        ).pack(side=tk.LEFT)

        # Основной контент с тремя колонками
        content_frame = ttk.Frame(parent, style="Card.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Настройка пропорций колонок: шифрование (2) | дешифрование (2) | документация (1)
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)

        # === ЛЕВАЯ КОЛОНКА: ШИФРОВАНИЕ ===
        encrypt_frame = ttk.LabelFrame(
            content_frame,
            text="🔒 Шифрование данных",
            padding=15,
            style="Card.TLabelframe"
        )
        encrypt_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Тип данных для шифрования
        data_type_frame = ttk.Frame(encrypt_frame, style="Card.TFrame")
        data_type_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(data_type_frame, text="Тип данных:", style="TLabel").pack(side=tk.LEFT)

        self.encrypt_data_type = tk.StringVar(value="text")
        ttk.Radiobutton(
            data_type_frame,
            text="Текст",
            variable=self.encrypt_data_type,
            value="text",
            command=self._toggle_encrypt_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT, padx=(10, 15))

        ttk.Radiobutton(
            data_type_frame,
            text="Файл",
            variable=self.encrypt_data_type,
            value="file",
            command=self._toggle_encrypt_input,
            style="TRadiobutton"
        ).pack(side=tk.LEFT)

        # Ввод текста
        self.encrypt_text_frame = ttk.Frame(encrypt_frame, style="Card.TFrame")
        self.encrypt_text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        ttk.Label(
            self.encrypt_text_frame,
            text="Введите текст для шифрования:",
            style="Secondary.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        # Панель инструментов текста
        text_toolbar = ttk.Frame(self.encrypt_text_frame, style="Card.TFrame")
        text_toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(
            text_toolbar,
            text="📋 Вставить",
            style="IconButton.TButton",
            command=self._paste_to_encrypt_text
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            text_toolbar,
            text="🗑️ Очистить",
            style="IconButton.TButton",
            command=lambda: self.encrypt_text_input.delete("1.0", tk.END)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.encrypt_text_input = scrolledtext.ScrolledText(
            self.encrypt_text_frame,
            height=6,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff"
        )
        self.encrypt_text_input.pack(fill=tk.BOTH, expand=True)

        # Выбор файла
        self.encrypt_file_frame = ttk.Frame(encrypt_frame, style="Card.TFrame")
        self.encrypt_file_frame.pack(fill=tk.X, pady=(0, 10))
        self.encrypt_file_frame.pack_forget()

        file_input_frame = ttk.Frame(self.encrypt_file_frame, style="Card.TFrame")
        file_input_frame.pack(fill=tk.X)

        ttk.Label(file_input_frame, text="Файл для шифрования:", style="TLabel").pack(side=tk.LEFT)

        self.encrypt_file_path = tk.StringVar()
        file_entry = ttk.Entry(
            file_input_frame,
            textvariable=self.encrypt_file_path,
            state='readonly',
            style="TEntry"
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(
            file_input_frame,
            text="📂 Выбрать...",
            command=self._select_encrypt_file,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Выбор алгоритма с цветовой индикацией безопасности
        algorithm_frame = ttk.Frame(encrypt_frame, style="Card.TFrame")
        algorithm_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(algorithm_frame, text="Алгоритм шифрования:", style="TLabel").pack(side=tk.LEFT)

        self.encrypt_algorithm = tk.StringVar(value="aes_256_gcm")
        algorithm_combo = ttk.Combobox(
            algorithm_frame,
            textvariable=self.encrypt_algorithm,
            values=list(EncryptionManager.SUPPORTED_ALGORITHMS.keys()),
            state="readonly",
            width=25,
            style="TCombobox"
        )
        algorithm_combo.pack(side=tk.LEFT, padx=5)
        algorithm_combo.bind("<<ComboboxSelected>>", self._update_encrypt_params_and_docs)

        # Параметры шифрования
        self.encrypt_params_frame = ttk.LabelFrame(
            encrypt_frame,
            text="Параметры шифрования",
            padding=10,
            style="Card.TLabelframe"
        )
        self.encrypt_params_frame.pack(fill=tk.X, pady=(0, 15))

        # Пароль
        password_frame = ttk.Frame(self.encrypt_params_frame, style="Card.TFrame")
        password_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(password_frame, text="Пароль:", style="TLabel").pack(side=tk.LEFT)

        self.encrypt_password = tk.StringVar()
        self.encrypt_password_entry = ttk.Entry(
            password_frame,
            textvariable=self.encrypt_password,
            show="●",
            style="TEntry"
        )
        self.encrypt_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.encrypt_show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            password_frame,
            text="Показать",
            variable=self.encrypt_show_password,
            command=self._toggle_encrypt_password_visibility,
            style="TCheckbutton"
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Кнопки действий
        button_frame = ttk.Frame(encrypt_frame, style="Card.TFrame")
        button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            button_frame,
            text="🔐 Зашифровать",
            style="Accent.TButton",
            command=self._start_encryption
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="💾 Сохранить",
            style="TButton",
            command=self._save_encrypted_data
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Результат шифрования
        result_frame = ttk.LabelFrame(
            encrypt_frame,
            text="Результат шифрования",
            padding=10,
            style="Card.TLabelframe"
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.encrypt_result = scrolledtext.ScrolledText(
            result_frame,
            height=8,
            font=("Consolas", 9),
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        self.encrypt_result.pack(fill=tk.BOTH, expand=True)

        # === ЦЕНТРАЛЬНАЯ КОЛОНКА: ДЕШИФРОВАНИЕ ===
        decrypt_frame = ttk.LabelFrame(
            content_frame,
            text="🔓 Дешифрование данных",
            padding=15,
            style="Card.TLabelframe"
        )
        decrypt_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10))

        # Ввод зашифрованных данных
        ttk.Label(
            decrypt_frame,
            text="Зашифрованные данные:",
            style="Secondary.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        # Панель инструментов дешифрования
        decrypt_toolbar = ttk.Frame(decrypt_frame, style="Card.TFrame")
        decrypt_toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(
            decrypt_toolbar,
            text="📋 Вставить",
            style="IconButton.TButton",
            command=self._paste_to_decrypt_input
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            decrypt_toolbar,
            text="📂 Загрузить",
            style="IconButton.TButton",
            command=self._load_encrypted_file
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            decrypt_toolbar,
            text="🗑️ Очистить",
            style="IconButton.TButton",
            command=lambda: self.decrypt_input.delete("1.0", tk.END)
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.decrypt_input = scrolledtext.ScrolledText(
            decrypt_frame,
            height=10,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff"
        )
        self.decrypt_input.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Пароль для дешифрования
        decrypt_password_frame = ttk.Frame(decrypt_frame, style="Card.TFrame")
        decrypt_password_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(decrypt_password_frame, text="Пароль:", style="TLabel").pack(side=tk.LEFT)

        self.decrypt_password = tk.StringVar()
        self.decrypt_password_entry = ttk.Entry(
            decrypt_password_frame,
            textvariable=self.decrypt_password,
            show="●",
            style="TEntry"
        )
        self.decrypt_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.decrypt_show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            decrypt_password_frame,
            text="Показать",
            variable=self.decrypt_show_password,
            command=self._toggle_decrypt_password_visibility,
            style="TCheckbutton"
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Результат дешифрования
        result_frame = ttk.LabelFrame(
            decrypt_frame,
            text="Результат дешифрования",
            padding=10,
            style="Card.TLabelframe"
        )
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.decrypt_result = scrolledtext.ScrolledText(
            result_frame,
            height=8,
            font=("Consolas", 10),
            wrap=tk.WORD,
            state='disabled',
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        self.decrypt_result.pack(fill=tk.BOTH, expand=True)

        # Кнопки действий
        button_frame = ttk.Frame(decrypt_frame, style="Card.TFrame")
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="🔓 Расшифровать",
            style="Accent.TButton",
            command=self._start_decryption
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="📋 Копировать",
            style="TButton",
            command=self._copy_decrypt_result
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            button_frame,
            text="💾 Сохранить",
            style="TButton",
            command=self._save_decrypt_result
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # === ПРАВАЯ КОЛОНКА: ДОКУМЕНТАЦИЯ (УМЕНЬШЕНА ПО ШИРИНЕ) ===
        docs_frame = ttk.LabelFrame(
            content_frame,
            text="📚 Детальная документация",
            padding=15,
            style="Card.TLabelframe"
        )
        docs_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        # Заголовок документации
        self.docs_title = ttk.Label(
            docs_frame,
            text="Выберите алгоритм для просмотра документации",
            font=("Segoe UI", 14, "bold"),
            style="TLabel"
        )
        self.docs_title.pack(anchor="w", pady=(0, 10))

        # Фрейм для содержимого документации с прокруткой
        docs_canvas = tk.Canvas(docs_frame, bg=self.colors["card"], highlightthickness=0)
        docs_scrollbar = ttk.Scrollbar(docs_frame, orient="vertical", command=docs_canvas.yview)
        docs_scrollable = ttk.Frame(docs_canvas, style="Card.TFrame")

        docs_scrollable.bind(
            "<Configure>",
            lambda e: docs_canvas.configure(scrollregion=docs_canvas.bbox("all"))
        )

        docs_canvas.create_window((0, 0), window=docs_scrollable, anchor="nw")
        docs_canvas.configure(yscrollcommand=docs_scrollbar.set)

        # Размещение канваса и скроллбара
        docs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        docs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Уровень безопасности
        self.docs_security_label = ttk.Label(
            docs_scrollable,
            text="Уровень безопасности: ",
            font=("Segoe UI", 11, "bold"),
            style="Secondary.TLabel"
        )
        self.docs_security_label.pack(anchor="w", pady=(0, 5))

        # Описание алгоритма
        self.docs_desc_label = ttk.Label(
            docs_scrollable,
            text="Полное описание алгоритма...",
            wraplength=350,  # Уменьшено для узкой колонки
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_desc_label.pack(anchor="w", pady=(0, 10))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Сценарии использования
        self.docs_use_label = ttk.Label(
            docs_scrollable,
            text="Рекомендуемые сценарии:",
            font=("Segoe UI", 10, "bold"),
            style="TLabel"
        )
        self.docs_use_label.pack(anchor="w", pady=(0, 5))

        self.docs_use_cases = ttk.Label(
            docs_scrollable,
            text="• Общее шифрование файлов",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_use_cases.pack(anchor="w", pady=(0, 10))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Ключевая производная функция
        self.docs_kdf_label = ttk.Label(
            docs_scrollable,
            text="Ключевая функция (KDF): PBKDF2-HMAC-SHA256",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_kdf_label.pack(anchor="w", pady=(0, 5))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Размер инициализирующего вектора/нонса
        self.docs_iv_label = ttk.Label(
            docs_scrollable,
            text="Размер IV/nonce: 16 байт",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_iv_label.pack(anchor="w", pady=(0, 5))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Аутентификация данных
        self.docs_auth_label = ttk.Label(
            docs_scrollable,
            text="Аутентификация: Встроенная (128-битный тег)",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_auth_label.pack(anchor="w", pady=(0, 5))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Производительность
        self.docs_perf_label = ttk.Label(
            docs_scrollable,
            text="Производительность: Высокая скорость шифрования",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_perf_label.pack(anchor="w", pady=(0, 5))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Ограничения и предостережения
        self.docs_limit_label = ttk.Label(
            docs_scrollable,
            text="Ограничения:",
            font=("Segoe UI", 10, "bold"),
            style="TLabel"
        )
        self.docs_limit_label.pack(anchor="w", pady=(0, 5))

        self.docs_limitations = ttk.Label(
            docs_scrollable,
            text="• Требуется надежный пароль",
            wraplength=350,
            justify=tk.LEFT,
            style="Warning.TLabel"
        )
        self.docs_limitations.pack(anchor="w", pady=(0, 10))

        ttk.Separator(docs_scrollable, orient="horizontal").pack(fill=tk.X, pady=10)

        # Рекомендации по паролям
        self.docs_password_label = ttk.Label(
            docs_scrollable,
            text="Рекомендации по паролям:",
            font=("Segoe UI", 10, "bold"),
            style="TLabel"
        )
        self.docs_password_label.pack(anchor="w", pady=(0, 5))

        self.docs_password_recommendations = ttk.Label(
            docs_scrollable,
            text="• Минимум 12 символов\n• Смешанные регистры, цифры, спецсимволы",
            wraplength=350,
            justify=tk.LEFT,
            style="Secondary.TLabel"
        )
        self.docs_password_recommendations.pack(anchor="w", pady=(0, 10))

        # Инициализация интерфейса
        self._toggle_encrypt_input()
        self._update_encrypt_params_and_docs()
        self._update_algorithm_documentation("aes_256_gcm")

    def _update_encrypt_params_and_docs(self, event=None):
        """Обновляет параметры шифрования И документацию при смене алгоритма"""
        algorithm = self.encrypt_algorithm.get()
        self._reset_password_field()

        # Очищаем фрейм параметров
        for widget in self.encrypt_params_frame.winfo_children():
            widget.destroy()

        # Добавляем параметры в зависимости от алгоритма
        if algorithm in ['xor', 'base64']:
            # Для учебных алгоритмов пароль не обязателен
            password_frame = ttk.Frame(self.encrypt_params_frame, style="Card.TFrame")
            password_frame.pack(fill=tk.X, pady=(0, 5))
            ttk.Label(
                password_frame,
                text="Ключ/пароль (опционально):",
                style="TLabel"
            ).pack(side=tk.LEFT)
            self.encrypt_password_entry = ttk.Entry(
                password_frame,
                textvariable=self.encrypt_password,
                style="TEntry"
            )
            self.encrypt_password_entry.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=5
            )

            # Предупреждение для ненадежных алгоритмов
            warning_label = ttk.Label(
                self.encrypt_params_frame,
                text="⚠️ ВНИМАНИЕ: Этот алгоритм НЕ обеспечивает реальную безопасность!",
                foreground=self.colors["error"],
                wraplength=300,
                justify=tk.LEFT,
                style="Error.TLabel"
            )
            warning_label.pack(fill=tk.X, pady=(5, 0))
        else:
            # Для надежных алгоритмов пароль обязателен
            password_frame = ttk.Frame(self.encrypt_params_frame, style="Card.TFrame")
            password_frame.pack(fill=tk.X, pady=(0, 5))
            ttk.Label(
                password_frame,
                text="Пароль (минимум 8 символов):",
                style="TLabel"
            ).pack(side=tk.LEFT)
            self.encrypt_password_entry = ttk.Entry(
                password_frame,
                textvariable=self.encrypt_password,
                show="●",
                style="TEntry"
            )
            self.encrypt_password_entry.pack(
                side=tk.LEFT,
                fill=tk.X,
                expand=True,
                padx=5
            )
            self.encrypt_show_password = tk.BooleanVar(value=False)
            ttk.Checkbutton(
                password_frame,
                text="Показать",
                variable=self.encrypt_show_password,
                command=self._toggle_encrypt_password_visibility,
                style="TCheckbutton"
            ).pack(side=tk.LEFT, padx=(5, 0))

        # Обновляем документацию
        self._update_algorithm_documentation(algorithm)

    def _update_algorithm_documentation(self, algorithm: str):
        """Обновляет панель документации в зависимости от выбранного алгоритма"""
        info = EncryptionManager.get_algorithm_info(algorithm)
        security_level = EncryptionManager.SECURITY_LEVELS.get(algorithm, "unknown")

        # Обновляем заголовок
        algo_name = EncryptionManager.SUPPORTED_ALGORITHMS.get(algorithm, algorithm)
        self.docs_title.config(text=f"Алгоритм: {algo_name}")

        # Цветовая индикация уровня безопасности
        security_colors = {
            "none": self.colors["error"],
            "low": "#FFA500",
            "medium": "#FFD700",
            "high": self.colors["success"],
            "very_high": "#00CED1",
            "unknown": self.colors["text_secondary"]
        }
        security_texts = {
            "none": "❌ НЕ БЕЗОПАСЕН (только для обучения)",
            "low": "⚠️ Низкий уровень безопасности",
            "medium": "🟡 Средний уровень безопасности",
            "high": "🟢 Высокий уровень безопасности",
            "very_high": "✅ Очень высокий уровень безопасности",
            "unknown": "❓ Уровень безопасности неизвестен"
        }

        # Обновляем метки документации
        self.docs_security_label.config(
            text=f"Уровень безопасности: {security_texts.get(security_level, security_texts['unknown'])}",
            foreground=security_colors.get(security_level, security_colors["unknown"])
        )
        self.docs_desc_label.config(
            text=info.get("description", "Описание недоступно")
        )

        # Форматируем сценарии использования
        use_cases = info.get("use_cases", "Неизвестно").split(". ")
        formatted_use = "\n".join([f"• {case.strip()}" for case in use_cases if case.strip()])
        self.docs_use_cases.config(text=formatted_use)

        # Форматируем ограничения
        limitations = info.get("limitations", "Неизвестно").split(". ")
        formatted_lim = "\n".join([f"⚠️ {lim.strip()}" for lim in limitations if lim.strip()])
        self.docs_limitations.config(text=formatted_lim)

        # Добавляем новые блоки документации:
        # 1. Ключевая производная функция
        kdf_info = info.get("key_derivation", "Неизвестно")
        if hasattr(self, 'docs_kdf_label'):
            self.docs_kdf_label.config(text=f"Ключевая производная функция: {kdf_info}")

        # 2. Размер инициализирующего вектора/нонса
        iv_info = info.get("iv_size", info.get("nonce_size", "Неизвестно"))
        if hasattr(self, 'docs_iv_label'):
            self.docs_iv_label.config(text=f"Размер инициализирующего вектора: {iv_info}")

        # 3. Аутентификация
        auth_info = info.get("authentication", "Неизвестно")
        if hasattr(self, 'docs_auth_label'):
            self.docs_auth_label.config(text=f"Аутентификация данных: {auth_info}")

        # 4. Производительность
        perf_info = info.get("performance", "Неизвестно")
        if hasattr(self, 'docs_perf_label'):
            self.docs_perf_label.config(text=f"Производительность: {perf_info}")

        # Добавляем предупреждения для ненадёжных алгоритмов
        if security_level in ["none", "low"]:
            warning_text = info.get("warning", "Не рекомендуется для защиты реальных данных")
            self.docs_limitations.config(
                text=f"❌ КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:\n{warning_text}",
                foreground=self.colors["error"],
                font=("Segoe UI", 10, "bold")
            )

    def _reset_password_field(self):
        """Сбрасывает состояние поля пароля при смене алгоритма"""
        self.encrypt_password.set("")
        self.encrypt_show_password.set(False)
        if hasattr(self, 'encrypt_password_entry'):
            self.encrypt_password_entry.config(show="●")

    def _toggle_encrypt_password_visibility(self):
        """Переключает видимость пароля для шифрования"""
        if not hasattr(self, 'encrypt_password_entry') or not self.encrypt_password_entry:
            return
        if self.encrypt_show_password.get():
            self.encrypt_password_entry.config(show="")
        else:
            self.encrypt_password_entry.config(show="●")

    def _toggle_decrypt_password_visibility(self):
        """Переключает видимость пароля для дешифрования"""
        if not hasattr(self, 'decrypt_password_entry') or not self.decrypt_password_entry:
            return
        if self.decrypt_show_password.get():
            self.decrypt_password_entry.config(show="")
        else:
            self.decrypt_password_entry.config(show="●")

    def _select_encrypt_file(self):
        """Выбирает файл для шифрования"""
        path = filedialog.askopenfilename(
            title="Выберите файл для шифрования",
            initialdir=self.last_open_dir
        )
        if path:
            self.encrypt_file_path.set(path)
            self.last_open_dir = os.path.dirname(path)
            self.show_toast("✅ Файл выбран для шифрования")
            # Автоматически переключаем тип данных на "файл"
            self.encrypt_data_type.set("file")
            self._toggle_encrypt_input()

    def _toggle_encrypt_input(self):
        """Переключает между вводом текста и выбором файла"""
        if self.encrypt_data_type.get() == "text":
            self.encrypt_text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.encrypt_file_frame.pack_forget()
        else:
            self.encrypt_text_frame.pack_forget()
            self.encrypt_file_frame.pack(fill=tk.X, pady=(0, 10))

    def _paste_to_encrypt_text(self):
        """Вставляет текст из буфера обмена в поле шифрования"""
        try:
            text = self.root.clipboard_get()
            self.encrypt_text_input.delete("1.0", tk.END)
            self.encrypt_text_input.insert("1.0", text)
            self.show_toast("✅ Текст вставлен из буфера обмена")
        except tk.TclError:
            messagebox.showwarning("⚠️ Буфер пуст", "Буфер обмена не содержит текста")

    def _paste_to_decrypt_input(self):
        """Вставляет данные из буфера обмена в поле дешифрования"""
        try:
            data = self.root.clipboard_get()
            self.decrypt_input.delete("1.0", tk.END)
            self.decrypt_input.insert("1.0", data)
            self.show_toast("✅ Данные вставлены из буфера обмена")
            # Автоматически пытаемся определить алгоритм из данных
            self._auto_detect_algorithm(data)
        except tk.TclError:
            messagebox.showwarning("⚠️ Буфер пуст", "Буфер обмена не содержит данных")

    def _auto_detect_algorithm(self, data: str):
        """Пытается автоматически определить алгоритм из сериализованных данных"""
        try:
            encrypted_data = EncryptionManager.deserialize_encrypted_data(data.strip())
            algorithm = encrypted_data.get('algorithm', 'unknown')
            if algorithm != 'unknown' and algorithm in EncryptionManager.SUPPORTED_ALGORITHMS:
                self.show_toast(
                    f"🔍 Обнаружен алгоритм: {EncryptionManager.SUPPORTED_ALGORITHMS.get(algorithm, algorithm)}")
        except:
            pass  # Не удалось определить алгоритм - игнорируем

    def _start_encryption(self):
        """Запускает шифрование данных с поддержкой всех новых алгоритмов"""
        try:
            algorithm = self.encrypt_algorithm.get()

            # Получаем данные для шифрования
            if self.encrypt_data_type.get() == "text":
                data = self.encrypt_text_input.get("1.0", tk.END).strip().encode('utf-8')
                if not data:
                    raise ValueError("Введите текст для шифрования")
            else:
                file_path = self.encrypt_file_path.get()
                if not file_path or not os.path.exists(file_path):
                    raise ValueError("Выберите файл для шифрования")
                with open(file_path, 'rb') as f:
                    data = f.read()

            # Шифруем в зависимости от алгоритма
            if algorithm == 'aes_256_cbc':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для AES требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_aes_cbc(data, password)
            elif algorithm == 'aes_256_gcm':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для AES-GCM требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_aes_gcm(data, password)
            elif algorithm == 'aes_256_ctr':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для AES-CTR требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_aes_ctr(data, password)
            elif algorithm == 'aes_256_ofb':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для AES-OFB требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_aes_ofb(data, password)
            elif algorithm == 'chacha20':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для ChaCha20 требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_chacha20(data, password)
            elif algorithm == 'chacha20_poly1305':
                password = self.encrypt_password.get()
                if not password or len(password) < 8:
                    raise ValueError("Для ChaCha20-Poly1305 требуется надежный пароль (минимум 8 символов)")
                encrypted = EncryptionManager.encrypt_chacha20_poly1305(data, password)
            elif algorithm == 'xor':
                key = self.encrypt_password.get()
                if not key:
                    raise ValueError("Введите ключ для шифрования XOR")
                encrypted = EncryptionManager.encrypt_xor(data, key)
                messagebox.showwarning(
                    "⚠️ Внимание",
                    "XOR НЕ ЯВЛЯЕТСЯ НАДЕЖНЫМ ШИФРОВАНИЕМ!\n"
                    "Используйте только для образовательных целей."
                )
            elif algorithm == 'base64':
                encrypted = EncryptionManager.encrypt_base64(data)
                messagebox.showinfo(
                    "ℹ️ Информация",
                    "Base64 - это кодирование, НЕ шифрование!\n"
                    "Данные легко декодируются без пароля."
                )
            else:
                raise ValueError(f"Неизвестный алгоритм: {algorithm}")

            # Сериализуем результат
            serialized = EncryptionManager.serialize_encrypted_data(encrypted)

            # Отображаем результат
            self.encrypt_result.config(state='normal')
            self.encrypt_result.delete("1.0", tk.END)
            self.encrypt_result.insert("1.0", serialized)
            self.encrypt_result.config(state='disabled')

            self.show_toast("✅ Шифрование успешно завершено!")
            self.log_manager.add_entry("encryption", "success", {"algorithm": algorithm})

        except Exception as e:
            messagebox.showerror("❌ Ошибка шифрования", str(e))
            self.log_manager.add_entry("encryption", "error", {"error": str(e)})

    def _start_decryption(self):
        """Запускает дешифрование данных с поддержкой всех алгоритмов"""
        try:
            serialized = self.decrypt_input.get("1.0", tk.END).strip()
            if not serialized:
                raise ValueError("Введите зашифрованные данные или загрузите файл")

            # Десериализуем данные
            encrypted_data = EncryptionManager.deserialize_encrypted_data(serialized)
            algorithm = encrypted_data.get('algorithm', 'aes_256_cbc')

            # Дешифруем в зависимости от алгоритма
            if algorithm in ['aes_256_cbc', 'aes_256_gcm', 'aes_256_ctr', 'aes_256_ofb',
                             'chacha20', 'chacha20_poly1305']:
                password = self.decrypt_password.get()
                if not password:
                    raise ValueError("Введите пароль для дешифрования")

                if algorithm == 'aes_256_cbc':
                    decrypted = EncryptionManager.decrypt_aes_cbc(encrypted_data, password)
                elif algorithm == 'aes_256_gcm':
                    decrypted = EncryptionManager.decrypt_aes_gcm(encrypted_data, password)
                elif algorithm == 'aes_256_ctr':
                    decrypted = EncryptionManager.decrypt_aes_ctr(encrypted_data, password)
                elif algorithm == 'aes_256_ofb':
                    decrypted = EncryptionManager.decrypt_aes_ofb(encrypted_data, password)
                elif algorithm == 'chacha20':
                    decrypted = EncryptionManager.decrypt_chacha20(encrypted_data, password)
                elif algorithm == 'chacha20_poly1305':
                    decrypted = EncryptionManager.decrypt_chacha20_poly1305(encrypted_data, password)

            elif algorithm == 'xor':
                decrypted = EncryptionManager.decrypt_xor(encrypted_data)
                messagebox.showwarning(
                    "⚠️ Внимание",
                    "Данные расшифрованы алгоритмом XOR.\n"
                    "XOR НЕ ЯВЛЯЕТСЯ НАДЕЖНЫМ ШИФРОВАНИЕМ!"
                )

            elif algorithm == 'base64':
                decrypted = EncryptionManager.decrypt_base64(encrypted_data)

            else:
                raise ValueError(f"Неизвестный или неподдерживаемый алгоритм: {algorithm}")

            # Сохраняем оригинальные данные для последующего сохранения
            self.decrypt_result_data = decrypted

            # Отображаем результат
            self.decrypt_result.config(state='normal')
            self.decrypt_result.delete("1.0", tk.END)

            # Пытаемся декодировать как текст
            try:
                text = decrypted.decode('utf-8')
                self.decrypt_result.insert("1.0", text)
                self.decrypt_result_type = 'text'
            except UnicodeDecodeError:
                # Если это бинарные данные, показываем информацию
                self._display_binary_data(decrypted)

            self.decrypt_result.config(state='disabled')
            self.show_toast("✅ Дешифрование успешно завершено!")
            self.log_manager.add_entry("decryption", "success", {"algorithm": algorithm})

        except Exception as e:
            messagebox.showerror(
                "❌ Ошибка дешифрования",
                f"{str(e)}\n\n"
                "Возможные причины:\n"
                "• Неверный пароль\n"
                "• Поврежденные данные\n"
                "• Несовместимый алгоритм шифрования"
            )
            self.log_manager.add_entry("decryption", "error", {"error": str(e)})

    def _display_binary_data(self, data: bytes):
        """Отображает информацию о бинарных данных в поле результата"""
        info = EncryptionManager.identify_data_type(data)
        display_text = f"ТИП ДАННЫХ: {info['type'].upper()}\n\n"

        if info['type'] == 'image':
            display_text += f"Формат: {info['format']}\n"
            display_text += f"Размер: {info['dimensions']}\n"
            display_text += f"Режим: {info['mode']}\n"
            display_text += f"Размер файла: {info['size']} байт"
        elif info['type'] == 'audio':
            display_text += f"Каналы: {info['channels']}\n"
            display_text += f"Частота: {info['sample_rate']} Гц\n"
            display_text += f"Длительность: {info['duration']}\n"
            display_text += f"Размер файла: {info['size']} байт"
        elif info['type'] == 'archive':
            display_text += f"Тип архива: {info['type']}\n"
            display_text += f"Размер: {info['size']} байт"
        elif info['type'] == 'binary':
            display_text += f"Размер: {info['size']} байт\n"
            display_text += f"\nПервые 32 байта (hex):\n{data[:32].hex(' ')}"

        self.decrypt_result.insert("1.0", display_text)

    def _save_encrypted_data(self):
        """Сохраняет зашифрованные данные в файл"""
        data = self.encrypt_result.get("1.0", tk.END).strip()
        if not data:
            messagebox.showwarning("⚠️ Нет данных", "Нет зашифрованных данных для сохранения")
            return

        filepath = filedialog.asksaveasfilename(
            title="Сохранить зашифрованные данные",
            defaultextension=".ongcrypt",
            filetypes=[
                ("Occultong Encrypted", "*.ongcrypt"),
                ("JSON", "*.json"),
                ("Все файлы", "*.*")
            ],
            initialdir=self.last_open_dir
        )

        if filepath:
            try:
                # Если это .ongcrypt, сохраняем с сигнатурой
                if filepath.endswith('.ongcrypt'):
                    encrypted_data = EncryptionManager.deserialize_encrypted_data(data)
                    EncryptionManager.save_encrypted_file(encrypted_data, filepath)
                else:
                    # Сохраняем как обычный JSON
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(data)

                self.last_open_dir = os.path.dirname(filepath)
                self.show_toast(f"✅ Данные сохранены: {os.path.basename(filepath)}")
                self.log_manager.add_entry("file_save", "success", {"path": filepath, "type": "encrypted"})
            except Exception as e:
                messagebox.showerror("❌ Ошибка сохранения", str(e))
                self.log_manager.add_entry("file_save", "error", {"error": str(e)})

    def _load_encrypted_file(self):
        """Загружает зашифрованные данные из файла"""
        filepath = filedialog.askopenfilename(
            title="Загрузить зашифрованные данные",
            filetypes=[
                ("Occultong Encrypted", "*.ongcrypt"),
                ("JSON", "*.json"),
                ("Все файлы", "*.*")
            ],
            initialdir=self.last_open_dir
        )

        if filepath:
            try:
                if filepath.endswith('.ongcrypt'):
                    encrypted_data = EncryptionManager.load_encrypted_file(filepath)
                    serialized = EncryptionManager.serialize_encrypted_data(encrypted_data)
                else:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        serialized = f.read()

                self.decrypt_input.delete("1.0", tk.END)
                self.decrypt_input.insert("1.0", serialized)
                self.last_open_dir = os.path.dirname(filepath)
                self.show_toast(f"✅ Данные загружены: {os.path.basename(filepath)}")
                self.log_manager.add_entry("file_load", "success", {"path": filepath, "type": "encrypted"})
            except Exception as e:
                messagebox.showerror("❌ Ошибка загрузки", str(e))
                self.log_manager.add_entry("file_load", "error", {"error": str(e)})

    def _copy_decrypt_result(self):
        """Копирует результат дешифрования в буфер обмена"""
        if not hasattr(self, 'decrypt_result_data') or not self.decrypt_result_data:
            messagebox.showwarning("⚠️ Нет данных", "Нет данных для копирования")
            return

        try:
            # Пытаемся скопировать как текст
            text = self.decrypt_result_data.decode('utf-8')
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.show_toast("✅ Результат скопирован в буфер обмена")
        except UnicodeDecodeError:
            messagebox.showinfo(
                "ℹ️ Бинарные данные",
                "Результат содержит бинарные данные.\n"
                "Используйте кнопку 'Сохранить' для сохранения в файл."
            )

    def _save_decrypt_result(self):
        """Сохраняет результат дешифрования в файл"""
        if not hasattr(self, 'decrypt_result_data') or not self.decrypt_result_data:
            messagebox.showwarning("⚠️ Нет данных", "Нет данных для сохранения")
            return

        # Определяем тип данных для предложения правильного расширения
        info = EncryptionManager.identify_data_type(self.decrypt_result_data)
        default_ext = ".txt"
        filetypes = [("Все файлы", "*.*")]

        if info['type'] == 'image':
            default_ext = f".{info['format'].lower()}"
            filetypes.insert(0, (f"Изображение {info['format']}", f"*{default_ext}"))
        elif info['type'] == 'audio':
            default_ext = ".wav"
            filetypes.insert(0, ("Аудио WAV", "*.wav"))
        elif info['type'] == 'text':
            default_ext = ".txt"
            filetypes.insert(0, ("Текст", "*.txt"))
            filetypes.insert(1, ("JSON", "*.json"))

        filepath = filedialog.asksaveasfilename(
            title="Сохранить расшифрованные данные",
            defaultextension=default_ext,
            filetypes=filetypes,
            initialdir=self.last_open_dir
        )

        if filepath:
            try:
                with open(filepath, 'wb') as f:
                    f.write(self.decrypt_result_data)

                self.last_open_dir = os.path.dirname(filepath)
                self.show_toast(f"✅ Данные сохранены: {os.path.basename(filepath)}")
                self.log_manager.add_entry("file_save", "success", {"path": filepath, "type": "decrypted"})
            except Exception as e:
                messagebox.showerror("❌ Ошибка сохранения", str(e))
                self.log_manager.add_entry("file_save", "error", {"error": str(e)})

    def validate_before_hide(self) -> bool:
        import os
        img_path = self.img_path.get()
        if not img_path or not os.path.exists(img_path):
            messagebox.showerror("❌ Ошибка", "Изображение/контейнер не выбран или не существует")
            return False

        ext = os.path.splitext(img_path)[1].lower()
        if ext == ".wav":
            # WAV: не проверяем размер изображения.
            pass
        else:
            try:
                w, h, total_bits = ImageProcessor.get_image_info(img_path)
                if w < 100 or h < 100:
                    if messagebox.askyesno("⚠️ Предупреждение",
                                           "Изображение слишком маленькое. Рекомендуется использовать изображения размером не менее 100x100 пикселей.\
Все равно продолжить?"):
                        pass
                    else:
                        return False
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Ошибка проверки изображения: {str(e)}")
                return False

        # Дальнейшая проверка без изменений:
        if self.data_type.get() == "text":
            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("❌ Ошибка", "Текст для скрытия не введён")
                return False
        else:
            file_path = self.file_path_var.get()
            if not file_path or not os.path.exists(file_path):
                messagebox.showerror("❌ Ошибка", "Файл для скрытия не выбран или не существует")
                return False

        return True

    def start_hide(self) -> None:
        if self.buttons_disabled:
            return
        if not self.validate_before_hide():
            return
        self.operation_thread = threading.Thread(target=self.hide_data, daemon=True)
        self.operation_thread.start()

    def hide_data(self) -> None:
        try:
            self.set_progress_mode(True, "⏳ Подготовка данных...")
            self.toggle_buttons(False)
            self.cancel_event.clear()

            img_path = self.img_path.get()
            if not img_path or not os.path.exists(img_path):
                raise ValueError("❌ Изображение не выбрано или не существует")

            if self.data_type.get() == "text":
                text = self.text_input.get("1.0", tk.END).strip()
                if not text:
                    raise ValueError("❌ Текст для скрытия не введён")
                data = text.encode('utf-8')
                data_type = "text"
            else:
                file_path = self.file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    raise ValueError("❌ Файл для скрытия не выбран или не существует")
                with open(file_path, 'rb') as f:
                    data = f.read()
                data_type = "file"

            # Создаем резервную копию если включено
            if self.settings.get("auto_backup", True):
                backup_path = Utils.create_backup(img_path)
                if backup_path:
                    self.log_manager.add_entry("backup_created", "success",
                                               {"original": img_path, "backup": backup_path})

            ext = os.path.splitext(img_path)[1].lower()
            if ext == ".wav":
                output = filedialog.asksaveasfilename(
                    title="💾 Сохранить аудио с данными",
                    defaultextension=".wav",
                    filetypes=[("WAV аудиофайлы", "*.wav")],
                    initialdir=self.last_save_dir
                )
            else:
                output = filedialog.asksaveasfilename(
                    title="💾 Сохранить изображение с данными",
                    defaultextension=".png",
                    filetypes=[("PNG изображения", "*.png")],
                    initialdir=self.last_save_dir
                )

            if not output:
                self.set_progress_mode(False)
                self.toggle_buttons(True)
                return

            self.last_save_dir = os.path.dirname(output)

            required_space_mb = os.path.getsize(img_path) / (1024 * 1024) * 1.1
            free_space_mb = Utils.get_free_space_mb(os.path.dirname(output) or '.')
            if free_space_mb < required_space_mb:
                raise ValueError(
                    f"❌ Недостаточно свободного места на диске.\
Требуется: {Utils.format_size(required_space_mb * 1024 * 1024)}\
Доступно: {Utils.format_size(free_space_mb * 1024 * 1024)}")

            start_time = time.time()

            def progress_callback(progress: float) -> None:
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")
                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:
                    return
                self.last_progress_update_time = current_time
                elapsed_time = current_time - start_time
                speed = (len(data) * (progress / 100)) / elapsed_time if elapsed_time > 0 else 0
                self.root.after(0, lambda: self.progress_var.set(progress))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"⏳ Скрытие данных... {progress:.1f}% | Скорость: {Utils.format_size(speed)}/с"
                ))

            method = self.method_var.get()
            ImageProcessor.hide_data(
                img_path,
                data,
                "",
                output,
                method=method,
                compression_level=self.compression_level.get(),
                progress_callback=progress_callback,
                cancel_event=self.cancel_event
            )

            # Записываем статистику
            file_ext = os.path.splitext(img_path)[1].lower()
            self.analytics_manager.record_operation("hide", True, method=method, file_type=file_ext)
            self.log_manager.add_entry("hide", "success", {
                "method": method,
                "data_type": data_type,
                "data_size": len(data),
                "container": img_path,
                "output": output
            })

            # Обновляем счетчики
            self.operations_count += 1
            self.operations_label.config(text=f"📊 Операций: {self.operations_count}")

            def after_success():
                messagebox.showinfo(
                    "✅ Успех",
                    f"🎉 Данные успешно скрыты в {'аудиофайле' if ext == '.wav' else 'изображении'}!\
            Файл сохранён: {output}"
                )
                if messagebox.askyesno("📂 Открыть папку", "Открыть папку с сохраненным файлом?"):
                    Utils.open_in_file_manager(output)


            self.root.after(0, after_success)

        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("⛔ Отмена", "Операция скрытия данных была отменена."))
                self.log_manager.add_entry("hide", "error", {"error": "Операция отменена пользователем"})
            else:
                error_msg = f"Произошла ошибка при скрытии данных:\
{str(e)}"
                if "too small" in str(e).lower() or "слишком мало" in str(e).lower():
                    error_msg += "\
💡 Возможные причины:\
- Изображение слишком маленькое для объема данных.\
- Выбран неверный метод скрытия."
                    error_msg += "\
🛠️ Решения:\
- Используйте изображение большего размера.\
- Попробуйте другой метод скрытия данных."
                elif "not enough space" in str(e).lower() or "недостаточно" in str(e).lower():
                    error_msg += "\
💡 Возможные причины:\
- Недостаточно свободного места на диске."
                    error_msg += "\
🛠️ Решения:\
- Освободите место на диске и повторите попытку."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\
💡 Возможные причины:\
- Указанный файл не существует или был перемещен."
                    error_msg += "\
🛠️ Решения:\
- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", error_msg))
                self.log_manager.add_entry("hide", "error", {"error": str(e)})

        finally:
            self.set_progress_mode(False)
            self.toggle_buttons(True)

    def start_extract(self) -> None:
        if self.buttons_disabled:
            return
        self.operation_thread = threading.Thread(target=self.extract_data, daemon=True)
        self.operation_thread.start()

    def extract_data(self) -> None:
        try:
            self.set_progress_mode(True, "⏳ Подготовка к извлечению...")
            self.toggle_buttons(False)
            self.cancel_event.clear()

            path = self.extract_img_path.get()
            if not path or not os.path.exists(path):
                raise ValueError("❌ Файл не выбран или не существует")

            start_time = time.time()

            def progress_callback(progress, message=None):
                if self.cancel_event.is_set():
                    raise Exception("Операция отменена пользователем")
                current_time = time.time()
                if current_time - self.last_progress_update_time < 0.1 and progress < 100:
                    return
                self.last_progress_update_time = current_time
                self.root.after(0, lambda: self.progress_var.set(progress))
                status_text = message if message else f"⏳ Извлечение данных... {progress:.1f}%"
                self.root.after(0, lambda: self.status_label.config(text=status_text))

            ext = os.path.splitext(path)[1].lower()
            if ext == ".wav":
                extracted = ImageProcessor.extract_data(
                    path,
                    "",
                    "audio_lsb",
                    progress_callback,
                    self.cancel_event
                )
                method = "audio_lsb"
            else:
                extracted = ImageProcessor.extract_data(
                    path,
                    "",
                    None,
                    progress_callback,
                    self.cancel_event
                )
                method = "auto_detect"

            # Пытаемся распознать как текст
            try:
                text = extracted.decode('utf-8')
                self.current_extracted = ('text', text)
                self.last_extracted_hash = hashlib.sha256(extracted).hexdigest()
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert("1.0", text))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
                self.root.after(0, lambda: self.copy_button.config(state="normal"))
                self.root.after(0, lambda: self.save_button.config(state="normal"))
                self.root.after(0, lambda: self.copy_hash_button.config(state="normal"))
                self.root.after(0, lambda: self.open_file_button.config(state="disabled"))
                self.show_toast("✅ Текст успешно извлечён")
            except UnicodeDecodeError:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(extracted)
                    tmp_file_path = tmp_file.name
                mime_type, encoding = mimetypes.guess_type(tmp_file_path)
                if mime_type:
                    ext = mimetypes.guess_extension(mime_type)
                    if ext:
                        new_name = tmp_file_path + ext
                        os.rename(tmp_file_path, new_name)
                        tmp_file_path = new_name
                self.current_extracted = ('binary', tmp_file_path)
                hex_hash = hashlib.sha256(extracted).hexdigest()
                self.last_extracted_hash = hex_hash
                self.root.after(0, lambda: self.result_text.config(state='normal'))
                self.root.after(0, lambda: self.result_text.delete("1.0", tk.END))
                self.root.after(0, lambda: self.result_text.insert(
                    "1.0",
                    f"📦 Бинарные данные: {len(extracted)} байт\
" +
                    f"🔑 Хеш SHA-256: {hex_hash}\
" +
                    f"📁 Временный файл: {tmp_file_path}"
                ))
                self.root.after(0, lambda: self.result_text.config(state='disabled'))
                self.root.after(0, lambda: self.save_button.config(state="normal"))
                self.root.after(0, lambda: self.copy_button.config(state="disabled"))
                self.root.after(0, lambda: self.copy_hash_button.config(state="normal"))
                self.root.after(0, lambda: self.open_file_button.config(state="normal"))
                self.show_toast("✅ Бинарные данные извлечены")

            self.save_to_history(path)

            # Записываем статистику
            file_ext = os.path.splitext(path)[1].lower()
            self.analytics_manager.record_operation("extract", True, method=method, file_type=file_ext)
            self.log_manager.add_entry("extract", "success", {
                "method": method,
                "data_size": len(extracted),
                "container": path,
                "data_type": "text" if isinstance(self.current_extracted[1], str) else "binary"
            })

            # Обновляем счетчики
            self.operations_count += 1
            self.operations_label.config(text=f"📊 Операций: {self.operations_count}")


        except Exception as e:
            if str(e) == "Операция отменена пользователем":
                self.root.after(0, lambda: messagebox.showinfo("⛔ Отмена", "Операция извлечения данных была отменена."))
                self.log_manager.add_entry("extract", "error", {"error": "Операция отменена пользователем"})
            else:
                error_msg = f"Произошла ошибка при извлечении данных:\
{str(e)}"
                if "incorrect data length" in str(e).lower() or "некорректная длина данных" in str(e).lower():
                    error_msg += "\
💡 Возможные причины:\
- В изображении нет скрытых данных.\
- Использован неверный пароль (если применяется).\
- Изображение повреждено или изменено после скрытия данных."
                    error_msg += "\
🛠️ Решения:\
- Убедитесь, что вы используете правильное изображение.\
- Проверьте правильность введенного пароля.\
- Попробуйте извлечь данные другим методом."
                elif "file not found" in str(e).lower() or "не найден" in str(e).lower():
                    error_msg += "\
💡 Возможные причины:\
- Указанный файл не существует или был перемещен."
                    error_msg += "\
🛠️ Решения:\
- Проверьте путь к файлу и повторите попытку."

                self.root.after(0, lambda: messagebox.showerror("❌ Ошибка", error_msg))
                self.log_manager.add_entry("extract", "error", {"error": str(e)})

        finally:
            self.set_progress_mode(False)
            self.toggle_buttons(True)

    def save_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("❌ Ошибка", "Сначала извлеките данные")
            return

        data_type, content = self.current_extracted
        if data_type == 'text':
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")],
                initialdir=self.last_save_dir
            )
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.last_save_dir = os.path.dirname(path)
                messagebox.showinfo("✅ Сохранено", f"Текст сохранён в файл: {path}")
                self.log_manager.add_entry("save_extracted", "success", {"file": path, "type": "text"})
        else:
            mime_type, encoding = mimetypes.guess_type(content)
            default_ext = ".bin"
            filetypes = [("Бинарные файлы", "*.bin"), ("Все файлы", "*.*")]
            if mime_type:
                ext = mimetypes.guess_extension(mime_type)
                if ext:
                    default_ext = ext
                    desc = mime_type.split('/')[0].capitalize() + " файлы"
                    filetypes.insert(0, (desc, f"*{ext}"))

            path = filedialog.asksaveasfilename(
                defaultextension=default_ext,
                filetypes=filetypes,
                initialdir=self.last_save_dir
            )
            if path:
                shutil.copy(content, path)
                self.last_save_dir = os.path.dirname(path)
                messagebox.showinfo("✅ Сохранено", f"Данные сохранены в файл: {path}")
                self.log_manager.add_entry("save_extracted", "success", {"file": path, "type": "binary"})

    def copy_extracted(self) -> None:
        if not self.current_extracted:
            messagebox.showerror("❌ Ошибка", "Нет данных для копирования")
            return

        data_type, content = self.current_extracted
        if data_type == 'text':
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.status_label.config(text="📋 Текст скопирован в буфер обмена")
            self.show_toast("✅ Скопировано в буфер обмена")
            self.log_manager.add_entry("copy_extracted", "success", {"type": "text", "length": len(content)})
        else:
            messagebox.showwarning("⚠️ Внимание", "Бинарные данные нельзя скопировать в буфер")

    def open_extracted_file(self) -> None:
        if not self.current_extracted:
            return
        data_type, content = self.current_extracted
        if data_type == 'binary' and content and os.path.exists(content):
            Utils.open_in_default_app(content)
            self.log_manager.add_entry("open_extracted_file", "success", {"file": content})
        else:
            messagebox.showwarning("❌ Нет файла", "Нет бинарного файла для открытия.")

    def copy_extracted_hash(self) -> None:
        if self.last_extracted_hash:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_extracted_hash)
            self.show_toast("✅ Хеш скопирован в буфер обмена")
            self.log_manager.add_entry("copy_hash", "success", {"hash": self.last_extracted_hash[:16] + "..."})

    def set_progress_mode(self, active: bool, message: str = None) -> None:
        if active:
            self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True)
            self.cancel_button.pack(side=tk.RIGHT, padx=(10, 0))
            self.progress_var.set(0)
            self.progress_bar.start_animation()
            if message:
                self.status_label.config(text=message)
                self.status_indicator.config(fg=self.colors["warning"])
        else:
            self.progress_bar.stop_animation()
            self.progress_bar.pack_forget()
            self.cancel_button.pack_forget()
            self.progress_var.set(0)
            self.status_label.config(text="✅ Готов к работе")
            self.status_indicator.config(fg=self.colors["success"])

    def toggle_buttons(self, enable: bool) -> None:
        self.buttons_disabled = not enable
        state = "normal" if enable else "disabled"

        # Основные кнопки
        if hasattr(self, 'hide_button'):
            self.hide_button.config(state=state)
        if hasattr(self, 'extract_button'):
            self.extract_button.config(state=state)

        # Кнопки извлечения
        if enable and self.current_extracted:
            data_type, content = self.current_extracted
            if hasattr(self, 'save_button'):
                self.save_button.config(state="normal")
            if hasattr(self, 'copy_hash_button'):
                self.copy_hash_button.config(state="normal")
            if data_type == 'text':
                if hasattr(self, 'copy_button'):
                    self.copy_button.config(state="normal")
                if hasattr(self, 'open_file_button'):
                    self.open_file_button.config(state="disabled")
            else:
                if hasattr(self, 'copy_button'):
                    self.copy_button.config(state="disabled")
                if hasattr(self, 'open_file_button'):
                    self.open_file_button.config(state="normal")
        else:
            if hasattr(self, 'save_button'):
                self.save_button.config(state=state if self.current_extracted else "disabled")
            if hasattr(self, 'copy_button'):
                self.copy_button.config(
                    state=state if (self.current_extracted and self.current_extracted[0] == 'text') else "disabled")
            if hasattr(self, 'open_file_button'):
                self.open_file_button.config(
                    state=state if (self.current_extracted and self.current_extracted[0] == 'binary') else "disabled")
            if hasattr(self, 'copy_hash_button'):
                self.copy_hash_button.config(state=state if self.current_extracted else "disabled")

        # Кнопки настроек
        if hasattr(self, 'save_settings_button'):
            self.save_settings_button.config(state=state)
        if hasattr(self, 'reset_settings_button'):
            self.reset_settings_button.config(state=state)

    def cancel_operation(self) -> None:
        self.cancel_event.set()
        self.status_label.config(text="⛔ Отмена операции...")
        self.status_indicator.config(fg=self.colors["error"])
        self.log_manager.add_entry("operation_cancelled", "info", {})

    def refresh_history(self) -> None:
        for i, lbl in enumerate(self.history_labels):
            if i < len(self.history):
                path = self.history[i]
                truncated_path = Utils.truncate_path(path)
                file_info = Utils.get_file_info(path)
                size_info = f" ({file_info['size_formatted']})" if 'size_formatted' in file_info else ""

                lbl.config(
                    text=f"📌 {i + 1}. {truncated_path}{size_info}",
                    style="History.TLabel"
                )
                lbl.bind("<Button-1>", lambda e, idx=i: self.load_from_history(idx))
                lbl.bind("<Button-3>", lambda e, idx=i: self.show_history_menu(e, idx))
                lbl.bind("<Double-Button-1>", lambda e, p=path: Utils.open_in_default_app(p))
            else:
                lbl.config(text="", cursor="")
                lbl.unbind("<Button-1>")
                lbl.unbind("<Button-3>")
                lbl.unbind("<Double-Button-1>")

    def show_history_menu(self, event, idx: int) -> None:
        if not self.history_menu:
            self.history_menu = tk.Menu(self.root, tearoff=0)
            self.history_menu.add_command(label="🔍 Открыть",
                                          command=lambda: self.load_from_history(self.history_menu.index))
            self.history_menu.add_command(label="🖼️ Предпросмотр",
                                          command=lambda: self.preview_from_history(self.history_menu.index))
            self.history_menu.add_command(label="📁 Открыть папку",
                                          command=lambda: self.open_history_folder(self.history_menu.index))
            self.history_menu.add_separator()
            self.history_menu.add_command(label="🗑️ Удалить из истории",
                                          command=lambda: self.remove_history_item(self.history_menu.index))
        self.history_menu.index = idx
        try:
            self.history_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.history_menu.grab_release()

    def preview_from_history(self, idx: int) -> None:
        if 0 <= idx < len(self.history):
            path = self.history[idx]
            if os.path.exists(path):
                self.show_image_preview(path)

    def open_history_folder(self, idx: int) -> None:
        if 0 <= idx < len(self.history):
            Utils.open_in_file_manager(self.history[idx])

    def remove_history_item(self, idx: int) -> None:
        if 0 <= idx < len(self.history):
            del self.history[idx]
            self.save_history(self.history)
            self.refresh_history()

    def load_from_history(self, idx: int) -> None:
        if idx < len(self.history):
            path = self.history[idx]
            if os.path.exists(path):
                self.extract_img_path.set(path)
                self.update_thumbnail(path, self.extract_preview)
            else:
                messagebox.showwarning("❌ Файл не найден", "Файл был перемещён или удалён.")
                del self.history[idx]
                self.refresh_history()

    def change_theme(self, theme_name: str) -> None:
        self.theme_manager.set_theme(theme_name)
        self.colors = self.theme_manager.colors
        self.refresh_history()
        if hasattr(self, 'status_label'):
            self.status_label.config(foreground=self.colors["text_secondary"])
        self.check_theme_contrast()

        # Обновляем цвета для текстовых полей
        if self.text_input:
            self.text_input.config(
                bg=self.colors["card"],
                fg=self.colors["text"],
                insertbackground=self.colors["fg"],
                selectbackground=self.colors["accent"],
                selectforeground="#ffffff"
            )
        if self.result_text:
            self.result_text.config(
                bg=self.colors["card"],
                fg=self.colors["text"],
                insertbackground=self.colors["fg"],
                selectbackground=self.colors["accent"],
                selectforeground="#ffffff"
            )
        if self.toast_label:
            self.toast_label.config(
                bg=self.colors.get("shadow", "#333333"),
                fg=self.colors.get("text", "#ffffff"),
                highlightcolor=self.colors.get("accent", "#58A6FF")
            )

        # Сохраняем настройки
        self.settings["theme"] = theme_name
        self.save_settings()

    def check_theme_contrast(self) -> None:
        c = self.colors
        contrast_ratio = Utils.get_contrast_ratio(c["fg"], c["bg"])
        if contrast_ratio < 4.5:
            print(
                f"⚠️ Предупреждение: Низкая контрастность текста и фона в теме '{self.theme_manager.current_theme}'."
            )

    def save_settings_ui(self) -> None:
        # Обновляем настройки
        self.settings["show_tips"] = self.show_tips_var.get()
        self.settings["auto_backup"] = self.auto_backup_var.get()
        self.settings["confirm_before_exit"] = self.confirm_exit_var.get()

        self.save_settings()
        messagebox.showinfo(
            "✅ Настройки сохранены",
            "Настройки успешно применены.\
Некоторые изменения вступят в силу после перезапуска программы."
        )
        self.log_manager.add_entry("settings_saved", "success", {"settings": "user_interface"})

    def reset_settings(self) -> None:
        if messagebox.askyesno(
                "🔄 Подтверждение сброса",
                "Вы уверены, что хотите сбросить все настройки к значениям по умолчанию?\
Это действие нельзя отменить."
        ):
            try:
                if os.path.exists(CONFIG["SETTINGS_FILE"]):
                    os.remove(CONFIG["SETTINGS_FILE"])
                if os.path.exists(CONFIG["HISTORY_FILE"]):
                    os.remove(CONFIG["HISTORY_FILE"])
                if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                        self.temp_extracted_file.name):
                    os.unlink(self.temp_extracted_file.name)
                messagebox.showinfo(
                    "🔄 Сброс настроек",
                    "Настройки сброшены. Программа будет закрыта."
                )
                self.log_manager.add_entry("settings_reset", "success", {})
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось сбросить настройки: {e}")

    def export_settings(self):
        """Экспортирует настройки в файл"""
        path = filedialog.asksaveasfilename(
            title="Экспортировать настройки",
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            initialdir=self.last_save_dir
        )
        if path:
            try:
                # Экспортируем только пользовательские настройки, без служебных
                export_settings = {
                    "theme": self.settings.get("theme", "Тёмная"),
                    "method": self.settings.get("method", "lsb"),
                    "data_type": self.settings.get("data_type", "text"),
                    "compression_level": self.settings.get("compression_level", 9),
                    "show_tips": self.settings.get("show_tips", True),
                    "auto_backup": self.settings.get("auto_backup", True),
                    "confirm_before_exit": self.settings.get("confirm_before_exit", True),
                    "export_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "version": VERSION
                }
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(export_settings, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("✅ Экспорт", f"Настройки успешно экспортированы в файл:\
{path}")
                self.log_manager.add_entry("settings_exported", "success", {"file": path})
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось экспортировать настройки: {e}")

    def import_settings(self):
        """Импортирует настройки из файла"""
        path = filedialog.askopenfilename(
            title="Импортировать настройки",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            initialdir=self.last_open_dir
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)

                # Проверяем версию
                if imported_settings.get("version", "0.0.0") > VERSION:
                    if not messagebox.askyesno("⚠️ Внимание",
                                               "Импортируемые настройки созданы в более новой версии программы.\
                       Это может вызвать проблемы. Продолжить?"):
                        return

                # Обновляем настройки
                for key in ["theme", "method", "data_type", "compression_level",
                            "show_tips", "auto_backup", "confirm_before_exit"]:
                    if key in imported_settings:
                        self.settings[key] = imported_settings[key]

                # Применяем настройки
                self.theme_manager.set_theme(self.settings.get("theme", "Тёмная"))
                self.method_var.set(self.settings.get("method", "lsb"))
                self.data_type.set(self.settings.get("data_type", "text"))
                self.compression_level.set(self.settings.get("compression_level", 9))

                # Обновляем чекбоксы
                if hasattr(self, 'show_tips_var'):
                    self.show_tips_var.set(self.settings.get("show_tips", True))
                if hasattr(self, 'auto_backup_var'):
                    self.auto_backup_var.set(self.settings.get("auto_backup", True))
                if hasattr(self, 'confirm_exit_var'):
                    self.confirm_exit_var.set(self.settings.get("confirm_before_exit", True))


                # Сохраняем настройки
                self.save_settings()

                messagebox.showinfo("✅ Импорт", "Настройки успешно импортированы.\
Некоторые изменения вступят в силу после перезапуска программы.")
                self.log_manager.add_entry("settings_imported", "success", {"file": path})

            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось импортировать настройки: {e}")

    def refresh_statistics(self):
        """Обновляет статистику"""
        # 1. Перезагружаем данные
        self.analytics_manager = AnalyticsManager()
        self.log_manager = HistoryLog()

        # 2. Очищаем содержимое существующей вкладки (НЕ удаляем саму вкладку!)
        for widget in self.statistics_tab.winfo_children():
            widget.destroy()

        # 3. Воссоздаем UI ВНУТРИ существующей вкладки.
        # Этот код повторяет логику из create_statistics_tab, но не создает новую вкладку,
        # а наполняет уже существующую (self.statistics_tab).
        parent_frame = self.statistics_tab

        # Создаем canvas с прокруткой
        stats_canvas = tk.Canvas(parent_frame, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=stats_canvas.yview)
        scrollable_frame = ttk.Frame(stats_canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: stats_canvas.configure(scrollregion=stats_canvas.bbox("all"))
        )

        stats_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        stats_canvas.configure(yscrollcommand=scrollbar.set)

        stats_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Общая статистика
        summary_group = ttk.LabelFrame(
            scrollable_frame,
            text="📈 Общая статистика",
            padding=15,
            style="Card.TLabelframe"
        )
        summary_group.pack(fill=tk.X, pady=(0, 15))

        summary = self.analytics_manager.get_summary()
        log_stats = self.log_manager.get_statistics()

        stats_info = [
            ("Всего операций", log_stats.get("total_operations", 0)),
            ("Успешных операций", log_stats.get("successful_operations", 0)),
            ("Операций с ошибками", log_stats.get("failed_operations", 0)),
            ("Процент успешных", f"{log_stats.get('success_rate', 0):.1f}%"),
            ("Операций скрытия", log_stats.get("operation_stats", {}).get("hide", {}).get("total", 0)),
            ("Операций извлечения", log_stats.get("operation_stats", {}).get("extract", {}).get("total", 0)),
            ("Последняя операция", log_stats.get("last_operation", "Никогда")),
            ("Сессий использования", self.analytics_manager.stats.get("sessions", 0)),
            ("Самый популярный метод", summary.get("most_used_method", "Нет данных")),
            ("Самый часто скрываемый тип файлов", summary.get("most_hidden_file_type", "Нет данных"))
        ]

        for i, (label, value) in enumerate(stats_info):
            row_frame = ttk.Frame(summary_group, style="Card.TFrame")
            row_frame.pack(fill=tk.X, pady=(5, 0))
            ttk.Label(row_frame, text=f"{label}:", font=("Segoe UI", 10, "bold"), style="TLabel").pack(side=tk.LEFT,
                                                                                                       padx=(0, 10))
            ttk.Label(row_frame, text=str(value), font=("Segoe UI", 10), style="Secondary.TLabel").pack(side=tk.LEFT)

        # Статистика по методам
        methods_group = ttk.LabelFrame(scrollable_frame, text="📊 Статистика по методам", padding=15,
                                       style="Card.TLabelframe")
        methods_group.pack(fill=tk.X, pady=(0, 15))
        methods_data = self.analytics_manager.stats.get("methods_used", {})
        if methods_data:
            total = sum(methods_data.values())
            for method, count in methods_data.items():
                method_name = STEGANO_METHODS.get(method, method)
                method_frame = ttk.Frame(methods_group, style="Card.TFrame")
                method_frame.pack(fill=tk.X, pady=(2, 2))
                ttk.Label(method_frame, text=f"{method_name}:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))
                progress = ttk.Progressbar(method_frame, orient="horizontal", length=200, mode="determinate",
                                           style="TProgressbar")
                progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
                percentage = (count / total * 100) if total > 0 else 0
                progress["value"] = percentage
                ttk.Label(method_frame, text=f"{count} ({percentage:.1f}%)", style="Secondary.TLabel").pack(
                    side=tk.RIGHT)
        else:
            ttk.Label(methods_group, text="Нет данных для отображения", style="Secondary.TLabel").pack(pady=10)

        # История операций
        history_group = ttk.LabelFrame(scrollable_frame, text="📋 История операций", padding=15,
                                       style="Card.TLabelframe")
        history_group.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        recent_operations = self.log_manager.get_entries(20)
        if recent_operations:
            history_text = scrolledtext.ScrolledText(history_group, height=15, font=("Consolas", 9), wrap=tk.WORD,
                                                     bg=self.colors["card"], fg=self.colors["text"],
                                                     insertbackground=self.colors["fg"],
                                                     selectbackground=self.colors["accent"], selectforeground="#ffffff",
                                                     relief="flat", borderwidth=1)
            history_text.pack(fill=tk.BOTH, expand=True)
            for op in recent_operations:
                status_icon = "✅" if op["status"] == "success" else "❌"
                status_color = "success" if op["status"] == "success" else "error"
                history_text.insert(tk.END, f"{status_icon} {op['formatted_time']} | ", status_color)
                history_text.insert(tk.END, f"{op['operation_type']} | ")
                history_text.insert(tk.END, f"{op['status']}")
                if op["details"]:
                    details_str = " | ".join([f"{k}: {v}" for k, v in op["details"].items()])
                    history_text.insert(tk.END, f"  Детали: {details_str}")
                history_text.insert(tk.END, "\n" + "-" * 80 + "\n")
            history_text.tag_configure("success", foreground=self.colors["success"])
            history_text.tag_configure("error", foreground=self.colors["error"])
            history_text.config(state='disabled')
        else:
            ttk.Label(history_group, text="История операций пуста", style="Secondary.TLabel").pack(pady=10)

        # Кнопки управления
        btn_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="🔄 Обновить статистику", style="TButton", command=self.refresh_statistics).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="📤 Экспортировать статистику", style="TButton", command=self.export_statistics).pack(
            side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="🗑️ Очистить историю", style="TButton", command=self.clear_statistics).pack(
            side=tk.LEFT, padx=10)

        # 4. Переключаемся на вкладку, чтобы пользователь видел результат
        self.notebook.select(self.statistics_tab)
        messagebox.showinfo("✅ Обновление", "Статистика успешно обновлена!")

    def export_statistics(self):
        """Экспортирует статистику в файл"""
        path = filedialog.asksaveasfilename(
            title="Экспортировать статистику",
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            initialdir=self.last_save_dir
        )
        if path:
            try:
                stats_data = {
                    "analytics": self.analytics_manager.stats,
                    "operation_log": self.log_manager.log,
                    "export_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "version": VERSION
                }
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(stats_data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("✅ Экспорт", f"Статистика успешно экспортирована в файл:\
{path}")
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось экспортировать статистику: {e}")

    def clear_statistics(self):
        """Очищает статистику"""
        if messagebox.askyesno("🗑️ Подтверждение",
                               "Вы уверены, что хотите очистить всю статистику и историю операций?"):
            try:
                # Очищаем файлы
                if os.path.exists("stego_analytics.json"):
                    os.remove("stego_analytics.json")
                if os.path.exists("operation_log.json"):
                    os.remove("operation_log.json")

                # Пересоздаем менеджеры
                self.analytics_manager = AnalyticsManager()
                self.log_manager = HistoryLog()

                # Обновляем вкладку
                if hasattr(self, 'statistics_tab'):
                    for widget in self.statistics_tab.winfo_children():
                        widget.destroy()
                    self.create_statistics_tab()

                messagebox.showinfo("✅ Очистка", "Статистика и история операций успешно очищены!")
            except Exception as e:
                messagebox.showerror("❌ Ошибка", f"Не удалось очистить статистику: {e}")


    def show_help(self) -> None:
        """Показывает помощь"""
        self.notebook.select(self.help_tab)

    def show_container_info(self):
        path = self.img_path.get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("❌ Ошибка", "Сначала выберите контейнер")
            return

        file_info = Utils.get_file_info(path)
        ext = os.path.splitext(path)[1].lower()

        info_text = f"""
    📁 Информация о контейнере
    Имя файла: {file_info['name']}
    Размер: {file_info['size_formatted']}
    Тип: {file_info['type']}
    Дата создания: {file_info['created']}
    Дата изменения: {file_info['modified']}
    """

        if ext in ['.jpg', '.jpeg']:
            info_text += """
    ⚠️ ВАЖНО ДЛЯ JPEG:
    • Для метода JPEG DCT требуется сохранение с качеством 100%
    • Любое пересохранение с качеством < 100% уничтожит скрытые данные
    • Рекомендуется использовать оригинальные JPEG файлы без повторной обработки
    """

        if file_info['type'] == "image":
            info_text += f"""
🖼️ Информация об изображении
Размеры: {file_info.get('dimensions', 'N/A')}
Цветовой режим: {file_info.get('mode', 'N/A')}
"""
        elif file_info['type'] == "audio":
            info_text += f"""
🎵 Информация об аудио
Каналы: {file_info.get('channels', 'N/A')}
Частота дискретизации: {file_info.get('sample_rate', 'N/A')} Hz
Количество сэмплов: {file_info.get('frames', 'N/A')}
Длительность: {file_info.get('duration', 'N/A')}
"""

        messagebox.showinfo("ℹ️ Информация о контейнере", info_text)

    def show_extract_container_info(self):
        """Показывает информацию о контейнере для извлечения"""
        path = self.extract_img_path.get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("❌ Ошибка", "Сначала выберите контейнер")
            return

        self.show_container_info()

    def analyze_extracted_data(self):
        """Анализирует извлеченные данные"""
        if not self.current_extracted:
            messagebox.showwarning("❌ Ошибка", "Сначала извлеките данные")
            return

        data_type, content = self.current_extracted
        analysis_text = f"""
📊 Анализ извлеченных данных

Тип данных: {'Текст' if data_type == 'text' else 'Бинарные данные'}
"""

        if data_type == 'text':
            text = content
            lines = text.count('\n') + 1
            words = len(text.split())
            chars = len(text)
            bytes_size = len(text.encode('utf-8'))

            analysis_text += f"""
🔤 Текстовая статистика
Строк: {lines}
Слов: {words}
Символов: {chars}
Размер в байтах: {Utils.format_size(bytes_size)}

🔤 Частотный анализ (топ-5 символов)
"""
            # Подсчет частоты символов
            char_freq = {}
            for char in text:
                char_freq[char] = char_freq.get(char, 0) + 1

            # Сортировка по частоте
            sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:5]

            for char, freq in sorted_chars:
                if char == '\n':
                    char_display = '\\n'
                elif char == '\t':
                    char_display = '\\t'
                elif char == ' ':
                    char_display = 'пробел'
                else:
                    char_display = char
                analysis_text += f"{char_display}: {freq} раз(а)"

        else:
            # Бинарные данные
            file_path = content
            file_size = os.path.getsize(file_path)
            file_ext = os.path.splitext(file_path)[1].lower()

            analysis_text += f"""
📦 Бинарные данные
Размер файла: {Utils.format_size(file_size)}
Расширение: {file_ext}
Хеш SHA-256: {self.last_extracted_hash}

"""

            # Попытка определить тип файла
            mime_type, encoding = mimetypes.guess_type(file_path)
            if mime_type:
                analysis_text += f"MIME тип: {mime_type}"

            # Если это изображение, показываем дополнительную информацию
            if file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga']:
                try:
                    with Image.open(file_path) as img:
                        analysis_text += f"""
🖼️ Информация об изображении
Размеры: {img.width}x{img.height}
Цветовой режим: {img.mode}
"""
                except:
                    pass
            elif file_ext == '.wav':
                try:
                    with wave.open(file_path, 'rb') as wav:
                        analysis_text += f"""
🎵 Информация об аудио
Каналы: {wav.getnchannels()}
Частота дискретизации: {wav.getframerate()} Hz
Количество сэмплов: {wav.getnframes()}
Длительность: {wav.getnframes() / wav.getframerate():.2f} сек
"""
                except:
                    pass

        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("📊 Анализ данных")
        analysis_window.geometry("600x500")
        analysis_window.transient(self.root)
        analysis_window.grab_set()

        text_area = scrolledtext.ScrolledText(
            analysis_window,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg=self.colors["card"],
            fg=self.colors["text"],
            insertbackground=self.colors["fg"],
            selectbackground=self.colors["accent"],
            selectforeground="#ffffff",
            relief="flat",
            borderwidth=1
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert(tk.END, analysis_text)
        text_area.config(state=tk.DISABLED)

        close_btn = ttk.Button(analysis_window, text="❌ Закрыть", command=analysis_window.destroy)
        close_btn.pack(pady=10)

    def clear_history(self):
        """Очищает историю"""
        if messagebox.askyesno("🗑️ Подтверждение", "Вы уверены, что хотите очистить историю файлов?"):
            self.history = []
            self.save_history(self.history)
            self.refresh_history()
            messagebox.showinfo("✅ Очистка", "История успешно очищена!")

    def show_templates(self):
        """Показывает шаблоны текста"""
        templates = {
            "Пустой шаблон": "",
            "Текстовое сообщение": "Секретное сообщение: \n\nДата: \n\nПодпись: ",
            "Координаты": "Координаты: \nШирота: \nДолгота: \n\nОписание: ",
            "Пароли": "Сервис: \nЛогин: \nПароль: \n\nПримечание: ",
            "Финансовые данные": "Сумма: \nВалюта: \nДата: \n\nНазначение: ",
            "Контактная информация": "Имя: \nТелефон: \nEmail: \n\nАдрес: ",
            "Заметка": "Заголовок: \n\nТекст: \n\nТеги: ",
            "Список задач": "Задачи:\n1. \n2. \n3. \n\nПриоритет: ",
            "Код доступа": "Код: \n\nДействует до: \n\nНазначение: ",
            "Секретный ключ": "Ключ: \n\nАлгоритм: \n\nДлина: "
        }

        template_window = tk.Toplevel(self.root)
        template_window.title("📝 Шаблоны текста")
        template_window.geometry("500x400")
        template_window.transient(self.root)
        template_window.grab_set()

        ttk.Label(
            template_window,
            text="Выберите шаблон:",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(10, 5))

        template_var = tk.StringVar()
        template_combo = ttk.Combobox(
            template_window,
            textvariable=template_var,
            values=list(templates.keys()),
            state="readonly",
            width=40
        )
        template_combo.pack(pady=5)
        template_combo.set("Пустой шаблон")

        preview_frame = ttk.LabelFrame(template_window, text="Предпросмотр", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        preview_text = tk.Text(
            preview_frame,
            height=10,
            font=("Consolas", 10),
            wrap=tk.WORD,
            bg=self.colors["card"],
            fg=self.colors["text"]
        )
        preview_text.pack(fill=tk.BOTH, expand=True)
        preview_text.insert("1.0", templates["Пустой шаблон"])
        preview_text.config(state="disabled")

        def update_preview(event=None):
            selected = template_var.get()
            preview_text.config(state="normal")
            preview_text.delete("1.0", tk.END)
            preview_text.insert("1.0", templates[selected])
            preview_text.config(state="disabled")

        template_combo.bind("<<ComboboxSelected>>", update_preview)

        def insert_template():
            selected = template_var.get()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", templates[selected])
            template_window.destroy()
            self.update_size_info()

        button_frame = ttk.Frame(template_window)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Вставить",
            style="Accent.TButton",
            command=insert_template
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            style="TButton",
            command=template_window.destroy
        ).pack(side=tk.LEFT, padx=5)

    def run(self) -> None:
        if "window_size" in self.settings:
            self.root.geometry(self.settings["window_size"])

        if self.data_type.get() == "text":
            self.text_frame.pack(fill=tk.BOTH, expand=True)
            self.file_frame.pack_forget()
        else:
            self.text_frame.pack_forget()
            self.file_frame.pack(fill=tk.X, pady=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self) -> None:
        # Показываем подтверждение если включено
        if self.settings.get("confirm_before_exit", True):
            if not messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из программы?"):
                return

        # Сохраняем настройки
        self.save_settings()

        # Удаляем временные файлы
        if hasattr(self, 'temp_extracted_file') and self.temp_extracted_file and os.path.exists(
                self.temp_extracted_file.name):
            try:
                os.unlink(self.temp_extracted_file.name)
            except:
                pass

        # Останавливаем автосохранение
        if self.autosave_id:
            self.root.after_cancel(self.autosave_id)

        # Закрываем все уведомления
        if hasattr(self, 'notification_manager'):
            self.notification_manager.clear_all()

        # Закрываем окно
        self.root.destroy()

    def bind_shortcuts(self) -> None:
        self.root.bind_all("<F1>", lambda e: self.show_help())
        self.root.bind_all("<Escape>", lambda e: self.cancel_operation())
        self.root.bind_all("<Control-Return>", self.on_ctrl_enter)
        self.root.bind_all("<Control-o>", self.on_ctrl_o)
        self.root.bind_all("<Control-e>", lambda e: self.start_extract())
        self.root.bind_all("<Control-s>", lambda e: self.save_extracted())
        self.root.bind_all("<Control-l>", lambda e: self.clear_text())
        self.root.bind_all("<Control-t>", self.toggle_theme)
        self.root.bind_all("<Control-1>", lambda e: self.set_method("lsb"))
        self.root.bind_all("<Control-2>", lambda e: self.set_method("noise"))
        self.root.bind_all("<Control-3>", lambda e: self.set_method("aelsb"))
        self.root.bind_all("<Control-4>", lambda e: self.set_method("hill"))
        self.root.bind_all("<Control-5>", lambda e: self.set_method("audio_lsb"))
        self.root.bind_all("<Control-r>",
                           lambda e: self.update_thumbnail(self.extract_img_path.get(), self.extract_preview))
        self.root.bind_all("<Control-c>", lambda e: self.copy_extracted())
        self.root.bind_all("<Control-h>", lambda e: self.copy_extracted_hash())
        self.root.bind_all("<Control-,>", lambda e: self.notebook.select(self.settings_tab))
        self.root.bind_all("<Control-q>", lambda e: self.on_close())
        self.root.bind_all("<Control-Tab>", self.next_tab)
        self.root.bind_all("<Control-Shift-Tab>", self.prev_tab)
        self.root.bind_all("<Control-k>", lambda e: self.notebook.select(self.encryption_tab))

    def toggle_theme(self, event=None):
        """Переключает между темной и светлой темой"""
        current_theme = self.theme_manager.current_theme
        if current_theme == "Тёмная":
            self.change_theme("Светлая")
        else:
            self.change_theme("Тёмная")

    def set_method(self, method, event=None):
        """Устанавливает метод скрытия"""
        self.method_var.set(method)
        self.update_size_info()
        self.show_toast(f"Метод изменен на: {STEGANO_METHODS.get(method, method)}")

    def next_tab(self, event=None):
        """Переключается на следующую вкладку"""
        current = self.notebook.index(self.notebook.select())
        next_tab = (current + 1) % self.notebook.index("end")
        self.notebook.select(next_tab)

    def prev_tab(self, event=None):
        """Переключается на предыдущую вкладку"""
        current = self.notebook.index(self.notebook.select())
        prev_tab = (current - 1) % self.notebook.index("end")
        self.notebook.select(prev_tab)

    def on_ctrl_enter(self, event=None):
        try:
            current = self.notebook.index(self.notebook.select())
            if current == 0:
                self.start_hide()
            elif current == 1:
                self.start_extract()
        except:
            pass

    def on_ctrl_o(self, event=None):
        try:
            current = self.notebook.index(self.notebook.select())
            if current == 0:
                self.select_image()
            elif current == 1:
                self.select_extract_image()
        except:
            pass

    def clear_text(self) -> None:
        try:
            self.text_input.delete("1.0", tk.END)
            self.update_size_info()
        except:
            pass

    def paste_text(self) -> None:
        try:
            self.text_input.insert(tk.INSERT, self.root.clipboard_get())
            self.update_size_info()
        except:
            pass

    def install_context_menus(self) -> None:
        # Контекстное меню для текстового ввода
        self.text_menu = tk.Menu(self.root, tearoff=0)
        self.text_menu.add_command(label="📋 Копировать", command=lambda: self.text_input.event_generate("<<Copy>>"))
        self.text_menu.add_command(label="📋 Вставить", command=lambda: self.text_input.event_generate("<<Paste>>"))
        self.text_menu.add_command(label="✂️ Вырезать", command=lambda: self.text_input.event_generate("<<Cut>>"))
        self.text_menu.add_separator()
        self.text_menu.add_command(label="📝 Выделить всё",
                                   command=lambda: self.text_input.event_generate("<<SelectAll>>"))
        self.text_menu.add_command(label="🗑️ Очистить", command=self.clear_text)
        self.text_menu.add_separator()
        self.text_menu.add_command(label="🔍 Найти", command=self.find_text)
        self.text_menu.add_command(label="🔄 Заменить", command=self.replace_text)

        def show_text_menu(event):
            try:
                self.text_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.text_menu.grab_release()

        self.text_input.bind("<Button-3>", show_text_menu)

        # Контекстное меню для результата
        self.result_menu = tk.Menu(self.root, tearoff=0)
        self.result_menu.add_command(label="📋 Копировать", command=self.copy_extracted)
        self.result_menu.add_command(label="💾 Сохранить", command=self.save_extracted)
        self.result_menu.add_separator()
        self.result_menu.add_command(label="🔑 Копировать хеш", command=self.copy_extracted_hash)
        self.result_menu.add_command(label="🗂 Открыть файл", command=self.open_extracted_file)
        self.result_menu.add_separator()
        self.result_menu.add_command(label="🔍 Найти", command=self.find_in_result)
        self.result_menu.add_command(label="📊 Анализировать", command=self.analyze_extracted_data)

        def show_result_menu(event):
            try:
                self.result_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.result_menu.grab_release()

        self.result_text.bind("<Button-3>", show_result_menu)

        # Контекстное меню для истории
        self.history_menu = tk.Menu(self.root, tearoff=0)
        self.history_menu.add_command(label="🔍 Открыть",
                                      command=lambda: self.load_from_history(self.history_menu.index))
        self.history_menu.add_command(label="🖼️ Предпросмотр",
                                      command=lambda: self.preview_from_history(self.history_menu.index))
        self.history_menu.add_command(label="📁 Открыть папку",
                                      command=lambda: self.open_history_folder(self.history_menu.index))
        self.history_menu.add_separator()
        self.history_menu.add_command(label="🗑️ Удалить из истории",
                                      command=lambda: self.remove_history_item(self.history_menu.index))

        # Привязка к меткам истории
        for i, lbl in enumerate(self.history_labels):
            lbl.bind("<Button-3>", lambda e, idx=i: self.show_history_menu(e, idx))

    def find_text(self):
        """Поиск текста в текстовом поле"""
        find_window = tk.Toplevel(self.root)
        find_window.title("Поиск")
        find_window.geometry("300x100")
        find_window.transient(self.root)
        find_window.grab_set()

        ttk.Label(find_window, text="Найти:").pack(pady=(10, 0))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(find_window, textvariable=search_var, width=30)
        search_entry.pack(pady=5)
        search_entry.focus_set()

        def find_next():
            search_term = search_var.get()
            if search_term:
                content = self.text_input.get("1.0", tk.END)
                pos = self.text_input.search(search_term, tk.INSERT, tk.END)
                if pos:
                    end_pos = f"{pos}+{len(search_term)}c"
                    self.text_input.tag_remove("search", "1.0", tk.END)
                    self.text_input.tag_add("search", pos, end_pos)
                    self.text_input.tag_configure("search", background=self.colors["accent"], foreground="white")
                    self.text_input.mark_set(tk.INSERT, end_pos)
                    self.text_input.see(pos)
                else:
                    messagebox.showinfo("Поиск", "Текст не найден")

        ttk.Button(find_window, text="Найти", command=find_next).pack(pady=5)
        find_window.bind("<Return>", lambda e: find_next())

    def replace_text(self):
        """Замена текста в текстовом поле"""
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Замена")
        replace_window.geometry("300x150")
        replace_window.transient(self.root)
        replace_window.grab_set()

        ttk.Label(replace_window, text="Найти:").pack(pady=(5, 0))
        find_var = tk.StringVar()
        find_entry = ttk.Entry(replace_window, textvariable=find_var, width=30)
        find_entry.pack(pady=5)

        ttk.Label(replace_window, text="Заменить на:").pack(pady=(5, 0))
        replace_var = tk.StringVar()
        replace_entry = ttk.Entry(replace_window, textvariable=replace_var, width=30)
        replace_entry.pack(pady=5)

        def replace_next():
            find_term = find_var.get()
            replace_term = replace_var.get()
            if find_term:
                content = self.text_input.get("1.0", tk.END)
                pos = self.text_input.search(find_term, tk.INSERT, tk.END)
                if pos:
                    end_pos = f"{pos}+{len(find_term)}c"
                    self.text_input.delete(pos, end_pos)
                    self.text_input.insert(pos, replace_term)
                    self.text_input.tag_remove("search", "1.0", tk.END)
                    self.text_input.tag_add("search", pos, f"{pos}+{len(replace_term)}c")
                    self.text_input.tag_configure("search", background=self.colors["accent"], foreground="white")
                    self.text_input.mark_set(tk.INSERT, f"{pos}+{len(replace_term)}c")
                    self.text_input.see(pos)
                else:
                    messagebox.showinfo("Замена", "Текст не найден")

        ttk.Button(replace_window, text="Заменить", command=replace_next).pack(pady=5)
        replace_window.bind("<Return>", lambda e: replace_next())

    def find_in_result(self):
        """Поиск в результатах"""
        if not self.current_extracted:
            return

        find_window = tk.Toplevel(self.root)
        find_window.title("Поиск в результатах")
        find_window.geometry("300x100")
        find_window.transient(self.root)
        find_window.grab_set()

        ttk.Label(find_window, text="Найти:").pack(pady=(10, 0))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(find_window, textvariable=search_var, width=30)
        search_entry.pack(pady=5)
        search_entry.focus_set()

        def find_next():
            search_term = search_var.get()
            if search_term:
                content = self.result_text.get("1.0", tk.END)
                pos = self.result_text.search(search_term, tk.INSERT, tk.END)
                if pos:
                    end_pos = f"{pos}+{len(search_term)}c"
                    self.result_text.tag_remove("search", "1.0", tk.END)
                    self.result_text.tag_add("search", pos, end_pos)
                    self.result_text.tag_configure("search", background=self.colors["accent"], foreground="white")
                    self.result_text.mark_set(tk.INSERT, end_pos)
                    self.result_text.see(pos)
                else:
                    messagebox.showinfo("Поиск", "Текст не найден")

        ttk.Button(find_window, text="Найти", command=find_next).pack(pady=5)
        find_window.bind("<Return>", lambda e: find_next())

    def install_tooltips(self) -> None:
        ToolTip(self.drop_label, "Перетащите файл или кликните, чтобы выбрать\
Поддерживаемые форматы: PNG, BMP, TIFF, TGA, JPG, JPEG, WAV")
        if self.extract_drop_label:
            ToolTip(self.extract_drop_label, "Перетащите картинку с данными или кликните для выбора\
Поддерживаемые форматы: PNG, BMP, TIFF, TGA, JPG, JPEG, WAV")
        ToolTip(self.hide_button, "Начать скрытие данных (Ctrl+Enter)\
Проверьте вместимость контейнера перед началом")
        ToolTip(self.extract_button, "Извлечь данные (Ctrl+Enter)\
Программа автоматически определит метод извлечения")
        ToolTip(self.save_button, "Сохранить извлечённые данные (Ctrl+S)\
Поддерживается сохранение в различные форматы")
        ToolTip(self.copy_button, "Скопировать извлечённый текст в буфер обмена")
        ToolTip(self.open_file_button, "Открыть извлечённый файл в приложении по умолчанию")
        ToolTip(self.copy_hash_button, "Скопировать SHA-256 хеш извлечённых данных\
Можно использовать для проверки целостности")
        ToolTip(self.usage_bar, "Индикатор заполнения контейнера\
Зеленый: ≤70% (оптимально)\
Желтый: 70-100% (максимально)\
Красный: >100% (невозможно)")


if __name__ == "__main__":
    app = SteganographyUltimatePro()
    if hasattr(app, 'root') and app.root.winfo_exists():
        app.run()
