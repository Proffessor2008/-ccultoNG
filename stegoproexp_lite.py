import base64
import hashlib
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tkinter as tk
import wave
import zlib
from tkinter import ttk, filedialog, messagebox, scrolledtext
from typing import List
from typing import Tuple

import cv2
import numba
import numpy as np
from PIL import Image
from PIL import ImageTk
from scipy import ndimage
from scipy.fftpack import dct, idct
from tkinterdnd2 import DND_FILES, TkinterDnD

# ───────────────────────────────────────────────
# 🎨 ГЛОБАЛЬНЫЕ НАСТРОЙКИ (УЛУЧШЕННЫЕ)
# ───────────────────────────────────────────────
VERSION = "2.1.0"
AUTHOR = "MustaNG"
BUILD_DATE = time.strftime("%Y-%m-%d")

# Константы для LSB-метода
HEADER_SIZE_BITS = 32  # Размер заголовка (биты)
PROGRESS_UPDATE_INTERVAL = 1000  # Частота обновления прогресса (биты)
MIN_DATA_LEN = 8  # Минимальный размер данных (биты)
MAX_DATA_LEN = 100 * 1024 * 1024 * 8  # Максимальный размер данных (100 МБ в битах)

# Улучшенные современные темы с плавными градиентами и закруглениями
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
MAX_FILE_SIZE_MB = 100  # Максимальный размер файла для скрытия (МБ)

CONFIG = {
    "MAX_FILE_SIZE_MB": MAX_FILE_SIZE_MB,
    "SETTINGS_FILE": SETTINGS_FILE,
    "HISTORY_FILE": HISTORY_FILE,
    "AUTO_SAVE_INTERVAL": 300,  # Автосохранение каждые 5 минут
    "ANIMATION_SPEED": 0.1,
    "TOAST_DURATION": 3000,
    "MAX_UNDO_HISTORY": 5
}


# ───────────────────────────────────────────────
# 🛠️ УТИЛИТЫ (УЛУЧШЕННЫЕ)
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
# 🛈 КЛАСС ПОДСКАЗОК (TOOLTIP) - УЛУЧШЕННЫЙ
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
# 🎨 КЛАСС ДЛЯ РАБОТЫ С ТЕМАМИ (УЛУЧШЕННЫЙ)
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

        # Дроп-зона — теперь отдельным стилем метки
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
# 🎯 КЛАСС ЦЕЛЕЙ И ДОСТИЖЕНИЙ
# ───────────────────────────────────────────────
class AchievementManager:
    def __init__(self):
        self.achievements_file = "achievements.json"
        self.achievements = self.load_achievements()
        self.initialize_achievements()

    def load_achievements(self):
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass

        return {}

    def save_achievements(self):
        try:
            with open(self.achievements_file, 'w', encoding='utf-8') as f:
                json.dump(self.achievements, f, indent=2, ensure_ascii=False)
        except:
            pass

    def initialize_achievements(self):
        """Инициализирует список достижений"""
        default_achievements = {
            "first_hide": {
                "name": "Первый шаг",
                "description": "Спрячьте свои первые данные",
                "icon": "🎯",
                "unlocked": False,
                "progress": 0,
                "target": 1
            },
            "first_extract": {
                "name": "Детектив",
                "description": "Извлеките данные в первый раз",
                "icon": "🔍",
                "unlocked": False,
                "progress": 0,
                "target": 1
            },
            "five_operations": {
                "name": "Начинающий стеганограф",
                "description": "Выполните 5 операций скрытия или извлечения",
                "icon": "⭐",
                "unlocked": False,
                "progress": 0,
                "target": 5
            },
            "ten_operations": {
                "name": "Опытный специалист",
                "description": "Выполните 10 операций",
                "icon": "🌟",
                "unlocked": False,
                "progress": 0,
                "target": 10
            },
            "twenty_operations": {
                "name": "Мастер стеганографии",
                "description": "Выполните 20 операций",
                "icon": "🏆",
                "unlocked": False,
                "progress": 0,
                "target": 20
            },
            "large_file": {
                "name": "Работа с большими файлами",
                "description": "Спрячьте файл размером более 10 МБ",
                "icon": "📦",
                "unlocked": False,
                "progress": 0,
                "target": 1
            },
            "multiple_methods": {
                "name": "Экспериментатор",
                "description": "Используйте все 4 метода скрытия данных",
                "icon": "🧪",
                "unlocked": False,
                "progress": 0,
                "target": 4
            },
            "audio_expert": {
                "name": "Аудио-стеганограф",
                "description": "Спрячьте данные в аудиофайле",
                "icon": "🎵",
                "unlocked": False,
                "progress": 0,
                "target": 1
            }
        }

        # Добавляем новые достижения, сохраняя прогресс старых
        for key, achievement in default_achievements.items():
            if key not in self.achievements:
                self.achievements[key] = achievement
            else:
                # Обновляем описание и иконку, сохраняя прогресс
                self.achievements[key]["name"] = achievement["name"]
                self.achievements[key]["description"] = achievement["description"]
                self.achievements[key]["icon"] = achievement["icon"]
                self.achievements[key]["target"] = achievement["target"]

        self.save_achievements()

    def increment_progress(self, achievement_key, amount=1):
        """Увеличивает прогресс достижения"""
        if achievement_key in self.achievements:
            achievement = self.achievements[achievement_key]
            if not achievement["unlocked"]:
                achievement["progress"] = min(achievement["progress"] + amount, achievement["target"])
                if achievement["progress"] >= achievement["target"]:
                    achievement["unlocked"] = True
                    return True  # Достижение разблокировано
            self.save_achievements()
        return False

    def get_unlocked_achievements(self):
        """Возвращает список разблокированных достижений"""
        return {k: v for k, v in self.achievements.items() if v["unlocked"]}

    def get_locked_achievements(self):
        """Возвращает список заблокированных достижений"""
        return {k: v for k, v in self.achievements.items() if not v["unlocked"]}

    def get_achievement_progress(self, achievement_key):
        """Возвращает прогресс достижения"""
        if achievement_key in self.achievements:
            achievement = self.achievements[achievement_key]
            return achievement["progress"], achievement["target"]
        return 0, 0


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
            JPEGStego.hide_dct(container_path, data, password, output_path)
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
# 🎯 КЛАСС ИНТЕРФЕЙСА ПАКЕТНОЙ ОБРАБОТКИ
# ───────────────────────────────────────────────
class BatchProcessingUI:
    """Интерфейс для пакетной обработки с прокруткой"""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.batch_processor = BatchProcessor(app)

        # Переменные
        self.selected_files = []
        self.selected_extract_files = []
        self.selected_analyze_files = []

        self.output_dir = tk.StringVar(value=os.path.expanduser("~"))
        self.operation_type = tk.StringVar(value="hide")
        self.method_var = tk.StringVar(value="lsb")
        self.overwrite_var = tk.BooleanVar(value=False)
        self.auto_save_var = tk.BooleanVar(value=True)
        self.hide_data_type = tk.StringVar(value="text")
        self.hide_file_path = tk.StringVar()
        self.hide_password = tk.StringVar()
        self.extract_password = tk.StringVar()
        self.extract_method = tk.StringVar()
        self.extract_output_dir = tk.StringVar(value=os.path.expanduser("~"))

        self.setup_ui()

    # В классе BatchProcessingUI добавьте метод очистки состояния:
    def reset_processing_state(self):
        """Сбрасывает состояние обработки"""
        self.batch_processor.clear_batch()
        self.batch_status_label.config(text="✅ Готов к обработке")
        self.batch_progress_var.set(0)
        self.disable_buttons(False)

        # Сброс статистики
        self.stats_processed.config(text="Обработано: 0")
        self.stats_success.config(text="Успешно: 0")
        self.stats_failed.config(text="Ошибки: 0")

    def setup_ui(self):
        """Создает интерфейс пакетной обработки с прокруткой"""
        # Основной контейнер с прокруткой
        main_container = ttk.Frame(self.parent)
        main_container.pack(fill=tk.BOTH, expand=True)

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
        self.canvas.pack(side="left", fill="both", expand=True, padx=1)
        scrollbar.pack(side="right", fill="y")

        # Связываем колесо мыши
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Создаем контент
        self.create_content()

    def _on_mousewheel(self, event):
        """Обработка колеса мыши для прокрутки"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_content(self):
        """Создает содержимое интерфейса"""
        # Заголовок
        ttk.Label(
            self.scrollable_frame,
            text="📦 Пакетная обработка файлов",
            font=("Segoe UI", 18, "bold"),
            style="Title.TLabel"
        ).pack(pady=(20, 10))

        ttk.Label(
            self.scrollable_frame,
            text="Одновременная обработка до 5 файлов",
            font=("Segoe UI", 11),
            style="Subtitle.TLabel"
        ).pack(pady=(0, 20))

        # Создаем Notebook для разных операций
        self.batch_notebook = ttk.Notebook(self.scrollable_frame)
        self.batch_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Вкладка скрытия
        self.hide_tab = self.create_hide_tab()
        self.batch_notebook.add(self.hide_tab, text="📤 Скрытие")

        # Вкладка извлечения
        self.extract_tab = self.create_extract_tab()
        self.batch_notebook.add(self.extract_tab, text="📥 Извлечение")

        # Вкладка анализа
        self.analyze_tab = self.create_analyze_tab()
        self.batch_notebook.add(self.analyze_tab, text="🔍 Анализ")

        # Статусная панель
        self.create_status_panel()

        # Кнопки управления внизу
        self.create_bottom_buttons()

    def create_hide_tab(self):
        """Создает вкладку для пакетного скрытия"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем сетку для компактности
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        row = 0

        # Выбор файлов
        files_frame = ttk.LabelFrame(tab, text="📁 Выбор контейнеров (до 5)", padding=10)
        files_frame.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        files_frame.grid_columnconfigure(0, weight=1)

        # Список файлов с прокруткой
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.files_listbox = tk.Listbox(
            list_frame,
            height=4,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            selectbackground=self.app.colors["accent"],
            selectforeground="white",
            font=("Segoe UI", 9)
        )
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки управления файлами
        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(
            btn_frame,
            text="➕ Добавить файлы",
            command=self.add_files,
            style="IconButton.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="🗑️ Очистить",
            command=self.clear_files,
            style="IconButton.TButton",
            width=10
        ).pack(side=tk.LEFT)

        row += 1

        # Данные для скрытия - левая колонка
        data_frame = ttk.LabelFrame(tab, text="📋 Данные для скрытия", padding=10)
        data_frame.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)

        # Тип данных
        ttk.Label(data_frame, text="Тип данных:", style="TLabel").pack(anchor="w", pady=(0, 5))

        type_frame = ttk.Frame(data_frame)
        type_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Radiobutton(
            type_frame,
            text="Текст",
            variable=self.hide_data_type,
            value="text",
            command=self.update_hide_data_input
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Radiobutton(
            type_frame,
            text="Файл",
            variable=self.hide_data_type,
            value="file",
            command=self.update_hide_data_input
        ).pack(side=tk.LEFT)

        # Текстовое поле
        self.hide_text_frame = ttk.Frame(data_frame)
        self.hide_text_frame.pack(fill=tk.BOTH, expand=True)

        self.hide_text = scrolledtext.ScrolledText(
            self.hide_text_frame,
            height=6,
            wrap=tk.WORD,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            font=("Segoe UI", 9)
        )
        self.hide_text.pack(fill=tk.BOTH, expand=True)

        # Выбор файла (скрыто по умолчанию)
        self.hide_file_frame = ttk.Frame(data_frame)

        file_select_frame = ttk.Frame(self.hide_file_frame)
        file_select_frame.pack(fill=tk.X, pady=(0, 5))

        self.hide_file_path = tk.StringVar()
        ttk.Entry(
            file_select_frame,
            textvariable=self.hide_file_path,
            state='readonly',
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            file_select_frame,
            text="📂",
            command=self.select_hide_file,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT)

        # Настройки - правая колонка
        settings_frame = ttk.LabelFrame(tab, text="⚙️ Настройки", padding=10)
        settings_frame.grid(row=row, column=1, sticky="nsew", padx=5, pady=5)

        # Метод
        ttk.Label(settings_frame, text="Метод скрытия:", style="TLabel").pack(anchor="w", pady=(0, 5))

        self.hide_method_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.method_var,
            values=list(STEGANO_METHODS.keys()),
            state="readonly",
            width=20
        )
        self.hide_method_combo.pack(fill=tk.X, pady=(0, 10))

        # Пароль
        ttk.Label(settings_frame, text="Пароль (опционально):", style="TLabel").pack(anchor="w", pady=(0, 5))

        ttk.Entry(
            settings_frame,
            textvariable=self.hide_password,
            show="●",
            style="TEntry"
        ).pack(fill=tk.X, pady=(0, 10))

        # Выходная директория
        ttk.Label(settings_frame, text="Папка для сохранения:", style="TLabel").pack(anchor="w", pady=(0, 5))

        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill=tk.X)

        ttk.Entry(
            output_frame,
            textvariable=self.output_dir,
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            output_frame,
            text="📂",
            command=self.select_output_dir,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT)

        # Опции
        options_frame = ttk.Frame(settings_frame)
        options_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Checkbutton(
            options_frame,
            text="Перезаписывать существующие файлы",
            variable=self.overwrite_var,
            style="TCheckbutton"
        ).pack(anchor="w")

        row += 1

        # Кнопка запуска (во всю ширину)
        self.hide_button = ttk.Button(
            tab,
            text="🚀 Начать пакетное скрытие",
            style="Accent.TButton",
            command=self.start_batch_hide
        )
        self.hide_button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        # Инициализация
        self.hide_text_frame.pack()
        self.hide_file_frame.pack_forget()

        return tab

    def create_extract_tab(self):
        """Создает вкладку для пакетного извлечения"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем сетку
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        row = 0

        # Выбор файлов
        files_frame = ttk.LabelFrame(tab, text="📁 Выбор стего-файлов (до 5)", padding=10)
        files_frame.grid(row=row, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        files_frame.grid_columnconfigure(0, weight=1)

        # Список файлов с прокруткой
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.extract_files_listbox = tk.Listbox(
            list_frame,
            height=4,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            selectbackground=self.app.colors["accent"],
            selectforeground="white",
            font=("Segoe UI", 9)
        )
        self.extract_files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.extract_files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.extract_files_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки
        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(
            btn_frame,
            text="➕ Добавить файлы",
            command=self.add_extract_files,
            style="IconButton.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="🗑️ Очистить",
            command=lambda: self.extract_files_listbox.delete(0, tk.END) or self.selected_extract_files.clear(),
            style="IconButton.TButton",
            width=10
        ).pack(side=tk.LEFT)

        row += 1

        # Настройки извлечения - левая колонка
        settings_frame = ttk.LabelFrame(tab, text="⚙️ Настройки извлечения", padding=10)
        settings_frame.grid(row=row, column=0, sticky="nsew", padx=5, pady=5)

        # Пароль
        ttk.Label(settings_frame, text="Пароль (если требуется):", style="TLabel").pack(anchor="w", pady=(0, 5))

        ttk.Entry(
            settings_frame,
            textvariable=self.extract_password,
            show="●",
            style="TEntry"
        ).pack(fill=tk.X, pady=(0, 10))

        # Метод
        ttk.Label(settings_frame, text="Метод (авто если пусто):", style="TLabel").pack(anchor="w", pady=(0, 5))

        ttk.Combobox(
            settings_frame,
            textvariable=self.extract_method,
            values=["", "lsb", "noise", "aelsb", "hill", "audio_lsb", "jpeg_dct"],
            state="readonly",
            width=20
        ).pack(fill=tk.X, pady=(0, 10))

        # Дополнительные настройки - правая колонка
        output_frame = ttk.LabelFrame(tab, text="📁 Сохранение", padding=10)
        output_frame.grid(row=row, column=1, sticky="nsew", padx=5, pady=5)

        ttk.Label(output_frame, text="Папка для сохранения:", style="TLabel").pack(anchor="w", pady=(0, 5))

        dir_frame = ttk.Frame(output_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Entry(
            dir_frame,
            textvariable=self.extract_output_dir,
            style="TEntry"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(
            dir_frame,
            text="📂",
            command=self.select_extract_output_dir,
            style="IconButton.TButton"
        ).pack(side=tk.LEFT)

        # Опции
        ttk.Checkbutton(
            output_frame,
            text="Автоматически сохранять извлеченные данные",
            variable=self.auto_save_var,
            style="TCheckbutton"
        ).pack(anchor="w", pady=(5, 0))

        row += 1

        # Кнопка запуска
        self.extract_button = ttk.Button(
            tab,
            text="🚀 Начать пакетное извлечение",
            style="Accent.TButton",
            command=self.start_batch_extract
        )
        self.extract_button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        return tab

    def create_analyze_tab(self):
        """Создает вкладку для пакетного анализа"""
        tab = ttk.Frame(self.batch_notebook, style="Card.TFrame")

        # Используем сетку
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=0)
        tab.grid_rowconfigure(1, weight=1)

        # Выбор файлов
        files_frame = ttk.LabelFrame(tab, text="📁 Выбор файлов для анализа (до 5)", padding=10)
        files_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        files_frame.grid_columnconfigure(0, weight=1)

        # Список файлов с прокруткой
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.analyze_files_listbox = tk.Listbox(
            list_frame,
            height=3,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            selectbackground=self.app.colors["accent"],
            selectforeground="white",
            font=("Segoe UI", 9)
        )
        self.analyze_files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.analyze_files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.analyze_files_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки
        btn_frame = ttk.Frame(files_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(
            btn_frame,
            text="➕ Добавить файлы",
            command=self.add_analyze_files,
            style="IconButton.TButton",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="🗑️ Очистить",
            command=lambda: self.analyze_files_listbox.delete(0, tk.END) or self.selected_analyze_files.clear(),
            style="IconButton.TButton",
            width=10
        ).pack(side=tk.LEFT)

        # Кнопка запуска анализа
        self.analyze_button = ttk.Button(
            files_frame,
            text="🔍 Начать анализ",
            style="Accent.TButton",
            command=self.start_batch_analyze
        )
        self.analyze_button.pack(fill=tk.X, pady=(10, 0))

        # Поле для результатов
        results_frame = ttk.LabelFrame(tab, text="📊 Результаты анализа", padding=10)
        results_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        self.analyze_results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            bg=self.app.colors["card"],
            fg=self.app.colors["text"],
            font=("Consolas", 9),
            state='disabled'
        )
        self.analyze_results_text.grid(row=0, column=0, sticky="nsew")

        return tab

    def create_status_panel(self):
        """Создает панель статуса"""
        status_frame = ttk.LabelFrame(self.scrollable_frame, text="📊 Статус обработки", padding=10)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Прогресс
        self.batch_progress_var = tk.DoubleVar()
        self.batch_progress = ttk.Progressbar(
            status_frame,
            variable=self.batch_progress_var,
            maximum=100,
            style="TProgressbar",
            length=400
        )
        self.batch_progress.pack(fill=tk.X, pady=(0, 10))

        # Статус
        self.batch_status_label = ttk.Label(
            status_frame,
            text="✅ Готов к обработке",
            font=("Segoe UI", 10),
            style="TLabel"
        )
        self.batch_status_label.pack(anchor="w", pady=(0, 10))

        # Статистика в ряд
        stats_frame = ttk.Frame(status_frame)
        stats_frame.pack(fill=tk.X)

        self.stats_total = ttk.Label(stats_frame, text="Всего: 0", style="TLabel")
        self.stats_total.pack(side=tk.LEFT, padx=(0, 20))

        self.stats_processed = ttk.Label(stats_frame, text="Обработано: 0", style="TLabel")
        self.stats_processed.pack(side=tk.LEFT, padx=(0, 20))

        self.stats_success = ttk.Label(stats_frame, text="Успешно: 0", style="Success.TLabel")
        self.stats_success.pack(side=tk.LEFT, padx=(0, 20))

        self.stats_failed = ttk.Label(stats_frame, text="Ошибки: 0", style="Error.TLabel")
        self.stats_failed.pack(side=tk.LEFT)

    def create_bottom_buttons(self):
        """Создает кнопки управления внизу"""
        btn_frame = ttk.Frame(self.scrollable_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=(0, 20))

        # Кнопки управления
        ttk.Button(
            btn_frame,
            text="⏹️ Остановить обработку",
            style="TButton",
            command=self.stop_processing
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            btn_frame,
            text="📊 Экспорт результатов",
            style="TButton",
            command=self.export_batch_results
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            btn_frame,
            text="🗑️ Очистить все",
            style="TButton",
            command=self.clear_all
        ).pack(side=tk.LEFT)

    # Методы для работы с файлами
    def add_files(self):
        """Добавляет файлы в список"""
        files = filedialog.askopenfilenames(
            title="Выберите файлы-контейнеры",
            filetypes=SUPPORTED_FORMATS,
            initialdir=self.app.last_open_dir
        )

        if not files:
            return

        for file in files:
            if file not in self.selected_files and len(self.selected_files) < 5:
                self.selected_files.append(file)
                display_name = os.path.basename(file)
                if len(display_name) > 30:
                    display_name = "..." + display_name[-27:]
                self.files_listbox.insert(tk.END, display_name)
            elif len(self.selected_files) >= 5:
                messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                break

        self.update_stats()

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
            if file not in self.selected_extract_files and len(self.selected_extract_files) < 5:
                self.selected_extract_files.append(file)
                display_name = os.path.basename(file)
                if len(display_name) > 30:
                    display_name = "..." + display_name[-27:]
                self.extract_files_listbox.insert(tk.END, display_name)
            elif len(self.selected_extract_files) >= 5:
                messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                break

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
            if file not in self.selected_analyze_files and len(self.selected_analyze_files) < 5:
                self.selected_analyze_files.append(file)
                display_name = os.path.basename(file)
                if len(display_name) > 30:
                    display_name = "..." + display_name[-27:]
                self.analyze_files_listbox.insert(tk.END, display_name)
            elif len(self.selected_analyze_files) >= 5:
                messagebox.showwarning("Ограничение", "Максимальное количество файлов - 5")
                break

    def clear_files(self):
        """Очищает список файлов"""
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)
        self.update_stats()

    def select_hide_file(self):
        """Выбирает файл для скрытия"""
        file = filedialog.askopenfilename(
            title="Выберите файл для скрытия",
            initialdir=self.app.last_open_dir
        )

        if file:
            self.hide_file_path.set(file)

    def select_output_dir(self):
        """Выбирает выходную директорию"""
        directory = filedialog.askdirectory(
            title="Выберите папку для сохранения",
            initialdir=self.output_dir.get()
        )

        if directory:
            self.output_dir.set(directory)

    def select_extract_output_dir(self):
        """Выбирает выходную директорию для извлечения"""
        directory = filedialog.askdirectory(
            title="Выберите папку для сохранения извлеченных данных",
            initialdir=self.extract_output_dir.get()
        )

        if directory:
            self.extract_output_dir.set(directory)

    def update_hide_data_input(self):
        """Обновляет поле ввода данных в зависимости от типа"""
        if self.hide_data_type.get() == "text":
            self.hide_file_frame.pack_forget()
            self.hide_text_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.hide_text_frame.pack_forget()
            self.hide_file_frame.pack(fill=tk.X, pady=(10, 0))

    def update_stats(self):
        """Обновляет статистику"""
        total = len(self.selected_files)
        self.stats_total.config(text=f"Всего: {total}")

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

        # Проверка вместимости
        try:
            # Проверяем первый файл для оценки
            if files_to_process:
                w, h, available_bits = ImageProcessor.get_image_info(files_to_process[0])
                required_bits = len(data) * 8
                if required_bits > available_bits:
                    if not messagebox.askyesno("Предупреждение",
                                               "Данные могут не поместиться в некоторые контейнеры. Продолжить?"):
                        return
        except:
            pass

        # Подготовка параметров
        params = {
            'data': data,
            'method': self.method_var.get(),
            'password': self.hide_password.get(),
            'output_dir': self.output_dir.get(),
            'overwrite': self.overwrite_var.get(),
            'compression_level': self.app.compression_level.get()
        }

        # Добавление в очередь
        self.batch_processor.clear_batch()
        self.batch_processor.add_to_batch(files_to_process, 'hide', params)

        # Запуск обработки
        self.start_processing("Скрытие данных...")

    def start_batch_extract(self):
        """Запускает пакетное извлечение - ИСПРАВЛЕНО!"""
        if not self.selected_extract_files:
            messagebox.showwarning("Ошибка", "Не выбраны файлы для извлечения")
            return

        # Ограничение до 5 файлов
        files_to_process = self.selected_extract_files[:5]

        # Подготовка параметров
        method = self.extract_method.get() if self.extract_method.get() else None

        params = {
            'password': self.extract_password.get(),
            'method': method,
            'output_dir': self.extract_output_dir.get(),
            'auto_save': self.auto_save_var.get()
        }

        # Проверка существования файлов
        for file in files_to_process:
            if not os.path.exists(file):
                messagebox.showerror("Ошибка", f"Файл не найден: {file}")
                return

        # Добавление в очередь
        self.batch_processor.clear_batch()
        self.batch_processor.add_to_batch(files_to_process, 'extract', params)

        # Запуск обработки
        self.start_processing("Извлечение данных...")

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

        # Запуск обработки
        self.start_processing("Анализ файлов...")

    def start_processing(self, initial_message="Обработка..."):
        """Запускает обработку с правильным статусом"""
        self.batch_status_label.config(text=initial_message)
        self.batch_progress_var.set(0)

        def progress_callback(progress, status):
            self.batch_progress_var.set(progress)
            self.batch_status_label.config(text=status)

            # Обновление статистики
            info = self.batch_processor.get_batch_info()
            self.stats_processed.config(text=f"Обработано: {info['completed']}")
            self.stats_success.config(text=f"Успешно: {info['success_count']}")
            self.stats_failed.config(text=f"Ошибки: {info['fail_count']}")

            # Обновляем интерфейс
            self.parent.update_idletasks()

        def completion_callback(results):
            # ВАЖНО: Разблокируем кнопки после завершения
            self.disable_buttons(False)

            self.batch_status_label.config(text="✅ Обработка завершена")
            self.batch_progress_var.set(100)

            # Подсчет результатов
            success = len([r for r in results if r['success']])
            failed = len([r for r in results if not r['success']])

            # Показываем результаты
            current_tab = self.batch_notebook.index(self.batch_notebook.select())
            if current_tab == 0:  # Вкладка скрытия
                message = f"Пакетное скрытие завершено.\n\nУспешно: {success}\nС ошибками: {failed}"
            elif current_tab == 1:  # Вкладка извлечения
                message = f"Пакетное извлечение завершено.\n\nУспешно: {success}\nС ошибками: {failed}"
            else:  # Вкладка анализа
                message = f"Пакетный анализ завершён.\n\nУспешно: {success}\nС ошибками: {failed}"
                self.show_analysis_results(results)

            # Показываем сообщение только если есть результаты
            if len(results) > 0:
                # Используем after для отложенного показа сообщения
                self.app.root.after(100, lambda: messagebox.showinfo("Завершено", message))

            # Записываем в лог
            operation_type = ["hide", "extract", "analyze"][current_tab]
            self.app.log_manager.add_entry(f"batch_{operation_type}",
                                           "success" if success > 0 else "error",
                                           {"total": len(results), "success": success, "failed": failed})

        # Отключаем кнопки на время обработки
        self.disable_buttons(True)

        # Запуск асинхронной обработки
        self.batch_processor.process_batch(progress_callback, completion_callback)

    def disable_buttons(self, disable=True):
        """Включает/отключает кнопки"""
        state = "disabled" if disable else "normal"

        # Отключаем/включаем кнопки на всех вкладках
        if hasattr(self, 'hide_button'):
            self.hide_button.config(state=state)
        if hasattr(self, 'extract_button'):
            self.extract_button.config(state=state)
        if hasattr(self, 'analyze_button'):
            self.analyze_button.config(state=state)

        # Также отключаем кнопки управления файлами
        if hasattr(self, 'files_listbox'):
            # Находим все кнопки в интерфейсе
            for widget in self.scrollable_frame.winfo_children():
                self._recursive_disable(widget, state)

        # Обновляем интерфейс
        self.parent.update_idletasks()

    def _recursive_disable(self, widget, state):
        """Рекурсивно отключает/включает виджеты"""
        try:
            if isinstance(widget, (ttk.Button, tk.Button)):
                if widget not in [self.hide_button, self.extract_button, self.analyze_button]:
                    widget.config(state=state)
        except:
            pass

        # Рекурсивно обрабатываем дочерние виджеты
        try:
            for child in widget.winfo_children():
                self._recursive_disable(child, state)
        except:
            pass

    def stop_processing(self):
        """Останавливает обработку"""
        if self.batch_processor.processing:
            self.batch_processor.cancel_processing()
            self.batch_status_label.config(text="⏹️ Обработка остановлена")
            self.disable_buttons(False)  # Разблокируем кнопки
            self.app.root.after(100, lambda: messagebox.showinfo("Остановлено",
                                                                 "Пакетная обработка была остановлена"))

    def export_batch_results(self):
        """Экспортирует результаты обработки"""
        if not self.batch_processor.results:
            messagebox.showwarning("Ошибка", "Нет результатов для экспорта")
            return

        file_path = filedialog.asksaveasfilename(
            title="Сохранить результаты",
            defaultextension=".json",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")],
            initialdir=self.app.last_save_dir
        )

        if file_path:
            if self.batch_processor.export_results(file_path):
                messagebox.showinfo("Успех", "Результаты успешно экспортированы")
                self.app.last_save_dir = os.path.dirname(file_path)
            else:
                messagebox.showerror("Ошибка", "Не удалось экспортировать результаты")

    def show_analysis_results(self, results):
        """Показывает результаты анализа"""
        self.analyze_results_text.config(state='normal')
        self.analyze_results_text.delete("1.0", tk.END)

        for result in results:
            if result['success']:
                info = result.get('data', {})
                file_info = info.get('file_info', {})
                text = f"📄 {os.path.basename(result.get('file', 'Unknown'))}:\n"
                text += f"   📏 Размер: {file_info.get('size_formatted', 'N/A')}\n"
                text += f"   📅 Создан: {file_info.get('created', 'N/A')}\n"
                text += f"   📝 Тип: {file_info.get('type', 'unknown')}\n"

                if info.get('has_stego'):
                    text += "   ✅ Содержит скрытые данные\n"
                    stego_info = info.get('stego_info', {})
                    text += f"      Размер данных: {stego_info.get('size', 0)} байт\n"
                    text += f"      Тип данных: {stego_info.get('data_type', 'unknown')}\n"
                else:
                    text += "   ❌ Скрытых данных не обнаружено\n"

                # Вместимость
                capacity = info.get('capacity_info', {})
                if capacity:
                    text += "   📊 Вместимость (в байтах):\n"
                    for method, cap in capacity.items():
                        method_name = STEGANO_METHODS.get(method, method)
                        cap_bytes = cap // 8
                        text += f"      • {method_name}: {cap_bytes:,}\n"

                text += "-" * 60 + "\n\n"
                self.analyze_results_text.insert(tk.END, text)
            else:
                text = f"❌ {os.path.basename(result.get('file', 'Unknown'))}:\n"
                text += f"   Ошибка: {result.get('error', 'Неизвестная ошибка')}\n"
                text += "-" * 60 + "\n\n"
                self.analyze_results_text.insert(tk.END, text)

        self.analyze_results_text.config(state='disabled')

    def clear_all(self):
        """Очищает все списки и результаты"""
        # Очистка списков
        self.selected_files = []
        self.selected_extract_files = []
        self.selected_analyze_files = []

        # Очистка виджетов
        self.files_listbox.delete(0, tk.END)
        self.extract_files_listbox.delete(0, tk.END)
        self.analyze_files_listbox.delete(0, tk.END)

        # Очистка полей ввода
        if hasattr(self, 'hide_text'):
            self.hide_text.delete("1.0", tk.END)
        self.hide_file_path.set("")
        self.hide_password.set("")
        self.extract_password.set("")
        self.extract_method.set("")

        # Очистка результатов анализа
        self.analyze_results_text.config(state='normal')
        self.analyze_results_text.delete("1.0", tk.END)
        self.analyze_results_text.config(state='disabled')

        # Сброс состояния обработки
        self.reset_processing_state()

        messagebox.showinfo("Очистка", "Все списки и результаты очищены")


# ───────────────────────────────────────────────
# 🧠 ИНТЕЛЛЕКТУАЛЬНЫЕ ПОДСКАЗКИ И АССИСТЕНТ
# ───────────────────────────────────────────────

class SmartAssistant:
    """Интеллектуальный помощник пользователя с расширенными правилами"""

    def __init__(self, app):
        self.app = app
        self.tips = [
            "💡 Совет: Используйте lossless-форматы (PNG/BMP/TIFF) для максимального качества скрытия данных",
            "💡 Совет: Для аудио используйте несжатый WAV; любое перекодирование может разрушить скрытые биты",
            "💡 Совет: Метод HILL-CA обеспечивает максимальную скрытность, но имеет меньшую вместимость",
            "💡 Совет: Метод Adaptive-Noise лучше маскирует изменения в изображении",
            "💡 Совет: Используйте сочетания клавиш для ускорения работы (F1 - помощь, Ctrl+O - открыть)",
            "💡 Совет: Всегда проверяйте вместимость контейнера перед скрытием данных",
            "💡 Совет: Для больших файлов используйте классический LSB для максимальной вместимости",
            "💡 Совет: Регулярно создавайте резервные копии важных файлов",
            "💡 Совет: Используйте историю для быстрого доступа к недавно использованным файлам",
            "💡 Совет: Откройте настройки, чтобы настроить тему интерфейса под ваши предпочтения",
            "💡 Совет: Для текстовых сообщений сжимайте данные в ZIP для экономии места",
            "💡 Совет: Проверяйте контрольные суммы извлеченных файлов для проверки целостности",
            "💡 Совет: Используйте разные методы для разных типов контейнеров (LSB для изображений, DCT для JPEG)",
            "💡 Совет: Создавайте регулярные копии настроек приложения",
            "💡 Совет: Используйте пакетную обработку для работы с несколькими файлами одновременно",
            "💡 Совет: Для конфиденциальных данных используйте комбинацию пароля и шифрования",
            "💡 Совет: Проверяйте статистику использования для оптимизации рабочих процессов",
            "💡 Совет: Используйте плагины для расширения функциональности приложения"
        ]
        self.context_rules = {
            "large_file": [
                "💡 Контекстный совет: Для больших файлов рекомендуется использовать классический LSB метод",
                "💡 Контекстный совет: Рассмотрите возможность сжатия файла перед скрытием",
                "💡 Контекстный совет: Проверьте свободное место на диске перед обработкой больших файлов"
            ],
            "small_container": [
                "💡 Контекстный совет: Контейнер слишком мал для выбранных данных",
                "💡 Контекстный совет: Попробуйте использовать изображение большего размера",
                "💡 Контекстный совет: Сожмите данные или используйте более эффективный метод"
            ],
            "audio_container": [
                "💡 Контекстный совет: Для аудио контейнеров используйте метод WAV LSB",
                "💡 Контекстный совет: Убедитесь, что аудиофайл не будет подвергаться сжатию",
                "💡 Контекстный совет: Аудиофайлы имеют меньшую вместимость чем изображения"
            ],
            "jpeg_container": [
                "💡 Контекстный совет: Для JPEG используйте DCT метод для лучшей устойчивости",
                "💡 Контекстный совет: JPEG сжатие может повредить скрытые данные",
                "💡 Контекстный совет: Вместимость JPEG меньше чем у lossless форматов"
            ],
            "first_time": [
                "💡 Добро пожаловать! Начните с выбора контейнера и данных для скрытия",
                "💡 Совет для новичка: Используйте вкладку 'Помощь' для получения подробной информации",
                "💡 Совет: Начните с небольшого текста для тестирования функциональности"
            ],
            "low_contrast": [
                "💡 Контекстный совет: Изображение имеет низкий контраст, что может повлиять на качество",
                "💡 Контекстный совет: Рассмотрите использование метода Adaptive-Noise для таких изображений",
                "💡 Контекстный совет: Низкий контраст может сделать изменения более заметными"
            ],
            "high_capacity_usage": [
                "💡 Контекстный совет: Высокое заполнение контейнера может ухудшить качество",
                "💡 Контекстный совет: Рекомендуется использовать не более 80% вместимости",
                "💡 Контекстный совет: Рассмотрите использование контейнера большего размера"
            ],
            "multiple_files": [
                "💡 Контекстный совет: Используйте пакетную обработку для нескольких файлов",
                "💡 Контекстный совет: Убедитесь, что все файлы имеют одинаковый формат",
                "💡 Контекстный совет: Создайте резервные копии перед пакетной обработкой"
            ],
            "password_weak": [
                "💡 Контекстный совет: Используйте более сложный пароль для безопасности",
                "💡 Контекстный совет: Рекомендуемая длина пароля - не менее 8 символов",
                "💡 Контекстный совет: Используйте комбинацию букв, цифр и специальных символов"
            ],
            "network_share": [
                "💡 Контекстный совет: Будьте осторожны при работе с сетевыми ресурсами",
                "💡 Контекстный совет: Создавайте локальные копии сетевых файлов",
                "💡 Контекстный совет: Проверьте права доступа к сетевым папкам"
            ],
            "low_disk_space": [
                "💡 Контекстный совет: На диске мало свободного места",
                "💡 Контекстный совет: Освободите место перед обработкой больших файлов",
                "💡 Контекстный совет: Проверьте доступное место на целевом диске"
            ],
            "unsupported_format": [
                "💡 Контекстный совет: Формат файла не поддерживается",
                "💡 Контекстный совет: Проверьте список поддерживаемых форматов",
                "💡 Контекстный совет: Конвертируйте файл в поддерживаемый формат"
            ],
            "performance_issue": [
                "💡 Контекстный совет: Операция выполняется медленно",
                "💡 Контекстный совет: Закройте другие приложения для повышения производительности",
                "💡 Контекстный совет: Используйте более простой метод для ускорения"
            ],
            "backup_recommended": [
                "💡 Контекстный совет: Рекомендуется создать резервную копию",
                "💡 Контекстный совет: Автоматическое резервное копирование включено",
                "💡 Контекстный совет: Проверьте настройки резервного копирования"
            ]
        }
        self.last_tip_index = -1
        self.rule_weights = {}
        self.initialize_rule_weights()

    def initialize_rule_weights(self):
        """Инициализирует веса правил для приоритизации"""
        self.rule_weights = {
            "small_container": 10,
            "low_disk_space": 9,
            "unsupported_format": 8,
            "high_capacity_usage": 7,
            "password_weak": 6,
            "large_file": 5,
            "low_contrast": 4,
            "performance_issue": 3,
            "backup_recommended": 2,
            "audio_container": 1,
            "jpeg_container": 1,
            "multiple_files": 1,
            "network_share": 1,
            "first_time": 0
        }

    def get_next_tip(self):
        """Возвращает следующий совет"""
        self.last_tip_index = (self.last_tip_index + 1) % len(self.tips)
        return self.tips[self.last_tip_index]

    def get_contextual_tip(self, context):
        """Возвращает контекстный совет в зависимости от ситуации"""
        if context in self.context_rules:
            tips = self.context_rules[context]
            return tips[self.last_tip_index % len(tips)]
        else:
            return self.get_next_tip()

    def analyze_situation(self, container_path=None, data_size=0, operation_type=None):
        """Анализирует текущую ситуацию и возвращает список контекстов с приоритетами"""
        contexts = []

        if not container_path:
            contexts.append(("first_time", self.rule_weights.get("first_time", 0)))
            return contexts

        try:
            # Проверка на низкий контраст (для изображений)
            if container_path.lower().endswith(('.png', '.bmp', '.tiff', '.tga', '.jpg', '.jpeg')):
                try:
                    from PIL import Image, ImageStat
                    with Image.open(container_path) as img:
                        if img.mode != 'L':
                            img_gray = img.convert('L')
                        else:
                            img_gray = img
                        stat = ImageStat.Stat(img_gray)
                        contrast = stat.stddev[0] / 128.0
                        if contrast < 0.2:
                            contexts.append(("low_contrast", self.rule_weights.get("low_contrast", 0)))
                except:
                    pass

            # Проверка вместимости
            if container_path.lower().endswith(".wav"):
                contexts.append(("audio_container", self.rule_weights.get("audio_container", 0)))
                with wave.open(container_path, 'rb') as wav:
                    available_bits = wav.getnframes()
            elif container_path.lower().endswith(('.jpg', '.jpeg')):
                contexts.append(("jpeg_container", self.rule_weights.get("jpeg_container", 0)))
                w, h, available_bits = ImageProcessor.get_image_info(container_path)
            else:
                w, h, available_bits = ImageProcessor.get_image_info(container_path)

            required_bits = data_size * 8

            if required_bits > available_bits * 0.9:
                contexts.append(("high_capacity_usage", self.rule_weights.get("high_capacity_usage", 0)))
            if required_bits > available_bits:
                contexts.append(("small_container", self.rule_weights.get("small_container", 0)))

            if data_size > 10 * 1024 * 1024:  # 10 MB
                contexts.append(("large_file", self.rule_weights.get("large_file", 0)))

            # Проверка свободного места
            free_space_mb = Utils.get_free_space_mb(os.path.dirname(container_path))
            if free_space_mb < 100:  # Меньше 100 МБ свободно
                contexts.append(("low_disk_space", self.rule_weights.get("low_disk_space", 0)))

            # Проверка на сетевой путь
            if container_path.startswith(('\\\\', '//')) or '://' in container_path:
                contexts.append(("network_share", self.rule_weights.get("network_share", 0)))

            # Проверка формата
            if not Utils.is_supported_container(container_path):
                contexts.append(("unsupported_format", self.rule_weights.get("unsupported_format", 0)))

        except Exception as e:
            print(f"Ошибка анализа ситуации: {e}")

        # Сортировка по приоритету (высокий вес = высокий приоритет)
        contexts.sort(key=lambda x: x[1], reverse=True)

        # Возвращаем только контексты (без весов)
        return [context for context, weight in contexts]

    def get_smart_recommendation(self, container_path, data_size, operation_type="hide"):
        """Возвращает интеллектуальную рекомендацию на основе анализа"""
        contexts = self.analyze_situation(container_path, data_size, operation_type)

        if not contexts:
            return self.get_next_tip()

        # Берем контекст с наивысшим приоритетом
        primary_context = contexts[0]

        # Получаем рекомендацию для этого контекста
        recommendation = self.get_contextual_tip(primary_context)

        # Добавляем дополнительные рекомендации если есть
        if len(contexts) > 1:
            secondary_context = contexts[1]
            secondary_tip = self.get_contextual_tip(secondary_context)
            if secondary_tip != recommendation:
                recommendation += f"\n\n{secondary_tip}"

        return recommendation

    def learn_from_user_action(self, action, success=True):
        """Учится на действиях пользователя"""
        # Здесь можно добавить логику машинного обучения
        # для улучшения рекомендаций со временем
        pass

    def get_method_recommendation(self, container_path, data_size):
        """Рекомендует лучший метод на основе характеристик"""
        if not container_path:
            return "lsb"

        ext = os.path.splitext(container_path)[1].lower()

        if ext == '.wav':
            return "audio_lsb"
        elif ext in ['.jpg', '.jpeg']:
            return "jpeg_dct"
        elif data_size > 5 * 1024 * 1024:  # >5MB
            return "lsb"
        else:
            # Для маленьких файлов рекомендуем более скрытные методы
            contexts = self.analyze_situation(container_path, data_size)
            if "low_contrast" in contexts:
                return "hill"
            else:
                return "noise"


# ───────────────────────────────────────────────
# 🎨 УЛУЧШЕННЫЙ КЛАСС ПРОВЕРКИ ПАРОЛЯ
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
# 🧠 КЛАСС ПРОДВИНУТЫХ СТЕГО-МЕТОДОВ (БЕЗ ИЗМЕНЕНИЙ)
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
        # Целочисленный тай-брейк от RNG — строго детерминирован
        tie = rng.integers(0, np.iinfo(np.int64).max, size=cost_flat.size, dtype=np.int64)
        # np.lexsort: последний ключ — первичный
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
                # Переинициализируем RNG — порядок должен совпасть полностью
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
    def hide_dct(container_path: str, data: bytes, password: str, output_path: str,
                 progress_callback=None, cancel_event=None) -> None:
        """
        Скрывает данные в JPEG изображении методом DCT.

        Физический смысл:
        1. Блоки 8x8 - JPEG использует разбиение на такие блоки для независимой обработки
        2. DCT преобразует пространственную информацию в частотную
        3. Среднечастотные коэффициенты лучше подходят для скрытия - они менее заметны для глаза
           и менее подвержены сжатию
        """
        try:
            # Загружаем изображение
            img = cv2.imread(container_path)
            if img is None:
                raise ValueError("Не удалось загрузить изображение")

            # Преобразуем в YCbCr (цветовое пространство JPEG)
            img_ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

            # Используем канал Y (яркость)
            # Глаз менее чувствителен к изменениям яркости в высокочастотных компонентах
            y_channel = img_ycbcr[:, :, 0].astype(np.float32)

            # Получаем размеры
            h, w = y_channel.shape

            # Разбиваем на блоки 8x8
            h_blocks = h // 8
            w_blocks = w // 8

            # Упаковываем данные с заголовком
            full_data = JPEGStego._pack_data_with_header(data)
            data_bits = np.unpackbits(np.frombuffer(full_data, dtype=np.uint8))

            # Проверяем вместимость
            # В каждом блоке можно встроить 1 бит в один из среднечастотных коэффициентов
            max_capacity = h_blocks * w_blocks

            if len(data_bits) > max_capacity:
                raise ValueError(
                    f"Данные слишком велики для изображения. "
                    f"Максимум: {max_capacity // 8} байт, требуется: {len(full_data)} байт"
                )

            # Коэффициенты DCT для встраивания (средние частоты)
            # Выбираем коэффициенты (4,4) и (5,5) - они устойчивы к сжатию
            embed_positions = [(4, 4), (5, 5), (4, 5), (5, 4)]

            bit_index = 0
            total_bits = len(data_bits)

            # Проходим по всем блокам
            for i in range(h_blocks):
                for j in range(w_blocks):
                    if cancel_event and cancel_event.is_set():
                        raise InterruptedError("Операция отменена пользователем")

                    # Берём блок 8x8
                    block = y_channel[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8]

                    # Применяем DCT (2D DCT через два 1D DCT)
                    dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')

                    # Встраиваем данные если ещё есть биты
                    if bit_index < total_bits:
                        # Выбираем позицию для встраивания (чередуем для равномерности)
                        pos_idx = (i * w_blocks + j) % len(embed_positions)
                        u, v = embed_positions[pos_idx]

                        # Получаем текущее значение коэффициента
                        coeff = dct_block[u, v]

                        # Встраиваем бит методом LSB
                        bit = data_bits[bit_index]
                        if bit == 1:
                            # Устанавливаем младший бит в 1
                            if int(coeff) % 2 == 0:
                                dct_block[u, v] = coeff + 1 if coeff >= 0 else coeff - 1
                        else:
                            # Устанавливаем младший бит в 0
                            if int(coeff) % 2 == 1:
                                dct_block[u, v] = coeff - 1 if coeff >= 0 else coeff + 1

                        bit_index += 1

                    # Обратное DCT
                    idct_block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')

                    # Возвращаем блок на место
                    y_channel[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8] = idct_block

                    # Обновляем прогресс
                    if progress_callback and (i * w_blocks + j) % 100 == 0:
                        progress = (i * w_blocks + j) / (h_blocks * w_blocks) * 100
                        progress_callback(progress, f"Обработано блоков: {i * w_blocks + j}/{h_blocks * w_blocks}")

            # Обрезаем значения до допустимого диапазона
            y_channel = np.clip(y_channel, 0, 255)

            # Обновляем канал Y
            img_ycbcr[:, :, 0] = y_channel.astype(np.uint8)

            # Конвертируем обратно в BGR
            img_stego = cv2.cvtColor(img_ycbcr, cv2.COLOR_YCrCb2BGR)

            # Сохраняем с минимальным JPEG сжатием для сохранения данных
            cv2.imwrite(output_path, img_stego, [cv2.IMWRITE_JPEG_QUALITY, 95])

            if progress_callback:
                progress_callback(100.0, "✅ Данные успешно скрыты")

        except Exception as e:
            raise Exception(f"Ошибка при скрытии данных JPEG DCT: {str(e)}")

    @staticmethod
    def extract_dct(stego_path: str, password: str, progress_callback=None, cancel_event=None) -> bytes:
        """
        Извлекает данные из JPEG изображения, скрытые методом DCT.

        Процесс:
        1. Разбиение на блоки 8x8
        2. Применение DCT к каждому блоку
        3. Чтение битов из тех же коэффициентов
        4. Сбор данных и проверка целостности
        """
        try:
            # Загружаем изображение
            img = cv2.imread(stego_path)
            if img is None:
                raise ValueError("Не удалось загрузить изображение")

            # Преобразуем в YCbCr
            img_ycbcr = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            y_channel = img_ycbcr[:, :, 0].astype(np.float32)

            # Размеры
            h, w = y_channel.shape
            h_blocks = h // 8
            w_blocks = w // 8

            # Коэффициенты для извлечения (должны совпадать с встраиванием)
            embed_positions = [(4, 4), (5, 5), (4, 5), (5, 4)]

            # Максимальное количество бит, которое можно извлечь
            max_bits = h_blocks * w_blocks

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
                    if progress_callback and (i * w_blocks + j) % 100 == 0:
                        progress = (i * w_blocks + j) / (h_blocks * w_blocks) * 100
                        progress_callback(progress, f"Извлечение блоков: {i * w_blocks + j}/{h_blocks * w_blocks}")

            # Преобразуем биты в байты
            extracted_bytes = np.packbits(extracted_bits).tobytes()

            # Пытаемся распаковать данные
            # Ищем заголовок в извлеченных данных
            try:
                # Пробуем разные смещения на случай ошибок синхронизации
                for offset in range(0, min(100, len(extracted_bytes) - 12)):
                    try:
                        data = JPEGStego._unpack_data_with_header(extracted_bytes[offset:])
                        if progress_callback:
                            progress_callback(100.0, "✅ Данные успешно извлечены")
                        return data
                    except:
                        continue

                raise ValueError("Не удалось найти валидные данные")

            except Exception as e:
                raise ValueError(f"Ошибка при распаковке данных: {str(e)}")

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
# 🖼️ КЛАСС ДЛЯ РАБОТЫ С ИЗОБРАЖЕНИЯМИ (БЕЗ ИЗМЕНЕНИЙ)
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
            return (0, 0, frames)

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

            # Добавьте обработку JPEG DCT
            if method == "jpeg_dct":
                JPEGStego.hide_dct(
                    container_path, data, password, output_path,
                    progress_callback, cancel_event
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
            methods_to_try = ["lsb", "noise", "aelsb", "hill"]

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
# 🎯 ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ (ПОЛНОСТЬЮ ПЕРЕРАБОТАННЫЙ ИНТЕРФЕЙС)
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
        self.achievement_manager = AchievementManager()
        self.smart_assistant = SmartAssistant(self)
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
            "confirm_before_exit": True,
            "show_achievements": True
        }

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
            "show_achievements": self.settings.get("show_achievements", True)
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
        tip = self.smart_assistant.get_contextual_tip("first_time")
        self.notification_manager.show_notification(
            f"Добро пожаловать в ØccultoNG Pro v{VERSION}!{tip}",
            "info",
            5000
        )

    def create_batch_tab(self):
        """Создает вкладку пакетной обработки"""
        self.batch_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.batch_tab, text="📦 Пакетная обработка")

        # Инициализация UI пакетной обработки
        self.batch_ui = BatchProcessingUI(self.batch_tab, self)

        # Обновляем SmartAssistant
        self.smart_assistant = SmartAssistant(self)

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
        self.create_settings_tab()

        # Убедимся, что статистика и достижения создаются правильно
        self.create_statistics_tab()  # Создаем вкладку "Статистика"
        self.create_achievements_tab()  # Создаем вкладку "Достижения"
        self.create_help_tab()  # Создаем вкладку "Помощь"

        # Добавляем вкладки в notebook с правильными текстами и иконками
        self.notebook.add(self.hide_tab, text="📦 Скрыть данные")
        self.notebook.add(self.extract_tab, text="🔍 Извлечь данные")
        self.notebook.add(self.settings_tab, text="⚙️ Настройки")
        self.notebook.add(self.statistics_tab, text="📊 Статистика")  # Правильное имя вкладки
        self.notebook.add(self.achievements_tab, text="🏆 Достижения")  # Правильное имя вкладки
        self.notebook.add(self.help_tab, text="❓ Помощь")
        self.create_batch_tab()  # Создаем вкладку пакетной обработки

        # Создаем тост
        self.create_toast()

        # Создаем панель быстрого доступа
        self.create_quick_access_panel(main_frame)

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

    def create_quick_access_panel(self, parent: ttk.Frame) -> None:
        """Создает панель быстрого доступа"""
        quick_frame = ttk.Frame(parent, style="Card.TFrame")
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        # Заголовок панели
        ttk.Label(
            quick_frame,
            text="⚡ Быстрый доступ",
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["accent"],
            style="TLabel"
        ).pack(side=tk.LEFT, padx=(0, 20))
        # Кнопки быстрого доступа
        quick_buttons = [
            ("📂 Открыть контейнер", self.select_image, "Ctrl+O"),
            ("🔐 Скрыть данные", self.start_hide, "Ctrl+Enter"),
            ("🔍 Извлечь данные", self.start_extract, "Ctrl+E"),
            ("💾 Сохранить результат", self.save_extracted, "Ctrl+S"),
            ("⚙️ Настройки", lambda: self.notebook.select(self.settings_tab), "Ctrl+,"),
            ("📊 Статистика", lambda: self.notebook.select(self.statistics_tab), "Ctrl+Shift+S"),
            ("🏆 Достижения", lambda: self.notebook.select(self.achievements_tab), "Ctrl+Shift+A"),
            ("❓ Помощь", self.show_help, "F1")
        ]
        for text, command, shortcut in quick_buttons:
            btn_frame = ttk.Frame(quick_frame, style="Card.TFrame")
            btn_frame.pack(side=tk.LEFT, padx=(0, 10))
            btn = ttk.Button(
                btn_frame,
                text=text,
                command=command,
                style="CardButton.TButton"
            )
            btn.pack(side=tk.LEFT)
            ToolTip(btn, f"{text}{shortcut}")

    def create_hide_tab(self) -> None:
        self.hide_tab = ttk.Frame(self.notebook, style="Card.TFrame", padding=15)
        self.notebook.add(self.hide_tab, text="📦 Скрыть данные")

        # Создаем две колонки
        left_frame = ttk.Frame(self.hide_tab, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_frame = ttk.Frame(self.hide_tab, style="Card.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

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

        # Создаем две колонки
        left_frame = ttk.Frame(self.extract_tab, style="Card.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_frame = ttk.Frame(self.extract_tab, style="Card.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

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

        # Показывать достижения
        self.show_achievements_var = tk.BooleanVar(value=self.settings.get("show_achievements", True))
        achievements_check = ttk.Checkbutton(
            extra_group,
            text="Показывать уведомления о достижениях",
            variable=self.show_achievements_var,
            style="TCheckbutton"
        )
        achievements_check.pack(anchor="w", pady=(0, 5))

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
• Python 3.10+ — платформа приложения
• Pillow — работа с изображениями (PNG/BMP/TIFF/TGA/JPG)
• NumPy + Numba — быстрые битовые операции/индексация
• SciPy (ndimage) — фильтры/карты стоимости для адаптивных методов
• tkinter + tkinterdnd2 — UI и drag‑and‑drop
• wave — чтение/запись PCM‑сэмплов для WAV‑LSB
📦 Контейнеры: PNG • BMP • TIFF • TGA • JPG • WAV
🛡 Методы: LSB • Adaptive‑Noise • AELSB(Hamming) • HILL‑CA • WAV LSB
📜 Лицензия: MIT — используйте, модифицируйте, делитесь свободно.
💡 Советы:
• Для изображений — используйте lossless‑форматы (PNG/BMP/TIFF).
• Для аудио — используйте несжатый WAV; любое перекодирование/сжатие может разрушить скрытые биты.
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

    def create_achievements_tab(self) -> None:
        self.achievements_tab = ttk.Frame(self.notebook, style="Card.TFrame")
        self.notebook.add(self.achievements_tab, text="🏆 Достижения")

        # Создаем canvas с прокруткой
        achievements_canvas = tk.Canvas(self.achievements_tab, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(self.achievements_tab, orient="vertical", command=achievements_canvas.yview)
        scrollable_frame = ttk.Frame(achievements_canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: achievements_canvas.configure(scrollregion=achievements_canvas.bbox("all"))
        )

        achievements_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        achievements_canvas.configure(yscrollcommand=scrollbar.set)

        achievements_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовок
        ttk.Label(
            scrollable_frame,
            text="🏆 Ваши достижения в ØccultoNG Pro",
            font=("Segoe UI Variable Display", 18, "bold"),
            foreground=self.colors["accent"],
            style="TLabel"
        ).pack(pady=(20, 30))

        # Разблокированные достижения
        unlocked_group = ttk.LabelFrame(
            scrollable_frame,
            text="✅ Разблокированные достижения",
            padding=15,
            style="Card.TLabelframe"
        )
        unlocked_group.pack(fill=tk.X, pady=(0, 15))

        unlocked_achievements = self.achievement_manager.get_unlocked_achievements()

        if unlocked_achievements:
            for key, achievement in unlocked_achievements.items():
                self.create_achievement_card(unlocked_group, achievement, unlocked=True)
        else:
            ttk.Label(
                unlocked_group,
                text="У вас пока нет разблокированных достижений. Начните использовать программу!",
                style="Secondary.TLabel",
                wraplength=800
            ).pack(pady=20)

        # Заблокированные достижения
        locked_group = ttk.LabelFrame(
            scrollable_frame,
            text="🔒 Достижения для разблокировки",
            padding=15,
            style="Card.TLabelframe"
        )
        locked_group.pack(fill=tk.X, pady=(0, 15))

        locked_achievements = self.achievement_manager.get_locked_achievements()

        if locked_achievements:
            for key, achievement in locked_achievements.items():
                self.create_achievement_card(locked_group, achievement, unlocked=False)
        else:
            ttk.Label(
                locked_group,
                text="Поздравляем! Вы разблокировали все достижения!",
                style="Success.TLabel",
                wraplength=800
            ).pack(pady=20)

        # Статистика достижений
        stats_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        total_achievements = len(self.achievement_manager.achievements)
        unlocked_count = len(unlocked_achievements)
        locked_count = len(locked_achievements)
        completion_percentage = (unlocked_count / total_achievements * 100) if total_achievements > 0 else 0

        ttk.Label(
            stats_frame,
            text=f"Прогресс: {unlocked_count}/{total_achievements} ({completion_percentage:.1f}%)",
            font=("Segoe UI", 12, "bold"),
            style="TLabel"
        ).pack(pady=10)

        # Прогресс-бар
        progress_bar = ttk.Progressbar(
            stats_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="TProgressbar"
        )
        progress_bar.pack(pady=(0, 10))
        progress_bar["value"] = completion_percentage

        # Кнопки
        btn_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="🔄 Обновить",
            style="TButton",
            command=self.refresh_achievements
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            btn_frame,
            text="🎁 Показать все",
            style="TButton",
            command=self.show_all_achievements
        ).pack(side=tk.LEFT, padx=10)

    def create_achievement_card(self, parent, achievement, unlocked=True):
        """Создает карточку достижения"""
        card_frame = ttk.Frame(parent, style="Card.TFrame")
        card_frame.pack(fill=tk.X, pady=5, padx=5)

        # Основная информация
        info_frame = ttk.Frame(card_frame, style="Card.TFrame")
        info_frame.pack(fill=tk.X, pady=5)

        # Иконка и название
        title_frame = ttk.Frame(info_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT)

        icon_label = tk.Label(
            title_frame,
            text=achievement["icon"],
            font=("Segoe UI", 16),
            bg=self.colors["card"],
            fg=self.colors["accent"] if unlocked else self.colors["text_secondary"]
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))

        name_label = ttk.Label(
            title_frame,
            text=achievement["name"],
            font=("Segoe UI", 12, "bold"),
            foreground=self.colors["text"] if unlocked else self.colors["text_secondary"],
            style="TLabel"
        )
        name_label.pack(side=tk.LEFT)

        # Прогресс
        if not unlocked:
            progress_frame = ttk.Frame(info_frame, style="Card.TFrame")
            progress_frame.pack(side=tk.RIGHT)

            current, target = achievement["progress"], achievement["target"]
            percentage = (current / target * 100) if target > 0 else 0

            ttk.Label(
                progress_frame,
                text=f"{current}/{target}",
                font=("Segoe UI", 10),
                style="Secondary.TLabel"
            ).pack(side=tk.LEFT, padx=(0, 5))

            progress_bar = ttk.Progressbar(
                progress_frame,
                orient="horizontal",
                length=100,
                mode="determinate",
                style="TProgressbar"
            )
            progress_bar.pack(side=tk.LEFT)
            progress_bar["value"] = percentage

        # Описание
        desc_label = ttk.Label(
            card_frame,
            text=achievement["description"],
            font=("Segoe UI", 10),
            foreground=self.colors["text"] if unlocked else self.colors["text_secondary"],
            style="Secondary.TLabel",
            wraplength=700,
            justify=tk.LEFT
        )
        desc_label.pack(anchor="w", padx=(30, 0), pady=(0, 5))

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
            ("5. Советы и рекомендации", self.show_help_tips),
            ("6. Горячие клавиши", self.show_help_shortcuts),
            ("7. Часто задаваемые вопросы", self.show_help_faq),
            ("8. Техническая поддержка", self.show_help_support)
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

    ØccultoNG Pro — это профессиональный инструмент для стеганографии,
    позволяющий скрывать тексты и файлы внутри изображений и аудиофайлов
    без потерь, с автоматическим извлечением и проверкой целостности.

    🚀 ОСНОВНЫЕ ВОЗМОЖНОСТИ:
    • Поддержка различных методов скрытия данных
    • Работа с изображениями (PNG, BMP, TIFF, TGA, JPG) и аудио (WAV)
    • Автоматическое определение метода при извлечении
    • Пакетная обработка до 5 файлов одновременно ✅ НОВОЕ!
    • Расширенная статистика и достижения
    • Интеллектуальные подсказки и ассистент
    • Поддержка плагинов и расширений

    📋 ОСНОВНЫЕ ВКЛАДКИ:
    1. 📦 Скрыть данные — скрытие данных в одном контейнере
    2. 🔍 Извлечь данные — извлечение скрытых данных
    3. 📦 Пакетная обработка — одновременная обработка до 5 файлов
    4. ⚙️ Настройки — настройка программы и темы
    5. 📊 Статистика — просмотр статистики использования
    6. 🏆 Достижения — ваши достижения в программе
    7. ❓ Помощь — это окно с руководством

    💡 СОВЕТ: Начните с выбора вкладки "Скрыть данные" или "Извлечь данные"
    в верхней части окна. Для работы с несколькими файлами используйте
    вкладку "Пакетная обработка".

    🎮 ДОСТИЖЕНИЯ: Следите за своими достижениями в соответствующей вкладке!
    📈 СТАТИСТИКА: Отслеживайте свою активность и прогресс!
    🤖 АССИСТЕНТ: Используйте интеллектуальные подсказки для лучших результатов!
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
       • Начните обработку — все файлы будут обработаны автоматически

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
    • Экономия времени — не нужно обрабатывать каждый файл отдельно
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
    • Если кнопки остаются заблокированными — нажмите "Очистить все"
    • Если обработка зависла — используйте кнопку "Остановить обработку"
    • Если файлы не обрабатываются — проверьте формат и права доступа
    • Для повторной обработки тех же файлов — очистите список и добавьте заново

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

    🎮 ДОСТИЖЕНИЯ, связанные с пакетной обработкой:
    • "Конвейер" — выполните первую пакетную операцию
    • "Мультитаскинг" — обработайте 5 файлов одновременно
    • "Эксперт по анализу" — проанализируйте 10 файлов
    • "Массовое скрытие" — скройте данные в 3 разных типах контейнеров
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

    ОСНОВНАЯ РАБОТА:

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

    📦 ПАКЕТНАЯ ОБРАБОТКА (НОВОЕ!):

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

    Интеллектуальный ассистент:
    • Программа анализирует ваши действия и дает советы
    • Автоматически рекомендует оптимальные методы
    • Предупреждает о потенциальных проблемах
    • Учится на ваших предпочтениях

    Расширенная статистика:
    • Отслеживание всех операций
    • Анализ использования методов
    • История успешных и неудачных операций
    • Визуализация данных

    Система достижений:
    • Разблокируйте достижения за использование функций
    • Следите за прогрессом
    • Получайте мотивацию для освоения всех возможностей

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
    • Если нужно обработать больше файлов — разбейте на несколько партий

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

    🤖 СОВЕТЫ ПО ИСПОЛЬЗОВАНИЮ АССИСТЕНТА:
    • Внимательно читайте контекстные подсказки
    • Следуйте рекомендациям по выбору метода
    • Используйте анализ ситуации для предотвращения ошибок
    • Обращайте внимание на предупреждения о проблемах

    📊 СОВЕТЫ ПО СТАТИСТИКЕ:
    • Регулярно проверяйте статистику использования
    • Анализируйте наиболее часто используемые методы
    • Используйте историю операций для отладки проблем
    • Экспортируйте статистику для отчетов

    🏆 СОВЕТЫ ПО ДОСТИЖЕНИЯМ:
    • Следите за прогрессом в достижениях
    • Ставьте цели по разблокировке достижений
    • Используйте достижения как руководство по изучению функций
    • Делитесь достижениями с коллегами

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
    • F1 — Открыть помощь
    • Esc — Отменить текущую операцию
    • Ctrl+Enter — Выполнить основное действие на активной вкладке
    • Ctrl+O — Выбрать контейнер (на активной вкладке)
    • Ctrl+E — Извлечь данные
    • Ctrl+S — Сохранить извлеченные данные
    • Ctrl+L — Очистить текстовое поле
    • Ctrl+T — Переключить тему

    НА ВКЛАДКЕ "СКРЫТЬ ДАННЫЕ":
    • Ctrl+1 — Выбрать метод "Классический LSB"
    • Ctrl+2 — Выбрать метод "Adaptive-Noise"
    • Ctrl+3 — Выбрать метод "Adaptive-Edge-LSB"
    • Ctrl+4 — Выбрать метод "HILL-CA"
    • Ctrl+5 — Выбрать метод "WAV LSB"
    • Ctrl+6 — Выбрать метод "JPEG DCT"

    НА ВКЛАДКЕ "ИЗВЛЕЧЬ ДАННЫЕ":
    • Ctrl+R — Обновить предпросмотр
    • Ctrl+C — Копировать извлеченные данные
    • Ctrl+H — Копировать хеш извлеченных данных
    • Ctrl+F — Найти в извлеченных данных

    НА ВКЛАДКЕ "ПАКЕТНАЯ ОБРАБОТКА" (НОВОЕ!):
    • Ctrl+B — Переключиться на вкладку пакетной обработки
    • Ctrl+Shift+H — Быстрый доступ к пакетному скрытию
    • Ctrl+Shift+E — Быстрый доступ к пакетному извлечению
    • Ctrl+Shift+A — Быстрый доступ к пакетному анализу
    • Ctrl+Shift+C — Очистить все списки в пакетной обработке
    • Ctrl+Shift+X — Экспорт результатов пакетной обработки

    ОБЩИЕ:
    • Ctrl+Tab — Переключиться на следующую вкладку
    • Ctrl+Shift+Tab — Переключиться на предыдущую вкладку
    • Ctrl+, — Открыть настройки
    • Ctrl+Q — Выйти из программы
    • Ctrl+Shift+S — Открыть статистику
    • Ctrl+Shift+D — Открыть достижения

    РАБОТА С ФАЙЛАМИ:
    • Ctrl+N — Создать новый проект
    • Ctrl+O — Открыть файл
    • Ctrl+Shift+O — Открыть несколько файлов (пакетная обработка)
    • Ctrl+W — Закрыть текущий файл
    • Ctrl+Shift+W — Закрыть все файлы

    РЕДАКТИРОВАНИЕ:
    • Ctrl+Z — Отменить
    • Ctrl+Y — Повторить
    • Ctrl+X — Вырезать
    • Ctrl+C — Копировать
    • Ctrl+V — Вставить
    • Ctrl+A — Выделить все
    • Ctrl+F — Найти
    • Ctrl+H — Заменить

    ПРОСМОТР:
    • Ctrl++ — Увеличить масштаб
    • Ctrl+- — Уменьшить масштаб
    • Ctrl+0 — Сбросить масштаб
    • F11 — Полноэкранный режим
    • Alt+Enter — Свойства файла

    СИСТЕМНЫЕ:
    • Alt+F4 — Закрыть программу
    • Alt+Tab — Переключение между приложениями
    • Win+D — Показать рабочий стол
    • Win+E — Открыть проводник

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
       вкладку и обратно. Если не помогает — перезапустите программу.

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

    🤖 ВОПРОСЫ ПО АССИСТЕНТУ:

    Q: Как работает интеллектуальный ассистент?
    A: Ассистент анализирует:
       1. Тип и размер контейнера
       2. Размер скрываемых данных
       3. Выбранный метод
       4. Системные ресурсы
       И дает рекомендации на основе этих данных.

    Q: Можно ли отключить подсказки ассистента?
    A: Да, в настройках программы есть опция "Показывать подсказки и советы".

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

            # Разблокируем достижения
            self.achievement_manager.increment_progress("first_hide")
            self.achievement_manager.increment_progress("five_operations")
            self.achievement_manager.increment_progress("ten_operations")
            self.achievement_manager.increment_progress("twenty_operations")

            if len(data) > 10 * 1024 * 1024:  # 10 MB
                self.achievement_manager.increment_progress("large_file")

            if method == "audio_lsb":
                self.achievement_manager.increment_progress("audio_expert")

            # Показываем уведомление о достижении если нужно
            if self.settings.get("show_achievements", True):
                unlocked = self.achievement_manager.increment_progress("multiple_methods")
                if unlocked:
                    self.notification_manager.show_notification(
                        f"🏆 Новое достижение разблокировано!\
{self.achievement_manager.achievements['multiple_methods']['name']}",
                        "success",
                        5000
                    )

            def after_success():
                messagebox.showinfo(
                    "✅ Успех",
                    f"🎉 Данные успешно скрыты в {'аудиофайле' if ext == '.wav' else 'изображении'}!\
            Файл сохранён: {output}"
                )
                if messagebox.askyesno("📂 Открыть папку", "Открыть папку с сохраненным файлом?"):
                    Utils.open_in_file_manager(output)
                # Показываем подсказку от ассистента
                if self.settings.get("show_tips", True):
                    # Analyze the current situation to get a context
                    container_path = img_path
                    data_size = len(data)
                    context = self.smart_assistant.analyze_situation(container_path, data_size)
                    if context:
                        tip = self.smart_assistant.get_contextual_tip(context)
                    else:
                        tip = self.smart_assistant.get_next_tip()
                    self.notification_manager.show_notification(tip, "info", 4000)

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

            # Разблокируем достижения
            self.achievement_manager.increment_progress("first_extract")
            self.achievement_manager.increment_progress("five_operations")
            self.achievement_manager.increment_progress("ten_operations")
            self.achievement_manager.increment_progress("twenty_operations")

            # Показываем уведомление о достижении если нужно
            if self.settings.get("show_achievements", True):
                unlocked = self.achievement_manager.increment_progress("multiple_methods")
                if unlocked:
                    self.notification_manager.show_notification(
                        f"🏆 Новое достижение разблокировано!\
{self.achievement_manager.achievements['multiple_methods']['name']}",
                        "success",
                        5000
                    )

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
        self.settings["show_achievements"] = self.show_achievements_var.get()

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
                    "show_achievements": self.settings.get("show_achievements", True),
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
                            "show_tips", "auto_backup", "confirm_before_exit", "show_achievements"]:
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
                if hasattr(self, 'show_achievements_var'):
                    self.show_achievements_var.set(self.settings.get("show_achievements", True))

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
                    "achievements": self.achievement_manager.achievements,
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

    def refresh_achievements(self):
        """Обновляет достижения"""
        # 1. Перезагружаем данные
        self.achievement_manager = AchievementManager()

        # 2. Очищаем содержимое существующей вкладки (НЕ удаляем саму вкладку!)
        for widget in self.achievements_tab.winfo_children():
            widget.destroy()

        # 3. Воссоздаем UI ВНУТРИ существующей вкладки
        parent_frame = self.achievements_tab

        # Создаем canvas с прокруткой
        achievements_canvas = tk.Canvas(parent_frame, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=achievements_canvas.yview)
        scrollable_frame = ttk.Frame(achievements_canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: achievements_canvas.configure(scrollregion=achievements_canvas.bbox("all"))
        )

        achievements_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        achievements_canvas.configure(yscrollcommand=scrollbar.set)

        achievements_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовок
        ttk.Label(scrollable_frame, text="🏆 Ваши достижения в ØccultoNG Pro",
                  font=("Segoe UI Variable Display", 18, "bold"), foreground=self.colors["accent"],
                  style="TLabel").pack(pady=(20, 30))

        # Разблокированные достижения
        unlocked_group = ttk.LabelFrame(scrollable_frame, text="✅ Разблокированные достижения", padding=15,
                                        style="Card.TLabelframe")
        unlocked_group.pack(fill=tk.X, pady=(0, 15))
        unlocked_achievements = self.achievement_manager.get_unlocked_achievements()
        if unlocked_achievements:
            for key, achievement in unlocked_achievements.items():
                self.create_achievement_card(unlocked_group, achievement, unlocked=True)
        else:
            ttk.Label(unlocked_group,
                      text="У вас пока нет разблокированных достижений. Начните использовать программу!",
                      style="Secondary.TLabel", wraplength=800).pack(pady=20)

        # Заблокированные достижения
        locked_group = ttk.LabelFrame(scrollable_frame, text="🔒 Достижения для разблокировки", padding=15,
                                      style="Card.TLabelframe")
        locked_group.pack(fill=tk.X, pady=(0, 15))
        locked_achievements = self.achievement_manager.get_locked_achievements()
        if locked_achievements:
            for key, achievement in locked_achievements.items():
                self.create_achievement_card(locked_group, achievement, unlocked=False)
        else:
            ttk.Label(locked_group, text="Поздравляем! Вы разблокировали все достижения!", style="Success.TLabel",
                      wraplength=800).pack(pady=20)

        # Статистика достижений
        stats_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        total_achievements = len(self.achievement_manager.achievements)
        completion_percentage = (len(unlocked_achievements) / total_achievements * 100) if total_achievements > 0 else 0
        ttk.Label(stats_frame,
                  text=f"Прогресс: {len(unlocked_achievements)}/{total_achievements} ({completion_percentage:.1f}%)",
                  font=("Segoe UI", 12, "bold"), style="TLabel").pack(pady=10)
        progress_bar = ttk.Progressbar(stats_frame, orient="horizontal", length=400, mode="determinate",
                                       style="TProgressbar")
        progress_bar.pack(pady=(0, 10))
        progress_bar["value"] = completion_percentage

        # Кнопки
        btn_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="🔄 Обновить", style="TButton", command=self.refresh_achievements).pack(side=tk.LEFT,
                                                                                                          padx=10)
        ttk.Button(btn_frame, text="🎁 Показать все", style="TButton", command=self.show_all_achievements).pack(
            side=tk.LEFT, padx=10)

        # 4. Переключаемся на вкладку, чтобы пользователь видел результат
        self.notebook.select(self.achievements_tab)
        messagebox.showinfo("✅ Обновление", "Достижения успешно обновлены!")

    def show_all_achievements(self):
        """Показывает все достижения"""
        # Создаем окно со всеми достижениями
        achievements_window = tk.Toplevel(self.root)
        achievements_window.title("🏆 Все достижения")
        achievements_window.geometry("800x600")
        achievements_window.transient(self.root)
        achievements_window.grab_set()

        # Создаем canvas с прокруткой
        canvas = tk.Canvas(achievements_window, bg=self.colors["bg"])
        scrollbar = ttk.Scrollbar(achievements_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Card.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовок
        ttk.Label(
            scrollable_frame,
            text="🏆 Все достижения в ØccultoNG Pro",
            font=("Segoe UI Variable Display", 16, "bold"),
            foreground=self.colors["accent"],
            style="TLabel"
        ).pack(pady=(20, 30))

        # Статистика
        unlocked = len(self.achievement_manager.get_unlocked_achievements())
        total = len(self.achievement_manager.achievements)
        percentage = (unlocked / total * 100) if total > 0 else 0

        stats_frame = ttk.Frame(scrollable_frame, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        ttk.Label(
            stats_frame,
            text=f"Прогресс: {unlocked}/{total} ({percentage:.1f}%)",
            font=("Segoe UI", 12, "bold"),
            style="TLabel"
        ).pack(pady=10)

        # Прогресс-бар
        progress_bar = ttk.Progressbar(
            stats_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            style="TProgressbar"
        )
        progress_bar.pack(pady=(0, 10))
        progress_bar["value"] = percentage

        # Все достижения
        for key, achievement in self.achievement_manager.achievements.items():
            self.create_achievement_card(scrollable_frame, achievement, unlocked=achievement["unlocked"])
            ttk.Separator(scrollable_frame, orient="horizontal").pack(fill=tk.X, pady=10)

        # Кнопка закрытия
        ttk.Button(
            scrollable_frame,
            text="❌ Закрыть",
            style="TButton",
            command=achievements_window.destroy
        ).pack(pady=20)

    def show_help(self) -> None:
        """Показывает помощь"""
        self.notebook.select(self.help_tab)

    def show_container_info(self):
        """Показывает информацию о контейнере"""
        path = self.img_path.get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("❌ Ошибка", "Сначала выберите контейнер")
            return

        file_info = Utils.get_file_info(path)
        info_text = f"""
📁 Информация о контейнере

Имя файла: {file_info['name']}
Размер: {file_info['size_formatted']}
Тип: {file_info['type']}
Дата создания: {file_info['created']}
Дата изменения: {file_info['modified']}
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

    # ─────────────────────────────
    # Доп. UX утилиты
    # ─────────────────────────────
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
